# Modules, imports and exports

Read when: creating a file or folder, adding an import or export, setting up path aliases, touching `package.json` `type`/`exports`/`imports`, or auditing a repo whose modules are organised inconsistently.

## Contents

1. Defaults at a glance
2. Named exports, default exports, and the exceptions
3. Barrel files
4. Public entry points and encapsulation
5. Path aliases: `#` subpath imports vs tsconfig `paths`
6. Import order and type-only imports
7. File and folder naming
8. One concept per file
9. ESM vs CommonJS in Node
10. Publishing a package: `exports`, types, dual formats
11. Circular imports
12. Side effects at import time
13. Enforcing feature boundaries
14. Detecting a mix and migrating
15. Checks

## 1. Defaults at a glance

| Decision | Default | Overridden by |
|---|---|---|
| Export style | named exports only | framework files that require `export default` (section 2) |
| Barrels (`index.ts` that re-exports) | none inside an app; one entry file per published package | an existing repo-wide barrel convention, until a planned migration |
| Import paths | relative inside a feature folder; one alias root (`#/` or `@/`) across features | none |
| Alias mechanism | package.json `"imports": { "#/*": ... }` | Next.js and other bundler apps that already use tsconfig `paths` with `@/*` |
| Type imports | `import type` / inline `type`, enforced by `verbatimModuleSyntax` | none |
| File names | kebab-case (`user-profile.ts`) | an existing convention (for example PascalCase component files) applied repo-wide |
| Module format | ESM (`"type": "module"`) | a legacy CJS package; do not convert one file at a time |
| Import sorting | the tool's autofix (Biome organizer, `import-x/order`, or `simple-import-sort`) | none; never hand-sort |

The overriding rule: the repo's existing convention beats this table. If the repo is mixed, follow the majority inside the folder you touch, do not add a third style, and report the mix (section 14).

## 2. Named exports, default exports, and the exceptions

Use named exports. Reasons, all checkable:

- A default export has no canonical name, so each importer names it differently (`import Btn from`, `import Button from`, `import PrimaryButton from`). Search and rename break. Google's TypeScript style guide bans default exports for this reason.
- Auto-import and rename-symbol work reliably on named exports.
- Named exports make "what does this module offer" visible in one line and let knip report each unused one.

```ts
// Bad
export default function formatPrice(cents: number) { ... }

// Good
export function formatPrice(cents: Cents): string { ... }
```

Default exports are required, and therefore correct, in:

- Next.js App Router special files: `page`, `layout`, `template`, `loading`, `error`, `global-error`, `not-found`, `default` (route handlers in `route.ts` use named `GET`/`POST` exports). Pages Router files and `_app`/`_document`.
- Expo Router and Remix/React Router framework route modules.
- Config files whose loaders expect it: `vite.config.ts`, `eslint.config.js`, `next.config.ts`, `tailwind.config.ts`, `vitest.config.ts`, `playwright.config.ts`, Storybook `*.stories.tsx` meta.
- `React.lazy(() => import("./x"))` expects a default. Keep the component named and adapt: `lazy(() => import("./chart").then((m) => ({ default: m.Chart })))`.

In those files, still name the function (`export default function SettingsPage()`) so stack traces and DevTools show it. Also avoid `export let` (mutable bindings); export a getter function instead.

Lint: `import-x/no-default-export` with an override block that turns it off for the framework globs above.

## 3. Barrel files

A barrel is an `index.ts` whose job is `export * from "./a"; export * from "./b"`. Inside an application, do not create them, and do not import through one when a direct path exists.

Evidence:

- Loading a module loads its whole import graph, and tree shaking does not happen in dev servers, test runners or Node. Marvin Hagemeister measured module load cost at 0.31 s for 1,000 modules, 3.1 s for 10,000 and 16.8 s for 25,000; test runners pay it per test file.
- Vercel measured popular barrel-exported packages at 200 to 800 ms just to import; `@mui/material` dev boot went from 7.1 s (2,225 modules) to 2.9 s (735) once imports were rewritten to direct paths (`optimizePackageImports`).
- Atlassian removed barrels across the Jira frontend (about 100,000 files): TypeScript highlighting more than 30 % faster, local unit tests about 50 % faster (up to 10x in some packages), unit tests per CI build 1,600 to 200, build minutes per commit down 75 %. They first added a lint rule blocking new barrels, then codemodded imports with a fixable ESLint rule, then deleted orphaned files.
- Barrels hide cycles: `a.ts` imports `./index` which imports `b.ts` which imports `a.ts`.

