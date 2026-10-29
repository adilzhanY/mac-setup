# Hierarchy and Gestalt

An intuitive interface answers three questions within a second: what is this, what matters most, what do I do next. Hierarchy is how you answer them without words.

## Contents

1. The one-primary rule
2. Tools of hierarchy, ranked
3. Limits that keep hierarchy readable
4. Gestalt principles as rules
5. Scanning patterns
6. Action hierarchy
7. Tests

## 1. The one-primary rule

- Each view has exactly one primary focal point and one primary action. Name both before designing. If you cannot, the screen has two jobs: split it.
- Not all elements are equal (Refactoring UI). Rank every element on the screen as primary, secondary or tertiary before choosing any size or colour.
- Visual hierarchy is separate from document hierarchy: an `h2` can look small (a section eyebrow), a `p` can look huge (a stat). Choose the HTML tag for meaning and the style for importance.

## 2. Tools of hierarchy, ranked

From strongest to subtlest. Use the subtlest tool that works.

1. **Position**: top left in LTR layouts and the centre of the first screen get seen first (NN/g: 57 percent of viewing time is above the fold, 74 percent in the first two screens).
2. **Size**: bigger is more important.
3. **Contrast** (value and saturation against the surroundings, not the hue itself): a saturated accent on a calm page wins over size.
4. **Weight**: bold vs regular.
5. **Space**: isolation draws attention; a lone element surrounded by space reads as important.
6. **Colour hue**: weakest alone, and invisible to colour-blind users.

De-emphasize to emphasize: when the primary element does not stand out, make competitors quieter (lighter text colour, smaller, less weight) instead of making the primary louder.

Size isn't everything (Refactoring UI): a label can drop size and gain weight, or keep size and lose colour. Combine at most two tools per step of hierarchy.

## 3. Limits that keep hierarchy readable

NN/g visual hierarchy guidance:

- At most 3 sizes of content text in one view (small, medium, large).
- At most 2 elements at the largest size.
- About 2 primary and 2 secondary colours in a simple design; at most 3 contrast variations.
- Labels are a last resort (Refactoring UI): `$12.99/month` needs no "Price:" label. Format the data so it explains itself, and if a label is needed, make it the quiet part.

## 4. Gestalt principles as rules

| Principle | Rule | Common failure |
|---|---|---|
| Proximity | Related things are closer together than unrelated things; inner gap at most half the outer gap. | Equal spacing everywhere; a button placed nearer the wrong group (NN/g: an Add button among Next and Cancel was not found). |
| Similarity | Things that look alike are read as the same kind. Same function, same style; different function, visibly different style. | A link styled like body text; a non-clickable tag styled like a button. |
| Common region | A shared background or border groups strongly, stronger than proximity. Use cards to bind a price, its features and its CTA. | Pricing features floating outside the card they belong to. |
| Figure and ground | The foreground must separate from the background by contrast or elevation. | A white card on an almost-white page with no border or shadow. |
| Continuity | Elements on one line or curve are read as a sequence. Align steps of a "how it works" row on one axis. | Zig-zag layouts that break the reading line for no reason. |
| Closure | People complete partial shapes. A card cut off at the viewport edge signals "scroll for more". | Full-bleed hero that ends exactly at the fold, so the page looks finished. |
| Common fate | Things that move together belong together. Animate a group as one. | Staggered animations that split a single card into unrelated parts. |
| Focal point | The one element that differs (colour, size) is noticed first. Spend it on the primary action. | Two highlighted pricing plans; a red badge competing with the CTA. |

## 5. Scanning patterns

- People scan, they do not read. Text-heavy pages are scanned in an F pattern: headings and the first words of lines get read. Front-load headings and list items with the meaningful word.
- Sparse marketing layouts are scanned in a Z pattern: logo, nav, headline, CTA. Put the CTA at the end of the Z, not in a corner nobody reaches.
- Every section headline must make sense alone; a visitor who reads only headlines should understand the product.

## 6. Action hierarchy

| Level | Style | Count per view |
|---|---|---|
| Primary | Solid accent fill, highest contrast | 1 |
| Secondary | Outline or tinted fill (step 3 or 4 background) | 1 to 2 |
| Tertiary | Text link or ghost button | any |
| Destructive | Red only when it is the primary action of a confirm step; otherwise secondary styled with red text | as needed |

- Hover, active and focus states have higher contrast than rest (Vercel).
- A specific verb beats a generic one: "Start 7-day free trial" over "Get started" (NN/g found "Get Started" misleads and stops users from reading the page).

## 7. Tests

- **Squint or blur test**: blur the screenshot by 5 to 10 px. The primary element and the groups should still be obvious. At 20 px blur, check no accidental focal point (a vivid image, a stray coloured badge) dominates. Do it with real content, not lorem ipsum.
- **Five-second test**: show the screen for 5 seconds; a person should be able to say what it is and what to do.
- **Greyscale test**: in greyscale, hierarchy must survive. If the only thing marking the primary button is hue, it fails.
- **Headline-only read**: read only the headings top to bottom. They should tell the story.
- **Count**: number of font sizes, colours and button styles on the screen. Each above the limits in section 3 needs a reason.
