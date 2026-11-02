# Flaky browser tests: causes and fixes

A flaky test passes and fails on the same code. Browser tests flake more than any other kind, because they add a real browser, rendering, the network, animations and a server to the usual sources of nondeterminism. This file lists the causes specific to browser tests, with the best data available on how often each happens, the fix for each, how to reproduce a flake on purpose, and what an agent must never do to make a flaky test green. The general flaky test policy (detect, quarantine within a day, fix, never paper over) is in kwx-developer `reliability/testing-strategy.md` section 11; this file is the browser specific part.

## Contents

1. Rules
2. The data
3. Causes and fixes
4. Next.js specific flakes
5. Reproducing a flake on purpose
6. What an agent must never do
7. Checks

## 1. Rules

1. **Fix the waiting, not the timing.** Replace every fixed delay with a wait for the condition the user waits for. Async wait problems were the root cause of 45.1% of flaky UI tests (52.0% on the web). Evidence: strong (Romano et al., ICSE 2021, 235 flaky tests from 62 projects).
2. **A test that passed on retry is flaky, not passing.** Playwright reports it in its own "flaky" category. Track it. Evidence: moderate.
3. **Reproduce before you fix.** Run the test many times with retries off; a fix you cannot show failing then passing is a guess. Evidence: opinion.
4. **Suspect the app before the test.** Race conditions, double submits and hydration gaps are real bugs that users hit too. Evidence: moderate (practitioner reports; a Google engineer reported that when a stable test turned flaky after a change, the cause was a production bug about 1 time in 6).
5. **Each test owns its data and does not depend on order.** Shared accounts and leftovers from other tests are a top source of parallel only failures. Evidence: moderate (Romano: test order dependency and resource load order categories; Playwright isolation docs).
6. **Run end to end tests against a production build.** The dev server compiles routes on first request and adds overlays and extra renders. Evidence: moderate (Next.js docs).
7. **Never raise timeouts, add retries, add sleeps or loosen assertions to make a flaky test pass.** Those hide the flake and sometimes a real bug. Evidence: strong (see section 6).

## 2. The data

Romano, Song, Grandhi, Yang, Wang, "An Empirical Analysis of UI-based Flaky Tests", ICSE 2021 (arXiv 2103.02669). 235 flaky UI tests from 62 projects, 152 web and 83 Android. Root causes:

| Category | Subcategory | Web | Mobile | Total |
|---|---|---|---|---|
| Async wait | Resource rendering (acting before an element or image is ready) | 47 | 14 | 61 |
| | Animation timing | 17 | 9 | 26 |
| | Network resource loading | 15 | 4 | 19 |
| Environment | Platform issue (browser or OS version) | 16 | 18 | 34 |
| | Layout difference (window size, rendering) | 9 | 1 | 10 |
| Test runner API issue | Incorrect test runner interaction (misused API) | 10 | 14 | 24 |
| | DOM selector issue | 13 | 3 | 16 |
| Test script logic | Incorrect resource load order | 11 | 11 | 22 |
| | Test order dependency | 6 | 6 | 12 |
| | Unordered collections | 5 | 0 | 5 |
| | Randomness | 2 | 3 | 5 |
| | Time | 1 | 0 | 1 |

Fixes the developers used (web counts): fixing the await mechanism 35, refactoring test logic 49, adding or increasing a delay 14, disabling animations 1. Refactoring logic (46.0% overall) and fixing delays (39.3%) were the most common. Note the difference between "fix the await mechanism" (wait for the right condition) and "add a delay": the paper counts both under delay fixes, but only the first is robust.

