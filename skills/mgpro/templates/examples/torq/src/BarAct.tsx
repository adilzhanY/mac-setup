import { ThreeCanvas } from "@remotion/three";
import { AbsoluteFill } from "remotion";
import type { Cam } from "./camera";
import { Words } from "./kit";
import { COLOR, EASE, FONT, T, clamp, cuesOf, logMix, mix, prog, sp } from "./lib";
import { Rig, Studio } from "./three";

/** Real barbell sizes, in metres. The bar runs along x. */
const SHAFT = 0.655;
const PLATE_R = 0.225;
const PLATE_H = 0.055;
const FIRST = 0.685 + PLATE_H / 2 + 0.002;
const plateX = (i: number) => FIRST + i * (PLATE_H + 0.002);
const OUTER_FACE = plateX(2) + PLATE_H / 2;
const RING_R = 0.19;

const SLAMS = cuesOf("slam").map((c) => c.frame);
const COLLAR = cuesOf("collar")[0]!.frame;
const KG = [60, 100, 140];

const STEEL = { color: "#c9ced3", metalness: 1, roughness: 0.22 };

/** How far a plate still has to travel before it hits the stack (metres), then a small recoil. */
function plateOffset(f: number, contact: number) {
  const lead = 10;
  if (f < contact - lead) return 99;
  if (f < contact) {
    const t = (f - (contact - lead)) / lead;
    return 1.7 * (1 - t * t);
  }
  const k = f - contact;
  return 0.012 * Math.exp(-k / 4) * Math.abs(Math.sin(k * 0.7));
}

function shakeAt(f: number) {
  let x = 0;
  let y = 0;
  for (const c of [...SLAMS, COLLAR]) {
    if (f < c) continue;
    const k = f - c;
    const amp = (c === COLLAR ? 4 : 16) * Math.exp(-k / 5.5);
    x += amp * Math.sin(k * 1.9 + c);
    y += amp * 0.8 * Math.cos(k * 2.3 + c);
  }
  return [x, y] as [number, number];
}

/** The camera: a slow push and orbit, then a rush into the outer plate's lime ring. */
export function barCam(f: number): Cam {
  const a = prog(f, 0, 200, EASE.standard);
  const base: Cam = { target: [0.3, 0.02, 0], dist: logMix(3.2, 2.45, a), az: mix(22, 34, a), el: mix(9, 5, a), fov: 28 };
  if (f < 200) return base;
  const t = prog(f, 200, 240, EASE.in);
  const u = prog(f, 200, 240, EASE.inOut);
  return {
    target: [mix(0.3, OUTER_FACE, u), mix(0.02, 0, u), 0],
    dist: logMix(2.45, 0.5, t),
    az: mix(34, 90, u),
    el: mix(5, 0, u),
    fov: 28,
  };
}

function Plate({ x, side, ghost = 1 }: { x: number; side: 1 | -1; ghost?: number }) {
  const transparent = ghost < 1;
  return (
    <group position={[side * x, 0, 0]} rotation={[0, 0, Math.PI / 2]}>
      <mesh>
        <cylinderGeometry args={[PLATE_R, PLATE_R, PLATE_H, 96, 1]} />
        <meshStandardMaterial color="#121311" roughness={0.62} metalness={0.05} transparent={transparent} opacity={ghost} />
      </mesh>
      {/* A softened rim, so the edge catches a line of light. */}
      <mesh rotation={[Math.PI / 2, 0, 0]}>
        <torusGeometry args={[PLATE_R - 0.004, 0.006, 12, 96]} />
        <meshStandardMaterial color="#2a2d28" roughness={0.35} transparent={transparent} opacity={ghost} />
      </mesh>
      {[1, -1].map((s) => (
        <group key={s}>
          <mesh position={[0, (s * PLATE_H) / 2 + s * 0.0006, 0]} rotation={[Math.PI / 2, 0, 0]}>
            <torusGeometry args={[RING_R, 0.005, 10, 128]} />
            <meshStandardMaterial color={COLOR.lime} emissive={COLOR.lime} emissiveIntensity={0.85} roughness={0.4} transparent={transparent} opacity={ghost} />
          </mesh>
          <mesh position={[0, (s * PLATE_H) / 2 + s * 0.0004, 0]} rotation={[Math.PI / 2, 0, 0]}>
            <ringGeometry args={[0.07, 0.165, 96]} />
            <meshStandardMaterial color="#191a18" roughness={0.8} transparent={transparent} opacity={ghost} />
          </mesh>
        </group>
      ))}
      <mesh>
        <cylinderGeometry args={[0.058, 0.058, PLATE_H + 0.003, 64]} />
        <meshStandardMaterial {...STEEL} transparent={transparent} opacity={ghost} />
      </mesh>
    </group>
  );
}

function Bar({ f }: { f: number }) {
  const grow = prog(f, 6, 34, EASE.out);
  const glow = 1 - prog(f, 14, 60);
  return (
    <group scale={[Math.max(0.001, grow), 1, 1]}>
      <mesh rotation={[0, 0, Math.PI / 2]}>
        <cylinderGeometry args={[0.014, 0.014, SHAFT * 2, 32]} />
        <meshStandardMaterial color="#aeb3b8" metalness={1} roughness={0.42} emissive={COLOR.lime} emissiveIntensity={glow * 2} />
      </mesh>
      {[1, -1].map((s) => (
        <group key={s}>
          <mesh position={[s * 0.67, 0, 0]} rotation={[0, 0, Math.PI / 2]}>
            <cylinderGeometry args={[0.04, 0.04, 0.03, 48]} />
            <meshStandardMaterial {...STEEL} />
          </mesh>
          <mesh position={[s * (0.685 + 0.2075), 0, 0]} rotation={[0, 0, Math.PI / 2]}>
            <cylinderGeometry args={[0.025, 0.025, 0.415, 48]} />
            <meshStandardMaterial color="#d7dbdf" metalness={1} roughness={0.12} emissive={COLOR.lime} emissiveIntensity={glow * 2} />
          </mesh>
        </group>
      ))}
    </group>
  );
}

