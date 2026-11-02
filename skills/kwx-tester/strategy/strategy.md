# Test strategy: what to test, how much, and how

Read this file first for any testing task bigger than one function: a new feature, a release, an audit of a test suite, or the question "how should we test this project?". It decides where the effort goes (risk), which kinds of tests carry the load for each type of project (the mix), and what a one page test plan looks like. The other files in this folder hold the techniques: how to design cases, how to know the right answer, doubles, data, properties, mutation, snapshots and flaky tests.

This folder goes deeper than kwx-developer and does not repeat it. For test layout, naming, the default mock table, Postgres per test, Playwright and Maestro basics, read `~/.claude/skills/kwx-developer/reliability/testing-strategy.md`. For never weakening a test and the honest report, read `~/.claude/skills/kwx-developer/ai-agents/tests-and-honesty.md`. For Rust test mechanics, read `~/.claude/skills/kwx-developer/languages/rust/testing.md`.

## Contents

1. Files in this folder
2. The rules that matter most
3. Before you start: the user's rules
4. Test from the spec, not from the code
5. Risk based testing: where the effort goes
5a. Effort tiers
6. How much is enough: exit criteria tied to risks
7. The mix per project type
8. Test sizes and what "unit" means
9. The one page test plan
10. Checks

## 1. Files in this folder

| File | Read when |
|---|---|
| `test-design-techniques.md` | Turning a spec into test cases: forms, ranges, business rules, lifecycles, config matrices, journeys, permissions. Worked examples: signup form, workout timer, pricing page, sync conflict, Supabase RLS matrix |
| `test-oracles.md` | You do not know what the right answer is, the spec is missing or vague, or the output is too big to check by hand. Invariants, metamorphic and differential testing, round trips, golden files |
| `test-doubles.md` | Deciding what to fake, stub or mock; a test that only checks a mock; keeping a fake honest against the real thing |
| `test-data-and-fixtures.md` | Building test data (builders, factories, mothers), seeded random data, realistic data, production data rules, cleanup and isolation |
| `property-based-testing.md` | Code with a rule that holds for all inputs (parsers, money, sync, merges) or with state (timers, carts, editors). Finding properties, shrinking, model based tests |
| `mutation-testing.md` | Checking whether tests would notice a wrong answer; high risk code; auditing a suite with high coverage but low trust |
| `snapshot-and-golden-tests.md` | Large outputs (CLI output, generated code, TUI frames, error reports); reviewing snapshot diffs; a suite where people press "update all" |
| `flaky-tests.md` | A test that passes and fails on the same code; setting up detection, quarantine and fixes |

## 2. The rules that matter most

1. **Read the user's rules before planning any test run.** Some environments forbid launching browsers, emulators or GUI apps, or injecting input. Plan around them (section 3). Evidence: house rule.
2. **Derive test cases from the spec before reading the implementation.** Write the list of conditions and expected results first, then look at the code only to find extra risks. Tests copied from the code repeat its mistakes. Evidence: moderate (ISTQB CTFL 4.0 test basis; Meszaros "tests as documentation").
3. **When the spec is silent, ask; if you cannot wait, write the assumption down** in the test name and in the plan, so it can be changed in one place (`test-oracles.md` section 7). Evidence: opinion.
4. **Spend effort by risk: likelihood times impact, with impact measured in what breaks for users.** Data loss, money, privacy and a blocked core journey come first; cosmetic issues last (section 5). Evidence: moderate (ISTQB 5.2).
5. **Write a one page test plan for any feature bigger than a function** and show it before writing many tests (section 9). Evidence: moderate (ISTQB 5.1); length is opinion.
6. **Choose the mix from the project type, not from a favourite shape.** Pure logic gets many small tests; a backend gets mostly integration tests against a real database; an app gets few end to end journeys (section 7). Evidence: moderate (Fowler 2021, Spotify 2018, Dodds).
7. **Name the technique for each input or rule.** Ranges get equivalence partitions and 3 value boundaries; rule combinations get a decision table; lifecycles get a state table; option matrices get pairwise (`test-design-techniques.md`). Evidence: strong for boundaries and combinations (ISTQB, NIST combinatorial studies).
8. **State the oracle before running the test.** Every test has an exact expected value or a property. "It did not crash" is an oracle only for robustness tests (`test-oracles.md`). Evidence: moderate (Barr et al. 2015 survey).
9. **Prefer real collaborators; double only what is slow, nondeterministic or outside your control,** and keep every fake under a contract test (`test-doubles.md`). Evidence: moderate (SWE at Google ch. 13, Khorikov, Freeman and Pryce).
10. **Each test builds the data it needs with a builder or factory, and leaves nothing behind.** Random data is seeded and the seed is printed (`test-data-and-fixtures.md`). Evidence: moderate (Meszaros, Pryce).
11. **Use properties for rules over all inputs and a model for anything with state.** One model based test of a timer or a sync engine replaces dozens of hand written sequences (`property-based-testing.md`). Evidence: moderate (Hughes 2020 measurements).
12. **Judge test strength by mutation on the diff, not by coverage** for high risk code (`mutation-testing.md`). Evidence: strong (Google, Petrovic et al.).
13. **Treat a flaky test as a bug in the test or the product,** reproduce it with repeats and shuffled order, and never fix it with a sleep (`flaky-tests.md`). Evidence: strong (Luo et al. 2014).
14. **End with an honest exit report:** risks covered, tests run, what was not checked, and what the user must check by hand (section 6). Evidence: moderate.

