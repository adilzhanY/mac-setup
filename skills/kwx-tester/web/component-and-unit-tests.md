# Component and unit tests for the web

How to test React and Next.js code below the end to end level: Vitest (with jsdom, happy-dom or a real browser through Browser Mode), Jest when a project already uses it, Testing Library's guiding principles and query priority, `user-event`, how to choose the DOM environment, the limits of testing React Server Components, and the Next.js App Router advice from the official docs. Most tests in a web app should live here: they are fast, run without a browser in jsdom, and an agent can always run them, even when browser automation is off. kwx-developer's `reliability/testing-strategy.md` section 9 lists the short Testing Library rules; this file is the full version for a tester.

## Contents

1. Rules
2. Which runner: Vitest or Jest
3. Which DOM: node, jsdom, happy-dom or a real browser
4. Vitest setup for Next.js
5. Testing Library: principles and query priority
6. user-event and async queries
7. Writing a component test from the spec
8. Vitest Browser Mode
9. Next.js App Router: what to test where
10. React Server Components, Server Actions and route handlers
11. Mocks, timers and snapshots
12. Checks

## 1. Rules

1. **Test what the user sees and does, never component internals.** Query the DOM, click and type like a person, assert on visible output. "The more your tests resemble the way your software is used, the more confidence they can give you" (Testing Library guiding principles). Evidence: moderate.
2. **Use `screen` and `getByRole` with a name as the default query.** `getByTestId` only when nothing user facing exists. Evidence: moderate (Testing Library query priority, Dodds "Common mistakes", rated high importance).
3. **Simulate input with `user-event` (`const user = userEvent.setup()`), not `fireEvent`.** `fireEvent` dispatches one DOM event; `user-event` simulates the whole interaction and refuses to click hidden or disabled elements. Evidence: moderate (user-event docs).
4. **Wait with `findBy*`, assert absence with `queryBy*`, never side effects inside `waitFor`.** Evidence: moderate (Dodds, rated high).
5. **Mock the network with MSW, not your fetch wrapper or data hook.** Evidence: moderate (MSW docs, Dodds "Stop mocking fetch"). See `network-and-api-mocking.md`.
6. **Use jsdom for logic and behaviour, a real browser (Vitest Browser Mode or Playwright) for layout, focus, scrolling, CSS and real events.** jsdom has no layout engine. Evidence: moderate (Vitest docs).
7. **Do not unit test async Server Components; cover them with end to end tests and test the functions they call.** Next.js: "we recommend using E2E tests for async components". Evidence: moderate (Next.js docs).
8. **Every test must be able to fail.** Before trusting a new test, break the behaviour (comment out the line, flip the condition) and watch it go red. Evidence: opinion, backed by kwx-developer `tests-and-honesty.md`.
9. **Snapshot tests are not behaviour tests.** Use them only for small, stable serialised output, and read every snapshot diff. Evidence: moderate.

## 2. Which runner: Vitest or Jest

| Situation | Use | Why |
|---|---|---|
| New project, Next.js, Vite, any ESM project | **Vitest 5** | Native ESM and TypeScript, Jest compatible API, watch mode, Browser Mode, built in visual regression (`toMatchScreenshot`) |
| Existing Jest suite that works | **Keep Jest 30** | Migration cost buys little. Use `next/jest` for config |
| React Native or Expo | Jest (`jest-expo`) | The RN tooling expects it. See the mobile folder |

Next.js `next/jest` setup (from the Next.js Jest guide), for an existing Jest project. Jest does not ship jsdom; install `jest-environment-jsdom` next to it.

```js
// jest.config.mjs
import nextJest from 'next/jest.js';
const createJestConfig = nextJest({ dir: './' });
export default createJestConfig({
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['<rootDir>/jest.setup.ts'],
  restoreMocks: true,
});
```

## 3. Which DOM: node, jsdom, happy-dom or a real browser

