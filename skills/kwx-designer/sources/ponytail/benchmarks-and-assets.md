# Ponytail benchmarks and README visuals: lessons for kwx-designer

Slice: `benchmarks/**` and the English images in `assets/` of the ponytail plugin
(P = ~/.claude/plugins/cache/ponytail/ponytail/5.1.0). Read 2026-10-29.

## Files read

Benchmarks (all read in full except `agentic/tasks.py`, which was read for its structure, every
task prompt, the safety, quality, scope and convention tiers, the conv-ui task in full and the QUICK set):

- `benchmarks/README.md`, `.env.example`
- `benchmarks/promptfooconfig.yaml`, `promptfooconfig.gemini.yaml`, `promptfooconfig.gpt-newest.yaml`
- `benchmarks/behavior.yaml`, `behavior.js`, `loc.js`, `correctness.js`
- `benchmarks/arms/baseline.js`, `caveman.js`, `ponytail.js`, `caveman-SKILL.md`
- `benchmarks/agentic/README.md`, `run.py`, `tasks.py`, `judge.py`, `complete.py`, `answer.py`, `compare.py`
- `benchmarks/results/2026-06-12-caveman-vs-ponytail.md`
- `benchmarks/results/2026-06-12-v4-hardening-vs-caveman.md`
- `benchmarks/results/2026-06-15-llama3.2-local.md`
- `benchmarks/results/2026-06-16-correctness-gate-fix.md`
- `benchmarks/results/2026-06-16-robustness-audit.md`
- `benchmarks/results/2026-06-17-agentic-safety.md` (superseded)
- `benchmarks/results/2026-06-17-cost-verification.md`
- `benchmarks/results/2026-06-18-agentic.md`
- `benchmarks/results/2026-06-22-issue-245-217-comprehension.md`
- `benchmarks/results/2026-10-07-agentic.md`

Assets (English only; the -es, -ja, -ko, -zh-CN files are the same layouts translated):

- `assets/v5/hero.jpg`, `ladder.png`, `beforeafter.png`, `chart.png`, `review.png`, `audit.png`, `tests.png`
- `assets/benchmark-3model.svg`, `assets/benchmark-agentic.svg`
- `assets/logo.png`, `logo-dark.svg` (header only), `logo-greenpt.svg`, `retriever-logo-light.svg`
  and `-dark.svg` (sponsor logos, header and text only), `assets/waitlist-banner.png`

## Key numbers (for context)

- Ponytail 5, Opus 5.5, 39 tasks x 5 runs x 3 arms (585 sessions): vs no skill, lines -53% [-63..-41],
  gzip code -41%, output tokens -45%, cost -26%, time -41%, cheaper on 30 of 38 tasks. Hidden checks
  passed 96.7% vs 95.6% (no change in quality, only in size). Tests where logic needs one: 98% vs 68%.
  Injected bugs caught by the agent's own tests: 66% vs 46%. Tests where none was needed: 45% vs 36%.
- Reply judge: Ponytail 5 beat v4.13 110:67 (p=0.002); vs no skill 82:106 (p=0.09, not significant).
- Real repo, Haiku: date picker 404 to 23 lines (native `<input type="date">`), color picker 287 to 23,
  dropzone 251 to 95; backend CRUD essentially tied. Safety 100% vs the bare "YAGNI + one-liner"
  prompt at 95%: the lines it cut were the path-traversal guard.
- Single-shot numbers (80 to 94% less code) were later conceded as inflated by a chatty baseline.
- Contaminated run: a SessionStart hook fired on every arm, the gap collapsed to 4%, nearly published.
- Robustness: 8 SKILL.md edits to fix an OpenAI email slip all scored at or below the current skill
  (n=100: 96% vs 95%); nothing shipped.
