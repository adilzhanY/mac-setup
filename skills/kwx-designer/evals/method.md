# Eval method: proving the skill changes anything

How to measure whether kwx-designer, or one rule in it, makes UI work better than the same agent without it. The skill has grown by adding text from videos and books, never by showing that the text moves a number. This method is adapted from the ponytail plugin's benchmark suite (585 agentic sessions per release, three arms, hidden checks, judges that prove themselves first). `evals.json` and `triggers.json` in this folder are the current seed: 3 graded prompts and a 10 plus 10 trigger set, with no baseline arm yet.

## Contents

1. Arms and isolation
2. Tasks
3. Scorers and their self tests
4. Planted defects: recall of the gate and the critique
5. Completeness next to restraint
6. LLM judges
7. Runs and statistics
8. Changing a rule
9. Reports
10. The kwx suite to build

---

## 1. Arms and isolation

1. **Baseline:** the same agent, same harness, same tasks, no skill. The fair baseline is the real agent doing the job, not a bare chat model answering with menus.
2. **Short prompt control:** the cheapest instruction that might do the same job: "Make it look premium and avoid generic AI design." If seven words match the skill, the router and 70 files are not worth their tokens. (Ponytail's control, "Follow YAGNI principles, and prefer one-liner solutions.", was shortest and the only arm that dropped a safety guard.)
3. **Surface trait control (optional):** another public design skill or a generic frontend prompt, to separate kwx's discipline from a side effect such as terse output.
4. **Isolation.** Every arm runs with `--setting-sources project,local`, `--strict-mcp-config`, `CLAUDE_CODE_DISABLE_CLAUDE_MDS=1` and `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`. This user's global CLAUDE.md already carries design rules (no em dashes, no emoji icons, UiScale, the ui-designer agent), so an unisolated baseline is secretly half kwx. Ponytail once ran with a SessionStart hook firing in every arm; the gap collapsed to 4% and was nearly published.
5. **Fresh folder outside git** for every cell, moved into the run folder afterwards. Inside a repo the agent sees recent commit messages, which leak the answer.
6. **Load the skill as it is really loaded:** copy it into the workspace `.claude/skills/kwx-designer` and check the transcript that the Skill tool fired. Pasting SKILL.md into the system prompt tests something else.
7. **Same constraints for every arm:** no browser, no dev server, no screenshots (the user's rule), stated in one shared instruction so it is never an arm effect.
8. Read one finished transcript per arm to prove what was injected where.

## 2. Tasks

- **Seeded projects, not bare prompts.** A small React or QML app with a token file, a house `ConfirmDialog` and `EmptyState` in a separate folder with a distinctive look, a fixture with a 40 character name, an empty list, a failing fetch. An agent that narrates "done" without writing a file fails honestly; track a "wrote a file" rate.
- **Implicit requirements,** the way real tickets read, checked anyway: "add a workouts list" (empty and error branches must exist), "show the user's name in the header" (with the 40 character name), "add a delete button" (house dialog, focus on Cancel).
- **Hidden checks** the agent never sees, for correctness and safety (ponytail: 18 of 39 tasks).
- **Tiers:** over-design traps ("add a date picker to settings", "add a colour picker": native or house control first); scope tasks ("add a compact mode setting": settings screen, persistence, every list; "rename Workspace to Project": every label); convention tasks (keep the house structure even when bypassing it is shorter); open tasks ("build a landing page for X"); critique tasks (section 4).
- **Decide before the run** which tasks need a behaviour (a custom icon, a native control, a test) and which do not, then count both missing and unneeded uses.
- **Extension phase:** after the build, send a surprise follow-up ("add a third plan", "add dark mode") and count lines changed and files touched. Ponytail's structured builds took 41 and 55 lines against 156 and 257. This tests critical rule 4 directly.
- **Acceptance criteria written before the run,** graded line by line.
- **A share of tasks in a real repo pinned to a commit** (one of the user's own apps, or an open source one), for real conventions and real temptation to over-build.

## 3. Scorers and their self tests

- **Every scorer has a good and a bad reference** and a `--selftest` that runs before any paid call: good must pass, bad must be caught on its declared axis. Refuse to run if any scorer is broken.
- **The bad reference is lazy but plausible:** right on the happy path, wrong only on the corner the rule is about. A list that renders with data but has no empty or error branch; `window.confirm` where the app has a house dialog; a hex literal instead of a token; `outline: none` with no replacement.
- **Demand evidence, not a mention.** The word "empty" in a comment is not an empty state; a rendered branch is.
- **Guard against false passes:** a substring match (`351` inside `13510`), code outside a fence still scored, an exception reported as a pass, an unknown task skipped instead of failed.
- **Static scorers** (no browser on this machine): the section 14 greps of the quality gate, a literal font size outside the scale, hex colours outside the token file, missing state branches; `scripts/contrast_check.py` on every colour pair; `scripts/icon_check.py` on new SVGs. Label them structural: "it compiles" is not quality.
- **Never count accessibility markup, state branches or tests as bloat.** A size metric that punishes ARIA punishes the gate. Measure gzip size next to line count, so packing code into one line cannot game it.
- **When the skill looks worse, suspect the scorer first.** Ponytail's "correctness drop" was the grader: it could not read unfenced code (41 of 74 failures) and tested a deliverable the prompt never asked for (31 of 74).

## 4. Planted defects: recall of the gate and the critique

1. Take the entries of `~/.claude/ui-designer/mistakes.md` (each a real defect the user had to point out) and plant them in a finished screen: overflowing text, a clipped label, an icon too small for its disc, a control that vanishes on its background.
2. Add generic ones: the focus ring removed, the error branch dropped, a contrast pair lowered, an emoji icon, a hard coded size.
3. Plant at least one in a screen the change did not touch but which imports a changed component.
4. Run the quality gate or a critique and count catches. Report recall for planted defects and separately for defects outside the diff (ponytail's review: 100% against 87% without, and 100% against 78% outside the diff).
5. The same planted set doubles as mutation testing of the agent's own checks: inject small defects into its finished work and count how many its own gate run finds (ponytail: 66% against 46%).

## 5. Completeness next to restraint

- Pair every "less" metric with a completeness score (0 stub, 1 partial, 2 one requirement missing, 3 full). A screen that is smaller because it dropped the feature is caught, not rewarded.
- Report quality next to any saving, so efficiency cannot hide a regression. Ponytail printed hidden checks (97% against 96%) beside its 53% fewer lines.
- Report cost per pass (all spend over the cells that passed every gate), not only cost per run.

## 6. LLM judges

- **Auditable:** a fixed model, temperature 0 where possible, a published rubric stored with the scores, JSON only, and every score cites the element it penalises (or "none").
- **Calibrated before use:** the judge must rank a deliberate slop reference (gradient hero, repeated KPI tiles, emoji) strictly below a clean one for the same task, or the run refuses to judge. Test the gate logic offline with fake scores too: a well ordered matrix passes, an inverted one is flagged.
- **Pairwise "which screen serves the user better":** shuffle the order per pair with a seed, require the good reference to win in both slots during the self test (position bias), drop ties, sign test over pairs.
- **Judge the reply the user reads** in two calls: a blind reader sees only the task and the reply and writes what it now believes (what changed, what was left out, what the user must do); a grader compares that with the real diff for accuracy, coverage and clarity. Report length, never score it. Gate it with four fixed replies about one diff: good must beat terse on coverage, beat a reply with one false claim on accuracy, and beat a padded essay on clarity.

## 7. Runs and statistics

- At least 5 runs per cell (10 to 30 for single shot prompts); report medians. n of 1 is noise: a small local model flipped sign between n = 3 and n = 5.
- Aggregate: per task median, arm divided by baseline, geometric mean of the ratios over tasks, a 95% bootstrap interval, and "better on X of Y tasks" with a sign test.
- Interleave all arms task by task in one run, so time of day and model drift hit every arm alike.
- Keep every workspace and rescore offline when a scorer changes. Never pay twice for a measurement tweak.
- Warm the prompt cache with one throwaway call before a parallel pool; cold first cells cost 3x and look like an arm effect.
- A timeout per cell that kills only that cell's process tree; report killed and dropped cells.
- Report per model and claim nothing beyond the models tested. When the baseline fails too, it is a model ceiling, not a regression.
- Watch provider artefacts (automatic caching zeroing cost on repeated prompts, quota errors shrinking denominators) and redo those runs instead of averaging them in.

## 8. Changing a rule

- **Ship only what moves the number.** A rule change is a three arm run on the same tasks and model: baseline, current skill, changed skill, at least 6 runs per arm, one change at a time. Ponytail tried eight careful edits to fix one slip; all scored at or below the current skill, several far worse, and none shipped.
- **Show the task it helps and an existing task it could break.** A new rule often fights an old one.
- **Write rules as operations, not attitudes.** "Trace the flow end to end" fixed 0 of 3 runs; "grep every caller of the function you touch and fix the shared function once" fixed 6 of 6. For kwx: "open every screen that imports the component you changed" beats "think about consistency".
- **One clear rule beats three overlapping ones.** Piling counter instructions onto a skill made models overthink and fail more.
- **Reproduce the failure without the rule first.** A rule whose failure never reproduced is "unproven"; tag each rule proven, unproven or untested.
- **Keep the router small.** Its read cost is a tax on every trivial task. Measure the tokens kwx reads on a one line UI fix and cap them; `scripts/check_skill.py` holds SKILL.md under a budget.
- **Quick set:** about 10 tasks, one per known failure mode, run on the candidate only and compared with the reference arms of the last full run. Re-pick it when the failure modes move.

## 9. Reports

- Every report has a limitations section and says where kwx did not win (ponytail published that backend CRUD tied).
- A result that turns out wrong keeps its file with a "superseded" banner naming the bug and linking the new run. Never delete it.
- Label which examples are measured runs and which are illustrative.
- Keep real before and after pairs from the runs next to the rules they support, as teaching examples.

## 10. The kwx suite to build

Nothing below is built yet. In order:

1. Self tested static scorers for the section 14 greps, literal sizes, token use and state branches, each with a good and a bad reference.
2. Behaviour probes: one prompt per critical rule in SKILL.md where only that rule changes the outcome; the baseline should mostly fail.
3. The planted defect set from the mistakes library (section 4).
4. Arms baseline, kwx and short prompt, isolated as in section 1, 5 runs per cell.
5. The completeness judge and the pairwise judge, each calibrated first.
6. A quick set for rule edits, and the "ship only what moves the number" rule applied to every new rule from then on.
