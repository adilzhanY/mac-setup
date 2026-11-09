# Cursor animation in product demos, launch films and SaaS ads

Scope note: the most precise numbers in this file come from open source code (Cap, the open source recorder that says it is inspired by Screen Studio, and a Screen Studio effects clone ported from Cap), plus one published house style for launch videos (HeyGen HyperFrames "oversized cursor"). The commercial tools (Screen Studio, Tella, Canvid, FocuSee, Arcade) publish their option names but almost never their numbers. Treat any Screen Studio number below as "what its open source imitators use", not as Screen Studio's own value.

## 1. Tools and their look: what parameters they expose and their defaults

### Takeaway
Every serious recorder converges on the same kit: a re-drawn vector cursor at 1.5x to 3x size, spring smoothing of the raw path (presets from "smooth/slow" to "rapid/snappy" plus custom tension and friction), a press shrink of about 0.8x over roughly 100 to 130 ms, an optional ripple, a small tilt in the direction of horizontal travel, directional motion blur, idle hide with a fade, auto zoom driven by clicks, and a "return to start" loop. Cap's source gives the only hard defaults: cursor spring tension 470, mass 3, friction 70 (about 150 ms of lag), click shrink to 0.8 over 130 ms with smoothstep, tilt capped at plus or minus 20 degrees, idle fade 400 ms.

### Cited Findings

