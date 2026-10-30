# SQLite and local first apps

SQLite setup that does not corrupt or lock, and how to build apps that work offline and sync. Sources: SQLite docs (WAL, foreign keys, STRICT tables, when to use, backup API), Ink and Switch "Local first software" (Kleppmann et al. 2019), PowerSync consistency docs, ElectricSQL write patterns guide, SQLite forum and Bert Hubert on SQLITE_BUSY.

## Contents

1. When SQLite is the right database
2. Connection setup (the pragmas)
3. Transactions and SQLITE_BUSY
4. STRICT tables and types
5. WAL details that bite
6. Schema migrations on devices
7. Local first: what it means in code
8. Sync architectures
9. Conflict resolution: LWW, per field merge, CRDT
10. Delta sync done right
11. Checks

## 1. When SQLite is right

SQLite docs checklist, in order:

1. Is the data separated from the app by a network? Use a client/server database. (A server app on the same machine as the file is fine.)
2. Many writers at the same instant that cannot take turns? Use a client/server database. SQLite allows one writer at a time; a write transaction takes milliseconds, so modest write loads queue fine.
3. Data heading toward a terabyte? Use a client/server database.
4. Otherwise SQLite. The docs call sites under 100k hits per day a conservative safe range.

Never put a SQLite file on a network filesystem (NFS, SMB, a Docker volume backed by one): WAL needs shared memory on one host, and network file locking is unreliable, which corrupts databases.

On phones and desktops SQLite is the default local store. Prefer it (expo-sqlite, op-sqlite, rusqlite, better-sqlite3, wa-sqlite/OPFS in browsers) over IndexedDB or AsyncStorage for anything relational, and never use AsyncStorage or localStorage for data the user would miss.

## 2. Connection setup

Run on every connection, right after open, before any transaction:

```sql
PRAGMA journal_mode = WAL;        -- persistent, but setting it again is cheap and safe
PRAGMA foreign_keys = ON;         -- OFF by default, per connection, no effect inside a transaction
PRAGMA busy_timeout = 5000;       -- wait up to 5 s for a lock instead of failing at once
PRAGMA synchronous = NORMAL;      -- in WAL: safe from corruption; last commits may roll back on power loss
```

Optional, measured: `PRAGMA cache_size = -20000` (20 MB), `PRAGMA temp_store = MEMORY`, `PRAGMA mmap_size` on servers. Run `PRAGMA optimize` periodically or before closing long lived connections.

- `synchronous = NORMAL` in WAL mode never corrupts the database, but a transaction committed just before a power cut can be lost. Use `FULL` for money, medical, or anything you told the user is saved.
- Foreign keys being off by default is the most common SQLite integrity bug. Assert it in a test: `PRAGMA foreign_keys` returns 1 on a connection from your pool.

```ts
// better-sqlite3
import Database from 'better-sqlite3';
export const db = new Database(path);
db.pragma('journal_mode = WAL');
db.pragma('foreign_keys = ON');
db.pragma('busy_timeout = 5000');
db.pragma('synchronous = NORMAL');
```

```rust
// rusqlite
let conn = Connection::open(path)?;
conn.execute_batch("PRAGMA journal_mode=WAL; PRAGMA foreign_keys=ON; PRAGMA synchronous=NORMAL;")?;
conn.busy_timeout(std::time::Duration::from_secs(5))?;
// sqlx: SqliteConnectOptions::new().journal_mode(Wal).foreign_keys(true).busy_timeout(..).synchronous(Normal)
```

## 3. Transactions and SQLITE_BUSY

