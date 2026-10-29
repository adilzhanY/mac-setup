# States, feedback and failure

"Every interaction needs a response" (Kole Jain, every UI concept). And the strongest premium evidence lives in the states AI tools skip: system status, undo, and recovery from errors (Tim Gabe, premium apps). A screen is not done until every state below is designed with the same care as the happy case.

## Contents

1. The three questions for every action
2. Interactive element states
3. Feedback for actions with no visible result
4. Loading
5. Empty states
6. Error states
7. Limit and quota states
8. Failure as the premium proof
9. Undo and reversibility
10. Break it on purpose
11. Checks

---

## 1. The three questions for every action

Walk the core flow. For every action the user can take, the UI must answer:

1. **What just happened?** Visible status: the tap registered, the save completed, the upload is at 40%.
2. **Can I take it back?** Undo, back, cancel, or an edit path.
3. **What do I do next?** The next step is obvious.

"Just that hand holding can get you really far." The Design Theater study (31 Jul 2026, cited by Tim Gabe) found five AI building tools explained their design choices confidently but "about a quarter of that reasoning never made it into the interface", and the parts dropped were exactly these: visibility of system status, user control and freedom, error prevention and recovery.

## 2. Interactive element states

| Element | Required states |
|---|---|
| Button | Default, hover, pressed (slightly darker, slightly smaller), disabled (grey fill, grey text), loading (spinner) when it starts async work |
| Input | Default, hover, focus (accent border plus ring), filled, error (red border plus message), warning (yellow border plus message with link), disabled, loading |
| Nav item | Default (ghost), hover (light fill), active (highlight), focus |
| Toggle, segmented, tab | Off, on, hover, focus, disabled; selected shown with a distinct surface (white pill plus soft shadow on a grey track) |
| List row | Default, hover (light fill), selected, inactive (greyed), dragging if draggable |
| Icon only control | All of the button states plus a tooltip |

Signifiers (Kole Jain): a container groups, a raised inner pill means selected, greyed text and icon together means inactive. Never leave an inactive item looking clickable.

## 3. Feedback for actions with no visible result

1. Copy, save, bookmark, send: confirm in place. The copy row example: hover gives a grey pill, click has a press state, "but you still do not know anything was copied". Fix: a small black chip "Copied!" with a green check slides up in place.
2. A success message when a long action completes: a dark toast "Update installed! v4.3" with a green check.
3. Long running work shows progress with a time estimate: "Update installing... v4.3", green progress bar, "8m 32s left", with a ghost "Cancel".
4. Keyboard shortcut pressed: the keycaps light up, then confirm (the "Quick access your datasets" modal).
5. Feedback appears where the user is looking (at the control), not in a far corner, unless it is a global event.

## 4. Loading

