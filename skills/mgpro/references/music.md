# Music: a new score for every film

Every film gets its own music: its own tempo, groove, key, palette, hook and form. Four films were made with this skill before this file existed, all at 120 BPM, and the Sendoku score reused the torq score's groove almost note for note (fingerprint: groove 0.98, harmony 1.00, palette 0.80). The user heard it straight away: "the rhythm is identical which is kinda bad". A score that sounds like the last ad makes the product sound like the last product.

The cause was in this skill: a fixed 120 BPM grid, one arrangement with fixed frames (gap 825, drop 840, stop 1290), one palette list, and the instruction to start from an example synth. All four are gone. What replaces them is below.

## The contract

A new score must differ from EVERY film in `music/registry.json` in all of these:

1. **Genre or groove family.** Not the same genre, and not the same kick pattern (four on the floor twice in a row counts as the same).
2. **Tempo.** At least 6 BPM away from any film whose groove is similar, and not 120 again by habit. Pick from the genre's own range.
3. **Key and mode.** Not the same key and mode as the last three films.
4. **Palette.** A different bass kind and a different lead kind. The kick may repeat only if the genre differs.
5. **Form.** The big moment (drop, reveal, switch) at a different place, or a different kind of form altogether.
6. **Signature.** One sound nobody else has, ideally taken from the product (see below).

Then it must pass the measurement: `audio/fingerprint.py public/film.wav --bpm <bpm> --against ~/.claude/skills/mgpro/music/registry.json` exits 0 (groove under 0.85, harmony under 0.97, palette under 0.70, form shape under 0.70 against every earlier film). If it fails, change the groove, tempo, palette or form, not the thresholds.

When the film is finished, append it to the registry (the command prints the measured part; add the choices by hand).

## The sonic brief (`src/music.json`)

Decide these before the script, because the form decides where the picture cuts. One file feeds the picture (`lib.ts` reads tempo and section starts), the cue list (`cues.py`) and the score (`score.py`). The kit has a filled example.

| Field | What it is | How to decide |
|---|---|---|
| genre | one of `grooves.GENRES` (or two for a beat switch) | brand traits table below, minus what the registry has used |
| bpm | from the genre's `tempos` (whole frames per beat at 60 fps) | the picture's energy; faster tunes stick better (Jakubowski 2016), but match the cut rate |
| key, mode | tonic and one of `theory.MODES` | the mood table below; the product's own UI sounds' key wins if it has any |
| mood, progression | a `theory.PROGRESSIONS` mood, or your own numerals | what the viewer should feel at the drop |
| palette | role to instrument kind (kick, snare, hat, bass, keys, pad, lead, plus genre roles) | genre default, then change at least two roles so it is this film's |
| drums | pattern overrides per part | rewrite at least one part (move a kick, add a percussion line) |
| hook | seed, contour, notes, register | see Hooks |
| signature | one sentence | see Signature |
| character | sfx character: glass, wood, metal, digital, soft | what the interface is made of |
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

At 60 fps a beat is 3600 / BPM frames. `grooves.FRAME_TEMPOS` lists the tempos whose beat is a whole number of frames; 24, 28, 32, 36, 40 and 48 frames per beat also give whole frame 16ths. Any tempo works (audio is exact and the picture rounds a 16th to the nearest frame), but whole frame beats keep cuts exactly on the beat.

The tempo sets the cut rate. Shots of 1.5 to 4 s are 2 to 8 beats at 120; at 75 BPM a bar is 3.2 s, so cut on bars and half bars; at 171 BPM a bar is 1.4 s, so cut every bar or two and let the hats carry the speed.

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

The hook is 3 to 6 notes in one bar, played as a call and answered (`theory.motif` and `theory.answer`). From the earworm research (Jakubowski et al. 2016): a common overall contour (rise then fall is the commonest), made memorable by one unusual interval or more repeated notes than usual, at a brisk tempo. So:

- Follow a contour mostly by step; break it once with a leap of a 4th to a 6th.
- End the call open (not on the tonic) and the answer closed (on the tonic).
- Repeat it. A hook heard four times in 30 s is remembered; one heard once is decoration.
- The end card's sonic logo is the hook's first 3 to 5 notes on the signature instrument, alone. That ties the mark to the music the way the Intel and Netflix idents do.

