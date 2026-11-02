# Test suite audit

How to audit an existing project's tests, step by step: find how the tests are run, run them and time them, list what is switched off, find tests that check nothing, sleeps and real network, flaky history, coverage gaps ranked by risk and churn, a mutation sample on the riskiest module, and the test levels that are missing. Then rank the findings and ask the owner about each one. The audit changes nothing in the repo: findings are asked about, not fixed, with the same three answers as kwx-developer (Later to TODO.md, Plan a fix, Keep as is to DECISIONS.md; procedure and exact wording in `~/.claude/skills/kwx-developer/workflow/audit-and-ask.md`).

Commands marked "verified" were run on 2026-10-31 on real repos of the owner (a 220 commit React and Vite app with 894 Vitest tests, a 182 commit Kotlin and Compose Android app) or on small fixtures. Others come from the tool docs named next to them.

## Contents

1. Rules
2. The checklist
3. Step by step
4. Ranking the findings
5. Asking and recording
6. The report
7. Checks

## 1. Rules

1. **Read the user's rules first** (their CLAUDE.md and project instructions). If they forbid launching a browser, an emulator or a GUI app, do not run Playwright, Maestro, instrumented Android tests or Quickshell UI tests yourself: list them as "not run, needs the owner's yes" and audit them by reading. If they forbid touching input devices, never use `adb shell input` or similar.
2. **Change nothing in the repo.** No config edits, no installed packages, no fixed tests. Write reports and caches outside the repo (`--coverage.reportsDirectory=$SCRATCH/cov`, `--outputFile=$SCRATCH/results.json`). Check `git status --porcelain` before and after; it must be the same.
3. **A tool hit is a lead, not a finding.** Open the test and confirm before it reaches the owner (kwx-developer audit rule 2).
4. **Measure, do not guess.** Suite time, pass counts and flaky history come from real runs and CI data, not from reading config.
5. **One finding per pattern per area**, with a key (section 4).
6. **Respect earlier answers.** Read DECISIONS.md and TODO.md first; drop findings on the do-not-flag list and add "Seen again" lines to open TODO items instead of asking again (kwx-developer `~/.claude/skills/kwx-developer/workflow/audit-and-ask.md` section 3).
7. **Time box.** A full audit of a mid size repo is 20 to 40 minutes of tool time. Mutation testing is limited to one module and 30 minutes.

## 2. The checklist

Copy this into your notes and tick it off.

```
- [ ] 0 Rules read (CLAUDE.md), DECISIONS.md and TODO.md read, git status clean noted
- [ ] 1 Test commands found (scripts, CI, task runners)
- [ ] 2 Inventory: frameworks, test files per level, config
- [ ] 3 Suite run and timed (fast suites only; browser/emulator suites need a yes)
- [ ] 4 Switched off: skip, only, todo, xfail, ignore, conditional skips
- [ ] 5 Smell scan: no assertion, empty, liars, sleeps (test-smells.md)
- [ ] 6 Real network and shared state
- [ ] 7 Flaky history: CI reruns and same commit fail then pass; local repeat of suspects
- [ ] 8 Coverage gaps ranked by churn and risk
- [ ] 9 Mutation sample on the riskiest module
- [ ] 10 Missing levels and missing kinds of tests
- [ ] 11 CI: which tests run where, time, retries, artifacts
- [ ] 12 Bug fixes without tests
- [ ] 13 Rank, key, filter (section 4)
- [ ] 14 Summary table, then ask (section 5)
- [ ] 15 Report (section 6), git status unchanged
```

## 3. Step by step

### Step 1. Find the test commands

Tests that are not run by a command nobody knows about are not tests. Find every entry point, and compare what developers run with what CI runs.

```bash
# package scripts (JS/TS)
jq -r '.scripts | to_entries[] | select(.key|test("test|e2e|spec|check|ci|cov")) | "\(.key): \(.value)"' package.json
# CI workflows: every run line that tests something
rg -n 'run:.*(test|vitest|jest|playwright|maestro|nextest|cargo test|gradlew|pytest|coverage)' .github/workflows
ls .eas/workflows 2>/dev/null && rg -n 'type: (maestro|build)' .eas/workflows
# task runners
rg -n '^[a-z][\w-]*:' justfile Justfile Makefile 2>/dev/null | rg -i 'test|check|e2e'
# Rust, Kotlin, Python
ls .config/nextest.toml 2>/dev/null; rg -n '^\[\[test\]\]|^\[dev-dependencies\]' -A8 Cargo.toml | head -30
./gradlew tasks --all -q 2>/dev/null | rg -i 'test|kover|jacoco' | head    # slow first time; skip if no JDK
rg -n '\[tool\.pytest|\[tool\.coverage|addopts' pyproject.toml pytest.ini setup.cfg 2>/dev/null
```

