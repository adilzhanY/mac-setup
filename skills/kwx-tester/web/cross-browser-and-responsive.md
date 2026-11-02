# Cross browser and responsive testing

Which browsers, screen sizes, input types and user preferences to test a website or web app on, and how to do it with Playwright projects and emulation: a browser matrix based on real usage, WebKit as the stand in for Safari, a viewport list, touch versus mouse, reduced motion, dark mode, forced colors, 200% zoom, and slow or offline networks. The aim is a small matrix that catches most real breakage, not every combination. Before running any of this yourself, check the user's browser rules (`web.md` section 1); without a browser, hand the user the checklist in section 9.

## Contents

1. Rules
2. Browser matrix by real usage
3. WebKit through Playwright, and real Safari
4. Viewport list
5. Touch versus mouse
6. User preferences: color scheme, motion, contrast, language
7. Zoom 200 percent and text size
8. Slow, flaky and offline networks
9. Checklist for a human when no browser can run
10. Checks

## 1. Rules

1. **Base the matrix on the project's own analytics when it has them; otherwise on global data.** A Kazakh consumer site and a developer tool have very different audiences. Evidence: opinion.
2. **Always include WebKit.** Safari is the second engine by share (18.2% of all browsing in September 2026, StatCounter) and the one that breaks most often for Chromium based developers. Evidence: moderate.
3. **Test mobile first.** 59.06% of worldwide page views were on mobile in September 2026 (StatCounter). Evidence: strong (large scale traffic data).
4. **Run the full journeys on one desktop Chromium project, and a smaller `@smoke` set on the rest.** Cost grows linearly with projects. Evidence: opinion.
5. **Test at breakpoints, not only at device sizes.** Bugs live at 1 px below and above each CSS breakpoint. Evidence: opinion.
6. **Never rely on hover for anything essential.** Touch screens have no hover. Evidence: moderate (WCAG 1.4.13, 2.5 pointer criteria).
7. **Respect user preferences in tests**: dark mode, reduced motion and forced colors are part of the spec, not extras. Evidence: moderate (WCAG, Media Queries Level 5).
8. **Emulation is not a device.** Playwright's mobile projects emulate viewport, scale, touch and user agent, not real phone hardware or real iOS Safari. Keep a short real device checklist for releases. Evidence: moderate (Playwright docs).

## 2. Browser matrix by real usage

StatCounter, worldwide, all platforms, September 2026: Chrome 66.45%, Safari 18.2%, Edge 6.02%, Firefox 2.79%, Samsung Internet 2.31%, Opera 1.77%. Platforms: mobile 59.06%, desktop 39.2%, tablet 1.75%.

By engine (what Playwright can run): Chromium based browsers (Chrome, Edge, Samsung Internet, Opera) are about 76%, WebKit (Safari, plus most browsers on iOS) about 18%, Gecko (Firefox) under 3%.

Default matrix for a solo developer's site or app:

| Tier | Projects | When | Covers |
|---|---|---|---|
| Every PR | `chromium` (Desktop Chrome, full suite), `mobile-safari` (iPhone 15, WebKit, `@smoke`), `mobile-chrome` (Pixel 7, `@smoke`) | CI on every pull request | Chromium desktop and mobile, WebKit mobile: the large majority of real traffic |
| Nightly or before release | + `webkit` (Desktop Safari), `firefox` (Desktop Firefox), `tablet` (iPad Pro 11) | Scheduled CI job | The rest of the engines and the tablet layout |
| Release, by hand | One real iPhone with Safari, one real Android phone with Chrome | The user, from a checklist | Real touch, real fonts, real iOS behaviour (safe areas, address bar, keyboard) |

Adjust: if analytics show Firefox at 10% (common for developer audiences), promote it to every PR. If the site is mostly read on phones, run the full suite on the mobile projects too.

```ts
projects: [
  { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
  { name: 'mobile-safari', use: { ...devices['iPhone 15'] }, grep: /@smoke/ },
  { name: 'mobile-chrome', use: { ...devices['Pixel 7'] }, grep: /@smoke/ },
  { name: 'webkit', use: { ...devices['Desktop Safari'] } },
  { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
  { name: 'tablet', use: { ...devices['iPad Pro 11'] }, grep: /@smoke/ },
],
```

Run one tier with `npx playwright test --project=chromium --project=mobile-safari --project=mobile-chrome`. Since 1.64 a project option can keep the nightly projects out of the default run.

## 3. WebKit through Playwright, and real Safari

- Playwright ships its own WebKit build. It runs on Linux, including in CI, which makes it the cheapest way to catch Safari engine bugs (date input differences, `position: sticky` quirks, flexbox gap and `100vh` issues, missing or newer APIs).
- It is the WebKit engine, not Safari the product: no Apple Pay, no iCloud Keychain, no exact iOS fonts, no real iOS virtual keyboard and toolbar behaviour. Things that pass in Playwright WebKit can still fail on an iPhone, mostly around viewport height, safe area insets, fixed elements when the keyboard opens, and autoplay rules.
- Real iOS testing needs an iPhone, a Mac with the iOS Simulator, or a cloud device service. For a solo developer, a release checklist run on a real phone by the user is usually enough.
- Install only what you run: `npx playwright install --with-deps chromium webkit`.

