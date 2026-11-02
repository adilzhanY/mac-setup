# The quality gate for code changes

Run this gate before you call any code change done: a feature, a bug fix, a refactor, a migration, a one line config change. It is permanent. It does not get skipped because the change is small, because the user is in a hurry, or because the tests are green. Green tests prove only what they test.

Lean mode (`SKILL.md` rule 11, a small change): run section 12 and every [critical] row; other rows may be N/A with the reason "lean". C9 is never N/A when the change shows money, a date or a counter.

Most rows are checked by a command; the rest by reading named code. Every row gets PASS, FAIL or N/A with its evidence (the command and its output, or file:line).

## Contents

1. How to run the gate
2. A. Understanding and scope
3. B. Consistency with house conventions
4. C. Correctness and tests
5. D. Errors
6. E. Data safety
7. F. Security
8. G. Performance
9. H. API and client calls
10. I. Honesty of the report
11. Report format
12. Fast checks (copy and run)
13. K. Brief and handover
14. Checks

## 1. How to run the gate

1. Set the base: the commit you started from (`git rev-parse HEAD` at the start of the task) or the merge base with the main branch. Run section 12 first; its output is evidence for many rows.
2. List the scope: every changed and new file (`git diff --stat "$BASE"`, `git ls-files -o --exclude-standard`), every caller and importer of a changed shape, the tests that cover them.
3. Write one line on what the change could break for users: data destroyed or exposed, a caller that stops working, a client that reads a field that moved.
4. Go through sections A to I. Mark each row PASS, FAIL or N/A with evidence.
5. Fix every FAIL in the code (never by loosening a test or the check), then rerun the failed rows and section 12.
6. Score with `quality/scoring-rubric.md`. Ship only at or above its minimum.
7. Report in the format of section 11.
8. A build from a brief also runs section 13 (K).

An item marked **[critical]** blocks shipping on its own.

When the change includes UI files, kwx-designer's gate runs on them as well (`workflow/duet-with-kwx-designer.md` section 7).

## 2. A. Understanding and scope

| # | Check | Pass condition | Verify |
|---|---|---|---|
| A1 [critical] | Rules of the project read | Every CLAUDE.md and AGENTS.md on the change path, DECISIONS.md and TODO.md were read; no conflict with an Accepted decision, or the user approved it | the project map lists them; `rg -n -i '<area words>' DECISIONS.md docs/adr` reviewed |
| A2 | Done defined first | An acceptance list or a failing test existed before the first edit | the spec block or the test's history in this task |
| A3 [critical] | Every caller updated | Each changed signature, type, export, response shape, column, event or config key has a caller list, and each caller is updated or proven unaffected | `rg -n -w '<name>'` output in the notes; typecheck clean |
| A4 [critical] | Only the task | The diff holds only what the task asked; findings noticed on the way are listed, not fixed | `git diff --stat "$BASE"` read against the plan's file list |
| A5 | One purpose per commit | Structure changes (moves, renames, extractions) are separate from behaviour changes | `git log --stat "$BASE"..HEAD`; renames never sit with test changes |
| A6 | Live path changed | The edit is in the code the entry point really calls, not a copy or legacy module | traced from the route, command or screen in the notes; a test goes through the real path |

## 3. B. Consistency with house conventions

| # | Check | Pass condition | Verify |
|---|---|---|---|
| B1 [critical] | No new variant | The scan after the change shows no new OFF, MIX or ODD line and no new variant in any area you touched | `diff scan-before.txt scan-after.txt` (section 12) |
| B2 | House examples copied | Each new kind of file names 2 existing examples and matches their location, naming, exports, imports, validation, errors, logging and test style | the plan lists the examples; read the new file next to one |
| B3 | Helper reused | No new helper duplicates an existing one | the searches run before writing it are in the notes; `rg -n -i '<verb><noun>'` |
| B4 [critical] | No unchecked dependency | Every added package was already installed, or was checked on the registry (age, downloads, repo) and approved by the user, and added through the package manager | section 12 dependency diff is empty, or each line has its approval |
| B5 | Installed API, not memory | Calls match the installed version's types or docs; no deprecated API | version read from the lockfile; deprecation lint clean |
| B6 | One term per concept | New names use the codebase's existing words for the same things | `rg -n -i '<synonym>'` shows no second word for the concept |
| B7 | No em or en dashes | None in code, comments, docs, commit messages | section 12 dash grep prints nothing |

## 4. C. Correctness and tests

