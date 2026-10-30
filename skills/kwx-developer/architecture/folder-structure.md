# Folder structure and file layout

Where files go, when to make a folder, when to split a file, and default layouts for the stacks this skill covers. Applies to new projects and to adding code to existing ones. In an existing repo the house layout wins over these defaults (see `consistency.md`); these defaults are for new code where nothing decides, and for audits.

## Contents

1. Feature folders vs layer folders
2. Colocation
3. The `utils` and `shared` problem
4. Barrels and index files
5. When to split a file, when to merge
6. Default layouts (web app, Expo app, full-stack monorepo, Rust crate, Rust workspace)
7. Monorepo or polyrepo
8. Checks

## 1. Feature folders vs layer folders

Layer folders: `components/`, `hooks/`, `services/`, `models/`, `controllers/`, `utils/` at the top. Feature folders: `features/billing/`, `features/auth/`, each containing its own components, hooks, API calls and tests.

Default: **feature folders at the top once the app has more than about three features or more than one developer; layers inside each feature.** Fowler: layering at the top is acceptable for small systems, but once any layer grows, "split your top level into domain oriented modules which are internally layered".

Why features win as projects grow:

- A change to one feature touches one folder. With layer folders the same change touches `components/`, `hooks/`, `services/`, `types/` and `tests/`, which is change amplification built into the tree.
- Deleting a feature is deleting a folder. With layers, dead code survives in four places.
- Ownership and boundaries are visible and lintable (`import/no-restricted-paths` per feature).
- The tree tells a newcomer what the app does ("screaming architecture"), not which framework it uses.

When layers at the top are fine: small apps, libraries with one concern, CLIs, and backend services that are a thin API over a database with few domains.

Never mix the two at the same level. `src/components/`, `src/hooks/`, `src/billing/`, `src/auth/` side by side means nobody knows where a billing hook goes. If an existing repo is mixed, that is an audit finding; new code follows whichever principle the area you touch uses.

Signals the structure is wrong:

- Adding a small feature edits five or more top level folders (check `git log --stat` of recent feature commits).
- A folder named after a technical role holds 50+ files from unrelated features.
- Files named with a feature prefix inside a layer folder (`components/BillingCard.tsx`, `components/BillingTable.tsx`, `components/BillingModal.tsx`): the prefix is a folder that has not been created yet.

## 2. Colocation

Kent C. Dodds: "Place code as close to where it's relevant as possible." Dan Abramov's version: things that change together should be located as close as reasonable.

- Unit tests next to the module: `price.ts` and `price.test.ts`. A reader sees at once that it is tested; moving the module moves its test.
- Styles, stories, fixtures and types used by one component live beside it.
- A helper used by one file lives in that file, unexported. It moves to a shared place only when a second consumer appears (R9).
- State lives in the lowest component that needs it.
- Exceptions: end to end tests at the root (`e2e/`), because they span the system and must survive refactors of `src/`; integration tests in the folder of the flow they cover; system wide docs in a README in the folder they describe.
- Rust: unit tests inline in `#[cfg(test)] mod tests` at the bottom of the file; integration tests in `tests/`; benchmarks in `benches/`.

## 3. The `utils` and `shared` problem

`utils/`, `helpers/`, `common/`, `misc/`, `lib/` grow into junk drawers: unrelated functions with no owner, kept alive after their last caller is deleted (Dodds), and imported by everything so they become a cycle hub.

Rules:

- No file named `utils.ts`, `helpers.ts`, `common.rs` or `misc.*`. Name files by what they hold: `currency.ts`, `dates.ts`, `retry.ts`, `slug.rs`.
- A shared folder holds code with two or more real consumers in different features. Check importers before adding (`rg -l "from '.*shared/currency'"`).
- Shared code depends on nothing feature specific. If it needs feature knowledge, it is not shared.
- Prefer the standard library or an existing dependency over a new helper; grep for an existing helper before writing one (agents often add a second `formatDate`).

## 4. Barrels and index files

