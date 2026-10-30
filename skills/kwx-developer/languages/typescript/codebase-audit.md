# Auditing a JS/TS codebase for inconsistency and organisation problems

Read when: asked to audit, review or "clean up" a JavaScript/TypeScript repository, before a large refactor, or when you notice two conventions for the same thing. Produces a ranked list of findings with counts and file paths. Changes nothing by itself.

## Contents

1. How to run an audit
2. Inventory
3. Convention mixes (the same job done two ways)
4. Organisation problems
5. Safety escape hatches
6. Tool output to collect
7. Ranking and the report format
8. Fixing what the audit finds
9. Checks

## 1. How to run an audit

1. Inventory the stack (section 2). Note the framework, because it explains some apparent inconsistencies (framework-mandated default exports, file names like `page.tsx`).
2. Measure each dimension in sections 3 to 5 with the commands given. Commands print counts or only the offending paths. Always pass an explicit path (`.`) to `rg`; exclude `node_modules`, build output and generated code (`rg` honours `.gitignore` by default, which usually covers them).
3. For each mix, compute the majority convention. The majority is the default target unless it is the worse option for a stated reason (for example default exports).
4. Run the tools in section 6.
5. Rank findings (section 7). Report with numbers and example paths, never vague adjectives.

Reading every file is not required; sample the worst offenders the commands point at.

## 2. Inventory

```bash
rg -n '"(type|packageManager|engines)"' -A2 package.json
ls package-lock.json pnpm-lock.yaml yarn.lock bun.lock bun.lockb 2>/dev/null
ls tsconfig*.json jsconfig.json eslint.config.* .eslintrc* biome.json* .oxlintrc.json .prettierrc* prettier.config.* 2>/dev/null
ls next.config.* vite.config.* app.json metro.config.* nest-cli.json astro.config.* 2>/dev/null
rg --files -t ts -t js . | sed -E 's/.*\.//' | sort | uniq -c            # file type mix (ts vs js)
rg --files -t ts -t js . | awk -F/ 'NF>1 {print $1"/"$2}' | sort | uniq -c | sort -rn | head -20   # where code lives
```

Record: framework, runtime, module format, package manager, monorepo tool (workspaces, Turborepo, Nx), linters, formatter, test runner.

## 3. Convention mixes (the same job done two ways)

Each row: what to measure, the command, and the default target. A mix is a finding when both variants have meaningful counts (as a rule of thumb the minority is over 10 % and over 3 files) or when the mix sits inside one folder.

### 3.1 Code style mixes

- **Default vs named exports, per folder.** Detect: the `MIXED` script in modules-imports-exports.md section 14. Target: named, framework files excepted.
- **File naming case, per folder.** Detect: the case-mix script in modules-imports-exports.md section 14. Target: kebab-case, or the repo majority.
- **Test file suffix.** Detect: `rg --files . | rg -c '\.test\.[jt]sx?$'` vs `rg --files . | rg -c '\.spec\.[jt]sx?$'`. Target: one suffix.
- **Test location.** Detect: `rg --files . | rg '(__tests__|/tests?/).*\.(test|spec)\.'` vs co-located. Target: one placement.
- **Alias roots.** Detect: `rg -o "from ['\"](@/|#/|~/|src/)" -t ts -t js -I . | sort | uniq -c`. Target: one root.
- **Deep relative imports.** Detect: `rg -c "from ['\"]\.\./\.\./\.\./" -t ts -t js .`. Target: zero.
- **Barrels.** Detect: `rg -l -g 'index.{ts,tsx,js,mts}' '^export (\*|\{[^}]*\}) from' .`. Target: none inside apps.
- **ESM vs CJS.** Detect: `rg -c '\brequire\(|module\.exports' -t ts -t js .` in a `"type": "module"` package. Target: ESM only.
- **`type` vs `interface` for object shapes.** Detect: `rg -c '^export interface ' -t ts .` vs `rg -c '^export type \w+ = \{' -t ts .`. Target: the majority, enforced by `consistent-type-definitions`.
- **Enums vs const objects.** Detect: `rg -c '^\s*(export\s+)?(const\s+)?enum\s' -t ts .` vs `rg -c 'as const;?$' -t ts .`. Target: const objects (types-and-strictness.md 9).
- **`.then` chains vs `await`.** Detect: `rg -c '\.then\(' -t ts -t js .` and `rg -c '\bawait\b' -t ts -t js .`. Target: `await`; `.then` is fine for one-liners and `void p.then(...).catch(...)`.
- **Component definition style.** Detect: `rg -c '^export function [A-Z]' -g '*.tsx' .` vs `rg -c '^export const [A-Z]\w* = \(' -g '*.tsx' .` and `React.FC` count `rg -c 'React\.FC|: FC<' -g '*.tsx' .`. Target: function declarations, no `React.FC`.
- **null vs undefined for "absent".** Detect: `rg -c 'return null;' -t ts .` vs `rg -c 'return undefined;' -t ts .` per layer. Target: one per layer (types-and-strictness.md 12).
- **Error style.** Detect: `rg -c 'ok: (true|false)' -t ts .` (Result values) vs `rg -c 'throw new' -t ts .` per module. Target: one style per layer (errors-and-async.md 2).

