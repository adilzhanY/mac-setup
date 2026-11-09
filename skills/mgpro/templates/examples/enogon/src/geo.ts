import * as THREE from "three";
import { C } from "./brand";
import {
  CENTER,
  FOOTPRINT,
  INNER_FACE,
  INNER_WALLS,
  KNEE,
  OPENINGS,
  OUTER_T,
  OUTER_WALLS,
  ROOF_PITCH,
  SLAB,
  STOREY_H,
  wallLength,
  wallPieces,
} from "./plan";
import type { P, Wall } from "./plan";

/** Plan metres to world: x east, z south (towards the camera at azimuth 0), y up. */
export const W3 = (p: P, y = 0): THREE.Vector3 => new THREE.Vector3(p.x - CENTER.x, y, CENTER.y - p.y);

const SILL = 0.9;
const HEAD = 2.2;

/** Face colour by the direction it faces: the logo's cube read as a building. */
function faceColor(n: THREE.Vector3, top: string) {
  if (n.y > 0.6) return top;
  if (n.y < -0.6) return C.tuerkis300;
  if (n.z > 0.6) return C.paper; // south
  if (n.x > 0.6) return C.tuerkis200; // east
  if (n.z < -0.6) return C.tuerkis300; // north
  if (n.x < -0.6) return "#f1f8f9"; // west
  // Slanted (the roof): by its horizontal direction.
  return n.z > 0 ? C.paper : C.tuerkis100;
}

export interface Built {
  pos: number[];
  col: number[];
  lines: number[];
}

const empty = (): Built => ({ pos: [], col: [], lines: [] });

/** A prism: a planar polygon at `o` in the (u, v) basis, extruded along `w`. */
function prism(out: Built, poly: [number, number][], o: THREE.Vector3, u: THREE.Vector3, v: THREE.Vector3, w: THREE.Vector3, top: string) {
  const at = (p: [number, number], back = false) => {
    const q = o.clone().addScaledVector(u, p[0]).addScaledVector(v, p[1]);
    return back ? q.add(w) : q;
  };
  const tris = THREE.ShapeUtils.triangulateShape(poly.map((p) => new THREE.Vector2(p[0], p[1])), []);
  const push = (a: THREE.Vector3, b: THREE.Vector3, c: THREE.Vector3) => {
    const n = b.clone().sub(a).cross(c.clone().sub(a)).normalize();
    const col = new THREE.Color(faceColor(n, top));
    for (const p of [a, b, c]) {
      out.pos.push(p.x, p.y, p.z);
      out.col.push(col.r, col.g, col.b);
    }
  };
  // Orientation: make the front face point against w.
  const n0 = u.clone().cross(v);
  const flip = n0.dot(w) > 0;
  for (const [i, j, k] of tris) {
    const a = at(poly[i]!), b = at(poly[j]!), c = at(poly[k]!);
    const a2 = at(poly[i]!, true), b2 = at(poly[j]!, true), c2 = at(poly[k]!, true);
    if (flip) {
      push(a, c, b);
      push(a2, b2, c2);
    } else {
      push(a, b, c);
      push(a2, c2, b2);
    }
  }
  // Sides: orient each outward from the polygon's centre.
  const cx = poly.reduce((s, p) => s + p[0], 0) / poly.length;
  const cy = poly.reduce((s, p) => s + p[1], 0) / poly.length;
  const mid = at([cx, cy]).addScaledVector(w, 0.5);
  for (let i = 0; i < poly.length; i++) {
    const p = poly[i]!, q = poly[(i + 1) % poly.length]!;
    const a = at(p), b = at(q), a2 = at(p, true), b2 = at(q, true);
    const n = b.clone().sub(a).cross(a2.clone().sub(a));
    const c = a.clone().add(b2).multiplyScalar(0.5);
    if (n.dot(c.clone().sub(mid)) > 0) {
      push(a, b, b2);
      push(a, b2, a2);
    } else {
      push(a, b2, b);
      push(a, a2, b2);
    }
  }
}

