import { ThreeCanvas } from "@remotion/three";
import { ArrowRight, Check, FileText, Send } from "lucide-react";
import { useMemo } from "react";
import { AbsoluteFill } from "remotion";
import * as THREE from "three";
import { ENERGY_CLASS_COLORS } from "@/geometry/energy";
import type { EnergyClass } from "@/geometry/energy";
import { ENERGY_CLASS_INK } from "@/lib/energyClassInk";
import type { Cam } from "./camera";
import { MacCursor, RemoteCursor } from "./Cursor";
import type { CursorTrack } from "./Cursor";
import { Glass, Words } from "./kit";
import { COLOR, EASE, FONT, MONO, T, clamp, cueAt, cuesOf, enter, exit, inOut, mix, prog, sp } from "./lib";
import { CENTRE, EAVE, STOREY_H, WINDOWS, toWorld } from "./plan";
import { BOO_REST, Boo, Rig } from "./world";

const GRAB = cueAt("grab");
const TOGGLE = cueAt("toggle");
const MESSAGES = cuesOf("message").map((c) => c.frame);
const DOTS = cuesOf("dots").map((c) => c.frame);
const ROLLS = cuesOf("roll");

const easeCubic = (t: number) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
/** The insulation slider, 0 to 16 cm, as Hannes drags it (the same curve as its tick sounds). */
const insulation = (f: number) => 16 * easeCubic(clamp((f - GRAB) / 60));

function energyClass(f: number): EnergyClass {
  let c: EnergyClass = "G";
  for (const r of ROLLS) if (f >= r.frame) c = r.to as EnergyClass;
  return c;
}

const CLASSES: EnergyClass[] = ["A+", "A", "B", "C", "D", "E", "F", "G", "H"];

function mixColor(a: string, b: string, t: number) {
  return `#${new THREE.Color(a).lerp(new THREE.Color(b), t).getHexString()}`;
}

/** The hero camera: a slow orbit round the building, the building nudged left once the chat opens. */
function heroCam(f: number): Cam {
  const t = clamp((f - T.drop) / (T.payoff - T.drop));
  const az = mix(58, 30, EASE.standard(t));
  const el = mix(12, 17, t);
  const centre = toWorld(CENTRE.x, CENTRE.y, 9.5);
  const shift = mix(0, -1.2, prog(f, 950, 1010, EASE.inOut));
  const r = (az * Math.PI) / 180;
  const target: [number, number, number] = [centre[0] + Math.cos(r) * shift, centre[1], centre[2] - Math.sin(r) * shift];
  const dist = mix(76, 64, EASE.out(clamp((f - T.drop) / 120))) - 3 * t;
  return { target, dist, az, el, fov: 30 };
}

/** The order windows pop onto the model: street facade from the bottom left, then the side. */
const POP = WINDOWS.map((w, i) => {
  const street = w.facade === 0;
  const col = street ? i % 6 : (i - 30) % 5;
  const diag = w.storey + col;
  return street ? T.drop + 2 + diag * 3 : T.drop + 30 + diag * 3;
});

// Layout of the panels (screen pixels).
const LEFT = 96;
const SLIDER = { x: LEFT, y: 560, w: 440, track: { x: LEFT + 30, w: 380, y: 560 + 96 } };
const TOGGLE_CARD = { x: LEFT, y: 712, w: 440 };
const ENERGY = { x: LEFT, y: 360, w: 440 };
const CHAT = { x: 1380, y: 250, w: 450 };

const hannes: CursorTrack = {
  stops: [
    { f: 1062, x: 1560, y: 560, leave: 1066 },
    { f: GRAB - 4, x: SLIDER.track.x + 2, y: SLIDER.track.y + 4, arc: 0.12, leave: GRAB },
    { f: GRAB + 60, x: SLIDER.track.x + SLIDER.track.w, y: SLIDER.track.y + 4, ease: easeCubic, leave: GRAB + 76 },
    { f: 1230, x: 760, y: 520, arc: -0.1 },
  ],
  clicks: [GRAB],
  visible: [
    { f: 1062, on: true },
    { f: 1226, on: false },
  ],
};
const leon: CursorTrack = {
  stops: [
    { f: 1196, x: 1480, y: 900, leave: 1204 },
    { f: TOGGLE - 4, x: TOGGLE_CARD.x + TOGGLE_CARD.w - 66, y: TOGGLE_CARD.y + 52, arc: 0.1, leave: TOGGLE + 14 },
    { f: 1300, x: 900, y: 430, arc: 0.12 },
  ],
  clicks: [TOGGLE],
  visible: [
    { f: 1196, on: true },
    { f: 1306, on: false },
  ],
};

