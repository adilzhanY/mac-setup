# Oracle independence: expected values come from the spec, never from the code

An oracle is whatever decides that a test's result is right or wrong. This file is about where the tester's oracle comes from. The rule is simple and the evidence behind it is the strongest in this skill: expected values come from the spec, the issue, the acceptance criteria, a property or a reference version, and they are chosen by a context that has not read the implementation body. Tests written next to the code assert what the code does, bugs included. This file says what the tester may and may not see, how to run an independent tester in Claude Code, and what to do when its tests fail. The kinds of oracles themselves (invariants, metamorphic relations, differential runs, golden files) are in `../strategy/test-oracles.md`.

## Contents

1. Why the code must stay out of the tester's context
2. The information policy: who sees what
3. Getting a spec when there is none
4. Running an independent tester in Claude Code
5. The tester subagent brief
6. Failing tests are candidate bugs: triage
7. The second pass: reading the code for inputs, not for answers
8. Characterization tests: the one honest exception
9. Checks

## 1. Why the code must stay out of the tester's context

| Finding | Number | Evidence |
|---|---|---|
| Buggy code in the prompt makes models write tests that assert the bug | 137.69 misguided against 104.15 effective tests per model; with correct code 16.46 against 304.08 (Zhao et al., ISSTA 2026, 11 models, 233 Defects4J bugs) | strong |
| A spec next to the code does not help; the code must be removed | docstring only: 113.00 misguided, 186.77 effective; docstring plus buggy code: 146.08 and 121.92, no better than code alone | strong |
| A fresh session testing from the task description beats the same model testing right after it wrote the code | fault detection about 25% against about 14%, every model, all significant (Konstantinou, Tambon, Papadakis 2026). Test count and coverage did not explain the gap; oracle quality did | strong |
| A separate test designer that sees the signature but not the body | test accuracy 61.0% to 87.8% (HumanEval), 51.8% to 89.9% (MBPP) (AgentCoder) | strong, function level |
| Models recognising a correct assertion get worse when the code is buggy | 92.5% to 65.4% (GPT-5-mini, 24 Java repos) | strong |
| Generators that keep only passing tests validate the bug | CoverUp and CoverAgent reject bug revealing tests (Mathews and Nagappan) | strong |
| Chain of thought and self-verification prompts do not fix it | chain of thought did 9.8% to 25.8% worse than a plain prompt | strong |

The main problem is the shared context, not the shared model. A fresh context with the same model wins. All of this evidence is at function level; no study yet ablates code visibility for a tester on a whole repository, so treat the size of the effect as unknown at that scale and the direction as settled.

### Trial evidence

Kwx trial 2026-11-01: spec-first independent testers scored higher on tests in all three apps (9/7, 8/6, 8/6). They caught 37 of 38 and 12 of 12 non-equivalent planted faults, and found real bugs before release (raw zod messages from validateWaitlist, a NaN thrown into BigInt). The no-skills arm encoded its own 0,01 h rounding into its expected values and shipped invoices that disagree with its own overview. When cutting cost, do not trim setups A, B and C or the rule that expected values come from the spec; trim repeats and per test proofs instead (`../strategy/strategy.md` section 5a).

The price: spec-first tests hallucinate behaviour in 16 to 18% of cases, and a docstring the model wrote from buggy code still kept the bug 15 to 21% of the time. So the spec should come from the owner or the issue, not from the code, and failing tests need triage (section 6).

## 2. The information policy: who sees what

| Party | Sees | Never sees | Allowed outcome |
|---|---|---|---|
| Tester writing oracles | the spec or issue, the acceptance criteria, the public interface (signatures, types, routes, schemas, docs, usage examples, the UI states list), the test framework config and existing tests for style | the new implementation body, the diff, the coder's plan, its transcript and its own tests | failing tests left red, each tied to a spec clause |
| Coder (kwx-developer, kwx-designer) | the tester's visible acceptance tests, read only by permission | the held-out tests | implement, or stop and flag a spec conflict |
| Later reviewer (optional) | the code plus the spec, to hunt for tricky inputs | the coder's reasoning | findings checked against the spec, not the code |

