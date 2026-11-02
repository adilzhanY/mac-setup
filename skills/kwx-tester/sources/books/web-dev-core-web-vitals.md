# Web Vitals; Largest Contentful Paint; Interaction to Next Paint; Cumulative Layout Shift

- Author: Google Chrome team (web.dev)
- Year: 2024 to 2026
- Legal URL: https://web.dev/articles/vitals ; https://web.dev/articles/lcp ; https://web.dev/articles/inp ; https://web.dev/articles/cls

## What I read

The four articles.

## Key lessons used in web/performance-and-seo-checks.md

- Good thresholds at p75 split by mobile and desktop: LCP 2.5 s, INP 200 ms, CLS 0.1; poor above 4.0 s, 500 ms, 0.25.
- Lighthouse cannot measure INP; TBT is the lab proxy.
- web-vitals library snippet with sendBeacon.
