# Playwright

How to write Playwright tests that stay green for the right reasons and go red for the right reasons. It covers locators, web first assertions and auto waiting, fixtures, projects (browsers and mobile viewports), `storageState` auth, test isolation, network routing, the clock API, traces and what CI should keep, sharding, the retry policy, codegen, UI mode, the new test agents, the current state of component testing, a full config for Next.js, and the anti patterns to reject in review. Version: Playwright 1.64.1 (`npm view @playwright/test version`, verified 2026-10-31). kwx-developer's `reliability/testing-strategy.md` section 8 gives the short version; this file is the deep one. Before running any of these commands yourself, check the user's browser rules (`web.md` section 1).

## Contents

1. Rules
2. Locators
3. Web first assertions and auto waiting
4. Fixtures and page objects
5. Projects: browsers, mobile, setup
6. Authentication with storageState
7. Test isolation and test data
8. Network routing
9. Time: the clock API
10. Traces, screenshots, video and reports
11. CI: workers, sharding, retries, flaky tests
12. Tools: codegen, UI mode, debug, test agents
13. Component testing status (1.62 and later)
14. Config for Next.js
15. Anti patterns
16. Checks

## 1. Rules

1. **Locate by role and accessible name first** (`getByRole('button', { name: 'Pay' })`), then label, text, placeholder, alt, title, and test id last. Reason: tests follow what users see and break only when the user facing contract changes. Evidence: moderate (playwright.dev best practices and locators).
2. **Assert with web first assertions** (`await expect(locator).toHaveText(...)`). They retry until the timeout (5 s by default). Never `expect(await locator.isVisible()).toBe(true)`. Reason: the manual check "won't wait a single second" (Playwright docs). Evidence: moderate.
3. **Never use `page.waitForTimeout`.** Wait for a visible result: an element, a URL, a response. Reason: fixed waits are the classic async wait flake; 45% of flaky UI tests had an async wait root cause (Romano et al. 2021). Evidence: strong.
4. **Each test is independent.** Fresh context per test (default), own data, no order dependence. Reason: lets you run one test alone, in parallel, sharded and retried. Evidence: moderate.
5. **Log in once per role with a setup project and `storageState`.** Do not log in through the UI in every test (except the login test itself). Evidence: moderate.
6. **Mock what you do not control** (payment provider, maps, analytics, email API) with `page.route`. Hit your own backend for real. Evidence: moderate ("Only test what you control", Playwright best practices).
7. **CI: `forbidOnly`, retries only in CI, trace on first retry, report uploaded even on failure.** A test that passes on retry is flaky and goes into the flaky policy. Evidence: moderate.
8. **Run against the production build.** Evidence: moderate (Next.js Playwright guide: "We recommend running your tests against your production code").
9. **Lint the tests** with `eslint-plugin-playwright` and `@typescript-eslint/no-floating-promises`, and type check them (`tsc --noEmit`). A missing `await` is a silent race. Evidence: moderate.
10. **Keep the suite small and focused on journeys.** Logic and edge cases go to component and API tests. Evidence: moderate.

## 2. Locators

Order of preference (playwright.dev/docs/locators):

| Priority | Locator | Use for |
|---|---|---|
| 1 | `page.getByRole(role, { name })` | Buttons, links, headings, form controls, dialogs, tabs, rows. Almost everything |
| 2 | `page.getByLabel('Email')` | Form fields with a label |
| 3 | `page.getByText('Welcome back')` | Non interactive text |
| 4 | `page.getByPlaceholder(...)` | Only if the field has no label (then file an a11y bug) |
| 5 | `page.getByAltText(...)` | Images |
| 6 | `page.getByTitle(...)` | Rare, `title` is not read reliably by screen readers |
| 7 | `page.getByTestId('cart-total')` | Dynamic text, canvas, charts, or no accessible name possible |
| Avoid | `page.locator('.btn-primary > span')`, XPath | CSS and XPath "are not recommended" because the DOM changes |

```ts
// Good: scoped, user facing, strict
const row = page.getByRole('row').filter({ hasText: 'Invoice 1042' });
await row.getByRole('button', { name: 'Download' }).click();

// Good: filter by a child locator
await page.getByRole('listitem')
  .filter({ has: page.getByRole('heading', { name: 'Pro plan' }) })
  .getByRole('button', { name: 'Choose' })
  .click();

// Good: scope to a dialog (1.64 also adds saveButton.within(dialog) for the same idea)
const dialog = page.getByRole('dialog', { name: 'Delete project' });
await dialog.getByRole('button', { name: 'Delete' }).click();

// Bad: position and styling
await page.locator('div.card:nth-child(3) .btn').click();
await page.getByRole('button').first().click(); // first(), last(), nth() are "not recommended"
```

