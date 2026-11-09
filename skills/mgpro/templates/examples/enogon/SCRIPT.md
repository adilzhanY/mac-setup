# Enogon v2 (mgpro 3.0.0), after the user's review of v1

v1 (below, kept for the record) was rejected: AI-like music and sounds, audio holes from -24 dB dips, slow and boring (40.8 s, a 5 s building hold, a roof that hovered), a robotic cursor, chunky wall blocks instead of a traced line, and an x-ray crossfade from the house into the logo. v2 keeps the thread and the copy and changes the rest:

- 25.1 s at 112.5 BPM (32 frames a beat); every scene overlaps the next; a visible change every 1 to 3 s.
- The AI traces like Bauwerk's final ad, in Enogon's style: one continuous apricot line round the outline with square CAD handles at the corners, inner walls, door arcs, rooms with black tags, then the lines thicken into walls (about 3 s).
- Storeys land 0.5 s apart, the roof falls in one move; "Ihr Gebäude, in 3D." holds 1.8 s with dimensions.
- The cursor follows a spring (Cap's mellow preset), tilts with speed, smears when fast, squashes on presses, enters and leaves through the frame edges; the dragged card rides it and tilts.
- Export packs the model: the box net is laid flat around the house, four sides fold up, the lid closes, the closed box is the Enogon cube; one opaque move; the logo holds 1.5 s.
- Score: bossa_electronica in F major on recorded CC0 instruments (no four on the floor, no dips); effects are recordings only (clicks, paper and wood thuds, swishes); the rooms fill as marimba notes; the sonic logo is C F A on vibes over a felt Fmaj7 on the logo frame.
- Frames: `src/timeline.ts` (F); cues: `audio/cues.py` reads `src/events.json`.

---

# Enogon: "Grundriss rein, CAD-Modell raus." (mgpro 2.0.0)

## Brief

- **Product**: Enogon (enogon.com, a product of 20° GmbH, Potsdam). Energy consultants (Energieberater) upload a floor plan; the AI recognises walls, doors (openings) and rooms; storeys stack into a 3D CAD model; one click exports it (to HottCAD, shown only as a button called "Export").
- **Viewer**: an energy consultant who today redraws every building by hand before a heat load calculation or a renovation roadmap. They must feel: this takes my most tedious hour away, and the model is precise.
- **Destination**: website hero, LinkedIn and YouTube (no answer needed; the user said not to ask). 16:9, 1920x1080, 60 fps, stereo, -14 LUFS, true peak -1 dBTP. No platform button, so the end card carries the URL.
- **Length**: about 40 s (the user found 30 s too fast and 60 s too slow for this; 17.5 bars at 102.86 BPM = 40.8 s).
- **Language**: German. On screen copy only, no voice over.
- **Copy rules** (from enogon.com): the product says "Die KI erkennt Räume, Wände und Öffnungen", "Anklicken, anpassen, fertig.", "Adresse und Grundrisse rein, CAD-Modell raus. In 10 Minuten." The film uses the product's own wording. It never claims the seconds we show are the product's speed; the only speed claim is the product's own "In 10 Minuten", on the end card.
- **Tokens** (from enogon.com CSS): paper #FFFFFF, ink #000000, apricot 100 #FEE6D8, 300 #EFB694 (primary), 400 #E7A780, 500 #DE8F5E (cube top), 600 #BD703F (hatch), Türkis 100 #E5F3F6 (surface), 200 #CDE7EB (room), 300 #9BC7CE, 500 #1E7F8C (cube depth), 700 #045E68, line #E2E4E8, line strong #9AA3AD, graphit #5C5C5C. Fonts: Tektur 700 (wordmark only), Inter Tight (display and UI), IBM Plex Mono (labels, numbers, uppercase tracking). Sharp corners, 1.5 to 2 px black strokes, flat fills, hatching, dimension lines with 45 degree ticks. No gradients, no glow, no rounded cards.
- **Logo**: an isometric cube, top #DE8F5E, right #1E7F8C, left white, black stroke with round joins; wordmark "Enogon" in Tektur 700 (exact paths from the site's SVG).
- **Interaction**: a web app, so the user's own macOS-White cursor (`public/cursor`), hand over buttons, grab while dragging.
- **Real data**: the site's example building "Lichtpausweg 7, 14467 Potsdam", 12,40 m wide, 4 Geschosse (EG, 1.OG, 2.OG, DG), wall AW 008 (Außenwand, EG, Süd) 0,36 m thick and 2,87 m high. The plan below is drawn for it (a two flat Mehrfamilienhaus with a central stair).

## The thread

**One sheet of paper becomes a building, and the building becomes the logo.** Every scene is the same object changing state: a scanned drawing, then lines the AI draws over it, then walls with thickness, then storeys in 3D, then a model you can click, then a file, then the Enogon cube (which is literally a box in the model's own three colours). No cuts between places: one continuous camera from top down to orbit to the logo.

Why it is not Bauwerk again: Bauwerk's AI was a rainbow glow over a sepia plan inside a city. Enogon's AI is a draftsman: black construction lines, apricot strokes laid with a ruler, dimension ticks, the product's own technical drawing language. No glow, no gradient, no city.

## Scenes, options and choices

### Scene 1: Grundriss rein (0 to 4.67 s, bars 0 to 2)
Options:
1. A crumpled scan unfolds itself on a white desk, then flies into the app.
2. The cursor drags a PDF thumbnail from the left into a dashed drop zone; on release the thumbnail grows into the full sheet, lying flat on the drawing table.
3. A photocopier style light bar passes over an empty sheet and leaves the old drawing on it.
4. The sheet slides in edge first, fast, like it was thrown on a table, and lands with paper weight.
Chosen: 2, with the paper weight of 4 on landing. It is the real action (upload) and gives the cursor one clear job.

### Scene 2: Die KI zeichnet mit (4.67 to 11.67 s, bars 2 to 5)
Options:
1. A scan line sweeps top to bottom; everything it passes turns into vector lines.
2. A drafting crosshair travels wall to wall; each wall is laid as a thick apricot stroke along a ruler, with its length ticking in mono; doors swing open as arcs; rooms fill Türkis 200 one after the other with their names.
3. All walls appear at once as dashed construction lines, then each solidifies in turn.
4. The old pencil lines lift off the paper, straighten in the air and drop back as clean vectors.
Chosen: 2, with the dashed construction lines of 3 as the first beat (the AI "sees" before it draws). It is the product's own visual language (dimension lines, apricot selection) and shows walls, doors and rooms as separate results, matching the copy.

### Scene 3: Geschoss für Geschoss (11.67 to 18.67 s, bars 5 to 8)
Options:
1. Cut to a finished 3D model.
2. The camera tilts from top down to a 40 degree oblique while the ground floor walls rise out of the traced lines to 2,87 m; then 1.OG, 2.OG and DG descend from above and land storey by storey, each with its chip in a storey stack like the app's (EG, 1.OG, 2.OG, DG).
3. The plan duplicates upward like a stack of transparent sheets, then the sheets become floors.
4. Walls rise like a wave from one corner around the house.
Chosen: 2 (the tilt starts before the rise, `craft.md`), with the rise travelling around the house like 4 so it is a wave, not a lift.

### Dip (18.67 to 19.83 s, half a bar)
Sound dips about 20 dB for about 0.3 s, the camera keeps arcing slowly, the roof hangs half a metre above the walls.

### Scene 4: Das Modell (19.83 to 25.67 s, bars 8.5 to 11)
Options:
1. The roof drops on with the return of the music; the camera orbits 50 degrees around the house; facades show their windows.
2. An exploded view: storeys separate vertically, then close.
3. A section cut slices through the house to show rooms inside.
4. The model spins once on a turntable.
Chosen: 1 with a short taste of 2 (storeys breathe apart by 12 cm and close as the roof lands). An orbit is how the product's 3D view is used, and the roof landing is the result moment.

### Scene 5: Anklicken, anpassen, fertig (25.67 to 30.33 s, bars 11 to 13)
Options:
1. The cursor clicks the south wall of the ground floor; it fills apricot; a floating property card (AW 008, Wandstärke 0,36 m, Höhe 2,87 m) slides in; the height field changes value.
2. The cursor drags a wall outward and the whole model adapts.
3. A tree of components (DG, 2.OG, 1.OG, EG) unfolds and the wall is picked from it.
Chosen: 1. It is the app's real interaction (click, panel, edit), uses the site's real example values, and never invents a feature.

### Scene 6: Export (30.33 to 35.0 s, bars 13 to 15)
Options:
1. A big "Export" button; the cursor presses it; the model folds into a file card that drops down.
2. The button fills like a progress bar, then a check and a summary row: 4 Geschosse, Außenwände, Öffnungen, Räume, counted from the model.
3. The model lines flow into the button.
Chosen: 2, ending with the model shrinking towards the camera's centre (handing over to the end card). Real counts from our plan, not invented numbers.

### Scene 7: End card (35.0 to 40.8 s, bars 15 to 17.5)
Options:
1. The building simplifies into a box, the box becomes the Enogon cube; the wordmark builds next to it; "Grundriss rein. CAD-Modell raus." then "enogon.com".
2. A plain fade to the logo.
3. The cube is drawn line by line like the plan was.
Chosen: 1 (the object hand over closes the thread), drawn with the black outline stroke growing on like 3.

## Shot cards

| Scene | Meaning | Space and camera | Text (exact) | Sound |
|---|---|---|---|---|
| 1 | the input is just a floor plan | white paper stage with a faint 1 m grid; top down, slow drift and push 4 percent | "Grundriss rein." (Inter Tight 600, 96 px) | quiet opening, paper slide, soft land (paper, low thump) |
| 2 | the AI understands the drawing | top down, slow drift towards the centre, focus on the active wall | "Die KI erkennt" then "Wände." "Türen." "Räume." each on its result | dashed lines: soft pencil ticks (ambient, varied); each wall: a short ruler stroke (support); rooms: soft wood tones in key (support); last room: hero |
| 3 | the plan becomes a building, storey by storey | tilt 88 to 38 degrees, orbit az 0 to 24, distance eases out | "Geschoss für Geschoss." with the storey stack EG 1.OG 2.OG DG on the right | walls: a rising airy body; storeys landing: three distinct weights (hero on DG) |
| dip | breath before the result | arc continues | none | dip, then a return about 9 dB up |
| 4 | the full model | orbit az 24 to 70, slight push | "Ihr Gebäude in 3D." | roof land (hero), music full |
| 5 | you can edit everything | push towards the south wall; cursor | "Anklicken, anpassen, fertig." + property card | click (support), card slide (ambient), value change ticks |
| 6 | out it goes, as CAD | pull back; Export button large in the right third | "CAD-Modell raus." + button "Export", then summary | press (support), fill (riser into), check (hero) |
| 7 | brand | the model becomes the cube in the centre | "Enogon", "Grundriss rein. CAD-Modell raus.", "enogon.com" | logo sting from the film's own motif, ring out, silence in the last 0.2 s |

Risk probe first: the tilt from the corner pinned 2D plan to the three.js walls (scene 2 to 3), because the SVG plan and the 3D walls must sit on exactly the same lines through the camera move.

## Timeline (60 fps, 102.86 BPM: a beat is 35 frames, a bar 140)

Frames come from `src/timeline.ts`; `scripts/events.ts` writes them to `src/events.json`, and `audio/cues.py` reads that file, so picture and sound share one source.

| Time | Frames | Section | Picture | Sound (weight) |
|---|---|---|---|---|
| 0.0 to 2.3 s | 0 to 140 | open | drop zone, "Grundriss rein.", the cursor grabs Grundriss_EG.pdf and drags it in | soft opening (2.4 LU under), drop zone panel (ambient), grab tap and paper slide (support, ambient) |
| 2.3 to 3.2 s | 140 to 192 | open | the card grows into the sheet with the scan on it, lands with paper weight | paper card and paper land (support) |
| 4.7 to 5.3 s | 280 to 315 | scan | dashed construction lines through every wall | strings ostinato enters; nothing on the lines |
| 5.3 to 7.5 s | 315 to 450 | scan | eight exterior walls laid in apricot, reticle with the wall id and length, counters | a short paper swish per wall, alternating direction (support) |
| 7.5 to 9.6 s | 450 to 577 | scan | inner walls, eleven doors swing, windows marked | taps (ambient, every second wall), rising blips per door (ambient) |
| 9.6 to 11.4 s | 577 to 686 | scan | ten rooms flood Türkis with names and areas; "Wände. Türen. Räume." | a wooden chip per room in the key (support) |
| 11.7 to 16.0 s | 700 to 962 | rise | the camera tilts from top down to 40 degrees, the ground floor rises in a wave, "Geschoss für Geschoss.", storey stack | a long whoosh on the tilt, a reverse swell into the rise (support) |
| 16.0 to 18.4 s | 962 to 1102 | rise | 1.OG, 2.OG and DG land, heavier each | three wooden lands, growing in size (support) |
| 18.7 to 19.8 s | 1120 to 1190 | rise, dip | the roof hovers; dip of an eighth of a bar | the music dips about 24 dB for 0.3 s |
| 19.8 s | 1190 | model | the roof lands | **hero**: wooden impact, taiko and crash, the music returns about 9 dB louder |
| 20.1 to 25.7 s | 1208 to 1540 | model | orbit, "Ihr Gebäude, in 3D.", dimension lines 12,40 m and 2,87 m | two ticks on the dimensions (ambient) |
| 25.7 to 30.3 s | 1540 to 1820 | edit | push to the south wall, the cursor clicks AW 008, the property card, Wandstärke 0,36 to 0,48 m, the new layer grows; "Anklicken, anpassen, fertig." | click, panel, field tap (support), typing taps and a toggle (ambient) |
| 30.3 to 35.0 s | 1820 to 2100 | export | pull back, the Export button, press, fill, check, summary 4 Geschosse, 45 Wände, 67 Öffnungen, 30 Räume; "CAD-Modell raus." | pop, click (support), riser into success (support), summary ticks (ambient) |
| 35.0 to 36.8 s | 2100 to 2205 | end | the house folds into the Enogon cube while the lens goes long (isometric) | transition (support) |
| 36.8 to 40.8 s | 2205 to 2450 | end | the 3D cube hands over to the flat logo, the wordmark, "Grundriss rein. CAD-Modell raus.", enogon.com, fade in the last 12 frames | **hero**: logo sting from the hook, ring out |
