# CAD and 3D modeling specifics

Rules for mechanical CAD (Fusion, Onshape, SolidWorks, FreeCAD), direct modelers (Shapr3D, Plasticity, SketchUp) and polygon tools (Blender). Read `editor-foundations.md` first.

## Contents

1. The CAD screen, region by region
2. Parametric versus direct modeling: what each needs from the UI
3. Feature tree and timeline
4. Sketch mode
5. Constraints and dimensions
6. Selection in 3D: filters, preselection, breadcrumbs
7. Numeric input during an operation
8. View navigation and orientation
9. Feature dialogs and live preview
10. Errors and rebuild failures
11. Touch and pencil CAD
12. Checklist

---

## 1. The CAD screen, region by region

| Region | Fusion | Onshape | SolidWorks | Blender | Rule |
|---|---|---|---|---|---|
| Command access | Toolbar tabs by workspace + S toolbox + marking menu | Context toolbars (Feature, Sketch, Assembly) + S shortcut toolbar + search | CommandManager tabs + S shortcut bar + mouse gestures | Toolbar per mode + menus + F3 search + pies | Give three paths: toolbar, cursor-local menu, search |
| History | Timeline at the bottom | Feature list on the left with rollback bar | FeatureManager tree on the left | Modifier stack in Properties | Always visible in the default layout |
| Structure | Browser (components, bodies, sketches) | Feature list doubles as tree; Assembly list | FeatureManager tree | Outliner | Hierarchy and history can share a panel but must be distinguishable |
| Properties | Floating feature dialog | Feature dialog over the list | PropertyManager replacing the tree | Properties editor + redo panel | Dialog stays beside the canvas, never covers the model |
| Orientation | ViewCube top right | View cube top right | View triad bottom left + heads-up view toolbar | Navigation gizmo top right | Fixed corner, clickable faces |

## 2. Parametric versus direct modeling

| | Parametric (Fusion, Onshape, SolidWorks, FreeCAD) | Direct (Shapr3D, Plasticity, SketchUp) |
|---|---|---|
| Truth | The feature list; geometry is its result | The geometry itself |
| Key UI | Timeline or tree, rollback, feature dialogs, sketch constraints | Push/pull handles, selection-driven commands, snapping |
| Strength | Design intent, editable history, families of parts | Speed, exploration, low learning cost |
| UI risk | Broken references, rebuild errors, history anxiety | Hard to change early decisions, weaker precision intent |

Rules:
- **Say which model a document uses.** Fusion has an explicit Parametric versus Direct modeling mode; in Direct mode "Fusion does not track features parametrically". Show the mode in the header or timeline area.
- **Direct tools still need numeric precision.** Shapr3D keeps persistent sketch dimensions and constraints; Plasticity snaps to a long list of geometric points. Direct does not mean imprecise.
- **Hybrid is the trend:** push and pull faces without managing history, but keep dimensions that persist through later edits (Shapr3D).

## 3. Feature tree and timeline

- **Each feature row:** type icon, name (renamable), and state (suppressed, error, warning) visible without hovering.
- **Rollback marker** is a distinct, draggable control (Fusion's timeline marker, Onshape's rollback bar). Dragging shows the model at that point; nothing is deleted. New features insert at the marker.
- **Marker position must be obvious.** If the user is not at the end, tint the timeline after the marker and show "Rolled back: 4 features hidden". (Fusion forum threads complain about the marker disappearing off the visible part of a long timeline; keep it pinned in view.)
- **Play controls** step through features one at a time (Fusion), which doubles as a teaching aid for inherited files.
- **Edit feature by double click** on the row or on the geometry it produced; the model rolls back temporarily to that feature and shows the downstream result live.
- **Hover a feature row, highlight its geometry** in the viewport; hover geometry, highlight its row.
- **Group features into folders** and collapse them; long trees are the norm.
- **Show dependents before deleting:** list the features that reference this one.
- **Reorder by drag** with a live validity check (red insertion line where a reorder would break references).

## 4. Sketch mode

