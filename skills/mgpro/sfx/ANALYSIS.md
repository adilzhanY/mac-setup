# What the library teaches

1126 CC0 sounds in 30 packs, analysed by `templates/kit/audio/sfx_catalog.py`; the synthesizer's 43 effects (`sfx.py`, every character, rendered by `--synth`) went through the same analysis. Everything here is measured, not heard. The picks below are where to start listening, not a verdict.

How to read the numbers: **length** is first to last point within 40 dB of the peak. **Attack** is 10 to 90 percent of the peak. **d20** is peak to -20 dB, the part a viewer actually hears; **d40** is peak to -40 dB, the tail. **Centroid** is power weighted, so a low "whum" with a faint hiss reads as low. **Low share** is the share of energy from 120 to 500 Hz, **sub** under 120 Hz. **Noisiness** is 0 for a pure tone and 1 for pure noise. Ranges are 25th to 75th percentile, "median" is the 50th.

Category counts come from file names first, features second, so they are approximate (a few "foley" files are really whooshes, a few "impact" files are really pops). Pitch movement for noisy sounds follows the centroid and is unreliable for impacts, whose high transient dies before the low body.

## 1. What each category has in common

| Category | n | Length ms | Attack ms | d20 ms | Centroid Hz | Noisiness | Tonal | Pitch movement |
|---|---|---|---|---|---|---|---|---|
| click/tap | 219 | 94 to 308 (median 167) | 2 to 17 (3) | 8 to 26 (14) | 1900 to 5900 (3600) | 0.52 to 0.93 | 16 % | falling 127, flat 72, rising 20 |
| pop | 19 | 82 to 175 (129) | 1 to 46 (4) | 16 to 39 (23) | 740 to 3250 (990) | 0.07 to 0.48 | 74 % | mostly flat, a few rising |
| whoosh/swish | 30 | 94 to 506 (212) | 17 to 98 (35) | 17 to 114 (27) | 260 to 3200 (590) | 0.06 to 0.80 | 27 % | flat or falling |
| impact/thud | 196 | 168 to 491 (265) | 0 to 10 (3) | 17 to 71 (34) | 200 to 1000 (500) | 0.14 to 0.73 | 33 % | mixed (centroid based) |
| riser | 26 | 262 to 520 (318) | 5 to 265 (80) | 49 to 173 (75) | 1280 to 3520 (3130) | 0.01 to 0.29 | 77 % | rising 17 of 26 |
| tonal/bell | 195 | 342 to 1000 (616) | 18 to 147 (51) | 67 to 240 (162) | 540 to 1960 (840) | 0.02 to 0.15 | 94 % | flat 72, falling 58, rising 48 |
| glitch/digital | 129 | 251 to 627 (369) | 2 to 89 (14) | 49 to 207 (102) | 480 to 2270 (990) | 0.04 to 0.33 | 67 % | falling 57 of 129 |
| texture/noise | 47 | loops, 4.7 to 5 s | 33 to 842 | n/a | 180 to 1050 | 0.04 to 0.54 | 53 % | flat |
| foley | 265 | 202 to 600 (381) | 2 to 84 (18) | 11 to 85 (37) | 1100 to 5800 (3200) | 0.51 to 0.94 | 11 % | mixed |

The pattern across the whole library: **what you hear is short even when the file is long.** Clicks ring out to -40 dB over 60 to 200 ms, but drop 20 dB in 8 to 26 ms. Impacts have a 150 to 450 ms tail but a d20 of 17 to 71 ms. Only bells and chimes keep a d20 above 100 ms.

Width: 934 of 1126 files are stereo and 427 have real width (side over mid above 0.1). Kenney's interface pack is mono; its UI Audio pack sits at 0.15 to 0.6; designed whooshes at 0.4 to 1.2.

## 2. Good versus cheap, in numbers

These contrasts compare the designed sets (Kenney interface, UI Audio and impact packs, made as coherent sets for interfaces) with the rougher ones in the same category (raw recorded or converted clips). They are tendencies to aim for, checked on the sheets, not rules proven by listening.

**A good UI click** (Kenney `click_002`, `click_003`, UI Audio `click4`, `click5`):

