import { Sparkles } from "lucide-react";
import { AbsoluteFill } from "remotion";
import { AiGlow, Glass, Words } from "./kit";
import { COLOR, EASE, FONT, MONO, T, clamp, cuesOf, mix, prog, sp } from "./lib";
import { EDGES, ROOF, STOREY_H, STOREYS, STREET } from "./plan";

/** The photo: the street facade drawn at 36 px per metre, framed like a phone picture. */
const S = 36;
const CARD = { x: 1000, y: 100, w: 640, h: 880 };
const WALL = EDGES[4]!.length;
const EAVE = STOREY_H * STOREYS;
const FX = (CARD.w - WALL * S) / 2;
const GROUND = CARD.h - 66;
const fx = (m: number) => FX + m * S;
const fy = (h: number) => GROUND - h * S;
const DETECT = cuesOf("detect");

/** Each opening's box on the photo, in the card's pixels. */
const BOXES = STREET.map((w) => ({
  x: fx(w.along - w.width / 2),
  y: fy(w.storey * STOREY_H + w.sill + w.height),
  w: w.width * S,
  h: w.height * S,
  door: !!w.door,
}));
const ROW_Y = [0, 1, 2, 3, 4].map((r) => BOXES[r * 6]!.y + BOXES[r * 6]!.h / 2);

/** Where the scan beam is: through each row as its openings are found. */
function beamY(f: number) {
  const pts: [number, number][] = [[T.scan, fy(EAVE + ROOF.rise) - 20]];
  ROW_Y.forEach((y, r) => pts.push([645 + 15 * r + 6, y]));
  pts.push([732, GROUND + 10]);
  if (f <= pts[0]![0]) return pts[0]![1];
  for (let i = 1; i < pts.length; i++) {
    const [f0, y0] = pts[i - 1]!;
    const [f1, y1] = pts[i]!;
    if (f <= f1) return mix(y0, y1, (f - f0) / (f1 - f0));
  }
  return pts[pts.length - 1]![1];
}

