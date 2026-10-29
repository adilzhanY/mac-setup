# Dashboards and data

"Designing a dashboard isn't that hard, but orchestrating one is" (Kole Jain, dashboard flaws). Three tells give away a designer who never built one: the data does not drive the form, everything is shown at once, and the invisible layer is missing. This file fixes all three, plus the chart and KPI rules from the vibe coded SaaS redesign.

Numbers marked (est.) were read off video frames, not stated.

## Contents

1. Let the data drive the form: the column rule
2. Chips
3. Numbers, text, people, time
4. Choosing the form: table, timeline, chart
5. Colour comes from the data
6. KPIs and metric cards
7. Charts
8. Progressive disclosure and the spectrum of explicitness
9. The invisible layer
10. Dashboard type and density
11. Before and after
12. Checks

---

## 1. Let the data drive the form: the column rule

For every column or field, decide its form from the kind of data, never default to plain text.

| Data kind | Form |
|---|---|
| Value from a small fixed set (department, status, category, severity) | Chip |
| Number (count, years, money) | Right aligned, tabular figures, header right aligned too |
| Person | Avatar plus first name; stacked avatars for several |
| Long free text (email, summary) | Truncate with ellipsis, full value on hover or tooltip |
| Point in time | Absolute plus relative: "Today, 2:13pm \| 4 hours ago" |
| Time range | "Apr 2, 3:26pm - Apr 3, 12:41pm"; open range "Apr 11 8:25am - Now" |
| Brand, source, browser, country | Real logo or flag beside the name |
| Inactive, archived, deactivated record | Whole row in lighter grey; status chip stays readable |

