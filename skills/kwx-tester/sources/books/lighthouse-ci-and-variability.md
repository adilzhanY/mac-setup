# Lighthouse CI getting started and configuration; Lighthouse variability; Lighthouse throttling

- Author: Google Chrome team
- Year: 2025 to 2026 (@lhci/cli 0.15.1, Lighthouse 13.6.0)
- Legal URL: https://github.com/GoogleChrome/lighthouse-ci/blob/main/docs/getting-started.md ; https://github.com/GoogleChrome/lighthouse-ci/blob/main/docs/configuration.md ; https://github.com/GoogleChrome/lighthouse/blob/main/docs/variability.md ; https://github.com/GoogleChrome/lighthouse/blob/main/docs/throttling.md

## What I read

The four documents.

## Key lessons used in web/performance-and-seo-checks.md, web/cross-browser-and-responsive.md

- staticDistDir or startServerCommand plus url; numberOfRuns default 3; presets all, recommended, no-pwa.
- aggregationMethod default is optimistic; median, pessimistic, median-run available.
- temporary-public-storage is public; filesystem target for private reports.
- 'The median Lighthouse score of 5 runs is twice as stable as 1 run'; dedicated cores, no burstable machines, no parallel runs on one machine.
- Mobile default: simulated Slow 4G, 150 ms RTT, 1.6 Mbps down, 750 Kbps up, 4x CPU.
