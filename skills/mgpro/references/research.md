# Research notes (with sources)

Research before building when the user asks for it, or when the brief brings something the notes below do not cover (a new genre, a platform convention, a style). Cite sources in the reply. What was learned so far:

## Apple style motion

- Restraint: whites, soft greys, blacks; saturation only for one or two focus elements; one element moves at a time; 2 to 3 font weights at most.
- Timings: hover 100 ms, press 150 ms, modal 250 ms, page 350 ms; general UI 300 to 500 ms. Curve cubic-bezier(0.4, 0, 0.2, 1), velocity peak about 60 percent through.
- Subtle scale 94 to 100 percent, motion along Z (depth), not just XY.
- Glass: blur 15 to 25 px frosted, surface 8 to 15 percent, 1 px white border at 30 percent, inner shadow, radial highlight white 20 to 5 percent, tiny rotations of 2 degrees.
- Sources: https://trydemotion.com/blog/apple-style-ui-motion-graphics, https://trydemotion.com/blog/after-effects-advanced-techniques, https://trydemotion.com/blog/apple-style-animation-guide

## Kinetic typography and After Effects techniques

- Per word or per character animators: position plus opacity with ease out, staggered; match motion speeds across a handoff; trim paths for line reveals; physics based easing with slight overshoot for organic motion.
- Sources: https://schoolofmotion.com/blog/kinetic-typography-after-effects-part-3, https://www.linearity.io/blog/kinetic-typography/, https://trydemotion.com/blog/trending-motion-graphic-styles

## Apple Intelligence glow

- A conic gradient sweeping around the edge (a linear one looks wrong on rounded rectangles), two layers: blurred glow plus sharp rim; colour order blue, violet, coral, amber; about 1.8 s per turn.
- Sources: https://mackrichardson.com/blog/apple-intelligence-animated-border/, https://dev.to/vector4wang/i-recreated-iphones-apple-intelligence-edge-glow-effect-on-mac-57f5

## Cursors

- Screen Studio smooths recorded cursor paths with bezier interpolation and spring easing; zooms use springs with optional motion blur.
- Multiplayer cursors: CSS transitions are straight lines; springs carry momentum; splines are the most accurate.
- Sources: https://screen.studio/, https://liveblocks.io/blog/how-to-animate-multiplayer-cursors, https://animations.dev/learn/animation-theory/spring-animations

## Music for commercials

- Upbeat ads: 100 to 140 BPM (product launches 100 to 120), major keys, bright instruments; claps and finger snaps over a modern beat, funky bass, plucky synths, soft piano; keep the arrangement uncluttered and the mids clear.
- Sources: https://www.foximusic.com/blog/upbeat-music-for-a-commercial-glossary-guide/, https://uppbeat.io/music/category/commercial

## Sound design for motion

- Sync every cut, fade and movement to an audio cue; synthesize in code for exact timing; whooshes for shape moves, soft clicks for text reveals; layer effects, ambience and music.
- Sources: https://nobledesktop.com/blog/the-role-of-sound-design-in-motion-design, https://www.motiontheagency.com/blog/sound-design-examples-before-after-in-motion

## Music identity (Oct 2026, after the Sendoku film)

- Earworms: a common global contour (rise then fall) plus an unusual interval or extra repeated notes, and a faster tempo, predicted which songs stick (Jakubowski et al.). Used in `theory.motif`. https://www.livescience.com/56739-what-makes-an-earworm-so-catchy.html
- Euclidean rhythms generate most world music timelines (tresillo E(3,8), cinquillo E(5,8)); rotate to move the downbeat. https://en.wikipedia.org/wiki/Euclidean_rhythm and https://cgm.cs.mcgill.ca/~godfried/publications/banff.pdf
- Genre grooves: UK garage swing and 2-step kick (https://theproducerschool.com/blogs/featured-blogs/how-to-program-uk-garage-drums-complete-guide-for-producers), dembow (https://www.ujam.com/tutorials/how-to-make-a-dembow-groove/), Jersey club kick (https://blog.native-instruments.com/jersey-club/), amapiano log drum at 108 to 115 BPM, FM based, in call and response with the kick (https://articles.roland.com/?p=67237, https://violetrecording.com/how-to-make-amapiano-beats/).
- Karplus Strong plucked strings in numpy: https://kennethreitz.org/essays/2026-03-29-numpy_as_synth_engine
- Audio logos: a 2 to 5 s mnemonic drawn from the brand's theme; design the system first, the mnemonic second (Intel's five notes). https://killerspots.com/blog/build-consistent-sonic-brand-system and https://www.creativebloq.com/features/audio-logos
- Short form editing: cuts synced to beats and drops; muted viewing is common, so the picture must work without the music, and the music must still earn the viewers who hear it. https://ueaeprints.uea.ac.uk/id/eprint/70746/
