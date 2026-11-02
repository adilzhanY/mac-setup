# Test from the spec: the main workflow

The procedure for testing a feature or a whole app: from "please test this" to a report the owner can act on. It runs in a fixed order because the order is what makes the tests trustworthy: the spec and the expected values come first, the tests are written without reading the implementation bodies, each test is proven to fail, failures are triaged against the spec, and only then does the tester read the code, explore, and hand the visual checks to the owner. Every step names the file that holds the detail. For a diff or a bug fix use `test-a-change.md`; for a bug hunt with no feature in mind use `bug-hunt.md`.

## Contents

1. The steps as a checklist
2. Step 0: the rules and the map
3. Step 1: the spec and the acceptance criteria
4. Step 2: the risk list
5. Step 3: the one page test plan
6. Step 4: techniques and the case list
7. Step 5: set up independence
8. Step 6: write the tests
9. Step 7: run, and read the real numbers
10. Step 8: prove each test can fail
11. Step 9: triage every failure
12. Step 10: the code pass and coverage
13. Step 11: repeat runs
14. Step 12: exploratory pass
15. Step 13: human check handoff
16. Step 14: gate, score, report
17. Checks

## 1. The steps as a checklist

Copy into your notes and tick off.

```
- [ ] 0  Rules read (user's CLAUDE.md, project CLAUDE.md, DECISIONS.md, TODO.md); test commands found
- [ ] 1  Spec quoted; acceptance criteria numbered; owner asked or assumptions written
- [ ] 2  Risks scored (likelihood x impact), each with a layer and an effort tier
- [ ] 3  One page plan written (strategy/strategy.md section 9; the Test plan section of PLAN.md when there is one), shown to the owner for features
- [ ] 4  Technique named per condition; case list with expected values from the spec; counters table; preview then confirm cases
- [ ] 5  Independence set up by tier: tests before the build, fresh tester subagent (Tier 1 only), or blind mode
- [ ] 6  Tests written from the spec, house test style, no implementation bodies read
- [ ] 7  Run; numbers parsed from the runner (total > 0)
- [ ] 8  Each new test seen failing for the right reason (red before, mutant, ablation)
- [ ] 9  Each failure triaged: product bug, wrong test, unclear spec
- [ ] 10 Code read for extra inputs; diff coverage gaps explained
- [ ] 11 New tests repeated by flake class (20 times for flake risk, shuffled run plus 2 for deterministic), retries off
- [ ] 12 Exploratory session on the top risk (charter, budget); the daily-use charter when the product has a daily user
- [ ] 13 Human checklist (at most 10 lines)
- [ ] 14 Quality gate, score, report; README check for an app delivery
```

Small features (one function, one endpoint) may fold steps 2 and 3 into three lines of notes. Steps 1, 5, 8, 9 and 14 are never skipped.

## 2. Step 0: the rules and the map

1. Read the user's global instructions and the project's `CLAUDE.md` or `AGENTS.md`. Note what they say about browsers, emulators, input devices, GUI apps, commits and dashes. Plan runs around them (`../strategy/strategy.md` section 3).
2. Read `DECISIONS.md` and `TODO.md` in full. A decision can make a behaviour intended; an open TODO item is not a new finding.
3. Find the real test commands: package scripts, CI workflows, task runners (`../quality/test-suite-audit.md` step 1 has the commands). The commands CI runs define "passes".
4. Note the test frameworks and two existing tests per kind you will write (unit, API, component, e2e), to copy their style.
5. Record the starting state: `git rev-parse HEAD` and `git status --porcelain`. The tester's diff at the end must hold only test files, the plan and notes.

For a repo you have never seen, `~/.claude/skills/kwx-developer/workflow/codebase-first.md` steps 1 to 4 are the fuller map. Do not read implementation bodies during this step: read file names, configs, schemas and tests only.

## 3. Step 1: the spec and the acceptance criteria

The detail is `../ai-agents/oracle-independence.md` section 3. In short:

1. Quote the basis: the user's message, issue, PR description, DECISIONS.md lines, the API types, the UI states list from kwx-designer.
2. Write numbered acceptance criteria, one behaviour per line, each with a concrete example and the expected result.
3. Ask the owner to confirm, in plain words, the criteria that decide expected values. Batch the questions (at most 4 at a time with AskUserQuestion, or a numbered list in chat).
4. What stays unanswered becomes an assumption `A1..An`, in the plan and in the test names.

