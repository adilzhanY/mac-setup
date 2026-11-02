# Coverage

Coverage says which code the tests ran. It does not say whether the tests checked anything. This file explains the coverage kinds (line, statement, branch, condition, MC/DC), what the research says about coverage and bug finding, how the skill uses coverage as a gap finder on changed code, the commands per stack, and why a coverage number is never a target. kwx-developer covers the policy in three bullets (`reliability/testing-strategy.md` section 12); this file is the tester's working method.

## Contents

1. The rules
2. What each coverage kind measures
3. What the research says
4. How the tester uses coverage
5. Gaps in changed code (diff coverage)
6. Tools per stack
7. Traps
8. Checks

## 1. The rules

1. **Use coverage to find untested code, never as proof that code is tested.** Inozemtseva and Holmes (ICSE 2014, 31,000 suites, 5 Java systems up to 724,000 lines): once suite size is controlled, the correlation between coverage and fault detection is "low to moderate", and coverage "should not be used as a quality target". Evidence: strong.
2. **Never set a coverage percentage as the goal of a task.** Goodhart's law: a measure that becomes a target stops measuring (`test-metrics.md`). Google's own guidance warns that a mandated number turns into a checkbox and invites tests "with little actual value" (Arguelles, Ivanković, Bender, Google Testing Blog 2020). Evidence: moderate.
3. **Read the uncovered lines in the code you changed, one by one, and decide for each: test it, or say why not.** "What's not covered is more meaningful than what is covered" (same post). Evidence: moderate.
4. **Look at branch coverage, not only lines.** One line can hold two branches. In a verified run below, a file showed 100% lines and 50% branches. Evidence: verified here.
5. **Never write a test only to turn a line green.** A test with no assertion raises coverage and checks nothing (`test-smells.md` 3.2). If a line is not worth an assertion, leave it red and say so.
6. **When coverage on risky code is already high, switch to mutation testing.** Google studied 1,502 high priority bugs whose bug introducing changes were already covered by tests: for 70% of them, a mutant on that change would have flagged the missing check (Petrović et al., ICSE 2021). Mutants detect real faults "independently of code coverage" (Just et al., FSE 2014, 357 real faults). Evidence: strong.
7. **Report coverage of named risky files, never one number for the repo.** A repo average hides a 0% payment module behind a 95% utils folder.
8. **Every coverage exclusion is reviewed like code.** `/* v8 ignore */`, `# pragma: no cover`, `#[coverage(off)]`, Kover `excludes` hide code from the report. Each needs a reason a reviewer accepts (generated code, debug only code, a platform branch CI cannot run).

## 2. What each coverage kind measures

Example function used below:

```ts
export function price(qty: number, unit: number, coupon?: string): number {
  if (qty < 0) throw new Error('negative')
  const base = qty * unit
  if (coupon === 'HALF') return base / 2
  return base
}
// the only test: expect(price(2, 3)).toBe(6)
```

| Kind | Counts | For the example |
|---|---|---|
| Line | source lines that ran at least once | 100% (4/4): every line ran, because `if (...) throw` sits on one line |
| Statement | statements that ran | 66% (4/6): the `throw` and `return base / 2` never ran |
| Function | functions called | 100% |
| Branch (decision) | each outcome of each `if`, `?:`, `&&`, `\|\|`, `switch` case | 50% (2/4): `qty < 0` true and `coupon === 'HALF'` true never happened |
| Condition | each boolean sub expression true and false at least once | for `a && b`: `a` true and false, `b` true and false |
| MC/DC (modified condition/decision) | each condition shown to change the decision on its own, others held fixed | for `a && (b \|\| c)`: needs about N+1 = 4 tests, not 2^3 = 8 |
| Path | every route through the function | grows exponentially; not used in practice |
| Region (LLVM) | code regions between branch points; what `cargo llvm-cov` reports as "regions" | close to statement coverage |

The line, statement and branch numbers in the table come from a real run (Vitest 5.0.5, v8 provider, 2026-10-31):

