# Software Engineering at Google, chapters 11 (Testing Overview) and 13 (Test Doubles)

- Authors: Titus Winters, Tom Manshreck, Hyrum Wright (eds.); chapter 13 by Andrew Trenk and Dillon Bly
- Year: 2020
- Legal URL: free online edition, https://abseil.io/resources/swe-book/html/ch11.html and https://abseil.io/resources/swe-book/html/ch13.html

## What I read

Chapters 11 and 13 in full (through summaries of the online edition).

## Key lessons used in strategy/strategy.md, strategy/test-doubles.md, strategy/flaky-tests.md

- Test sizes (small, medium, large) by what a test may do; scope (narrow, medium, large) and the 80/15/5 target mix.
- Anti shapes: ice cream cone and hourglass.
- Coverage measures that a line ran, not what happened; a target like 80% becomes a ceiling.
- Flakiness: about 0.15% flake rate at Google means thousands a day; near 1% tests lose value.
- Test doubles: prefer real, then fake, then stub or interaction testing. "A fake is often the ideal solution if a real implementation can't be used in a test." Fakes need their own tests and should be owned by the team that owns the real code. "Overuse of stubbing leads to tests that are unclear and brittle." Interaction testing for state changing calls only, avoid overspecifying.
