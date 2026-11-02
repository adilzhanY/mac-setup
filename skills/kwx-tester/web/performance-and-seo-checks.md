# Performance and SEO checks for websites

The release checks for a website that are not about features: Core Web Vitals budgets with Lighthouse CI, JavaScript bundle size, broken links and anchors, HTML validity, meta tags, Open Graph and other things search engines and link previews read, and response headers. Most of these run without a browser, which makes them cheap, stable, and available to an agent even when browser automation is off. Only Lighthouse (and anything that renders the page) needs a browser. Deep performance and load testing of backends lives in the performance folder; this file is the web page side.

## Contents

1. Rules
2. Which checks need a browser
3. Core Web Vitals: thresholds, lab and field
4. Lighthouse CI
5. Bundle size
6. Broken links and anchors
7. HTML validation
8. Meta tags, Open Graph, robots and sitemap
9. Response headers: compression, caching, security
10. Checks

## 1. Rules

1. **Run every check that does not need a browser on every change**: links, HTML validation, meta tags, bundle size, headers. They are fast and never flaky. Evidence: opinion.
2. **Judge performance by budgets on the median of several runs, never one Lighthouse score.** "The median Lighthouse score of 5 runs is twice as stable as 1 run" (Lighthouse variability docs). Set `aggregationMethod: 'median'`; the default is `optimistic`. Evidence: moderate.
3. **Use the Core Web Vitals thresholds at the 75th percentile**: LCP 2.5 s or less, INP 200 ms or less, CLS 0.1 or less (web.dev). In the lab, use TBT as the stand in for INP, because Lighthouse "cannot measure INP, as there is no user input". Evidence: strong (Google field data basis).
4. **Lab numbers find regressions; field numbers tell you what users get.** Use Lighthouse CI to block regressions and real user data (CrUX, Search Console, the `web-vitals` library) to set targets. Evidence: moderate.
5. **Budget JavaScript size per route** and fail CI when it grows past the budget. Bytes shipped are the most stable performance number you can measure. Evidence: opinion.
6. **Check internal links on every build, external links on a schedule with a cache.** External sites fail randomly and should not block a merge. Evidence: opinion.
7. **Every public page has a unique title, a meta description, a canonical URL, `lang`, and Open Graph tags, and none of them points at localhost or a preview domain.** Evidence: moderate (ogp.me, search engine docs).
8. **Never upload private site reports to public storage.** Lighthouse CI's `temporary-public-storage` makes reports readable by anyone with the link. Use `filesystem` for private projects. Evidence: moderate (Lighthouse CI docs).

## 2. Which checks need a browser

| Check | Tool | Browser? | Agent can run when browsers are off? |
|---|---|---|---|
| Status codes, redirects, soft 404 | curl smoke test (`browser-automation-for-agents.md` section 7) | No | Yes |
| Internal links and anchors | lychee `--offline`, linkinator | No | Yes |
| External links | lychee with cache | No | Yes (network only) |
| HTML validity, some a11y rules | html-validate | No | Yes |
| Meta tags, Open Graph, canonical, robots, sitemap, JSON-LD | curl + HTML parsing | No | Yes |
| Bundle size | size-limit, build output | No | Yes |
| Compression, caching, security headers | `curl -sI` | No | Yes |
| LCP, CLS, TBT, Lighthouse categories | Lighthouse CI | **Yes** (headless Chrome) | No: write the config, CI runs it |
| INP and real user numbers | `web-vitals` in production, CrUX, Search Console | Field data | Read the reports only |
| Content rendered only by JavaScript (client only pages) | Playwright, Lighthouse | **Yes** | No. Static checks see only server HTML |

## 3. Core Web Vitals: thresholds, lab and field

Thresholds from web.dev, measured at the 75th percentile of page loads, split by mobile and desktop:

| Metric | Measures | Good | Needs improvement | Poor | In the lab |
|---|---|---|---|---|---|
| LCP, Largest Contentful Paint | Loading | 2.5 s or less | 2.5 to 4.0 s | over 4.0 s | Yes (Lighthouse) |
| INP, Interaction to Next Paint | Responsiveness | 200 ms or less | 200 to 500 ms | over 500 ms | No. Use TBT as the proxy |
| CLS, Cumulative Layout Shift | Visual stability | 0.1 or less | 0.1 to 0.25 | over 0.25 | Yes, for the load only (shifts after interaction are missed) |

