# Raw material and independent proof (steps 3 and 5)

Research notes for kwx-deepen. Step 3 asks: what raw material does the expert start from, instead of a digested summary, and how do we go and get it. Step 5 asks: what, other than the author or the requester, proves the result is right.

Every factual claim below carries a source tag like [S12]. The full list is at the end. Lines marked "Agent practice" are our own synthesis of how an AI agent can apply the cited idea; they are not claims made by the source.

---

## Part A: raw material

### A1. Primary, secondary, tertiary

- Primary sources are first hand, original information, published or not: diaries, letters, interviews, photographs, speeches, original works [S1].
- Secondary sources analyse or restate what primary sources describe: review articles, biographies, critiques, monographs [S1].
- Tertiary sources compile and summarise the first two and add no new information or analysis: encyclopedias, almanacs, bibliographies. Some library guides describe them mainly as finding tools [S1].
- The boundaries move with the discipline and the question. A newspaper article is secondary for the event it reports and primary for a study of how the press covered that event [S1].

Agent practice: a tertiary or secondary source is a map to the primary source, not the destination. Use it to find the citation, then fetch the thing cited.

### A2. Why the digested version is not enough

- Summaries drift away from the original. In 462 UK university health press releases, 33 to 40 percent contained claims stronger than the peer reviewed paper (causation from correlation, animal results applied to humans, advice not in the study). When the release exaggerated, 58 to 86 percent of the resulting news stories exaggerated too, against 10 to 18 percent when it did not [S2].
- Summary statistics hide structure. Anscombe's four datasets share nearly identical means, variances, correlation and regression line but look completely different when plotted [S3]. The Datasaurus dozen extends the point [S3].
- Commercial summaries carry interests. Analysts at banks that underwrote an IPO issued "buy" calls that did worse than unaffiliated brokers' "buy" calls before, at and after the recommendation, and the same analysts did better on IPOs their bank did not lead [S4].
- An AI's own memory is a tertiary source with no index. In a 2023 study, 55 percent of GPT 3.5 citations and 18 percent of GPT 4 citations were fabricated, and many of the real ones had substantive errors [S5].

Agent practice: never cite from memory. Every reference, quote, number, API signature and version gets fetched before it is used.

### A3. Source hierarchies by field

| Field | Start from (primary) | Use only to find the primary | Where it lives |
|---|---|---|---|
| Law | Constitution, statute, regulation, the court decision itself | Treatises, law reviews, legal encyclopedias, blog explainers | Official code sites, court websites, legislature portals, free case law databases |
| Medicine | Trial reports, systematic reviews of trials, registries | News, press releases, health sites | PubMed, Cochrane Library, trial registries, the full paper PDF |
| Software | The code, logs, stack traces, specs, RFCs, standards, changelogs, issue trackers | Blog posts, Q and A answers, tutorials | The repo at the exact version in use, `node_modules` or vendored source, the RFC Editor, release notes |
| Data | The raw rows and the collection method (who, when, how sampled, what was dropped) | Charts, dashboards, headline numbers | The dataset download, its datasheet or codebook, the query that produced it |
| History, journalism | Documents, archives, original recordings, interviews with people who were there | Retellings, aggregators, viral reposts | Archives, court filings, the Wayback Machine, the original uploader |
| Product | User interviews about past behaviour, support tickets, usage and event data, churn reasons | Stakeholder opinions, competitor marketing, survey "would you" answers | Support inbox, analytics, CRM notes, call recordings |
| Design | Real users doing real tasks, the existing product and its analytics | Trend articles, Dribbble shots, other people's redesigns | The live product, session recordings, contextual inquiry notes |
| Finance | Audited filings and statements (10-K, 10-Q, 8-K, Form 4), the notes to the accounts | Analyst summaries, finance news, ratings sites | SEC EDGAR, company investor relations pages, national registries |

Evidence for the rows:

- Law: primary authority is the law itself (constitutions, statutes, regulations, court decisions). Secondary authority is commentary and "is not law", and mainly helps locate primary law. Mandatory authority is always primary and depends on jurisdiction and court level [S6].
- Medicine: the Oxford CEBM levels rank systematic reviews of randomized trials at the top for treatment questions and tell the user to start there and move down only if nothing is found. The levels are a shortcut, not a final verdict on quality, and may be moved up or down for study quality, consistency and effect size [S7]. Ioannidis argues that small studies, small effects, flexible designs, many tested hypotheses and financial interests all make a published finding less likely to be true, so a single study is weak ground [S8].
- Software: the RFC Editor records when an RFC is obsoleted or updated by a later one, and errata live on the errata page, not in the RFC text files. A verified erratum is "reviewed and considered accurate" [S9]. Agent practice: read the RFC status line and errata before quoting a spec; read the library source at the installed version before trusting a blog post about it.
- Data: Datasheets for Datasets asks dataset creators to document motivation, composition, collection process, preprocessing, uses, distribution and maintenance. The authors say a datasheet is not proof of what the data contains [S10]. Agent practice: ask for or find the datasheet or codebook, then check the raw rows against it.
- History and journalism: the Verification Handbook's first step for user generated content is to find the original piece, then check its source, date, location and motivation, and to contact the original source [S11]. Web archives show what a page said at a given time and can reveal silent edits; captures can be incomplete and should be checked across several dates [S12].
- Product: The Mom Test says to talk about the customer's life rather than your idea, to ask about specifics in the past rather than opinions about the future, and to listen more than talk, because people predict their own future behaviour poorly [S13].
- Design: contextual inquiry (Beyer and Holtzblatt) observes people doing their work in their own setting, with the researcher as apprentice and the user as master, built on context, partnership, interpretation and focus [S14].
- Finance: EDGAR gives free access to public company filings; the 10-K is the annual report, the 10-Q the quarterly report, the 8-K reports major events, and Form 4 records insider trades [S15]. The analyst bias result in A2 is the reason to read the filing rather than the note about it [S4].

### A4. Provenance checks

For any source, answer five questions before relying on it. These are drawn from the IFCN and Verification Handbook practice [S11, S16] and SIFT [S17]:

1. Who made it, and what is their expertise and agenda?
2. When was it made, and is there a newer version (obsoleted RFC, retracted paper, amended filing, updated law)?
3. How was it made (method, sample, instrument, which version of the code)?
4. Who paid for it or gains from it (conflicts of interest)?
5. Is this the original, or a copy that may have lost context?

The IFCN code requires signatories to prefer primary sources, check key claims against more than one source, name every significant source so readers can repeat the work, and disclose source interests that could affect the evidence [S16].

### A5. Lateral reading (Wineburg and McGrew)

- The study compared 10 PhD historians, 10 professional fact checkers and 25 Stanford undergraduates evaluating live websites [S18, S19].
- Historians and students read vertically: they stayed on the page and judged it by its own look, and were fooled by logos, official sounding names and domains. Fact checkers read laterally: they left the page quickly and opened new tabs to see what others said about the source [S18, S19].
- Fact checkers also showed "click restraint": they scanned results and chose which link to open instead of clicking the first one [S18].
- Even participants who did read laterally sometimes searched badly, for example without quotation marks [S18].

Agent practice: to judge a source, search for the source (its name plus "funding", "criticism", "who is behind"), not for more of the source's own pages.

### A6. SIFT (Mike Caulfield)

Four moves [S17]:

1. Stop. Do not read or share until you know what it is.
2. Investigate the source. Know what you are reading before you read it: its expertise and agenda.
3. Find better coverage. Look for the best source on the topic and see what the consensus is.
4. Trace claims, quotes and media to the original context, because much online content is clipped, recaptioned, or cites a study for something it does not say.

Agent practice: move 4 is step 3 of kwx-deepen. Move 3 is the cure for an agent that settles on the first search result.

---

## Part B: independent proof

The core reason this step exists: the author is a poor judge of their own work. Myers's second testing principle is that a programmer should avoid testing their own program, partly from unconscious reluctance to find errors and partly because a misread spec gets copied into the tests [S20]. For AI the same holds in measured form. LLMs struggle to self-correct reasoning without external feedback, and their answers sometimes get worse after trying [S21]. LLM evaluators recognise their own output and score it higher than others' work that humans rate as equal [S22].

