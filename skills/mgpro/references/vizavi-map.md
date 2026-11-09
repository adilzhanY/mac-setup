# vizavi-motion → mgpro: where every item now lives

vizavi-motion 1.6.1 (`~/.claude/skills/vizavi-motion`, in Russian) was merged into mgpro in October 2026. Every rule, method, number, checklist item, workflow step and source it contains is listed below with its status in mgpro before the merge and where it lives now.

Status before the merge: **covered** (mgpro already had the same idea), **partly** (mgpro had some of it), **lacked**, **contradicted** (mgpro had an opposing rule; mgpro's rule stays the default and vizavi's is recorded as an option). Sound content was held back by design and merged into `sound.md` and `music.md` after the separate sound research (Oct 2026); the holding file is gone.

**Nothing was dropped.** Five items contradicted mgpro (S5, M3.6, RE.10, RE.12, D3.12); each is kept as an option next to mgpro's default, which rests on a lesson the user taught: Remotion is the stack every film, the kit and every lesson were built on; the destination decides size and frame rate (the Sendoku lesson, "ask first"); a published commercial uses nothing licence protected (the torq lesson). MS.28 was in partial tension with mgpro's old rule "every visual event has a sound"; the sound research replaced that rule with a hierarchy (hero, support, texture, none) that agrees with it (`sound.md` §2 and §7).

## SKILL.md (core)

