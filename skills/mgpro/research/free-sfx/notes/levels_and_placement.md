# How editors mix premade SFX into videos: levels, placement, density and processing

Source quality note: almost no primary, standards-body or manufacturer source gives SFX-specific numbers. Most numbers below come from sound-library vendors (Epidemic Sound, Krotos, Pro Sound Effects, SFX Engine, Zella), editing blogs and forums. The one manufacturer number found is the DaVinci Resolve Fairlight ducker default. Treat all per-track dB figures as rules of thumb that guides repeat, not standards. Peak meter "dB" figures (dBFS on a Premiere or Resolve meter) and LUFS figures are different measures and must not be mixed up.

## 1. Level targets for voice, music and SFX (dB and LUFS)

### Takeaway
The guides agree on the order (voice loudest, then foreground SFX, then music, ambience lowest), and on peak-meter bands of roughly voice -6 to -15 dBFS, music -18 to -22 dBFS (and -25 to -35 under speech), SFX -10 to -20 dBFS with impacts allowed to spike near -8. Ambient and background SFX sit near -20 to -40. Measured in loudness rather than peaks, one creator keeps SFX about 19 to 20 dB below voice, while another guide says about 6 dB below speech, so "how far below the voice" is not settled.

### Cited Findings
- PremiumBeat (Caleb Ward, 2015, older than the 2018 window but still the most quoted table): dialogue -12 to -15 dB, music -18 to -22 dB, "Sound Effects: -10db to -20db with occasional spikes up to -8db", overall mix -10 to -14 dB, "For safety, no peaks should be above -6db." [PremiumBeat](https://www.premiumbeat.com/blog/how-to-set-audio-levels-for-video/)
- Epidemic Sound (May 2023): overall sound between -24 and -8 dB, dialogue around -18 to -9 dB, music -18 to -22 dB, music under dialogue around -30 to -35 dB, sound effects -10 to -20 dB ("going higher risks distortion"). [Epidemic Sound](https://www.epidemicsound.com/blog/audio-mixing-for-video/)
- Krotos (James Russell, Nov 2025): music about -20 dB; footsteps and environmental SFX around -20 dB; hits, cracks and louder SFX up to -10 dB; real peaks louder than -10 dB. [Krotos](https://krotos.studio/blog/how-to-balance-music-and-sound-effects)
- SFX Engine (2026 blog): ambient sound "typically between -25dB and -40dB"; normalize individual clips to a consistent target such as -12 dB; final master peaking between -6 and -3 dB; dialogue compression at 2:1 to 4:1. [SFX Engine](https://sfxengine.com/blog/common-sound-design-mistakes-in-video-editing)
- Other guides surfaced in search give dialogue -6 to -12 dB, music under dialogue -18 to -25 dB or -20 to -30 dB rising to -12 to -18 dB in gaps without speech, and SFX -12 to -18 dB; one Adobe community post gives a wider SFX span of -10 to -30 dB. [Pixflow](https://pixflow.net/blog/audio-mixing-premiere-pro/); [WeVideo](https://www.wevideo.com/blog/how-to-set-audio-levels); [Adobe Community](https://community.adobe.com/t5/premiere-pro-discussions/master-entire-project-audio-at-once/m-p/12348279/highlight/true)
- Zella (July 2026), on whooshes and impacts at cuts: target "roughly -6 dB relative to speech, meaning about half your voice's volume or quieter"; "If a viewer notices the whoosh consciously, it is too loud." [Zella](https://zellahq.com/blog/sound-design-at-cuts-whoosh-impact-riser/)
- A YouTube explainer creator who measured their own mix (Aug 2026): narration about -20.7 LUFS, SFX clip volume 0.14 (about -17.1 dB) which plays at roughly -39.6 LUFS, so SFX sit about 19 to 20 dB below the voice; BGM volume 0.04. Advice: set SFX volume to a fixed number and keep it, rather than setting it by ear each time. [note.com samune_labo](https://note.com/samune_labo/n/n3727df03a197?hl=en)
- OverseerOS (Oct 2026) refuses to give a single number ("There is no universal dB value for every sound effect") and instead sorts SFX into three level classes: background, supporting, foreground. [OverseerOS](https://www.overseeros.com/blog/youtube-sound-design)
- UI clicks and pops: guides say keep them quiet so they confirm an action without pulling attention from voice or music, and call loud UI pops a common mistake. [media.io](https://www.media.io/audio-effects/quick-sound-effects.html); [Pixabay](https://pixabay.com/blog/posts/free-and-high-quality-sound-effects-for-video-edit-453/)
- Short-form guide: mix effects roughly 10 to 20 percent below voice level as a starting point. [Shortzly](https://shortzly.com/blog/short-form-video-sound-design)
- Broadcast spots anchor on dialogue: one Gearspace poster says for short-form spots "make sure your dialogue is -24 and make everything else sound correct relative to it." [Gearspace](https://gearspace.com/board/post-production-forum/1211989-commercial-advert-mixing-loudness.html)
- Measure music and SFX playing together, not separately: stacking SFX on a music peak is a common cause of running out of headroom near 0 dB. [itch.io devlog via search](https://postgoodism.itch.io/stand-elsewhere/devlog/845058/smoothing-out-the-levels)

### Inferences
- A workable three-tier scheme consistent with all the sources (peak meter, voice-led mix): story SFX (the key click, the reveal hit, the logo impact) peak around -10 to -12 dBFS, at most -8; supporting SFX (whooshes, swipes, pops) peak around -14 to -18 dBFS; ambient or motion texture (hums, room tone, small rustles) around -22 to -35 dBFS. Music sits at -18 to -22 dBFS alone and drops under voice.
- In a music-only product ad with no voice, the music becomes the anchor. Story SFX should still read clearly above the bed, which points to peaks a few dB above the music's typical level plus a brief duck (section 2).
- The -6 dB (Zella) and -19 to -20 dB (note.com) "below voice" figures are not directly comparable: the note.com number is integrated loudness of a short sound, which reads lower than its peak level. Both agree the transition SFX should be clearly under the voice.

### Gaps
- No source gave separate peak targets per SFX type (click vs whoosh vs impact vs riser) beyond Krotos's footsteps -20 vs hits -10. The per-tier numbers in Inferences are a synthesis, not a quoted rule.
- No r/editors or r/audiopost thread with SFX-specific numbers turned up in search.

## 2. Making important SFX cut through without harshness (EQ, ducking, phone and laptop speakers)

### Takeaway
Editors make the key SFX read by briefly ducking the music (2 to 6 dB is the common range; Resolve's ducker default is 2.7 dB), high-passing SFX around 80 to 100 Hz so they do not muddy the voice and music, and giving low-heavy hits upper harmonics so they survive small speakers. Boosting 2 to 5 kHz helps presence but guides warn it turns harsh on phones, so boost there carefully.

### Cited Findings
- DaVinci Resolve Fairlight Ducker defaults: lookahead 15 ms, rise time 10 ms, duck amount 2.7 dB, hold 150 ms, recovery 750 ms; the Resolve 21 manual says 2 to 5 dB works "best most of the time." [DaVinci Resolve Club](https://davinciresolveclub.com/davinci-resolve-audio-ducking/)
- Voice-over-music ducking guides cluster around 6 dB: one gives 6 to 10 dB reduction with 30 to 60 ms attack and 300 to 500 ms release; another 6 dB with about 20 ms attack, 200 ms hold, 400 to 800 ms release; a Gearspace mixer keeps automatic ducking to "usually 3 dB max". Too-short release causes audible pumping. [Audio Tool Kit](https://audio-tool-kit.com/blog/audio-ducking); [Gearspace](https://gearspace.com/board/post-production-forum/1198509-ducking-music-under-dialog-your-thoughts-philosophy.html); [Boris FX](https://borisfx.com/blog/davinci-resolve-audio-ducking-tutorial-in-5-steps/)
- OverseerOS: music should be lowered "briefly" around important SFX; reduce frequencies that compete with the voice. [OverseerOS](https://www.overseeros.com/blog/youtube-sound-design)
- Pro Sound Effects: adjust clip gain first; lower a detailed foreground sound until it supports the scene rather than dominating it. [Pro Sound Effects](https://blog.prosoundeffects.com/how-to-make-sound-effects-sit-better-in-a-mix)
- SFX Engine: high-pass filter "around 80-100Hz" for dialogue and most sound effects; voice and music conflict in the 200 to 500 Hz range; keep "no more than 3-5 key audio layers playing simultaneously." [SFX Engine](https://sfxengine.com/blog/common-sound-design-mistakes-in-video-editing)
- Small speakers: saturation that adds harmonics in roughly 150 to 500 Hz lets bass read on phones; one source says 300 Hz to 5 kHz "is where the story of the mix lives on phone speakers"; presence 2 to 5 kHz: "Be conservative with boosts"; another says phones hype 2 to 6 kHz and harshness "becomes painful fast"; adding "click in the 5KHz range to a kick adds presence and clarity ... even when you can't feel or hear the low frequencies." [Mastrng Substack](https://mastrng.substack.com/p/mixing-for-phone-speakers); [Sonarworks](https://www.sonarworks.com/blog/learn/make-your-mix-sound-great-on-small-speakers); [Audio Forge Pro](https://audioforgepro.com/blog/mobile-audio-optimization-guide); [Johnny Copland](https://johnnycopland.com/how-to-mix-bass-for-smartphone-speakers/)
- Sub-heavy effects around 20 Hz (explosions) are the hardest to reproduce. [Wikipedia: Low-frequency effects](https://en.wikipedia.org/wiki/Low-frequency_effects)
- Test on headphones, phones, small speakers and car audio; OverseerOS adds low-volume, mono, laptop and TV checks, an eyes-closed one-minute listen, and a "remove 50%" test (mute half the decorative effects and compare). [PitchDrift](https://pitchdrift-productions.com/sound-design-tips-for-motion-graphics/); [OverseerOS](https://www.overseeros.com/blog/youtube-sound-design)

### Inferences
- For a key SFX over music, a 2 to 6 dB duck lasting about the length of the SFX (fast rise near 10 ms, recovery 300 to 750 ms) matches the ducker numbers found; keyframing it by hand gives the same result.
- A sub-heavy impact on its own vanishes on phones. Layering a short transient or click with content in the 1 to 5 kHz band on top of the boom keeps the hit audible (the "kick click" logic applied to SFX).

### Gaps
- No source gave a dB duck specifically for music under a single SFX hit (all numbers are from voice-over ducking or the generic Resolve default).
- No source gave measured EQ moves for UI clicks or whooshes.

## 3. Placement and timing (frames, whooshes, impacts, J and L cuts)

### Takeaway
Impacts and clicks land on the exact frame of the action (even 50 ms early reads as sloppy). Whooshes start before the cut and peak on it, with lead times of 2 to 6 frames quoted. Risers build about one second before the moment and stop dead when it lands. Pre-lapping the next scene's sound before the picture changes is a standard transition device.

### Cited Findings
- Zella: impact on the cut itself, "even 50 ms early reads as sloppy"; whoosh starts just before the change, peaks at the change, tapers just after; for a transition of about half a second the whoosh runs roughly 400 to 500 ms; riser begins about one second before the key claim and stops abruptly when the moment lands; keep effects short while music is ducked under voice. [Zella](https://zellahq.com/blog/sound-design-at-cuts-whoosh-impact-riser/)
- Lead-time advice varies: about two to three frames before the cut so the audio drives the transition, or four to six frames early so the swell peaks as the new shot lands; check the waveform peak against the cut frame; a long-tailed whoosh running past a hard cut blurs it, a tail-less swipe suits hard cuts. [Morphic](https://morphic.com/resources/sounds/whoosh-sound-effect); [Morphic transitions](https://morphic.com/resources/sounds/transition-sound-effects) (vendor pages, rule of thumb)
- SFX Engine: nudge clips "one frame at a time"; "Even a delay of a few frames can be perceived by the viewer." [SFX Engine](https://sfxengine.com/blog/common-sound-design-mistakes-in-video-editing)
- A YouTube creator plays the diagram sound about 0.3 seconds after the diagram appears, once per diagram, not per item. [note.com samune_labo](https://note.com/samune_labo/n/n3727df03a197?hl=en)
- PitchDrift: introduce the next scene's sound early in transitions; align sounds with visual beats "but avoid cutting on every beat." [PitchDrift](https://pitchdrift-productions.com/sound-design-tips-for-motion-graphics/)
- A pop that lines up with music or motion "feels intentional." [add.app](https://add.app/sound-effects/pop-sound-effect/)
- Mismatched energy between a sound and its transition is worse than no sound. [Zella](https://zellahq.com/blog/sound-design-at-cuts-whoosh-impact-riser/)

### Inferences
- At 30 fps one frame is 33 ms, so Zella's 50 ms tolerance means impacts and clicks must be within about one frame. At 24 fps, 2 to 6 frames of whoosh lead is 83 to 250 ms, consistent with a 400 to 500 ms whoosh peaking near its middle.
- Align the sample's transient or peak, not the clip start, to the action frame. Many library files have silence or a slow onset before the peak.
- Snapping key hits to the music's beat grid where the picture allows it makes the SFX feel part of the score.

### Gaps
- No source gave frame-level rules for J and L cuts applied to SFX specifically, beyond "introduce the next scene's sound early."
- Frame lead numbers come from vendor pages; no editor survey or primary source confirmed them.

## 4. Variation, fades, panning and reverb (avoiding the machine-gun effect, gluing SFX in)

### Takeaway
Repeated identical samples sound mechanical; the fix is several alternate files with no immediate repeats, plus small random changes in pitch (a few percent) and level per hit. Add short fades to nearly every sound, pan SFX to follow on-screen motion while keeping voice centred, and keep quick UI sounds mostly dry, using reverb mainly to push sounds back or match a space.

### Cited Findings
- Game-audio practice: 4 to 8 variations per sound type, random selection without immediate repeats, subtle randomized pitch ("a few percent") and volume per play. [Bugnet](https://bugnet.io/blog/how-to-implement-footstep-variation-to-avoid-repetition)
- Pitch variation per play adds natural variation; a random pitch envelope within one sample reduces the machine-gun effect more than a plain whole-sound shift; other parameters to vary: volume, transient attack, filtering, panning. [Game Developer](https://gamedeveloper.com/audio/the-power-of-pitch-shifting); [VI-Control](https://vi-control.net/community/threads/if-you-had-only-one-snare-sample.138821/)
- Repeated use of a single sample gives a mechanical result, called the "machine-gun effect." [DAFx 2021 paper](https://acris.aalto.fi/ws/portalfiles/portal/67780224/DAFx20in21_paper_22.pdf)
- For repeated video SFX, vary sample, pitch, timing, stereo position, level and duration; "same whoosh repeated constantly" is listed as a mistake. [OverseerOS](https://www.overseeros.com/blog/youtube-sound-design)
- Using an untouched stock whoosh straight from a library is flagged as an amateur giveaway. [SFX Engine](https://sfxengine.com/blog/common-sound-design-mistakes-in-video-editing)
- Abrupt starts and stops are a strong amateur giveaway; short fades on nearly every sound. [SFX Engine tips](https://sfxengine.com/blog/sound-design-tips-for-video-editors); fades prevent clicks and pops. [OverseerOS](https://www.overseeros.com/blog/youtube-sound-design)
- Keep UI tails short (under 1 s) since repeated pops with long tails clutter quickly; most UI and social pops work better dry; heavy reverb on quick UI sounds increases masking; UI sounds mono-centred or narrow stereo; keep a family (success, error) in the same pitch range and decay length. [Pixabay](https://pixabay.com/blog/posts/free-and-high-quality-sound-effects-for-video-edit-453/); [media.io](https://www.media.io/audio-effects/quick-sound-effects.html)
- Panning: pan directional sounds (footsteps left to right, an off-screen phone); flybys and whooshes often have panning built in and need less manual panning; keep narration centred and pan SFX with on-screen movement. [Pro Sound Effects](https://blog.prosoundeffects.com/how-to-make-sound-effects-sit-better-in-a-mix); [OverseerOS](https://www.overseeros.com/blog/youtube-sound-design)
- Room matching: pick a recording whose perspective already fits; to push a sound back, cut highs, add reverb and lower the dry signal; use a room impulse reverb indoors; add Doppler to moving sounds. [Pro Sound Effects](https://blog.prosoundeffects.com/how-to-make-sound-effects-sit-better-in-a-mix)
- Ambience or room tone acts as glue between shots; "No ambience" and "Ambience too loud" both appear on the mistakes list. [Pixabay](https://pixabay.com/blog/posts/free-and-high-quality-sound-effects-for-video-edit-453/); [OverseerOS](https://www.overseeros.com/blog/youtube-sound-design)

### Inferences
- "A few percent" of pitch is about 0.5 to 1 semitone (1 semitone is about 5.9 percent). Larger shifts (2 to 3 semitones) change the sound's character and are better used to make a deliberately different variant, for example a rising pitch for successive UI pops in a sequence.
- For motion graphics, a short shared reverb (or the music's own reverb character) at a low send can glue whooshes and impacts to the score, while clicks stay dry and close. This is an inference; no source gave send levels or decay times.

### Gaps
- No video-editing source gave numeric fade lengths in ms or pitch ranges in semitones; the game-audio "few percent" is the only quantified figure.
- No numbers for reverb send level or decay time for SFX glue.

## 5. Density: SFX per minute and spacing

### Takeaway
There is no standard count. Quoted figures: 1 to 2 SFX per minute for restrained styles, 4 to 6 per minute for energetic niches, a measured median of 6.5 per minute in YouTube explainers, and a warning that 20 to 30 per minute stops registering. Spacing matters more than count: the gap between sounds should be longer than the sound itself, and not every cut gets a whoosh.

### Cited Findings
- YouTube SFX guide: 4 to 6 sounds per minute is normal for energetic niches (fitness, finance); 1 to 2 per minute maximum for restrained styles like vlogs. [YouTubeSFX](https://youtubesfx.com/guides/sound-effects-for-every-type-of-youtube-video/)
- Creator self-measurement over six 10 to 12 minute explainers (418 plays): median 6.5 SFX per minute, range 4.5 to 7.9; median gap 9.2 s, tightest gap 2.2 s, sound length 1.25 s, zero overlaps; rule: shortest gap longer than the sound's length; at 20 or 30 per minute "the viewer's brain stops processing them as signals"; use only three spot types: diagram appears, topic shift (4 to 6 per video), conclusion or key number (1 to 2 per video). [note.com samune_labo](https://note.com/samune_labo/n/n3727df03a197?hl=en)
- OverseerOS: SFX go at meaningful audio events, "not on a timer"; about 15 visual changes per minute do not require 15 whooshes; contrasts a 20 second sequence with 6 whooshes, 4 impacts and 3 clicks against one UI click and one impact at the reveal. [OverseerOS](https://www.overseeros.com/blog/youtube-sound-design)
- Zella: use sounds only on meaningful cuts (section changes, punch-ins, reveals); in a video that cuts every 4 to 5 seconds, sounding every join is excessive and makes the mix "feel like a percussion track." [Zella](https://zellahq.com/blog/sound-design-at-cuts-whoosh-impact-riser/)
- Short-form: one effect per transition, two as the ceiling in most short clips. [Shortzly](https://shortzly.com/blog/short-form-video-sound-design)
- No more than 3 to 5 key audio layers playing at once. [SFX Engine](https://sfxengine.com/blog/common-sound-design-mistakes-in-video-editing)
- YouTube editing discussion: beginners overuse transitions and effects; use them sparingly so they do not become grating. [Recapio digest](https://recapio.com/digest/how-to-edit-killer-youtube-videos-by-itsproger)

### Inferences
- Polished product ads and motion graphics are a different case from talking-head YouTube: every on-screen action is designed, so a 30 second ad can carry many sounds, but they should be layered in tiers (a few loud story hits, many quiet texture sounds), not many equally loud hits.

### Gaps
- No source measured SFX density in polished product ads (Apple-style launch films). No study links SFX density to retention.

## 6. Final loudness for web and social delivery

### Takeaway
The most repeated web target is -14 LUFS integrated with a true peak ceiling of -1 dBTP (some say -1 to -1.5), but TikTok and Instagram publish no official number, and guides range from -16 to as loud as -10 to -12 LUFS. Platforms turn loud audio down but do not reliably turn quiet audio up, so a too-quiet master stays quiet. Broadcast is -24 LKFS (US, ATSC A/85) or -23 LUFS (EBU R128).

### Cited Findings
- Streaming target "-14 LUFS"; master limiter ceiling "-1dBTP to -1.5dBTP." [SFX Engine](https://sfxengine.com/blog/common-sound-design-mistakes-in-video-editing)
- TikTok and Instagram Reels listed at -14 LUFS, -1.0 dBTP; TikTok has not published an official loudness standard; -16 is "a conservative production convention"; one guide suggests -10 to -12 LUFS (a single -11 LUFS export for both). Loud audio is turned down; quiet audio is not pushed up. [APU Software](https://apu.software/tiktok-instagram-reels-loudness/); [Cutscore](https://cutscore.io/blog/loudness-for-instagram-reels); [Audio Gear Hub](https://audiogearhub.com/mix-audio-for-social-media/); [Magic Master](https://magicmaster.pro/blog/tiktok-mastering-loudness)
- OverseerOS rejects the claim that YouTube "requires exactly -14 LUFS"; recommends AAC-LC, 48 kHz, 384 kbps stereo upload audio. [OverseerOS](https://www.overseeros.com/blog/youtube-sound-design)
- Krotos: music streaming about -14 LUFS, TV -23 LUFS, film -27 LUFS in general standards; Sundance 2023 spec -24 LUFS integrated (conflicts with the -27 figure). [Krotos](https://krotos.studio/blog/how-to-balance-music-and-sound-effects)
- Broadcast: ATSC A/85 (CALM Act) -24 LKFS within about 2 LU; EBU R128 -23 LUFS within 0.5 LU (some quote 1 LU); true peak -2 dBFS commonly used; normalization does not reward over-compression. [Pro Audio Files](https://theproaudiofiles.com/introduction-broadcast-loudness-standards/); [Gearspace](https://gearspace.com/board/post-production-forum/1211989-commercial-advert-mixing-loudness.html)

### Inferences
- Mastering to about -14 LUFS integrated with a -1 dBTP limiter is a safe single target for YouTube, Reels and TikTok. Since loud SFX peaks drive the limiter, a mix with overly hot SFX loses voice and music loudness after normalization; keeping SFX peaks under the voice protects the overall level.

### Gaps
- No official TikTok or Instagram loudness documentation was found; all social figures are from vendor blogs.

## 7. Common amateur mistakes

### Takeaway
The recurring list: SFX too loud (noticed consciously), a whoosh on every cut, the same sample repeated, untouched stock sounds, abrupt starts with no fade, mistimed hits, effects masking words, wrong room or perspective, everything "cinematic", too many layers, and mixing only on headphones or in solo.

### Cited Findings
- OverseerOS list of 12: sound on every cut; effects covering important words; same whoosh repeated constantly; music and SFX fighting the voice; everything cinematic; no ambience; ambience too loud; no dynamic range; mixing tracks in solo; mixing only on headphones; using mastering to fix the mix; adding effects because the video feels boring. [OverseerOS](https://www.overseeros.com/blog/youtube-sound-design)
- SFX Engine list: ignoring levels and dynamic range (normalizing a whisper and an explosion to the same level makes "a flat wall of noise"); generic or untouched stock SFX; timing and sync errors of a few frames; excessive layering; neglecting ambience and silence; frequency clashes; not checking other playback systems. [SFX Engine](https://sfxengine.com/blog/common-sound-design-mistakes-in-video-editing)
- Whoosh noticed consciously means too loud; mismatched energy is worse than silence; every cut sounded becomes a percussion track. [Zella](https://zellahq.com/blog/sound-design-at-cuts-whoosh-impact-riser/)
- Loud UI pops and long UI tails; stacking several bright clicks on the same frame; long risers for tiny UI moves. [media.io](https://www.media.io/audio-effects/quick-sound-effects.html)
- Epidemic Sound: uneven levels between clips; music too high; cutting audio without a fade. [Epidemic Sound](https://www.epidemicsound.com/blog/audio-mixing-for-video/)
- Mismatched room: sounds from the wrong perspective or dry sounds in a reverberant scene; fix with perspective-matched recordings and room reverb. [Pro Sound Effects](https://blog.prosoundeffects.com/how-to-make-sound-effects-sit-better-in-a-mix)

### Inferences
- "Too quiet" is under-reported: the only signal is that story SFX inaudible on phone speakers lose their point, which ties back to section 2 (harmonics, brief duck).

### Gaps
- Few sources describe the "too quiet" failure explicitly or give a lower bound for story SFX.
