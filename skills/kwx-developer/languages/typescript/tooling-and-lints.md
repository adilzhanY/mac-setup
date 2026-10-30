# Tooling, lint and CI

Read when: setting up or changing tsconfig, ESLint/Biome/Oxlint, Prettier, the test runner, package scripts or CI for a JS/TS project, or when a repo has no automated checks. The tsconfig itself is in types-and-strictness.md section 2.

## Contents

1. Detect what the repo already uses
2. The toolchain decision (October 2026)
3. ESLint flat config, typed
4. Rules to add beyond the presets
5. Biome or Oxlint instead of, or next to, ESLint
6. Formatting
7. Tests
8. Package scripts and CI pipeline
9. Editor and pre-commit
10. Checks

## 1. Detect what the repo already uses

Never introduce a second tool for a job the repo already does. Inventory first:

```bash
ls package-lock.json pnpm-lock.yaml yarn.lock bun.lock bun.lockb 2>/dev/null           # package manager
ls eslint.config.* .eslintrc* biome.json* .oxlintrc.json oxlint.json 2>/dev/null       # linters
ls .prettierrc* prettier.config.* .editorconfig 2>/dev/null                            # formatter
ls vitest.config.* jest.config.* playwright.config.* 2>/dev/null                        # tests
rg -n '"(typescript|eslint|typescript-eslint|@biomejs/biome|oxlint|prettier|vitest|jest)":' package.json
rg -n '"scripts"' -A 25 package.json
ls .github/workflows 2>/dev/null && rg -n 'run:' .github/workflows
```

`.eslintrc*` files are dead in ESLint 10 (flat config only; v9 reached end of life 2026-08-06). Migrate with `npx @eslint/migrate-config .eslintrc.json` and review the output.

## 2. The toolchain decision (October 2026)

