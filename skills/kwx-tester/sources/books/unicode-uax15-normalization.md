# Unicode Standard Annex 15: Unicode Normalization Forms

- Author: Unicode Consortium (editor Ken Whistler)
- Year: Unicode 18.0.0, revision 58, 2026-08-12
- Legal URL: https://unicode.org/reports/tr15/

## What I read

The forms, canonical versus compatibility equivalence, the stability guarantees, and the implementation notes (via a summary of the page).

## Key lessons used in exploratory/edge-case-catalogue.md and exploratory/i18n-and-localisation-testing.md

- NFC, NFD (canonical), NFKC, NFKD (compatibility: ligatures, circled digits and width variants are folded).
- W3C recommends NFC for all content.
- No form is closed under concatenation; normalise after joining.
- Compare strings only after normalising both; NFKC is lossy and should not be applied blindly to user text.
- Verified locally: é precomposed vs e + U+0301, й decomposes to и + U+0306, Kazakh ә has no decomposition.
