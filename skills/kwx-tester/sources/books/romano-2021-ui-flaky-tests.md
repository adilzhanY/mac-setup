# An Empirical Analysis of UI-based Flaky Tests

- Author: Alan Romano, Zihe Song, Sampath Grandhi, Wei Yang, Weihang Wang
- Year: 2021 (ICSE 2021)
- Legal URL: https://arxiv.org/abs/2103.02669

## What I read

The full paper (arXiv PDF): findings table, root cause table, fixing categories, relationship analysis.

## Key lessons used in web/e2e-flakiness.md, web/web.md, web/playwright.md

- 235 flaky UI tests from 62 projects (152 web, 83 Android).
- Async wait is the root cause of 45.1%; 52.0% on the web vs 32.5% on mobile; resource rendering is the largest subcategory (61).
- Layout differences are more common on the web (5.3% vs 1.2%); platform issues more common on mobile.
- Fixes: refactor logic 46.0%, delay fixes 39.3% (fix await mechanism 43, add or increase delay 21); delay fixes more common on the web.

## Mobile numbers (merged from the mobile agent's note)

## What I read

The arXiv PDF: Table I (findings and implications), Table IV (root cause categories with web and mobile counts), the root cause descriptions and the fixing strategy summary.

## Key lessons used in mobile/e2e-maestro-detox.md (also mobile/mobile.md)

- 235 flaky UI tests from 62 web and Android projects; 152 web, 83 mobile.
- Async wait caused 45.1% overall; 52.0% on web and 32.5% on mobile (mobile: resource rendering 14, animation timing 9, network loading 4, out of 83).
- Platform issues are more common on mobile (21.7% vs 10.5% web), which the authors link to Android fragmentation.
- Mobile: incorrect test runner interaction 14 of 83 (16.9%), incorrect resource load order 11 (13.3%), test order dependency 6 (7.2%).
- Fixes: refactoring logic 46.0%, fixing delays 39.3%; dependency fixes far more common on mobile (21.4% vs 1.3%); delay fixes less common on mobile (17.9% vs 32.2%), which the authors relate to Espresso's advice to disable animations.
