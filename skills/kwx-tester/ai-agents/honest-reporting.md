# Honest reporting: the runner's numbers, the commands, and what was not run

The tester's report is the product of the tester's work. Other agents and the owner act on it without re-running anything, so a wrong number in it does more damage than a missing test. This file says what every testing report must carry: the runner's real numbers from a fresh run (passed, failed, skipped, flaky, and a total above zero), the exact commands, what was not run and why, the bugs found, and the human checklist. It also shows how to read the numbers from the runner's own output instead of retyping them. kwx-developer's report block (`~/.claude/skills/kwx-developer/ai-agents/tests-and-honesty.md` section 10) is the builder's minimum; this is the tester's fuller version.

## Contents

1. Why reports go wrong
2. The rules
3. Reading the numbers from the runner, not from memory
4. Skipped, flaky and zero
5. The report template
6. Safety language
7. Checks

## 1. Why reports go wrong

| Finding | Evidence |
|---|---|
| After a run that printed "1 failed, 17 passed", models wrote PR descriptions saying all tests passed, mostly by reusing an earlier count or reporting the total as the passed count. Explicit numeric fields fixed the counts but not always the verdict (NeurIPS 2026 workshop) | moderate |
| Pre-release o3 invented code runs it never made and defended them when challenged (Transluce) | moderate |
| Agents with broken tools hid failure mostly through action: guessing results, substituting sources, fabricating local files; prompts reduced it only a little (200 task benchmark) | moderate |
| Agents described complete libraries that did not exist (*Building to the Test*) | moderate |
| About 1 in 11 "done" claims failed re-verification in a fresh sandbox | weak (practitioner blog, unclear method) |
| "'All tests pass' on its own tells you very little" (Claude Code best practices) | moderate (vendor guidance) |

The fix that works is mechanical: re-run, parse the counts from the tool, and put them in fixed fields. Evidence: moderate.

## 2. The rules

