import { Img, staticFile } from "remotion";
import { EASE, FONT, clamp } from "./lib";

/** A place the cursor arrives at (`f`) and may rest at until `leave`. */
export interface Stop {
  f: number;
  x: number;
  y: number;
  leave?: number;
  /** Bulge of the path towards this stop, as a share of its length; sign picks the side. */
  arc?: number;
  /** The move's easing, when it must match something else (a dragged thumb); minimum jerk otherwise. */
  ease?: (t: number) => number;
}

export interface CursorTrack {
  stops: Stop[];
  /** Shape changes: the macOS cursor turns into the hand over links and the I-beam over text. */
  shapes?: { f: number; shape: Shape }[];
  clicks?: number[];
  /** Visibility changes, faded over 8 frames. */
  visible?: { f: number; on: boolean }[];
}

type Shape = "arrow" | "hand" | "text" | "grab";

/** The macOS-White theme from this PC (96 px images) and each image's hotspot. */
const SHAPES: Record<Shape, { src: string; x: number; y: number }> = {
  arrow: { src: "cursor/left_ptr.png", x: 30, y: 14 },
  hand: { src: "cursor/hand2.png", x: 34, y: 19 },
  text: { src: "cursor/xterm.png", x: 48, y: 51 },
  grab: { src: "cursor/grabbing.png", x: 51, y: 32 },
};

/** Where the cursor is: a minimum-jerk move between stops along a gentle arc, like a hand. */
export function cursorAt(stops: Stop[], frame: number) {
  let i = 0;
  while (i < stops.length - 1 && frame >= stops[i + 1]!.f) i++;
  const a = stops[i]!;
  const b = stops[i + 1];
  const leave = a.leave ?? a.f;
  if (!b || frame <= leave) return { x: a.x, y: a.y };
  const t = clamp((frame - leave) / (b.f - leave));
  const e = (b.ease ?? EASE.jerk)(t);
  const dx = b.x - a.x;
  const dy = b.y - a.y;
  const bulge = (b.arc ?? 0.1) * Math.sin(Math.PI * e);
  return { x: a.x + dx * e - dy * bulge, y: a.y + dy * e + dx * bulge };
}

function visibility(track: CursorTrack, frame: number) {
  const events = track.visible ?? [];
  if (!events.length) return 1;
  let last: { f: number; on: boolean } | undefined;
  for (const v of events) if (frame >= v.f) last = v;
  if (!last) return events[0]!.on ? 0 : 1;
  const t = clamp((frame - last.f) / 8);
  return last.on ? t : 1 - t;
}

/** Cursor springs from Cap (open source, "inspired by Screen Studio"): tension, mass, friction. */
const SPRINGS = {
  mellow: [470, 3, 70],
  click: [530, 1, 40],
  drag: [1000, 1, 40],
} as const;

export interface Click {
  f: number;
  /** ring: an ink ring spreads; none: the target reacts on its own (a field, a button). */
  style?: "ring" | "none";
}

/** Power3 out between stops: fast away, decelerating into the target as if pulled in. */
const out3 = (t: number) => 1 - Math.pow(1 - t, 3);

/**
 * The cursor's real path for every frame: the stops give a target (an arc between them, power3
 * out), and a spring follows that target, stiffer near clicks and while dragging. Computed once.
 */
export function makePath(track: CursorTrack, frames: number, clicks: Click[], drag?: [number, number]) {
  const xs = new Float64Array(frames);
  const ys = new Float64Array(frames);
  const t0 = cursorAt(track.stops.map((s) => ({ ...s, ease: s.ease ?? out3 })), 0);
  let x = t0.x, y = t0.y, vx = 0, vy = 0;
  const stops = track.stops.map((s) => ({ ...s, ease: s.ease ?? out3 }));
  for (let f = 0; f < frames; f++) {
    const tgt = cursorAt(stops, f);
    const nearClick = clicks.some((c) => f >= c.f - 12 && f <= c.f + 4);
    const dragging = drag && f >= drag[0] && f <= drag[1];
    const [k, m, c] = dragging ? SPRINGS.drag : nearClick ? SPRINGS.click : SPRINGS.mellow;
    const sub = 8;
    const dt = 1 / 60 / sub;
    for (let i = 0; i < sub; i++) {
      const ax = (k * (tgt.x - x) - c * vx) / m;
      const ay = (k * (tgt.y - y) - c * vy) / m;
      vx += ax * dt;
      vy += ay * dt;
      x += vx * dt;
      y += vy * dt;
    }
    xs[f] = x;
    ys[f] = y;
  }
  const at = (f: number) => {
    const i = Math.max(0, Math.min(frames - 1, Math.round(f)));
    return { x: xs[i]!, y: ys[i]! };
  };
  return { at };
}

