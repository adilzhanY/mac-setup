# Testing strategy

Tests exist to let people change code with confidence. A suite that is slow, flaky, or breaks on every refactor destroys that confidence and gets ignored. This file sets the default test mix per kind of project, where tests live and how they are named, what to mock and what never to mock, how to test against a real Postgres, end to end tests for web and mobile, property and snapshot testing, and a flaky test policy.

## Contents

1. Principles (T1 to T12)
2. The default mix: pyramid or trophy
3. Test sizes (speed and determinism)
4. Where tests live and how they are named
5. Fixtures and test data
6. What to mock, what never to mock
7. Testing against a real Postgres
8. End to end: Playwright (web), Maestro (React Native)
9. React and React Native component tests
10. Property based, snapshot, contract and mutation testing
11. Flaky test policy
12. Coverage
13. Checks

## 1. Principles

**T1. Test behavior through the public API, not implementation.** Call the code the way its users do. A test should change only when requirements change, not when you refactor, fix an unrelated bug or add a feature (Software Engineering at Google ch. 12: "strive for unchanging tests"). The more your tests resemble the way the software is used, the more confidence they give (Kent C. Dodds).

**T2. Prefer state checks over interaction checks.** Assert on results and resulting state (`expect(await repo.get(id)).toEqual(...)`), not on which methods were called (`expect(repo.save).toHaveBeenCalledWith(...)`). Interaction asserts are for side effects you cannot observe otherwise (an email sent, a payment provider charged), and then only on state changing calls (SWE at Google ch. 13).

**T3. A test that fails must say why.** Test name states behavior and expected outcome; assertion messages include the inputs that matter; one behavior per test.

**T4. No logic in tests.** No loops, conditionals or string building to compute the expected value; write the literal expected value. A test with logic needs its own test (SWE at Google: "Don't put logic in tests").

**T5. DAMP over DRY.** Repetition in tests is fine if each test reads top to bottom on its own. Share helpers that build data, not helpers that hide the arrange, act and assert.

**T6. Each test sets up its own state and leaves none behind.** No order dependence, no shared mutable fixtures, no reliance on data another test created. Tests must pass in random order and in parallel.

**T7. Every bug fix starts with a failing test that reproduces it,** at the lowest level that can reproduce it. If a higher level test caught a bug no lower test caught, add the lower test (Ham Vocke, "The Practical Test Pyramid").

**T8. Push tests as far down as they still give confidence, and do not duplicate across levels.** Cover edge cases in fast tests; keep one higher level test that proves the wiring. Delete higher level tests already covered below if they add no confidence.

**T9. Determinism is required.** Inject the clock, seed randomness, never sleep for a fixed time (wait for a condition), never hit the public internet. A test that sometimes fails is worse than no test (section 11).

**T10. Error paths are tested.** For every dependency: it returns an error, it times out, it returns malformed data. For every input boundary: invalid, empty, too large.

**T11. Tests are code: typed, linted, reviewed.** No `any` to make a test compile; `.only` and `.skip` are lint errors on CI.

**T12. Speed budget.** The pre-push suite (unit + integration) runs in under about 5 minutes on CI for a typical app; anything slower gets split, parallelized or sharded before people start skipping it.

## 2. The default mix: pyramid or trophy

Both shapes agree on the substance: many fast tests, few slow ones, and confidence as the goal. They differ on where the bulk sits.

| Project kind | Default shape | Bulk of tests |
|---|---|---|
| Web app / API in TypeScript (React, Next, Remix, Node API) | Testing trophy (Dodds): static types + lint as the base, then mostly integration | Route or component level tests with real modules wired together, network mocked at the HTTP boundary (MSW), real DB for API tests |
| Rust library, parser, algorithm, pure domain logic | Pyramid (SWE at Google aims about 80% unit, 15% integration, 5% end to end) | Small unit tests + property tests |
| Backend service with a database | Integration heavy middle | HTTP handler tests against a real Postgres per test (section 7) |
| React Native app | Trophy + a few device E2E flows | Component tests with React Native Testing Library; Maestro for 5 to 15 critical flows |
| CLI | Integration via the binary | `assert_cmd` (Rust) or spawn the CLI with fixtures, snapshot the output carefully |

"Unit" and "integration" mean different things to different people; Kent C. Dodds counts a component test with mocked HTTP as integration, Fowler distinguishes "solitary" (collaborators mocked) and "sociable" (real collaborators) unit tests. Do not argue about names; decide by size (section 3) and by what is mocked (section 6).

End to end tests: only the critical user journeys (sign up, log in, pay, the core action of the product). Each one is slow and can flake; 10 good ones beat 200 brittle ones.

