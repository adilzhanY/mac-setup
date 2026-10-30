# Rate limits, retries, timeouts, overload

Read when: writing any code that calls another service (HTTP, DB, Redis, a third party API, an LLM), any endpoint that can be abused or is expensive, any client that fetches data, and any retry loop.

Sources: AWS Builders' Library ("Timeouts, retries, and backoff with jitter", "Using load shedding to avoid overload"), AWS Architecture Blog "Exponential Backoff And Jitter", Google SRE book chapters 21 and 22, Stripe "Scaling your API with rate limiters", Cloudflare "Counting things", IETF RateLimit headers draft 11, RFC 9110 and 6585, TanStack Query docs.

## Contents

1. The failure models skip
2. Timeouts: every remote call, with numbers
3. Deadlines: propagate the remaining budget
4. Retries: which, how many, how spaced, at which layer
5. Circuit breakers and retry budgets
6. Server side rate limiting
7. Overload: load shedding and bounded queues
8. Client side: call the server less
9. Checks

## 1. The failure models skip

Models write the happy path: `await fetch(url)`, `for (i < 5) retry`, no limit on the login route. In production this produces:

- A hung dependency holds every worker thread forever, because nothing had a timeout. One slow service takes down the caller (bimodal latency: Google SRE shows 5% of requests hanging for 100 s leaves capacity for only about 20% of traffic).
- Retries at every layer multiply. AWS: 3 tries at each of 5 layers is 3^5 = 243x the load on the database. Google SRE: 4 attempts at each of 3 layers is 64 attempts. The retry storm keeps the system down after the original cause is gone.
- Retries without jitter synchronize: every client retries at the same instants and hits the server in waves.
- An unlimited endpoint (login, signup, password reset, SMS send, LLM call) becomes the cost or abuse vector.

## 2. Timeouts: every remote call, with numbers

Rule: no remote call without a timeout. That includes HTTP, database queries, Redis, queue operations, DNS, TLS, and SDK calls. Library defaults are usually infinite or minutes long:

| Client | Default | What to set |
|---|---|---|
| Node `fetch` (undici) | headers and body timeouts 300 s, no total | `fetch(url, { signal: AbortSignal.timeout(5000) })` |
| axios | 0 (none) | `axios.create({ timeout: 5000 })` |
| Rust `reqwest` | none | `Client::builder().connect_timeout(2s).timeout(10s)` |
| Postgres server | `statement_timeout = 0` (none) | per role or per pool: `SET statement_timeout = '5s'`, plus `idle_in_transaction_session_timeout = '30s'` |
| node-postgres pool | `connectionTimeoutMillis = 0` (wait forever for a connection) | `connectionTimeoutMillis: 2000`, `query_timeout` |
| sqlx pool | `acquire_timeout` 30 s | 2 to 5 s for request paths |
| Go `http.Client` | none | `Timeout: 10 * time.Second` |

