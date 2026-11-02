# Mock Roles, not Objects

- Authors: Steve Freeman, Nat Pryce, Tim Mackinnon, Joe Walnes
- Year: 2004 (OOPSLA 2004 companion)
- Legal URL: jMock project site, http://jmock.org/oopsla2004.pdf

## What I read

The full paper, especially section 4 "Mock Objects in Practice" and section 5 "Misconceptions about Mocks". GOOS (Growing Object Oriented Software, Guided by Tests, 2009) itself was not read: no legal free copy beyond what the authors published as this paper and their articles.

## Key lessons used in strategy/test-doubles.md

- Only mock types you own; write thin wrappers around runtime and third party types.
- Be explicit about things that should not happen.
- Specify as little as possible in a test: over specified tests are brittle.
- Do not use mocks to test boundary objects (values, independent calculations); assert on returned values.
- Do not add behaviour to mocks; an urge to do so signals misplaced responsibilities.
- Only mock immediate neighbours; too many mocks signals a design problem.
- Mock based tests become complicated quickly when the design is weak: use it as a design signal.
