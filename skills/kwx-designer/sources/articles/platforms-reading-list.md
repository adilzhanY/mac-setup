# Reading list: mobile and desktop platform design

Every source used for the files in `platforms/mobile/` and `platforms/desktop/` (research done 2026-10-27). "Read" means fetched and read; "located" means found but not readable, with nothing taken from it beyond what is noted. Apple HIG pages were read from their DocC JSON (`https://developer.apple.com/tutorials/data/design/human-interface-guidelines/<page>.json`) because the HTML pages render with JavaScript; the content is the same and reflects the September 2026 revision (Liquid Glass).

## Apple Human Interface Guidelines (read, JSON form)

- Layout: https://developer.apple.com/design/human-interface-guidelines/layout
- Typography (full Dynamic Type tables, macOS text styles): https://developer.apple.com/design/human-interface-guidelines/typography
- Accessibility (control sizes, contrast, text sizes): https://developer.apple.com/design/human-interface-guidelines/accessibility
- Tab bars: https://developer.apple.com/design/human-interface-guidelines/tab-bars
- Toolbars: https://developer.apple.com/design/human-interface-guidelines/toolbars
- Sheets: https://developer.apple.com/design/human-interface-guidelines/sheets
- Modality: https://developer.apple.com/design/human-interface-guidelines/modality
- Sidebars: https://developer.apple.com/design/human-interface-guidelines/sidebars
- Split views: https://developer.apple.com/design/human-interface-guidelines/split-views
- Windows: https://developer.apple.com/design/human-interface-guidelines/windows
- The menu bar: https://developer.apple.com/design/human-interface-guidelines/the-menu-bar
- Menus: https://developer.apple.com/design/human-interface-guidelines/menus
- Context menus: https://developer.apple.com/design/human-interface-guidelines/context-menus
- Keyboards (standard shortcut table, modifier rules): https://developer.apple.com/design/human-interface-guidelines/keyboards
- Gestures: https://developer.apple.com/design/human-interface-guidelines/gestures
- Playing haptics: https://developer.apple.com/design/human-interface-guidelines/playing-haptics
- Pointing devices: https://developer.apple.com/design/human-interface-guidelines/pointing-devices
- Focus and selection: https://developer.apple.com/design/human-interface-guidelines/focus-and-selection
- Drag and drop: https://developer.apple.com/design/human-interface-guidelines/drag-and-drop
- Undo and redo: https://developer.apple.com/design/human-interface-guidelines/undo-and-redo
- Materials: https://developer.apple.com/design/human-interface-guidelines/materials
- Loading: https://developer.apple.com/design/human-interface-guidelines/loading
- Launching: https://developer.apple.com/design/human-interface-guidelines/launching
- Onboarding: https://developer.apple.com/design/human-interface-guidelines/onboarding
- Also downloaded and skimmed: buttons, color, dark mode, motion, alerts, action sheets, popovers, text fields, feedback, settings, scroll views, segmented controls, toggles, progress indicators, panels, file management, multitasking, going full screen, search fields, lists and tables, SF Symbols, widgets, notifications.
- Navigation bars and inspectors JSON did not convert (located only).

## Apple talks and articles

- WWDC18 Designing Fluid Interfaces, transcript: https://developer.apple.com/videos/play/wwdc2018/803/ (read; notes in `sources/books/wwdc18-designing-fluid-interfaces.md`)
- WWDC20 Adopt the new look of macOS, transcript: https://developer.apple.com/videos/play/wwdc2020/10104/ (read; notes in `sources/books/wwdc20-adopt-new-look-macos.md`)
- Behind the Design: Flighty: https://developer.apple.com/news/?id=970ncww4 (read)
- Behind the Design: Halide Mark II: https://developer.apple.com/news/?id=x6bv1a36 (read)

## Material Design 3 and Android

