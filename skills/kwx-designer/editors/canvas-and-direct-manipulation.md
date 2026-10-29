# Canvas and direct manipulation

How the canvas itself should behave: representation, navigation, handles, gizmos, snapping, feedback and performance.

## Contents

1. Direct manipulation: the four principles as design rules
2. Zoom and pan conventions
3. Selection handles and hit areas
4. Gizmos in 3D
5. Snapping and smart guides
6. Live feedback during a drag
7. Performance perception
8. Canvas backgrounds, grids and empty states
9. Presence and multiplayer on the canvas
10. Touch and pen on the canvas

---

## 1. Direct manipulation: the four principles as design rules

Shneiderman (1983) defined direct manipulation by four principles. Turn each into a check:

| Principle (Shneiderman) | Design rule | Test |
|---|---|---|
| Continuous representation of the object of interest | The object is always visible while being edited. Dialogs never cover it. Properties panels never overlap the canvas content being edited. | Open every dialog and popover while an object is selected. Is the object still visible? |
| Physical actions instead of complex syntax | Frequent operations are drags, clicks and handles, not typed commands. Typing is the precision path, not the only path. | Can you move, resize, rotate, reorder and connect without the keyboard? |
| Rapid, incremental, reversible operations whose impact is immediately visible | Every drag updates the object live, every step can be undone, partial results are shown as you go. | Drag something slowly. Does the object update every frame? Undo it. Is it exactly back? |
| Layered learning | A small set of basic actions works on day one; advanced ones layer on top without changing the basics. | Can a new user finish a basic task using only the default tool, drag and the inspector? |

Shneiderman's warnings, also as rules:
- **Icons are not automatically clearer than words.** "A graphic icon, although meaningful to the designer, may require as much or more learning time as a word." Label rare icons, or make labels optional (Figma UI3).
- **Graphic representations can eat space.** "For experienced users, a tabular textual display of 50 document names is far more appealing than only 10 document graphic icons." Offer a dense list view next to any thumbnail grid (layers, assets, files).
- **Do not mix metaphors.** "Mixing metaphors from two sources adds complexity."

Bret Victor's extension (Inventing on Principle): creators need an immediate connection to what they make. Concretely:
- If a parameter affects the canvas, dragging it updates the canvas live. No "Apply" button for anything that can be previewed.
- If behavior unfolds over time (animation, physics, playback), show it across time: onion skins, motion paths, a trail of future positions. "You need to be able to see across time, otherwise you're designing blind."
- Show the data. Show comparisons: hovering an alternative value previews it against the current one.

## 2. Zoom and pan conventions

These are the conventions users bring from Figma, Sketch, Illustrator, Miro, tldraw and Blender. Match them unless you have a strong reason.

### 2.1 Input mapping (2D canvas)

| Input | Action |
|---|---|
| Space held + drag | Pan (quasimode: release Space returns to the previous tool) |
| Middle mouse drag | Pan |
| Trackpad two finger scroll | Pan |
| Trackpad pinch | Zoom around the pinch center |
| Ctrl/Cmd + wheel | Zoom around the cursor |
| Plain mouse wheel | Pan vertically (design tools) OR zoom (whiteboards, maps). Pick one, and expose a "Mouse / Trackpad" preference |
| Shift + wheel | Pan horizontally |
| Ctrl/Cmd + `+` / `-` | Zoom in/out in steps, centered on the viewport center (or the selection if any) |
| Shift+0 or Ctrl/Cmd+0 | Zoom to 100 percent |
| Shift+1 | Zoom to fit all content |
| Shift+2 | Zoom to fit selection |
| Z tool / Z held + drag | Marquee zoom or scrubby zoom |