function Avatar({ initials, color, size = 44 }: { initials: string; color: string; size?: number }) {
  return (
    <div
      style={{
        width: size,
        height: size,
        borderRadius: 999,
        background: color,
        color: "white",
        fontSize: size * 0.38,
        fontWeight: 600,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        boxShadow: "0 0 0 3px rgba(255,255,255,.95), 0 6px 14px -4px rgba(13,33,55,.35)",
        flex: "none",
      }}
    >
      {initials}
    </div>
  );
}

function Badge({ value, size, roll = 1, from }: { value: EnergyClass; size: number; roll?: number; from?: EnergyClass }) {
  const bg = from && roll < 1 ? mixColor(ENERGY_CLASS_COLORS[from], ENERGY_CLASS_COLORS[value], roll) : ENERGY_CLASS_COLORS[value];
  return (
    <div
      style={{
        width: size,
        height: size,
        borderRadius: size * 0.22,
        background: bg,
        color: ENERGY_CLASS_INK[value],
        fontFamily: MONO,
        fontWeight: 700,
        fontSize: size * 0.56,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        boxShadow: `0 ${size * 0.12}px ${size * 0.3}px -${size * 0.08}px ${ENERGY_CLASS_COLORS[value]}aa`,
        overflow: "hidden",
        position: "relative",
      }}
    >
      {from && roll < 1 && (
        <span style={{ position: "absolute", color: ENERGY_CLASS_INK[from], transform: `translateY(${-roll * size * 0.75}px)`, opacity: 1 - roll, filter: `blur(${roll * 4}px)` }}>{from}</span>
      )}
      <span style={{ transform: `translateY(${(1 - roll) * size * 0.75}px)`, opacity: roll, filter: roll < 1 ? `blur(${(1 - roll) * 4}px)` : undefined }}>{value}</span>
    </div>
  );
}

