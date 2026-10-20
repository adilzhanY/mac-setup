# Pipeline: from brief to final file

## Project

- A separate Remotion project next to the product, e.g. `~/dev/<product>-video`, never inside the product's repo. Start from `templates/kit/` (package.json, remotion.config.ts with swangle, tsconfig, src with lib, kit, camera, three, Cursor, Touch, Root, Film, cues.json).
- **Pin exact versions** in package.json (no `^`), and check package.json still lists every dependency after any npm subcommand. In the torq project something rewrote package.json and pruned node_modules after the final render, and a fresh install would have lost three.js, the fonts and the icons. Put the video project under git so a change like that shows in `git diff`.
- Fonts: the product's own font as a fontsource variable package (`@fontsource-variable/space-grotesk`), plus Geist Mono for numbers if the brand has no mono. Icons: the product's own set as its React package (`lucide-react`, `@tabler/icons-react`).
- Reusing the product's code (tokens, small components, 3D models): an `@` alias to its `src` and shared copies of react and three (see `templates/examples/bauwerk/remotion.config.ts`). Copying the few tokens you need into `lib.ts` is usually simpler. Watch Tailwind preflight (`img { max-width: 100% }` shrinks large images; set `maxWidth: "none"`).
- Python venv in the project (`.venv`) with numpy, scipy, soundfile, pyloudnorm, pedalboard, librosa (for the fingerprint) (plus pyproj and mapbox-earcut for map data).
- `.gitignore`: node_modules, out, .venv.

## Files

- `SCRIPT.md`: the per-second script (tables per act: time, picture, sound) and the copy list.
- `audio/cues.py` writes `src/cues.json`: `{frame, sound, ...params}` sorted. Typing rhythms, trace orders, detection grids, slider detents (computed from the same easing the picture uses) are generated here.
- `src/lib.ts`: scene start frames `T`, cue helpers (`cuesOf`, `cueAt`), easing, springs, enter and exit, colours, fonts.
- One component per act, all reading the global frame (pass the absolute frame into `<Sequence>` children so timings stay in film frames).
- `src/music.json`: the sonic brief (genre, tempo, meter, key, mode, palette, hook, signature, form). `lib.ts`, `cues.py` and `score.py` all read it, so a tempo or form change is one edit.
- `audio/score.py` (with the kit's `dsp.py`, `instruments.py`, `grooves.py`, `theory.py`, `sfx.py`) writes `public/film.wav`; the composition plays it with `<Audio src={staticFile(...)} />`. `audio/fingerprint.py` checks it against `~/.claude/skills/mgpro/music/registry.json`.

## Review loop

- Stills: `npx remotion still src/index.ts <Comp> out/s/f<N>.png --frame=<N> --gl=swangle --log=error`, 4 to 6 s each (3D included). Render 4 to 9 per act in a loop, then a contact sheet: `magick a.png b.png c.png -resize 33% +append r1.png`, rows joined with `-append`. Look at it; fix; repeat. A still at a transition frame shows composition; it cannot show motion.
- Full draft: `npx remotion render src/index.ts <Comp> out/draft.mp4 --gl=swangle --codec=h264 --crf=18 --audio-bitrate=320k --concurrency=8` with `run_in_background`, then wait with a background `until [ -s <output> ]; do sleep 5; done` loop (a foreground wait times out at 10 minutes; re-arm it). About 20 to 25 minutes for 30 s with 3D on this machine.
- Review the draft from frames, not stills: extract frames with `ffmpeg -ss <t> -i draft.mp4 -frames:v 1 -vf scale=384:-1` in segments around every transition (3 to 8 frames apart), `magick montage *.png -tile 6x -geometry +2+2 -background black sheet.png`, one sheet per transition. Read each sheet asking: does anything pop, overlap, stall, lag behind its sound, or land on an empty frame?
- What the torq draft review caught that stills had missed: a bloom too weak to read, a "GO" visible for two frames, a leaderboard still leaving while the next title entered, a counter that reached its final value while the line had barely started, a hit landing on an empty frame. All five took one edit each.
- Debug a blank 3D layer with `--log=verbose` and grep for errors; no error usually means a data or timing problem, not a shader problem.

## Parallel work

- Hand the soundtrack to a background agent with: `src/music.json`, `references/music.md`, the registry, every cue name with what it should sound like, which cues end on their frame (risers, reverse cymbals), the signature sound to design, and the files it may touch (only `audio/score.py`, `src/music.json` if it must change a part, and `public/film.wav`). Forbid starting from an earlier film's synth. Ask it to report LUFS, true peak, the balance line, RMS per section and the fingerprint table. Rerun the score yourself whenever the cue list changes (seconds).
- Keep picture work in your own hands; it needs constant visual checking.

## Finishing

- Final render CRF 16, 320k audio, one render per format the destinations need (`Film-<format>` compositions).
- Export per destination (`destinations.md`):
  - App Store: 30 fps, 886x1920 or 1920x886, H.264 about 11 Mbps, AAC 256k: `ffmpeg -i film.mp4 -vf fps=30 -c:v libx264 -b:v 11M -maxrate 12M -bufsize 24M -profile:v high -level 4.0 -pix_fmt yuv420p -c:a aac -b:a 256k app-preview.mp4`. 15 to 30 s exactly.
  - Google Play: upload to YouTube as public or unlisted, monetisation off, not age restricted, embeddable; paste the single video URL.
  - TV: master the score to the broadcaster's loudness (`"loudness": {"lufs": -23, "tp": -2}` in `music.json` for EBU, -24 for the US), convert the frame rate (`-vf fps=25` or `fps=30000/1001`), and hand the file and the spec to whoever delivers it.
  - Website loop: no audio track (`-an`), seamless loop, 1080p or less, under about 5 MB (`-crf 28 -preset slow`, WebM as well if the site serves it), plus a poster PNG of the best frame.
  - Social feeds: H.264 MP4 at 30 or 60 fps, -14 LUFS, the vertical render; check one still per act with `--props='{"guides":"tiktok"}'` (also `reels`, `shorts`, `snapchat`) before the final render.
- Strip metadata without re-encoding: `ffmpeg -i in.mp4 -map_metadata -1 -map_chapters -1 -fflags +bitexact -flags:v +bitexact -flags:a +bitexact -c copy -movflags +faststart out.mp4`.
- Register the music: append the film to `~/.claude/skills/mgpro/music/registry.json` with its choices (genre, bpm, meter, key, mode, palette, form, signature) and the measured part from `audio/fingerprint.py public/film.wav --bpm <bpm> --name <film>`. Without this the next film cannot avoid repeating it.
- Check: `ffprobe -show_entries format_tags:stream_tags` (only handler names and language should remain) and `strings out.mp4 | grep -iE "lavf|remotion|claude|anthropic"` (nothing).
- `grep -rnP "\x{2014}|\x{2013}"` over every file you wrote (em and en dashes).
- Reply with the path, length, size, a shot list by seconds, what was fixed during review, what could not be verified (audio by ear), and leftovers (test accounts, running servers) with a question before deleting anything.

## Keeping the user posted

A film takes an hour or more of tool calls and renders. Say one short line at each stage: project set up, script written, act N built and checked, draft rendering, what the review found, final rendering. Never go quiet through a long render.
