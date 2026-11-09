# Ready 3D models: where to find them, and how to bring one into a scene

mgpro builds most 3D itself: primitives, the product's own SVG mark and font extruded, real data (`three.md`). A ready model is worth it when the brief needs an object that is not worth modelling: a real looking device, a character with a rig, a scanned prop. Merged from vizavi-motion (3D sources and 3D models).

## Rights first

- Check the exact model and its terms; "free" does not mean every right. Rights to the code, the model, the textures, the font and the music can all differ.
- An mgpro commercial is published by definition, so the specific file's licence must allow commercial use in a video, and another company's product or logo stays out of the film (`rights.md`; the torq lesson: never use licence protected material, no other brands' marks). A generic laptop or phone without marks is fine; never forbid showing devices as such.
- For a personal film that will not be published (vizavi's case), an ordinary allowed download does not need to be refused over a possible future commercial use. Do not turn an ordinary personal download into a legal barrier.
- Use a source that is really available and its ordinary download. Never bypass access restrictions, never present a model you could not get as obtained, never sign up for an account or install an integration on your own.
- If a model is unavailable, paid, or its terms do not fit the intended use, look for the next one. Never treat the right to view or download as a right to resell or redistribute the asset.
- Keep the knowledge and the links in this skill, never the model files themselves (for example Quaternius' licence forbids redistributing standalone assets).

## Sources (research handed to vizavi-motion, dated 16.10.2026)

The research does not mean that each file was downloaded and tested. A release's terms and availability can change: check its page and the bundled licence when downloading. The order below is a choice by task, not a chain of sites to try in turn.

| Task and source | What to watch when choosing |
|---|---|
| Realistic objects: [Poly Haven Models](https://polyhaven.com/models) | glTF, CC0, no sign up. Good for realistic props; check the texture set and the actual model. |
| Stylised sets: [Kenney Assets](https://kenney.nl/assets) | Choose a 3D set specifically: GLB available, CC0. "Continue without donating" gets the free set without a required donation. |
| Characters and rigs: [Quaternius](https://quaternius.com/) | Free Standard releases often have FBX or glTF; Source may be paid. Keep the licence of the exact release; do not assume the whole site is CC0 (see below). |
| Real 3D scans: [ambientCG](https://ambientcg.com/list?type=3d-model,terrain) | CC0; check the format and the contents of the ZIP. Do not promise every object comes as GLB. |
| Specific devices and other models: [Sketchfab](https://sketchfab.com/) | Look for downloadable and free, glTF or GLB, and the terms of that specific model. Downloading needs an account: use access that already exists or another source, never a self made sign up. |
| Free models with a format filter: [CGTrader](https://www.cgtrader.com/3d-models?free=1) | Check the glTF filter, a really zero price and the individual terms. "Free in subscription" is not a free download; waits and limits are possible. |
| Stylised characters: [KayKit Adventurers](https://kaylousberg.itch.io/kaykit-adventurers) | The free part is 5 models, FBX and glTF, CC0; the extras are paid. Do not credit the free part with the extra content. |
| Technical fallback: [Khronos glTF Sample Assets](https://github.com/KhronosGroup/glTF-Sample-Assets) | GLB and glTF for compatibility and technical scenes. Each asset's licence is in its own README; the repository's licence does not replace it. |

- **Quaternius**: [QAL v1.0 of 28.08.2026](https://quaternius.com/license.html) allows personal and commercial finished projects but forbids distributing standalone assets, packs and templates. Some older specific releases may still be CC0. Never carry one release's licence over to another.
- **Poly Pizza**: do not make it the main automatic source: [its terms](https://poly.pizza/docs/tos) restrict automated downloads. That limits how a model is fetched, not 3D in the project. Pick another free source; never get around the restriction.

## Before the scene

1. Check the exact model or variant, its format and that it is complete: mesh, UVs, textures, materials, rig and animations, external dependencies. Open or render the actual file, not just the page's preview. Prefer GLB or glTF when it suits the renderer and the export.
2. Normalise units and scale, axes, position, orientation, origin and pivot. Check normals, edges, thickness, topology, transparency, roughness and metalness, the textures' colour space, and that the material suits the renderer. Do not substitute WebGPU or TSL material properties for those of an ordinary WebGL material.
3. Check that the textures are found after loading, their sizes, paths and alpha. Make sure the model holds together at the chosen shot size. Reduce heavy meshes and textures while keeping the silhouette and the needed detail; check the real render speed and the export path (swangle is software rendering, `three.md`).
4. Set light, environment, exposure, camera, shadows and contact for the material. Plastic, metal and glass must behave differently on the surface (for metal on black see `three.md`). A bright highlight or an overall gradient does not fix a wrong form.
5. A laptop: check that the lid and the base are separate and where the hinge axis is. Opening is the lid rotating relative to the base around the hinge, not the whole body turning. Check the closed and open states, the screen, the starting orientation, and that no stray underside shows in the staging.

In Remotion, load the GLB from `public/` with `staticFile()` and three's `GLTFLoader` behind `delayRender` in the component that owns the canvas, and mount the canvas only when it is loaded, like the city data in `three.md` (Async data and the first frame).

## In the scene

- Any hiding or reveal, the captions and the camera all serve one spatial scene.
- On a close pass keep the hero in focus and at the right scale, and never let the camera cross the surface at the near plane (mgpro sets near = max(0.3, dist x 0.02)).
- When a model is replaced, check orientation, pivot, light, contact and animation again.

## Credits in the final reply

List the sites, pages and files really used: author and title, link, format, the stated licence or terms with the date checked, the required attribution, and what you changed. If the intended use is really limited, say exactly how and find an allowed alternative.
