# Choosing sound effects like a human editor

A human editor does not synthesize a click. They search a few libraries for a recorded one, listen to a handful at the same loudness, pick the one that fits the object and the move, trim it to the frame, and make sure the click that matters is heard. The ones that do not matter get no sound at all. This file turns that workflow into steps an agent performs for every film. The sources and their licences are in `sfx-sources.md`; the rest of the mix (music against effects, loudness, the arc) is in `sound.md`.

Two films taught it. In the first Enogon film the same slide sound played on every slide, and it was a bad one. In Enogon v2 the clicks were very quiet, although the clicks are what the story turns on and must be heard (`lessons.md`). Both come from one habit: treating sound as a one to one map from picture events to one sample at one fixed gain. A human editor turns that around: decide which few moments carry the story and make those unmistakable, then let the music and a quiet, varied texture carry everything else (`research/free-sfx/report.md`, Conclusion).

The research behind every number is in `research/free-sfx/` (report and seven notes, read on 31 October 2026). Numbers marked **(heuristic)** are working starting points derived by the research or by this file, not measured or published values. The agent cannot hear: every "audition" below is a measurement plus a look at the waveform and spectrogram, and the reply says "measured, not heard".

## 1. What the professionals measure

- **Published SaaS and brand films use few separate effects and let the music carry the motion.** Ten films measured from the mix (Superhuman, Linear Releases, Arc 1.0, Framer, Screen Studio, Supademo, a Zelios agency explainer, What a Story, Motion Swell, Raycast Pro) carry **0 to 9 clearly designed accents per minute**: risers into drops, impacts on section starts and logos, a whoosh on the switch from live action to the UI, a silence or hard cut before a hit. Across all ten, whooshes appeared at only 4 to 5 transitions in total, never once per motion, and in the two films with the most on screen UI motion every audible attack sat on the music's grid: the music "sounded" the motion (`notes/case_studies_measured.md`).
- **Accents peak 7 to 13 dB over the bed** in the middle of a film (the bed is the median 50 ms level of the music in the 1.5 s before), and 17 to 25 dB only after a quiet intro or a silence, so big contrast is made by pulling the music down, not by pushing the effect up. Raycast's end: a 1.45 s noise riser at +9.2 dB, 150 ms of silence, the logo impact at +12.8 dB.
- **Audible UI clicks were not confirmed in any of the ten mixes.** The closest case is Screen Studio, two possible clicks at +6.4 and +9.3 dB on the frame a "Private" toggle appears. Where a click is there, it is tied to one meaningful action. These counts are lower bounds: quiet clicks under music cannot be confirmed from a mix.
- **Sound designed launch films** (Tomas Havranek's Contra and HeroUI, with published stems) carry three continuous families each, audible 28 to 61 percent of the running time, sitting **3 to 14 dB under the music**: Contra's transitions (long low swells) a median 2.6 dB under, the typewriter thread 7.5 dB under, the digital UI tones 13.8 dB under. The only effects 17 to 21 dB over the music fell in silent gaps between the music's hits; once the music stopped for 2.4 s and the effects carried the moment alone.
- **The AI pattern is the opposite.** The mgpro film torq had 191 cues in 30 s across 29 sound types, each tied to a picture event, at fixed per type gains varied by only 1 dB. The earlier AI films hit cuts 18.6 times above baseline against 1.18 for 2,666 professional cuts, and shared 42 percent of their strong transients between films against 4.6 percent for unrelated professional films. Counting cues does not separate human from machine (the stem films have 217 to 242 onsets per minute); families, level against the music, coupling to every event and repetition across films do.

## 2. The steps for every film

1. List the film's sound moments by role and tier (section 3).
2. Choose 3 or 4 sound families for the whole film (section 4).
3. Search each role with action, feel and context words, every synonym, and a duration filter (section 5).
4. Audition the candidates at matched loudness and judge their fit to the move (section 6).
5. Drop the sounds everyone uses (section 7).
6. Build a pool for every repeated role: 5 to 8 takes from at least two sources (section 8).
7. Prepare each file: cut to the moment, lead silence trimmed to the transient, tail faded, clicks high passed (section 9).
8. Record every file's licence in `public/sfx/ASSETS.txt` (`sfx-sources.md`, section 6).
9. Write the cues with `"file"`, `"story"` and `"gain"`, follow the click rule, and measure the story sounds (sections 10 and 11).

## 3. List the moments by role and tier

Before any search, go through the storyboard and give every visual event a role (the rows of the table in section 12) and one of three tiers, or no sound. The tiers come from the level research (`notes/levels_and_placement.md`, OverseerOS's background, supporting and foreground classes) and the measured films above:

| Tier | What it is | Level | How many | In the cue list |
|---|---|---|---|---|
| **Story** | The actions the story turns on: the click that opens the next scene, the press that exports, the reveal hit, the logo | Peak **6 to 9 dB over the bed**, with a 2 to 4 dB music dip of about 150 ms where it still hides; up to 9 to 17 dB for the reveal and the logo, 17 to 25 only after a silence (measured films above). With a voiceover, about -10 to -12 dBFS peak, at most -8 (**heuristic**, synthesized from PremiumBeat, Epidemic Sound and Krotos) | 2 to 5 story clicks in 30 s, 1 to 2 impacts, 1 logo (section 12) | `"story": true`, `weight` support (hero for the reveal and the logo), `"gain"` set by measurement |
| **Supporting** | Slides and swishes on the hero move of a scene, pops for a group appearing, secondary clicks | Under the music: a slide about 3 dB under (Contra's transitions 2.6 dB under), pops and secondary clicks 4 to 8 dB below the story clicks; about -14 to -18 dBFS with a voiceover (**heuristic**). "If a viewer notices the whoosh consciously, it is too loud" ([Zella](https://zellahq.com/blog/sound-design-at-cuts-whoosh-impact-riser/)) | At most one slide per 3 s (HeroUI's ceiling); group moves get one sound | `weight` support |
| **Texture** | Typing runs, paper rustles, UI tones, room tone | About 7 to 14 dB under the music (Contra: typing 7.5, UI tones 13.8); -22 to -35 dBFS with a voiceover (**heuristic**) | One typing burst per text field | `weight` ambient (about a third of ambient cues play nothing, by design) |

Everything else gets no cue: most motion, most cuts, every hover and small fade. Film Editing Pro's rule: "if you try to make every moment special none of them will be special" ([YouTube](https://www.youtube.com/watch?v=Wcxw3BPSt3A)). If muting a sound changes nothing, delete it ([Sonilo](https://sonilo.com/ai-music/whoosh-sound-effect-guide)). If the music already swells or resolves on a cut, a whoosh on top is redundant ([Sonilo](https://sonilo.com/blog/guides/transition-effect-sound-video-edits)).

## 4. Choose 3 or 4 families for the film

Editors commit to a palette before placing anything: "commit to a style instead of mixing random sounds", since gritty bass hits do not belong in a corporate film (Herman Huang, [YouTube](https://www.youtube.com/watch?v=tzfzkTAQsnE)); both stem films use exactly three families. Pick them from the product's world: a paper and ink brand gets paper foley and pen strokes, a hardware product its own materials, a calm SaaS tool soft air swishes and soft ticks. If the real product makes no sounds, soft designed ticks that agree with each other read better than literal desktop clicks, because sounds that do not match the product read as a mistake ([IRPR](https://sounddesign.irpr.agency/applications/app-videos/)). Write the families in the sound plan of `SCRIPT.md`, and choose them so no hero or support family repeats the last film's (`sound.md`, section 4b).

Example for a light technical drawing brand: mouse clicks (recorded hardware), paper and card (cardboard slides, a pen), soft air swishes (sticks and cloth), and the music for everything else.

## 5. Search each role

Real searches are short and generic, which is why results sound alike. Freesound's most searched terms in 2024 were "wind, rain, explosion, music, whoosh, footsteps, woosh, click", and over 81 percent of searches kept the default relevance sort ([Freesound blog](https://blog.freesound.org/?p=2141)). So everyone who types "whoosh" downloads the same few files: qubodup's CC0 "Whoosh" (ID 60013) has about 209,800 downloads. Search wider:

- **Action plus feel plus context**: "whoosh soft short", "impact deep muted", "UI click success", "typing modern" ([Pixabay blog](https://pixabay.com/blog/posts/free-and-high-quality-sound-effects-for-video-edit-453/)).
- **Every synonym**: whoosh, swoosh, swish, woosh; impact, hit, slam; bubble, pop, plop; click, tick, tap, press, button; riser, rise, swell.
- **A material word** gets sounds other editors have not used: cloth, paper, air, bamboo, stick, flag, wood, plastic, cardboard. **Exclude the trailer vocabulary**: "-cinematic -trailer -epic" (Freesound takes "+word -word", [forum](https://freesound.org/forum/production-techniques-music-gear-tips-and-tricks/44539)).
- **Sort by newest or by rating**, not relevance, to step off the path everyone walks.
- **Filter in this order**: licence first (CC0, or the source's own clause from `sfx-sources.md`, table 1), then duration (under 1 s for clicks, taps and pops; 0.3 to 3 s for whooshes and transitions; Pixabay's guidance is under 1 s for UI and 1 to 3 s for transitions), then WAV at 48 kHz, "a safe default for video" ([Pixabay blog](https://pixabay.com/blog/posts/free-and-high-quality-sound-effects-for-video-edit-453/)). On the Freesound API: `filter=license:"Creative Commons 0" duration:[0 TO 1] avg_rating:[4 TO 5]`, and the field is the singular `tag` ([Freesound API](https://freesound.org/docs/api/resources_apiv2.html)).
- Freesound files average 73 s, so the useful moment usually sits inside a long recording and is cut out (section 9).

Search terms per role (the first three come from the sources, the rest follow the action, feel and context rule):

| Role | Search terms |
|---|---|
| Story click | "mouse click", "trackpad click", "click soft", "mouse click single", "button press" |
| Typing | "keystroke single", "typing laptop", "keyboard soft", "typing quiet" |
| UI tap, toggle | "UI click", "switch soft", "toggle", "button tick", "UI click success" |
| Pop | "pop soft", "plop", "bubble pop", "pop short" |
| Slide, swish | "swoosh short", "swish cloth", "whoosh soft -cinematic", "stick swing", "air pass" |
| Big object move | "whoosh low", "whoosh bamboo", "swing heavy" |
| Paper, foley | "paper slide", "page turn", "paper rustle", "cardboard slide", "wood tap", "card on table" |
| Impact | "impact muted", "hit soft", "thud wood", "knock" |
| Riser | "swell", "riser short", "reverse cymbal", "breath swell" |

## 6. Audition at matched loudness and judge the fit

**Audition.** Shortlist 3 to 6 candidates per role by length first (about the length of the move or shorter) **(heuristic: no source gives a number of candidates)**. Level match them before judging, because the louder take always seems better ([Sonilo](https://sonilo.com/ai-music/whoosh-sound-effect-guide)): peak normalise every candidate (the kit's `recording()` does this) or match their loudness. Then, without ears: measure each with `sfx_catalog.py --file <candidate>` (attack, d20, total length, centroid, band shares, noisiness, pitch movement, width, `lead_ms`), look at its waveform and spectrogram the way `sfx/sheets/` shows the library, and compare with the targets below. Place the best one with its peak on the fastest frame of the move and render; an editor nudges one frame either way at normal speed, and the agent checks the onset against the frame (`sound.md`, section 6). When it matters, ask the user to listen to the two finalists.

**Judge the fit.** "A convincing whoosh sound effect follows the motion's speed, mass, direction, distance, and stopping point" ([Sonilo](https://sonilo.com/ai-music/whoosh-sound-effect-guide)).

- **Material**: paper for paper, wood for wood, a real air pass for a card, a mouse for a cursor. A heavy metallic clank on clean digital text is the classic mismatch ([SFX Engine](https://sfxengine.com/blog/common-sound-design-mistakes-in-video-editing)). For a card, a page or a box flap, a short paper or cardboard sound beats any whoosh.
- **Size**: big objects get lower, longer sounds; MKBHD's team gives a rotating phone "a big, low-pitched whoosh to convey its mass" ([summary](https://gist.ly/youtube-summarizer/master-video-editing-creative-choices-pro-tips)). Pitching a file a few semitones down adds mass, up makes it smaller; past 4 to 5 semitones the processing itself is heard ([Swell AI](https://www.swellai.com/blog/how-to-pitch-shift-in-audacity)).
- **Speed**: short, bright envelopes read fast and light; long builds read broad or heavy.
- **Length matched to the motion**: "a whoosh that outlasts its transition is the most common reason one feels wrong" ([Morphic](https://morphic.com/resources/sounds/whoosh-sound-effect)). A tiny card crossing 10 percent of the screen in 180 ms gets a 150 to 300 ms swish trimmed from a longer file; a 0.48 s title reveal leaves its last 80 ms empty for a separate landing ([Sonilo](https://sonilo.com/ai-music/whoosh-sound-effect-guide)). Build short, medium and long takes from different files rather than time stretching one, which smears transients into metallic artefacts.
- **Pitch**: a pitched sound must sit in the music's key or be unpitched ([CRI Middleware](https://blog.criware.com/index.php/2020/05/20/keeping-sfx-in-key/)). Clicks, swishes, paper and taps should be unpitched noise; a found pop, chime or sting with a clear note is checked against the score's key (`sfx_catalog.py` prints its `note`), shifted to a scale note, or dropped.
- **Measured targets** from the local CC0 library (`sfx/ANALYSIS.md`): a good click falls 20 dB in 4 to 18 ms, attacks in under 1 to 3 ms and centres at 1.9 to 4.6 kHz with under 10 percent of its energy below 500 Hz; a real swish is a low "whum" with a whistle, 60 to 160 ms, centred at 190 to 600 Hz; only designed airy transitions sit at 5 to 13 kHz, and they read as digital. A good product pop is soft and short, 70 to 110 ms near 740 to 990 Hz, rising 3 to 7 semitones.
- **Phone test**: high pass every click at 150 to 200 Hz and keep it only if it still reads; a file that vanishes after the filter was mostly thump ([Cursa](https://cursa.app/en/page/sound-design-that-reads-on-small-speakers)). In `sfx_catalog.py` terms, its energy leans to the 2 to 6 kHz band, with under 10 percent below 500 Hz.
- **Dry or wet**: quick UI sounds stay dry and narrow, since "heavy reverb on quick UI sounds increases masking" ([media.io](https://www.media.io/audio-effects/quick-sound-effects.html)); motion sounds get a little of the film's shared room to glue them in (Joe Vanz uses about 15 percent wet, [YouTube](https://www.youtube.com/watch?v=GovWYxWNS54); the kit's effects bus goes through one shared room).

## 7. Avoid the sounds everyone uses

- **The top of a relevance search.** The first result for "whoosh" is the most heard whoosh on the free internet (qubodup 60013). Take the third page, the newest uploads, or a material word instead.
- **Named overused sounds**: the Vine boom (a 2012 library sound that peaked on TikTok and YouTube in 2020 to 2022 and still signals meme editing, [Know Your Meme](https://knowyourmeme.com/memes/vine-boom-sound-effect)); the braam (Hans Zimmer said he felt "horrible" hearing Inception style braams in trailers, [The Playlist](https://theplaylist.net/hans-zimmer-feels-horrible-when-his-inception-bramms-are-used-in-movie-trailers-20131106)); anything named "epic trailer", "Swoosh Explosion" (Freesound 234555) or "Epic whoosh" (27281) for UI motion; operating system sounds (macOS Tink, the iPhone keyboard tick). For business content: "stick to whooshes, pops and clean zooms" ([Videotto](https://videotto.com/blog/add-sound-effects-and-meme-edits)).
- **The default of a tool.** Remotion ships Freesound 678248 as its built in `mouseClick`, so many Remotion films click with the same recording; Enogon v2 did. Prefer another recording for the story click, or at least a pool around it **(heuristic)**.
- **The last film's sounds.** No hero or support sound may come from the same file or recording as an earlier film's: write each role's files in the film's registry entry (`"effects": {"click": "file: freesound 683099, 213004, 347544", ...}`) and read the last entries before searching. Changing the pool between films is the fix for the 42 percent shared transients the first films had.
- **An untouched stock file.** "Using an untouched stock whoosh straight from a library" is listed as an amateur giveaway ([SFX Engine](https://sfxengine.com/blog/common-sound-design-mistakes-in-video-editing)): every file gets at least a trim, a fade and a level set for its moment.

## 8. Pools: no role repeats the same take

"The same whoosh on every move" is the most cited amateur tell ([media.io](https://www.media.io/audio-effects/whoosh-sound-effects.html): edits feel cheap "when the same type of sweep is used again and again"; [Filmora](https://filmora.wondershare.com/audio-editing-tips/whoosh-sound-effect.html)). Film Editing Pro's first pass mistakes were the same keyboard sound for every keystroke and the same pen sound for every stroke. The game audio fix transfers directly: **4 to 8 variations per sound type, random selection with no immediate repeats, and a few percent of random pitch and level per play** ([Bugnet](https://bugnet.io/blog/how-to-implement-footstep-variation-to-avoid-repetition); [DAFx 2021](https://acris.aalto.fi/ws/portalfiles/portal/67780224/DAFx20in21_paper_22.pdf)).

- **Every repeated role gets a per film pool of 5 to 8 takes from at least two sources** (slides, swishes, pops, card landings), 3 to 5 takes for story clicks, 6 to 10 single keystrokes for typing ([report](../research/free-sfx/report.md), A per film download pipeline).
- **Different recordings beat one recording at several pitches**: whole file pitch shifting helps less than changing the timbre. A cheap way to make a new take: the start of one whoosh with the tail of another, both peaking together ([Krotos](https://krotos.studio/guide/4-whoosh-sound-effects-tips)). Trim each take differently, and vary the path (across, past, toward, away) ([Sonilo](https://sonilo.com/ai-music/whoosh-sound-effect-guide)).
- **Jitter**: about half to one semitone of pitch ("a few percent": one semitone is 5.9 percent) and 1 to 2 dB of level per play; tonal sounds move by scale notes instead; a run of pops climbs 2 to 3 semitones per item, because a jitter of half a semitone does not read as a deliberate step.
- **A new pool for every film**, recorded in the registry so the next film avoids it (section 7).

**In the kit.** A cue's `"file"` names one recording. `vary.py` gives each play a different take of that recording (pitch jitter of the `sample` kind, 100 cents either way, and level within 1.5 dB), which is variation of one file, not a pool. The pool lives in `audio/cues.py`: rotate the role's files across its cues, never the same file twice in a row. Enogon v2's typing did this with two Kenney clicks:

```python
SWISH = ["sfx/swish-shinplaster-264777.wav", "sfx/swish-digitator-stick2.wav", "sfx/swish-halgrimm-169867.wav",
         "sfx/swish-soundresponse-07.wav", "sfx/swish-florianreichelt-683101.wav", "sfx/swish-digitator-badge1.wav"]
for n, f in enumerate(F["slides"]):                       # every slide a different recording, from three sources
    add(f, "swish", "support", file=SWISH[n % len(SWISH)])   # each file already cut to the move (section 9)
```

## 9. Prepare each file

The small edits are consistent across every source ([Krotos](https://krotos.studio/blog/audio-trimming); [SFX Engine](https://sfxengine.com/blog/sound-design-tips-for-video-editors); [Pro Sound Effects](https://blog.prosoundeffects.com/how-to-make-sound-effects-sit-better-in-a-mix)):

1. **Cut the useful moment** out of a long file, a little longer than the move. `ffmpeg -i long.wav -ss 12.34 -t 0.40 -ar 48000 cut.wav`.
2. **Trim the lead silence to the transient**, so the sync point is the transient and not the file start ([Morphic](https://morphic.com/resources/how-to/how-to-sync-sound-effects-to-video)). **The Enogon lesson: the click file had 123 ms of silence before its transient, so at 60 fps (16.7 ms a frame) the click landed 7 frames after the press.** The kit's `recording()` now trims it on load (section 10), but check `lead_ms` with `sfx_catalog.py --file` on anything placed by other means.
3. **Fade both ends**: abrupt starts and stops are a strong giveaway. A short fade in only if the file starts mid sound; a fade out so the tail ends when the picture settles (the kit adds 5 ms at the end; a longer tail is cut and faded in step 1).
4. **High pass clicks and taps at 150 to 200 Hz** so they read on phones, and most other effects at 80 to 100 Hz ([SFX Engine](https://sfxengine.com/blog/common-sound-design-mistakes-in-video-editing)); cut 200 to 400 Hz on a whoosh that muddies the music. Since mgpro 3.1.0 the kit high passes every `"story": true` cue at 170 Hz (`"hp"` on the cue changes it); for other found files do it when copying: `ffmpeg -i cut.wav -af "highpass=f=180,afade=t=out:st=0.30:d=0.06" -ar 48000 public/sfx/click-<author>-<id>.wav`.
5. **Mono and centred for clicks** (phones play effectively in mono); pan only what visibly travels.
6. **Name by role and source** (`click-florianreichelt-683099.wav`) in the film's `public/sfx/`, and add its line to `public/sfx/ASSETS.txt` (`sfx-sources.md`, section 6). Files that are not CC0 stay out of git.

## 10. The click rule: a story sound is clearly heard

**A click, or any sound, that drives the story must be clearly heard.** It is never mixed as background and never randomly skipped.

- **Level**: its peak sits about **6 to 9 dB over the music bed around it**. One Remotion oriented guide puts primary button clicks about +6 dB over the bed ([skills.sh](https://www.skills.sh/jeremielim/skills/ui-sound-design)), Screen Studio's possible toggle clicks measured +6.4 and +9.3 dB, and mid film accents in the ten films 7 to 13 dB. The number rests on one guide and two uncertain measurements, so measure each film (section 11).
- **A short music dip where it still hides**: 2 to 4 dB for about 150 ms around it. Story effects cut through by dipping the music briefly, not by pushing the effect: DaVinci Resolve's ducker defaults to 2.7 dB with 15 ms lookahead, 10 ms rise, 150 ms hold and 750 ms recovery, and its manual says 2 to 5 dB works "best most of the time" ([DaVinci Resolve Club](https://davinciresolveclub.com/davinci-resolve-audio-ducking/)); Cursa advises dipping the music 1 to 3 dB rather than raising the effect overall. This is not a gain hole (`sound.md`, section 9): it is under 5 dB, it lasts 150 ms and it has a cause on screen.
- **Off the music's own accents.** In the Contra stems the effects that rose above the music all fell in the gaps between the music's hits. A click on the same frame as a downbeat, a chord stab or a drum hit is masked whatever its gain; move the music's accent, thin the music at that frame, or let the click lead the beat **(heuristic, from the stems)**.
- **Bright**: high passed at 150 to 200 Hz, its identity at 1 to 3 kHz presence and 2 to 8 kHz energy, so it reads on phones ([Cursa](https://cursa.app/en/page/sound-design-that-reads-on-small-speakers)). Centred.
- **On the frame**: the transient on the frame the button visibly depresses, or up to one frame late, never two frames early. ITU-R BT.1359 puts detection at about 45 ms of lead and 125 ms of lag ([ITU](https://www.itu.int/dms_pubrec/itu-r/rec/bt/R-REC-BT.1359-1-199811-I!!PDF-E.pdf)); Netflix logs effects 2 or more frames off as an issue ([Netflix](https://backlothelp.netflix.com/hc/en-us/articles/115000533952-Sync-Effects)). If the button squashes over 2 to 3 frames, the click goes where it is smallest. A release, if the file has one, lands 1 to 3 frames later and 6 to 10 dB quieter, on the frame the button springs back **(heuristic: frame arithmetic, no source measured mouse press to release gaps)**.
- **Few**: one per action that causes the next beat, usually 2 to 5 in 30 s. Every other click is secondary (4 to 8 dB under it) or silent. With a voiceover, place it between stressed words rather than raising it over them.

### The kit fields that implement it

`templates/kit/audio/score.py` reads three cue fields for found sounds (the `effects()` loop and the `recording()` loader):

- **`"file"`**: plays this recording instead of a synthesized effect or a `samples.py` pick. `recording(path)` looks for it in the film's `public/` folder first (so `"sfx/click-florianreichelt-683099.wav"` is `public/sfx/click-florianreichelt-683099.wav`), then in the CC0 library at `~/.local/share/mgpro/sfx/` (or `$MGPRO_SFX`; so `"remotion-cc0/mouse-click.wav"` works without copying), then as an absolute path; a missing file stops the render. On load it resamples to 48 kHz, **cuts the silence before the first transient** (everything before the first sample over 8 percent of the peak, keeping 2 ms), **normalises the peak** to 1, puts a 5 ms fade on the tail and copies a mono file to both channels. Its comment names the reason: "a click file with 120 ms of lead lands 7 frames late otherwise". The cue's job (`sound`) still decides how it sits on its frame (`click` and `tap` start on it, `swish` and `whoosh` peak on it, `riser` ends on it) and its base level.
- **`"story": true`**: the cue is an action the story turns on. A support cue on a `cut: true` frame is no longer demoted to ambient, and an ambient story cue is raised to support, so it is **never in the third of ambient cues that play nothing**. It does not make the cue a hero: weight still sets the base gain.
- **`"gain"`**: a per cue multiplier. A cue's level on the effects bus is the job's level (`JOBS`: `click` and `tap` 0.5, `swish` 0.45, `card` 0.7) times the weight's gain (`hero` 1.0, `support` 0.4, `ambient` 0.16) times `gain`; the effects bus then enters the mix at `fx_level` (default 0.5) before mastering. A support click at gain 1 is 0.2 of full scale on the effects bus, which is what made the Enogon v2 clicks quiet; Enogon's rebuild set gain 3.6 (0.72). No fixed number gives 6 to 9 dB, because the bed differs per film and per moment: set it, render, measure, adjust.

In the kit since mgpro 3.1.0:

- `"file"` may be a list: a pool of recordings for one role, rotated without an immediate repeat (`vary.take`), so four clicks use three different recordings.
- every `"story": true` cue is high passed at 170 Hz (`"hp"` changes it) and the music ducks under it: `"story_duck_db"` in `music.json` (default 3 dB; Enogon uses 6), from 20 ms before the sound, back over about 150 ms.
- every found file a cue played is copied into `public/sfx/` with a licence line in `public/sfx/ASSETS.txt` (`copy_found` in `score.py`); files already under `public/` stay where they are, so keep your own `public/sfx/found/ASSETS.txt` for what you download.

**The limiter ceiling (Enogon, 31 October 2026).** At -14 LUFS with a busy bed, the master's limiter caps how loud a 10 ms transient can get: raising a click's gain from 8 to 10 moved its "over the bed" number by 0.2 dB. Past that point the levers are the duck (it raises "over the music at that moment above 1 kHz"), a fuller recording (a 42 ms click reads about 2 dB lower than a 100 ms one at the same peak), and keeping story clicks off the music's own accents. Gain alone is not the answer.

```python
# audio/cues.py: story clicks from a pool of three recordings, each a role and source named file
CLICKS = ["sfx/click-florianreichelt-683099.wav", "sfx/click-abstraktgeneriert-213004.wav", "sfx/click-masgame-347544.wav"]
for n, f in enumerate([F["grab"], F["wall"], F["field"], F["export"]]):
    add(f, "click", "support", story=True, file=CLICKS[n % 3], gain=3.6)   # gain from the measurement below
```

## 11. Measure your story sounds

A story sound passes only with a number. Render the score twice from the same cue list, once as it is and once with every effect cue at gain 0 (the `"notes"` cues are music and stay), so the difference between the two renders is the effects alone. For each `"story": true` cue, print how far it rises over the bed and over the music at that moment:

```python
# story_check.py: run from the film folder with the kit's Python (~/.local/share/mgpro/.venv/bin/python).
# Renders the score twice, with the effects and with every effect cue at gain 0, so the difference is the effects.
import json, sys
from pathlib import Path
import numpy as np
from scipy.signal import butter, sosfilt
sys.path.insert(0, str(Path("audio").resolve()))
import score
from dsp import SR

brief = json.loads((score.ROOT / "src/music.json").read_text())
cues = json.loads((score.ROOT / "src/cues.json").read_text())
sec = brief.get("length", 30.0)
full = score.build(brief, cues, sec, score.ROOT, verbose=False)[0]
muted = [c if c["sound"] == "notes" else dict(c, gain=0.0) for c in cues]   # "notes" cues are music
bed = score.build(brief, muted, sec, score.ROOT, verbose=False)[0]
fx = full - bed
hp = butter(4, 1000, "hp", fs=SR, output="sos")
fxh, bedh = sosfilt(hp, fx, axis=1), sosfilt(hp, bed, axis=1)

def db(x, a, n): return 20 * np.log10(np.sqrt(np.mean(x[:, a:a + n] ** 2)) + 1e-9)
def loudest(x, a):   # loudest 10 ms RMS from 10 ms before the cue frame to 50 ms after it
    return max(db(x, i, int(0.01 * SR)) for i in range(max(0, a - int(0.01 * SR)), a + int(0.05 * SR), int(0.005 * SR)))
for c in cues:
    if not c.get("story"):
        continue
    a = int(c["frame"] / score.FPS * SR)
    lo = max(0, a - int(1.5 * SR))
    bedlevel = np.median([db(bed, i, int(0.05 * SR)) for i in range(lo, lo + int(1.5 * SR), int(0.05 * SR))])
    meter = 20 * np.log10(np.abs(fx[:, max(0, a - int(0.01 * SR)):a + int(0.05 * SR)]).max() + 1e-9)
    print(f"frame {c['frame']:5d} {c['sound']:6s} over the bed {loudest(fx, a) - bedlevel:+5.1f} dB (rule: 6 to 9), "
          f"over the music at that moment above 1 kHz {loudest(fxh, a) - loudest(bedh, a):+5.1f} dB (3 or more), "
          f"peak meter {meter - bedlevel:+5.1f} dB (not the rule's number)")
```

How to read it:

- **Over the bed** is the rule's number: the effect's loudest 10 ms against the median 50 ms level of the music over the 1.5 s before it, the bed the ten films were measured against. The window is 10 ms, not the research's 50 ms, because a 50 ms window averages a 15 ms click with 35 ms of nothing and reads it about 5 dB low (10 log10 of 15/50) **(heuristic)**. Want 6 to 9 dB, more for the reveal and the logo.
- **Over the music at that moment above 1 kHz** catches a click masked by a music accent on the same frame: in the click's own band, it should be at least about 3 dB louder than the music in the same 60 ms **(heuristic, from the Contra stems and the Enogon measurement below)**.
- **Peak meter** is the sample peak against the same bed, what a DAW's meter suggests. For the Enogon clicks it read 14 to 17 dB higher than the RMS numbers (a click's crest factor), so never report it as "over the bed".
- The two renders are mastered separately, so the muted one is slightly louder; that makes the numbers a little conservative. Each build takes about a minute.

**On Enogon v2.** The rebuild reported its clicks at "6 to 20 dB over the bed". This check, run on the shipped cue list on 31 October 2026, printed over the bed -0.2, -1.0 and -2.1 dB for the three mouse clicks at frames 40, 896 and 940, -3.4, -7.7 and -6.2 dB for the three typed keys, and -2.0 dB for the Export press at frame 1088, and over the music above 1 kHz +7.6, +1.7, +4.0, +1.8, -8.1, -5.7 and -1.9 dB; the peak meter numbers were +7.4 to +14.7 dB, which is the likely source of the higher figure. So the rule was not met: the clicks needed more gain, a high pass, and room under the music. After the 3.1.0 fixes (three CC0 recordings rotated: Remotion's 678248, Freesound 683099 and 213004 cut to one click each; story cues; gain 8; the 170 Hz high pass; a 6 dB story duck) the same check printed over the bed +8.0, +5.3, +3.2 and +6.7 dB for the four clicks and +2.7 to +3.9 dB for the typed keys, and over the music at that moment above 1 kHz +5.3 to +16.8 dB: every click unmasked, three of four within 1 dB of the rule's band, the field click held at +3.2 by the limiter ceiling below. Report both numbers and the method every time.

## 12. The table per sound type

Levels "over bed" are for music led films; the dBFS figures apply when a voiceover anchors the mix. Budgets assume a 30 s film and are **derived, not quoted**: no source publishes per type counts for product ads. Source: `research/free-sfx/report.md`, Ready to use table per sound type; IDs are Freesound unless named (`sfx-sources.md`, section 5).

| Sound type | First sources, IDs or search terms | Licence | Length used | Level | Timing | Budget per 30 s | Variation |
|---|---|---|---|---|---|---|---|
| Story cursor click | 678248, 347544, 213004, 448086, 683099, 108336; trackpad 118206, 197169, 332010 (check the page); Kenney UI Audio clicks; Mixkit "Mouse click close", "Select click"; search "mouse click", "trackpad click", "click soft" | CC0, Mixkit Free, Pixabay | 30 to 150 ms audible; head trimmed to the transient | +6 to +9 dB over the bed, a 2 to 4 dB music dip for about 150 ms; about -10 to -12 dBFS between words with a voiceover | Transient on the press frame or 1 frame late, never 2 early; an optional release 6 to 10 dB quieter 1 to 3 frames later | One per action that causes the next beat, usually 2 to 5 | 3 to 5 takes, no repeat in a row, 0.5 to 1 st and 1 to 2 dB either way; high passed 150 to 200 Hz, mono |
| Secondary click, hover | Kenney Interface Sounds; or nothing | CC0 | 30 to 100 ms | 4 to 8 dB under the story clicks | On the press frame | Few; hovers silent | The same family, small pitch shifts |
| Keyboard typing | OpenGameArt "Keyboard Soundpack #1" (CC0); 729421, 391541; Mixkit "Typing on a laptop keyboard"; search "keystroke single", "typing laptop", "keyboard soft". "Soft keyboard tones suit modern looks better than mechanical clacks" (Pixabay) | CC0, Mixkit Free | Single strokes 40 to 120 ms, or a burst the length of the word | About 7 dB under the music; under the story clicks | A stroke on every 2nd or 3rd character, under 10 to 12 per second; a heavier stroke on space or enter | One burst per text field | 6 to 10 strokes, no repeat in a row, 1 to 2 st and 2 to 3 dB either way |
| UI tap, toggle, notification | Kenney UI Audio (38 switches), Interface Sounds; Mixkit "Modern click box check", "On or off light switch tap", "Positive interface beep"; 244266 (unfa) | CC0, Mixkit Free | Taps 30 to 150 ms; cues under 300 ms; tails under 1 s | About 14 dB under the music on average, above it only in its gaps | On the snap frame | One per meaningful state change; one chime per new panel | One tonal family in the score's key; on rises, off falls |
| Pop, an element appears | 202230 (deraj), 240566 (onikage22), 447910 (Breviceps), 59978 (OGMeek); Mixkit "Explainer video pops whoosh light pop"; search "pop soft", "plop", "bubble pop" | CC0, Mixkit Free | 70 to 110 ms | Supporting, well under the story clicks; -14 to -18 dBFS | 1 to 2 frames before full scale, on the overshoot | One per group, 2 to 4 | Rising 2 to 3 st per item in a sequence; dry, mono |
| Slide or swish: card, text, picture | 264777, 169867, 683101, 59988, 127197, 181889; Sound Digitator Mini Whooshes; SoundResponse 20; Mixkit "Air woosh", "Arrow whoosh"; Pixabay 405445, 405447, 379079; search "swoosh short", "swish cloth", "whoosh soft -cinematic" | CC0, free commercial, Mixkit, Pixabay | Equal to the travel time: 150 to 300 ms for a fast card, up to 1.2 s for a slow pass | About 3 dB under the music (6 dB under speech); never consciously noticed | Starts 2 to 6 frames early, peaks on the fastest or the settle frame, the tail ends when the picture settles | The hero move of each scene only; at most one per 3 s; a group move gets one | A pool of 5 to 8 files from 2+ sources, no repeat in a row, 1 st either way, different trims, pan with the direction |
| Big object or product move | Pixabay "Whoosh Bamboo" 389752; qubodup's megaswosh files; Sonniss; 99Sounds whooshes | Pixabay, CC0, Sonniss, 99Sounds | 0.5 to 1.2 s, matched to the move | At the music's level to a few dB above | Peak on the fastest frame; a landing layer only if it visibly stops | 1 to 2 | Pitch down a few st for mass; a different file from the small swishes |
| Scene transition | 99Sounds "Cinematic Transitions"; Mixkit transition and swell tags; Sonniss; Zapsplat (credit) | 99Sounds, Mixkit, Sonniss | 400 to 500 ms for a 0.5 s transition; tail less for hard cuts | 7 to 13 dB over the bed when featured | Starts before the cut, peaks on the first frame of the new shot | Section changes only, 1 to 3; skipped where the music already resolves | Alternate a whoosh, a reverse swell and the next scene's sound pre lapped |
| Paper and foley | 344432 (GrayJoy), 135014, 364932, 339365, 271318, 407405; designerschoice pack 43548; Nox_Sound; Fiftysounds paper; Kenney Impact Sounds wood and soft; search "paper slide", "page turn", "cardboard slide", "wood tap" | CC0, royalty free, Fiftysounds | Single events cut from long files, 100 to 500 ms | About 7 dB under the music; contact moments may rise | Contact on the frame | Replaces whooshes for physical objects | Many events cut from one recording, each used once |
| Impact, landing | Kenney Impact Sounds; Mixkit "Metal hit woosh"; 99Sounds impacts and transients; BOOM processed impacts; Sonniss | CC0, Mixkit, 99Sounds, BOOM, Sonniss | Transient plus a 150 to 450 ms tail; the sub trimmed | 7 to 13 dB over the bed mid film; up to 17 to 25 after a silence; peak about -10 dBFS, at most -8 | Exactly on the contact or the cut; an optional 100 to 300 ms silence before | 1 to 2 | A 1 to 5 kHz transient layer for phones; never the same hit twice |
| Riser, swell | Mixkit swells (23); 181889; Fiftysounds risers; Pixabay "Riser Wildfire" (trim) | Mixkit, CC0, Fiftysounds, Pixabay | 1 to 3 s (1 to 2 bars) | Peak 6 to 9 dB over the bed | Starts about 1 s early, stops dead on the reveal or the downbeat | 1 to 2 | High passed below 100 Hz; tonal risers in the key |
| Logo sting | The music's own final hit first, plus a soft swish or air swell; Mixkit "Movie whoosh impact presentation" | Music; Mixkit | Hit plus tail under a 1.5 to 3 s hold | The loudest accent, 9 to 17 dB over the bed | The landing frame or 1 frame early, after one clean frame | 1 | A non tonal layer over the music; never the brand's reusable sonic logo (`sfx-sources.md`, section 4) |

## 13. Before calling the sound done

- Every story sound measured by section 11, both numbers written in `REVIEW.md` (`review.md`, Self check 9).
- No role plays the same file twice in a row; every repeated role has a pool from at least two sources.
- Every file has its line in `public/sfx/ASSETS.txt`; non CC0 files are out of git.
- The "remove 50 percent" test: mute half the decorative effects and compare; keep the version that loses nothing ([OverseerOS](https://www.overseeros.com/blog/youtube-sound-design)). The mute test per sound: if muting it changes nothing, delete it.
- OverseerOS's twelve mistakes as a last pass: sound on every cut, effects over important words, the same whoosh repeated, music and effects fighting the voice, everything cinematic, no ambience, ambience too loud, no dynamic range, mixing in solo, mixing only on headphones, mastering to fix the mix, and adding effects because the video feels boring.
- Check on a phone speaker, in mono and at low volume, or say that it was not checked. "Measured, not heard."
