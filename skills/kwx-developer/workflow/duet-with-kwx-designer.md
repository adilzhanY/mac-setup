# Duet with kwx-designer: one full stack feature, two skills

How kwx-developer and its sister skill kwx-designer split a feature that has both screens and data (a comments section, a checkout, a settings page that saves), how they hand work to each other, and how to run them as two subagents in parallel without editing the same files. The rule underneath: the UI states list and the API contract are the same document seen from two sides. Every state the designer draws needs a signal from the API, and every error the API returns needs a state on screen.

## Contents

1. Who owns what
2. The contract: states list and API shapes
3. The order of work
4. Running two subagents in parallel
5. The two briefs
6. When one side needs a change from the other
7. The joint final gate
8. Without subagents: the same duet in one context
9. Checks

## 1. Who owns what

| Area | Owner | Examples |
|---|---|---|
| User experience, flows, screen structure | kwx-designer | what is on the screen, the primary action, what is hidden |
| Screens, components, layout, styles, tokens, icons | kwx-designer | `src/screens/**`, `src/components/**`, theme files, SVG icons |
| Every UI state and its copy | kwx-designer | loading skeleton, empty state text, error messages users read, limits |
| Data model, schema, migrations | kwx-developer | `migrations/**`, `src/db/**` |
| API: routes, validation, authorization, errors, pagination | kwx-developer | `src/routes/**`, `server/**` |
| Shared types and schemas (the contract in code) | kwx-developer | `src/api/types.ts`, `shared/schema.ts`, generated clients |
| Client data layer: API calls, hooks, cache, retries | kwx-developer | `src/api/**`, `src/hooks/use<Data>.ts` |
| Error codes and their mapping to states | both: developer defines the codes, designer writes the copy per code | `src/api/errors.ts` (codes), `src/copy/errors.ts` or the screen (text) |
| Wiring: route registration, flags, persistence | kwx-developer | router file, flag list, settings store |
| Navigation entry, menu item | kwx-designer (the placement), kwx-developer (the registration) | split per file in the brief |
| Tests | kwx-developer for logic, API, client and contract; kwx-designer for component state rendering where the repo tests components | `*.test.ts` |
| Code organisation, conventions, the final gate run | kwx-developer | scan, findings, the joint gate |

In this user's setup, all UI code is written by the **ui-designer** subagent (`~/.claude/agents/ui-designer.md`), which loads kwx-designer. The data side is written by a developer subagent that loads kwx-developer. The main agent briefs both, owns the contract, and runs the joint gate.

## 2. The contract: states list and API shapes

The contract is one short document the main agent writes before either side builds. It has three parts.

**Part 1, the states list (kwx-designer side).** Every screen in the feature, every state it can be in, and the data each state shows:

| Screen | State | Shows | Triggered by |
|---|---|---|---|
| Comments | loading | 3 skeleton rows | first fetch in flight |
| Comments | empty | "No comments yet" and the composer | `items: []`, no cursor |
| Comments | list | author, time, text, newest first | `items.length > 0` |
| Comments | loading more | spinner row at the end | next page in flight |
| Comments | end | nothing more to load | `nextCursor: null` |
| Comments | load failed | "Could not load comments" and Retry | network error or 5xx |
| Composer | posting | button busy, text kept | mutation in flight |
| Composer | too long | inline count, button disabled | client check, and 422 `comment_too_long` from the server |
| Composer | signed out | "Sign in to comment" | 401 `unauthenticated` |
| Composer | post failed | text kept, "Not sent. Try again." | 5xx or timeout |
| Composer | offline | text kept, "You are offline" | no network |

**Part 2, the API shapes (kwx-developer side).** For each endpoint: method and path, request type, response type, error codes with status, pagination, idempotency, and which state each response drives. Written as code when the stack allows (a zod schema or TypeScript types file, an OpenAPI file, Rust types exported with `ts-rs`), so the contract compiles:

```ts
// src/api/comments.types.ts  (owned by the developer side; the UI imports, never edits)
export type Comment = { id: string; author: { id: string; name: string }; body: string; createdAt: string };
export type CommentPage = { items: Comment[]; nextCursor: string | null };
export type CommentError =
  | "unauthenticated"      // 401 -> Composer: signed out
  | "post_not_found"       // 404 -> Comments: "This post is gone" (new state, added to the list)
  | "comment_too_long"     // 422 -> Composer: too long
  | "rate_limited";        // 429 -> Composer: "Slow down, try again in a minute"
export const COMMENT_MAX = 2000; // one source for the client check and the server CHECK constraint
```

**Part 3, the hook signature (the handshake).** The exact thing the UI calls and what it gets back, so the designer can build every state against it before the server exists:

```text
useComments(postId) -> { status: "loading" | "error" | "success"; items: Comment[]; error?: CommentError | "network";
                         hasMore: boolean; loadMore(): void; isLoadingMore: boolean; retry(): void }
usePostComment(postId) -> { post(body: string): Promise<void>; isPosting: boolean; error?: CommentError | "network" | "timeout" }
```

Rules for the contract:

1. Every state in Part 1 has a trigger that exists in Part 2 or Part 3. A state with no signal is a screen that can never appear.
2. Every error code in Part 2 maps to a state in Part 1. An error with no state is a failure users see as a frozen or blank screen.
3. Shared limits and enums are defined once in code and imported by both sides (`COMMENT_MAX`), never typed twice.
4. Time travels as ISO 8601 UTC strings; money as integer minor units plus a currency; ids as strings. The UI formats them.
5. The contract lives in the conversation and in the types file. It is not a new markdown file in the repo.

## 3. The order of work

```
main agent    : codebase-first map -> spec and acceptance list -> contract (parts 1, 2, 3)
developer     : types file + hook signatures with fixture data (short, first)  ─┐
                then migration -> API + tests -> real hook implementation      │ parallel
ui-designer   : screens and every state, built against the hook signature     │
                and fixtures for each state                                   ─┘
main agent    : merge check -> contract test -> joint gate -> report
```

The developer's first deliverable is small and blocks the designer: the types file and the hooks returning fixtures for each state (`?state=empty` in a dev story, or a fixture module). Everything after that runs in parallel.

## 4. Running two subagents in parallel

1. **One working tree, disjoint files.** Both agents work in the same checkout. The main agent lists every file each one may create or edit in its brief. A file not on an agent's list is read only to it. Worktrees are not needed when files are disjoint, and they add a merge step.
2. **Shared files have one owner.** The types file, the router, the navigation config, `package.json`: one named owner each, written in both briefs. The other side asks the main agent (section 6).
3. **Launch both in one message**, so they run at the same time, after the developer has delivered the types file and fixtures (or launch the developer first with only that step, then both).
4. **Checks do not collide.** The developer runs the full checks loop. The designer runs typecheck and its component tests only. Nobody runs a formatter over the whole repo while the other agent is writing; format only your own files.
5. **No installs during the parallel phase.** A new dependency is requested from the main agent, which installs it between phases, after asking the user (`ai-agents/change-discipline.md` section 4).
6. **Neither agent commits.** The main agent commits after the joint gate, when the user or the project's rules say so.
7. **Live reloading apps** (the Quickshell shell, a dev server watched by the user): follow the project's lock rule for saves; in this user's setup the main agent names the lock in the briefs.

## 5. The two briefs

Developer subagent (general purpose agent):

```text
Load the kwx-developer skill (~/.claude/skills/kwx-developer/SKILL.md) and follow it.
Repo: <path>. Project map: <paste the map>.
Feature: <one line>. Acceptance list: <paste>.
Contract: <paste parts 1, 2, 3>.
Your files (create or edit only these): <list>. Read only: everything else.
Shared files you own: <types file, router>. The UI agent imports them and never edits them.
Order: 1) types file and hooks returning fixtures for every state, then report "contract ready";
       2) migration, API with tests through HTTP, real hooks with tests; 3) checks loop.
Do not edit UI files, do not install dependencies, do not commit.
Report: files changed, each check command with its result, contract changes you need (if any), not checked.
```

