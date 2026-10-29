# Heuristics as checks

Use this file to review a design. Every heuristic is written as pass/fail checks with typical violations. Run all of it on any screen before handing it over, and record failures with a severity.

## Contents

1. How to run a heuristic review
2. Nielsen's 10 usability heuristics
3. Tognazzini's first principles of interaction design
4. Raskin's humane interface rules
5. Krug's laws and rules
6. Norman's principles (short form)

---

## 1. How to run a heuristic review

1. Pick the user and the top three tasks.
2. Walk each task screen by screen. At each screen run every check below.
3. For each failure write: where, which check, what the user would experience, the fix.
4. Rate severity (Nielsen's scale):
   - 0: not a problem
   - 1: cosmetic, fix if time allows
   - 2: minor, low priority
   - 3: major, users will struggle; fix before shipping
   - 4: catastrophe, users will fail or lose data; must fix
5. Fix all 3s and 4s. A heuristic review finds problems; it does not prove there are none.

## 2. Nielsen's 10 usability heuristics

### H1. Visibility of system status
Keep users informed about what is going on, with feedback in reasonable time.
- [ ] Every input gets a visible response within 100 ms.
- [ ] Anything over 1 s shows a busy indicator; over 10 s shows progress and a Cancel.
- [ ] The current location, mode, selection, filter and account are visible.
- [ ] Consequential system actions (sync, deletion, sending, price changes) are announced, never silent.
- [ ] Backstage facts that change the user's decision are surfaced (low stock, sold out, free-shipping threshold).
- Violations: a button that does nothing visible until the next page loads; a silent background deletion; a "saving" state with no "saved".

### H2. Match between the system and the real world
Speak the user's language; follow real-world conventions; present things in a natural order; use natural mapping.
- [ ] No jargon, internal names or codes the user would not say.
- [ ] Order follows the user's task, not the database (name before ID, date in the user's format).
- [ ] Controls are laid out like the things they control (stove knobs).
- Violations: "Entity sync failed"; settings grouped by implementation module.

### H3. User control and freedom
Users make mistakes and need a clearly marked emergency exit.
- [ ] Undo and redo exist for content changes.
- [ ] Every dialog, flow and mode has a visible way out (Cancel, close, Escape, Back).
- [ ] Leaving a multistep flow keeps the progress, and says where to resume.
- Violations: a wizard with no Cancel; a full-screen modal with no close; an "are you sure" chain to leave.

### H4. Consistency and standards
Users should not wonder whether different words, situations or actions mean the same thing. Follow platform conventions.
- [ ] One word per concept across the product; one concept per word.
- [ ] Same component, same look, same behaviour everywhere.
- [ ] Platform conventions followed (button order, shortcuts, gestures, back behaviour).
- Violations: "Remove" and "Delete" used for the same thing; primary button on the left in one dialog and the right in another.

### H5. Error prevention
Better than good error messages is a design that prevents the problem. Slips come from inattention; mistakes come from a wrong mental model.
- [ ] High-cost errors are prevented first (data loss, money, sending to the wrong person).
- [ ] Constraints rule out invalid input; defaults are sensible.
- [ ] Destructive or wide actions show their scope before they run.
- See `errors-and-forgiveness.md`.

### H6. Recognition rather than recall
Make elements, actions and options visible. Users should not have to remember information from one part of the interface to another.
- [ ] Choices are shown (menus, suggestions, recent items) instead of typed from memory.
- [ ] Information needed at a step is on that step (no "remember the code from the previous screen").
- [ ] Icons have labels; commands are visible in menus with their shortcuts.
- [ ] Search offers suggestions and history.
- Violations: a command-only interface for occasional users; unlabelled icon toolbars; placeholder-only form labels.

### H7. Flexibility and efficiency of use
Accelerators, unseen by the novice, speed up the expert. Let people tailor frequent actions.
- [ ] Frequent actions have shortcuts, and the shortcuts are shown next to the visible command.
- [ ] Repeated work can be batched, templated or remembered.
- [ ] There is a visible path for novices *and* a fast path for experts; neither replaces the other.
- Violations: shortcuts with no visible command; a power feature with no shortcut.

