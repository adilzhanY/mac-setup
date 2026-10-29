# Windows, panels, toolbars, menus, drag and drop

The structural parts of a desktop app and how each one should behave. Sources: Apple HIG (windows, toolbars, the menu bar, menus, context menus, sidebars, split views, panels, sheets, drag and drop, undo, pointing devices), WWDC20 "Adopt the new look of macOS", Microsoft (title bar, command bar, NavigationView), GNOME HIG (header bars, pointer and touch, adaptive), KDE HIG (layout and navigation).

## Contents

1. App anatomy
2. Windows
3. Title bars and header bars
4. Toolbars and command bars
5. Sidebars and navigation panes
6. Split views and resizable panels
7. Inspectors and panels
8. Menus: menu bar, hamburger, context menus
9. Dialogs and sheets on desktop
10. Drag and drop
11. Undo, autosave and state restore
12. Tests

## 1. App anatomy

The standard productivity layout (Mail, Finder, Linear, Notion, Outlook, VS Code):

```
+-----------------------------------------------------------+
| title / toolbar: back fwd | title        | actions search |
+-----------+----------------------------+------------------+
| sidebar   | content list or canvas     | inspector        |
| (nav)     | (primary)                  | (details, opt.)  |
|           |                            |                  |
+-----------+----------------------------+------------------+
| optional status bar: counts, sync state (never critical)  |
+-----------------------------------------------------------+
```

- Leading = navigation, center = the work, trailing = details about the selection. This matches every platform's reading order and the KDE form factor table (sidebar leading, contextual tools trailing).
- Linear calls the sidebar plus header the "inverted L" chrome; keep it quiet so the content wins.

## 2. Windows

- Primary window: main navigation and content. Auxiliary window: one task, no navigation elsewhere, a button to close it (HIG).
- Open new windows deliberately: good for comparing or composing while reading (Mail compose). Do not open a new window by default for every item; offer "Open in New Window" in the context menu and File menu.
- Use the system window frame and controls. Custom chrome that does not exactly match the system feels broken (HIG). If you must draw a custom title bar (Electron, Tauri, Qt), reproduce: drag on all empty space, double click to maximize or zoom, right click for the system window menu (Windows), inactive state dimming, snap layouts on Windows 11 (hover the maximize button), traffic lights position on macOS.
- macOS: only one main and one key window; the key window has colored traffic lights and full materials, inactive ones are grey and subdued. Mimic these states in custom chrome.
- Keep critical information and actions out of the bottom of a window; people often push windows partly off screen (HIG). A bottom status bar may show counts and sync state only.
- Title each window with its content (document name, selected mailbox), never just the app name (HIG). Keep titles under about 15 characters where controls share the space.
- Remember size, position, panel widths and open tabs; restore them on relaunch (HIG, KDE).
- Do not keep running in the system tray after the last window closes unless the user chose that (KDE).
- Full screen is optional and reversible: Ctrl+Cmd+F / F11 / Esc to exit, menu bar revealed by moving the pointer to the top.

## 3. Title bars and header bars

| Platform | Pattern | Key numbers |
|---|---|---|
| Windows 11 | Title bar with icon, title, caption buttons; may host tabs, back button, search, account | 32 px tall standard, 48 px when it holds a search box or person picture; 16 x 16 icon 16 px from the edge; title 16 px after the icon in Caption style; caption buttons min / max / close full bleed on the trailing edge |
| macOS | Unified toolbar and title; traffic lights top leading; inline title next to the sidebar | toolbar symbols 13 pt medium; styles: unified, unified compact, expanded (title above toolbar for long titles or crowded toolbars), preference |
| GNOME | Header bar: primary actions start, title or view switcher center, menus end | few controls so the window can shrink; always leave blank space for dragging; every control has a tooltip |
| KDE | Title bar from the window manager plus a toolbar; menubar above toolbar or a hamburger menu | hamburger only if it holds about 15 items or fewer |

Rules:

- Leave draggable empty space in any custom title or header bar. A title bar packed edge to edge with tabs and buttons cannot be moved.
- Back and forward sit at the far leading edge, before the title (Windows, macOS, GNOME).
- Global search sits centered in the Windows title bar (48 px tall bar) or trailing in the macOS toolbar, collapsing to a button when narrow.
- In GNOME header bars use icon buttons (they lose their background automatically). Avoid label only and linked buttons in primary window header bars; group with spacing.

## 4. Toolbars and command bars

