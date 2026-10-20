import { EASE, clamp, cuesOf, prog } from "./lib";
import { DOORS, FOOTPRINT, INNER_WALLS, ROOMS, STREET, EDGES, centroid, offset } from "./plan";
import type { P } from "./plan";

/** The sheet's own pixels: 40 per metre around the ground floor. */
export const K = 40;
export const SHEET = { x0: -10.7, x1: 9.7, y0: -9.6, y1: 9.7 };
export const SHEET_W = (SHEET.x1 - SHEET.x0) * K;
export const SHEET_H = (SHEET.y1 - SHEET.y0) * K;
const u = (x: number) => (x - SHEET.x0) * K;
const v = (y: number) => (SHEET.y1 - y) * K;
const pt = (p: P) => `${u(p.x)},${v(p.y)}`;

const TRACE = cuesOf("trace");
const ROOM = cuesOf("room");
const INK = "#4d3a2b";
const OLD_NAMES = ["Stube", "Kammer", "Küche", "Laden", "Bad", "Kammer", "Stube", "Abort"];

const CENTRE_LINE = offset(FOOTPRINT, -0.2);
const OUTER_SEGMENTS = CENTRE_LINE.map((a, i) => [a, CENTRE_LINE[(i + 1) % CENTRE_LINE.length]!] as const);
const SEGMENTS: (readonly [P, P])[] = [...OUTER_SEGMENTS, ...INNER_WALLS.map((w) => [w.a, w.b] as const)];

/**
 * The ground floor as an old drawing on yellowed paper (sepia ink, hatched walls, door arcs,
 * dimension chains, German room names), and on top of it what the AI finds: every wall traced in
 * light, the doors swung, the rooms flooded with colour. Drawn in the sheet's own pixels; the
 * scene corner-pins it onto the 3D ground.
 */
