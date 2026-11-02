# axe-core README and jest-axe README

- Author: Deque Systems; Nick Colley and contributors
- Year: 2026 (axe-core 4.14.0, jest-axe 11.0.0)
- Legal URL: https://github.com/dequelabs/axe-core ; https://github.com/NickColley/jest-axe

## What I read

Both READMEs.

## Key lessons used in web/accessibility-testing.md, web/component-and-unit-tests.md

- axe-core finds 'on average 57% of WCAG issues automatically', aims for zero false positives, returns incomplete results for manual review, covers WCAG 2.0 to 2.2 A to AAA.
- color-contrast is 'known not to work with JSDOM'; jest-axe turns it off.
- jest-axe: disable the region rule for isolated components; real timers around axe calls; it 'does not guarantee that what you build is accessible'.
