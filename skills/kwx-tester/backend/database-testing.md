# Database testing

How to test code and rules that live in the database: queries, constraints, transactions, migrations, and Supabase Row Level Security. The rule is a real Postgres, never a mock and never SQLite standing in for Postgres. kwx-developer `reliability/testing-strategy.md` section 7 gives the container setup and the three isolation options; `data/migrations.md` covers writing safe migrations. This file is the tester's part: how to pick an isolation strategy, what to assert for constraints, how to test a migration on real data, and how to test RLS as each role.

## Contents

1. Choosing where Postgres runs
2. Isolation per test
3. Seed data and fixtures
4. Constraint tests
5. Concurrency and transaction tests
6. Migration tests
7. Row Level Security tests (Supabase and plain Postgres)
8. Time inside the database
9. Checks

## 1. Choosing where Postgres runs

| Option | Use when | Notes |
|---|---|---|
| Docker Compose or CI service container (`postgres:17`/`postgres:18`) | default for most projects | same major version and extensions as production |
| Testcontainers (`@testcontainers/postgresql` 12, Rust `testcontainers-modules`) | tests should start and stop their own database | Node module has `snapshot()` and `restoreSnapshot()`; close connections first, and do not name the database `postgres` when using snapshots (Testcontainers docs) |
| Local cluster with `initdb` + `pg_ctl` on a spare port | no Docker, or fastest local loop | verified below |
| Supabase CLI local stack (`supabase start`) | Supabase projects: you need `auth`, roles, RLS helpers, PostgREST | heavy (many containers); exclude services you do not need with `-x` |
| PGlite (`@electric-sql/pglite` 0.5) | pure SQL logic tests in Node with no Docker | Postgres compiled to WASM with one exclusive connection; no concurrency tests, check extension support first. Not a stand in for Supabase roles |

Test only settings make Postgres much faster: `fsync=off`, `synchronous_commit=off`, `full_page_writes=off`, data directory on tmpfs. Never in production.

Local cluster, verified 2026-10-31 with PostgreSQL 18.6:

```bash
initdb -D ./pgdata -U postgres -A trust
pg_ctl -D ./pgdata -l pg.log start \
  -o "-p 55432 -k $PWD -c fsync=off -c synchronous_commit=off -c full_page_writes=off"
export PGHOST=$PWD PGPORT=55432 PGUSER=postgres
# ... run tests ...
pg_ctl -D ./pgdata stop
```

## 2. Isolation per test

| Strategy | Speed | Isolation | Breaks when |
|---|---|---|---|
| Transaction per test, rolled back | fastest | good | code under test opens its own connections or transactions; you need to test commit behaviour, `now()` (section 8), or concurrency |
| Database per test from a template | fast (cloning took 16 ms locally) | full, parallel safe | many hundreds of tests share one small CI database server (raise `max_connections`) |
| Schema per test | fast | good | code hard codes `public.` |
| Truncate between tests | slow | serial only | anything in parallel |

Template recipe (verified locally): migrate once into `app_template`, then per test:

```sql
CREATE DATABASE test_7f3a TEMPLATE app_template;
-- run the test against test_7f3a
DROP DATABASE test_7f3a;
```

The template must have no open connections while it is cloned. Rust's `#[sqlx::test]` does this for you: a new database per test, migrations from `./migrations` applied, databases of passing tests dropped, failed ones kept for debugging (sqlx docs).

Rules:

1. **Tests must pass in random order and in parallel.** Run the suite with shuffling on (`vitest --sequence.shuffle`, `cargo nextest run` is per process already) before you trust it. Evidence: strong.
2. **App level tests cannot always roll back.** When tests go through an HTTP API or `supabase-js`, data is committed. Use unique ids per test (`crypto.randomUUID()`), filter every read by the ids you created, and never assert on whole table counts (Supabase RLS testing docs). Evidence: moderate.

## 3. Seed data and fixtures

- **Two layers:** a small committed seed with reference data every test needs (plans, countries, roles), and per test factories that create exactly the rows that test needs. Evidence: moderate.
- **Factories, not shared fixtures.** `createUser({ plan: 'pro' })` returns a fresh row with unique values. Shared "user 1 is Alice" fixtures couple tests together.
- **Realistic shapes.** Unicode names, long strings, nulls in optional columns, timestamps across time zones and DST. Bugs hide in data that `'test'` and `'foo'` never exercise.
- **Volume for some tests.** Pagination, performance and migration tests need thousands of rows: `INSERT ... SELECT FROM generate_series(1, 100000)` is fast.
- **Supabase:** `supabase/seed.sql` runs on `supabase db reset`. Keep it deterministic; it is also the base for local manual testing.
- **Never copy production data into tests** unless it is anonymised and the user has agreed. Evidence: strong (privacy law, leaked fixtures).

## 4. Constraint tests

The database is the last line of defence; test that it holds even when the app code is bypassed.

For every table, from the schema:

