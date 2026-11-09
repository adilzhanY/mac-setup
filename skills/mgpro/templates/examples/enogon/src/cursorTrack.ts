import { project, threeCamera } from "./camera";
import { makePath } from "./Cursor";
import type { Click, CursorTrack } from "./Cursor";
import { F, camAt } from "./timeline";

export const BUTTON = { x: 1236, y: 560, w: 520, h: 120 };
const CARD0 = { x: 120, y: 600, w: 260, h: 196 };
const DROP = { x: 1222, y: 554 };
const accel = (t: number) => t * t * t;

const wall = project(threeCamera(camAt(F.hover)), [0.6, 1.45, 4.975]);

/** One cursor for the whole film: enters and leaves through the frame edges, never fades in place. */
export const TRACK: CursorTrack = {
  stops: [
    { f: 0, x: 330, y: 1220 },
    { f: F.grab - 2, x: CARD0.x + CARD0.w / 2, y: CARD0.y + CARD0.h / 2, leave: F.grab + 4 },
    { f: F.release - 4, x: DROP.x, y: DROP.y, leave: F.release + 8, arc: -0.12 },
    { f: F.release + 46, x: 2010, y: 1180, ease: accel },
    { f: F.hover - 48, x: 1990, y: 1160 },
    { f: F.hover, x: wall.x, y: wall.y, leave: F.click + 10, arc: 0.18 },
    { f: F.field, x: 1702, y: 452, leave: F.type + 26, arc: -0.08 },
    { f: F.press - 4, x: BUTTON.x + 300, y: BUTTON.y + 66, leave: F.done + 8, arc: 0.1 },
    { f: F.done + 44, x: 2010, y: 260, ease: accel },
  ],
  shapes: [
    { f: F.grab - 12, shape: "hand" },
    { f: F.grab, shape: "grab" },
    { f: F.release + 2, shape: "arrow" },
    { f: F.field - 6, shape: "text" },
    { f: F.type + 24, shape: "arrow" },
    { f: F.press - 14, shape: "hand" },
  ],
};

export const CLICKS: Click[] = [
  { f: F.grab, style: "none" },
  { f: F.click, style: "ring" },
  { f: F.field, style: "none" },
  { f: F.press, style: "none" },
];

export const PATH = makePath(TRACK, 1700, CLICKS, [F.grab, F.release]);

/** The dragged file card rides on the cursor, so it lags, swings and settles with it. */
export function cardRect(frame: number) {
  const lift = Math.min(1, Math.max(0, (frame - F.grab) / 8)) * (1 - Math.min(1, Math.max(0, (frame - (F.release - 6)) / 6)));
  const s = 1 + 0.04 * lift;
  const w = CARD0.w * s, h = CARD0.h * s;
  if (frame < F.grab) return { x: CARD0.x, y: CARD0.y, w, h, lift, tilt: 0 };
  const f = Math.min(frame, F.release);
  const p = PATH.at(f);
  const q = PATH.at(f - 6);
  const tilt = Math.max(-9, Math.min(9, (p.x - q.x) * 0.06));
  return { x: p.x - w / 2, y: p.y - h / 2 - 6 * lift, w, h, lift, tilt };
}
