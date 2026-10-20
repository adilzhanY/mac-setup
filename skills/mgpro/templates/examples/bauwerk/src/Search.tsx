import { MapPin, Search as SearchIcon } from "lucide-react";
import { COLOR, EASE, FONT, clamp, cuesOf, enter, mix, prog, sp } from "./lib";
import { MacCursor } from "./Cursor";
import type { CursorTrack } from "./Cursor";

const ADDRESS = "Methfesselstraße 8";
const KEYS = cuesOf("key");

/** The search pill, centred, and where things in it are on the screen. */
export const PILL = { x: 960 - 410, y: 420, w: 820, h: 96 };
const CARD = { x: PILL.x, y: PILL.y + PILL.h + 16, w: PILL.w };
const ROW = { x: CARD.x + 22, y: CARD.y + 14, h: 92 };
/** The result row's pin badge centre: it becomes the map pin. */
export const BADGE = { x: ROW.x + 8 + 30, y: ROW.y + ROW.h / 2 };

const CLICK_FIELD = 60;
const CLICK_RESULT = 180;

const track: CursorTrack = {
  stops: [
    { f: 0, x: 1500, y: 930 },
    { f: 56, x: PILL.x + 330, y: PILL.y + 52, arc: 0.14 },
    { f: 150, x: PILL.x + 520, y: PILL.y + 120 },
    { f: 174, x: ROW.x + 300, y: ROW.y + 50, arc: -0.1 },
  ],
  shapes: [
    { f: 44, shape: "text" },
    { f: 150, shape: "arrow" },
    { f: 166, shape: "hand" },
  ],
  clicks: [CLICK_FIELD, CLICK_RESULT],
  visible: [
    { f: 14, on: true },
    { f: 66, on: false },
    { f: 148, on: true },
    { f: 190, on: false },
  ],
};

/**
 * Act I: a floating search pill opens out of a dot, the cursor clicks it, the address types in
 * letter by letter, a result unfolds, and the click sends its pin down to the map.
 */
