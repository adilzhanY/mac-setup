# Reading list: strategy folder

Every source used for `strategy/`, one line each on what it gave. Read on 2026-10-31. Primary sources with their own notes in `sources/books/` are marked (note).

## Papers and books read

- https://research.chalmers.se/publication/517894 : Hughes, "How to Specify It!" (2020). Five property kinds, bug hunting numbers, generator distribution, model based advice. (note: hughes-how-to-specify-it.md)
- http://mir.cs.illinois.edu/marinov/publications/LuoETAL14FlakyTestsAnalysis.pdf : Luo et al., "An Empirical Analysis of Flaky Tests" (FSE 2014). Root cause counts, fix strategies, 78% flaky at birth, 24% fixes in product code. (note: luo-2014-empirical-analysis-flaky-tests.md)
- https://istqb.org/certifications/certified-tester-foundation-level-ctfl-v4-0/ : ISTQB CTFL syllabus v4.0.1. Technique definitions, coverage items, test plan, entry and exit criteria, risk. (note: istqb-ctfl-syllabus-v4.md)
- https://istqb.org/wp-content/uploads/2025/10/Boundary-Value-Analysis-white-paper.pdf : Hamburg and Roman, BVA white paper. Six step procedure, 2 vs 3 value coverage items, login example. (note: istqb-ctfl-syllabus-v4.md)
- https://abseil.io/resources/swe-book/html/ch11.html : SWE at Google ch. 11. Sizes, scope, 80/15/5, ice cream cone, hourglass, coverage, flake rates. (note: swe-at-google-testing-chapters.md)
- https://abseil.io/resources/swe-book/html/ch13.html : SWE at Google ch. 13. Real over fake over stub; fakes need tests; interaction testing limits. (note)
- https://enterprisecraftsmanship.com/files/Unit-Testing-Chapter-1-Excerpt.pdf : Khorikov ch. 1 (author's excerpt). Goal of tests, coverage as negative indicator, successful suite. (note: khorikov-unit-testing-principles.md)
- https://enterprisecraftsmanship.com/posts/when-to-mock/ : Khorikov, managed vs unmanaged dependencies, mocks for commands, stubs for queries. (note)
- http://jmock.org/oopsla2004.pdf : Freeman, Pryce, Mackinnon, Walnes, "Mock Roles, not Objects". Only mock types you own, specify little, do not mock values. (note: freeman-pryce-mock-roles-not-objects.md)
- https://arxiv.org/abs/2102.11378 : Petrović et al., "Practical Mutation Testing at Scale". Diff based mutation, arid nodes, 15% to 89% productive mutants. (note: petrovic-mutation-testing-at-google.md)
- https://arxiv.org/abs/2103.07189 : Petrović et al., "Does mutation testing improve testing practices?". More tests written, 70% coupling with high priority bugs. (note)
- https://arxiv.org/abs/2002.12543 : Chen, Cheung, Yiu, "Metamorphic Testing" (1998 report). Origin of metamorphic relations, shortest path example. (note: chen-1998-metamorphic-testing.md)
- http://xunitpatterns.com : Meszaros pattern pages (Fresh Fixture, Shared Fixture, Erratic Test, Obscure Test). Fixture strategies and smells. (note: meszaros-xunit-test-patterns.md)
- http://www.natpryce.com/articles/000714.html : Pryce, Test Data Builders. Builder vs Object Mother. (note: pryce-test-data-builders.md)

## Articles and docs read

