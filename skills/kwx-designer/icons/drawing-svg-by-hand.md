# Drawing an icon as SVG code, by hand

How an AI agent draws an icon that holds up next to a professional set: plan it in words as named primitives with numbers, write it under a fixed root element on whole unit coordinates, then let a renderer and a pixel check do the looking. Research backs each part: LLMs lay out scenes well but "struggle with complex geometric shapes" (Chat2SVG), so primitives come first; render and compare loops beat training alone (RLRF), so every icon is rasterised and measured; reasoning before code improves SVG scores (survey, arXiv 2503.04983), so the plan is written before the markup.

Use the numbers from `construction-spec.md` (house spec: 24 canvas, 2 stroke, round caps and joins, live area 2 to 22).

## Contents

1. The method in eight steps
2. Element choice and path syntax
3. Reading the checker's output
4. Worked example 1: lock (a shared verb, drawn to spec)
5. Worked example 2: deck (a product noun, and a recognition failure)
6. Worked example 3: calendar-check (a badge with a cut gap)
7. Bonus: the filled twin of the lock
8. Common failure modes

---

## 1. The method in eight steps

1. **Name the metaphor in one sentence.** "A padlock: a rounded body with a keyhole, an arched shackle on top." If it takes more than five seconds to find a picture, the concept needs a label (NN/g); stop and say so.
2. **Find the nearest reference.** Look in the project's set, then in its base pack, for the closest existing icon (Lucide `lock`, the project's own `calendar`). Reuse its base geometry exactly where the meaning is shared: same body rect, same badge slot. Apple's own advice for custom symbols is to start from a similar symbol's template.
3. **Write the parts list as primitives with numbers**, before any markup. One line per part, giving the element, its centreline coordinates and its ink extent (centreline plus or minus 1 for the 2 unit stroke):
   `body: rect x 4..20, y 11..21, rx 2 -> ink x 3..21, y 10..22`
4. **Do the arithmetic in the plan.** For every pair of parts that come close, write the gap: **gap = distance between centrelines minus 2**. Every gap must be 2 or more. Check the ink box against the live area (2 to 22 for straight edges, 1 to 23 for round overshoot) and against the keyshape it should match. Check centring: empty space left equals right and top equals bottom, within 1.
5. **Write the fixed root, then children with geometry only.** Copy the root byte for byte:
   ```svg
   <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
   ```
   Children carry only position and size attributes (and `fill="currentColor"` plus `fill-rule` on a solid part). No `stroke`, `stroke-width`, `transform`, `style`, `class`, `id`, `opacity`, groups or `<use>`.
6. **Whole unit coordinates.** With the 2 unit stroke every line end, rect edge, circle centre, arc end and radius is a whole number. Use half units only with an odd stroke. Never more than 3 decimals, and in practice none.
7. **Render and check**: `python3 ~/.claude/skills/kwx-designer/scripts/icon_check.py icon.svg`. Read the table, read the ASCII picture row by row against your plan, then open the contact sheet PNG with the image reader. Fix and rerun until there are 0 errors and every warning is fixed or explained in one line.
8. **Check it in its family.** Rerun the script with the whole set plus the reference circle and square, open the sheet, and compare weight and size (`process-and-consistency.md` section 5).

## 2. Element choice and path syntax

| Part | Element | Example |
|---|---|---|
| Box, card, screen, body | `rect` with `rx` | `<rect x="3" y="7" width="18" height="14" rx="2"/>` |
| Round part, dot, lens | `circle` | `<circle cx="12" cy="12" r="3"/>` |
| Single straight stroke | `line` | `<line x1="12" y1="15" x2="12" y2="17"/>` |
| Bent open stroke (chevron, check, arrowhead) | `polyline` | `<polyline points="15 18 17 20 21 16"/>` |
| Closed straight-sided shape | `polygon` | `<polygon points="12 3 21 20 3 20"/>` (round joins soften it) |
| Arc, partial outline, cut outline | `path` | `<path d="M8 11V7A4 4 0 0 1 16 7V11"/>` |

Path rules:

- Use absolute commands only (`M L H V A Q Z`). Relative commands drift when one number changes.
- Arcs: `A rx ry rotation large-arc sweep x y`. With SVG's y axis pointing down, `sweep 1` goes clockwise on screen. To bulge upward from a left point to a right point, use sweep 1 (`M8 7A4 4 0 0 1 16 7`). A wrong sweep flag flips the arc, the most common hand-written path bug: check it in the ASCII picture.
- A rounded corner on a path is an arc with the corner radius: `H19A2 2 0 0 1 21 5` turns a horizontal edge down into a vertical one with radius 2.
- Prefer `A` and `Q` to `C`. If `C` is unavoidable, put each control point on the tangent line of its end point.
- Close closed shapes with `Z`, so the start is a join, not two overlapping caps.
- One element per part, one element per line in the file, in the order of the parts list. A working copy may carry `<!-- shackle -->` comments; the lint ignores them and SVGO strips them.

## 3. Reading the checker's output

```text
  size  ink x      ink y      partial  coverage  parts  holes  soft
    24   3..20      2..21       28.4%     24.6%      2      2     0
```

- `ink x`, `ink y` at 24: first and last inked pixel. They must match the ink extents in your plan. Pixel index 21 is the last pixel inside the live area; 22 means 1 unit of overshoot.
- `partial`: share of inked pixels that are anti-aliased. Straight-edged icons land near 15%, icons with arcs and diagonals 25 to 70%. Compare it before and after a change, not with an absolute target.
- `soft`: straight edges at half opacity, the signature of a line on a half unit. Must be 0 at 24 px. At 16 and 20 px it is expected (the 24 grid cannot be crisp there).
- `coverage`: ink area. Compare across the family; the reference circle is about 22%, the square 24%.
- `parts` and `holes`: separate shapes and enclosed counters. If either drops from 48 to 16 px, a gap or a counter closes when small.
- The ASCII picture uses two characters per pixel: `##` solid, `**` 67 to 99%, `++` 33 to 66%, `--` under 33%, `. ` empty. Column and row headers are pixel indices, so pixel x maps to geometry x: a 2 unit vertical line at x 12 shows as `####` in columns 11 and 12. Read it as a picture first (is it a padlock?), then as a grid (are the gaps 2 columns of `. `?).

## 4. Worked example 1: lock (a shared verb, drawn to spec)

**Metaphor.** A padlock: rounded body, keyhole, arched shackle. Convention, so keep the familiar picture and only tune it to the spec.

**Parts list.**

```text
body:    rect x 4..20 (w 16), y 11..21 (h 10), rx 2   -> ink x 3..21, y 10..22
shackle: path up from (8,11) to (8,7), arc r 4 over the top to (16,7), down to (16,11)
         arc top at y 3 -> ink top y 2; ink x 7..17
keyhole: line x 12, y 15..17                            -> ink x 11..13, y 14..18
```

**Arithmetic.** Ink box x 3..21, y 2..22: inside the live area, width 18 (portrait keyshape is 16 by 20, a padlock is wider, fine). Centred: x 3 and 21 sit 3 from each edge; y 2 and 22 sit 2 from each edge. Keyhole to body inner edge: centreline 15 against 11 is 4, gap 2; 17 against 21 is 4, gap 2. Shackle legs end on the body's top edge (y 11), a join, not a crossing.

**Code** (`examples/lock.svg`):

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <rect x="4" y="11" width="16" height="10" rx="2"/>
  <path d="M8 11V7A4 4 0 0 1 16 7V11"/>
  <line x1="12" y1="15" x2="12" y2="17"/>
</svg>
```

**Check.** 0 errors, 0 warnings. Pixels x 3..20, y 2..21 (the plan's 3..21 and 2..22 as pixel indices), `soft` 0, 2 parts and 2 holes at every size. The ASCII at 24 px:

```text
    0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3
  2 . . . . . . . . . --********--. . . . . . . . .
  3 . . . . . . . . ++############++. . . . . . . .
  4 . . . . . . . --##**++--. ++**##--. . . . . . .
  5 . . . . . . . **##--. . . . ++##**. . . . . . .
  7 . . . . . . . ####. . . . . . ####. . . . . . .
 10 . . . --++**##########################++--. . .
 11 . . . **################################++. . .
 13 . . . ####. . . . . . . . . . . . . . ####. . .
 15 . . . ####. . . . . . ####. . . . . . ####. . .
 20 . . . **################################++. . .
 21 . . . --****##########################++--. . .
