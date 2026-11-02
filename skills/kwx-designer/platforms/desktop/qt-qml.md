# Qt Quick and Quickshell

The traps a UI agent hits in Qt Quick, and in the user's Quickshell shell in particular. Each section names the mistakes library entry it comes from (`quality/mistakes-library.md`) and a grep or log check. Iris parts, palette and measures are in `~/.config/quickshell/ii/IRIS.md` and `~/.config/quickshell/ii/modules/iris/README.md`; they win over this file.

## Contents

1. Sizing
2. Layouts
3. Text
4. Positioners
5. Room tests
6. Overlays
7. Input masks
8. Ids vs properties
9. File reading
10. Colour animation
11. Names
12. Rendering limits
13. Hot reload
14. Fonts
15. Springs

---

## 1. Sizing

- Fonts only from `Appearance.font.pixelSize.*`; never a literal, never below `pixelSize.smallest`.
- Every other pixel value through `UiScale.px(n)` or a named metric (`UiScale.rowHeight`, `controlSmall`, `fieldHeight`, `chartHeight`, `cardPadding`).
- Do not scale `hyprlandGapsOut`, `barShortenScreenWidthThreshold`, `rounding.full` or `screenRounding`: they match things outside the UI.
- A singleton edit may not apply on hot reload (Appearance's inline QtObject blocks kept old values). Verify with a value you can observe.

Check: `grep -nE 'pixelSize: *[0-9]'` over the changed files is empty; every bare number in a size property (implicitHeight, implicitWidth, preferredWidth, preferredHeight, radius, margins, spacing) is 0, 1, or a listed exception.

## 2. Layouts

- Every custom visual (Canvas, Shape, icon item) declares `implicitWidth` and `implicitHeight`, or a Layout gives it 0 x 0 (KM8).
- In a row, `Layout.fillWidth: true` goes on the label; the siblings get fixed sizes.
- Never size a positioner's child from the positioner's own size. A Row capped by its implicit width around a Text capped by the Row's width never settled: an endless polish loop took a whole CPU core and froze the shell. Use anchors for "text takes the rest".

Check: each custom visual has implicit sizes; `qs log -c ii` shows no "polish() loop" after the change.

## 3. Text

- Labels the product writes: `wrapMode: Text.Wrap` and `elide: Text.ElideNone` (KM3). Elide only user data.
- A measuring twin uses the same component, font, renderType, hinting and width as the drawn Text, or its advances differ (KM11).

Check: `grep -nE 'elide: *Text\.Elide(Right|Left|Middle)'`; each hit is bound to user data.

## 4. Positioners

Column and Row know their implicit sizes only after the next polish, and a hidden Row reports 0. Reading them in the same tick as the content change returns the old size. Wait a frame (two 30 ms ticks) or compute the fixed parts by arithmetic (KM11).

Check: every read of a positioner size that feeds an animation has a frame between the content change and the read.

## 5. Room tests

Compare `screen.width / UiScale.scale`, or use the font token test (`Appearance.font.pixelSize.normal >= 22` means scale 1.25 and up), never raw `screen.width` (KM6).

Check: `grep -n 'screen.width'`; each comparison includes the scale.

## 6. Overlays

A StyledToolTip whose parent has no `hovered` property stays visible for good unless `extraVisibleCondition` is bound (KM9).

Check: for every StyledToolTip, the parent has `hovered` or the tooltip binds `extraVisibleCondition`.

## 7. Input masks

`Region { item: x }` re-reads geometry only when x's own x, y, width or height change. Mask items never sit inside a moving parent; bind `x: stage.x + field.x` on a fixed parent instead (KM16).

Check: for every `Region { item: ... }`, walk the parents to the window; none has an animated or bound x, y or scale.

## 8. Ids vs properties

Never write `history: history` across a Component boundary (sourceComponent, delegate): an outer id loses to the object's own property and binds it to itself (KM17).

Check: `grep -nE '^\s+([A-Za-z]+): \1\s*$'`; each hit has its id inside the same Component, or is renamed.

## 9. File reading

A FileView reused for several files needs `blockAllReads: true`, or one FileView per file. `blockLoading` does not block after a path change, so `text()` returns the previous file (KM13).

Check: grep `blockLoading` next to a `path =` assignment.

## 10. Colour animation

`ColorAnimation` interpolates unpremultiplied colours, so going from opaque to translucent flashes light grey on the way. Keep the base colour static and fade an overlay's `opacity` instead.

Check: no ColorAnimation whose from and to differ in alpha.

## 11. Names

- Never a property called `top` or another FINAL Item property on an Item based component: Qt refuses the whole file.
- Never an inline component named after a QtQuick type or a singleton.
- Use `?.` on `Config.options` in bindings: it goes undefined mid reload.

Check: `grep -nE 'property \w+ (top|left|right|bottom|width|height|x|y)\b'` is empty; `grep -n 'Config.options\.'` hits in bindings use `?.`.

## 12. Rendering limits

- The shell's Canvas ignores `setLineDash`; draw dashes as segments.
- Qt rich text honours only `<font color>` with no alpha; pre-blend translucent colours.

## 13. Hot reload

- A change is live only after a "Reloading configuration" plus "Configuration Loaded" pair later than your last write of every changed file (KM15). `sed -i` or a bare `touch` may not trigger it; rewrite the file with its own content.
- A new inline `component X:` in an already loaded file does not hot reload ("X is not a type"): inline the delegate or say a restart is needed. Anchors, layer and window structure changes also need a restart.
- With parallel agents on the shell, take the shell lock around each save, wait about 3 s, read `qs log -c ii | tail -30` for errors from your file, release.

Check: the log position before the last write, and a new reload pair after it with no errors between.

## 14. Fonts

Install a rebuilt font with `install -m644`, never `cp` over a loaded font, then restart the shell (Ctrl+Super+R) and `koima --daemon` (KM5).

Check: `grep -nE "cp .*fonts|cp .*\.(otf|ttf|woff2?)"` over your commands is empty.

## 15. Springs

`SpringAnimation` uses per tick values; use the calibrated constants in `premium/motion-and-feel.md` "Qt/QML springs", or the project's own (`Iris.snappySpring` and friends).
