import { useLayoutEffect, useMemo, useState, useEffect } from "react";
import * as THREE from "three";
import { useThree } from "@react-three/fiber";
import { continueRender, delayRender, staticFile } from "remotion";
import { clipOf, eyeOf } from "./camera";
import type { Cam } from "./camera";
import {
  BOO_POSITION,
  BOO_ROTATION,
  EAVE,
  EDGES,
  FOOTPRINT,
  INNER_WALLS,
  ROOF,
  ROOMS,
  STOREY_H,
  STOREYS,
  WINDOWS,
  offset,
} from "./plan";
import type { P } from "./plan";

// --- The city -------------------------------------------------------------------------------------

export interface CityData {
  city: Float32Array;
  streets: Float32Array;
}
let cached: CityData | null = null;
let pending: Promise<CityData> | null = null;

function loadCity() {
  pending ??= Promise.all(["ad/city.bin", "ad/streets.bin"].map((f) => fetch(staticFile(f)).then((r) => r.arrayBuffer()))).then(
    ([a, b]) => ({ city: new Float32Array(a!), streets: new Float32Array(b!) }),
  );
  return pending;
}

/** The LoD2 neighbourhood and its streets, loaded once per render tab. */
export function useCityData() {
  const [data, setData] = useState(cached);
  const [handle] = useState(() => (cached ? null : delayRender("city data")));
  useEffect(() => {
    if (cached) return;
    void loadCity().then((d) => {
      cached = d;
      setData(d);
      if (handle !== null) continueRender(handle);
    });
  }, [handle]);
  return data;
}

/** Shared uniforms: the frame drives the rising wave through them. */
export const cityUniforms = {
  uTime: { value: 0 },
  uStart: { value: 240 },
  uFade: { value: 1 },
  /** Frame the lights go down: the city sinks and vanishes in a wave from the building. */
  uNight: { value: 360 },
  uCentre: { value: new THREE.Vector2(0, 0) },
  uMapColor: { value: new THREE.Color("#cbd4df") },
  uWall: { value: new THREE.Color("#fbfbfc") },
  uRoof: { value: new THREE.Color("#e6eaef") },
};

function riseVertex(src: string) {
  return src
    .replace(
        "#include <common>",
        `#include <common>
attribute float aDist;
attribute float aKind;
uniform float uTime;
uniform float uStart;
uniform float uNight;
varying float vRise;
varying float vKind;
varying float vSink;
// Back out over 0.6 s: up past its height by a few percent, then settles.
float riseAt(float t) { float x = clamp(t / 0.6, 0.0, 1.0); float k = x - 1.0; return 1.0 + 2.3 * k * k * k + 1.3 * k * k; }`,
      )
      .replace(
        "#include <begin_vertex>",
        `#include <begin_vertex>
float r = uTime < uStart ? 0.0 : riseAt((uTime - uStart - aDist * 0.2) / 60.0);
float sink = smoothstep(0.0, 1.0, (uTime - uNight - aDist * 0.045) / 22.0);
transformed.y *= max(r, 0.0) * (1.0 - sink);
vRise = clamp(r, 0.0, 1.0);
vSink = sink;
vKind = aKind;`,
      );
}

