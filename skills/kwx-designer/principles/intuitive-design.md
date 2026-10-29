# Intuitive design: the master file

Intuitiveness is the single most important quality for this user. Read this file first for any interface work. The other files in `principles/` go deeper on each part:

- `mental-models-and-conventions.md`: what users already know, and how to reuse it.
- `affordances-signifiers-feedback.md`: making actions visible, predictable and confirmed.
- `laws-of-ux.md`: every Law of UX with a rule and a concrete example.
- `heuristics.md`: Nielsen, Tognazzini, Raskin and Krug as pass/fail checks.
- `discoverability-and-onboarding.md`: finding features, progressive disclosure, empty states, onboarding, gestures.
- `errors-and-forgiveness.md`: prevention, constraints, undo, confirmation, error messages.
- `scanning-and-information-scent.md`: how people read screens and choose where to click.

## Contents

1. What "intuitive" means, as something you can test
2. The seven questions every screen must answer
3. The method: make any screen intuitive in 15 steps
4. Fast checks you can run by reading the code or the mockup
5. The intuitiveness rubric (score before you hand anything over)
6. Tie-breakers when principles conflict
7. Red flags that always mean "not intuitive yet"

---

## 1. What "intuitive" means, as something you can test

"Intuitive" is not a mystical property. The sources agree on what it really is:

- **Jef Raskin (1994, "Intuitive equals familiar"):** a feature is intuitive to the degree it resembles something the user has already learned. His precise definition: intuitive means *using readily transferred, existing skills*. A teacher who had never seen a mouse lifted it in the air and spun its ball upside down. It became "intuitive" only after one sentence of explanation, because the motion then mapped onto joysticks and pencils she already knew.
- **Don Norman (The Design of Everyday Things):** good design has two properties, *discoverability* (can I work out what actions are possible and what state the thing is in?) and *understanding* (what does it all mean, how is it meant to be used?).
- **Nielsen Norman Group:** learnability is "how easy it is for users to accomplish a task the first time they encounter the interface", plus how many repetitions they need to get efficient.

**Working definition for this skill.** An interface is intuitive for a named user when, on first contact and with no instruction, that user can:

1. tell what the screen is for,
2. see what they can do,
3. predict what an action will do *before* doing it,
4. tell what happened *after* doing it,
5. get back out of a wrong step,

using only skills they already have from other products, the platform and the physical world.

Consequences you must act on:

- **Intuitive is relative to a person.** Always name who the user is and what they already use. "Intuitive" for a Hyprland power user and for a first-time phone owner are different targets.
- **Every novel element costs intuitiveness.** Novelty must buy something real (speed, power, beauty that does not hide function), and it must be taught at the moment of use. A different layout for the sake of looking different is a pure loss.
- **It is measurable.** First-use success without help, time to the first correct action, number of wrong first clicks, and visible hesitation are the numbers. Raskin adds error rate and retention after a break.

## 2. The seven questions every screen must answer

Norman's seven stages of action (goal, plan, specify, perform, perceive, interpret, compare) turn into seven questions a user silently asks. The screen must answer each one without the user having to ask anyone.

| # | User's question | Gulf | What answers it |
|---|---|---|---|
| 1 | What is this, and is it for me? | evaluation | Title in the user's words, one clear purpose, recognisable layout |
| 2 | What can I do here? | execution | Visible controls, strong signifiers, labels on icons, no hidden-only actions |
| 3 | How do I do it? | execution | Conventions, natural mapping, constraints that rule out wrong moves |
| 4 | What will happen if I do it? | execution | Feedforward: specific verb labels, previews, counts ("Delete 3 photos") |
| 5 | What happened? | evaluation | Immediate feedback in under 100 ms, result shown where the eye already is |
| 6 | Is this what I wanted? | evaluation | Visible current state, comparison with before, success or error in plain words |
| 7 | Where am I, and how do I get out? | both | Location indicator, back and cancel always present, undo |

Diagnose a failure by naming the question that failed. "The user did not notice the button" is question 2. "The user pressed it twice" is question 5. Fix the question that failed, not a neighbouring one.

## 3. The method: make any screen intuitive in 15 steps

Do these in order. Each step has an output you can write down. Do not skip to visuals before steps 1 to 4 are written.

