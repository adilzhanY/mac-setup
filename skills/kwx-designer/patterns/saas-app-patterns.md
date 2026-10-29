# SaaS app patterns: sidebar, account menu, list rows, modals, settings, analytics

The shell of a SaaS app is where vibe coded products give themselves away (Kole Jain, vibe coded SaaS; dashboard flaws; every UI concept). These are the patterns to build instead. AI is good at logic when told exactly what; layout, colour and which cards exist are the designer's job, and "this is where you spend the least time and see the largest change".

Numbers marked (est.) were read off video frames, not stated.

## Contents

1. Sidebar
2. Account menu
3. Page header
4. List rows
5. Primary actions and buttons
6. Modals and creation flows
7. Popovers instead of pages
8. Settings, usage and billing
9. Analytics page
10. Announcements and onboarding in the shell
11. Checks

---

## 1. Sidebar

1. Navigation only. No stat tiles (the LinkGuard sidebar had "LINKS 2 / CLICKS 0" tiles; delete them). Click counts do not belong on Custom Domains or Teams pages.
2. Left aligned, tight spacing. Sections with small uppercase labels are fine (PLATFORM, ORGANIZATION) if there are enough items to need them.
3. Links are ghost buttons: no fill until hover, then a light rounded fill. Active item: a lighter row fill or raised segment, plus full contrast text.
4. Icon size equals the text line height: 15 px label with 24 px line height gets 24 px icons, and a tight icon to text gap. Most icons are drawn too large.
5. Right side of a row may hold a count or badge: "6" in a green badge, a "New" chip. Counts must be real.
6. Collapsed rail: icon only, with a dark tooltip on hover ("Quick actions").
7. Give every page that the sidebar opens a real title.
8. Add the destination the user will look for: LinkGuard gained an "Analytics" item, because the numbers removed from other pages need a home.

## 2. Account menu

1. Replace the gradient circle with a letter ("AI also loves to make these gradient profile circles with letters in them") with one account row at the bottom of the sidebar: avatar (photo, or a neutral person icon on a brand tinted rounded square), name or "My Account", a chevron on the right.
2. Clicking it opens a popover beside it with Billing and Usage, Settings, Sign Out, each with a line icon.
3. Remove the separate ACCOUNT section and the standalone Sign Out link; everything account related lives in the popover.
4. Multi workspace apps: the account switcher sits at the top of the sidebar (name plus switcher chevrons).

## 3. Page header

1. Pattern: small eyebrow with icon ("Private Database" with a lock), title, one line grey description, then segmented tabs with "+" to add one. Title medium weight, about 2x body (est.).
2. Top bar right: status text ("Edited 23 min ago"), the one primary action (Share), avatar, star, kebab. Breadcrumb top left.
3. Segmented tabs: a light grey track, the active tab a white raised segment.
4. A real title ("Links", "Settings", "Analytics") instead of only a grey sentence like "Manage your links and view analytics".

## 4. List rows

1. Columns: identity left (title plus a grey secondary line), date centre, the key metric right, overflow menu far right. LinkGuard row after the redesign: white monospace short URL with a small check icon (was a "Verified Safe" chip) and a copy icon (was a "Copy" chip), destination URL in grey below, date centred, "green dot 27 clicks" on the right, vertical three dot menu.
2. At most one or two visible actions per row. Collapse the rest (Analytics, QR Code, Delete) into the three dot menu.
3. Collapse text chips into icon only affordances beside the item, each with a tooltip.
4. Data text stays neutral. The short URL was brand green; it became white. Accent only for actions and live states (the small green dot).
5. A list header can carry a count: "2 Active Links" with the number large and the label small grey.
6. Secondary destructive actions in tight space appear on hover (a small "x" with tooltip "Delete").

## 5. Primary actions and buttons

1. One bright accent fill per view, for the single primary action. Page header actions ("Create New Link", "Create Report", "Export Report") use a dark neutral button with a plus or action icon.
2. Pair a filled primary with a ghost secondary side by side.
3. Horizontal padding about double the vertical padding (32 px sides, about 16 px top and bottom; the vertical value is implied, not stated).
4. Every button: default, hover, pressed, disabled, plus loading with a spinner when it starts async work.
5. Size the button to its label. Full width bars only for the one action of a mobile screen or a modal footer on narrow screens.

## 6. Modals and creation flows

