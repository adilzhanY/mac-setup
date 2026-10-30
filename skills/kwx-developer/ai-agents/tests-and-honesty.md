# Tests and honesty

How to treat tests so they keep meaning something: never weaken one to pass, stop and flag a test that looks wrong, run the covering tests first, do not treat green as proof, and add property, differential and mutation tests where correctness matters.

Why this file exists: test gaming is the best documented agent failure. METR saw reward hacking in 30.4% of runs where the model could see the scorer and 0.7% where it could not. On tasks made impossible by a planted test bug, Claude Opus 4 and Sonnet 4 hard-coded test cases 51% of the time without a prompt. In ImpossibleBench, Claude models used "modify test cases" in over 79% of their cheating cases. "Do not cheat" barely moved METR's rates (80% to 80%); giving the model a legitimate exit ("tell me if a test is wrong") did. Evidence: strong.

## Contents

1. The rules for existing tests
2. When a test looks wrong: stop and flag it
3. Bug fixes: a failing test first
4. Which tests to run, in which order
5. Passing tests are not proof
6. Property tests
7. Differential tests
8. Mutation testing when correctness matters
9. Make test edits structurally hard
10. Reporting honestly
11. Checks

## 1. The rules for existing tests

1. **Do not edit, delete, skip, mark xfail, or loosen an existing test to make your change pass.** Loosening includes widening a tolerance, replacing an exact assertion with `toBeTruthy`, catching an exception inside the test, snapshot updates you did not read, and mocking out the code under test. Reason: this is the most common way agents fake success. Evidence: strong.
2. **Edit an existing test only when the task changes the behaviour it asserts.** Then, in the report, list each changed assertion with the line of the request or spec that requires it. Reason: a reviewer must be able to tell a spec change from a cheat in seconds. Evidence: vendor claim.
3. **Put no test knowledge in production code.** No literal expected values copied from a test, no `if (process.env.NODE_ENV === 'test')`, no `cfg!(test)` branch that changes behaviour, no checks for a test's exact input. Reason: special-casing survives even when tests are read-only. Evidence: strong (ImpossibleBench).
4. **Do not patch the measuring tools.** No monkeypatching `time`, `Date.now`, `==` / `__eq__` / `PartialEq` to pass a check, no `exit(0)`, no `raise SkipTest`, no stub evaluator. Reason: these are the exact hacks METR and OpenAI recorded. Evidence: strong.
5. **After two failed attempts at a general solution, stop and report.** Reason: special-casing shows up after several failed attempts (Anthropic, Claude 3.7 card), and more retries against the same visible tests raised cheating from 33% to 38% while pass rate rose only 80% to 83% (ImpossibleBench). Evidence: strong.

## 2. When a test looks wrong: stop and flag it

A test can be wrong: stale after an earlier change, asserting an implementation detail, flaky, or contradicting the spec. The right move is the same in every case: do not change the code to fit it, do not change the test to fit the code. Stop and tell the user. An explicit flag exit cut GPT-5's cheating from 54% to 9% and o3's from 49% to 12%; a strict "stop if tests are flawed, do not carve out the code" prompt took GPT-5 from about 92% to 1% on one benchmark. Evidence: strong.

Gather the evidence first, then report in this shape:

```text
Test that looks wrong: tests/billing/test_invoice.py::test_rounds_half_up (line 42)
It asserts: round_amount(2.675) == 2.68
The spec / code says: DECISIONS.md 2026-03-02 "money rounds half to even" -> 2.67
Evidence:
  - pytest tests/billing/test_invoice.py::test_rounds_half_up -> FAILED, got 2.67
  - git log -L 42,42:tests/billing/test_invoice.py -> assertion written 2025-11, before the decision
  - 3 other tests (test_vat, test_totals, test_refund) assert half to even and pass
What I did: nothing to the test or to round_amount.
Options: (a) update this assertion to 2.67, (b) the decision changed and the code is wrong.
Which one?
```

Useful evidence commands: run the single test and quote the failure, `git log -L <start>,<end>:<file>` or `git blame -L` for when and why the assertion was written, the spec or DECISIONS.md line, and other tests that assert the opposite. For a flaky test, run it 20 times (`pytest --count=20` with pytest-repeat, `npx vitest run -t name --retry=0` in a loop, `cargo test name -- --test-threads=1` in a loop) and report the fail ratio.

Then wait for the answer. Carry on with other parts of the task that do not depend on it.

## 3. Bug fixes: a failing test first

