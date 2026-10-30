# Software Engineering at Google (Winters, Manshreck, Wright; O'Reilly 2020), testing chapters

Legal free edition by Google: https://abseil.io/resources/swe-book (CC BY-NC-ND 4.0).

## What I read

Ch. 11 Testing Overview (sizes, scope, Beyonce rule, coverage), ch. 12 Unit Testing (TL;DRs and the sections on brittle tests, public APIs, naming, DAMP, shared values and setup), ch. 13 Test Doubles (structure, TL;DRs, prefer realism, fakes, stubbing dangers, interaction testing), ch. 14 Larger Testing (flakiness and understandability sections).

## Key lessons used in reliability/testing-strategy.md

- Classify tests by size (what they may do): small = one process, no I/O, no sleep, no network; medium = one machine, localhost only; large = multiple machines. Write the smallest test that can verify the behavior. Speed and determinism matter more than the unit/integration label.
- Rough mix target: 80% narrow unit, 15% integration, 5% end to end.
- Coverage as a target becomes a ceiling (80% treated as the maximum); judge suites by behaviors covered.
- Unit test TL;DRs: strive for unchanging tests; test via public APIs; test state, not interactions; complete and concise; test behaviors, not methods; name tests after behavior; no logic in tests; clear failure messages; DAMP over DRY.
- Use helper methods with defaults to build test data instead of shared constants; do not hide values a test asserts on inside setup methods.
- Test doubles TL;DRs: prefer real implementations; a fake is the best double when the real one cannot be used; overused stubbing makes tests unclear and brittle; avoid interaction testing, and when used, only for state changing calls and without overspecification. Fakes must be tested against the real implementation.
- GWS story: before testing discipline, more than 80% of production pushes had user affecting bugs.
- Larger tests: flakiness grows with scope; reduce scope, make tests event driven instead of timed, make failure output understandable.
