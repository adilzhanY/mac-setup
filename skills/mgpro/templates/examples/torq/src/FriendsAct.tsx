import { IconFlame } from "@tabler/icons-react";
import { AbsoluteFill } from "remotion";
import { Badge } from "./Badge";
import { Words } from "./kit";
import { COLOR, EASE, FONT, T, cueAt, cuesOf, enter, exit, lime, mix, prog, sp } from "./lib";

const LEFT = 790;
const WIDTH = 1030;
const TOP = 300;
const ROW_H = 118;
const BADGE = 84;

/** Where the medal lands at the cut: the badge of the "You" row, fourth place. */
export const YOU_BADGE = { x: LEFT + 92 + BADGE / 2, y: TOP + 3 * ROW_H + ROW_H / 2, size: BADGE };

const ROWS_IN = cuesOf("tick").filter((c) => c.frame >= T.friends).map((c) => c.frame);
const SWAPS = cuesOf("swap").map((c) => c.frame);
const COUNT_FROM = cuesOf("count")[0]!.frame;
const COUNT_TO = cuesOf("count").filter((c) => c.frame < T.streak).pop()!.frame;
const MESSAGE = cueAt("message");
const BLIPS = cuesOf("blip").map((c) => c.frame);
const STREAK_POP = cuesOf("pop").filter((c) => c.frame > T.streak)[0]!.frame;

interface Person {
  name: string;
  handle: string;
  tier: number;
  pts: number;
  lift: string;
  colour: string;
}

const PEOPLE: Person[] = [
  { name: "Maya", handle: "@maya.lifts", tier: 7, pts: 1402, lift: "Deadlift 210 kg", colour: "#9C86E8" },
  { name: "Alex", handle: "@alexk", tier: 6, pts: 1266, lift: "Squat 180 kg", colour: "#5AC8A0" },
  { name: "Sam", handle: "@samtrains", tier: 6, pts: 1240, lift: "Bench 125 kg", colour: "#F0A742" },
  { name: "You", handle: "@adilzhan", tier: 7, pts: 1180, lift: "Bench 140 kg", colour: COLOR.lime },
  { name: "Jonas", handle: "@jonas", tier: 5, pts: 1051, lift: "Squat 160 kg", colour: "#6FA9E8" },
];

/** Each row's place over time: you pass Sam on the first swap and Alex on the second. */
function place(i: number, f: number) {
  const a = sp(f, SWAPS[0]!, "settle");
  const b = sp(f, SWAPS[1]!, "settle");
  if (i === 3) return 3 - a - b;
  if (i === 2) return 2 + a;
  if (i === 1) return 1 + b;
  return i;
}

