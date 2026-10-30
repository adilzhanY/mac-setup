# Migrations without downtime

How to change a live Postgres schema without blocking traffic, plus SQLite notes. Sources: PostgreSQL docs (ALTER TABLE, explicit locking, CREATE INDEX), the strong_migrations rules (ankane), the Squawk linter rules, GitLab's migration style guide, Stripe's online migrations post, GitHub's gh-ost post.

## Contents

1. Why a "fast" migration takes the site down: the lock queue
2. Lock and rewrite table for every common operation
3. Safe recipes
4. Expand and contract (rename, type change, split, move)
5. Backfills
6. Timeouts and retries
7. Deploy order and rollback
8. Tool notes: Squawk, Supabase, Prisma, Drizzle, sqlx, SQLite
9. Migration checklist
10. Checks

## 1. The lock queue

- Postgres grants locks in queue order. `ALTER TABLE` needs ACCESS EXCLUSIVE, which conflicts with everything, including plain SELECT. If one long query (an analytics report, an idle transaction, a backup) holds even ACCESS SHARE on the table, the ALTER waits, and every new SELECT and write queues behind the waiting ALTER. A metadata only change that would take 5 ms ends up blocking the table for as long as the oldest query runs.
- Fix: always `SET lock_timeout` before DDL so the ALTER gives up after a few seconds instead of stalling traffic, then retry. Also kill or wait out idle in transaction sessions first:

```sql
select pid, state, now() - xact_start as age, query
from pg_stat_activity
where xact_start is not null and now() - xact_start > interval '1 minute'
order by age desc;
```

## 2. Lock and rewrite table

ACCESS EXCLUSIVE blocks reads and writes. SHARE blocks writes. SHARE UPDATE EXCLUSIVE blocks neither reads nor writes (only other DDL and VACUUM). "Rewrite" means the whole table and its indexes are copied, holding the lock the whole time and needing up to double the disk.

| Operation | Lock | Rewrite / scan | Safe on a big live table? |
|---|---|---|---|
| `CREATE TABLE`, `CREATE TABLE ... (LIKE)` | none on others | no | yes |
| `ADD COLUMN` nullable, no default | ACCESS EXCLUSIVE, brief | no | yes, with lock_timeout |
| `ADD COLUMN ... DEFAULT <constant>` (PG 11+) | ACCESS EXCLUSIVE, brief | no (default stored in catalog) | yes |
| `ADD COLUMN ... DEFAULT now()`, `clock_timestamp()`, `gen_random_uuid()` (volatile) | ACCESS EXCLUSIVE | full rewrite | no: add without default, set default, backfill |
| `ADD COLUMN ... GENERATED ... STORED`, identity column | ACCESS EXCLUSIVE | full rewrite | no |
| `ADD COLUMN ... GENERATED ... VIRTUAL` (PG 18) | ACCESS EXCLUSIVE, brief | no | yes |
| `ADD COLUMN ... NOT NULL` without default on a non empty table | fails | | add nullable, backfill, then NOT NULL recipe |
| `DROP COLUMN` | ACCESS EXCLUSIVE, brief | no (space reclaimed later) | yes after code stopped using it |
| `ALTER COLUMN TYPE` | ACCESS EXCLUSIVE | full rewrite plus index rebuild, except binary coercible changes (`varchar(n)` to `text`, larger `varchar(n)`, `numeric` precision increase at same scale, `timestamp` precision increase) | no: expand and contract |
| `ALTER COLUMN SET NOT NULL` | ACCESS EXCLUSIVE | full scan, unless a valid `CHECK (col IS NOT NULL)` exists (PG 12+) | only with the CHECK recipe |
| `ALTER COLUMN DROP NOT NULL` | ACCESS EXCLUSIVE, brief | no | yes (but old code may not expect NULLs) |
| `ALTER COLUMN SET DEFAULT` / `DROP DEFAULT` | ACCESS EXCLUSIVE, brief | no | yes |
| `ADD CONSTRAINT ... CHECK` | ACCESS EXCLUSIVE | full scan | no: `NOT VALID` then `VALIDATE` |
| `ADD CONSTRAINT ... CHECK ... NOT VALID` | ACCESS EXCLUSIVE, brief | no | yes |
| `ADD CONSTRAINT ... FOREIGN KEY` | SHARE ROW EXCLUSIVE on both tables (blocks writes on both) | full scan | no: `NOT VALID` then `VALIDATE` |
| `VALIDATE CONSTRAINT` | SHARE UPDATE EXCLUSIVE (ROW SHARE on referenced table for FKs) | scan, reads and writes continue | yes |
| `ADD CONSTRAINT ... UNIQUE` / `PRIMARY KEY` | ACCESS EXCLUSIVE | builds an index under the lock | no: build `UNIQUE INDEX CONCURRENTLY`, then `ADD CONSTRAINT ... USING INDEX` |
| `ADD CONSTRAINT ... EXCLUDE` | ACCESS EXCLUSIVE | builds index | no safe online form; do it on a small table or in a window |
| `CREATE INDEX` | SHARE (blocks writes) | builds index | no |
| `CREATE INDEX CONCURRENTLY` | SHARE UPDATE EXCLUSIVE | two scans, waits for old transactions | yes, outside a transaction block |
| `DROP INDEX` | ACCESS EXCLUSIVE | no | use `DROP INDEX CONCURRENTLY` |
| `REINDEX` | ACCESS EXCLUSIVE on the index, SHARE on table | rebuild | use `REINDEX INDEX CONCURRENTLY` (PG 12+) |
| `RENAME COLUMN` / `RENAME TABLE` | ACCESS EXCLUSIVE, brief | no | the lock is fine; running code breaks. Expand and contract |
| `CREATE TRIGGER`, `ENABLE/DISABLE TRIGGER` | SHARE ROW EXCLUSIVE | no | brief, with lock_timeout |
| `ALTER TYPE enum ADD VALUE` | brief | no | yes; new value unusable inside the same transaction until commit |
| `ATTACH PARTITION` | SHARE UPDATE EXCLUSIVE on parent, ACCESS EXCLUSIVE on the attached table | scans the new partition unless a matching CHECK exists | add the CHECK NOT VALID and validate first |
| `DETACH PARTITION CONCURRENTLY` | SHARE UPDATE EXCLUSIVE | no | yes, outside a transaction |
| `VACUUM FULL`, `CLUSTER` | ACCESS EXCLUSIVE | full rewrite | no: use `pg_repack` or `pg_squeeze` |
| `TRUNCATE`, `DROP TABLE` | ACCESS EXCLUSIVE | no | only when nothing uses it; `TRUNCATE ... CASCADE` is banned |
| `REFRESH MATERIALIZED VIEW` | ACCESS EXCLUSIVE | rebuild | use `CONCURRENTLY` (needs a unique index on the view) |

