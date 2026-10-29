# Typography craft

Type is most of any interface. Butterick: body text is most of a document, so its appearance mostly determines the quality of the whole. Bringhurst: "Typography exists to honor content." This file gives the numbers.

## Contents

1. The order of work
2. Body text: the four decisions
3. Measure (line length)
4. Leading (line height)
5. Type scale and hierarchy
6. Tracking (letter spacing) by size
7. Weights
8. Headings
9. Numerals and data
10. Punctuation and characters
11. Alignment and rag
12. Choosing and pairing fonts
13. Optical sizes and platform type
14. Text over colour, images and glass
15. CSS recipe
16. Checklist
17. Sources

---

## 1. The order of work

1. Body text first (size, leading, measure, font). Butterick, maxim 1: "Decide first how the body text will look."
2. Then the scale (headings, small text) relative to body.
3. Then tracking per size.
4. Then hierarchy via weight and colour.
5. Then the micro details (numerals, punctuation, rag).

Never design headings first and squeeze body text in afterwards.

## 2. Body text: the four decisions

| Decision | Rule | Source |
|---|---|---|
| Size | Screen: 15 to 25px; default to 16 to 18px for app UI body, 17 to 21px for long reading. Never under 16px for inputs on mobile (iOS zooms). | Butterick; Hobday rule 20; Vercel |
| Line height | 120 to 145% of size for print-like text; 1.4 to 1.6 for screen body. Unitless in CSS. | Butterick; Rutter (Bringhurst on the web) |
| Line length | 45 to 90 characters (Butterick), 45 to 75 with 66 ideal (Bringhurst), 60 to 80 (Hobday). Default target: 60 to 70. | All three |
| Font | A professional, well hinted face with at least 5 weights, or the platform system font. Avoid Arial and Times New Roman as deliberate choices. | Butterick; Refactoring UI |

Butterick's warning on size: fonts with the same point size differ in apparent size (x-height). Judge size by eye, not by the number.

## 3. Measure (line length)

- **Single column body:** 45 to 75 characters, 66 ideal (Bringhurst 2.1.2).
- **Multi column text:** 40 to 50 characters per line.
- **In CSS, set measure in `ch` or `em`, not `px`.** Rutter: one character averages about 0.5em, so `max-width: 33em` gives about 66 characters at any font size. `max-width: 65ch` is the modern equivalent.
- **Do not let text stretch to the window edges** (Butterick). A 1440px wide paragraph is a defect.
- **Narrow columns need less leading, wide columns need more** (Refactoring UI, "Line-height is proportional").

Good: `.prose { max-width: 66ch; }`
Bad: body text inside a 100% width container on a desktop monitor.

## 4. Leading (line height)

- Body on screen: **1.4 to 1.6** (Rutter: values "upwards of 1.3 are common", his own site uses 1.5).
- UI labels, buttons, single lines: **1.2 to 1.3**.
- Large headings: **1.0 to 1.2**; display sizes can go to **0.9 to 1.05** (Refactoring UI: large text works near 1).
- Small text needs **more** leading relative to size, large text needs **less** (Refactoring UI, Apple).
- Scripts with tall ascenders and descenders (Arabic, Thai, Devanagari) need **more** leading (Apple WWDC20; WWDC22 notes Thai needs more vertical space). Design containers that can grow.
- Apple text styles ship tight and loose variants at **minus or plus 2pt** of line height (watchOS: 1pt). Example: iOS body 17pt on 22pt, tight 20pt, loose 24pt. Use tight in dense UI, loose for reading.
- **Always unitless** in CSS: `line-height: 1.5`, never `24px`. A fixed value overlaps lines when users enlarge text (Rutter 2.2.1).
- **Vertical rhythm:** space between blocks in multiples of the body line height (Rutter 2.2.2, Bringhurst "add and remove vertical space in measured intervals"). Example: 16px on 24px lines, paragraph gap 24px, heading margin top 48px bottom 24px.

## 5. Type scale and hierarchy

- **Never compose without a scale** (Bringhurst 3.1.1).
- Classic scale (Rutter applying Bringhurst, 16px base): 12, 14, 16, 18, 24, 36px.
- Refactoring UI hand tuned scale: **12, 14, 16, 18, 20, 24, 30, 36, 48, 60, 72px**. Steps of 2px at the small end, 12px at the top. Hand tuned beats a strict modular ratio because small sizes need finer steps.
- **Use 2 to 3 sizes per view** (Vignelli). His typical contrast: text and heading about **2x** apart (10pt and 20pt). Contrast of scale is what makes a layout forceful.
- **Hierarchy order of tools:** space, then weight, then colour, then size. Butterick: space above and below is "the best way to emphasize a heading". Refactoring UI: "Size isn't everything"; use weight and colour.
- **Three text colours are enough:** primary (near black), secondary (mid grey, for dates and metadata), tertiary (light grey, for footers and hints). Refactoring UI.
- **De-emphasize to emphasize.** When the main heading does not stand out, make the competing text lighter instead of making the heading bigger.
- **Separate visual hierarchy from document hierarchy.** An `h1` can be visually small (Refactoring UI). A page title in an app is often smaller than the content's key number.

