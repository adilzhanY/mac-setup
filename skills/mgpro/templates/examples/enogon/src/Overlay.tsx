import type { CSSProperties, ReactNode } from "react";
import { C, CUBE, DISPLAY, LOGO, MONO, de } from "./brand";
import { project, threeCamera } from "./camera";
import type { Cam } from "./camera";
import { EASE, clamp, enter, exit, inOut, mix, prog, sp } from "./lib";
import { cubeRect } from "./cubeRect";
import { BUTTON, cardRect } from "./cursorTrack";
import { DOOR_AT, INNER_AT, OUTER_AT, ROOM_AT } from "./PlanLayer";
import { CENTER, COUNTS, FOOTPRINT, INNER_WALLS, OPENINGS, OUTER_WALLS } from "./plan";
import { F } from "./timeline";

const M = 96;

/** Kinetic words: each rises out of a blur (expo out, 24 frames), leaves upward faster. */
export function Word({ text, frame, start, end, size = 92, color = C.ink, weight = 600, font = DISPLAY }: { text: string; frame: number; start: number; end?: number; size?: number; color?: string; weight?: number; font?: string }) {
  const t = prog(frame, start, start + 24, EASE.out);
  const o = end === undefined ? 0 : prog(frame, end, end + 12, EASE.in);
  const blur = 14 * (1 - t) + 10 * o;
  if (t <= 0) return null;
  return (
    <span
      style={{
        display: "inline-block",
        fontFamily: font,
        fontSize: size,
        fontWeight: weight,
        letterSpacing: "-0.035em",
        lineHeight: 1.04,
        color,
        opacity: clamp(t * 1.4) * (1 - o),
        transform: `translateY(${(1 - t) * size * 0.5 - o * size * 0.32}px) scale(${0.94 + 0.06 * t})`,
        transformOrigin: "50% 100%",
        filter: blur > 0.1 ? `blur(${blur}px)` : undefined,
        marginRight: size * 0.24,
        whiteSpace: "nowrap",
      }}
    >
      {text}
    </span>
  );
}

function Title({ children, style }: { children: ReactNode; style?: CSSProperties }) {
  return <div style={{ position: "absolute", left: M, top: M - 6, display: "flex", flexDirection: "column", ...style }}>{children}</div>;
}

const row = (children: ReactNode) => <div style={{ display: "flex", alignItems: "baseline" }}>{children}</div>;

/** A box in the product's style: sharp corners, a black hairline, paper fill. */
const box = (extra: CSSProperties = {}): CSSProperties => ({ background: C.paper, border: `1.5px solid ${C.ink}`, ...extra });
const label = (extra: CSSProperties = {}): CSSProperties => ({ fontFamily: MONO, fontSize: 16, letterSpacing: "0.12em", textTransform: "uppercase", color: C.ink, ...extra });

function FileCard({ frame }: { frame: number }) {
  if (frame >= F.release) return null;
  const r = cardRect(frame);
  const e = enter(frame, 14);
  return (
    <div style={{ position: "absolute", left: r.x, top: r.y, width: r.w, ...e, filter: undefined, transform: `${e.transform} rotate(${r.tilt}deg)`, transformOrigin: "50% 20%" }}>
      <div style={{ ...box({ height: r.h, boxShadow: `0 ${6 + 18 * r.lift}px ${18 + 30 * r.lift}px rgba(0,0,0,${0.08 + 0.1 * r.lift})`, background: "#fbfaf6", overflow: "hidden" }) }}>
        <svg width={r.w} height={r.h} viewBox="0 0 200 150" preserveAspectRatio="xMidYMid meet">
          <g transform="translate(40 20) scale(9)" fill="none" stroke="#3b3b3b" strokeWidth={0.18}>
            <polygon points={FOOTPRINT.map((p) => `${p.x},${11 - p.y}`).join(" ")} fill="#e2e0d9" />
            {INNER_WALLS.map((w) => (
              <line key={w.id} x1={w.a.x} y1={11 - w.a.y} x2={w.b.x} y2={11 - w.b.y} />
            ))}
          </g>
        </svg>
      </div>
      <div style={{ ...label({ fontSize: 21, letterSpacing: "0.02em", textTransform: "none", marginTop: 12 }) }}>Grundriss_EG.pdf</div>
    </div>
  );
}

