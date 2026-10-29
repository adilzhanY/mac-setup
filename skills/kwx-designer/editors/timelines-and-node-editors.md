# Timelines and node editors

Two special canvases: time-based editors (video, audio, animation) and graph editors (shader nodes, compositing, geometry nodes, workflow builders). Primary sources were thin for these; the rules below are the shared conventions of DaVinci Resolve, Premiere, Final Cut, Logic, Ableton, Blender and Houdini, plus the Blender HIG grid rule. Treat them as conventions to match, and test.

## Contents

1. Timeline anatomy
2. Playhead, scrubbing and transport
3. Editing on a timeline
4. Zoom and navigation in time
5. Node editor anatomy
6. Connecting, inserting and organizing nodes
7. Feedback in node graphs
8. Checklist

---

## 1. Timeline anatomy

| Part | Rule |
|---|---|
| Ruler | Top edge, timecode or bars:beats, density adapts to zoom. Grid lines along time only (Blender HIG: draw the grid on the axis whose coordinates matter, here only time). |
| Tracks / lanes | One row per track, header on the left with name, mute, solo, lock, visibility, arm (audio). Headers stay fixed while the content scrolls horizontally. |
| Clips / regions | Show content: thumbnails for video, waveforms for audio, curves or keys for animation. Name at the left edge, kept visible when the clip start scrolls off screen. |
| Playhead | A full-height line in an accent color with a grab handle in the ruler. |
| Viewer | Above the timeline; the timeline and viewer are the "canvas pair". |
| Transport | Play, stop, loop, record, jump to start/end; usually under the viewer and on the keyboard. |

Workflow pages: DaVinci Resolve splits the whole pipeline into pages (Media, Cut, Edit, Fusion, Color, Fairlight, Deliver) along the bottom edge, in pipeline order. Use workflow pages when the tasks need different layouts and tools but share one project.

## 2. Playhead, scrubbing and transport

- **J K L** for reverse, pause, forward; repeated J or L speeds up. **Space** plays and pauses. **Left/Right** step one frame, **Shift+Left/Right** step a larger unit, **Up/Down** jump to previous/next edit point. These are cross-NLE conventions; match them.
- **Click in the ruler moves the playhead; drag scrubs** with audio scrubbing optional.
- **Scrubbing must render at the display rate** or show lower resolution frames; never freeze the viewer while the playhead moves.
- **Loop region** set in the ruler by drag, shown as a tinted band.
- **The current time is an editable field:** type `1:02:10` or `+30` (frames) to jump.

## 3. Editing on a timeline

- **Selection follows the canvas rules** in `tools-modes-selection.md`: click, Shift click, marquee in empty track space.
- **Trim at clip edges** with edge-specific cursors (trim in, trim out). Hit zones in screen pixels, at least 6 to 8 px, growing with zoom only up to a cap.
- **Ripple, roll, slip, slide** are modes of trimming; show the active trim mode in the cursor and in the toolbar, and offer them as quasimodes with modifiers where possible.
- **Snapping to playhead, clip edges and markers** on by default, toggled with a visible magnet button and a key (N in many NLEs, S in others); show a snap line when it engages.
- **Blade / split at playhead** is one key (Ctrl/Cmd+B or B tool). Splitting never loses media; clips reference sources with handles.
- **Gaps are visible** and closable with one command (ripple delete).
- **Magnetic or track-free timelines** (Final Cut) trade control for fewer collisions; if you build one, show clearly what will move when you drop.
- **Drop preview:** while dragging a clip, show exactly where it will land and what it will push or overwrite (insert versus overwrite indicated by cursor and color).
- **Audio levels and fades** are direct-manipulation handles on the clip (fade handles at the top corners, level line across the clip).

## 4. Zoom and navigation in time

- **Ctrl/Cmd + wheel or pinch zooms time around the cursor**, plain wheel scrolls tracks vertically, Shift + wheel scrolls time. Alt + wheel can change track height.
- **Zoom to fit the whole sequence** on one key (Shift+Z in Premiere, Home in Blender).
- **The playhead stays in view while playing** (page or smooth scroll follow), with a toggle.
- **Minimap or overview bar** for long timelines.

## 5. Node editor anatomy

- **Dotted grid background** because coordinates do not matter but movement must stay visible (Blender HIG).
- **Node:** header with title and collapse toggle, colored by category; input sockets on the left, outputs on the right (data flows left to right); socket color and shape encode the data type; inline fields for unconnected inputs.
- **Links (noodles):** bezier curves from output to input, colored by type, drawn behind nodes.
- **Side panel:** properties of the active node (same inspector rules as everywhere).
- **Breadcrumb for nested groups:** "Material > Wood > Grain group", Tab to enter a group, Esc or Tab to exit (Blender).

## 6. Connecting, inserting and organizing nodes

- **Drag from a socket to a socket** to connect; valid targets highlight during the drag, invalid ones dim. Never allow a link between incompatible types silently; show an inline conversion or refuse with the reason.
- **Drag from a socket and release on empty canvas** opens a search filtered to nodes that accept that type, and the new node connects automatically. This is the single biggest speed-up in node editors.
- **Search to add** a node at the cursor (Blender Shift+A, plus typing to search). The palette rules in `shortcuts-and-command-search.md` apply.
- **Drop a node onto an existing link to insert it.** Highlight the link while hovering so the user sees the insert will happen, and allow a modifier to suppress it. Blender developers debated whether insert-on-link should need a modifier; whichever you pick, the highlight is mandatory.
- **Cut links** by a knife gesture (Blender Ctrl + right drag) or by dragging the input end away.
- **Reroute points** on links (double click or Shift drag on a link) to tidy long noodles.
- **Frames** group nodes with a title and color; moving a frame moves its contents.
- **Mute / bypass** a node with one key (Blender M), drawn with a pass-through line.
- **Auto-arrange** on command, never automatically while the user is working.
- **Duplicate keeps links to inputs** optionally (Blender Shift+D versus Ctrl+Shift+D style variants).

## 7. Feedback in node graphs

- **Preview the output of any node** with one action (Blender Ctrl+Shift+click with Node Wrangler, viewer node) so users can see the data at any point in the graph. This is Bret Victor's "show the data" applied to graphs.
- **Show values on links** where they are cheap: field types, counts (Blender shows geometry counts on hover), small thumbnails for images.
- **Errors appear on the node** (red header, icon, message on hover), not in a separate console only.
- **Performance per node** available on demand (Blender geometry nodes timings overlay), so slow nodes can be found.
- **Unused nodes are dimmed** so users see what does not contribute to the output.

## 8. Checklist

- [ ] Timeline track headers stay fixed; clip names stay visible when scrolled.
- [ ] J K L, Space, frame stepping and edit-point jumps work.
- [ ] Trims show cursor-specific edges; trim mode is visible.
- [ ] Snapping in time is on, toggleable, and shows a line.
- [ ] Drops preview insert versus overwrite.
- [ ] Node editor uses a dotted grid and left-to-right flow.
- [ ] Dragging a link to empty space opens a type-filtered search.
- [ ] Insert-on-link is highlighted before release.
- [ ] Any node's output can be previewed in one action.
- [ ] Errors and slow nodes are shown on the node itself.
