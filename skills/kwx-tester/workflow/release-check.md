# Release check: what runs before a web deploy or a store release

The short procedure for "we are about to ship, check it". The full checklists, the smoke script, canary and rollback criteria are in `../quality/regression-and-release-testing.md` (web section 4, mobile section 5, canary section 6, monitoring section 7, rollback section 8); the Play testing tracks, pre-launch report, device farms and staged rollouts are in `../mobile/stores-and-device-farms.md`. This file says which checks run in which order, who does each (the agent or the owner, by the user's rules), and what the release report looks like.

## Contents

1. Before anything: rules and rollback criteria
2. Web deploy
3. Mobile store release
4. Desktop, CLI and Supabase releases
4b. README check
4c. Daily journeys
5. The release report
6. Checks

## 1. Before anything: rules and rollback criteria

1. Read the user's rules: which checks the agent may run (browsers, devices) and which go to the owner. Read DECISIONS.md for release rules the project already has.
2. Write the rollback criteria before the release starts, with numbers and a time window (`../quality/regression-and-release-testing.md` section 8). Decided calm, not during an incident.
3. Test the artifact you ship: the release build, not the dev server or a debug build.
4. A smoke failure stops everything. Do not run the regression set on a build that cannot start.

## 2. Web deploy

| Order | Check | Who | Detail |
|---|---|---|---|
| 1 | CI green on the exact commit, including e2e on the built artifact; no quarantined test covers a critical flow | agent | regression-and-release-testing.md section 4 rows 1 and 2 |
| 2 | Migrations expand only, tried on a copy; env vars and secrets present; flags for unfinished work off | agent | rows 3 to 5 |
| 3 | Production build passes; bundle size did not jump | agent | row 6; `../web/performance-and-seo-checks.md` |
| 4 | Preview smoke: key pages and API routes return the right status and text | agent | `python3 -I ~/.claude/skills/kwx-tester/scripts/smoke_checks.py <preview-url> checks.txt` (status and text per path), and `python3 -I ~/.claude/skills/kwx-tester/scripts/smoke_site.py <preview-url> / /pricing/` (head tags, links, robots.txt, 404) |
| 5 | SEO basics on changed pages: title, description, canonical, no `noindex` leaked from staging | agent | row 10 |
| 6 | Visual, accessibility and form checks of the changed pages on the preview | owner (when browsers are off for the agent) | a checklist of at most 10 lines (`../exploratory/human-check-handoff.md`) |
| 7 | Deploy, canary or quiet hour; health endpoint reports the new SHA | agent | rows 11 and 12 |
| 8 | Production smoke; error and 5xx rates within the criteria for 30 to 60 minutes | agent | rows 13 and 14 |
| 9 | Core flow once for real; rollback path available | owner, agent | rows 15 and 16 |

## 3. Mobile store release

Phones cannot be pulled back: halting a rollout stops new installs only. Test harder before mobile releases, and ship with a remote kill switch or minimum version gate (`../quality/regression-and-release-testing.md` rule 6).

| Order | Check | Who | Detail |
|---|---|---|---|
| 1 | Version bumped; CI green on the release commit with JVM and Jest tests and the critical Maestro or instrumented flows | agent | regression-and-release-testing.md section 5 rows 1 and 2 |
| 2 | Release build (R8, Hermes, minified) runs the smoke flows | CI emulator job, or the owner | row 3; locally only with the user's yes, on the one allowed emulator, never with `adb shell input` when the rules forbid it |
| 3 | Upgrade test: old store version with data, then the new build; data and login survive | owner or a CI job | row 4; migration tests from real old data (`../mobile/mobile.md` rule 8) |
| 4 | Fresh install, permissions, offline, large font, dark mode, main locales, small screen, deep links | owner | rows 5 to 8, as one checklist |
| 5 | Crash symbols and source maps uploaded; minimum version gate and remote flags answer | agent | rows 9 and 10 |
| 6 | OTA: `runtimeVersion` matches the native build; a test channel update installs | agent and owner | row 11 |
| 7 | Store listing, privacy form, permission declarations current | owner | row 12 |
| 8 | Internal track, then closed testing (the 12 testers for 14 days rule for new personal accounts), read the pre-launch report | owner, agent reads the report | `../mobile/stores-and-device-farms.md` sections 2 to 4 |
| 9 | Staged rollout, next stage gated on crash free sessions and ANR rate | owner, agent reads vitals | `../mobile/stores-and-device-farms.md` section 9 |

## 4. Desktop, CLI and Supabase releases

| Product | Before release | Detail |
|---|---|---|
| Rust CLI or TUI | full suite on the release profile; golden output tests; `--help` and exit codes; a smoke run of the built binary on a clean directory | `../desktop/cli-and-tui-testing.md` |
| Qt/QML or Quickshell app | headless tests (`QT_QPA_PLATFORM=offscreen`); the owner checks visuals after a reload; never drive the user's live desktop | `../desktop/desktop.md` sections 4 and 9 |
| Supabase | `supabase test db` (pgTAP, RLS matrix) on the local stack; migrations tried on a copy; edge functions called over HTTP locally | `../backend/database-testing.md` |

## 4b. README check

Run it before every release and before calling a built app done. A README is the first thing the owner or a reviewer tries, and a command that fails there costs more trust than a missing feature.

1. List every command and claim in README.md: run, test, build, env vars, test counts, "works offline" and similar.
2. Run each command from a clean copy with no machine specific paths or env, then follow the README literally. Clone the commit being released: `git clone . "$SCRATCH/clean" && cd "$SCRATCH/clean"`. If the work is uncommitted, copy the tracked and new files instead: `mkdir "$SCRATCH/clean" && git ls-files -co --exclude-standard -z | xargs -0 cp --parents -t "$SCRATCH/clean"`. Say in the table which one was used. A command that would open a browser, app window, emulator or device follows rule 7. Run its headless part (build, start the server and curl it, cargo test), and list the rest as 'owner to run' in the README table. That is not a FAIL. Trial: `CARGO_TARGET_DIR=/games/cargo-target` was hard coded and worked only on the builder's machine.
3. Record each row: claim, tried, passed, note. Test counts must match the last fresh run.
4. Check the headings the brief requires (for example run, test, build, decisions, open questions, not finished). A section the brief requires that is missing is blocking (gate G7 in `../quality/quality-gate.md`).

```text
| README claim                     | Tried | Passed | Note                                   |
|----------------------------------|-------|--------|----------------------------------------|
| npm install && npm run dev       | yes   | yes    |                                        |
| npm test (README says 148 tests) | yes   | no     | 151 tests ran; README count is stale   |
| cargo build --release            | yes   | no     | needs CARGO_TARGET_DIR=/games/... set  |
| npm run tauri dev                | build | owner  | opens an app window: owner to run      |
| section "Not finished"           | n/a   | no     | brief requires it, missing: blocking   |
```

## 4c. Daily journeys

Walk the day-in-the-life journeys from PLAN.md end to end, through tests, IPC or API calls, or hand them to the owner per the browser and input rules (never drive the user's desktop, a browser or a device yourself unless allowed). Desktop example: start the timer, stop it, add a manual entry, invoice the month, mark it paid with a date. One row each: done, steps it took, friction noted. Friction goes to kwx-designer as a UX gap (`../exploratory/exploratory.md` section 3).

```text
| Journey                               | Done | Steps | Friction                         |
|---------------------------------------|------|-------|----------------------------------|
| start, stop, manual entry, invoice    | yes  | 11    | manual entry refuses "1,5"       |
| mark invoice paid with a date         | no   |       | no payment date: UX gap major    |
```

## 5. The release report

```text
Release check: <app> <version or SHA> -> <target> (<date>)
Verdict: ship | ship after <items> | do not ship (<blocker>)
Rollback criteria: <numbers and window>
Ran (agent): <each check with command, exit code and counts>
README: <the README table from section 4b>
Daily journeys: <the journey table from section 4c>
Widths: <route x 1440, 390, 360 rows, or "width not measured: <reason>">
Cold start: <route, 3 fresh builds, result, log path>
Owner checks: <the checklist, at most 10 lines, and their answers when back>
Not run: <check, why, how it will run>
Open risks: <accepted by the owner, in plain words>
```

Use the numbers rules of `../ai-agents/honest-reporting.md`: real counts from fresh runs, skipped explained, flaky named, total above zero.

## 6. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| Rollback criteria first | written with numbers before the release started | the report |
| Shipped artifact tested | smoke and regression ran on the release build | commands in the Ran block |
| Smoke before regression | no regression run on a build whose smoke failed | command order |
| Rules respected | browser and device checks went to the owner or CI when the rules forbid them | the Not run and Owner checks lines |
| Mobile gate | upgrade test and kill switch or minimum version gate checked | the report |
| Honest verdict | every row of the relevant checklist marked, open items named | the report |
| README verified | every README command tried from a clean clone; counts match; the brief's sections present, not finished included | the README table |
| Daily journeys walked | each journey from PLAN.md has a row: done, steps, friction | the journey table |
| Widths and cold start | width rows per route or a not measured line; a cold start row per dynamic route for web | the report |
