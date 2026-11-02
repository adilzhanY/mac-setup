# Flaky Tests at Google and How We Mitigate Them (2016); Where do our flaky tests come from? (2017)

- Author: John Micco; Jeff Listfield (Google Testing Blog)
- Year: 2016, 2017
- Legal URL: https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html ; https://testing.googleblog.com/2017/04/where-do-our-flaky-tests-come-from.html

## What I read

Only the reader comments and author replies were readable through the fetch tool; the article bodies did not load. The 2016 numbers are taken from kwx-developer's testing-strategy.md, which cites the same post.

## Key lessons used in web/e2e-flakiness.md

- Author reply (Listfield): when a stable test became flaky after a change, the cause was a production bug about 1 time in 6.
- Replies confirm the finding that larger tests are flakier.
- Reruns at Google only for tests marked flaky or on request (reply).
