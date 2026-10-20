# The brief: decisions before the story

Make these calls after the intake (`intake.md`), which already settled the destination, goal, features, length, feel and music. Each call below has a default; take it, state it in the reply, and move on. Do not add questions beyond the intake's two rounds.

## 1. Platform and interaction

| Product | Interaction | Why |
|---|---|---|
| Desktop app, web app, dev tool | The user's own cursor (see `interaction.md`), I-beam over fields, hand over clickables, hidden while typing | A cursor is how people use it; their own theme makes it feel like theirs |
| Mobile app | Taps: the control presses and a soft ring spreads from it. No drawn finger, no cursor | A cursor on a phone UI reads as wrong instantly |
| Hardware, a service, a brand film | Nothing. Things act by themselves on the beat | Interaction would be a prop with no meaning |

Collaborators (other people's cursors, avatars, typing bubbles) only when the product is actually multiplayer.

## 2. Light or dark stage

Use the brand's own stage colour from its tokens. Do not flip a dark brand to light because the Bauwerk film was light.

| Brand | Working scenes | Magic moment | Into the drop | Result and end |
|---|---|---|---|---|
| Light (Bauwerk: white, navy) | light radial stage | dark navy | white bloom | light |
| Dark (torq: near black, lime) | the brand's near black | deeper black, accent glow only | accent bloom, then half a beat of pure black, then an accent flash | the brand's near black, the mark in the accent |

On a dark brand all the contrast comes from the accent: lime light, lime fills, lime glows. Keep greys for structure (axes, hairlines, inactive cells).

## 3. The magic moment

Every ad needs one shot where the product does something nobody else does. Find the product's real version:

| Product has | Magic moment | Example |
|---|---|---|
| AI | the AI reading, tracing, detecting, with its gradient glow and notes in the song's key | Bauwerk tracing an old plan, finding every window |
| A scoring or ranking engine | the engine working on real data: a population forming, the user landing in it | torq: 401,158 real meet results raining into a curve, the lifter's dot landing at 87 percent |
| Real time collaboration | people arriving, editing together, changes appearing live | Bauwerk's live team |
| Speed | a long process collapsing into a beat (a counter racing, a progress ring closing) | |
| A physical object | the object assembling itself in 3D | torq's barbell loading, the medal being forged |

Never paint an AI glow on a product that has no AI.

## 4. Real data

Read the repo for data the film can show honestly: datasets bundled with the app, real geometry, real copy, real limits. torq shipped OpenPowerlifting quantiles in `src/data/percentiles.json`; the curve in the film is that table, smoothed. Real data makes a shot convincing and keeps every number defensible.

## 5. The product's own claim rules

Products often have rules about how they may describe themselves. Find them (README, CLAUDE.md, docs, store listing) and follow them in the copy. torq never says "top N% of people", only "of competitive lifters", because the population is meet lifters. A film that breaks the product's own wording rule is a film the user cannot publish.

## 6. People

- Fictional first names for friends, teammates and leaderboards (Maya, Alex, Sam, Jonas), varied, never a real public figure.
- The viewer's own row can carry the user's handle when the film is theirs.
- Real colleague names only when the user gives them (Bauwerk used two colleagues by request).
- No faces. Initials on a coloured circle.

## 7. The end card

- The product's mark, its wordmark, its tagline (from its own docs if it has one), and the ask that fits the goal and the destination.
- The destination limits the ask: a store preview has no call to action text at all (the store's own button does it); a social ad's platform shows its own button, so the end card names the product rather than "Download now"; a YouTube video with end screen elements keeps its last 5 to 20 s calm with room for them; a TV spot shows the URL or the name, held still.
- Only claim availability the docs confirm. "For Android" when it is an Android app not yet in a store; a URL only when it exists. Never a store badge (see `rights.md`).
- Hold it at least 2 s; fade to black in the last 12 frames as the music rings out.

## 8. State the choices

End the reply with the choices made on the user's behalf in one short list: interaction, invented names, what was left out for rights reasons, the call to action wording.
