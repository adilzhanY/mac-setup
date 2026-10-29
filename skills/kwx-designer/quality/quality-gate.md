# The quality gate

Run this gate before you call ANY piece of UI done: a new screen, a fix, a component, a redesign, a one line style change. It is permanent. It does not get skipped because the change is small, because the user is in a hurry, or because a screenshot "looks fine".

Most items can be checked by reading the code. Where there is no screenshot, work the real sizes out from the code (font size times text length against the box, icon size against its container, colour against the colour behind it) and predict how it renders.

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
13. Report format
14. Fast code checks (copy and run)

---

## 1. How to run the gate

1. List every screen and component the change touches, and every state of each (default, hover, focus, pressed, disabled, loading, empty, error, offline, limit, long content, no content).
2. Go through sections A to K. For each item write PASS, FAIL or N/A, with the evidence (file and line, or the computed value).
3. Fix every FAIL, then run the failed items again. Do not report done with an open FAIL.
4. Run the fast code checks in section 14.
5. Score the result with `scoring-rubric.md`. Ship only above its minimum.
6. Report in the format of section 13.

An item marked **[critical]** blocks shipping on its own.

## 2. A. Intuitiveness

| # | Check | Pass condition | Verify by reading code |
|---|---|---|---|
| A1 [critical] | One obvious next step | Each screen has exactly one primary action, and a new user could name it in 3 seconds | Count elements with the primary style per screen: exactly 1 |
| A2 [critical] | Every action answers: what happened, can I undo, what next | Each handler leads to a visible result, a way back, and an obvious next step | For each handler, find the feedback it triggers and the undo/back path |
| A3 | Signifiers without instructions | Grouped, selected, inactive and clickable are distinguishable without help text | Selected, disabled and hover styles exist and differ; inactive items are not clickable |
| A4 | Conventions kept | Back is top left, close is an X, destructive is red and last, search looks like search | Read placement of these controls |
| A5 | Data drives the form | Enums are chips, numbers right aligned, people avatars, time absolute plus relative | Read each cell or field renderer |
| A6 | Progressive disclosure ranked | Frequent actions visible; rare and destructive ones on hover or in a menu | Count visible buttons per row: 2 or fewer |
| A7 | Smart defaults | Every predictable input has an initial value; CTA enabled on first paint | Read initial state and the CTA `disabled` expression |
| A8 | Inputs next to the action they feed | Stepper beside the button, filters beside the list | Read the layout container |
| A9 | Consequence in the action | CTA label says what happens and, when known, the count or total | Read label strings and expressions |
| A10 | One screen, one job (mobile) | Focused screens (editor, settings) have no unrelated sections | Read the screen's children |
| A11 | Tooltips on icon only controls | Every icon only button has a tooltip and an accessible name | Search icon buttons without `title`/`aria-label`/Tooltip |
| A12 | Gestures have a visible alternative | Each swipe or long press action also exists as a control | Map gesture handlers to buttons or menu items |

## 3. B. Hierarchy

| # | Check | Pass condition | Verify by reading code |
|---|---|---|---|
| B1 [critical] | Squint test | Blurred, the most important thing is seen first, the second thing second | List elements with size, weight, colour; rank by visual weight; the order matches the intended order |
| B2 | No competing primaries | Title, badge and CTA do not all use the heaviest weight or brightest colour | Compare the style tokens of the top 3 elements |
| B3 | Most important near the top, larger, bolder | The key item is the largest text in its card | Read font tokens per element in the card |
| B4 | Secondary info smaller and grey, directly below | Meta lines use a smaller, muted token | Read the meta line tokens |
| B5 | The one different value has its own colour and place | Price or status is the only accent coloured value in a card | Count accent coloured texts per card: 1 |
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
| C8 | Text fits its box | Longest realistic string fits at the current scale | Font px times characters times about 0.55 (average glyph width) against the box width; truncation or wrap defined |
| C9 | Numbers aligned | Numeric columns right aligned, tabular figures | Read numeric cell styles |

## 5. D. Type

| # | Check | Pass condition | Verify by reading code |
|---|---|---|---|
| D1 [critical] | One family | One font family (a mono for code or data is allowed) | `grep` font family declarations; one source token |
| D2 | Size count | 6 or fewer sizes on a marketing page; dashboard sizes 24 px or below | Count distinct size tokens per view |
| D3 | No literal sizes | Every size comes from the type scale tokens | `grep` for literal px font sizes outside the token file |
| D4 | Large headings tightened | Letter spacing -2% to -3%, line height 110% to 120% on display text | Read heading tokens |
| D5 | Body readable | Body line height about 1.5 to 1.6; mobile body at least the platform base (17 px iOS) | Read body tokens |
| D6 | Small caps tracked | Small uppercase labels have positive letter spacing | Read label tokens |
| D7 | Sentence case | Buttons and attribute labels in sentence case, not ALL CAPS | `grep` for `uppercase` / `text-transform` on buttons and long strings in caps |
| D8 | Weights | Hierarchy by size, weight, colour, line height; no more than 3 weights | Count weight tokens |
| D9 | Floor | No text below the smallest token of the scale | Read the smallest size used |

## 6. E. Colour

