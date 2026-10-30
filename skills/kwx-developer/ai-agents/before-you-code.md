# Before you code: read the codebase first

What to read before the first edit, how to find the house pattern for the thing you are about to write, how to find helpers to reuse, how to map callers, and how to work in a repo too big to read.

Why this file exists: the agent's main source of conventions is the code it reads, and it copies whatever it reads first. In big repos the failure is not reasoning but finding the right files: on SWE-bench Pro, Claude Sonnet 4's top failures were context overflow (35.6%) and endless file reading (17.0%), and agents that pass nearly everything under 10K lines average 15.3% above 50K lines. Evidence: strong for the size effect, inference for the copying mechanism.

## Contents

1. The reading order (15 minutes, not 2 hours)
2. Find the real check commands
3. Find the house pattern: 2 examples, copy their shape
4. Find helpers before writing one
5. Map every caller before changing a shape
6. Big repos: search, do not read everything
7. DECISIONS.md and TODO.md
8. Define done before the first edit
9. Checks

## 1. The reading order

Read in this order and stop as soon as you can write the plan. Each item has a reason.

| Step | Read | Why |
|---|---|---|
| 1 | `CLAUDE.md`, `AGENTS.md`, `.claude/rules/*.md`, `.cursor/rules/*`, `.github/copilot-instructions.md`, and the nested ones on the path to the files you will touch (`find . \( -name AGENTS.md -o -name CLAUDE.md \) -not -path '*/node_modules/*'`) | the team's operational rules; nearest file wins |
| 2 | `DECISIONS.md`, `docs/adr/`, `TODO.md` | choices already made and work already planned (section 7) |
| 3 | CI config: `.github/workflows/*.yml`, `.gitlab-ci.yml`, `Makefile`, `justfile`, `package.json` scripts, `pyproject.toml` tool sections | the commands that actually gate a merge (section 2) |
| 4 | manifest and lockfile | what is installed and at which version, before you reach for anything new |
| 5 | the entry point of the feature (route, command, screen, job) and the call path down to the code you will change | so the edit lands in the live path, not in a copy or legacy module |
| 6 | 2 existing examples of the thing you will write (section 3) | the house pattern |
| 7 | the tests of the files you will change | the expected behaviour, the test style, and what must keep passing |

Skip the README's architecture tour unless the task needs it. Overviews did not shorten the path to the files a fix needed (Gloaguen et al.). Evidence: medium.

## 2. Find the real check commands

The commands in CI are the definition of "passes". Write them down before editing; you will run them in `verification-loop.md`.

```bash
rg -n 'run:' .github/workflows/ 2>/dev/null | head -40     # GitHub Actions steps
jq -r '.scripts' package.json 2>/dev/null                    # npm / pnpm / bun scripts
rg -n '^[a-z][a-z0-9_-]*:' Makefile justfile 2>/dev/null     # make / just targets
rg -n '^\[tool\.' pyproject.toml 2>/dev/null                 # ruff, mypy, pytest config
```

Record: format, typecheck, lint, test (all), test (one file or one test), build, and how to start the app locally. If the instruction file names a command, use that one over anything you infer. Reason: agents follow named commands almost perfectly. Evidence: strong (Gloaguen: `uv` used 1.6 times per task when named, under 0.01 otherwise).

## 3. Find the house pattern: 2 examples, copy their shape

Before writing a new endpoint, component, migration, CLI command, job, hook, store or test, find 2 existing ones of the same kind and copy their shape. Reason: naming a canonical example is the instruction vendors converge on, and describing a style does not work. Evidence: vendor claim (Anthropic "follow the pattern in HotDogWidget.php"), weak to medium in measurement.

How to pick the 2:

1. Same kind of thing, in the same area of the repo as your change (same package, feature folder or crate).
2. The most recently added ones. Older code may carry a pattern the team has dropped.
   ```bash
   # files added most recently under a path, newest first
   git log --diff-filter=A --name-only --format='%ad' --date=short -- 'src/routes/' | head -30
   ```
3. Not from a folder the instruction files call legacy or "do not copy".
4. If the instruction file names an example, that one wins.

What to copy from them, as a checklist:

- [ ] file location and file name pattern
- [ ] export style (named or default, barrel file or direct)
- [ ] import style (alias or relative, order)
- [ ] how input is validated (which schema library, where)
- [ ] how errors are raised and returned (which helper, which error type)
- [ ] how it logs (which logger, which fields)
- [ ] how auth or permissions are checked (and where: keep it next to the route)
- [ ] how it is registered (router table, DI container, plugin list, menu)
- [ ] its test: file location, framework, fixtures, assertion style

When the 2 examples disagree, pick the one in the same area and the newer one, say which you chose and why in the report, and do not invent a third style. To see where the repo disagrees with itself:

```bash
python3 -I ${CLAUDE_SKILL_DIR}/scripts/scan_conventions.py <repo-root>
```

## 4. Find helpers before writing one

Before writing any function that formats, parses, validates, converts, fetches, retries, caches, logs, or wraps an error, search for one that already does it. Reason: copy-pasted code is rising and moved (reused) code is falling. Evidence: weak (GitClear, correlational, vendor).

Search in this order and stop at the first hit that fits:

1. The project's shared folders: `rg --files | rg -i '(^|/)(utils?|lib|helpers?|shared|common|core|internal)/'`
2. The verb and the noun of what you need, as names and in comments:
   ```bash
   rg -n -i 'def (format|parse|to)_?date|function (format|parse)Date|fn (format|parse)_date'
   rg -n -i 'retry|backoff' --type ts --type py --type rust -l
   ```