| # | Check | Pass condition | Verify |
|---|---|---|---|
| C1 [critical] | Proof per acceptance item | Each acceptance item has a test or a terminal check that fails before the change and passes after; a bug fix starts with a test that reproduces it | test names mapped to the list; the red run in the notes |
| C2 [critical] | No test weakened | No assertion loosened, test deleted, skipped or focused, and no fixture changed to fit the code, unless the task changes that behaviour and the report says which line requires it | `git diff --stat "$BASE" -- '*test*' '*spec*' tests __tests__`; section 12 focused test grep |
| C3 [critical] | Checks loop green | Format, typecheck, lint (warnings as the project treats them), covering tests, full suite and build pass with the project's own commands | each command and its exit code in the notes |
| C4 | Every new branch has a test | New branching logic, parsers, money, dates, permissions have a test, including one error path | read the tests beside each new function |
| C5 | No stubs | No TODO, `todo!()`, placeholder return or sample data left in a production path | section 12 stub grep |
| C6 | Edge cases | Empty, one, many, maximum size, unicode, time zones, concurrent calls considered where they apply; each one that applies has a test or a reason | the acceptance list and the tests |
| C7 | Tests are real | Tests assert outcomes (state, response, rows), not only that a mock was called; the database is real, not mocked | `rg -n "(vi\|jest)\.mock\(.*(db\|prisma\|pg\|drizzle)" <tests>` prints nothing |
| C8 | Pre-existing failures proven | A failure you did not cause is shown failing on the base too, and reported, not fixed | `git stash; <cmd>; git stash pop` output |
| C9 [critical] | Shown numbers proven | Every money amount, date and counter the UI shows has a spec test at its boundaries (rounding at the .5 step, for example 80 minutes at 64,13 EUR per hour is 85,51 EUR (85,5066 rounded half away from zero); future and backdated dates refused where the rules say so; a counter at 0), and every number that should change (remaining visits, free places, balance, unbilled hours, open invoices) has the event that changes it implemented and tested. Never N/A "lean" when the change shows a money amount, a date or a counter | the life cycle table (`ai-agents/before-you-code.md` section 8) and the list of shown values mapped to test names |
| C10 | Same number everywhere | Screen totals, CSV, invoice and reports for the same entries come from one pricing function with one rounding step and agree | the pricing grep in section 12 shows one definition; a test asserts CSV net sum equals invoice net |

## 5. D. Errors

| # | Check | Pass condition | Verify |
|---|---|---|---|
| D1 [critical] | No swallowed error | No empty catch, `.catch(() => {})`, `let _ =` on a Result, `except: pass`, or fallback value that hides a failed call | section 12 swallowed error grep; read each hit |
| D2 | House error model | New failures use the layer's error type or result shape and the house helper; callers branch on codes, never on message text | read against the map's "errors" convention |
| D3 | Context added | Errors propagated with what was being done (`.context(...)`, `cause:`), logged once where handled | read each new `throw`, `?`, `return err` |
| D4 | Safe user messages | Responses and UI errors carry a safe message and a request id, never a stack, SQL, path or secret | read the error mapping; curl an error case |
| D5 | Crash on bugs | Bad config fails at startup; impossible states are asserted, not limped through | read config loading and new `expect`/asserts |

## 6. E. Data safety

| # | Check | Pass condition | Verify |
|---|---|---|---|
| E1 [critical] | Migrations are lock safe and backward compatible | `lock_timeout` set, indexes built concurrently, constraints added NOT VALID then validated, no drop or rename of anything the running code reads; old code works on the new schema | `npx -y squawk-cli <new migrations>`; read against `data/migrations.md` section 9 |
| E2 [critical] | No destructive command without a go | Nothing deleted, reset, dropped, force pushed or overwritten outside the task's own new files without a backup and the user's explicit yes | the commands run in this task; `ai-agents/safety-and-destructive-actions.md` section 4 |
| E3 | Invariants in the database | Each "must be unique, must exist, must be positive" rule has a matching constraint | grep the migration for UNIQUE, CHECK, REFERENCES, NOT NULL |
| E4 | Atomic writes | Read, modify, write is one statement, a row lock or a version check; multi row changes are in one transaction; no network call inside a transaction | read every new transaction block |
| E5 | Safe to retry | Mutations a client or a job may retry take an idempotency key or a natural unique key | read the handler; test calls it twice |
| E6 | Time and money | Instants are `timestamptz` in UTC; money is integer minor units or `numeric` plus currency, never float | `data/data.md` section 5 greps |
| E7 | Backfills batched | Data rewrites run in batches outside the DDL transaction, resumable | read the backfill |

