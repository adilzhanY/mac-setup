# mgpro releases

The skill is versioned like software. The current version is in `VERSION`, every release is a git tag `vX.Y.Z` in this repo (private, `adilzhanY/mgpro`), and every release gets an entry here, newest first.

## How to version a change

- **Patch** (`1.2.3` to `1.2.4`): a fix or a clarification. A rule reworded, a wrong number corrected, a bug in the kit fixed. Films made before still match the skill.
- **Minor** (`1.2.3` to `1.3.0`): something new that does not break old habits. A new reference file, a new element recipe, a new lesson from a film, a new sound in the library, a new genre in the score engine.
- **Major** (`1.2.3` to `2.0.0`): the way films are made changes. A rule reversed, the workflow reordered, the kit's API changed so an earlier film's code no longer drops in.

Steps for every release:

1. Make the change. Check it: `grep -rnP "\x{2014}|\x{2013}" . --include=*.md` finds no em or en dash, and the kit still builds if you touched it.
2. Bump `VERSION` and the `metadata.version` line at the top of `SKILL.md`.
3. Add an entry at the top of this file: the version, the date, and a few lines on what changed and why (which film or which review taught it).
4. Commit with a one line message, tag and push: `git commit -am "mgpro X.Y.Z: <what>" && git tag -a vX.Y.Z -m "<what>" && git push --follow-tags`.
5. Mirror the desktop copy: `arch-config-push "mgpro X.Y.Z"`.

To see what changed between two versions: `git diff v1.0.0 v2.0.0 --stat`. To go back to an older version for a test: `git worktree add /tmp/mgpro-old v1.0.0`.

Every film records the skill version it was made with in its `SCRIPT.md` header and in `music/registry.json` (`"mgpro": "X.Y.Z"`), so a later review knows which rules the film followed.

## 3.1.0 (2026-10-31)

Sound effects are found, not made. From the user's request after Enogon v2 (search premade sounds the way human editors do, choose each one wisely, make the clicks audible) and a third deep research run (seven researchers: major free sites and licences, creator and niche packs, editors' workflow, UI and cursor sounds, motion sounds, levels and placement, measured case studies of human edited product films), in `research/free-sfx/`.

- New `references/sfx-sources.md`: every free source in three tables (safe for client ads without credit; credit, paid plan or one tool only; excluded), how to download each, the quoted licence clauses and the traps (no stock sound as a sonic logo, no raw files in templates, Pixabay forbids systematic copying, Fairlight only in Resolve, CapCut only in CapCut), named Freesound recordists and IDs per role.
- New `references/sfx-selection.md`: the editor's workflow as steps per film (roles, search words, audition at matched loudness, judge fit, pools of 5 to 8 takes from two or more sources, trim to the transient, licence lines), the table per sound type (source, IDs or search terms, licence, length, level, timing, budget, variation), the three level tiers, the story sound rule and a measurement script.
- Kit (`score.py`): `"file"` may be a pool of recordings rotated without repeats; `"story": true` cues are never skipped or ambient, are high passed at 170 Hz, and the music ducks under them (`story_duck_db`); found files are copied into `public/sfx/` with licence lines.
- Enogon: story clicks were too quiet (support or ambient weights, random skips, a 123 ms lead silence); now three CC0 mouse click recordings (Remotion 678248, Freesound 683099 and 213004) rotate, measured +3 to +8 dB over the bed and +5 to +17 dB over the music in their band. Lessons in `lessons.md`, self checks 9 to 11 in `review.md`.

## 3.0.1 (2026-10-29)

Enogon example: the lockup now waits for the cube to settle and the wordmark slides out from behind it (it had overlapped the moving cube for a few frames).

## 3.0.0 (2026-10-29)

A major release from the user's review of the Enogon film: films now sound and move differently by default.

- **Real instruments by default.** `sampler.py` plays the score on 1.3 GB of recorded CC0 instruments (VSCO 2 CE, VCSL, Virtuosity Drums, Karoryfer, Osiris Piano, FreePats) in a convolution room (`fetch_instruments.sh`, library in /games/mgpro/instruments); `"instruments": "samples"` is the default, the synth is the fallback. "notes" cues play real notes on a sampled instrument at a frame (sonic logos, musical accents).
- **No more gain holes.** Automatic dips are off by default; a dip section is an arranged breath within 3 dB. The user heard the -24 dB dips as the audio breaking.
- **Systematic feel.** A repeating per bar timing and accent template, velocity contours over phrases, pushes only on peaks and cadences, instead of random jitter.
- **Recordings first for effects,** few of them; no synth pops, dings or bells.
- **A second deep research run** (seven researchers: composition, AI tells and realism, transitions and feeling, sample libraries, logo reveals, pacing, cursor animation), in `research/ad-music-and-logo/`, taught into new `composition.md` and `logo-resolve.md` and into sound, music, craft (pacing), interaction (cursor), elements (fast trace, box fold), review (self checks) and lessons (Enogon review).
- **The kit cursor** (`Cursor.tsx`): a spring follower (Cap presets), tilt with speed, motion blur ghosts, a press squash, rings only where they mean something, entries and exits through the frame edges.
- **Enogon v2** replaces v1 in `templates/examples/enogon/` and in the registry.

## 2.0.0 (2026-10-27)

A major release: the way films are made changed in three places.

- **vizavi-motion merged** (its v1.6.1, translated from Russian, every item mapped in `references/vizavi-map.md`). Direction before code: one thread and 3 to 5 options for every scene (`storyboard.md`). The first build is a draft: a mandatory review that checks the decoded export (`review.md`). A camera that keeps moving through depth, motion blur, depth of field and weight (`craft.md`). New references for 3D models, generated images, reference videos and style registries.
- **Sound rebuilt from research.** A deep research run (five researchers, 129 professional films measured with their audio, a 1126 sound CC0 library analysed) showed the first three films were clones of each other. `sound.md` is now a manual with measured targets, a hierarchy of cue weights (hero, support, ambient) in place of "every visual event has a sound", dips in place of dead gaps, sync tolerances, loudness per destination, and the checks every film must pass. The evidence is in `research/` and `sound-research.md`.
- **The audio kit reworked.** One effect per job in seven characters, all measured inside the library's ranges; variation pools so no sound repeats; optional CC0 samples; automatic dips, a soft opening, a beatless option, humanised timing, a darker master; `fingerprint.py` checks every film against the professional range and against every earlier film (profile distance at least 2.67, shared transients at most 10 percent).
- **Versioning**: `VERSION`, this file, git tags, the version in `SKILL.md` and in every film's script and registry entry.
- **Enogon**, the first film made with this version, added as `templates/examples/enogon/` with its lessons (flat tone mapping for flat brands, analytic ink lines for walls with openings, an exact 3D to flat logo hand over, picture frames exported for the cue list, monotone camera keys).

## 1.0.0 (2026-10-27)

Baseline before versioning: the skill as it was after Bauwerk, torq and Sendoku. Remotion and three.js pipeline, the synthesized score engine with 21 genres, the music registry and fingerprint, the sound recipes, destinations, intake, lessons.