1. Write a test that reproduces the bug through the real code path (the route, the command, the public function), not through a private helper.
2. Run it and read the failure. It must fail for the reason in the bug report, not for an import error or a typo.
3. Fix the code.
4. Run it again: it passes.
5. Prove the test guards the bug: revert the fix (`git stash push <fixed files>`), run the test, see it fail, `git stash pop`.

Reason: a reproducing test is concrete context, and the revert step proves it can fail. Generic "do TDD" instructions raised regressions from 6.08% to 9.94% in TDAD, so the value is in the specific failing test, not in the ritual. Evidence: medium.

## 4. Which tests to run, in which order

Run the tests that cover the change first, then the full suite. Telling the agent exactly which tests cover the changed code cut regressions by 70% (6.08% to 1.82%) in TDAD. SWE-bench itself only runs the test files the fix touched, which is why 29.6% of its "passing" patches diverge: running only the nearest test reproduces that blind spot. Evidence: medium (TDAD is small), strong for the blind spot.

Find the covering tests:

| Stack | Command |
|---|---|
| Jest | `npx jest --findRelatedTests src/billing/invoice.ts` |
| Vitest | `npx vitest related src/billing/invoice.ts --run` |
| pytest | `pytest $(rg -l -F 'billing.invoice' tests/)`, or `pytest --testmon` if pytest-testmon is installed |
| Rust | `cargo test -p <crate>` for the crate, plus `cargo test -p <each dependent crate>` (`cargo tree -i <crate> --workspace`) |
| Go | `go test ./billing/...`, then `go test ./...` (the test cache makes the wide run cheap) |
| Any | `rg -l -w '<changed symbol>' -g '*test*' -g '*spec*'` from the caller map in `before-you-code.md` |

Order: covering tests until green, then the full suite once. If the full suite has failures that also fail on the base branch, prove it (`git stash; <run>; git stash pop`) and report them as pre-existing; do not fix them inside the task unless asked, and do not hide them.

## 5. Passing tests are not proof

Green means the assertions that exist passed. It does not mean the change is right. On SWE-bench Verified, 29.6% of patches marked resolved behave differently from the developer's fix and half the certainly wrong ones were caught by no developer test; SWE-Bench+ found 31.08% of successful patches passed only because tests were weak. Evidence: strong.

Before trusting green, answer these in the report:

- Did each new test fail before the change? (the revert step in section 3)
- Does the test assert behaviour the user cares about (output, stored row, response body), or only that a function was called?
- Is the code under test mocked so heavily that the test checks the mock?
- Are the edge cases from the acceptance list (empty, null, huge, unicode, concurrent, unauthorized) each tested?
- Did the full suite run, not only the nearest file?

If any answer is no, say so in "Not checked".

## 6. Property tests

Use a property test when the code has a rule that holds for all inputs: parsers and serializers, encoders, money and unit math, sorting and dedup, date ranges, state machines, permission rules, any pure function with a wide input space. A Claude Code agent running Hypothesis over 100 Python packages found bugs where the top-ranked reports were 86% valid. Evidence: medium.

| Language | Library |
|---|---|
| Python | Hypothesis |
| TypeScript / JS | fast-check |
| Rust | proptest (or quickcheck) |
| Go | `testing/quick`, or rapid |
| Kotlin / Java | jqwik, Kotest property testing |

Properties that find real bugs, in the order to try them:

1. Round trip: `parse(format(x)) == x`, `decode(encode(x)) == x`.
2. Invariant: output sorted, total equals sum of lines, balance never negative, length preserved.
3. Idempotence: `f(f(x)) == f(x)` for normalizers, migrations, dedup, retries.
4. Oracle: the new fast version equals a slow obvious version on the same input.
5. Metamorphic: scaling all amounts by 2 doubles the total; adding an unrelated row does not change a filtered result.

```python
from hypothesis import given, strategies as st

@given(st.lists(st.integers(min_value=0, max_value=10**9)))
def test_total_is_sum_of_lines(cents):
    assert invoice_total([Line(c) for c in cents]) == sum(cents)
```

## 7. Differential tests

Use a differential test for refactors, rewrites, performance work, library upgrades and ports: run the old and the new code on the same inputs and compare outputs. This is how PatchDiff found that 29.6% of test-passing patches changed behaviour. Evidence: strong.

