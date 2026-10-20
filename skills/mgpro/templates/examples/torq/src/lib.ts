import { Easing, interpolate, spring } from "remotion";
import cueList from "./cues.json";

/** 60 fps at 120 BPM: a beat is 30 frames, a bar 120. */
export const FPS = 60;
export const LENGTH = 1800;

/** Scene starts, on the bar grid (see SCRIPT.md). */
export const T = {
  bar: 0,
  log: 240,
  engine: 420,
  forge: 600,
  gap: 825,
  drop: 840,
  friends: 960,
  streak: 1170,
  stop: 1290,
  payoff: 1320,
  end: 1560,
} as const;

export interface Cue {
  frame: number;
  sound: string;
  index?: number;
  row?: number;
  col?: number;
  value?: number;
  to?: string;
  char?: string;
  space?: boolean;
  seconds?: number;
}

export const CUES = cueList as Cue[];
export const cuesOf = (sound: string) => CUES.filter((c) => c.sound === sound);
/** The frame of the n-th cue of a sound. */
export const cueAt = (sound: string, n = 0) => cuesOf(sound)[n]?.frame ?? 0;

export const clamp = (v: number, a = 0, b = 1) => Math.min(b, Math.max(a, v));
export const mix = (a: number, b: number, t: number) => a + (b - a) * t;
/** Exponential mix, for zooms and distances: equal ratios in equal time. */
export const logMix = (a: number, b: number, t: number) => a * Math.pow(b / a, t);

export const EASE = {
  standard: Easing.bezier(0.4, 0, 0.2, 1),
  /** Expo out: the Apple entrance, fast start and a long soft landing. */
  out: Easing.bezier(0.16, 1, 0.3, 1),
  in: Easing.bezier(0.7, 0, 0.84, 0),
  inOut: Easing.bezier(0.83, 0, 0.17, 1),
  /** Minimum jerk: how a hand moves a mouse from rest to rest. */
  jerk: (t: number) => t * t * t * (10 - 15 * t + 6 * t * t),
};

/** 0 to 1 between two frames, eased, clamped. */
export function prog(frame: number, from: number, to: number, ease: (t: number) => number = EASE.standard) {
  if (to <= from) return frame >= to ? 1 : 0;
  return ease(clamp((frame - from) / (to - from)));
}

/** Springs: only results overshoot; the camera never does. */
export const SPRING = {
  snappy: { mass: 1, stiffness: 400, damping: 38 },
  settle: { mass: 1, stiffness: 300, damping: 30 },
  pop: { mass: 1, stiffness: 260, damping: 16 },
  soft: { mass: 1, stiffness: 120, damping: 20 },
  camera: { mass: 1.4, stiffness: 70, damping: 24, overshootClamping: true },
} as const;

export function sp(frame: number, start: number, config: keyof typeof SPRING = "settle") {
  if (frame < start) return 0;
  return spring({ frame: frame - start, fps: FPS, config: SPRING[config] });
}

/** A value over keyframes, each segment eased; holds outside. */
export function keys(frame: number, frames: number[], values: number[], ease: (t: number) => number = EASE.inOut) {
  return interpolate(frame, frames, values, { easing: ease, extrapolateLeft: "clamp", extrapolateRight: "clamp" });
}

/** Entrance of a block: rises out of a blur, Apple keynote style. */
export function enter(frame: number, start: number, { rise = 18, blur = 10, scale = 0.97, config = "settle" as keyof typeof SPRING } = {}) {
  const t = sp(frame, start, config);
  const b = blur * clamp(1 - (frame - start) / 14);
  return {
    opacity: clamp(t * 1.6),
    transform: `translateY(${(1 - t) * rise}px) scale(${scale + (1 - scale) * t})`,
    filter: b > 0.05 && frame >= start ? `blur(${b}px)` : frame < start ? `blur(${blur}px)` : undefined,
  };
}

/** The matching exit: up, soft and fast (12 frames, ease in). */
export function exit(frame: number, start: number, { lift = 14, blur = 8, length = 12 } = {}) {
  const t = prog(frame, start, start + length, EASE.in);
  return {
    opacity: 1 - t,
    transform: `translateY(${-lift * t}px)`,
    filter: t > 0.01 ? `blur(${blur * t}px)` : undefined,
  };
}

/** Merge an entrance and an exit into one style (exit wins once it has begun). */
export function inOut(frame: number, start: number, end: number, opts: Parameters<typeof enter>[2] = {}) {
  const a = enter(frame, start, opts);
  if (frame < end) return a;
  const b = exit(frame, end);
  return { ...b, opacity: a.opacity * b.opacity, transform: `${a.transform} ${b.transform}` };
}

/** torq's own tokens (src/theme.ts in the app). */
export const COLOR = {
  page: "#0E0F0E",
  deep: "#060706",
  page2: "#1B1E1A",
  surface: "#151714",
  ink: "#F2F4EE",
  soft: "#9AA294",
  faint: "#5C6356",
  line: "#262A24",
  hair: "#22261F",
  lime: "#C8FE23",
  limeInk: "#1A1B1A",
  pr: "#9C86E8",
  good: "#5AC8A0",
  warn: "#F0A742",
  gold: "#E9B920",
} as const;

export const lime = (a: number) => `rgba(200,254,35,${a})`;

/** The tier metals from RankBadge.tsx. */
export const TIERS = [
  { name: "Rust", base: "#A05A32", light: "#C77E4F", dark: "#7A4020" },
  { name: "Iron", base: "#9AA3AE", light: "#C3CBD4", dark: "#6E7681" },
  { name: "Bronze", base: "#C97E35", light: "#E8A55B", dark: "#96591F" },
  { name: "Silver", base: "#C9D2DA", light: "#EDF2F7", dark: "#97A2AD" },
  { name: "Gold", base: "#E9B920", light: "#FFDF5E", dark: "#B08812" },
  { name: "Platinum", base: "#A8D8DC", light: "#DFF6F8", dark: "#74A6AB" },
  { name: "Diamond", base: "#6FA9E8", light: "#A9D4FF", dark: "#4678B8" },
  { name: "Elite", base: "#A8D51C", light: "#C8FE23", dark: "#79A010" },
] as const;

export const FONT = "'Space Grotesk Variable', system-ui, sans-serif";
export const MONO = "'Geist Mono Variable', ui-monospace, monospace";