What to do instead:

- Import the file that defines the symbol: `import { Button } from "#/ui/button"`.
- A few barrels are fine (Hagemeister): one public entry per published package (section 4). The problem is a barrel in every folder.
- For third-party barrel packages in Next.js, list them in `experimental.optimizePackageImports` (many, such as `lucide-react`, are preconfigured).

```js
// eslint.config.js: block imports that go through an index file
"no-restricted-imports": ["error", { patterns: [{ regex: "(^|/)index(\\.[jt]sx?)?$", message: "Import the defining file, not a barrel." }] }],
```

## 4. Public entry points and encapsulation

Encapsulation is the real argument for barrels; get it without them:

- Inside one app: a feature folder exposes what other features may use through a file named for the purpose (`features/billing/public.ts` or `api.ts`), and other features import only that file. Enforce with `no-restricted-imports` patterns or dependency-cruiser (section 13). This is one small explicit file, not a re-export of everything.
- Across packages in a monorepo: each package declares `"exports"` in its `package.json`. Once `exports` exists, every subpath not listed is unreachable (`ERR_PACKAGE_PATH_NOT_EXPORTED`), which is enforced encapsulation without an `index.ts` chain.

## 5. Path aliases: `#` subpath imports vs tsconfig `paths`

`tsconfig` `paths` only tells the type checker where files are. It does not rewrite emitted code, Node ignores it, and Node type stripping does not read tsconfig at all. Each tool (Vite, Jest, Vitest, Metro) needs its own copy of the alias, which drifts.

Prefer package.json subpath imports, which Node, bundlers and TypeScript (`moduleResolution` `nodenext` or `bundler`) all understand natively:

```jsonc
// package.json
{
  "type": "module",
  "imports": {
    "#/*": "./src/*"            // Node 24.14+/25.4+ and TS 6.0+ accept the bare "#/" prefix
  }
}
```

```ts
import { db } from "#/db/client.ts";   // with type stripping
import { db } from "#/db/client.js";   // with tsc emit under nodenext
import { db } from "#/db/client";      // with a bundler (moduleResolution bundler)
```

For older Node, use a named prefix: `"#src/*": "./src/*"`.

When a framework already standardised on `@/*` in tsconfig `paths` (Next.js `create-next-app`, many Vite templates), keep it; the framework's bundler reads it. Do not add a second alias root. Never use `baseUrl` (deprecated in TS 6.0, removed in 7.0); write `"paths": { "@/*": ["./src/*"] }`.

Relative vs alias, one rule: relative (`./`, `../`) within a feature folder; alias when crossing into another top-level folder. Ban climbing more than two levels: `../../../` means the import should use the alias. Lint: `no-restricted-imports` with `patterns: [{ group: ["../../../*"], message: "Use the #/ alias" }]`.

## 6. Import order and type-only imports

- Let a tool own the order and run its autofix; never reorder by hand and never review ordering in PRs. Pick one: Biome's import organizer (merges imports from the same module, sorts, respects blank-line chunks only as separators it understands), `import-x/order` with `alphabetize`, or `simple-import-sort`. Two tools fighting over order produce churn on every save.
- Group order, if configuring by hand: `node:` builtins, external packages, internal alias (`#/`, `@/`), parent, sibling, then side-effect imports (CSS) where order matters.
- Import Node builtins with the `node:` prefix (`import { readFile } from "node:fs/promises"`). It cannot be shadowed by an npm package. Lint: `unicorn/prefer-node-protocol` or Biome `useNodejsImportProtocol`.
- Type-only imports use `import type { X }` or `import { type X, y }`. With `verbatimModuleSyntax: true`, `tsc` fails when a type is imported as a value, and Node type stripping crashes at runtime on it. Use `@typescript-eslint/consistent-type-imports` only if you want autofix; with `verbatimModuleSyntax` the compiler already enforces correctness, and running both gives duplicate reports. Pair with `@typescript-eslint/no-import-type-side-effects` when using inline `type` specifiers, so `import { type A } from "x"` does not keep a side-effect import of `x`.
- No `require()` in TypeScript or ESM files (`@typescript-eslint/no-require-imports`). For a CJS-only package from ESM, use a default import (`import pkg from "cjs-pkg"`) or `createRequire(import.meta.url)`.
- No dynamic `import(variable)` with user input (`6.17 Avoid module loading using a variable`, Node best practices). Dynamic imports with literal paths are fine for code splitting.

