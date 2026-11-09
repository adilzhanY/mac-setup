# Composition: writing the score like a composer

`music.md` decides what this film's music must be (genre, tempo range, key, palette, form) so it differs from every earlier film. This file is how to write it: timing first, then a short motif, a harmony with fresh colour, a groove that follows the cut, energy built through texture, and an ending that lands on the logo frame. `sound.md` covers effects, realism of the instruments and the mix.

Why this file exists: the Enogon film (mgpro 2.0.0) passed every measured check and the user still heard it as AI music, slow, with holes. A score can be distinct from the registry and still be written like a loop that ignores the cut. Ad composers do the opposite: they lock the timing skeleton to the picture first and write to and away from a few moments.

Sources are linked inline; the full notes are in `research/ad-music-and-logo/` (`notes/composition_craft.md` for most of this file). Studios almost never publish chords or tempos of named ads, so much of the harmony and arrangement advice below is standard composition practice that no single page states. It is marked **(craft practice)**, the same way `sound.md` marks **(heuristic)**.

## 1. Timing first, from the cut's hit points

Composer Jorde Heys, on a 30 s brief, spends the first part of the work "locking down the tempo, any tempo shifts, hit points, and time signature changes" while melodic ideas are still "bubbling away", and composes "to and away from" a few moments ([AFTRS](https://www.aftrs.edu.au/blog/mastering-the-score-jorde-heys-on-crafting-music-to-brief/)). The hit point method notes the exact timecode of each event and chooses a tempo so a strong beat lands on it ([IRPR](https://sounddesign.irpr.agency/glossary/hit-point/)). A textbook commercial cue holds a constant 99 BPM and still lands its hits on downbeats ([Packt, Scoring to Picture in Logic Pro, ch. 10](https://packtpub.com/en-mx/product/scoring-to-picture-in-logic-pro-9781837636891/chapter/chapter-10-scoring-a-commercial-14/section/chapter-10-scoring-a-commercial-14)). Older composers kept printed books of tempos against durations for exactly this ([Mix](https://www.mixonline.com/blog/mix-blog-studio-residual-knowledge)).

In mgpro the picture is code, so this goes both ways: the tempo is chosen from the hit points, and an event a few frames off the grid can be moved to it.

1. **List the hit points** from the storyboard: the 2 to 4 structural moments only (an act change, the reveal or payoff, the logo landing frame). Ordinary cuts are not hit points (`sound.md`, section 6: a bar downbeat alone measures 3 to 9 times baseline).
2. **Compute candidate tempos.** A hit at t seconds lands on beat n when BPM = 60 x n / t. At 60 fps a beat is 3600 / BPM frames; tempos whose beat is a whole number of frames include 72, 75, 80, 90, 100, 102.86, 112.5, 120, 128.57, 144 and 150 BPM (50, 48, 45, 40, 36, 35, 32, 30, 28, 25 and 24 frames; `grooves.FRAME_TEMPOS` lists them all). 96 BPM is never whole (37.5 frames). At 30 fps only 90, 100, 120 and 150 are whole.
3. **Pick the tempo that puts the most hit points on downbeats** within the genre's range and the contract in `music.md`. Then move the remaining structural events by a few frames to the nearest downbeat, or let them fall on beat 3.
4. **When an event cannot move** (it is tied to a long camera path), catch it with the meter: one bar of 2/4 or 3/4 before it, or a 5/4 or 7/8 bar, keeps the downbeat on the picture **(craft practice)**. In the kit the form takes fractional `bars`, which does the same job.
5. **Lay out the spot by bars** **(craft practice)**: in a 30 s spot at 96 BPM (12 bars), bars 1 and 2 hold one texture and a motif fragment, bars 3 to 6 add a layer and the full motif, bar 7 is the one turn or breath on the main reveal, bars 8 to 10 are the fullest, bars 11 and 12 clear space for the logo: one hit on the logo frame and 1.5 to 2.5 s of ring. Lines of copy get the thinnest bars.

**Worked example.** A 30 s film has three structural hit points: the act change at 7.2 s (frame 432), the reveal at 19.2 s (frame 1152), the logo landing at 26.4 s (frame 1584).

| Tempo | Beat (frames) | 7.2 s | 19.2 s | 26.4 s | Verdict |
|---|---|---|---|---|---|
| 120 | 30 | beat 14.4 | beat 38.4 | beat 52.8 | none on a beat |
| 112.5 | 32 | beat 13.5 | beat 36 (bar 10, beat 1) | beat 49.5 | one |
| 100 | 36 | beat 12 (bar 4, beat 1) | beat 32 (bar 9, beat 1) | beat 44 (bar 12, beat 1) | all three on downbeats |

100 BPM wins. A fourth event at 13.1 s (frame 786) sits on beat 21.8: it is not structural, so it stays with the action; if it must be a hit, move it 6 frames to frame 792 (beat 22, the third beat of bar 6).

Second case, the Enogon rebuild at 112.5 BPM (32 frames a beat, 128 a bar), counted on a plain 4/4 grid from frame 0: the logo lands at frame 1376, beat 43, the last beat of bar 11, not a downbeat. Moving the picture to the next downbeat costs 32 frames (frame 1408, 23.47 s), so here the music moves instead: one 3/4 bar earlier in the form puts a downbeat on 1376. Check this for every film before the cue list is written.

## 2. Tempo: from the cut, then from the feel

- The first three mgpro films all sat at 120.2 BPM, where only 18 percent of professional films sit between 117 and 123 (`sound-research.md`, section 1). Choosing tempo from the hit points fixes the habit and the sync at once.
- The user heard the Enogon score at 102.86 BPM as too slow and asked for music that is "faster and more dynamic, but still readable" (Enogon review, `lessons.md`). Faster does not mean busier: a faster pulse with sparse upper parts reads as energy, and a slow pulse cannot be rescued by adding notes.
- Rough ranges by feel, quarter note **(craft practice)**: calm, wellness, a premium reveal 60 to 80 (or 120 to 160 felt in half time); thoughtful tech with piano and ostinato 84 to 100; a confident product, indie electronic 100 to 118; an energetic launch, sport, Afro and Latin 118 to 128; hype and social cut downs 128 to 150, or half time at 140 to 170.
- Tempo is the strongest single lever on arousal ([Wikipedia, Music and emotion](https://en.wikipedia.org/wiki/Music_and_emotion)), and arousal is predicted better than valence (r = 0.81 against 0.67 in a 2025 meta analysis, [C4DM, Eerola](https://www.c4dm.eecs.qmul.ac.uk/news/2025-06-06.C4DM-Seminar_Tuomas_Eerola)). If the film must feel faster, change the tempo before anything else.
- A half time switch keeps the tempo and the grid but moves the backbeat from 2 and 4 to 3, for a weight moment on a hero shot; double time hats are the opposite gesture **(craft practice)**.

## 3. The motif: 2 to 5 notes

Brand motifs are short and built from few, stable intervals.

- Intel's bong is five notes, D flat, D flat, G flat, D flat, A flat, its rhythm taken from "In-tel In-side" ([t3n](https://t3n.de/news/?p=1627039); [Straight Dope](https://boards.straightdope.com/t/intels-sonic-logo/501341)). Only unisons, perfect fourths and a fifth, ending open on the fifth.
- Antfood's 3 s YouTube logo: a diving bass, an upward glissando, a two note figure on the two syllables of "YouTube", a door unlock texture and a warm major 7th pad, designed around contrasts "small to large, close to far, dark to bright" ([Antfood](https://antfood.com/labs/crafting-youtubes-first-sonic-brand)).
- Across 90 sonic logos, more structural complexity improved recognition but hurt sung recall ([Cambridge repository](https://www.repository.cam.ac.uk/items/903c50f3-6d66-4721-af94-7c037073b139)). So keep the pitches simple and make the timbre and rhythm distinctive.
- Mastercard develops one core melody by changing instrument and tempo, not notes, across cinematic, playful and city versions ([Mastercard](https://newsroom.mastercard.com/news/press/2019/february/sound-on-mastercard-debuts-sonic-brand/)).

Rules **(craft practice)**:

- 2 to 5 notes, under about 3 s at the logo's tempo, one rhythmic hook (a dotted figure, an anticipation, a short then long).
- Fit the brand name's syllables and stress (Intel, YouTube and CBS all do).
- Lead with a leap (a 4th, 5th, 6th or octave), then step back inside it in the opposite direction. Avoid pure scale runs (they sound like a doorbell or a stock riser).
- End on scale degree 5, 2 or 3 over the tonic for "open, forward"; on 1 for "closed, trusted".
- This replaces nothing in `music.md`, Hooks: the hook there (3 to 6 notes, call and answer) is the motif stated twice.

**Develop it across the film** **(craft practice)**: state it softly in one timbre; repeat the same pitches with a displaced rhythm (start on the "and" of 1) or under a new chord, so one melody note changes meaning (E over C, then over Am, then over Fmaj7 where it becomes the 7th); fragment it (the first two notes as a riff or counter line); use inversion only as a counter melody, never as the last statement; restate it in its original form at the logo, in a brighter register or a new timbre.

**Worked example** (Enogon's key, E flat lydian, three syllables "E-no-gon"): B flat 3, F 4, E flat 4 (up a fifth, down a step, closed on the tonic). Bars 1 and 2: only B flat to F on muted piano, under the hook of the plan. Bar 4: the full three notes on mallets over E flat maj7, where the F is the 9th. Bar 7: the same F over C minor 7 (now the 11th), the turn. Bar 9: B flat, F as a counter line in the strings while the bass moves. The logo frame: all three an octave higher on the signature instrument over E flat add9, the last note on the landing frame, 2 s of ring.

## 4. Harmony: simple progressions, fresh colour

What is sourced: I-V-vi-IV is "said to be the most used progression in modern music" ([Berklee Online](https://online.berklee.edu/takenote/common-chord-progressions-and-how-to-make-them-your-own/)); corporate stock music follows "the basic composition rules, and only the basic composition rules" ([Boing Boing](https://boingboing.net/2019/10/23/how-to-make-bland-soulless-co.html)); the "thoughtful tech" sound descends from Thomas Newman, whose Saving Mr. Banks opening uses only I and IV for sixteen bars with an ostinato carrying the motion ([Film Music Notes](https://filmmusicnotes.com/oscar-nominees-2014-best-original-score-part-2-of-6-thomas-newmans-saving-mr-banks/)) and whose Shawshank theme uses C dorian with major 7th and minor 9th voicings and half step movement inside chords ([Beato](https://rosetta.to/u/rickbeato/thomas-newman-stoic-theme-shawshank-redemption-breakdown)); that piano, strings and marimba palette is now sold as stock "in the style of Thomas Newman" ([Shockwave-Sound](https://shockwave-sound.com/stock-music-track/14392/distant-horizon-lp)); Lydian's raised fourth gives the "weightless suspension" film composers use for wonder ([Mark Slater](https://markslater.net/unlocking-the-power-of-the-lydian-mode/)); YouTube's logo sits on a major 7th pad (Antfood, above).

**Clichés to avoid as written** **(craft practice)**:

- I-V-vi-IV or vi-IV-I-V as root position block triads on every downbeat, one chord per bar, at 110 to 128 BPM with claps on 2 and 4.
- The "uplifting corporate" move: every four bars end on V, then crash on I.
- A final root position major triad with a cymbal.
- The ukulele, glockenspiel and claps bundle, sold explicitly "for corporate presentations, advertising" ([MonsterONE](https://monsterone.com/stock-music/independent-ukulele-cheerful-acoustic-commercial-pop-stock-music-o287302/)).
- Piano, strings and marimba minimalism as the default "tech" sound: it is now a stock template.
- The half or whole step "truck driver" key change as the lift.

**The harmony kit** (examples in C, transpose to the film's key) **(craft practice)**:

| Colour | Chords | Use |
|---|---|---|
| Same function, fresher | Fmaj9, C/E, Am11, Gsus4(add9) | IV-I-vi-V with inversions, 9ths and a sus that never resolves |
| Lydian loop | Cmaj7 to D/C (or Dadd9/C) over a C pedal | wonder, a product reveal; two chords for 8 bars are enough |
| Mixolydian | C, Bb/C, F/C over a C pedal | warm, confident, human (outdoors, Afro and Latin grooves) |
| Dorian minor | Dm9 to G/D (or G13) over a D pedal | cool, focused, tech noir |
| Borrowed iv | C, Fm/C (or Fm6), C | one borrowed chord near the end for "earned" warmth |
| Chromatic mediant | from C to Abmaj7 or E major for the reveal, back to Cadd9 | sounds expensive, voice leads by a common tone |
| Newman stasis | I and IV (or Imaj7 and IVmaj7#11) for 16 bars | movement carried by ostinato and inner voices |

- **Pedal points**: hold the bass (or a high piano octave) on the tonic or dominant while the upper chords change. "Forward but grounded", and it lets clashing chords (Bb/C, D/C) sound modern.
- **Voicing**: wide intervals low (an octave or fifth below about C3, no thirds below about E3), close clusters high (2nds and 9ths between C4 and C6), the third in the middle register or left out, the top voice moving by step while the bass moves by fourths and fifths or holds.
- **In 30 s, do not modulate.** Lift by register instead (the same chords an octave up, a new high layer). If a change is needed: the relative major or minor, bVI, or drop the bass for a bar and re-enter a fourth lower.
- **Endings**: resolved is I add9 or Imaj7 (warm, trusted); open is IVmaj7, Isus2, or the melody ending on the 5th or 9th over a tonic pedal (forward looking). Intel ends on the fifth, YouTube on a major 7th colour.
- `theory.py` holds the modes and `theory.PROGRESSIONS`; write the numerals by hand when the kit's moods give the cliché.

## 5. Rhythm and groove

Sourced: rhythm in a short ad score comes mainly from the cut's pacing and the tempo choice (Heys, AFTRS above); motifs take their rhythm from the brand name (Intel, YouTube); Newman's identity rests on ostinato, not drum grooves. The rest is **(craft practice)**:

- A four on the floor loop sounds cheap because of identical velocity, an identical sample, no fills, the same bar fifteen times and no change at the picture's turns. Write 2 and 4 bar phrases with something different in bar 4 (a fill, the kick dropping, an open hat) and make the arrangement change on the cuts.
- Accents with a template that repeats per bar (strong on 1 and on the "and" of 2, for example), ghost snares at 20 to 35 percent velocity on the "e" and "a" 16ths.
- Syncopation that reads as modern: kick on 1 and the "and" of 2; claps on 2 and 4 only in the full section; 3+3+2 eighths (tresillo) for Afro, Latin and dancehall; 3 against 2 or 3 against 4 in shakers and marimba; a dotted eighth delay as a rhythmic layer.
- Swing of 54 to 60 percent on 16ths lifts without a shuffle.
- Odd groupings: one bar of 7/8 or 5/4 to catch a cut, or a 7/8 ostinato over 4/4 drums for restless energy.
- The timing of the performance itself (systematic, not random) is in `sound.md`, Realism.

## 6. Building through texture, not level

Heys builds the climax "through texture and dynamics": a synth front half, a hard cut before the one line of dialogue, then a "punchier orchestral push" into the message. Keith Kenniff calls his Apple, Google and Toyota work "mini film scores"; one Toyota brief asked for spooky ambient in the first half and upbeat pop in the second, as one piece ([NPR / KUER](https://www.kuer.org/2012-08-26/composer-keith-kenniff-keeps-the-ads-humming)). Newman passes an ostinato from piano to strings for a climax ([Scribd notes](https://www.scribd.com/document/487936862/Presentation-Notes)). Professional editors reviewing AI ads named a track that "stays at roughly the same energy level" with no crescendo or drop at the climax as a weakness ([arXiv 2608.24329](https://arxiv.org/html/2608.24329)).

Energy without volume **(craft practice)**: more rhythmic density (8ths to 16ths); a wider register (add a low octave and a high octave); a change of articulation (staccato to legato or back); pads from close to wide voicing; a counter melody in contrary motion; a switch from synth to acoustic or back at the turn; an ostinato handed from one instrument to another.

Roles and registers **(craft practice)**: sub and bass (below C2 to C3) on roots or a pedal only; pulse or ostinato (C4 to C6: piano, marimba, plucks, muted guitar) in 8ths or 16ths; pads or strings (C3 to C5) on chord tones; the motif an octave above or below the ostinato, never in its register; an air layer (C6 and up: bells, shimmer, harmonics) only in the peak and the logo. Leave 300 Hz to 3 kHz open under a voice.

Repetition is not the problem: looped random sequences are rated more musical than ones heard once ([University of Arkansas](https://news.uark.edu/articles/22615/repetition-in-music-pulls-us-in-and-pulls-us-together)). Identical audio is. A four or eight bar figure that changes something each pass (a layer, a fill in bar 4, a voicing, a filter opening) reads as arranged.

Contrast is arranged, never a gain hole: a breath thins the arrangement and keeps a bed or a tail under it (`sound.md`, section 9).

## 7. One lift or one drop per 30 s

In a 15 to 30 s spot there is room for at most one lift or one drop ([PDX spot assignment](https://web.pdx.edu/~jnewton/assignments/69rs_radio_spot/index.html), and the craft notes).

- **A lift** adds layers and register gradually to a bigger restatement of the motif (warm, emotional, a product story).
- **A drop** removes everything but a bed for one or two beats, often after a riser or reverse swell, then slams back with the full groove on a structural cut (hype, launch, social).
- Trailer practice: when every hit is oversized, every riser full band and every cut has a whoosh, the sequence "gets louder but less dramatic", and a held silent frame after a riser often reads bigger than any hit ([add.app](https://add.app/sound-effects/sound-design-for-trailers-hits-rises-drones-pulses/)).
- Builds are short in ads: risers span one to several bars ([UJAM](https://www.ujam.com/tutorials/how-to-create-huge-edm-transitions/)), and at 120 BPM a four bar riser takes 8 s, a third of a 30 s spot. Use one to two bars. A riser built from musical material (a scale or arpeggio whose subdivision doubles over the last one to two bars, Shepard style if it must feel endless) is better than noise ([Medium, Dunkirk](https://medium.com/world-of-music/the-dunkirk-soundtrack-is-way-cleverer-than-you-think-18f5dc155d91)).
- 15 s: usually 6 to 8 bars, one idea, no development (motif, one lift, logo). 45 to 60 s: room for one real development (a reharmonisation, a half time switch) and a return of the opening idea **(craft practice)**.

## 8. The ending and the sonic logo on the landing frame

- The last musical event lands on the logo's landing frame, or one or two frames before it so the transient is perceived on the frame, and its tail rings out inside the film's length; leave at least 1 to 2 s for the tail **(craft practice)**. A strong accent exactly where the animation completes is the common pattern ([Cursa](https://cursa.app/en/page/audio-and-final-rhythm-using-sound-to-support-motion)).
- Pull the groove out one or two beats before the logo, keep a pad or a tail under that gap, then one combined hit on the landing frame: a low thump, the chord and the motif's last note **(craft practice)**.
- The sonic logo is the motif in its original form, the resolved short version of music already heard (Mastercard's 30 s core melody down to a 3 s signature, [Marketing Week](https://www.marketingweek.com/people-asked-if-i-was-smoking-something-mastercards-cmo-on-developing-its-new-sonic-branding/)).
- Pair a real tactile hit with a musical tail: Netflix's ta-dum is a wedding ring knocked on a cabinet with a reversed guitar swell, briefed as "tension and release" ([MusicRadar](https://www.musicradar.com/news/the-netflix-ta-dum-sound-features-a-reversed-electric-guitar-sample-that-was-created-using-90s-effect-pedals)). Recorded, not synthesized (`sound.md`, Realism).
- Hans Zimmer's theatrical Netflix ident builds about 16 s of tremolo strings and percussion into the same ta-dum, because the 3 s original felt rushed in a cinema ([Classic FM](https://www.classicfm.com/composers/zimmer/netflix-extended-cinema-ta-dum-sound/)): the logo sound can grow with the film; its core stays the same.
- The logo's picture rules (one decisive move, a clean frame before, a 1.5 to 3 s hold) are in `logo-resolve.md`.

## 9. Feeling: arousal first, brand words last

Tempo, loudness and pitch variation raise arousal; mode and consonance shift valence; legato reads calm or cohesive, staccato tense, energetic or playful ([Wikipedia, Music and emotion](https://en.wikipedia.org/wiki/Music_and_emotion)). Juslin's mechanisms give an ad its levers: a brain stem reflex for sudden loud hits, rhythmic entrainment for pulse, musical expectancy for tension and release, conditioning for a sonic logo ([Juslin 2013](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2013.00596/full)). Brand words such as "premium", "trust" or "precision" have no peer reviewed mapping. Working translations **(heuristic, from `notes/transitions_and_feeling.md`)**:

| Brand word | Music |
|---|---|
| precision | staccato, short envelopes, sparse rhythm locked to the grid, consonant, dry or short space; a moderate tempo so it stays calm |
| trust, calm | legato, moderate to slow tempo, mid or low register, cadences that resolve, low pitch variation |
| warmth | legato, mid and low register, soft attacks, darker timbre, close space |
| delight, playful | staccato, higher register, major, faster, small surprises that resolve quickly |
| effortless | legato, a steady pulse without dense fills, few hard transients, long smooth envelopes |
| premium | restraint: fewer elements, longer tails, wide but uncluttered stereo, one well made signature sound |

## 10. Before the score is called done

- [ ] Hit points listed, tempo chosen from them, every structural moment on a downbeat (or a meter change catches it).
- [ ] A motif of 2 to 5 notes, stated, developed and restated at the logo in its original form.
- [ ] No progression from the cliché list as written; at least one colour from the kit (a pedal, a sus or add9, a lydian or dorian loop, a borrowed chord).
- [ ] Energy built by texture, register and articulation; at most one lift or one drop per 30 s; no gain hole anywhere.
- [ ] The last note on the logo's landing frame, its tail inside the film.
- [ ] Every rule of `music.md` (contract, fingerprint) and the realism rules of `sound.md` still pass.