| # | vizavi item | Before | Now in mgpro |
|---|---|---|---|
| S1 | Three mechanics are the core; modules help them, are not a template | partly | `SKILL.md` intro (vizavi-motion bullet), Golden rules (Depth, Direction before code, The first build is a draft) |
| S2 | The explicit brief, format, length, sound and allowed resources beat defaults | covered | `intake.md` After the answers (Notes win); `brief.md` intro |
| S3 | A simple idea is enough; make staging calls yourself; no technical questionnaire | partly | `brief.md` intro; `intake.md` already forbids technical questions. mgpro's two intake rounds stay (Sendoku lesson: the user asked the skill to ask first) |
| S4 | Never invent real product properties, prices or confirmed preferences | partly | `SKILL.md` Real over fake; `brief.md` intro |
| S5 | Default to plain HTML, CSS, JS, SVG or Canvas with its own timeline; libraries only when needed; no deps up front | contradicted | `pipeline.md` Project, "When Remotion is not the right tool" (option; Remotion stays default) |
| S6 | Version 1.6.1, display name vizavi_motion | n/a | `research.md` vizavi-motion |
| M1.1 | Lively, rich, detailed animation | covered | `SKILL.md` intro (After Effects bar) |
| M1.2 | Camera moves continuously while the story is active: smooth acceleration and braking, coherent path, motivated tilts, diagonals, rolls, fly arounds | partly | `craft.md` Camera, "The camera keeps moving, through depth"; `SKILL.md` Golden rules, Depth |
| M1.3 | Perspective depth, foreground, middle and background moving against each other; one linear zoom of a flat frame does not count | lacked | `craft.md` Depth and layers; Camera subsection |
| M1.4 | A technical pause or the final readable frame needs no pointless motion | partly | `craft.md` Camera subsection (reading phase bullet) |
| M1.5 | Type takes part in the action (typeface, plasticity of letters, words, space) | partly | `craft.md` Kinetic type |
| M1.6 | Objects have weight, inertia, material, light, contact, secondary reactions | lacked | `craft.md` Weight, form and secondary action |
| M1.7 | Vary accents and shot size without long holds or chaotic flicker; richness through hierarchy, not by removing the environment | partly | `craft.md` Weight, form and secondary action |
| M1.8 | Motion blur from relative motion, controlled depth of field in spatial and close shots | partly | `craft.md` Optics; `SKILL.md` Golden rules, Depth; checklist |
| M1.9 | Radial blur for cards or deep scenes when needed; it replaces neither DOF nor motion blur | lacked | `craft.md` Optics |
| M1.10 | Keep readability and recognisability | covered | `craft.md` Readability, Optics |
| M1.11 | Music and sound design by default, in sync; silence when the brief says so; never call a silent film scored | partly | `sound.md` §2 The sound plan comes first |
| M1.12 | Now and then tie cuts and actions to expressive accents of the real music, not every beat | partly | `sound.md` §6 (cut on accents, sometimes); `music.md` The music serves the picture |
| M2.1 | One original thread and a full dynamic storyboard before the full build | partly | `storyboard.md` §2; `SKILL.md` workflow 8 |
| M2.2 | 3 to 5 substantially different options per scene; pick the strongest for the whole | lacked | `storyboard.md` §3; `SKILL.md` workflow 8, Golden rules |
| M2.3 | Short options, the choice and a practical storyboard are enough; no reasoning written out | lacked | `storyboard.md` §3 |
| M2.4 | Every shot fixes accent, composition and layers, action, text and its motion, camera, light and focus, entry, exit, sound and rhythm | partly | `storyboard.md` The shot card |
| M2.5 | Scenes develop the story causally | lacked | `storyboard.md` §3 |
| M2.6 | Circle, letter O or portal is one possible device; never repeat it by habit | lacked | `storyboard.md` §3 |
| M2.7 | Two or three devices may combine into one action | lacked | `storyboard.md` §3 |
| M2.8 | Probe the main technical or artistic risk before the expensive build | partly | `storyboard.md` Probe; `pipeline.md` Review loop; `SKILL.md` workflow 12 |
| M3.1 | The first build is an internal unfinished draft, never handed over as final | partly | `review.md` The first build is a draft; `SKILL.md` workflow 13, Golden rules |
| M3.2 | Review the whole film, each scene and join; with sound listen to music, effects, the mix | partly | `review.md` The first build (picture); `sound.md` §17 Checking without ears (listening) |
| M3.3 | Check meaning, boring holds, pace, camera, readability, form, artefacts, joins, sync | partly | `review.md` What to check |
| M3.4 | Fix the causes; recheck the changed parts and the whole | partly | `review.md` Fix, recheck, finish |
| M3.5 | Never claim the skill works from its instructions or one good frame | lacked | `review.md` Honest statuses |
| M3.6 | Default delivery MP4 1920x1080, 60 fps, H.264, yuv420p, AAC; sources extra; 4K on request; HTML preview is not the video | contradicted | `pipeline.md` Finishing (used when the destination decides nothing); `destinations.md` stays the default |
| M3.7 | Check the decoded final export, its start, end, scene boundaries and parameters; code, contact sheet and frame counter do not replace perception | lacked | `review.md` Check the decoded export; `pipeline.md` Finishing; `SKILL.md` workflow 14 |
| M3.8 | A missing tool: name the unchecked property, deliver with that status | partly | `review.md` Honest statuses |
| M3.9 | Finish when significant defects are fixed and the brief is met; taste alternatives need no endless rework | lacked | `review.md` Fix, recheck, finish |
| M3.10 | Optional modules only when the task needs them (video refs, images, 3D, product UI, styles) | lacked | `SKILL.md` Read what you need table |
| M3.11 | The six demo parts apply only to that demo | lacked | `styles.md` |

## storyboard.md