## 7. File and folder naming

- Default: kebab-case for every file and folder (`order-summary.tsx`, `use-cart.ts`). It is safe on case-insensitive file systems (macOS, Windows), where renaming `button.tsx` to `Button.tsx` leaves git and the bundler disagreeing.
- Many React codebases use PascalCase for component files (`OrderSummary.tsx`). That is acceptable if it is applied to every component file. What is not acceptable is a mix inside one folder.
- Test files sit next to the code: `price.ts` and `price.test.ts`. Pick `.test.` or `.spec.` once.
- Framework-mandated names win: `page.tsx`, `layout.tsx`, `+page.svelte`, `_layout.tsx`, `[id].tsx`.
- File name equals the main export in the matching case: `format-price.ts` exports `formatPrice`; `OrderSummary.tsx` exports `OrderSummary`.
- No `utils.ts`, `helpers.ts`, `common.ts`, `misc.ts` grab bags. Name the file after what it holds (`currency.ts`, `retry.ts`). A file that needs the word "utils" to be named has no single purpose.
- Lint: `unicorn/filename-case` (`{ case: "kebabCase" }`) or `check-file/filename-naming-convention`; Biome `useFilenamingConvention`.

## 8. One concept per file

- A file exports one main thing plus its closely tied helpers and types. Export only what other modules use (Google style guide: "Only export symbols that are used outside of the module"). knip lists unused exports.
- No container classes with only static members to fake a namespace; export functions and constants.
- Types live with the code that owns them. A global `types.ts` collecting every interface becomes a dependency hub that everything imports and that causes cycles. Shared domain types go in the domain module (`orders/order.ts`), shared wire types next to the schema that produces them.
- Keep files under roughly 300 to 400 lines as a smell threshold, not a rule. Split by concept, never by line count.

## 9. ESM vs CommonJS in Node

How Node decides (Node docs, "Packages"):

- `.mjs` is always ESM, `.cjs` always CommonJS. `.js` follows the nearest `package.json` `"type"`: `"module"` means ESM, missing or `"commonjs"` means CJS. Same for `.ts`/`.mts`/`.cts` under type stripping.
- Files with no `"type"` are "ambiguous": Node sniffs for ESM syntax and pays a performance cost. Always set `"type"` explicitly.
- ESM `import` never guesses extensions or `index` files. `import "./util"` fails; write `./util.js` (tsc emit, `nodenext`) or `./util.ts` (type stripping, with `rewriteRelativeImportExtensions` if you also emit). Directories are not modules in ESM.
- `require()` of an ES module works in current Node (22.12+, 20.19+) only if the graph has no top-level `await`, otherwise `ERR_REQUIRE_ASYNC_MODULE`.
- In ESM there is no `__dirname`/`__filename`; use `import.meta.dirname` and `import.meta.filename` (Node 20.11+), and `import.meta.resolve()`.
- JSON import in ESM: `import data from "./data.json" with { type: "json" }` (`assert` is a TS 6 error).

Default for new code: `"type": "module"`, ESM syntax everywhere, `module: "nodenext"` or `"preserve"`. Do not mix `require` and `import` in one package. Converting an existing CJS package is a separate, whole-package change.

## 10. Publishing a package: `exports`, types, dual formats

