# Test a change: a diff, a PR or a bug fix someone else made

The procedure for testing a change the tester did not write: kwx-developer's bug fix, a teammate's PR, an agent's branch. The builder has usually written its own tests, and they pass. The tester's job is to find out whether they mean anything and whether the change does what its intent says, without inheriting the builder's view. The order matters: the intent and the bug come first, the bug is reproduced end to end as a user would hit it, the tester writes its own failing test from the bug report before reading the fix, then it checks the builder's tests, the changed lines (coverage and mutation), the whole change (ablation, special casing), and the rest of the suite. For reviewing a test PR as code, use `../quality/review-method.md`; this file is about testing the product change.

## Contents

1. The steps as a checklist
2. Step 1: intent, acceptance and the base
3. Step 2: reproduce the bug end to end first
4. Step 3: the tester's own failing test, before reading the fix
5. Step 4: the builder's test changes
6. Step 5: fail on base, pass on the change
7. Step 6: changed lines: diff coverage and mutation
8. Step 7: the whole change: ablation and special casing
9. Step 8: neighbours and regression run
10. Step 9: report
11. Checks

## 1. The steps as a checklist

```
- [ ] 1 Intent in one line; acceptance list or bug report; BASE set
- [ ] 2 Bug reproduced end to end on BASE, the way a user meets it (or "could not", with what was tried)
- [ ] 3 Own failing test written from the bug report or intent, before reading the fix
- [ ] 4 Builder's test diff read: no weakened, skipped or deleted test; new tests assert behaviour
- [ ] 5 Every new test (own and builder's) fails on BASE for the right reason, passes on the change
- [ ] 6 Diff coverage gaps explained; mutation on changed lines, survivors explained
- [ ] 7 Ablation of the change drops the score; no special casing of test inputs in product code
- [ ] 8 Neighbouring cases and the full suite run; pre-existing failures proven on BASE
- [ ] 9 Repeats, gate, report
```

## 2. Step 1: intent, acceptance and the base

