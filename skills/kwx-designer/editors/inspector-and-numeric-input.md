# Inspector and numeric input

The properties panel, number fields, units, expressions, and the "operate, then adjust" pattern.

## Contents

1. Inspector structure
2. Section order: the Figma UI3 lesson
3. Multi-selection and mixed values
4. Number fields: the full behavior spec
5. Units and expressions
6. Limits, defaults and reset
7. Property state decorators
8. Operate, then adjust (redo panel)
9. Contextual toolbars and popovers
10. Labels, icons and density in panels
11. Checklist

---

## 1. Inspector structure

- **The inspector shows the active selection, never a stale one.** Its header names what is selected ("Frame", "3 layers", "Cube") and holds actions on the selection (Figma UI3's header row of actions on the selected object).
- **Nothing selected shows document or canvas properties** (background, grid, units), never an empty panel.
- **Sections are collapsible, with a stable order.** Collapsing remembers per section type, not per object.
- **Subpanels hold less common settings, collapsed by default** (Blender 2.80 Properties editor). Expanded by default only when users need them most of the time (Figma expanded constraints by default after launch feedback).
- **Mostly one column of controls with labels on the left**, values aligned on a shared vertical line (Blender 2.80 moved "mostly to a single column"). Pair fields side by side only for true pairs: X/Y, W/H, start/end.
- **Separate data properties from tools.** Blender paradigm: property panels edit data directly; tool panels act on selections. Do not put "Apply to all" actions among plain properties.
- **Presets live in the section header** (Blender moved presets into panel headers) as a small dropdown, not as a separate panel.
- **Never require Apply.** Changes are live. If an operation is expensive, preview it at lower quality during the drag and refine on release.

## 2. Section order: the Figma UI3 lesson

Figma reordered its properties panel for UI3 and tested the results. What they learned:
- **Put what users touch most first.** Component controls (variants, instance properties) moved above color and size, because components became central to the work.
- **Group by the user's mental task, not the data model.** Width, height and Auto Layout were merged into one Layout section.
- **But do not break muscle memory for marginal gains.** Putting W and H above X and Y "disrupted muscle memory too much", so X and Y stayed on top. A condensed alignment grid "moved around too much" and was reverted.
- **Do not hide current state behind an icon.** An early UI3 build put blend modes behind an icon button; users had to hover for a tooltip to learn the current mode. The fix: show an inline dropdown whenever a non-default blend mode is set. Rule: a non-default value must be visible without interaction.
- **Do not add a click to a binary choice.** Clip content went from checkbox to dropdown in beta (one more click), then back to a checkbox.

Process rule: order sections by observed frequency of edits, then freeze the order. Any later reorder must pass a test with existing users.

## 3. Multi-selection and mixed values

- When selected objects differ in a property, show **"Mixed"** (placeholder text in the field), never the first object's value.
- Typing into a Mixed field sets all selected objects to that value.
- Scrubbing a Mixed field applies a relative delta to each object (each keeps its own offset), and the field shows the delta while dragging.
- Expressions in multi-edit can be relative: typing `+10` adds 10 to each.
- Sections that apply to only some of the selected types are hidden, or shown with "Applies to 3 of 5" in the section header.
- **Edit all selected from one field:** Blender holds Alt while editing to apply to all selected objects, and offers "Copy to Selected" in the field's context menu. Make the default for multi-selection "applies to all", and offer "only active" in the context menu.
- **Edit several fields at once:** Blender's multi-value editing: press on the first field and drag vertically across X, Y, Z, then drag horizontally to change all, or release and type one value for all.

## 4. Number fields: the full behavior spec

This is the reference behavior, combining Blender's input fields manual, Figma, and the conventions of every pro tool. Implement all of it.

| Input | Behavior |
|---|---|
| Hover | Cursor becomes horizontal resize (or a scrub cursor) over the label or the field; stepper arrows appear on the sides (Blender shows < and > on hover) |
| Press + drag horizontally on the label or field | Scrub: value changes continuously. 1 px of movement = one step unit (fine) by default |
| Shift while scrubbing | Precision: 10x finer (Blender: Shift for precision) |
| Ctrl/Cmd while scrubbing | Snap to discrete steps (Blender: Ctrl snaps to steps). In some apps Shift means 10x coarser; pick one convention and document it in the tooltip |
| Click without drag | Enter text editing with the whole value selected |
| Enter or click outside | Commit |
| Esc (or right click in Blender) | Cancel, restore the old value |
| Tab / Shift+Tab | Commit and move to the next / previous field, in reading order |
| Up / Down arrow keys while editing | Step by 1; Shift + arrow steps by 10 (Figma convention) |
| Ctrl + wheel while hovering | Step the value without clicking (Blender) |
| Minus key while hovering | Negate the value (Blender) |
| Backspace while hovering | Reset to default (Blender, via "Reset to Default Value") |
| Ctrl+C / Ctrl+V while hovering | Copy and paste the value without entering the field (Blender) |
| Drag the label onto another field | Not standard; do not invent this |

Rules:
- **Pointer lock while scrubbing.** Hide the cursor and use relative motion so the scrub does not stop at the screen edge; show the cursor again where the drag started.
- **Scrub sensitivity is in screen pixels per unit**, configurable per field (Base UI calls it `pixelSensitivity`). Angles: 1 degree per px. Opacity: 1 percent per px. Lengths: one display unit step per px at the current precision.
- **Scrub updates the canvas live** at 60 fps, and the whole scrub is one undo step.
- **The scrub handle is the label.** Make labels and leading icons ("W", "H", the radius icon) the scrub target, so clicking the number itself still edits text. Figma users rely on label scrubbing and complain loudly when a field lacks it.
- **Committed text is reformatted** to the field's display precision and unit (`10/3` becomes `3.33`), but full precision is stored.
- **Invalid input never clears the value.** Show the field in an error state with a tooltip, keep the old value, and let Esc restore.
- **Steppers are optional.** Show them on hover only, or hide them entirely in dense panels (Spectrum NumberField has a `hideStepper` option). Never let steppers eat the width the digits need.
- **Right-align numbers or left-align them consistently**, monospaced or tabular figures so digits do not jump while scrubbing.

## 5. Units and expressions

- **Every numeric field accepts arithmetic:** `+ - * / ( )` at minimum. Blender evaluates full Python math: `3*2`, `10/5+4`, `pi`, `sqrt(2)`.
- **Every length field accepts units** and converts to the document unit: `1cm`, `3mm`, `2ft`, `5'`, `3"`, mixed expressions like `2.2mm + 5' / 3" - 2yards` (Blender). Plurals are accepted (`meter`, `meters`).
- **A number without a unit uses the document's default unit.** State the unit in the field suffix ("12 mm", "45°") so users know which one.
- **Units are a document setting** with a visible location (Blender scene units, Fusion document units, Onshape workspace units).
- **Angles accept `deg` and `rad`.** Percent fields accept `%` or a bare number.
- **Expressions can become live links** for advanced users: Blender: an expression starting with `#` creates a driver (`#frame`). CAD: parameters and user variables (Fusion `d1 = width / 2`, Onshape variables) let one value drive many. Show a field that holds an expression with a distinct style (Blender drivers are purple) and show the expression on hover or focus.
- **Relative operators in multi-edit:** `+10`, `-5`, `*2` apply to each selected object.

## 6. Limits, defaults and reset

- **Soft limits for dragging, hard limits for typing.** Blender: dragging is restricted to the soft range; typing allows wider values "but never wider than the hard limit". Example: opacity scrubs 0 to 100; a light's strength scrubs 0 to 1000 but accepts 100000 typed.
- **Clamp silently at hard limits**, and flash the field edge once to show the clamp happened.
- **Every property has a default** and a "Reset to default" in its context menu and on Backspace when hovered (Blender). VS Code UX guideline: "Add default values to each setting."
- **Show when a value differs from the default** in panels where that matters (VS Code marks modified settings with a bar on the left; Blender shows decorators). Do not show default values in tooltips; Blender HIG: "Don't state default values, since they change and are hard to keep current."

## 7. Property state decorators

Blender 2.80 added a decorator column beside each property showing whether it is animated, a keyframe, driven, linked or overridden. Adopt the pattern for any tool where properties can be linked, animated, bound to tokens or variables:

| State | Decorator |
|---|---|
| Plain value | Empty dot, click to keyframe (animation tools) or nothing |
| Bound to a variable / style / token | Field shows the variable name as a chip; a detach icon on hover (Figma variables, design tokens) |
| Animated, keyframe on this frame | Filled diamond; field tinted (Blender yellow) |
| Animated, no key on this frame | Hollow diamond; field tinted (Blender green) |
| Driven by expression | Field tinted (Blender purple) |
| Overridden from library / instance override | Field tinted plus a reset icon to return to the source value |

Rules: the color of the field itself shows the state (readable at a glance across a whole panel), the decorator is the control, and every state has a tooltip that names it.

## 8. Operate, then adjust (redo panel)

Blender paradigm "Operate -> Settings": "Tools can be adjusted after use, so you aren't forced into settings before seeing results."

- After any operator with parameters, show a **redo panel** (Blender's Adjust Last Operation, bottom left corner of the editor, F9 to pop it up). Changing a value re-runs the operator from the state before it.
- The panel stays until the next action, then collapses to a small header so it does not cover the canvas.
- Example from Blender's manual: add a circle, set Vertices to 3 in the redo panel, get an equilateral triangle. The operator's dialog would have forced the user to know the value up front.
- **Repeat last** (Blender Shift+R) reruns the last operator with the same parameters on a new selection.
- **No modal parameter dialogs before an operator runs** unless the operator is destructive and cannot be previewed. Blender HIG avoids "dialogs that demand input before an action runs".
- **CAD variant:** feature dialogs stay open while the model previews live (Fusion, Onshape). Onshape distinguishes field types visually: "A solid blue field expects a selection in the graphics area. A blue-outlined field expects keyboard input." Make the expected input type visible on the field.

## 9. Contextual toolbars and popovers

- **Context toolbar = options of the selected tool or selection, shown in one fixed strip** above the canvas (Affinity context toolbar: "shows the commands and options relevant to the selected tool each time you pick a new tool"; it is a quick-access subset, not the full list).
- **Floating context toolbars near the selection** (SolidWorks context toolbar appears near the cursor on selection; Figma shows actions on selection) must: appear only after the selection settles (no flicker while dragging), never cover the selection, follow it when it moves, and disappear when the pointer moves far away or on Esc.
- **Bulk-action bars for collections** (Adobe Spectrum ActionBar): appear only when one or more items are selected, show the count ("3 selected") and a clear button, collapse labels into icons when space is tight, and overflow into a menu.
- **Popovers group related settings without taking space** (Blender 2.80). Press and hold on a popover button, drag to an option, release to set it, in one gesture. Popovers close on Esc or on moving the pointer well away.
- **A context menu is the per-object toolbar.** It shows verbs first, the most common at the top, shortcuts on the right, and is never the only place for an action (VS Code: "Show actions when contextually appropriate. Group similar actions together. Place large groups of actions into a submenu").

## 10. Labels, icons and density in panels

- **Labels optional, never absent.** Figma UI3 made property labels a toggle: on for guidance, off for an icon-led view. The icon-only version must still have tooltips, and screen reader labels must match the visible labels (Figma revised an early minimal approach after it hurt accessibility, calling it "a deal breaker").
- **Use nouns for labels, add direction in tooltips** ("Padding" with tooltip "Vertical padding") (Figma UI3).
- **Affordances must be visible.** Figma's earlier minimal style (sharp edges, abstract icons, subtle affordances) "became hard to parse as controls grew more complex"; UI3 added input backgrounds, dropdown borders, rounded corners and about 200 redrawn icons. Rule: every editable field has a visible background or border at rest, not only on hover.
- **Row height for dense pro panels: 24 to 32 px** at 1x scale. Field text at the body size of the product, never smaller than the type scale's smallest step.
- **Align values on one column** so the eye scans down a single edge.
- **Tooltips follow Blender HIG:** name without a trailing period; a description that starts with an imperative verb ("Determine how..."), two or three lines at most; a disabled hint explaining why a control is disabled; the shortcut; for toggles describe only the positive state ("Show in Viewport", not "Hide in Viewport"); never explain a term with itself; avoid "Enables..." ("Snap during transform", not "Enables snapping during transform").

## 11. Checklist

- [ ] Inspector header names the selection and its count.
- [ ] Empty selection shows document properties.
- [ ] Section order is by edit frequency and matches the previous version unless tested.
- [ ] Non-default values are visible without hovering.
- [ ] Mixed values show "Mixed"; typing sets all; scrubbing applies deltas.
- [ ] Every number field implements the table in section 4.
- [ ] Every number field accepts expressions and units, and shows its unit.
- [ ] Dragging respects soft limits, typing respects hard limits.
- [ ] Reset to default is available on every property.
- [ ] Animated, driven, bound and overridden values are tinted and decorated.
- [ ] Operators with parameters get a redo panel; no pre-operation dialogs.
- [ ] Every field has a visible resting background or border.
- [ ] Every icon-only control has a tooltip with name, verb-first description and shortcut.