## 6. Tracking (letter spacing) by size

Tracking must change with size. A single letter-spacing value for all sizes is wrong somewhere (Apple WWDC20: "Make any custom tracking size-specific").

- **Body (12 to 18px):** 0 or very slightly positive.
- **Small text (11 to 13px):** slightly positive, about +0.01em.
- **Headings (24px+):** negative. Typical: -0.01em at 24px, -0.02em at 32 to 48px, up to -0.03em for display sizes over 60px.
- **All caps and small caps:** +5 to +12% (CSS `0.05em` to `0.12em`). Butterick; Bringhurst gives 5 to 10%. Never set all caps without extra tracking.
- **Long digit strings** (serial numbers, codes): letterspace slightly (Bringhurst 2.1.6).
- **Never letterspace lowercase body text without a reason** (Bringhurst 2.1.7). Butterick: if the gaps are wide enough to fit another letter, it is too much.

Inter's published dynamic metrics (Rasmus Andersson) give a formula you can use for any neo-grotesque:

```
tracking_em = a + b * e^(c * size_px)
a = -0.0223, b = 0.185, c = -0.1745
```

Results: 12px about 0, 16px about -0.011em, 24px about -0.020em, 32px about -0.022em, 48px and up about -0.022em.

Apple SF Pro has the same behaviour built in: the system applies size specific tracking and switches from Text to Display design between 17 and 28pt (variable optical size).

## 7. Weights