let cityMesh: { geometry: THREE.BufferGeometry; material: THREE.Material; depth: THREE.Material } | null = null;
function cityParts(d: CityData) {
  if (cityMesh) return cityMesh;
  const n = d.city.length / 5;
  const pos = new Float32Array(n * 3);
  const dist = new Float32Array(n);
  const kind = new Float32Array(n);
  for (let i = 0; i < n; i++) {
    pos[i * 3] = d.city[i * 5]!;
    pos[i * 3 + 1] = d.city[i * 5 + 1]!;
    pos[i * 3 + 2] = d.city[i * 5 + 2]!;
    dist[i] = d.city[i * 5 + 3]!;
    kind[i] = d.city[i * 5 + 4]!;
  }
  const geometry = new THREE.BufferGeometry();
  geometry.setAttribute("position", new THREE.BufferAttribute(pos, 3));
  geometry.setAttribute("aDist", new THREE.BufferAttribute(dist, 1));
  geometry.setAttribute("aKind", new THREE.BufferAttribute(kind, 1));
  geometry.computeVertexNormals();
  const material = new THREE.MeshLambertMaterial({ transparent: true, side: THREE.DoubleSide });
  const depth = new THREE.MeshDepthMaterial({ depthPacking: THREE.RGBADepthPacking, side: THREE.DoubleSide });
  // The shadow pass must see the same rising and sinking, or flat buildings cast tall shadows.
  depth.onBeforeCompile = (shader) => {
    Object.assign(shader.uniforms, cityUniforms);
    shader.vertexShader = riseVertex(shader.vertexShader);
  };
  material.onBeforeCompile = (shader) => {
    Object.assign(shader.uniforms, cityUniforms);
    shader.vertexShader = riseVertex(shader.vertexShader);
    shader.fragmentShader = shader.fragmentShader
      .replace(
        "#include <common>",
        `#include <common>
uniform vec3 uMapColor;
uniform vec3 uWall;
uniform vec3 uRoof;
uniform float uFade;
varying float vRise;
varying float vKind;
varying float vSink;`,
      )
      .replace(
        "vec4 diffuseColor = vec4( diffuse, opacity );",
        "vec4 diffuseColor = vec4( mix( uMapColor, mix( uWall, uRoof, vKind ), smoothstep( 0.0, 0.5, vRise ) ), uFade * ( 1.0 - smoothstep( 0.6, 1.0, vSink ) ) );",
      )
      // Flat and unlit while it is still a map; lit once it stands.
      .replace(
        "#include <opaque_fragment>",
        "outgoingLight = mix( diffuseColor.rgb, outgoingLight, smoothstep( 0.0, 0.5, vRise ) );\n#include <opaque_fragment>",
      );
  };
  cityMesh = { geometry, material, depth };
  return cityMesh;
}

const STREET_COLORS = [new THREE.Color("#ffffff"), new THREE.Color("#f6f7f8"), new THREE.Color("#d8e8d4"), new THREE.Color("#d3d9e0")];
const STREET_Y = [-0.25, -0.2, -0.35, -0.3];
/** A flat material that disappears inside the growing night ring (20 m per frame). */
function nightMaterial(params: THREE.MeshLambertMaterialParameters) {
  const m = new THREE.MeshLambertMaterial({ transparent: true, side: THREE.DoubleSide, ...params });
  m.onBeforeCompile = (shader) => {
    Object.assign(shader.uniforms, cityUniforms);
    shader.vertexShader = shader.vertexShader
      .replace("#include <common>", "#include <common>\nvarying vec2 vWorldXZ;")
      .replace("#include <worldpos_vertex>", "#include <worldpos_vertex>\nvWorldXZ = (modelMatrix * vec4(transformed, 1.0)).xz;");
    shader.fragmentShader = shader.fragmentShader
      .replace("#include <common>", "#include <common>\nvarying vec2 vWorldXZ;\nuniform float uTime;\nuniform float uNight;\nuniform vec2 uCentre;")
      .replace(
        "#include <opaque_fragment>",
        "float ring = max(0.0, uTime - uNight) * 20.0;\ndiffuseColor.a *= smoothstep(ring - 40.0, ring + 10.0, length(vWorldXZ - uCentre));\n#include <opaque_fragment>",
      )
      .replace("#include <opaque_fragment>", "gl_FragColor = vec4( outgoingLight, diffuseColor.a );");
  };
  return m;
}
const groundMat = nightMaterial({ color: "#edf0f4" });
const streetMat = nightMaterial({ vertexColors: true });