| Environment | Has | Lacks | Use for |
|---|---|---|---|
| `node` (Vitest default) | Fast, no DOM | Everything browser | Pure functions, validation schemas, reducers, server code, route handlers |
| `jsdom` 30 | Most DOM APIs, events, forms, `localStorage` | Layout (every size is 0), real CSS cascade, `IntersectionObserver`, `ResizeObserver`, `matchMedia`, canvas, real focus behaviour in some cases | Component behaviour, forms, conditional rendering. The Next.js default |
| `happy-dom` 21 | Same idea, "considered to be faster than jsdom, but lacks some API" (Vitest docs) | More gaps than jsdom | Large suites where speed matters and you hit no gaps. Switch per file if one breaks |
| Real browser (Vitest Browser Mode, Playwright) | Everything: layout, CSS, focus, scrolling, real events, contrast checks in axe | Slower start, needs a browser (check the user's browser rules) | Anything about size, position, visibility by CSS, focus traps, drag and drop, virtualised lists, canvas |

Switch one file: put `// @vitest-environment happy-dom` (or `jsdom`, `node`) at the top.

Traps in jsdom that make tests lie:

- `toBeVisible()` in jsdom only sees inline styles and the `hidden` attribute. A class that sets `display: none` from a CSS file is not applied, so the element counts as visible. Test CSS driven visibility in a real browser.
- Layout reads (`getBoundingClientRect`, `offsetWidth`) return 0. Code that measures will take its fallback path.
- axe color contrast does not run in jsdom (axe-core and jest-axe docs). Contrast needs a browser.
- `window.matchMedia` is missing; dark mode and reduced motion code needs a small stub. Keep the stub in the setup file and make each test set the value it needs.

## 4. Vitest setup for Next.js

Install (Next.js Vitest guide, plus the tester's additions):

```bash
npm install -D vitest @vitejs/plugin-react jsdom @testing-library/react @testing-library/dom \
  @testing-library/user-event @testing-library/jest-dom vite-tsconfig-paths msw
```

```ts
// vitest.config.mts
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import tsconfigPaths from 'vite-tsconfig-paths';

export default defineConfig({
  plugins: [tsconfigPaths(), react()],
  test: {
    environment: 'jsdom',
    setupFiles: ['./vitest.setup.ts'],
    restoreMocks: true,   // spies do not leak between tests
    unstubEnvs: true,
    unstubGlobals: true,
    include: ['src/**/*.test.{ts,tsx}'],
  },
});
```

```ts
// vitest.setup.ts
import '@testing-library/jest-dom/vitest';
import { afterAll, afterEach, beforeAll } from 'vitest';
import { cleanup } from '@testing-library/react';
import { server } from './src/mocks/node';

beforeAll(() => server.listen({ onUnhandledFrame: 'error' })); // MSW 3: unknown requests fail the test
afterEach(() => { server.resetHandlers(); cleanup(); });
afterAll(() => server.close());
```

(`cleanup` is automatic when Vitest `globals` is on. With globals off, as here, call it in `afterEach`. MSW 2 projects use `onUnhandledRequest: 'error'` instead.)

Run: `npx vitest run` (CI, once), `npx vitest` (watch), `npx vitest run src/cart` (one folder), `npx vitest run -t "shows an error"` (one test by name), `npx vitest run --sequence.shuffle` (order independence).

## 5. Testing Library: principles and query priority

Guiding principles (testing-library.com):

1. "If it relates to rendering components, then it should deal with DOM nodes rather than component instances."
2. "It should be generally useful for testing the application components in the way the user would use it."
3. "Utility implementations and APIs should be simple and flexible."

Query priority (testing-library.com/docs/queries/about):

| Priority | Query | Note from the docs |
|---|---|---|
| 1 | `getByRole('button', { name: /save/i })` | "This should be your top preference for just about everything" |
| 2 | `getByLabelText('Email')` | "Really good for form fields" |
| 3 | `getByPlaceholderText` | "A placeholder is not a substitute for a label" |
| 4 | `getByText` | Main way for non interactive content |
| 5 | `getByDisplayValue` | Filled in forms |
| 6 | `getByAltText` | Images, `area`, `input type=image` |
| 7 | `getByTitle` | "Not consistently read by screenreaders" |
| 8 | `getByTestId` | Only "where you can't match by role or text" |

Query types:

| Type | 0 matches | More than 1 | Waits? | Use for |
|---|---|---|---|---|
| `getBy` | throws | throws | no | Element that must be there now |
| `queryBy` | `null` | throws | no | Asserting something is **not** there |
| `findBy` | throws | throws | yes (1 s default) | Element that will appear (after fetch, after a click) |
| `*AllBy` | same rules, returns arrays | | | Lists |

Common mistakes rated high importance by Kent C. Dodds ("Common mistakes with React Testing Library"): the wrong assertion (use jest-dom matchers like `toBeDisabled` for good failure messages), the wrong query, adding `aria-*` or `role` that native HTML already provides, `query*` for anything but absence, `waitFor` where `find*` works, an empty `waitFor` callback, side effects inside `waitFor`. Medium: not using the ESLint plugins, calling `cleanup` by hand, not using `screen`, wrapping things in `act` without need, not using `user-event`.

Lint them away: `eslint-plugin-testing-library` and `eslint-plugin-jest-dom`.

## 6. user-event and async queries

```ts
import userEvent from '@testing-library/user-event';

test('submits the form with the typed email', async () => {
  const user = userEvent.setup();          // before render, inside the test
  render(<Newsletter />);
  await user.type(screen.getByLabelText('Email'), 'a@b.co');
  await user.click(screen.getByRole('button', { name: 'Subscribe' }));
  expect(await screen.findByRole('status')).toHaveTextContent('Check your inbox');
});
```

- Every `user.*` call returns a promise: always `await` it.
- Do not create `user` or render in `beforeEach` (user-event docs).
- Keyboard: `await user.keyboard('{Enter}')`, `await user.tab()`, `await user.keyboard('{Shift>}{Tab}{/Shift}')`. Use `user.tab()` to test focus order in a form; in jsdom it follows DOM order and `tabindex`, which is what the spec usually means.
- With fake timers: `userEvent.setup({ advanceTimers: vi.advanceTimersByTime })`, otherwise typing hangs.
- `findBy*` waits up to 1000 ms. If the real app needs longer, mock the slow part instead of raising the timeout.

## 7. Writing a component test from the spec

Write the cases from the spec or acceptance criteria before you open the component's source. For a sign up form the spec says: email required, password at least 12 characters, button disabled while submitting, server error shown in an alert. The tests follow the spec line by line:

```tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { http, HttpResponse } from 'msw/http';
import { server } from '@/mocks/node';
import { SignUpForm } from './SignUpForm';

function setup() {
  const user = userEvent.setup();
  render(<SignUpForm />);
  return {
    user,
    email: screen.getByLabelText('Email'),
    password: screen.getByLabelText('Password'),
    submit: screen.getByRole('button', { name: 'Create account' }),
  };
}

test('shows a message when the password is shorter than 12 characters', async () => {
  const { user, email, password, submit } = setup();
  await user.type(email, 'ada@example.com');
  await user.type(password, 'short');
  await user.click(submit);
  expect(screen.getByText('Use at least 12 characters')).toBeInTheDocument();
  expect(password).toHaveAccessibleDescription(/at least 12 characters/); // error is tied to the field
});

test('shows the server error in an alert', async () => {
  server.use(http.post('/api/signup', () => HttpResponse.json({ error: 'Email already used' }, { status: 409 })));
  const { user, email, password, submit } = setup();
  await user.type(email, 'ada@example.com');
  await user.type(password, 'long-enough-password');
  await user.click(submit);
  expect(await screen.findByRole('alert')).toHaveTextContent('Email already used');
  expect(submit).toBeEnabled();
});
```

Cover per component: the happy path, each validation rule at and around its boundary (11, 12, 13 characters), the loading state, the server error, the empty state, and keyboard use (submit with Enter). Test design techniques (boundaries, equivalence classes, state tables) are in the strategy folder.

## 8. Vitest Browser Mode

Browser Mode runs the same Vitest tests in a real browser through a provider. The Vitest docs: jsdom and happy-dom "only simulate a browser environment and not an actual browser". It does not replace an end to end runner, and it starts slower.

Running it opens a browser (headless or not). Check the user's browser rules before you run it yourself; CI can always run it.

```bash
npm install -D @vitest/browser-playwright vitest-browser-react
# or: npx vitest init browser
```

```ts
// vitest.config.mts: two projects, jsdom for most tests, a browser for *.browser.test.tsx
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import { playwright } from '@vitest/browser-playwright';

export default defineConfig({
  plugins: [react()],
  test: {
    projects: [
      { extends: true, test: { name: 'unit', environment: 'jsdom', include: ['src/**/*.test.tsx'], exclude: ['src/**/*.browser.test.tsx'] } },
      { extends: true, test: { name: 'browser', include: ['src/**/*.browser.test.tsx'],
          browser: { enabled: true, provider: playwright(), headless: true, instances: [{ browser: 'chromium' }] } } },
    ],
  },
});
```

```tsx
// Menu.browser.test.tsx
import { expect, test } from 'vitest';
import { page, userEvent } from 'vitest/browser';
import { render } from 'vitest-browser-react';
import { Menu } from './Menu';

test('Escape closes the menu and returns focus to the trigger', async () => {
  await render(<Menu />);
  const trigger = page.getByRole('button', { name: 'Account' });
  await trigger.click();
  await expect.element(page.getByRole('menu')).toBeVisible();
  await userEvent.keyboard('{Escape}');
  await expect.element(page.getByRole('menu')).not.toBeInTheDocument();
  await expect.element(trigger).toHaveFocus();
});
```

- `expect.element(...)` retries like Playwright's web first assertions.
- Use `userEvent` from `vitest/browser` in browser tests, not `@testing-library/user-event`.
- `vi.spyOn` on an ES module export throws in the browser; use `vi.mock('./mod', { spy: true })`.
- `alert`, `confirm` and `print` block the thread; mock them.
- Visual snapshots of components: `await expect(page.getByRole('button')).toMatchScreenshot()`. See `visual-regression.md`.

## 9. Next.js App Router: what to test where

| Code | Test level | Tool |
|---|---|---|
| Pure helpers (`lib/`), Zod schemas, formatters | Unit | Vitest, node |
| Client Components (`'use client'`) | Component | Vitest + Testing Library, jsdom (Browser Mode if layout matters) |
| Synchronous Server Components | Component (works) | Vitest + Testing Library. The Next.js docs say you can unit test "synchronous Server and Client Components" |
| `async` Server Components (pages that fetch) | End to end | Playwright. Unit test the data functions they call |
| Server Actions | Unit or integration | Call the action function directly with a `FormData`, real DB |
| Route handlers (`app/api/**/route.ts`) | Integration | Import `GET`/`POST`, call with a `Request`, assert the `Response` |
| Middleware / proxy, redirects, auth gates | End to end, plus a unit test of the matcher logic | Playwright, Vitest |
| `loading.tsx`, `error.tsx`, `not-found.tsx`, streaming | End to end | Playwright (route a slow or failing API) |
| Caching and revalidation | End to end against `next start` | Playwright, curl response headers |

Next.js APIs in component tests:

- `next/navigation` hooks need the App Router context. Mock them per test:
  ```ts
  const push = vi.fn();
  vi.mock('next/navigation', () => ({ useRouter: () => ({ push, replace: vi.fn(), refresh: vi.fn() }), usePathname: () => '/settings', useSearchParams: () => new URLSearchParams('tab=billing') }));
  ```
  Then assert on what the user sees after navigation in an end to end test, and only on `push` being called here when the navigation is the visible outcome.
- `next/image` and `next/link` render in jsdom without setup.
- `next/font` is handled by the Next.js SWC transform in `next/jest`; in Vitest, mock the font module to return `{ className: '' }` if an import fails.

## 10. React Server Components, Server Actions and route handlers

Async Server Components: "Since async Server Components are new to the React ecosystem, Vitest currently does not support them" (Next.js Vitest guide, updated 2026-08). The common workaround `render(await Page({ params }))` works only for a shallow page with mocked data. It breaks with nested async components, `cookies()`, `headers()` and caching. Do this instead:

1. Move data loading into plain async functions (`getInvoices(userId)`) and unit or integration test those against a real database.
2. Keep the presentational part as a synchronous component that takes data as props; component test it.
3. Cover the page itself with one Playwright test.

Experimental: Storybook's `vitest-plugin-rsc` renders Server Components in Vitest Browser Mode (`renderServer`). Treat it as experimental; do not make it the base of a suite. Evidence: opinion.

Route handler test (no browser, no server):

```ts
// app/api/health/route.test.ts
// @vitest-environment node
import { GET } from './route';

test('health returns ok with no-store caching', async () => {
  const res = await GET(new Request('http://localhost/api/health'));
  expect(res.status).toBe(200);
  expect(res.headers.get('cache-control')).toContain('no-store');
  expect(await res.json()).toEqual({ ok: true });
});
```

Server Action test:

```ts
// @vitest-environment node
import { createProject } from './actions';

test('rejects an empty project name', async () => {
  const fd = new FormData();
  fd.set('name', '');
  await expect(createProject(fd)).resolves.toEqual({ error: 'Name is required' });
});
```

Actions that call `cookies()`, `revalidatePath` or `redirect` need those mocked (`vi.mock('next/headers')`, `vi.mock('next/cache')`), which tests your code's use of them, not Next.js. Assert the end result (the row in the DB, the returned error), and cover the redirect in an end to end test.

## 11. Mocks, timers and snapshots

- **Mock at the edges only**: network (MSW), time (`vi.useFakeTimers()`, `vi.setSystemTime()`), randomness (seed or inject), browser APIs jsdom lacks. Never mock the component or module under test. kwx-developer `testing-strategy.md` section 6 has the full what to mock table.
- **Fake timers and Testing Library**: `vi.useFakeTimers({ shouldAdvanceTime: true })` keeps `findBy` working; pair with `userEvent.setup({ advanceTimers: vi.advanceTimersByTime })`. Restore with `vi.useRealTimers()` in `afterEach`.
- **Environment variables**: `vi.stubEnv('NEXT_PUBLIC_FLAG', 'on')` with `unstubEnvs: true` in config.
- **Snapshots**: inline snapshots for small serialised values (`expect(formatPrice(1999)).toMatchInlineSnapshot('"$19.99"')`) are fine. Whole component snapshots break on every markup change and get updated blindly; prefer explicit assertions or an ARIA snapshot in Playwright. Never run `vitest -u` without reading every changed snapshot.

## 12. Checks

| Check | Pass condition | How |
|---|---|---|
| Queries are user facing | `getByTestId` and `container.querySelector` rare and justified | `rg -n -e getByTestId -e "container\.querySelector" src` |
| user-event, not fireEvent | `fireEvent` only where user-event cannot | `rg -n fireEvent src` |
| No act or cleanup noise | No manual `act(` around render or user-event | `rg -n "act\(" src --glob '*.test.*'` |
| No side effects in waitFor | Each `waitFor` holds one assertion | read hits of `rg -n "waitFor\(" src` |
| Network blocked by default | MSW `onUnhandledFrame: 'error'` (MSW 3) or `onUnhandledRequest: 'error'` (MSW 2) | `rg -n -e onUnhandledFrame -e onUnhandledRequest .` |
| Mocks restored | `restoreMocks: true` in config | `rg -n restoreMocks vitest.config.* jest.config.*` |
| Right environment | jsdom or happy-dom only for files that need a DOM; layout and focus tests in a browser project | read the config and per file `@vitest-environment` comments |
| Async Server Components | Covered by Playwright, not by `render(await Page())` | `rg -n "render\(await" src` |
| Tests can fail | Each new test was seen red once (break the behaviour, run, restore) | state it in the report |
| Order independent | Suite passes shuffled | `npx vitest run --sequence.shuffle` |
| Lint plugins on | `testing-library` and `jest-dom` ESLint plugins active | `rg -n -e eslint-plugin-testing-library -e eslint-plugin-jest-dom package.json` |