Verified on the Kotlin app: CI ran `:engine:check`, `:app:testDebugUnitTest`, lint and `connectedDebugAndroidTest` in an emulator job. Findings here: a test suite that CI never runs, a script that runs a different set than CI, no test command at all.

### Step 2. Inventory

```bash
# test files per kind (adjust globs to the repo)
git ls-files | rg -c '\.(test|spec)\.[jt]sx?$'                 # JS/TS unit and component
git ls-files | rg -c '(^|/)e2e/|\.e2e\.|playwright'            # web e2e
git ls-files | rg -c '(^|/)\.?maestro/.*\.ya?ml$'               # mobile e2e
git ls-files | rg -c '/src/test/.*\.kt$'                        # Kotlin JVM unit
git ls-files | rg -c '/src/androidTest/.*\.kt$'                 # Android instrumented
git ls-files | rg -c '(^|/)tests/.*\.rs$'; rg -l '#\[cfg\(test\)\]' -g '*.rs' | wc -l   # Rust integration, unit
git ls-files | rg -c '(^|/)test_\w+\.py$|_test\.py$'            # Python
git ls-files | rg -c 'supabase/tests/.*\.sql$'                  # pgTAP database tests
git ls-files | rg -c 'tst_\w+\.qml$'                            # QML (Qt Quick Test)
# test code vs source code size
echo "test lines: $(git ls-files | rg '\.(test|spec)\.|/tests?/|/src/test/' | xargs cat 2>/dev/null | wc -l)  source lines: $(git ls-files 'src/*' 'app/*' 'lib/*' | rg -v '\.(test|spec)\.|/test/' | xargs cat 2>/dev/null | wc -l)"
```

Write the shape down as a short table (level, count, framework). Compare it to the target mix in kwx-developer `testing-strategy.md` section 2; an ice cream cone (mostly e2e) or an hourglass (unit and e2e, nothing between) is a finding (Wacker, Google Testing Blog 2015).

### Step 3. Run the suite and time it

Run the fast suites with the project's own command, with machine readable output written outside the repo. Do not run browser, emulator or device suites unless the user's rules allow it.

```bash
# Vitest (verified: 894 tests, 26 s wall with coverage, git status unchanged)
npx vitest run --reporter=json --outputFile="$SCRATCH/results.json"
jq -r '"tests \(.numTotalTests) passed \(.numPassedTests) failed \(.numFailedTests) skipped \(.numPendingTests) todo \(.numTodoTests)"' "$SCRATCH/results.json"
jq -r '.testResults[] | .name as $f | .assertionResults[] | "\((.duration // 0)|floor) ms  \($f|split("/")|.[-1])  \(.title)"' "$SCRATCH/results.json" | sort -rn | head
jq -r '.testResults[] | "\((.endTime-.startTime)|floor) ms \(.name)"' "$SCRATCH/results.json" | sort -rn | head -5
# Jest
npx jest --json --outputFile="$SCRATCH/results.json"
# Rust (nextest shows SLOW and per test time; docs)
time cargo nextest run --workspace --no-fail-fast   # or: time cargo test --workspace
# Kotlin
time ./gradlew testDebugUnitTest --continue   # per test times in app/build/test-results/**/TEST-*.xml
# Python
time pytest -q --durations=15 -p no:cacheprovider
```

Real output from the React app: the slowest single test took 14.6 s (an app level test), one file took 20 s and a convergence test file 16 s, out of 26 s total. One slow test is fine; a unit suite over a minute, or single "unit" tests over a second, are findings ("slow-suite").

Record: total, passed, failed, skipped, wall time, the 5 slowest tests. A suite that is red on the main branch is the first finding, above everything else.

### Step 4. What is switched off

