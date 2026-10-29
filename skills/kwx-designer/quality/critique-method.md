# Critique method

How to review a design, your own or someone else's, so the review finds real problems instead of matters of taste. Each technique has a version for when you can see the UI and a version for when you only have the code.

## Contents

1. Order of the review
2. Squint and blur test
3. Count the primaries
4. Stress the content
5. Screen 80 next to screen 1
6. Break it on purpose
7. Compare against a real reference app at the same zoom
8. Walk the flow: the three questions
9. Rank the actions (spectrum of explicitness)
10. Design theater audit
11. Use it for an hour
12. Writing the critique
13. Checks

---

## 1. Order of the review

Review from the foundation up, the same order the redesign method uses: content and media, grid and alignment, colour, type, hierarchy, information placement, states, flow. A colour comment is wasted if the layout is about to change.

## 2. Squint and blur test

- **With a screenshot**: blur it (or squint). What do you see first, second, third? It should match the intended order. In a dashboard, only meaningful colour signals should survive (Kole Jain's blurred employee table kept only the status and department chips).
- **Code only**: list every element on the screen with its font size, weight, colour and area. Rank by visual weight (size times weight times contrast against the background). The top three must be the three most important things, in order. Any saturated area that is not a signal is a fail.

## 3. Count the primaries

- How many elements claim "primary"? The strawberry page had three (heavy title, loud badge, neon CTA) and the callout "Competing visual weight". There must be exactly one primary action and one dominant heading per view.
- Code only: count elements using the heaviest weight, the largest size, or the accent fill.

## 4. Stress the content

"Design for systems, not screens" (uxpeak, strawberry redesign).

1. Swap the variable content: a dark image, a bright image, a busy image, no image. Every overlay (icons, text) still readable?
2. Longest realistic text in every field (a 40 character name, a German translation, a 12 digit amount). Does it wrap or truncate as designed?
3. Shortest content: one item, zero items, a 1 character name.
4. The full catalog: would this image or card style still look right next to 20 others in a grid?
5. Code only: find every text binding and image binding; for each, state the minimum and maximum realistic value and compute whether it fits (font px times characters times about 0.55 against the box width).

## 5. Screen 80 next to screen 1

"Your user sees screen 80 sitting right next to screen one" (Tim Gabe). Users who saw the nav move from left to right were 3x slower on that page (1.9 s to 6.8 s) and still rated the effect low (York study, 2009).

1. Lay every screen side by side (or list them). Check nav position, header height, title size, spacing, button styles, wording, icon set, empty and error patterns.
2. Code only: list the components and tokens each route uses. Any route with local styles where a shared component exists, or a different value for the same role, fails.
3. Write down "every spot where it stops feeling like the same product". Fix each.

## 6. Break it on purpose

"Open your product and break it on purpose" (Tim Gabe):

- turn off the network mid flow;
- fail a payment (or any server call);
- empty every list;
- expire the session;
- deny a permission (camera, location, notifications);
- double tap every submit;
- use the slowest realistic connection.

Each case must render a state designed as carefully as the success screen. Code only: trace each case through the handlers and find the branch that renders it. A missing branch is a fail.

## 7. Compare against a real reference app at the same zoom

1. Pick a real, well regarded app that solves the same job (from a pattern library such as Mobbin, or a known product: Spotify, Apple apps, Linear, Notion, Resend, Stripe).
2. Put your screen next to it **at the same zoom and device size**. Kole Jain's mobile calendar looked fine alone and obviously too small and dense next to Spotify.
3. Compare: body size, line height, row height, margins, touch targets, number of things on screen, number of colours.
4. Code only: write down the reference's measured values (iOS body 17 px, tab cell 72 x 48 px, 44 px minimum target) and compare your tokens against them.
5. Study the reference's flow, not only its look: what comes before and after this screen.

## 8. Walk the flow: the three questions

For each action in the core flow ask (Tim Gabe):

1. Does the user know what just happened?
2. Can they take it back?
3. Do they know what to do next?

Write the answer per action. Any "no" is a finding.

## 9. Rank the actions (spectrum of explicitness)

List every action on the screen with its frequency and importance (Kole Jain, dashboard flaws). Place each on the spectrum: always visible, visible icon, icon on hover with tooltip, hidden in a menu. Findings: a rare action that is always visible (a red "remove" button on every row), or a frequent one that is buried.

## 10. Design theater audit

AI tools state reasoning that never reaches the interface (about a quarter of it in the "Design Theater" study). For any design with a written rationale (yours included): list every claim ("errors are recoverable", "users can undo", "status is always visible") and find the code that implements each. A claim with no code is a finding.

## 11. Use it for an hour

When the product runs: use it for an hour like a real user, with real data, and write down every moment of hesitation ("did that work?", "where is...?", "why is this different?"). When it does not run: walk three realistic user stories end to end through the code, screen by screen.

## 12. Writing the critique

1. One finding per line: **where**, **what is wrong**, **why it matters** (the principle), **the fix**, **severity** (blocker, major, minor).
2. Lead with blockers: broken states, dishonest patterns, unreadable text, missing primary action.
3. Be specific: "The badge and the title both use 700 weight and the CTA is neon, so three things compete; drop the title to 500 and mute the CTA", not "the hierarchy is off".
4. Separate fact from taste. Taste comments are labelled as taste and come last.
5. End with what works, so it is kept in the next round.

Example:

```
[major] ProductPage hero: back and menu icons sit bare on the photo. Invisible on a
bright product image (tested with a white background image). Fix: 36 px white circle
with a 1 px outline behind each icon.
```

## 13. Checks

| Check | Pass when |
|---|---|
| Blur order | The top 3 by visual weight are the top 3 by importance |
| Primaries | Exactly one primary action per view |
| Content stress | Dark, bright, busy, long, short and empty content all render as designed |
| Consistency | No route differs from the shared components and tokens |
| Breakage | Every break case has a designed state |
| Reference | Sizes and density match or exceed the reference at the same zoom |
| Three questions | Answered yes for every action in the core flow |
| Rationale | Every stated design claim is implemented |
