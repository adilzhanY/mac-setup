# Coverage Is Not Strongly Correlated with Test Suite Effectiveness

- Authors: Laura Inozemtseva, Reid Holmes
- Year: 2014 (ICSE 2014, ACM SIGSOFT Distinguished Paper)
- Legal URL: https://cs.ubc.ca/~rtholmes/papers/icse_2014_inozemtseva.pdf (author's site)

## What I read

Abstract, introduction, the survey of earlier studies (Table 1), method (31,000 suites generated for 5 Java systems up to 724,000 lines; statement, decision and modified condition coverage; mutation score as effectiveness), results sections 4.2 and 4.3, threats, conclusion.

## Key lessons used in quality/coverage.md and quality/test-metrics.md

- When suite size is ignored, coverage and effectiveness correlate moderately to highly; when size is held constant, the correlation drops to low to moderate.
- Stronger coverage kinds (decision, modified condition) gave no more insight than statement coverage.
- Conclusion quoted in the skill: coverage is useful to find under tested parts, but "should not be used as a quality target".
- Earlier studies disagreed partly because they did not control for suite size and used small or fully adequate suites.
