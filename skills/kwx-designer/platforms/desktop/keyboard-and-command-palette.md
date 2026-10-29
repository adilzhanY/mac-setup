# Keyboard first design and command palettes

On desktop the keyboard is the fastest input for anyone who uses an app daily. A premium desktop app can be driven entirely from the keyboard, teaches its shortcuts as you use it, and has one universal place to search for any command. Sources: Apple HIG keyboards and menu bar, GNOME HIG keyboard guidelines and standard shortcuts reference, KDE HIG "Powerful when needed", Superhuman "How to build a remarkable command palette" and "Built for speed", Raycast "A fresh look and feel", Maggie Appleton "Command K bars".

## Contents

1. Principles
2. Standard shortcuts you must not break
3. Choosing custom shortcuts
4. Focus and keyboard navigation
5. The command palette (Cmd/Ctrl+K)
6. Teaching shortcuts
7. Single key shortcuts and modes
8. Tests

## 1. Principles

- Every action reachable by pointer is reachable by keyboard (GNOME, KDE, HIG Full Keyboard Access). Every pointer operation in progress (drag, drawing) cancels with Esc.
- Shortcuts are accelerators, never the only path. Primary workflows stay visible by default (KDE).
- Give the most frequent actions shortcuts, not every action (HIG, GNOME). Too many custom shortcuts make the app feel hard to learn. KDE asks for every action to at least be user assignable.
- Speed is a feature: every keyboard action should complete in under 100 ms, ideally under 50 ms (Superhuman). A shortcut that triggers a 400 ms spinner feels broken.

## 2. Standard shortcuts you must not break

Show Cmd on macOS, Ctrl on Windows and Linux.

