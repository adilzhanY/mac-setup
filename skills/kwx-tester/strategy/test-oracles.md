# Test oracles: how to know the right answer

An oracle is the source of the expected result: the thing that tells you whether an output is right. A test without a real oracle runs code but checks nothing. This file lists the kinds of oracles, from the strongest (an exact value from the spec) to the weakest (the program did not crash), how to build oracles when the right answer is hard to compute (invariants, metamorphic relations, differential testing, round trips, golden files), and what to do when there is no spec at all.

The term "oracle problem" comes from Weyuker ("On testing non-testable programs", 1982): for many programs an oracle is too costly or impossible to build. Barr, Harman, McMinn, Shahbaz and Yoo surveyed the solutions ("The Oracle Problem in Software Testing: A Survey", IEEE TSE 2015). The consistency heuristics an exploratory tester uses (FEW HICCUPPS) are covered in depth in `exploratory/heuristics.md`; this file is about oracles you can automate.

## Contents

1. Kinds of oracles, strongest first
2. Specified oracles: the spec and the acceptance criteria
3. Invariants and partial oracles
4. Metamorphic testing
5. Differential testing and reference implementations
6. Round trips, idempotence and golden files
7. When there is no spec
8. Implicit oracles: crashes, hangs, logs, accessibility
9. Oracle mistakes
10. Checks

## 1. Kinds of oracles, strongest first

| Kind | Example | Strength |
|---|---|---|
| Specified exact value | "5 seats yearly for a student cost 125 €" from the pricing spec | Strongest: one right answer, written before the code |
| Model | A simple in memory map that the real store must match after every operation | Strong, covers many inputs; the model can share a bug with the code if written the same way |
| Differential | Old version vs new version, or two implementations, on the same input | Strong for refactors and ports; both can be wrong together |
| Metamorphic relation | "Adding a filter never returns more results" | Partial: checks a relation, not the value |
| Invariant / property | "Balance never negative", "output sorted", "no duplicate ids" | Partial |
| Golden file | The output last approved by a human | As good as the review that approved it |
| Consistency heuristic | Consistent with the product's history, its claims, comparable products, user expectations | Human judgement; strong at finding issues, weak at proving correctness |
| Implicit | No crash, no panic, no hang, no error in the console, no accessibility violation | Weakest for correctness; still finds real bugs at scale (fuzzing) |

Combine them. A pricing function gets exact values from the decision table, plus properties for all inputs. A sync engine gets a model, plus invariants checked after every step.

## 2. Specified oracles: the spec and the acceptance criteria

- **Write the expected value as a literal in the test.** Never compute it with the code under test or with a copy of its logic (kwx-developer T4: no logic in tests). If the literal is hard to derive by hand, the case is a good candidate for a property or a model instead.
- **Quote the source.** Put the spec line or acceptance criterion next to the test (`// AC2: lifetime has no student discount`). When the spec changes, a search finds the tests.
- **Check the whole observable result.** For a function, the return value and the error variant. For an endpoint, status, body and the stored row. For a screen, the text the user sees. Asserting only `status === 200` misses a wrong body.
- **Exact beats loose.** `toEqual({ ok: false, code: "PASSWORD_RULES" })` beats `toBeFalsy()`. Loose assertions are how tests pass on wrong answers.

## 3. Invariants and partial oracles

An invariant is something that must hold no matter the input or the step: a balance is never negative, a list stays sorted, the sum of line items equals the total, every foreign key points to an existing row, the timer's remaining time never goes up while running, a user never sees a row they do not own.

- Check invariants after every operation in model based and stateful tests, not only at the end (fast-check commands, Hypothesis `@invariant()`, proptest `check_invariants`).
- In end to end and integration tests, an invariant query on the database after the test is a cheap second oracle: `select count(*) from workouts where user_id is null` must be 0.
- An invariant alone is a partial oracle. Hughes (2020) found that validity properties (the data structure invariant holds) missed five of eight planted bugs; a function that always returns an empty but valid result passes them all. Pair invariants with a stronger oracle.

### Consistency across outputs

When the same quantity appears on several surfaces (UI total, overview, CSV, PDF invoice, API, email), write one test per quantity that builds one fixture and asserts that all surfaces agree to the cent. Use a rounding sensitive fixture: 7 min at 95 EUR, 7 min 20 s at 95 EUR, 1 h 20 min at 85,50 EUR, a tax amount with a half cent. When rounding differs by design (whole euros in a headline, cents in a row), the spec must say so; otherwise it is a bug. Trial: one arm priced CSV by exact seconds and invoices by rounded minutes, the other billed amounts that differ from its own Offene Zeiten view.

