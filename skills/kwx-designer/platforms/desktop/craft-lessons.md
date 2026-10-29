# Craft lessons from desktop apps known for quality

What Linear, Raycast, Superhuman, Arc and Things for Mac do, turned into rules. Sources: Linear "How we redesigned the Linear UI", Raycast "A fresh look and feel" and manual, Superhuman "Built for speed" and "How to build a remarkable command palette", MacStories Things 3 review, Maggie Appleton "Command K bars". Secondary design analyses (third party guides) were read but only primary statements are used as facts here.

## Superhuman: speed is the product

- 100 ms is the ceiling for every interaction ("where interactions feel instantaneous", Paul Buchheit); Superhuman aims below 50 ms. Rule: write a latency budget per interaction and test it.
- Local database, so mail displays instantly and works offline; preload and prerender the threads you are likely to open next.
- Minimal animation so no time is spent animating; keyboard over gestures.
- Cmd+K command palette that "teaches the shortcut for next time". Forgiving fuzzy match, aliases shown in the result, default scores, context boosts, a cut off last row to invite scrolling, visually dominant and centered.
- Onboarding is a guided practice session, not a tour: people learn shortcuts by doing them (reported by NFX and others).

## Linear: dense, aligned, quiet

- Goal: "reduce visual noise, maintain visual alignment, and increase the hierarchy and density of navigation elements."
- Tested shell options from very condensed to spacious; often followed Apple standards to feel native.
- Tested each decision in every view type (list, board, split) before shipping.
- Strict alignment of labels, icons and buttons in the sidebar and tabs.
- Theme generator in LCH with three inputs (base, accent, contrast) instead of 98 variables; less accent color in the chrome; surfaces separated by elevation steps; contrast control for accessible themes.
- Inter Display for headings, Inter for text.
- Cut scope when risk is high: navigation changes were left out of the redesign.

## Raycast: fast, simple, delightful

- Design principles stated: fast, simple, delightful.
- The search bar was made bigger "to reflect its importance". Result icons enlarged for scanning.
- Actions used to hide behind a small button; they moved into a bottom action bar that shows the navigation title and toasts on the left and context actions with their shortcuts on the right. Return runs the primary action, Cmd+Return the secondary, Cmd+K opens all actions.
- Icons redrawn with consistent stroke width and corner radii.
- Optional Compact Mode for users who want only the search field and results.

## Arc: reimagined chrome (observations, not company statements)

- Tabs moved to a vertical sidebar that also holds the address field, organized by context (spaces) rather than recency.
- A Spotlight like Command Bar (Cmd+T) searches tabs, history and actions in one place.
- Lesson: chrome can be radically simplified when one universal command surface replaces many small controls. The risk, visible in Arc's later history, is that novelty adds learning cost for mainstream users.

## Things for Mac

- Type Travel: just start typing anywhere and search opens; no field to click.
- Excellent keyboard support, multiple windows; creation needs only a title.
- Lesson: the fastest search is the one with no entry step.

## Rules distilled

1. Set and measure a latency budget: < 100 ms for every interaction, < 50 ms for the hot path.
2. One universal command surface (palette) that shows shortcuts in every row.
3. Show the primary and secondary action of the current context, with shortcuts, in a persistent place.
4. Align everything in the chrome to exact lines; density only works when aligned.
5. Keep the chrome neutral; let accent mark only selection and primary action.
6. Generate themes from few inputs in a perceptual color space, with a contrast control.
7. Test every design decision in every view type.
8. Cache locally, prefetch the next likely item, update optimistically.
9. Offer a stripped compact mode for focused experts rather than more settings.
