# Ponytail: examples slice

Source: `~/.claude/plugins/cache/ponytail/ponytail/5.1.0/examples/` (read only).

## Files read (all in full)

| File | What it is |
|---|---|
| README.md | Index; claims outputs are verbatim benchmark runs (Claude Haiku 4.5, temperature 1, promptfoo); LOC table for 5 of them |
| csv-sum.md | Benchmarked: 20 -> 3 LOC (pandas plus 2 alternatives vs one `csv.DictReader` line) |
| debounce.md | Benchmarked: 116 -> 10 LOC (utility, loading state, cancel option, HTML, CSS, benefits table vs inline clearTimeout/setTimeout) |
| deep-clone.md | Illustrative: lodash or JSON hack -> `structuredClone` |
| email-validation.md | Benchmarked: 75 -> 3 LOC (three versions plus comparison table vs one lenient regex) |
| group-by.md | Illustrative: lodash or reduce -> `Object.groupBy` |
| infinite-scroll.md | Illustrative, UI: react-infinite-scroll-component -> IntersectionObserver sentinel |
| modal-dialog.md | Illustrative, UI: Radix Dialog -> native `<dialog>` plus `showModal()` |
| number-formatting.md | Illustrative, UI: numeral -> `Intl.NumberFormat` |
| rate-limit.md | Benchmarked: 128 -> 10 LOC (six approaches plus table vs one slowapi decorator) |
| react-countdown.md | Benchmarked, UI: 267 -> 9 LOC (four components, styled-components, CSS vs one effect) |
| url-params.md | Illustrative, UI state: query-string -> `URLSearchParams` |

Numbers found: 75->3, 116->10, 20->3, 267->9, 128->10 LOC; modal "1 dependency + 30 lines -> 0 dependencies + 8 lines"; query-string "4.5 kB gzipped, 3.5M downloads/week"; debounce 300 ms; "add a utility when you need it on 3+ inputs"; Object.groupBy Chrome 117, Firefox 119, Safari 17.4, Node 21; structuredClone all browsers since 2022, Node 17; `<dialog>` all browsers since 2022; URLSearchParams Node 10.

Method used for this file: every lesson was grepped in kwx-designer (`grep -rniE ... --include=*.md | grep -v sources/`, 2 to 3 keyword sets each). I also tested the skill's emoji grep (quality-gate.md section 14) against the symbols in the bloated countdown (U+23F8 pause, U+25B6 play, U+21BB reset): zero hits.

Several lessons below are corrections: places where the "With Ponytail" answer is itself wrong or lost something the bloated answer had. They are marked (critique). For a design skill these are the most useful part of the slice.

## A. The general before/after pattern each example teaches

