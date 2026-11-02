# Web testing reading list

Every URL used for the `web/` folder of kwx-tester, read on 2026-10-31, with one line on what it gave. Per source notes are in `sources/books/` (file names in brackets).

## Playwright (sources/books/playwright-docs.md)

- https://playwright.dev/docs/best-practices : test user visible behaviour, isolation, "only test what you control", web first assertions, CI, linting, soft assertions.
- https://playwright.dev/docs/locators : locator priority list, strictness, filter, and/or, within, test ids, CSS and XPath "not recommended".
- https://playwright.dev/docs/test-assertions : retrying vs non retrying matchers, 5 s default, expect.poll, toPass default timeout 0, soft and configured expect.
- https://playwright.dev/docs/auth : setup project, storageState, .gitignore, one account per worker, API login, roles, sessionStorage caveat.
- https://playwright.dev/docs/browser-contexts : contexts as incognito like profiles, start clean, order independence.
- https://playwright.dev/docs/mock : route, fulfill, fetch and patch, HAR record and replay, routeWebSocket.
- https://playwright.dev/docs/clock : setFixedTime, install, fastForward, runFor, pauseAt.
- https://playwright.dev/docs/test-webserver : webServer options, readiness status codes, baseURL, several servers.
- https://playwright.dev/docs/test-retries : worker restart, passed / flaky / failed, serial mode, testInfo.retry.
- https://playwright.dev/docs/trace-viewer : trace modes, what a trace holds, show-trace and trace.playwright.dev.
- https://playwright.dev/docs/ci : workers 1 in CI, GitHub Actions workflow, report upload, Docker image tag, no browser caching.
- https://playwright.dev/docs/test-snapshots : toHaveScreenshot naming, OS rendering warning, threshold, maxDiffPixels, stylePath, update.
- https://playwright.dev/docs/api/class-pageassertions : full toHaveScreenshot options and defaults (animations disabled, caret hide, scale css).
- https://playwright.dev/docs/aria-snapshots : toMatchAriaSnapshot YAML, partial matching, update modes.
- https://playwright.dev/docs/accessibility-testing : AxeBuilder, withTags, include, exclude, disableRules, fingerprints, fixture.
- https://playwright.dev/docs/emulation : devices, viewport, colorScheme, locale, timezone, permissions, offline.
- https://playwright.dev/docs/test-components : new component testing with mount and story galleries (1.62), old packages removed.
- https://playwright.dev/docs/test-agents : planner, generator, healer; init-agents; healer may skip tests.
- https://playwright.dev/docs/getting-started-cli : playwright-cli commands, sessions, headless default, CLI vs MCP.
- https://playwright.dev/docs/release-notes : versions 1.50 to 1.64 and what each added.

## Agent browser tools

- https://github.com/microsoft/playwright-mcp : accessibility snapshot vs screenshot, profile modes, flags, "not a security boundary" (playwright-mcp-readme.md).
- https://github.com/ChromeDevTools/chrome-devtools-mcp : tools, isolation flags, telemetry defaults and opt outs (chrome-devtools-mcp-readme.md).

## Component and unit testing

- https://testing-library.com/docs/guiding-principles : the three principles and the core quote (testing-library-docs.md).
- https://testing-library.com/docs/queries/about/ : query priority and query type table.
- https://testing-library.com/docs/user-event/intro : user-event vs fireEvent, setup() pattern.
- https://kentcdodds.com/blog/common-mistakes-with-react-testing-library : 15 mistakes with importance ratings (dodds-rtl-mistakes-and-trophy.md).
- https://kentcdodds.com/blog/the-testing-trophy-and-testing-classifications : trophy layers and the "mostly integration" principle.
- https://vitest.dev/guide/browser/ : Browser Mode providers, config, limitations (vitest-docs.md).
- https://vitest.dev/guide/browser/why : why a real browser, drawbacks.
- https://vitest.dev/guide/browser/component-testing : locators, expect.element, userEvent from vitest/browser, a11y checks.
- https://vitest.dev/guide/browser/visual-regression-testing : toMatchScreenshot, comparator options, environment and review advice.
- https://vitest.dev/guide/environment : node, jsdom, happy-dom, edge-runtime, per file comments.
- https://nextjs.org/docs/app/guides/testing : test types, async Server Components need e2e (nextjs-testing-docs.md).
- https://nextjs.org/docs/app/guides/testing/vitest : setup and the async Server Component caveat.
- https://nextjs.org/docs/app/guides/testing/playwright : production build recommendation, webServer.

## Network mocking

- https://mswjs.io/docs/philosophy : network level interception, standard Request and Response (msw-docs.md).
- https://mswjs.io/docs/best-practices/structuring-handlers : happy path file, overrides, reset, domains.
- https://mswjs.io/docs/best-practices/avoid-request-assertions : test the UI reaction, encode validity in handlers.
- https://mswjs.io/docs/api/setup-server/listen : onUnhandledFrame strategies.
- https://mswjs.io/docs/integrations/node : setupServer with Vitest hooks.
- https://mswjs.io/docs/migrations/2.x-to-3.x : MSW 3 breaking changes.
- https://npmjs.com/package/openapi-msw : typed MSW handlers from OpenAPI types (search result summary only).
- https://npmjs.com/@msw/playwright : official binding, API changed across 0.x versions (search result summary only).

## Flaky tests

