# Destinations: where the film will be shown decides its shape

Ask where the film will be shown before anything else (see "Ask first" in `SKILL.md`). The destination sets the length, the frame size, the frame rate, the loudness, where nothing important may sit, and sometimes what the film is allowed to show at all. A film that ignores its destination gets cropped, covered by buttons, rejected by a store, or turned down by a broadcaster.

## At a glance

| Destination | Length | Frame (px) | Frame rate | Loudness | The rule that matters most |
|---|---|---|---|---|---|
| Google Play preview | 30 s (only the first 30 s autoplay) | 1920x1080 or 1080x1920, no black bars | 60 or 30 | -14 LUFS | at least 80 percent real app experience, real app within 10 s, no call to action text, no fingers |
| Apple App Store preview | 15 to 30 s (hard limits) | 886x1920 or 1920x886 for current iPhones; 1200x1600 iPad | 30 max | -14 LUFS, plays muted by default | only screen captures of the app; no device frames, no hands, no people |
| TikTok | 15 to 30 s (5 to 60 s allowed) | 1080x1920 | 30 or 60 | -14 LUFS | keep text out of the bottom third and the right column |
| Instagram and Facebook Reels, Stories | 15 to 30 s | 1080x1920 (Meta also takes 1440x2560) | 30 or 60 | -14 LUFS | Meta's safe zone: 14 percent top, 35 percent bottom, 6 percent sides clear |
| YouTube Shorts | 15 to 60 s | 1080x1920 | 30 or 60 | -14 LUFS | the bottom quarter to third holds title, channel and subscribe |
| Snapchat | 3 to 10 s works best (3 to 180 s allowed) | 1080x1920 | 30 | -14 LUFS | about 150 to 230 px clear at top, 380 px at the bottom (swipe area) |
| Facebook and Instagram feed, LinkedIn | 15 to 30 s | 1080x1350 (4:5), or 1080x1080 | 30 | -14 LUFS | most viewers start muted; the story must work without sound |
| X | 15 to 30 s | 1920x1080 or 1080x1080 | 30 or 60 | -14 LUFS | as for feeds |
| YouTube video, launch film | 30 to 90 s | 1920x1080 (3840x2160 if 4K) | 60 | -14 LUFS | if it gets end screen elements, keep the last 20 s calm with space for them |
| YouTube ads | bumper 6 s (non skippable); in stream 15 to 30 s (skippable after 5 s) | 1920x1080, also 1080x1920 and 1080x1080 | 30 or 60 | -14 LUFS | brand and product in the first 5 s, before the skip button |
| Website hero, landing page | 6 to 15 s seamless loop | 1920x1080 or wider, under 5 MB | 30 | no audio track | muted, autoplay, loop, a poster frame; never put the message only in the video |
| TV and cinema spots | exactly 10, 15, 20, 30 or 60 s | 1920x1080 | 25 (Europe) or 29.97 (US), as the broadcaster asks | -23 LUFS (EBU R128, Europe) or -24 LKFS (ATSC A/85, US) | everything important inside the graphics safe area (90 percent); delivery to the broadcaster's own spec |
| Event screen, presentation | 30 to 90 s | the screen's size, often 1920x1080 | 60 | -16 to -14 LUFS | readable from the back of a room: bigger type, slower cuts |

Numbers for the social feeds come from measured overlays, not published constants, and the apps change their interfaces. Check a draft with `SafeZones` guides (below) and, when possible, in the app's own preview before publishing.

## Store previews are not commercials

Both stores want to see the product, not an ad about it.

**Google Play** (official guidance, Play Console help "Add preview assets"):
- The preview is a YouTube URL to a single video: public or unlisted, embeddable, not age restricted, with ads (monetisation) turned off.
- Only the first 30 seconds autoplay, muted. Keep it short.
- Show the real app or game within the first 10 seconds. At least 80 percent of the video should be the actual user experience; keep title screens, logos and cutscenes to a minimum.
- Landscape or portrait, whichever suits the app; no black bars beside a portrait video.
- No fingers or people tapping the device. Text overlays must be legible and must not be calls to action ("Download now" is out; Google Play awards are allowed). No time sensitive content.
- Captions help viewers who are deaf, hard of hearing or in loud places.
- The feature graphic is the video's cover image with a play button on it, so the two should belong together.

