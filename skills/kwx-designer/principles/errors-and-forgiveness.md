# Errors and forgiveness

Preventing errors, absorbing the ones that happen, and helping people recover. An interface that forgives invites exploration, and exploration is how people learn it.

## Contents

1. Slips and mistakes need different fixes
2. Preventing slips
3. Preventing mistakes
4. The forgiveness ladder: undo, then confirmation, then friction
5. Undo and redo
6. Confirmation dialogs
7. Error messages
8. Protecting the user's work
9. Checks

---

## 1. Slips and mistakes need different fixes

- **A slip:** the user has the right goal and the right plan but carries it out wrongly from inattention (taps Delete instead of Archive next to it, types into the wrong field, hits a key while in the wrong mode). Experts make slips more than novices, because they act on habit.
- **A mistake:** the user's mental model is wrong, so they form the wrong goal or plan (thinks "Remove from playlist" deletes the song from the library, or expects an inactive-looking control to be off when it is on).

Treat both as design failures, never user failures. Do not respond with warnings, training or "be careful" copy. Change the design.

Tognazzini on why forgiveness matters: in a study of hazardous versus supportive environments, people made no more mistakes in the hazardous one, but they worked far more slowly. NN/g: making cart items easy to remove did not raise removals, but shoppers added more items, because they knew they could take them out.

## 2. Preventing slips

