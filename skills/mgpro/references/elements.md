# Drawn elements: recipes

Build these from the product's own tokens (colours, radius, font, its icon set). Hero size, isolated, floating. Shadows and glass on light brands; on dark brands, surfaces in the product's surface colour with a 1.5 px line border and the accent for everything that is alive. Code: `templates/kit/src/kit.tsx`; Bauwerk elements in `templates/examples/bauwerk/src/` (Search, Facade, HeroAct, PlanSheet, EndAct); torq elements in `templates/examples/torq/src/`.

# Light brand, desktop, AI (Bauwerk)

## Liquid glass panel

- Background: linear gradient white 78 to 58 percent (dark variant: rgba(40,52,70,.62) to rgba(22,30,44,.58)).
- `backdrop-filter: blur(28px) saturate(170%)` (works in Remotion over a WebGL canvas).
- Rim: `inset 0 1px 0` white 95 percent plus `inset 0 0 0 1px` white 60 percent.
- Shadow: `0 1px 2px rgba(13,33,55,.06), 0 28px 64px -18px rgba(13,33,55,.32)`.
- Specular light: a radial gradient of white 70 percent at 18 percent x, 0 y, fading by 55 percent.
- Radius 28 for cards, 999 for pills. From research: glass opacity 8 to 15 percent and blur 15 to 25 px for the frosted look, 1 px white border at 30 percent.

## AI glow (Apple Intelligence style)

Two layers behind and around the element: a sharp rim (3 to 5 px) and a wide blurred glow (blur 36 to 48 px, opacity about 0.85), both a `conic-gradient(from <angle>deg, #3d7bff, #a855f7, #ff5c8a, #ffb547, #3d7bff)`. The rim uses the mask trick: `mask: linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0); mask-composite: exclude` with padding equal to the rim width. Rotate the angle with the frame (one turn per 110 frames, about 1.8 s). Fade its strength in over 20 frames when the AI starts and out when it finishes. Inside a corner-pinned layer it follows the 3D plane.

## Floating search pill

820 x 96 px, radius 999, centred over a blurred map. Opens from a 96 px dot: width spring pop, height spring settle 4 frames later. Search icon pops at frame 14. Placeholder in muted grey fades in, then on focus slides up 14 px into a 6 px blur. Focus ring: 3 px navy at 56 percent plus a 9 px halo at 10 percent, springing in. Typed glyphs rise out of a blur on their key cues. Result card unfolds below (height animates from 14 px, rows enter 5 frames apart): a 60 px navy circle with a Lucide MapPin, title 31 px 600, subtitle 22 px muted, a chip on the right ("LoD2 · 5 floors"), a dimmer second row to show it is a real search. Hover tint 7 percent navy on the row before the click.

## Map pin

Teardrop SVG path (navy fill, 3 px white stroke, drop shadow) with the Lucide MapPin glyph inside. Lands with spring pop from 40 px above, a ground ripple (ellipse 0.62 aspect, border 3 px navy, grows to 160 px and fades over 40 frames). Rides on top of the building as it rises (projected from the 3D roof point every frame), fades out after about 1.5 s.

## Old paper plan (for the AI to read)

SVG at 40 px per metre: paper #efe4cb with fractal noise multiplied in, an ageing radial gradient to #b89a68 at the edges, two coffee stains, a fold line with a highlight. Ink #4d3a2b at 88 percent through a slight displacement filter (wobble scale 2.2) so lines look hand drawn. Exterior walls as a hatched poche (evenodd path between outline and its 0.4 m inset, 45 degree hatch pattern). Interior walls as thick strokes (thickness x scale). Window breaks in the wall with two thin lines, door arcs, dimension chains with tick marks and italic serif numbers ("4,41"), old German room names (Stube, Küche, Kammer, Laden, Abort), a title block ("ERDGESCHOSS", "M 1:100"). When the AI starts, dim the paper (brightness 0.38, saturate 0.5) so the light lines pop.

## AI tracing (trim paths with a spark)

Each wall is three stacked strokes: violet glow (16 px, 55 percent, Gaussian blur 5), lilac (6 px), white core (2.5 px), all with `stroke-dasharray: L L` and `stroke-dashoffset: L(1 - t)`, t over 13 frames expo out. A spark rides the head: a radial gradient circle (white to lilac to transparent violet), radius 16 to 24, fading 10 frames after the wall completes. Walls start on 32nd notes: outer walls first, then inner walls, then door swings drawn as dashed arcs. Rooms flood from their centroid: a `clipPath` circle growing over 16 frames on 16th notes, fills in soft distinct colours at 42 percent. Labels (dark glass pills, name 21 px, area in mono counting up) pop at the room's centroid, projected from 3D, upright.

## Facade photo (drawn)

