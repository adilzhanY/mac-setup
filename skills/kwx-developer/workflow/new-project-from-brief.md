# New project from a brief: building an app when the client cannot be asked

The workflow for an empty or freshly scaffolded folder plus a written brief, when the client cannot be asked (the brief says so, or the run is non interactive). It replaces the house example search of `workflow/codebase-first.md` and the questions of `workflow/audit-and-ask.md` for this case, because there is no house yet and nobody to ask. `workflow/feature-workflow.md` still runs for each feature.

Evidence: in the 2026-11-01 trial all three briefs asked for decisions and open questions in the README and an honest "not finished" list. The skilled builds missed them, wrote machine paths into the README, and filed a missing feature (a 10 visit card that never counted down) as a decision.

## Contents

1. When to use it
2. The shared plan and the requirement matrix
3. Daily user pass
4. Stateful things and their life cycle
5. Promises table
6. Stack and framework choices
7. Decisions without the client
8. Security must haves
9. Budget
10. Handover README
11. Checks

## 1. When to use it

- An empty or new repo plus a brief (a BRIEF.md, a pasted spec, a ticket that describes a whole product).
- The client is unreachable, or the run is non interactive (`claude -p`, a workflow subagent).
- Size class is Large (`SKILL.md` rule 11): one shared plan, at most one builder subagent per side, one targeted tester round.

If the client can be reached, use this file anyway for sections 2 to 6 and 10, and ask the questions of section 7 instead of deciding them.

## 2. The shared plan and the requirement matrix

Write PLAN.md first, in the scratchpad (`workflow/shared-plan.md`). Then build the matrix: copy every numbered brief item, and every sentence with "must", "needs", "has to", "explains" or "shows", into one row each.

| id | Item (quoted from the brief) | Proven by (test name or command) | Status |
|---|---|---|---|
| R1 | "Members book a course and see their remaining visits" | `booking.uses-visit.test.ts` | done |
| R2 | "The README explains what is not finished" | gate K2 loop | partial |
| R3 | "Course times are shown for the Berlin studio" | `schedule.zone.test.tsx` under `TZ=Pacific/Auckland` | missing |

- Status is done, partial or missing. A done row without proof is partial.
- The matrix lives in PLAN.md. At handover every partial or missing row goes to README "Not finished", with the reason.
- A REQUIREMENTS.md in the repo only when the brief or the owner asks for one.

## 3. Daily user pass

Before coding, write the daily workflows the brief implies, and the operator's (admin, export). They are scope, not extras.

- "Replaces a spreadsheet" implies period navigation, totals, quick entry, edit and delete, export.
- "Admin page" implies sign in with a session, sign out, delete with a confirm, export with labels, attempt limits (`backend/auth.md` section 14).
- A "skip what nobody asked for" rule (ponytail, lean) applies to options, abstractions and configurability, never to these.

For a tool used every day, list the 5 jobs the user repeats most and check the API supports each one. Defaults a daily user expects:

- Every report or overview takes a period (`from`, `to`) with the current period as the default, so the UI can step back to last week or last month.
- An entry can be added for a past day in one step, with forgiving input: a parser for words like "gestern" or "yesterday" and for "930", "9:30", "1:30", "1,5", "90m", with tests. The accepted forms are returned by the API or documented, so the UI can show them as hints.
- New entries prefill from the last project and the current time.
- A running timer older than a threshold (for example 10 hours) is flagged as possibly forgotten.
- Every irreversible action (issue an invoice, cancel, delete) has a preview built from the same function as the commit (`data/transactions-and-integrity.md` section 3).
- Derived values the screens show (amount per entry and per period, days overdue, free places) are computed once on the server and returned. The UI never recomputes money.

Any daily workflow not built goes to "Not finished" with the reason.

## 4. Stateful things and their life cycle

Fill the life cycle table from `ai-agents/before-you-code.md` section 8 for every stateful thing the brief shows the user: a visit card, a balance, free places, a waitlist position, an invoice status, a running timer. Each event gets code and a test, including the zero or end case.

A counter that no event changes is a gap, never a decision. Build the smallest event that changes it, or put it at the top of "Not finished".

## 5. Promises table

List every promise the product's own text makes: the privacy policy, terms, FAQ, onboarding copy, the README. Retention periods, deletion on request, consent and its withdrawal, "data never leaves your device", "cancel any time".

