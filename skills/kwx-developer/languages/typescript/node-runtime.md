# Node.js runtime

Read when: writing or reviewing server code, CLIs, workers or scripts that run on Node.js (also mostly true for Bun and Deno in Node-compat mode). Module format rules are in modules-imports-exports.md section 9; error rules in errors-and-async.md.

## Contents

1. Versions and running TypeScript
2. Project structure for a service
3. Configuration and environment
4. Process lifecycle: crash on unknown errors, shut down gracefully
5. Do not block the event loop
6. HTTP clients and servers
7. Logging and observability
8. Security defaults
9. Dependencies and installs
10. Built-ins before packages
11. Checks

## 1. Versions and running TypeScript

- Run an Active LTS release in production (Node best practices 5.17). As of October 2026: Node 24 is LTS, Node 26 enters LTS this month, Node 22 is in maintenance. Odd versions are never LTS. Pin it in three places that agree: `package.json` `"engines": { "node": ">=24" }`, `.nvmrc` or `.node-version`, and the Docker base image / CI matrix.
- Node runs `.ts` files directly by stripping types: on by default since 22.18 / 23.6, stable since 24.12 / 25.2. It does no type checking, ignores `tsconfig.json` (so no `paths`, no downlevelling), rejects enums, runtime namespaces, parameter properties and decorators, requires explicit `.ts` extensions in imports and `import type` for types, refuses `.ts` under `node_modules`, and does not support `.tsx`.
- So for a Node service: either run `node src/main.ts` with type stripping (tsconfig from types-and-strictness.md with `erasableSyntaxOnly`, `rewriteRelativeImportExtensions`), or compile with `tsc` to `dist/` and run JavaScript. Use `tsx` only when you need tsconfig `paths`, decorators or JSX at runtime. In every case run `tsc --noEmit` in CI: stripping runs code with type errors.
- Useful built-in flags: `--env-file=.env` (stable in 24.10+), `--watch` for dev, `--test` (built-in runner), `--permission` with `--allow-fs-read`/`--allow-fs-write` to sandbox scripts.

## 2. Project structure for a service

- Organise by business component first (`src/orders/`, `src/billing/`), each with its own API layer, domain logic and data access (Node best practices 1.1).
- Inside each, three layers that only call downward: entry points (HTTP routes, queue consumers, CLI commands), domain services (plain functions on plain types), data access (DB, external APIs). The web framework's `req`/`res` never reach the domain layer (1.2): the route parses input into a typed object and calls `createOrder(input)`.
- Composition root: one `main.ts` builds config, logger, DB pool, HTTP server and wires dependencies by passing them as arguments. No module-level singletons that connect on import.
- Keep the HTTP app factory (`createApp(deps)`) separate from `listen()`, so tests can start the app on an ephemeral port or call it in-process.

## 3. Configuration and environment

- Parse and validate all env vars once at startup (validation-at-boundaries.md); fail fast with a message listing every missing or invalid variable.
- `process.env` is read only in the config module. Everywhere else receives typed config.
- `NODE_ENV=production` in production (5.15): frameworks and libraries switch off dev checks with it. But do not branch business logic on `NODE_ENV`; use explicit config flags.
- Secrets come from the environment or a secret manager, never from committed files. `.env` files are for local development, gitignored, with a committed `.env.example` listing every key.

## 4. Process lifecycle: crash on unknown errors, shut down gracefully

- Do not keep running after an unknown error (programmer error, `uncaughtException`). Log it with context and exit non-zero; the supervisor (systemd, Kubernetes, ECS, the PaaS) restarts the process (2.6, 5.5). Do not run a second process manager (PM2) inside a container that already has one.
- Leave `--unhandled-rejections` at its default (`throw`).
- Graceful shutdown on `SIGTERM` and `SIGINT`: stop accepting new work, finish in-flight work with a deadline, close resources, exit.

```ts
// main.ts
const server = app.listen(config.port);
let shuttingDown = false;

async function shutdown(signal: string): Promise<void> {
  if (shuttingDown) return;
  shuttingDown = true;
  logger.info({ signal }, "shutting down");
  const force = setTimeout(() => {
    logger.error("shutdown timed out, forcing exit");
    process.exit(1);
  }, 10_000);
  force.unref();
  try {
    await new Promise<void>((resolve, reject) => server.close((err) => (err ? reject(err) : resolve())));
    await queueConsumer.stop();
    await db.end();
    process.exitCode = 0;
  } catch (err) {
    logger.error({ err }, "error during shutdown");
    process.exitCode = 1;
  }
}

process.once("SIGTERM", () => void shutdown("SIGTERM"));
process.once("SIGINT", () => void shutdown("SIGINT"));
```