A phone-photo framed card (640 x 880, radius 26) with sky gradient and clouds, neighbour facades cut by the frame, the brick facade (SVG brick pattern: courses 5.4 px, mortar lines at 45 to 55 percent), stucco bands at every storey, a cornice with a shadow line, a stone plinth, the gable with a round attic window, every window from the real data (white frame, glass gradient reflecting the sky, cross mullion, lintel cap, sill), doors in dark wood with glass, pavement, a vignette.

## Scan and detection

- Scan beam: a 3 px lilac-white line with violet glows (0 0 18px 6px and 0 0 60px 20px), a 70 px violet gradient trailing above it. Below the beam the photo waits: dark overlay 42 percent with 3 px backdrop blur and desaturation; above it the photo is clear. The beam's position is keyed so it crosses each row exactly as that row's detections fire.
- Detection per window: four corner brackets (white 3 px, round caps, arm min(16 px, 30 percent of width), glow drop shadow) flying in from 1.35x scale over 9 frames expo out, a violet mask pulsing from 60 to 20 percent opacity over 18 frames. 30 detections at 2.5 frame spacing reads as one fast run. A few measurement labels ("0.98 × 1.60 m", mono 18 px, dark chip with lilac rim) pop on chosen windows.
- Counter: dark glass card with the AI gradient badge (Lucide Sparkles), a big mono number ticking with each detection, a two-line label ("windows / and doors").

## Presence bar

