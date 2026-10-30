# Consistency: one codebase, one way

A codebase should read as if one person wrote it. This file lists the dimensions on which code drifts, how to detect drift in each, how to decide which variant is the house convention, and when a variant is not drift at all. Use it in two modes: before writing (find the convention and follow it) and in audits (find every place where two conventions coexist).

## Contents

1. Why consistency is worth enforcing
2. Deciding the house convention (precedence)
3. Legitimate differences that are not drift
4. The scan: run this first
5. Cross-language dimensions
6. TypeScript and JavaScript dimensions
7. Rust dimensions
8. Dependency level consistency (two libraries for one job)
9. Fixing drift without making it worse
10. Checks

## 1. Why consistency is worth enforcing

- Readers "chunk" familiar patterns. Every second way of doing a thing doubles what a reader must recognise (Software Engineering at Google, ch. 8).
- Tools only work on code that follows the rules they assume: a grep for importers, a codemod, a lint rule, an agent searching for "the way we do X". Mixed code makes every search silently incomplete, which is an unknown unknown.
- Mixed conventions spread. A new contributor (or agent) copies whichever example it opened first, so a 90/10 split drifts toward 50/50 unless someone decides.
- The decision matters more than the choice. "It's the consistency of having one answer rather than the answer itself that is the valuable part" (Google). Default export vs named export, `function` vs arrow, `mod.rs` vs `foo.rs`: either is fine. Both is not.
- Google's code review rule: style guide first; where it is silent, "the author should maintain consistency with the existing code"; file a cleanup for existing inconsistency rather than adding a third way.

## 2. Deciding the house convention (precedence)

When the code is mixed, decide by this order and stop at the first that gives an answer. State the source in the PR or finding.

1. **Enforced tooling.** A lint rule, formatter, compiler setting or CI check that already requires one variant (`import/no-default-export`, `func-style`, `@typescript-eslint/consistent-type-definitions`, `unicorn/filename-case`, clippy `mod_module_files`). Code that violates an enforced rule is a bug, not a convention.
2. **Written rules.** CONTRIBUTING, ARCHITECTURE.md, ADRs, a style guide linked from the README, a comment in a config file.
3. **Direction of travel.** What the newest code uses. If the team started moving from A to B, B is the convention even if A is still the majority. Find it with: `git log --diff-filter=A --name-only --format= --since=6.months -- '*.ts' '*.tsx' | head -50` then check those files; or `git log -S 'export default' --oneline | head` to see whether a pattern is being added or removed.
4. **Majority in the area you are editing** (the feature folder, the crate). Local consistency beats global when the area is a clear unit with its own owners.
5. **Majority of the repo.** Use `scan_conventions.py`.
6. **Language and ecosystem standard.** Rust API Guidelines, `rustfmt` and clippy defaults; for TS the framework's documented style, then Google's TS style guide.

If two sources disagree (docs say A, all new code does B), report it as a finding: the docs or the code are wrong, and someone must decide.

## 3. Legitimate differences that are not drift

Do not report these as inconsistency. Check for them before flagging.

- **Framework mandated forms.** Default exports for Next.js `page.tsx`, `layout.tsx`, `route` handlers in some frameworks, Expo Router route files, Storybook CSF files, config files (`next.config.ts`, `vite.config.ts`, `tailwind.config.ts`, `metro.config.js`). File naming forced by the framework (`page.tsx`, `+layout.svelte`, `_layout.tsx`, `[id].tsx`).
- **Library vs binary in Rust.** Libraries return typed errors (`thiserror` style enums); binaries and tests use `anyhow`. A library crate with its own error type next to an `anyhow` binary is correct.
- **Unit vs integration tests in Rust.** Inline `#[cfg(test)] mod tests` for unit tests and `tests/` for integration tests is the standard split, not a mix.
- **Tests and scripts.** `unwrap()` in tests, `console.log` in CLI scripts, `println!` in a CLI's user facing output (as opposed to diagnostics).
- **Generated code** (`*.generated.ts`, protobuf, OpenAPI clients, Supabase types, `build.rs` output). Exclude it from scans.
- **Different runtimes.** A Supabase Edge function (Deno) importing by URL next to a Node app importing by package name.
- **A boundary that intentionally differs.** A public package that uses a barrel `index.ts` as its entry point while app code imports files directly is correct: library entry points are the one good use of barrels.

## 4. The scan: run this first

```
python3 -I ${CLAUDE_SKILL_DIR}/scripts/scan_conventions.py <repo> [--depth 3] [--min 3]
```

