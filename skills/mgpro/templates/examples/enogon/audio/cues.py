"""
Enogon v2 cue list, read from src/events.json (written from the picture's own code by
scripts/events.ts). After the review of v1: few effects, all recorded (mouse clicks, paper and
wood thuds, recorded swishes), no pops, dings or synth bells; the music carries the rest; musical
moments are real notes on sampled instruments in the score's key ("notes" cues).

    python3 audio/cues.py
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
E = json.loads((ROOT / "src" / "events.json").read_text())
F = E["F"]

# Story clicks (the actions the film turns on) must read clearly over the music: about 6 dB
# above the bed around them, checked with the measurement in the release notes.
GAIN = float(__import__("os").environ.get("CLICK_GAIN", "8.0"))

# Three different CC0 mouse click recordings, rotated without repeats (references/sfx-selection.md).
CLICKS = ["remotion-cc0/mouse-click.wav", "sfx/found/freesound_683099_click.wav", "sfx/found/freesound_213004_click.wav"]

cues = []


def add(frame, sound, weight="support", **extra):
    cues.append({"frame": int(round(frame)), "sound": sound, "weight": weight, **extra})


# The upload: a click to grab, the paper sliding, the sheet landing on the table.
add(F["grab"], "click", "support", story=True, file=CLICKS, gain=GAIN)
add((F["grab"] + F["release"]) / 2, "swish", "ambient", seconds=0.5)
add(F["sheetLand"] - 6, "card", "support", size=0.35)

# The AI reads: no effects on the line; the rooms fill as marimba notes rising through F major.
scale = [65, 67, 69, 72, 74, 77, 79, 81, 84, 86]
for i, a in enumerate(E["ROOM_AT"]):
    add(a + 1, "notes", "support", family="keys", kind="marimba", notes=[scale[i]], v=0.38 + 0.03 * i, d=0.5)

# Storeys land with wood, heavier each time; the roof lands with the build's downbeat in the music.
add(F["tilt"] + 30, "swish", "ambient", seconds=0.6)
for n, key in enumerate(["land1", "land2", "land3"]):
    add(F[key], "card", "support", size=0.45 + 0.12 * n)
add(F["roofLand"], "card", "support", size=0.8)

# Edit: the wall click, the field click, three keys typed.
add(F["click"], "click", "support", story=True, file=CLICKS, gain=GAIN)
add(F["field"], "click", "support", story=True, file=[CLICKS[0], CLICKS[2]], gain=GAIN * 1.3)
for k in range(3):
    add(F["type"] + k * 5, "tap", "support", story=True, file=["kenney-ui-audio/Audio/click1.ogg", "kenney-ui-audio/Audio/click3.ogg", "kenney-ui-audio/Audio/click1.ogg"][k], gain=GAIN * 0.72)

# Export: the press; the result lands as a chord in the music, not a ding.
add(F["press"], "click", "support", story=True, file=CLICKS, gain=GAIN)
add(F["done"], "notes", "support", family="keys", kind="vibes", notes=[69, 72, 77], spread=0.0, v=0.55, d=1.2)

# The box: the net is laid (a soft swish), four sides fold up (paper thuds), the lid closes (wood).
add(F["net"] + 4, "swish", "ambient", seconds=0.4)
for k in range(4):
    add(F["fold"] + k * 7 + 14, "card", "ambient", size=0.3)
add(F["lid"] + 10, "card", "support", size=0.65)

# The sonic logo lands on the logo frame: C F A rising on vibes over a felt Fmaj7.
add(F["logo"] - 18, "notes", "hero", family="keys", kind="vibes", notes=[72, 77, 81], spread=0.15, v=0.8, d=1.6, accent=[0.8, 0.9, 1.0])
add(F["logo"] + 12, "notes", "hero", family="keys", kind="felt", notes=[53, 57, 60, 64], spread=0.0, v=0.6, d=3.0)

cues.sort(key=lambda c: c["frame"])
(ROOT / "src" / "cues.json").write_text(json.dumps(cues, indent=1))
print(len(cues), "cues")
