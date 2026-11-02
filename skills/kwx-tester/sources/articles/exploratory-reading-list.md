# Exploratory testing reading list

Every URL used for the `exploratory/` folder (exploratory testing, heuristics, edge cases, i18n and accessibility testing, bug reports, human check handoff), read on 2026-10-31, one line each on what it gave. Notes for the primary sources are in `sources/books/`.

## Exploratory testing and heuristics

- https://www.satisfice.com/download/heuristic-test-strategy-model : HTSM v6.3 PDF (5 pages): SFDPOT sub items, nine techniques, quality criteria. Download needs the page's session cookie; plain curl of the link returns HTML.
- https://www.satisfice.com/download/session-based-test-management : Jonathan Bach 2000, session definition, session sheet, TBS metrics, PROOF debrief.
- https://www.satisfice.com/blog/archives/1509 : Bach and Bolton, Exploratory Testing 3.0: definition of testing, checking versus testing, formality continuum.
- https://kaner.com/?p=46 (via search result summary) : origin of the exploratory testing definition (2006 research summit), wording variants.
- https://developsense.com/blog/2012/07/few-hiccupps : Bolton's FEW HICCUPPS oracles and the fallibility warning.
- https://web.archive.org/web/2019id_/http://testobsessed.com/wp-content/uploads/2011/04/testheuristicscheatsheetv1.pdf : Hendrickson's Test Heuristics Cheat Sheet (original host has a broken TLS certificate).
- https://media.pragprog.com/titles/ehxta/charters.pdf : Explore It! excerpt on good charters and where charters come from.
- https://learn.microsoft.com/en-us/archive/blogs/james_whittaker/the-touring-test : Whittaker's tours, the names he used at Microsoft.
- https://www.getxray.app/blog/test-tours-exploratory-testing-strategy-qa-teams and https://googletesting-test.blogspot.com/2009/10/the-fedex-tour.html (search summaries only) : confirmation of money, landmark, FedEx, garbage collector's tours.

## Bug reports and debugging

- https://kaner.com/pdfs/BugAdvocacy.pdf : Kaner 2002, bug advocacy, follow up testing, non reproducible errors, report writing.
- https://developsense.com/presentations/2017-10-TestBash-RecordingAndReporting.pdf : Bolton 2017, PEOPLE WORKing, RIMGEA glosses, coverage levels, safety language, test case counts.
- https://spin.atomicobject.com/rimgea-testing-mnemonic/ : a practitioner gloss of RIMGEA (its "externalize" reading differs from Bolton's; Bolton's was used).
- https://www.debuggingbook.org/html/DeltaDebugger.html : Zeller, ddmin, 1-minimal, DeltaDebugger API, lessons.
- https://www.debuggingbook.org/html/Intro_Debugging.html : Zeller, scientific debugging, keep a log, vocabulary.

## Edge cases

- https://github.com/minimaxir/big-list-of-naughty-strings and the raw blns.txt / blns.json : section headings, 515 strings, usage warning.
- https://github.com/kdeldycke/awesome-falsehood : the falsehoods index by topic.
- https://www.kalzumeus.com/2010/06/17/falsehoods-programmers-believe-about-names/ : McKenzie's names list.
- https://web.archive.org/web/2023id_/https://infiniteundo.com/post/25326999628/falsehoods-programmers-believe-about-time : Sussman's time list (the live page returned 403).
- https://github.com/google/libphonenumber/blob/master/FALSEHOODS.md : phone number falsehoods.
- https://unicode.org/reports/tr15/ : UAX 15 normalisation forms, W3C NFC recommendation, concatenation pitfall.

## Internationalisation

- https://www.w3.org/International/articles/article-text-size : IBM text expansion table, vertical expansion, design rules.
- https://developer.android.com/guide/topics/resources/pseudolocales : en-XA and ar-XB, `isPseudoLocalesEnabled`.
- CLDR plural rules were read through `Intl.PluralRules` in Node 24.21 (bundled ICU) rather than the CLDR chart page; the outputs are recorded as verified in the i18n file.

## Accessibility

- https://www.w3.org/TR/WCAG22/ : new criteria in 2.2, removed 4.1.1, thresholds.
- https://www.w3.org/WAI/test-evaluate/preliminary/ : WAI Easy Checks procedures and caveats.
- https://www.gov.uk/service-manual/helping-people-to-use-your-service/testing-for-accessibility : GOV.UK testing guidance, WCAG 2.2 AA baseline, audit before public beta.
- https://www.gov.uk/service-manual/technology/testing-with-assistive-technologies : recommended screen reader and browser combinations.
- https://alphagov.github.io/accessibility-tool-audit/ : GDS 2018 audit of 13 automated tools against 142 barriers.
- https://www.deque.com/blog/automated-testing-study-identifies-57-percent-of-digital-accessibility-issues (search summary) : Deque 2021 vendor claim of 57 percent of issues by volume.

## Cited but not read, and why

- James Whittaker, How to Break Software (2002) and Exploratory Software Testing (2009): paid books, no legal free copy found; only the blog post and search summaries of the table of contents were used. The attack list in heuristics.md is marked as recalled.
- Elisabeth Hendrickson, Explore It! (2013) beyond the free excerpt: paid.
- Cem Kaner, James Bach, Bret Pettichord, Lessons Learned in Software Testing (2001): paid; not needed beyond Kaner's free paper.
- BBST Bug Advocacy course materials (testingeducation.org): the old PDF URL returned an empty response; RIMGEA was taken from Bolton's quotation of Kaner instead.
- Andreas Zeller, Why Programs Fail (2009): paid; the free Debugging Book covers the same delta debugging material.
- Zeller and Hildebrandt, "Simplifying and Isolating Failure-Inducing Input" (IEEE TSE 2002): not fetched; the Debugging Book chapter by the same author was enough.
- Unicode CLDR plural rules chart and UTS 35: used indirectly through ICU in Node.
- WCAG 2.2 text after section 2.5 (3.x and 4.x criteria wording): the fetch was truncated; those criteria are described from the W3C criteria names and common knowledge, not re read in full.
