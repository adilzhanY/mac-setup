# Flaky tests

A flaky test passes and fails on the same code. It costs twice: people stop trusting red builds, and the flake often hides a real bug in the product. This file gives the data on where flakiness comes from, how to detect it before and after merge, a quarantine policy, and fix patterns per cause, with commands for the owner's stacks.

kwx-developer has the policy summary (detect, quarantine in a day, fix in two weeks, no retries in unit tests) and a short cause table in `~/.claude/skills/kwx-developer/reliability/testing-strategy.md` section 11. This file adds the research behind it, detection techniques, and the fix patterns in code.

## Contents

1. What the data says
2. Causes, with numbers
3. Detecting flakiness
4. Reproducing one flaky test
5. Quarantine policy
6. Fix patterns per cause
7. Never fix with a sleep
8. Checks

## 1. What the data says

- **Google, 2016** (John Micco): about 1.5% of all test runs reported a flaky result, almost 16% of tests showed some flakiness, and 84% of pass to fail transitions in CI involved a flaky test (via kwx-developer). Google counts a test as flaky when it fails and then passes on one of up to 10 reruns of the same code (Luo et al. 2014, citing Google).
- **Google, 2017** (Jeff Listfield, "Where do our flaky tests come from?"): of about 4.2 million tests, around 63 000 had a flaky run in a week. Flakiness grew with test size: 0.5% of small, 1.6% of medium and 14% of large tests were flaky. Binary size and RAM use correlated strongly with flakiness (r² 0.82 and 0.76). Tests using WebDriver were flaky far more often: 10.45% (Java) and 18.72% (Python), against 1.65% for all tests. Some tools are used mostly in large tests, so size explains part of that.
- **Luo, Hariri, Eloussi and Marinov, "An Empirical Analysis of Flaky Tests"** (FSE 2014, 201 flaky test fixing commits in 51 open source projects; FSE 2024 test of time honourable mention): the top causes were async wait (45% of the classified fixes), concurrency (20%) and test order dependency (12%). 78% of flaky tests were flaky the first time they were written. 96% did not depend on the platform. 24% of the fixes changed the code under test, and 94% of those fixed a real bug in it.
- **Gruber, Lukasczyk, Kroiß and Fraser, "An Empirical Study of Flaky Tests in Python"** (ICST 2021, 22 352 projects, 876 186 tests, 7 571 flaky): 59% of flaky tests were order dependent and 28% came from test infrastructure problems; most of the rest involved network and randomness.

Evidence: strong. The lessons that drive the rules below: smaller tests flake less; most flakiness is in the test's handling of async and shared state, not in the platform; new tests are where flakiness is born; and a flaky test is a bug report about the product a quarter of the time.

## 2. Causes, with numbers

Luo et al. classified 161 of the commits by root cause:

| Cause | Commits | Typical form | Typical fix (share within the category) |
|---|---|---|---|
| Async wait | 74 (45%) | Test checks a result before the async work is done; fixed sleeps | Wait on the condition, `waitFor` style (57%); longer sleeps (27%, fragile) |
| Concurrency | 32 (20%) | Data races, atomicity violations, deadlocks between threads in test or code | Add locks (31%), make code deterministic (25%), change conditions (9%) |
| Test order dependency | 19 (12%) | A test relies on state another test left (static fields, files, DB rows, ports) | Clean shared state between tests (74%), remove the dependency (16%), merge tests (10%) |
| Resource leak | 11 | Unclosed connections, handles, threads exhaust a pool | Release resources; pool size 1 trick (section 6) |
| Network | 10 | Remote connection failures (60%), bad local socket handling (40%) | Do not call real remote services; random free ports |
| Time | 5 | Midnight in UTC, time zone, precision | Inject or fake the clock; `TZ=UTC` |
| IO | 4 | Files left over, shared paths | Unique temp dirs |
| Randomness | 4 | Unseeded random values, edge values like 0 | Seed; test the edge values explicitly |
| Floating point | 3 | Precision, overflow | Tolerances; integer minor units |
| Unordered collections | 1 | Assuming hash or set iteration order | Sort, or compare as sets |

Google's own list of flakiness sources (George Pirocanac, "Test Flakiness: One of the main challenges of automated testing", parts I and II, December 2020 and March 2021) groups them by where they live: the test (setup, cleanup, assumptions about data, time, order), the test framework (resources, scheduling collisions), the product and its dependencies (races, uninitialized variables, slow responses, leaks), and the OS, hardware and network. Hermetic environments, with everything the test needs and nothing external, flake less.

## 3. Detecting flakiness

### New tests: run them many times before merge

Since 78% of flaky tests are flaky from birth (Luo F.2), the cheapest detection is at birth. Before calling a new or changed test done, run it repeatedly, in isolation and in the suite, and in shuffled order. How many times follows the test's flake class (gate C2 in `../quality/quality-gate.md`): a test that touches I/O, a database, time or timers, concurrency, network, randomness or UI rendering runs 20 times plus one shuffled run; a deterministic test (pure function, fixed inputs, no I/O, no clock) runs in one shuffled suite run plus 2 repeats. The commands below show 20; use 2 for deterministic files:

