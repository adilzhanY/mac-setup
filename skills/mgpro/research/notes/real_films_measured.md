# Sound in real motion graphics films, measured

129 professional motion graphics films and the three films made with the `mgpro` skill (Bauwerk, Torq, Sendoku) were run through the same audio analysis. This note gives the method, the film list, the distribution of every metric, the contrasts with the AI films, 20 timestamped examples, and rules for a code based sound engine.

Everything here is reproducible from `/home/wopler/dev/mgpro-research/films/`: `analyze.py` (per film metrics), `summarize.py` (CSV, distributions, charts), `crossfilm.py` (how alike films are), `cutsync.py` (sound around picture cuts), `examples.py` (timestamped moments). Per film JSON is in `films/json/`, the table of all films and metrics is `films/summary.csv`, distributions with each AI film's percentile are `films/distributions.json`.

## The short version

The AI films are not wrong on any single number. Their loudness, onset density, stereo width and loudness arc all fall inside the professional range. What is wrong is that **they are the same film three times**, and that they sit at the same edge of the range on a few axes:

1. **They are clones of each other.** On a 10 metric profile (tempo, density, percussive share, low end, loudness range, peak position, grid tightness, width, dips, density variation), the three AI films are 0.88 to 1.60 apart. Professional films by different makers are a median 4.1 apart (10th percentile 2.7), and films by the same maker 3.8. Only 0.45% of the 8,256 professional pairs are as close as the most distant AI pair. All three run at 120.2 BPM, all three are at -14.0 to -14.2 LUFS, two have the identical true peak (-1.36 dBTP), and all three have their one gap at exactly 13.75 s (45.8%). Torq and Sendoku share 42% of their strong transients (the same sound, correlation above 0.9); unrelated professional films share a median 4.6%.
2. **They are on the grid.** Professional onsets sit a median 0.105 of a 16th note off the tracked grid, and only 78% land within 25 ms of a 16th. The AI films sit at 0.047 to 0.093, with 91 to 100% of onsets on the grid (0th to 22nd percentile for offset, 71st to 98th for on grid share).
3. **They are bright.** Spectral centroid 2.3 to 3.0 kHz against a professional median of 1.8 kHz (AI at the 75th to 98th percentile), and 85% rolloff 5.7 to 7.5 kHz against 4.0 kHz (83rd to 100th).
4. **They hit every cut hard, and only cuts.** Averaged over 2,666 professional cuts, the onset strength around a picture cut rises to only 1.18 times its baseline (per film median 1.7 times). In the AI films it rises to 18.6 times. Professional sound marks some cuts and lets the music carry the rest. The AI films slam each one.
5. **They have little dynamic range and use dead silence instead of dips.** Loudness range 3.6 to 4.2 LU against a professional median of 5.8 (24th to 28th percentile). Professionals dip (20 dB down for a median 0.3 s, a median 4 times per film) far more than they go silent: 71% of professional films contain no near silence at all.
6. **They start at full volume and always have a pulse.** The first second of every AI film is at about its integrated loudness or above (-0.2 to +1.4 LU). The professional median first second is -1.9 LU, and the 10th percentile is -18.6 LU. 29% of professional films have no clear pulse (pulse strength under 0.2). Every AI film has one.

What the data does not support: the AI films are not too dense (3.0 to 3.6 onsets per second against a professional median of 4.0), not too loud, not too narrow, and the loudness arc (rise, plateau, drop at the end) is the same shape professionals use. Within one film they do not repeat their own sounds more than professionals do. The "same pops" complaint is about repetition **across films**, and the data confirms that.

## Method

**Film selection.** Candidates were found with WebSearch and `yt-dlp "ytsearch4:<query>"` over 143 queries (Apple feature films, Stripe, Linear, Figma, Notion, Vercel, Raycast, Arc, Framer, Spotify, Google and Material, the studios Buck, Ordinary Folk, ManvsMachine, Oddfellows, Giant Ant, Tendril, Buff, THE LINE, sound studios Antfood and Echoic, and SaaS and fintech brands). 130 were kept by hand: official brand or studio channels where possible, 12 to 250 s long, motion graphics or product film rather than live action talk, and no video known to be cut to a licensed pop song. The screening was by title and context, not by listening, so a few films with licensed or library music may remain. One film (Stripe Billing animation) turned out to have no audio and was excluded, which leaves **129 analysed professional films**. Vimeo now requires a login for yt-dlp, so all films are from YouTube. Unminus, Sono Sanctus, Gunner and Animade pieces could not be found as standalone YouTube uploads; Antfood and Echoic are represented by their own uploads.

**Download.** Audio only (`yt-dlp -x --audio-format wav --download-sections "*0-180"`), plus the smallest video stream (144p) for cut detection. Only one film was longer than 180 s (Oddfellows, The Blend is near, 4:09), so it was analysed for its first 3 minutes. The files are in `films/audio/` and `films/video/` for private analysis only.

**AI films.** `~/dev/bauwerk-video/public/ad.wav`, `~/dev/torq-video/public/torq.wav`, `~/dev/sendoku-video/public/film.wav` (all 30.0 s, 48 kHz stereo), with cuts from `out/bauwerk.mp4`, `out/torq.mp4` and `out/sendoku-ad.mp4`. The Bauwerk mp4 predates the final Bauwerk wav by a few hours, so its cut times may be slightly off.

**Metrics** (`analyze.py`, librosa 0.11, pyloudnorm, all audio resampled to 44.1 kHz for loudness and 22.05 kHz for analysis):

