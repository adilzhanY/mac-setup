# Reliability: the master rules

Read this file first for any work that touches error handling, tests, logging, deploys, retries, timeouts, health checks, CI or performance. It holds the 20 rules that apply to every project, a map of the detailed files, and the audit checklist. The detailed files carry the code examples, numbers and sources.

## Contents

1. File map: what to read when
2. The 20 rules
3. When writing new code
4. When auditing an existing codebase
5. Checks (summary)

## 1. File map: what to read when

| File | Read when |
|---|---|
| `error-handling-strategy.md` | Writing any function that can fail, an API error response, a React error boundary, crash reporting setup; auditing for swallowed errors or a mix of strategies |
| `logging-and-observability.md` | Adding logs, metrics, traces, alerts or SLOs; anything that might log user data or secrets |
| `resilience-patterns.md` | Any network call, DB call, retry, queue consumer, cache, fallback, rate limit, health check endpoint |
| `deploy-and-rollback.md` | Deploy config, migrations, feature flags, graceful shutdown, Dockerfiles, mobile releases and OTA updates |
| `testing-strategy.md` | Writing or reviewing tests, choosing what to mock, test DB setup, E2E (Playwright, Maestro), flaky tests |
| `ci-pipeline.md` | Creating or reviewing CI workflows for TS, Rust, full stack or Expo projects |
| `performance.md` | Anything slow, any optimization PR, budgets, profiling Node, Rust, web or React Native |
| `failure-patterns.md` | Design reviews of config pipelines, automation, destructive scripts, backups; writing a postmortem |

## 2. The 20 rules

**Errors**

1. **One error strategy per project, written down.** Expected outcomes are values (result unions, enums); operational failures and bugs are thrown / returned as errors with context. One error class file, stable error codes. Callers branch on codes, never on message text. (`error-handling-strategy.md` E1)
2. **Never swallow an error.** No empty catch, no `.catch(() => {})`, no `let _ =` on a `Result`, no "log and continue as if it worked". Handle it or propagate it with context; log it once, where it is handled. (E2, E3, E4)
3. **Validate at every trust boundary, including data your own systems generate.** Schema, size and count limits; on invalid input keep the last good version. Never `unwrap` or index unchecked on loaded data. (E8, E10; Cloudflare 2025, CrowdStrike 2024)
4. **Users get a safe, actionable message plus a request id; operators get the cause chain.** Never leak stacks, SQL, paths or secrets to users. (Section 4 of error handling)
5. **Crash on bugs, do not limp.** Uncaught exception: report, flush, exit, let the supervisor restart. Fail fast at startup on bad config. (E9, section 6)

**Observability**

6. **Structured logs with one canonical line per request and one request id end to end.** JSON to stdout, constant event names, fields for variables, emitted for failures too. (`logging-and-observability.md` L1 to L3)
7. **Never log secrets or personal data.** Redaction configured in the logger, secrets as types that print `[REDACTED]`, internal user ids instead of emails. (Section 3)
8. **Measure latency as histograms, alert on symptoms via SLO burn rate.** RED per endpoint, USE per resource, queue age, success latency separate from failure latency. Every page is urgent, actionable and user visible. (Sections 4 and 6)

**Resilience**

9. **Every remote call has a timeout, and deadlines propagate.** Including DB statements and pool acquisition. Timeout from the dependency's p99.9, not a guess. (`resilience-patterns.md` R1 to R5)
10. **Retry at one layer only, at most 3 attempts, capped exponential backoff with full jitter, within a retry budget, and only for retryable errors on idempotent operations.** (R6 to R12)
11. **Mutations that may be retried take an idempotency key; queue consumers are idempotent.** (R13 to R16)
12. **Bound everything and shed load early.** Concurrency limits, bounded queues and channels, page size limits, per tenant limits; reject cheaply with 503 and `Retry-After`. No fallback that piles load onto a shared dependency. (R17 to R27)
13. **Liveness checks the process only; readiness checks local health; dependency health drives alerts, not automatic removal.** (R28 to R33)

**Change**

14. **Every change is small, reversible with one command, exposed gradually, and rolled back automatically on alarm.** This includes config, flags, rules and data files, not only code. Roll back first, debug later. (`deploy-and-rollback.md` D1 to D6, D11)
15. **Old and new versions must coexist.** Formats change in two phases (read both, then write new); schemas change by expand, migrate, contract; Postgres migrations use `lock_timeout`, `CONCURRENTLY`, `NOT VALID`, batched backfills, bigint ids. (Sections 3 and 4)
16. **New risky code paths ship behind a flag, default off, with an owner and an expiry; kill switches work when your own tools are down.** (D12, D13, section 5)
17. **Shut down gracefully:** on SIGTERM flip readiness, wait for the load balancer, drain, flush telemetry, close pools, exit before the grace period. Exec form `CMD` so the signal arrives. (Section 6)

