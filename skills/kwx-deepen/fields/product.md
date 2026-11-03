# Product and strategy

## When this playbook applies

- Product ideas: "is this a good idea", "what should we build", new feature or new product.
- Roadmaps: plan the next quarter or year, prioritize a backlog, choose between bets.
- Pricing: set a price, design tiers, change a pricing model, discounting.
- Positioning: describe what the product is and for whom, homepage message, category choice.
- Marketing and launch: launch plan, go to market, campaign, channel choice, announcement copy.
- Choosing a tool or vendor: buy versus build, compare SaaS options, pick a supplier or platform.

## The expert

Pick the one whose failures this request would cause, and adapt the description to the exact case. It goes on the `Expert:` line of the output block; the rewritten task itself carries the moves, never a persona line (`method/expert.md`).

- Product leader at a product company, 15+ years, trained in empowered teams and discovery (the Marty Cagan or Teresa Torres school). Fits: product ideas, feature requests, roadmaps.
- Pricing strategist at a monetization consultancy, 10+ years, B2B and B2C SaaS (the Simon-Kucher, Madhavan Ramanujam type). Fits: pricing, packaging, tiers, monetization of a new product.
- Positioning consultant, 20+ years in B2B tech product marketing (the April Dunford type). Fits: positioning, messaging, homepage, sales narrative, category.
- Launch and growth marketer, 10+ years, brand and performance both, reads effectiveness data (the Binet and Field school). Fits: launch plans, campaigns, channel mix.
- Procurement lead or staff engineer who has run vendor selections and migrations, 10+ years. Fits: tool and vendor choice, buy versus build.

## Moves the expert makes unasked

1. Restate the request as an outcome (a measurable change in customer or business behaviour), not an output.
   Why: Torres starts every opportunity solution tree from a desired outcome; features are only candidate means.
   Check: the task names one metric that should move and by roughly how much.
2. Name the four risks for the idea: value, usability, feasibility, business viability (Cagan), and say which is the biggest.
   Why: teams test the easy risk (can we build it) and skip the one that kills products (will anyone choose it).
   Check: each risk is rated and the riskiest one has a planned test.
3. Ask for the job the customer is hiring the product to do, including functional, emotional and social parts (Christensen).
   Why: Christensen argues that demographic segments rarely explain why people switch, and the job usually does.
   Check: a job statement exists in the form "when [situation], I want to [motivation], so I can [outcome]".
4. Get stories of past behaviour, not opinions about the future ("tell me about the last time you...").
   Why: people are poor predictors of their own future choices, and polite about your idea (Fitzpatrick, The Mom Test).
   Check: the evidence cites specific past events, dates or spend, not "would you use".
5. Map the forces on a switch: push of the current situation, pull of the new, anxiety about the new, habit of the present (Moesta and Spiek).
   Why: many products lose to "do nothing"; reducing anxiety and habit often beats adding features.
   Check: the plan addresses at least one anxiety and one habit, not only pull.
6. List the real competitive alternatives, including spreadsheets, an intern, or doing nothing (Dunford).
   Why: the customer's comparison set decides what counts as better, not the analyst's competitor list.
   Check: the alternatives list includes the status quo and at least one non-product option.
7. Position in Dunford's order: alternatives, then unique capabilities, then the value they enable, then the customers who care most, then the market category.
   Why: choosing the category first locks in the wrong comparison.
   Check: the positioning document follows that order and each value claim traces to a capability.
8. Have the willingness to pay conversation before the product is designed (Ramanujam).
   Why: products designed first and priced later are often priced into a corner; price should shape the product.
   Check: price ranges come from customer research with segments, not from cost plus or a competitor's page alone.
9. Segment by needs and willingness to pay, then build packages (good, better, best) around the segments, with a clear "leader" feature per tier.
   Why: one price for everyone leaves money from high value users and loses price sensitive ones.
   Check: each tier is tied to a named segment and a reason to upgrade.
10. Define the success metric and the kill criteria before the launch or the build.
    Why: without a preset threshold every result gets rationalized as a win.
    Check: a written "we continue if X by date Y, we stop if Z" exists.
11. Plan the launch for both brand and activation, and say the split (Binet and Field found about 60 brand and 40 activation on average in IPA data, varying by category).
    Why: all activation buys short spikes and decays; all brand cannot be measured this quarter.
    Check: the plan names both long and short term objectives and their metrics.
