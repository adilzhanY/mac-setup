# Panels, workspaces, density and onboarding

How to lay out panels, let people reshape them, set density, and teach a complex tool without a tutorial wall.

## Contents

1. Panel layout rules
2. Floating versus docked: the UI3 reversal
3. Workspaces, pages and personas
4. Customization without chaos
5. Density
6. Progressive disclosure for expert features
7. Onboarding a complex tool
8. Notifications, status and messages
9. Checklist

---

## 1. Panel layout rules

- **Non-overlapping by default.** Blender's first paradigm: "The UI should show all relevant options and tools at a glance without moving windows around." Blender subdivides the window into areas, and areas into regions (header, toolbar, sidebar). Floating windows that hide each other are the exception, not the system.
- **Reading flow left to right, top to bottom** (Blender HIG): choose (left), act (center), refine (right).
- **Panels are resizable by dragging their inner edge**, with min and max widths (240 to 480 px is a sane range for an inspector). The resize affordance is a full-height hit zone of at least 6 px with a resize cursor.
- **Panels collapse to zero or to a thin rail**, and come back from the same edge. Collapsing never loses their scroll position or expanded sections.
- **A single shortcut minimizes all UI** to the canvas plus a minimal toolbar (Figma Minimize UI keeps tools reachable; the older Hide UI was "blunt and limiting"). Blender Ctrl+Space maximizes the hovered area.
- **One panel per job.** VS Code: "Keep the number of Views to a minimum." Tabs inside a sidebar are fine for a few peers; deep tab nesting is not.
- **Do not let the canvas be pushed narrower than about 50 percent** of the window. Panels yield first.
- **Splitting:** let users split the editor area (two viewports, code side by side, source and program monitors). Blender lets any area become any editor type via the editor type dropdown at its left header edge.

## 2. Floating versus docked: the UI3 reversal

Figma explored hover-only panels, panels hanging above the canvas, then shipped floating panels in the UI3 beta. In the full rollout they reattached the panels. Reasons from beta feedback:
- Floating panels cramped the canvas on smaller screens.
- Designs peeked out around the panels, which was distracting.
- Rulers moved farther from the designs.
- "The nail in the coffin was learning that they slowed people down."
- Panels that appeared and disappeared made the workspace "too unstable".

