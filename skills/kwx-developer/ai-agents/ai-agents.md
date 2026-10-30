# AI agents: how coding agents fail and the guards that work

Master file for working as an AI coding agent in a real codebase, and for auditing code an agent wrote. Read this first, then the file the task needs.

The research in one line: agents fail by producing changes that look done and pass the nearest test while being wrong somewhere else, and the guards that measurably help are operations and structure (named commands, named example files, tests the agent cannot edit, hooks, CI, scoped credentials), not descriptions or prohibitions.

## Contents

1. Files in this folder and when to read them
2. Evidence strength key
3. The failure modes table
4. The 12 operations that hold on every task
5. Stop signals: when to stop and report instead of pushing on
6. Auditing code an agent wrote
7. Checks

## 1. Files in this folder

| File | What is in it | Read when |
|---|---|---|
| `before-you-code.md` | what to read first, finding the house pattern (2 examples), finding helpers to reuse, mapping callers, big repos, DECISIONS.md and TODO.md | before the first edit of any task in an existing codebase |
| `change-discipline.md` | small diffs, every caller and importer, no unrequested changes, no invented dependencies, current APIs, no swallowed errors, no stubs, the "not checked" report | while making the change, and when reviewing a diff |
| `tests-and-honesty.md` | never weaken a test, the "flag the broken test" exit, covering tests first, passing is not proof, property, differential and mutation tests | any change that runs or touches tests, any bug fix |
| `verification-loop.md` | the ordered loop (format, typecheck, lint, covering tests, full suite, fresh review), commands per stack, a check that cannot run, full stack checks without a browser | before saying a task is done |
| `safety-and-destructive-actions.md` | incident table, destructive command protocol, dev and prod separation, scoped credentials, secrets in commits, approval gates and hooks | any command that deletes, resets, migrates, deploys or touches credentials |
| `writing-instructions.md` | writing and maintaining CLAUDE.md / AGENTS.md, what goes in and out, mechanical rules to lint and hooks, adding a lesson after a mistake | creating or editing an instruction file, or after the agent repeated a mistake |

## 2. Evidence strength key

Every rule in this folder carries one of these labels.

- **strong**: measured by several independent studies or labs, or a consistent public incident record.
- **medium**: one solid study, or several studies with caveats (small sample, autocomplete not agents, benchmark not field).
- **weak**: correlational data, practitioner reports or anecdote; the direction is consistent but the size is unknown.
- **vendor claim**: guidance or numbers from a vendor (Anthropic, OpenAI, GitHub, Cursor, a tool seller), not independently checked.

## 3. The failure modes table

