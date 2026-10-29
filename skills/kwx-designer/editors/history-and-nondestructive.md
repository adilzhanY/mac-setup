# Undo, history and non-destructive editing

Users explore freely only when nothing they do is permanent. This file specifies the undo model and the non-destructive patterns that make that true.

## Contents

1. Why undo replaces confirmations
2. The undo model: steps, marks, squashing, bailing
3. What goes into history and what does not
4. Undo history panel and snapshots
5. Multiplayer undo
6. Non-destructive editing patterns
7. Parametric history (feature trees and timelines)
8. Saving and recovery
9. Checklist

---

## 1. Why undo replaces confirmations

- Raskin: answering "yes" to a delete confirmation becomes a habit, which defeats its purpose; the better solution "would be to allow for easy undos". Habituation makes every frequent confirmation worthless.
- Shneiderman: users "experience less anxiety because the system is comprehensible and because actions are so easily reversible".
- Rule: **no confirmation dialog for any action that undo can reverse.** Confirm only actions that cannot be undone (deleting a file from disk, sending, publishing, emptying trash), and then name the consequence in the button ("Delete 12 files").
- Show a short toast after a large but undoable action: "Deleted 48 layers. Undo (Ctrl+Z)".

## 2. The undo model

Use the tldraw history model as the reference design, because it is explicit:

- **Two stacks:** undo and redo.
- **Marks are stopping points.** Changes accumulate until a mark; undo reverts to the previous mark. Create a mark at the start of every user interaction, so one drag is one undo step no matter how many frames it touched.
- **Squash** multi-step operations into one step on exit (tldraw squashes image crop changes when the user leaves crop mode; each tweak was undoable during cropping).
- **Bail** to cancel: Esc during an interaction reverts to the mark and the changes never reach the redo stack (tldraw: Alt-drag cloning bails when the user switches modes mid-drag).
- **The next recorded change clears the redo stack**, but creating a mark does not.