## 7. F. Security

| # | Check | Pass condition | Verify |
|---|---|---|---|
| F1 [critical] | Authorization on the server, per object | Every new route or query checks the session's user and tenant against the specific object; not found and not yours both return 404 | read each handler; curl as another user |
| F2 [critical] | Input validated at the boundary | Every input from outside (body, query, params, headers, files, webhooks, LLM output, third party responses) passes a strict schema with limits, unknown fields rejected | read each entry point for the schema call |
| F3 [critical] | No injection | SQL is parameterized, shell runs with argument arrays, HTML is rendered as text or sanitized, URLs fetched by the server pass an SSRF guard | section 12 SQL and HTML greps; read each hit |
| F4 [critical] | No secrets in the diff | No key, token, password, cookie or `.env` file added; secrets come from the environment or a secret store | section 12 secret grep; `gitleaks git --staged --redact` when installed |
| F5 | Nothing sensitive logged | No password, token, auth header, full card or personal data in logs | `rg -n -i '(log\|logger\|console)\.\w+\(.*(password\|token\|secret\|authorization)'` on the changed files |
| F6 | Least privilege | New credentials, roles, RLS policies and CORS rules grant only what the feature needs | read the policy or config |
| F7 [critical] | Abusable endpoints limited and probed | Every password check (member login, admin login, Basic auth) and every sign up, reset, send and export endpoint has a limit: every password check has a hard limit per client IP and a growing delay per account that never refuses the correct password (`backend/auth.md` section 6); sign up, reset, send and export endpoints have a limit per client IP and per target (the email or phone, since there is no account yet). The IP is read through the one helper (`backend/rate-limits-retries-timeouts.md` section 6). Probes, results pasted: (a) 10 wrong passwords for one account from IP A, then the right password from IP B succeeds (no lockout DoS); (b) after 30 wrong passwords from one IP across random emails the next attempt gets 429; (c) a forged `X-Forwarded-For` does not get a fresh bucket in the default config; (d) the admin password endpoint returns 429 after its limit. "Documented in the README as not done" passes only when the fix needs infrastructure the brief excludes, and then it is the first line of "Not finished" | the four probe outputs (curl or test names); a test for probe (a) |

The full list and the five minute diff review are in `security/security.md`.

## 8. G. Performance

| # | Check | Pass condition | Verify |
|---|---|---|---|
| G1 | No query in a loop | Related rows load with a join, `IN (...)` or the ORM's batch include | read loops over rows; query count test where the repo has one |
| G2 | Lists bounded | Every list endpoint and query has a finite default and a clamped maximum; keyset pagination on growing tables | read the handler and query |
| G3 | Index for the new query | A new query on a table that grows has an index matching its WHERE and ORDER BY | the migration; `EXPLAIN` on a seeded DB when the table is large |
| G4 | Nothing blocks the event loop or executor | No sync file or network IO, no long CPU work in async handlers; no lock held across an await | read the async functions |
| G5 | Claims measured | Any "faster" claim has a before and after number from the same machine and build | the numbers in the report, or no claim |

## 9. H. API and client calls

| # | Check | Pass condition | Verify |
|---|---|---|---|
| H1 [critical] | Client and server agree | The client's type for each response is the server's type (one source), and a test parses a real response with it | `rg -n '<TypeName>'` shows one definition; the contract test |
| H2 | House API shape | Paths, methods, status codes and the error envelope match the house examples; stable machine codes per error | read against the example route |
| H3 | No breaking change in place | A shipped response or request shape changes only by adding; removals and renames get a new version or expand and contract | `git diff "$BASE" -- <types and schema files>` shows only additions |
| H4 | Timeouts on every remote call | HTTP, DB, cache, queue and SDK calls have a timeout; deadlines pass down | section 12 fetch grep; read client construction |
| H5 | Retries bounded, one layer | At most 3 attempts with backoff and jitter, only for retryable errors on idempotent calls | read the retry code and the library config |
| H6 | Every state handled | Each call the UI makes has loading, error (mapped from the machine code) and empty handling, matching the states list | read the hook's return type and its callers |
| H7 | Cache stays true | After a mutation, exactly the queries showing that data are invalidated or updated; optimistic updates roll back on error | read the mutation's success and error handlers |

## 10. I. Honesty of the report