- https://martinfowler.com/articles/mocksArentStubs.html : double vocabulary, state vs behaviour verification, classical vs mockist. (note: fowler-testing-articles.md)
- https://martinfowler.com/articles/nonDeterminism.html : quarantine caps, causes and fixes of non determinism. (note)
- https://martinfowler.com/articles/2021-test-shapes.html : sociable vs solitary, shape debates are a distraction. (note)
- https://martinfowler.com/bliki/ObjectMother.html : origin of Object Mother.
- https://engineering.atspotify.com/2018/01/testing-of-microservices : the testing honeycomb.
- https://kentcdodds.com/blog/the-testing-trophy-and-testing-classifications : the testing trophy and its rationale.
- https://kentcdodds.com/blog/effective-snapshot-testing : snapshot rot, Searls quotes, size limits, serializers, good uses.
- https://jestjs.io/docs/snapshot-testing : snapshot best practices, property matchers, inline snapshots, CI does not write snapshots.
- https://docs.rs/insta/latest/insta/ : insta 1.49.0, INSTA_UPDATE modes and CI default.
- https://insta.rs/docs/cli/ : cargo insta review, accept, reject, pending-snapshots, --unreferenced.
- https://testing.googleblog.com/2017/04/where-do-our-flaky-tests-come-from.html : Listfield, flakiness by size and tool, r² for binary size and RAM (read through the Blogger feed, since the page renders by script).
- https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html : Micco, Google flake rates (numbers taken from kwx-developer, which cites this post; the page body did not render here).
- https://testing.googleblog.com/2020/12/test-flakiness-one-of-main-challenges.html : Pirocanac part I, sources of flakiness by component.
- https://testing.googleblog.com/2021/03/test-flakiness-one-of-main-challenges.html : Pirocanac part II, triage and remedies, no arbitrary delays.
- https://testing.googleblog.com/2021/06/how-much-testing-is-enough.html : Pirocanac, critical user journeys, changed line coverage, other test tiers, field feedback.
- https://arxiv.org/abs/2101.09077 : Gruber et al., flaky tests in Python (abstract only): 59% order dependent, 28% infrastructure.
- https://fast-check.dev/docs/advanced/model-based-testing/ : fc.commands, modelRun, replayPath.
- https://hypothesis.readthedocs.io/en/latest/stateful.html : RuleBasedStateMachine, rules, bundles, invariants, preconditions, settings.
- https://hypothesis.works/articles/what-is-property-based-testing/ : MacIver's definition of property based testing.
- https://proptest-rs.github.io/proptest/proptest/state-machine.html : ReferenceStateMachine and StateMachineTest signatures.
- https://docs.rs/proptest-state-machine/latest/proptest_state_machine/ : crate version 0.9.0.
- https://fsharpforfunandprofit.com/posts/property-based-testing-2/ : Wlaschin's property patterns.
- https://mutants.rs/in-diff.html : cargo-mutants --in-diff and its caveats.
- https://mutants.rs/mutants-out.html : mutants.out layout and outcome files.
- https://stryker-mutator.io/docs/stryker-js/incremental/ : Stryker incremental mode, --mutate with line ranges, limitations.
- https://github.com/microsoft/pict/blob/main/doc/pict.md : PICT model syntax, constraints, negative values, /o order.
- https://github.com/thombashi/allpairspy : allpairspy usage and filter_func.
- https://csrc.nist.gov/Projects/automated-combinatorial-testing-for-software/combinatorial-methods-in-testing/interactions-involved-in-software-failures : interaction rule, 4 way to 6 way coverage found all faults exhaustive testing found.
- https://csrc.nist.gov/projects/automated-combinatorial-testing-for-software : ACTS tool, most failures from one or two parameters.
- https://blog.regehr.org/?p=492 : Csmith, more than 325 compiler bugs by differential testing.
- https://github.com/hcoles/pitest/issues/579 and https://central.sonatype.com/artifact/com.arcmutate/pitest-kotlin-plugin : PIT noise on Kotlin coroutines; the Kotlin plugin is paid.

## Tools verified locally (scratch projects, not in the skill)

fast-check 4.10.2, Vitest 5.0.5, @faker-js/faker 10.6.0, @stryker-mutator/core 10.1.1 (Vitest runner), cargo-mutants 27.1.0, Hypothesis 6.170.14 (with pytest via uv), allpairspy 2.5.1. The runs produced the counterexamples and survivors quoted in the strategy files.

## Cited but not read, and why

- Lee Copeland, "A Practitioner's Guide to Software Test Design" (2003): paid book, no legal free excerpt found; its techniques are covered by the ISTQB syllabus, which was read.
- Freeman and Pryce, "Growing Object Oriented Software, Guided by Tests" (2009): paid; the authors' OOPSLA paper and Pryce's article were read instead.
- Khorikov, chapters 2 to 11: paid; search results offered only pirate copies, which were not used.
- Meszaros, "xUnit Test Patterns" (book): paid; the free pattern pages were read.
- Chen et al., "Metamorphic Testing: A Review of Challenges and Opportunities" (ACM CSUR 2018): the author repository copy is behind a Cloudflare challenge the tools could not pass; cited from abstracts and from Hughes.
- Barr, Harman, McMinn, Shahbaz, Yoo, "The Oracle Problem in Software Testing: A Survey" (IEEE TSE 2015): cited for the term; not fetched.
- Weyuker, "On testing non-testable programs" (1982): cited via Chen 1998.
- McKeeman, "Differential testing for software" (1998): cited via the Csmith work.
- Just et al., "Are mutants a valid substitute for real faults in software testing?" (FSE 2014): cited via the Google papers.
- Kuhn, Wallace, Gallo, "Software Fault Interactions and Implications for Software Testing" (IEEE TSE 2004): only NIST's summary pages were read; the exact per system percentages were not checked.
- Bach and Schroeder, "Pairwise Testing: A Best Practice That Isn't" (PNSQC 2004): available on satisfice.com; only its summary was read.
- Eck et al., "Understanding Flaky Tests: The Developer's Perspective" (arXiv 1907.01466) and Parry et al., "A Survey of Flaky Tests" (TOSEM 2021): seen in search, not read for lack of time.
- "State of Mutation Testing at Google" (ICSE SEIP 2018): abstract only; the 2021 arXiv papers by the same authors were read in its place.
