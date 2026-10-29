# The Icon Handbook (Jon Hicks, Five Simple Steps, 2011): reading notes

Source: the author's own free download, announced on https://hicks.design/shop/the-icon-handbook ("The Icon Handbook is now available to download for free! ... I now feel that the content is too out of date to charge actual money for. So you can now download the PDF for free"). File: https://hicksdesign.ams3.cdn.digitaloceanspaces.com/IconHandbook_Optimised.pdf (162 pages, square format). The book is still "All rights reserved", so these notes paraphrase and quote only short lines.

Read in full: chapter 2 (How we use icons), chapter 4 (The metaphor), chapter 5 (Drawing icons), the Susan Kare interview in chapter 1, and the appendix badge chart. Skimmed: chapter 3 (favicons, for the pixel crispness basics) and chapter 6 (formats and deployment). Skipped: chapter 7 (application icons, mostly photorealistic app icons) and the tool lists, which are dated (Fireworks, Opacity, IE6).

What is dated: the file format chapter (CSS sprites, icon fonts as "largely untapped", canvas, Raphael) predates the GitHub 2016 move to SVG and modern accessibility patterns. Its delivery advice is superseded by `icons/delivery.md`. The design advice (metaphor, balance, company, context, badges) has not aged.

## The core ideas worth keeping

### 1. Icons must earn their place (chapter 2)

- Icons do real jobs: navigation and wayfinding, managing expectations (a disclosure arrow says "a menu opens", a magnifier on a thumbnail says "zoom", a play symbol says "video"), comparison charts, status (the Coda file states: unsaved, publish, pending, uploading, finished), feedback next to form fields, crossing language barriers, emotion.
- Never use colour alone for meaning. About one man in twelve has a colour vision deficiency (Hicks is one), and colours mean different things in different cultures (red is luck in China, danger in the west). Pair colour with a shape.
- Size and grouping decide whether a nav icon helps. His bad example: icons at the text x-height, spaced evenly between labels instead of next to their own label, indistinct. "If it wasn't possible to use larger icons in the design, the navigation would've worked better without any icons at all."
- The restraint test, his own checklist: first remove the icon and see if the design works without it. Then ask: is it only decoration? Is it repeated so often it lost meaning? Too many in a small space? Does it need text to be understood? Does the page look like a "Christmas tree"? If so try monochrome, or keep only the one most important icon (the basket, the contact details). Basecamp's restraint (icons only on delete, print, add) is the model.

### 2. The brief and the metaphor (chapter 4)

- A brief is usually a "laundry list of concepts". Question every item before drawing:
  1. What is it for (warning, wayfinding, action)?
  2. What is its context (toolbar, next to a text link, small in a list) and size? Sometimes the space makes it too small to be useful.
  3. Who is it for (age, culture)? Treat icons with personas like any other design.
  4. Is there a single message? "History of customer support requests" is too much; "history" works.
  5. Does it need to be an icon at all, and does it need text with it?
