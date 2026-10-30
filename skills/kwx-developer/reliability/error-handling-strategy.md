# Error handling strategy

One project gets one error strategy, written down once and applied everywhere. Most error bugs are not a missing `try`. They are a mix of strategies (some code returns `null`, some throws, some returns `{ error }`), errors swallowed on the way up, and the same failure logged three times or not at all. This file gives the default strategy per stack, the rules that keep it honest, and how to detect a mix in an audit.

## Contents

1. The model: who is an error for
2. Default strategy per stack
3. Rules (E1 to E16)
4. User facing vs developer facing messages
5. React error boundaries and crash reporting
6. Process level: crash, do not limp
7. Detecting a mixed strategy (audit recipe)
8. Checks

## 1. The model: who is an error for

An error has two jobs, and they are different (Palmieri, Zero To Production, "Error handling in Rust"):

| Job | Consumer | Needs |
|---|---|---|
| Control flow | the calling code | a machine readable kind: enum variant, error class, error `code` string, HTTP status at the edge |
| Reporting | an operator (developer, on-call) | full context: what was being done, with which ids, the cause chain, a stack |
| Reporting | the end user | what happened in their terms, and what they can do next. Nothing internal |

Every design question below reduces to: does the caller need to act differently on this failure (make it a typed kind), or will it just give up and report (make it opaque with context)?

Three classes of failure, handled differently:

- **Expected domain outcomes**: not found, validation failed, insufficient funds, already exists. These are values. The caller must handle them. Never use exceptions or panics for them.
- **Operational failures**: network timeout, DB down, disk full, rate limited by a dependency. Expected to happen, not expected per call. Propagate with context, retry at one layer only (see `resilience-patterns.md`), report at the boundary.
- **Programmer errors (bugs)**: invariant broken, impossible state, null where the type said never. Crash the unit of work loudly. Do not try to recover inside the same process state (see section 6).

## 2. Default strategy per stack

### TypeScript / JavaScript (Node, web, React Native)

Default: **throw for operational failures and bugs, return values for expected domain outcomes.**

```ts
// Domain outcome: a discriminated union. The caller must narrow it.
type CreateUserResult =
  | { ok: true; user: User }
  | { ok: false; reason: "email_taken" | "invalid_email" };

export async function createUser(input: NewUser): Promise<CreateUserResult> {
  if (!isEmail(input.email)) return { ok: false, reason: "invalid_email" };
  try {
    const user = await db.insertUser(input);
    return { ok: true, user };
  } catch (err) {
    if (isUniqueViolation(err, "users_email_key")) return { ok: false, reason: "email_taken" };
    throw new Error(`createUser failed for email domain ${domainOf(input.email)}`, { cause: err });
  }
}
```

- Use one result shape for the whole project. If the project already uses `neverthrow`, `ts-results`, Effect or a house `Result<T, E>`, use that and nothing else. If it uses none, the plain discriminated union above needs no dependency.
- Throw only `Error` instances (or subclasses). Chain with `new Error(msg, { cause })` (ES2022, Node 16.9+), never by string concatenation of `err.message`, which loses the stack and the type.
- One error class hierarchy per project, in one file (`src/errors.ts` or `src/lib/errors.ts`), each with a stable `code` string. Callers branch on `code` or `instanceof`, never on `message` text.

```ts
export class AppError extends Error {
  constructor(
    readonly code: string,          // stable, machine readable: "PAYMENT_DECLINED"
    message: string,                // developer facing
    options?: { cause?: unknown; status?: number; expose?: boolean },
  ) {
    super(message, { cause: options?.cause });
    this.name = new.target.name;
    this.status = options?.status ?? 500;
    this.expose = options?.expose ?? false; // may the message reach the user?
  }
  readonly status: number;
  readonly expose: boolean;
}
```

### Rust

Default: **`Result` everywhere, typed enums where callers branch, opaque errors where callers only report.** The common myth "anyhow for applications, thiserror for libraries" is the wrong framing; reason about intent (Palmieri):

- The caller will behave differently per failure mode: a `thiserror` enum with one variant per mode.
- The caller will only give up and report: an opaque error (`anyhow::Error`, `eyre::Report`) with `.context("what we were doing")`.

```rust
#[derive(Debug, thiserror::Error)]
pub enum CheckoutError {
    #[error("cart {0} is empty")]
    EmptyCart(CartId),
    #[error("payment declined: {reason}")]
    Declined { reason: String },
    #[error(transparent)]
    Unexpected(#[from] anyhow::Error), // everything the caller cannot act on
}
```