function DropZone({ frame, cam }: { frame: number; cam: Cam }) {
  const on = enter(frame, F.zoneIn);
  const out = prog(frame, F.release - 2, F.release + 10);
  if (out >= 1) return null;
  const hot = prog(frame, F.release - 40, F.release - 20);
  const c3 = threeCamera(cam);
  const a = project(c3, [-2.6 - CENTER.x, 0, CENTER.y - 12.1]);
  const b = project(c3, [15.0 - CENTER.x, 0, CENTER.y + 2.3]);
  return (
    <div
      style={{
        position: "absolute",
        left: a.x,
        top: a.y,
        width: b.x - a.x,
        height: b.y - a.y,
        border: `2px dashed ${hot > 0 ? C.ink : C.lineStrong}`,
        background: hot > 0 ? `rgba(254,230,216,${0.55 * hot})` : "transparent",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        gap: 18,
        opacity: on.opacity * (1 - out),
      }}
    >
      <svg width={84} height={84} viewBox="0 0 24 24" fill="none" stroke={C.ink} strokeWidth={1.4} strokeLinecap="round" strokeLinejoin="round">
        <path d="M12 15V3" />
        <path d="M7 8l5-5 5 5" />
        <path d="M4 15v4a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-4" />
      </svg>
      <div style={label({ fontSize: 30, letterSpacing: "0.1em" })}>Grundriss hochladen</div>
      <div style={label({ fontSize: 22, color: C.graphit, letterSpacing: "0.08em" })}>PDF · JPG · PNG</div>
    </div>
  );
}

function Counter({ name, value, frame, start }: { name: string; value: number; frame: number; start: number }) {
  const e = enter(frame, start);
  return (
    <div style={{ ...box({ width: 190, padding: "14px 18px 10px" }), ...e }}>
      <div style={label({ fontSize: 17, color: C.graphit })}>{name}</div>
      <div style={{ fontFamily: DISPLAY, fontWeight: 600, fontSize: 52, letterSpacing: "-0.02em", fontVariantNumeric: "tabular-nums", marginTop: 2 }}>{value}</div>
    </div>
  );
}

const countBy = (frame: number, ats: number[]) => ats.filter((a) => frame >= a + 2).length;

function Counters({ frame }: { frame: number }) {
  const out = exit(frame, F.title2Out);
  if (frame < F.traceStart || out.opacity <= 0) return null;
  const walls = countBy(frame, [...OUTER_AT, ...INNER_AT.map((a) => a + F.innerLen)]);
  const doors = countBy(frame, DOOR_AT.map((a) => a + 6));
  const windows = frame >= F.doorStart ? Math.min(OPENINGS.filter((o) => o.kind === "window").length, Math.max(0, Math.floor((frame - F.doorStart) / 2))) : 0;
  const rooms = countBy(frame, ROOM_AT.map((a) => a + 6));
  return (
    <div style={{ position: "absolute", left: M, bottom: M, display: "grid", gridTemplateColumns: "190px 190px", gap: 14, ...out }}>
      <Counter name="Wände" value={walls} frame={frame} start={F.traceStart} />
      <Counter name="Fenster" value={windows} frame={frame} start={F.traceStart + 4} />
      <Counter name="Türen" value={doors} frame={frame} start={F.doorStart - 6} />
      <Counter name="Räume" value={rooms} frame={frame} start={F.roomStart - 6} />
    </div>
  );
}

