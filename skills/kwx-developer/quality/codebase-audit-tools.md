# Codebase audit tools: what each finds, the exact command, how to read it

The audit reads a repo and finds organisation problems: mixed export and import styles, naming mixes, duplicated helpers, layering violations, dead code, cycles, inconsistent error handling, risky code without tests. Tools find candidates fast; the agent confirms each one by reading code, then asks the owner what to do ([tech-debt-and-todo.md](tech-debt-and-todo.md)). Commands were run on real repos on 2026-10-30 (a 514 file React and NestJS app, a Next.js app, a 165 file Rust workspace) and times are from those runs, except where a section says "not run here" (scc, ts-prune, cargo-udeps, cargo-modules, the ESLint plugins): those come from their docs.

## Contents

0. Rules for every audit
1. Run order and time budget
2. Size: tokei, scc
3. Cycles and layers: dependency-cruiser, madge, ESLint plugins
4. Dead code: knip, ts-prune, cargo-machete, cargo-udeps, cargo-modules
5. Duplication: jscpd and the same-name helper finder
6. Convention census: find the majority, then the outliers
7. Custom structural rules: ast-grep and semgrep
8. Rust lints: clippy as an audit tool
9. Risky code without tests
10. From tool output to findings
11. Checks

## 0. Rules for every audit

1. **Read `DECISIONS.md` first** (and `CLAUDE.md`, `AGENTS.md`, `docs/decisions/`). Build the do-not-flag list before running anything ([decision-records.md](decision-records.md) section 6). A recorded decision is never reported again.
2. **Read `TODO.md` second.** A problem already listed there is not a new finding ([tech-debt-and-todo.md](tech-debt-and-todo.md) section 5).
3. **Run the project's own checks before outside tools**: `npm run typecheck`, `npm run lint`, `cargo clippy`, the test suite. Failures there outrank everything an outside tool says.
4. **Do not install anything into the project** to audit it. Use `npx -y`, `uvx`, or a throwaway prefix in the scratchpad (`npm i --prefix "$SCRATCH/tools" ...`, `cargo install --root "$SCRATCH/tools" ...`). Writing configs (`knip.json`, `.dependency-cruiser.cjs`, `sgconfig.yml`) into the repo is a fix, and fixes need the owner's yes. Keep audit configs in the scratchpad and pass them with `--config`.
5. **A tool that reports 0 files, 0 modules or nothing at all is broken until proven clean.** dependency-cruiser run through `npx` printed `no dependency violations found (0 modules, 0 dependencies cruised)` and exited 0 on a 514 file repo, because it could not load TypeScript. Always read the "N files / N modules analyzed" line.
6. **Prefer compiler backed tools over grep.** `grep '\.unwrap()\|\.expect('` counted 227 hits in one Rust crate; `clippy::expect_used` on non-test targets found 1. Grep cannot see `#[cfg(test)]`, type-only imports, or macros. Use grep for the census (section 6), then confirm with a parser based tool.
7. **One finding per pattern, not per line.** 41 files exporting one way and 1 file the other way is one finding about that 1 file. 1070 `cast_precision_loss` warnings in a renderer are one question ("are lossy float casts accepted here?"), not 1070.
8. **Framework mandated shapes are never findings.** Next.js `page.tsx`, `layout.tsx`, `route.ts` (default export, `GET`/`POST` names), Expo Router screens, Storybook stories, `*.config.ts`, Vite and Vitest configs, Rust `main.rs`/`build.rs`. Exclude them from every census and rule.

## 1. Run order and time budget

Fast, high signal tools first. Total wall time for a mid size repo is under two minutes.

| Step | Tool | Finds | Measured time |
|---|---|---|---|
| 1 | `git` hotspots ([hotspots.md](hotspots.md)) | Where changes land, for ranking | under 1 s |
| 2 | tokei or scc | Size per language and file, the largest files | 0.01 s |
| 3 | Project checks (tsc, eslint, clippy, tests) | Real errors | 9 s clippy warm |
| 4 | dependency-cruiser (TS/JS), cargo-modules (Rust) | Runtime cycles, layer violations, orphans | 1 s |
| 5 | knip (TS/JS), cargo-machete (Rust) | Unused files, exports, dependencies | 2.5 s, 0.04 s |
| 6 | jscpd | Copy paste blocks | 6 s |
| 7 | Census greps and ast-grep | Style mixes per folder | under 1 s each |
| 8 | Test gap check (section 9) | Hotspots with no test | under 1 s |