```bash
# explicit skips and focus (verified on fixtures)
rg -n --pcre2 '\b(it|test|describe)\.(skip|only|todo|fixme)\b|\.(skipIf|runIf)\(|\b(xit|xdescribe|fit|fdescribe)\(|#\[ignore|cfg_attr\([^)]*ignore|@Ignore|@Disabled|assume(True|That)?\(|pytest\.mark\.(skip|skipif|xfail)|pytest\.skip\(|@unittest\.skip' \
   -g '!**/node_modules/**' -g '!**/target/**' .
# age of each skip: who and when
rg -n --pcre2 '\.(skip|fixme)\(|#\[ignore|@Ignore|mark\.skip' -g '!**/node_modules/**' . | while IFS=: read f l _; do
  echo "$(git blame -L "$l,$l" --porcelain "$f" | awk '/^author-time/{print strftime("%Y-%m-%d",$2)}') $f:$l"; done | sort
```

Verified lesson: the React app's JSON reported 4 skipped tests, and the first grep found none. They were behind `describe.runIf(process.env.IFC_CHECK)`, a conditional skip. Always compare the runner's skipped count with the grep; conditional skips (`runIf`, `skipIf`, `skipif`, `assumeTrue`, `cfg_attr(..., ignore)`) are easy to miss. A conditional skip that CI never enables is a test that never runs.

Findings: focused tests (always), skips older than 30 days or with no reason and issue, xfail without `xfail_strict`, conditional suites no CI job enables.

### Step 5. Smell scan

Run the linters and `smellscan.py` from `test-smells.md` section 2 over all test folders. Then read every `EMPTY` and `NO-ASSERT` hit, and the liar patterns of section 3.3. Count the rest per flag and per folder; report them grouped.

### Step 6. Real network and shared state

```bash
# leads
rg -n "https?://(?!localhost|127\.0\.0\.1|example\.(com|org))" --pcre2 -g '*.test.*' -g '*.spec.*' -g 'tests/**' -g '**/src/test/**' .
rg -n "onUnhandledRequest|disable-socket|nock\.disableNetConnect" .   # network blocked anywhere?
# proof: run the unit suite with no network at all (verified on Arch, no root needed; loopback stays usable)
unshare -rn sh -c 'ip link set lo up && npx vitest run'      # or: cargo test, pytest, ./gradlew test --offline
# shared state: shuffle and parallel
npx vitest run --sequence.shuffle.tests --sequence.shuffle.files      # verified flags (Vitest 5)
npx jest --randomize
pytest -p randomly                                   # needs pytest-randomly; do not install into the repo
cargo nextest run                                     # one process per test exposes hidden globals (nextest docs)
```

A unit test that fails inside `unshare -rn` but passes outside talks to the network: a finding with the test name. If `unshare` is not allowed on the machine (`unshare: unshare failed: Operation not permitted`), fall back to the greps. A suite that fails only shuffled has order dependence.

### Step 7. Flaky history

CI history is the best evidence. A flaky test is one that passed and failed on the same commit.

```bash
R=$(gh repo view --json nameWithOwner -q .nameWithOwner)
# runs re-attempted, and same commit + workflow with both failure and success (verified on a 100 run history)
gh api "repos/$R/actions/runs?per_page=100" --jq '.workflow_runs[] | [.head_sha[0:7], .name, .conclusion, .run_attempt] | @tsv' \
 | awk -F'\t' '{k=$1"\t"$2; s[k]=s[k]" "$3; if($4>1) r[k]=1} END {for(k in s) if ((s[k] ~ /failure/ && s[k] ~ /success/) || r[k]) print k"\t"s[k]}'
# how red is main
gh api "repos/$R/actions/runs?branch=main&per_page=100" --jq '.workflow_runs[].conclusion' | sort | uniq -c
# which job and step failed in a run
gh run view <run-id> --log-failed | head -50
```

On this machine use `gh-axi` when the user's rules ask for it (`gh-axi run list`, `gh-axi api ...`); the `gh api` lines above are the fallback. Verified on the Kotlin app: no same commit flips, but 60 of the last 100 runs failed. A main branch that is red most of the time trains everyone to ignore CI, which is a finding of its own.

Then repeat the suspects locally (never the whole browser suite without a yes):

```bash
npx vitest run path/to/suspect.test.ts --repeats=50          # verified flag (Vitest 5)
npx playwright test e2e/checkout.spec.ts --repeat-each=30 --retries=0 --workers=4   # needs the owner's yes when browsers are off
cargo nextest run suspect_name --retries 0 ; for i in $(seq 30); do cargo nextest run suspect_name || break; done
for i in $(seq 30); do ./gradlew :app:testDebugUnitTest --tests '*SuspectTest' --rerun -q || break; done
pytest tests/test_suspect.py --count=30 -x            # pytest-repeat
```

