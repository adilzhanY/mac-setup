# Sound: the practical manual

**Music is decided in `music.md`** (genre, tempo, key, palette, hook, form, the registry). This file is everything else: which sound goes on which event, how it is built, where it lands to the frame, how loud it sits against the music, how the film breathes, and how to master it for where it is shown. Where a rule came from, with its source and numbers, is in `sound-research.md`. The CC0 sample library and its measurements are in `sfx/` (`sfx/README.md`, `sfx/ANALYSIS.md`, `sfx/CATALOG.md`, contact sheets in `sfx/sheets/`).

**Sound effects are found, not made** (Oct 31 2026). For every film the agent searches free libraries for premade, human recorded effects, the way a video editor does, and chooses each one for its moment: `sfx-selection.md` is the workflow (roles and tiers, search, audition, fit, pools, trimming, the click rule, measuring), and `sfx-sources.md` is the catalogue of free sources with their licence clauses. A premade recording found for the film is the first choice for every effect; the kit's synthesized effects (section 3, In the kit) are only for a film's signature sound or when no search turns up anything that fits.

Two facts shape everything below. First, the first three films made with this skill measured as near copies of each other, and as louder, brighter, more on the grid and more slammed on every cut than 129 professional films (section 12). Second, the agent cannot hear. Every rule here is something that can be planned from the cue list and measured in the rendered file; say "measured, not heard" in the reply, every time.

Numbers marked **(heuristic)** are working starting points chosen by the research, not measured or published values. Everything else carries its source in `sound-research.md`.

## 1. The short version

1. **Sound is planned with the storyboard**, not added after the picture. Every shot card names its sound weight and sync point (`storyboard.md`).
2. **Hierarchy.** One to three hero sounds in a 30 s film (the reveal, the title, the end card), small short sounds for support events, nothing for most events. The music carries ordinary cuts, and only structural cuts sit on a bar downbeat (sections 6 and 7). In the cue list this is each cue's `weight` and `cut`.
3. **Every sound has a type and a size.** Pick the type from the vocabulary (section 3), the weight from the object's size and material (section 5), the pitch from the score's key.
4. **Sync by type.** Impacts and taps on the contact frame; whooshes peak on the cut; risers end on it (section 6).
5. **Nothing repeats the same way.** Every repeated role (slides, swishes, pops, landings) gets a per film pool of 5 to 8 different recordings from at least two sources, never the same file twice in a row, with small changes of pitch and level per use; within the film and across films (section 8, `sfx-selection.md` section 8). No job uses the same source (recording, synth recipe or sample family) as the last film.
6. **Contrast is arranged, never a gain hole.** The film breathes by thinning the arrangement over a bed or a ringing tail, never by pulling the level down; a level change under about 3 dB is not heard, and a deep drop with no musical reason reads as a broken mix (section 9, corrected after the Enogon review).
7. **Recordings first, found per film.** Effects are premade, human recorded sounds found for this film from free sources (`sfx-selection.md`, `sfx-sources.md`), instruments are recorded samples, all in one shared room; synthesis is the fallback, or the signature (section 4b).
8. **An arc that moves.** Start below the body, stay alive until about 85 percent of the length, put the loudest moment where this story needs it, which is not where the last film had it (section 10).
9. **Darker and more dynamic than the first films**: centroid 1.0 to 2.6 kHz, little above 6 kHz, loudness range 5 to 11 LU (sections 10 and 12, and `music.md`, Tonal balance).
10. **Every impact survives a phone speaker**: a 120 to 500 Hz knock and a 2 to 5 kHz click on top of any sub (section 14).
11. **Master to the destination** (section 13), then check the decoded file, the stream and the sync.
12. **Story actions are clearly heard.** A click or any sound the story turns on peaks about 6 to 9 dB over the music bed around it, with a 2 to 4 dB music dip of about 150 ms where needed, high passed at 150 to 200 Hz, on the press frame or up to one frame late, never skipped and never mixed as background; cue fields `"story": true` and `"gain"`, checked by measurement (`sfx-selection.md`, sections 10 and 11).

## 2. The sound plan comes first

Sound is decided at concept, by job: what each moment must make the viewer notice or feel (attention, confidence, release, or staying in the background). Studios that win sound awards bring it in before picture lock and treat music and effects as one discipline.

