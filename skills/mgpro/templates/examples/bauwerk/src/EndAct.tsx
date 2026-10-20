import { AbsoluteFill } from "remotion";
import { MacCursor } from "./Cursor";
import type { CursorTrack } from "./Cursor";
import { Words } from "./kit";
import { COLOR, EASE, FONT, T, clamp, cuesOf, enter, prog, sp } from "./lib";

const BLOCKS = cuesOf("block").map((c) => c.frame);
const MARK = ["M3 25V11l6-3v17H3Z", "M10.5 25V6l7-3.5V25h-7Z", "M19 25V9.5l6 2.5v13h-6Z"];
const URL = { x: 960, y: 760 };

const you: CursorTrack = {
  stops: [
    { f: 1652, x: 1440, y: 1000 },
    { f: 1700, x: URL.x + 92, y: URL.y + 8, arc: 0.12 },
  ],
  shapes: [{ f: 1690, shape: "hand" }],
  visible: [{ f: 1652, on: true }],
};

/** Act IV: the mark builds block by block, the name rises, and the address to try it. */
export function EndAct({ frame: f }: { frame: number }) {
  const drift = 1 + 0.025 * prog(f, T.end, 1800, EASE.out);
  const name = prog(f, 1572, 1600, EASE.out);
  const hover = prog(f, 1694, 1708);
  return (
    <AbsoluteFill style={{ fontFamily: FONT, background: "radial-gradient(120% 100% at 50% 40%, #ffffff 0%, #f1f4f7 100%)" }}>
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", transform: `scale(${drift})` }}>
        <div style={{ display: "flex", alignItems: "center", gap: 36, marginTop: -90 }}>
          <svg width={150} height={150} viewBox="0 0 28 28" style={{ color: COLOR.navy, overflow: "visible" }} fill="currentColor">
            {MARK.map((d, i) => (
              <path key={d} d={d} opacity={[1, 0.85, 0.7][i]} style={{ transform: `scaleY(${sp(f, BLOCKS[i]!, "pop")})`, transformOrigin: "50% 100%", transformBox: "fill-box" }} />
            ))}
          </svg>
          <div style={{ overflow: "hidden", paddingBottom: 18, marginBottom: -18 }}>
            <div style={{ fontSize: 156, fontWeight: 600, letterSpacing: "-0.04em", color: COLOR.ink, transform: `translateY(${(1 - name) * 110}%)`, filter: name < 1 ? `blur(${(1 - name) * 8}px)` : undefined }}>Bauwerk</div>
          </div>
        </div>
        <div style={{ marginTop: 26 }}>
          <Words lines={["From survey to iSFP."]} frame={f} start={1594} size={54} weight={500} color={COLOR.muted} align="center" />
        </div>
        <div
          style={{
            marginTop: 64,
            padding: "18px 40px",
            borderRadius: 999,
            background: `rgba(2,78,123,${0.08 + 0.06 * hover})`,
            color: COLOR.navy,
            fontSize: 38,
            fontWeight: 600,
            letterSpacing: "-0.01em",
            boxShadow: `inset 0 0 0 ${1.5 + hover}px rgba(2,78,123,${0.25 + 0.2 * hover})`,
            ...enter(f, 1630, { rise: 16 }),
          }}
        >
          bauwerk-demo.xyz
        </div>
      </AbsoluteFill>
      <div style={{ position: "absolute", bottom: 64, width: "100%", textAlign: "center", fontSize: 24, color: "#8a95a1", ...enter(f, 1660, { rise: 8 }), opacity: clamp((f - 1660) / 20) }}>
        Made by Adilzhan Yerzhan for 20°
      </div>
      <MacCursor track={you} frame={f} />
    </AbsoluteFill>
  );
}
