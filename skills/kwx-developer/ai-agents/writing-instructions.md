# Writing instructions for agents: CLAUDE.md and AGENTS.md

How to write and maintain a project's agent instruction file so agents actually follow it, what goes in and what stays out, which rules belong in lint, hooks and CI instead, and how to add a lesson after a mistake.

Why this file exists: controlled studies found that instruction files barely move task success (LLM-generated files: about 0.5 to 2% lower success and 20 to 23% more cost; developer-written files: about 2.4% better, not significant, up to 19% more cost), yet agents obey them closely: a tool named in the file was used 1.6 times per task against under 0.01 when not named, and repo-specific tools went from under 0.05 to 2.5 uses. Instruction files are a steering wheel, not an engine: they change which commands, helpers and examples the agent uses. Evidence: strong for compliance, medium for the null effect on success.

## Contents

1. What an instruction file can and cannot do
2. What goes in
3. What stays out
4. How to write each line
5. Size, order and layout
6. Mechanical rules go to lint, hooks and CI
7. Adding a lesson after a mistake
8. Maintaining the file
9. A skeleton
10. Checks

## 1. What an instruction file can and cannot do

- **Can**: make the agent run the right commands, use the house helper, copy the right example, avoid a known trap, respect a decision made outside the code. These are operations, and agents follow named operations almost perfectly.
- **Cannot**: make the agent a better designer. Failures that remain with a good file are "feature design, pattern choice, and exact wiring" (Khatri 2026, small study). Those need examples, tests and review.
- **Cannot guarantee anything.** CLAUDE.md is delivered as a user message "with no guarantee of strict compliance" (Anthropic). A rule that must hold every time belongs in a hook, deny rule or CI (section 6).

## 2. What goes in

Apply Anthropic's two-question test to every candidate line: could the agent find this by reading the code, and would it actually go and look? If both are yes, leave it out. Evidence: vendor claim.

What passes the test:

| Kind | Example line |
|---|---|
| Exact commands, including a single test | `Test one file: pnpm vitest run src/billing/invoice.test.ts` |
| House example to copy, per kind of file | `New API route: copy the shape of src/routes/invoices.ts (validation with zod schema in src/schemas/, errors via src/lib/errors.ts).` |
| The helper the team settled on | `Errors: throw AppError from src/lib/errors.ts; never throw strings or plain Error in handlers.` |
| Misleading places | `src/legacy/ is still live (billing v1) but do not copy its patterns into new code.` |
| Decisions not visible in code | `Money is integer cents everywhere (DECISIONS.md 2026-03-02).` |
| Non-functional requirements | `Every new route checks permissions in the handler with requirePerm(); no route is public unless listed in src/routes/public.ts.` |
| Traps that cost time | `Tests need the test DB: docker compose up -d db-test first.` |
| Anything corrected twice | the operation that fixes the repeated mistake (section 7) |

Security and performance are worth an explicit line: only 14.8% and 14.5% of real context files mention them, while AI code picks the insecure option in about 45% of security-relevant tasks. Evidence: strong for the gap.

## 3. What stays out

| Leave out | Why | Evidence |
|---|---|---|
| Architecture overview, file layout tour | the agent reads the repo itself; overviews did not shorten the path to the right files and raised cost | medium (Gloaguen), vendor claim (Anthropic retired it) |
| Generic quality advice ("write clean code", "be thorough", "be more accurate") | adds noise, changes nothing | vendor claim (GitHub, Devin, Anthropic) |
| "Keep going, don't be lazy, loop until done" | "more likely to cause over-work than fix a stall" | vendor claim (Anthropic) |
| ALL CAPS, IMPORTANT, CRITICAL emphasis | "piling on emphasis mostly makes Claude over-apply the rule" | vendor claim (Anthropic) |
| A pasted style guide | a linter enforces it and the agent knows common conventions | vendor claim (Cursor) |
| Copied community template rules | 28.7% of Cursor rule lines are verbatim copies whose effect nobody tested | medium (Jiang and Nam) |
| Rare one-off edge cases | every line takes attention on every task | vendor claim |
| Content duplicated from the README or code | goes stale; point to the file instead | vendor claim (Cursor) |
| An LLM-generated `/init` dump kept unedited | lowered success slightly and raised cost about 20% | medium (Gloaguen) |

## 4. How to write each line

1. **Write an operation, not a description.** Name the command, the file, the helper.

   | Description (does not change behaviour) | Operation (does) |
   |---|---|
   | We value consistent error handling. | Throw `AppError` from `src/lib/errors.ts` in handlers. |
   | Keep tests up to date. | After changing `src/billing/`, run `pnpm vitest related <files> --run`. |
   | Follow our component conventions. | New component: copy `src/ui/Button/` (folder with `index.ts`, `Button.tsx`, `Button.test.tsx`). |
   | Be careful with the database. | Migrations: `pnpm db:migrate:dev` only; prod migrates in CI. |

