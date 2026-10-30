# Webhooks, queues and background jobs

Read when: receiving webhooks (Stripe, GitHub, Supabase, Clerk, any provider), sending webhooks to customers, adding a background job, a queue consumer, a cron task, or any "do this after the request" logic.

Sources: Stripe webhook docs, Standard Webhooks spec v1, brandur "Implementing Stripe-like Idempotency Keys in Postgres", microservices.io transactional outbox, AWS Builders' Library "Avoiding insurmountable queue backlogs", Google SRE book.

## Contents

1. Delivery guarantees you actually get
2. Receiving webhooks: the handler template
3. Sending webhooks
4. The dual write problem and the outbox
5. Background jobs and queues
6. Scheduled jobs (cron)
7. Checks

## 1. Delivery guarantees you actually get

Assume, for every webhook provider and every queue:

- At least once delivery. The same event arrives twice or more (Stripe: "occasionally receive the same event more than once"; queue redelivery after a visibility timeout).
- No ordering. `invoice.paid` can arrive before `invoice.created` (Stripe: "doesn't guarantee delivery of events in the order in which they're generated").
- Delays. Retries span hours to days (Stripe retries with exponential backoff for up to 3 days in live mode).
- Forgeries. Anyone who finds the URL can POST to it.

So every consumer must be: authenticated (signature), idempotent (dedupe by event ID or naturally idempotent writes), order independent (read current state, compare versions), and fast to acknowledge.

## 2. Receiving webhooks: the handler template

```ts
// Express. The raw body is required: any JSON parse + re-stringify changes bytes and breaks the HMAC.
app.post("/webhooks/stripe", express.raw({ type: "application/json", limit: "1mb" }), async (req, res) => {
  let event: Stripe.Event;
  try {
    event = stripe.webhooks.constructEvent(req.body, req.header("stripe-signature")!, process.env.STRIPE_WEBHOOK_SECRET!);
  } catch {
    return res.status(400).send("bad signature");           // no detail, no processing
  }

  // Dedupe and enqueue in one transaction; the unique key makes redelivery a no-op.
  await db.$transaction(async (tx) => {
    const inserted = await tx.$executeRaw`
      INSERT INTO webhook_events (provider, event_id, type, payload)
      VALUES ('stripe', ${event.id}, ${event.type}, ${JSON.stringify(event)}::jsonb)
      ON CONFLICT (provider, event_id) DO NOTHING`;
    if (inserted === 1) await enqueue(tx, "process_stripe_event", { eventId: event.id });
  });

  res.sendStatus(200);                                     // ack fast; real work happens in the job
});
```

Rules:

1. Verify the signature on the raw request bytes before anything else. Frameworks that parse JSON first (Express `json()`, Next.js body parser, NestJS default) break verification; mount a raw body parser on the webhook route only. Next.js App Router: `const body = await req.text()`.
2. Use the provider's SDK verifier (`stripe.webhooks.constructEvent`, `@octokit/webhooks` `verify`, `standardwebhooks` package, Svix). If you must hand-roll: HMAC-SHA256 over the exact signed string, compare with a constant time function (`crypto.timingSafeEqual`, Rust `subtle::ConstantTimeEq` or `hmac::Mac::verify_slice`), never `===`.
3. Reject stale timestamps to stop replays. Stripe's libraries default to a 5 minute tolerance. Keep the server clock on NTP.
4. Support multiple active secrets during rotation (Stripe keeps the old one valid up to 24 hours and sends one signature per active secret). Accept if any configured secret verifies.
5. Ignore signature schemes you do not know (Stripe: only `v1`; ignoring others prevents downgrade attacks).
6. Return 2xx fast, before slow work. Persist the event and enqueue a job, then return (Stripe: return 200 "before any complex logic that might cause a timeout"; month-start renewals spike delivery volume). Return 2xx for event types you do not handle, or the provider retries them for days.
7. Return non-2xx only when you want a retry (storage down). A 3xx counts as failure (Stripe, Standard Webhooks): point the provider at the final URL.
8. Dedupe by event ID with a unique constraint, inside the same transaction as the work or the enqueue. Some providers send two distinct events for one change; for those, dedupe on (object ID, event type) too (Stripe).
9. Do not trust the payload for state that matters. Event payloads are snapshots and may be stale or out of order. For money and access decisions, fetch the object from the provider's API in the job (`stripe.subscriptions.retrieve(id)`), or use "thin" events that carry only IDs.
10. Order independence: store the provider's object version or `updated` timestamp and ignore an event older than what you have. Never infer order from the event `created` field (Stripe: second precision, ties are common).
11. Exempt the webhook route from CSRF middleware (it has no session), and only that route (Stripe).
12. Subscribe only to the event types you handle (Stripe).
13. Reconcile: webhooks get lost when your endpoint was down beyond the retry window. For anything involving money, run a periodic job that lists recent objects from the provider API and repairs drift.