12. For a vendor choice, write the requirements and weights before looking at vendors, and include exit cost and data portability.
    Why: demos anchor the requirements; lock in shows up only when leaving.
    Check: the scoring sheet predates the shortlist; there is an "exit" row.
13. Price a vendor by total cost of ownership over 3 years: licences, seats growth, implementation, training, integration, migration out.
    Why: list price is often a minor part of the cost.
    Check: a 3 year TCO table with assumptions exists for each finalist.
14. Run the riskiest assumption test that is cheapest, before building (fake door, concierge, prototype, presale).
    Why: discovery is about learning faster than building.
    Check: at least one assumption test with a pass threshold is in the plan.

## Raw material

- Customer interviews (recordings or verbatim notes), support tickets, sales call notes, churn and cancellation reasons. Get them from the CRM, help desk, call recorder. Distrust summaries written by the team that wants the feature.
- Product analytics: event data, funnels, cohort retention. Distrust single dashboard screenshots without the query and date range.
- Win and loss records with the reason in the customer's words. Distrust "lost on price" without a follow up question: it often means lost on value.
- Real prices paid: invoices, discounts given, contract values by segment. Distrust the price list as a description of what people pay.
- Competitor and alternative sources: their pricing pages (archived via the Wayback Machine for history), public docs, changelogs, reviews on G2 or app stores read in full. Distrust analyst quadrants and "top 10 tools" articles, which are often paid placements.
- For vendors: the actual contract and order form, the SLA, the data processing agreement, the API docs, the status page history, a reference call with a current customer you found yourself. Distrust the sales deck and case studies chosen by the vendor.
- Market data from primary sources: public company filings (SEC EDGAR 10-K), government statistics, industry association reports. Distrust market size numbers from press releases of research vendors.

## Methods and tools

- Opportunity solution tree (Torres): to connect an outcome to opportunities, solutions and assumption tests; use for product ideas and roadmaps.
- Story based interviews, weekly (Torres) and The Mom Test question rules (Fitzpatrick): any time a decision depends on what customers do.
- Jobs to be Done: switch interview and four forces (Moesta), job statements (Christensen); for understanding why people buy or leave.
- Outcome Driven Innovation (Ulwick): desired outcome statements rated for importance and satisfaction; opportunity score = importance + max(importance minus satisfaction, 0); for ranking needs across a market.
- Four big risks (Cagan): to choose what to test first.
- Pricing research: willingness to pay interviews, Van Westendorp price sensitivity meter (four questions: too cheap, cheap, expensive, too expensive), Gabor Granger, conjoint or MaxDiff for feature value; use Van Westendorp for a range, conjoint for packaging trade offs.
- Positioning (Dunford, Obviously Awesome): the 10 step process with the five components.
- Sean Ellis product market fit survey ("how would you feel if you could no longer use the product?", 40 percent "very disappointed" as a rough bar): after launch, on active users, paired with retention.
- Pre-mortem (Klein): before committing a roadmap or launch, imagine it failed and list why.
- Weighted decision matrix with weights set first, plus 3 year TCO: vendor choice.
- RICE or cost of delay: only to rank items that already passed discovery, never as a substitute for it.

## Independent proof

- Customer behaviour, not approval: signups to a fake door, preorders, signed letters of intent, paid pilots, activation and week 4 retention. An agent can define the event, read the analytics export, and compute the rate against the preset threshold.
- Interview evidence an outsider can audit: the quotes and dates behind each opportunity. An agent checks that each claim in the plan links to at least two independent customer stories.
- Pricing: actual conversion and expansion at the tested price in an A/B or segmented rollout, or the Van Westendorp acceptable range per segment with the number of respondents stated (a handful of answers is a hint, not a range).
- Positioning: a five second or first click test on the homepage with target customers ("what does this do, who is it for, what is it instead of?"), and sales cycle or win rate changes over the next quarter.
- Launch: pre-registered metrics (reach, signups, activation, cost per acquired user) checked against the plan after the window closes.
- Vendor: a paid or free trial on your own real data with scripted test cases, a reference call with a customer you found, and the contract read for exit, price increase caps and data return.
- Pre-mortem output reviewed by someone outside the team.

## Amateur mistakes

