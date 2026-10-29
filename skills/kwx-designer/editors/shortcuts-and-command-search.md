# Shortcuts, command search and fast menus

How to assign shortcuts, make them discoverable, and give experts a fast path that novices learn by using the slow path.

## Contents

1. The principle: the slow path must train the fast path
2. Assigning shortcuts
3. International keyboards and physical keys
4. Modifier keys: timing and meaning
5. Discoverability: six places a shortcut must appear
6. Command palette spec
7. Marking menus and pie menus
8. Cursor-local menus (S key, Shift+Space, Q)
9. Custom shortcuts and keymap presets
10. Checklist

---

## 1. The principle: the slow path must train the fast path

Kurtenbach and Buxton's marking menus show the ideal: a novice presses and waits about 1/3 s, a radial menu appears, and they stroke toward the item. An expert makes the same stroke without waiting, and no menu appears. Because "the physical movement" is identical, every novice use rehearses the expert gesture. In a field study, the experienced user chose by mark in 93 percent of selections, and marks were 3 to 4 times faster than menu selection even after removing the wait.

Apply this to every fast path:
- Menus and palettes show the shortcut next to each item, so reading the menu teaches the key.
- The pop-up toolbar shows each tool's key (Blender Shift+Space lists shortcuts on the right).
- Tapping Alt in Blender shows the tool keys in the status bar.
- Status bars list the current tool's mouse and modifier map and update when a modifier is held.

Superhuman's command palette guide says the same: show each command's shortcut in the results so the user can "learn the shortcut for next time".

## 2. Assigning shortcuts

### 2.1 Priority order

1. **Platform standards first, never overridden:** copy, paste, cut, undo, redo, save, open, find, select all, quit, new, close window, zoom in/out. VS Code guideline: do not "overwrite existing keyboard shortcuts".
2. **Category standards second:** V move/select, P pen, T text, R rectangle, O ellipse, F frame (Figma), Space pan, Z zoom, G/R/S move/rotate/scale (Blender, Plasticity), Tab edit mode (Blender), Delete/Backspace delete, Shift+D or Ctrl/Cmd+D duplicate, H hide, Ctrl/Cmd+G group. Check what Figma, Blender, Photoshop and VS Code use before inventing.
3. **Frequency third:** single-letter keys go to the most frequent tools and operators. Rare commands get no default shortcut; they live in the palette. Blender 2.80 deliberately assigned "fewer defaults" so users can map their own.
4. **Mnemonics fourth:** the first letter of the verb where it is free. If the first letter is taken, use a strong consonant (Blender: Extrude E, Knife K, Loop cut Ctrl+R).

### 2.2 Rules

- **Single letters for tools, modifiers for operators.** A bare letter switches tools or starts a temporary mode; destructive operators need a modifier or are reversible by undo.
- **Pairs sit next to each other physically.** Figma's rule: "move to front" and "move to back" must be "physically next to each other" (`]` and `[`). Same for zoom in/out, previous/next, increase/decrease.
- **Inverse equals Shift.** Shift reverses or extends: Tab / Shift+Tab, Ctrl+Z / Ctrl+Shift+Z, Alt+H unhide versus H hide (Blender).
- **Same key, same meaning everywhere.** Raskin's monotony: one gesture per effect; and consistency of the gesture's meaning across contexts. G is move in the viewport, in UV, in nodes, in the graph editor (Blender).
- **Never bind a destructive action to a key adjacent to a frequent one** without undo.
- **Do not clash with typing.** Single-key shortcuts must be suspended while a text field has focus, and text fields must take focus visibly.

## 3. International keyboards and physical keys

Figma's "Behind the scenes: international keyboard shortcuts" found over 2.5k distinct keyboard layouts in 30 days of usage.

- **Decide per shortcut: positional or character.** Mnemonic letters (T for text) follow the character. Spatial pairs and clusters (brackets for front/back, WASD style, number rows for selection modes) follow the physical position.
- **Detect the layout, but let the user confirm it.** Figma shows a diagram of each supported layout in settings so the user can match it to the physical keyboard, and stores the choice per device.
- **Never auto-switch the layout setting silently.** Figma dropped auto-updating because it could "cause unintended changes to their settings".
- **Test dead keys and numpad.** On AZERTY `^` is a dead key; Shift with numpad keys overrides Num Lock, breaking Shift+0 on some keyboards. Provide an alternative binding.
- **Do not uppercase keys with `toUpperCase()` naively** (`ß` becomes `SS`).
- **Respect each OS's modifier semantics:** Cmd on macOS maps to Ctrl on Windows and Linux, but macOS Ctrl has its own meaning.
- **Display shortcuts in the platform's notation:** ⌘⇧P on macOS, Ctrl+Shift+P elsewhere.

