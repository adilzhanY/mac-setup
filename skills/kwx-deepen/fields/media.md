# Media and creative

## When this playbook applies

- Video: edit a cut, make a promo, trailer, explainer, tutorial, talking head, social clip.
- Motion graphics: animate a logo, title sequence, UI demo, kinetic type, data animation.
- Audio and music: mix, master, podcast cleanup, voiceover, score, sound design, loudness fixes.
- Photography and images: shoot plan, retouch, colour grade, product shots, hero images, thumbnails, asset sets.
- Presentations: build or fix a deck, pitch, talk, keynote, board update, slide redesign.

## The expert

Pick the one whose failures this request would cause, and adapt the description to the exact case. It goes on the `Expert:` line of the output block; the rewritten task itself carries the moves, never a persona line (`method/expert.md`).

- Feature film editor, 20+ years, story and performance first (the Walter Murch type). Fits: any cut of existing footage, trailers, documentary, "make this video better".
- Broadcast and streaming re-recording mixer, 15+ years, delivers to published specs (EBU R128, Netflix). Fits: mixing, mastering, podcast audio, "it sounds bad", any audio that will be published.
- Motion designer at a product studio, 10+ years, animates product UI and brand systems. Fits: logo animation, UI demo, explainer, kinetic type.
- Commercial photographer and retoucher, 15+ years, product and editorial, colour managed workflow. Fits: product images, portraits, retouching, image sets for a site or store.
- Presentation designer and speechwriter, 10+ years, executive talks and pitches (the Duarte or Minto trained type). Fits: decks, talks, board updates, pitch rehearsal.

## Moves the expert makes unasked

1. Name the destination and its spec before touching anything (platform, aspect ratio, length, loudness target, colour space, room size for a talk).
   Why: the destination decides what "good" means; a mix right for cinema is wrong for a phone.
   Check: the task states one destination and quotes its numbers (for example "Spotify, -14 LUFS integrated, -1 dBTP").
2. Write the one sentence the audience should remember, before structure or style.
   Why: every cut, shot and slide is judged by whether it serves that sentence.
   Check: a single takeaway sentence exists and each section can be tied to it.
3. Watch or listen to all the raw material once without editing, taking timecoded notes.
   Why: Murch logs first impressions because the first viewing is the only time you see it like the audience will.
   Check: a log with timestamps and reactions exists before the first cut.