## 3. Before you start: the user's rules

Read the user's global and project instructions (on Claude Code: `~/.claude/CLAUDE.md` and the project's `CLAUDE.md`) before you plan where tests run. Then apply them like this:

| If the rules say | Then |
|---|---|
| No browser automation by the agent | Write Playwright or other browser tests into the project, but do not run them. Ask the user for a yes, or let CI run them. Verify meanwhile with type check, build, unit and integration tests, `curl` against a production build, direct database queries |
| Never inject input into an emulator or phone | Write Maestro, Detox or Espresso flows, but do not run them locally without the user's yes, since they tap and type on the device. Never use `adb shell input` |
| One emulator only, never download another | Reuse the named emulator; never create an AVD or fetch a system image for a test |
| Never move the mouse or type for the user | Do not run GUI tests that take over the desktop. Run headless or offscreen where the toolkit allows it (for Qt: `QT_QPA_PLATFORM=offscreen`) and hand visual checks to the user |
| No em or en dashes, no watermarks | Applies to test names, fixtures, plans and reports too |

Visual and hands on checks always end up as a short checklist for the user at the end of the task: what to open, what to do, what they should see. Keep it under ten lines.

## 4. Test from the spec, not from the code

The test basis is whatever says what the software should do: the issue, the user story and its acceptance criteria, a design, a DECISIONS.md entry, an API schema, the user's message. Work in this order:

1. **Collect the basis.** Quote the lines you test against. If there is none, write the expected behaviour as a short list and ask the user to confirm it.
2. **List test conditions.** One line per rule, input range, state, or journey ("password shorter than 8 characters is rejected").
3. **Design cases with a named technique** (`test-design-techniques.md`) and an oracle (`test-oracles.md`).
4. **Then read the implementation** to find risks the spec does not show: a cache, a retry, a time zone conversion, a third party call, a hand rolled parser. Add cases for those. White box reading adds risks; it does not replace the spec cases (ISTQB 4.3.3: white box testing cannot find a requirement that was never implemented).
5. **Never take the current output as the expected value** unless the task is to pin legacy behaviour before a refactor. Then call the tests "characterization tests" in their names and the plan, so nobody mistakes them for a spec.

## 5. Risk based testing: where the effort goes

A risk is something that may go wrong, scored by likelihood and impact (ISTQB CTFL 4.0, section 5.2). Score both from 1 to 3 and multiply. Do it in a few minutes per feature, not as a ceremony.

### Impact: what breaks for the user

| Score | Impact | Examples in the owner's projects |
|---|---|---|
| 3 | Data loss or corruption, money taken wrongly, private data exposed, security hole, the core journey blocked for everyone | Sync overwrites a workout log; RLS lets user A read user B's rows; a lifetime purchase is charged monthly; a migration drops a column; a CLI deletes the wrong files |
| 2 | A feature is wrong but has a workaround, or fails for a group of users | Timer drifts 2 s per minute; wrong price shown but right price charged; one locale breaks the date picker; a TUI panics on a narrow terminal |
| 1 | Cosmetic or rare and harmless | Misaligned icon, a typo in a toast, slow animation |

