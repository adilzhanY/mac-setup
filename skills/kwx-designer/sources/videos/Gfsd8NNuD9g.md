# Everything you need to know about Mobile App UI's in 8 minutes

- Channel: Kole Jain
- URL: https://www.youtube.com/watch?v=Gfsd8NNuD9g
- Duration: 7:36
- Demo app: "Notely", a dark notes/calendar/tasks app, designed first as a desktop dashboard and then translated to mobile (iPhone frame, status bar 9:41). Figma assets linked in the video description.

## Core thesis

Mobile is not a shrunk desktop. The screen gets smaller but type and spacing stay about the same or get larger (iOS base font 17px vs macOS 13px), so you show far less at once: on desktop you had five panels, on mobile you pick one. Layout changes accordingly: each section scrolls in only one direction, cards replace white space as the grouping tool, and one screen does one thing. Because space is scarce, actions are contextual and come and go, secondary tasks open in bottom sheets so the user keeps context, and gestures (swipe back, swipe down, long press) carry a lot of the interaction. Finally, design the empty states, not just the ideal full state.

## Timestamped walkthrough

**0:00 to 0:20 Intro.** Mobile is so different from desktop that it produces questionable designs. Shown: the finished Notely home screen (dark, near black background, slightly lighter grey cards, Tasks card with a blue filled check on a struck-through completed task, Notes section with "Recents / Suggested" tabs at the right of the section header, horizontally scrolling note cards cut off at the right edge) and a floating bottom bar.

**0:20 to 0:58 Navigation option 1: floating bottom tab bar.** The desktop sidebar is gone. If the sidebar links can be consolidated into a few key icons, use a bottom bar, "nowadays typically floating, with the important action broken out". Shown: a pill shaped floating bar with Overview / Notes / Calendar / Tasks (icon above label), the active tab (Overview) sits on a lighter pill highlight inside the bar, and a separate circular "+" button floats to the right of the bar (the broken out primary action). He first shows a 7 icon bar (icons only, no labels, at 0:05) then reduces it. At 0:43 a 3 tab variant (Overview, Notes, Calendar) plus "+" is shown as the more ideal count.
- "Five links down here is pretty much the definite limit, and three or four is much more ideal."
- Tap target always over 44px "since people do have fat fingers".
- At 0:47 the tab item is annotated: **72px wide x 48px tall** (each tab cell; the active pill fills that cell). Icon about 24px, label small (about 12 to 13px) under it.
- The bar actions change with context (covered later: the editor replaces it).
- Shown at 0:52: in the note editor the tab bar is replaced by a small formatting toolbar pill (more "...", list, format paint icons) plus a separate round undo button at the right.

**0:58 to 1:30 Navigation option 2: sidebar becomes the home page.** When there are too many important sidebar items to fit a bottom bar, turn the sidebar into a whole page that becomes the home page. Shown at 1:10 to 1:22: the desktop sidebar (Kole Jain account switcher, Quick Search with a cmd F badge, Overview / Notes / Calendar / Tasks / Files / Templates, divider, Notebook / Tags / Shared with me) becomes a mobile screen. To stop it feeling lopsided (all items on the left, empty right side), he adds "Recent notes" as small horizontal cards at the top and puts counts and badges on the right of rows (Notes 13, Tasks 9, Files 132 in green, "new" in green on Shared with me). Top right: inbox icon and "..." more. The bottom is now free for a big "Search for anything..." pill and a round "+" button. Cited example: Notion does this (1:25 shows Notion's mobile home: Teamspace Home, Tasks Tracker, Document Hub, Goals Tracker rows with disclosure chevrons, a "Browse templates" card, and a bottom row of search icon button, a wide "Ask AI" pill and a compose button, above the home indicator).
- Top of screen: "a bell and more menu is a good place to start", but top actions are highly contextual per page. Shown: bell + "..." grouped in one small pill at top right (1:27, 1:35).

**1:30 to 2:15 Type scale and density.** It is natural to squish things down to fit as much as possible. Shown at 1:35 to 1:44: his first attempt looks normal alone (Calendar section, "FRIDAY, FEB 27" in red caps, events with a coloured left bar: yellow "Meeting with Jeremy 10:00 AM" highlighted on a tinted row, then "TOMORROW" header in grey caps, purple and red events). Then he zooms out beside a real Spotify home screen (chip row Podcasts / Audiobooks / Wrapped, 2 column shortcut tiles, "Your shows" header with big artwork): his text is visibly smaller and denser than Spotify's. At 1:48 the fixed version has larger type (titles, event rows and the section header all grow, the event row title about the size of Spotify's tile titles).
- "Despite our screen getting much, much smaller, the type scale and spacing remains relatively similar to desktop, even getting a bit larger."
- **iOS base font size 17px, macOS base 13px.** "More often than not, things actually get larger on these smaller screens."
- Shown: iOS lock screen media player (Seagulls / Butcher Brown, big transport controls, flashlight and camera round buttons near the bottom) and iMessage held in hand, as reference for real iOS sizing.
- 2:02 to 2:15: the full desktop dashboard (action bar with New Note / New Event / New Task, a gallery of recent notes, full day calendar timeline 8am to 2pm, Tasks, Scratch Pad) versus mobile: "now you can pick one of those things."

