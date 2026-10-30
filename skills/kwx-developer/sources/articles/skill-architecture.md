# Skill architecture: how to build a large, high quality Agent Skill

Research notes for building `kwx-designer` as a big, multi folder skill. Compiled 2026-10-27 from Anthropic's official docs, the `anthropics/skills` repo, the Agent Skills open spec, three community writeups, and the two big skills already on this machine. Every rule carries its source. Where sources disagree, both sides are given.

## Contents

1. Sources
2. How a skill is loaded (the three levels)
3. Frontmatter rules
4. The description: how triggering works and how to write one that fires
5. Progressive disclosure: what goes in SKILL.md and what goes in references
6. Linking reference files so they load on demand
7. Scripts vs instructions
8. Assets
9. Naming files and folders
10. Writing style inside a skill
11. Evaluation and testing
12. Common mistakes
13. What the big Anthropic skills actually look like
14. What the local skills (mgpro, design-taste-frontend) teach
15. Recommended layout for kwx-designer (router SKILL.md)

## 1. Sources

Official (Anthropic):

- [O1] Skill authoring best practices: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices (old URL docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices redirects here)
- [O2] Agent Skills overview: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- [O3] Claude Code skills page: https://code.claude.com/docs/en/skills
- [O4] Engineering blog, "Equipping agents for the real world with Agent Skills" (2025-10-16): https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- [O5] "The Complete Guide to Building Skills for Claude" (PDF, 2026-01-29): https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf (intro page: https://claude.com/blog/complete-guide-to-building-skills-for-claude)
- [O6] anthropics/skills repo: https://github.com/anthropics/skills, in particular `skills/skill-creator/SKILL.md`, `skills/claude-api/`, `skills/pdf/`, `skills/mcp-builder/`, `skills/pptx/`
- [O7] Agent Skills open specification: https://agentskills.io/specification (the repo's `spec/agent-skills-spec.md` now points here)
- [O8] Evaluating skill output quality: https://agentskills.io/skill-creation/evaluating-skills

Community:

- [C1] Simon Willison, "Claude Skills are awesome, maybe a bigger deal than MCP" (2025-10-16): https://simonwillison.net/2025/Oct/16/claude-skills/
- [C2] Jesse Vincent (obra), superpowers `writing-skills` skill and its `references/discovery.md`: https://github.com/obra/superpowers/tree/main/skills/writing-skills
- [C3] HatchWorks, "Claude Skills Architecture: How to Design Skills That Scale": https://hatchworks.com/blog/claude/skills-architecture/

Local:

- [L1] `~/.claude/skills/mgpro` (router SKILL.md plus 22 reference files, templates, a sound library)
- [L2] `~/.claude/skills/design-taste-frontend` (one 1206 line SKILL.md, no other files)

## 2. How a skill is loaded (the three levels)

Skills are built on progressive disclosure: content enters the context window in stages, only when needed [O2][O4].

| Level | What | When loaded | Cost |
|---|---|---|---|
| 1. Metadata | `name` + `description` from the frontmatter | Always, at startup, in the system prompt | About 100 tokens per skill [O2][O7] ("a few dozen extra tokens" [C1]) |
| 2. Instructions | The body of `SKILL.md` | When the skill triggers | Under 5k tokens recommended [O2][O7] |
| 3+. Resources | Every other file in the folder | Only when Claude reads or runs it | Zero until accessed. Scripts cost only their output [O2] |

Consequences that shape the architecture:

- "No practical limit on bundled content": files cost nothing until read, so a skill "can include dozens of reference files, but if your task only needs the sales schema, that's the one file Claude loads" [O2]. The amount of context a skill can carry is "effectively unbounded" [O4].
- In Claude Code, the full skill content "stays in the conversation" once invoked, and Claude "doesn't re-read the file on later turns" [O3]. Anything in SKILL.md is paid for on every later turn.
- After compaction, Claude Code re-attaches the most recent invocation of each skill, keeping "the first 5,000 tokens of each" within a combined "25,000 tokens" [O3]. So the most important rules must sit near the top of SKILL.md [O3][O5].
- Skills need a filesystem and command execution. That is what makes Level 3 possible [C1][O2].

## 3. Frontmatter rules

`SKILL.md` must start with YAML frontmatter on line 1 (`---`). If the YAML does not parse, Claude Code loads the skill with no fields set, so `/name` still works but automatic matching on the description does not [O3].

### `name`

- 1 to 64 characters, lowercase `a-z`, `0-9` and hyphens only [O1][O2][O7].
- Must not start or end with a hyphen, no consecutive hyphens (`--`) [O7].
- Must match the parent directory name [O7] ("should match folder name" [O5]). In Claude Code it defaults to the directory name [O3].
- No XML tags, and the reserved words `anthropic` and `claude` are forbidden [O1][O2][O5].

### `description`

- Non empty, at most 1,024 characters, no XML tags (no `<` or `>`) [O1][O2][O5][O7]. The angle bracket ban is a security rule: "Frontmatter appears in Claude's system prompt. Malicious content could inject instructions" [O5].
- Must say what the skill does and when to use it [O1][O2][O7].
- In Claude Code, `description` plus `when_to_use` is truncated at 1,536 characters in the skill listing, and the whole listing has a budget of about 1% of the context window; when it overflows, descriptions of the least used skills are dropped first [O3]. Put the key use case first.

### Other fields

Open spec fields (portable to claude.ai and the API): `license`, `compatibility` (1 to 500 characters, only if there are real environment requirements), `metadata` (string to string map), `allowed-tools` (experimental) [O7]. Outside Claude Code only `name`, `description`, `license`, `compatibility`, `metadata` and `allowed-tools` are allowed; other keys are a hard error on upload [O3].

Claude Code only fields [O3]: `when_to_use`, `argument-hint`, `arguments`, `disable-model-invocation` (only the user can invoke; the description is then not in context), `user-invocable: false` (only Claude can invoke), `allowed-tools`, `disallowed-tools`, `model`, `effort`, `context: fork` with `agent` and `background`, `hooks`, `paths` (globs that limit automatic activation), `shell`. Unknown fields are ignored silently.

Claude Code substitutions useful in a big skill [O3]: `$ARGUMENTS`, `$0`/`$1`, `${CLAUDE_SKILL_DIR}` (the folder holding SKILL.md, so script paths work at personal, project or plugin level), and `` !`command` `` dynamic context, which runs before Claude sees the skill (a non zero exit aborts the whole invocation, so append `|| true` where failure is normal).

## 4. The description: how triggering works and how to write one that fires

### How triggering works

- The description is the router. Claude sees every skill's name and description and picks from "potentially 100+ available Skills" on that text alone [O1]. "The `description` is what Claude matches your request against" [O2].
- Claude "only consults skills for tasks it can't easily handle on its own": simple one step requests may not trigger a skill "even if the description matches perfectly". Complex, multi step or specialized requests trigger reliably [O6 skill-creator].
- Claude tends to undertrigger. skill-creator's advice: make descriptions "a little bit 'pushy'", e.g. add "Make sure to use this skill whenever the user mentions dashboards, data visualization, internal metrics ... even if they don't explicitly ask for a 'dashboard.'" [O6 skill-creator].

### How to write it

- Third person, always: "Processes Excel files and generates reports", never "I can help you" or "You can use this" [O1]. The text is injected into the system prompt and a mixed point of view hurts discovery.
- Structure: `[What it does] + [When to use it] + [Key capabilities]` [O5].
- Include the words users actually say, file types, and concrete tasks [O1][O5]. "The more variations you include, the more reliably the skill fires" is the common community finding [C3].
- Put all "when to use" information in the description, not in the body. The body is only read after the skill has already triggered [O6 skill-creator].
- To stop overtriggering, add negative triggers and narrow scope, e.g. "Do NOT use for simple data exploration (use data-viz skill instead)" [O5]. In Claude Code you can also set `disable-model-invocation: true` [O3].
- Quick self test: read only the name and description and route ten realistic requests. If you cannot, Claude cannot [C3]. Or ask Claude "When would you use the X skill?" and see what it quotes back [O5].

Good official examples [O1]:

```yaml
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
```

Bad: `Helps with documents`, `Processes data`, `Does stuff with files` [O1].

### Disagreement: should the description summarize the workflow?

Anthropic says the description should say what the skill does and when [O1][O5]. obra's superpowers goes further: the description should contain only triggering conditions, start with "Use when...", stay under 500 characters if possible, and "NEVER summarize the skill's process or workflow", because in his tests an agent given a workflow summary "may follow the description instead of reading the full skill content" (a description saying "code review between tasks" made the agent do one review instead of the two stage review in the body) [C2]. Practical reconciliation: say what the skill covers (its domain and outputs), list triggers generously, and never compress the procedure into the description.

## 5. Progressive disclosure: what goes in SKILL.md and what goes in references

### Size targets

- Keep the SKILL.md body under 500 lines [O1][O3][O7]; under 5,000 tokens [O2][O7]; under 5,000 words is the outer ceiling in the PDF guide [O5]. HatchWorks translates 500 lines to roughly 1,500 to 2,000 words [C3].
- When approaching the limit, "add an additional layer of hierarchy along with clear pointers about where the model using the skill should go next" [O6 skill-creator].
- Be concise: "Claude is already very smart. Only add context Claude doesn't already have", and ask of each paragraph "does this paragraph justify its token cost?" [O1].
- If more than 20 to 50 skills are enabled at once, consider fewer skills or skill "packs" [O5].

### What belongs in SKILL.md

- The core rules that must hold on every task, at the top (they survive compaction and get read first) [O3][O5].
- The workflow: ordered steps, with decision points ("Creating new content? Follow X. Editing? Follow Y") [O1].
- A map of every reference file and when to read it [O1][O6].
- A short quality checklist Claude can copy and tick off [O1].
- "Treat the body as an index that points outward" [C3]. SKILL.md is "like a table of contents in an onboarding guide" [O1].

### What goes to references

Content that is "detailed, occasional, or mutually exclusive with another path" [C3]: API references, long recipes, per domain or per platform material, examples, schemas, research evidence. Three official patterns [O1]:

1. High level guide with references: quick start in SKILL.md, advanced features in `FORMS.md`, `REFERENCE.md`, `EXAMPLES.md`.
2. Domain specific organization: `reference/finance.md`, `reference/sales.md`, ... so a sales question never loads finance.
3. Conditional details: basic path inline, advanced paths linked ("For tracked changes: See REDLINING.md").

Variant organization (one file per framework or platform, `references/aws.md`, `gcp.md`, `azure.md`) is the skill-creator's version of pattern 2 [O6]. obra's threshold for moving something out: heavy reference of 100+ lines, or a reusable tool; keep code patterns under 50 lines inline [C2].

## 6. Linking reference files so they load on demand

- **One level deep.** Every reference file should be linked directly from SKILL.md. When a referenced file links to another file, Claude "might use commands such as `head -100` to preview content rather than reading entire files, resulting in incomplete information" [O1]. The spec says the same: "Avoid deeply nested reference chains" [O7]. This is about link chains, not directory depth: `references/platforms/web.md` is fine as long as SKILL.md links it directly (claude-api uses `{lang}/claude-api/README.md` three folders down [O6]).
- **Say when to read each file.** "Reference files clearly from SKILL.md with guidance on when to read them" [O6 skill-creator]. "Link them from SKILL.md so Claude knows when to load each" [O3]. A table of `file | what is in it | read when` works well (mgpro does this [L1]; claude-api has a "Reading Guide" and a "Quick Task Reference" keyed by task [O6]). claude-api also writes imperative routing: "**Read `shared/model-migration.md` immediately** and follow it in order" [O6].
- **Table of contents in long files.** Reference files over 100 lines get a contents list at the top, so a partial read still shows the full scope [O1] (skill-creator uses a 300 line threshold [O6]; 100 is the stricter official one).
- **Relative paths, forward slashes**, from the skill root: `references/guide.md`, never `references\guide.md` [O1][O7].
- **Greppable references.** For big reference sets, give Claude grep commands: `grep -i "revenue" reference/finance.md` [O1].
- **No `@` links to other files.** `@path` force loads the file immediately and burns context before it is needed; reference other skills by name instead [C2].
- **Watch what Claude actually opens.** Unexpected read order means the structure is not intuitive; a file Claude rereads every time probably belongs in SKILL.md; a file never opened is unnecessary or poorly signposted [O1].

## 7. Scripts vs instructions

### Degrees of freedom [O1]

- High freedom (prose heuristics) when many approaches are valid and decisions depend on context, e.g. design critique.
- Medium freedom (pseudocode, parameterized templates) when a preferred pattern exists.
- Low freedom (exact scripts, "Run exactly this script ... Do not modify the command") when operations are fragile, consistency is critical, or a sequence must be followed. The analogy: a narrow bridge with cliffs gets guardrails; an open field gets a direction.

### When to bundle a script

- Deterministic work belongs in code: sorting, validation, measurement. Code makes workflows "consistent and repeatable" [O4]. "Prefer scripts for deterministic operations" [O1]. "Code is deterministic; language interpretation isn't" [O5].
- Pre made scripts are more reliable than generated code, save tokens, save time and are consistent [O1].
- Signal from evals: if every test run writes a similar helper, bundle it in `scripts/` [O8].
- If a constraint can be checked by regex or validation, automate it and save prose for judgment calls [C2].

### How to write and reference scripts

- Say whether to run or read: "Run `analyze_form.py` to extract fields" vs "See `analyze_form.py` for the algorithm". Running is the default [O1]. Scripts that run never enter context, only their output does [O2].
- Solve, don't punt: handle errors inside the script instead of failing and leaving Claude to cope; make error messages specific ("Field 'signature_date' not found. Available fields: ...") [O1].
- No voodoo constants: justify every number in a comment [O1].
- List dependencies and do not assume packages are installed [O1]. In Claude Code, install locally, not globally [O2].
- Feedback loops: run validator, fix, repeat; "Only proceed when validation passes" [O1]. Plan, validate, execute: write a plan file, validate it with a script, then apply [O1].
- Call scripts through their interpreter (`bash scripts/x.sh`, `python3 scripts/x.py`), not by bare path, since some packagers strip the executable bit [C2]. In Claude Code use `${CLAUDE_SKILL_DIR}/scripts/...` so paths resolve wherever the skill is installed [O3].
- Visual analysis is a valid loop: render to an image, then have Claude look at it [O1].

## 8. Assets

`assets/` holds static files used in the output rather than read as instructions: templates, images, fonts, data files, lookup tables, schemas [O6 skill-creator][O7]. Examples: canvas-design ships 80+ font files with their OFL licences in `canvas-fonts/` [O6]; docx ships XML templates under `scripts/templates/` [O6]; skill-creator ships `assets/eval_review.html` [O6]. Bundle comprehensive resources freely, since they cost nothing until accessed [O1]. Keep licence files next to third party assets.

## 9. Naming files and folders

- The file must be exactly `SKILL.md`, case sensitive; `skill.md` or `SKILL.MD` are not accepted [O5].
- Folder name in kebab case, no spaces, underscores or capitals [O5]; it must equal `name` [O7].
- Skill names: gerund form recommended (`processing-pdfs`), noun phrases (`pdf-processing`) or action form (`process-pdfs`) acceptable; avoid vague (`helper`, `utils`), generic (`documents`) and reserved words, and keep one pattern across a collection [O1].
- Reference files: descriptive names that say what is inside (`form_validation_rules.md`, not `doc2.md`); organize directories by domain or feature (`reference/finance.md`, not `docs/file1.md`) [O1].
- No `README.md` inside the skill folder; documentation goes in SKILL.md or references. A repo level README for humans is fine [O5].
- For MCP tools, use fully qualified names (`ServerName:tool_name`) [O1].

## 10. Writing style inside a skill

- Explain the why rather than piling up MUSTs: "Today's LLMs are smart ... explain the why behind everything" [O6 skill-creator]; reasoning based instructions ("Do X because Y tends to cause Z") beat rigid ALWAYS/NEVER lists [O8]. The PDF guide still recommends `## Critical` headers and specific, checkable rules for the few things that must never slip [O5].
- One term per concept, used consistently ("field", never also "box" or "element") [O1].
- No time sensitive text ("before August 2025 use..."); put legacy material in an "Old patterns" section [O1].
- Give a default with an escape hatch instead of a menu of options ("Use pdfplumber. For scanned PDFs use pdf2image with pytesseract") [O1].
- Concrete input and output examples convey style better than description [O1]. obra: one complete, well commented example beats several ports [C2].
- Templates: strict ("ALWAYS use this exact template") where the format must hold, flexible ("a sensible default, adapt as needed") elsewhere [O1].
- Checklists for long workflows that Claude copies and ticks off [O1].
- A rule that must hold every single time (e.g. "never write a literal font size") is better enforced by a hook than by prose: Claude Code runs hooks on every event whether or not Claude is still following the skill, and hooks can live in the skill's own `hooks` frontmatter [O3]. For judgment guidance, word it to cover the whole task ("run the tests after every edit") because the skill is not re-read [O3].

## 11. Evaluation and testing

### Build evals first [O1]

1. Run Claude on representative tasks without the skill and record the failures.
2. Write three scenarios that test those gaps.
3. Measure the baseline without the skill.
4. Write the minimum instructions that pass.
5. Iterate against the baseline.

"Create evaluations BEFORE writing extensive documentation" so the skill solves real problems, not imagined ones [O1]. obra's stricter form: "NO SKILL WITHOUT A FAILING TEST FIRST", including edits; watch an agent fail without the skill (RED), write the minimum that fixes it (GREEN), close loopholes (REFACTOR) [C2]. The engineering blog: "Start with evaluation" [O4].

### Output quality evals [O8][O6 skill-creator]

- `evals/evals.json` with `prompt`, `expected_output`, optional `files`, and later `assertions`. Start with 2 to 3 realistic prompts (real paths, casual phrasing, at least one edge case).
- Run each case with the skill and without it (or against a snapshot of the old version), each in a clean context (a fresh subagent per run).
- Record tokens and duration per run (`timing.json`), grade assertions with quoted evidence (`grading.json`), aggregate pass rate, time and tokens with deltas (`benchmark.json`).
- Drop assertions that pass in both configurations (they measure nothing); investigate ones that fail in both; study the ones that pass only with the skill.
- Human review catches what assertions cannot (style, visual quality). Blind A/B comparison by an LLM judge helps when both versions pass every assertion.
- High variance between runs means ambiguous instructions: add examples or tighten wording [O8]. obra: "Variance is a metric" [C2].
- If pass rates plateau while rules keep growing, the skill may be over constrained; try removing instructions [O8].

### Trigger evals [O6 skill-creator][O5]

- About 20 queries: 8 to 10 should trigger, 8 to 10 should not. The negatives must be near misses that share keywords but need something else, not obviously unrelated tasks.
- Queries must be realistic and detailed (paths, backstory, typos), never "Format this data".
- skill-creator's `run_loop.py` splits 60% train, 40% held out test, runs each query 3 times for a stable trigger rate, and proposes better descriptions.
- Target from the PDF guide: triggers on about 90% of relevant queries, measured with 10 to 20 test queries [O5].
- In Claude Code: `/skill-doctor` reports each skill's context cost and flags never invoked skills; plugin skills can use `claude plugin eval` with a `tool_used: Skill` grader; `claude plugin validate ~/.claude/skills` finds frontmatter that does not parse [O3]. The open spec offers `skills-ref validate ./my-skill` [O7].

### Claude A / Claude B [O1]

One Claude instance (A) helps write and refine the skill; fresh instances (B) use it on real tasks. Observe B, bring specifics back to A ("it forgot to filter test accounts even though the skill mentions it"), apply, retest. Test with every model you will run the skill on: Haiku may need more detail, Opus may be over explained [O1].

## 12. Common mistakes

| Mistake | Why it hurts | Source |
|---|---|---|
| Vague or short description | Skill never triggers; the agent improvises | [O1][C3] |
| Description in first or second person | Discovery problems, text is in the system prompt | [O1] |
| Workflow summarized in the description | Agent follows the summary and skips the body | [C2] |
| "When to use" written only in the body | The body is read after triggering, too late | [O6] |
| Bloated SKILL.md (everything inline) | Every token paid on every turn; rules buried; partly lost after compaction | [O3][O5][C3] |
| Critical rules at the bottom | Read last, cut by compaction | [O3][O5] |
| Reference chains (A links B links C) | Partial reads with `head`, missing information | [O1] |
| Long reference files without contents | Claude previews and misses sections | [O1] |
| References not signposted with "read when" | Never opened, or opened at the wrong time | [O1][O3] |
| `@` links between files | Force loads everything up front | [C2] |
| Explaining what Claude already knows | Wasted tokens | [O1] |
| Too many options with no default | Indecision, inconsistent output | [O1] |
| Inconsistent terminology | Misparsed instructions | [O1] |
| Time sensitive statements | Become wrong silently | [O1] |
| Asking Claude to generate deterministic code each time | Unreliable and expensive; use a bundled script | [O1][O4] |
| Scripts that fail and punt to Claude, magic numbers | Fragile runs | [O1] |
| Backslash paths, bare script paths | Break on Unix or after packaging | [O1][C2] |
| No evals, no baseline | You cannot tell if the skill helps | [O1][O8] |
| Skill that pretends to look up live data | "Confident guesses rather than facts"; use a tool or MCP | [C3] |
| Same expertise copied into several agents' prompts | Copies drift; put it in one skill | [C3] |
| Installing untrusted skills unaudited | Skills can run code and exfiltrate data | [O2][O4] |

## 13. What the big Anthropic skills actually look like

Measured from the repo tree on 2026-10-27 [O6]:

| Skill | Files | SKILL.md | Layout |
|---|---|---|---|
| claude-api | 96 | 616 lines (105 KB) | Router SKILL.md with a subcommand table, "Reading Guide" and "Quick Task Reference"; per language folders (`python/claude-api/README.md`, `tool-use.md`, `streaming.md`...), `shared/` for cross language topics (`models.md`, `prompt-caching.md`, `evals/build-eval.md`...), `curl/`. Note: it exceeds its own 500 line advice |
| canvas-design | 83 | 129 lines | Short SKILL.md, `canvas-fonts/` assets with licences |
| docx, pptx, xlsx | 53 to 61 | 91 to 238 lines | SKILL.md plus large `scripts/` (validators, helpers, `soffice.py`, XML templates, schemas). Code does the fragile work |
| skill-creator | 18 | 485 lines | `agents/` (grader, comparator, analyzer prompts for subagents), `scripts/` (run_eval, run_loop, improve_description, package_skill, quick_validate), `references/schemas.md`, `assets/eval_review.html`, `eval-viewer/` |
| mcp-builder | 10 | 236 lines | `reference/` (best practices, Python server, Node server, evaluation), `scripts/` |
| pdf | 12 | 314 lines | `forms.md` and `reference.md` beside SKILL.md, 8 scripts |
| frontend-design | 2 | 71 lines | Single short file |

Patterns worth copying: the router table keyed by task (claude-api), subagent prompts kept as separate files and handed to subagents (skill-creator `agents/`), validators as scripts (office skills), domain folders with one file per variant (claude-api languages, mcp-builder servers).

## 14. What the local skills teach

### mgpro [L1], a good router

- SKILL.md is 113 lines but about 4,100 words (about 6,200 tokens), because each line is a long paragraph. It is under 500 lines yet above the 5k token guidance [O2]. Line count is not the only budget; watch tokens.
- Strong structure: description with explicit "Use when ..." triggers (743 characters); a "Read what you need" table of 22 reference files and folders with what each holds, bold marking the ones to start with; a 14 step workflow that names which reference each step needs; golden rules; a copyable quality checklist.
- Supporting folders by kind: `references/` (topic files), `templates/kit/` (reusable code) and `templates/examples/` (whole prior projects to read, "never copy"), `sfx/` (a catalog plus analysis), `music/registry.json` (data that grows with each film).
- Lessons live in `references/lessons.md` and research evidence in `references/research.md` / `sound-research.md`, separate from the rules that cite them.
- Gaps against the rules: reference files of 239 to 530 lines open without a Contents list [O1]; a few cross references between reference files (sound.md points to music.md) approach chained linking.

### design-taste-frontend [L2], the anti pattern for size

- One SKILL.md of 1,206 lines, about 12,900 words (about 21,800 tokens), no other files. Every trigger loads all of it and keeps it for the rest of the session, about four times the 5k token guidance [O2], and after compaction only its first 5,000 tokens come back [O3].
- Its description (269 characters) says what it does but has no "Use when" trigger list, file types or user phrases [O1][O5].
- The content itself is useful; it simply belongs in topic references behind a router.

## 15. Recommended layout for kwx-designer (router SKILL.md)

The existing folders (`principles/`, `visual/`, `patterns/`, `platforms/{desktop,web,mobile}`, `icons/`, `editors/`, `premium/`, `psychology/`, `quality/`, `workflow/`, `scripts/`, `assets/`, `sources/`) already follow the domain organization pattern [O1]. The rules from sections 5 and 6 decide how SKILL.md links them.

```
kwx-designer/
  SKILL.md                      # router, under 300 lines and under 5k tokens
  workflow/
    intake.md                   # questions to ask, when to skip asking
    process.md                  # brief -> direction -> build -> review, step by step
    review.md                   # the review pass, how to judge a finished screen
  principles/
    hierarchy.md  layout-grid.md  spacing.md  typography.md  color.md  motion.md
  visual/
    style-directions.md         # named looks with when to use each
    depth-and-material.md       # shadow, glass, borders
  patterns/
    navigation.md  forms.md  data-display.md  empty-and-error-states.md  onboarding.md
  platforms/
    web/README.md               # web rules and how they differ
    desktop/README.md           # desktop (Quickshell, Iris, native apps)
    mobile/README.md            # Android and iOS rules, touch targets, safe areas
  icons/
    icon-system.md              # choosing, sizing, drawing missing icons
  editors/
    figma.md  code-first.md     # tool specific how to
  premium/
    what-reads-as-premium.md    # the details that separate premium from template
  psychology/
    perception-and-attention.md # Gestalt, Fitts, Hick, cognitive load, with sources
  quality/
    checklist.md                # the full pre ship checklist
    anti-slop.md                # templated defaults to avoid
    mistakes.md                 # lessons from defects the user reported
  scripts/
    contrast_check.py           # WCAG contrast from two colours (run, not read)
    type_scale.py               # generate a modular scale
    lint_tokens.py              # flag literal sizes and colours in code
  assets/
    templates/                  # starter files to copy into an output
    tokens/                     # base token sets (JSON or CSS)
  evals/
    evals.json                  # 3+ output cases with assertions
    triggers.json               # ~20 should / should not trigger queries
  sources/                      # raw research: books, videos, articles, reports
    articles/  books/  videos/  research_notes/  reports/
```

### The router SKILL.md

```markdown
---
name: kwx-designer
description: Designs and reviews interfaces for web, desktop and mobile: layout, type, colour, spacing, motion, icons, components and whole screens, aiming for a premium, non template look. Use when the user asks to design, redesign, polish or critique a UI, screen, landing page, app, dashboard, component or icon, picks between visual directions, or says a UI looks cheap, generic or off, even if they do not say "design".
---

# kwx-designer

## Critical rules (always apply)
5 to 10 rules that hold on every task, each with its reason. These come first
because they are read first and survive compaction.

## Workflow
1. Intake: read `workflow/intake.md` ...
2. Pick the platform file: web, desktop or mobile (table below).
3. Direction, build, review: `workflow/process.md`, then `workflow/review.md`.
Copyable checklist of the steps.

## Read what you need
| File | What is in it | Read when |
|---|---|---|
| `principles/typography.md` | scale, pairing, line length | choosing or fixing type |
| `platforms/mobile/README.md` | touch targets, safe areas | the output runs on a phone |
| ... every reference file, each linked directly from here ... |

## Scripts
Run, do not read: `python3 ${CLAUDE_SKILL_DIR}/scripts/contrast_check.py <fg> <bg>`.

## Before you finish
Short checklist; the full one is `quality/checklist.md`.
```

### Rules for this layout

1. Every reference file is linked from the SKILL.md table with a "read when" column. No reference file depends on another reference file to make sense [O1][O7]. Folder depth is fine; link depth is one.
2. Every reference file over 100 lines opens with a Contents list [O1].
3. One topic per file, small enough that a task loads only what it needs [O7]. Platform specific rules live only in `platforms/`, so a mobile task never loads web rules [O1].
4. `sources/` is research input, not runtime material. SKILL.md does not route to it for normal tasks; references distill it and cite it (as mgpro keeps `research.md` apart from its rules [L1]). Link it from SKILL.md only for explicit "show me the evidence" requests.
5. Anything mechanical (contrast, scales, token lint) is a script that is run, with specific error messages [O1][C2].
6. `quality/mistakes.md` grows with every defect the user reports, like mgpro's `lessons.md` [L1].
7. Write the evals before filling the references, run with and without the skill, and tune the description with the trigger set until it fires on about 90% of relevant prompts and stays quiet on near misses [O1][O5][O6].
8. Keep the SKILL.md body under 500 lines and, more importantly here, under about 5k tokens: long one line paragraphs count [O2][L1].