| # | vizavi item | Before | Now in mgpro |
|---|---|---|---|
| SB.1 | Storyboard before the full film; turns an idea into staging | partly | `storyboard.md` intro |
| SB.2 | Step 1: extract goal, viewer, key idea, copy, format, length, sound, resources, outputs; invent nothing, decide reversible things yourself | partly | `storyboard.md` §1 |
| SB.3 | Step 2: one thread; never copy an earlier film's sequence | lacked | `storyboard.md` §2 |
| SB.4 | Step 3: 3 to 5 options differing in action, space, metaphor or transition; colour or font alone is not an option; choice plus short reason | lacked | `storyboard.md` §3 |
| SB.5 | Step 4: fill all shots and joins, check reading times and risks; a working plan, not a queue of approvals; respect an asked approval | partly | `storyboard.md` §4 (with intake's "Check the script with me first") |
| SB.6 | Shot card: time and meaning, states and action, space, text, camera and optics, joins, sound, check | partly | `storyboard.md` The shot card |
| SB.7 | Design transitions with both scenes: match cut (silhouette, scale, orientation, direction), a real mask, one location continuity | partly | `storyboard.md` Design a transition |
| SB.8 | Probe in real quality and motion, with sound; length by need, no fixed 5 to 7 s; replaces neither storyboard nor review | lacked | `storyboard.md` Probe; sound side `sound.md` §2 |

## motion-and-sound.md

| # | vizavi item | Before | Now in mgpro |
|---|---|---|---|
| MS.1 | Apply per storyboard; the goal is quality, not every tool at once | lacked | `craft.md` Optics intro |
| MS.2 | Separate path, speed, orientation, target, FOV, focus | partly | `craft.md` Camera subsection |
| MS.3 | One long path with speed waves; no chain of ease in outs stopping on every accent | lacked | `craft.md` Camera subsection |
| MS.4 | At joins check position, direction, screen speed, acceleration | partly | `craft.md` Camera subsection; `review.md` What to check |
| MS.5 | In the reading phase a big travel becomes a calm arc or drift | lacked | `craft.md` Camera subsection |
| MS.6 | Tracking the hero goes with clear parallax | lacked | `craft.md` Camera subsection |
| MS.7 | A meaningful cut between places needs no continuous world coordinate | lacked | `craft.md` Camera subsection |
| MS.8 | Layers differ in scale, relative motion, overlaps, perspective | lacked | `craft.md` Depth and layers |
| MS.9 | Protect silhouettes and text from accidental overlap | partly | `craft.md` Depth and layers |
| MS.10 | A label by a moving 3D object follows its anchor's projection, keeps margins, no jitter or lag | partly | `craft.md` Depth and layers; `three.md` World space and screen space |
| MS.11 | Motion blur is relative screen motion; tracked hero sharp, background smeared; sub frame sampling is not proof; weakens when braking | partly | `craft.md` Optics |
| MS.12 | Depth of field: focus follows the detail; near and far may go soft; never fake unreadability in flat UI | partly | `craft.md` Optics |
| MS.13 | Radial or zoom blur is a stylised accent, never the maximum blur on the whole film | lacked | `craft.md` Optics |
| MS.14 | Form reads through geometry, light, normals, thickness, contact shadow, overlaps; highlights, grain, particles do not fix it | lacked | `craft.md` Weight, form and secondary action |
| MS.15 | Pick an expressive available typeface; check glyphs, Cyrillic, weight, breaks, file licence; system fonts or drawn geometry if external fonts are banned | partly | `craft.md` Kinetic type |
| MS.16 | Readable final layout first, then the letters' action (assembly, width, masks, space, object); every effect has a job | lacked | `craft.md` Kinetic type |
| MS.17 | Anticipation, action, contact, reaction, settle with different masses and curves | lacked | `craft.md` Weight, form and secondary action |
| MS.18 | One main accent with coordinated secondary layers; change phase, scale, depth, contrast when all compete | partly | `craft.md` Weight, form and secondary action |
| MS.19 | Never save the pace by cutting required elements or by unreadable speed | lacked | `craft.md` Weight; `review.md` Fix |
| MS.20 | Repeated flashes are not energy | lacked | `craft.md` Weight; `review.md` Flashes |
| MS.21 | Music and effects part of the staging from the start unless silent; method free; character matters | partly | `sound.md` §2; `music.md` The music serves the picture |
| MS.22 | Music needs motif or groove, development, contrast, ending; whooshes and hits are not a composition; effects tied to motion, contact, material | partly | `music.md` The music serves the picture; `sound.md` §2 |
| MS.23 | Sound and picture from the same events; recompute accents after a speed ramp; no accidental tempo or pitch change | partly | `music.md` The music serves the picture; `sound.md` §2 (speed ramps) |
| MS.24 | Listen to the full mix and layers; balance, clipping, clicks, sync, tail; metrics are not musical quality; keep "not made" and "not heard" apart | partly | `sound.md` §17 Checking without ears |
| MS.25 | Plan musical points (note, hit, phrase or harmony change, pause, return) to support cuts, reveals, contact, endings; occasional, not every beat; piano only an example | partly | `sound.md` §6 (cut on accents, sometimes); `music.md` The music serves the picture |
| MS.26 | Accent map from the real track: perceived peak, visual target, nearest frame `frame / fps`; offsets; grid or file start is not enough; check by ear | lacked | `sound.md` §6 (the accent map) |
| MS.27 | When a match fails, adjust gently; meaning, reading, voice and a silent brief beat the beat | lacked | `sound.md` §6 (cut on accents, sometimes) |
| MS.28 | Effects support, complement or leave room; no same whoosh on every transition; update the accent map after edits; never claim perfect sync unchecked | contradicted in part, resolved by the sound rewrite | `sound.md` §2 and §7: the hierarchy that replaced "every visual event has a sound" |

## review-and-export.md

| # | vizavi item | Before | Now in mgpro |
|---|---|---|---|
| RE.1 | A working check, not a certificate | lacked | `review.md` intro |
| RE.2 | First result is a draft; full view at normal speed, then each scene and join | partly | `review.md` The first build is a draft |
| RE.3 | Listen to the full mix and separate layers | partly | `sound.md` §17 |
| RE.4 | Notes as interval → observation → cause → fix → recheck | lacked | `review.md` (in `REVIEW.md`); `pipeline.md` Review loop; `SKILL.md` workflow 13 |
| RE.5 | No faked iterations; if no defects, record what was checked | lacked | `review.md` The first build is a draft |
| RE.6 | Checklist: idea and thread, camera and joins, type, form and artefacts, blur and focus, music and effects, format and requirements | partly | `review.md` What to check; sound side `sound.md` §17 |
| RE.7 | Fix the causes, re-view with neighbouring phases and the whole | partly | `review.md` Fix, recheck, finish |
| RE.8 | After simplifying, compare with the brief; "cleaner" with missing elements is not accepted | lacked | `review.md` Fix, recheck, finish |
| RE.9 | Finish when required is done and checked, defects fixed, only taste left | lacked | `review.md` Fix, recheck, finish |
| RE.10 | Prefer plain HTML, CSS, JS; do not require Remotion; a preference, not a ban; vanilla not always better | contradicted | `pipeline.md` "When Remotion is not the right tool" |
| RE.11 | Web Audio API is not audio.js; no fixed generator; do not rebuild the user's stack | partly | `music.md` The music serves the picture (method free, never rebuild a chosen stack); `pipeline.md` |
| RE.12 | Default MP4 1920x1080, even 60 fps, H.264, yuv420p, AAC; sources extra; 4K on request; never call a file 4K or 60 fps when it is not | contradicted | `pipeline.md` Finishing; `review.md` Check the decoded export |
| RE.13 | Export step 1: every frame at `i / fps`, complete and ordered, never a realtime recording | partly | `pipeline.md` plain route step 1; `review.md` timeline |
| RE.14 | Export step 2: a real mixed audio file through offline render; a realtime preview is not proof | partly | `pipeline.md` plain route step 2; `sound.md` §17 (the decoded file) |
| RE.15 | Export step 3: FFmpeg mux, keep fps and length, map streams, lose nothing, no audio on a silent brief | partly | `pipeline.md` plain route step 3; `sound.md` §17 |
| RE.16 | Export step 4: settle start and tails; never cut the ending; no blind `-shortest` | lacked | `pipeline.md` Finishing |
| RE.17 | Export step 5: check the decoded MP4 (codec, pixel format, size, fps, timestamps, frames, length, AAC, AV sync, start, end, boundaries) | lacked | `review.md` Check the decoded export (`ffprobe` command); sound side `sound.md` §17 |
| RE.18 | If the environment blocks the export: blocker, finished parts, sources and instructions; HTML is not the video; no auto install | lacked | `review.md` When the environment cannot export |
| RE.19 | Decode the final file; first and last frames, frames around every boundary, holds, fastest phases; the kinds of evidence do not replace each other | partly | `review.md` Check the decoded export |
| RE.20 | Sync check against the real track's accents and the decoded frames, including the offset after mux | lacked | `sound.md` §6 (the accent map, rechecked after muxing) and §17 |
| RE.21 | 20 s at 60 fps = 1200 frames on 0 to 1199 over 60; the end point is not a frame; 20 s only an example | lacked | `review.md` Frame count |
| RE.22 | An audio stream is not good sound; silent stream never passes; AAC alone proves nothing | lacked | `review.md` Audio; `sound.md` §17 |
| RE.23 | Same frame after cold seek, rewind, jump; analytic or baked state for simulations; one random seed is not enough | partly | `review.md` A timeline that gives the same frame every time |
| RE.24 | Compare source and output by hash to keep a version | lacked | `review.md` timeline section |
| RE.25 | Never label an earlier weak result "without the skill" when the skill was used | lacked | `review.md` Honest statuses |
| RE.26 | Statuses: implemented, checked by running, seen in frames, checked in motion, listened to | partly ("measured, not heard") | `review.md` Honest statuses table; `SKILL.md` Golden rules |
| RE.27 | Nothing passes from parameters or impression; name the missing check; label the delivered file | partly | `review.md` Honest statuses |
| RE.28 | Impossible quality: exact blocker and finished parts; never hide it after claiming ready | lacked | `review.md` Honest statuses |
| RE.29 | Unclear outcome of an external action: find out before repeating | lacked | `review.md` Honest statuses |
| RE.30 | Do not ask again for permission for allowed reversible work | lacked | `review.md` Honest statuses |
| RE.31 | No repeating strobe; check luminance changes; reduced motion is not flash safety; no standard claims without analysis | lacked | `review.md` Flashes and strobing |

## saas-ui-motion.md (product UI)

| # | vizavi item | Before | Now in mgpro |
|---|---|---|---|
| UI.1 | A conditional module; "SaaS/UI motion" names staging of an interface, not a style | lacked | `interaction.md` "The cursor leads an action"; `research.md` |
| UI.2 | Adapted from the user's Higgsfield archives (handed 15.10.2026, line references); not an official Higgsfield work | lacked | `research.md` vizavi-motion |
| UI.3 | MahdiEdits lessons named, URLs unconfirmed; archive statuses unchecked; principles taken, not implementations, palette, tastes, length, BPM, engine | lacked | `research.md` vizavi-motion |
| UI.4 | Each episode one clear task (pick, change, drag, rearrange, start, show) | lacked | `interaction.md` The cursor leads an action |
| UI.5 | One plausible app with consistent data and states, not a new decorative card per scene | partly | `elements.md` One product across the film |
| UI.6 | Keep the hierarchy, radii, shadows, line widths | partly | `elements.md` One product across the film |
| UI.7 | Few main controls per action (1 to 3, not a quota) | lacked | `interaction.md` Few controls |
| UI.8 | Demo data never shown as real metrics | covered | `elements.md`; `brief.md` §5 |
| UI.9 | Cursor chain: hover → reaction → press or grab → change → readable result | partly | `interaction.md` The chain |
| UI.10 | The hit is the arrow's tip, not the sprite's centre | covered | `interaction.md` (hotspots; The hit) |
| UI.11 | A readable hover before the click, a visible caused change after | partly | `interaction.md` Before a click |
| UI.12 | Cursor sharp and whole when pressing; never covers label, result, numbers | lacked | `interaction.md` Fully visible |
| UI.13 | States in causal order; no success before the process ends | lacked | `interaction.md` States in causal order |
| UI.14 | Indicators of one operation share one progress | partly | `interaction.md` States; `elements.md` counters |
| UI.15 | A shortened wait is not the product's speed; mark it | lacked | `brief.md` §5 |
| UI.16 | Drag: fixed grab point and offset; lift, arc, drop zone lights, shrink into the slot | lacked | `interaction.md` Drag and drop |
| UI.17 | Follow with lag shows weight but never a lost grip; neighbours react after | lacked | `interaction.md` Drag and drop |
| UI.18 | Drop, snap and settle end stable; never the same spring on every layer | lacked | `interaction.md` Drag and drop; `craft.md` Weight |
| UI.19 | Timing by pace, frame and reading; preset: move 0.6 to 0.9 s on a small arc, squeeze on click, off frame entry and exit; not a norm | partly | `interaction.md` Timing |
| UI.20 | A few functional micro reactions | lacked | `interaction.md` Micro reactions |
| UI.21 | Going to a detail is motivated by the action; text gets reading time | partly | `interaction.md` |
| UI.22 | Tie some cuts and reveals to real music and effect accents, not every beat | partly | `sound.md` §6 (cut on accents, sometimes) |
| UI.23 | An object passed between scenes matches position, size, state; no ghost; results grow from their cause; cards on soft arcs | partly | `transitions.md` Passing an object between scenes |
| UI.24 | A morph changes real dimensions, never stretches the whole UI | lacked | `transitions.md` Passing an object |
| UI.25 | Keep the interface's identity from flat to spatial | lacked | `transitions.md`; `three.md` One interface |
| UI.26 | Camera helps the action (follow caret, close in, pull back, around layers); one gesture | partly | `craft.md` Camera subsection |
| UI.27 | 2D, 2.5D and 3D: what must really change in each | lacked | `three.md` One interface in 2D, 2.5D and 3D |
| UI.28 | Carry object IDs, anchors, colours, content, result across the modes (the demo) | lacked | `three.md` One interface; `styles.md` demo |
| UI.29 | World space versus screen space; cursor point from the anchor's projection (camera, viewport, aspect, scale); never mix units | partly | `three.md` World space and screen space |
| UI.30 | Screen labels keep position; world labels follow projection; margins, depth, off camera; volume never covers the overlay cursor or text | partly | `three.md` World space and screen space |
| UI.31 | One controlled timeline; no real input; states from time including rewind; no dependence on mouse events or frame count | partly | `interaction.md` A film, not an app; `review.md` timeline |
| UI.32 | Full functional QA only for a live app | lacked | `interaction.md` A film, not an app |
| UI.33 | Checks: action, grab, drop, progress, identity, modes, projection under camera and rewind, overlays; then the decoded export; code is not the result | lacked | `interaction.md` Check a product UI shot |

## 3d-sources.md and models-3d.md

| # | vizavi item | Before | Now in mgpro |
|---|---|---|---|
| D3.1 | Conditional; research of 16.10.2026; not every file tested; check page and bundled licence; order by task | lacked | `models.md` Sources |
| D3.2 | Poly Haven: glTF, CC0, no sign up; check textures | lacked | `models.md` Sources table |
| D3.3 | Kenney: pick a 3D set, GLB, CC0, "Continue without donating" | lacked | `models.md` Sources table |
| D3.4 | Quaternius: Standard often FBX or glTF, Source may be paid; keep each release's licence | lacked | `models.md` Sources table |
| D3.5 | ambientCG: CC0 scans; check the ZIP; not always GLB | lacked | `models.md` Sources table |
| D3.6 | Sketchfab: downloadable, free, glTF; account needed; no self sign up | lacked | `models.md` Sources table |
| D3.7 | CGTrader: glTF filter, real zero price, "free in subscription" is not free | lacked | `models.md` Sources table |
| D3.8 | KayKit Adventurers: 5 free models, FBX and glTF, CC0; extras paid | lacked | `models.md` Sources table |
| D3.9 | Khronos glTF Sample Assets: licence per asset README | lacked | `models.md` Sources table |
| D3.10 | Quaternius QAL v1.0 (28.08.2026): finished projects yes, standalone assets no; older CC0; keep links, not models, in the skill | lacked | `models.md` Sources and Rights first |
| D3.11 | Poly Pizza restricts automated downloads; pick another, never bypass | lacked | `models.md` Sources |
| D3.12 | A personal download needs no refusal over future commercial use | contradicted | `models.md` Rights first (kept for unpublished films; published commercials follow `rights.md`, torq lesson) |
| D3.13 | Credit the source, author, release and terms at the end | partly | `models.md` Credits; `rights.md`; `pipeline.md` reply |
| D3.14 | Unavailable, paid or unfit: look for the next; free is not any distribution | lacked | `models.md` Rights first |
| M3D.1 | Free models may be fetched for the current request; prefer GLB or glTF when it suits | lacked | `models.md` intro, Before the scene 1 |
| M3D.2 | Check each object's terms; no blanket ban; never forbid showing devices | partly | `models.md` Rights first (other brands' marks stay out, `rights.md`) |
| M3D.3 | Ordinary allowed download only; no bypass, no faking, no self sign up or integration install; invent no services | lacked | `models.md` Rights first |
| M3D.4 | Step 1: exact variant, format, completeness; render the real file | lacked | `models.md` Before the scene 1 |
| M3D.5 | Step 2: units, axes, pivot, normals, thickness, topology, PBR values, colour space, renderer; WebGPU or TSL is not WebGL | lacked | `models.md` Before the scene 2 |
| M3D.6 | Step 3: textures found, alpha, holds at shot size, reduce weight, real render speed and export | lacked | `models.md` Before the scene 3 |
| M3D.7 | Step 4: light, environment, exposure, contact; plastic, metal, glass differ; a highlight never fixes form | partly | `models.md` Before the scene 4; `three.md` Metal on black |
| M3D.8 | Step 5: a laptop's lid rotates around the hinge; check states and no stray underside | lacked | `models.md` Before the scene 5 |
| M3D.9 | Reveal, captions, camera serve one scene; close pass keeps focus and scale, never crosses the near plane; recheck after a swap | lacked | `models.md` In the scene |
| M3D.10 | Credits list sites, files, author, link, format, terms with date, attribution, changes; rights differ per asset; view or download is not resale | lacked | `models.md` Credits and Rights first |

