# Scoring rubric for code changes

Score every finished change from 0 to 5 on each dimension below, after running `quality/quality-gate.md`. A score is a judgement backed by evidence: write one line per dimension saying why it earned that level. Dimensions that do not apply (no data change, no API) are N/A and leave the average.

## Contents

1. Minimum to ship
2. Dimensions and levels
3. How to score
4. Example
5. Checks

## 1. Minimum to ship

- **Hard fails** (ship is blocked whatever the scores): any [critical] gate row open; a check reported as passing that did not run; a weakened or skipped test without a reason the task requires; a secret in the diff; a destructive command run without the user's yes.
- **Correctness, Security, Data safety, Honesty**: at least 4 each.
- **Every other dimension**: at least 3.
- **Average** over the dimensions that apply: at least 4.0.

A 3 is "works, nothing a user or the next developer would trip over". A 4 is "a strong team would merge this without comments". A 5 is "a reference codebase would use it as the example".

## 2. Dimensions and levels

### Fit with the codebase

| Level | Looks like |
|---|---|
| 0 | Written as if the repo did not exist: new structure, new libraries, new style |
| 1 | Ignores the house examples; a new variant of exports, errors or naming |
| 2 | Mostly house style, but a duplicated helper or a second way of doing something |
| 3 | Copies the house examples; scan diff clean; no new dependency |
| 4 | Reuses existing helpers and layers; names use the domain's words; the change lands in one place |
| 5 | Reads as if the original authors wrote it; the next change in this area got easier |

### Correctness

| Level | Looks like |
|---|---|
| 0 | Does not do what was asked, or breaks existing behaviour |
| 1 | Main path works; callers or other paths broken |
| 2 | Main path and callers work; edge cases (empty, null, limits, time zones) wrong |
| 3 | Every acceptance item proven; obvious edge cases handled |
| 4 | Edge cases from the spec all tested; concurrency and retries considered where they apply |
| 5 | Invariants enforced by types or the database so wrong states cannot be built |

### Tests

| Level | Looks like |
|---|---|
| 0 | No tests, or tests weakened to pass |
| 1 | Tests exist but assert little (only that a mock was called) |
| 2 | Happy path tested; no error path; owned code mocked |
| 3 | Each acceptance item and each new branch tested, including one error path, against real dependencies the project owns |
| 4 | Contract test between layers; tests through the public interface; fail before, pass after shown |
| 5 | Property, differential or mutation testing where correctness matters most |

### Error handling

| Level | Looks like |
|---|---|
| 0 | Errors swallowed; failures look like success |
| 1 | Errors caught and logged, then the code continues as if it worked |
| 2 | Errors propagate, but in a second style for the layer, or without context |
| 3 | House error model, context added, logged once where handled, safe user messages |
| 4 | Stable machine codes the client maps to states; expected outcomes are values, bugs crash |
| 5 | Error cases designed out where possible; every failure has a tested recovery path |

### Data safety

| Level | Looks like |
|---|---|
| 0 | Can lose or corrupt data: unsafe migration, unscoped delete, race on writes |
| 1 | Data safe on the happy path; a retry or crash halfway corrupts it |
| 2 | Atomic writes, but invariants only in app code; migration locks a big table |
| 3 | Constraints in the database, transactions where needed, lock safe additive migration |
| 4 | Idempotent mutations, expand and contract for shape changes, backfills batched |
| 5 | Restore path known and tested for the touched data; rollback command written down |

### Security

| Level | Looks like |
|---|---|
| 0 | Injection, missing authorization, or a secret in the diff |
| 1 | Authorization by role only, not per object; input partly validated |
| 2 | Per object authorization, but a sink or a log leaks data |
| 3 | Every never cut rule of `security/security.md` holds for the change |
| 4 | Abuse cases tested (another user's object, oversized input); rate limits where abusable |
| 5 | Least privilege throughout; the change reduces attack surface |

### Performance and bounds

| Level | Looks like |
|---|---|
| 0 | Unbounded list, query in a loop on a growing table, blocking IO in async code |
| 1 | Bounded, but no index for the new query on a growing table |
| 2 | Indexed and bounded; offset pagination on a user facing list |
| 3 | Keyset pagination, timeouts on remote calls, no N+1 |
| 4 | Query plans checked on realistic data; concurrency bounded |
| 5 | Measured against a budget, with before and after numbers |

### API and client contract

| Level | Looks like |
|---|---|
| 0 | Client and server disagree on a shape; a shipped field removed in place |
| 1 | Shapes typed twice by hand; error responses vary per route |
| 2 | One error envelope, but the client ignores codes and shows a generic failure |
| 3 | One source for shapes, house envelope and codes, every UI state has a signal |
| 4 | Contract test; retries and cache invalidation correct; additive changes only |
| 5 | Generated or shared types end to end; the contract is impossible to break silently |

### Scope and simplicity

| Level | Looks like |
|---|---|
| 0 | Unrequested rewrites, features or refactors mixed in |
| 1 | Task done plus "while I was here" changes |
| 2 | Only the task, but over built: options, layers or interfaces nobody uses |
| 3 | Only the task, the smallest change that fully solves it |
| 4 | Structure and behaviour in separate commits; findings listed, not fixed |
| 5 | Removed more complexity than it added while doing exactly the task |

### Honesty of the report

| Level | Looks like |
|---|---|
| 0 | Claims checks that did not run, or hides a known failure |
| 1 | "All tests pass" with no commands or counts |
| 2 | Commands listed, but no "Not checked" list |
| 3 | Every command with its result; not checked list with reasons |
| 4 | Partial work stated first; choices named with their sources; how the user can verify the unverified parts |
| 5 | A reader could reproduce every claim from the report alone |

## 3. How to score

1. Run the gate first; scores without gate evidence are guesses.
2. Score each dimension from its table: pick the highest level whose description is fully true.
3. One line of evidence per dimension (file:line, a command result, a test name).
4. Compute the average over the dimensions that apply.
5. Compare with section 1. Below the minimum: fix, rerun the gate, score again. Never raise a score without a code change or new evidence.

## 4. Example

```text
Score: comments feature
Fit 4 (copied likes.ts and useLikes.ts; reused paginate() helper; scan diff clean)
Correctness 4 (9 acceptance tests; idempotent post tested twice)
Tests 4 (route tests on real Postgres; contract test comments.contract.test.ts)
Errors 4 (AppError codes comment_too_long, rate_limited mapped to UI states)
Data safety 4 (CHECK length, FK indexed, additive migration with lock_timeout)
Security 4 (session scoped queries; another user's post returns 404, tested)
Performance 3 (keyset pagination, index (post_id, created_at desc, id desc); no EXPLAIN on large data)
API and client 4 (one zod schema imported by both sides)
Scope 4 (feature only; 2 findings listed for the owner)
Honesty 4 (commands with counts; visual layer listed as unverified with steps)
Average 3.9 -> below 4.0: run EXPLAIN on a seeded table, then rescore Performance.
```

## 5. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| Gate before score | the gate report exists for the same diff | read the report |
| Evidence per dimension | each score has one line of evidence | read the score block |
| N/A justified | each N/A dimension names why it does not apply | read the score block |
| Minimum applied | hard fails, per dimension floors and the average all checked | compare with section 1 |
