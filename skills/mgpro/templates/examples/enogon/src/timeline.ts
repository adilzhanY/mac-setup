import type { Cam } from "./camera";

/** Every event of the film, in film frames (112.5 BPM: a beat is 32 frames, a bar 128). Scenes
 * overlap: the next action starts while the last one settles, so nothing waits. */
export const F = {
  // Hook: Grundriss rein (bar 0 to 1.25)
  zoneIn: 2,
  title1: 8,
  grab: 40,
  release: 108,
  sheetLand: 134,
  title1Out: 150,
  // The AI reads the plan (bar 1.25 to 3.5)
  title2: 162,
  traceStart: 172,
  traceLen: 64,
  innerStart: 228,
  innerStep: 6,
  innerLen: 14,
  doorStart: 262,
  doorStep: 4,
  roomStart: 298,
  roomStep: 4,
  thicken: 352,
  title2Out: 418,
  // Storeys (bar 3.5 to 6.5)
  tilt: 404,
  egRise: 458,
  egRiseLen: 64,
  title3: 500,
  stack: 500,
  land1: 548,
  land2: 580,
  land3: 612,
  roofLand: 660,
  title3Out: 690,
  title4: 700,
  title4Out: 820,
  // Edit (bar 6.5 to 8.5)
  title5: 838,
  hover: 888,
  click: 896,
  card: 900,
  field: 940,
  type: 954,
  title5Out: 1010,
  // Export (bar 8.5 to 10)
  title6: 1030,
  button: 1034,
  press: 1088,
  done: 1142,
  title6Out: 1196,
  // Logo (bar 10 to 12.5)
  net: 1214,
  fold: 1232,
  lid: 1276,
  logo: 1318,
  word: 1370,
  tag: 1392,
  url: 1404,
  fade: 1490,
  morph: 1214,
} as const;

/**
 * Monotone cubic interpolation (Fritsch and Carlson) through keyframes: the velocity is continuous
 * at every key, so the camera never stops dead at an accent, and it never overshoots a value.
 */
export function smooth(frame: number, xs: number[], ys: number[]) {
  const n = xs.length;
  if (frame <= xs[0]!) return ys[0]!;
  if (frame >= xs[n - 1]!) return ys[n - 1]!;
  const d: number[] = [];
  const m: number[] = [];
  for (let i = 0; i < n - 1; i++) d.push((ys[i + 1]! - ys[i]!) / (xs[i + 1]! - xs[i]!));
  m.push(d[0]!);
  for (let i = 1; i < n - 1; i++) m.push(d[i - 1]! * d[i]! <= 0 ? 0 : (d[i - 1]! + d[i]!) / 2);
  m.push(d[n - 2]!);
  for (let i = 0; i < n - 1; i++) {
    if (d[i] === 0) {
      m[i] = 0;
      m[i + 1] = 0;
      continue;
    }
    const a = m[i]! / d[i]!;
    const b = m[i + 1]! / d[i]!;
    const s = a * a + b * b;
    if (s > 9) {
      const t = 3 / Math.sqrt(s);
      m[i] = t * a * d[i]!;
      m[i + 1] = t * b * d[i]!;
    }
  }
  let i = 0;
  while (frame > xs[i + 1]!) i++;
  const h = xs[i + 1]! - xs[i]!;
  const t = (frame - xs[i]!) / h;
  const t2 = t * t;
  const t3 = t2 * t;
  return (2 * t3 - 3 * t2 + 1) * ys[i]! + (t3 - 2 * t2 + t) * h * m[i]! + (-2 * t3 + 3 * t2) * ys[i + 1]! + (t3 - t2) * h * m[i + 1]!;
}

const K = [0, 160, 404, 600, 672, 790, 884, 980, 1036, 1130, 1214, 1318, 1504];
const AZ = [0, 0, 0, 22, 30, 50, 16, 18, 26, 31, 34, 45, 45];
const EL = [89.9, 89.9, 89.9, 40, 36, 26, 10, 11, 22, 28, 30, 35.26, 35.26];
const DIST = [31, 29.5, 28, 50, 47, 41, 37, 38, 46, 50, 52, 336, 336];
const TX = [-4.4, -4.6, -4.4, -3.4, -0.8, -2.4, 2.2, 2.2, 3.6, 4.2, 3.0, 0, 0];
const TY = [0, 0, 0, 5.8, 5.6, 3.8, 7.9, 7.9, 7.0, 7.0, 7.5, 8, 8];
const TZ = [0, 0, 0, 0, 0, 0, 4.4, 4.4, 1.0, 0, 0, 0, 0];
const FOV = [30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 8, 8];

/** The box the model is packed into, which becomes the logo cube: side in metres, standing on the ground. */
export const CUBE_S = 16;

export function camAt(frame: number): Cam {
  return {
    az: smooth(frame, K, AZ),
    el: smooth(frame, K, EL),
    dist: smooth(frame, K, DIST),
    target: [smooth(frame, K, TX), smooth(frame, K, TY), smooth(frame, K, TZ)],
    fov: smooth(frame, K, FOV),
  };
}
