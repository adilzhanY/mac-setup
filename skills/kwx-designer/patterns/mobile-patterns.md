# Mobile patterns

Patterns from the videos, mainly Kole Jain's mobile UI video (the "Notely" notes app translated from a desktop dashboard to a phone) and the uxpeak strawberry redesign. Platform foundations (safe areas, system controls, iOS vs Android) live in the platform folder; this file is the patterns. Core idea: mobile is not a shrunk desktop. Type and spacing stay the same or grow, so you show far less, and one screen does one thing.

Numbers marked (est.) were read off video frames, not stated.

## Contents

1. Navigation: tab bar or sidebar as home
2. Top bar actions
3. Type and density
4. Layout: one scroll direction, four blocks, no nested cards
5. One screen does one thing
6. Bottom sheets
7. The primary action button
8. Contextual actions
9. Gestures
10. Long scroll pages: sticky action, sticky title
11. Empty states
12. Checks

---

## 1. Navigation: tab bar or sidebar as home

**Option 1: bottom tab bar** (when the destinations reduce to a few key icons)

1. 3 or 4 tabs is ideal, 5 is "pretty much the definite limit". An icon only 7 item bar is wrong.
2. Modern default: a floating pill bar inset from the screen edges, with the primary action broken out as a separate round "+" button beside it.
3. Tab cell 72 px wide x 48 px tall (annotated). Icon about 24 px above a short label about 12 to 13 px (est.).
4. Tap targets always over 44 px, "since people do have fat fingers".
5. Active tab: a lighter pill highlight filling the cell, not only a colour change.

**Option 2: the sidebar becomes the home page** (when there are too many important destinations)

1. The sidebar list becomes a full screen (Overview, Notes, Calendar, Tasks, Files, Templates, then Notebook, Tags, Shared with me). Notion does this.
2. Avoid the lopsided look (everything on the left): add recent items as small horizontal cards at the top, and right aligned counts and badges on rows (Notes 13, Tasks 9, Files 132, "new" on Shared with me).
3. The free bottom gets a large "Search for anything..." pill and a round "+" button.

## 2. Top bar actions

1. Top actions are contextual per page. For home, a bell plus a "..." more menu grouped in one small pill at the top right is a good default.
2. Detail pages: a round back button top left, share plus more in a pill top right.
3. Over a photo hero, each icon sits in a white circular container with a thin outline so it reads on any image (uxpeak).

## 3. Type and density

1. Do not shrink type for mobile. iOS base size is 17 px, macOS 13 px: "more often than not, things actually get larger on these smaller screens".
2. Validate density against a real top app: put your screen next to a Spotify (or Apple) screenshot at the same zoom. If your text is smaller or denser, scale it up. Kole's first calendar attempt looked fine alone and visibly small next to Spotify.
3. Bigger text means less content. A desktop dashboard had five panels; on mobile "you can pick one of those things".

## 4. Layout: one scroll direction, four blocks, no nested cards

1. Each section scrolls in one direction: vertical stack or horizontal carousel, never a 2D grid that extends both ways.
2. A horizontal carousel cuts the last card off at the screen edge so the scroll is obvious.
3. Four building blocks: cards (the main grouping tool, because white space is scarce), text or links, images, inputs.
4. Do not nest cards inside cards. Note cards inside a Notes container card create "padding on padding" that cramps width. Group the set with a section header ("Notes >") and white space instead.
5. Section headers: "Title >" tappable with a chevron, optional text tabs on the right ("Recents / Suggested").
6. Date group labels small caps: today in red ("FRIDAY, FEB 27"), "TOMORROW" in grey. Events with a 3 px coloured left bar; the current event row gets a faint tinted background.

## 5. One screen does one thing

1. Home is the exception. Otherwise "the settings is just settings, and the notes editor is just a notes editor".
2. No recent notes or suggested templates wedged into a focused screen. The cluttered editor had a Templates gallery between the properties and the body; the clean editor: back button, share and "..." pill, large bold title, property rows (Status with a purple "In progress" chip, "+ Add field"), a hairline divider, the body.
3. "Whenever you need to add something new, don't reach for a different layout, reach for a different page altogether."
4. For a short side task that must keep context, use a bottom sheet (next section).

