# Laws of UX: every law, the rule, and a concrete example

All 30 laws from lawsofux.com (Jon Yablonski), with the origin, the design rule as an imperative, and a good and a bad example. Some laws add detail from Tognazzini, Nielsen and Raskin where they make the rule sharper.

## Contents

- Heuristics: Aesthetic-Usability, Doherty Threshold, Fitts's Law, Goal-Gradient, Hick's Law, Jakob's Law, Miller's Law, Occam's Razor, Pareto, Parkinson's Law, Peak-End Rule, Postel's Law, Tesler's Law, Von Restorff, Zeigarnik
- Gestalt: Common Region, Proximity, Prägnanz, Similarity, Uniform Connectedness
- Cognitive concepts: Choice Overload, Chunking, Cognitive Bias, Cognitive Load, Flow, Mental Model, Paradox of the Active User, Selective Attention, Serial Position Effect, Working Memory
- Quick lookup table at the end

---

## Heuristics

### Aesthetic-Usability Effect
*Users perceive attractive designs as easier to use.* Kurosu and Kashimura (Hitachi, 1995) had 252 people rate 26 ATM layouts: perceived ease of use correlated with beauty more than with actual ease of use.
- **Rule:** make it beautiful, because people forgive small issues in a beautiful product. But test with tasks, not opinions: beauty hides problems in testing.
- **Good:** a polished, calm settings screen where users tolerate one extra tap.
- **Bad:** a gorgeous dashboard that "tested great" in interviews, while users silently fail to find the export button.

### Doherty Threshold
*Productivity soars when the system responds in under about 400 ms, so neither side waits.* Doherty and Thadani, IBM Systems Journal, 1982 (the old standard was 2 s).
- **Rule:** respond to every input within 400 ms; acknowledge within 100 ms. When the real work is slower, use perceived performance: optimistic updates, skeletons, animation that starts immediately.
- **Good:** a "like" turns red instantly and syncs in the background.
- **Bad:** a button that shows nothing for a second and a half before a new page appears, so people press it again.
- Note: a deliberate short delay can make a heavy computation feel more trustworthy (a "searching 400 flights" step), but never delay a routine action.

### Fitts's Law
*Time to acquire a target depends on its distance and size.* Paul Fitts, 1954.
- **Rules:**
  - Make frequent and important targets big and close to where the pointer or thumb already is.
  - Make dangerous targets smaller and farther away from frequent ones.
  - Put pointer targets on screen edges and corners: the edge stops the pointer, so the target is effectively infinite in depth. Corners are the fastest spots on a screen (Tognazzini). A one-pixel gap between a toolbar and the screen edge can slow edge targets by 20 to 30%.
  - Make the whole row, card or label clickable, not only the small icon or text inside it.
  - Touch targets at least 44 by 44 pt (Apple) or 48 by 48 dp (Material), with spacing between.
  - Reduce the number of targets in a sequence, not only their size: total time is the sum.
- **Good:** a context menu that opens at the cursor; a full-width "Continue" at the bottom of a phone screen within thumb reach; a checkbox whose label is also clickable.
- **Bad:** a 16 px close icon in a phone corner; "Delete" right next to "Save" at the same size.

### Goal-Gradient Effect
*People speed up as they get closer to a goal.* Clark Hull, 1932 (rats ran faster near the food).
- **Rule:** show progress in multi-step tasks, and give a head start where honest (a loyalty card with 2 of 12 stamps pre-filled was completed faster than a 10-stamp card).
- **Good:** "Step 3 of 4" with a progress bar in checkout; a profile meter at 60% after sign-up.
- **Bad:** a long form with no indication of how much is left.

