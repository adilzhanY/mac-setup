import { AbsoluteFill, Audio, staticFile, useCurrentFrame } from "remotion";
import { Grain } from "./kit";
import { COLOR } from "./lib";
import { SafeZones } from "./SafeZones";

/**
 * The whole film reads ONE global frame. Each act renders only inside its section of the form
 * (T.<section> from music.json) and gets the absolute frame, so every timing in the acts and in
 * cues.json is in film frames. Lay scenes out from useVideoConfig() so every format works.
 */
export function Film() {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{ background: COLOR.stage }}>
      {/* {f >= T.cold && f < T.verse && <ColdOpen frame={f} />} */}
      <Audio src={staticFile("film.wav")} />
      <Grain frame={f} opacity={0.05} />
      <SafeZones />
    </AbsoluteFill>
  );
}
