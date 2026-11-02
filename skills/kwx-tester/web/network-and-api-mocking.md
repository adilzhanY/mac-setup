# Network and API mocking for web tests

When a web test should fake the network and when it should talk to a real backend, and how to do both well: MSW 3 for component tests, dev and Storybook, Playwright's `route` and HAR replay for end to end tests, a real local backend (local Supabase or Postgres in Docker) for your own API, and how to stop mocks from drifting away from the real API. kwx-developer's `testing-strategy.md` section 6 has the general "what to mock, what never to mock" table; this file is the web specific how.

## Contents

1. Rules
2. Decision table: mock or real, per level
3. MSW 3 in component tests
4. Error and edge cases worth simulating
5. A real local backend for your own API
6. Playwright routing and MSW in end to end tests
7. Contract drift: keeping mocks honest
8. Checks

## 1. Rules

1. **Mock at the network boundary, not inside your code.** Intercept HTTP (MSW, `page.route`), never mock your own `apiClient` or data hook. Mocking the client means you never test that you call it correctly. Evidence: moderate (MSW philosophy, Dodds "Stop mocking fetch").
2. **Never call real third party APIs in tests** (Stripe, OpenAI, email, maps, analytics). Cost, rate limits, flakiness, and data you do not control. Evidence: moderate (Playwright best practices: "Only test what you control").
3. **Hit your own backend for real in end to end and API tests**, with a seeded local database. Mocking your own API in end to end tests tests nothing but the frontend. Evidence: moderate.
4. **Make unhandled requests fail the test** (`onUnhandledFrame: 'error'` in MSW 3, `onUnhandledRequest: 'error'` in MSW 2). A request you forgot to mock must not silently reach the internet or silently return nothing. Evidence: moderate (MSW docs).
5. **Assert on what the UI does with the response, not on the request itself.** Encode request validity in the handler (return 400 when the body is wrong), so a bad request shows up as a broken UI. Evidence: moderate (MSW "Avoid request assertions").
6. **Keep one happy path handler set, override per test for errors and edge cases, reset after each test.** Evidence: moderate (MSW "Structuring handlers").
7. **Derive mock data from the same schema or types as the real API**, and run a small set of contract tests against the real API in CI. Otherwise mocks drift and tests stay green while production breaks. Evidence: moderate.

## 2. Decision table: mock or real, per level

| Level | Your own API | Third party API | Database |
|---|---|---|---|
| Unit (pure functions) | Not involved | Not involved | Not involved |
| Component (Vitest + jsdom) | MSW handlers | MSW handlers | Not involved |
| API / route handler / server action | Real handler code called directly | MSW in node (or `wiremock` for Rust) | Real local Postgres / local Supabase |
| End to end (Playwright) | **Real**, running locally against a seeded DB | `page.route` / `context.route`, or `@msw/playwright` | Real local DB, data created per test |
| Visual regression | Mocked or fixed data so pixels are stable | Mocked | Fixed seed |
| Smoke test against staging or a preview URL | Real | Real sandbox mode if the provider has one (Stripe test mode) | Staging data, read only tests |

## 3. MSW 3 in component tests

MSW 3.0.3 is current (verified with `npm view msw version`, 2026-10-31). It needs Node.js 22 or newer. The main changes from MSW 2 (mswjs.io migration guide): handlers are imported from subpaths, and `onUnhandledRequest` is now `onUnhandledFrame` because it also covers WebSockets.

```ts
// MSW 3
import { http, HttpResponse } from 'msw/http';
import { delay } from 'msw/utils/delay';
import { setupServer } from 'msw/node';
// MSW 2 (older projects): import { http, HttpResponse, delay } from 'msw';
```

Happy path handlers, shared by tests, local dev and Storybook:

```ts
// src/mocks/handlers.ts
import { http, HttpResponse } from 'msw/http';
import type { Project } from '@/types/api';      // the same type the app uses

export const handlers = [
  http.get('/api/projects', () =>
    HttpResponse.json<Project[]>([{ id: 'p1', name: 'Torq', createdAt: '2026-01-02T00:00:00Z' }])),

  http.post('/api/projects', async ({ request }) => {
    const body = (await request.json()) as { name?: string };
    if (!body.name?.trim()) return HttpResponse.json({ error: 'Name is required' }, { status: 400 }); // validity lives here
    return HttpResponse.json<Project>({ id: 'p2', name: body.name, createdAt: new Date().toISOString() }, { status: 201 });
  }),
];
```

