import { Composition } from "remotion";
import "@fontsource-variable/space-grotesk";
import "@fontsource-variable/geist-mono";
import { Film } from "./Film";
import { LENGTH } from "./lib";

export function Root() {
  return <Composition id="Torq" component={Film} durationInFrames={LENGTH} fps={60} width={1920} height={1080} />;
}
