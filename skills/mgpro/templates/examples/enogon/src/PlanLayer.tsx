import { C, DISPLAY, MONO, de } from "./brand";
import { cornerPin, project, threeCamera } from "./camera";
import type { Cam } from "./camera";
import { innerQuad, outerQuad } from "./geo";
import { EASE, clamp, mix, prog } from "./lib";
import { CENTER, FOOTPRINT, INNER_FACE, INNER_WALLS, OPENINGS, OUTER_WALLS, ROOMS, onWall, roomArea, roomCentre, wallById, wallLength, wallPieces } from "./plan";
import type { P, Wall } from "./plan";
import { F } from "./timeline";

/** The drawing table: plan metres from x0 to x1 and y0 to y1, K pixels per metre. */
const X0 = -9, X1 = 21.4, Y0 = -8, Y1 = 18;
const K = 56;
const SW = (X1 - X0) * K;
const SH = (Y1 - Y0) * K;
const u = (x: number) => (x - X0) * K;
const v = (y: number) => (Y1 - y) * K;
const pts = (ps: P[]) => ps.map((p) => `${u(p.x).toFixed(1)},${v(p.y).toFixed(1)}`).join(" ");
const W3 = (p: P): [number, number, number] => [p.x - CENTER.x, 0, CENTER.y - p.y];

/** The paper sheet the plan was printed on, in plan metres. */
const PAPER = { x0: -2.6, x1: 15.0, y0: -2.3, y1: 12.1 };

/** The AI's trace: one continuous line around the outer face, a corner handle popping as the
 * line passes each corner (OUTER_AT), then the inner walls, the doors and the rooms. */
const RING = [...FOOTPRINT, FOOTPRINT[0]!];
const SEG = RING.slice(1).map((p, i) => Math.hypot(p.x - RING[i]!.x, p.y - RING[i]!.y));
const TOTAL = SEG.reduce((a, b) => a + b, 0);
const CUM = SEG.reduce<number[]>((acc, l) => [...acc, acc[acc.length - 1]! + l], [0]);
export const OUTER_AT = CUM.slice(1).map((c) => Math.round(F.traceStart + (c / TOTAL) * F.traceLen));
export const INNER_AT = INNER_WALLS.map((_, i) => F.innerStart + i * F.innerStep);
const DOORS = OPENINGS.filter((o) => o.kind === "door");
const WINDOWS = OPENINGS.filter((o) => o.kind === "window");
export const DOOR_AT = DOORS.map((_, i) => F.doorStart + i * F.doorStep);
export const ROOM_AT = ROOMS.map((_, i) => F.roomStart + i * F.roomStep);
const TRACE_EASE = (t: number) => (t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2);

/** The traced outline up to length d along the ring, as a polyline. */
function ringTo(d: number): P[] {
  const out: P[] = [RING[0]!];
  for (let i = 0; i < SEG.length; i++) {
    if (d >= CUM[i + 1]!) {
      out.push(RING[i + 1]!);
      continue;
    }
    const t = (d - CUM[i]!) / SEG[i]!;
    out.push({ x: RING[i]!.x + (RING[i + 1]!.x - RING[i]!.x) * t, y: RING[i]!.y + (RING[i + 1]!.y - RING[i]!.y) * t });
    break;
  }
  return out;
}

function Handle({ p, t, size = 15 }: { p: P; t: number; size?: number }) {
  if (t <= 0) return null;
  // Pops in with a small overshoot (a result), then sits still.
  const k = t < 1 ? 1 + 0.35 * Math.sin(Math.PI * t) * (1 - t) : 1;
  const s = size * Math.min(1, t * 1.6) * k;
  return <rect x={u(p.x) - s / 2} y={v(p.y) - s / 2} width={s} height={s} fill={C.paper} stroke={C.ink} strokeWidth={1.8} />;
}

function wallPolys(w: Wall, s: number, outerIndex: number) {
  const L = wallLength(w) * s;
  const out: P[][] = [];
  for (const [a, b] of wallPieces(w)) {
    if (a >= L) break;
    out.push(outerIndex >= 0 ? outerQuad(outerIndex, a, Math.min(b, L)) : innerQuad(w, a, Math.min(b, L)));
  }
  return out;
}

