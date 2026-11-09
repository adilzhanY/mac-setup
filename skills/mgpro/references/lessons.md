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

# The first three films were clones of each other (sound, measured Oct 2026)

After the Sendoku fix (a new score for every film), the soundtracks of Bauwerk, torq and Sendoku were measured against 129 professional motion graphics films with the same analysis (`sound-research.md`, section 1). The music fix had not gone far enough: the three films were the same film three times, and the habits that made them so lived in the skill, not in any one score.

What was measured:

| Metric | Bauwerk, torq, Sendoku | 129 professional films |
|---|---|---|
| distance between two films' 10 metric profiles | 0.88 to 1.60 | median 4.1 between different makers (10th percentile 2.7); only 0.45 % of 8,256 pairs are as close as the most distant AI pair |
| strong transients shared with another film | torq and Sendoku 42 %, the others 15 to 17 % | median about 5 % |
| tempo | 120.2 BPM, all three | spread 108 to 148 BPM; 29 % have no clear beat |
| loudness | -14.2, -14.1, -14.0 LUFS; true peak -1.36, -0.96, -1.36 | -21 to -10 LUFS |
| the gap | one, at exactly 13.75 s (45.8 %) in all three, dead silence, returning only 3.6 to 6 dB louder | dips (20 dB down) a median 4 per film, clustered at the opening and before the end card; 71 % have no near silence; re-entries come back about +9 dB |
| onsets on the 16th grid | 91 to 100 % | 78 % |
| spectral centroid | 2.3 to 3.0 kHz | median 1.8 kHz |
| onset strength at a picture cut | 18.6 times baseline | 1.18 times |
| loudness range | 3.6 to 4.2 LU | median 5.8 LU |
| first second against the body | -0.2 to +1.4 LU | median -1.9 LU, often far quieter |
| density at 90 % of the length | about 0.5 onsets per second | 3.4 per second |

Causes in the skill: the golden rule "every visual event has a sound" (so every cut was slammed), "silence is the strongest hit" (so every film had one dead gap, placed by the same form at the same frame), a mastering chain that hit -14.0 LUFS exactly, a grid that every effect snapped to, bright hats and risers, a long quiet end card, and a synthesizer whose effects were all the same size: every sound rang about ten times too long, every tonal effect was a pure sine, the impact was 95 percent sub (nearly silent on a phone), and seven different cue names played the same blip (`sfx/ANALYSIS.md`, section 5).

What changed:

- `sound.md` became a practical manual: a vocabulary of sound types with measured targets, layering recipes, material and size, sync tables at 30 and 60 fps with the ITU and EBU tolerances, a hierarchy (hero, support, texture, none) in place of "every event has a sound", variation with numbers, dips in place of dead air, a dynamic arc that moves between films, loudness per destination, small speakers, a worked 40 s plan, and the checks every film must pass ("Why AI films sound the same").
- `music.md`: the contract gained pulse (about one film in three beatless) and shape (dips and the loudest moment placed differently from every earlier film), the whole film distance and shared transient checks, humanising the score, and a darker tonal balance.
- `sfx/`: a CC0 library of 1126 sounds with measurements and contact sheets, used as the reference for what designed sounds look like in numbers and, when a film opts in, as a source of samples (`rights.md`).
- The audio kit was reworked alongside (`templates/kit/audio/CHANGES.txt`): `sfx.py` rewritten with one effect per job and seven characters, every effect inside the library's measured ranges on 665 of 686 measures; cue `weight` (hero, support, ambient) and `cut`; `vary.py` pools so no sound plays the same way twice and no two films share a transient; `samples.py` and the `samples` block for CC0 library sounds; `["dip"]` sections and automatic dips in place of dead gaps; `"beat": false`; a soft opening; a master gain staged so it no longer squashes the range, with the tone shelved toward a 1.8 kHz centroid and 4 kHz rolloff; and `fingerprint.py` with `filmstats.py` and `pro_stats.json` measuring every film against the professional range and the registry (profile distance at least 2.67, shared transients at most 10 percent).
- Two findings from that rework: a cut on a bar downbeat measures 3 to 9 times baseline from the music alone, so only structural cuts sit on downbeats; and a 0.57 s gap before the hero cut made it read 27 times baseline, so the gap is now about an eighth of a bar (about 0.28 s).
- `sound-research.md` holds the evidence, so each rule can be traced to its source.

The lesson: "different genre and tempo" is not enough. A film can pass a music fingerprint and still sound like the last one, because the sameness lives in how sound is placed, mixed and mastered. Measure the whole soundtrack against every earlier film and against the professional range.

# Enogon (desktop and web, light technical drawing brand, AI, German, Oct 2026)