Rules:
- **One user intention = one undo step.** A drag, a scrub of a number field, a paste of 30 objects, an operator with its redo panel tweaks: each is one step.
- **Typing is grouped** by word or by pause (about 1 s) or by focus leaving the field.
- **Every step has a human name** ("Move 3 layers", "Change fill", "Extrude"), shown in Edit > Undo and Edit > Redo menu items and in the history panel.
- **Undo restores selection and, where useful, the view of the change.** If the change is off screen, pan or flash to show what was undone; otherwise users think undo did nothing.
- **Undo is unlimited by default** or bounded only by memory, with the limit in preferences (Blender: Memory and Limits preferences).
- **Undo works across modes** (Blender's global undo across object and edit mode is a long story of bugs; get this right early).

## 3. What goes into history and what does not

| Change | Recorded? |
|---|---|
| Document data (geometry, properties, layers, nodes, clips) | Yes |
| Selection of document objects | Yes, but must not clear the redo stack (tldraw `record-preserveRedoStack`; Figma: undo, copy, redo must leave the document unchanged) |
| Selection in UI lists like a file browser | No (Blender HIG) |
| Camera, zoom, pan | No. Blender and Figma do not put view changes in undo; offer a separate "previous view" command instead. |
| Panel layout, tool choice, preferences | No |
| Remote collaborators' changes | Never in your stack (tldraw: remote changes "are never recorded") |
| Your cursor position broadcast to others | No (`ignore`) |

Blender HIG: "Whenever scene data selection changes, an undo push should be triggered. Conversely if selection did not change, no undo push should be triggered."

## 4. Undo history panel and snapshots

- **Show a history list** (Blender Edit > Undo History, Photoshop History panel): newest at the top or bottom consistently, current state marked with a dot, click any entry to jump there. Blender: you can hop around "as long as you do not make a new change. Once you do make a new change, the Undo History is truncated at that point."
- **Snapshots or named versions** let users mark a state worth returning to before exploring (Photoshop snapshots, Figma version history with named versions, Fusion versions on save).
- **Repeat history** (Blender Shift+R repeat last, Repeat History menu) reuses past operations on new selections.
- **Version history is a separate concept from undo:** undo is the session; versions are durable and survive closing the file. Blender warns that its undo history is lost when you quit, "even if you save your file". Tell users which one they are looking at.

## 5. Multiplayer undo

Figma's principle, verbatim: "if you undo a lot, copy something, and redo back to the present (a common operation), the document should not change."

- **Undo only your own changes.** Never revert a collaborator's edit with your Ctrl+Z.
- **Undo modifies the redo history at the time of the undo** (Figma), so redo does not overwrite others' later edits with stale values.
- **When undo cannot apply** because a collaborator deleted the object, skip that step silently or with a small notice, never crash or undo something else.
- **Show who changed what** in version history with avatars and timestamps.

## 6. Non-destructive editing patterns

Non-destructive = the original data is kept and the change is a removable, editable layer on top. Use it whenever the operation is lossy or the user is likely to revisit it.

| Pattern | Where it comes from | Rule |
|---|---|---|
| Adjustment layers | Photoshop, Affinity, Resolve nodes | Color and tone changes are layers above the pixels, with a mask and opacity, toggleable |
| Smart objects / smart filters | Photoshop | Filters applied to a container keep the original pixels; double click to edit parameters later |
| Masks instead of erasing | Photoshop, Affinity | Hide pixels, do not delete them; painting black hides, white reveals |
| Modifier stacks | Blender modifiers, 3ds Max stack | Operations are an ordered list on the object, each with show/hide, apply, reorder, and live parameters |
| Parametric features | Fusion, Onshape, SolidWorks, FreeCAD | Geometry is the result of a feature list; edit any feature and everything after it recomputes |
| Node graphs | Blender shader/geometry nodes, Resolve color page, Houdini, Nuke | The result is a function of a graph; any node can be bypassed or tweaked |
| Effects and styles | Figma effects, layer styles | Shadows and blurs are properties, not baked pixels |
| Instances / components | Figma components, Blender linked duplicates | Edit the source once, all instances update; overrides are tracked per property |
| Clips reference media | Every NLE | Trimming never deletes media; handles are kept |

Rules:
- **Every non-destructive layer has a visibility toggle** (eye icon) right in its row, so users can compare before and after in one click.
- **Order is visible and editable by drag** (modifier stack, layer list, node graph).
- **"Apply" or "bake" is an explicit, named, undoable action**, never a side effect of something else.
- **Make the destructive version clearly labeled** when both exist ("Image > Adjustments" versus "New Adjustment Layer"); default menus should lead to the non-destructive one.
- **Show cost.** If a stack gets slow, show which layer or modifier costs time (Blender's geometry nodes timings overlay, Resolve's render cache indicators) so users can disable it temporarily instead of applying it.
- **Overrides are visible per property.** A changed property on an instance is tinted and has a reset to source (see `inspector-and-numeric-input.md` decorators).

## 7. Parametric history (feature trees and timelines)

CAD-specific detail lives in `cad-specific.md`. The general rules:

- **The history is the document, the view is the result.** (A Fusion learner's summary: the timeline is effectively the document while the 3D view is a result of it.)
- **A rollback marker** shows where you are in the history; dragging it shows the model as it was at that point without deleting anything (Fusion timeline marker, Onshape rollback bar).
- **Work at the end by default.** Rolling back is an explicit act with a visible marker; new features insert at the marker position, which must be obvious.
- **Broken downstream features are shown in place** with a warning color and a reason ("Reference lost: Face 3"), not as a modal error.
- **Editing an earlier feature previews the downstream result live** before committing.
- **Deleting a feature warns about dependents** with a list, because "deleting a feature can break later features that reference it".

## 8. Saving and recovery

- **Autosave by default** for cloud tools; for file-based tools, save recovery snapshots every few minutes and offer "Recover last session" on the splash (Blender splash: "Recover Last Session").
- Raskin's principle: work should be saved automatically and continuously, with no manual save step. Where files must exist, at least never lose more than a minute of work.
- **Show the save state** quietly in the title or header ("Saved", "Saving...", "Offline, changes kept locally"). Figma lets you go offline "for an arbitrary amount of time and continue editing".
- **Never block editing while saving.**

## 9. Checklist

- [ ] No confirmation for undoable actions.
- [ ] Each drag, scrub, paste and operator is exactly one named undo step.
- [ ] Esc during an interaction reverts to the mark, nothing goes to redo.
- [ ] Undo restores selection and reveals off-screen changes.
- [ ] Selecting objects does not clear redo.
- [ ] A history panel exists and jumps to any entry.
- [ ] In multiplayer, undo only affects your own changes.
- [ ] Lossy operations have a non-destructive default (layer, modifier, mask, feature).
- [ ] Every non-destructive layer has an eye toggle and a drag handle for order.
- [ ] Apply/bake is explicit and undoable.
- [ ] Autosave or recovery exists; save state is visible.