Glass pill at the top centre: overlapping avatars (44 px circles in each person's presence colour, white initials, 3 px white ring), each popping in on its join cue with its width growing so the row reflows; a green live dot whose halo breathes (3 + 3 sin(f/9) px); "3 editing".

## Chat

Glass panel (450 wide) in the right column with the project name as header. Each message: a typing bubble first (three 10 px dots bouncing: translateY -5 x max(0, sin((f - start)/4 - i 0.9))), then the message springs in from the bottom left (scale 0.9 to 1, 18 px rise). Bubble white, radius 22 22 22 8, text 25 px, sender name in their colour 17 px above. Messages are short and human: "Facade is in. Insulate the walls?" / "16 cm. Doing it now." / "Triple glazing too."

## Slider being dragged by a collaborator

Glass card: label left, value right in mono navy ("14 cm"). Track 6 px, navy fill, 30 px white thumb with a coloured halo (the dragger's colour at 25 percent) while held. The remote cursor's drag uses the same easing as the value and the tick sounds (cubic in-out over 60 frames). The 3D change follows the value live (plaster wiping up the facade with a bright edge line at the wipe height).

## Toggle

72 x 42 track, 34 px knob, spring pop on the click, track colour switches to navy at half way. The 3D change follows (glass tint lerps to cool blue, a diagonal light sweep runs across all windows over 40 frames).

## Energy class badge with a slot roll

Square badge in the official class colour with the letter in the matching ink (dark or white by contrast). On each change: the old letter moves up 0.75 x size into a blur and fades while the new one comes up from below out of a blur over 10 frames expo out; the background colour interpolates between the two class colours. Next to it a mini scale of all classes, the current one full opacity and 1.6x taller.

## Payoff

Centre: "From G to B." at 110 px with G in its red and B in green, the two badges at 170 px popping in 14 frames apart, an arrow drawn between them (trim path, 18 frames), the saving counting up in mono green ("−75 % energy") over 42 frames. Behind: the 3D scene defocused.

## Document (the deliverable)

A white page (600 x 760, radius 14, deep shadow) with a second page peeking behind (offset 22, -18, rotated 2.5 degrees). Content: a small icon title ("Renovation roadmap (iSFP)"), the address at 36 px, a meta line, the class path G to D to C to B with arrows, step rows (colour bar, year in mono, step name, class badge) entering 6 frames apart, grey placeholder text bars. A pill button "Send PDF" that the cursor clicks; it presses to 0.95 and turns green with a check and "Sent".

## End card

White radial stage, the logo mark built from blocks (spring pop scaleY from the base, 5 frames apart), the wordmark at 156 px rising out of a slot, the tagline word by word in muted 54 px, the URL in a navy tinted pill (hover state when the cursor arrives: tint and ring strengthen), a small credit line at the bottom. Slow drift in scale.

## Finishing layers

- Grain: an SVG `feTurbulence` (fractalNoise, baseFrequency 0.85, 2 octaves, seed = frame) desaturated, overlay blend, 4 to 5 percent.
- Vignette: radial gradient to rgba(13,33,55,.12) at the edges when the frame needs focus.
- Backdrops that breathe: two soft radial light pools (navy and violet at 8 to 10 percent) drifting with slow sines.

# Dark brand, mobile, no AI (torq)

## Set rows (a live logger)

Exercise title (54 px bold), a faint caps header (SET, PREVIOUS, KG, REPS, a check icon), rows 112 px tall: set number in a 76 px surface square, previous value faint, KG and REPS cells (76 px tall, surface fill, 1.5 px line inset, values 40 px), a 76 px check box. Values start in the faint colour (prefilled ghost values) and turn ink on the tap. The tap: box presses, fills with the accent on a pop spring, the check icon scales in, a soft accent glow decays, the row washes with the accent from left to right over 16 frames (a moving gradient stop) and settles at 5 percent. Four ticks on 8ths. A record set gets a pill (the product's PR colour, trophy icon) popping beside the check with a small rotation from -14 degrees.

## Rest timer ring

SVG circle, 10 px stroke in the accent over a dark track (the accent burned down, torq's #26320C), `stroke-dasharray` for the remaining fraction, round cap, rotated -90 degrees, a drop shadow glow. Inside, the time (92 px bold, tabular) and a caps label; the label becomes a 3, 2, 1 on the ticks; at zero the time turns "GO" in the accent with a 12 percent scale bump and a brighter glow.

## Particle distribution (a population forming)

The strongest data shot so far. From a real quantile table (torq: OpenPowerlifting bench DOTS at 1 to 99 percent): build a CDF by piecewise linear interpolation, take per bin probabilities over about 50 bins, smooth them with a 5 tap kernel (0.06, 0.24, 0.4, 0.24, 0.06) so the quantile steps vanish, and allot N particles (2200) by bin. Each particle gets a column slot (two sub columns per bin), a stack row, a land frame (`start + row x 2.4 + random x 9`, so the curve grows bottom up as a wave) and a start height above the frame; it falls with gravity (t squared) over 22 frames drawn as a vertical streak whose length follows its speed, then lands as a 9 px rounded square that flashes bright for 10 frames and settles grey. Draw everything on one `<canvas>` in `useLayoutEffect` keyed on the frame, with a deterministic hash for randomness (never `Math.random`). A counter of the population counts up in sync. Then "you" (a dot carried in from the previous scene) drops onto the axis with a ripple, a vertical accent line rises from it, and every particle left of it lights in the accent in a wave running toward the line (8 frames per particle, delayed by its distance); a pill on the line says the value. Source line in faint type in the corner.

## Leaderboard with an overtake

Five rows (rank, the product's flat badge, initials avatar in a colour, name, handle, top lift, points). The viewer's row has an accent outline and wash. Points count up (ticks every 3 frames); when they pass the row above, the rows trade places on a "settle" spring while the viewer's row lifts (scale 1.025, a shadow, a stronger outline) and the passed row steps back (opacity 0.45, 2 px blur, scale 0.97) for the moment they cross. Draw rows in an order that keeps the viewer's row on top.

## Push notification

A dark card (surface gradient, 1 px line inset, deep shadow, radius 16) drops from above the frame on a settle spring: the product's badge, "PRODUCT · NOW" in faint caps, one line with the key word in the accent. The event it announces also happens on screen (the friend's badge pops to the new tier). Leaves up 40 px into a blur.

## Week dots and a streak

Seven 104 px circles on surface with a line ring, day letters below; each fills with the accent on a pop spring on 8ths with a decaying glow, the letter turning ink. A pill below (accent tint, accent ring, a flame icon) whose number slot rolls to the next value on the last hit.

## Flat rank badge

Pointy top rounded hexagon (corners by quadratic curves), the tier metal as a light to base to dark diagonal gradient, a darker inner hex field, the product mark in the tier's light colour. The same drawing at every size; it is what the 3D medal becomes in lists (`Badge.tsx`).

## Line chart of progress, with a riding head

Catmull-Rom through monthly values as explicit cubic segments, so the head can be evaluated exactly on the curve (a head interpolated linearly between knots floats off the line). Reveal with a clip rect that follows the head's x (line, a 14 px blurred glow copy, an area gradient fading down), a white dot with an accent glow riding the head, record points popping in the PR colour with a ring when the head passes them (place them on cue frames by moving the head at a fixed number of frames per month), a pill with the final value. The big number above counts the best value so far, one tick per unit, generated in `cues.py` from the same head formula, so it can never run ahead of the line.

## Logo build from its own paths

Split the mark's SVG path at each `M` into its parts (torq's vortex: six blades). Each part springs from scale 0 around the mark's centre with a rotation from -50 degrees, 4 frames apart, while the whole mark spins in from -150 degrees with an expo out over 64 frames (torque made literal). The wordmark then slides out of a widening clip beside it, rising 110 percent out of a blur, and a sheen (a moving linear gradient fill) crosses the mark on the bell.

## Counter with a slot roll

The old number moves up into a blur and fades while the new one rises from below out of a blur (12 frames expo out) inside an overflow hidden box that is taller than the glyphs (descenders and the cap height clip otherwise), plus a 6 percent bump on each change.
