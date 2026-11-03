# Data and analytics

## When this playbook applies

- Answer a question with data: "why did sales drop", "which customers churn".
- Build or change a dashboard or report: "make a KPI dashboard", "weekly report".
- Define or fix a metric: "what is our retention", "the numbers don't match".
- Design or read an experiment: A/B tests, rollouts, "did the change work".
- Work in a spreadsheet: build a model, clean a sheet, fix formulas, merge files.
- Clean or reshape data: CSV exports, joins, deduplication, pipelines.
- Make a chart for a slide, a paper or a decision.

## The expert

Pick the one whose failures this request would cause, and adapt the description to the exact case. It goes on the `Expert:` line of the output block; the rewritten task itself carries the moves, never a persona line (`method/expert.md`).

- **Senior data scientist, 10 years, online experimentation at a large consumer platform.** Fits A/B tests, "did it work", launch decisions, metric sensitivity.
- **Analytics engineer, 7 years, warehouse modelling with SQL and dbt.** Fits metric definitions, dashboards that disagree, pipelines, joins and deduplication.
- **Statistician, 15 years, applied work in health or economics.** Fits causal questions, small samples, surveys, "is this difference real".
- **Information designer, 12 years, dashboards and charts for executives.** Fits dashboards, chart choice, reports read in thirty seconds.
- **Financial analyst, 9 years, spreadsheet models audited by finance.** Fits budgets, forecasts, pricing models, any spreadsheet someone will rely on.

## Moves the expert makes unasked

1. **Writes the decision the analysis will inform, and what result would change it.**
   Why: an analysis with no decision attached grows without end and proves nothing.
   Check: the first lines name the decision, the options, and the threshold that would pick each option.

2. **Defines each metric exactly: numerator, denominator, unit of analysis, time window, filters, time zone.**
   Why: "conversion" or "active user" means different things to different people, which is why dashboards disagree.
   Check: each metric has a one line definition and the query or formula that implements it.

3. **Looks at raw rows before any aggregate: row count, nulls, duplicates, min and max, odd values.**
   Why: test accounts, bots, duplicated events and placeholder dates (1970-01-01) silently drive the result.
   Check: a profile of each input (counts, null rates, distinct keys, ranges) is shown before the first chart.

4. **Reconciles a key total against an independent source of truth.**
   Why: if the revenue in the export does not match finance or billing, every later number is wrong.
   Check: one number (total revenue, user count) is compared with the other system, with the difference explained.

5. **Checks the grain of every table and the row count before and after every join.**
   Why: a one to many join silently multiplies sums; an inner join silently drops rows.
   Check: row counts and the sum of a key measure are printed before and after each join, and they change only as expected.

6. **Keeps the raw data untouched and does every transformation in a saved script, in tidy form.**
   Why: manual edits cannot be reviewed or rerun; tidy data (one variable per column, one observation per row) makes analysis code simple.
   Check: the raw file is unchanged on disk; a script recreates the clean table from it.

7. **Handles time on purpose: time zones, incomplete current periods, late arriving data, calendar effects.**
   Why: a "drop" in the current week is often a week that is not over yet, or a holiday.
   Check: charts mark or exclude partial periods; the time zone used for day boundaries is stated.

8. **Splits by the main segments before concluding (platform, country, new vs returning, plan).**
   Why: Simpson's paradox and mix shift can reverse an aggregate trend.
   Check: the headline result is shown for the main segments, and any reversal is called out.

9. **Shows uncertainty and sample size next to every comparison.**
   Why: a 3 percent lift on 40 users is noise; a point estimate alone invites false confidence.
   Check: comparisons carry n and an interval, or a clear note that the difference is within noise.

10. **For experiments: fixes the primary metric, guardrails, sample size and duration before starting, and does not stop on a peek.**
    Why: repeated peeking at a fixed horizon test inflates false positives far above the nominal 5 percent.
    Check: a written plan with a power calculation exists and predates the results; the analysis uses the planned end date.

