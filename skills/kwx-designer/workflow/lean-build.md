# Lean build

How to build or change UI code with the least new code that fully does the job. Lean applies to the solution, never to the work: read everything the change touches, finish every caller, keep every state. The result is small because each part is necessary, not because lines were golfed ("the rule was never fewest tokens", ponytail README).

Distilled from the ponytail Claude Code plugin (5.1.0) and its benchmarks, translated to interface work. Numbers quoted below are ponytail's own measurements.

## Contents

1. Read before you build
2. The reach order
3. When a dependency is right
4. Replacing something keeps what it gave
5. The smallest complete change
6. Fixing a reported defect
7. Never cut
8. Logic gets one check
9. The deferral marker
10. The reply
11. Checks

---

## 1. Read before you build

1. Read the request and the code it touches before choosing anything. The reach order in section 2 runs after understanding, not instead of it.
2. Write the scope list: every place the change must reach. For UI that is the screens and components you edit, every file that imports a component, prop or token you change (`grep -rn "ComponentName" src`), the wiring a new feature needs (route, nav entry, settings row, persistence, the code that reads it on launch), and the tests, stories, snapshots and fixtures that render it. Scope is this list. Features nobody asked for are not scope.
3. Write one line on what the change could break for users: data it could destroy or expose, a caller whose props or return value no longer match, a screen that loses a state.
4. A renamed prop or field, or a changed return shape, breaks code the diff never touches. In ponytail's benchmark a renamed field crashed an untouched `src/routes/feed.js`. Grep every caller before you rename.
5. A new setting is done only when it is in the settings screen, persisted, read on launch and reflected in every screen that uses it.

## 2. The reach order

Stop at the first rung that fully does the job:

1. **Does it need to exist?** Skip options, variants and flexibility nobody asked for, and name each skipped thing in the reply's Skipped line (section 10).
2. **Does the codebase have it?** The house component, hook, token or helper, used the way the surrounding code uses it. A house component beats a native element: when the app has a `ConfirmDialog`, a delete uses it, not `window.confirm` and not a fresh `<dialog>`.
3. **Does the platform have it?** Web: `<dialog>` with `showModal()`, `<details>`, `<input type="date">`, `type="color"`, `type="file"`, `type="search"`, `IntersectionObserver`, `Intl.NumberFormat` and `DateTimeFormat`, `URLSearchParams`, `structuredClone`, `AbortController`, CSS `scroll-snap`, `:focus-visible`. QML: the project's component library first, then Qt Quick Controls.
4. **Is it in an installed dependency?** Use it before adding another.
5. **Otherwise** the minimum new code that works, in the structure the codebase already has (its layers, component folders, naming).

Example, ponytail on a real repo: "add a date picker" produced a library or a hand built calendar (335 lines) without the rule, and the repo's own `Input` with `type="date"` (10 lines) with it. A colour picker went from 287 to 23 lines, a dropzone from 251 to 95. The large wins always came from a native control replacing a custom build.

Before using a newer platform API, check the target runtime and write the versions in a code comment (`Object.groupBy`: Chrome 117, Firefox 119, Safari 17.4; `structuredClone`: every browser since 2022). If the target is older, the fallback is a few plain lines (a `reduce`), not a library.

State the limits of the built-in you chose, not only those of what it replaced: `structuredClone` throws on functions and DOM nodes and drops class prototypes; `<input type="date">` returns a `YYYY-MM-DD` string and a calendar drawn by the browser that you cannot style.

## 3. When a dependency is right

- Never add a dependency for a few lines: a date picker the browser has, an icon pack for three icons (draw them, see `icons/icons.md`), an animation library for one transition, a query string parser over `URLSearchParams` (query-string is about 4.5 kB gzipped for what the platform does).
- Drop a dependency that is a thin wrapper or a polyfill over an API that has shipped everywhere for years.
- Keep one that does real work you would need more than a few dozen tested lines to replace (ponytail kept `slowapi` for rate limiting). The test is the size and risk of the replacement, not "zero dependencies" as a goal.

## 4. Replacing something keeps what it gave

Removing a dependency or rewriting a component must not remove what it did for free. Before deleting, list what the old code provided for accessibility and states, and keep each item:

- Radix `Dialog.Title` and `Dialog.Description` named the dialog. Ponytail's own native rewrite dropped the title, so the dialog had no accessible name.
- An infinite scroll library showed a loader and an end message. The native rewrite silently stopped at the end.
- A countdown that had `tabular-nums` lost it in the rewrite and started to jitter.
- A redesign that moves a form keeps its validation, `aria-*` attributes, error, empty and loading branches.

Operation: before deleting the old file, `grep -nE 'aria-|role=|disabled|error|empty|loading|focus|tabular' old-file` and tick off every hit in the new file.

## 5. The smallest complete change

