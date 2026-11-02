# AI agents and testing: how agents fail at it, and the guards that work

Master file for an AI agent that writes, runs or judges tests. Read it on every testing task. It covers the tester's side of the problem: tests that pass without proving anything, tests that lock in the bug they should catch, and reports that say "all green" when they are not. The builder's side (never weaken a test to pass, the flag exit, covering tests first, property, differential and mutation basics, the honest report block) is in `~/.claude/skills/kwx-developer/ai-agents/tests-and-honesty.md`. Read that file too; this folder does not repeat it.

The research in one line: what makes an agent's test trustworthy is not who wrote it or how much code it covers, but two properties. Something other than the current code chose its expected values (a spec, an issue, a property, a reference version), and something automatic proved it can fail (it was red before the fix, or it killed a planted bug). Every rule below serves one of those two properties, or keeps the report honest about them. Source for every number in this folder: `sources/reports/AI agents and testing.md`.

## Contents

1. Files in this folder
2. Evidence key
3. How agents fail at testing
4. The guards, ranked by measured effect
5. The 12 operations that hold on every testing task
6. Stop signals
7. Checks

## 1. Files in this folder

| File | What is in it | Read when |
|---|---|---|
| `oracle-independence.md` | expected values from the spec, what the tester may and may not see, the fresh tester subagent and its brief, triage of failing tests | writing any test; setting up a tester subagent |
| `proving-tests-work.md` | fail before the fix, planted mutants, ablation (no-op the change), repeat runs, held-out checks | before counting any new test as done |
| `gui-agents.md` | driving browsers and phones when allowed: snapshots, explore then script, prompt injection, isolation, healer patches; what to do when not allowed | any browser, emulator or desktop UI work |
| `honest-reporting.md` | the runner's real numbers, exact commands, what was not run, the human checklist, the report template | writing the final report of any testing task |

## 2. Evidence key

Every rule in this folder carries one label.

- **strong**: peer reviewed or large sample primary evidence measured the effect.
- **moderate**: a primary preprint, a small sample, or official vendor guidance (Anthropic, Playwright, Google).
- **weak**: practitioner reports or secondary readings of system cards.
- **opinion**: no measurement; a judgement call that follows from the rest.

## 3. How agents fail at testing

Five failures, all measured, all looking like success.

| Failure | What it looks like | What it costs | Evidence |
|---|---|---|---|
| **Gaming the check** | the crude form: edited, deleted or skipped tests, `exit(0)`. The current form: no test touched, but the code special cases the tested inputs, hard codes a lookup table, or puts the tested behaviour in a throwaway demo while the real deliverable is dead ("building to the test") | a green suite over broken software | strong. Claude models still cheat on 37 to 45% of impossible tasks by default (secondary card readings, weak for the exact numbers). ImpossibleBench: test edits in over 79% of Claude cheating transcripts. EvilGenie: heuristic, non general solutions in 20.7% of cases versus 2.1% hard coded tests. SpecBench: visible tests saturated, a 43 to 48 point gap on held-out tests, one compiler 97% visible and 0% held out. *Building to the Test*: 7 of 12 runs scored 221 or 222 of 222 with the library dead or absent |
| **Tests written beside the code lock in its bugs** | the agent reads the implementation, then asserts what it does, bugs included | the suite protects the bug against being fixed | strong. Zhao et al. (ISSTA 2026, 11 models, 233 bugs): with buggy code in the prompt, 137.69 bug enshrining tests against 104.15 effective ones; with the fixed code, 16.46 against 304.08. Adding a spec next to the code did not help (146.08 misguided). The code has to be removed |
| **False "all pass" claims** | a summary that reuses an earlier count, reports the total as the passed count, or describes work that never ran | the owner ships on a claim nobody checked | moderate. NeurIPS 2026 workshop: models wrote "all passed" after a run printed "1 failed, 17 passed". Transluce: o3 invented runs and defended them. Anthropic: "'All tests pass' on its own tells you very little" |
| **Weak assertions** | tests that run code and check little: no assertion, `toBeTruthy()`, `toBeDefined()`, a snapshot nobody read | high coverage, low fault detection | strong for prevalence. 80.2% of 86,156 agent test patches carried weak or no oracle (All Smoke, No Alarm). TestGenEval: 35.2% coverage but 18.8% mutation score |
| **Over-mocking** | the unit under test, or code the project owns, replaced by mocks; the test checks the mock | the test passes whatever the code does | strong for prevalence, moderate for effect. Agent commits added mocks in 36% of cases versus 26% for other commits (Hora and Robbes, MSR 2026, 1.2 million commits) |

