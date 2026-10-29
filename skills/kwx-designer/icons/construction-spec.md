# Construction spec: the house rules for drawing icons

Use the project's own icon spec when it has one (look for an icon guide, a design tokens file, or the existing icons' root element). When it has none, use this house spec, then adjust it to the project's typeface and brand with section 7. Write the final spec into the project (section 12) before drawing the second icon.

The house spec is Lucide compatible on purpose: Lucide is the most common base pack, the user's own shell is built on it, and a hybrid set only works when custom icons cannot be told apart from the pack's.

## Contents

1. The house spec at a glance
2. Canvas, live area and keyshapes
3. Stroke, caps and joins
4. Corner radii
5. Gaps, counters and detail
6. Angles, curves and the pixel grid
7. Deriving the spec from the typeface and brand
8. Perspective and optical balance
9. States: outline, filled, badges
10. Sizes, small masters and fractional scale
11. Comparison of real systems
12. The spec block to write into a project

---

## 1. The house spec at a glance

| Rule | Value | How `icon_check.py` tests it |
|---|---|---|
| Canvas | `viewBox="0 0 24 24"`, `width="24" height="24"` | root lint |
| Live area | ink inside pixels 2..21 (2 unit padding); round shapes may overshoot by 1 | ink box at 24 px |
| Stroke | 2 units, centred, one width for the whole set | root lint, children may not set stroke |
| Caps and joins | round and round | root lint |
| Corner radius | 2 on shapes 8+ units across, 1 on smaller shapes, 2.41 where diagonals meet at a right angle; never round where 3+ lines meet | read the code |
| Gap | 2 units of empty space between separate parts and inside counters | `parts` and `holes` at 48 vs 16 px |
| Angles | 0, 90 and 45 degrees (45 means equal integer dx and dy) | `soft` edges, `partial` |
| Coordinates | whole units for the 2 stroke; at most 3 decimals anywhere | lint grid warnings, `soft` |
| Elements | `rect` (with `rx`), `circle`, `ellipse`, `line`, `polyline`, `polygon`, `path` | lint |
| Colour | `stroke="currentColor"` on the root; children carry geometry only; a child may set `fill="currentColor"` for solid parts | lint |
| Perspective | front facing and flat | read the code |
| States | outline at rest, filled twin with the same silhouette when selected | contact sheet |
| Master size | 24; ships at 16, 20, 24, 32, 48 | renders at 16, 20, 24, 48 |

