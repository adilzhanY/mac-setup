# Verification loop

The ordered checks to run before saying a task is done, the commands per stack, how to enforce them with hooks and CI, how to run a fresh-context review, what to do when a check cannot run, and how to verify a full stack feature without a browser.

Why this file exists: models improve their code when they get external, executable feedback, and do not when they only re-read their own work (Huang et al.: self-correction without an outside signal does not help and sometimes hurts; self-debugging with execution results does). "Claude stops when the work looks done. If it has nothing to run that tells it whether the work actually is done, 'looks done' is all it has to go on" (Anthropic). Evidence: strong for executable feedback, vendor claim for the quote.

## Contents

1. The loop, in order
2. Commands per stack
3. Running the loop well
4. Enforce it: hooks and CI
5. Fresh-context review against the spec
6. When a check cannot run
7. Full stack features without a browser
8. Checks

## 1. The loop, in order

Cheap, deterministic checks first; slow and judgement-based checks last. Each step answers a measured failure.

| Step | What | Why this step | Evidence |
|---|---|---|---|
| 0 | Done is defined: a failing test or an acceptance list (`before-you-code.md` section 8) | without a check, "looks done" is the only signal | vendor claim |
| 1 | Formatter, on changed files | removes noise from every later diff and review; no model turn needed when run by a hook | vendor claim |
| 2 | Typecheck / compile | catches missed callers in typed code; type information cut TypeScript compile errors by more than half | strong |
| 3 | Lint, including deprecation, error-swallowing and security rules | precise, cheap feedback that models act on well | medium |
| 4 | Tests that cover the change (`tests-and-honesty.md` section 4) | telling the agent which tests cover the change cut regressions 70% | medium |
| 5 | Full test suite | the nearest test misses callers elsewhere (29.6% of "passing" SWE-bench patches diverge) | strong |
| 6 | Build and start the app, smoke the changed path | catches wiring, config and startup errors that unit tests skip | vendor claim |
| 7 | Fresh-context review against the spec, style skipped (section 5) | a reviewer that did not write the code is not swayed by its reasoning | vendor claim, AI reviewers about 50% F1 |
| 8 | Report with evidence: each command and its result, and what was not checked | "All tests pass" alone tells the reader very little | vendor claim |

Fix failures at the step where they appear, then rerun from step 1. Do not jump to step 5 while step 2 is red.

## 2. Commands per stack

Use the project's commands from CI or the instruction file first (`before-you-code.md` section 2). This table is the fallback.

| Stack | Format | Typecheck | Lint | Covering tests | Full suite |
|---|---|---|---|---|---|
| TypeScript (pnpm) | `pnpm prettier --write <files>` or `pnpm biome format --write <files>` | `pnpm tsc --noEmit` | `pnpm eslint <files>` | `pnpm vitest related <files> --run` / `pnpm jest --findRelatedTests <files>` | `pnpm test` |
| Python (uv) | `uv run ruff format <files>` | `uv run pyright` or `uv run mypy <pkg>` | `uv run ruff check <files>` | `uv run pytest <test files>` | `uv run pytest` |
| Rust | `cargo fmt` | `cargo check --workspace --all-targets` | `cargo clippy --workspace --all-targets -- -D warnings` | `cargo test -p <crate>` | `cargo test --workspace` |
| Go | `gofmt -w <files>` | `go build ./...` and `go vet ./...` | `golangci-lint run` or `staticcheck ./...` | `go test ./<pkg>/...` | `go test ./...` |
| Kotlin / Android | `./gradlew ktlintFormat` | `./gradlew compileDebugKotlin` | `./gradlew detekt lint` | `./gradlew test --tests '<Class>'` | `./gradlew test` |
| SQL migrations | | apply to a scratch DB | `squawk <files>` | the migration's own test | full replay from empty |

## 3. Running the loop well