Also look for retries already hiding flakiness: `rg -n 'retries|retry|--retries|flaky-result|rerun' playwright.config.* vitest.config.* .config/nextest.toml .github/workflows pyproject.toml`. Retries without a report of retried passes is a finding (`ci-testing.md` section 4).

### Step 8. Coverage gaps ranked by churn and risk

Coverage alone ranks the wrong files: a 0% file nobody changes matters less than a 70% file changed every week that moves money. Combine churn, coverage and a risk word list. Script (verified on the React app):

`scripts/riskgaps.py` scores each file as commits times (uncovered lines plus untaken branches) and tags paths that match a risk word list (money, auth, sync, parse, delete and similar). Run it (from the repo root, lcov written outside the repo):

```bash
npx vitest run --coverage --coverage.include=src --coverage.reporter=lcov --coverage.reportsDirectory="$SCRATCH/cov"
python3 -I ~/.claude/skills/kwx-tester/scripts/riskgaps.py "$SCRATCH/cov/lcov.info"               # optional: "6 months ago" 'pay|auth|sync'
# Rust: cargo llvm-cov --workspace --lcov --output-path "$SCRATCH/lcov.info"
# Python: coverage run --branch -m pytest && coverage lcov -o "$SCRATCH/lcov.info"
# Kotlin: ./gradlew koverXmlReport, then rank by hand from build/reports/kover/report.xml, or use the hotspot list
python3 -I ~/.claude/skills/kwx-tester/scripts/riskgaps.py --selftest
```

It prints the top 20 files with score, commits, line and branch percentages, and `RISK` on risky paths. Start the audit at the top rows.

Real output (React app, trimmed):

```
   5772   39 commits  lines  93.6%  branches  77.1%    41 lines  107 branches  src/store/building.ts
   4020   15 commits  lines  79.4%  branches  64.2%    72 lines  196 branches  src/geometry/export.ts  RISK
   1989   17 commits  lines   0.0%  branches   0.0%    55 lines   62 branches  src/scene/Wall.tsx
   1177   11 commits  lines  64.0%  branches  53.1%    62 lines   45 branches  src/sync/useSync.ts  RISK
```

How to read it: the top file is well covered by lines but changed 39 times with 107 untaken branches, so it leads. `export.ts` and `useSync.ts` match the risk list (data export and sync can lose data). `Wall.tsx` at 0% is a 3D scene component: probably tested by eye, so check whether that is a deliberate decision before reporting. Without coverage tooling, use kwx-developer `~/.claude/skills/kwx-developer/quality/codebase-audit-tools.md` section 9 (which hotspots have any test importing them).

### Step 9. Mutation sample on the riskiest module

Pick the top RISK file from step 8 (or the money, auth or permission module the owner names). Run mutation testing on that file only, time boxed. Survivors show assertions that are missing even where coverage looks fine.

| Stack | Command (source) |
|---|---|
| JS/TS | `npx -y @stryker-mutator/core run --mutate 'src/geometry/export.ts' --testRunner vitest --reporters clear-text,html --htmlReporter.fileName "$SCRATCH/mutation.html"` (Stryker docs; needs `@stryker-mutator/vitest-runner` resolvable: if the repo does not have it, install Stryker in a scratch prefix, never in the repo) |
| Rust | `cargo mutants --file src/billing.rs --timeout 60 -o "$SCRATCH"` (cargo-mutants docs) |
| Rust, changed code only | `git diff origin/main > "$SCRATCH/changes.diff" && cargo mutants --in-diff "$SCRATCH/changes.diff"` (mutants.rs) |
| Kotlin JVM | PIT via the `info.solidsoft.pitest` Gradle plugin (JVM modules); for Android modules `pl.droidsonroids.pitest`. Both need a build file change, so in an audit only propose it, do not add it |
| Python | `uvx mutmut run` with `paths_to_mutate` in `[tool.mutmut]` (mutmut 3 reads only pyproject, so write a copy of the project to the scratchpad if the repo has no config) |

Report: mutants created, killed, survived, timed out, score, and the top 5 survivors as plain sentences ("changing `>` to `>=` in the minimum order check was not caught"). Do not write the tests for them in the audit; each surviving cluster is a finding (`untested-risk:<file>` or `weak-assertions:<file>`). Google surfaces only a few mutants per change and suppresses unproductive ones (logging, equivalent code); do the same and skip survivors in log lines.