/** Press: down to 0.84 in 0.1 s (ease in), back in 0.22 s (ease out), the HeyGen launch timing. */
function press(clicks: Click[], frame: number) {
  let p = 0;
  for (const c of clicks) {
    const d = frame - c.f;
    if (d >= -6 && d < 0) p = Math.max(p, Math.pow((d + 6) / 6, 2));
    else if (d >= 0 && d < 13) p = Math.max(p, 1 - out3(d / 13));
  }
  return p;
}

/**
 * The person's own cursor, the macOS-White arrow, hand, I-beam and grab, alive: it follows a spring,
 * tilts with its horizontal speed (as in Figma and launch films), smears when fast, squashes on a
 * press, and enters and leaves through the frame edges instead of fading.
 */
export function MacCursor({ track, frame, path, clicks, scale = 1.15 }: { track: CursorTrack; frame: number; path: ReturnType<typeof makePath>; clicks: Click[]; scale?: number }) {
  const pos = path.at(frame);
  const back = path.at(frame - 24);
  const prev = path.at(frame - 1);
  const tilt = Math.max(-20, Math.min(20, (pos.x - back.x) * 0.03 * 0.15 * 2));
  const dx = pos.x - prev.x, dy = pos.y - prev.y;
  const speed = Math.hypot(dx, dy);
  const shapes = track.shapes ?? [];
  let shape: Shape = "arrow";
  let from: Shape = "arrow";
  let since = 1e9;
  for (const s of shapes) {
    if (frame < s.f) break;
    from = shape;
    shape = s.shape;
    since = frame - s.f;
  }
  const blend = clamp(since / 3);
  const p = press(clicks, frame);
  const draw = (s: Shape, o: number, at: { x: number; y: number }, key: string) => {
    const img = SHAPES[s];
    const k = scale * (1 - 0.16 * p);
    return (
      <Img
        key={key}
        src={staticFile(img.src)}
        style={{
          position: "absolute",
          left: at.x - img.x * k,
          top: at.y - img.y * k,
          width: 96 * k,
          height: 96 * k,
          opacity: o,
          transform: `rotate(${tilt}deg)`,
          transformOrigin: `${img.x * k}px ${img.y * k}px`,
          filter: "drop-shadow(0 6px 10px rgba(0,0,0,0.18))",
        }}
      />
    );
  };
  // Motion blur: ghosts along this frame's travel, only when it really moves fast.
  const ghosts = speed > 6 ? [0.25, 0.5, 0.75].map((g, n) => draw(shape, [0.22, 0.14, 0.07][n]!, { x: pos.x - dx * g, y: pos.y - dy * g }, `g${n}`)) : [];
  const rings = clicks.filter((c) => (c.style ?? "ring") === "ring" && frame >= c.f && frame < c.f + 36);
  return (
    <div style={{ position: "absolute", inset: 0, pointerEvents: "none" }}>
      {rings.map((c) => {
        const t = (frame - c.f) / 36;
        const r = 8 + 34 * out3(t);
        const at = path.at(c.f);
        return (
          <div
            key={c.f}
            style={{ position: "absolute", left: at.x - r, top: at.y - r, width: r * 2, height: r * 2, borderRadius: "50%", border: `2px solid rgba(0,0,0,${0.55 * (1 - t)})` }}
          />
        );
      })}
      {ghosts}
      {blend < 1 && draw(from, 1 - blend, pos, "from")}
      {draw(shape, blend, pos, "now")}
    </div>
  );
}

/** A collaborator's cursor as multiplayer apps draw it: an arrow in their colour with their name on a tag. */
export function RemoteCursor({ track, frame, color, name }: { track: CursorTrack; frame: number; color: string; name: string }) {
  const opacity = visibility(track, frame);
  if (opacity <= 0.001) return null;
  const pos = cursorAt(track.stops, frame);
  const p = press((track.clicks ?? []).map((f) => ({ f })), frame);
  const k = 1 - 0.12 * p;
  return (
    <div style={{ position: "absolute", left: pos.x, top: pos.y, opacity, pointerEvents: "none", transform: `scale(${k})`, transformOrigin: "0 0" }}>
      <svg width={34} height={38} viewBox="0 0 34 38" style={{ position: "absolute", left: -4, top: -3, filter: "drop-shadow(0 3px 6px rgba(13,33,55,.3))" }}>
        <path d="M5 3.5 L5 30 L12.2 23.4 L17.4 34.2 L22.6 31.8 L17.5 21.3 L27.2 21 Z" fill={color} stroke="white" strokeWidth={2.4} strokeLinejoin="round" />
      </svg>
      <div
        style={{
          position: "absolute",
          left: 22,
          top: 30,
          background: color,
          color: "white",
          fontFamily: FONT,
          fontWeight: 600,
          fontSize: 19,
          padding: "5px 13px 6px",
          borderRadius: 999,
          whiteSpace: "nowrap",
          boxShadow: "0 6px 16px -4px rgba(13,33,55,.35)",
        }}
      >
        {name}
      </div>
    </div>
  );
}