Rules:
- **Zoom toward the cursor, never toward the viewport center, for wheel and pinch.** The point under the cursor stays under the cursor. Test: put the cursor on a corner of an object, zoom in five steps. The corner must not move on screen.
- **Use discrete zoom steps for keyboard zoom** and continuous zoom for wheel and pinch. tldraw's default steps are `[0.1, 0.25, 0.5, 1, 2, 4, 8]`; the first and last are the clamps.
- **Clamp zoom** (for example 2 percent to 25600 percent in Figma class tools) and show the current zoom as an editable percentage, which also opens a zoom menu.
- **Do not auto-detect mouse versus trackpad silently.** Miro's auto-switch is the top source of "the wheel randomly zooms, then scrolls" complaints. Default to a sensible mode, detect if you want, but show the choice in preferences and let the user lock it.
- **Panning has momentum on trackpads only**, and any new user input stops the slide (tldraw: user pan or zoom input stops programmatic animations).
- **Animated camera moves** (zoom to fit, zoom to selection) last 200 to 300 ms with ease out. Instant for very frequent ones if users ask, never longer than 400 ms.
- **The canvas never scrolls on its own** while the user is not dragging. Edge autoscroll during a drag near the viewport edge is allowed and expected.

### 2.2 3D viewport navigation

| Input (Blender default) | Action |
|---|---|
| Middle mouse drag | Orbit |
| Shift + middle drag | Pan |
| Wheel / Ctrl + middle drag | Zoom (dolly) |
| Numpad 1 / 3 / 7 | Front / right / top view; Ctrl inverts |
| Numpad period, or "Frame selected" | Center view on selection |
| Home | Frame all |

Rules:
- **Offer navigation presets for people coming from other tools.** Blender ships "Industry Compatible" keymap; Plasticity and Fusion have navigation style preferences (Blender, Maya, SolidWorks, Fusion). A preset is one dropdown, not a remapping project.
- **Show an orientation widget** (view cube or axis gizmo) in a fixed corner. Clicking a face or axis snaps the view; dragging it orbits. Blender's navigation gizmo also has buttons for zoom, pan, camera and perspective toggle, which makes navigation possible with a one-button trackpad.
- **Orbit around the selection or the point under the cursor**, offered as a preference ("orbit around selection"). Orbiting around the world origin while the object is far away is the most common 3D navigation frustration.
- **Never lose the object.** Offer "frame selected" in the view menu with its shortcut displayed, and in the context menu.

## 3. Selection handles and hit areas

Sources: tldraw's "exhaustive review of design tool hover areas" and Bjango's "Design tool canvas handles". Both mapped every app's hit zones by moving the cursor in a grid.

### 3.1 Rules

- **Hit areas are in screen pixels, not document units.** A handle is the same grabbable size at 10 percent and at 3200 percent zoom. (tldraw sets its eraser margin "in screen pixels, so it feels the same size at any zoom level"; do the same for every hit test.)
- **Visual handle size and hit area are different numbers.** Draw corner handles about 6 to 8 px; make their hit areas at least 16 px (24 px or more on touch, at least 44 pt on iPad).
- **Resize along the whole edge**, not only from the midpoint handle. Bjango: full-side resizing (Figma, Sketch) is preferred and "I see no reason not to" when the space is unused.
- **Corner resize beats edge resize where they overlap.** Edges must never overlap each other (tldraw marks Framer and Miro down for overlapping edges).
- **Put rotation just outside the corner**, as an arc or square hugging the corner (Figma, tldraw, Framer), so rotation needs no modifier and no separate knob. If you add a knob, keep the outside-corner zone too.
- **Show the cursor that matches the zone on hover, before the press.** Bjango: "The only way to know if you can perform an action is to hover near the edge of a selected shape and note cursor changes." Most tools change the cursor only after the press starts (tldraw review); do better and change it on hover.
- **Respect the grab offset.** When the user presses inside a handle off-center, the drag must not jump to center the handle on the cursor. Photoshop and Affinity get this right; Figma, Sketch and Illustrator jump (Bjango).
- **Small objects keep their handles usable.** Options in order of preference: (1) enlarge the handle frame outside the object so all handles stay reachable (Sketch, Flinto); (2) hide resize and rotate handles and allow only move (Figma); never (3) let handles stack on top of each other (Illustrator, Affinity, Photoshop).
- **Drop secondary handles when they do not fit.** Corner radius handles disappear on small objects in every app that has them.
- **Resolve overlapping zones with one fixed priority** and document it: active handle > corner resize > rotation > edge resize > object body > objects behind.

### 3.2 Handle states

| State | Look |
|---|---|
| Idle selection | Thin 1 px accent outline, white filled square handles with accent border |
| Hover over handle | Cursor changes; handle can grow by 1 to 2 px |
| Dragging | Handles of other corners hide or fade; dimension label appears near the cursor (W x H, or angle) |
| Locked object | No handles; outline uses a neutral color; a lock badge on hover |
| Multi-selection | One shared bounding box with handles; each item gets a thinner outline |

