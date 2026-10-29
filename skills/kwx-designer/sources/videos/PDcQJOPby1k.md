# 5 SaaS UI/UX mistakes that SCREAM you Vibe Code

- Channel: Kole Jain
- URL: https://www.youtube.com/watch?v=PDcQJOPby1k
- Duration: 6:32
- Notes made from: the English auto transcript plus 134 timestamped stills (scene-change frames and one frame every 8 s), with about 25 key frames read at full size.

## Core thesis

AI builders (Cursor, Replit, Builder) produce apps that work but look generated, and the tells are predictable: emoji used as icons, AI-picked bright colours, the same KPI cards repeated on every page, gradient letter avatars, crowded rows of buttons and chips, sparse forms, cards that do nothing, and landing pages with no real graphics. Kole redesigns one real vibe coded URL shortener ("LinkGuard") step by step. The fixes are mostly subtractive and structural: swap emoji for an icon library, calm the colours, put colour into data (charts) instead of buttons and icon tiles, decide the layout yourself (what belongs on which page), collapse secondary actions into menus and popovers, and show the product itself as the landing page graphic. AI is good at logic when told, bad at complex layouts and cards, so layout is where a human gets the most change for the least time.

## Timestamped walkthrough

### 0:00 to 0:18 Intro
- Said: you build an idea in Cursor, Replit or Builder, it works but does not look good. He will redesign a real vibe coded URL shortener.
- Shown: app logos of Cursor, Replit, Builder.io. A wireframe skeleton of the dashboard. The "Link Tracking Platform" analytics end result. Reference sites flashing past as the quality bar: Linear ("Linear is a purpose-built tool for planning and building products"), Notion ("One workspace. Zero busywork."), Relume ("Websites designed and built faster with AI"), Resend ("Email for developers", serif headline, dark with a 3D cube render, then a yellow variant).

