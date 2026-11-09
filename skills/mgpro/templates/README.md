# Templates

## `kit/`: start every film here

A standalone Remotion 4 project: copy the folder to `~/dev/<product>-video`, `npm install`, make a `.venv` for the audio (`pip install numpy scipy soundfile pyloudnorm pedalboard librosa`), write `src/music.json` (the sonic brief, see `references/music.md`), then fill in the brand.

| File | What it is |
|---|---|
| `package.json`, `remotion.config.ts`, `tsconfig.json` | Remotion 4 with three.js, exact versions, swangle renderer |
| `src/music.json` | the sonic brief: genre, tempo, meter, key, mode, palette, hook, signature, form. Replace the example per film |
| `src/lib.ts` | the film's grid from `music.json` (`BPM`, `BEAT`, `BAR`, `at`, `SECTION`, `T`), cue helpers (`cuesOf`, `cueAt`), easing, springs, `prog`, `keys`, `enter`, `exit`, `inOut`, placeholder `COLOR` and `FONT` to replace with the product's tokens |
| `src/kit.tsx` | `Words` (kinetic type), `Glass`, `AiGlow` (only for products with AI), `Grain`, `Vignette` |
| `src/camera.ts` | orbit camera, `threeCamera`, `project`, `pxPerMetre`, `cornerPin` homography |
| `src/three.tsx` | `Rig` (camera from a pure function of the frame, with roll and a view offset shake) and `Studio` (reflection map for metal) |
| `src/Cursor.tsx` | desktop cursor from the user's theme (`MacCursor`) and collaborator cursors (`RemoteCursor`) |
| `src/Touch.tsx` | mobile taps: `pressScale` and `TapRipple` |
| `src/formats.ts` | frame sizes and safe boxes per destination (landscape, tv, vertical, feed45, square, App Store, Google Play); `Root.tsx` registers a `Film-<format>` composition for each |
| `src/SafeZones.tsx` | review guides: TikTok, Reels, Shorts and Snapchat overlays plus the safe box, shown only with `--props='{"guides":"tiktok"}'` |
| `src/Root.tsx`, `src/Film.tsx`, `src/index.ts`, `src/cues.json` | the composition, one global frame passed to every act |
| `audio/cues.py` | cue list on the film's own grid (`at`, `start(section)`) |
| `audio/score.py` | the score engine: plays the form from `music.json`, places effects from `cues.json`, mixes and masters to `public/film.wav` |
| `audio/dsp.py`, `instruments.py`, `grooves.py`, `theory.py`, `sfx.py` | the audio library: signal blocks, a large instrument set, 21 genres as data, keys, modes, chords and motifs, key aware effects |
| `audio/demo.py` | 8 bar sketch of any genre, to choose before committing |
| `audio/fingerprint.py` | checks the score against every earlier film in `music/registry.json` |
| `audio/sampler.py`, `audio/sampler_map.json` | sampled instruments: a numpy SFZ player and the map from the engine's kinds (`keys:piano`, `kick:punch`, `pad:strings` ...) to recorded CC0 instruments; the default when the library is installed (`"instruments": "synth"` turns it off), see below and `audio/SAMPLER.txt` |
| `audio/fetch_instruments.sh` | downloads the sample instruments (CC0, pinned commits) to `/games/mgpro/instruments` |
| `prep/xcursor.py` | extract a Linux Xcursor theme to PNGs and hotspots |

## Sampled instruments

Recorded instruments are the default when the library is installed (`"instruments": "samples"` in `src/music.json`; `"synth"` forces the synth): every part whose kind is in `audio/sampler_map.json` is performed by recorded instruments (Kawai grand, Osiris una corda piano as `felt`, VSCO 2 CE string sections in sustain, spiccato and pizzicato, a solo cello, VCSL marimba, vibraphone, glockenspiel and kalimba, an archtop guitar, upright and electric bass, the Virtuosity jazz kit with round robins, hand percussion), placed in a Voxengo room by convolution. Kinds without a recording (808, reese, supersaw, epiano, organ ...) stay synthesized, and without the library everything falls back to the synth with a message.

1. Fetch once: `audio/fetch_instruments.sh` (about 1.3 GB as FLAC in `/games/mgpro/instruments`, or pass another folder and set `MGPRO_INSTRUMENTS`). It stops if `/` has under 3 GB free or the target disk under 8 GB. Licences per source are in `SOURCES.txt` there: all CC0 1.0 except the Voxengo impulse responses (free for any use, not to be redistributed).
2. Try it: `audio/demo.py boom_bap --film` (add `--synth` to compare), `audio/sampler.py --list`, `audio/sampler.py --demo keys:felt`.
3. Change a kind per film with `"samples_map": {"keys:piano": "felt", "lead:cello": "cello"}`. New kinds that exist only as samples: `felt`, `grand`, `upright_piano` (keys), `cello`, `pizz` (lead), `pizz` (bass, contrabass pizzicato).

## `examples/`: three finished films

Read the one closest to the brief, copy the scenes that fit, rename the product specifics.

| Example | Product | What to take from it |
|---|---|---|
| `examples/bauwerk/` | desktop 3D building editor with AI, light brand (navy, IBM Plex Sans, Lucide) | floating search with typing, map dive, a real city rising (LoD2 plus OSM, `prep/lod2_osm_city.py`), corner pinned plan with AI tracing, facade scan and detection, live team chat, slider and toggle, energy class roll, report, end card with URL; synth in G major with 37 effects. Config shows how to alias the app's own code and three.js. |
| `examples/torq/` | Android workout tracker with a strength rank, dark brand (near black, lime, Space Grotesk, Tabler) | 3D barbell with slamming plates and a rush into a shape match cut (`BarAct`), set rows and a rest timer with taps (`LogAct`), a particle distribution from real quantiles on canvas (`EngineAct`), an extruded 3D medal forged through tier metals with bloom, gap and drop (`Medal`, `ForgeAct`), 3D to 2D handoff into a leaderboard with an overtake, a push notification, week dots (`FriendsAct`, `Badge`), a line chart with a riding head and a counter tied to it (`PayoffAct`), a logo built from its own paths (`EndAct`); synth in A minor. |
| `examples/enogon/` | web app that turns floor plans into 3D CAD models, light technical drawing brand (paper, ink, apricot, Türkis, Inter Tight, IBM Plex Mono, Tektur wordmark), German | upload by drag and drop into a drop zone, the scan growing out of the card (`PlanLayer.tsx`), an AI draftsman laying walls with a crosshair, doors swinging, rooms flooding, counters (`Overlay.tsx`), walls with real openings and analytic ink lines (`geo.ts`, `Scene3D.tsx`), storeys landing, a roof, dimension lines, a property card with a field edit, an Export button with a fill, a house folding into the isometric logo cube by a dolly zoom with an exact hand over to the flat SVG logo (`cubeRect.ts`), monotone camera keys (`timeline.ts`), picture frames exported for the cue list (`scripts/events.ts`); score in `cinematic_pulse` with cue weights. Its music is taken. |

Each example has its `SCRIPT.md` (the per second script, the format to follow), `audio/cues.py` and `audio/synth.py`. Their music is taken (see `music/registry.json`): read the synths for mixing ideas, never start a new score from them.
