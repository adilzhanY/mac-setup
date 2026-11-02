# Test design techniques

How to turn a spec into a small set of test cases that still finds the bugs: equivalence partitioning, boundary value analysis, decision tables, state transition testing, pairwise and combinatorial testing, cause and effect, error guessing, use case and journey tests, and CRUD matrices. Each technique has a "use when", the steps, and a worked example on a feature like the ones the owner builds. The definitions follow the ISTQB Foundation syllabus 4.0.1 and the ISTQB boundary value white paper; the worked examples are new.

## Contents

1. Picking a technique
2. Equivalence partitioning
3. Boundary value analysis (2 value and 3 value)
4. Worked example: a signup form
5. Decision tables (and cause and effect)
6. Worked example: a pricing page with monthly, yearly and lifetime plans
7. State transition testing
8. Worked example: a workout timer
9. CRUD matrices and the Supabase RLS matrix
10. Pairwise and combinatorial testing
11. Worked example: a sync conflict
12. Use case and user journey tests
13. Error guessing and fault attacks
14. Writing the cases down
15. Checks

## 1. Picking a technique

| The spec contains | Technique | Coverage item |
|---|---|---|
| An input with ranges or categories (age, length, amount, file type) | Equivalence partitioning, then boundary values for ordered partitions | Each partition; each boundary value and its neighbours |
| Rules that combine conditions ("students get 50% off, except on lifetime") | Decision table | Each feasible column (rule) |
| A lifecycle or modes (idle, running, paused) | State transition table | Each valid transition, then each invalid transition |
| Many independent options (plan x payment x currency x platform) | Pairwise (or 3 wise for high risk) | Each pair of values |
| Data with owners and roles (rows, files, posts) | CRUD matrix | Each entity x operation x role cell |
| A goal a user reaches in several steps | Use case and journey tests | Main path and each extension |
| Experience of how things fail | Error guessing, fault attacks, checklists | Each item on the list |

Combine them. A form field gets partitions and boundaries; the form's submit rules get a decision table; the screen's modes get a state table; the whole flow gets one journey test. Evidence: moderate (ISTQB 4.2 to 4.4).

## 2. Equivalence partitioning

Split each input (and each output, if the spec defines output classes) into partitions whose values the software should treat the same way. Then one value per partition is enough to show that partition works (ISTQB 4.2.1).

Steps:

1. List each input. For each, list valid partitions and invalid partitions. Invalid includes wrong type, missing, empty, too long, and values the spec does not define.
2. Pick one representative per partition, not on a boundary (boundaries come next).
3. Test each invalid partition in its own test case, with all other inputs valid. Two invalid values in one case hide each other (the first rejection masks the second). ISTQB calls this defect masking.
4. Coverage: partitions exercised divided by partitions identified. For several inputs, the minimum is "each choice": every partition of every input appears in at least one case.

Rules:

- **Partition by behaviour, not by type.** "Integer" is not a partition. "1 to 50 seats, priced per seat" and "more than 50 seats, contact sales" are.
- **Output partitions find bugs too.** If the spec says prices show as "Free", "5 €/month" or "Contact us", each display class needs a case.
- **A partition you cannot name an expected result for is a spec gap.** Write it as an assumption (`test-oracles.md` section 7).

## 3. Boundary value analysis (2 value and 3 value)

Boundaries are where off by one errors live: `<` written for `<=`, a limit moved by one, or a check missing. Boundary value analysis applies to ordered partitions only. A boundary value is the minimum or maximum value of a partition (ISTQB 4.2.2).

| Variant | Coverage items per boundary value | Finds |
|---|---|---|
| 2 value (Myers, Craig) | The boundary value and its closest neighbour in the adjacent partition | A boundary moved by one |
| 3 value (Koomen) | The boundary value and both neighbours | Also a condition written as `==` instead of `<=` |

The ISTQB example: if `x <= 10` is wrongly written `x == 10`, the 2 value cases `10` and `11` both pass, but the 3 value case `9` fails.

Steps (ISTQB white paper by Hamburg and Roman):

1. Identify the domain (for a text field: its length, `0, 1, 2, ...`).
2. Find the partitions.
3. Find the boundary values of each partition (an open ended partition has one).
4. List the coverage items for the variant you use.
5. Take the union (items overlap between neighbouring partitions).
6. Write one test per item.

Use 3 value boundaries for risks scored 6 or more and for anything with money, time or permissions; 2 value elsewhere. The cost difference is a few cases.