function Drawing() {
  const apex = { x: fx(WALL / 2), y: fy(EAVE + ROOF.rise) };
  return (
    <svg width={CARD.w} height={CARD.h} style={{ position: "absolute", inset: 0 }}>
      <defs>
        <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#8db6dc" />
          <stop offset="0.6" stopColor="#cfe0ee" />
          <stop offset="1" stopColor="#e9eef2" />
        </linearGradient>
        <pattern id="brick" width={18} height={5.4} patternUnits="userSpaceOnUse">
          <rect width={18} height={5.4} fill="#8a3b2f" />
          <rect x={0} y={4.6} width={18} height={0.8} fill="#a25a4b" opacity={0.55} />
          <rect x={8.6} y={0} width={0.8} height={2.7} fill="#a25a4b" opacity={0.45} />
          <rect x={0} y={2.7} width={0.8} height={2.7} fill="#a25a4b" opacity={0.45} />
          <rect x={9} y={2.7} width={9} height={1.9} fill="#7e3429" opacity={0.35} />
        </pattern>
        <linearGradient id="glass" x1="0" y1="0" x2="0.4" y2="1">
          <stop offset="0" stopColor="#9fb8cc" />
          <stop offset="0.45" stopColor="#3b4f62" />
          <stop offset="1" stopColor="#1d2733" />
        </linearGradient>
        <linearGradient id="pave" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#9a9590" />
          <stop offset="1" stopColor="#6f6b67" />
        </linearGradient>
        <radialGradient id="vig" cx="50%" cy="45%" r="75%">
          <stop offset="0.6" stopColor="#000" stopOpacity="0" />
          <stop offset="1" stopColor="#000" stopOpacity="0.38" />
        </radialGradient>
      </defs>
      <rect width={CARD.w} height={CARD.h} fill="url(#sky)" />
      <ellipse cx={120} cy={90} rx={140} ry={34} fill="#fff" opacity={0.5} />
      <ellipse cx={520} cy={150} rx={120} ry={26} fill="#fff" opacity={0.4} />
      {/* The neighbours, cut by the frame. */}
      <rect x={0} y={fy(EAVE + 1.2)} width={fx(0)} height={GROUND - fy(EAVE + 1.2)} fill="#d8ccb4" />
      <rect x={fx(WALL)} y={fy(EAVE - 0.8)} width={CARD.w - fx(WALL)} height={GROUND - fy(EAVE - 0.8)} fill="#b9b3aa" />
      {[1, 2, 3, 4].map((s) => (
        <g key={s}>
          <rect x={fx(0) - 46} y={fy(s * STOREY_H + 0.9 + 1.5)} width={30} height={1.5 * S} fill="#3a4654" />
          <rect x={fx(WALL) + 16} y={fy(s * STOREY_H + 0.9 + 1.5)} width={30} height={1.5 * S} fill="#3a4654" />
        </g>
      ))}
      {/* The facade: brick, gable, bands, cornice and a stone plinth. */}
      <polygon points={`${fx(0)},${fy(EAVE)} ${apex.x},${apex.y} ${fx(WALL)},${fy(EAVE)}`} fill="url(#brick)" />
      <circle cx={apex.x} cy={fy(EAVE + 2.2)} r={0.55 * S} fill="#efe6d6" />
      <circle cx={apex.x} cy={fy(EAVE + 2.2)} r={0.42 * S} fill="url(#glass)" />
      <rect x={fx(0)} y={fy(EAVE)} width={WALL * S} height={EAVE * S} fill="url(#brick)" />
      {[1, 2, 3, 4].map((s) => (
        <rect key={s} x={fx(0)} y={fy(s * STOREY_H) - 4} width={WALL * S} height={8} fill="#e8dcc6" />
      ))}
      <rect x={fx(0) - 8} y={fy(EAVE) - 6} width={WALL * S + 16} height={14} fill="#eadfca" />
      <rect x={fx(0) - 8} y={fy(EAVE) + 8} width={WALL * S + 16} height={4} fill="#000" opacity={0.18} />
      <rect x={fx(0)} y={fy(0.8)} width={WALL * S} height={0.8 * S} fill="#7f7872" />
      {STREET.map((w, i) => {
        const b = BOXES[i]!;
        return (
          <g key={i}>
            <rect x={b.x - 7} y={b.y - 11} width={b.w + 14} height={7} fill="#eadfca" />
            {!w.door && <rect x={b.x - 5} y={b.y + b.h} width={b.w + 10} height={5} fill="#d7cfc3" />}
            <rect x={b.x} y={b.y} width={b.w} height={b.h} fill="#f2efe8" />
            {w.door ? (
              <>
                <rect x={b.x + 3} y={b.y + 3} width={b.w - 6} height={b.h * 0.24} fill="url(#glass)" />
                <rect x={b.x + 3} y={b.y + b.h * 0.27} width={b.w - 6} height={b.h * 0.73 - 3} fill="#3b2a20" />
                <line x1={b.x + b.w / 2} y1={b.y + b.h * 0.27} x2={b.x + b.w / 2} y2={b.y + b.h} stroke="#2a1c15" strokeWidth={1.5} />
              </>
            ) : (
              <>
                <rect x={b.x + 3} y={b.y + 3} width={b.w - 6} height={b.h - 6} fill="url(#glass)" />
                <line x1={b.x + b.w / 2} y1={b.y + 3} x2={b.x + b.w / 2} y2={b.y + b.h - 3} stroke="#f2efe8" strokeWidth={2} />
                <line x1={b.x + 3} y1={b.y + b.h * 0.3} x2={b.x + b.w - 3} y2={b.y + b.h * 0.3} stroke="#f2efe8" strokeWidth={2} />
              </>
            )}
          </g>
        );
      })}
      <rect x={0} y={GROUND} width={CARD.w} height={CARD.h - GROUND} fill="url(#pave)" />
      <rect x={0} y={GROUND} width={CARD.w} height={3} fill="#5c5853" />
      <rect width={CARD.w} height={CARD.h} fill="url(#vig)" />
    </svg>
  );
}

