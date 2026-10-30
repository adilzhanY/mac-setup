# Tech debt: asking the owner, prioritising, and writing findings into TODO.md

The audit ([codebase-audit-tools.md](codebase-audit-tools.md)) produces confirmed findings. This file covers what happens next: ranking them, explaining each one to an owner who may not read code, asking what to do, and recording the answer. Every finding ends in exactly one place: an item in `TODO.md` (later), a plan (now), or an entry in `DECISIONS.md` (intentional, [decision-records.md](decision-records.md)).

## Contents

1. What not to raise at all
2. Asking the owner, one finding at a time
3. Prioritising: interest, risk, effort
4. Explaining findings in plain words
5. Writing into TODO.md without duplicates
6. Outcome (b): planning the fix
7. The audit summary
8. Checks

## 1. What not to raise at all

Every finding costs the owner a decision. Drop these before asking:

- Anything a configured formatter or linter already enforces (quotes, semicolons, import order). If no formatter exists, that is one finding ("add Prettier, Biome or rustfmt"), never a list of style nits.
- Personal preference the project's style guide does not cover. Google's review standard: points the style guide does not cover are preference; follow the existing code, and if there is no precedent, the author's choice stands ([standard](https://google.github.io/eng-practices/review/reviewer/standard.html)).
- Framework mandated shapes (Next.js default exports, `GET`/`POST` names, config files).
- Anything matching an Accepted `DECISIONS.md` entry or an open `TODO.md` item.
- Cosmetic issues in cold code (no changes in 12 months, [hotspots.md](hotspots.md)). Interest is only paid when someone works there (Fowler).
- "Rewrite it in X", "add a framework", "should use microservices". Findings are concrete problems in this code, not architecture fashion. Over-engineering is itself a finding Google tells reviewers to watch for.

## 2. Asking the owner, one finding at a time

### The three answers

| Answer | Means | What the agent does |
|---|---|---|
| (a) Later | Real problem, not now | Writes an item into `TODO.md` (section 5). Nothing else changes |
| (b) Plan the fix | Fix it | Writes the plan (section 6), shows it, starts only on the owner's go |
| (c) Intentional | This is how the project should be | Records a `DECISIONS.md` entry and tool exemption ([decision-records.md](decision-records.md) section 7). Never asked again |

There is no silent fourth answer. A finding the owner skips stays unrecorded and is asked again next audit; say that when they skip.

### How to ask

The exact AskUserQuestion wording, the fixed answer labels (`Later`, `Plan a fix`, `Keep as is`) and the batching limits are in `workflow/audit-and-ask.md` section 6; where this section and that one differ, that one wins.

1. First show the ranked summary table (section 7) so the owner sees the whole list before deciding on any item.
2. Ask about P1 and P2 findings one at a time, in rank order. Use the harness's question tool when it exists (Claude Code: `AskUserQuestion`, up to 4 questions per call, 2 to 4 options each); otherwise a numbered chat question. One question per finding, never one question covering unrelated findings.
3. Bundle P3 findings into a single question: "9 small items, all low risk, listed below. Write them all to TODO.md? (yes / let me pick / skip)".
4. Put your recommendation first and say why in one clause. The owner should be able to answer by picking the first option when they trust you.
5. Stop asking after 12 questions in one sitting; write the rest to TODO.md under "Not yet reviewed" and say so.

Question template (fill every slot; no slot may contain unexplained jargon):

```
[P1 · 1 of 7] Refunds and order changes have no tests

What: the two files that handle admin order changes and refunds (app/api/admin/orders/...) were changed 20 times this year, and no automated test checks them.
Why it matters: a mistake there can refund the wrong amount or lose an order's status, and nobody would know until a customer complains.
Effort to fix: about half a day (tests for the 5 main cases).
I recommend (b), plan the fix: this is money and it changes often.

(a) Later: add it to TODO.md
(b) Plan the fix now  [recommended]
(c) Intentional: keep as is and never ask again
```

Bad (what not to send):

```
Finding #14: untested-risk in app/api/admin/orders/route.ts, [id]/route.ts. Coverage 0%. Fix?
```

It has no consequence, no effort, no recommendation, and "fix?" is not one of the three answers.

### When the owner is a developer

Keep the same three answers and the same order. Add the tool evidence (file, line, command output) under the plain text; do not replace the plain text with it.

## 3. Prioritising: interest, risk, effort

### Priority

| Priority | Rule (first match wins) |
|---|---|
| P1 | Can lose or corrupt data, leak data or money, or break auth, in any file. Or: violates an Accepted decision in a top 10 hotspot. Or: a top 5 hotspot with no tests |
| P2 | Any finding in a top 15 hotspot. Any runtime cycle or layering violation (they spread: the next change copies the bad import). Duplicated logic where the copies change together ([hotspots.md](hotspots.md) section 6) |
| P3 | Everything else: style mixes, dead exports, unused dependencies, problems in cold code |

Rationale: Fowler's interest is paid on every change to the code, so frequency of change decides the cost of leaving it; Tornhill and Borg measured 15 times more defects and 124% longer development in low quality code, which concentrates where the changes are. Risk to users overrides churn because one data loss costs more than any slowdown.

