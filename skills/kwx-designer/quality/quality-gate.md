# The quality gate

Run this gate before you call ANY piece of UI done: a new screen, a fix, a component, a redesign, a one line style change. It is permanent. It does not get skipped because the change is small, because the user is in a hurry, or because a screenshot "looks fine".

Check by reading the code, never by taking screenshots, opening the app on the user's screens, moving the mouse or typing. Work the real sizes out from the code at the current scale (`quality/predict-from-code.md`) and predict the render. Use a screenshot only when the user gives one. What only the screen can show goes in the report under "Only your eyes can confirm".

## Contents

1. How to run the gate
2. A. Intuitiveness
3. B. Hierarchy
4. C. Spacing and alignment
5. D. Type
6. E. Colour
7. F. States
8. G. Copy
9. H. Consistency across screens
10. I. Accessibility
11. J. Premium details
12. K. Honesty
13. L. Daily use
14. Report format
15. Fast code checks (copy and run)

---

## 1. How to run the gate

1. Read the local mistakes library (the project's, or ~/.claude/ui-designer/mistakes.md) and `quality/mistakes-library.md` first. Then list every screen and component the change touches, and every state of each (default, hover, focus, pressed, disabled, loading, empty, error, offline, limit, long content, no content). Add every file that imports a component, prop or token you changed (`grep -rn` the names), the wiring a new feature needs (route, nav, settings, persistence), and the tests and stories that render it. Each must still work: they are part of the change (`workflow/lean-build.md`).
2. Write one line on what the change could break for users: data destroyed or exposed, a caller whose props no longer match, a screen that lost a state.
3. Go through sections A to L. Run every row. Write evidence only for [critical] rows and for any FAIL or fixed row; passing non critical rows are a count per section ("B 7/7"). Spend the time saved on section L and on comparing each main screen with the step 2 references (J9).
4. Fix every FAIL, then run the failed items again. Do not report done with an open FAIL.
5. Run the fast code checks in section 15.
6. Go through every mistakes library entry, one line each (`scoring-rubric.md` is not used for builds; it is for critiques of someone else's UI).
7. Report in the format of section 14.

Rows always run; only the write up scales (`enforcement.md` rule 7).

A shorter version is not a verified one: size metrics reward code that does not run. Trace every changed handler before calling it done.

An item marked **[critical]** blocks shipping on its own.

## 2. A. Intuitiveness

| # | Check | Pass condition | Verify by reading code |
|---|---|---|---|
| A1 [critical] | One obvious next step | Each area (header, hero, a dialog, a closing band) has exactly one filled primary, and a new user could name the screen's next step in 3 seconds. The header CTA repeating the hero action is allowed | Count primary styled elements per area: 1 |
| A2 [critical] | Every action answers: what happened, can I undo, what next | Each handler leads to a visible result, a way back, and an obvious next step | For each handler, find the feedback it triggers and the undo/back path |
| A3 | Signifiers without instructions | Grouped, selected, inactive and clickable are distinguishable without help text | Selected, disabled and hover styles exist and differ; inactive items are not clickable |
| A4 | Conventions kept | Back is top left, close is an X, destructive is red and last, search looks like search | Read placement of these controls |
| A5 | Data drives the form | Enums are chips, numbers right aligned, people avatars, time absolute plus relative | Read each cell or field renderer |
| A6 | Progressive disclosure ranked | Frequent actions visible; rare actions in a menu; safe actions (copy, open, pin) may appear on hover | Count visible buttons per row: 3 or fewer as quiet text buttons, a menu at 4 or more |
| A7 | Smart defaults | Every predictable input has a real initial value in body colour (last used choice, today, now rounded); CTA enabled on first paint. A placeholder that looks like data (a time, date, amount, real looking email) or reads "Optional" fails | List each input, its initial value and placeholder; read the CTA `disabled` expression |
| A8 | Inputs next to the action they feed | Stepper beside the button, filters beside the list | Read the layout container |
| A9 | Consequence in the action | CTA label says what happens and, when known, the count or total | Read label strings and expressions |
| A10 | One screen, one job (mobile) | Focused screens (editor, settings) have no unrelated sections | Read the screen's children |
| A11 | Tooltips on icon only controls | Every icon only button has a tooltip and an accessible name | Search icon buttons without `title`/`aria-label`/Tooltip |
| A12 | Gestures have a visible alternative | Each swipe or long press action also exists as a control | Map gesture handlers to buttons or menu items |
| A13 [critical] | Nothing destructive on hover | Delete, remove, forget, unpair, disconnect, discard never sit on a control that appears on hover; they live behind a ... or right click menu and take a second deliberate step (a confirm naming the thing, or an undo window) | Every handler named delete/remove/forget/unpair reachable from a hover revealed element passes a confirm or undo |

## 3. B. Hierarchy

| # | Check | Pass condition | Verify by reading code |
|---|---|---|---|
| B1 [critical] | Squint test | Blurred, the most important thing is seen first, the second thing second | List elements with size, weight, colour; rank by visual weight; the order matches the intended order |
| B2 | No competing primaries | Title, badge and CTA do not all use the heaviest weight or brightest colour | Compare the style tokens of the top 3 elements |
| B3 | Most important near the top, larger, bolder | The key item is the largest text in its card; the focal figure is the largest text on the screen | Read font tokens per element in the card and on the screen |
| B4 | Secondary info muted by colour, directly below | Meta lines use a muted colour token, at most one size step smaller, never below the floor | Read the meta line tokens |
| B5 | The one different value has its own colour and place | At most one brand accent value per card (the key figure), plus its semantic status chip | Count brand accent texts per card: at most 1, status chips excluded |
| B6 | No equal weight label: value lists | Summary cards drop labels the format explains | Search for repeated `Label:` patterns in a card |
| B7 | Headlines attract, paragraphs support | Body text is lighter and smaller than headings | Compare tokens |

## 4. C. Spacing and alignment

| # | Check | Pass condition | Verify by reading code |
|---|---|---|---|
| C1 [critical] | One margin system | All content blocks on a screen start and end on the same edges | Horizontal padding/margin for content uses one token; no stray values (a 17 px offset was the strawberry page's tell) |
| C2 | 4 point scale | Every spacing, size and radius is a multiple of 4 (2 allowed for hairline details) | `grep` numbers in spacing props; all from tokens or multiples of 4 |
| C3 | Proximity groups | Gaps inside a group are smaller than gaps between groups (for example 16 vs 32) | Compare the gap tokens used inside and between groups |
| C4 | No oversized gaps | No gap is noticeably larger than the rest without a reason | List vertical gaps on the screen; outliers have a reason |
| C5 | No nested cards | No card inside a card (padding on padding) | Search the tree for card in card |
| C6 | Button padding ratio | Horizontal padding about twice the vertical | Read button padding tokens |
| C7 | Icon to text | Icon size equals the text line height; tight gap | Compare icon size and line height tokens |
| C8 [critical] | Text fits its box | Longest realistic string fits at the current scale in the width left after padding and siblings | characters x font px x 0.6 (regular) or 0.65 (semibold, bold), digits and % included, plus 15% margin (`predict-from-code.md` section 3); own labels never elide (ellipsis only for user data, full value in a tooltip); siblings of a wrapping label nowrap and flex-shrink 0 |
| C9 | Numbers aligned | Numeric columns right aligned, tabular figures | Read numeric cell styles |
| C10 [critical] | Content fits its shape | A number in a ring, a glyph in a disc, a badge on an icon: the widest value fits with room | widest value + 15% each side < diameter minus 2 x stroke minus padding; if not, the shape grows (`predict-from-code.md` section 5) |
| C11 | Icon fills its container | The glyph fills 40 to 55% of its disc or button | icon / disc between 0.40 and 0.55, set explicitly through the scale on big discs; read what the house component picks by default |
| C12 | Sizes scale together | Fonts from tokens, every other measurement through the scale function or a named metric | the C12 grep in section 15; each hit is 0, 1 (a hairline), or a listed exception (compositor gaps, hardware thresholds, a pill sentinel) |
| C13 [critical] | No sideways page scroll at 360 and 390 px | Nothing makes the page wider than the viewport on a phone | Wide elements sit in an overflow-x box; flex and grid children have min-width 0; tables become cards per row below 640 px; with kwx-tester, measure scrollWidth <= innerWidth on every route |
| C14 | Navigation labels fit their slot | Tab bar and sidebar labels stay on one line at the largest allowed font scale | chars x px x 0.65 <= slot width minus 8; tab bar height computed from content; shortcut hints nowrap; shorten the word before shrinking |

## 5. D. Type

| # | Check | Pass condition | Verify by reading code |
|---|---|---|---|
| D1 [critical] | One family | One font family (a mono for code or data is allowed) | `grep` font family declarations; one source token |
| D2 | Size count | 6 or fewer sizes per view; app running text 24 px or below; key figures 26 to 32 px; one focal figure up to 44 px; mobile titles per platform | Count distinct size tokens per view |
| D3 | No literal sizes | Every size comes from the type scale tokens | `grep` for literal px font sizes outside the token file |
| D4 | Large headings tightened | Letter spacing -2% to -3%, line height 110% to 120% on display text | Read heading tokens |
| D5 | Body readable | Body line height about 1.5 to 1.6; mobile body at least the platform base (17 px iOS) | Read body tokens |
| D6 | Small caps tracked | Small uppercase labels have positive letter spacing | Read label tokens |
| D7 | Sentence case | Buttons, field labels and table headers in sentence case; uppercase only on one or two word eyebrows at the smallest size with +0.05 to +0.12em tracking (`visual/typography.md` section 4) | `grep` for `uppercase` / `text-transform` on buttons and long strings in caps |
| D8 | Weights | No more than 3 weights; page titles 700, section headings 600 to 700, body 400; nothing below 400 | Count weight tokens; read the title and heading weights |
| D9 | Floor | No text below the smallest token of the scale | Read the smallest size used |

## 6. E. Colour

| # | Check | Pass condition | Verify by reading code |
|---|---|---|---|
| E1 [critical] | Every colour has a purpose | Each colour is the brand ramp, a neutral, or a semantic colour with meaning | List every colour token used on the screen and name its meaning; unnamed ones fail |
| E2 | One filled primary per area | One filled primary per area; the brand colour may also mark the current nav item, the selected segment or chip, key numbers and links; selected states never near black when the brand is not black | Count primary variant buttons per area; read the selected state colours |
| E3 | No AI default palette | No generic navy plus purple gradient, no neon accents; neutrals tinted toward the brand | Read the palette; the `#667eea` to `#764ba2` gradient, or hexes like `#7c3aed`, `#6366f1`, `#8b5cf6` with a navy `#0f172a`-style background without a brand reason fail |
| E4 | Desaturated | No pure neon hues (`#00ff00`, pure yellow) unless the brand demands it | Read hex values |
| E5 | Red reserved | Red only for error, danger, urgent. Stop, pause, cancel a running timer or upload, and close are not destructive: neutral or primary. Red only when data or money is lost. A red filled button visible on every screen fails | `grep -rnE -e 'variant=\{?"danger' -e 'btn-danger' -e 'bg-danger'`; each hit names its destructive action |
| E6 | Semantic colour never alone | Status uses icon plus word, not colour only | Read chip and status components |
| E7 | Dark mode depth | Raised surfaces lighter than the background; borders low contrast; chips dimmed with bright text | Read dark surface and border tokens |
| E8 | Colour in data, not decoration | Charts, status chips, a fixed set of 4 to 6 muted category hues reused on every screen with a word; an icon tile only in the brand tint for an icon that names its object; no rainbow discs or per card border colours for emphasis | Search for tinted icon backgrounds and coloured borders; each maps to a category, status or the brand tint |
| E9 | Blur test | Blurred, only meaningful colour signals remain | Same list as E1: every saturated area is a signal |
| E10 [critical] | Control visible on its surface | A filled control separates from the real surface behind it | Walk up the tree to the real parent surface; fill vs surface per channel delta over 10 (`contrast_check.py --surface <bg> <fill>`); use the variant made for that surface; the label still 4.5:1 |
| E11 | Status in tone | Availability, booking, payment and sync status render as a chip with a tone, words and its number; tiered success, warning, danger | Read each status renderer; a status in muted caption text fails |

## 7. F. States

| # | Check | Pass condition | Verify by reading code |
|---|---|---|---|
| F1 [critical] | Screen states | Loading, empty, error exist for every data view; offline and limit where relevant; paged lists also have loading more, end of list and error with retry | Read the render branches |
| F2 [critical] | Button states | Default, hover, pressed, disabled, loading | Read the button component |
| F3 | Input states | Default, focus, error, warning, disabled | Read the input component |
| F4 | Silent actions confirmed | Copy, save, send show a confirmation in place | Handlers trigger a chip or toast |
| F5 | Errors specific | Cause, next step, and a support path for money or account | Read error mappings and views |
| F6 | Limit states factual | Count, plain headline, exact reset date | Read the strings |
| F7 | Effort never yields nothing | Every "not enough" branch gives something back and a next step | Read those branches |
| F8 | Undo | Destructive actions have undo or a named confirm | Read destructive handlers |
| F9 | Broken on purpose | Network off, payment failed, empty lists, long text, missing image each render a designed state | Walk each case through the code |
| F10 | First run | New account sees a designed empty state pointing at the main action | Zero data branch of home |
| F11 | Nothing lost in a rewrite | Replaced or removed code (a dependency, an old component) left behind every accessible name, focus rule and state branch it had | `grep -nE -e 'aria-' -e 'role=' -e 'disabled' -e 'error' -e 'empty' -e 'loading' -e 'focus' old-file`; each hit exists in the new code |
| F12 | Logic has one check | New branching logic, parsers, formatters, price or date maths have one test or assert | Find the test beside each one |

## 8. G. Copy

| # | Check | Pass condition | Verify by reading code |
|---|---|---|---|
| G1 | Labels earn their place | No label the format explains ("Price:" before "$6.20") | Read label strings |
| G2 | Consistent labelling | Sibling controls all labelled or none | Read sibling labels |
| G3 | Facts, not slogans | No exclamation slogans in system states | `grep -n '!"'` in state copy |
| G4 | Shortest badge | Badges are 1 to 3 words ("20% off") | Read badge strings |
| G5 | Action labels | Verb plus object, sentence case | Read button strings |
| G6 | Title describes the thing only | No variable attribute in a title | Read title bindings |
| G7 | No em or en dashes, no emoji | Zero in UI strings | `grep -nP '[\x{2013}\x{2014}]'` and the emoji check in section 15 |
| G8 | Plain words | No jargon the user did not bring | Read strings aloud |

## 9. H. Consistency across screens

| # | Check | Pass condition | Verify by reading code |
|---|---|---|---|
| H1 [critical] | Shared chrome from one source | Nav, header, tab bar come from one component | Every route imports the same component; no local copies |
| H2 | Screen 80 vs screen 1 | Same spacing, fonts, buttons and wording on the newest and the oldest screen | Diff the token usage of the newest screen against an old one |
| H3 | One situation, one pattern | Same state uses the same component everywhere | Search for duplicate empty, limit, error components |
| H4 | One home per metric | Each KPI rendered on one route | `grep` KPI component usage |
| H5 | Same term for the same thing | One word per concept across the product | `grep` synonyms (Delete/Remove, Workspace/Project) |
| H6 | Icon family | One icon set, one stroke weight, one style | Read icon imports; one library |

## 10. I. Accessibility

| # | Check | Pass condition | Verify by reading code |
|---|---|---|---|
| I1 [critical] | Text contrast | Body 4.5:1, large text 3:1 (WCAG AA) | `python3 ${CLAUDE_SKILL_DIR}/scripts/contrast_check.py <bg> <fg>` for every text colour on its real background, including translucent text |
| I2 | UI part contrast | Borders of inputs, icons, focus rings 3:1 | Same script |
| I3 [critical] | Focus visible | Every interactive element has a visible focus style | `grep` for `outline: none`/`outline-none` without replacement |
| I4 | Target size | 44 x 44 px minimum on touch, 24 x 24 px minimum on desktop | Read control sizes plus padding |
| I5 | Names | Icon only controls have accessible names; images have alt text | Search for missing labels |
| I6 | Not colour alone | Status, errors and chart series also use icon, text or pattern | Read status components |
| I7 | Reduced motion | Animations respect the reduced motion setting | Find the media query or platform flag |
| I8 | Keyboard | Every action reachable by keyboard; modals trap and return focus; Escape closes | Read key handlers and focus management |
| I9 | Scaling | Layout survives 200% text or the platform's large text setting | Sizes come from scalable tokens; no fixed heights on text containers |
| I10 | Current page and required fields marked | The current nav item has `aria-current="page"` plus a visible non colour style; required inputs have `required` or `aria-required` and the form states its convention once | grep `aria-current` in the nav component and `required` on the form inputs |
| I11 | Language before sign in | A product with more than one language offers the switch on the first signed out screen (preselected from the device locale) and in settings; the choice is stored before an account exists | List the screens with a language control; the first signed out screen is one (`patterns/onboarding.md`) |

## 11. J. Premium details

| # | Check | Pass condition | Verify by reading code |
|---|---|---|---|
| J1 | Shadows quiet | Low opacity, large blur; stronger only for overlays | Read shadow tokens; card shadow weaker than popover shadow |
| J2 | Dividers subtle | Thin, light, or none | Read divider tokens |
| J3 | Overlays readable on any image | Icons in containers, text on a gradient | Read hero overlay styles |
| J4 | Images as a system | One aspect ratio, background and framing per catalog | Read the image component |
| J5 | Motion purposeful | Transitions under about 300 ms for UI, eased, interruptible | Read durations and easings |
| J6 | Micro interaction where the result is invisible | Copy, save, send have a small confirming animation | Read handlers |
| J7 | No AI slop | None of the tells in `ai-slop-tells.md` | Run its detection column |
| J8 | Commodity test | The screen shows evidence of care an AI default would not: states, recovery, real data | Name three such details in the report |
| J9 | Rich and not poorer than the references | Each main screen shows at least the facts and actions the step 2 references show on the same screen | Per main screen list, per item: key figure, status chip, derived value, the one strong signal per card; then facts and actions here vs the references; fewer needs a written reason |

## 12. K. Honesty

| # | Check | Pass condition | Verify by reading code |
|---|---|---|---|
| K1 [critical] | No dark patterns | No confirmshaming, fake urgency, fake scarcity, hidden costs, roach motel, nagging, preselected consent or add ons | Run the checks in the ETHICS section of `psychology/psychology.md` |
| K2 | Claims are data | Counts, ratings, stock, deadlines, struck prices come from real data | Trace each to its source |
| K3 | Numbers agree and explain themselves | Shown parts add up to the shown total at the same precision; the same figure has the same value and format everywhere; count words use plural rules; a caveat sits in the result card under the figure, before any CTA | One test asserts sum(displayed parts) == displayed total; grep count strings for a plural helper; read the result card DOM order (`visual/data-visualization.md` section 8) |

## 13. L. Daily use

Run the brief's day in the life (`patterns/daily-use.md`) against the build.

| # | Check | Pass condition | Verify by reading code |
|---|---|---|---|
| L1 [critical] | Daily questions answered | Each daily question from the brief has a visible answer on the first screen, with money beside time where money exists | Map each question to the element and file that answers it |
| L2 [critical] | Period views navigate | Every day, week or month view has previous, next, a reset to the current period, a period label and a total row | Read the period header and the table footer (`patterns/data-dense-tools.md` sections 1 and 2) |
| L3 | Forms prefilled | Create and daily forms open with the last used choice and the most likely values; an empty field with an example placeholder fails | Count fields and clicks for the 3 repeated tasks; list each input's initial value |
| L4 | Power input shown | Every accepted shortcut format is named in the hint and the parsed value is echoed | Read the hint text and the echo element per lenient field |
| L5 | Stale state warned | A timer over 10 h, an unsaved draft or a stale sync shows a plain warning with the start time and a fix action | Read the branches for each stale condition |
| L6 | Housekeeping exists | Delete with confirm, export and sign out exist where data or admin screens exist | Find each handler and the control that reaches it |

## 14. Report format

```
Quality gate: <screen or component>
Design source: <user named look | project design system | default>
Size of job: <tiny | screen | product>
Scope: <files>, states checked: <list>
A Intuitiveness   13/13 (A6 fixed: row actions moved to menu, Row.tsx:41)
B Hierarchy        7/7
...
L Daily use        6/6
Critical items: all pass (one line of evidence each)
L Daily use: <questions and moves, each answered where>
J9: <screen: facts/actions here vs reference>
Numbers checked: <element: content width vs space, icon/container ratio, fill vs surface hex>
Mistakes library: <each entry id: applies or N/A, how avoided> (local library and quality/mistakes-library.md)
Ship: no [critical] row fails and no open FAIL
Three details an AI default would not have: <1>, <2>, <3>
Not checked and why: <list, or "none">
Only your eyes can confirm: <list>
```

## 15. Fast code checks (copy and run)

Run from the project root, adjust the source folder. Each hit is a lead to inspect, not an automatic fail.

```bash
SRC=src
# emoji and symbol characters used as icons: arrows, media and technical symbols,
# geometric shapes, dingbats, stars, emoji planes, emoji variation selector
grep -rnP '[\x{2190}-\x{21FF}\x{2300}-\x{23FF}\x{25A0}-\x{25FF}\x{2600}-\x{27BF}\x{2B00}-\x{2BFF}\x{1F000}-\x{1FAFF}\x{FE0F}]' "$SRC"
# em and en dashes in strings
grep -rnP '[\x{2013}\x{2014}]' "$SRC"
# sizes that bypass the scale (C12): each hit is 0, 1, or a listed exception
grep -rnE '(implicitHeight|implicitWidth|preferredWidth|preferredHeight|radius|margins?|spacing): *[0-9]+' "$SRC"
# literal font sizes outside the token file
grep -rnE 'font-?size: *[0-9]+|fontSize: *[0-9]+|text-\[[0-9]+px\]|pixelSize: *[0-9]+' "$SRC"
# gradient text and gradient buttons
grep -rnE 'bg-clip-text|background-clip: *text|text-transparent|linear-gradient' "$SRC"
# common AI default palette hexes
grep -rniE '#(667eea|764ba2|7c3aed|6366f1|8b5cf6|a855f7|0f172a|1e293b|020617)\b' "$SRC"
# focus outlines removed
grep -rnE 'outline: *none|outline-none' "$SRC"
# letter avatars
grep -rnE 'charAt\(0\)|\[0\]\.toUpperCase\(\)|slice\(0, *1\)' "$SRC"
# placeholder copy and slogans shown to users (a TODO inside a code comment is a lead, not copy)
grep -rnE 'Lorem|TODO|Coming soon|!\"' "$SRC"
# user or server text written as HTML (injection hole); use textContent or the framework
grep -rnE 'innerHTML *=|dangerouslySetInnerHTML|v-html' "$SRC"
# native confirm or alert where the app has a house dialog
grep -rnE 'window\.(confirm|alert)\(|(^|[^.[:alnum:]_])(confirm|alert)\(' "$SRC"
# deferral markers, then the ones with no upgrade trigger (no comma after the limit)
grep -rnE '(//|#|/\*|<!--) ?(kwx-defer|shortcut):' "$SRC" | grep -viE 'shortcut:.*(key|ctrl|cmd|alt\+)'
grep -rnE '(//|#|/\*|<!--) ?(kwx-defer|shortcut):' "$SRC" | grep -viE 'shortcut:.*(key|ctrl|cmd|alt\+)' | grep -vE '(kwx-defer|shortcut):[^,]+,'
# identifiers broken mid word (allowed only on the one free text column)
grep -rnE 'overflow-wrap: *anywhere|break-all' "$SRC"
# red buttons: each hit must name a destructive action (never Stop or Close)
grep -rnE 'variant=\{?"danger|btn-danger|bg-danger' "$SRC"
# placeholders that look like values or say Optional
grep -rnE 'placeholder="Optional"|placeholder="[0-9]{1,2}[:.][0-9]{2}"' "$SRC"
# ellipsis: each hit must be bound to user data, never to a label the product writes
grep -rnE 'truncate|text-ellipsis|ellipsizeMode|numberOfLines=\{1\}|elide: *Text\.Elide(Right|Left|Middle)' "$SRC"
# watermarks and generator credits (none allowed)
grep -rniE 'generated (with|by)|made with claude|name="generator"' "$SRC"
```

Pointed at a project root instead of a source folder, add `--exclude-dir={.git,node_modules,dist,build}` to each `grep -r`, or vendored code floods the output. End the marker harvest with a count line: `<N> markers, <M> with no trigger`. A marker in a comment is allowed when it names its trigger; placeholder text shown to users always fails.

For hand drawn SVG icons run `python3 ${CLAUDE_SKILL_DIR}/scripts/icon_check.py <icon.svg>`.
