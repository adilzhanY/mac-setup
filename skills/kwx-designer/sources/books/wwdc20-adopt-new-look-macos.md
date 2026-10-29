# Adopt the new look of macOS (Apple WWDC 2020, session 10104)

## What was read, and where

- Official session page with transcript: https://developer.apple.com/videos/play/wwdc2020/10104/ (transcript read). Covers the Big Sur redesign that still defines the macOS app shell: full height sidebars, unified toolbars, inline titles, inset tables.

## Key lessons

1. Full height sidebar via NSSplitViewController sidebar items; sidebar icons tint with the accent color by default, with fixed colors only when the color carries meaning (Mail VIP star is always yellow).
2. Sidebar text and symbols scale with the user's sidebar size setting (three sizes); never hardcode them.
3. Toolbar styles: unified (large controls, bold icons, inline title next to the sidebar), unified compact (regular controls, shorter bar), expanded (title above the toolbar for long titles or crowded toolbars), preference (centered uniform icons for settings windows).
4. Window subtitle under the title saves space; navigation back and forward items are pinned to the title leading position.
5. Toolbar search collapses into a button when the window narrows (NSSearchToolbarItem).
6. Toolbar symbols: SF Symbols at 13 pt, medium weight, large scale. Body font 13 pt. macOS text styles are not Dynamic Type.
7. Large is a standard control size; toolbar controls use it. Borderless toolbar buttons show their bezel only on hover; text buttons keep a border.
8. Let AppKit measure toolbar items instead of fixed min and max sizes.
9. Multicolor accent lets the app's own accent apply; still draw with named system colors, never hardcoded accent values.
10. Table styles: inset (extra padding, taller rows), full width, source list (sidebars); automatic picks by context. Scroll edge shadow appears under the toolbar when content scrolls beneath.
11. Toolbar sections align with split view dividers (tracking separator items) for clean full height columns.

## Where this lives in the skill

`platforms/desktop/desktop-foundations.md` sections 2 and 7, `platforms/desktop/windows-panels-menus.md` sections 3, 4 and 5, `platforms/desktop/macos-windows-linux-differences.md`.