### Hick's Law
*Decision time grows with the number and complexity of choices.* Hick and Hyman, 1952.
- **Rules:** cut choices where speed matters; break complex tasks into steps; highlight a recommended option; introduce features progressively to new users. Do not simplify to the point of abstraction (an icon-only toolbar is fewer words, not easier).
- **Good:** Google's home page offers one field; Slack's onboarding first shows only the message box and teaches the rest later; the Apple TV remote moves complexity into on-screen menus.
- **Bad:** a 14-item navigation bar with equal weight; a "Choose your plan" page with six columns and no recommendation.
- Hick's Law applies to choices the user must *decide* between. Scanning a familiar, well-ordered list (an alphabetical country list) is closer to a search and grows more slowly.

### Jakob's Law
*Users spend most of their time on other products, so they expect yours to work the same way.* Jakob Nielsen.
- **Rules:** reuse familiar patterns for standard tasks (cart, checkout, settings, search, file pickers). When you redesign, let users keep the old version for a while.
- **Good:** YouTube's 2017 redesign could be previewed and reverted.
- **Bad:** a custom scrolling model, or a "save" floppy that actually means "export".
- See `mental-models-and-conventions.md` for when breaking a convention is justified.

### Miller's Law
*People hold about 7 plus or minus 2 items in working memory* (Miller, 1956). Modern estimates are lower: about 4 chunks.
- **Rules:** chunk content so nothing needs to be held in the head. Do not use "seven" to justify an arbitrary limit (a nav bar is read, not memorised).
- **Good:** a phone number shown as 030 1234 5678; an IBAN grouped in fours; a settings page split into labelled sections.
- **Bad:** a 16-digit confirmation code shown as one string on one screen, to be typed on another.

### Occam's Razor
*Among equally good explanations, prefer the one with fewest assumptions.*
- **Rule:** remove every element you can without losing function; the design is done when nothing more can be removed. The best way to reduce complexity is to never add it.
- **Good:** a share sheet that lists only the targets the user actually uses.
- **Bad:** a toolbar with decorative separators, two ways to do every action and a "tips" banner.

### Pareto Principle
*Roughly 80% of effects come from 20% of causes.*
- **Rule:** find the 20% of features that 80% of use goes to (analytics, frequency counts, task analysis) and make those the first level; push the rest to secondary levels.
- **Good:** a camera app whose shutter, switch-camera and gallery are on screen and everything else is in settings.
- **Bad:** equal prominence for every feature because each has an owner.

### Parkinson's Law
*Any task inflates to fill the time available.*
- **Rule:** make tasks take less time than users expect: autofill, sensible defaults, remembered values, one-tap reorder.
- **Good:** address autocomplete that fills street, city and postcode from the first few characters.
- **Bad:** a booking form that makes returning customers retype their passport number.

### Peak-End Rule
*People judge an experience mostly by its most intense moment and its end.* Kahneman et al., 1993 (a longer cold-water trial that ended slightly warmer was preferred).
- **Rules:** find the peaks (moments of highest value or highest stress) and design them carefully; make the end good; remember that negative peaks are remembered most vividly.
- **Good:** Mailchimp's send confirmation adds illustration and humour to a stressful moment; Uber shows the car approaching on the map to soften the wait.
- **Bad:** a smooth checkout that ends on a cluttered page of upsells and a newsletter pop-up.

### Postel's Law
*Be liberal in what you accept and conservative in what you send.* Jon Postel, TCP robustness principle.
- **Rules:** accept any reasonable input format and normalise it; output consistent, predictable results; define the limits clearly and give clear feedback at them.
- **Good:** a date field that accepts "3/4", "4 March" and "2026-03-04"; a phone field that ignores spaces, dashes and brackets; search that tolerates typos.
- **Bad:** "Phone number must not contain spaces." (Tognazzini: requiring unspaced numbers saves a few lines of code and costs many errors.)

