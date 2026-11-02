# Code Coverage at Google

- Authors: Marko Ivanković, Goran Petrović, René Just, Gordon Fraser
- Year: 2019 (ESEC/FSE 2019)
- Legal URL: https://homes.cs.washington.edu/~rjust/publ/google_coverage_fse_2019.pdf (author's site)

## What I read

The whole paper: infrastructure (lcov based, 7 languages, 1 billion lines daily), changelist versus project coverage, visualisation in code review, adoption over 5 years, voluntary coverage levels (Table 2), reasons for failed coverage runs, survey of 3,000 developers (512 answers), recommendations.

## Key lessons used in quality/coverage.md

- Coverage is most useful at changelist level, shown per line in code review; only 0.5% of developers run coverage by hand daily.
- No company wide threshold; voluntary levels: project 60/75/90% with changelist 70/80/90%.
- Survey: 45% use changelist coverage often or very often when authoring, 40% when reviewing, 10% never; 60% positive, 16% negative sentiment.
- Coverage instrumentation causes timeouts and memory failures, and makes sleep based tests flaky because code runs slower.
- Safety critical projects use mutation testing as the stricter criterion.
