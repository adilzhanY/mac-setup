# An Empirical Study of Flaky Tests in Android Apps

- Authors: Swapna Thorve, Chandani Sreshtha, Na Meng (Virginia Tech)
- Year: 2018 (ICSME 2018, pp. 534 to 538)
- Legal URL: author copy, https://people.cs.vt.edu/nm8247/publications/empirical-study-flaky-pdf.pdf

## What I read

The full short paper: method (GitHub search, 77 commits in 29 Android projects), root cause categories with counts, and fixing strategies.

## Key lessons used in mobile/e2e-maestro-detox.md

- Root causes in 77 commits: concurrency 28 (36%), dependency on OS version, hardware or third party libraries 17 (22%), program logic 9 (12%), network 6 (8%), UI design 6 (8%); the rest hard to classify.
- Dependency, program logic and UI are causes not seen in earlier studies of Apache projects; test order dependency, common there, did not show up in Android apps.
- Fix strategies include changing the implementation, replacing an unstable library or network call, adding retries with a limit, and some developers simply removed or skipped the flaky test (about 13% of commits).
- Cites Google's figure that about 1.5% of test runs report a flaky result and almost 16% of tests show some flakiness.
