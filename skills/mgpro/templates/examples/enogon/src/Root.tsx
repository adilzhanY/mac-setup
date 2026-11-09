import { Composition } from "remotion";
import { Film } from "./Film";
import { LENGTH } from "./lib";

export function Root() {
  return <Composition id="Film" component={Film} durationInFrames={LENGTH} fps={60} width={1920} height={1080} />;
}