How to pick the number (AWS Builders' Library):

1. Choose an acceptable false timeout rate, for example 0.1%.
2. Take the dependency's latency at the matching percentile (p99.9) and set the timeout there.
3. Add the worst case network latency if the caller is far away (mobile, cross region).
4. If p99.9 is close to p50, add padding, or a small latency shift times out everything.

Starting points when you have no latency data yet:

- Connect timeout: 1 to 3 s (default 2 s). Connecting should be fast; a slow connect means the host is gone.
- Internal service or DB query on a user request: 1 to 5 s.
- Third party API on a user request: 5 to 10 s.
- LLM or other generative API: 30 to 120 s total, but stream and set an idle timeout between chunks (for example 30 s).
- Webhook delivery you send: 15 to 30 s (Standard Webhooks).
- Background job: a hard per-job timeout shorter than the queue's visibility timeout or lease (see `webhooks-and-jobs.md`).

The user facing request has its own total budget (for example 10 s at the load balancer, often 30 to 60 s by default). Every inner timeout must fit inside it, or the outer layer gives up while inner work keeps burning resources.

```ts
// bad: no timeout, unbounded retry, no jitter
async function getRate() {
  for (;;) {
    try { return await (await fetch(RATES_URL)).json(); } catch { await sleep(1000); }
  }
}

// good
const res = await fetch(RATES_URL, { signal: AbortSignal.timeout(3000) });
```

```rust
// good: one shared client, built once, with both timeouts
let http = reqwest::Client::builder()
    .connect_timeout(std::time::Duration::from_secs(2))
    .timeout(std::time::Duration::from_secs(10))
    .build()?;
```

Also: build HTTP clients and DB pools once per process and reuse them. A new client per request means a new TCP and TLS handshake per request, which is slow and exhausts ephemeral ports. Warm connections at startup so the first requests after a deploy do not spend their budget on handshakes (AWS).

## 3. Deadlines: propagate the remaining budget

A timeout per hop is not enough when calls chain. Pass the remaining time down (Google SRE, AWS):

- Compute a deadline at the edge (`now + 10s`). Each hop gets `deadline - now - small margin` (a few hundred ms for the network and post-processing, Google SRE).
- Before an expensive stage, check the remaining time; if it is not enough to finish, fail now instead of doing work nobody will receive.
- When the client disconnects or the deadline passes, cancel downstream work. In Node pass an `AbortSignal` through; in Rust drop the future or use `tokio::time::timeout`; in Go use `context.Context`.
- Never let an inner timeout be longer than the outer one.

```ts
async function handler(req: Request) {
  const signal = AbortSignal.any([req.signal, AbortSignal.timeout(8000)]); // client gone OR budget spent
  const user = await fetch(USERS + id, { signal });
  const orders = await db.query({ text: Q, values: [id], signal }); // if your driver supports it
}
```

## 4. Retries: which, how many, how spaced, at which layer

### Which failures to retry

| Failure | Retry? |
|---|---|
| Connection refused, reset, DNS failure, timeout before any response | yes, if the operation is idempotent or carries an idempotency key |
| 408, 429 | yes, after `Retry-After` if present |
| 502, 503, 504 | yes, with backoff, `Retry-After` if present |
| 500 | only for idempotent reads, at most once or twice; often a bug that will not change |
| 400, 401, 403, 404, 409, 422 | no. The same request will fail the same way (AWS). Fix the request, refresh the token once on 401, or surface the error |
| A timeout on a non-idempotent call without a key | no. You do not know whether it happened. Mark it unknown and reconcile (brandur) |
| An "overloaded, do not retry" signal from the server | no (Google SRE) |

Never retry a POST that creates or charges unless it carries an idempotency key (`api-design.md` section 6).

### How many

- At most 3 attempts in total (1 try + 2 retries) on a user facing path (Google SRE caps per request at 3). Background jobs may retry longer, but over minutes to hours via the job queue, not in a tight loop in memory.
- Stop early if the remaining deadline cannot fit another attempt.

### How spaced: exponential backoff with full jitter

Use "Full Jitter" from the AWS Architecture Blog. It did the least total work in their simulation and is the simplest:

```
sleep = random_between(0, min(cap, base * 2 ** attempt))
```

Equal jitter (`t = min(cap, base*2**n); sleep = t/2 + random(0, t/2)`) took longer for slightly more work; decorrelated jitter (`sleep = min(cap, random(base, prev_sleep * 3))`) did more calls. No jitter was "the clear loser". Defaults: `base = 100 ms`, `cap = 2 s` for interactive paths, `cap = 30 s to 5 min` for background work.

```ts
async function withRetry<T>(fn: (signal: AbortSignal) => Promise<T>, opts = { attempts: 3, baseMs: 100, capMs: 2000 }): Promise<T> {
  for (let attempt = 0; ; attempt++) {
    try {
      return await fn(AbortSignal.timeout(3000));
    } catch (err) {
      if (attempt + 1 >= opts.attempts || !isRetryable(err)) throw err;
      const retryAfterMs = retryAfterFrom(err);              // parse Retry-After: seconds or HTTP date
      const backoff = Math.random() * Math.min(opts.capMs, opts.baseMs * 2 ** attempt);
      await sleep(retryAfterMs ?? backoff);
    }
  }
}
```

```rust
// Rust: backon crate, or tokio-retry; the formula is the same
use backon::{ExponentialBuilder, Retryable};
let body = (|| async { http.get(url).send().await?.error_for_status()?.text().await })
    .retry(ExponentialBuilder::default().with_jitter().with_max_times(2).with_max_delay(Duration::from_secs(2)))
    .when(|e: &reqwest::Error| e.is_timeout() || e.is_connect() || e.status().map_or(false, |s| s.is_server_error() || s.as_u16() == 429))
    .await?;
```

Most official SDKs (AWS, Stripe, OpenAI, Anthropic) already retry with backoff. Do not wrap an SDK call that retries in another retry loop; configure the SDK's `maxRetries` instead.

Add jitter to every timer too: cron jobs, cache TTLs, polling intervals, token refresh. Use a fixed per-host offset for scheduled jobs so spikes are reproducible (AWS).

### At which layer

Retry at exactly one layer, the one closest to the failing dependency that can do it cheaply, usually the direct caller (Google SRE, AWS). Layers above pass the error up. If a layer exhausted its retries, it returns a "do not retry" error to its caller. Check: grep for retry helpers and draw the call chain; two retrying layers on one path is a defect.

## 5. Circuit breakers and retry budgets

A retry budget caps retry traffic as a fraction of normal traffic. Default: retries may be at most 10% of requests per client (Google SRE: worst case load drops from about 3x to about 1.1x). AWS SDKs implement the same idea as a retry token bucket: each retry spends a token, successes refill it, and when it is empty the client stops retrying (AWS prefers this over circuit breakers, which "introduce modal behavior into systems that can be difficult to test").

Default: use a retry budget (or your SDK's built-in one). Add a circuit breaker only around a dependency that fails slowly and whose failure you can degrade around:

- Closed: count failures. Trip when the failure rate over a rolling window passes a threshold (for example 50% of at least 20 calls in 10 s), not on N consecutive failures in low traffic.
- Open: fail immediately with a fallback (cached value, default, "try later" message) for a cool-down (for example 30 s).
- Half open: let one probe through; success closes, failure reopens.
- Count only failures that mean "the dependency is unhealthy" (timeouts, 5xx), never 4xx.
- Log every state change and expose state as a metric (Fowler). Test the open path: code that only runs during outages is the code that does not work (Google SRE).

Client side adaptive throttling (Google SRE): track `requests` and `accepts` over 2 minutes and reject locally with probability `max(0, (requests - K * accepts) / (requests + 1))`, K = 2. Useful for high volume internal clients.

## 6. Server side rate limiting

### What to limit, keyed by what

| Endpoint class | Key | Starting limit (tune by dark launch) |
|---|---|---|
| Authenticated API | user ID or API key (never IP alone: NAT puts thousands of users behind one IP) | token bucket, for example 10 to 100 req/s sustained with a burst of 2x to 5x |
| Unauthenticated public API | IP (or IPv6 /64 prefix) | lower, for example 1 to 10 req/s |
| Login | account identifier AND IP, separately | per account: exponential backoff after failures, hard stop well under 100 consecutive failures (NIST SP 800-63B-4 caps at 100) |
| Password reset, magic link, OTP send, SMS, email | target address or phone AND IP | for example 3 to 5 per hour per target. Every SMS costs money; SMS pumping fraud targets these |
| Signup | IP and device signals | for example 5 per hour per IP |
| Expensive (search, export, report, LLM call, image processing) | user | concurrency limit (for example 2 to 5 in flight per user) plus a daily quota in cost units |
| Webhook receivers | sender | usually unlimited but body size and signature checked first |

Track per account failures, not only per IP, for login (OWASP): credential stuffing rotates IPs, and per IP limits alone do not stop password spraying across accounts.

### Algorithms

- Token bucket: capacity B, refill R per second. Allows bursts up to B and an average of R. Default for API limits (Stripe uses it in Redis).
- Sliding window counter: `rate = prev_count * ((window - elapsed) / window) + curr_count`. Two counters per key, one INCR and one GET. Cloudflare measured 0.003% of requests wrongly allowed or limited over 400 million requests. Good default for simple "N per minute".
- Fixed window: lets 2N through at the window boundary. Avoid for anything security relevant.
- Concurrency limiter: caps in-flight requests per key. Use for CPU heavy endpoints (Stripe example: 20 in progress per user).

Implementation rules:

- Store counters in a shared store (Redis, Postgres, the platform's limiter). In-memory per-process limits multiply by the number of instances and reset on deploy. Exception: a single-instance app.
- Update atomically: a Lua script or `INCR` + `EXPIRE` in one `MULTI`, or a library (`rate-limiter-flexible` in Node, `governor` in Rust for in-process, Upstash Ratelimit on serverless).
- Fail open on limiter errors for normal API limits (Stripe: a Redis outage must not take the API down), but fail closed for login, OTP and SMS limits, where an outage of the limiter would let an attacker through.
- Dark launch new limits: log what would have been rejected for a week, then enforce (Stripe).
- Get the client IP right: take it from the proxy header your platform sets (`X-Forwarded-For` rightmost untrusted hop, or `CF-Connecting-IP`), and only trust it when the request came through that proxy. Reading the leftmost `X-Forwarded-For` lets anyone pick their own IP (ASVS 4.1.3).

### Responses

```http
HTTP/1.1 429 Too Many Requests
Retry-After: 12
RateLimit-Policy: "default";q=100;w=60
RateLimit: "default";r=0;t=12
Content-Type: application/problem+json

{"type": "https://api.example.com/problems/rate-limited", "title": "Too many requests", "status": 429, "code": "RATE_LIMITED", "detail": "Limit is 100 requests per minute. Retry in 12 seconds."}
```

- 429 for per-client limits, 503 for "the whole service is overloaded" (Stripe, RateLimit draft).
- Always send `Retry-After` (delay seconds or HTTP date, RFC 9110 section 10.2.3). Clients must prefer it over their own backoff.
- `RateLimit` and `RateLimit-Policy` (IETF draft 11, May 2026) are optional. Older APIs use `X-RateLimit-Limit/Remaining/Reset`; keep whichever the API already uses.
- The message says what the limit is and when to retry (Stripe: "actionable").

## 7. Overload: load shedding and bounded queues

- Every queue is bounded: thread pool queues, in-memory job arrays, connection pool wait queues. Unbounded queues turn overload into latency until everything times out. Google SRE: for steady traffic, queue length at most about 50% of the worker pool.
- Prefer fail fast over queueing when full ("spillover", AWS): reject with 503 and `Retry-After`.
- Drop requests that waited longer than the client will wait. A request queued past its deadline is pure waste.
- Reserve capacity for critical traffic: Stripe reserves 20% of the fleet for critical calls and sheds non-critical ones with 503 beyond 80%. Health checks always get through (AWS).
- Finish started work before starting new work: prioritize page 2 of a list and the second step of a checkout over new sessions (AWS).
- Measure goodput (successful responses within the deadline), not throughput. Keep rejected requests out of the latency metrics or median latency looks great during an outage (AWS).

## 8. Client side: call the server less

Many backend overloads are front end bugs: a request per keystroke, the same query fired by five components, polling every second, retries without backoff.

Rules, all with a default:

- Debounce input driven requests. Search as you type: 250 to 300 ms after the last keystroke, and not below 2 characters. Throttle scroll or resize driven requests to at most one per 100 to 200 ms.
- Cancel stale requests. When a newer request supersedes an older one (new search term, route change, component unmount), abort the old one. Otherwise an old slow response can land after the new one and show wrong results.

```ts
let current: AbortController | undefined;
async function search(q: string) {
  current?.abort();
  current = new AbortController();
  const res = await fetch(`/api/search?q=${encodeURIComponent(q)}`, { signal: current.signal });
  return res.json();
}
```

- Dedupe in-flight identical requests: one shared promise per key. Data libraries do this for you (TanStack Query, SWR, RTK Query, Apollo). Prefer them over hand-rolled `useEffect` fetching.

```ts
const inflight = new Map<string, Promise<unknown>>();
function dedupedGet<T>(url: string): Promise<T> {
  let p = inflight.get(url) as Promise<T> | undefined;
  if (!p) {
    p = fetch(url).then(r => r.json()).finally(() => inflight.delete(url));
    inflight.set(url, p);
  }
  return p;
}
```

- Cache with stale-while-revalidate. Show the cached value immediately and refetch in the background. TanStack Query defaults: data is stale immediately (`staleTime` 0), refetched on mount, window focus and reconnect, kept for 5 minutes after unused (`gcTime`), failed queries retried 3 times with exponential backoff. For most dashboards set `staleTime` to 30 s to 5 min so tab switching does not refetch everything; set `retry: false` or a predicate that skips 4xx.
- Batch: when a screen needs 50 items by ID, send one `GET /items?ids=a,b,c` or a batch endpoint, not 50 requests (N+1 over HTTP). DataLoader style batching collects calls in one tick.
- Poll slowly and stop when hidden. Poll at 5 to 30 s with jitter, pause when `document.visibilityState === "hidden"`, and prefer server push (SSE, WebSocket) or webhooks when updates are rare.
- Back off on errors. Never retry on a fixed interval, never retry 4xx, honor `Retry-After`, and cap total retries.
- Disable the submit button while a mutation is in flight and send an idempotency key so a double click is harmless.
- Prefetch only on clear intent (hover over 100 ms, viewport entry) and only cacheable GETs.

## 9. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| Every fetch has a timeout | each `fetch(` has a `signal`, each axios instance a `timeout` | `rg -n "fetch\(" --type ts \| rg -v "signal"`; `rg -n "axios\.(get\|post\|create)" ` and check config |
| Rust HTTP clients have timeouts | every `reqwest::Client` is built with `.timeout(` and `.connect_timeout(` | `rg -n "Client::new\(\)\|reqwest::get\(" --type rust` (both have no timeout) |
| DB statement timeout set | role, pool or connection sets `statement_timeout` | `rg -n "statement_timeout"`; `SHOW statement_timeout;` on the app role is not `0` |
| Clients reused | no client or pool constructed inside a handler | `rg -n "new Pool\(\|Client::new\(\|Client::builder\(\)" ` and check it is at module/app-state level |
| Retries bounded and jittered | every retry loop has a max attempt count and `Math.random`/jitter | `rg -n "retry\|attempt" ` ; `rg -n "while \(true\)\|for \(;;\)\|loop \{" ` near network calls |
| No non-idempotent retry | retried POSTs carry an `Idempotency-Key` | read each retry wrapper's call sites |
| One retry layer | no retry wrapper around an SDK that already retries | check SDK `maxRetries` config next to any custom retry |
| Auth routes limited | login, signup, reset, OTP/SMS routes pass through a limiter keyed by target and IP | `rg -n "login\|signin\|reset\|otp\|sms\|magic" ` in routes; confirm limiter middleware |
| Limits keyed correctly | authenticated limits key on user/API key, not IP | read limiter key function |
| Client IP trusted correctly | no `x-forwarded-for` split `[0]` without trusted proxy config | `rg -n "x-forwarded-for" -i` |
| 429 carries Retry-After | every 429 response sets `Retry-After` | `rg -n "429" ` and check header set |
| Queues bounded | no unbounded in-memory arrays used as job queues; worker pools have max size | `rg -n "unbounded_channel\|new Array\(\)\.push" `; tokio `mpsc::channel(n)` used instead |
| Search debounced and cancelled | input driven fetch uses debounce and AbortController or a query library | read search components |
| No hand-rolled fetch in effects when a query lib exists | `useEffect(() => { fetch(` absent when TanStack/SWR is a dependency | `rg -n "useEffect\(.*\n?.*fetch\(" -U` |