- `server.close()` waits for keep-alive connections; on Node 19+ idle keep-alive sockets are closed automatically, and `server.closeAllConnections()` exists for the forced path.
- Make the shutdown timeout shorter than the orchestrator's grace period (Kubernetes default `terminationGracePeriodSeconds` is 30 s).
- Health endpoints: liveness (`/healthz`: the process responds) and readiness (`/readyz`: dependencies reachable, not shutting down). Return not-ready as soon as shutdown starts so the load balancer stops sending traffic.
- In Docker, run `node` as PID 1 directly (`CMD ["node", "dist/main.js"]`), not through `npm start`, which does not forward signals; or use `--init`/tini.

## 5. Do not block the event loop

Node runs all JavaScript on one thread. One slow callback delays every other request. From the Node docs, "Don't block the event loop":

- Keep each callback short and bound its input size. An O(n) handler on a client-controlled n is a denial-of-service.
- `JSON.stringify` of a 50 MB object takes about 0.7 s and `JSON.parse` about 1.3 s, all blocking. Limit request body size (for example 1 MB default, more only on specific routes) and stream large payloads.
- Never use synchronous APIs on a server path: `fs.*Sync`, `crypto.pbkdf2Sync`, `crypto.randomFillSync`, `zlib.*Sync`, `child_process.execSync`/`spawnSync`. They are fine in CLIs and startup code.
- ReDoS: regexes with nested quantifiers (`(a+)*`, `(\/.+)+$`), overlapping alternation (`(a|a)*`) or backreferences can take exponential time on crafted input. Use plain string methods for simple matching, cap input length before matching, and lint with `eslint-plugin-regexp` / `security/detect-unsafe-regex`.
- CPU-heavy work (image processing, large CSV, hashing in bulk) goes to `worker_threads` (a pool such as `piscina`) or a separate service. Do not spawn a child process per request.
- Password hashing uses the async APIs (`crypto.scrypt`, `argon2` async) because they run on the libuv pool (default 4 threads, `UV_THREADPOOL_SIZE`).
- Measure event loop delay in production (`perf_hooks.monitorEventLoopDelay()`); alert when p99 exceeds about 100 ms.

## 6. HTTP clients and servers

- Use the built-in `fetch` (undici) for outgoing HTTP. Every call has a timeout (`AbortSignal.timeout`), checks `res.ok`, and parses the body with a schema.
- Always consume or cancel the response body (`await res.text()` or `res.body?.cancel()`), or the connection is not returned to the pool.
- Reuse connections: one client per upstream; do not create a new agent per request.
- Server frameworks: use whatever the repo has. For new services, Fastify (schema validation, fast, good TypeScript) or Hono (web-standard `Request`/`Response`, runs on Node, Bun, edge) are sound defaults; Express 5 if the team knows it (it now forwards rejected promises from async handlers to error middleware).
- Set server timeouts deliberately: `requestTimeout`, `headersTimeout`, `keepAliveTimeout` above the load balancer's idle timeout (AWS ALB 60 s) to avoid 502s from reused dead connections.
- Return consistent error bodies (`{ error: { code, message } }`) with correct status codes; never stack traces.

## 7. Logging and observability

- Use a structured JSON logger (pino) writing to stdout; the platform ships logs (5.18). No `console.log` in server code.
- Every log line in a request carries a request ID; propagate it with `AsyncLocalStorage` and to downstream calls in a header (5.14). Prefer OpenTelemetry for traces when the platform supports it.
- Log errors as objects (`logger.error({ err }, "msg")`) so the stack and `cause` chain serialize; never `logger.error(err.message)`.
- Never log secrets, tokens, passwords, full card numbers or whole request bodies. Configure redaction paths (`redact: ["req.headers.authorization", "*.password"]`).
- Levels: `error` needs a human, `warn` is unexpected but handled, `info` is lifecycle and business events, `debug` is off in production.

## 8. Security defaults

From Node best practices section 6 and the Node docs:

- No `eval`, `new Function`, `vm` on untrusted input (`vm` is not a security boundary).
- Child processes: `execFile`/`spawn` with an argument array, never `exec` with a string built from input (shell injection).
- File paths from input: resolve and check they stay inside the allowed root (`path.resolve(root, input).startsWith(root + path.sep)`); reject `..` and absolute paths.
- Queries: parameterized only (tagged template SQL clients, ORM methods). No string concatenation into SQL.
- Limit payload size and rate (6.2, 6.14); set security headers (helmet or framework equivalent) on HTML responses.
- Hash passwords with argon2id or scrypt (bcrypt acceptable in existing code); compare secrets with `crypto.timingSafeEqual`.
- Run as a non-root user in containers (6.13). Do not publish `.env` or secrets to npm (`files` allowlist in `package.json`).
- Redirect targets from input must be checked against an allowlist (6.24).
- Prototype pollution: do not deep-merge untrusted objects into config; parse input with a schema (which builds fresh objects) and use `Object.create(null)` or `Map` for dictionaries keyed by user input.