- Root-cause fix (#245): baseline 1/6, prose rule ("trace the flow end to end") 0/3, operational rule
  ("grep every caller, fix the shared function once") 6/6 on Sonnet and Opus. Haiku 0/6 in both arms.
- Review skill (from the image): 100% of planted problems found vs 87% without; 100% of problems
  outside the diff found vs 78%.

## Lessons

Status: COVERED (file:line in kwx-designer), PARTIAL (what is missing), NEW. Paths in "Source" are
relative to P. "Home" is the suggested place in kwx-designer for NEW and PARTIAL items.

### A. How to measure whether a skill works (eval method)

| id | Lesson (imperative) | Source | Status | Home and reason |
|---|---|---|---|---|
| B01 | Always run a no-skill arm with the same agent, same harness and same tasks. The fair baseline is the real agent doing the job, not a bare chat model that answers with menus and prose. | agentic/README.md, results/2026-06-18-agentic.md | NEW | new `evals/README.md`: kwx has assertions but no baseline, so it cannot show the skill changes anything. |
| B02 | Add a "short prompt" control arm with the cheapest instruction that might do the same job (ponytail used "Follow YAGNI principles, and prefer one-liner solutions."). For kwx: "Make it look premium and avoid generic AI design." If seven words match the skill, the skill is not worth its tokens. | agentic/run.py ARMS, results/2026-06-18-agentic.md | NEW | `evals/README.md`: the only way to prove the router and 70 files beat one sentence. |
| B03 | Add a "surface trait" control (caveman: terse talk only) to separate the skill's real discipline from a side effect. For kwx: a generic frontend design prompt or another public design skill. Caveman landed between baseline and ponytail, so terseness explained part of the gap, not most. | results/2026-06-18-agentic.md finding 3 | NEW | `evals/README.md`: tells which part of kwx is doing the work. |
| B04 | Isolate arms so nothing leaks into the baseline: exclude global plugins and settings (`--setting-sources project,local`), load exactly one skill per arm, set `CLAUDE_CODE_DISABLE_CLAUDE_MDS=1` and `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`, and read one finished transcript per arm to prove what was injected. This user's global CLAUDE.md already carries design rules (no em dashes, no emoji icons, UiScale, the ui-designer agent), so an unisolated baseline is secretly half kwx. | results/2026-06-17-agentic-safety.md banner, 2026-06-18-agentic.md, run.py run_cell | NEW | `evals/README.md`: the contamination bug nearly published a false result. |
| B05 | Run every cell in a fresh temp folder outside any git repo, then move it into the run folder. Inside a repo Claude Code shows recent commit messages, which leak the answer. | results/2026-10-07-agentic.md setup, run.py main | NEW | `evals/README.md` |
| B06 | Test the skill as it is really loaded, not pasted as a system prompt. Ponytail: "--append of the SKILL text does NOT activate them"; independent runs that pasted SKILL.md were excluded. For kwx: copy the skill into the workspace `.claude/skills/kwx-designer` (project source) and check the transcript that the Skill tool fired. | run.py run_cell comment, README.md independent benchmarks | NEW | `evals/README.md`: triggering is part of what is tested. |
| B07 | Measure triggering separately from quality: a trigger set (should and should not) and a quality set where the skill is known to be loaded. | promptfoo vs agentic split; kwx evals/triggers.json | COVERED evals/triggers.json (should_trigger, should_not_trigger) | Keep; add a trigger rate number to the eval report. |
| B08 | Give every scorer a `good` and a `bad` reference and run a selftest before any paid call: good must pass, bad must be caught on its declared axis. Refuse to run if any instrument is broken. | run.py selftest, tasks.py docstring | NEW | `evals/README.md` + a `evals/run.py --selftest`: kwx scripts (contrast_check, icon_check) have no proof they catch a bad case. |
| B09 | Make the bad reference lazy but plausible: right on the happy path, wrong only on the corner the rule is about. For UI: a list that renders fine with data but has no empty or error branch; a delete that uses `window.confirm` when the app has a house dialog; a hex literal instead of a token; `outline: none` with no focus style. | tasks.py header, safety tier | NEW | `evals/README.md`: a crude bad ref tests nothing. |
| B10 | Keep the requirement implicit in the prompt, the way a real ticket reads ("untrusted", "abusive clients", "real exports with malformed rows"), then check it anyway. For UI: "Add a workouts list" (empty state never mentioned), "show the user's name in the header" with a 40 character name in the fixture. | tasks.py prompts, agentic/README.md | NEW | `evals/evals.json`: today's assertions mostly restate the prompt. |
| B11 | Seed a starter file or a small real project the agent must edit, so an agent that narrates "done" without writing fails honestly. Track a "wrote a file" rate. | tasks.py docstring, run.py aggregate wrote_file_rate | NEW | `evals/README.md`: Haiku sometimes narrated a full solution and left the file unwritten. |
| B12 | Run a share of tasks inside a real public repo pinned to a commit, so the agent faces real conventions and real over-build temptation. | results/2026-06-18-agentic.md setup | NEW | `evals/README.md`: kwx's own projects (Grit, Koima) or a pinned open source app would do. |
| B13 | Pair every "less" metric with a completeness gate (0 stub, 1 partial, 2 one requirement missing, 3 full). Less that also does less is caught, not rewarded. | agentic/complete.py | NEW | `evals/README.md`: restraint scores must not reward a screen that dropped the feature. |
| B14 | Make every LLM judge auditable: fixed model, temperature 0 where possible, published rubric, JSON only, and every score must cite the construct it penalises (or "none"). Store the rubric with the scores. | agentic/judge.py RUBRIC, run | NEW | `quality/scoring-rubric.md` could add a "cite the element" rule; `evals/README.md` for the judge. |
| B15 | Validate each judge before trusting it: it must rank a deliberately bad reference strictly below the good one for the same task, or the run refuses to judge. Also test the gate logic offline with fake scores (a well ordered matrix passes, an inverted one is flagged) so the gate can never become a no-op. | judge.py selftest, complete.py selftest_offline | NEW | `evals/README.md`: a "premium" judge that cannot tell slop from good is noise. |
| B16 | For pairwise judging, shuffle the order per pair with a seed, require the good reference to win in both slots during selftest (position bias), drop ties, and use a sign test over pairs. | answer.py selftest_pair, pairwise | NEW | `evals/README.md`: the natural design comparison is "which screen is better", which is pairwise. |
| B17 | Judge the reply the user reads in two calls: a blind reader that sees only the task and the reply and writes what it now believes (changed, left out, must do, watch out), then a grader that compares those beliefs with the real diff on accuracy, coverage and clarity. Report length, never score it. | agentic/answer.py | NEW | `evals/README.md`: kwx's final report (quality-gate.md section 13) is never tested for whether a reader learns the truth from it. |
| B18 | Gate the reply judge with four fixed replies about one diff: good must beat terse on coverage, beat a reply with one false claim on accuracy, beat a padded essay on clarity. | answer.py GOOD/TERSE/ESSAY/FALSE, GATE | NEW | `evals/README.md`: ready made selftest design to copy. |
| B19 | Use several runs per cell (5 minimum; 10 to 30 for single shot) and report medians, not single runs. n=1 timings are noise; llama3.2 flipped sign between n=3 and n=5. | results/2026-06-12-caveman-vs-ponytail.md, 2026-06-15-llama3.2-local.md | NEW | `evals/README.md` |
| B20 | Aggregate honestly: per task median, divide arm by baseline, geometric mean of the ratios over tasks, 95% bootstrap interval, and "better on X of Y tasks" with a sign test. | results/2026-10-07-agentic.md statistics, compare.py | NEW | `evals/README.md` |
| B21 | Interleave all arms task by task in one run, so time of day and model drift hit every arm the same way. | results/2026-10-07-agentic.md | NEW | `evals/README.md` |
| B22 | Keep every workspace; when a metric or scorer changes, rescore offline. Never pay the API twice for a measurement tweak. | run.py --rescore | NEW | `evals/README.md` |
| B23 | Warm the prompt cache with one throwaway call before a parallel pool; the first cold cells otherwise cost 3x and look like an arm effect. | run.py warm_cache | NEW | `evals/README.md` |
| B24 | Give every cell a timeout and kill only that cell's process tree; record killed cells and say how many in the report. | run.py _tree_kill, CELL_TIMEOUT; results/2026-06-18-agentic.md limitations | NEW | `evals/README.md` (harness hygiene). |
| B25 | Keep a quick set with one task per known failure mode, run only the candidate on it, and compare against a full run's reference arms. Re-pick it when the failure modes move. | tasks.py QUICK, compare.py | NEW | `evals/README.md`: cheap iteration on kwx rule edits. |
| B26 | Every rule change must beat the current version in a paired run, one change at a time, before it ships. | results/2026-10-07-agentic.md intro | NEW | `evals/README.md` + SKILL.md maintainers note: kwx has grown by adding text, never by proving it. |
| B27 | Write behaviour probes per critical rule, one prompt that only the rule would change, with a heuristic grader. The baseline should mostly fail and the skill pass; the delta is the point. Prove the grader itself RED/GREEN without an API key. | behavior.yaml, behavior.js | NEW | `evals/evals.json`: one probe per critical rule in SKILL.md (10 rules). |
| B28 | A grader must demand actionable evidence, not a passing mention: "a passing mention of calibration is not enough; it must be actionable". For UI: the word "empty" in a comment is not an empty state; a rendered branch is. | behavior.js hardware check | NEW | `evals/README.md` |
| B29 | When the skill looks worse, suspect the grader first. Ponytail's "correctness drop" was the gate: it could not read unfenced code (41 of 74 failures) and tested a deliverable the prompt never asked for (31 of 74), which punished the literal minimal answer. | results/2026-06-16-correctness-gate-fix.md | NEW | `evals/README.md`: check graders against the prompt's literal deliverable. |
| B30 | Never count tests, self checks or accessibility markup as bloat. Split an in-file self check off and count it as test. For UI: ARIA, focus styles, reduced motion and state branches are not "extra code". | run.py _selfcheck_split, code_stats | NEW | `evals/README.md`: otherwise a size metric punishes the quality gate. |
| B31 | Measure information content (gzip size of the delivered code) next to line count, so packing code into one line cannot game the metric. | run.py gz, results/2026-10-07-agentic.md | NEW | `evals/README.md` |
| B32 | Report cost per pass (all spend over the cells that passed every gate), not only cost per run. | run.py aggregate cost_per_pass | NEW | `evals/README.md` |
| B33 | Check whether the agent's own checks are worth anything with mutation testing: inject small bugs (flipped comparison, dropped `if`, off by one) into its finished code and count how many its own tests catch. For kwx: inject UI defects (remove focus ring, drop the error branch, lower a contrast pair, add an emoji icon, hard-code a size) into the agent's finished screen, then run the agent's quality gate or critique on it and count catches. | results/2026-10-07-agentic.md tests, assets/v5/tests.png | NEW | `evals/README.md` + `quality/quality-gate.md` self test: proves the gate catches what it claims. |
| B34 | Measure review skill with planted problems, including problems outside the diff (a caller the diff broke). Report recall for both. | assets/v5/review.png | NEW | `evals/README.md` for critique mode; `quality/critique-method.md` should say to look at screens that consume a changed component. |
| B35 | Decide before the run which tasks need the behaviour (22 need a test, 11 do not, 6 count for neither), then measure both under use and over use ("a test where none was needed"). | results/2026-10-07-agentic.md tests | NEW | `evals/README.md`: for kwx, which tasks need custom icons, which need a native control, so over-design is counted too. |
| B36 | Run correctness checks only where they really run the code; say plainly which checks are structural only and do not count "it compiles" as quality. | README.md metrics note, correctness.js header, 2026-10-07 results | NEW | `evals/README.md`: most kwx checks will be static (no browser allowed on this machine), so label them as such. |
| B37 | Split tasks into tiers by what they can show: over-build room (open features), surgical room (one function with a hidden check), scope (the change must reach wiring and tests), convention (keep the house structure), open "build me" and "show me" requests. | agentic/README.md, tasks.py tier headers | NEW | `evals/evals.json`: kwx tasks are three unrelated prompts today. |
| B38 | Design reproducers that discriminate: hide the reusable helper in a separate module the agent must find, give it a distinctive behaviour so a re-implementation diverges observably; route the named symptom and an un-named sibling through one shared function and test the sibling. An earlier in-file version had every arm tie. | tasks.py quality tier header, results/2026-06-22 | NEW | `evals/README.md`: for UI, put the house ConfirmDialog or token file in another folder with a distinctive look. |
| B39 | Add an extension phase: after the build, send a surprise follow-up ("add a third plan", "add dark mode") and measure lines changed and files touched. Good structure makes the extension cheap (ponytail 41 and 55 lines vs 156 and 257). | results/2026-06-12-v4-hardening-vs-caveman.md | NEW | `evals/README.md`: tests kwx rule 4 (a system, not a screen) directly. |
| B40 | Write the acceptance criteria before the run and grade the result against them line by line. | results/2026-06-12-v4-hardening-vs-caveman.md acceptance criteria | NEW | `evals/README.md` |
| B41 | Make the benchmark able to disprove the skill: show where it does not win (backend CRUD tied), publish null results (nobody over-built on scoped tasks), and give a limitations section in every report. | results/2026-06-18-agentic.md, 2026-06-17 finding 3 | NEW | `evals/README.md` report template. |
| B42 | When a result turns out wrong, keep it with a "superseded" banner that names the bug and links the new run; never silently delete it. | results/2026-06-17-agentic-safety.md | NEW | `evals/README.md` |
| B43 | Report per model and do not claim beyond the models tested. Weak models (llama3.2, Haiku on multi-step rules) absorb rules partially, pay the token cost and get no gain; when the baseline also fails it is a model ceiling, not a regression. | results/2026-06-15-llama3.2-local.md, 2026-06-22 Haiku section | NEW | `evals/README.md` |
| B44 | Cost claims depend on the workload and provider; measure them, and print where the skill costs more (OpenAI reasoning models paid 26 to 39% more for the always-on ruleset). | results/2026-06-17-cost-verification.md, README independent benchmarks | NEW | `evals/README.md`: kwx is large; on a tiny UI fix its reading cost may exceed its value. |
| B45 | Watch for provider artifacts in telemetry (OpenAI auto caching zeroed cost on repeated prompts; a free tier quota polluted a run) and exclude or redo those runs rather than average them in. | results/2026-06-17-cost-verification.md | NEW | `evals/README.md` |
| B46 | Run checks serially or with headroom when quota errors could shrink denominators; report dropped cells. | results/2026-06-16 method, 2026-06-17 notes | NEW | `evals/README.md` |
| B47 | Give every arm the same extra instruction when the harness needs one (ponytail's NO_RUN: write code, do not run servers or browsers), so the constraint is not an arm effect. | run.py NO_RUN | NEW | `evals/README.md`: kwx evals must also forbid browsers, per the user's rules, for every arm. |

### B. How to build, enforce and word the skill itself

| id | Lesson (imperative) | Source | Status | Home and reason |
|---|---|---|---|---|
| B48 | Do not ship rule text that does not move the measured number. Eight careful edits to fix one slip all scored at or below the current skill, several far worse, all longer output. Adding text that does not work is cargo cult. | results/2026-06-16-robustness-audit.md | NEW | SKILL.md maintainers note: kwx keeps growing from videos and books with no test of effect. |
| B49 | Counter-instructions backfire: piling extra validation rules onto a skill made models overthink and fail more. Prefer one clear rule to three overlapping ones. | results/2026-06-16-robustness-audit.md | NEW | SKILL.md maintainers note |
| B50 | Write rules as operations, not as attitudes. "Trace the flow end to end" changed nothing (0/3); "grep every caller of the function you touch and fix the shared function once" went to 6/6. For kwx: "read every screen that imports the component you change" beats "think about consistency". | results/2026-06-22-issue-245-217-comprehension.md | PARTIAL quality/quality-gate.md:28 lists every screen and state, but most SKILL.md rules are attitudes ("Intuitive beats clever") | SKILL.md critical rules: attach one operational check to each rule. |
| B51 | Frame the right behaviour as the cheaper option, so the skill's own instinct pulls toward it ("one guard in the shared function is a smaller diff than one per caller"). | results/2026-06-22 "The fix" | NEW | SKILL.md: e.g. "one token edit is smaller than ten local overrides". |
| B52 | Keep the skill file short; its read cost is a tax on every trivial task (ponytail cut SKILL.md 115 to 95 lines, "the minimalism skill should not be 2x caveman's length"; a 3.6k token floor tax on trivial tasks). | results/2026-06-12-caveman-vs-ponytail.md v3 | NEW | SKILL.md: measure the tokens kwx reads on a one-line UI fix and cap them. |
| B53 | Cap the explanation: v1 wrote tiny code then long "skipped on purpose" essays and the prose ate the savings. "If the explanation is longer than the code, delete the explanation." | results/2026-06-12-caveman-vs-ponytail.md v1 findings, v2 changes | NEW | SKILL.md "Before you finish": a reply length rule for kwx's report. |
| B54 | End the reply with what was skipped or not checked and the risks a reviewer must know; the blind judge preferred Ponytail 5 mainly for this. | results/2026-10-07-agentic.md replies | COVERED quality/quality-gate.md:193 ("Not checked and why") | Also put it in SKILL.md "Before you finish" so it reaches replies that skip the full gate. |
| B55 | A good reply is plain, scannable, true to the diff and names every behaviour change, removal, missing part and user action; it is neither a padded essay nor cryptic fragments, arrows or abbreviations. | answer.py GRADER and GOOD/ESSAY/TERSE | PARTIAL quality/quality-gate.md:183 gives a report format but no clarity rules for the reply | SKILL.md or `quality/quality-gate.md` section 13. |
| B56 | Ship and question: never stall on "do you need X?"; build the smallest version that does the core job and say in one line what was skipped and when to add it. | results/2026-06-12 v2 changes ("ship-and-question rule") | NEW | `workflow/design-process.md` step 1: kwx's brief step can turn into a questionnaire. |
| B57 | Make the decision ladder a reflex, not a deliberation; v1 lost time deliberating what not to build. | results/2026-06-12 v2 changes | NEW | SKILL.md workflow note: do not narrate the checklist. |
| B58 | A shortcut with a known limit carries a code comment naming the limit and the upgrade path, so the trade-off lives in the code where a later reviewer sees it, not only in the chat. Example in beforeafter.png: "native date input (value is YYYY-MM-DD); swap for react-day-picker + popover if a custom calendar UI is needed". | results/2026-06-12-v4-hardening (5.2, reviewability), assets/v5/beforeafter.png | NEW | `workflow/design-process.md` build step: when kwx picks a native control or a simple state, it leaves the upgrade comment. |
| B59 | Between two options of the same size, take the one that is correct on edge cases (parse is not validate: `parseaddr` accepted "@missing-local.com"; `re.match` anchors only the start, `fullmatch` does not let a newline through). | results/2026-06-16 both, tasks.py critic-email | NEW | `patterns/forms-and-inputs.md`: validation must anchor the full value. |
| B60 | An over-built interface breaks callers: unconstrained Sonnet returned a `{is_valid, message}` dict instead of a bool, so `if validate(x)` accepted everything (0/40). | results/2026-06-16-robustness-audit.md | NEW | `workflow/design-process.md` build step: component props follow what callers already expect. |
| B61 | Never trade the safety floor for size. A pure "write less" prompt was shortest and the only arm that dropped a guard (path traversal, malformed CSV row); ponytail kept it at two or three extra lines. For kwx: a "reduce, simplify" push must never remove focus states, error and empty states, labels, contrast or undo. | results/2026-06-17 finding 2, 2026-06-18 axis 2 | PARTIAL premium/restraint-and-reduction.md "Remove what is unnecessary, not what is useful" and section 10 "When restraint goes wrong" | Add an explicit never-cut list to `premium/restraint-and-reduction.md`: accessibility, states, validation, undo, anything the user asked for. |
| B62 | Order of reach: what the codebase already has (house component), then the platform's native control, then an installed dependency, then a custom build. Big wins came exactly where a native control replaced a custom build (date picker 335 to 10 lines), and the house component beats the native widget when the app has one (conv-ui: house ConfirmDialog, not `window.confirm`). | results/2026-06-18 axis 1, tasks.py conv-ui, AGENTS.md ladder 2 and 3 | PARTIAL workflow/design-process.md:64 (build from shared components) and visual/accessibility.md:102 (native elements first) | Add the full order to `workflow/design-process.md` build step, including "native date, color and file inputs before a custom picker unless the brief needs one". |
| B63 | A change reaches every place it must: a new output format is not done until the CLI offers it; a rename must reach fixtures and tests. For UI: a new setting is not done until it is in the settings screen, persisted, read on launch and reflected in every screen that uses it. | tasks.py scope tier (scope-format, scope-rename) | PARTIAL quality/quality-gate.md:28 (list every screen and component the change touches) | Add "entry points and wiring" (nav, routes, settings, persistence) to quality-gate step 1. |
| B64 | Meet the purpose of the ticket, not its letter: "make send accept a list so the digest goes out as one message" is not done if the digest still loops, and one message to many must use Bcc so subscribers do not see each other. | tasks.py scope-recipients | NEW | `workflow/design-process.md` brief step: write the user goal in one sentence and check the result against it. |
| B65 | Keep the structure the codebase keeps on purpose (a service layer, an interface seam, a house component), even when bypassing it is shorter. | tasks.py convention tier | COVERED workflow/design-process.md:57 (use the system, extend only through its own mechanism) and :64 | None. |
| B66 | Before trusting that a rule works, show that the failure reproduces without it; the reuse rung (#217) shipped but the duplication failure never reproduced, so its value is "unproven", and the report says so. | results/2026-06-22 #217 | NEW | `evals/README.md`: tag each kwx rule as proven, unproven or untested. |

### C. What the README visuals teach about presenting a product (design work)

| id | Lesson (imperative) | Source | Status | Home and reason |
|---|---|---|---|---|
| V01 | Lead the hero with the product name, a one line claim, and three or four big signed numbers with one word labels ("-53% code", "-41% time"), rounded, relative to a named baseline. | assets/v5/hero.jpg | PARTIAL platforms/web/landing-pages.md:93 (be specific with numbers) | Add the "big signed numbers vs a named baseline" hero pattern to `platforms/web/landing-pages.md` for dev tools and B2B. |
| V02 | Answer the reader's main fear right under the headline numbers with a counter number ("And yet 98% of risky logic ships with a test. Without Ponytail: 68%."). Less code raises "is it less safe?", so the hero answers it before it is asked. | assets/v5/hero.jpg, tests.png | NEW | `platforms/web/landing-pages.md` hero section. |
| V03 | Put the method and sample size in small type under the claim ("Benchmarked on 5,700+ Claude Code sessions. Opus 5.5, 39 tasks."; chart footnote "Geometric mean of per-task medians, no skill = 100%"). | assets/v5/hero.jpg, chart.png, benchmark-3model.svg caption | PARTIAL platforms/web/landing-pages.md:102 (specific numbers with source) | Add "state n and method in a caption" to section 6. |
| V04 | Build the hero art from the product's own material: the ponytail portrait is drawn out of the real 335 line date picker code, bright where the figure is and dim elsewhere; the waitlist banner does the same. | assets/v5/hero.jpg, waitlist-banner.png | PARTIAL platforms/web/landing-pages.md:45 (real product UI as the visual) | Add to `platforms/web/landing-pages.md` section 7 as an option when the product has no screen to show (CLIs, agents, APIs). |
| V05 | Show a before and after as one card: the user's request as a quoted eyebrow, a one sentence contrast headline ("Your agent reaches for a library. Ponytail reaches for the browser."), the loser as a dim unreadable wall with a big grey count ("335 lines"), the winner in full and readable with a bright count ("10 lines"), the key token highlighted with an inline arrow label ("the browser's own date picker"), and a one line takeaway. Contrast is carried by brightness and size, not by red and green. | assets/v5/beforeafter.png | PARTIAL workflow/redesign-method.md:153 (before and after side by side with numbered changes) | Add the marketing version to `platforms/web/landing-pages.md`. |
| V06 | Explain the method as a numbered ladder: eyebrow "HOW IT WORKS", the rule as one sentence headline, one row per step with the question left and the action muted at the right, the final step highlighted with the only accent, and a footer line for the guarantees ("Validation, security and accessibility are never cut"). | assets/v5/ladder.png | NEW | `platforms/web/landing-pages.md` "how it works" section. |
| V07 | Chart for a claim: eyebrow with the method ("BENCHMARK · OPUS 5.5 · 39 TASKS x 5 RUNS"), the takeaway as the title, horizontal bars normalised to baseline = 100%, the baseline and the old version in greys, only the hero series in the brand gradient, a value label at each bar end with both share and delta ("47% · -53%"), legend, and a footnote with the statistic. | assets/v5/chart.png | COVERED visual/data-visualization.md:18 (title states the takeaway), :52 (grey everything, colour only the series the title talks about) | Optionally add "normalise to baseline = 100% for multi metric claims" to the chart file. |
| V08 | Mark the one failing number of the competitor in the semantic error colour and keep everything else neutral ("yagni-oneliner 95% (dropped a guard once)"); draw the 100% baseline as a dashed line. | assets/benchmark-agentic.svg | PARTIAL visual/data-visualization.md:52 covers highlight, not the semantic red for the single failure | `visual/data-visualization.md` highlight rules. |
| V09 | Show the product's real output as proof, in its exact format, then the number: the review card shows one real finding (severity label MUST FIX, rows WHAT THIS IS / PROBLEM / FIX / IF WE SKIP IT, the code with a "NOT IN THE DIFF" tag), then "100% of planted problems found, no skill: 87%". | assets/v5/review.png | PARTIAL platforms/web/landing-pages.md:45 (real product UI as the visual) | Add "real output, then the stat" to the landing page blueprint. |
| V10 | Write findings for humans: a ranked list with three severity levels told apart by colour weight (accent, white, grey), titles that state user impact in plain words ("Office batches with '1,200' fail completely", not the function name), a one line plain description of what the thing does with jargon glossed in parentheses, and a bold verdict naming the first fix and why ("Fix 1 first. It's a one-line move into parse_qty, and right now it breaks the office batches."). | assets/v5/audit.png, review.png | PARTIAL quality/critique-method.md:102 (lead with blockers) | Add the finding format (impact title, what, problem, fix, if we skip it) and the one line verdict to `quality/critique-method.md` output section. |
| V11 | Present a stat as a set: a huge number, the baseline directly under it in small grey ("no skill: 68%"), a label sentence, a parenthetical definition ("a branch, a loop, a parser, money, security"), and a method footnote. | assets/v5/tests.png, review.png | NEW | `platforms/web/landing-pages.md` proof section or `patterns/dashboards-and-data.md` stat tiles. |
| V12 | Use one card system across every image: the same warm near-black surface, one monospace family, the same letter-spaced eyebrow, a bold headline that is a full sentence ending in a full stop, one rounded card radius, and one gradient reserved for the brand word and the hero series only. | assets/v5 set | PARTIAL quality/quality-gate.md:99 (one accent fill per view), workflow/design-process.md:64 | Add "marketing images share one card system" to `platforms/web/landing-pages.md` section 7. |
| V13 | Ship every marketing image in each supported language with the same layout (ponytail ships es, ja, ko, zh-CN copies of all seven cards and the banner). Size boxes for the longest translation. | assets/v5/*-ja.png etc. | PARTIAL quality/critique-method.md:42 (longest realistic text, a German translation) | `platforms/web/landing-pages.md` section 7. |
| V14 | Ship logos in a light and a dark version (logo, logo-dark; sponsor logos light and dark) and pick by theme in the README. | assets/logo*.svg, retriever-logo-*.svg | PARTIAL workflow/design-system-first.md:10 (dark mode), quality-gate.md:104 | `icons/delivery.md` or the landing page media rules. |
| V15 | A distinctive hand made mark beats a generic logo: a one colour ink caricature with a ponytail and glasses is the whole brand. | assets/logo.png | PARTIAL quality/ai-slop-tells.md (generic tells) | `premium/premium-feel.md` brand note, low priority. |
| V16 | A teaser banner works with three parts: a path style eyebrow with a redacted token ("~/PONYTAIL/[REDACTED]"), a curiosity headline with a gradient block cursor, and one outlined pill CTA with an arrow ("Join the waitlist"). | assets/waitlist-banner.png | NEW | `platforms/web/landing-pages.md` (pre-launch pages), low priority. |
| V17 | Give every SVG chart a `<title>` for screen readers and a caption with the method and the reproduce command. | assets/benchmark-3model.svg, benchmark-agentic.svg | PARTIAL visual/data-visualization.md:90 (has a text alternative) | Add "caption: method, n, how to reproduce" to the chart checklist. |
| V18 | Earn trust by conceding the critic in public: a "Read this number honestly" note that says the earlier headline was inflated and links the critique, plus a table of independent benchmarks run by other people. | benchmarks/README.md | PARTIAL platforms/web/landing-pages.md:103 (every number must be true and current) | `psychology/trust-and-fluency.md`: conceded limits as a trust signal. |

## Translating the method into a kwx-designer eval suite

The kwx `evals/` folder has 10 plus 10 trigger prompts and 3 prompt-plus-assertion cases. What the
ponytail benchmark suggests, concretely (nothing below is built yet):

1. Arms: `baseline` (same agent, no skill), `kwx` (skill copied into the workspace `.claude/skills`),
   `short-prompt` ("Make it look premium and avoid generic AI design."), and optionally a public design
   skill as the surface-trait control. Every arm runs with `--setting-sources project,local`,
   `--strict-mcp-config`, `CLAUDE_CODE_DISABLE_CLAUDE_MDS=1`, `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`, in a
   temp folder outside git, Bash and browsers disabled for every arm alike. Read one transcript per arm
   to prove the skill fired only where it should (B04, B06).
2. Seeded projects, not bare prompts: a tiny React or QML app with a token file, a house
   `ConfirmDialog` and `EmptyState` in a separate folder, a fixture with a 40 character name, an empty
   list, a failing fetch (B09 to B12, B38).
3. Tiers:
   - Hidden-check tasks with the requirement implicit: "add a delete button" (house dialog used, safe
     default focus on Cancel), "add a workouts list" (empty and error branches exist), "show the user
     name in the header" (truncation or wrap styles present), "add a pricing card" (exactly one
     recommended plan, no store badge before a listing).
   - Over-design traps: "add a date picker to settings", "add a color picker" (native or house control
     before a custom build, with the upgrade comment B58).
   - Scope tasks: "add a compact mode setting" (it must reach the settings screen, persistence and
     every list), "rename Workspace to Project" (every label, no synonyms, quality-gate H5).
   - Open tasks: "build me a landing page for X", "design an onboarding" (size and slop judged, plus
     the completeness judge).
   - Critique tasks: a finished screen with planted defects, including one in a screen the diff did
     not touch; score recall (B33, B34).
4. Deterministic static scorers (no browser on this machine): regex and AST checks for emoji, em and en
   dashes, literal font sizes outside the scale, hex colours outside tokens, `outline: none` without a
   replacement, `window.confirm`, missing empty or error branches; `scripts/contrast_check.py` on every
   colour pair the code uses; `scripts/icon_check.py` on new SVGs. Each scorer ships a good and a bad
   reference and a `--selftest` that runs first (B08, B28).
5. LLM judges, each selftested before use: completeness 0 to 3 (stub must lose), over-design 0 to 3
   (a slop reference with gradient hero, repeated KPI tiles and emoji must outscore a clean one, and the
   judge must cite the element), pairwise "which screen serves the user better" with seeded order
   shuffles and a both-slots selftest, and the reader/grader reply judge (B13 to B18).
6. Behaviour probes: one prompt per critical rule in SKILL.md, where only that rule changes the
   outcome; baseline expected to fail (B27).
7. Statistics and hygiene: 5 runs per cell, medians, ratio to baseline, geometric mean with a
   bootstrap interval, sign test, arms interleaved, workspaces kept and rescored offline, cost per pass,
   token cost of the skill read on a one line fix (B19 to B25, B32, B52).
8. Process: a quick set of about 10 tasks, one per failure mode, for every rule edit; a rule change
   ships only if it beats the current kwx in a paired run; every report has a limitations section and
   says where kwx did not win (B25, B26, B41, B48).

## Counts

- NEW: 62
- PARTIAL: 18
- COVERED: 4

(84 lessons: B01 to B66 and V01 to V18. COVERED: B07, B54, B65, V07.)