```
File      | % Stmts | % Branch | % Funcs | % Lines | Uncovered Line #s
price.ts  |   66.66 |       50 |     100 |     100 | 2-4
```

**MC/DC in one example.** Decision `canEdit = isOwner && (isAdmin || !locked)`. MC/DC asks for a pair of tests per condition where only that condition changes and the result flips:

| Test | isOwner | isAdmin | locked | canEdit | Shows |
|---|---|---|---|---|---|
| 1 | T | T | T | T | |
| 2 | F | T | T | F | isOwner matters (1 vs 2) |
| 3 | T | F | T | F | isAdmin matters (1 vs 3) |
| 4 | T | F | F | T | locked matters (3 vs 4) |

DO-178C requires MC/DC for the most critical avionics software (level A). Common JS, Rust, Kotlin and Python tools do not report it. For this owner's projects, use MC/DC as a thinking tool for permission and pricing rules with three or more conditions: write the table by hand, then one test per row. Evidence: moderate (Chilenski and Miller 1994, cited by Ivankovic et al.).

## 3. What the research says

| Study | Data | Finding | Use it for |
|---|---|---|---|
| Inozemtseva and Holmes, ICSE 2014 | 31,000 generated suites, 5 Java systems, statement, decision and modified condition coverage, mutation score as effectiveness | moderate to high correlation when suite size is ignored; low to moderate when size is fixed. "Stronger forms of coverage do not provide greater insight" | rule 1, rule 2 |
| Gopinath, Jensen and Groce, ICSE 2014 | hundreds of open source Java projects | of the coverage kinds, statement coverage predicted mutation kills best (summary read, full paper not) | do not chase exotic coverage kinds |
| Kochhar, Lo, Lawall and Nagappan, IEEE Trans. Reliability 2017 | 100 large Java projects, real post release bugs | insignificant correlation between coverage and post release bugs at project level, none at file level (abstract) | a high number does not mean few escaped bugs |
| Chekam et al., ICSE 2017 | real faults, no clean program assumption | statement and branch coverage have little effect on fault revelation until very high levels; strong mutation reveals the most faults (abstract) | gaps matter more than the last percent |
| Just et al., FSE 2014 | 357 real faults, 5 projects | mutant detection correlates with real fault detection independently of coverage; 73% of real faults coupled to mutants | rule 6 |
| Ivanković, Petrović, Just and Fraser, FSE 2019 ("Code Coverage at Google") | 1 billion lines measured daily, 7 languages, 5 years, survey of 3,000 (512 answered) | coverage shown per changed line in code review; 45% of developers use it often or very often when authoring, 40% when reviewing, 10% never. No company wide threshold; voluntary levels: project 60% / change 70%, 75% / 80%, 90% / 90%. Instrumentation slows tests and made sleep based tests flaky | section 4, section 7 |
| Arguelles, Ivanković and Bender, Google Testing Blog 2020 | practitioner guidance | 60% "acceptable", 75% "commendable", 90% "exemplary"; gains past a point are "logarithmic"; per commit goals of 99% are reasonable, 90% a good lower bound; get from 30% to 70% before arguing about 90 to 95 | how to talk about numbers with the owner |
| Petrović, Ivanković, Fraser and Just, ICSE 2021 | 15 million mutants, 6 years, 1,502 high priority bugs | developers shown mutants write more tests; the bug introducing changes were all covered by tests, yet for 70% of the bugs a surviving mutant would have pointed at the gap | rule 6 |

Synthesis: low coverage is a strong signal (that code is not tested at all). High coverage is a weak signal (the code ran; nobody knows if anything was checked). The useful direction is red to green on the lines that matter, then mutation on the risky ones.

## 4. How the tester uses coverage

The tester writes tests from the spec first (see the strategy files). Coverage comes after, as a second opinion:

1. **Write the spec tests without looking at coverage.** Coverage first leads to tests shaped like the code, which copy its mistakes.
2. **Run coverage with branch data** on the changed files only (section 5).
3. **List each uncovered line and branch in the changed code.** For each, ask: which requirement or failure mode is this? Typical answers: an error branch (missing negative test), a boundary (missing edge case), dead code (report to kwx-developer, do not test it), defensive code that cannot happen (leave it, say why).
4. **Write the missing tests from the requirement, not from the line.** "Negative quantity is rejected with message X" is a test. "Line 2 throws" is not.
5. **On risky modules (money, auth, permissions, migrations, parsers of untrusted input) with branch coverage already near full, run mutation testing on the changed lines** (`test-suite-audit.md` step 8 has the commands).
6. **Report what is not covered and why**, in the final report: "3 uncovered branches in `price.ts`: 2 tested now, 1 is a platform check for iOS that CI cannot run".

## 5. Gaps in changed code (diff coverage)

Diff coverage means: of the lines this change added or modified, which did tests run. It is the number Google shows in review, and the only coverage number worth a CI gate.

**Option A: the project's runner, per changed file (verified, Vitest 5.0.5).**

```bash
npx vitest run --changed origin/main --coverage --coverage.changed=origin/main \
  --coverage.reporter=text --coverage.thresholds.branches=100 --coverage.thresholds.perFile
# exit 1: "ERROR: Coverage for branches (50%) does not meet global threshold (100%) for src/price.ts"
```

`--changed` runs only tests related to changed files; `--coverage.changed` limits the report to changed files. The check is per changed file, not per changed line, so old untested code in a touched file also counts. Use it as a local gap finder; as a CI gate it can punish someone for touching an old file.

**Option B: diff-cover (any stack, line level).**

```bash
uvx diff-cover coverage/cobertura-coverage.xml --compare-branch=origin/main          # or lcov.info, jacoco.xml
uvx diff-cover coverage/lcov.info --compare-branch=origin/main --fail-under=90 --html-report diff-cover.html
```

Verified with diff-cover 11.0.0. Trap found while verifying: diff-cover is line based. On the example above it reported "src/price.ts (100%)" for the change that added the coupon branch, although the coupon branch was never taken. Use it for "did the new lines run at all", not for branches.

**Option C: changed lines plus branches (script, verified).** Reads any lcov file (Vitest, Jest, cargo llvm-cov, coverage.py `coverage lcov`) and prints changed lines that never ran and changed lines with a branch never taken. Exit 1 when there are gaps. Kover writes JaCoCo XML, not lcov, so for Kotlin use diff-cover (Option B).

Run it (from the repo root):

```bash
npx vitest run --coverage --coverage.include=src --coverage.reporter=lcov
python3 -I ~/.claude/skills/kwx-tester/scripts/diffgaps.py coverage/lcov.info origin/main
# real output on the example:   src/price.ts:4  BRANCH 1/2 taken     (diff-cover said 100%)
python3 -I ~/.claude/skills/kwx-tester/scripts/diffgaps.py --selftest   # proves it finds an unrun line and an untaken branch
```

It prints one line per gap (`path:line  NOT RUN` or `path:line  BRANCH 1/2 taken`), the count on stderr, and exits 1 when there are gaps. Each gap is a missing test case: write the case from the spec, see it fail on a mutant, then rerun.

A file missing from the report is skipped silently: check that `coverage.include` covers all source, or new files never imported by a test look "fine".

**Option D: a hosted service.** Codecov and Coveralls show "patch coverage" on the pull request. Fine if the project already uses one; the owner's projects usually do not need it.

## 6. Tools per stack