| Constraint | Test |
|---|---|
| `NOT NULL` | insert null, expect SQLSTATE `23502` |
| `UNIQUE` (including partial and case insensitive ones) | insert a duplicate, expect `23505`; for `lower(email)` uniqueness try `A@x.com` vs `a@x.com` |
| `CHECK` | insert at the boundary and one past it, expect `23514` |
| Foreign key | insert an orphan, expect `23503`; delete a parent, check `ON DELETE` behaviour (cascade, restrict, set null) |
| Exclusion constraint (bookings, ranges) | overlapping range, expect `23P01` |
| Generated columns, defaults, triggers | insert minimal row, assert computed values |

Assert the SQLSTATE code, not the message text; messages change with versions and locales. In pgTAP: `select throws_ok($$ insert ... $$, '23505');`. In node-postgres: `await expect(q).rejects.toMatchObject({ code: '23505' })`.

Verified example: a `check (length(title) between 1 and 200)` rejected an empty title with `new row for relation "todos" violates check constraint "todos_title_check"`.

## 5. Concurrency and transaction tests

Single threaded tests never find race conditions. For anything with "check then write" logic (balances, stock, seat booking, unique usernames, idempotency keys):

```ts
// two connections, real concurrency
const [a, b] = await Promise.allSettled([
  withConn((c) => reserveSeat(c, seatId, alice)),
  withConn((c) => reserveSeat(c, seatId, bob)),
]);
expect([a, b].filter((r) => r.status === 'fulfilled')).toHaveLength(1);
expect(await countReservations(seatId)).toBe(1);
```

- Use separate connections (a pool with size at least 2), not one connection, or the calls serialize.
- To force the bad interleaving deterministically, open transaction A, do its read, then run B fully, then finish A. Use `SELECT pg_sleep()` only as a last resort.
- Under `SERIALIZABLE`, assert that the code retries on SQLSTATE `40001`.
- Loop the test (for example 50 times) in a nightly job; a race that fails 1 in 30 runs is still a bug.

## 6. Migration tests

A migration that runs on an empty database can still destroy production data. Test it the way it will run: on a database that holds the previous version's data.

Recipe:

1. Create a database and migrate it to the version before the new migration (`sqlx migrate run --target-version`, Prisma `migrate deploy` on a checkout of the previous commit, or apply files up to N-1).
2. Insert realistic rows that touch every table and column the migration changes, including edge values: nulls, duplicates that a new unique constraint would reject, very long text, rows that a new `CHECK` would reject.
3. Apply the new migration.
4. Assert: the migration succeeded (or failed with a clear message if bad data exists and the plan says it should); row counts unchanged; values transformed as specified; new constraints and indexes exist (`\d table` or pgTAP `has_index`, `col_not_null`); the old app version's queries still work if the deploy is expand and contract.
5. If the project keeps down migrations: apply down, assert the schema equals the N-1 snapshot and the data is still there. If it uses forward fixes only, write the forward fix test instead: apply a corrective migration and assert the state.
6. Apply all migrations from zero on an empty database and compare `pg_dump --schema-only` with the committed schema snapshot. Drift means someone changed the database by hand.

Rules:

1. **Every migration that changes or deletes data has a data test.** Renames, type changes, splits, backfills, drops. Evidence: moderate (GitLab 2017 and many smaller postmortems).
2. **Run on a production sized copy before deploy when the table is large,** and record the duration and the locks taken. kwx-developer `data/migrations.md` has the lock table. Evidence: strong.
3. **Mobile and desktop apps with local SQLite: test upgrading from every shipped schema version,** because users skip versions. Evidence: strong (kwx-developer `data/migrations.md`).

## 7. Row Level Security tests (Supabase and plain Postgres)

RLS is the authorization layer of a Supabase app. Test it per table, per operation, per role.

What to know before writing tests:

- Superusers and the table owner bypass RLS (unless `FORCE ROW LEVEL SECURITY`). Connect as, or `SET ROLE` to, `authenticated` and `anon`.
- In Supabase, `auth.uid()` reads the JWT claims from the `request.jwt.claims` setting. Set it per transaction with `set local`.
- A `SELECT` blocked by RLS returns zero rows, not an error. An `UPDATE` or `DELETE` of someone else's row returns `UPDATE 0` / `DELETE 0`, not an error. An `INSERT` that fails `WITH CHECK` raises SQLSTATE `42501`. A role with no table grant gets `permission denied`, also `42501`.
- A check of `pg_policies` alone is not a test; the policy can exist and still be wrong. Test through the rows returned (Supabase docs).
- Do not drop a policy to test denial: with no policy every read is denied anyway, so deny tests pass. Instead add a temporary `using (true)` policy, see a deny test fail, then remove it (Supabase docs). This is mutation testing by hand.

Verified on plain PostgreSQL 18.6 with a Supabase style `auth.uid()` (2026-10-31):