Other boundaries to look for, beyond numeric limits: empty and one element collections, first and last item of a page, midnight, month end, February 29, DST changes, the moment a trial ends, the last second before a token expires, the maximum file size, the 255th and 256th character of a database column, `i32::MAX` and `u32` underflow.

Boundaries of a duration are 0 s, 1 s, 59 s, 60 s; an interval also gets start == stop.

## 4. Worked example: a signup form

Spec (from the issue):

- Email: required, valid address, unique (case insensitive).
- Password: 8 to 64 characters, at least one letter and one digit.
- Username: 3 to 20 characters, lowercase letters, digits and underscore, unique.
- Age: 16 or older (birth date entered).
- Terms checkbox must be ticked.

### Partitions

| Input | Valid partitions | Invalid partitions |
|---|---|---|
| Email | well formed, not used | empty; no `@`; no domain; already used; already used in other case (`Ana@x.test` vs `ana@x.test`) |
| Password length | 8 to 64 | 0; 1 to 7; 65 and more |
| Password content | letters and digits | letters only; digits only |
| Username length | 3 to 20 | 0 to 2; 21 and more |
| Username characters | `[a-z0-9_]` | uppercase; space; `-`; non Latin letters (`ә`, `й`); emoji |
| Age on signup day | 16 and more | under 16; birth date in the future; no date |
| Terms | ticked | not ticked |

### Boundaries (3 value, password length)

Partitions: `{0..7}` rejected, `{8..64}` accepted, `{65..}` rejected. Boundary values: 0, 7, 8, 64, 65. Coverage items: `0, 1, 6, 7, 8, 9, 63, 64, 65, 66`. Ten cases, each one a password of that length that otherwise meets the content rule.

Age is a date boundary: with a fixed clock at `2026-03-15`, birth dates `2010-03-15` (exactly 16, accepted), `2010-03-16` (one day short, rejected) and `2010-03-14` (accepted). Add a person born on `2008-02-29` checked on `2024-02-28` and `2024-02-29` if the product has any leap day rule; ask which day counts as the birthday in non leap years.

### What the cases look like

```ts
// Each invalid case changes one field; the rest come from validSignup().
it.each([
  ["7 characters", "abcdef1"],
  ["65 characters", "a1".repeat(32) + "b"],
  ["letters only", "abcdefgh"],
  ["digits only", "12345678"],
])("rejects a password with %s", async (_, password) => {
  const res = await signup(validSignup({ password }));
  expect(res).toEqual({ ok: false, field: "password", code: "PASSWORD_RULES" });
});
```

### Error guessing on top

From the edge case catalogue in the exploratory folder: leading and trailing spaces in email (trimmed or rejected? ask), plus addressing (`ana+test@x.test`), an email that is unique only in case, a username that only differs by a Cyrillic look alike letter, a password with emoji (are they counted as one character or two UTF-16 units?), double submit, submit while offline, pasting a password with a trailing newline.

## 5. Decision tables (and cause and effect)

Use a decision table when the outcome depends on a combination of conditions (ISTQB 4.2.3). Rows are conditions and actions; each column is a rule: one combination of condition values and the actions that follow.

Steps:

1. List conditions (inputs that change the outcome) and actions (outcomes).
2. For boolean conditions, a full table has 2^n columns. Write them all, then mark infeasible combinations `N/A` and merge columns where a condition does not matter (`-`).
3. Every remaining feasible column is a test case.
4. Look at the table for gaps (a column with no defined action) and contradictions (two rules for the same combination). Those are spec bugs; send them to the user before testing.

Cause and effect graphing (Myers) draws causes and effects as a boolean graph and derives the decision table from it. It is useful when rules are written as prose with "and", "or", "unless". In practice, write the decision table directly; draw the graph only if the rules are too tangled to tabulate.

If the table has too many columns (more than about 16), split the conditions into independent groups, test one table per group, and cover cross group interactions with pairwise (section 10).

## 6. Worked example: a pricing page with monthly, yearly and lifetime plans

Spec:

- Monthly 5 €, yearly 50 € (two months free), lifetime 150 € once.
- Students get 50% off monthly and yearly. Lifetime has no student discount.
- A coupon gives 20% off the first payment of any plan. Coupons do not stack with the student discount; the bigger discount wins.
- Users with an active lifetime licence cannot buy another plan.

### Decision table