/** The old drawing as a consultant would get it: a grey scan, slightly turned, a little wobbly. */
function Scan({ opacity }: { opacity: number }) {
  const ink = "#3b3b3b";
  return (
    <g opacity={opacity} filter="url(#scan)" transform={`rotate(-1.1 ${u(CENTER.x)} ${v(CENTER.y)}) translate(${0.18 * K} ${-0.12 * K})`}>
      <polygon points={pts(FOOTPRINT)} fill="url(#poche)" stroke={ink} strokeWidth={2} />
      <polygon points={pts(INNER_FACE)} fill="#fbfaf6" stroke={ink} strokeWidth={1.6} />
      {INNER_WALLS.map((w) => (
        <polygon key={w.id} points={pts(innerQuad(w, 0, wallLength(w)))} fill="#d9d7d0" stroke={ink} strokeWidth={1.2} />
      ))}
      {OPENINGS.map((o, i) => {
        const w = wallById(o.wall);
        const a = onWall(w, o.at - o.width / 2);
        const b = onWall(w, o.at + o.width / 2);
        const dx = (w.b.x - w.a.x) / wallLength(w), dy = (w.b.y - w.a.y) / wallLength(w);
        const nx = -dy * (w.t / 2 + 0.02), ny = dx * (w.t / 2 + 0.02);
        const gap = [
          { x: a.x - nx, y: a.y - ny },
          { x: b.x - nx, y: b.y - ny },
          { x: b.x + nx, y: b.y + ny },
          { x: a.x + nx, y: a.y + ny },
        ];
        return <polygon key={i} points={pts(gap)} fill="#fbfaf6" stroke="none" />;
      })}
      {WINDOWS.map((o, i) => {
        const w = wallById(o.wall);
        const a = onWall(w, o.at - o.width / 2), b = onWall(w, o.at + o.width / 2);
        return <line key={i} x1={u(a.x)} y1={v(a.y)} x2={u(b.x)} y2={v(b.y)} stroke={ink} strokeWidth={1.2} />;
      })}
      {DOORS.map((o, i) => <DoorSymbol key={i} o={o} color={ink} width={1} progress={1} />)}
      {ROOMS.map((r, i) => {
        const c = roomCentre(r);
        return (
          <text key={i} x={u(c.x)} y={v(c.y)} fontFamily={MONO} fontSize={15} fill={ink} textAnchor="middle" opacity={0.8}>
            {r.name.toUpperCase()}
          </text>
        );
      })}
      <text x={u(0)} y={v(-1.25)} fontFamily={MONO} fontSize={16} fill={ink}>
        GRUNDRISS EG · M 1:100
      </text>
      <line x1={u(0)} y1={v(-0.7)} x2={u(12.4)} y2={v(-0.7)} stroke={ink} strokeWidth={1} />
      <text x={u(6.2)} y={v(-0.5)} fontFamily={MONO} fontSize={14} fill={ink} textAnchor="middle">
        12,40
      </text>
    </g>
  );
}

function ScanDefs() {
  return (
    <defs>
      <pattern id="poche" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
        <rect width="8" height="8" fill="#e9e7e0" />
        <line x1="0" y1="0" x2="0" y2="8" stroke="#6b6b6b" strokeWidth="1.3" />
      </pattern>
      <filter id="scan" x="-5%" y="-5%" width="110%" height="110%">
        <feTurbulence type="fractalNoise" baseFrequency="0.04" numOctaves="2" seed="7" result="t" />
        <feDisplacementMap in="SourceGraphic" in2="t" scale="2.6" />
      </filter>
    </defs>
  );
}

