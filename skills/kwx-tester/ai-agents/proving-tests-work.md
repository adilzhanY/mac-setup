# Proving tests work: every new test must be seen failing for the right reason

A test that passes has proved only that it passes. Before a new test counts, the tester must see it fail when the behaviour it guards is wrong, and the failure must be the one the test is about, not an import error or a typo. This file gives the four ways to get that proof (fail before the fix, a planted mutant, an ablation of the change, a revert), how to do them without touching the user's working tree, how to repeat new tests for flakiness, and how held-out checks catch what the visible suite cannot. The builder's version of "fail first" for a bug fix is `~/.claude/skills/kwx-developer/ai-agents/tests-and-honesty.md` section 3; mutation tools and triage are in `../strategy/mutation-testing.md`. This file is the tester's proof procedure that ties them together.

## Contents

1. Why green is not proof
2. The right reason
3. Proof 1: red before the fix (fail to pass)
4. Proof 2: a planted mutant
5. Proof 3: ablation, the change turned into a no-op
6. Doing it without touching the working tree
7. Held-out checks and the final independent check
8. Repeat runs for flakiness
9. The evidence block
10. Checks

## 1. Why green is not proof

| Finding | Number | Evidence |
|---|---|---|
| Coverage does not mean the code is checked | GPT-4o tests: 35.2% coverage, 18.8% mutation score (TestGenEval): about half the executed code ran with no assertion that would notice a change | strong |
| Tests can pass while the deliverable is dead | *Building to the Test*: replacing the library's state method with a no-op did not move the scores in all 12 dead library cells; real implementations dropped | moderate (18 runs, one task) |
| Self-written tests let wrong answers through | Reflexion's self tests had a 16.3% false positive rate on MBPP, and the loop scored below the plain baseline | strong |
| The fail to pass rule makes generated tests useful | SWT-bench counts a test only if it fails before the fix and passes after; such tests doubled the precision of a fix filter | strong |
| Mutation guided tests are accepted by engineers | Meta ACH: 571 tests from 9,095 mutants, 73% accepted | strong |

No study measures "red first" as an anti-gaming guard directly. The rule rests on the mechanism and the studies above. Evidence: moderate.

## 2. The right reason

A failure counts only when the assertion that guards the behaviour fails, with a message that names the behaviour.

| Failure seen | Counts? |
|---|---|
| `expected 422, received 201` on the "too long comment" test | yes |
| `expect(received).toEqual(expected) - "Too long (2000 max)" + undefined` | yes, if the spec says that message |
| `Cannot find module './comments'` | no: a broken test. Fix the plumbing, run again |
| `TypeError: x is not a function` in the test's own setup | no |
| timeout after 5000 ms | no, until you know what it waited for |
| the test fails on the base and still fails after the fix | no: it tests something else, or the fix is wrong |

Write the failure line into the evidence block (section 9).

## 3. Proof 1: red before the fix (fail to pass)

For a bug fix, or a feature whose code is not written yet (tests before the build):

1. Run the new test on the code without the fix or feature. It must fail for the right reason.
2. Run it on the code with the fix. It must pass.
3. Record both runs.

When the tests were written before the build (setup A in `oracle-independence.md` section 4), step 1 happens naturally: run them before the builder reports done and keep the output. A test that passes before the feature exists tests nothing about the feature (or the feature already existed: find out which).

## 4. Proof 2: a planted mutant

For code that already exists and passes, plant a small bug the test should catch and run the test. Use the mutation tool when the stack has one; plant by hand only on a scratch copy (section 6).

```bash
# scoped to the changed files (commands from strategy/mutation-testing.md, verified there)
cargo mutants --in-diff "$SCRATCH/changes.diff"
npx stryker run --mutate "$(git diff --name-only "$BASE"...HEAD -- 'src/**/*.ts' ':!**/*.test.ts' | paste -sd, -)"
```

| Result for a mutant on the line the test guards | Means |
|---|---|
| killed by the new test | proof: the test can fail for this fault |
| survived | the test misses this fault: strengthen the assertion, or show the mutant is equivalent (`../strategy/mutation-testing.md` section 8) |
| killed only by another test | fine for the suite, but the new test adds nothing for this fault: ask why it exists |