```

(rows trimmed). The straight edges are solid `####`; only the arc and the rounded corners are partial, as they should be.

## 5. Worked example 2: deck (a product noun, and a recognition failure)

**Concept.** A flashcard app's own object: a deck of cards. No pack has it, so it is drawn custom on the same grid.

**First attempt, rejected.** A front card `rect x 3 y 8 w 14 h 13` with a back card shown as an L in the top right (`M7 4H19A2 2 0 0 1 21 6V15`) and a text line on the front. Two faults:

1. The checker's ink box was y 3..21 against x 2..21: 3 empty rows on top, 2 at the bottom, so it sat 1 pixel low. Moving the front card to y 7 and the L to y 3 fixed the centring.
2. Fixed and rendered, the contact sheet showed what the plan did not: **the icon is the standard "copy" picture** (two offset rectangles) with a dash in it. A user would read "duplicate". A noun that looks like a known verb is worse than a new picture, because it misleads (never use a familiar shape in an unfamiliar way: Adobe).

**Second attempt: a stack seen from the front.** Card edges peeking above one front card, so it reads as "many cards", not "two copies".

```text
front card: rect x 3..21 (w 18), y 11..21 (h 10), rx 2  -> ink x 2..22, y 10..22
second card edge: line y 7, x 5..19                     -> ink y 6..8,  x 4..20
third card edge:  line y 3, x 7..17                     -> ink y 2..4,  x 6..18
text on front: line y 16, x 8..16                       -> ink y 15..17
```

**Arithmetic.** Gaps: third edge to second, centrelines 3 and 7, gap 2. Second to front top, 7 and 11, gap 2. Text to front top inner edge, 16 and 11, gap 3; to bottom, 21 and 16, gap 3. Each edge is 2 units shorter on each side than the one below it, so the stack recedes without perspective. Ink box x 2..22, y 2..22: centred, uses the square keyshape's full size.

**Code** (`examples/deck.svg`):

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <rect x="3" y="11" width="18" height="10" rx="2"/>
  <line x1="5" y1="7" x2="19" y2="7"/>
  <line x1="7" y1="3" x2="17" y2="3"/>
  <line x1="8" y1="16" x2="16" y2="16"/>
</svg>
```

**Check.** 0 errors, 0 warnings, pixels 2..21 both ways, `partial` 16.7% (almost all straight edges), `soft` 0, 4 parts and 1 hole at every size. It still needs a recognition check with real users or at least a fresh agent shown the icon alone (`process-and-consistency.md` section 5), because "stack of cards" can also read as "inbox tray" or "layers".

## 6. Worked example 3: calendar-check (a badge with a cut gap)

**Concept.** "Day done" in a habit tracker: a calendar with a check badge. Verb plus noun: the calendar and the check are conventions; the combination is the product's.

**Parts list.**

```text
frame:  path, an open outline: starts on the right edge at (21,12), up to the top right corner,
        across the top, down the left side, along the bottom, ends at (11,21).
        Corners r 2. The bottom right is left open for the badge.