| # | Check | Pass condition | Verify by reading code |
|---|---|---|---|
| E1 [critical] | Every colour has a purpose | Each colour is the brand ramp, a neutral, or a semantic colour with meaning | List every colour token used on the screen and name its meaning; unnamed ones fail |
| E2 | One accent fill per view | Only one bright filled button | Count primary variant buttons per screen |
| E3 | No AI default palette | No generic navy plus purple gradient, no neon accents; neutrals tinted toward the brand | Read the palette; hexes like `#7c3aed`, `#6366f1`, `#8b5cf6` with a navy `#0f172a`-style background without a brand reason fail |
| E4 | Desaturated | No pure neon hues (`#00ff00`, pure yellow) unless the brand demands it | Read hex values |
| E5 | Red reserved | Red only for error, danger, urgent | `grep` danger tokens; each use is one of those |
| E6 | Semantic colour never alone | Status uses icon plus word, not colour only | Read chip and status components |
| E7 | Dark mode depth | Raised surfaces lighter than the background; borders low contrast; chips dimmed with bright text | Read dark surface and border tokens |
| E8 | Colour in data, not decoration | Charts, logos, status dots carry colour; icon discs and card borders do not | Search for tinted icon backgrounds and coloured borders |
| E9 | Blur test | Blurred, only meaningful colour signals remain | Same list as E1: every saturated area is a signal |

## 7. F. States

| # | Check | Pass condition | Verify by reading code |
|---|---|---|---|
| F1 [critical] | Screen states | Loading, empty, error exist for every data view; offline and limit where relevant | Read the render branches |
| F2 [critical] | Button states | Default, hover, pressed, disabled, loading | Read the button component |
| F3 | Input states | Default, focus, error, warning, disabled | Read the input component |
| F4 | Silent actions confirmed | Copy, save, send show a confirmation in place | Handlers trigger a chip or toast |
| F5 | Errors specific | Cause, next step, and a support path for money or account | Read error mappings and views |
| F6 | Limit states factual | Count, plain headline, exact reset date | Read the strings |
| F7 | Effort never yields nothing | Every "not enough" branch gives something back and a next step | Read those branches |
| F8 | Undo | Destructive actions have undo or a named confirm | Read destructive handlers |
| F9 | Broken on purpose | Network off, payment failed, empty lists, long text, missing image each render a designed state | Walk each case through the code |
| F10 | First run | New account sees a designed empty state pointing at the main action | Zero data branch of home |

## 8. G. Copy

| # | Check | Pass condition | Verify by reading code |
|---|---|---|---|
| G1 | Labels earn their place | No label the format explains ("Price:" before "$6.20") | Read label strings |
| G2 | Consistent labelling | Sibling controls all labelled or none | Read sibling labels |
| G3 | Facts, not slogans | No exclamation slogans in system states | `grep -n '!"'` in state copy |
| G4 | Shortest badge | Badges are 1 to 3 words ("20% off") | Read badge strings |
| G5 | Action labels | Verb plus object, sentence case | Read button strings |
| G6 | Title describes the thing only | No variable attribute in a title | Read title bindings |
| G7 | No em or en dashes, no emoji | Zero in UI strings | `grep -nP '\x{2014}\|\x{2013}'` and the emoji check in section 14 |
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

## 12. K. Honesty

| # | Check | Pass condition | Verify by reading code |
|---|---|---|---|
| K1 [critical] | No dark patterns | No confirmshaming, fake urgency, fake scarcity, hidden costs, roach motel, nagging, preselected consent or add ons | Run the checks in the ETHICS section of `psychology/psychology.md` |
| K2 | Claims are data | Counts, ratings, stock, deadlines, struck prices come from real data | Trace each to its source |

## 13. Report format

```
Quality gate: <screen or component>
Scope: <files>, states checked: <list>
A Intuitiveness   12/12 (A6 fixed: row actions moved to menu, Row.tsx:41)
B Hierarchy        7/7
...
K Honesty          2/2
Critical items: all pass
Score (scoring-rubric.md): <per dimension>, ship: yes/no
Three details an AI default would not have: <1>, <2>, <3>
Not checked and why: <list, or "none">
```

## 14. Fast code checks (copy and run)

Run from the project root, adjust the source folder. Each hit is a lead to inspect, not an automatic fail.

```bash
SRC=src
# emoji in UI code (pictographs, symbols, dingbats)
grep -rnP '[\x{1F300}-\x{1FAFF}\x{2600}-\x{27BF}]' "$SRC"
# em and en dashes in strings
grep -rnP '\x{2014}|\x{2013}' "$SRC"
# literal font sizes outside the token file
grep -rnE 'font-?size: *[0-9]+|fontSize: *[0-9]+|text-\[[0-9]+px\]|pixelSize: *[0-9]+' "$SRC"
# gradient text and gradient buttons
grep -rnE 'bg-clip-text|background-clip: *text|text-transparent|linear-gradient' "$SRC"
# common AI default palette hexes
grep -rniE '#(7c3aed|6366f1|8b5cf6|a855f7|0f172a|1e293b|020617)' "$SRC"
# focus outlines removed
grep -rnE 'outline: *none|outline-none' "$SRC"
# letter avatars
grep -rnE 'charAt\(0\)|\[0\]\.toUpperCase\(\)|slice\(0, *1\)' "$SRC"
# placeholder copy and slogans
grep -rnE 'Lorem|TODO|Coming soon|!\"' "$SRC"
```

For hand drawn SVG icons run `python3 ${CLAUDE_SKILL_DIR}/scripts/icon_check.py <icon.svg>`.
