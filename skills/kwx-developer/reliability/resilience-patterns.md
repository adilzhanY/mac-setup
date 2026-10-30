# Resilience patterns: timeouts, retries, idempotency, overload, health checks

The code that runs only when something else is failing is the code models get most wrong: retries without backoff, no timeouts, health checks that call the database, fallbacks that DDoS the primary. These rules come from Google's SRE book (ch. 21 "Handling Overload", ch. 22 "Addressing Cascading Failures") and the AWS Builders' Library. They apply to any service that calls another service, a database, or a third party API, including a mobile app calling your backend.

## Contents

1. Timeouts and deadlines (R1 to R5)
2. Retries, backoff, jitter (R6 to R12)
3. Idempotency (R13 to R16)
4. Overload, load shedding, queues (R17 to R23)
5. Fallbacks, caches, circuit breakers (R24 to R27)
6. Health checks (R28 to R33)
7. Code templates
8. Checks

## 1. Timeouts and deadlines

**R1. Every remote call has a timeout, including connect, DNS and TLS.** The default for `fetch`, Node `http`, most DB drivers and Rust `reqwest` is no request timeout or a very long one. A call without a timeout holds a socket, a pool slot and memory until the process restarts.

```ts
// Bad: hangs forever if the peer stops responding
const res = await fetch(url);
// Good
const res = await fetch(url, { signal: AbortSignal.timeout(2_000) });
```

```rust
let client = reqwest::Client::builder()
    .connect_timeout(Duration::from_millis(500))
    .timeout(Duration::from_secs(2))
    .build()?;
```

**R2. Pick the timeout from data.** Choose an acceptable false timeout rate (for example 0.1%) and set the timeout at that percentile of the dependency's latency (p99.9), plus padding when p99.9 is close to p50, plus worst case network latency for calls over the internet (AWS). A timeout three orders of magnitude above normal latency is a bug: with 5% of requests hanging for a 100 s deadline, a frontend with 1,000 threads can serve only about 20% of traffic (SRE book, "Bimodal latency").

**R3. Propagate deadlines, do not invent new ones.** The edge sets the total budget (for example 10 s for an API request, 30 s for a page). Each hop passes the remaining time minus a margin for its own work. A downstream call never gets a longer timeout than what is left of the caller's. gRPC does this with deadlines; for HTTP pass the remaining budget in a header or an `AbortSignal` through the call chain.

**R4. Check the deadline before each expensive stage.** If the client has already given up, stop: "you don't get credit for late assignments with RPCs" (SRE book). Pass `AbortSignal` into DB queries and fetches so work is cancelled when the request is.

**R5. Database statements have a server side timeout.** Postgres: set `statement_timeout` (for example 5 s for web requests) and `idle_in_transaction_session_timeout` per role or per connection; migrations set `lock_timeout` (see `deploy-and-rollback.md`). A pool `acquire` timeout is separate and also required.

## 2. Retries, backoff, jitter

**R6. Retry only at one layer.** Retries multiply: 3 attempts at each of 5 layers is 3^5 = 243 attempts on the database for one user action (AWS); 4 attempts at 3 layers is 64 (SRE book). Pick the layer closest to the failing dependency, and have every other layer pass the failure up. A layer that gives up returns an explicit "overloaded, do not retry" status so the layers above do not retry either.

**R7. Capped exponential backoff with full jitter.** Never retry immediately in a loop, never retry at fixed intervals. Without jitter, all clients that failed together retry together.

```ts
// full jitter: sleep = random(0, min(cap, base * 2^attempt))
const delay = Math.random() * Math.min(capMs, baseMs * 2 ** attempt);
```

**R8. Limit attempts per request (default: 3 attempts total).** Then fail. Google uses at most 3 attempts per request (SRE book ch. 21).

**R9. Add a retry budget per client or per process.** Allow retries only while retries are under about 10% of requests (Google), or use a token bucket (AWS SDK behavior since 2016). This turns a capacity failure into some dropped requests instead of a 3x load spike that keeps the dependency down after the trigger is gone.

**R10. Retry only what can succeed.** Retryable: connection reset, timeout on an idempotent call, 429, 502, 503, 504, Postgres `40001` and `40P01`. Never retryable: 400, 401, 403, 404, 409, 422, validation errors, "overloaded, do not retry". Honor `Retry-After`.

**R11. Do not retry non-idempotent calls without an idempotency key.** A timeout does not mean the side effect did not happen (AWS).

**R12. Count retries.** Emit a metric for retries per dependency and alert when it rises. Retries that are rarely needed become a hidden fallback mode that only runs during incidents (AWS, "Avoiding fallback"). Graphs of retry rate are how retry storms are diagnosed (SRE book).