- d20 4 to 18 ms and a total length of 7 to 60 ms. One transient.
- Attack under 1 to 3 ms, no silence before it (`lead_ms` 0).
- Centroid 1.9 to 4.6 kHz with 55 to 80 percent of the energy in 2 to 6 kHz and under 10 percent below 500 Hz.
- Often a quick downward pitch: UI Audio clicks fall 10 to 14 semitones within 40 ms.
- Clean: noise floor below -50 dB, no clipped samples, and a set of 3 to 5 variants with the same shape.

**A cheap click** (most of `oga-button-clicks`, many of `oga-click-clips`): 200 to 600 ms long with a d20 of 15 to 55 ms, 4 to 5 transients (rattle and room), attack 10 to 360 ms where an encoder or a slow fade softened the hit, noise floor around -44 dB, levels spread over 17 LU (-15 to -32 LUFS), and 20 to 70 percent of energy above 6 kHz, so it hisses instead of clicking.

**A soft pop versus a harsh pop.** Soft (Kenney `drop_002`, `drop_003`, `drop_004`, `oga-pop-effects/p_1`): a tone (noisiness 0.01 to 0.2) on F#5 to B5 (740 to 990 Hz), centroid 640 to 980 Hz, nothing in 2 to 6 kHz, attack under 5 ms, d20 10 to 42 ms, total 70 to 105 ms, flat or with a small upward bend of 3 to 7 semitones. Harsh (Kenney `drop_001`, `oga-100-sfx/plop_01`, `plop_02`): noise instead of tone (noisiness 0.5 to 1.0), centroid above 1 kHz, a 16 semitone bend, and clipped samples (8 and 60 in the plops).

**A whoosh that feels fast versus one that feels heavy.**

