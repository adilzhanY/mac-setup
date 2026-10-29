# Mobile navigation

How people move between places in a phone or tablet app, and how to choose the right structure. Sources: Apple HIG (tab bars, toolbars, sidebars, sheets, modality, split views, 2026 revision), Material 3 component docs and Compose adaptive navigation, NN/g hidden navigation study, Hoober touch research.

## Contents

1. Pick the structure first
2. Bottom navigation (tab bar / navigation bar)
3. Top bars, titles and back
4. Hierarchy, drill down and split views
5. Sheets, dialogs and modality
6. Menus, overflow and hidden navigation
7. Search as navigation
8. Adapting navigation to bigger windows
9. Tests

## 1. Pick the structure first

| App shape | Use | Example |
|---|---|---|
| 2 to 5 peer sections, used often | Bottom tab bar / navigation bar | Clock, Music, Instagram |
| One main list with deep items | Single stack with drill down, no tabs | Settings, Mail on iPhone |
| One dominant task with tools | Full-screen canvas plus toolbar and sheets | Camera, Maps, Halide |
| More than 5 peer sections | Tab bar with the 4 most used plus a "More" or profile tab; on tablet a sidebar | Files, Music library on iPad |
| Linear task | Flow with a progress indicator, presented modally | Checkout, onboarding |

Rule: write the top level destinations as a list of nouns before drawing anything. If you cannot name each in one word, the structure is not ready.

## 2. Bottom navigation (tab bar / navigation bar)

- Use it for navigation only, never for actions (HIG). "Compose" or "Add" is a button or FAB, not a tab. Bad: a center "+" tab that opens a sheet. Good: a toolbar or FAB "+" inside the relevant tab.
- 3 to 5 destinations on Android (Material). iOS has no hard number, but more than 5 makes the system turn the last into "More"; avoid that overflow (HIG).
- Every tab has an icon and a one word label. Prefer filled icons for the selected tab on iOS; Material shows an active indicator pill behind the selected icon (behind icon plus label in the horizontal item layout).
- Keep the bar visible on every screen inside the section. Hide it only under a modal (HIG). People forget where they are when it vanishes.
- Never disable or hide a tab because its content is empty. Show the tab and explain the empty state inside it (HIG).
- Each tab keeps its own navigation stack. Switching tabs and back returns to where the user was, not to the tab root.
- Tapping the already selected tab pops its stack to the root; tapping again at the root scrolls to top. Users rely on this on both platforms.
- Badges only for something that needs attention (unread messages), not marketing. A red count badge on "Explore" is noise.
- iOS 26: the tab bar floats on Liquid Glass and can minimize while scrolling, with an accessory (like a mini player) moving inline. A dedicated search tab may sit at the trailing end.
- Android: bar height 64 dp (M3 Expressive flexible bar) or 80 dp (baseline). On medium windows use the horizontal item layout (icon beside label) or switch to a rail.

## 3. Top bars, titles and back

- Every pushed screen has a back control in the leading corner and supports the edge swipe (iOS) or system back (Android). The gesture supplements the button, never replaces it (HIG).
- Use the standard back chevron and close "X". Do not write "Back" or "Close" as a text label (HIG 2026 wording).
- Title: a word or short phrase, under 15 characters, never the app name (HIG). Large titles on iOS collapse to the inline title on scroll and come back at the top; use them on top level list screens, not on detail screens.
- One primary action per bar, on the trailing side, using the prominent style (Done, Send). Max three groups of toolbar items (HIG).
- Do not put a text button directly next to an icon button without space; they read as one control (HIG toolbars).
- Android: up arrow in the top app bar plus predictive back. Back must always be predictable: it leaves the current screen or closes the topmost sheet, never triggers an action.

## 4. Hierarchy, drill down and split views

- Depth of 3 levels (list, item, detail of item) is fine on a phone. Beyond 4, add search or shortcuts; people lose their place.
- Keep the path visible: the previous title appears beside the back chevron on iOS; on Android the top bar title names the current screen.
- On iPad and Android expanded widths, show list and detail side by side (split view / list-detail canonical layout). Persistently highlight the selected row in the list (HIG split views).
- When the window narrows from two panes to one, keep the detail visible and hide the list (Android canonical layout behavior). When it widens from list only, show a placeholder detail.
- Sidebars show at most two levels of hierarchy. Deeper data gets a middle content column (HIG sidebars).