- Integrated loudness (ITU BS.1770 via pyloudnorm), true peak (4 times oversampled), loudness range (EBU LRA: 3 s windows every 0.1 s, gated at -70 LUFS and -20 LU relative, 95th minus 10th percentile), a 1 s loudness curve (K weighted), the position of the loudest 1 s and 3 s, and the mean loudness of each third relative to integrated.
- Tempo and beats from `librosa.beat.beat_track` on the onset envelope (hop 11.6 ms). Pulse strength is the normalised autocorrelation of the onset envelope at the tracked beat period (a steady click track gives 0.96; under 0.2 means no clear pulse).
- Onsets from `librosa.onset.onset_detect`; density overall and in 2 s windows.
- Percussive share: energy of the percussive part of a median filter HPSS split over total.
- Spectral centroid and 85% rolloff per frame (frames within 40 dB of the loud level), as percentiles and as a 1 s curve. Low end share is energy below 120 Hz; high share above 6 kHz.
- Stereo: side energy over mid plus side, and L/R correlation.
- Near silence: 50 ms frames more than 40 dB under the film's 95th percentile level, lasting 100 ms or more. Dip: more than 20 dB under, lasting 150 ms or more. Both skip the first and last 0.2 s. For each, the level 1 s before and after and the delay to the next onset are stored.
- Grid tightness: each onset's distance to the nearest 16th note on a grid built by splitting every tracked beat interval into four. Reported in ms and as a share of a 16th (0 means perfectly quantized, 0.25 is what random timing gives). The millisecond figure is limited by the 11.6 ms hop, so the normalised one is the useful number.
- Repetition: the 93 ms log mel patch of the percussive signal after every onset stronger than the film's median onset, mean centred. Patches are clustered (average linkage, correlation distance 0.3) into "sound types". A patch with a twin elsewhere in the film at correlation above 0.9 counts as a near duplicate.
- Cuts: ffmpeg `select='gt(scene,0.3)',showinfo` on the 144p video. For each cut, the signed offset to the nearest onset, the share of cuts with an onset within 2 video frames, and the same share for 2,000 random times (chance). Because a busy track has an onset every 250 ms, chance is high (median 64%), so `cutsync.py` also averages the onset envelope (divided by its median) in a ±400 ms window around every cut.
- Cross film (`crossfilm.py`): for each pair of films, the share of strong onsets whose best match in the other film correlates above 0.9 ("shared sounds"), and the Euclidean distance between the films' standardized 10 metric profiles.

**Self check.** A synthetic 120 BPM click track gives 120.2 BPM, pulse 0.96, 1.9 onsets per second, grid offset 0, one sound type and 100% near duplicates, as it should.

**Limits.** YouTube audio is lossy (Opus or AAC); this barely moves the metrics used here but slightly lowers energy above 15 kHz in the professional films. Many professional films have a voiceover and the AI films do not; the analysis does not separate them, which pushes professional onset density and percussive share up a little. Scene detection at a 0.3 threshold finds hard cuts, not morphs and match moves, so motion graphics films with continuous transitions show few cuts (the AI films only 2 or 3 each). Onset times come from the peak of the spectral flux, which lags the true attack by roughly one hop (about 12 ms), so every "onset minus cut" figure is about 12 ms later than the real sound. The beat tracker makes octave errors and returns tempo in coarse steps (110.3, 117.5, 120.2, 129.2...), so tempo values are approximate, and meaningless for films with a weak pulse.

## Distributions

Professional percentiles over the 129 films. Each AI value is followed by its percentile inside the professional distribution in brackets (for example "(98)" means higher than 98% of professional films). Charts are in `films/charts/`.

| Metric | n | Pro p10 | Pro median | Pro p90 | Bauwerk | Torq | Sendoku |
|---|---|---|---|---|---|---|---|
| Length analysed (s) | 129 | 30.0 | 60.0 | 102 | 30.0 (9) | 30.0 (9) | 30.0 (9) |
| Integrated loudness (LUFS) | 129 | -21.0 | -15.0 | -10.1 | -14.2 (59) | -14.1 (59) | -14.0 (64) |
| True peak (dBTP) | 129 | -5.18 | -0.67 | 0.43 | -1.36 (41) | -0.96 (44) | -1.36 (41) |
| Peak to loudness ratio (dB) | 129 | 9.81 | 13.5 | 17.0 | 12.8 (37) | 13.2 (43) | 12.6 (34) |
| Loudness range, EBU LRA (LU) | 129 | 2.35 | 5.83 | 11.4 | 3.81 (26) | 4.22 (28) | 3.61 (23) |
| Std of 1 s loudness (dB) | 129 | 2.02 | 4.47 | 7.15 | 4.13 (44) | 4.03 (42) | 3.84 (36) |
| Loudest 3 s, position (% of length) | 129 | 21.1 | 66.2 | 91.0 | 51.7 (38) | 51.7 (38) | 66.0 (48) |
| Loudest 1 s, position (%) | 129 | 16.9 | 65.0 | 90.7 | 48.3 (36) | 48.3 (36) | 68.3 (53) |
| Mean 1 s loudness, first third, vs integrated (LU) | 129 | -2.31 | 1.62 | 3.50 | 0.50 (30) | 1.19 (43) | 2.87 (81) |
| Same, middle third (LU) | 129 | 1.27 | 3.39 | 5.05 | 3.23 (46) | 3.91 (69) | 3.86 (67) |
| Same, last third (LU) | 129 | -5.19 | 1.48 | 4.30 | 1.32 (49) | 2.00 (55) | 1.32 (49) |
| Tempo, beat tracker (BPM) | 129 | 108 | 123 | 148 | 120 (36) | 120 (36) | 120 (36) |
| Pulse strength (0 to 1) | 129 | 0.085 | 0.37 | 0.61 | 0.36 (48) | 0.47 (67) | 0.52 (75) |
| Beat interval variation (CV) | 129 | 0.028 | 0.062 | 0.093 | 0.051 (40) | 0.042 (29) | 0.013 (1) |
| Onsets per second, whole film | 129 | 2.08 | 4.02 | 5.64 | 3.63 (41) | 3.00 (22) | 3.40 (35) |
| Onsets/s in 2 s windows, median | 129 | 2.00 | 4.00 | 5.75 | 4.50 (53) | 3.50 (31) | 3.50 (31) |
| Onsets/s in 2 s windows, 90th pct | 129 | 3.84 | 5.70 | 7.26 | 5.80 (53) | 4.50 (19) | 5.50 (36) |
| Onsets/s in 2 s windows, max | 129 | 4.90 | 7.00 | 8.10 | 7.00 (49) | 4.50 (5) | 6.50 (35) |
| Variation of 2 s density (CV) | 129 | 0.27 | 0.42 | 0.77 | 0.61 (76) | 0.45 (54) | 0.52 (69) |
| Variation of onset strength (CV) | 129 | 0.39 | 0.49 | 0.58 | 0.58 (88) | 0.72 (98) | 0.68 (98) |
| Percussive share of energy (HPSS) | 129 | 0.12 | 0.29 | 0.57 | 0.19 (32) | 0.16 (26) | 0.14 (16) |
| Energy share below 120 Hz | 129 | 0.11 | 0.45 | 0.75 | 0.35 (38) | 0.55 (63) | 0.45 (50) |
| Energy share above 6 kHz | 129 | 0.001 | 0.010 | 0.032 | 0.034 (91) | 0.027 (86) | 0.015 (67) |
| Spectral centroid, median (Hz) | 129 | 982 | 1834 | 2652 | 3035 (98) | 2810 (95) | 2271 (74) |
| 85% rolloff, median (Hz) | 129 | 1714 | 3973 | 5927 | 7494 (100) | 7235 (100) | 5701 (83) |
| Brightness movement (CV of 1 s centroid) | 129 | 0.19 | 0.30 | 0.49 | 0.36 (71) | 0.43 (79) | 0.49 (88) |
| Stereo side share of energy | 129 | 0.018 | 0.10 | 0.24 | 0.073 (40) | 0.082 (41) | 0.066 (35) |
| L/R correlation | 129 | 0.52 | 0.80 | 0.96 | 0.85 (60) | 0.84 (59) | 0.87 (65) |
| Near silences per film (40 dB down, 100 ms+) | 129 | 0.000 | 0.000 | 2.20 | 0.000 (0) | 1.00 (71) | 2.00 (82) |
| Near silences per 10 s | 129 | 0.000 | 0.000 | 0.37 | 0.000 (0) | 0.33 (88) | 0.67 (92) |
| Near silence total (s) | 129 | 0.000 | 0.000 | 0.81 | 0.000 (0) | 0.20 (77) | 0.65 (88) |
| Dips per film (20 dB down, 150 ms+) | 129 | 0.000 | 4.00 | 19.4 | 1.00 (16) | 1.00 (16) | 2.00 (24) |
| Dips per 10 s | 129 | 0.000 | 0.78 | 3.53 | 0.33 (30) | 0.33 (30) | 0.67 (48) |
| Share of film spent in dips | 129 | 0.000 | 0.027 | 0.12 | 0.008 (28) | 0.008 (28) | 0.025 (49) |
| Silence before first sound (s) | 129 | 0.000 | 0.050 | 0.45 | 0.000 (0) | 0.000 (0) | 0.000 (0) |
| Onset offset from 16th grid, median (ms) | 129 | 11.6 | 11.6 | 23.2 | 11.6 (4) | 5.80 (0) | 5.80 (0) |
| Same, as share of a 16th (0 = quantized, 0.25 = random) | 129 | 0.085 | 0.11 | 0.17 | 0.093 (22) | 0.047 (0) | 0.047 (0) |
| Onsets within 25 ms of a 16th | 129 | 0.56 | 0.78 | 0.96 | 0.91 (71) | 0.96 (86) | 1.00 (98) |
| Distinct onset sound types (clusters) | 129 | 1.00 | 7.00 | 11.0 | 9.00 (74) | 7.00 (46) | 6.00 (39) |
| Effective number of sound types | 129 | 1.11 | 5.10 | 13.5 | 14.3 (94) | 7.94 (66) | 7.20 (63) |
| Share of the most common sound type | 129 | 0.17 | 0.36 | 0.95 | 0.16 (8) | 0.27 (30) | 0.24 (21) |
| Onset to nearest twin correlation, median | 129 | 0.81 | 0.88 | 0.97 | 0.78 (3) | 0.84 (24) | 0.86 (33) |
| Onsets with a near identical twin (r > 0.9) | 129 | 0.10 | 0.43 | 0.91 | 0.15 (15) | 0.29 (33) | 0.41 (48) |
| Strong onsets compared | 129 | 42.0 | 115 | 219 | 55.0 (16) | 45.0 (12) | 51.0 (14) |
| Detected picture cuts per second | 129 | 0.020 | 0.24 | 0.85 | 0.10 (30) | 0.10 (30) | 0.067 (23) |
| Cuts with an onset within 2 frames | 120 | 0.25 | 0.72 | 1.00 | 0.67 (42) | 0.67 (42) | 0.50 (20) |
| Same, for random times (chance) | 120 | 0.34 | 0.64 | 0.89 | 0.24 (3) | 0.19 (1) | 0.21 (2) |
| Onset minus cut, median (ms) | 117 | -31.7 | 7.89 | 57.9 | 29.5 (78) | 4.91 (46) | 13.2 (56) |

