# Sound research: the evidence behind sound.md and music.md

Where every sound rule in this skill came from, with sources and numbers, so a later version can check a rule against its origin and change it when better evidence arrives. Researched 27 October 2026. The full notes are in `~/dev/mgpro-research/research_notes/Sound design in motion graphics/` (six files) and the measurement code and data in `~/dev/mgpro-research/films/`.

**Second research run (29 October 2026, after the Enogon review)**: composition to picture, AI tells and realism, CC0 instrument libraries and headless rendering, transitions and feeling, logo reveals, pacing and cursor animation. It corrected one rule built on this file: the dip numbers in section 7 and section 1 are measured results of professional arrangement, not instructions to automate gain (`sound.md`, section 9). Report and notes: `research/ad-music-and-logo/`; the rules: `composition.md`, `logo-resolve.md`, `sound.md` sections 4b and 9, `craft.md` Pacing, `interaction.md` How it moves.

How to read this file:

- A plain statement is sourced; the source follows it.
- **(heuristic)** marks a number chosen by the research as a working start point, derived from sourced ranges but not itself published or measured.
- **(snippet)** marks a finding read only in a search result summary, not on the fetched page.
- **(measured)** marks a number from the skill's own analysis of real films or of the CC0 library.
- Many vendor pages (sound libraries, plugin makers) are marketing; they are cited because nothing better was found, and their numbers carry less weight than standards and measurements.

## 1. 129 professional films measured against the first three mgpro films (measured)

Source: `~/dev/mgpro-research/research_notes/Sound design in motion graphics/real_films_measured.md`; code `films/analyze.py`, `summarize.py`, `crossfilm.py`, `cutsync.py`, `examples.py`; data `films/summary.csv`, `films/distributions.json`, charts `films/charts/*.png`.

**Corpus.** 130 films chosen by hand from 143 searches (Apple, Stripe, Linear, Figma, Notion, Vercel, Raycast, Arc, Framer, Spotify, Google, Buck, Ordinary Folk, ManvsMachine, Oddfellows, Giant Ant, Tendril, Buff, THE LINE, Antfood, Echoic, SaaS and fintech brands): official channels, 12 to 250 s, motion graphics or product films, none known to be cut to a licensed pop song. One had no audio, leaving 129. All from YouTube (Vimeo needs a login). Audio of the first 180 s. AI films: Bauwerk, torq and Sendoku, 30.0 s each, 48 kHz.

**Method.** ITU BS.1770 loudness (pyloudnorm), 4x oversampled true peak, EBU LRA, librosa 0.11 beat tracking and onsets (hop 11.6 ms), HPSS percussive share, spectral centroid and 85 percent rolloff, mid and side energy, near silences (40 dB under the 95th percentile level, 100 ms or more) and dips (20 dB under, 150 ms or more), grid offset of each onset from the nearest 16th, repetition by clustering 93 ms log mel patches after strong onsets, cuts by ffmpeg scene detection at 0.3 on 144p video, cross film shared sounds (strong onsets matching at r above 0.9) and a 10 metric standardized profile distance. Self check: a 120 BPM click track gives 120.2 BPM, pulse 0.96, grid offset 0.

**Limits.** YouTube audio is lossy; many professional films have a voiceover (pushes density and percussive share up a little); scene detection finds hard cuts, not morphs; onset times lag the attack by about one hop (12 ms); the beat tracker makes octave errors and returns tempo in coarse steps, so tempo is approximate and meaningless for films with a weak pulse; screening was by title, not listening.

**Distributions** (professional 10th percentile, median, 90th percentile; then Bauwerk, torq, Sendoku with their professional percentile in brackets):

| Metric | p10 | median | p90 | Bauwerk | torq | Sendoku |
|---|---|---|---|---|---|---|
| integrated loudness (LUFS) | -21.0 | -15.0 | -10.1 | -14.2 (59) | -14.1 (59) | -14.0 (64) |
| true peak (dBTP) | -5.18 | -0.67 | 0.43 | -1.36 | -0.96 | -1.36 |
| loudness range, EBU LRA (LU) | 2.35 | 5.83 | 11.4 | 3.81 (26) | 4.22 (28) | 3.61 (23) |
| loudest 3 s position (% of length) | 21.1 | 66.2 | 91.0 | 51.7 | 51.7 | 66.0 |
| first third mean 1 s loudness vs integrated (LU) | -2.31 | 1.62 | 3.50 | 0.50 | 1.19 | 2.87 |
| tempo (BPM) | 108 | 123 | 148 | 120 | 120 | 120 |
| pulse strength | 0.085 | 0.37 | 0.61 | 0.36 | 0.47 | 0.52 |
| beat interval variation (CV) | 0.028 | 0.062 | 0.093 | 0.051 | 0.042 | 0.013 (1) |
| onsets per second | 2.08 | 4.02 | 5.64 | 3.63 | 3.00 | 3.40 |
| busiest 2 s window (onsets/s) | 4.90 | 7.00 | 8.10 | 7.00 | 4.50 | 6.50 |
| 2 s density variation (CV) | 0.27 | 0.42 | 0.77 | 0.61 | 0.45 | 0.52 |
| onset strength variation (CV) | 0.39 | 0.49 | 0.58 | 0.58 (88) | 0.72 (98) | 0.68 (98) |
| percussive share | 0.12 | 0.29 | 0.57 | 0.19 | 0.16 | 0.14 |
| energy below 120 Hz | 0.11 | 0.45 | 0.75 | 0.35 | 0.55 | 0.45 |
| energy above 6 kHz | 0.001 | 0.010 | 0.032 | 0.034 (91) | 0.027 (86) | 0.015 (67) |
| spectral centroid, median (Hz) | 982 | 1834 | 2652 | 3035 (98) | 2810 (95) | 2271 (74) |
| 85 % rolloff, median (Hz) | 1714 | 3973 | 5927 | 7494 (100) | 7235 (100) | 5701 (83) |
| brightness movement (CV of 1 s centroid) | 0.19 | 0.30 | 0.49 | 0.36 | 0.43 | 0.49 |
| stereo side share | 0.018 | 0.10 | 0.24 | 0.073 | 0.082 | 0.066 |
| near silences per film | 0 | 0 | 2.2 | 0 | 1 | 2 |
| dips per film | 0 | 4.0 | 19.4 | 1 | 1 | 2 |
| dips per 10 s | 0 | 0.78 | 3.53 | 0.33 | 0.33 | 0.67 |
| silence before first sound (s) | 0 | 0.05 | 0.45 | 0 | 0 | 0 |
| grid offset (share of a 16th) | 0.085 | 0.11 | 0.17 | 0.093 (22) | 0.047 (0) | 0.047 (0) |
| onsets within 25 ms of a 16th | 0.56 | 0.78 | 0.96 | 0.91 | 0.96 | 1.00 (98) |
| onsets with a near identical twin in the film | 0.10 | 0.43 | 0.91 | 0.15 | 0.29 | 0.41 |
| cuts per second | 0.020 | 0.24 | 0.85 | 0.10 | 0.10 | 0.067 |
| onset minus cut, median (ms) | -31.7 | 7.89 | 57.9 | 29.5 | 4.91 | 13.2 |