### Likelihood: where bugs come from

Raise likelihood for: new or heavily changed code (churn), complex branching or arithmetic, time, dates, time zones and DST, concurrency and async ordering, sync and offline, parsing input from outside, third party APIs and SDK upgrades, code written fast or by an agent without tests, and modules with past bugs (defects cluster). Lower it for code that is old, simple, stable and already well tested.

### The risk register

Write it as a table in the test plan. The response says which level and technique covers the risk. Layer is where the failure would live: server, client data (stores, caches, sync, query hooks), client UI (rendered screens and their states), bridge (HTTP contract, Tauri or Electron IPC, a native module) or CLI. Tier is the effort tier from section 5a.

```text
| Risk                                          | L | I | Score | Layer       | Tier | Response                                              |
|-----------------------------------------------|---|---|-------|-------------|------|-------------------------------------------------------|
| Offline edit on two devices loses one edit    | 3 | 3 | 9     | client data | 1    | Property tests on merge; model based sync test; 1 E2E |
| RLS lets another user read workouts           | 2 | 3 | 6     | server      | 1    | CRUD x role matrix as pgTAP tests                     |
| Yearly price computed wrong for students      | 2 | 3 | 6     | server      | 1    | Decision table, unit tests; fault batch on pricing.ts |
| Booking button live while offline             | 2 | 2 | 4     | client UI   | 2    | Rendered test with netinfo offline                    |
| save_entry arguments renamed on one side      | 2 | 2 | 4     | bridge      | 2    | Name diff plus one get_ipc_response test per command  |
| Timer keeps counting while paused             | 2 | 2 | 4     | client data | 2    | State transition tests, model based test              |
| Settings screen layout on small phones        | 2 | 1 | 2     | client UI   | 3    | Hand check by the user (checklist)                    |
```

Rules for the register:

- Scores 6 to 9: tests at the lowest level that can catch the failure, plus one journey test that proves the wiring, plus mutation testing on the changed code.
- Scores 3 to 4: equivalence partitions and boundaries at unit or integration level.
- Scores 1 to 2: a smoke test or nothing. Write "accepted risk" in the plan so the gap is visible.
- Revisit the register when a bug escapes: the bug proves the likelihood was higher than you thought.

### Balance across layers

Sum the risk score per layer before writing tests. A layer holding at least 25% of the total risk may not hold under 10% of the planned tests without a written reason. A suite that tests only the server is reported as client untested. The independent tester's brief names every layer it covers. The report gives tests per layer beside risk per layer.

Tests per risk, not per function: a pure calculation with an oracle (tax tariff, VAT, rounding) gets one differential or property test over the full input range plus named boundary cases instead of hundreds of examples; spend the saved budget on the riskiest untested layer (offline UI, auth throttling, restore, the bridge). Trial: web A wrote 223 unit tests and B 52 for tax engines both correct on every euro, while android A had 13 app tests against 128 server tests.

## 5a. Effort tiers

Every register row gets a tier. The tier scales the process; it does not change the rule that expected values come from the spec.

| Tier | Which risks | What it gets |
|---|---|---|
| 1 | Score 6 to 9, or any money, tax, invoices, dates and time zones, booking or capacity, auth, permissions, data loss, legal numbers, or a feature with more than about 15 ACs | Spec-first tests; one tester subagent (setup B in `../ai-agents/oracle-independence.md`) when the code exists; a planted fault batch of 10 to 15 on the module (`../ai-agents/proving-tests-work.md` section 4); an exploratory session |
| 2 | Score 3 to 4: business rules, UI states, offline, i18n | Spec-first tests by the main agent (setup A or C); a batch of 3 to 5 planted faults per module |
| 3 | Score 1 to 2: formatting, copy, cosmetic layout | One test or a human check line. The test still needs one proof (red before the fix, or a single planted fault or no-op), but no fault batch and no mutation run |

Repeats follow flake class, not tier (gate C2 in `../quality/quality-gate.md`, `flaky-tests.md`).

Subagent policy: one tester subagent per job. A second only for a separate Tier 1 area too big for one brief (about 60 cases). Never one to finish or lint another. The report says why one was or was not launched, and states the tier per test file.