![Loudness and space](../../films/charts/loudness_and_space.png)

![Rhythm and repetition](../../films/charts/rhythm_and_repetition.png)

![Tone and width](../../films/charts/tone_and_width.png)

![Tempo](../../films/charts/tempo.png)

![Loudness arc](../../films/charts/loudness_arc.png)

![Density arc](../../films/charts/density_arc.png)

![Dip positions](../../films/charts/dip_positions.png)

![Cut sync](../../films/charts/cut_sync.png)

![Cross film similarity](../../films/charts/crossfilm.png)

## Contrasts, pro against AI

**Sameness across films** (`crossfilm.json`, chart `crossfilm.png`).

| Pairs | n | Shared sounds, median (p10 to p90) | Profile distance, median (p10 to p90) | Tempo within 3 BPM |
|---|---|---|---|---|
| AI vs AI | 3 | 0.17 (0.16 to 0.37) | 1.41 (0.99 to 1.57) | 100% |
| Pro, same maker | 188 | 0.05 (0.00 to 0.48) | 3.76 (2.44 to 5.50) | 9% |
| Pro, different makers | 8,068 | 0.05 (0.00 to 0.29) | 4.09 (2.67 to 6.11) | 11% |

The AI pairs individually: Sendoku and Torq share 42% of strong transients and are 0.88 apart, Bauwerk and Sendoku 17% and 1.41, Bauwerk and Torq 15% and 1.60. A typical professional film's nearest neighbour among the other 128 is 1.70 away (p10 1.25), so each AI film is closer to its siblings than most professional films are to the single most similar film in the whole set. Even films by the same professional maker (the four Apple Health films, six Notion films, four Framer films, five Tendril films) are as different from each other as films from different studios.

**Timing.** Grid offset as a share of a 16th: pro median 0.105 (p10 0.085, p90 0.174); AI 0.093, 0.047, 0.047. At 120 BPM a 16th is 125 ms, so the professional median is about 13 ms off grid and the AI films about 6 ms (the hop limit of the measurement). Onsets within 25 ms of a 16th: pro median 78% (p10 56%); AI 91%, 96%, 100%. Beat interval variation: Sendoku 0.013, lower than 99% of professional films (median 0.062).

**Pulse.** Pulse strength pro median 0.37, but p10 0.085, and 29% of professional films are under 0.2, meaning they are built on sound design, pads and voice without a steady beat. The AI films are 0.36, 0.47, 0.52. The skill has never made a film without a beat. The tracked tempo of professional films is spread from 107 (p10) to 148 BPM (p90); 18% fall between 117 and 123, so 120 is common, but not three times in a row.

**Brightness.** Centroid pro median 1,834 Hz (p10 982, p90 2,652); AI 3,036, 2,808, 2,272 Hz. Rolloff pro median 3,960 Hz; AI 7,490, 7,240, 5,700 Hz. Energy above 6 kHz pro median 0.95%; AI 3.4%, 2.7%, 1.5%. The AI films also change brightness more over time (centroid CV 0.36 to 0.49 against 0.30), because bright hats and risers come and go over a dark sub.

