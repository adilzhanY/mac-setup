# Mock Service Worker docs: philosophy, structuring handlers, avoid request assertions, setupServer.listen, Node integration, 2.x to 3.x migration

- Author: Artem Zakharchenko and MSW contributors
- Year: 2026 (msw 3.0.3)
- Legal URL: https://mswjs.io/docs/philosophy ; https://mswjs.io/docs/best-practices/structuring-handlers ; https://mswjs.io/docs/best-practices/avoid-request-assertions ; https://mswjs.io/docs/api/setup-server/listen ; https://mswjs.io/docs/integrations/node ; https://mswjs.io/docs/migrations/2.x-to-3.x

## What I read

The six pages.

## Key lessons used in web/network-and-api-mocking.md, web/component-and-unit-tests.md

- Network level interception; 'Network behavior is a contract-like description of the network's expected state.'
- Happy path handlers file, per test server.use overrides, resetHandlers after each test, split by domain.
- Do not assert on requests; encode validity in handlers; fail on unhandled requests; life cycle events for side effect only calls.
- MSW 3: Node 22+, subpath imports (msw/http, msw/graphql, msw/utils/delay), onUnhandledRequest renamed onUnhandledFrame, GraphQL link first, worker.stop async.
