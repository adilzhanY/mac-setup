# Business, money and legal

## When this playbook applies

- Budgets and financial estimates: project budget, cost estimate, forecast, runway, business case, unit economics.
- Contracts and terms: draft or review a contract, terms of service, privacy policy, NDA, freelance agreement, vendor terms.
- Hiring: write a job ad, design an interview process, assess candidates, decide employee versus contractor.
- Job applications: CV, cover letter, application answers, interview preparation, offer negotiation.
- Operations: process design, SOPs, capacity planning, scheduling, supplier management, recurring admin.

## The expert

Pick the one whose failures this request would cause, and adapt the description to the exact case. It goes on the `Expert:` line of the output block; the rewritten task itself carries the moves, never a persona line (`method/expert.md`).

- Finance lead or CFO at a growing company, 15+ years, budgets and forecasts that boards rely on, trained in reference class forecasting (the Flyvbjerg and Kahneman school). Fits: budgets, estimates, business cases, runway.
- Commercial lawyer, 15+ years, contract drafting and review in the relevant jurisdiction (drafts in the Ken Adams style: clear categories of obligation, discretion, condition). Fits: contracts, terms, privacy documents, NDAs.
- Head of talent or industrial and organizational psychologist, 10+ years, structured selection. Fits: job ads, interview design, candidate assessment.
- Senior recruiter or hiring manager in the target industry, 10+ years, has read thousands of applications. Fits: CVs, cover letters, application answers, negotiation.
- Operations manager, 15+ years, lean and process improvement in service or manufacturing. Fits: process design, SOPs, capacity, suppliers.

## Moves the expert makes unasked

1. State the jurisdiction and the date at the top of anything legal, tax or employment related.
   Why: law differs by country and state and changes; a rule vacated last year reads the same in a blog as one in force (for example the FTC click to cancel rule, vacated by the Eighth Circuit on 8 July 2025).
   Check: the output names the jurisdiction, the date the law was checked, and the version of each source.
2. Cite the official source: the statute, regulation, regulator guidance or tax authority page, not a summary or a law firm blog.
   Why: summaries drop conditions and exceptions, and go stale.
   Check: each legal or tax claim has a link to EUR-Lex, legislation.gov.uk, the US Code or eCFR, a regulator (ICO, FTC, EEOC, SEC) or a tax authority (IRS, HMRC), with the section number.
3. Say where professional advice is required, and say it specifically, not as a blanket disclaimer.
   Why: an experienced generalist knows where the cost of being wrong is high and the answer depends on facts only a licensed professional can weigh.
   Check: the output lists the specific points that need a lawyer, accountant or tax adviser and why (for example: signing anything with uncapped liability, a dispute or threat of one, employee termination, worker classification, cross border tax, equity, regulated activities, amounts that matter to the business).
4. Estimate from the outside view first: find a reference class of similar past projects and their actual outcomes, then adjust (Kahneman and Lovallo, Flyvbjerg).
   Why: inside view estimates built from task lists are reliably optimistic (the planning fallacy).
   Check: the estimate names its reference class, its source and the distribution, before the bottom up figure.
5. Give a range with stated confidence, not a point number, and name the assumptions that drive it.
   Why: a single number hides the risk; the drivers are what the reader must watch.
   Check: low, likely, high values exist, with the 3 to 5 assumptions that move them most.
6. Model the fat tail: ask what happens in the worst 10 to 20 percent of cases, not only the average.
   Why: Flyvbjerg's data show IT projects have fat tails, where a minority of projects overrun by several times.
   Check: a contingency or downside scenario is sized from the reference class, not a flat 10 percent.
7. Run a pre-mortem on the budget, contract or plan: assume it failed and list why (Klein).
   Why: prospective hindsight surfaces risks that people do not raise in a normal review.
   Check: a list of failure causes and the mitigation for each top cause.
