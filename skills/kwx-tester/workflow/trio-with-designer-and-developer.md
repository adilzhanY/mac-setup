# Trio with kwx-designer and kwx-developer: one feature, three roles

How the three skills work on one feature that has screens and data. kwx-designer owns the interface, kwx-developer owns data, API and the client layer, kwx-tester owns the proof. The developer and designer already run as a duet (`~/.claude/skills/kwx-developer/workflow/duet-with-kwx-designer.md`); the tester joins at the start, not at the end. The reason is the evidence in `../ai-agents/oracle-independence.md`: tests written from the spec while the code is being built cannot copy its bugs, and checks the builders never saw catch what their own tests miss. This file gives the order of work, who owns which files, the handoff formats, the gates, and what happens when roles disagree.

## Contents

1. Who owns what
2. The order of work
3. The tester's inputs: spec, contract, states list
4. Visible tests and held-out tests
5. Running three subagents
6. The handoffs
7. Disagreements: the owner decides
8. The gates
9. Without subagents
10. Checks

## 1. Who owns what

| Area | Owner | Others |
|---|---|---|
| Spec and acceptance criteria | the main agent writes them with the owner | all three read them; the tester's questions about them go to the owner |
| The contract: states list, API shapes, hook signatures (duet section 2) | main agent; states list from kwx-designer, API shapes and types file from kwx-developer | the tester reads all three parts as its public interface |
| Screens, components, styles, copy | kwx-designer (through the ui-designer agent in this user's setup) | tester reads only what the states list and copy expose |
| Schema, migrations, API, client data layer, shared types | kwx-developer | tester reads the types file, schemas and routes, not handler bodies |
| Unit and contract tests written while building | kwx-developer and kwx-designer, as their own skills say | the tester reviews them (`../quality/review-method.md`) but does not edit them |
| **Acceptance tests from the spec, the held-out set, e2e journeys, the test plan, exploratory notes, bug reports** | **kwx-tester** | the developer and designer read the visible acceptance tests, never edit them |
| Product code | developer and designer | **the tester never edits product code**, not even a one line fix; it hands a bug report |
| Test config, CI test jobs | the tester proposes, the developer applies when it touches build or CI config | owner approves config changes |
| The joint gate and the final report | main agent | each role's gate result is an input |

Rules that follow from the table:

1. **The tester owns the test files it writes and the test plan.** Paths are listed in its brief (for example `tests/acceptance/comments/**`, `e2e/comments.spec.ts`, `flows/comment.yaml`).
2. **The developer never weakens the tester's tests.** If it thinks one is wrong, it flags it with evidence (`~/.claude/skills/kwx-developer/ai-agents/tests-and-honesty.md` section 2) and carries on with the rest. The tester's test files are read only to it, enforced by permissions where the owner allows (`.claude/settings.json` deny rules on the tester's paths, `~/.claude/skills/kwx-developer/ai-agents/tests-and-honesty.md` section 9).
3. **The designer's UI states list is the tester's state checklist.** Every row (loading, empty, list, loading more, end, load failed, posting, too long, signed out, post failed, offline) gets a test or a human check line. kwx-designer's gate requires these states to exist (its gate F1); the tester proves they appear when their trigger happens.
4. **Files are disjoint.** No file is written by two roles. A shared file has one owner named in every brief.

## 2. The order of work

```
main agent : rules and map -> spec and ACs (owner confirms) -> contract parts 1, 2, 3
tester     : test plan (risks, levels, states) -> case list from the spec -> owner sees the plan
             ──────────────────────── parallel ───────────────────────────────────────────────
developer  : types file + hooks with fixtures ("contract ready") -> migration, API, hooks, own tests
designer   : every state against the hook signature and fixtures
tester     : visible acceptance tests (red: nothing built yet) -> held-out set in the scratchpad
             -> e2e and Maestro flows written (run only where the user's rules allow)
             ─────────────────────────────────────────────────────────────────────────────────
developer and designer report done
tester     : run visible tests -> run held-out set -> prove, triage -> attack (bug hunt on top risks)
             -> bugs back in the bug report format -> re-test fixes -> human checklist
main agent : joint gate (developer gate, designer gate, tester gate, J rows) -> one report
```

The tester starts at the same moment as the builders, from the spec and the contract, so its tests exist before the code (setup A in `../ai-agents/oracle-independence.md` section 4). Its first tests are red by construction: that is the fail before proof for free.

## 3. The tester's inputs: spec, contract, states list

The tester's brief contains only what an outside tester could know:

| Input | From | Used for |
|---|---|---|
| PLAN.md sections 1 to 6 and 8 (owner rules, day in the life, ACs, states, API shapes, risks, not in scope), when it exists. Not the designer and developer appended sections, and not the proof column of section 3 | main agent and owner | expected values |
| Contract part 1, the states list | kwx-designer side | state tests, the human checklist |
| Contract part 2, API shapes, error codes, limits (`COMMENT_MAX`) | kwx-developer side | API tests, the authorization matrix, boundaries |
| Contract part 3, hook signatures | main agent | component tests against fixtures, client tests |
| The types file path (once "contract ready") | developer | imports in tests; it compiles against the real shapes |
| Two existing tests per kind, the test commands | the repo | house style |
| The user's rules | CLAUDE.md | which suites the tester may run |

Not in the brief: handler bodies, component bodies, the builders' plans, transcripts, or their tests while they are being written.

The tester appends a Test plan section to PLAN.md keyed by AC id (the one page plan of `../strategy/strategy.md` section 9 lives there, not in a separate file) and asks spec questions only about ACs missing or ambiguous there. It does not re-derive the spec. Test names carry the PLAN.md AC ids.

## 4. Visible tests and held-out tests

The tester splits its tests in two (`../ai-agents/proving-tests-work.md` section 7):

| Set | What | Where during the build | Who sees it |
|---|---|---|---|
| Visible acceptance tests | one or more tests per AC and per state, through the public interface | in the repo, in the tester's paths, read only to the builders | builders run them as their target |
| Held-out set | composition and journey cases (two features together, a full flow, a second user, a retry after failure, a differential run against the old version), plus a few extra boundary cases | in the scratchpad | nobody but the tester until the builders report done |

After the builders report done, the tester runs the held-out set. Failures are triaged like any other (`../ai-agents/oracle-independence.md` section 6). Then the held-out cases are added to the repo as regression tests. A held-out case is never shown to a builder while it is still iterating; a bug report that quotes a held-out test is sent only after the builder has reported done.

## 5. Running three subagents

Extends duet section 4.

1. **Launch the tester with the developer's first step.** The tester can start on the plan and case list from the spec alone; it needs the types file only to compile its tests.
2. **Disjoint paths in every brief.** Developer: `src/api/**`, `src/routes/**`, `migrations/**`, `src/hooks/**`, its unit tests. Designer: `src/screens/**`, `src/components/**`, theme files, component tests. Tester: `tests/acceptance/**`, `e2e/**`, `flows/**`, the plan file.
3. **The tester runs only its own tests and read-only checks** during the parallel phase. It does not run formatters over the repo, install packages, or start long servers on ports the builders use. A shared dev server or live reloading app follows the project's lock rule.
4. **No one commits.** The main agent commits after the joint gate, when the user or the project's rules say so.
5. **Live GUI runs follow the user's rules.** If browsers or emulator input are off, the tester writes e2e and Maestro flows and hands them to CI or the owner (`../ai-agents/gui-agents.md` section 7).

Tester brief (fresh general purpose subagent, never a fork of a context that read the code):

```text
Load the kwx-tester skill (~/.claude/skills/kwx-tester/SKILL.md) and follow
workflow/trio-with-designer-and-developer.md and workflow/test-from-spec.md.
Repo: <path>. User's rules: <paths>. Project map: <paste, without implementation details>.
Feature: <one line>. Spec and ACs: <paste>. Assumptions: <A1..>.
Contract: states list <paste>, API shapes and error codes <paste>, hook signatures <paste>.
Types file (read only, compiles your tests): <path>, ready when the developer reports "contract ready".
Style examples: <two test paths per kind>. Test commands: <list>.
Your files (create or edit only these): <tests/acceptance/comments/**, e2e/comments.spec.ts, flows/comment.yaml>.
Held-out set: write it in <$SCRATCH/heldout/>, not in the repo, until I tell you the builders are done.
Do not open: <src/** except the types file>, the builders' tests, their plans.
Do not edit product code, existing tests, snapshots, CI config. Do not install, do not commit.
Do not run browsers or device flows unless the user's rules allow it; write them and list them.
Report 1 (before the build is done): the plan, the case list, visible tests written, all red, with the run output.
Report 2 (after I say the builders are done): visible and held-out results with runner numbers, proofs,
triage of each failure, bugs in the handoff format, spec questions, not run, the human checklist.
```

## 6. The handoffs

| From | To | Format | When |
|---|---|---|---|
| Tester | owner (through the main agent) | the one page test plan (`../strategy/strategy.md` section 9) and spec questions in plain words | before tests are written in bulk |
| Tester | developer, designer | visible test paths and the AC mapping, as their target | when the visible tests are written |
| Tester | developer or designer | one bug handoff block per bug (`../exploratory/bug-reports.md` section 8): title, severity, reproducibility, oracle, minimal repro, failing test path, "do not edit the test to pass; if you think it is wrong, flag it", done when | after the build, per bug |
| Developer or designer | tester | "fixed B3" with the commit or the files changed and the command they ran | after each fix |
| Tester | main agent | re-test result: the failing test now green, the neighbours green, 20 repeats; or "not fixed" with the new output | after each fix |
| Developer or designer | main agent | a flagged test: test path, what it asserts, why they think it is wrong, evidence | whenever a tester test looks wrong to them |
| Tester | owner | human checklist (`../exploratory/human-check-handoff.md`) | end |

Routing bugs: logic, data, API, security, performance, crashes and missing accessible names in code go to kwx-developer; layout, hierarchy, contrast tokens, target sizes, copy, empty states and motion go to kwx-designer; a missing state that spans both goes to both, with the contract row named.

## 7. Disagreements: the owner decides

The tester's tests encode the spec as the tester read it. A builder may read it differently. Neither side wins by editing last.

| Disagreement | Do |
|---|---|
| A builder thinks a tester's test is wrong | the builder flags it and does not edit it. The tester re-checks it against the spec: if the tester misread the spec, it fixes its own test and says so in one line; if not, the main agent asks the owner |
| The spec allows both readings | the main agent asks the owner one plain question with both readings and what each means for users. The answer goes into the spec (and DECISIONS.md if it is lasting) |
| The tester reports a bug the builder calls intended | the builder points to the spec line or decision; if there is none, the owner decides |
| A fix would need a contract change | the main agent updates the contract (all parts), tells all three roles, the tester updates its tests to the new contract, and the contract test runs again |
| The tester wants a product change for testability (a test id, an injectable clock) | the tester asks in its report; the owner of that file makes it |

The question to the owner, in plain words:

```text
The tester and the builder read the spec differently on one point, and I need your call:
When a signed out user opens a post, should they see the comments (read only) or only "Sign in to comment"?
(a) See comments, cannot post. (b) See nothing until signed in.
The tester's test expects (a); the current build does (b). Nothing changes until you answer.
```

Record the answer in the spec. A lasting rule goes to DECISIONS.md in kwx-developer's format (`~/.claude/skills/kwx-developer/quality/decision-records.md`). The losing side updates its own files: the tester its test, or the builder its code.

## 8. The gates

1. **Each role's own gate:** kwx-developer `quality/quality-gate.md` on non UI files, kwx-designer `quality/quality-gate.md` on UI files, `../quality/quality-gate.md` on the tester's work.
2. **The duet rows J1 to J9** (kwx-developer duet section 7), run by the main agent.
3. **Trio rows**, run by the main agent on the combined result:

| # | Check | Pass condition | How to verify |
|---|---|---|---|
| T1 [critical] | Tester's tests untouched by builders | no builder edited, skipped or deleted a file in the tester's paths | `git diff --name-only` against the tester's path list, by role |
| T2 [critical] | Every AC and state tested | each AC and each states list row has a passing test or a human check line | the tester's mapping table |
| T3 [critical] | Held-out set ran last | the held-out set ran after the builders reported done, results in the report | the tester's report 2 |
| T4 | Every bug closed or open on purpose | each bug is fixed and re-tested, or left open with the owner's say | bug list with statuses |
| T5 | Flagged tests resolved | each test a builder flagged has a decision (tester fixed its own misread, or the owner chose) | conversation |
| T6 | Product code only from builders | the tester's diff holds no product file | `git diff --name-only` for the tester's run |

4. **One report:** the three gate summaries, the J and T rows, the tester's runner numbers, one "Not run" list, one human checklist.

## 9. Without subagents

One agent can play all three roles in order, but independence then depends on order alone: spec and contract first; then the tester's plan, case list and visible tests, written before any implementation file is opened; then the builder steps (data, API, hooks, screens); then the tester's run, held-out set, proof, triage and bug hunt. Say in the report that the tests were written in the same context before the build (setup C in `../ai-agents/oracle-independence.md` section 4). Load each skill's files only for its own step.

## 10. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| Tester started at the start | the plan and case list existed before the builders reported "contract ready" or soon after | conversation order |
| Inputs clean | the tester's brief held spec, contract and types file only; from PLAN.md only sections 1 to 6 and 8, without the designer and developer appended sections and the proof column of section 3 | read the brief |
| One plan | when PLAN.md exists, the test plan is its Test plan section keyed by AC id; no separate plan file and no second spec | `ls docs/test-plans` is empty for this feature; PLAN.md |
| Ownership written | every brief lists its files and the shared file owners | read the briefs |
| Tests before code | the visible tests' first run was red because the feature did not exist yet | report 1 output |
| Held-out kept back | held-out cases stayed in the scratchpad until the builders were done | file paths and timing |
| Bugs in format | each bug went to the right owner in the handoff block | the reports |
| Disagreements to the owner | no test or spec dispute resolved by whoever edited last | conversation |
| Trio rows pass | T1 to T6 marked, no open [critical] | the final report |
