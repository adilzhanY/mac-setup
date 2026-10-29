# Practical Typography (Matthew Butterick)

- **Status:** free to read online (the author asks readers who benefit to pay what they think it is worth).
- **Legal source:** https://practicaltypography.com
- **Read:** "Summary of key rules", "Typography in ten minutes", "Why does typography matter", "Maxims of page layout", "Headings", "Letterspacing", "System fonts", "Websites" (October 2026).
- **Who recommends it:** a standard recommendation on Hacker News and in developer design threads; Butterick's earlier *Typography for Lawyers* is on the Stripe Design Team's reading list.

## Why it matters for premium UI

Butterick's core argument: typography protects reader attention, "the reader's gift to you. That gift is precious. And finite." Readers judge by appearance when attention is short; his example is two résumés with the same content, where the one with better typography gets the interview. Good typography does not replace substance, but "typography can make good writing even better."

## Key lessons

**Body text first.** Body text is most of any document, so it decides most of the quality. Four decisions shape it: point size, line spacing, line length, font.

| Setting | Rule |
|---|---|
| Size | 10 to 12pt print; 15 to 25px web |
| Line spacing | 120 to 145% of size; unitless in CSS (1.3 = 130%) |
| Line length | 45 to 90 characters average, about 2 to 3 lowercase alphabets |
| Font | a professional font is the fastest visible improvement |

**Emphasis and case**
- Bold or italic as little as possible; never both together.
- Never underline except links.
- All caps fine for under one line; add 5 to 12% letterspacing to caps and small caps (CSS 0.05 to 0.12em). Lowercase normally gets none, except text under about 9pt or large headlines that may need tightening. If the gap between letters could fit another letter, it is too much.
- Fake small caps are worse than none.
- Kerning always on.
- Centred text sparingly.

**Paragraphs**
- First line indent of 1 to 4x the point size, OR 4 to 10pt between paragraphs. Never both.
- Justified text always with hyphenation.

**Punctuation**
- Curly quotes; apostrophes point down; straight marks only for feet and inches.
- One space between sentences; no runs of spaces.
- Real ellipsis character; real trademark and copyright symbols.
- Do not confuse hyphens and dashes; never multiple hyphens as a dash.
- In a document over three pages, one exclamation mark is enough.
- Ampersands sparingly.

**Headings**
- 3 levels maximum, 2 better.
- Smallest visible size increase (for 12pt text, 12.5 or 13pt, not 14 to 15).
- A bold heading can be 0.5 to 1pt smaller to offset weight.
- Bold, not italic. No all caps. Emphasize with space above and below. Two levels of indent at most.

**Maxims of page layout**
1. Decide first how the body text will look.
2. Divide the page into foreground and background; secondary elements must not compete.
3. Make adjustments with the smallest visible increments.
4. When in doubt, try it both ways.
5. Be consistent.
6. Relate each new element to existing elements.
7. Keep it simple.
8. Imitate what you like.
9. Don't fear white space.

**Fonts**
- Avoid system fonts if you can, choose carefully if you cannot. Arial is "the sans serif of last resort". His tiers: A list tolerable (Avenir, Franklin Gothic, Gill Sans, Helvetica, Palatino, Charter, Optima...), B list in limited doses (Calibri, Futura...), C list questionable (Georgia, Cambria, Times New Roman...), F list fatal (Arial, Comic Sans, Papyrus, Verdana, Tahoma).
- On the web, system fonts have the advantage of native rendering.

**Web habits to drop** (2013 list): tiny body sizes, oversized headings, a handful of default fonts, dense blocks of navigation at the edges, layouts built from big blocks of colour. Treat the web as a typographic medium; borrow ideas from books, posters, art and software.

## Used in

`../../premium/typography-craft.md`, `../../premium/copywriting-and-tone.md`, `../../premium/restraint-and-reduction.md`.

## Additional pages read for the visual and web files

Also read on 2026-10-27: "Line length" (45 to 90 characters including spaces; "two to three alphabets" per line as a quick test; set the base measure with margins) and "Line spacing" (120 to 145 percent of point size; fonts that look small need less, large-looking fonts more; in CSS use unitless `line-height`). Used in `visual/typography.md`.