| id | Lesson | Source | Status | Suggested home, reason |
|---|---|---|---|---|
| EX-01 | Before adding a dependency or hand rolling a widget, name the platform feature that already does it (`<dialog>`, IntersectionObserver, Intl, URLSearchParams, structuredClone, Object.groupBy, the csv module) and use it. Order: house component, then platform, then installed dependency, then new code. | all | PARTIAL: `visual/accessibility.md:102` says native HTML elements first; `workflow/design-process.md:64` says reuse shared components. Missing: platform APIs (not only elements) before dependencies, and the full order | `workflow/design-process.md` Build step, one rule with the order |
| EX-02 | When a dependency is a thin wrapper or polyfill over a shipped API ("the library wraps exactly this API", "a polyfill for an API that has shipped everywhere for years"), drop it. | infinite-scroll, url-params | NEW | same rule as EX-01 |
| EX-03 | A dependency is right when it does real work that would take more than a few lines (rate-limit kept slowapi). The test is size of the replacement, not "zero dependencies" as a goal. | rate-limit | NEW | same rule as EX-01, as its limit |
| EX-04 | Give one answer. The bloated outputs offer basic, advanced, hook and styled versions, six rate limit approaches, "Choose the version that best fits your needs", plus a pros/cons table. A menu pushes the decision back onto the user. Pick, and say why in one line. | email, rate-limit, countdown, csv-sum | NEW (grep for menu/variants/one answer found only component variants) | `SKILL.md`, a reply rule; also `quality/ai-slop-tells.md` as a reply tell |
| EX-05 | End with one "Skipped: X, Y, Z. Add when <trigger>." line, so deferred scope is visible and has a condition ("add a utility when you need it on 3+ inputs", "swap Limiter for a Redis backend when you run several servers"). | csv-sum, debounce, email, rate-limit, countdown | NEW | `SKILL.md` workflow step 7 or a "Reply" section |
| EX-06 | Mark the choice in code with one line that says which built-in and why ("browser has one, with focus trapping and backdrop built in"). | all illustrative ones | NEW | `workflow/design-process.md` Build step |
| EX-07 | Check the target runtime before using a newer built-in and cite the versions. If the target is too old, the fallback is the one line native version (the reduce), not the library. | group-by, deep-clone, url-params | NEW (no baseline/support/caniuse rule in the skill) | `platforms/web/web-foundations.md`, browser support line |
| EX-08 | State the limits of the built-in you chose, not only of the thing you replaced. Ponytail lists what the JSON hack drops (Date, undefined, Map, Set, circular refs, functions) but not that structuredClone throws on functions and DOM nodes and drops class prototypes. (critique) | deep-clone | NEW | `SKILL.md` reply rule, "name the limit" |
| EX-09 | Removing a dependency must not remove what it gave for free. Radix wired `Dialog.Title`/`Description` to the dialog and returned focus; the native version dropped the title. The infinite scroll library had a loader and an end message; the native version dropped both. Before deleting, list what the old thing did for accessibility and states, and keep each one. (critique) | modal-dialog, infinite-scroll, debounce | NEW, high value | `quality/quality-gate.md`, a check in the I (accessibility) or F (states) section |
| EX-10 | Shorter is not verified. The ponytail rate-limit answer does not work as written (slowapi needs `request: Request` typed and the `RateLimitExceeded` handler registered; `HTTPException` is imported unused), and the ponytail countdown tears down its interval every tick. A LOC count rewards these. Run or trace the code before calling it done. (critique) | rate-limit, react-countdown | PARTIAL: `quality/quality-gate.md:39` verifies by reading code. Missing: a warning that size metrics reward broken output | `quality/quality-gate.md` intro, one line |
| EX-11 | Snippets must run where pasted, or say what they assume. Ponytail's answers assume markup (`input[type="search"]`), globals (`React.useState` with no import), and undefined handlers (`onConfirm`). (critique) | debounce, countdown, modal | NEW | `SKILL.md` reply rule |
| EX-12 | Show the gain as one quantified line ("1 dependency + 30 lines -> 0 dependencies + 8 lines", "267 -> 9 lines"). | all | PARTIAL: `workflow/redesign-method.md:153` shows before and after with a numbered list; no quantified one liner | `workflow/redesign-method.md` step 4 of the report |
| EX-13 | No marketing in replies: no "Key Benefits" tables, no feature checklists with check marks, no rocket emoji, no heading per variant, no "Here's a complete ..." opener. | debounce, countdown, rate-limit, email | PARTIAL: emoji banned in UI strings (`quality/quality-gate.md:133`), not in the agent's replies | `SKILL.md` reply rule |
| EX-14 | Measure a skill A/B: same model, same prompt, no-skill arm vs skill arm, temperature 1, verbatim outputs saved, one reproduce command, median of 10 runs across 3 models. | README | NEW: `evals/evals.json` has 3 prompts with assertions, no baseline arm, no repeat count, no runner | `evals/` README plus a runner script |
| EX-15 | Keep real before/after pairs from those runs as teaching examples next to the rules. | README | NEW (the skill has before/after from videos, none from its own runs) | new `evals/examples/` |
| EX-16 | Label which examples are measured and which are illustrative. Ponytail's README says "These are not hand-written" but 6 of its 11 examples have no benchmark header and are not in the table. (critique) | README | NEW | `evals/` README |

## B. UI and accessibility lessons

### Modal dialog

