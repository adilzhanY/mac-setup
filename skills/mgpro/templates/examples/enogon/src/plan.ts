/**
 * The example building from enogon.com, Lichtpausweg 7: a two flat Mehrfamilienhaus, 12,40 m
 * wide, four storeys (EG, 1.OG, 2.OG, DG), central stair in a bay on the north side. Plan
 * coordinates in metres: x east, y north, origin at the outer south west corner.
 */
export interface P {
  x: number;
  y: number;
}

export const OUTER_T = 0.36; // AW 008 on enogon.com: 0,36 m
export const INNER_T = 0.175;
export const STOREY_H = 2.87; // wall height on enogon.com
export const SLAB = 0.25;
export const LEVEL = STOREY_H + SLAB;
export const KNEE = 0.9;
export const ROOF_PITCH = 38;

/** The outer face of the exterior walls, counter clockwise from the south east corner, so the
 * south wall is the eighth: AW 008, as in the product's own example. */
export const FOOTPRINT: P[] = [
  { x: 12.4, y: 0 },
  { x: 12.4, y: 8.75 },
  { x: 7.4, y: 8.75 },
  { x: 7.4, y: 9.95 },
  { x: 5.0, y: 9.95 },
  { x: 5.0, y: 8.75 },
  { x: 0, y: 8.75 },
  { x: 0, y: 0 },
];

export const CENTER: P = { x: 6.2, y: 4.975 };

/** Offset a counter clockwise polygon (negative d goes inwards). Corners are mitred. */
export function offset(poly: P[], d: number): P[] {
  const n = poly.length;
  return poly.map((p, i) => {
    const a = poly[(i - 1 + n) % n]!;
    const b = poly[(i + 1) % n]!;
    const n1 = normal(a, p);
    const n2 = normal(p, b);
    const mx = n1.x + n2.x;
    const my = n1.y + n2.y;
    const len = Math.hypot(mx, my);
    const k = d / ((mx * n1.x + my * n1.y) / len) / len;
    return { x: p.x + mx * k, y: p.y + my * k };
  });
}

/** Outward normal of an edge of a counter clockwise polygon. */
function normal(a: P, b: P): P {
  const dx = b.x - a.x;
  const dy = b.y - a.y;
  const l = Math.hypot(dx, dy);
  return { x: dy / l, y: -dx / l };
}

export const INNER_FACE = offset(FOOTPRINT, -OUTER_T);

export interface Wall {
  id: string;
  a: P;
  b: P;
  t: number;
  outer: boolean;
}

/** Exterior walls along their centre line, AW 001 (east) to AW 008 (south). */
const CENTRE = offset(FOOTPRINT, -OUTER_T / 2);
export const OUTER_WALLS: Wall[] = CENTRE.map((a, i) => ({
  id: `AW ${String(i + 1).padStart(3, "0")}`,
  a,
  b: CENTRE[(i + 1) % CENTRE.length]!,
  t: OUTER_T,
  outer: true,
}));

const IW = (id: number, a: P, b: P, t = INNER_T): Wall => ({ id: `IW ${String(id).padStart(3, "0")}`, a, b, t, outer: false });
const yi = OUTER_T; // inner face of the south wall
export const INNER_WALLS: Wall[] = [
  IW(1, { x: 5.0, y: yi }, { x: 5.0, y: 8.75 - OUTER_T }),
  IW(2, { x: 7.4, y: yi }, { x: 7.4, y: 8.75 - OUTER_T }),
  IW(3, { x: OUTER_T, y: 4.6 }, { x: 12.4 - OUTER_T, y: 4.6 }),
  IW(4, { x: 3.1, y: 4.6 }, { x: 3.1, y: 8.75 - OUTER_T }, 0.115),
  IW(5, { x: 3.1, y: 6.6 }, { x: 5.0, y: 6.6 }, 0.115),
  IW(6, { x: 9.3, y: 4.6 }, { x: 9.3, y: 8.75 - OUTER_T }, 0.115),
  IW(7, { x: 7.4, y: 6.6 }, { x: 9.3, y: 6.6 }, 0.115),
];