const line = (out: Built, a: THREE.Vector3, b: THREE.Vector3) => out.lines.push(a.x, a.y, a.z, b.x, b.y, b.z);

/** A vertical prism from a plan polygon between heights y0 and y1. */
function column(out: Built, poly: P[], y0: number, y1: number, top: string) {
  const o = new THREE.Vector3(0, y0, 0);
  const u = new THREE.Vector3(1, 0, 0);
  const v = new THREE.Vector3(0, 0, -1);
  prism(out, poly.map((p) => [p.x - CENTER.x, p.y - CENTER.y]), o, u, v, new THREE.Vector3(0, y1 - y0, 0), top);
}

function unit(w: Wall) {
  const L = wallLength(w);
  return { x: (w.b.x - w.a.x) / L, y: (w.b.y - w.a.y) / L };
}

/** A point on a line through `origin` parallel to the wall, at centre line coordinate t. */
function onLine(w: Wall, origin: P, t: number): P {
  const d = unit(w);
  const off = (origin.x - w.a.x) * d.x + (origin.y - w.a.y) * d.y;
  return { x: origin.x + d.x * (t - off), y: origin.y + d.y * (t - off) };
}

/** The plan quad of a piece of an exterior wall, mitred at the corners. */
export function outerQuad(i: number, s0: number, s1: number): P[] {
  const w = OUTER_WALLS[i]!;
  const L = wallLength(w);
  const n = FOOTPRINT.length;
  const oA = FOOTPRINT[i]!, oB = FOOTPRINT[(i + 1) % n]!;
  const iA = INNER_FACE[i]!, iB = INNER_FACE[(i + 1) % n]!;
  const start = s0 < 1e-6;
  const end = s1 > L - 1e-6;
  return [start ? oA : onLine(w, oA, s0), end ? oB : onLine(w, oB, s1), end ? iB : onLine(w, iB, s1), start ? iA : onLine(w, iA, s0)];
}

export function innerQuad(w: Wall, s0: number, s1: number): P[] {
  const d = unit(w);
  const n = { x: -d.y * (w.t / 2), y: d.x * (w.t / 2) };
  const a = { x: w.a.x + d.x * s0, y: w.a.y + d.y * s0 };
  const b = { x: w.a.x + d.x * s1, y: w.a.y + d.y * s1 };
  return [
    { x: a.x - n.x, y: a.y - n.y },
    { x: b.x - n.x, y: b.y - n.y },
    { x: b.x + n.x, y: b.y + n.y },
    { x: a.x + n.x, y: a.y + n.y },
  ];
}

/** One wall of one full storey (EG to 2.OG): its solid bands with real openings, and its ink lines. */
export function buildWall(w: Wall, storey: number, topColor: string = C.apricot300): Built {
  const out = empty();
  const H = STOREY_H;
  const quad = (s0: number, s1: number) => (w.outer ? outerQuad(OUTER_WALLS.indexOf(w), s0, s1) : innerQuad(w, s0, s1));
  const bands: [number, number, ("door" | "window")[], string][] = [
    [0, SILL, ["door"], C.paper],
    [SILL, HEAD, ["door", "window"], C.paper],
    [HEAD, H, [], topColor],
  ];
  for (const [y0, y1, kinds, top] of bands) for (const [s0, s1] of wallPieces(w, kinds, storey)) column(out, quad(s0, s1), y0, y1, top);

  // Ink: the top outline, the outer face's corners and every opening.
  const L = wallLength(w);
  const full = quad(0, L);
  const [oA, oB, iB, iA] = full.map((p) => W3(p, H));
  line(out, oA!, oB!);
  line(out, iA!, iB!);
  if (!w.outer) {
    line(out, oA!, iA!);
    line(out, oB!, iB!);
  }
  const base = w.outer ? 0 : 0;
  line(out, W3(full[0]!, base), W3(full[1]!, base));
  if (w.outer) line(out, W3(full[0]!, base), W3(full[0]!, H));
  else {
    line(out, W3(full[3]!, base), W3(full[2]!, base));
    for (const p of [full[0]!, full[1]!, full[2]!, full[3]!]) line(out, W3(p, base), W3(p, H));
  }
  for (const op of OPENINGS.filter((x) => x.wall === w.id && !(storey > 0 && x.egOnly))) {
    const s0 = op.at - op.width / 2;
    const s1 = op.at + op.width / 2;
    const yb = op.kind === "door" ? 0 : SILL;
    const faces = w.outer ? [0, 3] : [0, 3];
    for (const f of faces) {
      const q = quad(s0, s1);
      const a = q[f === 0 ? 0 : 3]!;
      const b = q[f === 0 ? 1 : 2]!;
      line(out, W3(a, yb), W3(b, yb));
      line(out, W3(a, HEAD), W3(b, HEAD));
      line(out, W3(a, yb), W3(a, HEAD));
      line(out, W3(b, yb), W3(b, HEAD));
    }
  }
  return out;
}