function StoreyStack({ frame }: { frame: number }) {
  const lands = [F.egRise + 30, F.land1, F.land2, F.land3];
  const names = ["EG", "1.OG", "2.OG", "DG"];
  const out = exit(frame, F.title4Out);
  if (frame < F.stack || out.opacity <= 0) return null;
  const active = lands.filter((l) => frame >= l).length - 1;
  return (
    <div style={{ position: "absolute", right: M, top: 300, display: "flex", flexDirection: "column-reverse", ...out }}>
      {names.map((n, i) => {
        const e = enter(frame, Math.max(F.stack + i * 4, lands[i]! - 30));
        const on = i === active;
        const done = i < active;
        return (
          <div
            key={n}
            style={{
              ...box({ width: 200, height: 76, marginTop: -1.5, background: on ? C.ink : done ? C.apricot100 : C.paper }),
              ...label({ fontSize: 26, color: on ? C.paper : C.ink, letterSpacing: "0.06em" }),
              display: "flex",
              alignItems: "center",
              paddingLeft: 18,
              justifyContent: "space-between",
              paddingRight: 16,
              ...e,
            }}
          >
            <span>{n}</span>
            {done && (
              <svg width={28} height={28} viewBox="0 0 24 24" fill="none" stroke={C.ink} strokeWidth={2.4} strokeLinecap="round" strokeLinejoin="round">
                <path d="M4 12.5l5 5L20 6.5" />
              </svg>
            )}
          </div>
        );
      })}
    </div>
  );
}

function PropertyCard({ frame }: { frame: number }) {
  const e = inOut(frame, F.card, F.title5Out);
  if (frame < F.card || e.opacity <= 0) return null;
  const typed = prog(frame, F.type, F.type + 22);
  const value = typed < 0.5 ? "0,36" : "0,48";
  const caret = frame >= F.field + 4 && frame < F.type + 40;
  const focus = frame >= F.field + 4;
  const rowStyle: CSSProperties = { display: "flex", justifyContent: "space-between", alignItems: "center", padding: "0 28px", height: 64 };
  const field = (v: string, active: boolean) => (
    <div style={{ ...box({ width: 160, height: 46, display: "flex", alignItems: "center", justifyContent: "flex-end", padding: "0 14px", borderWidth: active ? 2.5 : 1.5 }), fontFamily: MONO, fontSize: 20 }}>
      {v} m{active && caret && Math.floor(frame / 18) % 2 === 0 ? <span style={{ width: 2, height: 22, background: C.ink, marginLeft: 3 }} /> : <span style={{ width: 5 }} />}
    </div>
  );
  return (
    <div style={{ position: "absolute", right: M, top: 250, width: 470, ...box({ boxShadow: "12px 12px 0 rgba(0,0,0,0.06)" }), ...e }}>
      <div style={{ padding: "26px 28px 20px", borderBottom: `1.5px solid ${C.ink}` }}>
        <div style={label({ fontSize: 15 })}>Aussenwand · EG · Süd</div>
        <div style={{ fontFamily: DISPLAY, fontWeight: 700, fontSize: 56, letterSpacing: "-0.03em", marginTop: 6 }}>AW 008</div>
      </div>
      <div style={{ ...label({ fontSize: 14, color: C.graphit }), padding: "18px 28px 4px" }}>Geometrie</div>
      <div style={rowStyle}>
        <span style={{ fontFamily: DISPLAY, fontSize: 24 }}>Wandstärke</span>
        {field(value, focus)}
      </div>
      <div style={rowStyle}>
        <span style={{ fontFamily: DISPLAY, fontSize: 24 }}>Höhe</span>
        {field("2,87", false)}
      </div>
      <div style={{ ...rowStyle, paddingBottom: 12 }}>
        <span style={{ fontFamily: DISPLAY, fontSize: 24 }}>Länge</span>
        <span style={{ fontFamily: MONO, fontSize: 20, paddingRight: 14 }}>12,40 m</span>
      </div>
    </div>
  );
}


