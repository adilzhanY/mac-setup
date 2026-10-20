# Lessons: what was rejected, what broke, what fixed it

# Bauwerk (desktop, light, AI)

## The rejected first version (60 s)

It was a demo with screenshots: captures of the real app (signed in with test accounts, AI run for real) placed in a floating window, a drawn cursor clicking on them, titles on the left. The user said:

- "i don't really like it"
- "use my Apple cursor for this video, i don't like the cursor there"
- "i don't like that you just made screenshots and drew elements there. i don't need to see the full UI"
- "build separate parts of an app like multi user chat, changes in 3d building, AI detection animation which looks very attractive"
- "make it 30 seconds instead of 60, use only drawn elements"
- "i don't need to see full UI like it's a demo video, but an commercial where for example search bar is floating in the center where you type the address of the building, then it zooms in to that building on the map"
- "write a script of every second"

What they liked in the second version: everything drawn, the floating search, the dive into the real map, the rising city, the AI tracing an old plan, the facade scan, the live team, G to B, the end card.

Earlier asks that still apply: Apple-like animation, spring animations, smooth transitions, the product's font (IBM Plex Sans), real icons, music with clicks, AI generation, wall and opening creation, typing and slider sounds, text explaining each step as ad copy (not like a lesson), research before building.

## Bugs and their fixes

| Symptom | Cause | Fix |
|---|---|---|
| WebGL context fails in render | wrong GL backend | `--gl=swangle` |
| Camera ignores settings | `perspectiveCamera makeDefault` did not take over | a Rig that sets the default camera in `useLayoutEffect` |
| City data never shows | fetched inside the canvas, drawn before it arrived | `delayRender` in the owner, mount the canvas after data |
| Building stays navy in the full render, fine in stills | a mutated `THREE.Color` passed as a prop never updates | pass a fresh hex string each frame |
| Camera spins a full turn in 0.6 s | interpolated to `angle + 360` by mistake | interpolate between the real start and end angles |
| Small jump in the camera at a join | next segment started from a guessed value | start each segment from the previous one's end values |
| Far city pops into view | fog switched off at a frame | keep fog until the city is gone |
| Flat map buildings look 3D | shadow pass ignores the vertex shader | `customDepthMaterial` with the same injection |
| City wave over in 0.3 s | tiny delay per metre and a fast spring | 0.2 frames per metre, back out over 0.6 s, tilt starts before the rise |
| Streets show as round blobs | ribbon quads culled (winding) | `side: DoubleSide` |
| Map washed out | lighting multiplies the flat map colours above 1 | unlit while flat (mix outgoingLight with diffuse by rise) |
| City fade looks ghostly | transparent 3D geometry overlapping | sink in a wave plus a ring cut, dark stage behind |
| Detection boxes hidden during the scan, offset later | coplanar overlay in a preserve-3d context sorts behind; `perspective()` inside the hierarchy misaligns | overlay translateZ 1 to 2 px, no nested perspective keystone |
| Report image tiny in a corner | Tailwind preflight `img { max-width: 100% }` | `maxWidth: "none"` |
| `findLastIndex` type error | TS target too old | target ES2023 |
| `three` has no types in the video project | types live in the app | tsconfig `paths` to `@types/three` |
| Cursor visible at the wrong time | visibility logic accumulated wrongly | last event wins, fade 8 frames |
| Remote cursor slips off a dragged thumb | different easings | the cursor segment uses the value's easing |
| Overpass 406 / 504 | no User-Agent / busy | plain User-Agent, retry; never put the user's email in a header |
| Old video: material colours, 3D angles looking into an open gable | camera on the wrong side | sweep renders every 30 degrees to choose angles |

## Process lessons

- A still is not a frame of a film. Always render a full draft and review frames around transitions before calling it done.
- Sweep a 3D object every 30 degrees once to find its best angles before planning camera moves.
- Real geometry beats invented geometry, but even it out for a commercial (regular bays, a full window grid; real data had a storey without windows).
- Write the script before any code, and the cue list before the scenes: changes then cost one edit.
- Say "measured, not heard" about audio, every time.

# torq (mobile, dark, no AI)

The brief was "a 30 second video about torq, show how good you are in motion graphics, make me feel like it was made in After Effects". The user's verdict: "good". Then they asked for this skill to learn from it, naming two things to generalize: not every project uses a cursor, and never use licence protected material.

## Decisions that held

- No cursor: a phone app. Taps as press plus ripple.
- Left out the app's own streak Lottie and exercise GIFs because the project's docs recorded their licences as unclear. Wrote "For Android" instead of a store badge. Fictional friend names.
- Kept the product's wording rule ("of competitive lifters") and its real data (the OpenPowerlifting quantiles bundled in the app).
- Dark stage throughout, contrast from the lime; the magic moment was the ranking engine, not an AI.
- Two 3D shots (a barbell loading, a rank medal forged) carried the After Effects feel; everything between them was 2D UI and data.

