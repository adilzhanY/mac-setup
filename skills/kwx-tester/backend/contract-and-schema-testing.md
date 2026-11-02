# Contract and schema testing

How to prove that a client and an API still agree after one of them changes. Three tools cover most cases: consumer driven contracts (Pact) when two deployables are released separately, OpenAPI driven property testing (Schemathesis) to check the server against its own published schema, and schema diffs (oasdiff, GraphQL Inspector, generated type diffs) to catch breaking changes in review. kwx-developer `reliability/testing-strategy.md` section 10 says when Pact is worth it; this file is how to run each approach and what to assert.

## Contents

1. Pick the approach
2. Consumer driven contracts with Pact
3. OpenAPI property testing with Schemathesis
4. Schema snapshots and breaking change diffs
5. GraphQL
6. Supabase and generated types
7. Versioning rules a tester checks
8. Checks

## 1. Pick the approach

| Situation | Approach | Why |
|---|---|---|
| One repo, frontend and backend deploy together, shared types | shared schema (zod or OpenAPI) + generated types + type check in CI; Schemathesis against the server | Pact adds little when both sides ship in one commit (kwx-developer) |
| Mobile app talks to your API (old app versions stay in the field) | schema diff on every PR with "no breaking change" gate; Schemathesis; optionally Pact with the app as consumer | users do not update the app on your schedule |
| Two services or repos, deployed separately, you control both | Pact with a broker and `can-i-deploy` | the consumer's real needs gate the provider's deploy |
| Public API with unknown consumers | OpenAPI as the contract, Schemathesis, oasdiff breaking check | Pact docs: not a good fit for public APIs, because consumers cannot be identified |
| You consume someone else's API | record their schema, run a small scheduled smoke suite against their sandbox, fake them with MSW or wiremock built from the schema | you cannot verify their side |

Pact is also not for functional testing of the provider, load testing, or pass-through APIs where the real effect is downstream (Pact docs, "What is Pact good for"). Evidence: moderate.

A contract is any boundary where two codebases agree on names and shapes, including in-process bridges: Tauri invoke to #[tauri::command], Electron ipcRenderer to ipcMain, React Native or Expo JS to a native module. These get the same two checks as an HTTP API: the names match, and each argument and response shape is exercised by a test that crosses the bridge. Desktop detail: `../desktop/desktop.md` section 6.

## 2. Consumer driven contracts with Pact

How it works (Pact docs): the consumer's tests describe each request it sends and the minimal response it needs; Pact runs a mock provider, the consumer code sends real requests to it, and a pact file is written. The provider side replays every interaction against the real provider and checks the response satisfies it. Provider states ("user 123 exists") are set up by handlers before each replay.

Consumer test (Pact JS 17, V4 specification, condensed from the Pact JS docs):

```js
const { Pact, Matchers, SpecificationVersion } = require('@pact-foundation/pact');
const { eachLike, like } = Matchers;

const provider = new Pact({
  consumer: 'mobile-app',
  provider: 'todo-api',
  spec: SpecificationVersion.SPECIFICATION_VERSION_V4,
});

it('lists todos', async () => {
  await provider
    .addInteraction()
    .given('user alice has 2 todos')
    .uponReceiving('a request for alice todos')
    .withRequest('GET', '/todos', (b) => b.headers({ Authorization: like('Bearer token') }))
    .willRespondWith(200, (b) => b.jsonBody(eachLike({ id: like(1), title: like('Buy milk') })))
    .executeTest(async (mock) => {
      const todos = await new TodoClient(mock.url).list();
      expect(todos[0].title).toBe('Buy milk');
    });
});
```

Provider verification (Pact JS docs):

```js
const { Verifier } = require('@pact-foundation/pact');

await new Verifier({
  provider: 'todo-api',
  providerBaseUrl: 'http://127.0.0.1:3000',
  pactBrokerUrl: process.env.PACT_BROKER_URL,
  consumerVersionSelectors: [{ mainBranch: true }, { deployedOrReleased: true }],
  stateHandlers: {
    'user alice has 2 todos': async () => { await seedAliceTodos(2); },
  },
  publishVerificationResult: process.env.CI === 'true',
  providerVersion: process.env.GIT_SHA,
  providerVersionBranch: process.env.GIT_BRANCH,
  enablePending: true,
}).verifyProvider();
```

