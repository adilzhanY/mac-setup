# Review: the mandatory pass after the first build, and the check of the decoded export

The first full build is never the film. This file is the working check that turns it into one (merged from vizavi-motion, its third core mechanic, on top of mgpro's review loop in `pipeline.md`). It is a way of working, not a certificate: code that exists, a contact sheet or a frame count do not prove that the film works.

## The first build is a draft

Treat the first full render as an internal, unfinished draft. Never hand it over as the final film.

1. Go through the whole film once in order, then scene by scene and join by join. An agent cannot watch at real speed; the closest it gets is a dense run of frames across each join and each fast phase (every frame or every second frame, `pipeline.md`, Review loop), and that is what it must look at. The audio side of the review (music, effects, the full mix) is in `music.md` and `sound.md`.
2. Write each real problem as one line in `REVIEW.md` next to `SCRIPT.md`: **interval → what is seen → cause → the concrete fix → how it was rechecked**. For example: `14.0 to 14.3 s → the drop lands on an almost empty frame → content starts 6 frames after the cut → the number arrives on the hit frame with a pop from 1.25x → frames 838 to 846 rechecked in the final render`.
3. Do not fake iterations to show effort. If a pass finds no defects, write down what exactly was checked.

## What to check

- The idea and the causal thread read; the hero is recognisable; the story develops instead of stalling in boring holds.
- Camera, shot size, perspective and layers lead the eye; speeds and joins are smooth (no jump in position, direction or screen speed at a join, `craft.md`, Camera).
- Type performs an action, and every required word is readable without pausing the video.
- Form, light, shadows, material, identity and contact hold; no artefacts, accidental crops or layers fighting each other.
- Blur and focus follow the motion and the depth without hiding what must be seen (`craft.md`, Optics).
- Music and effects support the style, the rhythm and the events; no drift out of sync, no clicks, no cut off tail (details in `music.md` and `sound.md`).
- The format, length, frame rate, silence or offline rules and every other explicit requirement of the brief and the destination are met.
- Everything in the quality checklist in `SKILL.md`.

## Self check: the failures the user has named

Every review the user gives adds lines here (`lessons.md`). Run the whole list on every film, on the draft and again on the decoded final file, and write each result in `REVIEW.md`. A line passes only with the measurement or the frames named; "looks fine" is not a result. Calibrated on the first Enogon film, which failed most of them.

**1. Audio holes.** No window where the sound drops more than about 6 dB under its own surroundings for 100 ms or more, unless it is a listed, arranged breath (on the grid after a cadence or a hit, a bed or a tail under it, resolving within one beat to one bar), and true silence only 100 to 300 ms right before a hit (`sound.md`, section 9). `music.json` has `"dips": 0` unless `score.py` already makes arranged breaths. Measure the rendered mix (or the audio of the final MP4):

```python
# python holes.py public/film.wav : every window 6 dB or more under its surroundings for 100 ms or longer
import sys, numpy as np, soundfile as sf
x, sr = sf.read(sys.argv[1], always_2d=True); x = x.mean(1)
w = int(0.05 * sr)                                    # 50 ms windows
db = 10 * np.log10(np.array([np.mean(x[i:i + w] ** 2) for i in range(0, len(x) - w, w)]) + 1e-12)
ctx = np.array([np.median(db[max(0, i - 60):i + 60]) for i in range(len(db))])   # the 3 s around it
low = db < ctx - 6
i = 0
while i < len(low):
    j = i
    while j < len(low) and low[j]: j += 1
    if j - i >= 2 and i * 0.05 > 0.5 and j * 0.05 < len(x) / sr - 1.0:   # skip the head and the tail
        print(f"{i * 0.05:6.2f} to {j * 0.05:6.2f} s  {db[i:j].min() - ctx[i]:+.0f} dB")
    i = max(j, i + 1)
```

On the first Enogon film it prints seven windows, five of them 20 to 29 dB deep (3.15, 6.65, 13.7, 18.85 to 19.8 and 35.7 s): the automatic dips the user heard as the sound dropping out. Every line it prints must match a listed breath in the sound plan, or be fixed.

**2. Holds over 2 s.** No static hero for more than about 2 s, a visible change every 1 to 3 s, the product or its effect in the first 2 s (`craft.md`, Pacing). Find candidates with ffmpeg's freeze detector at a tolerant threshold:

```bash
ffmpeg -hide_banner -i out/film.mp4 -vf "scale=480:-1,freezedetect=n=-30dB:d=2" -map 0:v:0 -f null - 2>&1 | grep -o "freeze_[a-z]*: [0-9.]*" | paste - - -
```

Each interval it prints is a candidate, not a verdict: look at a dense run of frames across it and pass it only if something new keeps happening (a line drawing on, a new element, a change of state). A camera drift over an unchanged hero does not count. On the first Enogon film it flags 18.7 to 23.8 s, the roof and the building the user found shown too long, and the opening 8.5 s. The end card hold of 1.5 to 3 s is the one allowed hold. Scene detection (`select='gt(scene,0.12)'`) misses changes inside a continuous camera move, so it cannot replace this for one shot films.

**3. Pauses in motion.** Nothing in flight stops before it lands: no flat run in a falling or travelling object's position between the start of its move and its contact frame. Check in the code (no stop with a `leave` inside a fall, no keyframe hold between the lift and the landing, no picture waiting for a music cue) and in frames (sample the object's projected position every frame across the move; 6 or more frames with no movement before contact fail). The Enogon roof hung for about 1.1 s before landing.

