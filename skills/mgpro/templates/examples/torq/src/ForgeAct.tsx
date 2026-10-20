import { ThreeCanvas } from "@remotion/three";
import { AbsoluteFill } from "remotion";
import { project, pxPerMetre, threeCamera } from "./camera";
import { YOU_BADGE } from "./FriendsAct";
import type { Cam } from "./camera";
import { Words } from "./kit";
import { COLOR, EASE, FONT, T, TIERS, clamp, cuesOf, enter, exit, lime, logMix, mix, prog, sp } from "./lib";
import { Medal } from "./Medal";
import type { MedalLook } from "./Medal";
import { Rig, Studio } from "./three";

const TIER_CUES = cuesOf("tier").map((c) => c.frame);
/** Six upgrades, Iron to Diamond, then the seventh hit spins it up for the drop. */
const UPGRADES = TIER_CUES.slice(0, 6);
const SPIN_UP = TIER_CUES[6]!;


function tierAt(f: number) {
  if (f >= T.drop) return 7;
  return UPGRADES.filter((c) => f >= c).length;
}

function forgeCam(f: number): Cam {
  if (f < T.drop) {
    const a = prog(f, T.forge, T.gap, EASE.standard);
    return { target: [0, 0, 0], dist: logMix(8.4, 6.6, a), az: mix(-16, 10, a), el: mix(9, 2, a), fov: 30 };
  }
  const a = prog(f, T.drop, T.friends, EASE.out);
  return { target: [-1.35, 0.05, 0], dist: logMix(6.8, 7.5, a), az: mix(-5, 4, a), el: mix(1, 4, a), fov: 30 };
}

function medalRotation(f: number): [number, number, number] {
  if (f >= T.drop) {
    const settle = sp(f, T.drop, "camera");
    return [0.04 * Math.sin((f - T.drop) / 40), mix(-0.9, 0, settle) + 0.08 * Math.sin((f - T.drop) / 34), 0];
  }
  let y = -0.4 + 0.25 * prog(f, T.forge, T.gap);
  for (const c of [T.forge - 4, ...UPGRADES]) y += 2 * Math.PI * prog(f, c, c + 26, EASE.out);
  // After the last upgrade the medal spins up like a flywheel.
  if (f > SPIN_UP) y += 0.0055 * Math.pow(f - SPIN_UP, 2);
  const drop = prog(f, T.forge - 4, T.forge + 30, EASE.out);
  return [mix(-0.5, 0.12, drop), y, mix(0.25, 0, drop)];
}

function lookAt(f: number): MedalLook {
  const ti = tierAt(f);
  const tier = TIERS[ti]!;
  const last = f >= T.drop ? T.drop : ([T.forge, ...UPGRADES].filter((c) => f >= c).pop() ?? T.forge);
  const flash = 1 - prog(f, last, last + 14, EASE.out);
  const heat = f > SPIN_UP && f < T.drop ? prog(f, SPIN_UP, T.gap, EASE.in) : 0;
  const steps = f >= T.drop ? mix(0.75, 1, prog(f, T.drop + 6, T.drop + 40, EASE.out)) : mix(ti / 8, (ti + 1) / 8, 1) * prog(f, last, last + 18, EASE.out) + (ti / 8) * (1 - prog(f, last, last + 18, EASE.out));
  return { base: tier.base, light: tier.light, dark: tier.dark, flash: Math.max(flash, heat), track: steps, trackColor: f >= T.drop ? COLOR.lime : tier.light };
}

/** The tier name under the medal, rolling like a slot at each upgrade. */
function TierName({ f, at }: { f: number; at: { x: number; y: number } }) {
  const ti = tierAt(f);
  const last = [T.forge, ...UPGRADES].filter((c) => f >= c).pop() ?? T.forge;
  const t = prog(f, last, last + 12, EASE.out);
  const out = 1 - prog(f, SPIN_UP + 10, SPIN_UP + 26, EASE.in);
  const line = (i: number, y: number, o: number, b: number) => (
    <div style={{ position: "absolute", inset: 0, textAlign: "center", color: TIERS[i]!.light, transform: `translateY(${y}px)`, opacity: o, filter: b > 0.1 ? `blur(${b}px)` : undefined }}>
      {TIERS[i]!.name.toUpperCase()}
    </div>
  );
  return (
    <div style={{ position: "absolute", left: at.x - 400, top: at.y, width: 800, height: 90, overflow: "hidden", fontSize: 64, fontWeight: 700, letterSpacing: "0.32em", paddingLeft: "0.32em", lineHeight: "90px", opacity: out * clamp((f - T.forge - 8) / 14) }}>
      {ti > 0 && line(ti - 1, -t * 80, 1 - t, t * 10)}
      {line(ti, ti > 0 ? (1 - t) * 80 : 0, ti > 0 ? t : 1, ti > 0 ? (1 - t) * 10 : 0)}
    </div>
  );
}

