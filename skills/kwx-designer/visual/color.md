# Colour

Premium colour is mostly restraint: tinted neutrals, one accent, perceptual scales, and contrast that is measured, not guessed.

## Contents

1. Work in OKLCH
2. Scale structure: 12 roles per hue
3. Building a palette
4. Neutrals
5. Accent and semantic colours
6. Contrast: WCAG 2 and APCA
7. Dark mode done right
8. Wide gamut (P3)
9. Tokens
10. Review checklist

## 1. Work in OKLCH

HSL lightness lies: yellow and blue at the same HSL lightness look nothing alike. Stripe rebuilt its palette in CIELAB for that reason; Linear moved its theme generation from HSL to LCH; Tailwind v4 defines every colour in OKLCH.

`oklch(L C H)`: L is perceived lightness 0 to 1, C is chroma (0 is grey, practical maximum about 0.37), H is hue angle (about 20 red, 90 yellow, 140 green, 220 blue, 320 purple).

- Same L means same perceived lightness across hues, so a red and a blue button at `oklch(0.6 0.15 H)` feel equally heavy.
- Derive states by moving L only: hover `oklch(from var(--accent) calc(l - 0.05) c h)`.
- Max chroma depends on hue and lightness. Yellow cannot be dark and saturated; blue cannot be light and saturated. Check in oklch.com before committing.
- Rule of thumb (Evil Martians): any background with L 0.87 or above takes black text safely. A lightness gap of only 0.20 between text and background is not enough.

## 2. Scale structure: 12 roles per hue

Use Radix Colors' 12 step semantics even if you generate your own values. Every step has one job:

| Step | Job |
|---|---|
| 1 | App background |
| 2 | Subtle background (cards, sidebars, striped rows, code blocks) |
| 3 | Component background, normal |
| 4 | Component background, hover |
| 5 | Component background, pressed or selected |
| 6 | Subtle border on non-interactive things (cards, separators) |
| 7 | Border on interactive components |
| 8 | Strong border, focus ring |
| 9 | Solid: the pure brand colour, highest chroma (buttons, badges) |
| 10 | Solid hover |
| 11 | Low contrast text (guaranteed APCA Lc 60 on step 2) |
| 12 | High contrast text (guaranteed APCA Lc 90 on step 2) |

Most step 9 colours take white text; sky, mint, lime, yellow and amber take dark text.

Tailwind's alternative is 11 steps, 50 to 950, with 500 as the base. Either works; mixing the two in one project does not.

Stripe's testable rule for any numbered scale with an even lightness curve: two levels **5 apart** pass 4.5:1 for small text; **4 apart** pass 3:1 for icons and large text. Design your scale so this holds for every hue, then contrast becomes arithmetic.

## 3. Building a palette

Refactoring UI method, done in OKLCH:

1. Greys: 8 to 10 shades. Primary: 5 to 10 shades. Each accent and semantic colour: 5 to 10 shades. A full product may need about 10 hues.
2. Pick the base (step 9 or 500) by eye as a button background.
3. Pick the darkest and lightest by where they are used (text on tint, page background).
4. Fill the middle in even L steps. Raise chroma slightly toward the middle and lower it at the extremes, or the light tints look washed out and the darks look muddy.
5. Rotate hue slightly toward a brighter neighbour for light steps and a darker neighbour for dark steps (yellow drifts toward orange as it darkens) so shades do not look dirty.
6. Define every shade up front. Never `lighten()` or `darken()` on the fly; never fake tints with opacity on coloured backgrounds (it changes with whatever is behind).

Linear's lesson: a theme can be generated from 3 inputs (base, accent, contrast) instead of 98 hand-set variables, if the generator works in a perceptual space. A `contrast` input makes a high contrast theme free.

## 4. Neutrals

- Never pure grey and never pure black text on pure white for large surfaces. Tint neutrals toward the brand hue with chroma 0.005 to 0.02 (Tailwind zinc is hue about 286 at chroma 0.016; slate leans blue; stone leans warm).
- Text: step 12 (about L 0.15 to 0.25 in light mode) for primary, step 11 for secondary. Avoid more than 3 text colours.
- Never put grey text on a coloured background: use a lighter or darker shade of that background's own hue instead (Refactoring UI).
- Borders: semi-transparent tints of the text colour (for example `oklch(0.2 0.02 286 / 0.10)`) adapt to any surface. Vercel's guidelines: tint borders, shadows and text toward the background hue.

## 5. Accent and semantic colours

