# API design: HTTP/JSON APIs that do not need a v2

Read when: adding or changing an HTTP endpoint, a public or internal API, a list endpoint, an error format, or anything a client depends on. For retries and limits see `rate-limits-retries-timeouts.md`; for webhooks see `webhooks-and-jobs.md`.

Sources: Google AIP (158, 180, 193), Microsoft Azure REST guidelines, Zalando RESTful guidelines, Stripe API docs and engineering blog, RFC 9457, RFC 9110. Full list in `sources/articles/backend-security-reading-list.md`.

## Contents

1. The contract mindset (what models get wrong)
2. Resources, paths, methods, status codes
3. Request and response bodies
4. Errors: RFC 9457 problem details
5. Pagination: cursor by default, from day one
6. Idempotency keys for POST
7. Concurrency: ETags and If-Match
8. Long running operations
9. Compatibility and versioning
10. IDs, time, money, numbers
11. Request IDs and tracing
12. Checks

## 1. The contract mindset

An API is a contract that outlives the code. Every field, status code, error code and default you ship becomes something a client depends on. The expensive mistakes are the ones that cannot be fixed without breaking someone:

- A list endpoint shipped without pagination. Adding it later is a breaking change, because old clients read page one and think it is everything (AIP-158, Microsoft).
- A bare JSON array as a top level response. It cannot grow a `next_cursor` field later (Zalando #110).
- A closed enum. Adding a value later breaks clients that switch on it exhaustively.
- Error messages that clients parse because there was no stable machine code.
- A boolean that later needs a third state (`verified: true` that becomes `status: "pending" | "verified" | "failed"`, Stripe's own example).

Default: design the response shape for the second version on day one. Rules below.

## 2. Resources, paths, methods, status codes

Rules:

- Paths are nouns, plural, kebab-case: `/v1/invoices/{invoice_id}/line-items`. No verbs in paths except for custom actions that are not CRUD, written as a sub-resource: `POST /v1/invoices/{id}/finalize`.
- Nest at most one level below the owning resource. Deeper than that, give the child its own top level collection with a filter: `GET /v1/line-items?invoice_id=...`.
- Method semantics are not optional:
  - `GET`, `HEAD`: no side effects. Never change state on GET (prefetchers, crawlers and CSRF via `<img>` all fire GETs).
  - `PUT`: full replace, idempotent.
  - `PATCH`: partial update with JSON Merge Patch (RFC 7396): absent field means "leave it", `null` means "clear it". Idempotent.
  - `DELETE`: idempotent. Deleting something already gone returns `204` (Microsoft) or `404`; pick one and document it. Default: `204`.
  - `POST`: create or action. Not idempotent unless you add an idempotency key (section 6).
- Status codes, the ones that matter:

| Code | Use for | Common mistake |
|---|---|---|
| 200 | success with body | returning 200 with `{"error": ...}` inside |
| 201 | created, with `Location` header | returning 200 |
| 202 | accepted, work continues async (section 8) | returning 200 before work is done |
| 204 | success, no body | sending a body with 204 |
| 400 | malformed request, failed validation | using 500 for bad input |
| 401 | not authenticated (no or bad credentials) | using 403 |
| 403 | authenticated but not allowed | leaking existence (see below) |
| 404 | not found, or not allowed and existence is secret | |
| 405 | method not allowed on this path | |
| 409 | conflict with current state (duplicate, idempotency key in use) | |
| 412 | `If-Match` precondition failed | |
| 413 | body too large | no body limit at all |
| 415 | unsupported `Content-Type` | parsing anything |
| 422 | well formed but semantically invalid | (400 is also fine; pick one per API) |
| 429 | rate limited, with `Retry-After` | 503 for per-client limits |
| 500 | bug | leaking a stack trace |
| 503 | overloaded or dependency down, with `Retry-After` | |

- Existence leaks: check permission before existence (AIP-193). If the caller may not know the object exists (another tenant's invoice), return `404`, not `403`.
- Reject unknown query parameters and unknown body fields with 400 on writes (Microsoft). Silently ignoring `{"emial": ...}` hides client bugs. Exception: clients must tolerate unknown fields in responses (tolerant reader, Zalando #108).
- Never accept credentials or tokens in the query string (`?api_key=`). They end up in access logs, browser history and `Referer` headers (OWASP REST, RFC 9700 for OAuth tokens).

## 3. Request and response bodies

- Top level of every response is a JSON object, never an array or a bare scalar.
- List responses: `{"data": [...], "next_cursor": "..."}`. One name for the items field across the whole API.
- One casing across the API. Default for JSON: `snake_case` (Zalando, Stripe) or `camelCase` (Microsoft, Google JSON). Pick one, write it down, lint it. Mixing is the defect.
- Absent and `null` mean the same thing in responses (Zalando #123); prefer omitting. Exception: Merge Patch requests, where `null` means delete.
- Never `null` for a boolean (use an enum if there is a third state) and never `null` for an empty list (use `[]`).
- Enums are open: document that new values may appear and clients must handle an unknown value. UPPER_SNAKE or lower_snake, one style.
- Do not return secrets on GET (Microsoft). A created API key is shown once in the POST response, then only its prefix and last four characters.
- Do not return fields the caller may not read. Build the response from an explicit allowlist or DTO, never by serializing the ORM row (`res.json(user)` ships `password_hash`).
- Do not bind request bodies straight onto models (mass assignment, see `../security/input-and-injection.md`).
- Limit body size at the edge of the server (for example 1 MB for JSON APIs, separate higher limit only on upload routes) and reject with 413.

```ts
// bad: ORM row straight out, and straight in
app.get("/users/:id", async (req, res) => res.json(await db.user.findUnique({ where: { id: req.params.id } })));
app.patch("/users/:id", async (req, res) => res.json(await db.user.update({ where: { id: req.params.id }, data: req.body })));

// good: explicit input schema, explicit output shape, scoped query
const UserPatch = z.object({ display_name: z.string().min(1).max(80).optional() }).strict();
app.patch("/users/me", async (req, res) => {
  const input = UserPatch.parse(req.body);
  const u = await db.user.update({ where: { id: req.session.userId }, data: input });
  res.json({ id: u.id, display_name: u.displayName });
});
```

## 4. Errors: RFC 9457 problem details

Default error format for new HTTP APIs: `application/problem+json` (RFC 9457, which obsoletes RFC 7807).

```http
HTTP/1.1 422 Unprocessable Content
Content-Type: application/problem+json

{
  "type": "https://api.example.com/problems/validation-failed",
  "title": "Request validation failed",
  "status": 422,
  "detail": "2 fields are invalid.",
  "instance": "/v1/orders/req_8f2k1",
  "code": "VALIDATION_FAILED",
  "request_id": "req_8f2k1",
  "errors": [
    { "pointer": "#/items/0/quantity", "detail": "must be a positive integer" },
    { "pointer": "#/currency", "detail": "must be one of EUR, USD" }
  ]
}
```

Rules:

- `type` is the stable identifier of the problem kind. `title` is fixed per type. `detail` is for humans and is never parsed by clients (RFC 9457).
- Add a stable machine code extension (`code`, UPPER_SNAKE, at most 63 chars, AIP-193 style) and treat it as API surface: never rename it, never reuse it for a different error. Clients switch on `code`, not on `detail`.
- Field errors go in an `errors` array with a JSON Pointer to the offending field, so a form can highlight it.
- `status` in the body must equal the HTTP status.
- Every error carries the request ID, so a support ticket can be traced.
- Never put stack traces, SQL, internal hostnames, file paths or library error strings in any field (RFC 9457 security section, OWASP REST). Log them server side with the request ID.
- 5xx responses are generic: `"title": "Internal error"`. The detail lives in logs.
- One error format for the whole API, including 404 from the router, 413 from the body parser and 401 from the auth middleware. Framework default HTML error pages on an API are a defect.

Existing API with a different envelope (`{"error": {"code", "message"}}`, Microsoft style): keep it, consistency beats the standard. Do not mix two formats.

## 5. Pagination: cursor by default, from day one

Every list endpoint is paginated from its first release, with a finite default page size (AIP-158: adding it later breaks clients).

Defaults:

- Parameters: `limit` (or `page_size`) and `cursor` (or `page_token`). Response: `next_cursor`, absent or empty on the last page. The only end-of-list signal is an empty `next_cursor`, never "fewer items than requested" (AIP-158 allows short pages).
- Default `limit` 50, maximum 100 to 1000 depending on item size. A `limit` above the max is clamped, not rejected. A negative or non-integer `limit` is a 400.
- The cursor is opaque. Encode it (base64url of a JSON blob or of the last sort key), and sign or encrypt it if it would reveal anything. Clients must not build cursors. Base64 is not obfuscation (AIP-158).
- A cursor never grants access. Authorization is checked on every page request (AIP-158).
- If filters or sort change between pages, reject the old cursor with 400 (AIP-158). Store a hash of the filter set inside the cursor and compare.
- Cursors may expire. Three days is a reasonable horizon (AIP-158).
- No `total_count` by default (Zalando #254, Microsoft). `COUNT(*)` over a large filtered set is a full scan on every page load. Offer it only as an explicitly requested, documented estimate.

Use keyset (seek) pagination in SQL, not OFFSET. OFFSET reads and discards every skipped row, so page 1000 costs 1000 pages of work, and inserts between requests shift rows so users see duplicates or miss items (use-the-index-luke.com/no-offset).

```sql
-- bad: cost grows with page number, rows drift on insert
SELECT * FROM orders WHERE org_id = $1 ORDER BY created_at DESC LIMIT 50 OFFSET 5000;

-- good: keyset on a unique, indexed sort key with a tie breaker
-- index: CREATE INDEX ON orders (org_id, created_at DESC, id DESC);
SELECT id, created_at, total_cents
FROM orders
WHERE org_id = $1
  AND (created_at, id) < ($2, $3)        -- values decoded from the cursor
ORDER BY created_at DESC, id DESC
LIMIT 51;                                  -- fetch limit + 1 to know if there is a next page
```

Rules for keyset:

- The sort key must be unique. `created_at` alone is not: two rows with the same timestamp get skipped or duplicated. Always add the primary key as a tie breaker.
- The index must match the `ORDER BY` exactly, including direction, and start with the equality filter columns.
- Fetch `limit + 1` rows; if you got the extra one, there is a next page and the cursor is the last row you return.
- OFFSET is acceptable only for small bounded admin tables or when the UI truly needs "jump to page 37". Cap the offset (for example 10,000).

## 6. Idempotency keys for POST

Any POST that creates something or moves money must be safely retryable, because the client cannot tell "request lost" from "response lost" after a timeout.

Contract (Stripe, IETF draft `Idempotency-Key` header):

- Client sends `Idempotency-Key: <uuid v4>` generated once per logical operation and reused on every retry of it. Never derived from user data (Stripe: no emails as keys). Max 255 chars.
- Server stores, per (caller, key): a fingerprint of the request (method, path, body hash), a lock, and once finished the response status and body.
- Same key, same fingerprint, finished: replay the stored response, including stored errors (Stripe v1 replays even 500s).
- Same key, different fingerprint: 409 or 422. The client has a bug.
- Same key, request still running: 409 with `Retry-After: 1`.
- Validation failures before execution starts are not stored, so the client can fix and retry (Stripe).
- Keep keys at least 24 hours (Stripe); brandur suggests up to 72 hours so a bug over a weekend can be fixed and the requests completed.
- Calls to third parties inside the handler get their own idempotency key derived from yours (for example `${key}:charge`), so a crash between your DB write and their response does not double charge (brandur).

```sql
CREATE TABLE idempotency_keys (
  id              bigserial PRIMARY KEY,
  user_id         bigint      NOT NULL,
  key             text        NOT NULL CHECK (char_length(key) <= 255),
  request_hash    bytea       NOT NULL,
  locked_at       timestamptz,
  response_code   int,
  response_body   jsonb,
  created_at      timestamptz NOT NULL DEFAULT now(),
  UNIQUE (user_id, key)
);
```

Flow: `INSERT ... ON CONFLICT (user_id, key) DO NOTHING RETURNING *`. If no row came back, read the existing one and apply the rules above. Do the business write and the `response_code/response_body` update in the same transaction as far as possible. Anything outside the database (a charge, an email) is a "foreign mutation": either pass an idempotency key to it, or put it in a job enqueued in the same transaction (outbox, `webhooks-and-jobs.md`).

Cheaper alternative when it fits: a natural unique constraint. `UNIQUE (org_id, external_order_ref)` plus `ON CONFLICT DO NOTHING` makes "create order" idempotent with no extra table (Zalando #231 "secondary key").

## 7. Concurrency: ETags and If-Match

Lost updates happen when two clients read version 3 and both write. Default for any resource edited by more than one person or device:

- Every resource has a `version` integer (or `updated_at` with sub-second precision; ETags are better than timestamps because two writes can land in the same second, Microsoft).
- GET returns `ETag: "v7"`. PATCH/PUT with `If-Match: "v7"` updates `WHERE id = $1 AND version = 7`, increments version, and returns 412 if zero rows changed.
- `If-None-Match: *` on PUT means "create only if absent", 412 otherwise.
- GET with `If-None-Match` matching returns 304 with no body: free bandwidth savings for polling clients.

## 8. Long running operations

If p99 latency of an operation is over about 1 second, or it calls slow third parties, make it async (Microsoft uses the 1 s p99 threshold):

- Return 202 with `Location` (or `Operation-Location`) pointing to a status resource, and `Retry-After` in seconds.
- Status resource: `{"id", "status": "queued" | "running" | "succeeded" | "failed" | "canceled", "error"?, "result_url"?}`. Keep it at least 24 hours after completion.
- Do not hold an HTTP request open for minutes waiting on work. Load balancers cut it (often at 60 s), the client retries, and you do the work twice.

## 9. Compatibility and versioning

What is a breaking change (AIP-180, Stripe, Microsoft). Never ship these inside a version:

- Removing or renaming a field, endpoint, enum value, query parameter or error code.
- Changing a field's type, even if the wire format still parses (int32 to int64 breaks JS clients above 2^53).
- Adding a required request field, or making an optional one required.
- Changing a default value, or starting to emit a field that used to be omitted at its default.
- Making validation stricter (a name that used to be accepted now fails).
- Raising a documented maximum length (clients sized buffers or DB columns for it).
- Changing the format of a value (IDs become UUIDs, timestamps change precision).
- Adding pagination to an unpaginated list, or lowering the default page size.
- Changing the meaning of a status code or error code.

Safe changes: new endpoint, new optional request field, new response field, new enum value (only if enums were documented as open), new error code for a new situation, looser validation.

Versioning strategy, default: avoid versions by only making additive changes. When a break is unavoidable:

- Public API with many integrators: date based versions pinned per account at first use, overridable per request by header (`Stripe-Version: 2026-10-01`). Old versions are served by transforming the current response backwards through small "version change" modules, so old versions do not fork the core code (Stripe).
- Simpler APIs: a major version in the path (`/v1/`, `/v2/`) is acceptable and easiest to route. Zalando and Microsoft forbid it, Google and Stripe use it; pick one style and keep it.
- Internal API with one client you deploy together (your own web app): no versions. Deploy server changes that accept both old and new shapes first, migrate the client, then remove the old shape (expand and contract).
- Mobile apps are not "one client you deploy together": old app versions live for years. Treat a mobile backend as a public API.
- Announce deprecation with the `Deprecation` and `Sunset` headers (RFC 9745 for Deprecation, RFC 8594 for Sunset) and a date, and log which callers still use the old shape before removing it.

## 10. IDs, time, money, numbers

- IDs are strings in JSON, always (Zalando). A 64-bit integer ID loses precision in JavaScript above 2^53 (9,007,199,254,740,991). Microsoft caps JSON integers at that range.
- Public IDs are not sequential database integers. Sequential IDs leak volume ("order 10234") and invite enumeration. Use UUIDv7 (time ordered, index friendly) or random IDs with a type prefix: `inv_3Kq9...`, `cus_...`, `sk_live_...` (Stripe). Prefixes make wrong-type bugs obvious in logs and make secrets greppable for leak scanners. Unguessable IDs are not access control (OWASP); still check ownership.
- Time: RFC 3339 in UTC with `Z`: `"2026-10-30T14:05:09.123Z"`. Name fields `*_at` (`created_at`) for instants, plain dates as `"2026-10-30"` named `*_on` or `*_date`. Never epoch seconds in one place and ISO in another.
- Durations: unit in the name (`timeout_seconds`, `ttl_ms`) or ISO 8601 (`"PT15M"`), one style.
- Money: integer minor units plus ISO 4217 currency (`{"amount": 1999, "currency": "EUR"}`, Stripe), or a decimal string (`{"amount": "19.99", "currency": "EUR"}`, Zalando). Never a float. Watch currencies with 0 or 3 minor digits (JPY, KWD).
- Country ISO 3166-1 alpha-2, language BCP 47.

## 11. Request IDs and tracing

- Every response carries `X-Request-Id` (or `Request-Id`). Accept an incoming one from trusted proxies only; otherwise generate it.
- Propagate it (or W3C `traceparent`) on every outgoing call and job, and put it in every log line and every error body.
- Request IDs are not secrets but are not authorization either.

## 12. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| Every list endpoint paginated | each `GET` returning a collection takes a limit and returns a cursor; default limit is finite | grep list routes: `rg -n "findMany\|SELECT .* FROM" --type ts` near routes and confirm `take`/`LIMIT` bound by a clamped param |
| No OFFSET on large tables | no `OFFSET`/`skip:` on user-facing lists over growing tables | `rg -n "OFFSET\|\.skip\(\|skip:" ` and review each |
| Keyset has tie breaker | every cursor `ORDER BY` ends with the unique id | read the query; `ORDER BY created_at` alone fails |
| Top level JSON is an object | no `res.json([...])`/`Json(vec)` at the top level | `rg -n "res\.json\(\s*\[\|Json\(vec!\|Json\(items\)"` |
| One error format | 404, 401, 413 and validation errors all return the same envelope with a `code` | curl a missing route, an unauthenticated route and an oversized body; compare bodies |
| No internals in errors | no stack, SQL or library message in any error body | `rg -n "err\.(stack\|message)" ` in response paths; `rg -n "format!\(\"\{e\}\|e\.to_string\(\)" ` in handlers |
| Responses are DTOs | no ORM entity serialized directly | `rg -n "res\.json\((user\|row\|record\|result)\)"`; review for `password`, `hash`, `token` fields |
| No secrets in URLs | no `api_key`, `token`, `password` query params | `rg -n "query\.(token\|api_?key\|password)\|searchParams\.get\(\"(token\|key)" ` |
| POST creates are idempotent | money moving or create POSTs accept `Idempotency-Key` or have a natural unique key with `ON CONFLICT` | read handler; send the same request twice, count rows |
| Lost update protection | multi-writer resources compare a version on update | `rg -n "If-Match\|version = " `; update query has a version predicate |
| IDs are strings, not sequential | public IDs are prefixed random or UUIDv7 strings | inspect a response; `rg -n "serial\|autoIncrement" ` used as public id |
| Money is not float | no `float`/`double`/`number` money columns or fields | `rg -n "price.*(float\|double\|real)\|amount.*Float\|f64" ` |
| Breaking change review | PR diff of the OpenAPI spec has no removed/renamed fields, no new required fields | `npx oasdiff breaking old.yaml new.yaml` (or `openapi-diff`) in CI |
