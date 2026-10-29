# Data visualization basics

A chart is a sentence. Decide what it says, then remove everything that does not help say it. For full chart builds in this environment, also load the `dataviz` skill.

## Contents

1. Pick the claim, then the chart
2. Chart choice table
3. Proportional ink and axes
4. Colour in charts
5. Labels, numbers and text
6. Small charts on marketing pages
7. Interaction
8. Review checklist

## 1. Pick the claim, then the chart

Write the takeaway as one sentence first ("Delays dropped 40 percent after the update"). Use it as the chart title. A title like "Delays by month" makes the reader do the work.

## 2. Chart choice table

| Question | Chart | Avoid |
|---|---|---|
| Compare amounts across categories | Horizontal bar (sorted), dot plot | Pie with more than 3 slices, 3D bars |
| Change over time | Line (continuous), columns (few discrete periods) | Area stacks with more than 3 series |
| Part of a whole | Stacked bar, a single 100 percent bar, pie or donut only for 2 to 3 parts | Pie with 8 slices |
| Distribution | Histogram, box or violin, strip plot | Bar of means without spread |
| Relationship | Scatter plot | Dual y-axes |
| A single number | Big number with comparison ("+12% vs last week") and a sparkline | A gauge |
| Progress toward a goal | Bar or ring with the value printed | Speedometer |

People judge position and length most accurately, then angle, then area, then colour intensity (Cleveland and McGill, cited in Wilke). Prefer bars to pies and treemaps when precise comparison matters.

## 3. Proportional ink and axes

From Claus Wilke, Fundamentals of Data Visualization:

- Shaded area must be proportional to the value. **Bars on a linear scale start at 0.** A truncated bar axis is a lie.
- Line charts may start above 0, because they encode position, not length; label the axis clearly.
- Log-scale bars represent ratios and start at 1; for amounts on a log scale use dots, not bars.
- Showing change? Plot the change itself from 0, and say what is compared.
- Sort bars by value unless the categories have a natural order (months, ratings).
- Gridlines: light and few (3 to 5). Remove chart borders, background fills and 3D effects.

## 4. Colour in charts

- Three jobs: distinguish categories (qualitative), represent values (sequential or diverging), highlight.
- Qualitative: 3 to 5 categories work well; beyond 8 to 10 matching colours to a legend becomes a burden. Above about 8, label directly or group into "Other".
- CVD-safe qualitative palette (Okabe-Ito): `#E69F00` orange, `#56B4E9` sky blue, `#009E73` green, `#F0E442` yellow, `#0072B2` blue, `#D55E00` vermillion, `#CC79A7` purple, `#000000` black.
- Sequential: one hue (or a natural multi-hue ramp) running monotonically dark to light. Never a rainbow scale: its lightness jumps around and its ends look alike.
- Diverging: two sequential ramps meeting at a light neutral midpoint that means something (0, 50 percent, average). Avoid red vs green; blue vs orange or purple vs green work for most CVD types.
- Highlight: grey everything (`--gray-8`), colour only the series the title talks about with the accent.
- When the one value the title talks about is a failure, it alone takes the semantic error colour; everything else stays neutral. Draw the reference (baseline, target, previous version) as a dashed line.
- A claim across several metrics: normalise each to the baseline as 100% and label each bar end with both the share and the change ("47% · -53%").
- Thin lines and small dots need stronger colour than big areas; large areas should be calmer (lower chroma).
- Dark mode: re-tune chart colours for the dark surface (higher L, lower chroma), do not reuse light values.
- Test with a CVD simulator, and check the greyscale version still separates series.

## 5. Labels, numbers and text

- Label lines at their end instead of a legend when there are 4 or fewer series.
- Print the value on or next to bars when there are fewer than about 12.
- Tabular numerals in axes, tables and tooltips; right-align numbers in tables.
- Round to what the reader needs: 1.2M, not 1,213,442; 43 percent, not 43.27 percent.
- Format for the reader's locale (`Intl.NumberFormat`); units after the number with a non-breaking space.
- Compact numbers change length with the locale: `notation: "compact"` gives `1.5K` in English, `1500` in German and `1,5 Mio.` for 1.5 million. Never assume their width in a layout or a test, and show the exact value in the tooltip, because compact hides precision.
- Axis labels horizontal; if category names are long, switch to horizontal bars.
- Always state the source and time range in a caption. A chart that backs a claim also states n and the method ("39 tasks x 5 runs, geometric mean of per task medians") and how to reproduce it. An SVG chart carries a `<title>`.

## 6. Small charts on marketing pages

Landing pages use charts as illustrations of a promise ("Save 3 hours a week"). Rules:

- One chart per section at most, built from real or clearly illustrative data; label illustrative data as such.
- Strip axes to the minimum; keep the 0 baseline for bars.
- Animate the draw-in only once on first view, under 800 ms, and never under reduced motion.
- A big stat ("4.8 average rating from 12,000 reviews") often beats a chart. Always give the denominator and the source.

## 7. Interaction

- Tooltips on hover and on tap, with the exact value, the unit and the date.
- Hover targets for points of at least 24 px; use a voronoi or column hit area on line charts.
- Keyboard: series and points reachable, or a data table alternative below the chart.
- Provide a text summary for screen readers (`<figure>` with `<figcaption>`).

## 8. Review checklist

- [ ] Title states the takeaway.
- [ ] Bars start at 0; no dual axes; no 3D; no pie with more than 3 parts.
- [ ] 8 or fewer colours, CVD-safe, highlight by greying the rest.
- [ ] Direct labels where possible, tabular numbers, rounded values, units.
- [ ] Source and date range stated.
- [ ] Works in dark mode and greyscale; has a text alternative.