11. **Runs a sample ratio mismatch check before reading any experiment result.**
    Why: if a 50/50 split arrives as 50.8/49.2 on a large sample, assignment or logging is broken and the result cannot be trusted.
    Check: a chi-square test on assignment counts is reported before any metric, and p below 0.001 (the usual alarm level) stops the analysis.

12. **Applies Twyman's law: a surprising result gets more checking, not a faster announcement.**
    Why: any figure that looks interesting or different is usually wrong.
    Check: large or surprising effects come with a list of bugs ruled out (logging, filters, joins, bots, SRM).

13. **Separates exploration from confirmation and counts the comparisons made.**
    Why: trying many cuts and reporting the one that looks good is the garden of forking paths.
    Check: the report says how many segments or metrics were examined and labels exploratory findings as such.

14. **Chooses charts by what the eye reads accurately, and gives every number context.**
    Why: position on a common scale is read far better than angle or area; a number without a comparison means nothing.
    Check: bars start at zero, no pie with more than a few slices, every KPI shows a target or prior period, lines are labelled directly.

15. **States the limitations and what was not checked, inside the answer.**
    Why: the reader will otherwise assume the analysis covers more than it does.
    Check: a few lines in the answer name the excluded data, the assumptions and the open questions.

## Raw material

What the expert starts from, and where to get it:

- **Event level or row level data,** not a pre aggregated report. Query the warehouse or production read replica, or ask for the export at the lowest grain.
- **The schema and the data dictionary,** and the code that writes the events (tracking plan, SDK calls, ETL jobs). The writing code tells you what a row really means.
- **The source of truth for money and accounts:** billing system, ledger, payment provider dashboard.
- **Experiment assignment logs,** not only the outcome table.
- **The context log:** release dates, marketing campaigns, outages, tracking changes, holidays. Ask for it or find it in release notes and incident reports.
- **The existing metric definitions,** in the BI tool, dbt models or the spreadsheet formulas, read as code.

What to distrust:

- Dashboard numbers and screenshots: they hide filters, time zones and refresh lag.
- Spreadsheet values without formulas, and any cell typed over a formula.
- Excel auto conversion: gene names, IDs and codes turned into dates or numbers with lost leading zeros.
- Vendor analytics tools' "significance" badges, which often ignore peeking and SRM.
- Averages of skewed data (revenue, session time); look at medians and the distribution.
- Your own query until its row counts are checked.
- Stakeholder recollection of when a change shipped; get the deploy timestamp.

## Methods and tools

- **SQL with explicit grain and CTEs, one step per CTE.** For any warehouse analysis; easy to check row counts step by step.
- **Tidy data and a scripted pipeline (R tidyverse, pandas, polars, DuckDB).** For cleaning and reshaping any export.
- **Data profiling (counts, null rates, distinct keys, histograms).** First step on any new dataset.
- **dbt tests (unique, not_null, relationships, accepted_values) or Great Expectations.** For metrics that feed a dashboard more than once.
- **Power analysis and sample size calculation.** Before any experiment; also to say whether an observed difference could have been detected at all.
- **SRM chi-square test, A/A tests, guardrail metrics.** For every experiment platform and result.
- **Variance reduction (CUPED, using pre period data).** When experiments are underpowered.
- **Difference in differences, interrupted time series, regression with controls.** For "did it work" questions without a randomized test; state the assumptions.
- **Confidence intervals and bootstrap.** For any comparison, especially skewed metrics.
- **Cleveland and McGill encoding ranking; Few's dashboard rules; Tufte's data-ink and small multiples.** For every chart and dashboard.
- **Spreadsheet hygiene (inputs separated from calculations, no hardcoded numbers in formulas, ISO dates, one table per sheet, a checks tab).** For any spreadsheet model.
- **Sensitivity analysis.** For forecasts and models: show how the result moves when each assumption moves.

