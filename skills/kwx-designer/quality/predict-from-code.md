# Predict from code

You never see the screen. This file is the method for working out, from the code alone, whether text fits, whether content fits its shape, whether an icon is the right size and whether a control can be seen. It owns the review arithmetic: no other file in this skill states different factors (`quality/enforcement.md` section 5).

## Contents

1. You never see the screen
2. Get the scale
3. Text vs box, horizontal
4. Text vs box, vertical
5. Content inside a shape
6. Icon vs container
7. Colour vs what is behind it
8. Room tests
9. Phone width
10. Every state
11. Every mistakes library entry
12. Write the numbers

---

## 1. You never see the screen

- No screenshots, no windows opened on the user's screens, no mouse moves, no typing, no focus changes. Predict the render from the code instead.
- Use a screenshot only when the user gives one.
- The report ends with `Only your eyes can confirm: <list>`: what the arithmetic cannot settle (optical balance, a colour's feel, motion timing).

## 2. Get the scale

Find the multiplier between the numbers in the code and the pixels on screen before any other arithmetic.

| Stack | Where the scale lives |
|---|---|
| QML (the user's shell) | `scale` in `~/.config/quickshell/ii/modules/common/UiScale.qml` (1.1 now); px(n) = round(n x scale); font tokens times scale |
| Web | the root font size (rem), any `--scale` variable, the browser zoom the user runs |
| React Native | `PixelRatio.getFontScale()` for text; layout in dp |
| Desktop OS | the display scale (125%, 150%) on top of the app's own scale |

Convert every number to real px before comparing. Example: `UiScale.px(56)` at 1.1 is 62 px; `pixelSize.small` (16) at 1.1 is 17.6 px.

## 3. Text vs box, horizontal

**Width of a string** = characters x font px x factor:

| Text | Factor |
|---|---|
| Regular weight | 0.6 |
| Semibold and bold | 0.65 |
| ALL CAPS | 0.7 |
| CJK | 1.0 |

Digits, spaces and % count as characters.

**Available width** = container width minus its padding minus every sibling in the row (icon, switch, chevron, key hint chip) minus the gaps between them.

**Longest realistic string**: German runs about 30% longer than English; take "100%" not "50%"; take a 40 character name, not "Anna".

Add 15% margin to the string width. If it does not fit, the remedy order is:

1. Give the box room (smaller side elements, less padding, a wider column).
2. Let it wrap (wrap on, elide off).
3. Shorter words.

Never shrink the text and never go below the smallest token. Elide only user data, with the full value in a tooltip.

Siblings of a label that may wrap never wrap: web `white-space: nowrap; flex-shrink: 0`; React Native `flexShrink: 0`; QML `Layout.fillWidth` on the label only, fixed size on the siblings.

## 4. Text vs box, vertical

Height needed = lines x line height + vertical padding + the bottom safe area where it applies. It must fit the bar, row or card that holds it.

Tab bars: icon + label line height x the largest allowed font scale + padding + `insets.bottom`. A library default height after you replaced the label with a larger one is a defect.

## 5. Content inside a shape

A number in a ring, a glyph in a disc, a badge on an icon.

- Inner free space = diameter minus 2 x stroke minus padding.
- The widest content (section 3) plus 15% each side must fit inside it.
- If not, the shape grows. The text never shrinks (KM1).

## 6. Icon vs container

- Icon / disc 0.40 to 0.55 of the diameter (KM2).
- An icon next to text equals the text's line height.
- Read what the house component picks by default (IrisDisc picks its icon size by its own size; a big disc keeps a small default). Set it explicitly through the scale on big discs.

## 7. Colour vs what is behind it

- Walk up the tree to the real surface behind the element, not the one in the mockup.
- Text: at least 4.5:1, checked with `python3 scripts/contrast_check.py <bg> <fg>`.
- A filled control: per channel difference over 10 against its surface, checked with `python3 scripts/contrast_check.py --surface <bg> <fill>`. VANISHES means use the variant made for that surface (KM4).

## 8. Room tests

Compare widths in content units: `screen.width / scale` in QML, em breakpoints or container queries on the web, width / fontScale in React Native. A 1920 px screen at 1.25 lays out like 1536 px (KM6).

## 9. Phone width

- At 360 and 390 px, anything wider than 358 px with a `min-width`, a fixed width or `nowrap` must sit in an `overflow-x` box of its own.
- Flex and grid children get `min-width: 0`, or a long word pushes the page wide.
- Tables become cards per row below 640 px.

## 10. Every state

Run the arithmetic for each: empty, one item, many items, long names, busy, failed, disabled, offline. The longest string usually lives in the failed or long name state.

## 11. Every mistakes library entry

Go through the local library, then `quality/mistakes-library.md`, one line per entry: applies or N/A, and how the code avoids it.

## 12. Write the numbers

Write the arithmetic for every risky element into the report, so a reader can check it. Worked example:

```
"100%" at 17.6 px DemiBold = 4 x 17.6 x 0.65 = 46 px
ring 84 - 2 x 5 stroke - 8 padding = 66 px inner
margin (66 - 46) / 2 = 10 px each side, over 15% of 46 (7 px): pass
```

Fix in code, then redo the arithmetic on the fixed numbers.