## 3. Sending webhooks

Follow Standard Webhooks (standardwebhooks.com, used by Svix, OpenAI, Supabase and others) instead of inventing a format:

- Headers: `webhook-id` (stable across retries, the consumer's dedupe key), `webhook-timestamp` (unix seconds, updated per attempt), `webhook-signature` (`v1,<base64 HMAC-SHA256>`; space separated list during rotation).
- Signed content: `${id}.${timestamp}.${body}`, body byte identical to what is sent.
- Secret: 24 to 64 random bytes, base64, prefixed `whsec_`, unique per endpoint.
- Payload: small (under 20 KB recommended). Thin payloads (IDs, type) are safer for access control; full payloads save the consumer a call.
- Timeout per attempt: 15 to 30 s. Any 2xx is success; 3xx is failure, do not follow redirects; `410 Gone` disables the endpoint; honor `Retry-After` on 429 and 503.
- Retry with exponential backoff and jitter over days. The spec's example schedule: immediately, 5 s, 5 min, 30 min, 2 h, 5 h, 10 h, 14 h, 20 h, 24 h.
- After prolonged failure, disable the endpoint and notify the owner by email or dashboard.
- SSRF: customer supplied URLs point wherever the customer wants, including `http://169.254.169.254/` and your internal network. Send through an egress proxy that blocks private ranges (Stripe's `smokescreen` is the reference), resolve and pin the IP, disallow redirects, and run delivery workers in a subnet with no access to internal services. See `../security/input-and-injection.md` SSRF section.
- Deliver from a queue (one job per delivery attempt), never inline in the request that caused the event.
- Give consumers a way to replay: a dashboard button or `POST /webhook-endpoints/{id}/replay?since=`.

## 4. The dual write problem and the outbox

Writing to the database and then calling another system (publish to a broker, send an email, call Stripe, enqueue to SQS) is two writes without a transaction. Crash between them and one happens without the other.

```ts
// bad: if the process dies after commit, no email; if publish succeeds but commit fails, a ghost email
await db.order.create({ data });
await sqs.send(new SendMessageCommand({ QueueUrl, MessageBody: JSON.stringify({ orderId }) }));
```

Transactional outbox (microservices.io): write the business row and an outbox row in the same transaction. A relay (poller or change data capture) publishes outbox rows and marks them sent. Messages are sent if and only if the transaction commits. The relay can publish twice after a crash, so consumers stay idempotent.

If your job queue lives in the same Postgres (pg-boss, graphile-worker, River for Go, Oban for Elixir, Solid Queue, or a hand-rolled table), enqueueing in the same transaction is the outbox. This is the default for small and medium apps: one database, transactional enqueue, no broker.

Never enqueue a job that refers to a row before that row is committed. A fast worker picks up the job, does not find the row, and fails or silently skips. Enqueue in the transaction, or after commit.

## 5. Background jobs and queues

### When to make it a job

Move work out of the request when it is slow (over a few hundred ms), calls an unreliable third party, can be retried later, or fans out: sending email, generating PDFs, image processing, webhooks out, syncing to a CRM, LLM calls that the user does not wait on.

### Job rules

- Idempotent handlers. Every job can run twice (redelivery after a crash, a lease that expired while the job was still running). Use unique constraints, upserts, idempotency keys to third parties, and "already done" checks keyed on the job's business ID.
- Small payloads: pass IDs, load fresh state in the job. A payload snapshot goes stale while queued and may carry personal data into queue logs.
- Hard timeout per job, shorter than the lease or visibility timeout. If processing can exceed the visibility timeout, two workers run the same job at once (AWS); extend the lease with heartbeats for long jobs or split the work.
- Bounded retries with exponential backoff and jitter (for example 5 to 25 attempts over hours to days), then move to a dead letter state. Classify errors: permanent errors (validation, 4xx from a third party, missing row) fail immediately to dead letter without retries.
- Dead letter queue: alarm on any message in it (AWS: "We alarm if there are any messages in this queue"), with a tool to inspect and replay after a fix.
- Bounded concurrency per job type, and per tenant if tenants can flood the queue. One tenant's 100,000 imports must not delay everyone's password reset emails: separate queues by priority and use per tenant rate limits or fair scheduling (AWS shuffle sharding).
- Transactional jobs that write to the database do so in one transaction with the "job done" mark when the queue is in the same database.
- Graceful shutdown: on SIGTERM stop taking new jobs, finish or release current ones within the platform's grace period (often 10 to 30 s).
- Record attempt count, last error and timestamps on the job row for debugging.

Postgres as the queue (default when you already run Postgres and need under roughly a few thousand jobs per second):

```sql
-- claim one job; SKIP LOCKED lets many workers poll without blocking each other
UPDATE jobs SET status = 'running', locked_until = now() + interval '5 minutes', attempts = attempts + 1
WHERE id = (
  SELECT id FROM jobs
  WHERE status = 'queued' AND run_at <= now()
  ORDER BY priority, run_at
  FOR UPDATE SKIP LOCKED
  LIMIT 1
)
RETURNING *;
-- a reaper re-queues rows with status = 'running' AND locked_until < now()
-- index: CREATE INDEX ON jobs (priority, run_at) WHERE status = 'queued';
```

Prefer an existing library over this hand-rolled table (pg-boss or graphile-worker in Node, apalis or a `sqlx` + SKIP LOCKED worker in Rust, Supabase Queues / pgmq on Supabase). Use a dedicated broker (SQS, Redis Streams, RabbitMQ, Kafka) when throughput, fan-out to many consumers, or cross-service delivery demands it.

### What to measure and alarm on (AWS)

- Age of the oldest queued job, not only queue depth. A growing age means consumers are behind.
- Dead letter count above zero.
- Job failure rate and retry rate per job type.
- Processing time p99 versus the job timeout.
- Expect recovery after an outage to take longer than the outage: draining a backlog needs spare capacity above normal load. For real time data where only the latest matters (presence, live prices), drop or coalesce superseded messages instead of draining them in order.

## 6. Scheduled jobs (cron)

- Exactly one runner per schedule. With N instances, an in-process `setInterval` or `node-cron` runs N times. Use the platform scheduler (Vercel Cron, Supabase pg_cron, Kubernetes CronJob, systemd timer) to enqueue a job, or take a Postgres advisory lock (`pg_try_advisory_lock`) before running.
- Idempotent per period: key the run on its period (`daily_report:2026-10-30`) with a unique constraint, so a retried or doubled run does nothing.
- Add jitter (or a fixed per-job offset) instead of everything at `0 * * * *`. Every app on earth runs at the top of the hour.
- Process in bounded batches with a cursor, not "load all rows" (a table that is small today is not small next year).
- Alert when a scheduled job did not run (dead man's switch: the job pings a heartbeat URL; absence alerts).
- Timezones: schedule in UTC and convert explicitly. "Daily at 9:00" for a user means their timezone, which needs per user scheduling, not one cron.

## 7. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| Webhook signature verified on raw body | each webhook route uses a raw body parser and an SDK verifier before any processing | `rg -n "webhook" ` routes; confirm `express.raw`/`req.text()` and `constructEvent`/`verify` |
| Constant time compare | hand-rolled HMAC checks use `timingSafeEqual`/`verify_slice` | `rg -n "signature.*===\|== *expected" ` |
| Timestamp tolerance | replay window enforced (SDK default or explicit, at most 5 to 10 min) | read verifier config |
| Events deduped | unique constraint on (provider, event_id) and insert with conflict handling | `rg -n "event_id\|eventId" ` in migrations |
| Fast ack | handler enqueues and returns; no third party calls or emails inline | read handler; time it with `stripe trigger` locally |
| Unknown types return 2xx | default branch returns 200 | read the switch |
| No dual writes | no publish/email/HTTP call right after a DB write without outbox or transactional enqueue | `rg -n "await .*send\(\|publish\(" ` after `create(`/`insert` in the same function |
| Jobs idempotent | each job handler tolerates running twice | run the job twice in a test and assert one side effect |
| Retries bounded, DLQ exists | max attempts set; failed jobs land in a dead state that is alerted | queue config; `rg -n "maxAttempts\|retryLimit\|max_attempts" ` |
| Job timeout below lease | per-job timeout < visibility timeout / lock duration | compare config values |
| Single cron runner | no `setInterval`/`node-cron` scheduling in a multi-instance web process | `rg -n "setInterval\|node-cron\|cron\.schedule\|tokio_cron" ` |
| Outgoing webhooks SSRF safe | customer URLs fetched through an egress filter with redirects off | read delivery code; try `http://127.0.0.1` and `http://169.254.169.254` as endpoint URLs in a test |