## Independent proof

What shows the result is right, other than the analyst saying so:

- **Reconciliation with an independent system.** The key total matches billing or finance within a stated tolerance. An agent queries both and prints the difference.
- **Recompute by a second method.** The headline number computed again by a different path (SQL in the warehouse and pandas on the export, or a hand count on a small sample). An agent writes the second computation without reading the first.
- **Rerun from raw.** A fresh agent or clean environment runs the saved script on the raw file and gets the same outputs.
- **Assertions on the data.** Tests that keys are unique, totals are non negative, row counts did not change across a join, dates fall inside the expected range. Run them in the script so they fail loudly.
- **Known answer test.** Feed synthetic data with a planted effect and confirm the pipeline finds it, and feed data with no effect and confirm it finds nothing.
- **Experiment trust checks.** SRM test passes, an A/A run shows about 5 percent false positives, guardrails are flat.
- **Placebo and pre period checks.** For non randomized analyses, the method finds no effect on a fake launch date or on an unaffected group.
- **Holdout or backtest.** For forecasts and models, accuracy on data the model never saw, compared with a simple baseline (last value, seasonal naive).
- **A reader test for dashboards.** Someone who did not build it answers three stated questions from it in under a minute. An agent writes the questions and the expected answers; a person runs it.

## Amateur mistakes

1. Summing after a one to many join and reporting the inflated total.
2. Comparing a partial current week or month with full past ones.
3. Stopping an A/B test the first day it shows significance.
4. Reading an experiment with a broken split (no SRM check).
5. Reporting the one segment out of twenty that looks significant.
6. Mean revenue per user on heavily skewed data, with no median or distribution.
7. Mixing time zones, so "daily" numbers shift by a day for part of the data.
8. Typing over a spreadsheet formula with a number, or a SUM range that misses the last rows (the Reinhart and Rogoff error).
9. Letting Excel turn IDs into dates or drop leading zeros.
10. Bar charts that do not start at zero, dual axis charts, 3D pies, rainbow colour scales for ordered data.
11. Dashboards with 30 numbers and no targets, comparisons or "data as of" time.
12. Calling a correlation in observational data an effect of the change.

## Scope traps

How "deeper" turns into "bigger" here:

- "Show me sales" becomes a full data warehouse with a semantic layer.
- One question becomes forty exploratory cuts, and the report becomes a tour.
- "Did it work" becomes a causal inference research project with five models.
- A dashboard grows to every metric anyone ever asked for.
- A spreadsheet fix becomes a migration to a database and a web app.
- Cleaning one export becomes a reusable pipeline framework for all future exports.

Deeper means the same answer or the same dashboard, now with defined metrics, checked joins, reconciled totals and honest uncertainty.

Typical "not doing" items:

- No new data infrastructure (warehouse, orchestration, BI tool).
- No metrics beyond the ones the decision needs.
- No predictive model when a description answers the question.
- No re-tracking or instrumentation changes; gaps are listed instead.
- No segments beyond the main pre named ones (extra cuts are labelled exploratory).
- No visual styling beyond clear, accessible, consistent charts.

## Worked example

Vague request: "Here's our CSV export. Did the new onboarding flow improve conversion?"

1. **Expert:** senior data scientist, 10 years, online experimentation.
2. **Unasked moves (top 5):** define conversion exactly (paid within 14 days of signup, by user, in UTC) and exclude signups younger than 14 days; find out whether the rollout was randomized, which decides the method; profile the CSV for duplicates, test accounts and nulls; reconcile paid users with billing; split by platform and channel before concluding.
3. **Raw material:** user level rows with signup time, variant or rollout date, payment time; the deploy timestamp from release notes; billing totals for the same period to reconcile.
4. **Methods:** profiling, two proportion comparison with confidence interval (if randomized, plus SRM chi-square); if not randomized, interrupted time series or difference in differences against an unaffected platform, with a placebo date.
5. **Independent proof:** paid user count reconciles with billing; the rate is recomputed in a second tool; placebo date shows no effect; a saved script reruns from the raw CSV.
6. **Rewritten task:**