Sketch mode is the most important persistent mode in CAD. Show it loudly:
- Header label "Sketch 3 on Top plane", a toolbar that swaps to sketch tools (Onshape swaps the Feature toolbar for the Sketch toolbar), the view optionally rotating normal to the sketch plane, out-of-sketch geometry dimmed, and a big "Finish sketch" button (check mark) plus Esc.
- **Entering:** select a face or plane, then Sketch. Shapr3D: double tap a face with a finger to look at it and start sketching.
- **Inference while drawing:** show horizontal, vertical, coincident, tangent, midpoint inferences as small glyphs at the cursor before click, and apply them as constraints on click. Let a modifier suppress inference.
- **Construction geometry** is a toggle on any sketch entity, drawn dashed.
- **Projected/derived geometry** from the model is drawn in a distinct color and updates when its source changes.
- **Closed profiles are filled** lightly so users see what can be extruded; open or self-intersecting profiles show the problem location.

## 5. Constraints and dimensions

- **Color by definition state**, the near-universal convention: under-defined geometry is blue, fully defined is black (or white on dark themes), over-defined or conflicting is red. Show a status text too: "Fully defined" or "3 degrees of freedom" (SolidWorks shows the state in the status bar).
- **Constraint glyphs** sit next to the geometry they bind, hide when the sketch is dense, and show on hover. Clicking a glyph selects the constraint; Delete removes it.
- **Dimensions are edited on the canvas.** Click a dimension value, type, Enter. The value field accepts expressions, units and parameter names (Fusion user parameters, Onshape variables).
- **Dimension placement follows the cursor** after selecting the geometry; the type is inferred from the selection (one line gives a length; two lines give a distance or angle, as Shapr3D does).
- **Driven (reference) dimensions** are drawn in a different color or in parentheses and cannot be edited.
- **Conflicts are explained, not just colored.** When adding a constraint would over-define, show which existing constraints conflict and offer to make the new one driven.
- **Dragging under-defined geometry** moves it live within its remaining freedom; this is the fastest way for users to understand what is not yet constrained.

## 6. Selection in 3D: filters, preselection, breadcrumbs

- **Preselection highlight** on hover is mandatory: the face, edge or vertex that a click would select lights up before the click.
- **Selection filter** for element type (vertex, edge, face, body, component, sketch), visible in the header. Plasticity maps them to number keys (2 edge, 3 face, 4 solid, Tab for all); Blender Edit Mode uses 1, 2, 3 for vertex, edge, face.
- **Convert selection** between levels (Plasticity Ctrl+4 selects the solids of the current selection; in Blender, switching between vertex, edge and face mode converts the current selection). Provide "grow", "shrink", "select loop", "select linked".
- **Selection breadcrumbs** (SolidWorks): when a face is selected, a strip shows face, feature, sketch, body, part, subassembly, assembly; click any crumb to select that level; D brings the strip to the cursor. Use this pattern in every tool with deep hierarchy.
- **Select other / cycle** for overlapping entities at the same pixel: a key or a small list near the cursor (SolidWorks Select Other, Blender Alt+click menu).
- **Toggle selection model** is acceptable in CAD (Onshape: click toggles, no modifier needed) because features need many entities. Be consistent across the whole product.
- **Selection count and type** appear in the status bar ("3 edges, 1 face").

## 7. Numeric input during an operation

The fastest precise workflow in 3D is: start the operation, type the value, confirm. Blender's numeric input is the reference:
- Press G (move), type `2`, Enter: moves 2 units along the default axis. X, Y, Z keys lock the axis (press twice for local axis). Tab moves to the next component: `G 1 Tab 1 Tab 1` moves one unit on each axis.
- Minus negates, slash takes the reciprocal (`2 /` gives 0.5), Backspace resets, then cancels numeric entry back to mouse control.
- Advanced mode (`=` or numpad `*`) accepts units and expressions (`cm`, `deg`, `pi`, `sqrt`).
- The typed value is shown live in the viewport footer or header.

Rules for any 3D or CAD tool:
- **Typing a number during a drag switches the drag to numeric entry** without opening a dialog. The object updates as you type.
- **The value field appears next to the cursor or the gizmo,** not only in a side panel (Fusion and Shapr3D show an inline value box on the manipulator arrow).
- **Axis keys work mid-operation** and the locked axis is drawn as a colored infinite line.
- **Enter confirms, Esc or right click cancels**, always.

