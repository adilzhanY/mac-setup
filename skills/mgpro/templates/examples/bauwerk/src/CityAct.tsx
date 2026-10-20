import { ThreeCanvas } from "@remotion/three";
import { MapPin, Sparkles } from "lucide-react";
import { AbsoluteFill } from "remotion";
import { cornerPin, project, threeCamera } from "./camera";
import type { Cam } from "./camera";
import { AiGlow, Glass, Words } from "./kit";
import { COLOR, EASE, FONT, MONO, T, clamp, cueAt, cuesOf, keys, logMix, mix, prog, sp } from "./lib";
import { CENTRE, EAVE, ROOF, ROOMS, centroid, toWorld } from "./plan";
import { PlanSheet, SHEET, SHEET_H, SHEET_W } from "./PlanSheet";
import { Search } from "./Search";
import { BOO_REST, Boo, City, Rig, useCityData } from "./world";

const HERE = toWorld(CENTRE.x, CENTRE.y, 0);
/** Top-down with the street at the bottom of the screen: the plan reads upright. */
const UPRIGHT = 67.25;

/** The camera of acts I and II, one continuous move. */
export function cityCam(f: number): Cam {
  const target: [number, number, number] = [...HERE];
  let dist: number;
  let az: number;
  let el: number;
  if (f < T.dive) {
    // The map behind the search, drifting towards the building.
    const t = f / T.dive;
    target[0] += mix(70, 12, t);
    target[2] += mix(40, 8, t);
    dist = mix(1500, 1320, t);
    az = mix(-14, -10, t);
    el = 89.9;
  } else if (f < T.rise) {
    // The dive: an exponential zoom that turns the map upright on the way down.
    const t = EASE.inOut(clamp((f - T.dive) / (T.rise - T.dive)));
    target[0] += mix(12, 0, t);
    target[2] += mix(8, 0, t);
    dist = logMix(1320, 170, t);
    az = mix(-10, UPRIGHT, t);
    el = mix(89.9, 64, EASE.in(clamp((f - T.dive - 24) / 36)));
  } else if (f < T.aiStart) {
    // The city rises: tilt into 3D and pull back to see the wave, then drift in.
    const t = EASE.out(clamp((f - T.rise) / 100));
    const d = EASE.standard(clamp((f - T.rise - 60) / 60));
    dist = mix(mix(170, 320, t), 230, d);
    az = mix(UPRIGHT, 22, t) - 12 * d;
    el = mix(64, 34, t) + 3 * d;
  } else if (f < T.extrude) {
    // Act II: up over the building, the plan upright beneath.
    const t = EASE.inOut(clamp((f - T.aiStart) / 36));
    dist = logMix(230, 48, t) - 4 * prog(f, 396, T.extrude, EASE.standard);
    az = mix(10, UPRIGHT, t);
    el = mix(37, 89.9, t);
  } else {
    // The plan becomes a model: tilt down, orbit.
    const t = EASE.out(clamp((f - T.extrude) / 30));
    dist = mix(44, 50, t);
    az = mix(UPRIGHT, UPRIGHT - 28, t);
    el = mix(89.9, 50, t);
  }
  return { target, dist, az, el, fov: 32 };
}

/** The building's moves over acts I and II. */
function booAt(f: number) {
  // The building itself rises first and a little slower than its neighbours (back out, 0.75 s).
  const x = clamp((f - T.rise) / 45);
  const k = x - 1;
  const rise = f < T.rise ? 0 : 1 + 2.3 * k * k * k + 1.3 * k * k;
  return {
    ...BOO_REST,
    tint: 1 - prog(f, T.rise + 6, T.rise + 40),
    roofDrop: 1 - sp(f, 262, "settle"),
    roofLift: prog(f, T.aiStart, T.aiStart + 26, EASE.in),
    rise: f < T.aiStart + 6 ? rise : rise * (1 - prog(f, T.aiStart + 6, 392, EASE.in)),
    groundModel: f >= T.extrude ? sp(f, T.extrude + 2, "settle") : 0,
    inner: f >= T.extrude ? sp(f, T.extrude + 8, "settle") : 0,
    rooms: prog(f, 560, 580),
  };
}

const ROOM_CUES = cuesOf("room");

