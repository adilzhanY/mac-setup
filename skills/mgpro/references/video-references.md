# Video references: analyse what is really there, and combine several

Read when the user gives a reference video, a link to one, or several references to blend (merged from vizavi-motion).

## Work from the real material

- **A file**: work from its real frames and whatever audio it has.
- **A URL**: first actually open the page and get what is available. Never describe the edit, the motion, the frames or the music from a title or a link. A page may give only text or a poster image; say plainly how much you could access.
- **Unavailable video**: name what could not be accessed. The film can still be directed independently, but nothing in it may be presented as observed in that reference.

## Map the scenes and transitions

Make a map with timecodes: scene boundaries, durations and shot sizes, composition and layers, what the hero does, the type, the camera's path and speed, material and light, what carries each join, the sound and the rhythm.

```
ffmpeg -i ref.mp4 -vf "select='gt(scene,0.3)',showinfo" -vsync vfr out/ref/cut%03d.png 2> out/ref/cuts.log   # cut points and their times
ffmpeg -ss 12.4 -t 0.6 -i ref.mp4 -vf scale=384:-1 out/ref/j%03d.png                                        # a dense run across one join
```

- For each important join, extract a dense sequence before, during and after it, and look at it as a sheet (`magick montage`, as in `pipeline.md`).
- A single still cannot tell the exact speed, the easing or how good the sound is. Three chosen frames are not a frame by frame analysis of the whole film.
- The agent cannot hear: describe sound only from what can be measured, and say so.

## Observation, then transfer

Keep each finding in three steps: **seen or heard in a given interval → the useful principle → your own decision for this story**. Keep the source and how much of it you could access. Analysing someone else's device does not give the right to put their video, model, font or music into the film (`rights.md`).

## Combining three references

- Use all three, each for a reason. Write down which quality you take from each: for example the spatial composition from the first, the type from the second, the camera and rhythm from the third. That split is an example, not a rule.
- Note which properties fit together and which conflict, and build one system out of them, not three separate fragments.
- Adapt the palette, logo, materials, hero and world to the brief (in mgpro: to the product's own tokens, `brief.md`); they do not have to copy the sources.
- Keep one causal thread and one scale of motion.
- Show a short map, **reference → quality → how it is used**, then write your own storyboard (`storyboard.md`). Blending references serves the three core mechanics (quality by default, direction before code, the review after the first build), never the other way round.
