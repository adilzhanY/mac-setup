# The 3 dashboard UI flaws that give away you've NEVER built one

- Channel: Kole Jain
- URL: https://www.youtube.com/watch?v=Ksx9C2-3yMo
- Duration: 6:59
- Notes made from the auto transcript plus 114 still frames (40 scene-change frames, 52 frames at 8 second intervals, 22 targeted frames), read as contact sheets and at full size for the key UI.

## Core thesis

Making a dashboard look good is easy, orchestrating one so it works in use is the hard part. Three tells give away a designer who has never built one. First, the UI is not shaped by the data: every value is plain text in a generic table, colour is decoration, and time based data sits in a table instead of a timeline or chart. Second, everything is shown at once instead of using progressive disclosure, so secondary actions crowd the screen and onboarding is a six bullet modal. Third, the "invisible UI" is missing: hover chips, comment indicators, popovers, menus, tooltips, sort and filter panels, checklists and announcements that a finished product needs but a mockup never shows.

## Timestamped walkthrough

### 0:00 to 0:21 Intro
- Said: "Designing a dashboard isn't that hard, but orchestrating one is." UI that looks good vs UI that works when you use it. Three tells.
- Shown (0:04): close up of a table toolbar: icon buttons for sort (up/down arrows), filter (lines), group, search (magnifier), settings (sliders), then a black pill "Add +" primary button. A dark tooltip "Filter" sits above the filter icon on hover. Column headers each carry a small leading icon (calendar for Start Date, mortarboard for Education). Last column is a narrow "add column" icon plus a kebab.

### 0:22 to 1:14 Flaw 1a: let the data drive the form (tables)
- Said: dashboards exist to display data, so build the UI around the data. The "before" table is logically laid out but "nothing is driving the form".
- Shown, the demo app: a light SaaS "Employee Management System" page inside a white rounded window on a soft grey gradient. Breadcrumb top left (logo, Home > ... > employee-management-system), top right "Edited 23 min ago", a black "Share" pill with a chevron, a small "KR" avatar circle, star, kebab. Under a small "Private Database" lock eyebrow: title "Employee Management System" (medium weight, about 2x body size), grey subtitle "Employee tracking across all departments, salaries, responsibilities, and termination". Segmented tabs "Employees | Departments | Positions | Payroll | +" in a light grey track, the active tab is a white raised segment. Table columns: checkbox, Employees (EMP001...), Department, Email, Employment, # Years, First Name, Last Name, Start Date, Education. Every header has a leading 16px line icon.
- BEFORE (0:28 to 0:40): every cell is plain black text. Department reads "Finance", Employment reads "Active" or "Inactive", Years numbers are left aligned, emails are full length.
- Fixes, applied one at a time (0:41 to 1:03):
  1. Department becomes a chip: a small coloured square dot plus the label in a pale grey outlined pill. Colours per department: Finance green, HR orange red, Marketing purple, Sales blue, Engineering dark grey. Reason: there is only a set number of departments.
  2. Employment becomes a status chip: "check Active" in green text on a pale green pill, "x Inactive" in red text on a pale red/pink pill. Reason: a fixed set of statuses.
  3. Numbers right aligned "so the digits align by place value". A pink dashed redline at 0:56 marks the right edge the digits now share (3, 7, 2, 12, 1, 4...).
  4. Long text truncated with an ellipsis ("alexreed@zipper.co...", "finngray@zipper.co...") to give breathing room to other columns.
  5. Inactive or deactivated rows shaded out: the whole row (ID, chip, email, name, date) goes light grey, the Inactive chip keeps its colour but softer (1:03 frame: EMP008, EMP011, EMP012 greyed).
- Said: compare before and after, the after is more appealing and "is letting the data drive the form". At 0:52 a blurred version of the table shows that only the coloured chips survive the blur: a squint test that shows where colour carries meaning.

