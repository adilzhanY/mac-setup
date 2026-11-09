# How human editors and studios use premade sound effects in product, SaaS and motion graphics videos: case studies and measurements

Scope: tutorials, breakdowns and studio write-ups (2019 to 2026), two projects where the sound designer published separated stems (exact ground truth), and my own measurement of 10 real product and SaaS videos downloaded with yt-dlp (audio only plus a 144p picture for cut and motion checks, private analysis).

Files: everything is in `/games/mgpro/sfx-casestudies` (45 MB): `audio/` (10 YouTube audio tracks), `video/` (144p pictures), `stems/` (Contra and HeroUI stem videos), `subs/` (tutorial transcripts), `scripts/` (all analysis code, runs with `/home/wopler/.local/share/mgpro/.venv/bin/python`), `analysis/` (per video candidate tables, spectrogram images, contact sheet). Disk after the work: / at 4.9 GB free, /games at 15 GB free.

Method in one paragraph. For the two stem projects, each SFX stem is measured on its own: audible segments (envelope within 35 dB of the stem peak, gaps under 150 ms merged), onsets (librosa), and level against the music stem in the same time span after fitting each stem's gain to the full mix (non negative least squares on power spectrograms). For the 10 mixed YouTube videos there is no stem, so I read 20 s spectrogram strips with numbered onsets and a level curve, checked the picture with a 1 fps contact sheet where needed, and measured each event I could identify: peak 50 ms RMS level inside the event minus the "bed" (median 50 ms level over the 1.5 s before it). Two automatic separators were tried and failed validation against the stems, so they were not used for counts: a "does this onset repeat one bar earlier or later" music detector (could not tell Contra's SFX from its music at any threshold) and a short transient click detector (of 130 clicks it found in the Contra mix, 49 were music only and only about 41 were SFX only). So the per video lists below are lower bounds: clearly designed events that stand out from music and voice. Quiet clicks tucked under music or voice cannot be confirmed from a mix.

## Tutorials, breakdowns and agency write-ups: what editors say they do

### Takeaway
Practitioners describe a small set of SFX families (3 to 4: UI or digital, whooshes and transitions, impacts and risers, sometimes one mechanical or foley thread), layered in transient, body and texture, synced to the frame, high passed and ducked under voice. Every source that speaks about frequency says to use fewer, chosen accents ("if you try to make every moment special none of them will be special"). The only concrete level guide found puts SFX at -10 to -30 dB on the meter, music at -20 to -30 dB and dialogue near -12 dB.

