# Transactions, concurrency and integrity

How to keep data correct when two requests run at once, when a request is retried, and when part of the work happens outside the database. Sources: PostgreSQL docs (transaction isolation, explicit locking, constraints), Brandur Leach's idempotency keys and transactional outbox posts, Stripe's idempotency design.

## Contents

1. Constraints first, code second
2. Isolation levels as Postgres implements them
3. The lost update and how to prevent it
4. Retrying transactions
5. Locks: row locks, SKIP LOCKED queues, advisory locks, deadlocks
6. Transactions and the outside world
7. Idempotency keys
8. Transactional outbox and job staging
9. Rules for transaction code
10. Checks

## 1. Constraints first, code second

- An app level check (`if (await exists(email)) throw`) is a race: two requests both see "not exists", both insert. Only a UNIQUE constraint stops it. Keep the app check for a friendly message, catch the constraint violation (SQLSTATE 23505) and map it to the same message.
- Same for foreign keys (23503), NOT NULL (23502), CHECK (23514), exclusion (23P01). Map these to 409 or 422 at the API edge, never a 500.
- Business rules that span rows: a unique partial index ("one active subscription per user": `UNIQUE (user_id) WHERE status = 'active'`), an EXCLUDE constraint (no overlapping bookings), or a SERIALIZABLE transaction. Not a SELECT then INSERT.
- Balances and stock: `CHECK (balance_cents >= 0)` makes overdraft impossible even when the app has a bug.

```ts
// good: constraint is the truth, the error is mapped
try {
  await db.insert(users).values({ email });
} catch (e) {
  if (e.code === '23505') return { status: 409, error: 'Email already registered' };
  throw e;
}
```

## 2. Isolation levels in Postgres

| Level | Each statement sees | Anomalies still possible | Must retry? |
|---|---|---|---|
| READ COMMITTED (default) | a fresh snapshot per statement | non repeatable read, phantom, lost update in read-modify-write app code, write skew | no, but you must use atomic updates or locks |
| REPEATABLE READ | one snapshot for the whole transaction | write skew | yes: 40001 "could not serialize access due to concurrent update" |
| SERIALIZABLE | one snapshot, plus conflict detection (SSI) | none | yes: 40001 on any dangerous pattern |

- READ UNCOMMITTED behaves as READ COMMITTED in Postgres. MySQL InnoDB defaults to REPEATABLE READ with different semantics; do not port assumptions across engines.
- Under READ COMMITTED, an `UPDATE ... WHERE` that hits a row changed by a concurrent committed transaction re-checks the WHERE on the new version and applies to it. That makes `SET n = n + 1` safe and makes app side "read, compute, write" unsafe.
- Use SERIALIZABLE when an invariant spans rows you read and rows you write (on call schedule "at least one doctor on call", seat counts across rows, "total allocation must not exceed budget"). It costs some throughput and requires retries; it does not block more than REPEATABLE READ (predicate locks do not block). Declare read only transactions `READ ONLY`; use `SERIALIZABLE READ ONLY DEFERRABLE` for long consistent reports.
- Reports and exports that must be consistent across several queries: run them in one REPEATABLE READ (or the deferrable form above) transaction, not as separate queries.

## 3. The lost update

```ts
// bad: two concurrent requests both read 10, both write 9; one sale is lost
const { stock } = await db.one('select stock from products where id = $1', [id]);
await db.none('update products set stock = $1 where id = $2', [stock - 1, id]);
```

Fixes, in order of preference:

1. **One atomic statement** with the rule in the WHERE:
   ```sql
   update products set stock = stock - 1 where id = $1 and stock > 0 returning stock;
   -- zero rows returned means out of stock
   ```
2. **Row lock** when the new value needs app logic:
   ```sql
   begin;
   select * from accounts where id = $1 for update;   -- second request waits here
   -- compute in app
   update accounts set ... where id = $1;
   commit;
   ```
   Lock rows in a consistent order (sort ids) when locking several, or two transactions deadlock.