/** Acts I and II: search, dive, the city rising, the AI reading the plan, the plan turned model. */
export function CityAct({ frame }: { frame: number }) {
  const f = frame;
  // The city must be in memory before the canvas draws its first frame.
  const data = useCityData();
  const cam = cityCam(f);
  const view = threeCamera(cam);
  const here = project(view, HERE);
  // Lights down for the AI: night grows out of the building.
  const blur = mix(9, 0, prog(f, T.dive - 4, T.dive + 26, EASE.out));
  const mapOpacity = mix(0.5, 1, prog(f, T.dive - 4, T.dive + 26));
  const cityGone = f > T.aiStart + 70;
  const fogNear = cam.el > 80 ? 1e5 : cam.dist * 1.15;
  const fogFar = cam.el > 80 ? 2e5 : cam.dist * 3.4;
  const maskR = mix(62, 160, prog(f, T.rise, T.rise + 60));

  // The plan sheet, corner-pinned onto the ground.
  const corners = [
    [SHEET.x0, SHEET.y1],
    [SHEET.x1, SHEET.y1],
    [SHEET.x1, SHEET.y0],
    [SHEET.x0, SHEET.y0],
  ].map(([x, y]) => project(view, toWorld(x!, y!, 0.05)));
  const pin = cornerPin(
    [
      [0, 0],
      [SHEET_W, 0],
      [SHEET_W, SHEET_H],
      [0, SHEET_H],
    ],
    corners,
  );
  const ai = prog(f, 404, 428) * (1 - prog(f, 566, 584));

  // The pin rides on the roof as the building rises.
  const top = project(view, toWorld(CENTRE.x, CENTRE.y, (EAVE + ROOF.rise) * booAt(f).rise + 3));
  const pinIn = f >= 210 ? 1 : 0;
  const drop = sp(f, 210, "pop");
  const pinOut = prog(f, 300, 326, EASE.in);

  return (
    <AbsoluteFill style={{ fontFamily: FONT }}>
      <AbsoluteFill style={{ background: "radial-gradient(130% 100% at 50% 40%, #f7f9fb 0%, #eaeef2 100%)" }} />
      {f >= T.aiStart && <AbsoluteFill style={{ background: "radial-gradient(90% 90% at 50% 45%, #0e2236 0%, #07121e 70%)" }} />}
      <AbsoluteFill
        style={{
          filter: blur > 0.05 ? `blur(${blur}px)` : undefined,
          opacity: mapOpacity,
          WebkitMaskImage: `radial-gradient(${maskR}% ${maskR * 1.15}% at 50% 50%, #000 55%, transparent 100%)`,
        }}
      >
        {data && <ThreeCanvas
          width={1920}
          height={1080}
          gl={{ antialias: true, alpha: true }}
          shadows
          camera={{ fov: 32, near: 1, far: 6000, position: [0, 1500, 0] }}
        >
          <Rig cam={cam} />
          {cam.el < 80 && f < T.aiStart + 70 && <fog attach="fog" args={["#f1f3f6", fogNear, fogFar]} />}
          <hemisphereLight args={["#ffffff", "#c9d2dc", 1.45]} />
          <directionalLight
            position={[-260, 420, 300]}
            intensity={2.3}
            color="#fff3e4"
            castShadow
            shadow-mapSize={[4096, 4096]}
            shadow-bias={-0.0004}
            shadow-normalBias={0.4}
            shadow-camera-left={-330}
            shadow-camera-right={330}
            shadow-camera-top={330}
            shadow-camera-bottom={-330}
            shadow-camera-near={10}
            shadow-camera-far={1400}
          />
          <directionalLight position={[300, 200, -200]} intensity={0.45} color="#dfe8ff" />
          {data && !cityGone && <City data={data} frame={f} night={T.aiStart} centre={[HERE[0], HERE[2]]} />}
          {f < 394 || f >= T.extrude ? <Boo s={booAt(f)} /> : null}
        </ThreeCanvas>}
      </AbsoluteFill>

      {/* The map pin, landing on the building with a ripple. */}
      {pinIn > 0 && pinOut < 1 && (
        <>
          <div
            style={{
              position: "absolute",
              left: here.x - 70 * prog(f, 210, 250, EASE.out) - 10,
              top: here.y - 70 * prog(f, 210, 250, EASE.out) * 0.62 - 10,
              width: 20 + 140 * prog(f, 210, 250, EASE.out),
              height: (20 + 140 * prog(f, 210, 250, EASE.out)) * 0.62,
              borderRadius: "50%",
              border: `3px solid ${COLOR.navy}`,
              opacity: 0.6 * (1 - prog(f, 214, 252)),
            }}
          />
          <div
            style={{
              position: "absolute",
              left: top.x - 30,
              top: top.y - 76 - (1 - drop) * 40,
              opacity: 1 - pinOut,
              transform: `scale(${0.9 + 0.1 * drop})`,
              transformOrigin: "50% 100%",
            }}
          >
            <svg width={60} height={78} viewBox="0 0 60 78" style={{ filter: "drop-shadow(0 10px 14px rgba(2,78,123,.4))" }}>
              <path d="M30 76 C30 76 4 46 4 28 A26 26 0 0 1 56 28 C56 46 30 76 30 76 Z" fill={COLOR.navy} stroke="white" strokeWidth={3} />
            </svg>
            <div style={{ position: "absolute", left: 15, top: 13, color: "white" }}>
              <MapPin size={30} strokeWidth={2.4} />
            </div>
          </div>
        </>
      )}

      {/* The old plan on the ground, with the AI glow around the sheet. */}
      {f >= 388 && f < T.facade && (
        <div style={{ position: "absolute", left: 0, top: 0, width: SHEET_W, height: SHEET_H, transformOrigin: "0 0", transform: pin }}>
          <div style={{ position: "absolute", inset: 0, borderRadius: 6 }}>
            <AiGlow frame={f} radius={6} strength={ai} rim={5} spread={48} />
          </div>
          <PlanSheet frame={f} />
        </div>
      )}

      {/* Room labels, standing up to the camera. */}
      {f >= 500 && f < T.facade &&
        ROOMS.map((r, i) => {
          if (r.area < 8) return null;
          const start = (ROOM_CUES[i]?.frame ?? 9999) + 4;
          const c = centroid(r.polygon);
          const p = project(view, toWorld(c.x, c.y, 0.05));
          const t = sp(f, start, "pop");
          const out = prog(f, 572, 586, EASE.in);
          const area = r.area * prog(f, start, start + 16, EASE.out);
          if (t <= 0.001) return null;
          return (
            <div
              key={i}
              style={{
                position: "absolute",
                left: p.x,
                top: p.y,
                transform: `translate(-50%, -50%) scale(${t * (1 - 0.2 * out)})`,
                opacity: clamp(t * 2) * (1 - out),
              }}
            >
              <Glass dark radius={16} style={{ padding: "8px 16px 9px", textAlign: "center" }}>
                <div style={{ color: "white", fontSize: 21, fontWeight: 600, letterSpacing: "-0.01em", whiteSpace: "nowrap" }}>{r.name}</div>
                <div style={{ color: "#d8c8ff", fontSize: 17, fontFamily: MONO, whiteSpace: "nowrap" }}>{area.toFixed(1)} m²</div>
              </Glass>
            </div>
          );
        })}

      {/* What the AI found, as a chip. */}
      {f >= cueAt("pop") && f < T.facade && (
        <div style={{ position: "absolute", right: 96, top: 110, transform: `scale(${sp(f, cueAt("pop"), "pop")})`, transformOrigin: "100% 0", opacity: 1 - prog(f, 584, 598) }}>
          <Glass dark radius={999} style={{ padding: "14px 26px 14px 18px" }}>
            <div style={{ display: "flex", alignItems: "center", gap: 14, color: "white", fontSize: 24, fontWeight: 600 }}>
              <span style={{ width: 38, height: 38, borderRadius: 999, background: "linear-gradient(135deg, #3d7bff, #a855f7 55%, #ff5c8a)", display: "inline-flex", alignItems: "center", justifyContent: "center" }}>
                <Sparkles size={20} strokeWidth={2.2} />
              </span>
              8 rooms · 13 walls · 11 doors
            </div>
          </Glass>
        </div>
      )}

      {/* Copy. */}
      <div style={{ position: "absolute", left: 96, top: 96 }}>
        <Words lines={["Any address."]} frame={f} start={T.rise + 6} end={346} size={92} />
        <Words lines={["In *3D. *Instantly."]} frame={f} start={T.rise + 58} end={348} size={92} />
      </div>
      <div style={{ position: "absolute", left: 96, top: 96 }}>
        <Words lines={["Reads old", "floor plans."]} frame={f} start={432} end={576} size={88} color="#ffffff" />
      </div>

      <Search frame={f} />
      {/* The plan turned model gets a lens flare of light at its walls' tops. */}
      <AbsoluteFill style={{ pointerEvents: "none", background: `radial-gradient(40% 40% at ${here.x}px ${here.y}px, rgba(168,85,247,${0.18 * keys(f, [T.extrude, T.extrude + 14, T.facade], [0, 1, 0.4])}), transparent 70%)` }} />
    </AbsoluteFill>
  );
}