**Step 1. Name the user, their goal, and what they already know.**
Write one line: "A [who], who already uses [apps, platform], wants to [goal] in [context]." The prior apps define the conventions you must honour (Jakob's Law). Example: "A desktop Linux user who lives in a file manager, a browser and a terminal, wants to find yesterday's screenshot in under five seconds."

**Step 2. Write the conceptual model in two sentences, as nouns and verbs.**
List the objects the user thinks about (nouns) and what they do to them (verbs), in the user's own words. Example: "A *note* belongs to one *notebook*. You *write*, *pin*, *move* and *delete* notes." If you cannot write this in two sentences the design will not be learnable either. Every screen must show these nouns and verbs and no others (no internal names like "entity", "sync job", "payload").

**Step 3. Choose conventions first, invent last.**
For every element, find the platform or category convention (where search lives, what a back arrow does, where the primary button sits in a dialog, what swipe-left means in a list). Use it. If you deviate, write a one-line reason that names what the user gains. No reason, no deviation. See `mental-models-and-conventions.md`.

**Step 4. Give the screen one primary action.**
Name the single most common thing the user comes here to do. Make it the most prominent element: largest target, strongest colour, nearest to where the eye and hand already are. Everything else is visibly secondary. Two equally loud buttons mean the design has not decided, so the user has to (Hick's Law, Von Restorff).

**Step 5. Make every action visible, or one obvious step away.**
List every action the screen supports. Each one must be either on screen, or behind a single clearly labelled control ("More", a labelled menu, an "Advanced" disclosure). Gestures, hover-only controls, long press, right click and keyboard shortcuts are *accelerators*: they may never be the only path. Tognazzini: "If the user cannot find it, it does not exist."

**Step 6. Signify: interactive things look interactive, static things do not.**
Buttons look like buttons (a bounded shape with a clear label). Links differ from body text in colour and ideally underline. Inputs look like places to type. Nothing static looks clickable (no button-shaped headings, no blue non-links). Every icon either has a visible text label or is one of the few universal icons (search, home, print, close, back, play). See `affordances-signifiers-feedback.md`.

**Step 7. Map controls to what they affect.**
Put each control next to, or in the same spatial arrangement as, the thing it changes. A per-item action lives on the item. A setting for the whole window lives in the window chrome, not inside one card. Direction matches effect: up or right means more, a slider moves the way the value grows.

**Step 8. Constrain away the wrong moves.**
Make invalid input impossible rather than reporting it later: pickers for dates, disabled return dates before the departure date, formats accepted however the user types them. A disabled control must say why it is disabled (tooltip or helper text), or it looks broken.

**Step 9. Feedforward: say what will happen before it happens.**
Buttons are labelled with the specific outcome ("Save draft", "Delete 3 photos", "Send to Anna"), never "OK", "Yes" or "Submit". For costly, wide or slow actions, show a preview first (Norman: previews prevent mistakes).

**Step 10. Feedback: answer every input, at the right speed.**
- under 0.1 s: show the visual response to every press, tap and keystroke (Tognazzini asks for acknowledgement within 50 ms).
- 0.1 to 1 s: no special indicator needed, but the pressed state must already be showing.
- 1 to 10 s: show a busy indicator in place.
- over 10 s: show percent done or step names, and a clearly labelled Cancel.
Show results where the user is already looking. If the result is off screen, bring it into view (Apple: after an undo, scroll to the restored paragraph).

**Step 11. Forgive.**
Every action that can be undone gets Undo. Confirmation dialogs are only for actions that are both irreversible and uncommon, and they name the object and the consequence. Never lose user input: keep form contents after an error, autosave drafts. See `errors-and-forgiveness.md`.

**Step 12. Disclose progressively, at most two levels.**
Frequent and important controls on the first level, rare and advanced ones behind one clearly labelled door. The label on that door must predict what is behind it ("Advanced print options", not "More"). More than two levels means the design needs simplifying, not another level.

**Step 13. Design every state, not just the happy one.**
For each view, design: first run (empty), loading, partial, full, error, offline, no results, and success. An empty area must say what will appear there and offer the action that fills it ("No favourites yet. Star a file to pin it here."). A loading area must never say "No results".

**Step 14. Write the words last, and carefully.**
Use the user's vocabulary, front-load the key word in every label ("Delete account", not "Account deletion options"), make labels mutually distinct so no two can be confused, and keep them short. Error messages say what happened, why, and how to fix it, in plain words.

**Step 15. Walk through it as the user, step by step.**
For every step of the primary task, answer the four cognitive walkthrough questions. Any "no" is a failure to fix before handing over:
1. Will the user try to achieve the right result?
2. Will the user notice that the correct action is available?
3. Will the user associate the correct action with the result they want?
4. After the action, will the user see that progress was made?

## 4. Fast checks you can run by reading the code or the mockup

These checks do not need a browser or a screenshot. Work them out from the layout code, the sizes and the colours.

- **Five-second test.** Pretend you see the screen for five seconds. Can you state (a) what it is for and (b) what the main action is? If (b) is ambiguous, step 4 failed.
- **Squint test.** Imagine the screen blurred. The primary action and the current state must still be the strongest shapes. If three things are equally loud, nothing is.
- **Label-only test.** Hide all icons. Does the screen still make sense from words alone? Then hide all words. Is every remaining icon a universal one? If any icon is neither labelled nor universal, add a label. NN/g's 5-second rule for icons: if you need more than five seconds to think of an icon for a concept, the icon will not communicate it.
- **Hidden-path audit.** List every action and how to reach it. Mark any action reachable *only* by gesture, hover, long press, right click, double click or shortcut. Each mark needs a visible alternative.
- **State matrix.** For every interactive component, list default, hover, focus, pressed, selected, disabled, loading and error. Each one must be defined in code and visibly distinct from its neighbours. Selected and focused must not look the same.
- **Mode audit.** List every situation where the same input does different things (an edit mode, a selection mode, a tool palette, caps lock). Each mode needs a strong persistent indicator where the user is looking, or should be removed (Raskin).
- **Undo audit.** List every action that changes or destroys data. For each: is there undo? If not, is there a specific confirmation? If neither, it is a defect.
- **Trunk test (Krug).** Dropped on any screen with no history, can the user answer: what product is this, what page is this, what are the main sections, where am I in them, how do I search or go home?
- **Vocabulary audit.** List every word on screen that the named user would not use themselves. Replace each.
- **Target audit.** Every touch target at least 44 by 44 points (Apple) or 48 by 48 dp (Material), with space between neighbours; frequent pointer targets large or on a screen edge or corner (Fitts).

## 5. The intuitiveness rubric

Score every screen before handing it over. Each criterion scores 0, 1 or 2. The criteria marked **critical** may never score 0.

| # | Criterion | 0 | 1 | 2 |
|---|---|---|---|---|
| C1 **critical** | Purpose is obvious | Unclear what the screen is for | Clear after reading body text | Clear from title and layout in five seconds |
| C2 | Conventions followed | Invents its own patterns for standard tasks | Mostly standard, one unexplained deviation | Standard everywhere, every deviation justified and taught |
| C3 **critical** | One primary action | No clear primary, or several competing | Primary exists but is not the most prominent | Primary is unmistakable; secondary actions visibly quieter |
| C4 | Everything findable | Some actions only via gesture, hover or shortcut | All visible but some buried two or more levels deep | All visible or one labelled step away |
| C5 | Signifiers | Clickable and static look alike | Mostly clear, a few ambiguous elements | Every control looks operable, nothing static does, icons labelled |
| C6 | Mapping and grouping | Controls far from what they affect | Mostly near, some global controls mixed with local | Every control sits with what it changes; groups match the mental model |
| C7 **critical** | Feedback and state | Some actions give no response, or state is hidden | Response exists but is slow, distant or vague | Every input answered within 100 ms where the eye is; state always visible |
| C8 | Feedforward | Generic labels (OK, Submit, Yes) | Specific verbs but no scope or preview | Specific verbs with object and count; previews for costly actions |
| C9 **critical** | Recovery | Destructive actions with no undo and no confirmation | Confirmation only, or undo that is hard to find | Undo everywhere practical; specific confirmation for the irreversible; input never lost |
| C10 | Memory load | User must remember values or codes across screens | Some carry-over missing | All needed context visible; recognition everywhere |
| C11 | Language | Jargon, internal names, error codes | Mostly plain, a few unclear terms | User's own words, front-loaded, distinct labels |
| C12 | All states designed | Empty, loading or error states missing | Present but unhelpful ("No data") | Every state explains itself and offers the next action |

**Pass:** 20 or more out of 24, and no critical criterion at 0. **Report the score** with one line per criterion below 2 saying what keeps it from 2.

## 6. Tie-breakers when principles conflict

- **Familiar versus better.** Default to familiar (Raskin's catch 22: a much better interface must differ, and difference reads as "not intuitive"). Break a convention only when the gain is large *and* you teach the new behaviour at the moment it is first needed. Buxton, quoted by Tognazzini: "The most important consistency is consistency with user expectations."
- **Learnable versus efficient.** Serve both with layers: a visible, labelled path for everyone, plus accelerators (shortcuts, gestures, command palette) for the frequent user. Show the accelerator next to the visible command (shortcut text in menus) so people graduate to it. Most users are perpetual intermediates (Cooper): design the main path for them, not for the first minute or for the expert.
- **Minimal versus discoverable.** Tognazzini: "Hiding complexity increases it." Remove what is unnecessary, but never hide what is necessary. Clean that comes from hiding the steering wheel is not simplicity.
- **Consistent versus correct.** Things that behave differently must look different. Reusing a familiar look for different behaviour is worse than inconsistency (a trash can that deletes instantly breaks every trash can).
- **Fewer clicks versus clearer clicks.** Krug's second law: the number of clicks matters less than how much thought each one takes. Three mindless, unambiguous clicks beat one click that needs thought.
- **Aesthetics versus clarity.** Beauty raises perceived usability and tolerance for small flaws (aesthetic-usability effect), but it also hides problems in testing. Never let a visual style weaken a signifier (ghost buttons, grey links, unlabelled icons) on a dense or novel screen.

## 7. Red flags that always mean "not intuitive yet"

- A tooltip, coach mark or tutorial is needed to explain a standard task.
- An icon without a label that is not search, home, close, back, play or print.
- A button labelled OK, Yes, Submit, Confirm or Continue where a specific verb fits.
- Two buttons of equal weight side by side, with no primary.
- Placeholder text used instead of a field label.
- A control that changes something elsewhere on screen, far from itself, with no visible link.
- A mode the user can be in without a persistent indicator.
- A destructive action with neither undo nor a specific confirmation.
- An empty panel with no words, or "No results" shown while still loading.
- An action available only by swipe, hover, long press or shortcut.
- A disabled button with no explanation of what would enable it.
- A confirmation dialog for something routine or undoable.
- A settings screen that asks the user to decide something the designer could have decided with a good default.
- Internal or technical words on screen: IDs, error codes, "null", "sync failed (409)".
