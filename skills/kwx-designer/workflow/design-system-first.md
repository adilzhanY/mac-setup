# Design system first

Define the tokens before the first component. Every later decision (a card, a chip, a chart) is then a choice from the system instead of a new guess, which is what keeps screen 80 consistent with screen 1. If the project already has a token system, use it and do not add literal values; extend it only through its own mechanism.

Numbers come from Kole Jain (every UI concept, mobile UI, dashboard flaws) and uxpeak (strawberry redesign). Numbers marked (est.) were read off video frames, not stated.

## Contents

1. Colour: one brand colour to an 11 step ramp
2. Neutrals, semantic colours, dark mode
3. Type: one font, a capped scale
4. Spacing: the 4 point system
5. Radii
6. Shadows and elevation
7. Icons
8. Component states
9. Motion
10. A starter token file
11. Checks

---

## 1. Colour: one brand colour to an 11 step ramp

1. Start with one primary colour, usually the brand colour (Kole's example: a vivid violet, about #5b33f5, est.).
2. Lighten it for backgrounds, darken it for text. In the "Raspberry Turkish Delight" example the page is a very light tint, the panel a slightly darker tint, the heading the primary darkened to a deep violet, the chip a light tint, the button the primary.
3. Build the ramp: 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950 (11 steps). 500 is usually the base. Build chips, states and charts from it (the Cashflow chart uses three ramp steps in stacked bars).
4. Generate the ramp in a perceptual space (OKLCH): keep hue fixed, step lightness evenly, reduce chroma toward both ends so the lightest and darkest steps do not look neon or muddy.
5. Typical use: 50 to 100 tinted backgrounds, 200 to 300 borders and selected fills, 500 to 600 buttons and accents, 700 to 900 text on tints.
6. "Let the colour find you": colour appears where it has meaning (an announcement pill, a focus ring, a "New" chip), never as decoration.
7. Desaturate. No neon (#00FF00 like greens) unless the brand truly is neon.

## 2. Neutrals, semantic colours, dark mode

**Neutrals**: a grey ramp tinted slightly toward the brand hue. A green brand gets a near black with a green tint, not a generic navy (Kole Jain, vibe coded SaaS).

**Semantic**: blue = info, trust, focus; red = danger, error, urgency; yellow = warning; green = success, new. Each with its own small ramp (a tint for backgrounds, a mid for icons and borders, a dark for text on the tint). Red only for urgent or destructive.

**Dark mode**

- Depth by lightness: raised surfaces lighter than the background, no shadows for depth.
- Borders low contrast (a bright border on a dark card is too harsh).
- Chips: desaturate and darken the fill, make the text the bright colour.
- Tinted darks (deep purple, red, green, teal) are fine, not only navy or grey.
- Body text a light grey, not pure white, on large areas.

## 3. Type: one font, a capped scale

1. One family. "You'll never need more than one [font] for any design." Kole's list: DM Sans, Axiforma, SF Pro, Geist, Plus Jakarta Sans, Montserrat, Unbounded. uxpeak switched the strawberry page to Lato. A mono family for code or IDs is allowed as a second, functional face.
2. Scale caps:

| Context | Sizes (px) |
|---|---|
| Marketing site, 6 sizes maximum | 64, 42, 32, 20, 16, 14 |
| Dashboard, nothing above about 24 | 24, 20, 18, 16, 14, 12 |
| Mobile | Body at the platform base: 17 on iOS (macOS base is 13); never smaller than desktop |

3. Line heights: hero heading 64/72, subtext 20/28, eyebrow pill 16/20; sidebar label 15/24. Display text 110% to 120%; body about 150% to 160%.
4. Letter spacing: display text -2% to -3%; small uppercase labels positive (about +4% to +8%).
5. Weights: 3 at most (regular, medium, semibold or bold). The strawberry title went from a very heavy black weight to medium.
6. Tabular figures for numbers in tables and prices.
7. Never write a literal size in a component; every size comes from the scale.

## 4. Spacing: the 4 point system

1. Every size, gap and padding is a multiple of 4, "not because it inherently looks better, but because you can always split things in half".
2. Scale: 4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96.
3. Rhythm: one default gap between stacked sections of a block (32 in the hero), half (16) between things that belong together.
4. Side margin: one value per breakpoint (24 in the strawberry example on mobile).
5. Button padding: horizontal about twice vertical (32 sides, about 16 top and bottom; the vertical value is implied).
6. Grids: 12 columns desktop, 8 tablet, 4 mobile for repeating content. Custom landing layouts may break the grid; white space matters more than columns.
7. Touch targets 44 minimum; tab cells about 72 x 48.

## 5. Radii

The videos show values, not a stated scale, so these are estimates from frames (est.):

| Element | Radius |
|---|---|
| Chips, pills, buttons, tab bars | Full (pill) |
| Inputs, small buttons | 8 to 12 |
| Menus, popovers | about 12 |
| Cards | 12 to 16 (mobile cards 16 to 20) |
| Sheets, modals | 16 to 24 on the top corners |

Rule: nested radii shrink by the padding between them (inner radius = outer radius minus padding), so corners stay concentric.

## 6. Shadows and elevation

1. Default shadows are too strong: lower opacity, raise blur. "If the shadow is the first thing you notice on a design, you're not using it right."
2. Strength scales with elevation: card subtle, popover, menu and dropdown stronger, modal strongest.
3. Inner plus outer shadow for tactile raised buttons.
4. Dark mode: lightness for depth, shadows only for overlays.

Example tokens (light mode):

```
--shadow-1: 0 1px 2px rgb(0 0 0 / 0.04), 0 2px 8px rgb(0 0 0 / 0.04);   /* card */
--shadow-2: 0 4px 12px rgb(0 0 0 / 0.08), 0 12px 32px rgb(0 0 0 / 0.08); /* popover, menu */
--shadow-3: 0 8px 24px rgb(0 0 0 / 0.12), 0 24px 64px rgb(0 0 0 / 0.12); /* modal */
```

## 7. Icons

1. One library (Phosphor, Lucide or similar), one stroke weight, one style.
2. Icon size equals the line height of the text beside it (24 icon for 15/24 text); tight gap.
3. Menu and header icons 16; nav icons 24 (with 24 line height labels).
4. No emoji, no Unicode symbols as icons. Draw missing icons on the library's grid.

## 8. Component states

Define these as tokens or variants before building screens:

| Component | States |
|---|---|
| Button | default, hover, pressed, disabled, loading; variants primary (one per view), secondary, ghost, destructive |
| Input | default, hover, focus (accent 2 px border plus ring), error, warning, disabled, loading |
| Nav item | ghost default, hover fill, active highlight, focus |
| Chip | category (dot plus label), status (icon plus word, tinted), tag (grey), selected |
| Row | default, hover, selected, inactive |
| Feedback | toast info, success, warning, error; inline "Copied!" chip |

## 9. Motion

1. UI transitions about 150 to 300 ms, eased out on enter.
2. Animate actions in and out when context changes (mobile toolbars).
3. Swipe back parallax: underlying page offset about 35%.
4. Respect reduced motion.

## 10. A starter token file

Adapt names to the project's conventions. Values are a neutral starting point, not a brand.

```css
:root {
  /* brand ramp: replace with your OKLCH ramp of the brand colour */
  --brand-50:  oklch(0.97 0.02 150); --brand-100: oklch(0.94 0.04 150);
  --brand-200: oklch(0.88 0.07 150); --brand-300: oklch(0.80 0.10 150);
  --brand-400: oklch(0.71 0.13 150); --brand-500: oklch(0.62 0.14 150);
  --brand-600: oklch(0.53 0.13 150); --brand-700: oklch(0.45 0.11 150);
  --brand-800: oklch(0.37 0.09 150); --brand-900: oklch(0.29 0.06 150);
  --brand-950: oklch(0.21 0.04 150);

  --font-sans: "Geist", system-ui, sans-serif;
  --text-xs: 12px; --text-sm: 14px; --text-md: 16px;
  --text-lg: 18px; --text-xl: 20px; --text-2xl: 24px;   /* dashboard cap */
  --leading-body: 1.55; --leading-display: 1.15;
  --tracking-display: -0.025em; --tracking-caps: 0.06em;

  --space-1: 4px; --space-2: 8px; --space-3: 12px; --space-4: 16px;
  --space-5: 20px; --space-6: 24px; --space-8: 32px; --space-10: 40px;
  --space-12: 48px; --space-16: 64px;

  --radius-sm: 8px; --radius-md: 12px; --radius-lg: 16px; --radius-full: 9999px;
}
```

## 11. Checks

| Check | Pass when | Verify in code |
|---|---|---|
| Tokens exist before components | A token file defines colour, type, space, radius, shadow | Find the file |
| No literal values | Components use tokens only | `grep -rnE '[0-9]+px' src/components` outside the token file; each hit justified |
| 11 step ramp | Brand ramp has 50 to 950 | Read the ramp |
| Neutrals tinted | Background hue matches the brand hue | Compare hue values |
| One family | One sans token (plus optional mono) | Read font tokens |
| Scale capped | Dashboard max 24; marketing 6 sizes | Count size tokens per context |
| 4 pt | All spacing tokens multiples of 4 | Read the spacing scale |
| Shadow tiers | Card shadow weaker than popover weaker than modal | Compare tokens |
| States defined | Every component in section 8 has all its states | Read component variants |
