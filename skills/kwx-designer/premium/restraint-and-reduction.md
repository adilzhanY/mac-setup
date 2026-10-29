# Restraint and reduction

Premium products say less, use fewer things, and make each thing count. This file turns that into rules you can check.

## Contents

1. The principle in the masters' words
2. Simplicity is not minimalism
3. Hard limits (numbers)
4. Where to spend novelty: the 90/10 rule
5. How to cut: a reduction procedure
6. Restraint in colour
7. Restraint in type
8. Restraint in motion and effects
9. Restraint in features and words
10. When restraint goes wrong
11. Sources

---

## 1. The principle in the masters' words

- **Dieter Rams, principle 10:** "Good design is as little design as possible. Less, but better, because it concentrates on the essential aspects, and the products are not burdened with non-essentials."
- **Rams, principle 5:** good design is unobtrusive. Products are tools, "neither decorative objects nor works of art". Design should be "neutral and restrained, to leave room for the user's self-expression".
- **Massimo Vignelli:** "In a world where everybody screams, silence is noticeable. White space provides the silence." And: "We love complexities but hate complications."
- **Vignelli on economy:** "Economy doesn't mean cheap design. Economy in design is the most appropriate and lean solution to every problem." And: "Good design doesn't cost more than bad design."
- **Jesper Kouthoofd (Teenage Engineering):** "I stick to rules and try to understand them, because then I can become free again." TE limits itself to simple geometric shapes, a 40 colour RAL palette and fixed colour meanings (orange or red always means record).
- **Frank Chimero:** "usually value and delight are created by taking things away and reducing friction."
- **Butterick, maxims of page layout:** "Keep it simple." "Make adjustments with the smallest visible increments." "Don't fear white space."
- **Apple, WWDC26:** "Design through subtraction." Every feature costs the user time, attention and trust.

## 2. Simplicity is not minimalism

Apple WWDC26 *Principles of great design* is explicit: hiding all functionality behind one control looks minimal but is not simple. Simple means the person finds what they need without effort.

Rules:

- **Remove what is unnecessary, not what is useful.** A play button alone is minimal. A play button with elapsed time, remaining time and a scrubber is simple, because the person can decide what to do. Aim for "exactly enough".
- **Show the common 20% first.** Apple *Essential Design Principles* (WWDC17): about 80% of the value comes from 20% of the functions. Show that 20% up front, put the rest one click deeper (progressive disclosure). Example: a print dialog shows printer, copies and page range; everything else is behind "Show Details".
- **Never bury a frequent action in a menu to make the toolbar look clean.** Visibility (WWDC17) beats tidiness when the action is used often. Hamburger menus that hide primary navigation fail this.
- **Rauno, *Contrasting Aesthetics*:** pure minimalism "often fails to stimulate". Calm uniform design is right for utilitarian tools ("a toaster doesn't need to provoke thought"). Expressive brands and first impressions can earn deliberate contrast. Know which one you are designing.

Test: for each element you removed, ask "will someone now need an extra step to do something they do every day?" If yes, put it back.

## 3. Hard limits (numbers)

Default limits. Break one only with a written reason.

| Thing | Limit | Source |
|---|---|---|
| Typefaces in a product | 2 maximum, 1 is often better | Hobday rule 23; Vignelli did a career's work with 4 faces in total |
| Font sizes visible in one view | 2 to 3 (body, heading, small) | Vignelli: "no more than two type sizes on a printed page"; heading about 2x body |
| Type scale for the whole product | 5 to 7 steps actually used | Refactoring UI defines 11 steps (12 to 72px) and uses a subset per screen |
| Heading levels | 3 maximum, 2 is better | Butterick, headings |
| Font weights in use | 2 to 3 (regular, medium or semibold, bold) | Rauno: no weights below 400; medium headings at 500 to 600 |
| Accent colours | 1 brand accent, plus semantic status colours | Liquid Glass: "When every element is tinted, nothing stands out" |
| Primary buttons per view | 1 | Refactoring UI: one primary, a couple of secondary, few tertiary |
| Depth techniques | 1 style throughout (soft shadow, or hard shadow, or flat with borders) | Hobday rule 27 |
| Hard divides between two regions | 1 (border OR background change OR divider line) | Hobday rule 25 |
| Exclamation marks | about 1 per long document; none in errors | Butterick; Apple WWDC22 and WWDC25 |
| Novel visual or motion treatments | about 10% of the experience | Rauno, *Novelty* |
| Configuration parameters on a widget or card | 1 to 2, with good defaults | Apple, WidgetKit foundations (WWDC26) |

## 4. Where to spend novelty: the 90/10 rule

Rauno Freiberg, *Novelty* (2026): novelty works only as contrast. Its effect drops each time the person sees it (he compares this to semantic satiation, when a repeated word loses meaning).

- **Make 90% of the experience familiar and 10% novel.** He borrows the film colour rule of about 60% primary, 30% secondary, 10% accent, and treats the accent as the novelty budget.
- **Spend novelty on rare moments:** onboarding, first launch, a celebration, an empty state seen once, a marketing page. Play a staggered entrance on first load only, not on every return to the page.
- **Never spend novelty on frequent paths:** command menus, context menus, list add and delete, hover on small buttons. Rauno removed the animation from his own bookmarking tool's command menu after two days because it felt sluggish at hundreds of uses a day.
- **Novelty is "the equivalent of an exclamation mark".** Seasoning, not the meal.
- **A new product pays a "novelty tax".** Arc's unusual features overwhelmed everyday users. If the audience wants a reliable tool, keep the core familiar and put the surprise at the edges.

Check: list every non-standard visual or motion treatment in the screen. If more than one or two are on the main path, cut down.

## 5. How to cut: a reduction procedure