Column headers: a 16 px line icon before each label that hints at the type (# for numbers, calendar for dates, envelope for email, person for names). Reuse the same icon for that column in the sort, filter and group menus.

## 2. Chips

1. **Category chip**: a small coloured dot (about 6 px, est.) plus the label inside a pale neutral outlined pill. One stable hue per category, reused everywhere that category appears. Example: Finance green, HR orange red, Marketing purple, Sales blue, Engineering dark grey.
2. **Status chip**: tinted pill, icon plus word. "check Active" green text on pale green; "x Inactive" red text on pale red. Never colour alone.
3. **Severity chip**: a graded icon. Low one grey signal bar, Medium orange bars, High red bars, Critical a red warning triangle. Only High and Critical are red.
4. **Tag chip** for datasets or references: grey, no colour ("Employees", "EMP008").
5. Chips are scanned as shapes and colours, faster than words, because the set is small and learnable.

## 3. Numbers, text, people, time

- Right align numbers "so the digits align by place value". The eye then compares magnitude by length. Use `font-variant-numeric: tabular-nums` (or the platform equivalent).
- Truncate long emails ("alexreed@zipper.co...") so other columns get room.
- Build each `Intl.NumberFormat` once and reuse it; constructing one per cell is slow in a long table.
- Decimals: dim them where the integer matters most ("USD 293.00" with ".00" dimmed in the crypto app, Tim Gabe).
- Copy on hover: a small copy icon at the right end of a hovered cell, then a "Copied!" confirmation.

## 4. Choosing the form: table, timeline, chart

1. If the main dimension is time and events are few and rich, use a **vertical timeline**, not a time sorted table. Anatomy (Proposal Activity panel): an info banner on top ("This proposal is pending review..."), per event a status dot on a thin vertical line, a bold event title, a grey meta line "Today, 2:13pm | 4 hours ago", a bordered card with label/value rows (Submitted by, Datasets, Summary) and one quiet full width secondary button "Review proposal details" with an up right arrow.
2. Place a timeline in a sidebar pop out or as a second column beside the table, never on its own page. It can overlay the table with a dimmed backdrop.
3. If table data has a time dimension, add a **summary chart above the table**: the chart is the summary, the table is the detail.
4. A summary card is not a label: value list. Use logo, bold title, grey meta, accent on the one key number, implied labels (the Chipotle card, section 11).

## 5. Colour comes from the data

"Dashboard colors shouldn't just be sprinkled in to look nice. It should come from the data itself." Landing pages may use decorative colour; dashboards may not.

1. Every colour maps to a meaning: category identity, status, urgency, a data series, a brand logo.
2. Red only for urgent or destructive, so it still draws the eye.
3. Put colour into charts, sparklines, donuts, gauges, map dots, logos and flags, not into tinted icon discs, coloured card borders and bright buttons (Kole Jain, vibe coded SaaS: "we've added in much more relevant information and color through charts instead of buttons and icons").
4. Blur test: blur the screen; the only things still visible should be the meaningful colour signals (the blurred employee table kept only its chips).

## 6. KPIs and metric cards

1. Each metric lives in exactly one place. The LinkGuard app showed the same four KPIs three times (dashboard, sidebar tiles, other pages). Delete the copies; give the metric a home (Dashboard or an Analytics tab).
2. Prefer fewer, wider cards: 2 cards, each with a label and chevron ("Total Clicks >"), a large bold number bottom left (32,142), a thin sparkline filling the right half. Not 4 small tiles with an icon disc and a lonely number.
3. No decorative icon in a KPI tile. An icon must carry meaning (a device type, a brand, a status).
4. Small grey label above a large dark value for stats ("Projects 12", "Rating 4.87").
5. Do not show a KPI that duplicates the chart directly below it; drop KPI tiles and tab rows that repeat the charts.
6. A metric that is 0 on a new account is an empty state, not a big "0". Show what will appear and how to get it.

## 7. Charts

1. Pick the chart the data deserves: a line chart for a time series, a shaded map plus the numbers in a table on its left for geography, a segmented gauge or donut with a legend (count and %) for share of devices, a ranked list with logos for sources and browsers.
2. Single series bar chart (the incident summary): one hue (about #6E66F5, est.), one bar per day, x labels every second day in small grey text, two or three faint horizontal gridlines, no y axis line, no legend, a quiet "View all >" link top right.
3. Comparison: one large real time series with a segmented "Aggregate | Individual" toggle that splits it into one line per item (three colours, a legend of item names). "Super easy to implement and genuinely useful."
4. Per card controls at the top right: period dropdown ("Last Month") and an export icon.
5. Real data, real jaggedness. A single smooth decorative curve reads as fake.
6. Devices card example: semi circle gauge, "1735 Clicks" in the centre, legend Monitor 1341 76.1%, Laptop 217 13.4%, Mobile 124 6.2%, Tablet 53 3.4%.
7. Demographics card example: a country table with flags (Germany 842 41.2%, United States 641 35.4%...) left, hex dot world map right.

## 8. Progressive disclosure and the spectrum of explicitness

Visual hierarchy is what is big; disclosure hierarchy is what is shown vs hidden.

1. List every action. Rank it by frequency and importance. Place it on the spectrum:

| Level | Visibility | Example |
|---|---|---|
| 1 | Always visible global button | Share, Add + |
| 2 | Visible icon | Sort, Filter icon buttons with tooltips |
| 3 | Icon on hover, with tooltip | Remove user "x" on row hover, tooltip "Delete" |
| 4 | Hidden in a menu | Row menu: Copy, Comment, Insert row, Change data type, Link data, Delete row |

2. Remove user, three levels compared: hover "x" (chosen), always visible "x", a full red "remove" button on every row (visibly heavy). Reveal it "as soon as the user starts to look for that functionality".
3. Infrequent features go in a popover anchored to their trigger, not a new page. Share popover: invite field with "Can view" dropdown and black "Invite" button at the top (the primary action first), "General access", "People with access" with role dropdowns (owner row with a green shield), footer with the share URL and "Copy Link".
4. "New features or elements often don't require a dedicated page." Try a popover, drawer, hover state or menu first.
5. Apple Reminders: swipe reveals Details, Flag, Delete as secondary actions to checking off.

## 9. The invisible layer

"UI is as much about what you can see as what you can't see." AI generated dashboards miss it almost always. A data table needs all of these designed, not left to defaults:

- tooltips on every icon button (Sort, Filter, Group, Search, Settings): "what's missing pretty much unequivocally on all beginner dashboards are tooltips";
- tooltips or descriptions on ambiguous labels;
- sort popover: "Sort by", drag handle, Property select, direction select (A to Z), delete, "+ Add sort";
- filter panel: search field plus the column list with the header icons; filter conditions ("Employment contains");
- group by (Property, A to Z);
- row context menu and column menu (Edit title, Add description, Insert column, Change data type, Link data, Delete column);
- cell copy on hover; cell comments with a tiny amber corner triangle that opens a threaded card (author, text, reactions, Reply, "6 hours ago");
- share popover; feature announcement card ("New", date, preview, changelog rows); getting started checklist; onboarding tooltips anchored to real controls;
- empty, loading, error and first run states for every widget.

Menu styling: 16 px line icon left of each label, white card, about 12 px radius (est.), soft shadow, equal left and right padding.

## 10. Dashboard type and density

- Dashboard type scale: nothing above about 24 px. Example: 24 H1, 20 H2, 18 H3, 16 H4, 14 H5, 12 H6 (Kole Jain, every UI concept).
- Sidebar label example: 15 px font, 24 px line height, 24 px icons.
- Page header: small eyebrow with icon ("Private Database" with a lock), title (medium weight, about 2x body, est.), one line grey description, segmented tabs with a "+" to add a tab. Top right: "Edited 23 min ago" grey, Share, avatar, star, kebab.
- One black (or accent) pill primary per toolbar ("Add +"); everything else ghost icon buttons.

## 11. Before and after

| Before | After |
|---|---|
| Employee table: every cell plain black text, "Finance", "Active", left aligned years, full emails | Department chips with dots, status chips with icon and word, right aligned years, truncated emails, inactive rows greyed |
| Proposal activity as a table with a Timestamp column | Vertical timeline in a side panel |
| Incident table alone | Bar chart summary above the table, severity chips, avatars for reporters |
| Delivery card: "Restaurant: Chipotle / Item: Burrito Bowl / Day: Today / Time: 9:30am / Deliver To / Pickup From / Total Cost: $32.45", equal weight | Chipotle logo tile, "Burrito Bowl" bold, "Today 9:30am" grey, "$32.45" blue top right, two pins joined by a dotted line. Every label gone |
| 4 KPI tiles with icon discs, repeated on 3 pages | 2 wide cards with sparklines, one home |
| Analytics: KPI tiles, tabs, one smooth curve | One real chart with Aggregate / Individual, devices gauge, sources with logos, map with country table |
| Six bullet welcome modal | One tooltip on "Add +", then a corner checklist |

## 12. Checks

| Check | Pass when | Verify in code |
|---|---|---|
| Column forms | Each column renderer matches the table in section 1 | Read each column definition's cell renderer; none is a bare `{value}` for enums, numbers, people |
| Numbers aligned | Numeric cells and headers right aligned, tabular figures | `text-align: right`/`justify-end` and `tabular-nums` on numeric columns |
| Inactive rows | Row style branches on status | Find the row class/style condition |
| Colour has meaning | Every hue in the screen maps to a category, status, series or logo | List all colour tokens used on the screen and name the meaning of each |
| Red reserved | Red only on urgent, error, destructive | `grep` red/danger tokens; each hit is one of those |
| One home per metric | Each KPI component is rendered on one route | `grep` the KPI component usage |
| Tooltips | Every icon only button has a tooltip/accessible label | Search icon buttons without `title`/`aria-label`/Tooltip wrapper |
| Hidden layer exists | Sort, filter, row menu, empty and error states implemented | Check the components exist and are wired, not stubs |
| Dashboard type cap | No font token above about 24 px inside the app shell | Read the type tokens used in dashboard views |
| Explicitness ranked | Rare or destructive row actions are hover or menu, not always visible buttons | Count visible buttons per row: at most one or two |
