# Emil Kowalski: design engineering, animation and taste

- **Who:** design engineer (Linear, previously Vercel), author of Sonner (toasts) and Vaul (drawers), teaches the animations.dev course.
- **Status:** articles free on emilkowal.ski; his design engineering skill files are public on GitHub. The animations.dev course is paid and was not read.
- **Read, October 2026:**
  - "Great animations": https://emilkowal.ski/ui/great-animations
  - "7 practical animation tips": https://emilkowal.ski/ui/7-practical-animation-tips
  - "You don't need animations": https://emilkowal.ski/ui/you-dont-need-animations
  - "Developing taste": https://emilkowal.ski/ui/developing-taste
  - Skill files in https://github.com/emilkowalski/skills: `skills/emil-design-eng/SKILL.md` (674 lines, read in full) and `skills/apple-design/SKILL.md` (290 lines, read in full)
- **Who recommends him:** widely cited by design engineers; Rauno Freiberg and Vercel's guidelines carry the same rules (tooltips, frequency, transform-origin).

## Philosophy

- **Taste is trained, not innate.** Surround yourself with great work (Jobs: "expose yourself to the best things that humans have done"), analyze why you like it, practice and get critique (Ira Glass's taste gap). When "it works" is a commodity (AI makes it cheap), taste is the differentiator.
- **Unseen details compound.** When a feature behaves exactly as assumed, people proceed without a thought. That is the goal.
- **Beauty is leverage.** Good defaults and good motion differentiate.

## Decision framework

1. Frequency: 100+ times a day, no animation ever; tens of times, remove or reduce; occasional, standard; rare, delight allowed. Never animate keyboard initiated actions. Raycast has no open animation.
2. Purpose: spatial consistency, state indication, explanation, feedback, preventing jarring changes.
3. Easing: entering or exiting ease-out; moving on screen ease-in-out; hover and colour ease; constant motion linear; never ease-in. Custom curves: `--ease-out: cubic-bezier(0.23, 1, 0.32, 1)`, `--ease-in-out: cubic-bezier(0.77, 0, 0.175, 1)`, `--ease-drawer: cubic-bezier(0.32, 0.72, 0, 1)`.
4. Duration: press 100 to 160ms, tooltips 125 to 200ms, dropdowns 150 to 250ms, modals and drawers 200 to 500ms; UI under 300ms; 180ms select beats 400ms.

## Component rules

- `scale(0.97)` on `:active` (0.95 to 0.98) with a 160ms ease-out transition.
- Never animate from `scale(0)`; start at 0.9 to 0.95 with opacity 0.
- Popovers use `transform-origin` at the trigger; modals stay centred.
- Tooltips: delay the first, then instant with no animation (`data-instant`, 0ms).
- CSS transitions (interruptible, retarget) over keyframes (restart) for rapidly triggered UI.
- `filter: blur(2px)` to blend a crossfade that looks like two objects; keep blur under 20px.
- `@starting-style` for enter animations without JS.
- `translateY(100%)` (percent of own size) for drawers and toasts.
- clip-path `inset()` for reveals, tab colour transitions (duplicate tab list, clip the active copy), hold to delete (2s linear while pressed, 200ms ease-out on release), comparison sliders.
- Asymmetric timing: slow where the user decides, fast where the system responds; exit faster than enter.
- Stagger 30 to 80ms between items; never block interaction during stagger.

## Springs

- Use for drags with momentum, "alive" elements, interruptible gestures, decorative pointer tracking (`useSpring(mouseX * 0.1, { stiffness: 100, damping: 10 })`). Decorative only: a banking chart should not wobble.
- Apple style `{ type: "spring", duration: 0.5, bounce: 0.2 }`; keep bounce 0.1 to 0.3 when used; most UI no bounce.
- Springs keep velocity when interrupted; CSS keyframes restart from zero.

## Gestures

- Dismiss on distance OR velocity (`abs(distance) / elapsedMs > 0.11`).
- Damping past boundaries; friction instead of hard stops.
- Pointer capture; ignore extra touches after a drag starts.

## Performance

- Only `transform` and `opacity`. Avoid changing an inherited CSS variable per frame on a container with many children.
- Framer Motion `x`/`y` shorthands run on rAF (main thread) and drop frames under load; a full `transform` string is hardware accelerated. Vercel's dashboard tabs dropped frames until moved to CSS.
- CSS animations and WAAPI stay smooth when the main thread is busy.

## Accessibility

- Reduced motion = fewer and gentler, keep opacity and colour, remove movement.
- Gate hover with `@media (hover: hover) and (pointer: fine)`.

## Sonner principles (building loved components)

Great developer experience (one `<Toaster />`, call `toast()` anywhere); good defaults matter more than options; naming creates identity; handle edge cases invisibly (pause timers when the tab is hidden, fill gaps between stacked toasts so hover holds, capture pointer during drag); transitions not keyframes; a docs site people can play with. Cohesion: Sonner is slightly slower than usual and uses `ease` to feel elegant, matching its name and look.

## Process

Review the next day; play at 2 to 5x slower or frame by frame; test gestures on real devices.

## Apple design notes (his apple-design skill)

Distills Designing Fluid Interfaces and The Details of UI Typography for the web: respond on pointer down; 1:1 tracking with grab offset; interruptibility from the presentation value; springs with damping 1.0 default and about 0.8 after momentum (Apple sample values: reposition 1.0 / 0.4, rotation 0.8 / 0.4, drawer 0.8 / 0.3); velocity handoff (`velocity / (target - current)` when an API wants relative velocity); Apple's projection function with deceleration 0.998; rubber band `(over * dim * 0.55) / (dim + 0.55 * abs(over))`; translucent chrome with `backdrop-filter: blur(20px) saturate(180%)` and a bright top edge; never stack light translucent surfaces; vibrancy (heavier, higher contrast text on glass); scroll edge fades instead of 1px borders; materialize glass by animating blur and scale; tracking negative on large text (about -0.02em), body near 0; reduced motion, reduced transparency and increased contrast fallbacks.

## Used in

`../../premium/motion-and-feel.md`, `../../premium/details-and-polish.md`, `../../premium/materials-depth-light.md`, `../../premium/premium-feel.md`.