`motif(key, seed, contour)` writes one; change the seed until the contour sings, or write the notes by hand.

## Forms

The form is the order of energy. The picture's acts are named after its sections and cut on their starts (`SECTION` in `lib.ts`, `start()` in `cues.py`). Pick the one that tells this product's story, and never the same one with the same drop frame as the last film.

| Form | Shape | Use when |
|---|---|---|
| spine | hook, magic moment (half time), build, half a beat of silence, drop, stop, payoff, end card | one big reveal in the middle; used by the first four films, so move it or pick another |
| cold open | starts at full energy on frame 0, breaks down, rebuilds to the end card | the product's best moment can open the film |
| slow burn | one long crescendo, no drop; every section adds a part; the end card is the peak | calm brands, craft, a single continuous camera move |
| two drops | small drop at 4 to 6 s, breakdown, a bigger second drop at 18 to 22 s | two features of equal weight |
| beat switch | first half in one genre and tempo, a hard switch (half or double time, new genre) at the reveal | before and after, old way and new way |
| stop start | phrases separated by silences of a beat or two; each scene a phrase | punchy claims, kinetic type, comedy |
| minimal pulse | one motif repeating and changing one part at a time (Reich style), drums only at the end | precision, systems, data |
| call and response | picture and music take turns: a shot, then a musical answer, then a shot | interfaces with a back and forth (chat, search, hints) |

Parts in a section: drum part names from the genre (`kick`, `snare`, `hat`, `shaker`, ...), `drums` for all of them, `-hat` to leave one out, `bass`, `chords`, `pad`, `hook`, `hook_sparse` (every other bar), `fill` (snare roll in the last beat), `crash` (on the downbeat), `silence`.

Energy (0 to 1) scales levels and filters. A gap of a beat or half a beat (`"bars": 0.25` or `0.125` in 4/4) with `silence` before the biggest moment works in almost every form; vary where it falls.

## Writing the score

`templates/kit/audio/` has everything; copy it into the project:

| File | What it gives |
|---|---|
| `dsp.py` | oscillators (band limited saw and square, FM, Karplus Strong), filters (including a sweeping low pass for acid and filter envelopes), envelopes, saturation, folding, bit crushing, wow, buses, sidechain, reverbs, ping pong, the tonal balance check, the master |
| `instruments.py` | 8 kicks, 8 snares and claps, 7 hats, 9 percussion, 10 basses (808 glide, reese, acid, log drum, upright...), 13 keys and mallets, 6 pads, 9 leads, vinyl |
| `grooves.py` | 21 genres as data, Euclidean and swing helpers, rolls |
| `theory.py` | keys, modes, chords, voice leading, progressions by mood, Euclidean rhythms, motif and answer writers |
| `sfx.py` | effects in the film's key with a material character: blips, ticks, clicks, whooshes, risers, reverse swells, impacts, sub drops, chimes, stutters, tape stops, textures |
| `score.py` | the engine: reads music.json and cues.json, plays the form, mixes, masters, writes public/film.wav and prints loudness, balance and RMS per section |
| `demo.py` | 8 bar sketches of any genre |
| `fingerprint.py` | the distinctness check against the registry |

`score.py` plays the brief as written. Make it the film's own in its per film parts: the `effects()` map (one designed sound per cue name, unknown names are reported), special moments (the product's signature sound placed from cues), and any part the genre engine does not cover. Never paste in an earlier film's synth; the examples in `templates/examples/*/audio/synth.py` are there to read for mixing ideas only.

## Checking without ears

1. `score.py` prints integrated loudness (-14 LUFS), true peak (at or under -1 dBTP), the balance (3 to 10 percent above 8 kHz, 15 to 55 percent under 150 Hz; it corrects gently and says so) and RMS per section. The gap and stop sections should read below -50 dB; the biggest section 2 to 5 dB above the build.
2. `fingerprint.py --against` the registry: must print "Distinct from every earlier film."
3. A spectrogram: `ffmpeg -i public/film.wav -lavfi showspectrumpic=s=1600x400:legend=1:scale=log out/spec.png`. Look for walls of noise (a ride or open hat too long), empty lows, and that the sections read as the form.
4. Say it plainly in the reply: measured, not heard. Name the genre, tempo, key and signature so the user knows what to listen for.

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
