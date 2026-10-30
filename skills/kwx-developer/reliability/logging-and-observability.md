# Logging and observability

Telemetry exists to answer two questions fast during an incident: what is broken (symptom) and why (cause) (SRE book ch. 6). Logs, metrics and traces are three views of the same unit of work, joined by one request id. This file gives the defaults for each, what never to log, alerting rules that do not burn out the person on call, and the checks.

## Contents

1. Defaults at a glance
2. Structured logging rules (L1 to L12)
3. What never to log
4. Metrics: what to measure
5. Traces and OpenTelemetry basics
6. Alerting and SLOs
7. Stack recipes (Node, Rust, React Native)
8. Checks

## 1. Defaults at a glance

| Decision | Default |
|---|---|
| Log format | JSON lines to stdout, one object per event. The platform ships them. Never write log files from the app in a container |
| Node logger | `pino` (fast, JSON, built-in `redact`). Not `console.log` in server code |
| Rust logger | `tracing` + `tracing-subscriber` with JSON formatter. Not `println!` / `log` + `env_logger` in services |
| Per request | One wide "canonical" log line at the end of every request, plus error events. Not a line per function |
| Correlation | `request_id` on every log line of the request, propagated to downstream calls; W3C `traceparent` if tracing is on |
| Metrics | RED per endpoint (Rate, Errors, Duration histogram) + USE per resource (Utilization, Saturation, Errors) |
| Latency | Histograms with exponential buckets, report p50/p95/p99. Never alert on averages |
| Traces | OpenTelemetry SDK, OTLP exporter, auto-instrumentation for HTTP/DB, head sampling by trace id |
| Alerting | Page on SLO burn rate (symptoms), ticket on slow burn. Never page on a cause like CPU unless it is imminent saturation |
| Errors | Crash reporter (Sentry or equivalent) with release = git SHA. See `error-handling-strategy.md` |

## 2. Structured logging rules

**L1. Log events, not prose.** A log line is a JSON object with a stable `msg` (or `event`) name and fields. The message is a constant; the variables are fields. Constant messages can be counted and grepped; interpolated ones cannot.

```ts
// Bad
logger.info(`User ${userId} paid ${amount} for order ${orderId}`);
// Good
logger.info({ userId, orderId, amountCents: amount }, "order.paid");
```