function ExportButton({ frame }: { frame: number }) {
  const e = inOut(frame, F.button, F.title6Out);
  if (frame < F.button || e.opacity <= 0) return null;
  const press = frame >= F.press ? 1 - 0.03 * Math.sin(Math.PI * clamp((frame - F.press) / 12)) : 1;
  const fill = prog(frame, F.press + 4, F.done - 4, EASE.standard);
  const done = sp(frame, F.done, "pop");
  const hover = frame >= F.press - 18;
  return (
    <div style={{ position: "absolute", left: BUTTON.x, top: BUTTON.y, ...e }}>
      <div
        style={{
          width: BUTTON.w,
          height: BUTTON.h,
          ...box({ borderWidth: 2.5, background: hover ? C.apricot400 : C.apricot300 }),
          position: "relative",
          overflow: "hidden",
          transform: `scale(${press})`,
          boxShadow: "10px 10px 0 rgba(0,0,0,0.08)",
        }}
      >
        <div style={{ position: "absolute", left: 0, top: 0, bottom: 0, width: `${fill * 100}%`, background: C.ink }} />
        <div style={{ position: "absolute", inset: 0, display: "flex", alignItems: "center", justifyContent: "center", gap: 20 }}>
          {[0, 1].map((k) => (
            <div
              key={k}
              style={{
                position: "absolute",
                inset: 0,
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                gap: 20,
                color: k === 0 ? C.ink : C.paper,
                clipPath: k === 0 ? `inset(0 0 0 ${fill * 100}%)` : `inset(0 ${100 - fill * 100}% 0 0)`,
              }}
            >
              {frame < F.done ? (
                <svg width={44} height={44} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round">
                  <path d="M12 3v12" />
                  <path d="M7 10l5 5 5-5" />
                  <path d="M4 17v2a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-2" />
                </svg>
              ) : (
                <svg width={44} height={44} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2.4} strokeLinecap="round" strokeLinejoin="round" style={{ transform: `scale(${0.6 + 0.4 * done})` }}>
                  <path d="M4 12.5l5 5L20 6.5" strokeDasharray={26} strokeDashoffset={26 * (1 - clamp(done * 1.3))} />
                </svg>
              )}
              <span style={{ fontFamily: DISPLAY, fontWeight: 600, fontSize: 52, letterSpacing: "-0.02em" }}>Export</span>
            </div>
          ))}
        </div>
      </div>
      <Summary frame={frame} />
    </div>
  );
}

function Summary({ frame }: { frame: number }) {
  const items: [string, number][] = [
    ["Geschosse", COUNTS.storeys],
    ["Wände", COUNTS.outerWalls + COUNTS.innerWalls],
    ["Öffnungen", COUNTS.openings],
    ["Räume", COUNTS.rooms],
  ];
  return (
    <div style={{ display: "flex", marginTop: 26 }}>
      {items.map(([n, v], i) => {
        const e = enter(frame, F.done + 6 + i * 4);
        return (
          <div key={n} style={{ ...box({ width: 130, padding: "10px 14px", marginLeft: i ? -1.5 : 0 }), ...e }}>
            <div style={label({ fontSize: 12, color: C.graphit, letterSpacing: "0.08em" })}>{n}</div>
            <div style={{ fontFamily: DISPLAY, fontWeight: 600, fontSize: 36, fontVariantNumeric: "tabular-nums" }}>{v}</div>
          </div>
        );
      })}
    </div>
  );
}

