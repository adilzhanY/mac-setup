# Data: the 20 rules

Master file for anything that stores data: schema, queries, migrations, transactions, sync, backups. Read this first, then the topic file the task needs.

## Contents

1. Files in this folder and when to read them
2. The 20 rules
3. Defaults table (when nothing else is said)
4. Before you touch data: 8 questions
5. Checks

## 1. Files in this folder

| File | What is in it | Read when |
|---|---|---|
| `schema-design.md` | keys, types, time, money, enums, JSONB vs columns, soft delete, naming | creating or changing tables |
| `indexes-and-queries.md` | index design, EXPLAIN, pagination, N+1, query anti-patterns | a query is slow, or you add a query on a big table |
| `migrations.md` | lock taken by every DDL, expand and contract, timeouts, Squawk, checklist | writing any migration against a live database |
| `transactions-and-integrity.md` | isolation, lost updates, retries, idempotency keys, outbox, constraints in the DB | writing code that changes more than one row, or calls an outside service |
| `sqlite-and-local-first.md` | SQLite pragmas, WAL, STRICT, busy errors, offline first, sync, CRDT vs LWW | SQLite, mobile, desktop, or any app that must work offline |
| `backups-and-recovery.md` | 3 2 1, pg_dump vs PITR, SQLite backup, Litestream, restore test script, encryption, retention, user data export | setting up or auditing backups, or any destructive operation |
| `orm-and-query-layers.md` | Prisma, Drizzle, Kysely, sqlx, raw SQL: which and how, N+1 detection | choosing or reviewing a data access layer |

## 2. The 20 rules

Each rule names the check that proves it. The detail lives in the topic file.

1. **The database enforces every invariant it can.** NOT NULL, CHECK, UNIQUE, FOREIGN KEY and EXCLUDE go in the schema, not only in app code. App validation is for nice error messages; the constraint is for truth. Two app servers racing past an `if (exists)` check is the normal case, not an edge case. Check: for each "must be unique / must exist / must be positive" rule in code, grep the migrations for the matching constraint.
2. **Every column is NOT NULL unless "unknown" is a real, distinct state.** Nullable by default makes three-valued logic leak into every query (`NOT IN` with a NULL returns nothing). Check: list nullable columns and justify each.
3. **Time is `timestamptz`, stored in UTC, converted at the edge.** Never `timestamp` without zone for an instant. Store a future local event (a 9:00 meeting in Berlin) as local date-time plus IANA zone name, because zone rules change. Check: `grep -rniE "\btimestamp\b" migrations/ | grep -viE "timestamptz|with time zone"` finds no plain timestamps for instants.
4. **Money is an integer of minor units or `numeric`, plus a currency column.** Never float, never Postgres `money`. Check: `grep -rniE "(price|amount|balance|total|cost)\w*\s+(real|float|double|money)" migrations/` returns nothing.
5. **Primary keys: `bigint generated always as identity` by default; UUIDv7 when the client or several systems mint ids.** Never random UUIDv4 as a clustered or B-tree primary key on a hot table. Never expose sequential ids where enumeration leaks business data; add a separate public id. Check: `grep -rniE "serial|uuid_generate_v4|gen_random_uuid" migrations/` and review each hit.
6. **Index every foreign key column you join or cascade on.** Postgres and SQLite do not create them. Check: the query in `indexes-and-queries.md` section 3 lists unindexed foreign keys.
7. **Design indexes from queries, equality columns first, range column last, at most about 3 columns for non-unique indexes.** Check: every new query on a table over 10k rows has an EXPLAIN that shows an index access predicate, not a filter.
8. **Paginate with a keyset (`WHERE (created_at, id) < ($1, $2) ORDER BY created_at DESC, id DESC LIMIT n`), not OFFSET**, on anything a user can scroll. Check: `grep -rniE "offset\s*\(|OFFSET \$|\.offset\(|skip:" src/` and justify each.
9. **No query inside a loop.** Load related rows with a join, `IN (...)`, or the ORM's batch include. Check: enable query logging in a test and assert the query count for a list endpoint does not grow with the row count.
10. **Read-modify-write is done in one statement or under a lock.** `UPDATE ... SET n = n + 1`, `SELECT ... FOR UPDATE`, a version column, or SERIALIZABLE with retry. Never read in app code, compute, then write the stale result. Check: grep for a SELECT followed by an UPDATE of the same row in one function without `FOR UPDATE` or a version check.
11. **Code that runs at REPEATABLE READ or SERIALIZABLE retries the whole transaction on SQLSTATE 40001 (and 40P01 deadlock).** Check: grep for the isolation level and find the retry loop next to it.
12. **Never hold a transaction open across a network call** (HTTP, payment provider, email, LLM). Commit, call out, then record the result in a new transaction, keyed by an idempotency key. Check: read every transaction block; no `fetch`, `axios`, `reqwest`, SDK client or `await` on an outside service inside it.
13. **Every mutating endpoint that a client may retry accepts an idempotency key**, stored with a unique constraint `(user_id, key)` and the stored response. Check: POST handlers for payments, orders, sends, imports read an `Idempotency-Key` header or equivalent.
14. **Migrations against a live database never take a long ACCESS EXCLUSIVE lock.** Set `lock_timeout` (about 2 to 10 s) and `statement_timeout` at the top, create indexes CONCURRENTLY, add constraints NOT VALID then VALIDATE, change types and names by expand and contract. Check: `squawk migrations/*.sql` passes.
15. **Schema changes and code changes ship in an order where every deployed code version works with every schema version that can coexist with it.** Add before use, stop using before drop. Check: a drop or rename in migration N has a code change in an earlier, already deployed release that stopped reading the column.
16. **Backfills run in batches outside the DDL transaction**, 1k to 10k rows per batch, each its own short transaction, with a pause, resumable from the last key. Check: no `UPDATE big_table SET ...` without a `WHERE id BETWEEN` or keyset batch.
17. **A backup that has not been restored is not a backup.** Automate a restore of the latest backup into a scratch database on a schedule, run a sanity query, and alert on failure or on age. Check: a scheduled job exists, and its last success is younger than the backup interval.
18. **Keep 3 copies, on 2 kinds of storage, 1 off site, and at least 1 that the production credentials cannot delete** (object lock, append-only, separate account). Encrypt backups before they leave the host. Check: the backup target and its credentials are listed in the repo docs; production keys cannot `DeleteObject` there.
19. **SQLite: `journal_mode=WAL`, `foreign_keys=ON` on every connection, `busy_timeout`, `BEGIN IMMEDIATE` for writes, STRICT tables.** Check: the connection setup code sets each pragma; `grep -rn "foreign_keys" src/` finds it.
20. **Offline first apps: client generated UUIDv7 ids, an upload queue of operations, a server that is the authority and applies each operation idempotently.** Last write wins only per field, never per row. Use a CRDT only for text or other data that people edit at the same moment. Check: ids are minted on the client, and the server upload handler is safe to call twice with the same operation.

