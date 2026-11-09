import { useEffect, useState } from "react";
import { continueRender, delayRender, staticFile } from "remotion";

const FACES: [string, string, string][] = [
  ["Inter Tight", "fonts/InterTight.ttf", "100 900"],
  ["Tektur", "fonts/Tektur.ttf", "400 900"],
  ["IBM Plex Mono", "fonts/IBMPlexMono-Regular.ttf", "400"],
  ["IBM Plex Mono", "fonts/IBMPlexMono-Medium.ttf", "500"],
  ["IBM Plex Mono", "fonts/IBMPlexMono-SemiBold.ttf", "600"],
];

let loaded: Promise<unknown> | null = null;

/** Loads the brand fonts before the first frame is captured. */
export function useFonts() {
  const [handle] = useState(() => delayRender("fonts"));
  useEffect(() => {
    loaded ??= Promise.all(
      FACES.map(([family, file, weight]) => {
        const face = new FontFace(family, `url(${staticFile(file)})`, { weight });
        document.fonts.add(face);
        return face.load();
      }),
    );
    loaded.then(() => continueRender(handle)).catch((e) => {
      console.error(e);
      continueRender(handle);
    });
  }, [handle]);
}
