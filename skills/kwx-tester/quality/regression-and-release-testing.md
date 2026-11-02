# Regression and release testing

What to test before, during and after a release, so a release does not break what already worked. This file defines smoke, sanity, regression, confirmation and acceptance testing in plain terms, gives a release checklist for a web app and for a mobile store release, treats canary and staged rollouts as tests with pass and fail rules, and makes production monitoring the last test layer with written rollback criteria. The mechanics of deploying and rolling back (two phase changes, migrations, feature flags, OTA updates) are in `~/.claude/skills/kwx-developer/reliability/deploy-and-rollback.md`; this file is about what the tester checks at each step.

## Contents

1. Rules
2. The kinds of release tests
3. Building and keeping the regression set
4. Release checklist: web app
5. Release checklist: mobile store release
6. Canary and staged rollout as tests
7. Monitoring after release: the last test layer
8. Rollback criteria
9. Checks

## 1. Rules

1. **Write the rollback criteria before the release starts.** Numbers and a time window, decided calm, not during an incident. The SRE workbook's core criterion: if the canary's error rate is far from the control's, pause and roll back. Evidence: moderate.
2. **Test the artifact you ship.** The release build, not a debug build or the dev server: minification, R8, env vars and source maps change behaviour. kwx-developer requires one artifact promoted from staging to production. Evidence: moderate.
3. **Every escaped bug becomes a regression test before the fix ships.** The test fails on the old code and passes on the fix (kwx-developer `~/.claude/skills/kwx-developer/ai-agents/tests-and-honesty.md` section 3). Evidence: moderate.
4. **Smoke the real environment after every deploy.** A green CI run proves the code; it does not prove the config, DNS, secrets, CDN or store build. Evidence: moderate.
5. **Roll out to a few users first, and compare against the rest.** Before and after comparisons are noisy (weekday versus weekend); a simultaneous canary against a control is cleaner (SRE workbook). Evidence: moderate.
6. **Mobile releases cannot be pulled back from phones.** Play halting stops new installs only; users who updated "will remain on that version" (Play Console Help). Test harder before mobile releases, and ship with a remote kill switch or minimum version gate. Evidence: strong (platform behaviour).
7. **The owner does the visual and device checks the agent may not do.** Check the user's rules: if the agent may not launch a browser, emulator or device, it prepares a short checklist for the owner and runs everything else itself (curl, API calls, DB queries, CI results).

## 2. The kinds of release tests

Names vary between teams. Use these meanings (close to the ISTQB glossary, simplified):

| Kind | Question | Scope | When | Who or what |
|---|---|---|---|---|
| Smoke | Is it alive at all? Does it start, load, log in? | a handful of critical paths, minutes | on every build and right after every deploy | automated (curl script, `@smoke` tagged e2e, a Maestro launch flow) |
| Sanity | Does the thing we just changed or fixed work, roughly? | narrow, the changed area | after a fix or a small change, before deeper testing | quick, often manual or one focused test |
| Confirmation (re-test) | Is this bug really fixed? | the exact repro steps of the bug | when a fix lands | the bug's regression test plus the original steps |
| Regression | Did the change break something that worked before? | broad, unchanged areas | before each release; the automated part on every PR | the automated suite plus a short manual checklist for what is not automated |
| Acceptance | Does it do what the user or owner needs? | the user stories or spec of this release | before release | the owner (UAT), with acceptance criteria written as tests where possible |

A smoke test that fails stops everything: do not run the regression suite on a build that cannot start. Sanity is a judgement call, not a suite; do not build a "sanity suite".

## 3. Building and keeping the regression set

The regression set is the automated suite plus a manual list for what automation does not cover (visual look, real device feel, store listing). Keep it lean: a regression set nobody can finish is skipped.

Choose by risk:

1. **Critical user flows** (sign up, log in, the core action, pay, sync, export): automated end to end, one test each, tagged `@smoke` or `@critical`.
2. **Areas that broke before**: one regression test per escaped bug, named after the behaviour (`rejects a negative quantity at checkout`), with the issue link in a comment.
3. **Areas that change most** (hotspots, `test-suite-audit.md` step 8): deeper unit and integration coverage.
4. **What the release changed**: the confirmation tests and new tests of this release.

Keep it healthy:

- Remove tests for features that no longer exist in the same change that removes the feature.
- When a regression test has not failed in a year and covers stable code, it is still cheap insurance: keep it unless it is slow or flaky. Delete flaky regression tests that cannot be fixed in the quarantine window (`ci-testing.md` section 5); a flaky regression test teaches people to ignore it.
- Keep the manual list under 15 items. When an item is checked by hand for the third release in a row, automate it or drop it.

