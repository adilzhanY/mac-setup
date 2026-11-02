# Backend testing

How to prove that an API or a service does what its spec says, and find where it breaks: wrong status codes, missing validation, one user reading another user's data, a migration that loses rows, a webhook processed twice, a parser that panics on odd input. This folder is the tester's view. The builder's defaults (test mix, mocks, real Postgres setup) live in kwx-developer `reliability/testing-strategy.md` and `languages/rust/testing.md`; read them first and do not repeat them here. This folder goes deeper on what to test, how to design the cases, and how to run them against real dependencies.

## Contents

1. Before you start
2. Test levels for APIs and services
3. The rules that matter most
4. Default setup: Node or Next.js API
5. Default setup: Rust (axum) service
6. Default setup: Supabase project
7. Files in this folder
8. Checks

## 1. Before you start

- Read the user's CLAUDE.md (global and project) and follow it. If it turns browser automation off, you may still write browser or WebDriver tests into the project, but ask before running them locally; CI may run them. Without a browser, verify with type checks, builds, `curl`, direct database queries and test scripts that drive the real code.
- If the rules forbid certain characters (for example em or en dashes), keep them out of test names, fixtures and reports too.
- Write the test list from the spec (ticket, README, OpenAPI file, DECISIONS.md) before you read the handler code. Reading the implementation first makes you test what the code does instead of what it should do. Evidence: moderate (the whole point of independent testing; kwx-developer `~/.claude/skills/kwx-developer/ai-agents/tests-and-honesty.md` shows agents copy their own mistakes into tests).
- Never point a test run at a production database or a production payment account. Check every connection string and API key before the first run.

## 2. Test levels for APIs and services

| Level | What it proves | What to test there | Speed |
|---|---|---|---|
| Unit (pure functions) | rules and calculations are right | validation rules, money math, permission predicates, parsers, state machines; use property tests for wide input spaces | ms |
| HTTP level (handler + router, in process) | the contract the client sees | every status code, error body shape, validation, pagination, idempotency, auth and the authorization matrix | ms to tens of ms |
| Integration with the real database | SQL, constraints, transactions, RLS work | queries, unique and check constraints, concurrent writes, RLS per role, migrations | tens of ms with a template database |
| External service boundary | your side of a third party integration | webhooks (signature, duplicates, order), payment flows in sandbox, email content, queues | ms (fakes) to minutes (sandbox) |
| Contract | two deployables agree | consumer contracts (Pact) or OpenAPI conformance (Schemathesis), schema diff on every PR | seconds to minutes |
| Fuzz | no input crashes the parser | parsers, decoders, file formats, protocol handlers | minutes to hours, scheduled |
| Load | it holds the expected traffic | see `../performance/performance.md` | minutes |

Push each case to the lowest level that can prove it, and keep one higher level test per feature that proves the wiring (kwx-developer T8).

## 3. The rules that matter most

1. **Test through HTTP, in process.** Call the router with a real request object (supertest, a Next route handler called with a `Request`, axum `oneshot`). It covers routing, extractors, middleware and serialization in milliseconds without a port. Reason: most API bugs live in the glue, not in the pure function. Evidence: moderate (axum, supertest and Zero To Production docs).
2. **Every documented status code has a test, and so does every undocumented one you can provoke.** 400, 401, 403, 404, 409, 422, 429 and the 5xx path each get at least one case, with an assertion on the error body shape, not only the code. Reason: error paths are where clients break. Evidence: moderate.
3. **Run the authorization matrix on every resource.** Owner, another user, anonymous, expired token, wrong role, for read, list, create, update, delete. Reason: Broken Object Level Authorization is item 1 of the OWASP API Security Top 10 (2023), and OWASP's first prevention step is to write tests for it. Evidence: strong. See `api-testing.md`.
4. **Use the real database, never a mock and never SQLite in place of Postgres.** One container or local cluster per run, one fresh database per test cloned from a migrated template. Reason: constraints, RLS, collations and JSON operators differ. Evidence: strong (kwx-developer section 7). Details in `database-testing.md`.
5. **Test RLS as the role the client uses, not as the superuser.** A superuser and the table owner bypass RLS, so a test that connects as `postgres` proves nothing. Evidence: strong (Postgres docs; verified locally, see `database-testing.md`).
6. **A denied write may return success with zero rows.** Under RLS an `UPDATE` of someone else's row returns `UPDATE 0`, not an error. Assert that the row is unchanged, not that an error came back. Evidence: strong (verified locally, Supabase docs).
7. **Every migration is tested on data, not only on an empty schema.** Apply it to a database that holds realistic rows from the previous version and assert the rows survived. Evidence: moderate.
8. **Webhooks are tested for bad signature, duplicate delivery and out of order delivery.** Stripe states it does not guarantee order and may deliver the same event more than once. Evidence: strong (Stripe docs). See `external-services-and-time.md`.
9. **Control time; never sleep.** Inject the clock, use fake timers, tokio paused time, or Stripe test clocks. Reason: sleeps make tests slow and flaky. Evidence: strong.
10. **Never call a real third party API from the default test run.** Fake it at the network boundary; run a small sandbox suite on a schedule. Evidence: moderate (kwx-developer section 6).
11. **Fuzz every parser of untrusted input.** Coverage guided fuzzing finds crashes that example tests never reach. OSS-Fuzz reports over 10,000 vulnerabilities and 36,000 bugs fixed in 1,000 projects (August 2023). Evidence: strong. See `fuzzing.md`.
12. **A schema change is reviewed as a contract change.** Diff the OpenAPI or GraphQL schema on every PR and fail on breaking changes unless the version changes. Evidence: moderate. See `contract-and-schema-testing.md`.
13. **Basic security cases only.** The tester runs the authorization matrix, invalid tokens and obvious injection inputs. Deep attacker style work (token forgery, SSRF chains, privilege escalation research) belongs to a future kwx-hacker skill; note suspected holes in the report and stop. Evidence: opinion (scope).

