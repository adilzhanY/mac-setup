# Trust and fluency

"The brain has no premium detector, but it does keep score quietly of every piece of evidence that a product is good" (Tim Gabe, premium apps). Trust is built from that evidence: things that are easy to take in, things that stay the same, information placed where the question is asked, and failures handled well.

## Contents

1. Processing fluency
2. Consistency is trust
3. Felt, not noticed: alignment and polish
4. Put proof where the question is
5. Honest imagery and copy
6. Remove uncertainty before commitment
7. Failure handling as trust
8. Checks

---

## 1. Processing fluency

- What is easy to perceive and process is judged as more beautiful and more positively (Reber, Schwarz, Winkielman 2004).
- Every "did the tap work? can I go back?" is processing effort that lowers the judgement (Tim Gabe).
- Looks get a product picked; evidence of a good product gets it called premium (packaging studies: Reimann et al. 2010; Pombo and Velasco 2021, as cited by Tim Gabe).

Rules:

1. Reduce what the user has to interpret on every screen: one primary action, labels only where the format does not explain itself, one font, colour only with a meaning.
2. Replace text with structure when the meaning is obvious: two location pins joined by a dotted line say "from" and "to" without the words (Kole Jain, every UI concept).
3. Use images and logos to speed scanning: a brand logo tile, avatars instead of names ("your eye can associate who did what way faster than reading a name", Kole Jain, dashboard flaws).
4. Keep body text easy: line height about 1.5 to 1.6, grey rather than pure black, short paragraphs (the strawberry description went from 5 lines to 3).

## 2. Consistency is trust

The York study (Petrie et al. 2009, cited by Tim Gabe): mid task the navigation bar moved from left to right, nothing else changed. Time on that page went from 1.9 s to 6.8 s, and on the following pages from 2.2 s to 6.2 s. 85.7% noticed the position change, and they still rated its effect low (2.38 of 5). Font size changes were noticed 42.9% of the time, font type and order 21.4%.

Lessons:

1. Inconsistency costs far more than users say and more than analytics show. Do not wait for complaints.
2. Lock shared chrome: navigation position, header height, font family and size, button styles, wording for the same action.
3. "Your user sees screen 80 sitting right next to screen one." Review the product as a sequence, not one screen at a time. AI makes this worse: an agent can generate "80 screens that don't quite agree" in an afternoon.
4. One situation, one pattern. Undertone had two different "out of sessions" screens (one with "Upgrade plan" + "Close", one with only "Close"). Merge into one component and vary only the action.
5. Label consistently: if one control in a group has a label, its siblings do too, otherwise none do (the strawberry "Price:" label removed because the quantity stepper had none).

## 3. Felt, not noticed: alignment and polish

- "When alignment is off, users may not consciously notice it, but they feel it": less calm, less structured, less trustworthy (uxpeak, strawberry redesign). The video measured a 17 px offset between the description and the icon row.
- Rule: one side margin (24 px in the example) and one set of edges. Every text block, icon row, divider and badge starts and ends on them.
- Thin light dividers or none. Heavy black dividers cut the page into harsh blocks. "Small details are often what make an interface feel premium."
- Shadows: "If the shadow is the first thing you notice on a design, you're not using it right" (Kole Jain).

## 4. Put proof where the question is

1. Ratings directly under the product title, as a star row plus count: "4.8 (89 reviews)". The user's questions in order: what is it, how is it rated, can I trust it. Reviews are one of the strongest e-commerce trust signals (uxpeak).
2. Show who did what with avatars and names in activity feeds and tables.
3. Show the source of a number: "Edited 23 min ago", "Today, 2:13pm | 4 hours ago".
4. Security and privacy reassurance next to the sensitive step (the neobank KYC intro: steps, "takes about 3 minutes", privacy note, one CTA).
5. Concede limits in public. A note that an earlier headline number was inflated, with the corrected figure and links to measurements other people ran, earns more trust than a flawless claim (ponytail's "Read this number honestly" section).
6. A landing page "establishes trust, even subconsciously" (Kole Jain, vibe coded SaaS). Real product graphics beat icon tiles; a vibe coded landing page is where most customers are lost.

## 5. Honest imagery and copy

1. Imagery must match what is sold. The strawberry page sells by weight, so one single berry is a mismatch; hands holding the product make the hands the focal point; a saturated pink and blue backdrop is artificial for fresh organic food. The chosen image: natural strawberries in a basket on a clean light background, one system for the whole catalog.
2. The title describes the product only. "Organic Strawberries - 1 kg" became misleading once the stepper said 3 kg: "a small mismatch in the user's mind, which costs trust".
3. Write facts, not slogans, in system messages: "You've used both sessions this month", not "Keep every session within reach!".
4. Never fake a count, a review, a stock level or a deadline (see the ETHICS section in `psychology.md`).

## 6. Remove uncertainty before commitment

1. Show the consequence inside the action: "Add to cart · $18.60", "Search 12 Available Tables".
2. Put inputs next to the action they feed: the quantity stepper directly left of Add to cart, the unit inside it ("- 3 kg +").
3. Keep the action reachable when the user is ready: a sticky bottom action area on long pages. People decide at different scroll depths.
4. Keep context when scrolling: once the hero leaves the screen, the product title moves into the top bar and stays.

## 7. Failure handling as trust

- **Service recovery paradox**: a big 2007 review found that when a failure is handled really well, people can end up as happy as if nothing had gone wrong, or happier. "This thing went south, but they caught me. That, my friends, is exactly what a premium experience feels like." (Tim Gabe)
- About a third of people leave after one bad experience (PwC 2018). People do not walk away because of a home screen.
- The crypto card client: a failed transaction had "zero information on what you should do, you're just left alone". The fix: an alert telling the user to check their balance with a contact support button right there. Together with other changes: new accounts +60%, money loaded onto cards +79%.
- Rules: say the likely cause, what to do now, and give a direct path to a human on the same screen. Tailor the message to the reason (low balance gets its own message). Full pattern in the states patterns file.

## 8. Checks

| Check | Pass when | Verify in code |
|---|---|---|
| One margin system | All blocks share the same horizontal padding token | `grep` for horizontal padding/margin values on the screen; one value for content edges |
| Shared chrome identical | Nav, header and tab bar come from one component | Every screen imports the same nav component; no local copies |
| One pattern per situation | Same state renders the same component | Search for duplicate limit/error/empty screens |
| Proof placement | Rating is the next sibling after the title | Read the component order |
| Consequence in action | Primary button label includes the computed outcome | Read the label expression |
| Factual system copy | No exclamation slogans in limit, error or empty states | `grep -n "!\""` in state copy |
| No fake proof | Counts, ratings and stock come from data | Trace each to an API field |