Manual regression checklist template (for the owner, in the release issue or PR):

```text
Manual regression, release 1.4.0 (about 10 minutes)
[ ] Fresh install, sign up, first run screens read well (light and dark)
[ ] Upgrade from 1.3.x: data is still there, no login loop
[ ] Core action on a slow network (Android: emulator network throttling; web: DevTools Slow 4G)
[ ] Rotate / resize: layout holds, no lost input
[ ] Largest system font size: no clipped labels on the main screens
```

## 4. Release checklist: web app

For a Next.js or static site, optionally with Supabase. "Agent" means the agent can do it without a browser; "owner" means it needs eyes or a browser the agent may not start.

**Before deploy**

| # | Check | Who | How |
|---|---|---|---|
| 1 | CI green on the exact commit being released, including e2e on the built artifact | agent | CI status for the SHA (`gh run list --commit <sha>` or `gh-axi`) |
| 2 | No quarantined test covers a critical flow | agent | `rg -n 'quarantine: ' e2e tests` and compare with the critical list |
| 3 | Database migrations are expand only (old code still works on the new schema) and were run on a copy | agent | read migrations; kwx-developer `deploy-and-rollback.md` section 4 |
| 4 | Env vars and secrets exist in the target environment | agent | the platform CLI (`vercel env ls`, `supabase secrets list`); compare with `.env.example` |
| 5 | Feature flags for unfinished work are off in production | agent | flag config |
| 6 | Production build succeeds locally or in CI with production env | agent | `npm run build`; check bundle size did not jump |
| 7 | Preview deploy smoke passes | agent | `smoke_checks.py <preview-url> checks.txt` (below) |
| 8 | Visual and accessibility pass of the changed pages on the preview | owner | short checklist from the agent; automated axe results from CI if present |
| 9 | Forms, emails, payments work in test mode on the preview | agent and owner | API calls with curl; owner checks the email arrives |
| 10 | SEO basics on changed pages: title, description, canonical, `robots.txt`, `sitemap.xml`, no `noindex` leaked from staging | agent | `curl -s <url> | rg -o '<title>[^<]*|noindex|rel="canonical"[^>]*'` |

**During deploy**

| # | Check | Who | How |
|---|---|---|---|
| 11 | Canary or gradual rollout if the platform supports it; otherwise deploy at a quiet hour when the owner is around | agent | platform docs; section 6 |
| 12 | Health endpoint reports the new version SHA | agent | `curl -s https://site/api/health | jq .version` |

**After deploy**

| # | Check | Who | How |
|---|---|---|---|
| 13 | Production smoke passes | agent | `smoke_checks.py https://site checks.txt` |
| 14 | Error rate and 5xx rate within criteria for 30 to 60 minutes | agent | monitoring query; section 7 |
| 15 | Core flow done once for real (sign in, main action) | owner | 2 minute checklist |
| 16 | Rollback path still works: previous deployment available to promote | agent | platform deployments list |

Post deploy smoke script: `scripts/smoke_checks.py` (its shell original was verified against a public site: passing status checks, a 404 check, and a failing text check that exits 1; the Python version is verified by its self test against a local server). Each line of the checks file is `path expected_status [text that must appear]`.

Run it:

```bash
cat > checks.txt <<'EOF'
/                200 Sign in
/pricing         200 per month
/api/health      200 "ok":true
/no-such-page    404
/robots.txt      200 Sitemap:
EOF
python3 -I ~/.claude/skills/kwx-tester/scripts/smoke_checks.py https://staging.example.com checks.txt
python3 -I ~/.claude/skills/kwx-tester/scripts/smoke_checks.py --selftest   # local test server, no network
```

It prints `ok   path status seconds` or `FAIL path: reason` per line and exits 1 if any check failed. A failure blocks the release: report the line and the response, do not retry until green.

Commit `checks.txt` (and a copy of the script) in the project (after the owner agrees) so CI can run them after each deploy. The text column catches the most common silent failure: a 200 page that renders an error message or an empty shell.

**Cold start.** After a production build, request each dynamic route (OG images, sitemap, API routes) once as the very first request, from three fresh builds, with the server log kept. Run it in a scratch worktree (`git worktree add "$SCRATCH/cold"`), since it deletes `.next`. It stops only the server it started. A failure seen only on the first request is a cold start bug reported with the log, not an unexplained flake.

