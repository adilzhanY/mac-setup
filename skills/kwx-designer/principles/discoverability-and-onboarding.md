# Discoverability and onboarding

How users find out what a product can do, and how to teach the rest without tutorials nobody reads.

## Contents

1. Findability versus discoverability
2. The five learnability problems (and the fix for each)
3. The cost of hiding things (numbers)
4. Progressive and staged disclosure
5. Teaching in context: push and pull help
6. Onboarding: when it is warranted and how to do it
7. Coach marks and instructional overlays
8. Empty states
9. Gestures, shortcuts and other invisible input
10. Announcing new features
11. Checks

---

## 1. Findability versus discoverability

- **Findability:** users can locate content or functions they *already assume* exist.
- **Discoverability:** users come across content or functions they *did not know* existed.

Both fail for two different reasons: a UI reason (the link is too low, looks like an ad, is too faint) or an information-architecture reason (it sits under a label nobody would choose). Diagnose which before fixing: click tests and first-click tests reveal UI problems; tree tests and card sorts reveal IA problems.

## 2. The five learnability problems

Grossman, Fitzmaurice and Attar (CHI 2009) observed users of a complex application and classified every learnability problem into five kinds. Use them to diagnose:

| Problem | What the user experiences | Design fix |
|---|---|---|
| **Task flow** | Knows a series of steps is needed but not where to start | Name the high-level tasks in the UI ("New project from template"); offer starting points in empty states; organise help by goals, not by tools |
| **Awareness** | Does not know a function exists | Visual exposure: show the function on screen; timely, unobtrusive suggestions when the user does the slow version of a task |
| **Locating** | Knows it exists, cannot find where | Put it where users look (card sort); keep positions stable; help that points at the actual control on the user's current layout |
| **Understanding** | Found it, cannot work out how to use it | Clear signifiers and feedforward; demonstrate in place rather than describe; examples next to the control |
| **Transition** | Knows a faster way exists but keeps using the slow one | Show the shortcut next to the menu command; hint at the accelerator when the slow path is used (an audio or text hint for the hotkey raised hotkey adoption) |

Novices mostly fail on **awareness**; experienced users still fail on locating, understanding and transition. Think-aloud testing misses awareness and transition problems because users do not say "I don't know about X". Look for people doing things the slow way.

## 3. The cost of hiding things

NN/g measured hidden navigation (hamburger menus) against visible navigation:

- **Desktop:** navigation used in 27% of cases when hidden, 48% when visible, 50% when combined (some visible, rest in a menu).
- **Mobile:** 57% hidden versus 86% combined.
- Content discoverability dropped by more than 20% with hidden navigation.
- Tasks were at least 39% slower on desktop with hidden navigation and 15% slower on mobile.
- Perceived difficulty was 21% higher than with visible navigation.

Tognazzini's estimate for hidden scroll bars: one extra second per scroll, ten scrolls a day, tens of millions of users, about 21 person-years lost per day.

Rules that follow:

1. **Desktop: never hide primary navigation.** Show top-level options across the top or down the side.
2. **Mobile: show up to four or five top-level destinations** (a tab bar); put the rest in a labelled menu.
3. **If a menu icon is used, label it** ("Menu") and give it a clear tap target. The hamburger is not reliably recognised.
4. **Hidden is acceptable only for the showroom** (Tognazzini): if you hide complexity, reveal it progressively as users show skill, never hide essential controls.

## 4. Progressive and staged disclosure

**Progressive disclosure:** show the few most important options first; offer the specialised ones on request.

1. **Get the split right.** Everything frequently needed is on the first level. Decide with data: task analysis, frequency of use, analytics, instrumented feature counts. Confirm with observation, since page hits can come from accidental visits.
2. **Make the door obvious.** The control that reveals more is easy to find and looks like a control.
3. **Label the door so it predicts what is behind it.** "Advanced print options (scaling, page order)" beats "More".
4. **Stop at two levels.** Beyond two, users get lost. If you need three, simplify first; if impossible, split into several separate secondary panels opened from the first level.
5. **Do not offer several routes to the same secondary options** unless every route is clearly labelled.
6. Anything shown first signals importance. Reserve that space.