### 1:14 to 1:46 Flaw 1b: data that should not be a table at all
- Shown (1:19 to 1:24): "Proposal Activity" table: Activity ID (P-3205...), Description, Contributors (avatar stack plus names), Datasets (grey chips "Employees", "EMP008"), Summary (truncated), Timestamp ("Today, 2:13pm", "Mar 15, 4:26pm"...). The Timestamp column gets a pink highlight to show it is the real organising dimension.
- Said: the table works, but the time delineated nature means it is not the best format. Arrange it as a timeline.
- AFTER (1:32): a narrow vertical timeline panel "Proposal Activity" with a close X. A blue info banner on top: "This proposal is pending review. All changes are prepared and ready to be implemented upon approval." Each event: a status dot on a thin vertical line (green dot for the newest, grey chat icon, half filled circle), bold event title ("Proposal submitted to update employee contract information"), then grey meta "Today, 2:13pm | 4 hours ago" (absolute time plus relative time separated by a thin bar). Under each a bordered card with label/value rows: "Submitted by" avatar plus name, "Datasets" grey chips, "Summary" wrapped text, then a full width quiet secondary button "Review proposal details" with an up-right arrow.
- Said: this form factor can be tucked into a sidebar pop out or made a wider second column beside the table. Shown (1:40): the timeline docked as a right side panel beside the employee table, and later (6:36 to 6:44) as an overlay sidebar that dims the table behind it.

### 1:46 to 2:24 Colour comes from the data
- Said: "Landing pages, you can get away with a lot, but dashboard colors shouldn't just be sprinkled in to look nice. It should come from the data itself."
- Shown (1:51): a colourful illustrated crypto wallet landing page ("Your favorite crypto wallet.") as the contrast case where decorative colour is fine.
- Shown (1:56 to 2:12): "Incident Tracking" table ("All incidents and logs from software release v12.3.1", tabs Incidents | Reports | Charges). Columns: ID Number (with sort arrows), Severity, Incident, Reported by, Period, Incident Category.
  - Severity chip: signal bar icon plus word. Low (one bar, grey), Medium (orange bars), High (red bars), Critical (red warning triangle). Only the urgent levels get red, "the red icon in the chip draws your eye to it because the action is urgent".
  - Reported by: round avatar photo plus first name, because "your eye can associate who did what way faster than reading a name".
  - Period as a range: "Apr 11 8:25am - Now", "Apr 2, 3:26pm - Apr 3, 12:41pm".
  - Incident Category tinted chips: Software green, Engineering blue, Hardware grey, 3rd party amber.