1. Under about 300 ms: show nothing extra. Longer: skeleton for content in a known layout, spinner for an action, a determinate bar when the length is known.
2. Keep the layout stable: a skeleton has the same size as the content it replaces.
3. Splash or slow loads you cannot speed up: progress feedback so it feels faster ("splash sucks. We need to use some loading bar UX tactics to ensure it feels faster even though the time to load the card info is pretty much the same", Tim Gabe's crypto client notes).
4. Remove steps a better mechanism replaces (a 2FA code input replaced by Face ID).
5. Optimistic updates for cheap, reversible actions; roll back with a clear message on failure.

## 5. Empty states

"What was designed is the ideal state. First login has no content" (Kole Jain, mobile UI).

**First run**

1. Prefer one full screen empty state that points at the primary action over many per section empty cards. Notely: "Get started with Notely / Add notes, calendar events, tasks files and more with the action bar", a hand drawn arrow pointing at the "+".
2. Rejected version: per section cards, each with a tinted icon, "No tasks yet. Add some!" and its own "Create Task" button.
3. Follow with one dismissible tip: "Quick Start" with a lightbulb icon and close X, "Start by selecting either a note, event, or task. We'll default to creating a note.", buttons "Settings" and "Dismiss".
4. A metric that is 0 on a new account is an empty state, not a big "0".

**No results**

1. An illustration (muted), the count ("0 results"), an acknowledgement ("Oops, nothing found / Your search didn't turn anything up"), a typo suggestion as a link ("Did you mean 'Sprint'?"), and an action that exits the empty state ("Start a New Note").
2. Never a bare "Please try again".
3. Keep the filters visible so the user can widen the search.

**Cleared** (inbox zero, all tasks done): a calm confirmation, not the first run teaching state.

## 6. Error states

1. Say the likely cause, what to do now, and give a direct path to a human on the same screen: "Your payment at Coffee Shop was declined. Please check your balance." plus a "Contact support" button.
2. Tailor the message to the reason. A low balance decline gets its own message and push ("Low balance for example is a very common occurrence that deserves a special push").
3. In money or trust moments, make the failed item unmistakable but calm: the amount struck through ("~~100~~ USDC"), a small coloured status pill ("Declined"), full details (date and time, amount, card, transaction ID with a copy icon, category), and the recovery action pinned at the bottom.
4. Keep the user's input and place. Never dump them on a dead page.
5. Offline: say it, keep what can work offline working, queue what can be queued, retry automatically when the connection returns.
6. Use semantic colour: red for error, yellow for warning, blue for info, green for success. Toasts pair the icon with two actions ("Help center / Retry", "Learn more / Done").
7. Never answer user effort with nothing. Undertone's mic test gave "Looks like we didn't get enough content!"; the founder: "I was expecting anything instead of nothing." Give something back, say it did not cost a session, show the next step.

## 7. Limit and quota states

Write limits as facts, not slogans (Undertone, Tim Gabe):

| Old | New |
|---|---|
| Bold headline "Keep every session within reach!" (an upsell slogan) | Small badge "2/2 SESSIONS USED" on a faint pill |
| "You've used all your sessions for this period. Please wait until your next period starts, or upgrade..." | Plain regular weight headline "You've used both sessions this month", no exclamation mark |
| No count, no date | "On **September 12**, your sessions will be refreshed." with the date emphasised |
| Two different screens for the same state (Upgrade + Close vs only Close) | One shared pattern, only the action varies |

"On the surface it's a really simple change, just a tiny bit of copywriting and visual structure, but it makes a world of difference at scale."

## 8. Failure as the premium proof

- Service recovery paradox (a 2007 review, cited by Tim Gabe): a failure handled really well can leave people as happy as if nothing went wrong, or happier. Failure "is where premium stops being an opinion".
- Chrome's offline dino (2014): instead of a dead page, a pixel T rex and "Press space to play". Four years on it was played about 270 million times a month. Delight belongs in the worst moment, not on the home screen.
- About a third of people leave after one bad experience (PwC 2018).
- Result at the crypto card client after the declined payment redesign plus other moves: new accounts +60%, money loaded +79%.
- Failure states are "one of the cheapest places to buy that feeling of premium quality", because most teams skip them.

## 9. Undo and reversibility

1. Every destructive or significant action has an undo or a way back. Prefer undo (a toast with "Undo" for several seconds) over a confirm dialog for reversible actions.
2. Confirm dialogs only for irreversible, high cost actions. Name the object and the consequence ("Delete 'Q3 report'? This cannot be undone."); the destructive button is red and says the verb ("Delete"); default focus on Cancel.
3. Destructive items in menus come last, in red with a red icon.
4. Long forms autosave drafts.

## 10. Break it on purpose

Before calling any flow done (Tim Gabe): turn off Wi-Fi mid flow, fail a payment, empty every list, then design what you see. Also: the slowest realistic network, the longest realistic text, a missing image, a permission denied, a session expired, a double tap on submit.

## 11. Checks

| Check | Pass when | Verify in code |
|---|---|---|
| State inventory | Each screen has loading, empty, error (and offline, limit where relevant) branches | Read the render function; find each branch, not only `data && ...` |
| Button states | The button component defines hover, pressed, disabled, loading | Read its variants |
| Async feedback | Every mutation sets a pending state shown in the UI | Each `mutate`/`fetch` call toggles a visible flag |
| Silent actions confirmed | Copy, save, send show a confirmation | Find the handler; it triggers a toast or chip |
| Errors specific | Error branches map reasons to messages; no single generic string | Read the error mapping |
| Support path | Money and account errors render a support action | Find the button in those error views |
| Limit copy | Limit screens show count, factual headline, exact reset date | Read the strings; a date variable is interpolated |
| One pattern | Same state uses one component across screens | `grep` for duplicate limit/empty components |
| Undo | Destructive actions have undo or a confirm with the object name | Read destructive handlers |
| Effort never yields nothing | Every "not enough input" branch returns something useful and a next step | Read those branches |
