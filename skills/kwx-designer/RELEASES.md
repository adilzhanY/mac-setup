# kwx-designer releases

The skill is versioned like software. The current version is in `VERSION` and in `metadata.version` in `SKILL.md`, every release is a git tag `vX.Y.Z` in this repo (private, `adilzhanY/kwx-designer`), and every release gets an entry here, newest first.

## How to version a change

- **Patch** (`1.2.3` to `1.2.4`): a fix or a clarification. A rule reworded, a wrong command or number corrected, a bug in a script fixed.
- **Minor** (`1.2.3` to `1.3.0`): something new that does not change old habits. A new reference file, a new platform section, a new lesson from a project, a new check in the gate or a script. A defect the user had to point out, added to quality/mistakes-library.md with its gate row, is a minor release.
- **Major** (`1.2.3` to `2.0.0`): the way work is done changes. A critical rule reversed, the workflow reordered, the gate's report format changed so old reports no longer compare. A defect the user had to point out, added to quality/mistakes-library.md with its gate row, is a minor release, not a major one.

Steps for every release:

1. Make the change. Run `python3 -I scripts/check_skill.py` (clean) and the self tests of any script you touched (`--selftest` on `check_skill.py`, `gate_hook.py`, `contrast_check.py`).
2. Bump `VERSION` and `metadata.version` in `SKILL.md`.
3. Add an entry at the top of the list below: the version, the date, and a few lines on what changed and why (which project or which mistake taught it).
4. Commit with a one line message (no attribution lines), tag and push: `git commit -am "kwx-designer X.Y.Z: <what>" && git tag -a vX.Y.Z -m "<what>" && git push --follow-tags`.
5. Mirror the desktop copy: `arch-config-push "kwx-designer X.Y.Z"`, and copy the skill into `~/mac-setup/skills/kwx-designer` and push that repo.

To see what changed between two versions: `git diff v1.0.0 v1.1.0 --stat`. To try an older version: `git worktree add /tmp/kwx-designer-old v1.0.0`.

A lesson from a real project (a mistake the user had to point out) is the most valuable kind of change: write it to the local mistakes library first, generalize it into `quality/mistakes-library.md`, add a check for it to `quality/quality-gate.md` if it can be checked, and say in the release entry which project taught it.

## 1.1.0 (2026-11-01)

Retaught from the A/B trial (three apps built with and without the kwx skills; the user preferred the no skills UI) and from the owner's own UI knowledge.

- The owner's knowledge now travels with the skill: `house/owner-house-style.md` (taste, Iris pointers, one scale, icons, showrooms, testing etiquette, defect loop), `quality/mistakes-library.md` (a generalized copy of ~/.claude/ui-designer/mistakes.md, KM1 to KM18; the live file is read first and wins), `quality/predict-from-code.md` (the review arithmetic: 0.6 and 0.65 glyph factors, 15% margin inside shapes, icon 40 to 55% of its disc, fill vs surface over 10 per channel), `platforms/desktop/qt-qml.md`.
- Daily use first: `patterns/daily-use.md` and `patterns/data-dense-tools.md` (period navigation, totals, derived money, labelled filters, prefilled entry, quantified statuses); gate section L.
- Rules reversed because they made the skills arm sparse and grey: destructive actions are never revealed on hover (was recommended), summary figures the user acts on are required (was banned as KPI tiles), cards are allowed for parallel or clickable items.
- Also reversed: category and status colour is data; brand colour may mark selected states and key numbers; headings 700; key figures above 24px; lean applies to code, never to user capability.
- Gate: write up only criticals and FAILs, rubric only for critiques; new rows A13, C10 to C14, E10, E11, I10, I11, J9, K3, L1 to L6; the C8 factor 0.55 corrected.
- Router: recipes per product type, at most 3 must-read files.
- Scripts: `contrast_check.py --surface`; `gate_hook.py` names the libraries and the house file at SessionStart; `check_skill.py` checks the library copy, the router budget and the reversed rules.
- 11 eval cases from the trial.
- Rules come from the 2026-10 trial evidence (eval/*.json); the paired eval run is pending.

Taught by: belegfrei-site vs belegfrei-web, stundenwerk vs stundenwerk-app, nordwand-app vs nordwand-members, and mistakes M1 to M18.

## 1.0.0 (2026-10-31)

First tracked version: the state before the trial lessons (router plus about 90 reference files over principles, visual, premium, psychology, patterns, platforms, editors, icons; quality gate with 91 rows and scoring rubric; enforcement hooks wired 2026-10-30; scripts check_skill, contrast_check, icon_check, gate_hook, watch_video; 3 eval cases).
