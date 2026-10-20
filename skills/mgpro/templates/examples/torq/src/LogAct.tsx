import { IconCheck, IconTrophy } from "@tabler/icons-react";
import { AbsoluteFill } from "remotion";
import { Words } from "./kit";
import { COLOR, EASE, FONT, SPRING, T, cueAt, cuesOf, enter, exit, lime, mix, prog, sp } from "./lib";
import { spring } from "remotion";

const SETS = cuesOf("set").map((c) => c.frame);
const ROWS_IN = cuesOf("tick").filter((c) => c.frame < T.engine).map((c) => c.frame);
const PR = cueAt("pr");
const GO = cueAt("go");
const REST_START = SETS[3]!;

const ROWS = [
  { prev: "97.5 × 5", kg: "100", reps: "5" },
  { prev: "97.5 × 5", kg: "100", reps: "5" },
  { prev: "97.5 × 5", kg: "100", reps: "5" },
  { prev: "100 × 4", kg: "102.5", reps: "4" },
];

/** Where the rest ring lives, and where the plate's lime ring was at the cut. */
export const RING = { x: 520, y: 600, r: 170, startR: 766 };
/** Where the dot waits at the start of Act III. */
export const DOT = { x: 960, y: 210, r: 11 };

const COL = { set: 0, prev: 120, kg: 440, reps: 640, check: 820 };
const ROW_H = 112;
const LEFT = 820;
const TOP = 470;

function Cell({ w, children, on }: { w: number; children: React.ReactNode; on: number }) {
  return (
    <div
      style={{
        width: w,
        height: 76,
        borderRadius: 8,
        background: COLOR.page2,
        boxShadow: `inset 0 0 0 1.5px ${COLOR.line}`,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        fontSize: 40,
        fontWeight: 600,
        color: on > 0.5 ? COLOR.ink : COLOR.faint,
        fontVariantNumeric: "tabular-nums",
      }}
    >
      {children}
    </div>
  );
}

function Row({ f, i }: { f: number; i: number }) {
  const row = ROWS[i]!;
  const done = SETS[i]!;
  const on = sp(f, done, "pop");
  const ink = prog(f, done - 1, done + 4);
  const sweep = prog(f, done, done + 16, EASE.out);
  const fade = 1 - prog(f, done + 10, done + 40);
  const press = f >= done - 3 && f < done + 6 ? 1 - 0.08 * Math.sin(((f - (done - 3)) / 9) * Math.PI) : 1;
  const ripple = prog(f, done - 2, done + 20, EASE.out);
  const style = f >= 392 + i * 2 ? exit(f, 392 + i * 2, { lift: 24, blur: 10 }) : enter(f, ROWS_IN[i]!, { rise: 30 });
  const prPop = i === 3 ? sp(f, PR, "pop") : 0;
  return (
    <div style={{ position: "absolute", left: LEFT, top: TOP + i * ROW_H, width: 1000, height: ROW_H, display: "flex", alignItems: "center", ...style }}>
      {/* The lime wash that runs across a row when its set is ticked. */}
      <div style={{ position: "absolute", inset: "6px -20px", borderRadius: 12, background: `linear-gradient(90deg, ${lime(0.13 * fade + 0.05)} ${sweep * 100}%, transparent ${sweep * 100 + 8}%)`, opacity: f >= done ? 1 : 0 }} />
      <div style={{ position: "absolute", left: COL.set, width: 76, height: 76, borderRadius: 8, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 34, fontWeight: 700, color: COLOR.soft, background: COLOR.surface }}>{i + 1}</div>
      <div style={{ position: "absolute", left: COL.prev, fontSize: 34, color: COLOR.faint, fontWeight: 500 }}>{row.prev}</div>
      <div style={{ position: "absolute", left: COL.kg }}>
        <Cell w={170} on={ink}>{row.kg}</Cell>
      </div>
      <div style={{ position: "absolute", left: COL.reps }}>
        <Cell w={140} on={ink}>{row.reps}</Cell>
      </div>
      {i === 3 && prPop > 0 && (
        <div
          style={{
            position: "absolute",
            left: COL.check + 100,
            top: 30,
            padding: "8px 18px 8px 12px",
            borderRadius: 999,
            background: COLOR.pr,
            color: "#16112a",
            display: "flex",
            alignItems: "center",
            gap: 4,
            fontSize: 26,
            fontWeight: 700,
            transform: `scale(${prPop}) rotate(${(1 - prPop) * -14}deg)`,
            boxShadow: `0 0 ${24 * prPop}px rgba(156,134,232,.55)`,
          }}
        >
          <IconTrophy size={26} stroke={2.4} />
          PR
        </div>
      )}
      <div style={{ position: "absolute", left: COL.check, width: 76, height: 76 }}>
        <div
          style={{
            position: "absolute",
            inset: 0,
            borderRadius: 10,
            background: on > 0.01 ? COLOR.lime : COLOR.page2,
            boxShadow: on > 0.01 ? `0 0 ${30 * fade}px ${lime(0.6)}` : `inset 0 0 0 1.5px ${COLOR.line}`,
            transform: `scale(${press * (on > 0.01 ? 0.7 + 0.3 * on : 1)})`,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            color: on > 0.01 ? COLOR.limeInk : COLOR.faint,
          }}
        >
          <IconCheck size={44} stroke={3} style={{ transform: `scale(${on > 0.01 ? on : 1})` }} />
        </div>
        {/* The finger's tap: a soft ring spreading from the box. */}
        {f >= done - 2 && ripple < 1 && (
          <div style={{ position: "absolute", left: 38 - 60 * ripple, top: 38 - 60 * ripple, width: 120 * ripple, height: 120 * ripple, borderRadius: 999, border: `3px solid rgba(255,255,255,${0.5 * (1 - ripple)})` }} />
        )}
      </div>
    </div>
  );
}

