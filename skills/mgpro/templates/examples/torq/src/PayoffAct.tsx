import { AbsoluteFill } from "remotion";
import { Words } from "./kit";
import { COLOR, EASE, FONT, MONO, T, clamp, cuesOf, lime, mix, prog, sp } from "./lib";

/** A year of bench, estimated 1RM per month: plateaus, one deload dip, three records. */
const KG = [105, 107, 110, 110, 114, 117, 116, 121, 125, 124, 129, 135, 140];
const MONTHS = ["O", "N", "D", "J", "F", "M", "A", "M", "J", "J", "A", "S", "O"];
const X0 = 200;
const X1 = 1720;
const Y_LO = 940;
const Y_HI = 420;
const LO = 100;
const HI = 142;
const pt = (i: number) => ({ x: X0 + (i / (KG.length - 1)) * (X1 - X0), y: mix(Y_LO, Y_HI, (KG[i]! - LO) / (HI - LO)) });
const PTS = KG.map((_, i) => pt(i));

/** Catmull-Rom through the months, as cubic segments, so the glowing head can ride the exact curve. */
const SEGS = PTS.slice(1).map((p, j) => {
  const i = j + 1;
  const p0 = PTS[i - 2] ?? PTS[i - 1]!;
  const p1 = PTS[i - 1]!;
  const p3 = PTS[i + 1] ?? p;
  return [p1, { x: p1.x + (p.x - p0.x) / 6, y: p1.y + (p.y - p0.y) / 6 }, { x: p.x - (p3.x - p1.x) / 6, y: p.y - (p3.y - p1.y) / 6 }, p] as const;
});
const PATH = `M ${PTS[0]!.x} ${PTS[0]!.y} ` + SEGS.map(([, c1, c2, p]) => `C ${c1.x} ${c1.y} ${c2.x} ${c2.y} ${p.x} ${p.y}`).join(" ");

const START = T.payoff + 6;
/** Nine frames per month, so the head passes each record exactly on its "pr" cue. */
const PER = 9;
const PR_CUES = cuesOf("pr").filter((c) => c.frame > T.payoff).map((c) => c.frame);
const PR_AT = [4, 8, 12];
const COUNTS = cuesOf("count").filter((c) => c.frame > T.payoff);

/** Where the head of the line is, in months. */
const headAt = (f: number) => clamp((f - START) / PER, 0, KG.length - 1);

function pointOn(m: number) {
  const i = Math.min(SEGS.length - 1, Math.floor(m));
  const t = m - i;
  const [a, b, c, d] = SEGS[i]!;
  const u = 1 - t;
  const w = [u * u * u, 3 * u * u * t, 3 * u * t * t, t * t * t] as const;
  return { x: w[0] * a.x + w[1] * b.x + w[2] * c.x + w[3] * d.x, y: w[0] * a.y + w[1] * b.y + w[2] * c.y + w[3] * d.y };
}