## 4. Metamorphic testing

Metamorphic testing was introduced by Chen, Cheung and Yiu (1998) for programs where checking one output is hard but relations between outputs of related inputs are easy. Their example: you cannot easily check that a path in a big graph is the shortest, but the shortest distance from x to y must not change when you swap x and y, and a subpath of a shortest path must itself be shortest. Since then it has found bugs in compilers, search engines, machine learning systems and scientific software (Chen et al., "Metamorphic Testing: A Review of Challenges and Opportunities", ACM Computing Surveys 2018). Evidence: strong.

A metamorphic relation (MR) says: if input changes in way T, the output must change in way R (or not change). Recipe:

1. Pick a transformation of the input that the spec lets you reason about: add, remove, reorder, scale, duplicate, negate, rename, split into parts.
2. State what must happen to the output.
3. Run the source input and the follow up input, compare with R.
4. Generate many source inputs with a property testing library.

MRs for the owner's kinds of products:

| Product | Transformation | Relation |
|---|---|---|
| Search or filter screen | Add one more filter | Results are a subset of the previous results |
| Search | Reorder or change case of the query words (if the spec says it is case and order insensitive) | Same result set |
| Sorting | Shuffle the input | Same output |
| Pricing | Double the seats | Price doubles; yearly never more than 12 monthly |
| Workout timer | Insert a pause of any length | Total active time unchanged |
| Statistics page | Add a workout dated outside the selected range | Numbers unchanged |
| Unit conversion (weather app) | Convert to Fahrenheit and back | Same value within rounding |
| Translation or gloss app | Add a blank line between verses | Same glosses per verse |
| CLI that processes files | Process files one at a time vs all at once | Same combined output |
| Map or route | Reverse start and end on an undirected graph | Same distance |

Hughes found metamorphic properties "less effective individually, but powerful in combination", and a good alternative to a model when a model is expensive to write. Write several MRs per function.

## 5. Differential testing and reference implementations

Differential testing runs the same input through two implementations and compares outputs (McKeeman, "Differential testing for software", 1998). Csmith used it to find more than 325 previously unknown bugs in GCC, LLVM and other C compilers by compiling random programs with several compilers and comparing results (Yang, Chen, Eide and Regehr, PLDI 2011). Evidence: strong.

Pairs that work:

- **Old version vs new version** for refactors, rewrites, performance work and dependency upgrades. The git worktree recipe is in `~/.claude/skills/kwx-developer/ai-agents/tests-and-honesty.md` section 7. Every difference is either an intended change (list it) or a bug.
- **Fast vs obvious.** An optimized function against a slow, obviously correct version (a nested loop, a brute force search, a SQL query against an in memory filter). This is Hughes' model based property and Wlaschin's "test oracle" pattern.
- **Your code vs an established library** for formats you parse or produce (your date parser vs `Temporal` or `chrono`; your CSV writer vs a CSV reader reading it back).
- **Two platforms.** The same shared logic on Android and in Node; the same query on local Supabase and production shaped data.

