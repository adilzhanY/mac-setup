# macOS vs Windows vs Linux (GNOME, KDE)

The same desktop product must feel native on each system. Users switch less between desktop systems than between apps, so system habits (button order, menu location, shortcuts, window controls) are deep muscle memory. Sources: Apple HIG 2026, Microsoft Windows app design docs and Fluent 2, GNOME HIG, KDE HIG.

## Contents

1. Big picture
2. Comparison table
3. Button order in dialogs
4. Menus and commands
5. Shortcuts and modifiers
6. Window chrome and controls
7. Typography and look
8. Cross platform apps (Electron, Tauri, Qt, Flutter, Compose Desktop)
9. Tests

## 1. Big picture

| System | Character | Primary command surface |
|---|---|---|
| macOS | Document centric, global menu bar, toolbar integrated in the title bar, materials and vibrancy | The menu bar (always complete) |
| Windows 11 | Window centric, commands inside the window, Mica / Acrylic materials, Segoe UI Variable, rounded 4 / 8 px | Command bar, ribbon, or in window menu |
| GNOME | Minimal, header bars, no menu bar, adaptive down to phones, few settings | Header bar plus primary (hamburger) menu |
| KDE Plasma | Configurable, menubar plus toolbar, "simple by default, powerful when needed" | Menubar or hamburger, toolbar, shortcuts for everything |

## 2. Comparison table

| Topic | macOS | Windows 11 | GNOME (libadwaita) | KDE (Kirigami / Qt) |
|---|---|---|---|---|
| Body font | SF Pro 13 pt | Segoe UI Variable 14 epx | Adwaita Sans / Cantarell 11 pt | Noto Sans 10 pt |
| Default / min control | 28 / 20 pt | 40 epx grid; 32 epx Compact | about 34 px buttons | gridUnit 18 px multiples |
| Window controls | Traffic lights, top leading | Min / max / close, top trailing, full bleed | Close (and optional min / max) at header bar end | Window manager decides, usually trailing |
| Title bar | Unified with toolbar, inline title | 32 px; 48 px with search or account | Header bar with app controls | Separate title bar plus toolbar |
| Menus | Global menu bar, Help search | In window menu or command bar | Primary menu at header bar end, no menubar | Menubar, or hamburger if 15 items or fewer |
| Settings | App menu > Settings (Cmd+,), separate window | Settings page in app (gear, often bottom of nav pane) | Primary menu > Preferences (Ctrl+,), dialog | Settings > Configure App, Kirigami FormLayout |
| Navigation pane | Sidebar, full height, accent tinted icons | NavigationView left, auto collapses at 1008 / 640 epx | Sidebar in split view, collapses to stack on narrow | GlobalDrawer, NavigationTabBar for 5 or fewer |
| Dialog buttons | Cancel left, default right | Primary left, Cancel right | Cancel start, suggested action end | Platform style: OK / Apply / Cancel order from Qt (Cancel last on Linux) |
| Primary modifier | Cmd | Ctrl | Ctrl (never Super) | Ctrl (never Meta) |
| Context menu | Ctrl+click or secondary click, no shortcuts shown | Right click or Shift+F10, shortcuts often shown | Right click, Menu / Shift+F10 | Right click, Menu |
| Corner radius | windows about 10 pt, controls about 6 pt | 8 px windows and flyouts, 4 px controls | about 12 px windows, 6 px buttons | theme dependent (Breeze about 3 to 5 px) |
| Materials | Vibrancy, Liquid Glass in macOS 26 | Mica base, Acrylic flyouts | Flat, accent color, no blur | Breeze, optional blur in Plasma |
| Accent color | User picks, apps follow | User picks, apps follow | User picks (GNOME 47+), apps follow | Color scheme, apps follow |
| Minimum window | as content needs | as content needs | 1024 x 600 desktop, 360 x 294 for phone ready apps | as content needs, remember size |
| Tray / background | Menu bar extra, user opt in | Notification area icon | No tray by default; background portal | System tray; do not stay running after close unless chosen |
| Quit | Cmd+Q; closing last window may not quit | Closing last window quits | Ctrl+Q; closing window quits | Ctrl+Q |

## 3. Button order in dialogs

This is the most common cross platform defect. Follow the host:

- macOS: `[Cancel] [Default action]`, default rightmost, triggered by Return; destructive actions are named and not default; Cancel by Esc and Cmd+.
- Windows: `[Primary action] [Secondary] [Cancel]`, primary leftmost (Accept, Yes, OK to the left of Reject, No, Cancel), Enter triggers default, Esc cancels.
- GNOME: `[Cancel] ... [Suggested action]`, suggested at the end in the accent style, destructive in red.
- KDE / Qt: use `QDialogButtonBox` and let Qt order buttons for the platform.

Rule: never hardcode one order for all systems. Use the toolkit's button box or a platform switch.

## 4. Menus and commands

- macOS: a complete menu bar is mandatory (App, File, Edit, Format, View, custom, Window, Help). Toolbar items duplicate menu items, not the other way round.
- Windows: document apps keep a menu bar or ribbon; simple apps use a command bar and a "..." overflow. Do not ship a macOS style app menu on Windows.
- GNOME: no menu bar. Primary menu holds New Window, Preferences, Keyboard Shortcuts, Help, About. Do not put Quit there; Ctrl+Q works.
- KDE: offer a menubar for apps with many commands; KHamburgerMenu gives both, user can switch.

## 5. Shortcuts and modifiers

- macOS: Cmd primary, Shift secondary, Option sparingly, avoid Control. Show symbols in menus.
- Windows: Ctrl primary, Shift secondary, Alt reserved for access keys (Alt+letter underlines) and Alt+F4. F2 rename, F5 refresh, F11 full screen, Ctrl+Y redo.
- GNOME: Ctrl plus letter; Shift+Ctrl for reverse; never Super; avoid Alt combos (access keys). F10 opens the primary menu, F9 the side pane, Ctrl+? shows the shortcuts window.
- KDE: KStandardShortcut actions, Ctrl plus alphanumeric, never function keys alone on laptops, never Meta.
- Cross platform: map Cmd to Ctrl automatically, but check every shortcut against each system's reserved list (Ctrl+Alt+Del, Win+letter, Cmd+Space, Cmd+Tab, Super, Alt+Tab).

## 6. Window chrome and controls

- macOS custom title bars keep the traffic lights in their system position with enough leading inset (toolbar content starts after them). Full size content view for edge to edge sidebars.
- Windows custom title bars: drag regions on all empty space, system menu on right click, double click maximizes, Snap Layouts flyout on maximize hover (use the system caption buttons via the Windows App SDK title bar APIs, do not paint fake ones), Mica behind.
- GNOME client side decorations: the header bar is the title bar; respect the user's button layout setting (close only, or min max close, left or right).
- KDE server side decorations by default; client side only if the app needs a header bar look.

## 7. Typography and look

- Use the native font on each system: SF Pro (macOS), Segoe UI Variable (Windows), the system UI font on Linux (read it from the theme). A single brand font everywhere is acceptable for content, but UI chrome in the system font feels native.
- Windows: sentence case everywhere. macOS: title case for menu items, buttons and window titles. GNOME: header case for titles and buttons, sentence case for descriptions. KDE: title case for buttons and menu items, sentence case for labels.
- Icons: SF Symbols on macOS, Segoe Fluent Icons on Windows (back E830, close E8BB), symbolic icons from the theme on GNOME (adwaita symbolic), Breeze monochrome icons on KDE. Do not ship Material icons as the only set on macOS; they read as a web app.

## 8. Cross platform apps

- Electron / Tauri / web: provide the native menu bar on macOS (even if the window has its own UI), native window controls on Windows (titleBarOverlay), respect system theme and accent via CSS `prefers-color-scheme` and `AccentColor` where available.
- Qt: use the platform style and `QDialogButtonBox`; Kirigami adapts to Plasma, Android and others.
- Flutter / Compose Desktop: add platform menus (PlatformMenuBar on macOS), keyboard shortcuts per system, and native file dialogs.
- Always use native file pickers, print dialogs, color pickers and notifications. Custom ones are the fastest way to feel foreign.

## 9. Tests

- Open a confirmation dialog on each system. The button order matches the host.
- Use a daily user of each system to run the top tasks; note every "my computer does not do this" moment.
- Check shortcut conflicts against each system's reserved list.
- Switch the system to dark mode, high contrast and a different accent color while the app is open. The app follows live.