| | Fast (swish) | Heavy (swing) | Airy (designed transition) |
|---|---|---|---|
| Examples | `oga-swishes/swish-*`, `remotion-cc0/whip`, `remotion-cc0/whoosh` | `oga-time-hit-wind/qubodup-megaswosh1`, `megaswosh2`, `60009__qubodup__swosh_22` | `oga-scifi-50/misc_09`, `misc_10`, `misc_11`, Kenney `open_00*` and `close_00*` |
| Length | 60 to 160 ms | 290 to 510 ms | 300 to 1100 ms |
| Attack | 10 to 30 ms, peak in the first third | 30 to 100 ms | 70 to 280 ms (open: peak at the very end) |
| d20 | 8 to 28 ms | 30 to 50 ms, then a long tail | 300 to 440 ms (close: 230 to 280) |
| Spectrum | centroid 190 to 600 Hz, nearly all energy under 2 kHz; often a whistle tone (noisiness under 0.2, whip at C#5) | centroid 400 to 450 Hz, 80 to 88 percent in 120 to 500 Hz | centroid 5 to 13 kHz, 30 to 90 percent above 6 kHz, noise |
| Width | near mono | 0.3 to 1.2 | 0.4 to 0.9 (Kenney open/close are mono) |

A real object moving through air is a low "whum" with a whistle, not hiss. Hiss reads as a designed, digital transition. Speed comes from a short length with the peak early; weight comes from length, a slower attack and width.

## 3. Best examples per motion graphics job

Paths are relative to `~/.local/share/mgpro/sfx/`. Listen to the 2 or 3 files of a family and vary them per use.

| Job | Start with | Why (measured) |
|---|---|---|
| Button press | `kenney-ui-audio/Audio/click4.ogg`, `click5.ogg`; `kenney-interface-sounds/Audio/click_002.ogg`, `click_003.ogg`; `kenney-interface-sounds/Audio/select_001.ogg` for a tonal press | 7 to 60 ms, d20 4 to 18 ms, centroid 1.9 to 4.6 kHz; UI Audio clicks fall 10 to 14 st and are slightly wide; select_001 is a D5 ping with d20 13 ms |
| Toggle or switch | `kenney-interface-sounds/Audio/toggle_001.ogg` to `toggle_004.ogg`; `kenney-ui-audio/Audio/switch2.ogg` | tonal C6 to G#6, d20 52 to 78 ms; switch2 is a 100 ms bright snap |
| Card lands | `kenney-impact-sounds/Audio/impactWood_light_000.ogg` to `_002`; `impactSoft_medium_000.ogg` to `_004`; `kenney-rpg-audio/Audio/bookClose.ogg`; `kenney-casino-audio/Audio/card-slide-1.ogg` | 80 to 180 ms, attack 0 to 5 ms, d20 12 to 27 ms, 60 to 100 percent of energy under 500 Hz; bookClose has a 10 st falling thump (trim its 56 ms lead) |
| Light object lands (glass card, chip) | `kenney-impact-sounds/Audio/impactGlass_light_000.ogg` to `_002`; `impactMetal_light_000.ogg` to `_002`; `kenney-casino-audio/Audio/chips-collide-1.ogg` | 105 to 185 ms, tonal (C6, D6) with d20 45 to 87 ms; chips are 70 to 120 ms bright clicks |
| Text appears (per word or line) | `kenney-ui-audio/Audio/rollover2.ogg`, `rollover5.ogg`; `kenney-interface-sounds/Audio/select_002.ogg`; `kenney-interface-sounds/Audio/glass_002.ogg`, `glass_006.ogg` | soft and short: 43 to 96 ms, d20 13 to 21 ms, centroid 0.9 to 2 kHz, rollovers fall 8 to 28 st |
| Transition, fast cut | `oga-swishes/swishes/swish-10.wav` to `swish-13.wav`; `remotion-cc0/whip.wav`; `remotion-cc0/whoosh.wav` | 60 to 155 ms with an early peak; place the peak on the cut |
| Transition, heavy or big | `oga-time-hit-wind/qubodup-megaswosh1.wav`, `qubodup-megaswosh2.wav` | 480 to 510 ms, low and wide (width 0.5 to 1.2) |
| Transition, panel opens or closes | `kenney-interface-sounds/Audio/open_002.ogg` to `open_004.ogg` (rise, END on the frame) and `close_002.ogg` to `close_004.ogg` (start on it, fall) | 300 ms noise sweeps, up 6 to 17 st or down 5 to 17 st, open stops within 2 ms |
| Airy reveal, light sweep | `oga-scifi-50/misc_10.ogg`, `misc_11.ogg`, `misc_09.ogg` | 0.5 to 1.1 s, centroid 5 to 8.4 kHz, wide |
| Logo | `oga-metal-dings/ding.3.ogg`, `ding.2.ogg`; `oga-bell-dings/bell_ding3.wav`; `oga-gui-lokif/GUI_Sound_Effects_by_Lokif/sharp_echo.wav`; for a weighty hit under it `kenney-impact-sounds/Audio/impactBell_heavy_000.ogg` | 1.2 to 2.4 s bells, d20 190 to 540 ms, inharmonic partials (noisiness 0.2 to 0.4 on a clear note); sharp_echo is a wide C5 with a 540 ms d20 |
| Success | `kenney-interface-sounds/Audio/confirmation_001.ogg` to `_004`; `kenney-interface-sounds/Audio/maximize_002.ogg` (rising); `oga-ui-feedback/ui_wav/Ding.wav`, `chimes.wav` | confirmation: 4 to 6 notes in 280 to 510 ms, d20 190 to 290 ms; maximize rises 11 st; Ding and chimes rise 5 to 7 st and are wide |
| Error | `kenney-interface-sounds/Audio/error_003.ogg`, `error_006.ogg`, `error_007.ogg`; `oga-ui-feedback/ui_wav/negative_sound2.wav`; `oga-ui-haeldb/New folder/Wrong Error.wav` | low (centroid 170 to 2700 Hz, most under 600), some buzz (noisiness 0.2 to 0.8), 1 to 4 hits, d20 40 to 75 ms; falling where it moves |
| Data tick, counter, scroll | `kenney-interface-sounds/Audio/tick_001.ogg`, `tick_002.ogg`; `kenney-interface-sounds/Audio/scroll_004.ogg`, `scroll_005.ogg` (19 ticks about 50 ms apart); `kenney-casino-audio/Audio/chips-stack-1.ogg` | 9 to 22 ms, d20 4 to 9 ms, centroid 3 to 11 kHz; scroll_004/005 are tonal ticks at F#7 and B5 |
| Musical sting under an end card | `kenney-music-jingles/Audio/*` (NES, SAX, STE, PIZ, HIT sets of 17) | 0.5 to 1 s, each a short phrase; check its key against the score before use |

The library is thin on pops (19), whooshes (30) and real risers (Kenney's are game power ups); synthesize those and use the targets below.

## 4. Synthesis targets for the numpy engine

Ranges a synthesized effect should land in, measured with `sfx_catalog.py --file`.

| Effect | Attack | d20 | Total to -40 dB | Centroid | Energy | Tone versus noise | Pitch | Width |
|---|---|---|---|---|---|---|---|---|
| tap / click | under 1 to 3 ms | 4 to 15 ms | 10 to 60 ms | 1.5 to 4.5 kHz | under 15 % below 500 Hz | noise burst (0.6 to 1.0), optionally a ping | ping falls 5 to 15 st in 40 ms | 0 to 0.4 |
| UI blip / select | under 2 ms | 13 to 35 ms | 35 to 180 ms | 1.2 to 3.5 kHz | mostly 500 Hz to 6 kHz | tone with a noise or click transient (0.05 to 0.3) | falls 1 to 2 st | 0 to 0.3 |
| tick (data) | under 1 ms | 4 to 9 ms | 9 to 25 ms | 3 to 10 kHz | 50 to 90 % above 2 kHz | noisy (0.3 to 0.85) or a very high ping | flat; a run rises by notes | mono |
| soft pop | 1 to 5 ms | 10 to 40 ms | 70 to 110 ms | 650 to 1000 Hz | nothing in 2 to 6 kHz | tone (under 0.2), fundamental 740 to 990 Hz | rises 3 to 7 st | mono |
| card lands (thud) | 0 to 5 ms | 12 to 30 ms | 80 to 180 ms | 70 to 450 Hz | 85 to 100 % under 500 Hz, most of it 120 to 500 Hz | mixed | short drop | mono |
| big impact | 0 to 12 ms | 30 to 60 ms (the body), then a tail | 0.4 to 1 s | 70 to 420 Hz | 60 to 80 % sub but 22 to 33 % in 120 to 500 Hz | mixed | body drops | 0 to 0.5 |
| fast swish | 10 to 30 ms | 8 to 28 ms | 60 to 160 ms | 200 to 600 Hz | nearly all under 2 kHz, mostly 120 to 600 Hz | low band noise plus a whistle tone | small bend | 0 to 0.3 |
| heavy swing | 30 to 100 ms | 30 to 50 ms then tail | 300 to 500 ms | 400 to 450 Hz | 80 % or more in 120 to 500 Hz | noise plus whum | falls 2 st | 0.5 to 1.2 |
| airy transition | 70 to 170 ms | 300 to 440 ms | 500 to 1100 ms | 5 to 8.5 kHz | 30 to 90 % above 6 kHz | noise (0.8 to 0.97) | slight rise | 0.4 to 0.9 |
| UI open (riser) | 200 to 280 ms, peak at the end | 1 to 2 ms (hard stop) | 300 ms | 8.7 to 13 kHz | mostly above 6 kHz | noise | rises 6 to 17 st | mono or wide |
| success chime | 0 ms per note | 190 to 290 ms | 280 to 500 ms | 1.2 to 2.6 kHz | | tones | 4 to 6 notes, 60 to 80 ms apart, flat or rising | 0 to 0.6 |
| error | 0 to 15 ms | 40 to 75 ms | 100 to 200 ms | 180 to 1000 Hz | low | some buzz (0.2 to 0.4) | flat or falling | mono |
| logo bell | 1 to 50 ms | 110 to 380 ms | 1.2 to 2.4 s | 0.7 to 3 kHz | | tone with inharmonic partials (0.15 to 0.4) | flat | 0 to 0.5 |

## 5. Where the current synthesizer is off

Measured from `synth.json` (each effect of `sfx.py` in all five characters, key G ionian).

1. **Everything rings ten times too long.** `dsp.perc(n, a, length)` treats `length` as an exponential time constant, so a sound is 20 dB down only after 2.3 x length and 40 dB down after 4.6 x length. `blip(length=0.12)` measures d20 166 to 413 ms; the library's tonal UI sounds measure 13 to 35 ms (Kenney `select_*`, `glass_*`). `chime` measures d20 430 to 690 ms against 190 to 290 ms for Kenney's confirmations. `tick` measures d20 19 ms against 4 to 9 ms. Fix: choose the time constant as the wanted d20 divided by 2.3 (a 20 ms d20 needs `length=0.009`), and stop padding blips by 0.3 s.
2. **Every tonal effect is a pure tone.** Noisiness 0.00 to 0.01 for all 15 blips, ticks and chimes. Designed UI tones carry a short noise or click transient on top (noisiness 0.05 to 0.3), and real clicks and ticks are mostly noise (0.55 to 1.0). The synth tick is a 12 ms sine at a fixed pitch; Kenney's ticks are 9 to 22 ms noise bursts centred at 9 to 11 kHz.
3. **Nothing moves in pitch.** 28 of 43 renders are flat and only 2 fall; in the library 127 of 219 clicks fall, selects fall 1 to 2 st, rollovers 5 to 39 st, UI Audio clicks 10 to 14 st, pops rise 3 to 7 st, swipes sweep 6 to 17 st. A small, fast pitch movement is most of what makes a sound feel physical.
4. **Everything is mono and dead centre.** 33 of 43 renders have width 0.00 (whoosh 0.14, textures 0.34 from panned grains). Library clicks from UI Audio and the click clips sit at 0.15 to 0.6, designed whooshes at 0.4 to 1.2.
5. **The click is a box, not a click.** 77 to 79 percent of its energy is the 380 Hz body (120 to 500 Hz band), centroid 680 to 1050 Hz, d20 26 to 27 ms. Library clicks keep under 10 percent below 500 Hz (Kenney interface median 3 percent), centre at 1.6 to 4.6 kHz and drop 20 dB in 4 to 18 ms. Cut the body to about 10 to 20 percent of the energy (or 5 ms long), and shorten the press.
6. **The impact is all sub and lasts too long.** 95 to 98 percent of the energy under 120 Hz, centroid 48 to 56 Hz (445 Hz for glass, from its hiss), d20 179 to 469 ms. Even the heaviest library hits (Kenney `impactPunch_heavy`, `impactPlate_heavy`, `lowFrequency_explosion`) keep 22 to 33 percent in 120 to 500 Hz and drop 20 dB in 31 to 55 ms. On laptop and phone speakers, which give little below 150 Hz, the synth impact is close to silent except its noise burst. Add a 120 to 500 Hz knock with a 30 to 50 ms d20 and shorten the sub body. A cinematic boom under a drop may keep a longer sub tail; a card landing must not.
7. **The whoosh is hiss of one fixed length.** 0.41 s whatever the move, noisiness 0.97 to 0.99, centroid 1.7 to 7.1 kHz, width 0.14. Real swishes are 60 to 160 ms, low (190 to 600 Hz) and partly tonal (a whistle); heavy swings are 300 to 500 ms, low and wide; designed airy whooshes are 0.5 to 1.1 s and wide (0.4 to 0.9). The synth sits between all three: too long for a swish, too bright for a swing, too narrow for an airy sweep. Make the length follow the motion's duration, add a band at 150 to 500 Hz and a whistle for physical moves, and decorrelate the channels for airy ones.
8. **The five characters barely differ.** Across glass, wood, metal, digital and soft: every click has d20 26 to 27 ms and a 380 Hz body, every tick d20 19 ms, every whoosh 0.41 s, every impact the same sub body, every chime the same three notes 80 ms apart. Only an oscillator frequency or a filter changes. Characters should differ in envelope (wood: d20 10 to 20 ms; metal and glass: ringing partials 50 to 300 ms), in noise share and in pitch movement, not only in frequency.
9. **One sound serves many events.** `score.py` sends `tap`, `place`, `blip`, `land`, `block`, `card` and `tier` all to `sfx.blip`, so a card landing gets the same 300 ms tonal ring as a tap. In the library a landing is an 80 to 180 ms low thud (`impactWood_light`, `impactSoft_medium`, `bookClose`) and a tap is a 7 to 60 ms click. This alone makes a film's effects feel alike.
10. **What is already in range.** Synth attacks of 2 to 4 ms equal the library's median click attack (3 ms); the designed Kenney interface set is sharper (under 1 ms), so for crisp UI keep the fade in under 1 ms. The riser's shape (a swell that stops within 6 to 50 ms) matches Kenney's `open_*` swipes, though theirs move 6 to 17 st in 0.3 s. Synth levels (-9 to -28 LUFS) sit inside the library's spread.
