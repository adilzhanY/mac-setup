# Feature workflow: building a feature end to end in an existing codebase

The order of work for a feature that crosses layers: data, API, client data layer, UI, tests. Data first, because every other layer depends on its shape and it is the hardest to change later. Each step names its exit condition, and the table in section 2 names the file to read at that step. When the feature has screens, kwx-designer owns the UI step; see `workflow/duet-with-kwx-designer.md`.

## Contents

1. The steps as a checklist
2. Which file to read at each step
3. Step 1: spec and done when
4. Step 2: house examples, one pair per kind of file
5. Step 3: the plan
6. Step 4: data (schema and migration)
7. Step 5: domain logic
8. Step 6: API
9. Step 7: client data layer
10. Step 8: UI and wiring
11. Step 9: tests across the layers
12. Step 10: the checks loop
13. Step 11: gate, score, report
14. Checks

## 1. The steps as a checklist

Copy into your notes and tick off. Skip a step only when the feature has no such layer, and say so.

```
- [ ] 0 Map: workflow/codebase-first.md (skip if mapped in this conversation)
- [ ] 1 Spec and done when: acceptance list, error cases, who may call it, states list for any screen
- [ ] 2 House examples: 2 per kind of file you will create, paths written down
- [ ] 3 Plan: files, callers, order, flags, risks; shown to the user if it changes schema, public API or auth
- [ ] 4 Data: schema, migration, constraints, indexes; migration applied to a dev or scratch DB
- [ ] 5 Domain logic: pure functions with tests, including one error path each
- [ ] 6 API: route, validation, authorization, errors, pagination, idempotency; tested through HTTP
- [ ] 7 Client data layer: typed calls, loading, error, empty, retries, cache invalidation
- [ ] 8 UI and wiring: screens (kwx-designer), route, navigation, registration
- [ ] 9 Tests across the layers: contract test, one end to end path if the repo has e2e
- [ ] 10 Checks loop: format, typecheck, lint, covering tests, full suite, build, smoke
- [ ] 11 Gate and report: quality/quality-gate.md, quality/scoring-rubric.md, findings noticed (audit-and-ask.md section 4)
```

## 2. Which file to read at each step

Read the master file of each area the feature touches once, then only the topic files the step needs.

| Step | Read | For |
|---|---|---|
| 0 Map | `workflow/codebase-first.md` | stack, checks, conventions, decisions |
| 1 Spec | `ai-agents/before-you-code.md` section 8; `backend/backend.md` section 3 when there is an endpoint | done when, what to ask before coding |
| 2 Examples | `ai-agents/before-you-code.md` sections 3 and 4; `architecture/consistency.md` | copying the house shape, finding helpers |
| 3 Plan | `ai-agents/change-discipline.md`; `architecture/modules-and-boundaries.md` and `architecture/folder-structure.md` when adding a module or folder | callers, one purpose, where new code goes |
| 4 Data | `data/data.md` (the 8 questions), `data/schema-design.md`, `data/migrations.md`, `data/indexes-and-queries.md`; `data/sqlite-and-local-first.md` on SQLite or offline | a lock safe, backward compatible migration |
| 5 Domain | `architecture/abstraction-and-duplication.md`; `reliability/error-handling-strategy.md`; the language master file | pure logic, one error model |
| 6 API | `backend/backend.md`, then `backend/api-design.md`; `security/security.md`; `data/transactions-and-integrity.md` for multi row writes | routes that are safe to call and to retry |
| 7 Client | `backend/rate-limits-retries-timeouts.md` (client side sections), `backend/caching.md` (client query caches); `languages/typescript/typescript.md` | loading, error, retry and cache rules |
| 8 UI | `workflow/duet-with-kwx-designer.md`, and the kwx-designer skill for the screens | who builds what, the states contract |
| 9 Tests | `reliability/testing-strategy.md`; `ai-agents/tests-and-honesty.md` | real DB, mocks only at the edge you do not own |
| 10 Loop | `ai-agents/verification-loop.md` | order of checks, full stack without a browser |
| 11 Gate | `quality/quality-gate.md`, `quality/scoring-rubric.md`, `workflow/audit-and-ask.md` section 4 | shipping, the report, findings noticed |

## 3. Step 1: spec and done when

Write the acceptance list before the first edit. For a feature, one line per item:

```markdown
Feature: comments on a post
- A signed in user can post a comment (1 to 2000 chars) on a post they can see. -> 201 with the comment
- Anyone who can see the post lists its comments, newest first, 20 per page, cursor paged. -> 200 { items, nextCursor }
- Empty body or over 2000 chars -> 422 with field errors. Not signed in -> 401. Post not visible -> 404.
- Posting twice with the same Idempotency-Key creates one comment.
- Screen states: loading, empty ("No comments yet"), list, loading more, end of list, post failed (retry), offline.
Done when: each line has a test that fails before and passes after; the checks loop is green.
```