semgrep (5 s per rule run through `uvx`, plus a one time download) only when an ast-grep rule cannot express the pattern.

## 2. Size: tokei and scc

```bash
tokei . -s code                       # per language: files, lines, code, comments, blanks
tokei src --files -s code -t Rust     # per file, largest first
scc --by-file -s complexity --no-cocomo --exclude-dir node_modules,dist,target .
scc --format json --by-file . > /tmp/scc.json
```

- tokei is installable with `cargo install tokei` (15.0.0, about a minute to build). scc is a Go binary (`go install github.com/boyter/scc/v4@latest`) and adds a `Complexity` column: a count of branch tokens (`if`, `for`, `&&`, ...) comparable only between files of the same language.
- Read: a file over ~800 code lines in TS or ~1500 in Rust that is ALSO a hotspot is a split candidate. A large cold file is not a finding.

## 3. Cycles and layers

### dependency-cruiser (default for TS/JS)

Validates the import graph against rules: cycles, orphans, layer boundaries, dev deps in production code. Version 18.7.0 tested.

Gotcha found in testing: through `npx -y -p dependency-cruiser depcruise ...` it could not load the project's TypeScript (5.9.3 installed in the repo) and silently cruised 0 modules. Install it next to TypeScript 5 (it does not support TypeScript 7 yet) in a scratch prefix and run that binary from the repo root:

```bash
T="$SCRATCH/tools/dc"; mkdir -p "$T" && npm i --prefix "$T" dependency-cruiser@18 typescript@5
cd /path/to/repo && "$T/node_modules/.bin/depcruise" src --config "$SCRATCH/depcruise.cjs"
echo $?   # exit code = number of error severity violations
```

Audit config (keep it in the scratchpad; add a layer rule per boundary the project claims in its docs):

```js
// depcruise.cjs
module.exports = {
  forbidden: [
    // type-only cycles are harmless at runtime; only report real ones
    { name: "no-circular-at-runtime", severity: "error", from: {},
      to: { circular: true, viaOnly: { dependencyTypesNot: ["type-only"] } } },
    { name: "no-orphans", severity: "warn",
      from: { orphan: true, pathNot: ["\\.d\\.ts$", "\\.(test|spec)\\.tsx?$", "(^|/)test/", "\\.config\\."] }, to: {} },
    // layer rule: a claimed boundary ("geometry is pure, no UI or store imports")
    { name: "geometry-is-pure", severity: "error",
      from: { path: "^src/geometry/", pathNot: "\\.test\\.tsx?$" },
      to: { path: "^(src/(components|store|scene)/|node_modules/three)" } },
    // features never import each other ($1 is the captured folder)
    { name: "no-cross-feature", severity: "error",
      from: { path: "^src/features/([^/]+)/" },
      to: { path: "^src/features/([^/]+)/", pathNot: "^src/features/$1/" } },
    { name: "not-to-dev-dep", severity: "error",
      from: { path: "^src", pathNot: "\\.(test|spec)\\." }, to: { dependencyTypes: ["npm-dev"] } },
  ],
  options: {
    doNotFollow: { path: "node_modules" },
    tsConfig: { fileName: "tsconfig.json" },   // tsconfig.app.json in Vite projects
    tsPreCompilationDeps: true,                 // needed to see type-only imports at all
  },
};
```

Output (`err` reporter):

```
  error no-circular-at-runtime: src/geometry/bridges.ts →
      src/geometry/energy.ts →
      src/geometry/bridges.ts
  error geometry-is-pure: src/geometry/notes.test.ts → src/store/building.ts
x 2 dependency violations (2 errors, 0 warnings). 563 modules, 3271 dependencies cruised.
```

Read: each `error` line is a candidate. Confirm the import in the file. The second line above is a test importing the store: exclude tests from layer rules (`pathNot`) unless the project says tests must respect layers. Other outputs: `-T err-long` (adds the rule comment), `-T json`, `-T mermaid`, `--focus "^src/store"` (one area and its neighbours), `--affected main` (only what changed since main).

To adopt in the repo later (only after the owner says yes): `npx depcruise --init`, then `depcruise src --baseline` writes `.dependency-cruiser-known-violations.json` and `--ignore-known` stops old violations failing CI while new ones still do.

