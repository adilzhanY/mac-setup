# Tools, modes and selection

How the pointer's meaning changes, how to keep that from confusing people, and exactly how selection should behave.

## Contents

1. Vocabulary: tool, operator, mode, quasimode
2. Modes: when they are acceptable and how to show them
3. Tool lifecycle and the toolbar
4. Noun-verb versus verb-noun
5. Selection model: the exact rules
6. Advanced selection: marquee, lasso, through, by type, hierarchy
7. Selection and undo
8. Checklist

---

## 1. Vocabulary

| Term | Definition | Example |
|---|---|---|
| **Tool** | A persistent state that decides what the primary button does on the canvas. One active tool at a time. | Pen, Rectangle, Box Select, Knife, Sculpt Draw |
| **Operator** | A one-shot command on the current selection that finishes immediately (possibly after an interactive drag). | Duplicate, Extrude Region, Flip, Boolean Union |
| **Mode** | A state in which the same gesture means something different, and which persists after the user stops acting. | Blender Edit Mode, CAD sketch mode, text editing, vi insert mode |
| **Quasimode** | A mode maintained physically, which ends when the user lets go (Raskin's term, also "spring-loaded mode"). | Hold Space to pan, hold Shift to constrain, hold Ctrl to toggle snapping |
| **Temporary mode** | A modal operator that ends as soon as the user stops acting (Blender's term). | Press G to move: the mouse moves the object until click or Esc |

Raskin's definition: an interface is modal for a gesture when the current state is outside the user's attention and the interface responds to that gesture differently depending on that state. Corollary: a mode the user is attending to is not a problem. A mode the user has forgotten is.

## 2. Modes: when they are acceptable and how to show them

### 2.1 Rules (from Raskin, Tesler and the Blender paradigms)

1. **Eliminate the mode if you can.** Tesler's Gypsy editor removed the insert mode and command mode by letting users select text with a drag and act on it with Cut and Paste keys. Ask: could this be a selection plus an operator instead of a mode?
2. **If a mode cannot be eliminated, make it a quasimode** (Raskin: "eliminate all modes. If a mode cannot be eliminated, convert it to a quasimode"). Hold to activate, release to exit. Users "cannot accidentally forget" a quasimode because they are physically holding it.
3. **Allowed persistent modes are editing modes tied to the data** (Blender's list: per-object editing modes such as Edit Mode and Pose Mode, plus sticky transform tools). Everything else is temporary.
4. **Transient modes beat persistent ones.** Raskin's notes: modes that end after a gesture cause fewer errors than modes that stay.
5. **Do not give the same gesture different meanings in different modes** when you can avoid it. Click-drag on empty canvas should box select in every mode where that makes sense.
6. **Preferences are modes too.** Raskin warns that settings which change what gestures do are "an obtuse way of specifying modes". Every preference that changes input mapping must be visible from where it acts (Miro's wheel behavior lives in preferences and causes "random" zoom complaints).

### 2.2 Showing the active mode: use at least three signals

Users miss single signals. For any persistent mode, show three of these at once:

| Signal | Example |
|---|---|
| A word in a fixed place | Blender header dropdown "Object Mode / Edit Mode"; "Editing sketch" in a CAD header |
| Cursor shape | Crosshair for drawing tools, I-beam for text, pen nib for path tools |
| Changed toolbar contents | Blender's toolbar shows Edit Mode tools only in Edit Mode; Onshape swaps the Feature toolbar for the Sketch toolbar |
| A visible frame or tint | A colored border around the canvas (sketch mode, follow mode, isolation mode), dimmed out-of-scope objects (entering a group in Illustrator dims everything else) |
| Status bar hint text | Blender status bar lists the mouse and key map of the current tool and updates while modifiers are held |
| An exit control | "Finish sketch" check button, "Exit isolation" breadcrumb, Esc hint |

Tests:
- Take a screenshot in the mode. Hide the cursor. Can a colleague tell which mode it is? If not, add a word.
- Leave the app for 10 minutes mid-mode, come back. Is the first thing you see the mode?

### 2.3 Entering and exiting

- Every mode has exactly one obvious entry (a toggle or a double click on the object) and at least two exits: Esc and a visible Done/Finish button.
- Esc exits one level at a time: cancel the current drag, then close the open popover, then finish the sub-mode, then deselect. Never more than one level per press.
- Switching tools inside a mode never leaves the mode silently.
- Leaving a mode never discards work without undo.
- Blender's "Lock Object Modes" protects against accidental mode changes: clicking another object while in Pose Mode does not throw you into Object Mode. Provide this protection for any mode tied to one object.

## 3. Tool lifecycle and the toolbar

### 3.1 The toolbar

- **Order tools by frequency and by group,** with the default tool (Select/Move) first. Blender's fallback tool is "the one at the top of the Toolbar".
- **Group variants behind one button** with a small corner triangle; press and hold to open, or drag to open instantly (Blender). Show the last used variant on the button (Onshape moves the last used tool to the top of its group).
- **Every tool button shows its shortcut in the tooltip.** Short hover shows the name; longer hover shows the full description (Blender's two-stage tooltip).
- **Let the toolbar widen to show labels.** Blender: resizing the toolbar shows two columns, then icon plus text. Good for learners, free for experts.
- **Offer a pop-up toolbar at the cursor** (Blender Shift+Space) so the user does not travel to the edge.
- **Cycle within a group with repeated presses** of the same key (Blender W cycles Box, Circle and Lasso select).

### 3.2 Tool states as a state machine

Model each tool as a small hierarchical state machine (tldraw's architecture). The select tool in tldraw has `idle`, `pointing_shape`, `translating`, `resizing`, `rotating`. A drawing tool has `idle`, `pointing`, `drawing`.

- The `pointing` state exists so that a press waits to see whether it becomes a click or a drag (drag threshold). Never start a drag on press.
- Transitions are explicit, and each state has enter and exit code. Cancel (Esc) returns to `idle` and restores the state at the last history mark.
- Spec every tool as this table: state, entering input, visible feedback, exit inputs.

### 3.3 After a creation tool finishes

Pick one behavior per tool and state it:

| Behavior | When | Example |
|---|---|---|
| Return to Select after one shape | Shapes, frames, notes, arrows: users usually adjust right after creating | tldraw and Figma rectangle, text |
| Stay in the tool | Repetitive drawing: pen, brush, eraser | Brush tools, Blender tools in general ("stay active until you pick another") |
| User lock | Let users lock any creation tool to keep it active | tldraw tool lock (`isToolLocked`), Excalidraw lock icon, double click a tool in some apps |

Show the lock state on the toolbar (a lock glyph on the tool or a pressed lock button).

### 3.4 Tool settings

- Tool settings show in the tool settings bar above the canvas, and in full in a tool tab of the inspector (Blender shows them in three places: Sidebar Active Tool panel, Properties Tool tab, Tool Settings region).
- Tool settings affect the NEXT action. Adjust Last Operation affects the LAST action. Keep the two physically separate: Blender puts the redo panel in the bottom left corner of the editor and the tool settings at the top "to avoid confusion".
- Tool settings persist per tool and per mode (Blender remembers the active tool per workspace and mode).

## 4. Noun-verb versus verb-noun

- **Default to noun-verb: select, then act.** Raskin's notes: noun-verb "is inherently less modal" because the user picks the content first and attention returns to it right after the action; verb-noun needs a cancel gesture when the user changes their mind about the verb.
- Blender's paradigm "Select -> Operate": "No tool mode must be activated beforehand."
- **Verb-noun is right for creation and painting tools** (pick a brush, then paint). Raskin's notes acknowledge palettes in painting tools as the accepted norm.
- **Selection-driven command lists are the modern noun-verb UI.** Shapr3D shows only the operations valid for the current selection; adding an edge to a face selection narrows the list to operations that use both (loft, revolve). Plasticity's "Suggested Commands" works the same way. Build this for any tool with more than about 30 operations.
- **Action-first context menus.** Blender HIG: a right click should "immediately show common actions, usually as verbs" without noun submenus first. Name menus by task ("Format", not "Font").

## 5. Selection model: the exact rules

Write this table in every editor spec and implement it exactly. The rules below are the consensus of Figma, Sketch, Blender (left-click select keymap) and the Blender HIG "select-tweaking" rules.

| Input | Result |
|---|---|
| Click unselected object | Select it, deselect all others (immediately on press) |
| Press on unselected object then drag | Select it and move it (no separate move tool needed) |
| Press on selected object then drag | Move ALL selected objects; selection unchanged |
| Press and release on an already selected object in a multi-selection, no drag | On release: select only that object (deselect the others), make it active |
| Shift + click | Toggle that object in the selection (add or remove) |
| Ctrl/Cmd + click (2D) | Deep select: select the innermost object under the cursor, ignoring groups |
| Click empty canvas | Deselect all |
| Drag on empty canvas | Marquee (box) select; replaces the selection |
| Shift + drag on empty canvas | Marquee adds to the selection |
| Double click a group or component | Enter it, select the child under the cursor |
| Esc | Exit one level: from child back to the parent group, then deselect |
| Ctrl/Cmd + A | Select all at the current level |
| Tab / Shift+Tab (design tools) | Select next/previous sibling |
| Right click unselected object | Select it (deselect others), then open its context menu |
| Right click selected object | Keep the selection, open the context menu |

The last two rows are verbatim Blender HIG: "If the item is already selected, don't deselect others. If the item is not already selected, deselect others."

Note: Onshape uses a different model: clicking toggles selection with no modifier ("Multiple selections don't require holding a function key"). This works in CAD where multi-entity selection for features is the norm. Pick one model per product and never mix them within one canvas.

### Active versus selected

- Many editors need an **active** item inside the selection: the one the inspector shows, the pivot for "align to active", the target for "copy to selected". Draw it brighter or with a thicker outline than the rest (Blender: active is light orange, others darker orange).
- Clicking an already selected item makes it active without changing the selection (Blender HIG).
- The inspector header names the active item and the count: "Rectangle 12 (and 4 more)".

## 6. Advanced selection

- **Marquee mode:** decide "touching" versus "fully enclosed". Design tools usually select objects the marquee touches; CAD often uses direction: left-to-right selects fully enclosed, right-to-left selects touched (AutoCAD window vs crossing). If you use direction, draw the two modes differently (solid versus dashed rectangle).
- **Lasso and paint selection** (Blender Circle Select, W cycles): hit test along segments between pointer samples so fast motion does not skip items.
- **Select through / behind:** Alt/Option + click cycles to the object underneath at the same point (Blender Alt+click shows a menu of overlapping objects; Illustrator and others cycle). Provide one of the two.
- **X-ray toggle:** in 3D, marquee normally selects only visible elements; toggling X-ray (Blender Alt+Z) lets it select through. Show the X-ray state in the header.
- **Selection filters:** CAD and 3D need element type filters (vertex, edge, face, body; Plasticity uses 1 to 4 for modes and Tab for all). Show the current filter in the header as a segmented control with the number shortcuts.
- **Select similar / by type:** "Select all with the same fill", "same component", "same font". Put it in the context menu of a selection (Figma shows "Select matching layers"; the UI3 context menu has "Search for similar").
- **Hierarchy navigation:** SolidWorks selection breadcrumbs show the chain of the selected element (face, feature, sketch, body, component, assembly) at the top left, and the D key brings them to the cursor; clicking a crumb selects that parent. Offer the same for any deep hierarchy: a breadcrumb strip near the selection or in the inspector header.
- **Hover preselection:** highlight what would be selected on click before the click (CAD preselection highlight, Figma hover outline). In dense scenes this is the single most important selection aid.
- **Lock and hide** prevent selection; locked items show a lock icon in the outliner and do not highlight on hover.

## 7. Selection and undo

Blender HIG, verbatim rules:
- "Whenever scene data selection changes, an undo push should be triggered."
- "Conversely if selection did not change, no undo push should be triggered."
- "Neither should UI data selection changes cause undo pushes, for example selection in the File Browser."

tldraw's refinement: selection changes are recorded in a mode that preserves the redo stack, "so a user can undo, select, copy, and redo back to their position". Figma's principle: "if you undo a lot, copy something, and redo back to the present, the document should not change."

Rule: selecting things must never destroy the redo stack.

## 8. Checklist

- [ ] Every persistent mode is shown by a word, a cursor and one more signal.
- [ ] Every mode exits with Esc and with a visible button.
- [ ] Esc unwinds exactly one level per press.
- [ ] Panning, constraining and snapping toggles are quasimodes (held keys).
- [ ] Press does not start a drag; a 3 to 4 px threshold does.
- [ ] The selection table above is implemented exactly, including press-release on a selected item.
- [ ] Right click on an unselected item selects it first.
- [ ] Active item is visually distinct from the rest of the selection.
- [ ] Creation tools state whether they return to Select, and tools can be locked.
- [ ] Tool settings (next action) and adjust last operation (last action) are in different places.
- [ ] Selection changes push undo for document selection only, and do not clear redo.