/** The end card: the cube (handed over from 3D), the wordmark, the line, the address. */
function EndCard({ frame }: { frame: number }) {
  if (frame < F.logo) return null;
  const swap = 1;
  const settle = prog(frame, F.logo + 4, F.logo + 60, EASE.standard);
  // From the 3D cube's size and place on screen to the lockup. The logo's own stroke sits
  // outside the cube's faces by half its width, so its viewBox is a little larger than the cube.
  const r = cubeRect();
  const h0 = r.h * (123 / 119);
  const h1 = 236;
  const hNow = mix(h0, h1, settle);
  const wNow = hNow * (107.06 / 123);
  const lockW = h1 * (107.06 / 123) + 34 + 590;
  const x1 = 960 - lockW / 2;
  const cx = mix(r.x + r.w / 2 - wNow / 2, x1, settle);
  const cy = mix(r.y + r.h / 2 - hNow / 2, 360 - h1 / 2 + 8, settle);
  const fade = 1 - prog(frame, F.fade, F.fade + 12);
  const reveal = prog(frame, F.word, F.word + 34, EASE.out);
  return (
    <div style={{ position: "absolute", inset: 0, opacity: fade }}>
      <div
        style={{
          position: "absolute",
          left: x1 + h1 * (107.06 / 123) + 34,
          top: 360 - 112,
          fontFamily: LOGO,
          fontWeight: 700,
          fontSize: 214,
          lineHeight: 1,
          letterSpacing: "-0.01em",
          color: C.ink,
          clipPath: `inset(0 ${100 - reveal * 100}% 0 0)`,
          transform: `translateX(${(1 - reveal) * -60}px)`,
        }}
      >
        Enogon
      </div>
      <svg style={{ position: "absolute", left: cx, top: cy, opacity: swap }} width={wNow} height={hNow} viewBox="-2 -2 107.06 123">
        <path d={CUBE.top} fill={C.apricot500} stroke={C.ink} strokeWidth={4.01} strokeLinejoin="round" />
        <path d={CUBE.right} fill={C.tuerkis500} stroke={C.ink} strokeWidth={4.01} strokeLinejoin="round" />
        <path d={CUBE.left} fill={C.paper} stroke={C.ink} strokeWidth={4.01} strokeLinejoin="round" />
      </svg>
      <div style={{ position: "absolute", top: 640, left: 0, right: 0, display: "flex", flexDirection: "column", alignItems: "center", gap: 26 }}>
        <div style={{ display: "flex" }}>
          <Word text="Grundriss rein." frame={frame} start={F.tag} size={58} />
          <Word text="CAD-Modell raus." frame={frame} start={F.tag + 6} size={58} color={C.apricot600} />
        </div>
        <div style={{ display: "flex", alignItems: "center", gap: 22, ...enter(frame, F.url) }}>
          <span style={{ ...box({ padding: "10px 20px" }), fontFamily: MONO, fontSize: 36, letterSpacing: "0.02em" }}>enogon.com</span>
          <span style={label({ fontSize: 24, color: C.graphit })}>Für Energieberater</span>
        </div>
      </div>
    </div>
  );
}

export function Overlay({ frame, cam }: { frame: number; cam: Cam }) {
  return (
    <>
      <DropZone frame={frame} cam={cam} />
      <FileCard frame={frame} />
      <Counters frame={frame} />
      <StoreyStack frame={frame} />
      <Dimensions frame={frame} cam={cam} />
      <PropertyCard frame={frame} />
      <ExportButton frame={frame} />

      {frame < F.title1Out + 14 && (
        <Title>{row(<><Word text="Grundriss" frame={frame} start={F.title1} end={F.title1Out} /><Word text="rein." frame={frame} start={F.title1 + 5} end={F.title1Out} color={C.apricot600} /></>)}</Title>
      )}
      {frame >= F.title2 && frame < F.title2Out + 14 && (
        <Title>
          {row(<><Word text="Die KI" frame={frame} start={F.title2} end={F.title2Out} size={64} /><Word text="erkennt" frame={frame} start={F.title2 + 4} end={F.title2Out} size={64} /></>)}
          {row(
            <>
              <Word text="Wände." frame={frame} start={F.traceStart + 10} end={F.title2Out} color={C.apricot600} />
              <Word text="Türen." frame={frame} start={DOOR_AT[0]!} end={F.title2Out} />
              <Word text="Räume." frame={frame} start={ROOM_AT[0]!} end={F.title2Out} color={C.tuerkis500} />
            </>,
          )}
        </Title>
      )}
      {frame >= F.title3 && frame < F.title3Out + 14 && (
        <Title>{row(<><Word text="Geschoss" frame={frame} start={F.title3} end={F.title3Out} /><Word text="für" frame={frame} start={F.title3 + 4} end={F.title3Out} /><Word text="Geschoss." frame={frame} start={F.title3 + 8} end={F.title3Out} color={C.apricot600} /></>)}</Title>
      )}
      {frame >= F.title4 && frame < F.title4Out + 14 && (
        <Title>{row(<><Word text="Ihr" frame={frame} start={F.title4} end={F.title4Out} /><Word text="Gebäude," frame={frame} start={F.title4 + 4} end={F.title4Out} /></>)}{row(<Word text="in 3D." frame={frame} start={F.title4 + 10} end={F.title4Out} color={C.apricot600} />)}</Title>
      )}
      {frame >= F.title5 && frame < F.title5Out + 14 && (
        <Title>
          {row(<><Word text="Anklicken," frame={frame} start={F.title5} end={F.title5Out} size={80} /><Word text="anpassen," frame={frame} start={F.click} end={F.title5Out} size={80} /></>)}
          {row(<Word text="fertig." frame={frame} start={F.type + 20} end={F.title5Out} size={80} color={C.apricot600} />)}
        </Title>
      )}
      {frame >= F.title6 && frame < F.title6Out + 14 && (
        <Title>{row(<><Word text="CAD-Modell" frame={frame} start={F.title6} end={F.title6Out} /><Word text="raus." frame={frame} start={F.title6 + 6} end={F.title6Out} color={C.apricot600} /></>)}</Title>
      )}
      <EndCard frame={frame} />
    </>
  );
}


