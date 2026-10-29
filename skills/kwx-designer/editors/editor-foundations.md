# Editor foundations: the anatomy of a pro tool and a method to design one

Master file for designing editors and pro tools (CAD, 3D, design tools, image, video and audio editors, node editors, code editors, canvas apps). Read this first, then open the topic file you need.

## Contents

1. What makes a pro tool different
2. The anatomy: seven regions every editor has
3. The ten laws of editor design
4. Method: designing an editor from zero in eight steps
5. Review checklist (run before shipping any editor screen)
6. Topic files in this folder

---

## 1. What makes a pro tool different

A pro tool is used for hours a day, for years, by people who build muscle memory. That changes the priorities compared with a consumer app:

- **The work is the hero, not the UI.** Figma's UI3 goal was literally "center your ideas, not Figma's UI". Blender 2.80's dark theme exists so "the interface should keep attention on the artwork". Every pixel of chrome must justify itself against canvas space.
- **Speed of the expert matters as much as clarity for the novice.** Shneiderman's direct manipulation paper lists both outcomes as goals: novices learn quickly, experts "work extremely rapidly". Design both paths, never only one.
- **Muscle memory is a feature you can break.** Figma reverted UI3 changes that "looked better on paper" because they "disrupted muscle memory too much" (x and y fields stayed above width and height; the condensed Auto Layout grid was rolled back).
- **Latency is a usability bug.** Under about 0.1 s, users feel they manipulate the object directly (Nielsen's first response time limit). Figma calls performance a feature "you only notice when it isn't there".
- **Errors must be cheap, not prevented by nagging.** Raskin: confirmation dialogs become habitual and stop protecting anyone; universal undo is the real protection.

## 2. The anatomy: seven regions every editor has

Map every editor you design onto these regions. Name them in the spec. If a region is missing, that is a decision, not an accident.

| Region | Job | Typical place | Examples |
|---|---|---|---|
| **Canvas / viewport / document** | The work itself. Largest region, always. | Center | Figma canvas, Blender 3D Viewport, VS Code editor group, Resolve timeline viewer |
| **Tool bar** | Pick the active tool (the verb that the pointer performs) | Left vertical strip or floating bottom bar | Blender toolbar (left of viewport), Figma UI3 bottom toolbar, Photoshop tools |
| **Tool settings / context bar** | Options of the active tool or the current selection, for the NEXT action | Thin strip directly above the canvas | Blender Tool Settings region, Affinity context toolbar, Photoshop options bar |
| **Inspector / properties** | Edit properties of the selected object(s) | Right panel | Figma Design panel, Blender Properties editor, Fusion dialogs |
| **Outliner / layers / tree / browser** | Structure, hierarchy, find and select by name | Left panel (design tools) or top right (Blender) | Figma Layers, Blender Outliner, Fusion Browser, VS Code Explorer |
| **Timeline / history / feature list** | Time or construction order | Bottom strip or left list | Blender Timeline, Fusion parametric timeline, Onshape Feature list with rollback bar |
| **Status bar** | Mode, hints, progress, stats; never primary actions | Bottom edge | Blender status bar shows mouse button hints for the current tool; VS Code status bar |

Plus three floating layers that sit above everything: **command search** (palette), **context menu** (right click), and **transient feedback** (snapping guides, measurement labels, toasts).

Reading the Blender default Layout workspace (manual screenshot): viewport top left about 75 percent of the width, outliner top right, properties bottom right, timeline across the bottom, status bar at the very bottom showing "Select / Box Select / Rotate View / Object Context Menu" next to mouse icons. Lesson: the status bar teaches the mouse map of the current tool all the time, at zero cost to the canvas.

Reading the VS Code architecture diagram (UX guidelines): Activity Bar (view containers) far left, Primary Sidebar, Editor with its own toolbar top right, Panel at the bottom with tabs and a panel toolbar, Status Bar with left items scoped to the workspace and right items scoped to the active file. Lesson: every toolbar is scoped to exactly one container, and its position tells the user its scope.

### Rule: one scope per strip

Every toolbar, header and status item acts on exactly one scope, and its position states that scope.

- Actions on the whole document go in the app header or the menu bar.
- Actions on one panel go in that panel's header (VS Code "View Toolbar").
- Actions on the selection go in the inspector header or a contextual bar near the selection.
- Settings for the next action of the active tool go in the tool settings bar.
- Test: point at any button and say out loud what it acts on. If the answer is "it depends", move it.

## 3. The ten laws of editor design

Each law is testable. The topic files expand each one.

1. **Canvas first.** The canvas takes at least 60 percent of the window area at the default layout on a 1440x900 screen. Panels are resizable and collapsible, and one shortcut hides all of them (Figma Minimize UI, Blender Ctrl+Space to maximize an area). Test: measure the default layout.
2. **Direct manipulation with continuous feedback.** Every drag shows its result live, under 16 ms per frame (60 fps), on the real object, not a proxy box, whenever the cost allows. Shneiderman: "rapid, incremental, reversible operations whose impact on the object of interest is immediately visible". See `canvas-and-direct-manipulation.md`.
3. **Select, then operate.** The default interaction is noun first (select the object), then verb (the action). Raskin: noun-verb interactions are inherently less modal. Blender lists "Select -> Operate" as a core paradigm. Tool palettes (verb first) are the accepted exception for drawing tools. See `tools-modes-selection.md`.
4. **Modes are visible or spring-loaded.** A persistent mode must be impossible to miss (header label, cursor shape, tinted UI, status bar text). Anything that can be a quasimode (hold Space to pan, hold Ctrl to toggle snapping) should be. See `tools-modes-selection.md`.
5. **Operate, then adjust.** Let people act first and tweak the parameters after, with live redo (Blender Adjust Last Operation, F9). Never force a settings dialog before the user has seen any result. See `inspector-and-numeric-input.md`.
6. **Every number is a scrubber, a calculator and a unit converter.** Drag to scrub, Shift and Ctrl for fine and stepped, type an expression (`10/3`, `2ft + 5cm`), Tab to the next field, Esc to cancel. See `inspector-and-numeric-input.md`.
7. **Everything is findable by name.** One command palette contains every command, shows its shortcut next to the result, and is reachable from anywhere with the same key. See `shortcuts-and-command-search.md`.
8. **Novice path rehearses the expert path.** The slow visible method should train the fast invisible one (marking menus: the menu stroke equals the mark). Tooltips and menu items show shortcuts. See `shortcuts-and-command-search.md`.
9. **Nothing is lost.** Universal undo with a visible history, autosave, non-destructive operations where the domain allows (layers, modifiers, parametric features, adjustment layers). Undo restores selection state; selection changes do not destroy the redo stack. See `history-and-nondestructive.md`.
10. **The layout fits the task, and the user can change it.** Workspaces per task (Blender tabs, Resolve pages, Affinity personas). Panels can be moved, resized, saved. Defaults stay excellent because most people never customize. See `panels-workspaces-onboarding.md`.

## 4. Method: designing an editor from zero in eight steps

Use this sequence. Write the output of each step into the spec before drawing anything.

**Step 1. Name the object of interest and its representation.**
What does the user manipulate? Shapes, solids, clips, nodes, text, samples. Shneiderman: the "continuous representation of the object of interest" is principle one. Decide how it looks on the canvas at every zoom level (including when tiny), and what its selected, hovered, locked, hidden and error states look like.

**Step 2. List the verbs and rank them by frequency.**
Write 20 to 60 verbs (move, rotate, extrude, trim, split clip, connect nodes). Mark each as: very frequent (several times per minute), frequent (per session), rare (per week). The ranking drives placement:

| Frequency | Gets |
|---|---|
| Very frequent | Direct manipulation on canvas (drag, handle, gizmo) plus single-key shortcut plus a spot in the toolbar |
| Frequent | Toolbar or context bar button, context menu entry, shortcut with one modifier |
| Rare | Menu bar, command palette, inspector section collapsed by default |

Kurtenbach and Buxton found marks were used for the most frequent commands (r squared 0.81 and 0.88 between frequency and mark use). Frequency is the single best predictor of where a command belongs.

**Step 3. Decide which verbs are tools and which are operators.**
A **tool** stays active and changes what the pointer does on the canvas (Blender: "tools that stay active until you pick another"). An **operator** runs once on the current selection and finishes (Extrude Faces, Flip Horizontal). Tools go in the toolbar, with their settings in the tool settings bar. Operators go in menus, context menus, the palette, and the inspector or context bar. Blender: "Tools behave differently from one-shot commands, so they need persistent, visible settings."

**Step 4. Define the selection model.**
Click, Shift click, drag marquee, click on empty to deselect, double click to enter a group, select through stacked objects, select by type, active versus selected. Write the exact table. See `tools-modes-selection.md`.

**Step 5. Define the modes, and minimize them.**
List every state in which the same input means something different (edit mode, text editing, sketch mode in CAD, pen tool path in progress). For each: how is it entered, how is it shown, how is it exited (Esc always works), and can it be a quasimode instead.

**Step 6. Lay out the regions.**
Place the seven regions. Rules: canvas center; tools on one edge, inspector on the opposite edge (left-to-right reading flow: choose tool, act on canvas, refine on the right); outliner beside the tools in design apps, above the inspector in 3D apps; status bar for hints. Write the default widths: tool strip 40 to 48 px, panels 240 to 320 px resizable, context bar 32 to 40 px tall.

**Step 7. Design the feedback loop for every verb.**
For each frequent verb, specify: hover preview, press feedback, live drag feedback (ghost, measurements, snap guides), commit feedback, undo label. Target under 100 ms from input to visible change, 60 fps during drags.

**Step 8. Design the learning path.**
First-run choices (Blender Quick Setup asks left or right click select, and what Spacebar does), labeled tooltips with shortcuts, status bar hints, empty states that show the first action, a command palette, and optional labels for icon-only panels (Figma UI3 property labels toggle).

## 5. Review checklist

Run this on every editor screen. Each line is pass or fail.

- [ ] Canvas is the largest region and at least 60 percent of the area by default.
- [ ] One shortcut hides or minimizes all panels; another restores them.
- [ ] Every toolbar sits next to the scope it acts on.
- [ ] The active tool is highlighted in the toolbar AND reflected in the cursor shape.
- [ ] The current mode is written in words somewhere visible (header or status bar), not only implied by color.
- [ ] Esc cancels the current drag, closes the current popover, then exits the current sub-mode, in that order, one level per press.
- [ ] Every drag gives live feedback on the real object; nothing jumps on commit.
- [ ] Clicking empty canvas with the default tool deselects all.
- [ ] Every number field: scrub, Shift fine, Ctrl stepped, type expression, accept units, Tab to next, Esc to cancel.
- [ ] Mixed values in a multi-selection display as "Mixed", never as the first object's value.
- [ ] Every command is in the palette and shows its shortcut there.
- [ ] Every tooltip shows the name, a one-line verb-first description and the shortcut.
- [ ] Undo works for every document change, restores the selection, and has a named entry in a history list.
- [ ] Selection changes are not lost by undo-then-redo (redo stack survives selection).
- [ ] Destructive or expensive operations can be canceled mid-way; long jobs show progress and a cancel button.
- [ ] Hit targets for handles stay a constant size on screen at every zoom level.
- [ ] The layout still works at 1280x800 and at 200 percent UI scale.

## 6. Topic files in this folder

- `canvas-and-direct-manipulation.md`: direct manipulation principles, zoom and pan, handles and hit areas, gizmos, snapping and smart guides, feedback and 60 fps, multiplayer presence.
- `tools-modes-selection.md`: tools versus operators, modes and quasimodes, showing the active mode, tool lifecycle, selection models and their exact rules.
- `inspector-and-numeric-input.md`: properties panel structure, mixed values, scrubbing, units, expressions, soft and hard limits, adjust last operation, contextual toolbars.
- `shortcuts-and-command-search.md`: shortcut assignment, international keyboards, modifier timing, discoverability, command palettes, marking and pie menus.
- `history-and-nondestructive.md`: undo model, history panels, multiplayer undo, non-destructive editing, parametric timelines.
- `panels-workspaces-onboarding.md`: panels, docking, workspaces, density, customization, onboarding and progressive disclosure for complex tools.
- `timelines-and-node-editors.md`: time-based editors (video, audio, animation) and node graph editors.
- `cad-specific.md`: CAD and 3D modeling: feature trees, sketches and constraints, gizmos, view cube, selection filters, touch and pencil CAD.
- `case-studies.md`: Figma UI3, Blender 2.80, VS Code, Shapr3D, Plasticity, SolidWorks, tldraw, and what each teaches.

Sources for everything here: `../sources/articles/editors-reading-list.md` and the notes in `../sources/books/`.