A barrel is an `index.ts` that re-exports a folder (`export * from './Button'`).

- **Do not create barrels in application code.** They cause import cycles (a file in the folder imports the barrel, which re-exports the file), load every module in the folder for one import (slower dev server and tests), and defeat tree shaking with side effects. Atlassian reported a 75 percent cut in build times after removing them from Jira's frontend; TkDodo measured module count dropping from about 11k to 3.5k (68 percent) in a Next.js app.
- **The one good use:** the entry point of a published package or a workspace package (`packages/core/src/index.ts` referenced by `"exports"`), where it defines the public API.
- If the repo already uses barrels as a feature's public API with a lint rule forbidding deep imports, keep that convention consistent rather than mixing.
- Enforce: Biome `noBarrelFile` and `noReExportAll`; `eslint-plugin-barrel-files`.
- Rust has no barrel problem in the same sense, but `pub use` re-exports at the crate root define the public API; keep them deliberate and grouped in `lib.rs`.

## 5. When to split a file, when to merge

Split by cohesion, not by line count. A file should hold one concept and the private helpers only it uses.

Split when:

- The file holds two or more concepts that change for different reasons (Fowler's divergent change): a component plus an unrelated API client plus date helpers.
- Two parts have no references to each other (find with your editor's call hierarchy or by reading); they are two modules sharing a file.
- Several people or agents edit the file at once for unrelated reasons (merge conflicts in `git log` on that file).
- A part has a clean interface that can be described without its body and is used from elsewhere.

Do not split when:

- The pieces are only understandable together (conjoined). Ousterhout: split only if it reduces what a reader must know.
- The "split" creates files that are each imported by exactly one other file in a chain (`A.tsx` -> `A.hooks.ts` -> `A.utils.ts` -> `A.types.ts`) for a 200 line component. One file is easier.

Size heuristics (heuristics, not limits; investigate, do not auto split):

| Signal | Threshold to investigate | Tool |
|---|---|---|
| File length | over about 400 lines in TS/TSX, over about 800 to 1000 in Rust (Rust files carry inline tests and impl blocks) | `git ls-files '*.ts*' \| xargs wc -l \| sort -rn \| head`; eslint `max-lines` (default 300) |
| Function length | over about 60 to 100 lines, or more than 3 levels of nesting | eslint `max-lines-per-function`, `max-depth` (default 4); clippy `too_many_lines` (pedantic, default 100) |
| Parameters | more than 4 positional parameters, or any boolean that selects behaviour | eslint `max-params` (default 3); clippy `too_many_arguments` (default 7), `fn_params_excessive_bools` (default 3) |
| Complexity | cyclomatic over about 15 to 20 | eslint `complexity` (default 20); clippy `cognitive_complexity` (default 25) |
| Exports per file | more than about 10 unrelated exports | `rg -c "^export " src \| sort -t: -k2 -rn \| head` |

Merge when files are tiny, always edited together, and import each other (conjoined): one file of 150 lines beats four of 40.

## 6. Default layouts

Use these for new projects or new areas when the repo has no convention. Include only folders you need.

### Web app (React, Next.js or Vite)

```
src/
  app/                 # routes or router, providers, app shell; composes features
  features/
    billing/
      components/      # only if more than a few files; otherwise flat
      api.ts           # this feature's server calls
      billing.ts       # domain logic, pure functions
      billing.test.ts
      types.ts
    auth/
  components/          # shared UI kit only (Button, Dialog), no feature knowledge
  lib/                 # configured clients: http.ts, queryClient.ts, analytics.ts
  config.ts            # typed, validated env, read once
```

Direction: `app -> features -> (components, lib)`; features do not import each other. Next.js `app/` route files stay thin and call into `features/`.

### Expo or React Native app

```
app/                   # Expo Router routes only; thin, call into src/features
src/
  features/<name>/     # screens' content, hooks, logic, tests
  components/          # shared UI kit
  lib/                 # storage, notifications, api client
  theme/               # tokens
```

Keep route files thin because Expo Router treats every file under `app/` as a route; helpers placed there become routes.

### Full-stack monorepo (web plus mobile plus shared core)

```
apps/
  web/                 # Next.js or Vite
  mobile/              # Expo
  api/                 # server, if separate
packages/
  core/                # domain types, zod schemas, pure logic; no platform imports
  api-client/          # typed client generated or written once for both apps
  ui-tokens/           # colours, spacing, type scale shared by both UIs
  config/              # shared tsconfig, eslint config
pnpm-workspace.yaml    # apps/*, packages/*
```

Packages are consumed with `"workspace:*"`. One version of React and React Native across the workspace.

### Rust single crate

```
src/
  main.rs or lib.rs    # thin: wiring, pub use of the API
  config.rs
  domain.rs            # or domain/ with submodules, foo.rs + foo/ style
  storage.rs
  http.rs
tests/                 # integration tests against the public API
benches/
```

### Rust workspace (from about 10k lines, or when a core must be IO free)

Follow matklad's large workspace layout:

```
Cargo.toml             # virtual manifest: [workspace], [workspace.dependencies], [workspace.lints]
crates/
  app-core/            # crate name == folder name
  app-storage/
  app-server/
  app-cli/
xtask/                 # automation in Rust instead of shell scripts
```

- Flat `crates/` (no nested hierarchy): Cargo's crate namespace is flat, a flat list fits on one screen, and "tree structure tends to deteriorate over time, while flat structure doesn't need maintenance".
- Root is a virtual manifest, not a crate.
- Each crate is named exactly as its folder.
- Internal crates use `version = "0.0.0"`; crates meant for publishing go in a separate `libs/` folder so you can check `libs/` never depends on `crates/`.

## 7. Monorepo or polyrepo

Default for one product or one small team: **one repository** containing all apps and shared packages. A monorepo is "a single repository containing multiple distinct projects, with well-defined relationships" (monorepo.tools); without enforced relationships it is just a big repo.

What a monorepo buys: atomic changes across a shared package and its consumers, one version of each dependency, one place to enforce conventions, no publishing step for internal code.

What it needs: workspace tooling (pnpm or npm workspaces, Cargo workspace), affected-only builds and tests once CI gets slow (Turborepo, Nx), and enforced package boundaries (each package's own `exports`, lint rules on imports).

Choose separate repos when: projects have different owners with different release cycles and no shared code, access must be restricted per project, or one part is open source and the rest is not. Splitting for "cleanliness" alone adds versioning and cross-repo change cost.

## 8. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| One organising principle per level | Top level is all features or all layers, not both | `ls src`; read names |
| Feature change locality | Recent feature commits touch one feature folder plus the app shell | `git log --stat -10 --format=%s` |
| No junk drawer files | No `utils.*`, `helpers.*`, `common.*`, `misc.*` files | `git ls-files \| rg -i '/(utils\|helpers\|common\|misc)\.(ts\|tsx\|js\|rs)$'` |
| Shared has 2+ consumers | Each shared module is imported from two or more features | `rg -l "<module>" src/features \| cut -d/ -f3 \| sort -u \| wc -l` |
| No app barrels | No pure re-export `index.ts` outside package entry points | `scan_conventions.py` "barrel files"; Biome `noBarrelFile` |
| Tests colocated | Unit tests next to source (or the repo's single declared pattern) | `scan_conventions.py` "test placement" |
| Large files reviewed | Every file over the size heuristic holds one concept | `git ls-files '*.ts' '*.tsx' '*.rs' \| xargs wc -l \| sort -rn \| head -15`, then read |
| Rust workspace shape | Virtual manifest, flat `crates/`, crate name equals folder | `cat Cargo.toml`; `ls crates`; compare `name =` in each `Cargo.toml` |
| Thin route files | Next.js or Expo Router route files delegate to features | `wc -l app/**/page.tsx app/**/*.tsx`; read the largest |