```bash
P=${E2E_PORT:-3100}
for i in 1 2 3; do
  rm -rf .next && npm run build >/dev/null || break
  npx next start -p "$P" > "$SCRATCH/cold-$i.log" 2>&1 & pid=$!
  for t in $(seq 300); do curl -s -o /dev/null "localhost:$P/robots.txt" && break; sleep 0.2; done   # robots.txt is static: it warms nothing dynamic
  curl -s -o /dev/null -w "%{http_code} /opengraph-image\n" "localhost:$P/opengraph-image"
  kill $pid; wait $pid 2>/dev/null
done
```

## 5. Release checklist: mobile store release

For Expo / React Native and Kotlin / Compose apps, Android first.

**Before submitting**

| # | Check | Who | How |
|---|---|---|---|
| 1 | Version bumped (`versionCode` / `buildNumber`, user facing version) | agent | `app.json` / `app.config.*`, `build.gradle.kts` |
| 2 | CI green on the release commit, including JVM unit tests and the critical Maestro or instrumented flows | agent | CI status |
| 3 | The release build (minified, R8, Hermes) runs: install it on the emulator or a device and do the smoke flows. R8 and minification break reflection and serialization only in release builds | owner, or CI emulator job | `./gradlew assembleRelease` / EAS `preview` profile; Maestro flow on CI |
| 4 | Upgrade test: install the current store version, create data, update to the new build, data and login survive | owner (or a CI job that installs two APKs) | `adb install old.apk`, use it, `adb install -r new.apk`; the agent must not drive input on the user's device if their rules forbid it |
| 5 | Fresh install and first run: permissions asked at the right moment, denial handled | owner | checklist |
| 6 | Offline and flaky network: the core action fails gracefully and recovers | owner | airplane mode, then back |
| 7 | Large font scale, dark mode, the main locales, a small screen | owner | checklist |
| 8 | Deep links and notifications open the right screen | agent and owner | `adb shell am start -a android.intent.action.VIEW -d 'app://item/1'` launches without input injection; owner looks |
| 9 | Crash reporting and symbols: source maps (JS) and mapping files (R8) uploaded for this build | agent | EAS / Sentry / Crashlytics upload logs |
| 10 | Minimum version gate and remote flags work (the only fast rollback on phones) | agent | call the config endpoint with an old version header |
| 11 | OTA updates: `runtimeVersion` matches the native build; an update published to a test channel installs | agent | `app.json` policy; `eas update --channel preview` and check on the owner's device |
| 12 | Store listing: screenshots match the release, privacy data form and permissions declarations are current | owner | Play Console |

**Store tracks as test stages (Google Play)**

1. **Internal testing**: up to 100 testers, available in minutes. Smoke and the manual regression list here.
2. **Closed testing**: personal developer accounts created after 13 November 2023 must run a closed test with at least 12 testers opted in for the last 14 days continuously before applying for production (Play Console Help). Plan two weeks for the first release.
3. **Pre-launch report**: Play runs the build on real devices automatically after upload to a testing track and reports crashes, accessibility and security warnings. Read it before promoting.
4. **Production with a staged rollout** (section 6).

iOS: TestFlight for internal and external testers, then App Store phased release.

## 6. Canary and staged rollout as tests

A staged rollout is a test in production with a sample of real users. It needs what any test needs: a metric, an expected value, and a pass or fail rule decided in advance.

**Web canary** (SRE workbook, chapter "Canarying Releases"):

- Send a small share of traffic (for example 5%) to the new version while the rest stays on the old one, at the same time. Compare the two populations, not before and after.
- Break metrics down per version. A 5% canary failing 20% of requests shows up as only about 1% in a service wide graph.
- Pick a few user facing metrics (at most about a dozen): error rate, latency, and the core flow's success rate. CPU and memory are noisy.
- Run one canary at a time, long enough to cover real traffic (peak hours expose performance bugs).
- Small sites without traffic splitting: deploy to a preview URL, run the smoke and e2e suite against it, then promote; treat the first 30 to 60 minutes of production as the canary window with rollback criteria from section 8.

**Mobile staged rollout:**

| Platform | How it works | Test rule |
|---|---|---|
| Google Play staged rollout | you choose the percentage; it "won't increase automatically"; halt stops new users getting it; users who already updated keep it; no rollback, only a new fixed release (Play Console Help) | start at 1% to 5%; wait for at least a few thousand sessions or 24 to 48 hours; compare crash rate and ANR rate with the previous release in Android vitals; raise to 20%, 50%, 100% only when within criteria |
| App Store phased release | 7 days: 1%, 2%, 5%, 10%, 20%, 50%, 100% of users with automatic updates; pause up to 30 days in total; anyone can still download it manually (Apple docs) | pause at the first sign of a crash spike; compare crash free sessions with the previous version |
| EAS Update (OTA) | updates can be rolled out to a percentage of users on a channel, and rolled back to the previous update (Expo docs; kwx-developer `deploy-and-rollback.md` section 7) | same metrics per update group; roll back on breach |