**2:15 to 2:48 One scroll direction per section.** Dashboards lay content out in two directions at once (2:24 to 2:28: a grid overlay shows the desktop as 2 columns x 3 rows). On mobile "you can choose one direction to move in per section": stack notes vertically, or scroll them horizontally off the page, never both. Shown: Dribbble style dashboards as the "two directions" example (Donezo dashboard, a Codename.com CRM, a "Twisty" income tracker). At 2:32 to 2:43: the desktop Notes row becomes a horizontal carousel on mobile (cards cut off at the right edge to signal scroll) while Calendar and Tasks stack vertically.

**2:48 to 3:30 Four building blocks, and no double nested cards.** Ignoring floating menus and actions, there are only four building blocks: **cards** (biggest and most important), **text or links**, **images**, **inputs**. Any of them can go inside cards. "Basically everything on here is a card in some way" because cards group content flexibly "in place of white space, which we don't typically have a lot of here". Shown: 2:57 the calendar card outlined in blue; 3:06 "from: Website Redesign" underlined as a link; 3:12 "Add task" row with an empty circle as the inline input.
- Avoid double nesting cards (3:15 to 3:27): note cards placed inside a Notes container card. The padding is highlighted with pink hatching at 3:20, showing padding on padding eating width. "It's not always avoidable, but it creates padding on padding, which really restricts the space you have and ends up cramping things." Fix: group with white space instead of a container. In the fixed version the note cards sit directly on the page background under the "Notes >" section header.

**3:30 to 4:10 One screen does one thing.** Home is the exception. Otherwise "the settings is just settings, and the notes editor is just a notes editor." Do not add clutter like recent notes or suggested templates at the top of the editor. Shown at 3:45 to 3:55: the cluttered editor version with a Templates gallery row (Project, Project planner thumbnails) wedged between the properties and the body, then the clean editor (3:59): round back button top left, a pill with share and "..." top right, large bold title "Portfolio design sprint V1", property rows (Status with a purple "In progress" chip, "+ Add field"), a hairline divider, then body text and a bullet list. "Whenever you need to add something new, don't reach for a different layout, reach for a different page altogether."

**4:00 to 4:35 Bottom sheets keep context.** Choosing a template while editing should not rip you away to a new page, but there is no room on screen. Use a bottom sheet. Shown at 4:10 to 4:15 and 6:20 to 6:26: a sheet rising from the bottom with a centred title "Templates", a full width "Search templates" field, and a 2 column grid of template thumbnails with captions (Meeting notes, Class notes, Agenda planner, Assignment planner, Project management, Expense tracker). The sheet's top controls: a round X at top left (dark grey) and a round blue check at top right (the confirm). Behind the sheet, the editor page is pushed back and slightly scaled down. "These can be any height, but they keep the user in context and are easy to navigate with gestures."
- The "+" button pattern (4:25 to 4:33): it either opens a little menu, or opens straight into an input so you can immediately start typing.
- At 4:38: references shown side by side: Apple Reminders "New Reminder" sheet (X left, blue check right, title, notes, URL, Date & Time toggles) and his Notely Templates sheet using the same X / check layout.

**4:35 to 5:10 Sponsor: Mobbin.** Library of screens and flows from real apps. Shown: Mobbin's filters by Categories (Finance, Lifestyle, AI, Food & Drink, Shopping), Screens (Signup, Welcome & Get Started, Dashboard, Filter & Sort, Payment Method), UI Elements (Card, Banner, Text Field, Button, Tab Bar, Bottom Sheet with the definition "Bottom Sheet is an overlay anchored to the bottom of the screen that displays supplementary content"), Flows (Browsing Tutorial, Chatting & Sending Messages, Creating Account, Editing Profile, Subscribing & Upgrading). Apps visible: Polestar, Pinterest, Paramount+, Pangea Charging, Beside, Reminders, Apple Wallet, State Farm, Craft, Notion onboarding prototype (notification permission dialog), TheFork, Viator, TIDE, Todoist. 20% off via his link.

