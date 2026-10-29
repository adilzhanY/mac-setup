# Ponytail 5.1.0: skills, commands, rule copies and docs

Source root: `~/.claude/plugins/cache/ponytail/ponytail/5.1.0` (P). Read in full, read only.

## Files read

- `skills/ponytail/SKILL.md`, `skills/ponytail-review/SKILL.md`, `skills/ponytail-audit/SKILL.md`, `skills/ponytail-debt/SKILL.md`, `skills/ponytail-gain/SKILL.md`, `skills/ponytail-help/SKILL.md`, `skills/plugin.json`
- `.openclaw/skills/*/SKILL.md` (all six, diffed against `skills/`)
- `commands/*.toml` (six), `.opencode/command/*.md` (six, diffed against the toml prompts)
- Rule copies diffed against `AGENTS.md`: `.cursor/rules/ponytail.mdc`, `.windsurf/rules/ponytail.md`, `.clinerules/ponytail.md`, `.kiro/steering/ponytail.md`, `.agents/rules/ponytail.md`, `.qoder/rules/ponytail.md`, `.github/copilot-instructions.md`
- `README.md`, `INSTALL.md`, `after-install.md`, `docs/agent-portability.md`, `docs/cursor-hooks.md`, `.github/CONTRIBUTING.md`

## Differences between the copies

- **OpenClaw skills vs `skills/`:** bodies are byte identical. Only frontmatter differs: the long folded multi-line description with trigger phrases becomes a one-line quoted description without trigger phrases, plus `homepage` and `license`. The main `ponytail` OpenClaw copy drops `argument-hint` and `license`. The copy is generated (`scripts/build-openclaw-skills.js`) and the test suite fails when it is stale.
- **`.opencode/command/*.md` vs `commands/*.toml`:** prompts are identical except `{{args}}` becomes `$ARGUMENTS`, and `ponytail-debt`: the toml row format uses an em dash (`<file>:<line> [em dash] <what was simplified>`) where the OpenCode copy and the skill use a comma. So a stale character survived in one copy.
- **Command prompts vs skills:** each command prompt is a one-paragraph compressed version of its skill, for hosts that cannot load skills. They drifted: `ponytail-help.toml` still calls review and audit an "over-engineering review" and ultra "deletion before addition", while the skills were rebuilt into a full quality review and ultra now means "question the request". The copy check script covers rule copies, not command prompts.
- **Rule copies vs `AGENTS.md`:** body identical to `AGENTS.md` (which equals the ponytail SKILL.md body minus the persistence line and the levels table). Differences: `AGENTS.md` has one extra closing line ("this file also applies to agents working on the ponytail repo itself"); Cursor adds frontmatter `description`, `globs:`, `alwaysApply: true`; Kiro adds `title` and `inclusion: always`. Everything else is a plain copy.

## Lessons

Status checked with `grep -rniE` over `~/.claude/skills/kwx-designer` (excluding `sources/`), two or three keyword sets each. Paths below are relative to kwx-designer.

### A. The core build rules (skills/ponytail/SKILL.md, AGENTS.md, rule copies)

