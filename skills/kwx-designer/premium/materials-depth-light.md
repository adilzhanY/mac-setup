# Materials, depth and light

How surfaces, shadows, borders and translucency make an interface feel physical and expensive instead of flat or fake. Vignelli: "Light is the master of form and texture." Jeremy Keith, after architecture: "One material should not be used as a substitute for another. Otherwise the end result is deceptive."

## Contents

1. Principles
2. The light source
3. Elevation: what changes as a surface rises
4. Shadow recipes (with values)
5. Shadow colour
6. Borders that work with shadows
7. Depth without shadows (flat and dark themes)
8. Colour of surfaces and neutrals
9. Glass, blur and translucency
10. Layering, overlap and focus
11. Texture, gradients and finish
12. Checklist
13. Sources

---

## 1. Principles

- **Depth encodes hierarchy, not decoration.** Raised means "interactive" or "on top right now". A shadow on everything means nothing is on top.
- **One depth technique per product** (Hobday rule 27): soft shadows, or hard offset shadows, or flat with borders. Mixing reads as inconsistent.
- **Honest materials** (Keith, *Resilient Web Design*): use the real CSS property for the effect (`border-radius`, `box-shadow`, `backdrop-filter`) and let it degrade, rather than faking it with images.
- **Apple Liquid Glass is a functional layer:** it floats above content to hold navigation and controls. Content itself stays on a solid, quiet surface.

## 2. The light source