| id | Lesson | Source | Status | Suggested home, reason |
|---|---|---|---|---|
| EX-17 | Build modals on native `<dialog>` opened with `showModal()` (not `show()`, which is non-modal): top layer, the rest of the page inert, Escape closes, `::backdrop` for the scrim, no portal, overlay, root or trigger wrappers. | modal-dialog | PARTIAL: `visual/accessibility.md:102` lists `<dialog>`; missing `showModal` vs `show`, `::backdrop`, inert, no portal | `visual/accessibility.md` section on native elements |
| EX-18 | Correct the claim "traps focus automatically": showModal makes the page inert, but Tab can still leave to the browser chrome, and focus return to the opener is only reliable in current browsers. Check return focus, set it yourself if older browsers matter. (critique) | modal-dialog | PARTIAL: trap and return rules exist (`quality/quality-gate.md:158`, `platforms/desktop/keyboard-and-command-palette.md:75`), not the native dialog's actual behaviour | `visual/accessibility.md` |
| EX-19 | Give every dialog an accessible name: a heading with `aria-labelledby`, and `aria-describedby` on the consequence text. Ponytail's native version dropped the Radix `Dialog.Title`, so the dialog has no name. (critique) | modal-dialog | NEW (accessible name rules in the skill cover icon buttons and images only) | `visual/accessibility.md` and gate item I5 |
| EX-20 | Put buttons in `<form method="dialog">` so they close the dialog and set `returnValue` with no click handlers. Handle the `cancel` event (fired on Escape) so Escape runs the same path as Cancel; ponytail's version never calls `onCancel` on Escape. (critique) | modal-dialog | NEW | `patterns/saas-app-patterns.md` dialog rules (line 73 area) |
| EX-21 | Delete confirm: name the object and the consequence, safe focus on Cancel, destructive button red and last. With native dialog, initial focus goes to the first focusable element or the one with `autofocus`, so put `autofocus` on Cancel rather than relying on source order. | modal-dialog | PARTIAL: rule COVERED at `psychology/defaults-and-choice.md:88`, `patterns/states-feedback-and-failure.md:113`, `quality/quality-gate.md:44`; the native `autofocus` mechanism is missing | `patterns/states-feedback-and-failure.md:113`, one clause |
| EX-22 | A native modal does not close on backdrop click by default. Decide light dismiss on purpose (`closedby="any"` where supported, or a click handler that checks `event.target === dialog`), and keep it off for destructive confirms so a stray click is not an answer. (critique) | modal-dialog | NEW | `patterns/saas-app-patterns.md` dialog rules |

### Infinite scroll and feeds

| id | Lesson | Source | Status | Suggested home, reason |
|---|---|---|---|---|
| EX-23 | Load the next page with an IntersectionObserver on a sentinel after the last item, not a scroll listener; no throttling, no jank. Disconnect in cleanup. | infinite-scroll | PARTIAL: IntersectionObserver appears only for starting video (`platforms/web/performance-and-loading.md:94`) | new `patterns/lists-and-feeds.md`, or a section in `patterns/states-feedback-and-failure.md`; the skill has no list/feed pattern at all |
| EX-24 | Prefetch early with `rootMargin` (a few hundred px) so the next page arrives before the user hits the end. | infinite-scroll (critique) | NEW | same |
| EX-25 | Guard against duplicate loads: the observer can fire again while a page is still loading. Keep an in-flight flag; keep `fetchMore` stable so the observer is not rebuilt each render. (critique) | infinite-scroll | PARTIAL: double submit covered for forms (`patterns/forms-and-inputs.md:81`), not for list loading | same |
| EX-26 | Keep the feed states: a loading row while the next page fetches, an end of list message, an error row with retry. The ponytail version silently stops. (critique) | infinite-scroll | NEW (no end of list state anywhere in the skill) | same, and `quality/quality-gate.md` state list |
| EX-27 | Infinite scroll locks keyboard and screen reader users out of the footer and loses their place. Prefer a "Load more" button (or add one as fallback), announce "20 more items loaded" with `aria-live="polite"`, keep focus where it was, restore scroll on Back. | infinite-scroll (critique) | PARTIAL: live regions (`visual/accessibility.md:107`) and scroll restore (`platforms/web/web-foundations.md:58`) covered; footer reachability and load more button missing | same |

### Countdown timer

