# Case studies: what the best editors teach

Each case: what changed, why, and the rule to steal. Sources are primary where possible (company blogs, release notes, official guidelines).

## Contents

1. Figma UI3 (2024)
2. Blender 2.80 (2019)
3. VS Code UX guidelines
4. Shapr3D: CAD on a tablet
5. Plasticity: keyboard-first direct modeling
6. SolidWorks, Fusion, Onshape: minimizing mouse travel
7. tldraw: the canvas as engineered craft
8. Marking menus at Autodesk (Alias, Maya, Fusion)
9. Gypsy and the end of the editing mode
10. Patterns across all cases

---

## 1. Figma UI3 (2024)

**Goal:** "Center your ideas, not Figma's UI." Balance newcomers and professionals, adapt to newer ways of designing, prepare for Dev Mode and AI. Over two years of iteration, hundreds of approaches.

**What they tried and dropped:**
- A hover-only UI with no panels: sidebars appearing and disappearing made the workspace "too unstable".
- Floating panels (shipped in beta): cramped small screens, designs peeked out distractingly, rulers moved away from the design, and "they slowed people down". Panels were reattached and kept resizable.
- Blend modes behind an icon button: users had to wait for a tooltip to learn the current mode. Final: an inline dropdown appears whenever a non-standard blend mode is set.
- Clip content as a dropdown: added a click. Back to a checkbox.
- Width and height above X and Y: "disrupted muscle memory too much".
- A condensed Auto Layout alignment grid: "moved around too much", reverted.
- A minimal label approach that hurt accessibility ("a deal breaker").

**What shipped:**
- A slim floating toolbar at the bottom of the canvas, which frees the top and gives all Figma products a common structure.
- Resizable, collapsible panels, and Minimize UI (replacing the "blunt and limiting" Hide UI) that collapses side panels but keeps tools reachable.
- Properties panel reordered: component controls first, all layout options unified (W, H, Auto Layout), header row with actions on the selection.
- Optional property labels, nouns with directional tooltips, matching screen reader labels.
- Stronger affordances: input backgrounds, dropdown borders, rounded corners, about 200 hand-drawn icons.
- A unified Actions menu for AI and quick tasks without interrupting work.

**How they ran it:** opt-out during beta so people could "switch back to finish deadline work"; feedback triaged by asking whether criticism was a lasting problem or a reaction to change; crits as 60-minute "speed rounds" with everyone commenting at once; reversed core decisions after launch.

**Rules to steal:**
- Prototype the extreme (no panels at all), then add back what people miss: "get as much signal as possible, then dial back".
- Never hide current state behind an interaction.
- Muscle memory outranks tidiness. Test every reorder with existing users.
- A major redesign of a pro tool ships with an opt-out and a gradual rollout.

## 2. Blender 2.80 (2019)

**Problems:** feature set had outgrown the keyboard, right-click select alienated newcomers and broke with pens and trackpads, the UI competed with the artwork, settings were scattered.

**What changed:**
- **Left click select** became default. Reasons (commit by Brecht Van Lommel and release notes): works well for mouse, trackpad and pen; easier for beginners and people from other software. Right click opens a context menu. Right-click select stays available.
- **Three keymaps:** Blender, Blender 2.7X (fewest changes), Industry Compatible. Fewer default shortcuts so users can assign their own.
- **Toolbar with persistent tools** on the left of the viewport, tool settings bar at the top, full settings in the Tool tab. Rationale: "Tools behave differently from one-shot commands, so they need persistent, visible settings."
- **Adjust Last Operation** panel bottom left, separate from tool settings, to avoid confusing "next" with "last".
- **Status bar** shows mouse and key actions for the current editor, mode and tool, updating while modifiers are held; plus progress, messages and statistics.
- **Workspaces as tabs** (were a dropdown, which cost a click), each tied to a task and optionally a mode; templates for General, 2D Animation, Sculpting, VFX, Video Editing.
- **Properties editor:** mostly one column, subpanels with less common settings collapsed, presets in panel headers, decorators for animated/keyframed/driven/linked/overridden.
- **Popovers** that can be operated in one press-drag-release gesture. **Pie menus** by default for orientation, pivot, view, shading, snap, falloff.
- **Quick Favorites (Q)** and right-click context menus everywhere; any command can be added to favorites from its button.
- **Dark theme and theme-colored icons** so attention stays on the artwork.

