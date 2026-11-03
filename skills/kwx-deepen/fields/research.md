# Research and fact finding

## When this playbook applies

- A literature review or "what does the research say about X".
- Market sizing, competitor analysis, or "who else does this".
- One factual question that needs a sourced answer ("is it true that...", "when did...", "how many...").
- An investigation: tracing who is behind something, what happened, or whether a document, image or quote is genuine.
- A due diligence check on a company, product, person in a public role, or claim in a pitch.
- Comparing options (tools, vendors, treatments, policies) on evidence rather than opinion.

## The expert

Pick the one whose failures this request would cause, and adapt the description to the exact case. It goes on the `Expert:` line of the output block; the rewritten task itself carries the moves, never a persona line (`method/expert.md`).

- **Cochrane systematic reviewer, 15 years, clinical trials and meta-analysis.** Fits any "what does the evidence say" question where studies disagree and the answer will drive a decision.
- **Magazine fact checker, 10 years at a long-form outlet that checks every claim against a primary source.** Fits a single factual question, checking a draft, or vetting quotes and numbers.
- **Open source investigator, 8 years, verification of online video, images and accounts for a newsroom or human rights group.** Fits "is this real", "who posted this first", "where and when was this taken".
- **Competitive intelligence analyst, 12 years, B2B software, works from filings, pricing pages and job ads.** Fits market and competitor research.
- **Intelligence analyst trained in structured analytic techniques, 10 years.** Fits investigations with several plausible explanations and thin, conflicting evidence.

## Moves the expert makes unasked

1. **Write the question in a structured form before searching** (for evidence questions: population, intervention, comparison, outcome; for factual questions: the exact claim, with its date, place and unit).
   Why: a vague question returns sources that answer a different question.
   Check: the question is written down at the top of the notes and every source is tagged with which part it answers.

2. **Decide inclusion and exclusion rules before reading results.**
   Why: rules chosen after reading drift toward the sources that agree with the first impression (this is why Cochrane reviews publish a protocol first).
   Check: the rules are dated before the first source is summarised, and excluded sources are listed with a reason.

3. **Search more than one place and log every search string.**
   Why: one engine or database gives one slice; PRISMA requires the full search to be reported so others can repeat it.
   Check: a search log with source, exact query, date and hit count exists, and a second person could rerun it.

4. **Read laterally before reading deeply.**
   Why: in Wineburg and McGrew's study, professional fact checkers left a site within seconds to see what others said about it, and reached better conclusions faster than historians who read the site itself closely.
   Check: for every source that carries weight, there is a note on who is behind it, taken from outside that source.

5. **Trace every claim to its origin (the T in SIFT).**
   Why: quotes, numbers and images change as they are copied; the third article citing a study often misstates it.
   Check: each key claim links to the first document that made it (the paper, filing, dataset, original upload), not to a write-up of it.

6. **Rate the certainty of each finding, not just the finding.**
   Why: "drug X reduces Y" means little without how sure we are; GRADE rates evidence as high, moderate, low or very low and downgrades for risk of bias, inconsistency, indirectness, imprecision and publication bias.
   Check: every conclusion line carries a certainty label and the reason for any downgrade.

7. **Look for the evidence that would prove the leading answer wrong.**
   Why: Heuer's Analysis of Competing Hypotheses works by trying to refute hypotheses, because evidence consistent with all of them proves nothing.
   Check: there is a list of rival explanations and, for the chosen one, the evidence that rules the others out.

8. **Start from the base rate (the outside view), then adjust.**
   Why: Tetlock's forecasters did better when they anchored on how often things like this usually happen before looking at the specifics.
   Check: the notes state a reference class and its rate before the case specific reasoning.

9. **Count and look for what is missing.**
   Why: unpublished null results, deleted posts, and companies that failed are invisible by default and bias the picture toward success.
   Check: the write-up names at least one source of missing evidence it searched for (trial registries, archived pages, dead competitors) and what it found.

10. **Date everything and note when it was retrieved.**
    Why: prices, headcounts, laws and web pages change; an undated fact cannot be rechecked.
    Check: every claim has a "as of" date and every web source has an archive link or retrieval date.

11. **Separate what the source says from what it means.**
    Why: mixing quotes, numbers and interpretation in one sentence hides which part is the researcher's guess.
    Check: findings are written as "Source says X (quote or number). This suggests Y." with the two parts distinguishable.

12. **Check the numbers yourself.**
    Why: percentages of the wrong base, mixed up units and totals that do not add up are common, and copying a number does not check it.
    Check: every derived number has its calculation shown and recomputes from the cited inputs.