- **No text weight under 400** (Rauno's interface guidelines). Thin weights break on low DPI screens and fail contrast.
- **Medium headings look best at 500 to 600** (Rauno).
- **Do not change font weight on hover or selection** (Rauno). It changes text width and shifts the layout. Change colour or background instead. If you must, reserve the bold width with a hidden bold copy or use a variable font with a fixed width axis.
- **Bold OR italic, never both together** (Butterick).
- **Use the fewest weights that make the hierarchy:** usually regular for text, medium or semibold for labels and headings, bold for the rare strong emphasis.
- **Pick fonts with at least 5 weights** (Refactoring UI); families with more weights usually had more care put in.

## 8. Headings

From Butterick, *Headings*:

- 3 levels maximum, 2 is better.
- Increase size by the **smallest visible step** (for 12pt text, try 12.5 or 13pt, not 14 or 15). On screen this usually means headings 1.1 to 1.5x body for in-content headings; save big jumps for page titles.
- A bold heading can be half to one point **smaller** than a regular one to balance its weight.
- Use bold, not italic, for headings.
- **No all caps headings** for anything longer than a short label.
- Emphasize with **space above** more than below, so the heading belongs to the text after it (Vignelli: "a line space above and none below").
- Do not center headings over left aligned text.

## 9. Numerals and data

- **Tabular figures** (`font-variant-numeric: tabular-nums`) for tables, timers, prices, counters, anything that changes or is compared (Vercel, Rauno). Without them, a ticking timer jitters.
- **Proportional oldstyle figures** read best inside running text if the font has them (Bringhurst 3.2.1: text figures in text, titling figures with caps).
- **Right align numbers in tables** so decimals line up (Refactoring UI).
- **Use one decimal convention per context:** currency with 0 or 2 decimals, never both on the same screen (Vercel).
- **Numbers as numerals** for counts ("3 files", not "three files") (Vercel).
- **A non breaking space between number and unit** ("10&nbsp;MB", "Cmd&nbsp;K") so they never split across lines (Vercel, Bringhurst 2.4.6).
- **Format for the user's locale** (Intl.NumberFormat, Intl.DateTimeFormat).

## 10. Punctuation and characters

- Curly quotes and apostrophes, never straight ones (Butterick, Vercel). Apostrophes point down.
- Straight marks only for feet and inches.
- The single ellipsis character, not three periods (Butterick, Vercel).
- Menu items that open a further step end with an ellipsis ("Rename..." written with the real character) (Vercel, Apple convention).
- One space between sentences.
- Real trademark and copyright symbols, not (c) or (tm).
- Do not use a double hyphen as a dash. (House rule for this skill: avoid long dashes entirely in UI copy; use a comma, a full stop, a colon or parentheses.)
- Avoid widows and orphans in headings and short paragraphs: `text-wrap: balance` for headings, `text-wrap: pretty` for paragraphs (Vercel: avoid widows and orphans).
- Underline only links, never for emphasis (Butterick).

## 11. Alignment and rag

- **Left align anything longer than 2 to 3 lines** (Refactoring UI). Center only short headlines, invitations, single lines (Vignelli: centred for "lapidary text").
- **Flush left, ragged right is the default** for screen text (Vignelli: "Most of the time we use flush left"). Watch the shape of the rag and fix awkward lines in headings by rewording or balancing.
- **Justified text requires hyphenation** (Butterick). On the web, avoid justification unless `hyphens: auto` and the language is set.
- **Align mixed sizes on the baseline, not the top or centre** (Refactoring UI, "Baseline, not center"). A large number next to a small unit shares one baseline.
- **Type hangs from rules:** when a label sits under a divider line, it sits close to the line above it (Vignelli: "Type should always hang from the ruler").

## 12. Choosing and pairing fonts

- **Default: the system UI font** (SF on Apple, Segoe on Windows, the platform face on Linux) or one high quality neutral sans (Inter, a grotesque). Apple: use system fonts and text styles; override only in exceptional cases.
- **Two typefaces maximum** (Hobday). A common premium pair: a neutral sans for UI plus either a serif or a display cut for headings. Linear uses Inter Display for headings and Inter for everything else: same family, different optical design.
- **Match the font to its size:** display faces have tighter spacing and smaller x-height; text faces have wider spacing and taller x-height (Refactoring UI; Apple SF Text vs SF Display).
- **Personality:** serif reads classic and elegant, rounded sans reads friendly and playful, geometric sans reads modern and clean (Refactoring UI, "Choose a personality").
- **Butterick's lists:** Arial is "the sans serif of last resort". Overexposed system defaults (Arial, Times New Roman, Verdana, Tahoma) signal no decision was made. On the web, a system UI stack is an acceptable modern choice because it renders natively.
- **Check character coverage** for every language the product supports before committing to a font.

## 13. Optical sizes and platform type

From Apple, *The Details of UI Typography* (WWDC20):

- Small sizes need wider spacing, sturdier thin strokes and larger details. Large sizes need tighter spacing and finer detail. That is what optical sizes do.
- SF Pro is variable; it moves from the Text design to the Display design between 17 and 28pt. In CSS, `font-optical-sizing: auto` does this for variable fonts with an `opsz` axis.
- Use predefined text styles (a set of size, weight and leading) instead of arbitrary sizes; emphasized styles use the bold trait with the same size.
- Support Dynamic Type or the platform text size setting, including for custom fonts. Scale padding with the text (`@ScaledMetric` on iOS, `rem` on the web).
- For truncation, allow the system to tighten tracking slightly before truncating (Apple's tight tracking table); never squeeze below legibility.

## 14. Text over colour, images and glass

- **No grey text on a coloured background** (Refactoring UI). Use a lighter or darker tint of the background hue, or white or black at reduced opacity.
- **On images, guarantee contrast** with an overlay, a lowered image contrast, or a tint (Refactoring UI, "Text needs consistent contrast").
- **On translucent materials, use vibrancy:** slightly heavier weight and higher contrast than on solid surfaces (Apple materials guidance via Emil's apple-design notes). Thin grey text on glass fails.
- **Contrast floor:** WCAG 2 4.5:1 for text under about 18px regular or 14px bold, 3:1 for larger text. Hover, active and focus states need **more** contrast than rest (Vercel).

## 15. CSS recipe

```css
:root {
  font-family: system-ui, -apple-system, "Segoe UI", Inter, sans-serif;
  font-size: 100%;           /* respect the user's browser setting */
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;   /* Rauno: antialiased smoothing on macOS */
  text-rendering: optimizeLegibility;
  font-kerning: normal;      /* Butterick: kerning always on */
}
.prose   { max-width: 66ch; font-size: 1.0625rem; line-height: 1.6; text-wrap: pretty; }
.label   { font-size: .8125rem; line-height: 1.3; letter-spacing: .01em; }
.caps    { text-transform: uppercase; letter-spacing: .08em; font-size: .75rem; }
.h2      { font-size: 1.5rem;  line-height: 1.25; letter-spacing: -.015em; font-weight: 600; text-wrap: balance; }
.display { font-size: clamp(2.25rem, 5vw, 4rem); line-height: 1.05; letter-spacing: -.025em; font-optical-sizing: auto; }
.num     { font-variant-numeric: tabular-nums; }
```

## 16. Checklist

- [ ] Body 16px+ with 1.4 to 1.6 leading and a 45 to 75 character measure
- [ ] A scale exists and each view uses 2 to 3 sizes
- [ ] Headings carry negative tracking from 24px up; all caps carry +0.05 to +0.12em
- [ ] No text weight under 400; no weight change on hover or selection
- [ ] Tabular figures wherever numbers change or are compared; numbers right aligned in tables
- [ ] Curly quotes, real ellipsis, non breaking spaces in "10 MB" and shortcuts
- [ ] Long text left aligned; headings balanced; no single word widows in headings
- [ ] No grey text on colour; text on images has a guaranteed contrast layer
- [ ] Line height unitless; spacing between blocks in multiples of the line height
- [ ] At most 2 typefaces; character coverage verified for every supported language

## 17. Sources

`../sources/books/practical-typography.md`, `elements-of-typographic-style.md`, `vignelli-canon.md`, `refactoring-ui.md`, `apple-wwdc-design-talks.md`, `rauno-freiberg-craft.md`, `vercel-web-interface-guidelines.md`, `anthony-hobday-safe-rules.md`, `linear-and-stripe-writeups.md`.
