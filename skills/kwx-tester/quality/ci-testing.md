# Running tests in CI

How to run tests in CI so a red build means a real problem and a green build can be trusted: order (fast first), caching, parallel runs and sharding, a retry policy that detects flakiness instead of hiding it, quarantine with an owner and a date, running only affected tests, artifacts to keep, timeouts, the matrix that matters, and working GitHub Actions jobs for web, Rust and Android (emulator and EAS). kwx-developer `reliability/ci-pipeline.md` sets the general pipeline (stage order, lockfile installs, action pinning, permissions); this file is only about the test jobs, and goes deeper.

## Contents

1. Rules
2. Order: fast and cheap first
3. Caching for test jobs
4. Retries: detect, never hide
5. Quarantine: owner and date
6. Parallel runs and sharding
7. Affected tests only
8. Artifacts to keep
9. Timeouts
10. The matrix that matters
11. GitHub Actions examples
12. Android emulator and EAS in CI
13. Checks

## 1. Rules

1. **The blocking test job is deterministic.** Only tests that pass reliably block a merge. Flaky ones go to quarantine (section 5). Google: 84% of pass to fail transitions in its CI involved a flaky test, and people learn to ignore red (Micco 2016). Evidence: strong.
2. **Retries are a detector, not a fix.** Retry at most 2 times, only in e2e and device suites, and always report which tests passed only on retry. A test that passes on retry is flaky, and gets an issue. Evidence: strong (Google, Slack, nextest and Playwright all classify a retried pass as flaky).
3. **Fail fast on cheap checks, but run every test once started.** Lint and typecheck first; inside the test job, `fail-fast: false` on shard matrices and `--no-fail-fast` / `--continue` so one failure does not hide the others.
4. **Every job has a timeout.** GitHub's default is 360 minutes; a hung emulator burns six hours. Evidence: moderate (GitHub docs).
5. **Keep the evidence of a failure.** Traces, screenshots, JUnit XML and logs are uploaded when a job fails (`if: ${{ !cancelled() }}`), with a short retention. Evidence: moderate (Playwright docs).
6. **PRs run what the change can break; main runs everything.** Affected only selection on pull requests, full suite on main and nightly (kwx-developer C8). Evidence: moderate.
7. **CI runs the same command as a developer.** `npm run test:e2e`, `just test`, `cargo nextest run --profile ci`: config lives in the repo, not in YAML (kwx-developer C1).
8. **Test only on the platforms that differ.** Add an OS or version to the matrix only when the code behaves differently there (section 10).
9. **Check the user's rules for who may run what.** CI may run browsers and emulators even when the user forbids the agent to launch them locally. The agent writes and edits the workflow; it does not start a local browser or emulator to "check" it.

## 2. Order: fast and cheap first

```
Job 1 (parallel, < 2 min):  format | lint (with test lint rules) | typecheck | forbid .only
Job 2 (< 5 min):            unit + component tests, then integration with real Postgres
Job 3 (after build):        e2e on the built artifact (sharded)        | Android: instrumented / Maestro
Job 4 (main / nightly):     full browser matrix, mutation sample, flaky hunt (shuffled, repeated)
```

Inside a test job, order by speed so the common failure shows first: unit before integration before e2e. Vitest and Jest already run previously failed and slow files first when a cache is kept. Run the smoke subset of e2e (tagged `@smoke`) before the rest: `npx playwright test --grep @smoke` then the full run.

Block focused tests before any test runs, because `.only` makes the suite green by running almost nothing: Playwright `forbidOnly: !!process.env.CI`; Vitest refuses `.only` on CI by default (`--allowOnly` defaults to `!process.env.CI`, verified in `vitest --help`, 5.0.5); Rust and Kotlin have no `.only`; pytest has no focus marker.

## 3. Caching for test jobs

Dependency caches are in kwx-developer C7. For tests, also cache:

| What | Key | How |
|---|---|---|
| Playwright browsers | Playwright version | `actions/cache` on `~/.cache/ms-playwright` keyed by `hashFiles('package-lock.json')`; on a hit run `npx playwright install-deps` only (system libraries are not cached). Or use the `mcr.microsoft.com/playwright:v<version>-noble` container (Playwright docs) |
| Rust build | lockfile and toolchain | `Swatinem/rust-cache@v2`; `taiki-e/install-action@nextest` installs a prebuilt nextest |
| Gradle | wrapper and build files | `gradle/actions/setup-gradle@v5` (handles caching) |
| Android AVD snapshot | API level | `actions/cache@v5` on `~/.android/avd/*` and `~/.android/adb*` (section 12) |
| Vitest / Jest results cache | branch | lets the runner order failed and slow files first; optional |

Never cache test outputs (snapshots, coverage, results) between runs: a stale cached result is a green build that ran nothing.

## 4. Retries: detect, never hide

**Policy:**

| Suite | Retries on CI | Locally |
|---|---|---|
| Unit, integration | 0. A retry there hides a race in code or shared state | 0 |
| Web e2e (Playwright) | up to 2 | 0 |
| Mobile e2e and instrumented | up to 2 | 0 |

Every retried pass is reported and gets an issue (or goes to quarantine). Google's "fail only if it fails 3 times" flag "encourages developers to ignore flakiness in their own tests" and delays real breakages (a 15 minute test takes 45 minutes to be declared broken) (Micco 2016). Slack first hid flaky results from the build and rolled it back: failing tests leaked into main and fixes looked successful when they were not (Slack Engineering 2022).

**How each runner reports retried passes:**

| Runner | Retry setting | How a retried pass shows | Make it fail the build (optional) |
|---|---|---|---|
| Playwright | `retries: process.env.CI ? 2 : 0` | result category `flaky` ("failed on the first run, but passed when retried"), counted in the summary and HTML report (Playwright docs) | `--fail-on-flaky-tests` (CLI, 1.45+) or `failOnFlakyTests` in config (1.52+, per release notes) |
| cargo-nextest | `[profile.ci] retries = 2` or `--retries 2` | status `FLAKY 2/3`, summary "1 passed (1 flaky)"; JUnit `<flakyFailure>` per failed attempt (nextest docs) | `--flaky-result fail` |
| Vitest 5 | `--retry=2` | verbose reporter prints `(retry x1)`; JSON reporter keeps `status: "passed"` with a non empty `failureMessages` (verified). Default and JUnit output show a plain pass | a CI step that fails on the JSON query below |
| Gradle (JVM, Android) | `org.gradle.test-retry` plugin (`retry { maxRetries = 2; failOnPassedAfterRetry = false }`) | the plugin reports the passed after retry tests (plugin docs) | `failOnPassedAfterRetry = true` |
| pytest | `pytest-rerunfailures`: `--reruns 2` | `R` in the progress line and "rerun" in the summary (plugin docs) | parse the JUnit or summary |

List retried passes in Vitest (verified on a test that fails once, then passes):

```bash
npx vitest run --retry=2 --reporter=default --reporter=json --outputFile.json="$RUNNER_TEMP/vitest.json"
jq -r '.testResults[].assertionResults[] | select(.status=="passed" and (.failureMessages|length)>0) | "FLAKY: \(.fullName)"' "$RUNNER_TEMP/vitest.json"
```

Put the list in the job summary so nobody has to open logs: `... | tee -a "$GITHUB_STEP_SUMMARY"`.

**Detecting flakiness on purpose** (weekly job, never on the PR path): repeat and shuffle.

```bash
npx vitest run --repeats=20 --sequence.shuffle.tests        # verified flags, Vitest 5
npx playwright test --repeat-each=20 --retries=0
cargo nextest run --retries 0 ; for i in $(seq 20); do cargo nextest run || break; done
pytest -p randomly --count=20                                 # pytest-randomly + pytest-repeat
```

Spotify cut its flakiness from 6% to 4% in two months by only publishing a table of flaky tests per team, before building any tool (Spotify Engineering 2019). Visibility first. Evidence: moderate.

## 5. Quarantine: owner and date

A quarantined test is removed from the blocking job but not forgotten. Fowler: put non deterministic tests in quarantine "but fix quarantined tests quickly", cap the quarantine (his example: 8 tests) and set a maximum stay (a week). kwx-developer `testing-strategy.md` section 11 sets the default: quarantine within a working day, fix or delete within 2 weeks.

**Marker format** (one line, machine checkable). Use the runner's own skip mechanism plus a fixed comment or reason:

```ts
test.fixme('applies coupon at checkout', async ({ page }) => { /* ... */ }) // quarantine: #123 owner=adil until=2026-11-14
```
```rust
#[ignore = "quarantine: #123 owner=adil until=2026-11-14"]
```
```kotlin
@Ignore("quarantine: #123 owner=adil until=2026-11-14")
```
```python
@pytest.mark.skip(reason="quarantine: #123 owner=adil until=2026-11-14")
```

**Enforcement step** (verified on fixtures): fails the build when a quarantine expired, so expiry cannot be ignored.

```bash
today=$(date +%F)
rg -n --no-heading 'quarantine: (#\d+|\S+) owner=\S+ until=(\d{4}-\d{2}-\d{2})' -or '$2' . \
 | awk -F: -v t="$today" '$3 < t {print "EXPIRED " $1 ":" $2 " (until " $3 ")"; bad=1} END {exit bad}'
# cap: fail when more than 8 quarantined
test "$(rg -c 'quarantine: ' . | awk -F: '{s+=$2} END {print s+0}')" -le 8
```

Slack's lesson after suppressing 1,000s of tests automatically: re-enabling was the hard part, because failures went stale. Run the quarantined tests in a separate, non blocking nightly job (`npx playwright test --grep @quarantine`, `cargo nextest run --run-ignored only`, `pytest -m quarantine`), so the owner sees when a fix worked. Spotify's Flakybot did this on demand for a PR.

## 6. Parallel runs and sharding

Parallel inside one machine first, then shards across machines.

| Runner | Inside one machine | Across machines |
|---|---|---|
| Vitest | `pool: 'forks'` (default) or `'threads'`; `--no-isolate` only when tests clean up state (Vitest docs) | `vitest run --reporter=blob --shard=1/3`, collect `.vitest/blob/`, then `vitest run --merge-reports`; shards split files, not tests |
| Playwright | `workers`; Playwright recommends `workers: 1` on CI for stability, so get speed from shards | `--shard=1/4` with `fullyParallel: true` (splits by test, balanced), `reporter: process.env.CI ? 'blob' : 'html'`, then `npx playwright merge-reports --reporter html ./all-blob-reports` |
| cargo-nextest | parallel by default, one process per test | `--partition slice:1/3` (`count:` is deprecated); build once with `cargo nextest archive` and reuse in each shard (nextest docs) |
| Gradle | `maxParallelForks = (Runtime.getRuntime().availableProcessors() / 2).coerceAtLeast(1)` in `tasks.withType<Test>` | split by module across jobs |
| pytest | `pytest -n auto` (pytest-xdist) | `pytest-split` with stored durations |

Shard only when one job would take over about 10 minutes (kwx-developer C6). Each shard costs setup time (install, browsers, build).

## 7. Affected tests only

On pull requests, run what the change can break; on main, run everything.

| Tool | Command (source) |
|---|---|
| Vitest | `vitest run --changed origin/main` (tests affected by changed files, via the import graph; verified); `vitest related src/a.ts src/b.ts` (static imports only, not dynamic, Vitest docs) |
| Jest | `jest --changedSince=origin/main` (Jest docs) |
| Nx | `nx affected -t test --base=origin/main` (Nx docs) |
| Turborepo | `turbo run test --filter='...[origin/main]'` (Turborepo docs) |
| cargo-nextest | filtersets: `cargo nextest run -E 'rdeps(my-crate)'` runs tests of `my-crate` and every crate that depends on it (nextest filterset docs) |
| Gradle | only the changed modules' `test` tasks; Gradle's build cache skips unchanged ones |
| pytest | `pytest-testmon` selects tests by coverage of changed code (plugin docs) |

Traps: selection misses changes the graph cannot see (config files, env vars, SQL migrations, fixtures, snapshot files, `package.json`). When any of those change, run everything:

```yaml
- id: scope
  run: |
    if git diff --name-only origin/main... | grep -qE '(package(-lock)?\.json|vitest\.config|\.env|migrations/|fixtures/|\.github/)'; then
      echo "args=" >> "$GITHUB_OUTPUT"; else echo "args=--changed origin/main" >> "$GITHUB_OUTPUT"; fi
- run: npx vitest run ${{ steps.scope.outputs.args }}
```