/** Act III: the building with its windows, the team on it live, the payoff and the report. */
export function HeroAct({ frame }: { frame: number }) {
  const f = frame;
  const cam = heroCam(f);
  const plane = useMemo(() => new THREE.Plane(new THREE.Vector3(0, -1, 0), 0), []);
  const value = f >= GRAB ? insulation(f) : 0;
  const plaster = (EAVE * value) / 16;
  plane.constant = plaster;
  const glazing = prog(f, TOGGLE + 6, TOGGLE + 40, EASE.inOut);
  const sweep = mix(-0.2, 1.3, prog(f, TOGGLE + 6, TOGGLE + 46, EASE.inOut));
  const cls = energyClass(f);
  const rollIndex = ROLLS.findLastIndex((r) => f >= r.frame);
  const lastRoll = ROLLS[rollIndex];
  const before = (rollIndex > 0 ? ROLLS[rollIndex - 1]!.to : "G") as EnergyClass;
  const roll = lastRoll ? prog(f, lastRoll.frame, lastRoll.frame + 10, EASE.out) : 1;
  const payoff = prog(f, T.payoff - 10, T.payoff + 20, EASE.inOut);
  const flash = 1 - prog(f, T.drop, T.drop + 18, EASE.out);
  const panelsOut = (start: number) => exit(f, T.payoff - 16 + start);
  const report = f >= T.report;

  const boo = {
    ...BOO_REST,
    window: (i: number) => sp(f, POP[i]!, "pop"),
    plaster,
    glazing,
    sweep,
  };

  return (
    <AbsoluteFill style={{ fontFamily: FONT }}>
      <AbsoluteFill style={{ background: "radial-gradient(120% 95% at 50% 38%, #ffffff 0%, #eef1f5 60%, #e3e8ee 100%)" }} />
      {/* The building, softened behind the payoff like a lens focusing past it. */}
      <AbsoluteFill style={{ filter: payoff > 0.01 ? `blur(${payoff * 16}px) saturate(${1 - 0.3 * payoff})` : undefined, transform: `scale(${1 + 0.06 * payoff})`, opacity: 1 - 0.35 * payoff }}>
        <ThreeCanvas width={1920} height={1080} gl={{ antialias: true, alpha: true }} shadows onCreated={(s) => (s.gl.localClippingEnabled = true)}>
          <Rig cam={cam} />
          <hemisphereLight args={["#ffffff", "#cbd3dc", 1.25]} />
          <directionalLight
            position={[-30, 46, 40]}
            intensity={2.5}
            color="#fff2e2"
            castShadow
            shadow-mapSize={[2048, 2048]}
            shadow-bias={-0.0004}
            shadow-normalBias={0.04}
            shadow-camera-left={-30}
            shadow-camera-right={30}
            shadow-camera-top={30}
            shadow-camera-bottom={-30}
            shadow-camera-far={140}
            shadow-radius={6}
          />
          <directionalLight position={[40, 20, -20]} intensity={0.6} color="#dce6ff" />
          <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0, 0]} receiveShadow>
            <circleGeometry args={[60, 64]} />
            <shadowMaterial opacity={0.16} />
          </mesh>
          <Boo s={boo} plasterPlane={plane} />
        </ThreeCanvas>
      </AbsoluteFill>
      {/* A soft contact shadow under the building. */}
      <AbsoluteFill style={{ pointerEvents: "none", background: "radial-gradient(22% 7% at 47% 86%, rgba(13,33,55,.12), transparent 70%)", opacity: 1 - payoff }} />

      {/* Copy. */}
      <div style={{ position: "absolute", left: LEFT, top: 96 }}>
        <Words lines={["Placed in *3D."]} frame={f} start={T.drop + 8} end={944} size={88} />
      </div>
      <div style={{ position: "absolute", left: LEFT, top: 96 }}>
        <Words lines={["Together.", "*Live."]} frame={f} start={968} end={T.payoff - 18} size={88} accent={COLOR.ok} />
      </div>

      {/* Who is here. */}
      {f >= 956 && (
        <div style={{ position: "absolute", left: 960, top: 44, transform: "translateX(-50%)" }}>
          <div style={inOut(f, 956, T.payoff - 18, { rise: -14 })}>
          <Glass radius={999} style={{ padding: "10px 22px 10px 12px" }}>
            <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
              <div style={{ display: "flex" }}>
                {[
                  { i: "AY", c: COLOR.you, f: cueAt("join", 0) },
                  { i: "LG", c: COLOR.leon, f: cueAt("join", 1) },
                  { i: "HB", c: COLOR.hannes, f: cueAt("join", 2) },
                ].map((a, k) => {
                  const t = sp(f, a.f, "pop");
                  return (
                    <div key={k} style={{ marginLeft: k ? -10 : 0, transform: `scale(${t})`, opacity: clamp(t * 2), width: 48 * clamp(t * 1.4) }}>
                      <Avatar initials={a.i} color={a.c} />
                    </div>
                  );
                })}
              </div>
              <div style={{ display: "flex", alignItems: "center", gap: 8, fontSize: 22, fontWeight: 600, color: COLOR.ink }}>
                <span style={{ width: 10, height: 10, borderRadius: 99, background: "#22c55e", boxShadow: `0 0 0 ${3 + 3 * Math.sin(f / 9)}px rgba(34,197,94,.2)` }} />
                {f >= cueAt("join", 2) ? 3 : f >= cueAt("join", 1) ? 2 : 1} editing
              </div>
            </div>
          </Glass>
          </div>
        </div>
      )}

      {/* The chat. */}
      {f >= 990 && (
        <div style={{ position: "absolute", left: CHAT.x, top: CHAT.y, width: CHAT.w, ...enter(f, 990), ...(f >= T.payoff - 16 ? panelsOut(4) : {}) }}>
          <Glass radius={30} style={{ padding: "22px 22px 8px" }}>
            <div style={{ fontSize: 20, fontWeight: 600, color: COLOR.muted, letterSpacing: "0.02em", marginBottom: 18 }}>Methfesselstraße 8</div>
            {[
              { who: "Leon", c: COLOR.leon, i: "LG", text: "Facade is in. Insulate the walls?" },
              { who: "Hannes", c: COLOR.hannes, i: "HB", text: "16 cm. Doing it now." },
              { who: "Leon", c: COLOR.leon, i: "LG", text: "Triple glazing too." },
            ].map((m, k) => {
              const typing = f >= DOTS[k]! && f < MESSAGES[k]!;
              const shown = f >= MESSAGES[k]!;
              if (!typing && !shown) return null;
              const t = shown ? sp(f, MESSAGES[k]!, "pop") : sp(f, DOTS[k]!, "settle");
              return (
                <div key={k} style={{ display: "flex", gap: 12, alignItems: "flex-end", marginBottom: 18, transform: `translateY(${(1 - t) * 18}px) scale(${0.9 + 0.1 * t})`, transformOrigin: "0 100%", opacity: clamp(t * 1.6) }}>
                  <Avatar initials={m.i} color={m.c} size={40} />
                  <div>
                    <div style={{ fontSize: 17, fontWeight: 600, color: m.c, marginBottom: 5, marginLeft: 4 }}>{m.who}</div>
                    <div style={{ background: "white", borderRadius: "22px 22px 22px 8px", padding: shown ? "13px 18px 14px" : "16px 18px", boxShadow: "0 8px 20px -10px rgba(13,33,55,.25), 0 0 0 1px rgba(13,33,55,.05)", fontSize: 25, color: COLOR.ink, lineHeight: 1.25, maxWidth: 330 }}>
                      {shown ? (
                        m.text
                      ) : (
                        <div style={{ display: "flex", gap: 6 }}>
                          {[0, 1, 2].map((d) => (
                            <span key={d} style={{ width: 10, height: 10, borderRadius: 99, background: "#9aa6b2", transform: `translateY(${-5 * Math.max(0, Math.sin((f - DOTS[k]!) / 4 - d * 0.9))}px)` }} />
                          ))}
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              );
            })}
          </Glass>
        </div>
      )}

      {/* Energy class, rolling as the building improves. */}
      {f >= 1040 && (
        <div style={{ position: "absolute", left: ENERGY.x, top: ENERGY.y, width: ENERGY.w, ...enter(f, 1040), ...(f >= T.payoff - 16 ? panelsOut(0) : {}) }}>
          <Glass radius={28} style={{ padding: "22px 26px" }}>
            <div style={{ display: "flex", alignItems: "center", gap: 22 }}>
              <Badge value={cls} size={92} roll={roll} from={lastRoll ? before : undefined} />
              <div style={{ flex: 1 }}>
                <div style={{ fontSize: 22, fontWeight: 600, color: COLOR.muted }}>Energy class</div>
                <div style={{ display: "flex", gap: 3, marginTop: 12 }}>
                  {CLASSES.map((c) => (
                    <div key={c} style={{ flex: 1, height: 14, borderRadius: 4, background: ENERGY_CLASS_COLORS[c], opacity: c === cls ? 1 : 0.4, transform: `scaleY(${c === cls ? 1.6 : 1})` }} />
                  ))}
                </div>
              </div>
            </div>
          </Glass>
        </div>
      )}

      {/* Hannes' insulation slider. */}
      {f >= 1050 && (
        <div style={{ position: "absolute", left: SLIDER.x, top: SLIDER.y, width: SLIDER.w, ...enter(f, 1050), ...(f >= T.payoff - 16 ? panelsOut(2) : {}) }}>
          <Glass radius={28} style={{ padding: "22px 30px 30px" }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline" }}>
              <span style={{ fontSize: 23, fontWeight: 600, color: COLOR.ink }}>Wall insulation</span>
              <span style={{ fontFamily: MONO, fontSize: 26, fontWeight: 600, color: COLOR.navy }}>{Math.round(value)} cm</span>
            </div>
            <div style={{ position: "relative", height: 30, marginTop: 20 }}>
              <div style={{ position: "absolute", left: 0, right: 0, top: 12, height: 6, borderRadius: 9, background: "rgba(13,33,55,.12)" }} />
              <div style={{ position: "absolute", left: 0, width: (SLIDER.track.w * value) / 16, top: 12, height: 6, borderRadius: 9, background: COLOR.navy }} />
              <div
                style={{
                  position: "absolute",
                  left: (SLIDER.track.w * value) / 16 - 15,
                  top: 0,
                  width: 30,
                  height: 30,
                  borderRadius: 99,
                  background: "white",
                  boxShadow: `0 0 0 ${f >= GRAB && f < GRAB + 66 ? 6 : 0}px rgba(231,111,81,.25), 0 4px 10px rgba(13,33,55,.3)`,
                }}
              />
            </div>
          </Glass>
        </div>
      )}

      {/* Leon's glazing switch. */}
      {f >= 1186 && (
        <div style={{ position: "absolute", left: TOGGLE_CARD.x, top: TOGGLE_CARD.y, width: TOGGLE_CARD.w, ...enter(f, 1186), ...(f >= T.payoff - 16 ? panelsOut(6) : {}) }}>
          <Glass radius={28} style={{ padding: "26px 30px" }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <span style={{ fontSize: 23, fontWeight: 600, color: COLOR.ink }}>Triple glazing</span>
              {(() => {
                const on = sp(f, TOGGLE, "pop");
                return (
                  <div style={{ width: 72, height: 42, borderRadius: 99, background: on > 0.5 ? COLOR.navy : "rgba(13,33,55,.16)", position: "relative", transition: "none" }}>
                    <div style={{ position: "absolute", top: 4, left: 4 + 30 * on, width: 34, height: 34, borderRadius: 99, background: "white", boxShadow: "0 3px 8px rgba(13,33,55,.3)" }} />
                  </div>
                );
              })()}
            </div>
          </Glass>
        </div>
      )}

      {/* Payoff: from G to B. */}
      {f >= T.payoff - 4 && (
        <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", ...(f >= T.report - 6 ? { transform: `translateY(${-300 * prog(f, T.report - 6, T.report + 20, EASE.inOut)}px) scale(${1 - 0.45 * prog(f, T.report - 6, T.report + 20, EASE.inOut)})`, opacity: 1 - prog(f, T.report + 8, T.report + 24) } : {}) }}>
          <Words lines={["From *G to *B."]} frame={f} start={T.payoff + 2} size={110} align="center" colors={{ G: ENERGY_CLASS_COLORS.G, "B.": COLOR.ok }} />
          <div style={{ display: "flex", alignItems: "center", gap: 40, marginTop: 44 }}>
            <div style={{ transform: `scale(${sp(f, T.payoff, "pop")})` }}>
              <Badge value="G" size={170} />
            </div>
            <svg width={120} height={60} viewBox="0 0 120 60">
              <path d="M8 30 H104 M84 10 L106 30 L84 50" fill="none" stroke={COLOR.ink} strokeWidth={7} strokeLinecap="round" strokeLinejoin="round" strokeDasharray="180" strokeDashoffset={180 * (1 - prog(f, T.payoff + 6, T.payoff + 24, EASE.out))} />
            </svg>
            <div style={{ transform: `scale(${sp(f, T.payoff + 14, "pop")})` }}>
              <Badge value="B" size={170} />
            </div>
          </div>
          <div style={{ marginTop: 40, fontFamily: MONO, fontSize: 52, fontWeight: 600, color: COLOR.ok, ...enter(f, T.payoff + 10) }}>
            −{Math.round(75 * prog(f, T.payoff + 12, T.payoff + 54, EASE.out))} % energy
          </div>
        </AbsoluteFill>
      )}

      {/* The report. */}
      {report && <Report frame={f} />}

      <RemoteCursor track={hannes} frame={f} color={COLOR.hannes} name="Hannes" />
      <RemoteCursor track={leon} frame={f} color={COLOR.leon} name="Leon" />
      {/* The drop arrives out of white. */}
      {flash > 0 && <AbsoluteFill style={{ background: "white", opacity: flash }} />}
    </AbsoluteFill>
  );
}

const DOC = { x: 960 - 300, y: 240, w: 600, h: 760 };
const SEND = { x: DOC.x + DOC.w - 190, y: DOC.y + DOC.h - 112 };
const you: CursorTrack = {
  stops: [
    { f: 1462, x: 1560, y: 1010 },
    { f: 1494, x: SEND.x + 120, y: SEND.y + 34, arc: -0.12 },
  ],
  clicks: [1500],
  shapes: [{ f: 1484, shape: "hand" }],
  visible: [
    { f: 1462, on: true },
    { f: 1536, on: false },
  ],
};

/** The iSFP report sliding up out of depth, sent with one click. */
function Report({ frame: f }: { frame: number }) {
  const t = sp(f, T.report, "settle");
  const out = prog(f, 1532, T.end, EASE.in);
  const sent = f >= 1504;
  const steps = [
    { year: "2027", what: "Facade, 16 cm", to: "D" as EnergyClass },
    { year: "2028", what: "Triple glazing", to: "C" as EnergyClass },
    { year: "2030", what: "Heat pump", to: "B" as EnergyClass },
  ];
  return (
    <AbsoluteFill style={{ opacity: 1 - out, transform: `scale(${1 - 0.08 * out})`, filter: out > 0 ? `blur(${out * 10}px)` : undefined }}>
      <div style={{ position: "absolute", left: LEFT, top: 330 }}>
        <Words lines={["Report.", "*Ready to send."]} frame={f} start={T.report + 10} size={84} />
      </div>
      <div style={{ position: "absolute", left: DOC.x + 520, top: DOC.y, perspective: 1600 }}>
        <div
          style={{
            position: "absolute",
            width: DOC.w,
            height: DOC.h,
            transform: `translateY(${(1 - t) * 700}px) rotateX(${(1 - t) * 28}deg) rotate(${(1 - t) * -4}deg)`,
            transformOrigin: "50% 100%",
          }}
        >
          {/* The second page, just behind. */}
          <div style={{ position: "absolute", inset: 0, transform: "translate(22px, -18px) rotate(2.5deg)", background: "#f6f7f9", borderRadius: 14, boxShadow: "0 30px 60px -20px rgba(13,33,55,.25)" }} />
          <div style={{ position: "absolute", inset: 0, background: "white", borderRadius: 14, boxShadow: "0 50px 100px -30px rgba(13,33,55,.45), 0 0 0 1px rgba(13,33,55,.05)", padding: "40px 44px", overflow: "hidden" }}>
            <div style={{ display: "flex", alignItems: "center", gap: 10, color: COLOR.navy, fontSize: 18, fontWeight: 600 }}>
              <FileText size={22} strokeWidth={2.2} /> Renovation roadmap (iSFP)
            </div>
            <div style={{ fontSize: 36, fontWeight: 600, color: COLOR.ink, marginTop: 14, letterSpacing: "-0.02em" }}>Methfesselstraße 8</div>
            <div style={{ fontSize: 19, color: COLOR.muted, marginTop: 4 }}>10965 Berlin · 5 storeys · 945 m²</div>
            <div style={{ display: "flex", alignItems: "center", gap: 14, marginTop: 30 }}>
              <Badge value="G" size={56} />
              {steps.map((s, i) => (
                <div key={i} style={{ display: "flex", alignItems: "center", gap: 14, ...enter(f, T.report + 20 + i * 6, { rise: 10 }) }}>
                  <ArrowRight size={22} color={COLOR.muted} />
                  <Badge value={s.to} size={56} />
                </div>
              ))}
            </div>
            <div style={{ marginTop: 30, display: "flex", flexDirection: "column", gap: 14 }}>
              {steps.map((s, i) => (
                <div key={i} style={{ display: "flex", alignItems: "center", gap: 16, padding: "14px 16px", borderRadius: 14, background: "#f4f6f9", ...enter(f, T.report + 26 + i * 6, { rise: 10 }) }}>
                  <div style={{ width: 8, alignSelf: "stretch", borderRadius: 9, background: ENERGY_CLASS_COLORS[s.to] }} />
                  <div style={{ fontFamily: MONO, fontSize: 19, color: COLOR.muted, width: 52 }}>{s.year}</div>
                  <div style={{ fontSize: 22, fontWeight: 600, color: COLOR.ink, flex: 1 }}>{s.what}</div>
                  <Badge value={s.to} size={36} />
                </div>
              ))}
            </div>
            <div style={{ marginTop: 26, display: "flex", flexDirection: "column", gap: 10 }}>
              {[0.92, 0.78, 0.86, 0.6].map((w, i) => (
                <div key={i} style={{ height: 10, borderRadius: 6, background: "#e9edf2", width: `${w * 100}%` }} />
              ))}
            </div>
            {/* Send. */}
            <div
              style={{
                position: "absolute",
                left: SEND.x - DOC.x - 520 + 520,
                top: SEND.y - DOC.y,
                height: 60,
                padding: "0 26px",
                borderRadius: 999,
                display: "flex",
                alignItems: "center",
                gap: 10,
                background: sent ? COLOR.ok : COLOR.navy,
                color: "white",
                fontSize: 22,
                fontWeight: 600,
                transform: `scale(${f >= 1500 && f < 1508 ? 0.95 : 1})`,
                boxShadow: "0 12px 24px -10px rgba(2,78,123,.6)",
              }}
            >
              {sent ? <Check size={24} strokeWidth={2.6} /> : <Send size={22} strokeWidth={2.2} />}
              {sent ? "Sent" : "Send PDF"}
            </div>
          </div>
        </div>
      </div>
      <MacCursor track={{ ...you, stops: you.stops.map((s) => ({ ...s, x: s.x + 520 })) }} frame={f} />
    </AbsoluteFill>
  );
}

export const HERO_STOREY = STOREY_H;
