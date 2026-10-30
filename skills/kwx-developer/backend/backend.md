# Backend: master rules and map

Read this first for any server side work: an endpoint, a handler, a job, a webhook, a database call from a request, a call to a third party, auth. Then open the one topic file the task needs. Security rules that are never cut live in `../security/security.md`; read it too when the change touches auth, user input, files, URLs, secrets or dependencies.

## Contents

1. The rules that hold on every backend change
2. Map: which file to read
3. Adding an endpoint: the order of work
4. Errors and logging in handlers
5. Checks

## 1. The rules that hold on every backend change

These are the mistakes that models make by default and that cause real outages or breaches. Each has a check in section 5.

1. Authorize every request on the server, per object. Scope every query by the owner or tenant taken from the session, never from the request. Not found and not yours return the same 404. (`auth.md` section 11)
2. Validate input at the trust boundary with a schema that rejects unknown fields, and bind only allowlisted fields to models. (`../security/input-and-injection.md`)
3. Every remote call has a timeout: HTTP, database statement, Redis, queue, SDK. Library defaults are infinite or minutes. (`rate-limits-retries-timeouts.md` section 2)
4. Retries are bounded (at most 3 attempts on a user path), use exponential backoff with full jitter, retry only retryable failures, happen at one layer, and never repeat a non-idempotent call without an idempotency key. (`rate-limits-retries-timeouts.md` section 4)
5. Every list endpoint is paginated from its first release with a finite default and a clamped max, using keyset (cursor) pagination on growing tables. (`api-design.md` section 5)
6. Every POST that creates or moves money is safe to retry: an `Idempotency-Key` or a natural unique key with `ON CONFLICT`. (`api-design.md` section 6)
7. Abusable and expensive endpoints are rate limited with the right key: login and reset by account and IP, API by user or key, LLM and exports by concurrency and quota. 429 carries `Retry-After`. (`rate-limits-retries-timeouts.md` section 6)
8. No side effect after a commit without an outbox or transactional enqueue; no slow work inside the request. Webhooks are verified on the raw body, deduped by event ID, acknowledged fast, and processed in a job. (`webhooks-and-jobs.md`)
9. Jobs and webhook handlers are idempotent and order independent; retries are bounded and end in an alerted dead letter state. (`webhooks-and-jobs.md` section 5)
10. Errors use one envelope with a stable machine code and a request ID, and never contain stack traces, SQL or internal hostnames. (`api-design.md` section 4)
11. Responses are built from explicit DTOs, never by serializing ORM rows; authenticated responses send `Cache-Control: no-store` or `private`. (`api-design.md` section 3, `caching.md` section 2)
12. Every cache entry has a TTL and a versioned, tenant-scoped key, and every write path invalidates it after commit. (`caching.md`)
13. Breaking changes to a shipped API are not made in place: additive only, or a new version. (`api-design.md` section 9)
14. Clients and pools are created once per process, not per request.

## 2. Map: which file to read

| File | What is in it | Read when |
|---|---|---|
| `backend/api-design.md` | paths, methods, status codes, RFC 9457 errors, cursor pagination with SQL, idempotency keys, ETags, async operations, versioning and breaking changes, IDs, time, money | adding or changing any endpoint or response shape |
| `backend/rate-limits-retries-timeouts.md` | timeout numbers per client library, deadline propagation, retry rules and full jitter code, retry budgets, circuit breakers, server rate limit keys and algorithms, 429 format, load shedding, client side debounce, dedupe, cancel, SWR, batching | any outbound call, any retry, any public or expensive endpoint, any data fetching UI |
| `backend/caching.md` | Cache-Control defaults per response type, CDN leak risks, cache-aside code, TTL and key rules, invalidation order and races, stampedes, client query caches | adding any cache or cache header, stale data bugs |
| `backend/webhooks-and-jobs.md` | webhook receiver template, Standard Webhooks for sending, outbox, job rules, Postgres SKIP LOCKED queue, DLQ, cron | webhooks in or out, background work, cron, queues |
| `backend/auth.md` | sessions vs JWT, cookies, Argon2id parameters, NIST password rules, login enumeration, reset tokens, passkeys, OAuth 2.1, API keys, object level authorization, multi-tenancy, Supabase RLS | anything about identity, permissions, tenants |
| `security/security.md` | the security rules that are never cut, and the security map | every change that touches input, auth, files, URLs, secrets, dependencies |