### Step 10. Missing levels and missing kinds of tests

Look for what is absent. Absence never shows in a pass rate.

| Project type | Ask | Detect |
|---|---|---|
| Any | Are the core user flows tested end to end at least once? | e2e or Maestro count from step 2 is 0 |
| Web app (Next.js, Vite) | Are API routes tested through HTTP or as handlers? Is there an accessibility check? | `rg -l 'route\.ts|api/' -g '*.test.*'`; `rg -n 'axe|toHaveNoViolations|@axe-core' -g '*.test.*' -g '*.spec.*'` |
| Supabase backend | Are row level security policies tested as each role? | `git ls-files supabase/tests`; `rg -n 'set local role|request.jwt.claims|pgtap' supabase` |
| React Native / Expo | Any Maestro flows, any component tests? | `.maestro/` exists; `rg -l '@testing-library/react-native'` |
| Kotlin / Compose | Any instrumented or Compose UI tests? Robolectric? | `src/androidTest` count; `rg -n 'createComposeRule|Robolectric'` |
| Rust CLI or TUI | Is the binary tested from outside (args, exit codes, stdout)? | `rg -n 'assert_cmd|Command::cargo_bin|trycmd|insta' tests Cargo.toml` |
| Quickshell / QML | Any Qt Quick Test or logic tests for JS helpers? | `git ls-files | rg 'tst_.*\.qml'`; tests for the `.js` modules |
| Data migrations | Is each migration tested up (and down, if supported) on a copy of real shaped data? | `rg -l 'migrat' -g '*test*'` |
| Anything with money or auth | Property tests or table tests over the rules? | `rg -n 'fast-check|proptest|quickcheck|hypothesis|@ParameterizedTest|it\.each|test\.each'` |

Each missing level for a core flow is one finding (`missing-level:<what>`), not one per screen.

### Step 11. CI

Read `ci-testing.md` and check its Checks table against the workflows: which suites run on pull requests, which only on main or nightly, which never; total time; retries and whether retried passes are reported; artifacts kept on failure; job timeouts. The most common real finding: e2e or instrumented tests exist but no CI job runs them.

### Step 12. Bug fixes without tests

A fix with no test change can come back. Ratio over the last year (verified on the React app: 3 fix commits with a test, 5 without):

```bash
git log --since="12 months ago" -i --grep='^fix' --format='%h' | while read h; do
  git show --name-only --format= "$h" | rg -q '\.(test|spec)\.|(^|/)tests?/|__tests__|/src/test/' && echo T || echo "N $h $(git log -1 --format=%s "$h" | cut -c1-70)"
done | awk '$1=="T"{t++} $1=="N"{n++; print} END{print t+0" fixes with a test, "n+0" without"}'
```

Read the "without" list: CI or config fixes need no test; behaviour fixes do. Report the behaviour fixes without tests as one finding with the list.

## 4. Ranking the findings

Priorities follow kwx-developer `~/.claude/skills/kwx-developer/quality/tech-debt-and-todo.md` section 3, applied to tests:

| Priority | Test findings |
|---|---|
| P1 | Suite red on main, or main red in most recent CI runs. Tests that cannot fail (Liar, Empty, Unknown) on money, data, auth or permission code. A top 5 churn file on a risk path with no tests. A suite the team believes runs in CI but does not. Focused test (`.only`) committed |
| P2 | Flaky tests (same commit fail then pass) or retries hiding them. Sleepy tests and real network in unit tests. Skips with no reason or older than 30 days. A missing level for a core flow (no e2e at all, no API tests, no RLS tests). Risk files in the top 15 of `riskgaps.py`. Surviving mutant clusters on risky code. Behaviour fixes without tests |
| P3 | Style smells (roulette, eager, magic numbers, general fixture). Slow but stable tests. Snapshot hygiene on internal output |

Keys: kwx-developer's fixed list (`~/.claude/skills/kwx-developer/quality/codebase-audit-tools.md` section 10) has `untested-risk`. The tester adds these kinds, used the same way (`kind:area`):

