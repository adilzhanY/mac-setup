# TypeScript and JavaScript: master file

Scope: TypeScript and JavaScript in Node.js, browsers, React, React Native and Next.js. Read this file first for any JS/TS task, then open only the topic files the router names.

## Contents

1. Step zero: read the repo before writing
2. The 20 rules that matter most
3. Router: which file to read
4. Version facts (October 2026)
5. Checks

## 1. Step zero: read the repo before writing

Conventions already in the repo beat every default in these files. Spend one minute measuring them, then match them. Run from the repo root (always pass a path to `rg`; with none it reads stdin and hangs in agent shells):

```bash
cat package.json | head -60                                   # type, scripts, engines, packageManager, deps
ls *lock* bun.lock* 2>/dev/null                               # package manager
ls tsconfig*.json jsconfig.json eslint.config.* biome.json* .oxlintrc.json .prettierrc* 2>/dev/null
npx tsc --showConfig 2>/dev/null | head -40                    # effective compiler options
rg -c '^export default ' -t ts -t js . | wc -l                # files with default exports
rg -l '^export ' -t ts -t js . | wc -l                        # files with any export
rg -o "from ['\"](@/|#/|~/|src/)" -t ts -t js -I . | sort | uniq -c   # alias roots in use
rg -o '"(zod|valibot|yup|joi|dayjs|date-fns|luxon|moment|axios|ky|zustand|@reduxjs/toolkit|jotai|@tanstack/react-query|swr)"' -g 'package.json' -g '!**/node_modules/**' . | sort | uniq -c
```

Then decide: framework (Next.js, Vite, Expo, plain Node), module format, strictness, lint and format tools, test runner, validation, date and state libraries. Use what exists. If two tools do one job, or a folder mixes conventions, do not add a third: follow the majority in the folder you touch and report the mix (codebase-audit.md).

## 2. The 20 rules that matter most

Each rule names the file with details and the check that proves it.

1. **Match the repo, then improve it on purpose.** Existing conventions win. Fix a convention mix only in a dedicated change with a lint rule that stops it returning. (codebase-audit.md)
2. **Strict compiler, no exceptions.** `strict`, `noUncheckedIndexedAccess`, `verbatimModuleSyntax`, `erasableSyntaxOnly`, `noImplicitOverride`. Never turn a strict member off to get green. Check: `npx tsc --showConfig`. (types-and-strictness.md 1 and 2)
3. **No `any`.** Unknown data is `unknown` and gets parsed or narrowed. Check: `no-explicit-any`, `no-unsafe-*`. (types-and-strictness.md 3)
4. **Never use `as` or `!` to silence an error.** Fix the type, narrow, parse, or write a real type guard; a remaining cast carries a comment saying why it is true. Check: grep in types-and-strictness.md 17. (section 4)
5. **Parse every trust boundary with a schema, and derive the type from it.** HTTP bodies, params, env, storage, third-party responses, server actions, LLM output. Bound every string and array. Check: no `.json()` result used without `.parse`. (validation-at-boundaries.md)
6. **Make wrong states unrepresentable.** Discriminated unions, not bags of optional fields; brands for IDs and units; exhaustive `switch` with a `never` check. Check: `switch-exhaustiveness-check`. (types-and-strictness.md 5 to 7)
7. **Named exports only**, except files a framework requires to default-export. Check: `import-x/no-default-export` with overrides. (modules-imports-exports.md 2)
8. **No barrel files inside an app.** Import the defining file; packages expose one entry through `package.json` `exports`. Check: barrel grep. (modules-imports-exports.md 3 and 4)
9. **One alias root, `#/` subpath imports preferred, no `baseUrl`, no `../../../`.** Check: alias grep. (modules-imports-exports.md 5)
10. **ESM everywhere**: `"type": "module"`, `node:` prefix for builtins, extensions on relative imports for Node targets, no `require` in TS. (modules-imports-exports.md 9)
11. **Every promise is awaited, returned, or deliberately `void`ed with a `.catch`.** No `forEach(async`. Check: `no-floating-promises`, `no-misused-promises`. (errors-and-async.md 5)
12. **Throw only `Error` objects; wrap with `{ cause }`; never swallow.** A `catch` handles a specific case, adds context and rethrows, or is the top-level handler. Check: `only-throw-error`, `preserve-caught-error`, empty-catch grep. (errors-and-async.md 1 to 4)
13. **Every network call has a deadline and checks status.** `AbortSignal.timeout`, `res.ok`, retries only for idempotent calls with backoff and jitter. Independent awaits run in parallel; large fan-outs use a bounded pool. (errors-and-async.md 7 to 9)
14. **React: derive, do not sync.** No Effect that sets state from props or state; Effects only for external systems, with cleanup. Server data lives in a cache, not `useState`. Check: `eslint-plugin-react-hooks` recommended. (react-and-react-native.md 3 to 5)
15. **Next.js: Server Components by default, `"use client"` at the leaves, and every server action validates, authenticates and authorizes the resource itself.** Secrets only in `server-only` modules; minimal DTOs cross to the client. (nextjs.md)
16. **Money is integer minor units (or decimal) plus a currency, never a float.** Allocate remainders, round once with a named mode, format with cached `Intl.NumberFormat`. (dates-and-money.md 1 to 3)
17. **Time: pick instant, zoned, or plain date deliberately.** Store instants in UTC with zone info where the event is local; date-only values as `YYYY-MM-DD`; never parse non-ISO strings with `Date`; inject the clock. (dates-and-money.md 4 to 8)
18. **Node services crash on unknown errors and shut down gracefully.** Validate config at startup, no sync APIs or unbounded work on request paths, structured logs to stdout, no `console.log`. (node-runtime.md)
19. **Readonly inputs, no mutation of arguments, no side effects at import time.** `readonly T[]` parameters, `toSorted`/spread; modules do not connect, listen or read env when imported. (types-and-strictness.md 14, modules-imports-exports.md 12)
20. **The gate is automated.** CI runs frozen install, format check, `tsc --noEmit`, typed lint with `--max-warnings 0`, tests, knip and build. A change is done when that passes locally. (tooling-and-lints.md 8)