A 40.8 s film for Enogon (enogon.com): an energy consultant uploads a floor plan, the AI recognises walls, doors and rooms, the storeys stack into a 3D model, one click exports it. The first film made with mgpro 2.0.0 (the vizavi merge, the sound research, the reworked kit). The user chose no length ("30 is too fast, 60 too slow"); 40.8 s carried seven scenes with every line readable and no hold over about 5 s. Its whole code is in `templates/examples/enogon/`.

## Decisions that held

- **One object, one continuous camera.** A sheet of paper becomes a building, the building becomes the logo cube. No cut between places: one camera from top down through a 40 degree tilt, an orbit, a push to one wall, a pull back, and a dolly zoom (fov 30 to 8 at a constant apparent size) that flattens the perspective house into the isometric logo.
- **The brand's own drawing language instead of an AI glow.** Enogon's site and app are technical drawings: black hairlines, flat apricot and Türkis fills, mono labels, dimension lines with 45 degree ticks, hatched roofs, sharp corners. The AI was drawn as a draftsman (dashed construction lines first, then apricot walls laid along a ruler with a crosshair reporting the wall id and length), not with the AI gradient Bauwerk used. The film looks like the product, and different from Bauwerk though both are building tools.
- **The product's own copy and data.** The site's headline "Adresse und Grundrisse rein, CAD-Modell raus. In 10 Minuten." became the film's spine ("Grundriss rein." to "CAD-Modell raus."); "Anklicken, anpassen, fertig." is the site's line; the example building (Lichtpausweg 7, 12,40 m, AW 008 at 0,36 m and 2,87 m) is the site's. The only speed claim is the product's own, on the end card.
- **The logo is a box in the model's colours.** The 3D faces are coloured by direction exactly like the logo cube (top apricot, east Türkis, south white), so the house can fold into the cube and the cube hands over to the flat logo.
- **Score**: `cinematic_pulse` at 102.86 BPM in E flat lydian, a 16th note string ostinato like a pen on a ruler, two hero cues only (the roof landing and the logo), an eighth of a bar dip before the roof. It passed every `fingerprint.py` check on the first render: profile distance 3.9 to 5.2 to every earlier film, 0 percent shared transients, centroid 1355 Hz, LRA 7.7 LU, opening -2.4 LU, rise at cuts 2.87x.

## Bugs and their fixes

| What was seen | Cause | Fix |
|---|---|---|
| White facades rendered grey (255 became 226), Türkis greyed | react three fiber tone maps by default (ACES) | `<ThreeCanvas flat ...>`: no tone mapping, flat brand colours come out exact |
| Ink lines along wall bands (at sill and head height) when using `EdgesGeometry` | walls with real openings are built as bands (0 to sill, sill to head, head to top) and the band seams are edges | draw the ink lines analytically (outlines, corners, opening rectangles) as `LineSegments2` fat lines, and push the faces back with `polygonOffset` so the lines win the depth test |
| The dragged file card grew into a blank sheet for 0.7 s before the drawing appeared | the scan lived in the ground layer, which only matched the sheet once it had landed | put the scan inside the paper element itself, so it grows with the card |
| The plan's apricot walls stayed on the ground and showed under the end cube | the plan layer had no exit | every layer gets an exit when its job is done (here, once the 3D walls cover it) |
| "Räume." appeared just as the title left | the drafting events ran to the end of their section | lay out the events backwards from the title's exit; give the last word at least a second |
| A storey falling from 7.5 m passed through the title | a big drop height on a high camera | 4.2 m; check titles against everything that moves into the top third |
| The 3D cube and the flat logo did not line up at the hand over | the logo was placed by hand | project the cube's corners at the swap frame (`cubeRect.ts`), size the SVG to that box, and grow the 3D ink width to the logo's stroke at that size (4.01 / 123 of its height) |
| Picture and sound could drift | event frames were computed in TypeScript and would have been copied by hand into `cues.py` | `scripts/events.ts` (run with `npx tsx`) writes every event frame from the picture's own code to `src/events.json`; `cues.py` reads it |
| The camera stopped dead at every keyframe | eased segments between keys | monotone cubic interpolation (Fritsch and Carlson) through the keys: continuous velocity, no overshoot (`timeline.ts`, `smooth`) |
| The title and the building fought in the edit and model shots | one camera target for both the hero and the copy | frame per scene from stills: raise the target to push the building down, shift it sideways away from the copy column |

## Enogon review (Oct 2026)

The user reviewed the finished 40.8 s film. They liked the new text animations. Everything else below was criticised, in their words condensed, and every point traced to a cause in the skill or the kit. They asked that the skill keep learning from every review: each criticism becomes a rule, a recipe and a line in the self check (`review.md`, Self check), and the next film is checked against all of them.