Lesson as rules:
- **Dock panels for any tool used for hours.** Fixed edges are spatial memory.
- **Floating chrome is fine for a single slim toolbar** (Figma's bottom toolbar) and for transient UI (popovers, context bars, palettes).
- **Never auto-hide panels on hover for productivity tools.** Use explicit collapse.
- **Floating is fine when content is presentational** (Figma keeps floating panels in Minimize UI, Slides grid view and FigJam).

## 3. Workspaces, pages and personas

All three are named, task-specific layouts:

| Product | Name | How it works |
|---|---|---|
| Blender | Workspaces | Tabs at the top (Layout, Modeling, Sculpting, UV Editing, Shading, Animation, Compositing, Geometry Nodes, Scripting). Each sets a layout and can switch the object mode on activation. Ctrl+PageUp/PageDown to cycle. Saved in the file or as defaults. |
| DaVinci Resolve | Pages | Media, Cut, Edit, Fusion, Color, Fairlight, Deliver, left to right in the order of the post-production chain, buttons along the bottom edge. |
| Affinity | Personas | Designer, Pixel, Export (plus others per app). Each has its own tools and panels on the same document. Active persona icon is saturated. |
| Onshape | Toolbars by context | Document, Feature, Sketch, Assembly, Drawing toolbars change with the workflow. |
| VS Code | Activity Bar view containers | Explorer, Search, Source Control, Run, Extensions swap the sidebar contents. |

Rules:
- **Order workspaces by the workflow sequence** (Resolve's left-to-right pipeline). The order itself teaches the process.
- **Show workspaces as visible tabs, not a dropdown.** Blender 2.80 moved workspaces from a dropdown to tabs because the dropdown "meant an extra click to switch".
- **The document is shared across workspaces.** Switching workspace never changes the data, only the tools and layout.
- **A workspace may change the mode** (Blender sets object mode per workspace), but must show the new mode immediately.
- **Five to nine default workspaces maximum.** More are added by the user from templates.
- **Users can duplicate, rename, reorder and delete workspaces** (right click on the tab).

## 4. Customization without chaos

- **Defaults must be excellent; most users never customize.** Raskin warns that users optimize customizations for likeability, not efficiency, and waste time on them. Customization is for experts and for task fit, not a substitute for design.
- **Customize where you are:** right click a toolbar to "Customize toolbar" (Onshape: drag tools off, move between groups, reset), right click any command to add it to favorites or the shortcut bar (Blender Quick Favorites, SolidWorks shortcut bar).
- **Every customization has "Reset to default"** next to it.
- **Layouts are saved per workspace and can be exported.** Blender "Load UI" decides whether a file's layout replaces yours; make this choice visible.
- **Adaptive toolbars collapse predictably.** Onshape: lower resolution or higher browser zoom moves more tools into group dropdowns, and the last used tool moves to the front of its group (and resets when the document reopens). Adaptivity must never move a tool between groups, only fold it.
- **Never reorder menus automatically by frequency.** Adaptive menus destroy spatial memory. Recency is allowed only in explicitly separate "Recent" sections and in the last-used slot of a tool group.

## 5. Density

- **Pro tools are dense by design.** Rows of 24 to 32 px, panels of 240 to 320 px, 11 to 13 px type at 1x in most pro apps. Density is correct when experts can see a whole section without scrolling, and wrong when targets drop below the platform minimum.
- **Offer a scale, not a redesign.** One UI scale setting multiplies type, controls and radii together (Blender Resolution Scale; Spectrum's desktop versus mobile scale). Test every layout at 1x and 2x.
- **Do not shrink text to fit.** Widen the panel or wrap the label. Truncate long names in the middle (`Header / Desk...op`), with a tooltip showing the full name.
- **Space is information.** Group with 8 to 12 px gaps between sections and 4 px within; use dividers only between unrelated groups.
- **Calm UI.** Blender HIG best practices: avoid strong color changes, big layout jumps and elements that pop in during simple interactions; flashy hover highlights distract. Hover shows a subtle background change only.
- **Color is reserved for meaning:** accent for selection and the active tool, axis colors for X/Y/Z, state colors for animated/driven/error. Never decorative color in the chrome. Blender 2.80 made icons take their colors from the theme so the UI stays quiet around the artwork.

## 6. Progressive disclosure for expert features

- **Layer the system** (Shneiderman's "layered or spiral approach to learning"): a modest set of commands lets novices become "expert at level 1", then expand.
- **Collapsed subpanels** for advanced settings (Blender 2.80: "less common settings collapsed by default").
- **"Advanced" toggles are a last resort;** prefer a subpanel with a meaningful name ("Tolerance", "Sampling") so the user knows what is inside.
- **Expert accelerators never replace the visible path:** every shortcut, gesture and palette command also exists as a visible button or menu item.
- **Feature visibility by context:** show tools only in the mode where they apply (Blender toolbar per mode) instead of disabling them everywhere.
- **Hide the developer layer behind an explicit switch** (Blender Developer Extras shows data paths and operator search).
- **Rarely used, dangerous options live in preferences with search**, not in panels.

## 7. Onboarding a complex tool

Shapr3D's founder: "Easy should be easy. Hard must not be impossible." and "A great product is characterized by a minimal tool time. Nobody really wants to learn to use their software."

Rules:
- **Ask only the choices that change input behavior on first run.** Blender Quick Setup: select with left or right click, Spacebar action (play, tools, search), theme. Nothing else.
- **Start from a template, not from nothing.** Blender: General, 2D Animation, Sculpting, VFX, Video Editing, each with its own startup layout. The splash also offers recent files and "Recover Last Session".
- **Teach through the status bar and tooltips, continuously,** not through a one-time tour. Blender's status bar always shows the mouse map for the current tool.
- **Show affordances explicitly.** Shapr3D: showing handles explicitly raised success "by two orders of magnitude".
- **Empty states that do the first step.** VS Code Welcome views: use links rather than buttons when possible, buttons only for primary actions, short content, no promotions, no generic "read more".
- **Walkthroughs are checklists of real actions** in the real UI (VS Code Walkthroughs), with progress, skippable, reopenable from Help.
- **Labels on for newcomers, off for experts** (Figma UI3 optional labels).
- **Make the change itself reversible.** Figma let users switch back from UI3 during the beta "to finish deadline work", and rolled out gradually with tutorials before removing the old UI. Any major UI change in a pro tool needs an opt-out period.
- **Test with real professionals and watch them fail.** Shapr3D: "You need to see them fail a thousand times." Figma ran crits as 60-minute "speed rounds" and judged criticism by asking whether it reflected a lasting problem or a reaction to change.

## 8. Notifications, status and messages

From the VS Code UX guidelines:
- "Respect the user's attention by only sending notifications when absolutely necessary." "Show one notification at a time." "Add a Do not show again option for every notification." Never use notifications for promotion or to ask for feedback on first install.
- Progress: show stages as they happen, link to details or logs, provide cancel, add timeouts, never leave progress running forever.
- Background progress lives in the status bar; only elevate to a notification when the user must act.
- Status bar: short text labels, icons only for clear metaphors, global items left, contextual items right, no custom colors; error and warning backgrounds are a last resort.
- Decision rule from the notification decision tree: "If the user does not really need to be notified consider to not show anything and relax."

Blender adds: report messages in the status bar disappear after a short time and open the full log on click.

## 9. Checklist

- [ ] Default layout has no overlapping panels.
- [ ] Every panel resizes and collapses; one key minimizes all UI.
- [ ] Panels are docked for long-session tools; floating only for transient UI.
- [ ] Workspaces are visible tabs ordered by workflow.
- [ ] Toolbars can be customized in place and reset.
- [ ] No adaptive reordering of menus.
- [ ] One UI scale setting scales type and controls together; layout passes at 2x.
- [ ] No text shrunk below the scale's smallest size.
- [ ] Advanced settings are in named, collapsed subpanels.
- [ ] First run asks only input-mapping questions and offers templates.
- [ ] The status bar teaches the current tool's mouse map.
- [ ] Notifications are rare, one at a time, and dismissible forever.