1. **Constrain.** Use controls that cannot hold invalid values (pickers, steppers with bounds, closed lists). Block invalid combinations (no return date before departure).
2. **Suggest.** Autocomplete and suggestions turn typing (recall) into picking (recognition) and absorb misspellings.
3. **Default well.** A sensible preset matched to the likely goal; common presets such as "In 1 hour", "Tomorrow morning" instead of typed times.
4. **Forgive formats.** Accept the way people naturally type and clean it up: strip spaces and dashes from card numbers, accept any date format, ignore stray characters. Format as they type (group card numbers in fours) so errors are easier to spot.
5. **Separate the dangerous from the frequent.** Different position, size and colour for destructive actions; never place Delete next to Save at the same weight (Fitts in reverse).
6. **Show where input is going.** Highlight the field being edited, the item being acted on, and the mode in force, so attention does not have to hold it.
7. **Remove modes,** or make them quasimodes (Raskin). Mode errors are the classic slip.
8. **Warn while the error forms, not after.** A live character count that turns negative and highlights the overflow, with the Send button disabled (NN/g's Twitter example), beats a rejection after submit.
9. **Catch the likely slip.** Warn when a message mentions "attached" but nothing is attached; when a recipient is outside the organisation; when a meeting is set at 3 am.

## 3. Preventing mistakes

1. **Find the model gaps early** with field studies and think-aloud tests.
2. **Follow conventions** so users' existing models are correct for your product.
3. **Use clear signifiers** so controls are understood (NN/g's Polarr example: tap-then-swipe value controls with no signifier made novices set wrong values several times).
4. **Show previews before committing** costly, wide or slow changes.
5. **Remove memory burdens.** Show the context needed at every step of a multistep task, as if the user had just been interrupted (dates, places and choices already made).
6. **Make state visible.** Many mistakes come from a wrong belief about the current state: "is this the live document or a copy?", "which account am I in?".

## 4. The forgiveness ladder

Choose the lightest tool that protects the user:

1. **Make the error impossible** (constraint, good default, forgiving format).
2. **Make the action reversible** (undo, trash, archive, version history). This is the default answer for anything destructive.
3. **Ask for confirmation** only when the action is irreversible *and* uncommon or high-cost.
4. **Add deliberate friction** (type the name, a second person approves) only for rare, catastrophic actions.

Apple HIG: do not alert for common, undoable actions even when they are destructive (deleting an email or a file). Do alert for uncommon destructive actions that cannot be undone. Finder does not warn when a file goes to the trash because deletion is the expected result.

## 5. Undo and redo

Users expect undo to reverse their recent actions and will press it several times until something changes.

1. **Offer undo for every content change,** not only text.
2. **Multiple levels.** Let users undo everything since a logical point (opening the document, the last save). Do not cap it arbitrarily.
3. **Say what will be undone.** Label the command with the action: "Undo Typing", "Redo Bold", "Undo Delete 3 files".
4. **Show the result of undo.** If the undone change is off screen, scroll to it and highlight it; otherwise users think nothing happened and undo again.
5. **Batch related micro-steps.** Twenty slider nudges are one undo step; offer "Revert all changes" for a session.
6. **Immediate-action pattern:** perform the action at once and show a toast with "Undo" for several seconds (Gmail deleting 92 emails; "Undo Send" for up to 30 seconds). This beats a confirmation dialog for everyday destructive actions.
7. **Soft delete:** move to a trash or archive that keeps items for a stated period; delete permanently only from there.
8. **Use system undo paths** (Edit menu, Ctrl/Cmd Z, shake on iPhone). Add on-screen undo buttons only where the platform path is not obvious, with standard icons, in the toolbar.
9. **Raskin:** universal undo plus continuous save removes the need for most confirmations and for "Save" itself.

## 6. Confirmation dialogs

Use them sparingly. Raskin: users habituate to confirmations; after a few repetitions "Yes" is pressed by reflex and the dialog protects nothing. NN/g: overused warnings train users to click through all warnings, including the important ones.

When you do use one:

1. **Only for serious, irreversible consequences** (permanent deletion, large payments, sending to many people, overwriting).
2. **Be specific.** Restate exactly what will happen, with names and counts: "Permanently delete 'Q3 report.pdf' and 14 other files? This cannot be undone." Never "Are you sure?".
3. **Buttons describe outcomes.** "Delete 15 files" and "Keep files", or "Delete" and "Cancel". Never Yes/No; never "OK" for anything but a purely informational alert. Cancel is always labelled "Cancel".
4. **No default on the destructive button.** Make the safe choice the default, or have none. Style the destructive button as destructive (red text or fill).
5. **Put the most likely button where people expect it** (trailing side in a row on Apple; follow the platform).
6. **Scale friction to rarity and severity.** For rare catastrophic actions, require a non-standard act: typing the resource name or "DELETE" (Mailchimp, GitHub repository deletion). Use this rarely or it loses its effect.
7. **Use context to decide** whether to confirm at all: a banking app might confirm only payments unusually large for that user.
8. **Confirm before closing something that would lose user content,** whether closed by button or gesture, and offer "Save draft" as a choice.
9. **Never show two alerts at once.** One modal at a time.

## 7. Error messages

**Visibility**

1. **Next to the cause.** Put the message by the field or item that needs attention, not in a banner at the top only.
2. **Redundant indicators.** Red text plus a border plus an icon. Never colour alone.
3. **Severity-matched.** Inline text or a toast for minor issues; a modal only when progress is blocked.
4. **Not premature.** Do not flag a field as wrong while the user is still typing or merely because it lost focus while empty. Validate on submit or after the user finishes the field; for tricky formats (passwords) show the requirements live beside the input as a checklist that ticks off.

**Communication**

5. **Plain language, no codes.** "We couldn't reach the server. Check your connection and try again." Codes only as an optional "Details" for support.
6. **Precise.** Say what went wrong and where: "The card number has 15 digits; Visa cards have 16." Never "An error occurred" or "Invalid input".
7. **Constructive.** Say how to fix it, or offer the fix as a button ("Use Berlin, 10115"). For out-of-stock, offer a restock date or a notification.
8. **No blame, no jokes.** Avoid "invalid", "illegal", "you failed". Humour wears thin on the second occurrence.
9. **Tognazzini's three tests:** the message explains what went wrong, tells the user specifically what to do, and allows for a deeper system fault. "Error -1264" passes none.

**Efficiency**

10. **Preserve input.** Never clear a form because one field is wrong.
11. **Guess the intent** and offer a short list of corrections ("Did you mean...?").
12. **Teach briefly** how the system works when that prevents the error recurring, linking to more detail.
13. **Total failure** (the service is down): apologise, say what still works, say when to try again.

## 8. Protecting the user's work

Tognazzini: users should never lose work through their own error, a network glitch or a timeout.

1. **Autosave continuously** (drafts, form progress, editor state). Make "Saved" status visible but quiet.
2. **Survive navigation.** Leaving a page or closing a sheet with unsaved content either keeps it as a draft or asks with a "Save draft" option.
3. **Survive sessions.** Restore where the user left off: open tabs, scroll position, half-filled forms, search criteria (Tognazzini's travel sites that wiped searches after a short idle).
4. **Survive errors.** A failed submit keeps every field (his airline form that erased all eight fields on every failed attempt).
5. **Survive going back in a flow.** Earlier steps keep their values.
6. **Version history** for documents and settings where changes are significant.

## 9. Checks

- List every destructive or wide action. For each: undo available? If not, a specific confirmation? Neither is a severity 4 defect.
- Do any confirmations exist for routine or undoable actions? Remove them.
- Does any dialog use Yes/No or OK for a decision? Rename the buttons to outcomes.
- Is the destructive button the default anywhere? Change it.
- Does any error message contain a code, the word "invalid", or no fix? Rewrite it.
- Does any error clear user input? Fix.
- Is there any field that rejects a format a person might naturally type? Make it forgiving.
- Are Delete and a frequent action next to each other at the same size? Separate them.
- Does closing, going back, timing out or losing network ever lose typed content? Fix.
