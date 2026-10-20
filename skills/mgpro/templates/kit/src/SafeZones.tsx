import { AbsoluteFill, getInputProps, useVideoConfig } from "remotion";
import { FORMATS, safeBox } from "./formats";

/**
 * Review guides: the platform's own overlays (approximate, measured from the apps) and the safe
 * box, drawn over the film only when rendered with --props='{"guides":"tiktok"}' (or reels,
 * shorts, snapchat, safe). Never on in a final render.
 */
const OVERLAYS: Record<string, { label: string; x: number; y: number; w: number; h: number }[]> = {
  tiktok: [
    { label: "caption, account, sound", x: 0, y: 1213, w: 1080, h: 707 },
    { label: "like, comment, share", x: 838, y: 560, w: 242, h: 900 },
    { label: "tabs", x: 0, y: 0, w: 1080, h: 254 },
  ],
  reels: [
    { label: "caption, account, audio", x: 0, y: 1248, w: 1080, h: 672 },
    { label: "actions", x: 918, y: 900, w: 162, h: 700 },
    { label: "header", x: 0, y: 0, w: 1080, h: 269 },
  ],
  shorts: [
    { label: "title, channel, subscribe", x: 0, y: 1539, w: 1080, h: 381 },
    { label: "actions", x: 879, y: 700, w: 201, h: 900 },
    { label: "header", x: 0, y: 0, w: 1080, h: 241 },
  ],
  snapchat: [
    { label: "swipe up", x: 0, y: 1536, w: 1080, h: 384 },
    { label: "header", x: 0, y: 0, w: 1080, h: 230 },
  ],
};

export function SafeZones() {
  const { width, height } = useVideoConfig();
  const guides = (getInputProps() as { guides?: string }).guides;
  if (!guides) return null;
  const format = Object.values(FORMATS).find((f) => f.width === width && f.height === height) ?? FORMATS.landscape!;
  const box = safeBox(format);
  return (
    <AbsoluteFill style={{ pointerEvents: "none", fontFamily: "system-ui, sans-serif" }}>
      {(OVERLAYS[guides] ?? []).map((o) => (
        <div key={o.label} style={{ position: "absolute", left: o.x, top: o.y, width: o.w, height: o.h, background: "rgba(255,40,80,0.28)", border: "2px solid rgba(255,40,80,0.9)", color: "#fff", fontSize: 26, padding: 8, boxSizing: "border-box" }}>
          {o.label}
        </div>
      ))}
      <div style={{ position: "absolute", left: box.x, top: box.y, width: box.w, height: box.h, border: "3px dashed rgba(80,255,160,0.9)", boxSizing: "border-box" }} />
    </AbsoluteFill>
  );
}