| Promise (quoted, with the page) | Kept by (code path or admin action) | Test or check |
|---|---|---|
| privacy page: "we delete your entry on request" | admin delete per entry with a confirm | `admin.delete.test.ts` |
| privacy page: "entries are deleted after 12 months" | Not finished: no retention job yet | README Not finished, line 2 |

- Each promise gets a row: the code path or admin action that keeps it, or a line in "Not finished".
- A privacy text that names consent as the legal basis needs a consent step in the form, or a recorded decision why submitting the form counts as consent.
- The rows live in PLAN.md beside the matrix. Gate K1 reads them.

## 6. Stack and framework choices

- Take the framework's boring, documented default for this kind of product. Every opt in or experimental flag needs a reason in Decisions.
- Choose the rendering model before the first page (`languages/typescript/nextjs.md` section 7). A static marketing site with a form and an admin does not need per request rendering.
- A variant harder than the brief needs (a localized 404, a router trick) is estimated first and usually deferred (`ai-agents/before-you-code.md` section 8).
- A fight with the framework is timeboxed (`ai-agents/verification-loop.md` section 3).
- Built ins before native modules: `node:sqlite` before better-sqlite3 on Node 22.13 and newer (`data/sqlite-and-local-first.md` section 2).

## 7. Decisions without the client

- Never call AskUserQuestion when the client cannot be reached (section 1). The run has nobody to answer, and a blocked question ends the build.
- Decisions go to the README under "Decisions made without the client": numbered, each with the reason and the rejected option.
- Questions go to "Open questions for the client", each with the default you built so the app works today.
- Creating these README sections is required here. This overrides `ai-agents/before-you-code.md` section 7, which says not to create decision files unasked: the brief is the ask.
- A decision may not empty a brief feature. When a brief item stays without its behaviour (a counter never changes, a feature is display only), it goes to the top of "Not finished", not to Decisions.

```markdown
## Decisions made without the client
1. Timer entries under 60 seconds are dropped with a notice. Why: a 0:00 line on an invoice looks like an error. Rejected: keeping them and hiding them on the invoice.

## Open questions for the client
1. Should a cancelled course give the visit back up to 2 hours before start, or 24? Built: 2 hours.
```

## 8. Security must haves

The security must haves of the stack are built, not parked:

- Password rules with a common password blocklist and a lockout safe throttle (`backend/auth.md` sections 5 and 6).
- A session login with sign out for any admin area (`backend/auth.md` section 14).
- Gate F7 with its four probes, results pasted (`quality/quality-gate.md` section 7).

"Documented as not done" passes only when the fix needs infrastructure the brief excludes. Then it is the first line of "Not finished".

## 9. Budget

Write a phase budget in PLAN.md, in this order: map and matrix, data and domain with tests, API, UI duet, one independent test round, handover.

- Each subagent brief names only the matrix rows it owns and the files it may touch.
- One tester round targeted at the risk list (money, dates, auth, the brief's hard rules) is worth its cost. A second open ended round is not.
- End the report with `Cost: <wall time>, <n> subagents, <output tokens when the harness shows them>`.

Trial evidence: the skilled arm used 2.2 to 3.2 times the output tokens of the arm without skills, while reading almost none of the rules that would have prevented its defects. Spend tokens on reading the triggered topic files (`SKILL.md` rule 10) and on targeted tests, not on re-deriving the spec in every pass.

## 10. Handover README

Headings, in this order:

1. Not finished (first, or near the top)
2. Run
3. Test, with the last run's counts, reproduced in this session
4. Build
5. Environment variables (write "none" if there are none)
6. Decisions made without the client
7. Open questions for the client

Portable: no absolute paths of the build machine, no user names, no operator shell dialect (fish `set -x`), no "on this machine" notes. Machine specific tips go in an optional Tips line that uses env vars (`CARGO_TARGET_DIR` as an option, never a path). Gate section 13 (K) checks it.

## 11. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| Requirement matrix | one row per brief item, proof for every done row | read PLAN.md against the brief, item by item |
| Daily workflows | listed, each mapped to a route, handler or test, or in Not finished | read PLAN.md section 2 |
| Life cycle table | every stateful thing has its events and a zero case test, or a Not finished line | read PLAN.md and the test names |
| Promises table | every promise of the product's text has a row | read the legal pages against PLAN.md |
| No questions asked | client unreachable: no AskUserQuestion call in the run | read the transcript or the tool log |
| README headings | all present and filled | gate K2 (the README block under the K table) prints nothing |
| README portable | no machine paths or shell dialect | gate K3 (the README block under the K table) prints nothing |
| Cost line | the report ends with the Cost line | read the report |
