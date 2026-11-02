# API testing at the HTTP level

How to test an HTTP API the way its clients use it: send real requests to the real router, in process, and assert on status, headers and body. This file covers the harness for Node, Next.js and axum, then the case lists a tester must cover for every endpoint: error statuses, validation, pagination, idempotency, authentication and the basic authorization matrix. Deep attacker style testing belongs to a future kwx-hacker skill; the tester runs the basic matrix and reports anything suspicious.

## Contents

1. Harnesses
2. Designing the case list for one endpoint
3. Status codes and error bodies
4. Validation
5. Pagination
6. Idempotency
7. Authentication
8. The authorization matrix
9. Rate limits and payload limits
10. Checks

## 1. Harnesses

Rule: **test the router in process, with a real request.** No port, no network, real middleware. Evidence: moderate (supertest, axum and Next.js testing docs).

When a test needs a real listening server (vitest over HTTP, node:test), take the port from PORT or E2E_PORT, else port 0 (`../web/playwright.md` section 14); never a literal port or range.

### Node (Express, Fastify, plain http): supertest

```js
import request from 'supertest';
import { app } from '../src/app';

const res = await request(app)
  .post('/api/todos')
  .set('Authorization', `Bearer ${aliceToken}`)
  .send({ title: 'Buy milk' });
expect(res.status).toBe(201);
expect(res.body).toMatchObject({ title: 'Buy milk' });
expect(res.headers['content-type']).toMatch(/application\/json/);
```

Fastify also offers `app.inject({ method, url, payload })`, which needs no extra package.

### Next.js App Router route handlers

A route handler is an exported function that takes a `Request` and returns a `Response`. The cheapest test calls it directly:

```ts
import { GET } from '@/app/api/todos/[id]/route';

it('returns 404 for an unknown id', async () => {
  const res = await GET(new Request('http://test/api/todos/999'), {
    params: Promise.resolve({ id: '999' }), // Next 15+: params is a Promise
  });
  expect(res.status).toBe(404);
  expect(await res.json()).toEqual({ error: 'not_found' });
});
```

When the handler uses `cookies()`, `headers()` or other request scoped Next APIs, use `next-test-api-route-handler` (App Router support starts at `next@14.0.4`; it must be the first import in the test file):

```ts
import { testApiHandler } from 'next-test-api-route-handler'; // must be first
import * as appHandler from '@/app/api/todos/route';

await testApiHandler({
  appHandler,
  async test({ fetch }) {
    const res = await fetch({ method: 'POST', body: JSON.stringify({ title: '' }) });
    expect(res.status).toBe(422);
  },
});
```

Server Actions are not HTTP endpoints you can call this way. Extract the logic into a plain function and test that; cover the wiring with one end to end test.

### axum: `tower::ServiceExt::oneshot`

Verified 2026-10-31 with axum 0.8.9, tower 0.5.3, http-body-util 0.1.5:

```rust
use axum::{body::Body, http::{Request, StatusCode}};
use http_body_util::BodyExt;
use tower::ServiceExt; // brings `oneshot`

async fn get(uri: &str) -> (StatusCode, String) {
    let res = my_service::app()
        .oneshot(Request::builder().uri(uri).body(Body::empty()).unwrap())
        .await
        .unwrap();
    let status = res.status();
    let body = res.into_body().collect().await.unwrap().to_bytes();
    (status, String::from_utf8(body.to_vec()).unwrap())
}

#[tokio::test]
async fn every_error_status() {
    assert_eq!(get("/items/abc").await.0, StatusCode::BAD_REQUEST);
    assert_eq!(get("/items/0").await.0, StatusCode::NOT_FOUND);
    assert_eq!(get("/nope").await.0, StatusCode::NOT_FOUND);
}
```

`oneshot` consumes the router; build a fresh `app()` per request (cheap) or clone it. Build `app()` from a function that takes its state (database pool, clock, config) so tests can pass test versions.

### Auth in tests

- Create real test users and real tokens through the same code path production uses (sign up endpoint, `supabase.auth.admin.createUser`, a test helper that signs a JWT with the test secret). Do not stub the auth middleware away; then the matrix tests nothing.
- Keep a helper per role: `asAlice()`, `asBob()`, `asAdmin()`, `anonymous()`, `withExpiredToken()`.

## 2. Designing the case list for one endpoint

Write the list from the spec before reading the handler. For each endpoint, fill this table; every cell is at least one test.