## 4. Default setup: Node or Next.js API

| Need | Default | Notes |
|---|---|---|
| Runner | Vitest 5 | Jest is fine if the project already uses it |
| HTTP tests (Express, Fastify, plain `http`) | supertest 7 | `request(app).get('/x').set('Authorization', ...)` |
| Next.js App Router route handlers | call the exported `GET`/`POST` with `new Request(...)`, or `next-test-api-route-handler` (App Router support from `next@14.0.4`) | NTARH must be the first import in the file |
| Database | Postgres 17 or 18 in Docker or a local cluster; `@testcontainers/postgresql` 12 when tests should own the container | template database per test, see `database-testing.md` |
| Third party HTTP | MSW 3 at the network layer | never `vi.mock` your own API client |
| Property tests | fast-check 4 | for validators and money math |
| Contract | Schemathesis 4 against the OpenAPI file; Pact JS 17 only when consumer and provider deploy separately | |
| Email | Mailpit | assert on the received message through its API |

Minimal HTTP test (verified 2026-10-31 with Vitest 5.0.5 and supertest 7.3.1):

```js
import { describe, it, expect } from 'vitest';
import request from 'supertest';
import { createServer } from './server.mjs';

const app = createServer();

describe('GET /items/:id authorization matrix', () => {
  it.each([
    ['owner', 'Bearer alice', 200],
    ['other user', 'Bearer bob', 404],
    ['anonymous', undefined, 401],
  ])('%s gets %i', async (_who, auth, status) => {
    const req = request(app).get('/items/1');
    if (auth) req.set('Authorization', auth);
    expect((await req).status).toBe(status);
  });
});
```

## 5. Default setup: Rust (axum) service

| Need | Default |
|---|---|
| Runner | `cargo nextest run` plus `cargo test --doc` |
| HTTP tests | `tower::ServiceExt::oneshot` on the `Router` (no socket); a real server on `127.0.0.1:0` with `reqwest` for end to end |
| Database | `#[sqlx::test]` (fresh database per test, migrations applied), or `testcontainers-modules` Postgres |
| Third party HTTP | `wiremock` |
| Snapshots | `insta` with redactions for ids and timestamps |
| Property and fuzz | `proptest`, `cargo fuzz` |
| Time | `#[tokio::test(start_paused = true)]` |

The axum `oneshot` pattern and the Rust specific extras are in `rust-services-testing.md`.

## 6. Default setup: Supabase project

| Need | Default | Notes |
|---|---|---|
| Local stack | `supabase start` (Docker) | API on 54321, Postgres on 54322, Studio on 54323, Mailpit on 54324 (Supabase CLI docs) |
| Exclude unused services for speed | `supabase start -x realtime,storage-api,imgproxy,studio,edge-runtime,logflare,vector` | names from the CLI reference |
| Schema and RLS tests | pgTAP files in `supabase/tests/database/*.sql`, run with `supabase test db` | each file `begin; select plan(n); ... select * from finish(); rollback;` |
| Fresh database | `supabase db reset` | replays migrations and `seed.sql`; deletes other local data |
| App level RLS tests | Vitest + `supabase-js`, two real test users signed in with `signInWithPassword` | create users with the admin client in setup, never in production |
| Auth emails | Mailpit on 54324 | magic links and confirmation emails land there |

`supabase test db --linked` runs the tests against the linked remote project. Do not use it against production; use a separate project or a branch.

## 7. Files in this folder

| File | Read when |
|---|---|
| `api-testing.md` | writing HTTP level tests: status codes, validation, pagination, idempotency, auth, the authorization matrix |
| `contract-and-schema-testing.md` | two services or an app and an API must stay compatible; adding Pact, Schemathesis, schema diffs, GraphQL checks |
| `database-testing.md` | tests touch Postgres or Supabase: isolation, migrations, constraints, RLS, seed data |
| `external-services-and-time.md` | payments, webhooks, email, queues, cron, anything that depends on the clock |
| `rust-services-testing.md` | the service is Rust: nextest, insta, proptest, loom, tokio time, sqlx test macros |
| `fuzzing.md` | the code parses untrusted bytes or text: file formats, protocols, decoders, user supplied config |

## 8. Checks

| Check | Pass condition |
|---|---|
| User rules read | CLAUDE.md read; browser and GUI runs only with permission |
| Spec first | a written case list exists, made from the spec before reading handlers |
| Status codes | every documented status has a test with a body assertion |
| Authorization matrix | owner, other user, anonymous, expired token, wrong role covered per resource and operation |
| Real database | no DB mocks, no SQLite stand in; tests pass in random order and in parallel |
| RLS | tested as `authenticated` and `anon`, never as superuser; denied writes assert the row is unchanged |
| Migrations | applied to a database with previous version data; rows survive |
| Webhooks | bad signature, duplicate and out of order cases exist |
| Time | no `sleep` in tests; clock injected or faked |
| Third parties | no real third party call in the default run |
| Parsers | fuzz target exists for each parser of untrusted input |
| Schema | breaking change check runs on PRs |
| Report | anything not tested is listed under "Not checked" |