- `#[from]` on a low level error type (`#[from] sqlx::Error`) leaks the dependency into your API and makes every DB error look the same. Wrap low level errors with context first, then convert.
- `unwrap()` and `expect()` are allowed only in tests, in `main` before serving starts (config parsing), and on invariants that are truly impossible, with `expect("why this cannot fail")`. Cloudflare's 18 Nov 2025 global outage was a `Result::unwrap()` on a config file that exceeded a 200 feature limit (see `failure-patterns.md`).
- Index with `.get(i)` on data that came from outside the process. CrowdStrike's July 2024 crash was an out of bounds read of a 21st input when only 20 were supplied.

### Postgres / SQL boundary

Map database errors by SQLSTATE, not by message: `23505` unique violation, `23503` foreign key violation, `23514` check violation, `40001` serialization failure (retry the transaction), `40P01` deadlock (retry), `57014` query canceled (statement timeout). Constraint name tells you which rule: branch on it (`users_email_key`) rather than on text.

## 3. Rules

**E1. One strategy, written in one place.** The project has a short section (in `CLAUDE.md`, `CONTRIBUTING.md` or `src/errors.ts` header) saying: what is a value, what is thrown, the error class file, the result type, where errors are logged. New code follows it. Check: section 7.

**E2. Never swallow.** An empty `catch {}`, `.catch(() => {})`, `.catch(() => null)`, `let _ = fallible();`, `.ok();` with no comment, or `try { } catch (e) { console.log(e) }` that then continues as if it succeeded, is a defect. Allowed only with a one line comment saying why the failure is irrelevant (for example: "best effort cache warm, miss is fine"), and even then count it in a metric.

```ts
// Bad: the user sees "saved" while nothing was saved
try { await save(draft); } catch (e) { console.error(e); }
toast("Saved");

// Good
try { await save(draft); toast("Saved"); }
catch (err) { reportError(err, { draftId: draft.id }); toast("Could not save. Your text is still here, try again."); }
```

**E3. Handle or propagate, never both log and rethrow.** Log an error exactly once, where it is finally handled (the request boundary, the job runner, the error boundary). Code in the middle adds context and propagates. Logging at every layer produces three stack traces for one failure and makes error counts lie (Palmieri: "errors should be logged when they are handled").

**E4. Add context when crossing a layer.** Each layer that propagates says what it was doing and with which ids: `cause` in TS, `.context()` / `.with_context()` in Rust, `%w` in Go. The final report reads as a chain: "checkout failed for cart 9f2 -> charge card failed -> stripe timeout after 10s".

**E5. Catch narrowly.** Catch the specific error you can handle, rethrow the rest. A `catch (e)` that maps every error to "not found" turns a DB outage into silent data loss.

```ts
try { return await repo.get(id); }
catch (err) {
  if (err instanceof NotFoundError) return null; // only this one is expected
  throw err;
}
```

**E6. `catch (err)` has type `unknown`.** Turn on `useUnknownInCatchVariables` (part of `strict`). Narrow before reading `.message`. Thrown values in JS can be anything; libraries throw strings.

**E7. No floating promises.** Every promise is awaited, returned, or explicitly handed to an error handler. An unawaited promise that rejects is an unhandled rejection, which kills a Node process (default since Node 15) or vanishes silently in a browser. Lint: `@typescript-eslint/no-floating-promises`, `@typescript-eslint/no-misused-promises`.

**E8. Validate at the trust boundary, then trust the types.** Parse external input (HTTP body, env, config files, queue messages, files your own pipeline generated) with a schema (zod, valibot, serde with `deny_unknown_fields` where appropriate) at entry. Return a 400-class error with field paths. Inside, do not re-validate defensively. Treat internally generated config and data files exactly like user input: Cloudflare (2025) and CrowdStrike (2024) both crashed fleets on files their own systems produced.

**E9. Fail fast at startup.** Missing env var, unreachable required config, bad migration state: crash on boot with a clear message, before the health check reports ready. Never start serving with a default that silently changes behavior (`PORT ?? 3000` is fine; `STRIPE_KEY ?? ""` is not).

**E10. Bound everything that can grow, and decide what happens at the bound.** Every limit (max features, max payload, max items in a batch) has an explicit behavior when exceeded: reject the new input and keep the last good one, truncate with a metric, or refuse to start. Never panic or crash the request loop on it.

**E11. Retryable is a property of the error, decided where it is created.** The error carries `retryable: boolean` (or a kind that implies it). 4xx validation is never retryable; 429 and 503 are retryable with backoff; a timeout on a non-idempotent write is retryable only with an idempotency key. See `resilience-patterns.md`.

**E12. Error paths are code paths: test them.** Every handled error kind has at least one test that triggers it (bad input, dependency returns 500, dependency times out, unique violation). The error path you never run is the one that breaks in the incident.