### H8. Aesthetic and minimalist design
Every extra unit of information competes with the relevant units and lowers their visibility. Minimalist does not mean flat.
- [ ] Nothing on screen that does not support a user goal.
- [ ] Decoration never weakens a signifier.
- [ ] Rarely needed information is one step away, not in the way.
- Violation: NN/g's ornate teapot, whose decoration makes the handle awkward and the spout hard to clean.

### H9. Help users recognise, diagnose and recover from errors
Plain language, precise problem, constructive solution, and visually distinct.
- [ ] Error text says what happened and how to fix it, with no codes (codes only as optional diagnostics).
- [ ] Errors appear next to their source, with icon, colour and text.
- [ ] The fix is offered as an action where possible ("Use Berlin instead").
- [ ] User input is preserved.
- See `errors-and-forgiveness.md`.

### H10. Help and documentation
Best if none is needed. If needed: searchable, task-focused, concrete steps, in context.
- [ ] Help appears where and when it is needed (inline hints, "What's this?" links, tooltips), not only in a manual.
- [ ] Help is a list of concrete steps.
- [ ] Help is searchable and reachable from the place of need.

## 3. Tognazzini's first principles of interaction design

Condensed into checks. Source: asktog.com, "First Principles of Interaction Design (Revised and Expanded)".

- **Anticipation.** [ ] Each step brings the information and tools the user needs for it; they never have to leave to fetch something.
- **Autonomy.** [ ] Users feel in charge inside safe boundaries. [ ] Status is current, glanceable and accurate (no "five minutes left" that takes an hour). [ ] Timing thresholds (double-click, long press) are adjustable.
- **Colour.** [ ] Colour is never the only cue (about 10% of men and under 1% of women are colour blind). [ ] Checked with a colour-blindness simulator.
- **Consistency.** [ ] Platform first, then product family, then app, then visible structures, then invisible structures, then learned behaviour (strictest). [ ] Things that behave differently look different.
- **Defaults.** [ ] A default exists only where there is a predictable winner (a default right in 25% of cases costs more than it saves). [ ] Field contents are selected on entry so typing replaces them. [ ] "Reset" says exactly what it resets ("Restore initial settings for this tab").
- **Discoverability.** [ ] "If the user cannot find it, it does not exist." [ ] Necessary controls are visibly accessible. [ ] New features are mentioned when first needed, repeated at spaced intervals, and stopped once adopted (active discovery). [ ] Gestures are shown with diagrams at first use and stay reachable afterwards.
- **Efficiency of the user.** [ ] Measured in user time, not machine time or lines of code. [ ] Error messages say what went wrong, what to do, and allow for a deeper fault.
- **Explorable interfaces.** [ ] Clear main roads plus freedom to wander. [ ] A stable landmark for "home" on every screen. [ ] Actions are reversible ("Always allow Undo"). [ ] There is always a way out, and leaving a wizard says where to finish later. [ ] Going back in a flow never destroys entered data.
- **Fitts's Law.** [ ] Important targets big and near; edge and corner placement for pointer targets; no gap between an edge toolbar and the screen edge.
- **Human-interface objects.** [ ] Each object has a standard manipulation and standard result. [ ] A new behaviour gets a new object, not a familiar look.
- **Latency reduction.** [ ] Every click acknowledged within 50 ms. [ ] Repeated clicks trapped. [ ] Work happens in the background so the user can continue.
- **Learnability.** [ ] Decide between learnability and long-term efficiency by frequency of use: one-time tasks favour learnability, all-day tools favour efficiency (and still need to be learnable).
- **Metaphors.** [ ] The metaphor lets users grasp the model at once; it does not cap function; abandon it when it holds the design back.
- **Protect users' work.** [ ] Users never lose work through their own error, a network failure or a timeout. [ ] Forms keep their contents on error. [ ] Continuous save.
- **Readability.** [ ] High contrast text. [ ] Data larger than its label. [ ] Key word first in labels and menu items. [ ] Checked against older eyes (most people over 45 have presbyopia).
- **Simplicity.** [ ] Simplicity comes from simplifying, not from hiding (no "illusion of simplicity"). [ ] Progressive revelation for advanced features, never for essential controls. [ ] No necessary capability removed for the sake of simplicity.
- **State.** [ ] The product remembers where the user left off, what they were doing, and their preferences, across sessions and devices.
- **Visible navigation.** [ ] Navigation is visible, the current location is highlighted, breadcrumbs exist where depth exists. [ ] Subtasks appear as overlays over a dimmed main screen rather than as new screens.

