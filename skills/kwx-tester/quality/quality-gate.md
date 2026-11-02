# The quality gate for testing work

An item marked **[critical]** blocks shipping on its own.

Run this gate before you call any testing work done: tests for a feature, a change tested, a bug hunt, a test suite audit, a release check. It checks the tester's own work: that the expected values came from the spec, that every new test can fail, that the numbers in the report are real, that the risks and states are covered, and that the user's rules were kept. Green tests prove only what they test; this gate checks that they test something. When the same task changed product code, kwx-developer's gate (`~/.claude/skills/kwx-developer/quality/quality-gate.md`) runs on that code, and kwx-designer's gate on UI files; this gate does not replace them.

Every row gets PASS, FAIL or N/A with its evidence: the command and its output, a file:line, or the note where the proof is recorded.

## Contents

1. How to run the gate
2. A. Spec and oracle
3. B. Tests prove something
4. C. Honesty and runner numbers
5. D. Coverage of risks and states
6. E. Platform specifics
7. F. The user's rules
8. G. The report
9. Report format
10. Fast checks
11. Checks

## 1. How to run the gate

1. Set the base: the commit the task started from (`git rev-parse HEAD` at the start) or the merge base with the main branch. Note `git status --porcelain` at the start.
2. Run section 10 first; its output is evidence for many rows.
3. Go through A to G. Mark each row PASS, FAIL or N/A with evidence. A row that does not apply says why (no UI, no backend).
4. Fix every FAIL in the tests, the plan or the report, never by weakening a test or this gate. Rerun the failed rows and section 10.
5. Score with `scoring-rubric.md`. Report in the format of section 9.

## 2. A. Spec and oracle

| # | Check | Pass condition | Verify |
|---|---|---|---|
| A1 [critical] | A written basis | Numbered acceptance criteria exist, quoted from the spec or confirmed by the owner; every gap is an assumption `A1..An` in the plan and the test names | the plan; `rg -n 'assumption A[0-9]' <test files>` |
| A2 [critical] | Expected values from the spec, not the code | Every assertion traces to an AC, an assumption, a property or a reference version; no expected value was copied from current output (except tests named as characterization) | the AC to test mapping table; read new assertions against the spec |
| A3 | Independence recorded | The report names the setup: tests before the build, a fresh tester subagent with an interface pack, or same context blind mode; and whether it was enforced (`../ai-agents/oracle-independence.md` section 4); why a tester subagent was or was not launched, with the risk tier (../strategy/strategy.md section 5a) | the report |
| A4 | Code read only after expected values | The implementation was read for extra inputs only after the case list with expected values was written | conversation order |
| A5 | Failures triaged | Each failing new test has a verdict (product bug, wrong test, unclear spec) with the spec line; no failure resolved by editing the expected value to the actual output | the triage notes |
| A6 | Characterization labelled | Tests pinned to current behaviour say so in their names and in the report | `rg -n -i 'characterization' <test files>` against the plan |
| A7 | Project records read | The user's and project's CLAUDE.md, DECISIONS.md and TODO.md were read; no test asserts against an Accepted decision | the notes; `rg -n -i '<area words>' DECISIONS.md` |

## 3. B. Tests prove something

