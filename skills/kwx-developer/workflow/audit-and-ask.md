# Audit and ask: finding organisation problems and letting the owner decide

How the skill finds problems that break its rules (mixed export styles, two error styles in one layer, duplicated helpers, layering violations, risky code without tests) and what it does with each one. The owner may not be a developer. For every problem the agent asks one plain question with three answers, records the answer where the next session will read it, and never asks the same question twice. It never fixes a problem the owner was not asked about.

The details of each tool, the decision format and the TODO format live in the quality files. This file is the procedure that ties them together and the exact wording of the question.

## Contents

1. Two triggers, two modes
2. Rules for both modes
3. Mode A: the full audit, step by step
4. Mode B: problems noticed during a normal task
5. Batching: how many questions, in what order
6. The question: AskUserQuestion wording
7. After answer (a): the TODO.md item
8. After answer (b): the plan
9. After answer (c): the DECISIONS.md entry
10. Other answers, skips and silence
11. Never re-ask, never fix unasked
12. Checks

## 1. Two triggers, two modes

| Trigger | Mode | What the agent does |
|---|---|---|
| The user asks for it: "audit this repo", "find inconsistencies", "review the whole codebase", "what is messy here", "clean up the structure" | A, full audit | runs section 3, shows a ranked summary, asks about each finding, records every answer |
| The agent notices a problem while doing something else (a feature, a fix, a review) | B, noticed in passing | finishes the task first, in the house style, then lists what it noticed and asks only about the findings that matter (section 4) |

A request to fix one named problem ("the exports in lib/ are mixed, fix them") is not an audit: the user has already chosen (b). Plan it (section 8) and build it with `workflow/feature-workflow.md`.

## 2. Rules for both modes

1. **Map first.** Run `workflow/codebase-first.md` if the repo is not mapped in this conversation. The do-not-flag list (Accepted decisions with an `Audit:` key) and the open TODO keys come from it.
2. **A lead is not a finding.** A tool hit, a scan OFF/MIX/ODD line or a grep match becomes a finding only after you open the file, read the lines, and check two files from each side of a mix. Drop false positives silently.
3. **Majority decides, not taste.** An inconsistency is relative to the area's own majority or to the precedence in `architecture/consistency.md` section 2. A codebase that consistently does something you would not choose has no finding, unless it breaks a safety rule (swallowed errors, injection, secrets, unsafe migrations, missing authorization).
4. **Framework shapes are never findings** (Next.js `page.tsx` default exports, `GET`/`POST` names, Expo Router routes, config files, Rust `main.rs`): `quality/codebase-audit-tools.md` section 0 rule 8.
5. **One finding per pattern per area.** 41 files one way and 1 file the other way is one finding about that file.
6. **Every finding gets a key** `kind:area` from the fixed list in `quality/codebase-audit-tools.md` section 10 (`export-style:lib`, `error-handling:src/api`). The key is how TODO.md and DECISIONS.md are matched later.
7. **Nothing is changed before an answer.** No code edit, no config file, no lint rule, no installed tool in the repo. Audit tools run through `npx -y`, `uvx` or a scratch prefix, with configs in the scratchpad (`quality/codebase-audit-tools.md` section 0 rule 4).

## 3. Mode A: the full audit, step by step

Copy this list into your notes and tick it off.

```
- [ ] 1 Map: workflow/codebase-first.md, all steps (do-not-flag list, open TODO keys, checks, scan)
- [ ] 2 Project checks: typecheck, lint, tests with the project's own commands; failures are findings first
- [ ] 3 Hotspots: quality/hotspots.md section 5, top 15 kept for ranking
- [ ] 4 Tools in order: quality/codebase-audit-tools.md section 1 (size, cycles and layers, dead code, duplication, census, custom rules, clippy, tests gap)
- [ ] 5 Organisation read: architecture/architecture.md section 4 steps 7 and 8 (read the 5 largest and 5 hottest files, one feature end to end)
- [ ] 6 Language and risk passes: languages/typescript/typescript.md or languages/rust/rust.md audit sections; reliability/reliability.md section 4; security/security.md; data/data.md section 5 checks
- [ ] 7 Confirm, filter, group, key: quality/codebase-audit-tools.md section 10
- [ ] 8 Rank and size: quality/tech-debt-and-todo.md section 3 (P1, P2, P3; effort S, M, L)
- [ ] 9 Summary to the owner: quality/tech-debt-and-todo.md section 7
- [ ] 10 Ask: sections 5 and 6 of this file
- [ ] 11 Record each answer: sections 7, 8, 9
- [ ] 12 Final report: what was checked, counts per answer, what could not be checked
```

