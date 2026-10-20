# Craft: how motion should feel, with numbers

Everything here is in frames at 60 fps unless it says otherwise. The code lives in `templates/kit/src/lib.ts` and `templates/kit/src/kit.tsx`.

## The grid

- The grid is the film's own: tempo, meter and form come from `src/music.json` (see `music.md`), and `lib.ts` turns them into `BEAT`, `BAR`, `at(bar, beat)` and `SECTION`. At 60 fps a beat is 3600 / BPM frames: 75 BPM is 48, 100 is 36, 112.5 is 32, 128.57 is 28, 144 is 25, 171.43 is 21.
- Never assume 30 frames a beat. A 30 s film is 1800 frames, which is 9.4 bars at 75 BPM and 21 bars at 171.
- Scene starts on bar lines or the form's section starts. Hits (a pin landing, a badge popping, the drop) on beats. Fast repeated events (typing, traced walls, found windows, slider detents) on the genre's subdivision (16ths, 8th note triplets in trap rolls, 8ths in 12/8), or at a steady 2.5 to 5 frame spacing that reads as a run.
- Choose the tempo for the film, not for easy maths: `grooves.FRAME_TEMPOS` lists tempos whose beat is a whole number of frames in every range from 72 to 171 BPM.

## Easing

Linear motion looks cheap. Use these (cubic-bezier control points):

| Name | Curve | Use |
|---|---|---|
| standard | (0.4, 0, 0.2, 1) | general moves, Apple's own UI curve; velocity peaks about 60 percent through |
| out (expo out) | (0.16, 1, 0.3, 1) | entrances: fast start, long soft landing |
| in | (0.7, 0, 0.84, 0) | exits: start slow, leave fast |
| inOut | (0.83, 0, 0.17, 1) | camera moves and morphs between two rests |
| minimum jerk | t^3 (10 - 15t + 6t^2) | a hand moving a mouse from rest to rest; cursors |
| cubic in-out | 4t^3, then 1 - (-2t+2)^3/2 | drags that must match another curve (a slider and its tick sounds) |
| back out | 1 + 2.3k^3 + 1.3k^2, k = x - 1 | things that rise and settle with about 6 percent overshoot (buildings rising) |

Exponential interpolation (`logMix(a, b, t) = a * (b/a)^t`) for zooms and camera distances: equal ratios in equal time, so a 10x zoom feels constant speed.

## Springs (Remotion `spring`)

| Preset | mass, stiffness, damping | Feel |
|---|---|---|
| snappy | 1, 400, 38 | UI that responds instantly, no overshoot |
| settle | 1, 300, 30 | panels and cards arriving, tiny overshoot |
| pop | 1, 260, 16 | results: badges, chips, avatars, pins, windows (visible overshoot) |
| soft | 1, 120, 20 | slow floaty things |
| camera | 1.4, 70, 24, overshootClamping | never overshoots |

Rule: only results overshoot. A camera or a large panel that bounces looks amateur.

## Durations (Apple's UI timings, scaled for film)

- Hover 100 ms, button press 150 ms, modal 250 ms, page transition 350 ms. In film, entrances take 20 to 26 frames, exits 12 to 14 frames.
- A press: scale down 3 frames, back up over 9 (about 0.86 for a cursor, 0.95 to 0.985 for a button).
- Scale changes stay subtle: 94 to 100 percent, never from zero for big panels (zero is fine for small results like pins and windows).
- One element moves at a time, or a clear lead with followers. Restraint reads as premium.

## Entrances and exits

- **Enter**: opacity 0 to 1 (faster than the move), translateY 16 to 20 px to 0, scale 0.96 to 1, blur 8 to 10 px to 0 in the first 14 frames, spring "settle". The blur clears first so the element is sharp while it settles.
- **Exit**: up 14 px, blur to 8 px, opacity to 0, 12 frames, ease in. Exits are faster than entrances.
- **Stagger** 3 to 5 frames between siblings (rows, words, chips), 2 frames on exits.
- **Stretch and settle** for a pill opening from a dot: width leads (spring pop), height follows 4 frames later (spring settle).

## Kinetic type

- Font weight 600 for titles, letter spacing -0.035 em, line height 1.02 to 1.05. Sizes at 1080p: titles 84 to 110 px, secondary 52 to 64, labels 18 to 26. Never below 16.
- Word by word: each word rises 0.5 em out of a 14 px blur with expo out over 24 frames, scale 0.94 to 1 from the baseline, 4 frames apart. Exit: words lift 0.32 em into a 10 px blur over 12 frames, 2 frames apart.
- Accent words (a `*` prefix in `Words`) in the brand colour, or per-word colours (`colors={{ G: red, "B.": green }}`) when the words are values.
- Copy style: short, declarative, two lines of two to three words. "Any address." / "In 3D. Instantly." Never an instruction or a lesson.
- Typed text (a search field): each glyph rises 10 px out of a 5 px blur over 9 frames as its key sound plays; the caret blinks only when idle (every 18 frames), otherwise solid.
- Numbers in a mono font (Geist Mono) with tabular feel; counters count up with expo out and each increment bumps the number's scale by 6 percent for 5 frames.

## Camera