Jitter is not only for retries: add jitter to every periodic job and timer (cron at minute 0, cache TTLs that expire together, clients polling every 60 s). AWS uses a per host deterministic jitter (hash of host id) so the pattern is reproducible for debugging.

## 3. Idempotency

**R13. Every mutating endpoint that a client may retry accepts an idempotency key.** Caller generates a unique key (UUID v4 or v7) per logical operation and reuses it on every retry; the server stores `(caller, key) -> request fingerprint, status, response` and returns the stored response for a repeat (AWS "Making retries safe with idempotent APIs"; Stripe `Idempotency-Key` header).

**R14. Same key, different parameters, is an error.** Return 409/422 ("idempotency key reused with different parameters"), never silently apply or silently return the old result.

**R15. Store the key in the same transaction as the side effect.** A unique constraint on `(account_id, idempotency_key)` makes concurrent duplicates fail fast. Keep keys for at least the client's maximum retry window (24 hours is a common default).

**R16. Queue consumers are idempotent by design.** Every mainstream queue (SQS, Kafka consumers, Postgres based queues) is at-least-once. Deduplicate on a message id or make the write naturally idempotent (upsert with a version, `INSERT ... ON CONFLICT DO NOTHING`).

```sql
CREATE TABLE idempotency_keys (
  account_id   uuid        NOT NULL,
  key          text        NOT NULL,
  request_hash text        NOT NULL,
  status_code  int,
  response     jsonb,
  created_at   timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (account_id, key)
);
```

## 4. Overload, load shedding, queues

**R17. Know your breaking point.** Load test each component until it fails and beyond, with both ramped and sudden load, and test recovery back to normal load. The goal: past capacity, goodput plateaus and excess is rejected cheaply, instead of throughput collapsing (SRE book; AWS "Using load shedding to avoid overload").

**R18. Limit concurrency per process and reject the excess early.** A cap on in-flight requests (semaphore) returning 503 with `Retry-After` keeps latency low for the requests accepted. Keep queues short: a queue sized 10x the thread pool turns a 100 ms request into 1.1 s (SRE book). For steady traffic, queue length at most about 50% of the worker count.

**R19. Rejections must be cheap and visible.** Reject before parsing bodies or touching the DB; record who was rejected and why; keep rejected latency out of the success latency metric (AWS).

**R20. Prioritize.** When shedding, drop background sync, prefetch and batch traffic before interactive user requests. Set criticality at the edge and propagate it (SRE book ch. 21).

**R21. Per client fairness.** One tenant must not consume all workers: cap per tenant concurrency or quota (for example no single client above 25% of threads, SRE book).

**R22. Queues hide outages until they make them worse.** An hour of backlog needs double capacity for an hour to drain (AWS). Monitor the age of the oldest message, set a max age or TTL after which messages are dropped or dead lettered, bound retry counts, and have a dead letter queue with an alarm. Consider LIFO or prioritizing fresh work during recovery when old work has lost its value.

**R23. No unbounded in-memory buffers.** Every array, channel or map that grows with input has a cap (`tokio::sync::mpsc::channel(n)`, not `unbounded_channel`; a bounded `p-queue`), and a decided behavior when full.

## 5. Fallbacks, caches, circuit breakers

**R24. Avoid fallback for critical paths.** A fallback runs only during failures, so it is untested and often adds load to the thing that is failing. Amazon's 2001 cache fallback to direct database queries took down the website and all fulfillment centers (AWS). Prefer: make the primary path more reliable, let the caller handle the error, push data ahead of time so no runtime call is needed, or run both paths all the time (failover).

**R25. Know whether a cache is a latency cache or a capacity cache.** If the service cannot handle its load with an empty cache, the cache is a hard dependency: plan for cold start (warm before taking traffic, ramp load slowly after a restart), and never respond to a cache outage by sending all traffic to the database (SRE book "Slow startup and cold caching"; GitHub 2021: a TTL cut from 12 h to 2 h plus 10x read growth overloaded the database).

**R26. Prefer bounded retries plus load shedding over circuit breakers.** Circuit breakers add a mode that is hard to test and can slow recovery (AWS). If you use one, make it per dependency and per host, half-open with a small probe rate, and test the open state in CI.

**R27. Degraded modes are tested continuously.** If the product has a degraded mode (serve stale data, hide recommendations), exercise it regularly in production (for example a small slice of servers near overload, SRE book) and alert when many servers enter it. Each degraded mode needs a fast manual off switch.

## 6. Health checks

**R28. Separate liveness from readiness.**

| Endpoint | Question | Checks | Failure action |
|---|---|---|---|
| `/livez` (liveness) | Is the process alive and not deadlocked? | The event loop or runtime responds. Nothing external | Restart the container |
| `/readyz` (readiness) | Should this instance get traffic now? | Startup finished (migrations checked, caches warm, config loaded), not shutting down, local resources OK (disk writable) | Remove from load balancer, do not restart |
| startup probe | Has slow startup finished? | Same as readiness, with a long window | Hold liveness checks until it passes |