let streetGeo: THREE.BufferGeometry | null = null;
function streetGeometry(d: CityData) {
  if (streetGeo) return streetGeo;
  const n = d.streets.length / 3;
  const pos = new Float32Array(n * 3);
  const col = new Float32Array(n * 3);
  for (let i = 0; i < n; i++) {
    const k = d.streets[i * 3 + 2]!;
    pos[i * 3] = d.streets[i * 3]!;
    pos[i * 3 + 1] = STREET_Y[k]!;
    pos[i * 3 + 2] = d.streets[i * 3 + 1]!;
    const c = STREET_COLORS[k]!;
    col[i * 3] = c.r;
    col[i * 3 + 1] = c.g;
    col[i * 3 + 2] = c.b;
  }
  streetGeo = new THREE.BufferGeometry();
  streetGeo.setAttribute("position", new THREE.BufferAttribute(pos, 3));
  streetGeo.setAttribute("color", new THREE.BufferAttribute(col, 3));
  return streetGeo;
}

/** The neighbourhood: a light map that rises into a white 3D city in a wave from the building. */
export function City({ data, frame, fade = 1, waveStart = 240, night = 360, centre = [0, 0] }: { data: CityData; frame: number; fade?: number; waveStart?: number; night?: number; centre?: [number, number] }) {
  const { geometry, material, depth } = cityParts(data);
  cityUniforms.uTime.value = frame;
  cityUniforms.uNight.value = night;
  cityUniforms.uCentre.value.set(centre[0], centre[1]);
  cityUniforms.uStart.value = waveStart;
  cityUniforms.uFade.value = fade;
  return (
    <group>
      <mesh geometry={geometry} material={material} customDepthMaterial={depth} castShadow receiveShadow />
      <mesh geometry={streetGeometry(data)} material={streetMat} receiveShadow />
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -0.5, 0]} material={groundMat} receiveShadow>
        <circleGeometry args={[2600, 96]} />
      </mesh>
    </group>
  );
}

// --- The building ------------------------------------------------------------------------------------

function shape(outer: P[], holes: P[][] = []) {
  const s = new THREE.Shape(outer.map((p) => new THREE.Vector2(p.x, p.y)));
  for (const h of holes) s.holes.push(new THREE.Path(h.map((p) => new THREE.Vector2(p.x, p.y))));
  return s;
}

/** A plan shape pushed up from `y0` by `depth`, in three.js axes (plan y becomes -z). */
function prism(outer: P[], holes: P[][], depth: number, y0 = 0) {
  const g = new THREE.ExtrudeGeometry(shape(outer, holes), { depth, bevelEnabled: false, curveSegments: 1 });
  g.rotateX(-Math.PI / 2);
  g.translate(0, y0, 0);
  return g;
}

const INSET = offset(FOOTPRINT, -0.4);
const GEO = {
  walls: prism(FOOTPRINT, [INSET], EAVE),
  plaster: prism(offset(FOOTPRINT, 0.07), [FOOTPRINT], EAVE),
  plinth: prism(offset(FOOTPRINT, 0.05), [FOOTPRINT], 0.75),
  bands: Array.from({ length: STOREYS - 1 }, (_, i) => prism(offset(FOOTPRINT, 0.06), [FOOTPRINT], 0.14, (i + 1) * STOREY_H - 0.07)),
  cornice: prism(offset(FOOTPRINT, 0.22), [offset(FOOTPRINT, -0.05)], 0.4, EAVE - 0.4),
  cap: prism(FOOTPRINT, [], 0.3, EAVE - 0.05),
  wipeEdge: prism(offset(FOOTPRINT, 0.12), [offset(FOOTPRINT, 0.0)], 0.07),
  storey: prism(FOOTPRINT, [INSET], STOREY_H),
  flat: new THREE.ShapeGeometry(shape(FOOTPRINT)).rotateX(-Math.PI / 2),
};

function gable(x: number) {
  const g = new THREE.BufferGeometry();
  const ym = (ROOF.y0 + ROOF.y1) / 2;
  g.setAttribute(
    "position",
    new THREE.BufferAttribute(new Float32Array([x, EAVE, -ROOF.y0, x, EAVE, -ROOF.y1, x, EAVE + ROOF.rise, -ym]), 3),
  );
  g.computeVertexNormals();
  return g;
}
const GABLES = [gable(ROOF.x0), gable(ROOF.x1)];

