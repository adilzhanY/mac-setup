# Craft: how motion should feel, with numbers

Everything here is in frames at 60 fps unless it says otherwise. The code lives in `templates/kit/src/lib.ts` and `templates/kit/src/kit.tsx`.

## The grid

- The grid is the film's own: tempo, meter and form come from `src/music.json` (see `music.md`), and `lib.ts` turns them into `BEAT`, `BAR`, `at(bar, beat)` and `SECTION`. At 60 fps a beat is 3600 / BPM frames: 75 BPM is 48, 100 is 36, 112.5 is 32, 128.57 is 28, 144 is 25, 171.43 is 21.
- Never assume 30 frames a beat. A 30 s film is 1800 frames, which is 9.4 bars at 75 BPM and 21 bars at 171.
- Structural changes (a new act, the reveal, the end card) start on bar lines or the form's section starts. Ordinary cuts and scene changes fall with the action, not on the downbeat: a bar downbeat already measures 3 to 9x louder from the music alone, so cutting on every one makes every cut a slam (`sound.md`, Sync). Hits that are results (a pin landing, a badge popping, the drop) on beats. Fast repeated events (typing, traced walls, found windows, slider detents) on the genre's subdivision (16ths, 8th note triplets in trap rolls, 8ths in 12/8), or at a steady 2.5 to 5 frame spacing that reads as a run.
- Choose the tempo for the film, not for easy maths: `grooves.FRAME_TEMPOS` lists tempos whose beat is a whole number of frames in every range from 72 to 171 BPM.

## Easing

Linear motion looks cheap. Use these (cubic-bezier control points):

| Name | Curve | Use |
|---|---|---|
| standard | (0.4, 0, 0.2, 1) | general moves, Apple's own UI curve; velocity peaks about 60 percent through |
| out (expo out) | (0.16, 1, 0.3, 1) | entrances: fast start, long soft landing |
| in | (0.7, 0, 0.84, 0) | exits: start slow, leave fast |
| inOut | (0.83, 0, 0.17, 1) | camera moves and morphs between two rests |
| minimum jerk | t^3 (10 - 15t + 6t^2) | a hand moving from rest to rest; a cursor's path uses power3 out under a spring instead, because one symmetric ease on every move reads as robotic (`interaction.md`) |
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
- A press: a cursor squeezes to about 0.84 in 0.1 s (6 frames) and recovers in 0.22 s (13 frames); the button it presses scales to about 0.94 on the same frames (`interaction.md`). A tap on mobile: 0.95 to 0.985 for the control.
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
- Type takes part in the action: the typeface's character and the plasticity of letters, words and the space between them, not just a caption appearing. Design the readable final layout first, then what the letters and words do to get there: assemble, change width, reveal through masks, relate in space, react to an object. Every effect has a job in the meaning.
- The font is the product's own (`brief.md`). When a film needs another face or a pairing, pick an expressive one that is available and allowed, and check the actual glyphs (Cyrillic and other scripts the copy uses), the weights, the line breaks and the licence of the file (`rights.md`). If external fonts are not allowed, use allowed system fonts or draw the letters as geometry.

## Camera

