# Fundamentals of Data Visualization (Claus O. Wilke)

- **Status:** published by O'Reilly (2019); the complete text is free to read online by the author's choice.
- **Legal source:** https://clauswilke.com/dataviz/
- **Read (October 2026):** chapter 4 "Color scales" (color-basics.html), chapter 19 "Common pitfalls of color use" (color-pitfalls.html), chapter 17 "The principle of proportional ink" (proportional-ink.html).
- **Why chosen:** the standard modern, tool-agnostic reference for chart design, widely assigned in data science courses; it states rules with worked bad and good figures.

## Key lessons

**Three uses of colour.** Distinguish unordered groups (qualitative scale), represent values (sequential or diverging scale), highlight (accent scale: muted base, one strong accent). Every colour in a chart must do one of these; decorative colour is noise.

**Qualitative scales.** No colour dominant, none implying order. 3 to 5 categories work well; beyond 8 to 10, matching colours to a legend becomes a burden, so label directly or group. Okabe-Ito (8 colours) is the recommended CVD-safe set.

**Sequential and diverging.** Sequential runs monotonically dark to light, single hue or a natural multi-hue path. Diverging joins two sequential ramps at a light neutral midpoint that means something, balanced so both directions look equally strong.

**Rainbow scales are a pitfall.** Circular (ends look alike), non-monotonic lightness, so they hide some features and invent others.

**Colour vision deficiency.** About 8 percent of men and 0.5 percent of women. Red/green diverging scales fail for deutans and protans; blue/green fails for tritans. Colours must differ in lightness, not only hue. Small areas and thin lines make differences harder to see. Test in a simulator.

**Proportional ink.** Shaded area must be proportional to the value. Bars on a linear scale start at 0. Log-scale bars show ratios and start at 1; amounts on a log axis use dots. Area encodings (pie, treemap) are less accurate than length; prefer bars when precision matters.

## Where it is used in the skill

- `visual/data-visualization.md`: chart choice, proportional ink, colour scale rules, Okabe-Ito palette, highlight technique.
- `visual/color.md`: the colour-alone rule and CVD numbers.
