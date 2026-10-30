# CI pipeline

CI is the only reviewer that checks every change the same way every time. The minimum below runs on every push and pull request; anything not in CI will drift. Fast checks first, so a formatting error fails in 30 seconds, not after a 10 minute test run.

## Contents

1. Rules (C1 to C12)
2. Stage order and time budget
3. TypeScript / Node minimum
4. Rust minimum
5. Full stack with Postgres
6. React Native / Expo minimum
7. Scheduled and release only jobs
8. GitHub Actions hygiene
9. Checks

## 1. Rules

**C1. CI runs exactly what developers run.** Every CI step is a script in `package.json`, `justfile`, `Makefile` or `cargo xtask`, and CI calls those scripts. No logic that exists only in YAML. A developer can reproduce a CI failure with one command.

**C2. Warnings fail the build.** `eslint --max-warnings=0`, `cargo clippy -- -D warnings`, `tsc` with `strict`. A warning nobody must fix becomes 400 warnings nobody reads.

**C3. Check, never fix, in CI.** `prettier --check`, `cargo fmt --check`. CI never commits formatting changes back.

**C4. Install from the lockfile, fail if it is out of date.** `npm ci`, `pnpm install --frozen-lockfile`, `yarn install --immutable`, `cargo build --locked`.

**C5. The main branch is always green and protected.** Required status checks on the merge target; no direct pushes; merge only when checks pass on the merged result (merge queue or "require branches to be up to date").

**C6. Time budget: under 10 minutes to a pass or fail on a pull request**, under 5 for the fast lane. Slow suites get cached, parallelized or sharded, not skipped.

**C7. Cache dependencies and build outputs**, keyed by lockfile hash: `actions/setup-node` with `cache`, `Swatinem/rust-cache`, Turborepo / Nx remote cache for monorepos.

**C8. Only test what changed in big monorepos, but always run everything on main.** Affected detection (`turbo run test --filter=...[origin/main]`, `nx affected`) on PRs; full run on the main branch and nightly.

**C9. Real services, not mocks, for integration tests.** Postgres and Redis as service containers, the same major version as production.

**C10. Secrets never reach untrusted code.** Pull requests from forks get no secrets; never use `pull_request_target` to check out and run PR code. Workflows declare minimal `permissions`.

**C11. Dependencies and supply chain are checked.** Known vulnerabilities (`npm audit --omit=dev --audit-level=high`, `cargo deny check` / `cargo audit`), license policy, and automated update PRs (Dependabot or Renovate) that run the full CI.

**C12. Flaky CI is a bug with an owner** (see `testing-strategy.md` section 11). A rerun button pressed without an issue is a policy violation.

## 2. Stage order and time budget

```
1. Setup + install (cached)                      < 1 min
2. Fast lane, in parallel:                        < 2 min
   format check | lint | typecheck | lockfile/deps check
3. Unit + integration tests (with Postgres)       < 5 min (shard if longer)
4. Build the production artifact                  < 3 min
5. E2E on the built artifact (critical flows)     < 10 min, sharded; may run on main + PRs labelled
6. Deploy (main only): staging, smoke test, prod with canary/rollback (see deploy-and-rollback.md)
```

Run stages 2 to 4 in parallel jobs where possible; E2E depends on the build artifact.

## 3. TypeScript / Node minimum

`package.json` scripts (CI calls these):

```json
{
  "scripts": {
    "format:check": "prettier --check .",
    "lint": "eslint . --max-warnings=0",
    "typecheck": "tsc --noEmit",
    "test": "vitest run",
    "test:e2e": "playwright test",
    "build": "vite build",
    "check": "npm run format:check && npm run lint && npm run typecheck && npm run test"
  }
}
```

Use the project's existing tools: Biome instead of ESLint + Prettier (`biome ci .`), Jest instead of Vitest, `next build`, `tsc -b` for project references. Monorepos with project references: `tsc -b --noEmit` or per package `tsc --noEmit`.

ESLint rules that matter for reliability (type aware config, `typescript-eslint` `recommendedTypeChecked` or `strictTypeChecked`):
`@typescript-eslint/no-floating-promises`, `no-misused-promises`, `only-throw-error`, `switch-exhaustiveness-check`, `no-unnecessary-condition`, plus `no-console` for server code and `eslint-plugin-playwright`, `eslint-plugin-testing-library` for test files.

Optional but cheap: `knip` (unused files, exports and dependencies), `size-limit` for bundle budgets (see `performance.md`), `publint` / `@arethetypeswrong/cli` for published packages.

## 4. Rust minimum

```bash
cargo fmt --all -- --check
cargo clippy --workspace --all-targets --all-features --locked -- -D warnings
cargo nextest run --workspace --all-features --locked     # or: cargo test --workspace --locked
cargo test --doc --workspace --locked                      # nextest does not run doctests
cargo deny check                                           # advisories, licenses, bans, sources
```

- Also build with `--no-default-features` if the crate has features (`cargo hack --each-feature check` for libraries).
- MSRV job if the crate declares `rust-version`: `cargo +<msrv> check --locked`.
- `RUSTFLAGS="-D warnings"` invalidates caches for every build; prefer `-D warnings` on the clippy command and `[lints]` in `Cargo.toml`.
- Unsafe code or FFI: run `cargo +nightly miri test` on the affected crates.
- Workspace lint defaults in `Cargo.toml`:

```toml
[workspace.lints.clippy]
unwrap_used = "warn"      # error in CI via -D warnings; allow in tests with clippy.toml allow-unwrap-in-tests = true
expect_used = "warn"
dbg_macro = "warn"
print_stdout = "warn"     # services log through tracing
todo = "warn"
```

## 5. Full stack with Postgres