4. Judge cuts by emotion first, then story, then rhythm, then eye trace, screen plane and space (Murch's Rule of Six, weighted 51, 23, 10, 7, 5, 4).
   Why: a cut that is right emotionally survives small continuity errors; the reverse is not true.
   Check: review notes name the emotional reason for the weakest cuts, not only continuity.
5. Cut for the first 3 seconds and the ending separately.
   Why: on feeds, viewers decide in the opening, and the ending decides whether they act.
   Check: the opening shows the subject or the promise within 3 seconds; the ending has a single clear next step.
6. Measure loudness with a BS.1770 meter and deliver to the target, instead of mixing "until it sounds loud".
   Why: platforms normalize; an over-limited master is turned down and just sounds squashed.
   Check: integrated loudness, true peak and loudness range are reported in numbers.
7. Check the work on the worst playback device (phone speaker, laptop speaker, projector in a lit room).
   Why: most viewers will not have studio monitors or a dark room.
   Check: notes from at least one low-end playback pass exist.
8. Keep a clean, colour managed chain: shoot or export in a known profile, convert to sRGB for the web, soft proof for print.
   Why: an unmanaged file shifts colour on every screen and printer.
   Check: the export settings name the colour profile and it is embedded.
9. Use motion with purpose: one primary movement at a time, consistent easing, durations from a scale (Material 3 duration tokens run from 50 to 1000 ms).
   Why: unmotivated motion reads as noise and makes UI demos feel slow.
   Check: every animated element has a stated purpose; durations and curves come from one defined set.
10. Make it accessible: captions for prerecorded speech (WCAG 1.2.2), no more than three flashes per second (WCAG 2.3.1), text contrast on images and slides at 4.5:1 or above, alt text for images.
    Why: many viewers watch muted, some cannot hear, flashing can trigger seizures.
    Check: a caption file exists, a flash check was run, contrast was measured.
11. For decks, put the answer first and group support beneath it (Minto pyramid), and make each slide title a full sentence claim.
    Why: busy audiences read titles only; a topic label like "Q3 results" tells them nothing.
    Check: reading only the slide titles in order tells the whole argument.
12. Decide whether the deck will be presented or read, and build it for that one use.
    Why: Duarte: reports should be distributed, presentations presented; one file doing both does both badly.
    Check: the task says which one it is. If the user needs both, that is a second deliverable: say so and let them choose.
13. Clear rights for every asset: music licence, stock licence, model and property releases, font licence.
    Why: an unlicensed track gets a video muted or taken down after launch.
    Check: an asset list with source and licence for each item.
14. Export a test render at final settings early, and check it on the target platform.
    Why: platform recompression, safe zones and UI overlays (captions, buttons) ruin details you cannot see in the editor.
    Check: one early test upload or simulated overlay review is noted.

## Raw material

- Camera originals and full takes, not the proxies or the last exported cut. Get them from the project folder or the person who shot it. Distrust a previous edit as a starting point: it hides the takes that were rejected, which are often the better ones.
- Multitrack stems or the session file for audio, not a stereo bounce. Distrust a file already normalized or limited by someone else.
- RAW photo files with their metadata, not JPEGs from a chat app (stripped profile, recompressed).
- The source facts for a deck: the actual data tables, the decision being asked for, who is in the room. Distrust last quarter's deck as a template for this quarter's argument.
- Destination specs from the platform itself: EBU R128 and EBU Tech 3341 or 3342, Netflix Partner Help sound and image specs, Spotify for Artists loudness page, W3C WCAG Understanding pages. Distrust vendor blog tables of "LUFS per platform": they are often out of date and copy each other.
- Reference work: 2 or 3 finished pieces the requester admires, and their measured numbers (loudness, cut rate, shot length, slide count). Distrust adjectives ("punchy", "clean", "premium") until tied to a reference.
- Brand assets in source form (vector logo, fonts, colour values), not screenshots of a website.

## Methods and tools

- Rule of Six (Murch, In the Blink of an Eye): to decide where and whether to cut.
- Timecoded logging and a paper or card edit: before a long edit, to see structure without rendering.
- Save the Cat beat sheet (Snyder, 15 beats) or a three act outline: for narrative video and trailers; use as a check for missing turns, not as a formula.
- Duarte's sparkline (what is versus what could be, ending on the new bliss and a call to action): for persuasive talks and pitches.
- Minto Pyramid Principle with SCQA opening (situation, complication, question, answer): for business decks and board updates.
- Loudness metering to ITU-R BS.1770 (for example ffmpeg `loudnorm` or `ebur128` filter, Youlean, iZotope Insight): every audio deliverable. Targets: EBU R128 broadcast -23 LUFS, true peak under -1 dBTP; Netflix dialog gated -27 LKFS within 2 LU, true peak -2 dBTP; Spotify -14 LUFS integrated, true peak -1 dBTP (-2 dBTP if louder than -14); AES TD1008 for streaming (about -18 LUFS for speech, -16 LUFS for track normalized music).
- Disney's 12 principles of animation (timing, easing, anticipation, follow through): for character and logo motion.
- Material 3 motion tokens (duration steps and emphasized or standard easing): for UI demos and product motion.
- Histogram and clipping warnings, a calibrated display, soft proofing: for every photo delivery.
- Tufte's data ink and small multiples: for any chart on a slide.
- Remotion, After Effects, DaVinci Resolve, Premiere, Logic, Reaper, Lightroom, Capture One, Keynote: choose by what the team already uses; the method matters more than the tool.

## Independent proof

- Spec compliance by measurement: run `ffmpeg -i out.wav -af ebur128=peak=true -f null -` (or `loudnorm=print_format=json`) and compare integrated LUFS, true peak and LRA with the published target. Pass or fail is a number, not an opinion.
- Flash and caption checks: run a photosensitivity analyzer (for example PEAT or a frame luminance script) on the final render; validate the caption file parses and covers every line of speech with timing.
- Contrast measurement: sample text and background colours from the exported frame or slide and compute the WCAG contrast ratio.
- Five second test or first impression test with 3 to 5 people from the audience: show the thumbnail, opening or title slide, ask what it is about. Compare their answer with the takeaway sentence. An agent writes the test and flags it as not run unless people are available.
- Titles only read: an agent extracts slide titles in order (for example with `python-pptx`) and checks they form a complete argument without the bodies.
- Retention or completion data after release (YouTube Studio audience retention, Spotify listen through, talk Q and A questions): the real verdict, defined before release.
- Side by side with the named reference at matched loudness: louder always sounds better, so match levels before comparing.
- Platform preview: upload unlisted or use the platform's safe zone overlay and confirm nothing important sits under its UI.

## Amateur mistakes

- Mixing to sound loud, then shipping a master that the platform turns down by 6 dB and that sounds flat next to others.
- Measuring peak with a sample peak meter instead of true peak, so the encoded file clips.
- Cutting on action or beat alone and ignoring emotion and performance.
- Starting a video with a logo sting or a long intro, losing the feed viewer before the subject appears.
- Music that fights the voice: no ducking, no EQ space around 1 to 4 kHz for speech.
- Exporting photos in Adobe RGB or Display P3 for the web without converting to sRGB or embedding the profile, so colours look dull or wrong wherever the profile is lost.
- Over retouching skin and product edges until they look plastic, with no comparison at 100 percent zoom.
- Slides with topic titles and bullet lists that the speaker reads aloud.
- Charts with 3D effects, legends far from the data, or more than one message per chart.
- Text burned into video that sits under the platform's caption or button area.
- Using a track because it is on a free site without checking the licence covers commercial use and the platform.
- Animating everything with the same default ease and duration, so nothing has hierarchy.

## Scope traps

"Deeper" means the same deliverable made better for its audience and destination. It turns into "bigger" when:

- One 30 second cut becomes a series of cutdowns, aspect ratios and languages nobody asked for.
- Fixing a mix becomes re-recording the voiceover or composing a new score.
- A deck fix becomes a full brand template system.
- A photo retouch becomes a reshoot plan.
- A motion piece adds 3D, particles or a character when the brief is one product screen.

Typical "not doing" items: other aspect ratios or lengths, new footage or reshoots, original music unless asked, translations, a new brand system, a template for future work, paid ads setup.

## Worked example

Vague request: "Make my product demo video better." (A 2 minute screen recording with voiceover, for the landing page.)

1. Expert: a product motion designer and editor, 10+ years on SaaS launch videos.
2. Unasked moves (top 5): name the destination (landing page, autoplay muted, then click for sound); one takeaway sentence; show the result in the first 3 seconds; captions so the muted version alone tells the story; loudness measured to a stated target.
3. Raw material: the original screen recording at full resolution, the voiceover stem, the landing page where it will sit, 2 reference videos the requester likes.
4. Methods: timecoded log, Rule of Six for trims, BS.1770 metering with ffmpeg, WCAG 1.2.2 and 2.3.1, Material motion durations for zooms and callouts.
5. Proof: ffmpeg loudness report against -16 LUFS integrated (a common web and podcast target; AES TD1008 suggests -18 LUFS for speech, so state the choice) and -1 dBTP; caption file covers all speech; a muted viewing by 3 people who can say what the product does (scripted, flagged as not run if no viewers are available); length measured.
6. Rewritten task:

```
Re-edit the existing 2:00 product demo for the landing page hero (muted autoplay, sound on click).
Goal: a first-time visitor can say what the product does after watching muted.
Keep length at or under 2:00. Show the end result within the first 3 s.
Trim dead time, add zoom and callouts on the 3 key actions (durations 250 to 400 ms, one easing).
Mix voice to -16 LUFS integrated, true peak at or under -1 dBTP; deliver burned and .vtt captions.
Prove it: ffmpeg ebur128 report, caption coverage check, flash check, 3 person muted test (flag if not run).
Not doing: new footage, new voiceover, music composition, other aspect ratios, cutdowns.
```

## Sources

- Walter Murch, In the Blink of an Eye (2nd ed., Silman-James, 2001); Rule of Six summary: https://nofilmschool.com/2016/11/6-rules-good-cutting-according-oscar-winning-editor-walter-murch
- Blake Snyder, Save the Cat (2005); beat sheet: https://savethecat.com/beat-sheets
- EBU R 128 (2014 revision): https://tech.ebu.ch/docs/r/r128-2014.pdf
- ITU-R BS.1770 loudness measurement: https://www.itu.int/rec/R-REC-BS.1770
- Netflix Sound Mix Specifications and Best Practices: https://backlothelp.netflix.com/hc/en-us/articles/360001794307-Netflix-Sound-Mix-Specifications-Best-Practices-v1-5
- Spotify for Artists, loudness normalization: https://support.spotify.com/artists/article/loudness-normalization
- AES TD1008 streaming loudness recommendation (summary by Ian Shepherd): https://productionadvice.co.uk/td1008/
- W3C, Understanding WCAG 2.2, Captions (Prerecorded): https://www.w3.org/WAI/WCAG22/Understanding/captions-prerecorded.html
- W3C, Understanding WCAG 2.2, Three Flashes or Below Threshold: https://www.w3.org/WAI/WCAG22/Understanding/three-flashes-or-below-threshold.html
- W3C, WCAG 2.2 contrast minimum: https://www.w3.org/TR/WCAG22/#contrast-minimum
- W3C, Understanding WCAG 2.2, Non-text Content (alt text): https://www.w3.org/WAI/WCAG22/Understanding/non-text-content.html
- Material Design 3, motion easing and duration tokens: https://m3.material.io/styles/motion/easing-and-duration/tokens-specs
- Twelve basic principles of animation (Thomas and Johnston, The Illusion of Life, 1981): https://en.wikipedia.org/wiki/Twelve_basic_principles_of_animation
- International Color Consortium (colour management, sRGB): https://www.color.org/
- Nancy Duarte, Resonate (2010): https://www.duarte.com/resources/books/resonate/
- Barbara Minto, The Pyramid Principle: https://www.barbaraminto.com/
- Edward Tufte, The Cognitive Style of PowerPoint (2003): https://www.edwardtufte.com/book/the-cognitive-style-of-powerpoint-pitching-out-corrupts-within-ebook/