- **Feed analyzer output back a few findings at a time** (3 to 5), fix, rerun the analyzer. Fixes can create new findings, so the analyzer always runs again after a round. Evidence: medium (static analysis feedback loop studies).
- **Read the whole error**, not the first line. Quote the exact error in your reasoning before changing code.
- **A check that passes on the first run after a big change deserves a second look**: confirm it actually ran your files (test count went up, the file is in the output).
- **Keep the green run's output** for the report: the command, the counts, the exit code.
- **Do not loop on the same failure.** After two failed attempts at a general fix, stop and report (`tests-and-honesty.md` section 1). More retries against the same visible tests raised cheating, not quality.
- **Pre-existing failures**: prove they fail on the base branch (`git stash; <cmd>; git stash pop`), report them, leave them alone unless asked.

## 4. Enforce it: hooks and CI

A line like "always typecheck before you finish" "works most of the time, not every time" (Anthropic). For a project the user wants hardened, move the loop into the harness. Evidence: vendor claim.

Formatter after every edit, `.claude/settings.json`:

```json
{ "hooks": { "PostToolUse": [ { "matcher": "Edit|Write",
  "hooks": [ { "type": "command",
    "command": "f=$(jq -r '.tool_input.file_path // empty'); case \"$f\" in *.ts|*.tsx|*.js|*.jsx) npx prettier --write \"$f\" >/dev/null;; *.py) ruff format \"$f\" >/dev/null;; *.rs) rustfmt \"$f\";; esac; exit 0" } ] } ] } }
```

Typecheck and tests before the agent may stop, `.claude/hooks/stop-gate.sh` wired as a `Stop` hook:

```bash
#!/usr/bin/env bash
# Exit 2 keeps the agent working and sends the errors back to it.
out=$(pnpm tsc --noEmit 2>&1) || { printf 'Typecheck failed:\n%s\n' "$out" | tail -40 >&2; exit 2; }
out=$(pnpm test --silent 2>&1) || { printf 'Tests failed:\n%s\n' "$out" | tail -60 >&2; exit 2; }
exit 0
```

Claude Code lets the agent stop anyway after eight consecutive blocked stops with no tool call (`CLAUDE_CODE_STOP_HOOK_BLOCK_CAP`), so a stuck gate cannot loop forever.

CI is the last gate: the same commands run on every PR, required for merge, in config the agent cannot edit (`tests-and-honesty.md` section 9). Pre-commit hooks for format, lint and secret scanning add a second layer.

## 5. Fresh-context review against the spec

The reviewer is a separate context that did not write the code, with read-only tools, checking the diff against a written spec. Anthropic: a fresh reviewer helps "because it hasn't seen your reasoning"; and "a reviewer that's asked to find problems will always find something. If you fix every finding, you end up with extra abstraction layers and tests for cases that can't happen." Published AI reviewer figures cluster around 50% F1, so it adds recall, not certainty. Evidence: vendor claim and medium.

How:

1. Write the spec down if it is not already: the acceptance list from step 0.
2. Start a read-only reviewer (a subagent with only Read, Grep, Glob, or `/code-review` in Claude Code).
3. Give it the spec, the diff (`git diff origin/main...`), the caller list, and this brief:

```text
Review this diff against the spec below. Do not comment on style, naming or formatting.
Report only:
- spec items not implemented, or implemented differently
- callers or importers of changed code that were not updated
- bugs: wrong logic, unhandled error paths, races, off by one, null cases
- security: injection, missing authorization, secrets, unsafe output
- tests that were weakened, skipped, or that assert nothing meaningful
- edge cases from the spec with no test
For each finding: file:line, what is wrong, the evidence (code quoted or a command to run),
and how sure you are (certain / likely / possible). Say "no findings" if there are none.
```

4. Triage: fix "certain" findings; check "likely" ones with a test or a command before changing code; drop findings that are style or that ask for abstraction the task did not need. Say in the report which findings you dropped and why.
5. A human reads any change that touches tests, dependencies, migrations, auth or destructive operations.

## 6. When a check cannot run

Typical causes: no test suite, a service the tests need is down (DB, Redis), missing env vars or keys, no network, a platform the machine lacks, a suite that takes hours.

