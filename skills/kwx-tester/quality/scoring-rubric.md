# Scoring rubric for test suites and test changes

Score every finished piece of testing work from 0 to 5 on each dimension below, after running `quality-gate.md`. It works for a test change (the tests for one feature or fix) and for a whole suite at the end of an audit. A score is a judgement backed by evidence: one line per dimension saying why it earned that level. Dimensions that do not apply are N/A, with the reason, and leave the average. The shape mirrors kwx-developer's rubric (`~/.claude/skills/kwx-developer/quality/scoring-rubric.md`) so scores from the three skills read the same way.

## Contents

1. Minimum to ship
2. Dimensions and levels
3. How to score
4. Example
5. Checks

## 1. Minimum to ship

- **Hard fails** (ship is blocked whatever the scores): any [critical] gate row open; a number reported that no run produced; an existing test weakened, skipped or deleted to get green; an expected value fitted to current output on a main path; product code edited by the tester; a rule of the user broken (a browser, device input or GUI run they forbid, an em or en dash).
- **Oracle independence, Fault detection, Honesty of the report**: at least 4 each.
- **Every other dimension**: at least 3.
- **Average** over the dimensions that apply: at least 4.0.

A 3 is "the tests check the spec and would catch the obvious breaks". A 4 is "a strong QA engineer would sign off without comments". A 5 is "a reference suite would use it as the example".

## 2. Dimensions and levels

### Oracle independence

| Level | Looks like |
|---|---|
| 0 | Expected values copied from current output; tests assert what the code does |
| 1 | Some ACs used, but key assertions are literals from running the code, unlabelled |
| 2 | Expected values mostly from the spec, but the tests were written after reading the implementation, same context, with no blind step |
| 3 | Every expected value traces to an AC, an assumption or a property; the case list was written before the code was read |
| 4 | Tests written before the build or by a fresh tester with an interface pack; failures triaged against the spec; characterization tests labelled |
| 5 | As 4, plus oracles that need no expected literal where they fit (properties, round trips, differential runs against a reference), and spec gaps resolved with the owner |

### Fault detection

| Level | Looks like |
|---|---|
| 0 | Tests cannot fail: no assertions, liars, the unit under test mocked |
| 1 | Tests run the code but assert little; the obvious mutant survives |
| 2 | Main path assertions are real, but no new test was seen failing; error paths unchecked |
| 3 | Every new test seen failing for the right reason (red before the fix, a killed mutant, or an ablation) |
| 4 | Mutation on the changed high risk lines with every survivor killed or explained; the whole deliverable ablated and the score dropped |
| 5 | Held-out composition checks and differential or property tests catch what the visible suite cannot, proven by planted faults |

### Risk coverage

| Level | Looks like |
|---|---|
| 0 | No idea which risks matter; tests where it was easy |
| 1 | Happy path only |
| 2 | ACs covered, but no risk register; a score 6+ risk untested |
| 3 | Risk register with scores; every score 6+ risk has a test that fails when it happens |
| 4 | The right level for each risk (lowest level that catches it plus one journey); accepted risks written down with the owner |
| 5 | Escaped bugs fed back into the register; every risk class from the plan (security, performance, i18n, accessibility) routed and checked |

### States and edge cases

| Level | Looks like |
|---|---|
| 0 | Only the success state |
| 1 | Success and one error |
| 2 | Most UI states, but empty, offline or limit missing; no edge inputs |
| 3 | Every row of the states list and every error code has a test or a human check line; the edge cases that apply from the catalogue are tested |
| 4 | Boundaries with 3 values, Unicode and Kazakh text, time zones and DST, double submit and concurrency where they apply |
| 5 | Stateful parts covered by a model based or property test; interruptions (process death, offline mid save) tested |

### Determinism

