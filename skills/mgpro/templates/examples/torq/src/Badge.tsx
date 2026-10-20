import { TIERS } from "./lib";
import { VORTEX_PATH } from "./Medal";

/** Pointy-top rounded hexagon as an SVG path, in a 100 box. */
function hexPath(r: number, round: number) {
  const pts = Array.from({ length: 6 }, (_, i) => {
    const a = -Math.PI / 2 + (i * Math.PI) / 3;
    return [50 + r * Math.cos(a), 50 + r * Math.sin(a)] as const;
  });
  let d = "";
  pts.forEach((p, i) => {
    const prev = pts[(i + 5) % 6]!;
    const next = pts[(i + 1) % 6]!;
    const toward = (q: readonly [number, number]) => {
      const dx = q[0] - p[0];
      const dy = q[1] - p[1];
      const l = Math.hypot(dx, dy);
      return [p[0] + (dx / l) * round, p[1] + (dy / l) * round];
    };
    const a = toward(prev);
    const b = toward(next);
    d += `${i ? "L" : "M"}${a[0]!.toFixed(2)} ${a[1]!.toFixed(2)} Q${p[0].toFixed(2)} ${p[1].toFixed(2)} ${b[0]!.toFixed(2)} ${b[1]!.toFixed(2)} `;
  });
  return d + "Z";
}

const FRAME = hexPath(44, 9);
const FIELD = hexPath(35, 7);

/** The flat rank badge, as the app draws it in lists: metal frame, dark field, the vortex. */
export function Badge({ tier, size, id }: { tier: number; size: number; id: string }) {
  const t = TIERS[tier]!;
  return (
    <svg width={size} height={size} viewBox="0 0 100 100" style={{ overflow: "visible" }}>
      <defs>
        <linearGradient id={`m${id}`} x1="0" y1="0" x2="1" y2="1">
          <stop offset="0" stopColor={t.light} />
          <stop offset="0.5" stopColor={t.base} />
          <stop offset="1" stopColor={t.dark} />
        </linearGradient>
      </defs>
      <path d={FRAME} fill={`url(#m${id})`} />
      <path d={FIELD} fill="#131510" />
      <g transform="translate(19.5 19.5) scale(0.06)">
        <g transform="translate(0,1024) scale(0.1,-0.1)">
          <path d={VORTEX_PATH} fill={t.light} />
        </g>
      </g>
    </svg>
  );
}