1. If a flyout or side panel is sparse and space is available, use a centred modal with a two column field grid. LinkGuard "Create New Link" after: Destination URL | Title (optional), Short Link (domain dropdown "linkguard.co" joined to a generated slug "pOg8x1e" with a regenerate icon) | Description.
2. Advanced options collapsed by default into small pill buttons with icons along the bottom left (Password, Targeting, Expiration). Each expands on click.
3. Primary button bottom right, sized to its label ("Generate Secure Link"). No full width bright bar.
4. No decorative sparkle icon in the modal title.
5. Add the options the AI missed: choosing the custom domain next to the slug, a description field. The layout should have slots for more features.
6. Inputs on dark: dark fill with a subtle 1 px border, not light grey filled boxes.
7. Escape closes, Enter submits when valid, focus starts in the first field, focus returns to the trigger on close.

## 7. Popovers instead of pages

1. Infrequent features (share, settings for one object, sort, filter) open in a popover anchored to their trigger.
2. The primary action of a popover goes at its top, immediately visible (the share popover's invite field with "Can view" and "Invite").
3. Menus: 16 px line icon left of each label, white card, about 12 px radius (est.), soft shadow, equal left and right padding. Destructive item last, in red with a red icon.
4. Popover shadows are stronger than card shadows: elevation decides strength.

## 8. Settings, usage and billing

1. Title "Settings", tabs Usage / Billing / Account (active tab a small grey pill). Tabs scale: Documents, Integrations, AI Credits later become another tab, not a longer page.
2. Usage tab: two columns. Left: "Usage" heading, grey helper "Upgrade for higher limits and more features", a small dark "Upgrade" button, "Plan: Free". Right: hairline separated rows, each with a tiny progress donut, label, and "used / limit" right aligned (Links Used 2/25, Custom Domains 0/0, Team Members 1/1 as a full ring, Analytics 7 days).
3. Do not use a grid of KPI tiles for usage ("These KPIs are very vibe cody and lame").
4. Billing tab: billing email input with Save, payment method "Visa ending in 0000, expires 04/28" with "Add card", side by side above Plans.
5. Plans: 3 to 4 equal neutral cards, small plan name, big price, struck original price if discounted, one quota line, one shared feature list (checked vs dimmed), muted buttons ("Current Plan" disabled, "Upgrade to Team").
6. Delete cards that do nothing. "Choosing the Right Plan", an explainer with two text columns and no action: "this card doesn't do anything. And that's a pattern you're going to see a lot with AI, so it can go."
7. An upgrade required state shows one clear upgrade path. No disabled "Create Team" button sitting under the upgrade card, no lock emoji.

## 9. Analytics page

1. Title "Analytics", dark neutral "+ Create Report".
2. One wide chart card: "Total Clicks: 32,142", segmented "Aggregate | Individual", a "Last Month" dropdown, an export icon. Real jagged line chart with y gridlines. Individual draws one line per link with a legend.
3. Below: Top Locations (country code badges, a bar, count) and Top Devices (donut).
4. Row of three cards: Devices gauge with legend, Sources with real brand logos (Instagram, Facebook, Direct, Dribbble, X, Pinterest), Browsers with logos (Chrome, Safari, Firefox, Opera, Edge, Other). The logos supply the colour.
5. Demographics: country table with flags on the left, shaded map on the right.
6. Toss KPI tiles and tabs that duplicate the charts. Add the low hanging features (comparison toggle, per card period and export).

## 10. Announcements and onboarding in the shell

1. Feature announcement: a small "New" card with a date, a preview, one line ("Tedious long email chains are a thing of the past with new chat features"), and changelog rows with dates. Dismissible.
2. Onboarding: never a six bullet modal at login. One dark tooltip anchored to the main control ("Add a row / Easily add or insert new rows into your data tables", "Dismiss"), then a corner checklist ("4 of 6 complete").

## 11. Checks

| Check | Pass when | Verify in code |
|---|---|---|
| Sidebar is navigation | No metrics or stat widgets in the sidebar component | Read the sidebar component tree |
| Account row | No gradient letter avatar; one account row opens a popover with Billing, Settings, Sign Out | `grep -niE "gradient" ` near avatar; find the account popover |
| Real page titles | Every route renders a title element | Each page has an h1 or title component |
| Row actions | At most two visible actions per list row, the rest in a menu | Count buttons in the row component |
| One accent fill per view | Only one primary variant button rendered per screen | Count `variant="primary"` (or the accent class) per route |
| Modal layout | Creation forms with 4+ fields use a grid; advanced options collapsed | Read the modal's layout and initial collapsed state |
| No dead cards | Every card has an action or real data | List cards; each has a handler or a data binding |
| Settings in tabs | Settings sections are tabs, not one long page | Read the settings route structure |
| Shared feature list | Plan cards render from one feature array | One array with per plan flags |
| Tooltips | Icon only controls have tooltips and accessible labels | Search icon buttons without label |
