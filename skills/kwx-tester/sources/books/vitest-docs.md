# Vitest docs: Browser Mode, why Browser Mode, component testing, visual regression, test environments

- Author: Vitest team
- Year: 2026 (v5.0.5)
- Legal URL: https://vitest.dev/guide/browser/ ; https://vitest.dev/guide/browser/why ; https://vitest.dev/guide/browser/component-testing ; https://vitest.dev/guide/browser/visual-regression-testing ; https://vitest.dev/guide/environment

## What I read

The five pages.

## Key lessons used in web/component-and-unit-tests.md, web/visual-regression.md

- jsdom and happy-dom 'only simulate a browser environment and not an actual browser'; Browser Mode does not replace e2e runners and starts slower.
- Providers: playwright (recommended), webdriverio, preview (not for CI); @vitest/browser-playwright; expect.element retries.
- vi.spyOn on ESM exports throws in the browser, use vi.mock with spy: true; mock alert/confirm/print.
- happy-dom is 'considered to be faster than jsdom, but lacks some API'; per file @vitest-environment comment.
- toMatchScreenshot with __screenshots__ folders, pixelmatch, no default tolerance, references only from a controlled environment, review before commit.
