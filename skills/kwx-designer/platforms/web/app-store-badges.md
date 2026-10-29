# App Store and Google Play badges

Exact official rules, checked on 2026-10-27 against Apple's "Marketing Resources and Identity Guidelines" and Google's Partner Marketing Hub. Badge rules are legal terms of the artwork licences, not style tips: never modify the artwork.

## Contents

1. Official sources and artwork links
2. Apple: App Store badge rules
3. Google: Google Play badge rules
4. Using both badges together (the recipe)
5. Pre-launch: what you may show
6. Links, QR codes and Smart App Banners
7. Wording and legal lines
8. HTML template
9. Review checklist

## 1. Official sources and artwork links

| What | URL |
|---|---|
| Apple guidelines (badges, wording, device images, legal) | https://developer.apple.com/app-store/marketing/guidelines/ |
| Apple badge generator, short links, QR codes, embed code (50 localizations, black or white) | https://toolbox.marketingtools.apple.com/app-store/ |
| Apple "Download on the App Store" US/UK black SVG | https://developer.apple.com/assets/elements/badges/download-on-the-app-store.svg |
| Apple badge API (per language and colour) | `https://tools.applemediaservices.com/api/badges/download-on-the-app-store/black/en-us` |
| Apple pre-orders | https://developer.apple.com/app-store/pre-orders/ |
| Apple product bezels (device frames) | https://developer.apple.com/design/resources/#product-bezels |
| Apple trademark list | https://www.apple.com/legal/intellectual-property/trademark/appletmlist.html |
| Google Play badges (redirects to Partner Marketing Hub) | https://play.google.com/intl/en_us/badges/ |
| Google Partner Marketing Hub, lockups icons and badges ("Get it on Google Play" and "Pre-register on Google Play" folders) | https://partnermarketinghub.withgoogle.com/brands/google-play/google-play/lockups-icons-badges/ |
| Google Play English PNG (classic generator output, 646 x 250 with padding) | https://play.google.com/intl/en_us/badges/static/images/badges/en_badge_web_generic.png |
| Google approval form (TV, out of home, over 1M impressions) | https://partnermarketinghub.withgoogle.com/login/?next=/submit-assets/ |

Always download fresh artwork from these sources. Never redraw a badge in CSS or SVG yourself, never recolour, never use a badge from a UI kit or a random npm package.

## 2. Apple: App Store badge rules

Artwork

- Use only Apple's badge artwork. Variants: Download on the App Store, Download on the Mac App Store, Download on Apple TV, and Pre-order versions of each.
- Preferred: the **black** badge. The thin grey border around the black badge is part of the artwork; do not remove it.
- Alternative: the **white** badge, only when a single badge appears in the layout and black looks too heavy. **If any other platform's badge appears, use the black badge.**
- One-colour print is allowed only when black and white inks are not used in the layout.

Size and clear space

| Context | Minimum height | Minimum clear space |
|---|---|---|
| Onscreen | **40 px** | **one quarter of the badge height** on all sides (10 px at 40 px) |
| Print | **10 mm** | one quarter of the height |
| Very limited space (mobile banners) | legible on the target device | **one tenth of the badge height** |

"Select a size that is clearly legible but not dominant in the layout."

Placement and use

- **Place the App Store badge first** in a lineup of store badges.
- Place it in a subordinate position to the main image or message; it is not the hero artwork.
- **One App Store badge per layout or video.**
- Do not modify, angle, rotate or animate the badge. No hover scale, no shine sweep, no 3D tilt.
- Do not add symbols (TM, R) to the badge or to headlines.
- Do not use icons, logos or images from apple.com. Never use the Apple logo alone or in place of the word Apple.

Localization

- Apple provides "Download on the" / "Pre-order on the" translated into about 50 languages. "App Store" always stays in English.
- Never translate "App Store" or make your own localized badge. Match the badge language to the page language.

Device images and screenshots (often on the same landing page)

