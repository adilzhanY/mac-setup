# Logo resolve: how the film arrives at the mark

The end of a commercial is the frame people remember. The user called the Enogon film's ending "the worst thing" in it: the 3D house turned semi-transparent and crossfaded into a growing cube, so for about two seconds the viewer saw two objects at once, each one's inner edges showing through the other. This file is how to do it instead: a catalogue of resolve techniques with real examples, what separates premium from cheap, the rules, and how to resolve to a simple geometric mark (a cube, a ring, a letter).

Sources are linked inline; the full notes are in `research/ad-music-and-logo/notes/logo_reveals.md` and the report beside them. Published frame by frame breakdowns of commercial end frames are rare, so the geometric recipes are built from the documented patterns and marked **(heuristic)**. No source names an "x-ray crossfade" as a failure in those words; the rule against it extends the documented critiques below.

## 1. The rules

1. **The story finishes before the logo move starts.** Toyota's end frame rules: the last shot is art directed for the transition, wide shots are preferred over centred key objects, story action must conclude before the logo transition starts, and there are no cuts during it ([Toyota NZ](https://brandguidelines.toyota.co.nz/tvc-endframe)).
2. **A clean frame before it.** "There should always be at least one clean frame between the graphics and the logo animation" (Toyota NZ, same page). Every title, UI part and label has left the frame before the resolve begins; Toyota also forbids a lock up that has not fully faded when the logo comes in.
3. **One decisive, opaque move.** One object transforms into the mark. Never two images blended by opacity, never a see-through morph, never a dissolve of 3D geometry. While both states are semi-transparent the eye reads an edit, not a transformation (the same family as fading scaffolding lines and letters "washed over" by an effect, section 3).
4. **It decelerates into the mark.** Arrivals slow into rest: WinUI's entrance curve is cubic-bezier(0, 0, 0, 1) ([Microsoft Learn](https://learn.microsoft.com/en-us/windows/apps/design/motion/timing-and-easing)), Material's emphasized decelerate (0.05, 0.7, 0.1, 1.0) ([Flutter](https://api.flutter.dev/flutter/material/Easing-class.html)), Apple's springs are duration and bounce, for example 0.6 s with bounce 0.2 ([WWDC23](https://developer.apple.com/videos/play/wwdc2023/10158/)). Spend the last 20 to 30 percent of the move on the last few percent of the distance, so the mark arrives and settles rather than stops **(heuristic)**.
5. **No secondary sparkle.** No glint, shimmer, particles or lens flare added on top. School of Motion's $7 logo animation was "sparkle engineering. Very standard and stiff" ([School of Motion](https://www.schoolofmotion.com/blog/motion-design-price-difference)).
6. **Hold the still mark 1.5 to 3 s.** A government style guide asks 1.5 s on 15 s ads and 2.5 s on 30 s ads ([Tas Gov](https://www.communications.tas.gov.au/styleguide/p_-_television/30_seconds_and_above)); the Ad Council requires at least 3 s on :15 and 5 s on :20 and longer ([Ad Council](https://www.adcouncil.org/media-standards-guide/television)); Apple films hold the product name about 1 to 2 s and then the logo about 2 s (own measurement in `notes/pacing_and_attention.md`). Viewers leave once they sense the value is over, so keep the end short and do not recap ([Wistia](https://wistia.com/learn/marketing/understanding-audience-retention)).
7. **The sonic accent lands on the landing frame** (or one frame early). Netflix's ta-dum was briefed as "tension and release" in one sound ([MusicRadar](https://www.musicradar.com/news/the-netflix-ta-dum-sound-features-a-reversed-electric-guitar-sample-that-was-created-using-90s-effect-pedals)), and the accent sits where the animation completes ([Cursa](https://cursa.app/en/page/audio-and-final-rhythm-using-sound-to-support-motion)). The motif's last note is on that frame (`composition.md`, section 8).
8. **The move comes from what the mark already owns.** Effects borrowed from outside the identity feel arbitrary; a stroke reveal suits a mark built from lines ([HackerNoon](https://hackernoon.com/how-designers-approach-logo-animation), low authority but consistent with Google and Meta below).

Typical timing **(heuristic)**: the resolve move 0.4 to 0.8 s (a spring of about 0.6 s, bounce about 0.2, or a strong decelerate), then the 1.5 to 3 s hold; the wordmark and tagline enter after the mark has landed, one at a time. UI durations (83 to 600 ms) are tuned for interfaces; an end frame is the film's climax and runs a little slower.

## 2. The catalogue

The best documented resolves treat the logo as something that already moves, so the film comes to rest in its motion rather than adding a treatment at the end.

| Technique | Real example | How it works | Fits |
|---|---|---|---|
| A motion state resolving into the mark | Google 2015: the dots are "a dynamic and perpetually moving state of the logo", moving "along geometric arcs" with "a standard set of snappy easing curves" ([Google Design](https://design.google/library/evolving-google-identity/)); animation was "almost the first part of the design process" ([Motionographer](https://motionographer.com/2015/11/09/interview-motion-design-and-the-google-identity/)) | the product's own working state (dots thinking, a pulse, a gradient) settles into the static mark | products whose UI has a signature state |
| A single line draws it | Meta 2021: the symbol drawn as one continuous line in VR, "to live in motion and 3D" ([Meta Design](https://www.meta.com/design-at-meta/blog/designing-our-new-company-brand-meta/)) | the film's last stroke (a traced wall, a cursor's path) becomes the mark's outline, a trim path decelerating into closure | marks built from lines; drawing products |
| A camera dive | Netflix 2019: the camera flies into the N to reveal a spectrum built from show thumbnails ([Creative Review](https://www.creativereview.co.uk/netflix-updates-its-ident/)) | fly into a detail until it fills the frame, pull out to show it is part of the mark | a mark with a face or an inside |
| The mark hidden in real objects | Mastercard: the two circles in parachutes, drums and sun hats ([Digital Synopsis](https://digitalsynopsis.com/advertising/mastercard-believe-in-experiences/)) | objects of the story line up into the mark | marks reducible to one or two primitives |
| Assembly from its own parts | Dropbox 2017: the box rebuilt as flat diamonds that play against the old 3D reading ([Design Week](https://www.designweek.co.uk/issues/2-8-october-2017/dropbox-rebrands-show-just-file-storage/)); ManvsMachine's More4 mark from triangles flipping like pages ([It's Nice That](https://www.itsnicethat.com/articles/manvsmachine-more-4-identity)) | the mark's own faces or pieces fold, flip or slide together | geometric marks; torq's blades (`elements.md`, Logo build) |
| A living material | Pepsi 2023 "pulse" ([PepsiCo](https://www.pepsico.com/newsroom/press-releases/2023/pepsi-unveils-a-new-logo-and-visual-identity-marking-the-iconic-brands-next-era)); Instagram 2022 gradient "lit from within" ([Meta Design](https://www.meta.com/design-at-meta/blog/behind-instagrams-brand-evolution-movement-inclusivity-and-a-new-purpose/)) | the mark breathes or flows, then holds | brands whose mark is a material |
| A match cut | (no published case study; follows from the match cut technique in `transitions.md`) | the last shot's object matches the mark's silhouette, size and position on one clean frame, then a hard cut | any mark with a clear silhouette |
| A mask or wipe | practitioner guides call it the low risk default ([fastestlogo](https://fastestlogo.com/blog/how-to-animate-a-logo), low authority) | the mark slides out from behind a shape | intricate marks; a fallback, not a concept |

Restraint is the craft. Google's Jonathan Jarvis calls restraint the second biggest challenge, with "a pretty messy cutting room floor", and wants motion "fast, simple, and clear" (Motionographer, above). Microsoft's Fluent gives larger elements more time and keeps linear motion only for constant rotations ([Fluent 2](https://fluent2.microsoft.design/motion)).

## 3. Premium against cheap

School of Motion bought the same logo animation for $7, $150 and $1,000; 84.5 percent of more than 100 blind viewers chose the professional one (School of Motion, above).

| Cheap | Premium |
|---|---|
| "sparkle engineering", stiff template motion, "kinda forgettable" with no concept | one idea that "fit the concept of our brand" |
| "cluttered", "things moving everywhere", "clip-art-ish" | one major action at a time ([Motion Design School](https://motiondesign.school/blog/animation-principles-in-logo-animation/)) |
| an effect "just dropped on top rather than a necessary part of the animation" (an RGB shift); scaffolding lines faded instead of drawn ([r/MotionDesign mirror](https://redlib.ssps.io/r/MotionDesign/comments/1lkcfbj/logo_design_and_animation_for_a_client)) | lines drawn, then removed by being drawn over or folded away |
| letters "washed over" by an effect instead of built by it ([r/animation mirror](https://reddit.birdcat.cafe/r/animation/comments/1igo0gs/what_do_you_think_of_this_animated_logo_im)) | the mark built from its own parts or strokes |
| a morph with poor point correspondence that "turns inside out" (why GSAP exposes `shapeIndex`, [GSAP MorphSVG](https://gsap.com/community/morphSVG)) | a morph with matched points, or no morph at all |
| the object changes shape during a push in; the logo softens as the light moves ([AI Film Contests](https://aifilmcontests.com/guide/ai-commercial-packshot-and-end-card)) | the mark keeps its exact geometry and colours from the landing frame on |
| two images blended by opacity (the Enogon x-ray) | one opaque object transforming for a visible reason |
| linear motion, too much secondary motion, spins ([playbooks](https://playbooks.com/skills/dylantarre/animation-principles/brand-marketing), low authority) | a decelerating ease or a low bounce spring, then stillness |
| an end card too short to read | the 1.5 to 3 s hold |

Motion cannot rescue a generic form: nearly 1,200 earlier logos used Meta's infinity loop ([Dezeen](https://www.dezeen.com/2021/11/03/meta-facebook-rebrand-infinity-loop/)). The mark is what it is; the resolve's job is to make the film arrive at it.

Shrinking a busy product into a small mark fails twice: larger elements need more time (Fluent), and a busy object collapsing to a point has no shape in common with the mark and nothing for the eye to follow **(heuristic)**. Simplify the object first (a house becomes its box), then resolve the simple shape.

## 4. Resolving to a simple geometric mark

Simple geometry is the easiest case for a premium resolve, because the mark can be found in real objects, drawn by one line, assembled from its faces or reached by a dive. The risk is the opposite of a busy logo: the mark is so plain that the motion must carry the identity without becoming decoration. Everything below is **(heuristic)**, inferred from the documented patterns.

**Isometric cube.** Its silhouette is a hexagon and its visible faces are three rhombi. Keep each face's tone constant through the whole move, so it never passes through an incoherent state. Four ways to get there from a 3D product (a house, a device, a room):

| Approach | How it works for a house to an isometric cube | Sound |
|---|---|---|
| Match cut on the isometric axis | As the house settles, move the 3D camera to the true isometric view (equal foreshortening on three edges; a long lens or a dolly zoom flattens the perspective), scale and centre it so its massing fills the cube's hexagon, then cut on one clean frame to the flat mark | a hard cut on a downbeat, the button on the first frame of the mark |
| Collapse into its own faces | Fade nothing. Roof, walls and floor slabs fold or slide as opaque planes into the three rhombi, each face keeping a constant tone (like Dropbox's flat faces) | one material sound (wood, a paper or card fold) that becomes the motif's last note, Randy Thom's metamorphosis ([filmsound.org](http://filmsound.org/articles/designing_for_sound.htm)) |
| Camera dive | Fly into one corner of the building until a face fills the frame, then pull out to reveal it is the cube's face | a riser of one to two bars, a short suck back, the button on the reveal |
| A single line draws it | The building's outline, or the cursor's last stroke, becomes the cube's edges as a trim path, decelerating into closure | the accent on the frame the stroke closes |

All four share the rules of section 1: the story action ends first, a clean frame separates any UI or text from the logo move, the move is one decisive motion on a strong decelerate or a low bounce spring (about 0.6 s, bounce about 0.2), there is no secondary sparkle, the sonic accent lands on the landing frame (or one frame early), and the still mark holds about 1.5 to 3 s.

**Ring.** A match cut from any circular object of the story (a lens, a cup rim, a wheel, a plate: torq's plate ring became its rest timer, `transitions.md`) with matched diameter and centre; or draw the ring as one stroke, a trim path from 0 to 100 percent on a decelerate curve so the closing gap slows into contact, with the sonic accent on the frame the stroke closes.

**Letter.** Draw it as its own stroke skeleton, never washed in by an effect; or let the film's last line (a traced wall, a typed caret, the cursor's path) become the stroke.

**Hand over from 3D to the flat mark.** At the swap frame the 3D object and the flat SVG must match to the pixel: project the 3D corners at that frame, size the SVG to that box, and grow the 3D ink width to the logo's stroke width at that size (Enogon: `cubeRect.ts`, `lessons.md`). Then the swap is invisible and needs no fade.

## 5. The Enogon lesson

**What failed (mgpro 2.0.0, 35.0 to 36.8 s).** The house's materials went transparent and its opacity fell while a cube grew inside it with rising opacity. For the whole move both objects were half visible: the house's walls, slabs and roof edges showed through the cube and the cube's edges through the house. The user called it "the worst thing" in the film. Causes: the skill had a "do not fade 3D geometry with transparency" rule in `transitions.md` but no rule for the logo resolve, and no review check for blends between states.

**The rebuild.** Export packs the model. The box's net is drawn flat on the ground around the house: the floor and four side panels grow out from their hinges (14 frames, ease out). The four sides fold up one after another, 7 frames apart, each on the `settle` spring (a closing box is a result, so a tiny overshoot is allowed). The lid closes last, on its own `settle` spring. Every panel is opaque and coloured like the logo cube from the start (top apricot, east Türkis, south white, the hidden sides lighter Türkis), with black ink edges whose width grows to the logo's stroke width by the swap frame. The house stays solid inside the box and is removed only once the lid has closed over it. The closed box is the Enogon cube; at the swap frame it hands over to the flat SVG logo exactly (`cubeRect.ts`). The export title leaves 4 frames before the net appears (the clean frame), and the whole pack, from the first panel to the closed lid, takes about 1.7 s, then the mark holds while the wordmark, the line and the URL enter one at a time. The sound for it **(heuristic, the planned design)**: a quiet card or paper fold per side as support, and the sonic logo, the motif's last note on a recorded tactile hit, on the frame the lid closes. Code: `PackBox` in `~/dev/enogon-video/src/Scene3D.tsx` (the recipe is in `elements.md`, Box fold into a cube mark).

The general lesson is wider than logos: the Enogon review found the same mistake four times, a change shown as a blend between two states instead of one thing transforming for a visible reason (`lessons.md`, Enogon review). An opacity crossfade between two objects is the picture's version of a gain hole in the music.

## 6. Check the resolve

- [ ] Every title, label and UI part is gone at least one frame before the resolve starts.
- [ ] No frame from the start of the resolve to the hold shows two objects or two scenes at partial opacity (step through every frame of the move; grep the resolve's code for `opacity`, `transparent: true` and `mix(` on materials).
- [ ] One move, decelerating into rest; nothing added on top (no glint, no particles).
- [ ] The mark's geometry and colours exact from the landing frame on; the 3D to 2D swap invisible.
- [ ] The sonic accent on the landing frame (measured onset within 1 frame at 30 fps, 2 at 60).
- [ ] The still mark holds 1.5 to 3 s before the wordmark and line (or together with them) and the film ends.