function DoorSymbol({ o, color, width, progress }: { o: (typeof OPENINGS)[number]; color: string; width: number; progress: number }) {
  if (progress <= 0) return null;
  const w = wallById(o.wall);
  const L = wallLength(w);
  const dx = (w.b.x - w.a.x) / L, dy = (w.b.y - w.a.y) / L;
  const hingeS = o.hinge === 0 ? o.at - o.width / 2 : o.at + o.width / 2;
  const hinge = onWall(w, hingeS);
  const side = o.swing ?? 1;
  // The leaf opens to 90 degrees across the wall.
  const along = o.hinge === 0 ? 1 : -1;
  const ang = (Math.PI / 2) * progress;
  const nx = -dy * side, ny = dx * side;
  const tip = { x: hinge.x + (dx * along * Math.cos(ang) + nx * Math.sin(ang)) * o.width, y: hinge.y + (dy * along * Math.cos(ang) + ny * Math.sin(ang)) * o.width };
  const start = { x: hinge.x + dx * along * o.width, y: hinge.y + dy * along * o.width };
  // Arc from the closed position to the leaf tip.
  const sweep = (along * side > 0 ? 0 : 1);
  return (
    <g>
      <line x1={u(hinge.x)} y1={v(hinge.y)} x2={u(tip.x)} y2={v(tip.y)} stroke={color} strokeWidth={width * 1.4} />
      <path d={`M ${u(start.x)} ${v(start.y)} A ${o.width * K} ${o.width * K} 0 0 ${sweep} ${u(tip.x)} ${v(tip.y)}`} fill="none" stroke={color} strokeWidth={width} strokeDasharray={progress < 1 ? undefined : undefined} />
    </g>
  );
}

