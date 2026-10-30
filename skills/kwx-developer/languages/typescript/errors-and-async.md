# Errors and async

Read when: writing `try`/`catch`, `throw`, `async` functions, promise combinators, timeouts, retries, cancellation, or reviewing code for swallowed errors and floating promises.

## Contents

1. Throw only `Error` objects, with a cause
2. Expected failures vs bugs: exceptions or result values
3. Catching: narrow `unknown`, handle or rethrow, never swallow
4. Where errors are handled
5. Every promise is awaited, returned, or deliberately detached
6. `return await`
7. Concurrency: `all`, `allSettled`, `any`, `race`, and bounded pools
8. Cancellation and timeouts with `AbortSignal`
9. Retries
10. Unhandled rejections and process-level handlers
11. Events, streams and callbacks
12. Cleanup: `finally` and `using`
13. Checks

## 1. Throw only `Error` objects, with a cause

- `throw new Error(...)`, never `throw "msg"`, `throw { code }`, or `Promise.reject("x")`. Strings have no stack and break every `instanceof Error` check downstream. Lint: `@typescript-eslint/only-throw-error`, `prefer-promise-reject-errors`.
- When wrapping, pass the original as `cause` so the chain survives:

```ts
try {
  await db.insert(order);
} catch (err) {
  throw new Error(`Failed to save order ${order.id}`, { cause: err });
}
```

- Messages say what failed and with which identifiers, never secrets or full request bodies.
- Define a small set of error classes for conditions callers branch on. Give them a stable `code`; set `name`.

```ts
export class NotFoundError extends Error {
  override readonly name = "NotFoundError";
  readonly code = "NOT_FOUND";
  constructor(readonly resource: string, readonly id: string, options?: ErrorOptions) {
    super(`${resource} ${id} not found`, options);
  }
}
```

(With `erasableSyntaxOnly`, write the fields out instead of parameter properties: `readonly resource: string;` then assign in the constructor.)

- Branch on `instanceof` or `code`, never on `err.message.includes("...")`. Messages change; codes are contracts.
- Do not create one class per throw site. Three to eight classes cover most apps: validation, not found, conflict, unauthorized, forbidden, rate limited, upstream failure.

## 2. Expected failures vs bugs: exceptions or result values

Node best practices 2.3 separates two kinds:

| Kind | Examples | Handling |
|---|---|---|
| Operational (expected) | invalid input, not found, conflict, upstream 503, timeout | handled close to where they happen: return a 4xx, retry, show a message |
| Programmer (bug) | `undefined is not a function`, broken invariant, failed assertion | not handled locally: log with context, fail the request, and for unknown state crash and let the supervisor restart |

Choose one style for expected failures per layer and keep it:

- Exceptions with typed error classes (most JS/TS code, frameworks expect them).
- Result values for domain functions whose failures are part of the contract and must be handled by the caller:

```ts
type Result<T, E> = { ok: true; value: T } | { ok: false; error: E };

function parseCoupon(code: string): Result<Coupon, "expired" | "unknown" | "used"> { ... }

const r = parseCoupon(input);
if (!r.ok) return showCouponError(r.error); // the compiler forces the check
```

Do not mix both styles in one module, and do not wrap every function in `Result`: bugs still throw. Do not add a Result library for a handful of functions; the two-line union above is enough. If the repo already uses one (neverthrow, Effect), follow it.

## 3. Catching: narrow `unknown`, handle or rethrow, never swallow

`catch (err)` gives `unknown` under `strict` (`useUnknownInCatchVariables`). Anything can be thrown, so narrow:

```ts
try {
  await sync();
} catch (err) {
  if (err instanceof NotFoundError) return null;   // handled: a known, expected case
  throw err;                                        // everything else goes up unchanged
}
```

Rules:

- A `catch` either handles a specific known error, adds context and rethrows (with `cause`), or is the top-level handler. Nothing else.
- Empty `catch {}` needs a comment explaining why ignoring is correct (Google style guide). `catch { return null }` that turns every error into "not found" is a bug factory: the database being down now looks like an empty result.
- Do not log and rethrow at every layer; the same error appears five times in the logs. Log once, at the handler that decides the outcome.
- `.catch(() => {})` on a promise is swallowing. Same rule.
- `err.message` on `unknown` is a type error for a reason. Use `err instanceof Error ? err.message : String(err)` in the one place that formats errors.
- Promise `.catch` callbacks also receive `unknown`: `@typescript-eslint/use-unknown-in-catch-callback-variable`.

## 4. Where errors are handled

- One central error handler per process or app surface (HTTP error middleware, React error boundary, CLI `main().catch`), which logs, maps known errors to responses, and decides whether to crash (Node best practices 2.4).
- HTTP: map error classes to status codes in the handler (`NotFoundError` to 404, `ValidationError` to 400 with the issues, unknown to 500 with a generic message and a request ID). Never send stack traces or internal messages to clients (6.20).
- React: error boundaries catch render errors only. Event handler and async errors need their own handling (state plus UI message, or a reporting hook). Next.js App Router uses `error.tsx` per segment.
- CLIs: `main().catch((err) => { console.error(err); process.exitCode = 1; })`. Use `process.exitCode` rather than `process.exit()` so pending output flushes.