### 0:18 to 1:11 Mistake 1: emoji and AI colours
- Before (0:08, full frame): LinkGuard dashboard on a dark navy background (blue-black, around #070b14). Sidebar with two mini stat tiles (LINKS 2, CLICKS 0), sections PLATFORM / ORGANIZATION / ACCOUNT in small uppercase labels, a purple gradient circle avatar with the letter "J". Header row "Manage your links and view analytics" plus a bright green filled "+ Create New Link" button. Four KPI tiles in a row (Total Links 2, Total Clicks 0, Click Rate 0 /link, Active Links 2), each with a tinted icon disc (globe, bar chart, %, sparkle). "Your Active Links" list: each row has a green monospace short URL, a green "Verified Safe" chip with a checkmark emoji, a "Copy" chip with a clipboard emoji, then "eye emoji 0 clicks" and "calendar emoji 2026-01-03". On the right three buttons: white "bar chart emoji Analytics", dark "phone emoji QR Code", red-text "Delete".
- Said: "Get rid of the emojis." Notion uses them successfully, but swapping to professional icons already looks better. He likes Phosphor; Lucide or any interface icon library also works.
- Shown (0:20 to 0:24): zoom on the emoji (eye, calendar, bar chart, phone, wastebasket). Notion sidebar with emoji page icons shown as the exception where emoji work (user-chosen page icons in a document tool). Logos of Phosphor, Lucide and a third icon set (blue flag logo, unidentified).
- After the icon swap (0:40 to 0:48): same layout, every emoji replaced by thin line icons (eye, calendar, copy, check, QR grid, analytics).
- Said: "Never let an AI choose any of your colors." AI picks bright colours that do not work together. Fix: change the backgrounds from dark blue to dark green, remove the icons in the KPI tiles, expand the KPIs, add micro charts.
- Shown (0:48 to 1:04, full frame 0:56): background moves from navy to a near-black with a slight green tint, matching the green brand. The four KPI tiles become two wide cards: label with a chevron ("Total Clicks >", "Click Rate >"), a large bold number bottom left (32,142 / 4,121) and a thin green sparkline filling the right half of the card. Icon discs gone. Page gets a real title "Links" in place of the grey subtitle. The list card header gains a count on the right ("2 Active Links", number large, label small grey).
- Said: "we've added in much more relevant information and color through charts instead of buttons and icons." A few more colour changes give the beginnings of a professional dashboard. Points to his previous software colour theory video.
- Shown (1:11): an AI paragraph full of em dashes ("I'd be happy to help you explore this important topic, one that demands careful consideration...") as the analogy: you can spot AI text by the dashes the way you spot AI UI by repeated KPIs.

### 1:11 to 2:36 Mistake 2: letting AI choose your layout
- Said: the four KPIs at the top show up three times in a small app (dashboard, sidebar tiles, other pages). "Never let an AI choose your layout either."
- Shown (1:24 to 1:36): Custom Domains and Teams pages still show the sidebar LINKS / CLICKS tiles. Teams page has a purple bordered "Team Feature - Upgrade Required" card with a lock emoji, a checklist of plans, a green "View Plans & Upgrade" button and a disabled "Create Team" button under it.
- Said: on Custom Domains or Teams the click counts do not matter. If I need that I go to the dashboard or the analytics tab, which we need to add. Align the sidebar to the left and tighten the spacing.
- Shown: sidebar stat tiles removed, "Analytics" added under PLATFORM, spacing tightened.
- Said: "AI also loves to make these gradient profile circles with letters in them." Replace with an account card; move the links into a popover on click; collapse Settings and Billing and Usage together.
- Shown (1:44, full frame): bottom of sidebar now a single "My Account" row: green rounded-square avatar with a person icon, label, chevron ">" on the right. On click a popover to the right lists Billing and Usage, Settings, Sign Out, each with a line icon. The ACCOUNT section and the separate Sign Out link are gone.
- Said: the link cards feel busy. Collapse the buttons into a triple dot menu, move the date to the centre, collapse the chips to just icons, move clicks to the right.
- Shown (1:52 to 2:05, full frame 2:05): each row is now: white monospace short URL (no longer green) with a small check icon (was "Verified Safe" chip) and a copy icon (was "Copy" chip), destination URL below in grey; date in a centre column; "green dot 27 clicks cursor icon" on the right; a vertical three dot menu at the far right. Analytics / QR Code / Delete buttons gone into the menu. The "Create New Link" button changes from a bright green fill to a dark neutral button with a plus icon. Second sparkline card label changes to "New Leads". List header simplified to "Active Links" (link icon removed).
- Said: AI sets up logic well if you tell it to, same for features. The create link flyout is sparse even with lots of space, so a modal fits better. Collapse advanced options by default and give it a modern look. Missing options: swap between custom domain and link cards, a description field. This layout lets more features slot in.
- Before (2:08, full frame): a tall flyout "sparkle icon Create New Link" with subtitle, a full width Destination URL input, a half width Title input, an "Advanced Options" box containing a green "Want branded links? Add a custom domain. Configure" banner and a Password Protection input with a lock emoji, then a full width bright green "Generate Secure Link" button. Inputs are light grey filled boxes on dark.
- After (2:29, full frame): a wide modal "Create New Link" with a two column grid: Destination URL | Title (optional), Short Link (domain dropdown "linkguard.co" joined to a generated slug "pOg8x1e" with a regenerate icon) | Description. Inputs are dark with a subtle 1px border, not light filled. Advanced options collapsed into three pill buttons along the bottom left (key icon Password, target icon Targeting, clock icon Expiration). The primary green "Generate Secure Link" sits bottom right, sized to its label. Sparkle icon in the title removed.
- Said: this is where you spend the least time and see the largest change, "since AI is generally pretty bad at putting together complex layouts and cards."

### 2:36 to 3:23 Sponsor (Builder.io)
- Import Figma designs, drop a screenshot, add a Slack thread, or describe what you need; it works with your existing codebase and design system. Visual editor: drag and drop components, adjust spacing, colours, layouts, and the changes go back into the code. Shown: Builder.io "What should we build?" prompt screen, Slack "@Builder.io Add a new page", a "Kangaroo Inc." link dashboard being edited with a style panel (margin and padding box, typography, design tokens).

### 3:23 to 4:49 Mistake 3 (part): billing and usage page, pricing
- Before (3:32, full frame): "Current Plan: Free" card with a purple border and four usage tiles (Links Used 2/25, Custom Domains 0/0, Team Members 1/1, Analytics 7d). A "bar chart emoji Choosing the Right Plan" card with two text columns (Personal Projects / Professional Use) that has no action. "Available Plans": five cards in a row (Free $0 green border + "Current" chip, Hobby $3, Standard $2 purple border + "Popular" chip, Team $10, Business $140), "/month (Early Adopter)" in small grey next to the price.
- Said: "this card doesn't do anything. And that's a pattern you're going to see a lot with AI, so it can go." Retitle the page and add tabs because the page is rebuilt. "These KPIs are very vibe cody and lame." A simple two column layout with small donut charts elevates it.
- After, Usage tab (3:48, full frame): title "Settings", tabs Usage / Billing / Account (active tab a small grey pill). Two columns: left "Usage" heading, grey helper "Upgrade for higher limits and more features", a small dark "Upgrade" button, "Plan: Free". Right: a list of rows separated by hairlines, each with a tiny progress donut (or icon), label, and value right aligned (Links Used 2/25, Custom Domains 0/0, Team Members 1/1 full green ring, Analytics 7 days).
- Said on plans: Standard ($2) is cheaper than Hobby ($3), which makes no sense until you realise it is discounted (Team too). Five plans is not ideal; drop Hobby, at least one has to go. Drop the size of the plan name since nobody cares, increase the size of the cost per month since people do. Business becomes Enterprise because at 50,000 links per month you need more. Show the actual discount. Show what the next plan includes that the current one lacks. This pricing pattern is common at Resend and Supabase.
- Shown (4:00 to 4:16): Hobby card animates out, four plans remain, chips and coloured borders removed. Then (4:24, full frame) four equal cards: plan name small, centred, regular weight (Free, Standard, Team, Enterprise); old price struck through in grey above ($10/mo, $24/mo); new price large, light weight, centred ("$2 / mo", "$10 / mo", "Custom"); checklist; a muted full width button at the bottom of each card ("Current Plan" disabled, "Upgrade to Standard", "Upgrade to Team", "Upgrade to Business"), no bright green CTA. Resend pricing page shown (4:32): Free $0/mo, Pro $20/mo, Scale $90/mo, Enterprise Custom, a volume slider (3,000 to 3,000,000+ emails), and one shared feature list where missing items get a grey x.
- Final (4:37, full frame): a quota line under each price (25 links / mo, 5,000 links / mo, 10,000 links / mo, Custom) and the SAME seven row feature list in every card (users, analytics, custom domains, security features, team collaboration, bulk operations, A/B testing + API access), green check where included, dim grey check where not, so the upgrade delta is visible by scanning across.
- Said: add a billing email and payment method. Shown (4:40): "Billing Email" input with "Save", "Payment Method: Visa ending in 0000, expires 04/28" with "Add card", side by side above Plans.
- Said: the pro of tabs is scale: documents, integrations or AI later just become another tab. Shown (4:48): tabs Usage, Billing, Account, Documents, Integrations, AI Credits.

### 4:49 to 5:36 Mistake 4: analytics, the low hanging features
- Before (4:52, full frame): breadcrumb "Dashboard / Analytics", title "First campaign", "Last 30 Days" dropdown, bright green "Export Report" button, four KPI tiles (Total Clicks 10 "+100% from previous period", Daily Average 3, Locations 2, Top Device desktop) each with a small coloured icon at top right (blue, green, purple, red), a tab row (Overview, Geography, Technology, Sources) and a "Click Performance" area chart that is one smooth curve.
- Said: toss the KPIs and the tabs. Don't forget low hanging fruit, simple features that make the app much better. Move the actions down and add a toggle to split into individual links so you can compare links. Super easy to implement and genuinely useful.
- Shown (5:04 to 5:13, full frames): title "Analytics", dark neutral "+ Create Report" button. One wide chart card: "cursor icon Total Clicks: 32,142", on the right a segmented control "Aggregate | Individual", a "Last Month" dropdown, an export icon button. Real jagged line chart with y gridlines 0 to 700. Toggling Individual draws three coloured lines (teal, magenta, yellow), one per link, with a legend of the link URLs. Below: "Top Locations" (country code badges CA / UN, a green bar, count) and "Top Devices" (green and blue donut).
- Said: shove more useful information into the row with helpful icons that also add a splash of colour.
- Shown (5:20, full frame): three cards: Devices (segmented semi-circle gauge in blue to teal to yellow with "1735 Clicks" in the centre, and a legend Monitor 1341 76.1%, Laptop 217 13.4%, Mobile 124 6.2%, Tablet 53 3.4%), Sources (Instagram, Facebook, Direct, Dribbble, X, Pinterest with their real brand logos, clicks and %), Browsers (Chrome, Safari, Firefox, Opera, Edge, Other with brand logos). Brand logos are where the colour comes from.
- Said: instead of a boring bar chart, show a map with shaded regions and the actual data to the left.
- Shown: "Demographics" card: country table on the left with flags (Germany 842 41.2%, United States 641 35.4%, China 452 8.2%, Canada 60 2.6%, Other 397 10.2%) and a hex dot world map on the right with coloured dots. Each card has its own "Last Month" dropdown and export icon.
- Said: from start to finish on analytics, a big change just from changing a few charts and adding icons.

### 5:36 to 6:13 Mistake 5: landing pages
- Said: this is where you lose most customers if you vibe code it. SaaS landing pages have a standard of quality that establishes trust, even subconsciously. Colour and layout principles help, but what you really need are graphics.
- Before (5:35 to 5:36, full frames): navy page, centred hero with a cyan gradient "Shorten links." over a green gradient "Expand your reach.", grey subline, a URL input with a green "Shorten It" button in a boxed card, a "Success! Cloudflare" badge, "LIMITED TIME OFFER" with two plan cards (Personal Founder $2, Team Founder $10 with a "BEST VALUE" purple chip and a teal to purple gradient CTA button). Then "Trust & Security First": a 3x2 grid of identical cards, each with a tiny tinted icon square (shield, chart, lock, layout, globe, phone) plus title plus two lines. Footer with Product / Company / Resources columns.
- Shown (5:44): first pass, colours calmed: white headline, solid green second line, dark green page.
- Said: even something as simple as link cards with some skew elevates the page.
- Shown (5:52, full frame): hero left aligned, two lines in plain white bold ("Shorten links. Expand your reach."), grey subline, a borderless URL field with a globe icon and a dark neutral "Shorten It ->" button. On the right, three of the product's own link row cards rendered in perspective (rotated and skewed), fading out down and to the right. Nav: logo, theme toggle, "URL Check", "Pricing", dark "Log In", green "Get Started Free" (the single bright CTA on the page). Below: "LIMITED TIME OFFER" with the new Standard / Team cards (struck through old prices).
- Said: instead of "these lameass icons", use a slightly edited image of the analytics page we designed, same idea for password protection.
- Shown (6:00, full frame): feature section "Detailed Analytics", grey copy "Know exactly who is clicking. Location, Device, Browser, and Referrer data.", dark "See it in action ->" button on the left; on the right the real multi-line analytics chart (with the Aggregate | Individual toggle) in 3D perspective, fading into the background.
- Said: "Landing pages aren't about complexity, they're about presentation. And generally, the better the presentation, the better the conversion."

### 6:13 to 6:32 Outro
- Builder.io link and the Figma assets of the redesign are in the description.

## Extracted rules

Icons
1. Never use emoji as UI icons (status chips, buttons, metadata, section titles, field labels). Use one interface icon library (Phosphor, Lucide or similar) at one stroke weight.
2. Emoji are acceptable only where users pick them as content (Notion page icons), never as the app's own iconography.
3. Do not put a decorative icon in every KPI tile or feature card by default. An icon must carry meaning (a brand logo, a device type, a status); otherwise remove it.

Colour
4. Do not accept AI default colours. Pick the palette yourself: a near-black background tinted toward the brand hue (here dark green for a green brand, not a generic dark navy).
5. Keep one bright accent fill for at most one primary CTA per view (the landing "Get Started Free", the modal "Generate Secure Link"). Page header actions ("Create New Link", "Create Report", "Export") use a dark neutral button with an icon.
6. Put colour into data: sparklines, chart lines, donuts, gauges, map dots and real brand logos. Not into tinted icon discs, coloured chip outlines and multiple coloured card borders.
7. Do not mark different plans with different coloured borders and chips (green "Current", purple "Popular"). Keep cards equal and neutral.
8. No gradient text headlines and no gradient CTA buttons on the landing page; plain white headline, one solid accent at most.
9. Body text values like the short URL stay neutral (white), not brand green; reserve the accent for actions and live states (a small green dot before "27 clicks").

Layout and information architecture
10. Each metric appears in exactly one place. If the same KPIs appear on several pages or in the sidebar, delete the copies and give them a home (Dashboard or an Analytics tab).
11. Show only what matters on the page the user is on. Click counts do not belong on Custom Domains or Teams.
12. Prefer fewer, wider KPI cards with a sparkline (2 cards: label + chevron, big number bottom left, micro chart right) over 4 small icon tiles with lonely numbers.
13. Give every page a real title ("Links", "Settings", "Analytics"), not only a grey descriptive subtitle.
14. Replace the gradient letter avatar circle with a single account row (avatar, name, chevron) that opens a popover with Billing and Usage, Settings, Sign Out. Merge settings-like links into it.
15. Tighten and left align sidebar spacing; remove stat widgets from the sidebar.
16. In list rows, collapse secondary actions (Analytics, QR Code, Delete) into a triple dot menu at the row end. Collapse text chips ("Verified Safe", "Copy") into icon-only affordances next to the item.
17. Lay a list row out in columns: identity left (title + secondary line), date centre, the key metric right, overflow menu far right.
18. Delete cards that do nothing: an informational card with no action or data ("Choosing the Right Plan") is an AI tell.
19. Group a growing settings area into tabs (Usage, Billing, Account, later Documents, Integrations, AI Credits) so new features become a tab, not a longer page.
20. Usage and limits: a two column layout, explanation and upgrade action on the left, a hairline-separated list of rows (progress donut, label, "used / limit" right aligned) on the right, instead of a grid of KPI tiles.

Forms and creation flows
21. If a flyout or side panel is sparse and space is available, use a centred modal with a two column field grid.
22. Collapse advanced options by default into small pill buttons with icons (Password, Targeting, Expiration) that expand on click.
23. Fill gaps in the feature set the AI missed: let the user choose the custom domain next to the slug (a domain dropdown joined to the slug input, with a regenerate icon), add a Description field.
24. Inputs on dark: dark fill with a subtle 1px border, not light grey filled boxes. Primary button sized to its label and aligned bottom right, not a full width bar.

Pricing
25. Show 3 to 4 plans, not 5. Drop the plan that confuses the ladder (a cheaper "Hobby" beside a discounted "Standard").
26. Make the price the biggest element in a plan card and the plan name small. Write prices as "$2 / mo"; the top tier is "Enterprise" with "Custom".
27. A plan that is discounted shows the original price struck through above the real price. Never let a discounted plan look cheaper than a lower tier without explanation.
28. Under the price, one quota line ("5,000 links / mo").
29. Use one shared feature list in every card, in the same order, checked where included and dimmed where not, so what the next plan adds is visible at a glance (Resend, Supabase pattern).
30. Buttons per card: "Current Plan" disabled on the current one, "Upgrade to X" on others, all neutral.
31. Put billing email (with Save) and payment method ("Visa ending in 0000, expires 04/28", Add card) on the billing tab.

Analytics
32. Use one large real time series chart with a segmented "Aggregate | Individual" toggle that splits it into one line per item for comparison. Cheap to build, genuinely useful.
33. Per card controls: period dropdown ("Last Month") and an export icon, top right of the card.
34. Replace generic bar charts with the chart the data deserves: a world map with shaded regions plus the numbers in a table to its left; a segmented gauge or donut with a legend (count and %) for devices.
35. Use real brand logos (Instagram, Chrome, Safari...) and country flags in source, browser and country tables; they supply colour and meaning together.
36. Drop KPI tiles and tab rows that duplicate what the charts below already show.

Landing page
37. A SaaS landing page needs graphics, not icon tiles. Use your own product UI as the visual: real components (link cards) in skewed perspective, or a slightly edited screenshot of a designed screen (the analytics chart in 3D tilt fading into the background).
38. Feature sections: text and one button on the left, a product visual on the right, one feature per section. Not a 3x2 grid of identical cards with tiny tinted icons.
39. Hero: left aligned, plain bold white headline, grey one line subhead, the input and a neutral action, product visual on the right.

Process
40. Let the AI write logic and features when you tell it exactly what; you decide layout, colour and which cards exist. Layout is where human time gives the biggest visible change.

## Anti-patterns (vibe coded tells) and fixes

| Tell | Fix |
|---|---|
| Emoji as icons (checkmark, clipboard, eye, calendar, bar chart, phone, lock emoji in chips, buttons, labels, card titles) | One icon library (Phosphor or Lucide), line icons, one weight |
| Generic dark navy background with bright saturated accents that clash | Near-black tinted toward the brand hue; one accent |
| Four KPI tiles with tinted icon discs and small numbers (often showing 0) | Two wide cards: label + chevron, big number, sparkline |
| The same KPIs repeated on 3 pages and in the sidebar | One home for each metric, remove the rest |
| Gradient circle avatar with a letter | Account row with avatar, name and chevron opening a popover |
| Separate Billing, Settings, Sign Out links in the sidebar | Collapsed into the account popover |
| A row of three buttons on every list item (Analytics / QR Code / Delete) | Three dot overflow menu |
| Text chips with emoji ("Verified Safe", "Copy") | Icon only affordances beside the item |
| Accent coloured monospace data text | Neutral text; accent only on actions and live dots |
| Bright green filled button for every action | Neutral dark buttons; one bright CTA per view |
| Sparse tall flyout with full width inputs and a full width CTA | Two column modal, advanced options as pills, CTA bottom right |
| Light grey filled inputs on a dark surface | Dark inputs with a hairline border |
| Missing obvious options (domain choice, description) | Add them; the layout should have slots for more |
| Cards that do nothing ("Choosing the Right Plan" explainer) | Delete |
| Upgrade-required promo card with lock emoji and a disabled button under it | Not shown fixed explicitly; implied: one clear upgrade path, no dead controls |
| Five pricing plans, a cheaper middle tier, unexplained "Early Adopter" prices | Four plans, struck through original prices, Enterprise "Custom" |
| Plan name as big as the price | Small name, large price |
| Coloured borders and chips per plan ("Current", "Popular") | Equal neutral cards |
| Each plan lists different features | One shared feature list, checked vs dimmed |
| Analytics page that is KPI tiles plus tabs plus one smooth fake looking curve | One real chart with Aggregate / Individual toggle, map, gauges, logo tables |
| Boring bar chart for geography | Shaded map plus the data table on its left |
| Gradient text headline (cyan, green), gradient CTA, "BEST VALUE" chip | Plain white headline, single solid CTA |
| 3x2 grid of feature cards with tiny tinted icons | Product UI as graphics: skewed link cards, tilted analytics screenshot |
| Em dashes in copy (shown as the text analogue of these UI tells) | Do not write them |

## Quality checks before shipping

- Search the UI for any emoji character. Zero allowed in app chrome.
- Is any metric shown in more than one place? Count the KPI widgets across all pages.
- Does every card have a job (an action or real data)? Delete the ones that only explain.
- On each page, is the information relevant to that page, or copied from the dashboard?
- How many bright accent fills are on this screen? More than one primary CTA means demote the others.
- Is colour carried by data (charts, logos, flags, status dots) rather than decorative icon discs and borders?
- In each list row: how many buttons are visible? More than one or two means an overflow menu.
- In each form: is there empty space while fields stack one per row? Use a grid or a modal. Are advanced options hidden by default?
- Pricing: can a user tell in one glance what the next plan adds? Is the price the largest text? Does any tier look illogically priced?
- Analytics: can the user compare items (split toggle)? Does each chart type fit its data (map for geography, gauge or donut for share)?
- Landing page: is there at least one real product graphic above the fold? Would the page still look generic with the logo swapped?
- Would this screen be recognisable as AI generated by the tells in the table above?

## Psychology / why it works

- Polish on a landing page "establishes trust, even subconsciously"; a vibe coded landing page is where you lose most customers. Better presentation means better conversion.
- Users scan for price, so price gets size; nobody cares about the plan name. Showing the discount and what the next plan adds makes the upgrade decision easy (anchoring with struck through prices, visible delta).
- Repetition and generic patterns (emoji, gradient avatars, repeated KPIs, dashes) read as machine made, the same way em dashes signal AI written text.
- Removing irrelevant information per page reduces noise: the user goes to the dashboard when they want numbers.

## Cited resources

- Cursor, Replit, Builder.io: the AI builders that produce vibe coded apps (Builder.io is also the sponsor: Figma import, screenshot or Slack thread input, visual editor that writes back to code, respects your design system).
- Phosphor Icons: his preferred icon library.
- Lucide: named as an equally good alternative ("or any other interface icon libraries").
- Notion: the example of an app that uses emoji successfully (user page icons); landing page shown as a quality reference.
- Linear, Relume, Resend landing pages: shown in the intro as the standard of finished SaaS design.
- Resend pricing page and Supabase pricing: the pricing pattern he copies (equal cards, big price, shared feature list with included vs excluded, Enterprise Custom, Resend also has a volume slider and Transactional / Marketing tabs).
- His previous video on software colour theory ("full deep dive on software color theory", linked at the end of that segment).
- The Figma file of this redesign, linked in the video description.
- A third icon library logo (blue flag) appears next to Phosphor and Lucide but is not named.

## Memorable quotes

- "Get rid of the emojis."
- "Never let an AI choose any of your colors."
- "Never let an AI choose your layout either."
- "We've added in much more relevant information and color through charts instead of buttons and icons."
- "This card doesn't do anything. And that's a pattern you're going to see a lot with AI, so it can go."
- "AI is generally pretty bad at putting together complex layouts and cards."
- "Landing pages aren't about complexity, they're about presentation."
- "The better the presentation, the better the conversion."