`actions/checkout` fetches one commit by default: set `fetch-depth: 0` (or fetch the base branch) or `--changed origin/main` has nothing to compare with.

## 8. Artifacts to keep

| Artifact | When | Retention | How |
|---|---|---|---|
| Playwright trace | first retry: `trace: 'on-first-retry'` | 14 to 30 days | inside `playwright-report/` or blob reports |
| Screenshots, video | on failure: `screenshot: 'only-on-failure'`, `video: 'retain-on-failure'` | same | same |
| JUnit XML | always | 7 days | Vitest `--reporter=junit --outputFile.junit=...` (verified), Jest `jest-junit`, nextest `[profile.ci.junit] path = "junit.xml"` (written to `target/nextest/ci/junit.xml`), Gradle `build/test-results/`, pytest `--junitxml=...` |
| Coverage (lcov, Cobertura) | when coverage runs | 7 days | for `diffgaps.py` or diff-cover (`coverage.md`) |
| Android logcat, screenshots | on failure | 7 days | `adb logcat -d > logcat.txt` in the emulator script; Maestro writes to `~/.maestro/tests/` |
| Flaky list | always | 30 days | the section 4 query, also in `$GITHUB_STEP_SUMMARY` |

Upload with `if: ${{ !cancelled() }}` so failed runs keep their evidence. Name artifacts with `${{ github.run_attempt }}` so a re-run does not overwrite the first attempt's trace (Playwright's own workflow does this).

## 9. Timeouts

| Level | Setting |
|---|---|
| Job | `timeout-minutes:` on every job: unit 10, e2e shard 20, emulator 30 |
| Whole Playwright run | `globalTimeout: 60 * 60 * 1000` on CI (Playwright docs: "Always set a global timeout in CI") |
| One test | Playwright `timeout` (default 30 s), Vitest `testTimeout` (default 5 s), nextest `slow-timeout = { period = "60s", terminate-after = 3 }`, pytest-timeout `--timeout=60`, Gradle `timeout.set(Duration.ofMinutes(10))` on the Test task |
| One wait | no fixed sleeps; web first assertions and polling with their own timeout |

A test that hits a timeout is a failure with a name, not a hung job. Raising a timeout to make a test pass is the same as adding a sleep: find out what is slow first.

## 10. The matrix that matters

Each matrix cell multiplies cost and flakiness exposure. Add a cell only when the code or platform behaves differently there.

| Project | Matrix |
|---|---|
| Next.js / static site | one Node version (the one production runs, from `.nvmrc`), Linux only. Browsers: Chromium on PRs; Chromium, Firefox, WebKit nightly. Mobile viewport as a Playwright project, not a separate OS |
| Rust CLI or TUI | Linux on PRs; add macOS and Windows only if you ship binaries there (path handling, line endings, terminals). MSRV job if you publish a crate |
| Expo / React Native, Android first | unit and component tests on Linux; one emulator API level on PRs (the target SDK), plus the minimum supported API level nightly |
| Kotlin / Compose Android | JVM unit and Robolectric on every PR; instrumented on one API level per PR, min and target nightly |
| Quickshell / QML on Arch | Linux only; QML logic tests headless with `QT_QPA_PLATFORM=offscreen` |
| Supabase backend | the Postgres major version production runs |

## 11. GitHub Actions examples

Web app: unit with coverage, flaky report, and sharded Playwright. Action major versions are those in the Playwright docs fetched 2026-10; pin third party actions to a commit SHA in real use (kwx-developer `ci-pipeline.md` section 8).