## Bugs and their fixes

| Symptom | Cause | Fix |
|---|---|---|
| A vertical rod through the plate when the camera looked down the bar | one torus inside the rotated plate group was left in its default plane | rotate every ring by pi/2 about x inside the group |
| The 3D logo lit inside out | geometry flipped on y only (SVG is y down), reversing winding | flip y and z together |
| The medal showed an empty face every half spin | emblem only on the front | emblem on both faces, symmetric field |
| Bloom before the drop barely visible | glow layer behind the 3D canvas, hidden by the object | glow on top with `mix-blend-mode: screen`, eased standard and squared |
| "GO" readable for two frames | the label faded out before the dot fold began | fade the label after GO, start the fold 5 frames later |
| Leaderboard still leaving while "Show up." entered | exits started 4 frames before the next act | exits start 20 frames earlier and finish before the act boundary |
| "+35 kg" reached 35 while the line was in month 3 | the counter had its own easing | the counter counts cue ticks generated from the line head's formula |
| The payoff hit landed on an almost empty frame | content started 6 frames after the cut | the number arrives on the hit frame with a pop from 1.25x out of a blur |
| Weight counter digits clipped at the top | overflow hidden box as tall as the font size | box and line height 25 percent taller than the font size |
| Line head floating off the curve between months | head interpolated linearly between knots | evaluate the same cubic segments the path uses |
| package.json and node_modules pruned after the render | an npm subcommand rewrote package.json (cause not pinned down) | pin exact versions, keep the project in git, check package.json after npm commands |

# Sendoku (mobile, true black, 3D digits)

The brief: "create a video about sendoku app, use 3D animations for filling the cells, show numbers in 3D, dynamic music that keeps the viewer watching". The picture landed ("i like the video itself"): 3D digits extruded from the app's own Inter (converted to three.js typeface JSON with fontTools, since `TTFLoader` pulls opentype from a CDN), a real X-Wing pulled from the app's solver with a temporary test, a 3D level tower, the real 4,000 puzzle catalog as an instanced field whose dive hands off to the logo at the same pixel size.

## The music was the same as the last film

The user: "the music is the same for all videos that you create using this skill... the rhythm is identical which is kinda bad". Measured afterwards: torq and Sendoku had groove similarity 0.98, harmony 1.00 (both A minor) and palette 0.80. Every film had been 120 BPM with the same four on the floor and bouncy bass, because the skill said 120 BPM was ideal, gave one arrangement with fixed frames, and told the sound agent to start from the closest example synth.

Fix: `references/music.md` (a new score per film, with a contract), `music/registry.json` (every film's choices and fingerprint), `audio/fingerprint.py` (fails a score that repeats one), and a real audio kit (21 genres as data, a large instrument library, theory and motif tools, key aware effects, a score engine driven by `music.json`). `lib.ts` reads tempo and form from `music.json`, so the picture's grid follows the music instead of a fixed 30 frame beat.

## Bugs and their fixes

| Symptom | Cause | Fix |
|---|---|---|
| Opening second weak: tiny digits far away, glare on the tiles | the camera started on the whole board and the first clues landed in the far corner | open close on the first clue's corner and pull back with the wave; lower metalness and key light |
| Neighbour boards vanished on the cut to the logo | the dive filled the frame with one board but its neighbours were still on screen | fade every board but the target (a `uSolo` uniform) over the last 20 frames |
| Stop line cut through a level name | the line was projected at the slab's front centre, the names at its corner | place it halfway between the two labels' projected positions |
| Pencil marks wrong | candidate bit for digit d is `1 << (d - 1)` in the engine | read the engine's bit layout before decoding |
| Score hissy (37 percent of energy above 8 kHz in a dnb sketch) | a long noisy ride on 8ths | rides are mostly ringing tone; `dsp.balance` keeps 3 to 10 percent above 8 kHz |

## Where it is shown changes everything

After the film was done the user asked whether an ad must be 30, 45 or 60 s. It depends on where it is shown, and the answer exposed a gap: the Sendoku film, a drawn commercial, would not pass Google Play's preview guidance (at least 80 percent real app experience, the real app within 10 s, no call to action text), and Apple only takes screen captures of the app. Its 16:9 frame also does not fit TikTok, Reels or Shorts. The user asked for the skill to ask first. Now it does (`intake.md`), and every destination's rules are in `destinations.md`, with formats and safe zone guides in the kit.
