# Visual regression testing

Visual regression tests take a screenshot, compare it with an approved baseline image and fail when pixels change. They catch what functional tests cannot see: a broken layout, a missing font, a button that moved under another element, a dark mode color that went wrong. They are also the most expensive tests to keep stable and the easiest to make meaningless by updating baselines without looking. This file covers Playwright `toHaveScreenshot`, Vitest `toMatchScreenshot` for components, thresholds, how to stabilise fonts, animations and dynamic content, hosted services (Chromatic, Percy, Argos, and the now archived Lost Pixel), and the review rules for baseline changes.

## Contents

1. Rules
2. When visual tests pay off
3. Playwright toHaveScreenshot
4. Stabilising the page
5. Thresholds
6. Updating baselines: the review rules
7. Component screenshots with Vitest
8. Hosted services
9. Cheaper alternatives: ARIA snapshots and computed style checks
10. When the agent cannot open a browser
11. Checks

## 1. Rules

1. **Generate and compare baselines in one pinned environment**: the same Linux Docker image in CI and for local updates. Playwright: "Browser rendering can vary based on the host OS, version, settings, hardware, power source." Never commit baselines made on a laptop next to baselines made in CI. Evidence: moderate (Playwright and Vitest docs).
2. **Never update a baseline without opening the diff image.** Every updated baseline is listed in the report with a one line reason linked to the spec or the request. Evidence: moderate (Vitest docs: "Review updated screenshots before committing"; kwx-developer tests-and-honesty).
3. **Stabilise before you capture**: fonts loaded, animations off (Playwright default), caret hidden (default), mouse moved away, dynamic content masked or frozen, data fixed. Evidence: moderate.
4. **Do not raise the threshold to silence a failure.** Find the cause of the noise. A threshold set high enough to pass every time also passes real regressions. Evidence: opinion.
5. **Screenshot a few stable, high value views, not every page.** Each screenshot is a maintenance cost. Prefer component or region screenshots over full pages. Evidence: opinion, shared by most vendor guides.
6. **Visual tests do not replace functional or a11y assertions.** A screenshot cannot tell you a button works or has an accessible name. Evidence: opinion.

## 2. When visual tests pay off

| Good fit | Poor fit |
|---|---|
| Design system components (buttons, inputs, cards) in each state and theme | Pages full of live data, ads, maps, video |
| Landing page hero and pricing table that must not shift | Screens that change every sprint |
| Dark mode, RTL, long text and Cyrillic or Kazakh text rendering | Anything you cannot make deterministic |
| CSS refactors and dependency upgrades (Tailwind, a UI kit) | Animations themselves (test the end state) |
| Charts and canvas output, where DOM assertions see nothing | Checking a value that a text assertion can check |

## 3. Playwright toHaveScreenshot

```ts
test('pricing table matches the approved design', async ({ page }) => {
  await page.goto('/pricing');
  await expect(page.getByRole('heading', { name: 'Pricing' })).toBeVisible();
  await expect(page.getByRole('table', { name: 'Plans' })).toHaveScreenshot('pricing-table.png');
});
```

- The first run writes the baseline and fails. Review the image, then run again.
- Baselines live in `<test file>-snapshots/`, named `<name>-<project>-<platform>.png` (for example `pricing-table-chromium-linux.png`). Each browser and OS needs its own baseline. Change the layout with `snapshotPathTemplate`.
- `toHaveScreenshot` retries: it takes screenshots until two in a row match, then compares with the baseline. So it waits for the page to settle, within the assertion timeout.
- Prefer a locator screenshot over `page` and over `fullPage: true`. Smaller images mean less noise and clearer diffs.

Options (page and locator variants, Playwright API reference):

| Option | Default | Use |
|---|---|---|
| `animations` | `'disabled'` | Finite animations jump to the end ("fast-forwarded to completion"), infinite ones reset. Keep the default |
| `caret` | `'hide'` | Hides the text cursor. Keep |
| `mask` | none | Array of locators painted over (default color `#FF00FF`). For clocks, avatars, random content |
| `maskColor` | `#FF00FF` | |
| `stylePath` | none | A CSS file injected for the screenshot, to hide volatile parts (`iframe { visibility: hidden }`) |
| `threshold` | `0.2` | Per pixel color tolerance, 0 strict to 1 lax (YIQ color space) |
| `maxDiffPixels` | unset | How many pixels may differ |
| `maxDiffPixelRatio` | unset | Share of pixels that may differ (0 to 1) |
| `fullPage` | `false` | Whole scrollable page |
| `scale` | `'css'` | One image pixel per CSS pixel, so DPR differences do not change the size |
| `omitBackground` | `false` | Transparent background |
| `clip` | none | A rectangle |
| `timeout` | expect timeout | |

Project wide defaults:

```ts
// playwright.config.ts
export default defineConfig({
  expect: {
    toHaveScreenshot: { maxDiffPixelRatio: 0.001, stylePath: './e2e/screenshot.css' },
  },
  // keep visual tests in their own project so the matrix stays small
  projects: [
    { name: 'visual', testMatch: /.*\.visual\.spec\.ts/, use: { ...devices['Desktop Chrome'], viewport: { width: 1280, height: 800 } } },
  ],
});
```