Multiple subcommands in one `ALTER TABLE` take the strongest lock any of them needs. Locks are held until the transaction ends: if a migration framework wraps the whole file in one transaction, a brief ALTER followed by a slow UPDATE keeps ACCESS EXCLUSIVE for the whole UPDATE. Put one risky statement per migration.

## 3. Safe recipes

### Add an index

```sql
-- migration must not run in a transaction (Rails: disable_ddl_transaction!, Prisma/Drizzle: separate raw SQL file, see section 8)
set lock_timeout = '5s';
create index concurrently if not exists orders_user_id_idx on orders (user_id);
-- if it failed, it left an INVALID index: drop it and retry
-- select indexrelid::regclass from pg_index where not indisvalid;
-- drop index concurrently orders_user_id_idx;
```

### Add a foreign key

```sql
-- migration 1
set lock_timeout = '5s';
alter table orders add constraint orders_user_id_fkey
  foreign key (user_id) references users (id) not valid;
-- migration 2 (separate transaction)
alter table orders validate constraint orders_user_id_fkey;
```

Create the index on `orders.user_id` before or with this, or deletes on `users` will scan `orders`. GitLab rule: one foreign key per transaction.

### Set NOT NULL on an existing column

```sql
-- 1: enforce for new rows, no scan
alter table users add constraint users_email_not_null check (email is not null) not valid;
-- 2: scan without blocking writes
alter table users validate constraint users_email_not_null;
-- 3: PG 12+ uses the valid CHECK as proof, no scan
alter table users alter column email set not null;
-- 4
alter table users drop constraint users_email_not_null;
```

(PG 18 also accepts `ADD CONSTRAINT ... NOT NULL ... NOT VALID` directly.)

### Add a unique constraint or primary key

```sql
create unique index concurrently users_email_key on users (lower(email));
-- a constraint needs a plain column index; expression indexes stay as unique indexes
create unique index concurrently accounts_slug_key on accounts (slug);
alter table accounts add constraint accounts_slug_key unique using index accounts_slug_key;
```

### Add a column with a volatile default

```sql
alter table events add column public_id uuid;                    -- no rewrite
alter table events alter column public_id set default uuidv7();  -- new rows only
-- backfill old rows in batches (section 5), then NOT NULL recipe
```

### Change a CHECK or an enum like set

Add the new CHECK `NOT VALID`, validate it, drop the old one. Never edit a CHECK in place.

## 4. Expand and contract

Use for rename, type change, splitting a column, moving data to another table. Each step is its own deploy; never two steps in one release.

