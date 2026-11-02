# Quality reading list

Every URL used for the `quality/` files of kwx-tester (test-smells, coverage, test-suite-audit, ci-testing, regression-and-release-testing, test-metrics), read on 2026-10-31, with one line on what it gave. Per source notes are in `sources/books/` (file names in brackets).

## Papers

- https://ir.cwi.nl/pub/4324/04324D.pdf : van Deursen et al. 2001, the 11 original test smells and 6 test refactorings (vandeursen-2001-refactoring-test-code.md).
- https://cs.ubc.ca/~rtholmes/papers/icse_2014_inozemtseva.pdf : Inozemtseva and Holmes 2014, coverage versus effectiveness with suite size controlled (inozemtseva-holmes-2014-coverage.md).
- https://homes.cs.washington.edu/~rjust/publ/google_coverage_fse_2019.pdf : Code Coverage at Google, changelist coverage, voluntary levels, survey numbers, instrumentation failures (ivankovic-2019-code-coverage-at-google.md).
- https://arxiv.org/abs/2103.07189 : Petrović et al. 2021, 15 million mutants, 70% of 1,502 high priority bugs coupled to mutants on covered changes (notes already in petrovic-mutation-testing-at-google.md, written by another agent; not duplicated).
- https://www.rit.edu/academicaffairs/facultyscholarship/submit/download_file.php?id=66568 : Peruma et al. 2019, smell prevalence in 656 Android apps and the developer survey (peruma-2019-test-smells-android.md).
- https://zenodo.org/record/1689875 : Spadini et al. 2018, smelly tests are more change and defect prone (spadini-2018-test-smells-quality.md).
- https://research.tudelft.nl/en/publications/test-smells-20-years-later-detectability-validity-and-reliability : Panichella et al. 2022, abstract only (the PDF download timed out twice): smell vocabulary mismatched to real concerns, older detector misclassified over 70% on generated suites.
- https://www.cs.ubc.ca/award/2014/06/acm-sigsoft-distinguished-paper-award-icse and the search abstracts of Bavota et al. 2015 (Springer DOI 10.1007/s10664-014-9313-0): 86% of JUnit tests smelly, comprehension about 30% better without smells. Abstract only, the full paper is paywalled.
- Search abstracts only: Gopinath, Jensen and Groce ICSE 2014 (statement coverage best predictor of mutation kills; the author PDF at nau.edu did not download); Kochhar et al. 2017 IEEE TR (no significant correlation between coverage and post release bugs, https://www.microsoft.com/en-us/research/publication/code-coverage-and-post-release-defects-a-large-scale-study-on-open-source-projects/); Chekam et al. ICSE 2017 (coverage helps fault revelation only past a high threshold, https://discovery.ucl.ac.uk/10058915/7/Chekam_ICSE17.pdf not downloaded); Just et al. FSE 2014 (mutant detection correlates with real fault detection independently of coverage, 73% of real faults coupled, https://homes.cs.washington.edu/~mernst/pubs/mutation-effectiveness-fse2014-abstract.html).

## Catalogues and tools

- https://testsmells.org/pages/testsmells.html : tsDetect's 19 smells with detection rules.
- http://xunitpatterns.com/Test%20Smells.html : Meszaros' smell index (code, behaviour and project smells). The detailed pages were not reachable (connection refused on HTTPS, index fetched over HTTP); another agent's notes are in meszaros-xunit-test-patterns.md.
- https://github.com/vitest-dev/eslint-plugin-vitest : rule names for test smells in Vitest.
- https://github.com/mskelton/eslint-plugin-playwright : rule names for Playwright smells (missing await, waits, raw locators).
- https://docs.astral.sh/ruff/rules/#flake8-pytest-style-pt : PT rule codes for pytest smells.
- https://vitest.dev/guide/coverage and https://vitest.dev/config/coverage : providers, AST remapping since 3.2, include, thresholds (perFile, negative numbers, globs), coverage.changed.
- https://vitest.dev/guide/cli : --changed, --shard, --retry, --repeats, reporters, --allowOnly default on CI (also checked with `vitest --help`, 5.0.5).
- https://vitest.dev/guide/improving-performance : sharding with blob reporter and --merge-reports, pools, isolate.
- https://github.com/taiki-e/cargo-llvm-cov : commands for lcov, html, nextest, --fail-under-lines, --branch on nightly.
- https://github.com/Bachmann1234/diff_cover : diff-cover usage and formats (verified that it is line based).
- https://kotlin.github.io/kotlinx-kover/gradle-plugin/ : Kover 0.9.8 plugin id, tasks, Android variant tasks, verify rules, units.
- https://mutants.rs/in-diff.html : cargo mutants --in-diff takes a diff file; caveats.
- https://stryker-mutator.io/docs/stryker-js/incremental/ : Stryker incremental mode and --mutate with line ranges.
- https://nexte.st/docs/features/retries/ : retries, backoff, FLAKY status, --flaky-result fail.
- https://nexte.st/docs/ci-features/partitioning/ : slice and hash partitions, count deprecated.
- https://nexte.st/docs/machine-readable/junit/ : JUnit profile config and flakyFailure elements.
- https://playwright.dev/docs/test-sharding : shards, blob reports, merge-reports workflow.
- https://playwright.dev/docs/ci : workers 1 on CI, globalTimeout, artifact upload, container image.
- https://playwright.dev/docs/test-retries : passed, flaky, failed categories.
- https://overctrl-web.vercel.app/r/microsoft/playwright/releases/v1.45.0 and https://docs.currents.dev/dashboard/tests/flaky-tests : --fail-on-flaky-tests (1.45) and failOnFlakyTests (1.52+); secondary sources, flagged as such in the file.
- https://github.com/ReactiveCircus/android-emulator-runner : KVM step, AVD snapshot caching, inputs.
- https://docs.expo.dev/eas/workflows/get-started/ and https://docs.expo.dev/eas/workflows/pre-packaged-jobs/ : EAS workflow syntax, maestro job params, job types.

## Engineering posts and practitioner guidance

- https://testing.googleblog.com/2020/08/code-coverage-best-practices.html : 60/75/90 guideline, per commit 99%/90%, logarithmic gains (google-coverage-best-practices-2020.md).
- https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html : 1.5% flaky runs, 16% of tests, 84% of transitions, 3 times rule and its cost (notes in google-testing-blog-flaky-tests.md by another agent).
- https://testing.googleblog.com/2017/04/where-do-our-flaky-tests-come-from.html : flakiness by size (0.5% small, 1.6% medium, 14% large) and by tool (Android emulator 25.46%).
- https://testing.googleblog.com/2015/04/just-say-no-to-more-end-to-end-tests.html : feedback loop properties, 70/20/10, ice cream cone and hourglass.
- https://testing.googleblog.com/2010/12/test-sizes.html : small, medium, large definitions and time limits.
- https://slack.engineering/handling-flaky-tests-at-scale-auto-detection-suppression : 57% to under 5% test job failures, why hiding results failed, re-enabling is hard.
- https://engineering.atspotify.com/2019/11/test-flakiness-methods-for-identifying-and-dealing-with-flaky-tests/ : visibility alone cut flakiness 6% to 4%; Flakybot (via search summary).
- https://www.atlassian.com/blog/atlassian-engineering/taming-test-flakiness-how-we-built-a-scalable-tool-to-detect-and-manage-flaky-tests : Flakinator, retry based detection and quarantine (search summary only, the page did not load in full).
- https://martinfowler.com/articles/nonDeterminism.html : quarantine with a cap and a time limit, causes and fixes of non determinism.
- https://sre.google/workbook/canarying-releases/ : canary method and rollback rule (sre-workbook-canarying-releases.md).

## Platform docs for release testing

- https://developer.android.com/topic/performance/vitals : bad behaviour thresholds 1.09% crash, 0.47% ANR, per device 8%, 28 day window.
- https://support.google.com/googleplay/android-developer/answer/6346149 : staged rollouts, halt, resume, no rollback.
- https://support.google.com/googleplay/android-developer/answer/14151465 : closed test with 12 testers for 14 days for new personal accounts (via search result quoting the page).
- https://developer.apple.com/help/app-store-connect/update-your-app/release-a-version-update-in-phases/ : 7 day phased release percentages, 30 day pause limit.
- https://docs.sentry.io/product/releases/health/ : crash free sessions and users, session statuses, adoption.

## Cited but not read

- Meszaros, xUnit Test Patterns (book, 2007): only the free online index; the book is not free.
- Bavota et al., "Are test smells really harmful?" (EMSE 2015): paywalled; only abstract level numbers used, marked as such.
- Chilenski and Miller 1994 (MC/DC): cited through Ivanković et al.; not read.
- DO-178C: a paid standard; only its MC/DC requirement as cited by Ivanković et al.
- Tornhill, Your Code as a Crime Scene: the hotspot method is used through kwx-developer `quality/hotspots.md`.
- Strathern 1997 (Goodhart phrasing): quoted from common citation, not read.
