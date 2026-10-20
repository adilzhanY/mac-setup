# Sound: effects, mixing, mastering, and two case studies

**Music is decided in `music.md`**: every film gets its own genre, tempo, key, palette, hook and form, checked against the registry of earlier films. This file covers what is shared: the sound effect recipes, the mix and the master. The kit's audio library (`templates/kit/audio/`: dsp, instruments, grooves, theory, sfx, score, fingerprint) implements all of it; a run of `score.py` takes seconds.

## Principles

- One cue list drives sound and picture. Effects are placed from cue frames, never by ear.
- The music has a shape that follows the picture, and the shape is the film's own form (see `music.md`), not a fixed timeline.
- If the product has its own UI sounds, write the score in their key so the film's effects and the app agree, and make one of them the film's signature.
- Interface events are notes in the film's own scale (`sfx.blip(key, i, character)`), so runs of taps become phrases. Counts and progress rise in pitch.
- Repeated sounds vary: random pitch, filter, level (plus or minus 1 dB), so nothing sounds like a machine gun.
- Keep 1 to 4 kHz clear enough for interface sounds to read over the music.

## Case studies (read, never reuse)

These two scores are what the first films used. They are here to show how an arrangement follows a picture, not as templates: their tempo (120), groove (four on the floor with the same bouncy bass), palette and frames are taken. A new film that resembles them fails the fingerprint check.

### Bauwerk (30 s, 120 BPM, G major, taken)

| Frames | Section | What plays |
|---|---|---|
| 0 to 240 | intro | Cmaj9, Em7, Dadd9. FM e-piano comping (beat 1, the and of 2, beat 4) low passed at 1600 Hz, soft pad, snaps on 2 and 4 from frame 60, swung 16th shaker (55 percent swing). No kick. |
| 240 | lift | Gadd9. Four on the floor kick, bouncy bass (sub sine plus plucky saw an octave up, octave jumps on off 16ths), offbeat closed hats, first clap. A low boom on the downbeat. |
| 360 to 600 | the AI reads | Am9, Em9 in half time (kick on 1 and the and of 3, rim snap on 3), pulsing 8th bass whose filter opens over two bars, an octave-up chorused shimmer pad, no claps. |
| 600 to 825 | build | Cmaj7, Dadd9. Kick back, offbeat e-piano stabs getting brighter, bass 8ths then 16ths, hats building in 16ths, synths thinning like an opening high pass, snare roll 8ths, 16ths, 32nds, 64ths, louder and brighter. |
| 825 to 840 | gap | dead silence (only a riser tail). |
| 840 to 1290 | drop | G, D/F#, Em7, Cmaj9. Crash, claps layered with snaps, open hats on offbeats, supersaw stabs on off 8ths, a two bar plucked hook in call and response with a dotted 8th ping pong delay. |
| 1290 to 1320 | stop | one beat of silence; only the success chime rings in it. |
| 1320 to 1530 | groove | G, Cmaj9, Dadd9, crash on the hit, no hook. |
| 1530 to 1560 | swell | drums out, reverse cymbal into the end. |
| 1560 | end | a big Gadd9 (e-piano, pad, supersaw, sub, kick, crash) ringing out, the bell chime at 28 s, fade from 28.3 s to silence at 29.8 s. |

Mix automation (level per section) made the shape: intro 0.42, lift 0.68, AI 0.5, build ramping 0.45 to 0.8, drop 1.0, groove 0.92, end 0.95. Measured RMS per section: intro -21 dB, lift -17, AI -18, build -17, gap -40, drop -15.4, groove -16, end -15 then silence.

### torq (30 s, 120 BPM, A minor, taken; Sendoku reused this groove and the user heard it)

| Frames | Section | What plays | RMS |
|---|---|---|---|
| 0 to 240 | intro | dark sub swell, low passed Am(add9) pad, ticking filtered 16th hats, snaps on 2 and 4 from frame 60, no kick. The three plate slams (30, 60, 90) are the rhythm | -19.1 dB |
| 240 to 420 | lift | four on the floor, bouncy distorted bass, offbeat hats, claps; Am, F, C, G per bar; boom on 240 | -16.7 |
| 420 to 600 | engine | half time, Am9 to Fmaj7, shimmering pad, pulsing 8th bass opening, no claps | -18.7 |
| 600 to 825 | build | kick back, Dm, F, G, E (the dominant for tension), snare roll 8ths to 64ths, synths high passing open | -17.9 |
| 825 to 840 | gap | dead silence | -55.8 |
| 840 to 1290 | drop | crash, Am F C G, claps and snaps, open hats, supersaw stabs, plucked hook with a dotted 8th ping pong | -14.3 |
| 1290 to 1320 | stop | only the chime | -21.4 |
| 1320 to 1530 | groove | no hook, crash on 1320 | -15.2 |
| 1530 to 1560 | swell | drums out, reverse cymbal ending on 1560 | -21.3 |
| 1560 to 1800 | end | big chord, bell at 1680, fade from 28.3 s to silence at 29.8 s | -16.9 |

