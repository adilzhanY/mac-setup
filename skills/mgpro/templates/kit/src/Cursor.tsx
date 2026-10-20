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

function press(clicks: number[] | undefined, frame: number) {
  let p = 0;
  for (const c of clicks ?? []) {
    const d = frame - c;
    if (d >= -3 && d < 0) p = Math.max(p, (d + 3) / 3);
    else if (d >= 0 && d < 9) p = Math.max(p, 1 - d / 9);
  }
  return p;
}

/** The person's own cursor, the macOS-White arrow, hand, I-beam and grab, with a soft press. */
export function MacCursor({ track, frame, scale = 0.74, dark = false }: { track: CursorTrack; frame: number; scale?: number; dark?: boolean }) {
  const opacity = visibility(track, frame);
  if (opacity <= 0.001) return null;
  const pos = cursorAt(track.stops, frame);
  const prev = cursorAt(track.stops, frame - 1);
  const speed = Math.hypot(pos.x - prev.x, pos.y - prev.y);
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
  const p = press(track.clicks, frame);
  const ripples = (track.clicks ?? []).filter((c) => frame >= c && frame < c + 20);
  const draw = (s: Shape, o: number, at: { x: number; y: number }, key: string) => {
    const img = SHAPES[s];
    const k = scale * (1 - 0.14 * p);
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
        }}
      />
    );
  };
  // A short trail while the cursor moves fast, as a shutter would smear it.
  const trail = speed > 7 ? [0.33, 0.66].map((d, n) => draw(shape, opacity * (n ? 0.08 : 0.18), cursorAt(track.stops, frame - d), `t${n}`)) : [];
  return (
    <div style={{ position: "absolute", inset: 0, pointerEvents: "none" }}>
      {ripples.map((c) => {
        const t = (frame - c) / 20;
        const r = 10 + 22 * EASE.out(t);
        return (
          <div
            key={c}
            style={{
              position: "absolute",
              left: pos.x - r,
              top: pos.y - r,
              width: r * 2,
              height: r * 2,
              borderRadius: "50%",
              border: `2px solid ${dark ? "rgba(255,255,255,.5)" : "rgba(2,78,123,.35)"}`,
              opacity: (1 - t) * opacity,
            }}
          />
        );
      })}
      {trail}
      {blend < 1 && draw(from, opacity * (1 - blend), pos, "from")}
      {draw(shape, opacity * blend, pos, "now")}
    </div>
  );
}

/** A collaborator's cursor as multiplayer apps draw it: an arrow in their colour with their name on a tag. */
export function RemoteCursor({ track, frame, color, name }: { track: CursorTrack; frame: number; color: string; name: string }) {
  const opacity = visibility(track, frame);
  if (opacity <= 0.001) return null;
  const pos = cursorAt(track.stops, frame);
  const p = press(track.clicks, frame);
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
