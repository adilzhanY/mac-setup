# Review method: reviewing a diff or a pull request

How to review a change, whether someone else's pull request, a branch, or your own diff before reporting. The diff alone hides most bugs: the missed caller is in a file the diff does not show, the broken invariant is in the function around the changed lines, and the weakened test looks like a cleanup. So the review reads past the diff, proves every finding, and ranks findings by what they cost users.

## Contents

1. What a review is for, and what it is not
2. Step 1: get the change and its intent
3. Step 2: read past the diff
4. Step 3: run what can be run
5. Step 4: look for these, in this order
6. Step 5: proof per finding
7. Severity and confidence
8. Writing the findings
9. The fresh context reviewer
10. Problems that were already there
11. Checks

## 1. What a review is for, and what it is not

A review answers: does this change do what it claims, without breaking anything else, safely, in the house style? Google's standard: approve once the change definitely improves the overall code health, even if it is not perfect; there is no perfect code, only better code.

Not review findings:

- Formatting, import order, quotes, anything a configured formatter or linter owns.
- Preference where the style guide and the house convention are silent (the author's choice stands).
- Abstractions, options or tests for cases that cannot happen. A reviewer asked to find problems always finds something; fixing every finding grows layers nobody needed (`ai-agents/verification-loop.md` section 5).
- Problems in code the change did not touch (section 10).

## 2. Step 1: get the change and its intent

```bash
git fetch -q origin && git diff --stat origin/main...HEAD          # a local branch
gh pr view <n> --json title,body,files,baseRefName,headRefName     # a pull request (gh-axi pr view <n> in this user's setup)
gh pr diff <n> > "$SCRATCH/pr.diff"
gh pr checkout <n>                                                  # only when you will run checks; never on a dirty tree
```

Write the intent in one line from the title, description and linked issue. If there is no stated intent, derive the acceptance list from the code and say that you did. A change whose diff does more than its intent has a scope finding.

Size it: over about 400 changed lines of logic, review in passes by layer (data, API, client, UI) and say so. Mixed structure and behaviour in one change is itself a finding (`architecture/architecture.md` R17), because it hides behaviour changes inside moves.

## 3. Step 2: read past the diff

For each changed hunk, read:

1. **The whole changed function or component**, not only the changed lines. Most logic bugs sit in the interaction between a changed line and an unchanged one.
2. **Every caller and importer of each changed shape** (signature, type, export, response field, column, event, config key):
   ```bash
   git diff origin/main...HEAD | grep -E '^[-+].*(export |pub fn |fn |function |interface |type |class )' | head -40
   rg -n -w '<changedName>' --glob '!*.lock'
   rg -n "['\"]<field_name>['\"]"          # names used as strings: JSON, SQL, events
   ```
   A caller still using the old shape is the most common agent bug (`ai-agents/ai-agents.md` section 3).
3. **The tests of the changed files**, and the diff of those tests. A changed assertion needs a reason in the intent.
4. **Two house examples** of each kind of file the change adds (`ai-agents/before-you-code.md` section 3), to judge consistency against the codebase, not your taste.
5. **DECISIONS.md and TODO.md** entries for the area (`rg -n -i '<area>' DECISIONS.md TODO.md`). A change that breaks an Accepted decision is a blocker unless the description says the decision is being replaced.
6. **The data path end to end** for anything touching user data: from the input to the write and back to the response.

## 4. Step 3: run what can be run

Run the project's own checks on the branch: typecheck, lint, the tests that cover the changed files, then the full suite. Then the fast checks of `quality/quality-gate.md` section 12 with `BASE` set to the merge base. A red check is a finding with its output as proof. If the branch cannot be checked out or a check cannot run, say which and why; never mark it passed.

## 5. Step 4: look for these, in this order

Order is by cost to users. Stop going deeper on a change that already has a blocker in the first rows: report and let the author fix it first.

| Order | Look for | Typical evidence |
|---|---|---|
| 1 | Data loss or corruption: unsafe migration, delete without scope, read modify write race, transaction around a network call | the migration line and its lock; the query without a tenant filter |
| 2 | Security: missing authorization per object, input not validated, injection, secrets, sensitive logs | the handler with no ownership check; a curl as another user |
| 3 | Wrong behaviour against the intent: logic errors, off by one, null and empty cases, time zones, money rounding | a failing test or a worked input and output |
| 4 | Broken callers and contracts: missed caller, response shape changed in place, client type out of sync | the `rg` hit still using the old shape |
| 5 | Error handling: swallowed errors, hidden failures, a second error style in a layer | the empty catch line |
| 6 | Tests: weakened or deleted assertions, skips, mocks of owned code, no test for a new branch | the test diff hunk |
| 7 | Reliability and performance: no timeout, unbounded list, query in a loop, retries at two layers | the loop with the query |
| 8 | Consistency: a new variant of an export, import, naming, error or test convention | scan before and after (`scripts/scan_conventions.py`) |
| 9 | Over-building: unused options, interfaces with one implementation, dead code added | the option no caller sets |

The full check list per category is `quality/quality-gate.md`; security detail is `security/security.md`; language specific traps are in `languages/typescript/typescript.md` and `languages/rust/rust.md`.

## 6. Step 5: proof per finding

A finding without proof is an opinion. Each one carries one of:

- **A reproduction**: a failing test you wrote (kept in the scratchpad unless asked to push it), or a command with its output (`curl` returning another user's row, `tsc` error, a scan line).
- **A quoted trace**: the lines that show the path, with file:line for each step ("`routes/orders.ts:42` reads `req.body.userId`; `services/orders.ts:17` uses it as the owner; no session check between them").
- **A counterexample input**: the concrete value that breaks it and what happens ("`limit=-1` passes the schema at `schema.ts:8` and becomes `LIMIT -1`, which Postgres rejects with a 500").

If you cannot produce one of these, lower the confidence (section 7) or drop the finding.

## 7. Severity and confidence

| Severity | Meaning | Merge? |
|---|---|---|
| Blocker | Data loss, security hole, broken caller, wrong result on the main path, failing check, weakened test without reason | no |
| Major | Wrong on an edge case users will hit, missing error handling on a real failure, new convention variant, missing test for new logic | not until fixed or explicitly accepted |
| Minor | A real but small cost: an unclear name in a public API, a missing index on a small table | author's call |
| Nit | Cosmetic, optional | leave it out unless asked for nits |

Confidence: **certain** (reproduced), **likely** (traced, not run), **possible** (a pattern that is often wrong; check before acting). Never present a possible as certain.

## 8. Writing the findings

One finding per problem, in severity order:

```text
[Blocker, certain] Orders of other users are readable
Where: src/routes/orders.ts:42 (GET /orders/:id)
What: the handler loads the order by id only; no check that it belongs to the session user.
Proof: curl -H "Authorization: Bearer $USER_B" localhost:3000/orders/17 -> 200 with user A's order.
Fix: scope the query by the session user, as src/routes/invoices.ts:30 does; return 404 when no row.
Test: add "returns 404 for another user's order" next to orders.test.ts:55.
```

Then a summary line: counts per severity, the checks run with results, what was not reviewed and why (generated files, a layer you could not run). Say what is good only when it helps the author keep doing it ("the migration follows expand and contract correctly"), in one line.

Posting: write findings to the user in chat. Post them as PR comments only when the user asks, and then as one review, not a comment per line.

## 9. The fresh context reviewer

For changes you wrote yourself, and for any change touching auth, money, migrations or deletes, get a second read from a context that did not write the code. Start a read only subagent (tools: Read, Grep, Glob, and Bash for read only commands) and give it the code, not your conclusions:

```text
Review this change against its intent. You did not write it; assume nothing is right.
Intent and acceptance list: <paste>
Diff: <path to the diff file in the scratchpad>
Repo: <path>. Project rules: <CLAUDE.md, DECISIONS.md paths>.
Read past the diff: the whole changed functions, every caller of changed names (rg -n -w), their tests.
Do not comment on style, formatting or naming unless it breaks the house convention shown by 2 existing files.
Report only, in this order: data loss, security, wrong behaviour, broken callers or contracts,
swallowed errors, weakened or missing tests, missing timeouts or bounds.
For each: severity (blocker, major, minor), confidence (certain, likely, possible), file:line,
the proof (a command and its output, a quoted trace, or a counterexample input), the fix.
Say "no findings" for a category with none. Do not edit any file.
```

Triage what comes back: fix certain findings, check likely ones with a test or command before changing code, drop findings that ask for abstraction or tests of impossible cases, and say in the report which were dropped and why. Published AI reviewer figures cluster around 50% F1: the second read adds recall, not certainty.

## 10. Problems that were already there

A problem in code the change did not touch is not a review finding against this change. Note it with a key and route it through `workflow/audit-and-ask.md` section 4 (listed at the end, asked only if it matters). Exception: if the change makes an old problem worse or newly reachable (a new route that calls an old unscoped query), it is a finding of this change.

## 11. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| Intent written | one line intent or a derived acceptance list before findings | the review notes |
| Read past the diff | every changed shape has a caller list | the `rg` output in the notes |
| Checks run | typecheck, lint, covering tests and section 12 fast checks ran, or each skip has a reason | commands and results in the summary |
| Proof per finding | each finding has a reproduction, a quoted trace or a counterexample | read the findings |
| Severity and confidence | each finding has both; no possible stated as certain | read the findings |
| No style noise | no finding about what a formatter or linter owns, or pure preference | read the findings |
| Old problems routed | pre-existing problems listed separately with keys, not as review findings | the summary |