## 4. Stabilising the page

Visual tests flake for a handful of reasons. Fix each at the source:

| Source of noise | Fix |
|---|---|
| Different OS, fonts, GPU between machines | Run in the official image pinned to your Playwright version, `mcr.microsoft.com/playwright:v1.64.1-noble`, for CI and for updates. On Arch, the desktop's fonts and hinting differ from the Ubuntu image, so local runs outside Docker will never match |
| Web font not loaded yet (fallback font captured) | Self host fonts (`next/font` does this). Wait before capturing: `await page.evaluate(() => document.fonts.ready)`. A font that 404s in CI produces baselines that never match locally: check the network panel of the trace |
| Text anti aliasing differences | Launch Chromium with `args: ['--font-render-hinting=none', '--disable-lcd-text']` (from the Argos docs; reduces sub pixel differences) |
| Animations, transitions, carousels | Default `animations: 'disabled'`; also emulate `reducedMotion: 'reduce'` and make sure the app honours it; stop carousels by test hook or freeze time |
| Hover and focus left from the last action | `await page.mouse.move(-1, -1)` (Playwright docs) or blur the active element before capturing |
| Clock, relative dates ("3 minutes ago") | `await page.clock.setFixedTime(new Date('2026-03-01T10:00:00Z'))` before `goto`, and fixed `timezoneId` and `locale` |
| Random data, avatars, ads, maps, embeds | Fixed seed data; `mask: [locator]`; route third party embeds to an empty response |
| Lazy images not loaded | Scroll the image into view, then wait until it has loaded: `await expect.poll(() => img.evaluate((el: HTMLImageElement) => el.complete && el.naturalWidth > 0)).toBe(true)` |
| Scrollbars appearing | Hide them in the `stylePath` CSS: `::-webkit-scrollbar { display: none }` and `html { scrollbar-width: none }` |
| Different viewport or DPR | Set `viewport` and keep `scale: 'css'` |
| Toasts, cookie banners | Dismiss them in a fixture, or set the consent cookie in `storageState` |

A small helper keeps tests short:

```ts
// e2e/visual.ts
import type { Page } from '@playwright/test';
export async function settle(page: Page) {
  await page.evaluate(() => document.fonts.ready);
  await page.mouse.move(-1, -1);
}
```

## 5. Thresholds

- Start strict: `threshold: 0.2` (default) and `maxDiffPixelRatio: 0.001` or a small `maxDiffPixels` for component shots. Strict defaults find the noise sources early, when they are cheap to fix.
- If a test is noisy, find the cause in the diff image (the trace and the HTML report show expected, actual and diff side by side). Most noise is fonts, anti aliasing at edges, or an unmasked dynamic area.
- Loosen per assertion, never globally, and write why next to it:
  ```ts
  // Chart lines are anti aliased differently between runs on the same image; 50 px is the measured noise.
  await expect(chart).toHaveScreenshot('revenue-chart.png', { maxDiffPixels: 50 });
  ```
- A useful sanity check after tuning: change something real (1 px of padding, a color token) and confirm the test fails. If it does not, the threshold is too loose. Evidence: opinion.

## 6. Updating baselines: the review rules

Update modes in 1.64.1 (verified with `npx playwright test --help`): `-u` / `--update-snapshots` takes `all`, `changed` (the preset when the flag has no value), `missing`, `none`, `default`. Since 1.64, `missing` writes absent baselines and lets the run pass; without the flag (`default`), missing baselines are written but the test fails.

Update inside the same image CI uses:

```bash
# from the repo root; the webServer in playwright.config.ts starts the app inside the container
docker run --rm --ipc=host -v "$PWD":/work -w /work mcr.microsoft.com/playwright:v1.64.1-noble \
  /bin/bash -c "npm ci && npx playwright test --project=visual --update-snapshots=changed"
```

(Command shape from the Playwright Docker docs, not run here because it starts a browser.) Or add a manually triggered CI workflow that runs the update and commits the images to the branch, as the Vitest docs suggest.

Review rules for every baseline change, for the agent and for a human reviewer:

1. **Open the diff, not just the new image.** Look at what moved, not whether the new picture looks fine on its own.
2. **Each changed image has a reason**: a line in the request, the spec, or a design change the user approved. "The test failed" is not a reason.
3. **Unexpected differences are bugs until proven otherwise.** A diff in a screen the change did not touch means a shared style moved. Investigate before accepting.
4. **Only `changed`, never `all`,** unless the whole baseline set is being regenerated on purpose (new image version), and then in a separate commit that changes nothing else.
5. **Keep baseline updates in their own commit** with the reason in the message, so `git log` shows when and why the design changed.
6. **Delete stale baselines** of renamed or removed tests (Vitest and Playwright do not always clean them up).
7. **The agent never accepts its own visual change as correct without the user seeing it** when the change is a design change. List the updated images in the report and ask the user to look at them.