- https://arxiv.org/abs/2103.02669 : Romano et al. 2021, root causes and fixes of 235 flaky UI tests (romano-2021-ui-flaky-tests.md).
- https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html : only comments readable (google-testing-blog-flaky-tests.md).
- https://testing.googleblog.com/2017/04/where-do-our-flaky-tests-come-from.html : only comments readable; author reply on production bugs and test size.

## Visual regression

- https://argos-ci.com/docs/playwright : stabilisation list, Chromium font flags (visual-testing-services.md).
- https://www.chromatic.com/docs/playwright/ : archive based snapshots, setup, review flow.
- https://github.com/lost-pixel/lost-pixel : archived, product sunset.
- Search results on Playwright screenshot flakiness (argos-ci.com/blog/fix-flaky-visual-tests and practitioner guides): fonts and Docker baselines; used only as corroboration of the official docs.

## Accessibility

- https://www.deque.com/blog/automated-testing-study-identifies-57-percent-of-digital-accessibility-issues/ : the 57% by volume study (deque-automated-coverage-2021.md).
- https://accessibility.blog.gov.uk/2017/02/24/what-we-found-when-we-tested-tools-on-the-worlds-least-accessible-webpage/ : 143 barriers, 10 tools, 71% together, 29% missed (govuk-a11y-tool-audit-blog-2017.md).
- https://alphagov.github.io/accessibility-tool-audit/ : 2018 update, 142 barriers, 13 tools, per tool results.
- https://webaim.org/projects/million/ : 2026 report, failure rates and the six common failures (webaim-million-2026.md).
- https://webaim.org/projects/screenreadersurvey10/ : screen reader shares, pairs, headings navigation (webaim-screen-reader-survey-10.md).
- https://github.com/dequelabs/axe-core : 57% claim, zero false positives, incomplete results, jsdom contrast limit (axe-core-and-jest-axe.md).
- https://github.com/NickColley/jest-axe : usage, contrast off in jsdom, region rule, timers.
- https://www.w3.org/TR/WCAG22/#new-features-in-wcag-2-2 : nine new criteria, 4.1.1 removed (w3c-wcag-22-understanding-target-resize.md).
- https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html : 24 px rule, exceptions, circle method.
- https://www.w3.org/WAI/WCAG22/Understanding/resize-text.html : 200% text, link to 320 px reflow.

## Performance and SEO

- https://web.dev/articles/vitals : thresholds, p75, lab vs field, TBT as INP proxy, web-vitals snippet (web-dev-core-web-vitals.md).
- https://web.dev/articles/lcp : LCP ranges.
- https://web.dev/articles/inp : INP ranges.
- https://web.dev/articles/cls : CLS ranges.
- https://github.com/GoogleChrome/lighthouse-ci/blob/main/docs/getting-started.md : lighthouserc, GitHub Actions (lighthouse-ci-and-variability.md).
- https://github.com/GoogleChrome/lighthouse-ci/blob/main/docs/configuration.md : numberOfRuns, assertions, aggregationMethod default, upload targets.
- https://github.com/GoogleChrome/lighthouse/blob/main/docs/variability.md : median of 5, hardware advice.
- https://github.com/GoogleChrome/lighthouse/blob/main/docs/throttling.md : Slow 4G preset values.
- https://github.com/lycheeverse/lychee : offline site check, fragments, cache, ignore file (link-and-html-checkers.md).
- https://github.com/JustinBeckwith/linkinator : CLI and config.
- https://html-validate.org/usage/cli.html : CLI, presets, formatters.
- https://ogp.me/ : required and recommended Open Graph properties (open-graph-protocol.md).
- Search results on Chrome DevTools throttling presets (debugbear.com/blog/chrome-devtools-network-throttling): preset names Fast 4G, Slow 4G, 3G; values disagree between sources, so the file uses explicit CDP numbers instead of preset names.

## Browser usage

- https://gs.statcounter.com/browser-market-share : September 2026 browser shares (statcounter-browser-platform-share-2026.md).
- https://gs.statcounter.com/platform-market-share/desktop-mobile-tablet : mobile 59.06%.

## Package versions

- `npm view <pkg> version` for 30 packages on 2026-10-31 (verified): Playwright 1.64.1, Vitest 5.0.5, Jest 30.5.2, MSW 3.0.3, Testing Library React 16.3.3, user-event 14.6.8, axe-core and @axe-core/playwright 4.14.0, jest-axe 11.0.0, happy-dom 21.0.4, jsdom 30.1.3, @lhci/cli 0.15.1, lighthouse 13.6.0, linkinator 8.1.0, html-validate 11.17.0, size-limit 14.3.0, @playwright/mcp 0.0.84, eslint-plugin-playwright 2.12.1, @argos-ci/playwright 7.8.0, @chromatic-com/playwright 1.0.0, @percy/playwright 1.1.2, lost-pixel 3.22.0 (last published 2024-11), web-vitals 6.2.3, next 16.4.3.

## Cited but not read

- Deque's full coverage report (deque.com/coverage-report/): behind a form; the blog post gave the method and numbers.
- Google Testing Blog article bodies (2016, 2017): did not load through the fetch tool; numbers from 2016 come via kwx-developer, the 2017 claims via the author's replies.
- WebAIM Million 2025 page: superseded by the 2026 report, which was read.
- A newer WebAIM screen reader survey: none published after #10 as of this date.
- Software Engineering at Google (book, free online at abseil.io/resources/swe-book): cited through kwx-developer, not re-read for this folder.
