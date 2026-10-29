# Landing pages

A landing page has one job: make the right visitor understand the product in seconds and take one action. For a mobile app that action is "install from the store" (or "join the waitlist" before launch). Everything on the page either explains, proves, or removes a doubt.

## Contents

1. What the research says
2. What great product sites do (observed)
3. Section by section blueprint (mobile app)
4. Hero in detail
5. Copy rules
6. Social proof rules
7. Visual and media rules
8. Mobile specifics
9. Pre-launch variant
10. Claim pages for dev tools, agents and B2B
11. Anti-patterns
12. Review checklist

## 1. What the research says

- **Attention is at the top.** NN/g eyetracking (2018): 57 percent of viewing time is spent in the first screenful, 17 percent in the second, 74 percent in the first two, 81 percent in the first three. Put the value proposition, the proof and the primary CTA in screen one.
- **Say what it is.** NN/g: a homepage tagline must explicitly say what the product does and for whom; a welcome message or a slogan wastes the best space.
- **Avoid false floors.** Full-screen heroes that end exactly at the fold make the page look finished. Show a cut-off element (a phone, the top of the next section) to signal more below.
- **Vague CTAs mislead.** NN/g's "Get Started stops users" study: users clicked "Get Started" expecting information, got funnels and quizzes, and stopped reading the page once they saw the button. Label the action specifically and give information before asking for data.
- **Price is a top information need.** NN/g: people leave sites that hide pricing. Show price or "Free, with optional Pro" near the main CTA, and link to the pricing section.
- **Social proof is remembered when it has faces.** CXL's social proof study: testimonials with photos were recalled significantly better than without; logos of well-known clients beat unknown logos; logos and bare numbers were not especially memorable. Place proof where doubt peaks: after the value proposition, before pricing, near the CTA.

## 2. What great product sites do (observed)

Studied on 2026-10-27 from live pages and screenshots (images not stored in the skill):

| Site | What to learn |
|---|---|
| Flighty (iPhone app) | Hero headline 6 words ("Get the truth when you travel"), one bold sans at about 72 px, subhead of 3 centred lines capped near 780 px. Awards row (Apple Design Award winner, App of the Year finalist) sits directly under the subhead, before the visual. Hero visual is a real app screen in a hand-held phone, surrounded by real notification snippets that tell the story without text. Nav has a quiet "Get the app" link instead of a badge. Feature sections each use a short benefit headline ("See why you're delayed. Finally!", "First to know. First to go."). A sticky segmented control (Preflight / At the airport / After landing / Download) turns features into a journey. Footer has "Compare" links against competitors. |
| Things (Cultured Code) | Extreme calm: icon, name, one paragraph, "Watch Introduction Video". The download section shows one card per platform (Mac, iPhone and Watch, iPad, Vision Pro) with requirements, price and one App Store badge each. Press quotes with publication logos as proof. |
| Raycast | Dark, centred, 2-line headline ("Your shortcut to everything."), 2-line subhead, one primary button with the platform icon ("Download for Mac") and monospace microcopy below it with requirements. Shows that a single CTA with requirements removes doubt. |
| Stripe | Left-aligned hero; two-tone headline (first sentence dark, the rest muted at the same size) gives hierarchy without a second size. Primary and secondary buttons side by side. Customer logo bar right at the fold edge. A live counter ("Global GDP running on Stripe") as proof above the headline. |
| Notion | Huge centred headline with one highlighted word in a tinted pill, one-line subhead, a primary "Get Notion free" plus a tinted secondary "Request a demo", then a real product screenshot cut off by the fold. |
| Copilot Money | Five award laurels in a row under the CTA ("Apple Design Awards Finalist", "Editor's Choice"). Hero text was captured mid fade-in: entrance animations make the hero illegible to previews and slow devices. |
| Linear | A third-party capture rendered only the navigation: the hero waits for JavaScript animation. Beautiful in a fast browser, blank elsewhere. |
| Structured | Full-bleed lifestyle video hero with no visible headline in the first screen: emotional but fails "say what it is". |
| Duolingo | Two stacked full-width buttons ("Get started", "I already have an account"): the returning user path is explicit. Bright brand colour reserved for the primary button. |
| Arc | arc.net now shows "A farewell to Arc" (sunsetting 22 December 2026); no longer a product landing reference. |