**Apple App Store** (App Store Connect app preview specifications, App Review Guideline 2.3.4):
- 15 to 30 seconds, up to 3 previews per device size and language, H.264 (10 to 12 Mbps, up to 30 fps) or ProRes 422 HQ, stereo AAC 256 kbps, 500 MB at most. The default poster frame is at 5 s: make that frame beautiful.
- Accepted sizes, not device sizes: 886x1920 or 1920x886 for every current iPhone group, 1080x1920 for home button Plus models, 1200x1600 for iPad, 1920x1080 for Mac and Apple TV.
- Previews may only use screen captures of the app itself, with narration and text or video overlays to explain what the footage does not show. Reviewers reject device frames, people, hands and promotional footage.
- Previews play muted by default, before the screenshots.

What this means for a store preview:

- The footage is real recordings of the real app, captured by the user or by the app's own UI tests (an instrumented test that walks through the flow, as many projects already have for screenshots). Never send taps or keystrokes to a device or emulator yourself unless the user says so.
- The craft moves into the edit: picking the moments, pacing, speed ramps, zooms into the recording (a scale and pan of the real frame, never a fake UI), captions that explain, transitions, music and sound.
- Allowed drawn elements: captions and short explanatory text, highlight rings or glows over a real control, a brief title at the start or the mark at the end (keep these under 20 percent of the time on Google Play). Not allowed: a drawn imitation of the UI standing in for the real one, device frames on Apple, hands, people, calls to action.
- A drawn commercial (the Bauwerk, torq and Sendoku films) belongs on YouTube, social feeds, the website and TV, not in a store's preview slot.

## Vertical feeds (TikTok, Reels, Shorts, Snapchat, Stories)

The app draws its own interface on top of the video: a caption and account name at the bottom, a column of buttons on the right, sometimes a header at the top. Anything important under those is lost.

