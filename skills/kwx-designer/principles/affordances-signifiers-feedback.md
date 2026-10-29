# Affordances, signifiers, mapping, constraints, feedforward and feedback

The mechanics of "I can see what to do, I can predict what it does, and I can see that it worked."

## Contents

1. Affordance versus signifier (get the words right)
2. Signifier rules for screens
3. Clickability: what the eye-tracking says
4. Mapping
5. Constraints
6. Feedforward
7. Feedback: rules and timing
8. States every control needs
9. Modes and visible state
10. Example images studied
11. Checks

---

## 1. Affordance versus signifier

- **Affordance** (J. J. Gibson): a relationship between an actor and an object, the actions that are possible. A chair affords sitting whether or not anyone notices. "To Gibson, affordances are a relationship."
- **Perceived affordance** (Norman, 1988): what the user *believes* is possible. On screens this is the only kind the designer controls: "All screens afford touching: only some detect the touch and are capable of responding."
- **Signifier** (Norman, 2008 and the 2013 edition): any perceivable cue that tells people what is possible, what is happening, and what the alternatives are. "Forget affordances: What people need, and what design must provide, are signifiers."
- **Social signifiers:** traces of other people's behaviour, like a crowded train platform (the train has not left) or a worn path across grass (a desire line). On screens: "most popular", view counts, "12 people are editing", recently used items, worn-in defaults.
- **The cursor is not an affordance, it is feedback** (Norman).

Use "signifier" when you mean "the thing that shows the user they can act". A designer's job on a screen is almost entirely about signifiers.

## 2. Signifier rules for screens

1. **Every interactive element has at least one strong signifier.** Strong means: a bounded shape (button), a distinct colour plus underline (link), an input border or inset (field), a handle (draggable), a chevron (expands or navigates), a visible label.
2. **No static element carries an interactive signifier.** No button-shaped headings, no blue or underlined non-links, no chevrons on rows that do nothing.
3. **Buttons look like buttons.** A rectangle, usually with rounded corners, with a clear text label. Flat is fine if the shape and contrast are still there. Ghost buttons (outline only, low contrast) are weak: avoid them for anything important.
4. **Inputs look like inputs.** A visible boundary and a label outside the field. Placeholder text is not a label.
5. **Icons get text labels** unless they are universal (search, home, close, back, play, print). Labels are always visible, not shown on hover (hover does not exist on touch and costs a move on desktop).
6. **Draggable things show a grip** (six dots, a handle bar) and change the cursor on hover. A sheet that can be dragged down shows a grabber.
7. **Scrollable areas show that more exists:** cut the last item off at the edge, fade it, or show a scrollbar. A perfectly aligned last row says "there is no more" (Zeigarnik: signal additional content).
8. **Hidden controls need a signifier for their hiding place.** If controls appear on hover, something visible must say "there is something here" (a faint handle, a "more" icon). Tognazzini's Safari case: the PDF save control appeared only when the mouse reached the bottom of the window, and it took about 20 minutes to find.
9. **Words are signifiers too.** "Use words" is one of Norman's four principles for screens, with "follow conventions", "use metaphor" and "use a coherent conceptual model".
10. **Unavailable must look unavailable, and say why.** Apple HIG: indicate when a gesture or control is not available, or people think the app has frozen. A locked object that can be dragged a few pixels and snaps back tells the user why far better than nothing.

## 3. Clickability: what the eye-tracking says

NN/g tested nine page pairs (71 people): the same page with weak signifiers (links styled like body text, ghost buttons) versus strong ones.

- Weak versions took about **22% longer** and drew about **25% more fixations**. Gaze spread over more elements, a sign of uncertainty, never the reverse.
- On one page, 86% of people on the strong version looked at the heading and then the target link. Only 50% did on the weak version; many stopped at the subheading.
- Flat designs held up only when the page had low density, a traditional layout, and salient high-contrast targets with space around them.
- **Rule:** give inline links a colour that contrasts with body text even if you drop the underline. Use ultra-flat styling only on sparse, conventional layouts.

## 4. Mapping

Mapping is the relationship between a control and its effect.

