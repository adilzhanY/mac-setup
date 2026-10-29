# Premium feel: what it is and how to get there

The master file for the `premium/` folder. Read this first, then open the topic file you need.

## Contents

1. What "premium" actually means
2. The seven sources of premium feel
3. The premium pass: a method in 12 steps
4. The 40 point premium audit
5. What makes an interface look cheap
6. Topic files in this folder
7. Where these rules come from

---

## 1. What "premium" actually means

Premium is not a style. It is not dark mode, glass, gradients, serif headings or big empty hero sections. Those are costumes. Premium is the feeling a person gets when **every decision they touch was made on purpose by someone who cared about them**.

The sources agree on this with unusual consistency:

- Apple, *The Qualities of Great Design* (WWDC18): quality is "considered and intentional", "nothing is random", and "your intentions are felt". A rushed settings screen lowers the trust in the whole app.
- Dieter Rams, principle 8: "thorough down to the last detail. Nothing must be arbitrary or left to chance."
- Massimo Vignelli, *The Vignelli Canon*: "There are no hierarchies when it comes to quality. Quality is there or is not there." And: "the end result is the sum of all the details."
- Paul Graham, quoted by Emil Kowalski: unseen details combine "like a thousand barely audible voices all singing in tune".
- Paul Stamatiou, *Craft*: a single alignment fix does not matter, a dozen together are noticeable. Quality compounds.
- Frank Chimero, *The Shape of Design*: "Needs more love." The work has enough love "when enthusiasm transfers from the maker to the audience".

So the working definition for this skill:

> **Premium = intention made visible in every detail, plus restraint, plus speed.**
> The user cannot point at why it feels good. They can only feel that nothing is wrong, nothing is slow, and nothing is there by accident.

Two consequences follow, and both are testable:

1. **Premium is mostly the absence of defects.** Misaligned icons, a jittery scroll, a 400ms dropdown, a grey label on a coloured card, a straight quote, a corner radius that does not nest. Each is small. Together they read as "cheap". Apple WWDC26 *Principles of great design* lists exactly these: laggy buttons, jittery scrolling, misaligned icons, layouts that break on rotation.
2. **Premium is defended with reasons.** Every value (spacing, radius, duration, weight, colour) must have an answer to "why this number?". If the answer is "it looked fine", it is not done.

## 2. The seven sources of premium feel

Each of these has its own file. In rough order of how much they matter:

| # | Source | One line rule | File |
|---|---|---|---|
| 1 | Restraint | Fewer typefaces, sizes, colours, effects, words. Spend novelty on 10% of the product. | `restraint-and-reduction.md` |
| 2 | Typography | Body text first. Size, leading, measure, font. Tracking that changes with size. | `typography-craft.md` |
| 3 | Details | Optical alignment, concentric radii, tabular numbers, real punctuation, every state designed. | `details-and-polish.md` |
| 4 | Motion and response | Instant feedback on press, under 300ms, ease-out or springs, always interruptible, never on keyboard actions. | `motion-and-feel.md` |
| 5 | Materials, depth, light | One light source, layered tinted shadows, borders that contrast with both sides, glass only for the floating layer. | `materials-depth-light.md` |
| 6 | Words | Specific labels, no filler, the why first, one term per concept. | `copywriting-and-tone.md` |
| 7 | Speed and robustness | Fast is a feature. Optimistic updates, no layout shift, works with long and empty content. | `details-and-polish.md` sections 9 and 10 |

## 3. The premium pass: a method in 12 steps

Run this after the feature works and before you call the UI finished. Do the steps in order: later steps depend on earlier ones.

