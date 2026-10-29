# Pricing pages

A pricing page answers four questions in order: how much, what do I get, which one is for me, what is the catch. Clarity converts; tricks erode trust and in many markets break consumer law.

## Contents

1. Evidence, and how strong it is
2. Mobile app pricing is different
3. Structure of the page
4. Plan cards
5. Billing period toggle
6. Recommended plan highlight
7. Anchoring, decoys and ordering
8. Feature comparison table
9. Trust, trial and cancel terms
10. FAQ
11. Mobile layout
12. Examples observed
13. Anti-patterns
14. Review checklist

## 1. Evidence, and how strong it is

| Finding | Source | Strength |
|---|---|---|
| Pricing is a top information need; people leave sites that hide it | NN/g usability studies | Strong, repeated |
| Comparison tables suit about 5 or fewer options; keep attributes consistent; sticky column headers for long tables; about 2 columns at once on mobile | NN/g comparison tables | Strong |
| The first two plans in reading order get the most attention; highlighting a plan draws attention to it (attention, not proven purchases) | CXL eye-tracking studies on plan order and highlight | Medium, small samples |
| Stacked cards are the dominant mobile pattern (78 percent of 59 SaaS sites); tabs suit 2 to 3 plans | CXL mobile SaaS pricing study | Medium |
| Decoy effect: adding a dominated option shifts choice toward the target (Economist print vs web+print example) | Behavioural economics (Ariely) | Strong in lab, varies in the field |
| Defaulting to annual raises annual uptake; "2 months free" beats "save 17 percent" | Vendor blogs | Weak, test it yourself |

Use the strong findings as rules and the weak ones as hypotheses.

## 2. Mobile app pricing is different

For an iOS and Android app, subscriptions are normally bought inside the app through the App Store or Google Play billing. The web pricing section then informs and sends people to the store.

- The CTA on each plan is the store badges or "Download and start free trial", not a web checkout, unless you really sell on the web.
- Store prices vary by country and are set per storefront. Show your base currency and add "Prices may vary by country and are shown in the app before you subscribe." Better: localise displayed prices to the visitor's currency only if they match the store price tiers exactly.
- Keep web prices identical to the in-app prices; a cheaper in-app price makes the web page look wrong, a more expensive one looks like bait.
- Trials are store-managed: say who manages billing ("Billed through your Apple ID or Google Play account. Cancel any time in your account settings at least 24 hours before renewal.").
- Family Sharing (Apple) and family plans: say whether Pro is shareable.
- In the EU and UK, prices shown to consumers include VAT.

## 3. Structure of the page

1. Headline that frames value, not cost: "Simple pricing. Free to start." or "Upgrade when you need more."
2. Billing period toggle (if both periods exist).
3. Plan cards: 2 to 3 plans side by side (Free, Pro, optionally Lifetime or Family). Enterprise or teams as a separate line if relevant.
4. One sentence of reassurance under the cards: trial, cancel any time, money-back policy if any.
5. Feature comparison table (only if plans differ in more than about 5 ways).
6. Social proof close to pricing (rating, one testimonial about value).
7. FAQ.
8. Final CTA (badges).

On a single-page app site, steps 1 to 4 plus FAQ are usually enough.

## 4. Plan cards

Each card, top to bottom:

1. Plan name (one word: Free, Pro, Family, Lifetime).
2. One-line "who it is for" (Notion style: "For individuals to organize personal projects and life.").
3. Price: big number (32 to 48 px, tabular numerals), with the unit next to it in smaller muted text ("/month"). Yearly: show the monthly equivalent big and the real charge small ("$4.17/month, billed $49.99 yearly").
4. CTA (full card width, 44 to 48 px tall). The recommended plan gets the solid primary button; others get secondary buttons.
5. Feature list: 3 to 7 items, the differences first, starting with "Everything in Free, plus:" on higher plans. Each item a short noun phrase with a check icon that has text for screen readers.

Rules:

- Same structure and same row order on every card, so eyes can compare across.
- Cards equal height; align price lines and buttons on the same baseline across cards.
- Avoid more than 4 plans for a consumer app. Two plans (Free and Pro) is the cleanest choice for most apps.
- Never hide the price of a self-serve plan behind "Contact us".
- Charm prices (4.99) are normal for consumer apps; round prices (5) feel premium. Pick one convention for the whole page.

## 5. Billing period toggle

- A segmented control with two visible labelled options, "Monthly" and "Yearly", built as a radio group or two `aria-pressed` buttons. Not an unlabeled switch where users must guess which side is on.
- Show the saving on the Yearly option: "Yearly, save 17%" or "Yearly, 2 months free". Compute it honestly: 1 - (yearly price / (12 x monthly price)). For $4.99 and $49.99: 1 - 49.99 / 59.88 = 16.5 percent, so say "save 16%", not "save 20%".
- Default to the period you most want people to choose, usually Yearly, but make sure the monthly price is one tap away and visible on the toggle state.
- Toggling changes prices in place without layout shift (tabular numerals, fixed-width price box); animate with a short crossfade or a number roll at most 200 ms.
- Persist the choice in the URL (`?billing=yearly`).

## 6. Recommended plan highlight

- Highlight exactly one plan: the one most customers should pick (usually the middle or the paid plan).
- Use 2 cues at most: a label ("Most popular" only if true, otherwise "Recommended" or "Best value") and a stronger border or tinted background (accent step 3 background, step 8 border). Optional: scale up by 2 to 4 percent or raise elevation one level.
- Do not use the accent colour for the whole card and its button and its badge; the button alone should be the most saturated thing on the card.
- On mobile, place the recommended plan first or open on its tab.

