# Mutation testing

Mutation testing changes the code in small ways (a `<` becomes `<=`, a condition becomes `false`, a function returns a default) and runs the tests against each change. If no test fails, the change "survived", and you have found behaviour no test checks. It answers the question coverage cannot: would the tests notice if this code were wrong? This file explains why coverage lies, what the industrial evidence says, the tools for the owner's stacks with commands verified on real runs, and the workflow that makes it affordable: run it on the diff, not on the whole repo.

kwx-developer has the short version (scoped commands per tool, `~/.claude/skills/kwx-developer/ai-agents/tests-and-honesty.md` section 8). This file adds the evidence, triage of survivors, and CI setup.

## Contents

1. Why coverage lies
2. Vocabulary
3. What the evidence says
4. When to run it
5. Tools
6. Worked examples (verified)
7. Workflow on a diff
8. Triage: kill, equivalent, or not worth it
9. CI setup
10. Checks

## 1. Why coverage lies

Coverage says a line ran during a test. It does not say any test checked what the line did. Google's example (Petrovic et al., "Practical Mutation Testing at Scale"):

```java
Buffer getBuffer() {
  Buffer buf = new Buffer();
  buf.Append(this.internal_buf);   // mutation: delete this line
  return buf;
}
```

The tests call the function, so the line is covered, but nothing asserts on the returned buffer's content. Deleting the line changes nothing in the test results. A statement deletion mutant points straight at the missing assertion.

Khorikov puts it as: coverage is a good negative indicator (low coverage means untested code) and a bad positive one (high coverage does not mean good tests). ISTQB adds that even 100% statement coverage misses data dependent defects such as a division that fails only when the denominator is zero. Tests without assertions, assertions on mocks, and `toBeTruthy` on rich results all reach high coverage.

## 2. Vocabulary

| Term | Meaning |
|---|---|
| Mutant | A copy of the program with one small change |
| Mutation operator | The kind of change: replace an operator, negate a condition, replace a return value, delete a statement, change a constant or string |
| Killed (caught) | At least one test failed against the mutant: good |
| Survived (missed) | All tests passed: a gap, or an equivalent mutant |
| No coverage | No test even ran the mutated code |
| Timeout | The mutant made a test hang (often an infinite loop); counts as killed in most tools |
| Unviable | The mutant did not compile (cargo-mutants); ignored |
| Equivalent mutant | A change that does not change behaviour (for example `i < n` vs `i != n` in a loop that always steps by 1); cannot be killed |
| Mutation score | Killed / (total minus equivalent and unviable), as a percentage |

## 3. What the evidence says

- **Mutants stand in for real faults.** Just et al. ("Are mutants a valid substitute for real faults in software testing?", FSE 2014) found that mutant detection correlates with real fault detection independently of coverage (cited via the Google papers; not read in full here).
- **Google runs it on code review at scale.** Mutation testing is applied only to changed lines in a code change, surfaced as review comments. The system was evaluated on almost 17 million mutants and 760 000 changes, which surfaced 2 million mutants during review (Petrovic, Ivankovic, Fraser and Just, "Practical Mutation Testing at Scale: A view from Google", 2021; earlier "State of Mutation Testing at Google", ICSE SEIP 2018). Evidence: strong.
- **Most raw mutants are noise unless you filter.** Developers at Google first marked 85% of reported mutants as unproductive (equivalent, or killable only by a test nobody should write, such as asserting the initial capacity of a collection). Suppressing "arid" code (logging, simple delegation, configuration) and keeping at most one mutant per line raised the productive share from 15% to 89%.
- **It changes behaviour.** Developers exposed to mutants wrote more tests over time, and mutants were coupled with 70% of a sample of high priority real bugs (Petrovic et al., "Does mutation testing improve testing practices?", ICSE 2021).

What this means for a solo developer: run it on the changed code, on the modules where a wrong answer costs money, data or security, and skip mutants in code that does not matter.

## 4. When to run it