Static analysis is part of testing: `tsc --strict`, ESLint with type aware rules, `cargo clippy -D warnings`. Types remove whole classes of tests (null checks, wrong argument shapes).

## 3. Test sizes (speed and determinism)

Classify by what a test may do, not by what it covers (Google testing blog "Test sizes"; SWE at Google ch. 11):

| Size | Allowed | Not allowed | Typical time limit |
|---|---|---|---|
| Small | One process (ideally one thread), in-memory only | Network, disk, database, sleep, real clock, system properties | about 1 s per test, 60 s per target at Google |
| Medium | One machine: localhost DB in a container, local files, multiple processes | Network beyond localhost | 300 s per target |
| Large | Multiple machines, real services, staging | Nothing | 900 s+ |

Write the smallest test that can verify the behavior. Small tests are fast and deterministic by construction. Medium tests (real Postgres in Docker) are the right size for repository and HTTP handler tests. Large tests run separately, not on every push.

## 4. Where tests live and how they are named

Pick one convention per project and apply it everywhere; a mix is an audit finding.

| Stack | Unit / small | Integration / medium | E2E |
|---|---|---|---|
| TS (Vitest/Jest) | Colocated: `src/billing/invoice.ts` + `src/billing/invoice.test.ts` | Colocated `*.int.test.ts`, or `tests/integration/` mirroring `src/` | `e2e/` at the root (Playwright) |
| Rust | Same file: `#[cfg(test)] mod tests { use super::*; ... }` | `tests/*.rs` (each file is a separate crate, public API only) with shared helpers in `tests/common/mod.rs` | `tests/e2e_*.rs` or a separate crate |
| React Native | Colocated `*.test.tsx` | Colocated, or `__tests__/` beside the screen | `.maestro/` flows at the app root |
| Python (if present) | `tests/` mirroring package | `tests/integration/` | `tests/e2e/` |

Rules:

- Do not mix `__tests__/` folders and colocated `*.test.ts` files in one project. Do not mix `.test.` and `.spec.` suffixes.
- Test files import from the module's public entry (`../billing`), not from internal files, unless testing an internal module deliberately.
- Test names describe behavior and outcome. Read as a sentence with the `describe`:

```ts
describe("Invoice.total", () => {
  it("applies the discount before tax", ...);
  it("returns 0 for an empty invoice", ...);
  it("throws INVALID_CURRENCY when lines use different currencies", ...);
});
```

```rust
#[test]
fn total_applies_discount_before_tax() { ... }
#[test]
fn parse_rejects_amount_with_more_than_two_decimals() { ... }
```

Bad names: `test1`, `it("works")`, `testCalculate`, `it("should call repository")` (implementation, not behavior).

- Structure each test as arrange, act, assert, separated by blank lines. One act per test.

## 5. Fixtures and test data

- **Factories with defaults, override only what the test cares about.** The test then shows the values that matter and nothing else (SWE at Google: helper methods with defaults beat shared constants).

```ts
export function buildUser(overrides: Partial<User> = {}): User {
  return { id: randomUUID(), email: `u-${randomUUID()}@test.local`, plan: "free", createdAt: FIXED_NOW, ...overrides };
}
// In the test, only `plan` matters:
const user = buildUser({ plan: "pro" });
```

- Unique values per test (UUID based emails) so parallel tests never collide on unique constraints.
- No shared mutable fixture objects across tests. If a `beforeEach` sets a value a test asserts on, set that value in the test instead (SWE at Google, "Shared Setup").
- Database seed data for tests lives with the tests (`tests/fixtures/*.sql` or factory calls), not in the dev seed script.
- Fixed clock: a single `FIXED_NOW` constant and an injected clock, or fake timers (`vi.useFakeTimers()`, `vi.setSystemTime()`; `tokio::time::pause()` in Rust). Never `Date.now()` inside expected values.
- Golden files (expected outputs on disk) are fine for formatters, code generators and parsers; review their diffs like code.

## 6. What to mock, what never to mock

Default order of preference (SWE at Google ch. 13): **real implementation, then a fake, then a stub, then a mock.** Use a double only when the real thing is slow, nondeterministic, or has side effects you cannot allow.