**L2. One canonical line per unit of work.** At the end of every request (or queue message, or job run) emit one wide line with everything about it: method, route template (not raw path), status, duration, user or account id, auth method, DB query count and time, downstream call timings, retries, cache hits, feature flags evaluated, error code. Emit it in a `finally` / middleware post step so it fires for failures too, and wrap its own construction so building the line can never fail the request (Stripe, "Canonical log lines"; AWS Builders' Library, "Instrumenting distributed systems": "one log entry per unit of work"). For work that runs minutes or hours, also emit periodic progress lines.

**L3. Every line of a request carries the same `request_id`.** Accept an incoming id (`x-request-id` or `traceparent`) or generate one at the edge, put it in async context (`AsyncLocalStorage` in Node, a `tracing` span in Rust), return it in the response header, include it in error responses shown to users, and pass it on every outgoing call and queue message. A user report with a request id should lead to the exact log lines in one query.

**L4. Log the request intent early.** Record what the request was trying to do before validation, auth or throttling can reject it, so rejected requests are still explainable (AWS). Sanitize first: encode, escape, truncate. Never interpolate raw user input into a log line (log injection via CR/LF).

**L5. Levels have meanings, and production runs at INFO.**

| Level | Meaning | Example |
|---|---|---|
| `error` | A unit of work failed and someone may need to act | request returned 5xx, job gave up after retries |
| `warn` | Degraded but handled; worth a look if it trends | retry succeeded on 2nd attempt, fallback cache used, deprecated API called |
| `info` | Business and lifecycle events | canonical request line, server started, migration applied, order.paid |
| `debug` | Developer detail, off in production | parsed config values (minus secrets), branch decisions |

A 4xx caused by the client is not `error`; it is part of the canonical line. If everything is `error`, nothing is.

**L6. Log once per failure, where it is handled.** Not at every layer (see `error-handling-strategy.md` E3). Include the full cause chain and stack in that one event.

**L7. Separate success latency from failure latency.** Fast failures (throttles, validation errors, load shedding) make average latency look great during an outage. Record a separate timer for successful responses and alarm on that (AWS). The same applies to metrics in section 4.

**L8. Use stable, low cardinality names; put high cardinality in fields.** Route template `/users/:id` in the `route` field, the actual id in `userId`. Never build a metric name or label from a user id, email, URL or error message.

**L9. Make verbosity adjustable at runtime without a deploy, per host or per tenant, and make it expire.** During an incident you need more detail for one customer, not a redeploy at DEBUG for everyone.

**L10. Logging must not take down the service.** Log asynchronously or to stdout, never block a request on a slow log sink. Load test at maximum sustained load to confirm logs ship as fast as they are produced, or disks fill (AWS). A tight error loop that logs a stack per iteration can turn a CPU bound service into an I/O bound one (AWS, "Avoiding fallback"). Rate limit repetitive error logs (log the first, then a count).

**L11. Timestamps in UTC, ISO 8601 or epoch milliseconds, from a synced clock.** Name it once (`time` or `ts`) across all services.

**L12. Logs are not an audit trail and not analytics.** If losing a line would be a compliance or billing problem, write it to a durable table or event stream in the same transaction as the change, not to the log pipeline.

## 3. What never to log

Never log these, at any level, including DEBUG, including inside error objects and request dumps (OWASP Logging Cheat Sheet, "Data to exclude"):

- Passwords, password hashes, one time codes, recovery codes.
- Session ids, access tokens, refresh tokens, API keys, JWTs, `Authorization` and `Cookie` headers, signed URLs (the signature is a credential).
- Database connection strings, encryption keys, any secret from env.
- Payment card data, bank account numbers, government ids, health data.
- Full request or response bodies of auth, payment or profile endpoints.
- Data the user did not consent to, or opted out of.
- Source code, internal file paths, internal hostnames (treat as sensitive; never expose to users).

Personal data (names, emails, phone numbers, IP addresses) is personal data under GDPR. Log a stable internal user id instead. If a raw value is needed for debugging, hash it with a keyed hash so equal values correlate without being readable.

How to enforce it in code, not by memory:

```ts
// pino: redact by path, applied to every line
const logger = pino({
  redact: {
    paths: ["req.headers.authorization", "req.headers.cookie", "*.password", "*.token",
            "*.accessToken", "*.refreshToken", "*.apiKey", "*.secret", "*.cardNumber"],
    censor: "[REDACTED]",
  },
});
```

```rust
// Rust: secrets are a type whose Debug prints [REDACTED]; spans skip arguments by default
use secrecy::{SecretString, ExposeSecret};
#[tracing::instrument(skip_all, fields(user_id = %cmd.user_id))]
async fn login(cmd: LoginCommand) -> Result<Session, AuthError> { /* cmd.password: SecretString */ }
```

- Never log a whole request, response, config, or error object from a third party SDK without checking what it contains: axios errors include the request config with headers; many SDK errors embed the API key.
- When a parse of a customer payload fails, log its size and the parse error position, not the payload (AWS: "it's important to not log the payload to protect customer privacy").
- Logs have retention and access control: restrict who can read production logs and keep them only as long as needed.

## 4. Metrics: what to measure

**Four golden signals** for every user facing service (SRE book): latency, traffic, errors, saturation. In practice:

- **RED per endpoint or operation**: request rate, error rate (5xx and timeouts, split client fault vs server fault), duration histogram (successful requests separately).
- **USE per resource**: DB connection pool (in use / max, wait time), worker pool, queue depth and oldest message age, memory, file descriptors, event loop delay (Node), disk.
- **Per dependency**: call count, error count by kind, latency histogram, retry count, circuit or throttle state. One metric per dependency per operation (per table for DynamoDB style stores), so "slow because of retries" is visible (AWS).
- **Per queue**: age of the oldest message and age at first attempt, not only depth (AWS, "Avoiding insurmountable queue backlogs"). Depth says how much, age says how late.
- **Availability as a 0/1 metric**: emit 1 on success and 0 on failure; the average is the availability rate (AWS).
- **A counter per error reason**, not one lumped error counter.

Rules:

- **M1. Histograms, not averages.** Latency is bimodal and long tailed; "the 99th percentile of one backend can easily become the median response of your frontend" (SRE book). Buckets roughly exponential (factor 2 to 3), covering 1 ms to your max timeout.
- **M2. Label cardinality is bounded.** Labels like `route`, `method`, `status_class`, `dependency` are fine. `user_id`, `email`, `url`, `error_message`, `trace_id` are not; each unique value creates a new time series.
- **M3. Delete what nobody looks at.** A metric on no dashboard and in no alert is a removal candidate; alert rules not exercised in a quarter are up for removal (SRE book).
- **M4. Measure from the client side too.** The load balancer, the caller, or a synthetic probe sees failures the server cannot report (a server whose disk is full may report nothing).

## 5. Traces and OpenTelemetry basics

Use OpenTelemetry for new instrumentation; it is vendor neutral and every major backend ingests OTLP.

- **Span** = one timed operation with a name, start/end, attributes, events, and status. A **trace** = the tree of spans for one request, sharing a `trace_id`.
- **Context propagation**: the default propagator is W3C Trace Context (`traceparent` header). Propagate on every HTTP call, gRPC call and queue message (put `traceparent` in message attributes). One service that drops it breaks every trace through it.
- **Auto-instrumentation first** (HTTP server and client, Postgres driver, Redis, fetch), then add manual spans only around meaningful internal steps (an external payment call, a heavy computation), not every function.
- **Span names are low cardinality**: `GET /users/:id`, `db.query users.select`, not the raw URL or SQL with values. Use semantic convention attribute names (`http.request.method`, `http.response.status_code`, `db.system`, `server.address`) so backends understand them.
- **Record errors on the span** (`span.recordException(err)`, set status `ERROR`), and put the `trace_id` into the log lines so logs and traces link.
- **Sampling**: at more than about 1000 traces per second, sample. Default to head sampling by trace id ratio (consistent, cheap, keeps whole traces). Tail sampling (keep all errors and slow traces) needs a collector and costs compute; add it when the head sampled data misses the incidents you care about.
- **Do not leak internals outward**: do not propagate internal baggage to third party APIs.
- Do not put PII or secrets in span attributes; the same rules as logs apply.

## 6. Alerting and SLOs

**A1. Every page must be urgent, actionable, and about real or imminent user pain.** Before adding a paging rule, answer (SRE book ch. 6): does it detect an otherwise undetected condition that is urgent, actionable and user visible? Will I ever ignore it as benign? Can I act on it now, or could it wait until morning? If the response is robotic, automate it instead of paging.

**A2. Page on symptoms, investigate with causes.** Page on "checkout error rate is burning the error budget", not on "CPU 85%" or "one pod restarted". Cause metrics go on dashboards. Exception: imminent, definite causes (disk will be full in 4 hours, zero redundancy left).

**A3. Define SLOs from the user's view before writing alerts.** SLI = good events / valid events (successful requests under a latency threshold, measured at the load balancer or client). SLO = target over a window (for example 99.9% over 30 days). Error budget = 1 minus SLO. 100% is never the target.

**A4. Alert on error budget burn rate, multiwindow** (SRE Workbook ch. 5). Starting numbers for a 30 day, 99.9% SLO:

| Severity | Budget consumed | Long window | Burn rate | Short window |
|---|---|---|---|---|
| Page | 2% | 1 hour | 14.4 | 5 minutes |
| Page | 5% | 6 hours | 6 | 30 minutes |
| Ticket | 10% | 3 days | 1 | 6 hours |

Fire only when both the long and the short window exceed the burn rate; the short window (1/12 of the long one) makes the alert reset quickly after recovery. Plain "error rate > X for 10 minutes" either pages on noise or misses slow burns; "for: 1h" durations miss bursty failures entirely.

**A5. Low traffic services** need synthetic traffic or longer windows; with 10 requests per hour one failure is a 10% error rate.

**A6. Every alert links to a runbook** with: what it means, how to confirm, first mitigation (usually: roll back the last change), who owns it.

**A7. Review paging load.** More than about 2 pages per on-call shift means the alerting is broken, not the people. Delete or demote alerts that never led to action.

**A8. Email alerts are dashboards in disguise.** Prefer a dashboard of ongoing sub-critical issues plus tickets.

## 7. Stack recipes

### Node (Express, Fastify, Hono)

```ts
import pino from "pino";
import { AsyncLocalStorage } from "node:async_hooks";
export const als = new AsyncLocalStorage<{ requestId: string }>();
export const logger = pino({
  level: process.env.LOG_LEVEL ?? "info",
  redact: ["req.headers.authorization", "req.headers.cookie", "*.password", "*.token"],
  mixin: () => ({ requestId: als.getStore()?.requestId }),
});
```

Fastify has pino built in (`logger: true`, `genReqId`). Use `pino-http` for Express. Instrument with `@opentelemetry/sdk-node` + `@opentelemetry/auto-instrumentations-node`, loaded before anything else (`node --import ./otel.js server.js`). Measure event loop delay with `perf_hooks.monitorEventLoopDelay()` and export p99.

### Rust (axum, tokio)

```rust
tracing_subscriber::fmt().json().with_env_filter(EnvFilter::from_default_env()).init();
let app = Router::new()
    .route("/users/:id", get(get_user))
    .layer(TraceLayer::new_for_http()) // tower-http: one span per request with method, route, status, latency
    .layer(SetRequestIdLayer::x_request_id(MakeRequestUuid))
    .layer(PropagateRequestIdLayer::x_request_id());
```

Use `#[tracing::instrument(skip_all, fields(...))]` and add only the fields you need; the default records every argument with `Debug`, which leaks secrets. Export to OTLP with `tracing-opentelemetry` + `opentelemetry-otlp`.

### React Native / web clients

- Crash reporter with breadcrumbs (navigation, network status), user id set to the internal id, never email.
- Send the request id from API error responses into the crash report so client and server events join.
- No `console.log` in production bundles (strip with `babel-plugin-transform-remove-console` or lint `no-console`); on RN `console.log` in hot paths costs frame time.

## 8. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| No console logging in server code | 0 hits outside scripts and tests | `rg -n 'console\.(log|info|debug)' src --glob '!**/*.test.*'`; ESLint `no-console: error` |
| No println in Rust services | 0 hits outside `main` usage and tests | `rg -n 'println!|eprintln!|dbg!' src`; clippy `print_stdout`, `dbg_macro` |
| JSON structured output | Logger configured with JSON | `rg -n 'pino\(|\.json\(\)' src` |
| Constant messages | No template literals as log message | `rg -n 'logger\.\w+\(`' src`; `rg -n '(info|warn|error)!\(\s*"[^"]*\{' src` then review |
| Request id everywhere | Middleware sets and returns it; logger mixin or span includes it | `rg -n 'x-request-id|requestId|traceparent' src`; curl a request and check the header and the log line |
| Canonical line on failure too | Emitted in finally/post-response hook | Integration test: trigger a 500 and assert one canonical line with status 500 |
| Redaction configured | Redact list covers auth headers, cookies, password, token | `rg -n 'redact' src`; test logs a fake request with `Authorization: Bearer x` and asserts the token is absent |
| No secrets in logs | 0 hits | `rg -n -i 'log.*(password|secret|token|authorization|apikey)' src`; scan a staging log sample: `rg -i 'bearer [a-z0-9]|sk_live_|-----BEGIN' logs.json` |
| `instrument` skips args | Every `#[instrument]` has `skip` or `skip_all` | `rg -n '#\[(tracing::)?instrument' src | rg -v 'skip'` returns 0 |
| No high cardinality labels | No metric label from ids, emails, urls | `rg -n 'labels?\(.*(user_?id|email|url|path)' src`; check series count in the metrics backend |
| Histograms for latency | Duration metrics are histograms | `rg -n 'Histogram|histogram' src` near each duration metric |
| Success latency separate | A success only timer or a status label used for alerting | Read alert rules |
| Queue age metric | Oldest message age exported for each queue | `rg -n -i 'age|oldest' src/queue*` |
| SLO alerts are burn rate | Page rules use multiwindow burn rate | Read alert rules for `14.4` / `6` style thresholds with two windows |
| Every alert has a runbook | Each rule has a runbook URL annotation | `rg -c 'runbook' alerts/` equals rule count |
| Trace context propagated | Outgoing HTTP and queue messages carry `traceparent` | Integration test asserts header on an outgoing mock; inspect a message's attributes |