## 3. Adding an endpoint: the order of work

1. Write the contract first: path, method, request schema, response DTO, error codes, status codes. Paginated if it returns a list. Idempotency if it creates.
2. Decide who may call it and on which objects. Write the deny test (user A on user B's object) before the handler.
3. Handler order: authenticate (middleware) -> rate limit -> parse and validate body against the schema (reject unknown fields, size limit) -> authorize on the specific object -> do the work in a transaction -> enqueue side effects in the same transaction -> build the response DTO.
4. Every outbound call inside it gets a timeout that fits inside the request budget.
5. Anything slower than a few hundred ms or dependent on a third party moves to a job; the endpoint returns 202 or the created resource.
6. Add the error cases to the API's error envelope; check that a thrown exception becomes a generic 500 with a request ID.
7. Run the checks in section 5 on the diff.

## 4. Errors and logging in handlers

- One error handler at the top of the stack maps known error types to problem responses and everything else to a generic 500. Handlers throw typed errors (`NotFound`, `Forbidden`, `Conflict`, `ValidationFailed`); they do not build HTTP responses for errors ad hoc.
- In Rust, handlers return `Result<_, ApiError>` with `impl IntoResponse for ApiError`; no `unwrap()` or `expect()` on anything derived from input or I/O in a request path (a panic drops the connection and, in some setups, the worker).
- In Node, an unhandled promise rejection must not crash the process silently or leave the request hanging; frameworks that do not catch async errors (Express 4) need a wrapper or Express 5.
- Structured logs (JSON), one line per request with: request ID, route, status, duration, user ID or tenant ID (not email), and error code. Log the full error with stack on the server for 5xx.
- Never log passwords, tokens, session IDs, API keys, full card numbers, or request bodies of auth routes (OWASP Logging). Redact by key name in the logger config (`pino` `redact`, `tracing` field filters).
- Log security events: login success and failure, lockouts, password and MFA changes, permission denied, validation failures on auth routes, admin actions (OWASP Logging, Top 10 2025 A09).

## 5. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| Object level authorization | queries by ID include an owner or tenant predicate from the session | `rg -n "where: \{ id: (req\|params\|body)" ` and `rg -n "WHERE id = \\$1\"" `; read each hit |
| Schema validation on every write route | every POST/PUT/PATCH parses the body with a schema in strict mode | `rg -n "req\.body" ` hits that are not inside `.parse(`/`.safeParse(`; Rust: handlers take `Json<T>` with `#[serde(deny_unknown_fields)]` |
| Timeouts | no outbound call without a timeout | see `rate-limits-retries-timeouts.md` checks |
| Pagination | list endpoints bound by a clamped limit | see `api-design.md` checks |
| Rate limits on auth and expensive routes | limiter middleware on login, signup, reset, OTP, LLM, export | read route registration |
| No panics in request paths (Rust) | no `unwrap()`/`expect()` on request or I/O data in handlers | `rg -n "\.unwrap\(\)\|\.expect\(" src/routes src/handlers` |
| Central error handler | one error to response mapping; no `res.status(500).json(err)` | `rg -n "status\(500\)\.(json\|send)\((e\|err)" ` |
| No secrets in logs | logger redacts auth headers, cookies, password fields | read logger config; `rg -n "console\.log\(.*(req\.body\|headers\|token\|password)" ` |
| No slow work inline | no email, PDF, third party sync in request handlers | `rg -n "sendMail\|sendEmail\|puppeteer\|resend\.emails" ` in route files |
| Tests for deny paths | each resource has a cross-user access test | `rg -n "403\|404" tests/ ` near "other user" fixtures |