## 4. Viewport list

| Width x height (CSS px) | Represents | Playwright device |
|---|---|---|
| 320 x 640 | WCAG 1.4.10 reflow width (400% zoom of 1280), smallest phones | custom `viewport` |
| 360 x 780 | Common Android size | `Galaxy S24` |
| 375 x 667 | Small iPhone | `iPhone SE (3rd gen)` |
| 393 x 659 | Current iPhone (viewport minus browser chrome) | `iPhone 15` |
| 412 x 839 | Pixel class Android | `Pixel 7` |
| 768 x 1024 | Tablet portrait, a common `md` breakpoint | custom or iPad |
| 834 x 1194 | iPad Pro 11 portrait | `iPad Pro 11` |
| 1024 x 768 | Small laptop or tablet landscape, a common `lg` breakpoint | custom |
| 1280 x 720 | Laptop, Playwright desktop default | `Desktop Chrome` |
| 1440 x 900 | Common laptop | custom |
| 1920 x 1080 | Desktop monitor | custom |

Device sizes verified in the Playwright 1.64.1 registry (`require('playwright-core').devices`).

Breakpoint test: read the breakpoints from the CSS or Tailwind config (Tailwind defaults: `sm` 640, `md` 768, `lg` 1024, `xl` 1280, `2xl` 1536) and check the layout at `breakpoint - 1` and `breakpoint`:

```ts
for (const width of [639, 640, 767, 768, 1023, 1024]) {
  test(`no horizontal overflow at ${width}px @smoke`, async ({ page }) => {
    await page.setViewportSize({ width, height: 900 });
    await page.goto('/');
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
    expect(overflow, `page is ${overflow}px wider than the viewport`).toBe(0);
    await expect(page.getByRole('navigation', { name: 'Main' })).toBeVisible(); // or the menu button below md
  });
}
```

Things to look for at each size: horizontal scroll, text overlapping or cut off, buttons wrapping into two lines, sticky headers covering content, images stretched, the navigation switching to a menu button at the right width, tap targets at least 24 px.

## 5. Touch versus mouse

- Mobile device presets set `isMobile: true` and `hasTouch: true`. `locator.tap()` works only with `hasTouch`. A desktop project with `hasTouch: true` models a touch laptop.
- Hover only UI breaks on touch: menus that open on hover, tooltips that hold essential info, buttons that appear on row hover. Test the same flow in a touch project and assert it is possible without hover.
- Check the CSS media features the app uses in the project being tested, instead of assuming:
  ```ts
  const media = await page.evaluate(() => ({ hover: matchMedia('(hover: hover)').matches, coarse: matchMedia('(pointer: coarse)').matches }));
  ```
- Gestures (swipe, pinch, long press): Playwright has `tap` and low level `touchscreen.tap`. Swipe needs dispatched touch events or the mouse API. Prefer testing the non gesture alternative, which WCAG 2.5.1 and 2.5.7 require anyway.
- The on screen keyboard is not emulated. Fixed bottom bars that jump or cover inputs when the keyboard opens are a real device check.

## 6. User preferences: color scheme, motion, contrast, language

Playwright context options (names checked in the 1.64.1 type definitions): `colorScheme` (`'light' | 'dark' | 'no-preference'`), `reducedMotion` (`'reduce' | 'no-preference'`), `forcedColors` (`'active' | 'none'`), `contrast` (`'more' | 'no-preference'`), `locale`, `timezoneId`.

```ts
test.describe('dark mode', () => {
  test.use({ colorScheme: 'dark' });
  test('pricing page uses the dark palette and stays readable', async ({ page, makeAxeBuilder }) => {
    await page.goto('/pricing');
    await expect(page.locator('html')).toHaveCSS('color-scheme', /dark/);   // or the app's own theme attribute
    expect((await makeAxeBuilder().analyze()).violations).toEqual([]);     // contrast in dark mode
  });
});

test.describe('reduced motion', () => {
  test.use({ reducedMotion: 'reduce' });
  test('hero animation does not run', async ({ page }) => {
    await page.goto('/');
    await expect(page.getByTestId('hero-art')).toHaveCSS('animation-name', 'none');
  });
});
```

- A manual theme toggle and the system preference must agree: test system dark with no stored choice, then the toggle, then a reload (the choice persists, no flash of the wrong theme on load).
- Switch mid test with `await page.emulateMedia({ colorScheme: 'dark' })` to test live theme changes.
- `forcedColors: 'active'` (Windows high contrast): icons drawn with `background-image` and focus rings drawn with `box-shadow` often vanish. Check the key controls are still visible and focus is still shown.
- Locale and timezone: `test.use({ locale: 'kk-KZ', timezoneId: 'Asia/Almaty' })` for date, number and currency formats. Right to left: if the app supports Arabic or Hebrew, run the smoke set with `locale: 'ar'` and check `dir="rtl"` layouts.
- Long and non Latin text: run one test with the longest real translation and with Cyrillic and Kazakh specific letters (ә, ғ, қ, ң, ө, ұ, ү, һ, і) to catch missing font glyphs and overflow.