Run this on any screen that feels busy.

1. **Write the screen's purpose in one sentence** (Apple PACE, WWDC22). Every element must serve it.
2. **List every element.** Mark each as: essential, helpful, decorative, duplicate.
3. **Delete duplicates.** Two buttons that do the same thing, a label that repeats the heading, an icon that repeats the word next to it, a "Welcome to X" heading inside X.
4. **Delete decoration with no job.** A gradient that does not separate anything, a divider between items that already have spacing, a card around content that is the only content.
5. **Replace labels with format where the format is obvious.** Refactoring UI, "Labels are a last resort": an email address does not need "Email:" before it.
6. **Replace borders with space or a background shift.** Refactoring UI, "Use fewer borders".
7. **Collapse rare options** into a "More" menu or a details disclosure.
8. **Merge similar sizes and colours.** If two greys are 4% apart, use one. If two font sizes are 1px apart, use one.
9. **Re-check the purpose sentence.** If the screen still does its job and feels calmer, you are done. If it now needs an extra step for a frequent task, restore that element.
10. **Cut the code the same way.** Dead variants, props no screen passes, duplicate components and styles nothing uses go too. Grep the whole tree (tests, fixtures, names built from strings) before deleting (`workflow/lean-build.md`).

## 6. Restraint in colour

- **Colour as signal, not decoration.** Vignelli: "Most of the time we use color as a Signifier, or as an Identifier." He preferred a primary palette for its timeless formal value. TE pairs shapes with fixed colours (triangle yellow, square blue, circle red) so colour always means the same thing.
- **Grey carries the interface.** Refactoring UI: almost everything is grey; plan 8 to 10 grey shades, then 1 to 2 primary hues with 5 to 10 shades each, then a few accents for status (danger, warning, success, new).
- **Tint the neutrals slightly toward the brand hue,** under 5% saturation in HSB (Hobday rule 2). Use warm or cool neutrals, never both (Hobday rule 10).
- **One tinted primary action per area.** Apple's new design system: the primary action (Done) is separate and tinted; everything else is neutral.
- **Do not use colour alone to carry meaning.** Add an icon, a sign (+ or -) or text (Refactoring UI, Vercel).

## 7. Restraint in type

- **"It is not the type but what you do with it that counts"** (Vignelli). He showed a career of varied work in Garamond, Bodoni, Century Expanded and Helvetica only.
- **Prefer the platform's system font** unless the brand has a reason (Apple, *The Details of UI Typography*). It ships optical sizes, tracking tables and hinting for free.
- **Differentiate with weight, colour and space before size.** Vignelli kept heads and subheads the same size as text, set in bold, "with a line space above and none below".
- **Never use type as decoration and never distort it** (Vignelli: "horrified by any type deformation"). No fake bold, no stretched letters, no outline text for emphasis.

## 8. Restraint in motion and effects

- **The best animation is often none.** Emil Kowalski: Raycast has no open animation and that is "the optimal experience" for something opened hundreds of times a day.
- **Never animate keyboard initiated actions** (Emil, Rauno). They repeat constantly and animation makes them feel disconnected from input.
- **Theme switches should not animate** (Rauno's interface guidelines).
- **Glass, blur and glow only on the floating navigation layer,** never on content, never glass on glass (Apple, *Meet Liquid Glass*).
- **Bounce only when the gesture had momentum.** Default springs are critically damped (Apple, *Designing Fluid Interfaces*).

## 9. Restraint in features and words

- **Decide what not to build** (Apple WWDC26 Purpose). Each feature asks for the user's time, attention and trust. Name what you left out in one line with the condition for adding it ("Skipped: CSV export. Add when a user asks for it."), so the cut is visible and can be reversed.
- **Sunset low-use features** so the product does not get cluttered, slow and hard to maintain (Stamatiou, *Craft*).
- **Ship Simple, Lovable, Complete instead of a rough MVP** (Stamatiou). A small thing done fully beats a large thing done half.
- **Cut filler words:** simply, easily, quickly, just, please, sorry, oops (Apple WWDC25). Keep a descriptive word only when it changes meaning ("feeds your pets automatically").
- **Say it once.** Apple WWDC25: "We're running late. Your driver won't make it on time. They'll be there in 10 minutes." becomes "Delivery delayed 10 minutes."

## 10. When restraint goes wrong

Restraint is not the same as removing contrast or information.

- **Too little contrast is not elegant, it is unreadable.** Hobday: high contrast for important elements, low contrast only for structure. Ultra light grey body text fails people.
- **Hiding everything is not simple** (Apple WWDC26). If a frequent action needs two taps, restraint went too far.
- **Some things are never cut:** focus styles, labels and accessible names, loading, empty and error states, validation, undo, and anything the user asked for. The full list is in `workflow/lean-build.md` section 7. In ponytail's benchmark the plain "write less" prompt was the only one that dropped a safety guard.
- **Uniform calm can be dull** (Rauno, *Contrasting Aesthetics*). A brand site or a first impression can earn one deliberate contrast: an unexpected typeface, a large scale jump, a single expressive image. Make it intentional and make it one.
- **Visual power is allowed.** Vignelli wanted design "forceful", "not limpy": big contrast of scale and weight on a page is restraint done well, because it uses few elements strongly.

## 11. Sources

See `../sources/books/` for full notes: `dieter-rams-ten-principles.md`, `vignelli-canon.md`, `shape-of-design.md`, `practical-typography.md`, `refactoring-ui.md`, `apple-wwdc-design-talks.md`, `rauno-freiberg-craft.md`, `emil-kowalski-design-engineering.md`, `anthony-hobday-safe-rules.md`, `paul-stamatiou-craft.md`, `teenage-engineering-kouthoofd.md`.
