# kwx-developer releases

The skill is versioned like software. The current version is in `VERSION` and in `metadata.version` in `SKILL.md`, every release is a git tag `vX.Y.Z` in this repo (private, `adilzhanY/kwx-developer`), and every release gets an entry here, newest first.

## How to version a change

- **Patch** (`1.2.3` to `1.2.4`): a fix or a clarification. A rule reworded, a wrong command or number corrected, a bug in a script fixed.
- **Minor** (`1.2.3` to `1.3.0`): something new that does not change old habits. A new reference file, a new language section, a new lesson from a project, a new check in the gate or the scanner.
- **Major** (`1.2.3` to `2.0.0`): the way work is done changes. A critical rule reversed, the workflow reordered, the DECISIONS.md or TODO.md format changed so old projects need updating.

Steps for every release:

1. Make the change. Run `python3 -I scripts/check_skill.py` (clean) and the self tests of any script you touched (`--selftest`).
2. Bump `VERSION` and `metadata.version` in `SKILL.md`.
3. Add an entry at the top of the list below: the version, the date, and a few lines on what changed and why (which project or which mistake taught it).
4. Commit with a one line message, tag and push: `git commit -am "kwx-developer X.Y.Z: <what>" && git tag -a vX.Y.Z -m "<what>" && git push --follow-tags`.
5. Mirror the desktop copy: `arch-config-push "kwx-developer X.Y.Z"`, and copy the skill into `~/mac-setup/skills/kwx-developer` and push that repo.

To see what changed between two versions: `git diff v1.0.0 v1.1.0 --stat`. To try an older version: `git worktree add /tmp/kwx-developer-old v1.0.0`.

A lesson from a real project (a mistake the user had to point out) is the most valuable kind of change: write it as an operation in the right reference file, add a check for it to `quality/quality-gate.md` if it can be checked, and say in the release entry which project taught it.

## 1.1.0 (2026-11-01)

Lessons from the A/B trial of 2026-11-01. The same model built three apps twice from the same briefs, once with the kwx skills and once without. The evidence is in ~/.claude/projects/-home-wopler/trial/eval/ (web.md, desktop.md, android.md, lessons.json, usage.json). The blind scores favoured the skilled builds on correctness, tests and security. But those builds had loaded SKILL.md and then almost none of the topic files, so they shipped defects the skill already forbids: a per email login lock that let anyone lock a member out, 11111111 accepted as a password, no limit on the admin login, course times in the device zone. They also used 2.2 to 3.2 times the output tokens.

New critical rule 10: read the named topic file sections before writing code that touches passwords, times, money, exports, forms, Next.js, Expo, offline caches, SQLite or Tauri, and put a Files read line in the notes and the report. New critical rule 11: scale the process to size and risk (small, medium, large). The never cut list includes money and date correctness, abuse limits, data loss guards, the daily workflows the brief implies and the README Not finished list. A new top row in Pick the workflow gives small changes a light path. Critical rule 1 now reads the owner's global files (~/.claude/CLAUDE.md, the agent definitions, the defect library for UI work). Critical rule 7 says never to ask when the client cannot be reached.

New workflow/new-project-from-brief.md covers a build from a brief with no reachable client. It includes a requirement matrix, a daily user pass (periods, quick entry with forgiving input, forgotten timer, preview before irreversible steps, derived values from the server), a life cycle table for every stateful thing, a promises table for the product's own legal text, decisions and open questions in the README, a phase budget with a Cost line, and a portable handover README. New workflow/shared-plan.md defines one PLAN.md that kwx-designer, kwx-developer and kwx-tester share, so the spec is written once. New languages/rust/tauri.md covers Tauri 2 apps: command contract test through tauri::test or generated bindings, file dialogs in Rust, least capabilities.

Quality gate: F7 is now [critical] and needs four pasted probes, including 'right password from IP B still works'. A gap documented in the README no longer passes it. New C9 [critical] proves every shown amount, date and counter at its boundaries and is never skipped in lean mode. New C10 checks that every output gives the same number. New section 13 (K1 to K4) checks the brief matrix, the README headings and that the README is portable. The report gains Size, Files read and Cost lines. Two new fast greps: date formatting without timeZone, and client IP headers read outside the one helper.

Topic fixes taught by the trial: a bundled common password blocklist with a test, and a login throttle order that cannot lock a member out (auth.md). New small admin section: session cookie, sign out, throttle, and delete wherever the privacy text promises it. One clientIp helper with TRUST_PROXY_HOPS. Place zone formatting with a grep and a two zone test run. One pricing function for screen, CSV and invoice, plus a zero duration rule. gcTime Infinity with persister maxAge (JS timers cap at 24.8 days). Preferences above the auth gate. Email validation that accepts internationalised domains. A stale preview hash on confirm steps. Export labels in place of codes. node:sqlite before better-sqlite3. Component tests for requirements that live only in the client. Choosing the Next.js rendering model from the brief. Timeboxing framework fights. In the duet, the contract carries every derived value, the UI brief passes the owner's defect library and the daily use list with no style words, the UI side never edits framework config, and background subagents under claude -p are waited for.

Three new evals came from the trial: a gym booking app built from a brief, a time tracker export with invoice rounding, and a waitlist admin built from a brief. The small change eval now checks lean mode, and check_skill.py pins the new rules and tests the new greps. The kwx-designer and kwx-tester releases should point to workflow/shared-plan.md and use the same PLAN.md section names.

## 1.0.1 (2026-10-31)

Points at the new kwx-tester skill: independent tests come from it, and its tests are never edited or weakened to get green.

## 1.0.0 (2026-10-30)

First release. Built from seven research areas (Rust, TypeScript and JavaScript, architecture and organisation, backend and security, data, reliability, codebase audit tooling) and a deep research report on what AI coding agents get wrong in real codebases. Workflows: codebase first, feature, audit and ask (Later to TODO.md, Plan a fix, Keep as is to DECISIONS.md), duet with kwx-designer. A code quality gate, review method and rubric. Scripts: `scan_conventions.py` (convention outliers per area, tested on torq, sahna, airi) and `check_skill.py`.