- m3.material.io pages render with JavaScript and returned no content (located). Numbers were taken from the Material 3 Compose token sources instead:
  - Token directory: https://github.com/androidx/androidx/tree/androidx-main/compose/material3/material3/src/commonMain/kotlin/androidx/compose/material3/tokens (read: NavigationBar, NavigationRailCollapsed / Expanded, NavigationDrawer, TypeScale, Shape, Elevation, Motion, StandardMotion, ExpressiveMotion, SheetBottom, Snackbar, AppBarSmall / Medium / Large, ButtonXSmall / Small / Medium, FabBaseline / Medium / Large, List, Dialog, State, SmallIconButton, DragHandle, SearchBar, Switch, Checkbox, Scrim)
  - PaneScaffoldDirective defaults (panes per size class, 24 dp spacer, 360 / 412 dp pane width): https://github.com/androidx/androidx/blob/androidx-main/compose/material3/adaptive/adaptive-layout/src/commonMain/kotlin/androidx/compose/material3/adaptive/layout/PaneScaffoldDirective.kt (read)
- Material Components for Android docs (navigation bar 3 to 5 destinations, rail 3 to 7, sheets): https://github.com/material-components/material-components-android/tree/master/docs/components (read: BottomNavigation, NavigationRail, NavigationDrawer, BottomSheet)
- Window size classes: https://developer.android.com/develop/ui/compose/layouts/adaptive/use-window-size-classes (read)
- Canonical layouts: https://developer.android.com/develop/ui/compose/layouts/adaptive/canonical-layouts (read)
- Adaptive navigation: https://developer.android.com/develop/ui/compose/layouts/adaptive/build-adaptive-navigation (read)
- Make apps more accessible (48 dp, contrast): https://developer.android.com/guide/topics/ui/accessibility/apps (read)
- Haptics design principles: https://developer.android.com/develop/ui/views/haptics/haptics-principles (read)
- Edge to edge: https://developer.android.com/develop/ui/views/layout/edge-to-edge (read)
- Material 3 Expressive navigation changes (secondary): https://9to5google.com/2025/05/14/material-3-expressive-navigation/ (located via search summary)

## Microsoft Windows and Fluent 2

- Content layout and spacing: https://learn.microsoft.com/en-us/windows/apps/design/basics/content-basics (read)
- Title bar: https://learn.microsoft.com/en-us/windows/apps/design/basics/titlebar-design (read)
- Typography in Windows: https://learn.microsoft.com/en-us/windows/apps/design/signature-experiences/typography (read)
- Geometry (corner radii): https://learn.microsoft.com/en-us/windows/apps/design/signature-experiences/geometry (read)
- Targeting (7.5 mm, 40 x 40): https://learn.microsoft.com/en-us/windows/apps/design/input/guidelines-for-targeting (read)
- NavigationView: https://learn.microsoft.com/en-us/windows/apps/design/controls/navigationview (read)
- Command bar: https://learn.microsoft.com/en-us/windows/apps/design/controls/command-bar (read)
- XAML styles (no density numbers): https://learn.microsoft.com/en-us/windows/apps/design/style/xaml-styles (read)
- Compact sizing (40 epx standard grid, 32 epx compact): found via search summary of https://learn.microsoft.com/en-us/windows/apps/design/style/spacing (located)
- Fluent 2 layout (spacing ramp, breakpoints): https://fluent2.microsoft.design/layout (read)

## GNOME and KDE

- GNOME HIG adaptive: https://developer.gnome.org/hig/guidelines/adaptive.html (read)
- GNOME HIG header bars: https://developer.gnome.org/hig/patterns/containers/header-bars.html (read)
- GNOME HIG keyboard: https://developer.gnome.org/hig/guidelines/keyboard.html (read)
- GNOME standard keyboard shortcuts: https://developer.gnome.org/hig/reference/keyboard.html (read)
- GNOME HIG pointer and touch: https://developer.gnome.org/hig/guidelines/pointer-touch.html (read)
- KDE HIG index: https://develop.kde.org/hig/ (read)
- KDE Simple by default: https://develop.kde.org/hig/simple_by_default/ (read)
- KDE Powerful when needed: https://develop.kde.org/hig/powerful_when_needed/ (read)
- KDE Layout and navigation: https://develop.kde.org/hig/layout_and_nav/ (read)