Lab conditions: Lighthouse's default mobile run uses simulated "Slow 4G" (150 ms RTT, 1.6 Mbps down, 750 Kbps up) and a 4x CPU slowdown (Lighthouse throttling docs). That is deliberately slower than a developer's machine.

Field data:

- Production sites with traffic: PageSpeed Insights and Search Console show CrUX data (real Chrome users, 28 day window).
- Small sites without enough traffic for CrUX: send the metrics yourself with the `web-vitals` library (6.2.3):
  ```js
  import { onCLS, onINP, onLCP } from 'web-vitals';
  function send(metric) {
    const body = JSON.stringify(metric);
    (navigator.sendBeacon && navigator.sendBeacon('/analytics', body)) || fetch('/analytics', { body, method: 'POST', keepalive: true });
  }
  onCLS(send); onINP(send); onLCP(send);
  ```
  (snippet from web.dev, Apache 2.0.)

## 4. Lighthouse CI

Lighthouse CI (`@lhci/cli` 0.15.1, Lighthouse 13.6.0) runs Lighthouse several times per URL in headless Chrome and asserts on the results. It needs a browser, so under a "no browser for the agent" rule the agent writes the config and CI runs it.

`lighthouserc.json` for a static export or a plain static site (with `staticDistDir`, LHCI serves the folder itself and replaces the port in the URLs):

```json
{
  "ci": {
    "collect": {
      "staticDistDir": "./out",
      "url": ["http://localhost/index.html", "http://localhost/pricing/index.html"],
      "numberOfRuns": 5
    },
    "assert": {
      "assertions": {
        "largest-contentful-paint": ["error", { "maxNumericValue": 2500, "aggregationMethod": "median" }],
        "cumulative-layout-shift": ["error", { "maxNumericValue": 0.1, "aggregationMethod": "median" }],
        "total-blocking-time": ["error", { "maxNumericValue": 200, "aggregationMethod": "median" }],
        "categories:accessibility": ["error", { "minScore": 0.95 }],
        "categories:seo": ["error", { "minScore": 0.95 }],
        "categories:best-practices": ["warn", { "minScore": 0.9 }],
        "resource-summary:script:size": ["error", { "maxNumericValue": 300000 }]
      }
    },
    "upload": { "target": "filesystem", "outputDir": "./lhci-reports" }
  }
}
```

For a Next.js app with a server, replace `staticDistDir` with `"startServerCommand": "npm run start"` and full `http://localhost:3000/...` URLs, after `next build`.

```yaml
# .github/workflows/lighthouse.yml (shape from the LHCI getting started guide)
- run: npm ci && npm run build
- run: npx @lhci/cli@0.15.x autorun
- uses: actions/upload-artifact@v5
  if: ${{ !cancelled() }}
  with: { name: lhci-reports, path: lhci-reports/ }
```

Notes:

- Budgets: start from today's median plus a margin, then tighten. A budget nobody can meet gets turned off.
- `lighthouse:recommended` preset makes every non performance audit an error. Fine for a new site; noisy on an old one. Lighthouse 12 removed the PWA category, so the `no-pwa` preset matters only for old versions.
- TBT budget 200 ms is the mobile "good" Lighthouse scoring point; adjust to your measured baseline.
- Variability: CI runners are shared and noisy. The Lighthouse docs recommend at least 2 dedicated cores (4 better), not burstable or function as a service machines, and never several Lighthouse runs in parallel on one machine. Expect noise on free CI runners; that is why budgets use the median of 5.
- The accessibility category is a small axe subset. It does not replace `accessibility-testing.md`.

## 5. Bundle size

Bytes are deterministic: the same build gives the same size. That makes size budgets the most stable performance gate.

`size-limit` (14.3.0) with the file preset measures built files compressed:

```bash
npm install -D size-limit @size-limit/file
```

`.size-limit.json`:

```json
[
  { "name": "all client JS", "path": ".next/static/chunks/**/*.js", "limit": "350 kB", "gzip": true },
  { "name": "global CSS", "path": ".next/static/css/**/*.css", "limit": "40 kB", "gzip": true }
]
```

Run `npx size-limit` after `next build`; it fails when a limit is exceeded. For a static export point `path` at `out/_next/static/...`.

A no dependency check for any static output (gzip size of all JS):

```bash
find out -name '*.js' -print0 | xargs -0 cat | gzip -9 | wc -c
```

To find what grew: `@next/bundle-analyzer` (`ANALYZE=true next build`) opens a treemap (a local page). Under a "no browser" rule, read the JSON stats or the build output instead. Common causes: a date or icon library imported whole, a server only module pulled into a client component, a polyfill for a modern API.

## 6. Broken links and anchors

**lychee** (Rust, Arch package `lychee`; commands from the lychee README, not run here because it was not installed):

```bash
# internal links and #fragments in the built site, no network
lychee --offline --root-dir "$(pwd)/out" --include-fragments anchor-only --index-files index.html out/

# external links, weekly, with a cache so reruns are fast and kind to other sites
lychee --cache --max-cache-age 1d --accept '200..=299,429' out/
```

- `--root-dir` must be absolute, otherwise root relative links like `/about/` are reported broken.
- Put stable exclusions (LinkedIn, sites that block bots) in `.lycheeignore` as regex lines, each with a comment saying why.
- lychee has no browser engine: anchors created by JavaScript are not seen.
- GitHub Action: `lycheeverse/lychee-action`.

**linkinator** (Node, no install needed). Verified on a fixture site on 2026-10-31: it served the folder, found a missing page, a missing image, a missing `#pricing` anchor and an external 404 on an `og:image` URL:

```bash
npx linkinator ./out --recurse --check-fragments
npx linkinator ./out --recurse --skip "linkedin.com" --format json > links.json
```

Note that linkinator also checks external URLs found in the pages (including `og:image`), so a run needs network unless you skip them.

## 7. HTML validation

**html-validate** (11.17.0) runs offline on built HTML. Verified on a fixture on 2026-10-31:

```bash
npx html-validate --preset recommended,a11y "out/**/*.html"
```

It reported, with rule names: `doctype-style`, `wcag/h37` (img without alt), `element-required-attributes` (html without lang). It does not check heading order, contrast or meta tag content. Keep a `.htmlvalidate.json` in the repo (`npx html-validate --init` creates one) and turn off rules that fight the framework's output on purpose, with a comment.

Validating a page served by Next.js (server rendered): fetch it first, then validate the file.

```bash
curl -s http://localhost:3000/pricing -o /tmp/pricing.html && npx html-validate /tmp/pricing.html
```

The W3C Nu validator (`vnu.jar`, Java) is the reference checker; its public web service should not receive private pages.

## 8. Meta tags, Open Graph, robots and sitemap

What every public HTML page needs, checkable with curl and an HTML parser:

| Item | Rule | Why |
|---|---|---|
| `<html lang="...">` | Present and correct | Screen reader language, search, translation |
| `<title>` | Unique per page, under about 60 characters, names the page then the site | Tab title, search result title |
| `<meta name="description">` | Unique, one or two sentences | Search snippet, link previews fallback |
| `<meta name="viewport" content="width=device-width, initial-scale=1">` | Present, no `maximum-scale=1` or `user-scalable=no` (blocks zoom) | Mobile layout, WCAG 1.4.4 |
| `<link rel="canonical">` | Absolute URL on the production domain, never localhost or a preview host | Duplicate content |
| Open Graph | Required by ogp.me: `og:title`, `og:type`, `og:image`, `og:url`. Recommended: `og:description`, `og:site_name`, `og:image:alt`, `og:image:width`, `og:image:height` | Link previews in chat apps and social sites |
| `og:image` | Absolute URL, returns 200 with an `image/*` content type | Broken previews are invisible until someone shares the link |
| `twitter:card` | `summary_large_image` if you want large previews on X | |
| One `<h1>` | Exactly one, describes the page | Structure for search and screen readers |
| `robots` | No `noindex` on public pages in production; `noindex` on previews and staging | A leaked `noindex` removes the site from search |
| `/robots.txt` | 200, does not `Disallow: /` in production, points at the sitemap | |
| `/sitemap.xml` | 200, valid XML, lists only canonical 200 URLs | |
| JSON-LD | Parses as JSON, uses a real schema.org type | Rich results |
| 404 | Unknown paths return status 404, not 200 | Soft 404s get indexed |

