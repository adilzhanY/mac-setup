# Critique method

How to review a design, your own or someone else's, so the review finds real problems instead of matters of taste. Each technique has a version for when you can see the UI and a version for when you only have the code.

Review like the person who will be called when it breaks; audit like the one who just inherited it. A review lists findings and changes no code unless the user asked for fixes. The review and report rules in sections 12 to 14 come from the ponytail plugin's review and audit skills, translated to UI.

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
12. Lean pass
13. Auditing a whole app
14. Writing the critique
15. Checks

---

## 1. Order of the review

Review from the foundation up, the same order the redesign method uses: content and media, grid and alignment, colour, type, hierarchy, information placement, states, flow. A colour comment is wasted if the layout is about to change.

**What to review.** When the user names nothing, review the uncommitted changes, else the last commit. A named file, branch or PR replaces that default.

**Read past the diff.** Open every screen that imports a component, prop or token the change touched, not only the changed files. A renamed prop or a changed token breaks screens the diff never shows. Ponytail's review measurement: problems outside the diff were found 100% of the time with this rule against 78% without it.

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
3. Shortest content: one item, zero items, a 1 character name, the last item removed.
4. Edge values: zero and negative amounts, rounding (3 items at a third each), another time zone, a date across midnight or a daylight saving change.
5. Volume: 3 rows or 30,000, one user or a team of 200. Find the expected size in the project (README, seed data, the product's pitch) and write the size you assumed in the review.
6. The full catalog: would this image or card style still look right next to 20 others in a grid?
7. Code only: find every text binding and image binding; for each, state the minimum and maximum realistic value and compute whether it fits (font px times characters times about 0.55 against the box width).

## 5. Screen 80 next to screen 1

"Your user sees screen 80 sitting right next to screen one" (Tim Gabe). Users who saw the nav move from left to right were 3x slower on that page (1.9 s to 6.8 s) and still rated the effect low (York study, 2009).

1. Lay every screen side by side (or list them). Check nav position, header height, title size, spacing, button styles, wording, icon set, empty and error patterns.
2. Code only: list the components and tokens each route uses. Any route with local styles where a shared component exists, or a different value for the same role, fails.
3. Write down "every spot where it stops feeling like the same product". Fix each.
4. A fix applied in one screen while the shared component or token stays broken is a finding of its own.

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

## 12. Lean pass

Go over the components the change adds or touches:

- **Delete:** dead variants, props no screen passes, components nothing imports, styles no element uses.
- **Reuse:** a local card, button or empty state where the house one exists. Name its path in the finding.
- **Native:** a custom widget where a native element does the job (`<dialog>`, `<details>`, `<input type="date">`).
- **Speculative:** a wrapper that only passes props through, a variant system with one variant, a context for one value.
- **Merge:** near copies that must change together (two card components 90% alike).
- Before calling anything unused, grep the whole tree, including tests, fixtures, config and names built from strings.

## 13. Auditing a whole app

1. Map first: README, build and deploy config, the dependency list, entry points, routes, the shared component folder, tests.
2. Read the risky paths end to end: checkout and payment, sign in and account, destructive actions, anything that writes user data, settings that persist.
3. Go deep where a mistake costs most, not file by file, and say which parts you did not read.
4. Cap the report at 20 findings and say how many smaller ones were left out.

## 14. Writing the critique

1. **Priority order:** works in every state, then honest, then accessible, then consistent, then polished, then lean. A slowdown a user feels is a problem; a small speed win is a suggestion.
2. **Open with what it is:** two or three sentences starting `What this change does:` (or `What this app does:` plus the size you assumed).
3. **Group by severity** (blocker, major, minor), blockers first: broken states, dishonest patterns, unreadable text, missing primary action. Skip empty groups.
4. **Number findings across all groups,** so the user can answer "fix 2 and 5".
5. **Each finding:** a bold title with `file:line` that states the user impact in plain words ("Long names push the Save button off the card", not the component name), then four short parts: **What this is** (context for someone who never saw the code), **Problem**, **Fix**, **If we skip it** (the consequence).
6. **Every finding needs a concrete case:** "this input or situation leads to this wrong result". No case, no finding. Before reporting, re-read the lines: the importer exists, the value can really be empty, the code really is unused.
7. **Be specific:** "The badge and the title both use 700 weight and the CTA is neon, so three things compete; drop the title to 500 and mute the CTA", not "the hierarchy is off". No "consider", no vague worries.
8. **Smallest fix that works.** Prefer fixes that delete code. Never propose a new layer, framework or config to fix one screen.
9. **A marked deferral is a decision.** A `kwx-defer:` comment (`workflow/lean-build.md`) that names its limit is not a finding, unless the expected load already crosses it.
10. **Separate fact from taste.** Taste comments are labelled as taste and come last.
11. **Plain English:** short sentences, everyday words, a technical term explained the first time it appears.
12. **End with** what works (so it is kept next round), then three lines: `Verdict:` ship, or fix N first; `Lean:` what can be deleted; `Not checked:` what you did not read or run.
13. **Nothing found:** say "Looks good. Ship." plus one line on what was checked.
14. A report the user asked for is given in full; brevity rules for replies do not cut it.

Example:

```
2. [major] ProductPage.tsx:41, the back and menu icons disappear on bright photos
What this is: the two icons sit straight on the hero photo.
Problem: on a white background product image they are invisible.
Fix: a 36 px white circle with a 1 px outline behind each icon.
If we skip it: on light products the user cannot find the way back.
```

## 15. Checks

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
| Past the diff | Every importer of a changed component or token was opened |
| Volume | The assumed data size is written in the review |
| Findings | Each has a concrete case, a fix and a consequence; numbered; verdict line present |