3. Installed dependencies that already cover it (date library, HTTP client with retries, schema validator): read the manifest.
4. The standard library.
5. Only then write a new helper, in the shared folder the examples use, and name the searches you ran in the report ("searched utils/, lib/, `rg -i slugify`: none found").

If you find two existing helpers for the same job, use the one the newer code calls, and note the duplicate as a follow-up. Do not merge them inside this task.

## 5. Map every caller before changing a shape

Before you change a function signature, a type, a return shape, an exported name, an API response, a DB column, an event payload or a config key, list every reader of the old shape. Reason: patches that pass their own tests but break a caller elsewhere are the clearest measured agent failure (29.6% of "passing" SWE-bench patches diverge), and giving the agent the list of covering tests cut regressions by 70%. Evidence: strong.

```bash
rg -n -w 'createInvoice'                      # every textual use, including strings and docs
rg -n -w 'createInvoice' -g '*test*' -g '*spec*' -l   # the tests that touch it
rg -n "['\"]invoice_total['\"]"               # keys used as strings: JSON, SQL, config, events
```

Then add the precise tools the stack has: LSP "find references", `tsc --noEmit` after the change, `cargo check`, `go build ./...`, `pyright`. In dynamic code (Python, JS) only the grep and the tests find callers; the typechecker will not.

Write the list into the plan: each caller file, whether it needs a change, and the tests that cover it. You run those tests first in the verification loop.

## 6. Big repos: search, do not read everything

Signs you are in one: `git ls-files | wc -l` over about 2,000 files or `cloc` over 50K lines. A bigger context window does not fix it (NL2Repo-Bench). Evidence: strong.

1. Size it: `git ls-files | wc -l`, then `git ls-files | cut -d/ -f1-2 | sort | uniq -c | sort -rn | head -20` for the shape.
2. Search for the domain words in the task (the entity, the error message, the route, the UI label): `rg -n -i 'refund' -l | head -30`. An error message or UI string from the task is the fastest way to the live code path.
3. Build a symbol map when names matter more than bodies: `ctags -R -x --languages=Python,TypeScript,Rust,Go . | rg -w Invoice`, or the agent's own repo map tool. A token-budgeted repo map retrieved better than plain keyword search in one 2026 benchmark. Evidence: medium.
4. Read only: the files on the change path, the 2 examples, the callers from section 5, and their tests.
5. Budget: if you have opened about 30 files and have no written plan, stop reading and write the plan with what you know, marking the unknowns. Long, erratic runs predict failure. Evidence: medium.
6. For a broad sweep across many folders, hand it to a read-only search subagent and keep only its conclusion, so the file dumps stay out of your context.

## 7. DECISIONS.md and TODO.md

Many projects keep their non-obvious choices in `DECISIONS.md` (or `docs/adr/NNNN-*.md`) and planned work in `TODO.md`. These are exactly the facts an agent cannot rediscover from the code. Evidence: vendor claim (Anthropic: write down "decisions not in the repo").

Before coding:

- Read both. Search them for the area you touch: `rg -n -i 'auth|session' DECISIONS.md TODO.md docs/adr/`.
- If the task conflicts with a recorded decision (it asks for Redis where DECISIONS.md says "no Redis, Postgres only"), stop and ask before writing code. Quote the decision.
- If TODO.md already has the task or a related item, follow what it says about scope.

After coding:

- Append any decision you made that a later reader could not see in the code: one entry, dated, with the reason and the option you rejected.
  ```markdown
  ## 2026-10-30: Invoice numbers come from a Postgres sequence
  Why: gapless per year is not required, and a sequence is safe under concurrency.
  Rejected: max(number)+1 in app code (races under two servers).
  ```
- In TODO.md, tick what you finished and add the follow-ups you noticed but did not do (duplicate helper, missing test, outdated dependency). Adding the item is the right move; doing the work inside this task is scope creep.
- If the project has neither file and you made a decision worth keeping, say so in the report and offer to create it. Do not create it unasked.

## 8. Define done before the first edit

Write down what "done" means before editing. Reason: without a check to run, "looks done" is all the agent has. Evidence: vendor claim (Anthropic), consistent with TDAD.

- Bug: a failing test that reproduces it, through the real code path. See `tests-and-honesty.md`.
- Feature: a short acceptance list (inputs, outputs, error cases, who may call it), plus the tests that will prove each item.
- Refactor: "behaviour identical", proven by the existing suite plus a differential check (see `tests-and-honesty.md`).
- If the task is underspecified on something that changes the design (data model, public API, permissions), ask one round of questions before coding. Underspecified multi-turn work loses about 39% on average because early assumptions stick. Evidence: medium.

## 9. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| Instruction files read | every CLAUDE.md / AGENTS.md on the path read | `find . \( -name AGENTS.md -o -name CLAUDE.md \) -not -path '*/node_modules/*'` and each was opened |
| Check commands recorded | format, typecheck, lint, test, single test, build written down | the plan lists them, taken from CI or the instruction file |
| House examples named | 2 example files named for each new kind of file | the plan names them with paths |
| Helper search done | searches listed before any new helper | the report names the rg queries and their result |
| Callers mapped | every changed shape has a caller list and covering tests | rg / LSP output in the plan |
| Decisions respected | no conflict with DECISIONS.md, or the user approved it | `rg -n -i '<area>' DECISIONS.md docs/adr/` reviewed |
| Done defined | a failing test or an acceptance list exists before the edit | the test file or list is in the plan |