## 3. Defaults table

| Decision | Default | Switch when |
|---|---|---|
| Database for a server app | PostgreSQL | single process, one machine, low write concurrency: SQLite |
| Database on a device | SQLite (WAL, STRICT) | never IndexedDB as the source of truth when SQLite (wasm or native) is available |
| Primary key | `bigint generated always as identity` | ids minted on clients or merged across databases: UUIDv7 (`uuidv7()` in PG 18) |
| Time | `timestamptz`, UTC | a calendar date: `date`; a future local event: local timestamp plus zone name |
| Money | `bigint` minor units plus `currency text` (ISO 4217, CHECK on length 3) | fractional cents or rates: `numeric(20, 6)` |
| String | `text` plus CHECK on length if a real limit exists | never `varchar(n)` as a habit, never `char(n)` |
| Small fixed set of states | `text` with CHECK (`status in ('a','b')`) or a lookup table | the set never shrinks and never gets renamed: Postgres enum |
| Semi structured payload | `jsonb` for data you store and return whole | you filter, join, sort or constrain on a key: make it a column |
| Delete | hard delete plus an archive table (`deleted_record`) | legal hold or user facing "trash" with restore: `deleted_at` plus partial unique indexes and a view |
| Isolation | READ COMMITTED with atomic updates or `FOR UPDATE` | an invariant spans several rows: SERIALIZABLE plus retry |
| Data access in TypeScript | Drizzle or Kysely | team already on Prisma: keep Prisma, watch N+1 and raw SQL holes |
| Data access in Rust | sqlx with `query!` macros and offline mode | heavy dynamic query building: sea-query or a small builder |
| Backup, Postgres server | managed PITR plus a nightly `pg_dump -Fc` to separate storage | self hosted: pgBackRest or WAL-G for PITR |
| Backup, SQLite | Litestream to object storage plus nightly `VACUUM INTO` copy | single user desktop app: `VACUUM INTO` on a timer plus export |

## 4. Before you touch data: 8 questions

Answer these in the plan before writing a migration or data code.

1. How many rows does the table have in production, and how many writes per second? (A migration that is fine at 10k rows takes the site down at 100M.)
2. Which lock does each statement take, and for how long? (See `migrations.md` section 2.)
3. Which code versions will run against the new schema, and does the old code still work after the migration?
4. What invariant must hold, and which constraint enforces it in the database?
5. What happens if this code runs twice? If it crashes halfway?
6. Does a transaction here wait on anything outside the database?
7. If this goes wrong, which backup restores it, how old is that backup, and when was it last restored?
8. Does this delete or overwrite data? Then take a backup or snapshot first and write the exact rollback command down before running it.

## 5. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| Migration lint | zero Squawk errors | `npx squawk-cli migrations/*.sql` (or `squawk` binary); see `migrations.md` |
| No float money | no hits | `grep -rniE "(price\|amount\|balance\|total\|cost)\w*\s+(real\|float\|double\|money)" migrations/ schema*` |
| No naive timestamps for instants | every hit justified | `grep -rniE "\btimestamp\b" migrations/ \| grep -viE "timestamptz\|with time zone"` |
| FK columns indexed | query returns no rows | SQL in `indexes-and-queries.md` section 3 |
| No OFFSET pagination on user lists | every hit justified | `grep -rniE "\boffset\b\|\.skip\(\|skip:" src/` |
| No query in loop | query count constant | test with query logging, see `orm-and-query-layers.md` |
| Retry on 40001 | retry next to every SERIALIZABLE or REPEATABLE READ | `grep -rniE "serializable\|repeatable read" src/` then read each |
| No network call in a transaction | none | read every `transaction(` / `BEGIN` block |
| Restore test | last success younger than backup interval | the restore job log or its healthcheck ping, see `backups-and-recovery.md` |
| SQLite pragmas | WAL, foreign_keys, busy_timeout set on open | `grep -rniE "journal_mode\|foreign_keys\|busy_timeout" src/` |
| RLS on exposed tables (Supabase) | every table in `public` has RLS on | `select relname from pg_class c join pg_namespace n on n.oid=c.relnamespace where nspname='public' and relkind='r' and not relrowsecurity;` returns no rows |
