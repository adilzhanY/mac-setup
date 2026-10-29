# Onboarding

"You're not hiding functionality, you're sequencing it so that the user is never overwhelmed" (Kole Jain, dashboard flaws). Onboarding is progressive disclosure in time: one step, one tooltip, one win, then the next. The account wall comes after value, not before.

## Contents

1. Goal first
2. The order
3. Never do this
4. Sign up inside onboarding
5. Teaching the interface: tooltips and checklists
6. First run empty state
7. Identity and verification flows
8. Research before designing
9. Checks

---

## 1. Goal first

Write the business goal and the user problem before any screen. The workshop board in Tim Gabe's video uses timed rounds: 4 min business goal, 10 min problems (as "How might we" notes), 2 min present, 4 min vote and discuss, 2 min decide. Example goal: "Ensure 80% of users experience the product's core value within their first two sessions." Example HMW: "...surface the most valuable features early without overwhelming or distracting new users?"

Then rate each existing step "It sucks / It's OK / It's good" with a note on why (the crypto card onboarding: splash, login and 2FA, Face ID setup, KYC, walkthrough).

## 2. The order

1. **Choose**: one meaningful choice (language, goal, use case). Preselect the most common answer.
2. **Commit**: a small commitment (a goal, a schedule).
3. **Achieve**: a first real win in the product (the first lesson, the first report, the first note).
4. **Save**: account creation, framed as keeping that win.
5. **Expand**: teach the next feature when the user reaches for it.

This is the Duolingo sequence (language, goals, first lesson, then sign up, about 10 minutes invested) as shown by uxpeak.

## 3. Never do this

- A six bullet welcome modal at login. It is "forgotten the moment it is dismissed".
- A first screen that says "Log in or create an account to get started" before the user has seen anything.
- A fully loaded dashboard for a brand new user.
- Results blurred behind "Sign up to unlock".
- A progress bar that starts at "0% Complete" with five empty dots after the user already signed up.
- A tour that forces ten steps of Next, Next, Next before the user may touch anything.
- Steps that a better mechanism replaces (a 2FA code input when Face ID works).

## 4. Sign up inside onboarding

1. Treat sign up as step 1 of onboarding, counted as done in the progress stepper (Sign up, Profile, Photo, Verify, Done, starting at 20%). Count only real steps.
2. Let the user customise something before the account wall, with a live preview that updates as they choose ("Design Your Profile": name, title, colour palette swatches, card style tiles Soft / Dark / Minimal).
3. Ask after a completed win: "That's a wrap / The anchor effect, done in 6 minutes", then "Don't lose tonight's work" listing what is unsaved (score, streak, XP), when that is true.
4. The button says what it does. If it creates an account, the label or the line under it says so.
5. Encouraging, factual progress copy: "Just a few more details to complete your account setup".

## 5. Teaching the interface: tooltips and checklists

**Tooltip on the key action** (Kole Jain, dashboard flaws)

- Start with a single tooltip on the most important action, anchored to the real control.
- Anatomy: dark card, a small illustration of the action (a skeleton row with a text cursor), a short title ("Add a row"), one line of help ("Easily add or insert new rows into your data tables"), a "Dismiss" button.
- Then a second tooltip, or a checklist. Never more than one tooltip on screen.

**Getting started checklist**

- Floating card in the lower right corner, collapsible with a chevron.
- Done items: filled accent check, struck through grey text. Open items: empty dashed circle.
- A quiet "Watch tutorial" button with a play icon.
- Footer "4 of 6 complete" with a progress bar.
- Items link to the control that completes them and tick themselves when the user does the action anywhere.

**Quick start popover** (Kole Jain, mobile UI): blue tooltip with a lightbulb icon and close X: "Start by selecting either a note, event, or task. We'll default to creating a note." Buttons "Settings" and "Dismiss". Note the default stated in the tip: the product picks for the user.

**Gestures**: if the product relies on a non obvious gesture (swipe up to search), teach it once, in context, the first time it would help.

## 6. First run empty state

One full screen empty state pointing at the primary action beats per section empty cards: "Get started with Notely / Add notes, calendar events, tasks files and more with the action bar" with an arrow to the "+". It teaches the core loop on first run.

## 7. Identity and verification flows

The neobank KYC flow (generated from Mobbin patterns in the Tim Gabe video) shows the patterns that are now the floor, so get them all right:

1. Intro: "Verify your identity, takes about 3 minutes", numbered steps (Scan your ID, Take a selfie, Get verified), privacy reassurance, one CTA "Start verification".
2. Document scan: 3 step stepper header, dashed capture frame, a "Make sure that" checklist (not expired, entire document fits, clear with no glare, all text readable), "Open camera" plus "Upload from photo library".
3. Liveness: dark full screen camera, oval face guide, "Center your face within the oval", minimal chrome.
4. Then go past the floor: a real time estimate from your data, a specific message for each rejection reason, a way to resume later, and a human path when verification fails.

## 8. Research before designing

Before designing any onboarding flow, study how strong products already solve it: search "onboarding" in a pattern library such as Mobbin, across the full journey (first screen, permission prompts, sign up, first win, upgrade). Examples cited: Duolingo, Forest ("Welcome To Forest! Ready to Focus?"), LinkedIn, Linear and Arcade onboarding flows, Notion's notification permission prompt. Look at the order of steps and what they ask for, not only at the styling.

## 9. Checks

| Check | Pass when | Verify in code |
|---|---|---|
| Value before account | The first win is reachable without an account (unless identity is the product) | Follow the routes; no auth guard before the first result |
| One teaching element at a time | At most one tooltip or coach mark is visible | Read the onboarding state machine |
| No welcome modal wall | No modal with a list of features opens on first login | Search for first login modals |
| Real progress | Stepper starts at completed real steps | Progress computed from step state |
| Checklist works | Items route to controls and auto complete | Each item has a target and listens to the event |
| Dismiss persists | Dismissed tips do not return | A stored flag per tip |
| First run state | New accounts see a designed empty state pointing at the main action | Find the zero data branch of the home screen |
| Time estimates true | "Takes about 3 minutes" comes from measured data | Ask for or find the source |