export const WALLS = [...OUTER_WALLS, ...INNER_WALLS];

export type OpeningKind = "door" | "window";
export interface Opening {
  kind: OpeningKind;
  /** The wall it sits in. */
  wall: string;
  /** Centre along the wall from its start, metres. */
  at: number;
  width: number;
  /** Doors: which side the leaf swings to (1 or -1 across the wall) and the hinge end. */
  swing?: 1 | -1;
  hinge?: 0 | 1;
  /** Only in the ground floor (the entrance). */
  egOnly?: boolean;
}

const along = (w: string, x: number, y: number) => {
  const wall = WALLS.find((v) => v.id === w)!;
  const dx = wall.b.x - wall.a.x;
  const dy = wall.b.y - wall.a.y;
  const l = Math.hypot(dx, dy);
  return ((x - wall.a.x) * dx + (y - wall.a.y) * dy) / l;
};

/** AW 008 is the south wall, the one the edit scene selects. */
export const OPENINGS: Opening[] = [
  // South: five windows, as in the product's own example model.
  ...[1.3, 3.6, 6.2, 8.8, 11.1].map((x) => ({ kind: "window" as const, wall: "AW 008", at: along("AW 008", x, 0.18), width: 1.2 })),
  // East and west: two each.
  { kind: "window", wall: "AW 001", at: along("AW 001", 12.22, 2.3), width: 1.2 },
  { kind: "window", wall: "AW 001", at: along("AW 001", 12.22, 6.6), width: 1.0 },
  { kind: "window", wall: "AW 007", at: along("AW 007", 0.18, 2.3), width: 1.2 },
  { kind: "window", wall: "AW 007", at: along("AW 007", 0.18, 6.6), width: 1.0 },
  // North: bedrooms and baths.
  { kind: "window", wall: "AW 006", at: along("AW 006", 1.6, 8.57), width: 1.1 },
  { kind: "window", wall: "AW 006", at: along("AW 006", 4.05, 8.57), width: 0.7 },
  { kind: "window", wall: "AW 002", at: along("AW 002", 8.35, 8.57), width: 0.7 },
  { kind: "window", wall: "AW 002", at: along("AW 002", 10.8, 8.57), width: 1.1 },
  // Entrance into the stair bay.
  { kind: "door", wall: "AW 004", at: along("AW 004", 6.2, 9.77), width: 1.1, swing: -1, hinge: 0, egOnly: true },
  // Flat doors from the stair, and the doors inside each flat.
  { kind: "door", wall: "IW 001", at: along("IW 001", 5.0, 5.65), width: 0.9, swing: -1, hinge: 1 },
  { kind: "door", wall: "IW 002", at: along("IW 002", 7.4, 5.65), width: 0.9, swing: 1, hinge: 1 },
  { kind: "door", wall: "IW 003", at: along("IW 003", 4.05, 4.6), width: 0.85, swing: -1, hinge: 0 },
  { kind: "door", wall: "IW 005", at: along("IW 005", 4.05, 6.6), width: 0.8, swing: 1, hinge: 0 },
  { kind: "door", wall: "IW 004", at: along("IW 004", 3.1, 5.45), width: 0.85, swing: -1, hinge: 0 },
  { kind: "door", wall: "IW 001", at: along("IW 001", 5.0, 2.2), width: 0.9, swing: 1, hinge: 0 },
  { kind: "door", wall: "IW 003", at: along("IW 003", 8.35, 4.6), width: 0.85, swing: -1, hinge: 1 },
  { kind: "door", wall: "IW 007", at: along("IW 007", 8.35, 6.6), width: 0.8, swing: 1, hinge: 1 },
  { kind: "door", wall: "IW 006", at: along("IW 006", 9.3, 5.45), width: 0.85, swing: 1, hinge: 0 },
];

