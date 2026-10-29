# Delivering icons: formats per platform

One source of truth: the plain 24 unit stroke SVG masters described in `construction-spec.md`, kept unoptimised in the repo. Every platform format is generated from them. Never hand-edit a generated file; fix the master and regenerate.

## Contents

1. Format per platform
2. Web: inline SVG components and accessible icon buttons
3. SVGO settings
4. `currentColor` and theming
5. React Native
6. iOS: custom SF Symbols or template images
7. Android: VectorDrawable and Compose
8. Qt/QML
9. Final checks after export

---

## 1. Format per platform

| Platform | Ship as | Why |
|---|---|---|
| Web (React, Vue, Svelte, plain HTML) | Inline SVG, one component per icon, tree shaken | Crisp, themable with CSS, no font failure modes, clean semantics |
| Web, very long repeated lists (1,000+ icons on one page) | `<img>` with an SVG data URI (escaped XML, not Base64) | Fastest in Cloud Four's 1,000 icon test (67 ms against 75 ms inline optimised), but cannot be recoloured by CSS |
| Web, Material Symbols with animated axes (fill, weight) | The variable font, subset with `&icon_names=` | The only case where a web icon font earns its cost |
| React Native and Expo | `react-native-svg` components (via `react-native-svg-transformer`) | Native vector, recolourable |
| iOS, iPadOS, macOS (native) | SF Symbols for shared verbs; custom symbols from an SF template for nouns | Weight and scale match SF text, Dynamic Type, Bold Text |
| Android (Views or Compose) | VectorDrawable XML (`res/drawable/ic_*.xml`) | Strokes are native, tint follows the theme |
| Qt/QML shell or app that bundles its own font | An icon font built from the SVGs (the user's shell does this), or SVG through `Image` | The font gets text anti-aliasing, follows `color`, scales with the font size token |

Avoid icon fonts on the web. GitHub dropped its Octicons font in 2016 because it blurred on 1x screens and in WebKit depending on window width, users who override page fonts (some dyslexic users) saw empty squares, and the icons flashed in late while the font loaded. Ad blockers, CORS failures and Private Use Area code points rendering as emoji add to it (CSS-Tricks). A ligature font such as Material Symbols writes the icon name as real text, so a screen reader reads "home" aloud unless the element is `aria-hidden="true"`.

## 2. Web: inline SVG components and accessible icon buttons

**The component.** One component per icon, the root attributes from the master, hidden from assistive tech by default:

```tsx
// src/icons/Lock.tsx (generated from icons/lock.svg)
import type { SVGProps } from "react";

export function LockIcon({ size = 20, ...props }: SVGProps<SVGSVGElement> & { size?: number }) {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg" width={size} height={size} viewBox="0 0 24 24"
      fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round"
      aria-hidden="true" focusable="false" {...props}
    >
      <rect x="4" y="11" width="16" height="10" rx="2" />
      <path d="M8 11V7A4 4 0 0 1 16 7V11" />
      <line x1="12" y1="15" x2="12" y2="17" />
    </svg>
  );
}
```

Generate these with SVGR rather than by hand: `npx @svgr/cli --typescript --out-dir src/icons icons/` (it runs SVGO; point it at the config in section 3 with `--svgo-config`). Only offer the sizes the spec ships (16, 20, 24); an arbitrary size prop is how Atlassian's icons got distorted.

**The icon button**, the pattern Sara Soueidan recommends and Scott O'Hara tested across browser and screen reader pairs: hide the graphic, name the button with text that describes the action, not the picture.

```html
<button type="button" class="icon-button">
  <svg aria-hidden="true" focusable="false" ...>...</svg>
  <span class="visually-hidden">Lock note</span>
</button>
```

or, equally valid, `aria-label` on the button itself:

```html
<button type="button" class="icon-button" aria-label="Lock note">
  <svg aria-hidden="true" focusable="false" ...>...</svg>
</button>
```

```css
.visually-hidden {
  position: absolute; width: 1px; height: 1px; margin: -1px; padding: 0;
  overflow: hidden; clip-path: inset(50%); white-space: nowrap; border: 0;
}
.icon-button { inline-size: 44px; block-size: 44px; display: inline-grid; place-items: center; }
```

Rules:

- Do not name a button with `aria-label` on the `<svg>`, or with `role="img"` plus `<title>` on the svg: both fail in some browser and screen reader pairs. `role="img"` with a `<title>` is fine only for a standalone meaningful image that is not a control.
- `focusable="false"` stops old Edge and IE giving the svg its own tab stop.
- A visible label next to the icon is still the default (NN/g). Then the icon stays `aria-hidden` and the text names the control.
- Icon only controls get a tooltip on hover and focus, and the accessible name matches the tooltip text.
- Hit target at least 44 by 44 CSS px for touch (24 by 24 is the WCAG 2.2 minimum, 2.5.8), however small the glyph.
- Use a sprite with `<use href="#lock">` only for a same document sprite. External sprites were among the slowest in Chrome and Edge, and `<use>` inside the icon masters themselves is banned (ID collisions when inlined).
- CSS mask icons (`mask: url(lock.svg)` with `background-color: currentColor`) were the slowest technique measured (149 ms per 1,000) and cannot do more than one colour. Avoid them.

## 3. SVGO settings

SVGO v4 is safe by default for icons: `removeViewBox` left `preset-default` "to preserve scalability". Keep the masters unoptimised in `icons/` and optimise into `dist/icons/`:

```js
// svgo.config.mjs (SVGO 4)
export default {
  multipass: true,
  floatPrecision: 3,
  plugins: [
    'preset-default',
    { name: 'removeAttrs', params: { attrs: ['class', 'data-.*'] } },
  ],
};
```

```bash
npx -y svgo@4 --config svgo.config.mjs -f icons -o dist/icons
python3 ~/.claude/skills/kwx-designer/scripts/icon_check.py dist/icons/*.svg --no-ascii
```

Verified on the worked examples with SVGO 4.1.0: it merges each icon's elements into one path with relative commands (the lock becomes `<rect .../><path d="M8 11V7a4 4 0 0 1 8 0v4m-4 4v2"/>`), keeps the root attributes and `viewBox`, and every output still passes `icon_check.py`. That merged, relative form is why the masters stay unoptimised: they are the editable source.

Never enable `removeViewBox`. Add `removeDimensions` only if every consumer sizes icons by CSS. Optimised output is for shipping; run the checker on it to prove the optimiser broke nothing.

## 4. `currentColor` and theming

- The master's root carries `stroke="currentColor"` (and children use `fill="currentColor"` for solid parts). The icon takes the CSS `color` of its parent, so text and icon change colour together on hover, disabled, dark mode and selection.
- Never hard-code a colour in an icon file. Colour belongs to the component that uses the icon (`.icon-button { color: var(--text-secondary); }`).
- Selected state: swap to the `-filled` twin and change colour; never change colour alone (`construction-spec.md` section 9).
- Opacity for a disabled state goes on the control, not inside the SVG.
- Dark mode weight compensation, if needed at all, is a CSS override of `stroke-width` on the root (`construction-spec.md` section 7.4).

## 5. React Native

- Install `react-native-svg` (Expo documents it as its SVG module) and `react-native-svg-transformer`, which turns `.svg` imports into components at build time. Its README has a separate `babelTransformerPath` for Expo.
- Colour: pass `color` on the root (`<LockIcon color={theme.text} width={20} height={20} />`) so `currentColor` resolves from it. If `currentColor` warns ("is not a valid color or brush" was reported on a `Path`), replace it at build time in `.svgrrc`: `{ "replaceAttrValues": { "currentColor": "{props.color}" } }`.
- Accessibility: the pressable carries the name, the icon is hidden.

```tsx
<Pressable accessibilityRole="button" accessibilityLabel="Lock note" hitSlop={12}
  style={{ minWidth: 44, minHeight: 44, alignItems: "center", justifyContent: "center" }}>
  <LockIcon color={colors.text} width={20} height={20}
    accessibilityElementsHidden importantForAccessibility="no-hide-descendants" />
</Pressable>
```

- Touch targets: 44 by 44 pt on iOS, 48 by 48 dp on Android.
- Very long lists: rendering hundreds of `react-native-svg` components at once was reported slow (500 icons in 9 to 10 s, a single anecdote from GeekyAnts). For long lists use `expo-image` with the SVG file (loses dynamic recolouring) or memoise rows.

## 6. iOS: custom SF Symbols or template images

**Preferred: custom SF Symbols** for product nouns, so they match SF text weight and scale and support Dynamic Type and Bold Text.

1. In the SF Symbols app, select the system symbol closest to your icon and choose File > Export Template. Apple's own advice is to start from a similar symbol.
2. SF templates work with **filled outlines, not strokes**. Expand the stroke master to outlines first (Inkscape: Path > Stroke to Path, or a build step such as `svg-outline-stroke`), then place the outlines on the template's guides (baseline, cap height, margins).
3. A variable template needs three source drawings, Ultralight, Regular and Black, at Small scale, with compatible paths; the app interpolates the other weights. At minimum supply Regular at Medium scale and a Bold variant for Bold Text.
4. File > Validate Custom Symbols, export, and drag the `.svg` into the Xcode asset catalog, where it becomes a Symbol Image Set. Use it as `Image("deck")` in SwiftUI or `UIImage(named: "deck")`.
5. Check the template version against your Xcode: a forum report shows Xcode 16.2 rejecting Template 6.0 files.
6. Do not bake enclosures or badges into a custom symbol; use the component library variants. Test every custom symbol under each animation preset you use, because layered paths can move unexpectedly.

**Simpler fallback: a template image.** Add the SVG to the asset catalog, check Preserve Vector Data, set Render As to Template Image, and tint with `.foregroundStyle(...)`. It recolours but does not follow SF weights or Dynamic Type, so size it explicitly next to the text.

Accessibility: `Image("deck").accessibilityLabel("Deck")` on meaningful icons; `.accessibilityHidden(true)` when a text label is next to it. In a `Button`, label the button.

## 7. Android: VectorDrawable and Compose

VectorDrawable keeps strokes natively, so the stroke master converts directly. It supports only `<path>` (and `<group>`), so every `rect`, `circle` and `line` becomes path data. Android Studio's Vector Asset Studio imports an SVG and does this; for a hand conversion, rewrite each primitive as a path. The worked lock:

```xml
<!-- res/drawable/ic_lock.xml -->
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="24dp" android:height="24dp"
    android:viewportWidth="24" android:viewportHeight="24"
    android:tint="?attr/colorControlNormal">
  <path
      android:pathData="M6,11H18A2,2 0 0,1 20,13V19A2,2 0 0,1 18,21H6A2,2 0 0,1 4,19V13A2,2 0 0,1 6,11Z"
      android:fillColor="@android:color/transparent"
      android:strokeColor="@android:color/white" android:strokeWidth="2"
      android:strokeLineCap="round" android:strokeLineJoin="round"/>
  <path
      android:pathData="M8,11V7A4,4 0 0,1 16,7V11M12,15V17"
      android:fillColor="@android:color/transparent"
      android:strokeColor="@android:color/white" android:strokeWidth="2"
      android:strokeLineCap="round" android:strokeLineJoin="round"/>
</vector>
```

- The white stroke is a mask colour: `android:tint` recolours it to the theme. VectorDrawable is supported from API 21 (`VectorDrawableCompat` below), and `app:srcCompat` is the most reliable way to use it in Views.
- Compose: `Icon(painter = painterResource(R.drawable.ic_lock), contentDescription = "Lock note")`; it tints with `LocalContentColor` by default. Pass `contentDescription = null` when a text label sits next to it. Put the click on an `IconButton`, which gives the 48 dp target.
- The pathData above was not compiled here (no Android toolchain in this session); open it in Android Studio's preview once before shipping.

## 8. Qt/QML

Two routes, both used on this machine.

**An icon font (the user's shell).** `~/.local/share/lucide/build-font.py` builds Lucide plus the custom `custom/iris-*.svg` glyphs into `LucideShell-Regular.otf` (2.0 px) and `LucideShell-Bold.otf` (2.5 px, for selected or filled icons). QML asks for a glyph by name: `MaterialSymbol { text: "iris_deck" }`. To add one: draw it to spec, run `icon_check.py` on it, save it as `custom/iris-<name>.svg`, add `"iris_<name>": "iris-<name>"` to `aliases.json` and `manual-map.json`, rebuild and install with `install` (never `cp` over an open font), and restart the shell (Ctrl+Super+R). Sizes come from the shell's font tokens (`Appearance.font.pixelSize.*`), never a literal number. Trade-off: one colour per glyph, no per part animation.

**SVG through `Image`.** Set `sourceSize` so Qt rasterises at the display size instead of scaling a bitmap:

```qml
Image {
    source: "icons/lock.svg"
    sourceSize: Qt.size(UiScale.px(20), UiScale.px(20))
    width: sourceSize.width; height: sourceSize.height
}
```

- Qt SVG supports static SVG Tiny 1.2, plus masks, symbols, markers, patterns and some filters since 6.7, but **not `clipPath`**. The house spec never uses it.
- Do not count on `currentColor` resolving to a theme colour in Qt's SVG renderer. Recolour the rendered image with `MultiEffect { colorization: 1.0; colorizationColor: ... }`, or prefer the font route for themed glyphs.
- Qt 6.8's `VectorImage` builds a Qt Quick scene from an SVG for icons that must scale live; for an icon shown at one size, a plain `Image` is enough (Qt blog).

## 9. Final checks after export

- [ ] `icon_check.py` passes on the optimised web output, not only on the masters.
- [ ] Every platform file was generated from the masters, and the masters are committed.
- [ ] Every icon button has an accessible name that describes the action; decorative icons are hidden from assistive tech.
- [ ] Touch targets are at least 44 pt or 48 dp, whatever the glyph size.
- [ ] Icons recolour with the theme on light and dark, and the selected twin is wired to the selected state.
- [ ] No icon font on the open web unless its variable axes are animated.
