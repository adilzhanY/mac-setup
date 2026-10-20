"""
The one timing source of the film: every timed event in frames at 60 fps (120 BPM, a beat is
30 frames, a bar 120, a 16th 7.5). The picture reads src/cues.json for its timing and the
synthesizer reads the same file for its sound, so a slam, a tick or a tier always lands on its hit.

    python3 audio/cues.py
"""

import json
from pathlib import Path

cues = []


def add(frame, sound, **extra):
    cues.append({"frame": int(round(frame)), "sound": sound, **extra})


# Act I. Load the bar.
add(6, "zip", seconds=0.5)
for i, fr in enumerate((30, 60, 90)):
    add(fr, "slam", index=i)
add(100, "collar")
add(225, "whoosh", seconds=0.6)

# Act II. Log it.
add(240, "boom")
for i in range(4):
    add(252 + i * 5, "tick", index=i)
for i in range(4):
    add(285 + i * 15, "set", index=i)
add(336, "pr")
for i, fr in enumerate((360, 375, 390)):
    add(fr, "rest", index=i)
add(405, "go")
add(408, "whoosh", seconds=0.4)

# Act III. The engine.
add(420, "shimmer", seconds=2.0)
for i in range(30):
    add(426 + i * 3.75, "grain", index=i)
add(540, "pin")
for i in range(8):
    add(546 + i * 3.75, "bell", index=i)
add(578, "pop")

# Act IV. Forge the rank.
add(600, "crash")
for i, fr in enumerate((630, 675, 705, 735, 757.5, 772.5, 787.5)):
    add(fr, "tier", index=i)
add(825, "riser", seconds=1.1)

# Drop.
add(840, "impact")
for i in range(36):
    add(842 + i * 1.3, "glass", index=i)
add(945, "whoosh", seconds=0.4)

# Act V. Together.
for i in range(5):
    add(966 + i * 5, "tick", index=i)
for i in range(16):
    add(1020 + i * 3, "count", index=i)
add(1038, "swap", index=0)
add(1062, "swap", index=1)
add(1100, "message")
for i in range(7):
    add(1180 + i * 15, "blip", index=i)
add(1275, "pop")
add(1290, "chime")

# Payoff.
add(1320, "hit")
# The gain counter follows the line's head (9 frames a month, from frame 1326): one tick per new kilo.
KG = [105, 107, 110, 110, 114, 117, 116, 121, 125, 124, 129, 135, 140]
best, n = 105, 0
for fr in range(1326, 1326 + 9 * 12 + 1):
    m = (fr - 1326) / 9
    i = min(11, int(m))
    v = KG[i] + (KG[i + 1] - KG[i]) * (m - i)
    while best < 140 and v >= best + 1:
        best += 1
        add(fr, "count", index=n)
        n += 1
for i, fr in enumerate((1362, 1398, 1434)):
    add(fr, "pr", index=i)
add(1560, "reverse", seconds=0.5)

# End.
add(1560, "final")
for i in range(6):
    add(1562 + i * 4, "block", index=i)
add(1590, "whoosh", seconds=0.5)
add(1680, "bell", index=8)

cues.sort(key=lambda c: c["frame"])
out = Path(__file__).resolve().parent.parent / "src" / "cues.json"
out.write_text(json.dumps(cues, indent=1))
print(len(cues), "cues")
