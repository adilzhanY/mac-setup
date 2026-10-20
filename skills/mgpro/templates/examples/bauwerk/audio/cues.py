"""
The one timing source of the commercial: every sound and every timed event, in frames at 60 fps
(120 BPM: a beat is 30 frames, a 16th 7.5). The picture reads the same file (src/ad/cues.json),
so a key, a traced wall or a found window always lands on its sound.

    python3 audio/cues.py
"""

import json
from pathlib import Path

cues = []


def add(frame, sound, **extra):
    cues.append({"frame": int(round(frame)), "sound": sound, **extra})


# Act I. Find.
add(6, "bloom")
add(60, "click")
TEXT = "Methfesselstraße 8"
gaps = [5, 4, 5, 4, 5, 4, 4, 5, 4, 7, 4, 5, 4, 4, 5, 4, 8]
f = 62
for i, ch in enumerate(TEXT):
    add(f, "key", index=i, char=ch, space=ch == " ")
    if i < len(gaps):
        f += gaps[i]
add(146, "tick")
add(151, "tick", pitch=1.12)
add(180, "click")
add(196, "whoosh", seconds=0.5)
add(210, "pin")
add(240, "riser", seconds=0.5)
add(240, "boom")
add(240, "rumble", seconds=1.6)

# Act II. The AI reads the plan.
add(366, "whoosh", seconds=0.6)
add(396, "shimmer", seconds=3.4)
for k in range(19):  # 6 outer walls, then 13 inner walls, on 32nd notes
    add(420 + k * 3.75, "trace", index=k)
add(492, "swish")
for k in range(8):  # rooms on 16ths
    add(510 + k * 7.5, "room", index=k)
add(568, "pop")
add(572, "build", seconds=0.5)

# The facade.
add(600, "whoosh", seconds=0.35)
add(622, "thud")
add(630, "shimmer", seconds=2.0)
add(636, "scan", seconds=1.4)
for n in range(30):  # five rows top to bottom, six bays left to right
    add(645 + n * 2.5, "detect", index=n, row=n // 6, col=n % 6)
add(750, "whoosh", seconds=0.8)
add(825, "riser", seconds=2.25)

# Act III. Placed, together.
add(840, "impact")
for n in range(40):
    add(842 + n * 1.2, "glass", index=n)
add(962, "join", pitch=1.0)
add(976, "join", pitch=1.12)
add(990, "join", pitch=1.26)
add(1000, "dots")
add(1024, "message")
add(1060, "dots")
add(1084, "message")
add(1092, "whoosh", seconds=0.4)
add(1110, "grab")


def ease_in_out(t):
    return 4 * t**3 if t < 0.5 else 1 - (-2 * t + 2) ** 3 / 2


value_prev = 0
for fr in range(1110, 1171):
    v = 16 * ease_in_out((fr - 1110) / 60)
    while value_prev < 16 and v >= value_prev + 1:
        value_prev += 1
        add(fr, "slider", value=value_prev)
        if value_prev in (5, 10, 15):
            add(fr, "roll", to="FED"[[5, 10, 15].index(value_prev)])
add(1176, "dots")
add(1200, "message")
add(1250, "toggle")
add(1256, "sweep")
add(1272, "roll", to="C")
add(1296, "roll", to="B")
add(1300, "chime")
add(1320, "hit")
add(1326, "whoosh", seconds=0.4)
for n in range(14):
    add(1332 + n * 3, "count", index=n)
add(1440, "paper")
add(1500, "click")
add(1506, "success")
add(1530, "reverse", seconds=0.5)

# Act IV. End.
add(1560, "final")
for n, fr in enumerate((1564, 1569, 1574)):
    add(fr, "block", index=n)
add(1572, "whoosh", seconds=0.5)
add(1680, "bell")

cues.sort(key=lambda c: c["frame"])
out = Path(__file__).resolve().parent.parent / "src" / "ad" / "cues.json"
out.write_text(json.dumps(cues, indent=1, ensure_ascii=False))
print(len(cues), "cues")
