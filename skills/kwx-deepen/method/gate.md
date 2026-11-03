# Step 0: the gate

Decide three things before anything else: whether to deepen, how much, and whether one
question is needed. This step takes seconds; if it takes longer, the task is probably
small enough to skip.

## 1. Deepen or not

Deepen when at least one holds:
- The user asked for it (`/kwx-deepen` or `/deepen`, "go deeper", "do it properly", "like an expert would",
  "improve my prompt first").
- Someone will rely on the result: money, health, law, security, data that could be lost,
  a text that goes public, a decision, a release.
- Amateurs and experts do this task very differently (most tasks in `fields/`).
- The answer depends on facts that are easy to misremember: versions, prices, laws, dates,
  quotes, API signatures, file contents.
- An outside check exists that the request does not mention.

Do not deepen, and do not mention the skill, for: one line edits, renames, typo fixes,
lookups, running a command, formatting, casual chat, and any request that says "quick",
"just", "keep it small" or "no extra steps". Studies of over thinking found models spend
many times the tokens on easy problems whose first answer was already right; the method
is pure cost there (`sources/research_notes/prompting-evidence.md`, section on cost).

## 2. How much

| Task size | Form |
|---|---|
| Small but relied on (an email to a client, one SQL query on production data) | One line per field of the output block |
| Medium (a feature, an article, an analysis) | The full block, at most 10 lines |
| Large (a product, a study, a launch plan) | The full block, plus a short plan of the inputs to fetch first |

The steps before the work always stay much shorter than the work itself.

## 3. One question or none

Ask only when both are true:
1. Two reasonable readings of the request lead to different deliverables (not just
   different details), and
2. No tool can settle it: not the files, not the history, not a search.

Then ask once, at most two or three specific questions, multiple choice where possible
("Is this for the hiring manager or the recruiter screen?"). Models rarely ask on their
own and are poor at spotting ambiguity, so apply the two readings test on purpose instead
of relying on "ask if unclear".

For a personal money, health or legal decision (rent or buy, which job offer, a contract), the
person's own numbers usually decide the answer: income, savings, prices where they live, how
long they will stay, their jurisdiction. Then the one round of questions asks for those, and the
analysis waits for them or works with clearly labelled example figures.

Otherwise write the guess under `Assumptions:` in the rewrite and continue. A visible
assumption the user can correct costs less than a round trip.

## 4. Do not stack

If the harness or another skill already plans, tests or reviews the work, this skill feeds
its rewrite into that process. It does not add a second plan or a second review of the
same thing.
