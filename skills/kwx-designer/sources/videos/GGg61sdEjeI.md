# This UI/UX Redesign Will Teach You More Than 100 Tutorials Combined

- Channel: uxpeak (UX Peak)
- URL: https://www.youtube.com/watch?v=GGg61sdEjeI
- Duration: 13:32
- Subject: a mobile e-commerce product detail page (Organic Strawberries, fresh food store), fixed mistake by mistake (15 mistakes), then improved with 3 UX upgrades.
- Notes method: auto transcript (en-orig) plus 96 scene/interval frames and 26 targeted frames, read as contact sheets and at full size.

## Core thesis

A screen that "looks fine" usually hides 10 to 15 small decisions that make it feel cheap: edge cases nobody tested (a bright image under white icons), loose alignment, saturated colours, too many fonts, heavy dividers, shouting buttons, information placed far from where the user needs it. Fix them in order from the foundation up (image system, grid, colour, type), then content and hierarchy, then the buying flow. Design for a product system, not one screen: every choice must still work with any product image, any catalog item, and the full journey. Strong product design does not stop at fixing what is broken; the last step is making the task itself easier (sticky action area, total price in the button, one tap preset quantities).

## The redesign in one picture (before vs after, final frame 13:26)

| Element | Original | New version |
|---|---|---|
| Hero image | Full bleed close up of a pile of strawberries, runs under the status bar, no focal point | Strawberries in a wicker basket, cut out on a soft light grey (near white, warm) background, centred, the product is the focal point |
| Nav icons | Back arrow and a three dot menu drawn directly on the photo | Back arrow and heart in small white circular containers with a thin outline, readable on any image |
| Category label | "FRUITS", neon green (#00FF00 like), tight letter spacing | "FRUITS", muted olive green, small uppercase with added letter spacing |
| Discount badge | Red pill "20% OFF DISCOUNT" + percent icon, slab serif caps, a different font from the page | Small red pill "20% off", same font as the page, no icon |
| Title | "Organic Strawberries - 1 kg", very heavy black (Mulish black/extra bold) | "Organic Strawberries", medium weight, dark grey, Lato, quantity removed from the title |
| Rating | "4.8 (89 reviews)" with one yellow star, placed below the description and a divider | 5 star row (4.5 filled, warm orange/amber) + "4.8 (89 reviews)" directly under the title |
| Price | "Price: $6.2 $7.2" at the bottom, label "Price:", one decimal | "$6.20" bold + "$7.20" grey strikethrough + "per kg", placed right under the rating, above the description, no "Price" label, two decimals |
| Description | Long, tight line height (about 1.0 to 1.1), pure black, 5 lines | Rewritten shorter copy, 3 lines, line height about 1.6, softer grey |
| Feature attributes | 2x2 grid of uppercase labels with icons in 4 colours (green filled truck, purple outlined drop, yellow globe, green filled leaf), mixed filled/outline | Monochrome olive outline icons, sentence case labels ("Free delivery", "Organic", "Fresh", "Produced in Mexico"), as soft pill chips; an intermediate version used 4 equal columns, icon above label |
| Dividers | Thick, near black lines | Thin, light grey, barely there |
| Quantity | "- 1 +" without unit, far from the button, on the price row | "- 3 kg +" stepper with a thin border, unit inside, sitting directly left of the button |
| CTA | Full width, neon green, white ALL CAPS "ADD TO CART", large | Olive green, sentence case "Add to cart · $18.60", smaller, total price inside |
| Layout | One flat white page, image glued to content | Content in a white card with rounded top corners overlapping the image, sticky bottom action bar |

## Timestamped walkthrough

- 00:00 to 00:37 Intro. Shows the original page with 15 numbered callouts and asks the viewer to count mistakes. "If you found at least 10 mistakes, you are a great designer." Original: neon green full width ALL CAPS "ADD TO CART", "Price: $6.2 $7.2 - 1 +", red "20% OFF DISCOUNT" badge, title "Organic Strawberries - 1 kg", multicolour attribute icons, black dividers.
- 00:37 Mistake 1, icons lost in the image. The photo goes to the edge and the back/menu icons sit straight on it. They only work because this image is dark. Swapping in a pineapple on white (0:57) makes the white icons vanish; a pizza (1:07) shows a busy image. Fix: a subtle background container (white circle) behind each icon, enough contrast, and a thin outline so they read on any background. On screen a toggle with an eye icon tests visibility across images. Caption card at 1:26: "Design for systems, not screens." Spoken: "This is the difference between designing for one screen and designing for a real product system."
- 01:28 to 02:00 Sponsor: Mobbin. Shows Mobbin's UI: Apps/Sites tabs, search "Product page", categories (Food & Drink, Education, Business, Finance, Health & Fitness), screens (Signup, Dashboard, Home, Filter & Sort, Payment Method), UI elements (Stacked List, Text Field, Banner, Button, Bottom Sheet), flows (Onboarding, Editing Profile, Creating Account, Filter & Sort, Verifying), and a flow filter listing Checkout, Order Confirmation, Tracking, Collections, Reporting. Advice: study how great products already solve the same problem, across the full journey (discover, product page, checkout, confirmation, saved items, order tracking).
- 02:00 Mistake 2, the product image. Six options A to F shown as full page mockups, then each scored with an emoji meter:
  - A: strawberries fill the whole frame. Too busy, no focal point (red meter, dizzy face).
  - B: hands holding strawberries. Has a focal point but it is the hands; reads as lifestyle photo, not product shot.
  - C: one single strawberry on grey. Simple, but the product is sold by weight, so one berry is a mismatch with what is bought.
  - D: strawberries on a saturated blue/pink backdrop (a rainbow slider shown). Styled but artificial; fresh organic food should feel natural, honest, real.
  - E: close up in a basket, natural. Strong on its own, but it will sit in a product grid; shown a grid of mixed backgrounds (bananas, apple on green, pear, watermelon, blueberries) that looks messy.
  - F wins: natural strawberries in a basket on a clean light background. The product is the focus and the whole catalog can follow one visual system.
  - Caption at 3:31: "Great product images support the entire journey." Principle: an image is not just beautiful alone, it must work inside the full shopping experience.
- 03:34 Mistake 3, alignment. "Reference Layout" wireframe shown (3:40): rows labelled CATEGORY LABEL + PROMOTION BADGE on one line, PRODUCT TITLE, Product Description, divider, SOCIAL PROOF, PRODUCT ATTRIBUTES (Free Delivery, Fresh, Origin, Organic), divider, PRICE: TOTAL with stepper, ADD TO CART. Overlays mark "Side margins" and "Section Spacing" bands. In the original: the badge pokes past the right margin, dividers are inset differently from the text, the description starts at a different x than the icons (a "17 px" measurement chip at 4:09 shows the mismatch between edges). Fix: define consistent margins, e.g. content starts 24 px from the left and everything follows the same structure; snap all elements to one grid. Users do not consciously notice misalignment, but they feel it: less calm, less structured, less trustworthy.
- 04:17 Mistake 4, colour. Too bright, too saturated, emphasising the wrong things: harder to read, weaker hierarchy, too many elements competing. Palette chips shown: before red, neon green, yellow, purple, orange; after muted red, olive green, mustard, steel blue, plum, with tags "sets the mood" and "supports product". CTA goes neon green to olive/moss green; FRUITS label to olive. On a fresh organic food page the colour should support the product, not overpower it.
- 04:51 Mistake 5, typography. Original font labelled on screen "Mulish Semibold"; the badge uses a different slab serif style, so several font styles coexist. Bolt app shown (5:02) as reference of a clean single family product page. Rule: one strong font family is usually enough; build hierarchy with size, weight, colour and line height (a "Heading & Subheading / body" specimen shown at 5:11). Switched to Lato.
- 05:20 Mistake 6, labels. "FRUITS" letters too close; small uppercase labels need a little letter spacing to breathe (red tracking guides drawn between letters at 5:26). Badge "20% OFF DISCOUNT" + icon is too much for a small label; changed to "20% off" (5:45). Badges must be scannable instantly and must not steal attention from the product.
- 05:50 Mistake 7, the title. Callouts at 5:55 mark three things all screaming "Primary" (title, badge, CTA), and at 6:04 "Competing visual weight" between badge and title. Title was bold but size and weight gave the wrong hierarchy. Fix: adjust size and weight; "A product title should stand out without shouting." Final title is a medium weight in dark grey.
- 06:20 Mistake 8, paragraph text. Lines too close (6:30 shows lines overlapping in red with "look at me!" tags). Fix: increase line height, slightly reduce body contrast (black to grey). The copy is also rewritten shorter and friendlier (6:38 to 7:02): "Grown without pesky synthetic pesticides and fertilizers. These fresh strawberries are packed with natural nutrients and a delicious taste." Rule spoken: "headlines attract attention, paragraphs support understanding."
- 06:51 Mistake 9, review placement. Rating sat below the description and a divider, far from the title. Reviews are one of the strongest trust signals. Moved directly under the title, as a 5 star row (7:12). Users now get: what is it, how is it rated, do others trust it. The tag "What is it?" over the title and stars beside it (7:08). "Good UI is not just about arranging elements. It's about placing information where the user needs it most."
- 07:27 Midpoint comparison (7:31): original vs current. Then sponsor: UX Peak Plus (course library: Designing SaaS Product Pages, Advanced UI Refinement, UX Psychology Patterns, Product Copy That Converts, Make Mobile UI Feel Senior, Junior vs Senior UI Decisions, Pricing Psychology for Designers, High Converting Forms and Flows, Make Any UI Look Premium). Code "redesign25" for 25% off.
- 08:21 Mistake 10, feature icons. Too many colours, inconsistent styles (some heavy, some light, some filled, some outlined); an "Inconsistent styles" callout at 8:38. Fix: one colour (olive), one outline style, tighter spacing, sentence case labels under icons in 4 equal columns (8:48, 9:16). The section still informs but no longer dominates. "You can use different colors in UI design, but they need to be used intentionally."
- 08:57 Mistake 11, divider lines. Extremely dark and heavy, they cut the page into harsh blocks. Softened to thin light grey. "Small details are often what make an interface feel premium."
- 09:21 Mistake 12, spacing balance. Some gaps too large (9:26 shows dashed boxes around each group; 9:30 shows pink bars for oversized gaps). Too much white space in the wrong place disconnects the layout. Tighten slightly so sections relate. "Good spacing is not just about adding more empty space. It's about creating the right relationship between elements."
- 09:47 Mistake 13, redundant price label. "Price:" crossed out (9:55). A number with a currency symbol already reads as a price. Consistency argument: if you label the price you must also label the quantity stepper, otherwise the UI is inconsistent. Remove the label; let the price speak for itself. (10:14 shows the price briefly in purple during the step.)
- 10:16 Mistake 14, quantity in the title and price placement. "Organic Strawberries - 1 kg" with a "problem" tag (10:24): the stepper changes quantity, so "1 kg" in the title becomes misleading. Title describes the product; quantity lives in the buying area. Price was far down; a panel (10:45) says price placement depends on Product (determines price importance), Audience (determines when price matters) and Buying context. Here users should see it early: moved under the rating as "$6.20 $7.20 per kg" (two decimals, unit added), stepper on the same row at first (10:52, 11:02).
- 10:57 Mistake 15, the purchase action. Add to cart is the most important action but shouts: all caps, large. Softened to sentence case "Add to cart", smaller, refined (11:12). Quantity selector moved directly next to the button (choose amount, then add). Unit "kg" put inside the stepper ("1 kg"). Total price added inside the button: "Add to cart · $6.20" (11:31), so users know what they pay before they click, removing uncertainty. Caption: "this is where many redesigns stop."
- 11:40 "Fixing the issues" vs "Enhancing" timeline graphic (a lock/shield icon for the enhancing phase).
- 11:46 Improvement 1, scrollable card. Content becomes a soft card with rounded corners and a subtle shadow; the image has its own space, details have their own. On scroll the card slides up over the image, keeping it visible at first; once the image is no longer the focus, the product title transitions into the top navigation and stays sticky (12:09 shows "Organic Strawberries" centred in the nav bar between back and heart). A new "Often bought with" section appears: 2 column cards with a + button (Organic Blueberries $7.2/kg, Organic Raspberries $9/kg, Organic Grapes $7/kg, Organic Peaches $7.5/kg).
- 12:16 Improvement 2, sticky bottom action area. Stepper and Add to cart stay pinned while scrolling (12:27, 12:43 shows "- 4 kg +" with "Add to cart · $24.80"). Users do not always decide at the top; they read, compare related products, and act when ready.
- 12:43 Improvement 3, predefined quantity options. "Choose weight" row of 4 tiles: 0.5 kg "Snack" $3.10, 1 kg "Regular" $6.20, 2 kg "Family" $12.40, 3 kg "Party" $18.60; selected tile gets an olive outline. One tap instead of many stepper taps. Base the presets on real purchase data (a "30% 1 kg" pie chip is shown, i.e. the most bought sizes). The custom stepper is kept for flexibility. Attribute chips now wrap as pills: Free delivery, Organic, Fresh, Produced in Mexico. "A small UX improvement with a real business impact."
- 13:09 to 13:32 Final 3D phone render and "PRODUCT IMAGE" annotated system diagram; final Original vs New version comparison. "The images feel consistent. The layout feels predictable. The product information is easy to scan."

## The redesign method (process order, repeatable)

The order he follows, from foundation to flow. Use it as a pass list on any screen.

1. Stress test the variable content. Swap the image (dark, bright, busy, simple, lifestyle, cutout) and check every overlay (icons, text on images). Add containers, contrast and outlines until it works for all.
2. Fix the media system. Choose imagery that has a focal point, matches what is sold (unit, quantity), feels honest for the brand, and is consistent across the whole catalog grid.
3. Grid and alignment. Draw a reference layout (wireframe of the content blocks), set side margins (e.g. 24 px) and section spacing, snap every element to the same edges.
4. Colour. Reduce saturation, cut to a palette that supports the product and mood, keep strong colour for the few things that deserve emphasis.
5. Typography system. One family; hierarchy by size, weight, colour, line height.
6. Small labels and badges. Track small caps, shorten badge copy to the minimum.
7. Title hierarchy. Stand out without shouting; remove competing primaries.
8. Body text. More line height, lower contrast, shorter and warmer copy.
9. Information placement for trust. Put social proof next to the name.
10. Supporting sections (icons). One icon style, one colour, tighter.
11. Separators. Soften or remove.
12. Spacing rhythm. Group related, tighten oversized gaps.
13. Remove redundant labels (and keep labelling consistent).
14. Content correctness and order. Title describes the product, quantity belongs in the buy area, price surfaces early.
15. Primary action. Calm the CTA, put its inputs next to it, show the consequence (total) inside it.
16. Then go beyond fixes: structure (card over image, sticky title), persistence (sticky action bar), shortcuts (presets from real data), cross sell ("Often bought with").

## Extracted rules

Overlays and images
- Never place bare icons or text on a variable image. Give each a background container (e.g. white circle) with enough contrast plus a thin outline. Test with a dark, a bright and a busy image.
- Pick product images with one clear focal point on the product, not on hands, props or a pattern of the product.
- The image must match the unit sold: sold by weight means show a quantity, not one item.
- For natural/organic goods, use natural, honest styling; avoid artificial saturated backdrops.
- Use one image system across the catalog: same clean background, lighting and framing on every product, so the grid looks coherent.

Layout
- Define side margins once (example: 24 px) and start every text block, icon row, divider and badge on the same edges. Nothing pokes past the margin.
- Sketch a reference layout of the content blocks before restyling: category + badge row, title, social proof, price, description, attributes, buy area.
- Keep section spacing consistent; tighten gaps that are noticeably larger than the rest so related sections stay connected.

Colour
- Desaturate. Replace neon/pure hues (#00FF00 green, pure yellow, saturated purple) with muted ones (olive, mustard, steel blue, plum, muted red).
- Choose the palette to support the product's mood (fresh food: natural greens), not to compete with the image.
- Use extra colours only with a reason; icon sets and attributes get one colour.

Typography
- One font family per screen in most cases (he used Lato). Badges use the same family as the page.
- Build hierarchy with size, weight, colour and line height, not with more fonts.
- Small uppercase labels: add letter spacing.
- Product title: medium/semibold, dark grey, stands out without shouting; it should not compete with the badge or the CTA for "primary".
- Body: line height about 1.5 to 1.6 (visible: about 1.0 before, about 1.6 after), slightly lower contrast than headings (grey, not pure black).
- Headlines attract attention, paragraphs support understanding.
- Avoid ALL CAPS on buttons and on attribute labels; use sentence case.

Copy and content
- Badges: the shortest phrase that carries the offer ("20% off", not "20% OFF DISCOUNT" + icon).
- Drop labels that the format already explains ("Price:" before "$6.20").
- Label consistently: if one control gets a label, its sibling controls need one too; otherwise label none.
- The title names the product only; variable attributes (quantity, size) live in the selector.
- Show prices with two decimals and a unit ("$6.20 per kg"), old price struck through in grey.
- Rewrite long descriptions shorter and friendlier (5 lines to 3).

Placement and flow
- Put the rating right under the product title: what is it, how is it rated, can I trust it.
- Surface the price early, near the title, unless the product/audience/context says otherwise (price placement depends on product, audience, buying context).
- Place the quantity selector directly next to the add to cart button; put the unit inside the selector ("1 kg").
- Put the total in the primary button ("Add to cart · $18.60") and update it live with quantity.
- Make the primary action calm: sentence case, moderate size, muted brand colour. It is the most important action, not the loudest element.
- Keep the buy area sticky at the bottom on long pages.
- On scroll, let the content card slide over the hero; once the hero leaves, move the title into the top nav, sticky.
- Offer one tap presets for common choices, derived from real purchase data, with friendly names (0.5 kg Snack, 1 kg Regular, 2 kg Family, 3 kg Party, each with its price). Keep the free stepper.
- Add related products ("Often bought with") with a quick add + on each card.

Details
- Dividers: thin and light grey, or none. Heavy black dividers split the page into harsh blocks.
- Icons in one set share weight, fill style (all outline or all filled), size and colour.

## Anti-patterns and their fixes

- White icons straight on a photo: invisible on bright images. Fix: circular container + contrast + thin outline.
- Designing against one sample image. Fix: test the full range of real content.
- Busy, edge to edge texture photos with no focal point. Fix: cutout product on a clean background.
- Mismatched catalog photography. Fix: one background/lighting system.
- Elements on slightly different left/right edges (a 17 px offset was called out). Fix: one margin, one grid.
- Neon, saturated colours everywhere (neon green CTA and label, rainbow icons). Fix: muted, product supporting palette.
- Several fonts and styles (body in Mulish, badge in a slab serif). Fix: one family.
- Cramped small caps. Fix: letter spacing.
- Long badge ("20% OFF DISCOUNT" + icon). Fix: "20% off".
- Three things all styled as primary (heavy title, loud badge, loud CTA). Fix: one primary; tone the others down.
- Tight, pure black paragraph text. Fix: more line height, grey.
- Rating buried below the description. Fix: move under the title.
- Mixed filled and outline icons in many colours. Fix: one style, one colour.
- Thick black dividers. Fix: thin light grey.
- Inconsistent, oversized gaps. Fix: tighten to a rhythm.
- "Price:" label in front of a currency number. Fix: remove.
- Quantity baked into the title ("- 1 kg") while a stepper exists. Fix: title is the product, quantity is in the selector.
- Price at the bottom of the page. Fix: near the title.
- Stepper far from the button, no unit in it. Fix: adjacent, unit inside.
- ALL CAPS, oversized, full width neon button that "shouts". Fix: sentence case, smaller, muted colour, total inside.
- Stopping at "fixed the mistakes". Fix: improve the task (sticky actions, presets, cross sell, sticky title).

## Quality checks before shipping

- Swap the hero image for a bright one and a busy one: are all overlays still readable?
- Would this image style still look right next to 20 other products in a grid?
- Does the image match what is sold (unit, quantity)?
- Draw vertical guide lines at the margins: does every element start and end on them?
- Squint: how many elements compete for attention? Is there exactly one primary?
- Count font families and styles on the screen. More than one family needs a reason.
- Are any colours saturated beyond what the product needs? Does the palette support the product?
- Are small uppercase labels tracked? Are buttons and attribute labels in sentence case?
- Body text: line height near 1.5 to 1.6 and softer than headings?
- Is every badge readable in one glance?
- Is any label redundant given the format? Is labelling consistent across sibling controls?
- Does the title contain anything the user can change elsewhere?
- Within the first screen, can the user answer: what is it, how is it rated, how much does it cost?
- Is each input placed right next to the action it feeds? Does the action show its consequence (total)?
- On a long page, is the primary action always reachable? Is context (the title) kept when the hero scrolls away?
- Are there one tap shortcuts for the most common choices, based on data?
- Are all icons in one set the same style, weight and colour? Are dividers subtle?

## Psychology and why it works

- Misalignment is felt, not noticed: it makes a screen feel less calm, less structured and less trustworthy.
- Too many saturated colours weaken hierarchy because everything competes; muted colour lets the product and the one primary action lead.
- Reviews are one of the strongest e-commerce trust signals; placing them at the product name answers "can I trust it?" at the moment of "what is it?".
- Showing the total inside the button removes uncertainty before commitment.
- People decide to buy at different scroll depths; a sticky action area lets them act at the moment they are ready.
- Presets cut effort (many stepper taps to one) and steer to common, data backed sizes: small UX change, real business impact.
- A misleading title ("1 kg" while 3 kg are selected) creates a small mismatch in the user's mind, which costs trust.
- Natural, honest imagery matches the expectation for fresh organic food; artificial styling breaks it.

## Cited resources

- Mobbin (mobbin.com): sponsor. Library of real product flows and screens from top apps (iOS and web), searchable by category, screen type, UI element and flow (product pages, checkout, order confirmation, saved items, tracking, collections). Used to study how strong products solve the same problem across the full journey. 20% off first year via the video's link.
- UX Peak Plus (uxpeak.com): the channel's own course platform, "Learn pro UX/UI design skills through interactive courses", rated 4.8/5 on Trustpilot per the page shown. Courses visible: Designing SaaS Product Pages, Advanced UI Refinement, UX Psychology Patterns, Product Copy That Converts, Make Mobile UI Feel Senior, Junior vs Senior UI Decisions, Pricing Psychology for Designers, High Converting Forms and Flows, Make Any UI Look Premium. Code "redesign25" for 25% off. Pitch: explains why a decision works, not just what looks good.
- Lato (Google Fonts): the single family used in the redesign, "a cleaner font".
- Mulish (Semibold): the original page's font, labelled on screen; replaced.
- Bolt (ride hailing / car rental app): its Audi Q2 car detail screen shown during the typography step as an example of a clean single family product page.
- Apps visible in the Mobbin and intro montages (examples of reference screens, not discussed): Phantom (crypto wallet), Fiverr, a recipes app ("All Recipes"), Apple Store app product browsing, an eyewear try on product page, DoorDash (DashMart, Deals, Convenience, Grocery tabs).

## Memorable quotes

- "Design for systems, not screens." (on screen caption)
- "Great product images support the entire journey." (caption)
- "A good product image is not just beautiful by itself. It also has to work inside the full shopping experience."
- "When alignment is off, users may not consciously notice it, but they feel it."
- "A product title should stand out without shouting."
- "Headlines attract attention, paragraphs support understanding."
- "Good UI is not just about arranging elements. It's about placing information where the user needs it most."
- "Small details are often what make an interface feel premium."
- "Good spacing is not just about adding more empty space. It's about creating the right relationship between elements."
- "Let the price speak for itself."
- "Strong product design is not just about fixing what is broken. It's about making the whole experience feel easier."
