# Motion and feel

How an interface responds is half of whether it feels premium. Apple, *Designing Fluid Interfaces*: when the interface aligns with the way we think and move, "it really stops feeling like a computer, and starts feeling like a seamless extension of us."

## Contents

1. The four questions before any animation
2. Response: latency is the first defect
3. Durations
4. Easing curves (with values)
5. Springs (with values and formulas)
6. Interruptibility and velocity
7. Spatial consistency and origin
8. Enter, exit and the details of a good transition
9. Gestures, drag and momentum
10. Stagger and choreography
11. Reduced motion and accessibility
12. Performance rules
13. Debugging motion
14. Review table (before, after, why)
15. Sources

---

## 1. The four questions before any animation

Answer in order (Emil Kowalski's decision framework, consistent with Rauno Freiberg and Apple).

**1. Should it animate at all?** Decide by frequency.

| How often the user sees it | Decision |
|---|---|
| 100+ times a day (keyboard shortcuts, command palette, app switcher) | No animation. Ever. |
| Tens of times a day (hover, list navigation, context menus) | Remove or reduce to a near instant state change |
| Occasionally (modals, drawers, toasts) | Standard animation |
| Rarely or once (onboarding, celebrations, feedback forms) | Can carry delight |

Never animate keyboard initiated actions (Emil). macOS context menus appear with no motion even though they are used thousands of times a day; the chosen item flashes briefly and the menu fades out (Rauno). The macOS app switcher never animates, and a fast Cmd+Tab switches without showing the switcher at all.

**2. What is the purpose?** Valid answers: spatial consistency (where it came from, where it went), state change, explanation, feedback that input was received, avoiding a jarring jump. "It looks cool" is valid only for rare moments.

**3. What easing?** See section 4.

**4. How fast?** See section 3.

## 2. Response: latency is the first defect

- **People are "really, really sensitive to latency"** (Apple WWDC18). Look for delays everywhere: taps, presses, every interaction.
- **Feedback on pointer down, action on pointer up.** The button highlights the instant it is touched; the action commits on release (Apple, *Designing Fluid Interfaces*, *The Life of a Button*).
- **Never fade in or grow slowly on press.** "That feels unresponsive. If you animate, keep it very fast" (Apple, *The Life of a Button*).
- **Press scale:** `transform: scale(0.97)` on `:active`, range 0.95 to 0.98 (Emil); Rauno gives 0.9 to 0.96 for small buttons. Transition about 100 to 160ms ease-out.
- **Continuous feedback during a gesture,** not only at the end. A drag or slider follows the pointer 1:1 the whole way.
- **Apply the delta immediately.** Rauno's pinch example: applying scale from the first frame tells the user the card can be pinched; waiting for a threshold gives no affordance.
- **Optimistic updates** when success is likely; roll back with a message on failure (Vercel, Rauno).
- **Avoid double tap disambiguation** unless double tap really exists: it delays every single tap by about half a second (Apple WWDC18).

## 3. Durations

| Element | Duration | Source |
|---|---|---|
| Button press feedback | 100 to 160ms | Emil |
| Tooltip, small popover | 125 to 200ms | Emil |
| Dropdown, select, menu | 150 to 250ms (180ms beats 400ms) | Emil |
| Interaction feedback in general | under 200ms | Rauno guidelines |
| Modal, drawer, sheet | 200 to 500ms (prefer a spring, 0.3 to 0.4s response) | Emil, Apple |
| Toast enter | about 400ms with `ease` (Sonner, deliberately elegant) | Emil |
| Marketing and explanatory | can be longer | Emil |
| Hold to confirm (delete) | 1.5 to 2s linear while pressed; 200ms ease-out on release | Emil |
| Spinner show delay | 150 to 300ms before it appears | Vercel |
| Spinner minimum visible time | 300 to 500ms once shown | Vercel |
| Autoplay motion longer than 5s | needs pause, stop or hide control | Vercel (WCAG) |

**Default ceiling: 300ms for UI.** Emil: "UI animations should stay under 300ms." When sources differ (Rauno under 200ms, Emil under 300ms), use the shorter value for small, frequent elements and the longer for large surfaces.

**Exit faster than enter.** The system responding should be fast; the user deciding can be slow (Emil: asymmetric timing).

**Perceived speed:** a faster spinner makes the same load feel faster; ease-out at 200ms feels faster than ease-in at 200ms.

## 4. Easing curves (with values)

Decision tree (Emil):

- Element **entering or exiting**: ease-out (starts fast, feels responsive).
- Element **moving or morphing on screen**: ease-in-out.
- **Hover or colour change**: ease.
- **Constant motion** (marquee, indeterminate progress, spinner): linear.
- Default: ease-out.
- **Never ease-in for UI.** It delays the first movement, exactly when the user is watching.

The built in CSS keywords are too weak. Use stronger custom curves (Emil's tokens):

```css
:root {
  --ease-out:    cubic-bezier(0.23, 1, 0.32, 1);    /* strong ease-out for UI */
  --ease-in-out: cubic-bezier(0.77, 0, 0.175, 1);   /* on-screen movement */
  --ease-drawer: cubic-bezier(0.32, 0.72, 0, 1);    /* iOS-like sheet (from Ionic) */
}
```

- **Linear** has a velocity jump at start and end; use only for repeating or constant motion (Apple WWDC23).
- **Ease curves cannot accept an initial velocity,** so after a gesture they halt abruptly. Use a spring after any gesture (Apple WWDC23).
- **Reversible transitions:** mirror the curve for the return path so the motion is symmetric (Apple, via Emil's notes).
- Match personality: Sonner uses plain `ease` and slightly longer timing to feel elegant; a dashboard uses crisp ease-out (Emil).

## 5. Springs (with values and formulas)

Springs are the default for anything the user can touch, drag or interrupt. They keep position and velocity continuous, from rest or from a thrown gesture (Apple WWDC18, WWDC23).

**Think in two designer parameters, not mass and stiffness** (Apple):

- **Duration / response:** how quickly it gets there (perceptual, in seconds).
- **Bounce / damping ratio:** how much it overshoots. Damping ratio 1.0 = no overshoot. Bounce 0 = no overshoot. Bounce runs from -1 to 1.

**Defaults:**

| Use | Setting | Source |
|---|---|---|
| General UI default | bounce 0 (damping ratio 1.0, critically damped) | Apple WWDC18 "start with 100% damping"; WWDC23 default bounce 0 |
| After a gesture with momentum (flick, throw, swipe to dismiss) | damping ratio about 0.8 (bounce about 0.15 to 0.2) | Apple Music Now Playing swipe uses 80%; tap uses 100% |
| Brisk but not bouncy | bounce 0.15 | Apple WWDC23 |
| Noticeably bouncy, playful | bounce 0.3 | Apple WWDC23 |
| Too much for UI | bounce over 0.4 | Apple WWDC23 "use with caution" |
| Move or reposition (PiP) | damping 1.0, response 0.4 | Apple sample values, via Emil |
| Rotation | damping 0.8, response 0.4 | same |
| Drawer, sheet | damping 0.8, response 0.3 | same |
| Motion / Framer Motion | `{ type: "spring", duration: 0.5, bounce: 0.2 }`, or `{ stiffness: 100, damping: 10, mass: 1 }` | Emil |

Rule: **reward momentum with overshoot; never overshoot something that just appeared** (a menu that bounces after fading in feels wrong, a card you flicked that bounces feels right).

Tuning order: pick the duration for pacing first, then bounce for character (Apple WWDC23).

**Conversion to physical parameters** (Apple WWDC23, mass = 1):

```
stiffness = (2 * PI / duration)^2
damping   = 1 - 4 * PI * bounce / duration        (bounce >= 0)
damping   = 4 * PI / (duration + 4 * PI * bounce) (bounce < 0)
```

**Do not wait for the settling time** to make a user facing change. The spring's tail is long and unpredictable; trigger follow up UI on the perceptual duration (Apple WWDC23).

**Treat behaviours as a family.** Reuse the same few springs across the product so people learn one feel (Apple WWDC18).

## 6. Interruptibility and velocity

The single most important property of fluid motion (Apple: "The thought and gesture happen in parallel").

- **Every animation can be grabbed, reversed or redirected mid-flight.** Never lock input during a transition.
- **Animate from the current on-screen (presentation) value, not the logical target value.** Starting from the target causes a jump.
- **CSS transitions retarget smoothly; `@keyframes` restart from zero.** Use transitions (or springs) for anything that can be triggered rapidly, such as stacking toasts or toggles (Emil).
- **Hand off velocity.** When a drag ends, start the spring with the finger's release velocity so there is no seam. Some APIs want relative velocity: `gestureVelocity / (target - current)`.
- **Track a short history of pointer positions and times,** not only the last point, to compute release velocity (Apple WWDC18).
- **On a reversal, blend velocity** instead of cutting to a new animation (that produces a "brick wall").
- **Decompose 2D motion into independent X and Y springs** so each keeps its own velocity.
- **Decide commit or cancel by velocity direction at release,** not only by how far it travelled.

## 7. Spatial consistency and origin

- **Symmetric paths:** if something leaves one way, it returns the same way. iOS navigation: in from the right, back out to the right (Apple WWDC18).
- **Popovers, menus and sheets grow from their trigger.** Set `transform-origin` to the trigger (Radix `var(--radix-dropdown-menu-content-transform-origin)`, Base UI `var(--transform-origin)`). Modals are the exception: they are not anchored, so they scale from the centre (Emil).
- **Action sheets and menus spring from their source element, not from the bottom of the screen** (Apple, new design system 2025).
- **Toasts enter and exit from the same edge,** which also makes swipe to dismiss in that direction obvious (Emil, Sonner).
- **Hint toward the final state.** Control Center modules "grow up and out toward your finger" before popping open (Apple WWDC18). In-between frames point at the outcome.
- **Source matters when there are many sources.** An app launching from its own icon shows where it came from; Rauno notes the expanded Dynamic Island launches the app from its icon so you know which of several music apps is playing.
- **Glass materializes by bending light, not by fading** (Apple, Liquid Glass). On the web: animate blur and scale together with opacity for material surfaces.

## 8. Enter, exit and the details of a good transition

- **Never animate from `scale(0)`.** Start at 0.9 to 0.97 with opacity 0 (Emil: "Nothing in the real world appears from nothing"; Rauno: dialogs from about 0.8 to 0.95 plus fade).
- **Pair opacity with height** when list items enter and leave; tune by eye, there is no formula (Emil).
- **Use `translateY(100%)` (percent of own size)** to hide drawers and toasts, not a hard coded pixel value.
- **Crossfade looks like two objects?** Add `filter: blur(2px)` during the transition to blend them into one (Emil). Keep blur under about 20px (expensive, especially in Safari).
- **Enter states without JS:** CSS `@starting-style`.
- **Tooltips:** delay the first one to prevent accidental triggers (Radix defaults to 700ms; 300 to 700ms is the usual range); once one is open, neighbours open instantly with no animation (Emil, Vercel, Radix and Base UI behaviour).
- **Theme switch:** no transitions during a light/dark switch (Rauno). Disable transitions for one frame while swapping.
- **Skeletons match the final layout exactly** so nothing jumps when content arrives (Vercel).

## 9. Gestures, drag and momentum

From Apple *Designing Fluid Interfaces*, Rauno *Invisible Details*, and Emil's drawer and toast work.

- **Hysteresis:** require about 10pt (10px) of movement before committing to a drag direction (iOS standard).
- **1:1 tracking with the grab offset preserved.** Do not snap the element's centre to the finger.
- **Pointer capture** (`setPointerCapture`) so the drag continues if the pointer leaves the element.
- **Ignore additional touches** once a drag has started, or the element jumps when fingers switch (Emil).
- **Generous hit area and drag to cancel:** add margin around tap targets; dragging off cancels, dragging back re-arms (Apple, *The Life of a Button*).
- **Flick to dismiss:** dismiss when distance passes the threshold OR velocity exceeds about 0.11 px/ms (Emil, Sonner). A quick flick should be enough.
- **Project momentum to choose the target.** Apple's projection function:
  ```js
  // decelerationRate: 0.998 normal, 0.99 fast
  const project = (v /* px/s */, d = 0.998) => (v / 1000) * d / (1 - d);
  const target = nearestSnapPoint(position + project(releaseVelocity));
  ```
  It works for scale and rotation too.
- **Rubber band at edges** instead of hard stops; resistance grows the further past the edge:
  ```js
  const rubberband = (over, dim, c = 0.55) => (over * dim * c) / (dim + c * Math.abs(over));
  ```
- **Trigger timing matches risk** (Rauno): lightweight, reversible actions can fire mid gesture (search overlay appears while swiping); destructive actions fire only on release, never mid swipe (iOS app switcher never kills an app mid swipe). Let a view snap into place but stay uncommitted until release, so the user can peek and back out.
- **Keep content visible under the finger:** loupe, key preview, and sliders that keep tracking when the finger drifts off the track (Rauno).
- **Every gesture has a click or keyboard alternative** unless the gesture is the point (Vercel).
- **Respect where pointers are fast:** screen corners are infinitely large targets (Fitts); radial menus put every item at the same distance (Rauno).

## 10. Stagger and choreography

- **Stagger groups that enter together,** 30 to 80ms between items (Emil), translateY about 8px plus fade. Never block interaction while a stagger plays; it is decorative.
- **Animate the element nearest the trigger first** to confirm input (Rauno, *Designing Depth*).
- **Delay competing elements** (Rauno: delay the keyboard so it does not fight the suggestions).
- **Blur the layer behind before revealing the layer in front,** so two layers do not collide.
- **Slightly different springs for siblings** read more natural than identical motion (schools of fish; Control Center rows).
- **Stagger on first load only,** not on every return (Rauno, *Novelty*).

## 11. Reduced motion and accessibility

- `prefers-reduced-motion: reduce` means **fewer and gentler** animations, not zero feedback. Replace movement, springs and parallax with short opacity fades (about 150 to 200ms). Keep colour and opacity changes that aid understanding (Emil, Apple, Vercel).
- `prefers-reduced-transparency: reduce`: make glass surfaces frosted or solid.
- `prefers-contrast: more`: near solid surfaces with a contrasting border.
- Avoid full viewport moving backgrounds, slow large oscillations and abrupt brightness jumps.
- Gate hover effects: `@media (hover: hover) and (pointer: fine)` so taps on touch screens do not trigger sticky hover states (Emil, Rauno).
- Pause looping animations when off screen (Rauno).

## 12. Performance rules

- **Animate only `transform` and `opacity`** (and `filter`/`clip-path` with care). `width`, `height`, `top`, `margin`, `padding` trigger layout (Emil, Vercel).
- **Never `transition: all`.** List properties explicitly (Vercel, Emil).
- **CSS animations and WAAPI run off the main thread** and stay smooth under load. rAF based libraries drop frames when the page is busy. At Vercel a dashboard tab animation dropped frames during page loads until it moved to CSS (Emil).
- **Framer Motion shorthand `x`, `y`, `scale` are not hardware accelerated;** use a full `transform` string when the main thread is busy (Emil).
- **Do not drive per-frame motion through an inherited CSS variable** on a parent with many children; set `transform` on the element (Emil).
- **Target 60fps; on 120Hz screens per frame budget halves.** "It's not just about framerate. It's what's in the frames" (Apple): fast motion can use motion blur or stretch.
- **Large `backdrop-filter` blur values are slow;** keep them moderate and avoid animating them on big surfaces (Rauno).
- **`will-change` only during the animation,** as a last resort (Rauno, Vercel).

## 13. Debugging motion

- Review the next day with fresh eyes (Emil).
- Play at 2 to 5x slower, or step frame by frame in the DevTools Animations panel. Look for: two overlapping states in a crossfade, wrong transform origin, properties out of sync, abrupt start or stop.
- Test gestures on a real device, not only a simulator.
- Ask: if I trigger it twice quickly, does it retarget smoothly or restart from zero?

## 14. Review table (before, after, why)

| Before | After | Why |
|---|---|---|
| `transition: all 300ms` | `transition: transform 200ms var(--ease-out)` | Name properties; faster |
| `transform: scale(0)` on enter | `scale(0.95); opacity: 0` | Nothing appears from nothing |
| `ease-in` on a dropdown | `var(--ease-out)` | ease-in feels sluggish |
| No `:active` state | `scale(0.97)` on `:active` | Press must feel heard |
| Popover `transform-origin: center` | `var(--transform-origin)` | Grow from the trigger (modals excepted) |
| Command palette opens with 250ms fade | No animation | Used 100+ times a day |
| Hover lift with 400ms transition | 120 to 150ms, gated by `(hover: hover)` | Frequent, touch false positives |
| Toasts built with `@keyframes` | CSS transitions | Retargets when toasts stack quickly |
| Drawer released, then animates with ease-out | Spring with release velocity | No seam between drag and motion |
| Swipe threshold only by distance | Distance OR velocity over 0.11 px/ms | A flick should be enough |
| Same timing for enter and exit | Exit about 30 to 50% faster | System responses should be snappy |
| Bounce on a menu that just appeared | Critically damped | Bounce only after momentum |
| Spinner shows instantly for 80ms | 200ms delay, 400ms minimum | No flicker |

## 15. Sources

`../sources/books/apple-wwdc-design-talks.md`, `emil-kowalski-design-engineering.md`, `rauno-freiberg-craft.md`, `vercel-web-interface-guidelines.md`.