```jsonc
{
  "name": "@acme/money",
  "type": "module",
  "exports": {
    ".": {
      "types": "./dist/index.d.ts",   // "types" first: conditions match in key order
      "default": "./dist/index.js"     // "default" always last
    },
    "./package.json": "./package.json"
  },
  "files": ["dist"],
  "sideEffects": false
}
```

- `exports` takes precedence over `main` and hides every subpath not listed. Targets start with `./`.
- Condition order is significant: most specific first, `default` last; `types` before everything (TypeScript reads it).
- Ship ESM only unless you have consumers stuck on CJS without `require(esm)`. Dual ESM plus CJS output risks the dual package hazard (two copies of module state, `instanceof` failing across them) and cannot be fully type-checked from one compilation (TS handbook).
- Mark `"sideEffects": false` only if importing any file truly does nothing; otherwise list the files with side effects (CSS, polyfills).
- Before publishing: `npx publint` and `npx @arethetypeswrong/cli --pack .` must pass.

## 11. Circular imports

Cycles cause `undefined` at import time (`Cannot access 'X' before initialization` in ESM, half-filled `exports` objects in CJS), make module order matter, and defeat code splitting.

- Detect: `npx madge --circular --extensions ts,tsx src`, `npx knip --include cycles` (newer knip versions), dependency-cruiser's `no-circular` rule, or `import-x/no-cycle`. `import-x/no-cycle` is "comparatively computationally expensive"; prefer dependency-cruiser or madge in CI on large repos, and if you use the lint rule set `ignoreExternal: true`. Type-only imports do not create runtime cycles and are ignored by these tools.
- Fix: extract what both modules need into a third module that imports neither; or invert the dependency (pass a function in); or merge two files that are really one concept. Never "fix" a cycle by moving an import inside a function.

## 12. Side effects at import time

- Importing a module must not connect to a database, read env, start timers, register global listeners or do network calls (Node best practices 3.13). Do that in an explicit `start()`/`createApp()` called from the entry point.
- Reason: tests and tools import modules without wanting a running system, import order becomes load-bearing, and serverless cold starts pay for all of it.
- Exception: modules that exist to register something (polyfills, `import "server-only"`, CSS) and are imported by side effect on purpose. They must be named for it.

## 13. Enforcing feature boundaries

For apps organised by feature (`src/features/<name>/`), allow imports from a feature's `public.ts` (or the agreed entry) only, and forbid features from importing each other's internals and `shared/` from importing features.

```js
// eslint.config.js (no plugin needed)
{
  files: ["src/**/*.{ts,tsx}"],
  rules: {
    "no-restricted-imports": ["error", {
      patterns: [{
        regex: "^#/features/[^/]+/(?!public$).+",
        message: "Import another feature only through its public.ts",
      }],
    }],
  },
}
```

For layered rules (`ui` may import `domain`, `domain` may not import `ui`), use dependency-cruiser (`npx depcruise --init`, then `npx depcruise src`) with `forbidden` rules (`from: { path: "^src/domain" }, to: { path: "^src/ui" }`) or `eslint-plugin-boundaries`. Its starter config already includes `no-circular`, `no-orphans`, `not-to-unresolvable`, `not-to-dev-dep`.

## 14. Detecting a mix and migrating

Measure before deciding. Each command prints only problems.

Directories that mix default and named exports in source files:

```bash
rg --files -g '*.{ts,tsx,js,jsx,mts,cts,mjs,cjs}' -g '!*.d.ts' \
   -g '!**/{node_modules,dist,build,.next,coverage}/**' . \
| while read -r f; do
    if rg -q '^export default ' "$f"; then k=default
    elif rg -q '^export ' "$f"; then k=named
    else continue; fi
    printf '%s %s\n' "$(dirname "$f")" "$k"
  done \
| awk '{n[$1,$2]++; d[$1]=1} END {for (x in d) if (n[x,"default"] && n[x,"named"]) printf "MIXED %s default=%d named=%d\n", x, n[x,"default"], n[x,"named"]}' \
| sort
```

Then discard directories where the defaults are framework files (section 2). What remains is a real inconsistency.

Barrels:

```bash
rg -l -g 'index.{ts,tsx,js,jsx,mts}' -g '!**/node_modules/**' '^export (\*|\{[^}]*\}) from' . | wc -l
```

