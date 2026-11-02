# Mistakes library

Every entry is a UI defect a real user had to point out, or one found the hard way. Read in full before any UI change and check your code against each entry by reading the code and doing the arithmetic (quality/predict-from-code.md). A local library (the project's, or ~/.claude/ui-designer/mistakes.md) is read FIRST and wins on conflict; this file is its generalized, travelling copy.

Numbering: KMn matches the user's local id Mn one to one, so drift can be tracked (`scripts/check_skill.py` warns when a local id has no KM entry). Entries are grouped by layer, not by number.

## Contents

1. Size and fit: KM1, KM3, KM6, KM8
2. Icons and assets: KM2, KM5
3. Colour: KM4
4. Interaction: KM7, KM9, KM14, KM16
5. Motion: KM10, KM11
6. Wiring: KM12, KM13, KM17, KM18
7. Verification: KM15
8. Adding an entry

---

# 1. Size and fit

## KM1. Content overflows the shape it sits in

Looked like: "100%" spilled over the edges of a battery ring.
Cause: the ring was fixed at 56 px (scaled) with a 5 px stroke, about 45 px of inner space, while "100%" at 17.6 px DemiBold is 4 x 17.6 x 0.65 = about 46 px wide. The mockup was only tried with short values.
Rule: size a shape (ring, disc, badge, pill) from its widest possible content, never from a nice looking number. Grow the shape, never shrink the text.
Check: widest content width (chars x px x 0.65 for bold) + 15% margin each side must be below the inner free space (diameter minus 2 x stroke minus padding).
Stacks: web, a fixed `width`/`height` on a ring around text; React Native, a fixed `width` on a View with centred Text; Qt/QML, a fixed `UiScale.px(56)` Item around a Text; Tauri, the web case.
Source: user M1, 2026-10-18.

## KM3. A label the product writes is elided, or its neighbour wraps

Looked like: "Connect automati..." in a settings row. In the 2026-10 trial a wrapping "Kunden & Projekte" sidebar label pushed its "Strg 4" key hint onto two lines.
Cause: the label shared a row with a 14 px inset, a large icon and a switch; the remaining width (about 190 px) was less than the text (about 200 px), and elide was left on. In the trial the key hint had no nowrap, so it shrank and wrapped when the label grew.
Rule: a label the product writes never elides. Let it wrap, give it room (smaller side elements, less padding), or shorten the words. Ellipsis is only for user data (file names, song titles) with the full value in a tooltip. Siblings of a label that may wrap never wrap.
Check: for each label, chars x px x 0.6 (0.65 bold) against the width left after padding and every sibling; grep the ellipsis properties and tie each hit to user data.
Stacks: web, `truncate` or `text-overflow: ellipsis` on a label, and a sibling without `white-space: nowrap; flex-shrink: 0`; React Native, `numberOfLines={1}` on a label, `flexShrink: 0` missing on the sibling; Qt/QML, `elide: Text.ElideRight` on a label, use `wrapMode: Text.Wrap` + `elide: Text.ElideNone` with `Layout.fillWidth` on the label only; Tauri, the web case.
Source: user M3, 2026-10-18.

## KM6. A room test forgot the app's own scale

Looked like: sections of a bar drawn on top of each other at scale 1.25.
Cause: the layout compared raw `screen.width` against a constant picked at scale 1. A 1920 px screen at 1.25 lays out like 1536 px, so the code believed it had room it did not.
Rule: every "is there room" test compares widths in drawn units: divide by the app's scale, or compare the sum of the pieces' real widths. When it does not fit, fold items in a fixed priority order; sections never overlap.
Check: grep `screen.width`, `innerWidth`, `Dimensions.get('window').width`; each comparison includes the scale.
Stacks: web, px media queries under a root font size change, use em breakpoints or container queries; React Native, width / fontScale or `onLayout`; Qt/QML, `screen.width / UiScale.scale` or the font token test (`pixelSize.normal >= 22`); Tauri, the web case plus the OS scale.
Source: user M6, before 2026-10-18.

## KM8. A custom visual has no intrinsic size

Looked like: an icon component vanished inside a layout.
Cause: a custom icon inside a Layout declared no implicitWidth or implicitHeight, so the layout gave it 0 x 0.
Rule: every custom visual (Canvas, Shape, SVG, icon item) declares its own intrinsic size.
Check: for each custom visual, find the size it reports when the parent gives it nothing.
Stacks: web, an `<svg>` without `width`/`height` attributes collapses in flex, add them plus `flex-shrink: 0`; React Native, a View or Svg without `width`/`height`; Qt/QML, `implicitWidth`/`implicitHeight` on the root; Tauri, the web case.
Source: user M8, before 2026-10-18.

# 2. Icons and assets

## KM2. Icon too small in its disc

Looked like: a tiny earbuds glyph in the middle of a large white circle.
Cause: an IrisDisc at 84 px (92 px at scale 1.1) kept its default icon size (27 px), about 30% of the disc.
Rule: a glyph fills about 40 to 55% of its disc or button. Set the icon size explicitly on big discs, through the scale.
Check: icon size / disc size between 0.40 and 0.55; read what the house component picks by default.
Stacks: web, an icon `size` prop left at its default inside a large round button; React Native, the same with vector icons; Qt/QML, `iconSize: UiScale.px(40)` for an 84 disc; Tauri, the web case.
Source: user M2, 2026-10-18.

## KM5. An asset was overwritten while a running app had it open

Looked like: every icon in the running shell showed a neighbouring glyph (a hand for Shut down, a rocking chair for Reboot).
Cause: the rebuilt icon font was `cp`'d over the installed file while the shell ran. The process kept the old name tables and read the new outlines.
Rule: install a rebuilt asset as a new file (`install -m644` unlinks and recreates), never copy over it, then restart the app.
Check: `grep -nE "cp .*fonts|cp .*\.(otf|ttf|woff2?)"` over the commands you ran or wrote is empty.
Stacks: web, rebuilt fonts and sprites get a content hash in the file name so caches never mix old and new; React Native, rebuild the app after replacing a font asset; Qt/QML, `install -m644` then Ctrl+Super+R and `koima --daemon`; Tauri, rebuild the bundle.
Source: user M5, 2026-10-18.

# 3. Colour

## KM4. A control vanishes on its surface

Looked like: a Disconnect pill was nearly invisible; only its text showed.
Cause: the pill's default fill `#050506` sat on a `#000000` panel, a difference of 5 to 6 per channel.
Rule: look up the real surface behind the control, not what the mockup had, and use the variant made for that surface (the on black variant `#161618`, or the white primary).
Check: fill vs surface differ by more than about 10 per RGB channel: `python3 scripts/contrast_check.py --surface "#000000" "#050506"` prints VANISHES. The label still needs 4.5:1.
Stacks: web, a dark secondary button on a dark card; React Native, a grey Pressable on a grey sheet; Qt/QML, IrisPill without `onBlack` on `Iris.ink`; Tauri, the web case.
Source: user M4, 2026-10-18.

# 4. Interaction

## KM7. A destructive action appeared under the cursor on hover

Looked like: a hover only Forget X unpaired the user's earbuds when they moved the pointer across the row.
Cause: the destructive control appeared on hover and acted on one click.
Rule: nothing destructive on hover. Destructive actions take two deliberate steps: a "..." or right click menu, then a confirm naming the thing or an undo window. Hover may reveal safe actions only (copy, open).
Check: every handler named delete, remove, forget, unpair, disconnect or discard reachable from a hover revealed element passes a confirm or undo.
Stacks: web, a `group-hover:` delete icon; React Native, rare (no hover) but the same for long press menus without confirm; Qt/QML, a `visible: hovered` delete button; Tauri, the web case.
Source: user M7, before 2026-10-18.

## KM9. An overlay never turned off

Looked like: a tooltip stayed on screen permanently.
Cause: a StyledToolTip sat in a parent with no `hovered` property and `extraVisibleCondition` was never bound, so nothing ever hid it.
Rule: every tooltip, popover, toast and hover card has a hide condition you can name in one line (pointer left, focus moved, Escape, timeout, parent closed).
Check: for each overlay, write its show and hide conditions side by side; a missing hide fails.
Stacks: web, a tooltip opened on `mouseenter` with no `mouseleave`, `blur` or Escape; React Native, a state set true with no path to false; Qt/QML, bind `extraVisibleCondition`; Tauri, the web case.
Source: user M9, before 2026-10-18.

## KM14. A live view stopped following new content

Looked like: once the user had scrolled up, new answers streamed in below the visible area and the chat never scrolled back to the newest message.
Cause: following was switched off on any contentY change the code had not made itself, so a layout shift could switch it off, and it was re-armed only on send, never at the start of an answer. A derived binding read inside the change handler returned the old value, so the view trailed growing content by up to 20 px.
Rule: only real input releases following (wheel, touchpad, drag, flick, keyboard). Every new message, every answer start and settling back at the bottom re-arm it. Compute derived values inline in the change handler.
Check: the handler that sets follow to false is reachable only from input events; in a harness sampled per frame, the newest message stays above the input line while following.
Stacks: web, release on `wheel`, `touchmove`, `keydown` or scrollbar `pointerdown`, not the bare `scroll` event; React Native, `onScrollBeginDrag`; Qt/QML, a contentY change while the Flickable is `moving`; Tauri, the web case.
Source: user M14, 2026-10-20.

## KM16. Hit areas stayed behind when their parent moved

Looked like: (caught in review) after a shelf slid a pill to the right, clicks on the moved pill would have reached the desktop and closed the popup.
Cause: a Quickshell `Region { item: x }` re-reads geometry only when x's own x, y, width or height change. Moving an ancestor changes none of them, so the input mask kept the old place.
Rule: a mask or hit item never sits inside something that moves. Put it on a fixed parent and bind its position to the moving parent's plus the child's (`x: stage.x + field.x`).
Check: for every mask or hit region, walk its parents up to the window; any animated or bound x, y or scale on the way makes it stale.
Stacks: web, a hit area or `clip-path` computed once from `getBoundingClientRect` before a transform; React Native, a cached `measure()` result after an animated move; Qt/QML, `Region { item }` inside an animated Item; Tauri, the web case plus window input regions.
Source: user M16, 2026-10-25.

# 5. Motion

## KM10. Content ran ahead of its container

Looked like: a reply bubble sprang open from a capsule, but the streamed letters appeared and ran across before the bubble had finished widening, so the text outran its own card.
Cause: the text was laid out at its final width and shown at once, while only the bubble's size animated on a spring. Content and container moved on two unrelated clocks.
Rule: content never appears before its container has arrived. When a container grows, its content stays hidden (opacity 0 or buffered) until the container's current size covers it, then fades in. While streaming, growth leads and letters follow.
Check: for every animated container, name what drives its children's visibility; text visible while the size animation still runs toward a larger target fails.
Stacks: web, reveal on `transitionend` or when the measured box covers the content, Framer Motion `layout` with children delayed; React Native, Reanimated children opacity from the container's progress; Qt/QML, gate opacity on the size Behavior or spring being settled; Tauri, the web case.
Source: user M10, 2026-10-20.

## KM11. An animation target came from a measurement that was not the drawn layout

Looked like: (caught by a harness) a reply bubble shrank under its still visible status line.
Cause: three ways a measured size lies. A Column or Row knows its implicit size only after the next polish (a hidden Row reports 0), so a same tick read returns the old size. A hidden measuring Text without the drawn Text's renderType, font, hinting or width has different advances. A "follow the measured size" handler fired while the new target was being written, before the state machine left idle.
Rule: measure with a twin that matches the drawn item exactly, treat positioner sizes as async (wait a frame or compute fixed parts by arithmetic), and change the state before writing values other handlers react to.
Check: for every size that drives an animation, name where it comes from and whether a frame passes between the content change and the read; diff a measuring twin's font properties against the drawn item.
Stacks: web, read sizes after `document.fonts.ready` in a ResizeObserver or the next frame; React Native, `onLayout`; Qt/QML, wait a polish or compute; Tauri, the web case.
Source: user M11, 2026-10-20.

# 6. Wiring

## KM12. A preview loaded through a different entry than the real viewer

Looked like: every idea in the Korme window showed "Could not load the idea".
Cause: the ideas imported a module the viewer's entry file never imported, so Quickshell never registered it. The agent's own harness imported it itself, so its check passed while the real window failed.
Rule: a preview may only use what the viewer's own entry loads. If it needs more, add it to the entry. A harness that imports the extra module proves nothing.
Check: compare the idea's imports with the viewer entry's imports; after opening, read the viewer's own log for "is not installed" or "not a type".
Stacks: web, a Storybook story that works only because a test wrapper adds a provider the decorators lack; React Native, a screen previewed outside the app's root providers; Qt/QML, `grep '^import qs'` on the ideas vs `~/dev/korme/korme.qml`; Tauri, a component previewed without the app's Tauri context.
Source: user M12, 2026-10-20.

## KM13. A reused reader returned the previous item

Looked like: (caught by a harness) each picture in a set got the aspect ratio and credit line of the one read before it.
Cause: one FileView with `blockLoading: true` was reused for several files by changing `path`; `blockLoading` does not block after a path change, so `text()` returned the previous file.
Rule: a reader used for several items in turn either blocks on every read (`blockAllReads: true`) or is one reader per item.
Check: read two different items in a row and compare a field that differs between them.
Stacks: web, a list without stable `key`s reusing state, or a slow earlier fetch landing after a newer one (abort it or drop stale responses); React Native, the same with FlatList `keyExtractor`; Qt/QML, FileView `blockAllReads`; Tauri, a shared command result cache.
Source: user M13, 2026-10-20.

## KM17. An id named like the property it feeds bound to itself

Looked like: (caught by a harness) a history shelf would have shown no chats and Continue did nothing, with no error in the log.
Cause: `QuickAskThread { history: history }` inside a Component, where `history` was both the child's property and an id outside the Component. An outer context id loses to the object's own property, so it was bound to itself and stayed null.
Rule: never give an id the same name as a property you pass it to. Name the id for what it is (`historyStore`) or qualify it (`root.history`).
Check: `grep -nE '^\s+([A-Za-z]+): \1\s*$'` over the QML; each hit has its id declared inside the same Component, or is renamed.
Stacks: web, a prop shadowed by a same name variable in a closure; React Native, the same; Qt/QML, the grep above; Tauri, the web case.
Source: user M17, 2026-10-25.

## KM18. An auth guard redirected into an unmatched route

Looked like: (caught by a router test) a signed out member got Expo Router's "Unmatched Route" screen instead of the login screen.
Cause: the protected stack guarded `/` while the login sat in a nested `(auth)` group with its own Stack and `initialRouteName`, and the redirect did not resolve into it. A test file inside `src/app/__tests__/` was itself a route and got bundled into the app.
Rule: screens a guard switches to are direct `Stack.Screen`s of the guarded stack. Tests and helpers live outside `src/app`.
Check: a `renderRouter('./src/app')` test per session state (signed out lands on login, signed in on home); `find src/app -path '*__tests__*' -o -name '*.test.*'` is empty.
Stacks: web, a Next.js middleware redirect into a route group that cannot match; React Native, the Expo Router case above; Qt/QML, a Loader switching to a page that is not registered; Tauri, a client router guard pointing at an unregistered path.
Source: user M18, 2026-11-01.

# 7. Verification

## KM15. A change was called live from a reload that came before the last edit

Looked like: the shell kept the old icon after the change was reported as live. The code on disk was correct.
Cause: the agent saw "Reloading configuration... Configuration Loaded" and called it live, but that reload had fired on an earlier write; the final edit was never picked up.
Rule: a change is live only when a reload line appears AFTER the last write of every changed file. If none appears, rewrite the file with its own content (a bare `touch` started no reload), and if still none, say a restart is needed. Without a log, say "on disk", not "live".
Check: note the log line count before the last write; after it, find a new reload pair with no errors between them.
Stacks: web, a Vite `hmr update` or Next `Compiled` line after the last save; React Native, an Expo Fast Refresh line; Qt/QML, `qs log -c ii` "Reloading configuration" plus "Configuration Loaded"; Tauri, the Vite line for the front end and a rebuild for Rust.
Source: user M15, 2026-10-25.

# 8. Adding an entry

- Same fields as above: Looked like, Cause (with the numbers), Rule, Check, Stacks, Source.
- One entry per defect class, written the day the defect is found.
- The local library first (the project's, or ~/.claude/ui-designer/mistakes.md for this user), then this file.
- Write the cause and rule stack free first, the stack detail second.
- The Source line points at the local id (user Mn) so `check_skill.py` can match them; it warns when a local id has no KM entry.
- Add a gate row to `quality/quality-gate.md` when the check can be run by reading code, and ship it as a release (`RELEASES.md`).