| Dependency | Default in tests | Why |
|---|---|---|
| Your own modules, pure functions, domain logic | Real. Never mock | Mocking your own code tests the mock and breaks on refactor |
| Your database (Postgres) | Real Postgres in Docker (section 7). Never mock the DB or the ORM, never swap in SQLite or an in-memory DB | Constraints, transactions, JSON operators, collation and query plans differ; the bugs live there |
| Your own HTTP API (from your frontend) | Real handlers in API tests; MSW handlers in frontend tests built from the same schema | Keeps both sides honest |
| Third party HTTP APIs (Stripe, GitHub, OpenAI) | Mock at the network layer: MSW (TS), `wiremock` (Rust), Playwright `page.route` in E2E | Never call the real API in CI: cost, rate limits, flakiness |
| Third party SDKs | Wrap the SDK in a small adapter you own; fake the adapter in unit tests; test the adapter itself against a network mock | "Don't mock what you don't own" (Freeman and Pryce): mocks of SDKs encode wrong assumptions |
| Time, randomness, UUIDs | Inject or fake | Determinism |
| Filesystem | Real temp dir (`fs.mkdtemp`, `tempfile` crate) | Cheap and real |
| Email, SMS, push | Fake that records messages (in-memory outbox) | Assert on the recorded message |
| Queues | Real broker in Docker for integration; in-memory fake with the same interface for unit tests | |
| Browser APIs in component tests | jsdom / happy-dom; real browser for anything layout or focus dependent (Playwright component tests or E2E) | jsdom has no layout |

Mocking rules:

- **Mock at the boundary, not in the middle.** Mock `fetch` traffic (MSW), not your `apiClient` module; mocking the client means you never test that you call it correctly (Dodds, "Stop mocking fetch").
- **No `jest.mock` / `vi.mock` of relative imports of your own code** except to cut off a true boundary module (the SDK adapter, the clock).
- **Fakes need tests too**: run the same contract test suite against the fake and the real implementation (SWE at Google, "Fakes should be tested").
- **Do not overspecify**: assert only the arguments that matter (`expect.objectContaining`), never the call order of unrelated calls.
- **Reset between tests**: `restoreMocks: true` (Vitest/Jest config) so spies do not leak.

## 7. Testing against a real Postgres

Default: one Postgres container for the test run, isolated state per test. Options, fastest first:

1. **Transaction per test, rolled back at the end.** Fast. Works when the code under test accepts a connection or transaction from the test. Does not work when the code opens its own transactions on other connections, or for code that tests commit behavior.
2. **Database per test from a template.** Migrate once into `app_template`, then each test runs `CREATE DATABASE test_<uuid> TEMPLATE app_template` (tens of milliseconds) and drops it after. Fully isolated, parallel safe. Rust: `#[sqlx::test]` does this for you (fresh database per test, migrations applied, optional fixtures from `fixtures/*.sql`).
3. **Truncate all tables between tests.** Simple but forces serial tests.

Setup:

- Locally and in CI, start Postgres with Docker Compose or a CI service container, or Testcontainers (`@testcontainers/postgresql`, `testcontainers-modules` for Rust) when tests should manage their own containers.
- Use the same major Postgres version and extensions as production (the GitLab 2017 backups failed silently because `pg_dump` 9.2 ran against a 9.6 database).
- Run the real migrations, never a hand written test schema.
- Speed up test Postgres with `fsync=off`, `synchronous_commit=off`, `full_page_writes=off` (test only), and a tmpfs data dir.

```yaml
# docker-compose.test.yml
services:
  db:
    image: postgres:17
    environment: { POSTGRES_PASSWORD: test }
    command: postgres -c fsync=off -c synchronous_commit=off -c full_page_writes=off
    tmpfs: [/var/lib/postgresql/data]
    ports: ["5433:5432"]
```

## 8. End to end: Playwright (web), Maestro (React Native)

### Playwright (official best practices)

- Locate by what the user sees: `getByRole('button', { name: 'Pay' })`, `getByLabel`, `getByText`. Not CSS classes or XPath. Add `data-testid` only where no accessible name exists (and then consider fixing the accessibility).
- Use web first assertions that auto-wait: `await expect(page.getByText('Paid')).toBeVisible()`. Never `expect(await locator.isVisible()).toBe(true)`, never `page.waitForTimeout(...)`.
- Each test is isolated: own browser context, own user and data created through the API or DB in a fixture, not through the UI. Log in once with `storageState` and reuse it.
- Do not test third party sites; stub them with `page.route`.
- CI: `retries: 2` only on CI, `trace: 'on-first-retry'`, `forbidOnly: !!process.env.CI`, shard with `--shard=i/n`. A test that passes only on retry is flaky and goes into the flaky policy, not ignored.
- Lint tests with `eslint-plugin-playwright` (catches missing `await`, `waitForTimeout`).
- Run against a production build (`next build && next start`), not the dev server.

### React Native

