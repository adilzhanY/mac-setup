# Scoring rubric

Score every finished piece of UI from 0 to 5 on each dimension below, after running the quality gate. The score is a judgement backed by evidence: for each dimension write one line saying why it earned that level.

## Contents

1. Minimum to ship
2. Dimensions and levels
3. How to score
4. Example

---

## 1. Minimum to ship

- **Hard fails** (ship is blocked whatever the scores): any dark pattern; any [critical] item of the quality gate open; text contrast below WCAG AA; a data view with no loading, empty or error state.
- **Intuitiveness, States and recovery, Honesty**: at least 4 each.
- **Every other dimension**: at least 3.
- **Average**: at least 4.0.

A 3 is "acceptable, nothing wrong a user would notice". A 4 is "a good product team would ship this". A 5 is "a reference app would be proud of it".

## 2. Dimensions and levels

### Intuitiveness

| Level | Looks like |
|---|---|
| 0 | The user cannot tell what the screen is for or what to do |
| 1 | Primary action unclear; controls look the same whether clickable or not |
| 2 | One primary action exists but competes; selected, inactive, hover states missing |
| 3 | One clear next step; conventions kept; signifiers for grouped, selected, inactive |
| 4 | Smart defaults, inputs beside their actions, consequence in the CTA, rare actions disclosed progressively, tooltips on icons |
| 5 | The task itself is easier than in the reference app: presets from real data, sticky actions, zero needless decisions |

### Hierarchy

| Level | Looks like |
|---|---|
| 0 | Everything the same size and weight (a spreadsheet card) |
| 1 | Several elements shout; the eye has no start |
| 2 | Clear title, but badges, CTAs and labels compete |
| 3 | Blur order matches importance; one primary |
| 4 | Secondary info grouped and muted; labels replaced by structure where obvious; the key value has its own colour and place |
| 5 | Calm and instantly scannable; nothing could be removed without losing meaning |

### Spacing and alignment

| Level | Looks like |
|---|---|
| 0 | Random gaps and edges |
| 1 | Visible misalignment (a 17 px offset between blocks) |
| 2 | One margin, but gaps irregular and groups unclear |
| 3 | 4 pt scale, one margin, groups closer inside than between |
| 4 | Rhythm consistent across the screen; no nested cards; icons sized to line height |
| 5 | Every value traceable to a token with a reason; feels inevitable |

### Typography

| Level | Looks like |
|---|---|
| 0 | Several families, tiny or huge text, unreadable body |
| 1 | Two or more families or too many sizes |
| 2 | One family, but untuned (loose headlines, tight body, ALL CAPS buttons) |
| 3 | One family, capped scale, readable body (about 1.5 line height) |
| 4 | Tuned display text (-2% to -3% tracking, 110% to 120% line height), tracked small caps, platform base size on mobile |
| 5 | Type alone carries the hierarchy; matches a reference app at the same zoom |

### Colour

| Level | Looks like |
|---|---|
| 0 | Neon, clashing, AI default palette |
| 1 | Decorative colour everywhere, gradient text or buttons |
| 2 | Calmer, but several accent fills and coloured borders without meaning |
| 3 | One brand colour with a ramp, semantic colours only for meaning, one accent fill per view |
| 4 | Colour carried by data; neutrals tinted toward the brand; dark mode depth by lightness |
| 5 | Blur test leaves only signals; palette is distinct and owned |

### States and recovery

| Level | Looks like |
|---|---|
| 0 | Happy case only |
| 1 | Some loading spinners; errors generic or missing |
| 2 | Loading, empty, error exist but are generic |
| 3 | Every data view has designed loading, empty and error; buttons and inputs have all states |
| 4 | Errors give cause, next step and support path; silent actions confirmed; undo for destructive actions; limits as facts with dates |
| 5 | Failure is a "they caught me" moment: reason specific messages, offline handled, effort never answered with nothing |

### Copy

| Level | Looks like |
|---|---|
| 0 | Placeholder or lorem text |
| 1 | Slogans, jargon, generic "Submit" |
| 2 | Clear but wordy; redundant labels |
| 3 | Verb plus object actions, no redundant labels, sentence case |
| 4 | Facts not slogans, shortest badges, consequences in buttons, consistent terms |
| 5 | Every string earns its place; reads like one careful voice |

### Consistency across screens

| Level | Looks like |
|---|---|
| 0 | Every screen styled on its own |
| 1 | Shared chrome moves or changes between screens |
| 2 | Shared nav, but components and wording drift |
| 3 | Shared components for chrome and controls |
| 4 | One pattern per situation; one home per metric; one term per concept |
| 5 | Screen 80 is indistinguishable in system from screen 1 |

### Accessibility

| Level | Looks like |
|---|---|
| 0 | Fails contrast, no focus, tiny targets |
| 1 | Some contrast fails, focus removed |
| 2 | Contrast passes, but focus, names or targets missing |
| 3 | WCAG AA contrast, visible focus, 44 px touch targets, names on icon controls |
| 4 | Not colour alone, reduced motion, full keyboard path, text scaling survives |
| 5 | Tested with a screen reader path and large text; nothing lost |

### Premium details

| Level | Looks like |
|---|---|
| 0 | AI slop tells throughout (emoji icons, gradients, repeated KPIs) |
| 1 | Several tells left |
| 2 | Tells removed, but heavy shadows, thick dividers, unreadable overlays |
| 3 | Quiet shadows and dividers, overlays readable, one icon set |
| 4 | Micro interactions where results are invisible; image system; purposeful motion |
| 5 | Three or more details an AI default would never produce, all rooted in this product |

### Honesty

| Level | Looks like |
|---|---|
| 0 | Dark patterns present (hard fail) |
| 2 | No dark patterns, but claims not traceable to data |
| 4 | Every claim from data; neutral dismissals; costs visible before commit |
| 5 | The user would thank you for every persuasive element if they understood it |

## 3. How to score

1. Run `quality-gate.md` first. Its FAILs cap the related dimension at 2.
2. Score each dimension, with one line of evidence.
3. Check the minimums in section 1.
4. If below the minimum, fix the lowest dimension first, then rescore.
5. Report the table with the gate report.

## 4. Example

```
Settings > Usage tab
Intuitiveness 4  one Upgrade action, rows explain themselves
Hierarchy     4  heading, helper, rows; value right aligned
Spacing       4  16/32 rhythm, hairline rows, no nested cards
Typography    4  one family, 14/16/20, tabular numbers
Colour        4  green only on the full ring and the one CTA
States        3  loading and error done; limit state lacks reset date -> fix
Copy          4  factual helper "Upgrade for higher limits and more features"
Consistency   4  same tabs component as Billing
Accessibility 3  contrast AA; donuts need text values for screen readers -> fix
Premium       3  quiet, but no detail beyond the floor yet
Honesty       5  usage from API, no nagging
Average 3.8 -> below 4.0, fix States and Accessibility, rescore.
```
