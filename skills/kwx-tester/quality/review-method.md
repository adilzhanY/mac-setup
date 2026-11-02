# Review method: reviewing someone else's tests or a test PR

How to review tests written by someone else: a teammate's test PR, kwx-developer's tests for its own change, a generated suite, a tester subagent's output. The order is the method: read the spec first and write down what you would test, then read the tests and map them to the spec, and only then read the code, to find risks nobody tested. Reading the code first makes the reviewer accept whatever the tests assert, which is the same trap that makes code-aware tests enshrine bugs (`../ai-agents/oracle-independence.md` section 1). Then run the tests, prove they can fail, and back every finding with evidence. `~/.claude/skills/kwx-developer/quality/review-method.md` reviews product code; this file reviews the tests themselves.

## Contents

1. What a test review answers
2. Step 1: the spec first
3. Step 2: the tests, mapped to the spec
4. Step 3: the code, for untested risks
5. Step 4: run, repeat, and prove they can fail
6. The smells that lie
7. Evidence for each finding
8. Severity and the output format
9. A fresh context reviewer for tests
10. Checks

## 1. What a test review answers

1. Do these tests check what the spec says, with expected values that come from the spec?
2. Would they fail if the behaviour broke? (Proven, not assumed.)
3. Are the risky parts and the states covered, at the right level?
4. Will they stay trustworthy: deterministic, isolated, readable when they fail?
5. Did the change weaken anything that existed?

Not review findings: formatting a formatter owns, naming preferences the house convention does not settle, and tests for cases that cannot happen. A reviewer asked to find problems always finds something (Claude Code best practices); drop findings that ask for impossible cases.

## 2. Step 1: the spec first

Before opening a test file:

1. Get the intent and the spec: the issue, the ACs, the PR description, the UI states list, the API contract, DECISIONS.md lines for the area.
2. Write your own short list of what must be tested: each AC, each state, each error code, the boundaries, the risks that matter (money, data, auth, sync, time). Five minutes, a list of lines. This is your oracle for the review.
3. If there is no spec, write the acceptance list from the issue and the user's words, mark it "derived", and say so in the review.

## 3. Step 2: the tests, mapped to the spec

```bash
git diff --stat "$BASE"...HEAD -- '*test*' '*spec*' tests __tests__ e2e '*.snap'
gh pr diff <n> > "$SCRATCH/pr.diff"           # gh-axi where the user's rules prefer it
python3 -I ~/.claude/skills/kwx-tester/scripts/smellscan.py $(git diff --name-only "$BASE"...HEAD -- '*test*' '*spec*')
```

For each test, write one line in a mapping table: test name, what it checks, which item of your list it covers, the source of its expected value.

| Your list item | Test | Expected value from | Verdict |
|---|---|---|---|
| AC3 reject over 2000 | `post.test.ts` "rejects long comment" | spec AC3 | covered |
| AC3 accept exactly 2000 | none | | gap |
| state "signed out" | `post.test.ts` "401 when signed out" | contract error code | covered |
| retry after 5xx keeps text | none | | gap |
| (none) | `post.test.ts` "formats date" | the code's current output, literal `"31 Oct, 14:02"` | not from the spec: characterization at best |

Items on your list with no test are gaps. Tests that cover nothing on your list are either extra value (an edge you missed: add it to the list) or noise.

Also read the diff of existing tests: every deleted, loosened, skipped or re-recorded test needs a reason in the intent (`~/.claude/skills/kwx-developer/ai-agents/tests-and-honesty.md` section 1).

## 4. Step 3: the code, for untested risks

Only now read the implementation, to find what the spec does not show: caches, retries, time zone conversions, hand rolled parsers, error branches, permission checks, external calls. For each, ask whether a test exercises it with an expected value from the spec. Run diff coverage as a second opinion:

```bash
python3 -I ~/.claude/skills/kwx-tester/scripts/diffgaps.py "$SCRATCH/cov/lcov.info" "$BASE"    # changed lines and branches no test ran (lcov from the project's coverage run)
```

An uncovered branch on a risk path is a gap finding. Dead code is a finding for the builder, not a test to write.

## 5. Step 4: run, repeat, and prove they can fail

1. Run the changed tests and the covering tests with the project's commands; read the numbers from the runner (`../ai-agents/honest-reporting.md` section 3). The total must be above zero and include the new tests by name.
2. Repeat the new tests by flake class with retries off: flake risk tests 20 times and once shuffled, deterministic ones in one shuffled suite run plus 2 repeats (gate C2, `../strategy/flaky-tests.md` section 3). Any failure is a flaky finding with the ratio.
3. Prove the important tests can fail (`../ai-agents/proving-tests-work.md`), in a scratch worktree, never in the author's tree:
   - a bug fix test: run it on the base, it must fail for the bug's reason;
   - a feature test: plant the obvious mutant on the line it guards, or run the mutation tool on the changed files; it must be killed;
   - a new module: no-op its core; the suite must go red.
4. Tests the user's rules keep you from running (browser, device) are read, not run, and listed as "not run".

## 6. The smells that lie

These make a test pass when the behaviour is wrong. Look for them first. Detail and fixes: `../quality/test-smells.md` section 3 and 4.