**4. Cursor fades.** The cursor never fades in or out in place: `grep -n "visible\|opacity" src/Cursor.tsx src/cursorTrack.ts` finds no visibility fade on the main cursor; its first and last stops lie outside the frame; every entry and exit crosses a frame edge. Moves vary (at least three tempos, arcs changing side and amount, durations following distance), every click has a target that answers on the same frame, and the visible arrow is about 7 percent of the frame width (`interaction.md`, How it moves).

**5. Crossfade transitions.** No frame shows two scenes or two objects at partial opacity at the same time: no crossfade between scenes, no see-through morph, no 3D material made transparent for a hand over. Grep each transition's code for `opacity`, `transparent: true` and `mix(` on materials or layers that overlap in time; then step through every frame of each transition and of the logo resolve. The logo resolve follows `logo-resolve.md` (a clean frame before it, one opaque decelerating move, the sonic accent on the landing, a 1.5 to 3 s hold). The first Enogon film's house to cube x-ray failed this.

**6. Identical sounds across films.** For every cue job, write its source (a sample file and pack, or a synth recipe and character) in the sound plan and compare it with the last film's registry entry: no hero or support job from the same source as the last film. `fingerprint.py --against` the registry passes (shared transients at most 10 percent), and the instruments come from the sampler (`"instruments": "samples"`) with recorded effects first (`sound.md`, section 4b). The first Enogon film's synthesized whoosh and reverse swell at 12 to 13 s sounded like the earlier films, though they passed the transient check.

**7. Composed to the picture.** The hit points sit on downbeats (or a meter change catches them), the motif is restated at the logo with its last note on the landing frame, at most one lift or one drop per 30 s, energy built by texture, not level (`composition.md`, section 10).

**8. Length from content.** The length is the sum of what the story needs, not a round number filled; no scene is stretched to reach a planned length (`craft.md`, Pacing).

**9. Every story sound audible, measured.** Every action the story turns on (the click that opens the next scene, the press that exports) is a cue with `"story": true`, and the check in `sfx-selection.md`, section 11, prints for each one at least 6 dB over the bed (its loudest 10 ms against the median 50 ms level of the music in the 1.5 s before) and at least about 3 dB over the music at that moment above 1 kHz. Write both numbers per cue in `REVIEW.md`, and the method; a peak meter figure is not this number. No story cue is `ambient` and none lands on the music's own accent. Enogon v2's clicks, which the user heard as too quiet, measured -0.2 to -7.7 dB by this check (`lessons.md`, Sound effects review).

**10. No identical repeats of a role.** For every role that sounds more than once (slides, swishes, pops, landings, clicks, keystrokes), list the files its cues play in order: no file twice in a row, a pool of 5 to 8 recordings from at least two sources for slides and swishes, 3 to 5 for story clicks, 6 to 10 keystrokes for typing (`sfx-selection.md`, section 8). This prints every repeat and must print nothing; also check that no repeated role relies only on one synth recipe or one `samples.py` family. The first Enogon film played the same slide sound on every slide.

```python
# python repeats.py : every role whose cues play the same file twice in a row
import json
last = {}
for c in sorted((c for c in json.load(open("src/cues.json")) if c.get("file")), key=lambda c: c["frame"]):
    if last.get(c["sound"]) == c["file"]:
        print(f"frame {c['frame']}: {c['sound']} plays {c['file']} again")
    last[c["sound"]] = c["file"]
```

**11. Every downloaded file has a licence line.** Every file under `public/sfx/` and every `"file"` in `src/cues.json` has a line in `public/sfx/ASSETS.txt`: source and author, source page, licence and version, download date, what was done to it. Every source is in table 1 of `sfx-sources.md`, or the user confirmed its condition (a paid plan, a credit place); no file was scraped from Pixabay or another browser only site; no stock sound is the sonic logo; no non CC0 file is tracked in git (`git ls-files public/sfx` shows only CC0 files and `ASSETS.txt`). Check:

```bash
for f in public/sfx/*; do [ "$(basename "$f")" = ASSETS.txt ] || grep -qF "$(basename "$f")" public/sfx/ASSETS.txt || echo "no licence line: $f"; done
python3 -c 'import json; [print(c["file"]) for c in json.load(open("src/cues.json")) if c.get("file")]' | sort -u |
  while read -r f; do grep -qF "$(basename "$f")" public/sfx/ASSETS.txt || echo "no licence line: $f (cue file)"; done
```

On Enogon v2 both checks print lines: its four story clicks all play one file (`remotion-cc0/mouse-click.wav`), and four Kenney clicks in `public/sfx/` plus the three cue files read from the library have no licence line.

## Fix, recheck, finish

- Fix the cause, not the symptom. Re-view each changed range together with its neighbouring phases, then the whole film again.
- After any simplification, compare with the brief: "cleaner" is not acceptable if required characters, copy, environment or actions disappeared. Do not save the pace by cutting required elements or speeding up until text cannot be read.
- Finish when everything required is done and checked, the significant defects are fixed, and what is left is optional taste. Optional alternatives do not call for endless reworking.

## Check the decoded export, not the preview

After the final encode, open and decode the delivered file itself and check its picture and sound. The Remotion studio, the source PNGs or the WAV prove nothing about the MP4.

- **Technical**: the real codec and pixel format, size, an even frame rate and timestamps, the frame count and the exact length, the audio stream and its codec.

```
ffprobe -v error -count_frames -show_entries stream=codec_type,codec_name,pix_fmt,width,height,r_frame_rate,avg_frame_rate,nb_read_frames,sample_rate,channels -show_entries format=duration -of compact out/film.mp4
```

- **Frame count**: at an even 20 s and 60 fps expect 1200 frames, on the grid 0 to 1199 over 60; the end point at exactly 20 s is not an extra frame. (20 s is only an example of the count; length and frame rate come from the destination.) Never call a file 4K, 60 fps or a finished MP4 when the real file is something else.
- **Picture**: the first and the last frames, the frames just before and just after every scene boundary, the readable holds and the fastest phases, all extracted from the final file.
- **Kinds of evidence do not replace each other**: a contact sheet judges compositions, a dense sequence judges one join, a full playback judges rhythm and smoothness, listening judges sound.
- **Audio**: an audio stream being present is not the same as good sound. A silent stream never passes as a scored film, and an AAC stream alone does not prove that the music or the voice is audible and balanced.

## A timeline that gives the same frame every time

Remotion renders each frame from the frame number, which is what makes this reliable; keep it that way.

- Check a few frames after a cold seek, after seeking backwards and after jumping from elsewhere: a `remotion still --frame=N` is a cold seek, so compare it with frame N taken from the full render.
- Anything that accumulates (particles, simulations, trails, a cursor's state) is computed analytically from the frame, or baked and replayed. Never depend on the previous render call, on a mouse event or on how many frames were already played. A single random seed is not enough; use a deterministic hash per element (as the particle field in `elements.md` does).
- When a version must be kept, compare source and output by hash (`sha256sum`).

## Honest statuses

Use these words, and only for what was done:

| Status | Means |
|---|---|
| implemented | the code exists |
| checked by running | it renders or runs without errors |
| seen in frames | stills or frame sheets were looked at |
| checked in motion | it was watched at speed (usually only the user can do this) |
| listened to | someone heard it (never the agent: say "measured, not heard") |

- Nothing gets a pass from its parameters or a general impression. If a tool is missing, name the exact check that was not done and why, and deliver the available file with that status.
- Do not claim the skill or a technique is proven by the instructions existing or by one good frame. Do not label an earlier weak result "made without the skill" when the skill was used.
- If the required quality is really impossible in this environment, give the exact blocker and the parts that are finished. Never hide it after having said the film is ready.
- If the outcome of an external action is unclear (an upload, a write), find out what happened before repeating it. Do not ask for permission again for ordinary reversible work that is already allowed.

## Flashes and strobing

Do not use a repeating strobe as a substitute for energy (mgpro's single flash into the drop is one event, not a strobe). Check risky luminance changes in the output. Reduced motion settings or the absence of errors do not prove flash safety, and the film must not claim to meet a flash standard without an actual analysis.

## When the environment cannot export

If rendering, encoding (FFmpeg or an equivalent) or handing over the file is really impossible, report the concrete blocker, the parts that were done and the actual format you have. Deliver the sources with instructions to render and export them. Never present an HTML page or the Remotion studio as the finished video. This is an exception for a confirmed blocker, not a shortcut instead of the required file, and it is no reason to install a framework that is not available.