## image-continuity.md and image-providers.md

| # | vizavi item | Before | Now in mgpro |
|---|---|---|---|
| IC.1 | One reference process per hero; keep identity; the same canonical references for every pose; no look-alikes | lacked | `images.md` Keep one hero the same |
| IC.2 | Fix traits, camera, anchors, scale, light, alpha and changes before; align and check anatomy, hands, perspective, light after; record intervals; pose count by task | lacked | `images.md` Keep one hero the same |
| IC.3 | Three poses are not a rotation; crop, zoom, parallax are not a new pose; smooth needs states or geometry; no morph through wrong anatomy | lacked | `images.md` Honest about motion |
| IC.4 | Real PNG alpha; check channel, edges on dark and light, halos, premultiplied; export must not bake it back | lacked | `images.md` Real transparency |
| IC.5 | The image has a role in the action; tie to the storyboard; no passive pan; layers hold under the camera; no invented angle | lacked | `images.md` Give the image a role |
| IP.1 | Only when images are needed; research 16.10.2026; docs only; no integration installed; use an allowed available tool; fall back honestly | lacked | `images.md` Providers |
| IP.2 | Krea MCP endpoint; OAuth units versus a separate paid API balance | lacked | `images.md` Krea |
| IP.3 | Krea Free 100 units a day, about 25 Klein or 5 Krea 3 Beta, not guaranteed edits; no free Nano Banana or GPT Image; read the schema | lacked | `images.md` Krea |
| IP.4 | Krea 3 up to 6 references, untested; commercial licence on paid plans only; no native alpha | lacked | `images.md` Krea |
| IP.5 | Cloudflare Free 10,000 neurons a day, reset 00:00 UTC, no card; neurons are not pictures | lacked | `images.md` Cloudflare |
| IP.6 | FLUX.2 Klein 4B: multipart, up to 4 inputs under 512x512, output 256 to 1920, base64 | lacked | `images.md` Cloudflare |
| IP.7 | REST needs an adapter; the general MCP is unchecked; no native alpha | lacked | `images.md` Cloudflare |
| IP.8 | Gemini web: reference editing, floating limits, not a free API; automation only with a real browser tool | lacked | `images.md` Web interfaces |
| IP.9 | ChatGPT images: web fallback; Free is not an API; asking for transparency is not an alpha check | lacked | `images.md` Web interfaces |
| IP.10 | Leonardo: 150 tokens a day, public, guidance Limited, transparency for SD1.5 and SDXL | lacked | `images.md` Other options |
| IP.11 | Ideogram: 30 credits a week with a login, public, no free API | lacked | `images.md` Other options |
| IP.12 | Hugging Face: $0.10 a month, queues in ZeroGPU, not a production backend | lacked | `images.md` Other options |
| IP.13 | Pollinations: Pollen bought or earned, not unlimited | lacked | `images.md` Other options |
| IP.14 | Recraft Free: no commercial licence | lacked | `images.md` Other options; `rights.md` |
| IP.15 | Replicate and fal: trials are not recurring free | lacked | `images.md` Other options |
| IP.16 | Local ComfyUI MCP, SD1.5 with IPAdapter, rembg; never auto install; Klein 4B needs 8.4 GB, too much for an RTX 3050 6 GB | lacked | `images.md` An optional local route (with this machine's RTX 5070 12 GB noted) |
| IP.17 | Same canonical references; animate a cutout or rig rather than generate each frame; check real alpha | lacked | `images.md` Keep one hero, Real transparency |
| IP.18 | Report provider, model, route, date, terms | lacked | `images.md` Say what was used; `rights.md` |
| IP.19 | VidIQ as an optional future sound source, not free by default, no voice chosen | lacked | `music.md` The music serves the picture (VidIQ); `styles.md` |
| IP.20 | No generation was run while preparing the notes | lacked | `images.md` Say what was used |

## styles-and-sources.md

| # | vizavi item | Before | Now in mgpro |
|---|---|---|---|
| ST.1 | The six parts belong to one demo; unapproved suggestions are not chosen; other films pick from their brief; not a permanent taste | lacked | `styles.md` Approved style cards |
| ST.2 | A style card after explicit approval: name, source and date, grammar, applicability; a language, not a scene order; mechanics stay | lacked | `styles.md` Approved style cards |
| ST.3 | The demo was chosen 16.10.2026; its format and length come from its own brief | lacked | `styles.md` six part demo |
| ST.4 | Pencil sketch part | lacked | `styles.md` table |
| ST.5 | Paper part | lacked | `styles.md` table |
| ST.6 | Pixel part | lacked | `styles.md` table |
| ST.7 | 2D plus UI part | lacked | `styles.md` table |
| ST.8 | 2.5D plus UI part | lacked | `styles.md` table |
| ST.9 | 3D plus UI part | lacked | `styles.md` table |
| ST.10 | The last three keep identity, change only the spatial model | lacked | `styles.md`; `three.md` One interface |
| ST.11 | One fixed screen space indicator through all six parts | lacked | `styles.md` |
| ST.12 | Energetic transitions on real music accents, keeping reading | lacked | `styles.md`; `sound.md` §6 |
| ST.13 | This labelling belongs to the demo only | lacked | `styles.md` |
| ST.14 | Sources researched 16.10.2026, documentation only; VidIQ optional | lacked | `styles.md` Vetted sources; `music.md` The music serves the picture (VidIQ) |
| ST.15 | Add only checked entries (page, availability, account, terms, format, date, method, limits); keep text, preview, download, file and working use apart | lacked | `styles.md` Vetted sources |

## video-references.md

| # | vizavi item | Before | Now in mgpro |
|---|---|---|---|
| VR.1 | A file: real frames and audio; a URL: open it first; never describe from a title; state the access; unavailable: say so and do not attribute | lacked | `video-references.md` Work from the real material |
| VR.2 | Scene and transition map with timecodes (boundaries, shot sizes, layers, action, type, camera, light, join carrier, sound) | lacked | `video-references.md` Map (with `ffmpeg` commands) |
| VR.3 | Dense sequences around important joins; a still cannot give speed, easing or sound; three frames are not an analysis | lacked | `video-references.md` Map |
| VR.4 | Seen in an interval → principle → own decision; keep the source and access; no right to use their assets | lacked | `video-references.md` Observation, then transfer |
| VR.5 | Three references: use all, say what each gives (example split) | lacked | `video-references.md` Combining |
| VR.6 | Note fits and conflicts; one system, not three fragments | lacked | `video-references.md` Combining |
| VR.7 | Adapt palette, logo, materials, hero, world | lacked | `video-references.md` Combining (to the product's tokens) |
| VR.8 | One thread and scale of motion; map reference → quality → use; then the own storyboard; serves the mechanics | lacked | `video-references.md` Combining; `storyboard.md` |