- Always moving: a slow orbit (20 to 30 degrees over several seconds), a slow push in, or a drift. A static frame looks like a screenshot.
- Orbit parameters: target, distance, azimuth, elevation, fov 28 to 32 (long lens looks like product photography). Interpolate parameters, not positions.
- Continuity: at each segment join the camera must have the same parameters on both sides. Write each segment's start values from the previous segment's end values. Never interpolate angles across a 360 wrap by accident.
- Dives use exponential distance plus a rotation (a swirl zoom): the map turns upright on the way down.
- Tilting from top down to oblique while things rise sells 3D. Start the tilt before the rise so the rise is seen in perspective.
- Shift the target sideways (along the camera's right vector) to make room for panels instead of moving the 3D object.
- Depth of field for focus changes: blur the 3D layer 14 to 16 px, scale it 1.04 to 1.06 and dim it while the payoff sits sharp in front.

## Layout at 1920x1080

- Side margins 96 px. Title top left at about (96, 96). Panels in a left column (x 96 to 536) and a right column (x 1380 to 1830), the hero object in the middle third.
- The hero object fills about 60 to 70 percent of the height.
- Overlays standing on 3D (labels) are projected from 3D points every frame and stay upright.

## Colour and light

- Restraint: neutrals plus one accent per scene. The product's brand colour for UI accents. Only a product with AI gets the AI gradient (blue #3d7bff, violet #a855f7, coral #ff5c8a, amber #ffb547).
- Stages come from the brand's tokens. Light brand (Bauwerk): radial from #f7f9fb in the middle to #eaeef2 at the edges, dark stage #0e2236 to #07121e. Dark brand (torq): the page colour (#0E0F0E) to a deeper #060706, with a faint accent tinted pool (#141712 to #10140b) under the hero.
- The rhythm of light is relative to the brand (table in `brief.md`): light brands go dark for the magic moment and bloom white into the drop; dark brands go deeper black, bloom in the accent, cut to pure black for the gap and flash the accent on the drop.
- On a dark brand the accent does all the work: fills, glows, the lit part of a chart, the active segment. Greys only for structure. A whole chart lighting up in the accent in a wave is a strong beat on its own.
- A clay world (white city, soft shadows) with one coloured hero (the real brick building) is the strongest product shot.
- Film grain 4 to 5 percent (animated noise, overlay blend) on everything: no banding, filmic. A soft vignette where needed.

## Pacing

- The music's form (see `music.md`: spine, cold open, slow burn, two drops, beat switch, stop start, minimal pulse, call and response) sets the order of energy, and the story follows it. The spine below worked twice and was then used for every film, so it is now one choice among eight, not the default:
  - Bauwerk (desktop, AI): find (0 to 6 s), the AI reads (6 to 14 s, darker), drop and result (14 s), people together (16 to 22 s), payoff number (22 s), the deliverable (24 s), end card with URL (26 to 30 s).
  - torq (mobile, no AI): the core physical action (0 to 4 s, plates slam onto a bar), the core app action (4 to 7 s, sets ticked, timer runs), the engine on real data (7 to 10 s), the build (10 to 14 s, the rank forged through every tier), gap and drop (14 s, Elite lands), people (16 to 19.5 s, overtaking friends), habit (19.5 to 21.5 s, the streak), stop, payoff number (22 s, +35 kg on a year's line), end card (26 to 30 s).
  - The shared spine: hook, magic moment, build, silence, drop, people or proof, stop, payoff, end card.
- Each shot 1.5 to 4 s. Copy changes with the shot.
- Hold the end card still enough to read the URL; let the music ring out; silence by the last 0.2 s.

## Layout in other formats (see `destinations.md` and `src/formats.ts`)

- **Vertical 1080x1920** (TikTok, Reels, Shorts, Snapchat): everything that carries meaning inside the safe box, x 64 to 838, y 260 to 1210. Copy at the top of the box (titles 96 to 132 px, two to four words a line, left aligned at x 64 or centred on x 451), the hero in the middle (y 600 to 1200), the world and motion filling the whole frame behind. Nothing that matters below y 1210 or right of x 838 under y 560. The hero fills about 60 to 70 percent of the box's width, not of the frame's height.
- **4:5 and square feeds** (1080x1350, 1080x1080): 60 px clear on every side, copy above the hero, type a step bigger than at 1920 wide (titles 80 to 100 px) because the frame is seen small in a feed.
- **App Store 886x1920**: the real recording fills the frame; captions sit in the top fifth, short, 64 to 80 px.
- **TV**: text and logos inside the central 90 percent, action inside 93 percent; hold every line longer (readable from a sofa).
- Lay scenes out from `useVideoConfig()` width and height, not from fixed 1920x1080 numbers, so every format re-lays out instead of cropping. Check every format at its key frames before the full render.

## Readability at 1080p

- Body text in a floating UI part at least 24 px, names and values 34 to 44 px, scaled up roughly 1.5 to 2 times from the app's real sizes. A phone UI shown at its real pixel size looks like a screenshot.
- Small labels (axis ticks, column headers) 18 to 20 px in the faint colour; never the only carrier of meaning.
- A line of copy stays at least 1 s fully readable, and its exit ends before the next scene's first entrance (a leaderboard still leaving while "Show up." arrives reads as a mess).