Why: in the kwx trial (2026-11-01) arm A used 2.2 to 3.2 times the output tokens of the no-skills arm, and the value came from Tier 1 work (planted faults caught, real bugs found in money and validation code). Tiers keep that work and cut the rest.

## 6. How much is enough: exit criteria tied to risks

Coverage percentage is not an exit criterion; it shows untested code, not tested behaviour (SWE at Google ch. 11; Khorikov ch. 1: coverage is "a good negative indicator" but a bad positive one). Use these instead:

- Every risk scored 6 or more has a test that fails when the risk happens. Prove it: revert the fix or plant the bug, see red.
- Every acceptance criterion maps to at least one test (list the mapping in the plan).
- Changed high risk code has no unexplained surviving mutants.
- The suite passes three times in a row with shuffled order (no new flaky tests). New flake risk tests run 20 times, deterministic ones in one shuffled run plus 2 repeats (gate C2; `flaky-tests.md`: 78% of flaky tests are flaky from the day they were written).
- Everything not checked is listed in the report, with the reason.

Two measures that do help, from Google's "How Much Testing is Enough?" (Pirocanac, 2021): **behaviour coverage** (list the critical user journeys, the goal plus the steps a user takes to reach it, and check each has an end to end test) and **changed line coverage** (coverage of the lines this change added or edited, which matters more than the repository total). The same post lists the tiers beyond functional tests; check each against the risk register and route it to its folder in this skill when it applies: performance, load, fault tolerance (a dependency fails or is down), security, accessibility, localization, privacy, usability.

Feed escaped bugs back: every bug found after release gets a regression test at the lowest level that reproduces it, and a line in the risk register explaining why the plan missed it.

ISTQB also accepts "out of time" as an exit, if the stakeholder accepts the remaining risk. For a solo owner, that means: say plainly which risks are still open and let the owner decide.

## 7. The mix per project type

The shape names (pyramid, trophy, honeycomb) agree on more than they differ. Fowler (2021) points out that people mean different things by "unit" and "integration", and that the debate over percentages distracts from writing tests with clear boundaries that run fast and fail for useful reasons. Pick by where the logic and the risk live.

| Shape | Bulk of the tests | Fits when |
|---|---|---|
| Pyramid (Cohn; SWE at Google aims about 80% small, 15% medium, 5% large) | Many small tests of pure logic | Most of the risk is in computation inside one process: parsers, algorithms, domain rules |
| Trophy (Dodds) | Static checks at the base, then mostly integration tests that render or call several modules together | A frontend or full stack TypeScript app where the risk is in how pieces work together |
| Honeycomb (Spotify 2018) | Integration tests of one service through its real API and real database; few implementation detail tests; almost no tests that depend on other teams' systems | A backend or service whose complexity is in its boundaries, not inside |

Anti shapes to fix: the ice cream cone (mostly slow end to end tests, few fast ones) and the hourglass (many unit and end to end tests, few integration tests, usually because dependencies are hard to set up) (SWE at Google ch. 11).

### The owner's project types

| Project | Default mix | The tests that carry the load | Notes |
|---|---|---|---|
| Rust CLI or TUI | Pyramid | Pure core (parse, decide, compute) with unit and `proptest` tests; the binary through `assert_cmd` or `trycmd` with golden output; TUI frames rendered to ratatui's `TestBackend` and snapshotted with `insta` | Keep IO at the edges so the core is testable without mocks. Fuzz any parser of untrusted input |
| React Native / Expo app | Trophy plus a few device flows | `tsc --strict` and ESLint; React Native Testing Library screen tests with MSW at the network boundary; property tests for sync, money and date logic; 5 to 15 Maestro flows for core journeys on a release build | Native modules cannot run under Jest, so a double at the JS boundary of a native module is fine; the real module is covered by the device flows. Running device flows locally follows section 3 |
| Next.js or static site | Trophy | Types and lint; unit tests for logic (pricing, formatting, validation); route handler and server action tests with a real database where there is one; a few Playwright journeys; `next build` plus `curl` smoke tests on `next start` | A static site may need little more than build, link check, `curl` on key pages, and accessibility checks |
| Supabase backend | Honeycomb | SQL and RLS tests with pgTAP through `supabase test db` against the local stack; edge functions called over HTTP on the local stack; the role by operation matrix (`test-design-techniques.md` section 9) | Never mock the Supabase client in backend tests; the bugs live in policies, triggers and SQL. RLS is almost always a score 6 to 9 risk |
| Quickshell / QML desktop app | Pyramid for logic, hand checks for visuals | Logic moved into plain JS or C++ and tested headless (Qt Quick Test with `QT_QPA_PLATFORM=offscreen`, or Node for pure JS modules); services tested through their public functions; visual and interaction checks handed to the user | See the desktop folder of this skill for QML specifics. Do not drive the user's live desktop |
| Kotlin / Compose Android app | Pyramid | JUnit 5 and Kotest property tests for view models and domain logic; Compose UI tests for key screens; a few instrumented journeys | Prefer fakes of repositories over MockK mocks of your own classes |