| id | Lesson | Source | Status | Suggested home, reason |
|---|---|---|---|---|
| EX-28 | Ticking numbers use `font-variant-numeric: tabular-nums` so the digits do not jitter each second. The bloated version had it; the ponytail version dropped it. (critique) | react-countdown | PARTIAL: tabular figures covered for columns and scrubbing (`quality/quality-gate.md:78`, `editors/inspector-and-numeric-input.md:82`), not for live counters and clocks | `premium/details-and-polish.md` tabular numbers line |
| EX-29 | Compute remaining time from a fixed end timestamp on each tick; do not decrement a counter per `setInterval` call. Intervals drift and are throttled in background tabs, so the timer runs slow. | react-countdown (critique) | PARTIAL: `psychology/psychology.md:70` says the end time must come from a stored deadline (for honesty), not the drift and background throttling reason | `psychology/psychology.md:70`, add the technical reason; or new `patterns/lists-and-feeds.md` sibling for live values |
| EX-30 | One interval for the timer's lifetime, not one per tick: ponytail's effect depends on `[remaining]`, so it is torn down and recreated every second. Reset when the `seconds` prop changes. (critique) | react-countdown | NEW | same home as EX-29 |
| EX-31 | Timer accessibility: `role="timer"` (its implicit live setting is off) so a screen reader is not interrupted every second; announce only milestones (1 minute left, done) in a separate polite live region; expose readable text ("45 seconds", or `<time datetime="PT45S">`), not "45s". | react-countdown (critique) | NEW | `visual/accessibility.md` |
| EX-32 | Show durations over a minute as m:ss (or h:mm:ss), never as a bare "245s"; `Intl.DurationFormat` where supported. Define what happens at zero. | react-countdown | NEW | same home as EX-29 |
| EX-33 | Warning state near zero: the bloated version pulses opacity to 0.5 forever (`pulse 0.5s infinite`), with no reduced motion guard and a contrast drop. Change colour or weight once, pulse at most once, respect reduced motion. | react-countdown | COVERED: `principles/laws-of-ux.md:194` (pulse once), `visual/accessibility.md:80` (reduced motion) | none |

### Slop tells in the bloated UI code

| id | Lesson | Source | Status | Suggested home, reason |
|---|---|---|---|---|
| EX-34 | Unicode media symbols as button icons (U+23F8 pause, U+25B6 play, U+21BB reset) are slop. The gate's emoji grep `[\x{1F300}-\x{1FAFF}\x{2600}-\x{27BF}]` does not catch them (tested: zero hits). Widen it with `\x{2190}-\x{21FF}\x{2300}-\x{23FF}\x{25A0}-\x{25FF}\x{2B00}-\x{2BFF}`. | react-countdown | PARTIAL: rule COVERED at `quality/ai-slop-tells.md:31`; the grep in `quality/quality-gate.md:202` misses these ranges | `quality/quality-gate.md` section 14 and `quality/ai-slop-tells.md:30-31`, fix the regex |
| EX-35 | The `#667eea -> #764ba2` purple gradient is the most common AI default. Add both hexes to the palette grep. | react-countdown | PARTIAL: rule COVERED at `quality/quality-gate.md:100`; the grep list lacks these two hexes | `quality/quality-gate.md` section 14 |
| EX-36 | `transition: all 0.3s` and hover `translateY(-2px)` lifts on buttons. | react-countdown | COVERED: `premium/motion-and-feel.md:225`, `premium/motion-and-feel.md:250`, `platforms/web/web-foundations.md:93` | none |
| EX-37 | Never build result markup from template strings into `innerHTML` (`${item.title}` is an injection hole); use `textContent` or the framework's escaping. | debounce | NEW (no innerHTML or escaping rule) | `platforms/web/web-foundations.md` |

### Search input with debounce

| id | Lesson | Source | Status | Suggested home, reason |
|---|---|---|---|---|
| EX-38 | Debounce remote search at about 300 ms with clearTimeout plus setTimeout inline; make a utility only when 3 or more inputs need it. Local filtering stays instant. | debounce | PARTIAL: `platforms/desktop/keyboard-and-command-palette.md:97` covers local results (no debounce above 50 ms); the remote 300 ms case is missing | `patterns/forms-and-inputs.md` search row |
| EX-39 | Debounce does not stop stale results: a slow earlier response can land after a newer one and overwrite it. Abort the previous request (`AbortController`) or drop responses whose query is no longer the current one. (critique) | debounce | NEW | `patterns/states-feedback-and-failure.md` loading section |
| EX-40 | Search states: empty query clears results with no request, loading indicator in the field, error with retry, no results. Ponytail's answer leaves all of them as `console.log` "replace with your render". For UI, states are part of the job, never "Skipped". (critique) | debounce | PARTIAL: loading in field (`patterns/forms-and-inputs.md:61`), no results (`patterns/states-feedback-and-failure.md:71`), all states (`SKILL.md` rule 5) covered; empty query clearing missing | `patterns/forms-and-inputs.md` |
| EX-41 | Search markup: `<input type="search">` inside a `<search>` element (or `role="search"`) with a label; a placeholder "Search..." is not a label. | debounce (critique of both arms) | PARTIAL: visible labels covered (`platforms/web/web-foundations.md:64`); `type="search"` and the search landmark missing | `platforms/web/web-foundations.md` forms lines |
| EX-42 | Inputs at 16 px or more so iOS does not zoom on focus (the bloated CSS had this right). | debounce | COVERED: `visual/accessibility.md:97`, `platforms/web/web-foundations.md:113` | none |