**R29. Liveness never checks dependencies.** If the database is down and liveness checks it, every pod restarts at once, caches go cold and the database gets a reconnect storm when it returns. The Kubernetes docs warn that wrong liveness probes cause cascading failures.

**R30. Readiness should check only local, instance specific health.** A readiness check that fails when a shared dependency fails removes every instance at once. AWS teams restrict fast acting load balancer checks to local checks and run dependency checks from a separate monitor that alerts or acts with rate limits. If you do check a dependency, check it in a background loop and serve a cached flag, and rely on load balancer fail-open (when all targets fail, route to all).

**R31. Health checks are cheap, fast and prioritized.** No DB query per probe (cache the result for a few seconds), keep spare worker capacity for probes, respond within the probe timeout even under load. An overloaded instance that fails its probe shrinks the fleet and overloads the rest (AWS).

**R32. Report the version in the health response** (`{"status":"ok","version":"<git sha>"}`) so out of date or zombie instances can be detected after a deploy.

**R33. A deploy waits for readiness, and fails the deploy if instances never become ready.** A start script that forks the server and reports "done" immediately lets a crashing build roll across the whole fleet (AWS).

## 7. Code templates

### TypeScript retry with budget, backoff and jitter

```ts
export async function withRetry<T>(
  fn: (signal: AbortSignal) => Promise<T>,
  { attempts = 3, baseMs = 100, capMs = 2_000, timeoutMs = 2_000, isRetryable }:
  { attempts?: number; baseMs?: number; capMs?: number; timeoutMs?: number; isRetryable: (e: unknown) => boolean },
): Promise<T> {
  for (let attempt = 0; ; attempt++) {
    try {
      return await fn(AbortSignal.timeout(timeoutMs));
    } catch (err) {
      if (attempt + 1 >= attempts || !isRetryable(err) || !retryBudget.tryTake()) throw err;
      metrics.retries.inc({ dep: "payments" });
      await new Promise((r) => setTimeout(r, Math.random() * Math.min(capMs, baseMs * 2 ** attempt)));
    }
  }
}
```

Before writing this, check whether the client already retries: the AWS SDK, `@octokit`, Stripe SDK, `ky`, many gRPC clients retry by default. Two retry layers is rule R6 broken.

### Rust

Use `tower::retry` with a `Budget` (tower has `TpsBudget`) or `backon` / `tokio-retry` with jittered exponential backoff; wrap each attempt in `tokio::time::timeout`. Use `tower::limit::ConcurrencyLimitLayer` and `tower::load_shed::LoadShedLayer` for R18.

## 8. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| Every fetch has a timeout | Every `fetch(` passes `signal` | `rg -n 'fetch\(' src | rg -v 'signal'` returns 0 (review wrapper usage) |
| HTTP clients configured with timeouts | axios `timeout`, reqwest `.timeout(`, got `timeout` set at client creation | `rg -n 'axios.create|Client::builder|got.extend' src` and read |
| DB statement timeout | Set on role, pool or connection | `rg -n 'statement_timeout' .`; `psql -c 'show statement_timeout'` as the app role |
| Pool acquire timeout | Set | `rg -n 'connectionTimeoutMillis|acquire_timeout' src` |
| No immediate retry loops | No retry without sleep and cap | `rg -nU 'while *\(.*retr|for .*attempt' src` and read each |
| Jitter present | Backoff uses randomness | `rg -n 'Math\.random|rand::' src/**/retry*` |
| One retry layer | SDK retries disabled or own wrapper not used on that dependency | Read client configs (`maxRetries`, `retries`) for each dependency |
| Idempotency keys on retried writes | POST endpoints for payments, orders, sends accept and store a key | `rg -n -i 'idempotency' src`; DB has unique constraint |
| Queue consumers dedupe | Message id stored or upsert used | `rg -n 'ON CONFLICT|message_id|dedup' src/workers` |
| Bounded channels and queues | No unbounded channels | `rg -n 'unbounded_channel|unbounded\(' src` returns 0 or justified |
| Liveness has no dependency checks | `/livez` handler touches no DB, cache or HTTP client | Read the handler; `rg -n -A15 'livez|healthz' src` |
| Readiness flips to false on shutdown | SIGTERM handler sets not-ready first | `rg -n -A10 'SIGTERM' src` |
| Health returns version | Response includes git SHA | `curl -s localhost:PORT/readyz` |
| Load shedding exists for public services | Concurrency limit or 503 path exists and is tested | `rg -n 'ConcurrencyLimit|LoadShed|503|Retry-After' src` and a load test result |
| Load tested past breaking point | A recorded load test shows goodput plateau | Check `load-tests/` (k6, oha, vegeta) and its last report |
