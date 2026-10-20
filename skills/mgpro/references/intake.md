# Ask first: the intake

Before the script, ask the user a few questions with the `AskUserQuestion` tool, in at most two rounds. Each question shows two to four options with a one line description; the tool adds a "Type something" choice by itself, so every question also takes a free answer. Put the option you would choose first and add " (Recommended)" to its label.

Spend a few minutes on the product first (README, store listing, design system, platform), so the options name real features and a real platform instead of placeholders. Never ask what the request, the code or the docs already answer: if the user said "a TikTok ad", the destination is answered; if the product is an unreleased Android app, Apple is not an option.

Do not ask about frame rate, resolution, codec, loudness or safe zones. Those follow from the destination (`destinations.md`).

## Round 1: where, why, what (one call, up to three questions)

**Where will the video be shown?** header `Where`, multiSelect. Order the options by what fits this product; recommend one when the product makes it obvious.

| Label | Description |
|---|---|
| Social feeds (vertical) | TikTok, Instagram Reels, YouTube Shorts, Snapchat. 9:16, 15 to 30 s, nothing important at the bottom or the right edge, works with the sound off. |
| YouTube or website | A 16:9 film for a YouTube video or ad, a landing page or a launch post. 30 to 60 s; short cuts (6 s, 15 s) can be made from it. |
| App store page | The Google Play or App Store preview slot. 15 to 30 s, plays muted, and must be real recordings of the app with captions, not a drawn commercial. |
| TV or big screen | A TV spot, an event screen or a keynote. Exactly 15 or 30 s, broadcast loudness and safe areas. |

The question text ends with: "Type something for anything else, for example a Facebook or LinkedIn feed."

**What should someone do after watching?** header `Goal`, single choice.

| Label | Description |
|---|---|
| Install the app | End on the mark and where to get it (in the store's own slot, no call to action text). |
| Remember the brand | End on the mark and the tagline, no ask. |
| Announce a launch | A date or "out now" at the end, a bigger reveal. |
| Visit a website | End on the URL, held long enough to read. |

Leave out what cannot apply (no "Install the app" for a website product).

**What must the video show?** header `Show`, multiSelect. Three or four of the product's real features, found in the codebase or docs, in the user's words, each with one line on how the film would show it. Recommend the one that only this product has.

Example for a sudoku app: "Hints that teach" (a hint walks through an X-Wing), "Difficulty past Extreme" (eight levels climb into the dark), "No ads, no tracking" (the clean promise, one line per beat), "Daily puzzle" (the same grid for everyone today).

## Round 2: length, feel, music, anything else (one call, up to four questions)

Built from round 1's answers.

**How long?** header `Length`, single choice. Only lengths the chosen destination allows, recommended first:

| Destination | Options |
|---|---|
| Social feeds | 15 s (Recommended), 30 s, 9 s |
| YouTube or website | 30 s (Recommended), 45 s, 60 s, 15 s |
| App store page | 30 s (Recommended), 20 s, 15 s |
| TV or big screen | 30 s (Recommended), 15 s, 20 s, 60 s |
| Several | one master plus cuts, for example "30 s film plus a 15 s vertical cut (Recommended)", "one 30 s film in every size", "a separate film for each" |

**What should it feel like?** header `Feel`, single choice. First option "Pick for me (Recommended)" whose description says in a few words what you would choose from the brand ("dark, precise, cyan light, a calm build to a big drop"). Then two or three real alternatives that also fit the brand ("Calm and premium", "Fast and bold", "Playful and bright"). Never offer a look that breaks the product's design system.

**Music?** header `Music`, single choice.

| Label | Description |
|---|---|
| Pick for me (Recommended) | A new score in a style that fits the brand and differs from every earlier film. Name the style you lean to. |
| Calm | Little or no drums, space for the picture. |
| High energy | Driving drums, a big drop. |
| Effects only | No music, only designed sounds for every event. |

**Anything you want or want to avoid?** header `Notes`, single choice.

| Label | Description |
|---|---|
| No preferences (Recommended) | Go with these choices and show me the result. |
| Check the script with me first | Write the second by second script and wait for an OK before building. |

The "Type something" choice is where the user writes colours to avoid, words that must appear, a voice over, a competitor not to resemble, a deadline.

## After the answers

1. Say the plan back in four to six short lines: destination and size, length, the story beats, the feel, the music style. No questions in it.
2. If the user chose "Check the script with me first", write `SCRIPT.md` and stop for an OK. Otherwise go straight on.
3. Map the answers:

| Answer | Decides |
|---|---|
| Where | formats (`src/formats.ts`), store preview mode or commercial mode, safe zones, frame rate, loudness, the export (`destinations.md`) |
| Goal | the end card and what it may say on that destination |
| Show | the acts of the story and the magic moment |
| Length | the form's total bars (`music.json`) and the number of acts (one idea per 3 to 5 s) |
| Feel | stage, pacing, transitions, and the shortlist of music genres |
| Music | `music.json` (still checked against the registry) |
| Notes | anything that overrides the defaults; free text wins over every default |

## When not to ask

- The user answered everything in the request, or said "just make it" or "don't ask": state the defaults you chose in one line each and go.
- No question tool is available: use the defaults (YouTube or website, 16:9, 30 s, goal from the product, pick for me) and say so.
- Never a third round. If something is still unclear after round 2, choose and say what you chose.