Hand planted mutants that work well: flip a comparison (`<` to `<=`), drop a condition, return the default (`0`, `""`, `[]`, `None`, `Ok(())`), skip a write, swap two arguments, remove an authorization check, change a time zone to UTC.

A planted fault batch on a module proves many tests at once: a test counts as proven when at least one planted fault on the behaviour it names turns it red. Pick faults from the module's risks (flip a boundary, change a constant, floor instead of round, a limit off by one, a function returning 0, a check removed). Batch size follows the tier: 10 to 15 for Tier 1, 3 to 5 for Tier 2 (`../strategy/strategy.md` section 5a). Report the batch as the table fault | failed tests | caught or not, with an equivalence argument for each fault not caught. A test no fault turned red is unproven (gate C8). Scratch worktree only (section 6).

Example: web A planted 14 faults in the tax and rate limit modules: 12 caught, 2 argued equivalent. Tests that no fault turned red stayed unproven (C8). The shape of the table (illustrative rows):

```text
| Fault                                  | Failed tests                 | Caught |
|----------------------------------------|------------------------------|--------|
| Free allowance 12096 -> 12097          | tax.test: boundary AC3 (2)   | yes    |
| Math.round -> Math.floor in cents()    | vat.test: AC5 rounding (4)   | yes    |
| `<=` -> `<` on the zero tax check      | none                         | no: equivalent, both branches return 0 at the boundary |
```

## 5. Proof 3: ablation, the change turned into a no-op

Ablation asks the question mutation testing asks at the scale of the whole change: if the new code did nothing, would the tests notice? It is the only probe that caught "building to the test", where the tested behaviour lived somewhere other than the deliverable. Evidence: moderate.

1. Take the changed code: the new function, module, handler or component the task asked for.
2. In a scratch copy (section 6), turn it into a no-op that still compiles: the function returns its input or a default, the handler returns 200 with an empty body, the component renders nothing, the library's state method does nothing.
3. Run the suite that is meant to cover it. **The score must drop.** List which tests went red.
4. If nothing went red, the tests do not test the change. If only unrelated tests went red, the tests test something else (a demo, a copy, a mock).

```bash
# example: the library's public function becomes a no-op in a scratch worktree
git worktree add -q "$SCRATCH/ablate" HEAD
cd "$SCRATCH/ablate"
git -C "$OLDPWD" diff | git apply            # bring in uncommitted work, if any
# edit the copy, not the user's tree: make filterRows return its input unchanged
perl -0pi -e 's/(export function filterRows\([^)]*\)[^{]*\{)/$1 return rows;/' src/table/filter.ts
npx vitest run src/table --reporter=dot      # expect failures; record which
cd - && git worktree remove --force "$SCRATCH/ablate"
```

The `perl` line is an example for one function shape; edit the copy by hand when a pattern is not obvious. In Rust, `cargo mutants` already includes "replace function body with `Default::default()`", which is an ablation per function.

## 6. Doing it without touching the working tree

The tester never edits product code, and never leaves the user's tree changed. Mutation and ablation edits happen only in a scratch copy or inside a tool that restores files.

| Need | Do | Never |
|---|---|---|
| Code before the fix, change committed | `git worktree add "$SCRATCH/base" "$BASE"`, copy the new test file in, run it there | `git checkout` the base in the user's tree |
| Code before the fix, change uncommitted | `git worktree add "$SCRATCH/base" HEAD` (it lacks the uncommitted change), copy the new test in, run | `git stash` on the user's tree when other work may be in it |
| Code with an ablation or hand mutant | worktree at HEAD, `git diff \| git apply` inside it, edit there | edit files in the user's tree, even "for one run" |
| Mutation tool | the tool's own copy and restore (Stryker sandbox, cargo-mutants copies the tree) | run a tool that mutates in place without a clean `git status` first |

Before and after every probe: `git status --porcelain` in the user's tree must print the same thing. Dependencies: a fresh worktree has no `node_modules` or `target`; symlink or reinstall inside the scratch copy (`ln -s "$PWD/node_modules" "$SCRATCH/base/node_modules"`), never in the user's tree.

## 7. Held-out checks and the final independent check