A reference implementation counts as an independent oracle only when it uses a different method from the code (exact rationals or Python Fraction against integer cents, a table lookup against a formula, a different library), or when at least 5 values come from an outside source (published tables, a statute's worked examples, a calculator run by the owner). The test file header names the method difference and the anchors. Trial: web A's oracle shared the code's BigInt cents arithmetic; the published lohn-info.de and finanz-tools.de values are what made it trustworthy.

Normalize before comparing: sort unordered collections, round floats to the precision the spec cares about, strip timestamps and ids. Otherwise every run differs and the oracle is noise.

## 6. Round trips, idempotence and golden files

- **Round trip ("there and back again"):** `decode(encode(x)) == x`, `parse(print(ast)) == ast`, export then import gives the same data, serialize to storage then load gives the same object. Cheap and strong for formats and persistence.
- **Idempotence:** `f(f(x)) == f(x)` for normalizers, formatters, migrations, retries and "save" operations. Running a migration twice or replaying a sync batch must not change the result.
- **Golden files:** the expected output stored on disk, approved by a person. The oracle is exactly as good as the review of the first version and of every change. Rules are in `snapshot-and-golden-tests.md`.

## 7. When there is no spec

Many tasks arrive as "add a timer screen" with no rules. Do not invent the rules silently, and do not read them off the implementation.

1. **List what you would need to know** to write expected values: limits, rounding, empty states, error messages, what happens on conflict, on offline, on invalid input.
2. **Ask the user** the questions that change a high risk outcome. Ask them together, with a proposed default for each, so the user can answer "yes to all" in one line:

```text
Before I write the tests for the timer, three things the spec does not say:
1. Does time keep running when the app is in the background? (I assume yes, measured from the start time.)
2. Can a finished timer be resumed, or only reset? (I assume only reset.)
3. Minimum interval length? (I assume 1 second; 0 is rejected.)
```

3. **If you cannot wait, write the assumption down** and make it visible in three places: the assumptions list of the test plan, the test name, and a comment with an id.

```ts
// Assumption A2 (unconfirmed): a finished timer cannot be resumed, only reset.
it("ignores resume after finishing [assumption A2]", ...);
```

4. **Use consistency oracles** where the user cannot be asked: the product's own behaviour elsewhere (how another screen handles the same case), the platform convention (Android back button behaviour), comparable products, and what the user plausibly expects. Name the oracle in the test comment ("consistent with the history screen, which shows 'No workouts yet'").
5. **Characterization tests are allowed only for legacy refactors.** If the task is to refactor code with no spec, pin the current behaviour first, name the tests `characterization_*` or put them in a `characterization` describe block, and say in the report that they pin behaviour, not correctness. Never present current behaviour as the spec.
6. **Report the open assumptions** at the end. An unconfirmed assumption is an open risk.

## 8. Implicit oracles: crashes, hangs, logs, accessibility

Some failures need no expected value: a crash, an unhandled promise rejection, a Rust panic, a timeout, a memory blow up, an error logged to the console, a React key warning, an accessibility violation, a failing type check. Make these fail the test automatically:

- Fail Vitest or Jest runs on console errors and unhandled rejections (a `setupFiles` hook that throws on `console.error`, or `vitest-fail-on-console`).
- MSW with `onUnhandledRequest: "error"` turns an unexpected network call into a failure.
- In Rust, a property test of "never panics on any input" and `cargo fuzz` for parsers.
- In Playwright, listen to `page.on("pageerror")` and fail the test (when browser tests are allowed to run).

Implicit oracles are the main oracle of fuzzing, and they find real bugs at scale, but they say nothing about whether a non crashing output is right.

## 9. Oracle mistakes

| Mistake | Why it is wrong | Fix |
|---|---|---|
| Expected value computed by the code under test or a copy of it | The test agrees with the bug | Literal from the spec, or an independent model |
| "No exception" as the only check | Passes on wrong answers | Assert the result |
| Asserting only that a mock was called | Checks the test's own wiring | Assert the state or the output (`test-doubles.md`) |
| Loose matcher (`toBeTruthy`, `contains`) where an exact value is known | Accepts many wrong values | Exact match, or a matcher plus a key field |
| Snapshot accepted without reading | The bug becomes the oracle | Review rules in `snapshot-and-golden-tests.md` |
| Expected value copied from the current output of new code | Same as above | Derive it from the spec before running |
| Comparing unnormalized outputs in differential tests | Noise hides real differences | Sort, round, redact first |
| Floating point compared with `==` | Fails or passes by luck | Compare within a tolerance the spec states; money in integer minor units |

## 10. Checks

| Check | Pass condition |
|---|---|
| Every test has a named oracle | Exact value, model, relation, invariant, golden file or implicit, stated in the test or plan |
| Exact values are literals | No expected value computed by the code under test |
| Source quoted | Specified oracles cite the spec line or acceptance criterion |
| Partial oracles paired | Invariant only tests are paired with an exact value, model or metamorphic relation |
| No spec handled | Questions asked with defaults; unconfirmed assumptions in the plan, test names and the report |
| Characterization labelled | Tests pinning current behaviour are named as such |
| Implicit oracles armed | Console errors, unhandled rejections and unhandled network requests fail the suite |
| Differential runs normalized | Unordered data sorted, timestamps redacted, floats rounded before comparing |
| Cross-surface consistency | Each quantity shown on more than one surface (UI, CSV, PDF, API) has one test with a rounding sensitive fixture asserting all surfaces agree to the cent, or a spec line allowing the difference |
| Reference implementation independent | A second implementation uses a different method or is anchored to at least 5 outside values, and the test file header names which |