| Run it on | Skip it on |
|---|---|
| Money, pricing, billing, quotas | Logging, analytics calls, debug output |
| Auth, permissions, RLS helper logic | Generated code, glue that only wires modules |
| Parsers of external input, validators | UI layout code (use visual review instead) |
| Sync, merge, conflict resolution, migrations | Code with no tests yet (write tests first; every mutant survives) |
| Code a test audit flagged as "covered but weakly asserted" | Whole repository on every push |
| Agent written code before accepting it | |

## 5. Tools

| Stack | Tool | Scope to a change | Notes |
|---|---|---|---|
| TypeScript / JS | StrykerJS 10.1.1 (`@stryker-mutator/core`, runners for Vitest and Jest) | `npx stryker run --mutate src/billing/price.ts` or with lines `--mutate src/app.js:5-7`; `--incremental` reuses results from `reports/stryker-incremental.json` | Verified with Vitest runner. `coverageAnalysis: "perTest"` runs only tests that cover each mutant |
| Rust | cargo-mutants 27.1.0 | `git diff main...HEAD > changes.diff && cargo mutants --in-diff changes.diff`; `--file src/x.rs`; `--package foo` | Verified. Results in `mutants.out/` (`caught.txt`, `missed.txt`, `timeout.txt`, `unviable.txt`, a diff per mutant). Skip a function with `#[mutants::skip]` (needs the small `mutants` crate as a dependency; docs) |
| Kotlin / JVM | PIT (pitest) with the Gradle plugin `info.solidsoft.pitest` | `targetClasses` for the changed package; `withHistory` for incremental runs | Docs only. Open source PIT makes many useless mutants on Kotlin bytecode (coroutines, generated null checks); the Kotlin plugin from ArcMutate fixes this but needs a paid licence. Judge the noise before relying on it |
| Python | mutmut 3 | `paths_to_mutate` in `[tool.mutmut]` in `pyproject.toml`, then `mutmut run`, `mutmut browse` | Docs only |
| Go | gremlins | `gremlins unleash ./pkg` | Docs only |

cargo-mutants notes from its docs: `--in-diff` only looks at changes to code under test (a diff that only touches tests runs no mutants), and an incremental run "doesn't replace a full test run", because a change in one place can weaken testing elsewhere. Stryker's incremental mode does not notice changes to dependencies, environment variables or `.snap` files.

## 6. Worked examples (verified)

### Stryker on a pricing module

A pricing function with the spec cases from `test-design-techniques.md` section 6 (all plans, student discount, seat boundaries 0, 1, 2, 49, 50, 51 and 1.5) and two properties. Coverage looked complete for the logic. Stryker 10.1.1 with the Vitest runner:

```text
$ npx stryker run --mutate src/pricing.js
[NoCoverage] StringLiteral  src/pricing.js:6:48
-     if (base === undefined) throw new RangeError('plan');
+     if (base === undefined) throw new RangeError("");

[Survived] ConditionalExpression  src/pricing.js:6:7
-     if (base === undefined) throw new RangeError('plan');
+     if (false) throw new RangeError('plan');

[Survived] StringLiteral  src/pricing.js:4:81
-     ... throw new RangeError('seats');
+     ... throw new RangeError("");

Mutation score 89.29
```

Reading the survivors:

1. `if (false) throw ...` survived: no test passes an unknown plan. The invalid partition "plan not in the catalogue" was missing from the spec cases. Kill it with `expect(() => price({ plan: "weekly" })).toThrow(RangeError)`, and ask the owner what the API should return.
2. The empty message mutants survived because tests check only the error type. If the message or an error code is part of the contract (shown to users, parsed by callers), assert it; if not, mark these as not worth killing.

### cargo-mutants on a diff

A crate with `remaining(total, elapsed)` tested, and a new function `is_done` added in the working tree without a test:

```text
$ git diff > changes.diff
$ cargo mutants --in-diff changes.diff
Found 3 mutants to test
MISSED   src/lib.rs:15:5: replace is_done -> bool with true
MISSED   src/lib.rs:15:5: replace is_done -> bool with false
MISSED   src/lib.rs:15:31: replace == with != in is_done
3 mutants tested in 0s: 3 missed
```