- **One global light source for every shadow,** from above and slightly to the left (Josh Comeau). Treat it as distant like the sun, so every element casts at the same angle.
- **Keep the offset ratio constant across elevations.** Comeau keeps vertical offset at 2x horizontal. Many UI systems use a purely vertical offset (light straight above); either is fine if it is the same everywhere.
- **Vertical offset looks more natural than none.** Steve Schoger: a slight vertical offset makes shadows look real; `0 0 Npx` centred glows look like a halo, not a shadow.
- **Light catches top edges.** A 1px lighter top border (inset highlight) on raised surfaces reads as light hitting the edge: `box-shadow: inset 0 1px 0 rgb(255 255 255 / 0.1)` on dark, `0.6` or more on light (Apple materials via Emil's notes: bright top edge = light catching the material).
- **Closer surfaces are lighter,** in light and dark themes alike (Hobday rule 15), because they are nearer the light.

## 3. Elevation: what changes as a surface rises

From Comeau and Refactoring UI:

| As elevation increases | Change |
|---|---|
| Offset | grows |
| Blur radius | grows (about 2x the offset: Hobday rule 16) |
| Opacity per layer | falls |
| Number of layers | grows |
| Surface lightness (dark theme) | grows |
| Optional | element scales up very slightly when lifted (drag) |

Map elevation to meaning (Refactoring UI, "Use shadows to convey elevation"):

| Level | Use | Feel |
|---|---|---|
| 0 | page, content | flat, no shadow |
| 1 | cards, inputs, buttons | small and sharp |
| 2 | dropdowns, popovers, hovering or dragged items | medium |
| 3 | modals, dialogs, command palettes | large and soft, needs full attention |

- A row that gains a shadow when grabbed looks draggable. A button that loses its shadow when pressed looks pushed in.
- Define 3 to 5 elevation tokens and nothing else.

## 4. Shadow recipes (with values)

**Two part shadow** (Refactoring UI): a large soft shadow for ambient light plus a small tight darker shadow for the contact area. The tight one matters most when the element is close to the surface. Vercel: "Use at least two shadow layers."

Starting tokens built on that rule (tune per brand):

```css
--shadow-1: 0 1px 2px rgb(0 0 0 / .06), 0 1px 3px rgb(0 0 0 / .10);
--shadow-2: 0 2px 4px rgb(0 0 0 / .06), 0 4px 12px rgb(0 0 0 / .10);
--shadow-3: 0 8px 16px rgb(0 0 0 / .08), 0 24px 48px rgb(0 0 0 / .16);
```

**Layered smooth shadow** (Tobias Ahlin, adopted by Comeau): stack layers whose offset and blur double each time. More layers, lower alpha each.

```css
/* 5 layers, alpha 0.075 each (Comeau) or 0.12 (Ahlin baseline) */
box-shadow:
  0 1px 1px   rgb(0 0 0 / .075),
  0 2px 2px   rgb(0 0 0 / .075),
  0 4px 4px   rgb(0 0 0 / .075),
  0 8px 8px   rgb(0 0 0 / .075),
  0 16px 16px rgb(0 0 0 / .075);
```

Variants from Ahlin:

- **Sharp:** decreasing alpha 0.25, 0.20, 0.15, 0.10, 0.05 on 1, 2, 4, 8, 16px.
- **Diffuse:** increasing alpha 0.08, 0.12, 0.16, 0.20 on 1, 2, 4, 8px.
- **Dreamy:** alpha 0.07 with blur at 2x the offset (offsets 1 to 32, blur 2 to 64).
- **Short:** decouple blur from offset (`0 6px 8px`, `0 8px 16px` on the last layers) for a shadow that stays close.

**Comeau's elevation set on a coloured background** (`--shadow-color: 220deg 60% 50%`):

```css
--shadow-low:  0.5px 1px 1px hsl(var(--shadow-color) / .7);
--shadow-mid:  1px 2px 2px hsl(var(--shadow-color) / .333),
               2px 4px 4px hsl(var(--shadow-color) / .333),
               3px 6px 6px hsl(var(--shadow-color) / .333);
--shadow-high: 1px 2px 2px hsl(var(--shadow-color) / .2),
               2px 4px 4px hsl(var(--shadow-color) / .2),
               4px 8px 8px hsl(var(--shadow-color) / .2),
               8px 16px 16px hsl(var(--shadow-color) / .2),
               16px 32px 32px hsl(var(--shadow-color) / .2);
```

Performance: layered shadows cost more to paint; do not animate them. To animate elevation, crossfade a pseudo element that holds the larger shadow (animate its `opacity`).

## 5. Shadow colour

- **Never pure transparent black on a coloured background:** it desaturates and looks grey and dirty (Comeau).
- **Match the background hue,** lower the lightness, keep some saturation. On `hsl(220 100% 80%)`: black at 0.5 is too grey, `hsl(220 100% 50%)` glows, `hsl(220 60% 50%)` is right (Comeau).
- **Tint borders, shadows and even text toward the background hue** (Vercel).
- **Keep shadow contrast as low as possible;** structure and shadows should not shout (Hobday rule 3).
- Store the shadow colour as a variable on the surface so a section with a different background updates every shadow inside it.

## 6. Borders that work with shadows

- **Combine a semi transparent border with the shadow** (Vercel). The border defines the edge on light backgrounds where a soft shadow alone looks blurry; the shadow adds lift.
  ```css
  .card { border: 1px solid rgb(0 0 0 / .06); box-shadow: var(--shadow-1); }
  .dark .card { border-color: rgb(255 255 255 / .08); }
  ```
- **On dark themes a border often replaces the shadow.** A lighter 1px edge reads clearly; a dark shadow on a dark page does not.
- **Border contrast rule:** darker than both sides on light themes, lighter than both on dark themes (Hobday rule 7).
- **Inner image border:** a 1px inset border at low alpha (`box-shadow: inset 0 0 0 1px rgb(0 0 0 / .06)`) keeps photos from bleeding into the page (Refactoring UI).
- **Focus rings as `box-shadow`** so they follow the radius (Rauno).

## 7. Depth without shadows (flat and dark themes)

- **Shadows barely work on dark backgrounds** and usually draw more attention than they deserve (Hobday rule 26). In dark themes, show elevation by **lighter surface colour**: page `L 8%`, card `L 12%`, popover `L 16%`, modal `L 20%` (rough HSL lightness steps, keep the hue).
- **Container brightness close to the background:** within about 12% HSB brightness in dark UI and about 7% in light UI (Hobday rule 18, from his review of about 100 well designed sites). A card that jumps far from the page looks heavy.
- **Flat depth** (Refactoring UI): lighter shade of a hue reads raised, darker reads recessed; or a short vertical shadow with no blur (`0 2px 0`) for a crisp, flat but tactile look.
- **Overlap to create layers:** a card that straddles two background sections, an avatar that overlaps the card edge (Refactoring UI).
- **Inset for wells:** inputs and sunken areas can use a subtle inner shadow `inset 0 1px 2px rgb(0 0 0 / .06)`.

## 8. Colour of surfaces and neutrals

- **Near-black and near-white, not #000 and #fff** for large surfaces (Hobday rule 1; Refactoring UI: "Avoid true black").
- **Saturate the neutrals slightly toward the brand hue,** under 5% saturation (Hobday rule 2). Pick warm or cool, never both (rule 10).
- **Greys do not have to be grey** (Refactoring UI): a cool UI tints greys blue, a warm one toward yellow or orange; raise saturation in the lightest and darkest greys to keep the temperature consistent.
- **Use a perceptual colour space** to build scales. Stripe moved to CIELAB so every hue has the same lightness curve; Linear moved themes to LCH and now generates a full theme from three inputs (base colour, accent colour, contrast) instead of 98 variables.
- **Stripe's contrast trick:** with a uniform lightness curve, any two levels 5 apart are safe for small text, 4 apart for icons and large text.
- **Palette colours need distinct brightness,** not only distinct hue, so they stop competing (Hobday rule 9).
- **Dark mode:** lighten text and neutral icons slightly more than you think; Linear did this in its redesign for readability.
- **Accessible is not the same as vibrant** (Stripe): passing contrast does not guarantee a colour still looks like the brand. Check both.

## 9. Glass, blur and translucency

From Apple *Meet Liquid Glass* and *Get to Know the New Design System* (2025), translated for any platform.

**Where glass belongs**

- **Only the navigation and control layer** that floats above content: toolbars, tab bars, sidebars, floating buttons, menus.
- **Never in the content layer.** A glass table or glass cards compete with the controls and muddy the hierarchy.
- **Never glass on glass.** Elements placed on glass use fills, transparency and vibrancy, not another glass surface. Never stack light translucent surfaces: legibility collapses.
- **Avoid content and glass intersecting in a resting state;** reposition content so it does not sit half under a bar at launch.

**How glass behaves**

- It adapts continuously to what is behind it: shadow opacity rises over text and falls over plain light backgrounds; tint and dynamic range shift for legibility.
- **Small elements** (bars, glyphs) can flip between light and dark with the content behind; **large elements** (menus, sidebars) adapt but do not flip, because the change would be distracting.
- **Bigger surfaces read thicker:** deeper shadow, stronger lensing, softer scattering.
- **Two variants, never mixed:** Regular (default, adaptive, works anywhere) and Clear (more transparent, needs a dimming layer). Use Clear only over media rich content, when dimming does not hurt it, and when the content on the glass is bold and bright.
- **Tint sparingly:** tint the one primary action; "when every element is tinted, nothing stands out". Put colour in the content layer instead.
- **Glass appears by bending light, not by fading.** On the web: animate blur radius and scale together with opacity.
- **Modality:** a task that interrupts the flow pairs the glass with a dimming scrim; a parallel task uses separation without a scrim.
- **Scroll edge effects** replace hard dividers where content scrolls under a bar: soft fade (default, touch) or hard (more opaque, for dense desktop UIs and pinned table headers). One edge effect per view.

**Web recipe**

```css
.toolbar {
  background: rgb(255 255 255 / .6);
  backdrop-filter: blur(20px) saturate(180%);
  border-top: 1px solid rgb(255 255 255 / .4);   /* light catching the edge */
}
@media (prefers-reduced-transparency: reduce) {
  .toolbar { background: rgb(255 255 255 / .96); backdrop-filter: none; }
}
@media (prefers-contrast: more) {
  .toolbar { background: #fff; border: 1px solid #000; }
}
```

- Text on glass: slightly heavier weight and higher contrast than on solid surfaces (vibrancy). Thin grey text on glass fails.
- Large blur values are slow (Rauno); keep blur moderate and avoid animating it over big areas.
- Provide the reduced transparency and increased contrast fallbacks every time.

## 10. Layering, overlap and focus

From Rauno Freiberg, *Designing Depth*, which borrows from film composition:

- **Blur or dim the backdrop when an overlay opens,** like a camera's depth of field; it also tells the user only the overlay is interactive.
- **Blur the inner background to push it back** on the Z axis.
- **Fade a container's bottom edge** so its boundary feels open rather than boxed.
- **Offset layers** (a second frame slightly behind the primary one, an out of focus object behind) create depth in marketing visuals.
- **Keep interactive layers sharp:** the iOS Dock slides away without fading so you know it can return.
- **Choreograph layers:** blur the back layer before the front layer appears, so they never collide visually.
- **Stacked sheets:** progressively dim and push back each parent layer (Apple).

## 11. Texture, gradients and finish

- **Vignelli on finish:** shiny surfaces reflect light, matte surfaces absorb it; polished reads opulent, matte reads restrained. Choose the finish that matches the content's character.
- **Subtle background decoration** is allowed when it has a job: a slight colour shift, a gentle gradient, a pattern along one edge (Refactoring UI, "Decorate your backgrounds").
- **Gradients: two close hues** (rule of thumb, not from one source). Hues 30 degrees or less apart look natural; far hues turn muddy in the middle unless you interpolate in OKLCH (`linear-gradient(in oklch, ...)`).
- **Banding:** large soft gradients band on 8 bit screens; add a little noise, or use a radial gradient instead of blurring a solid shape (Rauno, Vercel).
- **Pair complex with simple:** simple foreground on a complex background, or complex foreground on a simple one, never complex on complex (Hobday rule 17).
- **Glow is not depth.** A coloured outer glow on a card reads as a 2010s effect; use it only as deliberate novelty.

## 12. Checklist

- [ ] One light direction and one depth technique across the product
- [ ] 3 to 5 elevation tokens; each level mapped to a meaning
- [ ] Every shadow has 2+ layers, a vertical offset, blur about 2x offset
- [ ] Shadows and borders tinted toward the surface hue, never grey black on colour
- [ ] Semi transparent borders that contrast with both sides; one hard divide per boundary
- [ ] Dark theme shows elevation with lighter surfaces, not heavy shadows
- [ ] No #000 or #fff large surfaces; neutrals warm or cool, not both
- [ ] Glass only on the floating control layer, never on content, never stacked
- [ ] Reduced transparency and increased contrast fallbacks exist
- [ ] Overlays dim or blur what is behind; backgrounds never compete with the foreground

## 13. Sources

`../sources/books/apple-wwdc-design-talks.md`, `refactoring-ui.md`, `anthony-hobday-safe-rules.md`, `shadows-comeau-ahlin.md`, `rauno-freiberg-craft.md`, `vercel-web-interface-guidelines.md`, `linear-and-stripe-writeups.md`, `vignelli-canon.md`, `resilient-web-design.md`, `emil-kowalski-design-engineering.md`.