**Cross film sameness.** AI vs AI (3 pairs): shared sounds median 0.17, profile distance median 1.41 (0.99 to 1.57), tempo within 3 BPM 100 percent. Professional, same maker (188 pairs): 0.05 and 3.76 (2.44 to 5.50), 9 percent. Professional, different makers (8,068 pairs): 0.05 and 4.09 (2.67 to 6.11), 11 percent. Sendoku and torq shared 42 percent of strong transients and sat 0.88 apart; Bauwerk and Sendoku 17 percent and 1.41; Bauwerk and torq 15 percent and 1.60. Only 0.45 percent of the 8,256 professional pairs are as close as the most distant AI pair. A typical professional film's nearest neighbour among the other 128 is 1.70 away (10th percentile 1.25). Same maker films (four Apple Health, six Notion, four Framer, five Tendril) differ as much as films from different studios.

**Cuts.** 2,666 cuts in 116 professional films: average onset strength at the cut 1.18 times baseline, peaking 35 ms after (about 23 ms after hop correction). Per film the cut peak is 1.7 times baseline (p10 1.17, p90 3.9) and lands a median 12 ms after the cut (p10 58 ms before, p90 70 ms after). 72 percent of cuts have an onset within 2 frames against 64 percent by chance. AI: 8 cuts, peak 18.6 times baseline at +12 ms, a duck to 0.5 times baseline in the 150 ms before, and a second spike about 270 ms later (one 8th at 120 BPM). With 8 cuts this AI curve is indicative.

**Dips.** 83 percent of professional films have a dip; 57 percent a re-entry dip (the sound returns at least 6 dB louder). Re-entry dips last a median 0.30 s (0.15 to 0.95), return a median +9.3 dB (6.5 to 15.7), first onset a median 41 ms after (11 to 240). They cluster in the first 10 percent (about one per film per 5 percent slice) and at 90 to 95 percent; even in between. 71 percent of professional films have no near silence. The AI gap: 13.75 s (45.8 percent, frame 825) in all three, returning only 3.6 to 6 dB louder, first onset 13 ms after.

**Starts, ends, density arc.** First second vs integrated: professional median -1.9 LU (p10 -18.6, p90 +3.9); AI -0.2, +0.8, +1.4. Last loud second about 1 s before the end in both (professional p90 5 s ring out). Professional density stays near its median to about 85 percent (4.2 per second at 80 percent, 3.4 at 90 percent); AI films thin from 70 percent (about 2 per second at 80 percent, 0.5 at 90 percent) and all three empty out at 40 to 45 percent. The overall loudness arc (rise, plateau, drop at the end) is the same shape in both.

**Loudest moment.** 16 percent of professional films peak in the first third, 32 percent in the middle, 52 percent in the last third.

**What the data does not support.** The AI films are not too dense, not too loud, not too narrow, and do not repeat their own sounds more than professionals within a film. The "same pops" complaint is about repetition across films.

**Timestamped examples** (times from the start of each YouTube video; "dB" is the 50 ms RMS level averaged over the second before or after):

1. Tendril, Microsoft emojis celebration film, https://www.youtube.com/watch?v=Kh8BZPgpUhc: 0:39.4, a 1.3 s drop of more than 20 dB (62 percent); -30.4 dB before, -16.1 dB after; first onset 51 ms after; density 1.0 per second in the 4 s before, 6.8 after; the loudest second at 0:43.
2. Superhuman, Introducing Superhuman, https://www.youtube.com/watch?v=4XKq7qGnJus: a 0.85 s dip at 0:13.7 (23 percent), -22.7 to -12.4 dB (+10.3), first onset 24 ms after, density 4.2 to 7.0; densest 2 s at 0:26 (9.5 per second), loudest second at 0:50 (84 percent).
3. Stripe, Stripe Sessions 2024, https://www.youtube.com/watch?v=KH0_HM6e66w: a 0.85 s dip at 0:41.4 (38 percent), -34.6 to -22.6 dB; pulse 0.03; 82 cuts, 89 percent with an onset within 2 frames, which is chance (88 percent) for a busy track: cuts carried by texture.
4. Oddfellows, The Blend is near, https://www.youtube.com/watch?v=Oy3-bb2VA7w: a 0.7 s dip at 0:48.3, -32.9 to -11.1 dB (+21.8); loudest second at 2:16 (76 percent).
5. Uber, Bringing our new look to life, https://www.youtube.com/watch?v=axjXNEordH8: a 0.2 s dip at 0:27.1 (48 percent), then -26.1 to -8.1 dB (+18); loudest second at 0:31; LRA 13.3 LU.
6. Apple, Introducing AirTag (Couch), https://www.youtube.com/watch?v=dJMUYP88lrs: a 0.5 s dip at 0:17.6, -30.4 to -17.4 dB, density 1.5 to 3.5; loudest second early at 0:22 (33 percent); LRA 17.6 LU.
7. Notion, Introducing Notion AI, https://www.youtube.com/watch?v=FElBbgnNtVA: a 0.3 s dip at 1:14.2 (88 percent), -46.5 to -21.2 dB (+25), density 4.2 to 7.7; densest 2 s right after (8.0 per second, film median 3.5).
8. Perplexity, Introducing Comet, https://www.youtube.com/watch?v=YeldJ4UezDQ: median density 1.0 per second with one burst of 6.5 at 0:44; the loudest second at 0:37 is 15.4 LU over integrated; a 1.5 s dip at 1:03.6 (88 percent) into the end card.
9. Raycast, New Raycast. Coming 2026, https://www.youtube.com/watch?v=Mi173xGb0ZA: median density 0.8 per second, one dense window of 5.5 at 0:12; a 0.35 s dip at 0:03.2 then +16 dB; percussive share 0.03, LRA 13.6 LU.
10. Linear, Introducing Linear Agent, https://www.youtube.com/watch?v=mRql2VJ99gM: -28.9 LUFS, LRA 17.6 LU; the loudest second at 0:04 (8 percent), 21.5 LU over integrated: one opening impact, then a near silent film (percussive share 0.02, low end share 0.86).
11. Dropbox, Dash: AI that understands you, https://www.youtube.com/watch?v=8Ab9EyV7DGY: a 0.75 s dip at 0:15.4 (15 percent), +16.8 dB; loudest second at 1:24 (83 percent).
12. Microsoft Design, Next generation of OneDrive, https://www.youtube.com/watch?v=DzXBdc8Dfmg: a 0.95 s dip at 0:08.8 (15 percent), -20.1 to -12.1 dB, density 0.7 to 2.8.
13. Tendril, Beauty and science reel, https://www.youtube.com/watch?v=bdsJeK22w4w: a 1.9 s dip at 0:26.9 (37 percent), +23.7 dB, density 0.7 to 1.3: the return is a swell, not hits.
14. Wise, Meet the new Wise design system, https://www.youtube.com/watch?v=x59J0l2EjAs: 70 cuts, 97 percent on an onset (chance 85), median offset -2 ms: cut to its own music; a 0.35 s dip at 0:12.2, +15 dB.
15. Apple, Introducing iPhone 15 Pro, https://www.youtube.com/watch?v=wqcjKkyuoZk: 30 cuts, 83 percent on an onset against 43 percent chance, median +14 ms; loudest second at the very end (96 percent).
16. ManvsMachine, Versus, https://www.youtube.com/watch?v=1ORKoaC3TlI: 32 cuts, 44 percent on an onset against 20 percent chance, median -20 ms; percussive share 0.05, low end 0.86, LRA 12.5 LU: only some cuts get a hit.
17. Samsung, One UI 5 introduction film, https://www.youtube.com/watch?v=Rb9PvLhe9ok: a 0.15 s dip at 0:12.3, -41.8 to -10.5 dB (+31), then 1.6 s to the next onset: the re-entry is a sustained chord.
18. Nothing, Phone (3): Come to play, https://www.youtube.com/watch?v=MHGQRnvE9GQ: side share 0.70 (widest in the set, median 0.10), LRA 16 LU; after a 0.45 s dip at 0:18.9, 7.5 s with no new onset.
19. Monzo, Money feels different on Monzo, https://www.youtube.com/watch?v=pOUs63Qc80k: pulse 0.00; 45 cuts, 53 percent on an onset against 33 percent chance, median +39 ms: effects follow the picture without a grid; a 1.25 s dip opens the film.
20. Ordinary Folk, Ordinary Folk ident, https://www.youtube.com/watch?v=EFdAOiNXUKY: a 0.95 s dip at 0:02.6, density 0.8 to 3.0, LRA 10.7 LU in 36 s.
21. Bauwerk, torq and Sendoku: the gap at 0:13.75 in all three (0.25, 0.2, 0.2 s), each followed by an onset 13 ms after; Sendoku adds a 0.45 s silence at 0:21.55; 120.2 BPM; -14.2, -14.1, -14.0 LUFS; -1.36, -0.96, -1.36 dBTP; their 2 s density curves dip at the same window (12 to 14 s).