The fixed root element, identical on every icon:

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
```

## 2. Canvas, live area and keyshapes

- Draw every master on a 24 unit square canvas.
- Keep ink inside the 20 unit live area: pixels 2 to 21 at 24 px. With a 2 unit centred stroke, that means geometry (the path centreline) stays between 3 and 21.
- Round shapes (circles, arcs, round caps at the extreme) may overshoot to pixel 1 or 22, because a circle looks smaller than a square of the same width. Nothing straight may overshoot.
- Size every icon against one of four keyshapes. They are maxima, not sizes every icon must fill. Paste them into the contact sheet as reference icons:

| Keyshape | SVG geometry (centreline) | Ink size |
|---|---|---|
| Circle | `<circle cx="12" cy="12" r="10"/>` | 22 (overshoot) |
| Square | `<rect x="3" y="3" width="18" height="18" rx="2"/>` | 20 |
| Portrait | `<rect x="5" y="3" width="14" height="18" rx="2"/>` | 16 by 20 |
| Landscape | `<rect x="3" y="5" width="18" height="14" rx="2"/>` | 20 by 16 |

These are Material's keylines (circle 20, square 18, portrait 16 by 20, landscape 20 by 16) plus 2 units, which is what Lucide ships: its square spans 3 to 21 and its circle has r 10. Material's own numbers fit a set that wants more air. Keep the ratio either way: the circle is 2 units larger than the square.

## 3. Stroke, caps and joins

- One stroke width for every element of every icon. Never mix 2 and 1.5 inside a set (Lucide: "never mixed"; Noun Project names small stroke variation as the classic fault).
- Set the stroke once on the root. A child that sets `stroke-width` is a lint error.
- Strokes are centred on their path (SVG cannot do inside or outside strokes).
- House caps and joins are round. Switch to `stroke-linecap="square"` with `stroke-linejoin="miter"` only through section 7 (a brand with hard, precise terminals and sharp UI corners, as Uber and Atlassian chose).
- Open paths end in caps; closed shapes end with `Z` so the join, not two caps, closes them.

## 4. Corner radii

- Rect corners: `rx="2"` on shapes 8 units or more across, `rx="1"` on smaller ones (Lucide). A rect without `rx` is a lint warning.
- Path corners: draw them as arcs, `A2 2 0 0 1 ...`, with the same radii.
- Where two diagonals meet at a right angle, use a 2.41 radius (1 plus the square root of 2) so the corner looks as round as a 2 radius on a square corner.
- Do not round a corner where three or more lines meet.
- Even sharp looking corners get a small radius; the round join already softens them by 1 unit.
- The alternative rule (Material, Carbon): 2 on outer silhouette corners, square inner corners. Pick one rule per set and apply it everywhere.
- The radius language follows the UI's (section 7): sharp UI, radius 1; default UI, radius 2; very round UI, radius 3 on large shapes.

## 5. Gaps, counters and detail

- Separate parts keep 2 units of empty space between their ink. Test: a 2 unit circle must fit in every gap and every inner counter.
- The arithmetic on centrelines: **gap = centreline distance minus stroke width**. Two parallel 2 unit lines need centrelines 4 units apart. A line inside a rect needs its centreline 4 units from the rect's centreline.
- Where one part crosses another, cut a 2 unit gap in the back part instead of overlapping strokes (the calendar outline stops short of the check badge in `examples/calendar-check.svg`).
- A gap of 2 units at 24 px is 1.33 px at 16 px and may close. `icon_check.py` warns when the count of `parts` or `holes` drops from 48 to 16 px.
- Detail: the fewest elements that still read. Aim for 2 to 6 elements; the script warns above 12. One metaphor per icon, two at most (Windows guideline).
- Too little detail is also a failure: a phone drawn as a plain rounded rect could be a frame or an e-reader; it needs its one telling detail (Hicks).

## 6. Angles, curves and the pixel grid

- Straight lines run at 0, 90 or 45 degrees. A 45 degree segment has equal whole number dx and dy, such as `15 18 17 20` or `17 20 21 16`. Other angles only when the metaphor needs them, with whole number endpoints. (IBM allows multiples of 15; a strict "45 only" rule was not found in any primary source, so it is a house choice for crispness.)
- A 45 degree line looks heavier than a horizontal one at the same stroke (Hicks), and a diagonal bar looks longer than a vertical one of the same length. Make diagonal bars shorter.
- Curves: prefer arcs (`A`) and quadratic curves (`Q`) to cubic Beziers (`C`). Put arc centres and radii on whole units. Use `C` only when needed, with control points on the tangent lines.
- **Pixel grid, the rule that decides crispness:** a 2 unit stroke on whole unit coordinates covers whole pixels at 24 px. The same line moved to x 11.5 smears into three half grey pixels (measured: alpha `0 0 255 255 0 0` against `0 128 255 128 0 0`).
  - Even stroke (2): whole units for lines, rect edges, circle centres.
  - Odd stroke (1 or 3): half units (x 11.5) for lines and rect edges.
  - Stroke 1.5: neither works; align the outer edge to the grid and accept a soft inner edge (Octicons, Polaris).
- A point that must look sharp (an arrow tip, a bookmark notch) needs a true centre pixel: give the shape an odd width so the tip lands in the middle of a pixel (Hicks's 5 unit bookmark, not 4).

## 7. Deriving the spec from the typeface and brand

Icons and text are "two expressions of one visual alphabet" (Uber). Derive four values from the project.

### 7.1 Stroke from the text stem

1. Find the body font, its weight and the size of the text that sits next to icons (the label size, often 14 to 16 px).
2. Measure the stem of a lowercase `l` at that size with ImageMagick:

```bash
FONT=$(fc-match -f '%{file}' "Open Runde:style=Regular")
magick -background none -fill black -font "$FONT" -pointsize 16 -density 72 label:l \
  -trim +repage -alpha extract -gravity center -crop 0x1+0+0 +repage -format "%[fx:mean*w]\n" info:
```

   The number printed is the stem width in pixels. Measured on this machine: Open Runde Regular 1.17 px at 14 px and 1.34 px at 16 px; SF Pro Text Regular 1.18 px and 1.36 px. GitLab's estimate for regular system sans fonts is about 1.5 px at 16 px.
3. Convert to canvas units for the size the icon is shown at: **stroke units = stem px times 24 divided by icon px**.
4. Icons are sparser than text, so let the on-screen icon stroke land between 1.0 and 1.3 times the stem (a house rule, not sourced). Round to 2, 1.75 or 1.5 units, preferring 2 for grid crispness.

Worked: Open Runde 16 px body, icons shown at 20 px. 1.34 times 24 / 20 = 1.61 units. The house 2 units gives 1.67 px on screen, 1.24 times the stem: keep 2. The same icons shown at 24 px next to 16 px text would be 2 px on screen, 1.49 times the stem: too heavy, so show them at 20 px or draw at 1.75.

If the UI body text is Medium or Semibold, measure that weight. If the UI scales fonts by one factor (the user's `UiScale.scale`), icon size must scale by the same factor so the ratio holds.

### 7.2 Size and alignment from the line

- Show icons a few pixels larger than the text they label: 20 px icons with 14 to 16 px text is the common pairing (Ant Design, React Magma; Hicks: "just a few pixels larger").
- Centre the icon on the middle of the text's cap height, not on the line box. Check one icon next to a capital letter in the contact sheet or a render of the real component.

### 7.3 Caps, joins and radii from the brand

| UI corner language | Typeface terminals | Icon caps and joins | Icon radius |
|---|---|---|---|
| Sharp (radii 0 to 4 px) | Hard, geometric, precise (a grotesk with flat cuts used tight) | square caps, miter joins (Uber, Atlassian ends) | 1, or square inner corners (Material rule) |
| Default (radii 6 to 12 px) | Neutral sans (Inter, SF Pro) | round and round (house) | 2 (house) |
| Very round (radii 16+ px, pills) | Rounded fonts (Open Runde, SF Pro Rounded, Nunito) | round and round | 2, and 3 on large shapes (the Iris glyphs in `~/.local/share/lucide/custom/` use 2 to 3) |

### 7.4 Dark mode weight

Light icons on dark backgrounds look heavier (a type design effect; no icon source gives a number). Material Symbols handles it with a grade axis (GRAD -25 on dark). With SVG, either accept it or override on the web with CSS, which beats the presentation attribute: `[data-theme="dark"] .icon { stroke-width: 1.85; }`. The override costs grid crispness, so use it only when the contact sheet shows the dark row visibly heavier.

## 8. Perspective and optical balance

- Front facing and flat. No tilt, no isometric view, no 3D. Below 32 px perspective only adds blur and shrinks the shape (Hicks).
- Depth only when the object is unrecognisable without it (an inbox tray, the top of a cylinder): keep the front flat and extend only the back edge.
- Optical size: the square is the smallest shape, the circle overshoots it by 2 units, irregular shapes (star, heart, organic forms) may use the full live area, a cross sits between (Hicks; Material keylines).
- Optical weight: a dense icon looks darker. Compare `coverage` in the script output: the reference circle and square cover about 22 and 24% at 24 px; across 250 Lucide icons the median was 26.5% (10th percentile 16%, 90th 34.5%). An outline icon far outside 16 to 35% needs a second look.
- Centring: symmetric icons are geometrically centred (equal empty pixels left and right, top and bottom, within 1). Asymmetric ones are centred by eye: shift toward the lighter side until the mass looks centred (a play triangle moves right by about 1 unit).

## 9. States: outline, filled, badges

- **Outline at rest, filled for selected or active** (SF Symbols tab bars, Fluent, Polaris). Use the filled twin for the selected tab or the "on" toggle, never for decoration.
- The filled twin keeps the outline's silhouette exactly: same outer path, now with `fill="currentColor"` on that child, stroke still on, so the edge and the size do not change.
- Inner details become knock-outs: cut holes in the filled shape with a second subpath and `fill-rule="evenodd"`. The stroke also draws around the hole and eats 1 unit on each side, so **draw the hole 2 units wider and taller than the visible gap you want**. A 2 by 4 visible keyhole is a 4 by 6 hole: see `examples/lock-filled.svg` (`M10 13V19H14V13Z`). A hole drawn at the visible size disappears completely; `icon_check.py` shows it as a solid block in the ASCII preview and fewer `holes`.
- The selected state must differ by more than colour or tone. Uber's grey to black selected state was invisible on a black brand; fill plus colour survives.
- **Badges** (plus, minus, check, x, dot, slash) carry a modifier. Put them bottom right, where most bases have empty space; top right would hide a document's corner (Hicks). Give every badge in the set the same size and place, inside the 8 by 8 square from 14 to 22 (Lucide: consistent size and placement). Cut the base outline 2 units around the badge's ink. Let the badge break the base silhouette; that draws the eye to the added meaning.
- A diagonal slash (mute, off, hidden) runs from top left to bottom right at 45 degrees, with a 2 unit gap cut in the base on each side of it, and must not hide the base's identifying part.

## 10. Sizes, small masters and fractional scale

- The 24 master is crisp at 24 and 48 px on a 1x screen and at every size on 2x and 3x screens.
- At 16 and 20 px a 24 master can never be crisp: the scale (0.667, 0.833) puts every edge on a fraction. Measured: 16% partial pixels at 24 px, 67% at 16 px, 71% at 20 px. The `soft` count at 16 and 20 px is expected; only the canvas size is judged.
- If the product must look sharp at 16 px on 1x screens (dense desktop tools), draw a separate 16 master, as Octicons, Fluent and Spotify do: `--canvas 16 --padding 1 --stroke 1.5`, outer edges on whole pixels, fewer details. Do not let code scale icons to arbitrary sizes (Atlassian removed the size prop after it distorted stroke and padding).
- Fractional UI scale breaks snapping at every size: at the user's `UiScale.scale` 1.1 a 24 px icon renders at 26.4 px and anti-aliases however carefully it was drawn. Prefer sizes that land on whole pixels after scaling, and accept soft edges where they cannot.
- `vector-effect="non-scaling-stroke"` keeps the stroke a fixed screen width at every size. Use it only for non-uniformly stretched shapes, never as a substitute for a small master.

## 11. Comparison of real systems

| System | Canvas | Padding | Stroke | Caps and joins | Corner radius | Minimum gap | States |
|---|---|---|---|---|---|---|---|
| Material Symbols | 24 (dense 20) | 2 | 2, 1.5 optical exceptions; variable `wght` 100 to 700, `opsz` 20 to 48, `GRAD` | not specified | 2 outer, square inner | not specified | `FILL` axis 0 to 1 |
| Lucide | 24 | at least 1 (2 in practice) | 2, never mixed | round, round | 2 on 8+, 1 below, 2.41 diagonals | 2 | outline only |
| Tabler | 24 | 1 | 2, centred | round | not published | not published | outline, some filled |
| Octicons (GitHub) | 16 and 24, drawn separately | not published | 1.5 at both sizes | round | 1 (0.25 on small fills) | 1, 1.5 around modifiers | outline, some filled |
| Atlassian 2025 | 16 (12 downscaled) | not published | 1.5, edges on the grid | rounded forms, square end caps | follows the typeface | not published | outline |
| Uber Base 2026 | not published | not published | 2 | square caps | exaggerated roundness | generous | defined filled and outline pairs |
| Shopify Polaris | 20 | 2 | 1.5 (1.25 for cut-outs) | not published | not published | 1 | filled for semi-permanent selection |
| IBM Carbon | 32, scaled down | 2 | 2, expanded to fills | not applicable | 2 on round objects, square where the object is square; angles in 15 degree steps | not published | monotone |
| Phosphor Regular | 256 units | 32 units (3 px at 24) | 16 units (1.5 px at 24); Thin 8, Light 12, Bold 24 | round | 8 units | not published | Fill and Duotone weights |
| SF Symbols | typographic points, 3 scales on SF cap height | template margins | 9 weights drawn by hand to match SF | per weight | per symbol | per symbol | outline, fill, slash, enclosed variants |
| Fluent 2 | per size files 16, 20, 24, 28, 48 | not published | not published (ships as fills) | not published | not published | not published | Regular for wayfinding, Filled for selection |

Sources: Material 1 and Google Fonts Material Symbols guide; lucide.dev icon design guide; docs.tabler.io design guide; primer.style Octicons guidelines; atlassian.design "Building Atlassian's new icon system"; uber.design "When to evolve a design system"; Polaris "Creating icons"; Carbon v10 and IBM Design Language; raw Phosphor SVGs; Apple HIG SF Symbols and WWDC19 session 206; fluent2.microsoft.design. Full citations in `../sources/reports/Custom icons for premium apps.md`.

## 12. The spec block to write into a project

Write this block into the project's design docs (or `icons/SPEC.md` in the repo) with the measured values filled in, so every later icon and every later agent uses the same numbers:

```text
Icon spec for <product>
canvas: 24 (viewBox 0 0 24 24), live area 2..22, round overshoot 1
stroke: 2 units, centred, round caps, round joins
  derived from: <font> <weight> <size>px, stem <measured> px, icons shown at <size> px
radius: 2 (shapes 8+), 1 (smaller), 2.41 (diagonal right angles)
gap: 2 units; badges bottom right inside 14..22
angles: 0, 90, 45; coordinates whole units, max 3 decimals
states: outline at rest, filled twin (same silhouette, knock-outs 2 units oversize) when selected
sizes: master 24; shipped at <sizes>; separate 16 master: <yes/no>
base pack: <pack and version, or none>; custom icons live in <path>, named <convention>
check: python3 ~/.claude/skills/kwx-designer/scripts/icon_check.py --canvas 24 --padding 2 --stroke 2 <files>
```