## 9. Dependencies and installs

- One package manager per repo, one lockfile, committed (5.4). Declare it in `"packageManager"`. CI installs with the frozen command: `npm ci`, `pnpm install --frozen-lockfile`, `yarn install --immutable`, `bun install --frozen-lockfile`.
- Before adding a dependency: is it in the platform (section 10)? Is it maintained (release in the last year), typed, ESM-compatible, small? Can it be 20 lines of code instead?
- Run `npm audit` (or `pnpm audit`) in CI and enable automated update PRs (Renovate, Dependabot). Remove unused dependencies (`npx knip`).
- `devDependencies` must not be imported by production code (knip reports it; dependency-cruiser `not-to-dev-dep`).

## 10. Built-ins before packages

| Need | Use | Not |
|---|---|---|
| HTTP client | `fetch` | axios, node-fetch, request |
| Test runner (small libs, scripts) | `node:test` + `node:assert` | adding Jest to a 3-file package |
| Env files | `--env-file` / `process.loadEnvFile()` | dotenv in new code |
| UUID | `crypto.randomUUID()` | uuid v4 |
| Deep clone | `structuredClone` | lodash.clonedeep |
| Sleep, timers | `node:timers/promises` | custom promise wrappers |
| Arg parsing | `util.parseArgs` | yargs for simple CLIs |
| Glob | `fs.glob` (Node 22+) | glob package in new code |
| SQLite | `node:sqlite` (check stability for your version) | adding a native module for a small tool |
| Watch mode | `node --watch` | nodemon |
| Array/object helpers | native (`Object.groupBy`, `Array.prototype.toSorted`, `Set` methods) | lodash for one function (7.2) |

## 11. Checks

- **LTS pinned consistently.** Pass: `engines.node`, `.nvmrc`/`.node-version`, Dockerfile `FROM node:` and CI agree on an even major. Verify: `rg -n '"node":' package.json; cat .nvmrc .node-version 2>/dev/null; rg -n 'FROM node:|node-version' Dockerfile* .github/workflows 2>/dev/null`
- **Typecheck in CI even with type stripping.** Pass: CI runs `tsc --noEmit`. Verify: `rg -n 'tsc' .github/workflows package.json`
- **No sync APIs on request paths.** Pass: `*Sync(` only in startup, scripts or CLIs. Verify: `rg -n '\w+Sync\(' -t ts -t js src | rg -v '(scripts|cli|bin)/'`
- **No console in server code.** Pass: zero `console.` in `src` of a service (logger only). Verify: `rg -n '\bconsole\.(log|info|debug|warn|error)\(' -t ts src`; ESLint `no-console`.
- **Graceful shutdown present.** Pass: handlers for `SIGTERM` that close the server and pools. Verify: `rg -n "SIGTERM" -t ts -t js .`
- **No shell string exec.** Pass: no `exec(`/`execSync(` with template strings or concatenation. Verify: `rg -nP '\bexec(Sync)?\((`|[^)]*\+)' -t ts -t js .`
- **No eval.** Pass: zero. Verify: `rg -nP '\beval\(|new Function\(' -t ts -t js .`
- **No SQL concatenation.** Pass: zero string-built queries. Verify: `rg -nP '(query|execute|raw|unsafe)\((\x60[^\x60]*\$\{|["\x27][^"\x27]*["\x27]\s*\+)' -t ts -t js .` and review; note that tagged templates (sql\`...\`) are safe.
- **Frozen installs in CI.** Pass: CI uses `npm ci` or the frozen flag. Verify: `rg -n 'npm ci|--frozen-lockfile|--immutable' .github/workflows 2>/dev/null`
- **One lockfile.** Pass: exactly one of `package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`, `bun.lock`/`bun.lockb` at the root. Verify: `ls package-lock.json pnpm-lock.yaml yarn.lock bun.lock bun.lockb 2>/dev/null`
- **Non-root container.** Pass: Dockerfile sets `USER node` (or another non-root user). Verify: `rg -n '^USER ' Dockerfile*`
- **Signals reach Node.** Pass: Docker `CMD` runs `node` directly or uses an init. Verify: `rg -n '^(CMD|ENTRYPOINT)' Dockerfile*`
