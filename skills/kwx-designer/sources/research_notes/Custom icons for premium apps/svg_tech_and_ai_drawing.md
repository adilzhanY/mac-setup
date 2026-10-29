# SVG icon delivery and hand written SVG icons by an AI agent

Scope: delivery formats (SVG vs icon fonts) on web, iOS, Android, React Native and Qt/QML, optimisation and theming, and a concrete method an AI agent can follow to write SVG icon code by hand and verify it without a screen. Research done 2026-10-27 with WebSearch and WebFetch, plus one local rasterisation experiment (resvg 0.48.1, ImageMagick 7.1.2) to confirm the verification method works.

## 1. SVG vs icon fonts: rendering, accessibility, failure modes, performance

### Takeaway
On the web, SVG wins on every axis that matters for a premium product: crisper rendering, no font override or blocking failures, no flash while a font loads, multicolour and per part control, and clean accessible markup. GitHub (2016), Filament Group and CSS-Tricks all moved to SVG for these reasons. Performance is a wash when SVGs are optimised, and badly optimised inline SVG is the one case that gets slow.

### Cited Findings
Rendering and anti-aliasing
- GitHub found icon fonts "often looked poor on 1x displays"; in WebKit icons could blur depending on window width, and sub-pixel text anti-aliasing made it worse. SVG renders icons as images, "locking nicely to whole pixel values at any resolution". Firefox still showed pixel rounding errors with SVG, but the font had the same issue. Source: [GitHub Engineering, Delivering Octicons with SVG (2016)](https://github.blog/engineering/architecture-optimization/delivering-octicons-with-svg/)
- Icon fonts are anti-aliased as text and the author found some font icons less sharp than the SVG version; an icon font's box depends on line-height, vertical-align, letter and word spacing and glyph metrics, so positioning is hard, while an SVG box is exactly its own size. Source: [Chris Coyier, Inline SVG vs Icon Fonts, CSS-Tricks (2014)](https://css-tricks.com/icon-fonts-vs-svg/)
- Icon fonts served one 16px glyph at every size at GitHub, because the set had to stay small; with SVG they could ship size appropriate drawings (larger glyphs for blank states and marketing pages). Source: [GitHub Engineering](https://github.blog/engineering/architecture-optimization/delivering-octicons-with-svg/)

Failure modes of icon fonts
- Users who override page fonts (some dyslexic users) saw icon glyphs as empty squares, breaking layout and meaning; "SVGs will display regardless of font overrides". Source: [GitHub Engineering](https://github.blog/engineering/architecture-optimization/delivering-octicons-with-svg/)
- Icon fonts caused a flash of unstyled content while the font downloaded, cached and rendered (the FOIT/FOUT problem); SVG removed it. Source: [GitHub Engineering](https://github.blog/engineering/architecture-optimization/delivering-octicons-with-svg/)
- Font failure causes listed by CSS-Tricks: cross domain loading without CORS headers in Firefox, network or server errors, a Chrome bug swapping in a fallback font, browsers without @font-face, proxy browsers that claim support but lack it, user stylesheets, extensions and ad blockers that block custom fonts, and Private Use Area code points rendering as unexpected emoji. Ad blockers do not affect inline SVG. Source: [CSS-Tricks](https://css-tricks.com/icon-fonts-vs-svg/)
- Filament Group listed mobile browsers without @font-face (Opera Mini, Nokia Xpress, BlackBerry 4 and 5, Android 2.1, Windows Phone 7 to 7.8) and said most icon font methods "don't accommodate screenreaders very well"; Filament itself later recommended SVG over icon fonts. These browser facts are dated (2013 to 2014). Source: [Filament Group, Bulletproof Accessible Icon Fonts](https://www.filamentgroup.com/lab/bulletproof_icon_fonts.html); [a-font-garde repo](https://github.com/zeyuanchen23/a-font-garde)
- An Opera developer article quoted in a talk: "many people with mild dyslexia have a special system font to aid legibility, which breaks icon fonts." Source: [Death to icon fonts, Seren Davies (slides)](https://speakerdeck.com/ninjanails/death-to-icon-fonts-1)
- Icon fonts usually live in a pseudo element on an empty span, giving bad or no semantics; the svg element signals an image. Source: [CSS-Tricks](https://css-tricks.com/icon-fonts-vs-svg/)

Accessibility patterns (Sara Soueidan, tested by Scott O'Hara)
- Preferred icon button pattern: hide the SVG and name the button with text.
  `<button><svg viewBox="0 0 32 32" aria-hidden="true" focusable="false">...</svg><span class="visually-hidden">Menu</span></button>`. Source: [Sara Soueidan, Accessible Icon Buttons](https://sarasoueidan.com/blog/accessible-icon-buttons/)
- Alternatives that also work: a `hidden` span referenced by `aria-labelledby` on the button, or `aria-label="Menu"` on the button (the label must match any visible text, WCAG 2.1). Source: [Sara Soueidan](https://sarasoueidan.com/blog/accessible-icon-buttons/)
- Not recommended for naming a button: `aria-label` on the svg itself, and `role="img"` + `<title id>` + `aria-labelledby` on the svg. Both fail in some browser and screen reader combinations; the role="img" + title pattern is fine for a standalone meaningful image but is not a dependable way to name a button. The label should describe the action, not the picture. Source: [Sara Soueidan](https://sarasoueidan.com/blog/accessible-icon-buttons/)
- `focusable="false"` stops old IE/Edge giving the svg its own tab stop (two tab stops per button). Source: [Sara Soueidan](https://sarasoueidan.com/blog/accessible-icon-buttons/)
- Inline SVG can carry `<title>`, `<desc>` and `aria-labelledby` with fewer failure states than an icon font. Source: [CSS-Tricks](https://css-tricks.com/icon-fonts-vs-svg/)

Performance and delivery technique on the web
- Cloud Four rendered 1,000 icons per technique (Tyler Sticka, 2021-10-28). Average ms, optimised / unoptimised: img + data URI 67.24 / 77.76; inline SVG 74.91 / 191.89; img (external file) 76.35 / 81.87; same document symbol sprite with use 98.61 / 164.85; external sprite 126.04 / 180.51; CSS background + data URI 109.14 / 120.55; CSS mask 148.87 / 153.25 (mask was generally the slowest). External sprites were fastest in Safari but among the slowest in Chrome and Edge. Source: [Cloud Four, SVG Icon Stress Test](https://cloudfour.com/thinks/svg-icon-stress-test/)
- Optimising five icons from roughly 684 B to 1.21 KB down to 245 to 488 B (removing extra groups, masks, attributes) helped inline SVG and sprites most. Recommendation: well optimised icons that need SVG features, use inline SVG; otherwise img with data URIs as escaped XML rather than Base64; optimise regardless. Only client side rendering was measured. Source: [Cloud Four](https://cloudfour.com/thinks/svg-icon-stress-test/)
- GitHub inlines SVG through a server helper (`octicon(:symbol => "alert")`) so `fill` can be themed with CSS and the delivery method can change later in one place. It rejected an external `<use>` sprite (cross domain and security policy problems with its asset pipeline), img/background (cannot recolour), and embedding the full sprite on every page. It measured "no adverse effects on pageload or performance", less jank, and smaller CSS bundles. IE needed explicit width/height, and serving font and SVG together during the migration crashed IE. Source: [GitHub Engineering](https://github.blog/engineering/architecture-optimization/delivering-octicons-with-svg/)
- Reader counterpoints on CSS-Tricks: an icon font is one cacheable file, inline SVG adds bytes and DOM nodes on every page. Source: [CSS-Tricks comments](https://css-tricks.com/icon-fonts-vs-svg/)
- A 2016 Safari bug reloaded the whole external sprite file per use; reported fixed. Source: [Smashing Magazine](https://smashingmagazine.com/2016/05/safari-svg-sprite-bug)

### Inferences
- For a premium web app: inline SVG components (React/Vue/Svelte component per icon, tree shaken) with `currentColor`, `aria-hidden="true"` and `focusable="false"` by default, and the accessible name on the button. Use img + data URI only for large repeated lists where colour does not need to change via CSS.
- CSS mask icons (`mask: url(icon.svg)` + `background-color: currentColor`) give themable colour without inline markup, but they were the slowest technique in the only measurement found, and they cannot do multicolour.
- An icon font ligature (Material Symbols writes the icon name as text, for example `<span>home</span>`) is real text in the DOM, so a screen reader reads "home" aloud unless the element gets `aria-hidden="true"`, and it shows the raw word when the font is blocked. This follows from how ligature fonts work; I did not find a primary test write up of it.

### Gaps
- No 2024 to 2026 benchmark newer than Cloud Four 2021 was found; browser engines have changed since.
- No primary source found that measures screen reader behaviour on ligature icon fonts specifically.

## 2. When icon fonts still make sense (Material Symbols, Qt/QML)

### Takeaway
Fonts still make sense where text shaping is the cheapest way to draw an icon and the font is guaranteed to load: native and desktop toolkits that bundle the font (Qt/QML shells, games, terminals), and Material Symbols when its variable axes (fill, weight, grade, optical size) are actively used. On the open web, subset hard or switch to SVG.

### Cited Findings
- Material Symbols has four variable axes: fill, weight, grade, optical size. Fill and grade are custom axes set via `font-variation-settings`; weight and optical size map automatically. Source: [Google Fonts, Material Symbols guide](https://developers.google.com/fonts/docs/material_symbols)
- Axis ranges reported by a package: FILL 0 to 1, wght 100 to 700, GRAD -25 to 200, opsz 20 to 48. Google's own page gives two different defaults for opsz (48 in one snippet, 24 elsewhere), so check before relying on a default. Source: [Fontsource, Material Symbols](https://fontsource.org/docs/getting-started/material-symbols.md); [Google Fonts guide](https://developers.google.com/fonts/docs/material_symbols)
- Google recommends subsetting to the icons used with the `&icon_names=` query parameter and instancing only the axes used, because the full axis set "increases the payload". Source: [Google Fonts guide](https://developers.google.com/fonts/docs/material_symbols)
- Qt SVG supports the static parts of SVG Tiny 1.2; since 6.7 it also parses masks, symbol, marker, pattern and some filter primitives (feGaussianBlur, feOffset, feMerge, feColorMatrix, feComposite). `clipPath` is not supported. `QSvgRenderer::setOptions(Tiny12FeaturesOnly)` turns the extras off. Source: [Qt docs, SVG extended features](https://doc.qt.io/qt-6/svgextensions.html); [Qt blog, Qt SVG: Not so 1.2 Tiny any more](https://qt.io/blog/qt-svg-not-so-1.2-tiny-any-more)
- Qt 6.8 added `VectorImage` (builds a Qt Quick item scene from an SVG instead of QPainter calls) and the `svgtoqml` tool (tech preview in 6.7). The Qt blog says a plain `Image` is often the right choice for an image shown at a single size. Source: [Qt blog, Vector Graphics in Qt 6.8](https://www.qt.io/blog/vector-graphics-in-qt-6.8)

### Inferences
- In Qt/QML an icon font is cheap and robust because the app ships the font: glyphs get text anti-aliasing, follow `color` like text, scale with the font size token, and need no per icon file. This is why shells like the user's Quickshell setup map Lucide into a font. The trade-off is single colour per glyph and no per part animation.
- For QML SVG: an `Image { source: "x.svg"; sourceSize: Qt.size(w, h) }` rasterises once at the given size (set sourceSize or it rasterises at the SVG's intrinsic size and then scales, which blurs). Recolouring needs a shader/MultiEffect colorization or a font. Avoid clipPath in icon sources for Qt.
- Fonts also make sense for a set that must change weight or fill continuously (Material Symbols axes); doing that with SVG needs multiple drawings or path morphing.

### Gaps
- No official list of SVG features VectorImage/svgtoqml support was found.
- I did not find a measured comparison of font vs SVG rendering cost in Qt Quick.

## 3. Platform delivery: iOS, Android, React Native, Qt

### Takeaway
Each platform wants its own vector container: SF Symbol SVG templates in an Xcode asset catalog (iOS), VectorDrawable XML or Compose ImageVector (Android), react-native-svg components or build time transformed SVGs (React Native), and SVG/Image or a bundled font (Qt). Keep one source of truth in plain 24x24 SVG and generate the rest.

### Cited Findings
iOS (custom SF Symbols)
- Workflow: in the SF Symbols app pick a similar symbol, File > Export Template (Cmd+E) to get an SVG template, replace the artwork in the template, import back, validate with File > Validate Custom Symbols, export, then drag the .svg into the Xcode asset catalog where it becomes a Symbol Image Set used as `Image("name")`. Source: [Apple, Custom SF Symbols overview](https://developer.apple.com/documentation/technologyoverviews/custom-sf-symbols.md); [Apple (CN), Creating custom symbol images](https://developer.apple.com/cn/documentation/xcode/creating_custom_symbol_images_for_your_app); [Blake Crosley, Custom SF Symbols](https://blakecrosley.com/blog/custom-sf-symbols-creation)
- A variable template needs three source drawings (Ultralight, Regular, Black, each at Small scale); SF Symbols interpolates the other weights. Source: [Blake Crosley](https://blakecrosley.com/blog/custom-sf-symbols-creation); [David Katsman, Medium](https://medium.com/@davidkatsman/how-to-create-custom-sf-symbols-d0e0abdb4972)
- Template version mismatch breaks builds: a forum report says Xcode 16.2 could not read Template 6.0 files (it supported 5.0). Source: [Apple forums, via search snippet](https://developer.apple.com/forums/thread/690608)
- Apple's WWDC21 session "Create custom symbols" covers templates, annotation for multicolour and hierarchical rendering. Source: [WWDC21 10250](https://developer.apple.com/wwdc21/10250)
- Glyphs app can author SF Symbols directly. Source: [Glyphs, Creating an SF Symbol](https://glyphsapp.com/learn/creating-an-sf-symbol)

Android
- A VectorDrawable is an XML tree of `path` and `group` elements with `android:viewportWidth/Height` (for example 24.0) and `width/height` in dp (for example 24dp); paths draw in document order; Android Studio's Vector Asset Studio imports SVG. Official support from API 21, with `VectorDrawableCompat` below that, `fillColor`/`strokeColor` need the compat classes below API 24, and `app:srcCompat` is the most foolproof way to use them in Views. `AnimatedVectorDrawable` supports path morphing (Support Library 25.4.0+). Compose is the recommended toolkit and uses `ImageVector`. Source: [Android Developers, Vector drawables overview](https://developer.android.com/develop/ui/views/graphics/vector-drawable-resources)

React Native
- `react-native-svg-transformer` turns .svg files into components at build time; its `replaceAttrValues` option maps a source colour to `currentColor`, which then inherits the `color` prop; it has an Expo specific `babelTransformerPath`. Source: [react-native-svg-transformer docs](https://docsearch.algolia.com/mcp/docs/repo/kristerkari/react-native-svg-transformer)
- An issue reports runtime `currentColor` on a react-native-svg `Path` warns that it "is not a valid color or brush", so resolve it at build time or pass `color` on the root Svg. Source: [react-native-svg issue (Lightrun mirror)](https://lightrun.com/answers/software-mansion-react-native-svg-currentcolor-fill-support)
- A GeekyAnts article reports rendering 500 SVGs at once with react-native-svg took 9 to 10 seconds and moved to expo-image native SVG rendering, which loses dynamic recolouring (source must be a file or Base64 URI). Secondary source, single anecdote. Source: [GeekyAnts](https://geekyants.com/blog/optimizing-svg-rendering-in-react-native-from-react-native-svg-to-expo-image)
- Expo documents `react-native-svg` as its SVG module. Source: [Expo docs, Svg](https://docs.expo.dev/versions/latest/sdk/svg.md)

Qt/QML: see section 2.

### Inferences
- iOS custom symbols are stroke free outlined shapes in the template (the SF Symbols app works with filled outlines and interpolation between weights needs matching point structure across the three sources). So a stroke based 24x24 source must be expanded to outlines (Inkscape "Stroke to Path" or a library like `svg-outline-stroke`) before it goes into a template, and the three weights need compatible paths. I could not fetch Apple's full English page to quote the stroke rule, so treat this as strong inference.
- Android VectorDrawable supports strokes natively (`strokeWidth`, `strokeLineCap`, `strokeLineJoin`), so a Lucide style stroke icon converts directly; tint with `android:tint`/`?attr/colorControlNormal` or Compose `Icon(tint=...)`.
- For a cross platform design system: author in SVG (24 grid, stroke based), generate web components, VectorDrawable/ImageVector, SF Symbol templates (outlined) and an icon font for Qt from that one source.

### Gaps
- Apple's English "Creating custom symbol images" page and exact current template version (Template 7 with SF Symbols 7?) were not confirmed.
- No primary performance numbers for VectorDrawable path complexity limits were found on the fetched page.

## 4. SVGO settings, currentColor theming, stroke vs fill, non-scaling-stroke

### Takeaway
Run SVGO preset-default with the viewBox kept (the v4 default), keep precision at about 3 decimals, never let it inline styles or hard code colours, and theme with `stroke="currentColor"` (stroke icons) or `fill="currentColor"` (solid icons) on the root element. Use `vector-effect="non-scaling-stroke"` only when an icon is stretched non uniformly, never as a substitute for designing at the target size.

### Cited Findings
- SVGO v4: `removeViewBox` is no longer in preset-default, "to preserve scalability"; enable it only explicitly. Source: [SVGO, Migration from v3 to v4](https://svgo.dev/docs/migrations/migration-from-v3-to-v4/)
- MediaWiki's v4 config notes `removeTitle` is now off by default and also disables `cleanupIds` and `removeDesc`; many icon sets (Bootstrap Icons) still set `removeViewBox: false` explicitly, harmless in v4. Source: [MediaWiki SVG coding conventions](https://www.mediawiki.org/wiki/Manual:Coding_conventions/SVG/de); [Bootstrap Icons svgo.config.mjs](https://git.tdem.in/twbs/icons/blob/main/svgo.config.mjs)
- Preset default plugin list. Source: [SVGO, Preset Default](https://svgo.dev/docs/preset-default/)
- Lucide root attributes: `xmlns`, `width="24" height="24" viewBox="0 0 24 24"`, `fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"`; no transforms, filters, fills or explicit stroke colours on children, never `<use>` (ID collisions when inlined); paths tidied to 3 decimal places. Source: [Lucide, Code conventions](https://lucide.dev/contribute/icons/code-conventions)
- GitHub chose inline SVG specifically so colour could be set with CSS `fill`. Source: [GitHub Engineering](https://github.blog/engineering/architecture-optimization/delivering-octicons-with-svg/)
- `vector-effect="non-scaling-stroke"` keeps stroke width constant on screen regardless of transforms (including non uniform scale) and zoom; applies to circle, ellipse, line, path, polygon, polyline, rect, text, use and others; Baseline widely available since July 2020; the other values (non-scaling-size, non-rotation, fixed-position) have no implementations; the CSS property beats the attribute. Source: [MDN, vector-effect](https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Attribute/vector-effect)

### Inferences
- Safe SVGO config for icons (v4): `preset-default` with `floatPrecision: 3`, plus overrides that keep what the design system needs. Things to watch: `convertShapeToPath` (turns circle/rect into paths, fine for shipping, bad for the editable source), `inlineStyles`/`minifyStyles` (fine), `removeUnknownsAndDefaults` (can drop attributes that equal defaults, fine when the root carries the stroke attributes), `cleanupIds` (fine for icons without gradients; turn off if IDs are referenced). Add `removeDimensions` only if the consumer sizes by CSS, and never `removeViewBox`. Keep an unoptimised source folder and optimise into a dist folder.
- Stroke vs fill: stroke icons keep weight editable (one attribute changes the whole set) and convert directly to VectorDrawable, but iOS symbol templates and many font pipelines need outlined fills. Fill icons render identically everywhere and handle filled states (Material "FILL 1"). A system that needs both should design in strokes and outline at build time.
- non-scaling-stroke matters for scaled chart lines or icons drawn with non uniform scale; for a uniformly scaled icon it makes stroke width ignore the icon size (a 2px stroke stays 2 CSS px at 48px), which changes the look against Lucide's proportional stroke. Use deliberately.

### Gaps
- I did not fetch the full SVGO preset-default list to confirm which plugins touch stroke attributes; verify against svgo.dev before freezing a config.

## 5. How an AI agent should write SVG icons by hand

### Takeaway
Write icons the way Lucide specifies them: a 24x24 viewBox, a 2px centred round stroke set once on the root, 1px minimum padding, geometry primitives (circle, rect with rx, line, polyline) before free paths, coordinates on integers (or exact halves when a 1px detail is needed), simple arcs and quadratic curves over cubic Beziers, at least 2px between separate parts, and reuse of base geometry across related icons. These rules keep the drawing in a form an LLM reasons about well (named shapes with a few numbers) instead of long coordinate soup.

### Cited Findings
Design rules (Lucide icon design guide)
- 24x24 square canvas; at least 1px between strokes and canvas edge; 2px strokes, never mixed; round joins and round caps only; centred strokes. Source: [Lucide, Icon design guide](https://lucide.dev/contribute/icon-design-guide)
- Corner radii: 2px for shapes 8px or larger, 1px for shapes under 8px, about 2.41px (1+sqrt 2) where diagonals meet at a right angle; even very sharp corners usually need a small radius; do not round where more than two lines meet. Source: [Lucide](https://lucide.dev/contribute/icon-design-guide)
- Spacing: at least 2px between distinct elements and inside inner gaps (test by fitting a 2px circle); touching elements still need 2px separation, avoid abrupt cuts. Source: [Lucide](https://lucide.dev/contribute/icon-design-guide)
- Optical volume: match the visual weight of the `circle` and `square` icons, compare by blurring; dense areas mean too much detail. Symmetric icons stay geometrically centred; asymmetric ones get optical adjustment. Source: [Lucide](https://lucide.dev/contribute/icon-design-guide)
- Curves: prefer simple arcs and quadratic curves; align cubic control points to avoid bumps; no extra control points. Pixel grid: align coordinates, arc centres and sub elements to the grid; off grid diagonals look blurry and optically wider on low density screens. Source: [Lucide](https://lucide.dev/contribute/icon-design-guide)
- Reuse base icon geometry exactly; keep add on badges (plus, x, check) at a consistent size and place across related icons. Source: [Lucide](https://lucide.dev/contribute/icon-design-guide)
- Allowed elements: path, line, polygon, polyline, circle, ellipse, rect (with rx); only size and position attributes on them; lint with `pnpm run lint:icons`. Source: [Lucide, Code conventions](https://lucide.dev/contribute/icons/code-conventions)

Why primitives first (research)
- Chat2SVG (CVPR 2025): an LLM first writes an SVG template from basic geometric primitives, then an image diffusion model guides refinement. The authors cite earlier findings that LLMs lay out reasonable scenes but "struggle with complex geometric shapes"; the primitive template keeps paths regular. Source: [Chat2SVG, arXiv 2411.16602](https://arxiv.org/html/2411.16602v1); [CVPR 2025](https://openaccess.thecvf.com/content/CVPR2025/html/Wu_Chat2SVG_Vector_Graphics_Generation_with_Large_Language_Models_and_Image_CVPR_2025_paper.html)
- VGBench: LLMs do better on high level vector languages (TikZ, Graphviz) than on low level SVG, which is "a greater challenge"; SGP-Bench shows limits on "complex spatial reasoning or understanding fine-grained details". Source: [Survey, arXiv 2503.04983](https://arxiv.org/html/2503.04983v2)
- Text tokenisation "often leads to inefficiencies when encoding geometric primitives and SVG-specific commands". Source: [Survey, arXiv 2503.04983](https://arxiv.org/html/2503.04983v2)

### Inferences (the method)
A concrete hand drawing procedure for an agent:
1. Name the metaphor in words first (for example "padlock: rounded body rect 18x11 at y=11, shackle as an arc"), then list each part as a primitive with its numbers. Check the plan against a reference set (Lucide's version of the nearest icon) and reuse its base geometry.
2. Fixed root, never varied per icon: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">`. Children carry geometry only.
3. Coordinates: with a 2px stroke, put lines and rect edges on integer coordinates (the stroke then covers whole pixels at 24px, confirmed in section 6). Use .5 coordinates only for an odd width stroke. Keep everything inside 3..21 so the stroke stays within the 2..22 live area (1px canvas padding plus half the stroke, matching Lucide's rule).
4. Element choice: `rect` with `rx="2"` for boxes, `circle` for round parts, `line` for single segments, `polyline` for open bent strokes (chevrons, checks), `path` only for arcs and curves. In paths use absolute M, L/H/V, A (arcs with simple radii) and Q; use C only when needed, with control points on the tangent lines. Close shapes with Z.
5. Separation: keep 2px gaps between parts; where a part crosses another, cut a 2px gap rather than overlapping strokes.
6. Write a short comment per element in the working file (removed by SVGO), for example `<!-- shackle -->`, so later edits target the right element.
7. Iterate with the render checks of section 6, not by eye.

### Gaps
- No published controlled experiment was found comparing "primitives first" prompting vs free paths for a general LLM; the support is indirect (Chat2SVG design, benchmark findings).

## 6. Verifying an icon without looking at a screen

### Takeaway
Rasterise with resvg or rsvg-convert at 16, 20, 24 and 48px, then read the pixels with ImageMagick: ink bounding box (live area check), alpha profiles across a stroke (crispness and stroke width), and the share of partially covered pixels (blur). Combine with an XML lint that checks root attributes, allowed elements, precision and coordinates inside the live area. A local test confirmed the method works and that a 2px stroke on integer coordinates is perfectly crisp at 24px while every stroke is soft at 16 and 20px.

### Cited Findings
- Local experiment (resvg 0.48.1, ImageMagick 7.1.2-32, 2026-10-27, not a published source). Test icon: `rect x=4 y=4 width=16 height=16 rx=2` plus a vertical `line` at x=12, root as in section 5. A copy moved the line to x=11.5.
  - Alpha across row 12 at 24px, pixels x=9..14: integer version `0 0 255 255 0 0` (the 2px stroke covers exactly two pixels); half pixel version `0 128 255 128 0 0` (smeared over three pixels at half opacity).
  - Share of inked pixels that are partial (anti-aliased): integer version 16% at 24px, 67% at 16px, 71% at 20px; half pixel version 25% at 24px. At 16 and 20px the 24 grid maps to fractional pixels (scale 0.667 and 0.833), so no coordinate choice is crisp there.
  - `magick icon-24.png -alpha extract -trim info:-` reported the ink box as `18x18+3+3`, i.e. ink spans pixels 3..20, inside the 2..22 live area; this is a one line padding check.
  - `resvg --query-all icon.svg` prints each element's geometric bounding box by id (`a,4,4,16,16` and `b,12,8,0,8`), which excludes stroke, so add half the stroke width when checking padding.
- Lucide validates icons with `pnpm run lint:icons` (structure) and Prettier formatting. Source: [Lucide, Code conventions](https://lucide.dev/contribute/icons/code-conventions)
- Lucide checks optical density by blurring the icon at its intended size and looking for dark areas. Source: [Lucide, Icon design guide](https://lucide.dev/contribute/icon-design-guide)

### Inferences (check list an agent can automate)
- Commands: `resvg -w 24 -h 24 icon.svg out24.png` (or `rsvg-convert -w 24 -h 24 icon.svg -o out24.png`); `magick out24.png -alpha extract -trim info:-` for the ink box; `magick out24.png -crop 24x1+0+12 -alpha extract -depth 8 txt:-` for a row profile; `magick out24.png -alpha extract -blur 0x1 -format "%[fx:maxima]" info:` style measures for density hot spots. Inkscape CLI (`inkscape --export-type=png -w 24`) and `magick icon.svg` work too but ImageMagick may delegate SVG to its own MSVG renderer or rsvg depending on build, so prefer resvg for deterministic output.
- Automated checks to script (Python with xml.etree, no dependencies):
  - Root has exactly the agreed attributes (viewBox 0 0 24 24, fill none, stroke currentColor, stroke-width 2, round cap and join); children have no stroke, fill, stroke-width, transform, filter, style or id attributes (uniform stroke width is then guaranteed by construction).
  - Only allowed elements; numbers have at most 3 decimals; endpoint coordinates are integers or .5 (flag anything else as off grid); all geometry within 3..21 after adding stroke half width.
  - Path sanity: no zero length segments, no duplicated consecutive points, no `M` without a following draw command (stray nodes), no unclosed shape that should be closed.
  - Raster checks: ink box inside 2..22 at 24px; partial pixel ratio at 24px under a threshold (about 25% for a stroke icon); minimum gap test by eroding the alpha mask with a 2px kernel and checking that separate parts stay separate (connected component count before and after); compare average ink coverage against a reference icon (Lucide `circle`/`square`) to match optical volume.
  - Render at 16px and confirm the icon still has the same number of connected components as at 48px; merged components mean a gap below about 3px that closes at small sizes.
- Visual inspection substitute: dump the 24px alpha as an ASCII grid (`magick out24.png -alpha extract -depth 8 txt:-` reshaped to 24 rows, mapping 0 to "." and 255 to "#"); an LLM can read a 24x24 character grid reliably enough to spot a missing stroke, a merge or an off centre shape.

### Gaps
- No published tool was found that implements the full raster check list above; it would need to be written (about one small Python script).
- Thresholds (25% partial pixels, coverage tolerance) are my own starting values from the local test, not from a source.

## 7. Published research on LLMs drawing SVG, and what improved results

### Takeaway
Plain LLMs can write valid SVG but are weak at precise geometry; results improve with (a) structured primitives first then refinement (Chat2SVG), (b) a render and compare loop used as feedback or reward (RLRF, StarVector's follow up), (c) reasoning models (survey), and (d) training on icon data with compact path tokens (IconShop, StarVector, OmniSVG). Simon Willison's "pelican riding a bicycle" test shows steady model progress but he now says it no longer tracks model quality.

### Cited Findings
- StarVector (CVPR 2025, ServiceNow): combines a code LLM with a vision encoder; introduced SVG-Stack (about 2 million captioned SVGs) and SVG-Bench (10 datasets, tasks Image to SVG, Text to SVG, diagram generation); reports state of the art. Source: [StarVector, arXiv 2312.11556](https://arxiv.org/abs/2312.11556); [StarVector README](https://cdn.jsdelivr.net/gh/joanrod/star-vector@main/README.md)
- IconShop: an autoregressive transformer over SVG path sequences; performs well on simplified icons; used as a Text to SVG baseline in StarVector. Source: [StarVector paper PDF](https://arxiv.org/pdf/2312.11556)
- RLRF (Rendering-Aware Reinforcement Learning, NeurIPS 2025): generates SVG roll outs, renders them, compares to the target image and rewards pixel similarity, semantic alignment and code efficiency; "significantly outperforms supervised fine-tuning", addressing common failure modes. Source: [RLRF, arXiv 2505.20793](https://arxiv.org/abs/2505.20793); [HTML v2](https://arxiv.org/html/2505.20793v2)
- Chat2SVG: LLM writes primitive based templates, diffusion produces image targets, then path level latent optimisation; reports better visual fidelity, path regularity and semantic alignment, and supports natural language editing. Full LLM prompts are in the CVPR supplement. Source: [Chat2SVG, arXiv 2411.16602](https://arxiv.org/html/2411.16602v1); [CVPR supplement](https://openaccess.thecvf.com/content/CVPR2025/supplemental/Wu_Chat2SVG_Vector_Graphics_CVPR_2025_supplemental.pdf)
- OmniSVG (NeurIPS 2025): built on Qwen2.5-VL with an SVG tokenizer; trained on MMSVG including MMSVG-Icon from Iconfont; text to SVG, image to SVG and character reference generation. Source: [OmniSVG, arXiv 2504.06263](https://arxiv.org/html/2504.06263v2); [MMSVG-Icon dataset](https://huggingface.co/datasets/OmniSVG/MMSVG-Icon)
- Survey of LLM SVG work: general LLMs' SVG ability is "inconsistent, especially when dealing with intricate vector compositions"; "reasoning improves performance and scores for SVG tasks" and distilled reasoning models beat same size models; SVGEditBench shows even strong models struggle with edits that need precise syntax; normalised scores (authors' 0 to 1 scale) e.g. gemini-2.5-pro-preview 0.961 VGen, GPT-4.1 0.960, Deepseek-R1 0.957. Claude was not evaluated. The survey did not test chain of thought, render feedback for general LLMs, or primitive prompting. Source: [Survey, arXiv 2503.04983](https://arxiv.org/html/2503.04983v2)
- Simon Willison started the pelican on a bicycle SVG test in October 2024 across 16 models via his LLM CLI and still runs it on new models (for example GLM-5.1, April 2026); he now says the link between pelican performance and model quality "has been mostly severed" and advises against using it to compare models. An OpenEnv environment turns the prompt into a repeatable scorer for training. Source: [Simon Willison, Pelicans on a bicycle (2024)](https://simonwillison.net/2024/Oct/25/pelicans-on-a-bicycle/); [GLM-5.1 post](https://simonwillison.net/2026/Apr/7/glm-51/); [OpenEnv pelican_svg](https://huggingface.co/docs/openenv/environments/pelican_svg)

### Inferences
- The research methods that work map directly onto an agent loop without training: primitives first (Chat2SVG stage 1), render and compare (RLRF's reward, done here with resvg + ImageMagick metrics instead of a learned reward), and spending reasoning on a written geometry plan before emitting code (survey finding on reasoning models).
- Code efficiency is part of RLRF's reward; short SVGs with few elements are both easier for the model to keep consistent and faster to render (Cloud Four), so "fewest elements that read clearly" is a good objective.
- The pelican test rewards whole scene composition, not icon grid discipline; it says little about whether a model can hit a 2px grid, so icon quality needs the automated checks of section 6, not a showcase prompt.

### Gaps
- No published experiment on a general purpose LLM (Claude, GPT) writing grid conformant UI icons with a render feedback loop was found.
- I did not read RLRF's quantitative tables, so no numbers on how much rendering feedback improved scores are given here.
