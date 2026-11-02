# Test suite audit: find what is wrong with the tests, then let the owner decide

The procedure for auditing a project's existing tests and for what happens with each finding. The audit itself (finding the commands, running and timing the suite, skips, smells, real network, flaky history, coverage gaps by churn and risk, a mutation sample, missing levels, CI, fixes without tests) is in `../quality/test-suite-audit.md`; run it step by step. This file wraps it in the same ask and record protocol as kwx-developer: for every finding the owner gets one plain question with exactly three answers (Later to TODO.md, Plan a fix, Keep as is to DECISIONS.md), the answer is recorded where the next session reads it, nothing is fixed before the owner says so, and nothing decided is ever asked again. The protocol's full wording is `~/.claude/skills/kwx-developer/workflow/audit-and-ask.md`; this file pins the parts that must match and adds what is specific to tests.

## Contents

1. Two triggers, two modes
2. Rules for both modes
3. Mode A: the full audit, step by step
4. Test finding kinds and keys
5. Ranking and the summary table
6. The question and the three answers
7. Mode B: test problems noticed during another task
8. After Later: the TODO.md item
9. After Plan a fix: the plan
10. After Keep as is: the DECISIONS.md entry
11. Never re-ask, never fix unasked
12. Checks

## 1. Two triggers, two modes

| Trigger | Mode | What the tester does |
|---|---|---|
| The user asks: "audit the tests", "is this tested enough", "why is CI flaky", "review our test suite", "what tests are missing" | A, full audit | runs section 3, shows the ranked summary, asks about each finding, records every answer |
| The tester notices a test problem while doing something else (testing a feature, a change, a bug hunt) | B, noticed in passing | finishes the task first, then lists what it noticed and asks only about the findings that matter (section 7) |

A request to fix one named problem ("the checkout test is flaky, fix it") is not an audit: the owner has already chosen Plan a fix. Write the plan (section 9), show it, and go on after the go.

## 2. Rules for both modes

1. **Rules and records first.** Read the user's CLAUDE.md and the project's; read DECISIONS.md and TODO.md in full. Build the do-not-flag list (Accepted decisions with an `Audit:` key) and the open TODO keys with the commands in `~/.claude/skills/kwx-developer/workflow/audit-and-ask.md` section 3.
2. **The audit changes nothing in the repo.** No test fixed, no config edited, no package installed. Reports, coverage and mutation output go to the scratchpad. `git status --porcelain` is the same before and after (`../quality/test-suite-audit.md` rule 2).
3. **The user's rules decide what runs.** Suites that need a browser, an emulator with input, or a GUI the rules forbid are audited by reading and listed as "not run, needs the owner's yes".
4. **A lead is not a finding.** A smell scan hit, a grep match or a coverage number becomes a finding only after you open the test, read it, and confirm it.
5. **Measure, do not guess.** Times, counts and flaky history come from real runs and CI data.
6. **One finding per pattern per area,** each with a `kind:area` key (section 4).
7. **The tester never edits product code,** not even after a Plan a fix answer. A fix that needs product changes goes to kwx-developer as a plan item.

## 3. Mode A: the full audit, step by step

Copy and tick.

```
- [ ] 1  Rules, DECISIONS.md, TODO.md read; do-not-flag list and open TODO keys built; git status noted
- [ ] 2  Run quality/test-suite-audit.md section 2 checklist, steps 1 to 12, in order
- [ ] 3  Fast checks: smellscan.py, riskgaps.py, grep for focus and skip markers and sleeps
- [ ] 4  Confirm every lead by reading it; drop false positives silently
- [ ] 5  Key each finding (section 4), filter against DECISIONS.md and TODO.md
- [ ] 6  Rank P1, P2, P3 and size S, M, L (section 5)
- [ ] 7  Show the summary table in chat
- [ ] 8  Ask (section 6), record each answer at once (sections 8 to 10)
- [ ] 9  Report (quality/test-suite-audit.md section 6), git status unchanged
```