**5:10 to 6:00 Gestures.**
- Swipe right to go back. "If we move the background left by about **35%** and then also animate it right, we get a super smooth transition." Shown at 5:15 to 5:22: the settings / account page (avatar tile "K" with green online dot, "Kole Jain" with account switcher chevrons, "This Device" group: Templates, Stats, On Device Folders, Private Folders, Tags, each with a chevron, then "General Settings") sliding back to Home, with Home starting offset to the left (parallax) and sliding in.
- Bottom sheets: as the sheet comes up, zoom out (scale down) the background, and zoom it back in on swipe down (5:26 to 5:30).
- Swipes "can be relied on pretty heavily" as long as you educate the user. Example: swipe up to search (Slack, and sort of Apple). Shown at 5:32 to 5:36: an illustrated "Classlist / Cooking Class" app and an "Invite List / Contact List" sheet demo of gesture driven transitions; at 5:40 his home with "Search for anything..." pill appearing at the top above the bell pill.
- Long press is "the mobile equivalent of the right click". Typical: blur the rest of the screen, show the actions, slightly zoom the pressed element (5:52 to 6:00). Shown: the pressed note card stays sharp, everything else (including the tab bar) is heavily blurred, and a menu card appears directly above it: Pin Note, Lock Note, Share Note, Note History, each with a right aligned icon (pin, lock, share, clock), hairline separators, and "Delete" in red with a red trash icon last. Go further: turn it into a dynamic preview like iOS does.

**6:00 to 6:27 Actions come and go.** Actions cannot always be persistent. Opening a note hides the navbar and reveals actions specific to editing: text formatting at the bottom, sharing at the top. Selecting templates hides all of that for just two actions, a confirm button and an X. How actions animate in and out "is half the fun". Shown 6:02 to 6:07: the back button and share/more pill animate in (they are separate floating round/pill controls with a subtle shadow).

**6:27 to 7:12 Empty states.** What was designed is the ideal state. First login has no content.
- Rejected option (6:40): per section empty cards, each with a tinted round icon (red calendar, blue check, yellow note), "No calendar events yet. Add some!" and a grey "Create Event" button, "No tasks yet. Add some!" + "Create Task".
- Chosen option (6:45): draw attention to the "+" (the main action) with one full screen empty state: "Get started with Notely" / "Add notes, calendar events, tasks files and more with the action bar", with a hand drawn curved arrow pointing down to the "+" button.
- Then a simple popover (6:50): blue "Quick Start" tooltip with lightbulb icon and close X: "Start by selecting either a note, event, or task. We'll default to creating a note." with "Settings" and "Dismiss" buttons, pointing at the composer. The composer is a "What's up?" input with a blue round send arrow, a row of type icons (note, calendar, task) and the keyboard up.
- No results state (6:55 to 7:10): search screen with "Search for anything..." field, filter chips Recents / Notes / Tasks / Events / Scratch, a recents list (title, type icon + source in grey, relative time "3h ago", "16h ago", "2d ago" right aligned). Typing "Spirnt" gives: a muted folder illustration with "0 results", "Oops, nothing found", "Your search didn't turn anything up. Did you mean 'Sprint'?" (the suggestion underlined as a link), and a "Start a New Note" button with icon. He says: add nice imagery, acknowledge there are no notes matching the keywords, offer suggestions in case of a typo, and give an action to exit the empty state. A bare "Please try again" (7:00) is the bad version.

**7:12 to 7:36 Outro.** This is a foundation. Mobbin link and the Figma assets in the description.

## Extracted rules

Navigation
1. If the desktop sidebar can be reduced to a few key destinations, use a bottom tab bar. Modern default: a floating pill bar inset from the screen edges, with the primary action (for example "+") broken out as a separate round button beside it.
2. Keep the tab bar to 3 or 4 items. 5 is the hard maximum.
3. Every tap target is over 44px. His tab cells are 72px wide x 48px tall. Icon (about 24px) above a short label.
4. Show the active tab with a lighter pill highlight filling the tab cell, not just a colour change.
5. If there are too many important destinations for a tab bar, make the sidebar the home page: list rows, recent items as small cards at the top, counts and badges right aligned on rows to balance the layout, and use the free bottom for a large search pill and a primary action button (Notion pattern).
6. Top bar actions are contextual per page. A bell + "..." more menu grouped in one pill at top right is a good default for home. Detail pages: round back button top left, share + more in a pill top right.

