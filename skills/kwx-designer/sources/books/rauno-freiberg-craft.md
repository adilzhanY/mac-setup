# Rauno Freiberg: craft essays and interface guidelines

- **Who:** Estonian design engineer; Arc at The Browser Company, then Vercel (co-crafted nextjs.org), later reported moving to Cursor. Runs the paid course Devouring Details (not read).
- **Status:** free on his site.
- **Read, October 2026:**
  - "Invisible Details of Interaction Design" (2023): https://rauno.me/craft/interaction-design
  - "Novelty" (2026): https://rauno.me/craft/novelty
  - "Contrasting Aesthetics" (2024): https://rauno.me/craft/contrasting-aesthetics
  - "Designing Depth" (2024): https://rauno.me/craft/depth
  - Web Interface Guidelines (the precursor of Vercel's): https://interfaces.rauno.me
  - Lovers Magazine interview: https://spaces.is/loversmagazine/interviews/rauno-freiberg
- **How he learned:** not from books. He "reverse engineered other people's code" for months; his advice is "Work with the material" (HTML, CSS, JavaScript), start by "copying things that inspire you" and "Don't forget to say thank you". Quality is "a function of patience and focus"; small teams aligned on taste beat large ones.

## Invisible Details of Interaction Design

Interaction design is "an artform to make experiences that fluidly respond to human intent." Reuse metaphors so people learn by doing (stacked layers, horizontal paging, pinch to zoom). Model real physics: interruptible like a page flip, momentum that keeps the throw's angle and speed, bounce proportional to the object's conceptual mass. Pinch precision: zoom anchors are easier when fingers start close. **Trigger timing matches risk:** reversible light actions mid gesture, destructive ones only at gesture end (the app switcher never kills mid swipe); let a view snap but stay uncommitted so you can peek and back out. **Respond immediately:** apply pinch scale from the first frame. **Spatial consistency:** launch from the source icon when there are many sources. Asset discipline: icons outside the safe zone show artifacts when iOS stretches them. **Frequency and novelty decide whether to animate:** he removed his command menu animation after two days of use; macOS context menus do not animate in but flash the chosen item and fade out; the macOS app switcher never animates. Fidgetability (AirPods case). Content under the finger: loupe, key preview, sliders that keep tracking off track. Fitts's law: infinite corner targets, radial menus. Scroll focus should not be hijacked by inactive windows. Implicit input from context (Wallet raises brightness, apps blur sensitive content in the app switcher). Explaining why something feels right builds taste.

## Novelty

Novelty works only as contrast and fades with repetition (like semantic satiation). Make 90% familiar and 10% novel (from film's 60/30/10 colour rule). Novelty is "the equivalent of an exclamation mark". Spend it on one time moments (onboarding, first load: his login to welcome transition plays once, a reload skips it). New products pay a "novelty tax" (Arc overwhelmed everyday users). "Make most things familiar, do something unexpected."

## Contrasting Aesthetics

Pure minimalism often stimulates nothing; calm uniform design suits utilitarian tools. Deliberate contrast of distant styles creates curiosity (a bitmap typeface with a Renaissance painting; a wordmark cycling typefaces with everything else fixed; vintage objects in a Nordic interior). Contrast needs intent and iteration, not chaos; it suits first impressions and expressive brands, sparingly in focused tools. Techniques in a list: colour, form (rotation), hand drawn style, higher fidelity on one item.

## Designing Depth

From film composition: dirtying the frame with foreground objects, obstructed framing, shooting through glass, out of focus foreground. In UI: offset layers behind the primary surface, blur the inner background to push it back, fade the bottom edge so the container feels open, blur or dim the backdrop behind an overlay (depth of field; only the overlay is interactive). Choreography: split a gesture into discrete states, blur the back layer before revealing the front, delay competing elements (the keyboard), animate the element nearest the trigger first. Stagger siblings slightly (fish, birds); different springs per Control Center row; staggered text. Keep interactive layers sharp (the Dock slides without fading).

## Web Interface Guidelines (rauno.me)

**Interactivity:** label click focuses input; inputs inside a form so Enter submits; correct input types; spellcheck and autocomplete off for most inputs; `required` where it fits; input icons positioned absolutely and focusing the input; toggles act immediately; disable buttons after submit; no text selection on inner content of controls; decorative glows ignore pointer events; no dead space between list items (pad the items instead).
**Typography:** antialiased smoothing; optimizeLegibility; subset fonts; no weight change on hover or selection; no weights below 400; medium headings 500 to 600; `clamp()` for fluid sizes; tabular numbers where alignment matters; prevent iOS landscape text resizing.
**Motion:** no transitions on theme switch; interaction animations under 200ms; scale to the element (dialogs from about 0.8, buttons pressed to about 0.9 to 0.96); skip animation for frequent low novelty actions (context menus, list add and delete, hovering trivial buttons); pause looping animations off screen; smooth anchor scrolling with offset.
**Touch:** hover only under `(hover: hover)`; inputs 16px+; no autofocus on touch; `muted playsinline` for iOS autoplay; disable `touch-action` on custom pan and zoom; replace the iOS tap highlight.
**Optimizations:** big blur values are slow; scaled or blurred solid rectangles band (use radial gradients); `translateZ(0)` sparingly; `will-change` only during expensive scroll animations; pause off screen videos on iOS; update real time values via refs; adapt to device and network.
**Accessibility:** no tooltips on disabled buttons; focus rings via box-shadow (outline ignores radius); arrow keys through focusable lists; Cmd+Backspace deletes a focused item; dropdowns open on mousedown; SVG favicon that follows the colour scheme; aria-labels on icon-only controls; no interactive content in hover tooltips; `<img>` for images; aria-label on HTML illustrations; unset gradient on `::selection` of gradient text; prediction cone in nested menus.
**Design:** optimistic updates with rollback; auth redirects on the server; styled `::selection`; feedback next to its trigger (inline check after copy, highlighted fields on error); empty states prompt creation, optionally with templates.

## Used in

`../../premium/motion-and-feel.md`, `../../premium/details-and-polish.md`, `../../premium/restraint-and-reduction.md`, `../../premium/materials-depth-light.md`, `../../premium/typography-craft.md`.