| Job | Default for a new project | Notes |
|---|---|---|
| Type checking | `tsc --noEmit` (TS 6.0.x) | TS 7.0 (Go, 8 to 12x faster) is stable, but typescript-eslint and other compiler-API tools (Vue/Svelte/Astro tooling, webpack loaders) cannot use it until 7.1. If the repo uses typescript-eslint typed linting, keep `typescript` on 6.0.x; check typescript-eslint's peer range before upgrading. |
| Linting | ESLint 10 + typescript-eslint typed configs | the most complete type-aware rule set (`no-floating-promises`, `no-misused-promises`, `no-unsafe-*`) |
| Formatting | Prettier (or Biome's formatter) | one formatter only |
| Fast lint alternative | Oxlint (with `--type-aware`, needs TS 7) or Biome 2 | Biome's own type inference finds about 75 % of what `no-floating-promises` finds |
| Tests | Vitest | `node:test` for small Node libraries and scripts; Jest only where it already exists |
| Dead code | knip | unused files, exports, dependencies |
| Cycles and layers | dependency-cruiser or madge | see modules-imports-exports.md |
| Library packaging | publint + `@arethetypeswrong/cli` | run before every publish |

If the repo already has Biome or Oxlint as its only linter, keep it, and consider adding typescript-eslint with only the type-aware promise rules as a second pass in CI.

## 3. ESLint flat config, typed

```js
// eslint.config.js
import js from "@eslint/js";
import { defineConfig, globalIgnores } from "eslint/config";
import tseslint from "typescript-eslint";
import importX from "eslint-plugin-import-x";
import reactHooks from "eslint-plugin-react-hooks";   // React projects only
import prettier from "eslint-config-prettier/flat";    // last: turns off rules that fight the formatter

export default defineConfig([
  globalIgnores(["dist/", "build/", ".next/", "coverage/", "**/*.gen.ts", "**/generated/**"]),

  {
    files: ["**/*.{ts,tsx,mts,cts}"],
    extends: [
      js.configs.recommended,
      tseslint.configs.strictTypeChecked,      // recommendedTypeChecked if the team is newer to TS
      tseslint.configs.stylisticTypeChecked,
      importX.flatConfigs.recommended,
      importX.flatConfigs.typescript,
    ],
    languageOptions: {
      parserOptions: { projectService: true, tsconfigRootDir: import.meta.dirname },
    },
    rules: {
      "@typescript-eslint/switch-exhaustiveness-check": "error",
      "@typescript-eslint/no-import-type-side-effects": "error",
      "@typescript-eslint/explicit-module-boundary-types": "error",
      "@typescript-eslint/restrict-template-expressions": ["error", { allowNumber: true }],
      "@typescript-eslint/no-unused-vars": ["error", { argsIgnorePattern: "^_", varsIgnorePattern: "^_" }],
      "import-x/no-default-export": "error",
      "import-x/no-duplicates": "error",
      "eqeqeq": ["error", "always", { null: "ignore" }],
      "no-console": ["error", { allow: ["warn", "error"] }],
      "no-await-in-loop": "warn",
      "preserve-caught-error": "error",
      "no-restricted-imports": ["error", {
        patterns: [
          { group: ["../../../*"], message: "Use the #/ (or @/) alias instead of deep relative paths." },
          { regex: "(^|/)index(\\.[jt]sx?)?$", message: "Import the defining file, not a barrel." },
        ],
      }],
    },
  },

  // Files where frameworks require default exports.
  {
    files: [
      "**/app/**/{page,layout,template,loading,error,global-error,not-found,default}.tsx",
      "**/*.config.{ts,js,mjs}", "**/*.stories.tsx",
    ],
    rules: { "import-x/no-default-export": "off" },
  },

  // Plain JS (config files, scripts): no type-aware rules.
  { files: ["**/*.{js,mjs,cjs}"], extends: [js.configs.recommended, tseslint.configs.disableTypeChecked] },

  // Tests: relax rules that fight test code.
  {
    files: ["**/*.test.{ts,tsx}", "**/*.spec.{ts,tsx}"],
    rules: { "@typescript-eslint/no-non-null-assertion": "off", "@typescript-eslint/no-unsafe-assignment": "off" },
  },

  reactHooks.configs.flat.recommended,
  prettier,
]);
```

Notes:

- `projectService: true` finds the right tsconfig per file and is the recommended typed-lint setup. Typed linting needs the whole program, so it is slower: run it in CI and before push; editors cache it.
- `strictTypeChecked` is not "stable" across minor versions (new rules arrive); pin the typescript-eslint version and review new errors on upgrade.
- `restrict-template-expressions` in `strict` forbids numbers in templates; allowing numbers is the usual relaxation. Do not relax `no-floating-promises`, `no-misused-promises`, or the `no-unsafe-*` family.
- `@typescript-eslint/consistent-type-imports` is unnecessary when `verbatimModuleSyntax` is on (the compiler already enforces it); enable it only for its autofix, and expect duplicate reports.
- Never `eslint-disable` a whole file to land a change. Disable one line, name the rule, give the reason after `--`.

## 4. Rules to add beyond the presets

These catch bugs models produce often and are not in `recommended`:

| Rule | Catches |
|---|---|
| `@typescript-eslint/switch-exhaustiveness-check` | a new union member not handled |
| `@typescript-eslint/strict-boolean-expressions` (optional, noisy) | `if (count)` dropping zero, `if (str)` dropping "" |
| `@typescript-eslint/prefer-nullish-coalescing` (in `stylistic-type-checked`) | `||` replacing valid falsy values |
| `@typescript-eslint/no-unnecessary-condition` (in `strict`) | checks that can never be true, often a sign the type is wrong |
| `@typescript-eslint/require-array-sort-compare` | `[10, 9, 1].sort()` sorting as strings |
| `@typescript-eslint/promise-function-async` | functions returning promises that can also throw synchronously |
| `preserve-caught-error` (ESLint 9.35+) | rethrowing without `cause` |
| `no-param-reassign` with `props: true` | mutating arguments |
| `unicorn/prefer-node-protocol`, `unicorn/filename-case` | builtin imports, file naming |
| `eslint-plugin-regexp` recommended | ReDoS-prone and wrong regexes |
| `n/no-process-env` (outside config) | env read all over the code |

Add them only if the repo will keep them green. A rule left at `warn` with 400 warnings is noise; use `--max-warnings 0` and fix or remove.

## 5. Biome or Oxlint instead of, or next to, ESLint

Biome 2 (formatter plus linter in one Rust binary):

```jsonc
// biome.json
{
  "$schema": "https://biomejs.dev/schemas/2.0.0/schema.json",
  "vcs": { "enabled": true, "clientKind": "git", "useIgnoreFile": true },
  "formatter": { "enabled": true, "indentStyle": "space", "lineWidth": 100 },
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true,
      "nursery": { "noFloatingPromises": "error" },
      "style": { "noDefaultExport": "error", "useImportType": "error", "useNodejsImportProtocol": "error" },
      "suspicious": { "noExplicitAny": "error" }
    }
  },
  "assist": { "actions": { "source": { "organizeImports": "on" } } }
}
```

- Rule group names (for example where `noFloatingPromises` lives) change between Biome versions; check `npx biome explain <rule>` for the installed version.
- Biome type-aware rules need the project scanner (`project` domain) and cover a subset of typescript-eslint.
- Oxlint: `npx oxlint --type-aware` runs 59 of 61 typescript-eslint type-aware rules through tsgolint (typescript-go); it requires TypeScript 7 and a tsconfig without options removed in 7 (`baseUrl`). `--type-check` can also report compiler errors.
- Valid combinations: Biome alone; ESLint + Prettier; Oxlint for fast feedback plus ESLint for the remaining rules (`eslint-plugin-oxlint` turns off duplicates). Not valid: two formatters, or two linters both reporting the same rules.

## 6. Formatting

- One formatter owns all formatting, runs on save and in CI (`prettier --check .` or `biome check`). ESLint does not format: no stylistic rules that conflict (`eslint-config-prettier` last in the config).
- Prettier defaults (3.x): `printWidth` 80, 2 spaces, semicolons, double quotes, `trailingComma: "all"`, `arrowParens: "always"`, `endOfLine: "lf"`. Do not override them in a new project unless the team asks; every override is a bikeshed. If the repo has a config, follow it exactly.
- `printWidth` is a target, not a hard limit (Prettier docs); do not fight it with manual line breaks.
- Commit a `.editorconfig` (indent, final newline, charset) so non-JS files agree.
- Formatting-only changes go in their own commit, never mixed with logic changes. Add the commit hash to `.git-blame-ignore-revs`.
- Never reformat a whole file you are editing for another reason if the repo is not formatter-clean; it buries the real diff. Format only what you touched, and report the drift.

## 7. Tests

- Vitest for new TS projects (native ESM and TS, Jest-compatible API, fast watch). Keep Jest where it exists; do not add a second runner.
- Tests live next to code (`x.test.ts`). Test behaviour through public functions, not private helpers.
- Type-level tests for library types and tricky generics: Vitest `expectTypeOf<ReturnType<typeof f>>().toEqualTypeOf<Expected>()`, run with `vitest --typecheck`.
- No real network in unit tests: inject the client or mock at the HTTP layer (MSW). Use fixed clocks (dates-and-money.md section 8).
- Integration tests hit a real database in a container (Testcontainers or a CI service), not mocks of the ORM.
- Flaky test policy: fix or delete; never retry-until-green in CI.
- E2E in browsers: Playwright.

## 8. Package scripts and CI pipeline

Standard script names, so humans and agents can guess them:

```jsonc
{
  "scripts": {
    "dev": "...",
    "build": "...",
    "typecheck": "tsc --noEmit",
    "lint": "eslint . --max-warnings 0 --cache",
    "format": "prettier --write .",
    "format:check": "prettier --check .",
    "test": "vitest run",
    "knip": "knip",
    "check": "npm run typecheck && npm run lint && npm run format:check && npm run test && npm run knip"
  }
}
```

CI order (fail fast, cheapest first), on every pull request:

1. Install with the frozen lockfile (`npm ci`, `pnpm install --frozen-lockfile`).
2. `format:check`.
3. `typecheck` (`tsc -b` for project references).
4. `lint` with `--max-warnings 0`.
5. `test` (with coverage if the repo tracks it).
6. `knip` (unused files, exports, dependencies).
7. `build` (catches bundler-only errors, env issues, Next.js server/client boundary errors).
8. Libraries: `npx publint && npx @arethetypeswrong/cli --pack .`.
9. Optional: `depcruise src` for cycles and layer rules, `npm audit --audit-level=high`.

Cache the package manager store and ESLint's `.eslintcache` between runs.

## 9. Editor and pre-commit

- Commit `.vscode/settings.json` only for project-wide needs (`"typescript.tsdk": "node_modules/typescript/lib"`, formatter on save); never personal preferences.
- Pre-commit hooks (`lint-staged` with Husky or `simple-git-hooks`, or lefthook) run the formatter and a fast lint on staged files only. Never run the full typed lint or test suite in pre-commit; it gets bypassed with `--no-verify`. CI is the gate.

## 10. Checks

- **One of each tool.** Pass: one lockfile, one formatter, one primary linter, one unit test runner. Verify: section 1 commands.
- **Flat config.** Pass: `eslint.config.*` exists; no `.eslintrc*`. Verify: `ls .eslintrc* 2>/dev/null` prints nothing.
- **Typed linting on.** Pass: `projectService` (or `project`) set and a `*TypeChecked` config used. Verify: `rg -n 'projectService|TypeChecked' -g 'eslint.config.*' .`
- **Promise rules active.** Pass: `no-floating-promises` reports in a deliberate test. Verify: `npx eslint --print-config src/index.ts | rg 'no-floating-promises|no-misused-promises'` shows `2`/`"error"`.
- **Zero warnings policy.** Pass: lint script uses `--max-warnings 0`. Verify: `rg -n 'max-warnings' package.json`
- **Formatter clean.** Pass: exit 0. Verify: `npx prettier --check .` or `npx biome check .`
- **CI runs the full set.** Pass: workflow runs install (frozen), typecheck, lint, format check, test, build. Verify: `rg -n 'run:' .github/workflows`
- **TS version compatible with the linter.** Pass: `typescript` is within typescript-eslint's peer range. Verify: `npm ls typescript typescript-eslint` shows no peer warnings.
- **No blanket disables.** Pass: no file-level `eslint-disable` without a rule name, and no `/* eslint-disable */` in source. Verify: `rg -n 'eslint-disable(?!-next-line|-line)\s*(\*/|$)' -P -t ts -t js .`
- **Disables have reasons.** Pass: every disable comment has `-- reason`. Verify: `rg -n 'eslint-disable' -t ts -t js . | rg -v -- ' -- '`
- **Dead code clean.** Pass: knip exits 0. Verify: `npx knip`
