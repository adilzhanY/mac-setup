# Transitions that worked, and how to build them

Every transition needs a sound (whoosh, impact, swell, silence) and should land on the grid. Code: `templates/examples/bauwerk/src/` (CityAct, Search, Facade, HeroAct, EndAct) and `templates/examples/torq/src/` (BarAct, LogAct, EngineAct, ForgeAct, FriendsAct, PayoffAct, EndAct).

## Object handoff (match cut through an object)

The search result's pin badge leaves its row, flies on an arc to the screen centre, and lands as the map pin on the building. Everything else in the search UI scales to 0.94, blurs 12 px and fades over 16 frames around the badge's origin (`transformOrigin` at the badge), so the eye follows the one object that continues.

- Badge path: `mix(start, centre, t)` with `y -= sin(pi t) * 60` for an arc, scale `1 + 0.25 sin(pi t)`, EASE.inOut over 28 frames.
- Sound: click, then a whoosh peaking mid flight, then a "pin" (pitched tock plus low thump) on landing, with a ripple ring expanding on the ground.

## Exponential dive with a swirl

From a blurred map behind the UI to the building: camera distance `logMix(1320, 170, t)` over 60 frames with EASE.inOut, azimuth turning about 80 degrees so the map arrives upright, elevation starting to tilt in the last 36 frames. The map behind the search was blurred (9 px) and at 50 percent opacity; both clear in the first 30 frames of the dive.

## Map to 3D, the city rises in a wave

At the bar: tilt from top down to about 34 degrees while every building rises from flat in a wave from the hero building outward. Per building: delay 0.2 frames per metre of distance, back-out rise over 0.6 s (about 6 percent overshoot). The hero rises first and a bit slower (0.75 s). Map colours (flat, unlit, light grey on white streets) blend into lit clay white as each building stands. Sound: kick and bass enter, a low boom, a rumble under the wave. Implemented as a vertex shader (see `three.md`).

## Lights down from the subject (mood change)

To go from the bright city to the dark AI scene, the city sinks back into the ground in a wave from the hero building outward while the ground and streets vanish inside a growing ring (20 m per frame), revealing the dark stage underneath. Then the hero's roof lifts off and fades while its walls sink. Transparency fades of 3D geometry looked ghostly; sinking plus a ring cut looks intentional. Sound: whoosh, filter closes, chords go minor.

## 3D to 2D to 3D (object metamorphosis)

The building lowers into its own ground floor plan: as the walls sink, an old paper plan of that floor appears exactly where the walls were (corner pinned onto the ground, upright on screen because the camera looks straight down with the street at the bottom). The AI traces it. Then the camera tilts down and the traced walls rise as a white 3D model of that floor while the paper fades. The corner pin keeps the 2D layer glued to the 3D ground during the tilt, so the swap from SVG lines to 3D walls is invisible.

## Hard cut on the bar

Dark to dark, from the plan model to the facade photo, exactly on bar 5. A hard cut is fine (Apple uses them) when it lands on a downbeat and the next shot starts with motion (the card falling in).

## Card drop

The photo card falls from 1000 px above with spring "pop", rotating from -9 to -1.5 degrees, landing about 22 frames later. Sound: whoosh in, soft paper thud on landing.

## Peel off in depth

The found windows lift off the photo: the card turns in 3D (rotateY -26, rotateX 12, perspective 1700) while each window box translates up to 170 px in Z, staggered by column and row; the photo dims to 35 percent brightness and desaturates. Needs `transformStyle: preserve-3d` on the card and the overlay; keep the overlay 1 to 2 px in front in Z from the start or it renders behind the photo.

## White bloom into the drop

Over the last 28 frames before the drop: a radial white fill grows from the centre (opacity ramps with ease in) while the card scales up 12 percent. The drop scene starts with a white overlay fading out over 18 frames. Sound: riser ending on the cut, half a beat of silence, then the impact.

## Cascade on (results arriving)

Windows pop onto the 3D facade along a diagonal from the bottom left: delay = (storey + column) x 3 frames, spring pop scale from 0. The side facade follows 28 frames later. Sound: a cascade of tiny glass tings under the drop.

## Defocus to the payoff