## 3. Router: which file to read

| Task | Read |
|---|---|
| Any TS code: types, tsconfig, `any`, `as`, enums, unions, generics | `types-and-strictness.md` |
| New file or folder, imports, exports, aliases, barrels, file names, ESM/CJS, publishing a package, cycles | `modules-imports-exports.md` |
| `try`/`catch`, custom errors, promises, concurrency, timeouts, retries, cancellation, streams | `errors-and-async.md` |
| Input from HTTP, forms, env, storage, webhooks, third-party APIs, LLMs; choosing Zod/Valibot | `validation-at-boundaries.md` |
| React components, hooks, state, effects, data fetching, lists; React Native screens and performance | `react-and-react-native.md` |
| Next.js App Router: server/client components, server actions, data access, caching, `proxy.ts` | `nextjs.md` (plus the React file) |
| Node services, CLIs, workers: config, lifecycle, event loop, logging, security, built-ins | `node-runtime.md` |
| Money, prices, dates, time zones, durations, formatting numbers and dates | `dates-and-money.md` |
| tsconfig, ESLint/Biome/Oxlint, Prettier, Vitest, scripts, CI pipeline | `tooling-and-lints.md` |
| `.js`/`.mjs`/`.jsx` files, JSDoc types, `checkJs` | `javascript-without-types.md` |
| Auditing a JS/TS repo for inconsistencies and organisation problems | `codebase-audit.md` |
| UI look, layout, accessibility, design quality | the kwx-designer skill, not this folder |

For a code review, read this file plus the topic files the diff touches, then run each file's Checks section on the changed paths.

## 4. Version facts (October 2026)

Verify against the repo's `package.json` before applying version-specific advice.

| Tool | State |
|---|---|
| TypeScript | 6.0 (March 2026): `strict` on by default, `types` defaults to `[]`, `module` esnext, `target` es2025, `noUncheckedSideEffectImports` on; deprecates `baseUrl`, `moduleResolution node`, `target es5`, `outFile`, AMD/UMD/System. 7.0 (Go compiler, August 2026): 8 to 12x faster builds, deprecations become errors, no stable compiler API until 7.1, so typescript-eslint typed linting stays on 6.0.x for now. |
| Node.js | 24 LTS, 26 entering LTS in October 2026 (Temporal on by default), 22 in maintenance. Type stripping stable (24.12+, 25.2+). `require(esm)` works for graphs without top-level await. |
| ESLint | 10: flat config only, `.eslintrc` ignored; v9 end of life 2026-08-06. |
| React | 19.2 (`useEffectEvent`, `<Activity>`); React Compiler 1.0 stable; `eslint-plugin-react-hooks` 6+ with compiler rules in `recommended`. |
| Next.js | 16: `middleware.ts` renamed `proxy.ts` (Node runtime), Cache Components (`"use cache"`) default in new apps, `params`/`searchParams` are Promises. |
| React Native | 0.82+: New Architecture only. 0.84: Hermes V1 default. FlashList v2 for heavy lists. |
| Zod | 4 stable (`zod`, `zod/mini`); Standard Schema shared by Zod, Valibot, ArkType. |
| Temporal | Stage 4. Native in Firefox 139+, Chrome/Edge 144+, Node 26. Not in Safari: polyfill in browser code. |

## 5. Checks

Run these on any JS/TS change before calling it done. Each topic file has its own detailed Checks.

- **Typecheck.** Pass: exit 0. Verify: `npx tsc --noEmit -p .` (or `npx tsc -b`).
- **Lint.** Pass: exit 0 with no warnings. Verify: `npx eslint . --max-warnings 0` (or `npx biome check .` / `npx oxlint --type-aware`, whichever the repo uses).
- **Format.** Pass: clean. Verify: `npx prettier --check .` or `npx biome format .`
- **Tests.** Pass: green, including new tests for new branches. Verify: the repo's `test` script.
- **Dead code.** Pass: no new unused files, exports or dependencies. Verify: `npx knip`
- **No new escape hatches.** Pass: the diff adds no `any`, `as` (other than `as const`), `!`, `@ts-ignore`, `eslint-disable` without a reason. Verify: `git diff -U0 | rg -n '^\+.*(\bany\b|\bas (?!const)|\w!\.|@ts-ignore|eslint-disable(?!.* -- ))' -P`
- **No convention drift.** Pass: new files follow the folder's export style, file naming and alias root. Verify: the mix commands in modules-imports-exports.md section 14 print nothing new.
- **Boundaries parsed.** Pass: any new input source in the diff passes through a schema. Verify: `git diff -U0 | rg -n '^\+.*(\.json\(\)|JSON\.parse|process\.env|searchParams|formData)'` and confirm a parse for each.