The title test: for every public page in every language the title is non-empty, unique within its language, contains the brand name (or matches the spec's title pattern), and the home title has the brand plus what the product is. Present and unique is not enough (trial: web A's home title had no brand).

Quick curl checks (no browser):

```bash
BASE=http://localhost:3000
curl -s "$BASE/" | grep -oiE '<(title|meta|link)[^>]*>' | grep -iE 'title|description|canonical|og:|twitter:|viewport|robots'
curl -s -o /dev/null -w '%{http_code}\n' "$BASE/this-does-not-exist"          # expect 404
curl -s "$BASE/robots.txt"; curl -s "$BASE/sitemap.xml" | xmllint --noout - && echo "sitemap is valid XML"
OG=$(curl -s "$BASE/" | grep -oiE 'property="og:image" content="[^"]+"' | sed -E 's/.*content="([^"]+)"/\1/')
curl -sI "$OG" | grep -iE '^(HTTP|content-type)'                              # expect 200 and image/*
```

The full scripted version, which checks every listed page and fails with a list of problems, is the smoke test in `browser-automation-for-agents.md` section 7.

## 9. Response headers: compression, caching, security

```bash
curl -sI -H 'Accept-Encoding: br, gzip' https://example.com/ | grep -iE '^(HTTP|content-encoding|cache-control|strict-transport|content-security|x-content-type|referrer-policy|permissions-policy)'
curl -sI https://example.com/_next/static/chunks/main.js | grep -i cache-control   # hashed assets: long max-age, immutable
```

| Header | Expect |
|---|---|
| `content-encoding` | `br` or `gzip` for HTML, JS, CSS |
| `cache-control` on hashed static assets | `public, max-age=31536000, immutable` |
| `cache-control` on HTML | short or `no-cache` with revalidation, unless the page is truly static |
| `strict-transport-security` | Present on HTTPS production |
| `content-security-policy` | Present; no `unsafe-inline` for scripts if you can avoid it |
| `x-content-type-options` | `nosniff` |

These are production and preview checks. Local `next start` may differ from the hosting platform; check the deployed URL too.

## 10. Checks

| Check | Pass condition | How |
|---|---|---|
| Smoke test | All listed pages 200, 404 for unknown paths, head tags present | `python3 -I smoke.py $BASE / /pricing/` (see `browser-automation-for-agents.md`) |
| Internal links | 0 broken, anchors resolve | `lychee --offline --root-dir "$PWD/out" --include-fragments out/` or `npx linkinator ./out --recurse --check-fragments` |
| External links | Checked this week, failures triaged | scheduled lychee run with `--cache` |
| HTML valid | 0 errors | `npx html-validate --preset recommended,a11y "out/**/*.html"` |
| Bundle budget | Under limits | `npx size-limit` after the build |
| Lighthouse budgets (CI) | Median of 5 runs within budgets for LCP, CLS, TBT, script size | `lighthouserc.json` with `aggregationMethod: "median"`, `numberOfRuns: 5` |
| Reports private | No `temporary-public-storage` for private sites | `rg -n temporary-public-storage lighthouserc.*` |
| Titles | Every public page in every language: title non-empty, unique within its language, contains the brand; home title has the brand plus what the product is | a title test per language |
| Canonical and OG domain | No localhost or preview domain in canonical, `og:url`, `og:image` | smoke test |
| Indexing | No `noindex` in production, `noindex` on previews | `curl -s $PROD | grep -i noindex` |
| Headers | Compression on, hashed assets immutable, HSTS on production | `curl -sI` as in section 9 |
| Field data | INP, LCP, CLS at p75 known for production (CrUX or own `web-vitals`) | link the dashboard in the report |