- Default: **Maestro** for device E2E flows (YAML flows in `.maestro/`, works with Expo and bare RN, tolerant of timing, `maestro test .maestro/`). Use **Detox** when you need gray box synchronization with the RN bridge and already have native build tooling; it is more setup and more maintenance.
- Run E2E on a release build, not a debug build with Metro.
- Target elements by `testID` (RN has no roles in the same way as the web) or accessibility labels, kept stable.
- Keep the flow count small: login, onboarding, the core action, purchase, offline/reconnect.

## 9. React and React Native component tests

Use Testing Library (`@testing-library/react`, `@testing-library/react-native`). The rules from Kent C. Dodds, "Common mistakes with React Testing Library":

- Query with `screen`, prefer `getByRole` with `name`, then `getByLabelText`, then `getByText`. Avoid `container.querySelector`.
- Simulate with `@testing-library/user-event` (`await user.click(...)`), not `fireEvent`, for anything a user does.
- Use `findBy*` to wait for something to appear; `queryBy*` only to assert absence; `getBy*` for presence (it throws with a helpful message).
- No side effects inside `waitFor`, one assertion per `waitFor`, never an empty `waitFor` callback.
- Do not wrap renders or events in `act` manually; Testing Library already does.
- Use the ESLint plugins `eslint-plugin-testing-library` and `eslint-plugin-jest-dom`.
- Do not test hooks in isolation when a component test covers them; test custom hooks directly only when they are a reusable library.
- Mock network with MSW, not the data fetching hook.

## 10. Property based, snapshot, contract and mutation testing

**Property based testing.** For parsers, serializers, encoders, math, sorting, state machines and anything with invariants. Libraries: `fast-check` (TS), `proptest` (Rust). Classic properties: round trip (`parse(format(x)) == x`), invariants (output sorted, total preserved), model based (compare with a simple reference implementation), no crash on any input. The framework shrinks a failure to a minimal counterexample and prints the seed; add that seed or the minimal case as a permanent regression test. Fix the seed on CI if runs must be reproducible (`fc.configureGlobal({ seed })`); proptest stores failures in `proptest-regressions/`, commit that folder.

```ts
fc.assert(fc.property(fc.string(), (s) => expect(decode(encode(s))).toBe(s)));
```

**Snapshot testing.** A snapshot is an assertion without stated intent; people re-record failing snapshots without reading them (Justin Searls via Kent C. Dodds, "Effective snapshot testing"). Rules: small and focused (lint `jest/no-large-snapshots`, for example 50 lines), prefer `toMatchInlineSnapshot` so the expected value is visible in review, use custom serializers to strip noise (ids, dates, absolute paths), never run `-u` across the whole suite to make CI green. Good uses: error message formatting, CLI output, generated code, serialized config. Bad uses: whole rendered component trees, API responses with timestamps.

**Contract tests.** When a consumer and provider are deployed independently by different teams or repos, use consumer driven contracts (Pact): the consumer's tests produce the contract, the provider verifies it in CI, and `can-i-deploy` gates releases. In a monorepo that deploys frontend and backend together with shared types, prefer a shared schema (OpenAPI or zod) with generated types and validation on both sides; Pact adds little there.

**Mutation testing.** Coverage says a line ran; mutation testing says a test would notice if it were wrong. Run `cargo-mutants` (Rust) or Stryker (TS) on the critical modules (money, auth, permissions) periodically, not on every push.

## 11. Flaky test policy

A flaky test passes and fails on the same code. At Google about 1.5% of test runs are flaky, almost 16% of tests have some flakiness, and 84% of pass to fail transitions in CI involve a flaky test (Google Testing Blog, 2016). People learn to ignore red builds, and real failures get dismissed as flakes.

Policy:

1. **Detect.** CI records which tests passed on retry. Locally: run the suspect test many times (`npx playwright test --repeat-each=50 --retries=0`, `vitest run -t 'name'` in a loop, `cargo nextest run --retries 0` repeatedly or `for i in $(seq 50); do cargo test name || break; done`). Randomize order to expose hidden coupling (`vitest --sequence.shuffle`, `jest --randomize`).
2. **Quarantine within one working day.** Move it out of the blocking suite (tag `@flaky`, `test.fixme`, `#[ignore = "flaky: #123"]`) with an issue and an owner. Quarantine keeps the main suite trustworthy (Fowler, "Eradicating non-determinism in tests").
3. **Fix or delete within a fixed time (default 2 weeks).** Cap the quarantine size (Fowler cites a limit like 8 tests); when it is full, fixing comes before new work.
4. **Never paper over with retries in unit or integration tests.** Retries are tolerated only in E2E on CI, and a pass on retry still counts as flaky.
5. **A flaky test may be a real bug** (race condition, missing timeout). Investigate the code, not only the test.