| Stack | Tool | Command (source) |
|---|---|---|
| TS/JS with Vitest | `@vitest/coverage-v8` (default) or `@vitest/coverage-istanbul` | `npx vitest run --coverage --coverage.include=src` (verified). Since Vitest 3.2 v8 uses AST based remapping and gives the same report as istanbul (Vitest docs). Branch data on by default |
| Jest (React Native, Expo) | istanbul built in | `npx jest --coverage --coverageReporters=lcov --coverageReporters=text-summary` (Jest docs) |
| Playwright e2e | no built in coverage for app code | do not merge e2e coverage into unit coverage by default; Google notes e2e coverage is "incidental and not deliberate" |
| Rust | `cargo-llvm-cov` | `cargo llvm-cov --workspace --lcov --output-path lcov.info`; `cargo llvm-cov --html` / `--open`; with nextest `cargo llvm-cov nextest`; gate `--fail-under-lines 80`; branch coverage `--branch` needs nightly (README) |
| Kotlin JVM and Android unit tests | Kover 0.9.x (`id("org.jetbrains.kotlinx.kover")`) | `./gradlew koverHtmlReport koverXmlReport` (XML is JaCoCo format, diff-cover reads it); Android variant `./gradlew :app:koverXmlReportDebug`; rule `kover { reports { verify { rule { minBound(50) } } } }`; units LINE, BRANCH, INSTRUCTION (Kover docs) |
| Android instrumented tests | JaCoCo through AGP | `android { buildTypes { debug { enableAndroidTestCoverage = true } } }` then `./gradlew createDebugCoverageReport` (AGP docs; needs an emulator, see `ci-testing.md`) |
| Python | coverage.py | `coverage run --branch -m pytest`; `coverage report -m --skip-covered`; `coverage xml` (Cobertura) or `coverage lcov` (coverage.py docs) |

Reading a report fast: sort by uncovered branches, not by percent. In the text table, the "Uncovered Line #s" column is the work list. In HTML, yellow marks partly taken branches.

## 7. Traps

- **Files no test imports are invisible.** Vitest, Jest and coverage.py report only files that were loaded unless you set `include` (`coverage.include: ['src']`, `collectCoverageFrom`, `[tool.coverage.run] source = ["src"]`). A 0% file not in the report looks like no problem.
- **Instrumentation changes timing.** Google's most common coverage failure was timeouts and memory from instrumentation, and sleep based tests became flaky when instrumented (Ivankovic et al. 2019). Run coverage as a separate CI job, not on the blocking test job, if it slows the suite.
- **Coverage from big tests flatters.** An e2e test that loads the whole app executes thousands of lines it never checks. Keep unit and e2e coverage separate unless the owner wants the union.
- **v8 and istanbul used to disagree.** Before Vitest 3.2, v8 coverage counted some lines differently from istanbul. A jump in numbers after an upgrade may be the tool, not the tests.
- **Ignore comments rot.** `rg -n 'v8 ignore|istanbul ignore|pragma: no cover|coverage\(off\)|@Generated' src` and read each; ignores on business logic are findings.
- **Thresholds that ratchet down.** `autoUpdate` in Vitest only raises thresholds; a team that lowers them by hand each time the number drops has a target, not a signal. Prefer a changed code gate (Option A or B) over a global number.
- **100% everywhere is waste.** Google: project wide goals above 90% "are most likely not worth it". Spend the effort on mutation testing of the risky 10%.

## 8. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| Coverage includes all source | `include` / `source` / `collectCoverageFrom` set to the source folders | `rg -n 'include|collectCoverageFrom|source *=' vitest.config.* jest.config.* pyproject.toml .coveragerc` |
| Branch data collected | report has a branch column | Vitest and istanbul by default; `coverage run --branch`; Kover BRANCH; cargo llvm-cov regions (branches on nightly) |
| Changed code gaps listed | every uncovered changed line and branch has a verdict (tested now, or reason) | `diffgaps.py` or Vitest Option A output, with verdicts in the report |
| No coverage only tests | new tests each assert behaviour from the spec | `python3 -I smellscan.py` on new test files: 0 `NO-ASSERT` |
| No new ignores without reason | each new ignore comment or exclude has a reason line | `git diff origin/main -- src | rg 'ignore|no cover|coverage\(off\)|excludes'` |
| No percentage target in the task | the task and report talk about named gaps, not "reach 80%" | read the plan and report |
| Risky code gets mutation testing | money, auth, permissions, parsers with high coverage have a mutation sample | `test-suite-audit.md` step 8 output |
| Repo average not reported as a finding | findings name files and branches | read findings |
