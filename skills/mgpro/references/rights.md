# Rights: what may be in the film

A commercial is published. Anything in it that the user has no right to use can get the film taken down, the app pulled from a store, or a claim against the user. The safe default of this skill is that everything is drawn in code or synthesized, so nothing third party is needed. Keep it that way.

## Before building, list every asset

For each thing the film shows or plays, write where it comes from and on what terms. If the answer is "I don't know", it does not go in.

## Safe

- **Drawn in code**: shapes, UI parts, charts, particles, 3D geometry, gradients, grain. The core of every film.
- **Synthesized audio**: music and every sound effect generated in code (`audio/score.py` and the kit audio library). No samples, no loops, no stock music.
- **The product's own assets**: its logo and wordmark, its colours, its UI, its copy, its data. Check the logo is really the product's (the user's own, not a placeholder from a template).
- **Permissive fonts**: SIL OFL fonts (Space Grotesk, IBM Plex Sans, Geist, Inter) through fontsource. Check the licence field of the package when in doubt.
- **Permissive icon sets**: Lucide (ISC), Tabler (MIT), Material Symbols (Apache 2.0). Use the set the product uses.
- **Public data with a licence that allows it**: OpenStreetMap (ODbL, attribution in the credits if shown as a map), official open geodata (LoD2), datasets whose licence the project already records.

## Not safe, do not use

- **Animations and images of unknown origin**, even if they sit in the product's repo. A Lottie downloaded from a marketplace, a recoloured or vectorised derivative of one, demo GIFs mirrored from an API. Being in the repo is not a licence. torq's own docs flagged its streak Lottie (unknown source) and its exercise GIFs (no media licence); the film used neither.
- **Store badges and platform marks**: "Get it on Google Play", "Download on the App Store", Android robot, Apple logo. They have strict brand rules and imply a listing that may not exist. Write "For Android" or "For iPhone" in the product's own type instead.
- **Other companies' logos and products** (gym equipment brands, a competitor's UI, a payment provider's logo).
- **Real people**: names of public figures, faces, voices, likeness. Real colleague names only when the user supplies them.
- **Stock footage, stock music, sample packs, sounds ripped from operating systems** (the macOS "sent" swoosh, the iPhone keyboard click). Synthesize an original instead.
- **Fonts without a clear licence** or desktop fonts the user owns but cannot embed.
- **Copyrightable text** that is not the product's own (instructions copied from a dataset, song lyrics, quotes).

## Claims are rights too

- No statistic the product cannot back. Numbers on screen come from the product's data or are clearly the example user's (their 140 kg bench).
- Keep the product's required wording (torq: "of competitive lifters", never "of people").
- No availability claim the docs do not support (no "Now on the App Store" before it is).

## When a needed asset is not clean

Redraw it. A streak creature, a trophy, an exercise demo, a mascot: draw a simple original in SVG or three.js in the product's style. If redrawing it would take the film off course, drop the shot and say so in the reply.

## Say it

In the final reply, name anything left out for rights reasons and why, in one line each, so the user can supply a cleared version if they have one.
