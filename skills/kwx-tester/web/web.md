# Web testing

This folder covers testing websites and web apps: static and marketing sites, Next.js apps (App Router), React single page apps and the HTTP APIs behind them. It says which kinds of test to write at which level, the default tool setup, what to test first on a landing page and on a web app, and how an agent works with a browser, including the case where the user has turned browser automation off. The general test strategy (pyramid or trophy, what to mock, flaky policy, coverage) lives in kwx-developer (`~/.claude/skills/kwx-developer/reliability/testing-strategy.md`) and the rules about never weakening tests live in `~/.claude/skills/kwx-developer/ai-agents/tests-and-honesty.md`. This folder goes deeper on the web side and does not repeat them.

## Contents

1. First: read the user's rules about browsers
2. The levels of web testing
3. Default setup for a Next.js or static site
4. What to test first: landing page vs web app
5. The rules that matter most
6. Files in this folder
7. Checks

## 1. First: read the user's rules about browsers

Before you run anything that opens a browser, read the user's instructions (`~/.claude/CLAUDE.md`, the project's `CLAUDE.md` or `AGENTS.md`, and memory files). Many users restrict agents here.

| If the rules say | Then |
|---|---|
| Browser automation is off for the agent | Do not run Playwright, Puppeteer, Lighthouse, axe in a browser, chrome devtools tools or any browser MCP yourself. You may still write browser tests into the project. Running them locally needs the user's explicit yes. CI may run them. Verify with type checks, the build, `curl`, HTML parsing, direct API and DB calls, and hand the user a short visual checklist. See `browser-automation-for-agents.md` section 6. |
| Browser automation is allowed | Use a headless browser with a fresh, isolated profile. Never the user's real profile or logged in sessions. See `browser-automation-for-agents.md`. |
| Do not move the mouse or type for the user | Never drive the user's real desktop browser or input devices. Headless runs in a separate profile are a different thing, but only when browser automation is allowed at all. |
| Nothing is said | Ask once before the first headless run, then follow `browser-automation-for-agents.md`. |

## 2. The levels of web testing

| Level | What it proves | Default tool (2026) | Runs without a browser? |
|---|---|---|---|
| Static | Types line up, obvious bugs, a11y lint, dead code | `tsc --noEmit`, ESLint with `eslint-plugin-jsx-a11y`, `eslint-plugin-playwright`, `eslint-plugin-testing-library` | Yes |
| Unit | One function or hook gives the right output | Vitest 5 (node environment) | Yes |
| Component | A component renders and reacts to the user as the spec says | Vitest + Testing Library in jsdom, or Vitest Browser Mode for layout, focus and real events | jsdom: yes. Browser Mode: no |
| API / integration | Route handlers, server actions, DB and auth work together | Vitest calling the handler or `fetch` against a local server, real Postgres or local Supabase | Yes |
| End to end | A real user journey works in a real browser against a production build | Playwright 1.64 | No |
| Visual | The page still looks the same where it should | Playwright `toHaveScreenshot`, or a hosted service (Argos, Chromatic, Percy) | No |
| Accessibility | Machine checkable WCAG failures are absent, keyboard and screen reader basics work | `@axe-core/playwright`, `jest-axe` / `vitest-axe` for components, manual keyboard and screen reader passes | Partly (html-validate a11y rules, jsdom axe without contrast) |
| Performance and SEO | Core Web Vitals budgets, bundle size, links, meta tags | Lighthouse CI, `size-limit`, lychee or linkinator, html-validate, a curl based meta tag check | Partly (bundle size, links, meta tags, HTML validation) |

Versions checked with `npm view` on 2026-10-31 (verified): `@playwright/test` 1.64.1, `vitest` 5.0.5, `jest` 30.5.2, `msw` 3.0.3, `@testing-library/react` 16.3.3, `@testing-library/user-event` 14.6.8, `@axe-core/playwright` 4.14.0, `jest-axe` 11.0.0, `happy-dom` 21.0.4, `jsdom` 30.1.3, `@lhci/cli` 0.15.1, `lighthouse` 13.6.0, `linkinator` 8.1.0, `html-validate` 11.17.0, `size-limit` 14.3.0, `next` 16.4.3.

## 3. Default setup for a Next.js or static site

The default for a solo developer. Change it only with a reason.

```text
src/**/*.test.ts(x)         Vitest unit and component tests, colocated
src/mocks/handlers.ts       MSW happy path handlers, shared by tests and dev
e2e/*.spec.ts               Playwright journeys, a11y scans, a few screenshots
e2e/auth.setup.ts           Logs in once, saves storageState
playwright.config.ts        webServer runs the production build
vitest.config.mts           jsdom by default, Browser Mode project optional
lighthouserc.js             Budgets for 3 to 5 key URLs
.size-limit.json            JS budget per entry
.lycheeignore               Link checker exclusions
```

