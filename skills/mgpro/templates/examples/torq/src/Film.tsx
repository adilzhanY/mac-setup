import { AbsoluteFill, Audio, staticFile, useCurrentFrame } from "remotion";
import { BarAct } from "./BarAct";
import { LogAct } from "./LogAct";
import { EngineAct } from "./EngineAct";
import { ForgeAct } from "./ForgeAct";
import { FriendsAct } from "./FriendsAct";
import { PayoffAct } from "./PayoffAct";
import { EndAct } from "./EndAct";
import { Grain } from "./kit";
import { COLOR, T } from "./lib";

export function Film() {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{ background: COLOR.deep }}>
      {f < T.log && <BarAct frame={f} />}
      {f >= T.log && f < T.engine && <LogAct frame={f} />}
      {f >= T.engine && f < T.forge && <EngineAct frame={f} />}
      {f >= T.forge && f < T.friends && <ForgeAct frame={f} />}
      {f >= T.friends && f < T.payoff && <FriendsAct frame={f} />}
      {f >= T.payoff && f < T.end && <PayoffAct frame={f} />}
      {f >= T.end && <EndAct frame={f} />}
      <Audio src={staticFile("torq.wav")} />
      <Grain frame={f} opacity={0.06} />
    </AbsoluteFill>
  );
}
