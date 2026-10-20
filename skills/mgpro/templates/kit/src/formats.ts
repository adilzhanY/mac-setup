/**
 * Frame sizes per destination (see references/destinations.md). Root registers one composition
 * per format the film needs; scenes lay out from useVideoConfig(), so another size is a re-layout,
 * not a crop. `safe` is the box where text, faces, the product and the mark must stay.
 */
export interface Format {
  id: string;
  width: number;
  height: number;
  /** Clear margins in pixels: interface chrome or broadcast safe area. */
  safe: { top: number; right: number; bottom: number; left: number };
  note: string;
}

const margin = (w: number, h: number, p: number) => ({ top: h * p, right: w * p, bottom: h * p, left: w * p });

export const FORMATS: Record<string, Format> = {
  landscape: { id: "landscape", width: 1920, height: 1080, safe: margin(1920, 1080, 0.05), note: "YouTube, website, X, LinkedIn, Google Play landscape, events" },
  tv: { id: "tv", width: 1920, height: 1080, safe: margin(1920, 1080, 0.05), note: "broadcast: text inside the central 90 percent" },
  vertical: { id: "vertical", width: 1080, height: 1920, safe: { top: 260, right: 242, bottom: 710, left: 64 }, note: "TikTok, Reels, Shorts, Snapchat, Stories: conservative union of their overlays" },
  feed45: { id: "feed45", width: 1080, height: 1350, safe: { top: 60, right: 60, bottom: 135, left: 60 }, note: "Facebook and Instagram feed, LinkedIn" },
  square: { id: "square", width: 1080, height: 1080, safe: margin(1080, 1080, 0.056), note: "feeds that do not take 4:5" },
  appstorePortrait: { id: "appstorePortrait", width: 886, height: 1920, safe: margin(886, 1920, 0.04), note: "App Store iPhone preview, portrait (render at 30 fps, real screen captures only)" },
  appstoreLandscape: { id: "appstoreLandscape", width: 1920, height: 886, safe: margin(1920, 886, 0.04), note: "App Store iPhone preview, landscape" },
  playPortrait: { id: "playPortrait", width: 1080, height: 1920, safe: margin(1080, 1920, 0.04), note: "Google Play portrait preview (80 percent real app)" },
};

/** The safe box as a rectangle, for placing copy: x, y, width, height. */
export const safeBox = (f: Format) => ({
  x: f.safe.left,
  y: f.safe.top,
  w: f.width - f.safe.left - f.safe.right,
  h: f.height - f.safe.top - f.safe.bottom,
});