## 7. Anchoring, decoys and ordering

- Anchoring: the first price seen sets the reference. Showing a higher plan (Lifetime $149, or a Family plan) beside Pro makes Pro look reasonable. Only show anchors that are real products people can buy.
- Order: in left-to-right layouts, people look at the first two plans most (CXL). Common consumer order is cheap to expensive (Free, Pro, Lifetime) with the recommended plan in the middle. Expensive first is worth testing for B2B.
- Decoy: a plan that is clearly worse value than its neighbour pushes choices toward the neighbour. Use with care: if visitors notice it, trust drops, and a decoy that targets features nobody wants does nothing.
- Lifetime plans anchor subscriptions well for indie apps; state what "lifetime" covers (this app, future updates).
- Never show a "was" price that was never charged; it is illegal in many places (EU Omnibus Directive requires the prior 30-day lowest price for reductions).

## 8. Feature comparison table

Follow NN/g:

- Plans as columns, features as rows, row labels on the left, plan names and prices in a header that stays sticky while scrolling.
- Group rows into 3 to 6 named sections (Linear and Notion group by area: Core, AI, Integrations, Security, Support).
- Put the most important differences first; offer "Show only differences" for long tables.
- Consistent values: "Included", a check, a number, or a dash for not included. Never playful varied wording.
- Translate technical features into outcomes, with a short tooltip or footnote for jargon.
- Use a real `<table>`; check icons have text alternatives ("Included", "Not included").
- On mobile: show 2 plans at a time with a plan switcher, or turn into per-plan lists; keep the plan name visible while scrolling.

## 9. Trust, trial and cancel terms

Near the CTA, in normal body size (not fine print):

- Trial length and what happens at the end: "7 days free, then $49.99 per year. Cancel any time before the trial ends and you will not be charged."
- How to cancel, in one sentence, with a link to the help article.
- Refund policy (store refunds are handled by Apple or Google; say so).
- Privacy reassurance if data is sensitive ("Your data stays on your device" only if true).
- A short testimonial about value ("Worth it for the delay predictions alone") beside or below the cards.

## 10. FAQ

5 to 10 questions, each answer 1 to 3 sentences, as `<details>` accordions or open text. Real examples from top pages: Flighty ("What's the difference between the free version and Pro?", "Can I trial Pro before subscribing?"), Raycast ("Why is Raycast free for personal use?", "Does Raycast have a Student Program?"), Notion ("How do I cancel my paid plan?", "How do refunds work?").

Template for a mobile app:

1. What is free and what needs Pro?
2. Is there a free trial, and when am I charged?
3. How do I cancel?
4. Can I use one subscription on iPhone, iPad and Android? (Store subscriptions usually do not cross between Apple and Google; say so plainly.)
5. Do you offer family sharing, student or regional discounts?
6. What happens to my data if I cancel or downgrade?
7. Can I get a refund?
8. Why a subscription and not a one-time price?

## 11. Mobile layout

- Stacked cards, recommended plan first or visually marked; or tabs when there are 2 to 3 plans (CXL).
- Toggle sits above the cards and stays reachable (sticky under the header is fine).
- Put the price and the CTA in the top half of each card; collapse long feature lists after 5 items with "Show all features".
- Swipeable carousels only for 4+ plans, with visible arrows and a page indicator.

## 12. Examples observed

| Product | Notes |
|---|---|
| Flighty | Pro at $4.99/month or $59.99/year; first flight free as the trial; plan list includes Annual, Weekly, Lifetime and Family with a "Most popular plan" label; CTA "Try it for free"; FAQ is 4 focused questions. |
| Raycast | Free / Pro $10 / Plus $20 / Max $50 monthly; annual $96 / $192 / $480 (20 percent off); team tiers per user; per-plan CTA "Select Plan", free plan CTA "Download"; 50 percent student discount; 10 FAQ items. |
| Linear | Free / Basic $10 / Business $16 per user per month billed yearly / Enterprise custom; higher plans list "All [previous] features +"; comparison table grouped into about 10 sections. |
| Notion | Free / Plus / Business / Enterprise; "Pay monthly" vs "Pay yearly, save up to 20%"; Business labelled "Recommended"; one-line audience per plan; currency selector; 17 FAQ items covering billing, seats, cancel and refunds. |

## 13. Anti-patterns

- Hidden price, or the real charge only in fine print after a big "per month" equivalent.
- An unlabeled billing switch; a toggle that flips the layout.
- Two highlighted plans, or a "Most popular" label that is not true.
- Pre-checked add-ons, confirmshaming ("No thanks, I like paying more"), countdown timers that reset.
- Trials that need a card without saying so on the pricing page.
- Feature lists of 25 items per card where the differences drown.
- Cancel information missing.

## 14. Review checklist

- [ ] Every price visible, with unit and billing period; yearly shows the real charge.
- [ ] Savings percentage computed, not rounded up.
- [ ] Labelled two-option toggle; state in URL; no layout shift on toggle.
- [ ] One recommended plan, 2 cues at most, label true.
- [ ] Cards share structure; prices and buttons aligned; tabular numbers.
- [ ] Trial, renewal, cancel and refund terms in body text near the CTA.
- [ ] Web prices equal in-app prices; regional price note.
- [ ] Comparison table (if any) is a real table with sticky header and grouped rows.
- [ ] FAQ answers the money questions first.
- [ ] Works at 390 px: stacked or tabbed, recommended first.