| # | Check | Pass condition | Verify |
|---|---|---|---|
| I1 [critical] | Evidence for every claim | Each check named in the report has its command and result; nothing is reported as passing that did not run | the report's Ran block against the commands actually run |
| I2 | Not checked list | Present, even when empty, with the reason and how the user can check each item (for UI: what to open and click) | the report |
| I3 | Partial work at the top | Anything not done is stated first, with why | the report |
| I4 | Choices named | Each convention or design choice made where the code was mixed names its source (tool, docs, newest code, area majority) | the report |
| I5 | Findings listed, asked as the protocol says | Problems noticed are listed with keys; questions only for P1 and P2 in touched files, with the three answers | `workflow/audit-and-ask.md` section 4 |

## 11. Report format

```text
Quality gate: <feature or fix>
Size: <small|medium|large>; subagents: <n, one line why each>
Files read: <topic files opened before their code>
Scope: <n> files changed, <n> new; callers checked: <n>; could break: <one line>
A Understanding  6/6
B Consistency    7/7 (B1: scan diff clean)
C Correctness    7/8 (C6 N/A: no user input)
D Errors         5/5
E Data safety    N/A (no schema or data change)
F Security       7/7
G Performance    4/5 (G5 N/A)
H API and client 7/7 (H1: comments.contract.test.ts)
I Honesty        5/5
K Brief/handover 4/4 (or N/A: not a brief build)
Critical items: all pass
Score (scoring-rubric.md): <per dimension>, ship: yes/no
Tests by risk: money/dates <n>, auth/abuse <n>, data loss <n>, UI and client only <n>, other <n>
Ran:
  pnpm tsc --noEmit -> 0 errors
  pnpm vitest run src/routes/comments.test.ts -> 9 passed
  pnpm test -> 412 passed
Not checked: <list with reasons and how to check, or "none">
Cost: <wall time>, <n> subagents, <output tokens when shown>
```

## 12. Fast checks (copy and run)

Run in bash from the repo root. They print added lines only (`path:line: text`), including new untracked files. Each hit is a lead to read, not an automatic fail.

