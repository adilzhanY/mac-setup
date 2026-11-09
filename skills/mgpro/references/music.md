# Music: a new score for every film

Every film gets its own music: its own tempo, groove, key, palette, hook and form. Four films were made with this skill before this file existed, all at 120 BPM, and the Sendoku score reused the torq score's groove almost note for note (fingerprint: groove 0.98, harmony 1.00, palette 0.80). The user heard it straight away: "the rhythm is identical which is kinda bad". A score that sounds like the last ad makes the product sound like the last product.

The cause was in this skill: a fixed 120 BPM grid, one arrangement with fixed frames (gap 825, drop 840, stop 1290), one palette list, and the instruction to start from an example synth. All four are gone. What replaces them is below.

Later the first three films were measured against 129 professional motion graphics films (`sound-research.md`). They were not wrong on any single number, but they were the same film three times: 120.2 BPM each, -14.0 to -14.2 LUFS, the one gap at 45.8 percent of the length in all three, profile distances of 0.9 to 1.6 where professional films by different makers sit a median 4.1 apart, and 42 percent of torq's and Sendoku's strong transients the same sound. They were also more on the grid, brighter and less dynamic than professional films, and all had a beat where 29 percent of professional films have none. The contract below now covers those too; the effects side is in `sound.md`.

Then the Enogon film (mgpro 2.0.0) passed every one of these measurements, and the user still heard it as AI music: slow, with holes where the automatic dips pulled the level down, and with synthesized sounds that recalled the earlier films. Distinct is not the same as well written or real. How to write the score from the picture (timing first, the motif, harmony, groove, building by texture, the ending on the logo frame) is now `composition.md`; how to make it sound performed and recorded (samples first, round robins, systematic timing, one shared room) is `sound.md`, section 4b; and contrast is arranged, never a gain hole (`sound.md`, section 9).

## The contract

A new score must differ from EVERY film in `music/registry.json` in all of these:

1. **Genre or groove family.** Not the same genre, and not the same kick pattern (four on the floor twice in a row counts as the same).
2. **Tempo.** At least 6 BPM away from any film whose groove is similar, never the tempo of any of the last three films, and not 120 by habit. Pick from the genre's own range; professional films spread from about 108 to 148 BPM (10th to 90th percentile), and only 18 percent sit between 117 and 123.
3. **Key and mode.** Not the same key and mode as the last three films.
4. **Palette.** A different bass kind and a different lead kind. The kick may repeat only if the genre differs.
5. **Form.** The big moment (drop, reveal, switch) at a different place, or a different kind of form altogether.
6. **Signature.** One sound nobody else has, ideally taken from the product (see below).
7. **Pulse.** About one film in three has no steady beat (the beatless option below). If the last two films in the registry both had one, this film is beatless unless the brief clearly needs a groove; say which in the reply.
8. **Shape.** The main breath and the loudest moment sit at different places in the film from every earlier film (`sound.md`, sections 9 and 10), and the ending is chosen, not the same tail again.

Then it must pass the measurement: `audio/fingerprint.py public/film.wav --bpm <bpm> --against ~/.claude/skills/mgpro/music/registry.json` exits 0 (groove under 0.85, harmony under 0.97, palette under 0.70, form shape under 0.70 against every earlier film). If it fails, change the groove, tempo, palette or form, not the thresholds.

The same run, given the cue list and the brief, also measures the whole film against the registry and the professional range, on the finished mix with effects (`fingerprint.py public/film.wav --bpm <bpm> --against ... --cues src/cues.json --music src/music.json`, plus `--video out/film.mp4` to take the cuts from the picture and `--cold-open` for a film that opens at full level on purpose). It prints pass or FAIL per check and exits 1 on any failure:

- **Profile distance at least 2.67** (the professional 10th percentile, different makers) from every earlier film. The profile is ten standardized measurements: tempo, onset density, percussive share, low end share, loudness range, where the loudest 3 s sits, grid offset, stereo side share, dips per 10 s and density variation. Professional films by different makers sit a median 4.1 apart (10th percentile 2.7); the first three mgpro films sat 0.9 to 1.6 apart.
- **Shared transients at most 10 percent**: no more than one in ten of the film's strong onsets may match an earlier film's at a correlation above 0.9 (professional median 4.6 percent; torq and Sendoku 42). The kit's `vary.py` derives every effect's synthesis seed from the film's seed, so two films never share a synthesized transient.
- Centroid 982 to 2652 Hz, rolloff 1714 to 5927 Hz, LRA 5 to 11.4 LU, the first second at most -1.0 LU against the whole, and the rise at cuts at most 3.93 times baseline. The other rules it prints without failing (grid, dips, pulse, density, width) are in `sound.md`, section 12.

When the film is finished, append it to the registry (the command prints the measured part; add the choices by hand).

## The sonic brief (`src/music.json`)

Decide these before the script, because the form decides where the picture cuts. One file feeds the picture (`lib.ts` reads tempo and section starts), the cue list (`cues.py`) and the score (`score.py`). The kit has a filled example.

