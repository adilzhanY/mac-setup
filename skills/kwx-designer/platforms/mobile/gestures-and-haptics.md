# Gestures, reach and haptics

How people actually hold phones, which gestures they already know, how to make gestures discoverable and fluid, and how to use haptics so they mean something. Sources: Steven Hoober (UXmatters 2013 and 2017, Smashing "Fitts's Law in the Touch Era", Touch Design for Mobile Interfaces), Apple HIG gestures and haptics, WWDC18 "Designing Fluid Interfaces", Android haptics design principles, NN/g contextual swipe and bottom sheets, GNOME and KDE HIG gesture rules.

## Contents

1. How people hold and touch phones
2. Where to put things (the center out rule)
3. Standard gestures people already know
4. Custom gestures and discoverability
5. Swipe actions on rows
6. Making gestures feel fluid
7. Haptics: when and which
8. Tests

## 1. How people hold and touch phones

Hoober 2013 (1,333 observations, 780 people touching the screen, in the street):

| Grip | Share |
|---|---|
| One handed | 49 percent (right thumb 67, left thumb 33) |
| Cradled (held in one hand, tapped with the other thumb or finger) | 36 percent |
| Two handed | 15 percent (90 percent of those in portrait) |

Hoober 2017 refinement: about 75 percent of touches are made with one thumb, but fewer than half of people hold the phone in one hand. People change grip often, sometimes every few seconds, usually when the task changes.

Consequences:

- Do not design for "the right thumb". Design for any grip and both hands. Left handed and cradled use are a third or more of real use.
- People shift grip to reach hard spots. A hard to reach control is not "safe", it is just slower and gets a grip change.
- Hoober himself withdrew the old curved "thumb zone" heat map: later studies showed people prefer the center. Do not cite the green/yellow/red thumb arc as a rule.

## 2. Where to put things (the center out rule)

- People look at and tap the center most, and scroll so what they read sits in the middle. Touch accuracy is best in the center (7 mm targets work) and worst at edges and corners (11 to 12 mm needed).
- Put primary content and its direct actions in the central scrolling area (list rows, cards, inline buttons).
- Put secondary, persistent controls along the top and bottom edges: tabs, search, compose. Make them bigger than the minimum (46 to 48 pt / 48 to 56 dp tall).
- Put tertiary functions behind a menu, typically from a corner.
- Do not assume the bottom is "easy" and the top is "hard". NN/g also notes the middle of the screen, not the bottom, is generally easiest to tap. Bottom placement helps one handed reach on tall phones, but the bottom edge still needs bigger targets.
- Hoober's three zone layout: content in the middle, persistent navigation and key actions on the top and bottom edges, rare functions in menus.
- Keep destructive actions away from frequent ones and away from where a thumb rests while scrolling.

Good: Mail puts Compose bottom right, a full width list in the middle, and filters at the top. Bad: a row of four 32 pt icons hugging the bottom corners with 4 pt gaps.

## 3. Standard gestures people already know

| Gesture | Expected meaning (all platforms) |
|---|---|
| Tap | Activate, select |
| Swipe / drag | Scroll, reveal actions, dismiss, move |
| Long press | Reveal more (context menu, drag lift) |
| Double tap | Zoom in / out, or like in media feeds |
| Pinch | Zoom; two finger rotate rotates |
| Edge swipe from leading edge (iOS) / either side (Android gesture nav) | Back |
| Swipe down on a sheet | Dismiss |
| Pull down at top of list | Refresh, or search in some apps |
| iOS three finger swipe left / right, shake | Undo / redo |
| iOS three finger pinch in / out | Copy / paste |
| iPad four finger swipe | Switch apps (system) |

Rules:

- Never redefine a standard gesture to mean something app specific (HIG). Tap always activates, swipe always scrolls or reveals.
- Never use a custom gesture for a standard action.
- Do not fight system gestures: bottom edge (home), side edges (Android back), top edge (notifications, Control Center). GNOME and KDE also reserve three and four finger gestures and top and bottom edge drags for the system; apps get two finger gestures and side edge drags.
- Single tap waits up to about 0.5 s when a double tap is also possible on the same element (WWDC18). Do not add double tap to buttons; it slows every single tap.

## 4. Custom gestures and discoverability

A custom gesture must be (HIG):

- discoverable,
- easy to perform,
- distinct from other gestures,
- never the only way to do an important action.

Rules:

- Every gesture has a visible equivalent: a button, a menu item, or a toolbar control. Swipe to delete also has Edit, then Delete. Swipe to go back also has the back chevron.
- Teach gestures with visual hints, not tutorials (WWDC18): clipped content at the edge suggests horizontal scroll, page dots suggest paging, a grabber suggests a draggable sheet, an element that grows toward the finger hints at where it will go.
- If you cannot describe the gesture in one short sentence with a simple picture, people will not learn it (HIG).
- Show when a gesture is not available. A locked item that silently refuses to move looks frozen (HIG). Give a small resistance or a shake.
- Halide's rule: a pro tool builds muscle memory only if gestures stay consistent and buttons do not move around. Vertical drag for exposure and horizontal for focus maps to physical camera dials.

## 5. Swipe actions on rows

- Reserve row swipe for the common or destructive action users expect (delete, archive). Hiding a primary action like "save" behind a swipe makes it undiscoverable (NN/g).
- One meaning per direction per app. Do not make the same swipe do different things depending on the row state or screen.
- Full swipe destructive actions get an easy Undo (snackbar or toast) instead of a confirmation if the action is frequent; confirm if it is rare and costly.
- Keep the item's title visible while the swipe actions show.
- Max two actions per side; more becomes a menu.
- Swipe on rows must not conflict with the back edge swipe: start row recognition a little in from the leading edge.

## 6. Making gestures feel fluid

From WWDC18 "Designing Fluid Interfaces":

- Respond instantly. Highlight on touch down, act on touch up, cancel if the finger slides off. Remove timers and delays from the path; detect a pause from deceleration, not from a fixed wait.
- Track one to one. The element stays under the finger for the whole drag.
- Allow interruption and redirection at any moment. A user who starts closing a sheet can grab it mid animation and pull it back.
- Project momentum. On release, compute where the flick would land using velocity and the scroll deceleration rate, then snap to the nearest valid endpoint to that projection, not to the nearest endpoint to the finger.
- Use springs described by damping ratio and response, not by duration. Default 100 percent damping (no overshoot). Use a little overshoot (about 80 percent) only when a flick with momentum drives the motion.
- Rubber band at boundaries so the user can tell "at the end" from "frozen".
- Keep spatial consistency: what leaves to the right comes back from the right; a sheet that rises from the bottom returns there.
- Small input, big output: a short flick can travel far.
- Gesture hysteresis on iOS is about 10 pt; do not start a drag on 1 or 2 pt of jitter.
- 60 fps minimum, 120 on ProMotion. What is in the frames matters too (motion blur, stretch).

## 7. Haptics: when and which

Principles (Apple and Android agree):

- Less is more. The best haptic is one people do not notice but miss when it is off.
- Pair every haptic with a visible change and, where used, sound. Match strength and sharpness to the animation.
- Use the system meaning of each pattern; never reuse a "success" pattern for failure.
- Make haptics optional and keep the app fully usable without them.
- Do not play haptics while the camera, microphone or gyroscope is capturing.

iOS feedback generators:

| Type | Use for | Example |
|---|---|---|
| Notification: success / warning / error | Outcome of a task | Payment sent, form error |
| Impact: light / medium / heavy / soft / rigid | Physical metaphor, something lands or snaps | Card snaps into a slot, sheet hits a detent |
| Selection | Value changing step by step | Picker wheel, segmented scrubbing |

Standard controls (toggles, sliders, pickers) already play these; do not double them.

Android:

- Use `HapticFeedbackConstants` that match the action (for example CONFIRM, REJECT, LONG_PRESS, CLOCK_TICK, KEYBOARD_TAP, GESTURE_START / GESTURE_END, TOGGLE_ON / OFF, SEGMENT_TICK) via `View.performHapticFeedback` before writing custom effects; then `VibrationEffect` predefined effects and `VibrationEffect.Composition` primitives.
- Prefer crisp "clear" haptics. Given a choice between buzzy vibration and nothing for touch feedback, choose nothing.
- Avoid `createOneShot` and `vibrate(long)` for feedback: a keyclick should be 10 to 20 ms and a long one shot rings on for 20 to 50 ms after, which feels buzzy.
- Scale strength to importance: very frequent events (scroll ticks, text handle) very subtle; form submit or refresh stronger than a toggle; ramp tick strength as a drag approaches its snap target.
- Rich haptics need better actuators; always have a fallback.

Craft examples: Things 3 plays haptics on lifting a task, dropping the Magic Plus button and pull to search, which gives touch "depth". Flighty and Apple Pay use a success notification only when the real world outcome is confirmed.

## 8. Tests

- Hold the device in each grip (right thumb, left thumb, cradled, two thumbs) and do the top three tasks. Any task that needs a grip change for a frequent action fails.
- For every gesture, find its visible equivalent. Missing one fails.
- Drag every draggable thing and reverse halfway. If it does not follow or jumps, fails.
- Disable haptics in system settings. The app must still communicate every outcome visually.
- Count haptics in a 30 second normal session. More than one every few seconds outside of scrubbing is overuse.
