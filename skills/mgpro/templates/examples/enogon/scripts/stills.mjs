// Render chosen frames as PNG stills from one bundle: node scripts/stills.mjs 60 400 900 ...
import { bundle } from "@remotion/bundler";
import { renderStill, selectComposition } from "@remotion/renderer";
import path from "node:path";

const frames = process.argv.slice(2).map(Number);
const serveUrl = await bundle({ entryPoint: path.resolve("src/index.ts") });
const composition = await selectComposition({ serveUrl, id: "Film", chromiumOptions: { gl: "swangle" } });
await Promise.all(
  frames.map((frame) =>
    renderStill({ serveUrl, composition, frame, output: `out/stills/${String(frame).padStart(4, "0")}.png`, chromiumOptions: { gl: "swangle" }, scale: Number(process.env.SCALE ?? 0.5) }),
  ),
);
console.log("done", frames.length);