/** Dimension lines the way the product draws them: ink line, 45 degree ticks, mono label on paper. */
function Dim({ a, b, off, text, frame, start, end, cam }: { a: [number, number, number]; b: [number, number, number]; off: [number, number, number]; text: string; frame: number; start: number; end: number; cam: Cam }) {
  const t = prog(frame, start, start + 26, EASE.out);
  const o = 1 - prog(frame, end, end + 12);
  if (t <= 0 || o <= 0) return null;
  const c = threeCamera(cam);
  const add = (p: [number, number, number], k = 1): [number, number, number] => [p[0] + off[0] * k, p[1] + off[1] * k, p[2] + off[2] * k];
  const A = project(c, add(a)), B = project(c, add(b));
  const A0 = project(c, add(a, 0.15)), B0 = project(c, add(b, 0.15));
  const A1 = project(c, add(a, 1.25)), B1 = project(c, add(b, 1.25));
  const mid = { x: A.x + (B.x - A.x) * 0.5, y: A.y + (B.y - A.y) * 0.5 };
  const Bt = { x: mid.x + (B.x - mid.x) * t, y: mid.y + (B.y - mid.y) * t };
  const At = { x: mid.x + (A.x - mid.x) * t, y: mid.y + (A.y - mid.y) * t };
  const tick = (p: { x: number; y: number }) => <line x1={p.x - 7} y1={p.y + 7} x2={p.x + 7} y2={p.y - 7} stroke={C.ink} strokeWidth={2} />;
  return (
    <svg width={1920} height={1080} style={{ position: "absolute", inset: 0, opacity: o, overflow: "visible" }}>
      <g opacity={t}>
        <line x1={A0.x} y1={A0.y} x2={A1.x} y2={A1.y} stroke={C.ink} strokeWidth={1.2} />
        <line x1={B0.x} y1={B0.y} x2={B1.x} y2={B1.y} stroke={C.ink} strokeWidth={1.2} />
      </g>
      <line x1={At.x} y1={At.y} x2={Bt.x} y2={Bt.y} stroke={C.ink} strokeWidth={1.6} />
      {t > 0.95 && tick(A)}
      {t > 0.95 && tick(B)}
      <foreignObject x={mid.x - 90} y={mid.y - 22} width={180} height={44}>
        <div style={{ display: "flex", justifyContent: "center", opacity: clamp((t - 0.4) * 2) }}>
          <span style={{ background: C.paper, border: `1.5px solid ${C.ink}`, fontFamily: MONO, fontSize: 22, padding: "4px 10px" }}>{text}</span>
        </div>
      </foreignObject>
    </svg>
  );
}

export function Dimensions({ frame, cam }: { frame: number; cam: Cam }) {
  const x0 = -CENTER.x, x1 = 12.4 - CENTER.x, zS = CENTER.y;
  return (
    <>
      <Dim a={[x0, 0, zS]} b={[x1, 0, zS]} off={[0, 0, 1]} text="12,40 m" frame={frame} start={F.title4 + 16} end={F.title4Out} cam={cam} />
      <Dim a={[x0, 0, zS]} b={[x0, 2.87, zS]} off={[-1, 0, 0]} text="2,87 m" frame={frame} start={F.title4 + 40} end={F.title4Out} cam={cam} />
    </>
  );
}