### Number and money formatting

| id | Lesson | Source | Status | Suggested home, reason |
|---|---|---|---|---|
| EX-43 | Format currency, percent and compact numbers with `Intl.NumberFormat`; never hand roll separators or symbols. | number-formatting | COVERED: `platforms/web/web-foundations.md:75`, `premium/typography-craft.md:132`, `visual/data-visualization.md:63` | none |
| EX-44 | Do not hardcode the locale. Ponytail's example passes `"en-US"` and then calls itself locale aware. Pass `undefined` (or `navigator.languages`) and take the currency code from the data, not the locale: a German visitor sees a USD price as "1.234.567,89 $". (critique) | number-formatting | PARTIAL: locale rule covered; the hardcoded locale trap and currency from data are missing | `platforms/web/web-foundations.md:75` |
| EX-45 | Build each formatter once and reuse it; one `formatPrice` everywhere. | number-formatting | PARTIAL: one formatter covered (`psychology/pricing-psychology.md:94`, `patterns/product-pages-and-commerce.md:136`); build once for speed in long lists missing | `patterns/dashboards-and-data.md` |
| EX-46 | Compact output differs by library and locale ("1.5k", "1.5K", "1,5 Tsd."): never assume its length in layout or tests, and show the exact value on hover or in a detail view because compact hides precision. | number-formatting | NEW | `visual/data-visualization.md:63` |
| EX-47 | Never sum money in floats (`float(row['amount'])`); use integer minor units or Decimal. And never concatenate a currency symbol (`f"${total:,.2f}"`). | csv-sum (critique of both arms) | PARTIAL: no string concatenation for prices covered (`psychology/pricing-psychology.md:94`); float arithmetic missing | `patterns/product-pages-and-commerce.md` price row |

### URL state

| id | Lesson | Source | Status | Suggested home, reason |
|---|---|---|---|---|
| EX-48 | Keep filters, tabs and page in the URL. | url-params | COVERED: `platforms/web/web-foundations.md:57`, `premium/details-and-polish.md:148` | none |
| EX-49 | Read and write it with `URLSearchParams`; `getAll` for repeated keys; `append` to build them. Values come back as strings ("2"), so parse and validate them at the boundary, since a URL is user input. | url-params | PARTIAL: the rule is covered, the API and the string/validation pitfall are not | `platforms/web/web-foundations.md:57` |
| EX-50 | Use `history.replaceState` while a filter is being typed and `pushState` for real navigation, so Back is not flooded with one entry per keystroke. | url-params (critique, not in the source) | NEW | `platforms/web/web-foundations.md:57` |

### Email field

| id | Lesson | Source | Status | Suggested home, reason |
|---|---|---|---|---|
| EX-51 | On the front end, `type="email" autocomplete="email"` gives native checks and the right keyboard. | email-validation | COVERED: `platforms/web/web-foundations.md:65`, `visual/accessibility.md:113` | none |
| EX-52 | Validate email leniently (something@something.something). Strict patterns like `[a-zA-Z]{2,}` for the TLD reject valid non ASCII and new domains, and the only real proof is a confirmation email. | email-validation | NEW | `patterns/forms-and-inputs.md` validation section |
| EX-53 | Lenient is not sloppy: ponytail's `[^@]+` accepts spaces and line breaks. Use `[^@\s]+`, and trim first. Its "Skipped" line also names `user+tag@sub.domain.co.uk` as something to reject, which is a valid address: review the skipped line as carefully as the code. (critique) | email-validation | NEW | same |
| EX-54 | Error messages say what is wrong and how to fix it (the bloated "advanced" version returned "Local part is too long", which is better than a bare False). | email-validation | COVERED: `visual/accessibility.md:114`, `quality/quality-gate.md:116` | none |

## Counts

NEW 26, PARTIAL 21, COVERED 7 (54 lessons).

- COVERED: EX-33, 36, 42, 43, 48, 51, 54
- PARTIAL: EX-01, 10, 12, 13, 17, 18, 21, 23, 25, 27, 28, 29, 34, 35, 38, 40, 41, 44, 45, 47, 49
- NEW: EX-02, 03, 04, 05, 06, 07, 08, 09, 11, 14, 15, 16, 19, 20, 22, 24, 26, 30, 31, 32, 37, 39, 46, 50, 52, 53