1. **Try to make it run, within scope and without touching production.** Install dev dependencies from the lockfile (`pnpm install --frozen-lockfile`, `uv sync`), start local services the repo already defines (`docker compose up -d db`), use the test env file the repo provides, run the subset that does not need the missing piece (`pytest -m "not integration"`).
2. **Do not fake it.** No mock that replaces the code under test, no skipping the test, no writing "passes" for a check that did not run, no secret fetched from somewhere the user did not offer.
3. **Run the nearest substitute** and say it is a substitute: typecheck when tests cannot run; a script that calls the function directly when the integration test cannot (section 7); a dry run (`terraform plan`, `prisma migrate diff`) when the real apply is not allowed.
4. **Report it in this form:**

```text
Not run: integration tests (tests/integration/), need STRIPE_TEST_KEY which is not set.
Substitute: unit tests for the webhook handler (9 passed) and a script that posts a recorded
  webhook payload to the local server (200, row written, see output above).
Risk: signature verification against real Stripe is unverified.
To run it: STRIPE_TEST_KEY=... pnpm test:integration
```

5. If no test suite exists at all, write the smallest test that proves the change (one file, the project's language and the most common test runner for it) and say that you added it.

## 7. Full stack features without a browser

When a browser cannot be used, verify every layer that can be reached from the terminal, and say plainly that the visual layer is unverified. Evidence: practice, not measured; the Claude docs list "a screenshot next to the mockup" as a check, which is the one step left out here.

1. **Front end compiles and its logic is tested**: typecheck, `build`, and component tests in a DOM emulator (Testing Library with jsdom or happy-dom) for the states that matter: loading, empty, error, filled, unauthorized.
2. **Back end, through the real HTTP layer**: start the server, then call it the way the UI will.
   ```bash
   pnpm dev >/tmp/server.log 2>&1 &   # or the project's start command
   until curl -s localhost:3000/health >/dev/null; do sleep 0.5; done
   curl -sS -w '\n%{http_code}\n' -X POST localhost:3000/api/invoices \
     -H 'content-type: application/json' -H "authorization: Bearer $TEST_TOKEN" \
     -d '{"customerId": 1, "lines": [{"amount": 1999}]}'
   ```
   Cover the happy path, a validation error (expect 400/422), no auth (expect 401), someone else's resource (expect 403/404), and not found. Check the status code and the body shape the UI reads.
3. **The data actually changed**: query the database directly after the call.
   ```bash
   psql "$DATABASE_URL" -c "select id, total, status from invoices order by id desc limit 3;"
   sqlite3 app.db "select * from invoices order by id desc limit 3;"
   ```
4. **A script that drives the real code** for logic with no HTTP entry (jobs, queues, CLI, sync): import the real module and call it with realistic input, against the dev database.
   ```bash
   pnpm tsx -e "import('./src/billing/close').then(async (m) => console.log(await m.closeMonth('2026-10')))"
   uv run python -c "from billing.close import close_month; print(close_month('2026-10'))"
   ```
5. **Logs**: read the server log for errors and warnings during the calls (`rg -n -i 'error|warn' /tmp/server.log`).
6. **The contract between layers**: the field names and types the front end reads match what the API returned in step 2. Compare the generated client or the TypeScript types against the real response.
7. **Stop what you started**: kill the dev server and any containers you launched.
8. **State what is unverified**, specifically, with how to check it:

```text
Verified from the terminal: build, 12 component tests, API (5 cases, outputs above), DB rows, server log clean.
Not verified: the visual layer (layout, styling, focus and hover states, responsive widths,
  the toast after saving). Please open http://localhost:3000/invoices/new, add a line,
  save, and check the toast and the new row in the list.
```

## 8. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| Done defined | a failing test or an acceptance list existed before the edit | named in the plan |
| Formatter | changed files formatted | the format command in check mode (`prettier --check`, `ruff format --check`, `cargo fmt --check`, `gofmt -l`) prints nothing |
| Typecheck | 0 errors | the typecheck command's output in the report |
| Lint | 0 errors on changed files | the lint command's output |
| Covering tests | all pass, and they were run first | the related-tests command and counts |
| Full suite | pass, or pre-existing failures proven on base | full run counts plus the base run |
| App starts | the changed path responds | a curl or script output in the report |
| Review | fresh-context review done, findings triaged | the review findings and what was done with each |
| Unrun checks | each listed with reason, substitute and risk | the "Not run" block in the report |
| Visual layer | marked unverified when no browser was used, with steps for the user | the report's "Not verified" line |