/** Collars: torq lime, they clamp in on the beat after the last plate. */
function Collars({ f }: { f: number }) {
  if (f < COLLAR - 8) return null;
  const t = prog(f, COLLAR - 8, COLLAR, (x) => x * x);
  const x = OUTER_FACE + 0.016 + 0.5 * (1 - t);
  return (
    <>
      {[1, -1].map((s) => (
        <mesh key={s} position={[s * x, 0, 0]} rotation={[0, 0, Math.PI / 2]}>
          <cylinderGeometry args={[0.042, 0.042, 0.03, 48]} />
          <meshStandardMaterial color={COLOR.lime} emissive={COLOR.lime} emissiveIntensity={0.25} roughness={0.35} metalness={0.2} />
        </mesh>
      ))}
    </>
  );
}

function Stack({ f }: { f: number }) {
  return (
    <>
      {SLAMS.map((c, i) => {
        if (f < c - 10) return null;
        const off = plateOffset(f, c);
        const moving = f < c;
        return [1, -1].map((s) => (
          <group key={`${i}${s}`}>
            <Plate x={plateX(i) + off} side={s as 1 | -1} />
            {/* A shutter smear behind a plate in flight. */}
            {moving &&
              [1, 2, 3].map((g) => <Plate key={g} x={plateX(i) + Math.min(3, plateOffset(f - g * 0.45, c))} side={s as 1 | -1} ghost={[0.28, 0.13, 0.06][g - 1]} />)}
          </group>
        ));
      })}
    </>
  );
}

/** The weight, rolling like a slot each time a pair lands. */
function Counter({ f }: { f: number }) {
  if (f < SLAMS[0]!) return null;
  let i = 0;
  for (let k = 0; k < SLAMS.length; k++) if (f >= SLAMS[k]!) i = k;
  const t = prog(f, SLAMS[i]!, SLAMS[i]! + 12, EASE.out);
  const out = 1 - prog(f, 192, 206, EASE.in);
  const bump = 1 + 0.06 * (1 - prog(f, SLAMS[i]!, SLAMS[i]! + 8));
  const digits = (n: number, y: number, o: number, b: number) => (
    <div style={{ position: "absolute", inset: 0, display: "flex", justifyContent: "center", transform: `translateY(${y}px)`, opacity: o, filter: b > 0.1 ? `blur(${b}px)` : undefined }}>
      {n}
    </div>
  );
  return (
    <div style={{ position: "absolute", top: 70, width: "100%", display: "flex", justifyContent: "center", alignItems: "baseline", gap: 18, fontFamily: FONT, color: COLOR.ink, opacity: out }}>
      <div style={{ position: "relative", width: 420, height: 250, overflow: "hidden", fontSize: 196, fontWeight: 700, letterSpacing: "-0.05em", lineHeight: "250px", transform: `scale(${bump})`, fontVariantNumeric: "tabular-nums" }}>
        {i > 0 && digits(KG[i - 1]!, -t * 150, 1 - t, t * 10)}
        {digits(KG[i]!, (1 - t) * 150, i === 0 ? clamp(t * 2) : t, (1 - t) * 10)}
      </div>
      <div style={{ fontSize: 46, fontWeight: 600, color: COLOR.lime, letterSpacing: "0.04em", marginLeft: -40, opacity: clamp((f - SLAMS[0]!) / 10) }}>KG</div>
    </div>
  );
}

/** Act I: the bar draws itself in lime, three pairs of plates slam on, and we rush into the ring. */
export function BarAct({ frame: f }: { frame: number }) {
  const cam = barCam(f);
  const shake = shakeAt(f);
  const pool = 0.5 + 0.5 * prog(f, 0, 60);
  return (
    <AbsoluteFill style={{ background: COLOR.deep }}>
      <AbsoluteFill style={{ background: `radial-gradient(60% 55% at 50% 56%, rgba(40,46,36,${0.9 * pool}) 0%, rgba(14,15,14,0.6) 45%, ${COLOR.deep} 100%)` }} />
      <ThreeCanvas width={1920} height={1080} gl={{ antialias: true, alpha: true }} camera={{ fov: 28, position: [0, 0, 4] }}>
        <Rig cam={cam} shake={shake} />
        <Studio intensity={0.55} />
        <ambientLight intensity={0.08} />
        <directionalLight position={[-2, 4, 3]} intensity={2.4} />
        <directionalLight position={[3, 1.5, -3]} intensity={3.2} color="#e9ffd0" />
        <pointLight position={[1.2, 0.6, 1.4]} intensity={2} color={COLOR.lime} distance={3} />
        <Bar f={f} />
        <Stack f={f} />
        <Collars f={f} />
      </ThreeCanvas>
      <Counter f={f} />
      <AbsoluteFill style={{ justifyContent: "flex-end", alignItems: "center", paddingBottom: 150 }}>
        <Words lines={["Every *kilo."]} frame={f} start={126} end={194} size={104} align="center" />
      </AbsoluteFill>
      {/* The plate face fills the frame on the way into Act II; keep the stage black around it. */}
      <AbsoluteFill style={{ background: COLOR.deep, opacity: f >= T.log ? 1 : 0 }} />
    </AbsoluteFill>
  );
}
