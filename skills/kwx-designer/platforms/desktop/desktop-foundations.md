# Desktop foundations: the numbers for macOS, Windows and Linux

Desktop users have a precise pointer, a keyboard, big resizable windows, several apps open at once and long sessions. Design for all of that. Sources: Apple HIG 2026 (typography, accessibility, layout, windows, toolbars, pointing devices), WWDC20 "Adopt the new look of macOS", Microsoft Windows app design docs (typography, geometry, spacing, title bar, targeting, NavigationView), Fluent 2 layout, GNOME HIG, KDE HIG.

## Contents

1. Units and scaling
2. Type: sizes per platform
3. Target sizes and density
4. Spacing and grid
5. Corner radius and geometry
6. Window sizes and responsive breakpoints
7. Pointer states: hover, press, focus, disabled
8. Color, contrast and materials
9. Checklist

## 1. Units and scaling

- macOS: points; Retina is 2x. Windows: effective pixels (epx), scaled by the display scale factor (100, 125, 150, 200 percent). GNOME and KDE: logical pixels with fractional scaling.
- Never compare a layout breakpoint against raw device pixels. A 1920 px wide screen at 125 percent is 1536 logical px. Breakpoints use logical width.

## 2. Type: sizes per platform

| Platform | Body default | Minimum | System font |
|---|---|---|---|
| macOS | 13 pt | 10 pt | SF Pro (macOS has no Dynamic Type) |
| Windows 11 | 14 epx (Body) | 12 epx Regular, 14 epx Semibold | Segoe UI Variable (optical size axis 8 to 36 pt) |
| GNOME | 11 pt Cantarell / Adwaita Sans at 96 dpi (about 14.7 px) | follow system | Adwaita Sans (GNOME 48+), Cantarell before |
| KDE Plasma | 10 pt Noto Sans (about 13.3 px at 96 dpi) | follow system | Noto Sans |
| Web desktop apps | 14 to 16 px | 12 px | system stack |

### macOS text styles

| Style | Weight | Size / line pt |
|---|---|---|
| Large Title | Regular | 26 / 32 |
| Title 1 | Regular | 22 / 26 |
| Title 2 | Regular | 17 / 22 |
| Title 3 | Regular | 15 / 20 |
| Headline | Bold | 13 / 16 |
| Body | Regular | 13 / 16 |
| Callout | Regular | 12 / 15 |
| Subheadline | Regular | 11 / 14 |
| Footnote, Caption 1, Caption 2 | Regular, Regular, Medium | 10 / 13 |

Toolbar symbols on macOS are SF Symbols at 13 pt, medium weight, large symbol scale (WWDC20).

### Windows 11 type ramp

| Style | Size / line epx | Weight |
|---|---|---|
| Caption | 12 / 16 | Regular |
| Body | 14 / 20 | Regular |
| Body Strong | 14 / 20 | Semibold |
| Body Large | 18 / 24 | Regular |
| Subtitle | 20 / 28 | Semibold |
| Title | 28 / 36 | Semibold |
| Title Large | 40 / 52 | Semibold |
| Display | 68 / 92 | Semibold |

Windows rules: Regular for text, Semibold for titles, never Bold or Italic in the ramp; sentence case for all UI text including titles; 50 to 60 characters per line, never more than 60 or fewer than 20; use Body Strong instead of Title in confined spaces; Caption for very tight spaces such as command buttons.

Desktop type rules:

- Desktop body is smaller than mobile (13 to 14 vs 17) because the screen is farther from the eye but the pointer is precise. Do not port a 17 pt mobile layout as is; it looks oversized.
- Use the platform font unless you have a strong brand reason. Inter, SF Pro and Segoe UI Variable all work for product UI; use one family.
- Use tabular (monospaced) numerals in tables, timers and any column of numbers.
- Respect the system text size setting (Windows text scaling, GNOME large text, macOS sidebar size). Title bars must grow with Windows text scaling.

## 3. Target sizes and density

| Platform | Default control | Minimum |
|---|---|---|
| macOS | 28 x 28 pt | 20 x 20 pt |
| Windows touch-capable layout | 40 x 40 epx grid (7.5 mm) | 32 x 32 epx in Compact density |
| Windows mouse-only dense UI | Compact density (`Compact.xaml`) | 32 epx grid |
| Web desktop (WCAG 2.2 AA) | 24 x 24 px target or 24 px spacing | 24 x 24 px |

Rules:

- Mouse targets can be smaller than touch, but not tiny: 24 px is the floor, 28 to 32 px is comfortable for frequent controls.
- Many laptops have touchscreens (Hoober: over half of laptops sold in 2021). If the app can run on a touch laptop or tablet mode, offer a comfortable density with 40 epx targets or switch density in tablet mode (KDE: enlarge small controls in tablet mode).
- Padding: about 12 pt around bezeled controls, about 24 pt around borderless ones (HIG, all platforms).

## 4. Spacing and grid

