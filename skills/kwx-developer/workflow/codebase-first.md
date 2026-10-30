# Codebase first: the first contact procedure for any repo

Run this before the first edit, the first review comment or the first audit finding in a repo you have not mapped in this conversation. It produces a short project map: the stack, the real check commands, the house conventions, the decisions in force and the open TODO items. Every other workflow file starts from that map. The why is measured: agents copy whatever they read first, obey commands that are named to them, and fail in big repos by reading too much, not by reasoning badly (`ai-agents/before-you-code.md`).

## Contents

1. When to run it, and how long it may take
2. Step 1: size and shape
3. Step 2: detect the stack
4. Step 3: read the instruction files, DECISIONS.md and TODO.md
5. Step 4: find the real check commands
6. Step 5: run the convention scan
7. Step 6: find the layers and the entry points
8. Step 7: hotspots (audits and big changes only)
9. Step 8: write the project map
10. Where the map lives: conversation by default, opt in cache
11. Checks

## 1. When to run it, and how long it may take

| Situation | Run |
|---|---|
| First task in a repo in this conversation | the whole procedure |
| Another task in the same repo, same conversation | nothing; reuse the map, re-read only DECISIONS.md and TODO.md if they changed (`git diff --stat -- DECISIONS.md TODO.md`) |
| A one line fix the user pointed at (typo, a constant) | steps 3 and 4 only |
| An audit (`audit-and-ask.md`) or a full stack feature (`feature-workflow.md`) | the whole procedure, including step 7 |

Budget: about 5 minutes and 15 to 25 tool calls for a repo under 2,000 files. Over that size, follow `ai-agents/before-you-code.md` section 6: search for the task's domain words, read only the change path, and hand broad sweeps to a read-only search subagent that returns its conclusion, not file dumps. If you have opened about 30 files and have no map, stop reading and write the map with the unknowns marked.

Run every command from the repo root. If the folder is not a git repo, skip the git commands, say so in the map, and treat every later "before and after" check as a manual comparison.

## 2. Step 1: size and shape

```bash
git rev-parse --show-toplevel && git rev-parse --short HEAD
git ls-files | wc -l                                              # tracked files
git ls-files | sed 's|/[^/]*$||' | sort | uniq -c | sort -rn | head -25   # busiest folders
git ls-files | sed -n 's/.*\.\([A-Za-z0-9]*\)$/\1/p' | sort | uniq -c | sort -rn | head -12   # languages by extension
git rev-list --count HEAD; git log -8 --format='%h %ad %s' --date=short   # age and recent activity
command -v tokei >/dev/null && tokei . -s code | head -20         # lines per language, when installed
```

Read the output for: total size (under 2,000 files is small, over 2,000 is big), the organising principle at the top level (feature folders, layer folders, or a mix, which is itself a lead), and whether the history is long enough for churn (under about 50 commits it is not, `quality/hotspots.md` section 9).

Monorepo signals: `ls pnpm-workspace.yaml turbo.json nx.json lerna.json 2>/dev/null`, a `workspaces` key in `package.json`, `[workspace]` in the root `Cargo.toml`. In a monorepo, every later step runs per package, and the scan uses `--depth 3`.

## 3. Step 2: detect the stack

```bash
ls package.json Cargo.toml pyproject.toml go.mod pubspec.yaml build.gradle* app.json app.config.* 2>/dev/null
find . -name package.json -not -path '*/node_modules/*' | head -20
jq -r '(.dependencies // {}) + (.devDependencies // {}) | keys[]' package.json 2>/dev/null \
  | grep -xE 'next|react|react-native|expo|expo-router|vite|svelte|vue|@nestjs/core|express|fastify|hono|prisma|@prisma/client|drizzle-orm|kysely|@supabase/supabase-js|zod|valibot|@tanstack/react-query|swr|zustand|redux|@reduxjs/toolkit|vitest|jest|@playwright/test|typescript|eslint|@biomejs/biome|prettier'
grep -A40 '^\[dependencies\]' Cargo.toml 2>/dev/null | grep -oE '^(axum|actix-web|tokio|sqlx|diesel|sea-orm|serde|thiserror|anyhow|tracing|tauri|reqwest|clap)\b'
grep -h '"typescript"\|"next"\|"expo"\|"react-native"' package.json 2>/dev/null   # versions matter: read them
```

Write the stack as one line per layer, with versions from the lockfile or manifest: runtime and framework, database and access layer, validation, client data library, test runners, lint and format tools. Then pick the master files to read for the task:

| Signal | Read |
|---|---|
| `.ts`, `.tsx`, `package.json` with `typescript` | `languages/typescript/typescript.md` |
| `Cargo.toml` | `languages/rust/rust.md` |
| a server framework, routes, handlers, jobs | `backend/backend.md` |
| migrations, an ORM, SQL, SQLite | `data/data.md` |
| auth, user input, uploads, secrets, payments | `security/security.md` |
| error handling, logging, CI, deploy, tests | `reliability/reliability.md` |
| screens or components in the change | the sister skill kwx-designer, see `workflow/duet-with-kwx-designer.md` |

## 4. Step 3: read the instruction files, DECISIONS.md and TODO.md

```bash
find . \( -name CLAUDE.md -o -name AGENTS.md -o -name CONTRIBUTING.md -o -name ARCHITECTURE.md \
  -o -name DECISIONS.md -o -name TODO.md -o -name copilot-instructions.md \) \
  -not -path '*/node_modules/*' -not -path '*/target/*' 2>/dev/null
ls .claude/rules .cursor/rules docs/adr docs/decisions doc/adr 2>/dev/null
```

1. Read every `CLAUDE.md` and `AGENTS.md` on the path to the files you will touch, nearest last (nearest wins). Their commands and rules override this skill.
2. Read `DECISIONS.md` and every ADR in full, never with `head`. Build the do-not-flag list with the awk in `quality/decision-records.md` section 6 and keep it in the map. A decision in that list is never reported or asked about again.
3. Read `TODO.md` in full. Note its heading, id and wrap style (`quality/tech-debt-and-todo.md` section 5) and the open finding keys:
   ```bash
   grep -E '^\s*- \[ \]' TODO.md | grep -oE '`[a-z-]+:[^`]+`' | sort -u
   ```
   An open item is already decided as "later": it is not a new finding.
4. If the task conflicts with an Accepted decision, stop and ask before writing code, quoting the decision.
5. README: read the setup and run sections only. Skip architecture tours unless the task needs them.

## 5. Step 4: find the real check commands

The commands CI runs are the definition of "passes". Collect them before editing (`ai-agents/before-you-code.md` section 2):

```bash
grep -rhn 'run:' .github/workflows/ 2>/dev/null | head -40
jq -r '.scripts // {} | to_entries[] | "\(.key): \(.value)"' package.json 2>/dev/null
grep -nE '^[a-zA-Z][a-zA-Z0-9_-]*:' Makefile justfile 2>/dev/null | head -30
ls .husky lefthook.yml .pre-commit-config.yaml 2>/dev/null
```

Fill this row set; write "none" where the project has none, never a guess:

| Check | Command | Source |
|---|---|---|
| format | `pnpm prettier --check .` | `package.json` scripts |
| typecheck | | |
| lint | | |
| test, all | | |
| test, one file | | |
| build | | |
| run locally | | |
| migrations | | |

A command named in an instruction file wins over one you infer. If CI and the scripts disagree, use CI and note the difference as a lead.

## 6. Step 5: run the convention scan

```bash
python3 -I ${CLAUDE_SKILL_DIR}/scripts/scan_conventions.py . > "$SCRATCH/scan-before.txt"   # --depth 3 in a monorepo
grep -E '^==|majority|OFF|MIX|ODD' "$SCRATCH/scan-before.txt"
```

`$SCRATCH` is the session scratchpad; never write the scan into the repo. From the output, record for each dimension the house convention (the majority, or the variant decided by the precedence in `architecture/consistency.md` section 2). Every OFF, MIX and ODD line is a lead, not yet a finding: confirm it by opening two files from each side, and check `architecture/consistency.md` section 3 for framework shapes that are not drift. Keep `scan-before.txt`: the quality gate diffs against it after your change.

The scan cannot see vocabulary, where validation happens, the client data path or dependency direction. Get those by reading two recent examples of each kind of file the task touches (`ai-agents/before-you-code.md` section 3), newest first:

```bash
git log --diff-filter=A --name-only --format= -- 'src/' | grep -vE '\.(test|spec)\.' | head -20
```

## 7. Step 6: find the layers and the entry points

Find where each layer lives, so a change lands in the live path and a feature touches the right places:

```bash
rg -l --max-count 1 -e 'createBrowserRouter|<Route |app\.(get|post)\(|router\.(get|post)\(|Router::new\(\)|\.route\("|@(Get|Post|Controller)\(' -g '!node_modules' | head -15   # routes
rg -l -e 'drizzle\(|new PrismaClient|createClient\(|sqlx::|PgPool|Database\(' -g '!node_modules' | head -10       # DB access
rg -l -e 'useQuery\(|useSWR\(|createApi\(|axios\.create\(|ky\.create\(|fetch\(' -g '!node_modules' -g '*.ts*' | head -15   # client data layer
ls migrations db/migrations prisma/migrations drizzle supabase/migrations 2>/dev/null | tail -5                # migrations
rg -l -e 'class \w*Error extends|thiserror|AppError|HttpError' -g '!node_modules' | head -5                     # error types
```

Write one line per layer: folder, the file that is the house example, and what calls what (screen, hook, client, route, service, DB).

## 8. Step 7: hotspots (audits and big changes only)

```bash
git log --since="12 months ago" --format=format: --name-only --no-renames -- . ':!*lock*' ':!*.md' \
  | grep -v '^$' | sort | uniq -c | sort -rn | head -10
```

For an audit, run the full hotspot score instead (`quality/hotspots.md` section 5). For a feature, this short list tells you whether the file you are about to change is one where every change costs more (take extra care with its tests).

## 9. Step 8: write the project map

Keep it under 40 lines. Facts with their source; unknowns marked as unknown.

```markdown
# Project map: <repo name> at <short sha>, <YYYY-MM-DD>
Size: <n> tracked files, <languages with counts>; <n> commits, last <date>; <small | big>
Stack: <framework + version>; <DB + access layer>; <validation>; <client data lib>; <tests>; <lint/format>
Layout: <top folders, one clause each>; organised by <feature | layer | mixed>
Instruction files read: <paths>
Decisions in force: <D-ids, one line each>; do-not-flag keys: <kind:area list>
Open TODO keys: <list>, TODO.md style: <heading/id/wrap>
Checks: format=<cmd>; typecheck=<cmd>; lint=<cmd>; test=<cmd>; one test=<cmd>; build=<cmd>; run=<cmd>
House conventions: exports=<variant, counts, source>; imports=<...>; errors=<helper and file>; logging=<...>; config=<...>; validation=<library, where>; tests=<runner, placement, helper>; DB=<access pattern, example file>
Layers: routes=<folder, example>; services=<...>; DB=<...>; client=<...>; UI=<...>
Leads from the scan (unconfirmed): <OFF/MIX/ODD lines worth checking>
Hotspots: <top 5, or "not run">
Unknowns: <what you could not determine and why>
```

Show the map to the user only when they asked for an overview or an audit; otherwise keep it in your notes and act on it.

## 10. Where the map lives: conversation by default, opt in cache

Decision: **the map lives in the conversation.** No file is written into the repo by default.

Why: a file the user did not ask for is an unrequested change (`ai-agents/change-discipline.md` section 3); it shows up in `git status`, can be committed by accident, and goes stale silently when the code moves on. Rebuilding the map costs a few minutes, which is cheap next to an agent trusting a stale map.

Opt in cache, only when the user says yes to "Save the project map in `.kwx/map.md` so the next session starts faster? It stays out of git.":

```bash
mkdir -p .kwx            # then write the map to .kwx/map.md with the Write tool
grep -qxF '.kwx/' .git/info/exclude || echo '.kwx/' >> .git/info/exclude   # ignored locally; no tracked file changes
git check-ignore -q .kwx/map.md && echo ignored
```

`.git/info/exclude` keeps it out of git without editing the tracked `.gitignore`. When reusing a cached map, check it is still true before trusting it:

```bash
sha=$(sed -n 's/.* at \([0-9a-f]\{7,\}\),.*/\1/p' .kwx/map.md | head -1)
git diff --stat "$sha" HEAD -- package.json '*/package.json' Cargo.toml pnpm-lock.yaml .github/ \
  CLAUDE.md AGENTS.md DECISIONS.md TODO.md tsconfig*.json eslint.config.* biome.json
```

Any output means the stack, checks, rules or decisions may have changed: rebuild the map and overwrite the file. DECISIONS.md and TODO.md are always re-read from the repo, never from the cache.

## 11. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| Instruction files read | every CLAUDE.md and AGENTS.md on the change path, DECISIONS.md and TODO.md opened in full | the map's "Instruction files read" line lists them |
| Do-not-flag list built | decision keys and open TODO keys recorded before any finding | the map has both lines, even if empty |
| Real checks found | each check row has a command from CI, scripts or an instruction file, or "none" | the map's Checks line; no invented command |
| Scan run and kept | `scan-before.txt` exists in the scratchpad | `ls "$SCRATCH/scan-before.txt"` |
| Conventions have sources | each house convention names counts or a precedence source | read the map |
| Leads not reported as findings | OFF, MIX, ODD lines stay leads until two files per side are read | the map labels them unconfirmed |
| No repo file written unasked | `git status --porcelain` unchanged by this procedure | run it before and after |
| Cache only on a yes | `.kwx/` exists only after the user agreed, and is ignored | `git check-ignore -q .kwx/map.md` |
