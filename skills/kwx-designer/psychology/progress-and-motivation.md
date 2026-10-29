# Progress and motivation: goal gradient, endowed progress, streaks

"0% feels like standing still. 20% feels like momentum." (uxpeak, UX psychology video). People speed up as a goal gets closer, and they judge closeness by what they see. Show real progress clearly, start the bar where the user really is, and never turn progress into guilt.

## Contents

1. The effects
2. Rules for progress indicators
3. Stepper anatomy
4. Checklists
5. Streaks (honest version)
6. Before and after
7. Forbidden
8. Checks

---

## 1. The effects

- **Goal gradient effect**: effort speeds up as the goal nears.
- **Endowed progress effect**: a car wash loyalty card. Group A: 8 empty stamps. Group B: 10 stamps with 2 already filled. Both need 8 washes. Group B completed at nearly double the rate (cited as "Columbia" by uxpeak; the numbers match Nunes and Dreze 2006, about 34% vs 19%). "You can choose where the starting line is."
- **Perceived progress counts**: the head start costs the user nothing, but it has to be honest (section 7).
- LinkedIn's profile strength meter is shown from sign up and never sits at zero (Beginner, Intermediate, All-Star).

## 2. Rules for progress indicators

1. Never start a user at 0% when they have already done something real. Count account creation, an email entered, or a choice made as completed steps. Account creation is step 1 of onboarding, not a separate gate.
2. Show progress two ways at once: a percentage (or "4 of 6 complete") and a labelled stepper or list, so the user sees both how far and what is left.
3. Pair progress with copy that shrinks the remaining work: "You're doing great! Just a few more details to complete your account setup" beats "We need a few details to create your profile". Keep it factual and short. No emoji in product copy (the video used a party popper and a flame; use an icon from the icon set or nothing).
4. Animate the counter when a step completes (0% to 10% to 20% in the video). Short, under 400 ms, and respect reduced motion.
5. Put progress where the user is working, not in a separate page.
6. For waits you cannot shorten (splash, loading card data), show progress so it feels faster: "loading bar UX tactics" (Tim Gabe, crypto card onboarding notes). A determinate bar when you know the length, an honest indeterminate state when you do not.

## 3. Stepper anatomy (uxpeak profile setup)

| State | Circle | Label |
|---|---|---|
| Done | Accent filled, white check | Regular, body colour |
| Current | Accent filled | Bold |
| Upcoming | Pale outline | Grey |

Steps shown: Sign up, Profile, Photo, Verify, Done. Above it a card: accent "Your Progress" title, "20%" on the right, an accent bar filled to 20%.

## 4. Checklists (Kole Jain, dashboard flaws)

The getting started checklist is the dashboard version of a stepper.

- A floating card in the lower right corner, collapsible with a chevron. Title "Getting started checklist", subtitle "Create your first database".
- Done items: filled accent check circle, text struck through in grey ("Start new data repository", "Define column structure", "Sync data", "Share database").
- Open items: empty dashed circle ("Create a tab", "Edit a filter").
- A quiet "Watch tutorial" button with a play icon.
- Footer "4 of 6 complete" in the accent colour with a progress bar.
- Each item, when clicked, takes the user to the exact control that completes it.
- Checks itself off when the user does the action anywhere, not only from the list.
- Dismissible, and once dismissed it stays dismissed (reachable again from Help).

## 5. Streaks (honest version)

The videos show a streak only in passing: "Streak started, Come back tomorrow, Day 1" listed as unsaved progress on a lesson complete screen (uxpeak). The rules below are general practice that keeps streaks motivating without becoming a guilt machine.

1. Count only real activity. A streak day is earned by doing the core action, not by opening the app.
2. Show the streak where the user finishes the action ("Day 1, come back tomorrow"), not as a red badge on the app icon.
3. Make it forgiving: allow a freeze or a grace day, and say so plainly. A broken streak shows the best run kept ("Best: 23 days") so the work is never erased.
4. Remind once per day at most, at a time the user chose, with an off switch in the reminder itself.
5. No shame copy: never "You let your streak die", never sad mascots guilting the user.
6. Never sell streak repair as the main revenue path.

## 6. Before and after

| Before | After |
|---|---|
| "Let's get started / We need a few details to create your profile", "Your Progress 0% Complete", empty bar, five empty dots, Full Name / Email / Phone, dark "Continue" | "You're doing great! / Just a few more details to complete your account setup", "20%", bar at 20%, stepper with Sign up done and Profile current |
| Six bullet welcome modal at first login, forgotten when dismissed | One tooltip on the most important action, then a corner checklist "4 of 6 complete" |
| Lesson ends, nothing kept | "That's a wrap / The anchor effect, done in 6 minutes", stats 8/10, Day 1, +40 XP, listed as progress |

## 7. Forbidden

- **Fake progress.** The uxpeak recap says "progress, even a fake one, creates real momentum". Do not do that. 20% must mean one of five real steps done. A bar that pre fills for work never done is a lie the user will notice when the remaining steps take longer than promised.
- Progress bars that slow down near the end to keep a user waiting on an upsell.
- Streak loss used as a threat in notifications.
- Counting steps that the product did by itself ("We analysed your profile, 40% done") as the user's progress, unless the label says it was automatic.

## 8. Checks

| Check | Pass when | Verify in code |
|---|---|---|
| Real start point | Initial progress equals completed real steps / total | Find the progress value; it is computed from step state, not a literal like `0.2` |
| Never a needless 0% | If any real step is done, the bar is above 0 | Trace the initial step state after sign up |
| Two forms | Percentage or "n of m" plus labelled steps | Both rendered from the same step array |
| Three step states | Done, current, upcoming differ in fill and label weight | Read the per step style branch |
| Checklist links | Every item routes to its control | Each item has an action/target |
| Streak forgiving | Freeze or grace rule exists and is shown | Read streak logic and its copy |
| Reduced motion | Counter animation off when reduced motion is set | `prefers-reduced-motion` or platform flag checked |
