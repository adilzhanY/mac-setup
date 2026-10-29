# Pricing psychology: contrast, anchoring, decoy, loss aversion

Prices are judged relative to what was seen just before. "That first number becomes the ruler they measure everything else against" (uxpeak, UX psychology video). Control the order and the context of numbers, make the cheapest honest reading the easy one, and never fake a price, a discount or a deadline. Layout rules for full pricing pages live in the platform folder; this file is the psychology.

## Contents

1. Contrast effect and anchoring
2. Decoy effect (honest use)
3. Loss aversion in pricing and retention
4. Making the price easy to read
5. Plan cards that make the upgrade delta obvious
6. Forbidden
7. Checks

---

## 1. Contrast effect and anchoring

- The brain does relative, not absolute, evaluation. After $1,900, $50 barely registers.
- Examples given: a restaurant lists a $90 Wagyu steak so the $40 salmon looks reasonable; estate agents show a slightly overpriced house first ($700,000 shown).

Rules:

1. Never show an add on price alone on its own page. The AppleCare+ style "before": a standalone page, "$49.99 /month, Cancel anytime", "Add AppleCare+", "No thanks", "Skip". The user computes $599.88 a year and leaves.
2. Show the add on right after the larger price it relates to: in the cart or order review, under the product. The "after": "Order Review", MacBook Pro 14" at $1,899, a divider label "RECOMMENDED FOR YOU", an add on card "Complete Protection / Full coverage for damage, theft, and repairs", "$49 /month", a small green pill "Just 2.6%", a compact "Add" button, then Subtotal $1,899.00, Shipping Free, Total $1,899.
3. A relative label is allowed when it is arithmetically true and honest about the period. Note the video's "Just 2.6%" compares $49 per month with a one time $1,899: that hides the yearly cost. Honest versions: "$49/mo, about $588/yr" or a percentage over the same period.
4. The add on is never preselected. It is offered with an "Add" button, unticked.
5. Decide deliberately which number the user sees first on any pricing screen. Lead with the plan most users should pick, not with an inflated decoy (see section 2).

## 2. Decoy effect (honest use)

Adding a dominated option shifts choice toward a target (the classic Economist print vs web plus print example). Use only this honest form:

- Every tier must be a real option that some rational customer would pick. If nobody should ever buy a tier, delete it.
- Do not invent a tier whose only purpose is to make another look cheap.
- Fix ladders that confuse instead: in the vibe coded LinkGuard pricing, "Standard" at $2 was cheaper than "Hobby" at $3 (because Standard was discounted). Kole Jain dropped Hobby. "At least one has to go."
- A "Recommended" highlight is allowed when it is the plan you would honestly recommend for the stated use. Do not mark the most expensive plan "Most popular" unless it is measured.

## 3. Loss aversion in pricing and retention

- Losses weigh about twice as much as equal gains (Kahneman, as cited by uxpeak). Gain framing ("Get 100GB of storage and unlock premium features", "Upgrade Now", "Maybe Later") is the weaker motivator.
- The video's strong version: "Your Files Will Be Deleted", "In 3 days your oldest files will be permanently deleted", "Files at risk: Project_Proposal.pdf, Design_Mockups.fig, and 12 other / Total: 2.8 GB will be lost", button "Protect My Files Now", dismiss "I'll Risk It".

Keep the specificity, drop the manipulation:

1. Use loss framing only for a loss that is real and scheduled in the system: storage really full, files really queued for deletion, a trial really ending on a date.
2. Be concrete: the user's own items by name, a count ("and 12 other"), the total ("2.8 GB"), the exact date.
3. Always offer the free way out next to the paid one: "Free up space" or "Review files" beside "Upgrade storage".
4. The dismiss is neutral: "Not now". "I'll Risk It" is confirmshaming and forbidden.
5. Danger colour only for the real loss: red warning tile, pale red inset, red on the date and total. The primary action stays in the brand colour.
6. For an ordinary upgrade with no loss, use specific gain framing: the concrete limit lifted ("5,000 links / mo instead of 25") and the price. Do not invent a threat.

## 4. Making the price easy to read

From the strawberry redesign (uxpeak) and the vibe coded SaaS redesign (Kole Jain):

1. The price is the largest element in a plan card; the plan name is small. "Nobody cares" about the name, people care about the cost.
2. Write prices consistently: two decimals for goods ("$6.20", not "$6.2"), a unit ("per kg"), "$2 / mo" for subscriptions, "Custom" for Enterprise.
3. A discounted price shows the original struck through in grey next to or above it ("$7.20", "$10/mo"). The struck price must be a price really charged recently. In the EU, the reference price must be the lowest price of the previous 30 days.
4. Drop labels the format explains: no "Price:" in front of "$6.20".
5. Put the total inside the primary button and update it live: "Add to cart · $18.60". The user knows what they pay before they tap.
6. Show the price early, near the title, unless the product, the audience or the buying context says otherwise (price placement depends on all three).

## 5. Plan cards that make the upgrade delta obvious

The Resend and Supabase pattern, as rebuilt by Kole Jain:

1. 3 to 4 plans: Free, Standard, Team, Enterprise.
2. Equal, neutral cards. No coloured border per plan, no green "Current" and purple "Popular" chips competing.
3. Plan name small, centred, regular weight; old price struck through above; new price large; one quota line under it ("25 links / mo", "5,000 links / mo", "10,000 links / mo", "Custom").
4. One shared feature list in every card, in the same order (users, analytics, custom domains, security, team collaboration, bulk operations, A/B testing plus API), checked where included, dimmed where not. The user scans across and sees exactly what the next plan adds.
5. Buttons: "Current Plan" disabled on the current one, "Upgrade to Standard" etc. on the others, all muted. No bright CTA on every card.
6. Billing tab also holds the billing email (with Save) and payment method ("Visa ending in 0000, expires 04/28", "Add card").

## 6. Forbidden

| Pattern | Honest alternative |
|---|---|
| Struck through "original" prices never charged | Strike only a real recent price, or show no discount |
| "Early Adopter" or "Limited time" prices with no end date | State the end date, or call it the price |
| Preselected add ons, insurance, donations | Unticked add on with an "Add" button |
| Showing a monthly equivalent while charging yearly up front, without saying so | "$8/mo, billed $96 yearly" in the same line |
| Fees appearing only at checkout | Fees and total in the cart and in the button |
| Cancel buried or by phone only | Cancel in billing settings, same number of steps as subscribing |
| "No thanks, I hate saving money" | "No thanks" |
| A tier designed never to be bought | Delete it |

## 7. Checks

| Check | Pass when | Verify in code |
|---|---|---|
| No isolated cost | Every add on price renders next to its anchor | The add on component sits inside cart or order review, not its own route |
| Price is the biggest text in a plan card | Price font token larger than the plan name token | Compare the two style tokens |
| Price formatting | Currency formatter with fixed decimals and unit | One `formatPrice` used everywhere; no string concatenation |
| Real discounts | Struck price comes from stored price history | Trace the struck value; a literal fails |
| Shared feature list | All cards render from the same feature array | One array, per plan inclusion flags |
| Total in button | Button label is computed from quantity and unit price | Read the label expression |
| Neutral dismiss | All decline labels are neutral | Read every decline string |
| Cancel parity | Cancel flow length not longer than subscribe | Count steps in both flows |