| Stack | Repeat | Shuffle |
|---|---|---|
| Vitest | `npx vitest run src/x.test.ts --repeats 20` (verified flag, Vitest 5.0.5) | `npx vitest run --sequence.shuffle --sequence.seed=$RANDOM` (verified) |
| Jest | `for i in $(seq 20); do npx jest src/x.test.ts || break; done` | `npx jest --randomize --seed=$RANDOM` |
| Playwright (when allowed to run) | `npx playwright test e2e/x.spec.ts --repeat-each=20 --retries=0` | `--workers=4` to add parallel pressure |
| Rust | `for i in $(seq 20); do cargo test name -- --exact || break; done`; nextest `cargo nextest run --retries 0` repeated | Run with `--test-threads=1` and with the default parallelism; compare |
| pytest | `pytest --count=20 x_test.py` (pytest-repeat) | `pytest -p randomly` (pytest-randomly), `-p no:randomly` to compare |
| Kotlin / JUnit 5 | `@RepeatedTest(20)` while investigating | `junit.jupiter.testmethod.order.default=org.junit.jupiter.api.MethodOrderer$Random` |
| Maestro flows | Repeat only with the user's yes (they drive a device); see `strategy.md` section 3 | |

Shell loops in fish (the owner's shell) use `for i in (seq 20); cargo test name -- --exact; or break; end`.

### Existing suites: watch the history

- Make CI record tests that passed on retry (Playwright reports them as "flaky", nextest prints `FLAKY` when retries are on). A pass on retry is a flaky result, not a pass.
- Run the full suite shuffled on a schedule (nightly or weekly), with the seed in the log.
- Run each test alone and in the suite. A test that passes alone and fails in the suite is a victim of a polluter test; one that fails alone and passes in the suite depends on a setup another test does (Meszaros' "Lonely Test").
- Add stress: more parallel workers than cores, a slower CI machine, CPU load (`stress-ng --cpu 8` alongside, Linux). Timing bugs show up under load.
- Inject delay: Luo found 85% of async wait flaky tests involve one ordering and no external resource, so adding one delay in the right place in the code reproduces most of them (I.5). Put a temporary `await sleep(200)` in the async producer, not in the test, to see if the test really waits.

## 4. Reproducing one flaky test

1. **Measure the failure rate:** run it 50 times in isolation and 50 times in the suite. Record both ratios in the issue.
2. **Classify by symptom:**
   - Fails only in the suite: order dependency or shared state.
   - Fails more under load or on CI: async wait or concurrency.
   - Fails at certain times of day or dates: time.
   - Fails with different values each time: randomness or unordered collections.
   - Fails after many tests ran: resource leak.
3. **Capture evidence on failure:** seed, test order, logs, timestamps, Playwright trace. Turn on whatever the tool offers only on failure.
4. **Find the polluter for order dependency:** bisect the tests that ran before the victim (run victim alone with each half of the preceding tests).
5. **Read the product code, not only the test.** In Luo's data a quarter of fixes changed the product, almost always fixing a real bug: a missing await, a race between two saves, a timer that drifts under load.

## 5. Quarantine policy

Quarantine keeps the main suite trustworthy while the flaky test is fixed (Fowler, "Eradicating Non-Determinism in Tests").

1. **Quarantine the same day** the flakiness is confirmed: move the test out of the blocking suite with a marker and a link to an issue: `test.fixme("flaky: #123", ...)` or a `@flaky` tag in Playwright, `it.skip` with an issue link in Vitest or Jest, `#[ignore = "flaky: #123"]` in Rust.
2. **Keep running it** in a separate non blocking job (Playwright `--grep @flaky`, `cargo test -- --ignored`) so you collect failure data and notice when it is fixed. Fowler advises most teams to keep quarantined tests out of the main pipeline entirely.
3. **Cap the quarantine:** Fowler suggests a number limit (for example 8 tests) or a time limit (a week). For a solo developer: at most 5 tests or 2 weeks each. When the cap is reached, fixing comes before new features.
4. **Each quarantined test has an issue with:** failure ratio alone and in suite, suspected cause, seed or trace, and the date it entered quarantine.
5. **Fix or delete.** If the test is not worth fixing, delete it and write in the issue what risk is now uncovered. Luo's implication I.12: flaky tests should not simply be removed or disabled, because they can help uncover bugs; delete only after reading the product code.
6. **Retries are a report, not a fix.** Retries are tolerated only for end to end tests on CI, and a pass on retry still opens or updates a flaky issue (kwx-developer rule).

## 6. Fix patterns per cause

### Async wait: wait for the condition

```ts
// Bad: hopes 500 ms is enough on every machine.
await new Promise((r) => setTimeout(r, 500));
expect(store.status).toBe("synced");

// Good: waits for the condition, with a generous timeout.
await vi.waitFor(() => expect(store.status).toBe("synced"), { timeout: 5000 });
await expect.poll(() => store.status, { timeout: 5000 }).toBe("synced");
// Testing Library: await screen.findByText("Synced")
// Playwright: await expect(page.getByText("Synced")).toBeVisible()
```

Better still: make the code awaitable (return the promise, emit an event) so the test awaits completion directly. For timers, use fake timers (`vi.useFakeTimers()`, `vi.advanceTimersByTimeAsync(1000)`, `#[tokio::test(start_paused = true)]`) so waiting takes no real time.

### Concurrency: control the schedule

- JS async races: explore orderings with fast-check's `fc.scheduler()` (verified example in `property-based-testing.md` section 7), then fix the race in code (ignore stale responses, serialize writes).
- Rust: `loom` explores thread interleavings for small concurrent data structures; `tokio::time::pause` makes timing deterministic.
- Kotlin coroutines: `runTest` with a `StandardTestDispatcher` and `advanceUntilIdle()`.
- Do not fix a race in the test by adding a lock in the test. Find where the product races.

### Order dependency and shared state: fresh fixtures

- Each test builds its own data (`test-data-and-fixtures.md`). No data created by another test.
- Reset globals: `vi.resetModules()`, `vi.unstubAllEnvs()`, MSW `server.resetHandlers()`, `restoreMocks: true`, clear `localStorage` and `AsyncStorage` mocks, reset singletons through a test only reset function.
- Unique names for files, ports (`bind 127.0.0.1:0`), database rows and temp dirs.
- Make teardown failures loud, so a failed cleanup does not quietly poison the next test.

### Time

- Inject the clock and fix it; wrap the system clock behind one module so tests can replace it. Fowler suggests a lint or regex check that fails the build on direct clock calls outside that module (`rg -n "Date\.now\(\)|new Date\(\)" src --glob '!src/clock.ts'`).
- `TZ=UTC` in the test environment, plus explicit tests that set other zones (Almaty UTC+5, a DST zone) where the feature depends on local time.
- Never compare against "now" with zero tolerance.

### Randomness

Seed every random source and print the seed (`test-data-and-fixtures.md` section 6). Test the edge values the random generator rarely produces (0, empty, max) as explicit cases.

### Unordered collections

Sort before comparing, or compare as sets with a length check: `expect(new Set(ids)).toEqual(new Set(expected))`. In Rust, `HashMap` iteration order changes between runs by design; use `BTreeMap` for output, or sort. SQL without `ORDER BY` has no defined order: add one in the query if order matters to the product, or sort in the test if it does not.

### Resource leaks

Close everything in `afterEach` or with Rust guards. Fowler's trick: set the pool size to 1 and make it throw when empty in tests; the first test that leaks fails at once, instead of a random later test. Jest: `--detectOpenHandles`.

### Network and infrastructure

No real remote calls in tests (MSW `onUnhandledRequest: "error"`, `wiremock`). Containers started once per run with a readiness check, not a sleep. A smoke test at the start that fails fast if the local Supabase or database is not up, so infrastructure problems are not reported as test failures.

### Floating point

Compare within a tolerance the spec states (`toBeCloseTo(x, 2)`, `approx` crate), and keep money in integer minor units so there is nothing to tolerate.

## 7. Never fix with a sleep

In Luo's data, fixes with `waitFor` style waits used an average bound of 13.04 s, sleeps 1.52 s; the waits finish as soon as the condition holds and tolerate slow machines, while the sleeps are both slower on fast machines and too short on slow ones. 60% of sleep based fixes were increases of a sleep that was already there, which shows how they fail again. Google's guidance says the same: do not add arbitrary delays, they "can become flaky again over time and slow down the test unnecessarily" (Pirocanac, part II, 2021).

Rule: no fixed sleep in a test to wait for work to finish. A sleep is allowed only when time passing is the behaviour under test, and then with fake timers.

## 8. Checks

| Check | Pass condition |
|---|---|
| New tests repeated | Each new or changed flake risk test ran 20 times green, alone and in the suite; each deterministic test file ran in one shuffled suite run plus 2 repeats; the class is noted per file |
| Shuffled runs | The suite passes with shuffled order; seed logged |
| Retries reported | CI marks pass on retry as flaky; no retries configured for unit or integration tests |
| Quarantine | Each quarantined test has an issue with failure ratios, cause, date; quarantine under the cap |
| No sleeps | `rg -n "waitForTimeout|setTimeout\(r|sleep\(" --glob '*test*' --glob 'e2e/**'` finds only fake timer use or justified cases |
| Clock behind one module | Direct clock calls only in the clock module |
| Product code checked | Every fixed flaky test's report says whether the cause was in the test or the product |
