# Typography

Type is most of any interface. Get body text right first, then build the scale around it.

## Contents

1. Body text: the four numbers
2. Type scale
3. Line height
4. Letter spacing and case
5. Weights and emphasis
6. Font choice and pairing
7. Optical sizes and variable fonts
8. Numerals and details
9. Units and responsive type
10. Review checklist

## 1. Body text: the four numbers

Four choices decide how body text reads: size, line height, line length, typeface (Butterick, Practical Typography).

| Setting | Rule | Test |
|---|---|---|
| Size (web) | 16 to 20 px body on marketing pages, never below 16 px for paragraphs. Butterick's comfortable web range is 15 to 25 px. | Inspect computed `font-size` of `p`. |
| Line length | 45 to 75 characters per line, 66 is the classic ideal (Bringhurst, via Rutter). Multi column: 40 to 50. | Count characters on the longest line, or set `max-width` in `ch`. |
| Line height | 1.4 to 1.6 for body (Butterick: 120 to 145 percent of size; longer lines need more). | Computed `line-height` unitless. |
| Paragraph gap | One line height, or 0.75 to 1 em. Never indent and space at once. | |

```css
/* Good: measure in ch, unitless line height */
.prose { font-size: 1.125rem; line-height: 1.55; max-width: 65ch; }

/* Bad: measure in px, it shrinks to ~50 chars when the user enlarges text,
   and a full width paragraph on a 1440 px screen runs to 180 chars */
.prose { font-size: 18px; line-height: 27px; width: 100%; }
```

Rule: a paragraph never spans the full width of a desktop viewport. Hero subheads included: cap at about 40 to 60 ch so they wrap into 2 or 3 balanced lines.

## 2. Type scale

"Don't compose without a scale" (Bringhurst 3.1.1). Pick one ratio and derive every size from it.

| Ratio | Name | Use |
|---|---|---|
| 1.125 | Major second | Dense app UI, dashboards |
| 1.2 | Minor third | General app UI, mobile marketing |
| 1.25 | Major third | Marketing pages on mobile, docs |
| 1.333 | Perfect fourth | Marketing pages on desktop |
| 1.5 and up | Fifth and above | Editorial, big display moments only |

Example scale at 16 px base, ratio 1.25: 12.8, 16, 20, 25, 31.25, 39, 48.8, 61. Round to whole pixels (13, 16, 20, 25, 31, 39, 49, 61).

Rules:

- Use 5 to 8 sizes for a whole product, not 15. A landing page typically needs: caption 13 to 14, body 16 to 18, lead 20 to 22, h3 24, h2 32 to 40, h1 48 to 72 (desktop).
- NN/g: within one view use no more than 3 size levels for content (small, medium, large), and at most 2 elements at the largest size.
- Headings grow in small steps in long documents (Butterick: the smallest visible step), but marketing heroes need a big jump: hero h1 at 2.5x to 4x body size.
- Use a fluid scale between two viewport widths instead of breakpoint jumps (Utopia method: 1.2 ratio at 320 px, 1.333 at about 1500 px).

```css
/* h1: 40px at 360px viewport, 72px at 1440px viewport */
h1 { font-size: clamp(2.5rem, 1.833rem + 2.963vw, 4.5rem); }
```

Fluid type must still respond to user font size: always mix `rem` into `clamp()`, never pure `vw` (pure vw breaks WCAG 1.4.4 resize text).

## 3. Line height

Line height shrinks as size grows.

| Text | Line height |
|---|---|
| Caption, 12 to 14 px | 1.4 to 1.5 |
| Body, 16 to 20 px | 1.45 to 1.6 |
| Lead / subhead, 20 to 24 px | 1.35 to 1.45 |
| Headings, 24 to 40 px | 1.15 to 1.3 |
| Display, 48 px and up | 1.0 to 1.1 |

- Always unitless in CSS (`1.5`, not `24px`), so it scales with the element.
- WCAG 1.4.12: the layout must survive the user forcing line height 1.5, paragraph spacing 2x, letter spacing 0.12 em, word spacing 0.16 em. No fixed heights on text containers: use `min-height`.
- Tall x-height fonts (Inter, SF Pro) need slightly more line height than small x-height fonts (Garamond) at the same size.

## 4. Letter spacing and case

