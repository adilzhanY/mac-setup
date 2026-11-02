# Unit Testing: Principles, Practices, and Patterns (chapter 1 excerpt) and the "When to mock" article

- Author: Vladimir Khorikov
- Year: 2020 (Manning); article on enterprisecraftsmanship.com
- Legal URL: author's free chapter 1 excerpt, https://enterprisecraftsmanship.com/files/Unit-Testing-Chapter-1-Excerpt.pdf; article https://enterprisecraftsmanship.com/posts/when-to-mock/

## What I read

Chapter 1 (the goal of unit testing, coverage metrics, what makes a successful test suite) from the author's excerpt; the "When to mock" blog article. The rest of the book (chapters 2 to 11) was not read: it is paid, and the only full copies found online were pirate copies, which were not used.

## Key lessons used in strategy/test-doubles.md, strategy/mutation-testing.md, strategy/strategy.md

- The goal of unit testing is sustainable growth of the project; tests are code and a liability, so keep only tests whose value clearly exceeds their upkeep cost.
- Coverage is a good negative indicator and a bad positive indicator.
- A successful suite is integrated into the development cycle, targets the most important parts (the domain model), and gives maximum value for minimum maintenance.
- Mock only unmanaged out of process dependencies; use real instances of managed ones (your own database). Intra system communication is an implementation detail; inter system communication is observable behaviour.
- Mocks are for outgoing commands, stubs for incoming queries; asserting interactions with stubs is an anti pattern. "Both schools are wrong in their treatment of mocks."