`package.json` scripts:

```json
{
  "scripts": {
    "typecheck": "tsc --noEmit",
    "lint": "eslint .",
    "test": "vitest run",
    "test:watch": "vitest",
    "e2e": "playwright test",
    "e2e:ui": "playwright test --ui",
    "check:links": "lychee --offline --root-dir \"$PWD/out\" --include-fragments out/",
    "check:html": "html-validate \"out/**/*.html\"",
    "check:size": "size-limit"
  }
}
```

What runs where:

| Stage | Commands | Browser? |
|---|---|---|
| Every save (local) | `vitest` watch | No |
| Before a commit (agent can always run) | `typecheck`, `lint`, `test`, `next build`, curl smoke test (`browser-automation-for-agents.md` section 7), `check:links`, `check:html`, `check:size` | No |
| Before a merge (CI) | All of the above + `e2e` (Chromium, WebKit, one mobile project) + axe scans + Lighthouse CI | Yes, in CI |
| Nightly or weekly (CI) | Full browser matrix, `--repeat-each` on new tests, external link check | Yes, in CI |

For a plain static site (no framework): skip Vitest unless there is real logic. Build, then run the curl smoke test, lychee, html-validate and Lighthouse CI against the output folder. Add Playwright only for interactive parts (menu, form, theme toggle).

## 4. What to test first: landing page vs web app

### Landing page or marketing site

The risk is not logic. The risk is a broken first impression, a dead link, a page that search engines and link previews cannot read, or a form that silently drops leads. Order:

1. Every public URL returns 200 with `text/html`, unknown URLs return 404 (no soft 404). Browserless.
2. Head tags: `lang`, `<title>`, meta description, canonical, Open Graph (`og:title`, `og:type`, `og:image`, `og:url`), viewport, no `localhost` URLs. Browserless.
3. Links and anchors: internal links and `#fragments` resolve, external links checked weekly. Browserless.
4. HTML validity and the machine checkable a11y rules (alt text, labels, `lang`). Browserless with html-validate. Contrast needs a browser (axe).
5. The lead form or call to action works end to end: fill, submit, see the success state, and the request reaches the backend (Playwright, or curl the form endpoint without a browser).
6. Lighthouse budgets on the home page and one inner page: LCP, CLS, TBT, total JS.
7. Responsive layout at 360, 768 and 1280 px wide, dark mode and reduced motion. Hand this to the user as a checklist when browsers are off.

### Web app

The risk is broken journeys and data. Order:

1. The 3 to 10 critical journeys as Playwright tests: sign up, log in, the core action, payment, settings that matter. Each test creates its own data.
2. Auth and permissions: signed out users are redirected, user A cannot read user B's data (test at the API level too, it is cheaper and stronger).
3. Component tests for every form: validation messages, disabled states, error state when the API fails (MSW returns 500), empty state.
4. API tests for route handlers and server actions against a real local database.
5. axe scans on each main screen in each main state (empty, filled, error, dialog open).
6. Visual snapshots only for a few stable screens or components.

## 5. The rules that matter most

