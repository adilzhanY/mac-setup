# Interaction: cursor, touch, or nothing

Pick by platform (see `brief.md`): a cursor for desktop and web products, taps for mobile products, nothing for films where things act on their own. Getting this wrong is the first thing a viewer notices.

## Touch (mobile products)

The torq film had no cursor at all: a phone app driven by a mouse arrow would read as wrong.

- **No drawn finger or hand.** A cartoon finger looks cheap and hides the control.
- **The control presses**: scale down to about 0.92 over 3 frames before the tap frame, back over 6 (`pressScale` in `templates/kit/src/Touch.tsx`).
- **A soft ring spreads** from the touch point: 0 to 120 px over 22 frames, white at 50 percent fading to 0, 3 px stroke (`TapRipple`). On a light stage use the ink colour at 35 percent.
- **The result answers on the same frame**: the check fills, the toggle flips, the row washes with the accent. The tap is the sound's frame (a blip in the song's key).
- Taps land on the grid: a run of four set checks on 8ths reads as a rhythm, not as a demo.
- Scrolling and swipes: move the content with the camera spring, never draw the finger. A row swiping away gets a whoosh.
- Keyboard input on mobile: skip it. Prefill values (the product's own prefill feature if it has one) and tap to confirm.

## Nothing

Hardware, a brand film, a data story: elements act by themselves on the beat. The pacing does the job of the hand.

## Cursor (desktop and web products)

A Bauwerk viewer called a generic drawn arrow "some sharp cursor" and asked for "my main cursor that I use on Arch Linux". On desktop products, always use the user's real cursor theme.

## Find and extract it

- Linux theme name: `$XCURSOR_THEME` (for example `macOS-White`, size 40), also in `~/.icons/default/index.theme` (`Inherits=`), or `gsettings get org.gnome.desktop.interface cursor-theme`.
- Files: `~/.local/share/icons/<theme>/cursors/` (Xcursor binary; `pointer` links to `hand2`, `text` to `xterm`).
- Run `templates/kit/prep/xcursor.py [theme_dir] public/cursor`: it parses the Xcursor TOC, takes the largest image (96 px), converts premultiplied BGRA to straight RGBA, writes PNGs and `cursors.json` with hotspots.
- macOS and Windows users: their cursor is the system one; draw it as an SVG matching the OS (black arrow with a white rim on macOS) and set the hotspot at the tip.
- macOS-White hotspots at 96 px: left_ptr (30, 14), hand2 (34, 19), xterm (48, 51), grabbing (51, 32), grab (50, 30). The image must be placed so its hotspot sits on the target point: `left = x - hotX * scale`.
- Size: about 7 percent of the frame width for a full frame cursor, "never smaller" (about 134 px at 1920 wide, [HyperFrames](https://skills.cat/skills/heygen-com/hyperframes/oversized-cursor)); Tella's product demo preset uses 2.5x the system size, and about 1.5x inside deep zooms so it does not hide labels ([Tella](https://www.tella.com/blog/animated-cursors-for-screen-recordings)). Measure the visible arrow, not the image box. Bauwerk and the first Enogon film used 0.74 of the 96 px image (about 71 px), half the guideline; the Enogon rebuild uses 1.15 (a 110 px box). When the camera zooms, keep the cursor's screen size constant or let it grow only slightly **(heuristic)**.

## How it moves

The Enogon review: "cursor movement quality was bad", it "needs different animations like the text has". The first Enogon cursor (the kit's 2.0.0 `Cursor.tsx`) had every documented tell: visibility faded in and out in place over 8 frames; every move used the same symmetric minimum jerk ease with an arc of 0.1 on the same side; the press was 3 frames down and 9 up with a 14 percent shrink while nothing on the target reacted; speed showed as two ghost copies at 18 and 8 percent; and it was about half the guideline size. The strongest robotic tell is identical timing: every move the same duration, curve and ease. Sources for this section are in `research/ad-music-and-logo/notes/cursor_animation.md`.

Every serious screen recorder converges on one kit, and the open source Cap (which says it is inspired by Screen Studio) gives the numbers Screen Studio does not publish:

| Parameter | Value | Source |
|---|---|---|
| Glide spring (Cap "Mellow", the default) | tension 470, mass 3, friction 70: trails its target by friction / tension, about 149 ms, nearly critically damped (zeta about 0.93) | [Cap configuration.rs](https://github.com/CapSoftware/Cap/blob/main/crates/project/src/configuration.rs), [cursor_interpolation.rs](https://github.com/CapSoftware/Cap/blob/main/crates/rendering/src/cursor_interpolation.rs) |
| Other presets | Slow 200 / 2.25 / 40 (200 ms lag); Smooth 80 / 2.5 / 28 (350 ms); Fast 380 / 1 / 30 (79 ms) | same |
| Click spring | 530 / 1 / 40, within 175 ms of a click, with a 500 ms lookahead so the cursor arrives on the target | same |
| Drag spring | 1000 / 1 / 40, so a dragged object tracks tightly | same |
| Camera spring | stiffness 200, damping 40, mass 2.25: heavier and more damped than the cursor | same |
| Duration | 0.3 to 0.4 s for short hops, 0.6 to 0.8 s standard, about 1 s for one considered move; grows with distance (Peekaboo: 280 to 350 ms under 200 px, 400 to 900 ms for 200 to 800 px, 900 to 1700 ms beyond) | [Peekaboo](https://github.com/steipete/Peekaboo/blob/main/docs/human-mouse-move.md); [HyperFrames](https://skills.cat/skills/heygen-com/hyperframes/oversized-cursor) |
| Ease | asymmetric decelerate (power3 out, travel 0.4 to 0.92 s) or the near critical spring; never symmetric ease in out on every move, never linear | HyperFrames; [Liveblocks](https://liveblocks.io/blog/how-to-animate-multiplayer-cursors) |
| Path | a shallow arc, its amount and side varied per move; overshoot near zero on short hops, about 20 percent of long moves | Peekaboo; [ghost-cursor](https://unpkg.com/ghost-cursor-frames@1.2.1/README.md) |
| Press | shrink to 0.8 to 0.84 over 100 to 130 ms, starting before the click frame; release about twice as long; the target scales to about 0.94 on the same frames, and the next beat fires on the click frame | [Cap cursor.rs](https://github.com/CapSoftware/Cap/blob/main/crates/rendering/src/layers/cursor.rs); HyperFrames |
| Tilt | horizontal pixels travelled in the last 0.4 s x 0.03 x 0.15, clamped to 20 degrees: about 4.5 degrees for a 1000 px move; only during horizontal travel, back to 0 at rest | [Cap lib.rs](https://github.com/CapSoftware/Cap/blob/main/crates/rendering/src/lib.rs) |
| Motion blur | a directional smear equal to this frame's travel, normalized to the frame rate | Cap cursor.rs |
| Entry and exit | from off frame (canonically from below) and out by accelerating off the nearest edge in 0.5 to 0.7 s; never fade in or out in place, never frozen on the action | HyperFrames |
| Hand over across a hard cut | in the last 0.3 s before the cut, accelerate toward the next scene's first click point, and the next shot continues at the matching speed | HyperFrames |

Remotion's `spring()` takes the same stiffness, damping and mass, so the numbers transfer; the integration should still be checked (the kit integrates them itself, below).

Human pointing gives the shape: the ballistic part of a reach has a bell shaped speed whose peak is 1.875 times the average (minimum jerk, [Duarte](https://nbviewer.jupyter.org/github/demotu/BMC/blob/master/notebooks/MinimumJerkHypothesis.ipynb)), but real mouse moves are a quick primary movement, often undershooting, then corrections ([arXiv 2002.11596](https://arxiv.org/pdf/2002.11596)), and duration grows with log distance over target size (Fitts, [MacKenzie](https://www.yorku.ca/mack/hfes2009.html)). Films keep the bell and the slight curve and drop the jitter. A film model **(heuristic)**: duration T = 0.25 s + 0.12 to 0.15 s x log2(D / W + 1), which gives 0.4 to 0.9 s for typical hops at 1080p.

### Variety: the cursor needs as many moves as the text has

The user liked the new text animations and asked for the cursor to get the same range. A recipe for a 30 to 60 s film **(heuristic, from the research)**:

- At least three tempos: quick 0.3 to 0.4 s hops, standard 0.6 to 0.8 s moves, one slow, considered move of 1 s or more.
- The arc's side and amount change per move (control point 5 to 15 percent of the distance to one side); ruler straight lines read as robotic, big S curves as drunk.
- An overshoot (2 to 6 percent of the distance, settling in 150 to 250 ms) on only one or two long moves, never on short hops.
- The pause before a click varies, about 3 to 15 frames.
- Different entry and exit edges; the cursor leaves the frame entirely for type only or hero beats.
- Personality beats sparingly: a small hesitation before a choice, a drift while waiting, a physical push on the UI. Animade gave Figma's "simple triangle that is usually overlooked" its character through "motion, weight and timing" ([Animade](https://archive.animade.tv/work/figma)).
- At least one cut the curve hand over across a hard cut.

### The press, and the target answering

At 60 fps **(heuristic, from Cap and HyperFrames)**: the cursor arrives and settles (6 to 12 frames of near zero speed), the target's hover state lights on arrival, the press takes 6 frames down to 0.84 while the button scales to about 0.94 in the same frames, the result fires on the click frame, the release takes about 13 frames. A cursor only tap (focusing a field) gets no target scale, but the field itself answers (a focus ring, the caret). "No visible reaction on clicks" is a listed mistake ([Tella](https://www.tella.com/blog/animated-cursors-for-screen-recordings)). A ripple is optional, soft, about 0.6 s (Cap's default, off by default).

**Magnet into targets** **(heuristic, no numeric source)**: on the last 10 to 20 percent of the travel, ease the target a few pixels toward the cursor (or the cursor toward the target's centre) so the landing reads intentional. The hit is still decided by the arrow's tip (the hotspot), never the sprite's centre.

### The code path (from the Enogon rebuild, being copied into the kit)

`Cursor.tsx` and `cursorTrack.ts` in `~/dev/enogon-video/src/` implement all of this; they are being copied into `templates/kit/src/`, and until then read them there.

- **`makePath(track, frames, clicks, drag?)`** turns the authored stops into the cursor's real path, computed once for every frame of the film, so any frame renders the same after any seek (`review.md`, A timeline that gives the same frame every time). The stops give a target that moves on an arc with power3 out between them (fast away, decelerating into the target); a spring follows that target with Cap's presets: `mellow` (470, 3, 70) by default, `click` (530, 1, 40) from 12 frames before to 4 frames after each click, `drag` (1000, 1, 40) between the grab and the release; 8 sub steps per frame.
- **`MacCursor({ track, frame, path, clicks, scale })`** draws the user's own cursor images (`left_ptr`, `hand2`, `xterm`, `grabbing`, with their hotspots) at the path's position. Tilt follows the horizontal travel over the last 24 frames (0.4 s) with Cap's factors (x 0.03 x 0.15, doubled in this film), clamped to 20 degrees, around the hotspot. When it moves faster than 6 px per frame, three smear copies sit along this frame's travel at a quarter, a half and three quarters back (opacity 0.22, 0.14, 0.07): a directional smear, not trailing ghosts from earlier frames. The press goes down to 0.84 over 6 frames (ease in) and back over 13 (power3 out). Shape changes (arrow, hand, I-beam, grab) crossfade over 3 frames; visibility never fades. A click is either `ring` (an ink ring spreading over 36 frames) or `none` (the target answers on its own).
- **`cursorTrack.ts`** holds the film's one cursor: `TRACK` (stops entering from below the frame at (330, 1220) and leaving off the right edge on an accelerating t cubed ease, shapes, arcs that change side and amount per move), `CLICKS`, `PATH = makePath(TRACK, 1700, CLICKS, [F.grab, F.release])`, and `cardRect(frame)`, the dragged card riding the cursor (Drag and drop, below).
- The collaborator cursor (`RemoteCursor`) still uses the older stop path with faded visibility; give collaborators the same path system, entering and leaving through the frame edges, when a film has them.

## Behaviour that sells realism

- Arrow by default; I-beam when it enters a text field (a few frames before reaching it); hand over clickable rows and buttons; grab while dragging.
- Shape changes crossfade over 3 frames.
- While typing it moves aside out of the way (macOS hides the pointer on the first key; in a film, drift it aside over 0.5 to 0.9 s with power2 out, or leave the frame), never frozen on the action and never fading in place. When it is not needed for a while it leaves through a frame edge and comes back through one.
- Enters from off frame (from below is the canonical entry), never pops or fades into existence on the target.
- Rests briefly (hover) before a click; the hovered element shows its hover state.

## The cursor leads an action (from vizavi-motion's product UI module)

Give each episode one clear task: pick an item, change a setting, drag a card, rearrange a panel, start a process, show the result.

- **The chain**: hover → the target reacts → press or grab → the change → a readable result. The cursor never wanders over a passive screen.
- **The hit** is decided by the tip of the arrow (the hotspot), never by the centre of the sprite.
- **Before a click** a short hover the viewer can read; **after it** a visible change of state that the click clearly caused.
- **Fully visible**: the cursor stays sharp and whole while it presses, and never covers the button's label, the result or numbers that must be read.
- **Few controls**: highlight only a few main controls per action (the source's guide is 1 to 3, not a quota).
- **States in causal order**: hover, pressed or dragging, processing, success or selected, or another set that makes sense. Never show success before the process has finished. A chart, a percentage and any other indicator of one operation share one progress value (the counter rule in `elements.md`).
- **Micro reactions**: a few functional ones (the target lighting up, a state change, a neighbouring card answering, a panel opening). They support the main point and never compete with it.
- **Timing**: fit durations and amplitudes to the distance, the pace, the frame size and the reading window (How it moves, above): durations that follow distance, an asymmetric ease, a press with weight, entering and leaving off frame. Never copy one move's numbers onto every move: identical timing is the strongest robotic tell.
- **Going to a detail** is motivated by the action, and the text gets its time to be read.

## Drag and drop

- Fix the grab point and the offset between cursor and object at the grab.
- **The object rides the cursor**: it is placed from the cursor's own path every frame, so it lags, swings and settles with it, and it tilts in the direction of travel. The Enogon rebuild's `cardRect(frame)`: the card lifts over 8 frames (scale 1.04, 6 px up), follows `PATH.at(frame)`, and tilts by the horizontal travel over the last 6 frames x 0.06, clamped to 9 degrees; it drops back over the 6 frames before the release. Keep the cursor tighter than the object (Cap's stiff drag spring on the cursor; the object may have its own softer lag).
- The card lifts and follows on an arc, the drop zone lights up, and on the drop the card shrinks softly and settles into its slot.
- A follow with lag can show weight and inertia, but must never look like the grip was lost: the main object stays under control and lags or catches up for a reason. Neighbours react after the event.
- The drop, the snap and the last settle end in a stable, clear layout. Do not put the same spring on every layer.
- Drags use the same easing as the thing being dragged (above), so the object never slips from under the pointer.

## A film, not an app

Animate the cursor, the grab, the states and the delays on the one timeline, computed from the frame (`review.md`, A timeline that gives the same frame every time). No real user input is needed to play it, and nothing depends on a previous mouse event. Full functional testing of fast repeated clicks, resizing and reduced motion is only needed when a live app is being built; do not turn a video demo into product development.

## Check a product UI shot

At speed and at the joins: is the action clear, is the grab precise, does the drop finish, do progress and states stay in sync, does the interface keep its identity where it should, are 2D, 2.5D and 3D really different (`three.md`), does the projection hold while the camera moves and after seeking backwards, can the overlays be read. Then check the decoded final file with its sound (`review.md`). A cursor, a `translateZ` or an extrusion parameter existing in the code does not prove the visual result.

## Collaborators' cursors

Draw them as the product does: an arrow in the person's presence colour with a 2.4 px white stroke and a soft shadow, plus a name tag pill in the same colour (white 19 px 600 text) at the arrow's lower right. They move with the same path system, fly in from the side where their chat message is, and leave after their action. Use real colleague names only when the user gives them.