**Verification**

18. **Test behavior through public APIs against real dependencies you own.** Real Postgres per test (never SQLite or DB mocks), network mocked only at the boundary you do not own (MSW, wiremock), state assertions over interaction assertions, factories with defaults, injected clock. (`testing-strategy.md` T1 to T10, sections 6 and 7)
19. **Zero tolerance for flaky tests and red main.** Quarantine within a day with an owner, fix or delete within two weeks, never hide flakes behind unit test retries. CI runs format, lint (warnings fail), typecheck, tests with a real DB, build, on every push, in under 10 minutes, calling the same scripts developers run. (`testing-strategy.md` section 11, `ci-pipeline.md`)
20. **Measure before optimizing, against written budgets, in production like builds.** p75 web vitals (LCP 2.5 s, INP 200 ms, CLS 0.1), p99 API latency, bundle size in CI; profile with real tools, then change one thing. (`performance.md`)

## 3. When writing new code

Before finishing any change, walk this list for the code you touched:

- [ ] Every new failure is either a typed outcome the caller handles, or propagated with context. No new empty catch.
- [ ] Every new network or DB call has a timeout and is inside at most one retry layer.
- [ ] New mutating endpoints that clients may retry accept an idempotency key.
- [ ] New logs are structured, carry the request id, and contain no secrets or personal data.
- [ ] New list endpoints have a page size limit; new queues and channels are bounded.
- [ ] New migrations are backward compatible with the running code and lock safe.
- [ ] New user facing behavior is behind a flag if it is risky, with both states tested.
- [ ] Tests cover the behavior and at least one error path, run against a real DB where data is involved, and pass in random order.
- [ ] CI passes with zero warnings.

## 4. When auditing an existing codebase

Run the checks tables in each file. Report findings ranked by blast radius:

1. **Data loss or exposure**: swallowed errors on writes, secrets or PII in logs, untested backups, unsafe migrations, missing idempotency on payments.
2. **Fleet wide outage risk**: unvalidated runtime config, global non-code pushes, retries without backoff or at several layers, liveness checks on dependencies, no timeouts, unbounded queues, fallbacks onto the DB, 32 bit ids near overflow.
3. **Slow recovery**: no automatic rollback, no version in health checks, migrations on app start, no kill switches, SIGTERM not handled.
4. **Erosion**: mixed error strategies, flaky tests, mocks of owned code, warnings ignored in CI, no budgets.

For each finding give: the file and line, the rule number here, the concrete fix, and the check that proves the fix.

## 5. Checks (summary)

The full tables live in each file. The fastest high value probes:

| Check | Pass condition | Command |
|---|---|---|
| Swallowed errors | 0 unexplained | `rg -nU --type ts 'catch *(\([^)]*\))? *\{\s*\}' src`; `rg -n '\.catch\(\(\) *=> *(\{\s*\}|null)\)' src` |
| Floating promises | Lint clean | ESLint `@typescript-eslint/no-floating-promises: error` |
| Rust unwrap in prod code | Clippy clean | `cargo clippy --all-targets -- -D clippy::unwrap_used -D clippy::expect_used` |
| fetch without timeout | 0 | `rg -n 'fetch\(' src | rg -v signal` |
| Secrets in logs | 0 | `rg -n -i '(log|logger|console)\.\w+\(.*(password|token|secret|authorization)' src` |
| Liveness touches DB | No | `rg -n -A15 'livez|healthz|/health' src` and read |
| SIGTERM handled | Yes | `rg -n 'SIGTERM|with_graceful_shutdown' src` |
| Unsafe migrations | 0 | `squawk migrations/*.sql` |
| DB mocked in tests | 0 | `rg -n "(vi|jest)\.mock\(.*(db|prisma|pg|drizzle)" src tests` |
| Focused tests | 0 | `rg -n '\.only\(' src tests e2e` |
| CI warnings fail | Yes | `rg -n 'max-warnings=0|-D warnings' .github/workflows package.json` |
| Lockfile install | Yes | `rg -n 'npm ci|frozen-lockfile|--locked' .github/workflows` |
