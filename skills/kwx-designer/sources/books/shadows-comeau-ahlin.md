# Shadows: Josh Comeau and Tobias Ahlin

- **Status:** free articles.
- **Legal sources:**
  - Josh Comeau, "Designing Beautiful Shadows in CSS": https://www.joshwcomeau.com/css/designing-shadows/
  - Tobias Ahlin, "Smoother and sharper shadows with layered box-shadows": https://tobiasahlin.com/blog/layered-smooth-box-shadows/
- **Read:** both in full, October 2026.

## Comeau

- One light source for the whole page (he suggests above and slightly left), distant like the sun, so every shadow shares the same angle. In his demo the vertical offset is always 2x the horizontal: "every shadow on the page should share the same ratio".
- As elevation rises: larger offsets, larger blur, lower opacity; optionally the element grows slightly.
- Layered shadows (credited to Ahlin) look far more realistic than one shadow:
  ```css
  box-shadow:
    0 1px 1px hsl(0deg 0% 0% / 0.075),
    0 2px 2px hsl(0deg 0% 0% / 0.075),
    0 4px 4px hsl(0deg 0% 0% / 0.075),
    0 8px 8px hsl(0deg 0% 0% / 0.075),
    0 16px 16px hsl(0deg 0% 0% / 0.075);
  ```
  More rendering cost; do not animate them.
- Shadow colour: transparent black on a colour background desaturates it to grey. Match the background hue with lower lightness: on `hsl(220 100% 80%)`, `hsl(220 60% 50%)` is right.
- Tokenize: small, medium, large elevations, with the colour as a CSS variable (`--shadow-color: 220deg 60% 50%`) set on the section so children inherit it. Small `0.5px 1px 1px / 0.7`; medium 3 layers at `/ 0.333`; large 5 layers at `/ 0.2` with offsets up to `16px 32px 32px`.

## Ahlin

- A single shadow has only offset, blur, spread and colour. Stacking layers whose offset and blur double gives control over sharpness, distance and concentration.
- Baseline: 5 layers at alpha 0.12 (1, 2, 4, 8, 16px). 4 layers at 0.15; 6 layers at 0.11 up to 32px. More layers need lower alpha each and widen the spread.
- Sharp: decreasing alpha 0.25 to 0.05. Diffuse: increasing alpha 0.08 to 0.20. Dreamy: alpha 0.07 with blur at 2x the offset up to 64px.
- Decouple blur from offset for shorter (`0 6px 8px`, `0 8px 16px`) or longer (`0 32px 16px`) shadows.

## Used in

`../../premium/materials-depth-light.md`.