Scale at Google (Google Testing Blog, 2016, summarised in kwx-developer): about 1.5% of test runs flaky, about 16% of tests with some flakiness, 84% of pass to fail transitions involving a flaky test. Larger tests (more binary size, more memory, WebDriver style) were flakier (Google Testing Blog, "Where do our flaky tests come from?", 2017; the article body could not be fetched for this file, the finding is confirmed in the author's replies under the post, which also give the "production bug 1 time in 6" figure used in rule 4).

## 3. Causes and fixes

| Cause | What it looks like | Fix |
|---|---|---|
| Fixed sleep (`waitForTimeout`, `setTimeout` in test) | Passes locally, fails on a slower CI runner | Web first assertion on the expected result: `await expect(page.getByRole('status')).toHaveText('Saved')` |
| One shot check (`isVisible()`, `textContent()` then `expect`) | Fails when the UI is a few ms late | Retrying assertion (`toBeVisible`, `toHaveText`) |
| Missing `await` | Random failures, steps run out of order, "target closed" errors | `@typescript-eslint/no-floating-promises` and `playwright/missing-playwright-await` as errors |
| Waiting for the wrong signal (`networkidle`, `load`) | Hangs with polling or analytics, or proceeds too early with lazy data | Wait for the element or response the user waits for |
| Click lands before the element is ready or while it moves | Click on the wrong item, or "element is not stable" retries | Playwright already waits for stable and enabled. If something covers the target (toast, cookie banner, sticky header), deal with that element; never `force: true` |
| Animations and transitions | Element found mid animation; screenshot differs | `reducedMotion: 'reduce'` in the project, app honours it; assert on the end state |
| Data from another test | Fails only in parallel or only after a specific test | Per test data from a fixture; unique names with `test.info().testId` |
| Shared account changed by parallel tests | Settings or cart "randomly" different | One account per worker or per test; named `lock` (1.63) as a last resort |
| Test order dependency | Passes in the full run, fails alone (or the reverse) | Make each test set up its own state; prove with `--shuffle` and running the file alone |
| Unordered results | Lists in a different order between runs | Sort before comparing, or assert with `toContainText` on each item, or make the API order deterministic (it is often a real bug) |
| Time and time zones | Fails near midnight, at month end, in CI's UTC | `page.clock.setFixedTime`, fixed `timezoneId` and `locale` in the project, `TZ` for the runner |
| Randomness | Random ids, shuffled content, A/B tests | Seed it, inject it, or turn experiments off by cookie in `storageState` |
| Real third party network | Fails when a CDN, font host or API is slow | Route third parties (`context.route`), self host fonts |
| Service worker caching | Stale content, routes not intercepted | `serviceWorkers: 'block'` unless the test is about the service worker |
| Server not ready, or cold | First test times out | `webServer.url` readiness check, production build, generous `webServer.timeout` |
| Resource contention in CI | Fails only with many workers | Fewer workers in CI (Playwright recommends 1, shard for speed), `retryStrategy: 'isolated'` to confirm |
| Browser or OS differences | Fails only in WebKit or only on CI's Linux | Run that project locally in the same Docker image; fix the app or scope the test to the project with a reason |
| Viewport and layout | Element off screen or behind a mobile menu | Set `viewport` per project; open the menu in the mobile flow |
| Popups, new tabs, downloads, dialogs | Missed event, test hangs | Start waiting before the action: `const popup = page.waitForEvent('popup'); await link.click(); await (await popup).waitForLoadState()`; `page.once('dialog', d => d.accept())` |
| Strict mode matches two elements sometimes | "resolved to 2 elements" only when a toast or duplicate render appears | Scope the locator (within the dialog, filter by text), use an exact name |
| Too tight a test or assertion timeout | Fails under load with "Timeout 5000ms exceeded" | First find what is slow (trace network tab). Raise the timeout only for a known slow operation, locally, with a comment |

## 4. Next.js specific flakes

- **Clicking before hydration.** The server rendered button is visible, Playwright clicks it, but React has not attached the handler yet, so nothing happens. The test then waits for a dialog that never opens. Fixes, in order of preference:
  1. Use a real `<form action>` or a link where possible: they work before hydration (progressive enhancement), which is better for users too.
  2. Wait for a sign that hydration finished that the user can also see, such as a control that is disabled until ready and then enabled: `await expect(button).toBeEnabled()`.
  3. For idempotent actions only, retry the action and the check together:
     ```ts
     await expect(async () => {
       await page.getByRole('button', { name: 'Open filters' }).click();
       await expect(page.getByRole('dialog', { name: 'Filters' })).toBeVisible({ timeout: 1000 });
     }).toPass({ timeout: 10_000 });
     ```
     Never use this for actions with side effects (submit, pay, delete): a retry would do them twice.
- **Dev server compile on first request.** `next dev` compiles each route the first time it is hit; the first test per route can take seconds. Run end to end tests against `next build && next start`.
- **Streaming and Suspense.** Content arrives in pieces. Assert on the final content with retrying assertions, and test the `loading.tsx` state on purpose by delaying the data (route a slow API).
- **Cached data between tests.** The Data Cache and `revalidate` can serve data created by an earlier test, or hide a change. Use unique data per test and test revalidation explicitly.
- **Hydration mismatch warnings** (dates, `Math.random`, `typeof window` in render) often go with flaky text assertions. Fail the test on console errors (`playwright.md` section 10) and fix the render.

## 5. Reproducing a flake on purpose

Run these in CI, or locally with the user's yes if browser automation is restricted. Flags verified with `npx playwright test --help` (1.64.1).

```bash
# Hammer one test with retries off
npx playwright test e2e/checkout.spec.ts --repeat-each=50 --retries=0 --workers=4

# Order and parallel problems
npx playwright test --shuffle --retries=0
npx playwright test e2e/checkout.spec.ts --workers=1        # passes alone but fails in the suite? shared state
npx playwright test --repeat-each=10 --fail-on-flaky-tests  # strict gate after a fix

# Rerun only what failed last time
npx playwright test --last-failed --trace on
```

Make the environment harsher to surface timing bugs: CPU throttling through CDP (`Emulation.setCPUThrottlingRate`, Chromium only, see `cross-browser-and-responsive.md` section 8), more workers than cores, a delayed API route. Then open the trace of a failing run: the timeline shows what the page looked like at the moment the step ran, and the network tab shows what was still pending.

Once reproduced, write down the failure rate before the fix (for example 7 of 50) and after (0 of 200). That pair of numbers is the evidence in the report.

## 6. What an agent must never do

These turn a visible flake into an invisible one. kwx-developer `~/.claude/skills/kwx-developer/ai-agents/tests-and-honesty.md` explains why agents are prone to them.

| Tempting move | Why it is wrong | Do instead |
|---|---|---|
| Add `waitForTimeout(1000)` | Moves the race, does not remove it; slows every run | Wait for the condition |
| Raise the global timeout or `expect.timeout` | Hides real slowness and makes failures slow to report | Find the slow step in the trace |
| Add retries, or `test.describe.configure({ retries: 5 })` | A pass on retry is still a flake; the bug ships | Fix, or quarantine with an issue |
| Loosen the assertion (`toContainText` instead of `toHaveText`, regex that matches anything, `toBeTruthy`) | The test stops checking the spec | Keep the spec's assertion; fix the cause |
| `force: true`, `.first()`, `{ strict: false }` style escapes | Skips the checks that revealed an overlay or a duplicate render | Fix the overlay or the locator |
| `test.skip` or `test.fixme` without an issue and owner | The suite shrinks silently | Quarantine with a tag, an issue link and a deadline, and say so in the report |
| Let the Playwright healer agent patch it unreviewed | It optimises for green, and may skip the test | Review every patch against the spec |
| Catch the error inside the test | Turns a failure into a pass | Let it fail |

If you cannot reproduce or fix a flake within the task, stop and report: the test, the failure rate you saw, the trace path, your best hypothesis, and the quarantine you propose. Do not ship a "fix" you could not verify.

## 7. Checks

| Check | Pass condition | How |
|---|---|---|
| No sleeps | 0 hits | `rg -n -F -e waitForTimeout -e "setTimeout(r" e2e` |
| No idle waits | 0 hits | `rg -n networkidle e2e` |
| No floating promises | Lint rules on and clean | `npx eslint e2e` with `no-floating-promises` and `playwright/missing-playwright-await` |
| Retries only in CI | `retries: process.env.CI ? 2 : 0` or similar | `rg -n retries playwright.config.*` |
| Flaky tests tracked | Each quarantined test has an issue link and owner | `rg -n -e "@flaky" -e "test.fixme" e2e` |
| Fix proven | Failure rate before and after, from `--repeat-each` with retries off | numbers in the report |
| Independence | Passes with `--shuffle` and alone | CI job or the user's yes |
| Production build | `webServer.command` uses `build` and `start` | read the config |
| Third parties routed, service workers blocked where needed | Routes in a fixture or `beforeEach`; `serviceWorkers: 'block'` | read the config and fixtures |
| No timeout or assertion was loosened to pass | Diff shows no raised timeouts, retries or weaker matchers without a stated reason | read the diff |
