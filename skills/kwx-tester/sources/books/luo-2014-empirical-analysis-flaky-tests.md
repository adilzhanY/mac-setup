# An Empirical Analysis of Flaky Tests

- Authors: Qingzhou Luo, Farah Hariri, Lamyaa Eloussi, Darko Marinov
- Year: 2014 (FSE 2014, pp. 643 to 653, DOI 10.1145/2635868.2635920); FSE 2024 Test of Time honourable mention
- Legal URL: author group copy, http://mir.cs.illinois.edu/marinov/publications/LuoETAL14FlakyTestsAnalysis.pdf

## What I read

The full paper: Table 1 findings and implications, root cause categories (Table 2 counts), manifestation, and fix strategies per category.

## Key lessons used in strategy/flaky-tests.md (also test-data-and-fixtures.md, strategy.md)

- 201 commits in 51 projects; 161 classified. Async wait 74 (45%), concurrency 32 (20%), test order dependency 19 (12%), resource leak 11, network 10, time 5, IO 4, randomness 4, floating point 3, unordered collections 1.
- 78% of flaky tests were flaky when first written; 96% platform independent.
- 85% of async wait flaky tests do not wait for external resources and involve one ordering; one added delay can reproduce most.
- Async wait fixes: waitFor 57% (42 of 74), sleep 27%; average bound 13.04 s for waitFor vs 1.52 s for sleep; 60% of sleep fixes increased an existing sleep.
- Concurrency fixes: locks 31%, deterministic code 25%, changed conditions 9%.
- Order dependency: 47% caused by external resources; 74% fixed by cleaning shared state.
- 24% of fixes changed the code under test, and 94% of those fixed a real bug: do not just delete flaky tests.
- Google TAP: 73K of 1.6M daily failures (4.56%) were flaky; a failing test is rerun up to 10 times.