## 4. Raskin's humane interface rules

Source: The Humane Interface (2000), via course notes and the Raskin Center summary.

- [ ] **Modelessness:** the same gesture in the same context always has the same result. Any mode that remains is a quasimode (held by the user) or has a strong indicator at the locus of attention.
- [ ] **Habituation:** nothing moves. Menu items, buttons and shortcuts keep their place, because practised users act before they look.
- [ ] **Monotony:** ideally one way to do each thing, so users habituate to one gesture. (Accelerators are the accepted exception; keep them consistent.)
- [ ] **Locus of attention:** interruptions (dialogs, warnings, progress popups) are proportional to importance; routine confirmations do not exist.
- [ ] **Undo over confirmation:** a habitual "Yes" defeats every confirmation dialog; provide undo instead.
- [ ] **Content persistence:** work is saved automatically and continuously; "Save" is not something the user must remember.
- [ ] **Do not hand design decisions to users as preferences.** Choose good behaviour; preferences are modes in disguise and users optimise for liking, not usability.
- [ ] **Measure:** task time, error rate, learning time, retention after a break. Some "improvements" measure worse.

## 5. Krug's laws and rules

Source: Don't Make Me Think, Revisited (2014), publisher sample and well-known principles.

- [ ] **First law: don't make me think.** Every screen is self-evident, or at least self-explanatory. Nothing makes the user stop and wonder "what is this?", "where do I click?" or "is that a link?".
- [ ] **Second law: clicks are fine if each one is mindless and unambiguous.** "Three mindless, unambiguous clicks equal one click that requires thought."
- [ ] **Users scan, satisfice and muddle through.** They pick the first reasonable option, not the best. Make the first reasonable option the right one.
- [ ] **Unavoidable guidance is brief, timely and unavoidable.** Krug's model: the London kerb marking "LOOK RIGHT" with an arrow, seen exactly when stepping off the kerb.
- [ ] **Omit needless words.** Cut happy talk and instructions; then cut half of what is left.
- [ ] **Clear visual hierarchy:** importance shown by prominence, logical grouping by nesting, clickable things obviously clickable, noise removed.
- [ ] **Trunk test:** on any page, the user can tell the site, the page name, the major sections, where they are, and how to search.
- [ ] **Reservoir of goodwill:** every annoyance (hidden information, forced formats, unnecessary questions, marketing fluff) drains it; every courtesy (obvious main tasks, telling the truth about costs, saving steps) refills it.

## 6. Norman's principles (short form)

From The Design of Everyday Things (2013 edition) and his essays.

- [ ] **Discoverability:** the user can work out which actions are possible and the current state.
- [ ] **Signifiers:** visible cues show where to act and how.
- [ ] **Affordances:** the actions the user needs are actually possible.
- [ ] **Mapping:** the relation between controls and effects is obvious from layout.
- [ ] **Constraints:** physical, logical, semantic and cultural constraints rule out wrong actions.
- [ ] **Feedback:** immediate, informative, not excessive.
- [ ] **Conceptual model:** the system image communicates one coherent model; once one part is learned, the same rules apply elsewhere.
- [ ] **Blame the design, not the user:** a repeated user error is a design defect; do not fix it with training or warnings.