## 4. Gizmos in 3D

A gizmo is a handle in 3D: arrows for move, rings for rotate, cubes for scale.

- **Color by axis, always X red, Y green, Z blue.** Never reuse those three colors for anything else in the viewport.
- **Constant screen size.** Gizmos scale with distance so they stay the same size on screen.
- **Explicit beats hidden.** Shapr3D's founder: showing the push-pull handles explicitly "increases the success rate by two orders of magnitude" compared with hiding them. If an operation can be done by dragging, show the thing to drag.
- **Plane handles** (small squares between two axes) move in a plane; the center sphere or the view ring moves in screen space.
- **Gizmo shows the active transform orientation** (Global, Local, Normal, View) and its label is visible in the header (Blender's Transform Orientation dropdown).
- **Gizmo is optional for experts.** Blender users can hide gizmos and use G/R/S plus axis keys; the viewport gizmo toggle sits in the header.
- **Tool gizmos belong to tools.** Blender: "Some tools define gizmos (Shear and Spin for example) to help control them." The gizmo appears only while its tool is active.

## 5. Snapping and smart guides

### 5.1 What to snap to (2D design tools)

In order of how often people expect it: pixel grid, edges and centers of other objects, equal spacing between objects, parent frame edges and center, layout grid columns, guides. Smart guides are colored lines (Figma uses red/pink) that appear only while dragging and only for the active match, with distance labels.

### 5.2 What to snap to (CAD and 3D)

Vertex, edge, edge midpoint, face, face center, perpendicular, tangent, intersection, grid, increment (Blender: "an imaginary grid that starts at the selection's original location"), and axis planes. Plasticity's list is a good reference: for curves alone it offers Beginning, End, Middle, Closest, Intersection, Center, 1/4, 3/4, Perpendicular, Tangent.

### 5.3 Rules

- **Snapping is on by default where precision matters** (CAD sketches, UI design) and toggled from a visible button in the header with a shortcut (Blender: magnet icon, Shift+Tab for the menu).
- **Invert snapping with a held modifier**, as a quasimode. Blender and Plasticity: hold Ctrl to toggle snapping temporarily. Figma: hold Ctrl/Cmd while dragging to suppress. Pick one modifier and use it in every tool.
- **Show what you snapped to, by name.** Plasticity shows a dot plus a tip label ("End", "Section,Edge"). Blender draws the target. Unlabeled snapping makes users distrust it.
- **Snap distance is in screen pixels** (about 5 to 8 px), constant across zoom.
- **Let users cycle candidates when several overlap.** Plasticity: pressing Shift+X repeatedly cycles and disables snap types until the right one remains.
- **Choose the snap base explicitly** for 3D: closest, center, median, active (Blender's Snap Base). Show it in the snapping popover.
- **Never snap silently to something off screen.** Guides that point to an off screen object should not appear.
- **Snapping must not fight the user.** If the user is moving the pointer slowly and steadily past a snap point, release the snap after the threshold; never trap the object.

## 6. Live feedback during a drag

For every drag interaction, specify all five moments:

1. **Hover:** cursor shape, highlight of the target (outline of the object or handle under the pointer, Figma's blue hover outline).
2. **Press:** immediate state change (handle fills, object lifts) within one frame.
3. **Drag threshold:** 3 to 4 px on mouse, 8 to 10 px on touch before a press becomes a drag. Below it, release is a click.
4. **Drag:** the real object moves, smart guides and a measurement label follow, other handles fade. Values in the inspector update live.
5. **Commit or cancel:** release commits as one undo step. Esc during the drag cancels and restores the exact previous state (tldraw "bails back to a history mark"). Right click during a drag also cancels (Blender convention).

Rules:
- **Preview destructive actions before they commit.** tldraw's eraser renders marked shapes semi-transparent during the stroke and deletes only on release; Esc restores them.
- **Lightweight effects can trigger mid-gesture; destructive ones only on release** (Rauno Freiberg on gesture timing).
- **Hit testing for fast strokes uses segments, not points.** tldraw tests "the segment from the previous position to the current one, so fast strokes don't skip shapes". Apply to lasso, eraser, brush and paint selection.
- **Modifiers can change mid-drag.** Shift constrains to an axis or aspect ratio, Alt/Option duplicates or scales from center, the effect is added or removed at any time during the drag (tldraw).
- **Delay modifier release by about 150 ms** before applying it, so releasing Shift and the mouse button at nearly the same time does not drop the constraint at the last frame (tldraw's "physical race condition" fix: they "went with 150ms").
- **Show numeric feedback next to the cursor**, not only in the inspector: "W 240 H 120", "45 degrees", "12.5 mm". The eye stays on the locus of attention.

## 7. Performance perception

- **Under 100 ms from input to visible change** (Nielsen: the limit for feeling that you directly manipulate the object). Above 1 s the user loses flow; above 10 s they leave the task.
- **60 fps during drags, pans and zooms, and 120 fps on displays that support it.** Drop detail before dropping frames: render proxies, skip shadows and blurs, show low resolution tiles, then refine on idle.
- **Apply local edits immediately, sync later.** Figma's multiplayer applies changes locally "instead of waiting for acknowledgement from the server", and discards conflicting server echoes so values do not flicker.
- **Long operations run in the background with progress and cancel.** Blender's paradigm "Non Blocking": tools should not stop you from using other parts of the app; where blocking is unavoidable (render, simulation) it "should be clearly indicated and allow an immediate exit". Blender's status bar shows a progress bar with a time estimate on hover and a cancel button.
- **Never show a modal progress dialog for anything under 2 s.** Use the cursor, a status bar spinner, or an inline progress bar.
- **Frequent, low-novelty actions get no animation** (Rauno Freiberg: command menus, context menus, the app switcher). Panels and menus open instantly or within 100 to 150 ms.
- **Performance budget is a design artifact.** Write it in the spec: "drag of 1000 objects at 60 fps on a 2021 laptop". Figma treats performance as "one of our most important features".

## 8. Canvas backgrounds, grids and empty states

Blender HIG rules, adopt them:
- "If the exact coordinates of items in an editor matter, the editor should draw a grid background" (UV editor, graph editor). If only one axis matters, draw the grid along that axis only (dopesheet, timeline).
- "If the exact coordinates of items in an editor with scrolling on two axes does not matter, the editor should draw a dotted grid" (node editor), so the user still sees that the view is moving when it is empty.
- Grid density adapts to zoom: subdivide when cells get larger than about 80 px on screen, merge when smaller than about 8 px.

Empty canvas:
- Show one sentence and the first action ("Press R to draw a rectangle, or drop an image here"), centered, in the muted text color, gone as soon as anything exists.
- Never show a blank infinite canvas with nothing to orient the user; at minimum the dotted grid.

## 9. Presence and multiplayer on the canvas

- Each collaborator gets a colored cursor with their name in a label that fades after a few seconds of no movement.
- Their selection shows as an outline in their color, so two people do not edit the same thing unknowingly.
- Follow mode (click an avatar to follow their viewport) must be obvious to enter and to leave: a colored frame around the whole canvas plus "Following Anna, Esc to stop".
- Cursor chat is live with no send step (Figma cursor chat: "there is no action to confirm or send your message"); Esc or clicking the canvas exits.
- Multiplayer undo only undoes your own changes (see `history-and-nondestructive.md`).
- Last writer wins per property is acceptable for design tools (Figma). Do not merge text keystrokes from two people into one field.

## 10. Touch and pen on the canvas

- **Split roles by input device.** Shapr3D (per AEC Magazine's review): fingers navigate (spin, pan, zoom), the Pencil creates and edits. This kills the pan-or-draw ambiguity.
- **Do not depend on two-handed gestures for core actions.** Shapr3D's founder: an early multitouch-only version failed, "when they reached two-handed gestures, most people failed".
- **Treat a second finger as a modifier**, mapped to the same code path as Shift (tldraw prototype). Do not build a parallel gesture system.
- **Do not assume finger and pen events arrive together.** tldraw found that once a pen touches the screen the OS can stop sending finger events entirely (palm rejection). Detect pen and touch separately, never infer device type from one API.
- **Touch hit areas at least 44 pt.** Handles and gizmo grips get a larger invisible grab zone on touch.
- **Long press replaces hover** for previews and tooltips; never put essential information only on hover.