Panels exit (up, blur, staggered), the 3D layer blurs 16 px, scales 1.06, dims 35 percent; the payoff (G badge, drawn arrow, B badge, counter) pops in the centre. The arrow draws with `stroke-dasharray` and `stroke-dashoffset` (trim paths). Sound: one beat of stop, then the hit.

## Make room (payoff to deliverable)

The payoff block moves up 300 px and scales to 0.55 while fading, and the report slides up from 700 px below with a 28 degree rotateX from its bottom edge (spring settle). Sound: paper swish.

## Out to the end card

Everything scales to 0.92, blurs 10 px and fades over 28 frames; the end card is on a white stage. The logo builds: three blocks scaleY from their base with spring pop, 5 frames apart, each with a tonal tap (marimba in key). The wordmark rises out of a clipping slot (overflow hidden, translateY 110 percent to 0, blur clears). Tagline word by word, then the URL pill, then the cursor glides to the URL and turns into the hand. The whole card drifts to 102.5 percent scale over 4 s.

## Do not

- Cross-fade two full scenes (looks like an edited video, not motion design).
- Fade 3D geometry with transparency over a changing background (ghost overlaps).
- Cut off the beat.
- Leave a scene completely static while waiting for the next cut.

## Shape match cut through a rush (torq)

The 3D camera rushes along the bar's axis into the outer plate until the plate's lime ring fills the frame (distance `logMix(2.45, 0.5)`, EASE.in, azimuth to 90 degrees so it looks straight down the axis). On the bar line, cut to 2D: the same ring at the same radius on screen (measure it: ring radius in metres x 540 / (dist x tan(fov / 2))), which then settles small as the rest timer with the camera spring. The eye keeps the circle and never registers the cut. Sound: whoosh peaking 15 frames before the cut, boom on it.

## Collapse to a dot, the dot becomes a character (torq)

A scene ends by folding into one point: the rest ring shrinks (radius and stroke both to a dot, EASE.in over 10 frames) and flies to where the next scene needs it. The next scene opens with that dot hanging, bobbing slightly, and later it drops into place as "you" in a particle chart. One small object carried through three scenes gives the film a protagonist.

## Spin hides the swap (torq)

To change a 3D object's material or identity (Rust to Iron to Bronze), start a full 360 degree spin on the hit (expo out over 26 frames) and swap the colour on the hit frame under a white emissive flash that decays over 14 frames. The spin's speed and the flash mask the change; the slowing spin shows off the new metal. Accelerate the hits (45, 30, 30, 22, 15, 15 frames apart on the grid) and end in a flywheel spin (angle += 0.0055 x frames squared).

## Bloom to black, flash to the drop (dark brands)

Over the last 37 frames before the gap: an accent glow grows from the object's centre ON TOP of everything with `mix-blend-mode: screen` (white hot core, accent ring, transparent edge, opacity eased standard, squared). A glow placed behind a 3D object is hidden by it and reads as nothing. On the gap: pure black for 15 frames with dead silence. On the drop: a near white accent tint over the frame fading over 20 frames, the result already in place under it, sparks and rays starting on the same frame, a camera jolt (view offset shake decaying over 5 frames).

## 3D object becomes a 2D list item (torq)

The Elite medal shrinks into the "You" row's badge on the friends board: transform the whole canvas layer (translate plus scale around the medal's projected centre) toward the badge's position, scale = badge frame height / (medal frame height in pixels), with the medal's pixel size from `pxPerMetre(camera, centre)`. EASE.inOut over 22 frames, fade in the last 4 frames; the 2D badge is there from the first frame of the next scene. The row's other content enters after the badge, so the object lands first and the UI builds around it.

## Rows exit, the next scene builds (torq)

Leaving a dense UI: rows exit up into a blur 2 frames apart, the header and copy a few frames earlier, all done before the next scene's first word enters. Then the new scene's title rises word by word on an empty stage.

## Hard cut on the hit

A hard cut on a downbeat works when the first frame after it already moves: a number arriving with a pop from 1.25x out of an 8 px blur, a medal falling in with a tilt. A cut onto an empty frame with the content starting 6 frames later reads as a dropped frame.