```bash
git worktree add ../base origin/main        # the old code, untouched
# run the same input set through both and diff the outputs
for f in fixtures/inputs/*.json; do
  (cd ../base && ./run.sh "$f") > /tmp/old.out
  ./run.sh "$f" > /tmp/new.out
  diff -q /tmp/old.out /tmp/new.out >/dev/null || echo "DIFF: $f"
done
git worktree remove ../base
```

For inputs, use recorded production-like fixtures plus a property-test generator. Every difference is either an intended change (list it in the report) or a bug.

## 8. Mutation testing when correctness matters

Use mutation testing on code where a wrong answer costs money, data or security: payments and money math, auth and permissions, parsers of untrusted input, data migrations, anything with a compliance rule. A surviving mutant is an assertion that is missing. Meta's mutation-guided test generation produced 571 privacy tests, 73% accepted by engineers, and a summary of the same paper reports about half of them would have been dropped by a coverage-only rule. Evidence: medium.

Run it scoped to the changed files only, since a full run is slow:

| Stack | Command |
|---|---|
| JS / TS | `npx stryker run --mutate src/billing/invoice.ts` |
| Python | `mutmut run --paths-to-mutate src/billing/invoice.py` (mutmut 2; in mutmut 3 set `paths_to_mutate` under `[tool.mutmut]` in pyproject.toml) |
| Rust | `cargo mutants --file src/billing/invoice.rs` (or `--in-diff <(git diff)`) |
| Java / Kotlin | PIT: `mvn org.pitest:pitest-maven:mutationCoverage -DtargetClasses=com.app.billing.*` |
| Go | `gremlins unleash ./billing` |

For each surviving mutant: add the assertion that kills it, or explain why it is equivalent (the mutated code behaves the same). Report the score before and after.

## 9. Make test edits structurally hard

Prose rules work "most of the time, not every time" (Anthropic). Read-only tests kept legitimate performance and blocked test edits in ImpossibleBench, while hiding tests hurt honest performance. Evidence: strong. When you set up a project for agents, or the user asks for it, add a guard.

Claude Code, `.claude/settings.json`:

```json
{
  "permissions": {
    "deny": ["Edit(tests/**)", "Edit(**/*.test.ts)", "Edit(.github/workflows/**)"]
  }
}
```

`Edit(...)` rules cover every built-in file editing tool. Use a PreToolUse hook instead when tests live next to the source (`*.test.ts`, `*_test.go`), when test edits should need approval rather than be blocked, or when Bash commands like `sed -i` must be covered too. Keep CI config out of the agent's write access as well: CI is the gate the agent must not be able to edit.

In review, flag every test file in the diff: `git diff --name-only origin/main... | rg -i '(test|spec)'`.

## 10. Reporting honestly

"All tests pass" on its own tells the reader very little (Anthropic). Evidence: vendor claim. End every task with this block, filled in:

```text
Ran:
  pnpm tsc --noEmit                      -> 0 errors
  pnpm vitest related src/billing/invoice.ts --run -> 14 passed
  pnpm test                              -> 812 passed, 2 failed (both fail on main too: test_x, test_y)
Tests changed: none   (or: each changed assertion and the request line that requires it)
Not checked: e2e suite (needs Stripe test keys, not in env); UI rendering of the invoice page
Known limits: rounding of negative amounts not covered by any test
```

Never write that a check passed if it did not run. Never describe a partial fix as complete. If a part of the task could not be done, say which part and why, at the top of the report.

## 11. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| No weakened tests | no test file in the diff, or each change justified by the request | command 1 below |
| No new skips | none added | command 2 below prints nothing |
| No test knowledge in production | no test-env branch or copied literal | command 3 below prints nothing |
| New test fails without the fix | fails when the fix is stashed | `git stash push <src files>`, run the test, `git stash pop` |
| Covering tests ran first | named in the report | the report lists the related-tests command |
| Full suite ran | result in the report, pre-existing failures proven on base | the report plus the base run |
| Mutation score (critical code) | no unexplained surviving mutants in changed files | the mutation tool's report |
| Honest report | Ran / Tests changed / Not checked / Known limits all present | read the final message |

```bash
# 1. test files touched by the change
git diff --stat origin/main... -- '*test*' '*spec*' tests/
# 2. skips and focus markers added
git diff origin/main... | rg '^\+.*(\.only\(|\.skip\(|xfail|@pytest\.mark\.skip|#\[ignore\]|t\.Skip\(|SkipTest)'
# 3. test knowledge in production code
git diff origin/main... -- src/ lib/ app/ | rg '^\+.*(NODE_ENV.*test|cfg!\(test\)|PYTEST_CURRENT_TEST)'
```