## 7. Component screenshots with Vitest

Vitest Browser Mode has `toMatchScreenshot` built in (vitest.dev visual regression guide). Baselines go to `__screenshots__/` next to the test, named with test, browser and platform.

```tsx
import { expect, test } from 'vitest';
import { page } from 'vitest/browser';
import { render } from 'vitest-browser-react';
import { Button } from './Button';

test('primary button, disabled state', async () => {
  await render(<Button variant="primary" disabled>Save</Button>);
  await expect(page.getByRole('button', { name: 'Save' })).toMatchScreenshot();
});
```

- Comparator: `pixelmatch`, options `comparatorOptions.threshold`, `allowedMismatchedPixelRatio` (recommended over a fixed count), `allowedMismatchedPixels`. Vitest sets no pixel tolerance by default.
- Same environment rule as Playwright: Docker or CI only for references. Updating locally "defeats the controlled environment".
- Update with `vitest --project <visual project> --update`, then review.

## 8. Hosted services

Hosted services render or store screenshots in the cloud and give a review UI where a person approves each change. That review step is the main value for a team; for a solo developer, Playwright's built in comparison plus the review rules above is usually enough.

| Service | How it works | Notes (checked 2026-10) |
|---|---|---|
| **Argos** (`@argos-ci/playwright` 7.8.0) | `argosScreenshot(page, 'name')` in Playwright tests, uploads in CI, review in the Argos UI | Stabilises by default: waits for fonts and images, `aria-busy`, pauses SVG and GIF animations, hides carets and scrollbars, handles sticky elements. Open source core. Needs Node 22 |
| **Chromatic** (`@chromatic-com/playwright` 1.0.0) | Replace the `test` import with Chromatic's; it archives DOM, CSS and assets during the test and renders snapshots in its cloud | Strong Storybook integration; TurboSnap does not apply to Playwright. Needs Chrome in the config |
| **Percy** (BrowserStack, `@percy/playwright` 1.1.2) | `percySnapshot(page, 'name')`, renders the DOM in several browsers in the cloud | Cross browser rendering in the cloud |
| **Applitools Eyes** | AI based comparison that ignores rendering noise | Commercial |
| **Lost Pixel** | Open source, Storybook, Ladle, pages or custom shots | **Archived and read only**: the team announced it is sunsetting the product. Do not start new projects on it; migrate existing ones |

Choose a hosted service only if: several people approve designs, or you need many browsers rendered in the cloud, or local Docker baselines are too slow. Check its current free tier and data policy (screenshots of a private app leave your machine).

## 9. Cheaper alternatives: ARIA snapshots and computed style checks

Before adding a screenshot, ask whether a cheaper, more stable assertion proves the same thing:

- **Structure and labels**: `toMatchAriaSnapshot` (see `playwright.md` section 2). It catches a missing heading, a reordered nav or a lost label, and does not break on a color change.
- **One CSS property**: `await expect(banner).toHaveCSS('position', 'sticky')`.
- **Element is on screen, not covered**: `await expect(cta).toBeInViewport()` plus a click (actionability checks fail if another element covers it).
- **Nothing overflows horizontally at 360 px**:
  ```ts
  await page.setViewportSize({ width: 360, height: 800 });
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
  expect(overflow).toBe(0);
  ```

## 10. When the agent cannot open a browser

If the user's rules turn browser automation off, the agent cannot create or compare screenshots. Then:

1. Write the visual tests and the stable fixtures into the project as normal.
2. Do not create baselines. Say that the first CI run (or the user's local Docker run) will create them, and that someone must review them.
3. When a change could alter the look, give the user a short checklist: which pages, which viewport widths, light and dark, what to look for ("the price column should not wrap at 360 px").
4. Never claim that a page "looks right" when no one rendered it.

## 11. Checks

| Check | Pass condition | How |
|---|---|---|
| Pinned environment | CI and baseline updates use the same Playwright image tag as `@playwright/test` | compare `npm ls @playwright/test` with the workflow's image tag |
| Baseline platform | All baselines end in `-linux.png` (or the CI platform) | `ls e2e/**/*-snapshots/` |
| Fonts stable | Fonts self hosted, `document.fonts.ready` awaited before capture | read the visual helper |
| Dynamic content handled | Time frozen, data fixed, volatile parts masked | read each visual test |
| Thresholds local and justified | No global loose threshold; each loosened assertion has a comment with the measured noise | `rg -n -e maxDiffPixels -e threshold e2e playwright.config.*` |
| Baseline updates reviewed | Every changed image listed in the report with a reason | `git diff --stat -- '*-snapshots/*' '__screenshots__/*'` |
| No mass update | No `--update-snapshots=all` in scripts or CI except a deliberate regeneration job | `rg -n "update-snapshots" package.json .github` |
| Stale baselines removed | No images without a matching test | compare snapshot names with test titles |
| Not on archived tooling | No `lost-pixel` in new setups | `rg -n lost-pixel package.json` |