| Conditions | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 |
|---|---|---|---|---|---|---|---|---|
| Has lifetime already | T | F | F | F | F | F | F | F |
| Plan | - | monthly/yearly | monthly/yearly | monthly/yearly | monthly/yearly | lifetime | lifetime | lifetime |
| Student | - | F | T | F | T | F | T | T |
| Coupon | - | F | F | T | T | F | F | T |
| **Actions** | | | | | | | | |
| Purchase blocked | X | | | | | | | |
| Price | | list | 50% | 80% first payment | 50% (bigger wins) | 150 € | 150 € | 120 € (coupon only) |

Eight rules, eight tests per billing period where the plan column says "monthly/yearly" (or one test each if a property covers the period, see below). The table already found two questions for the owner: does "the bigger discount wins" apply to every payment or only the first one (R5: 50% recurring beats 20% first payment, but over a year the coupon is never better)? And can a student apply a coupon to lifetime (R8)?

### Properties that cover the rest

Once the table is tested, properties pin relations the table does not state. Verified with fast-check 4.10.2 and Vitest 5.0.5:

```ts
it("yearly is never more than 12 monthly payments", () => {
  fc.assert(fc.property(fc.boolean(), fc.integer({ min: 1, max: 50 }), (student, seats) =>
    price({ plan: "yearly", student, seats }) <= 12 * price({ plan: "monthly", student, seats })));
});
it("price scales linearly with seats", () => {
  fc.assert(fc.property(fc.constantFrom("monthly", "yearly", "lifetime"), fc.boolean(),
    fc.integer({ min: 1, max: 50 }), (plan, student, seats) =>
      price({ plan, student, seats }) === seats * price({ plan, student })));
});
```

The seat count (1 to 50) gets its own 3 value boundary cases: `0, 1, 2, 49, 50, 51`, plus a non integer (`1.5`). A mutation run on this exact module (`mutation-testing.md` section 6) then showed that no test covered an unknown plan name: the spec cases alone missed an invalid partition.

## 7. State transition testing

Use it when behaviour depends on what happened before: modes, lifecycles, sessions, wizards, players, timers, sync states (ISTQB 4.2.4).

1. Draw or list the states and events. Label transitions `event [guard] / action`.
2. Write the state table: rows are states, columns are events, cells hold the target state. An empty cell is an invalid transition. The table shows invalid transitions, which a diagram hides.
3. Pick the coverage:
   - **All states**: weakest, every state visited.
   - **Valid transitions (0 switch)**: every arrow taken once. The usual default.
   - **All transitions**: every valid transition plus an attempt at every invalid one, one invalid event per test (to avoid masking). ISTQB says this should be the minimum for mission and safety critical software. Use it for score 6 to 9 risks.
   - **1 switch**: every pair of consecutive transitions. Use it where history matters (pause then resume, offline then online).
4. For each test, assert the state after every event and the action (sound, notification, saved row), not only the final state.
5. When the machine is large or sequences matter, write a model based property test instead of picking sequences by hand (`property-based-testing.md` section 7).

For any flow that shows a preview and then commits (invoice preview and issue, checkout summary and pay, import preview and apply), add a case where the data changes between preview and confirm (add an entry, edit the rate, delete an item). Expected: the commit refuses with a clear message, or commits exactly the confirmed preview; it never silently commits different numbers.

## 8. Worked example: a workout timer

Spec: a timer for one interval of N seconds. Start, pause, resume, reset. When the time runs out it beeps and shows "Done". While paused, no time passes.

### State table

| State \ Event | start | pause | resume | tick (1 s passes) | reset |
|---|---|---|---|---|---|
| idle | running | (invalid) | (invalid) | (ignored) | idle |
| running | (invalid) | paused | (invalid) | running, or finished when left reaches 0 / beep | idle |
| paused | (invalid) | (invalid) | running | (ignored, left unchanged) | idle |
| finished | (invalid) | (invalid) | (invalid) | (ignored) | idle |

### Cases

- Valid transitions (0 switch): 9 arrows, coverable in about 4 sequences, for example `start, tick, pause, resume, tick x N (finished, beep), reset`.
- Invalid transitions: 9 cells, one test each: `resume` from idle does nothing and leaves `left` unchanged, and so on.
- 1 switch where history matters: `pause, resume, pause, resume` keeps `left` exact; `pause` then `tick` x 60 then `resume` keeps `left` the same as before the pause.
- Boundaries: N = 1 (one tick finishes), N = 0 (should be impossible; is it rejected?), the tick that takes `left` from 1 to 0 (beep exactly once).

### Error guessing for a mobile timer