- Put only frequently used commands in the toolbar. Every toolbar item must also exist in the menu bar (macOS, HIG) because toolbars can be hidden or customized.
- Three groups at most: leading (navigation, sidebar toggle, title, document menu), center (common tools, customizable, first to collapse), trailing (inspector toggle, search, More menu, the one primary action). Trailing items stay visible at every width (HIG).
- One prominent primary action, trailing (Done, Submit).
- Prefer clear symbols without borders; macOS toolbar buttons show a bezel only on hover; buttons with text keep a visible border.
- Overflow: let the system collapse items into an overflow menu as the window narrows. Define which items go first. Do not design a toolbar that overflows at the default window size.
- Windows CommandBar: primary commands right aligned, most important first; at 320 epx only 4 primary commands fit; overflow "See more" holds secondary commands. Icons 20 x 20 in the bar, 16 x 16 in the overflow. Labels one word. On larger windows put labels to the right of icons so they are visible without opening the bar. Put Accept / OK to the left of Cancel / No in Windows command groups.
- Avoid sticky command bars; light dismiss is expected (Windows).
- Show a tooltip with name and shortcut on every icon only button, after about 500 ms of hover.
- Allow toolbar customization in apps used for long sessions (HIG, KDE).

## 5. Sidebars and navigation panes

- Use a sidebar when there are 5 to 10 or more top level places, or user created collections (folders, playlists, projects). With 5 or fewer equally important places a top nav or tab bar is enough (Windows NavigationView, KDE NavigationTabBar threshold of 5).
- Show at most two levels of hierarchy; collapse groups with disclosure triangles; deeper hierarchies get a middle content column (HIG).
- Let people hide the sidebar (toolbar toggle, View menu, shortcut) and resize it. Remember its width.
- Let people reorder and customize sidebar contents (HIG).
- Windows NavigationView auto behavior: expanded at >= 1008 epx, icons only at 641 to 1007, menu button only at <= 640. Settings sit at the bottom of the pane.
- Do not put critical items at the bottom of a sidebar; the bottom can be pushed off screen (HIG). Account and settings at the bottom are acceptable because they are not critical to the task.
- Selected item: accent tinted row (macOS sidebar uses accent icon tint by default), clear on dark and light, and stays visible when focus moves to the content.
- Icons: one consistent set, same size (16 px standard rows), aligned on one vertical line; color only when it carries meaning.

## 6. Split views and resizable panels

- Dividers: 1 pt thin divider style preferred (HIG), with a hit area of about 6 to 8 px for dragging and the resize cursor on hover.
- Every pane has a minimum and maximum width so the divider never disappears and content never collapses to unusable (sidebar typical 180 to 320 px; list pane 280 to 480 px; inspector 240 to 360 px).
- Collapse a pane by dragging it below its minimum, by a toolbar button, by a menu command and by a shortcut; offer more than one way back (HIG).
- Auto collapse the sidebar when the window gets narrow (Mail does this) and restore it when wide.
- Persistently highlight the selected item in each pane that leads to the detail (HIG).
- Double clicking a divider restores its default size (common convention).
- Resize live: content reflows during the drag, no jank, no flash.
- Support drag and drop between panes (move a message to a mailbox in the sidebar).

## 7. Inspectors and panels

- Inspector: a trailing pane that shows and edits properties of the current selection (Keynote, Figma, Xcode). It updates with the selection and never navigates.
- Panel (macOS): a floating auxiliary window for repeated input while watching results (Find and Replace, Colors, Fonts). Use a panel instead of a sheet when people need to act repeatedly and observe (HIG).
- Panels hide when the app is inactive, do not appear in the Window menu list, and do not steal key status unless a field needs input.

## 8. Menus: menu bar, hamburger, context menus

### macOS (and iPadOS) menu bar

- Provide the standard menus in order: App, File, Edit, Format, View, app specific, Window, Help. Keep standard items and their shortcuts (HIG).
- The menu bar is the complete, searchable command list. Every command lives here, even if it also lives in a toolbar or context menu. Help menu search finds any item.
- Always show the same items; disable unavailable ones instead of hiding them, so people learn what the app can do.
- Titles one word; items are verbs in title case, no articles ("Duplicate Layer"), ellipsis when more input follows ("Export As..."), checkmarks for active toggles, toggled labels that state the result ("Show Sidebar" / "Hide Sidebar").
- One level of submenu at most; submenus stay openable even if all children are disabled.
- Undo and Redo name the action ("Undo Paste and Match Style").
- Prefer "Duplicate" over "Save As"; autosave and offer Revert To versions.
- Menu bar extras: open a menu, not a popover, unless the function is too complex; let users choose whether the extra appears.

