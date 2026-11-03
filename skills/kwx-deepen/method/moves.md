# Step 2: what the expert would do that was not asked

## Name the deep type and the real goal first

Experts sort problems by the principle underneath them; novices sort them by the words on
the surface (Chi, Feltovich and Glaser 1981). So before listing moves:
- **Deep type**: "this is an idempotency problem", "this is a positioning problem, not a
  copy problem", "this is a missing data problem, not a chart problem".
- **Real goal**: the job behind the request. Someone who asks for a faster report may need
  a decision by Friday; someone who asks how to parse a date string may really need to
  store time zones (the XY problem). Say the goal in one line.

## Run a quick pre mortem

Assume the result has already failed. Write the two or three most likely reasons. Each
reason becomes a move or a check (Klein 2007).

## The deeper test

A candidate move counts only if it changes one of these:
- **the inputs**: a better source, the raw data, the real user's words;
- **the method**: a technique, a control, an order of work;
- **the check**: a way to find out the result is wrong.

A move that adds a section, a feature, an option, a file or a deliverable is bigger, not
deeper. It goes to the not doing list. Models already tend to add scope and length, and
judges tend to reward length, so this filter matters more than any single move.

## Keep 3 to 5

Rank by how much each move could change the answer, keep the top 3 to 5, and drop the rest
without comment. Each move is one line: what, and why it matters here. The field
playbooks list the moves experts in each field make most often; pick from them, do not
copy all of them.

## Example

Request: "add a discount code field to checkout".
- Deep type: money correctness under retries.
- Real goal: discounts that never double apply and never go below zero.
- Moves: compute the total on the server from the lines, never trust the client total;
  make the payment call idempotent per quote; define what "first order only" means
  before coding it.
- Not doing: a promotions admin, stacking rules, a coupon marketplace.
