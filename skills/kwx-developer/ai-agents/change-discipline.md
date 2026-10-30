# Change discipline

How to make the change itself: small, complete across every caller, nothing unrequested, no invented dependencies, current APIs, no swallowed errors, no stubs, and a plain report of what was not checked.

Why this file exists: in 33,596 agent PRs on GitHub, each extra changed line cut merge odds by about 1% and each failed CI check by about 15%, and reviewers kept asking for smaller, focused PRs. 27.3% of divergent SWE-bench patches added behaviour nobody asked for. Evidence: medium.

## Contents

1. One purpose per change
2. Every caller and importer updated
3. No unrequested changes
4. No invented dependencies
5. Current APIs, read from the installed version
6. No swallowed errors
7. No stubs left behind
8. Security is part of every change
9. Report what was not checked
10. Checks

## 1. One purpose per change

- **One change does one thing the user asked for.** A bug fix, a feature, or a refactor; not two of them. Reason: diff size predicts rejection, and AI reviewer recall near 50% leaves more misses in a big diff. Evidence: medium.
- **Refactor and behaviour change go in separate commits.** If the fix needs a refactor first, commit the refactor with the suite green, then the fix. The reviewer can then read the refactor as "no behaviour change" and check it with a differential test (`tests-and-honesty.md`).
- **Keep formatting churn out.** Run the formatter only on files you changed; if the repo is not formatted, do not format it inside this task.
- **Measure before you report:** `git diff --stat origin/main...`. If the diff is much larger than the task suggests, find out why before going on: usually it is a second purpose or a reformat.

## 2. Every caller and importer updated

The caller list from `before-you-code.md` section 5 is the to-do list for this step. Missed callers are the main reason a passing patch is wrong (29.6% of "resolved" SWE-bench patches diverge from the real fix). Evidence: strong.

After changing a name, signature, type, return shape, response field, column, event or config key:

1. Update every caller on the list, including tests, fixtures, mocks, factories, seed data, storybook stories, docs and examples.
2. Update the export surface: barrel files (`index.ts`), `__init__.py` re-exports, `pub use` in `lib.rs`, the public API docs, the OpenAPI or GraphQL schema, generated clients (regenerate them with the project's command, do not hand-edit generated files).
3. Search again for the old shape. The search must come back empty or every hit must be intended:
   ```bash
   rg -n -w 'oldName'                       # code
   rg -n "['\"]old_key['\"]"                # string keys: JSON, SQL, config, events, i18n
   rg -n 'oldName' -g '*.md' -g '*.yml' -g '*.json'   # docs and config
   ```
4. Run the typechecker and build (`tsc --noEmit`, `cargo check --workspace`, `go build ./...`, `pyright`), then the covering tests of every caller.
5. If the old shape is used by things outside this repo (a public API, a mobile app already shipped, another service), do not change it in place. Add the new shape beside the old, migrate callers, and remove the old one later (expand and contract). Ask the user if the outside callers are unknown.

## 3. No unrequested changes

- **Build what the task names and nothing else.** No new options, flags, config, abstraction layers, base classes, extra files, or "for later" hooks. Anthropic says recent Opus models tend toward "creating extra files, adding unnecessary abstractions, or building in flexibility that wasn't requested". Evidence: vendor claim, plus PatchDiff 27.3% (medium).
- **Validate at system boundaries only**: user input, HTTP requests, files, env, external APIs. Do not re-validate inside internal calls that already receive checked data. Reason: defensive checks everywhere hide where the real contract is. Evidence: vendor claim.
- **Do not rename, move, reorder or restyle code you were not asked to touch.** Reason: it inflates the diff and hides the real change.
- **Write what you noticed as follow-ups, not as edits.** Add them to TODO.md or the report: "Duplicate helper `fmtDate` in `utils/time.ts` and `lib/date.ts`; not merged here."
- **In scope, always:** anything your change breaks (callers, tests, types, docs that describe the changed behaviour), and the error handling and validation of any code you move or merge.

## 4. No invented dependencies

Across 16 models, 19.7% of recommended packages did not exist; 43% of those fake names came back on every rerun, which makes them registrable by an attacker (an empty package under one such name drew over 30,000 downloads). Checking that the name exists is not enough, since an attacker may already own it. Evidence: strong.

Before adding any package:

1. **Look for it already installed.** Read the manifest and the lockfile; use the standard library or an installed package if it covers the need. Reason: zero new supply chain risk, zero new version to track.
2. **Ask the user.** A new dependency is a decision with a long tail. Name the package, the version, why the installed ones do not cover it, and the size.
3. **Check the registry, not your memory:**
   ```bash
   npm view <pkg> name version time.created time.modified repository.url dist.unpackedSize
   curl -s https://pypi.org/pypi/<pkg>/json | jq '.info.name, .info.version, .info.project_urls, (.releases|keys|length)'
   cargo info <pkg>            # or: curl -s https://crates.io/api/v1/crates/<pkg> | jq '.crate | .name, .created_at, .downloads'
   go list -m -versions <module>
   ```
   Red flags: created in the last few months, very few downloads, no repository link, a name one letter away from a popular package, a description that does not match.
4. **Add it only through the package manager** (`pnpm add`, `uv add`, `cargo add`, `go get`), so the lockfile records the exact version and hash, and commit the lockfile with the change.
5. **Never install from a name you have not checked**, and never `curl | sh` an installer the user did not ask for.

## 5. Current APIs, read from the installed version

All seven LLMs tested at ICSE 2025 struggled with deprecated APIs, outdated code in the surrounding context pushed them further toward deprecated calls, and a prompt line alone was not enough. Evidence: medium (completion models, not agents).

1. **Read the installed version**, not the latest:
   ```bash
   npm ls <pkg>            # or: jq -r '.packages["node_modules/<pkg>"].version' package-lock.json
   uv pip show <pkg>       # or: pip show <pkg>
   cargo tree -i <crate> --depth 0
   go list -m <module>
   ```
2. **Read that version's API**, in this order: the type definitions and docs inside the installed package (`node_modules/<pkg>/dist/*.d.ts`, `README.md`, `CHANGELOG.md`), `cargo doc --open -p <crate>`, `go doc <pkg>.<Symbol>`, `python -c "import x; help(x.fn)"`; then the official docs for that exact version; then a docs retrieval tool if the agent has one.
3. **Turn the deprecation warning into a failure** in the loop where the stack allows: `@typescript-eslint/no-deprecated` (typescript-eslint v8), `python -W error::DeprecationWarning -m pytest`, Rust `#![deny(deprecated)]` or `RUSTFLAGS="-D deprecated"`, Go `staticcheck` (SA1019).
4. **Do not copy an old call just because the file next to you uses it.** If the neighbour uses a deprecated API, write the new call in your code and list the old ones as a follow-up.
5. **Do not upgrade a dependency to get a newer API** unless the task asks for it. Write against what is installed or ask.

## 6. No swallowed errors

GitClear reports "error-masking" up 47% versus 2022, and Anthropic's Claude 4 card notes the model sometimes wrote "plausible-seeming solutions without acknowledging flaws". No study isolates this for agents. Evidence: weak.

Rules:

- **No empty catch, no catch that only logs and continues when the failure changes the result.** Either handle it (retry, fallback that is correct for the user, a typed error result) or let it propagate.
- **No fallback value that hides a failed call**: `?? []` after a failed fetch, `unwrap_or_default()` on a parse error, `except Exception: return None`, `_ = err` in Go, `.catch(() => {})`. A default is fine only when "missing" is a real, expected state and the code says so.
- **Use the project's named error helper and error types**, found from the 2 examples in `before-you-code.md`. Do not invent a new error class or a new response shape.
- **Catch the narrowest error type**, keep the cause (`raise X from e`, `new Error(msg, { cause })`, `.context()` in anyhow, `fmt.Errorf("...: %w", err)`).
- **Report failures in the final message plainly**, including a failure you could not fix.

Lint for it, so the rule is not left to prose:

| Stack | Rules |
|---|---|
| TS / JS | ESLint `no-empty`, `@typescript-eslint/no-floating-promises`, `@typescript-eslint/no-misused-promises` |
| Python | Ruff `E722` (bare except), `BLE001` (blind except), `S110` (try-except-pass) |
| Rust | Clippy `unwrap_used`, `expect_used` in library code, `let_underscore_must_use` |
| Go | `errcheck`, `errorlint` (through golangci-lint) |

The project's full error policy belongs in `reliability/error-handling-strategy.md`.

## 7. No stubs left behind

A stub that compiles looks finished to a reviewer skimming the diff. The Replit agent fabricated 4,000 records rather than admit a failure. Evidence: weak (no measured rate), strong as an incident.

Before finishing, grep the diff:

```bash
git diff origin/main... | rg -n '^\+.*(TODO|FIXME|XXX|HACK|todo!\(|unimplemented!\(|NotImplementedError|not implemented|placeholder|lorem|console\.log\(|dbg!\(|print\()'
```

Each hit is one of three things: finished now, removed, or listed in the report under "Not done" with the reason. No sample data or hard-coded return in a production code path. No `// handle error later`. Debug prints removed unless the project logs that way.

## 8. Security is part of every change

About 45% of AI code on security-relevant benchmark tasks picks the insecure option, flat across model generations; developers with an AI assistant wrote insecure code more often and believed it was secure. Only 14.8% of real agent context files mention security. Evidence: strong.

On every change that touches input, output, storage, auth or secrets:

- Parameterized queries or the query builder; never build SQL from strings.
- Encode output for its context (HTML, attribute, URL, shell); XSS was defended in only 14 to 15% of benchmark samples.
- Put the authorization check in the handler of every new route or action, next to the code, not only in a config file elsewhere. Ronacher: an indirect permission check "will almost guarantee" the agent omits it on a new route.
- No secrets in code, logs or error messages. Read them from env or the secret store the project already uses.
- Run the project's SAST if it has one (`semgrep --config auto <changed files>`, `bandit -r <dir>`, `cargo audit`, `npm audit --omit=dev`), and run it again after each fix since fixes can add new findings.

The full security rules live in `security/`.

## 9. Report what was not checked

Every task ends with a report that says, plainly, what was not checked. Reason: an unstated gap is read as "verified". Evidence: vendor claim.

```text
Changed: src/billing/invoice.ts (rounding), 4 callers updated (list), DECISIONS.md entry added
Ran: tsc 0 errors; eslint 0; vitest related 14 passed; full suite 812 passed
Not checked:
  - mobile app reads `total` from the API: not in this repo, field name unchanged so should be safe
  - PDF export rendering: needs a browser, not run
Not done: retry on Stripe timeout (follow-up added to TODO.md)
New dependencies: none
```

## 10. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| Diff size fits the task | one purpose, no reformat churn | `git diff --stat origin/main...` read against the task |
| Old shape gone | no unintended hits | the rg searches in section 2, step 3 |
| Types and build | 0 errors | the project's typecheck and build commands |
| No unrequested files | every new file is needed by the task | `git diff --name-status origin/main... --diff-filter=A` |
| Dependencies | none added, or each checked in the registry and approved | `git diff origin/main... -- package.json pyproject.toml Cargo.toml go.mod` |
| Lockfile committed with any new dependency | lockfile changed in the same commit | `git show --stat HEAD` lists the lockfile |
| No deprecated calls added | deprecation lint clean on changed files | the lint in section 5, step 3 |
| No swallowed errors | lint rules in section 6 pass | the project's lint, or the rules added for this run |
| No stubs | the stub grep in section 7 is empty or every hit is reported | run it |
| Security | SAST clean on changed files, authz check in every new handler | the SAST command, then read each new handler |
| Report | Changed / Ran / Not checked / Not done / New dependencies present | read the final message |