function Row({ f, i }: { f: number; i: number }) {
  const p = PEOPLE[i]!;
  const me = i === 3;
  const y = TOP + place(i, f) * ROW_H;
  const pts = me ? Math.round(mix(1180, 1284, prog(f, COUNT_FROM, COUNT_TO + 2, EASE.standard))) : p.pts;
  const rank = Math.round(place(i, f)) + 1;
  // The medal from the drop becomes this badge, so the "You" row is there from the first frame.
  const style = me ? {} : f >= 1148 + i * 2 ? exit(f, 1148 + i * 2, { lift: 22, blur: 10 }) : enter(f, ROWS_IN[i === 4 ? 3 : i]!, { rise: 26 });
  const meOut = me && f >= 1154 ? exit(f, 1154, { lift: 22, blur: 10 }) : {};
  const meIn = me ? enter(f, T.friends - 2, { rise: 0, blur: 0, scale: 1 }) : {};
  const lifting = me ? Math.max(sp(f, SWAPS[0]!, "pop") * (1 - prog(f, SWAPS[0]! + 14, SWAPS[0]! + 30)), sp(f, SWAPS[1]!, "pop") * (1 - prog(f, SWAPS[1]! + 14, SWAPS[1]! + 30))) : 0;
  // A row being passed steps back for the moment the "You" row crosses it.
  const passed = i === 2 ? Math.sin(Math.PI * prog(f, SWAPS[0]!, SWAPS[0]! + 22)) : i === 1 ? Math.sin(Math.PI * prog(f, SWAPS[1]!, SWAPS[1]! + 22)) : 0;
  const promoted = i === 1 && f >= MESSAGE + 8;
  const promo = i === 1 ? sp(f, MESSAGE + 8, "pop") : 0;
  const bump = me && f >= COUNT_FROM && f <= COUNT_TO + 4 ? 1 + 0.05 * Math.abs(Math.sin((f - COUNT_FROM) * 0.9)) : 1;
  const detail = me ? enter(f, T.friends + 6, { rise: 10 }) : {};
  return (
    <div style={{ position: "absolute", left: LEFT, top: y, width: WIDTH, height: ROW_H, zIndex: me ? 2 : 1, ...style, ...meOut }}>
      <div style={{ position: "absolute", inset: 0, transform: `scale(${(1 + 0.025 * lifting) * (1 - 0.03 * passed)})`, transformOrigin: "50% 50%", opacity: 1 - 0.55 * passed, filter: passed > 0.05 ? `blur(${2 * passed}px)` : undefined }}>
        {me && <div style={{ position: "absolute", inset: "8px -22px", borderRadius: 12, background: lime(0.07 + 0.08 * lifting), boxShadow: `inset 0 0 0 1.5px ${lime(0.32 + 0.4 * lifting)}, 0 ${20 * lifting}px ${50 * lifting}px -10px rgba(0,0,0,.6)`, ...detail }} />}
        {!me && i < 4 && <div style={{ position: "absolute", left: 0, right: 0, bottom: 0, height: 1, background: COLOR.hair }} />}
        <div style={{ position: "absolute", left: 0, top: 0, height: ROW_H, display: "flex", alignItems: "center", fontSize: 32, fontWeight: 700, color: me ? COLOR.lime : COLOR.faint, width: 60, fontVariantNumeric: "tabular-nums", ...detail }}>{rank}</div>
        <div style={{ position: "absolute", left: 92, top: (ROW_H - BADGE) / 2, ...meIn }}>
          <div style={{ transform: promoted ? `scale(${0.6 + 0.4 * promo})` : undefined, filter: promoted && promo < 0.99 ? `drop-shadow(0 0 ${20 * (1 - promo)}px ${COLOR.lime})` : undefined }}>
            <Badge tier={promoted ? 7 : p.tier} size={BADGE} id={`r${i}`} />
          </div>
        </div>
        <div style={{ position: "absolute", left: 210, top: 22, ...detail }}>
          <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
            <div style={{ width: 38, height: 38, borderRadius: 999, background: p.colour, color: COLOR.limeInk, fontSize: 20, fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center" }}>{p.name[0]}</div>
            <div style={{ fontSize: 36, fontWeight: 700, color: COLOR.ink, letterSpacing: "-0.02em" }}>{p.name}</div>
            <div style={{ fontSize: 24, color: COLOR.faint, fontWeight: 500 }}>{p.handle}</div>
          </div>
          <div style={{ fontSize: 24, color: COLOR.soft, marginTop: 8, marginLeft: 52 }}>{p.lift}</div>
        </div>
        <div style={{ position: "absolute", right: 0, top: 0, height: ROW_H, display: "flex", alignItems: "center", gap: 10, ...detail }}>
          <span style={{ fontSize: 44, fontWeight: 700, color: me ? COLOR.lime : COLOR.ink, fontVariantNumeric: "tabular-nums", letterSpacing: "-0.02em", transform: `scale(${bump})`, display: "inline-block" }}>{pts.toLocaleString("en-US")}</span>
          <span style={{ fontSize: 24, color: COLOR.faint, fontWeight: 600 }}>pts</span>
        </div>
      </div>
    </div>
  );
}

/** The app's You / Friends / Arena switch, with Friends lit. */
function Segments({ f }: { f: number }) {
  const s = f >= 1146 ? exit(f, 1146) : enter(f, T.friends + 4, { rise: 14 });
  return (
    <div style={{ position: "absolute", left: LEFT, top: TOP - 110, display: "flex", gap: 6, padding: 6, borderRadius: 12, background: COLOR.surface, boxShadow: `inset 0 0 0 1.5px ${COLOR.line}`, ...s }}>
      {["You", "Friends", "Arena"].map((l) => (
        <div key={l} style={{ padding: "12px 34px", borderRadius: 8, fontSize: 26, fontWeight: 700, background: l === "Friends" ? COLOR.lime : "transparent", color: l === "Friends" ? COLOR.limeInk : COLOR.soft }}>{l}</div>
      ))}
    </div>
  );
}

/** A push from a friend's promotion, dropping in from the top like the real one. */
function Notification({ f }: { f: number }) {
  if (f < MESSAGE - 14) return null;
  const t = sp(f, MESSAGE - 14, "settle");
  const o = f >= 1142 ? exit(f, 1142, { lift: 40 }) : {};
  return (
    <div
      style={{
        position: "absolute",
        left: 96,
        top: mix(-160, 96, t),
        width: 600,
        padding: "22px 26px",
        borderRadius: 16,
        background: "linear-gradient(180deg, rgba(34,38,31,.92), rgba(21,23,20,.92))",
        boxShadow: `inset 0 1px 0 rgba(255,255,255,.08), inset 0 0 0 1px ${COLOR.line}, 0 30px 70px -20px rgba(0,0,0,.8)`,
        display: "flex",
        gap: 20,
        alignItems: "center",
        ...o,
      }}
    >
      <Badge tier={7} size={72} id="note" />
      <div>
        <div style={{ fontSize: 20, color: COLOR.faint, fontWeight: 600, letterSpacing: "0.06em" }}>TORQ · NOW</div>
        <div style={{ fontSize: 30, color: COLOR.ink, fontWeight: 700, marginTop: 4, letterSpacing: "-0.01em" }}>
          Alex reached <span style={{ color: COLOR.lime }}>Elite</span>
        </div>
      </div>
    </div>
  );
}

const DAYS = ["M", "T", "W", "T", "F", "S", "S"];

/** The week fills in on the 8ths and the streak ticks over. */
function Streak({ f }: { f: number }) {
  if (f < T.streak) return null;
  const roll = prog(f, STREAK_POP, STREAK_POP + 12, EASE.out);
  const drift = 1 + 0.02 * prog(f, T.streak, T.payoff, EASE.standard);
  return (
    <AbsoluteFill style={{ alignItems: "center", transform: `scale(${drift})` }}>
      <div style={{ position: "absolute", top: 180, width: "100%", display: "flex", justifyContent: "center" }}>
        <Words lines={["Show *up."]} frame={f} start={T.streak + 4} size={130} align="center" />
      </div>
      <div style={{ position: "absolute", top: 470, display: "flex", gap: 54 }}>
        {DAYS.map((d, i) => {
          const s = enter(f, T.streak + 2 + i * 3, { rise: 20 });
          const on = sp(f, BLIPS[i]!, "pop");
          const glow = 1 - prog(f, BLIPS[i]!, BLIPS[i]! + 24);
          return (
            <div key={i} style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 22, ...s }}>
              <div style={{ position: "relative", width: 104, height: 104 }}>
                <div style={{ position: "absolute", inset: 0, borderRadius: 999, background: COLOR.page2, boxShadow: `inset 0 0 0 2px ${COLOR.line}` }} />
                <div style={{ position: "absolute", inset: 0, borderRadius: 999, background: COLOR.lime, transform: `scale(${on})`, boxShadow: `0 0 ${46 * glow}px ${lime(0.7)}` }} />
              </div>
              <div style={{ fontSize: 28, fontWeight: 700, color: f >= BLIPS[i]! ? COLOR.ink : COLOR.faint }}>{d}</div>
            </div>
          );
        })}
      </div>
      <div style={{ position: "absolute", top: 760, display: "flex", alignItems: "center", gap: 16, padding: "18px 38px 18px 28px", borderRadius: 999, background: lime(0.12), boxShadow: `inset 0 0 0 1.5px ${lime(0.4)}`, color: COLOR.lime, ...enter(f, T.streak + 26, { rise: 16 }) }}>
        <IconFlame size={46} stroke={2.2} />
        <div style={{ position: "relative", width: 64, height: 60, overflow: "hidden", fontSize: 50, fontWeight: 700, lineHeight: "60px", fontVariantNumeric: "tabular-nums" }}>
          <div style={{ position: "absolute", inset: 0, transform: `translateY(${-roll * 60}px)`, opacity: 1 - roll }}>12</div>
          <div style={{ position: "absolute", inset: 0, transform: `translateY(${(1 - roll) * 60}px)`, opacity: roll }}>13</div>
        </div>
        <div style={{ fontSize: 40, fontWeight: 600, color: COLOR.ink }}>day streak</div>
      </div>
    </AbsoluteFill>
  );
}

/** Act V: together. The board, the overtake, a friend's promotion, then the streak. */
export function FriendsAct({ frame: f }: { frame: number }) {
  return (
    <AbsoluteFill style={{ fontFamily: FONT, background: `radial-gradient(80% 80% at 70% 50%, #121510 0%, ${COLOR.deep} 80%)` }}>
      {f < T.streak && (
        <>
          <div style={{ position: "absolute", left: 96, top: 420 }}>
            <Words lines={["Climb with", "*friends."]} frame={f} start={T.friends + 10} end={1144} size={112} />
          </div>
          <Segments f={f} />
          {[0, 1, 2, 4, 3].map((i) => (
            <Row key={i} f={f} i={i} />
          ))}
          <Notification f={f} />
        </>
      )}
      <Streak f={f} />
    </AbsoluteFill>
  );
}