- Unless the brief asks for a silent film, every film gets music and sound design from the start. A silent result is never called "scored".
- In the storyboard, each shot card's Sound field holds: the weight (hero, support, ambient, or none), the sound type, the event and frame it syncs to, or an explicit "nothing, the music carries it".
- In the cue list (`audio/cues.py` writes `src/cues.json`), every cue carries `weight` (`hero`, `support` or `ambient`) beside its frame and `sound`, and `cut: true` when it marks a picture cut. `score.py` plays the weights at gains 1.0, 0.4 and 0.16, lets about a third of ambient cues play nothing, keeps full size and the long sub only for hero impacts, and reports more than one hero per 8 s. Defaults when `weight` is missing: `logo` and `boom` hero, `texture` and `tick` ambient, the rest support. Other cue fields: `size` (0 to 1, or `"light"`, `"heavy"`), `material` (overrides the film's character), `seconds`, `index`, `on` (toggle), `notes` (the logo's hook as MIDI notes), `air` (whoosh), `direction` (1 or -1), `pan`, `loose` (allows a small start offset). For found sounds: `file` (a recording in the film's `public/` folder or the CC0 library, played instead of the synthesized effect, its lead silence trimmed to the transient and its peak normalised), `story` (`true` for an action the story turns on: never demoted to ambient, never skipped) and `gain` (a per cue level multiplier); `sfx-selection.md`, section 10, says exactly what each does.
- Anything that counts or runs (typing, ticks, a counter following a line) is generated from the same formula the picture uses.
- Effects support a musical accent, complement it, or leave it room. Never double every musical hit with an effect, and never put the same whoosh on every transition. A set of whooshes and hits does not replace a composition (`music.md`).
- After a speed ramp or a retimed shot, recompute the accent frames from the new timing; do not change the music's tempo or pitch by accident.
- The risk probe before the full build (`storyboard.md`) is made with sound when the film has sound, because a move that works silent can feel late or empty against its hit.

## 3. The vocabulary of sound types

Motion graphics sound is a small vocabulary of jobs: movement (whoosh, swish), anticipation (riser, reverse swell), arrival (impact, thud, click, pop, sub drop), identity (tonal hit, sting, sonic logo) and glue (bed, texture). A movement sound follows speed, mass, direction and where the move stops; a landing sound fires only when an object visibly stops, attaches or appears.

The numbers below are targets measured on the CC0 library's designed sets (`sfx/ANALYSIS.md`, section 4), unless the row says otherwise. **d20** is peak to -20 dB, the part a viewer actually hears; **total** is peak to -40 dB. Level is against the music at that moment and is a starting point **(heuristic)**.

| Type | Job and visual event | Attack | d20 | Total | Centroid | Pitch movement | Width | Level vs music |
|---|---|---|---|---|---|---|---|---|
| tap, click | a press, a cursor click, a key | under 1 to 3 ms | 4 to 15 ms | 10 to 60 ms | 1.5 to 4.5 kHz, under 15 % of energy below 500 Hz | a ping that falls 5 to 15 st in 40 ms, or none | 0 to 0.4 | -8 to -14 dB |
| UI blip, select | a state change, a field filled, a word landing | under 2 ms | 13 to 35 ms | 35 to 180 ms | 1.2 to 3.5 kHz | falls 1 to 2 st | 0 to 0.3 | -10 to -14 dB |
| tick (data) | a counter step, a scroll detent, a data point | under 1 ms | 4 to 9 ms | 9 to 25 ms | 3 to 10 kHz | flat; a run rises by scale notes | mono | -12 to -18 dB |
| soft pop | a round element appears (badge, avatar, dot) | 1 to 5 ms | 10 to 40 ms | 70 to 110 ms | 650 to 1000 Hz, nothing in 2 to 6 kHz | rises 3 to 7 st | mono | -10 to -14 dB |
| toggle | on and off | under 2 ms | 50 to 80 ms | about 100 ms | two tones about 1 to 1.6 kHz | two notes, rising for on, the same pair falling for off | mono | -10 to -14 dB |
| thud (card lands) | a card, panel or chip settles | 0 to 5 ms | 12 to 30 ms | 80 to 180 ms | 70 to 450 Hz, 85 to 100 % under 500 Hz | a short drop | mono | -8 to -12 dB |
| big impact | a hero arrival: title slam, product lands, stamp | 0 to 12 ms | 30 to 60 ms body, then a tail | 0.4 to 1 s | 70 to 420 Hz, 60 to 80 % sub but 22 to 33 % in 120 to 500 Hz | the body drops | 0 to 0.5 | 0 to +3 dB, music ducked 3 to 6 dB |
| sub drop, boom | the floor drops under a reveal or a drop | 0 ms, phase starts at 0 | long by design | 1 to 4 s | 30 to 110 Hz plus a click and harmonics | glides from 80 to 110 Hz down to 30 to 45 Hz over 0.5 to 2 s **(heuristic)** | mono | under the impact |
| fast swish | a quick slide, a swipe, a fast cut | 10 to 30 ms, peak early | 8 to 28 ms | 60 to 160 ms | 200 to 600 Hz, nearly all under 2 kHz, often a whistle tone | a small bend | 0 to 0.3 | -6 to -10 dB |
| heavy swing | a big or heavy object passes | 30 to 100 ms | 30 to 50 ms, then a tail | 300 to 500 ms | 400 to 450 Hz, 80 % or more in 120 to 500 Hz | falls about 2 st | 0.5 to 1.2 | -6 to -10 dB |
| airy whoosh | a designed transition, light across glass, a camera sweep | 70 to 170 ms | 300 to 440 ms | 0.5 to 1.1 s | 5 to 8.5 kHz, noise | a slight rise | 0.4 to 0.9 | -8 to -12 dB, use rarely (it is what makes a mix bright) |
| panel open, close | a sheet or panel opens (rise) or closes (fall) | open 200 to 280 ms with the peak at the end; close starts at its peak | open stops within 1 to 2 ms | about 300 ms | high noise | open rises 6 to 17 st, close falls 5 to 17 st | mono or wide | -10 to -14 dB |
| riser | anticipation before a reveal or a drop | the whole sound is the attack | stops dead | 0.5 to 4 s | a filter opening from about 200 Hz to 10 kHz **(heuristic)** | up, on an accelerating curve | widens as it peaks | rising to about -6 dB, then gone |
| reverse swell | a softer lead in: a reversed reverb tail into a hit | the whole sound | stops on the frame | 0.5 to 2 s | follows its source | none | wide | as the riser |
| downlifter | release after a drop or a reveal | instant | slow | 0.5 to 2 s | a filter closing from 8 kHz to 200 Hz **(heuristic)** | falls about an octave | wide to narrow | -10 dB |
| success chime | a task done, a check, a payment | 0 ms per note | 190 to 290 ms | 280 to 500 ms | 1.2 to 2.6 kHz | 2 to 6 notes 60 to 80 ms apart, flat or rising | 0 to 0.6 | -8 to -12 dB |
| error | something wrong, a shake | 0 to 15 ms | 40 to 75 ms | 100 to 200 ms | 180 to 1000 Hz, some buzz | flat or falling; a semitone clash | mono | -10 to -14 dB |
| tonal hit, sting | an accent the score can own: a title, a number | 0 to 5 ms | 100 to 300 ms | 0.5 to 2 s | follows the chord | a chord in the key | 0.2 to 0.6 | 0 to -6 dB |
| sonic logo, logo bell | the end card | 1 to 50 ms | 110 to 380 ms | 1.2 to 2.4 s (the whole logo 1.5 to 4 s) | 0.7 to 3 kHz, inharmonic partials | the hook's first 3 to 5 notes | 0 to 0.5 | at or under the loudest moment |
| glitch | a digital error, a stutter cut | under 2 ms | per slice | 50 to 400 ms **(heuristic)** | 0.5 to 8 kHz | random slices | hard panned slices | -10 dB |
| shimmer | magic, AI at work, sparkle | slow | long | 1 to 3 s | 2 to 10 kHz partials in the scale **(heuristic)** | none | wide | -16 to -22 dB |
| data chatter | a system computing, lists filling | under 2 ms | 10 to 30 ms per blip | as long as the event | high passed at 1 kHz | random scale notes, 10 to 30 per second **(heuristic)** | moving | -18 to -24 dB |
| bed, texture | glue under a scene, room tone | slow | n/a | the scene | low passed noise 400 to 1500 Hz plus a pad in key **(heuristic)** | none | wide | -18 to -24 dB |
| braam | a trailer scale hit | 30 to 80 ms | long | 1.5 to 4 s | low brass and saws, heavily saturated | none | wide | rare: overused, and it fights the music's bass |

Useful durations by job, from UI sound libraries: click 30 to 120 ms, hover 15 to 45 ms, navigation 80 to 450 ms, success 100 to 300 ms, error 150 to 600 ms. Whoosh length follows the move: quick swipes and fast cuts 0.25 to 0.5 s, cards 0.5 to 1 s, big titles and slow push ins 1 s or more.

What the library shows across all 1126 sounds: **what you hear is short even when the file is long.** Clicks ring to -40 dB over 60 to 200 ms but drop 20 dB in 8 to 26 ms; impacts have a 150 to 450 ms tail but a d20 of 17 to 71 ms. Only bells and chimes keep a d20 above 100 ms. A real object moving through air is a low "whum" with a whistle, not hiss; hiss reads as a designed digital transition. Speed comes from a short length with the peak early, weight from length, a slower attack and width.

### In the kit

These synthesized effects are the **fallback**, not the default: a cue with a `"file"` plays a recording found for the film (`sfx-selection.md`), and the synth plays only where the film's signature needs a designed sound or no search turned up a recording that fits. The job names below still decide how every cue sits on its frame and its base level, recording or not.

`sfx.py` has one effect per job, and the cue's `sound` names the job. Every effect takes a `seed` (same seed, same sound) and most take `size` (0 light to 1 heavy: lower, longer, wider). Measured with `sfx_catalog.py --synth-only --check`, 665 of 686 measures of 152 renders sit inside the library ranges above (measured, not heard).

| Job (cue `sound`) | `sfx.py` | What it is | On its frame |
|---|---|---|---|
| `tap` | `tap()` | a press: 4 to 15 ms of falling noise | starts |
| `click` | `click()` | a press plus a quieter release 45 to 80 ms later | starts |
| `tick` | `tick()` | a data tick, 4 to 9 ms, 3 to 10 kHz | starts |
| `blip` | `blip(key, i, ...)` | a select: tone plus a noise transient, falling 1 to 2 st | starts |
| `pop` | `pop()` | a soft pop, 740 to 990 Hz, rising 3 to 7 st | starts |
| `text` | `text()` | text appearing, falling an octave or more | starts |
| `toggle` | `toggle(key, on, ...)` | a click plus two tones a fourth apart, up for on | starts |
| `card` | `card()` | a card lands: an 80 to 180 ms thud, mostly 120 to 500 Hz | starts |
| `chip` | `chip()` | a light object lands: a struck tone near C6 | starts |
| `land` | `land()` | chip, card or impact by `size` | starts |
| `impact` | `impact()` | a 50 to 70 ms sub body plus a 120 to 500 Hz knock (20 to 30 % of the energy, so it survives phones) | starts |
| `boom` | `boom()` | an impact with a long cinematic sub tail | starts |
| `swish` | `swish()` | 60 to 160 ms of low air plus a whistle | peaks |
| `whoosh` (and `airy`) | `whoosh()` | length follows the move; up to 0.18 s it is a swish, longer a wide low "whum" falling 2 st; `air: true` is the bright designed sweep (5 to 8 kHz, wide) | peaks |
| `transition` | `transition()` | a whoosh into a small landing | peaks |
| `panel_open`, `panel_close` | `panel()` | a sheet opens (rising sweep) or closes | open ends, close starts |
| `success` | `success()` | 4 notes 60 to 80 ms apart, d20 190 to 290 ms | starts |
| `error` | `error()` | low, buzzy, a semitone clash, falling | starts |
| `tier` | `tier()` | a struck hit plus a bell rising per tier | starts |
| `logo` | `logo()` | the hook's notes, then an inharmonic bell, 1.2 to 2.4 s | starts |
| `riser`, `reverse` | `riser()`, `reverse_swell()` | anticipation | ends |
| `sub_drop`, `texture` | `sub_drop()`, `texture()` | the floor dropping; a bed | starts |

Old cue names still work as aliases (`place` and `block` play `chip`, `key` plays `tap`, `chime` and `done` play `success`, `bell` plays `logo`, `hit` and `final` play `impact`, `count` and `grain` play `tick`, and so on); `gap` and `stop` are skipped, because dips replaced them. `sfx.peak_index(x)` finds where a sound peaks, so a whoosh's peak can sit on its frame.

The film's `character` in `music.json` is one of seven: `glass`, `wood`, `metal`, `plastic`, `paper`, `digital`, `soft`. They differ in envelope, noise share, width and pitch movement, not only in frequency. Known misses: `soft` is low passed on purpose (its tick, panel and success sit a little dark), `paper` has no tonal chip (it lands as a light card).

### Which event gets which sound

| Visual event | Sound | Weight |
|---|---|---|
| An element slides or flies in | a whoosh whose length equals the move, peak at the frame of fastest motion or the cut; a small UI move gets nothing | support or none |
| An element lands, snaps, docks | click (small), pop (round), thud plus click (card), impact (hero) | support, hero for the reveal |
| A group staggers in | one sound for the group, or a decaying series (below) | support |
| A hard cut between acts | a whoosh into a hit, or a riser ending on the cut with a dip or a sub after | hero on structural cuts only |
| An ordinary cut inside an act | nothing; the music carries it | none |
| Build up before a reveal | riser or reverse swell, 1 to 4 s at ad tempos, ending on the reveal frame | hero (once per film) |
| A reveal | tonal hit or sting, plus a sub, plus a short shimmer tail | hero |
| Hover, toggle, checkbox, counter step | UI ticks of the 15 to 120 ms class | support or ambient |
| Success, a check | a rising two or three note motif | support |
| Error, a shake | a falling pair or a semitone clash | support |
| Counters and charts | ticks at the counter's rate, pitch rising with the value | ambient |
| Typing | key ticks generated from the letter times, from a pool | ambient |
| The end card | the sonic logo, 1.5 to 4 s, a clear start and end | hero or structural |
| Background motion (particles, a slow drift, parallax) | nothing, or the bed | none |

## 4. How each sound is built

Every recipe reduces to a few shapes: filtered noise with a moving cutoff plus pitch movement (whooshes, risers); a sine with a fast downward pitch envelope plus a noise click (booms, sub drops); transient, body, sub and tail aligned on one sample (impacts); short enveloped tones with a noisy transient (UI sounds). Each layer owns its own band, and only one layer owns the sub.

The kit's `sfx.py` already builds the jobs above this way. These recipes are not how a film gets its clicks, whooshes, paper or impacts: those are found recordings (`sfx-selection.md`). The recipes are for a film's own designed sounds (the signature, a special moment), for a job no search turns up, and for judging any sound, found or made.

**Shared rules for every generated sound.** Linear attack of at least 0.5 to 2 ms (never zero, it clicks), exponential release, a 3 ms fade to exactly zero at the end, DC removed, harmonics kept below about 8 kHz. Exponential pitch glides are built by integrating the frequency (`phase = 2 pi cumsum(f) / SR`), never `sin(2 pi f t)` with a moving f. One shared short reverb for all effects, so everything sits in one room. An exponential decay with time constant tau is 20 dB down after 2.3 tau, so choose **tau = wanted d20 / 2.3** (a 20 ms d20 needs tau 9 ms). Treating the decay constant as the length is what made the kit's first effects ring five to ten times too long. In the kit, `dsp.dec(n, d20_ms)` takes the d20 directly; `dsp.perc()` still takes a time constant. `dsp.glide`, `dsp.pink`, `dsp.modal`, `dsp.repitch` and `dsp.spread` cover pitch tracks, pink noise, modal bodies, repitching and width.

**Impact** (0.5 to 2.5 s), four layers on sample 0:

- Transient: a 3 to 10 ms noise burst high passed at 2 kHz, attack 0.5 ms.
- Body: 120 to 500 Hz, a knock with a d20 of 30 to 50 ms, matched to the material (section 5). This layer is what a phone plays; without it the hit vanishes.
- Sub: a sine at 40 to 60 Hz starting 2 to 4 st high and settling in 20 to 50 ms (up to 20 to 25 st for a punchier, kick like attack), decay 0.3 to 2 s, soft saturation (tanh, drive 2 to 4) so harmonics carry it on small speakers.
- Tail: the shared reverb, 1 to 3 s, high passed at 200 Hz so it does not smear the sub.
- High pass every non sub layer at 100 to 120 Hz. A small timing shift between transient and body changes the perceived size and punch a lot, so align them to the sample. A thin hit usually lacks a layer, not a plugin.
- A card landing is not a hero impact: drop the sub and the tail, keep a short low thud plus a click.

**Whoosh** (length = the move):

- Pink noise, never raw white noise, through a band pass or low pass whose cutoff rises then falls, peaking at 55 to 65 percent of the length **(heuristic)**: about 300 Hz up to 4 to 8 kHz and back to 600 Hz for a light object, 150 Hz to 1.5 kHz for a heavy one **(heuristic)**. A fast sweep sounds sharp and quick, a slow one heavy and grand.
- The level swells into the centre and fades out the back. A small rise in pitch at the peak lifts energy; a falling pitch means leaving or settling. Doppler: up a semitone or two on approach, down as it passes **(heuristic)**.
- For a physical move add a 150 to 500 Hz band and a whistle tone (the library's fast swishes are mostly under 2 kHz with a whistle); for an airy designed move decorrelate the two channels for width.
- Pan along the on screen direction with equal power panning, resolving to centre at the landing.
- Layers by function: an air layer for the broad motion, a texture layer, optionally a tonal layer, and a landing layer only when the object visibly stops.

**Riser** (0.5 to 4 s):

- Noise riser: noise high passed at 100 to 150 Hz (full range noise piles up under 100 Hz and fights the kick at the drop), a band pass or low pass opening on an accelerating curve, level rising as t squared to t cubed. Pitch riser: detuned saws (7 or 8 voices, 10 to 25 cents apart) gliding up an octave. Mixed: noise about 6 dB under the tonal layer.
- Choose **one** primary motion (filter for noise, pitch for tones), not pitch, filter and level all at full strength. Avoid a linear rise; an accelerating one builds more tension. Widen it as it peaks.
- Quick lift 1 to 2 beats; general build one to several bars; big tension into a main drop 4 to 8 bars (in a 30 s film that is rarely more than 4 s).
- It **ends** on its frame: cut it dead, or end it into the dip. The hit lands in the space after it.
- At most one big riser per spot. A riser before every reveal is template grammar.

**Reverse swell** (0.5 to 2 s): make the hit, run it through a 2 to 4 s decaying reverb fully wet, reverse it, trim so its peak lands one frame before the target, then play the dry hit on the target **(heuristic)**.

**Sub drop, boom** (1 to 4 s): a sine starting at 80 to 110 Hz gliding down to 30 to 45 Hz over 0.5 to 2 s, decay 2 to 4 s, phase starting at 0, a 2 to 5 ms noise click on top, tanh saturation, mono. A short envelope (10 to 50 ms) is a punch, a long one (0.5 s and up) is the cinematic drop; a long one inside a kick pattern reads as a "pew".

**UI sounds** (the most portable recipes, built in Python by their authors):

- Click: a noise layer (low passed at 4 kHz, 12 ms, 0.5 ms attack, 4 ms release) plus a body tone gliding 1800 to 1200 Hz over 40 ms.
- Hover: a sine 1400 to 1500 Hz, 50 ms.
- Confirm: a soft square (sine plus 3rd harmonic at 1/3 and 5th at 1/5) at 660 Hz for 70 ms, then 990 Hz (a fifth up) for 160 ms. Cancel: 520 Hz, then 350 gliding to 330 Hz. The same timbre for both, so the interface "answers two ways".
- Text blips: 880 Hz shifted 0, 2, 4 st, each gliding up 2 percent, 45 ms; under 50 ms so fast text does not smear.
- Designed UI tones carry a short noise or click transient on top (noisiness 0.05 to 0.3); real clicks and ticks are mostly noise (0.55 to 1.0). A pure sine tick sounds like a test tone.
- A small, fast pitch movement is most of what makes a UI sound feel physical: library clicks fall 10 to 14 st in 40 ms, selects 1 to 2 st, pops rise 3 to 7 st.
- Ease harsh 3 to 6 kHz content and cut below 200 Hz on taps.

**Tonal hit, sting**: a chord in the score's key (root, fifth, octave, maybe a third or ninth) of bell or mallet tones (FM with a modulator at 1.4 to 3.5 times the carrier and an index decaying from 3 to 8 toward 0), plus a low sine on the root, the impact transient, and the shared reverb **(heuristic)**.

**Sonic logo**: 1.5 to 3 s, a clear beginning and end, the hook's first 3 to 5 notes on the signature instrument, often one note per syllable of the name (YouTube's two notes), and one tactile, physical detail (Netflix's ring on a cabinet, YouTube's door unlock) so it feels made, not generated.

**Glitch, shimmer, data chatter, bed** have no sourced recipes; the vocabulary table gives working starting points, all **(heuristic)**: bit crushed or sample held noise with 10 to 40 ms slices repeated 2 to 8 times for a glitch; 6 to 20 high partials on scale notes with slow random level changes for a shimmer; 10 to 30 ms blips at random scale notes, 10 to 30 per second, high passed at 1 kHz for chatter; low passed pink noise plus a pad in key for a bed.

**Check a designed sound without ears**: `sfx_catalog.py --synth-only --check` renders every kit effect in every character and prints each against the targets; for one designed sound, run `sfx_catalog.py --file sound.wav` and compare attack, d20, total length, centroid, band shares, noisiness, pitch movement and width with the table in section 3. Then look at its waveform and spectrogram the way `sfx/sheets/` shows the library (a vertical bar is a transient, a horizontal line a tone, a haze noise, a diagonal a sweep).

### Samples from the library

Recorded effects come first (section 4b), and the first of those are the ones found for this film and placed with a cue's `"file"` (`sfx-selection.md`). The `samples` block below is the quick route for jobs the film did not search for: it picks from the local CC0 library automatically. The kit's code still has samples off by default, so a film that wants it turns it on (`rights.md`) in `music.json`:

```json
"samples": {"enabled": true, "jobs": ["card", "logo"], "layer": ["impact"]}
```

A sensible start is `"jobs": "all"` with `"layer": ["impact", "boom"]`. `jobs` (a list, or `"all"`) are played from a sample instead of the synth; `layer` puts a sample under the synth at -6 dB. `samples.py` picks each job's family (the picks of `sfx/ANALYSIS.md` section 3, else the 3 nearest files by features in the job's category, never clipped, lead silence under 150 ms), copies the files into the film as `public/sfx/<pack>__<path>`, trims their lead silence, and writes `public/sfx/ASSETS.txt` (file, pack, source page, CC0 1.0). The film reads them from there, with the same variation as synthesized sounds. `python audio/samples.py` lists every job's family. A family is only 2 or 3 files from one pack, so `samples.py` alone cannot give a repeated role the pool of 5 to 8 recordings from two sources it needs (`sfx-selection.md`, section 8). The library is thin on pops (19), whooshes (30) and real risers (26); find those per film from `sfx-sources.md` (Freesound CC0, Sound Digitator, SoundResponse, Mixkit, 99Sounds), and synthesize only when nothing fits.

