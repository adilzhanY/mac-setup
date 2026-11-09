# Transitions between scenes and how sound creates feeling (commercials and motion graphics)

Note on sources: about 30 searches and fetches. Peer reviewed psychology and film sound writing (Randy Thom, Walter Murch) were reachable. Many production tutorials (MusicRadar, Attack Magazine) returned only paywall or navigation text, so several numeric production rules come from secondary tutorial sites and are flagged as practitioner rules of thumb, not research. Format below: claim, then source in brackets.

## 1. Musical and sound transitions between scenes: techniques, lengths, when to cut hard

### Takeaway
Transitions sit on the musical grid. Fills last under a bar. Risers, sweeps and filter moves run 1 to 8 bars (some tools go to 16). Silence before a hit lasts from one beat up to a bar. J and L cuts carry one scene's sound across the picture cut. The strongest film bridge is a sound that changes form across the cut (Randy Thom's mill clank turning into train wheels).

### Cited Findings
**Fills, risers, sweeps, reverse effects**
- Fills are short, "typically less than a bar (measure) long". They do not build enough tension for a large section change on their own, but they work for breaking up a section. ([Arends notes on transitions](https://publish.obsidian.md/arends-digital-garden/Notes/20+Shareable/22+Music+Production+%F0%9F%94%88/22.03+Recording+Tips/How+to+create+transitions+in+your+arrangements))
- Transitions "don't have to be obvious; they can be tucked under the rest of the parts". Taking parts out matters as much as adding them, as long as they leave "without it sounding like they were suddenly muted". ([Arends notes](https://publish.obsidian.md/arends-digital-garden/Notes/20+Shareable/22+Music+Production+%F0%9F%94%88/22.03+Recording+Tips/How+to+create+transitions+in+your+arrangements))
- Standard kit: drum fills (snare rolls, tom fills), risers, downlifters after drops, brief silence before a drop, crash cymbal to mark a section start. ([Flowstate arranging guide](https://flowstate-learn.pages.dev/guides/arranging-songs))
- A riser usually spans one to several bars. Pick its length first, because the length sets the slope of the rise. Simplest build: filtered noise through a band pass or high pass filter, with the cutoff automated upward over the bars before the drop. ([UJAM, EDM transitions](https://www.ujam.com/tutorials/how-to-create-huge-edm-transitions/); [Violet Recording, risers and sweeps](https://violetrecording.com/how-to-make-risers-and-sweeps/))
- Reverse cymbals and reversed instruments were the classic swell methods. Reverse a recorded sound, stretch it, and automate a filter opening across it. ([Violet Recording](https://violetrecording.com/how-to-make-risers-and-sweeps/))
- AIR's The Riser maps length to octave: transitions start at 16 bars at low octaves and get as short as 1/16 bar at high octaves. ([AIR Music Technology, The Riser](https://airmusictech.com/virtual-instruments/the-riser))
- Uplifters rise in pitch or amplitude to build into a new section. Downlifters fall in pitch or amplitude at the start of a section. Reverse reverb is made by rendering a reverb tail to audio and reversing it so it swells into the source sound. ([Sweetwater InSync, 5 transition effects](https://www.sweetwater.com/insync/5-transition-effects-to-spice-up-your-music/); [Recording Arts](https://recordingarts.com/?p=2798))
- Tape stop and tape start come from switching a tape emulation between play and stop, with "Play Time" and "Stop Time" setting the speed. Timing is fiddly, so automate the transport and adjust by ear. ([MusicRadar, tape stop](https://www.musicradar.com/how-to/tape-stop-start))
- A breakdown into a drop: close the filter on synths and mute drums, then reopen the filter, unmute, and add an impact. ([Soundbridge, groove to breakdown](https://www.soundbridge.io/how-to-create-smooth-transitions-from-groove-to-breakdown))
- Bring parts in and out in pairs or fours, and place gaps and fills inside 8 bar transitions. ([Flowstate](https://flowstate-learn.pages.dev/guides/arranging-songs))

**Silence or gap before the hit**
- Tutorials suggest muting everything for one beat before a drop, a half or full bar, or cutting instruments one or two bars before. A sparser build makes the gap hit harder, and an overcrowded build weakens it. Some producers pull only the low end instead of cutting everything. The figures are spread across these sources and are practitioner advice. ([FaderPro, silence](https://blog.faderpro.com/creativity/silence-in-music-production/); [Point Blank, drops](https://www.pointblankmusicschool.com/blog/how-to-make-your-drops-hit-harder-tips-for-edm-producers/); [SampleFocus, space and silence](https://samplefocus.com/blog/using-space-and-silence-in-music-production))

**Film editing: J cuts, L cuts, sound bridges**
- J cut: the incoming scene's audio starts before the picture cut. L cut: the outgoing scene's audio continues after the cut. Both are kinds of sound bridge, the umbrella term for any sound that joins two scenes. A single event (a phone ring, a door slam) can also start in one scene and finish in the next. ([Filmdaft, L and J cuts](https://filmdaft.com/the-l-cut-and-j-cut-how-film-editors-use-audio-to-control-time/); [Adobe, J and L cuts](https://www.adobe.com/creativecloud/video/discover/j-cut-and-l-cut))
- Workflow: get the pacing right with a straight cut first, then split audio from picture. Test the straight cut against short J and L versions. ([Boris FX, L and J cuts](https://borisfx.com/blog/l-and-j-cuts-smoother-more-cinematic/))
- Randy Thom on sound as transition: "Over a transition from one period to the other, one or more sounds can go through a metamorphosis." His example is a mill's rhythmic clank that becomes a train's click clack. When a sound changes in response to the story, "its power and richness grow exponentially." ([Randy Thom, Designing a Movie for Sound](http://filmsound.org/articles/designing_for_sound.htm))
- Murch: "Music and dialogue are perceived and analysed by different parts of the brain. Sound effects provide the bridge between the two." ([NFTS, Walter Murch masterclass](https://nfts.co.uk/blog/triple-oscar-winning-sound-designer-editor-walter-murch-deconstructs-iconic-sequence-))
- Worldizing (Murch, first used on THX 1138): play a sound back in the space where it should be heard and re-record it there, so a sound can move between "worlds" (radio in the room versus radio inside the car). ([filmsound.org, worldizing](https://filmsound.org/terminology/worldizing.htm))

**Whooshes across a cut**
- Match whoosh length to the movement it covers. A whoosh that outlasts its transition is a common reason it feels wrong. Put the whoosh peak just before the cut, so the edit lands right after it. Vendor advice. ([Morphic, whoosh](https://morphic.com/fr/resources/sounds/whoosh-sound-effect))
- Animation sound designer Jeff Shiffman (Boom Box Post): "moving a sound effect only a few frames can change a moment from flat to outright hilarious". He designs the camera whooshes first, to support the editor's rhythm. ([A Sound Effect, animation sound design](https://www.asoundeffect.com/animation-sound-design/))

### Inferences
- Converting grid lengths to time with ms = 60000 / BPM per beat: at 120 BPM one beat is 500 ms and a bar of 4/4 is 2 s. So a 1 bar reverse cymbal takes 2 s, and a one beat gap before the hit takes 500 ms. In a 15 to 30 s spot a 4 bar riser at 120 BPM (8 s) would use a third to half the film, so short spots likely need 1 to 2 bar builds or a faster tempo. This is my arithmetic, not a sourced rule.
- Hard cuts (no bridge) suit a change of world that should feel like a jolt or a reveal, and they work best on a downbeat with a transient landing on the first frame. The L or J cut suits continuity of feeling. This follows from the sources above but no source gives a rule for when to choose a hard cut.
- Key change, half time, stop time and tempo change as ad transitions: no reliable source found with numbers (see Gaps). In practice a half time switch keeps the BPM and grid but doubles the backbeat spacing, so the edit can keep cutting on the same grid while the feel slows down.

### Gaps
- No reachable source gave standard pre-lap lengths in frames for commercials. The MusicRadar transition articles (7 techniques, 10 steps, 8 drop recipes) and Attack Magazine's "Filter Fills" returned only page furniture.
- No sourced lengths for tape stops, sidechain swells (reverse sidechain or "pumping" into a hit), pickup notes, or held chords.
- No sources on key changes or tempo changes used as scene transitions in advertising.

## 2. Why sudden volume drops read as mistakes, and how to make contrast read as intended

### Takeaway
Listeners notice a 1 dB change only under good conditions. Around 3 dB is a clearly audible change, and 10 dB sounds about half as loud. A drop that changes only level, with no musical reason (no arrangement change, no tail, no cadence), gives the ear nothing to explain it, so it reads as a fault. Professionals thin the arrangement, filter, drop the drums, keep a bed and let tails ring instead of pulling the fader. No study was found that measures directly when a loudness dip stops reading as intended.

### Cited Findings
- About 1 dB is the textbook just noticeable difference in intensity. It can fall to 1/3 or 1/2 dB for loud sounds. ([HyperPhysics, decibels](https://hyperphysics.gsu.edu/hbase/Sound/db.html))
- The average listener cannot tell apart level differences under 3 dB, while trained listeners can pick out 1 dB. An EQ move smaller than 3 dB is imperceptible to most listeners. ([Digital Sound and Music, 4.2.1.1](https://digitalsoundandmusic.com/chapters/ch4/4-2))
- A change of 3 dBA is generally regarded as just noticeable in environmental acoustics. ([Acoustical, dBA](https://www.acoustical.co.uk/decibels-acoustic-principles/what-does-dba-mean/))
- Loudness follows a power law with an exponent of about 0.3, so each 10 phon (10 dB at 1 kHz) is roughly a doubling or halving of perceived loudness. Listeners mostly heard 10 dB as at least twice as loud and 5 dB as less than twice. ([Wikipedia, Sone](https://en.wikipedia.org/wiki/Sone); [Sengpielaudio loudness calculator](https://www.sengpielaudio.com/calculator-loudness.htm))
- Gaps of 4 to 5 ms can be heard in continuous sound (2 to 3 ms with practice). Gap detection gets up to an order of magnitude worse when the sounds on either side of the gap are spectrally different. ([Phillips et al. 1997, PubMed](https://www.ncbi.nlm.nih.gov/pubmed/9193057))
- Spoken audio rule of thumb: after about one second of silence listeners feel an uncomfortable gap, and by about five seconds they wonder whether more is coming. Podcast industry advice, not research. ([Radio Today, silence is golden](https://radiotoday.com.au/silence-is-golden-why-shutting-up-makes-people-listen/))
- Removing parts should not sound like a sudden mute. ([Arends notes](https://publish.obsidian.md/arends-digital-garden/Notes/20+Shareable/22+Music+Production+%F0%9F%94%88/22.03+Recording+Tips/How+to+create+transitions+in+your+arrangements))
- Musical expectancy (Juslin and Västfjäll): emotion arises when rhythm or harmony "violates, delays, or confirms a listener's expectations". Rhythm violations trigger strong neural responses (Vuust et al. 2009). ([Wikipedia, Music and emotion](https://en.wikipedia.org/wiki/Music_and_emotion))
- Randy Thom argues for leaving pauses: "To stay around after the obvious 'action' is past, so that we can listen", and "Into these little pauses sound can creep." ([Randy Thom](http://filmsound.org/articles/designing_for_sound.htm))
- Shiffman: "See how a pause between a reaction or line of dialog can be used for your benefit and work with it." ([A Sound Effect](https://www.asoundeffect.com/animation-sound-design/))

### Inferences
- A level drop under about 3 dB is mostly invisible, so it buys no contrast. A drop of 6 to 10 dB is clearly heard (10 dB reads as half as loud), so it needs a visible or musical reason, or the ear treats it as a fault. Derived from the JND and sone figures, not from a dropout study.
- The gap detection data suggests why "keep a bed" works. A gap between two spectrally similar sounds is easy to hear (a few ms). A pad, room tone or reverb tail under the gap fills the spectrum, so there is no hole for the ear to flag, only a change in texture.
- An intended breath has three signs. It lands on the grid (beat or bar line, usually right after a cadence or a hit). It keeps a tail or a bed. It resolves into something bigger within a short, predictable time (one beat to one bar in the production sources, which is 500 ms to 2 s at 120 BPM). A mistake has none of these: off grid, cut tails, nothing after it. My synthesis.
- Short full silences of about 100 to 300 ms (a sixteenth to an eighth note at 120 BPM is 125 to 250 ms) just before a hit are the safe use of true silence, since the hit arrives before the ear can wonder. This fits the one beat gap advice but the exact 100 to 300 ms range is not sourced.

### Gaps
- No study found on perceived audio "dropouts" in ads or video, or on how much reduction (in dB or time) audiences read as intentional rather than broken.
- No broadcast silence detector thresholds were found (these exist in playout systems but no source was reached).

## 3. Sound and emotion: timbre, register, harmony, tempo, density, space

### Takeaway
Psychology gives solid mappings for arousal (tempo, loudness, pitch variation, staccato) and coarser ones for valence (mode, consonance). Juslin's BRECVEMA lists the mechanisms an ad can use: brain stem reflex (sudden loud hits), rhythmic entrainment (tempo pulls the body), expectancy (tension and release), and conditioning or memory (sonic logos). Brand words like "premium", "trust" or "precision" are not studied in this literature. They come from agency frameworks that publish little evidence.

### Cited Findings
**Mechanisms**
- Juslin and Västfjäll (2008) proposed mechanisms of musical emotion that differ in induction speed, volitional control and dependence on musical structure. The later BRECVEMA set: Brain stem reflex, Rhythmic entrainment, Evaluative conditioning, Contagion, Visual imagery, Episodic memory, Musical expectancy, Aesthetic judgment. ([Juslin 2013, Physics of Life Reviews](https://ui.adsabs.harvard.edu/abs/2013PhLRv..10..235J); [JAMK music psychology notes](https://oppimateriaalit.jamk.fi/?p=6565))
- Brain stem reflex: acoustic features are taken as a signal of an urgent event, especially "sudden, loud, and dissonant" music. Rhythmic entrainment: rhythm pulls bodily rhythms such as heart rate. ([Wikipedia, Music and emotion](https://en.wikipedia.org/wiki/Music_and_emotion))
- Critique: the mechanisms (contagion in particular) are poorly defined and ignore context and culture. ([Wikipedia, Music and emotion](https://en.wikipedia.org/wiki/Music_and_emotion))

**Feature to emotion mappings**
- Tempo is "typically regarded as the most important" factor and is linked to arousal and valence. Major is linked to happiness, minor to sadness. Major triads elicit more happiness and energy, minor triads more melancholy and nostalgia (Lahdelma and Eerola 2016). Louder music and more pitch variation mean higher arousal (Gomez and Danuser 2007). Resolving harmonies give tension and release, unexpected harmonies give surprise (Juslin 2019). Legato reads as cohesive, calm, sad or scary. Staccato reads as tense, energetic, amusing or surprising (Carr et al. 2023). ([Wikipedia, Music and emotion](https://en.wikipedia.org/wiki/Music_and_emotion))
- Sad music in Juslin and Laukka (2004): minor mode, slow tempo, low pitch, low dynamics, dissonance, descending pitch (reported by a secondary source). ([Juslin and Laukka 2004, J. New Music Research](https://www.tandfonline.com/doi/pdf/10.1080/0929821042000317813))
- Expression marks correlate with emotions: "Dolce" with tenderness (r = 0.98), "Scherzando" with happiness (r = 0.76), "Grave" with sadness (r = 0.88). Harmonic motion creates "tension", "release", "climax", "repose". Intrinsic musical structure gives "dynamically shifting levels of tension, arousal and stability" and suits time based emotions such as relief and hope. Associative coding (church organ reads as solemn) is listener and culture dependent. ([Juslin 2013, Frontiers in Psychology](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2013.00596/full))
- Valence and arousal are the main axes. Three dimensional models reduce to two without much loss of fit (Eerola and Vuoskoski 2011). A 2025 meta analysis of music emotion models found arousal predicted better (r = 0.81) than valence (r = 0.67). ([Eerola and Vuoskoski 2011](https://is.muni.cz/el/phil/jaro2017/PS_BA007/um/A_comparison_of_the_discrete_and_dimensional_models_of_emotion_in_music.pdf); [C4DM seminar, Eerola 2025](https://www.c4dm.eecs.qmul.ac.uk/news/2025-06-06.C4DM-Seminar_Tuomas_Eerola))
- Randy Thom: "We, the audience, interpret sound with our emotions, not our intellect." Distance against closeness of the same sound is "a very powerful element". ([Randy Thom](http://filmsound.org/articles/designing_for_sound.htm))

**Sonic branding practice**
- Netflix "ta-dum" (Lon Bender): brief asked for both tension and release. Core layer is Bender knocking his wedding ring on a cabinet, with a slowed anvil and muted hits under it, and a reversed guitar sample as the tail, called "The Blossom". He made 20 to 30 options. Goat and underwater bubble options were rejected. Hans Zimmer later made the long theatrical version. ([MusicRadar, Netflix ta-dum](https://www.musicradar.com/news/the-netflix-ta-dum-sound-features-a-reversed-electric-guitar-sample-that-was-created-using-90s-effect-pedals); [SlashFilm](https://slashfilm.com/netflixs-signature-launch-sound-was-almost-the-bleating-of-a-goat))
- Mastercard: the melody must be "simple, neutral, likeable, memorable". A 30 s core melody adapts across genres (operatic, cinematic, EDM), with a 3 s musical logo at point of sale and hundreds of mood variations. A Mastercard and GfK study says 77% felt the sound made the transaction more trustworthy (company funded). ([Marketing Week, Mastercard CMO](https://www.marketingweek.com/people-asked-if-i-was-smoking-something-mastercards-cmo-on-developing-its-new-sonic-branding/); [Mastercard, science of sound 2024](https://www.mastercard.com/nz/en/news-and-trends/stories/2024/inside-the-science-and-success-of-sound.html))
- amp's Best Audio Brands index scores brands on trust, recognition, efficiency and engagement over 12 months, using desk research, AI evaluation and social monitoring. The 2022 edition covered 250 brands. Mastercard has ranked first in several editions. ([amp Best Audio Brands](https://ampsoundbranding.com/best-audio-brands); [Transform magazine 2023](https://www.transformmagazine.net/articles/2023/mastercard-holds-ground-as-best-audio-brand-says-amp/))
- Process from a sonic branding agency: define brand personality as "sonic adjectives", sketch options, test memorability, deliver several lengths. A logo should be recognisable within about 3 seconds. ([IRPR, how to design a sonic logo](https://sounddesign.irpr.agency/guides/how-to-design-a-sonic-logo/))
- Agency research claims are self reported. One agency claims 73% positive emotion association and 52% recognition on TikTok, which is unverified. ([A-MNEMONIC, frameworks](https://a-mnemonic.com/sonic-branding-frameworks/))

### Inferences
Practical mapping for product films, built from the cited arousal and valence findings. The brand words are my labels, not tested categories:
- Precision: staccato, short envelopes, bright but not harsh transients, sparse rhythm locked tightly to the grid, consonant harmony, dry or short space. (Staccato means tense or energetic in Carr et al., so keep tempo moderate to stay calm.)
- Trust or calm: legato, moderate to slow tempo, mid or low register, consonant major or open fifth harmony, cadences that resolve, low pitch variation (low arousal, positive valence).
- Warmth: legato, mid and low register, soft attacks, rounder or darker timbre, close (intimate) space. Thom's distance against closeness contrast supports close sound for intimacy.
- Delight or playful: staccato, higher register, major, faster tempo, more pitch variation, small expectancy surprises that resolve quickly.
- Effortless: legato, steady pulse without dense fills, few hard transients, long smooth envelopes, consonance.
- Premium: restraint and space (Thom's "room" for sound). Fewer elements, longer tails, wide but uncluttered stereo, one well made signature sound (Netflix layered a real object with a musical tail). This is the least evidenced mapping.

### Gaps
- Juslin and Laukka's (2003) full cue table (tempo, sound level, timbre, articulation by emotion) was not retrievable in full text.
- No peer reviewed study found that maps sound features to "premium", "precision" or "trust". Agencies (Sixième Son, MassiveMusic, Antfood, amp) do not publish their emotion frameworks in detail.
- Timbre and brightness mappings (bright means happy or active, dark means sad or serious) are widely assumed, but no source reached here stated them with data.

## 4. Sound for a transformation (2D to 3D, assembly, product resolving into a logo)

### Takeaway
A transformation sounds best when one sound changes form across it (Thom's metamorphosis), with tension built through musical material (rising scales, faster subdivisions, Shepard style layered octaves) and released on harmonic resolution at the logo. The logo moment then needs a short, simple, owned "button" that pairs a real tactile hit with a musical tail (the Netflix model) and can be recognised in about 3 s.

### Cited Findings
- Thom: when a sound changes in response to the story, "its power and richness grow exponentially". The mill clank turning into the train's click clack is the template for a sound that morphs with an object. ([Randy Thom](http://filmsound.org/articles/designing_for_sound.htm))
- Shepard tone: tones stacked an octave apart give the illusion of endless rising pitch. In Dunkirk it is mostly a discrete rising diminished scale. At the climax the bottom part plays the scale slowly, the middle at double speed and the top at quadruple speed. That is a riser built from musical material plus rhythmic acceleration. Zimmer, asked if the tension should resolve: "No." A falling version feels like relaxation. ([Medium, The Dunkirk soundtrack is cleverer than you think](https://medium.com/world-of-music/the-dunkirk-soundtrack-is-way-cleverer-than-you-think-18f5dc155d91); [Kottke, Shepard scale in Dunkirk](https://kottke.org/18/05/hans-zimmers-clever-use-of-the-shepard-scale-in-dunkirk))
- Nolan used a Shepard tone for the Batpod acceleration sound in The Dark Knight. ([Mental Floss](https://www.mentalfloss.com/entertainment/movies/inside-auditory-illusion-makes-hans-zimmers-movie-scores-so-anxiety-producing))
- Harmonic motion creates tension, release, climax and repose. Intrinsic structure suits time based feelings such as relief and hope. ([Juslin 2013, Frontiers](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2013.00596/full)) Expectancy can be violated, delayed or confirmed. ([Wikipedia, Music and emotion](https://en.wikipedia.org/wiki/Music_and_emotion))
- Netflix's brief for its ident was "tension and release" in one short sound: a physical knock with a reversed (swelling) tail. ([MusicRadar](https://www.musicradar.com/news/the-netflix-ta-dum-sound-features-a-reversed-electric-guitar-sample-that-was-created-using-90s-effect-pedals))
- A strong accent placed exactly when the animation completes is the common pattern for logo reveals and title entrances. ([Cursa, audio and final rhythm](https://cursa.app/en/page/audio-and-final-rhythm-using-sound-to-support-motion))
- It is "very rare that a single sound effect works well on its own". Layering is the norm. ([A Sound Effect, Shiffman](https://www.asoundeffect.com/animation-sound-design/))
- Mastercard runs one melody from a 30 s piece down to a 3 s logo, so the logo is the resolved short form of music already heard. ([Marketing Week](https://www.marketingweek.com/people-asked-if-i-was-smoking-something-mastercards-cmo-on-developing-its-new-sonic-branding/))

### Inferences
- A transformation recipe from these sources: (1) start with one sound tied to the 2D state (a pencil scratch, a thin sine); (2) morph it as the object gains dimension (add layers, open a filter, widen the stereo, lower the register for mass); (3) build with musical material, a rising scale or arpeggio whose subdivisions double (quarters, eighths, sixteenths) over the last 1 to 2 bars, Shepard style if it must feel endless; (4) a short gap or suck back (reverse tail) of a beat or less; (5) land the logo on a tonic chord with a tactile transient and a ringing tail, which is the "button"; (6) let the tail ring or fade. Do not cut it.
- The melody in the button should come from the film's own music (the Mastercard model), so the logo reads as resolution rather than a new sound.

### Gaps
- No source found that studies build ups or buttons in commercials specifically, or measures how harmonic resolution on a logo affects brand recall.
- No reachable School of Motion or Antfood article with concrete transformation sound techniques. Two School of Motion podcast episodes on sound exist (2017 "Sound Design for Fun and Profit"; 2019 episode 71 with Sono Sanctus) but no transcript was reached.

## 5. Motion curves and sound envelopes

### Takeaway
Apple's audio haptic principles (causality, harmony, utility) are the clearest statement: sound, touch and picture must agree in timing and character. Practitioners say the sound should "breathe with" the motion curve, not fire one transient at the start. No source gives a formal mapping from easing curves to envelope shapes. That mapping has to be derived.

### Cited Findings
- Apple WWDC 2019 session 810, "Designing Audio-Haptic Experiences": causality (it must be obvious what caused the feedback), harmony (audio, haptics and visuals agree, as they naturally do in the real world), utility (add only where it gives clear value). Case study: the Apple Pay confirmation checkmark. ([Apple WWDC19 810](https://developer.apple.com/videos/play/wwdc2019/810); [WWDC Notes](https://wwdcnotes.com/documentation/wwdc19-810-designing-audiohaptic-experiences/))
- WWDC 2021 session 10278, "Practice audio haptic design": a haptic and an audio asset that do not match feel disjointed. They demonstrate combining the haptic of one asset with the sound of another to fix it. ([Apple WWDC21 10278](https://developer.apple.com/videos/play/wwdc2021/10278))
- "The sound needs to breathe with that curve, not fire a transient at the start and stop." Frame accurate sync is required. Beat based sync (on the music grid) differs from cue based sync (whoosh, impact on events). ([Cursa, audio and final rhythm](https://cursa.app/en/page/audio-and-final-rhythm-using-sound-to-support-motion))
- Sharp ease in creates punch. ([Animation principles, slow in and slow out](https://skills.sh/dylantarre/animation-principles/slow-in-out-mastery))
- Shiffman time compresses sounds (animal roars) to match performance length and moves effects by a few frames to change the feel. ([A Sound Effect](https://www.asoundeffect.com/animation-sound-design/))
- Whoosh length should match the movement, with the peak just before the cut or landing. ([Morphic](https://morphic.com/fr/resources/sounds/whoosh-sound-effect))

### Inferences
Curve to envelope mapping, derived from the above (not a sourced standard):
- Ease in (slow start, fast end): the sound rises with the velocity. A swelling envelope (reverse sound, riser, filter opening) peaks at peak speed, and the transient sits at the end of the move.
- Ease out (fast start, slow end): a fast attack at the start of the move and a long decay that follows the deceleration. A whoosh with a quick onset and a tail, or a pluck with long release.
- Ease in out: the loudness and brightness of a whoosh peak at mid move (maximum velocity). Pitch can follow velocity too (Doppler like).
- Overshoot: a transient at the moment of contact, plus a small secondary blip or pitch bend at the overshoot peak.
- Settle (damped spring): decaying repeats or a resonant ring whose decay time matches the settle time. Repeat spacing follows the spring's oscillation period.
- Practical rule: drive sound parameters (gain, cutoff, pitch) from the same curve as the motion property (often velocity, the derivative of position), sampled per frame. At 30 fps one frame is 33 ms, at 60 fps 16.7 ms, so "a few frames" of offset is 50 to 100 ms, which Shiffman says changes how a moment reads.

### Gaps
- No academic or practitioner source found that maps cubic bezier or spring parameters to ADSR or filter envelopes.
- No data on how many ms of audio to picture offset viewers tolerate for motion graphics hits (broadcast lip sync tolerance standards exist but were not retrieved here).