function fmt(s: number) {
  const m = Math.floor(s / 60);
  const r = Math.floor(s % 60);
  return `${m}:${String(r).padStart(2, "0")}`;
}

/** The rest timer: born from the plate's ring, then it runs down and folds into a single dot. */
function RestRing({ f }: { f: number }) {
  const land = spring({ frame: f - T.log, fps: 60, config: SPRING.camera, durationInFrames: 46 });
  const run = prog(f, REST_START, GO, EASE.standard);
  const fold = prog(f, 410, 420, EASE.in);
  const x = mix(mix(960, RING.x, land), DOT.x, fold);
  const y = mix(mix(540, RING.y, land), DOT.y, fold);
  const r = mix(mix(RING.startR, RING.r, land), DOT.r, fold);
  const stroke = mix(mix(8 * (RING.startR / RING.r) * 0.55, 10, land), DOT.r * 2, fold);
  const C = 2 * Math.PI * r;
  const goFlash = 1 - prog(f, GO, GO + 18);
  const tick = cuesOf("rest").reduce((n, c) => (f >= c.frame ? n + 1 : n), 0);
  const label = f < REST_START ? "1:30" : f >= GO ? "GO" : fmt(90 * (1 - run));
  const textIn = prog(f, T.log + 10, T.log + 34, EASE.out) * (1 - prog(f, 409, 415));
  return (
    <>
      <svg style={{ position: "absolute", left: 0, top: 0 }} width={1920} height={1080}>
        <circle cx={x} cy={y} r={r} fill="none" stroke="#26320C" strokeWidth={stroke} />
        <circle
          cx={x}
          cy={y}
          r={r}
          fill={fold > 0.6 ? COLOR.lime : "none"}
          stroke={COLOR.lime}
          strokeWidth={stroke}
          strokeLinecap="round"
          strokeDasharray={`${C * (fold > 0 ? 1 : 1 - run * 0.999)} ${C}`}
          transform={`rotate(-90 ${x} ${y})`}
          style={{ filter: `drop-shadow(0 0 ${10 + 30 * goFlash * (f >= GO ? 1 : 0)}px ${lime(0.55)})` }}
        />
      </svg>
      <div style={{ position: "absolute", left: x - 200, top: y - 70, width: 400, textAlign: "center", opacity: textIn, transform: `scale(${1 + (f >= GO ? 0.12 * goFlash : 0)})` }}>
        <div style={{ fontSize: 92, fontWeight: 700, color: f >= GO ? COLOR.lime : COLOR.ink, letterSpacing: "-0.04em", lineHeight: 1, fontVariantNumeric: "tabular-nums" }}>{label}</div>
        <div style={{ fontSize: 22, fontWeight: 600, letterSpacing: "0.18em", color: COLOR.soft, marginTop: 12 }}>{tick > 0 && f < GO ? `${4 - tick}` : "REST"}</div>
      </div>
    </>
  );
}

/** Act II: the session. Prefilled sets get ticked on the 8ths, the last one is a record, the timer runs. */
export function LogAct({ frame: f }: { frame: number }) {
  const head = f >= 390 ? exit(f, 390, { lift: 20 }) : enter(f, 246, { rise: 24 });
  return (
    <AbsoluteFill style={{ fontFamily: FONT, background: `radial-gradient(70% 70% at 60% 55%, #141712 0%, ${COLOR.deep} 100%)` }}>
      <div style={{ position: "absolute", left: 96, top: 92 }}>
        <Words lines={["Every set.", "*Logged."]} frame={f} start={262} end={386} size={96} />
      </div>
      <div style={{ position: "absolute", left: LEFT, top: TOP - 160, ...head }}>
        <div style={{ fontSize: 54, fontWeight: 700, color: COLOR.ink, letterSpacing: "-0.03em" }}>Bench Press</div>
        <div style={{ display: "flex", fontSize: 19, fontWeight: 600, letterSpacing: "0.14em", color: COLOR.faint, marginTop: 28, position: "relative", width: 1000, height: 24 }}>
          {(["SET", "PREVIOUS", "KG", "REPS"] as const).map((h, k) => (
            <span key={h} style={{ position: "absolute", left: [0, COL.prev, COL.kg + 62, COL.reps + 36][k] }}>{h}</span>
          ))}
          <span style={{ position: "absolute", left: COL.check + 26 }}>
            <IconCheck size={22} stroke={2.6} />
          </span>
        </div>
      </div>
      {ROWS.map((_, i) => (
        <Row key={i} f={f} i={i} />
      ))}
      <RestRing f={f} />
    </AbsoluteFill>
  );
}
