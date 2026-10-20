# 3D in Remotion: techniques and traps

Example code: `templates/kit/src/camera.ts` (orbit camera, projection, corner pin) and `three.tsx` (Rig, Studio). Bauwerk (`templates/examples/bauwerk/src/`): `world-example.tsx` (city shader, building model), `CityAct.tsx` (camera path, corner pinned plan, projected overlays), `HeroAct.tsx` (shadows, clipping wipe). torq (`templates/examples/torq/src/`): `BarAct.tsx` (a barbell from primitives, slams, smear, shake), `Medal.tsx` and `ForgeAct.tsx` (extruded hex medal with the logo, tier metals, lit track, handoff to 2D).

## Setup

- `@remotion/three` `ThreeCanvas` with `gl={{ antialias: true, alpha: true }}`, `shadows`, `onCreated={(s) => (s.gl.localClippingEnabled = true)}` when clipping planes are used.
- Standalone (torq): install `three`, `@react-three/fiber`, `@remotion/three` and `@types/three` in the video project, pinned to exact versions; nothing to alias.
- Reusing the app's 3D code (Bauwerk): alias `three`, `@react-three/fiber`, `@react-three/drei` to ONE copy (the app's node_modules), and `react`, `react-dom` to one copy, in `remotion.config.ts` webpack overrides (see `templates/examples/bauwerk/remotion.config.ts`). Type check with a `paths` entry for `three` pointing at `@types/three`.
- Render with the swangle backend on Linux: `Config.setChromiumOpenGlRenderer("swangle")` in `remotion.config.ts` (and `--gl=swangle` on the command line). `angle`, `egl` and `angle-egl` failed to create a WebGL context. Swiftshader is software, so budget time: Bauwerk (a 60k triangle city with shadows on most frames) took about 25 minutes at concurrency 6; torq (600 of 1800 frames in 3D, no shadows) about 20 minutes at concurrency 8. A 3D still takes 4 to 6 s.
- `PCFSoftShadowMap` is deprecated in three 0.185 (falls back to PCF); fine.

## Camera

- Drive the camera from a pure function of the frame: `{ target, dist, az, el, fov }` to an eye position. A `Rig` component sets position, `lookAt`, fov, near and far in `useLayoutEffect` every render (a raw `perspectiveCamera makeDefault` did not take over).
- near = max(0.3, dist x 0.02), far = dist x 4 + 2500: keeps depth precision at both city and room scale.
- Top down: elevation 89.9 (not 90) with up (0, 1, 0); screen up is then the direction (-sin az, -cos az) in xz, so choose az to put the plan upright (street at the bottom).

## Projecting DOM overlays onto 3D

Build the same camera in the DOM (`threeCamera(cam)` in camera.ts: a `PerspectiveCamera` with the same parameters, `updateMatrixWorld`, `updateProjectionMatrix`) and `project()` world points to pixels. Use it for pins on roofs, room labels, ripples. Labels stay upright and sharp because they are DOM.

## Corner pin (After Effects technique in code)

A plane seen through a perspective camera is a projective map of the plane, which CSS `matrix3d` can express exactly. Project the four corners of a 2D layer's rectangle (placed on the 3D ground) and solve the 8 unknowns of the homography (`cornerPin(src, dst)` in camera.ts, Gaussian elimination), then `transform: matrix3d(...)` with `transformOrigin: 0 0`. The SVG plan, its AI glow and its traced lines stay glued to the ground while the camera dives and tilts. Hand the job over to real 3D geometry before the tilt gets steep (the DOM layer cannot be occluded by 3D walls).

## Real city data