- Convention first, always. Familiarity is what makes an icon work. Search Google Images (photos and illustrations too, not only icons), the Noun Project, Iconfinder (filter by small size to drop illustrative app icons). Ad hoc test colleagues: "If I said 'submit a support request', what image do you think of?"
- Standards win even when they are imperfect. The Iconglobe comparison of four real "information" symbols showed variations of a standard were recognised less. The RSS icon became a standard in about a year once Firefox, then IE and Outlook, then Opera adopted it.
- Reasons to leave a standard: licence or trademark (Apple's icons, a share icon bought by a company that changed its licence), confusion with another icon in the same set (magnifier for search and for zoom), or a negative meaning in the audience's culture (owl means wisdom in the west, stupidity in parts of Asia; thumbs up is obscene in Iran).
- Some standards age out (the floppy disk for save); some objects stay robust (the envelope for email); some pictograms drift into arbitrary symbols (the map pin may one day just mean "location").
- Inventing a metaphor: put the concept in the centre of a mind map, branch freely, sketch at each node. For "view" the branches gave glasses, eye, binoculars, magnifier. Binoculars won because it had a unique profile (no confusion with other icons in the UI), was a familiar object that renders without looking like something else, had no negative connotations, and said "view" without many other meanings.
- Checks for a chosen metaphor: is it recognisable or can it be misread (a weight that looks like a handbag, hand dryer pictograms that "dispense bacon")? How much detail does it need, and does that fit the size ("A padlock can still be recognisable at 8px, but a train doesn't stand a chance")? Any negative connotations?
- Avoid letters (they do not translate; the "i" for information is the exception) and body parts (gestures change meaning across cultures).
- Combinations: build a modular system from a base icon plus badges (modifiers). Document plus "+" for add, padlock for private or locked. Put badges bottom right, where the base has natural white space; top right would hide a crucial part of a document. Let the badge break the base outline, which draws attention to the added meaning. Other options: an enclosing shape (a warning triangle around a power symbol, at the cost of a smaller base) or a diagonal bar across the base (mute), as long as the base stays recognisable.
- Appendix badge chart (base plus modifier): octagon = stop, no entry = private, plus = add, minus = remove, closed padlock = locked, open padlock = unlocked, pencil = edit, exclamation mark = error or attention needed, closed eye = invisible, diagonal bar = prevention, off, not allowed.
- Colour reinforces but never carries meaning alone. His table pairs each colour with positive, negative and technical meanings, for example green = go, growth, correct; grey = disabled, off; blue = selected, on, enabled; red = stop, error.

### 3. Drawing (chapter 5)

- His two firm rules for a suite of icons: draw them **in context** (on the real toolbar colour, over photos if they will sit on photos, as hidden layers) and **in company** (all icons in one document on multiple artboards, never one file per icon), because inconsistency in size, colour, weight and style only shows when they sit together. Keep rejected versions off the artboard, never throw them away.
- Tools: sketch first (graph paper notebooks are ideal), then vector with a pixel grid and a pixel preview.
- Sizing: square, even sizes and multiples (16, 32, 48). An odd grid sometimes suits the artwork better: an arrow point on an even grid falls on a gridline and renders as two blunt pixels, while on a 15px grid it falls in the centre of a pixel and stays sharp. An odd grid also lets an element sit centred in a circle.
- Next to text: the icon can be a few pixels larger than the text so it reads clearly without looking obviously bigger (Dribbble's example).
- Optical balance, the most useful numbers in the book: shapes at the same size do not look the same size. "Of all these shapes, the square needs to be the smallest." Rough guide: make a square 75 to 80% of the canvas (24 on a 32 canvas, a 4px margin); the circle overlaps that guide; irregular shapes such as a star or heart may take the whole space; a cross sits in between. A diagonal bar must be shorter than a vertical or horizontal one.
- Optical weight: "Because of anti-aliasing, a 2px line will appear thicker at 45 degrees than when it's horizontal", and rounded corners suffer the same. Tweak by eye, for example a 1px stroke reduced to 0.9px to trim stray subpixels.
- Scaling: icons in several sizes are usually multiples (16, 32, 64). A 1px stroke at 32 must be 2px at 64. Many designers draw the largest first and scale down, but every scaled size still needs hand tweaking.
- Detail: the more detail, the longer the brain takes to decode. "History" as a clock face is clearer simplified, but a phone drawn too simply could be a picture frame or a Kindle and needs its speaker and home button. Other clarity killers: heavy shadows and borders, too much anti-aliasing (often from perspective), straight lines that are not crisp.
- Perspective: icons of 32px or smaller should be face-on, because perspective shrinks the image and adds anti-aliased edges. Some metaphors need a hint of depth (an inbox tray is unrecognisable face-on); keep the front flat and extend only the back, or suggest depth without foreshortening (a wallet, a book).
- Negative space: let the brain complete shapes (the Dribbble bucket shows only the handle's shadow). Suggest form with line weight: thin where light catches top edges, thicker at sides and bottoms.
- Reusing font glyphs (a "?" for help) works at large sizes; at 16px and below, redraw it.
- Worked tutorial (book icon, 32px and 16px): 2px margin so it halves cleanly to 16px; built from rectangles and circles, not strokes, because rectangles land exactly where you want; a 5px wide bookmark rather than 4px so its notch has a true centre pixel (odd width for a sharp point); after scaling to 16, the odd-width part needed hand tweaking.
- Fred LeBlanc's Drawn set: outline first with a 2px round cap round join stroke, then detail lines at 1px, "as few lines as possible", "made like you would make cookies. First, you cut out the shape until it looks right, and then you decorate inside with thin frosting lines." Do not trace (copyright and artistic reasons).
- Colour icons: one consistent light source (top, or top and slightly to one side), gradients light at the top, "if you are aware of the gradient, it's probably too steep", avoid pure black (80 to 90% grey reads more natural). Mostly relevant to app icons, not UI glyphs.
- Testing metaphors: Sebastiaan de With's "mom test" for new concepts like AirPlay: colleagues first, then his mother and his mother-in-law; when they recognised it, it was done.

### 4. Susan Kare (chapter 1 interview)

- She drew the first Mac icons on graph paper, then in a bitmap editor by Andy Hertzfeld that showed the icon at 100% and enlarged side by side.
- For abstract concepts she leafed through Henry Dreyfuss's Symbol Sourcebook; the Command key cloverleaf came from a Swedish campground sign for "interesting feature".
- "If you can do needlepoint, you can design bitmap graphics."
- Her framing of the whole job: "what image can you create in a limited piece of screen real estate to communicate a particular idea at a glance?"

## How this feeds the skill

- `icons/process-and-consistency.md`: the five brief questions, convention first research, the mind map method with its four acceptance checks, the mom test, drawing in company and in context, never throwing away rejected versions.
- `icons/construction-spec.md`: optical balance (square smallest, circle overshoots, irregular shapes take the full area, diagonals shorter), the odd width trick for sharp points, face-on below 32px, badges bottom right breaking the outline.
- `icons/icons.md`: the restraint test (remove it first, the Christmas tree check) as part of the stance.