/** Eight rays, one per blade, turning slowly behind the Elite medal. */
function Rays({ f, at }: { f: number; at: { x: number; y: number } }) {
  const on = prog(f, T.drop, T.drop + 30, EASE.out);
  const spin = (f - T.drop) * 0.35;
  return (
    <svg width={1920} height={1080} style={{ position: "absolute", inset: 0, opacity: on }}>
      <defs>
        <radialGradient id="ray" cx={at.x} cy={at.y} r={760} gradientUnits="userSpaceOnUse">
          <stop offset="0.12" stopColor={COLOR.lime} stopOpacity={0.5} />
          <stop offset="1" stopColor={COLOR.lime} stopOpacity={0} />
        </radialGradient>
        <radialGradient id="pool" cx={at.x} cy={at.y} r={520} gradientUnits="userSpaceOnUse">
          <stop offset="0" stopColor={COLOR.lime} stopOpacity={0.26} />
          <stop offset="1" stopColor={COLOR.lime} stopOpacity={0} />
        </radialGradient>
      </defs>
      <circle cx={at.x} cy={at.y} r={520} fill="url(#pool)" />
      <g transform={`rotate(${spin} ${at.x} ${at.y})`}>
        {Array.from({ length: 8 }, (_, i) => (
          <path key={i} d={`M ${at.x} ${at.y} L ${at.x + 760} ${at.y - 34} L ${at.x + 760} ${at.y + 34} Z`} fill="url(#ray)" transform={`rotate(${i * 45 + 22.5} ${at.x} ${at.y})`} />
        ))}
      </g>
    </svg>
  );
}

/** Sparks thrown off the medal on the drop: fast out, slowing, fading. */
function Sparks({ f, at }: { f: number; at: { x: number; y: number } }) {
  const k = f - T.drop;
  if (k < 0 || k > 60) return null;
  return (
    <svg width={1920} height={1080} style={{ position: "absolute", inset: 0 }}>
      {Array.from({ length: 46 }, (_, i) => {
        const h = Math.sin(i * 91.7) * 43758.5;
        const r = h - Math.floor(h);
        const a = (i / 46) * Math.PI * 2 + r * 0.5;
        const speed = 380 + 520 * r;
        const d = speed * (1 - Math.exp(-k / 14));
        const d0 = speed * (1 - Math.exp(-Math.max(0, k - 2.5) / 14));
        const o = 1 - prog(k, 18 + 20 * r, 46 + 12 * r);
        return (
          <line
            key={i}
            x1={at.x + Math.cos(a) * (180 + d0)}
            y1={at.y + Math.sin(a) * (180 + d0)}
            x2={at.x + Math.cos(a) * (180 + d)}
            y2={at.y + Math.sin(a) * (180 + d)}
            stroke={i % 3 ? COLOR.lime : "#ffffff"}
            strokeWidth={2 + 3 * r}
            strokeLinecap="round"
            opacity={o}
          />
        );
      })}
    </svg>
  );
}