## 5. Every promise is awaited, returned, or deliberately detached

A promise nobody awaits ("floating") loses its errors and its timing: the function returns before the work is done, tests pass by accident, and a rejection becomes an unhandled rejection that crashes Node.

```ts
// Bad
async function onSave() {
  saveDraft(form);            // floating: errors vanish, ordering is undefined
  router.push("/done");
}

// Good
async function onSave() {
  await saveDraft(form);
  router.push("/done");
}

// Good, when fire-and-forget is the intent: say so and handle the error
void reportAnalytics(event).catch((err) => logger.warn({ err }, "analytics failed"));
```

- Lint: `@typescript-eslint/no-floating-promises` and `no-misused-promises` (both in `recommended-type-checked`). `no-misused-promises` catches async functions passed where a void callback is expected (`arr.forEach(async ...)`, `onClick={async () => ...}` returning a rejected promise nobody sees, `if (promise)` that is always truthy).
- `array.forEach(async (x) => ...)` never waits. Use `for...of` with `await` (sequential) or `await Promise.all(array.map(...))` (concurrent).
- `.then` callbacks must return the inner promise (MDN: otherwise it floats).
- `await` in a non-async callback is a syntax error; a missing `await` is not. Type-aware lint is the only reliable detector. `@typescript-eslint/require-await` flags `async` functions that never await (often a sign the `await` was forgotten somewhere).

## 6. `return await`

Inside `try`, `return await p` is required: `return p` leaves the `try` before `p` settles, so its rejection skips your `catch` and `finally` runs early. Outside `try`, `return await` also keeps the caller in async stack traces (Node best practices 2.12). typescript-eslint's `return-await` with `"error-handling-correctness-only"` (the `strict-type-checked` setting) enforces the `try` case; `"always"` enforces both.

## 7. Concurrency

| Need | Use | Behaviour to remember |
|---|---|---|
| Several independent operations, all must succeed | `Promise.all` | rejects on the first failure; the others keep running and their results are lost |
| Several independent operations, report each outcome | `Promise.allSettled` | never rejects; inspect `status` for each |
| First success wins (mirrors, fallbacks) | `Promise.any` | rejects with `AggregateError` only if all fail |
| First settled wins | `Promise.race` | mostly replaced by `AbortSignal.timeout`; a lost race does not cancel the loser |
| Many items (N unknown or large) | a bounded pool | unbounded `Promise.all(items.map(fetch))` on 10,000 items opens 10,000 sockets and gets you rate-limited |

Independent awaits in sequence are a latency bug:

```ts
// Bad: 3 round trips in sequence (sum of latencies)
const user = await getUser(id);
const orders = await getOrders(id);
const prefs = await getPrefs(id);

// Good: 1 round trip of wall time (max of latencies)
const [user, orders, prefs] = await Promise.all([getUser(id), getOrders(id), getPrefs(id)]);
```

`await` inside a loop is correct only when each step depends on the previous one or rate limits demand it. ESLint `no-await-in-loop` flags it; disable it per line with the reason.

A bounded pool without a dependency (use `p-limit` if the repo already has it):

```ts
async function mapPool<T, R>(items: readonly T[], limit: number, fn: (item: T) => Promise<R>): Promise<R[]> {
  const results = new Array<R>(items.length);
  let next = 0;
  async function worker(): Promise<void> {
    while (next < items.length) {
      const i = next++;
      results[i] = await fn(items[i] as T);
    }
  }
  await Promise.all(Array.from({ length: Math.min(limit, items.length) }, worker));
  return results;
}
```

## 8. Cancellation and timeouts with `AbortSignal`

Every network call and every long operation has a deadline. `fetch` has no default timeout; a hung upstream holds your request, socket and memory forever.

```ts
const res = await fetch(url, { signal: AbortSignal.timeout(5_000) });
```

- Accept `signal?: AbortSignal` as an option in your own async APIs and pass it down to every `fetch`, DB driver and child call that takes one. Check `signal.throwIfAborted()` between expensive steps.
- Combine a caller's signal with a deadline: `AbortSignal.any([callerSignal, AbortSignal.timeout(5_000)])`.
- Distinguish outcomes by `err.name`: `"TimeoutError"` from `AbortSignal.timeout`, `"AbortError"` from `controller.abort()`. A user-initiated abort is not an error to log or report.
- When implementing an abortable API, reject with `signal.reason` and remove listeners and timers on completion.
- React effects that fetch must abort or ignore stale responses in their cleanup (see react-and-react-native.md); otherwise a slow old response overwrites a newer one.
- Node: `import { setTimeout as sleep } from "node:timers/promises"` gives `await sleep(ms, undefined, { signal })`.
- Validate the response status before parsing: `fetch` resolves on 404 and 500. `if (!res.ok) throw new UpstreamError(res.status, url)`.

## 9. Retries

