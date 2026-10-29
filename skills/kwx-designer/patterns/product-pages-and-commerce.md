# Product pages and commerce

Built mainly from the uxpeak strawberry redesign (a mobile product detail page fixed mistake by mistake), plus the contrast effect cart from the uxpeak UX psychology video and the declined payment from Tim Gabe. The thesis: "Design for systems, not screens." Every choice must still work with any product image, any catalog item, and the full journey.

Numbers marked (est.) were read off video frames, not stated.

## Contents

1. Images that work for the whole catalog
2. Icons and text over images
3. The information order
4. Title, badge, rating, price
5. Description and attributes
6. The buy area
7. Beyond fixing: structure, persistence, shortcuts, cross sell
8. Cart and checkout
9. Payment failure
10. Before and after
11. Checks

---

## 1. Images that work for the whole catalog

Six options were scored for the hero image:

| Option | Verdict |
|---|---|
| A. Strawberries fill the frame | Too busy, no focal point |
| B. Hands holding strawberries | Focal point is the hands; a lifestyle shot, not a product shot |
| C. One single strawberry on grey | Mismatch: the product is sold by weight |
| D. Saturated blue and pink backdrop | Artificial; fresh organic food should feel natural and honest |
| E. Close up in a basket, natural | Strong alone, but messy in a grid of mixed backgrounds |
| F. Strawberries in a basket on a clean light background | Wins: focus on the product, and the whole catalog can follow one system |

Rules:

1. One clear focal point on the product.
2. The image matches the unit sold (by weight shows a quantity, not one item).
3. Styling matches the brand promise (natural for fresh food).
4. One image system across the catalog: same background, lighting and framing, so a grid of 20 products looks coherent. "Great product images support the entire journey."

## 2. Icons and text over images

1. Never place bare icons or text on a variable image. The back arrow and menu worked only because the first image was dark; on a pineapple on white they vanished.
2. Give each overlay icon a container: a small white circle with enough contrast and a thin outline, so it reads on any image.
3. Text on a photo: a linear gradient from transparent to dark behind the text, optionally with a progressive blur (Kole Jain, every UI concept). A flat full overlay "does not do the image justice".
4. Test with a dark, a bright and a busy image.

## 3. The information order

The reference layout (draw it before restyling):

1. Category label plus promotion badge on one row
2. Product title
3. Social proof (rating)
4. Price
5. Description
6. Attributes
7. Buy area (quantity plus Add to cart)

Within the first screen the user can answer: what is it, how is it rated, how much does it cost. "Good UI is not just about arranging elements. It's about placing information where the user needs it most."

## 4. Title, badge, rating, price