**The 18 rules the note derives** (now the checks in `sound.md`, section 12): measure every score's profile against every earlier one and demand a distance of at least 2.5 (the kit's `fingerprint.py` uses 2.67, the professional 10th percentile itself); never reuse a transient across films (under 10 percent shared); do not sit every event on the grid (about 0.1 of a 16th, 20 to 40 percent off grid); make about one film in three unmetered; spread the tempo (105 to 150, not the last three films' tempos); darken the mix (centroid 1.0 to 2.6 kHz, under about 2 percent above 6 kHz); use dips, not dead air (0.5 to 3.5 per 10 s, one re-entry of +6 to +16 dB, first onset 10 to 250 ms after, true silence once or twice); put dips where the film breathes and move them; move the big moment; start below the body (2 to 18 LU under, up to 0.5 s silence); widen the range (LRA 5 to 11, vary integrated level between films); even out the hits (strength variation 0.4 to 0.6, percussive share 0.2 to 0.5); mark some cuts, not all (whooshes may lead by 2 to 4 frames, impacts on or 1 to 2 frames after); no duck before every hit; shape density with contrast (2 to 9 times, sparse near 1 per second, bursts 6 to 9); vary width by film and section (0.02 to 0.24); vary the ending (1 s, or 5 s ring out); keep the film alive until the end card (density near median to 85 percent). The margins of 5 points for dip position and 10 points for the loudest moment in `sound.md` are **(heuristic)**.

## 2. Sound types and their durations

- Motion graphics sound has "unique challenges due to their short, abstract nature" (Adobe Research, MoSound, CHI 2026): https://research.adobe.com/publication/mosound-an-interactive-tool-for-generative-sound-design-in-motion-graphics/
- Whoosh duration by event: quick UI swipes and fast cuts 0.25 to 0.5 s, general 0.5 to 1 s, big titles and slow push ins 1 s or more; the loudest point on the cut. Light airy whooshes for text and menus, dark, distorted, low passed ones for heavy objects: https://violetrecording.com/how-to-make-whoosh-sounds/
- A layered whoosh has air, texture, tonal and landing layers; the landing layer only "when the object visibly stops, attaches, or appears" (snippet): https://aishasound.com/blog/whoosh-sound-design-a-practical-guide
- A whoosh follows speed, mass, direction, distance and stopping point (snippet): https://sonilo.com/ai-music/whoosh-sound-effect-guide
- Risers: 1 to 2 beats for a quick lift, one to several bars for a build, 4 to 8 bars into a main drop; peak on beat one of the new section, then cut or duck; a downlifter releases tension: https://violetrecording.com/how-to-make-risers-and-sweeps/
- UI sound durations: click 30 to 120 ms, hover 15 to 45 ms, navigation 80 to 450 ms, success 100 to 300 ms, error 150 to 600 ms, delete 80 to 300 ms, loading 20 to 200 ms: https://ui-sounds.com/ . Other vendors: taps 80 to 150 ms, hovers 120 to 200 ms (conflicts on hover), notifications 200 to 600 ms, transitions 300 to 1000 ms (snippets): https://sfxengine.com/blog/sound-effects-click , https://sfxengine.com/blog/best-practices-for-game-ui-sounds
- UI roles: feedback, decoration, hero sounds, notifications; sound never the only carrier of essential information (snippet): https://designcode.io/ui-design-handbook-ui-sound-design
- UI set roles (press crisp, hover a tick, confirm rising and bright, cancel softer, error lower and blunt, notification a chime; all brief and quiet): https://voidless.dev/tutorials/sound-effects/generate-ui-sound-effects
- Navigation smallest, select bigger, confirm biggest (snippet): https://sfxengine.com/blog/best-practices-for-game-ui-sounds
- Rubik's cube spot: a warm bed, swirly synths pitched to follow the spins, rubbery stretches rising and falling with the morph, a wave growing as the camera nears: https://krotos.studio/blog/sound-effects-motion-graphics-tips
- Braam: low brass, synth and sub, distorted; shares the bass with the music, so both at full weight "turns to mud" (snippets): https://sounddesign.irpr.agency/glossary/braam/ , https://vi-control.net/community/threads/making-braams.121447/
- The event to sound map in `sound.md` section 3 is the research's synthesis of these **(heuristic)**.

## 3. How sounds are built

- Whoosh: a filter sweep on noise over about 0.8 s, cutoff rising then falling; fast sweep sharp, slow sweep heavy; swell into the centre; pitch rising lifts, falling settles; Doppler; pan across; short reverb; pink or filtered noise over white: https://violetrecording.com/how-to-make-whoosh-sounds/
- Whoosh layers with complementary characters; bigger objects lower and slower (snippets): https://sound.krotosaudio.com/whoosh-sound-effects/ ; carve frequencies and glue with compression on one bus: https://krotos.studio/blog/whoosh-sound-effects-krotos-studio , https://pixflow.net/blog/cinematic-whoosh-sound-effects/
- Risers: noise through a band or high pass opening; pitch risers on saws; Shepard risers; an accelerating, not linear, curve; widen at the peak; high pass to keep energy out below 100 Hz; one primary motion: https://violetrecording.com/how-to-make-risers-and-sweeps/ . Noise about -6 dB under the tonal riser (snippet): https://unison.audio/how-to-create-risers/ . Eight unison voices for width (snippet): https://soundbridge.io/en/create-a-perfect-white-noise-riser
- Impacts: transient, body, sub, tail; one layer owns the sub; align on one transient; small shifts change size and punch; a thin hit lacks a layer (snippets): https://violetrecording.com/how-to-make-impact-sounds/ , https://morphic.com/resources/how-to/how-to-layer-sound-effects , https://sounddesign.irpr.agency/glossary/layering/ . Quiet before the impact, headroom: https://sounddesign.irpr.agency/guides/how-to-add-weight-to-impacts/
- Sub drops: a sine near 50 Hz with phase reset, a short noise click (snippet): https://forum.ableton.com/viewtopic.php?p=903916 ; pitch envelope 1 to 2 st over 10 to 30 ms or 2 to 4 st over 20 to 50 ms, amp decay 2 to 4 s (snippet): https://www.audeobox.com/learn/fl-studio/how-to-make-808s-in-fl-studio/ ; trap kick 20 to 25 st (snippet): https://soundbridge.io/making-trap-kicks ; too slow a drop is a "pew", a clean sine vanishes on small speakers (snippets): https://violetrecording.com/how-to-design-an-808/ ; Attack Magazine's 808 boom chain: https://www.attackmagazine.com/technique/synth-secrets/808-style-booms/
- UI sounds in Python, exact parameters: 2 ms linear attack ("must not be zero"), exponential release, 3 ms fade to zero, glides with `np.geomspace`, soft square (3rd at 1/3, 5th at 1/5), DC removal, peak at -3 dBFS, harmonics under 8 kHz; click = noise low passed at 4 kHz (12 ms, 0.5 ms attack, 4 ms release, gain 0.6) plus a sine 1800 to 1200 Hz (40 ms, gain 0.5); hover 1400 to 1500 Hz, 50 ms; confirm 660 Hz 70 ms then 990 Hz 160 ms; cancel 520 Hz then 350 to 330 Hz; text blips 880 Hz plus 0, 2, 4 st, 45 ms: https://yetiancai.itch.io/cozy-ui-sfx-190/devlog/1730801/synthesizing-game-ui-sound-effects-with-code
- Taps, swishes and page turns as band passed noise so they have no pitch to clash: https://heyheythere.itch.io/soft-ui-sfx/devlog/1685319/ui-sounds-that-dont-clash-pitch-them-all-from-one-pentatonic-scale
- Tap EQ: ease 3 to 6 kHz, cut below 200 Hz (vendor snippets): https://sfxengine.com/blog/best-practices-for-game-ui-sounds , https://elements.envato.com/learn/ui-sound-design-ai
- Modal synthesis (sums of decaying sinusoids; only a few of hundreds of modes matter; evaluated for ceramic, glass, metal, wood): https://www.cs.ubc.ca/~kevinlb/LCI/01/vandendoel-020809.html , https://www.smc2019.uma.es/articles/P1/P1_05_SMC2019_paper.pdf
- Keep most effects mono in busy projects so they can be panned with the action: https://krotos.studio/blog/sound-effects-motion-graphics-tips
- **(heuristic)**: the whoosh peak at 55 to 65 percent and its cutoff values, the reverse swell recipe, the sub drop glide 80 to 110 Hz down to 30 to 45 Hz, the braam numbers, tonal hit FM ratios, and every glitch, shimmer, data chatter and bed recipe. No source gave recipes for those.
- `tau = d20 / 2.3`: arithmetic (an exponential decay reaches -20 dB at ln(10) times tau), and the cause of the first kit's over long effects (section 14).

## 4. Material, size and pitch

- Bigger objects get lower, slower whooshes (snippet): https://sound.krotosaudio.com/whoosh-sound-effects/
- Material brightness "from wood to glass, from nylon to steel" as a primary modal control: https://modulargrid.net/e/modules/view/4606 ; modal synthesis of ceramic, glass, metal and wood: https://www.smc2019.uma.es/articles/P1/P1_05_SMC2019_paper.pdf
- One pentatonic for every tonal UI sound, so no minor seconds, tritones or major sevenths; confirm as steps (0, 2, 4); toggle as a rising pair, off as the same pair falling; error as a note plus a semitone ("the clash is the message"): https://heyheythere.itch.io/soft-ui-sfx/devlog/1685319/ui-sounds-that-dont-clash-pitch-them-all-from-one-pentatonic-scale
- Confirm up a fifth, cancel down: "Players read the direction without thinking about it": https://yetiancai.itch.io/cozy-ui-sfx-190/devlog/1730801/synthesizing-game-ui-sound-effects-with-code
- **(heuristic)**: the size factor mapping (1200 to 150 Hz, 60 to 600 ms, sub from s = 0.4), and the material table's partials and decay times (standard acoustics, not sourced to motion graphics practice).

## 5. Sync and tolerances

- ITU-R BT.1359-1 (1998): detectable at about +45 ms (audio leading) to -125 ms (lagging); acceptable about +90 to -185 ms: https://en.wikipedia.org/wiki/Audio-to-video_synchronization , https://www.tvtechnology.com/opinions/av-synchronization-how-bad-is-bad , https://www.forasoft.com/learn/audio-for-video/articles-audio/lip-sync-itu-r-bt-1359-tolerance-windows
- EBU R37: +40 ms to -60 ms end to end (framing disputed between sources): https://en.wikipedia.org/wiki/Audio-to-video_synchronization
- Netflix QC: sync effects 1 frame or less off are minor, 2 or more frames off is an issue (snippet; page login walled): https://backlothelp.netflix.com/hc/en-us/articles/115000533952-Sync-Effects
- "Sound early is always worse than sound late" (forum): https://gearspace.com/threads/sync-issues.1192176/ ; "a hair early often reads better than late", the visual peak often comes 1 to 2 frames after contact: https://morphic.com/resources/how-to/how-to-sync-sound-effects-to-video
- Impacts on the cut ("even 50 ms early reads as sloppy"); a 0.5 s transition gets a 400 to 500 ms whoosh starting just before; a riser about a second ahead of the key claim; do not sound every join: https://zellahq.com/blog/sound-design-at-cuts-whoosh-impact-riser/
- Whoosh peak on the first frame of the new shot; wholly after the cut "always feels late": https://morphic.com/resources/sounds/transition-sound-effects
- Risers and reverse whooshes stop dead where the moment lands; the edit lands in the silence after: https://add.app/sound-effects/sound-design-for-trailers-hits-rises-drones-pulses/ , https://violetrecording.com/sound-design-for-trailers/
- Align the strongest part with the frame the animation finishes or turns: https://wearefevr.com/sound-design-for-motion-graphics
- Trailer practice: audio starts before the previous scene ends; hits on title slams and edits; whooshes on dips to black, dissolves, flares: https://www.derek-lieu.com/blog/2022/1/17/secrets-to-trailer-sound-design
- Create the audio first for motion graphics: https://larryjordan.com/articles/create-the-audio-first-for-a-motion-graphic-video/
- J cut, L cut, prelap: https://en.wikipedia.org/wiki/J_cut , https://en.wikipedia.org/wiki/Prelap
- Professional cut timing measured: section 1.
- **(heuristic)**: the per type frame table in `sound.md` section 6 is derived from these, not published as a table.

## 6. Rhythm, tempo and density

- Murch's Rule of Six: emotion 51 percent, story 23, rhythm 10, eye trace 7, 2D plane 5, 3D space 4: https://nofilmschool.com/2016/11/6-rules-good-cutting-according-oscar-winning-editor-walter-murch
- 26,025 video ads plus three experiments: fast music raises purchase intent for promotion focused ads only, through time pressure: https://thearf.org/access-knowledge-2/publications/journal-of-advertising-research/when-fast-music-makes-ads-more-persuasive-and-when-it-doesnt/ ; fast music raised arousal and purchase intent for a restaurant ad: https://ideas.repec.org/a/eee/joreco/v63y2021ics0969698921002964.html ; slow tempo gave higher recall in a thesis: https://figshare.le.ac.uk/articles/thesis/Cognitive_and_affective_responses_to_music_in_ads_and_service_environments/10153406 ; "fast" is above about 94 BPM (Milliman 1982, cited secondhand): https://www.immerse.education/wp-content/uploads/2024/04/Effects-of-fast-tempo-background-music.pdf
- Do not sound every cut; in a video cutting every 4 to 5 s that makes a percussion track: https://zellahq.com/blog/sound-design-at-cuts-whoosh-impact-riser/
- Trailers carry a dozen SFX tracks, but quantity is not the skill: https://www.derek-lieu.com/blog/2022/1/17/secrets-to-trailer-sound-design
- Professional tempo spread, pulse, density and density contrast: section 1. No source gave BPM by mood for ads, edits on downbeats, or hits per second; the "one accented effect per 1 to 2 s" ceiling is **(heuristic)**.

## 7. Silence, dips and dynamics

- A braam is "only huge because of the beat of near-silence right before it": https://add.app/sound-effects/sound-design-for-trailers-hits-rises-drones-pulses/ , https://tonalchaostrailers.com/blog/sound-design-for-film-trailers/
- A hit suits a shot that needs weight, silence one that needs air; a swell cut at its loudest: https://morphic.com/resources/sounds/transition-sound-effects
- "Without quiet, your loud moments have nothing to contrast against": https://violetrecording.com/sound-design-for-trailers/
- EBU R128 s1 (2020) caps short term loudness at -18 LUFS on a -23 LUFS ad, so contrast must come from going quieter: https://tech.ebu.ch/docs/r/r128s1.pdf
- Over compressing a commercial makes it sound smaller once normalised: https://gearspace.com/board/post-production-forum/1276450-mix-bus-processing-tv-commercials.html
- How often, how long, how deep and where professionals dip, and where they peak: section 1 (measured). No external source gave silence durations before reveals.

## 8. Balance and ducking

- Krotos: music about -20 dB, footsteps and environment about -20 dB, hits and cracks -20 to -10 dB; music about -14 LUFS mastered, TV -23, film about -27: https://krotos.studio/blog/how-to-balance-music-and-sound-effects
- Music under dialogue -18 to -25 dB, nearer -10 with no speech; SFX -12 to -18 dB (snippet): https://pixflow.net/blog/?p=92478
- Music 18 to 20 dB under speech, SFX 12 to 18 dB under: https://pureaudioinsight.com/blogs/content-production/background-music-volume-how-loud-should-it-be ; featured cut sounds about -6 dB under speech: https://zellahq.com/blog/sound-design-at-cuts-whoosh-impact-riser/
- Ducking: 6 to 10 dB to start (6 to 12 gentle), attack 30 to 80 ms, release 300 to 500 ms (400 to 700 if pumping); over ducking by 15 to 20 dB is the most common mistake; plugin defaults 10 ms attack, 200 to 500 ms release, 200 ms hold: https://composer-docs.vindral.com/operators/operators-sidechain-ducking.html , https://develop.unitedplugins.com/VoxDucker/documentation , https://www.capcut.com/create/audio-ducking-for-clear-dialogue-in-video , https://davinciresolveclub.com/davinci-resolve-audio-ducking.md
- Broadcast mixers set the voice to spec first and mostly automate faders, with a couple of dB of voice keyed ducking: https://gearspace.com/board/post-production-forum/1276450-mix-bus-processing-tv-commercials.html
- EQ carving: 1200 to 2400 Hz for consonants, 2 to 5 kHz presence, 600 Hz to 1.1 kHz nasal, small 1 to 3 dB moves: https://www.dvinfo.net/forum/archive/index.php/t-41476.html , https://davinciresolveclub.com/fairlight-eq-dialogue.md , https://www.production-expert.com/production-expert-1/should-you-to-carve-eq-when-mixing
- The torq film's effects bus buried its intro at 1.0 and sat right at 0.5 (`lessons.md`, measured on the film).
- **(heuristic)**: the level table in `sound.md` section 11, the no voiceover ducking (2 to 4 dB, 1 to 10 ms, 100 to 250 ms, extrapolated from the voice numbers), the frequency slots, stereo placement and shared reverb (common practice, unsourced).

## 9. Variation and humanization

- The machine gun effect: one sample repeated on consecutive notes (snippet): https://www.kvraudio.com/forum/viewtopic.php?p=7231754 ; even a slight random pitch envelope reduces it "drastically", whole sound pitch shift less than expected (snippet, anecdotal): https://www.kvraudio.com/forum/viewtopic.php?p=7232081
- Unity Audio Random Container (read in full): volume and pitch randomisation as min and max (pitch in cents), Sequential, Shuffle (no repeats until all have played), Random; "Avoid Repeating Last"; randomised trigger timing: https://docs.unity.com/en-us/engine/6000.3/manual/audio/random-container/ui.md
- HALion "Random Exclusive" (no variation twice in a row) (snippet): https://steinberg.help/halion/v7/en/halion/topics/editing_programs_and_layers/sound_editor_variation_groups_section_r.html ; SFZ `pitch_random` in cents, a ±20 cent humanise (snippet): https://sfzformat.com/opcodes/tune_random ; Wwise example -25 cents (snippet): https://audiokinetic.com/qa/2909/random-pitch-how-is-it-applied-to-children-containers
- Footsteps in games: pitch factor 0.85 to 1.15 or 1 ± 0.1, about ±170 to ±280 cents (snippet): https://discussions.unity.com/t/foot-step-audio-randomize-pitch/26725 ; "widen pitch to ±15% to confirm it's working, then dial it back" (snippet): https://uhiyama-lab.com/en/notes/ue/sound-cue-vs-sound-wave-best-practices/ ; per band random pitch for timbre variation: https://www.kvraudio.com/product/randrobin-by-fanan-team
- Humanise: Logic about ±10 ticks of position and ±10 velocity; downbeats higher, offbeats lower, hats the most variation; "unvaried velocity values can be one of the main culprits": https://splice.com/blog/humanize-your-drums/ , https://unison.audio/how-to-humanize-midi/
- Most of 35 listeners could not reliably hear subtle humanise timing (snippet): https://www.academia.edu/49227033/Timing_Forget_the_Timing
- Frühauf, Kopiez and Platz (2013): ±15 and ±25 ms shifts rated lower than quantised, early worse than late (snippet): https://labs.sonicfield.org/library/music-on-the-timing-grid-the-influence-of-microtiming-on-the-perceived-groove-qu ; Davies et al. (2013): systematic microtiming lowered groove ratings except a simple shuffle (snippet): https://repositorio.inesctec.pt/items/38083482-243e-4090-bfa6-735d148ee1ff ; Skaansar, Laeng and Danielsen (2019): ±80 ms asynchronies raised mental effort (snippet): https://sonicfield.org/library/microtiming-and-mental-effort ; Frontiers in Psychology (2016): quantised and original microtiming rated equally (snippet): https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2016.01487/pdf
- Professional grid offset and on grid share, and cross film transient sharing: section 1 (measured).
- **(heuristic)**: pools of 3 to 6, avoid last 1 to 2, pitch jitter 100 to 200 cents for noisy sounds and 25 to 50 for tonal, level 1 to 3 dB, the decaying series for staggers (1 to 3 dB per step), and the reading that the professional off grid share comes mostly from picture led effects (consistent with the studies above, not measured directly).

## 10. Loudness targets

- EBU R128 s1 (August 2020, short form): -23.0 LUFS (±0.2 LU QC), short term max -18.0 LUFS, -1 dBTP, no LRA for short form: https://tech.ebu.ch/docs/r/r128s1.pdf
- ATSC A/85 -24 LKFS, -2 dBTP (CALM Act); Netflix -27 LKFS dialogue gated (±2 LU), -2 dBTP; YouTube -14 LUFS, -1 dBTP, turn down only (a -10 LUFS upload is lowered 4 dB); Spotify -14 (Loud -11, Quiet -19), Apple Music -16, AES TD1008 -16 music, -18 speech, -17 mixed; TikTok, Instagram and Meta publish no target; creators often master -10 to -12 for phones: https://www.forasoft.com/learn/audio-for-video/articles-audio/lufs-targets-per-platform-2026 , https://en.wikipedia.org/wiki/Audio_normalization
- Conflicting vendor claims for social (-10 to -16): https://opus.pro/blog/best-loudness-normalizers , https://openclip.app/learn/audio-normalization
- Apple app previews: stereo, 256 kbps AAC (H.264) or PCM or AAC (ProRes 422 HQ), 44.1 or 48 kHz, all tracks enabled, 15 to 30 s, max 30 fps, 500 MB; no loudness target: https://developer.apple.com/help/app-store-connect/reference/app-information/app-preview-specifications
- Cinema ads about 82 dB Leq(m): https://duc.avid.com/archive/index.php/t-280573.html
- Inferences: Google Play previews follow YouTube's -14 (they are YouTube videos); -1 dBTP minimum for lossy encoding, -2 safer. The professional films' spread of integrated loudness (-21 to -10 LUFS) is in section 1. "A more dynamic master that lands slightly under the target loses little" is **(heuristic)**: YouTube turns down only, so it plays slightly quieter, which a wider range offsets.

## 11. Small speakers and muted viewing

- The missing fundamental: pitch is heard from harmonics when the speaker cannot play the fundamental: https://en.wikipedia.org/wiki/Missing_fundamental
- Small speakers cannot resolve lows; harmonic synthesis extends perceived bass about two octaves; MaxxBass, multiband saturation: https://www.production-expert.com/production-expert-1/how-to-make-sure-bass-is-heard-on-small-speaker-devices
- Duplicate the bass, saturate, high pass, blend; audible phone "low end" about 110 to 800 Hz (forum, anecdotal): https://blog.faderpro.com/mixing/mixing-bass-for-all-speaker-sizes/
- Muted viewing (secondhand, 2016 to 2019): 69 percent sound off in public, 25 percent in private, 80 percent more likely to finish with captions (Verizon Media and Publicis): https://www.rev.com/blog/speech-to-text-accessibility/top-7-places-you-need-to-watch-videos-on-mute ; Facebook 85 percent without sound (Digiday via Hypebot): https://www.hypebot.com/85-watch-your-videos-with-the-sound-off-plus-what-you-can-do-about-it.md
- The first kit's impact at 95 to 98 percent of its energy under 120 Hz: section 14 (measured).
- **(heuristic)**: the 150 Hz phone cut off (plausible, unmeasured), the 120 to 500 Hz knock and 2 to 5 kHz click on every hit, the mono fold and 150 to 200 Hz high pass check.

## 12. Why AI and template sound reads as generic

- Slendebroek and Metaxa, "The Algorithmic Flattening of Sound", AIES 2026: Suno and Lyria 3 against human corpora on 72 MIR features, 4 genres, 100 tracks per system and genre; reduced variation in rhythm and timing, timbre and dynamics; neither follows prompts closely; a standard classifier separates AI from human tracks near perfectly: https://ojs.aaai.org/index.php/AIES/article/view/43312
- Listeners could not tell random Suno and human pairs apart, but could with highly similar pairs (snippet): https://arxiv.org/html/2509.25601v1
- Generic stock stingers, no sub design, no dynamic contrast make trailers flat (snippet): https://sounddesign.irpr.agency/solutions/weak-trailer-impact/ ; the braam as a cliche through overuse (snippet): https://sounddesign.irpr.agency/glossary/braam/ ; three even low impacts read as controlled (snippet): https://morphic.com/resources/sounds/cinematic-sound-effects
- A sound can be exciting alone and wrong for the moment (snippet): https://pixflow.net/blog/cinematic-whoosh-sound-effects/
- The AI "spaghetti crunch": a sound from a statistical default, not the material (snippet): https://getcoai.com/news/sora-vs-veo-3-fight-openai-readies-sora-2-with-audio-to-challenge-google/
- Corporate music's "most common and egregious isn't-life-just-awesome instrument is the ukulele" (snippet): https://boingboing.net/2019/10/23/how-to-make-bland-soulless-co.html
- "Less is more", hierarchy and negative space in animation sound (snippet): https://publications.scss.tcd.ie/theses/diss/2021/TCD-SCSS-DISSERTATION-2021-015.pdf ; elements appearing, moving, disappearing or changing as places for subtle effects (snippet): https://www.newscaststudio.com/2022/12/13/sound-design-tips-news-promos/
- The first mgpro films' own sameness: section 1 (measured). No source quantified "120 BPM four on the floor" as the corporate default; in this skill the evidence is the skill's own three films.
- **(heuristic)**: the hierarchy of 1 hero, 2 to 4 support and the rest unscored per sequence is the research's synthesis.

## 13. Studios, case studies and sonic identity

- Antfood: involved "from concept and pre-production"; music, sound design and post as one discipline; 30, 50 or 100 ideas, then narrowing: https://motionographer.com/2018/09/05/the-other-half-with-antfood/
- Wes Slover (Sono Sanctus, Sanctus Audio): start from what the audio must do; avoid temp tracks ("demo love can be really hard to break"); custom score for arcs with hit moments, a library track for simple energy; a sonic identity extends from the logo into UX sounds: https://www.bythebooth.com/insights/creative-tangent-wesley-slover-sound-the-invisible-brand-layer
- Apple iMac Pro (BUCK, Antfood): "tightly scored music and sound design" to fast, erratic animation; ADC 2019 Bronze, sound design: https://antfood.com/work/apple-imac
- Apple "Start Up: 45 Years of Apple Sounds" (D&AD 2022): a track built only from Apple device sounds, "No fillers": https://dandad.org/awards/professional/2022/236414/event-opener-start-up-45-years-of-apple-sounds
- Google Design "Design and Material Explorations" (Zelig Sound, D&AD Yellow Pencil 2023): "blurring the lines between music and sound design": https://dandad.org/awards/professional/2023/236787/google-design-design-material-explorations
- YouTube sonic logo (Antfood with BUCK): about 3 s, a "deep dive" bass, an upward glissando, two notes for two syllables, a champagne pop, a door unlock, a major 7th pad; a clear beginning and end: https://www.antfood.com/labs/crafting-youtubes-first-sonic-brand
- Netflix "ta-dum" (Lon Bender): 20 to 30 options, a ring knocked on a cabinet: https://www.20k.org/episodes/netflix
- Mastercard: a 30 s melody, a 3 s version and a 1.6 s burst: https://fortune.com/2019/09/07/sonic-branding-logo-audio-sound-mastercard
- Ordinary Folk "Instrumental Visual Poem": music first, a four section "sound chart", shapes animated to it: https://www.stashmedia.tv/exploring-the-dance-of-sound-and-imagery
- Brabantia's sonic brand from its own products (snippet): https://www.brabantia.com/int_en/inspiration/the-sound-of-brabantia/
- No public sound credits, BPM, keys or SFX counts were found for Stripe, Linear, Notion, Vercel, Raycast, Arc, Framer, Airbnb or Duolingo films; do not invent them.

## 14. The CC0 library and the first synthesizer (measured)

Source: `sfx/ANALYSIS.md`, `sfx/CATALOG.md`, `sfx/catalog.json`, `sfx/synth.json`, made by `templates/kit/audio/sfx_catalog.py` over 1126 CC0 sounds and the 43 effects of the first `sfx.py`.

- Per category ranges (25th to 75th percentile): clicks 94 to 308 ms long but d20 8 to 26 ms, centroid 1.9 to 5.9 kHz; pops d20 16 to 39 ms, centroid 740 to 3250 Hz, 74 percent tonal; whooshes 94 to 506 ms, centroid 260 to 3200 Hz; impacts d20 17 to 71 ms, centroid 200 to 1000 Hz; risers 262 to 520 ms; bells d20 67 to 240 ms.
- Good against cheap: a good UI click is 7 to 60 ms with a d20 of 4 to 18 ms, attack under 1 to 3 ms, centroid 1.9 to 4.6 kHz with under 10 percent below 500 Hz, often falling 10 to 14 st in 40 ms; a cheap one is 200 to 600 ms with several transients, a slow attack, a -44 dB noise floor and 20 to 70 percent above 6 kHz. A soft pop is a tone on F#5 to B5, 70 to 105 ms; a harsh one is noise with a 16 st bend and clipped samples. Fast swishes are 60 to 160 ms, low (190 to 600 Hz) with a whistle; heavy swings 290 to 510 ms, low and wide; airy designed whooshes 0.3 to 1.1 s, centroid 5 to 13 kHz.
- The first synthesizer's faults: everything rang about ten times too long (a decay constant used as the length: `blip` d20 166 to 413 ms against 13 to 35 ms, `chime` 430 to 690 against 190 to 290, `tick` 19 against 4 to 9); every tonal effect a pure tone (noisiness 0.00 to 0.01 against 0.05 to 0.3); 28 of 43 flat in pitch; 33 of 43 at width 0; the click 77 to 79 percent body at 380 Hz; the impact 95 to 98 percent under 120 Hz with a d20 of 179 to 469 ms (library heavy hits keep 22 to 33 percent in 120 to 500 Hz and drop 20 dB in 31 to 55 ms); the whoosh 0.41 s of hiss whatever the move; the five characters barely different; `tap`, `place`, `blip`, `land`, `block`, `card` and `tier` all sent to one blip. What was in range: attacks of 2 to 4 ms, the riser's hard stop, levels.

## 14b. What the reworked kit measured (measured, not heard)

Source: `templates/kit/audio/CHANGES.txt` (27 October 2026).

- 665 of 686 measures of 152 effect renders (every job in every character) sit inside the library ranges of `sfx/ANALYSIS.md` section 4 (`sfx_catalog.py --synth-only --check`). Before and after: blip d20 166 to 413 ms, now 19 to 29; tick 19, now 5 to 7; click 26 to 27, now 6 to 10, with the 120 to 500 Hz share from 77 percent to 0; success 432 to 692, now 199 to 284; impact 95 to 98 percent sub with d20 179 to 469, now 70 to 79 percent sub, 20 to 29 percent in 120 to 500 Hz, d20 20 to 47. Pitch movement: 28 of 43 renders flat before, 58 of 152 now.
- Cuts on bar downbeats measure 3 to 9 times baseline from the music alone, with no effect. This is why only structural cuts sit on downbeats.
- A 0.57 s gap before the hero cut made it read 27 times baseline; the kit's dips are about an eighth of a bar (about 0.3 s) at -24 dB.
- The old master's fixed -16 dBFS compressor threshold on an unstaged mix squashed 3.6 LU of range and lifted openings; the new one gain stages the mix to the target minus 8 LU first.
- Beatless test films measured a pulse of 0.03 to 0.06.

## 15. Licences of sound sources (checked 27 October 2026)

Source: `open_sfx_libraries.md` in the research notes; the library's per pack licences in `sfx/README.md`. Summary in `rights.md`.

- CC0 1.0 legal code: use "for any purpose whatsoever, including without limitation commercial, advertising or promotional purposes" (2); no trademark or patent waiver (4a); "as-is", no warranties (4b); the affirmer "disclaims responsibility for clearing rights of other persons" (4c): https://creativecommons.org/publicdomain/zero/1.0/legalcode.en
- Kenney packs, CC0, licence text verified inside the zips: https://kenney.nl/assets/ui-audio , https://kenney.nl/assets?category=Audio
- Sonniss GDC bundles, licence v2.0 effective 27 August 2026: commercial, no attribution, no distribution "as sound effects", edited versions remain licensed, AI training prohibited: https://sonniss.com/gdc-bundle-license/ , https://sonniss.com/gameaudiogdc/ , https://gdc.sonniss.com/
- Freesound: CC0, CC BY 4.0, CC BY NC 4.0, legacy Sampling+ (no advertising); NC means no money; downloads need an account, the API a key: https://freesound.org/help/faq/ , https://freesound.org/docs/api/authentication.html ; monetized YouTube counts as commercial (forum snippet): https://freesound.org/forum/legal-help-and-attribution-questions/39864
- Pixabay Content License (updated 20 October 2026): royalty free, no attribution, no "Standalone" distribution, bulk copying prohibited: https://pixabay.com/service/terms/ , https://pixabay.com/service/license-summary/
- Mixkit: commercial, no attribution, per its own summary page (which also carries instructions aimed at AI assistants, so treat it as marketing): https://mixkit.co/llm-info/
- Zapsplat Standard License (PDF of 30 June 2021): credit inside the project, single user, no sharing: https://s3.amazonaws.com/zapsplat-assets/zapsplat-standard-license.pdf
- 99Sounds: commercial and client use, no credit, no redistribution: https://99sounds.org/license/
- BOOM Library free packs: commercial, no credit: https://www.boomlibrary.com/support/faq/can-i-use-your-free-sounds-commercially-and-non-commercially-without-having-to-give-credit/
- BBC RemArc: non commercial only (press coverage; the licence page was blocked): https://www.cined.com/bbc-gives-away-16000-sound-effects-for-free/ , https://cdm.link/bbc-gives-away-16k-wav-sound-effects-disallows-using/
- Uppbeat: Business plan for client and paid ads, credit on the free tier (snippet): https://uppbeat.io/pricing
- YouTube Audio Library: use "in your videos" on YouTube, credit in the description: https://support.google.com/youtube/answer/3376882?hl=en
- OpenGameArt licences and CC0 packs: https://opengameart.org/content/faq
- Universal UI Soundpack, CC BY 4.0: https://cyrex-studios.itch.io/universal-ui-soundpack
- Sonic Pi samples, CC0: https://raw.githubusercontent.com/sonic-pi-net/sonic-pi/main/etc/samples/README.md
- Remotion SFX (MIT package, per sound licences, many CC0): https://www.remotion.dev/docs/sfx
- Older macOS licences limit bundled content to personal use: https://www.apple.com/legal/sla/docs/macOS1012TouchID.pdf

## 16. The heuristics in use, in one list

So a later version knows which numbers to test first: the level table against the music (`sound.md` 11); ducking without a voiceover; pitch and level jitter ranges and pool sizes; the decaying series for staggers; the size factor mapping and the material table; whoosh peak position and cutoffs; riser, reverse swell, sub drop, braam, tonal hit, glitch, shimmer, chatter and bed recipes; the sync table as a whole (it is derived from standards, not published); the 5 and 10 point margins for dip and peak positions; the "one accented effect per 1 to 2 s" ceiling; "a slightly quieter dynamic master loses little"; the phone cut off near 150 Hz.

## 17. Gaps

- No primary interview with a commercial sound house (Lime, Barking Owl, Sonic Union, Wave, Factory, String and Tins) gave numbers on dynamics, ducking or stereo.
- No study measured where the loudest moment or the pre reveal silence sits in award winning short ads, other than this skill's own 129 film measurement.
- No perception study on how many identical repeats a listener tolerates.
- Official Wwise and FMOD randomisation defaults could not be read.
- No current (2024 to 2026) first party data on sound off viewing for TikTok, Reels, LinkedIn or X.
- The AIES 2026 paper's exact percentages were not read (only the abstract).
