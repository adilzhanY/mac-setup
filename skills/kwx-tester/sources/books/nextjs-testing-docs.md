# Next.js App Router testing guides (overview, Vitest, Playwright)

- Author: Vercel
- Year: 2026 (pages updated Feb, Aug and Oct 2026)
- Legal URL: https://nextjs.org/docs/app/guides/testing ; https://nextjs.org/docs/app/guides/testing/vitest ; https://nextjs.org/docs/app/guides/testing/playwright

## What I read

The three pages.

## Key lessons used in web/component-and-unit-tests.md, web/playwright.md

- Async Server Components: 'we recommend using End-to-End Testing over Unit Testing'; Vitest 'currently does not support them'; synchronous Server and Client Components can be unit tested.
- Vitest setup: jsdom, @vitejs/plugin-react, vite-tsconfig-paths.
- Playwright: 'We recommend running your tests against your production code'; webServer alternative; @next/playwright instant() helper for Cache Components.