| Dimension | Cases |
|---|---|
| Happy path | minimal valid request; full valid request; response body shape and headers |
| Validation | each required field missing; each field wrong type; each boundary (min, min minus 1, max, max plus 1); empty string vs null vs absent; unknown fields; unicode, emoji, RTL text, very long strings |
| Auth | no token; malformed token; expired token; token for a deleted user; wrong audience or issuer if you use JWTs |
| Authorization | owner; another user; another tenant; wrong role; anonymous (section 8) |
| State | resource missing (404); resource already exists (409); resource in a state that forbids the action (409 or 422) |
| Concurrency | two identical requests at once; update with a stale version (412 or 409 if you use ETags or version columns) |
| Idempotency | same idempotency key twice; same key with a different body; concurrent same key (section 6) |
| Lists | empty list; one page; many pages; page size max and max plus 1; invalid cursor (section 5) |
| Limits | body over the size limit (413); too many requests (429 with `Retry-After`) |
| Dependencies | database down or slow; third party returns 500, times out, returns malformed JSON |

Techniques that keep the list small but strong (evidence: strong, classic test design, ISTQB syllabus and Kaner "Lessons Learned in Software Testing"):

- **Equivalence classes:** one case per class of input that the spec treats the same way.
- **Boundary values:** for every limit, test at the limit and one step past it on both sides.
- **Decision tables:** when the result depends on several conditions (role x resource state x plan), list the combinations and test each distinct outcome.

## 3. Status codes and error bodies

Rules:

1. **Assert the status and the body together.** `expect(res.status).toBe(422)` alone passes when the server returns 422 for the wrong reason. Assert the error code and the field: `expect(res.body).toEqual({ error: 'validation', field: 'title', reason: 'too_long' })`. Evidence: moderate.
2. **Check the error body shape is the same for every endpoint.** If the API uses RFC 9457 problem details, every 4xx and 5xx has `type`, `title`, `status`. One table driven test over all endpoints catches drift. Evidence: moderate.
3. **5xx never leaks internals.** Force an internal error (a fake dependency that throws) and assert the body has no stack trace, SQL text, file path or library version. Evidence: moderate (OWASP API8 Security Misconfiguration).
4. **Know the semantic differences and test them:**

| Situation | Usual code | Test |
|---|---|---|
| Malformed JSON | 400 | send `{"title":` |
| Valid JSON, fails validation | 422 (or 400 if the API documents it) | each validation rule |
| No or invalid credentials | 401 with `WWW-Authenticate` | missing, malformed, expired token |
| Authenticated, not allowed | 403, or 404 to hide existence | section 8 |
| Unknown route or id | 404 | |
| Wrong method | 405 with `Allow` header | `DELETE` on a read only route |
| Duplicate create, version conflict | 409 | |
| Precondition failed (`If-Match`) | 412 | stale ETag |
| Body too large | 413 | |
| Unsupported `Content-Type` | 415 | send `text/plain` |
| Rate limited | 429 with `Retry-After` | |

Whatever the API chooses, the choice must match the spec and be consistent. A mismatch between spec and code is a bug report, not a reason to change the test (kwx-developer `~/.claude/skills/kwx-developer/ai-agents/tests-and-honesty.md`).

## 4. Validation