1. **Expand:** add the new column or table (nullable, no constraint yet).
2. **Dual write:** code writes both old and new. Reads still use old.
3. **Backfill:** copy old to new for existing rows, in batches.
4. **Verify:** compare old and new (a count of mismatches must be 0; Stripe ran GitHub Scientist style comparisons in production and alerted on any mismatch).
5. **Switch reads** to new. Add constraints on new (NOT VALID, validate).
6. **Stop writing old.** For ORMs that cache columns (Rails, some others), tell the ORM to ignore the old column first (`ignored_columns`) and deploy.
7. **Contract:** drop the old column in a later migration.

A rename that skips this breaks every running instance for the length of the deploy: old code still selects `name` after the migration renamed it to `full_name`. A view or a generated column under the old name can bridge a short window, but the full recipe is the default.

## 5. Backfills

- Never `UPDATE big_table SET new = old` in one statement: it locks every row it touches until commit, bloats the table, floods WAL and replicas, and cannot resume.
- Batch by primary key range, each batch its own transaction, sleep between batches, record progress:

```sql
-- repeat with the last id returned until no rows
with batch as (
  select id from users
  where id > $1 and full_name is null
  order by id limit 5000
)
update users u set full_name = u.first_name || ' ' || u.last_name
from batch where u.id = batch.id
returning u.id;
```

- Size: 1k to 10k rows, each batch well under 1 second (GitLab: every query under 1 s with cold cache; regular migrations under 3 minutes, post deploy migrations under 10 minutes, longer work becomes a background job).
- Run backfills from a job or script, not inside the schema migration transaction. Make them idempotent (`WHERE new IS NULL`), so a crash resumes.
- Watch replica lag and pause if it grows (gh-ost throttles on lag; do the same with a sleep that grows when `pg_stat_replication.replay_lag` is high).

## 6. Timeouts and retries

- Every migration file starts with:

```sql
set lock_timeout = '5s';        -- give up instead of queueing traffic behind us
set statement_timeout = '15min'; -- no runaway statement (raise per file for CONCURRENTLY builds)
```

- strong_migrations defaults: `lock_timeout` 10 s, `statement_timeout` 1 hour for migrations, with up to 3 retries 10 s apart on lock timeout. Squawk's example uses `1s` and `5s`. Pick 2 to 10 s for lock_timeout on busy tables.
- App connections: `statement_timeout` around 15 to 30 s and `idle_in_transaction_session_timeout` around 60 s, so an abandoned transaction cannot block a migration forever. Behind PgBouncer in transaction mode, set these on the role: `ALTER ROLE app SET statement_timeout = '15s';`
- Retry a migration that hit `lock_timeout` (SQLSTATE 55P03) a few times with a delay. Do not raise the timeout instead.

## 7. Deploy order and rollback

- Order: migration that adds things runs before the code that uses them; code that stops using something deploys before the migration that drops it. With rolling deploys, old and new code run at the same time, so each migration must work with both the previous and the next code version.
- Post deploy migrations (GitLab term): drops, cleanup and non critical indexes run after the new code is live.
- Roll forward, not back. Write a `down` for local development, but in production fix with a new migration. A `down` that drops a column with new data in it destroys that data.
- Before any migration that drops or rewrites data: take a backup or snapshot, write the restore command in the PR, and know its age (see `backups-and-recovery.md`).
- Never edit a migration that has run anywhere shared. Add a new one. CI should fail if an applied migration's checksum changes.
- Test on production sized data: restore last night's backup to a scratch database and time the migration there. A migration that takes 2 s on dev data can take an hour on 50M rows.

## 8. Tool notes

### Squawk (Postgres migration linter)

```bash
npx squawk-cli 'migrations/**/*.sql'      # or: pip install squawk-cli / cargo binstall squawk
```

`.squawk.toml` at the repo root:

```toml
pg_version = "17.0"
assume_in_transaction = true      # most frameworks wrap each file in a transaction
excluded_rules = []
```

Rules that catch the outages above: `require-concurrent-index-creation`, `require-concurrent-index-deletion`, `constraint-missing-not-valid`, `adding-foreign-key-constraint`, `adding-not-nullable-field`, `adding-field-with-default` (volatile defaults), `changing-column-type`, `renaming-column`, `renaming-table`, `ban-drop-column`, `disallowed-unique-constraint`, `adding-serial-primary-key-field`, `ban-concurrent-index-creation-in-transaction`, `require-timeout-settings` (now `require-lock-timeout` plus `require-statement-timeout`), `prefer-bigint-over-int`, `prefer-identity`, `prefer-timestamptz`, `prefer-text-field`, `prefer-robust-stmts` (`IF NOT EXISTS` so a retried migration does not fail), `ban-truncate-cascade`. Ignore one statement with `-- squawk-ignore rule-name` and a reason comment.