```ts
// src/mocks/node.ts
import { setupServer } from 'msw/node';
import { handlers } from './handlers';
export const server = setupServer(...handlers);
```

Wire it in the test setup file (see `component-and-unit-tests.md` section 4): `listen` in `beforeAll` with `onUnhandledFrame: 'error'`, `resetHandlers` in `afterEach`, `close` in `afterAll`.

Per test override:

```ts
test('shows a retry button when loading projects fails', async () => {
  server.use(http.get('/api/projects', () => new HttpResponse(null, { status: 500 })));
  render(<Projects />);
  expect(await screen.findByRole('button', { name: 'Try again' })).toBeInTheDocument();
});
```

Notes:

- **Relative URLs in node**: MSW matches `/api/projects` against the request URL. In jsdom, relative `fetch` URLs resolve against `location.href` (`http://localhost:3000` by default in Vitest's jsdom). If your client builds absolute URLs from an env var, match those, or use a wildcard `*/api/projects`.
- **One time overrides**: `http.get(url, resolver, { once: true })` for "fails once, then succeeds" retry tests.
- **Requests with no visible effect** (analytics beacons) are the one case where asserting on the request is fine; use MSW's life cycle events for that.
- **Browser side MSW** (`setupWorker` from `msw/browser`) is for local development and Storybook. Do not leave it running in end to end tests against your real backend; it hides real network behaviour. If it is registered, block service workers in Playwright (`serviceWorkers: 'block'`).
- **GraphQL in MSW 3** is link first: `const api = graphql.link('https://api.example.com/graphql'); api.query('GetUser', resolver)`.

## 4. Error and edge cases worth simulating

Most frontend bugs live in states the developer never saw locally. For every screen that loads data, write one test per row that applies:

| Case | MSW handler | What the spec should say happens |
|---|---|---|
| Server error | `new HttpResponse(null, { status: 500 })` | Error message, a way to retry, no crash, no stale data shown as fresh |
| Network failure | `HttpResponse.error()` | Same as above, plus offline wording if the app has it |
| Slow response | `async () => { await delay(3000); return HttpResponse.json(data) }` | Loading state appears, no double submit, cancel works |
| Never responds | `async () => { await delay('infinite') }` | Timeout message after the app's timeout |
| Session expired | `HttpResponse.json({ error: 'expired' }, { status: 401 })` | Redirect to login, the user's typed input survives if the spec promises it |
| Forbidden | status 403 | "No access" state, not a blank page |
| Rate limited | status 429 with `Retry-After` | Backoff message, no hammering (count calls only here) |
| Validation error | status 400 / 422 with field errors | Errors next to the right fields, focus moves to the first one |
| Empty list | `HttpResponse.json([])` | Empty state with a next action |
| Huge list, pagination | 1000 items, or `next` cursor | Pagination or virtualisation works, no freeze |
| Malformed body | `new HttpResponse('not json', { headers: { 'content-type': 'application/json' } })` | Error state, error reported to logging, no white screen |
| Unicode and long text | Names with Kazakh or Cyrillic letters, emoji, 200 characters | No overflow, no mojibake, correct sorting |

Use `delay` inside handlers freely: it shapes the fake server. It is not the same as a fixed sleep in the test.

## 5. A real local backend for your own API

End to end and API tests should exercise the real server code and a real database. Rules:

- **Start from a known seed every run.** For Supabase: `supabase start` once, then `supabase db reset` before the suite (applies migrations and `supabase/seed.sql`). For plain Postgres: a Docker container plus your migration tool and a seed script. kwx-developer `testing-strategy.md` section 7 covers real Postgres in detail.
- **Create per test data on top of the seed** through the API or a DB helper in a Playwright fixture. Never depend on rows another test created.
- **Never point tests at production.** Guard it in code: refuse to run if the database URL host is not `localhost`, `127.0.0.1` or a known CI host.
  ```ts
  // e2e/global-setup.ts
  const url = new URL(process.env.DATABASE_URL ?? '');
  if (!['localhost', '127.0.0.1', 'db'].includes(url.hostname)) throw new Error(`Refusing to run e2e against ${url.hostname}`);
  ```
- **Row level security is part of the backend.** Test it with real tokens for two users (user A cannot read user B's rows) at the API level, not with the service role key, which skips RLS.
- **Email, SMS, payments**: use the provider's sandbox or a local catcher (Supabase local includes an email inbox service; Mailpit for others) and read the message through its API in the test.
- **Agent without a browser** can still run all of this: `curl` the local API, query the database directly, and run Vitest API tests. Only the browser part needs the user's yes.

## 6. Playwright routing and MSW in end to end tests

Full syntax is in `playwright.md` section 8. In end to end tests, route only what you do not control:

```ts
test.beforeEach(async ({ context }) => {
  await context.route(/(stripe\.com|js\.stripe\.com)/, route => route.fulfill({ status: 200, body: '' }));
  await context.route(/(plausible|google-analytics|sentry)\./, route => route.abort());
});
```

- Route on the context so popups and new tabs are covered too.
- To force an error state of your own API in an end to end test (rare, usually a component test does it better), route that one endpoint in that one test.
- **HAR replay** (`routeFromHAR`) freezes a real API's responses. Good for a slow or paid external API. Re-record on purpose (`update: true`), review the diff, and date the file name, because HARs go stale without warning.
- **`@msw/playwright`** (0.7.0, official MSW binding) lets end to end tests reuse `src/mocks/handlers.ts`. It uses Playwright routing underneath. The API changed between 0.3, 0.4 and 0.6; read the README for the installed version before writing the fixture. Use it for third party handlers only, not to replace your own backend.

## 7. Contract drift: keeping mocks honest

A mock is a copy of the real API's behaviour. When the real API changes and the mock does not, tests stay green and production breaks. Defences, cheapest first:

1. **Type the mock data with the real types.** `HttpResponse.json<Project[]>(...)` with `Project` from the same module the app uses. A renamed field becomes a compile error in `tsc --noEmit`. For Supabase, generate the types from the database: `supabase gen types typescript --local > src/types/database.ts`, and regenerate in CI to catch uncommitted schema changes (`git diff --exit-code src/types/database.ts`).
2. **Share one runtime schema.** If the API validates with Zod, parse every mock response with the same schema in the handler factory (`ProjectSchema.array().parse(data)`), so a mock that the real server could never send fails at once.
3. **Type handlers from an OpenAPI spec** when the API has one: `openapi-typescript` generates types, `openapi-msw` (2.0.0) wraps MSW so only paths in the spec are accepted and response bodies are typed per status code. Undefined paths fail at compile time.
4. **Run a small contract suite against the real API in CI.** The same requests the mocks answer (`GET /api/projects`, `POST /api/projects` with a bad body) sent to the real local server; assert status and schema, not exact values. If this suite and the mocks disagree, the mock is wrong.
5. **Consumer driven contracts (Pact)** are for separate teams owning frontend and backend. For a solo developer with one repo, steps 1 to 4 give the same safety with far less machinery. Evidence: opinion.

## 8. Checks

| Check | Pass condition | How |
|---|---|---|
| Unknown requests fail | `onUnhandledFrame: 'error'` (MSW 3) or `onUnhandledRequest: 'error'` (MSW 2) in the test setup | `rg -n -e onUnhandledFrame -e onUnhandledRequest .` |
| Handlers reset | `server.resetHandlers()` in `afterEach` | `rg -n resetHandlers .` |
| No mocking of own client | No `vi.mock` of the app's API client or data hooks in component tests | `rg -n "vi\.mock\(" src` (read each hit for the app's own client or hooks) |
| MSW import style matches version | MSW 3 imports from `msw/http`; MSW 2 from `msw` | `npm ls msw` and `rg -n "from 'msw'" src` |
| No real third party calls | Third party hosts routed or stubbed in Playwright and MSW | `rg -n -e "context\.route" -e "page\.route" e2e` |
| E2E uses the real own backend | No route on the app's own `/api` except deliberate error tests | `rg -n "route\(.*/api/" e2e` (read each hit) |
| Mock data typed | Handlers use the app's types or schemas | read `src/mocks/handlers.ts` |
| Error states covered | 500, network error, slow, 401, empty for every data screen | list the screens and the tests |
| Production guard | Test setup refuses non local database hosts | read `global-setup` |
| Contract suite | Real API checked against the same shapes as the mocks, in CI | read the CI workflow |