| Field | What it is | How to decide |
|---|---|---|
| genre | one of `grooves.GENRES` (or two for a beat switch) | brand traits table below, minus what the registry has used |
| bpm | from the genre's `tempos` (whole frames per beat at 60 fps) | from the cut's hit points first (`composition.md`, section 1), then the picture's energy; faster tunes stick better (Jakubowski 2016) |
| key, mode | tonic and one of `theory.MODES` | the mood table below; the product's own UI sounds' key wins if it has any |
| mood, progression | a `theory.PROGRESSIONS` mood, or your own numerals | what the viewer should feel at the drop |
| palette | role to instrument kind (kick, snare, hat, bass, keys, pad, lead, plus genre roles) | genre default, then change at least two roles so it is this film's |
| drums | pattern overrides per part | rewrite at least one part (move a kick, add a percussion line) |
| hook | seed, contour, notes, register | see Hooks |
| signature | one sentence | see Signature |
| character | sfx character: glass, wood, metal, plastic, paper, digital, soft | what the interface is made of |
| beat | true (default) or false (the beatless option) | the contract's pulse rule |
| opening, opening_lu, head | `"soft"` (default, the first second about 2 LU under the whole) or `"cold"`; the soft target in LU; silence before the first sound | a cold open form only gets `"cold"` |
| dips, dip_db | set `0`: no automatic dips (the 2.0.0 code still defaults to `"auto"` at -24 dB, which made the Enogon holes); breaths are written as thin form sections | `sound.md` section 9 |
| instruments, samples_map | `"samples"`: every part the sampler map covers is played by recorded CC0 instruments in a convolved room, the rest stays synth; optional per role overrides such as `{"keys:piano": "felt"}` | always `"samples"` unless the library is missing (`sound.md` section 4b) |
| lra | target loudness range (default 6.0) | 5 to 11; wider for calm and cinematic films |
| tone, bass_harmonics | the master's tone target (default centroid 1800, rolloff 4000; `false` to keep the mix's own); low end harmonics for small speakers (default 0.3) | see Tonal balance |
| humanize_ms | median timing offset of music onsets (default 12) | see Humanising the score |
| bed, bed_rate, keep_alive | quiet off grid grains between the hits (default 0.5, beatless 1.5; 7 per second, beatless 10); the lightest part kept in drumless bars between 55 and 85 percent (default true) | leave the defaults unless the measurement says otherwise |
| pool, fx_level | effect takes per sound (default 4); effects bus level (default 0.5) | |
| samples | `{"enabled": true, "jobs": "all", "layer": [...]}` for recorded effects (the code's default is still `false`) | `rights.md` and `sound.md` sections 4 and 4b |
| form | sections: name, bars (fractions allowed), energy, parts | see Forms; name sections after the acts |
| seed | any number | a new one per film, so humanising and noise differ |

## Choosing the genre

Start from the brand, not from the last film. Each genre in `templates/kit/audio/grooves.py` lists what it fits; this table is the short version.

| Brand trait | Candidates |
|---|---|
| Calm, focused, crafted (reading, puzzles, writing, wellbeing) | lofi, boom_bap, bossa_electronica, ambient_pulse |
| Precise, systematic, technical (data, AI, infra, dev tools) | minimal_techno, breakbeat, synthwave, cinematic_pulse |
| Warm, social, joyful (food, payments, community, travel) | afrobeats, amapiano, afro_68, nu_disco, funk |
| Bold, competitive, young (sports, gaming, fitness) | trap, phonk, jersey_club, dembow, liquid_dnb |
| Premium, minimal, quiet luxury | ambient_pulse, deep_house, bossa_electronica |
| Launch, reveal, hardware, science | cinematic_pulse, liquid_dnb, synthwave |
| Playful, maximal, Gen Z | hyperpop, jersey_club, uk_garage |

Two films for similar brands still get different genres: the registry decides between the candidates.

**The beatless option.** 29 percent of professional films have no clear pulse (pulse strength under 0.2): they are built on pads, swells, impacts, textures and interface sounds placed from picture cues, with no kick pattern at all. Linear's agent film is one opening impact and then quiet tones (percussive share 0.02); Raycast's is a swelling, almost entirely tonal piece; Monzo's effects follow the picture with no grid; Stripe's Sessions film carries 82 cuts on continuous texture. A beatless score still has a form, a motif, development, contrast and an ending; it just measures time in phrases and swells, not in a kick. In the kit set `"beat": false` in `music.json`: no drums, one long bass note per chord, rubato strums and hook, swells instead of crashes, and a stronger bed of off grid grains (`bed` 1.5, `bed_rate` 10). Its test films measured a pulse of 0.03 to 0.06. Cues then land where the picture says, not on a grid. Sketch it with `demo.py <genre> --beatless`, or a whole 30 s film with `demo.py <genre> --film --beatless`. Good for calm, premium, craft and reflective brands, and for any film whose last two predecessors had a beat.

| Genre | BPM (frames per beat) | Feel | What makes it recognisable |
|---|---|---|---|
| deep_house | 124 (29), 120, 116 | light swing | minor 9th organ stabs on the offbeat, a sung vowel lead |
| uk_garage | 133 (27), 129 | heavy swing | 2-step kick that skips beat 3, shuffled hats |
| trap | 144 (25), 138, 150 | half time | snare on 3, hat rolls in triplets, gliding 808 |
| boom_bap | 90 (40), 92, 95 | swung 8ths | lazy hats, chopped piano, upright bass |
| lofi | 75 (48), 80, 82 | heavy swing | tape wow, vinyl, detuned e-piano |
| liquid_dnb | 171 (21), 164 | straight | fast two-step breaks under slow warm chords, reese |
| amapiano | 112.5 (32), 109 | light swing | the log drum in call and response with the kick |
| afrobeats | 106 (34), 103, 100 | light swing | tresillo kick, interlocking rims and congas, plucked guitar |
| dembow | 95 (38), 97, 92 | straight | kick every beat, snare on the and of 1 and on 3 |
| synthwave | 106 (34), 100, 109 | straight | gated snare, 16th octave bass, wide saws |
| nu_disco | 116 (31), 120, 112.5 | slight swing | octave bass, string stabs, clav |
| breakbeat | 129 (28), 133, 124 | straight | broken beat with ghost snares, acid line |
| jersey_club | 138 (26), 144 | straight | the five kick bounce bar, vowel chops |
| minimal_techno | 129 (28), 124 | slight swing | one bar loop changing one part at a time |
| cinematic_pulse | 100 (36), 90, 106 | straight | string ostinato, taiko, brass swell |
| bossa_electronica | 112.5 (32), 120 | light swing | 3-2 bossa clave on a rim, nylon comping |
| phonk | 138 (26), 144, 133 | straight | phrygian cowbell riff over a blown 808 |
| hyperpop | 150 (24), 157 | straight | sugary supersaws, folded leads, glitch stutters |
| funk | 106 (34), 103, 109 | light swing | ghost note snares, clav, brass hook |
| ambient_pulse | 75 (48), 72, 80 | swung, sparse | glass pads, half time pulse, one vowel motif |
| afro_68 | 120 (30), 112.5, 106 in dotted quarters | 12/8 | the West African standard bell: a rolling triple feel |

Missing a genre the brand needs (bachata, k-pop, country, footwork, baile funk, gamelan)? Add it to `grooves.py` as data: tempos, swing, patterns, bass, chords, palette, fit, signature. Look the pattern up; do not guess it.

Render any candidate before committing: `audio/demo.py <genre> --key F# --mode dorian --bpm 112.5` writes an 8 bar sketch to `out/`. `demo.py all` renders every genre (about a minute).

## Tempo and the picture

At 60 fps a beat is 3600 / BPM frames. `grooves.FRAME_TEMPOS` lists the tempos whose beat is a whole number of frames; 24, 28, 32, 36, 40 and 48 frames per beat also give whole frame 16ths. Any tempo works (audio is exact and the picture rounds a 16th to the nearest frame), but whole frame beats keep structural cuts exactly on the beat.

Only structural cuts belong on a bar downbeat (act changes, the reveal, the end card). The kit measured that a cut on a downbeat rises 3 to 9 times over the baseline from the music alone, with no effect, so a film cut on every bar slams every cut even with no hits. Ordinary cuts fall with the action, between downbeats; professional cuts are barely more aligned with musical hits than chance (72 against 64 percent).

The tempo sets the cut rate. Shots of 1.5 to 4 s are 2 to 8 beats at 120; at 75 BPM a bar is 3.2 s, so acts change on bars and shots inside them fall with the action; at 171 BPM a bar is 1.4 s, so acts change every bar or two and the hats carry the speed.

## Key and mode

| Mode | Colour | Good for |
|---|---|---|
| ionian (major) | plain, bright, confident | friendly consumer, clear claims |
| lydian | wonder, floating, futuristic optimism (the raised 4th) | reveals, AI, space, "imagine" |
| mixolydian | sunny swagger (flat 7th) | food, social, groove, rock and funk |
| dorian | the hopeful minor, cool, jazzy (raised 6th) | creative tools, calm, house and lofi |
| aeolian (minor) | serious, emotional | drama, dark brands |
| phrygian | tense, exotic, aggressive (flat 2nd) | phonk, gaming, security |
| harmonic minor | dramatic, cinematic pull home | launches, trailers |
| pentatonics, hirajoshi | no clashes at all; sparse and precise | UI sounds, mallet melodies, Japanese minimalism |

Move the tonic between films too: four films in A, G and D is a habit, not a choice.

## Palette and signature

A palette is one instrument kind per role (`instruments.py`): kick, snare, hat, perc, bass, keys, pad, lead. Start from the genre's palette and change at least two roles, choosing by the brand's material: a wooden puzzle app gets mallets and nylon, a fintech glass and FM bells, a fitness app metal and distorted 808.

The signature is the one sound the viewer will remember, and the best ones come from the product:

- Sendoku: the digits of the real puzzle play a wooden mallet melody in the app's own pentatonic as they land.
- torq: iron plates slamming are the intro's rhythm.
- A camera app: the shutter as the snare. A payments app: a card tap as the clap. A keyboard app: typing as the hats.

Make it once, in the score, and give it the hook or the backbeat.

## Hooks

The hook is 3 to 6 notes in one bar, played as a call and answered (`theory.motif` and `theory.answer`); it is the film's motif (2 to 5 notes, `composition.md`, section 3) stated twice, developed through the film and restated at the logo. From the earworm research (Jakubowski et al. 2016): a common overall contour (rise then fall is the commonest), made memorable by one unusual interval or more repeated notes than usual, at a brisk tempo. So:

- Follow a contour mostly by step; break it once with a leap of a 4th to a 6th.
- End the call open (not on the tonic) and the answer closed (on the tonic).
- Repeat it. A hook heard four times in 30 s is remembered; one heard once is decoration.
- The end card's sonic logo is the hook's first 3 to 5 notes on the signature instrument, alone. That ties the mark to the music the way the Intel and Netflix idents do.

`motif(key, seed, contour)` writes one; change the seed until the contour sings, or write the notes by hand.

## Forms

The form is the order of energy. The picture's acts are named after its sections and cut on their starts (`SECTION` in `lib.ts`, `start()` in `cues.py`). Pick the one that tells this product's story, and never the same one with the same drop frame as the last film.

| Form | Shape | Use when |
|---|---|---|
| spine | hook, magic moment (half time), build, a breath, drop, stop, payoff, end card | one big reveal in the middle; used by the first four films with the gap at 45.8 percent every time, so move it or pick another |
| beatless | swells and phrases with no kick: an opening breath, textures under the working scenes, a swell into the reveal, one impact, a ringing end | calm, premium, reflective brands; one film in three |
| cold open | starts at full energy on frame 0 (`"opening": "cold"`, and `--cold-open` for the fingerprint), breaks down, rebuilds to the end card | the product's best moment can open the film |
| slow burn | one long crescendo, no drop; every section adds a part; the end card is the peak | calm brands, craft, a single continuous camera move |
| two drops | small drop at 4 to 6 s, breakdown, a bigger second drop at 18 to 22 s | two features of equal weight |
| beat switch | first half in one genre and tempo, a hard switch (half or double time, new genre) at the reveal | before and after, old way and new way |
| stop start | phrases separated by silences of a beat or two; each scene a phrase | punchy claims, kinetic type, comedy |
| minimal pulse | one motif repeating and changing one part at a time (Reich style), drums only at the end | precision, systems, data |
| call and response | picture and music take turns: a shot, then a musical answer, then a shot | interfaces with a back and forth (chat, search, hints) |

Parts in a section: drum part names from the genre (`kick`, `snare`, `hat`, `shaker`, ...), `drums` for all of them, `-hat` to leave one out, `bass`, `chords`, `pad`, `hook`, `hook_sparse` (every other bar), `fill` (snare roll in the last beat), `crash` (on the downbeat), `silence`.

Energy (0 to 1) scales levels and filters, but contrast comes from the parts, not the level. Before the biggest moment, a **breath** works in almost every form: a short section whose `parts` keep only something sustained (`["pad"]`, or `["chords", "pad"]`) so a tail or a held chord stays alive, then the next section comes back with the full arrangement, the first hit 20 to 70 ms after. Keep that breath near an eighth of a bar (`"bars": 0.125`, about 0.28 s at 105 BPM): a 0.57 s gap made the hero cut measure 27 times its baseline. For the return to feel big, the section before the breath must be thinner than the one after (fewer parts, closed hats, the bass out), never a fader moved down. The `silence` part (true silence) is for at most one or two moments per film, 100 to 300 ms right before a hit; 71 percent of professional films have no near silence at all. Set `"dips": 0`: the 2.0.0 engine's automatic dips (`"auto"`, about one per 7 s at -24 dB on the whole mix after the reverbs, and a 5 to 8 dB slide before the main one) are the gain holes the Enogon review heard. Why, and what the kit should do instead, is in `sound.md`, section 9. At most one lift or one drop per 30 s (`composition.md`, section 7).

Mark the section that gets the crash with `"hero": true` (by default only the highest energy section); the crash now plays only there.

## The music serves the picture

- The music needs a motif or groove, development, contrast and an ending. A set of whooshes and hits does not replace a composition, and a score that never changes ignores the edit.
- Sound and picture come from the same events (`music.json` sections and `cues.json`). After a speed ramp or a retimed shot, recompute the accents; never change the tempo or pitch by accident.
- Tie some cuts, reveals and ends of moves to expressive accents of the real music (a featured note, a hit, a change of phrase or harmony, a pause, the return of the rhythm), not every cut to every beat. Editing ranks rhythm third, behind emotion and story (Murch: rhythm is 10 percent of a cut's value), so meaning, reading time and a voice beat the beat. The accent map in `sound.md`, section 6, checks the chosen points against the rendered mix.
- How the music is made is free in principle; this skill writes it with the kit because that keeps it original, exact and repeatable, and has it performed by recorded CC0 instruments through the sampler (`"instruments": "samples"`), with synthesis as the fallback and for the signature sound (`sound.md`, section 4b). Do not rebuild a stack the user chose. VidIQ came up as a possible optional source of music or voice for a future task; it is not a dependency, not assumed free, and no voice was chosen.
- Custom scoring fits a film with an arc and hit moments; a single mood bed fits only a short, flat piece. Avoid temp tracks ("demo love" is hard to break), and avoid the stock "life is awesome" signals (corporate ukulele, handclaps, the uplifting pluck): if the brief is "upbeat", get it from rhythm and harmony, not from the stock instrument.

## Humanising the score

Professional onsets sit a median 0.105 of a 16th note off the tracked grid (about 13 ms at 120 BPM; 10th to 90th percentile 0.085 to 0.17), and 78 percent land within 25 ms of a 16th. The first three mgpro films sat at 0.047 to 0.093 with 91 to 100 percent on the grid, and Sendoku's beat intervals varied less than 99 percent of professional films'. But listening studies found that drums shifted by 15 to 25 ms were rated lower than quantised ones, and early shifts worse than late ones. Both hold when the looseness comes from the right places:

- Keep downbeats and structural hits exact.
- Vary velocity first: downbeats a little higher, offbeats lower, hats the most, kick and snare only slightly. Identical velocity and identical samples read as robotic more than grid timing does.
- Timing is systematic, not random (`sound.md`, section 4b, Performance): real players repeat their deviations bar to bar and shape them to the phrase (pushes of 5 to 15 ms early on phrase peaks and late into cadences), while ostinatos, arpeggios and the pulse stay locked, and listeners rate quantized grooves as well as or better than large random deviations. The kit's `humanize_ms` draws an independent offset per note, which is the weaker half: keep it at about 6 or below for pulse parts (a 3 to 6 ms offset only breaks sample identity) and put the feel in velocity contours and phrase pushes, written in `score.py`'s per film parts. Loosen late rather than early, more on hats, shakers and percussion than on kick and snare (default 12, the median offset of music onsets; never above about 15, where listeners start to rate grooves lower). Each part takes a share of it (`HUMANIZE` in `score.py`: kick 0.3, snare 0.55, hat and percussion 1.0, bass 0.45, chords 0.8, hook 0.7), the bar's kick downbeat stays exact, and velocity spreads by 6 percent (`grooves.hits(..., humanize, rng, lock, late, vel)`). A swung genre gets its swing from the genre's own feel, not from random jitter.
- Most of the professional off grid share comes from effects that follow the picture instead of the bar (`sound.md`, section 8). With them, 20 to 40 percent of the film's onsets end up off the 16th grid without any drum sounding sloppy.
- Velocity in a shape, not jitter: a spread of at least 20 points that drifts up over four bars and back down; with the sampler, velocity also changes the tone (velocity layers), so test velocity 40 against 110.
- Round robins: 6 to 8 alternates on anything repeated faster than about 4 per second; the sampler draws them from a bag that never repeats a take twice in a row.
- Change parts over time: drop the kick for a section, use half time, let a part enter late. Generators that flatten rhythm, timbre and dynamics are what makes AI music separable from human music on measured features alone (AIES 2026).

## Tonal balance

The first films were bright: median spectral centroid 2.3 to 3.0 kHz against a professional median of 1.8 kHz (10th to 90th percentile 1.0 to 2.6), rolloff 5.7 to 7.5 kHz against 4.0, and 1.5 to 3.4 percent of the energy above 6 kHz against a median 1.0. Bright hats and risers came and went over a dark sub, so the brightness also jumped more over time. Aim near the professional medians, a centroid around 1.8 kHz and a rolloff around 4 kHz (the fingerprint fails outside 982 to 2652 Hz and 1714 to 5927 Hz), with energy above 6 kHz under about 2 percent: low pass hats, shakers and risers, use fewer of them, and prefer a ride's ringing tone to a long noisy open hat. The kit's master shelves the mix toward those medians (`dsp.darken` inside `dsp.master`; `"tone": {"centroid": 1800, "rolloff": 4000}` in `music.json` is the default, `false` keeps the mix's own brightness), and `dsp.balance()` now aims at 0.1 to 1.5 percent above 8 kHz (it was 3 to 10, which brightened). Arrange darker first; the shelf is a safety net, not the sound. The low end is not the problem (the first films' share under 120 Hz, 0.35 to 0.55, sat around the professional median 0.45).

## Writing the score

`templates/kit/audio/` has everything; copy it into the project:

| File | What it gives |
|---|---|
| `dsp.py` | oscillators (band limited saw and square, FM, Karplus Strong), filters (including a sweeping low pass for acid and filter envelopes), envelopes (`dec(n, d20_ms)` by the part you hear; `perc()` still takes a time constant), `glide`, `pink`, `modal`, `repitch`, `spread`, saturation, folding, bit crushing, wow, buses, sidechain, reverbs, ping pong, `harmonics` (low end harmonics for small speakers), `darken` (tone toward the professional medians), the tonal balance check, `master(mix, lufs, tp, tone, bass_harmonics)` |
| `instruments.py` | 8 kicks, 8 snares and claps, 7 hats, 9 percussion, 10 basses (808 glide, reese, acid, log drum, upright...), 13 keys and mallets, 6 pads, 9 leads, vinyl |
| `grooves.py` | 21 genres as data, Euclidean and swing helpers, rolls, `hits()` with late leaning humanise, locked steps and velocity spread |
| `theory.py` | keys, modes, chords, voice leading, progressions by mood, Euclidean rhythms, motif and answer writers |
| `sfx.py` | one effect per job in the film's key and one of seven characters: tap, click, tick, blip, pop, text, toggle, card, chip, land, impact, boom, swish, whoosh, transition, panel, success, error, tier, logo, riser, reverse swell, sub drop, stutter, tape stop, texture (`sound.md` section 3) |
| `vary.py` | `Vary(film_seed, pool)`: a pool of takes per effect, a shuffled bag with no immediate repeat, pitch, level and loose start jitter; `python vary.py` self tests |
| `samples.py` | CC0 library sounds for effects (the `samples` block); copies them into `public/sfx/` and writes `ASSETS.txt`; `python audio/samples.py` lists each job's files |
| `sampler.py`, `sampler_map.json`, `fetch_instruments.sh` | recorded CC0 instruments for the score (`"instruments": "samples"`): an SFZ player with velocity layers, round robins, release samples, pedal and a convolution room; the library is fetched once outside the skill (`sound.md`, section 4b); `sampler.py --list`, `--demo piano` |
| `score.py` | the engine (`score.py [--root FILM_DIR]`): reads music.json and cues.json, plays the form, plans the dips (`plan_dips`), places each cue by its job (`JOBS`, `ALIASES`) and weight, mixes, masters, writes public/film.wav and prints loudness, LRA, opening, centroid, rolloff, grid offset, pulse, late density, planned and measured dips and RMS per section |
| `demo.py` | 8 bar sketches of any genre through the full chain (`demo.py <genre> [--beatless]`), or a 30 s film on the kit's example form with a sample cue list (`demo.py <genre> --film [--beatless --key --mode --bpm --seed]`, into `out/demo-film-<genre>/`) |
| `fingerprint.py` | the distinctness check against the registry and the professional range checks (`--checks` without a registry; `--build-stats ~/dev/mgpro-research/films` rebuilds `pro_stats.json`) |
| `filmstats.py`, `pro_stats.json` | the whole film measurement, a port of the research scripts (`analyze`, `cut_rise`, `shared_transients`, `profile_vector`, `video_cuts`), and the professional distribution it compares against |
| `sfx_catalog.py` | measures sounds like the CC0 library; `--synth-only --check` renders every effect in every character and prints it against the targets |

`score.py` plays the brief as written. Make it the film's own in its per film parts: the cue list's jobs and weights (`effects(cues, seconds, key, character, vary, samples)` plays them; unknown names are reported), special moments (the product's signature sound placed from cues), and any part the genre engine does not cover. Never paste in an earlier film's synth; the examples in `templates/examples/*/audio/synth.py` are there to read for mixing ideas only.

## Checking without ears

1. `score.py` prints integrated loudness (the destination's target, `sound.md` section 13), true peak (at or under -1 dBTP), LRA, the opening, centroid and rolloff (aim near 1.8 kHz and 4 kHz, see Tonal balance), grid offset, pulse, density at 75 to 85 percent, the planned and measured dips (none planned with `"dips": 0`), and RMS per section. No section reads more than about 6 dB under its neighbours unless it is a listed breath with a bed; then run the audio hole check in `review.md`.
2. `fingerprint.py --against` the registry with `--cues` and `--music`: every check must pass (exit 0). Report its table.
3. `composition.md`, section 10: the hit points on downbeats, the motif restated at the logo, no cliché progression as written, at most one lift or drop per 30 s.
4. A spectrogram: `ffmpeg -i public/film.wav -lavfi showspectrumpic=s=1600x400:legend=1:scale=log out/spec.png`. Look for walls of noise (a ride or open hat too long), empty lows, and that the sections read as the form.
5. Say it plainly in the reply: measured, not heard. Name the genre, tempo, key and signature so the user knows what to listen for.

## Sources

- Toussaint, The Euclidean Algorithm Generates Traditional Musical Rhythms (2005): https://cgm.cs.mcgill.ca/~godfried/publications/banff.pdf
- Jakubowski et al. on earworm melodies (contour, unusual intervals, tempo): https://www.livescience.com/56739-what-makes-an-earworm-so-catchy.html
- UK garage programming (2-step kick, swing): https://theproducerschool.com/blogs/featured-blogs/how-to-program-uk-garage-drums-complete-guide-for-producers
- Dembow pattern: https://www.ujam.com/tutorials/how-to-make-a-dembow-groove/
- Jersey club kick: https://blog.native-instruments.com/jersey-club/
- Amapiano log drum (tempo, FM, call and response): https://articles.roland.com/?p=67237 and https://violetrecording.com/how-to-make-amapiano-beats/
- House drum patterns: https://ampedstudio.com/blog/how-tomake-a-house-beat/
- Karplus Strong in numpy: https://kennethreitz.org/essays/2026-03-29-numpy_as_synth_engine
- Audio logos (short mnemonic from the brand theme): https://www.creativebloq.com/features/audio-logos and https://killerspots.com/blog/build-consistent-sonic-brand-system
- Mood and progressions (dorian as hopeful minor): https://blog.flat.io/music-notation-software-emotional-chord-progressions
- 129 professional films measured against the first three mgpro films (tempo, pulse, grid, brightness, dips, cross film distance): `sound-research.md`, section 1, with the film list and URLs.
- Microtiming studies (Frühauf, Kopiez and Platz 2013; Davies et al. 2013; Frontiers in Psychology 2016) and humanise settings (Splice, Logic): `sound-research.md`, section 9.
- AI music flattening rhythm, timbre and dynamics (Slendebroek and Metaxa, AIES 2026): https://ojs.aaai.org/index.php/AIES/article/view/43312
- Composition to picture, motifs, harmony, realism (round robins, systematic timing, shared rooms), CC0 instrument libraries and their licences, and why gain dips read as faults (Oct 29 2026, after the Enogon review): `research/ad-music-and-logo/report.md` and its `notes/`; the rules in `composition.md` and `sound.md`, sections 4b and 9.
- Murch's Rule of Six (rhythm 10 percent of a cut): https://nofilmschool.com/2016/11/6-rules-good-cutting-according-oscar-winning-editor-walter-murch
- Stock or custom, temp tracks (Wes Slover): https://www.bythebooth.com/insights/creative-tangent-wesley-slover-sound-the-invisible-brand-layer