| # | Check | Pass condition | Verify |
|---|---|---|---|
| B1 [critical] | Every new test seen failing for the right reason | Each new or changed test has a recorded proof: red before the fix, a killed mutant, or an ablation drop; the failure is the guarding assertion, not plumbing; a planted fault batch counts as proof for every test it turned red (../ai-agents/proving-tests-work.md section 4) | the evidence blocks (`../ai-agents/proving-tests-work.md` section 9) |
| B2 [critical] | No existing test weakened to get green | No existing test, assertion, snapshot or fixture deleted, skipped, focused, loosened or blind updated, unless the owner confirmed the behaviour changed and the report names the line that requires it | `git diff --stat "$BASE" -- '*test*' '*spec*' tests __tests__ e2e '*.snap'`; section 10 focus and skip grep |
| B3 | Assertions on observable behaviour | New tests assert response, stored rows, rendered text by role, exit code or output; no assertion free test, no `toBeTruthy` on a complex value as the only check, no assertion only on mock calls | smellscan on the new test files; read each new test |
| B4 | Doubles only at boundaries | No mock of the unit under test or of code the project owns; real local database where the project has one | `rg -n '(vi|jest)\.mock\(' <new tests>` read against `../strategy/test-doubles.md` |
| B5 | Mutation on high risk changed code | Money, auth, permissions, migrations, parsers: no unexplained surviving mutant on the changed lines | the mutation tool output and the triage of each survivor |
| B6 | Whole deliverable ablated | For a new feature or module, its core turned into a no-op made the covering tests go red | the ablation note |
| B7 | Held-out check last | A check the builder did not run (held-out set, differential run, fresh judge) ran at the end, or the report says why none existed | the report |
| B8 | No special casing passed | When testing someone else's change: the product diff has no test environment branches or test literals | `../workflow/test-a-change.md` step 7 output |
| B9 | No fixed waits | New tests wait for conditions, never `waitForTimeout`, `sleep` or fixed timeouts | section 10 sleep grep |

## 4. C. Honesty and runner numbers

