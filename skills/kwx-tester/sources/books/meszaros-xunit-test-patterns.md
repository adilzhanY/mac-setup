# xUnit Test Patterns: Refactoring Test Code (online pattern catalogue)

- Author: Gerard Meszaros
- Year: 2007 (book); the pre publication pattern pages are free on the author's site
- Legal URL: http://xunitpatterns.com (Fresh Fixture, Shared Fixture, Erratic Test, Obscure Test pages)

## What I read

The pattern pages Fresh Fixture, Shared Fixture, Erratic Test and Obscure Test. The site notes the book's final text may differ.

## Key lessons used in strategy/test-data-and-fixtures.md, strategy/test-doubles.md, strategy/flaky-tests.md

- Fresh Fixture: each test builds its own fixture for private use; prevents Erratic Tests and supports Tests as Documentation. Persistent fresh fixtures need extra steps to stay private.
- Shared Fixture: faster but causes collisions (Interacting Tests, Test Run War) and leads to Obscure Tests and Fragile Fixtures; prefer an Immutable Shared Fixture before a mutable one.
- Erratic Test causes: Interacting Tests, Lonely Test, Unrepeatable Test, Test Run War, Nondeterministic Test; troubleshoot by collecting data on where and when tests fail.
- Obscure Test causes: Mystery Guest (cause and effect not visible in the test), General Fixture, Irrelevant Information, Hard Coded Test Data, Indirect Testing.
- The dummy, stub, spy, mock, fake vocabulary (as summarized by Fowler).