**Transient shape.** Percussive share pro median 0.29 (p10 0.12, p90 0.57); AI 0.19, 0.16, 0.14. But the variation of onset strength is high in the AI films (0.58, 0.72, 0.68 against a pro median 0.49, 88th to 98th percentile): a few very hard hits on top of a smooth pad and sub, where professional tracks spread their transients more evenly (ticks, foley, small textures, voice).

**Dynamics.** LRA pro median 5.8 LU (p10 2.3, p90 11.4); AI 3.8, 4.2, 3.6. Std of 1 s loudness: pro 4.5 dB, AI 3.8 to 4.1 dB (the loudness curve shape itself is normal, see `loudness_arc.png`). Integrated loudness pro median -15.0 LUFS with a 11 LU spread (p10 -21.0, p90 -10.1); AI -14.2, -14.1, -14.0, as if one preset.

**Space.** Dips (20 dB down, 150 ms or longer) per 10 s: pro median 0.73 (p90 3.5); AI 0.33, 0.33, 0.67. 83% of professional films have at least one dip, 57% have a "re-entry" dip after which the sound comes back at least 6 dB louder than before it. Those re-entry dips last a median 0.30 s (p10 0.15, p90 0.95), the sound comes back a median +9.3 dB louder (p10 +6.5, p90 +15.7), and the first onset lands a median 41 ms after the dip ends (p10 11, p90 240). The AI gap at 13.75 s is a different gesture: the level before it is already high from the build (-18 to -20 dB), so it comes back only 3.6 to 6 dB louder, and the first onset arrives 13 ms after (exactly on the grid). Professional dips cluster in the first 10% of the film (opening breaths, an average 1 per film per 5% slice) and again at 90 to 95% (before the end card); in the middle they are spread evenly. The AI dips sit at 45.8% in all three films.

**Starts and ends.** First second relative to integrated: pro median -1.9 LU (p10 -18.6, p90 +3.9); AI -0.2, +0.8, +1.4. Silence before the first sound: pro median 0.05 s (p90 0.45 s); AI 0. The end is similar: the last loud second comes a median 1 s before the end in both (pro p90 5 s ring out). Onset density is not: professional films stay busy to about 85% of their length (median 4.2/s at 80%, 3.4/s at 90%), while all three AI films thin out from 70% (about 2/s at 80% and 0.5/s at 90%), because the end card is held for the last 8 to 9 s with little happening (`density_arc.png`). The same chart shows all three AI films emptying out at the same point, 40 to 45%.

**Cuts.** Pro: of 2,666 detected cuts in 116 films, the average onset strength at the cut rises to 1.18 times baseline, peaking 35 ms after the cut (about 23 ms after correcting the hop lag). Per film, the cut peak is 1.7 times baseline (p10 1.17, p90 3.9) and lands a median 12 ms after the cut (p10 58 ms before, p90 70 ms after). Cuts with an onset within 2 frames: 72% against a chance level of 64%. AI: 8 cuts, average peak 18.6 times baseline at +12 ms, with a duck to 0.5 times baseline in the 150 ms before the cut and a second spike about 270 ms later (roughly one 8th note at 120 BPM after the hit); with only 8 AI cuts this curve is indicative.

## Examples with timestamps

Times are from the start of the YouTube video. "Density" is onsets per second; "dB" is the 50 ms RMS level in dBFS averaged over the second before or after; "LU over integrated" is the 1 s loudness minus the film's integrated loudness.

1. **Tendril, Microsoft emojis celebration film** (Kh8BZPgpUhc). At 0:39.4 the sound drops more than 20 dB for 1.3 s (62% of the film). The second before sits at -30.4 dB, the second after at -16.1 dB, and the first new onset lands 51 ms after the drop ends. Density is 1.0/s in the 4 s before and 6.8/s in the 4 s after. The loudest second of the film follows at 0:43.
2. **Superhuman, Introducing Superhuman** (4XKq7qGnJus). A 0.85 s dip at 0:13.7 (23%), -22.7 dB before and -12.4 dB after (+10.3 dB), first onset 24 ms after. Density goes from 4.2/s to 7.0/s. The densest 2 s comes later at 0:26 (9.5/s, film median 6.5/s), the loudest second at 0:50 (84%).
3. **Stripe, Stripe Sessions 2024** (KH0_HM6e66w). A 0.85 s dip at 0:41.4 (38%), -34.6 dB to -22.6 dB, density 1.8/s before and 5.5/s after. The film has almost no pulse (0.03) and 82 cuts, of which 89% have an onset within 2 frames, which is chance level (88%) for a track this busy: the cuts are carried by continuous texture, not hits.
4. **Oddfellows, The Blend is near** (Oy3-bb2VA7w). At 0:48.3 a 0.7 s dip from -32.9 dB to -11.1 dB, a 21.8 dB jump, with density rising from 2.0/s to 4.7/s. The loudest second is much later, at 2:16 (76%).
5. **Uber, Bringing our new look to life** (axjXNEordH8). A 0.2 s dip at 0:27.1 (48%), then the level jumps from -26.1 dB to -8.1 dB (+18 dB). The loudest second follows at 0:31. LRA is 13.3 LU, more than twice the AI films.
6. **Apple, Introducing AirTag (Couch)** (dJMUYP88lrs). A 0.5 s dip at 0:17.6, -30.4 dB to -17.4 dB, density 1.5/s before and 3.5/s after; the loudest second comes early, at 0:22 (33%). LRA 17.6 LU, among the four highest in the set.
7. **Notion, Introducing Notion AI** (FElBbgnNtVA). A 0.3 s dip at 1:14.2 (88%), from -46.5 dB to -21.2 dB (+25 dB), and density goes from 4.2/s to 7.7/s; the densest 2 s of the film is right after it at 1:16 (8.0/s, film median 3.5/s). Late reveal, not mid film.
8. **Perplexity, Introducing Comet** (YeldJ4UezDQ). A sparse film: median density 1.0/s, with one burst of 6.5/s at 0:44. The loudest second at 0:37 is 15.4 LU over integrated. A 1.5 s dip at 1:03.6 (88%) leads into the end card.
9. **Raycast, New Raycast. Coming 2026** (Mi173xGb0ZA). Median density 0.8/s, a single dense window of 5.5/s at 0:12. A 0.35 s dip at 0:03.2 then a jump from -26.4 dB to -10.3 dB (+16 dB). Percussive share 0.03 and LRA 13.6 LU: an almost entirely tonal, swelling film.
10. **Linear, Introducing Linear Agent** (mRql2VJ99gM). Integrated -28.9 LUFS with an LRA of 17.6 LU. The loudest second is at 0:04 (8%), 21.5 LU over integrated: one opening impact, then a near silent film built on quiet tones (percussive share 0.02, low end share 0.86).
11. **Dropbox, Dropbox Dash: AI that understands you** (8Ab9EyV7DGY). A 0.75 s dip at 0:15.4 (15%), -30.8 dB to -14.0 dB (+16.8 dB). The loudest second is at 1:24 (83%).
12. **Microsoft Design, Next generation of OneDrive** (DzXBdc8Dfmg). A 0.95 s dip at 0:08.8 (15%), -20.1 dB to -12.1 dB, density 0.7/s before and 2.8/s after.
13. **Tendril, Beauty and science reel** (bdsJeK22w4w). A 1.9 s dip at 0:26.9 (37%), -37.5 dB to -13.8 dB (+23.7 dB). Density 0.7/s before, 1.3/s after: the return is a swell, not a burst of hits.
14. **Wise, Meet the new Wise design system** (x59J0l2EjAs). 70 cuts, 97% with an onset within 2 frames (chance 85%), median offset -2 ms: a film cut to its own music. A 0.35 s dip at 0:12.2, -25.1 dB to -10.0 dB (+15 dB).
15. **Apple, Introducing iPhone 15 Pro** (wqcjKkyuoZk). 30 cuts, 83% with an onset within 2 frames against 43% chance, median offset +14 ms (about one frame after the cut once the hop lag is removed). The loudest second is the very end, 0:36 (96%).
16. **ManvsMachine, Versus** (1ORKoaC3TlI). 32 cuts, 44% with an onset within 2 frames against 20% chance, median offset -20 ms (sound slightly before the cut). Percussive share 0.05, low end share 0.86, LRA 12.5 LU: a heavy, slow, tonal score where only some cuts get a hit.
17. **Samsung, One UI 5 introduction film** (Rb9PvLhe9ok). A 0.15 s dip at 0:12.3 from -41.8 dB to -10.5 dB (+31 dB), then 1.6 s until the next onset: the re-entry is a sustained chord, not a hit. Densest window at 1:58 (7.5/s, film median 4.0/s).
18. **Nothing, Phone (3): Come to play** (MHGQRnvE9GQ). Stereo side share 0.70 (the widest in the set; the median is 0.10), LRA 16 LU. A 0.45 s dip at 0:18.9 is followed by 7.5 s with no new onset at all.
19. **Monzo, Money feels different on Monzo** (pOUs63Qc80k). No pulse (pulse strength 0.00), 45 cuts, 53% with an onset within 2 frames against 33% chance, median +39 ms: sound effects follow the picture without a beat grid. A 1.25 s dip at 0:03.7 opens the film.
20. **Ordinary Folk, Ordinary Folk ident** (EFdAOiNXUKY). A 0.95 s dip at 0:02.6, density 0.8/s before and 3.0/s after, LRA 10.7 LU in a 36 s ident.

