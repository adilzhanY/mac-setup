import { EASE, prog } from "./lib";

/**
 * A finger tap for mobile products, where a cursor would be wrong. No drawn finger: the tapped
 * control presses (pressScale) and a soft ring spreads from the touch point (TapRipple).
 */
export function pressScale(f: number, tap: number, depth = 0.08) {
  if (f < tap - 3 || f >= tap + 6) return 1;
  return 1 - depth * Math.sin(((f - (tap - 3)) / 9) * Math.PI);
}

export function TapRipple({ f, tap, x, y, size = 120, color = "255,255,255" }: { f: number; tap: number; x: number; y: number; size?: number; color?: string }) {
  if (f < tap - 2) return null;
  const t = prog(f, tap - 2, tap + 20, EASE.out);
  if (t >= 1) return null;
  const d = size * t;
  return <div style={{ position: "absolute", left: x - d / 2, top: y - d / 2, width: d, height: d, borderRadius: 999, border: `3px solid rgba(${color},${0.5 * (1 - t)})`, pointerEvents: "none" }} />;
}