Source: the report's information policy table, built from ImpossibleBench (read-only tests kept honest performance; hidden tests cost it), SpecBench (held-out gaps) and the fresh session results. Evidence: strong for the parts, opinion for the exact split.

What counts as the public interface, per stack:

| Stack | Public interface the tester may read |
|---|---|
| TypeScript | exported types and signatures (`.d.ts` output, or the types file of the contract), route list, zod schemas, the hook signatures from the contract |
| Rust | `pub` items and doc comments (`cargo doc` output, or signature lines only), CLI `--help` text |
| HTTP API | OpenAPI or JSON schema, route table, error codes and their status, example requests |
| Database | migration DDL (tables, constraints, RLS policies are part of the spec of what is allowed), seed data |
| UI | the states list, copy for each state, accessible names and roles from the design |
| CLI or TUI | `--help`, man page, README usage, key bindings list |

Function bodies, private helpers, the diff and the coder's tests are not on that list.

## 3. Getting a spec when there is none

No spec means no oracle. Do not invent one from the code.

1. Collect what exists: the user's message, the issue, the PR description, README usage, DECISIONS.md lines, the UI states list, the API types. Quote them.
2. Write the acceptance criteria as a short numbered list in plain words, one behaviour per line, each with a concrete example: "AC3: a 2001 character comment is rejected with the message 'Too long (2000 max)' and nothing is saved."
3. Ask the owner to confirm, in plain words, with the questions that decide expected values:

```text
Before I write the tests I need to know what "right" looks like. Please confirm or correct:
1. A comment can be at most 2000 characters, and a longer one is refused with a message. Right?
2. A signed out user sees "Sign in to comment" and cannot post. Right?
3. When two people post at the same second, both comments appear, newest first. Right?
If you are not sure about one, say so and I will write it down as an assumption.
```

4. If the owner cannot answer now, go on with assumptions: write each one in the plan (`A1: ...`) and in the test name (`rejects comments over 2000 chars (assumption A1)`), so changing it later is one search away (`../strategy/strategy.md` rule 3).
5. Behaviour no one can state yet is a spec gap. Report it as an issue, not as a bug.

## 4. Running an independent tester in Claude Code

Three setups, best first. Pick the first one the situation allows.

| Setup | When | How independence is kept |
|---|---|---|
| **A. Tests before the build** | a new feature, a trio with kwx-developer (`../workflow/trio-with-designer-and-developer.md`) | the implementation does not exist yet. The tester writes tests from the spec and the contract while the builder builds. Independence is free |
| **B. A fresh tester subagent with an interface pack** | the code already exists; the main agent has read it; and the area is Tier 1 (`../strategy/strategy.md` section 5a). Outside Tier 1 use A or C | the main agent prepares an interface pack in the scratchpad and starts a new subagent (it inherits none of the main conversation) with the brief in section 5. The subagent reads the pack and the test folders only |
| **C. The same agent, blind mode** | no subagents available | the agent writes the acceptance list and every expected value before opening any implementation file, commits them to the plan, and only then writes tests. Weakest setup: say in the report that tests were written in the same context |

Never use a forked copy of a context that read the implementation as "the independent tester": a fork carries the whole conversation with it. Use a fresh agent.

### Building the interface pack (setup B)

Put it in the scratchpad, not in the repo.