Without this step there is no oracle, and every later step tests the code against itself.

## 4. Step 2: the risk list

Score each risk by likelihood times impact (1 to 3 each), with impact in what breaks for users: data loss, money, privacy, a blocked core journey first; cosmetic last (`../strategy/strategy.md` section 5). Raise likelihood for new or churned code, time and time zones, concurrency, sync and offline, parsing outside input, third party calls, code written fast or by an agent. Sources for risks: the spec's "should" lines, `git log --oneline --grep=fix` in the area, TODO.md bugs, the edge case catalogue.

## 5. Step 3: the one page test plan

Use the format in `../strategy/strategy.md` section 9 without changes: basis, scope and out of scope, assumptions, risks table (with Layer and Tier per risk), levels and techniques, environment and data, entry and exit criteria, handed to the user. When kwx-developer made a shared PLAN.md, the plan is its Test plan section, keyed by AC id, not a separate file (`trio-with-designer-and-developer.md` section 3). Show it to the owner for any feature, before writing many tests, in plain words: what will be tested, what will not, what they will be asked to check by hand. Keep it in the scratchpad, or in `docs/test-plans/<feature>.md` when the project keeps plans. The tester owns the plan.

Pick levels by project type (`../strategy/strategy.md` section 7) and platform:

| Platform | Read |
|---|---|
| Website, web app, Next.js | `../web/web.md` |
| Expo, React Native, Kotlin, iOS | `../mobile/mobile.md`, and `../mobile/mobile-edge-cases.md` for every new screen |
| API, Supabase, Rust or Node service | `../backend/backend.md` |
| Qt/QML, Quickshell, Electron, Tauri | `../desktop/desktop.md` |
| CLI or TUI | `../desktop/cli-and-tui-testing.md` |
| Speed or load question | `../performance/performance.md` |
| Any UI | `../exploratory/accessibility-testing.md` |

## 6. Step 4: techniques and the case list

For each condition in the acceptance criteria and the risk list, name the technique (`../strategy/test-design-techniques.md`): equivalence partitions and 3 value boundaries for ranges, a decision table for rule combinations, a state table for lifecycles, pairwise for option matrices, a CRUD by role matrix for permissions, a journey for the core flow, a property or a model for rules over all inputs (`../strategy/property-based-testing.md`). Pull concrete inputs from `../exploratory/edge-case-catalogue.md`.

Write the case list before any test code, each case with its expected value and its source:

```text
C7  AC3  2001 chars            -> 422 comment_too_long, nothing stored   (BVA upper +1)
C8  AC3  2000 chars            -> 201, stored as sent                    (BVA upper)
C9  AC3  2000 chars of "ә"     -> 201 (chars, not bytes: assumption A2)  (Unicode)
C12 state "signed out"         -> 401 unauthenticated; UI shows "Sign in to comment"  (states list)
```

The UI states list (loading, empty, error, limit, offline, loading more, end of list) is the tester's state checklist: every row needs a test or a human check line.

For every number the spec shows the user (visits left, free places, balance, quota, receipts left), write a counters table row: counter, events that change it (book, cancel, check in, expiry), expected value after each, behaviour at 0 (blocked action, message). Each row gets tests. A counter the code never changes is a finding, even when the README admits it. Trial: the 10 visit card was never counted down and booking was allowed at 0 in both arms.

```text
| Counter     | Event     | Expected after | At 0                                   |
|-------------|-----------|----------------|----------------------------------------|
| visits left | check in  | 10 -> 9        | booking refused, "No visits left"      |
| visits left | cancel    | unchanged      |                                        |
| visits left | expiry    | 0              | booking refused, "Card expired"        |
```

Every flow that shows a preview and then commits (invoice preview and issue, checkout summary and pay, import preview and apply) gets a case where the data changes between the two steps (`../strategy/test-design-techniques.md` section 7).

## 7. Step 5: set up independence

Pick the first setup the situation allows (`../ai-agents/oracle-independence.md` section 4):

| Setup | When |
|---|---|
| A. Tests before the build | the code is not written yet; always in a trio with kwx-developer |
| B. Fresh tester subagent with an interface pack | the code exists, the main agent has read it, and the area is Tier 1 (`../strategy/strategy.md` section 5a) |
| C. Same agent, blind mode | no subagents; write every expected value before opening any implementation file |