8. Read a contract by category of language: obligations (shall), discretion (may), conditions, prohibitions, representations (Adams).
   Why: the risk is in who must do what and what happens if they do not, not in the headings.
   Check: a table of each party's obligations, the conditions on them, and the remedies.
9. Find the clauses that carry the money and the exit: liability cap and exclusions, indemnities, term and renewal, termination rights, price increases, payment terms, IP ownership, data protection, governing law and venue.
   Why: these decide the outcome when things go wrong.
   Check: each is located with its clause number and summarized in plain words, with a flag if missing or one sided.
10. For hiring, define the job outputs and the must have skills first, then use structured interviews with the same questions and a scoring rubric for every candidate, plus a work sample.
    Why: structured interviews are among the most valid selection methods in the meta-analytic evidence (Sackett et al. 2022), and unstructured ones invite bias.
    Check: a written rubric with anchored scores exists before the first interview.
11. Check the ad and process against the equal employment rules of the jurisdiction (for example EEOC in the US, Equality Act 2010 in the UK), and against AI rules if automated screening is used (the EU AI Act lists recruitment AI as high risk in Annex III).
    Why: wording like "young, energetic team" or a screening tool can be discriminatory without intent.
    Check: the ad and each screening step were reviewed against the named official guidance.
12. Classify workers by the actual working relationship, using the official test (IRS common law factors in the US, HMRC CEST and employment status guidance in the UK).
    Why: the label in the contract does not decide status; the real control and dependence do.
    Check: the decision walks through the official factors and notes where to get a formal ruling (IRS Form SS-8, CEST result saved).
13. For an application, start from the posting and the hiring manager's problem, and make every CV line an outcome with a number.
    Why: screeners skim; in one Ladders eye tracking study the first scan averaged 7.4 seconds and focused on titles and headings.
    Check: each requirement in the posting maps to a line of evidence in the CV or letter.
14. For operations, measure the current process before redesigning it: arrival rate, cycle time, work in progress, error rate.
    Why: Little's Law (work in progress = throughput times cycle time) shows where the queue is; intuition usually points at the wrong step.
    Check: a baseline with real counts over a stated period exists.

## Raw material