| id | Lesson | Source | Status | Suggested home and reason |
|---|---|---|---|---|
| A1 | Give the agent one identity sentence that carries the whole stance ("You are a lazy senior developer. The best code is the code never written."). | ponytail/SKILL.md:15 | COVERED SKILL.md:8 ("You design like a senior product designer") | |
| A2 | End every reply with one or two lines: what you skipped or did not check, and any risk the user must know. | ponytail/SKILL.md:15, README:118 | PARTIAL quality-gate.md:193 ("Not checked and why", only inside the gate report) | SKILL.md "Before you finish": make it the last line of every reply, not only the gate report |
| A3 | A mode stays on for the whole session until an explicit off phrase; startup and mode change text names the current level. | ponytail/SKILL.md:17, README:148 | NEW | not needed in kwx (it is task triggered); note only |
| A4 | Before writing, list every place the change must reach: callers, tests, fixtures, config, exports. That is scope; extra features are not. | ponytail/SKILL.md:21 | PARTIAL quality-gate.md:28 (lists screens, components and states touched; not importers of a changed shared component, tests, stories, snapshots, exports) | quality-gate.md section 1 step 1: add "every screen that imports a component or token you changed" |
| A5 | Check what the change could break for users: data it would destroy or expose, callers that stop working. | ponytail/SKILL.md:21 | PARTIAL heuristics.md:63 (high-cost errors in the designed UI, not in your change) | quality-gate.md section 1: a "what could this change break" line |
| A6 | Ordered ladder, stop at the first rung that fully works: does it need to exist, already in this codebase, standard library or platform feature, installed dependency, one line, then the minimum. | ponytail/SKILL.md:25-32, README ladder image | PARTIAL design-process.md:64 (shared components), accessibility.md:102 (native elements first), restraint-and-reduction.md:115 (decide what not to build); no single ordered ladder | workflow/design-process.md section 5 Build: one ordered ladder for UI (need, house component, native element, installed lib, new code) |
| A7 | Skip features, options and flexibility nobody asked for, and name what you skipped in one line. | ponytail/SKILL.md:27 | PARTIAL restraint-and-reduction.md:115 (decide what not to build); the "name it in one line" part is missing | restraint-and-reduction.md section 9 |
| A8 | A vague request ("build me X") gets the smallest version that does the core job. | ponytail/SKILL.md:27 | PARTIAL design-process.md:30 (write the brief, state assumptions), restraint-and-reduction.md:117 (Simple, Lovable, Complete) | design-process.md section 1: say the core job and build that first |
| A9 | Reuse what the codebase already has, the way the surrounding code uses it. | ponytail/SKILL.md:28 | COVERED design-process.md:64, critique-method.md:52 | |
| A10 | A house component beats a native widget; the standard or platform feature beats custom code unless the project has its own. | ponytail/SKILL.md:29 | PARTIAL SKILL.md:48 (read the project's design system first) and accessibility.md:102 (native first) never say which wins when both exist | design-process.md Build ladder: house component first, then native, and prefer a house component that wraps the native element |
| A11 | Worked example: "add a date picker". Without the skill: a library or a hand built calendar, 335 lines. With it: the repo's `Input` with `type="date"`, the browser brings the calendar, 10 lines. | README:82-88, assets/v5/beforeafter.png alt text | NEW (grep "date picker", "type=date": nothing) | design-process.md Build, as the example for A6 and A10 |
| A12 | Never add a dependency for a few lines (a date picker, an icon pack, an animation library for one transition). | ponytail/SKILL.md:30 | NEW | design-process.md Build ladder |
| A13 | Be lazy about the solution, never about the change: finish every part the task needs, including the callers, tests and fixtures your change breaks. | ponytail/SKILL.md:34 | NEW | quality-gate.md section 1: done means every importer, test and story still works |
| A14 | No abstraction, wrapper, prop, variant, option or config "for later" that nobody asked for. Keep values in the form the platform gives you (no needless type conversions). | ponytail/SKILL.md:35 | NEW (design-system-first.md:112-116 even asks to predefine variants; no rule against speculative ones) | workflow/design-system-first.md section 8: define variants and props only for states the product has |
| A15 | Deletion beats addition. | ponytail/SKILL.md:35 | PARTIAL restraint-and-reduction.md:76-88 (for UI elements, not for code) | restraint-and-reduction.md section 5: apply the same cut to code (dead variants, unused props, duplicate components) |
| A16 | Keep the structure the codebase already has: its layers, interfaces and conventions. | ponytail/SKILL.md:35 | PARTIAL SKILL.md:41 (house rules override), mental-models-and-conventions.md:68 (product consistency); code structure not named | design-process.md Build |
| A17 | The shortest working diff wins, once you know everything it must touch. A one-liner that needs decoding is not short. | ponytail/SKILL.md:36 | NEW | design-process.md Build |
| A18 | Comment only the why the code cannot show, in one line. | ponytail/SKILL.md:37 | NEW | design-process.md Build |
| A19 | Bug fix: grep every caller first, then fix the root cause once in the shared code (for UI: fix the shared component or token, not each screen). | ponytail/SKILL.md:38 | PARTIAL quality-gate.md:140 (H1 shared chrome), SKILL.md:169 (mistakes library); root cause in the shared source not stated | quality-gate.md section 1 or a "fixing a reported defect" step in SKILL.md |
| A20 | Code you move or merge keeps its error handling and validation (in a redesign: the form keeps its validation, aria, error and empty states). | ponytail/SKILL.md:39 | NEW | workflow/redesign-method.md section 1, since redesigns move the most code |
| A21 | Between options of equal size, take the one that is correct on edge cases. | ponytail/SKILL.md:40 | NEW | design-process.md Build |
| A22 | Lazy code without its check is unfinished: new non-trivial logic (a branch, a loop, a parser, money, security, a new app) leaves one small test or an assert based self-check; trivial changes need none. In UI: formatters, price and savings maths, layout calculations. | ponytail/SKILL.md:41, README:118 | NEW (only the skill's own evals exist) | quality-gate.md section 1: one test for any UI logic with a branch or money |
| A23 | Mark a deliberate shortcut with a fixed form: `shortcut: <the limit>, <when to upgrade>`. | ponytail/SKILL.md:42 | NEW | design-process.md Build |
| A24 | Never cut: validation at trust boundaries, error handling that prevents data loss, security, accessibility, the calibration real hardware needs, anything the user asked for. | ponytail/SKILL.md:44, README:116 | PARTIAL restraint-and-reduction.md:121-128 (contrast and information) and visual/accessibility.md; no single never-cut list | restraint-and-reduction.md section 10: list what simplification may never remove |
| A25 | Levels: lite builds what was asked and names the smaller option in one line, letting the user pick; ultra questions the request and pushes back on any part the need does not justify before building. | ponytail/SKILL.md:50-52 | PARTIAL design-process.md:30 ("Ask only when a wrong guess would waste the work") | design-process.md section 1: when a requested element has no job, say so before building |
| A26 | "The rule was never fewest tokens": the result is small because it is necessary, not golfed. Lower cost is a side effect. | README:80 | NEW | SKILL.md critical rules, so restraint is not read as minimalism (pairs with restraint-and-reduction.md section 2) |
| A27 | The ladder runs after understanding, not instead of it: lazy about the solution, never about reading. | README:114 | PARTIAL SKILL.md:48 (brief: what exists) | design-process.md section 1 |

### B. Review and audit method (skills/ponytail-review, skills/ponytail-audit, commands)

| id | Lesson | Source | Status | Suggested home and reason |
|---|---|---|---|---|
| B1 | Review like the person who will be paged when it breaks; audit like the one who just inherited it. Ownership framing sets the bar. | review:11, audit:11 | NEW | quality/critique-method.md intro |
| B2 | Fixed priority order for findings: correct, safe, holds under load, tested, fast, lean. Lean still matters because every extra line is read, tested and fixed later. | review:12-13 | PARTIAL critique-method.md:25 (layer order for the review) and :102 (lead with blockers) | critique-method.md section 12: a UI priority order (works in every state, honest, accessible, consistent, polished, lean) |
| B3 | A report the user asked for is given in full; the brevity rules do not apply to it. | review:14, audit:14 | NEW | critique-method.md section 12 |
| B4 | Default target when the user names none: the uncommitted changes, else the last commit. Accept staged, branch, PR link, files. | review:18-20 | NEW | critique-method.md section 1 |
| B5 | Read the connected code, not only the diff: callers of every changed function, what it calls, the tests, the README. Benchmark: problems outside the diff found 100% vs 78% without the skill. | review:21-22, README:95-98 | PARTIAL critique-method.md:52 (routes and tokens) | critique-method.md section 1: open every importer of a changed component or token |
| B6 | Trace the real flow: where data comes in, what is stored, what goes out. | review:23, audit:24 | PARTIAL critique-method.md:67 (trace break cases through handlers) | critique-method.md section 6 |
| B7 | A change can break code it does not touch: when a signature, return value, prop or field name changes, grep every caller. Benchmark example: a renamed field crashed an untouched `src/routes/feed.js`. | review:24-25, README:95 | NEW | quality-gate.md section 1 and critique-method.md section 1 |
| B8 | Find the expected load in the repo (README, deploy config), judge scale against it, and say which load you assumed. UI version: 3 rows or 30,000, one user or a team. | review:26-28, audit:22 | PARTIAL critique-method.md:37-45 (content length, empty, one item; not volume) | critique-method.md section 4: add volume and state the assumed size |
| B9 | Edge case list: empty, zero, last item, rounding, time zones. | review:32-33 | PARTIAL critique-method.md:41-45 (empty, long, short); rounding, time zone and last item missing | critique-method.md section 4 |
| B10 | A fix applied in one caller while the shared function stays broken is a finding. | review:34 | NEW | critique-method.md, consistency section |
| B11 | Scale traps: check-then-write races, the same work done by every process, lists or memory that only grow, a query per item, O(n^2) on big input, per-process state that must be shared. | review:38-40 | PARTIAL critique-method.md:64 (double tap every submit covers one race) | platforms/web/performance-and-loading.md: per-row fetch, unbounded lists, re-render per item |
| B12 | Missing test means risky logic with no test that fails when it breaks. One good test, not coverage. | review:41-43 | NEW | quality-gate.md (pairs with A22) |
| B13 | Big slowdowns are problems; small wins are suggestions; some software counts every millisecond. | review:44-45 | NEW | critique-method.md section 12 severity mapping |
| B14 | Lean taxonomy for findings: delete (dead code, unused options), reuse (the repo has it, name the path), stdlib/native, yagni (one implementation, factory with one product, wrapper that only passes calls through), merge (near copies that must change together), split. | review:46-55, audit:45-55 | PARTIAL restraint-and-reduction.md:81-87 (delete duplicates, merge similar sizes, for UI elements) | critique-method.md: a "lean" pass over components (pass-through wrapper components, near-duplicate cards, one-variant props) |
| B15 | Split by job, never by line count, and never into helpers that exist only to make a function shorter. | review:53-55 | NEW | design-process.md Build, component splitting |
| B16 | Every finding needs a concrete case: "this input or situation leads to this wrong result". No case, no finding. | review:59-60 | PARTIAL critique-method.md:103 (be specific) and the example at :110 ("tested with a white background image"); not stated as a gate | critique-method.md section 12 |
| B17 | Re-read the lines before reporting: confirm the caller exists, the value can really be empty, the code really is unused. | review:61-62 | NEW | critique-method.md section 12 |
| B18 | Before calling code unused, grep the whole tree, including tests, fixtures, config, and string or dynamic references (class names built from strings, tokens looked up by name). | audit:61-62 | NEW | restraint-and-reduction.md section 5 and critique-method.md |
| B19 | A marked shortcut that names its limit is a decision, not a finding, unless the expected load already crosses it. | review:63-64 | NEW | critique-method.md section 12 (needs A23 first) |
| B20 | Propose the smallest fix that works, prefer fixes that delete code, never add layers, frameworks or config. | review:65-66 | PARTIAL restraint-and-reduction.md (UI) | critique-method.md section 12 |
| B21 | No style taste, no "consider", no vague worries. | review:67 | PARTIAL critique-method.md:104 (taste allowed but labelled and last); the ban on "consider" and vague worries is missing | critique-method.md section 12: drop "consider" phrasing |
| B22 | Very simple English for the report: short sentences, everyday words, explain a technical term the first time; assume the reader never saw the code. | review:71-72 | PARTIAL quality-gate.md:134 and heuristics.md:42 (plain words in UI copy, not in review prose) | critique-method.md section 12 |
| B23 | Open with `What this change does:` (or `What this repo does:` plus the assumed load) in two or three sentences. | review:74, audit:74-75 | NEW | critique-method.md section 12 |
| B24 | Group findings Must fix / Should fix / Nice to have, skip empty groups; Must fix means bug, security, data loss, breaks at expected load. | review:76-81 | PARTIAL critique-method.md:101-102 (severity blocker, major, minor) | critique-method.md section 12: group by severity, skip empty groups |
| B25 | Number findings across all groups so the user can answer "fix 2 and 5". | review:82 | PARTIAL redesign-method.md:19 (numbered problems in a redesign), not in critique | critique-method.md section 12 |
| B26 | Each finding: bold title with `file:lines`, then four short parts: What this is (context for a stranger), Problem, Fix, If we skip it (the consequence). | review:83-91 | PARTIAL critique-method.md:101 (where, what, why, fix, severity); "what this is" and "if we skip it" missing | critique-method.md section 12 |
| B27 | Close with `Verdict:` (Ship, or fix N first), `Lean: -N lines possible`, `Not checked:`. | review:93-96, audit:95-98 | PARTIAL quality-gate.md:191-193 (ship yes/no, not checked); critique has no closing block | critique-method.md section 12 |
| B28 | Nothing found is reported plainly: "Looks good. Ship." plus one line on what was checked. | review:98-99, audit:100-101 | NEW | critique-method.md section 12 |
| B29 | A review or audit lists findings and changes no code. | review:101, audit:103 | NEW | critique-method.md intro: review is read only unless the user asks for fixes |
| B30 | Audit maps first: README, deploy and build config, dependency list, entry points, tests. | audit:16-21 | PARTIAL redesign-method.md:18 (inventory of screens and states) | critique-method.md: a whole-app audit section |
| B31 | Read the risky paths in full: user input, money, auth, data writes, background jobs, shared state. | audit:24-26 | PARTIAL heuristics.md:63 (high-cost errors prevented first) | critique-method.md audit section: checkout, sign in, destructive actions read end to end |
| B32 | Big scope: go deep where a mistake costs most, not file by file, and say which parts you did not read. | audit:27-28 | NEW | critique-method.md audit section |
| B33 | Cap an audit at 20 findings and say how many smaller ones were left out. | audit:83-84 | NEW | critique-method.md section 12 |
| B34 | The same rule applied differently in two places is a bug. | audit:33-34 | COVERED critique-method.md:52, quality-gate.md:144 | |

### C. Debt ledger (skills/ponytail-debt, commands/ponytail-debt)

| id | Lesson | Source | Status | Suggested home and reason |
|---|---|---|---|---|
| C1 | Every deliberate shortcut carries a greppable marker naming its ceiling and upgrade trigger, so a deferral cannot quietly become permanent ("later means never"). | debt:9-11 | NEW | design-process.md Build (with A23) |
| C2 | Harvest with a comment-prefix regex (`(#|//|/[*]) ?(shortcut|ponytail):`) and exclude `.git`, `node_modules`, `dist`, `build`; the prefix keeps prose that only mentions the convention out. | debt:15-23 | NEW | quality-gate.md section 14 fast checks |
| C3 | Skip false positives such as a note about a keyboard shortcut. Directly relevant here: kwx has whole files about keyboard shortcuts, so the marker word collides. | debt:23-24 | NEW | quality-gate.md section 14; consider another marker word for UI repos |
| C4 | Tag any marker that names no upgrade trigger as `no-trigger`; those are the ones that rot. End with `<N> markers, <M> with no trigger`. | debt:36-39 | NEW | quality-gate.md section 14 |
| C5 | Let the user name their own marker word; persist the ledger to a file only when asked. | debt:20, 41-44 | NEW | note only |
| C6 | quality-gate.md:217 greps `TODO` as placeholder copy. Separate deferral markers in code comments (allowed when they name a trigger) from placeholder strings shown to users (always a fail). | inference from debt + quality-gate.md:217 | NEW | quality-gate.md section 14 |

### D. Measuring the skill (skills/ponytail-gain, README, CONTRIBUTING)

| id | Lesson | Source | Status | Suggested home and reason |
|---|---|---|---|---|
| D1 | Measure the skill against the same agent without it: 39 tasks (a real FastAPI + React repo, bug fixes, security and privacy cases, small apps), 5 runs each, geometric mean of per-task medians. | gain:14-19 | PARTIAL evals/evals.json (assertions per prompt, no baseline arm, no repeated runs) | evals/: add a no-skill arm and N runs per prompt |
| D2 | Give tasks hidden checks for correctness and safety that the agent never sees (18 of 39). | gain:17-18 | NEW | evals/evals.json: hidden assertions, e.g. contrast and target size computed by script |
| D3 | Report quality next to savings so efficiency cannot hide a regression: hidden checks 97% vs 96%, tests where logic needs one 98% vs 68%, injected bugs caught by own tests 66% vs 46%, six security tasks 30 of 30 runs, blind reply preference 110 to 67. | gain:28-36, README:75-78 | NEW | evals/: track a quality metric beside any "less" metric |
| D4 | Measured savings: lines of code -53%, output tokens -45%, cost -26%, time -41%. | gain:30-34, README:38 | NEW (evidence) | sources only |
| D5 | Honesty boundary: never print a per-project saving; the unbuilt version was never written, so there is no baseline. Point to a counted ledger instead. | gain:42-48 | PARTIAL quality-gate.md K2 "claims are data" (for UI claims, not the agent's own reports) | SKILL.md "Before you finish": no invented impact numbers in replies |
| D6 | Scoreboard rendering: bar length shows the share of baseline, the label carries the exact figure. | gain:24-40 | COVERED visual/data-visualization.md:78, :88 (exact value, direct labels) | |
| D7 | A rule change needs a three-arm benchmark on the same task and model: baseline, current, changed. | CONTRIBUTING:271-275 | NEW | evals/: before adding a rule to SKILL.md or quality-gate.md |
| D8 | Show a task where the change helps AND an existing task it could break ("a new rule often fights an old one"), at least 6 runs per arm, name the model. | CONTRIBUTING:277-282 | NEW | evals/ (most important guard for a growing rule set) |
| D9 | Every eval task has a good and a bad reference output, and a selftest proves the scorer tells them apart. | CONTRIBUTING:297-298 | NEW | evals/: a known-bad UI per prompt (built from mistakes.md entries) |
| D10 | Measure review recall with planted problems, including ones outside the diff: planted found 100% vs 87%, outside the diff 100% vs 78%. | README:95 | NEW | evals/: plant past defects from `~/.claude/ui-designer/mistakes.md` and check the critique finds them |
| D11 | Compare reply quality blind between versions (new beat old 110 to 67). | README:78 | NEW | evals/ |

### E. How the plugin ships and enforces itself (help, commands, plugin.json, docs, INSTALL)

| id | Lesson | Source | Status | Suggested home and reason |
|---|---|---|---|---|
| E1 | One source of truth: the prompt lives in SKILL.md, a compact copy in AGENTS.md; every other file is a thin adapter that points at them. | README:120-122, agent-portability:45-49 | PARTIAL ui-designer.md:18 reads kwx SKILL.md instead of copying it (good); no rule for future copies | SKILL.md maintenance note |
| E2 | Copies are checked by a script (`check-rule-copies.js`) and generated copies fail the test suite when stale. Yet the command prompts drifted (em dash in debt toml, old wording in help toml) because the check did not cover them: a sync check must cover every copy. | CONTRIBUTING:300-302, 325; diff results above | NEW | scripts/: a check that any duplicated rule text (SKILL.md critical rules, ui-designer.md, mistakes.md) matches |
| E3 | Each skill also exists as a one-paragraph command prompt for hosts that cannot load skills. | commands/*.toml | PARTIAL SKILL.md:11-41 (critical rules are the compact core) | note only |
| E4 | Descriptions carry the user's trigger phrases ("review this", "is this over-engineered", "what can I delete"). | skill frontmatter | COVERED SKILL.md:3, evals/triggers.json | |
| E5 | One-shot display or report skills say explicitly: do not change mode, write files or persist anything. | help:10-11, gain:11-12, debt:43 | NEW | note for any kwx sub-command; low value now |
| E6 | Config resolution is spelled out: env var, then config file, then default; `off` disables auto activation. | help:43-60 | NEW | not applicable to kwx |
| E7 | Hook injection reaches subagents by default; a regex matcher can keep it off read-only agents; an invalid regex or unknown agent type falls back to injecting. | INSTALL:191 | PARTIAL ui-designer.md:18 (agent reads SKILL.md itself) | note only, the current route works |
| E8 | Hook execution is not delivery: verify by asking the model to quote a string that exists only in the injected payload. | cursor-hooks:224-233, 248 | NEW | evals/: check ui-designer quotes a mistakes.md entry id it was told to check |
| E9 | A delivery pass says nothing about compliance; that needs a behavioural comparison against a baseline. | cursor-hooks:253-255 | NEW | evals/ (pairs with D7) |
| E10 | Write contracts with source, date and version, and mark what is documented vs verified in shipped code; treat undocumented behaviour as version dependent. | cursor-hooks:102-112 | PARTIAL editors/case-studies.md:155 ("Not verified" column) | sources/ convention for platform numbers |
| E11 | Keep a verification record table (step, version, result, date) and mark open steps "not yet run" instead of dropping them. | cursor-hooks:245-251 | NEW | evals/ |
| E12 | Two always-on copies of the same rules are alternatives, not layers: when both are present one yields and says so, because neither can remove the other. | cursor-hooks:162-176 | PARTIAL SKILL.md:40-41 (house rules override the skill) | note only |
| E13 | Injected rule text has a size budget (Cursor inlines up to 10,000 characters; the level-filtered ruleset is about 5,300). | cursor-hooks:110, 147 | NEW | SKILL.md maintenance: keep the router and critical rules small enough to load every time |
| E14 | Fail open: hooks always exit 0 and never block; skills keep working without node, with a harmless error. | cursor-hooks:122-123, INSTALL:5 | NEW | note only |
| E15 | Installers are idempotent, keep foreign entries, refuse malformed config, and uninstall only removes entries that point at their own files. | cursor-hooks:85-94, INSTALL:235 | NEW | not applicable |
| E16 | Supply chain line: install only from the named repo and npm package; a copy shipping binaries is not genuine. | README:150 | NEW | not applicable |
| E17 | One change per PR, linked to its issue; ideas for new skills go to an issue first. | CONTRIBUTING:260-262, 314 | NEW | not needed (user's CLAUDE.md already has one commit per change) |

## Counts

- NEW: 52
- PARTIAL: 37
- COVERED: 5

(Items marked "not applicable" or "note only" are counted as NEW but have little value for kwx: A3, C5, E5, E6, E14, E15, E16, E17.)