- Finish every part the task needs. Each importer, test, story and fixture your change breaks is part of the change.
- No prop, variant, wrapper, context, config or "for later" option nobody asked for. A `size` prop with one value in use, a `variant="ghost"` no screen renders, a wrapper component that only passes props through: delete them.
- Keep values in the form the platform gives you. The ISO string from a date input stays a string until something needs a `Date`.
- Props and return values follow what callers already expect. A validator that returned `{isValid, message}` where callers wrote `if (validate(x))` let every value pass (0 of 40 in ponytail's audit).
- The shortest working diff wins, once you know everything it must touch. A one liner the reader must decode is not short.
- Between two options of the same size, take the one that is correct on edge cases: empty, zero, the last item, a 40 character name, rounding, another time zone.
- Split components by job, never by line count, and never into helpers that exist only to make a file shorter.
- Before calling code unused, grep the whole tree including tests, fixtures, config and names built from strings (`"icon-" + name`, class names assembled at run time, tokens looked up by key).
- Comment only the why the code cannot show, in one line ("native dialog: Escape and the scrim come with showModal").
- Make the right move the cheap one: one token edit is a smaller diff than ten local overrides; one fix in the shared component is smaller than one per screen.

## 6. Fixing a reported defect

1. Find the shared source first: the component, token or style every affected screen takes it from. Grep every user of it.
2. Fix the root cause once, there. A fix in one screen while the shared component stays broken is itself a defect, and a review finding.
3. Check that every other user of that source still renders right after the fix.
4. Write the defect into the project's mistakes library when it has one.

Why this is written as an operation: in ponytail's test the instruction "trace the flow end to end" fixed 0 of 3 runs, while "grep every caller of the function you touch and fix the shared function once" fixed 6 of 6.

## 7. Never cut

Simplification never removes:

- validation at trust boundaries (form input, URL parameters, data from storage or the network);
- error handling that prevents data loss (typed input kept on failure, autosave, undo);
- security (escaping, permission checks);
- accessibility: labels, accessible names, focus styles, focus management, reduced motion, live announcements;
- states: loading, empty, error, offline, limit, disabled;
- the calibration real hardware needs (scale factors, DPI, safe areas, the compositor's own gap values);
- anything the user asked for.

A pure "write less" prompt was the shortest arm in ponytail's benchmark and the only one that dropped a guard (a path traversal check). Tests, ARIA, focus styles and state branches are never counted as bloat.

## 8. Logic gets one check

New non trivial logic in UI code leaves one small test or an assert based self check: a branch on data, a parser, a formatter, price or savings maths, date and duration maths, a layout calculation (does this text fit, how many columns). One test that fails when the logic breaks, not coverage. Markup and style changes need none. Ponytail: tests where the logic needed one, 98% with the rule against 68% without.

## 9. The deferral marker

A deliberate simplification with a known limit gets a comment in this exact form, so the limit lives in the code where the next reader sees it:

```
// kwx-defer: <the limit>, <when to upgrade>
// kwx-defer: native date input (value is YYYY-MM-DD), swap for a calendar popover when date ranges are needed
```

- The word is `kwx-defer`, never "shortcut". In this skill a shortcut is a keyboard shortcut (`editors/shortcuts-and-command-search.md`), so a grep for it finds keymaps. A repo that already uses another marker (ponytail writes `shortcut:`) keeps its own, and the harvest greps both.
- Always write the comma and the upgrade trigger. A marker with no trigger rots: "later" means never.
- A marker in a code comment is allowed. A placeholder shown to users ("TODO", "Coming soon", lorem ipsum) is always a fail.
- The harvest commands are in `quality/quality-gate.md` section 14.
- In a review, a marker that names its limit is a decision, not a finding, unless the expected load already crosses that limit.

## 10. The reply

- **One answer, not a menu.** No basic, advanced and hook versions, no "choose the version that fits your needs", no table of six approaches. Pick one and say why in one line.
- **Vague request, smallest real version.** "Build me X" gets the smallest version that does the core job, built now, with the left out parts named. Ask only when a wrong guess would waste the work. When a requested element has no job, say so in one line before building it.
- **End with two lines:** `Skipped: <X, Y>. Add when <trigger>.` and what was not checked plus any risk the user must know.
- **Count the gain** when you replaced something: "1 dependency and 30 lines became 0 dependencies and 8 lines".
- **Snippets run where pasted**, or say what they assume (imports, the markup they query, the handlers they call).
- **No marketing in the reply:** no "Key benefits" table, no check mark feature lists, no emoji, no "Here's a complete..." opener. If the explanation is longer than the code, cut the explanation.
- **No invented impact numbers.** The version you did not build was never written, so "saved 40% of the code" has no baseline.
- **Do not narrate** the reach order or the checklist. Apply them.
- **Shorter is not verified.** Ponytail's own short rate limit answer did not run (the error handler was never registered), and its short countdown rebuilt its interval every second. Trace or run the code before calling it done.

## 11. Checks

| Check | Pass when | Verify by |
|---|---|---|
| Scope list | Every importer of a changed component, prop or token is listed and still works | `grep -rn` the changed names; read each hit |
| Reach order | No new dependency or custom widget where a house component, native element or installed library does the job | Read the new imports and the package diff |
| Nothing lost | Every `aria-`, state branch and focus rule of replaced code exists in the new code | The section 4 grep on the old file, ticked off |
| No speculation | Every new prop, variant and option is used by a screen today | Grep each new prop name for a caller |
| Root cause | A reported defect is fixed in the shared source, not per screen | The fix lands in the component or token file |
| Never cut | Validation, states, accessibility and calibration all still present | Diff for removed branches and attributes |
| One check | Each new branch, parser, formatter or money calculation has a test or assert | Find the test next to it |
| Markers | Every `kwx-defer:` has a limit and an upgrade trigger | Section 14 harvest of the quality gate |
| Reply | One answer, Skipped line with a trigger, not checked line, no menu | Read the reply before sending |
