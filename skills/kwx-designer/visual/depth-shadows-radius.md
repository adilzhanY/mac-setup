# Depth, shadows and radius

Depth tells people what sits on top of what, and therefore what they can touch. Keep one light source, one elevation scale and one radius scale.

## Contents

1. Light source
2. Elevation scale
3. Shadow recipes
4. Borders with shadows
5. Depth in dark mode
6. Radius scale
7. Nested radii
8. Review checklist

## 1. Light source

- One light source for the whole product, above and very slightly in front: shadows fall downward (y offset), with x offset 0 or very small. Josh Comeau's elevation demo keeps vertical offset at twice the horizontal one when x is used.
- Raised elements get a lighter top edge (an inset highlight `inset 0 1px 0 rgb(255 255 255 / 0.1)` works on dark buttons); recessed elements (inputs, wells) get a darker top inner edge (Refactoring UI: emulate a light source).

## 2. Elevation scale

Five levels are enough. Higher elevation means: bigger offset, bigger blur, lower opacity per layer.

| Level | Used for |
|---|---|
| 0 | Page, flat sections, cards that sit in the page (border only) |
| 1 | Cards that lift on hover, inputs, segmented controls |
| 2 | Dropdowns, popovers, sticky headers |
| 3 | Floating panels, toasts |
| 4 | Modals, dialogs |

A component moves at most one level on hover. Elevation communicates layering, so a modal never sits lower than a dropdown.

## 3. Shadow recipes

Layer at least two shadows (Vercel): a tight, darker one for contact and a wide, soft one for ambient light (Refactoring UI: shadows can have two parts). Josh Comeau's layered technique doubles offset and blur each layer at low opacity:

```css
:root {
  --shadow-color: 220 40% 20%;            /* tinted toward the background hue, not black */
  --shadow-1: 0 1px 2px hsl(var(--shadow-color) / 0.08),
              0 1px 1px hsl(var(--shadow-color) / 0.06);
  --shadow-2: 0 1px 1px hsl(var(--shadow-color) / 0.06),
              0 2px 4px hsl(var(--shadow-color) / 0.06),
              0 4px 8px hsl(var(--shadow-color) / 0.06);
  --shadow-3: 0 1px 1px hsl(var(--shadow-color) / 0.05),
              0 2px 4px hsl(var(--shadow-color) / 0.05),
              0 4px 8px hsl(var(--shadow-color) / 0.05),
              0 8px 16px hsl(var(--shadow-color) / 0.05);
  --shadow-4: 0 1px 1px hsl(var(--shadow-color) / 0.075),
              0 2px 2px hsl(var(--shadow-color) / 0.075),
              0 4px 4px hsl(var(--shadow-color) / 0.075),
              0 8px 8px hsl(var(--shadow-color) / 0.075),
              0 16px 16px hsl(var(--shadow-color) / 0.075);
}
```

Rules:

- Tint shadows with the background hue (for a blue-tinted page, a desaturated dark blue). Black at partial opacity turns coloured backgrounds muddy grey.
- Bad: `box-shadow: 0 0 20px rgba(0,0,0,0.5)`. No offset means no light source, and 0.5 opacity reads as a dirty halo. This is the most common amateur shadow.
- Bad: coloured glow shadows under every card. Reserve a coloured shadow (step 9 of the accent at low opacity) for one hero element at most.
- `filter: drop-shadow()` follows the real shape (transparent PNG device mockups, tooltips with arrows); `box-shadow` follows the box.
- Never animate a layered `box-shadow` directly; animate the opacity of a pseudo-element that holds the larger shadow. Test on low-end phones.
- Flat designs still have depth: a slightly lighter or darker surface, or overlapping elements, does the job without any shadow (Refactoring UI).

## 4. Borders with shadows

- Combine a hairline border with a soft shadow for crisp edges on light themes: `border: 1px solid oklch(0.2 0.02 286 / 0.08)` plus `--shadow-1`. Semi-transparent borders adapt to any background (Vercel).
- Use fewer borders: prefer spacing, a background tint, or a shadow to separate things. A page of boxed boxes looks like a form, not a product.
- 1 px borders in px, never rem.

## 5. Depth in dark mode

- Shadows nearly vanish on dark backgrounds. Elevate by lightening the surface (about +0.02 to +0.04 OKLCH L per level) and add a subtle top highlight or a lighter border (step 6 or 7 of the dark scale).
- A dark shadow is still useful under modals to separate them from a dimmed backdrop; use a higher opacity (0.3 to 0.5) because the background is already dark.

## 6. Radius scale

Radius sets personality: small radii feel precise and professional, large radii friendly and soft (Refactoring UI: choose a personality). Choose one personality and keep it everywhere.

| Token | Value | Used for |
|---|---|---|
| `--radius-xs` | 4 | Tags, checkboxes, small chips |
| `--radius-sm` | 6 to 8 | Inputs, small buttons |
| `--radius-md` | 10 to 12 | Buttons, menus, list cells |
| `--radius-lg` | 16 to 20 | Cards, pricing cards, sheets |
| `--radius-xl` | 24 to 32 | Large media frames, feature panels, modals on mobile |
| `--radius-full` | 9999 | Pills, avatars, segmented toggles |

- Radius grows with component size; a 400 px card with a 4 px radius looks sharp-cornered, a 32 px button with a 16 px radius is a pill.
- Do not mix sharp and round personalities (square buttons next to pill tags) unless the contrast is a deliberate system rule.
- Apple-style continuous corners (squircles) look smoother than circular arcs at large radii. On the web, approximate with a slightly larger radius, or `corner-shape: squircle` where supported, or an SVG mask for hero device frames.
- Device mockups use the device's real corner radius; do not round a screenshot with an arbitrary radius.

## 7. Nested radii

Nested corners must be concentric: **inner radius = outer radius minus the padding between them** (Vercel: child radius never larger than the parent).

| Outer card radius | Padding | Inner element radius |
|---|---|---|
| 24 | 8 | 16 |
| 20 | 12 | 8 |
| 16 | 16 | 0 to 4 (use the scale minimum) |

Bad: a 16 px radius image inside a 16 px radius card with 16 px padding; the corners look pinched and the gap uneven.

## 8. Review checklist

- [ ] All shadows from the 4 to 5 token scale; no ad-hoc `box-shadow`.
- [ ] Every shadow has a y offset; none is pure black at high opacity.
- [ ] Hover lifts by one level at most.
- [ ] Dark theme elevates by surface lightness.
- [ ] Radii from the scale; nested radii concentric (inner = outer minus padding).
- [ ] One personality across buttons, inputs, cards and badges.