```yaml
name: test
on:
  pull_request:
  push:
    branches: [main]
concurrency:
  group: test-${{ github.ref }}
  cancel-in-progress: ${{ github.event_name == 'pull_request' }}
permissions:
  contents: read

jobs:
  unit:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    env: { TZ: UTC }
    steps:
      - uses: actions/checkout@v6
        with: { fetch-depth: 0 }
      - uses: actions/setup-node@v6
        with: { node-version-file: .nvmrc, cache: npm }
      - run: npm ci
      - name: Unit tests (affected on PRs, all on main)
        run: |
          ARGS=""; [ "${{ github.event_name }}" = pull_request ] && ARGS="--changed origin/${{ github.base_ref }}"
          npx vitest run $ARGS --retry=0 --coverage --coverage.reporter=lcov \
            --reporter=default --reporter=junit --outputFile.junit=junit.xml
      - name: Changed code gaps (report only)
        if: github.event_name == 'pull_request'
        run: python3 -I scripts/diffgaps.py coverage/lcov.info origin/${{ github.base_ref }} | tee -a "$GITHUB_STEP_SUMMARY" || true
      - if: ${{ !cancelled() }}
        uses: actions/upload-artifact@v4
        with: { name: unit-${{ github.run_attempt }}, path: "junit.xml\ncoverage/lcov.info", retention-days: 7 }

  e2e:
    needs: unit
    runs-on: ubuntu-latest
    timeout-minutes: 20
    strategy:
      fail-fast: false
      matrix: { shard: [1, 2, 3] }
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-node@v6
        with: { node-version-file: .nvmrc, cache: npm }
      - run: npm ci
      - run: npx playwright install --with-deps chromium
      - run: npm run build
      - run: npx playwright test --shard=${{ matrix.shard }}/3   # config: retries 2 on CI, trace on-first-retry, forbidOnly, blob reporter
      - if: ${{ !cancelled() }}
        uses: actions/upload-artifact@v4
        with: { name: blob-report-${{ matrix.shard }}, path: blob-report, retention-days: 1 }

  e2e-report:
    if: ${{ !cancelled() }}
    needs: e2e
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-node@v6
        with: { node-version-file: .nvmrc, cache: npm }
      - run: npm ci
      - uses: actions/download-artifact@v5
        with: { path: all-blob-reports, pattern: blob-report-*, merge-multiple: true }
      - run: npx playwright merge-reports --reporter html,list ./all-blob-reports | tee merged.txt
      - run: grep -i flaky merged.txt >> "$GITHUB_STEP_SUMMARY" || true
      - uses: actions/upload-artifact@v4
        with: { name: playwright-report-${{ github.run_attempt }}, path: playwright-report, retention-days: 14 }
```

The `diffgaps.py` step needs the script committed in the repo (`scripts/`): propose it to the owner first, as with any new file.

Rust: nextest with a CI profile.

```toml
# .config/nextest.toml
[profile.ci]
retries = 0            # unit and integration: no retries
fail-fast = false
slow-timeout = { period = "60s", terminate-after = 3 }
[profile.ci.junit]
path = "junit.xml"     # written to target/nextest/ci/junit.xml
```

```yaml
  rust-test:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@v6
      - uses: dtolnay/rust-toolchain@stable
      - uses: Swatinem/rust-cache@v2
      - uses: taiki-e/install-action@nextest
      - run: cargo nextest run --workspace --locked --profile ci
      - run: cargo test --doc --workspace --locked     # nextest does not run doctests
      - if: ${{ !cancelled() }}
        uses: actions/upload-artifact@v4
        with: { name: junit-rust, path: target/nextest/ci/junit.xml, retention-days: 7 }
```

## 12. Android emulator and EAS in CI

**GitHub hosted emulator** with `reactivecircus/android-emulator-runner@v2` (README, 2026-10). Linux runners need KVM enabled first. Cache the AVD snapshot so boots are fast.

```yaml
  android-instrumented:
    runs-on: ubuntu-latest
    timeout-minutes: 30
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-java@v4
        with: { distribution: temurin, java-version: 21 }
      - uses: gradle/actions/setup-gradle@v5
      - name: Enable KVM
        run: |
          echo 'KERNEL=="kvm", GROUP="kvm", MODE="0666", OPTIONS+="static_node=kvm"' | sudo tee /etc/udev/rules.d/99-kvm4all.rules
          sudo udevadm control --reload-rules
          sudo udevadm trigger --name-match=kvm
      - id: avd-cache
        uses: actions/cache@v5
        with:
          path: |
            ~/.android/avd/*
            ~/.android/adb*
          key: avd-35
      - name: Create AVD snapshot
        if: steps.avd-cache.outputs.cache-hit != 'true'
        uses: reactivecircus/android-emulator-runner@v2
        with:
          api-level: 35
          arch: x86_64
          target: google_apis
          force-avd-creation: false
          emulator-options: -no-window -gpu swiftshader_indirect -noaudio -no-boot-anim -camera-back none
          disable-animations: false
          script: echo "snapshot created"
      - name: Instrumented tests
        uses: reactivecircus/android-emulator-runner@v2
        with:
          api-level: 35
          arch: x86_64
          target: google_apis
          force-avd-creation: false
          emulator-options: -no-snapshot-save -no-window -gpu swiftshader_indirect -noaudio -no-boot-anim -camera-back none
          disable-animations: true
          script: |
            ./gradlew :app:connectedDebugAndroidTest --stacktrace
            adb logcat -d > logcat.txt || true
      - if: ${{ !cancelled() }}
        uses: actions/upload-artifact@v4
        with: { name: android-test-${{ github.run_attempt }}, path: "app/build/reports/androidTests\nlogcat.txt", retention-days: 7 }
```