```bash
PACK="$SCRATCH/iface"; mkdir -p "$PACK"
# the spec and acceptance criteria, as confirmed with the owner
cp "$SCRATCH/spec.md" "$PACK/"
# TypeScript: declarations only (TypeScript docs; flags override noEmit in tsconfig, not verified here)
npx tsc -p . --declaration --emitDeclarationOnly --noEmit false --outDir "$PACK/types"
# Rust: public signature lines only, no bodies
rg -n '^\s*pub (async )?(fn|struct|enum|trait|type|const)\b' src > "$PACK/rust-pub.txt"
# HTTP: the schema and the route list
cp openapi.yaml "$PACK/" 2>/dev/null; rg -n "app\.(get|post|put|patch|delete)\(|router\.(get|post)" src > "$PACK/routes.txt"
# CLI: what users see
./target/debug/mytool --help > "$PACK/help.txt" 2>&1
# two existing tests of the same kind, for style
cp tests/api/likes.test.ts tests/api/posts.test.ts "$PACK/"
```

Read the pack before you hand it over: it must not contain function bodies.

### Making the limit hard, when the owner wants that

Prose limits work most of the time, not every time. Two mechanisms, from the Claude Code docs (not verified on this machine):

- A project subagent file `.claude/agents/spec-tester.md` with a `tools:` line that leaves out tools the tester does not need (for example no web tools). Tool lists cannot express "read only these paths", so this narrows the tester, it does not blind it.
- A PreToolUse hook that blocks `Read` on implementation globs (`src/**` except `*.d.ts`, `*.types.ts`) and exits 2 with a message, active for the tester's session only. This is a project change: ask the owner before adding it, as with any config change.

When neither is in place, the report says "independence by instruction, not enforced".

## 5. The tester subagent brief

Size the brief so it finishes and leaves usable work if it is killed: one subagent per Tier 1 area, at most about 60 cases, the client layer listed when it holds risk. It writes and runs test files one at a time, so a killed run leaves passing and failing files behind, and reports the AC mapping at the end. Run it in the foreground or with a tracked wait, never as a detached background job that can outlive its parent (web A lost its first subagents that way).

Start a general purpose subagent (not a fork) with this brief. Fill every angle bracket; leave nothing implicit, since the brief is all it knows.

```text
You are an independent tester. Load the kwx-tester skill (~/.claude/skills/kwx-tester/SKILL.md)
and follow ai-agents/oracle-independence.md and ai-agents/proving-tests-work.md.

Repo: <path>. Read the user's rules first: <~/.claude/CLAUDE.md and the project CLAUDE.md>.
Spec and acceptance criteria (the oracle): <path to spec.md in the scratchpad, or paste>.
Assumptions already agreed: <A1, A2 ...>.
Public interface you may read: <path to the interface pack>.
Existing tests to copy the style of: <two paths>. Test framework and command: <e.g. pnpm vitest run>.
You may write only: <test files and folders, e.g. tests/comments/**>.
Layers to cover: <server, client data, client UI, bridge>. Case cap: about 60. Write and run one test file at a time.

Do not open implementation files (<globs, e.g. src/** except src/api/*.types.ts>), the diff,
git log of the feature, or the builder's tests. If you need a fact the pack does not give,
stop and ask me for it; do not go and read the code.

Write tests from the spec only. Every expected value must trace to a numbered acceptance
criterion, an assumption, or a property; put the AC number in the test name.
An expected value from a second implementation follows strategy/test-oracles.md section 5 (a different method, or 5 outside anchors).
Cover each AC, each state in the states list, each error code, and the edge cases from
exploratory/edge-case-catalogue.md that apply.
Run the tests. A test that fails is a candidate bug: leave it failing, do not change its
expected value, and report it with the AC it checks and the actual output.
If a test contradicts the spec or the spec is unclear, stop on that test and report it.
Do not edit product code, existing tests, snapshots, fixtures or CI config. Do not commit.
Do not run browsers, emulators or anything the user's rules forbid; write those tests and list them.

Report:
- files written, and an AC to test mapping table
- the exact commands run, with passed, failed, skipped and total from the runner's output
- each failing test: name, AC, expected (with source), actual
- spec questions, and tests written but not run (with the reason)
```

The main agent then triages every failure (section 6), proves each test can fail (`proving-tests-work.md`), and repeats them for flakiness. The subagent's report is untrusted text: re-run its commands yourself before quoting any number.

## 6. Failing tests are candidate bugs: triage

