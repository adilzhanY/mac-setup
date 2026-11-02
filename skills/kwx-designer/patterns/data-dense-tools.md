# Data dense tools

For tools that record time, money or quantities: time tracking, invoicing, booking admin, CRM, inventory. The trial's time tracker lost to a build that showed money beside hours, a week switcher and totals. These are the rules that build had.

## Contents

1. Period navigation
2. Derived values and totals
3. Summary figures
4. Filters
5. Entering time and money
6. Quantified statuses
7. Inputs next to the action
8. Checks

---

## 1. Period navigation

- Every period view (day, week, month) has previous and next buttons with tooltips and accessible names ("Vorherige Woche"), and a reset to the current period that is disabled when already there.
- A label names the period with the ISO week and the dates: "KW 44, 26.10.2026 bis 01.11.2026".
- A Day / Week / Month segmented control when more than one granularity helps.
- Today's group is marked.
- Keys: Alt+Left and Alt+Right (or [ and ]) step, T jumps to today; the tooltips show them.
- The period lives in the URL or the app state, so a reload or Back keeps it.

## 2. Derived values and totals

- Each row shows the derived value next to the raw one: "1:00 h / 90,00 EUR".
- Each group header shows its subtotal.
- Each table of amounts ends with a bold total row.
- A rate column where amounts are derived from a rate.
- A running item counts up live and is included in the totals, or the total says it is excluded.
- A short plain note says how the totals are computed (entries split at midnight, net amounts).
- The parts shown add up to the total shown at the same precision (`visual/data-visualization.md` section 8).

## 3. Summary figures

- On list pages with open or overdue states, 2 to 4 tiles the user acts on: "Offen 2.311,58 EUR / 2 Rechnungen", "Überfällig" in the danger tone, "Noch nicht abgerechnet".
- The amount is large (26 to 32 px, bold, tabular), the count small.
- Each tile filters the list below it.
- Period tiles show hours AND money.
- These are required, not KPI slop. Slop is a tile that repeats a chart, repeats on several pages, or shows 0 on a new account (`quality/ai-slop-tells.md` section 4).
- On a new account with no records, show the first run empty state (gate F10) in place of the tiles; the tiles appear with the first record.

## 4. Filters

- Each dimension is a labelled group (Kursart, Level), with one "Alle" first per group.
- Chips for small sets; a dropdown above about 7 values.
- An active filter count and a Reset.
- The filtered empty state names the active filters and offers Reset.
- On phones a chip row scrolls in its own row with an edge fade; the page never scrolls sideways.
- The selected chip is filled with the brand colour plus a check; unselected chips are outlined.

## 5. Entering time and money

- A new entry opens with: date today, end now rounded to 5 minutes, start = end minus the last duration (or 1 h), the last used project.
- Duration and start/end stay in sync: editing one updates the other.
- Duration accepts 1:30, 1,5, 90m and 1h30. Time accepts 930 and 9.30. Date accepts heute, gestern and the locale date (3.11.).
- The hint names two or three forms ("z. B. 1:30, 1,5 oder 90m") and the parsed value is echoed under the field.
- Amounts show grouping as typed (1.250,00).
- One tested parse function per kind of field, with a test case for every format the hint names.

## 6. Quantified statuses

- A status with a size says it, as a chip: "10 Tage überfällig", "6 Plätze frei", "Ausgebucht", "Läuft seit 1:35".
- Tiered tones: success, warning, danger. Only the urgent state is red.
- Count words use plural rules ("1 Platz frei", "6 Plätze frei"; `premium/copywriting-and-tone.md` section 11).

## 7. Inputs next to the action

An action that writes a value shows its input beside the button, prefilled: "Zahlung erhalten am [29.10.2026] Als bezahlt markieren". A bare "Mark as paid" that stamps today hides a decision the user has to make.

## 8. Checks

| Rule | Check |
|---|---|
| Period navigation | Previous, next, reset (disabled on current), label with KW and dates; the period in the URL or state |
| Derived values | Each row renders the derived value; each group a subtotal; a bold total row |
| Totals agree | A test asserts the displayed parts sum to the displayed total |
| Summary tiles | 2 to 4 tiles on list pages with open states; each has a filter handler |
| Filters | Every chip row has a label and one Alle; Reset and a filtered empty state exist |
| Entry defaults | List each input's initial value on a new entry: date, end, start, project |
| Lenient parse | The hint names the formats; the echo element exists; one parser test per format |
| Statuses | `grep` status strings; each one that has a size carries its number |
| Inputs beside actions | Each action that writes a value renders its prefilled input next to it |
