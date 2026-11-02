# Test Data Builders: an alternative to the Object Mother pattern

- Author: Nat Pryce
- Year: 2007 (blog article)
- Legal URL: http://www.natpryce.com/articles/000714.html

## What I read

The full article. Also Martin Fowler's bliki entry "ObjectMother" (https://martinfowler.com/bliki/ObjectMother.html) for the origin of the Object Mother name.

## Key lessons used in strategy/test-data-and-fixtures.md

- Constructing valid objects in tests fills tests with irrelevant detail and makes them brittle to constructor changes.
- Object Mother keeps tests readable with named factory methods but copes badly with variation and becomes bloated.
- A builder has a field per constructor parameter with safe defaults, chainable overrides, and a build method; tests state only what matters and stay isolated from structure they do not care about.
- Object Mother personas (Fowler) become familiar to the team, like personas; combine them with builders underneath.