| # | Check | Pass condition | Verify |
|---|---|---|---|
| C1 [critical] | Runner numbers reported, total above zero, skips explained | Every suite run in the report shows total, passed, failed, skipped and flaky from the runner's own output of the last fresh run, with the exit code; total above 0; the new tests appear by name; each skipped test or group has a reason and "new" or "existed before" | compare the report with the runner's JSON or summary lines (`../ai-agents/honest-reporting.md` section 3) |
| C2 [critical] | New tests repeated by flake risk | New tests with I/O, a database, time or timers, concurrency, network, randomness or UI rendering ran 20 times green alone and in the suite plus one shuffled run, retries off (slow CI only suites at least 5, stated); small deterministic tests (pure functions, fixed inputs, no I/O, no clock) ran in one shuffled suite run plus 2 repeats; each new test file is labelled flake risk or deterministic in the notes | the class per file, the repeat commands and their output (../strategy/flaky-tests.md section 3) |
| C3 [critical] | No claim without a run | Nothing reported as run or passing that did not run in this task; subagent numbers re-run before quoting | the Ran block against the session's commands |
| C4 [critical] | Product code untouched by the tester | The tester's diff holds only test files, fixtures it created, the plan and notes; mutation and ablation left no trace in the user's tree | `git status --porcelain` and `git diff --stat "$BASE"` read against the tester's path list |
| C5 | Flaky named | Every pass after a retry is counted as flaky and named | the runner's flaky count or retry records |
| C6 | Pre-existing failures proven | A failure the task did not cause is shown failing on the base (worktree), reported, not fixed | the base run |
| C7 | Not run listed | Each suite or check not run has a reason and how it will run (CI job, the owner's command) | the report |
| C8 | Unproven tests not counted | New tests with no proof are listed as unproven, outside the new passed count | the report |

## 5. D. Coverage of risks and states

| # | Check | Pass condition | Verify |
|---|---|---|---|
| D1 [critical] | High risks have a test that fails when the risk happens | Each risk scored 6 or more (likelihood x impact) has at least one test seen failing when the risk is planted, or the owner accepted the gap in writing | the risk register in the plan; evidence blocks |
| D2 | Every AC tested | Each acceptance criterion maps to at least one test | the mapping table |
| D3 | Every UI state covered | Each row of the UI states list (loading, empty, error, limit, offline, loading more, end of list, and the feature's own) has a test. Offline, error, empty, limit, signed out and any state that disables or hides an action get a rendered component test (Testing Library, jest-expo, or the toolkit's offscreen renderer) asserting the visible text by role and that the guarded action is disabled or refused; a test of a pure viewState or reducer does not count for these. A human check line only for how a state looks (layout, colour, motion) | the plan against the states list |
| D4 | Every error code tested | Each error code in the contract has a test that triggers it and checks the response and the state it drives | `rg -n '<code>' <test files>` per code |
| D5 | Edge cases from the catalogue | Empty, one, many, too long, Unicode and Kazakh or Cyrillic text, valid IDN emails (user@müller.de), time zones and DST, concurrent or double submit: each one that applies has a test or a reason | the case list (`../exploratory/edge-case-catalogue.md`) |
| D6 | Changed lines covered or explained | Diff coverage gaps on changed lines each have a test from a requirement or a reason | `scripts/diffgaps.py` output |
| D7 | One journey per core flow | The core user journey has an end to end or integration test through the real wiring (run in CI if the rules keep it from running here) | the test list |
| D8 | Exploratory pass | At least one chartered session on the top risk for a feature, with notes; a product with a daily user also ran the daily-use charter (../exploratory/exploratory.md section 3) and its findings are in the bug list | the session file |
| D9 | Derived numbers and time | Each number shown to the user has a test for each event that changes it and for 0; each money value agrees across every surface it appears on (UI, CSV, PDF, API) with a rounding sensitive fixture; interval code has a start == stop case; date code ran under the business zone and a far zone (Pacific/Auckland) on server and client | the counters table (../workflow/test-from-spec.md section 6), the consistency tests (../strategy/test-oracles.md section 3), the two TZ runs in the Ran block |
| D10 | Tests follow risk across layers | The register has Layer and Tier columns; a layer holding 25% or more of the risk score holds at least 10% of the tests or has a reason line; the report gives tests per layer beside risk per layer | the register and the report (../strategy/strategy.md section 5) |

## 6. E. Platform specifics

Mark the rows for the platforms the task touched; the rest are N/A.

| # | Platform | Pass condition | Verify |
|---|---|---|---|
| E1 | Web | Role and label locators, web first assertions, isolated test data; axe checks on changed pages; browserless smoke run when browsers are off; title tests assert the brand per language; aria-current and required state asserted; the width probe at 390 and 360 ran per route, or the report says why width was not measured (../web/playwright.md section 5); test servers take their port from an env var or port 0, no literal port or range (../web/playwright.md section 14) | `../web/web.md` checks; `scripts/smoke_site.py` output |
| E2 | Mobile | Logic and screens tested without a device first (Jest, JVM, Robolectric); device flows written as Maestro or instrumented tests; the mobile edge case list walked for each new screen; Expo Router has one test per session state and no test files under src/app; the offline rendered set exists (../mobile/react-native-expo.md sections 5 and 7) | `../mobile/mobile.md` section 9; `../mobile/mobile-edge-cases.md` |
| E3 | Backend | HTTP level tests on a real local database; another user's object returns 404; each mutation tried twice for idempotency; RLS by role matrix in pgTAP for Supabase | `../backend/backend.md` checks |
| E4 | Desktop | Tests run offscreen or headless (`QT_QPA_PLATFORM=offscreen`); the user's live desktop never driven; Tauri: invoke names equal the registered commands and each command is crossed once through get_ipc_response with the frontend's camelCase keys; QML harnesses load through the real entry file (../desktop/desktop.md sections 4 and 6) | `../desktop/desktop.md` checks |
| E5 | CLI or TUI | Exit codes, stdout and stderr asserted; golden output reviewed; TUI frames rendered to a test backend | `../desktop/cli-and-tui-testing.md` checks |
| E6 | Accessibility | Automated checks where the stack has them; names and roles asserted in tests; keyboard and screen reader items on the human checklist | `../exploratory/accessibility-testing.md` checks |
| E7 | Performance | Any speed claim measured as percentiles with the environment named; no average only claims | `../performance/performance.md` section 8 |

## 7. F. The user's rules

| # | Check | Pass condition | Verify |
|---|---|---|---|
| F1 [critical] | Browser, device and input rules followed | No browser, browser MCP, emulator input, device flow or desktop driving that the user's rules forbid; no second emulator created, no system image downloaded; runs that need a yes had one | the commands run in this task, against the rules read at the start |
| F2 [critical] | No em or en dashes | None in test names, fixtures, plans, notes, bug reports or the report | section 10 dash grep prints nothing |
| F3 [critical] | No production data or real side effects | No production database or account touched; no real email, SMS, push or payment sent; test accounts and disposable data only | session notes; environment variables used |
| F4 | No watermarks or AI markers | No "generated by" lines, attribution comments or markers in test files, plans or reports | `rg -n -i 'generated (by|with)|co-authored-by' <tester files>` |
| F5 | Irreversible actions confirmed | Every delete, send, publish, pay or permission change in a test environment had the user's yes | conversation |
| F6 | Owner's rules win | The user's global CLAUDE.md, ~/.claude/agents, the UI mistakes library, then the project's CLAUDE.md and DECISIONS.md were followed where they differ from this skill | the notes |
| F7 | UI mistakes library walked | For UI under test, each applicable entry of ~/.claude/ui-designer/mistakes.md was checked from code; only what code cannot settle is on the human list, with its M-id | code check notes and the human list cite M-ids (../exploratory/human-check-handoff.md) |

## 8. G. The report

| # | Check | Pass condition | Verify |
|---|---|---|---|
| G1 | Template followed | The report follows `../ai-agents/honest-reporting.md` section 5: not done first, basis, independence, Ran, new tests and proofs, bugs, waiting on the owner, not run, coverage gaps, risks not covered | read the report |
| G2 | Bugs in format | Each bug in the format of `../exploratory/bug-reports.md`, most severe first, handed to the right owner with the failing test path | the bug list |
| G3 | Human checklist | At most 10 lines, ranked, each with where, action and what correct looks like, starting with what was already verified | `../exploratory/human-check-handoff.md` checks |
| G4 | Findings asked, not fixed | Test problems noticed outside the task are listed with keys; questions only for P1 and P2 in the tested area, with the three answers | `../workflow/test-suite-audit.md` section 7 |
| G5 | Safety language | No absolute claim from a sample ("works", "secure"); "in the cases I tried", "I did not check" | read the report |
| G6 | Score given | Rubric score with one line of evidence per dimension | `scoring-rubric.md` |
| G7 [critical] | README claims verified | For an app or feature delivery: every run, test and build command in README.md ran from a clean clone with no machine specific paths, test counts match the last fresh run, and the sections the brief asks for are present (run, test, build, decisions, not finished); N/A with a reason when nothing was delivered. A command that would open a browser, app window, emulator or device follows rule 7. Run its headless part (build, start the server and curl it, cargo test), and list the rest as 'owner to run' in the README table. That is not a FAIL | the README table (../workflow/release-check.md section 4b) |

## 9. Report format

```text
Quality gate (tester): <feature, change, hunt or audit>
Scope: <n> test files new, <n> changed; tester's diff: tests and plan only (C4)
A Spec and oracle      7/7 (A3: fresh tester subagent with interface pack, enforced by instruction)
B Tests prove          8/9 (B6 N/A: bug fix, no new module)
C Honesty and numbers  8/8
D Risks and states     9/10 (D7: e2e journey written, runs in CI only)
E Platform             E1 PASS, E3 PASS, others N/A
F User's rules         7/7
G Report               7/7
Critical items: all pass
Layers: server 40 tests (risk 18), client UI 22 (risk 12), bridge 6 (risk 6)
Score (scoring-rubric.md): <per dimension>, ship: yes/no
Ran:
  pnpm vitest run --reporter=json --outputFile=$SCRATCH/v.json  exit 0  total 214, passed 214, failed 0, skipped 3, flaky 0
  pnpm vitest run tests/acceptance/comments --repeats 20        exit 0  12 tests x 20, 0 failures
Not run: <list with reasons and how each will run>
```

## Fast checks

Run from the repo root in bash. Each hit is a lead to read, not an automatic FAIL. The scripts are run, not read: `python3 -I ~/.claude/skills/kwx-tester/scripts/<name> --help` prints the usage, `--selftest` proves the script on built in fixtures.

```bash
BASE=${BASE:-$(git merge-base HEAD origin/main 2>/dev/null || git rev-parse HEAD)}
S=~/.claude/skills/kwx-tester/scripts
# test smells in new and changed test files (B3, B4, B9)
python3 -I $S/smellscan.py $(git diff --name-only "$BASE" -- '*test*' '*spec*'; git ls-files -o --exclude-standard -- '*test*' '*spec*')
# changed lines and branches no test ran (D6)
python3 -I $S/diffgaps.py "$SCRATCH/cov/lcov.info" "$BASE"     # lcov from the project's coverage run (quality/coverage.md section 6)
# files ranked by churn x untested code (D1, audits)
python3 -I $S/riskgaps.py "$SCRATCH/cov/lcov.info"
# browserless smoke of a site (E1, release checks)
python3 -I $S/smoke_site.py http://localhost:3000 / /pricing/
# post deploy smoke from a checks file, "path status [text]" per line (quality/regression-and-release-testing.md section 4)
python3 -I $S/smoke_checks.py <base-url> <checks-file>

# tests touched by the task: every line needs a reason (B2)
git diff --stat "$BASE" -- '*test*' '*spec*' tests __tests__ e2e '*.snap'
# focused, skipped and todo tests added (B2)
git diff "$BASE" | grep -E '^\+.*(\b(it|test|describe|context)\.(only|skip|todo)\(|\b(xit|xdescribe|xtest)\(|#\[ignore|@pytest\.mark\.(skip|xfail)|t\.Skip\(|@Disabled|@Ignore|test\.fixme\()'
# fixed waits added (B9)
git diff "$BASE" | grep -E '^\+.*(waitForTimeout\(|thread::sleep|time\.sleep\(|Thread\.sleep\(|setTimeout\([^,]*resolve|\bsleep [0-9])'
# retries added that could hide flakiness (C5)
git diff "$BASE" | grep -E '^\+.*(retries\s*[:=]\s*[1-9]|--retr(y|ies)[= ][1-9]|retry\s*:\s*[1-9])'
# test knowledge in product code (B8)
git diff "$BASE" -- . ':!*test*' ':!*spec*' ':!tests' ':!e2e' | grep -E '^\+.*(NODE_ENV.*test|cfg!\(test\)|PYTEST_CURRENT_TEST|process\.env\.CI)'
# product files changed by the tester (C4): should list only test paths, the plan and notes
git status --porcelain; git diff --name-only "$BASE"
# em and en dashes in everything the tester wrote (F2)
git diff "$BASE" | grep -P '^\+.*[\x{2013}\x{2014}]'                                   # added lines in tracked files
git ls-files -o --exclude-standard -z | xargs -0 -r grep -nP '[\x{2013}\x{2014}]'      # new untracked files
grep -nP '[\x{2013}\x{2014}]' "$SCRATCH"/*.md 2>/dev/null                              # plan, notes and report drafts
# Tauri: invoke names vs registered commands (E4), prints nothing when they match
diff <(grep -rhoE "invoke(<[^>]*>)?\(\s*['\"][a-z_][a-z0-9_]*" src | grep -oE "[a-z_][a-z0-9_]*$" | sort -u) <(sed -n '/generate_handler!\[/,/\]/p' src-tauri/src/*.rs | sed 's/.*generate_handler!\[//; s/\].*//' | grep -oE '[a-z_][a-z0-9_]*\s*(,|$)' | grep -oE '^[a-z_][a-z0-9_]*' | sort -u)
# Literal ports in test harnesses (E1), only env fallbacks may show
rg -n ':[0-9]{4}\b|port\s*[=<]=?\s*[0-9]{4}' tests e2e playwright.config.* vitest.config.* 2>/dev/null
# Expo Router: test files inside the routes folder (E2), prints nothing
find src/app app -path '*__tests__*' -o -name '*.test.*' 2>/dev/null
# README sections the brief asks for (G7)
rg -n -i 'not finished|open questions|decisions' README.md
```

End with one count line in the report: `<N> leads read, <M> fixed, <K> kept with a reason`.

## 11. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| Every row marked | each row of A to G is PASS, FAIL or N/A with evidence | read the gate notes |
| No open critical | no [critical] row is FAIL: A1, A2, B1, B2, C1, C2, C3, C4, D1, F1, F2, F3, G7 | read those ids in the notes |
| Fast checks run | section 10 output is in the notes with the count line | read the notes |
| Fixes were in the tests or the report | no FAIL turned PASS by weakening a test, a lint config or this gate | `git diff "$BASE" -- '*test*'` read for loosening |
| Other gates too | product code changes in the task ran kwx-developer's gate; UI files ran kwx-designer's | the joint report |
