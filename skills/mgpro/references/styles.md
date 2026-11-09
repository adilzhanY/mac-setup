# Styles and vetted sources: two registries

mgpro already keeps one registry, the music registry (`music/registry.json`), so that no film repeats another's score. This file keeps two more, merged from vizavi-motion: approved visual styles, and sources that were actually checked.

## Approved style cards

A film's visual language comes from its brief and the product's own design system (`brief.md`, `craft.md`). A style becomes a card here only after the user explicitly approved it.

- Card: the name, where and when it was approved, the visual grammar (forms, type, material, light, camera and rhythm), and where it applies.
- A card describes a language, not an order of scenes. The three core mechanics (quality by default, direction before code, the review after the first build) still apply, within the explicit brief.
- Earlier suggestions that were never approved do not count as chosen. A style picked for one film is not the user's permanent taste; for other films choose the language from their own brief.

### The six part teaching demo (the user's choice, 16.10.2026, from vizavi-motion)

These six parts were approved for one specific teaching demo, not as the plan for every film. Its format and length come from that demo's own brief and are not set here.

| Part | Visual language and action |
|---|---|
| Hand drawn pencil sketch | A drawn stroke with pressure and an uneven line, forms being constructed, a light paper texture. Text or drawing appears along a meaningful pencil path; a plain outline of a printed font is not handwriting. Deliberately swapping drawings is fine under a smooth, controlled camera. |
| Paper | Cut out shapes, layers, edges with contact shadows, folds and the plasticity of the material. Stretch, squash, collision and a local stop motion stepping support the action rather than replace it with random jitter. |
| Pixel | One working pixel grid, consistent scales of shapes and glyphs, controlled motion without accidental blur of the outlines. Keep the rate of drawn states separate from the output frame rate; the final text is readable. |
| 2D plus product UI | A flat interface of cards, panels and buttons, a clear cursor and causal state changes. The viewer sees the product work through one concrete action. |
| 2.5D plus product UI | The same interface: flat panels spread out in depth, the camera revealing the layers and the parallax. No fake real 3D thickness or sides. |
| 3D plus product UI | The same recognisable objects get real thickness, edges and side faces, matching light and shadows, volume, and a spatial orbit or fly through. The difference from 2.5D shows in the output. |

- In the last three parts keep the identity of the interface, the data and the objects; change only how space is represented (`three.md`, One interface in 2D, 2.5D and 3D; the interaction rules in `interaction.md`).
- Through all six parts one fixed screen space indicator: constant position and look, only the name of the current part changes. It is not tied to the world camera and is protected from overlaps and crops.
- Energetic transitions land on expressive accents of the real music and effects while keeping reading and meaning (the sound side is in `sound.md`, section 6).
- This labelling and direction belong to that demo only; they are not a requirement for other films.

## Vetted sources

Add an entry only when it was actually checked: the site and the exact page, what is available, whether an account is needed, the terms of free use and of the specific file, the format and output, the date and how it was checked, known limits. Keep apart what the page says, a preview, access to a download, the real file, and verified working use. Never claim that something works from a URL or a listing card alone.

| Area | Where | Checked | How |
|---|---|---|---|
| 3D models | `models.md` | 16.10.2026 | documentation only, not each model downloaded |
| Image generation and editing | `images.md` | 16.10.2026 | documentation only, not a practical test of keeping a character |

VidIQ came up as a possible optional sound source for a future task; it is not a general dependency and not claimed to be free. It is noted in `music.md`, The music serves the picture.