| What the user said | Cause in the skill or the kit | Fix |
|---|---|---|
| The sounds and music were still AI-like | Every instrument and effect was synthesized; the skill made synthesis the default and samples an opt in for effects only (`rights.md`: "the music is always synthesized"). Measured distinctness (the fingerprint) was taken as quality | Recordings first: CC0 instruments through the sampler (`"instruments": "samples"`), recorded effects, one shared convolution room, round robins, velocity that changes tone, systematic timing (`sound.md`, section 4b; `rights.md`) |
| The same sounds as earlier mgpro films around 12 to 13 s | The kit's synthesized `whoosh` (12.33 s) and `reverse` swell (12.82 s): the same recipes as every earlier film, with only a new seed. The shared transient check (r above 0.9) does not catch a family resemblance | No hero or support job may use the same source as the last film; each job's source is written in `SCRIPT.md` and the registry entry (`sound.md`, sections 4b and 8) |
| The drum hit on the roof landing at 20 s sounded AI-like | A synthesized impact (sub plus knock) under a synthesized taiko, dry, from `sfx.py` and `instruments.py` | Physical hits are recordings (a real drum or knock with velocity layers and round robins), the synth sub only as a layer, in the shared room (`sound.md`, section 4b) |
| On some moments the sound dropped and they barely heard anything | `"dips": "auto"` (the 2.0.0 default) multiplied the whole mix down 24 dB for about 0.3 s about every 7 s, after the reverbs, cutting every tail; the golden rule "Dips, not dead air" turned measured outputs of professional arrangements (20 dB for 0.3 s) into gain automation | Contrast is arranged, never a gain hole; a level change under about 3 dB is not heard and a deep drop with no musical reason reads as a broken mix; every film sets `"dips": 0` until `score.py`'s default changes to arranged breaths (`sound.md`, section 9; `music.md`, Forms) |
| The animation took too much time and was boring | 40.8 s with holds up to about 5 s; the skill allowed "each shot 1.5 to 4 s" and had no rule for change inside a long take | A visible change every 1 to 3 s, the product in the first 2 s, processes compressed, the reading time formula (`craft.md`, Pacing) |
| The building was shown too long | The 3D house stayed the static hero through the storeys, the roof, the orbit and the titles, waiting for copy and music | Never hold a static hero more than about 2 s; give the hero a new change or leave it (`craft.md`, Pacing) |
| The roof hovered, paused, for about a second | The storyboard hung the roof half a metre above the walls for about 1.1 s (18.7 to 19.8 s) to sit under the music's dip before the hero hit: the picture waited for the sound | No pauses inside a fall or a landing; the music moves to the picture (`craft.md`, Pacing; `composition.md`, section 1). The rebuild drops the roof in one move like the storeys |
| Cursor movement quality was bad; it needs different animations like the text has | `Cursor.tsx` 2.0.0: fades in place over 8 frames, one symmetric minimum jerk ease with the same arc every move, a 3 and 9 frame press with no target reaction, ghost copies, about 71 px | Cap's springs, asymmetric ease, duration from distance, varied moves, press with the target answering, tilt, a directional smear, about 7 percent of the frame width, entries and exits through frame edges, the dragged card riding and tilting (`interaction.md`, How it moves; the rebuild's `makePath` and `MacCursor`) |
| The wall drawing should look like Bauwerk's fast traced line, not chunky blocks | The draftsman metaphor was built as apricot wall blocks laid one at a time along a ruler | The fast trace: one continuous line with square corner handles, inner walls, door arcs, room tags, lines thickening into walls, about 3 s for a whole plan (`elements.md`, Fast trace) |
| The music and rhythm should be faster and more dynamic, but still readable | `cinematic_pulse` at 102.86 BPM chosen from the genre's range, not from the cut; energy built mostly by level | Tempo from the cut's hit points, energy built through texture, one lift or drop per 30 s (`composition.md`); the rebuild runs at 112.5 BPM |
| Length should come from content, not seconds | With no length given, the agent took the middle of "30 too fast, 60 too slow" and filled 40.8 s | Add up the beats the story needs (`craft.md`, Pacing: Length comes from the content). The rebuild tells the same story in 26.7 s |
| The transition from the 3D house to the logo was "the worst thing": an x-ray, transparent crossfade from the house into a growing cube | No rule for the logo resolve; transparency on 3D materials during the hand over, two objects half visible at once | One decisive opaque move after a clean frame, decelerating into the mark, sonic accent on the landing, a 1.5 to 3 s hold (`logo-resolve.md`). The rebuild packs the model into a box whose net folds up and closes into the cube (`elements.md`, Box fold) |