Fast checks for step 3 (usage from each script's `--help`):

```bash
python3 -I ~/.claude/skills/kwx-tester/scripts/smellscan.py tests src      # also opens Rust files with an inline #[cfg(test)] module
python3 -I ~/.claude/skills/kwx-tester/scripts/riskgaps.py "$SCRATCH/cov/lcov.info"   # lcov from quality/test-suite-audit.md step 8
rg -n '\b(it|test|describe)\.(only|skip|todo)\(|\b(xit|xdescribe|xtest)\(|#\[ignore|@pytest\.mark\.(skip|xfail)|@Disabled|@Ignore' -g '!node_modules'
rg -n 'waitForTimeout\(|setTimeout\(.*resolve|thread::sleep|time\.sleep\(|Thread\.sleep\(|delay\(' -g '*test*' -g '*spec*' -g '!node_modules'
```

Time box: 20 to 40 minutes of tool time for a mid size repo; mutation limited to one module and 30 minutes. If the owner named a folder or a concern, audit only that and say what was left out.

## 4. Test finding kinds and keys

Every finding gets a key `kind:area`, the same way kwx-developer keys its findings, so TODO.md and DECISIONS.md can be matched later with `grep -F`. The tester uses kwx-developer's `untested-risk` kind (from `~/.claude/skills/kwx-developer/quality/codebase-audit-tools.md` section 10) and adds these:

| kind | What it means | Example key |
|---|---|---|
| `test-smell` | tests that lie or break for the wrong reason: no assertion, empty, liar, swallowed exception, over-mocking, sleepy, mystery guest, snapshot rot (`../quality/test-smells.md`) | `test-smell:liar-src/api`, `test-smell:sleepy-e2e` |
| `skipped-test` | skipped, focused, todo or conditionally disabled tests, with their age | `skipped-test:ifc-openshell` |
| `flaky` | passes and fails on the same commit, or retries hide failures | `flaky:checkout.spec.ts/applies-coupon` |
| `missing-level` | a level the project type needs is absent: no API tests, no RLS tests, no e2e for the core journey, no migration test | `missing-level:rls`, `missing-level:e2e` |
| `weak-assertions` | tests run the code but miss faults: surviving mutant clusters, coverage high and mutation low | `weak-assertions:src/billing/invoice.ts` |
| `ci-tests` | CI does not run what people think, main is red, retries hide flakes, artifacts missing | `ci-tests:e2e-not-in-ci`, `ci-tests:main-red` |
| `slow-suite` | the suite or a level is too slow for its place in the loop | `slow-suite:app-test` |
| `fix-without-test` | bug fixes merged without a regression test | `fix-without-test:last-12-months` |
| `untested-risk` | a churned file on a money, auth, data or sync path with untested code | `untested-risk:src/sync/useSync.ts` |

Areas are the folder, file or test name the finding is about. One key per pattern per area.

Filter before ranking, exactly as `~/.claude/skills/kwx-developer/workflow/audit-and-ask.md` section 3 says: drop a finding whose key matches an Accepted decision and whose path is inside its Scope; report one outside the Scope naming the related decision; never ask about a key already open in TODO.md, add a dated "Seen again in audit" line to that item instead.

## 5. Ranking and the summary table

Priorities follow `../quality/test-suite-audit.md` section 4 (P1: suite red on main, tests that cannot fail on money, data, auth or permission code, a focused test committed, a suite believed to run in CI that does not; P2: flaky, sleepy, real network in unit tests, old or unexplained skips, a missing level for a core flow, surviving mutant clusters on risky code, fixes without tests; P3: style smells, slow but stable, snapshot hygiene on internal output). Effort S, M or L.

Before any question, show the whole ranked list as plain chat text, in the format of `../quality/test-suite-audit.md` section 5, with a first line saying what ran and what did not (and why).

## 6. The question and the three answers

One question per P1 and P2 finding, never one question for unrelated findings. At most 4 questions per AskUserQuestion call, at most 12 per sitting; the rest go to TODO.md under `### Not yet reviewed`. All P3 findings go into one bundled question (`~/.claude/skills/kwx-developer/workflow/audit-and-ask.md` section 6, second example). Record each answer before sending the next call.

Each question says, in plain words: what was found (real numbers, one example path), why it matters for users or for the owner's next change, the effort, and the three answers with the recommended one first. Translate test words: "assertion" is "the check at the end of a test"; "flaky" is "passes or fails at random on the same code"; "mutant" is "a small bug I planted on purpose that no test noticed"; "skipped" is "switched off, so it never runs"; "mock" is "a fake stand-in for the real thing".

The labels and descriptions are pinned. Keep them word for word, identical to kwx-developer's, so the owner learns one set of buttons for both skills:

| Answer | Label | Description |
|---|---|---|
| (a) later | `Later` | It is a real problem, but not now. I write it in TODO.md so it is not lost. Nothing in the code changes. |
| (b) plan | `Plan a fix` | I write a short step by step plan and show it to you. I change code only after you say go. |
| (c) keep | `Keep as is` | It is on purpose: this is how the project is meant to be. I record it in DECISIONS.md and never ask about it again. |

Put the recommended answer first and add ` (Recommended)` to its label; the other two follow in a, b, c order. The `header` is at most 12 characters. Recommend Plan a fix for anything on money, data or auth paths and for tests that cannot fail; Keep as is when a whole folder is untested by choice (3D scene components checked by eye, a prototype folder); Later for small issues in quiet code. If TODO.md or DECISIONS.md does not exist yet, add to that option's description: "TODO.md does not exist yet; I will create it at the project root."

Example:

```json
{
  "questions": [{
    "header": "Coupon test",
    "question": "The test that checks coupons at checkout passed and failed at random on the same code in 7 of the last 100 CI runs. Each time it fails, CI goes red for a reason that is not a real bug, and a real coupon bug could hide behind it. Finding the cause and fixing the test takes about an hour and changes no app behaviour. What should I do?",
    "multiSelect": false,
    "options": [
      {"label": "Plan a fix (Recommended)", "description": "I write a short step by step plan and show it to you. I change code only after you say go."},
      {"label": "Later", "description": "It is a real problem, but not now. I write it in TODO.md so it is not lost. Nothing in the code changes."},
      {"label": "Keep as is", "description": "It is on purpose: this is how the project is meant to be. I record it in DECISIONS.md and never ask about it again."}
    ]
  }]
}
```

When the owner is a developer, put the evidence (file:line, the command and its output, the CI run ids) in chat text right before the question; never replace the plain words with it. Without the AskUserQuestion tool, ask in chat with the same text and `1) Plan a fix (recommended)  2) Later  3) Keep as is`, and wait.

Other answers, skips and silence: handle them as `~/.claude/skills/kwx-developer/workflow/audit-and-ask.md` section 10 says (a typed answer mapped to a, b or c and confirmed; a skipped question is not recorded and comes back next time; "stop asking" writes the rest under `### Not yet reviewed`).

## 7. Mode B: test problems noticed during another task

The task comes first.

1. While working, note candidates seen in files you already opened for the task: `path:line, kind, what`. Do not open extra files or run audit tools to chase them.
2. Do not fix them, even a one line `.only` or a sleep, unless the task cannot be done correctly without it (then it is part of the task, and the report says so). Never edit an existing test to make your new tests or the build pass.
3. Stop mid task only when a finding makes the task's results untrustworthy: the suite cannot run, main is red for a reason that hides your results, a test you depend on is switched off. Ask one question with the evidence, then wait.
4. At the end, after the task report: confirm each candidate by reading it again, drop anything on the do-not-flag list or in an open TODO item, rank, and ask with AskUserQuestion only about every P1 and the P2 findings in the area you tested, at most 4 in one call, with the three answers of section 6.
5. List the rest in a short "Also noticed" block, one line each with its key, and offer once: "Say 'audit' and I will go through these with you, or I can write them all to TODO.md."

```text
Done: comments feature tested, 12 new tests, 1 bug handed to kwx-developer. Ran: <commands and numbers>. Not run: <list>.

Noticed while testing (not changed):
1. [P2] tests/api/likes.test.ts:12 waits a fixed 2 seconds instead of waiting for the result; it adds 2 s to every run and fails on a slow machine. (test-smell:sleepy-tests/api)
2. [P3] 3 tests in tests/share.test.ts have been switched off since March with no reason. (skipped-test:share)
I have one question about item 1 (below). Say 'audit' to go through item 2, or I can add it to TODO.md.
```

## 8. After Later: the TODO.md item

Follow `~/.claude/skills/kwx-developer/workflow/audit-and-ask.md` section 7 and the format rules of `~/.claude/skills/kwx-developer/quality/tech-debt-and-todo.md` section 5: read the whole TODO.md first, match its heading, id, checkbox and wrap style, check for a duplicate (`grep -nF 'flaky:checkout.spec.ts' TODO.md`), and append a "Seen again" line instead of a second item. Default shape, under `## Test audit YYYY-MM-DD` (mode A) or `## Noticed YYYY-MM-DD` (mode B), subsections `### P1`, `### P2`, `### P3`:

```markdown
- [ ] **T4. Coupon checkout test fails at random** `flaky:checkout.spec.ts/applies-coupon`
      `e2e/checkout.spec.ts:58` failed then passed on the same commit in 7 of the last 100 CI runs (run ids in the audit notes). Retries hide it.
      Impact: CI red without a real bug; a real coupon bug can hide behind it. Effort: M (about an hour).
```

Bugs in the product (not in the tests) found during the audit go to the `## Bugs` section in the format of `../exploratory/bug-reports.md` section 9, not to the audit section. Then say in one line: "Added T4 to TODO.md." Nothing else changes.

## 9. After Plan a fix: the plan

Write the plan as sub items under the TODO item (create the item first), as `~/.claude/skills/kwx-developer/workflow/audit-and-ask.md` section 8 does, and show it in plain words before any change. Test specific plan rules:

1. **Who changes what.** Test files, test config and the test plan are the tester's. Product code changes (an injectable clock, a missing test id, a real bug the audit exposed) are steps for kwx-developer or kwx-designer, named as such.
2. **A fix to a test keeps or raises what it checks.** Never "fix" a flaky or failing test by loosening its assertion, adding a retry, adding a sleep, or skipping it. A flaky test fix names the cause (`../strategy/flaky-tests.md` section 6).
3. **Prove the fixed test still fails for the right reason** (`../ai-agents/proving-tests-work.md`) and passes 20 times with retries off.
4. **A guard where one exists:** a lint rule for `.only` and sleeps (`eslint-plugin-playwright`, `vitest/no-focused-tests`), a CI cap on quarantined tests (`../quality/ci-testing.md` section 5), added only after the owner agrees to it.
5. **A verify line** with the exact commands and the expected counts.

```markdown
- [ ] **T4. Coupon checkout test fails at random** `flaky:checkout.spec.ts/applies-coupon`
  - [ ] Reproduce: `npx playwright test e2e/checkout.spec.ts -g "applies coupon" --repeat-each=50 --retries=0` in CI (browsers are off locally); record the fail ratio.
  - [ ] Cause from the trace: the test clicks Apply before the price request returns (async wait).
  - [ ] Replace `waitForTimeout(500)` with `await expect(page.getByTestId('total')).toHaveText('€45.00')`. Test file only.
  - [ ] Add `playwright/no-wait-for-timeout` to the e2e lint config (the repo already runs eslint-plugin-playwright).
  - [ ] Verify: 50 runs with retries off, 0 failures; the test still fails when the coupon code is wrong.
```

On go: do the tester's steps, hand product steps to their owner, tick each sub item, end with `Done: YYYY-MM-DD, <what changed>, <the verify result>`.

## 10. After Keep as is: the DECISIONS.md entry

Follow `~/.claude/skills/kwx-developer/workflow/audit-and-ask.md` section 9 and `~/.claude/skills/kwx-developer/quality/decision-records.md` section 7: match the file's style, Scope exactly what the owner said, the owner's reason in their words (or "Owner's call, no reason given"), never an invented reason. Test example:

```markdown
## D-11 3D scene components are checked by eye, not by unit tests

2026-10-31. **Accepted.**
Audit: missing-level:src/scene
Scope: `src/scene/**`
Keep: no unit or component tests for Three.js scene components; the owner checks them by eye after changes.
Why: the visual output is what matters and is hard to assert; logic lives in src/geometry, which is tested.
Revisit when: a scene bug reaches a user twice.
Enforced by: nothing, reviewed by hand.
```

If the owner keeps something that is a real risk (a test that cannot fail on the payment path, RLS with no tests), say the risk once in one plain sentence before recording, and record it under Why.

## 11. Never re-ask, never fix unasked

- Before any question, match the key and path against the do-not-flag list and the open TODO keys. A match is never asked again, in any mode or later session. The only exceptions: a skipped question comes back, and a decision's `Revisit when:` trigger that has happened is asked once, quoting the entry.
- No edit to tests, test config, CI or lint rules for a finding before a Plan a fix answer and the owner's go on the plan.
- In mode B the tester's diff holds only the task's test files, plan and notes.
- Recording an answer in TODO.md or DECISIONS.md needs no further go: the answer was the permission. Commit them only when the project's rules say to commit.

## 12. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| Records first | do-not-flag list and open TODO keys built before the first finding | audit notes |
| Repo unchanged | `git status --porcelain` identical before and after the audit (except TODO.md and DECISIONS.md answers) | run it twice |
| Rules respected | suites the rules forbid were read, not run, and listed | the report's Not run line |
| Leads confirmed | each finding cites a test file:line that was opened | the findings |
| Keys | every finding has a `kind:area` key from section 4 | the findings |
| No re-asked decision | no question matches an Accepted key in scope or an open TODO key | compare with the filter output |
| Pinned answers | every question uses the three labels and descriptions of section 6 word for word, recommended first | read the AskUserQuestion calls |
| Batching | at most 4 questions per call, 12 per sitting, P3 bundled | count the calls |
| Every answer recorded | each Later has a TODO item, each Plan a fix a plan under its item, each Keep as is a D entry | `git diff -- TODO.md DECISIONS.md` |
| No unasked fix | no test, config or CI edit without a go on a plan | `git diff --stat` |
| Task not derailed | in mode B the task finished before any non-blocking question | conversation order |