Only the new function was mutated (the old, tested function was not touched), and all three mutants were missed: the new code has no test. Two boundary tests (`is_done(30, 29) == false`, `is_done(30, 30) == true`) and one for overshoot (`is_done(30, 31) == true`) kill all three.

## 7. Workflow on a diff

1. Make sure the normal suite is green; mutation tools first run an unmutated baseline and stop if it fails.
2. Produce the diff against the base branch: `git diff origin/main...HEAD > changes.diff`.
3. Run the scoped tool:
   - Rust: `cargo mutants --in-diff changes.diff`
   - JS / TS: list changed source files and pass them: `npx stryker run --mutate $(git diff --name-only origin/main...HEAD -- 'src/**/*.ts' ':!**/*.test.ts' | paste -sd, -)`
4. Triage every survivor (section 8). Write the result in the report: score before and after, survivors left and why.
5. Re-run the scoped tool to confirm the new tests kill the mutants. Then run the normal suite.

Budget: a scoped run on a typical change takes seconds to a few minutes. If it takes longer, scope tighter (one file, the high risk files only) rather than skipping it.

## 8. Triage: kill, equivalent, or not worth it

For each surviving mutant, decide one of three:

| Decision | When | Action |
|---|---|---|
| Kill | The mutant changes behaviour the spec cares about | Add or strengthen a test at the lowest level that can observe it. Assert the output, not that a function was called |
| Equivalent | The mutant cannot change observable behaviour | Note it in the report; optionally restructure the code so the mutant disappears |
| Not worth killing (unproductive) | Killing it would need a test that pins an implementation detail: a log message, a buffer capacity, an internal error string nobody reads | Skip with a reason (`#[mutants::skip]` with a comment, Stryker `// Stryker disable next-line <mutator>: reason`), or exclude the file pattern in config |

Rules:

- Never kill a mutant with a test that asserts on implementation details or on mocks. That trades a missing assertion for a brittle test (Google's "change detector" warning).
- A surviving mutant in an `if` condition near a boundary usually means a missing boundary case: add the 3 value boundary tests from `test-design-techniques.md` section 3.
- A surviving "return default value" mutant usually means the result is never checked: the test calls the function and ignores what it returns.
- Do not chase 100%. The target is: no unexplained survivors in changed high risk code.

## 9. CI setup

- **On pull requests:** run the scoped tool on the diff for the high risk directories. Start as a non blocking report (comment or job summary); make it blocking for the critical folders (billing, auth, sync) once the noise is under control.
- **Nightly or weekly:** a full run on the critical modules, to catch weakening from changes elsewhere.
- **Keep reports:** Stryker's HTML report, `mutants.out/`. Stryker's incremental file can be cached between CI runs.
- **Timeouts:** mutation runs multiply test time; give the job its own timeout and run it after the normal suite passes.

Example GitHub Actions step for Rust (from the cargo-mutants docs pattern; not run here):

```yaml
- name: Mutation test the diff
  run: |
    git diff origin/${{ github.base_ref }}...HEAD > changes.diff
    cargo install cargo-mutants --locked
    cargo mutants --in-diff changes.diff || true   # report only at first; drop "|| true" to block
- uses: actions/upload-artifact@v4
  with: { name: mutants.out, path: mutants.out }
```

## 10. Checks

| Check | Pass condition |
|---|---|
| Scoped | Mutation runs target the diff or named high risk files, not the whole repo on every push |
| Baseline green | The normal suite passed before mutation |
| Every survivor triaged | Each is killed, marked equivalent, or skipped with a written reason |
| Kills are real tests | New tests assert behaviour, not calls on mocks or implementation details |
| Reported | Score before and after, and the remaining survivors, are in the task report |
| Critical modules covered | Billing, auth, sync, parsers and migrations get a scheduled full run |