| Level | Looks like |
|---|---|
| 0 | Tests fail at random; fixed sleeps; shared state between tests |
| 1 | Mostly stable, but retries are on and flaky passes are counted as passes |
| 2 | No sleeps, but order dependence or real clock and network untested |
| 3 | New tests repeated by flake class (20 times for flake risk, a shuffled run plus 2 for deterministic), retries off; each test builds its own data |
| 4 | Clock, randomness and network controlled at the boundary; seeds printed; parallel safe |
| 5 | Flaky detection in CI with quarantine owners and dates; zero unexplained flakes in recent history |

### Design and readability

| Level | Looks like |
|---|---|
| 0 | Tests nobody can read: one giant test, mystery guests, magic numbers |
| 1 | Assertion roulette, eager tests, copy pasted setup |
| 2 | Readable, but names do not say the behaviour; failures need a debugger |
| 3 | One behaviour per test, named with the AC or case id; failure messages say what broke; house test style |
| 4 | Builders and factories, no general fixture; the right level (unit, integration, e2e) for each case; doubles only at boundaries |
| 5 | The suite reads as the spec; a new teammate learns the behaviour from it |

### Speed and fit in the loop

| Level | Looks like |
|---|---|
| 0 | The suite is too slow or too heavy to run; people skip it |
| 1 | Slow tests at the bottom of the loop (e2e for what a unit test could catch) |
| 2 | Fast enough locally, but CI runs the wrong set or none |
| 3 | Fast tests on every change, slower ones in CI, all known to run somewhere |
| 4 | Affected tests first, sharded where large; slow tests justified by the risk they cover |
| 5 | Feedback in seconds for the changed area, the full gate within the team's budget, measured |

### Honesty of the report

| Level | Looks like |
|---|---|
| 0 | Claims runs that did not happen, or hides a failure |
| 1 | "All tests pass" with no commands or counts |
| 2 | Commands listed, but counts incomplete (no skipped or flaky), or numbers from an old run |
| 3 | Fresh runner numbers (total, passed, failed, skipped, flaky) with commands and exit codes; not run list with reasons |
| 4 | New tests separated with their proofs; skips explained; pre-existing failures proven on the base; a short, ranked human checklist |
| 5 | A reader could reproduce every number and every bug from the report alone |

## 3. How to score

1. Run the gate first; scores without gate evidence are guesses.
2. For each dimension, pick the highest level whose description is fully true.
3. Write one line of evidence per dimension: a test name, a command result, a mutation score, the mapping table.
4. Compute the average over the dimensions that apply.
5. Compare with section 1. Below the minimum: fix, rerun the gate, score again. Never raise a score without new tests, new runs or new evidence.

For a whole suite at the end of an audit, score the suite as it is, and say which findings would raise which dimension. The audit itself changes nothing (`../workflow/test-suite-audit.md`).

## 4. Example

```text
Score: comments feature tests
Oracle 4 (written before the build from AC1..AC9 and the contract; 2 failures triaged: 1 bug, 1 wrong test)
Fault detection 4 (9 red before the build, 2 killed mutants, ablation of postComment turned 6 of 9 red; Stryker on routes/comments.ts 88%, 2 equivalent survivors explained)
Risk 4 (RLS read by another user: pgTAP, seen failing with the policy dropped; spam rate limit accepted by the owner)
States 3 (11 of 11 states: 8 tested, 3 on the checklist; no offline mid post test)
Determinism 4 (20/20 repeats, shuffled; clock faked at the boundary)
Design 4 (one behaviour per test, AC ids in names, comment factory)
Speed 3 (unit and API tests 4 s; e2e in CI only)
Honesty 4 (fresh JSON counts, 3 skips explained, e2e listed as not run with the CI job)
Average 3.75 -> below 4.0: add the offline mid post test (States), then rescore.
```

## 5. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| Gate before score | the gate report exists for the same work | read the report |
| Evidence per dimension | each score has one line of evidence | read the score block |
| N/A justified | each N/A names why it does not apply | read the score block |
| Minimum applied | hard fails, the three floors at 4, the others at 3 and the 4.0 average all checked | compare with section 1 |
