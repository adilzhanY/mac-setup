# How video editors and motion designers find, audition, choose and organise premade sound effects

Source quality note for the report writer: Reddit (reddit.com) is blocked for this research agent's search and fetch tools, and Reddit mirrors returned 403, so no first-hand r/editors or r/sounddesign threads could be read. No first-hand interview was found in which an editor for MKBHD, Ali Abdaal, Johnny Harris or Kurzgesagt explains their SFX picking process in detail (the MKBHD material below is a third-party summary of a team video). Much of the practical "how to" material on the open web in 2024 to 2026 comes from vendor blogs (Pixabay, Krotos, Sonilo, Morphic, SFX Engine, media.io, Videotto). Their advice is consistent with each other but should be treated as practitioner heuristics, not measured fact. The strongest hard data are Freesound's own 2024 statistics.

## 1. Search terms, query tricks and filters on Freesound, Pixabay, Zapsplat and similar

### Takeaway
Real search behaviour is short and generic ("whoosh", "click", "woosh"), which is exactly why results feel samey. The better trick is to combine an action word with a feel word and a context word ("whoosh soft short", "UI click success"), try every synonym (whoosh / swoosh / swish / woosh), and filter by duration first (under 1 s for UI, 1 to 3 s for transitions) and by licence (CC0 or CC BY for commercial work).