13. **Go to the party closest to the fact.**
    Why: a company's own filing beats a blog about the company, and magazine checkers call the person quoted.
    Check: each high stakes claim rests on the closest available record (the filing, the statement, the original recording); where only a call or an email to a person could settle it, that is flagged for the requester.

## Raw material

What the expert starts from:
- **Evidence questions:** the original studies (full text, not abstracts), trial registries (ClinicalTrials.gov, WHO ICTRP), existing systematic reviews (Cochrane Library), datasets and supplementary files.
- **Factual questions:** the primary record: statute text, court filing, official statistics table, the original interview recording or transcript, the archived web page.
- **Companies and markets:** annual reports and regulatory filings (for US firms, SEC EDGAR 10-K and 10-Q), pricing pages over time (Wayback Machine), job postings (they reveal what a firm is building), product documentation and changelogs, customer reviews in volume, patents.
- **Online media:** the earliest upload, its metadata where available, the account history of the uploader, satellite or street imagery of the claimed location.

Where to get it: Google Scholar, PubMed, and the field's own database; official statistics offices; company investor relations pages; the Internet Archive; reverse image search across several engines.

What to distrust:
- Summaries of studies written by anyone other than the authors (press releases, news, AI summaries), until checked against the paper.
- Single studies with large effects, small samples, or no preregistration.
- Market size figures from paid report vendors quoted without method, and any figure that only appears in marketing.
- Sources that cite each other in a circle (several articles, one original).
- Content that arrived with strong emotion or perfect timing attached.
- Search results ranked by engagement rather than accuracy.

## Methods and tools

