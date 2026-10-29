# Icon system construction rules: grids, keylines, stroke, optical sizing and pixel snapping

Research date: 2026-10-27. Method: WebSearch and WebFetch only, plus raw SVG files pulled from the Phosphor and Lucide GitHub repositories with curl to measure real values. Several current official pages (m3.material.io, carbondesignsystem.com/elements/icons, ibm.com/design/language, developer.apple.com HIG, polaris.shopify.com) render with JavaScript or redirect and returned no body text, so older static versions or text mirrors were used where noted.

## 1. Grid and live area: canvas, padding and keyline shapes

### Takeaway
The dominant convention is a 24 unit canvas with a 20 unit live area (2 unit padding) and four keylines (Material: circle 20, square 18, portrait 16x20, landscape 20x16). Smaller systems (Octicons, Atlassian, Phosphor, Polaris) draw on 16 or 20 unit grids, and Lucide only requires 1px of padding, not 2.

### Cited Findings
- Material system icons: 24dp canvas, live area 20x20dp with 2dp padding around it; square keyline 18x18dp, circle keyline 20dp diameter, vertical rectangle 20dp high x 16dp wide, horizontal rectangle 16dp high x 20dp wide ([Material Design, System icons](https://material.io/design/iconography/system-icons.html), values as returned by search of that page).
- The older Material 1 page gives the same keylines (square 18x18dp, circle 20dp, vertical 20x16dp HxW, horizontal 16x20dp HxW) but describes the 20dp live area with "4dp padding", which conflicts with 24 minus 20 = 2dp per side; treat 2dp per side as correct ([Material 1, Style Icons](https://m1.material.io/style/icons.html)).
- Material dense layouts: icons may scale down to 20dp, using a 16x16dp live area with 2dp padding ([Material 1, Style Icons](https://m1.material.io/style/icons.html)).
- Material product (launcher) icons: 48dp, drawn on a 48 unit grid at 400% (192x192dp); keylines square 152x152dp, circle 176dp diameter, vertical rectangle 176 high x 128 wide, horizontal 128 high x 176 wide ([Material 1, Style Icons](https://m1.material.io/style/icons.html)).
- Android adaptive icons: 108x108dp layers, 72dp masked section; keylines square 44dp (4dp corner radius), circle 52dp, tall rectangle 52 high x 36 wide, wide rectangle 36 high x 52 wide ([Material 1, Style Icons](https://m1.material.io/style/icons.html)).
- Lucide: icons "must be designed on a 24 x 24-pixel canvas" and "must have at least 1 pixel of padding between their strokes and the edge of the canvas"; no numeric keylines are given, only "Match the visual weight of circle and square", checked by blurring ([Lucide icon design guide](https://lucide.dev/contribute/icon-design-guide)).
- Measured Lucide `house.svg`: `viewBox="0 0 24 24"`, outer path spans x=3 to x=21, so with a 2px stroke the ink reaches x=2 and x=22, i.e. 2px visual padding in practice even though the rule is 1px minimum ([lucide/icons/house.svg](https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/house.svg)).
- Tabler uses 24px grid, 1px padding and a 2px centered stroke ([Tabler icon design guide](https://docs.tabler.io/icons/design-guide)).
- IBM Carbon: "Create a 32px x 32px artboard for each icon", "32 px icons should have 2 px padding", deliver SVG at 32x32 ([Carbon v10, Contribute icons](https://v10.carbondesignsystem.com/guidelines/icons/contribute)).
- Carbon components typically use icons on 16px artboards; 20px, 24px and 32px artboards are also used in UI ([Carbon, Icons usage](https://carbondesignsystem.com/elements/icons/usage/), via search summary).
- Octicons: two drawings per icon, a 16px version on a 16x16 grid and a 24px version on a 24x24 grid; 12px is reserved for when "a 16px icon can't be used"; circle, square and rectangle reference shapes are used on both grids for matching optical volume (numbers for the keylines not published, the page points to Nucleo) ([Primer, Octicons design guidelines](https://primer.style/foundations/icons/design-guidelines)).
- Atlassian (2024 to 2025 refresh): "System icons are drawn within a 16 x 16px bounding box"; 16px is the core size, 12px is downscaled from 16px and "less legible", 24px is legacy only because its extra whitespace caused workarounds ([Atlassian, Building Atlassian's new icon system](https://atlassian.design/whats-new/building-atlassians-new-icon-system); [Atlassian iconography](https://atlassian.design/foundations/iconography)).
- Shopify Polaris: "The icon container is 20 x 20 px. The content of an icon should be confined within a safe space of 16 x 16 px" (2px padding) ([Polaris, Creating icons](https://polaris.shopify.com/design/icons/creating-icons), via search; page now redirects to shopify.dev).
- Phosphor: "Designed at 16 x 16px to read well small and scale up big" ([Phosphor homepage README](https://raw.githubusercontent.com/phosphor-icons/homepage/master/README.md)). The shipped SVGs, however, use `viewBox="0 0 256 256"` (measured, below).
- Measured Phosphor `house.svg` (all weights): viewBox 0 0 256 256, path spans x 40 to 216; with a 16 unit stroke the ink spans 32 to 224, i.e. 32/256 = 1/8 of the canvas padding per side (3px at 24px, 2px at 16px) ([phosphor-icons/core raw/regular/house.svg](https://raw.githubusercontent.com/phosphor-icons/core/main/raw/regular/house.svg)).
- Microsoft Windows app icons are aligned "to a 48x48 grid initially" ([Microsoft Learn, Design guidelines for Windows app icons](https://learn.microsoft.com/en-us/windows/apps/design/style/iconography/app-icon-design)).
- Fluent UI System Icons npm package lists sizes 16/20/24/28/48 with regular and filled styles; "some icons do not have all sizes available yet" ([@fluentui/svg-icons on npm](https://npmjs.com/package/@fluentui/svg-icons), via search). The GitHub repo also names regular, filled, color and light styles, with sizes per icon in `metadata.json` ([microsoft/fluentui-system-icons](https://github.com/microsoft/fluentui-system-icons)).

### Inferences
- A safe default recipe for a 24px set: 24 canvas, 20 live area (2 padding), keylines circle d=20, square 18, portrait 16w x 20h, landscape 20w x 16h. This is the Material set and is effectively what Lucide and Feather ship (ink at 2 to 22).
- Keylines scale proportionally: Material product keylines (152/176/128 on 192) are the 24 unit numbers times 8 (18x8=144 is not 152, so product keylines are NOT a pure scale of system keylines; do not assume they are).
- Phosphor's 256 grid with 32 unit padding equals a 24px canvas with 3px padding, so Phosphor glyphs read slightly smaller than Lucide or Material at the same nominal size.

### Gaps
- Current m3.material.io, carbondesignsystem.com/elements/icons/design and ibm.com/design/language iconography pages are client rendered and returned no text, so Carbon keyline dimensions and Carbon 16/20/24 padding values could not be quoted from a primary source.
- Fluent 2 iconography page publishes no grid, padding or keyline numbers ([Fluent 2 iconography](https://fluent2.microsoft.design/iconography)).
- No published Phosphor or Atlassian keyline sizes were found.

## 2. Stroke: weights per size, caps and joins, scaling

### Takeaway
Stroke systems split into two camps: 2px on 24 (Material, Lucide, Feather, Tabler, legacy Atlassian) and 1.5px on 16 or 20 (Octicons at both 16 and 24, Atlassian new, Polaris). Round caps and joins dominate outline sets; Atlassian deliberately uses square end caps. Pixel-critical systems (Carbon) expand strokes to fills and forbid centered strokes.

### Cited Findings
- Material: stroke 2dp "for all instances, including curves, angles, and interior and exterior strokes"; optical exceptions such as a complex paperclip using 1.5dp inside the 2dp area and a small microphone with a 1.5dp stroke ([Material 1, Style Icons](https://m1.material.io/style/icons.html)).
- Lucide: "Strokes must be 2 pixels wide" (no mixing), "Open paths must use round line caps", "Strokes must use round line joins", "Strokes must be centered on their paths" ([Lucide icon design guide](https://lucide.dev/contribute/icon-design-guide)). Measured house.svg confirms `stroke-width="2" stroke-linecap="round" stroke-linejoin="round"` ([lucide house.svg](https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/house.svg)).
- Octicons: "a consistent stroke width of 1.5px for both 16px and 24px icons"; round caps and joins ([Primer, Octicons design guidelines](https://primer.style/foundations/icons/design-guidelines)).
- Atlassian: legacy "2px stroke on a 24px canvas", new "1.5px stroke on a 16px canvas" chosen to match the stroke of standard UI text; the chosen "balanced" style has "rounded features and square end caps" ([Atlassian, Building Atlassian's new icon system](https://atlassian.design/whats-new/building-atlassians-new-icon-system)).
- Atlassian 12px icons are downscaled from 16px, reducing both size and stroke; the team found that shrinking legacy icons with a size prop "distorted stroke width and spacing" ([Atlassian, Building Atlassian's new icon system](https://atlassian.design/whats-new/building-atlassians-new-icon-system)).
- Polaris: "Stroke weight is 1.5 px, but is reduced to 1.25 px when used inside a shape as a cut-out" ([Polaris, Creating icons](https://polaris.shopify.com/design/icons/creating-icons), via search).
- Carbon: "All strokes must be expanded and at full pixel values"; "Never use center borders. Centering can cause half pixels"; "Avoid using the line tool; use the rectangle tool instead"; shapes combined with Unite ([Carbon v10, Contribute icons](https://v10.carbondesignsystem.com/guidelines/icons/contribute)).
- Phosphor, measured from raw SVGs on a 256 grid: Thin stroke-width 8, Light 12, Regular 16, Bold 24, all with round caps and round joins ([Phosphor core raw thin](https://raw.githubusercontent.com/phosphor-icons/core/main/raw/thin/house-thin.svg), [light](https://raw.githubusercontent.com/phosphor-icons/core/main/raw/light/house-light.svg), [regular](https://raw.githubusercontent.com/phosphor-icons/core/main/raw/regular/house.svg), [bold](https://raw.githubusercontent.com/phosphor-icons/core/main/raw/bold/house-bold.svg)). Phosphor also ships Fill and Duotone weights; duotone is described as the stroke colour plus the same colour at 20% opacity for fills ([Phosphor guide, allsvgicons](https://allsvgicons.com/blog/phosphor-icons-complete-guide/), secondary source).
- Material Symbols variable font axes: Fill `FILL` 0..1 (default 0), Weight `wght` 100..700 (default 400), Grade `GRAD` -50..200 (default 0), Optical size `opsz` 20..48; optical size "automatically adjust[s] the stroke weight" as size changes ([Google Fonts, Material Symbols guide](https://developers.google.com/fonts/docs/material_symbols)). That page states the default opsz as 48 in one place and 24 in another, an internal inconsistency.

### Inferences
- Converted to pixels at 24px display: Phosphor Thin 0.75px, Light 1.125px, Regular 1.5px, Bold 2.25px. Phosphor Regular is therefore Octicons/Polaris weight, not Lucide weight.
- As a ratio of canvas: Lucide 2/24 = 8.3%; Octicons 1.5/16 = 9.4% at 16 but 1.5/24 = 6.25% at 24 (stroke held constant in px, not scaled); Phosphor Regular 16/256 = 6.25%. Octicons deliberately keeps a constant absolute stroke across sizes so 16 and 24 icons sit next to the same text weight, which is the "non scaling stroke" approach; Lucide and Phosphor scale the stroke with the canvas (SVG `stroke-width` scales with the viewBox unless `vector-effect="non-scaling-stroke"` is set, which is an SVG platform fact, not from these guides).
- Material Symbols opsz is the variable-font version of "thinner stroke at larger size": at opsz 48 strokes are relatively thinner than at opsz 20, so a 48px icon does not look heavy.

### Gaps
- No primary source gave Fluent System Icons stroke widths per size (Fluent SVGs ship as outlined fills, so stroke cannot be read from the file). Commonly repeated values (1px at 16/20, 1.5px at 24 and up) were not verified and should be treated as unconfirmed.
- No primary Carbon stroke weight was found; a secondary gallery page claims 1px/2px by size but could not be verified.

## 3. Corner radii, angles, gaps, minimum detail, optical balance and centering

### Takeaway
Corner radius rules converge on "about one stroke width": Material 2dp outer and square inner, Lucide 2px (1px under 8px shapes, 2.41px for 45 degree diagonals), Octicons 1px, Windows 48 grid 2px outer and 1px inner. Minimum gaps are 2px on 2px-stroke sets (Lucide) and 1px on 1.5px sets (Octicons, Polaris).

### Cited Findings
- Material: exterior silhouette corners 2dp radius; "Strokes 2dp wide or less are not rounded"; interior corners are square ([Material 1, Style Icons](https://m1.material.io/style/icons.html)).
- Lucide: right-angle corners on shapes at least 8px wide or tall get 2px radius; shapes smaller than 8px get 1px; "Diagonal lines that meet at a right angle usually need a 2.41 pixel radius (1+sqrt 2)"; "Even very sharp corners usually need a small amount of rounding"; "Don't round corners where more than two lines meet" ([Lucide icon design guide](https://lucide.dev/contribute/icon-design-guide)).
- Lucide spacing: "Distinct elements must have at least 2 pixels of visual spacing between them"; "Most inner gaps should be at least 2 pixels wide", tested by fitting a 2px-wide circle inside ([Lucide icon design guide](https://lucide.dev/contribute/icon-design-guide)).
- Lucide curves: prefer simple arcs and quadratic curves; align cubic control points to avoid bumps; avoid extra control points ([Lucide icon design guide](https://lucide.dev/contribute/icon-design-guide)).
- Lucide balance: "Icons should look centered and balanced within the canvas"; "Symmetrical icons should remain geometrically centered"; same level of detail across the set, checked with a blur test at intended size ([Lucide icon design guide](https://lucide.dev/contribute/icon-design-guide)).
- Octicons: 1px corner radius unless a different radius helps recognition; 0.25px radius for small filled elements like arrowheads; 1px gap to separate overlapping objects; 1.5px gap around modifiers such as lines and arrows; line arrowheads by default, filled arrowheads when there is no room ([Primer, Octicons design guidelines](https://primer.style/foundations/icons/design-guidelines)).
- Polaris: "The minimum gap between strokes should never be less than 1px"; optical adjustments allowed in 0.25px increments ([Polaris, Creating icons](https://polaris.shopify.com/design/icons/creating-icons), via search).
- Windows app icons: "When rounded corners are applied to an exterior curve, use a 2px radius at 48x48. When rounded corners are applied to an interior curve, use a 1px radius instead"; use "as few shapes with as few corners as possible"; avoid extremes of thick and thin shapes ([Microsoft Learn, Windows app icon design](https://learn.microsoft.com/en-us/windows/apps/design/style/iconography/app-icon-design)).
- Fluent 2 UI shape radii (components, not icon artwork): 4px default, 2px for shapes smaller than 32px, 8px and 12px for large components ([Fluent 2, Shapes](https://fluent2.microsoft.design/shapes)).
- Atlassian: rounded corners and curves chosen "to align with our typography" ([Atlassian, Building Atlassian's new icon system](https://atlassian.design/whats-new/building-atlassians-new-icon-system)).
- Measured Phosphor house: corner arcs use radius 8 on the 256 grid (`a8,8`), i.e. half the 16 unit stroke ([Phosphor house.svg](https://raw.githubusercontent.com/phosphor-icons/core/main/raw/regular/house.svg)). Measured Lucide house: inner door corners radius 1, outer body corners radius 2 ([lucide house.svg](https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/house.svg)).

### Inferences
- Optical balance (circle bigger than square) is encoded in the Material keylines: circle diameter 20 against square side 18, so a circle is drawn about 11% wider than a square to look the same size; portrait and landscape rectangles give up 4 units in one axis.
- A centered stroke radius equal to the stroke width (Lucide 2 on 2) gives an inner radius of 1 and an outer of 3; Material's "do not round strokes 2dp or less" plus square inner corners is the sharper alternative. Pick one and apply it everywhere.
- The Lucide 2.41 value is the radius at which a 45 degree corner's rounding visually matches a 2px radius on a 90 degree corner.

### Gaps
- No primary source in this pass states an explicit "45 degree only" angle rule for system icons; Material 1 does not state one (the WebFetch extract confirmed it is absent). Lucide only says to align diagonals to the pixel grid. A 45 degree rule is commonly taught but was not sourced here.
- No numeric overshoot value (for example "circles extend 1px past the square") was found from a primary source beyond the keyline sizes; Nucleo's guide (referenced by Octicons) returned 404.

## 4. Pixel snapping and hinting at 16, 20, 24px; when to draw separate sizes

### Takeaway
Every system that cares about crispness snaps geometry to integer coordinates. Odd-width strokes centered on a path need half-pixel coordinates, which is why Carbon bans centered strokes and Polaris aligns one side of its 1.5px stroke to the grid. Systems that target 16px either draw a separate 16 master (Octicons, Atlassian core) or derive small sizes from it, rather than shrinking a 24.

### Cited Findings
- Material: position icons "on pixel", X and Y coordinates integers; width equals height ([Material 1, Style Icons](https://m1.material.io/style/icons.html)).
- Carbon: "Icons should be at whole pixels. No decimals are allowed in x and y coordinates or width and height fields"; artboard and artwork "must be aligned to the pixel grid"; set tools to "snap to pixels and round values to whole pixels"; beware automatic alignments that create half pixels ([Carbon v10, Contribute icons](https://v10.carbondesignsystem.com/guidelines/icons/contribute)).
- Lucide: "Align coordinates, arc centers, and other geometric elements to the pixel grid when possible", align subelements, "try to align every diagonal line to the pixel grid" ([Lucide icon design guide](https://lucide.dev/contribute/icon-design-guide)).
- Octicons: align the outer edges of shapes to pixel boundaries when possible, do not align inner edges ([Primer, Octicons design guidelines](https://primer.style/foundations/icons/design-guidelines)).
- Polaris: "Shapes must align with the pixel grid"; exceptions for optical adjustments in 0.25px increments; "Since the stroke has half a pixel, one side of the stroke should always be aligned with the pixel grid" ([Polaris, Creating icons](https://polaris.shopify.com/design/icons/creating-icons), via search).
- Atlassian: stroke edges align to the pixel grid for crispness on lower-resolution displays ([Atlassian, Building Atlassian's new icon system](https://atlassian.design/whats-new/building-atlassians-new-icon-system)).
- Why off-grid lines blur: a 1px line straddling a pixel boundary covers two pixels by half each and renders as two 50% grey lines; fix is +0.5 offset for a 1px stroke, no offset for fills ([WHATWG list, Blurry lines in 2D Canvas and SVG, 2013](https://lists.whatwg.org/pipermail/whatwg-whatwg.org/2013-July/082515.html)). Rule of thumb from the same discussion and an Inkscape forum: no stroke or even-width strokes snap to whole pixels, odd-width strokes snap to half pixels; under any scale transform the stroke width also scales and snapping breaks ([Inkscape forum thread](https://alpha.inkscape.org/vectors/www.inkscapeforum.com/viewtopice6ca-2.html?t=10636)). These are older sources; the geometry still holds.
- Separate drawings: Octicons designs a 16px and a 24px version of each icon ([Primer](https://primer.style/foundations/icons/design-guidelines)). Fluent ships per-size files (16/20/24/28/48 in the npm package) ([@fluentui/svg-icons](https://npmjs.com/package/@fluentui/svg-icons)). Fluent product icons simplify below 48px and should be used at specific sizes "instead of scaling them"; above 48 scale by factors of 4 (48, 64, 96...) ([Fluent 2 iconography](https://fluent2.microsoft.design/iconography)). Fluent: 12px icons are "generally too small for interactions" ([Fluent 2 iconography](https://fluent2.microsoft.design/iconography)).
- Windows picks an exact size first, else the next size up and scales down; minimum set 16, 24, 32, 48 and 256 so it "should only ever scale your icon down, never up"; at 125% scale a 16px slot becomes 20px, at 150% 24px, at 200% 32px ([Microsoft Learn, Construct your Windows app's icon](https://learn.microsoft.com/en-us/windows/apps/design/style/iconography/app-icon-construction)).

### Inferences
- With Lucide's 2px stroke on integer path coordinates, each stroke edge falls on a whole pixel at 24px (1px each side of the path), so 24px renders crisp. At 16px the same SVG scales by 2/3, the stroke becomes 1.33px and edges fall off-grid; this is the concrete reason dedicated 16px masters exist.
- A 1.5px stroke can never have both edges on whole pixels; the Polaris and Octicons answer is to snap the outer edge only and accept a soft inner edge.
- On a fractionally scaled desktop (for example UiScale 1.1), every px value is multiplied, so pixel snapping at design time is only preserved at integer scale factors; at 1.1 a 24px icon is 26.4px and will antialias regardless.

### Gaps
- Carbon's per-size redraw rules (whether 16 and 20 are redrawn or scaled from 32) were not available from a retrievable primary page.
- A current Bjango pixel fitting article (a well-known reference) returned 404 at the guessed URL.

## 5. Weights and scales: SF Symbols and variable icon fonts

### Takeaway
SF Symbols ties icon weight to text weight: 9 weights matched to San Francisco and 3 scales defined against SF cap height, so a symbol set at the same point size and weight as adjacent text matches it. Material Symbols exposes the same idea as variable axes (wght 100 to 700, opsz 20 to 48, GRAD -50 to 200, FILL 0 to 1).

### Cited Findings
- SF Symbols: "Each of the nine symbol weights, from ultralight to black," corresponds to a San Francisco weight; three scales small, medium (default) and large; "The scales are defined relative to the cap height of the San Francisco system font"; changing scale changes emphasis without breaking weight matching at the same point size ([Apple HIG SF Symbols, text mirror apple-hig-mcp](https://unpkg.com/apple-hig-mcp@1.1.3/content/sf-symbols.md)). Apple's SF Symbols 5 page also states nine weights and three scales and automatic alignment with text ([Apple, SF Symbols](https://developer-mdn.apple.com/sf-symbols/), via search).
- SF Symbols rendering modes: monochrome, hierarchical (one colour, opacity by layer), palette (two or more colours), multicolor; variable color for changing values, "don't use it to communicate depth" ([apple-hig-mcp mirror](https://unpkg.com/apple-hig-mcp@1.1.3/content/sf-symbols.md)).
- Custom SF symbols: start from an exported template of a similar symbol; match system symbols in detail, optical weight, alignment, position and perspective; negative side margins allowed for optical alignment, named like "left-margin-Regular-M"; do not bake enclosures or badges into a custom symbol ([apple-hig-mcp mirror](https://unpkg.com/apple-hig-mcp@1.1.3/content/sf-symbols.md)).
- Material Symbols axes and guidance: low grade (for example -25) to reduce glare of light icons on dark backgrounds; high grade (for example 200) for emphasis; match the icon grade to the text font grade; FILL 0 to 1 for state change and animation ([Google Fonts, Material Symbols guide](https://developers.google.com/fonts/docs/material_symbols)). The examples also show a `ROND` axis 0..100 not described in the axis list ([same](https://developers.google.com/fonts/docs/material_symbols)).
- Atlassian chose a 1.5px stroke on 16px so the icon matches "the stroke of standard UI text" ([Atlassian](https://atlassian.design/whats-new/building-atlassians-new-icon-system)); Phosphor's six weights (Thin, Light, Regular, Bold, Fill, Duotone) are meant to pair with text weight ([UAE design system iconography](https://designsystem.gov.ae/guidelines/iconography), secondary).

### Inferences
- The nine SF weight names are those of the SF font (Ultralight, Thin, Light, Regular, Medium, Semibold, Bold, Heavy, Black); the mirror did not list them, so this comes from the font family, not the quoted page.
- Grade differs from weight: grade changes stroke thickness without changing glyph width or metrics, which is why it is recommended for dark mode compensation (light on dark looks heavier).
- For a custom set, the portable rule is: icon stroke at body size roughly equals the text stem width of the paired font weight (Atlassian 1.5px at 16px against UI text).

### Gaps
- WWDC "Introducing SF Symbols" (2019) and "Create custom symbols" transcripts were not retrieved; the commonly cited rule that custom symbol templates need three masters (Ultralight, Regular, Black at small scale) with the rest interpolated is unverified here.
- No numeric mapping of Material Symbols wght values to stroke widths in px was found.

## 6. States: outline vs filled, duotone, selected

### Takeaway
Outline is the resting state and fill is the selected or emphasized state across Apple, Microsoft, Shopify and Google; duotone and hierarchical rendering add a second tone through opacity, not a second hue.

### Cited Findings
- SF Symbols: outline "works well in toolbars, lists, and other places where you display a symbol alongside text"; fill adds emphasis for selection states, iOS tab bars and swipe actions; an iOS tab bar prefers fill and a toolbar takes outline automatically; enclosed (circle, square) variants aid small-size legibility; slash variants mean unavailable ([apple-hig-mcp mirror](https://unpkg.com/apple-hig-mcp@1.1.3/content/sf-symbols.md)).
- Fluent 2: Regular is "primarily as a wayfinding device"; Filled is "for highlighting selected states or for smaller moments" that need weight; modifiers always use the filled theme and sit bottom right; one colour per icon, system icons solid colours only ([Fluent 2 iconography](https://fluent2.microsoft.design/iconography)).
- Polaris: "Use filled icons for semi-permanent selected states, like pinning an app"; one colour, no transparency ([Polaris, Creating icons](https://polaris.shopify.com/design/icons/creating-icons), via search).
- Material Symbols: FILL axis 0 (outline) to 1 (filled) for state change, animatable ([Google Fonts, Material Symbols guide](https://developers.google.com/fonts/docs/material_symbols)).
- Material legacy opacity states: light background active 54% black, inactive 38%; dark background active 100% white, inactive 50% ([Material 1, Style Icons](https://m1.material.io/style/icons.html)).
- Phosphor Duotone: stroke at full colour plus fills at 20% opacity of the same colour ([allsvgicons Phosphor guide](https://allsvgicons.com/blog/phosphor-icons-complete-guide/), secondary).

### Inferences
- A filled variant must keep the same silhouette and keyline as its outline twin so the state change reads as a fill, not a swap; Material Symbols' FILL axis and Fluent's paired regular/filled files both enforce this by construction.

### Gaps
- No published rules were found for how interior details (for example the lines inside a document) are reversed out in the filled state, such as a minimum knock-out gap. Polaris' 1.25px cut-out stroke is the only number found.

## 7. Metaphor, perspective and family coherence

### Takeaway
Flat, front-facing views are the default everywhere; depth is allowed only when an object is unrecognizable without it. Metaphors are literal and icons are named for what they show, and consistency is checked by matching detail level and optical weight across the set.

### Cited Findings
- Material: icons "should be front-facing. Do not tilt, rotate, or make them appear dimensional"; product icons must never be skewed, rotated, bowed, warped or bent ([Material 1, Style Icons](https://m1.material.io/style/icons.html)).
- Octicons: 2D perspective unless depth makes the icon more recognizable ([Primer](https://primer.style/foundations/icons/design-guidelines)).
- Windows: "straight-on perspective" by default; exceptions are when the metaphor does not read without another side (a cylinder seen straight on is a rectangle, so its top may be added) or the app is about 3D; layers stay flat and perpendicular to the view; no more than two metaphors per icon, one is better; avoid letters; add literal detail only to the most prominent layer; drop shadows and gradients defined at 48x48, default gradient angle 120 degrees ([Microsoft Learn, Windows app icon design](https://learn.microsoft.com/en-us/windows/apps/design/style/iconography/app-icon-design)).
- Fluent 2: system icons are "literal metaphors" named for the object, not the function ("Shield, not security") ([Fluent 2 iconography](https://fluent2.microsoft.design/iconography)).
- Atlassian: single-purpose icons are named for their concept ("Work item"), multi-purpose icons are "named by what they look like" ("arrow right", "globe"); before contributing, check for a near-duplicate and avoid confusion with another product concept ([Atlassian](https://atlassian.design/whats-new/building-atlassians-new-icon-system); [Atlassian iconography](https://atlassian.design/foundations/iconography)).
- Lucide: similar level of detail across the set, verified by blurring at intended size; match visual weight to the `circle` and `square` icons ([Lucide icon design guide](https://lucide.dev/contribute/icon-design-guide)).
- SF Symbols custom symbols must match system symbols in detail, optical weight, alignment, position and perspective ([apple-hig-mcp mirror](https://unpkg.com/apple-hig-mcp@1.1.3/content/sf-symbols.md)).
- Polaris: consistent visual style, stroke weight and only one colour ([Polaris, Creating icons](https://polaris.shopify.com/design/icons/creating-icons), via search).

### Inferences
- A practical coherence checklist for an agent: same canvas and padding, same stroke width and caps/joins, same corner radius rule, same minimum gap, same keyline fit (the blurred icon should match the blurred reference circle and square), front view only, one metaphor, named by what it shows.

### Gaps
- No published numeric limit on detail (for example a maximum number of strokes or elements per icon) was found in any system.
