# Spacing and layout

Space is the cheapest premium signal and the main tool for grouping. Start with too much, then remove.

## Contents

1. The 4/8 grid and a spacing scale
2. Spacing expresses relationships
3. Component padding
4. Section rhythm on long pages
5. Containers and line length
6. Layout grids and breakpoints
7. Alignment
8. Responsive and zoom rules
9. Review checklist

## 1. The 4/8 grid and a spacing scale

Use multiples of 8 for sizes, padding and margins, with 4 as the half step for small UI and the type baseline (spec.fm 8 pt grid; Material uses 4 and 8 dp). It removes 7 of every 8 choices and keeps platforms consistent.

Scale (tokens): `4, 8, 12, 16, 24, 32, 48, 64, 96, 128, 160` px (`--space-1` to `--space-11`).

- Neighbouring scale steps should differ by at least about 25 percent so the difference is visible. 20 vs 24 is not a hierarchy; 16 vs 24 is.
- Do not invent 18, 22, 30 for one component. If a value is missing, the scale is wrong or the component is.
- Soft grid (measure 8 pt increments between elements) is fine on the web and iOS; hard grids (everything snapped into 8 pt containers) suit Material.
- Text exception: line boxes need not be multiples of 8, but the space between text blocks should be.

## 2. Spacing expresses relationships

Gestalt proximity: items close together read as one group, and proximity beats colour and shape (NN/g).

Testable rule: **space inside a group is at most half the space between groups.**

| Relationship | Typical gap |
|---|---|
| Label to its field, icon to its label | 4 to 8 |
| Heading to its own paragraph | 8 to 16 |
| Between items in a list or form rows | 12 to 24 |
| Between cards in a grid | 16 to 32 |
| Between groups inside a section | 32 to 64 |
| Between page sections | 96 to 160 desktop, 64 to 96 mobile |

- A heading sits closer to the content below it than to the content above it (at least 2:1). Bad: equal margins above and below an h2, so it floats between sections.
- Avoid ambiguous spacing: when everything is 24 apart, nothing is grouped (Refactoring UI).
- Twelve form fields in one block feel heavier than three groups of four (NN/g).
- Responsive stacking can break groups: when side by side items stack on mobile, check that the pair still reads as a pair.

## 3. Component padding

- Size text controls with padding around the text, not with fixed heights: button `padding: 12px 20px` at 16 px text gives a 48 px target. Use `min-height` if you must fix a height.
- Horizontal padding is roughly 1.5x to 2x the vertical padding for buttons and chips.
- Card padding: 16 to 24 on mobile, 24 to 40 on desktop. Padding grows with card size; a big card with 12 px padding looks cramped.
- Touch targets: 44 x 44 pt (Apple), 48 x 48 dp (Material), 24 x 24 CSS px minimum (WCAG 2.5.8). Small visual icons get an invisible hit area.

## 4. Section rhythm on long pages

- Use one vertical section padding token for the whole landing page (for example 128 desktop / 80 mobile) and change it only to mark a deliberate change of pace (a dense logo strip gets less, the final CTA more).
- Alternate density: a dense feature grid followed by a calm single statement keeps scrolling pleasant.
- The first screen must show a hint that content continues below (a cut-off card or screenshot): NN/g warns that full-screen heroes create a false floor.

## 5. Containers and line length

| Container | Max width |
|---|---|
| Reading text | 60 to 70 ch (about 640 to 720 px at 18 px) |
| Hero headline block | about 20 to 35 characters per line at display size, usually 720 to 1000 px |
| Content grid | 1120 to 1280 px |
| Full-bleed media | viewport, with inner content still capped |

You do not have to fill the screen. A narrow centred column on a wide display looks deliberate, a stretched one looks broken (Refactoring UI).

## 6. Layout grids and breakpoints

| Viewport | Columns | Gutter | Outer margin |
|---|---|---|---|
| Phone (under 600 px) | 4 | 16 | 16 to 24 |
| Tablet (600 to 1023) | 8 | 24 | 32 |
| Desktop (1024 and up) | 12 | 24 to 32 | 48 to 80, or centred max-width container |

- 12 columns divide into 2, 3, 4 and 6, which covers feature grids of 2, 3 or 4 cards.
- Choose breakpoints where the content breaks, not at device widths. Express them in `rem`.
- Grids are a tool, not a cage. A sidebar or a fixed-width card can stay fixed while the rest flows (Refactoring UI: grids are overrated).
- Prefer CSS Grid and Flexbox with `gap` over margins on children; let CSS do the sizing, never JavaScript measurement (Vercel).
- Respect safe-area insets on phones: `padding-inline: max(16px, env(safe-area-inset-left));` and `viewport-fit=cover` only if you handle them.

## 7. Alignment

- Every element aligns to something on purpose: a column edge, a text baseline, or a centre axis (Vercel). Count the distinct left edges in a section: 1 to 3 is calm, 6 is chaos.
- Align text by baseline, not by box centre, when mixing sizes on one line (Refactoring UI).
- Icons next to text: centre the icon on the x-height or cap height, not the line box. Size icons to about the cap height plus 20 to 40 percent (16 px text pairs with 18 to 20 px icons).
- Optical alignment beats mathematical: a play triangle shifts right 1 to 2 px, round shapes overshoot squares by about 2 to 3 percent, big headlines may need a 1 to 2 px pull to the left.
- Left-aligned layouts are easier to scan than centred ones. Centre only symmetrical moments (hero, final CTA, a single quote).

## 8. Responsive and zoom rules

- Reflow at 320 CSS px without horizontal scrolling (WCAG 1.4.10); this is the same as a 1280 px screen at 400 percent zoom.
- Text resizes to 200 percent without loss (WCAG 1.4.4).
- Horizontal padding in px, vertical spacing in rem (Josh Comeau): text growth should not starve line length.
- Test at 360, 390, 768, 1024, 1280, 1440 and 1920 px, and at 50 percent zoom for ultra-wide (Vercel).
- Design for short, average and very long content (names, translations: German runs about 30 percent longer than English).

## 9. Review checklist

- [ ] Every spacing value is a scale token.
- [ ] Gaps inside groups are half or less of gaps between groups.
- [ ] Headings sit closer to what follows than to what precedes.
- [ ] One section padding token on the landing page.
- [ ] Reading text capped at about 65 ch; hero fits on one screen with a visible hint of more.
- [ ] No horizontal scroll at 320 px; nothing clips at 200 percent text.
- [ ] Hit targets 44 px or more on touch.