So a proof must carry information that did not come from the author or the requester. For each method: what it proves, what it does not, and how an agent runs it.

### B1. Tests written from the spec (specified oracles)

- The oracle problem is telling correct from incorrect behaviour for a given input. Barr and colleagues classify oracles by where their information comes from: specified (from a spec), derived (from other artefacts such as an older version or documentation), implicit (crashes, exceptions) and human [S23].
- Proves: the code does what the spec says for the cases tested.
- Does not prove: the spec is right, or that untested cases work. A test whose expected value was copied from the code's own output proves nothing.
- Agent practice: write the expected values from the spec, the issue, the RFC or the user's words before reading the implementation, and watch each new test fail before the fix.

### B2. Property based testing

- QuickCheck (Claessen and Hughes, 2000) lets programmers state properties as functions and checks them against many random inputs, with custom generators [S24]. Implementations exist in about 40 languages [S24].
- Proves: a general rule (round trip, invariant, ordering) holds across a wide input space, often finding edge cases nobody listed.
- Does not prove: the property is the right one, or that rare inputs the generator never produces are handled.
- Agent practice: Hypothesis (Python) and fast-check (TypeScript) run in an ordinary test suite. Good properties: decode(encode(x)) == x, output sorted, total preserved, idempotence.

### B3. Differential testing against a reference

- McKeeman (1998) introduced differential testing: run several implementations on the same input and flag any disagreement [S25].
- Csmith generated random C programs, compiled each with several compilers and compared outputs, finding more than 325 bugs in GCC, LLVM and commercial compilers; the authors argue fixed test suites are not enough for compiler quality [S26].
- Proves: the new thing agrees with an independent implementation on those inputs.
- Does not prove: correctness when both share the same bug or the same misreading of the spec.
- Agent practice: compare a rewrite against the old version, a hand rolled parser against a standard library, a new SQL query against a slow obvious one, a computed figure against an official calculator.

### B4. Metamorphic testing

- Metamorphic testing checks relations between outputs of related inputs instead of the exact output, which makes it a response to the oracle problem [S27].
- Proves: the system behaves consistently under known transformations (sorting a shuffled list gives the same result, a search with an added filter returns a subset).
- Does not prove: that the base output is correct.
- Agent practice: useful for ML, search, ranking, simulation and anything with no known answer.

### B5. External reference values and test vectors

- NIST publishes known answer test vectors for cryptographic algorithms; anyone can check an implementation against them informally, though that does not replace formal validation [S28].
- Proves: agreement with an authority's published answers.
- Does not prove: behaviour outside the vectors, or security beyond correctness.
- Agent practice: for any standard (crypto, dates, tax, units, encodings, file formats), look for the official vectors, conformance suite or calculator and run against it.

### B6. Replication and reproducibility

- The National Academies (2019) separate reproducibility (same data and code give the same result) from replicability (new data aimed at the same question gives a consistent result), and note fields use the terms inconsistently [S29].
- The Open Science Collaboration repeated 100 psychology studies: 97 percent of the originals were significant, 36 percent of the replications were, and replication effect sizes were about half the originals [S30]. The figure has been contested on statistical grounds [S30].
- Proves (reproduction): the stated analysis yields the stated number. Proves (replication): the finding survives new data.
- Does not prove: the design was valid; a flawed method reproduces perfectly.
- Agent practice: rerun the analysis from raw data with your own code; rerun the bug reproduction after the fix; for a claim from a paper, look for an independent replication or meta-analysis.

### B7. Triangulation (Denzin)

- Denzin (The Research Act, 1970) described data triangulation (different times, places, people), investigator triangulation (more than one researcher), theory triangulation (several frameworks) and methodological triangulation (several methods, within or between) [S31]. Whether he meant three or four types is debated [S31].
- Proves: a finding that holds across independent sources and methods is less likely to be an artefact of one.
- Does not prove: anything when the "independent" sources share a common origin (several news stories from one press release, see [S2]).
- Agent practice: confirm a claim from sources with different origins, and a number by two different routes (top down and bottom up).