**The one mistake under four of them.** The research behind this review (`research/ad-music-and-logo/report.md`) found that the gain holes, the x-ray crossfade, the cursor fading in place and the synth notes with no attack, drift or room are one mistake made four times: **a change shown as a blend between two states instead of one thing transforming for a visible reason.** A music bus multiplied to zero is the audio version of an opacity crossfade; a cursor that fades in where it already is, instead of arriving from somewhere, is the interaction version. Wherever code interpolates gain or opacity between two states, ask what physical or musical event explains the change; if none does, replace the interpolation with an arrangement or a transformation.

**Measurements are checks, not instructions.** The earlier study correctly found that professionals make contrast with short dips, but turning "20 dB for 0.3 s" into gain automation reproduced the number and lost the cause. Output metrics are for checking a render; they are harmful as the instruction that generates one. The same caution applies to every number in this skill, from 6 to 8 round robins to a 149 ms cursor lag.

**Learning from every review.** Every film so far has come back with a review, and the user insists the skill must learn more from each one: write each criticism here with its cause and its fix, add a check for it to `review.md`, Self check, and run that whole list on every new film before it is shown.

## Sound effects review (Enogon v1 and v2, Oct 2026)

After both Enogon films the user asked for a different way of getting sound effects: search premade, human recorded sounds on free sources the way human video editors do, select each one wisely so it sounds normal in the video, and say where to download them and how to use them (what volume, where, how often) instead of downloading every famous sound. It should feel like a real person edited it. Two failures started it, and both became rules (`sfx-selection.md`, `sfx-sources.md`, research in `research/free-sfx/`).

| What the user said | Cause in the skill or the kit | Fix |
|---|---|---|
| **The same slide sound every time** (the first Enogon film), and a bad one | One source reused for every slide. In v1 every slide was the kit's synthesized `swish` in the `paper` character; `vary.py`'s 4 takes of one recipe, with pitch and level jitter, still read as one sound. The skill's own fallback, `samples.py`, picks a family of only 2 or 3 files from one pack, so even with samples on a role had no real pool. "The same whoosh on every move" is the most cited amateur tell in the research | A per film pool for every repeated role: 5 to 8 different recordings from at least two sources, rotated in `cues.py` with no file twice in a row, each trimmed to its move, small pitch and level jitter, a new pool for every film recorded in the registry (`sfx-selection.md`, section 8) |
| **Enogon v2 clicks were too quiet**, although the clicks drive the story and must be heard | Story clicks were cues of weight `support` (gain 0.4 times the job's 0.5, so 0.2 of full scale on the effects bus, which enters the mix at half) or `ambient` (0.16, and about a third of ambient cues are randomly skipped by design, so some clicks played nothing); a support click on a `cut: true` frame was demoted to ambient; and the click file had 123 ms of silence before its transient, so at 60 fps it landed 7 frames after the press | A recorded mouse click (Freesound 678248, CC0) played with a cue's `"file"`, its lead silence trimmed to the transient on load (`recording()` in `score.py`); `"story": true`, which stops the demotion and the random skip; a per cue `"gain"` (3.6 in the rebuild). The rebuild measured the clicks at 6 to 20 dB over the bed. The click rule: about 6 to 9 dB over the bed, a 2 to 4 dB music dip of about 150 ms where needed, high passed at 150 to 200 Hz, on the press frame or one frame late (`sfx-selection.md`, section 10) |

**Say how a level was measured.** Rechecked on 31 October 2026 with the check in `sfx-selection.md`, section 11 (the effect's loudest 10 ms RMS against the median 50 ms level of the music in the 1.5 s before, which is how the research measured accents), the same Enogon v2 clicks measured -0.2 to -2.1 dB over the bed and the typed keys -3.4 to -7.7 dB, while their sample peaks sat +7.4 to +14.7 dB over it; and at frames 959, 964 and 1088 the music had its own accent in the same 60 ms, so in the click's band (above 1 kHz) the click was 1.9 to 8.1 dB under the music. A peak meter and an RMS window differ by a click's crest factor (about 14 to 17 dB here), so "over the bed" always names its method, and a story click also has to avoid the music's own hits. The clicks are louder than they were, and still short of the rule.

**The one mistake under both.** A click too quiet to hear and a whoosh that repeats on every slide both come from treating sound as a one to one map from picture events to one sample at one fixed gain. A human editor ranks the events first, makes the few story moments unmistakable, and lets the music and a quiet, varied texture carry the rest (`research/free-sfx/report.md`, Conclusion).