The table is the spec; real timers fail on events the spec forgot. Add these as states or events and ask the owner what should happen: app goes to background while running (does time keep passing? it must, measured from a monotonic clock, not by counting ticks); phone locks; incoming call; the OS kills the app and restores it; the device clock changes (time zone, manual change, DST); two taps on start within 50 ms. A timer that counts ticks instead of comparing against a start timestamp drifts and freezes in the background.

The model based version of this test, verified with fast-check 4.10.2, found a planted bug (resume allowed from idle) and shrank it to the two step sequence `[N=1, resume]` (`property-based-testing.md` section 7).

## 9. CRUD matrices and the Supabase RLS matrix

A CRUD matrix lists entities against create, read, update and delete, and fills each cell with who may do it. As a test design it does two jobs: it shows operations nobody specified (a delete that exists in the API but not in the spec), and it turns permission rules into a complete list of cases.

For a Supabase table, add the role dimension. Example: table `workouts` (owner `user_id`), roles `anon`, `authenticated` owner, `authenticated` other user, `service_role`.

| Operation | anon | owner | other user | service_role |
|---|---|---|---|---|
| select own rows | deny (0 rows) | allow | deny (0 rows) | allow |
| insert with `user_id = auth.uid()` | deny | allow | n/a | allow |
| insert with someone else's `user_id` | deny | deny | deny | allow |
| update own row | deny | allow | deny (0 rows updated) | allow |
| update to change `user_id` to another user | deny | deny | deny | allow |
| delete own row | deny | allow | deny (0 rows deleted) | allow |

Every cell is a test. Note the RLS specific oracle: a denied `select`, `update` or `delete` usually returns zero rows, not an error, so assert the row count and then check the row is unchanged with the service role. A test that only checks "no error" passes on a hole. Run these as pgTAP tests (`supabase test db`) or through supabase-js clients signed in as two different test users against the local stack. See the backend folder of this skill for the setup.

## 10. Pairwise and combinatorial testing

When several independent parameters each take a few values, testing all combinations explodes (4 parameters with 3 values each: 81 cases). Most failures are triggered by a single parameter or by the interaction of two; NIST's studies across several domains found that 4 way to 6 way coverage detected all faults that exhaustive testing found (NIST combinatorial testing project, Kuhn, Wallace and Gallo 2004). Evidence: strong for the interaction rule, with the caveat that the parameters and values must be chosen well.

Pairwise (2 way) testing picks a small set of cases in which every pair of values appears at least once. Bach and Schroeder ("Pairwise testing: a best practice that isn't", 2004) warn that it only helps if the parameters really are independent and the values are well partitioned; it does not replace thinking about which combinations matter. So: do partitions first, decision tables for known interacting rules, and pairwise for the remaining configuration space.

Tools:

- **allpairspy** (Python, `uv run --with allpairspy`). Verified with allpairspy 2.5.1:

```python
from allpairspy import AllPairs

parameters = [
    ["monthly", "yearly", "lifetime"],   # plan
    ["none", "student", "coupon"],       # discount
    ["card", "paypal", "apple_pay"],     # payment
    ["EUR", "USD", "KZT"],               # currency
]

def valid(row):  # lifetime has no student discount
    return not (len(row) > 1 and row[0] == "lifetime" and row[1] == "student")

for i, row in enumerate(AllPairs(parameters, filter_func=valid), 1):
    print(i, *row)
# 9 rows instead of 81
```

The filter receives partial rows while the generator builds them, hence the `len(row)` check.

- **PICT** (Microsoft, C++ CLI, `pict model.txt /o:3 > suite.tsv`). Model file from the PICT docs:

```text
Plan:     monthly, yearly, lifetime
Discount: none, student, coupon
Payment:  card, paypal, apple_pay
Currency: EUR, USD, KZT, ~XXX

IF [Plan] = "lifetime" THEN [Discount] <> "student";
```

`~XXX` marks an invalid value; PICT puts each invalid value in exactly one case with otherwise valid values. `/o:3` asks for all triples, for high risk configuration. Not verified here (PICT is not packaged on Arch; build from github.com/microsoft/pict).

- **NIST ACTS** for larger t way suites (Java, free on request from NIST).

Use 2 way by default, 3 way for score 6 to 9 risks. Always add the specific combinations the decision tables and bug history name; generated suites do not know your past bugs.

## 11. Worked example: a sync conflict