And the AI films:

21. **Bauwerk, Torq and Sendoku.** All three have their gap at 0:13.75 (frame 825 at 60 fps, 45.8%): 0.25 s in Bauwerk (-18.4 dB before, -14.8 dB after), 0.2 s of near silence in Torq (-19.6 dB to -14.9 dB), 0.2 s in Sendoku (-20.5 dB to -14.9 dB), each followed by an onset 13 ms after. Sendoku adds a second 0.45 s silence at 0:21.55. All three track at 120.2 BPM, integrate at -14.2, -14.1, -14.0 LUFS and peak at -1.36, -0.96, -1.36 dBTP. Their 2 s density curves rise and fall at the same points: Bauwerk 6.0, 5.0, 7.0, 4.5, 4.5, 2.5, **0.0**, 5.0...; Torq 3.5, 3.5, 4.5, 4.0, 3.0, 3.0, **2.0**, 3.5...; Sendoku 5.5, 6.5, 4.0, 3.0, 5.5, 4.5, **2.0**, 4.0... (the dip at window 7, 12 to 14 s, in each).

## Rules for a code based sound engine

Each rule comes from the measurements above. The numbers are the professional distribution, which is a range to move around in, not a target to hit every time.

1. **Measure every new score against every earlier one, as a profile, and demand distance.** Compute the 10 metric profile (tempo, onset density, percussive share, low end share, LRA, loudest 3 s position, grid offset, side share, dips per 10 s, density variation) and require a standardized distance of at least 2.5 (the professional 10th percentile is 2.7) from every film in the registry. The AI films are 0.9 to 1.6 apart.
2. **Never reuse a transient sample across films.** Fewer than 10% of a new film's strong onsets may correlate above 0.9 with any earlier film's (professional median 5%; Torq and Sendoku 42%). Synthesize hits with per film parameters (pitch, envelope, body, noise colour), not from a shared kit.
3. **Do not sit every event on the grid.** Keep downbeat and structural hits exact, but give other musical events a timing spread of roughly 10 to 15 ms at 120 BPM (a median of 0.1 of a 16th). Let 20 to 40% of onsets be off grid entirely: sound design that follows the picture rather than the bar (professional films have a median 78% of onsets within 25 ms of a 16th, AI 91 to 100%).
4. **Make about one film in three unmetered.** 29% of professional films have no clear pulse. Drive those with swells, impacts, textures and UI sounds placed from picture cues, with no kick pattern at all.
5. **Spread the tempo.** Use 105 to 150 BPM (professional 10th to 90th percentile) and never the same tempo as the last three films. 120 is fine once.
6. **Darken the mix.** Aim the median spectral centroid between 1.0 and 2.6 kHz (professional p10 to p90, median 1.8 kHz) and keep energy above 6 kHz under about 2% (median 0.95%). Low pass hats, shakers and risers, or use fewer of them. The AI films sit at 2.3 to 3.0 kHz.
7. **Use dips, not dead air.** Plan 0.5 to 3.5 dips per 10 s (20 dB down, 0.15 to 1 s; median 0.3 s). Make at least one a re-entry: come back 6 to 16 dB louder (median +9 dB) with the first onset 10 to 250 ms after (median 41 ms), not always exactly on the beat. Reserve true silence (40 dB down) for at most one or two moments; 71% of professional films have none.
8. **Put dips where the film breathes, and move them.** Professional dips cluster in the first 10% (the opening) and at 90 to 95% (before the end card), with the rest spread evenly. Never put the main gap at the same percentage as an earlier film.
9. **Move the big moment.** The loudest 3 s sits anywhere from 20% to 91% of the length (median 66%); 16% of films peak in the first third, 32% in the middle, 52% in the last third. Pick per film, from the story.
10. **Start below the body.** Let the first second be quieter than the film's integrated loudness by 2 to 18 LU (median -1.9, p10 -18.6), and allow up to 0.5 s of silence before the first sound. Do not open at full level every time.
11. **Widen the dynamic range.** Aim for an LRA of 5 to 11 LU (median 5.8, p90 11.4), with quiet passages that really are quiet. Vary the integrated level between films (professional p10 to p90 is -21 to -10 LUFS) instead of mastering every film to -14.0; for platforms that normalize, a quieter, more dynamic master loses nothing.
12. **Even out the hits.** Keep the variation of onset strength near the professional 0.4 to 0.6 (AI 0.58 to 0.72). Fewer giant isolated hits over a smooth pad, more mid level texture: ticks, foley like clicks, noise grains, small UI blips, so that the percussive share rises toward 0.2 to 0.5.
13. **Mark some cuts, not all.** Across professional films the average cut gets only 1.2 to 1.7 times the baseline onset strength; the AI films give 18 times. Give a strong hit to the structural cuts (title, product reveal, end card), and let the music or a continuous texture carry ordinary cuts. Vary the timing: a whoosh or riser may lead the cut by 2 to 4 frames, an impact can land on it or 1 to 2 frames after (per film median +12 ms, p10 -58 ms, p90 +70 ms).
14. **Do not duck before every hit.** The AI films pull the level to half in the 150 ms before each cut. Professionals rarely do it on ordinary cuts; save the pre-hit duck for the one or two re-entry moments of rule 7.
15. **Shape density with contrast.** Within a film, the busiest 2 s should carry about 2 to 9 times the onsets of the quietest (median 2.2 times), with sparse passages near 1 onset per second and bursts of 6 to 9 per second (max 2 s window median 7.0/s). Place the burst where the story needs it, not on a fixed section map.
16. **Vary width by film and by section.** Side share 0.02 to 0.24 (median 0.10). Some films should be nearly mono and close, some wide; widen at the big moment, not throughout.
17. **Vary the ending.** Most films end 1 s after the last loud second, but 10% ring out for 5 s or more. Choose per film rather than always closing with the same one second tail.
18. **Keep the film alive until the end card.** Professional onset density stays near its median until about 85% of the length and falls only in the last 10 to 15%. Do not let the last third go quiet while the picture is still telling the story; if the end card is long, give it its own small events (a logo sound, a tail, a last UI tick).