Rules:

- **Locators are strict.** An action on a locator that matches two elements throws. Fix the locator (add a name, scope it, filter it); do not reach for `.first()`.
- **Use `exact: true` or a regex when names overlap**: `getByRole('button', { name: 'Save', exact: true })` so it does not also match "Save draft".
- **Combine with `.and()` and `.or()`.** `.or()` is useful for "either the onboarding dialog or the dashboard": `await expect(dashboard.or(onboarding).first()).toBeVisible()`.
- **Test ids are a contract.** If you add `data-testid`, name it after meaning (`invoice-total`), not layout. Change the attribute with `use: { testIdAttribute: 'data-qa' }` if the project already uses one.
- **When no role query works, that is usually an a11y bug** (a `div` with a click handler, an icon button with no label). Report it instead of adding a test id. Evidence: opinion, shared by Testing Library docs.
- **Generate locators, then review them**: `npx playwright codegen http://localhost:3000` picks role locators when it can. Codegen needs a headed browser, so it is for the user to run, or for an agent only when browsers are allowed.

ARIA snapshots (`toMatchAriaSnapshot`, since 1.49) assert the structure of the accessibility tree as YAML. Use them for a whole region whose structure matters (navigation, a pricing table) instead of ten separate assertions:

```ts
await expect(page.getByRole('navigation', { name: 'Main' })).toMatchAriaSnapshot(`
  - link "Home"
  - link "Pricing"
  - link "Docs"
  - button "Sign in"
`);
```

Matching is partial by default (`/children: contain`), so extra items do not fail unless you set `/children: equal`. They break less than screenshots and also catch a11y regressions (a link that lost its name).

## 3. Web first assertions and auto waiting

Actions (`click`, `fill`, `check`) auto wait until the element is attached, visible, stable, enabled and receives events. Assertions with `await expect(locator)` retry until they pass or time out.

Auto retrying (always `await` them): `toBeVisible`, `toBeHidden`, `toBeEnabled`, `toBeDisabled`, `toBeChecked`, `toBeFocused`, `toBeInViewport`, `toHaveText`, `toContainText`, `toHaveValue`, `toHaveCount`, `toHaveAttribute`, `toHaveClass`, `toContainClass`, `toHaveAccessibleName`, `toHaveAccessibleDescription`, `toHaveAccessibleErrorMessage`, `toHaveRole`, `toHaveCSS`, `toHaveURL`, `toHaveTitle`, `toHaveScreenshot`, `toMatchAriaSnapshot`, and `toBeOK` for API responses.

Not retrying: `toBe`, `toEqual`, `toContain`, `toBeTruthy` and the other generic matchers. Use them only on values you already have.

```ts
// Good
await expect(page.getByRole('status')).toHaveText('Saved');
await expect(page).toHaveURL(/\/dashboard$/);
await expect(page.getByRole('row')).toHaveCount(3);

// Bad: reads once, no retry
expect(await page.getByRole('status').textContent()).toBe('Saved');
```

Other tools:

- **Custom message**: `await expect(banner, 'payment success banner').toBeVisible()`. Shows in the report.
- **Soft assertions** keep the test running after a failure, so one run reports several problems: `await expect.soft(price).toHaveText('$9')`. Use them for a list of independent checks on one page, not for steps that depend on each other.
- **`expect.poll`** turns any async value into a retrying assertion (for example an API status or a DB row):
  ```ts
  await expect.poll(async () => (await request.get('/api/jobs/42')).status(), { timeout: 15_000 }).toBe(200);
  ```
- **`expect(...).toPass()`** retries a whole block. Its default timeout is 0, so always pass one: `.toPass({ timeout: 10_000 })`.
- **Change the timeout** per assertion (`{ timeout: 10_000 }`) or globally (`expect: { timeout: 7_000 }`), not with sleeps. If you need more than 15 s, something is wrong with the app or the test data.
- **Wait for a response** when the UI gives no signal:
  ```ts
  const saved = page.waitForResponse(r => r.url().endsWith('/api/profile') && r.request().method() === 'PUT');
  await page.getByRole('button', { name: 'Save' }).click();
  expect((await saved).ok()).toBe(true);
  ```
  Start the wait before the click, or you can miss the response.