```yaml
name: ci
on:
  pull_request:
  push:
    branches: [main]
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: ${{ github.ref != 'refs/heads/main' }}
permissions:
  contents: read
jobs:
  check:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    services:
      postgres:
        image: postgres:17            # same major version as production
        env: { POSTGRES_PASSWORD: test, POSTGRES_DB: app_test }
        ports: ["5432:5432"]
        options: >-
          --health-cmd "pg_isready -U postgres" --health-interval 5s --health-timeout 5s --health-retries 10
    env:
      DATABASE_URL: postgres://postgres:test@localhost:5432/app_test
      TZ: UTC
      CI: true
    steps:
      - uses: actions/checkout@<sha>  # pin third party actions to a full commit SHA
      - uses: actions/setup-node@<sha>
        with: { node-version-file: .nvmrc, cache: npm }
      - run: npm ci
      - run: npm run format:check
      - run: npm run lint
      - run: npm run typecheck
      - run: npm run db:migrate        # the real migrations, not a test schema
      - run: npm test
      - run: npm run build
```

Also check that migrations are reversible or at least apply cleanly to an empty DB and to a copy of the previous schema, and run `squawk` on new migration files (see `deploy-and-rollback.md`).

Schema drift check: generate the ORM client or SQL types in CI and fail if the result differs from what is committed (`git diff --exit-code`). Same for any generated code (OpenAPI clients, `sqlx prepare --check`).

## 6. React Native / Expo minimum

```bash
npx expo install --check            # native module versions match the SDK
npx expo-doctor                     # project health
npx tsc --noEmit
npx eslint . --max-warnings=0
npx jest --ci                       # jest-expo preset + @testing-library/react-native
npx expo export --platform all      # proves the JS bundle builds; catches Metro resolution errors
```

- Native builds (`eas build`) and Maestro E2E on an emulator are slow: run them on main, on release branches, or on PRs with a label, not on every push.
- Check that `app.json` / `app.config.ts` changes that affect native code bump the `runtimeVersion` (OTA safety, see `deploy-and-rollback.md`).

## 7. Scheduled and release only jobs

| Job | When | Why |
|---|---|---|
| Full E2E across browsers | Nightly + before release | Too slow for every PR |
| Dependency audit | Daily | New advisories appear without code changes |
| Flaky detection (repeat suite, shuffled order) | Weekly | Find flakes before they block PRs |
| Mutation testing on critical modules | Weekly | Test quality signal |
| Load / overload test | Before major releases, after capacity changes | Know the breaking point (`resilience-patterns.md`) |
| Backup restore test | At least monthly, automated | A backup never restored is not a backup (GitLab 2017) |
| Certificate and domain expiry check | Daily | Expired certs are a recurring postmortem cause |
| Benchmarks | On main, compared to baseline | Catch performance regressions (`performance.md`) |

## 8. GitHub Actions hygiene

- `permissions: contents: read` at the top; grant more per job only when needed.
- `timeout-minutes` on every job (the default is 360 minutes; a hung job burns runner time and blocks merges).
- `concurrency` with `cancel-in-progress` for PR branches, so superseded runs stop.
- Pin third party actions to a commit SHA, not a moving tag (`tj-actions/changed-files` was compromised in March 2025 through retagged versions). Let Dependabot update the SHAs.
- Never interpolate untrusted input (`${{ github.event.pull_request.title }}`, branch names) directly into `run:` scripts; pass through `env:` and quote.
- Upload test reports and Playwright traces as artifacts on failure only.
- Use the `ubuntu-latest` image, but pin language versions from repo files (`.nvmrc`, `rust-toolchain.toml`) so local and CI match.

## 9. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| CI exists and runs on PRs and main | Workflow with `pull_request` and `push: main` | `rg -n 'pull_request|push:' .github/workflows` |
| Steps call scripts | `run:` lines call `npm run`, `just`, `make`, `cargo` | Read workflow; no multi-line inline logic |
| Lockfile install | `npm ci` / frozen lockfile / `--locked` | `rg -n 'npm install(?! -g)|pnpm install(?!.*frozen)|cargo (build|test|clippy)(?!.*--locked)' -P .github/workflows` returns 0 |
| Warnings fail | `--max-warnings=0`, `-D warnings` | `rg -n 'max-warnings|-D warnings' .github/workflows package.json justfile Makefile` |
| Format checked | `prettier --check` / `biome ci` / `cargo fmt --check` | rg the same files |
| Typecheck in CI | `tsc --noEmit` or `tsc -b` | rg |
| Real DB in CI | Postgres service or Testcontainers | `rg -n 'postgres' .github/workflows` |
| Timeouts on jobs | Every job has `timeout-minutes` | `rg -c 'timeout-minutes' .github/workflows/*.yml` vs job count |
| Least privilege | Top level `permissions` set | `rg -n '^permissions:' .github/workflows` |
| Actions pinned | Third party `uses:` pinned to 40 char SHA | `rg -n 'uses: [^.][^@]+@(?![0-9a-f]{40})' -P .github/workflows` returns only first party or none |
| No pull_request_target with checkout of PR head | 0 hits | `rg -n -A10 'pull_request_target' .github/workflows | rg 'ref: .*head'` |
| Dependency audit scheduled | A job runs audit on a schedule | `rg -n 'schedule:|cargo deny|npm audit|cargo audit' .github/workflows` |
| Generated code not drifted | CI regenerates and diffs | `rg -n 'git diff --exit-code|sqlx prepare --check' .github/workflows` |
| Branch protection | Required checks on main | `gh api repos/{owner}/{repo}/branches/main/protection` (or gh-axi equivalent) |
| Pipeline time | PR pipeline median under 10 min | `gh run list --workflow ci --json startedAt,updatedAt -L 50` and compute the median difference, or read the Actions UI |