Screen Studio (macOS, the reference look)
- Marketing claim: the app "automatically zooms in on your cursor, increases the cursor size and smooths its movements". [Screen Studio guide index via search](https://screen.studio/guide/cursor)
- Cursor options: Hide cursor, Cursor size, Cursor type (macOS or Touch, Touch used for iPad and iPhone recordings), Always use default system cursor (do not switch to I-beam etc.), Hide cursor if it's not moving, Loop cursor position ("Near the end of the video, cursor will move back to its initial position"). [Screen Studio: Cursor](https://screen.studio/guide/cursor)
- Advanced cursor options: Rotate cursor while moving ("slightly rotates the cursor to mimic chasing the mouse"), Stop cursor movement at the end of the video, Remove cursor shakes, Optimize original cursor types (reduces rapid cursor type changes). [Screen Studio: Cursor](https://screen.studio/guide/cursor)
- Cursor animation style presets: Smooth, Medium, Rapid, None. Motion blur is one strength slider with advanced per-channel options for "Cursor movement", "Screen zooming in" and "Screen moving". Screen animation has "Focused" (settles quickly, easier to read) and "Smooth" (more fluid, for creative content not meant for reading). No numeric values are published. [Screen Studio: Look and Feel / Animations](https://screen.studio/guide/animations)
- Smooth mouse movement can be disabled for a specific fragment of the timeline, recommended when recording drop down menus. [Screen Studio: Disable smooth mouse movement](https://screen.studio/guide/disable-smooth-mouse-movement)
- Cursor can be hidden per section of the timeline. [Screen Studio: Hiding the cursor in specific sections](https://www.screen.studio/guide/hiding-the-cursor-in-specific-sections)
- Auto zoom is click driven: it "automatically detects the click positions and zooms in on those areas"; a zoom placed where no click happened will not zoom anywhere. [Screen Studio: Auto zoom](https://screen.studio/guide/auto-zoom)
- A user feedback post complains that the auto zoom range starts too late before clicks and ends too soon after them, and that defaults cannot be tuned globally (user request, not official doc). [Screen Studio Hub](https://hub.screen.studio/p/custom-settings-for-default-automatic-zoom-range)
- Screen Studio 3.0 (Dec 2024) added custom cursors and click effects. [AlternativeTo](https://alternativeto.net/news/2024/12/screen-studio-3-0-launched-with-shareable-links-dynamic-layouts-command-menu-and-more)
- Third party tutorial says cursor size is a slider relative to screen resolution and that there is a "Hide delay" for idle hide (non official, labels may differ). [TemperStack](https://www.temperstack.com/learn/screen-studio/adjust-cursor-animations/)

Cap (open source, "inspired by Screen Studio"): actual defaults from source code, CapSoftware/Cap, read 2026-10-29
- Cursor smoothing presets (tension, mass, friction): Slow 200 / 2.25 / 40; Smooth 80 / 2.5 / 28; Mellow (default) 470 / 3.0 / 70; Fast 380 / 1.0 / 30; plus Custom. Legacy names "regular", "quick", "rapid" alias to Mellow. [Cap configuration.rs](https://github.com/CapSoftware/Cap/blob/main/crates/project/src/configuration.rs)
- Click spring (used near clicks): tension 530, mass 1, friction 40, applied within a 175 ms window of a click, with a 500 ms click lookahead so the cursor arrives on the click target. Drag spring: tension 1000, mass 1, friction 40. [Cap cursor_interpolation.rs](https://github.com/CapSoftware/Cap/blob/main/crates/rendering/src/cursor_interpolation.rs)
- Code comment: a spring chasing a moving target trails it by friction/tension seconds at steady state (independent of mass), so the Mellow default lags about 149 ms. Shake removal threshold 0.015 of the frame within a 100 ms window; simulation step 1/60 s. [Cap cursor_interpolation.rs](https://github.com/CapSoftware/Cap/blob/main/crates/rendering/src/cursor_interpolation.rs)
- Cursor config defaults: size 100 (percent), hide_when_idle false, hide_when_idle_delay 2.0 s, motion_blur 1.0 (one slider drives both cursor and screen blur), rotation_amount 0.15, base_rotation 0, SVG cursor rendering on. [Cap configuration.rs](https://github.com/CapSoftware/Cap/blob/main/crates/project/src/configuration.rs)
- Click press: CURSOR_CLICK_DURATION 0.13 s, CLICK_SHRINK_SIZE 0.8, eased with smoothstep both into the press (before mouse down) and out after mouse up; the cursor stays shrunk while the button is held. [Cap layers/cursor.rs](https://github.com/CapSoftware/Cap/blob/main/crates/rendering/src/layers/cursor.rs)
- Idle: minimum 500 ms before hiding, 400 ms fade out, and the cursor starts reappearing 250 ms before movement resumes (lookahead). [Cap layers/cursor.rs](https://github.com/CapSoftware/Cap/blob/main/crates/rendering/src/layers/cursor.rs)
- Motion blur: smear length equals the cursor's per frame travel times the user amount, linear, normalized to 60 fps (120 fps needs 2x to keep the same real time shutter), max strength 4, capped at 480 px only to stop teleports. [Cap layers/cursor.rs](https://github.com/CapSoftware/Cap/blob/main/crates/rendering/src/layers/cursor.rs)
- Tilt: degrees = (horizontal pixels travelled over the last 0.4 s) x 0.03 x rotation_amount (default 0.15), clamped to plus or minus 20 degrees. [Cap rendering lib.rs](https://github.com/CapSoftware/Cap/blob/main/crates/rendering/src/lib.rs)
- Click ripple defaults: off by default, color RGB 71,133,255, strength 0.7 (range 0 to 1), size 1.0 (range 0.25 to 3), duration 0.6 s (range 0.2 to 1.5 s). [Cap configuration.rs](https://github.com/CapSoftware/Cap/blob/main/crates/project/src/configuration.rs)
- Screen movement (camera) spring default: stiffness 200, damping 40, mass 2.25. [Cap configuration.rs](https://github.com/CapSoftware/Cap/blob/main/crates/project/src/configuration.rs)

Screen Studio effects clone (ported from Cap, older values)
- Cursor springs: default tension 170, mass 1, friction 20 (damping ratio about 0.77); snappy 700 / 1 / 30 (about 0.57) used within 160 ms of clicks; drag 136 / 1.2 / 26 (about 1.02). Viewport springs: focused 300 / 6.75 / 120 (about 1.33), smooth 240 / 3.375 / 80 (about 1.40). Viewport pans only when the cursor leaves the inner 70 percent safe zone; 1 s lookahead for jitter cancellation; pan target averages 0.5 s of future positions; auto zoom "silence" = displacement under 2 px for at least 0.5 s; zoom in slightly bouncy, zoom out softer and more damped. [Screen-Studio-Effects README](https://github.com/pythonlearner1025/Screen-Studio-Effects)

Tella
- Options: style (macOS Sequoia, Tahoe, Golden Gate, Windows, Touch) and size; Smooth movement (adjustable); Movement tilt ("subtle lean during horizontal motion", off by default, for launch style clips); Click spring (shrink then spring back, off by default); Click ripple (adjustable size); Hide when inactive (fade); Return to start. [Tella blog](https://www.tella.com/blog/animated-cursors-for-screen-recordings), [Tella llms.txt](https://www.tella.com/animated-cursors/llms.txt)
- Size guidance: 2x default for full screen laptop recordings, 2.5x to 3x for social clips watched on phones, about 1.5x in deep UI zooms so the pointer does not cover the target. A big cursor in a 250 percent+ zoom hides labels. [Tella blog](https://www.tella.com/blog/animated-cursors-for-screen-recordings)
- Presets: Product demo (30 to 60 s): Sequoia, 2.5x, smoothing medium high, tilt on, spring on, ripple on, "Snappy" animation. Software tutorial (5 to 20 min): 2x, smoothing medium, ripple on, spring off, tilt off, hide when inactive on, "Gentle" animation. Mobile: Touch, 2x, smoothing high, larger ripple. [Tella blog](https://www.tella.com/blog/animated-cursors-for-screen-recordings)
- Higher smoothing for slow narrated tutorials, lower for fast demos where the pointer should feel responsive. [Tella blog](https://www.tella.com/blog/animated-cursors-for-screen-recordings)

Canvid
- Cursor smoothing on by default for all new recordings. Styles Windows, Mac, Touch, Recorded. "Always use pointer style" (no hand or I-beam swaps) off by default. Click effect = ripple. "Tilt cursor with movement". Movement animation style: four presets or custom tension and friction. [Canvid cursor editor](https://www.canvid.com/support/editing/cursor-editor), [Canvid cursor smoothing](https://www.canvid.com/support/editing/cursor-smoothing)
- Zoom: auto mode follows the cursor, manual picks an area; four zoom animation presets "from smooth to snappy", tension and friction settable; adjustable motion blur. [Canvid auto/manual zoom (search summary)](https://www.canvid.com/features/auto-manual-zoom)

FocuSee, Cursorful, Arcade, Recordly, others
- FocuSee: auto zoom detects clicks and generates zoom animations after recording; Cursor tab has size, color, style, click animation, click sound. [FocuSee features](https://focusee.imobie.com/features/auto-zoom-and-cursor-animation.htm)
- Cursorful: browser based recorder advertising automatic zooms and pans from clicks with editable zoom position, depth and timing. [Cursorful](https://cursorful.com/), [FocuSee comparison](https://focusee.imobie.com/compare/cursorful-alternative.htm)
- Arcade (interactive demos, not video): pan and zoom with easing styles Gentle, Quick, Slow and a delay before zoom; if frame size is unchanged between steps it pans instead of zooming; auto pan and zoom added where it detects a large area or hotspot; hotspots are created at every click. No cursor animation settings documented. [Arcade docs](https://docs.arcade.software/kb/build/interactive-demo/edit/pan-and-zoom)
- Recordly (open source fork of OpenScreen): cursor size, smoothing, motion blur, click bounce, "sway", loop mode, macOS style cursor assets drawn with PixiJS over footage. [Recordly](https://github.com/nonomal/Recordly)
- CineScreen fork: "glide" with critically damped spring, presets slow, mellow, quick, rapid. [search summary of CineScreen](https://github.forks.workers.dev/jasonzh0/CineScreen)
- Framer "Smooth Arrow Cursor": spring follow (stiffness, damping) so it trails the mouse, and rotates toward the direction of travel. [Framer marketplace](https://www.framer.com/marketplace/components/smooth-arrow-cursor)
- Camtasia 2025: cursor path editing and smoothing, cursor scaling for busy screens. [TechSmith webinar](https://www.techsmith.com/learn/webinars/making-the-cursor-the-hero/)

### Inferences
- Damping ratios computed from Cap's presets (zeta = friction / (2 x sqrt(tension x mass))): Slow about 0.94, Smooth about 0.99, Mellow about 0.93, Fast about 0.77, click spring about 0.87, drag spring about 0.63. So the default cursor glide is almost critically damped (no visible bounce), and only the click and drag springs are allowed a little overshoot. Steady state lag (friction/tension): Slow 200 ms, Smooth 350 ms, Mellow 149 ms, Fast 79 ms.
- Tilt is small in practice: with Cap's formula a 1000 px horizontal move inside 0.4 s at 1920 width gives 1000 x 0.03 x 0.15 = 4.5 degrees. The plus or minus 20 degree clamp only matters for flicks. A good working range for a code cursor is 3 to 8 degrees, never constant, and decaying back to 0 when it stops.
- Press feel consensus: scale 0.8 to 0.84, press 100 to 130 ms, release about twice as long (spring or ease out). Ripples last about 0.6 s.
- Remotion's spring() takes the same stiffness/damping/mass trio, so Cap's preset numbers can be pasted in directly (Mellow: stiffness 470, mass 3, damping 70). This is an inference from matching parameter names; verify the integration matches.

### Gaps
- No official numeric defaults for Screen Studio (spring values, default size, auto zoom level, zoom lead-in and lead-out times). Only option names are published.
- Rotato: no source found describing cursor features; it appears to be a device mockup tool rather than a cursor tool.
- Cursorful and FocuSee: no numeric defaults found.
- Canvid's four preset names and values were not published on the pages fetched.

## 2. Motion: human mouse movement models and how designers stylize them

### Takeaway
Real pointing is a fast ballistic move with a bell shaped speed profile (minimum jerk: peak speed at mid move, 1.875x the average speed), followed by small corrective submovements, often after an undershoot; the duration grows with log distance over target size (Fitts). For film, pros keep the bell profile and slightly curved path, remove the jitter and corrections, and add deliberate stylization: ease out heavy arrivals, occasional single overshoot on long moves, and a short settle before the click.

### Cited Findings
- Minimum jerk trajectory (Flash and Hogan 1985): x(t) = x0 + (xT - x0)(10t^3 - 15t^4 + 6t^5) on normalized time; speed peaks at mid move with peak to average ratio 1.875 (minimum acceleration gives 1.5); human reaching measures about 1.75. [Shadmehr and Wise supplement](https://www.scribd.com/document/688690290/minimumjerk), [Duarte notebook](https://nbviewer.jupyter.org/github/demotu/BMC/blob/master/notebooks/MinimumJerkHypothesis.ipynb)
- Minimum jerk fits only the initial ballistic part of mouse pointing; fitted to the whole movement it is "very poor" because real pointing is a quick move then corrections. [Optimal control model of mouse pointing (arXiv 2002.11596)](https://arxiv.org/pdf/2002.11596)
- Corrective submovements occur regularly in mouse pointing at large index of difficulty. [Optimal feedback control for HCI (arXiv 2110.00443)](https://arxiv.org/pdf/2110.00443)
- Flash and Henis (1991) reproduce corrected movements by superposing scaled minimum jerk submovements. [Lee, Port and Georgopoulos (UMN)](https://brain.umn.edu/assets/story_file_104)
- Most distance is covered by a primary ballistic submovement with smooth acceleration and deceleration; primary submovements often undershoot (cheaper to correct forward). [Springer, J NeuroEng Rehab 2008](https://link.springer.com/doi/10.1186/1743-0003-5-28)
- Target size changes the shape of the velocity profile by lengthening the corrective phase, while distance scales the whole curve without changing its shape (Thompson et al. 2007). [search summary](https://searchworks.jioinstitute.edu.in/articles/cmedm__17126941)
- Fitts for mouse: MacKenzie and Buxton's classic regression MT = 1.03 + 0.096 ID; reanalysis under ISO 9241-9 gives throughput 2.65 bits/s (4.32 with grasp adjustment); ISO throughput values rarely exceed 5 bits/s; a 2009 study found 3.83 bits/s. [MacKenzie, HFES 2009](https://www.yorku.ca/mack/hfes2009.html), [MacKenzie 1992](https://www.yorku.ca/mack/gi92.pdf)
- Peekaboo "human" mouse profile (a working engineering model): under 200 px: 280 to 350 ms; 200 to 800 px: 400 to 900 ms; over 800 px: 900 to 1700 ms; shallow Bezier arc with minimum jerk timing; overshoot probability near 0 for short hops rising to about 20 percent for long moves; perpendicular jitter capped at about 0.35 px per frame and tapering to zero near the target; final point always exact. [Peekaboo human-mouse-move.md](https://github.com/steipete/Peekaboo/blob/main/docs/human-mouse-move.md)
- Automation libraries: cubic Bezier paths with randomized control points on one side of the line; Fitts law sets the number of points from target width and distance; far targets "overshoot or slightly miss and re-adjust"; click on a random point inside the element, not its exact center. [ghost-cursor README](https://unpkg.com/ghost-cursor-frames@1.2.1/README.md). The chromey Rust crate uses an overshoot factor of 0.15 past the target and cubic ease in out timing; vs-humanize adds a short pre-click hover. [chromey mouse.rs](https://docs.rs/chromey/2.46.2/src/chromiumoxide/mouse.rs.html), [vs-humanize](https://docs.rs/crate/vs-humanize/0.1.8/source/src/mouse.rs)
- Motion design house style (HeyGen HyperFrames): travel 0.4 to 0.92 s (example 0.85 s) with power3.out; default path straight, diagonal only as one continuous vector when the story needs it; the arrow tip, not the box center, lands on the target. [HyperFrames oversized cursor](https://skills.cat/skills/heygen-com/hyperframes/oversized-cursor)
- Remotion components (framecn Cursor Flow) move the cursor along cubic Bezier paths with pauses and clicks. [21st.dev Cursor Flow](https://21st.dev/@framecn/components/cursor-flow.md)
- Vendor claim: cursor eased so it is fastest mid path and slow at start and end. [VideoCaptions.ai](https://www.videocaptions.ai/elements/cursor-box-select-animation)

### Inferences
- A practical film model: duration T = a + b x log2(D/W + 1) with a about 0.25 s and b about 0.12 to 0.15 s/bit gives 0.4 to 0.9 s for typical UI hops at 1080p, matching Peekaboo and HyperFrames ranges. Films run faster than real users (real ISO throughput of about 4 bits/s would make a 1000 px hop to a 40 px button about 1.2 s plus reaction time).
- Curvature: a shallow arc, control point offset roughly 5 to 15 percent of the distance to one side, consistently on the same side for a given "hand", reads as human. Ruler straight lines read as robotic; big S curves read as drunk. (Numbers are a synthesis, not measured.)
- Asymmetric ease (power3.out, or minimum jerk with a later peak) reads more "premium" than symmetric ease in out, because it spends more frames in the readable arrival.
- Overshoot: use on at most about 1 in 5 long moves, 2 to 6 percent of distance, settling in 150 to 250 ms. Never on short hops.

### Gaps
- No primary source found giving measured trajectory curvature for mouse pointing, the percentage of moves that overshoot, or the typical pause between arrival and click (dwell before click). Those numbers above are inferences.

## 3. Click and state feedback

### Takeaway
The premium click is a quick press (scale to about 0.8 to 0.84 in about 100 to 130 ms) and a slower springy release (about 2x the press), with the target reacting in the same frame (button scale about 0.94) and the next beat starting on that frame. Ripples are optional and soft (about 0.6 s). Tilt is subtle and only on horizontal travel. Motion blur is directional and proportional to per frame travel. Cursor type swaps (I-beam, hand) exist but tools offer ways to suppress rapid swaps.

### Cited Findings
- Press 0.84 scale in 0.1 s (power2.in), release to 1 in 0.22 s (power2.out) starting 0.1 s after the press; press to release ratio about 1:2; button target reacts with scale 0.94 at the same moment; cursor-only taps (focusing an input) get no target reaction; every click must trigger the next beat in the same frame (menu opens, typing starts, logo launches); transform origin at the arrow tip ('21% 14%' in a 24 unit viewBox). [HyperFrames oversized cursor](https://skills.cat/skills/heygen-com/hyperframes/oversized-cursor)
- Cap press: shrink to 0.8 over 130 ms with smoothstep, starting before mouse down, held while the button is down, released over 130 ms; separate click spring (530 / 1 / 40) for the path within 175 ms of a click. [Cap layers/cursor.rs](https://github.com/CapSoftware/Cap/blob/main/crates/rendering/src/layers/cursor.rs), [Cap cursor_interpolation.rs](https://github.com/CapSoftware/Cap/blob/main/crates/rendering/src/cursor_interpolation.rs)
- Ripple: Cap default 0.6 s, strength 0.7, blue 71,133,255, off by default. Tella and Canvid offer ripple with adjustable size. [Cap configuration.rs](https://github.com/CapSoftware/Cap/blob/main/crates/project/src/configuration.rs), [Tella](https://www.tella.com/blog/animated-cursors-for-screen-recordings)
- Without ripple or spring on, "no visible reaction on clicks" is listed as a mistake. [Tella blog](https://www.tella.com/blog/animated-cursors-for-screen-recordings)
- Tilt in direction of movement: Screen Studio "Rotate cursor while moving", Tella "Movement tilt", Canvid "Tilt cursor with movement", Recordly "sway", Framer Smooth Arrow Cursor rotates toward direction of travel; Cap formula gives about 4.5 degrees for a 1000 px move in 0.4 s, clamped at 20. [Screen Studio](https://screen.studio/guide/cursor), [Tella](https://www.tella.com/animated-cursors/llms.txt), [Canvid](https://www.canvid.com/support/editing/cursor-editor), [Cap lib.rs](https://github.com/CapSoftware/Cap/blob/main/crates/rendering/src/lib.rs), [Framer](https://www.framer.com/marketplace/components/smooth-arrow-cursor)
- Motion blur: directional smear equal to per frame travel times amount, fps normalized; Screen Studio lets you set cursor blur separately from zoom and pan blur. [Cap layers/cursor.rs](https://github.com/CapSoftware/Cap/blob/main/crates/rendering/src/layers/cursor.rs), [Screen Studio animations](https://screen.studio/guide/animations)
- Drag: Cap uses a stiffer drag spring (tension 1000, friction 40) so the dragged object tracks tightly; the clone used a softer, overdamped drag spring (136 / 1.2 / 26). [Cap](https://github.com/CapSoftware/Cap/blob/main/crates/rendering/src/cursor_interpolation.rs), [clone README](https://github.com/pythonlearner1025/Screen-Studio-Effects)
- Cursor type morphing: Screen Studio "Always use default system cursor" and "Optimize original cursor types" (reduces rapid type changes); Canvid "Always use pointer style" stops hand and text pointer swaps. [Screen Studio](https://screen.studio/guide/cursor), [Canvid](https://www.canvid.com/support/editing/cursor-editor)
- Cursor look: white body with black stroke or black (#1c1c1c) body with 1.4 px white stroke, one choice per film; drop shadow 0 4px 6px rgba(0,0,0,.3). [HyperFrames](https://skills.cat/skills/heygen-com/hyperframes/oversized-cursor)
- After Effects kits: Mouse Pack (one click cursor, auto keyframed states, click animations), CursorKit (click, drag, scroll, auto typing), free tutorial file with realistic click, color change on click, glow, impact circle; Squash and Stretch plugin used for organic press. [Mouse Pack](https://aescreens.gumroad.com/l/mouse-pack), [CursorKit](https://www.behance.net/gallery/63246851/CursorKit-Script), [aescripts Squash and Stretch](https://aescripts.com/learn/after-effects-plugin-squash-and-stretch-easy-animation-tutorial/)
- Remotion component catalog shows the common moves as separate building blocks: Cursor Click, Cursor Drag, Cursor Changes Shape (morph), Magnetic Button Click, Dot and Ring cursor, Cursor Spotlight Reveal, Zoom Follows the Click, Select Text and Ask AI. [21st.dev Cursor Click](https://21st.dev/@21st/components/cursor-click.md), [Magnetic Button](https://21st.dev/@21st/components/magnetic-button.md), [Cursor Morph](https://21st.dev/@21st/components/cursor-morph.md)

### Inferences
- Order of events for one premium click (at 60 fps): arrive and settle (about 6 to 12 frames of near-zero speed), hover state on the target lights up on arrival, press 6 to 8 frames, target scales 0.94 in the same frames, UI result fires on the release frame, release spring 12 to 14 frames.
- Magnetic snap: on the last 10 to 20 percent of travel, ease the target toward the cursor a few pixels (or the cursor toward the target center) so the landing reads intentional. No numeric source found; treat as stylization.
- For drags, add a little lag on the dragged object (it follows the cursor through its own spring) and a small tilt of the object in the direction of motion; keep the cursor itself tighter than the object.

### Gaps
- No source with numbers for magnetic snapping strength, I-beam morph timing, or hover state lead time.
- No source with numbers for cursor trails (ghost copies); only Jitter's template mentions "movement trails". [Jitter cursor template](https://bobo.jitter.video/template/cursor/)

## 4. Camera and cursor

### Takeaway
The camera follows clicks, not the raw cursor: auto zoom targets click positions, pans only when the cursor leaves a central safe zone (about 70 percent), uses heavier and more damped springs than the cursor, and zooms out softer than it zooms in. The cursor enters from off frame and exits off frame with acceleration; it never fades in or out in place, and between actions it drifts aside or hides after an idle delay.

### Cited Findings
- Auto zoom is click based in Screen Studio, Tella, FocuSee, Cursorful, Canvid; Canvid's auto zoom follows the cursor. [Screen Studio](https://screen.studio/guide/auto-zoom), [Tella](https://www.tella.com/blog/how-to-add-auto-zoom-to-screen-recordings), [FocuSee](https://focusee.imobie.com/features/auto-zoom-and-cursor-animation.htm), [Cursorful](https://cursorful.com/), [Canvid](https://www.canvid.com/features/auto-manual-zoom)
- Safe zone: viewport pans only when the cursor leaves the inner 70 percent; pan target averages 0.5 s of future cursor positions; zoom triggered after cursor stays within 2 px for 0.5 s. [Screen-Studio-Effects](https://github.com/pythonlearner1025/Screen-Studio-Effects)
- Camera springs are heavier than cursor springs: Cap screen movement spring stiffness 200, damping 40, mass 2.25 vs cursor 470 / 70 / 3; clone viewport presets overdamped (zeta about 1.33 to 1.40). Cap's zoom spring re-aims continuously across segment boundaries and clusters points within 50 percent width and 70 percent height of the frame. [Cap configuration.rs](https://github.com/CapSoftware/Cap/blob/main/crates/project/src/configuration.rs), [Cap zoom_spring.rs](https://github.com/CapSoftware/Cap/blob/main/crates/rendering/src/zoom_spring.rs)
- Screen Studio "Focused" camera settles quickly (for reading), "Smooth" is more fluid (for creative pieces). [Screen Studio](https://screen.studio/guide/animations)
- Arcade pans instead of zooming when the frame size stays the same between steps; offers a delay before zoom starts. [Arcade docs](https://docs.arcade.software/kb/build/interactive-demo/edit/pan-and-zoom)
- Entry: start off screen, canonically below frame (top 115 to 120 percent), never fade in or mask reveal. Exit: accelerate off the nearest edge with power2.in over 0.5 to 0.7 s (left 118 percent, left -12 percent or top 116 percent); never fade out in place. "Cut the curve" handoff: in the last about 0.3 s before a hard cut, accelerate toward the next scene's first click point covering about a third of the path, and the next scene continues with power2.out at matching velocity. [HyperFrames](https://skills.cat/skills/heygen-com/hyperframes/oversized-cursor)
- Idle: during beats the cursor does not own (typing, narration) it drifts aside over 0.5 to 0.9 s with power2.out; never frozen on the action, never wobbling idly. [HyperFrames](https://skills.cat/skills/heygen-com/hyperframes/oversized-cursor). Recorders instead fade it: Cap 500 ms minimum idle, 400 ms fade, 250 ms early return; Tella "Hide when inactive". [Cap](https://github.com/CapSoftware/Cap/blob/main/crates/rendering/src/layers/cursor.rs), [Tella](https://www.tella.com/blog/animated-cursors-for-screen-recordings)
- Loop: Screen Studio "Loop cursor position" and Tella "Return to start" move the cursor back to its first position near the end for seamless loops; Screen Studio and Cap can stop cursor movement in the last seconds. [Screen Studio](https://screen.studio/guide/cursor), [Cap configuration.rs](https://github.com/CapSoftware/Cap/blob/main/crates/project/src/configuration.rs)
- Size versus zoom: smaller cursor (about 1.5x) in deep zooms so it does not cover the target. [Tella](https://www.tella.com/blog/animated-cursors-for-screen-recordings)
- Full frame cursor size in launch films: 7cqw (about 134 px at 1920), "never smaller"; 4.6 to 5.5cqw inside a mock. "Big cursor movement is one of the cheapest high-yield motion sources in a launch video." [HyperFrames](https://skills.cat/skills/heygen-com/hyperframes/oversized-cursor)

### Inferences
- When the camera is zoomed, keep the cursor's screen size constant (counter scale it) or let it grow only slightly; otherwise the 7cqw cursor becomes huge at 2x zoom.
- Start the zoom 0.3 to 0.6 s before the click so the click lands in a settled frame (the Screen Studio complaint about late starts supports this direction, not the exact number).

### Gaps
- No official zoom levels, lead-in or lead-out timings for any commercial tool.

## 5. Variety across a film, and named brand examples

### Takeaway
No source gave a frame by frame breakdown of cursor work in Apple, Linear, Notion, Arc, Raycast, Framer, Stripe or Vercel films. The documented lesson from Figma's campaign (Animade with COLLINS) is that cursors became characters through "motion, weight and timing", physical gags and "human" flourishes. Variety in practice comes from varying distance driven duration (Fitts), curvature side and amount, occasional overshoot, idle behavior, entry and exit directions, and handing off between scenes, plus multiplayer cursors with name tags.

### Cited Findings
- Figma campaign "Nothing great is made alone": storyboard by COLLINS put cursors front and center; Animade's job was to give the "simple triangle that is usually overlooked" personality, using motion, weight and timing to add humour and humanity, with physical gags and human flourishes that bent the software's rules; four animated stories for Instagram and YouTube. [Animade: Figma](https://archive.animade.tv/work/figma)
- A Config 2024 presenter animated cursors in After Effects and recreated FigJam's high five animation. [Contra case study](https://contra.com/p/lqBLRme3-a-case-study-deck-presented-at-figma-config-2024)
- Brand cursors (a multiplayer arrow with a name tag) can replace the macOS arrow when the brand's cursor is widely recognized. [HyperFrames](https://skills.cat/skills/heygen-com/hyperframes/oversized-cursor)
- Multiplayer cursor motion: CSS linear transitions move in straight lines and ignore momentum (ease in out looks worse than linear); springs are the best balance of smoothness and responsiveness but path accuracy is loose; splines (perfect-cursors) pass through every point but add delay. Demo update interval 120 ms with 5 to 15 ms jitter. [Liveblocks](https://liveblocks.io/blog/how-to-animate-multiplayer-cursors). perfect-cursors (Steve Ruiz, used in tldraw) interpolates points sent every 80 ms with a spline. [perfect-cursors](https://npmjs.com/package/perfect-cursors)
- Peekaboo seeds randomness per run so "runs feel unique" while distance changes duration and overshoot probability. [Peekaboo](https://github.com/steipete/Peekaboo/blob/main/docs/human-mouse-move.md)
- Randomized Bezier control points so each path differs; click a random point inside the element rather than its exact center. [ghost-cursor](https://unpkg.com/ghost-cursor-frames@1.2.1/README.md)
- Cursor should clarify rather than distract (checklist question). [Hera](https://hera.video/use-cases/ui-animation-videos)

### Inferences
- A variety recipe for a 30 to 60 s film: mix at least three tempos (quick 0.3 to 0.4 s hops, standard 0.6 to 0.8 s moves, one slow 1 s+ "considered" move), vary curvature side and amount per move, give only one or two long moves an overshoot, vary pause before click (about 3 to 15 frames), use different entry and exit edges, let the cursor leave the frame entirely for type-only or hero beats, and use at least one cut-the-curve handoff.
- Multiplayer scenes: give each collaborator cursor its own color, name tag, spring and tempo (one quick and decisive, one slow and wandering) so they read as different people; small lag and spline smoothing match how real multiplayer cursors look in Figma-like apps.
- Personality beats (Figma/Animade style): a cursor "waiting" (gentle drift), "thinking" (small hesitation loop before a choice), or interacting physically with UI (pushing, high five) reads as human and gives the film a signature moment.

### Gaps
- No breakdowns found for Apple, Linear, Notion, Arc, Raycast, Framer, Stripe or Vercel launch videos. Claims about their cursor style would need frame by frame viewing of the actual videos, which was not done.

## 6. Common mistakes that look robotic or cheap

### Takeaway
Cheap: tiny cursor, raw jittery path, no zoom, no click reaction, constant speed linear moves, two cursors visible, cursor fading in or out in place, cursor frozen on the action, cursor covering the target in deep zooms, and moves that are too fast for a first time viewer. Robotic: every move with the same duration, curve and ease, straight ruler lines, symmetric ease in out everywhere, perfect center clicks.

### Cited Findings
- Cheap looking demos: tiny cursor, no zoom ("filming through a screen door"), jittery cursor, raw unpadded recordings. [How I make product demos that don't look like garbage](https://www.twoaveragegamers.com/how-i-make-product-demos-that-dont-look-like-garbage/)
- Tella mistake list: no visible reaction on clicks (ripple and spring off), big cursor hiding labels in 250 percent+ zooms, cursor jumping at clip start (trim the first half second), two cursors visible. [Tella](https://www.tella.com/blog/animated-cursors-for-screen-recordings)
- Move slower than you think; avoid circling the cursor around or speeding up and slowing down without reason; move deliberately. [Packt, E-learning with Camtasia](https://subscription.packtpub.com/book/web-development/9781849698665/5/ch05lvl1sec41/using-the-mouse-properly), [Adobe eLearning demo tips](https://elearning.adobe.com/2022/08/video-demo-practical-tips)
- Never fade in, mask reveal, or fade out in place; never frozen on the action; never idle wobble. [HyperFrames](https://skills.cat/skills/heygen-com/hyperframes/oversized-cursor)
- Linear CSS transitions ignore momentum and move in straight lines; ease in out on each segment looks worse. [Liveblocks](https://liveblocks.io/blog/how-to-animate-multiplayer-cursors)
- Rapid cursor type changes are a known artifact that tools filter out. [Screen Studio](https://screen.studio/guide/cursor)
- Smooth movement can make drop down menu interactions look wrong, so it is disabled for those fragments. [Screen Studio](https://screen.studio/guide/disable-smooth-mouse-movement)
- Motion blur must be fps normalized, otherwise 120 fps renders look sharper or smeared differently than 60 fps. [Cap layers/cursor.rs](https://github.com/CapSoftware/Cap/blob/main/crates/rendering/src/layers/cursor.rs)

### Inferences
- Over smoothing is its own mistake: a 350 ms lag spring (Cap "Smooth") makes the cursor arrive late relative to UI reactions; with code-driven films the click must still land exactly on the frame the UI responds.
- Over-tilt (constant 15 to 20 degree lean) and bouncy cursor springs read as toy-like; keep tilt only during horizontal travel and the main glide nearly critically damped.
- Identical timing is the strongest robotic tell; derive duration from distance and target size and add seeded variation.

### Gaps
- No controlled study found on viewer perception of cursor "premiumness"; the mistake list is practitioner and vendor opinion.