/** The floor slab under an upper storey, sitting on the storey below. */
export function buildSlab(poly: P[] = FOOTPRINT): Built {
  const out = empty();
  column(out, poly, -SLAB, 0, C.tuerkis100);
  for (let i = 0; i < poly.length; i++) {
    const a = poly[i]!, b = poly[(i + 1) % poly.length]!;
    line(out, W3(a, -SLAB), W3(b, -SLAB));
    line(out, W3(a, -SLAB), W3(a, 0));
  }
  return out;
}

/** The roof storey: knee walls on the main rectangle, gable ends, and a 38 degree roof. */
export const MAIN: P[] = [
  { x: 0, y: 0 },
  { x: 12.4, y: 0 },
  { x: 12.4, y: 8.75 },
  { x: 0, y: 8.75 },
];
const DEPTH = 8.75;
const RISE = (DEPTH / 2) * Math.tan((ROOF_PITCH * Math.PI) / 180);
export const RIDGE = KNEE + RISE;

export function buildDG(): Built {
  const out = empty();
  const t = OUTER_T;
  // South and north knee walls.
  column(out, [{ x: 0, y: 0 }, { x: 12.4, y: 0 }, { x: 12.4, y: t }, { x: 0, y: t }], 0, KNEE, C.apricot300);
  column(out, [{ x: 0, y: DEPTH - t }, { x: 12.4, y: DEPTH - t }, { x: 12.4, y: DEPTH }, { x: 0, y: DEPTH }], 0, KNEE, C.apricot300);
  // Gable ends: a pentagon in the (south to north, up) plane, extruded along x.
  const gable: [number, number][] = [
    [0, 0],
    [DEPTH, 0],
    [DEPTH, KNEE],
    [DEPTH / 2, RIDGE],
    [0, KNEE],
  ];
  for (const x0 of [0, 12.4 - t]) {
    const o = W3({ x: x0, y: 0 });
    prism(out, gable, o, new THREE.Vector3(0, 0, -1), new THREE.Vector3(0, 1, 0), new THREE.Vector3(t, 0, 0), C.apricot300);
    const xf = x0 === 0 ? 0 : 12.4;
    const pts = gable.map(([s, h]) => W3({ x: xf, y: s }, h));
    for (let i = 0; i < pts.length; i++) line(out, pts[i]!, pts[(i + 1) % pts.length]!);
    // A small gable window, centred.
    const g = [
      W3({ x: xf, y: DEPTH / 2 - 0.45 }, KNEE + 0.5),
      W3({ x: xf, y: DEPTH / 2 + 0.45 }, KNEE + 0.5),
      W3({ x: xf, y: DEPTH / 2 + 0.45 }, KNEE + 1.7),
      W3({ x: xf, y: DEPTH / 2 - 0.45 }, KNEE + 1.7),
    ];
    for (let i = 0; i < 4; i++) line(out, g[i]!, g[(i + 1) % 4]!);
  }
  for (const y of [0, DEPTH]) {
    line(out, W3({ x: 0, y }, KNEE), W3({ x: 12.4, y }, KNEE));
    line(out, W3({ x: 0, y }, 0), W3({ x: 12.4, y }, 0));
  }
  return out;
}