## 7. Zoom 200 percent and text size

WCAG 1.4.4 asks for text resizable to 200% without loss of content or function; 1.4.10 asks for reflow at 320 CSS px. Playwright cannot press the browser's zoom, but zoom is equivalent to a smaller CSS viewport at a higher device scale factor:

```ts
test.describe('200% zoom on a 1280 px window', () => {
  test.use({ viewport: { width: 640, height: 400 }, deviceScaleFactor: 2 });
  test('checkout is usable', async ({ page }) => {
    await page.goto('/checkout');
    await expect(page.getByRole('button', { name: 'Pay' })).toBeInViewport({ ratio: 1 });
    // ...walk the flow; nothing may be cut off or require horizontal scroll
  });
});
```

Text only zoom (Firefox setting, also Android font size): set a larger root font size and check nothing clips. It only works if the CSS uses `rem` or `em`; fixed `px` font sizes that do not grow are themselves the finding.

```ts
await page.addStyleTag({ content: 'html { font-size: 200% !important }' });
```

## 8. Slow, flaky and offline networks

Playwright has no built in throttling option. Choose by what you want to prove:

| Goal | Method |
|---|---|
| Loading states and skeletons appear, no double submit | Delay one endpoint in a route handler: `await page.route('**/api/orders', async r => { await new Promise(res => setTimeout(res, 3000)); await r.continue(); })` |
| Offline banner, retry, service worker cache | `await context.setOffline(true)`, act, then `setOffline(false)` |
| Whole page on a slow mobile link (Chromium only) | CDP: see below |
| Performance budgets on a slow link | Lighthouse (simulated throttling, mobile default about 150 ms RTT and 1.6 Mbps, 4x CPU slowdown); see `performance-and-seo-checks.md` |

Chromium only, through the DevTools protocol:

```ts
test('product page is usable on a slow 3G class link', async ({ page, browserName }) => {
  test.skip(browserName !== 'chromium', 'CDP throttling is Chromium only');
  const cdp = await page.context().newCDPSession(page);
  await cdp.send('Network.emulateNetworkConditions', {
    offline: false, latency: 400, downloadThroughput: (400 * 1024) / 8, uploadThroughput: (400 * 1024) / 8,
  });
  await cdp.send('Emulation.setCPUThrottlingRate', { rate: 4 });
  await page.goto('/product/1', { timeout: 60_000 });
  await expect(page.getByRole('button', { name: 'Add to cart' })).toBeEnabled({ timeout: 30_000 });
});
```

Keep throttled tests few and out of the per PR set; they are slow by design. The goal is behaviour (nothing breaks, the user sees progress), not timing numbers, which belong to Lighthouse with repeated runs.

## 9. Checklist for a human when no browser can run

When the agent may not run a browser, give the user this, trimmed to what the change touched:

```text
Please check on the dev or preview URL:
[ ] Phone width (about 360 px, or a real phone): no sideways scrolling, menu opens, main button visible
[ ] Tablet width (about 768 px): layout switches cleanly, nothing overlaps
[ ] Desktop (1280 px and 1920 px): content not stretched, header correct
[ ] Dark mode (system setting): text readable, no white flashes on load
[ ] Reduced motion (system setting): big animations stop
[ ] Zoom to 200% (Ctrl and +): nothing cut off, can still reach every button
[ ] Safari or an iPhone if you have one: the changed page loads and the main action works
[ ] Keyboard only: Tab through the changed part, focus visible, Enter and Escape work
```

Say in the report that these were not verified by the agent.

## 10. Checks

| Check | Pass condition | How |
|---|---|---|
| Matrix matches audience | Projects reflect analytics or the default tiers | read `playwright.config.ts` and the analytics summary |
| WebKit present | At least one WebKit project runs per PR | `rg -n -e "iPhone" -e "Desktop Safari" playwright.config.*` |
| Mobile first | A mobile Chromium and a mobile WebKit project exist | read the config |
| Breakpoints covered | Overflow test at each breakpoint minus 1 and at it | list the widths in the test |
| Touch path | Essential actions work in a `hasTouch` project without hover | read the smoke tests |
| Preferences | Dark mode, reduced motion and forced colors tests exist for themed or animated UI | `rg -n -e colorScheme -e reducedMotion -e forcedColors e2e` |
| Zoom | 640 px at scale 2 (200% of 1280) test for the main flow | `rg -n "deviceScaleFactor: 2" e2e` |
| Slow and offline | Loading and offline states tested | `rg -n -e setOffline -e emulateNetworkConditions -e "route(" e2e` |
| Real device | Release checklist includes one real iPhone and one real Android pass, done by a person | the release notes |
| Unverified parts reported | Report lists what was not run | the report |