## 8. View navigation and orientation

- **View cube or navigation gizmo** in a fixed corner. Click faces, edges and corners for standard and isometric views; drag to orbit; a home button resets.
- **Named standard views** on number keys or a pie menu (Blender numpad 1, 3, 7; Blender's View pie with ` key).
- **Look at / normal to** a selected face (SolidWorks Normal To, Shapr3D double tap on a face).
- **Orbit pivot** around the selection or the point under the cursor, as a preference.
- **Perspective versus orthographic** toggle visible in the view widget; orthographic by default for sketching, with automatic switch when snapping to a standard view (Blender "Auto Perspective").
- **Section view and isolate** are frequent in CAD: a one-click isolate of the selection (Plasticity Focus and Isolate, Blender local view with `/`), and a section plane with a draggable gizmo.
- **3D mouse (SpaceMouse) support** for professionals; Shapr3D supports SpaceMouse on desktop.

## 9. Feature dialogs and live preview

- **Dialog beside the model, not over it**, with the first field focused and the first selection field active.
- **Field types are distinguishable:** Onshape uses a solid blue field for "expects a selection in the graphics area" and a blue outline for "expects keyboard input". The active selection field is highlighted and lists its picked entities, each removable.
- **Live preview** of the feature on the model while the dialog is open, with a distinct preview color (semi-transparent, or green for add and red for cut).
- **Direction flip and type switches** (new body, join, cut, intersect) are small toggles in the dialog AND handles on the model.
- **Drag handles on the preview** update the dialog values, and dialog values update the handles: two views of one parameter.
- **OK, Cancel and "OK and repeat"** (apply and start the same feature again).
- **The dialog remembers last values** per feature type, which users then adjust.

## 10. Errors and rebuild failures

- **Show the failure on the feature row and on the model**, with a clear reason in plain words, not only an error code. Onshape uses color-coded feedback, messages and constraint icons.
- **Never block with a modal error** after a rebuild; the user needs to see the model and the tree to fix it.
- **Offer the fix:** "Reference lost. Reselect face" opens the feature with the broken field highlighted.
- **Tolerances and units** are document settings shown in the document properties, not hidden in preferences.
- **Long recomputes show progress and stay cancelable** (Blender non-blocking paradigm).

## 11. Touch and pencil CAD

Lessons from Shapr3D (Apple Design Award 2019) and its reviews:
- **Fingers navigate, the pencil creates and edits.** No ambiguity between drawing and orbiting.
- **Show handles explicitly**: push/pull arrows on faces drag to extrude outward and cut inward; draft-angle glyphs appear on extrudes. Explicit handles raised the success rate "by two orders of magnitude".
- **Selection-driven commands:** select one face to see offset, move, extrude, cut; add an edge to see revolve and loft. The UI proposes only what is valid.
- **Avoid two-handed gestures as the only path;** "when they reached two-handed gestures, most people failed".
- **Physical analogies:** "The best interactions are always the ones that have physical analogies." Use the pencil like a pencil (draw a line, scribble to erase), not like a mouse.
- **Hit areas grow on touch**, and the snap radius grows with them.
- **Keep a keyboard path** for iPad users with keyboards (shortcuts, numeric entry).

## 12. Checklist

- [ ] Parametric or direct mode is stated in the UI.
- [ ] History is visible by default, with an obvious, pinned rollback marker.
- [ ] Hover links feature rows and geometry both ways.
- [ ] Sketch mode shows a label, a swapped toolbar, dimmed context and a Finish button.
- [ ] Constraint state is shown by color (blue/black/red) AND by text.
- [ ] Dimensions are editable on the canvas with expressions, units and parameters.
- [ ] Preselection highlight on hover, element filters in the header with number keys.
- [ ] Breadcrumbs or select-parent exist for deep hierarchies.
- [ ] Typing during a transform starts numeric entry; axis keys lock axes.
- [ ] View cube in a fixed corner; frame selected and isolate are one key.
- [ ] Feature dialogs preview live, never cover the model, and distinguish selection fields from value fields.
- [ ] Rebuild errors appear on the feature and the model with a plain-language reason and a fix action.
