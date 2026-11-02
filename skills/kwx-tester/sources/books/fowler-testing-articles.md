# Martin Fowler: Mocks Aren't Stubs; Eradicating Non-Determinism in Tests; On the Diverse And Fantastical Shapes of Testing

- Author: Martin Fowler
- Year: 2007 (Mocks Aren't Stubs, revised), 2011 (Non-Determinism), 2021 (Test Shapes)
- Legal URL: https://martinfowler.com/articles/mocksArentStubs.html, https://martinfowler.com/articles/nonDeterminism.html, https://martinfowler.com/articles/2021-test-shapes.html

## What I read

All three articles in full (through summaries of the pages).

## Key lessons used in strategy/test-doubles.md, strategy/flaky-tests.md, strategy/strategy.md

- Dummy, fake, stub, spy, mock definitions; state vs behaviour verification; classical vs mockist TDD; Fowler is "a convinced classicist" because mockist tests couple to implementation.
- Quarantine non deterministic tests and fix them quickly; cap the quarantine by number (for example 8) or time (a week).
- Causes and fixes: lack of isolation (rebuild state per test), async (never bare sleeps: callbacks or polling), remote services (doubles plus periodic contract tests), time (wrap the clock; fail the build on direct clock calls), resource leaks (pool of size 1 that throws).
- Unit vs integration mean different things to different people; sociable vs solitary tests (Jay Fields); debating percentages per test type is a distraction from test quality.