### Ideas from earlier films (designs, never reuse as they were)

The earlier films' designed effects are in `templates/examples/*/audio/`. Their mapping from event to sound is still a good idea list: a slider whose detent ticks rise one octave over the range; a chart line with a rising zip as it draws; ticks rising per count; a leaderboard swap as a short whoosh plus an upward pop; a tier upgrade as a metal hit plus a bell rising with the tier; a scan beam as noise sweeping down from 6.5 kHz to 900 Hz because the beam goes down; detected items as bells whose pitch follows row and column; typing indicator dots as three soft ticks 130 ms apart. The sounds themselves are taken: Torq and Sendoku shared 42 percent of their strong transients.

## 4b. Realism: recordings first, synthesis as the fallback

The Enogon film (mgpro 2.0.0) passed every check in section 12, and the user still heard its music and effects as AI made: the same sounds as earlier mgpro films around 12 to 13 s (the kit's synthesized whoosh and reverse swell), and a drum hit on the roof landing at 20 s (a synthesized impact under a synthesized taiko) that "sounded AI-like". Measured distinctness is not realism. The research behind this section is in `research/ad-music-and-logo/` (`notes/ai_tells_and_realism.md`, `notes/sample_libraries_and_tools.md`).

**What the ear flags is sameness, not imperfection.** Listeners pick AI songs from human ones at chance on random pairs (53 percent) and reach only 66 percent on closely matched pairs; their reasons include "Something about Track 1 sounded too perfect, too contrived to be Human" and "Track 2 immediately seemed more human cause it made better use of stereo sound" ([Echoes of Humanity, arXiv 2509.25601](https://arxiv.org/html/2509.25601)). A 2026 classroom test of 3,210 responses found 48.16 percent, chance ([Zenodo](https://zenodo.org/records/22278782)). MIDI mockups give themselves away by the "machine gun" (the identical recording on every trigger, [SampleStack](https://samplestack.app/news/round-robin-explained/)), dynamics drawn as straight ramps and one reverb on every track ([Composer Workflow](https://agents.composerworkflow.com/academy/humanizing-a-mockup/); [modwheel.net](https://modwheel.net/guides/reverb-for-cinematic-mixing)). An instrumental score has no vocal tells, so its realism rests on three layers: the instrument, the performance and the space.

**The order, for every sound and every part:**

1. A recording: a CC0 instrument through the sampler; an effect found for this film from a cleared free source (`sfx-selection.md`, `sfx-sources.md`), the skill's CC0 library (`sfx/`) included.
2. A recording transformed: pitched to the key, filtered, reversed, layered, stretched to the move.
3. Synthesis, only as the fallback for a job no search for this film could fill, or for the film's own signature sound. Then it follows the synthesis rules below.

### Effects: recorded beats synthesized, now measured

In a 2026 study, 18 audio professionals rated scenes built from library samples above scenes using procedural sounds, by **13.8 percent (live action) to 34.8 percent (a cartoon everyday scene)**. Synthetic sounds were believable for sci-fi (lasers, rockets, air) and least believable for everyday actions. Classifiers separated the two groups at 90 to 95 percent from temporal centroid, spectral flatness, high frequency content, log attack time and effective duration, and the professionals asked for more low end on impacts, a stronger first hit, more layering and more reverb ([arXiv 2605.31082](https://arxiv.org/html/2605.31082)). A footstep model that matched the spectrum still lacked "temporal sharpness" until a transient was synthesized on purpose ([arXiv 2412.18710](https://arxiv.org/pdf/2412.18710)).

- **Physical events are recordings**: a card landing, paper, a box closing, a door, a hand on wood, a drum, a stamp. A hero impact is a recorded hit (a real knock, a real drum) with the kit's sub only as a layer under it.
- **UI clicks and taps are recordings too**: a real mouse or trackpad (Freesound CC0), Kenney's designed clicks and switches, not the kit's synthesized `click` (`sfx-selection.md`, section 10).
- **Synthesis stays for** digital blips, sci-fi glows, a data chatter no library has, and the film's signature, and then it has a sharp transient of a few ms, a body with a downward pitch envelope, a tail into the shared room and variation per instance **(heuristic, from the study's features)**. Layer transient, body and tail with aligned attacks ([Pixflow](https://pixflow.net/blog/sound-effects-layering/)).
- **Sources**: every free source, what it is good for, how to download it and its licence clause are in `sfx-sources.md` (31 October 2026); the summary that was here: the skill's CC0 library (`sfx/`, thin on pops, whooshes and real risers); the Sonniss GDC bundles, royalty free, "no attribution", explicitly covering "advertisements, trailers", forbidding redistribution as sound effects and AI training ([Sonniss licence](https://sonniss.com/gdc-bundle-license/)), tens of GB a year (2024 counted as 23.5 GB in nine parts here and 27.5+ GB by GameFromScratch; 2026 is 7.47 GB), so take one part at a time and keep only whooshes, impacts, foley, paper, wood and mechanical sounds; Freesound's CC0 subset through `filter=license:"Creative Commons 0"` (originals need OAuth2, previews are lossy, [Freesound API](https://freesound.org/docs/api/resources_apiv2.html)). Record each file's source URL, licence and download date.
- **Across films**: the same synth recipe in every film is a family sound even with a new seed, and the shared transient check (r above 0.9) does not catch a family resemblance. No hero or support job may use the same source (the same synth recipe and character, or the same sample family) as the last film. Write each job's source in the sound plan of `SCRIPT.md` and in the film's registry entry (`"effects": {"whoosh": "sample: <pack>/<file>", ...}`), so the next film can avoid it.

### Instruments: the sampler path

The kit plays the score's parts with recorded instruments when `music.json` says `"instruments": "samples"` (the code's default is still `"synth"`). Use it for every film; the synth remains only for kinds the sampler map does not cover. What it does (`templates/kit/audio/sampler.py`, `sampler_map.json`, `fetch_instruments.sh`, documented in `SAMPLER.txt`):

- `fetch_instruments.sh` downloads the CC0 instruments once (default `/games/mgpro/instruments`, or `$MGPRO_INSTRUMENTS`), pinned to commits, about 1.3 GB as FLAC, with licence evidence per source in `SOURCES.txt`, plus the Voxengo room impulses. It stops if `/` has under 3 GB or the destination disk under 8 GB free, and can be run again.
- `sampler.py` is a small SFZ player in numpy: velocity layers, round robins drawn from a bag per key and layer that never plays the same take twice in a row, release samples, a sustain pedal, choke groups, loops for long notes, and a convolution room (Voxengo's Nice Drum Room, French 18th Century Salon or Musikvereinsaal when installed, a generated room otherwise).
- `score.py` sends every part the map covers to the sampler (pianos including a soft una corda Osiris piano, mallets, harp, guitar, string sections with spiccato and pizzicato, solo cello, flute, horn, upright and electric bass, timpani, a Virtuosity drum kit with up to 26 velocity layers and 4 round robins, hand percussion, body percussion) and falls back to the synth for anything not covered (808s, saw pads, synth leads) or when the library is missing (it prints that). With samples the kick pump is lighter (`"pump"` 0.12 against 0.4), because players do not duck. `python audio/sampler.py --list` shows which kinds are installed, `--demo keys:felt` renders a phrase, and `demo.py <genre> --samples` sketches a genre with them.
- Its limits, measured by its author: the sampled piano, marimba and strings have one take per velocity layer, so repeated notes at one velocity are identical and their variety must come from the velocity spread choosing other layers; the drum kit has 4 round robins, under the 6 to 8 below. Write velocity contours for those parts, and alternate two instruments on fast repeats. Filters, LFOs and pitch envelopes inside SFZ files are not modelled. The full API and the measured demo films are in `templates/kit/audio/SAMPLER.txt`.

Which libraries, and which not (licences checked 29 October 2026, `notes/sample_libraries_and_tools.md`):

| Role | Library | Licence | Note |
|---|---|---|---|
| strings, pizzicato, winds, brass, mallets | VSCO 2 CE ([GitHub](https://github.com/sgossner/VSCO-2-CE)) | CC0 | good for shorts and pizzicato, thinner for long legato |
| a wider set | VCSL ([GitHub](https://github.com/sgossner/VCSL)) | CC0, "no royalties, no credit" | mostly one round robin and two to three velocity layers, more for percussion |
| piano | Osiris Piano ([sfzinstruments](https://github.com/sfzinstruments)); Upright Piano KW ([FreePats](https://freepats.zenvoid.org/Piano/acoustic-grand-piano.html)) | CC0 | the upright has two velocity layers |
| drums | Virtuosity Drums, Big Rusty Drums ([sfzinstruments](https://github.com/sfzinstruments)) | CC0 | |
| guitar, bass, cello | Karoryfer guitars and basses, Sneakybass, Bigcat Cello | CC0 | single notes, so picked lines beat strums |
| mallets, bells, crotales | University of Iowa MIS ([Iowa](https://theremin.music.uiowa.edu/mis.html)) | "without restrictions" | no ready SFZ mapping |
| room | Voxengo IMreverbs ([Voxengo](https://www.voxengo.com/impulses/)) | royalty free for any purpose, commercial included | 38 impulses, 6.9 MB |
| **not for ads** | Sonatina Symphonic Orchestra | CC Sampling Plus 1.0: "All advertising and promotional uses are excluded" ([CC legal code](https://creativecommons.org/licenses/sampling+/1.0/legalcode)) | Virtual Playing Orchestra embeds Sonatina samples, so it inherits this |
| **not here** | Spitfire LABS | now inside Splice INSTRUMENT behind an account ([Splice](https://splice.com/instrument/labs-instrument)) | no headless Linux route |
| credit needed | Salamander Grand Piano V3, Naked Drums | CC BY | legal, but a credit in a 30 s ad is awkward; prefer the CC0 set |

No CC0 felt piano was found; felt piano is the one popular ad timbre without a clean free source (the sampler's `felt` kind is the Osiris piano played una corda, the nearest stand in). Sample quality caps everything: a great performance on a mediocre sample still sounds mediocre ([Taxi forum](https://forums.taxi.com/post329840.html)).

### Performance: variation with a cause

- **Round robins, 6 to 8** on any note repeated faster than about 4 per second. At 150 BPM 16ths, four round robins cycle back every 0.4 s, inside the window where the ear hears repetition; 6 to 8 push the return past 1 s. Resetting the cycle at every loop recreates the machine gun ([modwheel.net](https://modwheel.net/guides/why-your-ostinatos-sound-like-a-machine-gun)). Staccatos "desperately need" round robins; for piano, velocity layers matter more ([VI-Control](https://vi-control.net/community/threads/are-round-robins-a-real-advantage-in-a-multi-velocity-layers-piano-library.64111/)). With too few alternates, alternate bars between two instruments about 1.5 dB apart through the one shared room (modwheel.net, same guide).
- **Velocity that changes the tone.** Play velocity 40 and 110: if only the loudness changes, velocity adds no variety (modwheel.net). In a synth fallback, tie the filter cutoff and the number of harmonics to velocity **(heuristic)**.
- **Velocity in a shape, not jitter**: a spread of at least 20 points that drifts up over four bars and back down; note lengths varied 10 to 20 percent in a shape (shorter through a crescendo, longer as it settles) (modwheel.net).
- **Timing is systematic, not random.** Real players deviate 5 to 50 ms from the grid ([ANU](https://openresearch-repository.anu.edu.au/bitstreams/dfcc9a33-70c6-4653-a5e7-1dcc82cb30fe/download)), but in a structured way: in "Funky Drummer" the deviations shrink from 56 ms to 4 ms across a fill, and drummers repeat their pattern within a few ms bar to bar ([ZGMTH](https://www.gmth.de/zeitschrift/artikel/1224.aspx)). Listeners rate perfectly quantized versions as grooving as well as or better than large random deviations ([Frühauf et al.](https://www.researchgate.net/publication/237423294_Music_on_the_timing_grid_The_influence_of_microtiming_on_the_perceived_groove_quality_of_a_simple_drum_pattern_performance); [Senn et al.](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5050221/)); experts detect swing displacement only at 8 to 14 ms, non drummers at 18 to 31 ms ([Frontiers](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2017.01709/full)). So: a tight pulse; a per bar accent and timing template that repeats; arrival notes at a phrase peak 5 to 15 ms early and notes approaching a cadence 5 to 15 ms late; ostinatos, arpeggios and trailer percussion left locked ([Composer Workflow](https://agents.composerworkflow.com/academy/humanizing-a-mockup/)). A random 3 to 6 ms offset is below the swing threshold; it only breaks sample identity. `music.md`, Humanising the score, says how this maps onto the kit.
- **Sustained lines** get a continuous dynamic curve: bow change dips of 1 to 3 dB where a bow would run out (under 1 dB is inaudible, too many sound like "constantly catching its breath"), pulling back at dissonance and pushing into resolutions, never a straight ramp (Composer Workflow). Vibrato starts late, at about 5 to 7 Hz (four top violin soloists averaged 6.63 Hz and 63 cents, [Illinois](https://experts.illinois.edu/en/publications/a-pilot-study-of-relationships-between-pitch-register-and-dynamic/); a typical extent near 30 cents within 10 to 60, [BYU](https://physics.byu.edu/docs/publication/1499)), with a depth that wanders.
- **Playable parts**: no more than ten simultaneous piano notes, guitar inside the fretboard, wind lines with breaths; MuseBench lists the opposite as measurable AI tells ([arXiv 2610.20310](https://arxiv.org/html/2610.20310)).
- **Synth fallback**: a few cents of detune and slightly different envelope times per note, a noise component in the attack (breath, bow, pick), a release that keeps ringing after note off **(heuristic)**. Synth brass needs a burst of air with a changing harmonic mix and velocity dependent brightness ([Sound On Sound](https://www.soundonsound.com/techniques/synthesizing-brass-instruments)); a constant triangle LFO on strings "sounds unnaturally regular" until random modulation is added ([Sound On Sound](https://www.soundonsound.com/techniques/synthesizing-strings-string-machines)).

### Space: one shared room, depth by pre-delay

A dry or uniformly reverbed mix reads as a game or a demo, because front to back depth is mostly early reflections and high frequency roll off ([modwheel.net](https://modwheel.net/guides/reverb-for-cinematic-mixing)).

- **One convolution room, two or three send depths** (close, mid, far), impulses trimmed to their early reflections, plus one shared tail with 40 to 80 ms of pre-delay ([VI-Control](https://vi-control.net/community/threads/what-are-your-techniques-for-early-reflections-on-dry-orchestral-libraries.82511/); [Gearspace](https://gearspace.com/board/music-computers/565702-reverb-settings-orchestral-sample-libraries-share-your-set-ups.html)). Back instruments get darker, later reflections.
- **Pre-delay is distance**: about 30 to 40 ms pulls a source forward, 0 to 8 ms pushes it back ([modwheel.net](https://modwheel.net/guides/basics-of-mixing-cinematic-music)). A quieter horn that stays as dry as the flute reads as a soft instrument at the front, not a distant one.
- **Reduce each library's own room** when combining libraries, so the shared room defines the space (modwheel.net, the ostinato guide).
- **Effects go into the same room**: a lone effect without a tail feels flat and spaceless (Pixflow), and the professionals in the 2026 study asked for more reverb. Not one reverb per bus: the Bauwerk score gave each bus its own algorithmic reverb with a different room size, the "one reverb per track" pattern, so there was no shared room and no depth inside it.
- Use the stereo field on purpose (the "better use of stereo sound" quote above); width per film stays inside section 12's side share.

## 5. Matching material, size and key

**Size sets pitch, speed and length.** Bigger objects get lower, slower, longer sounds with more low end and more room. A working mapping **(heuristic)**: a size factor s from 0 (a chip, a small label) to 1 (a hero card, full screen type); body pitch from about 1200 Hz down to 150 Hz, length from about 60 ms up to 600 ms, both on an exponential scale; no sub under s = 0.4, a full sub at s = 1; reverb send rising with s. Big type gets a lower, longer, wider sound; small type a short, bright, mono tick.

**Material sets the spectrum and the decay** of the body layer. A modal body is a sum of decaying sines; the values below are standard acoustics, not sourced to a motion graphics practitioner **(heuristic)**:

| Material | Body | Ring |
|---|---|---|
| glass | few, sparse, inharmonic partials, about 1 to 6 kHz, very bright | long, tau 0.3 to 1.5 s |
| metal | many inharmonic partials (free bar ratios about 1, 2.76, 5.40, 8.93), slight beating | very long, 1 to 4 s |
| ceramic | like glass, lower | shorter, tau 0.1 to 0.4 s |
| wood | low to mid partials, 200 to 1200 Hz, upper partials dying first | short, tau 20 to 80 ms (library wood: d20 10 to 20 ms) |
| plastic | mid partials with a noise click, duller than wood | tau 15 to 50 ms |
| paper | no modes: high passed noise 2 to 10 kHz with fast irregular crackle | 50 to 300 ms |
| cloth | low passed noise (1 to 3 kHz), soft 10 to 30 ms attack | smooth |

The kit's seven characters (glass, wood, metal, plastic, paper, digital, soft) differ in envelope, noise share, width and pitch movement, not only in frequency; a cue's `material` overrides the film's character for one event. When the first kit's five characters were measured, every click had the same 26 ms d20 and 380 Hz body whatever its material.

**The product's world beats a library.** The most distinctive films take their palette from the product: its own UI sounds, the materials it is made of, its existing sonic logo. Apple built an event opener from 45 years of its own device sounds; Brabantia built its sonic brand from recordings of its products. A transition can be the product's own sound stretched, filtered or reversed instead of a generic whoosh. This also fixes the "spaghetti crunch" failure of AI video, where a sound comes from a statistical default instead of from the object.

**Pitch follows the score.** Every tonal effect (pops with pitch, confirms, chimes, data blips, tonal hits) takes its notes from the score's key, usually its pentatonic, so any two effects form a consonant interval. Root and fifth for hits and stings; the root an octave or two below for sub drops. Rising intervals (a fifth, an octave) for reveals and success, falling ones for exits, a semitone clash only for errors ("the clash is the message"). Whooshes, ticks, taps, paper and cloth stay unpitched noise so they cannot clash. If the product has its own UI sounds, write the score in their key.

## 6. Sync to the frame

At 30 fps one frame is 33.3 ms; at 60 fps it is 16.7 ms. Think in milliseconds and convert per frame rate.

**Tolerances** (positive means the sound arrives before the picture):

| Standard | Audio early | Audio late | At 30 fps | At 60 fps |
|---|---|---|---|---|
| ITU-R BT.1359, detectable | +45 ms | -125 ms | +1.35 / -3.75 frames | +2.7 / -7.5 frames |
| ITU-R BT.1359, acceptable | +90 ms | -185 ms | +2.7 / -5.6 frames | +5.4 / -11.1 frames |
| EBU R37, end to end | +40 ms | -60 ms | +1.2 / -1.8 frames | +2.4 / -3.6 frames |
| Netflix delivery QC | 1 frame or less is minor; 2 or more frames is a fix | | | |

Early is noticed sooner than late, because early never happens in nature. So hard sync sits from 0 to 1 frame early, and only sounds whose job is anticipation start long before their frame.

| Sound | What lands on the frame | 30 fps | 60 fps |
|---|---|---|---|
| impact, tap, click, logo hit, stamp | the transient on the contact frame (the frame the object stops or touches) | on the frame, at most 1 frame early | on the frame, at most 2 frames early |
| same, if it feels late | the visual peak often comes 1 to 2 frames after contact, or the sound has a slow attack: move it earlier one frame at a time, or trim its lead in | | |
| whoosh | its loudest point on the first frame of the new shot, or on the frame of fastest motion | starts 6 to 15 frames before; a 0.5 s move gets a 400 to 500 ms whoosh (12 to 15 frames) | starts 12 to 30 frames before; 24 to 30 frames long for a 0.5 s move |
| riser, reverse swell, panel opening | its END on the cut or on the start of the dip before the hit | 15 to 60 frames long (0.5 to 2 s) for a quick one | 30 to 120 frames |
| sub drop | its start on the hit frame | on the frame | on the frame |
| re-entry after a dip | the first onset after the dip | 0 to 7 frames after (median about 1) | 1 to 15 frames after (median 2 to 3) |
| a sound that follows picture (blips as fields fill, a tick per data point) | the frame the element changes state, not the nearest 16th | | |

`score.py` places each job this way from its cue frame: `riser`, `reverse` and `panel_open` end on it, `swish`, `whoosh` and `transition` peak on it, everything else starts on it. Picture synced hits stay frame exact; only `loose` cues (ambient cues, textures) get a small, late leaning start offset.

- A whoosh placed wholly after its cut always feels late. A whoosh slightly before a change builds anticipation; one exactly on the cut reads as clarity.
- Professional films, averaged per film, put the sound's peak a median 12 ms after the cut (10th to 90th percentile: 58 ms before to 70 ms after). The measurement lags the real attack by about 12 ms, so in practice the pros land on the cut, with whooshes and risers leading by 2 to 4 frames and impacts on it or 1 to 2 frames after.
- **J and L cuts.** Let the next scene's first sound, ambience or music change enter a few frames before the picture changes (J cut, it pulls the viewer forward); let a hit's tail or the last scene's pad ring through the new scene (L cut, it keeps the cut from feeling chopped).
- Trim the lead silence of every sample before placing it (`lead_ms`). A file that starts 50 ms in lands 3 frames late at 60 fps.
- **Only structural cuts sit on a bar downbeat.** The kit measured that cuts on bar downbeats rise 3 to 9 times over the baseline from the music alone, with no effect at all, because the downbeat is where the kick, the bass and the chord change land. Professional cuts are barely more aligned with musical hits than chance (72 against 64 percent). So keep downbeat cuts for structure (act changes, the reveal, the end card) and let ordinary cuts fall with the action, between the downbeats. `fingerprint.py` prints what this music's bar downbeats measure with no cut, next to the hero and ordinary cuts.
- **Cut on accents, sometimes.** A featured note, a hit, a change of phrase or harmony, a pause or the return of the rhythm can support a cut, a reveal or the end of a move. It is an occasional, meaningful device, not a rule to cut on every beat. Meaning, reading time, a voice and a silent brief all matter more than hitting the beat; when a match does not work, adjust the shot length, path or arrangement gently, never with an unnatural speed.
- **The accent map.** The grid and the start of a sound file are not where the perceived peak is. Once the mix exists, measure the onset of every cue that is meant to sync (librosa onset detection on the rendered `film.wav`, or `filmstats.analyze`) and compare it with the cue frame: within 1 frame at 30 fps, 2 at 60. Record the cue, the measured onset and the target frame. Recheck after any retime, speed ramp or track change, and again after muxing (the offset of the audio stream in the final file). Matching numbers are a measurement, not proof that it feels in sync; say so.

## 7. Hierarchy and density

**Rank the events before placing a single sound.**

| Weight | How many | What it gets |
|---|---|---|
| `hero` | 1 to 3 in a 30 s film, up to 4 or 5 in 60 s (the kit reports more than one per 8 s): the reveal, the drop, the title slam, the end card | the full layered sound (transient, body, sub, tail), the loudest moment, the music making room; gain 1.0 |
| `support` with `"story": true` | the 2 to 5 actions the story turns on: the click that opens the next scene, the press that exports | a found recording peaking 6 to 9 dB **over** the bed, never skipped, never demoted on a cut; gain 0.4 times the cue's `gain`, set by measurement (`sfx-selection.md`, sections 10 and 11) |
| `support` | the events that carry meaning: a card landing, a check, a counter reaching its value, a secondary click | small, short sounds from the vocabulary, 8 to 14 dB under the music (secondary clicks 4 to 8 dB under the story clicks); gain 0.4 |
| `ambient` | runs and repeats: typing, ticks, data points, grains | very quiet, generated from the picture's formula, varied; gain 0.16, and about a third of ambient cues play nothing |
| none (no cue) | background motion, secondary elements, most ordinary cuts | nothing; the music or the bed carries them |

- The professional cut, averaged over 2,666 cuts in 116 films, raises onset strength to only **1.18 times** its baseline (per film median 1.7 times, 90th percentile 3.9). The first three mgpro films raised it **18.6 times**: every cut slammed. Hit the structural cuts (title, product reveal, end card); let the music or a continuous texture carry the others. In a video that cuts every 4 to 5 s, a sound on every join turns the mix into a percussion track. In the kit, a `support` cue with a hard attack on a cue marked `cut: true` drops to ambient by itself, and automatic dips stay off cuts.
- **A stagger of N items** gets one sound for the group (one swish the length of the stagger), or a decaying series: each hit 1 to 3 dB quieter than the last, pitched up the scale, with small timing offsets so the hits are not on a perfect grid **(heuristic)**. Never N identical pops.
- **The second time something happens, it gets less sound.** The first typed line gets key ticks; the second gets two ticks or none.
- **Even out the hits.** The first films had a few giant hits on a smooth pad and sub (onset strength variation 0.58 to 0.72, against a professional 0.39 to 0.58). More mid level texture (ticks, foley like clicks, grains, small blips) and fewer isolated giants bring the percussive share up toward 0.2 to 0.5 (professional median 0.29; the first films 0.14 to 0.19). The kit adds a quiet bed of off grid percussive grains between the hits (`bed`, default 0.5, beatless 1.5; `bed_rate` 7 grains per second at energy 0.5, beatless 10).
- **Density with contrast.** Professional films average 4.0 onsets per second (10th to 90th percentile 2.1 to 5.6). Within a film the busiest 2 s carry 2 to 9 times the onsets of the quietest (median 2.2 times), with sparse passages near 1 per second and bursts of 6 to 9 per second (the busiest 2 s window: median 7.0 per second). Put the burst where the story needs it, not on a fixed section map. As a ceiling, one accented effect per 1 to 2 s of a busy section **(heuristic)**.
- Restraint is the craft: three even, low impacts can carry the weight of a braam while reading as controlled. Remove any layer or sound that adds nothing.

## 8. Variation and humanization

Identical sounds repeated read as a machine gun, and the ear learns them and stops hearing them. Within a film the first three films did not repeat themselves more than professionals do; across films they did (section 12). Vary both.

**Within a film.** `vary.py` does this for every effect: `Vary(film_seed, pool=4)` builds a pool of takes per effect, each its own synthesis seed derived from the film's seed (so two films never share a transient), served from a shuffled bag with no immediate repeat, then pitch jitter like a sampler, level within 1.5 dB either way, and a small late leaning start offset only for loose sounds. Pool size is `pool` in `music.json` (default 4). Its pitch jitter in cents (`CENTS`): tonal 12, bell 6, impact 60, noisy 120, whoosh 150, sample 100. `python vary.py` runs its self test. The ranges behind it **(heuristic, bracketed by game audio practice)**:

- A pool of 3 to 6 variants per sound type, played in shuffle with the last 1 or 2 excluded (Unity's "Shuffle" and "Avoid Repeating Last"). Kenney ships most sounds in numbered sets of 3 to 5.
- Pitch jitter per use: noisy sounds (whooshes, ticks, paper) about 100 to 200 cents either way; tonal sounds tuned to the key stay small (the kit uses 12 cents, bells 6), or move by scale degrees. Game footsteps use a pitch factor of 0.85 to 1.15 (about 280 cents), which is too wide for anything tonal.
- Level jitter 1 to 3 dB either way (the kit: 1.5); a start offset of a few ms, only on loose sounds.
- Timbre variation (filter cutoff, a swapped layer, per band pitch) hides repetition better than pitch alone; whole sound pitch shifting helps less than expected.
- With samples: the same bag and jitter (100 cents), plus 2 or 3 files of a family. With found recordings (a cue's `"file"`), the jitter varies one file, which is not a pool: rotate 5 to 8 different recordings from at least two sources across a repeated role's cues in `cues.py`, never the same file twice in a row (`sfx-selection.md`, section 8). The first Enogon film played one slide sound on every slide, and the user heard it.

**Sync points stay exact.** Never jitter a sound that is synced to picture; humanise the music, the ambient layers and the choice of sample.

**Timing.** Professional onsets sit a median 0.105 of a 16th note off the tracked grid (about 13 ms at 120 BPM), and 78 percent land within 25 ms of a 16th. The first films sat at 0.047 to 0.093, with 91 to 100 percent on the grid. Most of the professional spread comes from sound design that follows the picture rather than the bar, not from sloppy drums. So:

- Keep downbeats and structural hits exact.
- Let 20 to 40 percent of onsets fall off the 16th grid by placing effects where the picture says (a field fills, a card settles), not snapped to the nearest 16th.
- In the music, vary velocity first (downbeats a little higher, offbeats lower, hats the most variation, kick and snare only slightly) and timing second, as a systematic template, not random jitter (section 4b, Performance). Listeners rated shifts of 15 to 25 ms lower than quantised, and early shifts worse than late ones of the same size, so keep the pulse tight and the median offset small. Details in `music.md`.

**Across films.** Never reuse a transient across films: fewer than 10 percent of a new film's strong onsets may correlate above 0.9 with any earlier film's (professional median 5 percent; Torq and Sendoku shared 42). That check misses a family resemblance: the same synth recipe with a new seed still sounds like the last film (the Enogon review heard it). Take hero and support sounds from a different source than the last film (section 4b), and when samples are used, pick different files from the last film and transform them.

## 9. Contrast is arranged, never a gain hole

**Corrected after the Enogon review (Oct 2026).** This section used to say "dips, not dead air: the sound drops 20 dB or more for 0.15 to 1 s", and the kit's automatic dips did exactly that: about once every 7 s the whole mix was multiplied down 24 dB for about 0.3 s, after the reverbs, so every tail was cut with the notes. The user heard moments where the sound dropped and they "barely heard anything". The numbers below were right as measurements and wrong as instructions. They describe the **result of arrangement** in finished professional films (everything stops on a cadence while a tail rings, then the full band re-enters on a cut). They are not instructions to automate gain. Output metrics are for checking a render, never the instruction that generates one ([report](../research/ad-music-and-logo/report.md), Contrast must be arranged).

### Why a gain dip sounds like a fault

- The just noticeable level change is about 1 dB under good conditions ([HyperPhysics](https://hyperphysics.gsu.edu/hbase/Sound/db.html)); most listeners need about 3 dB ([Digital Sound and Music](https://digitalsoundandmusic.com/chapters/ch4/4-2)); 10 dB sounds about half as loud ([Sengpielaudio](https://www.sengpielaudio.com/calculator-loudness.htm)). So a level change under about 3 dB buys no contrast at all, and a 6 to 10 dB drop is clearly heard and needs a reason the ear can find: a cadence, a picture event, an arrangement change. A drop with no musical cause reads as a broken mix.
- Gaps of only 4 to 5 ms are audible in continuous sound, and detection gets up to ten times worse when the sounds on either side differ in spectrum ([Phillips et al. 1997](https://www.ncbi.nlm.nih.gov/pubmed/9193057)). That is why professionals keep a bed: a pad, room tone or a reverb tail under the breath fills the spectrum, so the ear hears a change of texture, not a hole.
- Parts should leave "without it sounding like they were suddenly muted" ([Arends notes](https://publish.obsidian.md/arends-digital-garden/Notes/20+Shareable/22+Music+Production+%F0%9F%94%88/22.03+Recording+Tips/How+to+create+transitions+in+your+arrangements)); in spoken audio about one second of silence already feels like an uncomfortable gap ([Radio Today](https://radiotoday.com.au/silence-is-golden-why-shutting-up-makes-people-listen/), practice, not research). No study was found on when audiences read a level dip as intended.

### The rules

- **No gain automation for contrast.** Never pull the music bus or the whole mix down to make a breath. The only level moves are small (under about 3 dB, and those buy nothing, so they are rarely worth doing), the music ducking 2 to 6 dB under a hero hit (section 11), and a genre's own kick pump.
- **Make contrast with the arrangement**: drums and bass stop, the pad or a held chord stays; a low pass closes on the pads; the bass high passes for a bar; the texture drops to one instrument; half time; a riser stops dead and its reverb tail rings into the hit. Every breath keeps a bed or a tail under it.
- **An intended breath has three signs** **(heuristic, synthesized from the sources above)**: it lands on the grid right after a cadence or a hit; it keeps a tail or a bed; it resolves into something bigger within one beat to one bar (0.5 to 2 s at 120 BPM). A mistake has none of these.
- **True silence** only as a short gap of about 100 to 300 ms immediately before a hit, where the hit arrives before the ear can wonder **(heuristic: inferred from the one beat gap advice of [FaderPro](https://blog.faderpro.com/creativity/silence-in-music-production/), not a measured threshold)**; at most once or twice per film. A held silent frame after a riser can read bigger than any hit ([add.app](https://add.app/sound-effects/sound-design-for-trailers-hits-rises-drones-pulses/)), but never a second of nothing.
- **The picture never waits for a breath.** The Enogon roof hovered over the walls for about 1.1 s to sit under the dip; the user saw a pause in the fall. The breath fits the action, not the other way round (`craft.md`, Pacing).
- **Do not duck before every hit.** The first films pulled the level to half in the 150 ms before each cut. A thinning before the one main re-entry is enough.

### What professional films measure (results, for checking)

What 129 professional films measure, as results of their arrangement:

- A **dip** (the level 20 dB or more under the film's loud level for 150 ms or longer): a median of 4 per film, 0.78 per 10 s (90th percentile 3.5). 83 percent of films have at least one.
- A **re-entry dip** (the sound comes back at least 6 dB louder than before it): 57 percent of films. It lasts a median 0.30 s (10th to 90th percentile 0.15 to 0.95 s), the sound comes back a median **+9.3 dB** louder (6.5 to 15.7), and the first onset lands a median **41 ms** after the dip ends (11 to 240 ms), not always on the beat.
- **True near silence** (40 dB down, 100 ms or longer): 71 percent of professional films have none.
- **Where dips sit**: they cluster in the first 10 percent (opening breaths, about one per film per 5 percent slice) and again at 90 to 95 percent (before the end card), and are spread evenly between.

What the first three mgpro films did: one gap each, at exactly 13.75 s (45.8 percent) in all three, a dead silence after a loud build, so the sound came back only 3.6 to 6 dB louder, with the first onset 13 ms after, exactly on the grid.

How to read this for a new film:

- **The breath before the hero cut is short: about an eighth of a bar** (about 0.28 s at 105 BPM, 0.27 s at 112.5), made by stopping parts, not by pulling the level. The kit measured a 0.57 s gap making the hero cut read 27 times its baseline; a long gap turns the return into a slam.
- **The return is bigger because the arrangement is bigger**: the full band, the hit and a wider register come back together, the first hit 20 to 70 ms after the breath (professional range 10 to 250 ms). For the jump to be large, the passage before must be thinner than the passage after (fewer parts, hats closed, a filter on the pads), never a fader slid down.
- **Where breaths go**: an opening breath in the first 10 percent, one before the end card at 90 to 95 percent, the main one wherever this story's reveal is, never at the same percentage of the length as any film in the registry.
- **Do not chase the dip count.** A film whose breaths are arranged over a bed may measure only 0 or 1 dips by the 20 dB definition; that is inside the professional range (10th percentile 0 per 10 s). `fingerprint.py` prints dips without failing on them.
- The return can be a burst of hits or a swell. Tendril's Microsoft emoji film drops 1.3 s at 62 percent and returns 14 dB louder with density jumping from 1.0 to 6.8 onsets per second; Samsung's One UI 5 film returns from a 0.15 s dip 31 dB louder on a sustained chord, with no new onset for 1.6 s. Both are arrangement: the parts stop and come back.

**In the kit.** The intended behaviour of `score.py`: `"dips"` defaults to `0` (no automatic dips), and a `["dip"]` section is an arranged breath (drums, bass and rhythmic parts stop, sustained parts and reverb tails keep ringing, the overall level moves less than about 3 dB). Until `score.py` behaves that way (read the `dips` lines of its header docstring and `plan_dips`; the 2.0.0 code defaults to `"auto"` at -24 dB applied to the whole mix after the reverbs), so **every film sets `"dips": 0` in `music.json`** and writes its breaths as form sections with thin `parts` (for example `["pad"]` or `["chords", "pad"]` for an eighth of a bar before the drop). If a deeper `dip_db` is ever used, keep it no deeper than -6 and only in a section whose arrangement already thins. The `"silence"` part is true silence; use it once or twice at most, 100 to 300 ms before a hit. `score.py` prints the planned and the measured dips; the review's audio hole check (`review.md`) reads the rendered file.

## 10. The dynamic arc

- **Start below the body.** The professional first second sits a median 1.9 LU under the film's integrated loudness (10th percentile 18.6 LU under); the first mgpro films opened at or above it (-0.2 to +1.4 LU). Let the first second be 2 to 18 LU quieter than the body, and allow up to 0.5 s of silence before the first sound (professional median 0.05 s, 90th percentile 0.45 s).
- **Stay alive until about 85 percent.** Professional onset density stays near its median until about 85 percent of the length (4.2 per second at 80 percent, 3.4 at 90 percent) and falls only in the last 10 to 15 percent. The first films thinned out from 70 percent (about 2 per second at 80 percent, 0.5 at 90 percent) because the end card was held for 8 to 9 s with little happening. If the end card is long, give it its own small events: the sonic logo, a tail, a last UI tick.
- **Move the loudest moment.** The loudest 3 s sits anywhere from 21 to 91 percent of the length (median 66 percent): 16 percent of professional films peak in the first third, 32 percent in the middle, 52 percent in the last third. Choose it from the story (the reveal, the payoff, sometimes the opening), and not at the same place as the last film. On broadcast short form (EBU R128 s1) the loudest 3 s may be at most 5 LU above the programme loudness, so contrast must come from going quieter, not louder.
- **Range.** A loudness range (EBU LRA) of 5 to 11 LU (professional median 5.8, 90th percentile 11.4; the first films 3.6 to 4.2). Quiet passages must really be quiet. Because every platform normalises integrated loudness, a dynamic mix costs little: the quiet parts make the payoff bigger.
- **The ending is a choice.** Most films end about 1 s after their last loud second; 10 percent ring out for 5 s or more. Pick per film, not always the same one second tail. End on a real cadence or a designed tail, never on a fade that cuts the last note. The film ends in silence (the last 0.1 to 0.3 s).
- **In the kit** (`music.json`): `opening` (default `"soft"`, the first second about 2 LU under the whole, target `opening_lu` seeded between -1.6 and -3.5; `"cold"` opens at full level for a cold open form), `head` (silence before the first sound, seeded 0 to 0.12 s), `lra` (default 6.0: the level span between energy 0 and 1 is fitted to land this LRA), `keep_alive` (default true: drumless bars between 55 and 85 percent of the film get the lightest part).
- The shape over time is not the problem: the first films' loudness arc (rise, plateau, drop at the end) followed the professional median closely. What differed was the range, the opening and the late thinning.

## 11. Music against effects, and ducking

Starting levels, against the music at that moment (sourced ranges from mixing guides, set here as starting points **(heuristic)**):

| Layer | Level |
|---|---|
| music bed | the reference, 0 dB |
| ambient ticks, chatter, beds | 12 to 24 dB under |
| story clicks (the actions the story turns on) | 6 to 9 dB **over** the bed, a 2 to 4 dB music dip of about 150 ms where it still hides (`sfx-selection.md`, section 10) |
| secondary clicks, UI taps, pops, blips | 8 to 14 dB under (4 to 8 dB under the story clicks) |
| whooshes | 3 to 10 dB under (Contra's transitions measured a median 2.6 dB under; "if a viewer notices the whoosh consciously, it is too loud") |
| support thuds | 8 to 12 dB under |
| hero hits | 0 to 3 dB over the music peak for the frames of the hit, with the music ducked 3 to 6 dB around it |

- The effects bus at full level buried the intro and build of the torq film; at half it sat right. Expect the effects bus around half the music bus (`fx_level`, default 0.5) and set each sound by its weight, not one gain for everything.
- **With a voiceover**: set the voice first; music about 18 to 20 dB under the speech, effects about 12 to 18 dB under (featured transition effects up to about 6 dB under). Duck the music under the voice by 6 to 10 dB (gentle range 6 to 12), attack 30 to 80 ms, release 300 to 500 ms (400 to 700 if the music pumps between phrases), hold about 200 ms. Over ducking by 15 to 20 dB on every line is the most common mistake; broadcast mixers mostly automate faders and use only a couple of dB of voice keyed ducking.
- **Without a voiceover** (most product films): duck the music from the effects bus lightly, 2 to 4 dB, attack 1 to 10 ms, release 100 to 250 ms **(heuristic, extrapolated from the voice numbers)**, and only under hero and support hits. Duck the music's bass under an impact's sub for 100 to 300 ms so the hit stays clean; a braam or big sub at full weight on top of the music's bass turns to mud.
- **Carve, do not notch.** Keep 1 to 4 kHz clear enough for interface sounds (and the voice: consonants live in 1.2 to 2.4 kHz, presence in 2 to 5 kHz) with small 1 to 3 dB moves on the music; 600 Hz to 1.1 kHz is the nasal region, cut only if confirmed.
- **Frequency slots** **(heuristic, general practice)**: the music's bass 60 to 250 Hz and pads 300 Hz to 1 kHz; voice 1 to 5 kHz; UI ticks above 2 to 3 kHz (they cut through without level); impacts own 30 to 80 Hz for a few frames.
- **Kick sidechain inside the music**: keys, pads, stabs and hook duck under every kick (depth per genre: about 0.45 for house, 0.2 for lofi, none for cinematic); the bass ducks a little deeper. A beatless film has no kick pump at all.

## 12. Why AI films sound the same

129 professional motion graphics films (Apple, Stripe, Linear, Figma, Notion, Google, Buck, Ordinary Folk, ManvsMachine, Tendril, Antfood and more) and the first three mgpro films (Bauwerk, torq, Sendoku) went through the same audio analysis. Full numbers, method and every film are in `sound-research.md`. The short version: the mgpro films are not wrong on any single number; they are **the same film three times**, sitting at the same edge of the range on a few axes.

| What was measured | 129 professional films (10th, median, 90th percentile) | Bauwerk, torq, Sendoku |
|---|---|---|
| distance between two films' 10 metric profiles | different makers 2.7, 4.1, 6.1; same maker median 3.8 | 0.88 to 1.60 apart (only 0.45 % of 8,256 professional pairs are as close as the most distant AI pair) |
| strong transients shared with another film (r above 0.9) | median 4.6 to 5 % | Torq and Sendoku 42 %, the others 15 to 17 % |
| tempo | 108, 123, 148 BPM; 18 % between 117 and 123 | 120.2, 120.2, 120.2 |
| integrated loudness | -21.0, -15.0, -10.1 LUFS | -14.2, -14.1, -14.0 (true peak -1.36, -0.96, -1.36) |
| where the gap sits | dips cluster at 0 to 10 % and 90 to 95 % | one gap at exactly 45.8 % (frame 825) in all three |
| onset offset from the 16th grid (share of a 16th) | 0.085, 0.105, 0.17; 78 % within 25 ms | 0.047 to 0.093; 91 to 100 % on the grid |
| clear pulse | 29 % of films have none (pulse under 0.2) | all three have one |
| spectral centroid | 982, 1834, 2652 Hz | 2271 to 3035 Hz (74th to 98th percentile) |
| energy above 6 kHz | 0.1, 1.0, 3.2 % | 1.5 to 3.4 % |
| onset strength at a picture cut | 1.18 times baseline on average | 18.6 times |
| loudness range | 2.3, 5.8, 11.4 LU | 3.6 to 4.2 LU |
| dips per 10 s | 0, 0.78, 3.5 | 0.33 to 0.67 |
| first second against integrated | -18.6, -1.9, +3.9 LU | -0.2 to +1.4 LU |
| silence before the first sound | 0, 0.05, 0.45 s | 0 |
| onset density at 80 and 90 % of length | 4.2 and 3.4 per s | about 2 and 0.5 per s |

Not the problem: density (the first films had 3.0 to 3.6 onsets per second against a median 4.0), loudness, width, the overall loudness arc, and repetition inside a film.

**What professionals do instead, in a few films** (times from the start of the YouTube video):

- **Tendril, Microsoft emojis** (youtube.com/watch?v=Kh8BZPgpUhc): at 0:39.4 the sound drops more than 20 dB for 1.3 s (62 % of the film), from -30.4 dB before to -16.1 dB after; the first onset 51 ms after; density from 1.0 to 6.8 per second; the loudest second follows at 0:43.
- **Superhuman, Introducing Superhuman** (4XKq7qGnJus): a 0.85 s dip at 0:13.7 (23 %), back +10.3 dB, first onset 24 ms after; the busiest 2 s comes later at 0:26, the loudest second at 0:50 (84 %).
- **Notion, Introducing Notion AI** (FElBbgnNtVA): a 0.3 s dip at 1:14.2 (88 %), back +25 dB, and the densest 2 s of the film right after it: a late reveal, not mid film.
- **Samsung, One UI 5** (Rb9PvLhe9ok): a 0.15 s dip at 0:12.3, back +31 dB on a sustained chord, no new onset for 1.6 s.
- **Linear, Introducing Linear Agent** (mRql2VJ99gM): -28.9 LUFS integrated, LRA 17.6 LU, the loudest second at 0:04 (8 %): one opening impact, then a near silent film of quiet tones.
- **Raycast, New Raycast** (Mi173xGb0ZA): median density 0.8 per second with one burst of 5.5 per second; percussive share 0.03, LRA 13.6 LU: a tonal, swelling film.
- **Monzo, Money feels different** (pOUs63Qc80k): no pulse at all; effects follow the picture without a grid (median +39 ms after its cuts); a 1.25 s dip opens the film.
- **Stripe, Sessions 2024** (KH0_HM6e66w): almost no pulse (0.03) and 82 cuts carried by continuous texture, not hits.
- **ManvsMachine, Versus** (1ORKoaC3TlI): a heavy, slow tonal score; only 44 % of cuts get an onset within 2 frames.
- **Wise, design system** (x59J0l2EjAs) and **Apple, iPhone 15 Pro** (wqcjKkyuoZk): films cut to their own music, with 97 % and 83 % of cuts on an onset, the Apple film's loudest second at the very end (96 %).
- **Uber, new look** (axjXNEordH8): a 0.2 s dip at 48 %, then a jump of +18 dB; LRA 13.3 LU, more than twice the first mgpro films.

### The checks every film must pass

`fingerprint.py` measures the rendered `film.wav` against the professional distribution (`pro_stats.json`) and every film in the registry, prints pass or FAIL per check with the professional range beside it, and exits 1 on any failure. It is a port of the research scripts (`filmstats.py`); registry films are measured once and cached in `~/.cache/mgpro/filmstats/`.

```bash
python audio/fingerprint.py public/film.wav --bpm 112.5 --against ~/.claude/skills/mgpro/music/registry.json \
    --cues src/cues.json --music src/music.json [--video out/film.mp4] [--cold-open]
python audio/fingerprint.py public/film.wav --checks --cues src/cues.json   # the pro range checks without a registry
```

A failure means change the sound, not the threshold. The checks it enforces:

| Check | Pass |
|---|---|
| Profile distance (tempo, onset density, percussive share, share under 120 Hz, LRA, loudest 3 s position, grid offset, side share, dips per 10 s, density variation; standardized) to every registry film | at least 2.67 (professional 10th percentile, different makers) |
| Shared strong transients with any registry film (r above 0.9) | at most 10 % (professional median 4.6) |
| Spectral centroid | 982 to 2652 Hz |
| 85 % rolloff | 1714 to 5927 Hz |
| Loudness range | 5 to 11.4 LU |
| Opening | the first second at most -1.0 LU against the whole (skipped with `--cold-open`) |
| Rise at cuts | at most 3.93 times baseline (professional 90th percentile; median 1.71). Cuts are the cues with `cut: true`, else the hero cues, else the section starts (`--music`), or the scene cuts of a video (`--video`). It also prints hero and ordinary cuts apart, and what the music's bar downbeats measure with no cut |

It prints, without failing: grid offset, onsets on the grid, dips per 10 s and each dip, pulse, density and the 2 s density curve, percussive share, side share and tempo. Judge these against the rest of the rules, by hand:

| Rule | Aim |
|---|---|
| Tempo | 105 to 150 BPM unless the genre says otherwise, and not the tempo of any of the last three films (`music.md`) |
| Pulse | about one film in three beatless (pulse under 0.2); never three films with a beat in a row by habit |
| Grid | median onset offset 0.085 to 0.17 of a 16th; 56 to 90 % of onsets within 25 ms of a 16th |
| Breaths | arranged (parts stop over a bed or a tail), never a gain hole; the measured dips per 10 s are a result, anywhere from 0 to 3.5; near silences at most 2, each 100 to 300 ms before a hit; no window where the level falls more than about 6 dB without a listed arranged breath (`review.md`, Self check) |
| Breath position | the main breath not within 5 points of the same percentage as any registry film **(heuristic margin)** |
| Loudest 3 s | placed by the story; not within 10 points of the last film's **(heuristic margin)** |
| Hit evenness | onset strength variation 0.4 to 0.6; percussive share 0.2 to 0.5 |
| Pre hit ducks | none before ordinary cuts; only at the one or two re-entries |
| Density contrast | busiest 2 s against quietest 2 s between 2 and 9 times; the busiest 2 s window 6 to 9 onsets per second |
| Width | side share 0.02 to 0.24, chosen per film; widen at the big moment, not throughout |
| Ending | chosen (a 1 s tail or a 5 s ring out) and not the same as the last film's |
| Late density | onset density near the film's median until about 85 % of the length (`score.py` prints density at 75 to 85 percent) |
| Energy above 6 kHz | under about 2 % |

Report both tables with the measured values in the reply. These numbers are not targets to hit every time: they are the range professionals move in, and the registry check is what stops the next film from sitting where the last one sat.

## 13. Loudness and mastering per destination

| Destination | Integrated | True peak | Notes |
|---|---|---|---|
| YouTube video, YouTube ads, website, event screens | -14 LUFS (-16 to -14 for event screens) | -1 dBTP | YouTube only turns loud uploads down (a -10 LUFS upload is lowered 4 dB); the -14 figure is measured, not published |
| TikTok, Instagram, Facebook, LinkedIn, X | -14 LUFS | -1 dBTP | no published target (Meta adapts loudness); some creators master hotter, -10 to -12, as a strategy, not a standard |
| Google Play preview | -14 LUFS | -1 dBTP | it is a YouTube video, so YouTube's normalisation applies (inference) |
| Apple App Store preview | no published target; -14 LUFS | -1 dBTP | stereo AAC 256 kbps (H.264) or PCM or AAC (ProRes 422 HQ), 44.1 or 48 kHz, all tracks enabled, 15 to 30 s, plays muted by default |
| European TV and promos (EBU R128 s1, 2020) | -23.0 LUFS (plus or minus 0.2 LU at QC) | -1 dBTP | short term loudness (3 s) never above -18 LUFS; no LRA requirement for short form |
| US TV (ATSC A/85, CALM Act) | -24 LKFS | -2 dBTP | mandatory for US TV ads |
| Netflix style long form | -27 LKFS dialogue gated (plus or minus 2 LU) | -2 dBTP | rarely relevant to an ad |
| Cinema ads | about 82 dB Leq(m) on Dolby metering | | keep the mix dynamic |

- Use at least -1 dBTP for anything that will be lossy encoded (AAC, Opus); encoding raises inter sample peaks. -2 dBTP is safer for broadcast and when unsure.
- Hit the destination's integrated target within about 1 LU, from the film's own arc. Three films at -14.0, -14.1 and -14.2 LUFS with identical true peaks read as one preset; the professional films spread from -21 to -10 LUFS. Do not force a dynamic film up to the target with heavy limiting; a more dynamic master that lands slightly under the target loses little **(heuristic)**.
- Several destinations at once: one -14 LUFS, -1 dBTP master serves web, YouTube, stores and social; broadcast needs its own master (-23 LUFS with the -18 short term cap for Europe, -24 LKFS at -2 dBTP for the US), mixed again if the short term cap clips the payoff.
- Chain (`dsp.master(mix, lufs, tp, tone, bass_harmonics)`): high pass at about 28 Hz, the mix gain staged to the target minus 8 LU, gentle glue compression with its threshold at the target minus 2 (1.8:1, 25 ms attack, 160 ms release), the tone shelved toward the professional medians (`dsp.darken`, centroid near 1.8 kHz, rolloff near 4 kHz; `tone` in `music.json`, `false` keeps the mix's own brightness), the low end's harmonics added for small speakers, loudness to target (pyloudnorm), then a look ahead limiter driven by the 4x oversampled peak, iterated until the true peak is under the limit. The old chain's fixed -16 dBFS threshold on an unstaged mix squashed 3.6 LU of range and lifted openings. Over compressing a commercial makes it sound smaller once everything is normalised; a couple of dB of limiting is enough.
- Write 48 kHz, 24 bit stereo, exactly the film's length.

## 14. Small speakers and muted viewing

- Phone and laptop speakers give little below about 150 Hz (one practitioner says 110 Hz; not measured). The brain hears a missing fundamental from its harmonics, so saturate subs lightly (or blend a saturated, high passed copy of the bass; the kit's `dsp.harmonics`, set by `bass_harmonics` in `music.json`, default 0.3) and give every impact and logo hit a 120 to 500 Hz knock and a 2 to 5 kHz click. A hit that is 95 percent sub, as the first kit's impact was, is nearly silent on a phone.
- Keep impacts, the logo and anything essential in the centre: phone speakers are often effectively mono, and anything wide or out of phase can vanish. Keep most effects mono at the source and pan them with the action.
- Check: fold to mono; high pass the mix at 150 to 200 Hz and confirm every hero hit and the bass still read through their harmonics (150 to 800 Hz) and clicks (2 to 5 kHz); look at the spectrogram of that version.
- Muted autoplay is common (a 2019 survey: 69 percent watch with sound off in public, 25 percent in private). The picture must carry the rhythm and every message on its own: cut on motion accents, keep text up long enough to read, burn in captions for any voice. Sound must never be the only carrier of essential information.

## 15. A worked example: a 40 s SaaS film, second by second

Kerno (an invented invoicing app for small studios), a 40 s YouTube launch film at 1920x1080, 60 fps, -14 LUFS. Sonic brief: a minimal pulse in E dorian at 112.5 BPM (32 frames per beat, a bar every 128 frames, 2.133 s), no kick until the AI scene, a nylon pluck hook, character "paper and glass" (paper invoices becoming clean). Signature: a paper slide that ends in a glass tick, the sound of an invoice being finished. The registry's films peaked at 48 to 68 percent and all gapped at 46 percent, so this one peaks at 80 percent (the payoff) and breathes at 1, 79 and 90 percent, each breath arranged over a bed.

| Time | Frame | Picture | Sound | Weight, level |
|---|---|---|---|---|
| 0.0 | 0 | black, an empty invoice line fades up | nothing for 0.25 s | |
| 0.25 | 15 | the line sharpens | room tone and a low E pad enter, the first second about 10 LU under the body | bed, -22 dB |
| 1 | 60 | "Studio Nord" types itself, 11 letters over 0.6 s | key ticks generated from the letter times (frames 60, 63, 67...), pool of 4, 1.5 dB and 120 cents jitter, off the 16th grid | ambient, -16 dB |
| 2 | 120 | the amount counts up to 4,800 | nothing: the counter is secondary | none |
| 3 | 180 | a second line types | two ticks only, on the first and last letter | ambient, -18 dB |
| 4 | 240 | the invoice tilts back | a 280 ms swish starts at frame 250 | support, -9 dB |
| 4.45 | 267 | ordinary cut, with the action (off the bar 2 downbeat at 256): the invoice slides into a stack | the swish peaks on 267 (`cut: true`); a soft paper slide | support |
| 5 | 300 to 330 | five more invoices stagger in over 0.5 s | one paper slide for the whole group, and one thud plus click only when the last card settles (frame 330) | support, -10 dB |
| 6.4 | 384 | "Every invoice. One place." rises word by word | no effect: the hook's first note lands with "place" (bar 3) | none |
| 7 | 420 | the stack drifts toward camera | a shaker texture enters, low passed at 6 kHz, loosely timed | ambient, -20 dB |
| 8.0 | 480 | the frame darkens | a reverse swell of one beat (0.53 s) starts | support |
| 8.53 | 512 | structural cut on the bar 4 downbeat (an act change): a crumpled receipt, the AI reads it | the swell ends on 512; the pulse enters (kick and bass), the section rises about 4 dB; a short low knock on the kick, no boom | structural, the kick is the hit |
| 9 to 11.5 | 540 to 690 | a scan beam moves down the receipt | band passed noise sweeping 6.5 kHz down to 900 Hz over 1.6 s, because the beam goes down | ambient, -18 dB |
| 9.8, 10.5, 11.2 | 590, 628, 671 | three fields light up as the beam passes | three blips rising E, G, B in the pentatonic, each d20 25 ms, on the frame each box lands (off grid) | support, -12 dB |
| 12 | 720 | the fields lift off the receipt | nothing yet | |
| 13.05 | 783 | ordinary cut, with the action (after the bar 6 downbeat at 768): the fields fly into the invoice | one airy whoosh of 0.7 s for all three (not three), panned left to right with the flight, peak on frame 790 where they arrive | support, -10 dB |
| 13.2 | 790 | the fields land in the invoice | one glass tick | support, -12 dB |
| 14 | 840 | "Read by AI. Checked by you." | nothing; the hook's answer phrase | none |
| 15 | 900 | a check mark toggles on | toggle: two notes up a fourth, 70 then 120 ms | support, -11 dB |
| 16 | 960 | the invoice shrinks into a list | nothing | none |
| 17.4 | 1044 | ordinary cut, as the list finishes shrinking (bar 8's downbeat was 1024): a cash flow chart | no hit; the music carries it (`cut: true` on no sound, so the rise at the cut is measured) | none |
| 17 to 21 | 1024 to 1280 | the line draws month by month | a very quiet rising filtered noise for the line, and a tick at each of 12 month knots (3 per second), pitch rising with the value, pool of 4 | ambient, -18 dB |
| 21.33 | 1280 | bar 10: the line lands, "+38 % paid on time" pops | a soft pop rising 5 st on 1280 (in a real film the number is the product's own figure) | support, -10 dB |
| 22 to 23.5 | 1320 to 1410 | three client avatars join | a decaying series: three pops, each 2 dB quieter and a scale step higher, frames 1320, 1352, 1381 | support |
| 24 to 25 | 1440 to 1500 | the chart pulls back into a list of unpaid invoices | nothing on the move; the hook's last phrase | none |
| 25.6 | 1536 | bar 12: three invoice rows flip to "sent" | three ticks, a scale step apart, on the frames each row flips (1540, 1561, 1583) | support, -12 dB |
| 27.73 | 1664 | bar 13: the list tightens, the camera pushes in | the arrangement thins to make room to rise: the bass drops out, the hats close, a low pass settles on the pads (no fader move) | music |
| 29.87 | 1792 | bar 14: invoices compress into one | a noise riser starts, high passed at 150 Hz, cutoff opening on an accelerating curve, widening | hero lead in, rising to -6 dB |
| 31.68 | 1901 | the screen holds on one invoice | the riser stops dead; an arranged **breath** of an eighth of a bar, 16 frames (0.27 s, to frame 1917): drums and bass stop, the riser's reverb tail and the pad ring on (a form section of `"bars": 0.125` whose `parts` are only `["pad"]`) | the main breath, at 79 % |
| 32.0 | 1920 | bar 15: a "Paid" stamp lands on the invoice | **the hero hit** on frame 1920 (`weight: "hero"`, `cut: true`), 3 frames (50 ms) after the breath ends: transient (5 ms noise over 2 kHz), paper and wood knock at 120 to 500 Hz (d20 40 ms), sub at 50 Hz dropping 2 st in 30 ms (0.6 s), the shared room tail; the signature paper slide and glass tick as its tail. The full band returns with it, about 10 dB above the thinned bar before the breath because more is playing, its bass ducked 4 dB under the sub for 250 ms | hero, +2 dB over the music peak |
| 32 to 35 | 1920 to 2100 | payoff: "Get paid on time. Every time." | full groove and hook, the widest section (side share about 0.2), 6 to 7 onsets per second; the loudest 3 s of the film (80 to 88 %) | music |
| 35 | 2100 | the stamp folds into the wordmark | drums out except the shaker; a last UI tick as the wordmark's dot lands (frame 2130); density stays about 3 per second | support |
| 36.0 | 2160 | a beat of stillness | the drums stop for 16 frames (0.27 s) at 90 %, the pad and the stamp's tail ring under it | breath |
| 36.27 | 2176 | structural cut on the bar 17 downbeat: the end card, the Kerno wordmark | the sonic logo: the hook's first four notes on the nylon pluck, a soft glass bell, the low root; 2.5 s, about 3 LU under the reveal | structural |
| 38 to 39.8 | 2280 to 2388 | the end card holds | the logo rings out, pad fades over its own tail | |
| 39.8 to 40 | 2388 to 2400 | | silence | |

What the plan adds up to: one hero hit (32.0 s), two structural moments carried by music (the pulse at 8.53 s, the end card at 36.27 s), about a dozen support sounds, everything else ambient or nothing. Of six cuts, three are structural (8.53, 32.0 and 36.27 s), sit on bar downbeats and get a mark; the ordinary ones fall with the action between downbeats. Three arranged breaths (an opening breath, the main one at 79 percent, one at 90 percent), no gain automation, one true silence (the last 0.2 s). The opening is 10 LU under the body, the loudest moment is at 80 percent, density stays up until about 36 s (90 percent). No sound repeats unchanged; the only exact grid sounds are the music and the structural hits.

## 16. Bad and good versions of the same moment

**Six cards stagger in over 0.5 s.**

- Bad: the same pop on each card, all at one level, each snapped to a 16th; a whoosh on top; a boom on the cut that follows. Six identical transients in half a second, then a slam.
- Good: one swish the length of the stagger; a thud and click only when the last card settles, on its frame; or, if each card matters, a decaying series of pops, 2 dB quieter and a scale step higher each, timed to each card's own landing. No boom: this is support.

**The reveal.**

- Bad: a four bar riser into dead silence of 0.25 s at 45.8 percent of the film (the same place as the last film), the level before it already at full build, so the hit returns only 4 dB louder; the hit is 95 percent sub (silent on a phone), 18 times the baseline; the kick resumes exactly on the grid 13 ms later; the music pulled to half 150 ms before every earlier cut too.
- Good: the passage before the riser is thinned (fewer parts, not a lower fader) so there is room to rise; a riser of one to two bars that stops dead; a breath of about an eighth of a bar (about 0.28 s) where drums and bass stop and a pad tail stays alive, no fader move; the hit 20 to 70 ms after the breath, built from a recorded knock (its transient and 120 to 500 Hz body), a short sub under it and the shared room; the full band back with it, about +9 dB because more is playing, its bass ducked under the sub for 250 ms; the reveal at the place this story needs, not where the registry already has one.

**A quiet moment between two scenes.**

- Bad (the Enogon film): the whole mix multiplied 24 dB down for 0.3 s about every 7 s, after the reverbs, so the pad and every tail vanish with the notes; nothing on screen or in the music explains it; the viewer hears the sound drop out.
- Good: the drums and bass stop on a cadence, a held chord or the last note's tail keeps ringing, the picture keeps moving, and within one beat to one bar the next section enters bigger on a structural cut.

**Typing.**

- Bad: one key sample on every 16th note while the letters appear at their own speed, so sound and picture drift apart and the run machine guns.
- Good: one tick per letter generated from the same times the picture uses, a pool of 3 to 6 variants, 1 to 3 dB and 100 to 200 cents of jitter, quieter as the line goes on; the second line gets two ticks, the third none.

**The opening.**

- Bad: the full mix from frame 0, at or above the film's integrated loudness, a kick on the first downbeat.
- Good: 0.1 to 0.5 s of silence, then a single tone, a room or a texture 5 to 15 LU under the body, and the first musical event when the first image means something.

**An ordinary cut between two shots of the same scene.**

- Bad: a whoosh and a hit on every cut, the same whoosh each time.
- Good: nothing, and the cut falls with the action between the downbeats, so the music's own downbeat (which alone measures 3 to 9 times baseline) does not slam it. Save the downbeat and the whoosh for the act change.

## 17. Checking without ears

1. `score.py` prints integrated loudness, true peak, LRA, the opening, centroid, rolloff, grid offset, pulse, density at 75 to 85 percent, the planned and measured dips, then RMS per section. With `"dips": 0` and arranged breaths, no section should read more than about 6 dB under its neighbours unless it is a listed breath with a bed (only a true `"silence"` part reads near -50, and only for 100 to 300 ms); then run the audio hole check in `review.md`.
2. `fingerprint.py --against` the registry with `--cues` and `--music`: the checks of section 12, pass or FAIL. To try an idea before the film exists, `demo.py <genre> --film [--beatless]` renders a 30 s film on the kit's example form with a sample cue list into `out/demo-film-<genre>/`.
3. The accent map: measured onsets of every synced cue against its frame (section 6).
4. A spectrogram: `ffmpeg -i public/film.wav -lavfi showspectrumpic=s=1600x400:legend=1:scale=log out/spec.png`, and `showwavespic` for the shape. Look for walls of noise (a ride or open hat too long), empty lows, a phone version (high passed at 150 Hz) that loses the hits, and sections that read as the form.
5. The decoded final file, not the preview: an AAC stream exists, its length matches the picture, nothing was cut by a blind `-shortest`, the last scene and the music's ending are whole, there is no stray audio tail, and the sync points still hold after muxing. Map the streams explicitly when muxing so no music, effect or voice is lost or replaced by a single effect; a silent brief gets no audio added. A realtime preview (Web Audio in the plain HTML route) proves nothing about the export: render the audio offline into a real file. An audio stream is not proof of audible sound; a silent stream never passes as scored. Listen for what the numbers can miss and say whether anyone did: clicks at sound boundaries, clipped samples, an abrupt cut off, a tiresome repeated effect.
6. Say it plainly in the reply: measured, not heard. "Listened to" is its own status, separate from implemented, checked by running, seen in frames and checked in motion; it stays unchecked unless someone listened. Name the tiers, the hero moments, the breaths and their positions, and where the loudest moment sits, so the user knows what to listen for.