| Action | macOS | Windows | GNOME / KDE |
|---|---|---|---|
| New | Cmd+N | Ctrl+N | Ctrl+N |
| Open | Cmd+O | Ctrl+O | Ctrl+O |
| Save / Save As | Cmd+S / Shift+Cmd+S | Ctrl+S / Ctrl+Shift+S | Ctrl+S / Shift+Ctrl+S |
| Close tab or window | Cmd+W | Ctrl+W (Alt+F4 closes window) | Ctrl+W |
| Quit | Cmd+Q | Alt+F4 on last window | Ctrl+Q |
| Settings | Cmd+, | Ctrl+, (common in modern apps) | Ctrl+, |
| Undo / Redo | Cmd+Z / Shift+Cmd+Z | Ctrl+Z / Ctrl+Y (Ctrl+Shift+Z also common) | Ctrl+Z / Shift+Ctrl+Z |
| Cut / Copy / Paste | Cmd+X / C / V | Ctrl+X / C / V | Ctrl+X / C / V |
| Paste and match style | Option+Shift+Cmd+V | Ctrl+Shift+V | Shift+Ctrl+V |
| Select all | Cmd+A | Ctrl+A | Ctrl+A |
| Find / next / previous | Cmd+F / Cmd+G / Shift+Cmd+G | Ctrl+F / F3 / Shift+F3 | Ctrl+F / Ctrl+G / Shift+Ctrl+G |
| Replace | Option+Cmd+F | Ctrl+H | Ctrl+H |
| Print | Cmd+P | Ctrl+P | Ctrl+P |
| Zoom in / out / reset | Cmd+= / Cmd+- / Cmd+0 | Ctrl+= / Ctrl+- / Ctrl+0 | Ctrl++ / Ctrl+- / Ctrl+0 |
| Back / forward | Cmd+[ / Cmd+] | Alt+Left / Alt+Right | Alt+Left / Alt+Right |
| Toggle sidebar | Ctrl+Cmd+S (common) | Ctrl+B or app specific | F9 |
| Help / shortcuts list | Cmd+? | F1 | F1 / Ctrl+? |
| Full screen | Ctrl+Cmd+F | F11 | F11 |
| Next / previous tab | Ctrl+Tab / Ctrl+Shift+Tab, Cmd+Shift+] / [ | Ctrl+Tab / Ctrl+Shift+Tab | Ctrl+Tab, Ctrl+PageDown / PageUp |
| Cancel / close transient UI | Esc, Cmd+. | Esc | Esc |
| Context menu | Ctrl+click | Shift+F10 or Menu key | Shift+F10 or Menu key |
| Rename (files) | Return (Finder) | F2 | F2 |
| Properties | Cmd+I | Alt+Enter | Alt+Return |

Do not repurpose any of these. Only reuse one if the action makes no sense in your app (HIG example: an app with no text styling may use Cmd+I for Get Info).

## 3. Choosing custom shortcuts

- Main modifier: Cmd on macOS, Ctrl on Windows and Linux, plus a letter (mnemonic if possible: Ctrl+E for Edit).
- Shift as the secondary modifier for the reverse or extended version of a related shortcut (Ctrl+Z / Shift+Ctrl+Z). Never add Shift to an existing shortcut for an unrelated command.
- Option (macOS) sparingly for power variants. Avoid Control as a modifier on macOS (system uses it). On Linux do not use Super / Meta (reserved for the desktop) and avoid Alt+letter (access keys).
- Avoid function keys alone on laptops (KDE): they often need Fn.
- Prefer one handed chords for frequent actions; avoid awkward reaches (GNOME).
- Only use letters available on all keyboard layouts with extra modifiers; Option+5 is "{" on French keyboards (HIG). Test on non US layouts.
- List modifiers in the platform order. macOS: Control, Option, Shift, Command, shown as symbols in menus. Windows and Linux: Ctrl+Shift+Alt+Key written out.
- For the upper character of a two character key write the character, not Shift: Cmd+? not Shift+Cmd+/.

## 4. Focus and keyboard navigation

- Tab and Shift+Tab move between controls in a logical reading order; Ctrl+Tab moves between groups or panes when Tab is used inside a field.
- Arrow keys move within a group: list rows, grid cells, menu items, tabs, toolbar items, radio groups. Home / End jump to first and last.
- Return activates the default action of the focused item or the dialog's default button. Space toggles. Esc closes the topmost transient layer (menu, popover, dialog, palette) and returns focus to where it came from.
- F6 (and Ctrl+F6 on macOS) cycles between major panes: sidebar, list, detail.
- Type to select: typing letters in a focused list jumps to the matching row. Things on Mac starts a search as soon as the user types ("Type Travel").
- Focus is always visible when the keyboard is in use: a 2 px ring with 3:1 contrast, or a full row highlight in lists. Show it on keyboard focus, hide it after a mouse click (`:focus-visible` on the web).
- Never trap focus except inside a modal, and every modal is escapable with Esc.
- After closing a dialog, restore focus to the control that opened it. After deleting a row, focus the next row, not the top of the page.
- Access keys (Windows and Linux): Alt shows underlined letters on labels and menus; give as many labeled controls as possible a unique access key, avoiding thin letters (i, l) and descenders (g, y).

## 5. The command palette (Cmd/Ctrl+K)

Why it exists: a GUI that shows every command does not scale past a few dozen commands. A palette lets people search for any command by name instead of remembering which submenu it lives in, and frees the screen from rarely used buttons (Appleton).

Rules:

1. One shortcut, everywhere. Cmd+K (macOS) / Ctrl+K is the convention (Superhuman, Linear, Slack, GitHub, Raycast's action panel). Ctrl+Shift+P is the code editor convention (VS Code). If Cmd+K is taken in a text editor (insert link), a second press can open the palette. The same shortcut and Esc close it and return focus where it was.
2. Also give it a visible entry point (a search button or "Cmd K" hint in the toolbar or sidebar). A palette nobody knows about does nothing.
3. Visually dominant: centered, wide (about 560 to 720 px), above a dim or blur, input focused immediately, results under the field.
4. Forgiving matching: case insensitive, then fuzzy, so "opn" and "oepn" match "Open". Drop weak matches below a score threshold.
5. Synonyms: give every command aliases ("remove", "trash" for Delete). When an alias matched, show it: "Delete (trash)".
6. Ranking: each command has a default score; context boosts relevant ones (list view vs single item); usage frequency and recency raise scores; some commands always rank below a related one.
7. Context: most commands are available everywhere; hide only the fully irrelevant ones.
8. Empty query is not empty: show recent and suggested commands, and a few top destinations.
9. Each row: icon, command name, optional context ("in Project X"), and the keyboard shortcut right aligned. Showing the shortcut is the whole teaching mechanism.
10. Cut off the last visible row partially so people see there is more to scroll (Superhuman).
11. Keyboard: Up / Down move, Return runs, Cmd+Return or Tab for a secondary action, Esc closes, Backspace on an empty query goes back one level in nested commands.
12. Nested steps for commands that need a parameter (Move to... then pick a project) stay inside the palette, with a breadcrumb chip in the field.
13. Search content too (documents, issues, files), but group it below commands with headers so actions and objects are not mixed.
14. Results appear on every keystroke within one frame or two; no debounce delays above about 50 ms; no spinner for local commands.
15. The palette is an addition, not a replacement: every command in it also lives in a menu, toolbar or context menu. Do not add one "because everyone has one"; add it when there are more commands than fit visibly.

Bad: palette that only searches documents, no shortcuts shown, opens with a 200 ms fade, and loses the current selection on close. Good: Cmd+K opens instantly over the current view, "arc" finds "Archive (E)", Return archives the selected item and the palette closes with focus back on the list.

## 6. Teaching shortcuts

- Show the shortcut next to every menu item (menu bar menus, not context menus, per HIG) and in every tooltip: "Archive (E)".
- Raycast moved actions into a bottom action bar where every action shows its shortcut, specifically so users learn them over time. Primary action on Return, secondary on Cmd+Return, more on Cmd+K.
- Provide a shortcuts reference: Cmd+? / Ctrl+? or "?" opens a searchable overlay grouped by area (GNOME shortcuts window pattern, Linear, Gmail).
- Optional nudges: after a user performs the same action by mouse several times, show a one time hint with its shortcut. Never nag repeatedly.

## 7. Single key shortcuts and modes

- Single letter shortcuts (E archive, J / K next / previous, C compose, / search) are the fastest, used by Gmail, Superhuman, Linear. Allow them only when focus is not in a text field, and let users turn them off (WCAG 2.1.4 requires a way to disable or remap single character shortcuts).
- Two key sequences (G then I to go to Inbox) need a short visible hint after the first key and a timeout of about 1 to 1.5 s.
- Vim style navigation (J / K, H / L) delights power users but must coexist with arrow keys.

## 8. Tests

- Unplug the mouse. Complete the top five tasks with the keyboard only. Any dead end or invisible focus fails.
- Press Esc at every layer; it closes the top layer only and focus returns to the opener.
- Open the palette and type a misspelled command, a synonym and a shortcut name. All three find the command.
- Check every menu item with a shortcut also shows it, and every shortcut appears in the reference overlay.
- Test the shortcuts on a German, French and Russian layout.
