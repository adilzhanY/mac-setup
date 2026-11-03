# Step 3: get the raw material

A summary is a map to the original, not the original. In one study, 33 to 40 percent of
university health press releases claimed more than the paper did; one estimate, from how
misprints spread through citations, is that only about one in five people who cite a paper
read it; and in one test language models invented 55 percent (GPT-3.5) and 18 percent
(GPT-4) of the references they gave. Fetch the source, do not recall it
(`sources/research_notes/raw-material-and-proof.md`, part A).

## Name the primary record

| Field | Primary | Distrust |
|---|---|---|
| Software | the code, the logs, the failing test, the spec, the RFC, the changelog of the exact version | blog posts, memory of how a library usually works |
| Data | the raw table and how it was collected | a chart, a dashboard number, last quarter's slide |
| Research | the original paper, its methods and data, the systematic review | the abstract, the press release, news |
| Law and money | the statute, the regulator's page, the filing, the contract | summaries, forums, old guides |
| Product and design | real users' words and behaviour, support tickets, usage data, the current product | opinions, trends, competitors' marketing |
| Writing | the reader's actual situation, the brief, the source documents | templates |

The field playbooks have the full list for each field.

## Fetch, then record

- Fetch anything load bearing: numbers, quotes, citations, versions, laws, file contents,
  prices. Stable, widely known facts may come from memory; long tail, recent or contested
  ones may not.
- Quote the part you rely on and keep its location: URL, file and line, table and row,
  section and paragraph. A claim with no supporting quote is dropped or marked as a guess.
- Note the date and status: an RFC can be obsoleted, a paper retracted, a law amended, a
  page edited.
- Never draw a conclusion from a law, rate, price or version that was not fetched in this
  task. If it could not be fetched, mark the point as not checked instead of stating it.
- When the primary record cannot be reached, say so in the rewrite and name what was used
  instead.

## Check a secondary source sideways

Before trusting a source you do not know, leave it and see what independent sources say
about it (lateral reading, Wineburg and McGrew 2017). The SIFT steps work in seconds: Stop,
Investigate the source, Find better coverage, Trace claims to the original (Caulfield).

## Prefer what people did over what they say

Usage data, receipts, logs and past behaviour beat predictions and stated intentions
(The Mom Test, for product and research questions).