The drop measured 3.6 dB above the build, enough to read as the biggest moment. Watch for hiss: 16th hats, a 64th snare roll and a crash stacked from 10 s on put a lot of energy above 8 kHz; pull them down if the user says it sounds harsh. The effects bus sat at 0.5 against the music; at 1.0 the effects buried the intro and the build.

## Instrument recipes (now in `templates/kit/audio/instruments.py`, with many more kinds)

- **Kick**: sine with pitch envelope 47 + 125 e^(-t/0.028) + 30 e^(-t/0.004) Hz, body decay 0.19 s, plus a 2.5 to 8 kHz noise click (2 ms), tanh saturation 1.7.
- **Clap**: four noise bursts 0, 8.5, 18, 27 ms apart (4 ms decays) plus a 0.1 s tail, band passed 900 to 2300 Hz layered with 1.5 to 6 kHz, slightly different per channel, short room reverb.
- **Snap**: 1.7 to 6 kHz noise crack (3 ms) plus a 2150 Hz ring (11 ms).
- **Shaker**: high passed noise (5.5 kHz, 4th order), 12 ms attack, 25 ms decay, swung 16ths.
- **Hats**: six square waves at 808 ratios (205.3, 304.4, 369.6, 522.7, 540, 800 Hz x 1.6) plus noise, band passed 7 to 15 kHz. Closed 0.02 to 0.035 s, open 0.16 s.
- **Snare (rolls)**: 180 Hz body with a pitch blip plus 1.8 to 9 kHz noise rattle, high pass rising with the roll.
- **Crash**: high passed noise plus 18 random metallic partials 3.2 to 9.5 kHz, 0.75 s decay, two decorrelated channels.
- **FM electric piano (DX7 style)**: body sin(2 pi f t + idx sin(2 pi f t)) with idx 0.25 + 1.5 v e^(-t/0.35), plus a metallic tine at a 14:1 modulator ratio (decay 45 ms). Chords strummed 4 ms per note, low passed per section, chorus plus reverb.
- **Pad**: band limited saws (drawn at 4x and resampled to avoid aliasing) detuned 0, plus and minus 7 and 13 cents, panned, low passed, slow attack, chorus and a big reverb.
- **Supersaw stabs**: seven saws at 0, plus and minus 11, 21, 31 cents, wide, low passed 6 kHz, short decay, high passed 280 Hz.
- **Bass**: sub sine on the root plus a saw an octave up through a fast closing filter (2200 to 260 Hz, 70 ms), tanh 1.3, compressed. Bouncy pattern in 16ths: (step, interval, length) (0,0,2) (3,12,1) (6,0,1) (8,0,2) (10,12,1) (11,7,1) (14,12,1).
- **Pluck (hook)**: two saws slightly detuned, filter envelope 8 kHz to 1.1 kHz over 50 ms, a sine sparkle an octave up, plus a quiet octave layer panned right.
- **Marimba**: sine fundamental (0.22 s) plus 4th partial (40 ms) plus a mallet noise click.
- **FM bell**: sin(2 pi f t + idx sin(2 pi f r t)), idx decaying from about 3, ratio 2 to 3.5.

## Effect recipes (cue name: recipe; `sfx.py` has key aware versions with a material character)