Common causes and fixes (Fowler; Google):

| Cause | Fix |
|---|---|
| Fixed sleeps, timing assumptions | Wait for a condition (poll with timeout, `findBy`, web first assertions); fake timers |
| Shared state between tests (DB rows, globals, module singletons, env vars) | Per test data with unique ids, DB per test or rollback, reset modules |
| Test order dependence | Randomize order in CI; each test builds its own state |
| Real clock, time zones, DST, month ends | Inject a fixed clock, set `TZ=UTC` in the test env, add explicit tests for DST and leap days |
| Network to real services | Network mocks; Testcontainers for owned dependencies |
| Concurrency and async races | Await everything; deterministic schedulers (`tokio::time::pause`); fix the race in code |
| Resource leaks (open handles, ports, connections) | Close in `afterEach`; `--detectOpenHandles` (Jest); random free ports |
| Unseeded randomness | Seed and print the seed on failure |

## 12. Coverage

- Coverage is a tool to find untested code, not a target. A fixed bar (for example 80%) becomes a ceiling and invites tests without assertions (SWE at Google, "A note on code coverage").
- Measure it, look at uncovered branches in changed files during review, and require tests for new logic, especially error branches.
- High value targets get near full branch coverage plus mutation testing: money, auth, permissions, data migrations, parsers of external input.

## 13. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| One test location convention | Only colocated or only `__tests__`, one suffix | `fd -e ts -e tsx '\.(test|spec)\.' src | sed -E 's/.*\.(test|spec)\..*/\1/' | sort | uniq -c`; `fd -t d __tests__ src` |
| No focused or skipped tests | 0 hits on main | `rg -n '\.(only|skip)\(|\bfit\(|\bxit\(|test\.fixme' src e2e tests` (skips allowed only with an issue link); ESLint `no-focused-tests`, `no-disabled-tests` |
| No fixed sleeps in tests | 0 hits | `rg -n 'waitForTimeout|setTimeout\(r|sleep\(' --glob '*test*' --glob 'e2e/**'` |
| No DB mocks | No mocking of the DB client, ORM or repository in integration tests | `rg -n "vi\.mock\(.*(db|prisma|drizzle|knex|pg)|jest\.mock\(.*(db|prisma|pg)" src tests` |
| No SQLite stand-in for Postgres | Test config uses Postgres | `rg -n 'sqlite|:memory:|h2' tests vitest.config.* jest.config.*` |
| No mocking own relative modules | Mocks only of boundary modules | `rg -n "(vi|jest)\.mock\(['\"]\.\.?/" src` and review each |
| Real network blocked in tests | MSW `onUnhandledRequest: 'error'` | `rg -n "onUnhandledRequest" src tests` |
| Mocks restored | `restoreMocks: true` or `mockReset` in config | `rg -n 'restoreMocks|clearMocks|mockReset' vitest.config.* jest.config.*` |
| Clock fixed | Tests use fake timers or injected clock where time matters | `rg -n 'Date\.now\(\)|new Date\(\)' --glob '*test*'` and review |
| TZ pinned | CI test env sets `TZ=UTC` | `rg -n 'TZ' .github/workflows package.json` |
| Order independence | Suite passes shuffled | `vitest run --sequence.shuffle` or `jest --randomize` in CI weekly |
| Playwright config sane | `forbidOnly` on CI, retries only on CI, trace on retry | `rg -n 'forbidOnly|retries|trace' playwright.config.*` |
| Playwright locators user facing | Few CSS / XPath locators | `rg -n "locator\(['\"](\.|#|//|xpath)" e2e` count trending to 0 |
| RTL best practices | Plugins enabled | `rg -n 'testing-library|jest-dom' eslint.config.* .eslintrc*` |
| Snapshot size limited | `jest/no-large-snapshots` on, or snapshot files under ~50 lines per entry | `fd -e snap | xargs wc -l | sort -n | tail` |
| Flaky tests tracked | Each quarantined test links an issue | `rg -n '@flaky|fixme|#\[ignore' tests src e2e` each with an issue URL |
| Proptest regressions committed | Folder present in git when proptest is used | `git ls-files | rg proptest-regressions` |
| Rust tests layout | Unit tests in `mod tests` with `#[cfg(test)]`, integration in `tests/` | `rg -n '#\[cfg\(test\)\]' src | wc -l`; `ls tests` |
| Bug fixes have tests | Fix PRs include a test change | PR review; `git log --grep=fix --stat` shows test files touched |