```
Answer "did new onboarding raise 14 day paid conversion?"
Metric: users paying within 14 days of signup / signups, UTC, test accounts and duplicates removed.
Exclude signups under 14 days old. Reconcile paid users with billing first.
If randomized: SRM check, then difference with 95% CI. If not: before/after vs an unaffected group, placebo date.
Show results overall and by platform and channel; label any other cut exploratory.
Deliver: one page with the answer, the CI, the limits, and the script that reruns from the raw CSV.
Not doing: a dashboard, new tracking, a churn model, segments beyond platform and channel.
```

## Sources

- Hadley Wickham, Tidy Data, Journal of Statistical Software 59(10), 2014: https://vita.had.co.nz/papers/tidy-data.html (DOI https://doi.org/10.18637/jss.v059.i10)
- Wickham, Cetinkaya-Rundel, Grolemund, R for Data Science (2nd ed.): https://r4ds.hadley.nz/
- Kohavi, Tang, Xu, Trustworthy Online Controlled Experiments (Cambridge University Press, 2020), including Twyman's law (ch. 3) and SRM (ch. 21): https://experimentguide.com/
- Kohavi, Deng, Vermeer, A/B Testing Intuition Busters, KDD 2022: https://exp-platform.com/abtestingintuitionbusters/
- Fabijan et al., Diagnosing Sample Ratio Mismatch in Online Controlled Experiments, KDD 2019: https://www.lukasvermeer.nl/publications/papers/2019/07/25/diagnosing-sample-ratio-mismatch-in-online-controlled-experiments.html
- Evan Miller, How Not To Run an A/B Test (peeking): https://www.evanmiller.org/how-not-to-run-an-ab-test.html
- Evan Miller, Sample Size Calculator: https://www.evanmiller.org/ab-testing/sample-size.html
- Gelman and Loken, The garden of forking paths (2013): http://www.stat.columbia.edu/~gelman/research/unpublished/forking.pdf
- Wasserstein and Lazar, The ASA Statement on p-Values, The American Statistician, 2016: https://doi.org/10.1080/00031305.2016.1154108
- Bickel, Hammel, O'Connell, Sex Bias in Graduate Admissions: Data from Berkeley (Simpson's paradox), Science, 1975: https://doi.org/10.1126/science.187.4175.398
- Cleveland and McGill, Graphical Perception, JASA 79(387), 1984: https://doi.org/10.1080/01621459.1984.10478080
- Stephen Few, Common Pitfalls in Dashboard Design (13 pitfalls): https://www.perceptualedge.com/articles/Whitepapers/Common_Pitfalls.pdf
- Edward Tufte, The Visual Display of Quantitative Information: https://www.edwardtufte.com/
- Broman and Woo, Data Organization in Spreadsheets, The American Statistician, 2018: https://doi.org/10.1080/00031305.2017.1375989
- Ziemann, Eren, El-Osta, Gene name errors are widespread in the scientific literature, Genome Biology, 2016: https://doi.org/10.1186/s13059-016-1044-7
- Herndon, Ash, Pollin, Does high public debt consistently stifle economic growth? A critique of Reinhart and Rogoff, Cambridge Journal of Economics, 2014: https://doi.org/10.1093/cje/bet075
- European Spreadsheet Risks Interest Group (horror stories archive): https://eusprig.org/
- dbt, Data tests: https://docs.getdbt.com/docs/build/data-tests
- Rodden, Hutchinson, Fu, Measuring the User Experience on a Large Scale (HEART), CHI 2010: https://research.google/pubs/pub36299/
- Google SRE book, ch. 4 Service Level Objectives (defining indicators precisely): https://sre.google/sre-book/service-level-objectives/