export function Search({ frame }: { frame: number }) {
  if (frame > 230) return null;
  // The pill opens: width leads, height follows four frames later (stretch and settle).
  const wOpen = sp(frame, 4, "pop");
  const hOpen = sp(frame, 8, "settle");
  const typed = KEYS.filter((k) => frame >= k.frame).length;
  const focus = sp(frame, CLICK_FIELD, "settle");
  const cardIn = sp(frame, 144, "settle");
  const away = prog(frame, CLICK_RESULT + 2, CLICK_RESULT + 18, EASE.in);
  const hover = prog(frame, 168, 174);
  const pinFly = prog(frame, CLICK_RESULT + 2, 210, EASE.inOut);
  const caretOn = typed === 0 || frame - (KEYS[typed - 1]?.frame ?? 0) > 18 ? Math.floor(frame / 18) % 2 === 0 : true;

  const pillW = Math.max(96, PILL.w * wOpen);
  const pillH = PILL.h * (0.6 + 0.4 * hOpen);
  return (
    <div style={{ position: "absolute", inset: 0, fontFamily: FONT }}>
      <div
        style={{
          position: "absolute",
          left: 0,
          top: 0,
          width: 1920,
          height: 1080,
          opacity: 1 - away,
          filter: away > 0 ? `blur(${away * 12}px)` : undefined,
          transform: `scale(${1 - 0.06 * away})`,
          transformOrigin: `${BADGE.x}px ${BADGE.y}px`,
        }}
      >
        {/* The pill. */}
        <div
          style={{
            position: "absolute",
            left: 960 - pillW / 2,
            top: PILL.y + (PILL.h - pillH) / 2,
            width: pillW,
            height: pillH,
            borderRadius: 999,
            background: "linear-gradient(180deg, rgba(255,255,255,.92), rgba(255,255,255,.78))",
            backdropFilter: "blur(30px) saturate(180%)",
            boxShadow: `inset 0 1px 0 rgba(255,255,255,1), 0 0 0 ${1 + focus * 2}px rgba(2,78,123,${0.06 + focus * 0.5}), 0 0 0 ${focus * 9}px rgba(2,78,123,${0.1 * focus}), 0 34px 80px -24px rgba(13,33,55,.4), 0 2px 6px rgba(13,33,55,.06)`,
            opacity: clamp(wOpen * 3),
            overflow: "hidden",
          }}
        >
          <div style={{ position: "absolute", left: 34, top: pillH / 2 - 17, transform: `scale(${sp(frame, 14, "pop")})`, color: focus > 0.5 ? COLOR.navy : COLOR.muted }}>
            <SearchIcon size={34} strokeWidth={2.2} />
          </div>
          {/* Placeholder, sliding away on focus. */}
          <div
            style={{
              position: "absolute",
              left: 90,
              top: pillH / 2 - 22,
              fontSize: 34,
              color: "#8b96a3",
              whiteSpace: "nowrap",
              opacity: clamp((frame - 18) / 12) * (1 - focus),
              transform: `translateY(${-focus * 14}px)`,
              filter: `blur(${focus * 6}px)`,
            }}
          >
            Search an address
          </div>
          {/* The typed address, each letter rising out of a blur. */}
          <div style={{ position: "absolute", left: 90, top: pillH / 2 - 23, fontSize: 36, fontWeight: 500, color: COLOR.ink, whiteSpace: "pre", letterSpacing: "-0.01em", display: "flex" }}>
            {ADDRESS.split("").map((ch, i) => {
              const k = KEYS[i];
              if (!k || frame < k.frame) return null;
              const t = prog(frame, k.frame, k.frame + 9, EASE.out);
              return (
                <span key={i} style={{ display: "inline-block", opacity: t, transform: `translateY(${(1 - t) * 10}px)`, filter: t < 1 ? `blur(${(1 - t) * 5}px)` : undefined }}>
                  {ch}
                </span>
              );
            })}
            {focus > 0.2 && <span style={{ width: 2.5, height: 40, marginLeft: 2, marginTop: 2, background: COLOR.navy, borderRadius: 2, opacity: caretOn ? 1 : 0 }} />}
          </div>
        </div>
        {/* The result card. */}
        {frame >= 144 && (
          <div
            style={{
              position: "absolute",
              left: CARD.x,
              top: CARD.y,
              width: CARD.w,
              height: 14 + (ROW.h + 2) * 2 * cardIn + 12 * cardIn,
              borderRadius: 30,
              overflow: "hidden",
              background: "linear-gradient(180deg, rgba(255,255,255,.9), rgba(255,255,255,.76))",
              backdropFilter: "blur(30px) saturate(180%)",
              boxShadow: "inset 0 1px 0 rgba(255,255,255,1), 0 34px 80px -24px rgba(13,33,55,.38)",
              opacity: clamp(cardIn * 2),
              transform: `translateY(${(1 - cardIn) * -14}px)`,
            }}
          >
            {[
              { title: "Methfesselstraße 8", sub: "10965 Berlin, Kreuzberg", chip: "LoD2 · 5 floors", start: 146, dim: 1 },
              { title: "Methfesselstraße 18", sub: "10965 Berlin, Kreuzberg", chip: "", start: 151, dim: 0.45 },
            ].map((r, i) => {
              const st = enter(frame, r.start, { rise: 10, blur: 6 });
              return (
                <div
                  key={i}
                  style={{
                    position: "absolute",
                    left: 14,
                    right: 14,
                    top: 14 + i * (ROW.h + 2),
                    height: ROW.h,
                    borderRadius: 20,
                    background: i === 0 ? `rgba(2,78,123,${0.07 * hover})` : undefined,
                    display: "flex",
                    alignItems: "center",
                    gap: 20,
                    padding: "0 16px",
                    ...st,
                    opacity: st.opacity * r.dim,
                    transform: `${st.transform} scale(${i === 0 && frame >= CLICK_RESULT && frame < CLICK_RESULT + 8 ? 0.985 : 1})`,
                  }}
                >
                  <div
                    style={{
                      width: 60,
                      height: 60,
                      borderRadius: 999,
                      background: i === 0 ? COLOR.navy : "#dfe5ec",
                      color: i === 0 ? "white" : "#7b8794",
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      opacity: i === 0 && frame > CLICK_RESULT + 1 ? 0 : 1,
                    }}
                  >
                    <MapPin size={30} strokeWidth={2.2} />
                  </div>
                  <div style={{ flex: 1 }}>
                    <div style={{ fontSize: 31, fontWeight: 600, color: COLOR.ink, letterSpacing: "-0.015em" }}>{r.title}</div>
                    <div style={{ fontSize: 22, color: COLOR.muted, marginTop: 2 }}>{r.sub}</div>
                  </div>
                  {r.chip && (
                    <div style={{ fontSize: 19, fontWeight: 600, color: COLOR.navy, background: "rgba(2,78,123,.08)", padding: "7px 14px", borderRadius: 999 }}>{r.chip}</div>
                  )}
                </div>
              );
            })}
          </div>
        )}
      </div>
      {/* The pin badge leaves the row and flies to the building in the middle of the map. */}
      {frame > CLICK_RESULT && frame < 214 && (
        <div
          style={{
            position: "absolute",
            left: mix(BADGE.x, 960, pinFly) - 30,
            top: mix(BADGE.y, 540, pinFly) - 30 - Math.sin(Math.PI * pinFly) * 60,
            width: 60,
            height: 60,
            borderRadius: 999,
            background: COLOR.navy,
            color: "white",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            boxShadow: "0 16px 40px -8px rgba(2,78,123,.6)",
            transform: `scale(${1 + 0.25 * Math.sin(Math.PI * pinFly)})`,
          }}
        >
          <MapPin size={30} strokeWidth={2.2} />
        </div>
      )}
      <MacCursor track={track} frame={frame} />
    </div>
  );
}