```sql
begin;
set local role authenticated;
set local request.jwt.claims = '{"sub":"11111111-1111-1111-1111-111111111111","role":"authenticated"}';
select count(*) from todos;            -- 1: only alice's row
update todos set title = 'hacked'
  where user_id = '22222222-2222-2222-2222-222222222222';   -- UPDATE 0, no error
insert into todos (user_id, title)
  values ('22222222-2222-2222-2222-222222222222', 'forged'); -- ERROR: new row violates row-level security policy
rollback;

begin;
set local role anon;
select count(*) from todos;            -- ERROR: permission denied for table todos (no grant to anon)
rollback;
```

The same as a pgTAP file for `supabase test db` (`supabase/tests/database/todos_rls.test.sql`), using the pattern from the Supabase docs (not run here: it needs the Supabase local stack with pgTAP):

```sql
begin;
select plan(5);

-- arrange as superuser
insert into auth.users (id, email) values
  ('11111111-1111-1111-1111-111111111111', 'alice@test.local'),
  ('22222222-2222-2222-2222-222222222222', 'bob@test.local');
insert into public.todos (user_id, title) values
  ('11111111-1111-1111-1111-111111111111', 'alice todo'),
  ('22222222-2222-2222-2222-222222222222', 'bob todo');

-- act as alice
set local role authenticated;
set local request.jwt.claims = '{"sub":"11111111-1111-1111-1111-111111111111","role":"authenticated"}';

select results_eq('select title from todos', $$values ('alice todo')$$, 'alice sees only her todo');
select is_empty($$update todos set title = 'x' where user_id = '22222222-2222-2222-2222-222222222222' returning id$$,
  'alice cannot update bob''s todo');
select throws_ok($$insert into todos (user_id, title) values ('22222222-2222-2222-2222-222222222222', 'forged')$$,
  '42501', null, 'alice cannot insert as bob');

-- act as anonymous
set local role anon;
set local request.jwt.claims = '{"role":"anon"}';
select is_empty('select * from todos', 'anon sees nothing');

-- verify state as superuser
reset role;
select results_eq($$select title from todos where user_id = '22222222-2222-2222-2222-222222222222'$$,
  $$values ('bob todo')$$, 'bob''s todo is unchanged');

select * from finish();
rollback;
```

Notes:

- If anon has no grant at all, `is_empty('select * from todos')` errors instead of passing. Decide which behaviour the spec wants (no grant, or grant plus a policy that returns nothing) and assert that one, for example with `throws_ok(..., '42501')`.
- The `basejump-supabase_test_helpers` package (installed through `dbdev`) adds `tests.create_supabase_user()`, `tests.authenticate_as()` and `tests.rls_enabled('public')`. The last one is a cheap guard that no table in a schema was left without RLS. Evidence: moderate (Supabase advanced pgTAP guide).
- pgTAP runs files in alphabetical order; put shared setup in `000-setup.sql` (Supabase docs).

Coverage target per table: for each of `select`, `insert`, `update`, `delete`, test allow for the owner and deny for another user and for `anon`; for `update`, also test that the owner cannot move a row to another owner (`with check`). Plus storage buckets (`storage.objects` policies) and any `security definer` function, which bypasses RLS and needs its own checks.

App level, through `supabase-js` (pattern from the Supabase RLS testing docs): create two users with the admin client in `beforeAll`, sign each in with `signInWithPassword` on its own client, and run the authorization matrix from `api-testing.md`. A cross user update returns no error and changes nothing; assert the other user's rows are unchanged.

## 8. Time inside the database

- `now()` and `current_timestamp` return the start time of the current transaction. Inside a test wrapped in one transaction, `now()` never moves, and two inserts get the same timestamp. Use `clock_timestamp()` when you need wall time, or pass the time in as a parameter. Evidence: strong (Postgres docs).
- Logic like "expires after 7 days" is easiest to test when the query takes `$now` as a parameter from the app's injected clock. Then the test passes any instant it wants.
- `pg_cron` jobs: test the function the job calls, with a time parameter; do not wait for the scheduler.

## 9. Checks

| Check | Pass condition |
|---|---|
| Real Postgres | same major version and extensions as production; no mocks, no SQLite stand in |
| Isolation | strategy chosen per section 2; suite passes shuffled and parallel |
| App level data | unique ids per test; reads filtered by own ids |
| Fixtures | factories per test; small deterministic seed; no raw production data |
| Constraints | each NOT NULL, UNIQUE, CHECK, FK, exclusion constraint has a test asserting SQLSTATE |
| Concurrency | check-then-write paths tested with two connections and a row count assertion |
| Migrations | data test on N-1 data for every data changing migration; from-zero schema equals snapshot |
| RLS roles | tests run as `authenticated` and `anon`, never as superuser or owner |
| RLS coverage | every table x operation: owner allowed, other user denied, anon denied; denied writes assert unchanged rows |
| RLS mutation | a temporary `using (true)` policy makes at least one deny test fail |
| RLS everywhere | `tests.rls_enabled('public')` or an equivalent query shows no table without RLS |
| Security definer | each such function has its own deny tests |
| Time | no reliance on `now()` moving inside a test transaction |