For very small apps (a few hundred users), a percentage rollout gives too little data to compare. Then the tests before release carry more weight, and the rollout is mainly a way to limit damage: go 20%, 50%, 100% over a few days while watching crash reports by hand.

## 7. Monitoring after release: the last test layer

Tests cannot cover every device, network and user path. Monitoring catches what escaped, if it is set up before the release and looked at during the rollout window.

| Signal | Web | Mobile | Source |
|---|---|---|---|
| Errors | 5xx rate, JS error rate per release, failed API calls | crash free sessions and users per release; handled errors | Sentry release health defines crash free sessions as sessions "not ended by a crash", crash free users as users who "did not experience a crash" |
| Platform thresholds | | Android vitals bad behaviour thresholds: user perceived crash rate 1.09% overall (8% per phone model), user perceived ANR rate 0.47% overall (8% per phone model). Above them Play "may reduce the visibility" of the app and show a warning; assessed over 28 days | Android developers docs |
| Latency and speed | p95 latency of key endpoints; Core Web Vitals from real users | cold start time, frozen frames | APM, CrUX, Android vitals |
| Core flow success | sign ups, checkouts, syncs per hour compared with the same hour last week | same | product analytics or a DB query |
| Synthetic | a scheduled smoke run (the `smoke_checks.py` above) every 5 to 15 minutes | | cron job or uptime service |
| User reports | support email, store reviews mentioning the new version | same | inbox, Play Console reviews filtered by version |

Every release must be identifiable in these signals: the version or git SHA is attached to errors, logs and sessions (Sentry `release`, Crashlytics version code, the health endpoint).

## 8. Rollback criteria

Write these into the release issue before starting. They are defaults to adjust with the owner; the exact numbers are opinion, the method (per version comparison against a baseline, decided in advance) is from the SRE workbook.

| Signal | Halt or roll back when |
|---|---|
| Any data loss or corruption report | immediately, at any rollout stage |
| Security or auth failure (users see others' data, cannot log in) | immediately |
| Web 5xx or JS error rate | more than 2 times the previous version's rate for 10 minutes, or above 1% of requests |
| Core flow success (checkout, sync) | more than 20% below the same hour last week for 30 minutes |
| Synthetic smoke | fails twice in a row |
| Mobile crash free sessions | more than 0.5 percentage points below the previous release at the same rollout stage |
| Android user perceived crash or ANR rate | approaching 1.09% or 0.47%, or clearly above the previous release |
| Latency p95 | more than 50% above the previous version for 30 minutes |

What rollback means per platform: web, promote the previous deployment (and the database stays compatible thanks to expand only migrations); Play, halt the rollout and ship a fixed build with a higher version code; App Store, pause the phased release and submit a fix; OTA, republish or roll back to the previous update; any platform, turn off the feature flag. Mechanics: kwx-developer `reliability/deploy-and-rollback.md`.

After a rollback: write the escaped bug as a regression test first (rule 3), then fix, then release again through the same stages.

## 9. Checks

| Check | Pass condition | How to verify |
|---|---|---|
| Rollback criteria written | the release issue or PR lists numbers and windows before the rollout | read it |
| Tested artifact is the shipped artifact | the build tested in CI or by the owner has the same SHA or version code as the one released | compare build ids |
| Cold start | each dynamic route requested first after 3 fresh builds; table of route, builds, result, log path | the cold start table in the report |
| Smoke after deploy | `smoke_checks.py` (or equivalent) ran against production and passed | its output in the report |
| Version visible in monitoring | errors and sessions carry the release id | health endpoint and monitoring filter by release |
| Escaped bugs have tests | each bug fixed in this release has a test that fails without the fix | PR diff and test names |
| Regression set within budget | automated suite green; manual list under 15 items and done by the owner | release issue checklist ticked |
| Mobile upgrade path tested | install old, update to new, data survives | owner's checklist result |
| Mobile release build tested | release (minified) build exercised, not only debug | CI job or owner's note |
| Staged rollout used | Play staged rollout or App Store phased release on, with the start percentage noted | store console |
| Monitoring window kept | someone watched the signals for the window in the criteria | release issue note |
| Agent stayed within the user's rules | no local browser, emulator or input injection by the agent unless allowed; visual checks handed over as a checklist | the agent's report |