## 6. Bottom sheets

1. Use a sheet when a sub task must not rip the user away (choosing a template while editing).
2. Anatomy: centred title ("Templates"), optional full width search field, the content (a 2 column thumbnail grid with captions), a round X at the top left (cancel, neutral grey) and a round check at the top right (confirm, accent). Apple Reminders' "New Reminder" sheet uses the same X and check layout.
3. Any height, always dismissible by swipe down.
4. As the sheet rises, scale the page behind it down slightly; scale it back up on dismiss.

## 7. The primary action button

1. The round "+" either opens a small menu of types, or opens straight into an input so the user can start typing.
2. The composer pattern: a "What's up?" input with a round accent send button, a row of type icons (note, calendar, task), keyboard up, with a sensible default type ("We'll default to creating a note").

## 8. Contextual actions

1. Actions come and go with context. Opening a note hides the tab bar and shows editing actions: a small formatting toolbar pill at the bottom (more, list, format icons) plus a separate round undo button, share at the top.
2. A picker sheet reduces actions to confirm and cancel.
3. Animate actions in and out: "How these actions animate in and out is half the fun."

## 9. Gestures

1. Swipe right to go back. Offset the underlying page left by about 35% and slide it right as the top page leaves (parallax).
2. Swipe down dismisses sheets, with the background scaling back up.
3. Swipe up to search (Slack, partly Apple) and similar gestures can be relied on heavily only if you teach them.
4. Long press is "the mobile equivalent of the right click": blur the rest of the screen (including the tab bar), slightly zoom the pressed element, show an action menu next to it. Menu rows: label left, icon right aligned (Pin Note, Lock Note, Share Note, Note History), hairline separators, "Delete" last in red with a red trash icon. Going further: a live preview like iOS.
5. Every gesture has a visible alternative (a button or menu item) for users who do not discover it and for accessibility.

## 10. Long scroll pages: sticky action, sticky title (uxpeak)

1. Content card with rounded top corners overlapping the hero image; on scroll it slides up over the image.
2. Once the hero leaves, the title moves into the top bar and stays.
3. The buy area (stepper plus Add to cart with the total) stays pinned at the bottom.

## 11. Empty states

1. First run: one full screen empty state that points at the "+" ("Get started with Notely", a hand drawn arrow), not per section empty cards each with a "Create" button.
2. Then one dismissible "Quick Start" popover.
3. No results: muted illustration, "0 results", "Oops, nothing found / Your search didn't turn anything up. Did you mean 'Sprint'?" (link), and "Start a New Note". Never just "Please try again".
4. Search screen: filter chips (Recents, Notes, Tasks, Events, Scratch), recent rows with type icon and source in grey, relative time right aligned ("3h ago", "16h ago", "2d ago").

## 12. Checks

| Check | Pass when | Verify in code |
|---|---|---|
| Tab count | 3 to 4 tabs, 5 maximum | Count tab bar items |
| Tap targets | Every interactive element at least 44 x 44 px (tab cells about 72 x 48) | Read sizes of buttons, rows, icons with their padding |
| Body size | Body text at least 17 px on iOS (or the platform base) | Read the body type token |
| Density vs reference | Type and spacing match or exceed a top app at the same zoom | Compare token values with the reference's measured sizes |
| One direction | No section scrolls both ways | Read scroll containers: each is vertical or horizontal |
| Carousel hint | Last card is cut off at the edge | Card width times count exceeds the visible width with a partial card |
| No nested cards | No card component renders inside another card | Search the tree for card in card |
| One thing per screen | Focused screens contain no unrelated sections | Read the editor/settings screen children |
| Sheets dismiss | Swipe down and the X both close the sheet | Read the sheet props |
| Gesture fallback | Each gesture action also exists as a visible control | Map each gesture handler to a button or menu item |
| Destructive last and red | Delete is the last menu item and uses the danger token | Read the menu item order |