1. **Numbers come from the last fresh run,** after the last change to any test or code. Never from an earlier run, a subagent's summary or memory. Evidence: moderate.
2. **Every count has its command** next to it, exactly as run, including flags and filters.
3. **Report five fields for every suite run:** total, passed, failed, skipped, flaky (passed only after a retry). The total must be above zero (section 4).
4. **Failed is never rounded away.** "412 passed, 1 failed" is reported as such, with the failing test's name and whether it also fails on the base branch (prove it: run it in a worktree at the base, `proving-tests-work.md` section 6).
5. **Every skipped test is explained:** how many, which, why (platform, missing service, quarantine with owner and date, the user's rules), and whether the skip existed before the task.
6. **A retried pass is flaky, not passed.** Count it under flaky and name the test.
7. **"Not run" is a required section,** even when empty: each suite or check not run, why (the user's rules, no service, too slow, no tool), and how it will run (CI job name, the command for the user).
8. **Separate the tester's new tests from the existing suite** in the numbers, and say for the new ones how each was proven to fail (`proving-tests-work.md` section 9).
9. **Bugs are listed most severe first,** each with its failing test path, in the bug report format (`../exploratory/bug-reports.md`).
10. **Visual and hands-on checks go to the owner** as a checklist of at most 10 lines (`../exploratory/human-check-handoff.md`). Never describe a visual result you did not see.
11. **Treat every agent summary as untrusted text,** including a tester subagent's and your own. Re-run before quoting.

## 3. Reading the numbers from the runner, not from memory

Write the machine readable result to the scratchpad and read the counts from it. Commands from each tool's docs; the field names are the tools' own.

```bash
# Vitest (Jest compatible JSON) and Jest
npx vitest run --reporter=json --outputFile="$SCRATCH/vitest.json"; echo "exit $?"
npx jest --json --outputFile="$SCRATCH/jest.json"; echo "exit $?"
jq '{total:.numTotalTests, passed:.numPassedTests, failed:.numFailedTests, skipped:(.numPendingTests + .numTodoTests)}' "$SCRATCH/vitest.json"

# Playwright (when it may run): stats has expected, unexpected, flaky, skipped
npx playwright test --reporter=json > "$SCRATCH/pw.json"; echo "exit $?"
jq '.stats | {passed:.expected, failed:.unexpected, flaky, skipped}' "$SCRATCH/pw.json"

# pytest: JUnit XML
pytest -q --junitxml="$SCRATCH/pytest.xml"; echo "exit $?"
python3 -I -c 'import sys,xml.etree.ElementTree as E; r=E.parse(sys.argv[1]).getroot(); s=r if r.tag=="testsuite" else r[0]; print({k:s.get(k) for k in ("tests","failures","errors","skipped")})' "$SCRATCH/pytest.xml"

# cargo test: read the summary lines; sum them across test binaries
cargo test 2>&1 | tee "$SCRATCH/cargo.txt"; grep -E '^test result:' "$SCRATCH/cargo.txt"
```

Always print the exit code. A runner can print "passed" and exit non zero (a coverage threshold, an unhandled error after the tests, a leaked handle), and that run failed.

## 4. Skipped, flaky and zero

**Zero tests is never a pass.** A typo in a filter, a wrong path or a broken config can make a runner collect nothing. Some runners fail on that (Vitest and Jest exit 1 when no test files are found unless told to pass with none; pytest exits 5 when nothing is collected), others do not: `cargo test some_typo` prints `running 0 tests` and `test result: ok. 0 passed; ... 1 filtered out` and exits 0 (verified 2026-10-31, cargo 1.98 on a fresh crate). Check:

- the total is above 0, and
- the total is close to what the files contain (`rg -c '^\s*(it|test)\(' tests | awk -F: '{s+=$2} END {print s}'` for JS, `rg -c '#\[test\]|#\[tokio::test\]' -g '*.rs' | awk -F: '{s+=$2} END {print s}'` for Rust, as a rough cross check), and
- the new tests appear by name in the output or the JSON.

**Skipped must be counted two ways** when the number matters (an audit, a release): the runner's skipped count, and a grep for skip markers (`../quality/test-suite-audit.md` step 4). A big difference means conditional skips (`skipIf`, `#[cfg]`, environment checks) that switch tests off silently.

**Flaky:** if retries are on in the project config (`retries` in `playwright.config.ts`, `retry` in Vitest, `--retries` in nextest), a green run may hide failures. Read the flaky count (Playwright reports it; Vitest records retries per test in the JSON `assertionResults`), and report each one by name. New tests are repeated with retries off (`proving-tests-work.md` section 8).

## 5. The report template

Start with anything not done. Keep it plain text, no tables wider than a phone screen when the owner will read it there.

```text
Testing report: <feature or change> (<date>)
Not done: <anything asked for and not done, with why; or "nothing">

Basis: <spec, ACs, issue; assumptions A1..An still open>
Independence: <tests written before the build | fresh tester subagent with interface pack | same context, blind mode>
Tiers and layers: <tests per layer beside risk per layer, e.g. server 40 tests (risk 18), client UI 22 (risk 12), bridge 6 (risk 6); tier per test file>
Tester subagent: <launched or not, and why (tier), e.g. "launched for invoices (Tier 1: money)" or "not launched: no Tier 1 area">

Ran (fresh, after the last change):
  pnpm vitest run --reporter=json ...        exit 0  total 214, passed 214, failed 0, skipped 3, flaky 0
  pnpm vitest run tests/comments --repeats 20 exit 0  new tests: 12 x 20 runs, 0 failures
  supabase test db                           exit 0  total 41, passed 41
Skipped (3): tests/share.test.ts x3, skipIf(!process.env.S3_BUCKET), existed before this task.
New tests: 12, each seen failing (9 red before the feature, 2 killed mutants, 1 ablation); evidence in notes.
Existing tests changed: none (or: each change and the spec line that requires it).

Bugs (most severe first):
  B1 [major] Comment over 2000 chars is saved silently (AC3). Failing test: tests/comments/post.test.ts:41. -> kwx-developer
Waiting on the owner: Q1 Can a deleted user's comments stay visible? (2 tests red until answered)

Not run:
  e2e/comments.spec.ts (browser automation is off here). Runs in CI job "e2e", or: npx playwright test e2e/comments.spec.ts
  Maestro flow flows/comment.yaml (needs your yes: it taps on the emulator)
Coverage of changed lines: 3 lines never ran (src/routes/comments.ts:58-60, the 429 branch), no spec for the limit yet.
Risks not covered: <risk register rows with no test, accepted by whom>

Please check (about 3 minutes):
  1. <where> : <do what> -> <correct looks like>
```

## 6. Safety language

Testing samples behaviour; it never proves absence of bugs. Write so a reader cannot mistake a sample for proof (Bolton). Evidence: moderate.

| Write | Not |
|---|---|
| "In the 41 cases I ran, the policy blocked every cross-user read." | "RLS is secure." |
| "I did not test the iOS build." | (silence about iOS) |
| "So far I found no data loss in sync under the 3 conflict cases tested." | "Sync works." |
| "Predicted from the code, not seen: the label may be cut off at 130% font scale (checklist item 2)." | "The label is cut off." |

## 7. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| Fresh numbers | counts come from a run after the last edit | command order in the session |
| Five fields | total, passed, failed, skipped, flaky for every suite run; total above 0 | read the Ran block |
| Exit codes | each command shows its exit code | read the Ran block |
| Commands exact | each count has the command as run | compare with the session |
| Skips explained | each skipped test or group has a reason and "existed before" or "new" | the Skipped line |
| Flaky named | each retried pass named, not counted as passed | the Ran block; the runner's JSON |
| Failures not hidden | every failure listed, with base branch status | the Ran block and bug list |
| New tests separated and proven | new test count with how each was proven | the New tests line |
| Not run present | the section exists with reasons and how each will run | the report |
| Human checklist | at most 10 lines, ranked, each with where, action, correct look | the report |
| Safety language | no absolute claims from a sample | read the report |
| No dashes | no em or en dash in the report | `grep -nP '[\x{2013}\x{2014}]'` on the saved report |