/** Act II, second half: a facade photo lands, the AI reads it, and every opening peels off into depth. */
export function Facade({ frame }: { frame: number }) {
  const f = frame;
  const land = sp(f, T.facade, "pop");
  const glow = prog(f, 628, 650) * (1 - prog(f, T.lift, T.lift + 30));
  const beam = beamY(f);
  const scanning = f >= T.scan && f < 740;
  const found = DETECT.filter((d) => f >= d.frame).length;
  const lift = prog(f, T.lift, T.freeze, EASE.inOut);
  const bloom = prog(f, 812, T.drop, EASE.in);
  const label = (i: number, text: string, start: number) => {
    const b = BOXES[i]!;
    const t = sp(f, start, "pop");
    return (
      <div
        key={`l${i}`}
        style={{
          position: "absolute",
          left: b.x + b.w / 2,
          top: b.y - 30,
          transform: `translate(-50%, -100%) scale(${t})`,
          transformOrigin: "50% 100%",
          opacity: clamp(t * 2) * (1 - lift),
          background: "rgba(16,10,30,.78)",
          backdropFilter: "blur(8px)",
          color: "white",
          fontFamily: MONO,
          fontSize: 18,
          padding: "6px 11px",
          borderRadius: 8,
          whiteSpace: "nowrap",
          boxShadow: "0 0 0 1px rgba(216,180,254,.5)",
        }}
      >
        {text}
      </div>
    );
  };
  return (
    <AbsoluteFill style={{ fontFamily: FONT, background: "radial-gradient(90% 90% at 50% 45%, #0e2236 0%, #07121e 70%)" }}>
      <div style={{ position: "absolute", left: 96, top: 120 }}>
        <Words lines={["Finds every", "*window."]} frame={f} start={642} end={792} size={88} color="#ffffff" accent="#d8b4fe" />
      </div>
      {/* The count, ticking with every opening found. */}
      <div style={{ position: "absolute", left: 96, top: 420, opacity: clamp((f - 646) / 10) * (1 - prog(f, 790, 806)) }}>
        <Glass dark radius={28} style={{ padding: "22px 30px 24px" }}>
          <div style={{ display: "flex", alignItems: "center", gap: 18 }}>
            <span style={{ width: 52, height: 52, borderRadius: 999, background: "linear-gradient(135deg, #3d7bff, #a855f7 55%, #ff5c8a)", display: "inline-flex", alignItems: "center", justifyContent: "center", color: "white" }}>
              <Sparkles size={28} strokeWidth={2.2} />
            </span>
            <span style={{ fontFamily: MONO, fontSize: 64, fontWeight: 600, color: "white", width: 82, transform: `scale(${1 + 0.06 * clamp(1 - (f - (DETECT[found - 1]?.frame ?? -99)) / 5)})`, display: "inline-block" }}>
              {found}
            </span>
            <span style={{ fontSize: 26, color: "#c9b6ec", lineHeight: 1.2 }}>
              windows
              <br />
              and doors
            </span>
          </div>
        </Glass>
      </div>

      <div style={{ position: "absolute", left: CARD.x, top: CARD.y, width: CARD.w, height: CARD.h, perspective: 1700, transform: `scale(${1 + bloom * 0.12})` }}>
        <div
          style={{
            position: "absolute",
            inset: 0,
            transformStyle: "preserve-3d",
            transform: `translateY(${(1 - land) * -1000}px) rotate(${mix(-9, -1.5, land)}deg) rotateY(${-26 * lift}deg) rotateX(${12 * lift}deg)`,
          }}
        >
          <div style={{ position: "absolute", inset: 0, borderRadius: 26 }}>
            <AiGlow frame={f} radius={26} strength={glow} rim={4} spread={44} />
          </div>
          <div style={{ position: "absolute", inset: 0, borderRadius: 26, overflow: "hidden", boxShadow: "0 40px 90px -20px rgba(0,0,0,.7)", filter: `brightness(${1 - 0.65 * lift}) saturate(${1 - 0.6 * lift})` }}>
            <div style={{ position: "absolute", inset: 0 }}>
              <Drawing />
              {/* Below the beam the photo is still waiting: darker and soft. */}
              {scanning && (
                <>
                  <div style={{ position: "absolute", left: 0, right: 0, top: beam, bottom: 0, background: "rgba(6,14,26,.42)", backdropFilter: "blur(3px) saturate(.6)" }} />
                  <div style={{ position: "absolute", left: 0, right: 0, top: beam - 70, height: 70, background: "linear-gradient(180deg, transparent, rgba(168,85,247,.22))" }} />
                  <div style={{ position: "absolute", left: 0, right: 0, top: beam - 1.5, height: 3, background: "#f5ecff", boxShadow: "0 0 18px 6px rgba(168,85,247,.85), 0 0 60px 20px rgba(168,85,247,.35)" }} />
                </>
              )}
            </div>
          </div>
          {/* The openings found: corner brackets snap on, a violet mask pulses; they lift off at the end. */}
          <div style={{ position: "absolute", inset: 0, transformStyle: "preserve-3d", transform: "translateZ(1px)" }}>
            {BOXES.map((b, i) => {
              const d = DETECT[i]?.frame ?? 9999;
              if (f < d) return null;
              const t = prog(f, d, d + 9, EASE.out);
              const pulse = clamp(1 - (f - d) / 18);
              const z = 2 + 170 * prog(f, T.lift + (i % 6) * 3 + Math.floor(i / 6) * 2, T.lift + 40 + (i % 6) * 3 + Math.floor(i / 6) * 2, EASE.out);
              const k = 1.35 - 0.35 * t;
              const arm = Math.min(16, b.w * 0.3);
              const corner = (cx: number, cy: number, sx: number, sy: number) => (
                <path key={`${cx}${cy}`} d={`M${cx} ${cy + sy * arm} L${cx} ${cy} L${cx + sx * arm} ${cy}`} fill="none" stroke="#ffffff" strokeWidth={3} strokeLinecap="round" />
              );
              return (
                <div
                  key={i}
                  style={{
                    position: "absolute",
                    left: b.x - 5,
                    top: b.y - 5,
                    width: b.w + 10,
                    height: b.h + 10,
                    transform: `translateZ(${z}px) scale(${k})`,
                    opacity: t,
                  }}
                >
                  <div style={{ position: "absolute", inset: 5, borderRadius: 3, background: `rgba(168,85,247,${0.2 + 0.4 * pulse + 0.25 * lift})`, boxShadow: `0 0 ${10 + 20 * pulse}px rgba(168,85,247,${0.5 + 0.4 * pulse})` }} />
                  <svg width={b.w + 10} height={b.h + 10} style={{ position: "absolute", inset: 0, overflow: "visible", filter: "drop-shadow(0 0 4px rgba(216,180,254,.9))" }}>
                    {corner(1.5, 1.5, 1, 1)}
                    {corner(b.w + 8.5, 1.5, -1, 1)}
                    {corner(1.5, b.h + 8.5, 1, -1)}
                    {corner(b.w + 8.5, b.h + 8.5, -1, -1)}
                  </svg>
                </div>
              );
            })}
            {label(2, "0.98 × 1.60 m", (DETECT[2]?.frame ?? 0) + 4)}
            {label(16, "0.98 × 1.60 m", (DETECT[16]?.frame ?? 0) + 4)}
            {label(26, "Door 1.40 × 2.60 m", (DETECT[26]?.frame ?? 0) + 4)}
          </div>
        </div>
      </div>
      {/* White bloom into the drop. */}
      <AbsoluteFill style={{ background: `radial-gradient(circle at 50% 50%, rgba(255,255,255,${bloom}) ${bloom * 70}%, rgba(255,255,255,${bloom * bloom}) 100%)` }} />
    </AbsoluteFill>
  );
}

export const FACADE_COLOR = COLOR.brick;
