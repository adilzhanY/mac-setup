# kwx-tester releases

The skill is versioned like software. The current version is in `VERSION` and in `metadata.version` in `SKILL.md`, every release is a git tag `vX.Y.Z` in this repo (private, `adilzhanY/kwx-tester`), and every release gets an entry here, newest first.

## How to version a change

- **Patch** (`1.2.3` to `1.2.4`): a fix or a clarification. A rule reworded, a wrong command or number corrected, a bug in a script fixed.
- **Minor** (`1.2.3` to `1.3.0`): something new that does not change old habits. A new reference file, a new language section, a new lesson from a project, a new check in the gate or the scanner.
- **Major** (`1.2.3` to `2.0.0`): the way work is done changes. A critical rule reversed, the workflow reordered, the DECISIONS.md or TODO.md format changed so old projects need updating.

Steps for every release:

1. Make the change. Run `python3 -I scripts/check_skill.py` (clean) and the self tests of any script you touched (`--selftest`).
2. Bump `VERSION` and `metadata.version` in `SKILL.md`.
3. Add an entry at the top of the list below: the version, the date, and a few lines on what changed and why (which project or which mistake taught it).
4. Commit with a one line message, tag and push: `git commit -am "kwx-tester X.Y.Z: <what>" && git tag -a vX.Y.Z -m "<what>" && git push --follow-tags`.
5. Mirror the desktop copy: `arch-config-push "kwx-tester X.Y.Z"`, and copy the skill into `~/mac-setup/skills/kwx-tester` and push that repo.

To see what changed between two versions: `git diff v1.0.0 v1.1.0 --stat`. To try an older version: `git worktree add /tmp/kwx-tester-old v1.0.0`.

A lesson from a real project (a mistake the user had to point out) is the most valuable kind of change: write it as an operation in the right reference file, add a check for it to `quality/quality-gate.md` if it can be checked, and say in the release entry which project taught it.

## 1.1.0 (2026-11-01)

Taught by the kwx A/B trial: the same model built belegfrei (Next.js site), stundenwerk (Tauri desktop) and nordwand (Expo app plus Node backend) once with the three kwx skills and once with none, followed by a blind evaluation.

Kept: spec-first independent testing. It beat the no-skills arm on tests in all three apps and caught 37 of 38 and 12 of 12 non-equivalent planted faults. The no-skills arm encoded its own rounding into its expected values.

Added to cut the 2.2 to 3.2 times token cost without losing that: effort tiers and layer balance (`strategy/strategy.md` section 5a). Tests go where the risk is, not to the easy layer. One tester subagent per job and only for Tier 1 areas. Repeats follow flake class (20 runs for I/O, time and rendering; one shuffled run plus 2 repeats for pure code). One planted fault batch proves a group of tests.

Added for coverage the trial showed missing: rendered tests for offline, error, disabled and signed-out states, with the Expo offline set and Router tests per session state; Tauri IPC and other bridges as contracts; two time zone runs on server and client; counters at zero, start == stop intervals, money that matches across UI, CSV and invoice, preview then confirm with data changed in between; login limit, lockout abuse and spoofed X-Forwarded-For tests; brand in page titles, aria-current and required state, width probes at 390 and 360 where a browser is allowed; a cold start check; a README claims check and daily journeys at release; the daily-use charter, which reports friction as UX gaps to kwx-designer; IDN emails, Unicode names and timer delay limits in the edge case catalogue; QML harness parity lessons from the UI mistakes library.

Rules: the owner's global CLAUDE.md, agents and UI mistakes library now rank above the skill (rule 9, gate F6 and F7). The tester writes its plan into the shared PLAN.md instead of a second spec.

smellscan rewritten: node:assert, t.assert, expect.soft, throw and assertion helpers (also from other scanned files) count as assertions, EAGER replaces ASSERTS and counts distinct subjects, BRANCH fires only for an assertion inside a branch, NET only for a real host in a network call, node:test options and test.each tables are found. Hits on the three skill built apps drop from 33, 20 and 55 to 3, 1 and 7, and the true positives stay.

Gate: A3, B1, C2 (repeats by flake class), D3, D5, D8, E1, E2, E4, F6 changed; D9, D10, F7 and G7 [critical] added. Three new evals: tauri-ipc-contract, expo-offline-and-counter, money-consistency-across-outputs.

## 1.0.0 (2026-10-31)

First release. Built from six research areas (test strategy and design, web and browser automation, mobile, backend plus desktop plus performance, exploratory testing with edge cases, accessibility, i18n and bug reports, test quality and CI) and a deep research report on how AI agents fail at testing (test gaming, tests that copy the implementation's bugs, LLM test generation studies, independent testers, GUI agents). Workflows: test from spec, test a change, bug hunt, test suite audit (Later to TODO.md, Plan a fix, Keep as is to DECISIONS.md), trio with kwx-designer and kwx-developer, release check. A tester's quality gate, review method and rubric. Scripts: `smellscan.py`, `diffgaps.py`, `riskgaps.py`, `smoke_site.py`, `smoke_checks.py`, `check_skill.py`, each with a self test.