### Cited Findings
- Contra launch video re-sound (Tomas Havranek, sound and mix, August 2025): typewriter sounds run "throughout as a consistent sonic thread"; whooshes mark each transition with intensity that "varies with the motion, from subtle to more noticeable"; digital and UI sounds keep it modern "without going full sci-fi". Published as full mix plus separate music, transitions, mechanical SFX and digital SFX stems. Tools: Ableton Live and Pro Tools. [Contra project page](https://contra.com/p/WPMQbb6O-sound-design-exploration-contra)
- HeroUI launch video (Tomas Havranek, sound design and mix credited to NewZone Audio, posted 11 October 2025): mechanical, tonal and UI sounds combined to stay "warm and approachable rather than overly digital"; SFX published as three soloed families: Interface + UI, Whooshes + Transitions, Impacts + Risers. [Contra project page](https://contra.com/p/ks662MrZ-hero-ui-launch-video-sound-design-exploration)
- Joe Vanz, "Motion Graphics Sound Design CRASH COURSE" (DaVinci Resolve): three layer "cake" (layer 1 transient: impact, click or pop; layer 2 body that mimics the movement; layer 3 texture); subframe nudging to hit "the exact peak of your motion graphic"; pan the sound with the graphic's screen movement; cut 200 to 400 Hz on whooshes so they do not muddy voice and music, but "you don't have to do this with every single whoosh"; reverb at about 15% wet ("you don't want to hear the reverb, you just want to notice when it's not there"); time stretch SFX with warp markers to match ease curves; sidechain the music to the SFX track so it ducks when an effect fires. Workflow: spot (markers on hits and turns), layer, sync, EQ, duck. [YouTube GovWYxWNS54](https://www.youtube.com/watch?v=GovWYxWNS54)
- Herman Huang, "3 Sound Design Secrets That Feel Like CHEATING": a single whoosh fits a small movement, a big one needs whooshes layered across frequencies; "commit to a style instead of mixing random sounds" (gritty bass hits do not belong in corporate video); enter a track with a reversed section of the song as a riser, exit with reverb on the last beat, and layer risers, swells, suckbacks and impacts over those music edits. [YouTube tzfzkTAQsnE](https://www.youtube.com/watch?v=tzfzkTAQsnE)
- Film Editing Pro, "How to SOUND DESIGN a Video": first pass problems were the same keyboard sound for every keystroke and the same pen sound for every stroke; fix was to cut a 10 s typing recording into single keystrokes and use each once. Whooshes on a character's quick movements, a reverberating hit on a box drop, a reverse cymbal ("suckback") plus boom at the climax. "Not every moment needs to be accented and not every accented moment needs to be maximum intensity ... if you try to make every moment special none of them will be special." Meter guide: nothing peaks, dialogue around -12 dB, "sound effects will be anywhere from -10 dB to -30 dB", "the score ... tends to sit around -20 to -30 dB". [YouTube Wcxw3BPSt3A](https://www.youtube.com/watch?v=Wcxw3BPSt3A)
- Echoic Audio (iZotope series, November 2019), dual screen phone film "Right: A Reverse Film": reversed church bells, reversed hits, sweeps and rumbles for builds and transitions; music box as the musical seed; online mixes aimed at about -14 to -11 LUFS, -7 to -9 LUFS judged "too aggressive". [iZotope, Echoic part 2](https://www.izotope.com/community/blog/echoic-audio-part-2)
- Echoic Audio on a short film score: "many sounds are heard only once", "every small decision is calculated", less is often more. [iZotope, Echoic part 3](https://www.izotope.com/community/blog/echoic-audio-part-3)
- School of Motion "Making Giants" part 10 combines VO, music and SFX into an "audio arc" and ships the SFX premixed, but the public page gives no counts or levels. [School of Motion](https://www.schoolofmotion.com/tutorials/making-giants-sound-design)
- Vendor and generator pages (weaker sources, product marketing): keep clicks "for actions that matter" because "every click competes with the voiceover", pull cue level down under narration, one click on the frame a new feature appears, reserve a chime for a new panel ([Morphic demo sounds](https://morphic.com/resources/sounds/demo-sound-effects)); "silent product interactions that feel cheap" and "mismatched generic clicks not tied to the product" listed as pitfalls, music must not overpower feature narration ([IRPR Sound, product videos](https://sounddesign.irpr.agency/applications/product-videos/)); "fewer well-placed effects read as more professional than many effects scattered throughout a project" ([Envato item page via freevisuals](https://www.freevisuals.net/item/woosh-premium-sound-effect)).
- A Supademo study of 1,000 interactive demos found 54% of the top completing demos run an AI voiceover over the clicks; it says nothing about SFX. [YouTube 1WXxcFaEEVE](https://www.youtube.com/watch?v=1WXxcFaEEVE)
- Jitter (browser motion design tool) added audio tracks in mid 2024 so SFX, music and VO can be layered and aligned with waveforms inside the tool. [AlternativeTo news](https://alternativeto.net/news/2024/7/motion-design-tool-jitter-adds-audio-support-to-enrich-animations-with-sound-effects)

### Inferences
- The consistent working model across sources: pick a palette of 3 to 4 families that match the brand, spot the key moments, layer and sync those, and leave the rest to the music. "Family" is a style decision made once per film, not a per event choice.
- Variation inside a family (each keystroke different, no repeated hit) is treated as a mark of quality, which is the opposite of a sample triggered by every event.
- No tutorial found gives SFX per minute. The measurements below fill that gap.

### Gaps
- No studio blog from Rotato, Pitch, Arcade, Screen Studio users or Motion Array was found that describes their own SFX counts or levels. Rotato searches returned nothing relevant; Motion Array returned only product pages.
- No Reddit thread with concrete numbers was found through search. Reddit itself was not fetched.
- Several YouTube transcripts hit HTTP 429 rate limits; the ones quoted above are the ones that downloaded.

## Ground truth from published stems: what professional SFX layers actually contain

### Takeaway
In both stem projects the SFX are not sparse accents laid on top of the music. They are three continuous families that are audible 28 to 61% of the running time, sit mostly 3 to 14 dB under the music, and poke above it only where the music leaves a gap. Their placement is not tied to visual motion: whooshes are audible near motion peaks no more often than at random times.

### Cited Findings
All numbers are my measurement of the stem videos on the two Contra pages ([Contra project](https://contra.com/p/WPMQbb6O-sound-design-exploration-contra), [HeroUI project](https://contra.com/p/ks662MrZ-hero-ui-launch-video-sound-design-exploration)); code in `/games/mgpro/sfx-casestudies/scripts/stems.py`, `stems2.py`, `heroui.py`, `motion.py`.

Contra launch video (30 s, full mix -14.4 LUFS integrated):

| Stem | Audible share of film | Segments (gaps under 150 ms merged) | Onsets | Onsets per min | Level vs music, same span (median RMS) |
|---|---|---|---|---|---|
| Transitions (whooshes, swells) | 61% | 8 | 38 | 76 | -2.6 dB (range -5.5 to -0.2) |
| Mechanical (typewriter) | 42% | 9 | 62 | 124 | -7.5 dB (range -18.4 to +17.3) |
| Digital (UI tones, blips) | 28% | 10 | 21 | 42 | -13.8 dB (range -31.1 to +21.5) |
| Music | 56% | 35 | 119 | 238 | reference |

- Gains fitted to the mix: music -6.9 dB, transitions -4.2 dB, mechanical -3.3 dB, digital -4.0 dB relative to the stem files (power fit residual -8.9 dB under the mix, so treat levels as accurate to a few dB). Mean power over the film relative to music: transitions -3.3 dB, mechanical -7.1 dB, digital -11.9 dB.
- Sound by sound (from spectrograms): the "transitions" stem is not a string of discrete whooshes but long low swells (centroid 370 to 710 Hz, mostly below 512 Hz) that run from 2.2 s to 12.1 s almost unbroken and again from 16.9 s to 26.1 s; the "mechanical" stem is typewriter key runs (3.4 to 10.5 s holds 31 onsets) plus one low impact at 21.6 s; the "digital" stem is about 10 short tonal gestures (pitched blips, a chime at 8.4 s, a zap at 12.4 s, a drone from 14.4 s).
- The two digital events that sit +18 and +21 dB over the music (3.7 s and 12.4 s) and the mechanical hit at +17 dB (12.4 s) fall in the silent gaps between the music's percussive hits. Everywhere else the SFX are under the music.
- The music stops completely at 23.8 to 26.2 s and the film briefly runs on SFX alone (transition tail and a high texture), then the music returns for the end card.
- Picture: only 6 hard cuts in 30 s (4.5, 7.4, 9.8, 13.2, 24.1, 26.5 s; ffmpeg scene score over 0.25), because the motion is continuous. Transitions stem audible within 0.3 s of 82% of the 34 motion peaks (frame difference peaks), against 75% for random times; mechanical 71% vs 64% chance; digital 44% vs 45% chance.

HeroUI launch video (39 s analysed of 41.6 s, main mix -12.8 LUFS; no music stem was published):

| Stem | Audible share | Segments | Onsets | Onsets per min | Stem loudness |
|---|---|---|---|---|---|
| Interface + UI | 42% | 12 | 41 | 63 | -16.2 LUFS |
| Whooshes + Transitions | 50% | 13 | 57 | 88 | -15.9 LUFS |
| Impacts + Risers | 46% | 5 | 43 | 66 | -12.2 LUFS |
| Main mix | 94% | 3 | 120 | 185 | -12.8 LUFS |

- Whooshes are 0.9 to 4 s noise swells, roughly one every 3 s (13 in 39 s). Impacts and risers come as 5 long gestures: a riser 2.8 to 5.0 s that cuts off, an impact cluster at 8.3 to 9.6 s, a riser 11.5 to 13.0 s, a sustained low layer 22.1 to 25.3 s, and a long build 26.6 to 35.5 s with a hit at 30.6 s and a new layer at 33.8 s. UI sounds are tonal blips with harmonic partials, single (16.9 s, 17.9 s) or in rapid patterns (21.5 to 24 s holds a ticking sequence of about 20 short hits).
- Picture: only 10 hard cuts (8 of them in the first 5 s). Whoosh stem audible within 0.3 s of 70% of 44 motion peaks against 67% for random times; UI 59% vs 58%; impacts 59% vs 57%. Correlation between the whoosh level and the frame difference energy: -0.04 (Contra transitions: 0.12).
- The impacts and risers stem is about as loud as the whole mix (-12.2 vs -12.8 LUFS), which suggests the stems were exported at mix level and that impacts and risers are the loudest SFX family. Whooshes and UI are about 3.5 dB quieter than the mix as a whole. This is an inference from loudness, not a fitted gain.

### Inferences
- "How many SFX" depends on what you count. Counted as placed gestures, the two pro films have 54 (Contra) and 46 (HeroUI) per minute; counted as onsets, 242 and 217 per minute. Most onsets come from runs inside one gesture (typing, ticking UI patterns, multi hit impacts).
- The SFX families behave like a second, quieter instrument section: long swells and textures that fill the space between music hits, not a one to one "motion gets a whoosh" mapping. At the motion peak level used here they are statistically indistinguishable from random placement. The frame difference measure is crude (it sees camera moves and big wipes best, not small UI changes), so this says "not on every big move", not "unrelated to the picture".
- The loud exceptions are deliberate: SFX jump 15 to 21 dB above the music only inside music gaps, and the music drops out entirely once (Contra) so the SFX carry a moment alone.

### Gaps
- No HeroUI music stem, so SFX level relative to music could not be computed for HeroUI.
- The stems are from one sound designer (Havranek). Two projects are not a population.
- Contra video audio is AAC from a web player; codec and the imperfect gain fit limit level accuracy to a few dB.

## Ten real product and SaaS videos measured from the mix

### Takeaway
In finished brand and SaaS videos the identifiable, separately designed SFX are few: 0 to 8 per minute that clearly stand out. Most are structural (a riser into a drop, an impact on a section start or the logo, a whoosh on the switch from live action to UI, silence or a hard cut before a hit). Audible UI clicks were not confirmed in any of the 10 mixes; where the picture shows UI, the music's own plucks or beats carry the clicks. Accents peak 7 to 13 dB over the bed in the middle of a film, and up to 17 to 25 dB only where they follow a quiet intro or a silence.

### Cited Findings
Measured by me; per video candidate tables and spectrograms in `/games/mgpro/sfx-casestudies/analysis/`, event levels from `scripts/measure.py`. "Over bed" is the event's peak 50 ms level minus the median 50 ms level in the 1.5 s before it. Analysis covers the first 60 s of each video. Videos: [Superhuman](https://www.youtube.com/watch?v=4XKq7qGnJus), [Linear Releases](https://www.youtube.com/watch?v=6dIwFoQ0eVg), [Arc 1.0](https://www.youtube.com/watch?v=n5Vwrj1gEWs), [That's Framer](https://www.youtube.com/watch?v=8AHPXm9Y6mI), [Screen Studio](https://www.youtube.com/watch?v=7AnqbpeJoHc), [Introducing Supademo](https://www.youtube.com/watch?v=uP8M-RW4Q5A), [Zelios for Teamble](https://www.youtube.com/watch?v=xNUx-rMGvvw), [What a Story, Infinity](https://www.youtube.com/watch?v=ZK-rNEhJIDs), [Motion Swell UI animation](https://www.youtube.com/watch?v=uwAnvbtIjrg), [Raycast Pro preview](https://www.youtube.com/watch?v=u6iro1jHujs).

Summary:

| Video (upload) | Length analysed | Sound bed | Identified designed SFX | Per min | Clicks audible? |
|---|---|---|---|---|---|
| Superhuman, Introducing Superhuman (2025-10) | 60 s | four on the floor music, no VO | 9 | 9 | none confirmed |
| Linear, Introducing Linear Releases (2026-04) | 30 s | quiet tonal score, film median -26 dBFS | 4 (may be part of score) | 8 | no |
| The Browser Company, Arc 1.0 (2023-07) | 34 s | dense sidechained music | 1 (falling tonal sweep, 19.3 s) | 2 | no |
| Framer, That's Framer (2025-04) | 37.5 s | VO plus music | 4 | 6 | one rapid tick burst |
| Screen Studio, Beautiful Screen Recording (2026-02) | 45 s | live action with VO and keyboard foley, then plucked music | 5 (2 uncertain) | 7 | 2 possible clicks, uncertain |
| Supademo, Introducing Supademo (2024-09) | 60 of 115 s | VO plus very loud music (median -5.6 dBFS) | 2 | 2 | not readable |
| Zelios for Teamble (agency explainer, 2025-02) | 60 of 98 s | music intro, then VO plus music | 4 | 4 | not readable |
| What a Story, Infinity (agency, 2022-03) | 19 s | near continuous VO plus music | 0 separable | 0 | not readable |
| Motion Swell, SaaS Product Demo (UI Animation) (2025-11) | 21 s | music on a 120 BPM 8th note grid | 0 off the music grid | 0 | no |
| Raycast, Raycast Pro preview (2023-05) | 22 s | staccato chord music | 3 (riser, silence, impact) | 8 | no |

Event lists with type and level (time in s, type, peak over bed):
- Superhuman: 4.5 to 5.6 whoosh swell +18.3 dB (over a quiet intro); 6.3, 9.9 and 11.7 short noise swipes +2.6, +5.1 and +1.1 dB (at or under music level; may be part of the track); 14.6 drop or impact at the section start +24.5 dB (over the quiet intro, +6.1 dB over the film median); 27.4 to 28.7 the music is filtered down (a dip, not an SFX); 40.0 to 44.6 riser (a rising sweep, music low passed underneath) +6.6 dB; 44.4 drop after it +9.3 dB; 58.5 to 59.3 riser into the end card +7.7 dB.
- Linear Releases: 0.06 opening low hit (+5.2 dB over film median); 10.2 to 11.2 airy swell +7.5 dB; 17.8 section entry +7.4 dB; 26.1 to 26.5 two final low hits +11.3 dB, then a 3 s fade to silence. No clicks anywhere.
- Arc 1.0: nothing separable from the music; hats and a pumping sidechained bass mark every 1.7 s phrase. Earlier library measure of this film: no dip or near silence ([local note](/home/wopler/dev/mgpro-research/research_notes/Sound%20design%20in%20motion%20graphics/real_films_measured.md)).
- That's Framer: 5.3 to 6.1 riser or suck into a drop +7.7 dB, the level dips to -50 dBFS just before; 6.1 drop +13.1 dB; 18.3 to 18.8 rapid burst of high ticks +8.7 dB; 30.2 hit +7.0 dB.
- Screen Studio: 0.7 whoosh burst +16.8 dB on the opening; keyboard foley under the live action close ups (6 to 7 s, keyboard shown in frame); 16.4 tonal whoosh +17.5 dB where the film moves from live action into the UI section; in the UI section (24 to 42 s) only plucked synth notes on a regular grid, with two possible clicks at 39.0 and 39.3 (+6.4 and +9.3 dB, on the frame a "Private" toggle appears, but they could be note attacks); 42.8 logo hit +9.2 dB.
- Supademo: 3.6 to 4.0 rising tonal sweep +4.6 dB; 7.9 drop +10.9 dB. The music is mastered so loud that little can poke above it.
- Zelios for Teamble: 4.1 and 5.5 hard cuts of the whole track to near silence (-43 and -48 dBFS) as punctuation; 6.0 to 7.3 riser +6.9 dB; 7.3 drop with a tonal "zip" +12.2 dB. After that, VO and music cover everything.
- Raycast Pro preview: 18.0 to 19.45 noise riser +9.2 dB; 19.45 to 19.6 a 150 ms cut to silence (-25 dB under the bed); 19.6 impact or drop at the logo +12.8 dB over bed, +16.9 dB over the film median.
- Across all 10: whooshes appeared at 4 to 5 transitions in total, never once per motion. In the two UI animation videos with the most on screen motion (Motion Swell, Screen Studio UI section) every audible attack lines up with the music grid, so the motion is "sounded" by the music, not by SFX.
- Earlier wider sample for comparison (129 professional films, same machine, October 2026): onset strength around a picture cut rises to only 1.18 times its baseline on average (per film median 1.7 times), and 71% of the films contain no near silence; the three mgpro AI films rise to 18.6 times at cuts. [Local note: real_films_measured.md](/home/wopler/dev/mgpro-research/research_notes/Sound%20design%20in%20motion%20graphics/real_films_measured.md)

### Inferences
- Two different practices exist side by side. Sound designed launch films (the Contra and HeroUI stems) carry dense, continuous SFX layers tucked under the music. Brand and SaaS videos as published on YouTube mostly lean on music cut to picture plus a handful of structural accents per minute. Both share the same structural accents: riser into drop, silence before the hit, impact on the logo.
- UI clicks, the sound most associated with "SaaS video", are rare as audible separate events in this sample. When present they are quiet and tied to one meaningful action (a toggle, a feature reveal), consistent with the vendor advice to keep clicks for actions that matter.
- Typical accent level in the middle of a film: 7 to 13 dB over the bed. Above 15 dB only after a quiet intro, a silence or a filter dip, which means the contrast is created by pulling the music down rather than pushing the SFX up.

### Gaps
- Mix only measurement cannot list every SFX. Quiet clicks and pops under music or VO could not be counted, and some "SFX" listed could be parts of the music track. Counts are lower bounds; confidence is high for risers, drops, silences and logo hits, low for clicks.
- No Apple feature video, Notion, Vercel or Pitch film was measured in this pass (Notion, Vercel and Apple films are in the earlier 129 film set, which measured aggregate metrics, not per SFX lists).
- I could not listen to the audio; types are from spectrogram shape (noise swell, rising sweep, tonal partials, broadband hit) plus level curves and the picture.

## What separates these from AI generated videos

### Takeaway
The human pattern is restraint per event and richness per layer: few families, varied takes, SFX mostly under the music, loud only in gaps the music leaves, and big moments made by subtraction (silence, filter dips, hard cuts) before a hit. The mgpro AI film Torq does the opposite: 29 different sound types, 191 cues in 30 s, every cue tied to a picture event from one timing file.

### Cited Findings
- Torq (mgpro AI film) cue sheet: 191 cues in 30 s (382 per min) across 29 sound types (count 51, glass 36, grain 30, tick 9, bell 9, tier 7, blip 7, block 6, whoosh 4, set 4, pr 4, slam 3, rest 3, pop 2, swap 2 and 14 single use types); the file header says "a slam, a tick or a tier always lands on its hit". Per type gains are fixed between 0.3 and 0.9 with only ±1 dB random variation. [Local file: ~/dev/torq-video/audio/cues.py and synth.py](/home/wopler/dev/torq-video/audio/cues.py)
- Professional stem films: 3 families each, 46 to 54 placed gestures per minute, family levels 3 to 14 dB under the music, placement no more correlated with motion peaks than chance (measured above). [Contra](https://contra.com/p/WPMQbb6O-sound-design-exploration-contra), [HeroUI](https://contra.com/p/ks662MrZ-hero-ui-launch-video-sound-design-exploration)
- Published YouTube product films: 0 to 9 identifiable accents per minute, structural, 7 to 13 dB over the bed (measured above).
- The three AI films (Bauwerk, Torq, Sendoku) hit cuts 18.6 times above baseline vs 1.18 for 2,666 professional cuts, have 91 to 100% of onsets on the 16th note grid, and share 42% of strong transients between two films (the same sounds), against 4.6% for unrelated professional films. [Local note: real_films_measured.md](/home/wopler/dev/mgpro-research/research_notes/Sound%20design%20in%20motion%20graphics/real_films_measured.md)
- Practitioner rules that the AI pattern breaks: "commit to a style instead of mixing random sounds" ([Herman Huang](https://www.youtube.com/watch?v=tzfzkTAQsnE)); same keystroke for every key and same pen sound for every stroke named as a first pass mistake, and "if you try to make every moment special none of them will be special" ([Film Editing Pro](https://www.youtube.com/watch?v=Wcxw3BPSt3A)); "many sounds are heard only once" ([Echoic](https://www.izotope.com/community/blog/echoic-audio-part-3)).

### Inferences
- Rules for a code based engine that follow from the data: (1) choose 3 to 4 families per film and stay in them; (2) render families as layers with gesture lengths of 0.5 to 4 s (swells, runs, patterns) rather than one sample per event; (3) mix families 3 to 14 dB under the music (whooshes about -3, mechanical or foley about -7, UI tones about -14) and let a sound rise above the music only where the music has a gap; (4) do not sound every motion: a whoosh or hit on 4 to 8 key moments per minute, with the music carrying the rest; (5) make the big moments by subtraction: a 150 ms silence or a filter dip before the drop, a hard cut of the whole track as punctuation; (6) vary every repeated hit (different takes, not one sample with ±1 dB).
- Counting cues per minute alone does not separate human from AI: the pro stem films have 217 to 242 onsets per minute, close to Torq's 382 cues. The difference is in families (3 vs 29), level relative to music, and coupling to picture events (chance level vs every event).

### Gaps
- The Torq comparison uses its cue sheet, not a stem measurement, so its SFX level relative to its music was not measured here.
- No source was found that directly compares human and AI edited product videos by SFX usage; the contrast is built from the measurements above.
