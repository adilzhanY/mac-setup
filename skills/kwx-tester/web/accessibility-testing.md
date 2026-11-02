# Accessibility testing for the web

How to test that a website or web app works for people who use a keyboard, a screen reader, zoom, high contrast or reduced motion. Automated scans (axe-core in Playwright and in component tests, HTML linting) catch a real but limited share of problems; the studies below put numbers on that share. The rest needs short manual passes: keyboard only, focus order, a screen reader smoke test, zoom and reflow. This file gives the tools, the data, the manual scripts, and the WCAG 2.2 criteria a tester checks. Design rules for accessible UI belong to kwx-designer; this file is about proving them.

## Contents

1. Rules
2. What automated tools catch and miss: the studies
3. axe-core in Playwright
4. axe in component tests
5. Browserless checks: lint and HTML validation
6. Keyboard only pass
7. Focus order, visible focus, focus management
8. Screen reader smoke test
9. Zoom, reflow, text spacing, contrast, motion
10. WCAG 2.2 criteria a tester checks
11. When the agent cannot open a browser
12. Checks

## 1. Rules

1. **Run axe on every main screen in every main state** (empty, filled, error, dialog open, menu open), not only on page load. Most a11y bugs live in states a load time scan never sees. Evidence: moderate (Playwright a11y docs show scanning after interaction).
2. **Treat a clean axe result as "no machine detectable failures", never as "accessible".** Automated testing covered about 57% of issues by volume in Deque's data, and 29% of the barriers on GOV.UK's test page were missed by all 10 tools tested. Evidence: strong.
3. **Do a keyboard only pass on every new interactive component.** Tab to it, use it, leave it, without a mouse. Evidence: moderate (WCAG 2.1.1, 2.1.2, 2.4.3, 2.4.7).
4. **Do a screen reader smoke pass on each new flow**, using the headings list first: 71.6% of screen reader users navigate long pages by headings (WebAIM survey #10). Evidence: strong (survey, 1,539 respondents, self selected).
5. **Use role based queries in tests** (`getByRole` with a name). A test that cannot find the button by role has found an a11y bug. Evidence: moderate.
6. **Prefer native HTML over ARIA, and test that ARIA is not added on top of native semantics.** Pages with ARIA averaged 59.1 detected errors against 42 without (WebAIM Million 2026; correlation, the pages were also more complex). Evidence: strong for the correlation, moderate for the advice.
7. **Do not suppress an axe rule globally to get green.** Exclude a specific element or rule with a comment and an issue link, and keep a snapshot of known violations so new ones still fail. Evidence: moderate (Playwright a11y docs).
8. **Contrast needs a real browser.** axe's `color-contrast` rule does not work in jsdom (axe-core and jest-axe docs). Low contrast text is the most common failure on the web (83.9% of home pages, WebAIM Million 2026). Evidence: strong.

## 2. What automated tools catch and miss: the studies

| Study | What was measured | Result |
|---|---|---|
| Deque, "Automated testing study identifies 57 percent of digital accessibility issues" (March 2021) | 2,000+ audits, 13,000+ pages, nearly 300,000 issues, first time assessments, axe tools | **57%** of issues by volume "completely covered" by automated testing. Vendor data. Counted by issue volume, so frequent issue types (contrast, alt text) push the number up |
| Same study, framing | The "widely accepted belief" | 20 to 30% coverage, measured by share of WCAG success criteria a tool can test. Deque gives no source for this figure |
| GOV.UK Government Digital Service, "What we found when we tested tools on the world's least accessible webpage" (Feb 2017) | A test page with **143 barriers** in 19 categories, **10 free tools** | All tools together found **71%**; **29% were missed by every tool**. Best single tool: 37% (Tenon, errors and warnings), 41% (Asqatasun, counting manual prompts). Worst: 17%. Data: alphagov.github.io/accessibility-tool-audit |
| GOV.UK accessibility tool audit page (updated 13 April 2018) | Same idea, re run: **142 barriers**, **13 tools** | Best single tool SortSite 40%; axe 29% (30% counting potential barriers); WAVE 30% (39%); lowest Nu Html Checker 13%. Counting potential barriers, the best was FAE at 50%. No single tool came near half on confirmed barriers |
| axe-core README | The engine | "on average 57% of WCAG issues automatically"; "zero false positives (bugs notwithstanding)"; returns "incomplete" results that need manual review |
| WebAIM Million (2026, February data) | Home pages of the top 1,000,000 sites, automated WAVE scan | **95.9%** had detected WCAG failures, 56.1 errors per page on average. Six types made up **96%** of all errors: low contrast text 83.9%, missing alt text 53.1%, missing form labels 51%, empty links 46.3%, empty buttons 30.6%, missing document language 13.5% |

What this means for a tester:

- Automated tools are very good at the six common failure types. Run them always; they are cheap.
- They cannot judge meaning: whether alt text describes the image, whether the focus order makes sense, whether an error message helps, whether a custom widget works with a screen reader, whether content is understandable. GOV.UK's misses included links identified by color alone and tables with empty cells.
- So the minimum for any new UI is: axe scan + keyboard pass + screen reader smoke pass. Evidence: strong.

## 3. axe-core in Playwright

Install: `npm install -D @axe-core/playwright` (4.14.0, verified version 2026-10-31). Running these tests opens a browser: check the user's browser rules first.

A shared fixture so every file uses the same rules:

```ts
// e2e/axe.ts
import { test as base, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

export const test = base.extend<{ makeAxeBuilder: () => AxeBuilder }>({
  makeAxeBuilder: async ({ page }, use) => {
    await use(() =>
      new AxeBuilder({ page })
        .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'])
        // .exclude('#third-party-chat')  // only with a comment and an issue link
    );
  },
});
export { expect };
```

Scan in each state, attach the full result, assert on violations:

```ts
import { test, expect } from './axe';

test('sign up form has no detectable a11y violations, before and after errors', async ({ page, makeAxeBuilder }, testInfo) => {
  await page.goto('/signup');
  let results = await makeAxeBuilder().analyze();
  expect(results.violations).toEqual([]);

  await page.getByRole('button', { name: 'Create account' }).click();       // trigger validation errors
  await expect(page.getByText('Email is required')).toBeVisible();
  results = await makeAxeBuilder().include('form').analyze();
  await testInfo.attach('axe-results', { body: JSON.stringify(results, null, 2), contentType: 'application/json' });
  expect(results.violations).toEqual([]);
});
```

Readable failures: the raw `violations` array is long. Map it before asserting so the report says what to fix:

```ts
const summary = results.violations.map(v => `${v.id} (${v.impact}): ${v.help} -> ${v.nodes.map(n => n.target.join(' ')).join(', ')}`);
expect(summary).toEqual([]);
```

Existing site with many known issues: do not disable rules. Snapshot a fingerprint of the known violations (rule id and target, not the HTML) so the suite fails on new ones while the backlog is fixed:

```ts
const fingerprints = results.violations.map(v => ({ rule: v.id, targets: v.nodes.map(n => n.target) }));
expect(JSON.stringify(fingerprints, null, 2)).toMatchSnapshot('known-a11y-violations.json');
```

Notes:

- `incomplete` results are items axe could not decide (often contrast over images or gradients). List them in the report for a manual look; do not ignore them.
- Scan dialogs, menus, toasts and error states after opening them. Scope with `.include('[role="dialog"]')`.
- Run scans in both color schemes: `test.use({ colorScheme: 'dark' })`. Dark mode contrast bugs are common.
- The `target-size` rule (WCAG 2.5.8) is tagged `wcag22aa`; that is why the tag is in the list.

For every page, the header nav link for the current page has `aria-current="page"`, and every required input exposes `required` or `aria-required="true"`. axe reports neither, so write the assertion. List the inputs the spec marks as required and assert each one by its label; the loop over marked fields catches the rest. Name the nav (`getByRole('navigation')` alone is a strict mode error on a page with a header nav and a footer nav).

```ts
const isRequired = (el: Element) => (el as HTMLInputElement).required || el.getAttribute('aria-required') === 'true';
await expect(page.getByRole('navigation', { name: /main|primary/i }).getByRole('link', { name: 'Pricing' })).toHaveAttribute('aria-current', 'page');
for (const label of ['Email', 'Company name']) {            // the required fields from the spec
  expect(await page.getByLabel(label).evaluate(isRequired), `${label} is required`).toBe(true);
}
for (const field of await page.locator('form [data-required], form input[aria-required], form input[required]').all()) {
  expect(await field.evaluate(isRequired)).toBe(true);
}
```

## 4. axe in component tests

`jest-axe` (11.0.0) works with Jest and, in practice, with Vitest's `expect.extend`. In jsdom, `color-contrast` is turned off because it does not work there.

```ts
import { axe, toHaveNoViolations } from 'jest-axe';
expect.extend(toHaveNoViolations);

test('Dialog has no detectable a11y violations when open', async () => {
  const { baseElement } = render(<ConfirmDialog open title="Delete project?" />);
  expect(await axe(baseElement, { rules: { region: { enabled: false } } })).toHaveNoViolations();
});
```

- Disable the `region` rule for isolated components (they are not inside landmarks in a test), per jest-axe docs.
- With fake timers, axe can time out: switch to real timers around the `axe` call.
- Component scans are fast and run without a browser, so an agent can always run them. They miss contrast, layout, focus visibility and anything CSS driven. Pair them with Playwright scans in CI.
- In Vitest Browser Mode, run axe in the real browser (contrast works there).

## 5. Browserless checks: lint and HTML validation

These run with no browser at all, so they are the agent's first line when browsers are off.

- `eslint-plugin-jsx-a11y` (`plugin:jsx-a11y/recommended`, or `strict`): missing alt, click handlers on non interactive elements, missing labels, invalid ARIA, autofocus.
- `html-validate` with the `a11y` preset on built HTML (`out/` or a curl'd page):
  ```bash
  npx html-validate --preset recommended,a11y "out/**/*.html"
  ```
  Verified on a fixture: it flagged `<img> is missing required "alt" attribute (wcag/h37)` and `<html> is missing required "lang" attribute`. It does not check heading structure or contrast.
- The curl smoke test in `browser-automation-for-agents.md` section 7 checks `lang`, one `h1`, `img` without `alt` and anchor targets.

## 6. Keyboard only pass

Do it on every new interactive component and flow. As a Playwright test where the browser is allowed, otherwise as a user checklist.

1. Put the mouse away. Load the page and press Tab. The first stop should be a "Skip to content" link (if the site has repeated navigation) and it must be visible when focused.
2. Tab through everything. Every interactive element is reachable (2.1.1), in an order that matches the visual and reading order (2.4.3), and nothing that is not interactive gets focus.
3. Focus is always visible (2.4.7) and never fully hidden behind a sticky header, cookie banner or chat bubble (2.4.11, new in 2.2).
4. Operate each control: Enter on links and buttons, Space on buttons and checkboxes, arrow keys inside radio groups, menus, tabs, sliders, listboxes, Escape closes menus and dialogs.
5. No keyboard trap (2.1.2): you can always Tab or Escape out, including from embedded widgets and editors.
6. Dialogs: focus moves into the dialog on open, Tab cycles inside it, Escape closes it, focus returns to the button that opened it.
7. After a client side route change or a form submit, focus goes somewhere sensible (the new page heading, the first error), and the change is announced.
8. Single key shortcuts can be turned off or remapped, or only work when the component has focus (2.1.4).

A Playwright test for the dialog part:

```ts
test('delete dialog traps focus and returns it on Escape', async ({ page }) => {
  await page.goto('/projects/p1/settings');
  const trigger = page.getByRole('button', { name: 'Delete project' });
  await trigger.click();
  const dialog = page.getByRole('dialog', { name: 'Delete project?' });
  await expect(dialog.getByRole('button', { name: 'Cancel' })).toBeFocused();
  await page.keyboard.press('Tab');
  await expect(dialog.getByRole('button', { name: 'Delete' })).toBeFocused();
  await page.keyboard.press('Tab');
  await expect(dialog.getByRole('button', { name: 'Cancel' })).toBeFocused(); // wrapped, did not escape
  await page.keyboard.press('Escape');
  await expect(dialog).toBeHidden();
  await expect(trigger).toBeFocused();
});
```

## 7. Focus order, visible focus, focus management

A tab order test that records every stop, useful as a regression check on a form or a header:

```ts
test('header tab order follows the visual order', async ({ page }) => {
  await page.goto('/');
  const stops: string[] = [];
  for (let i = 0; i < 8; i++) {
    await page.keyboard.press('Tab');
    stops.push(await page.evaluate(() => {
      const el = document.activeElement as HTMLElement | null;
      return `${el?.tagName.toLowerCase()}:${el?.getAttribute('aria-label') ?? el?.textContent?.trim()}`;
    }));
  }
  expect(stops).toEqual(['a:Skip to content', 'a:Torq', 'a:Features', 'a:Pricing', 'a:Docs', 'a:Sign in', 'a:Get started', 'a:Start free trial']);
});
```

Write the expected list from the design or spec, not from the current output.

Visible focus: assert that the focused element has an outline or ring, for example `await expect(link).toHaveCSS('outline-style', 'solid')` after focusing it with the keyboard (`:focus-visible` applies only after keyboard focus, so press Tab, do not call `focus()`). Focus not obscured: after tabbing to an element near the bottom, check it is in the viewport and not under a fixed element:

```ts
await expect(page.locator(':focus')).toBeInViewport();
const covered = await page.evaluate(() => {
  const el = document.activeElement as HTMLElement; const r = el.getBoundingClientRect();
  const top = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2);
  return !(top === el || el.contains(top));
});
expect(covered, 'focused element is covered by another element').toBe(false);
```

## 8. Screen reader smoke test

Agents cannot listen to a screen reader. This is always a manual pass for the user or a tester; the agent writes the script.

Which screen reader (WebAIM survey #10, Dec 2023 to Jan 2024, 1,539 respondents): primary desktop readers JAWS 40.5%, NVDA 37.7%, VoiceOver 9.7%, Orca 2.4%. Any use: NVDA 65.6%, JAWS 60.5%, VoiceOver 43.9%. Mobile: VoiceOver 70.6%, TalkBack 34.7%. Most common pairs: JAWS with Chrome 24.7%, NVDA with Chrome 21.3%, JAWS with Edge 11.4%, NVDA with Firefox 10.0%, VoiceOver with Safari 7.0%. The survey is self selected; treat the numbers as direction, not market share.

| Platform | Pair to test | Notes |
|---|---|---|
| Windows | NVDA + Chrome (free) | Covers the largest free reader. JAWS needs a license |
| macOS / iOS | VoiceOver + Safari | Built in. iOS VoiceOver is the most used mobile reader |
| Android | TalkBack + Chrome | Built in |
| Linux | Orca + Firefox | Orca is the only realistic option on Linux (Arch package `orca`). Small user share; good enough for a smoke pass of semantics, not a replacement for NVDA or VoiceOver |

The 10 minute smoke script per flow:

1. Open the headings list (NVDA: Insert+F7; VoiceOver: rotor, VO+U). There is one `h1`, levels do not skip, headings describe sections.
2. Open the landmarks list. There is a `main`, a `nav` with a name if there are several, a `banner` and `contentinfo`.
3. Tab through the form. Each field announces its label, its type, required state and any hint.
4. Submit with errors. The error is announced (live region or focus move) and each field announces its own error.
5. Each button and link announces a name that makes sense out of context ("Delete project", not "Click here", not an icon name).
6. Images: informative images announce useful alt text; decorative ones are silent.
7. Dynamic updates (toast, "Saved", cart count, search results count) are announced through a live region, once, without stealing focus.
8. Custom widgets (combobox, tabs, menu) announce role, state (expanded, selected) and position.

Write down what was announced when something is wrong; that text is the bug report's evidence.

## 9. Zoom, reflow, text spacing, contrast, motion

| Check | WCAG | How |
|---|---|---|
| Text resizes to 200% without loss of content or function | 1.4.4 AA | Browser zoom 200% (Ctrl and +). Nothing cut off, overlapped or hidden |
| Reflow at 320 CSS px wide (400% zoom on a 1280 px screen) with no horizontal scrolling, except tables, maps, code | 1.4.10 AA | Playwright: `page.setViewportSize({ width: 320, height: 800 })` and check `scrollWidth <= clientWidth` (see `visual-regression.md` section 9) |
| Text spacing override does not break layout | 1.4.12 AA | Inject the WCAG spacing and look for clipped text: `page.addStyleTag({ content: '* { line-height: 1.5 !important; letter-spacing: 0.12em !important; word-spacing: 0.16em !important } p { margin-bottom: 2em !important }' })` |
| Text contrast 4.5:1 (3:1 for large text), UI components and focus indicators 3:1 | 1.4.3, 1.4.11 AA | axe in a browser, both color schemes. Manual check over images and gradients |
| Color is not the only signal | 1.4.1 A | Errors have text or icons, links in text are underlined or otherwise marked |
| Motion can be reduced | 2.3.3 AAA, plus the `prefers-reduced-motion` expectation | `test.use({ reducedMotion: 'reduce' })` and assert large animations are off. Nothing flashes more than 3 times per second (2.3.1 A) |
| Forced colors / high contrast mode | 1.4.11 | `test.use({ forcedColors: 'active' })`, icons and focus still visible |

## 10. WCAG 2.2 criteria a tester checks

WCAG 2.2 (W3C Recommendation) added 9 criteria and removed 4.1.1 Parsing. Level AA is the usual legal and contract target. The criteria most worth a tester's time on a typical site or app:

| Criterion | Level | Auto (axe) | How to test manually |
|---|---|---|---|
| 1.1.1 Non text content | A | Partly (missing alt) | Alt text is meaningful; decorative images are `alt=""` |
| 1.3.1 Info and relationships | A | Partly | Headings, lists, tables, labels are real markup |
| 1.4.3 Contrast (minimum) | AA | Yes, in a browser | Over images and gradients by eye |
| 1.4.4 Resize text, 1.4.10 Reflow | AA | No | Section 9 |
| 1.4.11 Non text contrast | AA | No | Borders of inputs, icons, focus rings at 3:1 |
| 2.1.1 Keyboard, 2.1.2 No keyboard trap | A | No | Section 6 |
| 2.4.3 Focus order | A | No | Section 7 |
| 2.4.7 Focus visible | AA | No | Section 7 |
| **2.4.11 Focus not obscured (minimum)** (new) | AA | No | Focused element not fully hidden by sticky headers, banners, chat widgets |
| **2.5.7 Dragging movements** (new) | AA | No | Every drag action (reorder, slider, map pan) has a single pointer alternative (buttons, click to place) |
| **2.5.8 Target size (minimum)** (new) | AA | Yes (`target-size`, tag `wcag22aa`) | Targets at least 24 by 24 CSS px, or spaced so a 24 px circle centred on each does not touch another target. Exceptions: inline links in text, browser default controls, an equivalent control elsewhere, essential |
| **3.2.6 Consistent help** (new) | A | No | Help links or contact info in the same place on every page |
| **3.3.7 Redundant entry** (new) | A | No | The user is not asked to type the same info twice in one process (offer "same as billing", prefill) |
| **3.3.8 Accessible authentication (minimum)** (new) | AA | No | Login does not require a cognitive test (remembering, transcribing, puzzles). Paste and password managers work in password and code fields; no paste blocking |
| 3.3.1 Error identification, 3.3.3 Error suggestion | A, AA | No | Errors in text, tied to the field, say how to fix |
| 4.1.2 Name, role, value | A | Partly | Custom widgets announce role, name and state |
| 4.1.3 Status messages | AA | No | Toasts and counts announced without focus moving |

AAA additions in 2.2 (2.4.12 Focus not obscured enhanced, 2.4.13 Focus appearance, 3.3.9 Accessible authentication enhanced) are worth checking only if the project targets AAA.

A quick Playwright check for 3.3.8 (paste must work in the password field):

```ts
test.use({ permissions: ['clipboard-read', 'clipboard-write'] }); // Chromium project only

test('password field accepts paste (WCAG 3.3.8)', async ({ page }) => {
  await page.goto('/login');
  await page.evaluate(text => navigator.clipboard.writeText(text), 'correct horse battery staple');
  await page.getByLabel('Password').focus();
  await page.keyboard.press('ControlOrMeta+V');
  await expect(page.getByLabel('Password')).toHaveValue('correct horse battery staple');
});
```

## 11. When the agent cannot open a browser

If the user's rules turn browser automation off:

1. Run what needs no browser: `eslint-plugin-jsx-a11y`, html-validate with `a11y` on built HTML, component tests with jest-axe in jsdom, the curl smoke test.
2. Read the code for the semantic bugs tools miss: `div` or `span` with `onClick`, icon buttons with no `aria-label`, inputs without a `label`, `outline: none` without a replacement focus style, `tabindex` greater than 0, `aria-hidden` on focusable elements, `user-select`/paste blocking on password fields, fixed heights on text containers.
3. Write the Playwright axe and keyboard tests into the project for CI.
4. Hand the user a short checklist (keyboard pass steps 1 to 6, the zoom 200% check, a dark mode contrast look, one screen reader pass of the changed flow) and say plainly that contrast and focus visibility were not verified.

## 12. Checks

- [ ] axe scan for each new screen and each main state (dialog, error, menu), tags include `wcag22aa`.
- [ ] Scans run in light and dark mode.
- [ ] No global rule disabling; each exclusion has a comment and an issue link (`rg -n -e disableRules -e "\.exclude\(" e2e src`).
- [ ] `incomplete` axe results listed in the report for manual review.
- [ ] Each page asserts `aria-current="page"` on its own nav link, and each required input exposes `required` or `aria-required="true"` (axe does not report either).
- [ ] Component tests use jest-axe or vitest-axe where cheap; contrast is not claimed from jsdom.
- [ ] `eslint-plugin-jsx-a11y` active and clean (`npx eslint .`).
- [ ] html-validate with `a11y` preset clean on built pages (`npx html-validate --preset recommended,a11y "out/**/*.html"`).
- [ ] Keyboard pass done, or the checklist handed to the user: reach, operate, leave, visible focus, no trap, dialog focus return.
- [ ] Focus not obscured by sticky elements checked at the bottom of long pages.
- [ ] Targets at least 24 by 24 CSS px or spaced (2.5.8); drag actions have a click alternative (2.5.7).
- [ ] Login fields allow paste and password managers (3.3.8).
- [ ] Reflow at 320 px and zoom 200% checked, or in the user's checklist.
- [ ] Screen reader smoke script run on the changed flow, or handed to the user with the steps.
- [ ] The report says which checks were automated, which were manual, and which were not done.