Spec (offline first app): each record keeps `updated_at` and `device_id`. On sync, if only one side changed, take it. If both changed, the later `updated_at` wins. A delete beats an edit made before the delete. Same timestamp: not specified.

### Decision table

| Conditions | R1 | R2 | R3 | R4 | R5 | R6 | R7 |
|---|---|---|---|---|---|---|---|
| Local changed | F | T | F | T | T | T (delete) | T |
| Remote changed | F | F | T | T | T | T (edit) | T |
| Local newer | - | - | - | T | F | delete newer | equal timestamps |
| **Result** | no change | push local | pull remote | local wins | remote wins | deleted | ? (spec gap) |

R7 is a spec gap: ask the owner. A property test of the merge function (commutative, idempotent, associative) found the gap concretely: with a "later timestamp, then device id" tie break, two edits from the same device at the same millisecond merge differently depending on argument order (Hypothesis 6.170.14 counterexample `a=(0, 'phone', ''), b=(0, 'phone', '0')`, see `property-based-testing.md` section 8). Each device must then pick a different winner, and the devices never converge.

Add state transition cases for the sync engine itself (offline, syncing, conflict, synced, error) and error guessing: sync interrupted halfway, clock skew between devices (one phone set 5 minutes ahead), the same record edited on three devices, a record created offline on two devices with the same natural key.

## 12. Use case and user journey tests

A use case has a main success scenario and extensions (alternatives and errors) (Cockburn style). Each scenario is a test case; the main path becomes an end to end journey test, the extensions mostly become lower level tests.

Example: "Log a workout" main path: open app, tap start, finish timer, save, see it in history. Extensions: no network at save (saved locally, synced later), app killed during the workout (restored), storage full, user not signed in.

Rules:

- One journey test per core user goal (sign up, log in, the core action, pay, restore after reinstall). 5 to 15 for an app.
- A journey asserts what the user sees and what was stored, at the end and at the key steps.
- Push extensions down: "no network at save" is a screen or service test with the network mocked, not another device flow.
- Journey tests are the slowest and flakiest; see the user's rules (`strategy.md` section 3) before running device or browser journeys.

## 13. Error guessing and fault attacks

Error guessing uses knowledge of how software usually fails: input not accepted, wrong output format, missing cases, wrong operator, wrong computation, interface mismatches, bad initialization (ISTQB 4.4.1). A fault attack is the systematic form: keep a list of failure types and design one test per item (Whittaker).

- Use the edge case catalogue and the attacks in the exploratory folder of this skill (`exploratory/edge-case-catalogue.md`, `exploratory/heuristics.md`) as the list.
- Add the project's own bug history: every escaped bug becomes a line on the list and a regression test.
- Error guessing comes after the systematic techniques, not instead of them. It finds what the spec forgot; the techniques find what the spec says.

## 14. Writing the cases down

Keep it light. A table in the test plan or as a comment above a table driven test is enough:

```ts
// Password length, 3 value BVA. Partitions: 0..7 reject, 8..64 accept, 65.. reject.
it.each([
  [0, false], [1, false], [6, false], [7, false],
  [8, true], [9, true], [63, true], [64, true],
  [65, false], [66, false],
])("password of length %i accepted=%s", ...);
```

Name each test after the condition and the expected result, so the test list reads as the spec. Put the technique name in a comment so a reviewer can check the coverage items are complete.

## 15. Checks

| Check | Pass condition |
|---|---|
| Technique per condition | Every input range, rule set, lifecycle, option matrix and permission rule has a named technique |
| Invalid partitions | Each invalid partition has its own case, with all other inputs valid |
| Boundaries | Ordered partitions have boundary cases; 3 value for money, time, permissions and high risks |
| Durations and intervals | Durations tried at 0 s, 1 s, 59 s, 60 s; every interval has a start == stop case |
| Preview then confirm | Every preview and commit flow has a case where the data changes between the two steps; the commit refuses or commits exactly the preview |
| Decision tables | Feasible columns all tested; gaps and contradictions sent to the user as questions |
| State tables | Valid transitions covered; invalid transitions attempted for high risks, one per test; state asserted after each event |
| CRUD and roles | Every entity x operation x role cell has a test; denied operations assert row counts, not just "no error" |
| Pairwise | Parameters are independent and partitioned first; known risky combinations added by hand |
| Journeys | One per core goal; extensions pushed to lower levels |
| Error guessing | Catalogue and bug history consulted after the systematic cases |
| Spec gaps | Every case without a known expected result is an assumption or a question, not a guess |