**Known friction:** with left-click select, right click opens the context menu rather than tool options (bug report archived "as designed"); W was reassigned to cycle selection tools.

**Blender's eight paradigms** (current Human Interface Guidelines): non-overlapping, non-blocking, non-modal, select then operate, operate then settings, data properties separated from tools, installation free, "Blender is for artists".

**Rules to steal:**
- Separate persistent tools from one-shot operators, and next-action settings from last-action settings.
- Use the status bar as a live, contextual cheat sheet.
- Ship keymap presets for migrants rather than forcing one map.
- Make every property's state (animated, driven, linked) visible at a glance.

## 3. VS Code UX guidelines

**Model:** containers (Activity Bar, Primary and Secondary Sidebar, Editor, Panel, Status Bar) hold items (Views, toolbars, status items). Each toolbar is scoped to exactly one container. Status bar left is workspace scope, right is file scope.

**Rules worth copying verbatim** (from the guideline pages):
- Command palette: clear command names, group in categories, add shortcuts where appropriate; do not overwrite existing shortcuts; no emoji in names.
- Quick picks: use a title for multi-step flows and pickers without text input; always have a placeholder; offer "create new" when picking from a list.
- Views: keep their number minimal; add an icon to every view so it can move to another container; do not use tree items as buttons; no more than three actions per tree item.
- Notifications: only when absolutely necessary, one at a time, always "Do not show again", never promotional.
- Status bar: short labels, icons only for clear metaphors, no custom colors.
- Settings: defaults for every setting, clear descriptions, no custom settings pages.

**Rule to steal:** write your editor's own "contribution guidelines" even if there are no plugins. A container-and-scope model plus a short do/don't list per surface keeps a growing tool coherent.

## 4. Shapr3D: CAD on a tablet

- Founder's rule on the office wall: "Easy should be easy. Hard must not be impossible."
- "A great product is characterized by a minimal tool time."
- Explicit handles: showing push-pull arrows "increases the success rate by two orders of magnitude".
- Physical analogies for every operation; "Explicit is always better than implicit."
- Fingers navigate, Pencil creates (AEC Magazine review). An early multitouch-only version failed at two-handed gestures.
- Selection-driven operations list: the UI proposes only what fits the current selection.
- Direct modeling on a Parasolid kernel, with persistent sketch dimensions; positioned as a conceptual tool by reviewers, with limited precision workflows.
- Process: hundreds of prototypes, professionals invited to break it, "You need to see them fail a thousand times."

**Rule to steal:** if users fail to discover a manipulation, show its handle; do not teach a gesture.

## 5. Plasticity: keyboard-first direct modeling

- Bottom command bar with the core verbs and their keys (F search, G move, R rotate, S scale, Shift+D duplicate, Q boolean), plus Suggested Commands that change with the selection type (solid, sheet, curve, region, point).
- Command palette (F) for everything without a button; assign shortcuts and favorites from the palette itself, with conflicts highlighted in red.
- Selection modes on number keys (edge, face, solid; Tab for all), Ctrl+4 converts a selection to its solids.
- Snapping with a rich point vocabulary and a labeled tip at each target ("Section,Edge"); Ctrl enables snapping temporarily; Shift+X cycles through and disables snap types.

**Rule to steal:** every command in three forms: key, bar button, palette entry. Let users bind keys from where they found the command.

## 6. SolidWorks, Fusion, Onshape: minimizing mouse travel