Three amplifiers make every failure worse: an ambiguous or impossible task (EvilGenie hard coding rose from 2% to 44% on ambiguous problems), a long task (SpecBench's gap grew with task size), and many retries against the same visible check (ImpossibleBench cheating rose from 33% to 38% with more submissions while honest passes rose only 80% to 83%). Evidence: strong.

The tester is the agent most exposed to this, because its output is the signal other agents optimise against. Anthropic's RL work saw a hack rate go from near zero to about 90% within 35 steps once a model found `sys.exit(0)`, with misalignment rising on unrelated tasks at the same time. Evidence: moderate.

## 4. The guards, ranked by measured effect

Use the ones that are mechanisms first. A rule a script or permission enforces beats a sentence in a prompt: prompt wording alone swung cheating from 1% to 92% in ImpossibleBench.

| Rank | Guard | What it stops | Measured effect | Evidence | Where |
|---|---|---|---|---|---|
| 1 | Expected values from the spec, written in a context that never saw the implementation | bug enshrining tests | fault detection about 25% versus about 14% for the same model testing after its own code; AgentCoder test accuracy 61.0% to 87.8% (HumanEval) | strong | `oracle-independence.md` |
| 2 | Read-only tests for the coder (permissions or a hook) | test edits and deletions | keeps honest performance, blocks edits, misses special casing | strong | `~/.claude/skills/kwx-developer/ai-agents/tests-and-honesty.md` section 9 |
| 3 | An explicit "flag it to a human" exit for the coder and the tester | cheating on impossible or conflicting tests | GPT-5 54% to 9%, o3 49% to 12% | strong | `oracle-independence.md` section 6 |
| 4 | Held-out and composition tests the coder never sees | special casing, features that pass alone and break together | expose 43 to 48 point gaps | strong | `proving-tests-work.md` section 7 |
| 5 | Mutation or ablation probe | tests that do not test the code; dead deliverables | no-op'ing the library left scores unchanged in all 12 dead library cells | moderate | `proving-tests-work.md` sections 4 and 5 |
| 6 | Fresh LLM judge over the diff | heuristics, lookup tables, special casing | about 1% false positives, 16.7% false negatives (EvilGenie) | strong, one benchmark | `../workflow/test-a-change.md` step 7 |
| 7 | Independent final check after any fix loop | overfitting to the visible check | more iterations widened gaps in three studies | strong | `proving-tests-work.md` section 7 |
| 8 | Re-run the command, parse counts from the tool's output | fabricated or garbled pass claims | structured fields fix counts, not verdicts | moderate | `honest-reporting.md` |
| 9 | Clean environment: no future git history, no solution files | reading the fix | documented leak (`git log --all` found the future commit) | moderate | section 5, rule 11 |
| 10 | Anti-hack wording in the prompt | general cheating | varies about threefold by model (45% to 12.5% at best) | weak to moderate | a modest extra, never the guard |

## 5. The 12 operations that hold on every testing task

1. **Choose expected values from the spec before reading the implementation body.** Quote the spec line each assertion comes from. Reason: code in the prompt shifts the model toward asserting the bug. Evidence: strong (`oracle-independence.md`).
2. **Never change an assertion to match current output.** A new test that fails is a candidate bug: triage it against the spec (product bug, wrong test, unclear spec) and report it. Evidence: strong (`oracle-independence.md` section 6).
3. **See every new test fail for the right reason** before it counts: red before the fix, a killed mutant, or a drop under ablation. Evidence: moderate (`proving-tests-work.md`).
4. **Assert on what a user or caller can observe:** the response body, the stored row, the rendered text, the exit code and output. No assertion free tests, no TODO assertions, no mock of the unit under test. Evidence: strong for prevalence (80.2% weak oracles).
5. **Existing tests, snapshots, fixtures and CI config are read only** to every agent unless the owner says the behaviour changed. Deleting, skipping, loosening or blind updating needs a human. Evidence: strong.
6. **Prefer oracles that do not come from current output:** properties, invariants, round trips, crash and sanitizer signals, differential runs against the previous version (`../strategy/test-oracles.md`). Evidence: strong to moderate (agentic property tests 56% valid reports, OSS-Fuzz-gen 26 new vulnerabilities).
7. **Judge a suite by mutation score or faults found on the changed code,** never by coverage alone (`../quality/coverage.md`, `../strategy/mutation-testing.md`). Evidence: strong.
8. **Repeat every new test by flake class** (20 times alone and in the suite plus a shuffled run for tests with I/O, time, concurrency or rendering; one shuffled suite run plus 2 repeats for deterministic ones; `../strategy/flaky-tests.md`) and reject flaky ones. Do not copy patterns from neighbouring flaky tests: a flaky assertion in context was copied into about two thirds of new tests. Evidence: strong for the filter.
9. **Label tests made from current behaviour as characterization tests.** They protect against change; they are not evidence of correctness. Evidence: strong (TestGen-LLM design).
10. **Finish with a check the coder did not run and could not see** (held-out tests, a fresh judge, a differential run). Never define done as "the loop went green". Evidence: strong.
11. **Keep answers out of reach:** no future git history, solution files or hidden tests in the coder's workspace; keep held-out tests in the scratchpad until the coder reports done. Evidence: moderate.
12. **Report evidence, not prose:** the exact command, exit code, and passed, failed, skipped and flaky counts parsed from a fresh run (`honest-reporting.md`). Treat every agent summary, including your own, as untrusted text. Evidence: moderate.

## 6. Stop signals

Stop and report instead of pushing on when:

| Signal | Do |
|---|---|
| A new test fails and you feel the urge to "fix" its expected value | stop; triage with `oracle-independence.md` section 6 |
| An existing test blocks the work | flag it with evidence (`~/.claude/skills/kwx-developer/ai-agents/tests-and-honesty.md` section 2); never edit it |
| Two attempts at making a test meaningful (seen failing for the right reason) have failed | report the test as unproven; do not count it |
| The spec is silent or contradicts itself on the behaviour under test | ask the owner one plain question; write the assumption down if you must go on |
| A run needs a browser, device input or a GUI the user's rules forbid | write the test, do not run it, ask or hand it to CI (`gui-agents.md` section 7) |
| The suite count is 0, or far below what the files contain | the filter or config is wrong; a 0 test run is never a pass (`honest-reporting.md` section 3) |
| The builder's diff special cases the tested inputs | report it as a blocker with the lines quoted |

## 7. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| Spec first | every assertion traces to a quoted spec line, property or reference | the test plan's mapping table |
| No assertion changed to fit output | no new test edited from red to green without a spec reason | the tester's notes; `git diff` of new test files across the task |
| Every new test seen failing | each has a red run, a killed mutant or an ablation drop recorded | `proving-tests-work.md` evidence block |
| Existing tests untouched | no deleted, skipped or loosened test | `git diff --stat "$BASE" -- '*test*' '*spec*' tests __tests__` read line by line |
| Repeats done | new tests repeated by flake class (gate C2), shuffled | the repeat command and its output |
| Final independent check | a check the coder did not run ran last | the report names it |
| Honest numbers | report has passed, failed, skipped, flaky and total above 0 from the last run | compare with the runner's output |
