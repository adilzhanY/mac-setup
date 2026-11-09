# AI and template sound patterns, and how professionals make sound feel human

Scope note: many primary pages (Audiokinetic Wwise docs, FMOD docs, Boing Boing, NewscastStudio, Tom's Guide) returned HTTP 403 or empty bodies to the fetch tool during this session. Where a finding rests only on a search engine summary of a page (not a full read), it is marked "(search summary)". Numbers that come from general practice and could not be tied to a source are kept in Inferences or Gaps and labelled as heuristics, never as facts.

## 1. What makes AI and template video sound cheap or generic (viewer, editor, critic complaints)

### Takeaway
Direct, well-sourced criticism of AI video sound is thin; the concrete complaints that exist are about foley that does not match the material or action (the "crunchy spaghetti" example), poor sync with dialogue, unreliable output, and generic stock stingers with no dynamic contrast. The template sound problem is mostly documented by trailer and library sound designers, who name the same culprits: overused braams and stock stingers, every second filled, and sound that is wrong for the moment even when it sounds good alone.

### Cited Findings
- A widely shared AI clip of "Will Smith eating spaghetti" had the character seem to crunch the pasta instead of making realistic eating sounds; the article attributes this to training data bias toward crunching effects paired with chewing mouths. This is the clearest documented case of AI sound not matching material: [getcoai / Sora vs Veo coverage](https://getcoai.com/news/sora-vs-veo-3-fight-openai-readies-sora-2-with-audio-to-challenge-google/) (search summary).
- Google's own V2A (video to audio) work was reported to struggle to sync a provided transcript with someone talking on screen: [Inverse on Google V2A](https://nc.inverse.com/tech/google-v2a-ai-generative-sound-videos) (search summary).
- A Tom's Guide head to head of Sora 2 and Veo 3.1 across 7 audio prompts found Sora 2 often ignored difficult audio and visual instructions, and said "gradual transitions and delicate sound design are still frontiers" for both: [Tom's Guide](https://www.tomsguide.com/ai/ai-image-video/sora-2-vs-veo-3-1-i-tested-both-ai-video-generators-with-7-audio-prompts-heres-the-winner) (search summary; full page body could not be fetched).
- Zapier on Veo 3: native audio is the headline feature and "impressive…when it works", i.e. reliability is the complaint more than timbre: [Zapier](https://zapier.com/blog/google-veo/) (search summary).
- Comparisons in 2026 say Veo 3 "now trails slightly in natural fit and liveliness" and that Sora 2 gets the edge for "more natural, contextually appropriate sound": [Atlas Cloud native audio comparison](https://www.atlascloud.ai/blog/guides/ai-video-models-native-audio-compared) (search summary, vendor source).
- Many "no sound" Veo complaints come from settings (audio toggle off, prompt never asked for sound), not quality: [veo3gen guide](https://www.veo3gen.app/blog/veo3-no-audio-problem-guaranteed-sound) (search summary, promotional source).
- Trailer sound: a sound agency blames flat trailer impact on "generic stock stingers, no sub-bass design, and a mix without dynamic contrast": [IRPR Sound, weak trailer impact](https://sounddesign.irpr.agency/solutions/weak-trailer-impact/) (search summary).
- The braam "became somewhat of a cliche through overuse in a particular era of trailers" but stays effective "when crafted and deployed with care": [IRPR Sound glossary, braam](https://sounddesign.irpr.agency/glossary/braam/) (search summary). Popularised by Hans Zimmer: [Ableton blog](https://www.ableton.com/en/blog/learn-how-to-make-high-impact-sounds-for-movies-and-trailers/) (search summary).
- A library page argues three even, low impacts give the same weight as a braam but read "as controlled rather than epic": [Morphic, cinematic sound effects](https://morphic.com/resources/sounds/cinematic-sound-effects) (search summary).
- Filling every second leaves no room to build: "Without quiet, your loud moments have nothing to contrast against": [Violet Recording, sound design for trailers](https://violetrecording.com/sound-design-for-trailers/) (search summary).
- Whoosh choice: light airy whooshes suit text, menus and delicate graphics; dark, distorted, low passed whooshes suit heavy objects and trailer cuts. Sweeps that are too slow drag behind picture, too fast "read as a click". Starting point: match whoosh duration to transition length: [Sonilo whoosh guide](https://sonilo.com/ai-music/whoosh-sound-effect-guide) (search summary).
- A sound can be exciting on its own and still be wrong for the moment it supports: [Pixflow, cinematic whooshes](https://pixflow.net/blog/cinematic-whoosh-sound-effects/) (search summary).
- Copy pasted patterns and repeated identical samples are noticeable because listeners pick up on the repetition; "unvaried velocity values can be one of the main culprits behind a performance sounding like it was performed by a robot": [Splice, humanize your drums](https://splice.com/blog/humanize-your-drums/).

### Inferences
Synthesis catalog: each audible "AI or template" pattern, why it reads as fake, and the countermeasure. Parameters marked (heuristic) are working starting points derived from the sources in sections 2 and 3, not published standards.

| Pattern | Why it reads as fake | Countermeasure, with parameters |
|---|---|---|
| Same whoosh on every transition | Identical waveform repeated is the "machine gun effect" (section 2); real air movement never repeats exactly. The ear also learns the cue and stops hearing it. | Pool of 3 to 6 whoosh variants, shuffle with "avoid last 1 or 2" (Unity Shuffle and Avoid Repeating Last, section 2). Pitch jitter about ±50 to ±150 cents (heuristic, inside the ±170 to ±280 cent span game devs use for footsteps). Gain jitter about ±1 to ±3 dB (heuristic). Length matched to the move (Sonilo). Weight matched to object size: light and bright for UI text, dark and low passed for big objects. Skip the whoosh on minor moves entirely. |
| Identical "pop" or "click" on every element appearing | Same as above, plus no hierarchy: everything is equally loud so nothing is important. | Sound only the elements that carry meaning (section 4). For a stagger of N items, either one sound for the group, or a decaying series: each successive hit 1 to 3 dB quieter and slightly pitched (heuristic), with small timing offsets so hits are not on a perfect grid. |
| Constant four on the floor at about 120 BPM | Library and AI defaults converge on safe tempo and groove (section 6: AI systems flatten rhythm and timing variation). A beat that never changes ignores the edit. | Let the cut decide tempo (pick BPM so key cuts land on beats or bars). Drop the kick for sections, use half time, break to silence before the hero moment. |
| Corporate ukulele, handclaps, uplifting pluck | Recognised as the default "life is awesome" signal (section 6), so it signals "template" before it signals mood. | Choose instrumentation from the product world (section 5). If the brief is "upbeat", get it from rhythm and harmony, not from the stock instrument. |
| Stock risers and braams before every reveal | Overused trailer grammar (IRPR, Morphic); identical shape every time makes the reveal predictable. | Build tension with something specific (a product sound pitched up, filtered noise of the actual material). Use a riser at most once per spot, and consider a pre hit silence of a few frames instead. |
| Every hit quantised to the grid, identical velocity | Robotic feel (Splice); perfectly identical attack times and levels never happen in performance. | Timing jitter a few ms (Logic ±10 ticks ≈ 5 ms at 120 BPM with 960 PPQ, section 3), velocity variation, accent pattern (strong downbeats, weaker offbeats). But keep hits that sync to picture frame accurate; humanise the music, not the sync points. |
| Wall to wall music, no silence | No contrast, so nothing feels loud or important (Violet Recording). | Plan at least one drop to near silence or room tone before the key message. Duck music 6 to 12 dB under voice or key effects (heuristic). |
| Sound not matching material or size | The spaghetti crunch case: the sound comes from a statistical default, not from the object. | Choose or synthesise by material (glass, metal, paper, plastic) and size (bigger means lower pitch, longer decay, more low end). |
| Music that ignores the edit | Stock tracks are written without picture; AI music is generated without picture. Cuts land mid phrase. | Edit music to picture: cut on bars, re time sections, add hits from the score on key cuts, end on a real cadence instead of a fade. |

### Gaps
- No systematic survey or study of viewer complaints about AI video sound was found. The evidence is anecdotal reviews and vendor content, several with SEO style dating.
- Reddit threads (r/sounddesign, r/editors, r/VideoEditing, r/MotionDesign) and YouTube essays on AI video sound did not surface in searches; no direct quotes from those communities are included.
- No source specifically criticising Kling, Pika, Runway, Canva or CapCut template audio was found.

## 2. The "machine gun effect" and the standard fixes (round robin, randomisation, middleware settings)

### Takeaway
The machine gun effect is the audible repetition of one identical sample triggered several times in a row. The standard fixes are a pool of recorded variations played in shuffle or random with no immediate repeats, plus small per trigger randomisation of pitch, volume and timing. Middleware exposes these as min/max randomisers (pitch in cents, volume in dB); official default ranges could not be retrieved, but engine examples put footstep pitch jitter at roughly ±10% to ±15% (about ±170 to ±280 cents).

### Cited Findings
- Definition: playing the same sample repeatedly on consecutive notes of the same pitch is the machine gun effect: [KVR forum, sampler techniques against machine gun samples](https://www.kvraudio.com/forum/viewtopic.php?p=7231754) (search summary).
- Even with one sample, randomising it slightly (for example a random pitch envelope) "drastically" reduces the effect; pitch shifting the whole sound helps "but not as much as you'd think": [KVR forum](https://www.kvraudio.com/forum/viewtopic.php?p=7232081) (search summary, anecdotal).
- Round robin modes: variations played in fixed order or randomly, and a "Random Exclusive" mode where no variation plays twice in succession: [Steinberg HALion, Variation Groups](https://steinberg.help/halion/v7/en/halion/topics/editing_programs_and_layers/sound_editor_variation_groups_section_r.html) (search summary).
- Unity Audio Random Container (official docs, read in full): volume randomisation and pitch randomisation are each a min/max distribution, with "both minimum and maximum to zero" disabling it; pitch is defined on a logarithmic cent scale. Playback modes: Sequential, Shuffle ("removes audio clips from the pool after they've played... avoids repetition until all audio clips have played"), Random (pool intact, can repeat). "Avoid Repeating Last" sets how many items must play before one can play again. Trigger timing (Pulse or Offset) also has min/max randomisation, and Pulse mode is suggested for an automatic rifle: [Unity Audio Random Container reference](https://docs.unity.com/en-us/engine/6000.3/manual/audio/random-container/ui.md).
- Godot's AudioStreamRandomizer uses a pitch multiplier and a volume offset in dB, where 1.0 and 0.0 mean no variation: [Godot AudioStreamRandomizer class doc](https://git.objectionable.solutions/Sara/this-city/raw/branch/development/engine/doc/classes/AudioStreamRandomizer.xml) (search summary).
- SFZ sampler format: `pitch_random` is in cents, default 0, range 0 to 9600; a bipolar ±20 cent humanisation is built with a fixed -20 cent shift plus up to 40 cents random: [sfzformat.com, tune_random](https://sfzformat.com/opcodes/tune_random) (search summary).
- Wwise: a forum thread uses an example random pitch of -25 cents on a parent container and discusses whether child containers inherit the same offset: [Audiokinetic Q&A 2909](https://audiokinetic.com/qa/2909/random-pitch-how-is-it-applied-to-children-containers) (search summary).
- Game dev footstep practice: `Random.Range(0.85f, 1.15f)` pitch multiplier, and another post uses 1 ± 0.1: [Unity discussions, footstep randomize pitch](https://discussions.unity.com/t/foot-step-audio-randomize-pitch/26725) (search summary). Conversion: 0.9 to 1.1 is about -182 to +165 cents; 0.85 to 1.15 is about -281 to +242 cents (calculated: cents = 1200 × log2(ratio)).
- Unreal guidance: if variation is inaudible, "widen pitch to ±15% to confirm it's working, then dial it back": [uhiyama-lab, UE5 footsteps](https://uhiyama-lab.com/en/notes/ue/sound-cue-vs-sound-wave-best-practices/) (search summary).
- RandRobin plugin splits the signal into 3 bands (low, mid, high) and applies random pitch per band, a way to make one sample vary in timbre, not only pitch: [KVR, RandRobin](https://www.kvraudio.com/product/randrobin-by-fanan-team) (search summary).

### Inferences
- For short UI and motion graphics hits, a practical recipe is: 3 to 6 variants per sound type, Shuffle or Random with "avoid last 1 to 2", pitch jitter well under the footstep span (tonal UI sounds go audibly out of key past about ±25 to ±50 cents, while noisy sounds such as whooshes tolerate ±100 to ±200), gain jitter ±1 to 3 dB, and optional start offset of a few ms into the sample. These are heuristics bracketed by the sourced figures above.
- Pitch randomisation on tonal elements (pops tuned to the music's key) should be quantised to scale degrees or kept tiny, otherwise it reads as out of tune rather than varied.
- Timbre variation (filter cutoff, per band pitch, layer swapping) hides repetition better than pitch alone, consistent with the KVR remark that whole sound pitch shift helps less than expected.

### Gaps
- Official Wwise Randomizer and FMOD randomisation docs (units, defaults, recommended ranges) returned 403 or empty pages. From general knowledge, Wwise randomises pitch in cents and volume in dB with independent min and max offsets, and FMOD exposes per instrument pitch and volume randomisation plus a multi instrument playlist with shuffle; neither default nor recommended values could be confirmed this session.
- No GDC talk transcript on the machine gun effect was retrieved; no published "standard" semitone range exists in the sources found.
- No academic perception study on how many repeats it takes before listeners notice an identical sample was found.

## 3. Humanisation: timing jitter, velocity, swing, microtiming

### Takeaway
Producers humanise programmed parts mainly through small timing offsets and velocity variation (Logic: about ±10 ticks timing, ±10 velocity), and through accent patterns rather than pure randomness. But perception research is mixed: several controlled studies found listeners rated quantised versions as good as or better than versions with microtiming, and large deviations (±25 to ±80 ms) reduce ratings. The robotic feel comes more from identical velocity, identical samples and copy pasted patterns than from grid timing alone.

### Cited Findings
- Logic Pro Humanize: about ±10 ticks of random position adds subtle life "without sounding like mistakes": [Splice, humanize your drums](https://splice.com/blog/humanize-your-drums/). Velocity: downbeats slightly higher, offbeats lower; hi hats get the most variation, kick and snare only slight: same source. Splice explicitly separates humanisation from swing.
- Logic MIDI Transform "Humanize" shifts velocity by ±10: [Unison, how to humanize MIDI](https://unison.audio/how-to-humanize-midi/) (search summary).
- Akai MPC humanise: timing as a maximum number of pulses, velocity as a strength percentage: [Akai Pro support](https://support.akaipro.com/en/support/solutions/articles/69000863026-akai-pro-mpc-series-humanizing-your-tracks) (search summary).
- At 960 PPQ, a 20 tick offset is about a 1/48 note of swing: [ReaMCP nudge tool](https://glama.ai/mcp/servers/danielkinahan/ReaMCP/tools/nudge_midi_notes) (search summary).
- Sound On Sound: programmed patterns move from "robot" to "human" through timing and velocity variation: [SOS, Cubase humanise your programmed drums](https://www.soundonsound.com/techniques/cubase-humanise-your-programmed-drums) (search summary; no numbers visible).
- A University of Central Lancashire study found most of 35 listeners could not reliably hear subtle Logic humanise timing changes: [Timing, Forget the Timing (academia.edu)](https://www.academia.edu/49227033/Timing_Forget_the_Timing) (search summary).
- Frühauf, Kopiez and Platz (2013): snare and bass shifted by ±15 and ±25 ms; quantised versions rated highest, larger deviations rated lower, early shifts worse than late shifts of the same size: summarised via [sonicfield library, music on the timing grid](https://labs.sonicfield.org/library/music-on-the-timing-grid-the-influence-of-microtiming-on-the-perceived-groove-qu) (search summary).
- Davies et al. (2013): systematic microtiming in synthesised jazz, funk and samba lowered groove, liking and naturalness ratings, except the simple short long jazz shuffle; stronger effect for experts: [INESC TEC repository](https://repositorio.inesctec.pt/items/38083482-243e-4090-bfa6-735d148ee1ff) (search summary).
- Skaansar, Laeng and Danielsen (2019): bass/drum asynchronies up to ±80 ms increased pupil dilation (mental effort) and reduced tapping stability; listeners mostly preferred on grid grooves except the condition closest to real music: [sonicfield library, microtiming and mental effort](https://sonicfield.org/library/microtiming-and-mental-effort) (search summary).
- Frontiers in Psychology (2016), recorded expert swing and funk: quantised and original microtiming versions rated equally high on groove, supporting neither "microtiming is necessary" nor "exactness is best": [Frontiers in Psychology 2016](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2016.01487/pdf) (search summary).

### Inferences
- ±10 ticks at 960 PPQ and 120 BPM is about ±5 ms (one beat = 500 ms = 960 ticks). That is below the ±15 ms where Frühauf et al. started to see lower ratings, which explains why it reads as "life" rather than "mistake".
- For motion graphics, the research argues against randomising sync points: hits tied to picture should stay frame accurate. Humanisation belongs in the music bed and in the texture layers (velocity, sample choice, accents), plus deliberate late (not early) placement where looseness is wanted, since early deviations were rated worse.
- The "robotic" impression in templates is most likely driven by identical velocity and identical samples (Splice) rather than grid timing, given that listeners often cannot hear small timing offsets.

### Gaps
- Hennig et al. (2011, PLoS ONE) on long range correlated timing fluctuations being preferred over white noise jitter was not retrieved this session, so it is not cited; worth checking because it bears on "random jitter vs correlated drift".
- No sourced numbers for swing percentage norms (for example MPC 50 to 75%) were found in this session.

## 4. Sound that tells a story versus decoration: when not to add sound, hierarchy, sparse vs dense

### Takeaway
Professionals frame restraint as the core skill: "less is more", hierarchy, negative space, and silence as the contrast that makes loud moments land. Sound goes where an element appears, moves, disappears or changes meaning, not on every element, and the cue must fit the moment rather than impress in isolation.

### Cited Findings
- A Trinity College Dublin dissertation applies "less is more" to animation sound design with the principles of simplicity, neutrality, balance, hierarchy and negative space: [TCD SCSS dissertation 2021-015](https://publications.scss.tcd.ie/theses/diss/2021/TCD-SCSS-DISSERTATION-2021-015.pdf) (search summary).
- A tutorial segment titled "Why Less Is More: Avoiding Sound Pack Overload" in "The only 3 sound effects you need to tell any story": [SozAI transcript](https://sozai.app/transcript/three-sound-effects-tell-any-story/index.md) (search summary).
- Visual elements appearing, moving, disappearing or changing are often good places for subtle effects: [NewscastStudio, sound design for news promos](https://www.newscaststudio.com/2022/12/13/sound-design-tips-news-promos/) (search summary; page 403 on fetch).
- "Without quiet, your loud moments have nothing to contrast against": [Violet Recording](https://violetrecording.com/sound-design-for-trailers/) (search summary).
- Three even, low impacts can carry the weight of a braam while reading as controlled: [Morphic](https://morphic.com/resources/sounds/cinematic-sound-effects) (search summary). Implies understatement as a deliberate tone choice.
- Goal is sound that improves motion, emphasis and pacing inside the real piece: [Sonilo whoosh guide](https://sonilo.com/ai-music/whoosh-sound-effect-guide) (search summary).

### Inferences
- A usable rule for an edit: rank events (1 hero, 2 to 4 supporting, the rest unscored). Only the hero gets the full, layered, loud sound; supporting events get small, short sounds; background motion gets nothing or a shared bed. This turns the "identical pop on every element" problem into a hierarchy.
- Silence or a drop to room tone for a few frames to a second before the hero event is the cheapest way to make it feel intentional (Violet Recording's contrast principle).

### Gaps
- No quantitative guidance (for example "sounds per second" density limits) was found in any source.
- No r/MotionDesign or r/editors threads were retrieved, so practitioner phrasing ("too many swooshes") is not quoted.

## 5. Sonic identity: sound specific to the product instead of generic library sound

### Takeaway
Brands that want an ownable sound derive it from their own product: Brabantia built its sonic branding from recordings of its own products, and branding writers point to Apple's product sounds (startup chime, mail "sent" swoosh) as signatures. Product sonification agencies treat startup, shutdown and interaction sounds as the strongest places for a signature.

### Cited Findings
- Brabantia's sonic branding was created using its own products: [Brabantia, the sound of Brabantia](https://www.brabantia.com/int_en/inspiration/the-sound-of-brabantia/) (search summary; process details not described).
- Product sounds split into types, with startup or shutdown sounds the biggest opportunity for a signature brand sound: [Listen, what is sonic branding pt 3](https://wearelisten.com/what-is-sonic-branding-pt-3) (search summary).
- Apple is cited as famous for product sounds such as its startup sound and the mail "sent" swoosh: [Brandingmag interview](https://www.brandingmag.com/?p=71813) (search summary). The same interview says sonic branding can draw on natural, organic, synthetic and hybrid sound.
- Audiobrain built branded product sounds and sonic logos for Toshiba and Whirlpool: [Audiobrain, product sonification](https://audiobrain.com/product-sonification) (search summary).
- Strategic product sounds guide UX and build brand recognition: [WARC opinion](https://www.warc.com/newsandopinion/opinion/how-strategic-product-sounds-guide-a-positive-user-experience-and-build-brand-recognition/5696) (search summary).

### Inferences
- For a product film, the anti generic move is to build the sound palette from the product's world: its real UI sounds (clicks, notifications, haptic ticks), the materials it is made of (aluminium, glass, fabric, paper), and its brand sonic logo if one exists. Transitions can be the product sound processed (stretched, filtered, reversed, pitched) instead of a library whoosh. Music can use a motif or timbre derived from those sounds, so the score and effects feel like one family.
- This also solves the material and size mismatch problem from section 1, because the sounds start from the real object.

### Gaps
- No source describing Apple's actual foley or product recording workflow for ads was found.
- No case study of a motion graphics or launch film that documents building its sound palette from product recordings was retrieved.

## 6. Research and writing on "sameness" in AI music (Suno, Udio) and stock music cliches

### Takeaway
There is now peer reviewed evidence that AI music generators flatten acoustic variety: an AIES 2026 audit of Suno and Lyria 3 found reduced rhythm, timbre and dynamics diversity (Lyria within genre, Suno across genres), and a classifier separated AI from human tracks near perfectly. Stock "corporate" music is criticised for a small, recognisable set of signals, with the ukulele named as the most overused "life is awesome" instrument.

### Cited Findings
- Slendebroek and Metaxa (University of Pennsylvania), "The Algorithmic Flattening of Sound", AIES 2026: 2 systems (Suno, Lyria 3), 4 genres (Afrobeats, K-pop, Dance Pop, Heavy Metal), 100 tracks per system and genre, compared with equal sized human corpora on 72 MIR features. Homogenisation measured as reduced variation in rhythm and timing, timbre and dynamics. Lyria mainly reduces within genre diversity; Suno blurs differences between genres without compressing within genre spread. Neither follows prompts closely, so patterns reflect learned defaults. The two systems do not converge on one sound. A standard classifier separates AI from human tracks "near-perfectly" from MIR features alone: [AAAI OJS, AIES paper 43312](https://ojs.aaai.org/index.php/AIES/article/view/43312).
- "Echoes of Humanity" (arXiv 2025): with random pairs, listeners could not tell Suno songs from human songs (no better than chance), but with highly similar pairs they could: [arXiv 2509.25601](https://arxiv.org/html/2509.25601v1) (search summary).
- A blog summary cautions the flattening study shows measurable tendencies, not proof that every AI song is generic: [Jack Righteous](https://jackrighteous.com/blogs/music-creation-process-guide/why-ai-music-sounds-the-same-keep-your-sound-distinct) (search summary, secondary).
- Boing Boing on a video parodying corporate music: "The most common and egregious isn't-life-just-awesome instrument is the ukulele": [Boing Boing, how to make bland, soulless corporate music (2019)](https://boingboing.net/2019/10/23/how-to-make-bland-soulless-co.html) (search summary; page 403 on fetch, so the other cliches listed in the video are not captured here).
- Stock libraries label large numbers of tracks with near identical descriptors ("uplifting", "motivational", "inspiring", "corporate"), e.g. "naive gentle-strumming ukulele" plus pop rock ensemble with synth and strings: [MonsterONE, ukulele corporate track](https://monsterone.com/stock-music/everyday-uplifting-and-positive-corporate-easy-listening-stock-music-with-ukulele-o309533) (search summary).
- An academic thesis at NOVA University Lisbon studies the "corporate" (empresarial) category on stock music sites and its cliches; findings were not visible in the excerpt: [RUN UNL abstract](https://run.unl.pt/bitstream/10362/30056/1/Abstract_ENIM_Ju_liaDurnad_.pdf) (search summary).

### Inferences
- Stock and AI music read as generic for the same reason: both optimise for the most likely, most licensable answer to a mood keyword, so they converge on a narrow band of tempo, instrumentation and dynamics. The AIES result that systems ignore prompts suggests that prompting alone will not escape the default; the escape is editing to picture, removing default instruments, and adding sounds from the product world.
- Because AI tracks are near perfectly separable on MIR features (rhythm, timbre, dynamics), increasing dynamic range and rhythmic variation over the track (sections that drop out, accents, silence) is a direct counter to the measurable "flatness".

### Gaps
- No study covering Udio specifically was found.
- The exact percentage of diversity reduction and the classifier accuracy figure are in the AIES full PDF, which was not read.
- The Boing Boing source video's full list of corporate cliches (chord progressions, tempo, structure) could not be retrieved; no source with corporate music tempo statistics (for example "most tracks at 120 BPM") was found, so the "~120 BPM four on the floor" pattern in the brief remains unsourced.