For Expo / React Native with Maestro, the same runner works: build the APK first (`npx expo prebuild` and `./gradlew assembleRelease`, or download an EAS build), then in `script:` install it with `adb install` and run `maestro test .maestro/`. In CI the emulator belongs to the runner, so the user's local rules about their own emulator and input do not apply there, but the agent still never runs these locally without a yes.

Google measured the Android emulator as its flakiest tool (25% of emulator tests had some flakiness, versus 1.65% for all tests, Listfield 2017), mostly because emulator tests are large. Keep this job small: the critical flows only, `disable-animations: true`, retries 2 with flaky reporting, and logic tested in JVM unit tests instead.

**EAS Workflows** (Expo's own CI, docs 2026-10) can build and run Maestro on EAS hosted emulators and simulators with the pre-packaged `maestro` job:

```yaml
# .eas/workflows/e2e.yml
name: e2e
on:
  pull_request:
    branches: ['main']
jobs:
  build_android:
    type: build
    params:
      platform: android
      profile: preview
  maestro_android:
    needs: [build_android]
    type: maestro
    params:
      build_id: ${{ needs.build_android.outputs.build_id }}
      flow_path: ./.maestro
```

Other job types include `fingerprint` and `get-build` (reuse a build when the native fingerprint did not change, which saves most of the build time), `repack` (new JS bundle on an existing build, for fast feedback), `update`, `submit` and `require-approval`. Run a workflow by hand with `eas workflow:run .eas/workflows/e2e.yml`. EAS minutes cost money on the free tier limits; check the owner's plan before making it run on every PR.

## 13. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| Focused tests blocked | `forbidOnly` on CI; Vitest default not overridden | `rg -n 'forbidOnly|allowOnly' playwright.config.* vitest.config.* package.json` |
| No retries on unit tests | retries 0 for unit and integration | `rg -n 'retry|retries|reruns|test-retry' vitest.config.* jest.config.* .config/nextest.toml pyproject.toml build.gradle* .github/workflows` |
| Retried passes reported | Playwright flaky category visible, nextest FLAKY, Vitest JSON query or equivalent in the summary | read the workflow; look for the flaky step |
| Quarantine has owner and date | every skip used as quarantine matches `quarantine: #id owner=x until=YYYY-MM-DD` | section 5 enforcement command |
| Quarantine enforced | CI step fails on expired entries and on more than the cap | read the workflow |
| Quarantined tests still run | a nightly non blocking job runs them | `rg -n 'quarantine|run-ignored|schedule:' .github/workflows` |
| Every job has a timeout | `timeout-minutes` count equals job count | `rg -c 'timeout-minutes' .github/workflows/*.yml` vs jobs |
| Artifacts on failure | traces, screenshots, JUnit, logs uploaded with `!cancelled()` and a retention | read the workflow |
| Shards balanced and merged | `fullyParallel: true` with Playwright shards; blob reports merged in one job | `rg -n 'fullyParallel|blob|merge-reports' playwright.config.* .github/workflows` |
| Affected selection safe | PRs use `--changed`/`affected`; config, migration and fixture changes run everything; main runs all | read the workflow |
| Base branch fetched | `fetch-depth: 0` or explicit base fetch where `--changed` is used | read the workflow |
| Matrix justified | each extra OS, version or API level has a reason in a comment | read the matrix |
| Emulator job lean | KVM enabled, AVD cached, animations off, critical flows only | read the job |
| Local rules respected | the agent wrote CI config but did not launch browsers or emulators locally unless the user allowed it | the agent's report |