Scope and time. A whole repo audit of a mid size repo takes about 15 to 30 minutes of tool time. If the user named a folder or a concern ("just the API", "only exports"), audit only that and say what was left out. For a big repo, audit the top 15 hotspots and the folders the user cares about, and say so in the summary.

Filter before ranking (`quality/decision-records.md` section 6 step 5):

```bash
# keys of Accepted decisions with their scope
awk '/^## /{id=$2; a=""; off=0} /Replaced by|Superseded by|\*\*Proposed|\*\*Rejected/{off=1}
     /^Audit:/{a=$0} /^Scope:/ && a && !off {print id"\t"a"\t"$0}' DECISIONS.md 2>/dev/null
# keys of open TODO items
grep -E '^\s*- \[ \]' TODO.md 2>/dev/null | grep -oE '`[a-z-]+:[^`]+`' | sort -u
```

| The finding | Do |
|---|---|
| same key, path inside an Accepted decision's Scope | drop it; do not mention it or ask |
| same key, path outside the Scope | report it and name the related decision; never widen a scope yourself |
| breaks an Accepted decision (code violates D-05) | report it one priority higher, quoting the decision |
| a decision's `Revisit when:` trigger has happened | ask once, quoting the entry |
| matches an open TODO key | do not ask; add a dated "Seen again in audit" line to that item |
| already fixed in the working tree | drop it |

## 4. Mode B: problems noticed during a normal task

The task comes first. The owner asked for a feature or a fix, not an audit, and a derailed task is the worst outcome of this mode.

While working:

1. When you see a candidate in a file you already opened for the task, write one line in your notes: `path:line, kind, what`. Do not open extra files to chase it and do not run audit tools for it.
2. Write your own code in the house style of the area you are in, even when the area is the minority variant and even when you would choose differently. Never add a third variant (`architecture/consistency.md` section 9).
3. The one exception to copying the house style: never copy a pattern that breaks a safety rule. If the neighbouring code swallows errors, builds SQL from strings or skips the authorization check, write yours correctly and say in the report that it differs from its neighbours on purpose.
4. Do not fix what you noticed, even when it is one line, unless the task cannot be done correctly without that change (then it is part of the task, and the report says so).

Stop and ask in the middle of the task only when a finding makes the task unsafe or impossible: the task conflicts with an Accepted decision, the code you must change can lose or corrupt data, or the task depends on behaviour that is clearly broken. Ask one question, quote the evidence, wait.

At the end, after the task report:

1. Confirm each noted candidate by reading the lines again (a minute, not an investigation). Drop the ones that fail rule 2, 3 or 4 of section 2.
2. Drop anything on the do-not-flag list or in an open TODO item.
3. Rank with the priority rule in `quality/tech-debt-and-todo.md` section 3.
4. Ask with AskUserQuestion only about findings that matter: every P1, and P2 findings in files the task touched. At most 4, in one call.
5. List the rest in a short "Also noticed" block, one line each with its key, and offer once: "Say 'audit' and I will go through these with you, or I can write them all to TODO.md." Do not ask about them one by one.

The report shape for this mode:

```text
Done: <the task, one line>. Ran: <checks and results>. Not checked: <list>.

Noticed while working (not changed):
1. [P2] In src/api/, 6 handlers report errors by throwing and 2 return { ok: false }. (error-handling:src/api)
2. [P3] lib/formatDate.ts shares its function the other way from the 41 files around it. (export-style:lib)
I have one question about item 1 (below). Item 2 is small; say 'audit' to go through it, or I can add it to TODO.md.
```

## 5. Batching: how many questions, in what order

1. Before any question in mode A, show the ranked summary table (`quality/tech-debt-and-todo.md` section 7) as plain chat text, so the owner sees the whole list first.
2. One question per finding for P1 and P2, never one question covering unrelated findings. AskUserQuestion takes up to 4 questions per call: send findings in rank order, 4 per call.
3. All P3 findings go into one bundled question (section 6, second example).
4. Stop after 12 questions in one sitting (3 calls). Write the rest to TODO.md under `### Not yet reviewed` and say so.
5. Record each answer as soon as it arrives (sections 7 to 9), before sending the next call. A session that ends halfway keeps the answers already given.

## 6. The question: AskUserQuestion wording

Every question has the same parts, in plain words: what was found (with real numbers and one example path), why it matters for users or for future work, the effort to fix, and the three answers with the recommended one first. Translate tool words with the table in `quality/tech-debt-and-todo.md` section 4; "export" becomes "how a file shares its functions with other files".

Fixed answer labels and descriptions (keep them word for word, so the owner learns them):

| Answer | Label | Description |
|---|---|---|
| (a) later | `Later` | It is a real problem, but not now. I write it in TODO.md so it is not lost. Nothing in the code changes. |
| (b) plan | `Plan a fix` | I write a short step by step plan and show it to you. I change code only after you say go. |
| (c) keep | `Keep as is` | It is on purpose: this is how the project is meant to be. I record it in DECISIONS.md and never ask about it again. |

Labels stay short because the tool shows them as buttons; the description carries the meaning. The `header` is at most 12 characters (`lib/ files`, `API errors`). Put the recommended answer first and add ` (Recommended)` to its label; the other two follow in a, b, c order. Recommend with the quadrant table in `quality/tech-debt-and-todo.md` section 3: (b) for anything on a money, data or auth path or in a hotspot, (c) when a whole folder consistently does it its own way, (a) for small accidents in quiet code. If TODO.md or DECISIONS.md does not exist yet, say in that option's description "TODO.md does not exist yet; I will create it at the project root."

Example, one finding:

```json
{
  "questions": [{
    "header": "lib/ files",
    "question": "In lib/, 41 files share their functions with the rest of the app in one way, and 1 file, lib/formatDate.ts, does it the other way. Anyone adding code has to guess which way to follow, and a search for where a function is used misses the odd file. Fixing it takes about 15 minutes and changes no behaviour. What should I do?",
    "multiSelect": false,
    "options": [
      {"label": "Later (Recommended)", "description": "It is a real problem, but not now. I write it in TODO.md so it is not lost. Nothing in the code changes."},
      {"label": "Plan a fix", "description": "I write a short step by step plan and show it to you. I change code only after you say go."},
      {"label": "Keep as is", "description": "It is on purpose: this is how the project is meant to be. I record it in DECISIONS.md and never ask about it again."}
    ]
  }]
}
```

Example, the P3 bundle (the only question whose answers differ, because a "keep" decision needs a scope and a reason per item):

```json
{
  "header": "Small items",
  "question": "9 small, low risk items are listed above (unused code, a library installed but never used, two files named differently from their neighbours). What should I do with them?",
  "multiSelect": false,
  "options": [
    {"label": "All later (Recommended)", "description": "I write all 9 in TODO.md. Nothing in the code changes."},
    {"label": "Plan fixes for all", "description": "I write one plan covering all 9 and show it to you before changing anything."},
    {"label": "One by one", "description": "I ask about each one, with the same three answers as before."}
  ]
}
```

When the owner is a developer, keep the same wording and add the evidence (file:line, the command and its output) in chat text right before the question. Never replace the plain words with the evidence.

Without the AskUserQuestion tool, ask in chat with the same text and a numbered list `1) Later (recommended)  2) Plan a fix  3) Keep as is`, and wait.

## 7. After answer (a): the TODO.md item

Read the whole TODO.md first and match its heading, id, checkbox and wrap style (`quality/tech-debt-and-todo.md` section 5). Check for a duplicate before writing:

```bash
key='export-style:lib'; grep -nF "$key" TODO.md; grep -nF 'lib/formatDate.ts' TODO.md
```

If an open item already covers it, append `Seen again in audit YYYY-MM-DD: <what changed>.` to that item instead. Otherwise add, under the audit's section (`## Audit YYYY-MM-DD`, subsections `### P1`, `### P2`, `### P3`; in mode B use `## Noticed YYYY-MM-DD`):

```markdown
- [ ] **A3. lib/formatDate.ts shares its function differently from the rest of lib/** `export-style:lib`
      `lib/formatDate.ts:1` uses a default export; the other 41 files in `lib/` export by name. Changed 4 times in 12 months (cold).
      Impact: new code guesses the wrong style; "find usages" misses this file. Effort: S (15 minutes, 3 importers).
```

Then say in one line: "Added A3 to TODO.md." Nothing else changes.

## 8. After answer (b): the plan

Write the plan as sub items under the TODO item (create the item first, as in section 7), so the plan and its progress live in one place (`quality/tech-debt-and-todo.md` section 6):

```markdown
- [ ] **A3. lib/formatDate.ts shares its function differently from the rest of lib/** `export-style:lib`
      (evidence and impact lines as above)
  - [ ] List every importer: `rg -n "from ['\"].*formatDate['\"]"` (3 found: Invoice.tsx, Receipt.tsx, report.ts).
  - [ ] Change `export default function formatDate` to `export function formatDate`; update the 3 imports. Structure only, its own commit.
  - [ ] Add the guard so it cannot come back: `import-x/no-default-export` for `lib/**` in eslint.config.js (the repo already runs ESLint).
  - [ ] Verify: `pnpm tsc --noEmit` clean, `pnpm eslint lib` clean, `pnpm test` green; scan shows no ODD line for lib/.
```

Plan rules: smallest steps that each leave the build green; tests first for anything with behaviour; reuse the repo's own helpers and tools (name them); a guard (lint rule, ast-grep rule, dependency-cruiser rule) for every convention fix, after the owner agrees to it; a verify line with exact commands; for an L item, stages that ship separately (`architecture/evolving-a-codebase.md`).

Show the plan in chat in plain words (what will change, what the owner will notice, how long), then wait for "go". On go, build it, then run `workflow/feature-workflow.md` steps 10 and 11 (checks loop, gate), tick each sub item as it is done, and finish with the file's done note style (`Done: 2026-10-30, 3 importers updated, lint rule added, checks green`). If the fix records a convention ("lib/ exports by name"), add it to DECISIONS.md as the guard's why.

## 9. After answer (c): the DECISIONS.md entry

Follow `quality/decision-records.md` section 7. Match the file's existing style; if there is no DECISIONS.md, create it with the header in section 2 of that file and add one line to the project's CLAUDE.md or AGENTS.md only if the owner agrees ("Read DECISIONS.md before changing structure or auditing; never re-flag an Accepted decision."). The entry:

```markdown
## D-07 Default export kept in lib/formatDate.ts

2026-10-30. **Accepted.**
Audit: export-style:lib
Scope: `lib/formatDate.ts`
Keep: the default export of `formatDate`.
Why: <the owner's reason in plain words, or "Owner's call, no reason given">
Revisit when: <a checkable trigger, or leave the line out>
Enforced by: nothing, reviewed by hand.
```

- Scope is exactly what the owner said: one file is that file, not the folder.
- Ask one short follow-up ("Why should it stay? One sentence is enough.") only when the reason decides the scope. Never invent a reason.
- If the owner keeps something that is a real risk (a swallowed error on a payment path, a secret in the repo), say the risk once in one plain sentence before recording, and record it under Why.
- Add the D-id to a tool exemption only where the project already has that tool configured (`quality/decision-records.md` section 7 step 3).
- Show the entry in one short block, then go on to the next question.

## 10. Other answers, skips and silence

| The owner | Do |
|---|---|
| types their own answer ("Other") | map it to (a), (b) or (c) if it clearly is one, and confirm in one line; if it is an instruction ("fix it now"), treat it as (b) with go already given, still showing the plan first in one block |
| gives a reason with (c) | use their words for Why |
| skips a question or ends the session | record nothing for it; say once: "Unanswered items are not recorded, so I will ask about them again next time." In mode A, write them under `### Not yet reviewed` in TODO.md |
| says "stop asking" | stop, write the remaining findings under `### Not yet reviewed`, and say how many |
| disagrees that it is a problem | that is answer (c); record it |

## 11. Never re-ask, never fix unasked

Never re-ask:

- Before any question, match the finding's key and path against the do-not-flag list and the open TODO keys (section 3 commands). A match is never asked again, in any mode, in any later session.
- A finding the owner skipped is the only kind that comes back.
- The one exception is a decision's `Revisit when:` trigger that has happened: ask once, quoting the entry.

Never fix unasked:

- No edit to code, tests, config or lint rules for a finding before answer (b) and the owner's go on the plan.
- In mode B the diff contains only the task. A reviewer reading it must not find a "while I was here" change.
- Recording an answer (TODO.md, DECISIONS.md) is not a fix and needs no further go: the answer was the permission.
- Commit TODO.md and DECISIONS.md changes on their own, with a one line message, only when the project's rules say to commit.

## 12. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| Map and filters first | do-not-flag list and open TODO keys built before the first finding | the audit notes list both, with counts |
| Findings confirmed | each finding cites a file:line that was opened, and both sides of a mix | read each finding |
| No re-asked decision | no question matches an Accepted `Audit:` key inside its Scope, or an open TODO key | compare the questions with the section 3 command output |
| Three answers, plain words | every question has what, why it matters, effort, the three fixed labels, recommended first | read the AskUserQuestion calls |
| Batching kept | at most 4 questions per call, 12 per sitting, P3 bundled | count the calls |
| Every answer recorded | each (a) has a TODO item, each (b) a plan under its item, each (c) a D-entry | `git diff --stat -- TODO.md DECISIONS.md` and read the additions |
| No duplicate TODO item | no key on two open items | `grep -E '^\s*- \[ \]' TODO.md \| grep -oE '\`[a-z-]+:[^\`]+\`' \| sort \| uniq -d` prints nothing |
| No unasked fix | the diff holds only the task (mode B) or only answered (b) plans with a go | `git diff --stat` read against the task and the answers |
| Task not derailed | in mode B the task was finished before any non blocking question | conversation order |
