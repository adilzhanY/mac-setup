// Dumps every picture event frame, from the same code the picture uses, for audio/cues.py.
import { writeFileSync } from "node:fs";
import { F } from "../src/timeline";
import { DOOR_AT, INNER_AT, OUTER_AT, ROOM_AT } from "../src/PlanLayer";
import { SECTION } from "../src/lib";

writeFileSync("src/events.json", JSON.stringify({ F, OUTER_AT, INNER_AT, DOOR_AT, ROOM_AT, SECTION }, null, 1));
console.log("events written");
