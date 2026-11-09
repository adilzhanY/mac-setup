# Sound effect vocabulary of professional motion graphics and how each sound is designed

Scope note: the web sources reachable in this session were mostly practitioner blogs, vendor tutorials, forum threads and two code-synthesis devlogs. School of Motion, Sono Sanctus, GDC Vault and Material Design pages either returned no body text or had no technical detail. Numbers below are labelled with their source. Where a number comes only from a search-result snippet (not a fetched page) it says "snippet". Everything in the Inferences sections is the researcher's own synthesis for a numpy implementation and is not a sourced fact.

## 1. What are the sound types and which visual event triggers each one?

### Takeaway
Motion graphics sound is a small vocabulary of functional roles: movement (whoosh, swish), anticipation (riser, reverse swell), arrival (impact, hit, sub drop, click, pop), identity (tonal hit, sting, logo sonic mark), and glue (bed, texture, ambience). The rule practitioners repeat is that a movement sound follows speed, mass, direction and stopping point, and a landing sound (impact, click, pop) fires only when an object visibly stops, attaches or appears.

### Cited Findings
- Motion graphics sound design is described by Adobe Research as having "unique challenges due to their short, abstract nature" (CHI 2026 paper, MoSound). [Adobe Research, MoSound](https://research.adobe.com/publication/mosound-an-interactive-tool-for-generative-sound-design-in-motion-graphics/)
- Whoosh duration by visual event: quick UI swipes and fast cuts about 0.25 to 0.5 s; general range 0.5 to 1 s; big title reveals and slow push-ins 1 s or longer. Time the loudest point of the whoosh to land on the cut. [Violet Recording, How to Make Whoosh Sounds](https://violetrecording.com/how-to-make-whoosh-sounds/)
- Weight by subject: light, airy whooshes for text, menus and delicate graphics; dark, distorted, low-passed whooshes for heavy objects and trailer cuts. [Violet Recording, whooshes](https://violetrecording.com/how-to-make-whoosh-sounds/)
- A layered whoosh is split by function: an air layer defines broad motion and duration, plus texture, tonal and landing layers. The landing layer (impact, click or pop) is used "only when the object visibly stops, attaches, or appears" (snippet). [Aisha Sound, Whoosh Sound Design](https://aishasound.com/blog/whoosh-sound-design-a-practical-guide)
- A convincing whoosh follows the motion's speed, mass, direction, distance and stopping point (snippet). [Sonilo, Whoosh Sound Effect guide](https://sonilo.com/ai-music/whoosh-sound-effect-guide)
- For motion graphics, combine a movement sound (whoosh) with a stronger impact or hit at the end of the animation (snippet). [Pixflow, cinematic transition sounds](https://pixflow.net/blog/enhancing-motion-graphics-with-cinematic-transition-sounds/)
- Timing: a whoosh placed slightly before a visual change creates anticipation; placed exactly on the cut it reinforces clarity. Constant motion sound tires the ear and flattens dynamics (snippet). [Soundgrail, movement and flow](https://soundgrail.com/blog/shape-movement-and-flow-in-modern-sound-design)
- Transitions: whooshes, swishes and fades; starting a sound from the next scene slightly early eases the viewer into the change. Avoid too many cuts landing on the same beat, which pulls focus. [Pitchdrift, 20 sound design tips for motion graphics](https://pitchdrift-productions.com/sound-design-tips-for-motion-graphics/)
- Risers: one or two beats for a quick lift, one to several bars for a general build, four to eight bars for big tension into a main drop. Peak the riser on beat one of the new section, then cut or duck it. A falling pitch or filter sweep (downlifter) at the drop releases tension. [Violet Recording, Risers and Sweeps](https://violetrecording.com/how-to-make-risers-and-sweeps/)
- UI sound durations by action (procedural UI sound library): click 30 to 120 ms ("short percussive tap"), hover 15 to 45 ms ("subtle presence"), navigation 80 to 450 ms ("frequency sweep, whoosh"), success 100 to 300 ms ("ascending tone"), error 150 to 600 ms ("vibrato alert"), delete 80 to 300 ms ("descending warning"), loading 20 to 200 ms ("repeating pulse"). [ui-sounds.com](https://ui-sounds.com/)
- Another vendor guide: taps and clicks 80 to 150 ms, hovers 120 to 200 ms, notifications 200 to 600 ms, transitions 300 to 1000 ms; a game audio guide puts micro-interaction sounds at about 100 to 300 ms (snippets). [SFX Engine, click sounds](https://sfxengine.com/blog/sound-effects-click); [SFX Engine, game UI best practices](https://sfxengine.com/blog/best-practices-for-game-ui-sounds). Note: these conflict with ui-sounds.com on hover (15 to 45 ms versus 120 to 200 ms).
- UI sound roles (Material-style taxonomy, from a search snippet of a UI sound design handbook): sound as feedback, sound as decoration, hero sounds, notifications; sound must never be the only carrier of essential information. [DesignCode, UI Sound Design](https://designcode.io/ui-design-handbook-ui-sound-design) (page body not retrievable, snippet only)
- UI set roles: click/press short and crisp; hover a subtle tick; confirm/success positive, rising, bright; cancel/back softer and neutral; error short, lower, blunt buzz; notification a light chime. Keep every UI sound brief and quiet. [Voidless.dev, Generating UI sound effects](https://voidless.dev/tutorials/sound-effects/generate-ui-sound-effects)
- Priority: navigation sounds smallest and lightest, select slightly bigger with more layers, confirm the biggest and most detailed (snippet). [SFX Engine, game UI best practices](https://sfxengine.com/blog/best-practices-for-game-ui-sounds)
- Practitioner example (Krotos interview, Rubik's cube spot): a warm musical bed for a calm background space; swirly synths pitched to follow the cube's spins and shifts; "bubbly sounds and rubbery stretches that rise and fall in pitch" when cubes morph into spheres; discrete spinning swishes as movement accents; a wave sound that grows as the camera moves closer. [Krotos, 6 tips for motion graphics](https://krotos.studio/blog/sound-effects-motion-graphics-tips)
- Braam: layered low brass plus synth plus sub, distorted, used as a trailer-style hit; it shares the bass range with the music, so both at full weight "turns to mud" (snippets). [IRPR, Braam glossary](https://sounddesign.irpr.agency/glossary/braam/); [VI-Control, making braams](https://vi-control.net/community/threads/making-braams.121447/)
- Brand consistency: jingles or sonic logos, and subtly referencing the brand sound in the music. [Pitchdrift](https://pitchdrift-productions.com/sound-design-tips-for-motion-graphics/)

### Inferences
- Event to sound map for a code pipeline (synthesised from the above):
  - Element slides or flies in: whoosh, length equals the tween length (0.25 to 0.5 s for UI, 0.5 to 1 s for cards, 1 s plus for hero type), peak aligned to the frame of maximum velocity or to the cut.
  - Element lands, snaps, docks: click (small), pop (round or bubbly element), thud plus click (card), impact (hero).
  - Scene change or hard cut: whoosh into a hit, or riser ending exactly on the cut with silence or a sub drop after.
  - Build-up before a reveal (logo, product shot, headline): riser or reverse swell, 1 to 4 s at ad tempos, ending on the reveal frame.
  - Reveal: tonal hit or sting plus sub drop plus shimmer tail.
  - Cursor hover, toggle, checkbox, counter tick: UI ticks in the 15 to 120 ms class.
  - Success state, checkmark: rising two or three note tonal motif.
  - Error, shake: falling pair or dissonant semitone.
  - Number counters and data visualisations: rapid ticks or data blips at the counter rate, pitch rising with value.
  - Glitch transitions: glitch bursts (see section 2 inferences).
  - Logo sting: riser into tonal hit, sub, shimmer and reverb tail, 2 to 4 s total.
- Because motion graphics are short and abstract (MoSound), sounds should be read as gestures that describe motion and weight, not literal foley.

### Gaps
- No primary School of Motion or Sono Sanctus text describing their SFX taxonomy was retrievable (podcast pages have no transcripts). [School of Motion, Sono Sanctus podcast](https://schoolofmotion.com/blog/sono-sanctus-podcast-podcast)
- No source in this session gave concrete numbers for glitches, shimmers, data sounds or textures/beds in motion graphics.

## 2. How are they built? Layering, synthesis, processing and parameter values

### Takeaway
Every sourced recipe reduces to: filtered noise with a moving cutoff plus pitch movement for whooshes and risers; a sine with a fast downward pitch envelope plus a noise click for booms and sub drops; transient plus body plus sub plus tail for impacts, all aligned to one transient; and short enveloped sines or soft squares (with a 0.5 to 2 ms attack, exponential release and a fade to zero) for UI sounds. Each layer owns its own frequency band, with a single layer owning the sub.

### Cited Findings

Whooshes and swishes
- Starter recipe: filter sweep on noise rising then falling over about 0.8 s; low-pass or band-pass, cutoff rising then falling. A fast sweep sounds sharp and quick, a slow sweep heavy and grand. [Violet Recording, whooshes](https://violetrecording.com/how-to-make-whoosh-sounds/)
- Volume envelope swells into the centre then fades out the back; a gentle pitch rise lifts energy at the peak, a falling pitch suggests something leaving or settling. Doppler: raise pitch as it approaches, lower as it passes. Pan across the field (L to R or R to L), add a little stereo width, a short reverb tail for size; a pitched delay gives a sci-fi character; a little distortion for aggressive whooshes. [Violet Recording, whooshes](https://violetrecording.com/how-to-make-whoosh-sounds/)
- Pink or filtered noise sounds smoother than white noise; if using white noise, roll off the top end. Two or three layers: airy noise body, a recorded texture (moving air, whipped cable, fabric, breath), optionally a low rumble, processed together. [Violet Recording, whooshes](https://violetrecording.com/how-to-make-whoosh-sounds/)
- Krotos: four layers with complementary characters, for example an airy high-frequency noise layer and a liquid texture layer; long broad-spectrum sources work best because short punctuated sounds disrupt the flow; bigger objects get lower, slower sounds (snippets). [Krotos, Whoosh tutorial](https://sound.krotosaudio.com/whoosh-sound-effects/)
- Layered whooshes need their frequencies carved to make room for each other plus some compression to tie them together; group all layers to one bus and automate volume on the group (snippets). [Krotos Studio, whoosh presets](https://krotos.studio/blog/whoosh-sound-effects-krotos-studio); [Pixflow, cinematic whooshes](https://pixflow.net/blog/cinematic-whoosh-sound-effects/)
- Classic reference: Charles Deenen's "100 whooshes in 2 minutes" (Designing Sound, 2010) and the Designing Sound whoosh review are standard practitioner references (not fetched). [Designing Sound, Deenen special](https://designingsound.org/2010/02/charles-deenen-special-100-whooshes-in-2-minutes/)

Risers, reverse swells, downlifters
- Noise riser: white or pink noise through band-pass or high-pass, cutoff opens over the build. Pitch riser: sustained saw or wavetable with pitch automated upward. Shepard riser: several octaves of the rising motion with the top and bottom layers faded so the rise never resets. [Violet Recording, risers](https://violetrecording.com/how-to-make-risers-and-sweeps/)
- Avoid a linear rise (mechanical); an exponential curve that accelerates near the end builds more tension. Automate width so the riser opens as it peaks. High-pass the riser; full-range noise piles up energy below 100 Hz and clashes with the kick at the drop. Choose one primary motion (filter for noise risers, pitch for tonal ones) rather than climbing pitch, filter and volume all at full strength. [Violet Recording, risers](https://violetrecording.com/how-to-make-risers-and-sweeps/)
- Reverse sources: reversed reverb tails, cymbal swells, vocals; bounce a crash or snare with a long tail, reverse it, automate a filter across it. [Violet Recording, risers](https://violetrecording.com/how-to-make-risers-and-sweeps/); [VI-Control, riser/uplifter thread](https://vi-control.net/community/threads/riser-uplifter-effects.172558/)
- Noise layer of a riser at about -6 dB relative so it does not overpower the tonal riser, with a slow steady cutoff rise (snippet). [Unison, How to create risers](https://unison.audio/how-to-create-risers/)
- Noise through a low-pass with a small resonance bump and automated cutoff; pitch modulated by an envelope with a long slow attack (snippet). [MusicRadar, synth sweep FX](https://www.musicradar.com/how-to/synth-sweep-fx)
- Serum riser: LFO to oscillator pitch, eight unison voices for width (snippet). [SoundBridge, white noise riser](https://soundbridge.io/en/create-a-perfect-white-noise-riser)

Impacts and hits
- Layer roles: transient (short bright noise burst or snappy snare, tail trimmed so only the crack remains), body (midrange, identifies what the thing is), sub (felt weight), tail (decay or reverb placing it in space). Let one layer own the sub and roll off the lows on the others; align all layers to the same transient, since small timing shifts between transient and body change perceived size and punch dramatically; a thin hit usually lacks a layer rather than needing another plugin. Layer counts vary: three (transient, body, sub) up to four or five (adding detail or mechanical layers) (snippets). [Violet Recording, impacts](https://violetrecording.com/how-to-make-impact-sounds/); [Morphic, layering](https://morphic.com/resources/how-to/how-to-layer-sound-effects); [IRPR, layering](https://sounddesign.irpr.agency/glossary/layering/)
- Weight: leave space and quiet before the impact so it has contrast to land against; preserve headroom; tune layers to picture. [IRPR, add weight to impacts](https://sounddesign.irpr.agency/guides/how-to-add-weight-to-impacts/)
- Layer complementary spectra: higher textures over low drones, metal clanks over sub-heavy explosions; remove any layer that adds no value. [Pitchdrift](https://pitchdrift-productions.com/sound-design-tips-for-motion-graphics/)

Sub drops and booms (808 style)
- Sine oscillator around 50 Hz with phase reset on each trigger so it does not click; add a very short noise burst or a second pitch envelope with zero decay for the click (snippet). [Ableton forum](https://forum.ableton.com/viewtopic.php?p=903916)
- Pitch envelope depth and time: start 1 to 2 semitones high and land within 10 to 30 ms, or 2 to 4 semitones over 20 to 50 ms; zero attack and a long amp decay of roughly 2 to 4 s for the tail (snippet). [Audeobox, 808s](https://www.audeobox.com/learn/fl-studio/how-to-make-808s-in-fl-studio/)
- Trap kick transient pitch envelope of 20 to 25 semitones (snippet). [SoundBridge, trap kicks](https://soundbridge.io/making-trap-kicks)
- A drop that is too deep or too slow becomes an audible "pew" instead of a thump; a clean sine disappears on small speakers, so add saturation so harmonics carry the pitch (snippets). [Violet Recording, 808](https://violetrecording.com/how-to-design-an-808/)
- Attack Magazine 808 boom (Waves Element): sine at 32' footage, test note C2; amp attack fastest, sustain zero, decay fully open, release about half; pitch envelope to osc pitch at about half depth "to avoid zaps", envelope sustain raised to about 10; longer pitch envelope decay gives a longer boom, shorter gives a kick; then distortion (Output Thermal), mono utility, compressor, and EQ shelving off below about 60 Hz. [Attack Magazine, 808 style booms](https://www.attackmagazine.com/technique/synth-secrets/808-style-booms/)

Braams
- Low brass (for example Century Brass ensemble) layered with a low synth with movement and a sub bass, through a guitar amp sim with distortion and saturation; traditional braams were probably pitched down an octave; ChowTape or Klanghelm SDRR suggested for saturation. Synth route: wavetable modulated by an envelope shaped like a braam ADSR, pitched down, then distortion and reverb; automate tuning of each layer separately for extreme results (snippets). [VI-Control, making braams](https://vi-control.net/community/threads/making-braams.121447/)
- Full chain: forceful low brass plus synthesized tones plus sub, then distortion, compression, filtering and reverb (snippet). [IRPR, Braam](https://sounddesign.irpr.agency/glossary/braam/)

UI clicks, hovers, confirms, cancels (code-synthesised, with exact parameters)
- Envelope: linear attack 2 ms by default ("must not be zero" to avoid a click), exponential release, then a 3 ms fade to exactly zero; exponential pitch glides via `np.geomspace`; soft square = sine plus 3rd harmonic at 1/3 and 5th at 1/5, nothing higher; subtract the mean (DC removal); peak-normalise every file to -3 dBFS; keep harmonics below about 8 kHz. [yetiancai, Synthesizing game UI sound effects with code](https://yetiancai.itch.io/cozy-ui-sfx-190/devlog/1730801/synthesizing-game-ui-sound-effects-with-code)
- Click: noise layer (uniform noise, one-pole low-pass at 4000 Hz, 12 ms, 0.5 ms attack, 4 ms release, gain 0.6) plus body layer (sine gliding 1800 to 1200 Hz, 40 ms, 10 ms release, gain 0.5). Hover: sine 1400 to 1500 Hz, 50 ms, 15 ms release. [yetiancai](https://yetiancai.itch.io/cozy-ui-sfx-190/devlog/1730801/synthesizing-game-ui-sound-effects-with-code)
- Confirm: soft square 660 Hz for 70 ms (30 ms release) then 990 Hz (up a perfect fifth) for 160 ms (60 ms release). Cancel: 520 Hz for 70 ms then 350 gliding to 330 Hz for 160 ms (down, drooping). Same timbre for both so the interface "answers two ways". Text blips: 880 Hz base shifted 0, 2, 4 semitones, each gliding up 2%, 45 ms, 15 ms release, kept under 50 ms so fast text does not smear. [yetiancai](https://yetiancai.itch.io/cozy-ui-sfx-190/devlog/1730801/synthesizing-game-ui-sound-effects-with-code)
- Taps, swishes and page turns as band-passed noise, so they have no pitch to clash. [heyheythere, pentatonic UI sounds](https://heyheythere.itch.io/soft-ui-sfx/devlog/1685319/ui-sounds-that-dont-clash-pitch-them-all-from-one-pentatonic-scale)
- EQ heuristics for taps: ease harsh content around 3 to 6 kHz, cut below 200 Hz; frequency bands for UI roles: 200 to 500 Hz confirmations, 1 to 5 kHz informational, 8 kHz plus high priority alerts (snippets, vendor guidance). [SFX Engine](https://sfxengine.com/blog/best-practices-for-game-ui-sounds); [Envato Elements, UI sound design](https://elements.envato.com/learn/ui-sound-design-ai)

Modal synthesis (foley-like struck objects)
- Modal synthesis is a sum of sinusoids each oscillating independently; measured everyday objects (metal vase, bowl) have several hundred modes, of which only a small fraction is perceptually relevant. [van den Doel](https://www.cs.ubc.ca/~kevinlb/LCI/01/vandendoel-020809.html); [Perceptual Evaluation of Modal Synthesis for Impact-Based Sounds, SMC 2019](https://www.smc2019.uma.es/articles/P1/P1_05_SMC2019_paper.pdf)
- The SMC 2019 study evaluated modal synthesis of ceramic, glass, metal and wood impacts. [SMC 2019 paper](https://www.smc2019.uma.es/articles/P1/P1_05_SMC2019_paper.pdf)
- Farnell's Designing Sound builds every effect from first principles in Pure Data, with chapters on oscillation of bars, rods, cones, membranes and laminas (table of contents snippet). [Designing Sound, Farnell, via SMC paper and listings](https://www.smc2019.uma.es/articles/P1/P1_05_SMC2019_paper.pdf)

Spatial and mix processing
- Keep most SFX mono in busy projects so there is room to pan elements across the stereo field and move them with the action (for example sparks shifting with camera perspective). [Krotos, motion graphics tips](https://krotos.studio/blog/sound-effects-motion-graphics-tips)
- Use EQ, compression, reverb plus flanger, chorus, distortion and delay; use reverb creatively (automated reverb, inverted samples, spectral resonance). [Pitchdrift](https://pitchdrift-productions.com/sound-design-tips-for-motion-graphics/)

### Inferences
These are numpy recipes assembled from the cited numbers above plus standard DSP. SR = 48000. Every sound ends with a 3 ms fade to zero, DC removal and peak normalisation (from yetiancai). Parameters that are the researcher's choice, not sourced, are marked (choice).

- Shared helpers: `env_ar(n, attack_ms, release_ms)` linear attack then `exp(-t/tau)` release; exponential glide `f = np.geomspace(f0, f1, n)` and phase `2*pi*np.cumsum(f)/SR` (never `sin(2*pi*f*t)` with a time-varying f, which mis-sweeps); time-varying filter by processing in 256 to 512 sample blocks with a biquad or a state-variable filter whose cutoff updates per block (choice), or one-pole low-pass `y[n] = y[n-1] + a*(x[n]-y[n-1])`, `a = 1 - exp(-2*pi*fc/SR)`.
- Whoosh (0.25 to 1.0 s): pink noise (white noise filtered with a -3 dB/octave filter, or the Voss or Kellet method) through a band-pass or state-variable low-pass whose cutoff follows a rise-then-fall curve peaking at 55 to 65% of the duration (choice), for example 300 Hz up to 4 to 8 kHz then back to 600 Hz for a light object, 150 Hz to 1.5 kHz for a heavy one (choice, consistent with "heavy = low-passed and slow"). Amplitude envelope: same peak position, raised-cosine or `t**2` rise and exponential fall. Doppler: multiply a tonal or comb layer by a pitch ratio going from about +1 to 2 semitones to -1 to 2 semitones through the peak (choice). Pan: equal-power pan `L = cos(theta)`, `R = sin(theta)` with theta sweeping 0 to pi/2 along the motion direction. Optional layers: low rumble (noise low-passed at 150 to 200 Hz, -10 dB) for heavy, a resonant band-pass at a fixed note (Q 5 to 10) for a "tonal whoosh" (choice). Short reverb: 0.3 to 0.8 s decaying-noise impulse response convolution, 10 to 20% wet (choice).
- Swish (UI, 80 to 250 ms): same as whoosh with a band-pass centre glide 1 to 6 kHz, Q about 1, peak early (30 to 40%) (choice).
- Noise riser (1 to 4 s): white or pink noise, high-pass at 100 to 150 Hz (sourced intent: keep energy out of below 100 Hz), band-pass or low-pass cutoff opening on an exponential curve, for example 200 Hz to 10 kHz, amplitude rising as `t**2` to `t**3`, stereo width increasing (decorrelate L and R noise, mix mid/side with side gain growing 0 to 1). Tonal layer: detuned saws (7 to 8 voices, plus or minus 10 to 25 cents, from the 8 unison voice Serum example) with pitch rising 12 semitones exponentially, noise at -6 dB relative to the tonal layer (Unison snippet). Shepard option: 4 to 6 sine or saw octave layers gliding up one octave per cycle, each weighted by a Gaussian over log frequency. End: hard cut at the hit frame, or reverse-tail ending exactly on the hit.
- Reverse swell (0.5 to 2 s): synthesize a hit (tonal hit or noise burst), convolve with a 2 to 4 s exponentially decaying noise reverb, keep 100% wet, reverse the array, trim so the peak lands one frame before the target frame, then follow with the dry hit (choice). This reproduces the "reversed reverb tail" source.
- Downlifter (0.5 to 2 s): mirror of the riser: cutoff falling 8 kHz to 200 Hz, pitch falling an octave, amplitude exponential decay.
- Impact (0.5 to 2.5 s): four layers aligned on sample 0. Transient: 3 to 10 ms white noise burst high-passed at 2 kHz, attack 0.5 ms. Body: band-passed noise or modal partials in 150 Hz to 2 kHz, 80 to 300 ms decay, matched to the object's material (see section 3). Sub: sine at 40 to 60 Hz with a downward pitch envelope from 2 to 4 semitones above (or up to 20 to 25 semitones for a punchier kick-like attack) settling in 20 to 50 ms, amp decay 0.3 to 2 s; soft saturation `np.tanh(drive*x)/np.tanh(drive)` with drive 2 to 4 so small speakers hear harmonics. Tail: reverb convolution 1 to 3 s, high-passed at 200 Hz so it does not smear the sub. Silence or a level dip 100 to 300 ms before the hit (IRPR contrast rule; duration is a choice). High-pass every non-sub layer at 100 to 120 Hz (sourced rule: one layer owns the sub; cutoff value is a choice).
- Sub drop and boom (1 to 4 s): sine starting at 80 to 110 Hz gliding exponentially down to 30 to 45 Hz over 0.5 to 2 s (choice), amp decay 2 to 4 s (Audeobox snippet), phase starting at 0, a 2 to 5 ms noise click on top, tanh saturation, mono. A slow, deep drop reads as a "pew" in kick context (Violet) but is exactly the cinematic sub drop gesture; use a short fast envelope (10 to 50 ms) for a punch, a long one (0.5 s plus) for the drop.
- Braam (1.5 to 4 s): 3 to 6 sawtooth voices at a low note (for example A1 55 Hz or the music's root an octave below), detuned plus or minus 5 to 15 cents, plus an octave-down sub sine; a low-pass whose cutoff jumps from about 300 Hz to 2 to 3 kHz in the first 50 to 150 ms and closes over the decay (brass "blat"); heavy saturation (tanh drive 4 to 10 or a hard clipper), slow attack 30 to 80 ms, long reverb (choice for every number; recipe is sourced only qualitatively).
- Tonal hit and sting: a chord in the music key (root, fifth, octave, plus maybe major third or ninth) of bell or mallet tones (FM: carrier f, modulator at 1.4 to 3.5 times f for bell inharmonicity, modulation index decaying from 3 to 8 to near 0 over the note), plus a low sine at the root, plus the impact transient, plus a long reverb (choice).
- UI click: use the yetiancai recipe verbatim (noise low-passed at 4 kHz, 12 ms, plus sine 1800 to 1200 Hz, 40 ms). Pop: sine gliding upward fast (for example 400 to 900 Hz in 15 to 30 ms, decay 40 to 80 ms) which reads as a bubble or cork pop (choice). Tick: 2 to 5 ms band-passed noise at 3 to 6 kHz, or a single 1 ms impulse through a resonant band-pass (choice).
- Confirm, success, check: the 660 then 990 Hz soft-square motif (perfect fifth up), or C5, E5, A5 from the pentatonic set. Error: falling pair (520 then 350 to 330 Hz) or a note plus the note times 2 ** (1/12).
- Glitch (50 to 400 ms, unsourced): sample-and-hold or bit-crushed noise (`np.round(x*2**bits)/2**bits` with bits 3 to 6, sample-rate reduction by holding every Nth sample, N 4 to 20), stutter by repeating 10 to 40 ms slices 2 to 8 times, random hard-panned slices, short sine bursts at random high pitches (2 to 8 kHz) (choice).
- Data and digital chatter (unsourced): trains of 10 to 30 ms sine or square blips at random notes of the music scale, 10 to 30 per second, low level, high-passed at 1 kHz (choice).
- Shimmer (unsourced): sum of 6 to 20 high sine partials (2 to 10 kHz) at random scale notes with random slow amplitude LFOs (0.5 to 6 Hz) and staggered onsets, or granular: 20 to 80 ms Hann-windowed grains of a bell tone, pitch shifted plus 12 and plus 24 semitones, randomised start times, through a long reverb; this imitates the "shimmer reverb" pitch-shifted-octave-feedback idea (choice).
- Bed and texture (unsourced): low-passed pink noise (cutoff 400 to 1500 Hz) plus a soft pad (detuned saws low-passed) in key, very slow amplitude LFOs, sitting well under the music.

### Gaps
- No fetched source gave concrete Hz ranges for whoosh filter sweeps, reverb times, or compression settings; those values in Inferences are the researcher's choices.
- No sourced recipe for glitch, shimmer, data chatter, bed, logo sting construction, or foley (paper, cloth, plastic, glass) synthesis was found in this session.
- Farnell's Designing Sound chapter recipes (glass, metal, wood) could not be fetched; the specific mode frequencies and damping tables from the book remain unverified.
- The ui-sounds GitHub repo (github.com/buburdin/ui-sounds), which likely contains synthesis code, was not read.

## 3. How does a sound match the material and size of the object, and how is pitch chosen relative to the music key?

### Takeaway
Size maps to pitch and speed (bigger objects get lower, slower, longer sounds), and material maps to the spectrum and decay of the body layer (modal partials and damping). For pitch, the most concrete practitioner method is to tune all tonal SFX to one scale shared with the music, usually a pentatonic, using rising intervals for positive events and falling or dissonant ones for negative events, and leaving taps and swishes as unpitched band-passed noise.

### Cited Findings
- Bigger objects get lower, slower whoosh sounds (snippet). [Krotos, Whoosh tutorial](https://sound.krotosaudio.com/whoosh-sound-effects/)
- Light airy whooshes for text, menus and delicate graphics; dark, distorted, low-passed whooshes for heavy objects. Fast sweep sharp and quick, slow sweep heavy and grand. [Violet Recording, whooshes](https://violetrecording.com/how-to-make-whoosh-sounds/)
- Material brightness, "from wood to glass, from nylon to steel", is a primary control in modal resonator interfaces; modal synthesis was perceptually evaluated for ceramic, glass, metal and wood. [SMC 2019 paper](https://www.smc2019.uma.es/articles/P1/P1_05_SMC2019_paper.pdf); [ModularGrid, modal synthesizer](https://modulargrid.net/e/modules/view/4606)
- Pitched synths that follow the cube's spins and "rubbery stretches that rise and fall in pitch" with the morph: pitch tracks the visual motion. [Krotos, motion graphics tips](https://krotos.studio/blog/sound-effects-motion-graphics-tips)
- One scale for everything: C major pentatonic (C, D, E, G, A) with F and B removed, so any two UI sounds form a second, third, fourth, fifth, sixth or minor seventh and never a minor second, tritone or major seventh. Confirm = steps (0, 2, 4) played in sequence (C5, E5, A5). Toggle = two steps two apart, rising for on, same pair reversed for off. Cancel = falling pair. Error = a marimba note plus the same note a semitone up (f * 2 ** (1/12)) at once: "the clash is the message". Sci-fi set in A minor pentatonic, fantasy set in D major pentatonic. [heyheythere, pentatonic UI sounds](https://heyheythere.itch.io/soft-ui-sfx/devlog/1685319/ui-sounds-that-dont-clash-pitch-them-all-from-one-pentatonic-scale)
- Confirm up a perfect fifth (660 to 990 Hz), cancel down (520 to 350 Hz) with a droop; "Players read the direction without thinking about it." [yetiancai](https://yetiancai.itch.io/cozy-ui-sfx-190/devlog/1730801/synthesizing-game-ui-sound-effects-with-code)
- A UI sound family can be "one soft celesta family in the song's key" (example from an open-source project issue, snippet). [GitHub issue, UI sound family in the song's key](https://github.com/Eric-Zhang-Developer/piano-arcade-gator-ai-days/issues/1167)
- Braam and music both occupy the bass; at full weight together the mix turns to mud, so carve the music's bass (snippet). [IRPR, Braam](https://sounddesign.irpr.agency/glossary/braam/)

### Inferences
- Size mapping for code (choice, consistent with the sourced direction): scale factor s from 0 (chip, small label) to 1 (hero card, full-screen type). Body fundamental `f = f_small * (f_large/f_small) ** s`, for example 1200 Hz down to 150 Hz; duration `d = d_small * (d_large/d_small) ** s`, for example 60 ms up to 600 ms; sub layer gain 0 for s < 0.4, rising to full at s = 1; reverb send rising with s. Big type gets a lower, longer, wider sound; small type a short, bright, mono tick.
- Material mapping via modal synthesis (standard acoustics, not sourced in this session): sum of exponentially decaying sines `a_k * exp(-t/tau_k) * sin(2*pi*f_k*t)`.
  - Glass: few, sparse, inharmonic partials high in frequency (roughly 1 to 6 kHz), long ring (tau 0.3 to 1.5 s), very bright.
  - Metal: many inharmonic partials (free bar ratios roughly 1, 2.76, 5.40, 8.93), very long decay (1 to 4 s), slight beating from paired detuned modes.
  - Ceramic: like glass but lower and shorter (tau 0.1 to 0.4 s).
  - Wood: low to mid partials (200 to 1200 Hz), heavy damping (tau 20 to 80 ms), higher partials decaying faster than low ones.
  - Plastic: mid partials, short (tau 15 to 50 ms) with a noise click, duller than wood at the top.
  - Paper: no modes, a burst of high-passed noise (2 to 10 kHz) with fast irregular amplitude modulation (crackle), 50 to 300 ms.
  - Cloth: low-passed noise (cutoff 1 to 3 kHz), soft attack 10 to 30 ms, smooth.
  - Heavier mass of the same material: lower f_k, longer tau, larger sub.
- Pitch relative to music: pick the music key, then set every tonal SFX (tonal hits, pops with pitch, confirms, shimmers, data blips) to notes from that key's pentatonic, root and fifth for hits and stings, the root an octave or two below for sub drops and braams, and keep whooshes, ticks and paper or cloth as unpitched noise. Use rising intervals (fifth, octave) for reveal and success, falling intervals for exits, a semitone cluster only for errors.

### Gaps
- No practitioner source in this session stated how motion graphics designers specifically tune whooshes or impacts to the music key (beyond the UI pentatonic method and the qualitative "pitched synths follow the motion").
- No sourced mode-frequency or damping tables for glass, plastic, paper or cloth were retrieved.

## 4. What is sweetening and how do designers make a sound feel expensive rather than cheap?

### Takeaway
No retrieved source defined "sweetening" for motion graphics directly. The sourced practices that separate polished from cheap are: layering complementary spectra with carved frequencies, aligning transients exactly, contrast (silence before a hit), restraint (fewer sounds, not on every beat), consistent tone across a set, saturation so lows survive small speakers, correct loudness, and checking on several playback devices.

### Cited Findings
- Sound effect definition: "an artificially created or enhanced sound, or sound process used to emphasize artistic or other content" (snippet; "enhanced" is the sweetening sense). [Wikipedia, Sound effect](https://en.wikipedia.org/wiki/Sound_effect)
- Layer complementary spectra (high textures on low drones, metal clanks on sub explosions) and remove any layer that adds nothing; test on headphones, phones, small Bluetooth speakers and car speakers. [Pitchdrift](https://pitchdrift-productions.com/sound-design-tips-for-motion-graphics/)
- Leave space and quiet before the impact for contrast; preserve headroom; listen in context; compare against a reference; when in doubt apply a lighter touch. [IRPR, add weight to impacts](https://sounddesign.irpr.agency/guides/how-to-add-weight-to-impacts/)
- Small timing shifts between transient and body layers dramatically change perceived size and punch; muddiness usually comes from overlapping low end (snippets). [Violet Recording, impacts](https://violetrecording.com/how-to-make-impact-sounds/); [Morphic, layering](https://morphic.com/resources/how-to/how-to-layer-sound-effects)
- A clean sine sub disappears on small speakers; saturation lets harmonics carry it (snippet). [Violet Recording, 808](https://violetrecording.com/how-to-design-an-808/)
- Constant motion sound tires the ear and flattens dynamics (snippet). [Soundgrail](https://soundgrail.com/blog/shape-movement-and-flow-in-modern-sound-design)
- Keep a consistent tone across a UI sound set (for example "soft, warm wooden clicks", "crisp digital blips"); keep UI sounds brief and quiet. [Voidless.dev](https://voidless.dev/tutorials/sound-effects/generate-ui-sound-effects)
- Keep harmonics below about 8 kHz and peak-normalise to -3 dBFS; never use zero attack (clicks). [yetiancai](https://yetiancai.itch.io/cozy-ui-sfx-190/devlog/1730801/synthesizing-game-ui-sound-effects-with-code)
- Wes Slover (Sono Sanctus) prefers clients to describe the feeling or energy wanted rather than prescribe a technique like "fast drums" (snippet). [Dash Bash, Sanctus Audio interview](https://www.dashbash.net/blog/sanctus-audio)

Levels relative to music (rules of thumb, sources conflict)
- Music about -20 dB; footsteps and environmental SFX about -20 dB; hits and cracks between -20 and -10 dB, real peaks can go louder; music around -14 LUFS when mastered, TV about -23 LUFS, film about -27 LUFS, Sundance 2023 film spec -24 LUFS integrated. [Krotos, Balance music and SFX](https://krotos.studio/blog/how-to-balance-music-and-sound-effects)
- Music under dialogue about -18 to -25 dB, closer to -10 dB when no speech; SFX usually -12 to -18 dB and never louder than dialogue unless the moment is intentional (snippet). [Pixflow, mixing in Premiere](https://pixflow.net/blog/?p=92478)
- YouTube target about -14 LUFS integrated with true peak under -1 dBTP; platforms turn louder uploads down; ducking music 15 to 20 dB below voice (snippet). [IRPR, Mix audio for YouTube](https://sounddesign.irpr.agency/guides/how-to-mix-audio-for-youtube/)
- -16 LUFS cited for most other online platforms; US A/85 broadcast at -24 LKFS (snippets). [OpenClip, loudness standard](https://openclip.app/learn/loudness-standard.md); [Gearspace, broadcast safe audio](https://gearspace.com/threads/broadcast-safe-audio.978550/)

### Inferences
- "Expensive" checklist for a numpy pipeline: (1) every hit has transient, body, sub and tail aligned on the same sample; (2) one layer owns the sub, everything else high-passed; (3) sub layers saturated so they read on phone speakers; (4) a short dip or silence before big hits; (5) tonal elements in the music key; (6) shared reverb (one impulse response for all SFX) so everything sits in one space; (7) no zero attacks, every tail faded to zero; (8) fewer sounds: skip SFX on minor moves, accent only the events that matter; (9) tiny random variation (plus or minus 1 to 2% pitch, plus or minus 1 dB) on repeated UI sounds so repeats do not sound machine-gunned (choice); (10) final mix to about -14 LUFS integrated, true peak under -1 dBTP for web.
- Cheap tells (inferred from the sourced rules): plain white noise with a static fade, unaligned layers, bass from several layers at once, SFX on every beat, out-of-key pitched sounds, hard digital clicks at sound boundaries, harsh 3 to 6 kHz energy and fizz above 8 kHz.
- Starting relative level for code: music bed at a reference 0 dB, UI ticks about -8 to -14 dB below the music peak, whooshes about -6 to -10 dB, hero hits roughly at or 0 to 3 dB above the music peak for one frame window, with the music ducked 3 to 6 dB around hero hits (choice derived from the -20/-10 dB Krotos ranges).

### Gaps
- No source in this session gave a formal definition of "sweetening" in commercial post or a breakdown of a specific SaaS launch film's sound layers.
- No sourced sidechain or ducking attack and release values were found.

## 5. Concrete tutorials and breakdowns with layers, plugins and settings

### Takeaway
The only retrieved sources with full numeric settings are the two Python UI-sound devlogs (yetiancai and heyheythere) and the Attack Magazine 808 boom; everything else gives structure without numbers. These are the most directly portable to numpy.

### Cited Findings
- yetiancai devlog: complete Python/numpy UI recipes (click, hover, confirm, cancel, text blips) with frequencies, durations, release times, gains, envelope rules and normalisation, as listed in section 2. [yetiancai](https://yetiancai.itch.io/cozy-ui-sfx-190/devlog/1730801/synthesizing-game-ui-sound-effects-with-code)
- heyheythere devlog: Python-synthesised pack of 173 sounds in 14 categories, all pitched from one pentatonic scale with `pn(i, octave)` step function, error as semitone dissonance. [heyheythere](https://heyheythere.itch.io/soft-ui-sfx/devlog/1685319/ui-sounds-that-dont-clash-pitch-them-all-from-one-pentatonic-scale)
- Attack Magazine 808 boom: Waves Element sine, envelope and mod matrix settings, Output Thermal distortion, Presswerk compressor, EQ shelf below about 60 Hz. [Attack Magazine](https://www.attackmagazine.com/technique/synth-secrets/808-style-booms/)
- Braam chains: 8Dio Century Brass plus low synth plus sub into a guitar amp sim; ChowTape or Klanghelm SDRR for saturation. [VI-Control, making braams](https://vi-control.net/community/threads/making-braams.121447/)
- Whoosh tools: Krotos Studio and UVI Whoosh FX (Doppler modulation, layer engines) are product-specific tutorials. [Krotos Studio whoosh presets](https://krotos.studio/blog/whoosh-sound-effects-krotos-studio); [UVI Whoosh Designer tips](https://support.uvi.net/hc/en-us/articles/360001692797-Whoosh-Designer-Tips)
- Krotos motion graphics breakdowns (Rubik's cube, Mirror Mirror, Luminous Bloom with Dehumaniser 2 for creature layers and mono SFX for panning). [Krotos, motion graphics tips](https://krotos.studio/blog/sound-effects-motion-graphics-tips)
- Sono Sanctus discussion of client process (podcast, no transcript retrieved). [School of Motion, Sono Sanctus podcast](https://schoolofmotion.com/blog/sono-sanctus-podcast-podcast); [Animalators Ep. 50, Wesley Slover](https://podtail.com/en/podcast/animalators/episode-50-wesley-slover/)

### Inferences
- For the code implementation, the yetiancai envelope and normalisation rules should be the shared base for every generated sound, and the heyheythere scale approach should be generalised from UI sounds to all tonal motion graphics SFX by setting the scale root to the soundtrack key.

### Gaps
- YouTube breakdown transcripts, School of Motion articles, GDC Vault UI audio talks, Ric Viers' Sound Effects Bible and Farnell's book recipes were not retrievable in this session; their numeric content is unverified here.
