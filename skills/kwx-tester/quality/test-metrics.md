# Test metrics

Which numbers about tests tell you something, how to get them, and which ones only look good. Use this file when the owner asks "how good are our tests?", when an audit needs evidence, or when someone proposes a target like "80% coverage" or "500 tests".

## Contents

1. Rules
2. Numbers that mean something
3. Vanity numbers
4. Goodhart's law in testing
5. Checks

## 1. Rules

1. **Measure outcomes (bugs that escaped, time to know), not activity (tests written).** A suite exists to catch bugs before users do, fast and reliably. Evidence: moderate.
2. **Never turn a test metric into a target for the person or agent being measured.** "When a measure becomes a target, it ceases to be a good measure" (Marilyn Strathern's phrasing of Goodhart's law). Google's coverage guidance warns that mandated numbers become a checkbox (Arguelles et al. 2020). Evidence: moderate.
3. **Report a trend with its context, never a lone number.** "Flaky rate 3%, down from 6% last month; 2 tests in quarantine, both with owners" says something; "flaky rate 3%" does not.
4. **Every number cites its source and window** (CI runs since a date, git log window, issue tracker query).

## 2. Numbers that mean something

| Metric | What it tells you | How to get it | Notes |
|---|---|---|---|
| Escaped defects | bugs found by users or in production instead of by tests, per release or month | issues labelled `bug` and `found-in-prod` (or created from crash reports) per release | the outcome metric. Each one should get a regression test (`regression-and-release-testing.md` rule 3); track which test level should have caught it |
| Flaky rate | share of tests or runs that pass and fail on the same commit | retried passes from CI (`ci-testing.md` section 4), same commit fail then pass (`test-suite-audit.md` step 7) | Google reported about 1.5% of runs flaky and 16% of tests with some flakiness (Micco 2016); Slack's test job failure rate went from 57% to under 5% after handling flaky tests (2022). Track tests in quarantine and their age too |
| Suite time | how long until a developer knows | p50 and p95 of the test job duration over the last 50 runs: `gh run list --workflow test -L 50 --json startedAt,updatedAt` | fast feedback is the whole value of a test loop (Wacker 2015); kwx-developer budget: under 10 minutes to a PR verdict |
| Time red on main | how long the main branch stays broken | time between a failing and the next passing run on main | a main that is red most of the time trains everyone to ignore CI |
| Mutation score on changed or risky code | whether the tests would notice a wrong result where it matters | `cargo mutants --in-diff`, Stryker `--mutate <files>` (`test-suite-audit.md` step 9) | Google shows developers surviving mutants per change rather than a global score; for 70% of 1,502 high priority bugs, the bug introducing change was already covered by tests and a mutant on it would have flagged the gap (Petrović et al. 2021) |
| Mean time to detect | from the commit that introduced a bug to the first signal (failing test, alert, user report) | issue links to the bad commit; CI history | moving detection left (unit before e2e before users) is the goal |
| Change failure rate | share of deployments that cause a failure needing a fix, rollback or hotfix (DORA) | deploy log and incident or hotfix list | a release level outcome; pairs with failed deployment recovery time |
| Uncovered changed lines and branches | gaps in the code just written | `diffgaps.py` or `vitest --coverage.changed` (`coverage.md` section 5) | a list to read, not a percentage to hit |
| Fix commits with a test | whether bugs get regression tests | `test-suite-audit.md` step 12 | aim for every behaviour fix |

## 3. Vanity numbers

| Number | Why it misleads | Use instead |
|---|---|---|
| Test count | 500 tests can check nothing (tsDetect found 34% of Android test files had a test with no assertion); counting rewards splitting and trivial tests | escaped defects, mutation score on risky code |
| Raw coverage percentage for the repo | coverage is only weakly related to fault detection once suite size is controlled (Inozemtseva and Holmes 2014); averages hide a 0% payment module | named uncovered branches in risky and changed files |
| Pass rate without flaky data | 100% green with retries hides flakiness; 98% may be one flaky test | pass rate plus retried passes plus quarantine count |
| Lines of test code, test to code ratio | says nothing about what the tests check | same as test count |
| Number of bugs a tester reported | rewards splitting and duplicate reports, punishes prevention | escaped defects and time to detect |
| "Zero skipped tests" | invites deleting tests instead of fixing them | skipped tests with owner, reason and date (`ci-testing.md` section 5) |

## 4. Goodhart's law in testing

What happens when each number becomes the goal, and the guard:

| Target | What people (and agents) do | Guard |
|---|---|---|
| "80% coverage" | tests without assertions that execute code; `ignore` comments on hard code; thresholds lowered when the number drops | read uncovered changed lines instead; `smellscan.py` for `NO-ASSERT`; review every ignore (`coverage.md` rule 8) |
| "All tests green" | retries hide flakiness; failing tests get skipped; assertions weakened or deleted | retried passes reported; skips need owner and date; test diffs reviewed (kwx-developer `~/.claude/skills/kwx-developer/ai-agents/tests-and-honesty.md`) |
| "Flaky rate under 1%" | flaky tests dumped into quarantine and never fixed; Slack found suppressed tests were hard to re-enable | quarantine cap and expiry enforced in CI |
| "N tests per feature" | trivial tests, one assertion each, many per method | review test intent, not count |
| "Suite under 5 minutes" | slow but important tests deleted or moved to a job nobody watches | move them to a nightly job that blocks release, with an owner |
| "Mutation score 90%" | tests written to kill equivalent or unproductive mutants (logging, timeouts) | survivors reviewed one by one; Google suppresses unproductive mutants and relies on reviewers to push back on low value tests |

AI agents are especially exposed: when they can see the scorer, they game it (kwx-developer `~/.claude/skills/kwx-developer/ai-agents/tests-and-honesty.md` cites METR and ImpossibleBench). Give an agent behaviours to prove, not a number to reach, and read its test diffs.

## 5. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| Outcome metric included | any test quality report has escaped defects or mean time to detect, or says why they are not available | read the report |
| Flaky data with every pass rate | pass rates come with retried pass counts and quarantine size | read the report |
| No lone repo coverage number | coverage appears only as named gaps or a trend with context | read the report |
| Sources and windows cited | each number names its query and date range | read the report |
| No metric set as a target for the agent | the task or plan states behaviours to test, not a number to reach | read the plan |
