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
- Display scale about 0.74 of the 96 px image (the arrow is then about 45 px tall at 1080p): big enough to follow in a film, not cartoonish.

## How it moves (`templates/kit/src/Cursor.tsx`)

- Stops: `{ f, x, y, leave?, arc?, ease? }`. The cursor arrives at `f`, rests until `leave`, then travels to the next stop.
- Path: minimum-jerk easing (how a hand moves a mouse from rest to rest) along a gentle arc: perpendicular offset `arc x sin(pi e)` of the segment length, `arc` about 0.1 to 0.14, sign picks the side. Never a straight robotic line, never linear speed.
- Research note: Screen Studio smooths recorded cursors with bezier interpolation and spring easing; multiplayer cursor apps use springs or splines. Minimum jerk with an arc gives the same calm, confident feel for authored paths.
- Drags use the same easing as the thing being dragged (`ease: easeCubic`) so the thumb never slips from under the pointer.
- Trail when fast (speed above 7 px per frame): two ghosts at -0.33 and -0.66 frames with opacity 0.18 and 0.08, like a shutter smear.
- Click: press to 0.86 over 3 frames before the click frame, release over 9 frames; a soft ripple ring (navy 35 percent on light, white 50 percent on dark) from 10 to 32 px over 20 frames.

## Behaviour that sells realism

- Arrow by default; I-beam when it enters a text field (a few frames before reaching it); hand over clickable rows and buttons; grab while dragging.
- Shape changes crossfade over 3 frames.
- Hidden while typing (macOS hides the pointer on the first key) and fades back when the hand moves again. Visibility fades over 8 frames.
- Enters from off the focus area (lower right is natural), never pops into existence on the target.
- Rests briefly (hover) before a click; the hovered element shows its hover state.

## Collaborators' cursors

Draw them as the product does: an arrow in the person's presence colour with a 2.4 px white stroke and a soft shadow, plus a name tag pill in the same colour (white 19 px 600 text) at the arrow's lower right. They move with the same path system, fly in from the side where their chat message is, and leave after their action. Use real colleague names only when the user gives them.