Run it in CI on changed migration files only (generated ORM migrations included).

### Supabase

- `supabase migration new <name>` writes `supabase/migrations/<timestamp>_<name>.sql`; `supabase db diff -f <name>` generates one from local changes; `supabase db reset` replays all migrations plus `seed.sql` locally; `supabase db push` applies to the linked project. Never change the remote schema in the dashboard without pulling it back into a migration (`supabase db pull`), or environments drift.
- RLS policies, grants and functions are schema: they live in migrations, and pgTAP tests (`supabase test db`) cover allow and deny per role.

### Prisma, Drizzle

- Prisma Migrate and drizzle-kit generate SQL; read every generated file. They will happily emit a column rename as drop plus add (data loss), a plain `CREATE INDEX`, or a FK without NOT VALID.
- For CONCURRENTLY, the statement must not run inside a transaction block. Prisma sends a migration file as one multi statement query, which Postgres runs as one implicit transaction, so a `CREATE INDEX CONCURRENTLY` must sit alone in its own migration file. Drizzle's migrator applies pending files inside a transaction; apply concurrent index builds with a separate script step. Verify against the tool version in the repo: run the migration on a scratch database and confirm it does not fail with "cannot run inside a transaction block".
- `prisma db push` and `drizzle-kit push` are for prototypes only. Production uses versioned migration files.

### sqlx (Rust)

- `sqlx migrate add -r <name>` creates up and down files; `sqlx migrate run`. sqlx runs each migration in a transaction unless the file starts with `-- no-transaction`; use that for CONCURRENTLY.
- `sqlx::migrate!()` embeds migrations; checksums of applied files are verified, so never edit an applied file.

### SQLite

- SQLite `ALTER TABLE` supports only rename table, rename column (3.25+), add column (no PRIMARY KEY, no UNIQUE, no non constant default, no NOT NULL without default) and drop column (3.35+, with limits). Anything else uses the 12 step rebuild: inside a transaction with `PRAGMA foreign_keys=OFF` set before it, create `new_t`, copy, drop `t`, rename `new_t` to `t`, recreate indexes and triggers, run `PRAGMA foreign_key_check`, commit, turn foreign keys back on.
- Track the version with `PRAGMA user_version` and run migrations in order on app start, each inside `BEGIN IMMEDIATE ... COMMIT`.
- On mobile and desktop, users skip versions: migration 3 must work on a database that went straight from 1. Test upgrading from every shipped version's schema, with real looking data.

## 9. Migration checklist

Copy into the PR:

```
- [ ] Rows in the table in production: ____ ; writes/s: ____
- [ ] lock_timeout and statement_timeout set at the top
- [ ] Each statement's lock checked against migrations.md section 2
- [ ] No table rewrite (no volatile default, no type change, no stored generated column) on a big table
- [ ] Indexes CONCURRENTLY, in a migration that does not run in a transaction
- [ ] FK and CHECK added NOT VALID, validated in a separate migration
- [ ] NOT NULL via CHECK NOT VALID, VALIDATE, SET NOT NULL
- [ ] Rename / type change done as expand and contract over several deploys
- [ ] Backfill batched, idempotent, outside the DDL transaction
- [ ] Old code works with the new schema; new code works with the old schema
- [ ] Squawk passes (or each ignore has a reason)
- [ ] Generated ORM SQL read line by line
- [ ] Ran on a production sized copy; duration: ____
- [ ] Destructive? Backup taken, restore command written here: ____
```

## 10. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| Lint | zero errors | `npx squawk-cli 'migrations/**/*.sql'` |
| Timeouts set | every migration file sets lock_timeout | `grep -L "lock_timeout" migrations/*.sql` prints nothing (or the framework sets it globally) |
| Concurrent index builds | all `CREATE INDEX` on existing tables are CONCURRENTLY | `grep -rniE "create (unique )?index" migrations/ \| grep -vi concurrently` and check each targets a new table |
| Constraints NOT VALID | every FK/CHECK on an existing table | `grep -rniE "add constraint" migrations/ \| grep -viE "not valid\|using index"` |
| No rename in one step | no `rename column` without a prior dual write release | `grep -rniE "rename (column\|to)" migrations/` and check history |
| Applied migrations unchanged | no edits to old files | `git diff --name-status origin/main -- migrations/ \| grep -v '^A'` prints nothing |
| No invalid indexes after deploy | none | `select indexrelid::regclass from pg_index where not indisvalid;` |
| Schema in repo matches prod | no diff | `supabase db diff --linked`, `prisma migrate diff`, or `pg_dump --schema-only` compared to a fresh replay |