- Always moving: a slow orbit (20 to 30 degrees over several seconds), a slow push in, or a drift. A static frame looks like a screenshot.
- Orbit parameters: target, distance, azimuth, elevation, fov 28 to 32 (long lens looks like product photography). Interpolate parameters, not positions.
- Continuity: at each segment join the camera must have the same parameters on both sides. Write each segment's start values from the previous segment's end values. Never interpolate angles across a 360 wrap by accident.
- Dives use exponential distance plus a rotation (a swirl zoom): the map turns upright on the way down.
- Tilting from top down to oblique while things rise sells 3D. Start the tilt before the rise so the rise is seen in perspective.
- Shift the target sideways (along the camera's right vector) to make room for panels instead of moving the 3D object.
- Depth of field for focus changes: blur the 3D layer 14 to 16 px, scale it 1.04 to 1.06 and dim it while the payoff sits sharp in front.

### The camera keeps moving, through depth (from vizavi-motion)

- While the story is active the camera moves continuously: smooth acceleration and braking, one coherent path, motivated tilts, diagonals, slight rolls and fly arounds. A single linear zoom into a flat composition does not count.
- Keep path, speed, orientation, target, field of view and focus as separate controls (mgpro's orbit parameters already split target, distance, azimuth, elevation and fov; give speed and focus their own curves too).
- Design one long coherent path with waves of speed. Do not chain identical ease in outs that come to a dead stop on every accent.
- At every join check position, direction, speed on screen and acceleration, not position alone.
- In the reading phase of an active scene, a big travel settles into a calm arc or drift. A technical pause or the final readable frame needs no motion for its own sake: the end card's slow scale drift is enough, and a TV spot ends still (`destinations.md`).
- Following the hero goes well with clear parallax in its surroundings.
- A deliberate hard cut between different places does not need one continuous world coordinate across it.
- The camera helps the action: it can follow a caret, close in on a click, pull back for the result, or move around layers spread in depth. Pick the one gesture that means something; do not do all of them in every scene.

## Depth and layers

- Foreground, middle ground and background differ in scale, in relative motion, in overlaps and in perspective. Show perspective depth and their motion against each other.
- Protect silhouettes and text from accidental overlaps.
- A label next to a moving 3D object is tied to the projection of its anchor (`three.md`), keeps its margin from the frame edge, and never jitters or lags behind.

## Optics: motion blur, depth of field, radial blur (from vizavi-motion)

Use motion blur for relative motion and controlled depth of field in spatial and close shots by default, always keeping the hero and the copy readable and recognisable. Apply them where the storyboard calls for them; the goal is quality, not showing every tool at once.

- **Motion blur** shows how far something moved on screen during the exposure. A sharp, tracked hero can have a smeared background. Sub frame sampling or a renderer feature is a means, not proof that the effect shows: check the frames. The smear weakens as the motion brakes. In Remotion: smear copies for a fast object (`three.md`, Speed without motion blur), the cursor's directional smear (`interaction.md`), `@remotion/motion-blur` only where its render cost is worth it.
- **Depth of field** isolates the chosen depth. When the camera closes in, focus follows the meaningful detail without accidental defocus. Near and far layers may go soft; the text and the hero stay recognisable. In a flat UI shot, do not make things unreadable just to tick a box.
- **Radial or zoom blur** is a separate stylised accent for depth or fast flying cards (a radial blur on the outgoing frame of a dive, for example). It is neither depth of field nor motion blur, and never the maximum blur on the whole film.

## Weight, form and secondary action (from vizavi-motion)

- Objects have weight, inertia, material, light, contact and secondary reactions.
- Combine anticipation, action, contact, reaction and settle, with different masses and curves per object. Never the same spring on every layer.
- Form reads through geometry, light, normals, thickness, contact shadows and overlaps. A highlight, grain or particles do not fix a wrong construction. Texture and shadow follow the object and the light.
- One main accent may carry coordinated secondary layers. When everything fights for attention, change the phase, scale, depth or contrast. Keep richness through hierarchy, not by removing the whole environment.
- Change the accents and the shot sizes without long holds and without chaotic flicker.
- Do not save the pace by removing required elements or by speeding up until text cannot be read.
- Repeated flashes are not a substitute for energy (`review.md`, Flashes and strobing).

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

The Enogon review (Oct 2026): "the animation took too much time and was boring", "the building was shown too long", the roof "hovered paused for about a second", and the length should "come from content, not seconds". The film was 40.8 s because the user chose no length and the agent picked the middle of "30 is too fast, 60 too slow". The rebuild tells the same story in 26.7 s. The numbers below are from the research in `research/ad-music-and-logo/` (`notes/pacing_and_attention.md`, including 17 launch films measured with ffmpeg scene detection).

### The rules

- **A visible change every 1 to 3 s**, even inside a long take: a cut, a new element, a change of camera direction, a UI state change. Pace comes from change, not from cuts. **(heuristic, derived from the measured films below)**
- **The product, or its effect, in the first 2 s**, with a few words, never a logo intro. Viewers make a go or no go decision within 2 to 3 s ([RBR](https://rbr.com/is-the-power-of-06-ads-a-concern-for-broadcast-tv/)); people who watched under 3 s produced up to 47 percent of campaign value in Facebook and Nielsen's study ([MarTech](https://martech.org/even-brief-video-views-drive-brand-lift-facebook-nielsen-study-finds/)); recognisable brand assets in the first 2 s lifted recall in System1's 887 ad TikTok study, while plain logo overlays reduced it ("They recognize the brand but scroll along", [Chief Marketer](https://chiefmarketer.com/system1-tiktok-study-branding-elements-and-creator-led-content-improve-short-form-video-ads/)).
- **Never hold a static hero for more than about 2 s.** Brand memory builds at roughly 1.5 to 2.5 s of active attention ([Advertising Week](https://advertisingweek.com/the-second-second-is-the-moment-that-matters-most-for-brands-right-now/); [Creative Salon](https://creative.salon/articles/features/vccp-media-dr-karen-nelson-field-hacking-the-attention-economy)), so a hero needs about that and no more. Long holds survive only while something keeps changing: the 9 to 19 s holds in Apple and Samsung films are continuous camera moves, and the Pixel 9 Pro intro holds one shot for 20 s because the typed prompt keeps growing ([YouTube](https://www.youtube.com/watch?v=OMVpP-Zam1A)). A static hold is a risk past about 3 s with nothing changing **(heuristic)**; a camera drift alone does not reset the clock if nothing new happens to the hero.
- **No pauses inside a fall or a landing.** An object in flight never stops in mid air to wait for a hit point or a breath; the Enogon roof hung over the walls for about 1.1 s to sit under the music's dip, and the user saw it as a pause. Anticipation happens before a move starts, never during it; if the move and the music disagree, move the music (`composition.md`, section 1).
- **Compress processes, never wait on them.** "Slow" usually means waiting on a process. Show the trigger in full (about 1 s), compress the middle into two to four jumps of 0.4 to 0.8 s or one shot ramped at 3 to 8x, then hold the result 1.5 to 2.5 s **(heuristic, from elliptical editing, [Filmdaft](https://filmdaft.com/elliptical-editing-how-films-compress-time-into-seconds/))**. Overlap each action's start with the previous one's end by 0.1 to 0.3 s, so there is never a frame of dead waiting; stagger many entrances 0.1 to 0.2 s apart ([Webflow](https://university.webflow.com/course-lesson/interactions-animations-sequencing-timing)); cut on action, not after the motion settles. Avoid near identical consecutive framings: editors reviewing AI ads called that stutter "uncomfortable" ([arXiv 2608.24329](https://arxiv.org/html/2608.24329)).
- **Length comes from the content.** Add up what the story needs: a 2 s hook, three to five beats of 4 to 6 s (each two to four shots or UI changes), the payoff, the logo resolve and its 1.5 to 3 s hold. That sum, inside the destination's limits (`destinations.md`), is the length. Never pick a round number first and fill it. Launch films people chose to watch run 30 to 60 s at Apple, Linear and Notion; 15 s spots "can hit just as hard as 30s" in feeds ([Kantar](https://www.kantar.com/north-america/company-news/kantar-super-bowl-ad-study-15-second-ads-match-30-second-spots)).
- **End short.** Viewers leave once they sense the value is over, so no recap and a short end ([Wistia](https://wistia.com/learn/marketing/understanding-audience-retention)). Apple films hold the product name about 1 to 2 s, then the logo about 2 s. The resolve itself is in `logo-resolve.md`.

### Reading time

Netflix caps adult reading at 20 characters per second with a 0.83 s minimum event ([Netflix](https://partnerhelp.netflixstudios.com/hc/en-us/articles/217350977-English-USA-Timed-Text-Style-Guide)). Viewers grasp a picture's gist in 13 ms but need about 500 ms of processing to remember it ([Potter 2012](https://www.frontiersin.org/articles/10.3389/fpsyg.2012.00032/text)). Fast cutting raises arousal, attention and memory ([Lang 2000](https://scholars.cityu.edu.hk/en/publications/the-effects-of-edits-on-arousal-attention-and-memory-for-televisi/)), but verbal recognition suffers first when pace and arousing content combine, so a 1 s cut is fine for pure picture and too fast for a shot that also carries words. Working holds **(derived, not measured)**:

- **Text**: hold = max(0.9 s, characters / 15) + 0.5 s to settle. A three word headline (about 18 characters) needs about 1.7 s, a seven word line (about 40 characters) about 3 s. 15 characters per second rather than 20 leaves room for viewers who did not expect the text and for animated text that is unreadable until it settles.
- **A UI change**: 1.5 to 2.5 s (about 0.5 s for the eye to land, the change, 0.5 to 1 s of settled result). Lead the eye with the cursor or a highlight, or put the change near the centre (cuts pull the eye to the centre, [Cutting et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC3485803/)).
- **The logo**: 1.5 to 2.5 s or more of clean screen time.

### What launch films measure (own measurement in the research, ffmpeg scene detection)

| Family | Films | Average shot |
|---|---|---|
| Hardware hero films, one product beat per cut | Apple iPhone 17 Pro ([YouTube](https://www.youtube.com/watch?v=TNhX1uR2vO8)) 2.3 s (median 1.6 s); MacBook Pro 3.7 s; Samsung S24 design film 3.5 s | 2 to 4 s |
| Feature parades, social cut downs | Figma Config 2024 ([YouTube](https://www.youtube.com/watch?v=0wCIP2Ox-EQ)) 1.4 s, 58 cuts in 80 s, 8 in its first 5 s; Arc Max 1.2 s | 1.2 to 1.6 s |
| SaaS UI films, change inside the shot | Linear Releases ([YouTube](https://www.youtube.com/watch?v=6dIwFoQ0eVg)) one continuous camera drift; Framer one 21 s shot; Raycast 4.8 s; Notion new AI 4.7 s | 5 to 20 s, with the picture changing all the time |

Hollywood fell below 4 s per shot after 2000, with shorter shots carrying more motion ([Cutting et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC3485803/)); social "cinematic ads" average about 1.2 s ([arXiv 2608.24329](https://arxiv.org/html/2608.24329)). Pick one family per film. mgpro's one continuous camera films (Enogon) are in the SaaS family, so their rhythm must come from change inside the shot, every 1 to 3 s.

### A 30 s structure consistent with all of this

| Time | Job | Picture | Music |
|---|---|---|---|
| 0 to 2 s | Hook | the product or its effect, with a few words, not a logo intro | one texture, the motif fragment, below full level |
| 2 to 22 s | three to five beats of 4 to 6 s | each beat two to four shots or UI changes, a visible change every 1 to 3 s | layers and register added at the turns, one breath at most |
| 22 to 27 s | Payoff | the single most impressive moment | the peak, on the payoff |
| 27 to 30 s | Name and logo | one clean frame, one move, a 1.5 to 3 s hold | the button on the landing frame, the tail rings out |

The music's form (`music.md`: spine, cold open, slow burn, two drops, beat switch, stop start, minimal pulse, call and response) sets the order of energy, and the story follows it. The spine of Bauwerk and torq (hook, magic moment, build, breath, drop, people or proof, stop, payoff, end card) is one choice among eight, not the default. Hold the end card still enough to read the URL; let the music ring out; silence by the last 0.2 s.

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