- 4 px base grid. Fluent 2 ramp: 2, 4, 6, 8, 10, 12, 16, 20, 24, 28, 32, 36, 40, 48, 52, 56.
- Windows spacing rules: 8 epx between buttons, 8 between a button and its flyout, 8 between a control and its header, 12 between a control and its label, 12 between content areas, 16 between a surface edge and text. Expander child controls indent 48 epx.
- KDE Kirigami: `smallSpacing` within a group, `largeSpacing` between groups and from the window edge to UI, `mediumSpacing` between toolbar items, 0 between window edge and frameless views; `gridUnit` 18 px for fixed sizes.
- Group with less space inside, more space between groups. Space between groups at least 2x the space within.

## 5. Corner radius and geometry

| Element | Windows 11 | macOS | GNOME (libadwaita) |
|---|---|---|---|
| Window | 8 px (0 when snapped or maximized) | about 10 pt, larger on macOS 26 windows with toolbars | about 12 px |
| Flyouts, menus, dialogs | 8 px | 6 to 10 pt menus, sheets rounded | 12 px dialogs, menus about 9 px |
| Buttons, inputs, list backplates | 4 px | about 5 to 6 pt (regular control) | 6 px buttons |
| Tooltip, progress, slider, scrollbar | 4 px | system | system |

Rules: nested radii are concentric (inner radius = outer radius minus the padding between them). Elements that touch each other (split button halves) are not rounded on the touching edges. A flyout attached to its trigger is square on that side.

(macOS and GNOME radii above are measured from current system controls, not written specs; check the live system theme.)

## 6. Window sizes and responsive breakpoints

- GNOME: every app supports 1024 x 600 at minimum; phone ready apps scale down to 360 x 294.
- Windows NavigationView auto modes: expanded left pane at >= 1008 epx, icon only (LeftCompact) at 641 to 1007, menu button only (LeftMinimal) at <= 640.
- Fluent 2 breakpoints: small 320 to 479, medium 480 to 639, large 640 to 1023, x-large 1024 to 1365, xx-large 1366 to 1919, xxx-large 1920+.
- Material window classes for desktop web and ChromeOS: expanded 840 to 1199, large 1200 to 1599, extra-large 1600+.
- Set a sensible minimum window size so nothing overlaps; never set min = max to block resizing.
- At very wide sizes, cap content width (readable column about 600 to 760 px for text, lists in a max width container) and center or anchor it (GNOME adaptive guidance). Long lines and stretched forms are the most common wide window defect.
- Remember and restore window size and position on relaunch (HIG, KDE).

## 7. Pointer states: hover, press, focus, disabled

Every interactive element has five visual states. Design all five:

| State | Treatment |
|---|---|
| Rest | Base look |
| Hover | Subtle fill or border appears (Material state layer 8 percent; macOS toolbar buttons show their bezel only on hover) |
| Pressed | Darker or lighter than hover (10 percent layer), no layout shift |
| Focused (keyboard) | Visible focus ring, at least 2 px, 3:1 contrast against neighbors, offset so it is not clipped |
| Disabled | 38 percent content opacity, no hover reaction, still readable |

Rules:

- Hover is a bonus, never the only way to discover something (GNOME: do not rely on hover to reveal actions or essential information). Hidden row actions that appear on hover also need a keyboard path and a context menu.
- Change the cursor only when meaningful: I-beam over text, pointing hand only for links (macOS convention: buttons keep the arrow), resize arrows on dividers, grab hand for pannable canvases, not-allowed during an invalid drop.
- Hover delays: tooltips appear after about 500 ms of rest and then appear instantly when moving to the next item in the same bar.
- Focus ring in a text or search field; full row highlight for focus in lists and collections (HIG focus and selection).
- Keep focus where the user put it. Never move focus programmatically except to the obvious next field or a just opened dialog (HIG).

## 8. Color, contrast and materials

- Contrast 4.5:1 for text, 3:1 for large or bold text and for icons and control borders. Check in light, dark and high contrast themes (Windows high contrast uses SystemColors; do not hardcode).
- Windows: Mica for the window base layer (title bar blends with the window), Acrylic for transient surfaces (flyouts). Inactive windows drop their materials and their caption buttons turn grey; mimic this in custom chrome.
- macOS: inactive windows look subdued (no vibrancy, grey traffic lights). Use system named colors and the user's accent color; never hardcode your own accent over theirs.
- Linux: follow the system theme (GTK accent color in GNOME 47+, KDE color schemes). Do not ship a custom theme that ignores dark mode or the accent.
- Selection uses the accent color in the key window and a neutral grey in inactive windows (background selection).

## 9. Checklist

- [ ] Body size matches the platform (13 pt macOS, 14 epx Windows), one font family, tabular figures in numbers.
- [ ] Every control has rest, hover, pressed, focused and disabled states; focus ring visible at 3:1.
- [ ] Targets >= 24 px, frequent ones >= 28 px, touch mode >= 40 epx.
- [ ] Window works at the minimum size (1024 x 600 at least) and at 2560+ wide with capped content width.
- [ ] Inactive window appearance handled.
- [ ] Light, dark, high contrast and accent color all respected.