## 8. Test sizes and what "unit" means

Use Google's size classes from kwx-developer (small: one process, no IO; medium: one machine, localhost services; large: anything). Sizes predict flakiness: in one week at Google 0.5% of small tests, 1.6% of medium tests and 14% of large tests were flaky (Listfield 2017). So:

- Write the smallest test that can catch the risk.
- When you say "unit test" in a plan, say what is real and what is doubled ("sociable: real repository against a test database" or "solitary: clock and HTTP doubled"). Fowler's sociable and solitary terms end most arguments about names.

## 9. The one page test plan

Write this before writing many tests, show it to the user for a feature of any size. When kwx-developer made a shared PLAN.md, the plan is its Test plan section, keyed by AC id, not a separate file. Otherwise keep it in the PR description or `docs/test-plans/<feature>.md` if the project keeps plans. ISTQB lists many more sections (stakeholders, budget, schedule); for a solo developer they add nothing. Keep it to one screen.

```markdown
# Test plan: <feature> (<date>)

Basis: <issue link / acceptance criteria / DECISIONS.md lines, quoted or linked>

## Scope
In: <behaviours and components under test>
Out of scope: <what is not tested and why> (for example: payment provider UI, older Android versions)

## Assumptions (to confirm)
- A1: <what the spec does not say and what the tests assume>

## Risks
| Risk | L | I | Score | Layer | Tier | Response (level + technique) |
|------|---|---|-------|-------|------|------------------------------|

## Levels and techniques
- Small: <modules, technique: EP + 3 value BVA, decision table ...>
- Medium: <integration targets, real DB, network mocked at ...>
- Large / journeys: <the 1 to 5 journeys>
- Properties / model: <rules and state machines>
- Mutation: <files>

## Environment and data
<local Supabase, seeded factories, fixed clock 2026-03-29T00:30:00Z (DST change), TZ=UTC ...>

## Entry criteria
- Builds, type check and lint pass; the feature is reachable; test data can be created.

## Exit criteria
- Every risk with score >= 6 has a test that was seen to fail without the fix.
- Every acceptance criterion maps to a test.
- No unexplained surviving mutants in <files>.
- Suite green 3 times with shuffled order; new flake risk tests green 20 times in a row, deterministic ones in one shuffled run plus 2 repeats.

## Handed to the user
- <visual or device checks, at most 10 lines>
```

## 10. Checks

| Check | Pass condition |
|---|---|
| User's rules read | The plan says where tests run and which runs need the user's yes |
| Spec first | Test conditions were listed from the basis before the implementation was read; the basis is quoted or linked |
| Assumptions visible | Every gap in the spec is an assumption line in the plan and in the test names |
| Risk register | Each risk has L, I, score and a response; scores 6+ have a lowest level test plus a journey |
| Tier and Layer columns | Every register row has a Layer and a Tier (section 5a); the report states the tier per test file |
| Layer balance | A layer with 25% or more of the risk score holds at least 10% of the tests, or a reason line says why; tests per layer are reported beside risk per layer |
| Mix fits the project | The bulk of tests sits where the project's logic and risk live (section 7) |
| Techniques named | Each input range, rule set, lifecycle and option matrix has a named technique |
| Oracles stated | No test passes on "no exception" unless it is a robustness test |
| Exit criteria met | Fail without fix seen for high risks; mutation clean on high risk diffs; shuffled runs green |
| Honest report | Ran, not checked, accepted risks and the user checklist are all present |