- One accent carries action. If everything is the accent colour, nothing is. The primary CTA, links, focus ring and selected state share it; decorative use is rare.
- NN/g: in simple designs about 2 primary and 2 secondary colours; at most 3 contrast variations.
- Semantic: red for destructive and errors, amber for warnings, green for success, blue for information. Keep each at matched L so no status shouts louder than another.
- Never rely on colour alone (WCAG 1.4.1): pair status colour with an icon, label or shape. About 8 percent of men and 0.5 percent of women have a colour vision deficiency.
- Gradients: keep them within about 60 degrees of hue and interpolate in OKLCH (`linear-gradient(in oklch, ...)`) to avoid the grey dead zone of sRGB interpolation.

## 6. Contrast: WCAG 2 and APCA

WCAG 2.2 AA is the legal baseline in most places; meet it always.

| WCAG 2 criterion | Requirement |
|---|---|
| 1.4.3 Text | 4.5:1; large text (24 px regular or 18.66 px bold) 3:1 |
| 1.4.11 Non-text | 3:1 for component boundaries, icons that carry meaning, focus indicators, chart marks |
| 1.4.6 Enhanced (AAA) | 7:1 text, 4.5:1 large |

WCAG 2 math overstates contrast for dark colours (it lets poor dark mode pairs pass). Vercel's guidelines prefer APCA. Use APCA as the design target and WCAG 2 as the compliance floor.

APCA Lc targets (Bronze, from the APCA documentation):

| Lc | Use | Minimum font |
|---|---|---|
| 90 | Preferred for body text | 14 px / 400, or 18 px / 300 |
| 75 | Minimum for body text columns | 18 px / 400, 16 px / 500, 14 px / 700 |
| 60 | Other content text (labels, short lines) | 24 px / 400, 16 px / 700 |
| 45 | Headlines, large text, fine icons | 36 px / 400, 24 px / 700 |
| 30 | Placeholder, disabled, copyright line | any, solid icons 5.5 px min |
| 15 | Dividers, non-semantic shapes | 5 px min dimension; below this treat as invisible |

Lc 90 is also a soft maximum for very large bold text and big colour fields: pure white on pure black at 64 px glares. Small text has no maximum.

Test: compute both numbers for every text token on every surface token, in both themes. Record the pairs in the token file.

## 7. Dark mode done right

Dark mode is a second palette, not an inversion.

- Base surface: dark grey, not black. Material's baseline is `#121212`; tinted versions work better, for example `oklch(0.16 0.01 286)`. Pure black is acceptable only for OLED focused apps and full-bleed media.
- Elevation goes lighter, not darker: each raised surface lifts L by about 0.02 to 0.04 (Material used a white overlay of roughly 5 percent at 1 dp up to 16 percent at 24 dp). Shadows barely show on dark, so the surface lightness does the work.
- Text: about 87 percent, 60 percent and 38 percent white for high, medium, disabled (Material), or Radix steps 12 / 11 from the dark scale.
- Desaturate accents: drop chroma 10 to 30 percent and raise L so the accent stays Lc 60+ on the dark surface (Material used the 200 tone of the primary instead of 500). Saturated colours vibrate on dark grounds.
- Borders matter more in dark mode; use step 6 or 7 of the dark scale.
- Images and illustrations: provide dark variants or dim photos slightly (`filter: brightness(0.9)`); never invert screenshots.
- CSS plumbing: `color-scheme: light dark` on `:root`, set `<meta name="theme-color">` per scheme to match the page background, follow `prefers-color-scheme` and allow a manual override.

## 8. Wide gamut (P3)

sRGB covers about 35 percent of visible colours; P3 adds about 30 percent more, and every recent iPhone and Mac shows it. For a mobile app landing page, most visitors see P3.

```css
:root { --accent: oklch(0.65 0.19 255); }
@media (color-gamut: p3) { :root { --accent: oklch(0.65 0.24 255); } }
```

Only push chroma on accents and illustrations, never on text tokens.

## 9. Tokens

Components never reference raw colours. Two layers:

1. Palette: `--blue-1` to `--blue-12`, `--gray-1` to `--gray-12`, per theme.
2. Semantic aliases: `--bg`, `--bg-subtle`, `--surface`, `--surface-raised`, `--border`, `--border-strong`, `--text`, `--text-muted`, `--accent`, `--accent-hover`, `--accent-contrast` (text on accent), `--focus`, `--danger`, `--success`, `--warning`.

Dark mode swaps only layer 1 or the alias mapping. A component file containing a hex value is a defect.

## 10. Review checklist

- [ ] All colours defined in OKLCH (or generated from a perceptual space) as tokens.
- [ ] Every hue follows the same lightness curve; 5 steps apart passes text contrast.
- [ ] Neutrals tinted (chroma 0.005 to 0.02), no pure grey.
- [ ] One accent; the primary CTA is the most saturated thing on screen.
- [ ] Every text/surface pair meets WCAG 2 AA and the APCA target for its size, in both themes.
- [ ] No status communicated by colour alone.
- [ ] Dark theme: no pure black base, elevation by lightness, desaturated accents, own `theme-color`.