### Windows and Linux

- Windows: classic menu bar (File, Edit, View, Help) for document apps, or a command bar / ribbon; modern single window apps put a "..." or hamburger in the title area.
- GNOME: no menu bar; a primary menu (hamburger) at the end of the header bar with Preferences, Keyboard Shortcuts, Help, About. Secondary menus for view specific options.
- KDE: a real menubar between title bar and toolbar for apps with many commands; hamburger only for about 15 items or fewer, without Quit or Minimize; disable irrelevant items rather than hiding them.

### Context menus (right click)

- Show the most relevant commands for the clicked item, in the same order everywhere, most frequent first near the pointer.
- Short: about 5 to 12 items, grouped by separators, one submenu level at most.
- Hide unavailable items in context menus (unlike menu bar menus, where they are dimmed) (HIG).
- Do not show keyboard shortcuts in context menus on macOS (HIG). Windows and many cross platform apps do show them; follow the host platform.
- Every context menu command also exists in the main UI or menu bar (HIG, GNOME, KDE).
- Support context menus consistently: if rows have one, all rows, cards and items of the same kind do.
- Right click on a non selected item selects it first, then shows its menu; right click inside a multi selection acts on the selection and the menu title states the count.
- Destructive items last, separated, red where the platform supports it.
- Keyboard: Shift+F10 / Menu key opens it at the focused item.
- Do not use secondary click for alternative actions like delete (GNOME); it reveals options.
- No middle click as a required interaction (GNOME).

## 9. Dialogs and sheets on desktop

- macOS sheets attach to their parent window and block only that window; the rest of the app stays usable (HIG). Do not use an app wide modal for a document task.
- Windows ContentDialog: 8 px corners, primary button on the left of the button row in Windows convention (Accept left of Cancel), at most three buttons, Esc cancels, Enter triggers the default.
- GNOME dialogs: action buttons with suggested (accent) and destructive (red) styles; Cancel on the start side.
- A dialog asks one question, names the action on its buttons ("Delete", "Keep"), not "OK / Cancel" alone.
- For complex or long tasks open a window instead of a giant dialog (HIG sheets).

## 10. Drag and drop

- Support drag and drop wherever it makes sense; people try it everywhere (HIG). Always offer an alternative (menu command, cut and paste).
- Start the drag after about 3 pt of movement; show a translucent drag image of the content immediately (HIG). Let people select and drag in one motion.
- Show the result before the drop: highlight valid targets, insertion lines between rows, a badge with the item count for multi item drags, cursor badges for copy (Option / Ctrl held) and alias / link, the not allowed cursor over invalid targets.
- Same container = move; different container or app = copy. Option (macOS) or Ctrl (Windows) forces copy.
- Auto scroll a scrolling destination when the pointer nears its edge; spring load folders and tabs when hovered with an item.
- Invalid drop or failure: animate the item back to its source.
- After a drop, keep the dropped content selected; show progress for slow transfers.
- Every drop is undoable.
- Esc cancels an in progress drag (GNOME).
- Allow dragging out to the Finder / Explorer / desktop in a format the app can open again.
- Allow dragging from an inactive window without activating it or losing its background selection (macOS).

## 11. Undo, autosave and state restore

- Unlimited undo where feasible, always in the Edit menu with standard shortcuts, and the undo shows what changed (scroll to it if offscreen) (HIG).
- Group fine grained changes (dragging a slider) into one undo step.
- Autosave continuously; Save remains available for explicit versions. Never lose work on crash or quit.
- Quit with unsaved changes: offer Save, Don't Save, Cancel with clear labels.
- Restore windows, tabs, panes, scroll positions, selection and unsent drafts after relaunch.

## 12. Tests

- Shrink the window to the minimum size, then maximize on a 2560 px display. Nothing overlaps at small size; content does not stretch into 200 character lines at large size.
- Drag the window by every empty part of the title bar. Double click it.
- Hide the toolbar; every command is still in the menu bar or palette.
- Right click every kind of item; menus are consistent, short, and their commands exist elsewhere.
- Drag an item onto valid and invalid targets with and without the copy modifier; undo the drop.
- Quit with unsaved work, relaunch: windows, panes and drafts come back.