- **Do not use `waitForLoadState('networkidle')`** as a readiness signal. Apps with polling, analytics or websockets never go idle, and the lint rule `playwright/no-networkidle` flags it. Wait for the element the user waits for.

## 4. Fixtures and page objects

Fixtures give each test exactly what it needs and clean up after it. Prefer them over `beforeEach` for anything with setup and teardown.

```ts
// e2e/fixtures.ts
import { test as base, expect } from '@playwright/test';

type Fixtures = { project: { id: string; name: string } };

export const test = base.extend<Fixtures>({
  project: async ({ request }, use) => {
    const name = `e2e-${test.info().testId}-${Date.now()}`;
    const res = await request.post('/api/projects', { data: { name } });
    expect(res.ok()).toBe(true);
    const project = await res.json();
    await use(project);                                  // the test runs here
    await request.delete(`/api/projects/${project.id}`); // cleanup, runs even if the test failed
  },
});
export { expect };
```

```ts
// e2e/projects.spec.ts
import { test, expect } from './fixtures';

test('renaming a project shows the new name in the sidebar', async ({ page, project }) => {
  await page.goto(`/projects/${project.id}/settings`);
  await page.getByLabel('Project name').fill('Renamed');
  await page.getByRole('button', { name: 'Save' }).click();
  await expect(page.getByRole('navigation').getByRole('link', { name: 'Renamed' })).toBeVisible();
});
```

- Worker scoped fixtures (`{ scope: 'worker' }`) run once per worker: use them for expensive things like a seeded tenant or one account per worker.
- `{ auto: true }` fixtures run for every test: good for failing a test on console errors (see section 10).
- Page objects are fine for long flows reused in many tests. Keep them thin: methods return locators or perform one user action. Do not hide assertions inside them, so the test still reads as a spec. Evidence: opinion.

## 5. Projects: browsers, mobile, setup

A project is the same tests under a different configuration.

```ts
projects: [
  { name: 'setup', testMatch: /.*\.setup\.ts/ },
  { name: 'chromium', use: { ...devices['Desktop Chrome'], storageState: 'playwright/.auth/user.json' }, dependencies: ['setup'] },
  { name: 'webkit', use: { ...devices['Desktop Safari'], storageState: 'playwright/.auth/user.json' }, dependencies: ['setup'] },
  { name: 'mobile-chrome', use: { ...devices['Pixel 7'], storageState: 'playwright/.auth/user.json' }, dependencies: ['setup'] },
  { name: 'mobile-safari', use: { ...devices['iPhone 15'], storageState: 'playwright/.auth/user.json' }, dependencies: ['setup'] },
],
```

Device names checked in the 1.64.1 registry (verified with `require('playwright-core').devices`): `Pixel 7` (412x839, Chromium, touch), `iPhone 15` (393x659, WebKit, touch), `iPhone SE (3rd gen)` (375x667), `Galaxy S24` (360x780), `iPad Pro 11` (834x1194), `Desktop Chrome` and `Desktop Safari` (1280x720). Newer ones exist (`Pixel 9`, `iPhone 17`).

- Mobile projects emulate viewport, device scale factor, touch and user agent. They do not emulate a real phone's CPU, GPU or iOS Safari quirks exactly. WebKit in Playwright is close to Safari, not identical. See `cross-browser-and-responsive.md`.
- Use `grep` and tags to run a subset per project: `test('checkout @smoke', ...)` and `{ name: 'mobile-chrome', grep: /@smoke/ }`.
- Since 1.64 a project can be marked so only some projects run by default (`default` option), for example keep the full matrix for nightly runs.

### Layout probes at real widths

Only in projects that already use Playwright, in CI, or where the owner allows a headless browser. Otherwise hand the code check back to kwx-designer and state in the report that width was not measured.

- For every route at 1440, 390 x 844 and 360 x 800, assert `document.documentElement.scrollWidth <= window.innerWidth`, and report the first element past the viewport; mark intentional scrollers with data-scroll-ok. A table inside an `overflow-x-auto` wrapper keeps the document width at 390, so the element check is what catches it.
- For data tables, assert that cells holding an email, a name or an amount do not wrap (the text range has one client rect).
- A main column under 60% of a 1440 viewport with nothing beside it is a visual lead for kwx-designer, not a failing assertion.