| Failure | How it shows up in a diff | Guard that works | Evidence |
|---|---|---|---|
| Editing, skipping or special-casing tests | changed assertions, deleted test cases, new `skip`/`xfail`/`.only`, `exit(0)`, `SkipTest`, literal expected values in production code, monkeypatched `time` or `==` | test files read-only to the agent (hook or permissions), an explicit "flag the broken test" exit, held-out or mutation tests, a human reads every test diff | strong (METR 30.4% where the grader was visible; Anthropic impossible tasks 51 to 78% without a prompt; ImpossibleBench: flag exit cut GPT-5 from 54% to 9%) |
| Partial change that misses callers | signature changed in one file, old call shapes still present elsewhere; only the nearest test was run | list every caller with grep or LSP before the change, run the tests that cover them, then typecheck and the full suite | strong (29.6% of "passing" SWE-bench patches behave differently; telling the agent which tests cover the change cut regressions 70%) |
| Right idea in the wrong file | a fix in a copy, a dead module or a legacy path; the live path untouched | trace the call path from the entry point before editing; confirm with a failing test that goes through the real path | medium (SWE-bench Pro "incorrect file" bucket) |
| Getting lost in a big repo | very long run, dozens of files read, repeated edits to the same lines, context overflow | targeted search (rg, LSP, repo map) instead of reading, a read budget, write the plan after the search | strong (SWE-bench Pro: 35.6% context overflow, 17% endless reading; scores under 16% above 50K lines) |
| Insecure code | string-built SQL, unescaped HTML output, missing authz check on a new route, secrets in code, weak crypto | explicit security requirements in the task, SAST in the loop, authz check written next to the route, review | strong, flat across model versions (Veracode 45% insecure choices in 2025, about 44% in 2026) |
| Invented dependency | a new package in the manifest that does not exist, is days old, or is a typo of a real one | prefer stdlib and installed packages; check the registry (age, downloads, repo) and add only through the package manager so the lockfile records it; ask before adding | strong (19.7% of recommended packages did not exist; 43% of fake names recur every run) |
| Outdated or deprecated API | calls the installed version marks deprecated or no longer has; copied from old code nearby | read the installed version from the lockfile, read that version's docs or type definitions, turn on the deprecation lint | medium (ICSE 2025, completion models; outdated context makes it worse) |
| Destructive action | `rm -rf` with `~` or an unquoted path, `migrate reset`, `DROP`, `push --force`, delete and recreate of an environment | deny rules and a PreToolUse hook, separate dev and prod, scoped credentials, backup plus the user's explicit go | strong incident record (9+ public data loss incidents; prompt rules failed in 3+) |
| Secret committed | `.env`, tokens, keys or cookies in the staged diff | scan the staged diff (`gitleaks protect --staged`) before every commit, `.env` in `.gitignore` | medium (GitGuardian: Claude Code assisted commits 3.2% vs 1.5% baseline, secondary coverage) |
| Oversized, unfocused diff | hundreds of lines, several unrelated purposes, reformatting mixed with logic | one purpose per change, refactor and behaviour change in separate commits, report follow-ups instead of doing them | medium (each extra line about 1% lower merge odds; AI PRs 154% larger) |
| Scope creep and over-engineering | new options, abstractions, files or validation nobody asked for | build only what the task names, validate at system boundaries only, list ideas as follow-ups | weak to medium (27.3% of divergent patches added unrequested behaviour; Anthropic says recent Opus models over-build: vendor claim) |
| Duplicated helper, convention drift | a new `formatDate` next to an existing one; a new file shaped unlike its neighbours | search for the helper before writing one; copy the shape of 2 existing examples; lint rules for boundaries | weak (GitClear: copy-paste up, refactoring down; correlational, vendor) |
| Swallowed error, hidden failure | empty `catch`, `except Exception: pass`, `let _ = ...`, a fallback value that hides a failed call | use the project's named error helper, lint for bare catches, report failures plainly | weak (GitClear "error-masking" up 47%; Claude 4 card: "plausible-seeming solutions without acknowledging flaws") |
| Stub left behind | `TODO`, `todo!()`, `NotImplementedError`, placeholder returns, sample data in a production path | grep the diff for stub markers before finishing; finish or list as not done | weak (practitioner reports; Replit agent fabricated 4,000 records to cover a failure) |
| "Done" without evidence | "all tests pass" with no command, no output, no list of what was skipped | report each command run with its result, and every check not run with the reason | vendor claim (Anthropic: "'All tests pass' on its own tells you very little") |

## 4. The 12 operations that hold on every task

Each one names the action, the reason, and the evidence. The detail lives in the topic file.

1. **Read the project's instruction files, DECISIONS.md and TODO.md, and find the real check commands in CI before the first edit.** The agent obeys named commands almost perfectly (a tool named in AGENTS.md was used 1.6 times per task vs under 0.01 otherwise). Evidence: strong for compliance. See `before-you-code.md`.
2. **Find 2 existing examples of the thing you are about to write and copy their shape.** The agent copies whatever it reads first, so choose what it reads. Evidence: weak to medium, vendor claim (Anthropic: "follow the pattern in X").
3. **Search for an existing helper before writing a new one, and say which searches you ran.** Duplication is rising and refactoring is collapsing. Evidence: weak.
4. **Before changing a signature, type, schema or exported name, list every caller and importer, and the tests that cover them.** Missed callers are the main reason passing patches are wrong. Evidence: strong.
5. **Define done before editing: a failing test or a written acceptance list.** "Looks done" is all an agent has without a check. Evidence: vendor claim, consistent with TDAD.
6. **Keep the diff to one purpose; list everything else as a follow-up.** Large diffs are rejected more and reviewed worse. Evidence: medium.
7. **Never edit, delete, skip or loosen a test to make a change pass; when a test looks wrong, stop and report it with evidence.** Giving the agent this exit is the measured fix. Evidence: strong.
8. **Run covering tests first, then the full suite, after format, typecheck and lint.** Executable feedback is what lets models repair code; self re-reading is not. Evidence: strong.
9. **Add no dependency that is not already installed without checking the registry and asking.** Fake package names repeat and get squatted. Evidence: strong.
10. **Write code against the installed version's API, read from its docs or types, not from memory.** Evidence: medium.
11. **No destructive command on data or files outside the workspace without a backup and the user's explicit go.** Every real fix after an incident was structural, but the protocol stops the agent from being the trigger. Evidence: strong.
12. **End with a report: what changed, each command run and its result, what was not checked and why.** Evidence: vendor claim.