- Asking "would you use this?" or "how much would you pay?" and treating a yes as evidence.
- Building the full product before testing the riskiest assumption.
- Pricing at cost plus margin, or at "a bit below the leader", with no customer research.
- One pricing tier for every segment, or tiers split by arbitrary usage limits nobody understands.
- Positioning that lists features without saying the value they create or what they replace.
- Picking a market category because it is hot rather than because it frames the product's strengths.
- A roadmap that is a dated list of features with no outcomes, so every date slip is a crisis.
- Prioritizing by the loudest customer or the highest paying one alone.
- A launch that is a single announcement day with no follow up and no definition of success.
- Choosing a vendor from a demo and a comparison article, without trying it on real data.
- Ignoring the cost and pain of leaving a vendor (data export, contract term, auto renewal).
- Surveying everyone for product market fit, including people who signed up once and left.

## Scope traps

"Deeper" means the same decision made with better evidence. It turns into "bigger" when:

- "Should we build X" becomes a full product strategy and vision document.
- A pricing question becomes a company wide packaging redesign across all products.
- A launch plan grows to every channel at once.
- A vendor choice becomes a long RFP with twenty vendors.
- Discovery never ends: more interviews are scheduled instead of making the call.

Typical "not doing" items: a full product vision, a brand redesign, building the feature, more than 3 finalist vendors, paid acquisition setup, a pricing change for existing customers, new market entry.

## Worked example

Vague request: "Help me figure out pricing for my app." (A B2B SaaS tool, early customers, currently one flat price.)

1. Expert: a pricing strategist, 10+ years in B2B SaaS monetization.
2. Unasked moves (top 5): segment by need and willingness to pay; find the value metric that grows with customer value; hear willingness to pay from customers before redesigning; include the status quo alternative; set a success metric and a test before changing prices.
3. Raw material: current invoices and discounts, usage data per account, 8 to 12 customer and prospect interviews, lost deal notes, 3 alternatives' public pricing pages.
4. Methods: willingness to pay interviews, Van Westendorp on prospects, good better best packaging, value metric analysis.
5. Proof: Van Westendorp acceptable range per segment; new price tested on new signups only, with conversion and average revenue compared to the old price over a set window.
6. Rewritten task:

```
Propose pricing for new customers of the app: one value metric and 2 or 3 tiers.
Base it on usage data, invoices, 10 willingness to pay interviews (the owner runs them from a script written here) and Van Westendorp per segment.
Each tier names its segment, the feature that justifies it, and a price range with the evidence.
Include the status quo alternative and what it costs the customer.
Define the test: new signups only, 6 weeks, pass if trial to paid holds and revenue per account rises.
Deliver: a 2 page proposal plus the evidence table.
Not doing: changing existing customers' prices, enterprise deals, new features, a pricing page redesign.
```

## Sources

- Marty Cagan, Inspired (2nd ed., Wiley, 2018); The Four Big Risks: https://svpg.com/four-big-risks/
- Teresa Torres, Continuous Discovery Habits (2021); Opportunity Solution Trees: https://www.producttalk.org/opportunity-solution-trees/
- Teresa Torres, story based customer interviews: https://www.producttalk.org/2024/04/story-based-customer-interviews/
- Clayton Christensen, Taddy Hall, Karen Dillon, David Duncan, Know Your Customers' Jobs to Be Done, HBR, September 2016: https://hbr.org/2016/09/know-your-customers-jobs-to-be-done
- Anthony Ulwick and Strategyn, opportunity scoring: https://strategyn.com/quantify-your-customers-unmet-needs
- Bob Moesta and Chris Spiek, the four forces of progress: https://jobstobedone.org/the-four-forces/
- Rob Fitzpatrick, The Mom Test (2013): https://www.momtestbook.com/
- Madhavan Ramanujam and Georg Tacke, Monetizing Innovation (Wiley, 2016): https://www.simon-kucher.com/en/insights/monetizing-innovation
- Van Westendorp price sensitivity meter: https://en.wikipedia.org/wiki/Van_Westendorp%27s_Price_Sensitivity_Meter
- April Dunford, Obviously Awesome (2019): https://www.aprildunford.com/books
- Les Binet and Peter Field, The Long and the Short of It (IPA, 2013): https://ipa.co.uk/knowledge/publications-reports/the-long-and-the-short-of-it-balancing-short-and-long-term-marketing-strategies
- Sean Ellis product market fit survey (overview): https://learningloop.io/plays/product-market-fit-survey
- Gary Klein, Performing a Project Premortem, HBR, September 2007: https://hbr.org/2007/09/performing-a-project-premortem
- Nielsen Norman Group, When to use which UX research methods: https://www.nngroup.com/articles/which-ux-research-methods/