export function PlanSheet({ frame }: { frame: number }) {
  const paperIn = prog(frame, 392, 412, EASE.out);
  const dim = prog(frame, 414, 440);
  const paperOut = prog(frame, 568, 584);
  const linesOut = prog(frame, 578, 594);
  const outer = FOOTPRINT.map(pt).join(" ");
  const inner = offset(FOOTPRINT, -0.4).map(pt).join(" ");
  return (
    <svg width={SHEET_W} height={SHEET_H} viewBox={`0 0 ${SHEET_W} ${SHEET_H}`} style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }}>
      <defs>
        <pattern id="hatch" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
          <line x1="0" y1="0" x2="0" y2="7" stroke={INK} strokeWidth="1.6" />
        </pattern>
        <filter id="wobble">
          <feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="4" />
          <feDisplacementMap in="SourceGraphic" scale="2.2" />
        </filter>
        <filter id="paper" x="0" y="0" width="100%" height="100%">
          <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="3" seed="2" result="n" />
          <feColorMatrix in="n" type="matrix" values="0 0 0 0 0.35  0 0 0 0 0.27  0 0 0 0 0.16  0 0 0 0.22 0" />
          <feComposite in2="SourceGraphic" operator="in" />
          <feBlend in2="SourceGraphic" mode="multiply" />
        </filter>
        <radialGradient id="age" cx="50%" cy="45%" r="75%">
          <stop offset="60%" stopColor="#efe5cd" stopOpacity="0" />
          <stop offset="100%" stopColor="#b89a68" stopOpacity="0.55" />
        </radialGradient>
        <radialGradient id="stain" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stopColor="#b08a52" stopOpacity="0.28" />
          <stop offset="100%" stopColor="#b08a52" stopOpacity="0" />
        </radialGradient>
        <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
          <feGaussianBlur stdDeviation="5" />
        </filter>
        <radialGradient id="spark">
          <stop offset="0%" stopColor="#ffffff" />
          <stop offset="35%" stopColor="#e9d5ff" stopOpacity="0.9" />
          <stop offset="100%" stopColor="#a855f7" stopOpacity="0" />
        </radialGradient>
        {ROOMS.map((r, i) => {
          const c = centroid(r.polygon);
          const start = ROOM[i]?.frame ?? 9999;
          const grow = prog(frame, start, start + 16, EASE.out);
          return (
            <clipPath key={i} id={`room${i}`}>
              <circle cx={u(c.x)} cy={v(c.y)} r={grow * 15 * K} />
            </clipPath>
          );
        })}
      </defs>

      {/* The paper and the old ink drawing, dimmed to night once the AI looks at it. */}
      <g
        opacity={paperIn * (1 - paperOut)}
        transform={`translate(${SHEET_W / 2} ${SHEET_H / 2}) scale(${0.92 + 0.08 * paperIn}) translate(${-SHEET_W / 2} ${-SHEET_H / 2})`}
        style={{ filter: `brightness(${1 - 0.62 * dim}) saturate(${1 - 0.5 * dim}) blur(${(1 - paperIn) * 6}px)` }}
      >
        <rect x={0} y={0} width={SHEET_W} height={SHEET_H} rx={6} fill="#efe4cb" filter="url(#paper)" />
        <rect x={0} y={0} width={SHEET_W} height={SHEET_H} rx={6} fill="url(#age)" />
        <circle cx={SHEET_W * 0.78} cy={SHEET_H * 0.2} r={90} fill="url(#stain)" />
        <circle cx={SHEET_W * 0.16} cy={SHEET_H * 0.82} r={120} fill="url(#stain)" />
        <line x1={SHEET_W / 2} y1={0} x2={SHEET_W / 2} y2={SHEET_H} stroke="#8a6c44" strokeOpacity={0.18} strokeWidth={2} />
        <line x1={SHEET_W / 2 + 2} y1={0} x2={SHEET_W / 2 + 2} y2={SHEET_H} stroke="#fff8e6" strokeOpacity={0.4} strokeWidth={1.5} />
        <g filter="url(#wobble)" opacity={0.88}>
          <polygon points={`${outer}`} fill="none" stroke={INK} strokeWidth={2} />
          <path d={`M${outer}Z M${inner}Z`} fill="url(#hatch)" fillRule="evenodd" stroke={INK} strokeWidth={1.4} />
          {INNER_WALLS.map((w, i) => (
            <line key={i} x1={u(w.a.x)} y1={v(w.a.y)} x2={u(w.b.x)} y2={v(w.b.y)} stroke={INK} strokeWidth={w.thick * K} strokeLinecap="square" />
          ))}
          {/* Openings in the street wall: the wall broken, two thin lines for the glass. */}
          {STREET.filter((w) => w.storey === 0).map((w, i) => {
            const e = EDGES[w.edge]!;
            const c = { x: e.a.x + e.u.x * w.along - e.n.x * 0.2, y: e.a.y + e.u.y * w.along - e.n.y * 0.2 };
            const hx = (e.u.x * w.width) / 2;
            const hy = (e.u.y * w.width) / 2;
            return (
              <g key={i}>
                <line x1={u(c.x - hx)} y1={v(c.y - hy)} x2={u(c.x + hx)} y2={v(c.y + hy)} stroke="#efe4cb" strokeWidth={0.42 * K} />
                {!w.door && (
                  <>
                    <line x1={u(c.x - hx + e.n.x * 0.06)} y1={v(c.y - hy + e.n.y * 0.06)} x2={u(c.x + hx + e.n.x * 0.06)} y2={v(c.y + hy + e.n.y * 0.06)} stroke={INK} strokeWidth={1.2} />
                    <line x1={u(c.x - hx - e.n.x * 0.06)} y1={v(c.y - hy - e.n.y * 0.06)} x2={u(c.x + hx - e.n.x * 0.06)} y2={v(c.y + hy - e.n.y * 0.06)} stroke={INK} strokeWidth={1.2} />
                  </>
                )}
              </g>
            );
          })}
          {DOORS.map((d, i) => (
            <path
              key={i}
              d={`M${u(d.at.x)},${v(d.at.y)} L${u(d.at.x + d.u.y * d.width)},${v(d.at.y - d.u.x * d.width)} A${d.width * K},${d.width * K} 0 0 1 ${u(d.at.x + d.u.x * d.width)},${v(d.at.y + d.u.y * d.width)}`}
              fill="none"
              stroke={INK}
              strokeWidth={1.1}
            />
          ))}
          {/* Dimension chains along two sides. */}
          <g stroke={INK} strokeWidth={1}>
            <line x1={u(-8.2)} y1={v(-8.6)} x2={u(7.2)} y2={v(-8.6)} />
            {[-8.2, -6.6, -2.19, 2.25, 7.2].map((x) => (
              <line key={x} x1={u(x) - 5} y1={v(-8.6) + 5} x2={u(x) + 5} y2={v(-8.6) - 5} />
            ))}
            <line x1={u(-9.6)} y1={v(-6.7)} x2={u(-9.6)} y2={v(7.27)} />
            {[-6.7, -2.5, 2.23, 7.27].map((y) => (
              <line key={y} x1={u(-9.6) - 5} y1={v(y) + 5} x2={u(-9.6) + 5} y2={v(y) - 5} />
            ))}
          </g>
          <g fill={INK} fontFamily="Georgia, 'Times New Roman', serif" fontStyle="italic" fontSize={15}>
            {[
              [-7.4, "1,59"],
              [-4.4, "4,41"],
              [0.03, "4,44"],
              [4.7, "4,95"],
            ].map(([x, t]) => (
              <text key={t as string} x={u(x as number)} y={v(-8.6) - 8} textAnchor="middle">
                {t}
              </text>
            ))}
            {ROOMS.map((r, i) => {
              const c = centroid(r.polygon);
              return (
                <text key={i} x={u(c.x)} y={v(c.y) + 5} textAnchor="middle" fontSize={r.area > 40 ? 22 : 16}>
                  {OLD_NAMES[i]}
                </text>
              );
            })}
            <text x={SHEET_W - 30} y={SHEET_H - 50} textAnchor="end" fontSize={20} fontStyle="normal" letterSpacing={3}>
              ERDGESCHOSS
            </text>
            <text x={SHEET_W - 30} y={SHEET_H - 26} textAnchor="end" fontSize={15}>
              Methfesselstr. 8, M 1:100
            </text>
          </g>
        </g>
      </g>

      {/* What the AI finds. Rooms first (under the lines), each flooding out from its middle. */}
      <g opacity={1 - linesOut}>
        {ROOMS.map((r, i) => (
          <polygon
            key={i}
            points={r.polygon.map(pt).join(" ")}
            clipPath={`url(#room${i})`}
            fill={["#7c9cff", "#b18cff", "#f08fd0", "#5fd0e6", "#ffc46b", "#86e0a3", "#9fa6ff", "#ff9f8a"][i]}
            fillOpacity={0.42}
          />
        ))}
        {SEGMENTS.map(([a, b], k) => {
          const start = TRACE[k]?.frame ?? 9999;
          const t = prog(frame, start, start + 13, EASE.out);
          if (t <= 0) return null;
          const len = Math.hypot(u(b.x) - u(a.x), v(b.y) - v(a.y));
          const head = { x: u(a.x) + (u(b.x) - u(a.x)) * t, y: v(a.y) + (v(b.y) - v(a.y)) * t };
          const spark = clamp(1 - (frame - start - 13) / 10);
          const props = { x1: u(a.x), y1: v(a.y), x2: u(b.x), y2: v(b.y), strokeDasharray: `${len} ${len}`, strokeDashoffset: len * (1 - t), strokeLinecap: "round" as const };
          return (
            <g key={k}>
              <line {...props} stroke="#a855f7" strokeWidth={16} strokeOpacity={0.55} filter="url(#glow)" />
              <line {...props} stroke="#e9d5ff" strokeWidth={6} />
              <line {...props} stroke="#ffffff" strokeWidth={2.5} />
              {spark > 0 && <circle cx={head.x} cy={head.y} r={16 + 8 * spark} fill="url(#spark)" opacity={spark} />}
            </g>
          );
        })}
        {DOORS.map((d, i) => {
          const t = prog(frame, 488 + i * 2, 504 + i * 2, EASE.out);
          if (t <= 0) return null;
          const r = d.width * K;
          const a0 = Math.atan2(-d.u.x, d.u.y);
          const a1 = a0 + (Math.PI / 2) * t;
          const hx = u(d.at.x);
          const hy = v(d.at.y);
          const ex = hx + r * Math.cos(a1);
          const ey = hy - r * Math.sin(a1);
          return (
            <g key={i}>
              <path d={`M${hx + r * Math.cos(a0)},${hy - r * Math.sin(a0)} A${r},${r} 0 0 0 ${ex},${ey}`} fill="none" stroke="#e9d5ff" strokeWidth={2} strokeDasharray="5 5" />
              <line x1={hx} y1={hy} x2={ex} y2={ey} stroke="#ffffff" strokeWidth={3} strokeLinecap="round" />
            </g>
          );
        })}
      </g>
    </svg>
  );
}