1. **State the purpose of the screen in one sentence.** (Apple PACE, WWDC22.) If you cannot, the screen is not ready for polish. Cut anything that does not serve that sentence.
2. **Pick the personality in three words** (for example: calm, precise, quiet; or warm, playful, quick). Every later choice (radius, easing, bounce, copy tone) must fit those words. Refactoring UI: small radii read neutral, large radii read playful. Emil: a playful component can bounce, a dashboard must be crisp.
3. **Limit the palette of decisions before designing.** Max 2 typefaces (Hobday, Vignelli uses one per job). A type scale of 5 to 7 sizes used per product, 1 to 2 per view (Vignelli). A spacing scale on a 4 or 8 base. 8 to 10 greys tinted toward the brand hue. One accent colour, used for the one primary action.
4. **Set the body text.** 16px minimum on screen (Butterick: 15 to 25px; Hobday: 16px+), line height 1.4 to 1.5 for body (Butterick 120 to 145%), measure 45 to 75 characters, target 66 (Bringhurst). Everything else is designed relative to this.
5. **Build hierarchy by de-emphasis, not by shouting.** Make secondary things lighter, smaller and greyer before making the primary thing bigger. (Refactoring UI, "De-emphasize to emphasize".) Use weight and colour before size. Headings only a small step bigger than body (Butterick).
6. **Align everything to something.** Every element shares an edge or a centre line with another (Hobday rule 8, Vercel). Then fix optics: nudge icons and play triangles by 1 to 2px until they *look* centred.
7. **Nest every radius.** Inner radius = outer radius minus the padding between them. If the result is 0 or negative, use a small fixed radius (2 to 4px) or a square corner. Capsule = height / 2.
8. **Design every state.** Rest, hover, pressed, focus-visible, disabled, loading, empty, error, overflow (very long text), sparse (one item), dense (500 items). A component with only a rest state is a mockup.
9. **Make it respond instantly.** Visual feedback on pointer down (scale 0.97 or a highlight within one frame). No animation on anything triggered by the keyboard or used 100+ times a day. Everything else under 300ms, ease-out or a critically damped spring.
10. **Light it consistently.** One light source (top, slightly left). Shadows layered (2 or more layers), tinted toward the background hue, blur about 2x the offset. In dark themes, closer surfaces get lighter instead of getting shadows.
11. **Rewrite every string.** Buttons say the action ("Save API Key", not "OK"). Errors say what happened and how to fix it. Empty states say what will appear here and how to make it appear. Remove "simply", "easily", "oops", "please". Curly quotes, real ellipsis, numbers as digits.
12. **Review cold.** Come back the next day (Emil). Play motion at 2 to 5x slower. Check at 50% zoom (Vercel: simulates ultra-wide), at 200% zoom, at the narrowest width, with the longest real string, in both themes, with reduced motion on.

## 4. The 40 point premium audit

Use it as a checklist when reviewing finished UI. Each line is pass or fail. A premium screen passes all of them, or has a written reason for each exception.

**Restraint**
1. No more than 2 typefaces on the product.
2. No more than 3 font sizes visible in one view (excluding numbers in a chart).
3. One primary (filled, accent coloured) action per view.
4. Accent colour covers under about 10% of the pixels.
5. No decorative element (gradient, glow, blob, pattern) without a job.
6. Every animation answers "why does this move?" with a purpose, not "it looks cool".

**Typography**
7. Body text 16px or more on screen (inputs 16px or more on mobile to stop iOS zoom).
8. Body line height 1.4 to 1.6; headings 1.0 to 1.25.
9. Line length 45 to 75 characters.
10. Large text (about 24px+) has negative tracking; all caps and small labels have positive tracking (+0.05 to +0.12em).
11. Numbers that are compared or that change (tables, timers, prices, counters) use tabular figures.
12. No font weight under 400 for text; no weight change on hover or selection (it shifts layout).
13. Curly quotes and apostrophes, real ellipsis character, no double hyphen dashes.

**Layout and details**
14. Every spacing value is on the scale. No 13px, no 7px.
15. Outer padding of a container is at least its inner gap (Hobday).
16. Related items closer to each other than to unrelated items (label to its input closer than to the previous input).
17. Every element aligns with at least one other element.
18. Icons optically centred; icon next to text balanced in weight (icon contrast lowered).
19. Nested corner radii are concentric.
20. Hit area at least 24px on pointer, 44px on touch, even when the visual is smaller.
21. No two hard divides side by side (border + background change + divider line). Use one.

**States and robustness**
22. Hover, pressed, focus-visible and disabled are all designed; hover/active/focus have more contrast than rest.
23. Loading state keeps the label and layout size (spinner inside the button, skeleton matching final layout).
24. Spinners wait 150 to 300ms before showing and stay at least 300 to 500ms once shown (no flicker).
25. Empty state explains what goes here and offers the first action.
26. Error state says what happened and how to fix it, next to the cause.
27. Layout survives the longest real string, a single item, and hundreds of items.
28. No layout shift when data, fonts or images load.

**Motion and response**
29. Press feedback within one frame of pointer down.
30. No animation on keyboard initiated actions or on things used 100+ times a day.
31. UI transitions under 300ms (tooltips 125 to 200ms, dropdowns 150 to 250ms).
32. Nothing scales in from 0; enter from scale 0.9 to 0.97 plus opacity.
33. Popovers grow from their trigger (transform-origin), modals from the centre.
34. Every animation can be interrupted and reversed mid-flight.
35. Reduced motion replaces movement with short fades.

**Depth and colour**
36. One light direction for every shadow.
37. Shadows are layered and tinted, never a single grey `0 0 10px rgba(0,0,0,.5)`.
38. No pure #000 or #fff for large surfaces; neutrals tinted under 5% saturation toward the brand.
39. Text on any coloured or image background passes contrast (WCAG 2: 4.5:1 small text, 3:1 large text and icons). Vercel prefers APCA for new work; if you use it, check against its published thresholds.

**Words**
40. Every button names its action; no "OK / Cancel" or "Yes / No" pair where a verb would do.

