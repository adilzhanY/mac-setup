# Code Coverage Best Practices (Google Testing Blog)

- Authors: Carlos Arguelles, Marko Ivanković, Adam Bender
- Year: 2020
- Legal URL: https://testing.googleblog.com/2020/08/code-coverage-best-practices.html

## What I read

The whole post.

## Key lessons used in quality/coverage.md and quality/test-metrics.md

- Coverage is "a lossy and indirect metric"; high coverage does not guarantee good tests, low coverage does guarantee untested code.
- No ideal number; Google's general guideline is 60% acceptable, 75% commendable, 90% exemplary, without top down mandates.
- Gains beyond a point are logarithmic; move from 30% to 70% before arguing about 90 to 95%.
- Per commit coverage goals of 99% are reasonable, 90% a good lower bound; project wide goals above 90% are probably not worth it.
- What is not covered matters more than what is; discuss uncovered lines in code review.
- Integration and e2e coverage is partly incidental; mandated numbers risk being treated as a checkbox.
- Mutation testing is the better check of whether covered lines are really tested.
