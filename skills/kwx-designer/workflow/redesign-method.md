# Redesign method: the 16 step order

A screen that "looks fine" usually hides 10 to 15 small decisions that make it feel cheap (uxpeak, strawberry redesign). Fix them in this order, from the foundation up: content and media, grid, colour, type, then content and hierarchy, then the flow, then go beyond fixing. The order matters: a colour fix is wasted if the grid is about to change.

The 16 steps come from the uxpeak strawberry redesign, generalised. Each step has a before and after from the videos.

## Contents

1. Before you start
2. The 16 steps
3. After the 16 steps
4. Redesign log format

---

## 1. Before you start

1. Inventory: list every screen and every state of the thing being redesigned. Screenshot or describe each.
2. Number the problems you see on the current version (the video numbered 15 callouts). Keep the list; it becomes the log.
3. Find 3 to 6 reference screens from real products that solve the same job.
4. Do not change features and visuals in the same pass without listing both.
5. List what the old code does that the screenshot does not show: validation, `aria-*` attributes, focus handling, error, empty and loading branches (`grep -nE 'aria-|role=|disabled|error|empty|loading|focus'` on each file). Moved or rewritten code keeps every item.

## 2. The 16 steps

### 1. Stress test the variable content

Swap every variable input (images, names, counts, long text) for its extremes: dark, bright, busy, simple, long, empty. Check every overlay.

- Before: back and menu icons straight on a dark strawberry photo; on a pineapple on white they vanished.
- After: each icon in a white circle with enough contrast and a thin outline. "Design for systems, not screens."

### 2. Fix the media system

Choose imagery with one focal point, matching what is sold, honest for the brand, consistent across the whole set.

- Before: a full bleed pile of strawberries with no focal point.
- After: strawberries in a basket on a clean light background; the whole catalog follows the same system.
- Generalised: avatars, thumbnails, logos and charts also form a system (same shape, size, background).

### 3. Grid and alignment

Draw a reference layout of the content blocks. Set side margins (24 px in the example) and section spacing. Snap every element to the same edges.

- Before: badge past the right margin, dividers inset differently from text, a 17 px offset between the description and the icons.
- After: everything starts and ends on the same margins.
- Kole Jain, every UI concept: 4 pt scale; one default gap (32 px) between sections, half (16 px) inside a group.

### 4. Colour

Reduce saturation. Cut to a palette that supports the product and the mood. Keep strong colour for the few things that deserve emphasis.

- Before: neon green CTA and label, rainbow icons (red, neon green, yellow, purple, orange).
- After: muted red, olive, mustard, steel blue, plum; olive CTA.
- Kole Jain, vibe coded SaaS: navy AI background to a near black tinted toward the green brand; colour moved into charts.

### 5. Typography system

One family. Hierarchy by size, weight, colour and line height.

- Before: Mulish for the page, a slab serif for the badge.
- After: Lato everywhere.
- Kole Jain: one sans (DM Sans, Axiforma, SF Pro, Geist, Plus Jakarta Sans, Montserrat, Unbounded); headlines at -2% to -3% tracking and 110% to 120% line height.

### 6. Small labels and badges

Track small caps. Shorten badge copy to the minimum.

- Before: "FRUITS" cramped; "20% OFF DISCOUNT" plus a percent icon.
- After: tracked "FRUITS"; "20% off".

### 7. Title hierarchy

Stand out without shouting. Remove competing primaries.

- Before: heavy black title, loud badge and loud CTA all "primary".
- After: medium weight dark grey title. "A product title should stand out without shouting."

### 8. Body text

More line height, lower contrast, shorter and warmer copy.

- Before: 5 tight lines (line height about 1.0 to 1.1, est.), pure black.
- After: 3 lines, about 1.6, grey, rewritten friendlier. "Headlines attract attention, paragraphs support understanding."

### 9. Information placement for trust

Put proof and key facts where the question is asked.

- Before: rating below the description and a divider.
- After: 5 star row and "4.8 (89 reviews)" directly under the title.
- Kole Jain, delivery card: the price moves to the top right in blue; the time sits under the title.

### 10. Supporting sections and icons

One icon style, one colour, tighter.

- Before: four colours, filled and outline mixed, uppercase labels.
- After: olive outline icons, sentence case labels, wrapping pills.
- Kole Jain: emoji replaced with one icon library; icon size equals line height.

### 11. Separators

Soften or remove.

- Before: thick near black dividers cutting the page into blocks.
- After: thin light grey. Kole Jain, dark mode: lower border contrast, depth by lighter surfaces.

### 12. Spacing rhythm

Group related things, tighten oversized gaps.

- Before: some gaps noticeably larger than others.
- After: consistent rhythm. "Good spacing is not just about adding more empty space. It's about creating the right relationship between elements."
- Kole Jain, mobile: remove nested cards (padding on padding).

### 13. Remove redundant labels, keep labelling consistent

- Before: "Price:" before "$6.2"; "Restaurant:", "Item:", "Total Cost:" in the delivery card.
- After: no labels where the format explains; logo, pins and a dotted line replace words. If one sibling control keeps a label, all do.

### 14. Content correctness and order

The title describes the thing; variable attributes live in their selector; key facts surface early.

- Before: "Organic Strawberries - 1 kg" while the stepper says 3 kg; price at the bottom.
- After: title is the product; price "$6.20 $7.20 per kg" under the rating.
- Kole Jain, vibe coded SaaS: delete cards that do nothing; one home per metric; remove click counts from pages where they do not matter.

### 15. Primary action

Calm the CTA, put its inputs next to it, show the consequence inside it.

- Before: full width neon "ADD TO CART", stepper far away without a unit.
- After: "- 3 kg +" beside "Add to cart · $18.60", sentence case, muted brand colour.
- Kole Jain: one bright accent fill per view; header actions dark neutral; modal CTA bottom right sized to its label.

### 16. Go beyond fixes

Structure, persistence, shortcuts, cross sell. Make the task easier.

- Card over the hero; the title moves into the nav when the hero scrolls away.
- Sticky bottom action area.
- One tap presets from real data (0.5 kg Snack, 1 kg Regular, 2 kg Family, 3 kg Party), stepper kept.
- "Often bought with" with a quick add.
- Kole Jain, analytics: an "Aggregate | Individual" toggle to compare links; maps and logos where they fit.
- Tim Gabe: redesign the failure states (declined payment with cause and support button; limit screen with count and reset date).

## 3. After the 16 steps

1. States pass: loading, empty, error, offline, limit for every screen touched (`patterns/states-feedback-and-failure.md`).
2. Consistency pass: the redesigned screen next to the untouched ones. Either bring the others along or keep the shared parts identical.
3. Run `quality/quality-gate.md` and `quality/scoring-rubric.md`.
4. Show before and after side by side with the numbered list of changes, and one counted line when code was replaced ("2 dependencies and 140 lines became 1 house component and 30 lines").

## 4. Redesign log format

```
#  Step            Before                                   After                                  Why
1  Variable content icons bare on photo                     white circle + 1px outline             unreadable on bright images
3  Grid            description 17px off the icon row        all blocks on the 24px margin          misalignment is felt
15 Primary action  full width neon "ADD TO CART"            "Add to cart · $18.60" beside stepper  calm, shows the total
...
```