- Use Apple's product bezels, the latest generation devices, unmodified: no added reflections, no content coming out of the screen, no cropping or tilting or obstructing the device, no flipping or spinning animation.
- Minimum device size: 200 px tall onscreen, 25 mm in print; keep correct relative scale between devices.
- Copy goes beside device images, not on top of them.
- Screens show the app as it really runs, on the latest OS, with a full signal, Wi-Fi and battery status bar, fictional (not real people's) data, no blank screens, no Home Screen with third-party content.
- No 3D renders or illustrations of Apple products (except instructional material), no die-cut device shapes.

Licence

- The badge licence covers promoting **your apps on the App Store, while you are an Apple Developer Program member**. Apple may terminate it with 10 days' notice.

## 3. Google: Google Play badge rules

From the Partner Marketing Hub and the badge guidelines that accompany the artwork:

- Use the badges as provided. **Never alter them**: no recolouring, no rearranging or removing elements, no rescaling the wordmark or icon separately.
- **Minimum height: 28 px digital, 0.3 in (7.6 mm) print.** All text must be legible.
- **Clear space: one quarter of the badge height** on all sides.
- **The Google Play badge must be the same size as or larger than** other app store badges shown with it.
- Show it on a solid background or a simple image that does not obscure it.
- Match the badge language to the campaign language.
- **Any online use of the badge must link to the Google Play store.**
- **The badge can only be used to promote content available on Google Play.**
- Use the "Get it on Google Play" badge to drive downloads, the "Pre-register on Google Play" badge to drive pre-registration. Do not use Google Play logo lockups to drive downloads.
- Do not use outdated artwork or low-resolution files.
- Include the legal attribution when there is space: **"Google Play and the Google Play logo are trademarks of Google LLC."**
- Brand team review is required for TV commercials, out-of-home campaigns, and campaigns over 1 million impressions.

## 4. Using both badges together (the recipe)

The two rule sets combine into one testable layout:

1. Order: **App Store first, Google Play second** (Apple rule). In RTL pages the reading order still puts App Store first.
2. Colour: **both black** (Apple requires black when another badge is present; Google's badge is black).
3. Size: **the same visible height**, 40 px minimum (Apple's floor is higher than Google's 28 px). Recommended: 48 to 56 px in a desktop hero, 44 to 48 px on phones, 40 px in compact footers.
4. Gap: at least one quarter of the badge height between them (12 px at 48 px). 12 to 16 px is typical.
5. Clear space: nothing (text, other buttons, images) inside one quarter of the height around the pair.

**The padding trap.** Google's classic PNG (`en_badge_web_generic.png`, 646 x 250) has transparent clear space baked in: the visible badge is 564 x 168 with 41 px of padding on every side, so the visible badge is only about 67 percent of the image height. If you set both images to `height: 48px`, the Google badge looks a third smaller than Apple's, which breaks Google's "same size or larger" rule. Fix one of two ways:

- Use the unpadded SVG/PNG from the Partner Marketing Hub folder, and set both to the same height; or
- Keep the padded PNG and size it to `visible height / 0.672` (48 px visible means a 71 px tall image), compensating its built-in margin in the layout.

Measure with ImageMagick: `magick badge.png -format "%@" info:` prints the visible bounding box.

Apple's SVG has a 119.66 x 40 viewBox with no padding, so `height: 48px` gives a visible height of 48 px.

Other combination rules:

- Do not put the badges inside a button, card with its own fill that clashes, or a pill. Place them directly on the page background.
- Hover feedback: none on the artwork itself. A focus ring around the link (outside the clear space) is required for keyboard users and is not a modification.
- On iOS visitors' devices you may show only the App Store badge and on Android only Google Play (detect with the user agent), but keep both on desktop, and keep a way to reach the other store.

## 5. Pre-launch: what you may show

Neither Apple nor Google provides a "Coming soon" badge, and both forbid modifying badges, so **never write "Coming soon" on, over, or next to a greyed-out badge**, and never show a real store badge that links nowhere.

| Situation | iOS | Android |
|---|---|---|
| App live | "Download on the App Store" badge linking to the product page | "Get it on Google Play" badge linking to the listing |
| Store page exists for pre-order / pre-registration | "Pre-order on the App Store" badge (pre-orders can open 2 to 180 days before release for a new app; the app must pass App Review first) | "Pre-register on Google Play" badge linking to the listing |
| No store page yet | No badge. Plain text such as "Coming soon to iPhone" or "Coming to the App Store this spring" plus an email waitlist | No badge. "Coming soon to Android" plus the waitlist |
| Launched | Replace every pre-order badge with the download badge on the day of release (Apple requires it) | Swap to "Get it on Google Play" |

Notes:

- Apple advises not to print a release date in marketing if it might move; people who pre-ordered are not told by Apple about date changes.
- A pre-launch waitlist CTA is a normal button in your own style, never styled to look like a store badge.
- Wording in text should follow Apple's naming: "the App Store" with "the", never "Apple App Store" or "iOS App Store".

## 6. Links, QR codes and Smart App Banners

- App Store link: `https://apps.apple.com/app/id<APP_ID>` (country path optional, Apple redirects to the visitor's storefront). Generate short links and campaign tokens in Apple's marketing toolbox.
- Google Play link: `https://play.google.com/store/apps/details?id=<package.name>`; add `&hl=<lang>` to match the page language if needed.
- Desktop visitors cannot install from a click: show a **QR code** next to the badges on desktop (Apple's toolbox generates one; for both stores use a single smart link that redirects by platform). Label it "Scan to download on your phone". Hide it on mobile.
- iOS Safari Smart App Banner: `<meta name="apple-itunes-app" content="app-id=<APP_ID>">` in `<head>`. It shows a native banner with Open or Get, only in Safari on iPhone and iPad, only for a published app. Do not stack your own sticky install bar on top of it.
- Badges are links: `<a href>` with `rel="noopener"` when opening a new tab; most sites open stores in the same tab on mobile.

## 7. Wording and legal lines

Apple naming:

- Write "App Store" with capital A and S; "available on the App Store", "download from the App Store". Not "at the App Store", not "downloadable", not "the best App Store".
- "<App name> for iPhone", "works with Apple Watch". Not "iPhone <App name>". Never set Apple product names in all caps. Do not call devices "smartphones" or "tablets"; use product names. Do not translate Apple trademarks.
- Avoid mentioning iOS or macOS in marketing; name the devices.
- Never start a domain with an Apple trademark (`iphoneapp.com` is not allowed; `company.com/iphone` is).

Credit lines (once per site, wherever legal notices go, usually the footer):

- Outside the US, following Apple's template "___ and ___ are trademarks of Apple Inc., registered in the U.S. and other countries.": "Apple, the Apple logo, iPhone and App Store are trademarks of Apple Inc., registered in the U.S. and other countries." Apple requires crediting both Apple and the Apple logo when the badge is used; list every Apple trademark the page mentions (check each against Apple's trademark list). A translation of the notice is allowed outside the US, the trademarks themselves are not translated.
- US-only material may use the registered/unregistered form and TM/R symbols on first mention in body copy (never in headlines or on the badge).
- Google: "Google Play and the Google Play logo are trademarks of Google LLC."

## 8. HTML template

```html
<div class="store-badges" role="group" aria-label="Download the app">
  <a href="https://apps.apple.com/app/id0000000000">
    <img src="/badges/app-store-en.svg" alt="Download on the App Store"
         width="144" height="48">  <!-- 119.66:40 ratio -->
  </a>
  <a href="https://play.google.com/store/apps/details?id=com.example.app">
    <img src="/badges/google-play-en.svg" alt="Get it on Google Play"
         height="48">              <!-- unpadded artwork, same visible height -->
  </a>
</div>
```

```css
.store-badges { display: flex; flex-wrap: wrap; gap: 12px; padding: 12px; margin: -12px; }
.store-badges img { display: block; height: 48px; width: auto; }
.store-badges a:focus-visible { outline: 3px solid var(--focus); outline-offset: 4px; border-radius: 10px; }
@media (max-width: 30rem) { .store-badges img { height: 44px; } }
```

Badges are not the LCP element: `loading="eager"` in the hero (small SVGs), `loading="lazy"` in the footer.

## 9. Review checklist

- [ ] Artwork downloaded from the official source in the page language; not modified in any way.
- [ ] App Store first, both black, same visible height, 40 px or larger.
- [ ] Clear space of one quarter of the height on all sides and between badges.
- [ ] Google PNG padding accounted for (measured, not assumed).
- [ ] Each badge links to the real store listing; none shown before a listing exists.
- [ ] Pre-order / pre-register badges replaced at launch.
- [ ] No hover animation, tilt, shine or overlay on the badges.
- [ ] Alt text "Download on the App Store" and "Get it on Google Play".
- [ ] QR code on desktop only; Smart App Banner meta tag for the live app.
- [ ] Footer has the Apple and Google trademark lines.
- [ ] Device frames are Apple's bezels, unmodified, at least 200 px tall.