/** The table, the sheet, the scan, and the AI's drawing on top: pinned onto the 3D ground. */
export function PlanLayer({ frame, cam, cardRect }: { frame: number; cam: Cam; cardRect: { x: number; y: number; w: number; h: number } }) {
  const c3 = threeCamera(cam);
  const corners = [W3({ x: X0, y: Y1 }), W3({ x: X1, y: Y1 }), W3({ x: X1, y: Y0 }), W3({ x: X0, y: Y0 })].map((p) => project(c3, p));
  const pin = cornerPin([[0, 0], [SW, 0], [SW, SH], [0, SH]], corners);

  // The sheet grows out of the dragged file card on release, and lands with paper weight.
  const grow = prog(frame, F.release, F.sheetLand, EASE.out);
  const paperShown = frame >= F.release;
  const paperCorners = [
    { x: PAPER.x0, y: PAPER.y1 },
    { x: PAPER.x1, y: PAPER.y1 },
    { x: PAPER.x1, y: PAPER.y0 },
    { x: PAPER.x0, y: PAPER.y0 },
  ].map((p) => project(c3, W3(p)));
  const card = [
    { x: cardRect.x, y: cardRect.y },
    { x: cardRect.x + cardRect.w, y: cardRect.y },
    { x: cardRect.x + cardRect.w, y: cardRect.y + cardRect.h },
    { x: cardRect.x, y: cardRect.y + cardRect.h },
  ];
  const sheetDst = paperCorners.map((p, i) => ({ x: mix(card[i]!.x, p.x, grow), y: mix(card[i]!.y, p.y, grow) }));
  const PW = (PAPER.x1 - PAPER.x0) * K, PH = (PAPER.y1 - PAPER.y0) * K;
  const sheetPin = cornerPin([[0, 0], [PW, 0], [PW, PH], [0, PH]], sheetDst);
  const lift = 1 - prog(frame, F.sheetLand - 6, F.sheetLand + 4);

  const gridOn = prog(frame, 0, 20) * (1 - prog(frame, F.morph, F.morph + 40));
  // The scan dims as the AI starts reading it, and leaves as the lines thicken into walls.
  const scanOn = paperShown ? 1 - 0.6 * prog(frame, F.traceStart - 8, F.traceStart + 12) - 0.4 * prog(frame, F.thicken, F.thicken + 24) : 0;
  const paperOn = paperShown ? 1 - prog(frame, F.tilt + 30, F.tilt + 90) : 0;
  const thick = prog(frame, F.thicken, F.thicken + 18, EASE.out);
  const traceOn = 1 - prog(frame, F.thicken + 6, F.thicken + 24);
  const planOn = 1 - prog(frame, F.land1 + 10, F.land1 + 30);
  const labelsOn = 1 - prog(frame, F.egRise, F.egRise + 24);

  return (
    <>
      {/* The table grid, part of the ground the house will stand on. */}
      <div style={{ position: "absolute", left: 0, top: 0, width: SW, height: SH, transformOrigin: "0 0", transform: pin, opacity: gridOn }}>
        <svg width={SW} height={SH}>
          <defs>
            <pattern id="grid" width={K} height={K} patternUnits="userSpaceOnUse" x={u(0) % K} y={v(0) % K}>
              <path d={`M ${K} 0 L 0 0 0 ${K}`} fill="none" stroke={C.line} strokeWidth={1.4} />
            </pattern>
            <radialGradient id="gridfade" cx="50%" cy="50%" r="50%">
              <stop offset="55%" stopColor="#fff" stopOpacity={1} />
              <stop offset="100%" stopColor="#fff" stopOpacity={0} />
            </radialGradient>
            <mask id="gridmask">
              <rect width={SW} height={SH} fill="url(#gridfade)" />
            </mask>
          </defs>
          <rect width={SW} height={SH} fill="url(#grid)" mask="url(#gridmask)" />
        </svg>
      </div>

      {/* The paper with the scan: first as the dragged card's growth, then lying on the table. */}
      {paperShown && paperOn > 0.001 && (
        <div style={{ position: "absolute", left: 0, top: 0, width: PW, height: PH, transformOrigin: "0 0", transform: sheetPin, opacity: paperOn }}>
          <div
            style={{
              position: "absolute",
              inset: 0,
              background: "#fbfaf6",
              boxShadow: `0 ${4 + 30 * lift}px ${16 + 50 * lift}px rgba(0,0,0,${0.1 + 0.08 * lift}), 0 1px 0 rgba(0,0,0,0.06)`,
              outline: `1px solid ${C.line}`,
            }}
          />
          <svg width={PW} height={PH} style={{ position: "absolute", inset: 0, overflow: "visible" }}>
            <ScanDefs />
            <g transform={`translate(${-u(PAPER.x0)} ${-v(PAPER.y1)})`}>
              <Scan opacity={scanOn} />
            </g>
          </svg>
        </div>
      )}

      <div style={{ position: "absolute", left: 0, top: 0, width: SW, height: SH, transformOrigin: "0 0", transform: pin }}>
        <svg width={SW} height={SH} style={{ overflow: "visible" }}>


          {/* Rooms flood one after the other, from their centre. */}
          <g opacity={planOn}>
            {ROOMS.map((r, i) => {
              const t = prog(frame, ROOM_AT[i]!, ROOM_AT[i]! + 14, EASE.out);
              if (t <= 0) return null;
              const c = roomCentre(r);
              const [x0, x1, y0, y1] = r.box;
              const sx = (x1 - x0) * t, sy = (y1 - y0) * t;
              const fill = r.name === "Treppe" ? C.tuerkis100 : r.name === "Bad" || r.name === "Küche" ? C.apricot100 : C.tuerkis200;
              return <rect key={i} x={u(c.x - sx / 2)} y={v(c.y + sy / 2)} width={sx * K} height={sy * K} fill={fill} />;
            })}
          </g>

          {/* Once traced, the lines thicken into walls: apricot with an ink edge, openings open. */}
          <g opacity={thick * (1 - prog(frame, F.egRise + 40, F.egRise + 64))}>
            {OUTER_WALLS.map((w, i) => wallPolys(w, 1, i).map((q, k) => <polygon key={`${i}-${k}`} points={pts(q)} fill={C.apricot300} stroke={C.ink} strokeWidth={1.8} strokeLinejoin="round" />))}
            {INNER_WALLS.map((w, i) => wallPolys(w, 1, -1).map((q, k) => <polygon key={`i${i}-${k}`} points={pts(q)} fill={C.apricot300} stroke={C.ink} strokeWidth={1.4} strokeLinejoin="round" />))}
          </g>

          {/* The trace itself: a fine line runs round the outline, handles pop at the corners. */}
          <g opacity={traceOn}>
            <polyline points={pts(ringTo(TOTAL * TRACE_EASE(prog(frame, F.traceStart, F.traceStart + F.traceLen, (t) => t))))} fill="none" stroke={C.apricot600} strokeWidth={5.5} strokeLinejoin="miter" />
            {INNER_WALLS.map((w, i) => {
              const t = prog(frame, INNER_AT[i]!, INNER_AT[i]! + F.innerLen, EASE.standard);
              if (t <= 0) return null;
              const b = onWall(w, wallLength(w) * t);
              return (
                <g key={w.id}>
                  <line x1={u(w.a.x)} y1={v(w.a.y)} x2={u(b.x)} y2={v(b.y)} stroke={C.apricot600} strokeWidth={4} />
                  <Handle p={w.a} t={prog(frame, INNER_AT[i]!, INNER_AT[i]! + 8)} size={11} />
                  <Handle p={w.b} t={prog(frame, INNER_AT[i]! + F.innerLen - 2, INNER_AT[i]! + F.innerLen + 6)} size={11} />
                </g>
              );
            })}
            {RING.slice(1).map((p, i) => (
              <Handle key={i} p={p} t={prog(frame, OUTER_AT[i]! - 1, OUTER_AT[i]! + 9)} />
            ))}
            {(() => {
              const t = prog(frame, F.traceStart, F.traceStart + F.traceLen, (x) => x);
              if (t <= 0 || t >= 1) return null;
              const pts2 = ringTo(TOTAL * TRACE_EASE(t));
              const h = pts2[pts2.length - 1]!;
              return <circle cx={u(h.x)} cy={v(h.y)} r={10} fill={C.apricot600} />;
            })()}
          </g>

          {/* Windows and doors: the symbols every plan uses. */}
          <g opacity={planOn}>
            {WINDOWS.map((o, i) => {
              const t = prog(frame, F.doorStart + i * 2, F.doorStart + i * 2 + 8);
              if (t <= 0) return null;
              const w = wallById(o.wall);
              const L = wallLength(w);
              const dx = (w.b.x - w.a.x) / L, dy = (w.b.y - w.a.y) / L;
              const nx = -dy, ny = dx;
              const a = onWall(w, o.at - o.width / 2), b = onWall(w, o.at + o.width / 2);
              return (
                <g key={i} opacity={t}>
                  {[-0.07, 0.07].map((k) => (
                    <line key={k} x1={u(a.x + nx * k)} y1={v(a.y + ny * k)} x2={u(b.x + nx * k)} y2={v(b.y + ny * k)} stroke={C.ink} strokeWidth={1.2} />
                  ))}
                </g>
              );
            })}
            {DOORS.map((o, i) => (
              <DoorSymbol key={i} o={o} color={C.ink} width={1.4} progress={prog(frame, DOOR_AT[i]!, DOOR_AT[i]! + 12, EASE.out)} />
            ))}
          </g>

          {/* Room tags in the product's own style: black label, white mono text. */}
          <g opacity={labelsOn}>
            {ROOMS.map((r, i) => {
              const t = prog(frame, ROOM_AT[i]! + 4, ROOM_AT[i]! + 16, EASE.out);
              if (t <= 0) return null;
              const c = roomCentre(r);
              const small = r.box[1] - r.box[0] < 2.2;
              const text = small ? r.name.toUpperCase() : `${r.name.toUpperCase()} ${de(roomArea(r), 1)} m²`;
              const fs = small ? 13 : 16;
              const w = text.length * fs * 0.62 + 16;
              const h = fs + 12;
              return (
                <g key={i} opacity={t} transform={`translate(${u(c.x)} ${v(c.y) + 8 * (1 - t)})`}>
                  <rect x={-w / 2} y={-h / 2} width={w} height={h} fill={C.ink} />
                  <text y={fs * 0.36} fontFamily={MONO} fontSize={fs} textAnchor="middle" fill={C.paper} letterSpacing="0.04em">
                    {text}
                  </text>
                </g>
              );
            })}
          </g>
        </svg>
      </div>
    </>
  );
}

