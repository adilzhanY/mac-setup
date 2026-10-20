import { Composition } from "remotion";
// The product's own fonts, as fontsource variable packages (add them to package.json).
// import "@fontsource-variable/<brand-font>";
// import "@fontsource-variable/geist-mono";
import { Film } from "./Film";
import { FORMATS } from "./formats";
import { LENGTH } from "./lib";

/** One composition per destination size: render Film-vertical, Film-feed45 and so on. Delete the ones the film does not need. */
export function Root() {
  return (
    <>
      {Object.values(FORMATS).map((f) => (
        <Composition key={f.id} id={`Film-${f.id}`} component={Film} durationInFrames={LENGTH} fps={60} width={f.width} height={f.height} />
      ))}
    </>
  );
}