Deploy gate (Pact broker docs):

```bash
pact-broker can-i-deploy --pacticipant todo-api --version "$GIT_SHA" --to-environment production
pact-broker record-deployment --pacticipant todo-api --version "$GIT_SHA" --environment production
```

Rules:

1. **Use matchers (`like`, `eachLike`, regex), not exact values,** for anything the consumer does not depend on. Exact values make the contract break on harmless data changes. Evidence: moderate (Pact docs).
2. **Only put in the contract what the consumer actually reads.** Extra fields in the pact force the provider to keep fields nobody uses. Evidence: moderate.
3. **Every `given` state has a handler.** Without `stateHandlers` the Verifier ignores provider states and logs only a warning (Pact JS docs), so tests pass against whatever data happens to exist. Evidence: moderate.
4. **Publish verification results only from CI,** with the git SHA as the version. Evidence: moderate (Pact docs).
5. **Contract tests do not replace provider functional tests.** A pact proves the shape; your API tests prove behaviour. Evidence: moderate.

## 3. OpenAPI property testing with Schemathesis

Schemathesis (v4.32 in October 2026) reads an OpenAPI 2.0 to 3.2 or GraphQL schema, generates valid and invalid requests, sends them, and checks the responses against the schema. Each failure comes with a minimal `curl` reproducer.

Run it (commands from the Schemathesis quick start; uses `uvx`, so nothing is installed globally):

```bash
# against a running local server with its schema
uvx schemathesis run http://127.0.0.1:3000/openapi.json \
  --header "Authorization: Bearer $TEST_TOKEN"

# local schema file, server elsewhere
uvx schemathesis run ./openapi.yaml --url http://127.0.0.1:3000

# replay one failure
uvx schemathesis replay <ID>
```

Checks it runs (Schemathesis checks reference; all on by default except `max_response_time`):

| Check | Finds |
|---|---|
| `not_a_server_error` | any 5xx |
| `status_code_conformance` | status codes not documented for the operation |
| `content_type_conformance` | missing or undocumented `Content-Type` |
| `response_headers_conformance` | required headers missing or wrong |
| `response_schema_conformance` | body does not match the schema |
| `negative_data_rejection` | invalid input accepted |
| `positive_data_acceptance` | valid input rejected |
| `missing_required_header`, `unsupported_method` | a missing required header accepted; undefined method not answered with 405 |
| `ignored_auth` | operation works without valid credentials |
| `use_after_free`, `ensure_resource_availability` (stateful) | deleted resource still readable; created resource returns 404 |
| `object_level_authorization` | one user reads another user's object; runs only with two or more configured users |
| `max_response_time` (off by default) | slow responses |

Rules:

1. **Run it against a server backed by a disposable database.** It creates, updates and deletes data. Never against production. Evidence: opinion (obvious, often forgotten).
2. **Treat each failure as either a server bug or a schema bug, and say which.** If the server returns 409 and the schema does not document 409, the fix may be in the schema. Do not silence the check. Evidence: moderate.
3. **Use the stateful mode for CRUD APIs.** It follows OpenAPI `links` (and infers some), passes real ids between calls, and finds use-after-delete bugs. Evidence: moderate (Schemathesis docs).
4. **Configure two users to get the BOLA check for free.** It complements, but does not replace, the matrix in `api-testing.md`. Evidence: moderate.
5. **Pin the seed in CI for reproducible runs, and run a longer randomized job on a schedule.** Evidence: opinion.

pytest integration, when the project already has Python tests (Schemathesis quick start):

```python
import schemathesis

schema = schemathesis.openapi.from_url("http://127.0.0.1:3000/openapi.json")

@schema.parametrize()
def test_api(case):
    case.call_and_validate()
```

