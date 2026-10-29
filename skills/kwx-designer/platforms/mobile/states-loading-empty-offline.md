# States: launch, loading, empty, error, offline, refresh

Most screens spend a large part of their life in a state that is not "full of data and working". A premium app designs every one of them. Sources: Apple HIG (launching, loading, onboarding, progress indicators, feedback, undo), NN/g (response time limits, skeleton screens, empty states), KDE "Simple by default", Superhuman speed post, Flighty and Halide "Behind the Design".

## Contents

1. Response time budget
2. Launch
3. Loading: pick the right indicator
4. Skeletons done right
5. Empty states
6. Errors
7. Offline and poor network
8. Pull to refresh and live data
9. Optimistic actions and undo
10. Onboarding and permission prompts
11. State matrix test

## 1. Response time budget

| Delay | What the user feels | What to show |
|---|---|---|
| < 100 ms | Instant, direct manipulation | Just the result. Target for taps, toggles, navigation. Superhuman aims for < 50 ms |
| 100 ms to 1 s | Noticed, flow kept | Nothing extra; press state and transition cover it |
| 1 to 2 s | Starting to wait | A subtle indicator; avoid flashing a spinner for a 300 ms load |
| 2 to 10 s | Waiting | Skeleton (full screen) or spinner (one module) |
| > 10 s | Attention lost | Determinate progress, a time estimate, a way to cancel, and let them leave the screen |

Rules:

- Do not show any indicator for loads under about 1 s; it causes flicker (NN/g). Delay the indicator by 300 to 500 ms and, once shown, keep it at least 500 ms so it does not blink.
- KDE: show progress for any task that takes longer than one second.
- Spinner is the last resort: it shows that something is happening but not what. If you know the steps, name them ("Uploading 3 of 12").

## 2. Launch

- Launch instantly. The iOS launch screen must look almost identical to the first screen (same background, bars, no text, no logo unless the first screen has it). It is not a splash or a branding moment (HIG).
- Restore state: reopen on the same tab, scroll position, draft and selection the user left (HIG).
- No splash screen that delays use. If you need branding, put it in onboarding, briefly.
- Match the current appearance (light or dark) and orientation from the first frame.

## 3. Loading: pick the right indicator

| Scope and length | Use |
|---|---|
| Whole screen, 1 to 10 s, layout known | Skeleton |
| One card or module, 2 to 10 s | Spinner inside that module, rest of screen usable |
| Over 10 s, or a file transfer | Determinate progress bar with estimate and Cancel |
| Unknown length, many items | Running count of items processed |
| Background sync | Small inline status ("Syncing 12 items"), never a blocking modal |

- Show something as soon as possible: cached content, placeholders, the chrome (HIG). Never a blank white screen.
- Let people do other things while it loads (HIG). Loading one tab must not block switching tabs.
- Load in place. Keep bars, titles and already known data visible; only the unknown part shows a placeholder.

## 4. Skeletons done right

- Use skeletons only for full page or full list loads under about 10 s (NN/g).
- Mirror the real layout: same row heights, same image boxes, text bars at about 60 to 80 percent of the real line width, the real number of rows that fit. A skeleton that does not match causes a layout jump when data arrives.
- Static or a very subtle shimmer (one slow pass, low contrast). Strong shimmer distracts and fails Reduce Motion.
- Do not use "frame only" skeletons (just header and footer); they work like a spinner and hide the structure.
- A skeleton is not a fix for slow code. Cache, prefetch and render progressively first.

Bad: a centered spinner on white for a feed that always has the same card layout. Good: five grey card shapes with avatar circles and two text bars, replaced row by row as data arrives, no shift.

## 5. Empty states

Three kinds, each needs its own design:

| Kind | Content |
|---|---|
| First use (nothing created yet) | What this place is for, one sentence, and the primary button that fills it ("New list") |
| User cleared it (inbox zero, all done) | A calm confirmation; no call to action needed; optional small reward |
| No results (search, filter) | Echo the query, say nothing matched, offer to clear filters or try a broader search |

Rules:

- Never leave a container blank. Blank means "loading? broken? empty?" (NN/g).
- Never show "No items" while still loading. It destroys trust when items then appear (NN/g). Empty is only shown after the load completes.
- Teach in context: "Star a project to pin it here" teaches the feature on the spot (NN/g).
- KDE: placeholder = icon + explanatory text + ideally a button to proceed.
- Do not hide or disable a tab because its section is empty; explain inside (HIG tab bars).
- Keep it short: one icon, one line of title, one line of body, one button. No marketing copy.

## 6. Errors

- Say what happened, why if known, and what the user can do, in plain words. Bad: "Error 500". Good: "Could not load messages. Check your connection, then try again." plus a Retry button.
- Show errors where they happened: inline under the field, inside the failed card, not a global alert for a local problem.
- Keep the user's input. A failed submit must never clear the form.
- Validate fields after the user leaves the field or submits, not on every keystroke while they type.
- Destructive or irreversible errors get alerts; recoverable ones get inline messages or a snackbar with an action.
- Avoid timed error toasts that vanish before a distracted user reads them (Hoober); errors stay until resolved or dismissed.

## 7. Offline and poor network

- Assume the network will vanish. Flighty designs for this explicitly: "Whenever someone takes off, we have to assume that we won't see them again until they land." Its Live Activity switches to a progress view that works without live data.
- Cache what the user saw last and show it offline, marked with when it was last updated ("Updated 10 min ago").
- Queue writes locally and sync later (local first). Show a small per item pending mark, not a modal. Superhuman keeps a local database so mail opens instantly even offline.
- Show one quiet, persistent offline indicator (a banner under the top bar or a status pill), not an alert per request.
- Disable only what truly needs the network, and say why on tap ("Needs a connection").
- When connection returns, sync silently and only surface conflicts.
- Never lose a draft because the request failed.

## 8. Pull to refresh and live data

- Offer pull to refresh on lists that change from the server (feeds, mail). Not on content that updates live or is local only.
- The spinner appears in the overscroll area, the list stays where it was, and new items insert at the top without moving what the user is reading. If many new items arrive while the user reads, show a "12 new posts" pill instead of jumping.
- Refresh also happens automatically on foreground if data is stale; pull is the manual override, not the only way.
- Live data (scores, flights, deliveries): update in place with a short, subtle highlight, and use the platform surfaces (Live Activities, widgets) so the user does not need to open the app. Flighty: "There's something comforting about information always being there."

## 9. Optimistic actions and undo

- For actions that almost always succeed (like, archive, mark done, reorder), update the UI instantly and sync in the background. Roll back visibly with a message if the server rejects.
- Prefer undo to confirmation for frequent, reversible actions (Hoober, HIG). A snackbar "Archived. Undo" for about 4 to 10 s, and a way to undo later.
- Confirm only for rare, costly, irreversible actions, and name the object ("Delete 'Q3 Report'?"). The destructive button names the action ("Delete"), not "OK".
- Undo is unlimited where possible and shows what it undid (HIG). On iOS describe the action in the shake to undo alert.
- KDE: move files to trash, do not delete immediately.

## 10. Onboarding and permission prompts

- Ideally the app explains itself through use. If onboarding is needed: short, optional, interactive, and never shown again after skip (HIG).
- Prefer contextual tips at the moment a feature is relevant over a front loaded tour.
- Provide sensible defaults so people start immediately; postpone setup (HIG).
- Ask for a permission only when the user triggers the feature that needs it, with a one sentence reason before the system prompt. Never ask for camera, location and notifications on first launch in a row.
- Show something actionable on first launch (KDE). An empty first screen needs a clear "start here" button.

## 11. State matrix test

For every screen, fill this table and design each cell before shipping:

| State | Designed? |
|---|---|
| First use (empty, never had data) | |
| Loading (first load, < 1 s, 1 to 10 s, > 10 s) | |
| Loaded, normal amount | |
| Loaded, one item / very many items / very long text | |
| Cleared (user emptied it) | |
| No results for search or filter | |
| Error (recoverable, with retry) | |
| Offline with cache / offline without cache | |
| Partial (some sections failed) | |
| Permission denied | |
| Refreshing while showing data | |

Fail the screen if any cell is "falls back to a blank view or a generic spinner".