### Effort

| Size | Meaning | Examples |
|---|---|---|
| S | under 1 hour, one commit, no behaviour change | Rename one file, switch one default export, delete an unused dependency |
| M | under 1 day, a few commits, tests included | Break one runtime cycle, extract a duplicated helper and cover it, add tests for one risky route |
| L | more than a day, needs a plan and stages | Split a 4000 line hotspot, move a layer boundary, replace an error handling style across a crate |

Estimate from the code you read (number of call sites: `grep -rn name src | wc -l`; number of files in scope), not from the finding kind.

### Which answer to recommend

Use Fowler's debt quadrant to word the recommendation ([TechnicalDebtQuadrant](https://martinfowler.com/bliki/TechnicalDebtQuadrant.html)):

| The finding looks... | Quadrant | Recommend |
|---|---|---|
| A known shortcut with a reason ("we'll ship and fix later"), in cold code | Prudent, deliberate | (a), or (c) if the reason still holds |
| A local style that the folder consistently follows on purpose | Not debt, a convention | (c) |
| An accident (copy paste, a forgotten import direction, a leftover file) | Inadvertent | (b) if P1 or P2, (a) if P3 |
| A risky shortcut in a hotspot or on a money, data or auth path | Reckless | (b), always |

## 4. Explaining findings in plain words

The owner decides on impact, risk and effort, not on tool vocabulary. Translate each kind:

| Kind | Plain words for the owner |
|---|---|
| `cycle` | Two parts of the program depend on each other, so neither can be changed or tested on its own. Changes there break things in surprising places. |
| `layering` | A part that should not know about another part reaches into it (for example the calculations reach into the screen code). It makes the calculations impossible to test without the screen. |
| `duplicate` | The same logic exists in two places. When one is fixed, the other keeps the bug. |
| `dead-code` | Code nothing uses. It costs reading time and can mislead whoever changes the code next. Removing it is safe and cheap. |
| `unused-dep` | A library the project installs but no longer uses. It makes installs slower and adds security updates to watch for nothing. |
| `export-style`, `naming`, `import-style` | The same thing is written two ways. Each new piece of code has to guess which way, and searches miss half the matches. Low risk, small effort. |
| `error-handling` | Failures are reported in different ways in different places, and in some places they are hidden. Hidden failures mean users see wrong results without an error. |
| `untested-risk` | Important code that changes often has no automatic check. A mistake there reaches users. |
| `hotspot` | One file takes most of the changes and has grown complicated, so every new feature there takes longer and breaks more. |
| `coupling` | Two files always have to be changed together, so one idea lives in two places. Forgetting one causes bugs. |
| `lint` | The language's own checker warns about a pattern in N places. Usually low risk; sometimes a real bug. |

Rules for the plain text:

- Name the consequence for users or for the speed of future work, not the principle. "Breaks the single responsibility principle" is not a consequence.
- Use real numbers from the audit: "changed 193 times this year", "2 copies", "41 of 42 files".
- Say the effort in hours or days, not story points.
- Never claim certainty you do not have: "can lose an order's status if X" is better than "will cause bugs".
- No blame, no "bad code", no "messy". The code may be the result of a good decision under old constraints (Fowler: even good teams learn the right design only after building).

## 5. Writing into TODO.md without duplicates

### Read the file's own conventions first

Read the whole `TODO.md` before writing. This user's repos differ: numbered parts with item ids (`CA.1`, `CB.4`) and "Done:" notes (bauwerk), milestones `M0`..`M10` (sahna), numbered sections ordered "by what hurts users most" with a "Rules for working this list" section (torq). Match:

- heading style and numbering (`## 11. Audit 2026-10-30` if sections are numbered, `## Audit 2026-10-30` if not),
- the checkbox and id style (`- [ ] **[3] Title**`, `- [ ] A.3 Title`),
- wrapping (hard wrapped at 80 if the file is, one line per paragraph if not),
- the file's ordering rule (if it says "ordered by what hurts users most", put P1 items where they belong in that order and say where you put them).

If there is no `TODO.md`, create one with `# TODO` and the audit section.

### Where in the file

Default: one new section per audit at the end, `## Audit YYYY-MM-DD`, with a one paragraph header (what was checked, the hotspot window, counts) and three subsections `### P1`, `### P2`, `### P3` in that order. Items the owner did not review go under `### Not yet reviewed`. Never scatter audit items across unrelated sections, except when the file's own ordering rule demands it.

### Item format

```markdown
### P1

- [ ] **A1. Admin order routes have no tests** `untested-risk:app/api/admin/orders`
      `app/api/admin/orders/route.ts`, `app/api/admin/orders/[id]/route.ts`. Changed 20 times in 12 months (hotspot #6). Refunds and status changes; no test imports either file.
      Impact: a broken refund or status change reaches customers unnoticed. Effort: M (half a day).
```