### Cited Findings
- Freesound's most searched terms in 2024 were "wind, rain, explosion, music, whoosh, footsteps, woosh, click". Both spellings "whoosh" and "woosh" are in the top list, so libraries are tagged under both. [Freesound blog, 2024 in numbers](https://blog.freesound.org/?p=2141)
- Freesound search filter usage in 2024: tags are over 57% of filter use, licence 15.4%, file type 5.9%. Default "Automatic by relevance" sort is over 81% of requests; newest first 11.9%; most downloaded 2.1%; highest rated 1.7%. Most queries are "a few words". [Freesound blog, 2024 in numbers](https://blog.freesound.org/?p=2141)
- Freesound scale: 670,954 sounds in total, 56,964 new in 2024, average sound length 73 seconds, 18,786,432 downloads in 2024. The 73 s average means many files are long recordings that contain the useful moment somewhere inside, so duration filters matter. [Freesound blog, 2024 in numbers](https://blog.freesound.org/?p=2141)
- Licences of 2024 Freesound uploads: Attribution (CC BY) 45%, CC0 44%. Historically CC0 was about 60% and Attribution about 25%. So a growing share of Freesound needs a credit line. [Freesound blog, 2024 in numbers](https://blog.freesound.org/?p=2141)
- Freesound's team points users to the "advanced search" section for min/max duration, and one user sorts by duration shortest first because most results ran too long. You can include or exclude words with + and - (for example "+water -rain"). [Freesound forum, via search snippet](https://freesound.org/forum/production-techniques-music-gear-tips-and-tricks/44539)
- Freesound filter syntax used by the Creative Commons client example: `duration:[0.0 TO 15.0]`, `avg_rating:[4.5 TO 5.0]`, `license:"Creative Commons 0"`. The API filter field is singular "tag", not "tags". [Creative Commons, Freesound intro](https://opensource.creativecommons.org/blog/entries/freesound-intro/); [Freesound API docs](https://freesound.org/docs/api/resources_apiv2.html)
- For commercial projects, open-source tooling treats CC0 and CC BY as usable and excludes CC BY-NC. [Freesound scraper / bgm provider code, via search snippet](https://apify.com/crawlerbros/freesound-scraper)
- Pixabay's own guidance on search: combine action and feel ("whoosh soft short", "impact deep muted", "notification friendly"); add context ("UI click success", "typing modern"); try synonyms (whoosh/swoosh/swish, impact/hit/slam, bubble/pop/plop). Filter by duration: under 1 second for UI, 1 to 3 seconds for transitions, longer for ambiences. [Pixabay blog](https://pixabay.com/blog/posts/free-and-high-quality-sound-effects-for-video-edit-453/)
- Pixabay sound licence summary: free for commercial and non-commercial use, no attribution required; do not resell or redistribute the raw files as standalone sounds. [Pixabay blog](https://pixabay.com/blog/posts/free-and-high-quality-sound-effects-for-video-edit-453/)
- Format: use WAV "when possible for editing headroom", MP3 only for small final exports; "48 kHz is a safe default for video; 44.1 kHz for music-only contexts." [Pixabay blog](https://pixabay.com/blog/posts/free-and-high-quality-sound-effects-for-video-edit-453/)
- For typing, "soft keyboard tones suit modern looks better than mechanical clacks". [Pixabay blog](https://pixabay.com/blog/posts/free-and-high-quality-sound-effects-for-video-edit-453/)

### Inferences
- Because 81% of Freesound searches use relevance sort and queries are a few words, the top results for "whoosh" are the ones everyone else also downloads. Sorting by newest, adding a texture word ("cloth", "paper", "air", "bamboo", "stick", "flag"), or excluding words ("-cinematic -trailer") is a cheap way to get sounds other editors have not used.
- A practical query set for product and UI edits, built from the cited synonym and context tricks: "click" + ("mouse", "trackpad", "UI", "button", "switch", "toggle", "soft"); "whoosh" / "swoosh" / "swish" + ("short", "soft", "cloth", "air", "subtle"); "pop" / "plop" / "bubble"; "paper" + ("slide", "rustle", "flip", "page turn"); "riser" / "rise" + ("tonal", "short"); "impact" / "hit" + ("muted", "soft", "deep"). The specific terms "trackpad click", "swish cloth" and "paper slide" were not found quoted in any source; they follow the cited "action + feel + context" rule.
- Filter order that follows from the data: licence (CC0, then CC BY) first, then duration (0 to 1 s for clicks and pops, 0.3 to 3 s for whooshes), then format WAV and 48 kHz where offered.

### Gaps
- No Zapsplat-specific search advice was found. No source quoted Reddit users' actual search strings.
- No source gave sample-rate filter usage numbers on Freesound (file type is 5.9% of filter use, but sample rate was not broken out).

## 2. How editors pick between 20 similar whooshes, and how they judge fit (material, size, speed, pitch, length)

### Takeaway
The working rule is "the sound follows the motion": speed, mass, direction, distance and stopping point. Short and bright reads fast and light; long and low reads big and heavy; the whoosh must not outlast the move; its peak lines up with the fastest point of the motion; an impact is only added where something visibly lands. Variants should be level-matched before comparing, because the louder one always sounds "better".

### Cited Findings
- MKBHD team (Ellis): "things that move should make a sound"; a phone rotating on screen should get "a big, low-pitched whoosh to convey its mass"; easing in the animation should be mirrored in the sound; "when viewers don't notice the audio, it means it's working perfectly". This is a third-party summary of an MKBHD team video, not a transcript. [Gistly summary of MKBHD team video](https://gist.ly/youtube-summarizer/master-video-editing-creative-choices-pro-tips)
- "A convincing whoosh sound effect follows the motion's speed, mass, direction, distance, and stopping point." "Short, bright envelopes feel fast; long builds suggest broad or deliberate motion." [Sonilo whoosh guide](https://sonilo.com/ai-music/whoosh-sound-effect-guide)
- Sonilo's worked examples: a product fly-by of 1.15 s with its fastest point at 620 ms; a title reveal of 0.48 s with its last 80 ms left empty for a separate impact; a tiny interface card crossing 10% of the screen in 180 ms needs a different envelope from a heavy pass. Advice for finding the sync point: "Move the cross point one frame earlier and later and watch at normal speed." [Sonilo whoosh guide](https://sonilo.com/ai-music/whoosh-sound-effect-guide)
- Sonilo on auditioning: level-match variants before judging, because loudness is mistaken for quality. It does not give a number of variants to audition. Its four-layer model: air, texture, optional tonal, landing; use the landing layer only when an object visibly stops, attaches or appears. [Sonilo whoosh guide](https://sonilo.com/ai-music/whoosh-sound-effect-guide)
- "A whoosh that outlasts its transition is the most common reason one feels wrong, because the ear expects the sound to end when the picture settles." A heavier, deeper pass with a dropping pitch "reads as mass moving rather than air alone". [Morphic whoosh guide, via search snippet](https://morphic.com/resources/sounds/whoosh-sound-effect)
- "Shorter, softer whooshes feel subtle; longer, brighter ones feel flashy." Match whoosh duration to the transition length as a starting point. [Pixabay blog](https://pixabay.com/blog/posts/free-and-high-quality-sound-effects-for-video-edit-453/)
- Timing: start the whoosh 10 to 20 ms before a camera move so sound leads picture; align the whoosh peak with "the movement's fastest point or most motion blur". [media.io / Ocular Sounds, via search snippet](https://ocularsounds.com/blogs/sound-design-tips-tricks/whoosh-audio-effect-adding-motion-and-energy-to-your-edits)
- "Choose a sound effect whose transient (the loudest, sharpest part of the waveform) aligns with the action"; "tens of milliseconds matter"; time the top transient layer "just before the visual peak for perceived impact". [SFX Engine blog](https://sfxengine.com/blog/sound-design-tips-for-video-editors); [Krotos blog](https://krotos.studio/blog/what-is-sound-design-in-video-editing)
- A delay of about two frames between visual change and sound can make an edit feel laggy. [MyInstantPlay blog](https://myinstantplay.com/blog/top-sound-effects-youtubers-use-in-every-video) (low-quality source)
- Cinematic boom versus impact: a boom "swells in slowly and feels like it arrives", an impact "has a fast percussive front and lands on a specific frame. Use the first to fill a held shot and the second to mark a cut." [Morphic boom guide](https://morphic.com/resources/sounds/boom-sound-effect)
- UI sounds: keep clicks quiet and crisp, pitched so they do not mask voices; keep each family (success, error) consistent in pitch and decay so the product "speaks with one voice". [Pixabay blog](https://pixabay.com/blog/posts/free-and-high-quality-sound-effects-for-video-edit-453/)
- Product motion: a click should land "at the exact moment of contact", with a softer whoosh as the next screen slides in; a UI toggle should click as it snaps into place. [Motion The Agency](https://www.motiontheagency.com/blog/sound-design-examples-before-after-in-motion)
- Pitch against music: pitched SFX that are not in the key of the score clash; the fix is to tune them to the scale (start at the root note, shift in cents to scale notes), or design them in the project key from the start. [CRI Middleware blog, Keeping SFX in Key](https://blog.criware.com/index.php/2020/05/20/keeping-sfx-in-key/)
- A TikTok editing post argues generic non-tonal swipes are in nearly every pack and feel disconnected; it suggests tonal risers, impacts and swells "in the film's key" so they blend with the score. [TikTok discover page](https://www.tiktok.com/discover/whoosh-sound-effect-for-edit?lang=en) (weak source)

### Inferences
- A repeatable audition method from these sources: (1) shortlist by length first (file length roughly equal to the move, or shorter); (2) level-match the shortlist; (3) drop each candidate on the timeline with its peak on the fastest frame of the motion and watch at normal speed, nudging one frame either side; (4) pick by weight (low and long for big or heavy objects, bright and short for small UI); (5) if the sound has a clear pitch, check it against the music key or choose an unpitched one.
- Material match (cloth, paper, air, plastic) is implied by "mass and material" guidance but no source gave a concrete rule beyond "weight that doesn't match the object" being a cheap tell.

### Gaps
- No source gave a number for how many variants editors audition (for example "20 whooshes, pick 1"). This could not be confirmed and should not be stated as fact.
- No first-hand editor interview on picking between similar whooshes was found.

## 3. Overused, recognisable sounds that make an edit feel cheap or templated

### Takeaway
The clearly documented ones are the Vine boom (a 2012 library sound popularised on Vine in 2014, peaked on TikTok and YouTube 2020 to 2022, still everywhere) and the Inception "BRAAAM", which even Hans Zimmer called overused. Beyond named memes, the strongest "templated" tell cited by sources is repetition: the same generic swipe on every transition and identical envelopes reused across edits.

### Cited Findings
- Vine boom: originally uploaded in 2012 (Bluezone Corporation library), popularised on Vine by King Bach in 2014, used to emphasise shock or surprise; peaked 2020 to 2022 on TikTok and YouTube and still regularly used across all major platforms. [Know Your Meme](https://knowyourmeme.com/memes/vine-boom-sound-effect); [meme.com](https://meme.com/memes/vine-boom)
- BRAAAM: trailer obsession began with trailers for Inception (2010); Hans Zimmer reportedly said braams are overused and losing their effect, and that he felt "horrible" when they are used in trailers. Authorship is disputed; the most popular trailer version is from Zack Hemsey's trailer score. [The Playlist](https://theplaylist.net/hans-zimmer-feels-horrible-when-his-inception-bramms-are-used-in-movie-trailers-20131106); [Score (2017)](https://www.score-movie.com/post/2017/04/04/composer-hans-zimmer-never-meant-to-make-movie-trailer-braams-a-thing); [Gizmodo](https://gizmodo.com/video-proof-that-the-inception-braaam-is-being-used-in-5967043)
- A sound design glossary says the braam "became somewhat of a cliche through overuse in a particular era of trailers" but stays effective when crafted with care. [IRPR Sound glossary](https://sounddesign.irpr.agency/glossary/braam/)
- "Low-quality sounds can make an edit feel cheap very quickly, especially when the same type of sweep is used again and again." [media.io, via search snippet](https://www.media.io/audio-effects/whoosh-sound-effects.html)
- Repeating exactly the same whoosh on every transition is listed as a common mistake. [Filmora whoosh guide, via search snippet](https://filmora.wondershare.com/audio-editing-tips/whoosh-sound-effect.html)
- Cheap whoosh tells: a generic sweep pasted over every cut, weight that does not match the object, identical envelopes reused, extreme time stretching with metallic artifacts, piercing highs, an impact where nothing visibly lands, stereo movement that collapses on phone speakers. [Sonilo whoosh guide](https://sonilo.com/ai-music/whoosh-sound-effect-guide)
- Videotto: reaction images and meme sounds suit comedy and commentary; for explainer or business content "stick to whooshes, pops and clean zooms". [Videotto blog](https://videotto.com/blog/add-sound-effects-and-meme-edits)

### Inferences
- Bruh, MLG airhorn, the iPhone ding and "glitch transition pack" sounds are widely seen as meme or template sounds, but no reliable source in this search named them as such. The report should present them as editor folklore, not as a cited finding.
- For product and motion work the bigger risk than any single meme sound is the default top-of-search whoosh reused on every move, which the data in section 1 makes likely.

### Gaps
- No credible source on the bruh, MLG, iPhone ding, or glitch pack sounds being "cheap". No audience research on how meme sounds affect perceived quality was found (some spam sites claimed retention numbers; these were excluded as unreliable).

## 4. Keeping sound sparse: density per minute, and when to use no sound

### Takeaway
The only concrete density numbers found are heuristics from one vendor blog: about one SFX every 8 to 15 seconds in explainers and business videos (roughly 4 to 7 per minute) and at most one every 3 to 5 seconds in comedy. The consistent principle from every source is that each sound must mark something that visibly happens, voice stays on top, and silence is a tool.

### Cited Findings
- Density heuristic: comedy and commentary at most one effect every 3 to 5 seconds; explainers and business roughly one every 8 to 15 seconds, "mostly whooshes and pops". A 30-second funny clip example uses 4 effects spaced at least 4 seconds apart. [Videotto blog](https://videotto.com/blog/add-sound-effects-and-meme-edits)
- When to drop a sound: if it marks nothing, cut it; do not stack a boom, a shake and a sticker on one moment; do not add SFX before the edit is locked, or they land on the wrong moments; many viewers watch muted, so important cues need a visual too. [Videotto blog](https://videotto.com/blog/add-sound-effects-and-meme-edits)
- "More isn't always better"; a whoosh, click or impact on every movement is distracting; "Good sound design knows when to stay quiet." Voiceover "should always be the clearest element". Check the mix on speakers, headphones, laptops and phones. [Motion The Agency](https://www.motiontheagency.com/blog/sound-design-examples-before-after-in-motion)
- "Sound effects should support dialogue, not compete with it"; keep UI peaks tame; use sci-fi sounds sparingly. [Pixabay blog](https://pixabay.com/blog/posts/free-and-high-quality-sound-effects-for-video-edit-453/)
- Keep transition sounds under a second and below the voice. [Videotto blog](https://videotto.com/blog/add-sound-effects-and-meme-edits)
- Real silence is rare in life; sound designers use ambience and room tone so scenes feel believable. [Gistly summary of MKBHD team video](https://gist.ly/youtube-summarizer/master-video-editing-creative-choices-pro-tips)
- Kurzgesagt's own account: each video gets a specifically composed soundtrack from Epic Mountain, and "you wouldn't guess what a difference this step makes if you haven't heard a video without their music and sfx". [Kurzgesagt, our video process](https://kurzgesagt.org/youtube/)

### Inferences
- For a 60 to 90 s product video, the 8 to 15 s rule gives about 4 to 11 featured SFX, plus quiet supporting clicks on UI contact moments. This is a derived number, not a measured industry figure.
- Silence before a key reveal or logo works because everything around it is sparse; dense SFX elsewhere removes that contrast.

### Gaps
- No measured study of SFX density in professional product videos or YouTube explainers was found. The 8 to 15 s figure is one blog's rule of thumb.

## 5. Library habits: folders, naming, tagging, browser tools, licences

### Takeaway
Keep folders shallow and broad (Transitions, UI, Ambience, Foley), use a weekly-processed inbox folder, rename files descriptively (pro libraries use the UCS pattern CatID_FXName_CreatorID_SourceID), and use a browser such as Soundly, Resonic or Reaper's Media Explorer to audition and drag straight to the timeline.

### Cited Findings
- Shallow layout: top-level SFX split into Transitions (swooshes, risers, hits), UI (clicks, pops, notifications), Ambience (room tone, outdoor, crowds), Foley (footsteps, handling, impacts); "deep nesting makes navigation slow and forces you to make categorization decisions that are often ambiguous". Use a staging folder for new downloads, processed weekly (rename, add metadata, move). "Never include dates in audio file names." Keep the library on a synced drive for multi-machine editing. [Wideframe blog](https://try-wideframe.pages.dev/blog/how-to-organize-sound-effects-and-music-for-creator-projects) (single creator's system)
- One guide says poor organisation is the most common reason editors do not use the library they already have, and that a solid library has 50 to 100 whoosh variations (short, long, light, heavy, stylised). [D Jordan Media](https://djordanmedia.com/blogs/news/best-sound-effects-for-video-editing) (vendor)
- UCS file naming: CatID_FXName_CreatorID_SourceID; rename files to UCS as you ingest them, not later. [Spencer Bruce blog](https://www.spencerbruce.com/blog1/2025/10/3/understanding-the-universal-category-system-ucs); [Barbe Generative Diary](https://barbegenerativediary.com/en/sounds/how-to-manage-a-sound-effects-library%EF%BD%9Cthe-universal-category-system/)
- Soundly has supported converting and exporting to UCS since June 2021 and has built-in tools to rename your own files to UCS. [Soundly news](https://getsoundly.com/news/soundly-is-finally-fully-ucs-compliant/); [Soundly FAQ](https://getsoundly.com/faq/does-soundly-the-support-universal-category-system/)
- Soundly's ReaSoundly integration sends sounds to the Reaper timeline as takes or lanes and can align to markers; spotting a selection transfers it "with handles". [Soundly ReaSoundly tutorial](https://getsoundly.com/news/soundly-reaper-integration-with-reasoundly-tutorial); [Soundly FAQ](https://getsoundly.com/faq/can-soundly-spot-to-reaper)
- Reaper's built-in Media Explorer: navigate to the sample folder and drag sounds onto the timeline. [Output blog](https://output.com/blog/reaper-samples-and-loops)
- Resonic is described as a fast audio player, browser and sample manager with a large waveform view and frequency analyser. [AlternativeTo, Resonic Pro](https://alternativeto.net/software/resonic-pro/)
- Artlist publishes its own guidance on using its SFX inside its subscription. [Artlist help](https://help.artlist.io/hc/en-us/articles/29595598088733-Using-Artlist-s-sound-effects)

### Inferences
- With 45% of new Freesound uploads requiring attribution (section 1), keeping the source URL, author and licence next to each file (in the filename's SourceID/CreatorID slots, or a sidecar text file) is the only way to produce credits later. No source described a specific "licence next to the file" habit for video editors.

### Gaps
- No source on how YouTube editors specifically tag in Premiere bins or DaVinci Resolve. No first-hand account of a named YouTube editor's folder structure.

## 6. Editing actions that make a premade sound fit

### Takeaway
The standard toolkit: trim the head to the transient (files often start with silence or pre-roll), fade the tail so it ends when the picture settles, shift pitch (small amounts; past about 4 to 5 semitones quality drops) to change perceived size, layer a body sound with a short transient, add a small impact only when something lands, reverse a sound to make it lead into a cut, and keep the sound below the voice.

### Cited Findings
- Trim silence at the start of a file, since "a sound file may contain silence before the actual effect starts"; for an impact, put the strongest onset on the exact visual frame. [Krotos audio trimming guide](https://krotos.studio/blog/audio-trimming)
- Trim the start to avoid pre-roll muddiness; fade the tail so it does not mask dialogue; for a build use "a short ramped fade-up rather than a hard volume boost". [Krotos blog](https://krotos.studio/blog/what-is-sound-design-in-video-editing)
- Layer stack: low sweep, mid whoosh, top transient; transient shaping and short transient EQ make whooshes snap "without raising overall level"; automate pitch or filter to match speed; keep a dry and a wet version to choose on the timeline. [Krotos blog](https://krotos.studio/blog/what-is-sound-design-in-video-editing)
- Add a short impact (metal hit, punchy drum transient, reversed glass break) at the end of a whoosh to give a transition a landing point, especially for cuts to new scenes or title cards. [SFX Engine blog](https://sfxengine.com/blog/sound-design-tips-for-video-editors)
- Pair a riser with a hit for trailers, or with a soft click for UI milestones; layer a tight transient with deeper low end for punch; ambience as a base layer. [Pixabay blog](https://pixabay.com/blog/posts/free-and-high-quality-sound-effects-for-video-edit-453/)
- Pitch shift quality: beyond 4 to 5 semitones in either direction, use better algorithms. [Swell AI](https://www.swellai.com/blog/how-to-pitch-shift-in-audacity)
- Layering an octave-up copy with the original adds depth. [Unison](https://unison.audio/pitch-shifting/)
- Plain pitch shift changes duration unless time-corrected; most pro editors offer time-corrected pitch shift. [Adobe Audition time and pitch reference](https://helpx.adobe.com/cl/audition/desktop/effects-reference/time-pitch-manipulation-effects.html); [Abyssmedia](https://www.abyssmedia.com/audioretoucher/how-to-change-pitch.shtml)
- Extreme time stretching smears transients and adds metallic artifacts; rising pitch suggests approach or acceleration, falling pitch suggests moving away; low-mid body gives weight, keep high air non-piercing. [Sonilo whoosh guide](https://sonilo.com/ai-music/whoosh-sound-effect-guide)
- MKBHD team recording levels for voice (context for SFX headroom): average about -20 dB, peaks no higher than -12 dB. [Gistly summary of MKBHD team video](https://gist.ly/youtube-summarizer/master-video-editing-creative-choices-pro-tips)

### Inferences
- Using only part of a long file (the 73 s Freesound average means most files are longer than any UI move) is the default, not a trick: find the one clean transient or pass inside and cut around it.
- Pitch down a few semitones to make a light whoosh feel heavier for a big object, pitch up for small UI elements, as an application of the "low-pitched whoosh conveys mass" rule.

### Gaps
- No source gave dB targets for SFX relative to voice or music in YouTube or product edits (only "below the voice").

## 7. What separates professional from amateur sound in YouTube edits, product videos and motion graphics

### Takeaway
Across sources the pro signals are restraint, frame-accurate sync to visible events, weight that matches the object, variation instead of repetition, voice always clearest, and a mix checked on phone speakers. Amateur signals are a sound on every cut, the same swipe repeated, loud meme sounds, sounds that outlast the move, and music that fights the narration.

### Cited Findings
- Amateur: no audio on key interactions, music overpowering narration, abrupt audio cuts, a sound on every movement. Pro: deliberate timing, restraint, a balanced mix, checking playback on different devices. The real skill is "choosing the right sounds, timing them to the animation". An energetic soundtrack "can undermine a premium brand"; slow cinematic music can make a fast demo "feel sluggish". [Motion The Agency](https://www.motiontheagency.com/blog/sound-design-examples-before-after-in-motion)
- "The best sound design is unnoticed" (MKBHD team). [Gistly summary of MKBHD team video](https://gist.ly/youtube-summarizer/master-video-editing-creative-choices-pro-tips)
- Johnny Harris style: third-party analysis describes upbeat music under voiceover with SFX like door creaks, paper rustling and typing reinforcing an investigative tone; a Motion Array tutorial imitating the style adds an old camera or projector sound over animation and camera click sounds timed to each cut. Neither is Harris's own account; his Emmy-credited team included a sound design / composer (Tom Fox). [EditorDuel blog](https://blog.editorduel.com/blog/johnny-harris-high-retention-documentary-content); [Motion Array](https://motionarray.com/learn/premiere-pro/edit-documentary-in-premiere-pro/); [The Long Story substack](https://thelongstory.substack.com/p/why-the-best-journalists-on-youtube)
- Kurzgesagt uses a dedicated studio (Epic Mountain, Munich) for custom score and SFX per video rather than stock packs. [Kottke](https://kottke.org/18/01/the-soundtrack-to-kurzgesagt); [Kurzgesagt](https://kurzgesagt.org/youtube/)
- Effects off the beat of the music "feel random". [Videotto blog](https://videotto.com/blog/add-sound-effects-and-meme-edits)

### Inferences
- The top channels named in the brief (Kurzgesagt, Johnny Harris) use dedicated composers or sound designers, so "human" sound partly comes from sound written for the picture, not picked from a pack. For a solo editor using premade sounds, the closest equivalent is tuning or choosing sounds against the music key and the specific motion, and placing fewer of them.

### Gaps
- No first-hand quotes from editors of MKBHD, Ali Abdaal, Johnny Harris or Kurzgesagt about stock SFX selection were found. Reddit discussion (r/editors, r/VideoEditing, r/AfterEffects, r/MotionDesign, r/sounddesign, r/NewTubers) could not be accessed from this environment, so community consensus is unverified.