Common pattern among the best: one idea per screen, real product UI as the visual, proof within the first screen, short benefit headlines, generous space, one accent colour.

## 3. Section by section blueprint (mobile app)

Order for a consumer mobile app with a subscription. Each section has one job.

| # | Section | Job | Contents | Rules |
|---|---|---|---|---|
| 0 | Announcement bar (optional) | One timely message | "New: widgets for iOS 26" with a link | 1 line, dismissible, 36 to 44 px tall, not on first launch week if it pushes the hero down |
| 1 | Nav | Orientation | Logo (links home), 3 to 5 anchor links (Features, Pricing, FAQ, Support), one quiet "Get the app" link or button | Sticky, 56 to 72 px; no store badges in the nav; on mobile a menu button plus the app CTA |
| 2 | Hero | What it is, for whom, why, how to get it | Headline, subhead, store badges (+ QR on desktop), price line, rating or award line, real app screen in a device | See section 4 |
| 3 | Proof strip | Instant credibility | Star rating with count ("4.8 from 12,400 ratings on the App Store"), awards (Apple Design Award, Editor's Choice), press logos | Directly under or inside the hero; greyscale logos at one height (24 to 32 px); only true claims |
| 4 | Problem / promise | Make the visitor feel the problem | One sentence or a short before/after | Optional; skip if the hero already does it |
| 5 | Feature sections (3 to 5) | Show the main benefits | Each: benefit headline (3 to 8 words), 1 to 2 sentence body, a real screen or short muted loop | One benefit per section; alternate image left/right on desktop, stack image under text on mobile; screens at legible size |
| 6 | How it works (optional) | Lower perceived effort | 3 steps, each a verb ("Add a flight", "Get alerts", "Relax") | 3 steps, never 7 |
| 7 | Detail grid | Long tail of features | 6 to 9 small cards: icon, title, one line | Icons from one set, same size; this is where secondary features go |
| 8 | Testimonials | Remove doubt with people | 3 to 6 quotes with photo, name, role or context, and the source (App Store review, X, press) | Real quotes only; short (under 30 words); link to the source when public |
| 9 | Pricing | Answer "what does it cost" | Free vs Pro, monthly and yearly, trial terms, store badges again | See `pricing-pages.md`; on one-page sites this is a section, with a full page only if plans are complex |
| 10 | FAQ | Kill the last objections | 5 to 8 questions: cost, trial and cancel, privacy, platforms and devices, sync and data export, offline, support | `<details>` accordions; answers 1 to 3 sentences; link to help centre |
| 11 | Final CTA | Convert people who scrolled to the end | Restated promise in one line, store badges, QR on desktop | Same badges and order as the hero |
| 12 | Footer | Trust and legal | Product, Company, Support, Legal links; privacy policy, terms, imprint where required (Germany and Austria require an Impressum), contact email, trademark lines for Apple and Google, language switcher | Small but at least 13 to 14 px; links 44 px tall on mobile |

Length: most app landing pages need 6 to 9 sections. If a section does not change the visitor's mind, cut it.

## 4. Hero in detail

The first screen (at 1440 x 900 desktop and 390 x 844 phone) must contain all of:

1. **Headline**: what the app does or the outcome it gives, 3 to 8 words, sentence case. Display size 48 to 72 px desktop, 36 to 44 px phone, tracking about -0.02 em, `text-wrap: balance`.
2. **Subhead**: who it is for and how it works, 1 to 2 sentences, 15 to 30 words, 18 to 22 px, max about 50 to 60 ch, muted text colour.
3. **Primary action**: the two store badges (App Store first, both black, same visible height 48 to 56 px), per `app-store-badges.md`. On desktop, a QR code (96 to 128 px) labelled "Scan to download". Under the badges, one line of microcopy: price and requirements ("Free to download. Pro from $4.99/month. iPhone and Android.").
4. **Proof**: rating line or award laurels, small, directly above or below the CTA.
5. **Visual**: the real app UI in a device frame (Apple's official bezel for iPhone, unmodified), at least 200 px tall (Apple rule) and in practice 480 to 640 px tall on desktop. Cut off by the fold on purpose, to pull the eye down.

Layout options:

- **Centred stack** (Flighty, Raycast, Notion): headline, subhead, CTA, then the device below. Best when the headline is short and the product visual is strong.
- **Split** (Stripe style): text left (5 to 6 of 12 columns), device right. Best when copy needs 2 to 3 lines, and keeps the CTA higher on the screen.

Hero rules:

- The hero text is in the HTML and visible without JavaScript; no entrance animation on the headline (it becomes the LCP element). Animate the device or the notifications around it instead, and only under `prefers-reduced-motion: no-preference`.
- One primary action. A secondary action, if any, is a text link ("See how it works", scrolling to features).
- The hero background stays calm: a soft gradient, a tinted neutral, or a single brand colour field. No busy photo behind text.

## 5. Copy rules

- Headlines are benefits or outcomes, not feature names. Good: "Know about delays before the airline does". Bad: "Advanced flight tracking platform".
- Be specific with numbers: "Set up in 2 minutes", "Tracks 50,000 flights a day". Vague superlatives ("the best", "revolutionary") are invisible.
- One idea per headline, 3 to 8 words. Body text under each feature: 1 to 2 sentences.
- Write for scanning: a visitor reading only headlines understands the product.
- Use the visitor's words (from App Store reviews, support emails), not internal jargon.
- CTA labels say exactly what happens: "Download on the App Store" (the badge), "Join the waitlist", "Start 7-day free trial", "See pricing". Never "Submit", never a generic "Get started" that hides where it leads.
- Sentence case everywhere; no exclamation marks except one at most on the whole page.
- Legal and pricing microcopy is honest and complete: trial length, price after the trial, billing period, how to cancel.

## 6. Social proof rules

- Ranked by trust: (1) specific numbers with source ("4.8 from 12,400 App Store ratings"), (2) recognised awards (Apple Design Award, Editor's Choice, Google Play Best of), (3) named press quotes with logo, (4) named user testimonials with photo, (5) logo bars (B2B only).
- Show the rating count with the stars; a 5.0 from 9 ratings reads as fake.
- Every number and quote must be true and current; date the claims that age ("App of the Year finalist 2023").
- Use Apple award artwork only as Apple provides it for winners; do not invent laurels for "featured" placements you cannot document.
- Photos make testimonials memorable (CXL); keep quotes short and concrete ("It told me about the gate change 20 minutes before the airport did").
- Place proof next to the CTA and before pricing, not only at the bottom.

## 7. Visual and media rules

- Use real screens from the app, current version, with believable fictional data (Apple requires fictional data and full status bars).
- Each screenshot is large enough to read: phone screens at least 280 px wide on desktop. Crop to the part that proves the headline, rather than shrinking whole screens.
- Device frames: Apple's official bezels for Apple devices; for Android use a generic frame without Apple-specific details. Never tilt or crop Apple devices, never add reflections.
- Short muted loops (MP4/WebM, 3 to 8 s, under 1 to 2 MB) beat GIFs; poster image first, `playsinline muted loop`, paused under reduced motion, a pause button if it plays longer than 5 s.
- One accent colour for the whole page, used on CTAs and highlights. Backgrounds alternate between 2 neutral surfaces at most, plus one dark or brand-coloured band for emphasis.
- Illustrations, icons and screenshots share one style (radius, stroke, shadow).

## 8. Mobile specifics

Most visitors to a mobile app landing page are on a phone, often from a social link.

- Design the 390 px layout first. The hero fits: headline, subhead, badges and the top of the device within 844 px.
- On iOS, the Smart App Banner (`apple-itunes-app` meta) already offers "Get"; keep the in-page badges anyway.
- Detect the platform to emphasise the matching store badge, but never hide the other store completely (people share links across platforms).
- Hide the QR code on phones.
- A sticky bottom install bar is acceptable on mobile only if it is small (56 to 64 px), dismissible, does not cover content or the cookie banner, and is not combined with the Smart App Banner.
- In-app browsers (Instagram, TikTok) cannot always open the App Store directly: test the badge links there.

## 9. Pre-launch variant

Same blueprint, with these changes:

- Hero CTA: email waitlist (one field plus a button "Join the waitlist"), with "Coming soon to iPhone and Android" as text. No store badges until a store listing exists (see `app-store-badges.md` section 5). Once a pre-order or pre-registration listing exists, use the official "Pre-order on the App Store" and "Pre-register on Google Play" badges.
- Promise what the waitlist gets: "Early access and 3 months of Pro free". Say how often you will email.
- Proof: beta tester quotes, waitlist count (only if impressive and true), the team's credibility.
- Pricing: show the planned price or "Free with optional Pro" if decided; never invent a crossed-out "launch discount" price you never charged.
- Confirm signup inline, then on email (double opt-in in the EU).

## 10. Claim pages for dev tools, agents and B2B

Products with no screen worth showing (CLIs, agents, APIs, plugins) sell on a measured claim. Observed on the ponytail plugin's README cards (2026), one consistent card set:

- **Hero numbers:** product name, a one line claim, then three or four big signed numbers with one word labels ("-53% code", "-41% time"), rounded, against a named baseline. Method and sample in small type under them ("39 tasks x 5 runs, Opus 5.5").
- **Answer the fear under the numbers.** A claim of less raises "is it less safe?", so the next line answers it with a counter number: "98% of risky logic ships with a test. Without it: 68%."
- **A stat as a set:** a huge number, the baseline directly under it in small grey ("no skill: 68%"), a label sentence, a definition in parentheses ("a branch, a loop, a parser, money"), a method footnote.
- **Before and after card:** the user's request as a quoted eyebrow, a one sentence contrast headline, the losing version as a dim unreadable wall with a big grey count ("335 lines"), the winning version full and readable with a bright count ("10 lines"), the key token marked with an inline label, and a one line takeaway. Contrast is carried by brightness and size, not by red and green.
- **How it works as a ladder:** an eyebrow, the rule as a one sentence headline, one row per step with the question left and the action muted on the right, the last step in the only accent, and a footer line with the guarantees ("Validation, security and accessibility are never cut").
- **Real output, then the number:** show one real result in its exact format (a review finding with its severity and rows), then the stat it earns.
- **Hero art from the product's own material** when there is no UI to show: a portrait built out of real code, bright where the figure is and dim elsewhere.
- **One card system:** the same near black surface, one font family, one letter spaced eyebrow style, headlines as full sentences ending in a full stop, one radius, and one gradient kept for the brand word and the hero series only.
- **Translations:** ship each image in every supported language with the same layout, boxes sized for the longest translation.
- **Logos** in a light and a dark version, picked by theme.
- **Teaser banner** before launch: a path style eyebrow with a redacted token, a short curiosity headline, one outlined pill CTA ("Join the waitlist").

## 11. Anti-patterns

- Hero headline that is a slogan with no information ("Life, simplified.").
- Full-screen video or carousel hero with the message hidden in slide 3. Carousels hide content and slides beyond the first are rarely seen.
- Store badges with hover scale, rotation, glow, a custom colour, or a "Coming soon" overlay.
- Stock photos of smiling people holding generic phones.
- Screenshots too small to read, or mockups showing fake UI that the app does not have.
- Fake urgency (countdown timers that reset), fake scarcity, fake reviews, made-up user counts.
- Cookie banners that cover the CTA; chat widgets on a consumer app page.
- Ten feature sections of equal weight; every section with the same layout.
- Hero text that animates in from `opacity: 0`.

## 12. Review checklist

- [ ] First screen (desktop and 390 px phone): headline, subhead, badges, proof and the top of the product visual.
- [ ] Headline says what the app does, 3 to 8 words; subhead says for whom and how.
- [ ] Price or "free" stated near the CTA; trial terms honest.
- [ ] Proof with real numbers and sources in the first two screens.
- [ ] 3 to 5 feature sections, one benefit each, real screens, legible.
- [ ] Testimonials with photos and sources; FAQ with 5 to 8 real objections.
- [ ] Final CTA repeats badges in the same order and size.
- [ ] Footer: privacy, terms, imprint if needed, support email, Apple and Google trademark lines.
- [ ] Hero renders without JavaScript; LCP under 2.5 s on a mid-range phone (see `performance-and-loading.md`).
- [ ] One accent colour; consistent screenshot style; no em dashes or emoji in copy if the project forbids them.