Ask one round of questions only when the answer changes the design: the data model (can comments be edited, deleted, nested?), the public API shape, or permissions. Use AskUserQuestion with concrete options and your recommendation first. Everything else, decide by the house convention and note the choice in the report.

Check the spec against DECISIONS.md and open TODO items for the same area (`rg -n -i 'comment' DECISIONS.md TODO.md`). A conflict with an Accepted decision stops the work until the user decides.

## 4. Step 2: house examples, one pair per kind of file

For every kind of file the feature adds, find the 2 most recent examples in the same area and write their paths into the plan (`ai-agents/before-you-code.md` section 3):

| Kind | How to find examples |
|---|---|
| migration | `ls -t migrations/ prisma/migrations/ drizzle/ supabase/migrations/ 2>/dev/null \| head -3` |
| table or model | `rg -l 'pgTable\(|model \w+ \{|CREATE TABLE|#\[derive\(.*FromRow' \| head` |
| route or handler | the layer line from the map; `git log --diff-filter=A --name-only --format= -- <routes dir> \| head` |
| validation schema | `rg -l 'z\.object\(|v\.object\(|#\[derive\(.*Deserialize' <routes dir> \| head` |
| client call or hook | `rg -l 'useQuery\(|useMutation\(|useSWR\(' \| head` |
| screen or component | the screens folder; kwx-designer decides the UI shape |
| test for each of the above | the test next to each example |

Copy from them: file location and name, export style, imports, validation, error helper, logging, authorization check, registration, and the test's runner, fixtures and assertion style. Search for existing helpers before writing any (`ai-agents/before-you-code.md` section 4) and list the searches you ran.

## 5. Step 3: the plan

A short plan in your notes, shown to the user before coding when the feature changes a schema, a public API, authentication or permissions, or touches more than about 10 files:

```markdown
Plan: comments
Files (new): migrations/0042_comments.sql, src/db/schema/comments.ts, src/routes/comments.ts, src/routes/comments.test.ts,
  src/api/comments.ts, src/hooks/useComments.ts, (UI, kwx-designer) src/screens/Post/Comments.tsx
Files (changed): src/routes/index.ts (register), src/db/schema/index.ts (export)
Callers of changed shapes: none (additive only)
Examples copied: src/routes/likes.ts + likes.test.ts, src/hooks/useLikes.ts, migrations/0040_likes.sql
Order: migration -> schema -> route + tests -> client hook -> UI -> contract test
Risks: comments table grows fast: keyset pagination, index (post_id, created_at desc, id desc)
Flag: none (additive, hidden until the UI ships)
```

One purpose per change. Tidying you notice on the way is not part of the plan; it goes to the findings list at the end (`workflow/audit-and-ask.md` section 4). If a tidy step makes the feature easier ("make the change easy, then make the easy change"), it is its own commit with no behaviour change, before the feature commit (`architecture/architecture.md` R17).

## 6. Step 4: data (schema and migration)

1. Answer the 8 questions of `data/data.md` section 4 in the plan (rows, locks, coexisting code versions, invariants, rerun safety, outside calls in transactions, backup, destructive steps).
2. Write the migration in the house migration tool and naming, with constraints in the database: NOT NULL, CHECK, UNIQUE, foreign keys, and an index for every foreign key and for the list query (`data/indexes-and-queries.md`).
3. Additive first. A rename or type change is expand, migrate, contract over several releases (`data/migrations.md` section 4). Never drop or rewrite a column in the same release that stops using it.
4. Apply it to a dev or scratch database, never production, and run it twice where the tool allows (idempotent or fails cleanly). Lint it when the repo has Squawk: `npx -y squawk-cli <file>.sql`.
5. Regenerate types the way the repo does (`pnpm db:generate`, `prisma generate`, `cargo sqlx prepare`), and commit the generated files only if the repo commits them.

Exit: migration applied on a scratch DB, generated types compile, the schema test (if the repo has one) passes.

## 7. Step 5: domain logic

Put decisions in pure functions that take data and return data; IO stays in handlers and adapters (`architecture/architecture.md` R14). Use the house error model for the layer (`reliability/error-handling-strategy.md` section 2). Write the test first for each rule in the acceptance list, then the code. Each new branch, parser, money or date calculation gets a test, including at least one error path.

Exit: domain tests green, typecheck clean.

## 8. Step 6: API

Copy the house route example, then check each item, which are the rules models skip by default (`backend/backend.md` section 1):

- Validation at the boundary with a strict schema that rejects unknown fields; body size limit.
- Authorization on the server, per object, user and tenant from the session; not found and not yours both return 404.
- The house error envelope with a stable machine code per failure; no stack traces or SQL in responses.
- Lists paginated from day one: finite default, clamped max, keyset cursor on growing tables.
- Mutations that a client may retry take an idempotency key or a natural unique key.
- Every outbound call has a timeout; no network call inside a database transaction.
- The response is built from an explicit type (DTO), never by returning the ORM row.

