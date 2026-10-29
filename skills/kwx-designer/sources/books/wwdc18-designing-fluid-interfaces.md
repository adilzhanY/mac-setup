# Designing Fluid Interfaces (Apple WWDC 2018, session 803; Chan Karunamuni, Marcos Alonso, Nathan de Vries)

## What was read, and where

- Official session page with full transcript: https://developer.apple.com/videos/play/wwdc2018/803/ (transcript read). The talk explains the thinking behind the iPhone X gesture system (home swipe, app switcher, Control Center).

## Key lessons

1. Response is everything: "Everything needs to respond instantly." Hunt down every latency and timer in the touch path. Detect a pause from the finger's deceleration, not a fixed timeout.
2. One to one tracking: the content stays under the finger; use continuous gesture data, not end only recognizers.
3. Constant interruption and redirection: thought and gesture happen in parallel, so any motion can be grabbed and reversed mid flight. One gesture can do many things (swipe home, then keep moving to the switcher).
4. Spatial consistency: what leaves along a path returns along the same path (navigation slides out right and back in from the right).
5. Hint toward the final state: elements grow toward the finger in the direction they will end up.
6. Small input, big output; preserve momentum and transfer it into the interface.
7. Momentum projection: on release, project the end point from velocity and the scroll deceleration rate, then snap to the endpoint nearest the projection (not the finger). Applies to position, scale and rotation.
8. Springs, specified by damping ratio and response, not duration. 100 percent damping (no overshoot) is the default; "A spring doesn't need to overshoot." Reward a flick that has momentum with slight overshoot (Music dismiss uses about 80 percent damping; tap driven motion uses 100).
9. Rubber band at boundaries so "at the edge" is distinguishable from "frozen".
10. Gesture hysteresis on iOS is about 10 pt; double tap support makes single taps wait about 0.5 s, so do not add it where single taps must feel instant.
11. Taps: highlight on touch down, confirm on touch up, cancel by dragging off; give targets extra margin.
12. Teach with the interface: clipped content, page indicators, grabbers, elevated controls; pair gestures with matching animations; use explanations sparingly.
13. Behavior over animation: objects have character (photos feel light, apps heavier) and a family of consistent behaviors.

## Where this lives in the skill

`platforms/mobile/gestures-and-haptics.md` section 6, `platforms/mobile/mobile-foundations.md` section 7, `platforms/mobile/craft-lessons.md`.
