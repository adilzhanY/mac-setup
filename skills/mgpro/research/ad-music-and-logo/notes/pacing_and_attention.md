# Pacing and attention in short product and SaaS films (10 to 90 s)

Method note: besides web research, I measured 17 official launch films myself (downloaded from YouTube at low resolution, cuts found with ffmpeg's scene filter at thresholds 0.25 and 0.4, softer visual changes at 0.12, final seconds checked by eye on contact sheets). Scene detection counts hard cuts well but misses dissolves, morphs and continuous camera moves, so for "one continuous shot" films the cut count is near zero even though the picture changes a lot. Numbers below are labelled "own measurement" and link to the film.

## 1. Shot length and cut rate in modern tech and product ads

### Takeaway
There is no published cut-rate study for Apple, Linear, Stripe and similar launch films, so I measured them: hardware films (Apple, Google, Samsung) cut every 2 to 4 s on average, fast "feature parade" films (Figma Config, Arc) every 1.2 to 1.6 s, and SaaS UI films (Linear, Notion, Framer, Raycast) are mostly long continuous shots of 5 to 55 s with the change happening inside the shot. Hollywood films average under 4 s per shot and AI-assisted social "cinematic ads" about 1.2 s, so tech launch films sit between the two, with SaaS deliberately much slower.

### Cited Findings
- Own measurement, average shot length (ASL) at threshold 0.25 (threshold 0.4 in brackets), median shot, longest shot:
  - Apple "iPhone 17 Pro: The most powerful iPhone ever" (60 s): 25 cuts, ASL 2.3 s (3.5 s), median 1.6 s, longest 9.5 s ([YouTube](https://www.youtube.com/watch?v=TNhX1uR2vO8))
  - Apple "MacBook Pro" (60 s): 15 cuts, ASL 3.7 s (6.0 s), median 2.1 s ([YouTube](https://www.youtube.com/watch?v=JlS6RmAJKnE))
  - Apple "AirPods Pro 3" (48 s): 12 cuts, ASL 3.7 s (5.3 s), median 3.8 s ([YouTube](https://www.youtube.com/watch?v=EMmKs8vMKhU))
  - Apple "AirPods Max 2" (39 s): 3 cuts, ASL 9.6 s, median 9.3 s ([YouTube](https://www.youtube.com/watch?v=RrfJVP-6Quw))
  - Apple "iPhone 17: 3x More Scratch Resistant" (35 s): 3 hard cuts but 18 softer changes, about one visual change per 1.8 s ([YouTube](https://www.youtube.com/watch?v=PBrYMBacnyM))
  - Google "The Design of Google Pixel 9 Pro" (63 s): 36 cuts, ASL 1.7 s, median 1.5 s ([YouTube](https://www.youtube.com/watch?v=EFUP3pJDZhw))
  - Google "Introducing the Google Pixel 9 Pro" (30 s): 0 hard cuts; about 20 s of a Gemini prompt being typed, then the phone reveal and logo in the last 9 s ([YouTube](https://www.youtube.com/watch?v=OMVpP-Zam1A))
  - Samsung "Galaxy S24 Series: Design Film" (76 s): 21 cuts, ASL 3.5 s (8.4 s), median 2.1 s, longest 19 s ([YouTube](https://www.youtube.com/watch?v=ePdbj2bZ-Ro))
  - Figma "All the Launches at Config 2024" (80 s): 58 cuts, ASL 1.4 s, median 0.4 s, 8 cuts in the first 5 s ([YouTube](https://www.youtube.com/watch?v=0wCIP2Ox-EQ))
  - The Browser Company "Arc Max" (18 s): 14 cuts, ASL 1.2 s ([YouTube](https://www.youtube.com/watch?v=ttylMKwIe7c)); "Arc 1.0 | Everything or nothing" (34 s): 20 cuts, ASL 1.6 s ([YouTube](https://www.youtube.com/watch?v=n5Vwrj1gEWs))
  - Notion "Introducing the new Notion AI" (57 s): 11 cuts, ASL 4.7 s, median 3.3 s ([YouTube](https://www.youtube.com/watch?v=S92KX8-Hmlc)); "Introducing Notion AI" 2023 (85 s): 7 cuts, ASL 10.6 s ([YouTube](https://www.youtube.com/watch?v=FElBbgnNtVA))
  - Raycast "New Raycast. Coming 2026" (39 s): 7 cuts, ASL 4.8 s ([YouTube](https://www.youtube.com/watch?v=Mi173xGb0ZA))
  - Framer "All Design, No Code, Real Websites" (37 s): 3 cuts, ASL 9.2 s, one shot of 21 s ([YouTube](https://www.youtube.com/watch?v=6xJWQRVl9nw))
  - Linear "Introducing Linear Releases" (30 s): 0 hard cuts; one continuous camera drift over a branching release graph for most of the film, then a mono text card, a typewriter "RELEASES", "AVAILABLE NOW", logo ([YouTube](https://www.youtube.com/watch?v=6dIwFoQ0eVg)); "Introducing Linear Agent" (55 s): 0 hard cuts, 2 soft changes ([YouTube](https://www.youtube.com/watch?v=mRql2VJ99gM))
- A 2026 study of 99 social-media "cinematic ads" measured an average length of 17.9 s, 15.2 shots and an average shot of about 1.2 s, and says modern films average about 4 s per shot, so social cinematic ads cut about three times faster than films ([arXiv 2608.24329](https://arxiv.org/html/2608.24329))
- Cutting et al. measured 160 Hollywood films 1935 to 2010: ASL fell from about 10 s in the 1930s and 1940s to below 4 s after 2000; shorter shots now carry more motion per shot, an "amplifying effect" on viewer response; cuts pull the eyes back to screen centre, so fast cutting forces repeated reorientation ([Cutting et al., PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC3485803/))
- Google/Ipsos analysis of 5,000 TrueView ads (Oct to Dec 2018, 11 verticals): two or more shots in the first 5 s was a positive factor for ad recall and consideration (reported via Think with Google ABCD material; I could not open the primary PDF text) ([Think with Google ABCD reference](https://services.google.com/fh/files/misc/youtube_google_abcd_reference_guide_en.pdf); [Think with Google article](https://thinkwithgoogle.com/marketing-strategies/video/viewer-attention-for-youtube-ads))
- TikTok's own analysis of auction ads: gaming ads with 5 or more scenes had a 171% conversion lift over ads with fewer than 5; e-commerce ads with scene variety had a 38% lift over one person selling in a continuous shot (2021) ([Mobile Marketing Reads](https://mobilemarketingreads.com/?p=20237))
- Annie Lang's lab (2000): raising the edit rate from slow to very fast raised arousal, attention and memory without a large rise in cognitive load ([CityU Scholars](https://scholars.cityu.edu.hk/en/publications/the-effects-of-edits-on-arousal-attention-and-memory-for-televisi/)); but fast pacing combined with arousing content overloads processing, and verbal recognition (words, voice over) suffers first while visual recognition holds up (Lang, Potter and Bolls 1999 and a related limited capacity study, as summarised in search results; primary papers not opened, URL attribution uncertain: [bvsalud](https://busqueda.bvsalud.org/portal/resource/es/mdl-17763054))
- System1's Orlando Wood argues that "short, sharp cuts from lots of scenes thrown together with an emphasis on words and no real narrative" engage only the left brain and do not sustain attention; System1 counts these "left brain" features as more common and less effective ([Medium interview](https://medium.com/higher-order/picking-brains-and-lemons-with-orlando-wood-dafd135c57a3))

### Inferences
- Three distinct pacing families exist and a film should pick one: (a) hardware hero films, one product beat per 2 to 4 s cut; (b) launch "feature parades" and social cutdowns, 1 to 1.5 s per cut, often on the beat; (c) SaaS UI films (Linear, Framer, Notion, Raycast), few or no hard cuts, a continuous camera that carries 5 to 20 s, with motion inside the frame providing the rhythm. The perceived pace in (c) comes from how often something changes on screen, not from cuts.
- Lang's results suggest the danger with fast cutting is on the verbal channel: a 1 s cut rate is fine for pure visuals but too fast if each shot also carries words to read.
- A practical target for "never boring": some visible change (a cut, a new element, a camera direction change, a UI state change) every 1 to 3 s, even inside a long continuous shot.

### Gaps
- No published ASL or cuts-per-second study for tech launch films or motion graphics explainers was found; all named-brand numbers above are my own scene-detection measurements on single films, not averages across a brand's catalogue.
- Stripe Sessions 2024 film failed to download, so Stripe is not measured.
- No Frame.io Insider or No Film School article with measured numbers on product ads was found.

## 2. How long viewers need to read, understand a UI change or register an object, and when a hold gets boring

### Takeaway
Reading is the binding constraint: Netflix caps adult subtitles at 20 characters per second with a floor of 0.83 s, so a 5 word line (about 30 characters) needs at least 1.5 s, and practical motion design adds about 0.5 s on top. Seeing that something is there takes a fraction of a second, but remembering it takes about 0.5 s of attention, and brand memory starts building at roughly 1.5 to 2.5 s of active attention. Measured Apple and Samsung shots hold a single product view for a median of about 2 to 4 s, and the longest holds (9 to 20 s) only work because the camera or object keeps moving.

### Cited Findings
- Netflix English timed text guide: adult reading speed up to 20 characters per second, children 17; max 42 characters per line ([Netflix Partner Help](https://partnerhelp.netflixstudios.com/hc/en-us/articles/217350977-English-USA-Timed-Text-Style-Guide)); minimum event duration 5/6 s (20 frames at 24 fps), maximum 7 s ([Netflix General Requirements](https://backlothelp.netflix.com/hc/en-us/articles/215758617))
- Caption timing guidance assumes an average adult reading speed of about 238 words per minute, and as low as 50 wpm for low vision or dyslexia ([search result: engage.wsdot.wa.gov video text duration](https://engage.wsdot.wa.gov/video-text-duration))
- Digital signage rule of thumb: at least 1 s per word on a rotating slide, one main message of 15 to 20 words per screen at most; designers should be able to read their copy several times within the hold ([WireSpring PDF](https://www.wirespring.com/pdf/wirespring_2012DSE_contenthowto.pdf); [UMW Designing Digital Signs](https://dkc.umw.edu/tools/signage/))
- Potter (2012): viewers can detect a picture's meaning at 13 ms in a rapid stream, but memory for a scene stays weak unless it gets about 500 ms of processing ([Frontiers in Psychology](https://www.frontiersin.org/articles/10.3389/fpsyg.2012.00032/text))
- Amplified Intelligence (Karen Nelson-Field): the "attention memory threshold" is about 2.5 s of active attention before memory structures shift; about 85% of digital ads get less than that ([Advertising Week](https://advertisingweek.com/the-second-second-is-the-moment-that-matters-most-for-brands-right-now/)); a VCCP Media and Amplified report found brands with distinctive assets can build memory in about 1.5 s ([Creative Salon](https://creative.salon/articles/features/vccp-media-dr-karen-nelson-field-hacking-the-attention-economy))
- Webflow's animation course: stagger offsets of 0.1 to 0.2 s, and a brief pause after an action so viewers can process it before the next begins ([Webflow University](https://university.webflow.com/course-lesson/interactions-animations-sequencing-timing))
- Accessibility guidance: text should settle and become still within 5 s of motion ([Pearson accessibility pattern](https://ux.pearson.com/prototypes/accessibility-guidelines/patterns/pag/g25))
- Own measurement: median shot lengths of Apple hardware films are 1.6 s (iPhone 17 Pro), 2.1 s (MacBook Pro) and 3.8 s (AirPods Pro 3); Samsung S24 design film median 2.1 s; holds of 9 to 19 s only occur on continuous camera moves around the object ([YouTube](https://www.youtube.com/watch?v=TNhX1uR2vO8); [YouTube](https://www.youtube.com/watch?v=JlS6RmAJKnE); [YouTube](https://www.youtube.com/watch?v=EMmKs8vMKhU); [YouTube](https://www.youtube.com/watch?v=ePdbj2bZ-Ro))
- Own measurement: end title cards in Apple films hold the product name about 1 to 2 s, then the Apple logo about 2 s; Arc Max splits its tagline across two cards of about 1 s each ([YouTube](https://www.youtube.com/watch?v=TNhX1uR2vO8); [YouTube](https://www.youtube.com/watch?v=ttylMKwIe7c))
- Wistia: drop-off in the body of a video usually means viewers are bored; suggested fixes include varying location, removing title cards and using music to keep pace ([Wistia, Understanding Audience Retention](https://wistia.com/learn/marketing/understanding-audience-retention))

### Inferences
- Text hold formula consistent with the above: hold = max(0.9 s, characters / 15) + 0.5 s for entrance and settle. A 3 word headline (about 18 characters) gets about 1.7 s; a 7 word line (about 40 characters) about 3 s. Using 15 cps rather than Netflix's 20 leaves headroom for viewers who did not expect the text, and for animated text that is not readable until it settles.
- A UI change needs: about 0.5 s for the eye to land (cuts pull gaze to centre, per Cutting, so put the change near centre or lead the eye with a cursor or highlight), the change itself, then about 0.5 to 1 s of settled result. Roughly 1.5 to 2.5 s per UI beat.
- A static hold becomes a risk past about 3 s with nothing changing; continuous camera drift, a parallax layer or a second element entering resets that clock, which is how Linear and Framer sustain 15 to 20 s shots.
- A logo or product hero that must be remembered deserves at least 1.5 to 2.5 s of clean screen time, matching the attention threshold research and what Apple does.

### Gaps
- No controlled study was found on "seconds to understand a UI state change" or "seconds to register a 3D object" in ads; the figures above are derived from reading speed, scene gist and attention research plus measured practice.
- No study measured when a hold starts to feel boring in seconds; this is inferred.

## 3. "Show, don't wait": compressing process shots

### Takeaway
Editors compress long processes with elliptical cuts (show start and finish, skip the middle), jump cuts within one framing, montage under music, and speed ramps (slow on the key moment, fast through the rest). In motion design the same job is done by staggered starts of 0.1 to 0.2 s so many elements overlap, and by letting the camera keep moving while the process completes. Real examples in my sample: Pixel 9 Pro shows an AI prompt typing for about 20 s in one shot but keeps it alive by the text growing line by line, and Figma Config packs 8 cuts into the first 5 s with sub-second shots of individual features.

### Cited Findings
- Elliptical editing cuts out the middle of an action and lands later, leaving the viewer to infer the gap; montage builds meaning from a run of moments, often with music carrying the weight ([Filmdaft, Elliptical Editing](https://filmdaft.com/elliptical-editing-how-films-compress-time-into-seconds/))
- Jump cuts compress time without transition effects and add energy; pairing a speed ramp with a jump cut gives time dilation effects ([Filmora, What is a jump cut](https://filmora.wondershare.com/video-creative-tips/what-is-jump-cut.html); [Fiveable, time compression](https://frontend.prod.fiveable.me/motion-picture-editing/unit-6/time-compression-expansion-editing/study-guide/NNO4kcpBTSFElsXJ))
- Professional editors reviewing AI-made ads: rapid pacing "builds momentum" for energetic brands but "the jump cuts make it too intense" for calm ones; tiny camera shifts between near identical close-ups created a stutter one editor called "uncomfortable"; one editor recommended a slow to fast speed ramp on an opening shot rather than fast to slow ([arXiv 2608.24329](https://arxiv.org/html/2608.24329))
- Figma's help docs: a small offset turns a group of animations into an ordered sequence; the right value depends on each animation's length, object count and product pace ([Figma Help](https://help.figma.com/hc/en-us/articles/41239278373271)); short durations with long offsets read as discrete pops, long durations with short offsets as fluid overlapping trails ([UI/UX Atlas](https://uiux-atlas.pages.dev/lessons/motion/animation-choreography-and-sequencing))
- Staggering is the screen version of Disney's "overlapping action" principle ([CSS-Tricks](https://css-tricks.com/?p=255880)); one research paper notes its benefit for visual tracking has not been demonstrated, so it is convention rather than proven ([HAL](https://hal.inrae.fr/CRISTAL-MINT/hal-01054408v1))
- Cutting et al.: modern films pair short shots with more motion per shot, which amplifies viewer response ([PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC3485803/))
- System1 on a Lay's TikTok cutdown: the social version cuts straight to the climax and drops the backstory, and shows the product right away ([System1](https://system1group.com/ad-of-the-week/two-creative-choices-behind-lays-tiktok-triumph))
- Own measurement: Pixel 9 Pro intro holds a typing Gemini prompt for about 20 of 30 s with no cut, then reveals the phone and logo in the final 9 s ([YouTube](https://www.youtube.com/watch?v=OMVpP-Zam1A)); Linear Releases keeps one continuous camera drift for most of its 30 s ([YouTube](https://www.youtube.com/watch?v=6dIwFoQ0eVg))
- Getlago, describing Linear's launch films as a reference: no voice over, no stock footage, no abstract 3D shapes, the camera moving through the real product ([Getlago blog](https://getlago.com/blog/we-killed-our-motion-design-job))

### Inferences
- For an AI process (agent running, code generating, build progressing): show the trigger in full (about 1 s), then compress the middle with either (a) 2 to 4 elliptical jumps of 0.4 to 0.8 s each where each frame shows clearly more progress, or (b) one continuous shot with a speed ramp that runs the middle at 3 to 8x and slows to 1x for the result; then hold the result 1.5 to 2.5 s. The viewer needs to see the start state and the end state clearly; the middle only needs to prove it happened.
- Start the next action before the current one finishes (overlap of 0.1 to 0.3 s) so there is never a frame of dead waiting.
- Cut on action: let the cut fall during movement (a cursor click, a panel sliding), not after the motion has settled, so the eye carries across the cut.
- Avoid near identical consecutive framings when jump cutting; the editors flagged that as stutter. Change scale or angle noticeably between jumps.
- The Pixel example shows a long process can hold one shot if the content itself grows continuously (typed text) and the payoff is guaranteed; it works for a 30 s film only because the product reveal is the punchline.

### Gaps
- No primary article from Linear, Apple or another named studio describing their compression techniques was found.
- No quantitative study of speed ramps or stagger offsets on comprehension in ads was found.

## 4. Structure of high retention product films: hook, beats per 30 s, payoff, end card

### Takeaway
The first 2 to 3 s decide most of the outcome: Meta and Nielsen found up to 47% of campaign value comes from people who watched under 3 s, MediaScience found viewers decide go or no go within 2 to 3 s, and System1 with TikTok found brand cues in the first 2 s lift recall. Show the product or its effect, plus some on-screen text, in the opening seconds; aim for several distinct beats per 30 s; keep end cards short (about 2 to 4 s of title plus logo in the films measured).

### Cited Findings
- Facebook and Nielsen (2016, outside the 2018 date range but still the most cited figure): people who watched under 3 s of a video ad generated up to 47% of total campaign value, and under 10 s up to 74% ([MarTech](https://martech.org/even-brief-video-views-drive-brand-lift-facebook-nielsen-study-finds/); [Marketing Dive](https://marketingdive.com/news/brand-lift-happens-in-less-than-1-second-of-video-study-finds/377333)); sources disagree on whether the metric is "campaign value" or "ad recall"
- MediaScience: average skip at 8.72 s into a skippable :30 and 5.72 s into a :06; the go or no go decision happens within the first 2 to 3 s regardless of length ([search summary of RBR](https://rbr.com/is-the-power-of-06-ads-a-concern-for-broadcast-tv/))
- System1 and TikTok, 887 short-form ads, 92,000 viewers, 8 markets: brands that put recognisable assets in the first 2 s got better recall and engagement; exceptional early branding in creator ads gave 2.3x brand awareness lift and 3x brand image lift; plain logo overlays reduced brand awareness lift ("They recognize the brand but scroll along") ([Chief Marketer](https://chiefmarketer.com/system1-tiktok-study-branding-elements-and-creator-led-content-improve-short-form-video-ads/); [System1 blog](https://system1group.com/blog/you-vs-the-ad-she-told-you-not-to-worry-about-why-distinctive-creator-ads-win-on-tiktok))
- TikTok auction ad analysis: on-screen text in the first 7 s gave a 43% conversion lift; a text CTA making the next action clear gave 152% ([Mobile Marketing Reads](https://mobilemarketingreads.com/?p=20237))
- Google ABCD: introduce brand or product within the first 5 s; ads following the ABCD principles saw a 30% lift in short-term sales likelihood ([Google Business, ABCDs](https://business.google.com/us/resources/articles/abcds-of-effective-video-ads/)); earlier YouTube research found floating logos not on the product made people less likely to watch, and early logos raise recall but also skip rate ([search summary of Think with Google](https://www.thinkwithgoogle.com/intl/en-gb/consumer-insights/consumer-journey/skip-or-not-skip-what-keeps-people-watching))
- YouTube research: humour was the top trait for view-through, and emotional or suspenseful tones in the first 5 s were linked to higher recall ([Think with Google PDF](https://thinkwithgoogle.com/_qs/documents/1076/creating-youtube-ads-that-break-through-in-a-skippable-world_YcGhCSk.pdf))
- Wistia: the "nose" (first 2% of a video) loses on average 4.9% of viewers for 1 to 2 minute videos; fixes are a shorter intro, no intro graphics, and showing rather than stating. The tail drops when viewers sense the value is over, so avoid recaps, keep end logos short and place the CTA where the video really ends ([Wistia](https://wistia.com/learn/marketing/understanding-audience-retention))
- Editors reviewing AI ads complained a tagline arrived at "a very awkward point" and that viewers "don't know what this ad is for until the end" ([arXiv 2608.24329](https://arxiv.org/html/2608.24329))
- Own measurement of endings: Apple films end with product name about 1 to 2 s then logo about 2 s (iPhone 17 Pro, MacBook Pro, AirPods Pro 3); Notion new AI ends with a CTA card about 2 s, a symbol and "Think it." about 2 s, logo about 2 s (about 6 s in all); Figma Config builds its logo for about 2 s and holds about 4 s; Arc Max uses two 1 s tagline cards and a 1 s logo ([YouTube](https://www.youtube.com/watch?v=TNhX1uR2vO8); [YouTube](https://www.youtube.com/watch?v=S92KX8-Hmlc); [YouTube](https://www.youtube.com/watch?v=0wCIP2Ox-EQ); [YouTube](https://www.youtube.com/watch?v=ttylMKwIe7c))
- Own measurement of beat density (visual changes at threshold 0.12, merged within 0.25 s): Apple iPhone 17 Pro 29 changes in 60 s (about 15 per 30 s), Pixel 9 Pro design 39 in 63 s, Notion new AI 13 in 57 s (about 7 per 30 s), Raycast teaser 9 in 39 s, Linear Releases 1 in 30 s ([YouTube](https://www.youtube.com/watch?v=TNhX1uR2vO8); [YouTube](https://www.youtube.com/watch?v=EFUP3pJDZhw); [YouTube](https://www.youtube.com/watch?v=S92KX8-Hmlc); [YouTube](https://www.youtube.com/watch?v=Mi173xGb0ZA); [YouTube](https://www.youtube.com/watch?v=6dIwFoQ0eVg))
- Professional editors noted a music track that "stays at roughly the same energy level" with no crescendo or drop to mark the climax as a weakness ([arXiv 2608.24329](https://arxiv.org/html/2608.24329))

### Inferences
- A 30 s structure consistent with the evidence: 0 to 2 s hook showing the product or its effect with a short line of text (no slow logo intro); 2 to 22 s three to five feature or story beats of 4 to 6 s each (each beat made of 2 to 4 shots or UI changes); about 22 to 27 s payoff, the single most impressive moment, with the music peak on it; last 2 to 4 s product name and logo, plus CTA if the goal is action.
- Brand early but not as an overlay: let the product UI or object itself carry the brand cue in the first 2 s, since System1 found overlays underperform and Google found floating logos raise skips.
- Endings: keep the logo short (about 2 s) and do not recap; Wistia's tail data says viewers leave once they sense the content is over.

### Gaps
- No study counted "beats per 30 s" in high-performing ads; the beat counts above are my measurements on single films, not correlated with performance.
- I could not open Meta's own current creative guidance page; Meta figures come via trade press.
- TikTok's often quoted "63% of top ads deliver the key message in the first 3 s" appeared only in secondary blogs and is not included as a finding.

## 5. Is there a right length? Completion and effect by length and platform

### Takeaway
Shorter videos get higher completion, but completion is not effect: 15 s ads often match 30 s ads on branding in digital feeds, 6 s works best as a reinforcement of a longer ad, TikTok found 21 to 34 s ads converted best, and Wistia finds that under one minute videos are watched about half way while longer videos convert better. Choose length by goal and platform: 6 to 15 s for awareness and cutdowns, 15 to 35 s for feed ads, 30 to 90 s for launch films on YouTube, X or a website where viewers came on purpose.

### Cited Findings
- Kantar (Feb 2026) tested 15 s and 30 s versions of a Ritz Super Bowl ad on linear TV, Prime Video, YouTube and Instagram: "15 second spots can hit just as hard as 30s when the moment and the creative are right"; both did well on branding on YouTube and Instagram, while the 30 s excelled on linear TV and Prime Video ([Kantar](https://www.kantar.com/north-america/company-news/kantar-super-bowl-ad-study-15-second-ads-match-30-second-spots))
- FreeWheel Council and Realeyes (2018, 4,885 participants): used alone, 15 s ads were rated twice as effective as 6 s and 30 s ads; 6 s ads do better reinforcing a message already delivered by a longer ad ([search summary via MediaPost](https://www.mediapost.com/publications/article/319172/verbatim-executive-summary.html))
- ARF and MediaScience: 7 s ads were almost as effective on unaided recall as 15 s and about 60% as effective as 30 s, a diminishing returns pattern (reported in the same search; primary not opened) ([ARF](https://thearf.org/?p=359750))
- Google bumper meta-analysis (2016 data, outside the date range): over 9 in 10 of 122 bumper campaigns drove significant ad recall lift, averaging over 30% ([Tubefilter](https://tubefilter.com/2017/04/27/youtube-six-second-bumper-ads-statistics/)); a Vodafone case found a bumper plus master video gave 4x the ad recall of the master alone ([Think with Google](https://www.thinkwithgoogle.com/intl/en-cee/marketing-strategies/video/testing-creatives-vodafone-using-brand-lift-surveys))
- TikTok auction ads (2021): 21 to 34 s videos showed a 280% conversion increase versus shorter or longer ones; 9:16 gave a 91% increase versus black bars ([Mobile Marketing Reads](https://mobilemarketingreads.com/?p=20237))
- Wistia, based on 13 million videos (2026 State of Video report): videos under 1 minute average a 52% engagement rate (product videos 50%, testimonials 46%); under 1 minute is recommended for awareness and social, 1 to 5 minutes for education ([Wistia, optimal video length](https://wistia.com/learn/marketing/optimal-video-length))
- Wistia 2024 report: under 5 minute videos averaged 47% engagement, 5 to 30 minute 38%, over 30 minute 21%; shorter videos had the lowest conversion (2% for very short videos versus 17% for over 30 minutes); instructional content under 5 minutes had 2x the engagement of promotional content of the same length ([Chief Marketer](https://www.chiefmarketer.com/wistia-state-of-video-report-engagement-down-content-under-promoted/); [Wistia](https://wistia.com/learn/marketing/insights-state-of-video-report))
- Vidyard: 66% of viewers finish videos under one minute (2022 data on 1.78 million videos); 56% for 1 to 2 minutes ([MarketingProfs](https://www.marketingprofs.com/charts/2023/49949/business-video-benchmarks-retention-rates-by-length))
- LinkedIn's own guidance says to optimise length for completion and put the key message in the first 10 s; ads with an offer drive 1.2x the average completion rate ([LinkedIn 2018](https://business.linkedin.com/marketing-solutions/blog/video-marketing-/2018/take-your-marketing-to-the-next-level-with-linkedin-video-ads); [LinkedIn 2021](https://business.linkedin.com/marketing-solutions/blog/video-marketing-/2021/4-tips-for-better-video-ads-on-linkedin-in-2021)); a vendor benchmark of 342 LinkedIn video ads reports 35 to 45% completion under 15 s and 25 to 35% at 15 to 30 s ([ZenABM](https://zenabm.com/blog/linkedin-video-ads-benchmarks.md))
- Kantar South Africa Adtrack, over 6,000 ads: no difference in cut-through between 30 s ads and longer ads ([Bizcommunity](https://www.bizcommunity.com/Article/196/12/198591.html))
- Website hero videos: no rigorous study found; guides range from 5 to 7 s loops for buyers to 15 to 25 s for explorers, with 20 s or less a common institutional limit; one case reported mobile sign-ups fell 12% when a hero video replaced a still image (uncited) ([Artfolio](https://www.artfolio.com/article/choosing-the-right-hero-video-keep-visitors-scrolling-instead-of-bouncing-away); [WKU hero video standards](https://www.wku.edu/web-cms/hero-video-standards/); [ErgoSEO](https://ergoseo.com/blog/video-on-mobile-homepage-killing-engagement))
- Own measurement of official launch film lengths in the sample: 18 to 85 s, with most between 30 and 63 s (Apple 35 to 60 s, Linear 30 to 55 s, Notion 57 to 85 s, Arc 18 to 34 s, Figma 80 s)

### Inferences
- Length guide by goal and placement:
  - Feed ad, cold audience (Meta, TikTok, LinkedIn): 15 to 30 s master, with a 6 s cutdown for reinforcement; product in the first 2 s.
  - TikTok conversion: 21 to 34 s.
  - YouTube pre-roll: 15 to 30 s, with the hook and brand in the first 5 s, since the skip decision lands at about 5 to 9 s.
  - Launch film on X, YouTube or a launch page (viewers chose to watch): 30 to 60 s is the norm among Apple, Linear and Notion; go to 90 s only with a new beat at least every 5 to 6 s.
  - Website hero loop: 8 to 20 s, silent, readable without sound, loopable.
- Completion rate falls with length but conversion and depth can rise, so a 60 s launch film is not "worse" than a 15 s cut; make both from the same material.

### Gaps
- No platform-wide completion curves by second for 10 to 90 s ads were found from Meta, TikTok or LinkedIn themselves.
- Several frequently quoted numbers (Meta's 85% sound off, "up to 86%" hero video conversion lift, TikTok's 63% message in 3 s) could not be traced to a primary source and are left out of the findings.
- The Kantar 2026 study tested one brand's ad only, so its generality is limited.