3. **Optimistic concurrency** with a version column, for edits that span user think time (a form open for minutes; never hold a lock across that):
   ```sql
   update documents set body = $1, version = version + 1
   where id = $2 and version = $3;     -- 0 rows: someone else saved first, show a conflict
   ```
   Send the version to the client with the form (or use an ETag and `If-Match`, answer 412 on mismatch).
4. **SERIALIZABLE** with retry, when the read set is complex.

## 4. Retrying transactions

- Retry the whole transaction, from BEGIN, including the reads, on SQLSTATE `40001` (serialization failure) and `40P01` (deadlock detected). Never retry only the failing statement. Never retry on other errors blindly.
- Retry 3 to 5 times with jittered backoff (for example 10 ms, 40 ms, 160 ms plus random).
- Nothing with an outside effect may happen inside the retried function (no email, no HTTP call), or it runs once per attempt.

```ts
async function withSerializable<T>(fn: (tx: Tx) => Promise<T>): Promise<T> {
  for (let attempt = 0; ; attempt++) {
    try {
      return await db.transaction(fn, { isolationLevel: 'serializable' });
    } catch (e: any) {
      const retryable = e?.code === '40001' || e?.code === '40P01';
      if (!retryable || attempt >= 4) throw e;
      await sleep((2 ** attempt) * 10 + Math.random() * 10);
    }
  }
}
```

## 5. Locks

- `SELECT ... FOR UPDATE` locks rows against UPDATE, DELETE and other FOR UPDATE. Use `FOR NO KEY UPDATE` when you will not change the key; it does not block inserts of child rows that reference the row (`FOR KEY SHARE`, taken by FK checks).
- Job queue in Postgres: `SELECT ... FOR UPDATE SKIP LOCKED LIMIT n` lets many workers take different rows without waiting:
  ```sql
  with next as (
    select id from jobs
    where run_at <= now() and locked_at is null
    order by run_at limit 10
    for update skip locked
  )
  update jobs set locked_at = now(), attempts = attempts + 1
  from next where jobs.id = next.id
  returning jobs.*;
  ```
  Index `(run_at) WHERE locked_at IS NULL`. Reclaim jobs whose `locked_at` is older than the max run time.
- `NOWAIT` fails immediately instead of waiting; use it for user actions where a 409 beats a hung request.
- Advisory locks for "only one instance runs this cron": `select pg_try_advisory_xact_lock(hashtext('nightly-report'))` inside a transaction (released at commit). Session level advisory locks (`pg_advisory_lock`) survive rollback and break behind PgBouncer transaction pooling; avoid them there.
- Deadlocks: Postgres detects them and aborts one transaction (40P01). Prevent by taking locks in the same order everywhere and by taking the strongest lock you need first. Retry the victim.
- Never hold a transaction open while waiting for a user, a queue, or a network call. Locks are held until commit, and an idle in transaction session blocks VACUUM and migrations. Set `idle_in_transaction_session_timeout`.

## 6. Transactions and the outside world

