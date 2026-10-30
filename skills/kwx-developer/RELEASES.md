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

## 1.0.0 (2026-10-30)

First release. Built from seven research areas (Rust, TypeScript and JavaScript, architecture and organisation, backend and security, data, reliability, codebase audit tooling) and a deep research report on what AI coding agents get wrong in real codebases. Workflows: codebase first, feature, audit and ask (Later to TODO.md, Plan a fix, Keep as is to DECISIONS.md), duet with kwx-designer. A code quality gate, review method and rubric. Scripts: `scan_conventions.py` (convention outliers per area, tested on torq, sahna, airi) and `check_skill.py`.