- **Frame**: 1080x1920 (9:16). Render the master at that size; do not crop a 16:9 film to it.
- **Safe box** for text, faces, the product and the mark, at 1080x1920: x from 64 to 838, y from 260 to 1210. That is the conservative union of the platforms' overlays: about 14 percent clear at the top, 37 percent at the bottom (TikTok's caption area is the deepest), 6 percent on the left and 22 percent on the right (TikTok's button column). The kit's `SafeZones.tsx` draws it and each platform's own overlay.
- **Layout**: copy in the upper part of the safe box (y 260 to 640), the hero in the middle (y 600 to 1200), nothing that matters below y 1210. Above y 560 the right column is free on every platform, so a headline may run wider there. Backgrounds, the 3D world and motion can and should fill the whole frame; only meaning stays inside the box.
- **Type**: bigger than for 16:9, because the viewer holds the phone at arm's length: titles 96 to 132 px at 1080 wide, labels at least 40 px. Two to four words per line, left aligned to the safe box's left edge (x 64) or centred on it (x 451), never centred on the frame (x 540), which sits too close to the buttons.
- **Hook**: something moves in the first frame and the product is on screen by second 2. Viewers decide within two or three seconds. Do not open on a logo.
- **Sound off**: many feed viewers start muted, so the story must read without sound: copy carries every claim. TikTok users more often watch with sound, so the music still earns its place.
- **Length**: 15 s for an ad, up to 30 s when the story needs it. Loops are fine and often rewarded: let the last frame lead back into the first.
- **Rules**: Meta's Reels ads cannot carry licensed music (ours is synthesized, so this never applies), face effects or product tags.

## Square and 4:5 feeds (Facebook, Instagram, LinkedIn, X)

- 1080x1350 (4:5) takes the most room in a phone feed; 1080x1080 where 4:5 is not offered; LinkedIn recommends 4:5 and lengths of 15 to 30 s.
- Keep 60 px clear on every side for interface chrome and rounded corners; the bottom 10 percent may carry the post's own captions on some placements.
- Muted by default almost everywhere: captions and copy are not optional.

## YouTube

- **Videos and launch films**: 16:9, 1920x1080 at 60 fps (or 3840x2160). If end screen elements will be added, the film must be at least 25 s long and its last 5 to 20 s should be calm, with free space where the elements go (usually the right half). Keep the first 5 s strong: that is what the thumbnail preview plays.
- **Ads**: a 6 s bumper cannot be skipped; non skippable in stream spots are 15 s (up to 30 s on TV screens); skippable spots can be any length but the skip button appears at 5 s, so the brand and the product must be on screen before it. Cut the bumper and the 15 s from the master's strongest moments.
- **Shorts**: see vertical feeds.

## Website and landing pages

- A hero loop: 6 to 15 s, seamless (the last frame matches the first), no audio track at all, 1080p or less, under about 5 MB (H.264 MP4, plus WebM if the site serves it), and a poster image (the loop's best frame) for slow connections and for people who prefer reduced motion.
- The page's headline is HTML, never baked into the loop: the video is atmosphere and proof, the words stay readable and translatable.
- A full film on a product page is a 16:9 YouTube style film with sound, started by the visitor.

## TV and cinema

- Lengths are bought in fixed slots: 10, 15, 20, 30, 60 s. The film must be exactly that, and many broadcasters want the last half second or so silent and still.
- Frame rate follows the market: 25 fps in Europe (1080i50 or 1080p25), 29.97 in the US (1080i59.94 or 1080p29.97). Render at 60 and convert at the end (see pipeline).
- Loudness: Europe EBU R128, -23 LUFS integrated; the US CALM Act through ATSC A/85, -24 LKFS. True peak limits vary by broadcaster (from -1 to -3 dBTP); use their delivery spec, and when unsure master to -2 dBTP.
- Safe areas: keep all text and logos within the central 90 percent (graphics safe) and all important action within 93 percent (action safe).
- Delivery goes through the broadcaster's or clearance body's spec (in the UK the DPP commercials standard with a slate and clock, cleared by Clearcast; in the US an Ad-ID code). Claims are checked: every number in the film needs evidence. The skill makes the film and the master; the user's agency or the broadcaster handles clearance and delivery.

## Several destinations at once

Make one master for the main destination, then derive the rest:

- **Other sizes**: the same timeline rendered as another composition (`src/formats.ts`). Scenes lay out from `useVideoConfig()` width and height, so a vertical version is a re-layout, not a crop. Check every size with the guides on.
- **Shorter cuts**: a 15 s or 6 s cut is a new form in its own brief (`src/cuts/<name>.json`), built from the master's strongest acts. Copy it over `src/music.json`, rerun `cues.py` and `score.py`, render, and restore the master brief. The music for a cut is rescored for its length, not faded early.
- **Store previews** are a separate edit of real recordings (see above), sharing only the music's palette, the type and the mark.

## Sources

- Google Play preview assets (official): https://support.google.com/googleplay/android-developer/answer/9866151
- Apple app preview specifications (official): https://developer.apple.com/help/app-store-connect/reference/app-information/app-preview-specifications
- Apple Guideline 2.3.4 as quoted and enforced: https://www.flowjam.com/blog/app-store-preview-video and https://developer.apple.com/forums/thread/797679
- TikTok specs and safe zones (measured, approximate): https://www.trymypost.com/blog/tiktok-ad-specs-2026-safe-zones and https://emplifi.io/resources/blog/tiktok-ad-specs
- Meta Reels safe zone (14, 35, 6 percent): https://www.inro.social/tools/instagram-reels-safe-zone-checker and https://moda.app/resources/sizes/meta-reels-ad
- YouTube Shorts overlays (measured, approximate): https://postplanify.com/tools/youtube-shorts-safe-zone-checker and https://reap.video/blog/short-form-video-safe-zones
- YouTube ad formats: https://megadigital.ai/en/blog/youtube-ad-specs/ and https://support.google.com/displayvideo/answer/6274216?hl=en-GB
- Snapchat specs: https://wallaroomedia.com/blog/snapchat/snapchat-ad-dimensions-formats-specs/ and https://adkit.so/tools/safe-zones/snapchat
- LinkedIn video ads (official): https://www.linkedin.com/help/linkedin/answer/85306
- Sound off viewing: https://marketingdive.com/news/most-of-facebooks-8b-daily-video-views-happen-without-sound/419407
- Website hero video: https://elfsight.com/guides/video-background-website/ and https://swarmify.com/blog/how-to-make-an-autoplaying-background-video/
- Broadcast loudness and delivery: https://www.izotope.com/en/learn/the-mixers-guide-to-loudness-for-broadcast and https://www.thedpp.com/news/dpp-announces-tech-standards-for-hd-commercials
