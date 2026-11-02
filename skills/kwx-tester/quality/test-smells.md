# Test smells

A test smell is a pattern in test code that makes a test lie, break for the wrong reason, or hide what it checks. This file is the catalogue the skill uses when it reviews tests (its own or a project's): for each smell, what it is, why it hurts, how to find it with a linter, a grep or the scan script below in JS/TS (Vitest, Jest, Playwright), Rust, Kotlin and Python, and how to fix it. It goes deeper than the principles in `~/.claude/skills/kwx-developer/reliability/testing-strategy.md` (T1 to T12, mocking, flaky policy) and does not repeat them.

## Contents

1. What the research says, and its limits
2. How to scan: linters first, then the script, then reading
3. Smells that make a test lie (fix first)
4. Smells that make a test break for the wrong reason
5. Smells that make a failure hard to read
6. Smells at suite level
7. Priority: what to fix, what to leave
8. Checks

## 1. What the research says, and its limits

- **Smells are everywhere.** Bavota et al. (EMSE 2015, abstract) found 86% of JUnit tests in open source and industrial systems had at least one smell. Peruma et al. (CASCON 2019) ran tsDetect on 656 open source Android apps (1,187,055 test methods): 97% of apps had smells, a test file had 3 smell types on average. Most common per file: Assertion Roulette 58%, Exception Handling 49%, Eager Test 39%, Magic Number 35%, Unknown Test (no assertion) 34%. Evidence: strong.
- **Some smells cost real money.** Spadini et al. (ICSME 2018, 221 releases of 10 systems, over a million tests): smelly tests are more change prone and more defect prone, and production code tested by smelly tests is more defect prone. Indirect Testing, Eager Test and Assertion Roulette were the strongest for change proneness. Bavota et al. measured comprehension about 30% better without smells. Evidence: strong.
- **But the detectors are blunt.** Panichella et al. ("Test smells 20 years later", EMSE 2022, abstract) hand labelled hundreds of suites: several smells were common in developer tests but "virtually never" tied to the problems developers care about, and an older detector misclassified over 70% of smells in generated suites. Developers in Peruma's survey agreed unanimously that empty tests and print statements should go, but disagreed on Conditional Test Logic and Magic Numbers. Evidence: strong.

What this means for the agent: a tool hit is a lead, not a finding. Open the test and decide whether it actually lies, breaks for the wrong reason, or hides intent. The smells in section 3 almost always matter; many in section 5 are taste.

## 2. How to scan: linters first, then the script, then reading

Run in this order and stop adding tools when the next one adds nothing.

**Step 1. The project's linters, with test rules on.** They parse code, so they have fewer false hits than grep.

| Stack | Plugin | Rules that catch smells |
|---|---|---|
| Vitest | `@vitest/eslint-plugin` | `expect-expect`, `no-conditional-in-test`, `no-conditional-expect`, `no-disabled-tests`, `no-focused-tests`, `no-commented-out-tests`, `no-identical-title`, `no-standalone-expect`, `valid-expect`, `valid-expect-in-promise`, `max-expects`, `no-large-snapshots`, `no-interpolation-in-snapshots`, `prefer-snapshot-hint`, `require-to-throw-message`, `no-test-return-statement`, `warn-todo` |
| Jest | `eslint-plugin-jest` | same names, prefix `jest/` |
| Playwright | `eslint-plugin-playwright` | `missing-playwright-await`, `no-wait-for-timeout`, `no-wait-for-selector`, `no-networkidle`, `no-force-option`, `no-element-handle`, `no-page-pause`, `no-skipped-test`, `no-focused-test`, `no-conditional-in-test`, `no-conditional-expect`, `prefer-web-first-assertions`, `no-raw-locators`, `no-nth-methods`, `no-magic-timeouts`, `expect-expect`, `require-annotation-reason` |
| Python | ruff `PT` (flake8-pytest-style) and `F` | `PT011` raises too broad, `PT012` raises block with many statements, `PT015` assert always false, `PT017` assert in except, `PT018` composite assertion, `F631` assert on a tuple (always true) |
| Rust | clippy | no test smell lints; use the script and the greps below |
| Kotlin | detekt | few test rules; use the script and the greps below |

Rule names were read from the plugin READMEs (2026-10). Run them without changing the repo: `npx -y eslint --rule '{"vitest/expect-expect":"error"}' ...` needs the plugin installed, so if the project does not have it, use the script instead and offer the plugin as a finding (kwx-developer `~/.claude/skills/kwx-developer/workflow/audit-and-ask.md`).

**Step 2. The scan script.** `scripts/smellscan.py` is a heuristic scanner for all four stacks, standard library only, verified on fixtures and on a 126 file Kotlin test suite (0.07 s). It reads files and never writes into the repo.

Run it:

```bash
python3 -I ~/.claude/skills/kwx-tester/scripts/smellscan.py src src-tauri tests e2e app/src/test   # paths that exist in the repo; Rust files with an inline #[cfg(test)] module are found too
# summary per flag
python3 -I ~/.claude/skills/kwx-tester/scripts/smellscan.py . | grep -oE 'EMPTY|NO-ASSERT|EAGER|SLEEP|BRANCH|PRINT|NET|SAME' | sort | uniq -c
python3 -I ~/.claude/skills/kwx-tester/scripts/smellscan.py --selftest   # proves every flag fires on built in fixtures
```

It prints one line per suspicious test, `path:line  name  FLAGS`, and exits 0. Open every hit and confirm it before it becomes a finding.

Flags: `EMPTY` (no statements), `NO-ASSERT` (no assertion, counting node:assert, t.assert, expect*/assert*/verify* calls, assertion helpers defined in any scanned file, and throw or panic! used as the check), `EAGER=k` (more than 5 distinct things checked: Eager Test), `SLEEP`, `BRANCH` (an assertion inside if/else/switch/match/when), `PRINT`, `NET` (a real host inside a network call), `SAME` (`assert_eq!(x, x)`, `expect(true).toBe(true)`).

Every NO-ASSERT and EMPTY hit is read. EAGER and BRANCH are P3 leads: count and group them, read them one by one only in Tier 1 code (../strategy/strategy.md section 5a). An if that only filters or collects mismatches is not flagged, and a loop that never runs is still not detected.

What the 1.1.0 rewrite taught (kwx trial, 2026-11-01): the old scanner gave 33, 20 and 55 hits on the three skill built apps, mostly false (node:assert and helper calls read as NO-ASSERT, any test with 6 expect calls on one row flagged as roulette, a URL in test data read as a network call). The rewrite gives 3, 1 and 7 and keeps the true positives on both arms (a Rust migration test that only calls `migrate` twice, an invoice test checking 9 different things, a sample writer with no assertion).

What the verification taught (real Kotlin suite): 4 `NO-ASSERT` hits, of which 2 were real "does not throw" smoke tests (they call every theme's colour builder and rely on an exception to fail). That is legal but weak, and the fix is a named assertion (section 3.2). An earlier version flagged every `for` loop: 256 hits, nearly all table driven tests that loop over data. Loops are not the smell; a branch that decides whether an assertion runs is. On a Rust workspace (unit tests in `src/`, 0.08 s) the one `NO-ASSERT` hit ended in `p.validate().unwrap()`: the test relies on `unwrap` panicking, the same "does not throw" pattern.

Known blind spots: it misses the unawaited promise assertion (The Liar, section 3.3), assertion helpers in files outside the scan (it flags `NO-ASSERT`; scan the helper folder too, or confirm by reading the helper), and braces inside strings can cut a JS, Rust or Kotlin body short.

**Step 3. Read.** For each hit: open the test, apply the definition, drop false hits silently, and group by pattern (one finding for "14 tests in `tests/api/` sleep 500 ms", not 14 findings).

## 3. Smells that make a test lie (fix first)

A lying test passes when the code is broken. It is worse than no test, because it creates trust. Evidence: strong for the general point (in Petrović et al. 2021, 1,502 high priority Google bugs sat in code already covered by tests, see `coverage.md`).

### 3.1 Empty test

A test with no statements, or only `pass`, `...` or comments. It always passes and counts in the test total. Common source: generated templates (Android Studio's `ExampleUnitTest`, Peruma's "Default Test"), and placeholders that were never written.

All four rg patterns below were verified on fixtures.

| Stack | Detect |
|---|---|
| JS/TS | script `EMPTY`; `rg -nU --pcre2 "\b(it|test)\(\s*['\"\x60][^'\"\x60]*['\"\x60]\s*,\s*(async\s*)?\([^)]*\)\s*=>\s*\{\s*\}"` |
| Rust | script `EMPTY`; `rg -nU '#\[test\]\s*fn \w+\(\)\s*\{\s*\}'` |
| Kotlin | script `EMPTY`; `rg -nU '@Test\s+fun [^(]+\(\)\s*\{\s*\}'`; files named `ExampleUnitTest.kt`, `ExampleInstrumentedTest.kt` |
| Python | script `EMPTY`; `rg -nU 'def test_\w+\([^)]*\):\s*\n\s+(pass|\.\.\.)\s*$'` |

Fix: write the test, or replace it with the runner's todo marker so it shows as pending, not passed: `it.todo('...')`, `#[ignore = "todo: #42"]`, `@Ignore("todo: #42")`, `pytest.skip("todo: #42")`. Delete Android template tests.

### 3.2 Unknown test (no assertion)

The test runs code but checks nothing. It passes unless the code throws. tsDetect calls it Unknown Test; 34% of Android test files had one.

| Stack | Detect |
|---|---|
| JS/TS | lint `expect-expect` (set `assertFunctionNames` for custom helpers like `expectValidUser`); script `NO-ASSERT` |
| Rust | script `NO-ASSERT`. A test returning `Result` and using `?` asserts only "no error" |
| Kotlin | script `NO-ASSERT` |
| Python | script `NO-ASSERT` |

Fix: assert on the result. If "does not throw" really is the behaviour, say so in the code so a reader and a linter can see it: `expect(() => build(theme)).not.toThrow()`, `assertDoesNotThrow { build(theme) }`, Rust `build(theme).expect("theme builds")` plus a comment, Python a plain call plus `assert result is not None` on something real.

### 3.3 The Liar

The test contains assertions, but they never run or never fail. The most dangerous smell because it looks fine in review.

| Stack | Pattern that lies | Detect | Fix |
|---|---|---|---|
| JS/TS | assertion in `.then()` or a callback, promise not awaited or returned: the test ends before the assertion runs | lint `valid-expect-in-promise`, `valid-expect`; `rg -n --pcre2 '^\s+(?!await|return)[\w.]+\([^;]*\)\.then\(' -g '*.test.*'` (verified) | `await expect(p).resolves.toBe(0)`; for callbacks `expect.assertions(1)` at the top |
| JS/TS | `try { await f() } catch (e) { expect(e)... }`: passes when `f` does not throw | lint `no-conditional-expect` | `await expect(f()).rejects.toThrow('msg')` |
| Playwright | `expect(locator).toBeVisible()` without `await`: never waits, never fails | lint `missing-playwright-await` | add `await` |
| Rust | `#[should_panic]` with no `expected`: any panic passes, including an unrelated `unwrap` | `rg -n '#\[should_panic\]'` | `#[should_panic(expected = "negative quantity")]`, or return `Result` and assert on the error |
| Rust | assertion in a spawned thread or task whose handle is dropped | `rg -n 'thread::spawn|tokio::spawn' tests` and read | `handle.join().unwrap()` / `.await.unwrap()` |
| Kotlin | `@Test(expected = Exception::class)`: any exception anywhere passes | `rg -n '@Test\(expected'` | `assertFailsWith<InvalidQty> { cart.add(-1) }` on the one call |
| Kotlin | JVM `assert()` is a no-op when assertions are disabled; Gradle enables them for tests by default, but check | `rg -n 'enableAssertions\s*=\s*false' -g '*.gradle*'` | use `assertEquals`/`assertTrue` from the test library |
| Python | `assert (x == 1, "msg")`: a non empty tuple is always true | ruff `F631` | `assert x == 1, "msg"` |
| Python | `async def test_...` without an async plugin: pytest skips it with a warning, it never runs | `rg -n 'async def test_'` plus check `pytest-asyncio`/`anyio` in deps | install the plugin, `asyncio_mode = "auto"`, and turn the warning into an error: `-W error::pytest.PytestUnhandledCoroutineWarning` |

### 3.4 Redundant assertion

An assertion whose expected and actual values are the same thing: `expect(true).toBe(true)`, `assert_eq!(x, x)`, `assertEquals(1, 1)`, `assert x == x`. Always passes. Often left over from a canary test or written to satisfy `expect-expect`. Detect: script `SAME`, ruff `PT015` for `assert False`-like cases. Fix: delete, or assert something real.

### 3.5 Swallowed exceptions (Exception Handling)

`try`/`catch` in a test that catches the failure and does nothing, or logs it. tsDetect's most common smell after Assertion Roulette (49% of files), because Java checked exceptions push people to wrap. Detect: JS `rg -n 'catch\s*\(' -g '*.test.*' -g '*.spec.*'`; Kotlin `rg -n 'catch\s*\(' app/src/test`; Python `rg -n '^\s+except' tests`; Rust `rg -n 'if let Err|\.ok\(\);|let _ = ' tests`. Fix: let it throw (the runner reports it), or assert on the error with the runner's API (`rejects`, `assertFailsWith`, `pytest.raises(..., match=...)`, `assert!(matches!(r, Err(Error::Invalid)))`).

### 3.6 Skipped, focused and todo tests left in

`it.only` silently disables the rest of the file. `skip`, `#[ignore]`, `@Ignore`, `xfail` hide a test forever unless someone has a reason and a date. Developers in Peruma's survey were split on ignored tests, so do not delete them blindly: ask.

```bash
# verified on fixtures and a real repo
rg -n --pcre2 '\b(it|test|describe)\.(skip|only|todo|fixme)\b|\.(skipIf|runIf)\(|\b(xit|xdescribe|fit|fdescribe)\(|#\[ignore|cfg_attr\([^)]*ignore|@Ignore|@Disabled|assume(True|That)?\(|pytest\.mark\.(skip|skipif|xfail)|pytest\.skip\(|@unittest\.skip' \
   -g '!**/node_modules/**' .
```

Conditional skips (`describe.runIf(process.env.X)`, `skipIf`, `pytest.mark.skipif`, `assumeTrue`) are the ones a first grep misses. On a real React app the runner reported 4 skipped tests and a plain `.skip` grep found none: they sat behind `runIf` on an env var no CI job set. Compare the grep with the runner's skipped count.

Fix: focused tests are always removed (and CI blocks them: Playwright `forbidOnly: !!process.env.CI`, Vitest `--allowOnly` is false on CI by default). Each skip needs a reason and an issue: `test.fixme('...')` with `require-annotation-reason`, `#[ignore = "flaky: #123"]`, `@Ignore("flaky: #123")`, `pytest.mark.skip(reason="#123")`. For pytest set `xfail_strict = true` so an xfail that starts passing fails the run.

### 3.7 Happy path only

Every test in a module feeds valid input. No error, empty, boundary or timeout case. Not in tsDetect, but it is the smell testers find most in AI written suites, because the builder tests what they built. Detect by ratio, per module:

```bash
# error-path assertions vs all tests, per file (JS/TS); swap patterns per stack
for f in $(rg -l '\b(it|test)\(' -g '*.test.*' src); do
  t=$(rg -c '\b(it|test)\(' "$f"); e=$(rg -c 'toThrow|rejects\.|toBeNull|toBeUndefined|status\)\.toBe\(4|status\)\.toBe\(5|error' "$f" || echo 0)
  echo "$e/$t $f"; done | sort -t/ -k1 -n | head
# Rust: is_err|unwrap_err|should_panic|Err\(   Kotlin: assertFailsWith|assertThrows|Result.failure   Python: pytest.raises|is None
```

A file with `0/12` is a lead. Confirm with branch coverage: uncovered `throw`, `catch`, `Err(` and `else` lines are the missing tests (`coverage.md` section 5). Fix: one test per error branch the spec names, plus boundaries (empty, one, max, max plus one).

## 4. Smells that make a test break for the wrong reason

### 4.1 Sleepy test

A fixed sleep waits for something asynchronous. Too short on a slow CI runner (flaky), too long everywhere else (slow). Google found coverage instrumentation alone made sleep based tests flaky because code ran slower (Ivankovic et al. 2019). Fowler: "Never use bare sleeps to wait for asynchronous responses: use a callback or polling." Evidence: strong.

| Stack | Detect (verified on fixtures) | Fix |
|---|---|---|
| JS/TS | `rg -n 'new Promise\(\s*\(?r(esolve)?\)?\s*=>\s*setTimeout' -g '*.test.*'` | fake timers (`vi.useFakeTimers()`, `vi.advanceTimersByTimeAsync`), `vi.waitFor(() => ...)`, Testing Library `findBy*` |
| Playwright | lint `no-wait-for-timeout`; `rg -n 'waitForTimeout\('` | web first assertions: `await expect(locator).toBeVisible()` retries until timeout |
| Rust | `rg -n 'thread::sleep|time::sleep' tests src` | `#[tokio::test(start_paused = true)]` or `tokio::time::pause()`; channels or `Notify` to wait for the event |
| Kotlin | `rg -n 'Thread\.sleep' app/src/test app/src/androidTest` | inside `runTest`, `delay()` uses virtual time and is fine; `advanceUntilIdle()`; Compose `composeTestRule.waitUntil { ... }`; Espresso idling resources |
| Python | `rg -n 'time\.sleep\(' tests` | `time-machine` or `freezegun` for clocks; poll with a deadline; `asyncio.wait_for` |

### 4.2 Mystery guest

The test reads a file, a database row, an environment variable or a network service that is not visible in the test. When someone changes the resource, unrelated tests fail, and the test cannot be read as documentation (van Deursen et al. 2001, smell 1). tsDetect found it in 12% of Android test files.

Detect: JS `rg -n "readFileSync|fs\.read|process\.env\.|fetch\(['\"]https?" -g '*.test.*'`; Rust `rg -n 'File::open|fs::read|env::var|include_str!' tests`; Kotlin `rg -n 'File\(|getResource|System\.getenv' app/src/test`; Python `rg -n 'open\(|os\.environ|requests\.' tests`; script `NET`. Real network in unit tests is never acceptable: block it (MSW `onUnhandledRequest: 'error'`, `pytest-socket --disable-socket`).

Fix (van Deursen's refactorings): Inline Resource (put the data in the test) when small; Setup External Resource (the test creates the file in a temp dir and removes it) when it must be a file; fixture files named after the test that uses them (`fixtures/parse-empty-invoice.json`). `include_str!` of a small, named fixture next to the test is fine.

### 4.3 Resource optimism and test run war

Resource Optimism: the test assumes a directory, table or port exists. Test Run War: two tests or two parallel runs use the same temp file, port or DB row (van Deursen smells 2 and 3). Both show up as failures only under parallel runs or on another machine.

Detect: fixed paths and ports: `rg -n "/tmp/|:\d{4,5}['\"/]|localhost:\d+" tests e2e src/**/*.test.*`; fixed ids in inserts: `rg -n "id: ?['\"]?(1|test|user1)['\"]?" tests`. Then run shuffled and in parallel (`vitest run --sequence.shuffle.tests`, `cargo nextest run` which runs each test in its own process, `pytest -p randomly -n auto`).

Fix: Make Resource Unique (temp dirs per test: `tempfile::tempdir()`, `tmp_path` in pytest, `fs.mkdtemp`, JUnit `@TempDir`), random free ports (bind to port 0), unique ids per test, transactions rolled back per test.

### 4.4 Sensitive equality

Comparing `toString()` output or a whole serialized string, so a change in formatting breaks tests that are not about formatting (van Deursen smell 10). Detect: `rg -n 'toString\(\)\)?\.?(toBe|toEqual)|assertEquals\(".*", .*\.toString\(\)\)|format!\("\{:\?\}"' tests`. Fix: compare values or structured fields (`toEqual({...})`, data class equality, `assert_eq!(parsed, Expected { .. })`). Keep string comparison only where the string is the product (CLI output, error message text).

### 4.5 Over-mocking

The test mocks so much that it checks the mocks, not the code. Signs: mocks returning mocks, more `vi.mock`/`every {}`/`patch` lines than assertions, assertions only on `toHaveBeenCalledWith`, and mocking the module under test or its own siblings. These tests break on every refactor and pass when the real integration is broken. kwx-developer T2 and section 6 of `testing-strategy.md` set the rule (state over interaction, mock only boundaries); this is how to find violations.

```bash
# mocks vs assertions per test file (JS/TS); top of the list first
for f in $(rg -l 'vi\.mock|jest\.mock|vi\.spyOn|jest\.spyOn' -g '*.test.*' src); do
  m=$(rg -c 'vi\.(mock|spyOn|fn)\(|jest\.(mock|spyOn|fn)\(' "$f"); a=$(rg -c 'expect\(' "$f")
  c=$(rg -c 'toHaveBeenCalled' "$f" || echo 0); echo "mocks=$m expects=$a calledWith=$c $f"; done | sort -t= -k2 -nr | head
# Kotlin (MockK / Mockito): rg -c 'mockk<|every \{|verify \{|mock\(|whenever\(' app/src/test
# Rust (mockall): rg -c 'expect_\w+\(\)|\.times\(' tests src
# Python: rg -c '@patch|patch\(|MagicMock\(|Mock\(' tests
```

Fix: replace mocks of your own code with the real objects; use fakes (an in memory repository that obeys the same contract) at boundaries; keep interaction asserts only for side effects you cannot observe (email sent, payment charged); move the check to an integration test against the real dependency (Testcontainers, a real Postgres, MSW at the HTTP boundary).

### 4.6 Snapshot rot

Snapshots grow, nobody reads them, and failing ones are re-recorded with `-u` without review. Then the snapshot asserts whatever the code did last time, bugs included. Kent C. Dodds and Justin Searls: a snapshot is an assertion without stated intent.

Detect:

```bash
fd -e snap | xargs wc -l | sort -n | tail                 # large snapshot files (Jest/Vitest)
fd -e snap -p 'snapshots/' . | xargs wc -l | sort -n | tail   # insta (Rust) keeps .snap files in snapshots/
git log --since="6 months ago" --format='%h %s' -- '*.snap' | head -20         # how often they change
# commits that touched snapshots AND source together, with no test file: likely blind -u
git log --since="6 months ago" --format='%h' -- '*.snap' | while read h; do
  git show --name-only --format= "$h" | rg -q '\.(test|spec)\.' || echo "$h $(git log -1 --format=%s $h)"; done
```

Fix: small snapshots (`no-large-snapshots` with `maxSize: 50`), inline snapshots (`toMatchInlineSnapshot`, insta `assert_snapshot!(x, @"...")`) so the expected value is in review, serializers that strip ids and dates, `prefer-snapshot-hint` for named snapshots, CI that fails on a missing snapshot instead of writing it (Jest `--ci`; insta does not write snapshots when it detects CI, docs), and remove unused ones (`vitest -u` after a reviewed run, `cargo insta test --unreferenced=reject`, docs). Replace snapshots of whole component trees with assertions on what the user sees.

### 4.7 Fragile test and Test Logic in Production

Fragile Test (Meszaros): the test fails when the code changes in ways that do not affect the behaviour under test: private method calls, CSS selectors, call order, exact log lines. Test Logic in Production / For Testers Only (van Deursen smell 9): production code has `if (process.env.NODE_ENV === 'test')`, `isTesting` flags, or methods only tests call.

Detect fragile: Playwright `no-raw-locators`, `no-nth-methods`; `rg -n "locator\(['\"](\.|#|//)" e2e`; tests that reach into internals (`rg -n '\._\w+|\[.private' -g '*.test.*'`, Kotlin `@VisibleForTesting` count). Detect test logic in production: `rg -n "NODE_ENV ?=== ?['\"]test|isTest(ing)?\b|cfg!\(test\)|BuildConfig\.DEBUG.*test|'pytest' in sys\.modules" src app lib --glob '!*test*'`.

Fix: test through the public API and user facing locators (`getByRole`, `getByLabel`); move test only code to test helpers or inject the dependency it was switching.

## 5. Smells that make a failure hard to read

These are real but low risk. Report them grouped, as P3, unless they sit in a hotspot (kwx-developer `~/.claude/skills/kwx-developer/quality/tech-debt-and-todo.md` section 3).

### 5.1 Assertion roulette

Several assertions with no message, so a failure does not say which one broke or why (van Deursen smell 7; the most common smell in every study). Modern runners print the failing line and a diff, which weakens the smell in JS, Kotlin and Rust; it still bites in loops and helpers where the line number is the same for every case.

Detect: script `EAGER=k`; lint `max-expects` (`{ max: 5 }`); ruff `PT018` for `assert a and b`. Fix: split by behaviour (one test per behaviour, T3 in kwx-developer), add messages where the line does not explain itself (`expect(total, 'after coupon').toBe(50)`, `assert_eq!(a, b, "case {name}")`, `assertEquals(5, total, "after coupon")`, `assert total == 50, f"case {name}"`), and use table driven tests with the case name in the message. Soft assertions (`expect.soft`, `assertSoftly`, `assertAll`) report every failure in one run.

### 5.2 Eager test

One test calls many production methods and checks them all. Hard to name, and it fails for many reasons. Spadini found it among the most harmful (change and defect proneness). Detect: test names with "and" or "works" (`rg -n "(it|test)\(['\"][^'\"]*( and |works|everything)" -g '*.test.*'`, Kotlin backtick names likewise), very long tests (`EAGER=k`, or over about 30 lines). Fix: one behaviour per test, named "does X when Y"; shared setup in a helper, not in one giant test.

### 5.3 Lazy test

The opposite: several tests check the same method with the same fixture, each asserting one field. Usually harmless; merge only if they are always read together (van Deursen smell 6). Do not report it unless the owner asks for a style pass.

### 5.4 General fixture

A shared `beforeEach`/`setUp` builds more than each test needs, so a reader cannot tell what matters, and tests run slower (van Deursen smell 4). Detect: `beforeEach` blocks longer than about 15 lines, or `lateinit var` fields in a Kotlin test class used by only some tests. Fix: build what each test needs in the test or in small named builders (`aUser({ role: 'admin' })`, test data builders, pytest fixtures composed per test).

### 5.5 Magic number test

Unexplained literals in assertions: `expect(price(3, 7)).toBe(18.9)`. 35% of Android test files. Developers in Peruma's survey said a constant is only worth it when the number has a meaning a reader cannot see in the test. Fix only those: show the derivation (`toBe(3 * 7 * 0.9)` with a comment "10% bulk discount") or name the constant from the spec.

### 5.6 Conditional test logic

`if`, `switch`, `when`, `match` inside a test, so some assertions may never run (Meszaros). Loops over a data table are not this smell; a branch that chooses which assertion runs is. Detect: script `BRANCH`; lint `no-conditional-in-test`, `no-conditional-expect`. Fix: split into one test per case (`it.each`, `test.each`, `#[rstest]` cases, JUnit `@ParameterizedTest`, `@pytest.mark.parametrize`).

### 5.7 Redundant print and duplicate assert

`console.log`, `println!`, `dbg!`, `print` left in tests (developers agreed unanimously these go). Duplicate Assert: the same assertion twice in one test. Detect: script `PRINT`; `rg -n 'console\.log|dbg!\(' -g '*.test.*' tests`. Fix: delete; use the runner's output on failure (`--silent=passed-only` in Vitest).

### 5.8 Obscure test

You cannot tell at a glance what it checks (Meszaros): long setup, irrelevant data, no clear arrange, act, assert. It is the umbrella over 5.1 to 5.5. Fix by the same refactorings; a good test reads like the spec line it proves.

## 6. Smells at suite level

| Smell (Meszaros) | Signal | Where handled |
|---|---|---|
| Slow tests | unit suite over a minute; single tests over 100 ms (Google: a tenth of a second is slow for a unit test) | `test-suite-audit.md` step 3, `ci-testing.md` |
| Erratic (flaky) tests | passes and fails on the same commit; retried passes in CI | kwx-developer `testing-strategy.md` section 11; `ci-testing.md` section 4 |
| Test code duplication | same setup copied in many files | report only when the copies drift apart; extract a builder |
| Developers not writing tests | source churn with no test churn | `test-suite-audit.md` step 7 |
| Production bugs | escaped defects keep coming from one area | `test-metrics.md` |
| High test maintenance cost | tests change in most feature commits | `git log --format= --name-only` ratio of test to source files per commit |

## 7. Priority: what to fix, what to leave

1. **Always a finding (P1 if on money, data, auth; else P2):** Liar (3.3), Empty test (3.1), focused test (3.6), Swallowed exception that hides a failure (3.5), Unknown test on risky code (3.2).
2. **Usually a finding (P2):** Sleepy (4.1), Mystery guest with real network (4.2), Test run war (4.3), skips with no reason (3.6), Happy path only on risky code (3.7), Over-mocking where the real integration has no test (4.5), Snapshot rot on user facing output (4.6).
3. **Taste, report grouped as P3 or not at all:** Assertion roulette, Eager, Lazy, General fixture, Magic number, Conditional logic in table tests, prints.

Never fix a smell the owner was not asked about (kwx-developer `~/.claude/skills/kwx-developer/workflow/audit-and-ask.md`). When the agent writes new tests, it writes none of these smells, and the checks below apply to its own work.

## 8. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| Linters for tests considered | Project has the test lint plugin, or its absence is reported as a finding | `rg -n 'eslint-plugin-(jest|playwright)|@vitest/eslint-plugin|"PT"' package.json eslint.config.* pyproject.toml ruff.toml` |
| Scan ran | `smellscan.py` output saved, counts per flag listed | output in scratchpad |
| Every hit read | Each reported smell was opened and confirmed; false hits dropped | notes list path:line and verdict |
| No liars in new tests | New tests await every promise assertion, name the panic, assert the exception type and message | lint run plus reading the diff |
| No empty or assertion-free new tests | 0 `EMPTY` and 0 unexplained `NO-ASSERT` in files the task added | `python3 -I smellscan.py <new test files>` |
| No sleeps in new tests | 0 `SLEEP` in files the task added | same |
| Skips carry reason and issue | Every skip, ignore, fixme, xfail has a reason with an issue link | the rg in 3.6, read each |
| No focused tests | 0 `.only`, `fit`, `fdescribe` | rg in 3.6 |
| Error paths tested | Each module the task touched has at least one error path test per error branch in the spec | section 3.7 ratio plus branch coverage |
| Snapshots reviewed | No snapshot file over about 50 lines per entry added; no blind `-u` | `git diff --stat -- '*.snap'` and read |
| Findings grouped and ranked | One finding per pattern per area, priority from section 7 | findings list |