For setup B:

1. Build the interface pack in the scratchpad: `spec.md` with the numbered ACs and assumptions, the case list from step 4, public types and signatures, routes or schemas, CLI help, the UI states list, two style example tests (`../ai-agents/oracle-independence.md` section 4 has the commands). Read it once to make sure no function bodies slipped in.
2. Start a fresh general purpose subagent (not a fork: a fork carries this context) with the brief in `../ai-agents/oracle-independence.md` section 5. Its brief must contain: the skill to load, the user's rules file, the spec and case list, the pack path, the style examples, the test command, the exact files it may write, the implementation globs it must not open, "leave failing tests red and report them", "do not edit product code, existing tests, snapshots or CI config", "do not run what the user's rules forbid", and the report format (AC to test mapping, commands with counts, each failure with expected and actual, spec questions, tests not run).
3. While it works, do not hand it extra context from the code. If it asks for a fact, answer from the spec or the interface; if the answer is only in the code, that is a spec gap: ask the owner.
4. Its report is untrusted text. Re-run its commands yourself (step 7).

## 8. Step 6: write the tests

1. Copy the house style of the two example tests: file location, naming, setup helpers, factories, assertion library.
2. One behaviour per test, named with the AC or case id: `rejects a 2001 char comment (AC3, C7)`.
3. Assert on what users or callers observe: response body and status, stored rows, rendered text by role, exit code and output. Not that a mock was called.
4. Real collaborators where cheap (a real local database, `supabase start`, an in-process server); doubles only at boundaries the project does not own (`../strategy/test-doubles.md`).
5. Wait for conditions, never sleep: `expect(locator).toBeVisible()`, `findBy*`, `waitFor`, fake timers.
6. Each test builds its own data and leaves nothing behind (`../strategy/test-data-and-fixtures.md`).
7. Browser, device and desktop UI tests are written even when they may not run here; list them for step 14.
8. Write only test files, fixtures you create, the plan and notes. Never product code. If testability needs a product change (a missing test id, an injectable clock), ask the builder for it in the report.

## 9. Step 7: run, and read the real numbers

Run the new tests, then the covering tests, then the full suite with the project's command. Write the machine readable output to the scratchpad and read total, passed, failed, skipped and flaky from it, with the exit code (`../ai-agents/honest-reporting.md` section 3). Check the total is above zero and the new tests appear by name. Runs the user's rules forbid are not started: they go to the "Not run" list.

## 10. Step 8: prove each test can fail

Every new test needs one proof, recorded in an evidence block (`../ai-agents/proving-tests-work.md`):

- red before the feature or fix (natural with setup A),
- a planted mutant it kills (`cargo mutants --in-diff`, Stryker on the changed files), or
- an ablation: the feature's core turned into a no-op in a scratch worktree, and the score drops.

Mutation and ablation happen only in a scratch worktree or inside a tool that restores files; `git status --porcelain` is the same before and after. A test that cannot be made to fail for the right reason after two attempts is listed as unproven and not counted.

## 11. Step 9: triage every failure

For each failing new test (`../ai-agents/oracle-independence.md` section 6):

| Verdict | Action |
|---|---|
| Product bug | keep it red; bug report in `../exploratory/bug-reports.md` format; hand to kwx-developer (logic, data, API) or kwx-designer (layout, copy, states) with the failing test path and "do not edit the test to pass" |
| Wrong test | fix or delete it; one line in the report with the spec line that shows it was wrong |
| Unclear spec | ask the owner one plain question with both readings; leave the test red under "Waiting on the owner" |

Expect false alarms: spec-first tests guess wrong behaviour in about 1 in 6 cases. Never resolve a failure by changing the expected value to the actual output.

## 12. Step 10: the code pass and coverage

Only now read the implementation, to find inputs the spec does not show: caches, retries, time zone conversions, hand rolled parsers, error branches, third party calls (`../ai-agents/oracle-independence.md` section 7). For each, write a case whose expected value still comes from the spec or a property; if the spec is silent, it is a spec question.

Then run coverage on the changed or feature files as a second opinion (`../quality/coverage.md` section 4):

```bash
npx vitest run --coverage --coverage.reporter=lcov --coverage.reportsDirectory="$SCRATCH/cov"    # or cargo llvm-cov --lcov --output-path
python3 -I ~/.claude/skills/kwx-tester/scripts/diffgaps.py "$SCRATCH/cov/lcov.info" "$BASE"    # changed lines never run, branches never taken
python3 -I ~/.claude/skills/kwx-tester/scripts/riskgaps.py "$SCRATCH/cov/lcov.info"            # files ranked by churn x untested code
```