### 3.2 Library mixes (two libraries for one job)

```bash
rg -o '"(axios|ky|got|node-fetch|superagent|zod|valibot|yup|joi|superstruct|arktype|io-ts|class-validator|moment|dayjs|date-fns|luxon|lodash|lodash-es|ramda|underscore|redux|@reduxjs/toolkit|zustand|jotai|mobx|recoil|valtio|@tanstack/react-query|swr|styled-components|@emotion/react|tailwindcss|sass|jest|vitest|mocha|ava|winston|pino|bunyan|log4js|uuid|nanoid|cuid|express|fastify|koa|hono)"' \
  -g 'package.json' -g '!**/node_modules/**' . | sed 's/.*://' | sort | uniq -c
```

Group the output by job (HTTP client, validation, dates, utility belt, state, server cache, styling, tests, logging, IDs, server framework). More than one entry in a group is a finding. Then confirm actual use, since a dependency can be listed but unused: `rg -l "from ['\"]axios['\"]" -t ts -t js . | wc -l`.

Also check for hand-rolled duplicates of a dependency's job: `fetch` wrappers next to axios, custom `formatDate` next to date-fns.

### 3.3 Duplicate helpers and types

The same function or type name exported from several files usually means copy-paste helpers that drift:

```bash
rg -oN --no-filename -t ts -t js '^export (async )?function (\w+)' -r '$2' . | sort | uniq -c | sort -rn | awk '$1>1'
rg -oN --no-filename -t ts '^export (type|interface) (\w+)' -r '$2' . | sort | uniq -c | sort -rn | awk '$1>1'
rg -oN --no-filename -t ts -t js '^export const (\w+) = (async )?\(' -r '$1' . | sort | uniq -c | sort -rn | awk '$1>1'
```

Ignore framework names that are meant to repeat (`GET`, `POST`, `generateMetadata`, `loader`, `Props`). For each remaining name, list the files (`rg -n '^export (async )?function errorMessageFromValue' -t ts .`) and diff the bodies. In a real monorepo checked while writing this file, one helper was defined 11 times.

## 4. Organisation problems

- **God files.** Detect: `rg --files -t ts -t js . | xargs wc -l | sort -rn | sed -n '2,21p'`. Threshold that makes it a finding: non-test source over about 500 lines, or one file mixing several concepts.
- **Grab-bag modules.** Detect: `rg --files . | rg -i '/(utils?|helpers?|common|misc|shared)\.(ts|js)x?$'` and their export counts. Threshold that makes it a finding: any `utils.ts` with more than about 10 unrelated exports.
- **Global types dump.** Detect: `rg --files . | rg '/types\.(ts|d\.ts)$' | xargs wc -l`. Threshold that makes it a finding: one `types.ts` imported by most of the codebase.
- **Mixed folder strategy.** Detect: top-level `components/`, `hooks/`, `utils/` next to `features/` or `modules/`. Threshold that makes it a finding: both strategies for the same kind of code.
- **Deep nesting.** Detect: `rg --files -t ts . | awk -F/ '{print NF-1}' | sort -n | uniq -c`. Threshold that makes it a finding: paths more than about 6 folders deep inside `src`.
- **Cycles.** Detect: `npx madge --circular --extensions ts,tsx src` or `npx knip --include cycles`. Threshold that makes it a finding: any runtime cycle.
- **Layer violations.** Detect: dependency-cruiser rules, or grep: `rg -l "from ['\"].*(/ui/|/components/)" src/domain src/server 2>/dev/null`. Threshold that makes it a finding: domain or server importing UI; UI importing the DB.
- **Env read everywhere.** Detect: `rg -l 'process\.env\.' -t ts -t js . | wc -l`. Threshold that makes it a finding: more than the config module and framework config.
- **Import-time side effects.** Detect: `rg -n '^(await |[a-zA-Z_.]+\.(listen|connect)\(|setInterval\()' -t ts -t js src`. Threshold that makes it a finding: outside entry files.
- **Dead code.** Detect: `npx knip`. Threshold that makes it a finding: any unused file or dependency; unused exports in app code.
- **Console logging in app code.** Detect: `rg -c '\bconsole\.(log|debug)\(' -t ts -t js src`. Threshold that makes it a finding: in server or library code.
- **Commented-out code.** Detect: `rg -c '^\s*//\s*(const|let|if|return|await|import)\b' -t ts -t js .`. Threshold that makes it a finding: blocks of more than a few lines.
- **TODO debt.** Detect: `rg -c 'TODO|FIXME|HACK|XXX' -t ts -t js .`. Threshold that makes it a finding: report the count and the oldest via `git blame`.

## 5. Safety escape hatches

Count, then sample. High counts are not automatically bugs, but each is a place the type system is not protecting the code.