File name case mix per folder (kebab vs Pascal vs camel):

```bash
rg --files -g '*.{ts,tsx,js,jsx}' -g '!**/node_modules/**' . \
| awk -F/ '{f=$NF; sub(/\..*$/,"",f); c = (f ~ /^[A-Z]/) ? "Pascal" : (f ~ /[A-Z]/) ? "camel" : (f ~ /_/) ? "snake" : "kebab"; d=$0; sub(/\/[^\/]*$/,"",d); n[d,c]++; ds[d]=1} END {for (x in ds) {s=""; k=0; split("Pascal camel snake kebab",cs," "); for (i in cs) if (n[x,cs[i]]) {s=s" "cs[i]"="n[x,cs[i]]; k++} if (k>1) print "MIXED " x s}}' | sort
```

Deep relative imports and alias usage:

```bash
rg -c "from '\.\./\.\./\.\./|from \"\.\./\.\./\.\./" -t ts -t js . | sort -t: -k2 -nr | head
rg -o "from ['\"](@/|#/|~/|src/)" -t ts -t js -I . | sort | uniq -c   # more than one root = mixed aliases
```

CJS in an ESM codebase:

```bash
rg -n '\brequire\(|module\.exports|exports\.\w+ =' -t ts -g '!*.cjs' -g '!**/node_modules/**' .
```

Migration rule: do not fix a convention mix inside an unrelated change. Report it with the counts, propose the target convention (the majority one), add the lint rule that blocks new violations first (Atlassian's order), then convert with a codemod in a dedicated change.

## 15. Checks

Always pass an explicit path to `rg` (it reads stdin otherwise).

- **Named exports.** Pass: no `export default` outside framework-mandated files. Verify: `rg -n '^export default' -t ts -t js . | rg -v '/(page|layout|template|loading|error|global-error|not-found|default|route)\.[jt]sx?:|\.config\.|\.stories\.'` returns nothing; lint `import-x/no-default-export` with overrides.
- **No barrels in app code.** Pass: zero `index.*` re-export files outside package entry points. Verify: barrel command in section 14; lint `no-restricted-imports` pattern from section 3.
- **One alias root.** Pass: the alias usage command prints one root. Verify: section 14.
- **No `baseUrl`.** Pass: absent. Verify: `rg -n '"baseUrl"' -g 'tsconfig*.json' .`
- **No deep relative imports.** Pass: no `../../../`. Verify: section 14 command prints nothing.
- **Type-only imports marked.** Pass: `tsc` passes with `verbatimModuleSyntax: true`. Verify: `npx tsc --showConfig | rg verbatimModuleSyntax`.
- **`node:` prefix.** Pass: builtins imported with `node:`. Verify: `rg -nP "from ['\"](fs|path|os|crypto|http|https|url|util|stream|events|child_process|zlib|net|tls|dns|worker_threads|timers|assert|buffer|readline)(/[a-z]+)?['\"]" -t ts -t js .` returns nothing.
- **Explicit module type.** Pass: every `package.json` with source files has `"type"`. Verify: `rg --files-without-match '"type":' -g 'package.json' -g '!**/node_modules/**' .` lists the ones missing it.
- **ESM relative imports have extensions (Node targets, no bundler).** Pass: `tsc` passes under `module: nodenext`. Verify: `npx tsc --noEmit`.
- **No cycles.** Pass: zero cycles. Verify: `npx madge --circular --extensions ts,tsx src` or `npx depcruise src --config`.
- **No unused exports or files.** Pass: knip clean. Verify: `npx knip`.
- **Consistent file naming.** Pass: the case-mix command prints nothing. Verify: section 14; lint `unicorn/filename-case`.
- **Package publishes correctly (libraries).** Pass: both tools clean. Verify: `npx publint && npx @arethetypeswrong/cli --pack .`
- **No import-time side effects.** Pass: no top-level `await connect(`, `setInterval(`, `listen(` in non-entry modules. Verify: `rg -n '^(await |[a-zA-Z_.]+\.(listen|connect)\(|setInterval\()' -t ts -t js src`