## Film list

129 analysed films (plus the excluded silent one, Stripe Billing animation, https://www.youtube.com/watch?v=8u6pQplVPio). Length is the full video length on YouTube; analysis covers the first 180 s.

| # | Title | Maker | Length | URL |
|---|---|---|---|---|
| 1 | Firefly: the next evolution | Adobe | 0:41 | https://www.youtube.com/watch?v=Fxck1CWjue4 |
| 2 | Firefly: the world is what you make it | Adobe | 1:00 | https://www.youtube.com/watch?v=3mQ7aVnnGRU |
| 3 | Meet Airbnb Cereal | Airbnb | 0:46 | https://www.youtube.com/watch?v=KOfxE-pDLW4 |
| 4 | Mailchimp ID: Grow | Alex Grigg for Mailchimp | 0:22 | https://www.youtube.com/watch?v=2tC2Q2xphRQ |
| 5 | AICP 2018 sponsor reel | Antfood | 3:00 | https://www.youtube.com/watch?v=egOMLmDYdjc |
| 6 | WarnerMedia The Prow case study | Antfood | 2:07 | https://www.youtube.com/watch?v=p6tkdDFgP7E |
| 7 | Analogue Loaders | Antfood (sound) | 2:03 | https://www.youtube.com/watch?v=7SD9ZUspWMc |
| 8 | Apple Pencil Pro reveal | Apple | 0:23 | https://www.youtube.com/watch?v=gTJMHryESvY |
| 9 | Genmoji It :30 | Apple | 0:30 | https://www.youtube.com/watch?v=Uhrpl5FGLFs |
| 10 | Health app: Activity | Apple | 0:51 | https://www.youtube.com/watch?v=WYRYWIWu_cE |
| 11 | Health app: Everything's connected | Apple | 1:02 | https://www.youtube.com/watch?v=qQjP951CM-c |
| 12 | Health app: Mindfulness | Apple | 0:47 | https://www.youtube.com/watch?v=BiEklELmzHk |
| 13 | Health app: Sleep | Apple | 0:47 | https://www.youtube.com/watch?v=zZTm_7VmCS8 |
| 14 | Introducing AirTag (Couch) | Apple | 1:08 | https://www.youtube.com/watch?v=dJMUYP88lrs |
| 15 | Introducing Apple Creator Studio | Apple | 0:35 | https://www.youtube.com/watch?v=ISYIEmQxs2M |
| 16 | Introducing iPhone 15 Pro | Apple | 0:38 | https://www.youtube.com/watch?v=wqcjKkyuoZk |
| 17 | The new Mac mini with M6 | Apple | 0:43 | https://www.youtube.com/watch?v=3WpzNmY35S4 |
| 18 | Vision Pro reveal | Apple | 1:17 | https://www.youtube.com/watch?v=Btf4mN37OsU |
| 19 | What is Asana? | Asana | 0:47 | https://www.youtube.com/watch?v=AW_PDcmjE-o |
| 20 | World's smartest corporate card | Brex | 1:13 | https://www.youtube.com/watch?v=B025YhrnYus |
| 21 | Buck Sydney turns ten | Buck | 1:00 | https://www.youtube.com/watch?v=SxYzrzRjfsI |
| 22 | iMac Pro artist film | Buck for Apple | 0:57 | https://www.youtube.com/watch?v=bNOVDZrgkjo |
| 23 | Showreel 2023 | Buff Motion | 1:18 | https://www.youtube.com/watch?v=CDpNDFAfQX8 |
| 24 | Showreel 2025 | Buff Motion | 0:50 | https://www.youtube.com/watch?v=gQldOO6KiU8 |
| 25 | Vaylens brand launch | Buff Motion | 1:12 | https://www.youtube.com/watch?v=Hbj6WMhVByQ |
| 26 | Innovation | Coinbase | 1:00 | https://www.youtube.com/watch?v=YjS_2Yq9Y94 |
| 27 | The financial system is out of date | Coinbase | 0:49 | https://www.youtube.com/watch?v=Gxr-ViBuHB8 |
| 28 | Introducing Cursor 3 | Cursor | 1:30 | https://www.youtube.com/watch?v=UxbULt_hCdA |
| 29 | Fuel your Discord with Nitro | Discord | 0:25 | https://www.youtube.com/watch?v=v2i6nu2OYfY |
| 30 | Nitro Basic | Discord | 0:30 | https://www.youtube.com/watch?v=oMZApgpr7Hc |
| 31 | Dropbox Dash: AI that understands you | Dropbox | 1:42 | https://www.youtube.com/watch?v=8Ab9EyV7DGY |
| 32 | Dropbox Dash: AI universal search | Dropbox | 0:55 | https://www.youtube.com/watch?v=Cn4r-ayMLto |
| 33 | Echoic X ident | Echoic | 0:15 | https://www.youtube.com/watch?v=qIREIJROPis |
| 34 | Marcom infographic | Echoic | 2:56 | https://www.youtube.com/watch?v=sv4wk6h89yc |
| 35 | All the launches at Config 2024 | Figma | 1:20 | https://www.youtube.com/watch?v=0wCIP2Ox-EQ |
| 36 | Introducing FigJam AI | Figma | 0:53 | https://www.youtube.com/watch?v=q-hRF2NJccc |
| 37 | Welcome to FigJam | Figma | 1:06 | https://www.youtube.com/watch?v=axDzyLEfYgU |
| 38 | Framer 3.0 | Framer | 1:15 | https://www.youtube.com/watch?v=6aioEoCdBJw |
| 39 | Framer for Enterprise | Framer | 0:47 | https://www.youtube.com/watch?v=-qD3KOfBjZE |
| 40 | Framer: All design, no code | Framer | 0:37 | https://www.youtube.com/watch?v=6xJWQRVl9nw |
| 41 | That's Framer | Framer | 0:38 | https://www.youtube.com/watch?v=8AHPXm9Y6mI |
| 42 | Slack Traffic | Giant Ant | 1:00 | https://www.youtube.com/watch?v=j0TlZetg1fk |
| 43 | GitHub Universe: We have lift off | GitHub | 1:33 | https://www.youtube.com/watch?v=qwLDACQeWBI |
| 44 | Project HydraFusion in Copilot | GitHub | 1:34 | https://www.youtube.com/watch?v=dJmt1PHsETM |
| 45 | Introducing Canvas in Gemini | Google | 1:00 | https://www.youtube.com/watch?v=4Leardp_AGc |
| 46 | Introducing Gemini Omni | Google | 0:54 | https://www.youtube.com/watch?v=KUyRq7szZsM |
| 47 | Introducing Material 3 Expressive | Google Design | 0:38 | https://www.youtube.com/watch?v=n17dnMChX14 |
| 48 | Introducing Google Vids | Google Workspace | 1:27 | https://www.youtube.com/watch?v=4SCjXcBeW1E |
| 49 | Accepting the mind | Headspace | 1:07 | https://www.youtube.com/watch?v=qUcC71-W9Os |
| 50 | Shopify Editions brand film | Imaginary Forces | 1:30 | https://www.youtube.com/watch?v=2qlHC9KPJG8 |
| 51 | The future of customer service | Intercom | 1:33 | https://www.youtube.com/watch?v=6xQO5Rjz-v8 |
| 52 | Introducing Linear Agent | Linear | 0:55 | https://www.youtube.com/watch?v=mRql2VJ99gM |
| 53 | Introducing Linear Releases | Linear | 0:30 | https://www.youtube.com/watch?v=6dIwFoQ0eVg |
| 54 | Introducing Linear for Agents | Linear | 0:33 | https://www.youtube.com/watch?v=sbwOQV5zY34 |
| 55 | Linear Insights | Linear | 0:37 | https://www.youtube.com/watch?v=fdyVP02X3l0 |
| 56 | What is Lottie? | LottieFiles | 1:49 | https://www.youtube.com/watch?v=A_sjNPSA4kg |
| 57 | Pixel Drop design refresh | Made by Google | 1:05 | https://www.youtube.com/watch?v=yPG0LCQF87s |
| 58 | Tiny floating dots (Pixel Buds) | Made by Google | 0:30 | https://www.youtube.com/watch?v=jkT6hXdmYec |
| 59 | Nike Air 2017 | ManvsMachine | 0:32 | https://www.youtube.com/watch?v=2HqvQfk_svc |
| 60 | Showreel | ManvsMachine | 1:42 | https://www.youtube.com/watch?v=yRNkF-i_Etk |
| 61 | Versus | ManvsMachine | 1:24 | https://www.youtube.com/watch?v=1ORKoaC3TlI |
| 62 | Copilot on Windows 11 | Microsoft | 0:30 | https://www.youtube.com/watch?v=C2VDW-Zsbzg |
| 63 | Introducing Windows 11 | Microsoft | 2:43 | https://www.youtube.com/watch?v=Uh9643c2P6k |
| 64 | Microsoft 365 vision video | Microsoft Design | 1:30 | https://www.youtube.com/watch?v=1kntpy9u4ZU |
| 65 | Next generation of OneDrive | Microsoft Design | 1:00 | https://www.youtube.com/watch?v=DzXBdc8Dfmg |
| 66 | Money feels different on Monzo | Monzo | 1:00 | https://www.youtube.com/watch?v=pOUs63Qc80k |
| 67 | Dropbox: Creative freedom | Nexus Studios | 1:00 | https://www.youtube.com/watch?v=gJl5JoUJVXw |
| 68 | Nothing Phone (1) | Nothing | 0:23 | https://www.youtube.com/watch?v=YWV2XjoRKhk |
| 69 | Phone (1): Pure instinct | Nothing | 0:24 | https://www.youtube.com/watch?v=hQWDUPJFHdg |
| 70 | Phone (3): Come to play | Nothing | 0:30 | https://www.youtube.com/watch?v=MHGQRnvE9GQ |
| 71 | Introducing Notion 3.0: Agents | Notion | 1:30 | https://www.youtube.com/watch?v=R1cF4T4lgI4 |
| 72 | Introducing Notion AI | Notion | 1:25 | https://www.youtube.com/watch?v=FElBbgnNtVA |
| 73 | Introducing the new Notion AI | Notion | 0:57 | https://www.youtube.com/watch?v=S92KX8-Hmlc |
| 74 | Meet Notion Calendar | Notion | 1:20 | https://www.youtube.com/watch?v=C4Q2ezioTUM |
| 75 | Meet Notion Mail | Notion | 1:00 | https://www.youtube.com/watch?v=54l-1NfXnX8 |
| 76 | What is Notion? | Notion | 1:27 | https://www.youtube.com/watch?v=3HLMH9t1Q-g |
| 77 | Nike Battle Force | Oddfellows | 0:20 | https://www.youtube.com/watch?v=Y4kI_DmCzLQ |
| 78 | Reel 2017 | Oddfellows | 1:28 | https://www.youtube.com/watch?v=JS_ZPtcWB8s |
| 79 | The Blend is near | Oddfellows | 4:09 | https://www.youtube.com/watch?v=Oy3-bb2VA7w |
| 80 | ABUS: Keep on riding | Ordinary Folk | 0:30 | https://www.youtube.com/watch?v=G73wGSYCx30 |
| 81 | Creation | Ordinary Folk | 1:27 | https://www.youtube.com/watch?v=nUReIjguWEw |
| 82 | Google Gemini launch | Ordinary Folk | 1:14 | https://www.youtube.com/watch?v=hsOyJdsXdp4 |
| 83 | Google Search On 2020 | Ordinary Folk | 0:35 | https://www.youtube.com/watch?v=t3c7bviDPz4 |
| 84 | Google montage | Ordinary Folk | 1:12 | https://www.youtube.com/watch?v=7Q4tHIp8UoI |
| 85 | Introducing Spline | Ordinary Folk | 1:25 | https://www.youtube.com/watch?v=sIfP9h-H23s |
| 86 | Ordinary Folk ident | Ordinary Folk | 0:36 | https://www.youtube.com/watch?v=EFdAOiNXUKY |
| 87 | Ordinary Reel | Ordinary Folk | 1:03 | https://www.youtube.com/watch?v=VCFbI49Vvyg |
| 88 | Reel II | Ordinary Folk | 1:32 | https://www.youtube.com/watch?v=SJ4u5pPMtKs |
| 89 | Webflow: Welcome to the age of no-code | Ordinary Folk | 1:30 | https://www.youtube.com/watch?v=_qCBg_Wsr8M |
| 90 | Deep Research on Perplexity | Perplexity | 0:54 | https://www.youtube.com/watch?v=Z1_M2XtsUwY |
| 91 | Introducing Comet | Perplexity | 1:12 | https://www.youtube.com/watch?v=YeldJ4UezDQ |
| 92 | Perplexity Computer | Perplexity | 1:34 | https://www.youtube.com/watch?v=qOsEYyQuxbU |
| 93 | New Raycast. Coming 2026 | Raycast | 0:39 | https://www.youtube.com/watch?v=Mi173xGb0ZA |
| 94 | Raycast Pro preview | Raycast | 0:22 | https://www.youtube.com/watch?v=u6iro1jHujs |
| 95 | Build anything, govern everything | Retool | 0:55 | https://www.youtube.com/watch?v=FWNNP5rqbF4 |
| 96 | Retool Tables launch | Right Hand Films for Retool | 0:20 | https://www.youtube.com/watch?v=zs8BYGx_wyQ |
| 97 | A new dawn at Robinhood | Robinhood | 0:47 | https://www.youtube.com/watch?v=i7rPKY5FxNM |
| 98 | The future of trading | Robinhood | 0:30 | https://www.youtube.com/watch?v=ivvw5uBvTh4 |
| 99 | Trade all in one place | Robinhood | 0:30 | https://www.youtube.com/watch?v=8oEQSOXnyPc |
| 100 | Gen-3 Alpha available now | Runway | 2:22 | https://www.youtube.com/watch?v=nByslCkykj8 |
| 101 | Introducing Gen-4.5 | Runway | 1:09 | https://www.youtube.com/watch?v=AwKSrJFvdps |
| 102 | One UI 5 introduction film | Samsung | 2:17 | https://www.youtube.com/watch?v=Rb9PvLhe9ok |
| 103 | Material 3 Expressive: Data's new language | Scene for Google | 0:50 | https://www.youtube.com/watch?v=6YD25EoV5Oo |
| 104 | Editions Summer '24 trailer | Shopify | 0:30 | https://www.youtube.com/watch?v=VU-zVyMsxmg |
| 105 | Editions Summer '25 trailer | Shopify | 0:35 | https://www.youtube.com/watch?v=CZqaS7PcjdI |
| 106 | Editions Winter '26 trailer | Shopify | 0:35 | https://www.youtube.com/watch?v=kDpckwYZgZI |
| 107 | Where work happens: the big pitch | Slack | 0:15 | https://www.youtube.com/watch?v=1AgbwhTHa7o |
| 108 | Introducing Reserved by Spotify | Spotify | 1:12 | https://www.youtube.com/watch?v=WEQvng2kfQU |
| 109 | Beneath the Surface | Stripe | 2:08 | https://www.youtube.com/watch?v=iuWizuXgXwc |
| 110 | Stripe Sessions 2024 | Stripe | 1:49 | https://www.youtube.com/watch?v=KH0_HM6e66w |
| 111 | The beauty in simplicity | Stripe | 2:10 | https://www.youtube.com/watch?v=98JAHz3eUHw |
| 112 | Introducing Superhuman | Superhuman | 1:00 | https://www.youtube.com/watch?v=4XKq7qGnJus |
| 113 | Introducing Superhuman Mail | Superhuman | 1:14 | https://www.youtube.com/watch?v=JMsFfX6qTNI |
| 114 | Showreel 2025 | THE LINE | 1:35 | https://www.youtube.com/watch?v=ORhQgrA79B4 |
| 115 | Beauty and science reel | Tendril | 1:13 | https://www.youtube.com/watch?v=bdsJeK22w4w |
| 116 | Best of sizzle reel | Tendril | 1:25 | https://www.youtube.com/watch?v=S4XaGMbWaHw |
| 117 | Figure 03 R&D reel | Tendril | 0:35 | https://www.youtube.com/watch?v=U2s417au_D8 |
| 118 | Industrial design reel | Tendril | 1:11 | https://www.youtube.com/watch?v=QlfBXfdEdnM |
| 119 | Microsoft emojis celebration film | Tendril | 1:03 | https://www.youtube.com/watch?v=Kh8BZPgpUhc |
| 120 | Arc 1.0: Everything or nothing | The Browser Company | 0:34 | https://www.youtube.com/watch?v=n5Vwrj1gEWs |
| 121 | Arc for Students | The Browser Company | 0:32 | https://www.youtube.com/watch?v=rgZbsYZ9dwo |
| 122 | Arc on Windows | The Browser Company | 0:37 | https://www.youtube.com/watch?v=LJQsAOon6og |
| 123 | Dia Browser | The Browser Company | 1:18 | https://www.youtube.com/watch?v=YVOw0TAO9ok |
| 124 | Why is Arc Search a better mobile browser | The Browser Company | 1:00 | https://www.youtube.com/watch?v=FHA5YZEAYOc |
| 125 | Bringing our new look to life | Uber | 0:56 | https://www.youtube.com/watch?v=axjXNEordH8 |
| 126 | Introducing v0: Generative UI | Vercel | 0:48 | https://www.youtube.com/watch?v=By9wCB9IZp0 |
| 127 | Meet the new Wise design system | Wise | 1:20 | https://www.youtube.com/watch?v=x59J0l2EjAs |
| 128 | Identity film | aflow | 0:47 | https://www.youtube.com/watch?v=xBZzVNi_4Xw |
| 129 | OP-XY | teenage engineering | 0:56 | https://www.youtube.com/watch?v=ukES66CtiAg |