It counts each variant per dimension per area (first N directory levels), prints the repo majority and flags areas as `OFF` (the area's own majority is a different variant) or `MIX` (the majority variant, with 20 percent or more of another). The counts are regex based leads. For every flagged line, open two files from each side and confirm before reporting; check section 3 for legitimate differences.

What the scan cannot see (check by reading): naming vocabulary, error translation at boundaries, where validation happens, state management choice, component structure, dependency direction. Those are covered below and in `modules-and-boundaries.md`.

## 5. Cross-language dimensions

For each: what drifts, how to detect, what to decide.

| Dimension | Drift looks like | Detect | Decide |
|---|---|---|---|
| Error model per layer | Some functions throw, siblings return `{ ok, error }` or `null`; some Rust fns return `Result<_, String>`, others `anyhow::Result` | scan "error handling" and "error type"; `rg -n "return null" src` next to `throw` | One model per layer. Translate at boundaries (HTTP handler maps domain errors to status codes once). |
| Swallowed errors | `catch {}` or `catch (e) { console.log(e) }` in some places, rethrow in others; `let _ = fallible();`, `.ok();` | `rg -n "catch \(\w*\) \{\s*\}" ; rg -n "catch \{\s*\}"`; `rg -n "\.ok\(\);\|let _ = "` | Never swallow silently. One documented place may log and continue. |
| Logging | `console.log` in some modules, a logger in others; `println!` diagnostics next to `tracing` | scan "logging" | One logger with levels. Plain prints only in CLI user output and scripts. |
| Config access | `process.env.X` read in ten files; `std::env::var` deep in library code | scan "config access"; `rg -n "env::var\|process\.env\|import\.meta\.env"` | Read once into a typed, validated config object at startup; everything else receives it. |
| Validation location | Some handlers validate input with zod, others trust the body; some validate in the service, some in the controller | `rg -n "\.parse\(\|\.safeParse\(" src` per route folder | Validate at the trust boundary (request handler, message consumer, file loader), once, with one library. |
| Date, time, money, IDs | `Date` in some places, `dayjs` in others; money as float in one module, integer cents in another; UUID strings vs branded IDs | `rg -n "new Date\(\|dayjs\|date-fns\|moment"`; `rg -n "price\|amount\|cents"` | One representation per concept, defined once (R11). |
| Async style | `await` in most code, `.then()` chains in some; callbacks mixed in | scan "async style" | `async`/`await` unless a combinator (`Promise.all`) needs otherwise. |
| Test placement and naming | `foo.test.ts` next to source in one feature, `__tests__/foo.spec.ts` in another, `tests/` at root in a third | scan "test placement"; `git ls-files '*test*' '*spec*'` | One pattern. Colocated unit tests are the default (Dodds); e2e at root. |
| Test framework and helpers | Jest in one package, Vitest in another; three different render helpers | `rg -l "from 'vitest'\|from '@jest\|from 'jest'"`; look for duplicate `test-utils` | One framework per runtime; one helper module per concern. |
| Comment and doc style | JSDoc on some exports, none on siblings; `///` on half of a crate's pub items | `rg -c "^\s*/\*\*" src`; `#![warn(missing_docs)]` | Public API documented uniformly; internals comment the why. |
| File naming | `user-profile.tsx`, `UserProfile.tsx`, `userProfile.tsx` in one app | scan "file naming" | One case per file kind (components, hooks, modules). Enforce with `unicorn/filename-case` or Biome `useFilenamingConvention`. |
| Constructor and factory style | `new Foo()` here, `createFoo()` there, `Foo.create()` elsewhere | `rg -n "export function create\w+\|static create\("` | One per kind of object. |
| Feature flags | `if (FLAGS.x)`, `useFlag('x')`, `process.env.ENABLE_X` | `rg -n "ENABLE_\|useFlag\|FLAGS\."` | One flag mechanism, flags listed in one file. |
| User facing strings | Inline literals in some screens, i18n keys in others | `rg -n ">[A-Z][a-z]+ [a-z]+<" --glob '*.tsx'` next to `t('` usage | Once i18n exists, every user string goes through it. |

## 6. TypeScript and JavaScript dimensions

| Dimension | Variants | Detect | Default when nothing decides |
|---|---|---|---|
| Export style | `export default` vs named | scan "export style"; `rg -l "^export default" src` | Named exports. Default exports have no canonical name, so the same thing is imported under different names, renames do not propagate, and a wrong import name silently binds (Google TS guide). Framework files excepted. |
| Exported function form | `export function f()` vs `export const f = () =>` | scan "exported function form" | Whatever the codebase uses. If none: `function` declarations for top level functions and components (hoisted, named in stack traces, clearer generics), arrows for callbacks. Enforce with eslint `func-style`. |
| Component definition | `function Card()` vs `const Card: FC = () =>` vs `React.FC` | `rg -n "React\.FC\|: FC<" src` | Plain function with typed props. |
| Props typing | `interface Props` vs `type Props =` vs inline | scan "type declaration" | One. Enforce with `@typescript-eslint/consistent-type-definitions`. |
| Import paths | relative vs alias (`@/`, `~/`, `#`) | scan "import paths" and "deep relative imports" | Alias for anything outside the current feature, relative within it. Never `../../../`. Enforce with `no-restricted-imports` patterns. |
| Barrel files | `index.ts` re-exporting a folder, used in some features only | scan "barrel files"; Biome `noBarrelFile`, `noReExportAll` | No barrels in app code (cycles, slow dev server and tests: Atlassian cut build times by 75 percent removing them; TkDodo saw module count drop 68 percent). Barrels only as a published package entry point. |
| Type-only imports | `import type` in some files, mixed value imports of types in others | scan "type-only imports"; `@typescript-eslint/consistent-type-imports` | `import type` for types, enforced by the lint rule and `verbatimModuleSyntax`. |
| Enums | `enum Status` vs union `'a' \| 'b'` vs `as const` object | `rg -n "^export enum\|^enum " src` | Union of string literals or `as const` objects; one choice repo wide. |
| null vs undefined | functions returning `null` for absence next to ones returning `undefined` | `rg -c "return null" ; rg -c "return undefined"` per folder | Pick one for "absent" (usually `undefined` in TS) and keep `null` for values that cross JSON. |
| Data fetching | `fetch` here, `axios` there, a custom client elsewhere; React Query in one feature, `useEffect` fetching in another | `rg -l "from 'axios'"`, `rg -n "useEffect\(.*fetch"`, `rg -l "useQuery"` | One HTTP client wrapper, one server state library. |
| State management | Zustand store in one feature, Context plus reducer in another, Redux slices in a third | `rg -l "create\(\|createContext\|createSlice"` | One global store library; local state stays local (colocation). |
| Styling | Tailwind classes, CSS modules and styled-components in one app; StyleSheet.create and inline style objects in RN | `rg -l "styled\.\|\.module\.css\|className=\"\|StyleSheet\.create"` | One styling system, tokens from one theme file. |
| Class vs functions | Some modules export classes with static methods, others export functions | `rg -n "static \w+\(" src` | Functions. Classes only for real state plus behaviour; never static-only classes as namespaces (Google TS guide). |
| Async in components | some screens call services directly, others through hooks | read two screens per feature | One path from UI to data. |

## 7. Rust dimensions

| Dimension | Variants | Detect | Default when nothing decides |
|---|---|---|---|
| Module file layout | `foo/mod.rs` vs `foo.rs` plus `foo/` | scan "module file style"; `find . -name mod.rs -not -path './target/*'` | `foo.rs` plus `foo/` (the Rust book calls it the most idiomatic; `mod.rs` is the older style). Never both in one crate. Enforce with clippy `mod_module_files` (forbids `mod.rs`) or `self_named_module_files` (forbids the other). |
| Error types | `thiserror` enums, hand written `impl Error`, `Box<dyn Error>`, `String`, `anyhow` | scan "error type" | Library crates: one error enum per crate or per module boundary, derived with `thiserror`. Binaries: `anyhow` with `.context()`. Never `Result<T, String>` in a library. |
| Panics | `unwrap()` and `expect()` in non-test code | scan "panicking unwrap"; clippy `unwrap_used`, `expect_used` (restriction) | No `unwrap` in library code paths reachable from input; `expect("why this cannot fail")` for real invariants. |
| Visibility | everything `pub` vs `pub(crate)` for internals | scan "visibility"; rustc `unreachable_pub` | Private by default, `pub(crate)` for crate internals, `pub` only for the API. |
| Path imports | `use crate::a::b` vs `use super::b` vs glob | scan "path imports" and "glob imports" | `use crate::` paths; `use super::*` only in `mod tests`; no other globs (clippy `wildcard_imports`, `enum_glob_use`). |
| Import grouping | std, external, crate groups mixed | rustfmt `group_imports = "StdExternalCrate"` and `imports_granularity = "Module"` (nightly options) | Let rustfmt decide; check `rustfmt.toml`. |
| Logging | `println!`/`eprintln!` diagnostics vs `tracing`/`log` | scan "logging" | `tracing` (or `log`) in libraries and services; `println!` only for a CLI's intended output. |
| Constructors | `new`, `with_*`, `from_*`, builders, `Default` | `rg -n "pub fn (new\|create\|make)\w*\(" ` | `new` for the primary constructor, `with_x` for variants, `From` impls for conversions, builder when more than about 3 optional fields (Rust API Guidelines). |
| Conversion names | `to_`, `as_`, `into_` used inconsistently with cost | read each conversion | `as_` free borrow, `to_` expensive or owned copy, `into_` consumes self (C-CONV). |
| Getters | `get_name()` vs `name()` | `rg -n "pub fn get_\w+\(&self"` | `name()` and `name_mut()`; no `get_` prefix (C-GETTER). |
| Async runtime | tokio in one crate, async-std or smol in another | `rg -n "tokio\|async-std\|smol" Cargo.toml crates/*/Cargo.toml` | One runtime per binary. |
| Workspace deps | the same crate at two versions or declared per crate with different features | `cargo tree -d`; check `[workspace.dependencies]` | Declare shared deps once in `[workspace.dependencies]`, members use `dep.workspace = true`. |
| Lints | `#![allow(...)]` sprinkled per file vs one `[workspace.lints]` | `rg -n "#!\[allow\(" ` | One lint table in the workspace `Cargo.toml`. |

## 8. Dependency level consistency (two libraries for one job)

Two libraries that do the same job is the most expensive inconsistency: double bundle size, two mental models, two upgrade paths. Check manifests:

```
# JS/TS: list deps and look for pairs
jq -r '.dependencies, .devDependencies | keys[]' package.json apps/*/package.json packages/*/package.json 2>/dev/null | sort | uniq -c
```

Known pairs to flag: `axios` and `ky` or a hand rolled fetch client; `moment`, `dayjs`, `date-fns`, `luxon`; `lodash` and `ramda` or `lodash` and `lodash-es`; `zod`, `yup`, `joi`, `valibot`; `jest` and `vitest`; `redux`, `zustand`, `jotai`, `mobx`; `styled-components`, `emotion`, `tailwind`; `uuid` and `nanoid` (fine if purposes differ); in Rust `anyhow` and `eyre`, `log` and `tracing`, `reqwest` and `ureq`, `chrono` and `time`, `tokio` and `async-std`, `serde_json` and `simd-json` without a reason.

Also flag the same dependency at different versions across workspace packages (`pnpm why <pkg>`, `npm ls <pkg>`, `cargo tree -d`). In an Expo monorepo duplicate `react` or `react-native` versions break at runtime.

## 9. Fixing drift without making it worse

- **Never add a third variant.** If you think both existing variants are wrong, raise it; do not start a new one in your change.
- **Follow local convention inside a change, fix globally in a separate change.** A feature PR matches the area it touches. The cleanup that unifies the repo is its own structure-only PR (R17).
- **Unify mechanically.** Use a codemod (`jscodeshift`, `ts-morph`, `ast-grep`, `comby`, rust-analyzer's SSR, `cargo clippy --fix`) instead of hand edits; hand edits miss cases.
- **Install the guard in the same PR.** A unification without a lint rule regresses. Add the rule; if old code cannot all be fixed now, use a ratchet: the rule on, with an explicit allowlist of the remaining files that only shrinks (see `evolving-a-codebase.md`).
- **Write it down.** One line in CONTRIBUTING or ARCHITECTURE.md per decided convention, with the reason, so the next person (or agent) does not reopen it.
- **Do not churn for taste.** If the codebase consistently uses a variant you would not choose, it is not a finding. Consistency is the goal, not your preference.

## 10. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| Scan run before writing in an unfamiliar repo | You can name the majority variant for each dimension your change touches | `python3 -I ${CLAUDE_SKILL_DIR}/scripts/scan_conventions.py <repo>` |
| No new variant introduced | Rerunning the scan after your change adds no OFF or MIX line and no new variant in a dimension | diff the scan output before and after |
| Precedence recorded | Every convention decision names its source (tooling, docs, direction, area, repo, ecosystem) | read the PR or finding |
| Framework exceptions respected | No finding flags framework mandated default exports, file names, or lib vs bin error styles | cross check flagged files against section 3 |
| Default exports | Only framework files use them | `rg -l "^export default" src --glob '!**/{page,layout,route,loading,error,not-found}.tsx' --glob '!*.config.*'` |
| No app barrels | No `index.ts` that only re-exports, outside package entry points | scan "barrel files"; Biome `noBarrelFile` |
| One Rust module style | Only one of `mod.rs` or `foo.rs`+`foo/` per crate | `find . -name mod.rs -not -path '*/target/*'` plus clippy `mod_module_files` or `self_named_module_files` |
| One library per job | No pair from section 8 in manifests without a written reason | `jq` listing above; `cargo tree -d` |
| Guard installed with every unification | A lint rule or ratchet exists for each unified convention | lint config diff in the same PR |
