# Daily use

The 2026-10 trial built three apps twice from the same briefs. The arm with the kwx skills shipped fewer daily features than the arm without: no period navigation, hours without money, statuses in grey text, empty lower halves. The owner preferred the richer build. This file is the counterweight: start every product screen from what its daily user needs, and keep it rich.

## Contents

1. Day in the life
2. Daily questions and moves per screen
3. Rich, not sparse
4. Housekeeping
5. Compare with the references
6. Do not lose these
7. Checks

---

## 1. Day in the life

Write five lines in the brief before designing:

- The 3 tasks the user repeats most, with how often ("logs time 6 times a day", "books a course twice a week").
- The one question they open the product to answer ("how much am I owed", "is there a free place tonight").

A brief that says "replace the spreadsheet" or "usable every day" implies these even when it does not list them. Each repeated task must be doable in one action with smart defaults, and the answer to the daily question must be visible on the first screen.

## 2. Daily questions and moves per screen

For each screen, list:

- **Questions:** what did I do this week, how much is open, what is overdue, when is my next course, how full is the gym right now.
- **Moves:** step back a period, jump to today, enter yesterday's time, fix a forgotten timer, delete a spam entry, export, sign out.

Then:

1. Every question gets a visible answer on the first screen, with the number the user cares about (money beside hours, places beside the time).
2. Every move gets a control.
3. A repeated task is one action with smart defaults (`patterns/forms-and-inputs.md` section 1).

## 3. Rich, not sparse

- Every record shows its key figure, a status chip and its derived value (hours and euros; days overdue as a number; places free).
- A screen with one item fills its column with the next useful thing: the description, the deadline, past items, the next step. An empty lower half while data exists means the screen is unfinished.
- Each card carries one strong signal: a solid chip, an accent number or a colour bar. Pale tints only for secondary chips.
- Restraint and lean cut decoration and code, never information or a daily workflow (`premium/restraint-and-reduction.md`, `workflow/lean-build.md`).

## 4. Housekeeping

Admin and data screens have delete (with a confirm or undo), export, and sign out. They are dull and every daily user needs them; the trial's skills arm left them out.

## 5. Compare with the references

Count the user facing facts and actions on each main screen and compare them with the 3 to 6 references from the brief (Harvest, Toggl, Lexoffice for a German time and invoice tool). Fewer needs a written reason in the report (gate row J9).

## 6. Do not lose these

What the skills arm did better in the trial. Softening restraint must not remove them:

- Skeletons instead of spinners for content areas.
- Separate offline, error, empty and filtered empty views.
- A first run setup checklist.
- Field specific errors with a fix.
- The running entry highlighted with its live duration.
- A confirmation state on detail screens with the cancel deadline.
- A sticky bottom action on mobile detail screens.
- Shortcuts printed on buttons ("Strg N").
- Detail in calculators (the marginal rate, the monthly reserve).
- Contrast checked tokens and a dark mode.

## 7. Checks

The gate section L rows (`quality/quality-gate.md`):

| Row | Check |
|---|---|
| L1 | Each daily question has a visible answer on the first screen |
| L2 | Period views have previous, next, reset, label and a total row |
| L3 | Forms open prefilled; the 3 repeated tasks counted in fields and clicks |
| L4 | Accepted input formats named and the parse echoed |
| L5 | Stale state (a timer over 10 h, an unsaved draft, a stale sync) warned with a fix |
| L6 | Delete with confirm, export and sign out exist |