| Smell | How it shows | Why it lies |
|---|---|---|
| No assertion (Unknown, Empty) | a test body with calls and no `expect`, `assert`, `should`; a TODO in place of the check | passes whatever happens |
| Liar | asserts something that does not depend on the code under test (a constant, the mock's own return value, the input echoed) | passes whatever the code does |
| Tautology | the expected value is computed with the same function or formula as the code (`expect(total(x)).toBe(total(x))`, a helper that reimplements the logic) | repeats the bug on both sides |
| Expected value copied from output | a long literal (a date string, a float with many digits, a snapshot) with no spec source, written after the code | enshrines current behaviour, bugs included |
| Mock of the unit under test, or of owned code | `vi.mock('./comments')` in `comments.test.ts`; the repository mocked in a service test that is about the query | the test checks the mock |
| Assertion only on calls | `expect(api.post).toHaveBeenCalled()` and nothing about the result or state | the call can happen with wrong data, or the result can be ignored |
| Swallowed exception | `try { ... } catch {}` inside the test, or `expect(fn).not.toThrow()` as the only check | failures vanish |
| Conditional logic | `if (result) expect(...)`; loops whose body may never run | the assertion may never execute |
| Blind snapshot | a snapshot re-recorded in the same commit as the source change, no reasoning; huge snapshots nobody can read | the new output became the expected value without review |
| Focus or skip left in | `.only`, `.skip`, `xit`, `#[ignore]`, `test.fixme` | other tests silently stop running |
| Retries hiding failure | `retries: 2` added with the test; a pass after retry reported as a pass | flakiness looks green |
| Fixed waits | `waitForTimeout(500)`, `sleep(1)` | passes on a fast machine, flakes elsewhere, and may pass before the behaviour happens |
| Too weak a matcher | `toBeTruthy()`, `toBeDefined()`, `length > 0` where the spec gives an exact value | most wrong values pass |
| Test knowledge in product code | `if (process.env.NODE_ENV === 'test')`, a tested literal hard coded in product code | the code special cases the test |

## 7. Evidence for each finding

A finding without proof is an opinion. Each carries one of:

- **A run:** the command and its output (the test passing on the base, a mutant surviving, 3 failures in 20 repeats).
- **A mapping:** the spec line with no test, or the test whose expected value has no spec line, quoted with file:line.
- **A counterexample:** a concrete wrong implementation the test would accept ("`total()` returning 0 for an empty cart and 100 otherwise passes all 4 tests in `cart.test.ts`").
- **A quoted smell:** the lines, with file:line, and why they cannot fail.

If you cannot produce one, mark the confidence "possible" or drop it.

## 8. Severity and the output format

| Severity | Test findings | Merge? |
|---|---|---|
| Blocker | an existing test weakened, skipped or deleted without a reason; a new test that cannot fail (passes on the base, survives the obvious mutant) on money, data, auth or permissions; a focused test committed; test knowledge in product code | no |
| Major | an AC or a state with no test; an expected value with no spec source on a main path; a mock of the unit under test; a flaky new test; no error path tested | not until fixed or accepted |
| Minor | weak matcher where a gap is unlikely; a slow test at the wrong level; assertion roulette | author's call |
| Nit | names, ordering, comments | only when asked |

Confidence: **certain** (reproduced by a run), **likely** (traced or mapped, not run), **possible** (a pattern that is often wrong).

```text
[Blocker, certain] The new coupon test passes without the fix
Where: tests/checkout/coupon.test.ts:22 "applies 10% coupon"
What: the expected total 90 is computed with applyCoupon() itself (line 20), so the test repeats whatever the code does.
Proof: in a worktree at BASE (before the fix), the test passes: `npx vitest run tests/checkout/coupon.test.ts` -> 1 passed.
Spec: AC2 "a 10% coupon on a 100 EUR cart gives 90.00 EUR"; the test should assert the literal 9000 cents from the spec.
Fix: replace the computed expectation with the spec value; add the 0.005 rounding case from AC4.
```

End with a summary: counts per severity, the mapping table's gaps, the commands run with their numbers, what was not run and why, and one line on what is good only when it helps the author keep doing it. Post findings as PR comments only when the user asks, and then as one review.

## 9. A fresh context reviewer for tests

For a large generated suite, or tests on money, auth or data, get a second read from a context that did not write the tests and has not read the implementation. Start a read-only subagent (Read, Grep, Glob, read-only Bash) with:

```text
Review these tests against the spec. You did not write them; assume nothing is right.
Spec and acceptance criteria: <paste or path>. UI states list and error codes: <paste>.
Test files to review: <paths>. Do not read the implementation under src/ until step 3.
1. From the spec alone, list what must be tested (each AC, state, error code, boundary, risk).
2. Map each test to that list: what it checks, where its expected value comes from. List gaps
   and tests whose expected values have no spec source.
3. Then read the implementation only to find risky branches with no test.
4. Flag the smells that lie: no assertion, liar, tautology, value copied from output, mock of the
   unit under test, assertion only on calls, swallowed exception, conditional assertion, blind
   snapshot, focus or skip, retries, fixed waits, weak matchers.
For each finding: severity (blocker, major, minor), confidence, file:line, the evidence.
Skip style and cases that cannot happen. Do not edit any file.
```

Triage what comes back: check likely findings with a run before reporting them, drop requests for impossible cases, and say which were dropped and why.

## 10. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| Spec before tests | your own test list existed before you opened a test file | the review notes, in order |
| Mapping table | every test mapped to a list item and an expected value source; every list item has a test or is a gap | the table |
| Code read last | the implementation was read only after the mapping | conversation order |
| Tests run | changed and covering tests ran with real numbers, total above 0; new tests repeated by flake class (gate C2) | commands and output |
| Proof sampled | at least the blocker candidates were checked on the base or with a mutant | the runs |
| Evidence per finding | each finding has a run, a mapping, a counterexample or a quoted smell | read the findings |
| Severity and confidence | each finding has both; no possible stated as certain | read the findings |
| No style noise | no finding a formatter owns or pure preference | read the findings |