- Validation must run on the server even when the client validates. Send requests that the UI would never send: extra fields, wrong types, negative quantities, arrays where objects are expected.
- **Mass assignment:** send fields the client must not set (`role: "admin"`, `user_id` of another user, `price`, `is_verified`) and assert they are ignored or rejected, and that the stored row did not change. This is OWASP API3:2023 Broken Object Property Level Authorization. Evidence: strong.
- **Response over-exposure:** assert that responses do not include fields the caller should not see (password hash, other users' emails, internal flags). Use an exact `toEqual` on the body or a snapshot with an allow list, not `toMatchObject`, which ignores extra fields.
- **Strings:** empty, whitespace only, leading and trailing spaces, 1 char, max length, max plus 1, a 1 MB string, NUL byte, combining characters (length in graphemes vs bytes), SQL and HTML special characters (expect them stored and returned literally, not executed).
- **Numbers:** 0, negative, max int, max plus 1, float where int expected, `NaN` and `Infinity` as strings, numbers as strings.
- **Dates:** invalid date, Feb 29 on a non leap year, time zone offsets, far past and far future, DST transitions if the logic is local time.
- Use a property test to throw generated invalid input at the validator and assert it never returns 500. Schemathesis does this from the OpenAPI file (`contract-and-schema-testing.md`).

## 5. Pagination

Cases for every list endpoint:

| Case | Expected |
|---|---|
| Empty collection | 200, empty array, no next cursor |
| Exactly one page | no next cursor |
| Page size = max allowed | accepted |
| Page size = max + 1, 0, negative, not a number | 400/422 or clamped, as the spec says |
| No page size | documented default |
| Walk all pages | every item exactly once, in the documented order, total equals the count in the database |
| Insert and delete rows between page requests | with keyset (cursor) pagination: no item seen twice and no item skipped among those that existed throughout. With `OFFSET`, this test shows duplicates and gaps; report it if the spec promises stable paging |
| Invalid, tampered or expired cursor | 400, not 500 |
| Cursor from another user or another filter | 400 or an empty page, never another user's rows |
| Ties in the sort column | stable order (sort key includes a unique column) |

Write the "walk all pages" test as a loop in a helper, then assert the collected ids equal the ids you inserted. That is test logic, but it lives in one reviewed helper, not in each test.

## 6. Idempotency

Applies to any endpoint that creates something or moves money, and to every webhook handler.

What the reference behaviours say:

- Stripe (API v1): the first response for a key is saved once execution begins, and retries with the same key return the saved response, including 500 errors; keys can be pruned after at least 24 hours; reusing a key with different parameters returns an error. Evidence: moderate (Stripe docs).
- IETF draft `draft-ietf-httpapi-idempotency-key-header-08` (October 2026): 400 when a required key is missing, 422 when a key is reused with a different payload, 409 when a retry arrives while the first request is still processing. Evidence: moderate (standards draft, not yet an RFC).

Cases:

| Case | Expected |
|---|---|
| Same key, same body, sequential | second call returns the same status and body; one row in the database; one charge, one email |
| Same key, different body | 422 (or the documented error); nothing changed |
| Same key, sent twice concurrently | one succeeds, the other gets 409 or waits and returns the same result; never two rows |
| Missing key where required | 400 |
| First call failed with 500 midway | retry with the same key does not create a half duplicate; check the rows |
| Key reused by another user | treated as a different key, or rejected; never returns the first user's response |
| After the expiry window (move time, do not sleep) | documented behaviour |

Concurrent case in Vitest:

```ts
const send = () => request(app).post('/api/payments')
  .set('Authorization', asAlice()).set('Idempotency-Key', 'k-123').send({ amount: 500 });
const [a, b] = await Promise.all([send(), send()]);
expect([a.status, b.status].sort()).toEqual([201, 409]); // or both 201 with equal bodies, per spec
expect(await countPayments(aliceId)).toBe(1);
```

The database assertion is the real test. The status codes only show the contract.

## 7. Authentication

| Case | Expected |
|---|---|
| No `Authorization` header | 401 |
| `Bearer ` with empty token, garbage, wrong scheme (`Basic`) | 401 |
| Token signed with another key | 401 |
| `alg: none` JWT | 401 |
| Expired token (sign one with `exp` in the past, do not wait) | 401 |
| Token valid but user deleted or disabled | 401 or 403 per spec |
| Token for another environment (audience or issuer mismatch) | 401 |
| Logout then reuse the session or refresh token | 401 |
| Password reset token used twice | second use rejected |

These are the basic cases. Token forgery research, timing attacks and session fixation chains go to kwx-hacker.

Every login, password and admin endpoint also gets a limit test, a lockout abuse test and a spoofed address test (section 9).

## 8. The authorization matrix

Broken Object Level Authorization (BOLA, also called IDOR) is API1 in the OWASP API Security Top 10 2023, and OWASP's prevention list says to write tests for the authorization mechanism and not deploy changes that make them fail. Evidence: strong.

Build the matrix per resource: rows are actors, columns are operations, each cell states the expected status.

| Actor | GET one | LIST | CREATE | UPDATE | DELETE |
|---|---|---|---|---|---|
| Owner | 200 | sees own | 201 | 200 | 204 |
| Other user, same tenant | 404 (or 403) | does not see it | n/a | 404, row unchanged | 404, row still there |
| User in another tenant | 404 | does not see it | cannot create in tenant (403) | 404 | 404 |
| Wrong role (viewer tries admin action) | per spec | per spec | 403 | 403 | 403 |
| Anonymous | 401 | 401 | 401 | 401 | 401 |
| Expired token | 401 | 401 | 401 | 401 | 401 |

Rules:

1. **Every denied write asserts the stored state.** Read the row back with an admin connection and compare. A 404 with a changed row is the worst bug in the table. Evidence: strong.
2. **LIST is part of the matrix.** Seed rows for two users and assert the list for one contains none of the other's ids. Filters and search endpoints too (`?user_id=<other>` must not work). Evidence: strong.
3. **Test nested and indirect paths.** `/projects/:pid/tasks/:tid` with a task from another project; `/me/orders?id=` with another user's order id; bulk endpoints with a mix of own and foreign ids; export and download endpoints. Evidence: moderate.
4. **Test function level authorization (OWASP API5).** Call admin endpoints as a normal user by guessing the route (`/admin/users`, `PATCH /users/:id/role`). Evidence: strong.
5. **Generate the matrix from a table, not by copy paste.** One `it.each` per resource keeps it readable and makes a missing cell visible.

```ts
const actors = { owner: asAlice, other: asBob, anon: () => undefined, expired: withExpiredToken };
const cases = [
  ['owner',   'GET',    200], ['other', 'GET',    404], ['anon', 'GET',    401], ['expired', 'GET',    401],
  ['owner',   'PATCH',  200], ['other', 'PATCH',  404], ['anon', 'PATCH',  401], ['expired', 'PATCH',  401],
  ['owner',   'DELETE', 204], ['other', 'DELETE', 404], ['anon', 'DELETE', 401], ['expired', 'DELETE', 401],
] as const;

it.each(cases)('%s %s /todos/:id -> %i', async (actor, method, status) => {
  const todo = await seedTodo({ owner: aliceId, title: 'original' });
  const token = actors[actor]();
  let req = request(app)[method.toLowerCase()](`/api/todos/${todo.id}`);
  if (token) req = req.set('Authorization', token);
  if (method === 'PATCH') req = req.send({ title: 'changed' });
  expect((await req).status).toBe(status);
  if (actor !== 'owner') expect(await adminGetTodo(todo.id)).toMatchObject({ title: 'original' });
});
```

For Supabase, run the same matrix twice: once in SQL with pgTAP as `authenticated` and `anon` (`database-testing.md`), once through `supabase-js` with two signed in users. RLS is the authorization layer there, so it is the code under test.

Schemathesis can also run an `object_level_authorization` check when you configure two or more users ("peers"), see `contract-and-schema-testing.md`.

## 9. Rate limits and payload limits

OWASP API4:2023 is Unrestricted Resource Consumption. Basic cases:

- Body over the size limit: 413, and the server does not read the whole body first (measure memory if in doubt).
- List endpoint with `limit=1000000`: clamped or rejected.
- Login, password reset, signup and any endpoint that sends email or SMS: rate limited, 429 with `Retry-After`. Test with a fake clock and a burst of requests in a loop; do not wait in real time.
- Expensive search or export: has a timeout and a limit.
- File upload: type checked by content, size limited, file name sanitised.

For each login, password or admin endpoint:

1. N wrong attempts give 429 or a delay, with N from the spec or an assumption. A missing limit is a High finding even when the README admits it.
2. Abuse case: failures against a victim's email from another client must not lock the victim out, or the report names the trade-off as a finding.
3. Limits keyed on the client address are tried with a prepended spoofed X-Forwarded-For entry (`X-Forwarded-For: 1.2.3.4, <real client>`), which stays blocked behind the documented proxy setup.

## 10. Checks

| Check | Pass condition |
|---|---|
| Harness | router tested in process with real middleware; auth not stubbed away |
| Case table | filled per endpoint from the spec |
| Status codes | each documented status has a test asserting status and body |
| Error shape | one test asserts the same error shape across endpoints |
| No leaks | forced 500 has no stack trace, SQL or paths |
| Validation | boundaries, wrong types, missing fields, unknown fields covered |
| Mass assignment | forbidden fields ignored or rejected; stored row unchanged |
| Over-exposure | responses compared exactly or against an allow list |
| Pagination | walk all pages, invalid cursor, foreign cursor, max page size covered |
| Idempotency | same key twice, different body, concurrent, failed first call covered with database assertions |
| Authentication | missing, malformed, expired, wrong key, deleted user covered |
| Authorization matrix | every resource x operation x actor cell has a test; denied writes check stored state; LIST included |
| Function level auth | admin routes called as a normal user |
| Limits | 413 and 429 paths tested with a fake clock |
| Auth limits | each login, password and admin endpoint has a limit test, a lockout abuse test from another client, and a prepended X-Forwarded-For test |
| Escalation | suspected deeper security issues reported for kwx-hacker, not chased |