/** One roof slope as a slab, from the eave line (with overhang) to the ridge. */
function slope(side: 1 | -1) {
  const half = (ROOF.y1 - ROOF.y0) / 2;
  const pitch = Math.atan(ROOF.rise / half);
  const run = half + ROOF.overhang;
  const len = run / Math.cos(pitch) + 0.15;
  const ym = (ROOF.y0 + ROOF.y1) / 2;
  const dc = run / 2;
  return {
    size: [ROOF.x1 - ROOF.x0 + 2 * ROOF.overhang, 0.24, len] as [number, number, number],
    position: [(ROOF.x0 + ROOF.x1) / 2, EAVE + ROOF.rise - dc * Math.tan(pitch) + 0.1, -ym + side * dc] as [number, number, number],
    rotation: [side * pitch, 0, 0] as [number, number, number],
  };
}
const SLOPES = [slope(1), slope(-1)];

/** Where a window sits: on its wall, centred, facing out. */
function placeOf(i: number) {
  const w = WINDOWS[i]!;
  const e = EDGES[w.edge]!;
  const x = e.a.x + e.u.x * w.along;
  const y = e.a.y + e.u.y * w.along;
  return {
    position: [x, w.storey * STOREY_H + w.sill + w.height / 2, -y] as [number, number, number],
    rotationY: Math.atan2(e.n.x, -e.n.y),
  };
}

const MAT = {
  frame: new THREE.MeshStandardMaterial({ color: "#f5f4f0", roughness: 0.6 }),
  stucco: new THREE.MeshStandardMaterial({ color: "#eadfcd", roughness: 0.85 }),
  sill: new THREE.MeshStandardMaterial({ color: "#d6d0c6", roughness: 0.8 }),
  door: new THREE.MeshStandardMaterial({ color: "#3c2a20", roughness: 0.55 }),
};
const glassMats = WINDOWS.map(() => new THREE.MeshStandardMaterial({ color: "#1a2530", roughness: 0.15, metalness: 0.35 }));

function WindowPiece({ i, scale, glazing, glow }: { i: number; scale: number; glazing: number; glow: number }) {
  const w = WINDOWS[i]!;
  const { position, rotationY } = placeOf(i);
  const mat = glassMats[i]!;
  mat.color.set("#1a2530").lerp(new THREE.Color("#3f78a3"), glazing);
  mat.emissive.set("#cfe9ff");
  mat.emissiveIntensity = glow;
  if (scale <= 0.001) return null;
  const { width: ww, height: hh } = w;
  const f = 0.08;
  return (
    <group position={position} rotation={[0, rotationY, 0]} scale={[scale, scale, scale]}>
      {w.door ? (
        <>
          <mesh position={[0, -0.25, 0.09]} material={MAT.door}>
            <boxGeometry args={[ww - 0.1, hh - 0.6, 0.04]} />
          </mesh>
          <mesh position={[0, hh / 2 - 0.3, 0.1]} material={mat}>
            <planeGeometry args={[ww - 0.16, 0.42]} />
          </mesh>
        </>
      ) : (
        <mesh position={[0, 0, 0.1]} material={mat}>
          <planeGeometry args={[ww - 0.1, hh - 0.1]} />
        </mesh>
      )}
      <mesh position={[0, hh / 2 - f / 2, 0.09]} material={MAT.frame}>
        <boxGeometry args={[ww, f, 0.12]} />
      </mesh>
      <mesh position={[0, -hh / 2 + f / 2, 0.09]} material={MAT.frame}>
        <boxGeometry args={[ww, f, 0.12]} />
      </mesh>
      <mesh position={[-ww / 2 + f / 2, 0, 0.09]} material={MAT.frame}>
        <boxGeometry args={[f, hh, 0.12]} />
      </mesh>
      <mesh position={[ww / 2 - f / 2, 0, 0.09]} material={MAT.frame}>
        <boxGeometry args={[f, hh, 0.12]} />
      </mesh>
      {!w.door && (
        <>
          <mesh position={[0, 0, 0.11]} material={MAT.frame}>
            <boxGeometry args={[0.05, hh - 0.1, 0.05]} />
          </mesh>
          <mesh position={[0, hh * 0.2, 0.11]} material={MAT.frame}>
            <boxGeometry args={[ww - 0.1, 0.05, 0.05]} />
          </mesh>
          <mesh position={[0, -hh / 2 - 0.03, 0.12]} material={MAT.sill}>
            <boxGeometry args={[ww + 0.2, 0.07, 0.2]} />
          </mesh>
        </>
      )}
      <mesh position={[0, hh / 2 + 0.14, 0.11]} material={MAT.stucco}>
        <boxGeometry args={[ww + 0.34, 0.14, 0.1]} />
      </mesh>
    </group>
  );
}