Test through the real HTTP layer against a real database (`reliability/testing-strategy.md` section 7): the happy path, validation error, no auth, someone else's object, not found, and the retry of an idempotent call. Then write the response type the client will use, from the same schema when the stack allows (zod schema exported from a shared module, OpenAPI generated client, a Rust type with `ts-rs` or `specta`). One source of truth for the shape.

Exit: route tests green; the response type exists in one place the client can import.

## 9. Step 7: client data layer

- Use the house client and server state library (`useQuery`/`useMutation`, SWR, a store); never a second one, never `fetch` in a component when the house has a client module.
- Typed calls from the shared response type. Parse untrusted responses at the boundary when the house does (zod `parse` in the client module).
- Every call exposes loading, error (with the machine code, so the UI can map it to copy) and empty, matching the states list from step 1.
- Timeouts and cancellation (AbortSignal on unmount or route change); retries only for idempotent reads, bounded, with backoff (`backend/rate-limits-retries-timeouts.md`).
- After a mutation, invalidate or update exactly the queries that show the changed data; optimistic updates only with a rollback on error.
- Pagination: a "load more" or infinite query using the server's cursor, never offset arithmetic on the client.

Exit: the hook or client module has tests for success, error code mapping, and empty (with the network mocked at the edge, MSW or equivalent, never the module under test).

## 10. Step 8: UI and wiring

When the feature has screens, kwx-designer owns them: hand over the states list and the client hook's return type and follow `workflow/duet-with-kwx-designer.md`. In this user's setup, UI code goes to the ui-designer subagent. kwx-developer owns the wiring: route registration, navigation entries agreed in the brief, feature flags, settings persistence, and every file that imports a changed component or type (`grep -rn` the names).

Exit: the screen renders every state in the states list from data the hook really returns; the app builds.

## 11. Step 9: tests across the layers

- A contract test: the real API response (from the route test or a running server) parses with the type or schema the client uses. This catches renamed or missing fields between layers.
- One end to end path when the repo already has e2e (Playwright for web, Maestro for React Native): the happy path of the main acceptance item. Do not add an e2e framework the repo does not have; say so in the report instead.
- Existing tests that cover changed code run before the full suite (`ai-agents/tests-and-honesty.md` section 4). Never weaken, skip or delete a test to get green; if one looks wrong, stop and report it with evidence.

## 12. Step 10: the checks loop

Run the project's own commands from the map, in the order of `ai-agents/verification-loop.md` section 1: format, typecheck, lint, covering tests, full suite, build, start the app and smoke the changed path. Without a browser, verify each layer from the terminal (`ai-agents/verification-loop.md` section 7): curl the API for each acceptance case, query the DB for the written rows, read the server log, and state that the visual layer is unverified and how the user can check it.

Then rerun the convention scan and diff it:

```bash
python3 -I ${CLAUDE_SKILL_DIR}/scripts/scan_conventions.py . > "$SCRATCH/scan-after.txt"
diff "$SCRATCH/scan-before.txt" "$SCRATCH/scan-after.txt"
```

A new OFF, MIX or ODD line in an area you touched means your code added a variant: fix your code, not the scan.

## 13. Step 11: gate, score, report

1. Run `quality/quality-gate.md`, every row, PASS, FAIL or N/A with evidence. No open [critical] row.
2. Score with `quality/scoring-rubric.md`; ship only at or above the minimum.
3. With a UI, run kwx-designer's gate too (the joint gate in `workflow/duet-with-kwx-designer.md` section 7).
4. Update TODO.md (tick finished items this task completed) and DECISIONS.md (a decision a later reader could not see in the code), only where those files exist or the user agreed to create them.
5. Report in the gate's format, then the "Noticed while working" block and at most one AskUserQuestion call (`workflow/audit-and-ask.md` section 4).
6. Commit only when the user or the project's rules say so: structure commits separate from behaviour commits, a one line message each.

## 14. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| Acceptance list before code | every item has a test or a terminal check | the spec block and the test names |
| Examples named | 2 example paths per kind of new file | the plan |
| Data first | the migration exists and was applied before the API code depending on it | file timestamps, the scratch DB apply output |
| Additive or expand and contract | no drop or rename used by currently deployed code | read the migration against the code in `git show HEAD` |
| One shape source | the client imports the response type from the place the server builds it | `rg -n 'CommentResponse\|commentSchema'` shows one definition |
| Every state wired | each states list item maps to an API signal and a client field | the duet table, or read the hook's return type |
| Contract test | a test parses a real response with the client's type | the test file |
| No new variant | scan diff shows no new OFF, MIX or ODD line in touched areas | `diff scan-before.txt scan-after.txt` |
| Gate run | every gate row marked, no open [critical] | the report |
| Findings listed, not fixed | the diff holds only the feature | `git diff --stat` against the plan's file list |