## 4. Modifier keys: timing and meaning

| Modifier during a drag | Common meaning |
|---|---|
| Shift | Constrain: axis lock, 45 degree steps, keep aspect ratio; with clicks, extend selection |
| Alt / Option | Duplicate while dragging; scale from center; select through |
| Ctrl / Cmd | Toggle snapping; deep select; precision |
| Space (held) | Pan (quasimode); in Figma while drawing a shape, reposition the shape being drawn |

- **Modifiers apply and release live during the drag** (tldraw).
- **Debounce the modifier release by about 150 ms** so releasing modifier and button together keeps the modifier's effect (tldraw's fix for a "physical race condition").
- **Show modifier hints in the status bar** during every drag: "Shift: constrain  Alt: duplicate  Ctrl: toggle snap". Blender updates the status bar "as modifier keys are held".

## 5. Discoverability: six places a shortcut must appear

A shortcut nobody can find does not exist. Every shortcut appears in:

1. **The tooltip** of its button (Blender HIG: "Include the shortcut, if one exists").
2. **The menu item**, right-aligned, muted (Blender: "All menu entries show any relevant shortcut keys").
3. **The command palette result** for that command.
4. **The status bar** while the related tool or mode is active.
5. **A searchable shortcut reference** (Figma Ctrl+Shift+? panel that highlights keys you have used; VS Code Keyboard Shortcuts editor). Opened by `?` or Ctrl+/ and from the Help menu.
6. **The context menu** entry for the same action.

Also:
- **Menus accept accelerators:** Blender menus can be driven by the underlined letter or number keys (1 for the first item).
- **Menus are searchable by typing** (Blender: press Space or just type in a popup menu to search it).
- **Teach on the second manual use.** After a user triggers a command from a menu several times, a subtle hint like "Tip: Ctrl+D duplicates" is allowed once, never repeated, and can be turned off.

## 6. Command palette spec

The palette is the one place where every command can be found. Requirements from VS Code's guidelines, Superhuman's guide, Retool's design write-up and Plasticity:

### 6.1 Behavior

- **One shortcut, available everywhere,** that does not clash with typing: Ctrl/Cmd+K, Ctrl/Cmd+Shift+P, or a single letter in a canvas-first tool (Plasticity F, Fusion S, Blender F3). The same shortcut closes it and returns focus to where it was (Superhuman).
- **Contains every command,** including those without a button or shortcut (Plasticity: "Commands that don't have buttons or shortcuts can be executed from the Command Palette"). Superhuman: "the one place where users can find every command." Decouple command execution from the UI that triggers it, so every button is also a command.
- **Fuzzy matching**, case insensitive, typo tolerant ("opn" finds "Open"), with a score threshold so junk is hidden.
- **Synonyms and aliases.** Match "remove" to Delete, "flip" to Mirror. Show the matching alias: "Delete (remove)", so users learn the canonical name.
- **Ranking:** before typing, show recent and suggested commands for the current context; after typing, sort by match score, boosted by frequency and recency. Group by category when helpful, but show a "Top result" above groups so a strong match is never buried (Retool).
- **Context-aware, not context-filtered.** Hide only commands that are impossible in the current context; show disabled ones with the reason if users often look for them.
- **Shows the shortcut** on the right of each result, and lets users assign one from the palette (Plasticity: right click a command, "Assign Shortcut", conflicts highlighted in red).
- **Favorites.** Pin commands from the palette (Plasticity favorites appear as buttons below the input).
- **Arguments without leaving the palette.** Multi-step commands take their arguments in the same box (VS Code multi-step Quick Picks with a title and step count).
- **Keyboard only:** Up/Down to move, Enter to run, Esc to close, Tab or Right to drill into a scope.
- **Opens in under 50 ms, filters every keystroke under 16 ms.** It is the expert's main tool; it cannot lag.

### 6.2 Look

- Centered or near the top, above everything, large enough for 8 to 10 results (Superhuman wants it prominent).
- Last visible item cut in half, to show there are more results (Superhuman).
- Each result: icon, command name in sentence case, category or path in muted text, shortcut right-aligned.
- Command names are clear verbs grouped by category ("Git: Commit"); no emoji in command names (VS Code).
- Placeholder text describes the purpose ("Search commands and layers"); a title only when the placeholder cannot say it (VS Code Quick Pick rules).

