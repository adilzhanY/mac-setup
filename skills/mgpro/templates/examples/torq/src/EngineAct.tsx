import { useLayoutEffect, useRef } from "react";
import { AbsoluteFill } from "remotion";
import { Words } from "./kit";
import { COLOR, EASE, FONT, MONO, T, clamp, cueAt, enter, exit, lime, mix, prog, sp } from "./lib";
import { DOT } from "./LogAct";

/** Male raw bench, DOTS points by percentile: torq's own src/data/percentiles.json (OpenPowerlifting). */
const Q: [number, number][] = [
  [20, 0], [36.2, 0.01], [51.8, 0.05], [59.9, 0.1], [68.9, 0.2], [75.0, 0.3], [80.3, 0.4], [85.1, 0.5],
  [89.9, 0.6], [95.2, 0.7], [101.5, 0.8], [110.5, 0.9], [118.3, 0.95], [133.6, 0.99], [150, 1],
];
const LIFTERS = 401158;
const MIN = 20;
const MAX = 150;
const BINS = 52;
const N = 2200;
const X0 = 260;
const X1 = 1660;
const BASE = 850;
const BIN_W = (X1 - X0) / BINS;
const PITCH_Y = 10;
const DOT_SIZE = 9;
/** The lifter in this film: 87th percentile of the bench curve. */
const YOU_DOTS = 101.5 + 0.7 * (110.5 - 101.5);
const xOf = (dots: number) => X0 + ((dots - MIN) / (MAX - MIN)) * (X1 - X0);
const YOU_X = xOf(YOU_DOTS);

function cdf(x: number) {
  for (let i = 1; i < Q.length; i++) {
    const [x0, p0] = Q[i - 1]!;
    const [x1, p1] = Q[i]!;
    if (x <= x1) return p0 + ((x - x0) / (x1 - x0)) * (p1 - p0);
  }
  return 1;
}

const hash = (n: number) => {
  const s = Math.sin(n * 127.1 + 311.7) * 43758.5453;
  return s - Math.floor(s);
};

/** Every particle: its column, its slot in the stack and when it lands. Built once. */
const PARTICLES = (() => {
  const raw = Array.from({ length: BINS }, (_, b) => cdf(MIN + ((b + 1) * (MAX - MIN)) / BINS) - cdf(MIN + (b * (MAX - MIN)) / BINS));
  // Soften the piecewise steps of the quantile table into a smooth curve.
  const k = [0.06, 0.24, 0.4, 0.24, 0.06];
  const smooth = raw.map((_, b) => k.reduce((s, w, j) => s + w * (raw[clamp(b + j - 2, 0, BINS - 1)] ?? 0), 0));
  const total = smooth.reduce((a, b) => a + b, 0);
  const out: { x: number; y: number; land: number; from: number; seed: number; bin: number }[] = [];
  smooth.forEach((d, b) => {
    const count = Math.round((d / total) * N);
    for (let i = 0; i < count; i++) {
      const sub = i % 2;
      const row = Math.floor(i / 2);
      const seed = hash(b * 977 + i);
      out.push({
        x: X0 + b * BIN_W + BIN_W * (0.27 + sub * 0.46),
        y: BASE - 14 - row * PITCH_Y,
        land: 428 + row * 2.4 + seed * 9,
        from: -30 - hash(seed * 31) * 260,
        seed,
        bin: b,
      });
    }
  });
  return out;
})();
const MAX_LAND = Math.max(...PARTICLES.map((p) => p.land));

const FALL = 22;
const DROP = cueAt("pin");
const LIGHT = 546;

function Rain({ f }: { f: number }) {
  const ref = useRef<HTMLCanvasElement>(null);
  useLayoutEffect(() => {
    const ctx = ref.current?.getContext("2d");
    if (!ctx) return;
    ctx.clearRect(0, 0, 1920, 1080);
    for (const p of PARTICLES) {
      const start = p.land - FALL;
      if (f < start) continue;
      const t = clamp((f - start) / FALL);
      const y = f >= p.land ? p.y : mix(p.from, p.y, t * t);
      const landed = f >= p.land;
      // The columns left of the lifter light lime in a wave that runs toward the marker.
      const lit = p.x < YOU_X ? prog(f, LIGHT + ((p.x - X0) / (YOU_X - X0)) * 26, LIGHT + ((p.x - X0) / (YOU_X - X0)) * 26 + 8) : 0;
      const flash = landed ? 1 - clamp((f - p.land) / 10) : 0;
      if (!landed) {
        // A falling grain is a short streak, longer the faster it goes.
        const v = (2 * t * (p.y - p.from)) / FALL;
        ctx.fillStyle = `rgba(242,244,238,${0.35 + 0.4 * p.seed})`;
        ctx.fillRect(p.x - 1.5, y - Math.min(40, v * 1.2), 3, Math.min(40, v * 1.2) + 3);
        continue;
      }
      const g = Math.round(mix(74 + 150 * flash, 200, lit));
      const r = Math.round(mix(68 + 150 * flash, 200, lit));
      const b = Math.round(mix(64 + 150 * flash, 35, lit));
      ctx.fillStyle = `rgb(${r},${Math.round(mix(g, 254, lit))},${b})`;
      ctx.beginPath();
      ctx.roundRect(p.x - DOT_SIZE / 2, y - DOT_SIZE / 2, DOT_SIZE, DOT_SIZE, 2);
      ctx.fill();
    }
  }, [f]);
  return <canvas ref={ref} width={1920} height={1080} style={{ position: "absolute", inset: 0, filter: f >= LIGHT ? `drop-shadow(0 0 10px ${lime(0.25 * prog(f, LIGHT, LIGHT + 30))})` : undefined }} />;
}