UI subagent (the ui-designer agent):

```text
Load kwx-designer and follow its gate. Repo: <path>. Design system: <files>.
Feature: <one line>. States list (part 1 of the contract): <paste>.
Data comes only from these hooks and types (read only to you): <paste part 3 and the types file path>.
Fixtures for each state: <path>. Build every state in the list; copy for each error code: <list of codes>.
Your files (create or edit only these): <list>. Do not fetch data directly, do not edit hooks, types or routes.
If a state needs data the hooks do not return, stop and report the exact field you need.
Report: files changed, which states are built and how each was checked, the kwx-designer gate result.
```

## 6. When one side needs a change from the other

1. The agent stops on that part, keeps working on the rest, and puts the request in its report: the field or code, why, and which state needs it.
2. The main agent decides, updates the contract (both parts, never one), and passes the change to the owner of the file.
3. The owner makes the change; the main agent tells the other agent it is in.
4. A change to the contract after the parallel phase starts is the most common source of breakage: rerun the contract test (section 7) after each one.

## 7. The joint final gate

Run by the main agent after both agents report, on the combined diff.

1. **Both gates, in full.** `quality/quality-gate.md` of this skill for everything outside the UI files; kwx-designer's `quality/quality-gate.md` for the UI files. The ui-designer agent ran its gate; the main agent reads its report and spot checks two states in the code.
2. **The duet checks:**

| # | Check | Pass condition | How to verify |
|---|---|---|---|
| J1 [critical] | Contract compiles across both sides | typecheck of the whole repo is clean | the project's typecheck command |
| J2 [critical] | Every state has a signal | each row of the states list maps to a response, code or client condition that exists | read the list against the types file and hook |
| J3 [critical] | Every error has a state | each error code in the types is handled by a branch in the UI | `rg -n 'comment_too_long\|rate_limited' src/screens src/components` finds each code, or a generic handler covers it on purpose |
| J4 | Real response parses with the client type | the contract test passes | the test from `workflow/feature-workflow.md` section 11 |
| J5 [critical] | UI does not fetch directly | no `fetch(`, `axios`, or DB client in UI files | `rg -n 'fetch\(\|axios\|createClient\(' <ui folders>` returns only the house client module |
| J6 | One source for limits and enums | shared constants imported, not retyped | `rg -n '2000' src` finds one definition |
| J7 | Loading and failure paths reachable | each async call has a loading and an error branch in the UI | read the screens' render branches |
| J8 | File ownership kept | no agent edited a file outside its list | `git diff --name-only` against both lists |
| J9 | Fixtures not shipped | fixture data is not imported by production code | `rg -n 'fixtures' src --glob '!**/*.test.*' --glob '!**/*.stories.*'` |

3. **One report** with both gate summaries, the J rows, the checks commands and results, and one "Not checked" list (the visual layer is unverified without a browser: say how the user can check it).

## 8. Without subagents: the same duet in one context

When the feature is small or subagents are not available, one agent does both sides, in this order: contract first (all three parts), then the developer side up to the hooks with fixtures, then the screens with kwx-designer loaded, then the real data, then both gates. Load each skill's reference files only for its own step, so the context does not hold both skill trees at once.

## 9. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| Contract before code | states list, API shapes and hook signatures written before either side builds | conversation order |
| Contract in code | the types file exists and both sides import it | `rg -l '<types file name>'` shows UI and API importers |
| Ownership written | each brief lists its files and the shared file owners | read the briefs |
| Disjoint edits | no file changed by both agents | the two reports' file lists do not intersect |
| Both gates run | developer gate and kwx-designer gate reports present | the final report |
| Duet rows pass | J1 to J9 marked, no open [critical] | the final report |