- A database transaction cannot include a Stripe charge, an email, an S3 upload or an LLM call. If you call out inside the transaction and then roll back, the charge happened and the record of it did not. If you commit and then the call fails, you have a record of something that did not happen.
- Pattern (Brandur's "atomic phases"): commit local state, then make the outside call with an idempotency key, then record the result in a new transaction. Each phase records a recovery point so a retry resumes from the right step.
- Outside calls that support idempotency keys (Stripe, most payment APIs): always send one, derived from your own record (`order_<id>_charge`), so a retry cannot double charge.
- Outside calls that cannot be made idempotent: treat an unknown outcome (timeout) as "maybe happened", record it, and reconcile (query the provider) before retrying.

## 7. Idempotency keys

Every endpoint that creates or changes something and that a client may retry (mobile apps on flaky networks, webhooks, queue consumers) must produce the same result when called twice with the same key.

```sql
create table idempotency_keys (
  id              bigint generated always as identity primary key,
  user_id         bigint not null references users(id),
  key             text not null check (char_length(key) <= 255),
  request_hash    text not null,          -- reject reuse of a key with different params
  locked_at       timestamptz,
  recovery_point  text not null default 'started',
  response_code   int,
  response_body   jsonb,
  created_at      timestamptz not null default now(),
  unique (user_id, key)
);
```

Rules (from Brandur, used at Stripe):

- Scope keys per user, not globally.
- Insert the key first (`INSERT ... ON CONFLICT (user_id, key) DO NOTHING RETURNING`). If it exists: same request hash and finished, return the stored response; still locked by a live request, return 409; different request hash, return 422.
- Store the final response and return it verbatim on replays.
- Reap keys after a retention window (Stripe: 24 hours; Brandur's example: 72 hours to survive a weekend).
- Webhook and queue consumers: dedupe on the sender's event id with a unique constraint (`processed_events (source, event_id) primary key`), inserted in the same transaction as the effect.
- Cheaper alternative when it fits: make the operation naturally idempotent with a client supplied id. The client generates a UUIDv7 for the new order; the server does `INSERT ... ON CONFLICT (id) DO NOTHING`. Offline first apps do this anyway.

## 8. Transactional outbox and job staging

- Problem: you update the database and publish an event (queue, webhook, search index). Doing both directly can lose one when the process dies between them.
- Outbox: in the same transaction as the change, insert a row into `outbox (id, topic, payload, created_at)`. A worker reads the outbox (`FOR UPDATE SKIP LOCKED`), publishes, then deletes or marks the row. Delivery is at least once, so consumers dedupe on the outbox id.
- Background jobs: enqueue them in the database transaction that creates their input (a Postgres backed queue such as pg-boss, graphile-worker, River for Go, Oban for Elixir, or a jobs table). A job enqueued in Redis before the transaction commits can run before its row is visible, or run for a row that was rolled back.

## 9. Rules for transaction code

- Keep transactions short: milliseconds. No user input, no network, no sleeps inside.
- Pass the transaction handle explicitly (`tx`) to every function that must run inside it. A helper that silently uses the global `db` inside a transaction runs outside it, on another connection, and can deadlock against its own caller.
- One connection per transaction. In Node, `await Promise.all([...])` on the same transaction client runs queries on one connection in sequence at best and errors at worst; do it sequentially.
- Savepoints (nested transactions in ORMs) cost a round trip and, in Postgres, subtransactions beyond 64 per transaction degrade performance for the whole cluster (subtrans SLRU overflow, which GitLab hit). Avoid per row savepoints in loops.
- Use `RETURNING` instead of a second SELECT after INSERT or UPDATE.
- Timestamps inside one transaction: `now()` is the transaction start time, the same for every statement. Use `clock_timestamp()` when you need wall time.

## 10. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| Unique rules backed by constraints | each "already exists" check in code has a UNIQUE in the schema | `grep -rniE "already (exists\|registered\|taken)" src/` then find the constraint |
| Constraint errors mapped | 23505/23503/23514 handled at the API edge | `grep -rnE "23505\|23503\|23514\|UniqueViolation\|P2002" src/` |
| No read-modify-write without lock | none | read every function that SELECTs then UPDATEs the same row; look for `for update`, version check or a single UPDATE |
| Retry on 40001/40P01 | present wherever SERIALIZABLE or REPEATABLE READ is used | `grep -rniE "serializable\|repeatable read\|isolationLevel" src/` then read |
| No outside calls in transactions | none | read each `transaction(` / `BEGIN` block for fetch, SDK clients, email, queue publish |
| Idempotency on retryable POSTs | key read and stored | `grep -rniE "idempotency" src/` for payment, order, import, send handlers |
| Webhook dedupe | unique on event id | `grep -rniE "event_id\|webhook" migrations/` |
| Jobs enqueued transactionally | enqueue uses the same tx | read enqueue call sites near writes |
| Session timeouts set | `idle_in_transaction_session_timeout` > 0 | `show idle_in_transaction_session_timeout;` |
| Concurrency test | two parallel requests produce the right final state | a test that fires the same endpoint N times with `Promise.all` and asserts the count/balance |