| kind | Example key |
|---|---|
| `untested-risk` | `untested-risk:src/sync/useSync.ts` |
| `test-smell` | `test-smell:liar-src/api` , `test-smell:sleepy-e2e` |
| `skipped-test` | `skipped-test:ifc-openshell` |
| `flaky` | `flaky:checkout.spec.ts/applies-coupon` |
| `missing-level` | `missing-level:e2e`, `missing-level:rls` |
| `weak-assertions` | `weak-assertions:src/billing/invoice.ts` (surviving mutants) |
| `ci-tests` | `ci-tests:e2e-not-in-ci`, `ci-tests:main-red` |
| `slow-suite` | `slow-suite:app-test` |
| `fix-without-test` | `fix-without-test:last-12-months` |

Filter against DECISIONS.md and TODO.md exactly as in kwx-developer `~/.claude/skills/kwx-developer/workflow/audit-and-ask.md` section 3 (drop Accepted keys in scope, add "Seen again" to open TODO keys).

## 5. Asking and recording

1. Show the ranked summary table first (plain chat text), so the owner sees the whole list:

```text
Test audit, 2026-10-31. Ran: unit suite (894 tests, 26 s, all green), coverage, smell scan, CI history (100 runs).
Not run: Playwright e2e (browsers are off on this machine), mutation testing (no Stryker in the repo).

| # | Finding | Priority | Effort | Suggested |
| A1 | Data export (src/geometry/export.ts) changed 15 times, 196 branches never tested | P2 | M | Plan a fix |
| A2 | 4 IFC tests only run when IFC_CHECK is set; no CI job sets it | P2 | S | Plan a fix |
| A3 | 5 of 8 bug fixes this year came without a test | P2 | S | Later |
| A4 | 35 tests have more than 5 assertions without messages | P3 | S | Keep as is |
```

2. Ask one question per P1 and P2 finding, recommended answer first, with the fixed labels and descriptions from kwx-developer `~/.claude/skills/kwx-developer/workflow/audit-and-ask.md` section 6 (`Later`, `Plan a fix`, `Keep as is`). Translate test words into plain words for the owner: "assertion" becomes "the check at the end of a test", "flaky" becomes "passes or fails at random on the same code", "mutant" becomes "a small bug I planted on purpose that no test noticed".
3. Bundle all P3 findings into one question.
4. Record each answer at once: TODO.md item (Later), a plan shown before any change (Plan a fix), DECISIONS.md entry with the key and scope (Keep as is).

Recommend `Plan a fix` for anything on money, data or auth paths and for liars; `Keep as is` when a whole folder is consistently untested by choice (for example 3D scene components checked by eye); `Later` for small issues in quiet code.

## 6. The report

```text
Test audit done. Changed in the repo: nothing (git status same as before).
Ran: <commands with counts and times>. Not run, needs your yes or tools: <list>.
Suite: <n> tests, <passed>/<failed>/<skipped>, <time>; slowest: <test, time>.
Shape: <unit n, integration n, e2e n>; missing: <levels>.
Flaky: <same commit flips n>, main red in <x> of last <y> runs.
Coverage: top risk gaps <3 files with branches>. Mutation: <file, score, top survivors> or not run.
Findings: P1 <n>, P2 <n>, P3 <n>. Answers: Later <n>, Plan <n>, Keep <n>, not reviewed <n>.
For you to check by hand: <short checklist, for suites the agent may not run>.
```

## 7. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| Rules read | The report names what the user's rules allowed and what was not run because of them | report "Not run" line |
| Repo unchanged | `git status --porcelain` identical before and after | run it twice, compare |
| Outputs outside the repo | coverage, results JSON, mutation reports in the scratchpad | paths in the commands used |
| All entry points found | Every test script and CI test step listed; mismatches between local and CI noted | step 1 notes |
| Suite measured | totals, time and slowest tests come from a real run | results JSON or runner output saved |
| Skips counted two ways | grep count compared with the runner's skipped count; conditional skips found | step 4 notes |
| Hits confirmed | each smell finding opened and read | notes list path:line and verdict |
| Flaky evidence real | flaky claims cite CI runs (same commit) or a local repeat count | step 7 output |
| Gaps ranked by churn and risk | coverage findings name files from `riskgaps.py` or the hotspot list, not a repo average | step 8 output |
| Mutation time boxed | one module, at most 30 minutes, or "not run" with the reason | step 9 notes |
| Absences checked | the step 10 table was walked for the project type | step 10 notes |
| Keys and filtering | every finding has a `kind:area` key; Accepted decisions and open TODO keys filtered | findings list |
| Nothing fixed unasked | no test or config edited during the audit | `git diff` empty |