## 5. What makes an interface look cheap

The fastest route to premium is removing these. Each is common in generated UI.

| Cheap tell | Why it reads cheap | Fix |
|---|---|---|
| Everything the same weight and size, or everything bold | No hierarchy, the eye has nowhere to land | De-emphasize secondary items with colour and weight first |
| Grey text on a coloured background | Looks washed out and dirty | Use a tint of the background hue, or white at reduced opacity |
| Pure black text on pure white, pure black dark mode | Harsh, vibrates, looks unfinished | Near-black (#111 to #1a1a1a range) and off-white, tinted |
| One heavy blurry shadow on every card | Looks like a 2012 template | Layered, tinted, small offset shadows, or no shadow plus a 1px border |
| Borders everywhere | Busy, boxed in | Separate with spacing or a background shift; keep one divide |
| Radii that do not nest (same radius inside and out) | Inner shape looks pinched or bloated | Inner = outer minus padding |
| Centred long paragraphs | Hard to read, looks like a flyer | Left align anything over 2 to 3 lines |
| 300 to 500ms fades on every hover and menu | Feels slow and heavy | Under 200ms, or no animation for frequent actions |
| `ease-in` or linear UI motion | Starts slow, feels laggy | ease-out custom curve or spring |
| Spinner that flashes for 80ms | Flicker reads as broken | Delay 150 to 300ms, minimum 300 to 500ms |
| "Oops! Something went wrong." | Says nothing, sounds flippant | Say what failed and the next step |
| Emoji used as icons | Inconsistent rendering, toy look | A real icon set at one stroke weight |
| Five accent colours | No signal survives | One accent; status colours only for status |
| Gradient text, glow, glass on everything | Novelty on 100% of the surface | Novelty on 10%, the rest familiar (Rauno) |
| Placeholder copy ("Lorem", "Item 1") left in states | Shows nobody looked | Real content, real lengths |
| Numbers jumping width as they tick | Jitter | `font-variant-numeric: tabular-nums` |

## 6. Topic files in this folder

- `restraint-and-reduction.md`: Rams, Vignelli, Teenage Engineering, the 90/10 novelty rule, simplicity versus minimalism, how to cut.
- `typography-craft.md`: body text, measure, leading, scale, tracking by size, weights, numerals, punctuation, headings.
- `details-and-polish.md`: optical alignment, concentric radii, hairlines, hit areas, states, focus, forms, loading, empty and error states, robustness.
- `motion-and-feel.md`: when to animate, durations, easing curves, springs and their numbers, interruptibility, gestures, momentum, reduced motion.
- `materials-depth-light.md`: light source, shadow recipes with values, borders, elevation, dark mode depth, glass and blur rules.
- `copywriting-and-tone.md`: voice and tone, labels, errors, empty states, word lists, formatting numbers and dates.

## 7. Where these rules come from

Every rule in this folder traces to a source read during research (October 2026). Full notes per source are in `../sources/books/`, and the canonical reading list with who recommends what is `../sources/books/README.md`. Main sources:

- Matthew Butterick, *Practical Typography* (free online)
- Robert Bringhurst, *The Elements of Typographic Style*, through Richard Rutter's *Elements of Typographic Style Applied to the Web*
- Massimo Vignelli, *The Vignelli Canon* (free PDF released by the author)
- Frank Chimero, *The Shape of Design* (free online)
- Jeremy Keith, *Resilient Web Design* (free online)
- Adam Wathan and Steve Schoger, *Refactoring UI* (paid; table of contents, free preview chapter and detailed reviews read)
- Dieter Rams, ten principles (Vitsoe)
- Don Norman, *The Design of Everyday Things* (paid; Norman's own essays and summaries read)
- Apple WWDC talks: Essential Design Principles (2017), Qualities of Great Design, Designing Fluid Interfaces, The Life of a Button (2018), The Details of UI Typography (2020), Writing for Interfaces (2022), Animate with Springs (2023), Add Personality through UX Writing (2024), Meet Liquid Glass, Get to Know the New Design System, Make a Big Impact with Small Writing Changes (2025), Principles of Great Design (2026)
- Rauno Freiberg, *Invisible Details of Interaction Design*, *Novelty*, *Contrasting Aesthetics*, *Designing Depth*, and his interface guidelines
- Emil Kowalski, articles on emilkowal.ski and his public design engineering skill files (github.com/emilkowalski/skills)
- Vercel, *Web Interface Guidelines*
- Paul Stamatiou, *Craft*
- Linear, *How we redesigned the Linear UI*; Stripe, *Designing accessible color systems*
- Anthony Hobday, *Visual design rules you can safely follow every time*
- Josh Comeau, *Designing Beautiful Shadows*; Tobias Ahlin, *Smoother and sharper shadows with layered box-shadows*