```bash
BASE=${BASE:-$(git merge-base HEAD origin/main 2>/dev/null || git rev-parse HEAD)}
A="${SCRATCH:-/tmp}/added.txt"
{ git diff -U0 "$BASE" -- . ':!*lock*'
  git ls-files -o --exclude-standard -z | xargs -0 -r -n1 git diff --no-index -U0 /dev/null
} | awk '/^\+\+\+ /{f=substr($0,7); next} /^@@/{split($3,h,","); n=substr(h[1],2); next}
         /^\+/{print f ":" n ": " substr($0,2); n++}' > "$A"
echo "$(wc -l < "$A") added lines"; git diff --shortstat "$BASE"
# swallowed errors (D1)
grep -P 'catch\s*(\([^)]*\))?\s*\{\s*\}|\.catch\(\s*\(\)\s*=>\s*(\{\s*\}|null|undefined)\s*\)|\blet _ = |\bexcept(\s+\w+)?\s*:\s*pass\b|\.ok\(\);' "$A"
# stubs and placeholders (C5)
grep -E '\b(TODO|FIXME|XXX)\b|todo!\(|unimplemented!\(|NotImplementedError|[Nn]ot implemented' "$A"
# focused or skipped tests (C2)
grep -E '\b(it|test|describe|context)\.(only|skip)\(|\b(xit|xdescribe|xtest)\(|#\[ignore\]|@pytest\.mark\.(skip|xfail)|t\.Skip\(' "$A"
# secrets (F4)
grep -P 'AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----|\bsk_live_[0-9A-Za-z]{10,}|\bgh[pousr]_[0-9A-Za-z]{30,}|\bxox[abprs]-[0-9A-Za-z-]{10,}|(?i:api[_-]?key|secret|password|passwd|token)\s*["\x27]?\s*[:=]\s*["\x27][^"\x27\s]{8,}["\x27]' "$A"
# SQL or shell built from strings (F3)
grep -P '\b(query|execute|exec|raw|queryRawUnsafe|executeRawUnsafe)\w*\s*\(\s*(`[^`]*\$\{|["\x27][^"\x27]*["\x27]\s*\+)|format!\(\s*"\s*(SELECT|INSERT|UPDATE|DELETE)|\bexecSync\(\s*`[^`]*\$\{' "$A"
# HTML sinks (F3)
grep -E 'innerHTML\s*=|dangerouslySetInnerHTML|v-html|insertAdjacentHTML|document\.write\(' "$A"
# new lint and type suppressions (B1, C3)
grep -E 'as any\b|:\s*any\b|@ts-ignore|@ts-nocheck|eslint-disable|#\[allow\(|# type: ignore|# noqa' "$A"
# env read outside the config module (D5)
grep -E 'process\.env\.|import\.meta\.env\.|env::var\(|os\.environ' "$A"
# debug output left in (D3)
grep -E 'console\.(log|debug)\(|\bdbg!\(|\bprintln!\(' "$A"
# fetch without an abort signal on the same line (H4)
grep -E '\bfetch\(' "$A" | grep -v signal
# unwrap and expect in Rust outside tests (D1)
grep -E '^[^:]+\.rs:[0-9]+: .*(\.unwrap\(\)|\.expect\()' "$A" | grep -vE '(^|/)tests?/|_test\.rs:'
# em and en dashes (B7)
grep -P '[\x{2013}\x{2014}]' "$A"
# date formatting without an explicit timeZone (C9); number formatting hits are leads to read
grep -P '(DateTimeFormat\(|toLocale(Date|Time)?String\()(?!.*timeZone)' "$A"
# pricing functions (C10): one definition in the whole repo
rg -n "fn price|function price"
# client IP headers, forwarded, read outside the one helper (F7)
grep -P '(?i:x-forwarded-for|x-real-ip|cf-connecting-ip)' "$A"
# tests changed (C2): every line needs a reason in the report
git diff --stat "$BASE" -- '*test*' '*spec*' tests __tests__
# dependencies added or changed (B4)
git diff "$BASE" -- '*package.json' '*Cargo.toml' '*pyproject.toml' '*go.mod' | grep -E '^[+-][^+-]'
# new migrations (E1): lint each one
git diff --name-only --diff-filter=A "$BASE" -- '*migrations*' '*.sql'
# conventions (B1): no new OFF, MIX or ODD line
python3 -I ${CLAUDE_SKILL_DIR}/scripts/scan_conventions.py . > "${SCRATCH:-/tmp}/scan-after.txt"
diff "${SCRATCH:-/tmp}/scan-before.txt" "${SCRATCH:-/tmp}/scan-after.txt"
```

End the harvest with one count line in the report: `<N> leads read, <M> fixed, <K> kept with a reason`. A hit kept on purpose (a CLI's `println!`, the config module's env read) needs one clause of reason.

## 13. K. Brief and handover

Runs when the task is a build from a brief or ends a project phase; N/A otherwise. Trial evidence: the skilled desktop build shipped a README with no Not finished list, no decisions, a /games path and fish syntax; the gate had no README row.

| # | Check | Pass condition | Verify |
|---|---|---|---|
| K1 [critical] | Brief matrix and promises closed | Every brief item has a matrix row with status and proof (test name or command); no done row without proof; every promise of the product's own text has a code path or a Not finished line | read PLAN.md against the brief, item by item (`workflow/new-project-from-brief.md` sections 2 and 5) |
| K2 [critical] | README complete | Headings for Run, Test, Build, Environment variables, Decisions, Open questions, Not finished exist and are filled; Not finished lists every partial or missing matrix row | the README block under this table prints nothing |
| K3 [critical] | README portable | No absolute paths of the build machine, no user names, no operator shell dialect, no "on this machine" notes; machine tips use env vars in an optional Tips line | the README block under this table prints nothing |
| K4 | Claims reproduced | Every test count, command and URL in the README was run in this session and matches | rerun the README's test commands and compare counts |

README block for K2 and K3 (copy as written; the table cells cannot hold a raw pipe):

```bash
for h in Run Test Build Environment Decisions "Open questions" "Not finished"; do grep -qi "^#.*$h" README.md || echo MISSING $h; done
grep -nE "/home/|/games/|/Users/|set -x |this machine" README.md
```

## 14. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| Every row marked | Each row of A to I (and K for a build from a brief) is PASS, FAIL or N/A with evidence | read the gate notes |
| No open critical | No [critical] row is FAIL | read the critical ids (A1, A3, A4, B1, B4, C1, C2, C3, C9, D1, E1, E2, F1 to F4, F7, H1, I1, and K1 to K3 for builds from a brief) in the notes |
| Lean mode honest | rows marked N/A "lean" only on a small change, and C9 never "lean" when the change shows a money amount, a date or a counter | read the notes |
| Brief build closed | section 13 rows marked with evidence | read the notes |
| Fast checks run | Section 12 output is in the notes with the count line | read the notes |
| Fixes were in code | No FAIL turned PASS by editing a test, a lint config or this gate | `git diff "$BASE" -- '*test*' eslint.config.* biome.json Cargo.toml` read for loosening |
| UI gated too | Changes with UI files also ran kwx-designer's gate | the joint report |
