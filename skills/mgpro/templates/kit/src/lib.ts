import { Easing, interpolate, spring } from "remotion";
import cueList from "./cues.json";
import music from "./music.json";

/**
 * The film's own grid, from its sonic brief (src/music.json): every film has its own tempo and
 * meter, so never hard code 30 frames per beat. At 60 fps a beat is 3600 / BPM frames.
 */
export const FPS = 60;
export const LENGTH = Math.round((music.length ?? 30) * FPS);
export const BPM: number = music.bpm;
export const BEAT = (FPS * 60) / BPM;
export const BAR = BEAT * ((music as { beats_per_bar?: number }).beats_per_bar ?? 4);
/** A frame on the grid: bar and beat counted from 0, fractions allowed (an 8th is 0.5). */
export const at = (bar: number, beat = 0) => Math.round(bar * BAR + beat * BEAT);

/** Where each section of the form starts, in frames: SECTION.drop, SECTION.end ... */
export const SECTION: Record<string, number> = (() => {
  const out: Record<string, number> = {};
  let bars = 0;
  for (const s of music.form) {
    out[s.name] = at(bars);
    bars += s.bars;
  }
  return out;
})();

/** Scene starts. Name the acts after the form's sections so picture and music cut together. */
export const T = SECTION;

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
  cell?: number;
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

/**
 * The product's own tokens, copied from its design system (never invented). Keep the key names:
 * the kit reads stage, ink, muted and accent. Examples: examples/bauwerk (light, navy) and
 * examples/torq (near black, lime).
 */
export const COLOR = {
  stage: "#f2f4f7",
  night: "#07131f",
  ink: "#0d2137",
  muted: "#66727f",
  accent: "#024e7b",
  ok: "#2a8a57",
} as const;

/** The AI's own gradient (Apple Intelligence order). Only for products that actually have AI. */
export const AI_GRADIENT = ["#3d7bff", "#a855f7", "#ff5c8a", "#ffb547", "#3d7bff"];

/** The product's font first. */
export const FONT = "'Brand Font Variable', system-ui, sans-serif";
export const MONO = "'Geist Mono Variable', ui-monospace, monospace";