2. **Say what to do, then why, in one line.** "Use `uv run` for every Python command, because the system Python lacks the dev dependencies." Reasons let the model judge exceptions. Evidence: vendor claim (Anthropic).
3. **Prefer "do X" over "do not Y".** Negative instructions suppress the behaviour less reliably. Evidence: weak (small studies). When a "do not" is needed, pair it with the alternative: "Do not hand-roll fetch calls; use `apiClient` from `src/lib/api.ts`."
4. **Show correct and incorrect code side by side** for a pattern that is easy to get wrong. Evidence: vendor claim (GitHub).
   ```ts
   // yes
   const user = await db.query.users.findFirst({ where: eq(users.id, id) });
   // no: raw SQL strings in handlers
   const user = await db.execute(`select * from users where id = ${id}`);
   ```
5. **Point to files, do not copy them.** "See `src/routes/invoices.ts`" stays true when the file changes; a pasted snippet goes stale. Evidence: vendor claim (Cursor).
6. **Plain wording.** No caps, no "MUST", no "CRITICAL". If a plainly worded rule keeps being missed, the file is too long or the rule belongs in a hook. Evidence: vendor claim (Anthropic; its skill guide still allows "MUST" for a rule that keeps slipping, a mild tension).
7. **No contradictions.** "If two instructions contradict each other, Claude may pick one arbitrarily." Search the file and its nested siblings for the topic before adding a line.

## 5. Size, order and layout

| Mechanism | Size guidance | Source |
|---|---|---|
| CLAUDE.md | under 200 lines per file; imports do not reduce context cost | Anthropic memory docs |
| Codex AGENTS.md | 32 KiB combined across the directory chain | OpenAI Codex docs |
| Cursor rule | under 500 lines each | Cursor docs |
| Copilot code review | only the first 4,000 characters are read | GitHub docs |
| SKILL.md | body under 500 lines, references one level deep | Anthropic skill docs |

- **Most important first.** Models favour earlier instructions, and frontier models follow only about 68% of 500 simultaneous instructions. Evidence: medium (IFScale).
- **Headings and short bullets**, grouped by task (commands, patterns, decisions, traps), not dense paragraphs.
- **Nest by scope.** A root file for the whole repo; a file in `packages/api/` for API-only rules; `.claude/rules/*.md` with a `paths:` glob for rules that only matter for some files. The nearest file wins.
- **One source for several tools.** Keep the content in `AGENTS.md` (read by Codex, Cursor, Copilot, Gemini CLI and others) and make `CLAUDE.md` a one-line import, `@AGENTS.md`, plus any Claude-only lines.
- **Procedures used only sometimes go in a skill**, not in the always-loaded file. Only a skill's name and description load each session.

## 6. Mechanical rules go to lint, hooks and CI

"If something has to happen every time, make it a hook, a deny rule, or a managed setting. CLAUDE.md is for guidelines, and Claude is allowed to decide a guideline doesn't apply." (Anthropic). Evidence: vendor claim, consistent with the incident record in `safety-and-destructive-actions.md`.

| The rule | Where it goes | Example |
|---|---|---|
| Zero exceptions, and an agent breaking it does damage | deny rule or PreToolUse hook | never edit `migrations/` that are applied; never `rm -rf`; never read `.env` |
| Must hold before the work counts as done | Stop hook and CI | typecheck and tests green |
| Mechanically checkable style or structure | formatter, linter rule, CI | import order, no relative imports across packages, no bare `catch`, no `console.log` |
| Checkable but custom | a small script in the repo, run by CI, named in the file | "no new file in `src/` without a test file"; "no dependency added without an entry in DECISIONS.md" |
| Judgement with exceptions | a line in the instruction file | "prefer named exports"; "prefer the query builder over raw SQL" |

Keep the enforced set small. "If you ever find yourself at forty of them, most are probably preferences that Claude could have weighed on its own" (Anthropic). When a rule moves into a tool, replace its prose with one line naming the tool: "`pnpm lint` enforces import boundaries; fix its errors, do not disable the rule."

## 7. Adding a lesson after a mistake

Add a rule only after a mistake repeats, or after one that was costly. Codex: add rules "only after you notice repeated mistakes"; Anthropic: write down "anything you've had to correct twice already"; Mitchell Hashimoto: each line answers an observed bad behaviour, ideally paired with a tool, and "it almost completely resolved them all". Evidence: vendor claim and practitioner report.

The procedure:

1. **Pin the mistake down in the diff.** What exactly did the agent do (file, line, command), and what should it have done instead? "Agent wrote a new `formatCurrency` in `src/components/Price.tsx`; `src/lib/money.ts` already has `formatMoney`."
2. **Check whether the file already covers it.** `rg -n -i 'money|currency' CLAUDE.md AGENTS.md .claude/rules/`. If a line exists and was ignored, the file is probably too long or the line is vague: shorten or rewrite, do not add a second line.
3. **Can a tool catch it?** If yes, add the tool first: a lint rule (`no-restricted-imports`, a Ruff banned-api entry, a clippy `disallowed_methods` entry), a hook, a test, a CI script. Then write one line naming it.
4. **Otherwise write one operation line** with the house file and the reason: "Money formatting: use `formatMoney` from `src/lib/money.ts` (handles currency and locale); do not write a new formatter."
5. **Put it in the narrowest file that covers the mistake**: a nested `AGENTS.md` or a path-scoped rule rather than the root, when the mistake only happens in one area.
6. **Test it when you can**: rerun a task like the one that failed in a fresh session, and see whether the line changes the behaviour.
7. **Record why, briefly**, in the commit message ("Add money helper rule: agent duplicated formatMoney twice"), so a later cleanup knows the line earned its place.

A one-off mistake gets fixed in the code and nothing else. A file that grows a line for every slip becomes the long file nobody follows.

In the moment, when the agent keeps failing in one session: after two failed corrections, start a fresh session with a better prompt instead of a third correction, since multi-turn conversations lose about 39% on average to early assumptions that stick. Evidence: medium (Laban et al.), vendor claim (Anthropic).

## 8. Maintaining the file

Review the file when the code it names changes, and at least when it passes about 150 lines.

- **Every path and command still exists**: run the check script in section 10.
- **Every line still passes the two-question test.** Delete lines the agent would now find by reading the code.
- **Delete prose for anything now enforced by a tool**, leaving at most one line that names the tool.
- **Delete rules written for older models**: emphasis, "think step by step", "don't be lazy". Claude Code's `/doctor prompt-audit` flags instructions written for older models, missing files and contradictions.
- **Review diffs to instruction files like code.** They steer every agent run, and a malicious line in one is an attack (the Amazon Q wipe prompt arrived as a merged PR).

## 9. A skeleton

```markdown
# <project>

## Commands
- Install: `pnpm install --frozen-lockfile`
- Dev server: `pnpm dev` (needs `docker compose up -d db`)
- Typecheck: `pnpm tsc --noEmit`
- Lint: `pnpm lint` (enforces import boundaries; fix errors, do not disable rules)
- Test all: `pnpm test`. One file: `pnpm vitest run <file>`. Related: `pnpm vitest related <files> --run`

## Patterns to copy
- API route: `src/routes/invoices.ts`. UI component: `src/ui/Button/`. Migration: `db/migrations/0042_add_refunds.sql`.
- Errors: `AppError` from `src/lib/errors.ts`. Money: integer cents, format with `formatMoney` from `src/lib/money.ts`.
- Permissions: call `requirePerm()` in every handler; public routes are listed in `src/routes/public.ts`.

## Traps
- `src/legacy/` is live billing v1. Do not copy its patterns.
- `pnpm db:reset` wipes the dev DB, including seeded fixtures used by e2e tests.

## Decisions
- See DECISIONS.md. Read it before changing auth, billing or the data model.

## Done means
- Typecheck, lint and tests green; the report lists each command and its result, and anything not checked.
```

## 10. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| Length | under 200 lines per CLAUDE.md, review-critical rules in the first 4,000 characters | `wc -l CLAUDE.md AGENTS.md` and `head -c 4000 AGENTS.md` |
| Paths exist | every backticked path in the file exists | script 1 below prints nothing |
| Commands run | every listed command runs | run each command once |
| No emphasis | no caps emphasis words | script 2 below prints nothing |
| No overview | no architecture or layout tour sections | read the headings: `rg -n '^#' CLAUDE.md AGENTS.md` |
| Operations | each rule names a command, file or helper | read each bullet; rewrite any that only describe |
| Enforced rules not duplicated | rules covered by a hook or lint have one line naming the tool, not a paragraph | compare against `.claude/settings.json`, lint config, CI |
| Each lesson traced | each rule added after a mistake has a commit message naming the mistake | `git log --format='%h %s' -- CLAUDE.md AGENTS.md` |

```bash
# 1. backticked paths that do not exist (run from the repo root)
rg -o '`[A-Za-z0-9_./-]+/[A-Za-z0-9_.-]+`' -N --no-filename CLAUDE.md AGENTS.md .claude/rules 2>/dev/null \
  | tr -d '`' | sort -u | while read -r p; do [ -e "$p" ] || echo "missing: $p"; done
# 2. emphasis words
rg -n -w 'IMPORTANT|CRITICAL|MUST|NEVER|ALWAYS' CLAUDE.md AGENTS.md .claude/rules 2>/dev/null
```