## 5. Sheets, dialogs and modality

Use modality only when it clearly helps focus (HIG). Choose by task:

| Need | Component |
|---|---|
| Short scoped task, return to context after | Sheet (iOS page/form sheet, Android modal bottom sheet) |
| Tool palette that changes the content behind it | Nonmodal sheet at medium detent (Notes formatting) |
| Must decide now, two or three choices | Alert / dialog |
| Choose one of several actions on an item | Action sheet / menu |
| Long, multi step, or media | Full-screen modal |
| Transient confirmation | Snackbar / toast with Undo |

Rules:

- One sheet at a time. If a sheet needs another, close the first, then open the second (HIG, NN/g). Never stack sheets.
- Resizable sheets show a grabber and support the medium (about half height) and large detents. Use medium for progressive disclosure (share sheet); skip it when the task needs full height (compose).
- Support swipe down to dismiss, and also a visible Close or Cancel button for people who cannot or do not swipe (NN/g: swiping down is imprecise and can trigger Notification Center). Support system back on Android.
- If the sheet holds unsaved input and the user swipes it away, ask with an action sheet ("Discard changes?") instead of silently losing it (HIG).
- Button placement in an iOS sheet: Cancel on the leading edge, Done on the trailing edge. Pair Done with Cancel or Back, never Done alone. Never show Cancel, Done and Back together (HIG).
- Material bottom sheets: drag handle 32 x 4 dp, top corners 28 dp, scrim 32 percent for modal sheets, no scrim for standard sheets.
- Do not use a sheet for content people need to keep visible, or as a replacement for a normal page (NN/g).
- Avoid timed UI that dismisses itself. Prefer explicit dismissal (HIG cognitive guidance, Hoober).

## 6. Menus, overflow and hidden navigation

- Hidden navigation is used much less. NN/g mobile study (179 users, 6 sites): navigation was used by 89 percent on a site with visible plus collapsed navigation, versus 44 to 56 percent on sites with only a hamburger. Time to first use was also longer with hidden menus.
- Rule: show the 4 or 5 most important destinations visibly. Use a hamburger only for tertiary destinations, and label it ("Menu") if the audience is broad.
- Context menus (long press) are accelerators. Everything in them must also be reachable in the visible UI (HIG). Hide unavailable items in a context menu; dim them in a regular menu.
- Destructive items go last in a menu and use the destructive (red) style.
- iOS menu layouts: small (row of 4 icons on top), medium (row of 3 icons with short labels), large (list, default). Use medium when three actions dominate.
- More menu / overflow: put least important actions there, never the primary one.

## 7. Search as navigation

- If the content set is larger than about 50 items, search is navigation, not a feature. Put it where the thumb can reach it (iOS 26 bottom search field / trailing search tab, Android top search bar 56 dp).
- Show recent searches and suggestions on focus; show results as you type; keep the query when the user goes back from a result.
- Pull down to search (Things 3 on iOS) is a delightful accelerator but needs a visible entry point too.

## 8. Adapting navigation to bigger windows

| Width | iOS / iPadOS | Android |
|---|---|---|
| Compact | Tab bar at bottom | Navigation bar at bottom |
| Medium (600 to 839 dp) | Tab bar at top on iPad, can convert to sidebar | Navigation rail on the leading edge (80 to 96 dp) |
| Expanded (840 dp +) | Sidebar (sidebarAdaptable tab view) plus split view | Rail, expanded rail (220 to 360 dp) or permanent drawer; M3 Expressive replaces the drawer with the expanded rail |

- Keep the same destinations and order in every form. Only the container changes (HIG: keep functionality, change visibility).
- If users can customize the iPad tab bar, default to five or fewer items so compact and regular stay continuous (HIG).
- Phone landscape is compact height: keep the bottom bar, do not add a rail, keep sheets short.

## 9. Tests

- Name each top level destination in one word. Fails if any needs two.
- Count taps from launch to the three most common tasks. More than 3 taps for a daily task fails.
- Press back (or swipe) from every screen. Each press must go to the screen the user expects, close the topmost layer first, and never perform an action.
- Rotate, resize to split view and back. Selection, scroll position and stack survive.
- Turn off gestures mentally: every swipe action (dismiss, back, delete) also has a visible control.
