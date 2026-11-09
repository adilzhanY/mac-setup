# AI, code-synthesized, MIDI and stock tells in music and sound effects, and what makes them sound human and expensive

Scope note: sources are 2018 to 2026. Most practical numbers come from producer guides and forums (modwheel.net, VI-Control, Gearspace) and are practitioner rules of thumb, not measurements. The academic sources (arXiv, ISMIR, Frontiers, PMC) are flagged as such. Several arXiv IDs (2604 to 2610) are from 2026 and were read only through abstracts, HTML pages or search snippets.

## Q1. How listeners, producers and critics describe the sound of Suno/Udio, MIDI mockups, stock corporate music and oscillator-made sound, and what gives each away

### Takeaway
Each family has its own fingerprint. Suno/Udio: a metallic, glassy, "watery" high end, robotic or mispronounced vocals, generic lyrics, "too perfect" polish and a default song shape. MIDI mockups: identical repeated samples ("machine gun"), flat dynamics, straight fader-ramp phrasing, wrong balance and everything at one depth. Stock corporate: competent but engineered to be inoffensive, with a narrow palette (ukulele, glockenspiel, whistling, claps) that signals "brand with nothing to say".

### Cited Findings
**Suno / Udio (generative AI music)**
- Guides describe a metallic, glassy sheen on cymbals and sibilants and a watery swirl on sustained notes, placed roughly in the 5 to 12 kHz region, plus a harsh grainy texture above 8 to 12 kHz. Several of these sources sell a fix or a detector, so treat the claims with caution. [Intrect: how to fix AI music artifacts](https://intrect.io/blog/how-to-fix-ai-music-artifacts/); [fwdmusic detection guide](https://fwdmusic.com/en/news/how-to-detect-ai-generated-music)
- Intrect's artifact list: metallic shimmer on cymbals, hats and vocal sibilance (high-frequency quantization residual of the neural codec); watery swirl on pads, strings and held vocals (phase inconsistency in codec reconstruction); grainy, harsh air band and room tails above about 8 kHz (codec bandwidth limits); thin, hollow mids on lead vocal and snare body; smeared transients and pre-echo (blamed on MP3 export, not on generation). Things that do NOT fix it: a high shelf cut (dulls the music), multiband compression, re-encoding, adding reverb or saturation (they only mask it). [Intrect: Suno artifacts](https://intrect.io/blog/suno-artifacts/)
- The shimmer is attributed to the residual vector quantization (RVQ) neural codec the generator decodes through; vocals "smear on long notes". [Intrect](https://intrect.io/blog/how-to-fix-ai-music-artifacts/)
- Detector vendor claim: Suno shows 32 kHz sampling artifacts and high-frequency "digital haze", Udio shows periodic transformer patterns and is harder to detect. Vendor claim, not independent research. [Authio](https://authio.io/blog/suno-vs-udio-detection)
- r/SunoAI users (2026) describe "too much treble, too much sibilance"; one audio student claims AI mixes lack the roughly 3 kHz presence lift human engineers usually add (one person's theory); commenters cite a 16 kHz MP3-style cutoff from training data; one user says newer models made the artifacts much harder to hear than before. Anecdotal. [Reddit snapshot](https://reddit.sentinel-team.org/posts/1rmom4q/snapshots/2026-03-08T21%3A34%3A58.198118Z); [r/SunoAI "can you tell"](https://cal1.lr.ggtyler.dev/r/SunoAI/comments/1ihtylx/can_you_tell/mb1s7l0/?context=3)
- Users have reported Suno generating sobbing, crying or other eerie vocal sounds, especially near endings. [ITC.ua](https://itc.ua/en/news/a-ghost-in-armor-sunoai-ai-music-generator-suddenly-cries-users-notice-other-eerie-sounds); [Techprincess](https://techprincess.it/glitch-suno-ai-singhiozzo-urla-tracce/amp/)
- Suno output shares a recognizable fingerprint: predictable chord progressions, stock lyrics, "polished but hollow" production; with no structural guidance it falls back on a default arrangement. [James Palm, Medium](https://james-palm.medium.com/10-suno-ai-mistakes-that-make-your-songs-sound-like-everyone-elses-b4c8a2784e33)
- A writer testing Suno for a podcast theme found it did not use standard 8 or 16 bar verse forms; the first verse came out an awkward 12 bars. [We Will Not Be Flattened, Substack](https://wewillnotbeflattened.substack.com/p/i-asked-generative-ai-music-platform-suno-to-write-a-podcast-theme-things-got-weird-a66820103f55)
- Listener free-text in a 308-person blind test: the most frequent tags were Vocals (369), Lyrics (247), Negative (231), Artificial (224), Generic (174), Robotic (112). Quotes: "The singer's voice in track 2 sounds more robotic"; "Track 2 immediately seemed more human cause it made better use of stereo sound"; "Something about Track 1 sounded too perfect, too contrived to be Human." [Echoes of Humanity, arXiv 2509.25601](https://arxiv.org/html/2509.25601)
- SONICS benchmark paper notes Suno vocals often sound synthetic or mechanical, while Udio occasionally produces a "karaoke effect" (vocal sitting on top of the backing rather than inside it). Reported via search summary; the full PDF was too large to fetch. [SONICS, arXiv 2408.14080](https://arxiv.org/pdf/2408.14080)
- MuseBench catalogs AI-music artifacts as: spectral (periodic line patterns from deconvolution layers), harmonic (stylistically implausible or abrupt chord transitions), performance-constraint (physically impossible events: piano with more than 10 simultaneous notes, guitar beyond the fretboard, wind lines with no breaths), and vocal/lyrical ("pseudo-lyrics" that fit the rhythm but mean nothing, and "approximate pronunciation"). [MuseBench, arXiv 2610.20310](https://arxiv.org/html/2610.20310)

**MIDI mockup**
- The "machine gun" effect is the audible repetition when a sampler plays the identical recording on every trigger. [SampleStack](https://samplestack.app/news/round-robin-explained/); [KVR](https://www.kvraudio.com/forum/viewtopic.php?t=274098)
- Mockup giveaways named by composers: the left hand in the middle register overpowering the melody (a pianist would not), unnatural piano decay (a sample fault, not a programming fault), strings that are not "warm and resonant", a piano placed so far back it sounds like it is "in the very back right corner of the room". [Taxi forum](https://forums.taxi.com/post329827.html); [Taxi forum](https://forums.taxi.com/post329840.html); [MusicStrive](https://musicstrive.com/midi-programming-mistakes/)
- A global random humanize pass, identical variance on a quiet chord and a busy passage, one unbroken sustain with no re-bow dips, and dynamics drawn as a straight fader ramp all read as fake. [Composer Workflow](https://agents.composerworkflow.com/academy/humanizing-a-mockup/)
- One reverb on every track puts everything at one distance so the result sounds flat; a quieter horn that is still as dry and present as the flute reads as a soft instrument at the front, not a distant one. [modwheel.net reverb guide](https://modwheel.net/guides/reverb-for-cinematic-mixing); [modwheel.net mixing basics](https://modwheel.net/guides/basics-of-mixing-cinematic-music)

**Stock corporate / royalty-free**
- Subscription libraries reward quantity over distinctiveness, producing tracks "engineered to be inoffensive, broadly applicable, and emotionally generic. They are designed to fit everything, which means they say nothing." [Artyfile](https://artyfile.com/blog/why-your-commercial-sounds-like-everyone-elses)
- "Corporate ukulele" is the default for organisations that want to seem friendly without being distinctive: "a generic cheery wave of a sound". [The Metropolitan, Tobias Sturt](https://www.themetropolitan.uk/p/corporate-ukulele)
- The strummy, twee, glockenspiel and whistling style is traced anecdotally to the Juno soundtrack and GarageBand-era home production, then copied into commercials and stock sites. [MetaFilter](https://ask.metafilter.com/295598/Strummm-ba-dumm-ba-dum-ba-diiink-dink-dink-dink-diiiink); [Gearspace: Nobody whistles](https://gearspace.com/board/music-for-picture/911668-nobody-whistles-why-do-advertisers-sell.html); [ResetEra](https://www.resetera.com/threads/those-shitty-minute-long-vids-with-the-generic-ukelele-music.6826/)

**Oscillator / synth-made sound**
- Synth brass fails without the initial burst of air: a simple filter with an AR envelope is not enough; it needs an ADSR contour, velocity sensitivity and a transient whose harmonic mix changes (tonguing). [Sound On Sound: Synthesizing Brass](https://www.soundonsound.com/techniques/synthesizing-brass-instruments)
- String-machine ensemble modulation "sounds unnaturally regular" because of a constant triangle LFO; adding instability (random modulation) makes it more human; too much detune gives an "off-colour" timbre. [Sound On Sound: String Machines](https://www.soundonsound.com/techniques/synthesizing-strings-string-machines)
- Virtual analog synths imitate analog warmth by adding small pitch and amplitude modulation plus a little noise; analog tuning drifts as circuits warm or cool. [Vintage Synth Explorer forum](https://forum.vintagesynth.com/viewtopic.php?t=54750)
- Much of perceived analog "warmth" is attributed to harmonic distortion rather than drift alone, and experienced producers struggle to tell good digital emulation from analog blind. No peer-reviewed study either way. [Dreyandersson](https://dreyandersson.com/blog/analog-vs-digital-synthesizers/)
- Sample-library vibrato made by pitching samples back and forth also shifts formants and can sound unnatural. [Search summary of Sound On Sound and library material](https://www.soundonsound.com/techniques/synthesizing-brass-instruments)

### Inferences
- Common thread across all four families: the ear flags sameness. Same waveform per note (MIDI), same depth per instrument (dry mix), same palette per brief (stock), same fizz on every high-frequency event (AI codec), same LFO cycle (synth). Realism is variation that has a cause (a bow running out, a breath, a room, a phrase goal), not random variation.
- For code-synthesized music (WebAudio, Remotion, raw oscillators), the oscillator family tells (static spectrum, perfectly stable pitch, identical envelopes, no noise component, no room) apply directly, and the AI codec tells do not. Fixes therefore come from the synth and mockup toolkit: per-note variation, noise layers, slow drift, envelope differences by velocity, and a shared room.
- "Too perfect, too contrived" (Echoes of Humanity quote) suggests that over-polish is itself a tell, matching the "polished but hollow" description of Suno.

### Gaps
- No primary journalism quotes (Verge, Wired, Rolling Stone US) on the specific sound of Suno/Udio were retrieved; the Rolling Stone Australia piece found was about ethics, not timbre.
- No source found that specifically describes chiptune or raw-oscillator music as a "tell" in ads; the oscillator section is built from synthesis tutorials.
- No published measurement of analog oscillator drift in cents was found.

## Q2. Instrument realism: why raw synthesis sounds artificial, how sample libraries get realism, and the minimum a convincing mockup needs

### Takeaway
Realism comes from variation per note that follows physics: different recordings for repeated notes (round robins, 6 to 8 for fast shorts), different timbre per dynamic (velocity layers that change tone, not just level), continuous dynamics on sustains (CC1 plus CC11), a real attack transient and release tail, natural vibrato (about 5 to 7 Hz, about 30 to 60 cents wide, varying), and physically playable parts.

### Cited Findings
- Velocity layers give dynamic range; round robins add variation within each layer. They solve different problems and are combined. [SampleStack](https://samplestack.app/news/round-robin-explained/)
- Staccatos "desperately need" round robins; sustains do not. For piano, forum users say dynamic layers matter more than round robins. [VI-Control](https://vi-control.net/community/threads/are-round-robins-a-real-advantage-in-a-multi-velocity-layers-piano-library.64111/)
- 4 to 6 round robins is practical for drums and plucks; beyond 6 to 8 the improvement is rarely noticeable; random selection can repeat the same sample twice in a row. [SampleStack](https://samplestack.app/news/round-robin-explained/)
- At 150 bpm semiquavers (10 notes per second), 4 round robins cycle back every 0.4 s, inside the window where the ear notices repetition; 6 to 8 pushes the return past 1 s. Resetting the round-robin cycle on every note, or at each loop point, recreates the machine gun. [modwheel.net: Why your ostinatos sound like a machine gun](https://modwheel.net/guides/why-your-ostinatos-sound-like-a-machine-gun)
- Fix for too few round robins: alternate bars between two libraries on separate tracks, the second about 1.5 dB lower, through a shared reverb with each library's built-in room reduced. [modwheel.net](https://modwheel.net/guides/why-your-ostinatos-sound-like-a-machine-gun)
- Test whether velocity changes tone or only loudness: play velocity 40 and 110. If only loudness changes, velocity does not multiply round robins. [modwheel.net](https://modwheel.net/guides/why-your-ostinatos-sound-like-a-machine-gun)
- Most orchestral libraries map dynamic layers (timbre crossfade) to CC1; one workflow uses CC1 alone and CC11 (expression volume) only in a second pass; another guide calls relying on CC1 alone a "fundamental mistake" and rides both. Practice differs. [Search summary of masterthescore / production-expert](https://www.masterthescore.com/article/orchestral-mockups); [Production Expert](https://www.production-expert.com/production-expert-1/how-to-improve-realism-in-orchestral-mock-ups)
- On short-note patches velocity selects the dynamic layer; guides recommend hand-sequencing velocities and accenting downbeats on fast spiccato rather than a uniform value. [modwheel.net mockup guide](https://modwheel.net/guides/ultimate-guide-to-orchestral-mockups)
- Recorded notes are trimmed to just before the beat because part of a note's performance happens a fraction of a second before it; grid-aligned notes may need to sit early. [VI-Control](https://vi-control.net/community/threads/what-is-your-best-tips-to-humanize-the-tracks.140809/)
- Bow-change dips of roughly 1 to 3 dB placed where a bow would run out; under about 1 dB is unnoticeable; too many sounds like "constantly catching its breath". Dynamics should pull back at dissonance and push into resolutions rather than ramp straight. [Composer Workflow](https://agents.composerworkflow.com/academy/humanizing-a-mockup/)
- Physically impossible parts are a measurable AI tell: more than 10 simultaneous piano notes, guitar beyond the fretboard, wind lines without breaths. [MuseBench](https://arxiv.org/html/2610.20310)
- Vibrato: empirical rates 4 to 10 Hz with means 5 to 7 Hz; student mean about 5.5 Hz; four top violin soloists (Bell, Midori, Mutter, Perlman) averaged 63 cents wide and 6.63 Hz, wider in the upper register; a classic measurement gives a typical extent of about 30 cents, ranging 10 to 60 cents. [Search summary of violin vibrato literature](https://experts.illinois.edu/en/publications/a-pilot-study-of-relationships-between-pitch-register-and-dynamic/); [Stellenbosch thesis](https://scholar.sun.ac.za/handle/10019.1/1792); [BYU physics](https://physics.byu.edu/docs/publication/1499)
- Individual cellists' tendencies shape vibrato depth beyond easily traceable parameters. [arXiv 2512.18162](https://arxiv.org/pdf/2512.18162)
- Brass realism needs the air-burst transient and velocity-dependent brightness (see Q1). [Sound On Sound](https://www.soundonsound.com/techniques/synthesizing-brass-instruments)
- A great performance on a mediocre piano or flute sample still sounds mediocre: sample quality caps realism. [Taxi forum](https://forums.taxi.com/post329840.html)

### Inferences
- Minimum convincing mockup, distilled from the above: (1) a library or synth patch whose timbre changes with dynamic, (2) at least 6 to 8 alternates on any note repeated faster than about 4 per second, (3) a continuous dynamic curve on every sustained line, shaped to the phrase, (4) vibrato that starts late and varies in depth (not a fixed LFO from note-on), (5) parts a human could play, (6) a shared room.
- For code synthesis the equivalents are: brightness (filter cutoff, harmonic count) tied to velocity; per-note random detune of a few cents and slightly different envelope times; a noise component in the attack (breath, bow, pick); a release tail that keeps ringing after note-off; vibrato delayed by a few hundred ms and with depth that wanders. The specific few-cents and few-hundred-ms values are my inference, not sourced numbers.

### Gaps
- No sourced numbers for legato transition times or library attack latency compensation (commonly discussed values of 50 to 300 ms exist in forums but were not retrieved).
- No sourced data on singer vibrato or intonation deviation in cents.

## Q3. Performance and groove: microtiming and dynamics of real players, how much variation, and why perfect quantization and constant velocity read as machine

### Takeaway
Real players deviate from the grid by roughly 5 to 50 ms, but the deviations are systematic (they repeat bar to bar and serve the phrase), not random. Experts notice swing displacement at 8 to 14 ms and non-drummers at 18 to 31 ms. Several studies found perfectly quantized versions rated as grooving as well or better than large random deviations, so the fix is shaped variation and velocity, not big random jitter.

### Cited Findings
- Microtiming deviations in groove typically range 5 ms to 50 ms (secondary summary of a thesis). [ANU repository](https://openresearch-repository.anu.edu.au/bitstreams/dfcc9a33-70c6-4653-a5e7-1dcc82cb30fe/download)
- In Clyde Stubblefield's "Funky Drummer", deviations shrink from 56 ms to 4 ms across a fill as the drummer returns to the downbeat, and drummers repeat their deviation patterns within a few milliseconds bar to bar. [ZGMTH: Microtiming in Early Funk](https://www.gmth.de/zeitschrift/artikel/1224.aspx)
- Onset displacement needed to detect swing: 8 to 14 ms for expert drummers, 18 to 31 ms for non-drummers. [Search summary of Frontiers/PMC work](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2017.01709/full)
- Frühauf et al. and Davies et al. found large microtemporal deviations got low groove ratings and the perfectly quantized version scored highest; Madison and colleagues found no correlation between deviation size and groove. [Frühauf et al. via ResearchGate](https://www.researchgate.net/publication/237423294_Music_on_the_timing_grid_The_influence_of_microtiming_on_the_perceived_groove_quality_of_a_simple_drum_pattern_performance); [Senn et al. PMC](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5050221/)
- Expert listeners are more sensitive to microtiming manipulation than non-experts, and listeners expect larger deviations in swing than in funk. [Senn et al., PMC5050221](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5050221/)
- Practitioner numbers for sampled shorts: after quantizing, a random offset of 3 to 6 ms; velocity spread across at least 20 points, not centred, drifting up over 4 bars and back down rather than jittering around a mean; note length varied 10 to 20 percent in a shape (shorter through a crescendo, longer as it settles). [modwheel.net](https://modwheel.net/guides/why-your-ostinatos-sound-like-a-machine-gun)
- A free-library guide suggests 10 to 30 ms offsets; a VI-Control user argues randomizing ensemble note positions does not help because recorded ensembles already contain timing spread, and suggests subtle tempo automation instead. Conflicting advice. [Bedroom Producers Blog](https://bedroomproducersblog.com/free-vst-plugins/orchestral/); [VI-Control](https://vi-control.net/community/threads/what-is-your-best-tips-to-humanize-the-tracks.140809/)
- Phrase-level timing: nudge only a few notes per phrase; arrival notes at a peak slightly early, notes approaching a cadence slightly late, mid-phrase notes near the grid. Some parts should stay locked: relentless ostinatos, sequenced arpeggios, trailer percussion. [Composer Workflow](https://agents.composerworkflow.com/academy/humanizing-a-mockup/)
- Exactly even spacing makes the waveform periodic and the ear locks onto periodic repetition; quantizing can make this worse. [modwheel.net](https://modwheel.net/guides/why-your-ostinatos-sound-like-a-machine-gun)

### Inferences
- For short ad music: keep the pulse layer (kick, ostinato) tight, put the variation into velocity contour and into the melodic and harmonic layers (small early/late pushes of 5 to 15 ms on phrase peaks and cadences), and use a repeating per-bar groove template rather than per-note random jitter, since real drummers repeat their deviations.
- 3 to 6 ms random jitter is below the 8 to 14 ms expert threshold for swing detection, so it mostly breaks waveform periodicity (sample identity) rather than creating audible looseness.

### Gaps
- No sourced numbers for typical velocity variance of real pianists or drummers (in MIDI units or dB).

## Q4. Mix and space: reverb, early reflections, stereo, saturation, bus compression; why dry mixes sound fake; what professional ad mixes do

### Takeaway
Dry or uniformly reverbed sources sound fake because depth comes from early reflections, pre-delay and high-frequency roll-off, and a mix with one reverb puts every instrument at one distance. Pros place instruments on close/mid/far sends with early-reflection-only rooms and one shared tail. Broadcast ads are delivered to loudness standards (-24 LKFS US, -23 LUFS EU), which limits how much loudness can be used as a substitute for quality.

### Cited Findings
- Front-to-back depth depends mainly on early reflections and high-frequency roll-off; convolution reverbs are most convincing for orchestra because a real hall's early reflection pattern is hard to fake. [modwheel.net reverb guide](https://modwheel.net/guides/reverb-for-cinematic-mixing); [Andrew Feazelle](https://andrewfeazelle.com/how-to-make-an-orchestral-sample-library-sound-real/)
- Pre-delay as distance cue: about 30 to 40 ms pulls a source forward, 0 to 8 ms pushes it back; another guide gives 20 to 40 ms for close instruments, shrinking as they move back. Starting points only. [modwheel.net](https://modwheel.net/guides/basics-of-mixing-cinematic-music); [Gearspace thread](https://gearspace.com/board/music-for-picture/1081931-searching-best-reverb-approach-orchestral-mock-ups.html)
- Workflow: send architecture with close, mid and far buses rather than per-track inserts; shorten an impulse response to get only early reflections, then add a separate algorithmic tail; one shared tail at the output with about 40 to 80 ms pre-delay; one user runs an ER-only bus about 2 dB above the dry signal for a dry clarinet. [VI-Control: early reflections on dry libraries](https://vi-control.net/community/threads/what-are-your-techniques-for-early-reflections-on-dry-orchestral-libraries.82511/); [VI-Control: mixing dry recorded with virtual](https://vi-control.net/community/threads/mixing-dry-recorded-orchestral-instruments-with-virtual-orchestration.147277/); [Gearspace reverb settings](https://gearspace.com/board/music-computers/565702-reverb-settings-orchestral-sample-libraries-share-your-set-ups.html)
- When combining libraries, reduce each library's built-in room and use one shared reverb, or the swap is audible. [modwheel.net](https://modwheel.net/guides/why-your-ostinatos-sound-like-a-machine-gun)
- Listeners in a blind AI test cited better use of stereo as a reason a track seemed human. [Echoes of Humanity](https://arxiv.org/html/2509.25601)
- Broadcast loudness: ATSC A/85 (basis of US CALM Act) -24 LKFS ±2, max true peak -2 dBTP; EBU R 128 -23 LUFS, max true peak -1 dBTP. LKFS and LUFS are the same measure. EBU R 128 s2 recommends about -23 for streaming, up to -16 where needed. [ITU-R BS.2434](https://www.itu.int/dms_pub/itu-r/opb/rep/R-REP-BS.2434-2018-PDF-E.pdf); [Lund TC 2011](https://clinicarchive.s3.amazonaws.com/2011/Lund-TC-2011.pdf); [Sports Video Group](https://www.sportsvideo.org/2022/06/15/audio-loudness-waters-are-a-little-less-calm-than-before/?print=1); [Adval](https://adval-www.pages.dev/features/sb-576-calm-act-streaming-audio-compliance)
- Spotify normalizes music to about -14 LUFS (only a secondary source found). [Voxbooster](https://voxbooster.com/ja/blog/streaming-audio-loudness-normalization-ebu-r128-statistics-2026/)
- Analog "warmth" is attributed largely to harmonic distortion. [Dreyandersson](https://dreyandersson.com/blog/analog-vs-digital-synthesizers/)
- Strings need to sound "warm and resonant" in production to avoid sounding like MIDI. [Taxi forum](https://forums.taxi.com/post329827.html)

### Inferences
- For a code-synthesized soundtrack, the cheapest large realism gain is a real convolution impulse response (a room or hall) on sends at two or three depths, with darker, later-ER sends for back instruments, plus gentle saturation on the master for harmonic density. A completely dry oscillator mix will read as "game" or "demo".
- Because platforms normalize loudness, over-compressed, maximized ad music loses its loudness advantage and keeps only the flattened dynamics, which reads as cheap. (Inference from normalization targets; not directly sourced.)

### Gaps
- No sourced specifics on bus compression settings (ratio, attack, gain reduction) used in professional ad mixes.
- No primary platform delivery specs for social video ads (Meta, TikTok, YouTube) were retrieved; the -14 LUFS social figure is unverified.

## Q5. Structure: loop-based repetition versus through-composed development; how many bars before a listener notices a loop

### Takeaway
No study gives a bar count at which a loop becomes noticeable or boring. What is supported: repetition itself is liked (looped random sequences are rated more musical), listeners shift attention to new details on each repeat, and AI or default-generated songs fall into generic default arrangements and odd phrase lengths. Identical sample-level repetition is what the ear catches fast (within about 0.4 s cycles at fast tempos).

### Cited Findings
- In a study cited by Margulis, random note sequences played as loops were rated more musical than those heard once, and listeners did not consciously recall which were looped. [University of Arkansas news](https://news.uark.edu/articles/22615/repetition-in-music-pulls-us-in-and-pulls-us-together)
- Listeners shift attention across repetitions, noticing different details (for example a guitarist's pitch bend) on each repeat; with stylistic familiarity, attention shifts from shorter to longer repetitions. [MTO review of On Repeat](https://mtosmt.org/issues/mto.14.20.4/mto.14.20.4.albrecht.html); [Margulis TED transcript](https://www.ted.com/talks/elizabeth_hellmuth_margulis_why_we_love_repetition_in_music?view=transcript)
- A colleague's estimate quoted by Margulis: 99 percent of listening is to passages heard before. [KQED](https://www.kqed.org/arts/11523994/repeat-after-me-its-normal-to-play-the-same-song-over-and-over-again)
- Four round robins at 150 bpm semiquavers cycle every 0.4 s, inside the repetition-noticing window; 6 to 8 push it past 1 s. A short repeated figure leaves the ear nothing to focus on but the sample. [modwheel.net](https://modwheel.net/guides/why-your-ostinatos-sound-like-a-machine-gun)
- MuseBench notes temporal structure, arrangement consistency and repetition only become available as cues in longer (30 s) clips. [MuseBench](https://arxiv.org/html/2610.20310)
- Suno without structural guidance falls back on a default arrangement; one test produced a 12-bar first verse instead of 8 or 16. [James Palm](https://james-palm.medium.com/10-suno-ai-mistakes-that-make-your-songs-sound-like-everyone-elses-b4c8a2784e33); [Substack](https://wewillnotbeflattened.substack.com/p/i-asked-generative-ai-music-platform-suno-to-write-a-podcast-theme-things-got-weird-a66820103f55)
- AI songs show stylistically implausible or abrupt chord transitions. [MuseBench](https://arxiv.org/html/2610.20310)
- Trailer advice: when every hit is oversized, every riser full-band and every cut has a whoosh, the sequence gets louder but less dramatic; a held silent frame after a riser peak often reads bigger than any hit. [add.app](https://add.app/sound-effects/sound-design-for-trailers-hits-rises-drones-pulses/); [Duende Sounds](https://duendesounds.com/trailer-sound-design-elements/)

### Inferences
- Repetition of musical material is fine and even helpful; repetition of identical audio is the tell. A 4 or 8 bar loop that repeats with the same notes but changes something each pass (a new layer, a fill on bar 4 or 8, a velocity swell, a voicing change, a filter opening) reads as arranged. A literally copied loop does not.
- In a 15 to 30 s ad, there is room for at most two or three phrase units, so the human feel comes from a clear arc (setup, lift, payoff on the logo) with standard 4/8 bar phrasing and a cadence that lands on the reveal.

### Gaps
- No empirical number of bars or repetitions after which listeners notice or tire of a loop was found.

## Q6. Sound effects: why synthesized SFX sound game-like or AI-like, why foley and layered library sounds feel real, the overused stock SFX and what replaces them

### Takeaway
Synthesized SFX lose to recorded ones mainly on envelope shape and transient sharpness (attack time, temporal balance), spectral flatness and missing real-world detail, and listeners can recognize them. Real-feeling SFX are built from layers (transient, body, tail) with aligned attacks and a room. Overused stock moves: braam on the reveal, whoosh on every cut, full-band risers; replacements include downers/subfalls, selective transitions, and silence before the hit.

### Cited Findings
- A 2026 study (18 audio professionals, WebMUSHRA, 8 scenes) rated library-sample designs above designs mixing in procedural (Nemisindo) sounds; gaps ranged from 13.8 percent (live-action action) to 34.8 percent (cartoon everyday scene). Synthetic sounds were most believable for sci-fi and drama (lasers, hits, air, rockets) and least for everyday actions. Top discriminating features between synthetic and library sounds: temporal centroid to total length, spectral flatness, high-frequency content, log attack time, zero crossing rate, max-to-total, pitch salience, effective duration, roll-off. Participants asked for more low end on impacts, more high end on liquid and sizzle, a stronger first impact on hits, more layering, more reverb and pitch modulation. Classifiers separated the two groups at 90 to 95 percent accuracy. Note: the paper's Bonferroni claim is inconsistent with its own table. [arXiv 2605.31082](https://arxiv.org/html/2605.31082)
- A synthesized footstep model reproduced the spectrum but lacked temporal sharpness and impact until explicit transient synthesis was added. [Search summary of SFX synthesis paper](https://arxiv.org/pdf/2412.18710)
- In a walking-sound study, subjects could recognize the synthetic sounds and preferred real or foley ones. [Real, foley or synthetic?](https://www.researchgate.net/publication/255962684_Real_foley_or_synthetic_An_evaluation_of_everyday_walking_sounds)
- Layering practice: transient (clear start), body (weight), tail (space); if all three are huge the result is mud; misaligned attacks make a sound weak and smeared; the midrange layer carries identity; a lone effect without a tail feels flat and spaceless. Vendor blogs. [Pixflow](https://pixflow.net/blog/sound-effects-layering/); [SFX Engine](https://sfxengine.com/blog/impact-sound-effect)
- Sound designers note that what they use is often what the audience expects, not what is literally realistic. [Slashdot thread on AutoFoley](https://entertainment.slashdot.org/story/20/08/15/2252206/new-ai-dupes-humans-into-believing-synthesized-sound-effects-are-real)
- The braam is called the most ubiquitous trailer sound of the past decade; overuse dates a cut, and editors replace it with a subfall or "downer" (reverse riser) for similar weight. [Duende Sounds](https://duendesounds.com/trailer-sound-design-elements/); [add.app](https://add.app/sound-effects/sound-design-for-trailers-hits-rises-drones-pulses/)
- Whooshes on every cut make it "feel like a template instead of a story"; transitions are most useful when the eye needs help moving. [add.app](https://add.app/sound-effects/sound-design-for-trailers-hits-rises-drones-pulses/)
- Braams and risers are pitched, so they should match the key of the score or the audience senses something is off. [Duende Sounds](https://duendesounds.com/trailer-sound-design-elements/)
- AI SFX (ElevenLabs, 2024): a library builder found some prompts came back wrong (a slot-machine "fail" sound returned as two clicks and one coin); Randy Thom called the Sora demo's sound design "mediocre at best"; Sound Ideas (April 2024) said AI had not yet significantly affected film, video or game SFX design. [AudioCipher](https://audiocipher.com/post/elevenlabs-ai-sound-effect-generator); [Sound Ideas](https://www.sound-ideas.com/blog/Sound-Design-and-AI)
- Stock sound effects that recur across productions (the Wilhelm scream and similar) are a documented phenomenon. [Wikipedia: Stock sound effect](https://en.wikipedia.org/wiki/Stock_sound_effect)

### Inferences
- A synthesized SFX reads as "game-like" when it has a clean, smooth attack, a flat noise spectrum, a fixed pitch and no tail or room. The fixes map directly onto the study's features: a sharp, short (a few ms) transient click layer, a pitched body with a downward pitch envelope, a broadband tail that decays into a shared room, and a little per-instance variation so repeated UI sounds are not identical.
- For logo reveals: one well-chosen, key-matched low hit or a downer, preceded by a short moment of silence, is more "expensive" than stacking riser plus braam plus whoosh plus ding. UI clicks and dings should be pitched to the music's key.

### Gaps
- No source quantifying how overused specific UI sounds (pop, ding, swoosh) are, or listener studies on their perception in ads.
- No independent technical study of AI-generated SFX artifacts (smeared transients etc.) found; evidence is reviews and opinion.

## Q7. Research on detecting or perceiving AI music (2024 to 2026)

### Takeaway
Machines detect current AI music easily (often above 97 to 99 percent in-domain) through architecture-level spectral artifacts, but robustness drops with short excerpts, speech over music, MP3 and pitch/time edits. Humans are near chance on random pairs (48 to 53 percent) and only reach about 66 percent when comparing stylistically matched pairs; when they do succeed, they cite vocals, lyrics and technical or sound-quality cues.

### Cited Findings
- Deconvolution (upsampling) layers in generators leave small, periodic spectral peaks (related to the checkerboard artifact), inherent to the architecture rather than training data; a simple detector on this exceeds 99 percent accuracy in several scenarios, validated on Suno and Udio. Afchar et al. (Deezer), ISMIR 2025. [arXiv 2506.19108](https://arxiv.org/abs/2506.19108)
- MuseBench detector results: ResNet18 on spectrograms and AST near perfect; ConvNeXt, ViT, SpecTTTra 99.5 to 99.8 percent; Deezer 97.6 percent balanced accuracy; Ircam Amplify 98.6 percent precision but 71.1 percent recall; Resemble AI 46.9 percent. Robustness: pitch/time modification gave Deezer a 93.6 percent false negative rate; MP3 gave Ircam Amplify 63.6 percent FNR. [MuseBench, arXiv 2610.20310](https://arxiv.org/html/2610.20310)
- Broadcast monitoring: detectors degrade substantially on short excerpts, music masked by speech or SFX, and broadcast processing. [arXiv 2602.06823](https://arxiv.org/pdf/2602.06823); [arXiv 2608.07359](https://arxiv.org/html/2608.07359v1)
- Edited or codec-processed human audio is a hard negative that can be mistaken for generation artifacts. [arXiv 2608.14916](https://arxiv.org/pdf/2608.14916)
- Trained classifiers identify Suno more easily than Udio. [Cros Vila, TISMIR](https://transactions.ismir.net/articles/254/files/68774364a6605.pdf)
- Echoes of Humanity (308 participants, 1,232 answers, Suno tracks from r/SunoAI vs MTG-Jamendo): 60 percent overall, 53 percent on random pairs (chance), 66 percent on stylistically similar pairs, 75 percent on similar pairs with lyrics; sound-related, technical and vocal cues were significantly associated with correct answers. [arXiv 2509.25601](https://arxiv.org/html/2509.25601); [Scientific American](https://www.scientificamerican.com/article/can-ai-music-ever-feel-human-the-answer-goes-beyond-the-sound/)
- Group classroom study (2026 preprint): 18 AI tracks (Suno, Udio, Mureka) vs 12 human studio tracks, 3,210 responses, 48.16 percent accuracy, indistinguishable from chance. [Zenodo](https://zenodo.org/records/22278782)
- SONICS reports human sensitivity of 82 percent for Suno v3.5 but only 23 percent for Udio 32 (search summary). [arXiv 2408.14080](https://arxiv.org/pdf/2408.14080)
- Deezer/Ipsos survey (9,000 adults, 8 countries, October 2025): 97 percent could not tell 2 AI songs from 1 human song in a blind test; 80 percent want fully AI music labelled; Deezer receives about 50,000 fully AI tracks per day, 34 percent of daily deliveries. Company-commissioned. [Deezer newsroom](https://newsroom-deezer.com/2025/11/deezer-ipsos-survey-ai-music/); [CBS News](https://www.cbsnews.com/news/ai-generated-music-real-thing-cant-tell)
- Overview of moving from audio deepfake detection to AI music detection. [arXiv 2412.00571](https://arxiv.org/pdf/2412.00571)

### Inferences
- For ad work, the audible risk is less the spectral fingerprint (which listeners cannot hear) and more the perceptual cues people do use: robotic or smeared vocals, generic lyrics, generic arrangement, "too perfect" polish and poor stereo use. Instrumental, code-synthesized music avoids the vocal and lyric cues entirely, so its realism depends on the instrument, performance and space fixes in Q2 to Q4.
- Detectors' weakness on short excerpts and music under voiceover means a 15 to 30 s ad bed is the hardest case for machine detection; human perception then dominates.

### Gaps
- No peer-reviewed listener study specific to stock or library music, or to MIDI mockup detection, was found.
- Full texts of the 2026 arXiv papers (2602 to 2610) were read only in part; exact frequencies of the deconvolution peaks were not extracted.