- A plain `BEGIN` is DEFERRED: it takes a read lock on the first read and tries to upgrade to a write lock on the first write. If another connection is writing at that moment, the upgrade fails with SQLITE_BUSY immediately, and busy_timeout does not help (waiting cannot fix it, because this transaction's snapshot is already stale).
- Fix: start every transaction that will write with `BEGIN IMMEDIATE`. It takes the write lock up front, so busy_timeout applies. Read only transactions can stay DEFERRED. You cannot upgrade DEFERRED to IMMEDIATE mid transaction.
- better-sqlite3: `db.transaction(fn).immediate()`. sqlx: there is no per call option; on a server use a single writer connection (a pool of size 1 for writes, a separate pool for reads). rusqlite: `conn.transaction_with_behavior(TransactionBehavior::Immediate)`.
- Server pattern: one writer connection (or a mutex around writes) plus N reader connections. This removes nearly all BUSY errors.
- Bulk inserts: one transaction around the whole batch. Each autocommit INSERT is its own commit and sync, which is 10 to 100 times slower.
- Keep transactions short; a long read transaction blocks WAL checkpoints (section 5).

## 4. STRICT tables and types

- Default SQLite typing is flexible: an `INTEGER` column happily stores `'abc'`. Add `STRICT` to every table (SQLite 3.37+, Nov 2021): wrong types fail with SQLITE_CONSTRAINT_DATATYPE.

```sql
create table task (
  id          text primary key,                 -- UUIDv7 minted on the device
  list_id     text not null references list(id) on delete cascade,
  title       text not null check (length(title) between 1 and 500),
  done        integer not null default 0 check (done in (0, 1)),
  due_on      text check (due_on is null or due_on glob '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]'),
  updated_at  integer not null,                 -- unix ms
  deleted_at  integer                           -- tombstone for sync, see section 10
) strict;
create index task_list_id_idx on task(list_id);  -- FK columns are not indexed automatically
```

- STRICT allows only INT, INTEGER, REAL, TEXT, BLOB, ANY. Booleans are INTEGER with a CHECK. Times are INTEGER unix ms or ISO TEXT, one choice per database.
- A table without `INTEGER PRIMARY KEY` or with `WITHOUT ROWID` behaves differently for VACUUM and performance; for text UUID keys, `WITHOUT ROWID` saves a lookup but makes wide rows slower. Default: keep rowid tables.
- Check the SQLite version shipped on the target (old Android system SQLite can be below 3.37). Bundle SQLite with the app (op-sqlite, expo-sqlite bundle it) when you need STRICT, `RETURNING` (3.35), `DROP COLUMN` (3.35) or JSONB functions (3.45).

## 5. WAL details that bite

- The database is three files: `app.db`, `app.db-wal`, `app.db-shm`. Never copy, move or delete only `app.db` while it is open: committed transactions live in the -wal file until a checkpoint. Use the backup API, `VACUUM INTO`, or Litestream (see `backups-and-recovery.md`).
- Auto checkpoint runs at 1000 pages (about 4 MB). A reader that never stops (a long query, a connection that keeps a statement open) prevents the WAL from being reset, and the -wal file grows without bound (checkpoint starvation). Finalize statements, close long reads, and if needed run `PRAGMA wal_checkpoint(TRUNCATE)` in a quiet moment.
- WAL mode cannot be used on read only media without the -shm file; ship read only bundled databases with `journal_mode=DELETE`.
- Upgrade to SQLite 3.51.3+ (or backports 3.44.6, 3.50.7): earlier WAL versions have a rare corruption bug when two connections write or checkpoint at the same instant.
- `PRAGMA integrity_check` (slow, full) or `quick_check` on app start after a crash report, or in a nightly job on servers.

## 6. Schema migrations on devices

- Users skip versions and downgrade by restoring old backups. Store the schema version in `PRAGMA user_version`; on open, run each pending migration in order inside `BEGIN IMMEDIATE ... COMMIT`; refuse to open (with a clear message) a database whose version is newer than the app knows.
- SQLite ALTER TABLE is limited; for anything beyond add/rename/drop column, use the rebuild recipe (`migrations.md` section 8): `PRAGMA foreign_keys=OFF` outside the transaction, create new table, copy, drop, rename, recreate indexes, `PRAGMA foreign_key_check`, commit, `PRAGMA foreign_keys=ON`.
- Test every upgrade path from every shipped schema version with a fixture database file per version committed to the repo.
- Synced apps: the server must accept uploads from clients one or two schema versions behind. Never rename a field in the sync protocol in one release; add the new one, accept both, then remove.

## 7. Local first: what it means in code

Ink and Switch's seven ideals: fast (no spinners), multi device, offline, collaboration, longevity, privacy, user ownership. In code that becomes:

- The UI reads from and writes to the local database only. The network never sits between a tap and the screen update. A spinner on a local write is a bug.
- Ids are minted on the device (UUIDv7, so they sort by time and index well), so a record can be created, referenced and edited offline before the server ever sees it.
- Every local write also appends an operation to an upload queue in the same local transaction. A background sync process drains the queue when online.
- The user can export all their data (JSON or another open format) and the app keeps working if your server disappears (longevity).
- Test offline for real: airplane mode, kill the app mid sync, two devices editing the same record offline, clock skew of hours on one device.

## 8. Sync architectures

Default: server authoritative sync with a local SQLite replica. Pick by need:

| Pattern | How | Pick when |
|---|---|---|
| Online writes, synced reads | writes go through your API; reads come from a synced local copy (ElectricSQL shapes, Supabase realtime into a cache) | writes must be validated live (payments, inventory) |
| Optimistic overlay | local overlay of pending writes on top of synced state; overlay dropped when the server echo arrives; persisted so it survives reload | most SaaS apps with occasional offline |
| Local database plus upload queue (PowerSync model) | client writes to local SQLite; operations go into a FIFO queue; the backend applies each one to Postgres and decides conflicts; the client then adopts the server's checkpoint state | mobile apps, field apps, anything that must work offline for hours |
| CRDT document sync (Automerge, Yjs, Loro) | each replica merges operations; no server authority needed for merges | real time collaborative text, canvases, outlines |

Rules for the upload queue model:

- The queue is FIFO and blocking: if the head operation fails with a temporary error, retry it; do not skip ahead, or later operations apply against state that never existed.
- Permanent errors (validation, permission, row deleted on the server) must not block the queue forever. Decide per error: drop and tell the user, rewrite (re-create a deleted parent), or move to a "needs attention" list the UI shows.
- The server upload handler is idempotent: the same operation (with its client operation id) applied twice has one effect. `INSERT ... ON CONFLICT (id) DO NOTHING` for creates; updates keyed by row id and operation id.
- Authorization happens on the server for every uploaded operation. The client queue is untrusted input.
- After upload, the client replaces its optimistic state with what the server sends back (the server may have rejected or changed the write). Match by row id or a client write id, not by content.
- Ship the minimal subset to each device (per user or per team buckets / shapes). Syncing the whole table to every client leaks data and does not scale.

## 9. Conflict resolution

- **Per row last write wins** (whole row from the latest timestamp) loses data: device A edits the title, device B edits the due date, one edit vanishes. Do not do this.
- **Per field LWW** (each field has its own timestamp or version, the newer value wins per field) is the right default for records like tasks, contacts, settings. Two edits to different fields both survive.
- Timestamps from device clocks are wrong (skew of minutes or years, users changing time zones). Use a hybrid logical clock (physical time plus a counter, never moving backwards and always above any timestamp seen from the server), or let the server order operations as they arrive (server authoritative model, which avoids the problem).
- **Counters** (likes, quantities changed on two devices) are not LWW fields: sync increments (operations like `+1`), or use a CRDT counter.
- **Sets** (tags, members): sync add and remove operations, not the whole array, or two offline adds overwrite each other.
- **Text edited by several people at once**: use a CRDT (Yjs, Automerge, Loro) or OT. Ink and Switch found CRDT merges work well and conflicts are rarer than feared, but history grows without bound (every keystroke) and is hard to truncate because a peer may come back months later. Store CRDT documents as binary blobs in a column, compact them periodically, and keep queryable fields (title, updated_at) as normal columns next to the blob.
- **Deletes vs edits**: decide explicitly. Default: delete wins, and an edit to a deleted record is dropped and reported. For user content, consider "edit resurrects".
- **Invariants that need a single authority** (unique usernames, stock, seat booking, money) cannot be resolved by merge. They go through an online write to the server and the UI says so.

## 10. Delta sync done right

- `WHERE updated_at > :last_sync` misses rows. Transactions commit out of order: transaction A sets `updated_at = 10:00:00.100`, transaction B sets `10:00:00.200` and commits first, a client syncs at that moment and stores cursor `.200`, then A commits and is never sent. Also clock based `updated_at` can go backwards.
- Correct options, in order of preference:
  1. Use a sync engine built on Postgres logical replication (PowerSync, ElectricSQL, Zero) that streams changes in commit order.
  2. Use a monotonic change log: each write inserts into `changes (seq bigint generated always as identity, table_name, row_id, op, at)` and the client pulls `WHERE seq > cursor`. Sequences are assigned at insert, not commit, so only serve changes below the oldest in progress transaction: compare each change's `xid8` (`pg_current_xact_id()` stored on the row) to `pg_snapshot_xmin(pg_current_snapshot())`, or hold back the last few seconds of changes and re-read with overlap. Clients dedupe by `(row_id, seq)`.
- Deletes need tombstones: a deleted row must still be sent as "deleted" so other devices remove it. Keep `deleted_at` on synced tables (or a change log entry), and purge tombstones only after every device has synced past them (or force a full resync for devices older than the purge horizon).
- Give each sync response a cursor and make the client store the cursor in the same local transaction as the applied changes. A crash between "applied" and "cursor saved" must not skip or double apply (applying is idempotent anyway, by row id and version).
- Full resync path: every client must be able to throw away local state (after uploading the queue) and download fresh. You will need it after a bug.

## 11. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| Pragmas set on every connection | WAL, foreign_keys, busy_timeout | `grep -rniE "journal_mode\|foreign_keys\|busy_timeout" src/`; a test asserts `PRAGMA foreign_keys` = 1 |
| Write transactions IMMEDIATE | every write transaction | `grep -rniE "begin(\s+deferred)?\s*;\|\.transaction\(" src/` then check for `immediate` or a single writer |
| STRICT tables | all tables | `sqlite3 app.db "select name from sqlite_schema where type='table' and sql not like '%STRICT%' and name not like 'sqlite_%';"` returns nothing |
| FK columns indexed | none missing | `sqlite3 app.db "select m.name, p.\"from\" from sqlite_schema m join pragma_foreign_key_list(m.name) p where m.type='table';"` compared with `pragma_index_list` |
| FK integrity | no rows | `sqlite3 app.db "PRAGMA foreign_key_check;"` |
| Integrity | `ok` | `sqlite3 app.db "PRAGMA quick_check;"` |
| No raw file copies of a live DB | none | `grep -rniE "copyFile\|fs\.copy\|cp .*\.db\|shutil\.copy" src/ scripts/` near `.db` |
| Ids minted on the client (offline apps) | uuidv7 on create | `grep -rniE "uuidv7\|uuid7" src/` in create paths |
| Upload handler idempotent | applying the same op twice gives the same state | server test that posts one operation twice |
| No `updated_at > cursor` sync | none, or with an overlap and xmin guard | `grep -rniE "updated_at\s*>\s*" src/ server/` |
| Tombstones for deletes | deleted rows reach other devices | test: delete on device A, sync B, record gone on B |
| Multi device conflict test | different fields edited offline on 2 devices both survive | integration test with two local DBs and one server |