### B8. Fact checking protocols

- IFCN signatories commit to non partisanship, transparent sources (primary preferred, more than one source for key claims), transparent funding, transparent method (including evidence against the claim) and an open corrections policy [S16].
- Magazine style checking (described in Borel's Chicago Guide to Fact-Checking) works through a story's sources and classifies them as primary or secondary and high or low quality [S32].
- Proves: each stated fact matches a named source a reader can check.
- Does not prove: that the selection of facts is fair, or that the source itself is right.
- Agent practice: before shipping any article or summary, list every checkable claim, attach the primary source to each, and drop or soften any claim without one.

### B9. Peer review and blind second review

- At the BMJ, papers with deliberately inserted major errors went to many reviewers. Nobody found all the errors, some found none, and most found about a quarter. Smith concludes there is little evidence peer review works and much on its defects [S33].
- Cochrane requires at least two people to extract outcome data independently, with a disagreement process set in advance, because duplication reduces mistakes and single person bias. Independent double extraction produced fewer errors than one person extracting and a second checking [S34].
- Proves: a second, independent reader catches some errors and some bias.
- Does not prove: correctness. Reviewers miss most planted errors; a reviewer who sees the first answer anchors on it.
- Agent practice: the second reviewer (a fresh subagent) gets the raw inputs and the spec, not the first answer or the author's reasoning, and produces its own answer to compare. Differences are the finding.

### B10. Measurement against a baseline, A/B tests

- Online controlled experiments (Kohavi, Tang, Xu) randomly split users and compare. Trust checks include the sample ratio mismatch guardrail: if the observed split differs from the designed split, randomization or logging is broken and the result cannot be trusted [S35]. A/A tests (both arms identical) catch broken assignment [S35].
- Proves: a causal effect on the chosen metric, for that population and period.
- Does not prove: long term effects, effects on unmeasured metrics, or anything when guardrails fail.
- Agent practice: an agent usually cannot run a live A/B test, but it can always measure before and after: benchmark the old code, profile, then rerun the same benchmark; record the baseline number before changing anything.

### B11. User testing

- Nielsen's model says five users find about 85 percent of usability problems for one user group, so three rounds of five beat one round of fifteen; distinct user groups each need their own users [S36]. Faulkner's simulation found five user samples ranged from about 55 to nearly 100 percent of problems found, so 85 percent is an average [S36].
- Proves: real people can or cannot complete the real task.
- Does not prove: frequency of problems in the whole population, or preference at scale.
- Agent practice: the agent cannot be the user. It writes the task script and success criteria, and hands the test to the human. It can run cheap proxies first: an accessibility checker, a heuristic review against a written checklist, a cold read by a subagent with no context.

### B12. Back of the envelope bounds

- Fermi estimation splits a quantity into factors that can each be guessed, multiplies them, and gets the right order of magnitude because errors partly cancel. Sanity checks include dimensional consistency and a second independent route that should agree within an order of magnitude [S37].
- Proves: the answer is in a plausible range. A result ten times off the bound is almost certainly wrong.
- Does not prove: precision.
- Agent practice: before reporting any number (cost, time, size, market, speedup), compute a rough bound by a different route and say whether the result sits inside it.

---

## Part C: catalogue for 12 common requests

| Request | Best raw material | Best independent proof |
|---|---|---|
| Fix a bug | The failing input, the full error and logs, the code at the deployed version, `git log` and blame for the area | A failing test written from the expected behaviour, seen failing before the fix and passing after; the original repro rerun end to end [S20, S23] |
| Build a feature | The spec or issue, the existing code and its conventions, the API docs and source at the installed version, real usage data | Spec derived acceptance tests, property tests for the core logic, differential check against a reference where one exists [S23, S24, S25] |
| Write an article | Primary documents, data, interviews, original papers, not other articles | Claim by claim fact check against named primary sources, lateral reading on every source [S16, S18] |
| Summarise research | The papers themselves (methods and results sections), systematic reviews, trial registries | Each claim traced to page and table; summary checked against abstract and conclusions for overstatement; a second reader extracts key numbers independently [S2, S7, S34] |
| Analyse data | The raw rows, the codebook or datasheet, the collection method | Recompute headline numbers by a second route; plot the raw data, not only summaries; a Fermi bound on each key figure [S3, S10, S37] |
| Design a screen | Users' real tasks, the existing product, its analytics and support tickets | Usability test with five users per group run by the human; meanwhile an accessibility check and a cold read by an agent that did not design it [S14, S36] |
| Plan a product | Interviews about past behaviour, support tickets, usage data, competitors' actual products and pricing pages | Evidence of past behaviour (people already paying for or hacking around the problem), not stated intent; smallest test that could fail [S13] |
| Cover letter or email | The job posting, the company's own pages and filings, the sender's real record (projects, numbers) | Every claim about the sender checkable against their record; every claim about the company traced to its own pages; read by someone other than the writer |
| Make a video | The brief, the destination platform's specs, the real product or footage, the brand's own assets | Rendered output checked against platform specs (size, length, safe zones); a viewer who has not seen the script states what it said |
| Learn a topic | The standard textbook, the original papers, official docs, worked problems | Solving unseen problems with known answers; explaining it to someone else and being checked; exercises from an independent source |
| Financial or legal estimate | Statute and regulation text, official rate tables, audited filings, the actual contract | Official calculators and published examples; a second route estimate; a qualified human for anything binding [S4, S6, S15] |
| Choose a tool or vendor | Their docs, changelog, issue tracker, pricing page, status history, licence, a hands on trial | A small trial on your own real task with a success measure set in advance; lateral reading on reviews (who wrote them, who paid) [S18, S35] |

---

## Sources

- [S1] Library guides on source types: OCAD U, https://ocadu.libguides.com/Definingsources ; University of Kentucky, https://libguides.uky.edu/sourcetypes/examples ; Connecticut College, https://conncoll.libguides.com/primary-sources
- [S2] Sumner P. et al. (2014). The association between exaggeration in health related science news and academic press releases. BMJ 349:g7015. https://doi.org/10.1136/bmj.g7015 ; editorial: Goldacre B. (2014) BMJ 349:g7465, https://www.bmj.com/content/349/bmj.g7465
- [S3] Anscombe F. J. (1973). Graphs in Statistical Analysis. The American Statistician 27(1):17-21. Summary: https://en.wikipedia.org/wiki/Anscombe%27s_quartet
- [S4] Michaely R., Womack K. (1999). Conflict of Interest and the Credibility of Underwriter Analyst Recommendations. Review of Financial Studies 12(4):653-686. https://ideas.repec.org/a/oup/rfinst/v12y1999i4p653-86.html
- [S5] Walters W. H., Wilder E. I. (2023). Fabrication and errors in the bibliographic citations generated by ChatGPT. Scientific Reports 13:14045. https://www.nature.com/articles/s41598-023-41032-5
- [S6] Law library guides on weight of authority: University of South Carolina, https://guides.law.sc.edu/LRAWFall/WeightofAuthority ; George Mason, https://libguides.law.gmu.edu/first-year-legal-research/legal-authority
- [S7] OCEBM Levels of Evidence Working Group (2011). The Oxford Levels of Evidence 2. https://www.cebm.ox.ac.uk/resources/levels-of-evidence/ocebm-levels-of-evidence ; https://www.cebm.net/2016/05/ocebm-levels-of-evidence/
- [S8] Ioannidis J. P. A. (2005). Why Most Published Research Findings Are False. PLoS Medicine 2(8):e124. https://doi.org/10.1371/journal.pmed.0020124
- [S9] RFC Editor, Errata definitions: https://www.rfc-editor.org/errata-definitions ; example status notes: https://www.rfc-editor.org/errata/rfc2223
- [S10] Gebru T. et al. (2018, 2021). Datasheets for Datasets. arXiv:1803.09010; Communications of the ACM 64(12). https://arxiv.org/abs/1803.09010
- [S11] Silverman C., ed. (2014). Verification Handbook. European Journalism Centre. Summaries: https://www.journalism.co.uk/verification-tips-both-source-and-content/ ; https://gijn.org/stories/a-guide-to-verifying-digital-content-in-emergencies/
- [S12] Internet Archive (2026). Follow the Changes: 9 Ways Web Archives are Used in Digital Investigations. https://blog.archive.org/2026/02/02/follow-the-changes/ ; GIJN, https://gijn.org/resource/4-more-essential-tips-for-using-the-wayback-machine/
- [S13] Fitzpatrick R. (2013). The Mom Test. Summaries: https://mtlynch.io/book-reports/the-mom-test/ ; https://www.sachinrekhi.com/the-mom-test-rob-fitzpatrick
- [S14] Beyer H., Holtzblatt K. (1998). Contextual Design. Morgan Kaufmann. Summary: Nielsen Norman Group, https://nngroup.com/articles/contextual-inquiry ; https://usabilitybok.org/contextual-inquiry
- [S15] SEC, Using EDGAR to Research Investments. https://investor.gov/research-before-you-invest/research/researching-investments/using-edgar-researching-public-companies
- [S16] International Fact-Checking Network, Code of Principles. https://ifcncodeofprinciples.poynter.org/the-commitments
- [S17] Caulfield M. (2019). SIFT (The Four Moves). https://hapgood.us/2019/06/19/sift-the-four-moves/
- [S18] Wineburg S., McGrew S. (2019). Lateral Reading and the Nature of Expertise: Reading Less and Learning More When Evaluating Digital Information. Teachers College Record 121(11). Working paper: https://purl.stanford.edu/yk133ht8603 ; Stanford news: https://news.stanford.edu/stories/2017/10/fact-checkers-outperform-historians-evaluating-online-information
- [S19] Stanford Daily (2017). Fact checkers best historians, Stanford students at judging source credibility. https://stanforddaily.com/2017/10/26/fact-checkers-more-likely-than-peer-expert-groups-to-identify-credible-information-determine-gse-researchers/
- [S20] Myers G. J. (1979, 2nd ed. 2004). The Art of Software Testing. Wiley. Principles summary: https://www.cs.auckland.ac.nz/courses/compsci230s1c/lectures/18MyersPrinciples.pdf
- [S21] Huang J. et al. (2024). Large Language Models Cannot Self-Correct Reasoning Yet. ICLR 2024. https://arxiv.org/abs/2310.01798
- [S22] Panickssery A., Bowman S. R., Feng S. (2024). LLM Evaluators Recognize and Favor Their Own Generations. NeurIPS 2024. https://arxiv.org/abs/2404.13076
- [S23] Barr E. T., Harman M., McMinn P., Shahbaz M., Yoo S. (2015). The Oracle Problem in Software Testing: A Survey. IEEE TSE 41(5):507-525. https://doi.org/10.1109/TSE.2014.2372785 ; open copy: https://discovery.ucl.ac.uk/1471263/
- [S24] Claessen K., Hughes J. (2000). QuickCheck: A Lightweight Tool for Random Testing of Haskell Programs. ICFP 2000. https://doi.org/10.1145/357766.351266 ; notes: https://alastairreid.github.io/RelatedWork/papers/claessen:icfp:2000 ; tools: https://hypothesis.readthedocs.io/ , https://fast-check.dev/
- [S25] McKeeman W. M. (1998). Differential Testing for Software. Digital Technical Journal 10(1):100-107. https://en.wikipedia.org/wiki/Differential_testing
- [S26] Yang X., Chen Y., Eide E., Regehr J. (2011). Finding and Understanding Bugs in C Compilers. PLDI 2011. https://doi.org/10.1145/1993316.1993532 ; preprint: https://www-old.cs.utah.edu/~regehr/papers/pldi11-preprint.pdf
- [S27] Chen T. Y. et al. (2018). Metamorphic Testing: A Review of Challenges and Opportunities. ACM Computing Surveys 51(1):4. https://doi.org/10.1145/3143561
- [S28] NIST Cryptographic Algorithm Validation Program. https://csrc.nist.gov/projects/cryptographic-algorithm-validation-program ; archived description: https://webarchive.library.unt.edu/web/20130213222914/http:/csrc.nist.gov/groups/STM/cavp/index.html
- [S29] National Academies of Sciences, Engineering, and Medicine (2019). Reproducibility and Replicability in Science. https://nap.nationalacademies.org/25303 ; news release: https://www.nationalacademies.org/news/2019/09/reproducibility-and-replicability-in-research
- [S30] Open Science Collaboration (2015). Estimating the reproducibility of psychological science. Science 349(6251):aac4716. https://doi.org/10.1126/science.aac4716 ; summary and critique notes: https://acawiki.org/Estimating_the_reproducibility_of_psychological_science
- [S31] Denzin N. K. (1970). The Research Act in Sociology. Aldine. Summaries and the three or four types debate: https://qualityresearchinternational.com/methodology/RRW1pt15Triangulation.php ; https://www.academia.edu/7116059/Why_Triangulate
- [S32] Borel B. (2016, 2nd ed. 2023). The Chicago Guide to Fact-Checking. University of Chicago Press. https://press.uchicago.edu/ucp/books/book/chicago/C/bo194938501.html
- [S33] Smith R. (2006). Peer review: a flawed process at the heart of science and journals. Journal of the Royal Society of Medicine 99(4):178-182. https://pmc.ncbi.nlm.nih.gov/articles/PMC1420798/
- [S34] Cochrane MECIR standards C43 to C51 (collecting data): https://www.cochrane.org/authors/handbooks-and-manuals/mecir-manual/standards-conduct-new-cochrane-intervention-reviews-c1-c75/performing-review-c24-c75/collecting-data-included-studies-c43-c51 ; Handbook v5.1 section 7.6.2: https://training-noproxy.cochrane.org/handbook/archive/v5.1/chapter_7/7_6_2_who_should_extract_data.htm
- [S35] Kohavi R., Tang D., Xu Y. (2020). Trustworthy Online Controlled Experiments. Cambridge University Press, ch. 19 and 21. https://www.cambridge.org/core/books/trustworthy-online-controlled-experiments/sample-ratio-mismatch-and-other-trustrelated-guardrail-metrics/8DBB0F59AC7729D7BC6B94690DB9CCD5 ; Fabijan et al. (2019) SRM taxonomy via https://exp-platform.com/
- [S36] Nielsen J. (2000). Why You Only Need to Test with 5 Users. Nielsen Norman Group. https://nngroup.com/articles/why-you-only-need-to-test-with-5-users/ ; Faulkner (2003) simulation discussed at https://measuringu.com/category/sample-size/page/5/
- [S37] Fermi problem: https://en.wikipedia.org/wiki/Fermi_problem ; OpenStax University Physics 1.5: https://openstax.org/books/university-physics-volume-1/pages/1-5-estimates-and-fermi-calculations ; Cooper L., Making Estimates in Research: https://courses.grainger.illinois.edu/PHYS596/fa2023/Lectures/EstimationFA23.pdf

---

## Ten rules worth keeping

1. A summary is a map to the original. Use it to find the primary source, then fetch the primary source and work from that.
2. Never cite, quote or give a version from memory. Fetch it first; models invent references at measurable rates [S5].
3. Check the date and status of every source: obsoleted RFCs, retracted papers, amended filings, changed pages [S9, S12].
4. Judge a source by what others say about it (lateral reading), not by how it presents itself [S18].
5. Trace every claim, quote and number to its original context before repeating it [S17].
6. Prefer evidence of what people did over what they say they will do [S13].
7. Proof must carry information the author did not supply: a spec, a reference implementation, an official value, real users, new data [S23].
8. Write expected values before reading the implementation, and see the check fail before it passes [S20].
9. A second reviewer gets the raw inputs, not the first answer, and works independently; differences are the finding [S34, S22].
10. Bound every number by a second route and record a baseline before changing anything [S35, S37].