Every visible check that an agent iterates against becomes its target. SpecBench found every model saturating the visible tests with a 43 to 48 point drop on held-out ones; moving held-out cases into the visible suite had mixed effects (one gap shrank from 35 to 9 points, another widened by 25). Evidence: strong.

1. **Keep a held-out set.** When the tester works alongside a builder (`../workflow/trio-with-designer-and-developer.md`), it splits its tests: the acceptance tests the builder may see (read only), and a held-out set kept in the scratchpad until the builder reports done. Put composition and journey cases in the held-out set: two features used together, a full user flow, a differential run against the old version.
2. **Never move held-out cases into the visible suite while the builder is still iterating.** After the builder reports done, run them, then add them to the repo as regression tests.
3. **End with a check the builder did not run:** the held-out set, a differential run, or a fresh judge over the diff (`../workflow/test-a-change.md` step 7). Never define done as "the builder's loop went green".
4. **Cap fix and rerun loops.** If the builder needs more than two rounds against the same failing test, stop and look at the test and the spec with the owner; more rounds raise gaming more than honest passes (ImpossibleBench 33% to 38% versus 80% to 83%).

## 8. Repeat runs for flakiness

78% of flaky tests are flaky from the day they are written, so the cheapest place to catch them is at birth. Evidence: strong (Luo et al. 2014). Flakiness comes from I/O, time, concurrency and order, so the number of repeats follows the test's flake class (gate C2):

- **Flake risk** (touches I/O, a database, time or timers, concurrency, network, randomness or UI rendering): 20 times green alone and in the suite, plus one shuffled run.
- **Deterministic** (pure functions, fixed inputs, no I/O, no clock): one shuffled suite run plus 2 repeats.

Label each new test file with its class in the notes. Commands per stack are in `../strategy/flaky-tests.md` section 3. Short form:

```bash
npx vitest run tests/comments.test.ts --repeats 20                   # verified flag in flaky-tests.md (Vitest 5)
npx vitest run --sequence.shuffle --sequence.seed=$RANDOM
for i in $(seq 20); do cargo test comments:: -- --exact || break; done
pytest --count=20 tests/test_comments.py                             # pytest-repeat
npx playwright test e2e/comments.spec.ts --repeat-each=20 --retries=0   # only when the user allows browsers, or in CI
```

- For a slow suite where 20 runs is too costly (an end to end flow in CI), run at least 5 (Meta's filter) and say the number in the report.
- Retries must be off (`--retries=0`, `--retry=0`) during the repeat run. A pass after a retry is a flaky result, never a pass.
- One failure in 20 is a flaky test. Do not ship it: find the cause (`../strategy/flaky-tests.md` section 6). Never fix it with a sleep.
- Device flows (Maestro, Detox) repeat only with the user's yes, since they drive a device.

## 9. The evidence block

Write one block per new test or per group of tests that share a proof, and keep it in the notes for the report.

```text
Test: tests/comments/post.test.ts "rejects a 2001 char comment (AC3)"
Proof: red before the feature
  base (worktree at a1b2c3d): FAILED  expected 422, received 201
  head:                        passed
Mutant: src/routes/comments.ts:31  `body.length > MAX` -> `body.length >= MAX`  killed by "accepts exactly 2000 chars (AC3)"
Ablation: postComment returns 201 without insert -> 6 of 9 comment tests red (list in notes)
Repeats: 20/20 green alone, 20/20 in suite, shuffled seed 23817 green
```

## 10. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| Every new test proven | each has one of: red before the fix, a killed mutant, an ablation drop | the evidence blocks |
| Right reason | each recorded failure is the guarding assertion, not plumbing | the failure lines in the blocks |
| Ablation for whole deliverables | a new module or feature had its core turned into a no-op and the score dropped | the ablation line |
| Working tree untouched | `git status --porcelain` identical before and after every probe; no product file edited | run it before and after; `git diff --stat` |
| Held-out last | a check the builder did not run ran at the end, or the report says why none existed | the report |
| Repeats | flake risk: 20 green runs (or at least 5 for slow CI suites, stated) plus one shuffled run; deterministic: one shuffled suite run plus 2 repeats; retries off; class noted per file | the commands and their output |
| Unproven tests not counted | tests with no proof are listed as unproven, not in the passed count of new tests | the report |