**Staged disclosure (wizards):** a linear sequence where each step shows only its own subset.

- Use it when the task splits into distinct steps with little interaction between them (account setup, a one-time import).
- Avoid it when users need to adjust and compare across steps (NN/g's hotel booking: room type, dates and price belong together on one screen for what-if comparison; payment details belong on a later step).
- Do not split into too many steps. Test one screen versus two versus five; the middle option often wins.
- Always show where the user is in the sequence, allow going back without losing data, and allow leaving with progress saved.

## 5. Teaching in context: push and pull help

Users do not read manuals and start using products at once (paradox of the active user). Help must come to the moment of need.

- **Push revelations** interrupt to show something (a tip that pops up, a tour). They block the core interface and are often dismissed unread. Use them only for information the user needs regardless of context, make them trivially dismissible, and show them one at a time.
- **Pull revelations** are available where the user is and are opened by the user (an info icon beside a field, a "What's this?" link, a hint in an empty state, a tooltip on a control). **Prefer pull.**
- **Krug's test for any guidance:** brief (the least information that helps), timely (exactly when needed), unavoidable (placed where the eye will be).
- **Contextual tips beat tutorials** (NN/g): tips tailored to the current page help users recognise what to do; tutorial content is rarely remembered.
- **Teach by doing.** Apple HIG: people retain more when they perform the task than when they watch. A safe practice round (MindNode's sample mind map, a game's first level) beats a slideshow.

## 6. Onboarding: when it is warranted and how to do it

NN/g's research on deck-of-cards tutorials (swipe-through intro slides) found **no improvement in task performance**. They also make simple apps look complicated. Default stance: **no onboarding; invest in usability instead.**

Onboarding is warranted only when:

1. **The product cannot work without information** (an account, identity verification, a device to pair).
2. **The experience depends on user details** (a language-learning app needs the language and level).
3. **A workflow is genuinely new or unusual** (the first mobile cheque deposit).

Test before adding it: test the product without onboarding; if users struggle, improve the design; only if that fails, prototype onboarding and keep it only if it measurably helps.

How to do it when needed:

- **Fast, optional, short.** A visible Skip, a progress indicator, the fewest possible screens, one concept per screen.
- **Ask only what is needed now.** Explain why each piece of data is needed. Anything you cannot justify at launch, ask later.
- **No visual customisation in onboarding** (themes, colours): users do not know their preference yet and keep defaults. Offer it later in settings.
- **Ask for permissions at the moment of need,** with the reason, not as a wall at launch. Exception: a permission the product cannot work without can be requested inside onboarding, where you can explain the benefit.
- **Do not teach the platform.** No slides explaining standard icons like Share or Settings.
- **Do not promote features at first launch.** The user already chose the product. Promote a feature when it becomes useful (show habit statistics after seven days of data).
- **If skipped, do not show it again,** but keep it findable in Help or Settings.
- **Let people use the product before asking for ratings, sign-up or payment** where the product allows it.
- **No alert at launch.** If there is a problem at start (no network), show cached content and a non-intrusive status label.

## 7. Coach marks and instructional overlays

If you use them:

1. **One hint, one interaction.** Cover a primary action or an unusual gesture, never every element.
2. **Show each hint when the user reaches the relevant part,** not all at once at launch. Never chain hints.
3. **Short text plus a visual.** A single visual intro can replace a series of text tips.
4. **Make hints look unlike the UI** (different style, handwritten feel, a pointer to the actual control), so nobody tries to tap the hint itself. NN/g saw users tap overlay icons thinking they were controls.
5. **Never explain standard elements.**
6. **They are a supplement, never a requirement.** If the hint is essential, the design is wrong.

Short-term memory fades in about 20 seconds: a user cannot read a five-step overlay, dismiss it, and then carry out the steps from memory.

## 8. Empty states

Four kinds: unpopulated personal lists (favourites, recents), unconfigured features (alerts, rules), unfilled workspaces (a new project), and no-result outputs (search, filter).

1. **Never show a totally blank area.** Blank reads as loading, broken, or empty, and the user cannot tell which.
2. **Report status accurately.** "No records for 1 to 7 March" once the query is done. Never show "No results" while still loading; show a progress indicator instead.
3. **Explain what will appear here and how to put it there.** "Star a file to pin it here." This is the best place to teach a feature, because it is pull help at the exact moment of relevance.
4. **Offer the action directly.** A "Create alert" button in the empty alerts panel, plus a "Learn more" link. Where useful, offer a second path (import, or load sample data).
5. **For no-results:** repeat the query, suggest a fix (spelling, fewer filters, a broader category), and offer a one-click way to clear filters.
6. **Make the link do the action.** "Send a request to view details" must link the words to the place where requests are sent.

## 9. Gestures, shortcuts and other invisible input

Norman ("Natural user interfaces are not natural", 2010): gestures are hard to learn and remember, and they are ephemeral, leaving no trace of what was done, so a failed gesture teaches nothing. Gestural systems still need feedback, explicit hints of possible actions, and guides.

Rules:

1. **Every gesture is an accelerator for a visible control,** never the only way (Apple HIG: a Back button stays even though edge-swipe also goes back).
2. **Use standard gestures with their standard meanings:** tap selects or activates, swipe scrolls or reveals row actions, pinch zooms, long press shows a context menu, pull down refreshes. Do not give a standard gesture an app-specific meaning, and do not invent a gesture for a standard action.
3. **Add a custom gesture only if it is** discoverable, easy to perform, distinct from other gestures, and not the only path to an important action. If it is hard to describe in simple words and a picture, it will be hard to learn.
4. **Show feedback during the gesture** so users can predict the result and see how far to go (the row slides, the action colour appears, a threshold snaps).
5. **Swipe on list rows:** keep the item visible while revealing the action; keep the direction's meaning consistent across the app; reserve it mostly for destructive or archive actions that users expect; give undo or confirmation because swipes trigger by accident; avoid conflict with system back and edge gestures (NN/g).
6. **Never conflict with system gestures** (screen edges, the home indicator, notification shade).
7. **Teach gestures visually at first relevant use** and keep the explanation reachable later (Tognazzini).
8. **Keyboard shortcuts:** follow platform conventions first; show every shortcut next to its menu command or in its tooltip; offer a searchable command palette for apps with many commands.
9. **Hover-only controls:** acceptable only as secondary accelerators on pointer devices, with the same action reachable from a visible control or menu, and never on touch.
10. **Give every gesture an accessible alternative** (a button, a menu item, a screen-reader action).

## 10. Announcing new features

Tognazzini's active discovery:

1. Mention the feature when the user first might need it (when they do the task it improves).
2. Repeat at intelligently spaced intervals (a few days, then months).
3. Stop as soon as the user has explored or adopted it.

His GroceryIQ case: sync was buried in a "More" submenu for five years; users left for a competitor that advertised sync. Spaced reminders would have kept them.

NN/g: promote only genuinely new features. Repeated promotion of familiar features trains users to ignore all onboarding. Keep "What's new" short and only after meaningful updates.

## 11. Checks

- For every function: is it visible, one labelled step away, or hidden? Hidden functions need a visible path.
- Is primary navigation visible on desktop? On mobile, are the top four or five destinations visible?
- Does every disclosure control predict what it reveals? Is anything more than two levels deep?
- Is there any onboarding? Can each screen of it be justified by one of the three warrants in section 6? Can it be skipped?
- Does every empty state say what goes there and offer the action that fills it? Is "no results" ever shown while loading?
- Is every gesture, hover action and shortcut duplicated by a visible control?
- Are shortcuts shown next to their commands?
- Is help pull, in context, and brief?