export function PayoffAct({ frame: f }: { frame: number }) {
  const m = headAt(f);
  const head = pointOn(m);
  const out = prog(f, 1500, 1556, EASE.in);
  const drift = 1 + 0.04 * prog(f, T.payoff, 1540, EASE.standard);
  // The gain is the best month so far, so it counts with the line and never goes down on the deload.
  const gain = COUNTS.filter((c) => f >= c.frame).length;
  const lastCount = COUNTS.filter((c) => f >= c.frame).pop()?.frame ?? -99;
  const bump = 1 + 0.05 * (1 - prog(f, lastCount, lastCount + 5));
  const done = sp(f, START + PER * (KG.length - 1) + 2, "pop");
  return (
    <AbsoluteFill style={{ fontFamily: FONT, background: `radial-gradient(80% 70% at 60% 80%, #12170a 0%, ${COLOR.deep} 75%)` }}>
      <AbsoluteFill style={{ transform: `scale(${drift * (1 - 0.08 * out)})`, filter: out > 0.01 ? `blur(${10 * out}px)` : undefined, opacity: 1 - out }}>
        <svg width={1920} height={1080} style={{ position: "absolute", inset: 0 }}>
          <defs>
            <linearGradient id="area" x1="0" y1={Y_HI} x2="0" y2={Y_LO} gradientUnits="userSpaceOnUse">
              <stop offset="0" stopColor={COLOR.lime} stopOpacity={0.3} />
              <stop offset="1" stopColor={COLOR.lime} stopOpacity={0} />
            </linearGradient>
            <clipPath id="upto">
              <rect x={0} y={0} width={head.x} height={1080} />
            </clipPath>
            <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
              <feGaussianBlur stdDeviation="9" />
            </filter>
          </defs>
          {[0, 0.5, 1].map((g) => (
            <line key={g} x1={X0 - 40} x2={X1 + 40} y1={mix(Y_LO, Y_HI, g)} y2={mix(Y_LO, Y_HI, g)} stroke={COLOR.hair} strokeWidth={1.5} opacity={prog(f, T.payoff, T.payoff + 20)} />
          ))}
          <line x1={X0 - 40} x2={X1 + 40} y1={PTS[0]!.y} y2={PTS[0]!.y} stroke={COLOR.faint} strokeWidth={2} strokeDasharray="6 10" opacity={0.7 * prog(f, T.payoff, T.payoff + 20)} />
          <g clipPath="url(#upto)">
            <path d={`${PATH} L ${X1} ${Y_LO + 60} L ${X0} ${Y_LO + 60} Z`} fill="url(#area)" />
            <path d={PATH} fill="none" stroke={COLOR.lime} strokeWidth={14} opacity={0.45} filter="url(#glow)" />
            <path d={PATH} fill="none" stroke={COLOR.lime} strokeWidth={6} strokeLinecap="round" strokeLinejoin="round" />
          </g>
          {PR_AT.map((i, k) => {
            const s = sp(f, PR_CUES[k]!, "pop");
            const ring = prog(f, PR_CUES[k]!, PR_CUES[k]! + 30, EASE.out);
            const p = PTS[i]!;
            return (
              <g key={i}>
                {f >= PR_CUES[k]! && ring < 1 && <circle cx={p.x} cy={p.y} r={14 + 46 * ring} fill="none" stroke={`rgba(156,134,232,${0.8 * (1 - ring)})`} strokeWidth={3} />}
                <circle cx={p.x} cy={p.y} r={14 * s} fill={COLOR.pr} stroke={COLOR.deep} strokeWidth={4} />
              </g>
            );
          })}
          {f >= START && m < KG.length - 1 && (
            <>
              <circle cx={head.x} cy={head.y} r={30} fill={lime(0.35)} filter="url(#glow)" />
              <circle cx={head.x} cy={head.y} r={9} fill="#ffffff" />
            </>
          )}
        </svg>
        {MONTHS.map((l, i) => (
          <div key={i} style={{ position: "absolute", left: PTS[i]!.x, top: Y_LO + 40, transform: "translateX(-50%)", fontFamily: MONO, fontSize: 20, color: f >= START + i * PER ? COLOR.soft : COLOR.faint, opacity: prog(f, T.payoff + i * 1.5, T.payoff + 10 + i * 1.5) }}>{l}</div>
        ))}
        <div style={{ position: "absolute", left: PTS[0]!.x - 10, top: PTS[0]!.y + 18, fontSize: 26, color: COLOR.soft, fontWeight: 600, opacity: prog(f, T.payoff + 4, T.payoff + 20) }}>105 kg</div>
        {done > 0.001 && (
          <div style={{ position: "absolute", left: PTS[KG.length - 1]!.x, top: PTS[KG.length - 1]!.y - 30, transform: `translate(-50%, -100%) scale(${done})`, transformOrigin: "50% 100%", padding: "12px 24px", borderRadius: 999, background: COLOR.lime, color: COLOR.limeInk, fontSize: 32, fontWeight: 700, boxShadow: `0 0 40px ${lime(0.5)}`, whiteSpace: "nowrap" }}>140 kg</div>
        )}
        <div style={{ position: "absolute", left: 96, top: 92 }}>
          <div style={{ fontSize: 210, fontWeight: 700, letterSpacing: "-0.055em", lineHeight: 1, color: COLOR.lime, transform: `scale(${bump * (1.25 - 0.25 * sp(f, T.payoff, "pop"))})`, transformOrigin: "0% 100%", opacity: prog(f, T.payoff, T.payoff + 4), filter: f < T.payoff + 8 ? `blur(${(1 - (f - T.payoff) / 8) * 8}px)` : undefined, fontVariantNumeric: "tabular-nums" }}>
              +{gain} <span style={{ fontSize: 120, letterSpacing: "-0.03em" }}>kg</span>
          </div>
          <div style={{ marginTop: 16 }}>
            <Words lines={["on the bench. In one year."]} frame={f} start={T.payoff + 30} size={52} weight={600} color={COLOR.soft} />
          </div>
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
}