```ts
for (const width of [1440, 390, 360]) {
  test(`no horizontal scroll on /pricing at ${width}`, async ({ page }) => {
    await page.setViewportSize({ width, height: width === 1440 ? 900 : 800 });
    await page.goto('/pricing');
    const r = await page.evaluate(() => {
      const vw = window.innerWidth;
      let firstOverflow = '';
      for (const el of document.querySelectorAll('body *')) {
        if (el.closest('[data-scroll-ok]')) continue;
        if (el.getBoundingClientRect().right > vw + 1) { firstOverflow = el.tagName + '.' + (el.getAttribute('class') ?? ''); break; }
      }
      return { sw: document.documentElement.scrollWidth, vw, firstOverflow };
    });
    expect(r.sw, `first element past the viewport: ${r.firstOverflow}`).toBeLessThanOrEqual(r.vw);
    expect(r.firstOverflow, 'element past the viewport').toBe('');
  });
}
```

Trial: the pricing page reached 537 px at 390 behind an `overflow-x-auto` wrapper, and admin emails broke mid word.

## 6. Authentication with storageState

Log in once, save cookies, local storage and IndexedDB to a file, reuse it (playwright.dev/docs/auth).

```ts
// e2e/auth.setup.ts
import { test as setup, expect } from '@playwright/test';
const authFile = 'playwright/.auth/user.json';

setup('authenticate', async ({ page }) => {
  await page.goto('/login');
  await page.getByLabel('Email').fill(process.env.E2E_USER!);
  await page.getByLabel('Password').fill(process.env.E2E_PASSWORD!);
  await page.getByRole('button', { name: 'Sign in' }).click();
  await page.waitForURL('/dashboard');
  await expect(page.getByRole('button', { name: 'Account' })).toBeVisible();
  await page.context().storageState({ path: authFile });
});
```