- Retry only operations that are idempotent (GET, PUT with the same body, POST with an idempotency key) and only on transient failures: network errors, timeouts, 408, 429, 502, 503, 504. Never retry 400, 401, 403, 404, 409, 422.
- Exponential backoff with full jitter and a cap: `delay = random(0, min(cap, base * 2 ** attempt))`, for example base 200 ms, cap 10 s, at most 3 to 5 attempts. Respect `Retry-After` on 429/503.
- The total time across retries stays inside the caller's deadline (pass the same `AbortSignal`).
- Retry at one layer only. Retries at the client, the SDK and the gateway multiply (3 x 3 x 3 = 27 calls).

## 10. Unhandled rejections and process-level handlers

- Node (15+) defaults to `--unhandled-rejections=throw`: an unhandled rejection becomes an uncaught exception and the process exits. Keep this default. It turns a silent bug into a visible crash.
- `process.on("unhandledRejection", ...)` replaces the default; if the handler does not rethrow or exit, rejections are "dropped on the floor and silently ignored" (MDN). If you register one, log and then exit.
- `process.on("uncaughtException")`: log with full context, flush, then exit with a non-zero code. Never continue after an unknown error: state may be corrupt (Node best practices 2.6). The platform (systemd, Kubernetes, the container runtime) restarts the process.
- Browser: report `window` `unhandledrejection` and `error` events to your error tracker once, globally.

## 11. Events, streams and callbacks

- `try/catch` does not catch errors emitted on an `EventEmitter` or stream. An `'error'` event without a listener crashes the process. Attach `'error'` listeners to every emitter you create or receive (Node best practices 2.13).
- Compose streams with `await pipeline(a, b, c)` from `node:stream/promises`, which propagates errors and destroys all streams. Never chain `.pipe()` (it does not forward errors or clean up).
- Wrap callback APIs with `util.promisify` or use the `node:fs/promises`-style promise APIs. Do not hand-write `new Promise` around something that already has a promise version.
- `new Promise(async (resolve, reject) => ...)`: never. An exception inside the async executor is lost. Lint: `no-async-promise-executor`.

## 12. Cleanup: `finally` and `using`

- Release resources (locks, file handles, DB clients from a pool, temp files) in `finally`, never only on the success path.
- Explicit resource management (`using` / `await using` with `Symbol.dispose` / `Symbol.asyncDispose`) is supported by TypeScript 5.2+ and shipped in V8 (Node 24+, Chrome 134+). Prefer it for pooled clients in new code when the runtime supports it; Safari support lags, so check before using it in browser code.

```ts
await using conn = await pool.connect(); // conn[Symbol.asyncDispose]() runs at scope exit, even on throw
await conn.query(sql);
```

## 13. Checks

- **No floating promises.** Pass: lint clean. Verify: `@typescript-eslint/no-floating-promises` and `no-misused-promises` enabled with typed linting; `npx eslint . --max-warnings 0`.
- **Only Error objects thrown.** Pass: lint clean; no string throws. Verify: `@typescript-eslint/only-throw-error`; `rg -nP "throw\s+['\"\`]" -t ts -t js .` returns nothing.
- **No swallowed errors.** Pass: every empty or blanket catch has a comment and a reason. Verify: `rg -nUP 'catch\s*(\([^)]*\))?\s*\{\s*\}' -t ts -t js .` and `rg -n '\.catch\(\(\) => (\{\s*\}|null|undefined)\)' -t ts -t js .`; ESLint `no-empty` (with `allowEmptyCatch: false`).
- **Wrapped errors keep a cause.** Pass: every `throw new X(...)` inside a `catch` passes `{ cause }`. Verify: ESLint `preserve-caught-error` (ESLint 9.35+, in `@eslint/js` recommended), configured with `errorClassNames` for the repo's own error classes.
- **No message sniffing.** Pass: no branching on error text. Verify: `rg -n '\.message\.(includes|startsWith|match)\(' -t ts -t js .`
- **Every fetch has a deadline.** Pass: each `fetch(` passes a `signal` or goes through a wrapper that adds one. Verify: `rg -n '\bfetch\(' -t ts -t js . | rg -v 'signal'` and inspect each hit.
- **No forEach with async.** Pass: zero hits. Verify: `rg -n 'forEach\(async' -t ts -t js .`
- **No sequential independent awaits in hot paths.** Pass: reviewed. Verify: ESLint `no-await-in-loop`; read functions with three or more consecutive `const x = await` lines.
- **`return await` inside try.** Pass: lint clean. Verify: `@typescript-eslint/return-await` set to `error-handling-correctness-only` or `always`.
- **Process handlers do not swallow.** Pass: any `unhandledRejection`/`uncaughtException` handler exits or rethrows. Verify: `rg -n -A6 "on\(['\"](unhandledRejection|uncaughtException)" -t ts -t js .`
- **Streams use pipeline.** Pass: no `.pipe(` chains in Node code. Verify: `rg -n '\.pipe\(' -t ts -t js -g '!**/*.{tsx,jsx}' .`
- **No async promise executor.** Pass: zero. Verify: `rg -n 'new Promise\(async' -t ts -t js .`; ESLint `no-async-promise-executor`.
