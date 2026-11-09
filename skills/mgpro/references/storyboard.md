# Storyboard: one thread, options for every scene, a card for every shot

Direction comes before code (merged from vizavi-motion, its second core mechanic). Do this after the intake (`intake.md`) and the brief decisions (`brief.md`), before the second by second tables in `SCRIPT.md` and before any scene is built. The storyboard is the top of `SCRIPT.md`: the thread, the options per scene with the choice, and a shot card per scene. The per second tables (time, frames, picture, sound) follow from it.

## 1. Pull the brief together

Write down the goal, the viewer, the key idea, the copy that must appear, the format, the length, the sound, the resources you may use and the files to deliver. Most of it comes from the intake and the destination. Never invent real facts you do not know (a feature, a price, a user preference nobody stated). Reversible creative calls you make yourself and state in the reply.

## 2. One original thread

State the film's single thread in one or two lines: what acts, what changes, and what idea the result proves. It can be a material changing, motion passed from object to object, a chain of cause and effect, a space unfolding, or another original device. Do not copy an earlier film's sequence under a new name. That includes mgpro's own films: the spine of Bauwerk and torq is one form among eight (`craft.md`, Pacing), not the default.

## 3. Three to five options for every scene

For each scene write 3 to 5 short options that differ in substance: in the action, the composition and space, the metaphor, or the transition. A different colour or font alone is not a new option. Pick the strongest one for the film as a whole, and write the choice with one short practical reason. Short options, the choice and a usable storyboard are enough; the reasoning behind it does not need to be written out.

- Scenes must develop the story causally: each one is caused by the last, or answers it.
- A circle, the letter O or a portal is only one possible device. Do not reach for it by habit. mgpro's films already leaned on rings (torq's plate ring became the rest timer, then a dot), so a new film looks for its own carrier.
- Two or three devices may be combined when together they form one continuous action.

In `SCRIPT.md`, per scene:

```
### Scene 3: the engine (7 to 10 s)
Options:
1. Particles rain into a curve built from the real quantiles; "you" lands in it.
2. The leaderboard zooms out until each row is a dot; the dots sort into the curve.
3. A single bar grows, splits into thousands, and the population forms.
Chosen: 1. The real data is the magic moment, and the dot from scene 2 carries through.
```

## 4. Fill every shot and every join

Then fill a card for every shot and check reading times and risks. This is a working plan, not a queue of approvals. If the user chose "Check the script with me first" in the intake, stop after the storyboard and the script for the OK; otherwise go straight on.

## The shot card

| Field | What to fix |
|---|---|
| Time and meaning | The interval, the main accent, the shot's role in the whole story |
| States and action | What was there before, what triggers the change, what the hero does, the reaction, the result |
| Space | Composition, foreground, middle ground and background, light, material |
| Text | The exact line, what the letters or words do, the reading window (at least about 1 s readable, `craft.md`) |
| Camera and optics | Path, target, rotation and speed, shot size, focus and blur (`craft.md`, Camera and Optics) |
| Joins | The entry from the previous shot, what carries the transition, the exit into the next |
| Sound | The bar or beat, the effect and the event it is synced to, or an explicit silence (`music.md`) |
| Check | The main risk, how it will actually be checked, a technical fallback that is allowed |

## Design a transition together with both scenes

- **Match cut**: match the projected silhouette, scale, orientation and direction of motion on both sides (torq's shape match cut in `transitions.md` measures the ring's radius on screen).
- **Mask**: the next scene must really appear inside the mask. An overlay laid on after a finished cut does not make a mask transition.
- **One location**: keep its poses, perspective, light and speeds across the shots, and tie any reveal of an object to a real overlap or action.

## Probe the biggest risk first

Before the full build, test the one riskiest thing (technical or artistic) at real quality and in motion, with sound if the film has sound. In mgpro that is a short render of just that range (`npx remotion render src/index.ts <Comp> out/probe.mp4 --frames=420-600 --gl=swangle`), for example the 3D dive, the particle field or the morph. Choose the probe's length by what it needs to read, not by a fixed 5 to 7 s. A probe replaces neither the storyboard nor the review after the full build (`review.md`).