1. **Category label**: small uppercase with added letter spacing, a muted brand colour (muted olive, not neon #00FF00 like green).
2. **Badge**: the shortest phrase that carries the offer ("20% off", not "20% OFF DISCOUNT" plus a percent icon), small red pill, same font as the page. It must not steal attention from the product.
3. **Title**: names the product only ("Organic Strawberries", not "Organic Strawberries - 1 kg", because the stepper changes the quantity). Medium weight, dark grey. "A product title should stand out without shouting." Exactly one primary on the screen: title, badge and CTA were all "screaming primary" before.
4. **Rating**: directly under the title, a 5 star row (4.5 filled, warm amber) plus "4.8 (89 reviews)".
5. **Price**: right under the rating: "$6.20" bold, "$7.20" grey struck through, "per kg". Two decimals, a unit, no "Price:" label. Price placement depends on the product, the audience and the buying context; here users should see it early. The struck price must be a real recent price.

## 5. Description and attributes

1. Description: shorter, friendlier copy (5 lines to 3), line height about 1.6 (was about 1.0 to 1.1, est.), softer grey instead of pure black. "Headlines attract attention, paragraphs support understanding."
2. Attributes: one icon style (all outline), one colour (olive), sentence case labels: "Free delivery", "Organic", "Fresh", "Produced in Mexico". The before had four colours, mixed filled and outline, uppercase labels. Final form: soft pill chips that wrap; an intermediate version used 4 equal columns with icon above label.
3. Dividers thin and light grey, or none.
4. Spacing: tighten oversized gaps so related sections stay connected. "Good spacing is not just about adding more empty space. It's about creating the right relationship between elements."

## 6. The buy area

1. Quantity stepper directly left of the Add to cart button: choose the amount, then add. The unit inside the stepper ("- 3 kg +"), thin border.
2. The total inside the button, live: "Add to cart · $18.60". Users know what they pay before they tap.
3. The CTA is calm: sentence case, moderate size, muted brand colour (olive, not neon green, not ALL CAPS, not oversized full width). "It is the most important action, not the loudest element."
4. Label consistently: if the price had a "Price:" label the stepper would need one too; remove both.

## 7. Beyond fixing: structure, persistence, shortcuts, cross sell

"This is where many redesigns stop." Then make the task easier:

1. **Card over the hero**: content in a white card with rounded top corners and a subtle shadow, overlapping the image. On scroll the card slides up over the image; once the image is no longer the focus, the product title moves into the top nav and stays sticky (centred between back and heart).
2. **Sticky action area**: stepper and Add to cart pinned at the bottom while scrolling ("- 4 kg +", "Add to cart · $24.80"). People decide at different scroll depths.
3. **Preset quantities** from real purchase data: a "Choose weight" row of 4 tiles: 0.5 kg "Snack" $3.10, 1 kg "Regular" $6.20, 2 kg "Family" $12.40, 3 kg "Party" $18.60; the selected tile gets a brand outline. Keep the custom stepper.
4. **Cross sell**: "Often bought with", 2 column cards each with a "+" quick add (Organic Blueberries $7.2/kg, Raspberries $9/kg, Grapes $7/kg, Peaches $7.5/kg). Format those prices with two decimals like the main price.

## 8. Cart and checkout

1. Add ons sit in the cart or order review under the product they relate to, in a "Recommended for you" section between product and totals, with a compact "Add" button, unticked. Never a full page interstitial with "No thanks".
2. A relative price label is allowed only when it compares the same period ("$49/mo, about $588/yr"; the video's "Just 2.6%" compared a monthly fee with a one time price).
3. Totals block: Subtotal, Shipping (say "Free" in green when it is), Total. All fees visible here, before the pay step.
4. Product card in review: name, an "In stock" pill, the configuration ("M3 Pro . 18GB RAM . 512GB SSD"), price, an "Edit" link.

## 9. Payment failure

From the crypto card client (Tim Gabe):

1. A push or alert that names the cause: "Card payment declined: Your payment at Coffee Shop was declined. Please check your balance."
2. The transaction detail: amount struck through, a small orange "Declined" pill, rows for date and time, amount, card, transaction ID with copy, category, and a full width "Contact support" button pinned at the bottom.
3. A specific message per decline reason. Low balance is common and gets its own.
4. Keep the cart. Offer another payment method in place.

## 10. Before and after

| Element | Before | After |
|---|---|---|
| Hero | Full bleed pile of strawberries under the status bar | Basket on a near white warm background, centred |
| Nav icons | Bare on the photo | White circles with a thin outline |
| Category | Neon green, tight tracking | Muted olive, tracked small caps |
| Badge | "20% OFF DISCOUNT" + icon, slab serif | "20% off", page font |
| Title | Very heavy black, with "- 1 kg" | Medium weight, dark grey, name only |
| Rating | One star, under the description | 5 star row under the title |
| Price | "Price: $6.2 $7.2" at the bottom | "$6.20 $7.20 per kg" under the rating |
| Description | 5 tight black lines | 3 lines, about 1.6 line height, grey |
| Attributes | 4 colours, mixed styles, uppercase | One colour, outline, sentence case pills |
| Dividers | Thick near black | Thin light grey |
| Quantity | "- 1 +" far from the button, no unit | "- 3 kg +" beside the button |
| CTA | Full width neon "ADD TO CART" | Olive "Add to cart · $18.60" |
| Layout | Flat page | Card over image, sticky bar, presets, cross sell |

## 11. Checks

| Check | Pass when | Verify in code |
|---|---|---|
| Overlays survive any image | Every icon or text on an image has a container or gradient | Read the hero overlay styles |
| Info order | Title, rating, price are the first three content blocks | Read the component order |
| One primary | Only the buy CTA uses the primary style; title and badge are calmer | Compare weights and colours of the three |
| Price format | One currency formatter, two decimals, unit | Find the formatter; no raw `toString` on prices |
| Total in button | Label computed from quantity times price | Read the label expression |
| Stepper placement | Stepper and button share a row container | Read the buy area layout |
| Sticky action | Buy area is sticky or fixed on long pages | `position: sticky/fixed` or platform equivalent |
| Title clean | Title string has no quantity or variant | Read the title binding |
| Add ons unticked | No add on is preselected | Initial state of add on items |
| Catalog consistency | Image component enforces one aspect ratio and background | Read the image component props |