### madge (fast cycle list, overreports)

```bash
npx -y madge --circular --extensions ts,tsx --ts-config tsconfig.json --no-spinner src   # exit 1 when cycles exist
npx -y madge --orphans --extensions ts,tsx src
npx -y madge --circular --image cycles.svg src   # needs Graphviz
```

madge 8.0.0 reported 5 cycles on the test repo; dependency-cruiser with `viaOnly` reported 1. The other 4 were `import type` edges (for example `store/building.ts` imports a value from `lib/storage.ts`, which imports only `type Theme` back). Use madge for a 2 second first look; confirm every cycle by opening both imports, or use dependency-cruiser. Type-only cycles are not findings.

### ESLint plugins (enforcement, not discovery)

- `eslint-plugin-import-x` (fork of `eslint-plugin-import` with a Rust resolver and 16 dependencies instead of 117): `import-x/no-default-export`, `import-x/prefer-default-export`, `import-x/no-cycle`, `import-x/no-restricted-paths`, `import-x/no-duplicates`, `import-x/consistent-type-specifier-style`, `import-x/order`. `no-cycle` resolves the import graph from every file it lints, which makes it slow on large repos; for discovery use dependency-cruiser, and keep `no-cycle` in the lint config only if lint time stays acceptable.
- `eslint-plugin-boundaries`: element types by folder pattern plus an allow list. Current rule name is `boundaries/dependencies` with `default: "disallow"` and `policies`; older docs and configs use `boundaries/element-types`. Check the installed version's docs before writing config.

```js
// eslint.config.js (sketch, boundaries v6 style)
settings: { "boundaries/elements": [
  { type: "ui", pattern: "src/components/*" }, { type: "domain", pattern: "src/domain/*" }, { type: "data", pattern: "src/data/*" } ] },
rules: { "boundaries/dependencies": [2, { default: "disallow", policies: [
  { from: { element: { type: "ui" } }, allow: { to: { element: { type: "domain" } } } },
  { from: { element: { type: "domain" } }, allow: { to: { element: { type: "data" } } } } ] }] }
```

Recommend these to the owner as the FIX for a recorded layering decision (the rule enforces it from then on), not as audit tools.

### Rust: cargo-modules

```bash
cargo install cargo-modules
cargo modules structure --lib -p my-crate --no-fns --no-traits --no-types   # module tree
cargo modules dependencies --lib -p my-crate --no-externs --no-sysroot --no-fns --no-traits --no-types --acyclic
cargo modules orphans --lib -p my-crate --deny   # .rs files not linked into the module tree (dead files)
```

`--acyclic` fails with "Circular dependency between ..." and the path. Rust allows module cycles inside one crate, so a cycle is a finding only when it crosses a boundary the project claims (for example `domain` using `ui`). Cycles between crates are impossible (Cargo rejects them), so cross crate layering is checked by reading each `Cargo.toml` `[dependencies]` list against the intended order.

## 4. Dead code

### knip (default for TS/JS)

Finds unused files, exports, types, dependencies, unlisted dependencies, duplicate exports (`duplicates`: one thing exported twice) and, in recent versions, cycles. Version 6.44.0 tested; 2.5 s on 514 files.

```bash
npx -y knip --reporter compact                                    # everything
npx -y knip --include files,exports,types,duplicates --reporter compact
npx -y knip --production --reporter compact                       # ignore tests and dev deps: what ships
npx -y knip --reporter json > /tmp/knip.json                      # {"issues":[{"file":..., "exports":[{"name","line","col"}]}]}
```

Exit codes: 0 no issues, 1 issues, 2 knip itself failed.

False positive traps measured on the test repo:

- **Nested packages that are not npm workspaces.** Root run reported 9 "unused files" (the server's `main.ts`, the CLI entry) and 46 "unlisted dependencies" (every `@nestjs/*` import) because `server/` and `lod2/*` have their own `package.json` but no `workspaces` field. Fix: a scratch `knip.json` with a `workspaces` map, or run knip inside each package.
- **Exports used only in their own file.** 39 "unused exports" dropped to 3 with `"ignoreExportsUsedInFile": true`. Most were constants exported "just in case". That is a style question for the owner (one finding), not 36 dead code findings.

```json
{
  "$schema": "https://unpkg.com/knip@6/schema.json",
  "ignoreExportsUsedInFile": true,
  "workspaces": {
    ".": { "entry": ["src/main.tsx", "scripts/*.mjs"], "project": ["src/**/*.{ts,tsx}"] },
    "server": { "entry": ["src/main.ts", "scripts/*.ts"], "project": ["src/**/*.ts"] }
  }
}
```

Run with `npx -y knip --config "$SCRATCH/knip.json"`. Intentional public exports (a library's API) are marked in code with a JSDoc tag and excluded with `"tags": ["-lintignore"]`, which is how outcome (c) is recorded for knip.

Before reporting an unused file: grep for dynamic use (`import(`, `require(`, string paths in configs, `lazy(() => import(...))`, route files picked up by convention). Before reporting an unused dependency: check `package.json` scripts, config files, and `@types/*` pairs.

### ts-prune (fallback)

```bash
npx -y ts-prune -p tsconfig.json -u    # file:line - exportName ; -u hides "(used in module)"
npx -y ts-prune -e                     # exit 1 when findings remain
```

Its README says it was revived after a long hiatus. Use it only when knip cannot run (odd build setup); it finds unused exports only, no files or dependencies.

### Rust: cargo-machete, cargo-udeps, compiler

```bash
cargo install cargo-machete --locked
cargo machete                  # 0.04 s on a 9 crate workspace; exit 1 when unused deps found
cargo machete --with-metadata  # fewer false positives, may rewrite Cargo.lock (do not run without asking)
```

Output names the crate, its `Cargo.toml` and the unused dependency (`sahna -- ./crates/sahna-cli/Cargo.toml: sahna-audio`). Confirm with `grep -rn 'sahna_audio' crates/sahna-cli/src` (dash becomes underscore in code). machete is a text search: macros that use a crate without naming it, or renamed crates, are false positives; record them as `[package.metadata.cargo-machete] ignored = ["crate"]`.

```bash
cargo install cargo-udeps --locked
cargo +nightly udeps --workspace --all-targets   # precise, compiles everything, needs nightly; ignores doc-test-only use
```

Use udeps only when machete's answer is disputed. Dead functions and modules inside a crate: `cargo build` already warns (`dead_code`); `pub` items in a binary crate escape that lint, so check them with `cargo modules orphans` and by reading.

## 5. Duplication

### jscpd

```bash
npx -y jscpd@4 src --min-tokens 70 --min-lines 8 --gitignore \
  --ignore "**/*.test.ts,**/*.test.tsx,**/*.spec.*,**/generated/**" \
  --reporters console,json --output "$SCRATCH/jscpd"
```

Defaults are `--min-lines 5 --min-tokens 50`; on a real codebase that is noisy (JSX prop blocks, import lists). 70 tokens and 8 lines gave 5 clones in 516 files, each worth reading. `--threshold N` exits non zero above N% duplicated lines (CI use). A 5.x line exists (5.4.2 seen); only 4.3.0 was run here, so pin `@4` or check `--help` before using 5.x options.

Output: `Clone found (tsx): - a.tsx [42:47 - 62:21] (20 lines, 213 tokens)  b.tsx [41:43 - 61:30]` plus a table per format with duplicated line percentages. JSON lands in `$SCRATCH/jscpd/jscpd-report.json` (`duplicates[].firstFile.name`, `.secondFile.name`, `.lines`).

Read: a clone inside one file (`Storey.tsx` lines 69 to 109 and 117 to 147) is a missing local function. A clone across two sibling files (`InteriorWallTool.tsx` and `MeasureTool.tsx`) is a missing shared hook or helper; check change coupling for the pair ([hotspots.md](hotspots.md) section 6): if they also change together, the duplication is costing edits now. Two similar test setups are usually fine. jscpd works for Rust too (`--format rust`).

### Same-name helper finder (catches rewritten, not copied, helpers)

jscpd misses a helper that was rewritten twice with different code. Find exported functions with the same name in two or more files:

```bash
git ls-files '*.ts' '*.tsx' | grep -vE '\.(test|spec)\.|\.d\.ts$|(^|/)(page|layout|route)\.tsx?$' \
 | xargs grep -HoE '^export (async )?function [A-Za-z0-9_]+|^export const [A-Za-z0-9_]+ = (async )?\(' \
 | sed -E 's/:export (async )?(function|const) / /; s/ = .*//' \
 | awk '{n[$2]++; f[$2]=f[$2]" "$1} END{for(k in n) if(n[k]>1) print n[k], k, f[k]}' | sort -rn
```

On the Next.js test repo, without the `route.ts` exclusion this listed `GET` 32 times and `POST` 32 times (framework names, rule 8). With it, the real hit was `plural` defined in two component files: one finding, "two copies of a pluralisation helper". Rust equivalent: `grep -rhoE '^\s*pub(\(crate\))? fn [a-z0-9_]+' crates/*/src | sort | uniq -d`.

## 6. Convention census: find the majority, then the outliers

An inconsistency is relative to the folder's own majority, not to your taste. Count first, then flag the minority. Google's review guide: when the style guide is silent, be consistent with the surrounding code, and file the cleanup of existing inconsistencies separately ([looking-for](https://google.github.io/eng-practices/review/reviewer/looking-for.html)).

Export style per folder (default vs named), TS/JS:

```bash
git ls-files '*.ts' '*.tsx' '*.js' '*.jsx' | grep -vE '\.d\.ts$|\.config\.|(^|/)(page|layout|route|loading|error|not-found)\.tsx?$' \
 | while read f; do d=$(dirname "$f")
     if grep -qE '^export default|^export \{[^}]*as default' "$f"; then echo "$d D"
     elif grep -qE '^export (const|let|function|async function|class|type|interface|enum|\{)' "$f"; then echo "$d N"; fi
   done | sort | uniq -c | awk '{a[$2]=a[$2]" "$3"="$1} END{for(k in a) print k":"a[k]}' | grep ' D=' | grep ' N='
```

Output `lib: D=1 N=41` means 41 files export by name and 1 by default: one finding about that one file. `D=5 N=3` is a real split: ask which style the folder should use (and whether the split is intentional, for example components default, hooks named).

File name case per folder (single lowercase words count as compatible with any style):

```bash
git ls-files '*.ts' '*.tsx' | grep -v '\.d\.ts$' | awk -F/ '{b=$NF; sub(/\..*$/,"",b)
  c = b ~ /^[A-Z][A-Za-z0-9]*$/ ? "Pascal" : b ~ /-/ ? "kebab" : b ~ /_/ ? "snake" : b ~ /[A-Z]/ ? "camel" : ""
  if (c=="") next; d=$0; sub(/\/[^\/]*$/,"",d); k[d" "c]++}
  END{for(x in k) print x, k[x]}' | sort | awk '{a[$1]=a[$1]" "$2"="$3; n[$1]++} END{for(d in a) if(n[d]>1) print d":"a[d]}'
```

PascalCase components next to camelCase hooks in one folder is the usual React convention, not a mix; flag only a mix inside one kind (two components, one `UserCard.tsx` and one `order-card.tsx`).

Import style (deep relative paths next to an alias):

```bash
git ls-files '*.ts' '*.tsx' | xargs grep -hoE "from ['\"](\.\./\.\./|@/|~/)" | sort | uniq -c
```

`466 from "@/` against `36 from "../../` means the alias is the convention and the 36 are outliers; `eslint-plugin-import-x/no-relative-packages` or `no-restricted-imports` with a `../../*` pattern enforces it after the owner agrees.

Error handling style. Look for more than one way to report failure in the same layer:

| Language | Census command | Mix that is a finding |
|---|---|---|
| TS | `grep -rnE 'catch \(\w*\) \{\s*\}' src` | Empty catch blocks (errors swallowed) |
| TS | `grep -rlE 'throw new' src/api src/services` vs `grep -rlE 'return \{ ?(ok\|error):' ...` | One service throws, its sibling returns `{ ok, error }` |
| TS | `grep -rnE '\.catch\(\(\) => (null\|undefined\|\{\})\)' src` | Silent fallbacks hiding failures |
| Rust | `for c in crates/*/; do printf '%s anyhow=%s thiserror=%s\n' $c $(grep -c '^anyhow' $c/Cargo.toml) $(grep -c '^thiserror' $c/Cargo.toml); done` | A library crate returning `anyhow::Error` across its public API while sibling libraries define error enums (convention: `thiserror` in libraries, `anyhow` in binaries; if the whole workspace uses `anyhow` consistently, that is a decision to record, not a finding) |
| Rust | clippy restriction lints, section 8 | `unwrap`/`expect`/`println!` in library code |

Other mixes worth one census each: `function` declarations vs `const x = () =>` for exported functions, `interface` vs `type` for object shapes, `enum` vs union of string literals, sync vs async file APIs in Node, `console.log` vs the project logger, `tracing` vs `log` vs `println!` in Rust. Formatting (quotes, semicolons, trailing commas) is never a finding when a formatter is configured; if none is configured, the single finding is "add Prettier, Biome or rustfmt".

## 7. Custom structural rules: ast-grep and semgrep

Both match syntax trees, so comments and strings never match. Neither can say "this folder's majority is named exports"; the census decides the convention, then a rule scoped to the folder by glob catches the outliers and keeps catching new ones.

### ast-grep (default: fast, no account, Rust and TS)

```bash
npx -y -p @ast-grep/cli ast-grep --version            # 0.51.0; plain `npx @ast-grep/cli` fails ("could not determine executable")
npx -y -p @ast-grep/cli ast-grep run -l ts -p 'export default $X' lib          # ad hoc search
npx -y -p @ast-grep/cli ast-grep scan --rule "$SCRATCH/rules/lib-named.yml"    # run from the repo root
```

Rule: default export in a folder that uses named exports. `files` globs resolve against the project root (the folder holding `sgconfig.yml`, or the working directory with `--rule`); run from the repo root or nothing matches and the scan exits 0 silently.

```yaml
# lib-named.yml
id: lib-named-exports-only
language: TypeScript          # use Tsx for .tsx files; one language per rule
severity: error               # error makes `scan` exit 1
message: lib/ exports by name (41 of 42 files do). Use `export function` or `export const`.
note: Decided in DECISIONS.md D-07. Next.js route files are exempt; they need a default export.
files:
  - lib/**/*.ts
ignores:
  - lib/**/*.test.ts
rule:
  any:
    - kind: export_statement
      regex: ^export\s+default\b
    - pattern: export { $$$A as default }
```

Real output:

```
error[lib-named-exports-only]: lib/ exports by name (41 of 42 files do). Use `export function` or `export const`.
   ┌─ lib/cropUtils.ts:14:1
14 │ ╭ export default async function getCroppedImg(
```

More rules that catch common inconsistencies:

```yaml
# Rust: no unwrap in library code outside tests (clippy::unwrap_used does the same with type info; use this when clippy is not configured)
id: no-unwrap-in-lib
language: Rust
severity: warning
message: Return an error instead of unwrap() in library code.
files: [ "crates/*/src/**/*.rs" ]
ignores: [ "crates/*/src/main.rs", "crates/*/src/bin/**" ]
rule:
  pattern: $E.unwrap()
  not:
    inside:
      kind: mod_item
      follows:                  # #[cfg(test)] is a sibling node before `mod tests`, not a child
        kind: attribute_item
        regex: cfg\(test\)
      stopBy: end
---
# TS: fetch() called outside the API layer (layering)
id: fetch-only-in-api
language: Tsx
severity: error
message: Network calls go through src/api. Call an api/ function instead.
files: [ "src/**/*.tsx" ]
ignores: [ "src/api/**" ]
rule:
  pattern: fetch($$$ARGS)
---
# TS: swallowed error
id: empty-catch
language: TypeScript
severity: warning
message: Empty catch hides the failure. Log it, rethrow it, or return an error value.
rule:
  kind: catch_clause
  has:
    field: body
    kind: statement_block
    not:                        # flags `catch {}` and `catch { /* ignore */ }`, not `{ log(e) }` or `{ return null }`
      has:
        any:
          - kind: expression_statement
          - kind: return_statement
          - kind: throw_statement
          - kind: lexical_declaration
          - kind: variable_declaration
          - kind: if_statement
```

All three rules were run against a known bad and a known good file. Several rules in one file are separated by `---`. For a permanent setup (after the owner agrees), put rules in `rules/` and `sgconfig.yml` (`ruleDirs: [rules]`) at the repo root, then `ast-grep scan` with no arguments. `fix:` rewrites (`ast-grep scan --rule r.yml -U` applies all); a fix is outcome (b) and needs a plan first. Test a rule on one known bad and one known good file before trusting a clean result.

### semgrep (when you need taint, cross function data flow, or the registry)

```bash
uvx semgrep --config "$SCRATCH/semgrep-lib.yml" --metrics=off --error --quiet lib   # exit 1 on findings with --error
uvx semgrep -e 'export default $X' --lang ts --metrics=off --json lib               # ad hoc
```

`--metrics=off` stops usage reporting. semgrep 1.183.0 tested: one pattern `export default $X` matched `export default async function f()`, `export default x;` and `export { a as default }`. Listing extra `pattern-either` branches for the function form reported the same line twice.

```yaml
rules:
  - id: lib-named-exports-only
    languages: [typescript]
    severity: ERROR            # newer names: HIGH, MEDIUM, LOW, CRITICAL (ERROR maps to HIGH)
    message: lib/ exports by name. Export `$X` by name instead of default.
    paths:
      include: ["/lib/**/*.ts"]      # leading slash anchors to the repo root
      exclude: ["*.test.ts"]
    pattern: export default $X
```

Rules match within one file; `paths` selects files and cannot make one file's result depend on another's. ast-grep is faster and needs no Python; reach for semgrep for `pattern-inside` plus `metavariable-regex` combinations or taint mode.

## 8. Rust lints: clippy as an audit tool

```bash
cargo clippy --workspace --all-targets -- -D warnings      # the project's own bar; any warning is a finding
# tally pedantic lints by name, deduplicated by location (raw counts double across lib and test targets)
cargo clippy --workspace --all-targets --message-format=json -- -W clippy::pedantic 2>/dev/null \
  | jq -r 'select(.reason=="compiler-message") | .message | select(.code) | "\(.code.code) \(.spans[0].file_name):\(.spans[0].line_start)"' \
  | sort -u | awk '{print $1}' | sort | uniq -c | sort -rn | head -20
# audit lints for library code only: --lib --bins leaves #[cfg(test)] code uncompiled
cargo clippy --workspace --lib --bins --message-format=json -- \
  -W clippy::unwrap_used -W clippy::expect_used -W clippy::print_stdout -W clippy::print_stderr -W clippy::todo -W clippy::dbg_macro 2>/dev/null \
  | jq -r 'select(.reason=="compiler-message") | .message | select(.code) | "\(.code.code) \(.spans[0].file_name | split("/")[1])"' | sort | uniq -c | sort -rn
```

`--message-format=short` drops the lint name; use JSON plus `jq` to tally. Measured on the Rust workspace (clean at default level): pedantic produced 1070 `cast_precision_loss`, 878 `must_use_candidate`, 695 `cast_possible_truncation`, 96 `too_many_lines`. In a renderer, float casts are expected: that is ONE question to the owner per lint, and a "keep" answer becomes a `[lints.clippy]` entry, not 1070 TODO lines. `too_many_lines` intersected with the hotspot list is the useful part.

Recording decisions in the manifest (Rust 1.74+ `[lints]`; members opt in with `[lints] workspace = true`):

```toml
[workspace.lints.clippy]
pedantic = { level = "warn", priority = -1 }   # group first, lower priority, so single lints below override it
cast_precision_loss = "allow"                  # D-12: lossy f32 casts are expected in the renderer
must_use_candidate = "allow"
```

For a single intentional spot use `#[expect(clippy::too_many_lines, reason = "D-14: one match over every effect kind")]` (stable since Rust 1.81). Unlike `allow`, `expect` warns when the lint no longer fires, so stale exemptions surface by themselves.

## 9. Risky code without tests

Risky means: money, auth, permissions, persistence or migrations, sync and concurrency, parsing untrusted input, and any hotspot. For each top hotspot or risky file, check whether any test imports it:

```bash
git log --since="12 months ago" --format=format: --name-only --no-renames -- 'lib/*.ts' 'src/**/*.ts' 'app/api/**/*.ts' \
 | grep -v '^$' | grep -vE '\.(test|spec)\.' | sort | uniq -c | sort -rn | head -20 \
 | while read n f; do [ -f "$f" ] || continue
     s=${f%.*}; s=${s%/index}; k=$(echo "$s" | awk -F/ '{print (NF>1 ? $(NF-1)"/"$NF : $NF)}')   # last two path segments
     t=$(git ls-files | grep -E '\.(test|spec)\.[jt]sx?$' \
         | xargs grep -lE "(from|import\() *['\"][^'\"]*${k//[/\\[}['\"]" 2>/dev/null | head -1)        # real imports only
     printf "%4d  %-50s %s\n" "$n" "$f" "${t:-NO TEST}"; done
```

Real output (Next.js repo):

```
  20  app/api/checkout/route.ts                          app/api/__tests__/promocodeEconomics.test.ts
  11  app/api/admin/orders/route.ts                      NO TEST
   7  lib/telegramClient.ts                              NO TEST
```

Two traps found while building this: matching only the file's base name (`route`) missed the test that imports `@/app/api/checkout/route`, and a plain text search counted `vi.mock("@/lib/telegramClient")` as a test of that file. A mock is the opposite of a test of the module. The command matches `from '...'` and `import('...')` with the last two path segments. It is still a heuristic (it misses tests that hit a route over HTTP by URL): open the test folder before reporting. Admin order routes changed 11 times this year with no test is a P1 candidate if they move money or permissions. Rust: a module with no `#[cfg(test)]` block and no `tests/*.rs` that names it: `grep -L 'cfg(test)' crates/*/src/*.rs`.

When the project has coverage, use it instead of the heuristic: `npx vitest run --coverage --coverage.reporter=json-summary` (TS) or `cargo llvm-cov --workspace --json --summary-only` (Rust), then list hotspot files under 50% line coverage. Never report a coverage percentage for the whole repo as a finding; report named risky files.

## 10. From tool output to findings

Every candidate goes through this before it reaches the owner:

1. **Confirm by reading.** Open the file at the reported line. Drop false positives silently (but if a tool's false positives repeat, fix the scratch config).
2. **Check the do-not-flag list** from `DECISIONS.md` and the TODO list. Drop matches.
3. **Group.** One finding per pattern per area: "3 files in `lib/` export by default; the other 41 export by name".
4. **Give it a key**: `kind:area`, with `kind` from this fixed list so DECISIONS.md and TODO.md can match it later:

| kind | Example key |
|---|---|
| `export-style` | `export-style:lib` |
| `naming` | `naming:src/components` |
| `import-style` | `import-style:src` |
| `duplicate` | `duplicate:plural-helper` |
| `layering` | `layering:geometry->store` |
| `cycle` | `cycle:geometry/energy<->bridges` |
| `dead-code` | `dead-code:src/test/setup.ts` |
| `unused-dep` | `unused-dep:sahna-cli/sahna-audio` |
| `error-handling` | `error-handling:api-throw-vs-result` |
| `untested-risk` | `untested-risk:app/api/checkout` |
| `hotspot` | `hotspot:sahna-editor/app.rs` |
| `coupling` | `coupling:core/text<->text/lib` |
| `lint` | `lint:clippy::cast_precision_loss` |

5. **Rank** by hotspot rank, then risk ([tech-debt-and-todo.md](tech-debt-and-todo.md) section 3).
6. **Ask** the owner per finding ([tech-debt-and-todo.md](tech-debt-and-todo.md) section 2).

## 11. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| Decisions read first | Audit notes list the D-ids loaded before tools ran | Read the audit log or report header |
| No tool installed into the repo | `git status --porcelain` shows no new `package.json` changes, configs or lockfile edits after the audit | `git status --porcelain` before and after |
| No silent empty run | Every tool's output shows a nonzero file or module count | Grep each output for `0 modules`, `0 files`, `Found 0` |
| dependency-cruiser saw TypeScript | No `missing-tsc-transpiler` warning; module count close to `git ls-files 'src/*.ts*' \| wc -l` | Read the summary line |
| Type-only cycles excluded | Every cycle finding has a value import in both directions | Open both files; `grep -n "^import [^t]"` |
| knip configured for nested packages | No "unlisted dependencies" for packages declared in a nested `package.json` | Compare with `find . -name package.json -not -path '*/node_modules/*'` |
| Framework files excluded | No finding on `page.tsx`, `layout.tsx`, `route.ts` default exports or `GET`/`POST` names | Grep the findings list |
| One finding per pattern | No two findings share a key | `cut -d' ' -f1 findings \| sort \| uniq -d` is empty |
| Convention from majority | Each style finding states the counts (`D=1 N=41`) | Read the finding |
| Clippy tallied by lint, deduped | Lint findings quote counts per lint name, not raw message totals | Read the finding |
| Every finding confirmed | Each finding cites a file and line the agent opened | Read the finding |