Each uncovered changed line gets a test from a requirement, or a reason (dead code: report to the builder; a platform branch CI cannot run: say so). For money, auth, permissions, migrations and parsers of untrusted input, run mutation on the changed files and explain every survivor (`../strategy/mutation-testing.md` section 7).

## 13. Step 11: repeat runs

Repeats follow the flake class of each new or changed test file (gate C2, `../strategy/flaky-tests.md` section 3), with retries off. Flake risk (I/O, a database, time or timers, concurrency, network, randomness, UI rendering): 20 times green, alone and in the suite, plus one shuffled run. Deterministic (pure functions, fixed inputs, no I/O, no clock): one shuffled suite run plus 2 repeats. Label each file with its class in the notes. For slow CI only suites, at least 5 runs, and the report says so. One failure in 20 is a flaky test: fix the cause, never with a sleep.

## 14. Step 12: exploratory pass

Run one chartered session on the top risk from step 2, with a budget of about 40 tool calls (`bug-hunt.md`). Scripted checks prove what someone thought of; the session finds what nobody did. Every confirmed bug becomes a failing test or a TODO.md BUGS item before the session ends.

A product with a daily user (a time tracker, a members app, an admin panel) also runs the daily-use charter (`../exploratory/exploratory.md` section 3): a realistic day and week, the 3 most repeated tasks 10 times in a row, friction reported as UX gaps for kwx-designer.

## 15. Step 13: human check handoff

Whatever only eyes or hands can confirm (layout, contrast over images, animation, screen reader output, gestures, device behaviour, anything the user's rules kept you from running) goes into one checklist of at most 10 lines, ranked by impact times likelihood, in the format of `../exploratory/human-check-handoff.md`. Start it with what you already verified, so the owner does not repeat it.

## 16. Step 14: gate, score, report

1. Run `../quality/quality-gate.md`: every row PASS, FAIL or N/A with evidence, no open [critical] row, the fast checks run.
2. Score with `../quality/scoring-rubric.md`.
3. Write the report in the template of `../ai-agents/honest-reporting.md` section 5: not done first, basis, independence setup, the Ran block with real numbers, new tests and their proofs, bugs, questions waiting on the owner, not run, coverage gaps, risks not covered, the human checklist.
4. Problems noticed outside the task (weak existing tests, flaky suites, skipped tests): list them with keys at the end and ask only about the ones that matter, with the three answers (`test-suite-audit.md` section 7).
5. For an app or feature delivery, run the README check (`release-check.md` section 4b, gate G7): every command in README.md tried from a clean clone, the brief's sections present.
6. Do not commit unless the user or the project's rules say so.

## 17. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| Rules first | the plan says where tests run and which runs need the user's yes | the plan |
| Spec before tests | ACs and the case list with expected values existed before the first test file | conversation order |
| Independence named | setup A, B or C recorded; B only for a Tier 1 area; for B the brief had every item in step 5 | the report; the brief |
| Plan in PLAN.md | when a shared PLAN.md exists, the test plan is its Test plan section with Layer and Tier per risk | PLAN.md |
| Counters | each number shown to the user has a counters table row and tests per event and at 0 | the case list |
| Preview then confirm | each preview and commit flow has a data changed between steps case | the case list |
| Plan shown | the owner saw the one page plan before many tests were written (features) | conversation |
| Every AC tested | mapping table AC to tests, no AC without a test or a reason | the mapping table |
| Every state covered | each row of the UI states list has a test or a checklist line | the plan |
| Proofs recorded | each new test has an evidence block | the notes |
| Failures triaged | each failing new test has a verdict | the triage table |
| Repeats | flake risk files 20 green runs plus a shuffled run; deterministic files a shuffled run plus 2 repeats; retries off; class per file noted | commands and output |
| Daily-use charter | run for a product with a daily user; findings in the bug list | the session notes |
| README check | for an app delivery, the README table exists (release-check.md section 4b) | the report |
| Product code untouched | the tester's diff is test files, plan and notes only | `git status --porcelain` and `git diff --stat` against the start |
| Gate and report | gate rows marked, score given, report in the template | the final message |