export interface Room {
  name: string;
  /** Axis aligned box, x0 x1 y0 y1, inside faces. */
  box: [number, number, number, number];
}

const o = OUTER_T;
const h = INNER_T / 2;
const q = 0.115 / 2;
export const ROOMS: Room[] = [
  { name: "Wohnen", box: [o, 5.0 - h, o, 4.6 - h] },
  { name: "Küche", box: [5.0 + h, 7.4 - h, o, 4.6 - h] },
  { name: "Wohnen", box: [7.4 + h, 12.4 - o, o, 4.6 - h] },
  { name: "Schlafen", box: [o, 3.1 - q, 4.6 + h, 8.75 - o] },
  { name: "Flur", box: [3.1 + q, 5.0 - h, 4.6 + h, 6.6 - q] },
  { name: "Bad", box: [3.1 + q, 5.0 - h, 6.6 + q, 8.75 - o] },
  { name: "Treppe", box: [5.0 + h, 7.4 - h, 4.6 + h, 9.95 - o] },
  { name: "Flur", box: [7.4 + h, 9.3 - q, 4.6 + h, 6.6 - q] },
  { name: "Bad", box: [7.4 + h, 9.3 - q, 6.6 + q, 8.75 - o] },
  { name: "Schlafen", box: [9.3 + q, 12.4 - o, 4.6 + h, 8.75 - o] },
];

export const roomArea = (r: Room) => (r.box[1] - r.box[0]) * (r.box[3] - r.box[2]);
export const roomCentre = (r: Room): P => ({ x: (r.box[0] + r.box[1]) / 2, y: (r.box[2] + r.box[3]) / 2 });

export const STOREYS = ["EG", "1.OG", "2.OG", "DG"] as const;

/** What the AI found, per full storey and for the whole model (the export summary). */
export const COUNTS = (() => {
  const full = 3;
  const doorsUpper = OPENINGS.filter((x) => !x.egOnly).length;
  const openings = OPENINGS.length + (full - 1) * doorsUpper;
  return {
    storeys: STOREYS.length,
    outerWalls: OUTER_WALLS.length * full,
    innerWalls: INNER_WALLS.length * full,
    openings,
    rooms: ROOMS.length * full,
    egWalls: WALLS.length,
    egDoors: OPENINGS.filter((x) => x.kind === "door").length,
    egWindows: OPENINGS.filter((x) => x.kind === "window").length,
    egRooms: ROOMS.length,
  };
})();

/** A point on a wall's centre line, s metres from its start. */
export function onWall(w: Wall, s: number): P {
  const dx = w.b.x - w.a.x;
  const dy = w.b.y - w.a.y;
  const l = Math.hypot(dx, dy);
  return { x: w.a.x + (dx / l) * s, y: w.a.y + (dy / l) * s };
}

export const wallLength = (w: Wall) => Math.hypot(w.b.x - w.a.x, w.b.y - w.a.y);
export const wallById = (id: string) => WALLS.find((w) => w.id === id)!;

/** Pieces of a wall between its openings (for the plan and for the solid parts of the 3D wall). */
export function wallPieces(w: Wall, kinds: OpeningKind[] = ["door", "window"], storey = 0): [number, number][] {
  const L = wallLength(w);
  const ops = OPENINGS.filter((x) => x.wall === w.id && kinds.includes(x.kind) && !(storey > 0 && x.egOnly))
    .map((x) => [x.at - x.width / 2, x.at + x.width / 2] as [number, number])
    .sort((a, b) => a[0] - b[0]);
  const out: [number, number][] = [];
  let s = 0;
  for (const [a, b] of ops) {
    if (a > s) out.push([s, a]);
    s = b;
  }
  if (s < L) out.push([s, L]);
  return out;
}
