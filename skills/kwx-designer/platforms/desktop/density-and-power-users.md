# Density and power users

Desktop apps are used for hours by people who know them well. They want to see more at once and do more per keystroke, without the screen becoming noise. Density is a design decision with numbers, not a vibe. Sources: Windows density docs (40 epx standard grid, 32 epx Compact), Linear UI redesign writeup, Raycast compact mode, Superhuman, KDE "Simple by default, powerful when needed", Apple HIG toolbars and menus, NN/g response times.

## Contents

1. Pick a density on purpose
2. Row heights and the numbers
3. Making dense UI calm
4. Progressive disclosure for power
5. Customization without settings sprawl
6. Bulk actions and selection
7. Tables and data
8. Speed as a density feature
9. Tests

## 1. Pick a density on purpose

| Product | Density | Row height |
|---|---|---|
| Consumer, touch capable, occasional use | Comfortable | 44 to 56 px |
| Daily productivity (mail, tasks, issues) | Standard | 32 to 40 px |
| Expert tools (IDEs, trading, logs, spreadsheets) | Compact | 22 to 28 px |

- Windows standard controls sit on a 40 epx grid; Compact density (WinUI `Compact.xaml`, for pointer input) on a 32 epx grid.
- macOS controls default 28 pt, minimum 20 pt; sidebar rows follow the user's chosen sidebar size (small, medium, large).
- Offer a density switch only when the audience truly splits (Gmail: default, comfortable, compact). Otherwise choose one and make it excellent.
- If the app runs on touch laptops or tablets, switch to comfortable spacing in tablet mode (KDE).

## 2. Row heights and the numbers

| Element | Compact | Standard | Comfortable |
|---|---|---|---|
| List / table row | 24 to 28 px | 32 to 36 px | 44 to 56 px |
| Sidebar item | 24 to 28 px | 28 to 32 px | 36 to 40 px |
| Toolbar | 36 to 40 px | 44 to 52 px | 56 to 64 px |
| Body text | 12 to 13 px | 13 to 14 px | 14 to 16 px |
| Icon in row | 14 to 16 px | 16 px | 20 to 24 px |
| Horizontal cell padding | 6 to 8 px | 8 to 12 px | 12 to 16 px |

Text never goes below 12 px (Windows minimum 12 epx Regular, macOS 10 pt only for captions). If dense rows feel cramped, remove elements from the row, do not shrink the type.

## 3. Making dense UI calm

Linear's redesign goal: "reduce visual noise, maintain visual alignment, and increase the hierarchy and density of navigation elements." Their methods, as rules:

- Align everything. Labels, icons and buttons in the sidebar and tabs share exact vertical and horizontal lines. Misalignment is far more visible at high density.
- Reduce chrome color. Linear limited the accent (blue) so it plays a smaller role; the interface is mostly neutral, so status colors and the selection stand out.
- Separate surfaces by small lightness steps (background, panel, dialog, modal), generated in a perceptually uniform space (Linear moved from HSL to LCH so equal lightness looks equally light across hues).
- Give users a contrast control instead of many theme variables (Linear: base color, accent, contrast; contrast 30 to 100 to produce accessible high contrast themes).
- Use a display cut of the font for headings (Inter Display) and the text cut for everything else.
- Remove borders before removing space. Use whitespace and alignment for grouping; keep 1 px dividers only where scanning across columns needs them.
- One accent, one weight change, one size change per level of hierarchy. Do not stack bold + color + size + icon on the same item.
- Secondary information at secondary contrast (about 60 to 70 percent of primary text contrast, still >= 4.5:1).
- Hover reveals row actions, but the same actions exist in the context menu and as shortcuts.

## 4. Progressive disclosure for power

KDE's principle: simple by default, powerful when needed.

- The default view shows what a new user needs, with labels and controls fully visible, no overflow menus at the default window size.
- Power features live one level deeper: context menus, the command palette, keyboard shortcuts, an inspector panel, a "more" section that expands in place.
- Do not hide features on an "Advanced" page. Use progressive disclosure instead: simple first, details on a sub page, an expandable section, or a separate window (KDE).
- Shortcuts, context menus and gestures are accelerators only; their functions are also elsewhere.
- Raycast's Compact Mode: optional, strips the interface to search and results for users who want focus.
- Halide's rule applies to desktop pro tools too: advanced features "never more than a few taps away", never a flight simulator of dials.

## 5. Customization without settings sprawl

- Settings choose between valid workflows; a setting that only turns a feature on or off is a warning sign of an undecided design (KDE).
- Apply settings immediately; never require a restart (KDE).
- Do not let customization override the platform theme, accent or font (KDE, HIG).
- Let people customize the toolbar in apps used for long sessions (HIG), the sidebar contents and order, and keyboard shortcuts.
- Saved views and filters are the most valuable customization for data apps (Linear views, Mail smart mailboxes). Make "save this filter" one action.

## 6. Bulk actions and selection

- Standard multi selection: click, Shift+click for a range, Cmd/Ctrl+click to toggle, Cmd/Ctrl+A for all, Shift+Up / Down to extend, Esc to clear. Rubber band (marquee) selection in grids and canvases.
- Checkboxes on hover in lists (Gmail, Linear) make selection discoverable without a mode.
- When items are selected, show a bulk action bar with the count ("3 selected") and the actions that apply to all.
- Every bulk action is undoable, or confirms with the exact count for destructive ones ("Delete 214 issues?").
- Background selection: selections in inactive windows stay visible in grey and can still be dragged (HIG).

## 7. Tables and data

- Left align text, right align numbers, use tabular numerals, align decimal points.
- Sticky header row and sticky first column for wide tables.
- Sort by clicking the header (indicator shows direction); resize columns by dragging the divider (resize cursor), double click the divider to fit content.
- Truncate long cells with an ellipsis and show the full value on hover tooltip and in the detail view. Never wrap rows unpredictably in dense tables.
- Zebra striping only for wide tables with many columns; otherwise hover highlight plus row dividers.
- Inline edit on double click or Return, commit on Return or blur, cancel on Esc.
- Virtualize long lists so scrolling 10,000 rows stays at 60 fps.

## 8. Speed as a density feature

- The perceived density of an expert app includes time. A dense screen that takes 800 ms to respond feels worse than a sparse one that is instant.
- Targets: input response < 100 ms (Superhuman aims < 50 ms), view switch < 200 ms, search results on every keystroke.
- Techniques: local database and cache, prefetch the next likely item (Superhuman preloads threads you are likely to open), optimistic updates, minimal animation in hot paths (Superhuman reduces animation so no time goes to it), virtualization.
- Animations for expert actions are 100 to 200 ms at most, or none. Save longer motion for rare, spatial transitions.

## 9. Tests

- Count the visible items in the main list at 1440 x 900. Compare with the best competitor. Fewer without a reason fails.
- Squint test: with blurred vision, only the selection, primary action and status colors should stand out.
- Alignment test: draw vertical guides at the icon and text start of the sidebar, list and toolbar. Off by 1 to 2 px fails.
- Measure input latency for the five most used actions. Anything over 100 ms needs work.
- New user test: complete the core task without opening any menu, palette or settings.