### 6.3 Scopes

- One surface for commands, objects (layers, components, files) and settings is easier than separate modes (Retool rejected VS Code style mode prefixes for their users). Use prefixes (`>`, `@`, `#`, `:`) only for audiences who already know them (code editors).
- Scope is shown as a removable chip in the input ("Button1 >"); Backspace on an empty input removes the chip and widens the scope (Retool).

## 7. Marking menus and pie menus

From Kurtenbach and Buxton (1993, 1994):

- **Breadth and depth limits for reliable marking:** 4 items up to 4 levels deep, or 8 items up to 2 levels deep, keep errors under about 10 percent. Beyond 8 items or 2 levels, "selection becomes error-prone, even for the expert".
- **Put the most frequent items on the axes** (N, E, S, W). Off-axis (diagonal) items were slower and less accurate.
- **Even number of items, at most 12.**
- **Keep item positions stable forever.** Marking menus are "unsuitable when item lists change dynamically" because users never learn stable directions.
- **Map directions to meaning.** Up for "top view", left for "previous", a command's inverse on the opposite side or the same mark (the paper suggests making a command's inverse repeat the same mark).
- **Always keep the visible menu as the fallback.** Experts return to the menu after a break "to refresh their memory of menu layout"; mark usage dips after lay-offs and recovers.
- **The press-and-wait delay is about 0.33 s.** Shorter and experts see menus flash; longer and novices think nothing happens.
- **Cancel by returning to the center** or releasing in the center dead zone.

Blender 2.80 pie menus (Orientation, Pivot, Viewport, Shading, Snap, Proportional falloff) open on key press and select by direction; a quick tap and flick selects without fully drawing. Fusion's marking menu opens on right click and drag. SolidWorks mouse gestures: right drag in a direction runs the command, with 2, 3, 4, 8 or 12 directions configurable.

## 8. Cursor-local menus

Moving the mouse to a far toolbar costs time on large screens (Fitts's law). Every pro tool converged on a menu that opens at the cursor:

| App | Key | What it shows |
|---|---|---|
| Blender | Shift+Space | Pop-up toolbar with tool shortcuts |
| Blender | Q | Quick Favorites: any command or menu added by right click "Add to Quick Favorites" |
| Fusion | S | Toolbox with search and user shortcuts, context-specific |
| SolidWorks | S | Shortcut bar per mode (part, assembly, drawing, sketch); press S twice to search (2022+) |
| Onshape | S | Shortcut toolbar, user-configured, fewer mouse trips |
| Plasticity | F | Command palette at the cursor |

Rules:
- Opens centered on the cursor, contents differ per mode, fully keyboard navigable.
- User customizable by right clicking any command anywhere ("Add to Quick Favorites", "Add to shortcut bar").
- Includes search as the first item, so the cursor menu doubles as a palette.

## 9. Custom shortcuts and keymap presets

- **Ship keymap presets for migrants:** Blender ships "Blender", "Blender 2.7X" (least changes for existing users), and "Industry Compatible". Zed ships base keymaps for VS Code, JetBrains, Sublime, Atom, TextMate. A preset beats a remapping guide.
- **First-run asks the two or three choices that matter most** (Blender Quick Setup: select with left or right click, what Spacebar does, theme).
- **Assign a shortcut from the item itself:** right click any button or menu item, "Assign Shortcut", press keys (Blender, Plasticity). Show conflicts before saving.
- **Shortcut editor lists conflicts**, filters by key ("what is Ctrl+D bound to?") and by command, and resets per entry.
- **Store keymaps as a readable file** that users can share and version (VS Code keybindings.json, Zed keymap).

## 10. Checklist

- [ ] No platform standard shortcut is overridden.
- [ ] Every frequent tool has a single-key shortcut; every destructive operator needs a modifier or is undoable.
- [ ] Pairs are physically adjacent; Shift inverts.
- [ ] Spatial shortcuts are positional and tested on AZERTY, QWERTZ and a Japanese layout.
- [ ] Every shortcut appears in tooltip, menu, palette, status bar, reference panel and context menu.
- [ ] The palette contains every command, matches fuzzily with aliases, shows shortcuts, opens under 50 ms.
- [ ] Any radial menu has at most 8 items, frequent ones on axes, stable positions.
- [ ] A cursor-local menu exists for tools used on large screens.
- [ ] Users can assign a shortcut by right clicking any command, with conflict warnings.
- [ ] At least one keymap preset matches the main competitor.