1. Get the change: `git diff --stat "$BASE"...HEAD` for a branch; `gh pr view <n> --json title,body,files` and `gh pr diff <n> > "$SCRATCH/pr.diff"` for a PR (`gh-axi pr view <n>` where the user's rules prefer it). Set `BASE` to the merge base.
2. Write the intent in one line from the bug report, issue, PR title and description. If none states it, derive an acceptance list from the issue and the user's words, not from the code, and say so.
3. For a bug fix, the bug report is the spec: steps, expected (with its oracle), actual. If it is vague, sharpen it with the reporter or the owner before going on (`../exploratory/bug-reports.md` section 2).
4. Read the rules (user's CLAUDE.md, project CLAUDE.md, DECISIONS.md lines for the area): a decision can make the "bug" intended.

## 3. Step 2: reproduce the bug end to end first

Start where the user meets the bug, on the code before the fix. A fix verified only by a unit test the fixer wrote can fix the wrong thing. Evidence: opinion, consistent with kwx-developer's bug fix rule and the 29.6% of "passing" SWE-bench patches that behave differently from the real fix (PatchDiff, strong).

Run the base in a scratch worktree so the user's tree stays as it is:

```bash
git worktree add -q "$SCRATCH/base" "$BASE"
cd "$SCRATCH/base" && ln -s "$OLDPWD/node_modules" node_modules 2>/dev/null   # or install / cargo build inside the copy
```

| Product | Reproduce end to end with |
|---|---|
| API or backend | `curl` against the base server on a free port, the exact request from the report; the database row it writes (`psql -c 'select ...'`) |
| Web page | `curl` the built page (`next build && next start -p 3100` in the worktree), the browserless smoke script; a browser only if the user's rules allow it, otherwise the owner reproduces it from a checklist line |
| CLI or TUI | the built binary with the report's arguments and input; exit code, stdout, stderr; a PTY test for TUIs (`../desktop/cli-and-tui-testing.md`) |
| Mobile | a Jest or JVM test through the real screen or view model; device steps only with the user's yes, or handed to the owner |
| Supabase RLS | `supabase test db` with a pgTAP case acting as the affected role, or `psql` with `set local role authenticated; set local request.jwt.claims = '...'` |

Record: the command, the output that shows the bug, and the configuration (commit, zone, locale, data). If the bug does not reproduce on the base, stop and say so: the fix cannot be tested against a bug nobody saw. Ask the reporter for the missing condition.

## 4. Step 3: the tester's own failing test, before reading the fix

Write one test that reproduces the bug through the real path (the route, the command, the public function, the screen), from the bug report alone. Do not open the fix's diff of product files yet. With kwx-developer in the team, setup A or B of `../ai-agents/oracle-independence.md` section 4 applies: the tester (or a fresh tester subagent briefed with the bug report and the public interface) writes it. It must fail on the base for the reason in the report.

Then add the neighbours the report implies (`../exploratory/bug-reports.md` section 4, "more general"): the westward case of an eastward time zone bug, the empty and maximum versions of a boundary bug, the other role in a permission bug. Expected values come from the spec or the report.

## 5. Step 4: the builder's test changes

Read the builder's test diff as the riskiest part of the change (agent authored tests: weak or no oracle in 80.2% of patches; mocks added in 36% of agent commits; evidence strong).

```bash
git diff --stat "$BASE"...HEAD -- '*test*' '*spec*' tests __tests__ e2e '*.snap'
git diff "$BASE"...HEAD -- '*test*' '*spec*' tests __tests__ | rg '^[-+].*(\.only\(|\.skip\(|\.todo\(|xit\(|xdescribe\(|xfail|#\[ignore|t\.Skip\(|SkipTest|waitForTimeout|sleep\()'
python3 -I ~/.claude/skills/kwx-tester/scripts/smellscan.py $(git diff --name-only "$BASE"...HEAD -- '*test*' '*spec*')
```

| Look for | Verdict |
|---|---|
| a deleted or loosened assertion, a widened tolerance, a new skip or `.only`, a snapshot updated together with source and no test reasoning | blocker unless the intent changes that behaviour and the description says which line requires it |
| a test that asserts the fixed output with a literal copied from the new code and no spec source | weak oracle: check it against the report; if it only pins output, label it characterization |
| the unit under test mocked, or a mock of the project's own code; assertions only on mock calls | the test checks the mock; finding |
| no assertion, `toBeTruthy()` on a complex value, `expect(fn).not.toThrow()` as the only check | finding |
| a new test that passes on the base too (step 5 shows it) | it does not test the fix |

## 6. Step 5: fail on base, pass on the change

Every new test, the tester's and the builder's, runs on both:

```bash
cp tests/streak.timezone.test.ts "$SCRATCH/base/tests/"         # copy the new tests into the base worktree
(cd "$SCRATCH/base" && npx vitest run tests/streak.timezone.test.ts)    # must fail, for the right reason
npx vitest run tests/streak.timezone.test.ts                            # must pass on the change
```

A builder's test that passes on the base proves nothing about the fix: report it. A tester's test that still fails on the change is a candidate bug in the fix: triage it (`../ai-agents/oracle-independence.md` section 6) and hand it back in the bug report format.

## 7. Step 6: changed lines: diff coverage and mutation

1. Coverage of the changed lines and branches, as a gap finder (`../quality/coverage.md` section 5):
   ```bash
   npx vitest run --coverage --coverage.reporter=lcov --coverage.reportsDirectory="$SCRATCH/cov"   # or cargo llvm-cov --lcov
   python3 -I ~/.claude/skills/kwx-tester/scripts/diffgaps.py "$SCRATCH/cov/lcov.info" "$BASE"     # changed lines never run, branches never taken
   ```
   Each changed line no test ran gets a test from the intent, or a reason.
2. Mutation on the changed lines only (`../strategy/mutation-testing.md` section 7):
   ```bash
   git diff "$BASE"...HEAD > "$SCRATCH/changes.diff"
   cargo mutants --in-diff "$SCRATCH/changes.diff"                                  # Rust
   npx stryker run --mutate "$(git diff --name-only "$BASE"...HEAD -- 'src/**/*.ts' ':!**/*.test.ts' | paste -sd, -)"   # TS
   ```
   Every survivor: write the killing test from the spec, or record it as equivalent with a reason. Report the score before and after.

## 8. Step 7: the whole change: ablation and special casing

Test file diffs miss the dominant cheats now: special casing, lookup tables, behaviour placed outside the deliverable (EvilGenie, SpecBench, *Building to the Test*; evidence strong).

1. **Ablation.** In a scratch worktree at HEAD, turn the fix or the feature's core into a no-op (return the input, return the default, skip the write) and run the covering tests. The score must drop; list the tests that went red (`../ai-agents/proving-tests-work.md` section 5).
2. **Special casing scan** of the product diff:
   ```bash
   git diff "$BASE"...HEAD -- . ':!*test*' ':!*spec*' ':!tests' | rg '^\+.*(NODE_ENV.*test|cfg!\(test\)|PYTEST_CURRENT_TEST|process\.env\.CI|import\.meta\.vitest)'
   # literal values from the new tests appearing in product code
   rg -o --no-filename "toBe\((['\"][^'\"]{4,}['\"]|[0-9]{3,})\)" $(git diff --name-only "$BASE"...HEAD -- '*test*' '*spec*') | sort -u
   ```
   Then search the product diff for each literal printed. A test input or expected value hard coded in production code is a blocker.
3. **Fresh judge over the diff**, for changes on money, auth, data or a large agent written change. Start a read-only subagent (Read, Grep, Glob, read-only Bash) with the intent, the bug report and the diff path, and ask only: "Does this change solve the general problem, or does it special case particular inputs, hard code expected values, use a lookup table, or put the behaviour somewhere the tests reach but users do not? Quote file:line for each finding, with a counterexample input the change gets wrong. Do not comment on style." An LLM judge measured about 1% false positives and 16.7% false negatives on this task (EvilGenie; strong, one benchmark). Check every finding it returns with a test before reporting it.

## 9. Step 8: neighbours and regression run

1. Run the tests that cover the changed files (`~/.claude/skills/kwx-developer/ai-agents/tests-and-honesty.md` section 4 has the per stack commands: `npx vitest related`, `npx jest --findRelatedTests`, `cargo test -p` plus dependents).
2. Run the full suite with the project's command. Read the numbers from the runner (`../ai-agents/honest-reporting.md` section 3).
3. A failure that also fails on the base is pre-existing: prove it in the base worktree, report it, do not fix it.
4. Re-run the original end to end reproduction from step 2 on the change: it must now show the expected behaviour.
5. Walk the area around the fix for a few minutes (Whittaker's garbage collector's tour, `../exploratory/heuristics.md` section 14): other callers of the changed function, the same pattern elsewhere (`rg -n '<the buggy pattern>'`).
6. New tests: repeated by flake class (20 runs for flake risk, one shuffled run plus 2 repeats for deterministic), retries off (gate C2, `../strategy/flaky-tests.md`).

Clean up: `git worktree remove --force "$SCRATCH/base"`; `git status --porcelain` in the user's tree matches the start.

## 10. Step 9: report

Run `../quality/quality-gate.md` and score with `../quality/scoring-rubric.md`, then report in the template of `../ai-agents/honest-reporting.md` section 5, with these lines added:

```text
Change: <PR or branch>, intent: <one line>. Verdict: fixes the bug | does not fix it | fixes it partly (<what is left>)
Reproduced on BASE: <command> -> <output showing the bug>. After the change: <same command> -> <expected output>
Builder's tests: <n> new, <n> changed. Failing on BASE: <n of n>. Findings: <weakened / passes on base / mocks the unit / none>
Tester's tests: <n> new, all red on BASE for the right reason, green on the change, 20/20 repeats
Diff coverage: <n> changed lines never run (<where, why>). Mutation on changed lines: <score before -> after, survivors left and why>
Ablation: <what was no-op'd> -> <n> tests red. Special casing scan: <clean | file:line>
```

Bugs in the fix go back to the builder in the handoff format of `../exploratory/bug-reports.md` section 8, with the failing test path and "do not edit the test to pass; if you think it is wrong, flag it".

## 11. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| Intent written | one line intent or an acceptance list from the issue, not from the code | notes |
| Reproduced first | the bug shown on BASE end to end, with command and output, before reading the fix | conversation order; the Reproduced line |
| Own test before the fix | tester's failing test written from the report before the product diff was opened | conversation order |
| Builder's tests checked | test diff read; no weakened, skipped or deleted test without a stated reason | step 4 commands and notes |
| Fail to pass for every new test | each new test red on BASE for the right reason, green on the change | step 5 runs |
| Changed lines checked | diff coverage gaps explained; mutation survivors on changed lines explained | step 6 output |
| Ablation drops the score | at least one covering test goes red when the change is a no-op | step 7 notes |
| No special casing | scan clean, or each hit reported with file:line | step 7 output |
| Regression run | covering tests and full suite ran; pre-existing failures proven on BASE | Ran block |
| Tree clean | worktrees removed; user's `git status --porcelain` unchanged | run it |