- Bauwerk's LoD2 API (live at `https://bauwerk-demo.xyz/api/`): `/buildings/<gid>` (detail with parts and mesh origin in EPSG:25833) and `/buildings/<gid>/neighbours?box=<20 to 1200 m>` (all buildings with full LoD2 meshes: wall, roof, ground, closure surfaces as rings relative to each mesh origin).
- Streets and parks from OpenStreetMap through Overpass (`https://overpass-api.de/api/interpreter`, `[out:json]`, `way(around:700,lat,lon)[highway]`, parks, grass, rail, `out geom;`). It answers 406 without a User-Agent (send a plain one like `bauwerk-video/1.0`, never the user's email) and 504 when busy (wait and retry).
- `templates/examples/bauwerk/prep/lod2_osm_city.py`: triangulates every planar ring with mapbox-earcut (drop the axis of the largest Newell normal component), flattens each building onto z = 0 (subtract its own minimum z; Kreuzberg's hill otherwise floats buildings), converts OSM lon/lat to EPSG:25833 with pyproj (a local tangent plane is off by metres at the edges because of grid convergence), builds street ribbons (quads plus round joins) and park polygons, and writes flat float32 buffers: city `[x, y, z, distance, kind]` per vertex, streets `[x, z, kind]`.
- Fit a hand-made model onto its LoD2 spot by brute force: rotation sweep in 0.05 degree steps, centroid translation, mean nearest-vertex error (1.5 m was good enough).

## The rising and sinking city (one shader)

Merged non-indexed geometry, attributes `aDist` and `aKind`, `MeshLambertMaterial` with `onBeforeCompile`:
- Vertex: `r = uTime < uStart ? 0 : riseAt((uTime - uStart - aDist * 0.2) / 60)` with back-out `riseAt`; `sink = smoothstep(0, 1, (uTime - uNight - aDist * 0.045) / 22)`; `transformed.y *= r * (1 - sink)`. Pass `vRise`, `vSink`, `vKind` to the fragment.
- Fragment: colour = mix(map colour, mix(wall, roof, kind), smoothstep(0, 0.5, vRise)); alpha fades with vSink; and **unlit while flat**: `outgoingLight = mix(diffuseColor.rgb, outgoingLight, smoothstep(0, 0.5, vRise))` before `#include <opaque_fragment>`, so the map reads as a clean flat map, not a hillshade.
- Uniforms live in one shared object (`Object.assign(shader.uniforms, shared)`) updated every render.
- **Shadows**: give the mesh a `customDepthMaterial` (MeshDepthMaterial, RGBADepthPacking) with the same vertex injection. Without it the shadow pass uses full height and flat buildings cast tall shadows.
- Ground and streets disappear inside a ring growing from the hero: inject a world xz varying and `alpha *= smoothstep(ring - 40, ring + 10, length(xz - centre))`, ring = 20 m per frame since the night cue. The dark stage is a DOM layer behind the transparent canvas.
- Flat geometry built with arbitrary winding (street ribbons from flipped axes) needs `side: DoubleSide` or half of it is culled.
- Fog for depth in oblique views (near dist x 1.15, far dist x 3.4, the stage colour); none in top down views; keep it until the far city is gone rather than switching it off (switching pops the far city into view).

## A building model from plan data

- Walls: `ExtrudeGeometry` of the footprint with the 0.4 m inset as a hole (hollow, so the roof can lift off), `rotateX(-pi/2)` so plan y becomes -z and depth becomes height.
- Polygon offset with mitred corners for inset and outset rings (plinth, string courses at each storey, cornice, a plaster shell 7 cm out).
- Gable roof: two slope slabs (boxes rotated by the pitch) and two gable triangles; a cap slab over the footprint.
- Windows as small groups facing the wall's outward normal (`rotationY = atan2(n.x, -n.y)`): glass plane (per window material for tint and sweep glow), four frame boxes, mullion, transom, sill, stucco lintel. Scale each group from 0 with a spring to pop them on.
- Insulation wipe: the plaster shell with a clipping plane `Plane((0, -1, 0), height)` (keeps y below height) plus a thin white ring at the wipe height.
- A navy flat footprint fill while the building is "selected on the map", fading to its brick as it rises.

## The trap that cost the most: props that do not change

R3F only updates a prop when its value changes. A `THREE.Color` (or any object) created once with `useMemo` and mutated each frame is the same object, so the material keeps the colour of the first frame that tab rendered. Stills look right (each still is a first frame); the full render is wrong. Pass a fresh value (`"#" + color.getHexString()`) or mutate the material directly (`mat.color.set(...)` on a material you own).

## Async data and the first frame

Data fetched inside the `ThreeCanvas` subtree arrived after R3F drew the frame, so the city never showed. Load with `delayRender` in the DOM component that owns the canvas and mount the canvas only when the data is there; pass the data down as a prop. Cache geometry at module level (once per render tab).

## Metal on a black stage (torq)

Metal reflects its surroundings, so on a black stage with only lights it renders as flat grey. Give the scene a reflection map: `PMREMGenerator(gl).fromScene(new RoomEnvironment(), 0.04).texture` as `scene.environment` (`Studio` in `templates/kit/src/three.tsx`, intensity 0.55 to 0.9). Then light it like a product shot: a key from the upper left, two strong rim lights from behind on both sides tinted with the object's own light colour, a weak point light in front in the accent. `MeshPhysicalMaterial` with metalness 1, roughness 0.22 to 0.28, clearcoat 0.6 for polished metal; rubber at roughness 0.6, metalness 0.05. Emissive in the accent (intensity 0.25 to 0.85) for parts that should glow on their own (a lime ring on a plate, collars).

## A product mark in 3D

Parse the mark's SVG with `SVGLoader().parse(svgString)` (it applies the group transforms, including potrace's `translate(0,1024) scale(0.1,-0.1)`), `SVGLoader.createShapes(path)` for every path, `ExtrudeGeometry` with a small bevel. Then centre and scale it into the object. **Flip y and z together** (`scale(k, -k, -k)`): flipping only y (SVG is y down) mirrors the geometry, reverses the winding, and the normals point inward, so the mark lights inside out. Recompute the bounding box after the flip and translate so its back sits on the surface it stands on.

## Rounded shapes with a real bevel

A medal frame: a `Shape` with rounded corners (lines plus `quadraticCurveTo` at each corner) with a smaller rounded hole, `ExtrudeGeometry` with `bevelSegments: 8`, `bevelSize: 0.045`, `bevelThickness: 0.05`; the bevel is what catches the light. A dark inner field as a separate thin extrusion; the emblem standing out of it.

## Spinning objects need a back

Anything that spins shows its back half of the time. Put the emblem on both faces (a second mesh rotated by pi around y) and make the field symmetric around z = 0. An empty back flashing every half turn reads as a glitch.

## Orientation inside rotated groups

A cylinder's axis is y. To lay a barbell plate along the bar (x), rotate its group by pi/2 about z. Every ring on that plate (a torus, a ring geometry) lies in its local xy plane by default and must be rotated by pi/2 about x INSIDE the group to sit flat on the plate's face. Forgetting one ring gave a vertical rod through the plate that only showed when the camera looked down the axis.

## Speed without motion blur

- Motion smear for a fast object: draw two or three transparent copies at the object's positions 0.45, 0.9 and 1.35 frames earlier (opacity 0.28, 0.13, 0.06), only while it moves. Far cheaper than `CameraMotionBlur` over a whole act.
- Impacts: a camera shake as a film offset, `camera.setViewOffset(1920, 1080, dx, dy, 1920, 1080)`, with dx, dy = amp x e^(-k/5.5) x sin(k x 1.9), amp 16 px for a plate slam, 4 for a click. It jolts the image without moving the camera, so the composition stays.
- A plate landing: it accelerates (t squared over 10 frames from 1.7 m out) and recoils 1.2 cm with a damped bounce.

## Lit progress along a path

A track around an object (the medal's hexagon): one dark `TubeGeometry` for the whole path, and the lit part rebuilt each frame as a tube through points sampled from 0 to the fraction t of the perimeter (CatmullRom with tension 0 stays straight between corners), `toneMapped={false}` and emissive so it glows, a small emissive sphere at the tip.

## Overlays tied to 3D

Rays, glows, sparks and labels around a 3D object are DOM or SVG layers positioned from `project(threeCamera(cam), point)`. A glow that must swallow the object goes on top with `mix-blend-mode: screen`; rays and pools go behind the transparent canvas.

## 3D to 2D handoff

See `transitions.md`: transform the canvas layer toward the 2D target, using `pxPerMetre(camera, centre)` to compute the exact scale at which the 3D object matches the 2D drawing.