Three mature CAD tools converged on the same set:
- **Cursor-local command menus:** S key in all three (SolidWorks shortcut bar per mode, with search on double S; Fusion toolbox with search; Onshape shortcut toolbar).
- **Directional gestures:** SolidWorks mouse gestures (right drag, 2 to 12 directions), Fusion marking menu.
- **Context toolbars** near the selection (SolidWorks, separate ones for graphics area and tree).
- **Selection breadcrumbs** (SolidWorks, D to bring them to the cursor).
- **Adaptive but predictable toolbars** (Onshape: collapse into group dropdowns at small sizes, last used tool moves to the front of its group).
- **Customization in place:** right click a toolbar to customize, reset to default.

**Rule to steal:** on big screens, bring commands to the cursor. Every frequent command must be reachable without leaving the work area.

## 7. tldraw: the canvas as engineered craft

Steve Ruiz's blog documents canvas details most tools get wrong:
- Hover areas reviewed across 15 apps: corners vs edges, rotation outside corners, overlap priority, cursor timing.
- Modifier release delayed 150 ms to fix a physical race between key-up and mouse-up.
- Eraser: segment hit testing, screen-pixel margins, preview by transparency, delete on release, Esc restores, follows group boundaries, frames erasable only when entering from outside.
- History with marks, squash, bail, and selection recorded without clearing redo.
- Tools as hierarchical state machines (idle, pointing, dragging), creation tools return to select unless tool lock is on.
- Camera: zoom steps, wheel behavior respecting the user's mouse or trackpad preference, momentum that any user input cancels.

**Rule to steal:** write every canvas interaction as a state machine with explicit cancel paths, and specify hit areas in screen pixels.

## 8. Marking menus at Autodesk

Kurtenbach and Buxton's research (University of Toronto, later Alias and Autodesk) put marking menus into Alias, Maya and Fusion.
- Press and wait 1/3 s for the menu, or mark immediately; the same movement in both, so novices rehearse.
- Reliable limits: 4 items to depth 4, or 8 items to depth 2. Off-axis items are slower and error-prone.
- Field study: the experienced user marked 93 percent of selections; marks 3 to 4 times faster than menus even after removing the wait; experts still pop the menu after breaks to refresh memory.

**Rule to steal:** design fast paths whose learning happens during normal slow use.

## 9. Gypsy and the end of the editing mode

Larry Tesler and Tim Mott's Gypsy editor at Xerox PARC (mid 1970s) replaced command and insert modes with click-drag selection and Cut/Paste keys, borrowing printing-industry terms. Tesler defined a mode as a state that "has no role other than to place an interpretation on operator input", and campaigned for "no modes" for the rest of his career. The ideas went into the Lisa and Macintosh.

**Rule to steal:** before adding a mode, try selection plus an operator.

## 10. Patterns across all cases

| Pattern | Figma | Blender | VS Code | Shapr3D | Plasticity | CAD trio | tldraw |
|---|---|---|---|---|---|---|---|
| Canvas-first layout | UI3, Minimize UI | Dark theme, areas | Zen mode | Full screen viewport | Minimal chrome | Collapsible panels | Infinite canvas |
| Command search | Actions menu (Ctrl/Cmd+K) | F3 menu search | Command palette | Not verified | F palette | S toolbox search | Shortcut dialog only |
| Cursor-local menus | Context menu | Q, Shift+Space, pies | Context menus | Selection-driven list | Suggested commands | S key, gestures | Context menu |
| Live contextual hints | Tooltips with keys | Status bar map | Status bar | Explicit handles | Snap labels | Breadcrumbs | Cursor changes |
| Operate then adjust | Live properties | Redo panel | Undo | Handles | Floating dialogs | Feature dialogs preview | Live drag |
| Keymap presets | International layouts | 3 keymaps | Keymap extensions | Keyboard support | Rebind from palette | Customizable | n/a |