- Said (2:10): "a pretty simple jump to adding a chart to roll up the data into a summary", because the data has a time dimension and the chart shows it instantly instead of hunting through a timestamp column.
- Shown (2:16 to 2:20): a card above the table with a single colour bar chart (one violet/indigo hue, about #6E66F5), one bar per day Jan 3 to Jan 31, x labels every second day in small grey text, two or three faint horizontal gridlines, no y axis line, no legend, a quiet "View all >" link top right. The table sits directly beneath it, so the chart is the summary and the table the detail.

### 2:24 to 2:39 Visual hierarchy vs disclosure hierarchy
- Shown (2:26 to 2:30): title card "2. Progressive Disclosure". A side by side labelled "Poor" vs strong:
  - Poor: a card listing every field as a two column label/value list with equal weight: "Restaurant: Chipotle / Item: Burrito Bowl / Day: Today / Time: 9:30am / Deliver To: Jamesville, NY / Pickup From: Syracuse, NY / Total Cost: $32.45". All same size and weight, labels left, values right.
  - Strong: the Chipotle logo as a dark rounded square app icon, "Burrito Bowl" bold as the title, "Today 9:30am" grey beneath it, "$32.45" in blue accent at top right, then a pickup to drop-off mini route: two location pin icons joined by a dotted vertical line, "Syracuse, NY" then "Jamesville, NY". The labels ("Restaurant:", "Item:", "Total Cost:") are dropped entirely because the format makes them obvious, and the restaurant name is carried by the logo.

### 2:34 to 3:37 Progressive disclosure and the spectrum of explicitness
- Said: another type of hierarchy is what you show vs what you hide.
- Shown (2:52 to 3:00): clicking the black "Share" pill opens a popover anchored under it (not a new page). Top row: email/name input "Email, name..." with an inline "Can view" dropdown and a black "Invite" button: the primary action, so it sits at the top and is immediately visible. Then "General access" section: icon tiles with two line items "Only those invited / 4 people" and "Link Access / Only users have link access". Then "People with access": avatar, name, email, a "can edit" dropdown on the right, the owner row shows "owner" plus a green shield. Footer row: the share URL "https://datasystems.co/file/Hf45rlf" and a black "Copy Link" button.
- Remove user, three levels of explicitness shown (3:08 to 3:24):
  1. Least explicit (chosen): on row hover a small red square "x" appears next to the role dropdown, with a dark tooltip "Delete".
  2. More explicit: the red x always visible.
  3. Most explicit: a full red "remove" labelled button on every row (3:16 frame, three stacked red buttons, visibly heavy).
- Said: since space is tight and removing a user is not a main action, reveal it "as soon as the user starts to look for that functionality".
- Shown (3:30 to 3:37): title "Spectrum of Explicitness", then a vertical gradient scale (green at top = always visible, through yellow, to red at bottom = hidden until hover) beside the table. A global always visible Share button sits high; a copy icon that appears on cell hover (a small copy glyph at the right end of the "BCom." cell) sits low.

### 3:38 to 4:19 Apple Reminders and onboarding as sequenced disclosure
- Shown (3:40): macOS Reminders, a row swiped to reveal "Details" (grey), "Flag" (orange), "Delete" (red), secondary to checking off the reminder.
- Said: onboarding is progressive disclosure. A first time user should not stare at a fully loaded dashboard. Start with a single tooltip on the most important action, then a second one or a simple checklist in the corner. "You're not hiding functionality, you're sequencing it." Compare a modal with six bullet points at login that is forgotten the moment it is dismissed.
- Shown (4:04 to 4:12, detailed at 6:12): a floating "Getting started checklist / Create your first database" card in the lower right corner, collapsible chevron. Done items have filled blue check circles and struck through grey text ("Start new data repository", "Define column structure", "Sync data", "Share database"), open items have empty dashed circles ("Create a tab", "Edit a filter"). A quiet "Watch tutorial" button with a play icon. Footer "4 of 6 complete" in blue with a blue progress bar.

### 4:20 to 4:59 Sponsor: Mobbin
- Said: the best way to learn disclosure, explicitness and onboarding flows is to look at a lot of real software. Mobbin curates hundreds of thousands of screens from real mobile and web apps, searchable by flow (for example Onboarding). It launched an MCP so the library can be pulled into AI development; he had it build a banking app mood board with real screenshots and links in about 2 minutes.
- Shown: Mobbin dark gallery (Shopify, Revolut, Attio, Wise, Airbnb, folk, Sana AI, Fey, Dovetail, OpenAI Platform, Mixpanel, PayPal, Bonsai, Stripe, Origin, Duolingo), a search menu with categories (Browsing Tutorial, Creating Account, Onboarding, Editing Profile, Logging In...), an "Onboarding" filter showing flows from Linear and Arcade. Cursor (the editor) with a Composer prompt asking for a mood board grouped by style. The result: "UI moodboard, 12 directions" (Minimal and light, Dark mode premium, Bold brand color, Playful 3D illustration, Card-centric, Investment and wealth, Savings pockets, Friendly neobank, Super-app finance, Corporate and B2B, Premium and ethical, Web dashboard). A Nu (Nubank) onboarding screen in purple.

### 5:00 to 6:30 Flaw 3: UI is what you can't see
- Shown (5:00 to 5:08): title cards "3. UI is what you can't see" and "UI is as much about what you can see as what you can't".
- Said: AI has a hard time with this. A dense table that looks good still needs extra functionality, and in a dense design it must live in UI you cannot immediately see.
- Shown, the hidden layer of the table:
  - Copy chip: a small copy icon appears at the right of the hovered cell ("Cole" row, 5:20).
  - Comment indicator: a tiny amber triangle in the corner of a cell; clicking opens a comment card "Michelle Reyes: Claire has requested we update a Masters in Science, as she finished her program 2 months ago. Let's fix that for her please!", with emoji reaction counts (3, 2), "Reply", "6 hours ago" (5:24).
  - Sort popover from the sort icon: "Sort by", a drag handle, "Property" select, "A to Z" select, trash icon, "+ Add sort" (5:16).
  - Filter by panel: search field "Filter by" then the column list with the same icons as the headers (Employees, Department, Email, Employment, Years, First Name, Last Name, Start Date, Education). At 5:40 a redline overlay shows equal pink padding columns on both sides and a magenta "16" spacing marker between rows.
  - The full inventory at 5:32 laid out on one canvas: comment card; dark toolbar tooltips "Sort, Filter, Group, Search, Settings"; a "New" announcement card (APR 3, attachments preview, "New Proposal Chat Files: Tedious long email chains are a thing of the past with new chat features", changelog rows "12 new integrations 03/24", "PDF document imports 03/04", "Agentic editing 02/21"); the getting started checklist; the share popover; Sort by; Filter by; a row context menu (Copy, Comment, Insert row, Change data type, Link data, Delete row); a column menu (Edit title, Add description, Insert column, Change data type, Link data, Delete column); Group by (Property, A to Z); a filter condition "Employment contains" with a Property select. Every menu uses 16px line icons left of the labels, white cards, about 12px radius, soft shadow.
- Said: "Here's all the UI that you can see and then this is all of the UI that you can't immediately see but is still there. And it's not a small amount." Putting pieces together (spacing, sizing) is not hard, orchestrating them takes thought. This applies to small items and to larger drawers, modals and elements with hidden components and states. New features often don't need a dedicated page, just better thought on how they are implemented.
- Said (6:00): think about moments you almost never see: an announcement of a newly launched feature, an onboarding pop-up. Shown (6:20): a dark onboarding tooltip anchored to "Add +": skeleton row illustration with a text cursor, "Add a row / Easily add or insert new rows into your data tables", "Dismiss" button.
- Said: "what's missing pretty much unequivocally on all beginner dashboards are tooltips". Assume users won't understand all your icons and may want more detail on ambiguous labels.

### 6:30 to 6:59 Recap
- The three flaws: the data driving the form, the right things hidden until they are needed, and all the invisible UI that makes the whole thing function. Figma assets used in the video are linked in the description.

## Extracted rules

Tables
1. For any column whose values come from a small fixed set (department, status, category, severity), render a chip, not plain text.
2. Category chips: a small coloured dot (about 6px square or circle) plus the label inside a pale neutral outlined pill. One stable hue per category, reused everywhere that category appears.
3. Status chips: tinted pill with an icon plus word, green text on pale green with a check for positive (Active), red text on pale red with an x for negative (Inactive). Never colour alone, always icon plus word.
4. Severity chips: a graded icon (signal bars 1 to 3, warning triangle for Critical). Only High and Critical get red; Low stays grey.
5. Right align every numeric column (counts, years, money) so digits align by place value. Use tabular figures. Right align the header too.
6. Truncate long free text (emails, summaries) with an ellipsis so other columns get room; keep the full value on hover or in a tooltip.
7. Grey out entire rows that are inactive, archived or deactivated (text in a lighter grey across the row), keeping the status chip readable.
8. Put a 16px line icon before every column header label that hints at the data type (# for numbers, calendar for dates, envelope for email, person for names). Reuse the same icon in filter, sort and group menus for that column.
9. Show people as avatar plus first name; use stacked overlapping avatars for multiple contributors.
10. Show time ranges as "Apr 2, 3:26pm - Apr 3, 12:41pm", and an open range as "Apr 11 8:25am - Now".
11. Show absolute plus relative time together: "Today, 2:13pm | 4 hours ago".

Choosing the form
12. If the main dimension of the data is time and events are few and rich, use a vertical timeline (status dot on a line, bold event title, grey meta line, detail card, one quiet action button) instead of a time sorted table.
13. Put a timeline either in a sidebar pop out or as a second column beside the table, not on its own page.
14. When table data has a time dimension, add a summary chart above it: single hue bars per day, faint gridlines, sparse x labels (every second day), no legend for a single series, a "View all >" link. The chart is the summary, the table is the detail.
15. For a summary card, drop field labels the format already explains. Use logo, bold title, grey meta, accent colour on the one key number (price), and a pin to pin route for from/to. Avoid the label: value list with equal weight.

Colour
16. On dashboards colour must encode data (urgency, category, status, identity). Do not add colour for decoration; that is a landing page privilege.
17. Reserve red for urgent or destructive things only, so it draws the eye where action is needed.
18. Squint or blur test: blur the screen; the only things still visible should be the meaningful colour signals.

Progressive disclosure
19. Rank every action by how often and how important it is, then place it on the spectrum of explicitness: always visible global button (high), visible icon, icon on hover with tooltip, hidden in a menu (low).
20. Infrequent features (share, settings) go in a popover anchored to their trigger, not a new page.
21. Inside a popover, the primary action (the invite field with role select and Invite button) goes at the top, immediately visible.
22. Secondary destructive actions in tight space (remove user) appear on row hover as a small icon with a tooltip, not a labelled button on every row.
23. Low level utility actions (copy a cell value) appear only on cell hover.
24. Onboarding: never a six bullet modal at login. Start with one tooltip on the single most important action, then the next, or a small collapsible checklist in a corner with progress ("4 of 6 complete" plus bar), done items checked and struck through.
25. Onboarding tooltips: dark card anchored to the real control, a small illustration of the action, short title ("Add a row"), one line of help, a "Dismiss" button.

Invisible UI (the finish checklist)
26. Every icon button gets a tooltip (Sort, Filter, Group, Search, Settings). Assume users will not understand your icons.
27. Every ambiguous label gets a tooltip or description.
28. A data table needs: sort popover (property, direction, add sort, delete), filter panel (search plus column list), group by, filter conditions ("contains"), row context menu (copy, comment, insert, change type, link, delete), column menu (edit title, add description, insert, change type, link, delete), cell copy on hover, cell comments with a corner triangle indicator and a threaded card, share popover, feature announcement card, getting started checklist.
29. Before adding a page for a new feature, try a popover, drawer, hover state or menu on the existing screen.
30. Menus: 16px line icon left of each label, white card, around 12px radius, soft shadow, equal left and right padding (redline shows matching pads, a 16 marker on spacing).

Shell and chrome details seen in the demo
31. Page header pattern: small eyebrow with lock icon ("Private Database"), title, one line grey description, then segmented tabs with a "+" to add a tab.
32. One black pill primary button per toolbar ("Add +", "Share", "Invite", "Copy Link"); everything else is ghost icon buttons.
33. Top bar right: "Edited 23 min ago" in grey, Share, avatar, star, kebab.

## Anti-patterns (tells) and fixes

- Every cell is plain text in the same weight. Fix: chips for enumerations, right aligned numbers, avatars for people, truncation, greyed inactive rows.
- Left aligned numbers. Fix: right align so place values line up.
- Long emails pushing columns wide. Fix: truncate with ellipsis.
- Inactive records look identical to active ones. Fix: shade the whole row.
- A time series stored as a time sorted table. Fix: timeline, or a summary bar chart over the table.
- Colour sprinkled to look nice. Fix: every colour must map to a data meaning; red only for urgent.
- Label: value card where every field has equal weight. Fix: logo, bold title, grey meta, accent on the key number, implied labels.
- Rare features given a permanent place or their own page (share panel bolted to the table side). Fix: popover on the trigger.
- Labelled red "remove" buttons on every row. Fix: hover x with a "Delete" tooltip.
- Fully loaded dashboard plus a six bullet welcome modal. Fix: sequenced tooltips and a corner checklist.
- No tooltips on icon buttons. Fix: tooltips everywhere an icon stands alone.
- A beautiful static table with no sort, filter, group, menus, comments or copy states. Fix: design the hidden layer as deliberately as the visible one.
- AI generated dashboards in particular miss the invisible UI.

## Quality checks before shipping

1. For each column: is the value from a fixed set (chip), a number (right aligned, tabular), a person (avatar), long text (truncate), a time (absolute plus relative, or range)?
2. Are inactive or archived rows visibly de-emphasised?
3. Is the primary dimension of this data time? If yes, is there a timeline or a chart instead of only a sorted table?
4. Blur the screen: do only meaningful colours remain? Is any colour decorative?
5. Is red used only for urgent or destructive states?
6. List every action, rank by frequency and importance, and check each sits at the right point on the spectrum of explicitness.
7. Is the primary action of every popover at its top?
8. Does every icon only button have a tooltip? Does every ambiguous label have help?
9. Inventory the invisible UI: hover states, sort, filter, group, row menu, column menu, copy, comments, share, empty and first run states, announcement, onboarding. Is each designed, not left to defaults?
10. Did any new feature get a new page when a popover, drawer or menu would do?
11. First run: does a new user see one clear next step instead of the whole product?

## Psychology / why it works

- Chips for enumerations are scanned as shapes and colours, faster than reading words, because the set is small and learnable.
- Right aligned numbers let the eye compare magnitude by length and place value without reading each digit.
- Avatars: the eye associates who did what faster from a face than from a name.
- Red draws attention, so it must mean urgency; used everywhere it stops meaning anything.
- A chart shows a time pattern instantly instead of making the user hunt through a timestamp column.
- Progressive disclosure reveals secondary actions exactly when the user starts looking for them, so the screen stays calm without losing power.
- Sequenced onboarding avoids overload; a front loaded modal is forgotten the moment it is dismissed.

## Cited resources

- Mobbin (sponsor, mobbin.com): curated library of hundreds of thousands of real mobile and web app screens, searchable by flow (onboarding etc.), recommended as the way to study progressive disclosure, explicitness and onboarding. Has a new MCP for pulling screens into AI coding; he used it to generate a banking mood board in about 2 minutes. 20% off via first description link.
- Apple Reminders (macOS/iOS): example of progressive disclosure, swipe reveals Details, Flag, Delete as secondary actions to checking off.
- Cursor (editor) with Composer: shown using the Mobbin MCP to build a "UI moodboard, 12 directions" for banking.
- Apps visible in the Mobbin gallery as references: Shopify, Revolut, Attio, Wise, Airbnb, folk, Sana AI, Fey, Dovetail, OpenAI Platform, Mixpanel, PayPal, Bonsai, Stripe, Origin, Duolingo, Linear (onboarding flow), Arcade (onboarding flow), Nu / Nubank (onboarding screen).
- Figma assets for every screen in the video: linked in the video description.
- His own earlier content on card hierarchy ("Often when I talk about hierarchy, I use examples like this"), referenced but not named.

## Memorable quotes

- "Designing a dashboard isn't that hard, but orchestrating one is."
- "Nothing is driving the form."
- "We right align the numbers so the digits align by place value."
- "Dashboard colors shouldn't just be sprinkled in to look nice. It should come from the data itself."
- "You're not hiding functionality, you're sequencing it so that the user is never overwhelmed."
- "UI is as much about what you can see as what you can't see."
- "What's missing pretty much unequivocally on all beginner dashboards are tooltips."
- "New features or elements often don't require a dedicated page."
