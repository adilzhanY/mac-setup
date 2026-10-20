"""
Hear (or measure) a genre before committing a film to it: renders an 8 bar sketch of any genre
in grooves.py with the film's key, mode and palette choices, to out/demo-<genre>.wav.

    .venv/bin/python audio/demo.py amapiano --key "F#" --mode dorian --bpm 112.5
    .venv/bin/python audio/demo.py all          # every genre, for comparing
"""

import argparse
import sys
from pathlib import Path

import numpy as np
import soundfile

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dsp  # noqa: E402
from grooves import GENRES  # noqa: E402
from score import render  # noqa: E402


def sketch(name, key="A", mode=None, bpm=None, seed=1):
    g = GENRES[name]
    brief = {
        "genre": name, "bpm": bpm or g.tempos[0], "key": key, "mode": mode or g.modes[0], "seed": seed,
        "hook": {"seed": seed + 2, "contour": "arch"},
        "form": [
            {"name": "intro", "bars": 2, "energy": 0.4, "parts": ["pad", "hook_sparse", "hat", "shaker"]},
            {"name": "main", "bars": 4, "energy": 1.0, "parts": ["drums", "bass", "chords", "pad", "hook", "crash"]},
            {"name": "outro", "bars": 2, "energy": 0.7, "parts": ["drums", "bass", "pad", "fill"]},
        ],
    }
    beats = 8 * g.beats_per_bar
    seconds = beats * 60 / brief["bpm"] + 2
    music, _ = render(brief, [], seconds)
    return dsp.master(music)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("genre")
    ap.add_argument("--key", default="A")
    ap.add_argument("--mode")
    ap.add_argument("--bpm", type=float)
    ap.add_argument("--out", default="out")
    a = ap.parse_args()
    Path(a.out).mkdir(exist_ok=True)
    for name in (GENRES if a.genre == "all" else [a.genre]):
        x = sketch(name, a.key, a.mode, a.bpm)
        assert np.isfinite(x).all(), name
        soundfile.write(Path(a.out) / f"demo-{name}.wav", x.T.astype(np.float32), dsp.SR, subtype="PCM_24")
        print(f"{name:18s} {GENRES[name].tempos[0] if not a.bpm else a.bpm:7.2f} BPM  {dsp.rms_db(x):6.1f} dB RMS  peak {dsp.true_peak(x):5.2f} dBTP")