Faster, when the app has an API login (for Supabase: sign in with the JS client against the local stack and write the session the way the app expects, or call the app's own login route):

```ts
setup('authenticate via API', async ({ request }) => {
  await request.post('/api/login', { form: { email: process.env.E2E_USER!, password: process.env.E2E_PASSWORD! } });
  await request.storageState({ path: 'playwright/.auth/user.json' });
});
```

Rules:

- **`playwright/.auth` goes in `.gitignore`.** The file is a live credential. Use test accounts only, never a real user's account.
- **Tests that change server state on a shared account interfere in parallel.** Use one account per worker (a worker scoped fixture keyed on `test.info().parallelIndex`) or create a fresh user per test through the API.
- **Several roles**: one setup test per role, then `test.use({ storageState: 'playwright/.auth/admin.json' })` per file or `describe`. For admin and user in one test, open two contexts.
- **Signed out tests**: `test.use({ storageState: { cookies: [], origins: [] } })`.
- **`sessionStorage` is not saved.** Restore it with `context.addInitScript` if the app keeps auth there.
- Credentials come from environment variables or CI secrets, never from the test file.

## 7. Test isolation and test data

Playwright gives each test a new browser context ("equivalent to incognito-like profiles"): no shared cookies, storage or cache. Your job is the server side.

- **Create data per test through the API or DB, not through the UI.** UI setup is slow and makes one broken screen fail fifty tests.
- **Make data unique**: include `test.info().testId` or a random suffix in names and emails, so parallel workers and retries never collide.
- **Start clean rather than clean up.** The Playwright docs favour fresh state because cleanup is easy to forget. Clean up in fixture teardown anyway, so the dev database does not fill up.
- **No order dependence.** `test.describe.configure({ mode: 'serial' })` is a last resort for a truly sequential flow; if one test fails the rest are skipped and retried as a group. Run new tests with `--shuffle` (1.64) and `--repeat-each` to prove independence.
- **Shared mutable resources** (one global settings row, a singleton feature flag): since 1.63 tests can declare a named `lock` so tests with the same lock never run at the same time. Prefer removing the shared resource.
- **Control the database**: run against a local or ephemeral database seeded by script (local Supabase, a Docker Postgres), never production. See `network-and-api-mocking.md` section 5.

## 8. Network routing

```ts
// Stub a third party API
await page.route('**/api.stripe.com/**', route => route.fulfill({ status: 200, json: { id: 'pi_test', status: 'succeeded' } }));

// Simulate failure and slowness of your own API to test error and loading states
await page.route('**/api/projects', route => route.fulfill({ status: 500, json: { error: 'boom' } }));
await page.route('**/api/search*', async route => { await new Promise(r => setTimeout(r, 2000)); await route.continue(); });
// (a delay inside a route handler is fine: it shapes the server, it does not make the test wait blindly)

// Patch a real response
await page.route('**/api/plans', async route => {
  const response = await route.fetch();
  const json = await response.json();
  json.push({ id: 'enterprise', price: null });
  await route.fulfill({ response, json });
});

// Block analytics and fonts from third parties to cut noise
await context.route(/(google-analytics|plausible|hotjar)\./, route => route.abort());
```

- Register routes **before** `page.goto`.
- `context.route` applies to every page in the context, including popups. `page.route` to one page.
- Service workers can bypass routing. If the app registers one (PWA, MSW in the browser), set `use: { serviceWorkers: 'block' }` for routed tests.
- **HAR replay** records real traffic once and replays it: `await page.routeFromHAR('e2e/hars/plans.har', { url: '**/api/**', update: false })`. Record with `update: true`. HARs go stale silently; re-record on purpose and review the diff.
- **WebSockets**: `page.routeWebSocket('wss://example.com/ws', ws => { ... })` can fully mock a socket or sit between the page and the real server.
- `@msw/playwright` (0.7.0) lets Playwright tests reuse the same MSW handlers as component tests. Its API changed several times before 1.0; check the README of the installed version. See `network-and-api-mocking.md`.

## 9. Time: the clock API

Never wait for real time to pass. Control it (playwright.dev/docs/clock).

```ts
// Fixed "now" while timers keep running: dates, "3 days left" banners
await page.clock.setFixedTime(new Date('2026-03-01T10:00:00Z'));
await page.goto('/billing');
await expect(page.getByText('Trial ends in 3 days')).toBeVisible();

// Full control: install first, before any other clock call and before goto
await page.clock.install({ time: new Date('2026-03-01T08:00:00Z') });
await page.goto('/editor');
await page.clock.fastForward('30:00');           // jump 30 minutes, fire due timers once
await expect(page.getByRole('dialog', { name: 'Still there?' })).toBeVisible();
await page.clock.runFor(2000);                    // tick 2 s, firing every timer and frame on the way
```

- `setFixedTime` for "what day is it" tests; `install` + `fastForward` / `runFor` / `pauseAt` for timeouts, debounces, session expiry and countdowns.
- The clock affects the browser only. The server still uses real time; for server side time logic use API tests with an injected clock.
- Set `timezoneId` and `locale` in the project (`use: { timezoneId: 'Asia/Almaty', locale: 'kk-KZ' }`) to test date formatting. For the test runner process use the `TZ` environment variable.

## 10. Traces, screenshots, video and reports

| Setting | Local | CI | Why |
|---|---|---|---|
| `trace` | `'off'` (use `--trace on` when debugging) | `'on-first-retry'` | Recording every test is "performance heavy". The first retry captures the flaky or failing run |
| `screenshot` | `'off'` | `'only-on-failure'` | Cheap, quick look at the end state |
| `video` | `'off'` | `'retain-on-failure'` or `'off'` | The trace already has a film strip; video is for people who will not open a trace |
| reporter | `'list'` | `[['github'], ['html', { open: 'never' }]]` (+ `['blob']` when sharding) | Annotations on the PR plus a browsable report |

Valid trace modes in 1.64.1 (verified with `npx playwright test --help`): `on`, `off`, `on-first-retry`, `on-all-retries`, `retain-on-failure`, `retain-on-first-failure`, `retain-on-failure-and-retries`.

A trace holds each action with before and after DOM snapshots, the source line, console logs, every network request with headers and bodies, errors and attachments. Open it with `npx playwright show-trace trace.zip` or drop it on trace.playwright.dev (runs locally in the browser, nothing uploaded). Agents can read traces without a browser: `npx playwright trace` has subcommands for inspecting trace files from the command line (1.59 and later).

Fail tests on unexpected browser errors with an auto fixture. Many real bugs show only as a console error or an uncaught exception:

```ts
export const test = base.extend<{ failOnPageErrors: void }>({
  failOnPageErrors: [async ({ page }, use) => {
    const errors: string[] = [];
    page.on('pageerror', e => errors.push(`pageerror: ${e.message}`));
    page.on('console', m => { if (m.type() === 'error') errors.push(`console: ${m.text()}`); });
    await use();
    expect(errors, 'browser errors during the test').toEqual([]);
  }, { auto: true }],
});
```

Keep an allowlist for known third party noise, and treat every new entry as a decision, not a reflex.

## 11. CI: workers, sharding, retries, flaky tests

```yaml
# .github/workflows/e2e.yml (shape from playwright.dev/docs/ci)
name: e2e
on: [pull_request]
jobs:
  e2e:
    runs-on: ubuntu-latest
    timeout-minutes: 30
    strategy:
      fail-fast: false
      matrix:
        shard: [1/2, 2/2]
    steps:
      - uses: actions/checkout@v5
      - uses: actions/setup-node@v5
        with: { node-version: lts/* }
      - run: npm ci
      - run: npx playwright install --with-deps chromium webkit
      - run: npx playwright test --shard=${{ matrix.shard }}
      - uses: actions/upload-artifact@v5
        if: ${{ !cancelled() }}
        with:
          name: blob-report-${{ strategy.job-index }}
          path: blob-report/
          retention-days: 14
```

Merge the shard reports in a follow up job with `npx playwright merge-reports --reporter html ./all-blob-reports` after downloading the blob artifacts.

- **Workers**: Playwright recommends `workers: 1` in CI "to prioritize stability and reproducibility", and sharding across jobs for speed. On a strong self hosted runner, more workers are fine once the suite is proven independent.
- **Install only the browsers you test** (`npx playwright install --with-deps chromium`). Do not cache browser binaries; the docs say restoring the cache takes about as long as downloading. Or use the image `mcr.microsoft.com/playwright:v1.64.1-noble`, pinned to the same version as `@playwright/test` (required for screenshot baselines).
- **Retries**: `retries: process.env.CI ? 2 : 0`. Locally 0, so flakiness is visible. A test that passes on retry is reported as "flaky" (Playwright's own category), not "passed".
- **`retryStrategy: 'isolated'`** (1.62) runs retries at the end, one by one in a single worker. It tells you whether a failure was caused by load or interference. Slower; use it when you investigate.
- **Strict mode**: `failOnFlakyTests: !!process.env.CI` (config since 1.52, flag `--fail-on-flaky-tests`) fails the run when any test needed a retry. Turn it on once the suite is stable, so new flakiness cannot sneak in.
- **Fast feedback**: `--only-changed=origin/main` runs only test files affected by the diff; `--last-failed` reruns the failures. Always run the full suite before merge.
- **Never ship a focused test**: `forbidOnly: !!process.env.CI`.
- The flaky policy itself (detect, quarantine within a day, fix the cause, never paper over) is in kwx-developer `testing-strategy.md` section 11 and `e2e-flakiness.md`.

## 12. Tools: codegen, UI mode, debug, test agents

All of these open a headed browser except where noted. Under a "no browser for the agent" rule, they are for the user to run.

| Tool | Command | Use |
|---|---|---|
| Codegen | `npx playwright codegen http://localhost:3000` | Record a flow, get role based locators. Rewrite the result: add assertions, remove noise, add data setup |
| UI mode | `npx playwright test --ui` | Watch mode with time travel through each step. Best for writing and fixing tests |
| Inspector | `npx playwright test e2e/cart.spec.ts:12 --debug` | Step through one test |
| VS Code extension | | Run, debug, pick locators from the editor |
| Show report | `npx playwright show-report` | Open the HTML report (serves a local page) |
| List tests | `npx playwright test --list` | No browser. Check what will run, catch duplicate titles |
| Trace CLI | `npx playwright trace ...` | No browser. Inspect a trace from the terminal |

**Playwright Test Agents** (1.56 and later): `npx playwright init-agents --loop=claude` (also `vscode`, `codex`, `opencode`) writes three agent definitions. The planner explores the app and writes a Markdown plan in `specs/`, the generator turns the plan into tests in `tests/`, the healer replays failing tests and patches them. Regenerate the definitions after every Playwright upgrade. Two warnings for a tester:

- The planner and healer drive a real browser. They fall under the user's browser rules like any other automation.
- **The healer edits tests until they pass, and may mark a test skipped if it "believes that functionality is broken."** That is exactly the test weakening that kwx-developer's `~/.claude/skills/kwx-developer/ai-agents/tests-and-honesty.md` forbids. Treat every healer patch as a proposal: read the diff, check that the assertion still matches the spec, and never let it change an expected value without a spec reason. Evidence: opinion, based on the Playwright docs and the test gaming studies.

## 13. Component testing status (1.62 and later)

Playwright component testing changed in 1.62. The old experimental packages (`@playwright/experimental-ct-react`, `-ct-react17`, `-ct-vue`) "have been removed and are no longer published". Projects still on them should stay on 1.62 until they migrate.

The new model: a component test is a normal Playwright test that uses the built in `mount` fixture against a "story gallery" page served by your own dev server. Stories are named exports in `*.story.*` files.

```ts
import { test, expect } from '@playwright/test';

test('click should expand', async ({ mount }) => {
  const component = await mount('components/Expandable/Stateful');
  await component.getByRole('button').click();
  await expect(component.getByTestId('expanded')).toHaveValue('true');
});
```

Set up with `npx playwright init-skills`, then ask the coding agent to "set up component testing using the playwright-component-testing skill"; run with `npx playwright test --project=components`. Caveats from the docs: story ids are strings, so a renamed story breaks at runtime, not compile time; per test JSX is gone (each case needs a named story); props must be plain serializable data; register `page.route()` mocks before `mount()`.

Default advice: for React and Next.js component tests use Vitest (jsdom for logic, Browser Mode for layout and focus), see `component-and-unit-tests.md`. Use Playwright component testing when the project already has stories and wants one runner for everything.

## 14. Config for Next.js

```ts
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

const PORT = Number(process.env.PORT ?? 3100);
const baseURL = process.env.E2E_BASE_URL ?? `http://localhost:${PORT}`;
const auth = 'playwright/.auth/user.json';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: process.env.CI ? [['github'], ['html', { open: 'never' }]] : 'list',
  expect: { timeout: 7_000 },
  use: {
    baseURL,
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    serviceWorkers: 'block',
  },
  projects: [
    { name: 'setup', testMatch: /.*\.setup\.ts/ },
    { name: 'chromium', use: { ...devices['Desktop Chrome'], storageState: auth }, dependencies: ['setup'] },
    { name: 'webkit', use: { ...devices['Desktop Safari'], storageState: auth }, dependencies: ['setup'] },
    { name: 'mobile', use: { ...devices['Pixel 7'], storageState: auth }, dependencies: ['setup'] },
  ],
  // Production build, not next dev. Skipped when E2E_BASE_URL points at a preview deployment.
  webServer: process.env.E2E_BASE_URL ? undefined : {
    command: `npm run build && npm run start -- -p ${PORT}`,
    url: baseURL,
    reuseExistingServer: !process.env.CI,
    timeout: 180_000,
    stdout: 'ignore',
    stderr: 'pipe',
  },
});
```

Notes:

- `webServer.url` counts as ready on 2xx, 3xx, 400, 401, 402 or 403. Default startup timeout is 60 s; a Next.js build needs more.
- `reuseExistingServer: !process.env.CI` lets the user keep `next start` running locally.
- For a static export (`output: 'export'`), serve the `out/` folder instead: `command: 'npx serve out -l 3100'`.
- Several servers (Next.js plus an API or a local Supabase) go in a `webServer` array, each with its own `url` and `name`.
- `PLAYWRIGHT_TEST=1` is set in the server's environment by default. Do not use it to change app behaviour (no test only branches in production code).
- Running against a Vercel or Netlify preview: set `E2E_BASE_URL` in CI after the deployment, and only run tests that do not write to shared data.
- Lint config (verified rule names in `eslint-plugin-playwright` 2.12.1):
  ```js
  // eslint.config.js
  import playwright from 'eslint-plugin-playwright';
  export default [
    { files: ['e2e/**'], ...playwright.configs['flat/recommended'],
      rules: { ...playwright.configs['flat/recommended'].rules,
        'playwright/no-wait-for-timeout': 'error',
        'playwright/no-networkidle': 'error',
        'playwright/prefer-web-first-assertions': 'error',
        'playwright/no-force-option': 'error',
        'playwright/no-raw-locators': 'warn',
        'playwright/no-skipped-test': 'error',
        'playwright/missing-playwright-await': 'error' } },
  ];
  ```

Never hard code a port or range in a test harness. Read `PORT` or `E2E_PORT`, or `E2E_PORT_RANGE` when the user's rules set a range (the rule's range is the default), else listen on port 0 and read the assigned port; pass the base URL through an env var or `provide()`. The same goes for vitest over HTTP harnesses and node:test servers.

```ts
const port = Number(process.env.E2E_PORT ?? process.env.PORT ?? 3100);
export default defineConfig({
  use: { baseURL: process.env.BASE_URL ?? `http://127.0.0.1:${port}` },
  webServer: { command: `npm run build && npm run start -- -p ${port}`, url: `http://127.0.0.1:${port}` },
});
```

## 15. Anti patterns

| Anti pattern | Why it hurts | Do instead |
|---|---|---|
| `await page.waitForTimeout(2000)` | Too short on a slow CI runner, too long everywhere else | `await expect(locator).toBeVisible()`, `waitForResponse`, `toHaveURL` |
| `page.locator('#root > div:nth-child(2) .btn')` | Breaks on any markup change, says nothing about intent | `getByRole('button', { name: 'Save' })` |
| `.first()` / `.nth(2)` to silence strictness | Clicks whatever happens to be first today | Scope with `filter`, a container, or an exact name |
| `expect(await el.isVisible()).toBe(true)` | No retry, so it races the UI | `await expect(el).toBeVisible()` |
| `{ force: true }` on click | Skips the actionability checks that would reveal an overlay bug | Find why the element is covered or disabled |
| Test B uses the user created in test A | Fails alone, fails in parallel, fails on retry | Fixture creates the data for each test |
| Logging in through the UI in every test | Slow, and one broken login fails the whole suite with a confusing error | Setup project + `storageState` |
| `waitForLoadState('networkidle')` | Never settles with polling or analytics; also hides real readiness bugs | Wait for the element the user needs |
| Testing a third party page (Stripe checkout UI, Google sign in) | You do not control it; it changes and rate limits you | Stub the boundary; test the return URL handling |
| Huge tests covering ten features | One failure hides the other nine | One journey per test, soft assertions for independent checks on one page |
| `try { ... } catch {}` around a step | Turns a failure into a pass | Let it fail; if a step is optional, branch on a known state, not on an exception |
| Accepting healer or codegen output as is | Locators and expectations follow the current UI, not the spec | Review against the spec, add the assertions that matter |
| `test.only`, `test.skip` without an issue link | Silently shrinks the suite | `forbidOnly` in CI; skips need an issue URL |

## 16. Checks

| Check | Pass condition | How |
|---|---|---|
| No fixed waits | 0 hits | `rg -n -e waitForTimeout -e networkidle e2e` |
| User facing locators | CSS / XPath count trending to 0 | `rg -n "locator\(['\"][.#/]" e2e` |
| No manual visibility checks | 0 hits | `rg -n -e "expect\(await .*isVisible\(" -e "expect\(await .*textContent\(" e2e` |
| No force clicks | 0 hits or each justified | `rg -n "force: true" e2e` |
| Focus and skip markers | 0 `only`, each `skip`/`fixme` has an issue link | `rg -n -e "test\.only" -e "test\.skip" -e "test\.fixme" e2e` |
| CI config sane | `forbidOnly`, retries only on CI, `trace: 'on-first-retry'` | `rg -n -e forbidOnly -e retries -e trace playwright.config.*` |
| Production build | `webServer.command` runs `build` and `start` | read `playwright.config.ts` |
| Width probes | a row per route at 1440, 390 and 360 with no horizontal scroll, or a "width not measured" line with the reason | the report |
| No literal ports | every port comes from an env var with a fallback, or port 0 | `rg -n ':[0-9]{4}' e2e tests playwright.config.*` shows only env fallbacks |
| Auth file ignored | `playwright/.auth` in `.gitignore` | `git check-ignore playwright/.auth/user.json` |
| Tests listed | No duplicate titles, expected count | `npx playwright test --list` (no browser) |
| Lint and types | Clean | `npx eslint e2e && npx tsc --noEmit` |
| Independence (CI or with the user's yes) | Passes 5 times shuffled | `npx playwright test --repeat-each=5 --shuffle --retries=0 <new files>` |
| Report kept | Upload step has `if: ${{ !cancelled() }}` | read the workflow |
| Healer or codegen output reviewed | Every changed expected value has a spec reason | read the diff |
