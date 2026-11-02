# lychee README, linkinator README, html-validate CLI docs

- Author: lycheeverse; Justin Beckwith; html-validate project
- Year: 2026 (linkinator 8.1.0, html-validate 11.17.0)
- Legal URL: https://github.com/lycheeverse/lychee ; https://github.com/JustinBeckwith/linkinator ; https://html-validate.org/usage/cli.html

## What I read

The three documents, plus running linkinator and html-validate on a fixture site (verified).

## Key lessons used in web/performance-and-seo-checks.md, web/accessibility-testing.md

- lychee --offline with an absolute --root-dir, --include-fragments, .lycheeignore, --cache with --max-cache-age; no JS engine.
- linkinator serves a folder, --recurse, --check-fragments, --skip, JSON output, retry options; also checks external URLs found in pages.
- html-validate presets recommended, standard, a11y; --init writes .htmlvalidate.json; formatters.