- All caps and small caps: add 5 to 12 percent tracking, `letter-spacing: 0.05em` to `0.12em` (Butterick). Bad: all caps eyebrow label at 0 tracking.
- Lowercase body: 0. Do not track body text.
- Large display text (40 px and up): tighten, `-0.01em` to `-0.03em`. Most premium product sites (Linear, Stripe, Raycast, Notion) set hero text with negative tracking. Fonts with a display optical size already do this; do not double it.
- All caps only for short labels under one line. Never all caps paragraphs or buttons with long labels (Duolingo's all caps buttons work only because labels are 2 to 4 words and tracked).

## 5. Weights and emphasis

- Use 2 to 3 weights per family: regular 400, medium 500 or semibold 600, bold 700. A hero may use one heavier display weight.
- Never use weights below 400 under 20 px. Light text (300) at small size fails contrast in practice even when its colour passes.
- Bold or italic, never both on the same words. No underline except links.
- De-emphasize to emphasize: make secondary text lighter in colour (step 11 of a Radix scale, or 60 to 70 percent contrast), not smaller and lighter and thinner at once.
- Two-tone headline (Stripe pattern): first clause in full text colour, the rest of the sentence in a muted colour at the same size. This creates hierarchy without a second size.

## 6. Font choice and pairing

Default: one excellent sans family for everything. Premium products rarely use more than two families.

- Safe choices for app marketing: Inter / Inter Display (Linear uses Inter Display for headings and Inter for everything else), SF Pro via `system-ui` on Apple, Geist, Manrope, General Sans, Satoshi, Open Runde (soft rounded). Serif accents: Newsreader, Fraunces, Instrument Serif, Source Serif.
- Pairing rules (Typekit type study, Google Fonts Knowledge):
  1. A superfamily (shared skeleton, matched x-height, cap height and baseline) pairs safely with itself: Inter + Inter Display, Source Serif + Source Sans, IBM Plex Sans + Plex Serif.
  2. Pairing two families: match x-height first, then create contrast on one axis only (serif vs sans, or expressive vs neutral). Two faces that are almost the same look like a mistake.
  3. Give each face one job: display face for h1 and h2 only, text face for everything else. Never alternate per section.
  4. Shared history helps: old style serifs pair with humanist sans.
- Test a pair by setting a headline and a paragraph together at real sizes, not by comparing specimens.
- Check character coverage before choosing (Cyrillic, Kazakh letters like Ә Ғ Қ Ң Ө Ұ Ү Һ І, Turkish, Vietnamese). A missing glyph falls back to a different font mid word.
- Bad: a geometric display font with tiny x-height over a large x-height body font; 3 families on one page; a script font for UI.

## 7. Optical sizes and variable fonts

- Optical sizes: small text needs sturdier strokes, open spacing and larger x-height; large text can be finer and tighter. Fonts with an `opsz` axis (Inter 4, SF Pro, Roboto Flex, Fraunces, Newsreader) adjust automatically: `font-optical-sizing: auto` is the default.
- If the family ships separate cuts (Inter Display, SF Pro Display vs Text), use Display at 20 px and up, Text below.
- Variable fonts: one file replaces several weights. Use them when you need 3+ weights; otherwise 2 static WOFF2 files can be smaller. See `platforms/web/performance-and-loading.md`.

## 8. Numerals and details

- Prices, tables, timers, counters, stats: `font-variant-numeric: tabular-nums;` so digits do not jump. Large display numbers in a hero: proportional is fine.
- Use real typographic characters: curly quotes, apostrophe, the single ellipsis character, the multiplication sign for dimensions, non-breaking space between number and unit (`10&nbsp;GB`) and inside brand names.
- Headlines: `text-wrap: balance;` so a 2 line headline does not end with one orphan word. Paragraphs: `text-wrap: pretty;`.
- Left align body text. Centre only short blocks (hero headline, a subhead of 1 to 3 lines, a short closing CTA). Never centre more than 3 lines.
- Hanging punctuation and optical alignment: large quotation marks and big headlines may need a 1 to 2 px nudge so letters, not their sidebearings, align with the column edge.

## 9. Units and responsive type

From Josh Comeau's pixels and accessibility study:

- Font sizes in `rem`. Px font sizes ignore the user's default font size.
- Vertical spacing around text in `rem` or `em`.
- Horizontal padding and borders in `px`, so text growth does not eat the line width.
- Media queries in `rem`, so users with large text get the narrower layout sooner.
- Test with the browser default font size at 32 px: nothing may overlap or clip.

## 10. Review checklist

- [ ] Body text 16 px or more, line height 1.4 to 1.6, line length 45 to 75 ch.
- [ ] Every size comes from one scale; count distinct sizes in the CSS (8 or fewer).
- [ ] Hero h1 is 2.5x to 4x body, negative tracking at display sizes, balanced wrapping.
- [ ] All caps labels tracked +0.05 to +0.12 em.
- [ ] Two families at most; each has one role; x-heights compatible.
- [ ] Tabular numbers in prices and tables.
- [ ] No text under 12 px anywhere; no weight under 400 below 20 px.
- [ ] Layout survives WCAG text spacing overrides and 200 percent zoom.