**E13. Do not invent fallbacks for critical failures.** "If the cache fails, query the DB directly" turned a partial Amazon outage into a full site outage (AWS Builders' Library, "Avoiding fallback"). Prefer: let the caller handle it, or fail the request. If a degraded mode is needed, run it continuously (failover), not only during failure.

**E14. Status codes at the HTTP edge are part of the contract.** 400 bad input (with field errors), 401 not authenticated, 403 not allowed, 404 not found (also for "exists but you may not see it"), 409 conflict, 422 semantic validation if the project already uses it, 429 rate limited with `Retry-After`, 500 bug, 502/503/504 dependency or overload with `Retry-After` when known. Never 200 with `{ error }` in the body. Never 500 for a client mistake (it pages someone and pollutes error budgets).

**E15. One error response body shape for the whole API.** Pick RFC 9457 problem details (`type`, `title`, `status`, `detail`, `instance`) or a house shape, and use it for every error including framework 404s and validation failures. Include the request id so a user report can be traced.

```json
{ "type": "https://example.com/errors/payment-declined", "title": "Payment declined",
  "status": 402, "detail": "Your card was declined. Try another card.",
  "code": "PAYMENT_DECLINED", "requestId": "req_8f2a1c" }
```

**E16. In React, async and event handler errors need their own handling.** Error boundaries catch errors thrown during rendering, in lifecycle methods and constructors below them. They do not catch errors in event handlers, in async code (`setTimeout`, promises, `fetch` callbacks), in server rendering, or in the boundary itself. Data fetching libraries (TanStack Query `throwOnError`, React Router `errorElement`, Next.js `error.tsx`) are the way to route async failures into a boundary.

## 4. User facing vs developer facing messages

- **User message**: what happened in their words, whether their data is safe, what to do next. No stack, no SQL, no class names, no "Error: undefined". The user message is chosen by the code that knows the user context (the UI or the API edge), from the error `code`, not from `err.message`.
- **Developer message**: the cause chain, ids, inputs (sanitized), the stack. Goes to logs and the crash reporter only.
- Only errors flagged `expose: true` (validation messages, domain outcomes) may forward their text to the user. Everything else becomes a generic message plus the request id: "Something went wrong on our side. Reference req_8f2a1c."
- Never put secrets, tokens, SQL or file paths in a message that could be exposed. Error messages end up in browser consoles, screenshots and support tickets.
- Write user messages that keep the user's work: "Could not save. Your changes are still here." beats "Save failed."

## 5. React error boundaries and crash reporting

**Placement.** One boundary at the root (last resort, full page fallback with a reload button), one per independent region (route, sidebar, widget) so one broken panel does not blank the page. Do not wrap every component.

```tsx
import * as Sentry from "@sentry/react";

<Sentry.ErrorBoundary
  fallback={({ resetError }) => <PanelError onRetry={resetError} />}
  beforeCapture={(scope) => scope.setTag("region", "billing")}
>
  <BillingPanel />
</Sentry.ErrorBoundary>
```

- Function components cannot be boundaries; use `react-error-boundary` or the Sentry component rather than writing a class each time.
- React 19: pass `onUncaughtError`, `onCaughtError`, `onRecoverableError` to `createRoot` (Sentry provides `reactErrorHandler()`), so errors caught by boundaries are still reported. In production React does not bubble caught errors to `window.onerror`.
- Reset the boundary on navigation (`resetKeys={[location.pathname]}`), or the user is stuck on the fallback.

**Crash reporting (Sentry or equivalent) minimum setup:**

- `release` set to the git SHA of the build, `environment` set (`production`, `staging`, `preview`). Without `release`, regressions cannot be tied to a deploy.
- Source maps uploaded for every web and React Native (Hermes) build, and not served publicly unless intended. A minified stack is close to useless.
- `sendDefaultPii` stays `false` (the default). Scrub in `beforeSend` / `beforeBreadcrumb` (auth headers, cookies, tokens, form values), and turn on server side scrubbing as a second layer.
- Report from the same place the error is handled (rule E3), not from every catch.
- Node: also capture `unhandledRejection` and `uncaughtException` (the SDK does this), then exit.
- Mobile: native crashes (`@sentry/react-native` captures both JS and native), and record breadcrumbs for navigation, not for every keystroke.
- Alert on new issue types and on regressions after a release, not on every event.

## 6. Process level: crash, do not limp

- Node: on `uncaughtException`, log, flush the reporter, and `process.exit(1)`. The process state is unknown after an uncaught exception; the Node docs say resuming is not safe. Let the supervisor (systemd, Kubernetes, PM2) restart it.
- Keep `--unhandled-rejections=throw` (Node 15+ default). Never set it to `warn` or `none` to "fix" crashes.
- Rust services: a panic in a request task should not take down the server. Axum/tower: `CatchPanicLayer`; tokio tasks: `JoinHandle` returns `Err` on panic, so check it. But a panic in a shared component (config loader, worker loop) should abort the process with `panic = "abort"` only if a supervisor restarts it.
- A crash loop is a signal, not a solution: alert on restart count.
- Workers and queue consumers: an exception processing one message must not kill the consumer loop. Catch at the loop, report, apply the retry or dead letter policy, continue (see `resilience-patterns.md`).

## 7. Detecting a mixed strategy (audit recipe)

Run these and compare counts per folder. A healthy project has one dominant pattern per row and clear reasons for the exceptions.

```bash
# TS: how do functions signal failure?
rg -n --type ts 'return \{ *(ok|success): *false' src | wc -l          # result objects
rg -n --type ts 'return \{ *error:' src | wc -l                        # ad hoc { error }
rg -n --type ts 'throw new \w+Error\(' src | wc -l                     # thrown classes
rg -n --type ts 'throw ["`'"'"']' src                                  # thrown strings (always a defect)
rg -n --type ts 'return null; *// *(error|fail)' src                   # null as error
rg -n --type ts 'class \w+ extends Error' src                          # error classes: should live in one file

# TS: swallowed errors
rg -nU --type ts 'catch *(\([^)]*\))? *\{\s*\}' src
rg -n --type ts '\.catch\(\(\) *=> *(\{\s*\}|null|undefined|\[\])\)' src
rg -n --type ts 'catch *\((\w+)\) *\{\s*console\.(log|error)\(\1\);?\s*\}' src

# TS: branching on message text
rg -n --type ts '\.message *(===|\.includes|\.startsWith|match)' src

# Rust: unwrap/expect outside tests, discarded results
rg -n --type rust '\.unwrap\(\)|\.expect\(' src | rg -v '#\[cfg\(test\)\]|tests?/'
rg -n --type rust 'let _ = .*\?|let _ = .*\(.*\);|\.ok\(\);' src

# Rust: error types, should be few and consistent
rg -n --type rust '#\[derive\([^)]*Error' src
rg -n --type rust 'Box<dyn (std::error::)?Error' src
```

Report format for each finding: the folder, the dominant pattern, the deviating files, and the fix (convert to the dominant pattern). Mixed patterns across layers are fine only when the rule is explicit (for example: repositories throw, services return results, routes map results to status codes).

## 8. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| Strategy written down | Error section exists in project docs or `errors.ts` header | `rg -il 'error handling' CLAUDE.md CONTRIBUTING.md docs src/errors.ts` |
| No empty catch | 0 hits, or each has a reason comment | ESLint `no-empty` (with `allowEmptyCatch: false`); rg in section 7 |
| No floating promises | Lint clean | `@typescript-eslint/no-floating-promises: error`, `no-misused-promises: error` |
| Only Error objects thrown | Lint clean | `@typescript-eslint/only-throw-error`, `prefer-promise-reject-errors` |
| `catch` var is unknown | `strict: true` or `useUnknownInCatchVariables: true` | `rg '"strict": *true' tsconfig*.json` |
| Errors chained with cause | No `throw new Error(\`...${err.message}\`)` | `rg 'new Error\(.*\$\{\w+\.message\}' src` returns 0 |
| No message-text branching | 0 hits | `rg '\.message *(===|\.includes)' src` |
| One error class file | All `extends Error` in one module (or one per bounded context) | `rg -l 'extends Error' src` |
| Rust: no unwrap in prod paths | Clippy clean | `cargo clippy -- -D clippy::unwrap_used -D clippy::expect_used` (allow in tests via `clippy.toml` `allow-unwrap-in-tests = true`) |
| Rust: no unchecked indexing on external data | Reviewed | `cargo clippy -- -W clippy::indexing_slicing` on parsing modules |
| Logged once | No `log + throw` pairs | `rg -nU 'console\.error\([^)]*\);\s*throw' src`; `rg -nU 'error!\(.*\);\s*(return Err|Err\()' src` |
| Error responses uniform | Every error route returns the one shape | Integration test hits 400, 404, 500 paths and validates the body schema |
| HTTP 200 never carries an error | 0 hits | `rg "status\(200\).*error|json\(\{ *error" src` |
| Crash reporter has release + source maps | Release equals git SHA; a test error shows a symbolicated stack | Check SDK init for `release`; CI step uploads maps |
| PII off in reporter | `sendDefaultPii` absent or false; `beforeSend` scrubs | `rg 'sendDefaultPii' src` |
| Error boundaries placed | Root + per region; reset on route change | `rg -n 'ErrorBoundary' src` |
| uncaughtException exits | Handler ends in `process.exit(1)` | `rg -n -A5 "uncaughtException" src` |
| Error paths tested | Each error `code` appears in at least one test | `for c in $(rg -o '"[A-Z_]{4,}"' src/errors.ts); do rg -q "$c" tests src/**/*.test.ts || echo "untested $c"; done` |