/** The two roof planes with eaves and verges, and the hatch the product draws on roofs. */
export function buildRoof(): { solid: Built; hatch: number[] } {
  const out = empty();
  const over = 0.45;
  const verge = 0.35;
  const thick = 0.24;
  const a = (ROOF_PITCH * Math.PI) / 180;
  const run = DEPTH / 2 + over;
  const slope = run / Math.cos(a);
  const hatch: number[] = [];
  for (const side of [1, -1]) {
    // From the eave (outside) up to the ridge, along the slope.
    const eave = { y: side === 1 ? -over : DEPTH + over };
    const yEave = KNEE - over * Math.tan(a);
    const o = W3({ x: -verge, y: eave.y }, yEave);
    const u = new THREE.Vector3(0, Math.sin(a), side === 1 ? -Math.cos(a) : Math.cos(a)); // up the slope
    const n = new THREE.Vector3(0, Math.cos(a), side === 1 ? Math.sin(a) : -Math.sin(a)); // out of the roof
    const x = new THREE.Vector3(12.4 + 2 * verge, 0, 0);
    // Rectangle in (x, slope), extruded along the roof normal by its thickness.
    prism(out, [[0, 0], [1, 0], [1, slope], [0, slope]], o, x.clone(), u, n.clone().multiplyScalar(thick), C.paper);
    const top = (s: number, t: number) => o.clone().addScaledVector(x, s).addScaledVector(u, t).addScaledVector(n, thick + 0.012);
    const edge = (s: number, t: number) => o.clone().addScaledVector(x, s).addScaledVector(u, t);
    // Outline.
    for (const [p, q] of [
      [top(0, 0), top(1, 0)],
      [top(0, 0), top(0, slope)],
      [top(1, 0), top(1, slope)],
      [edge(0, 0), edge(1, 0)],
      [edge(0, 0), top(0, 0)],
      [edge(1, 0), top(1, 0)],
    ] as const)
      line(out, p, q);
    // Hatch: lines down the slope every 0.42 m.
    const count = Math.floor((12.4 + 2 * verge) / 0.42);
    for (let k = 1; k < count; k++) {
      const s = k / count;
      const p = top(s, 0.05), q = top(s, slope - 0.05);
      hatch.push(p.x, p.y, p.z, q.x, q.y, q.z);
    }
  }
  // Ridge line.
  const r0 = W3({ x: -0.35, y: DEPTH / 2 }, RIDGE + thick / Math.cos(a));
  const r1 = W3({ x: 12.75, y: DEPTH / 2 }, RIDGE + thick / Math.cos(a));
  line(out, r0, r1);
  return { solid: out, hatch };
}

export function toGeometry(b: Built) {
  const g = new THREE.BufferGeometry();
  g.setAttribute("position", new THREE.Float32BufferAttribute(b.pos, 3));
  g.setAttribute("color", new THREE.Float32BufferAttribute(b.col, 3));
  return g;
}

/** Wall order for the rising wave: around the house from the south west, then the inside. */
export const WAVE: Wall[] = [...OUTER_WALLS, ...INNER_WALLS];
export function waveDelay(w: Wall) {
  const mx = (w.a.x + w.b.x) / 2 - CENTER.x;
  const my = (w.a.y + w.b.y) / 2 - CENTER.y;
  const ang = (Math.atan2(my, mx) + Math.PI * 1.25) % (Math.PI * 2);
  return (ang / (Math.PI * 2)) * (w.outer ? 1 : 0.8);
}