Type and density
7. Do not shrink type for mobile. Body at the iOS base of 17px (macOS base is 13px). Mobile type and spacing are equal to or larger than desktop.
8. Validate density by placing your screen beside a real top app screenshot (he uses Spotify) at the same scale. If your text is smaller or denser, scale it up.
9. Accept that a mobile screen shows one of the things a desktop dashboard shows. Pick one per screen or section.

Layout
10. Each section scrolls in exactly one direction: vertical stack or horizontal carousel, never a 2D grid that extends both ways.
11. A horizontal carousel cuts the last card off at the screen edge so the scroll is obvious.
12. Build screens from four blocks: cards, text/links, images, inputs. Cards are the main grouping tool because there is little white space to group with.
13. Do not nest cards inside cards. If content is already in cards, group the set with a section header and white space, not a container.
14. One screen does one thing (home is the exception). No "recent" or "suggested" clutter inside a focused screen like an editor or settings.
15. For a new task, open a new page, not a new layout on the current one. For a short side task that must keep context (pick a template, quick create), use a bottom sheet.

Bottom sheets and overlays
16. Bottom sheet anatomy: centred title, optional search field, content (for example a 2 column thumbnail grid), and the screen top controls change to a round X (cancel, left, neutral grey) and a round check (confirm, right, accent blue).
17. Sheets can be any height. They must be dismissible by swipe down.
18. The "+" primary action either opens a small menu of types or opens straight into an input focused for typing.

Gestures and motion
19. Support swipe right to go back. During the transition, offset the underlying page left by about 35% and slide it right as the top page leaves (parallax).
20. When a bottom sheet rises, scale the background page down slightly; scale it back up on swipe down.
21. Swipe gestures can be relied on heavily (swipe up to search) only if you teach them to the user.
22. Long press = right click. Blur the rest of the screen (including nav), slightly zoom the pressed element, and show an action menu next to it: icon right aligned per row, hairline separators, destructive "Delete" last and in red with a red icon. Optionally show a live preview (iOS style).

Contextual actions
23. Actions come and go with context. Opening an editor hides the tab bar and shows editor tools (formatting bar at the bottom, share at the top). A selection sheet reduces actions to confirm and cancel.
24. Animate actions in and out; the transition is part of the design.

Empty states
25. Design the empty first run state, not only the full ideal state.
26. On first run, prefer one full screen empty state that points at the primary action (heading "Get started with X", one line of explanation, an arrow to the "+") over many per section empty cards.
27. Follow with a single dismissible popover tip (title with icon, one or two sentences, a secondary and a primary button, close X).
28. A no results state needs: an illustration, an acknowledgement that nothing matched the keywords, a typo suggestion ("Did you mean 'Sprint'?") as a link, and an action that exits the empty state ("Start a New Note"). Never just "Please try again".

Visual details observed (dark Notely style)
29. Near black page background, cards one step lighter grey, generous corner radii (cards about 16 to 20px, bars and buttons fully rounded pills/circles).
30. Section headers are "Title >" (tappable, with chevron) with a faint "..." or small text tabs ("Recents / Suggested") on the right.
31. Date group labels in small caps style: today's date in red ("FRIDAY, FEB 27"), "TOMORROW" in grey. Events use a 3px coloured left bar and coloured title; the current event row gets a faint tinted background.
32. Secondary metadata in grey and smaller ("from: Website Redesign", "3h ago"); completed tasks get a filled blue check and strikethrough grey text.
33. List rows: relative time right aligned, type icon + source below the title.

## Anti-patterns and fixes

- Squishing everything to fit on screen (small type, tight spacing). Fix: keep 17px body, compare against real apps, show less.
- More than 5 tab bar items, or an icons only 7 item bar. Fix: 3 or 4 labelled tabs plus a broken out primary action, or make the sidebar the home page.
- Tap targets under 44px. Fix: tab cells about 72 x 48px.
- Sidebar turned into a page that is all left aligned and lopsided. Fix: recent items at top, counts on the right.
- 2D dashboard grids ported to mobile. Fix: one scroll direction per section.
- Cards inside cards (padding on padding). Fix: group with white space and a section header.
- Editor or settings screens cluttered with recents or suggested templates. Fix: one screen does one thing, put extras on another page or in a sheet.
- Navigating away to a full page for a small sub task. Fix: bottom sheet.
- Persistent nav and actions on every screen. Fix: contextual actions that animate in and out.
- Only designing the full ideal state. Fix: design first run and no results states.
- A no results message like "Please try again". Fix: illustration, acknowledgement, typo suggestion, exit action.
- Many per section empty cards each with its own "Create" button on first run. Fix: one full screen empty state pointing at the main action.

