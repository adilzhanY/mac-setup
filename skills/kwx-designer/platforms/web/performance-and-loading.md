# Performance and loading

Speed is part of the premium feel. A landing page that shifts, flashes unstyled text or waits for JavaScript feels cheap no matter how good the design is.

## Contents

1. Targets
2. The LCP element (usually the hero)
3. Layout shift
4. Fonts
5. Images and video
6. JavaScript and third parties
7. Perceived performance
8. Measuring without a browser
9. Review checklist

## 1. Targets

Core Web Vitals, measured at the 75th percentile of real visits, mobile and desktop separately (web.dev):

| Metric | Good | Poor |
|---|---|---|
| LCP, Largest Contentful Paint | 2.5 s or less | over 4.0 s |
| INP, Interaction to Next Paint | 200 ms or less | over 500 ms |
| CLS, Cumulative Layout Shift | 0.1 or less | over 0.25 |

Budgets for a mobile app landing page (aim, not law):

- HTML under 50 KB compressed, critical CSS under 20 KB, total JS under 100 KB compressed for the first view (zero is ideal for a static page).
- Hero image under 150 KB (AVIF/WebP), total first-view transfer under 500 KB.
- At most 2 font files on the critical path.

## 2. The LCP element (usually the hero)

LCP splits into 4 parts (web.dev targets): time to first byte about 40 percent, resource load delay under 10 percent, resource load duration about 40 percent, render delay under 10 percent.

- Prerender or server render the page; the hero headline and hero image are in the initial HTML.
- The hero image (the device screenshot) is an `<img>` in the HTML, not a CSS background or a JS-injected element, not `data-src`.
- `fetchpriority="high"` on that one image; never `loading="lazy"` on it. Lazy-load everything below the fold. More than 1 or 2 high priority images cancels the benefit.
- If the LCP is text (often on centred heroes), the font must arrive fast or the fallback must look right (section 4).
- **No entrance animation on the LCP element.** A headline that fades in from `opacity: 0` delays LCP and shows a blank page to screenshots, previews and slow devices (observed on Linear and Copilot Money captures).
- Avoid render-blocking scripts in `<head>`: `defer` or `type="module"`.
- Serve from a CDN with long cache headers on hashed assets: `Cache-Control: public, max-age=31536000, immutable`.
- Minimise redirects (ad and short links often add 2 or 3).

```html
<img src="/hero-800.avif" srcset="/hero-400.avif 400w, /hero-800.avif 800w, /hero-1200.avif 1200w"
     sizes="(min-width: 64rem) 560px, 80vw" width="1200" height="2460"
     alt="Flight card showing a 43 minute delay and its cause" fetchpriority="high">
```

## 3. Layout shift

- `width` and `height` (or `aspect-ratio`) on every image, video and iframe.
- Reserve space for anything that arrives late: cookie banner (overlay it, do not push content), announcement bar (render it server side or not at all), embeds, testimonials loaded from an API.
- Font swaps shift text: match fallback metrics (section 4).
- Price toggles, counters and timers: tabular numerals and fixed-width containers.
- Never insert content above what the user is reading.

## 4. Fonts

From web.dev font best practices and Chrome's fallback guidance:

- WOFF2 only. Subset to the scripts you need (Latin, plus Cyrillic or others only if the page uses them) and split by `unicode-range`.
- Self-host on the same origin as the page (no extra connection). If you use Google Fonts, `preconnect` to `fonts.googleapis.com` and `fonts.gstatic.com` (with `crossorigin`).
- Preload only the one font used by the LCP text: `<link rel="preload" href="/fonts/display.woff2" as="font" type="font/woff2" crossorigin>`.
- Inline the `@font-face` rules in `<head>`.
- `font-display`: `swap` for the display face used in the hero (with matched fallback metrics), `optional` for body text if a late swap would shift layout. Never `block` on a landing page.
- Variable font when you need 3 or more weights; otherwise 2 static files may be smaller.
- Match the fallback to kill CLS:

```css
@font-face {
  font-family: "Inter Fallback";
  src: local("Arial");
  size-adjust: 107%;          /* compute from the real font with Capsize or fontaine */
  ascent-override: 90%;
  descent-override: 22%;
  line-gap-override: 0%;
}
body { font-family: "Inter", "Inter Fallback", system-ui, sans-serif; }
```

Tools that compute these values: `fontaine`, `next/font` (automatic), Capsize. Values above are placeholders; compute real ones.

- Icons as inline SVG or an SVG sprite, not an icon font (icon fonts flash as wrong glyphs and shift layout).

## 5. Images and video

- AVIF first, WebP fallback via `<picture>`; PNG only for artwork that needs exact pixels (store badges ship as SVG).
- Export phone screenshots at 2x the displayed CSS size, not the native 3x device resolution; compress at quality 50 to 65 for AVIF.
- `srcset` with 3 to 4 widths and an honest `sizes`.
- Decorative backgrounds as CSS gradients instead of images where possible.
- Video: MP4 (H.264) plus WebM, `muted playsinline loop preload="none"` below the fold, a poster image, under 2 MB for a loop; start playback only when in view (IntersectionObserver) and never under reduced motion. Never a GIF for anything over a few frames.
- Device mockups: flatten the screen into the frame image once instead of compositing multiple PNGs at runtime.

## 6. JavaScript and third parties

- A marketing page should work with JavaScript disabled: content, links, badges and the FAQ (`<details>`) all native.
- Hydrate only interactive islands (toggle, waitlist form, video controls).
- Third-party scripts (analytics, chat, A/B testing, tag managers) are the main INP and LCP killers. Load analytics with `defer` or after `load`; avoid client-side A/B testing that hides the page until it runs (it causes flashes and slow LCP).
- Break long tasks; keep any single main-thread task under 50 ms.
- No scroll-jacking libraries; use CSS `scroll-snap` or native scrolling.
- Scroll-linked animation via CSS `animation-timeline: view()` where supported, not scroll event handlers.

## 7. Perceived performance

- Show the real layout immediately; skeletons only for data that loads later, and they match the final layout.
- Buttons respond within 100 ms (pressed state), even if the action takes longer.
- Optimistic UI for the waitlist form: show success instantly, roll back on failure.
- Test on iOS Low Power Mode and in Safari (Vercel): Low Power Mode throttles animation frame rates and video autoplay.

## 8. Measuring without a browser

- Lighthouse CLI: `npx lighthouse https://example.com --only-categories=performance --form-factor=mobile --output=json` (lab LCP and CLS; INP needs real users, lab uses Total Blocking Time).
- PageSpeed Insights API for field data (CrUX) once the site has traffic: `https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=...&strategy=mobile`.
- `web-vitals` library in production to collect real LCP, INP and CLS.
- Check transfer sizes with `curl -sI` and the build output; check that the hero image and headline exist in the raw HTML with `curl -s URL | grep`.

## 9. Review checklist

- [ ] Hero headline and hero image in the initial HTML; no fade-in on them.
- [ ] One `fetchpriority="high"` image; no lazy loading above the fold; lazy below.
- [ ] Every media element has dimensions; no late banners pushing content.
- [ ] Fonts: WOFF2, subset, self-hosted or preconnected, one preload, matched fallback, no `block`.
- [ ] AVIF/WebP with `srcset`; screenshots at 2x; video muted, poster, lazy.
- [ ] Page works without JavaScript; third parties deferred.
- [ ] Lighthouse mobile: LCP under 2.5 s, CLS under 0.1, TBT under 200 ms.