- **PRISMA 2020 (27 item checklist and flow diagram):** for any literature review; report how many records were found, screened, excluded (with reasons) and included.
- **Cochrane Handbook (protocol, dual screening, data extraction, risk of bias, GRADE):** when the review drives a decision and needs to survive scrutiny.
- **GRADE:** to rate certainty of each outcome; use it even outside medicine as a discipline for "how sure are we".
- **SIFT (Stop, Investigate the source, Find better coverage, Trace to the original):** for any single claim or unfamiliar source; takes minutes.
- **Lateral reading:** before trusting any website, open new tabs to see what others say about it.
- **Verification Handbook (Silverman, EJC):** for user generated images and video; provenance, source, date, location.
- **Berkeley Protocol on Digital Open Source Investigations:** when findings may be used as evidence; preservation, chain of custody, verification.
- **Analysis of Competing Hypotheses (Heuer):** a matrix of hypotheses against evidence, scoring diagnosticity; for investigations with several explanations.
- **Outside view and Fermi decomposition (Tetlock):** for estimates and forecasts, including market sizing (build it bottom up from countable units, then compare to a top down figure).
- **Claim ledger:** a table of claim, source, origin link, date, certainty, checked by; the core tool for fact checking (the approach in Borel's Chicago Guide to Fact-Checking).
- **Archiving:** save pages to the Wayback Machine or a local copy at retrieval time.

## Independent proof

What shows the result is right, other than the researcher:
- **Reproducible search:** another agent reruns the logged searches and gets substantially the same included set. Run it: give a fresh subagent only the question, the inclusion rules and the search log; compare its included list to yours.
- **Origin check:** every key claim's link opens a primary document that contains the claim. Run it: a script or subagent opens each link and confirms the quoted text or number appears there.
- **Independent second extraction:** a second pass extracts the same numbers from the same sources. Disagreements are resolved against the source, not by vote.
- **Adversarial pass:** a subagent is told to find the strongest evidence against the conclusion. The result stands only if its best counterevidence is addressed in the write-up.
- **Numeric recheck:** a script recomputes every derived figure from cited inputs.
- **Triangulation:** each important claim is supported by at least two sources that do not share an origin.
- **Prediction or ground truth, when one exists:** if the research implies something checkable (a price, a date, a forthcoming event), state it so it can be checked later.

## Amateur mistakes

1. Searching one engine with one phrasing and treating the first page as the literature.
2. Reading abstracts or summaries and citing the paper.
3. Quoting a statistic from a news article without opening the study it came from.
4. Treating the number of sources that agree as strength, when they all copy one origin.
5. Judging a website by its design, its "About" page, or its domain ending instead of reading laterally.
6. Mixing study types (one randomised trial, three surveys, a blog) and weighing them equally.
7. Stopping when the first plausible answer appears, so rival explanations are never tested.
8. Leaving out dates, so a 2019 price or headcount is presented as current.
9. Reporting relative risk ("halves the risk") without the absolute numbers.
10. Using a market report's headline figure without its definition of the market.
11. Presenting a confident conclusion when the honest answer is "the evidence is weak" or "unknown".
12. Citing a source that does not actually say what the sentence claims.

## Scope traps

How "deeper" turns into "bigger" here:
- A question about one claim grows into a survey of the whole field.
- A competitor scan grows from the 5 direct rivals to every adjacent product.
- A literature review grows into a full meta-analysis with new statistics when a structured narrative synthesis answers the question.
- Verification of one image grows into an investigation of the whole account or network.
- "While I am here" side questions are researched instead of listed.

Deeper means: the same question, answered from origins, with certainty stated and rivals tested. It does not mean more questions.

Typical "not doing" items:
- Not running a meta-analysis; narrative synthesis with GRADE style certainty only.
- Not covering adjacent markets or indirect competitors.
- Not searching paywalled databases we cannot access; noted as a gap.
- Not contacting people or companies directly.
- Not answering the side questions found along the way; they are listed at the end.
- Not producing a forecast, only the current evidence.

## Worked example

Request: "Find out if intermittent fasting is better than regular dieting for weight loss."

1. **Expert:** a Cochrane style systematic reviewer in nutrition trials.
2. **Unasked moves (top 5):** fix the question (adults with overweight, intermittent fasting vs continuous calorie restriction, weight change at 6 to 12 months); set inclusion rules first (randomised trials only); start from existing systematic reviews before single trials; rate certainty per outcome; report absolute kilograms, not just "better".
3. **Raw material:** existing systematic reviews and meta-analyses, the randomised trials they include (full text), ClinicalTrials.gov entries; distrust diet books, press coverage and single small trials.
4. **Methods:** PubMed and Cochrane Library searches logged; PRISMA style counts; GRADE certainty; a claim ledger for each number.
5. **Independent proof:** a fresh subagent reruns the search log and lands on the same key reviews; a script confirms each cited number appears in its source; an adversarial pass looks for trials showing the opposite.
6. **Rewritten task:**

```
Question: in adults with overweight, does intermittent fasting lead to more weight loss than continuous calorie restriction at 6 to 12 months?
Start from systematic reviews of randomised trials (Cochrane Library, PubMed), then check their key trials in full text and trial registries.
Log every search (database, query, date, hits). Include randomised trials only.
Report the difference in kilograms with its range and a GRADE certainty level, plus adherence and dropout.
State the strongest evidence against the conclusion and how it was weighed.
Deliverable: a short answer (about a page), with each number linked to its source.
Not doing: a new meta-analysis, other outcomes (blood sugar, longevity), diet recommendations, non randomised studies.
```

## Sources

- Page MJ, McKenzie JE, et al. The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. BMJ 2021;372:n71. https://www.prisma-statement.org/prisma-2020 and https://doi.org/10.1136/bmj.n71
- Higgins J, Thomas J, et al. (eds). Cochrane Handbook for Systematic Reviews of Interventions, version 6.5, 2024. https://training.cochrane.org/handbook/current
- Guyatt GH, et al. What is "quality of evidence" and why is it important to clinicians? BMJ 2008. https://pmc.ncbi.nlm.nih.gov/articles/PMC2364804 ; GRADE Working Group: https://www.gradeworkinggroup.org/ ; BMJ Best Practice, What is GRADE?: https://bestpractice.bmj.com/info/evidence/learn-ebm/what-is-grade/
- Caulfield M. SIFT (The Four Moves), 2019. https://hapgood.us/2019/06/19/sift-the-four-moves/
- Wineburg S, McGrew S. Lateral Reading and the Nature of Expertise: Reading Less and Learning More When Evaluating Digital Information. Teachers College Record 121, 2019. Preprint: https://purl.stanford.edu/yk133ht8603
- Silverman C (ed). Verification Handbook, European Journalism Centre, 2014; and Verification Handbook for Disinformation and Media Manipulation, 2020. https://datajournalism.com/read/newsletters/disinformation-in-the-age-of-media-manipulation
- UC Berkeley Human Rights Center and OHCHR. Berkeley Protocol on Digital Open Source Investigations, 2022. https://humanrights.berkeley.edu/projects/berkeley-protocol-on-digital-open-source-investigations/
- Heuer RJ. Psychology of Intelligence Analysis, CIA Center for the Study of Intelligence, 1999, chapter 8 (Analysis of Competing Hypotheses). https://www.cia.gov/resources/csi/static/Pyschology-of-Intelligence-Analysis.pdf
- Tetlock P, Gardner D. Superforecasting, 2015; summary of Good Judgment Project practices: https://aiimpacts.org/?p=1283
- Borel B. The Chicago Guide to Fact-Checking, 2nd ed., University of Chicago Press, 2023. https://press.uchicago.edu/ucp/books/book/chicago/C/bo194938501.html