/** The lifter: the dot from the rest timer hangs, then drops into its place on the curve. */
function You({ f }: { f: number }) {
  const bob = Math.sin((f - T.engine) / 14) * 6 * (1 - prog(f, 500, 520));
  const fallT = prog(f, DROP - 18, DROP, (x) => x * x);
  const x = mix(DOT.x, YOU_X, prog(f, 470, DROP, EASE.inOut));
  const y = f < DROP ? mix(DOT.y + bob, BASE + 26, fallT) : BASE + 26;
  const line = prog(f, DROP + 2, DROP + 20, EASE.out);
  const ripple = prog(f, DROP, DROP + 34, EASE.out);
  const tag = sp(f, DROP + 10, "pop");
  return (
    <>
      <svg width={1920} height={1080} style={{ position: "absolute", inset: 0 }}>
        <line x1={YOU_X} y1={BASE + 26} x2={YOU_X} y2={BASE + 26 - 520 * line} stroke={COLOR.lime} strokeWidth={3} style={{ filter: `drop-shadow(0 0 8px ${lime(0.7)})` }} />
        {f >= DROP && <ellipse cx={YOU_X} cy={BASE + 26} rx={12 + 90 * ripple} ry={(12 + 90 * ripple) * 0.32} fill="none" stroke={lime(0.7 * (1 - ripple))} strokeWidth={3} />}
        <circle cx={x} cy={y} r={DOT.r + (f >= DROP ? 3 * (1 - prog(f, DROP, DROP + 10)) : 0)} fill={COLOR.lime} style={{ filter: `drop-shadow(0 0 14px ${lime(0.8)})` }} />
      </svg>
      {tag > 0.001 && (
        <div
          style={{
            position: "absolute",
            left: YOU_X,
            top: BASE + 26 - 520 - 30,
            transform: `translate(-50%, -100%) scale(${tag})`,
            transformOrigin: "50% 100%",
            padding: "12px 22px",
            borderRadius: 999,
            background: COLOR.lime,
            color: COLOR.limeInk,
            fontSize: 26,
            fontWeight: 700,
            whiteSpace: "nowrap",
            boxShadow: `0 0 40px ${lime(0.45)}`,
          }}
        >
          YOU · {YOU_DOTS.toFixed(1)} DOTS
        </div>
      )}
    </>
  );
}

function Axis({ f }: { f: number }) {
  const s = enter(f, 428, { rise: 10 });
  return (
    <div style={{ position: "absolute", inset: 0, ...s }}>
      <div style={{ position: "absolute", left: X0 - 20, width: X1 - X0 + 40, top: BASE, height: 1.5, background: COLOR.line }} />
      {[40, 60, 80, 100, 120, 140].map((d) => (
        <div key={d} style={{ position: "absolute", left: xOf(d), top: BASE + 46, transform: "translateX(-50%)", fontFamily: MONO, fontSize: 18, color: COLOR.faint }}>{d}</div>
      ))}
      <div style={{ position: "absolute", right: 96, bottom: 70, fontSize: 19, color: COLOR.faint, letterSpacing: "0.02em" }}>Raw bench press, DOTS points · OpenPowerlifting</div>
    </div>
  );
}

/** Act III: the engine. Every lifter who ever benched at a meet rains down into one curve. */
export function EngineAct({ frame: f }: { frame: number }) {
  const counted = prog(f, 428, MAX_LAND, EASE.standard);
  const n = Math.round(LIFTERS * counted);
  const push = 1 + 0.035 * prog(f, T.engine, T.forge, EASE.standard);
  return (
    <AbsoluteFill style={{ fontFamily: FONT, background: `radial-gradient(80% 60% at 50% 100%, #10140b 0%, ${COLOR.deep} 70%)` }}>
      <AbsoluteFill style={{ transform: `scale(${push})`, transformOrigin: "50% 80%" }}>
        <Axis f={f} />
        <Rain f={f} />
        <You f={f} />
      </AbsoluteFill>
      <div style={{ position: "absolute", left: 96, top: 92 }}>
        <Words lines={["Ranked against"]} frame={f} start={436} end={DROP - 4} size={64} color={COLOR.soft} weight={600} />
        <div
          style={{
            fontSize: 112,
            fontWeight: 700,
            letterSpacing: "-0.045em",
            color: COLOR.ink,
            marginTop: 6,
            fontVariantNumeric: "tabular-nums",
            ...(f >= DROP - 2 ? exit(f, DROP - 2, { lift: 20 }) : enter(f, 444, { rise: 30 })),
          }}
        >
          {n.toLocaleString("en-US")} <span style={{ color: COLOR.lime }}>lifters.</span>
        </div>
      </div>
      <div style={{ position: "absolute", left: 96, top: 92 }}>
        <Words lines={["Stronger than *87%"]} frame={f} start={DROP + 14} size={112} />
        <div style={{ marginTop: 10 }}>
          <Words lines={["of competitive lifters."]} frame={f} start={DROP + 26} size={56} color={COLOR.soft} weight={600} />
        </div>
      </div>
    </AbsoluteFill>
  );
}