## Touch research (Steven Hoober)

- How Do Users Really Hold Mobile Devices? (2013): https://www.uxmatters.com/mt/archives/2013/02/how-do-users-really-hold-mobile-devices.php (read)
- Design for Fingers, Touch, and People, Part 1 (2017): https://www.uxmatters.com/mt/archives/2017/03/design-for-fingers-touch-and-people-part-1.php (read); Parts 2 and 3 URLs tried returned 404
- Fitts's Law in the Touch Era (2022): https://www.smashingmagazine.com/2022/02/fitts-law-touch-era/ (read)
- Touch Design for Mobile Interfaces, free sample PDF: https://smashingmagazine.com/provide/eBooks/touch-design-for-mobile/touch-design-for-mobile-interfaces-sample-chapter.pdf (read; notes in `sources/books/touch-design-for-mobile-interfaces.md`)
- Accessible Target Sizes Cheatsheet (Vitaly Friedman, cites the book): https://www.smashingmagazine.com/2023/04/accessible-tap-target-sizes-rage-taps-clicks/ (read)

## Nielsen Norman Group

- Response Times: The 3 Important Limits: https://www.nngroup.com/articles/response-times-3-important-limits/ (read)
- Skeleton Screens 101: https://www.nngroup.com/articles/skeleton-screens/ (read)
- Bottom Sheets: https://www.nngroup.com/articles/bottom-sheet/ (read)
- Hamburger Menus and Hidden Navigation Hurt UX Metrics (mobile study): https://www.nngroup.com/articles/find-navigation-mobile-even-hamburger/ (read)
- Contextual Swipe: https://www.nngroup.com/articles/contextual-swipe/ (read)
- Designing Empty States in Complex Applications: https://www.nngroup.com/articles/empty-state-interface-design/ (read)

## Craft: apps and their own writeups

- Superhuman, How to build a remarkable command palette: https://blog.superhuman.com/how-to-build-a-remarkable-command-palette/ (read)
- Superhuman, Built for speed (100 ms rule): https://blog.superhuman.com/superhuman-is-built-for-speed/ (read)
- Linear, How we redesigned the Linear UI: https://linear.app/now/how-we-redesigned-the-linear-ui (read)
- Linear Method index: https://linear.app/method (read, table of contents only)
- Raycast, A fresh look and feel: https://www.raycast.com/blog/a-fresh-look-and-feel (read)
- Raycast manual, action panel: https://manual.raycast.com/action-panel (located via search summary)
- MacStories, Things 3 review: https://www.macstories.net/reviews/things-3-beauty-and-delight-in-a-task-manager/ (read)
- Maggie Appleton, Command K Bars: https://maggieappleton.com/command-bar (read)
- Arc: Wikipedia and secondary design analyses only (located via search); no primary Browser Company design writeup found
- NFX on Superhuman onboarding (secondary): https://www.nfx.com/post/superhuman-product-frameworks (located via search summary)

## Illustrative images viewed (not copied into the skill)

Downloaded to the session scratchpad and viewed:

- Material navigation bar anatomy (vertical and horizontal items): active indicator is a pill behind the icon only in the vertical layout and behind icon plus label in the horizontal layout; badges are a small dot or a count pill offset to the icon's top trailing corner. Lesson: on wide windows the bar item becomes icon beside label, and the selection pill grows to contain both.
- Material navigation rail hero: collapsed rail stacks icon over label with a FAB on top; expanded rail turns into a drawer like list with icon plus label rows and an extended FAB. Lesson: one component, two widths, same order of destinations.
- Material bottom sheets, standard vs modal: identical sheet with 28 dp top corners and a 32 x 4 dp handle; only the modal one dims the background with a scrim. Lesson: scrim signals "background is unavailable", so omit it when the background stays interactive.
- Windows title bar with search: icon and app title at the leading edge, a search box centered in a taller (48 px) title bar, caption buttons trailing, menu row below. Lesson: a centered global search lives in the title bar only when the bar grows to hold it, and empty space on both sides stays draggable.
- Also downloaded: Windows title bar overview and command bar open state images.