1. **Read the user's browser rules before running anything that opens a browser.** Writing browser tests is always fine; running them follows the rules (section 1). Evidence: house rule.
2. **Write the test from the spec, before or without reading the implementation.** Assert what the user is promised, not what the code happens to do. Evidence: opinion, backed by the test gaming data in kwx-developer's tests-and-honesty.
3. **Locate elements the way users do: `getByRole` with a name first, `getByTestId` last.** Role queries also fail when accessibility breaks, which is a bonus test. Evidence: moderate (Playwright and Testing Library docs).
4. **Never wait with a fixed sleep. Wait for a condition with a retrying assertion** (`await expect(locator).toBeVisible()`). Async wait problems caused 45% of flaky UI tests in a study of 235 cases, 52% on the web. Evidence: strong (Romano et al., ICSE 2021).
5. **Each test owns its data and its browser context.** No test depends on another test's leftovers or order. Evidence: moderate (Playwright isolation docs).
6. **Run end to end tests against the production build** (`next build && next start`), not `next dev`. Evidence: moderate (Next.js docs).
7. **Mock third party services at the network boundary (MSW, `page.route`), never your own code in the middle.** Hit a real local backend for your own API in end to end tests. Evidence: moderate (MSW docs, Playwright best practices).
8. **Keep end to end tests to the critical journeys.** Push every other check down to component, API or browserless levels. Evidence: moderate (Dodds testing trophy, SWE at Google).
9. **Automated a11y tools find only part of the problems.** The best case is about 57% of issues by volume (Deque, vendor data), and 29% of the barriers on GOV.UK's test page were missed by all 10 tools. Always add a keyboard pass and a screen reader smoke pass. Evidence: strong.
10. **Never accept a changed screenshot or snapshot baseline without opening the diff.** Generate baselines in the same Linux image CI uses. Evidence: moderate (Playwright and Vitest docs).
11. **Save a trace on the first retry in CI (`trace: 'on-first-retry'`) and upload the report even when the job fails.** Evidence: moderate (Playwright CI docs).
12. **Measure performance with budgets on the median of several runs, not one Lighthouse score.** The median of 5 runs is twice as stable as 1 run. Evidence: moderate (Lighthouse variability docs).
13. **Check everything that does not need a browser without one:** status codes, head tags, links, HTML validity, bundle size. It is faster, never flaky, and works when browsers are off. Evidence: opinion.
14. **Report what you could not check.** If no browser ran, say so and hand the user the visual checklist. Never write "looks good" about a page nobody rendered. Evidence: house rule.

## 6. Files in this folder

| File | What is in it | Read when |
|---|---|---|
| `playwright.md` | Locators, web first assertions, fixtures, projects, storageState auth, isolation, routing, clock, traces, sharding, retries, codegen, UI mode, test agents, component testing status, a full config for Next.js, anti patterns | Writing or reviewing any Playwright test or config |
| `component-and-unit-tests.md` | Vitest (jsdom, happy-dom, Browser Mode), Jest, Testing Library principles and query priority, user-event, Server Components limits, Next.js App Router advice | Writing component or unit tests for React or Next.js |
| `network-and-api-mocking.md` | MSW 3, Playwright `route`, HAR replay, when to mock and when to hit a real local backend, keeping mocks in line with the real API | A test talks to an API, or mocks are drifting |
| `visual-regression.md` | `toHaveScreenshot`, thresholds, stabilising fonts and animation, hosted services, baseline review rules | Adding screenshot tests or reviewing a baseline change |
| `accessibility-testing.md` | axe-core in Playwright and in components, what tools catch and miss (with the studies), keyboard checks, focus order, screen reader smoke tests, the WCAG 2.2 criteria to check | Any a11y check, any new screen, any form |
| `cross-browser-and-responsive.md` | Browser matrix by real usage, WebKit, viewport list, touch, reduced motion, dark mode, 200% zoom, slow network | Deciding which browsers and sizes to test |
| `performance-and-seo-checks.md` | Lighthouse CI, Core Web Vitals budgets, bundle size, link checks, HTML validation, meta and Open Graph checks | Before a release, or setting up CI for a site |
| `browser-automation-for-agents.md` | How an agent should drive a browser when allowed (Playwright CLI and MCP, snapshots vs screenshots, isolated profiles, console and network), and the browserless path with a curl smoke test | Any time you, the agent, want to look at a page |
| `e2e-flakiness.md` | Causes of flaky browser tests with the data, the fix for each, how to reproduce and quarantine | A browser test fails sometimes |

## 7. Checks

Tick these at the end of any web testing task.

- [ ] I read the user's rules on browsers and followed them (section 1). If no browser ran, I said so.
- [ ] Tests come from the spec or the user's request, each one names the behaviour it checks.
- [ ] No `waitForTimeout`, no `sleep`, no CSS chain or XPath locators in new tests (`rg -n -e waitForTimeout -e "locator\(['\"][.#/]" e2e`).
- [ ] Every new test creates its own data and passes alone and in any order (`npx playwright test --repeat-each=5 --shuffle <file>` in CI, or the user's yes locally).
- [ ] End to end tests run against a production build (`webServer.command` uses `build` and `start`).
- [ ] Third party calls are mocked, the app's own API is real or mocked from one shared schema.
- [ ] Browserless checks ran and passed: `tsc --noEmit`, lint, unit tests, `next build`, curl smoke test, links, HTML validation, bundle size.
- [ ] a11y: axe scan added for each new screen and state, plus a keyboard pass or a keyboard checklist for the user.
- [ ] No baseline or snapshot updated without reading the diff, and the report lists every updated baseline.
- [ ] CI keeps traces on first retry and uploads `playwright-report/` with `if: ${{ !cancelled() }}`.
- [ ] The final report lists what was verified, how, and what was left for the user to look at.