1. **Natural mapping by layout.** Arrange controls in the same spatial pattern as what they control. The stove is the classic example: four burners in a square need four knobs in the same square, not in a row.
2. **Proximity.** Put the control on or beside its target. A delete button on each row beats one delete button at the top that acts on "the selected row".
3. **Direction.** Up, right and clockwise mean more. A volume slider fills from left to right. A scroll wheel moves content the way the platform does.
4. **Scope by placement.** A reset button inside a tab card resets that tab; one in the window chrome resets all tabs (Tognazzini). Placement must tell the user how wide an action reaches.
5. **One control, one effect.** A control that changes something far away needs a visible link (highlight the affected thing, animate the change toward it).
6. **Movement mirrors the content.** Drag follows the finger exactly; a dismissed card leaves the way it was flicked.

## 5. Constraints

Constraints limit what can be done, so the wrong action is impossible or obviously wrong.

- **Physical:** the cursor cannot leave the screen; a vertical scrollbar only moves vertically; a slider has ends.
- **Logical:** reasoning reveals the rest. If a task needs five steps and four are shown, users infer a fifth.
- **Cultural:** learned conventions (red means stop or error; a scrollbar's direction).
- **Semantic** (from the book): the meaning of the situation rules out options.

Screen rules:

1. Use a control that can only hold valid values: a date picker rather than a free date field, a stepper with min and max, a dropdown or segmented control for a short closed list.
2. Disable invalid combinations rather than rejecting them later (a return date before departure cannot be chosen).
3. Enforce a logical order only when the task has one (departure before return).
4. Prefer forgiving input to strict input: accept "+49 30 1234", "030/1234" and "0301234" alike and normalise them.
5. A constraint must be visible. A field that silently refuses a character looks broken; show the rule next to it.

## 6. Feedforward

Feedforward tells the user *what will happen* before they act, closing the gulf of execution. Feedback tells them what *did* happen. Research (Djajadiningrat et al.; Vermeulen et al., CHI 2013) separates:

- **Inherent feedforward:** the form itself shows what action is possible (a slider's track and thumb say "drag me sideways").
- **Augmented feedforward:** added information such as a label, an arrow, an on-screen hint.
- **Functional feedforward:** shows the purpose and result of the action, not only that it is possible.

Rules:

1. Label buttons with the outcome: verb plus object, plus count when it matters ("Archive 12 messages").
2. Show the destination: a link says where it goes; a "Move to..." menu shows folder names.
3. Preview the result for costly, wide or slow actions (a filter preview, a print preview, the display-zoom preview before a restart).
4. Show the effect while the gesture is in progress: a swipe reveals the action's colour and icon, and passes a visible threshold before it commits.
5. Hover and focus states are feedforward: they say "this will respond". Every pointer target gets one.

## 7. Feedback: rules and timing

Norman: feedback must be immediate, informative, and not excessive. Too much feedback is as bad as too little (a constantly beeping appliance gets ignored).

**Timing (Nielsen, Doherty, Tognazzini):**

| Delay | What the user feels | What to show |
|---|---|---|
| under 50 to 100 ms | Instant, "I did that" | The pressed or selected state, the typed character, the drag following the finger |
| 100 ms to 1 s | A noticeable but uninterrupted flow | Nothing extra beyond the pressed state; keep the old content visible |
| about 400 ms | Doherty threshold: above it, people start waiting and productivity drops | Aim to complete common actions under this |
| 1 to 10 s | Attention starts to drift | An in-place busy indicator (spinner on the button, skeleton in the area) |
| over 10 s | Users switch tasks | Percent done or named steps, a time estimate, a labelled Cancel, and let them do other work |

**Rules:**

1. **Acknowledge every press within 50 ms** (Tognazzini), even if the work takes longer.
2. **Trap repeated presses.** Slow systems get pressed again; disable or debounce the control after the first press and show it is working.
3. **Show results where the eye is.** Mail shows "Updated just now" and the unread count in its own toolbar (Apple). Feedback far from the action is missed.
4. **Match the strength of feedback to its importance.** Passive status for routine things; an interrupting alert only for possible data loss or a blocked task (Apple HIG).
5. **Do not confirm the expected.** People expect actions to succeed; tell them when one fails. Confirm success only when it is significant (a payment) or invisible otherwise (a message sent in the background).
6. **Say when a command cannot be carried out, and why.** Maps tells you it cannot route from a place to itself.
7. **Never move a done item silently.** Do not remove items from a list without showing that it happened; show status and let the user choose (NN/g on silent removals).
8. **Use more than one channel for important feedback.** Colour plus text plus icon (plus haptics or sound where the platform supports them), so muted, colour-blind and screen-reader users all receive it.
9. **Progress bars make waits tolerable even when imprecise.** But keep estimates honest: Tognazzini's iPad update said five minutes and took an hour, which left users unable to plan.
10. **Show something immediately when loading.** Placeholders or skeletons, then fill in. An empty screen reads as broken (Apple: "Show something as soon as possible").

## 8. States every control needs

Define each one in code and make each visibly different:

- **default**
- **hover** (pointer platforms): feedforward that it responds
- **focus** (keyboard): a clear ring or outline, never removed
- **pressed / active**: immediate response
- **selected / checked / on**: persistent, distinct from focus and hover
- **disabled**: lower contrast *and* an explanation available
- **loading / busy**: for actions that take over 1 s
- **error**: border, icon and text, not colour alone
- **success**: only when the success is not otherwise visible

Material 3 renders hover, focus, pressed and dragged as a translucent "state layer" over the control (hover about 8%, dragged about 16%; focus and pressed around 10 to 12% depending on version), and disabled content at about 38% opacity. Check the current Material documentation for exact token values.

## 9. Modes and visible state

- **A mode** exists when the same input gives different results depending on a state the user is not attending to (Raskin). Caps Lock is the archetype. Modes cause errors because habituated users act without checking the state.
- **Eliminate modes where possible.** Convert the rest to **quasimodes**: states held only while the user physically holds them (Shift, holding a key for a temporary tool, a press-and-hold menu). The user cannot forget a mode they are holding.
- **If a persistent mode must exist** (edit mode, selection mode, recording), show it strongly where the user is looking: a coloured frame around the work area, a changed toolbar, a visible "Done" button. A small badge in a corner is not enough.
- **Transient modes cause fewer errors than persistent ones** (Raskin). Prefer a mode that ends itself after the action.
- **Eliminate hidden state** (Bret Victor). If a setting, filter or account changes what the user sees, show which one is active ("Showing: unread only. Clear filter").

## 10. Example images studied

These were downloaded to the research scratchpad and examined; they are described here, not copied.

- **A "PUSH" door with a pull bar** (Wikimedia Commons, "Push Plate at 570 Lex"). A horizontal metal bar, which the hand reads as "grab and pull", carries an engraved PUSH sign. The bar's form signifies the opposite of what the label says. This is the archetypal "Norman door": when a design needs a text label to correct what its shape says, the shape is wrong. On screens, the equivalent is a button-shaped element that is not clickable, or a link styled like plain text with "click here" next to it.
- **NN/g's stove illustration** for heuristic 2. Four burners are arranged as two large at the back and two small at the front, with four knobs grouped in the centre in a matching pattern, so each knob's position predicts its burner. Natural mapping: no labels needed.
- **NN/g eye-tracking of a flat versus a strong link** (Brilliant Earth "3 YEAR: PEARL"). The strong version shows "SHOP PEARL" in teal, uppercase and underlined; the weak version shows "Shop Pearl" in small dark grey text that looks like a caption. The heatmaps show the strong version's attention concentrated on headings and the link, and the weak version's attention spread across navigation and body text: uncertainty made visible.
- **Fitts's task diagram** (Wikimedia Commons). Two bars of width W separated by distance D with the path of motion between them: the time to hit a target grows with D and shrinks with W.

## 11. Checks

- Can you point to the signifier for every interactive element? Is there any static element with an interactive signifier?
- For every icon: label visible, or universal?
- For each control, which thing does it affect, and is it next to that thing?
- Is every invalid input made impossible or forgiven, rather than rejected after submit?
- Does every button say what it will do, with the object?
- For every action, what appears within 100 ms, and where? What appears after 1 s and after 10 s?
- Are all nine states in section 8 defined where they apply?
- List the modes. Does each have a strong indicator where the user is looking?