/** Act IV and the drop: the rank is forged through every metal, then lands as Elite. */
export function ForgeAct({ frame: f }: { frame: number }) {
  if (f >= T.gap && f < T.drop) return <AbsoluteFill style={{ background: "#000" }} />;
  const cam = forgeCam(f);
  const lens = threeCamera(cam);
  const at = project(lens, [0, 0, 0]);
  const look = lookAt(f);
  const bloom = f < T.drop ? prog(f, SPIN_UP, T.gap, EASE.standard) : 0;
  const flash = f >= T.drop ? 1 - prog(f, T.drop, T.drop + 20, EASE.out) : 0;
  const shake = f >= T.drop && f < T.drop + 24 ? 18 * Math.exp(-(f - T.drop) / 5) : 0;
  // The handoff: the medal shrinks into its badge on the friends board.
  const hand = prog(f, 938, T.friends, EASE.inOut);
  // The flat badge's frame is 88 percent of its box; the medal's frame is 2 units tall.
  const handScale = mix(1, (YOU_BADGE.size * 0.88) / (2 * pxPerMetre(lens, [0, 0, 0])), hand);
  const tx = mix(0, YOU_BADGE.x - at.x, hand);
  const ty = mix(0, YOU_BADGE.y - at.y, hand);
  const pts = Math.round(mix(0, 1284, prog(f, T.drop + 20, T.drop + 70, EASE.out)));
  return (
    <AbsoluteFill style={{ fontFamily: FONT, background: f >= T.drop ? `radial-gradient(70% 80% at 65% 50%, #141a0a 0%, ${COLOR.deep} 70%)` : `radial-gradient(60% 70% at 50% 50%, #161914 0%, ${COLOR.deep} 75%)` }}>
      <AbsoluteFill style={{ transform: `translate(${tx}px, ${ty}px) scale(${handScale})`, transformOrigin: `${at.x}px ${at.y}px`, opacity: 1 - prog(f, 956, T.friends) }}>
        {f >= T.drop && <Rays f={f} at={at} />}
        <AbsoluteFill style={{ background: `radial-gradient(circle at ${at.x}px ${at.y}px, ${lime(0.85 * bloom)} 0%, ${lime(0.3 * bloom)} ${8 + 14 * bloom}%, transparent ${22 + 30 * bloom}%)` }} />
        <ThreeCanvas width={1920} height={1080} gl={{ antialias: true, alpha: true }} camera={{ fov: 30, position: [0, 0, 8] }}>
          <Rig cam={cam} shake={[shake * Math.sin(f * 2.1), shake * Math.cos(f * 2.7)]} />
          <Studio intensity={0.9} />
          <ambientLight intensity={0.1} />
          <directionalLight position={[-3, 4, 5]} intensity={2.6} />
          <directionalLight position={[4, 1, -2]} intensity={4} color={look.light} />
          <directionalLight position={[-4, -1, -2]} intensity={3} color={look.light} />
          <pointLight position={[0, 0, 2.2]} intensity={1.5 + 6 * bloom} color={look.light} distance={6} />
          <Medal look={look} rotation={medalRotation(f)} />
        </ThreeCanvas>
        {f >= T.drop && <Sparks f={f} at={at} />}
      </AbsoluteFill>
      {f < T.drop && <TierName f={f} at={{ x: at.x, y: at.y + 380 }} />}
      {f >= T.drop && (
        <>
          <div style={{ position: "absolute", left: 120, top: 330 }}>
            <Words lines={["Earn", "your *rank."]} frame={f} start={T.drop + 6} end={936} size={150} />
          </div>
          <div style={{ position: "absolute", left: at.x - 300, top: at.y + 370, width: 600, display: "flex", justifyContent: "center", alignItems: "center", gap: 20, ...(f >= 934 ? exit(f, 934) : enter(f, T.drop + 22, { rise: 20 })) }}>
            <div style={{ padding: "12px 28px 12px 32px", borderRadius: 999, background: lime(0.14), color: COLOR.lime, fontSize: 34, fontWeight: 700, letterSpacing: "0.24em", boxShadow: `inset 0 0 0 1.5px ${lime(0.45)}` }}>ELITE</div>
            <div style={{ fontSize: 48, fontWeight: 700, color: COLOR.ink, fontVariantNumeric: "tabular-nums", letterSpacing: "-0.02em" }}>
              {pts.toLocaleString("en-US")} <span style={{ color: COLOR.soft, fontWeight: 600, fontSize: 30 }}>pts</span>
            </div>
          </div>
        </>
      )}
      {/* The heat of the spin-up swallows the medal itself, on top of everything, just before the black. */}
      {bloom > 0.01 && <AbsoluteFill style={{ mixBlendMode: "screen", background: `radial-gradient(circle at ${at.x}px ${at.y}px, rgba(236,255,190,${bloom * bloom}) 0%, ${lime(0.6 * bloom * bloom)} ${10 + 25 * bloom}%, transparent ${30 + 45 * bloom}%)` }} />}
      <AbsoluteFill style={{ background: `rgba(236,255,190,${flash})`, pointerEvents: "none" }} />
    </AbsoluteFill>
  );
}
