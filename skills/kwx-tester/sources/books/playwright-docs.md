# Playwright documentation (Test runner, best practices, locators, assertions, auth, isolation, mocking, clock, webServer, retries, traces, CI, snapshots, ARIA snapshots, accessibility, emulation, component testing, test agents, CLI, release notes)

- Author: Microsoft Playwright team
- Year: 2026 (docs for 1.64)
- Legal URL: https://playwright.dev/docs/best-practices ; https://playwright.dev/docs/locators ; https://playwright.dev/docs/test-assertions ; https://playwright.dev/docs/auth ; https://playwright.dev/docs/browser-contexts ; https://playwright.dev/docs/mock ; https://playwright.dev/docs/clock ; https://playwright.dev/docs/test-webserver ; https://playwright.dev/docs/test-retries ; https://playwright.dev/docs/trace-viewer ; https://playwright.dev/docs/ci ; https://playwright.dev/docs/test-snapshots ; https://playwright.dev/docs/aria-snapshots ; https://playwright.dev/docs/accessibility-testing ; https://playwright.dev/docs/emulation ; https://playwright.dev/docs/test-components ; https://playwright.dev/docs/test-agents ; https://playwright.dev/docs/getting-started-cli ; https://playwright.dev/docs/release-notes ; https://playwright.dev/docs/api/class-pageassertions

## What I read

All the pages listed, the first 100,000 characters of the release notes (1.50 to 1.64), the toHaveScreenshot options in the API reference. Also the installed 1.64.1 CLI help and type definitions (retryStrategy, failOnFlakyTests, lock, emulation option names, device registry).

## Key lessons used in web/playwright.md, web/e2e-flakiness.md, web/visual-regression.md, web/cross-browser-and-responsive.md, web/browser-automation-for-agents.md, web/accessibility-testing.md

- Locator priority: getByRole first, getByTestId last; CSS and XPath 'are not recommended'; first(), last(), nth() 'not recommended'.
- Web first assertions retry (5 s default); manual isVisible checks do not wait; toPass default timeout is 0.
- Each test gets a fresh browser context; start clean rather than clean up; order independence.
- storageState setup project, .auth in .gitignore, one account per worker via parallelIndex, sessionStorage not saved.
- webServer options and readiness rules; production build recommended by Next.js.
- Trace 'on-first-retry' in CI, 'on' is performance heavy; workers 1 in CI recommended; do not cache browsers; report upload with !cancelled().
- Retries: passed / flaky / failed categories; retryStrategy 'isolated' (1.62); failOnFlakyTests (1.52); --shuffle (1.64); named locks (1.63).
- Component testing moved to the built in mount fixture and story galleries in 1.62; experimental ct packages removed.
- Test agents (planner, generator, healer) from 1.56; healer may skip a test it believes is broken.
- toHaveScreenshot: animations disabled and caret hidden by default, threshold 0.2, rendering varies by OS and hardware.
- Clock API: setFixedTime vs install plus fastForward/runFor/pauseAt.
- playwright-cli is positioned for coding agents as more token efficient than MCP; headless and in memory profile by default.