### Tesler's Law (conservation of complexity)
*Every system has a core of complexity that cannot be removed, only moved between the system and the user.* Larry Tesler, Xerox PARC.
- **Rules:** absorb the complexity in the system wherever possible (Tesler: an engineer should spend an extra week so millions of users do not spend an extra minute). Do not design for an idealised rational user. Note Tognazzini's corollary: when you simplify, users attempt harder things, so keep power available.
- **Good:** an email client that infers the sender's name and avatar instead of asking the user to configure contacts.
- **Bad:** a "simple" app that removes a needed capability and forces workarounds (Tognazzini's iPad alarm that offers only one or two hours of warning).

### Von Restorff Effect (isolation effect)
*Among similar items, the one that differs is remembered.* Hedwig von Restorff, 1933.
- **Rules:** make the primary action or key information visually distinct; use restraint so only one thing stands out; never rely on colour alone; be careful with motion as the distinguishing cue; do not make important content look like an ad (it will be ignored).
- **Good:** one filled primary button among outlined secondary ones; the recommended plan with a badge and a border.
- **Bad:** five red "NEW" badges on one screen.

### Zeigarnik Effect
*Unfinished tasks are remembered better than finished ones.* Bluma Zeigarnik, 1920s.
- **Rules:** show clear signifiers that more content exists; show progress and what remains; let users resume where they left off.
- **Good:** "2 steps left to finish your profile"; a half-visible card at the edge of a carousel.
- **Bad:** abusing it with fake unfinished states to pull users back.

## Gestalt principles

### Law of Common Region
*Elements inside a shared bounded area are seen as a group.*
- **Rule:** put related controls in a card, panel or background tint; one region per concept.
- **Good:** a card containing a product image, name, price and its own "Add" button.
- **Bad:** a "Delete" button that sits inside the visual box of the item below the one it deletes.

### Law of Proximity
*Things near each other are seen as related.*
- **Rules:** space within a group must be clearly smaller than space between groups (a ratio of about 1 to 2 or more). Put a label closer to its own field than to the next field.
- **Good:** Google results, where each result's title, URL and snippet are tight and results are separated by larger gaps.
- **Bad:** a form with equal spacing everywhere, so the user cannot tell whether a label belongs to the field above or below.

### Law of Prägnanz (simplicity)
*People read ambiguous shapes in the simplest possible form.* Max Wertheimer, 1910.
- **Rule:** use simple, regular shapes and layouts; simple figures are processed and remembered better.
- **Good:** a schematic icon with a single clear silhouette.
- **Bad:** a detailed illustrative icon that turns into noise at 16 px.

### Law of Similarity
*Elements that look alike are seen as a group or as sharing a function.*
- **Rules:** give every element of the same type the same look; make links and controls look different from plain text.
- **Good:** all clickable tags share one chip style; all static tags use a different, flat style.
- **Bad:** the same coloured pill used for both clickable filters and read-only status labels.

### Law of Uniform Connectedness
*Visually connected elements are seen as more related than unconnected ones.*
- **Rule:** connect related items with lines, frames or shared colour; use connectors to show sequence or dependency.
- **Good:** a stepper whose steps are joined by a line; Google's bordered "featured snippet" box.
- **Bad:** a chain of dependent settings with no visual link between parent and child.

## Cognitive concepts

### Choice Overload (paradox of choice)
*Too many options overwhelm people and lower satisfaction.* Alvin Toffler, 1970.
- **Rules:** show a featured or recommended option; offer search and filters to narrow early; when comparison is needed, show options side by side with aligned attributes.
- **Good:** a pricing table with three tiers, aligned rows and one recommended.
- **Bad:** a "pick a theme" dialog with 80 thumbnails and no categories.

### Chunking
*Break information into meaningful groups.* From Miller, 1956.
- **Rule:** group content into visually distinct modules with headings and hierarchy so users can scan to what matters.
- **Good:** an order summary split into Items, Delivery and Payment.
- **Bad:** a 40-field settings list with no sections.

### Cognitive Bias
*Systematic errors in judgement from mental shortcuts.* Tversky and Kahneman, 1972.
- **Rule:** expect users (and yourself) to rely on shortcuts: defaults get accepted, the first result gets clicked, information that confirms belief gets noticed. Design defaults and order responsibly; check your own design decisions against confirmation bias by testing.
- **Good:** a privacy-preserving default, because most users keep defaults.
- **Bad:** pre-checked add-ons that exploit default bias.

### Cognitive Load
*The mental effort needed to understand and use an interface.* John Sweller, 1988.
- **Rules:** cut *extraneous* load (decoration, inconsistency, needless choices, jargon, remembering things the screen could show). Support *intrinsic* load (the real complexity of the task) with structure, examples and visible state.
- **Good:** inline examples under a complex field ("e.g. 0 9 * * 1").
- **Bad:** decorative animation running while the user fills in a tax form.

### Flow
*Full immersion and focus, when challenge matches skill.* Csíkszentmihályi, 1975.
- **Rules:** give immediate feedback; remove friction (dialogs, waits, re-entering data); keep features discoverable so users are not stalled; match difficulty to skill.
- **Good:** an editor where typing, formatting shortcuts and autosave never interrupt.
- **Bad:** a "Saved!" modal after every save in a writing app.

### Mental Model
*A compressed internal model of how a system works.* Kenneth Craik, 1943.
- **Rule:** match the design to the model users bring from similar products; shrink the gap with research (interviews, think-aloud, card sorting).
- **Good:** e-commerce sites share product cards, carts and checkout flows, so users transfer knowledge.
- See `mental-models-and-conventions.md`.

### Paradox of the Active User
*Users never read manuals; they start using the product immediately.* Carroll and Rosson, 1987.
- **Rules:** never depend on a tutorial or manual; put guidance in context, at the moment and place it is needed (tooltips, inline hints, empty-state instructions).
- **Good:** a field-level hint that appears when the field is focused.
- **Bad:** a seven-card intro carousel before the app can be used.

### Selective Attention
*People attend only to the stimuli tied to their current goal.*
- **Rules:** guide attention to what matters for the task; do not style content like ads (banner blindness: users ignore anything that looks like, sits near, or is placed where ads usually are); avoid change blindness by not changing several things at once and by animating important changes.
- **Good:** a single subtle highlight that pulses once on the item that just changed.
- **Bad:** an important notice in a colourful right-rail box that looks like a banner ad.

### Serial Position Effect
*People remember the first and last items in a series best.* Ebbinghaus.
- **Rule:** place the most important items at the start and end of lists and navigation; put the least important in the middle.
- **Good:** a tab bar with Home first and Profile last.
- **Bad:** the key action buried as item 5 of 9 in a menu.

### Working Memory
*A temporary store of about 4 to 7 chunks, each fading in 20 to 30 s.*
- **Rules:** put the burden of memory on the system: carry information across screens, mark visited items, show breadcrumbs, offer comparison tables instead of making users remember specs from page to page.
- **Good:** a flight-booking step that still shows the dates, airports and fare already chosen (NN/g's Hipmunk example).
- **Bad:** a 2FA screen that hides the code's source, so the user must switch apps and remember six digits.

## Quick lookup table

| Situation | Laws to apply |
|---|---|
| Choosing how many options to show | Hick, Choice Overload, Pareto, Miller |
| Placing and sizing buttons | Fitts, Von Restorff, Serial Position |
| Grouping a layout | Proximity, Common Region, Similarity, Uniform Connectedness, Chunking |
| A long or multi-step task | Goal-Gradient, Zeigarnik, Working Memory, Parkinson |
| Anything slow | Doherty, Peak-End |
| Input fields | Postel, Tesler, Parkinson |
| A redesign | Jakob, Mental Model, Aesthetic-Usability |
| First-run experience | Paradox of the Active User, Hick, Cognitive Load |
| Making something stand out | Von Restorff, Selective Attention |
| Simplifying | Occam, Tesler, Pareto |
