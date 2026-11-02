# Refactoring Test Code

- Authors: Arie van Deursen, Leon Moonen, Alex van den Bergh, Gerard Kok
- Year: 2001 (XP2001, Cagliari; CWI report SEN-R0119)
- Legal URL: https://ir.cwi.nl/pub/4324/04324D.pdf (CWI institutional repository)

## What I read

The whole paper (8 pages): the 11 test smells (Mystery Guest, Resource Optimism, Test Run War, General Fixture, Eager Test, Lazy Test, Assertion Roulette, Indirect Testing, For Testers Only, Sensitive Equality, Test Code Duplication) and the 6 test refactorings (Inline Resource, Setup External Resource, Make Resource Unique, Reduce Data, Add Assertion Explanation, Introduce Equality Method).

## Key lessons used in quality/test-smells.md

- The original definitions of Mystery Guest, Resource Optimism, Test Run War, General Fixture, Eager, Lazy, Assertion Roulette, Sensitive Equality and For Testers Only, with the fix for each.
- Make Resource Unique: unique names per test and per run (they suggest a timestamp plus the test name) prevent interference between parallel runs.
- A test refactoring must not add or remove test cases, and "replacing all test code by assert(true) is not considered a valid refactoring".
- Indirect Testing is disputed even by the authors ("opinions differ"), which is why the skill reports it carefully.
- Splitting an Eager Test can slow the suite through extra setup; the trade off is stated, not hidden.
