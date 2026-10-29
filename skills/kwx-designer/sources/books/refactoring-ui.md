# Refactoring UI (Adam Wathan and Steve Schoger)

- **Status:** paid (refactoringui.com, about 218 pages, by the creators of Tailwind CSS). Not read in full.
- **What was read (legal):** the full table of contents on https://www.refactoringui.com; the free preview chapter "Building your color palette" (https://www.refactoringui.com/previews/building-your-color-palette); a detailed chapter by chapter review on DEV (https://dev.to/updivision/book-review-refactoring-ui-by-adam-wathan-steve-schoger-2f7m); Steve Schoger's public tips as quoted in secondary sources. The authors' Medium article "7 practical tips for cheating at design" returned 403 and was not read.
- **Who recommends it:** the most cited visual design book in Hacker News "how do I learn UI design" threads (thread 26932020 and the 172 HN comments mentioning it); Goodreads 4.64 from about 2,200 ratings; listed in Anthony Hobday's comprehensive list of visual design books. One HN commenter warns it teaches one aesthetic (the Tailwind look), so treat it as tactics, not taste.

## Structure (table of contents)

1. Starting from Scratch: start with a feature, not a layout; detail comes later; don't design too much; choose a personality; limit your choices.
2. Hierarchy is Everything: not all elements are equal; size isn't everything; don't use grey text on coloured backgrounds; de-emphasize to emphasize; labels are a last resort; separate visual hierarchy from document hierarchy; balance weight and contrast; semantics are secondary.
3. Layout and Spacing: start with too much white space; establish a spacing and sizing system; you don't have to fill the whole screen; grids are overrated; relative sizing doesn't scale; avoid ambiguous spacing.
4. Designing Text: establish a type scale; use good fonts; keep your line length in check; baseline, not center; line-height is proportional; not every link needs a color; align with readability in mind; use letter-spacing effectively.
5. Working with Color: ditch hex for HSL; you need more colors than you think; define your shades up front; don't let lightness kill your saturation; greys don't have to be grey; accessible doesn't have to mean ugly; don't rely on color alone.
6. Creating Depth: emulate a light source; use shadows to convey elevation; shadows can have two parts; even flat designs can have depth; overlap elements to create layers.
7. Working with Images: use good photos; text needs consistent contrast; everything has an intended size; beware user-uploaded content.
8. Finishing Touches: supercharge the defaults; add color with accent borders; decorate your backgrounds; don't overlook empty states; use fewer borders; think outside the box.

## Key lessons with numbers

**Workflow.** Start from the feature (a flight search is two date pickers, two airports and a button: 80% of the work). Design early in greyscale. Define the system up front: type sizes and weights, 3 text colours (primary, secondary, tertiary), icon sizes, button sizes and padding, shadows, radii. Personality: serif classic, rounded sans playful, small radius neutral, large radius playful.

**Hierarchy.** Size isn't everything: use weight and colour. Secondary text grey on white; on colour, a tint of the background hue. One primary action, a few secondary, tertiary as links. Destructive is not primary unless it is the confirm step. Labels last: bold or formatted data can stand alone.

**Spacing.** Start with too much space. A scale from a 16px base. Small values matter more than large. Fixed widths are fine (sidebars, login cards). Labels closer to their input than to the previous one.

**Type.** Scale: 12, 14, 16, 18, 20, 24, 30, 36, 48, 60, 72px. Fonts with 5+ weights. Display faces tighter and shorter x-height, text faces wider and taller. Align mixed sizes on the baseline. Center only headlines and short text. Right align table numbers. 45 to 75 characters per line. Line height proportional: narrow and large text tighter, wide and small text looser, large text near 1. Tighten headline tracking, loosen all caps.

**Colour (preview chapter read).** Greys 8 to 10 shades; primaries 5 to 10 shades; accents at least 5, ideally 10; complex UIs may need up to ten accent hues. Nine step scales (100 to 900): pick the base 500 that works as a button background, then 900 (text) and 100 (tinted background), then 700 and 300, then the rest. Define shades up front; do not generate them with lighten/darken functions. Darkest grey is the darkest text, lightest grey a subtle off white; avoid true black. Tune saturation and lightness by eye; the book rejects formulas like "start at 50% lightness" and harmony rules like "triads". Tint greys blue (cool) or yellow/orange (warm), more saturation at the extremes. For white text on colour, shift the hue brighter instead of using washed out grey. Never colour alone: add + and - signs, shades of one hue in charts.

**Depth.** Emulate one light source. Small sharp shadows for buttons, large soft ones for modals. Shadows signal interactivity (gain shadow on drag, lose it on press). Two part shadow: large soft ambient plus small dark contact shadow. Flat depth: lighter shade raised, darker recessed, or a short unblurred vertical shadow. Overlap elements across sections.

**Images.** Text over images needs an overlay, reduced contrast or a tint. Icons have intended sizes (16 to 24px icons look chunky scaled up). Show partial or simplified screenshots instead of shrunk full ones. User uploads in fixed containers with a subtle inner shadow.

**Finishing.** Replace bullets with icons, enlarge quote marks, style checkboxes in brand colour. Accent borders on cards and alerts. Decorate backgrounds subtly. Design empty states. Use fewer borders: shadow, background difference or spacing instead.

## Used in

All files in `../../premium/`.