header: line y 10, x 3..21
rings:  lines x 8 and x 16, y 3..7 (cross the top edge at y 5, as in Lucide's calendar)
check:  polyline (15,18) -> (17,20) -> (21,16): both segments 45 degrees (dx = dy = 2, then 4)
```

**Arithmetic.** Check ink spans x 14..22, y 15..21. Frame right end at (21,12): its cap ink reaches y 13, the check's top end at (21,16) starts at y 15, gap 2. Frame bottom end at (11,21): cap ink reaches x 12, the check's left end at (15,18) starts at x 14, gap 2 (the first draft ended at x 12 and gave a gap of 1). Ink box 2..22 both ways.

**Code** (`examples/calendar-check.svg`):

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M21 12V7A2 2 0 0 0 19 5H5A2 2 0 0 0 3 7V19A2 2 0 0 0 5 21H11"/>
  <line x1="3" y1="10" x2="21" y2="10"/>
  <line x1="8" y1="3" x2="8" y2="7"/>
  <line x1="16" y1="3" x2="16" y2="7"/>
  <polyline points="15 18 17 20 21 16"/>
</svg>
```

**Check.** 0 errors, 0 warnings, pixels 2..21, `soft` 0, `partial` 28.6% (the diagonals and corners), parts stable from 48 to 16 px. The ASCII shows rows 13 and 14 empty between the frame end and the check, the 2 unit cut.

## 7. Bonus: the filled twin of the lock

The selected state keeps the silhouette and fills the body. The keyhole becomes a hole in the body path with `fill-rule="evenodd"`. The stroke also traces the hole and eats 1 unit on each side, so the hole is drawn 4 by 6 to show 2 by 4 (`examples/lock-filled.svg`):

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M6 11H18A2 2 0 0 1 20 13V19A2 2 0 0 1 18 21H6A2 2 0 0 1 4 19V13A2 2 0 0 1 6 11ZM10 13V19H14V13Z" fill="currentColor" fill-rule="evenodd"/>
  <path d="M8 11V7A4 4 0 0 1 16 7V11"/>
</svg>
```

The first draft drew the hole at the visible size (`M11 14V18H13V14Z`). It passed the lint but the ASCII showed rows 12 to 19 solid from column 3 to 20: the keyhole was gone. The ink box matches the outline lock exactly (x 3..20, y 2..21), which is the proof that the silhouette did not change.

## 8. Common failure modes

| Symptom | Cause | Fix | Caught by |
|---|---|---|---|
| Icon renders as a black blob | Root lacks `fill="none"`, so every shape fills | Use the fixed root byte for byte | lint (root fill) |
| Straight edge looks grey and fuzzy | Coordinate on a half unit with an even stroke, or a converted path with long decimals | Move to whole units | lint grid warning, `soft` above 0 |
| Ink touches or crosses the canvas edge | Plan used ink extents as centrelines (forgot the 1 unit half stroke) | Pull geometry in to 3..21 | ERROR in ink box |
| One icon looks thicker than the rest | A child sets `stroke-width`, or a `transform="scale()"` scales the stroke | Geometry only on children, no transforms | lint |
| Icon sits 1 pixel off centre | Uneven empty rows or columns | Shift the whole drawing by 1 unit | ink box (compare margins) |
| Arc bulges the wrong way | Sweep flag inverted | Flip the `sweep` flag (0 and 1) | ASCII picture |
| Parts merge at 16 px | Gap under 2 units, or exactly 2 next to a diagonal | Widen to 2+, shorten the diagonal | `parts` or `holes` drop warning |
| Knock-out vanishes in the filled twin | Hole drawn at the visible size; the stroke fills it | Draw the hole 2 units larger in each direction | ASCII, `holes` |
| Icon looks small next to its family | Fills less of its keyshape than the others | Size it to the matching keyshape | contact sheet, `coverage` |
| Icon looks dark and busy | Too many parts, gaps at the minimum everywhere | Remove detail until it still reads | `coverage` high, element count warning |
| Users read the wrong meaning | Picture matches a known icon with another meaning (deck v1 read as copy) | Change the silhouette, not the details | contact sheet next to the base pack, recognition test |
| Check mark looks lumpy | Segments not at 45 degrees (dx not equal to dy) | Use equal whole number dx and dy | `soft`, ASCII |
| Closed shape has a notch at the start point | Path not closed with `Z`, two caps overlap | End closed shapes with `Z` | ASCII picture, the 48 px tile on the contact sheet |
| Theme colour does not apply | Hard-coded `#000` or `fill="black"` on a child | `currentColor` on the root only | lint |
| Emoji or a Unicode symbol used as an icon | Shortcut | Draw it; never ship emoji as UI icons | review |