- Id: `A<n>` numbered within this audit (or the file's own id style).
- The finding key in backticks on the title line. It is what makes de-duplication and later matching mechanical.
- Paths in backticks, with line numbers when the finding is a spot (`src/geometry/energy.ts:2`).
- One line of evidence with numbers, one line of impact plus effort.
- No plan here unless the owner chose (b).

### Never duplicate

Before writing each item:

```bash
key='untested-risk:app/api/admin/orders'
grep -nF "$key" TODO.md                                   # same key anywhere?
grep -nF 'app/api/admin/orders' TODO.md                   # same paths under other wording?
```

| Found | Do |
|---|---|
| An open item with the same key or paths about the same problem | Do not add. Append one line to that item: `Seen again in audit 2026-10-30: still no tests, now 20 changes.` |
| An open item about the same paths but a different problem | Add the new item; mention the other id in its evidence line |
| A done `[x]` item for the same key and the problem is back | Add a new item titled `... (regressed, was A1 in Audit 2026-10-09)` |
| Nothing | Add the item |

Also check `DECISIONS.md` (a (c) answer from an earlier audit means it must not be in TODO at all) and check that the item is not already fixed in the working tree (`git diff`, `git log -5 -- <path>`).

### Closing items

Tick `[x]` in place and add the file's style of done note (`Done: ...` with what changed and how it was verified). Never delete an item; the history of what was fixed is part of the file.

## 6. Outcome (b): planning the fix

Write the plan as sub-items under the TODO item, so the plan and its progress live in one place (torq's audit section does this):

```markdown
- [ ] **A1. Admin order routes have no tests** `untested-risk:app/api/admin/orders`
      (evidence and impact lines as above)
  - [ ] Write a failing test first for each case: refund full, refund partial, refund twice, status change by a non-admin (expect 403), unknown order (expect 404).
  - [ ] Use the existing test database helper (`test/utils/pgliteDb`), the same way `promocodeEconomics.test.ts` does.
  - [ ] Fix whatever the tests expose, one commit per bug.
  - [ ] Verify: `npm test -- app/api/admin` green; `npm run typecheck` clean.
```

Plan rules:

- Smallest steps that each leave the build and tests green. For an L item, stages that can ship separately; never one big rewrite.
- Tests first for anything with behaviour (reproduce, then fix).
- Reuse what the repo already has (its test helpers, its error type, its folder pattern); the plan names them.
- A verify line with the exact command.
- For a style fix in many files, the plan includes the enforcement rule (ESLint, ast-grep, depcruise) so the problem cannot come back, and records the convention in `DECISIONS.md` as the rule's why.
- Show the plan, then wait for the owner's go before editing code.

## 7. The audit summary

Shown before the questions, short enough to read in a minute. Example shape (counts illustrative):

```markdown
## Audit 2026-10-30: whaleabyss

Checked 412 source files (TypeScript), 373 commits, hotspot window 12 months. Typecheck clean, lint clean, 96 tests green.

Biggest risks:
1. Admin order and refund routes change often and have no tests.
2. The pluralisation helper exists twice; a fix to one will miss the other.
3. lib/ has one file exporting differently from the other 41.

| # | Finding | Priority | Effort | Recommend |
|---|---|---|---|---|
| A1 | Admin order routes have no tests | P1 | M | (b) plan |
| A2 | `plural` defined in two components | P2 | S | (b) plan |
| A3 | Default export in lib/cropUtils.ts | P3 | S | (a) or (c) |

Skipped as already decided: D-07 (default export in cropUtils), D-08 (anyhow everywhere). Already in TODO.md: 2 (seen-again notes added).
```

- Lead with a one line state of health and the counts, then the top 3 risks in plain words, then the table.
- Name what was skipped because of decisions and existing TODO items, so the owner trusts that nothing was lost.
- Name what could not be checked (no tests to run, no git history, a tool that failed).

## 8. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| Every finding resolved | Each confirmed finding is in exactly one of: TODO.md, a plan, DECISIONS.md, "Not yet reviewed" | Count findings in the summary table against the three files |
| Three answers offered | Every question offers (a), (b), (c) with a recommendation | Read the questions sent |
| Plain words | Each question has What, Why it matters, Effort, Recommendation; no unexplained term from the kind list | Read the questions; grep for `cycle\|layering\|coupling` without a following explanation |
| No duplicate TODO items | No finding key appears on two open items | The open-key command below prints nothing |
| Seen-again instead of re-adding | Re-found open items got a dated "Seen again" line | `grep -n 'Seen again in audit' TODO.md` |
| File conventions kept | New section matches the file's heading, id and wrap style | `git diff TODO.md` read side by side with an older section |
| Nothing deleted | No removed lines in TODO.md except a `[ ]` to `[x]` change | `git diff TODO.md \| grep '^-' \| grep -v '^---'` shows only checkbox lines |
| Priority rule applied | Every P1 is data, money, auth, a decision violation in a top 10 hotspot, or an untested top 5 hotspot | Read each P1's evidence line |
| Effort grounded | Each M or L estimate mentions the count of call sites or files | Read the items |
| Plan before code | No code edited for a (b) finding before the owner's go | Conversation order; `git log` timestamps |

Open-key command (prints any finding key held by two or more open items):

```bash
grep -E '^\s*- \[ \]' TODO.md | grep -oE '`[a-z-]+:[^`]+`' | sort | uniq -d
```
