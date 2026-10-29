# Details and polish

The invisible details that separate "fine" from "premium". Most users never notice any single one. Together they decide whether the product feels cared for (Emil Kowalski: "unseen details compound"; Stamatiou: a dozen small fixes together are noticeable).

## Contents

1. Alignment: geometric first, optical last
2. Corner radii: concentric nesting
3. Spacing systems and grouping
4. Borders, hairlines and dividers
5. Icons next to text
6. Buttons and controls
7. Hit areas and pointer details
8. States: the full set
9. Loading, empty, error and overflow
10. Robustness: content of every length
11. Forms
12. Focus and keyboard
13. Platform and browser details
14. Images and media
15. Polish checklist
16. Sources

---

## 1. Alignment: geometric first, optical last

- **Every element aligns with something** (Hobday rule 8, Vercel "Align every element to something intentional"). Unaligned elements read as not belonging.
- **Align to a grid first** (12 columns for horizontal layout divides into 1, 2, 3, 4, 6: Hobday rule 13; Vignelli: the grid exists "to prevent arbitrary, meaningless placements").
- **Then correct optically.** Shapes with uneven visual weight look off when centred mathematically (Hobday rule 5). Vercel: adjust "by about 1px when optical alignment looks better than geometry". Apple's new design system: centre mathematically when it makes sense, offset subtly when centring hurts balance.
- **Common optical corrections** (workshop practice rather than numbers from one source; always confirm by eye):
  - Play triangle in a circle: shift right by about 1/12 to 1/10 of the circle diameter (the triangle's centre of mass sits left of its bounding box).
  - Text in a button: cap height looks low with symmetric padding in many fonts; check that the text looks vertically centred and nudge 0.5 to 1px if not, or use `text-box-trim` where supported.
  - Icon + label: centre the icon on the label's x-height or cap height, not on the line box.
  - Round shapes next to square ones: circles need to be slightly larger (about 5 to 10%) to look the same size.
  - Pointed and round glyphs overshoot the baseline; do not "fix" a font's overshoot.
- **Align mixed type on the baseline,** not tops or centres (Refactoring UI).
- **Linear's redesign** aligned labels, icons and buttons in the sidebar and tabs both vertically and horizontally: "hard to notice at first but is felt after a few minutes of use."

Test: draw horizontal and vertical guides through every edge. Each element should touch at least one guide that another element also touches.

## 2. Corner radii: concentric nesting

- **Inner radius = outer radius minus the padding between them** (Hobday rule 24; Apple concentric shapes; Vercel "child radius at most the parent's and concentric").
  - Card radius 16, padding 8, inner thumbnail radius 8.
  - Card radius 12, padding 12, inner radius 0, so use a small fixed radius (2 to 4) or square corners.
- **Three shape types** (Apple, 2025): fixed radius, capsule (radius = height / 2), concentric (computed from the parent).
- **Pinched or flared inner corners** mean the shape is not concentric (Apple).
- **Components used both nested and alone:** concentric radius with a fallback radius when standalone.
- **Radius expresses personality** (Refactoring UI): 0 to 4px neutral and serious, 6 to 12px friendly, large and pill shapes playful. Pick one family and apply it everywhere.
- **Capsules suit touch and standout actions;** dense desktop UIs use rounded rectangles and reserve capsules for prominent buttons (Apple macOS controls: mini, small, medium stay rounded rectangles; large and extra large become capsules).
- **Keep radius consistent by size class:** small controls, medium cards, large sheets. Do not invent a radius per component.

## 3. Spacing systems and grouping

- **One spacing scale** from a base of 4 or 8 (Hobday rule 11). Refactoring UI uses a 16px base with factors: 4, 8, 12, 16, 24, 32, 48, 64, 96, 128.
- **Small values matter most.** A 2px change in button padding is very visible; on a card width it is not (Refactoring UI).
- **Start with too much white space,** then remove (Refactoring UI). Adding space to a cramped design is harder.
- **Proximity groups.** Space between related items must be clearly smaller than space between groups. A label sits closer to its own input than to the previous input (Refactoring UI, "Avoid ambiguous spacing"; Apple *Essential Design Principles*: proximity and grouping).
- **Outer padding at least the inner gap** (Hobday rule 19).
- **Measure spacing between points of high contrast** (Hobday rule 14): from text cap height to the edge of a card, not from the invisible line box.
- **Remove dead zones between list items;** give the items more padding instead, so the pointer never falls into a gap (Rauno).
- **You do not have to fill the screen** (Refactoring UI). Fixed width sidebars, a centred login card; not everything should stretch.
- **Buttons: horizontal padding about 2x vertical** (Hobday rule 22). 8px by 16px, 10px by 20px.

## 4. Borders, hairlines and dividers

- **Use fewer borders.** Separate with spacing, a background shift or a shadow (Refactoring UI).
- **Never two hard divides side by side** (Hobday rule 25): a background change plus a border plus a divider line is clutter. Pick one.
- **A container border contrasts with both the container and the background:** darker than both on light themes, lighter than both on dark themes (Hobday rule 7).
- **Semi transparent borders** adapt to any background: `border: 1px solid rgb(0 0 0 / 0.08)` on light, `rgb(255 255 255 / 0.08)` on dark. Combine with a shadow (Vercel: "Combine borders and shadows, using semi-transparent borders").
- **Tint borders and shadows toward the background hue** (Vercel).
- **Hairlines on high DPI:** `0.5px` borders render as a true hairline on 2x screens; fall back to 1px on 1x. Or use `box-shadow: 0 0 0 0.5px`.
- **Scroll edge instead of a divider** under sticky headers: a soft fade or blur where content passes under the floating bar, only when content actually overlaps (Apple 2025).
- **Accent borders** (a 3 to 4px coloured top or left edge) add identity cheaply (Refactoring UI) but count as your one accent.

## 5. Icons next to text

- **Lower the icon's contrast** relative to the text; icons look heavier than letters at the same colour (Hobday rule 28; Refactoring UI).
- **Balance weight, size and spacing** when icon and text sit together (Vercel). Solid icons are heavier than outline icons.
- **One icon family, one stroke weight, one corner style** across the product.
- **Icons have an intended size.** A 16 to 24px icon blown up to 64px looks chunky; a detailed icon at 16px turns to mush (Refactoring UI). Use the size the set was drawn for.
- **Icon-only buttons need an accessible name** (`aria-label`) and usually a tooltip (Vercel, Rauno).
- **Do not group a symbol with text in one bar group** where it might read as one button (Apple 2025: "Select" next to a share icon).
- **Use a text label when no glyph is clearly understood** (Apple: a pencil may read "annotate", a checkmark may read "confirm").
- **Never emoji as icons.**

## 6. Buttons and controls

- **Hierarchy:** one primary (filled), a couple of secondary (outlined or tinted), tertiary as links (Refactoring UI).
- **Destructive is not primary** unless it is the confirming step in a dialog about destruction (Refactoring UI).
- **Labels name the action** ("Make toast", not "Toast"; "Save API Key", not "Continue") (Apple *The Life of a Button*, Vercel).
- **Loading:** keep the label, add a spinner, keep width fixed (Vercel).
- **Submit stays enabled until the request starts,** then disables, shows progress and sends an idempotency key (Vercel). Do not disable submit to hint at validation; let people submit and see the errors.
- **Toggles apply immediately,** no confirm step (Rauno).
- **Separate stop from start:** do not swap "Make toast" to "Stop toasting" in the same button, which looks too similar (Apple).
- **Anything that looks interactive is interactive** (Vercel).
- **Disabled buttons have no tooltips** (Rauno), and should be rare. Prefer explaining why something is unavailable.

## 7. Hit areas and pointer details

- **Minimum hit area 24px for pointer, 44px for touch** (Vercel). Expand with padding or a pseudo element when the visual is smaller.
- **Checkbox and radio share one hit area with their label** (Vercel).
- **Hover only for fine pointers:** `@media (hover: hover)` (Rauno).
- **`touch-action: manipulation`** on controls to remove double tap zoom delay (Vercel).
- **Replace the default tap highlight** with your own pressed state (Rauno, Vercel).
- **Open dropdown menus on `mousedown`,** not `click` (Rauno), so they feel instant.
- **Prediction cone in nested menus** so moving diagonally toward a submenu does not close it (Rauno).
- **Decorative glows and gradients do not catch pointer events** (`pointer-events: none`) (Rauno).
- **Disable text selection inside interactive elements' chrome** and on dragged items; apply `inert` to the dragged element (Rauno, Vercel).

## 8. States: the full set

A component is not finished until each applicable state exists:

| State | Rule |
|---|---|
| Rest | The baseline |
| Hover | Visible change, more contrast than rest; fine pointers only |
| Pressed / active | Instant (scale 0.97 or darker fill), within one frame |
| Focus visible | `:focus-visible` ring, never removed without replacement; use `box-shadow` so it follows the radius (Rauno) |
| Selected / current | Distinct from hover, without changing font weight |
| Disabled | Lower contrast, no hover, cursor not-allowed; explain why nearby if possible |
| Loading | Label kept, spinner or progress, no layout change |
| Success | Confirmation near the trigger (inline check after copy, Rauno) |
| Error | Message beside the field, field highlighted, focus moved to the first error on submit (Vercel) |

Vercel: hover, active and focus states need **more** contrast than rest.

## 9. Loading, empty, error and overflow

- **Skeletons match the final content exactly** (Vercel). A skeleton that is a different shape causes a jump.
- **Spinner timing:** show after 150 to 300ms, keep at least 300 to 500ms (Vercel).
- **Empty states are first impressions** (Refactoring UI). Explain what appears here and how to create it, with the primary action and optionally templates (Rauno, Apple WWDC22: "No Saved Episodes. Save episodes you want to listen to later, and they'll show up here.").
- **Errors:** what happened, why if known, how to fix it, and a button that fixes it ("Add Payment Method", "Not Now") (Apple WWDC22).
- **Every screen offers a next step or a recovery path** (Vercel).
- **Design empty, sparse, dense and error states** for every list (Vercel).
- **Feedback near the trigger,** not in a far corner (Rauno).
- **Undo beats confirm** for reversible destructive actions; confirm only what cannot be undone (Vercel, Apple WWDC26 Agency).

## 10. Robustness: content of every length

- **Layouts handle short, average and very long user content** (Vercel). Test with a 1 character name, a 60 character name, and a German compound word.
- **Truncate deliberately:** ellipsis with a full value in a tooltip or title, `min-width: 0` on flex children so truncation works.
- **Translations grow:** Dutch and German run long, Thai needs more height, Arabic and Hebrew mirror (Apple WWDC22). Leave 30 to 40% slack in fixed width labels.
- **User uploaded images:** fixed containers with `object-fit: cover`; a subtle inner shadow or 1px inset border so a white photo does not bleed into a white card (Refactoring UI).
- **No layout shift:** explicit image dimensions, reserved space for async content, font loading that does not reflow (Vercel).
- **URL holds state** (filters, tabs, pagination, expanded panels) so refresh, share and back work (Vercel).
- **Restore scroll position** on back and forward (Vercel).
- **Hydration must not wipe focus or input values** (Vercel).

## 11. Forms

From Vercel and Rauno's guidelines:

- Every control has a label; clicking the label focuses the control.
- Enter submits a single field form; in a textarea, Cmd/Ctrl+Enter submits and Enter adds a line.
- Correct `type`, `inputmode` and `autocomplete`; spellcheck off for emails, codes and usernames.
- Never block paste, including one time codes and passwords.
- Do not block keystrokes to enforce format; accept input and validate with a message.
- Placeholders show an example format and end with an ellipsis character; they never replace the label.
- Inputs at least 16px on mobile.
- Warn before leaving with unsaved changes.
- Trim trailing whitespace.
- Explicit `background-color` and `color` on `<select>` so Windows dark mode does not break it.
- Inline validation in real time, and prevent errors where possible: Things 3 turns "June 31" into "July 1" instead of showing an error (Apple WWDC17).

## 12. Focus and keyboard

- Every flow works by keyboard, following WAI-ARIA patterns (Vercel).
- Focus rings visible and never covered by sticky elements (`scroll-margin-top`).
- Trap focus in modals, return it to the trigger on close.
- Arrow keys move through lists; Cmd+Backspace deletes a focused list item (Rauno).
- Autofocus the main input on desktop, rarely on mobile (Vercel, Rauno: never on touch).
- Show platform specific shortcut symbols and localize them for non QWERTY layouts (Vercel).

## 13. Platform and browser details

- `theme-color` meta matches the page background; `color-scheme: dark` on `html` in dark themes (Vercel).
- `overscroll-behavior: contain` on modals and drawers (Vercel).
- Respect safe areas with `env(safe-area-inset-*)`.
- Preview Windows scrollbars on macOS by setting scrollbars to "Always" (Vercel). Avoid unnecessary scrollbars.
- Text blurs after a transform: animate a wrapper, or use `translateZ(0)` sparingly (Vercel, Rauno).
- Gradient banding: avoid scaling or blurring solid rectangles; use radial gradients or background images instead of CSS masks (Rauno, Vercel).
- SVG favicon that responds to `prefers-color-scheme` (Rauno).
- Style `::selection` to match the brand; unset gradients on selected gradient text (Rauno).
- Prevent iOS landscape text inflation: `-webkit-text-size-adjust: 100%` (Rauno).
- Right click on the nav logo can offer brand assets (Vercel). A small gift for the people who look.

## 14. Images and media

- Use good photos or none; bad stock photography is worse than an empty area (Refactoring UI).
- Text on images needs a guaranteed contrast layer: overlay, reduced image contrast, or tint (Refactoring UI).
- Product screenshots in marketing: do not shrink a full screenshot into a thumbnail; crop to one feature, or draw a simplified UI where small text becomes lines (Refactoring UI).
- Respect asset safe zones: iOS stretches the bottom of an app icon during the launch morph, and icons that ignore the safe zone show a visible artifact (Rauno, the Bluesky icon example).
- Looping video instead of GIF, `muted` and `playsinline` for iOS autoplay, a still fallback for reduced motion (Vercel, Rauno).
- Pause or unmount off screen videos (Rauno).

## 15. Polish checklist

- [ ] Every element aligns to a guide shared with another element; optical nudges applied
- [ ] Nested radii concentric; one radius family
- [ ] All spacing on the scale; grouping gaps smaller inside than between
- [ ] At most one hard divide between regions; borders contrast with both sides
- [ ] Icons one family, one weight, intended size, lower contrast than text
- [ ] One primary action; labels are verbs; loading keeps label and width
- [ ] Hit areas 24px pointer, 44px touch; hover gated to fine pointers
- [ ] All nine states designed; focus visible with radius following ring
- [ ] Skeleton matches layout; spinner delay and minimum; empty and error states written
- [ ] Longest real string, one item and hundreds of items all tested
- [ ] No layout shift on load; URL holds view state
- [ ] Forms: labels, autocomplete, paste allowed, inline errors, 16px inputs on mobile

## 16. Sources

`../sources/books/vercel-web-interface-guidelines.md`, `rauno-freiberg-craft.md`, `refactoring-ui.md`, `anthony-hobday-safe-rules.md`, `apple-wwdc-design-talks.md`, `emil-kowalski-design-engineering.md`, `linear-and-stripe-writeups.md`, `paul-stamatiou-craft.md`.