## 4. Schema snapshots and breaking change diffs

A committed schema file is a snapshot of the contract. Diffing it on every PR turns "did we break clients?" into a check.

OpenAPI with oasdiff (oasdiff docs; 778 checks; "breaking" means a request valid before can now be rejected, or a response can contain something clients were not written to handle):

```bash
oasdiff breaking origin-main/openapi.yaml openapi.yaml --fail-on ERR
oasdiff changelog origin-main/openapi.yaml openapi.yaml
```

GitHub Action: `oasdiff/oasdiff-action/breaking@v0` with `base` and `revision` inputs.

Rules:

1. **Generate the schema from code and commit it; CI fails if the generated file differs from the committed one.** Then a schema change is always visible in the diff. Evidence: moderate.
2. **Breaking changes need a version bump or an explicit, reviewed exception.** Typical breaking changes: removing a field or endpoint, renaming, making an optional request field required, narrowing a type or enum in a request, widening an enum in a response for clients that switch exhaustively, changing a status code. Evidence: moderate (oasdiff rule set).
3. **Snapshot the database schema too.** `pg_dump --schema-only --no-owner` into a file, committed, diffed in review. A surprise in that diff (a dropped index, a changed policy) is a finding. Evidence: opinion.
4. **Response snapshots are for shape, not for data.** Redact ids and timestamps; prefer a schema assertion over a whole body snapshot. kwx-developer section 10 covers snapshot hygiene.

## 5. GraphQL

- Diff schemas with GraphQL Inspector: `graphql-inspector diff OLD_SCHEMA NEW_SCHEMA`. It sorts changes into breaking, dangerous and non-breaking, and fails only on breaking ones by default (GraphQL Inspector docs). Evidence: moderate.
- Schemathesis supports GraphQL schemas (June 2018 spec and later) for generated queries.
- Test per field authorization: a field resolver that skips the check leaks data even when the parent query is protected. Query nested paths (`user { orders { customer { email } } }`) as another user.
- Test query cost limits: deep nesting and huge `first:` arguments must be rejected (OWASP API4).

## 6. Supabase and generated types

For a Supabase backend, the database schema is the API (PostgREST). The contract test is:

```bash
supabase gen types typescript --local > types/supabase.ts
git diff --exit-code types/supabase.ts   # fails if migrations changed types without committing them
```

Then the app's type check (`tsc --noEmit`) shows every call site a schema change breaks. Add pgTAP `has_column`, `col_type_is` and `policies_are` assertions for tables a mobile app depends on, because old app versions in the field cannot be type checked. Evidence: moderate.

## 7. Versioning rules a tester checks

| Rule | How to check |
|---|---|
| Additive changes only within a version | oasdiff breaking check passes |
| Old mobile app versions keep working | run the previous release's API client tests (or its pact) against the new server |
| Deprecated fields still returned until the announced date | test asserts the field is present and a `Deprecation` or `Sunset` header if the API uses them |
| Enum values added in responses do not crash old clients | client code has a default branch; test with an unknown enum value |
| Error codes are part of the contract | error code strings snapshot or schema checked |

## 8. Checks

| Check | Pass condition |
|---|---|
| Approach chosen | matches the table in section 1, with the reason written down |
| Bridges | every in-process bridge (Tauri or Electron IPC, a native module) has a name match check and a test per call that crosses it with the real argument keys |
| Pact (if used) | matchers used, only consumed fields, every state has a handler, verification published from CI, `can-i-deploy` gates deploys |
| Schemathesis | runs against a disposable database; failures triaged as server bug or schema bug; stateful mode on for CRUD |
| BOLA via peers | two users configured, or the gap noted |
| Schema committed | generated schema file committed and checked for drift in CI |
| Breaking diff | oasdiff or GraphQL Inspector gate on PRs |
| DB schema snapshot | schema dump committed or diffed in review |
| Supabase types | generated types fresh; app type check passes |
| Old clients | previous client version tested against the new server |
