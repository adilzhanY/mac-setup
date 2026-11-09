# Rights: what may be in the film

A commercial is published. Anything in it that the user has no right to use can get the film taken down, the app pulled from a store, or a claim against the user. The safe default of this skill is that everything is drawn in code, and every note is written in code and performed by recorded instruments and effects whose licence is CC0 or equally clear (below), with synthesis where no recording exists. Nothing else third party goes in.

## Before building, list every asset

For each thing the film shows or plays, write where it comes from and on what terms. If the answer is "I don't know", it does not go in.

## Safe

- **Drawn in code**: shapes, UI parts, charts, particles, 3D geometry, gradients, grain. The core of every film.
- **Audio written in code**: the music is composed in code (`audio/score.py` and the kit audio library) and performed by the CC0 instruments that `fetch_instruments.sh` installs (VSCO 2 CE, VCSL, Karoryfer and Versilian SFZ instruments, FreePats Upright Piano KW) in a Voxengo room (royalty free for any purpose, commercial included), with synthesis for anything they do not cover. Effects are premade, human recorded sounds found for each film from the cleared free sources in `sfx-sources.md` (table 1), the CC0 library below included, synthesized only for a signature or where no search fits (`sfx-selection.md`). Never loops, stock music or finished music from a library: the notes are always this film's own (Enogon review, `sound.md` section 4b).
- **The product's own assets**: its logo and wordmark, its colours, its UI, its copy, its data. Check the logo is really the product's (the user's own, not a placeholder from a template).
- **Permissive fonts**: SIL OFL fonts (Space Grotesk, IBM Plex Sans, Geist, Inter) through fontsource. Check the licence field of the package when in doubt.
- **Permissive icon sets**: Lucide (ISC), Tabler (MIT), Material Symbols (Apache 2.0). Use the set the product uses.
- **Public data with a licence that allows it**: OpenStreetMap (ODbL, attribution in the credits if shown as a map), official open geodata (LoD2), datasets whose licence the project already records.

## Not safe, do not use

- **Animations and images of unknown origin**, even if they sit in the product's repo. A Lottie downloaded from a marketplace, a recoloured or vectorised derivative of one, demo GIFs mirrored from an API. Being in the repo is not a licence. torq's own docs flagged its streak Lottie (unknown source) and its exercise GIFs (no media licence); the film used neither.
- **Store badges and platform marks**: "Get it on Google Play", "Download on the App Store", Android robot, Apple logo. They have strict brand rules and imply a listing that may not exist. Write "For Android" or "For iPhone" in the product's own type instead.
- **Other companies' logos and products** (gym equipment brands, a competitor's UI, a payment provider's logo).
- **Real people**: names of public figures, faces, voices, likeness. Real colleague names only when the user supplies them.
- **Stock footage, stock music, sample packs of unknown licence, sounds ripped from operating systems** (the macOS "sent" swoosh, the iPhone keyboard click). Use a cleared recording instead (`sfx-sources.md`). Sound libraries are sorted in "Sound effects from a library" below.
- **Instrument libraries that exclude advertising or need a credit**: Sonatina Symphonic Orchestra is under CC Sampling Plus 1.0, which states "All advertising and promotional uses are excluded" ([CC legal code](https://creativecommons.org/licenses/sampling+/1.0/legalcode)); Virtual Playing Orchestra embeds Sonatina samples, so it inherits that unless every patch is verified file by file; Spitfire LABS lives behind a Splice account with no headless Linux route. CC BY libraries (Salamander Grand Piano, Naked Drums) are legal but need a credit; prefer the CC0 set. The checked list is in `sound.md`, section 4b.
- **Fonts without a clear licence** or desktop fonts the user owns but cannot embed.
- **Copyrightable text** that is not the product's own (instructions copied from a dataset, song lyrics, quotes).

## Sound effects from a library

**Found per film (changed 31 October 2026).** Every effect is a premade, human recorded sound that the agent finds for this film from a free source whose licence covers a client ad with no credit, the way a video editor does (`sfx-selection.md`); physical events were already recordings after the Enogon review, because professionals rated library samples 13.8 to 34.8 percent above procedural sounds in a 2026 study (`sound.md`, section 4b). Synthesis stays for a signature sound and for a job no search can fill. Pick different files from the last film so no two films share a transient (under 10 percent of strong onsets, `sound.md` section 8). Say in the reply which recordings the film uses.

**The sources and their clauses are in `sfx-sources.md`**, read from the licence pages on 31 October 2026, in three tables: safe for client ads without credit (the CC0 library, Kenney, Freesound CC0, Sonniss GDC, Mixkit, Pixabay, 99Sounds, BOOM free packs, Soundly Free, SoundJay, SoundGator, Sound Digitator, SoundResponse, Fiftysounds, Remotion's CC0 files, Sonic Pi); usable only with a credit, a paid plan or one tool (Zapsplat, Freesound CC BY, the CC BY UI packs, freesfx.co.uk, Free To Use Sounds, Uppbeat, A Sound Effect, AEJuice, Adobe Stock, Apple content, the Fairlight library, CapCut, Canva, the AI generated BudgetPixel and ElevenLabs, the paid libraries); and excluded (BBC RemArc, Freesound CC BY-NC and Sampling+, the CC BY-NC "Sound Pack for Motion Designers", the YouTube Audio Library outside YouTube, Partners In Rhyme, Videvo, unconfirmed free tiers, Gumroad editor packs with no written licence, soundcn's Blizzard sounds, operating system sounds, Remotion's meme sounds and `ding.wav`). A source not in table 1 goes in only when the user says its condition is met.

### The clause traps

1. **No stock sound as a sonic logo.** Pixabay bars use "as part of a trade-mark ... or service mark", Adobe bars audio in "logos or ... branding material", CapCut bars use "as a ... logo"; Mixkit and Soundsnap ban Content ID registration. The sonic logo is composed for the film; a found sound may only sit under it as a non tonal layer.
2. **No raw files in templates or shared repositories unless CC0.** Mixkit ("in a tool or template"), Sonniss ("project template"), 99Sounds (no redistribution "(even for free)") and Adobe forbid it. A non CC0 file lives only in the film's `public/sfx/`, kept out of git with `ASSETS.txt` committed as its manifest, never in `templates/examples/` or the skill repo; a client receives the rendered film, not the audio folder.
3. **Pixabay forbids "bulk, large-scale or systematic copying"** and automated collection for machine learning: pick by hand, a few files per film. Mixkit, 99Sounds, BOOM and Zapsplat are browser flows too, never scraped.
4. **The Fairlight library only inside DaVinci Resolve, CapCut materials only inside CapCut** (and one non commercial CapCut item makes the whole project non commercial): neither can go into a Remotion film.
5. **CC0 and user upload sites promise nothing about provenance**; only Sonniss warrants non infringement, and a Pixabay ambience reportedly failed Epic's content review. Prefer curated sources and named recordists. Content ID risk for short effects is low (the registrations found concern music), the real risk is a re uploaded commercial sound.

Sonniss binds each file to the licence version current on its download date, and on Freesound the licence is per sound, so the record of every file carries its source page, author, licence and version and download date (`sfx-sources.md`, section 6).

### The skill's CC0 library

`sfx/` holds 1126 sounds from 30 packs, every one CC0 1.0 (https://creativecommons.org/publicdomain/zero/1.0/): no attribution, commercial and advertising use allowed, no share alike, no non commercial clause. Each pack folder holds its licence file; the per pack table (author, source page, licence) is in `sfx/README.md`. It is one source among those in `sfx-sources.md`, already on disk, and thin on pops, whooshes and risers.

| Source | Packs | Licence evidence |
|---|---|---|
| Kenney (kenney.nl) | ui-audio, interface-sounds, impact-sounds, digital-audio, casino-audio, rpg-audio, sci-fi-sounds, music-jingles | `License.txt` in every zip: "License (Creative Commons Zero, CC0) ... You may use these assets in personal and commercial projects. Credit (Kenney or www.kenney.nl) would be nice but is not mandatory." |
| OpenGameArt | 21 packs (swishes, click clips, pops, UI feedback, bells, sci fi, breaking and hits, and more) | each page's "License(s)" field lists CC0 and nothing else; packs listing several licences were left out |
| Remotion SFX | 5 files | the CC0 originals from Freesound that Remotion mirrors; each attribution line on remotion.dev reads "License: Creative Commons 0" |

### Rules for every found sound or sample in a film

1. It is copied into the film's `public/sfx/` under a role and source name (`click-<author>-<id>.wav`); `samples.py` does this for library picks. A cue's `"file"` may read the CC0 library directly while drafting, but the final film holds every file it plays, so it renders without `~/.local/share`.
2. It has a line in `public/sfx/ASSETS.txt`: file, source and author, source page, licence and version, download date, what was done to it, and for anything not CC0 that it is kept out of git (`sfx-sources.md`, section 6). No credit goes on screen; every file is listed in the reply.
3. Every repeated role draws from a pool of different recordings, and every use is varied and transformed to this film (`sfx-selection.md`, section 8; `sound.md` section 8). Do not use the files the last film used; the shared transient check still applies.
4. CC0 is only as clean as the uploader: the waiver says the work comes "as-is" and the affirmer "disclaims responsibility for clearing rights of other persons". Kenney (one author, self made) is low risk; single uploads on Freesound, OpenGameArt or Pixabay carry a small risk of re uploaded material, which is why the source of each file is recorded.

## Downloaded 3D models and generated images

They are not part of the default, which stays "drawn in code". When a brief needs one, it may go in only with a licence you can point to for that exact file or output, and one that covers a published commercial (a free plan without a commercial licence, such as Krea Free or Recraft Free, does not). The vetted sources and the traps are in `models.md` and `images.md`. List each one in the reply: source, author, release or version, terms and the date you checked them.

## Claims are rights too

- No statistic the product cannot back. Numbers on screen come from the product's data or are clearly the example user's (their 140 kg bench).
- Keep the product's required wording (torq: "of competitive lifters", never "of people").
- No availability claim the docs do not support (no "Now on the App Store" before it is).

## When a needed asset is not clean

Redraw it. A streak creature, a trophy, an exercise demo, a mascot: draw a simple original in SVG or three.js in the product's style. If redrawing it would take the film off course, drop the shot and say so in the reply.

## Say it

In the final reply, name anything left out for rights reasons and why, in one line each, so the user can supply a cleared version if they have one. List every found sound and sample in the reply too (file, source and author, licence).

Sources for the sound licences: `sfx-sources.md` and `research/free-sfx/` (checked 31 October 2026); the earlier check of 27 October 2026 is in `sound-research.md`, section 15.