- click: band passed noise press (1.2 ms) plus a 3.1 kHz ping plus a 380 Hz body; a quieter release 75 ms later.
- key: noise top at a random 2.8 to 4.6 kHz centre, a 170 to 240 Hz thock (lower and longer for space with a rattle 30 ms later), a 0.5 to 1.6 kHz clack; random level.
- tick: 1.8 kHz x pitch sine (12 ms) plus a noise click.
- whoosh: pink noise band passed with a centre sweeping 350 to 2600 to 600 Hz, panned left to right, sin^2 envelope; its peak lands on the cue frame.
- pin: pitched tock 1100 to 520 Hz plus a 110 Hz thump.
- riser: noise with a high pass rising 400 Hz to 9 kHz plus three log chirps up an octave, amplitude k^2.2; it ENDS on its frame.
- boom (impact, hit, final): sine body 38 + 55 e^(-t/0.09) Hz, 0.35 s decay, plus a low passed noise burst, tanh; the music ducks about 3 dB under it for 0.6 s.
- rumble: low passed brown noise under 180 Hz, sin envelope.
- shimmer: 28 tiny FM bell grains per second from the high pentatonic at random pans and levels (-20 to -8 dB) plus 6.5 to 11 kHz air.
- trace: one FM pluck per traced line rising up the G major pentatonic, alternate panning.
- room: marimba notes on chord tones.
- detect: FM bell, note = pentatonic[5 + 2 row + col]: each row a rising phrase starting higher than the last, panned by column.
- glass: tiny high sine tings, random pentatonic notes 20 to 27, random pans, very quiet (the drop's window cascade).
- scan: band passed noise sweeping 6.5 kHz down to 900 Hz (the beam goes down).
- build: rising 70 to 190 Hz tone plus rumble (walls rising).
- thud: low band noise plus a 90 Hz body (a card landing).
- join: upward pitch pop (380 to 820 Hz in 40 ms) at rising pitches per person.
- dots: three soft ticks 130 ms apart (typing indicator).
- message: short upward noise swish (1.2 to 6 kHz) then a pop 100 ms later (original, not a copy of any OS sound).
- grab: low passed noise plus 300 Hz (a soft grip).
- slider: detent ticks, pitch 1300 Hz x 2^((value - 1)/16), one octave over the range.
- roll: four fast ticks 24 ms apart, pitched higher as the class improves (slot machine flip).
- toggle: click then a pop.
- sweep: band passed noise rising 3 to 11 kHz panned across plus five rising bell notes (light across glass).
- chime: three FM bells (D5, G5, B5) 80 ms apart; success: two bells.
- count: ticks rising 900 Hz x 2^(i/28).
- paper: crinkle from cubed noise through a slow envelope, panned across.
- reverse: a crash reversed and ramped (ends on its frame plus seconds).
- block: marimba plus a quiet bell an octave up (logo blocks, rising notes).
- bell: three FM bells (G5, D6, G6) for the close.

Added for torq (dark, physical):

- slam: a heavy iron plate hit: a 50 Hz body with a fast pitch drop, inharmonic metallic clang partials between 300 and 2500 Hz with a short ring, pitch rising a little per plate.
- collar: a sharp metal click.
- zip: a rising filtered noise zip as a line draws.
- set: the app's own set done blip (E5 plus A5), rising per set.
- pr: a quick bright run (E5, G5, C6, E6) for a record.
- rest, go: a quiet A4 tick for each countdown second, A5 plus E6 at zero.
- grain: a tiny tick per landing particle at random pitch, very soft (a run of 30 on 32nds reads as rain).
- tier: a metallic hit plus an FM bell rising with the tier index, each brighter (a metal being upgraded).
- swap: a short whoosh plus an upward pop when a row overtakes another.
- blip: rising pentatonic blips for a run of fills (week dots).
- A riser always ENDS on its frame; a reverse cymbal cue at frame F with seconds s plays from F minus s to F. Say which in the brief to the sound agent.
- bloom: a soft G chord swelling with filtered air (the search pill opening).

## Mixing

- Buses: drums, percussion, keys, pad, stabs, bass, hook, effects. Room reverb on percussion, chorus plus reverb on keys and pad, high pass on stabs, dotted 8th ping pong on the hook, compression on bass (3:1) and drums (2.5:1).
- Sidechain: keys, pad, stabs and hook duck under every kick (`dsp.duck_curve`, depth per genre: 0.45 for house, 0.2 for lofi, none for cinematic); the bass ducks 1.3x as deep.
- Tonal balance: `dsp.balance` keeps 3 to 10 percent of the energy above 8 kHz and 15 to 55 percent under 150 Hz, correcting with gentle shelves and printing what it did. Long open hats and rides are the usual cause of a hissy mix; a ride is mostly ringing tone, not noise.
- The build thins the synths toward the drop by crossfading to a 900 Hz high passed copy.
- Dead stops are cut with 4 ms ramps.
- Effects bus gets a light room (size 0.3, wet 0.1). Gains per effect: interface sounds 0.7 to 0.9, textures 0.3 to 0.6, AI notes about 0.3.

## Mastering

- High pass 28 Hz, gentle glue compression (threshold -16 dB, 1.8:1, 25 ms attack, 160 ms release).
- Loudness to -14 LUFS integrated (pyloudnorm), then a look ahead limiter whose gain follows the 4x oversampled peak, iterate until the true peak is at or below -1 dBTP (measure on a 4x oversampled signal). Result: -14.00 LUFS, -1.38 dBTP.
- Write 48 kHz, 24 bit stereo, exactly the film length.

## Checking audio without ears

- Print integrated loudness, true peak and RMS per 0.5 s; compare the curve with the arrangement (it must dip at the gap and the stop and rise at the drop).
- Draw `ffmpeg -i a.wav -lavfi showspectrumpic=s=1600x400:legend=1:scale=log` and `showwavespic` and look at them.
- Run `audio/fingerprint.py --against` the registry (see `music.md`); it must report the score distinct.
- Then say honestly in the reply: measured, not heard; ask the user to listen with sound.
- Weak spot to watch: the drop was only 2 to 3 dB above the build in RMS; it relies on density (sub, stabs, hook). If the user says it is flat, widen that gap.