- Actuals: bank exports, ledger, past invoices, timesheets, past project budgets versus final costs. Get them from the accounting system or bank. Distrust budgets from previous plans; they show intentions, not outcomes.
- Reference class data: your own past projects, public post mortems, Flyvbjerg's published overrun studies, industry benchmarks with a named sample. Distrust a single analogy chosen because it looks like success.
- Official prices and rates: tax rates and thresholds from the tax authority, wage data from government statistics (US BLS OES, UK ONS ASHE), filings of comparable companies on SEC EDGAR or Companies House. Distrust salary sites and tax calculators without a stated source and year.
- The contract itself, every schedule, order form and document incorporated by reference (terms linked by URL, policies, SLAs). Distrust the cover email's description of what it says.
- The law in force: EUR-Lex (EU), legislation.gov.uk (UK), US Code and eCFR (US federal), state codes, regulator guidance pages. Distrust law firm alerts and blog posts, which are useful for finding the source but may be outdated or one sided.
- For hiring: the work the role actually does (outputs, tools, last year's problems), performance data of current people in the role. Distrust copied job descriptions.
- For applications: the job posting saved in full, the company's own site, annual report, recent news, the hiring manager's public writing. Distrust generic "what recruiters want" lists.
- For operations: logs, tickets, timestamps, order data, observation of the process as done (not as documented). Distrust the SOP as a picture of reality.

## Methods and tools

- Reference class forecasting (Lovallo and Kahneman 2003, Flyvbjerg): every estimate of cost or time for a project.
- Three point estimates and Monte Carlo simulation (a spreadsheet or a short Python script): when several uncertain drivers combine.
- Pre-mortem (Klein, HBR 2007): before approving a budget, signing a contract, or launching a process.
- Driver based models and sensitivity tables (tornado chart): to show which assumption matters most.
- Unit economics: contribution margin, customer acquisition cost, payback period; for any business case.
- Contract categories of language (Adams, A Manual of Style for Contract Drafting): to draft and to review.
- Clause checklist for money and exit (liability, indemnity, termination, renewal, IP, data, law and venue): every review.
- GDPR Article 28 checklist and the Commission's standard contractual clauses: any contract where one party processes personal data for the other.
- Structured interviews with behavioural and situational questions, anchored rating scales, work samples: hiring.
- Official status tools: IRS Form SS-8 and Topic 762 (US), HMRC CEST (UK): worker classification.
- Lean tools: process mapping, value stream mapping, Little's Law, checklists, five whys: operations.

## Independent proof

- Reconciliation: the budget's baseline ties to the ledger or bank totals for the same period. An agent can sum the exports and compare.
- Back testing: apply the estimating method to 3 to 5 finished past projects and compare the predicted with the actual results.
- Formula and model checks: recompute key totals independently (a second script or spreadsheet), and vary each driver to confirm the sensitivity table.
- Source check for every legal or tax claim: the agent opens the cited official page, confirms the section says what is claimed, and records the date checked and whether the page shows amendments, pending changes or court decisions.
- Professional review where step 3 flagged it: the output is framed as a brief for the lawyer or accountant (facts, questions, documents), and only the professional's answer settles those points.
- Contract redline compared against the original with a diff tool, so every change is visible to the other side.
- Hiring: inter rater agreement on the rubric (two interviewers score the same candidate independently), and later, performance of hires against the scores.
- Application: the posting to evidence map is complete; a person from the target field reads it for 30 seconds and says what role it fits and the top 3 strengths; outcome tracked as response rate per version.
- Operations: the same metric measured before and after, over the same length of period, with the change in work in progress and cycle time.

## Amateur mistakes

- A single point estimate built bottom up from a task list, with a flat 10 percent contingency.
- Mixing nominal and real figures, or one off and recurring costs, in one total.
- Forgetting taxes, payment fees, currency conversion, or the cost of the person's own time.
- Quoting a law or tax rate from a blog without the jurisdiction or date, or applying US rules to an EU business.
- Calling a summary "the law": citing a law firm alert instead of the statute or regulator.
- A generic "this is not legal advice" line instead of naming the exact points that need a lawyer.
- Reviewing only the main agreement and missing the terms linked by URL that can change at any time.
- Accepting uncapped indemnities or auto renewal with a short notice window without noticing.
- Copying a template contract from another country or another type of deal.
- Job ads full of adjectives and a long wish list, and interviews where each candidate gets different questions.
- Calling someone a contractor because the contract says so, while controlling their hours and tools like an employee.
- CVs that list duties instead of outcomes, and one cover letter sent unchanged to every company.

## Scope traps

"Deeper" means the same deliverable with the right evidence, sources and limits. It turns into "bigger" when:

- A project budget becomes a full company financial model with three statements.
- A contract review becomes a redraft of the whole agreement, or a review of every other contract the company has.
- A job ad becomes a full employer brand and careers site.
- A CV update becomes a career change plan.
- An SOP fix becomes a full process reengineering program or a new software system.
- The agent starts acting as the lawyer or accountant instead of preparing the brief for one.

Typical "not doing" items: legal advice on the flagged points (prepared as questions instead), tax filing, a full redraft, other jurisdictions than the one named, negotiation with the other party, a financial model beyond the asked scope, choosing payroll or HR software.

## Worked example

Vague request: "Can you check this freelance contract before I sign?" (A software developer in Germany, client in the US, 6 month engagement.)

1. Expert: a commercial lawyer with 15+ years in cross border IT services contracts, working from the governing law named in the document.
2. Unasked moves (top 5): state jurisdictions (the contract's governing law, plus German rules on the freelancer's side) and the date checked; locate the money and exit clauses; flag false self employment risk under German law; check data protection terms if client personal data is handled; list exactly what needs a licensed lawyer.
3. Raw material: the full contract with every schedule and linked terms, the statement of work, the client's email offer; official sources: the German Social Code (SGB IV section 7) and the Deutsche Rentenversicherung status procedure page, GDPR on EUR-Lex.
4. Methods: obligations and conditions table, clause checklist, GDPR Article 28 check, pre-mortem ("the engagement went badly, what in this contract made it worse?").
5. Proof: every flag cites a clause number and an official source with its date; a lawyer confirms the flagged items.
6. Rewritten task:

```
Review the attached freelance contract (governing law as stated in it; freelancer in Germany; checked on today's date).
Produce: a table of each party's obligations, conditions and remedies, with clause numbers.
Flag and explain in plain words: liability, indemnity, IP, payment terms, termination, renewal, governing law, data protection.
Note false self employment risk using the official German sources (SGB IV section 7, DRV status procedure).
Cite every legal point to the statute or regulator page, with the date checked.
End with the 3 to 5 questions a licensed lawyer must answer before signing, and why.
Not doing: legal advice on those questions, a full redraft, negotiating with the client, US state law analysis.
```

## Sources

- Dan Lovallo and Daniel Kahneman, Delusions of Success: How Optimism Undermines Executives' Decisions, HBR, July 2003: https://hbr.org/2003/07/delusions-of-success-how-optimism-undermines-executives-decisions
- Bent Flyvbjerg, comment on Lovallo and Kahneman (strategic misrepresentation): https://arxiv.org/pdf/1305.0741
- Reference class forecasting overview: https://en.wikipedia.org/wiki/Reference_class_forecasting
- Bent Flyvbjerg and Dan Gardner, How Big Things Get Done (Currency, 2023).
- Gary Klein, Performing a Project Premortem, HBR, September 2007: https://hbr.org/2007/09/performing-a-project-premortem
- Kenneth A. Adams, A Manual of Style for Contract Drafting (5th ed., ABA, 2023); categories of contract language quick reference: https://www.adamsdrafting.com/wp-content/uploads/2023/06/MSCD5-Quick-Reference-for-the-Categories-of-Contract-Language.pdf
- Regulation (EU) 2016/679 (GDPR), Article 28: https://eur-lex.europa.eu/eli/reg/2016/679/oj
- ICO, what needs to be included in a controller and processor contract (UK GDPR): https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/accountability-and-governance/contracts-and-liabilities-between-controllers-and-processors-multi/what-needs-to-be-included-in-the-contract/
- Eighth Circuit vacates the FTC click to cancel rule, Custom Communications v. FTC, 8 July 2025 (summary): https://www.gunder.com/en/news-insights/insights/client-insight-eighth-circuit-vacates-ftcs-click-to-cancel-rule
- IRS Topic 762, Independent contractor vs. employee: https://www.irs.gov/taxtopics/tc762
- HMRC, check employment status for tax (CEST): https://www.gov.uk/guidance/check-employment-status-for-tax
- EEOC, prohibited employment policies and practices: https://www.eeoc.gov/prohibited-employment-policiespractices
- EU AI Act, Annex III high risk systems (employment): https://artificialintelligenceact.eu/annex/3/
- Sackett, Zhang, Berry and Lievens, revisiting validity of selection procedures (2022) and commentary: https://www.cambridge.org/core/product/A20984B138319E3D432E643978BF026D
- Ladders eye tracking study 2018 (report coverage): https://www.hrdive.com/news/eye-tracking-study-shows-recruiters-look-at-resumes-for-7-seconds/541582/
- US Small Business Administration, calculate your startup costs: https://www.sba.gov/business-guide/plan-your-business/calculate-your-startup-costs
- US BLS Occupational Employment and Wage Statistics: https://www.bls.gov/oes/
- SEC EDGAR full text search: https://www.sec.gov/edgar/search/
- Little's Law: https://en.wikipedia.org/wiki/Little%27s_law
