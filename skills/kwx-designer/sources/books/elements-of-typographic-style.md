# The Elements of Typographic Style (Robert Bringhurst)

- **Status:** paid book (Hartley and Marks, version 4.0, 2012, 398 pages). Not read in full.
- **What was read (legal):** Richard Rutter's *The Elements of Typographic Style Applied to the Web* (https://webtypography.net), which quotes and applies Bringhurst's rules section by section (2.1.2 measure, 2.1.6 letterspacing, 2.2.1 leading, 2.2.2 vertical rhythm, 3.1.1 type scale, table of contents); Maurice Meilleur's review in *Typographica* (https://typographica.org/typography-books/the-elements-of-typographic-style-4th-edition/); Wikipedia's entry.
- **Who recommends it:** on the Stripe Design Team reading list; called "the typographers' bible" by Hermann Zapf and "the finest book ever written about typography" by Hoefler and Frere-Jones; repeatedly recommended in Hacker News design threads.

## Core principle

"Typography exists to honor content." Typography must first draw attention to itself to be read, and then, to be read, give up the attention it has drawn. Read the text before designing it.

## Key rules (with Rutter's web translation)

**Horizontal motion (2.1)**
- Measure: 45 to 75 characters for a single column, 66 "widely regarded as ideal"; 40 to 50 for multiple columns.
- On the web, set the measure in ems (one character is about 0.5em, so 33em is about 66 characters) so it holds when the reader resizes text. Pixel widths change the measure when text size changes (400px gives 66 characters at 12px but 50 at 16px).
- Use ragged setting when it suits the text; one word space between sentences.
- Letterspace capitals, small caps and long digit strings by 5 to 10% of type size (CSS 0.05 to 0.1em). Do not letterspace lowercase without a reason.
- Kern consistently and modestly, or not at all. Do not distort letter shapes.

**Vertical motion (2.2)**
- Choose a base leading for the typeface, text and measure. Express it unitless (1.25 x 12pt = 15pt). On the web, values over 1.3 are common; Rutter uses 1.5. Negative leading only for short display text where ascenders and descenders cannot collide.
- Add and remove vertical space in measured intervals: every gap (paragraph, heading, image, sidenote) is a multiple of the base line height, so text returns to the same baseline grid. Example: 12px text on 18px lines, paragraph margins 18px; a 14px heading uses line-height 18/14 = 1.286 and margins of whole lines; asymmetric margins allowed if they sum to whole lines (1.5 above plus 0.5 below).

**Blocks and paragraphs (2.3)**
- Opening paragraphs flush left; later paragraphs indented at least one en (if indenting).
- Extra space around block quotations.

**Hyphenation and pagination (2.4)**
- At least 2 characters before a hyphen and 3 after; no more than 3 hyphenated lines in a row.
- Hard (non breaking) spaces in short numeric expressions.

**Harmony and counterpoint (3)**
- Don't compose without a scale. The classic scale of sizes survived about 400 years. Rutter's 16px application: 12, 14, 16, 18, 24, 36px.
- Titling (lining) figures with capitals, text (oldstyle) figures in running text.
- Spaced small caps for abbreviations in running text.

## Limits noted by the reviewer

Print focused. Web, CSS and display typography barely appear; screen type gets about two pages. It explains what good typography achieves more than how to get there. Read it, but "not first or alone": pair it with web specific sources (Rutter, Butterick, Apple's typography talks).

## Used in

`../../premium/typography-craft.md`.