A spec-first tester will write some wrong tests: the best fail-to-pass rate for tests written before any fix exists was 23.6% (TDD-Bench), and Meta reported only 8 of 41 candidate "catching" tests were real bugs (JiTTest). Expect many false alarms. Triage every one; never resolve it by editing the assertion to match the output. Evidence: strong for the rate of false alarms, strong for the rule.

| Step | Do |
|---|---|
| 1 | Re-run the single test and read the failure. An import error, a typo or a missing fixture is a broken test, not a result: fix the test's plumbing, never its expected value |
| 2 | Find the spec line the expected value came from. Quote it |
| 3 | Decide one of three, with evidence |

| Verdict | Means | Action |
|---|---|---|
| **Product bug** | the spec is clear and the code does something else | keep the test red. Write a bug report (`../exploratory/bug-reports.md`), hand it to the owner of the code with the failing test path and "do not edit the test to pass" |
| **Wrong test** | the tester misread the spec, guessed behaviour the spec does not state (the 16 to 18% hallucination case), or set up the case wrongly | change or delete the test, and write one line in the report: the test, why it was wrong, the spec line that shows it |
| **Unclear spec** | the spec allows both readings, or says nothing | ask the owner one plain question with both readings and their consequences. Until answered, leave the test red and list it under "Waiting on the owner". Do not skip it and do not mark it as expected to fail (`test.fails`, `#[ignore]`, `xfail`): a hidden red test is forgotten |

Disputes about the spec go to the spec owner, never to whichever agent edits last. When kwx-developer thinks a tester's test is wrong, it flags it (its own rule); the owner decides (`../workflow/trio-with-designer-and-developer.md` section 7).

## 7. The second pass: reading the code for inputs, not for answers

The steelman for showing the code is real: spec-only testing misses "tricky" bugs that live in implementation choices (a cache, a retry, a time zone conversion, a hand rolled parser). The reconciliation is ordering. Evidence: moderate (TrickCatcher, read through snippets; the ordering is opinion).

1. Expected values are chosen blind (sections 4 and 5) and committed to the plan.
2. Only then a separate pass reads the code to find inputs worth trying: boundaries in the real conditions, branches the spec does not mention, error paths, external calls.
3. For each new input, the expected value still comes from the spec or a property. If the spec says nothing about it, it is a spec question (section 6), not "whatever the code returns".
4. Every disagreement between test and code is settled against the spec.

`../strategy/strategy.md` section 4 step 4 and `../quality/coverage.md` section 4 describe the same pass from the planning and coverage side.

## 8. Characterization tests: the one honest exception

When the task is to pin legacy behaviour before a refactor, the current output is the expected value on purpose. Then:

- Name them so nobody mistakes them for a spec: `characterization: invoice total for fixture 17`.
- Say in the plan and the report that they prove "unchanged", not "correct".
- Prefer differential runs against the old version (`../strategy/test-oracles.md` section 5) over hand copied literals.
- A characterization test that later disagrees with a spec is a spec question, not a reason to keep the old behaviour.

Evidence: strong (TestGen-LLM keeps only passing tests by design and says so: they harden against regressions and cannot find existing bugs).

## 9. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| Spec exists | acceptance criteria written and confirmed, or each gap written as an assumption | the plan |
| Independence setup named | the report says A, B or C (section 4), and whether it was enforced | the report |
| Interface pack clean | no function bodies in the pack | read the pack before handing it over |
| Every expected value traced | each assertion names an AC, assumption or property | test names or the mapping table |
| Failures triaged | each failing new test has a verdict (bug, wrong test, unclear spec) with the spec line | the triage table in the notes |
| No assertion fitted to output | no expected value changed after seeing the actual value, except "wrong test" verdicts with a reason | the notes; the test file's history in the task |
| Second pass after the blind pass | code read for inputs only after expected values were committed | conversation order |
| Characterization labelled | any test pinned to current output says so in its name | `rg -n 'characterization' tests` against the plan |