## 5. Stop signals

Stop, write down what you know, and report to the user instead of continuing when any of these happens. Each one predicts a bad outcome.

| Signal | Why it matters | Evidence |
|---|---|---|
| Two attempts at a general fix failed on the same test | special-casing appears after several failed attempts; more retries against the same visible tests raised cheating from 33% to 38% | strong (Anthropic 3.7 card, ImpossibleBench) |
| The only way to green is to change a test, a fixture or a CI file | that is test gaming whatever the intent | strong |
| The task contradicts a recorded decision, a test, or itself | underspecified multi-turn work loses 39% on average because early assumptions stick | medium (Laban et al.) |
| 30+ files read with no plan written, or the run keeps circling | failed runs are longer and more erratic than successful ones | medium (Majgaonkar et al.) |
| A command would delete, reset or overwrite data you did not create in this task | see `safety-and-destructive-actions.md` | strong |
| A check cannot run (no DB, no network, missing env) | an unrun check reported as passed is a false claim | vendor claim |

## 6. Auditing code an agent wrote

Run these on a branch or a repo with heavy agent output. Each line is a lead to read, not a verdict.

```bash
# test gaming: test files changed in the same commits as source, skips added
git log --format='%h %s' --name-only -- '**/*test*' '**/*spec*' | head -100
rg -n '\.(only|skip)\(|@pytest\.mark\.(skip|xfail)|#\[ignore\]|t\.Skip\(|SkipTest|exit\(0\)' -g '!node_modules'
# swallowed errors
rg -nP 'catch\s*(\([^)]*\))?\s*\{\s*\}|except(\s+Exception)?\s*:\s*pass|let _ = |_ = err\b|\.catch\(\(\)\s*=>\s*\{?\s*\}?\)'
# stubs and placeholders
rg -n 'TODO|FIXME|XXX|todo!\(|unimplemented!\(|NotImplementedError|not implemented|lorem ipsum|placeholder' -g '!*.md'
# duplicated helpers: same function name defined in several files
rg -o --no-filename -NP '^\s*(?:export\s+)?(?:pub(?:\([\w:]+\))?\s+)?(?:async\s+)?(?:function|def|fn)\s+\K\w+' | sort | uniq -c | sort -rn | awk '$1>1' | head -30
# dependencies added recently, to check against the registry
git log -p --since='3 months ago' -- package.json pyproject.toml Cargo.toml go.mod requirements*.txt | rg '^\+\s'
```

Convention drift across areas: `python3 -I ${CLAUDE_SKILL_DIR}/scripts/scan_conventions.py <repo-root>`.

## 7. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| Instruction files read | CLAUDE.md, AGENTS.md (root and nested), DECISIONS.md, TODO.md opened if present | list them in the report |
| Callers listed | every changed exported symbol has a caller list | the report or plan contains the rg / LSP output |
| No test weakening | no test file changed unless the task changes that behaviour, each change justified | `git diff --stat -- '*test*' '*spec*' tests/` is empty or each line is explained |
| Loop run | format, typecheck, lint, covering tests, full suite each ran | each command and its result is in the report |
| No new unchecked dependency | every added package was checked and approved | `git diff -- package.json pyproject.toml Cargo.toml go.mod` reviewed |
| No stub or swallowed error added | none in the diff | the rg lines in section 6, run on `git diff` output |
| Not checked list | present, even if empty | the final report has a "Not checked" line |