```bash
rg -cP -t ts ':\s*any\b|<any>|\bas any\b' -g '!*.d.ts' . | awk -F: '{s+=$2} END {print "any:", s+0}'
rg -cP -t ts '\bas (?!const\b)[A-Za-z_{\[(]' -g '!*.d.ts' . | awk -F: '{s+=$2} END {print "as:", s+0}'
rg -cP -t ts '\w!(\.|\[|\))' . | awk -F: '{s+=$2} END {print "non-null:", s+0}'
rg -c '@ts-ignore|@ts-nocheck' -t ts -t js . | awk -F: '{s+=$2} END {print "ts-ignore/nocheck:", s+0}'
rg -c 'eslint-disable' -t ts -t js . | awk -F: '{s+=$2} END {print "eslint-disable:", s+0}'
rg -c 'forEach\(async' -t ts -t js . | awk -F: '{s+=$2} END {print "forEach(async:", s+0}'
rg -cUP 'catch\s*(\([^)]*\))?\s*\{\s*\}' -t ts -t js . | awk -F: '{s+=$2} END {print "empty catch:", s+0}'
```

Divide by thousands of lines (`rg --files -t ts . | xargs cat | wc -l`) so repos of different sizes compare. Also run the typed lint with the promise rules on, even if the repo does not have them configured, to count floating promises:

```bash
npx eslint . --no-config-lookup -c /tmp/audit-eslint.config.js -f json -o /tmp/audit.json 2>/dev/null
```

(where the temporary config enables only `no-floating-promises`, `no-misused-promises`, `switch-exhaustiveness-check` with `projectService`). Never commit that config.

## 6. Tool output to collect

- **TypeScript.** Command: `npx tsc --noEmit -p . 2>&1 | tail -3` and `npx tsc --showConfig`. What it gives: error count, real strictness.
- **Lint.** Command: `npx eslint . -f json -o /tmp/eslint.json` then count by `ruleId`. What it gives: which rules fail most.
- **knip.** Command: `npx knip --reporter json`. What it gives: unused files, exports, dependencies, unlisted dependencies, duplicates.
- **madge / dependency-cruiser.** Command: `npx madge --circular --extensions ts,tsx src`. What it gives: cycles.
- **Tests.** Command: the repo's test script with coverage. What it gives: failing and untested areas.
- **Bundle (web).** Command: framework build output, `@next/bundle-analyzer`, `vite-bundle-visualizer`. What it gives: heavy client dependencies.
- **Dependencies.** Command: `npm outdated`, `npm audit --audit-level=high`. What it gives: stale and vulnerable packages.
- **Packaging (libraries).** Command: `npx publint`, `npx @arethetypeswrong/cli --pack .`. What it gives: broken exports and types.

## 7. Ranking and the report format

Rank by (impact) x (spread), cheapest fixes first within a tier:

1. **Correctness and security**: unparsed boundaries, missing auth checks in server actions or routes, floating promises, swallowed errors, float money, secrets reachable from client code, SQL or shell injection.
2. **Things that make bugs likely**: `any`/`as` hotspots, `@ts-ignore`, disabled strict flags, cycles, import-time side effects, duplicate helpers that drifted apart.
3. **Convention mixes**: export style, naming, aliases, two libraries for one job, two error styles.
4. **Organisation and hygiene**: god files, grab-bag utils, dead code, deep nesting, TODOs.

Each finding in the report:

```
[tier] Title in plain words
Evidence: counts and up to 5 example paths with line numbers
Why it matters: one sentence, concrete consequence
Fix: the target convention or change, the lint rule that prevents regression, rough size (files touched)
```

Report what you could not check (no tests to run, build needs secrets, tool failed). Do not pad the report with style opinions the repo has no reason to adopt.

## 8. Fixing what the audit finds

- One finding per change. Never mix a convention migration with feature work.
- Order: add the lint rule or check that blocks new violations (as a warning in the PR that adds it, then error), then migrate existing code with a codemod or autofix (`eslint --fix`, `biome check --write`, `knip --fix`, `ts-morph` scripts), then delete what became unused.
- For large repos, land migrations in waves that avoid files with open pull requests (Atlassian's barrel removal touched about 90,000 files in a few days this way).
- After each wave: typecheck, lint, tests, build.

## 9. Checks

- **Audit is reproducible.** Pass: every finding states the command that produced its numbers. Verify: re-run the commands in the report.
- **Framework exceptions removed.** Pass: export-style and naming findings exclude framework-mandated files. Verify: no `page.tsx`, `layout.tsx`, `*.config.*`, route modules in the export-mix evidence.
- **Majority computed.** Pass: each mix finding states both counts and the chosen target. Verify: read the report.
- **No changes made during the audit.** Pass: `git status` is clean after the audit (temporary configs in `/tmp` only). Verify: `git status --porcelain` is empty.
- **Tier 1 items have evidence lines.** Pass: each security or correctness finding cites file and line. Verify: read the report.
