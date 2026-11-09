import { AbsoluteFill, Audio, staticFile, useCurrentFrame } from "remotion";
import { C } from "./brand";
import { MacCursor } from "./Cursor";
import { CLICKS, PATH, TRACK, cardRect } from "./cursorTrack";
import { useFonts } from "./Fonts";
import { Grain } from "./kit";
import { Overlay } from "./Overlay";
import { PlanLayer } from "./PlanLayer";
import { Scene3D } from "./Scene3D";
import { F, camAt } from "./timeline";

const HAS_AUDIO = true;

export function Film() {
  useFonts();
  const f = useCurrentFrame();
  const cam = camAt(f);
  return (
    <AbsoluteFill style={{ background: C.paper, overflow: "hidden" }}>
      <PlanLayer frame={f} cam={cam} cardRect={cardRect(F.release)} />
      <Scene3D frame={f} cam={cam} />
      <Overlay frame={f} cam={cam} />
      <MacCursor track={TRACK} frame={f} path={PATH} clicks={CLICKS} />
      {HAS_AUDIO && <Audio src={staticFile("film.wav")} />}
      <Grain frame={f} opacity={0.03} />
    </AbsoluteFill>
  );
}
