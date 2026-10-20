"""
The one timing source of the film: every timed event in frames at 60 fps, on THIS film's grid
(tempo, meter and form from src/music.json). The picture reads src/cues.json for its timing and
score.py reads the same file for its sound, so every hit lands on its picture. Generate rhythms
here (typing, runs, counters) from the SAME formula the picture uses.

    python3 audio/cues.py
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MUSIC = json.loads((ROOT / "src" / "music.json").read_text())
FPS = 60
BEAT = FPS * 60 / MUSIC["bpm"]                  # frames per beat
BAR = BEAT * MUSIC.get("beats_per_bar", 4)      # frames per bar
STEP = BEAT / MUSIC.get("steps_per_beat", 4)    # frames per 16th (per 8th in 12/8)

SECTION = {}
_bars = 0.0
for s in MUSIC["form"]:
    SECTION[s["name"]] = _bars
    _bars += s["bars"]


def at(bar: float, beat: float = 0.0) -> int:
    """Frame of a bar and beat counted from the film's start (fractions allowed)."""
    return int(round(bar * BAR + beat * BEAT))


def start(section: str, bar: float = 0.0, beat: float = 0.0) -> int:
    """Frame of a bar and beat inside a section of the form."""
    return at(SECTION[section] + bar, beat)


cues = []


def add(frame, sound, **extra):
    cues.append({"frame": int(round(frame)), "sound": sound, **extra})


# Example: a run of taps on 8ths in the second bar of the verse, a riser into the drop.
for i in range(4):
    add(start("verse", 1, i * 0.5), "tap", index=i)
add(start("drop"), "riser", seconds=1.2)  # a riser ENDS on its frame
add(start("drop"), "impact")

cues.sort(key=lambda c: c["frame"])
(ROOT / "src" / "cues.json").write_text(json.dumps(cues, indent=1))
print(len(cues), "cues;", f"{MUSIC['bpm']} BPM, beat {BEAT:.2f} frames, bar {BAR:.2f} frames")
for name, b in SECTION.items():
    print(f"  {name:10s} frame {at(b):5d}")