## Quality checks

- Is every tap target at least 44px (bottom tabs about 48px tall, 72px wide)?
- Does the tab bar have 3 or 4 items (5 max)? Is the primary action broken out?
- Is body text at least 17px? Next to a Spotify or Apple screenshot at the same zoom, is my type as large and my spacing as generous?
- Does each section scroll in only one direction? Does every carousel show a cut off last item?
- Is any card nested inside another card?
- Does this screen do one thing? Could any element move to its own page or a sheet?
- Does a secondary task keep context (bottom sheet) instead of a full navigation?
- Are actions contextual (tab bar hidden in the editor, only confirm and cancel in a picker)?
- Are gestures supported: swipe back with ~35% parallax, swipe down to dismiss sheets with background scale, long press menu with blur? Are non obvious gestures taught?
- Is there a first run empty state and a no results state with suggestion and exit action?
- Is the destructive action in a menu last and red?

## Psychology and why it works

- Fat fingers: touch needs physical size, so targets stay over 44px regardless of screen size.
- Mobile is viewed close but with lower acuity at arm's length and in motion, so platforms use a larger base (17px iOS vs 13px macOS); bigger text means less content, which forces prioritisation.
- One direction per section makes scrolling predictable; two directions at once is not possible to navigate with a thumb.
- Cards replace white space as a grouping cue when white space is scarce; nesting them wastes the very space they save.
- Bottom sheets keep the user in context, so they do not lose their place in the task.
- Parallax on swipe back and scaling behind sheets give spatial continuity: the user sees where they came from and where they will return.
- Long press blur focuses attention on the element and its actions.
- An empty state that points at one main action teaches the app's core loop on first run; a no results state with suggestions recovers from typos instead of dead ending.

## Everything cited

- **Apple iOS / macOS system fonts**: iOS base font size 17px, macOS 13px. Used to argue that mobile type gets larger, not smaller. Also shown: iOS lock screen media controls, iMessage, iOS long press previews ("dynamic preview like how iOS does it"), Apple Reminders "New Reminder" sheet (X and blue check layout), Apple's partial use of swipe up to search.
- **Notion**: example of the sidebar becoming the home page, with a big bottom search bar / action button ("Ask AI" pill, search and compose buttons). Notion onboarding also appears in Mobbin.
- **Spotify**: shown beside his design as the reference for real mobile type size and density.
- **Slack**: uses swipe up to search.
- **Mobbin** (mobbin.com, sponsor): curated library of hundreds of thousands of screenshots, videos and user flows from top apps (Notion, Craft, Headspace and more). He uses it all the time and used it to make this video, to see how top teams design flows like onboarding and to check specific UI elements like bottom sheets. Filters: categories, screens, UI elements, user flows. 20% off via his link.
- **Craft** and **Headspace**: named as apps in Mobbin. Craft ("AI powered docs & second brain") onboarding screens shown.
- Apps visible in Mobbin: Polestar, Pinterest, Paramount+, Pangea Charging, Beside, Reminders, Apple Wallet, State Farm, TheFork, Viator, TIDE, Todoist.
- Dribbble style dashboards shown as two direction layouts: "Donezo" dashboard, a "Codename.com" sales CRM, a "Twisty" income tracker. A green investment app ("Your investment is on its way") shown near the end.
- **Figma**: all assets of the video are in a Figma file linked in the description.

## Memorable quotes

- "Five links down here is pretty much the definite limit, and three or four is much more ideal."
- "We'll always maintain over a 44 pixel target since people do have fat fingers."
- "iOS actually has a base font size of 17 pixels, while macOS has a base of only 13 pixels."
- "On mobile, you can choose one direction to move in per section."
- "Avoid double nesting them... it creates padding on padding."
- "One screen does one thing, and that's it."
- "Don't reach for a different layout, reach for a different page altogether."
- "The long press, the mobile equivalent of the right click."
- "How these actions animate in and out is half the fun."
