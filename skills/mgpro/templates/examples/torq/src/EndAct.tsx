import { AbsoluteFill } from "remotion";
import { Words } from "./kit";
import { COLOR, EASE, FONT, T, cueAt, cuesOf, enter, lime, mix, prog, sp } from "./lib";
import { BLADES } from "./Medal";

const BLOCKS = cuesOf("block").map((c) => c.frame);
const NAME = cueAt("whoosh", cuesOf("whoosh").length - 1);
const BELL = cuesOf("bell").filter((c) => c.frame > T.end)[0]!.frame;
const MARK = 300;

/** The mark builds blade by blade, spinning in like torque, then the name and the line. */
export function EndAct({ frame: f }: { frame: number }) {
  const drift = 1 + 0.025 * prog(f, T.end, 1800, EASE.out);
  const spin = -150 * (1 - prog(f, T.end, T.end + 64, EASE.out));
  const name = prog(f, NAME, NAME + 30, EASE.out);
  // The mark slides left to make room for the name.
  const slide = prog(f, NAME - 6, NAME + 26, EASE.inOut);
  const sheen = prog(f, BELL - 6, BELL + 30, EASE.inOut);
  const glow = 0.35 + 0.65 * (1 - prog(f, T.end, T.end + 40));
  const fade = prog(f, 1786, 1800);
  return (
    <AbsoluteFill style={{ fontFamily: FONT, background: `radial-gradient(70% 70% at 50% 46%, #141711 0%, ${COLOR.deep} 70%)` }}>
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", transform: `scale(${drift})` }}>
        <div style={{ display: "flex", alignItems: "center", marginTop: -110, gap: mix(0, 44, slide) }}>
          <div style={{ position: "relative", width: MARK, height: MARK }}>
            <div style={{ position: "absolute", inset: -80, borderRadius: 999, background: `radial-gradient(circle, ${lime(0.22 * glow)} 0%, transparent 65%)` }} />
            <svg width={MARK} height={MARK} viewBox="0 0 1024 1024" style={{ position: "absolute", inset: 0, overflow: "visible", transform: `rotate(${spin}deg)` }}>
              <defs>
                <linearGradient id="sheen" gradientUnits="userSpaceOnUse" x1={mix(-600, 1300, sheen)} y1={0} x2={mix(-200, 1700, sheen)} y2={400}>
                  <stop offset="0" stopColor={COLOR.lime} />
                  <stop offset="0.5" stopColor="#F6FFD8" />
                  <stop offset="1" stopColor={COLOR.lime} />
                </linearGradient>
              </defs>
              {BLADES.map((d, i) => {
                const s = sp(f, BLOCKS[i]!, "pop");
                const r = -50 * (1 - prog(f, BLOCKS[i]!, BLOCKS[i]! + 24, EASE.out));
                return (
                  <g key={i} transform={`rotate(${r} 512 512) translate(512 512) scale(${Math.max(0.001, s)}) translate(-512 -512)`} opacity={Math.min(1, s * 2)}>
                    <g transform="translate(0,1024) scale(0.1,-0.1)">
                      <path d={d} fill={sheen > 0 && sheen < 1 ? "url(#sheen)" : COLOR.lime} />
                    </g>
                  </g>
                );
              })}
            </svg>
          </div>
          <div style={{ overflow: "hidden", width: mix(0, 470, slide), paddingBottom: 30, marginBottom: -30 }}>
            <div style={{ fontSize: 250, fontWeight: 700, letterSpacing: "-0.06em", lineHeight: 1, color: COLOR.ink, transform: `translateY(${(1 - name) * 110}%)`, filter: name < 1 ? `blur(${(1 - name) * 8}px)` : undefined }}>torq</div>
          </div>
        </div>
        <div style={{ marginTop: 40 }}>
          <Words lines={["Strength, *ranked."]} frame={f} start={NAME + 22} size={64} weight={600} color={COLOR.soft} align="center" />
        </div>
        <div style={{ marginTop: 56, padding: "14px 34px", borderRadius: 999, fontSize: 28, fontWeight: 600, color: COLOR.ink, boxShadow: `inset 0 0 0 1.5px ${COLOR.line}`, background: COLOR.surface, ...enter(f, NAME + 60, { rise: 14 }) }}>For Android</div>
      </AbsoluteFill>
      <AbsoluteFill style={{ background: "#000", opacity: fade }} />
    </AbsoluteFill>
  );
}
