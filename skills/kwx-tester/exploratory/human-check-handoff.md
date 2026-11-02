# Handing checks to a human

Some checks need eyes, a finger or a screen reader: does the label fit, is the focus ring visible, does TalkBack read the button, does the animation feel right. When the agent cannot or may not look (the user's rules forbid browsers, emulator input, screenshots or moving the pointer; or there is no device), it finishes everything it can check from code, scripts and logs, and then hands the rest to the owner as a short checklist. This file says when to hand over, how to write the shortest useful list, how to order it, and how to read the answers. It has examples for a web page, a mobile screen and a desktop panel.

## Contents

1. When to hand over
2. The rules that matter most
3. The checklist format
4. Choosing and ordering the items
5. Writing each line
6. Examples: web page, mobile screen, desktop panel
7. Reading the answers
8. Checks

## 1. When to hand over

Read the user's CLAUDE.md and the project's rules first. Then:

| Situation | Do |
|---|---|
| Rules forbid the agent to launch a browser, use browser automation or browser MCP | Do not launch it. Verify by type check, build, curl, DB queries and scripts; hand visual checks over |
| Rules forbid input into an emulator or phone (`adb shell input ...`) or moving the user's mouse and keyboard | Never inject input. Build and install if allowed, then hand the tapping over |
| Rules ask that visual tests happen on a specific workspace or monitor, or not at all | Follow them exactly; if not possible, hand over |
| A check needs a sense the agent does not have here: hearing a screen reader, feeling haptics, judging motion | Hand over |
| A check is about taste ("does it look right") | Hand to the owner, and to kwx-designer for the design side |
| The agent could check it from code or a script | Do it yourself; do not put it on the list |

The handoff comes **at the end** of the work, once, after every automated check passed. Never ask the owner to click while the agent is still changing code, and never ask them to set up capture tools or send screenshots during testing unless they offered.

## 2. The rules that matter most

| # | Rule | Why | Evidence |
|---|---|---|---|
| H1 | At most about 10 items. If there are more, keep the riskiest 10 and say what was left out. | Long lists get skimmed or skipped; the owner is not a QA team. | opinion (practice) |
| H2 | One line per check: where to go, what to do, what correct looks like. | The owner should not need to think about what you meant. | opinion |
| H3 | Order by risk: what would hurt users most if wrong comes first. | If the owner stops after three, the three most important are done. | moderate (risk based testing) |
| H4 | Describe correct in observable terms: "the whole label is visible on one or two lines, no '...'" not "the button looks fine". | A vague expectation gets a vague answer. | moderate (oracles, Bolton) |
| H5 | Ask for a short answer per item: ok, or what you saw. Number the items so the reply can be "all ok except 4: the text is cut". | Cheap to answer means it gets answered. | opinion |
| H6 | Give the exact starting point: URL, screen, keybind, account, data to use, setting to change. | Setting up is where most of the owner's time goes. | opinion |
| H7 | Say what the agent already verified, in one line, so the owner does not repeat it. | Trust, and no duplicated effort. | opinion |
| H8 | Put predictions from code on the list with the prediction: "I expect the label to wrap at 200 percent font; check it does not cut off". | It tells the owner where to look and tests the agent's model. | opinion |

## 3. The checklist format

```markdown
### Please check (about 3 minutes)

Already verified by me: build, type check, 42 unit tests, API responses for all states, contrast of all tokens (4.6:1 or more), labels and roles in code.

Setup: <how to open it, which account or data, any setting to change first>

1. <where> : <do what> -> <correct looks like>
2. ...

Reply with the numbers that were not ok and what you saw, for example "3: the toast covers the button". "All ok" is enough otherwise.
```

Keep it plain text and short enough to read on a phone. One paragraph lines (no hard wrapping inside an item), because the owner may copy it elsewhere.

## 4. Choosing and ordering the items

Pick candidates from:

1. Visual predictions from code that could be wrong (overflow, clipping, overlap, contrast over images).
2. States the agent could not render: empty, loading, error, offline, very long text, large font, dark mode, RTL.
3. Interaction that needs a person: keyboard walk, focus visibility, screen reader output, gestures, haptics, animations.
4. Platform behaviour: back button, rotation, app to background and return, notification tap, widget refresh.

Score each by **impact if wrong** (blocks a task, loses data, looks broken on a main screen, cosmetic) times **likelihood** (the agent's confidence in its prediction is low, the code is new, it broke before). Sort, keep the top 10, merge items on the same screen into one setup.

Group items by screen in visiting order after sorting by risk only when it does not push a high risk item below the cut. The owner's path should be short: one setup, then move through the screens once.

For any UI under test, turn each applicable entry of the owner's UI mistakes library (`~/.claude/ui-designer/mistakes.md`) into a check. Settle it from code where possible: text width against its box at the current scale, icon size against its disc, a fill against the surface behind it, siblings that must not wrap. Put only what code cannot settle on the human list, quoting the M-id (for example "3. (M3) Bluetooth device page: the device name shows in full, not elided, at scale 1.25").

## 5. Writing each line

Template: `<number>. <where> : <action> -> <correct looks like>`

| Weak line | Strong line |
|---|---|
| Check the settings page | Settings > Profile : type a 60 letter name and save -> the name shows in full on two lines, no "..." and nothing overlaps the Save button |
| Test dark mode | Phone in dark mode, Habits list : look at the "Done" chips -> chip text is readable, the chip border is visible against the background |
| See if the screen reader works | TalkBack on, Habits list : swipe right through the first row -> it says "Morning run, ticked, button" then "Delete habit Morning run, button" |
| Is the panel OK? | Super+N : open the panel and press Tab five times -> a visible ring moves through Wi-Fi, Bluetooth, Volume, Brightness, Close in that order |
| Check the error | Turn off Wi-Fi, tap Sync -> an error message in words appears under the button within 5 s, and the typed data is still there |

Rules for lines:

- Start with where: the URL, screen path, or keybind.
- One action per line, two at most.
- Correct is something you can see or hear, with a number when there is one (within 5 s, two lines, in this order).
- Use the same names the UI uses (copy the label text from code).
- No jargon: "the text is cut off with ..." not "truncation"; "the outline that shows where the keyboard is" the first time you say focus ring.

## 6. Examples

### Web page (Next.js pricing page, browsers off for the agent)

```markdown
### Please check (about 4 minutes)

Already verified by me: build and type check pass; `curl` shows all three plans and prices in the HTML; axe rules in the component tests pass; all text tokens have 4.5:1 contrast or more; every button has a name.

Setup: run `npm run dev`, open http://localhost:3000/pricing in Firefox.

1. /pricing at full width : click "Buy Pro" -> the checkout page opens with "Pro, 9 €/month" at the top.
2. /pricing : press Tab from the top of the page until "Buy Pro" -> every step shows a visible outline, the order is logo, nav links, the three plan buttons left to right, and the outline is never hidden under the sticky header.
3. Narrow the window to about 320 px (or zoom to 400 percent) -> the three plans stack in one column, no sideways scrolling, prices fully visible.
4. Ctrl + + three times (zoom 175 percent) on the plan cards -> the feature lists wrap, no text overlaps the buttons.
5. Switch the language menu to Русский -> plan names and prices fit on their buttons ("Купить Pro" on one line), prices show as "9 €" with a space.
6. Hover the (i) next to "Seats" then press Esc -> the tooltip appears, stays while the pointer is on it, and Esc closes it.

Reply with the numbers that were not ok and what you saw.
```

### Mobile screen (Expo app on the owner's phone or the one emulator; the agent may not inject input)

```markdown
### Please check (about 5 minutes)

Already verified by me: unit tests for streak logic (12, all green incl. time zone cases), API sync with two clients, plural forms for ru and kk, all icon buttons have accessibility labels in code.

Setup: install the dev build (`npx expo run:android` already built it), sign in as test@example.com / the test password from .env.test. Habits list has 3 habits.

1. Habits list : tick "Morning run" -> the tick fills, the streak badge goes up by 1, a short vibration.
2. Habits list : tick and untick the same habit fast 5 times -> it ends unticked and the streak returns to its old number.
3. Phone Settings > Display > Font size largest, back to Habits list -> habit names wrap to two lines, the streak badge is not cut, nothing overlaps.
4. TalkBack on, Habits list : swipe right through the first row -> it says the habit name, "ticked" or "not ticked", and "Delete habit <name>" for the trash icon.
5. Airplane mode on, tick a habit, airplane mode off, wait 10 s -> the tick is still there and a "Synced" message appears once.
6. Phone language Қазақша, open Stats -> month names in Kazakh (Қазан), "5 әдет" (no "-тер"), all letters drawn (no boxes).
7. Rotate the phone on the Stats screen -> the chart redraws, the selected month stays selected.
8. Press Home, wait 1 minute, reopen -> the same screen and scroll position.

Reply with the numbers that were not ok and what you saw.
```

### Desktop panel (Quickshell/QML panel on Hyprland; the agent may not move the pointer or focus windows)

```markdown
### Please check (about 2 minutes, after a shell reload)

Already verified by me: QML loads with no errors or warnings in the shell log; sizes computed from code at the current UI scale (longest label "Bluetooth: 2 connected" needs 182 px, the row gives 236 px); all text uses theme font sizes; the panel's IPC call returns the right state.

Setup: reload the shell, then use the keybind.

1. Super+N : open the panel -> it slides in from the top right, fully on screen, with the 5 px gap to the screen edge like the other panels.
2. In the panel : look at the Bluetooth row with your earbuds connected -> "Bluetooth: 2 connected" on one line, not cut off, icon centred in its circle.
3. In the panel : press Tab several times -> a visible ring moves through the toggles in order, Esc closes the panel.
4. Light theme (wait for the day theme or switch it) : open the panel -> all text and icons readable, toggle "on" and "off" states clearly different.
5. Hover the volume slider and scroll the wheel -> volume changes in steps, the OSD does not cover the panel.

Reply with the numbers that were not ok and what you saw.
```

## 7. Reading the answers

| Answer | Do |
|---|---|
| "All ok" | Record in the report: "owner confirmed items 1 to 6 on <date>". Close the related predictions. |
| "4 not ok: text cut" | Treat it as a bug report from the owner: write it up ([bug-reports.md](bug-reports.md)), find the cause in code, hand it to kwx-designer or kwx-developer, and add the defect to any mistakes library the user keeps (check the user's rules; some require UI defects to be logged as lessons). After the fix, send a new checklist with only the failed item and its neighbours. |
| A screenshot or description of something not on the list | Same as a bug; also ask whether the list should have caught it, and add that kind of item to future lists. |
| No answer | Do not block. Mark the items "not confirmed" in the report and in TODO.md if they matter. |
| "Can't check, no device" | Mark as not confirmed and name the risk in the report. |

Never claim a visual result is correct because the code looks right. Until the owner confirms, it is "predicted from code".

## 8. Checks

- [ ] The user's rules were read; nothing on the list is something the agent was allowed and able to check itself.
- [ ] The list was sent once, at the end, after all automated checks passed.
- [ ] At most about 10 numbered items, sorted by risk, with anything cut named.
- [ ] One setup paragraph with exact URLs, keybinds, accounts and data.
- [ ] Each line has where, action, and an observable correct result (with numbers where possible).
- [ ] An "already verified" line tells the owner what not to repeat.
- [ ] Predictions from code are stated as predictions.
- [ ] For UI under test, the applicable UI mistakes library entries were checked from code; the code check notes and the human list cite M-ids.
- [ ] The reply format is stated ("numbers that were not ok and what you saw").
- [ ] Answers were recorded in the report; failures became bug reports.
- [ ] No hard wrapped lines inside items; no em or en dashes.