export interface BooState {
  /** Walls rising out of the map (Act I), with overshoot. */
  rise: number;
  /** 1 = the selected building's navy on the map, 0 = its brick. */
  tint: number;
  roofDrop: number;
  roofLift: number;
  shellOpacity: number;
  /** A single white storey with the inner walls, for the plan turned model (Act II). */
  groundModel: number;
  inner: number;
  rooms: number;
  window: (i: number) => number;
  /** Insulation plaster wiped up the facade, metres. */
  plaster: number;
  glazing: number;
  /** The light sweep across the glass, a diagonal position 0 to 1 (outside = off). */
  sweep: number;
}

export const BOO_REST: BooState = {
  rise: 1,
  tint: 0,
  roofDrop: 0,
  roofLift: 0,
  shellOpacity: 1,
  groundModel: 0,
  inner: 0,
  rooms: 0,
  window: () => 0,
  plaster: 0,
  glazing: 0,
  sweep: -1,
};

const ROOM_COLORS = ["#8aa8ff", "#c4a5ff", "#f3a6d8", "#7fd6e8", "#ffcf8a", "#9fe0b0", "#b5b8ff", "#f7b2a0"];
const brick = new THREE.Color("#8e3d31");
const navy = new THREE.Color("#0b5b8c");

/** Methfesselstraße 8, placed in the city. */
export function Boo({ s, plasterPlane }: { s: BooState; plasterPlane?: THREE.Plane }) {
  // A fresh string each frame: R3F only updates a prop whose value changes.
  const wallColor = `#${brick.clone().lerp(navy, s.tint).getHexString()}`;
  const h = Math.max(0.001, s.rise);
  const shellVisible = s.shellOpacity > 0.001;
  const roomShapes = useMemo(() => ROOMS.map((r) => new THREE.ShapeGeometry(shape(r.polygon)).rotateX(-Math.PI / 2)), []);
  const xs = WINDOWS.map((_, i) => placeOf(i).position);
  return (
    <group position={BOO_POSITION} rotation={[0, BOO_ROTATION, 0]}>
      {s.tint > 0.01 && (
        <mesh geometry={GEO.flat} position={[0, 0.06, 0]}>
          <meshBasicMaterial color={navy} transparent opacity={0.85 * s.tint} />
        </mesh>
      )}
      {shellVisible && (
        <group scale={[1, h, 1]}>
          <mesh geometry={GEO.walls} castShadow receiveShadow>
            <meshStandardMaterial color={wallColor} roughness={0.92} transparent={s.shellOpacity < 1} opacity={s.shellOpacity} />
          </mesh>
          <mesh geometry={GEO.plinth} castShadow>
            <meshStandardMaterial color="#6f6a66" roughness={0.9} transparent={s.shellOpacity < 1} opacity={s.shellOpacity} />
          </mesh>
          {GEO.bands.map((g, i) => (
            <mesh key={i} geometry={g} material={MAT.stucco} />
          ))}
          <mesh geometry={GEO.cornice} material={MAT.stucco} castShadow />
          {GABLES.map((g, i) => (
            <mesh key={i} geometry={g} castShadow>
              <meshStandardMaterial color={wallColor} roughness={0.92} side={THREE.DoubleSide} transparent={s.shellOpacity < 1} opacity={s.shellOpacity} />
            </mesh>
          ))}
        </group>
      )}
      {s.plaster > 0.001 && plasterPlane && (
        <>
          <mesh geometry={GEO.plaster} castShadow>
            <meshStandardMaterial color="#f0e4cf" roughness={0.95} clippingPlanes={[plasterPlane]} />
          </mesh>
          {s.plaster < EAVE - 0.05 && (
            <mesh geometry={GEO.wipeEdge} position={[0, s.plaster - 0.035, 0]}>
              <meshBasicMaterial color="#ffffff" />
            </mesh>
          )}
        </>
      )}
      {s.roofDrop < 1 && s.roofLift < 1 && (
        <group position={[0, s.roofDrop * 9 + s.roofLift * 16, 0]}>
          <mesh geometry={GEO.cap}>
            <meshStandardMaterial color="#73767c" roughness={0.9} transparent opacity={(1 - s.roofDrop) * (1 - s.roofLift)} />
          </mesh>
          {SLOPES.map((sl, i) => (
            <mesh key={i} position={sl.position} rotation={sl.rotation} castShadow>
              <boxGeometry args={sl.size} />
              <meshStandardMaterial color="#555960" roughness={0.75} transparent opacity={(1 - s.roofDrop) * (1 - s.roofLift)} />
            </mesh>
          ))}
        </group>
      )}
      {WINDOWS.map((_, i) => {
        // The sweep is a band moving along a diagonal over the facade (along + height).
        const p = xs[i]!;
        const k = (p[1] / 18 + (WINDOWS[i]!.along / 15)) / 2;
        const glow = Math.max(0, 1 - Math.abs(k - s.sweep) / 0.08) * 2.2;
        return <WindowPiece key={i} i={i} scale={s.window(i)} glazing={s.glazing} glow={glow} />;
      })}
      {s.groundModel > 0.001 && (
        <group scale={[1, s.groundModel, 1]}>
          <mesh geometry={GEO.storey}>
            <meshStandardMaterial color="#f4f5f7" roughness={0.8} />
          </mesh>
        </group>
      )}
      {s.inner > 0.001 &&
        INNER_WALLS.map((w, i) => {
          const len = Math.hypot(w.b.x - w.a.x, w.b.y - w.a.y);
          const hh = (STOREY_H - 0.05) * s.inner;
          return (
            <mesh
              key={i}
              position={[(w.a.x + w.b.x) / 2, hh / 2, -(w.a.y + w.b.y) / 2]}
              rotation={[0, Math.atan2(w.b.y - w.a.y, w.b.x - w.a.x), 0]}
            >
              <boxGeometry args={[len + w.thick, Math.max(0.001, hh), w.thick]} />
              <meshStandardMaterial color="#ffffff" roughness={0.8} />
            </mesh>
          );
        })}
      {s.rooms > 0.001 &&
        roomShapes.map((g, i) => (
          <mesh key={i} geometry={g} position={[0, 0.03, 0]}>
            <meshBasicMaterial color={ROOM_COLORS[i % ROOM_COLORS.length]} transparent opacity={0.55 * s.rooms} />
          </mesh>
        ))}
    </group>
  );
}

/** Puts the canvas camera where the frame wants it. */
export function Rig({ cam }: { cam: Cam }) {
  const { camera } = useThree();
  const eye = eyeOf(cam);
  const { near, far } = clipOf(cam);
  useLayoutEffect(() => {
    const c = camera as THREE.PerspectiveCamera;
    c.position.set(...eye);
    c.up.set(0, 1, 0);
    c.lookAt(...cam.target);
    c.fov = cam.fov;
    c.near = near;
    c.far = far;
    c.updateProjectionMatrix();
    c.updateMatrixWorld();
  });
  return null;
}
