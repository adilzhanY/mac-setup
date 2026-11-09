"""
Hear (or measure) a genre before committing a film to it: renders an 8 bar sketch of any genre
in grooves.py with the film's key, mode and palette choices, to out/demo-<genre>.wav. Or render
a whole 30 s film (music, effects on a sample cue list, dips, opening, master) to see the engine
end to end.

    .venv/bin/python audio/demo.py amapiano --key "F#" --mode dorian --bpm 112.5
    .venv/bin/python audio/demo.py ambient_pulse --beatless     # the same form with no beat
    .venv/bin/python audio/demo.py all                          # every genre, for comparing
    .venv/bin/python audio/demo.py afrobeats --film             # a full film: out/demo-film/
    .venv/bin/python audio/demo.py boom_bap --film --synth      # the same with the synth instead of samples
"""

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import soundfile

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dsp  # noqa: E402
from grooves import GENRES  # noqa: E402
from score import FPS, build, report  # noqa: E402

KIT = Path(__file__).resolve().parent.parent


def sketch(name, key="A", mode=None, bpm=None, seed=1, beat=True, instruments="samples"):
    g = GENRES[name]
    brief = {
        "genre": name, "bpm": bpm or g.tempos[0], "key": key, "mode": mode or g.modes[0], "seed": seed, "beat": beat,
        "instruments": instruments,
        "hook": {"seed": seed + 2, "contour": "arch"},
        "form": [
            {"name": "intro", "bars": 2, "energy": 0.4, "parts": ["pad", "hook_sparse", "hat", "shaker"]},
            {"name": "main", "bars": 4, "energy": 1.0, "parts": ["drums", "bass", "chords", "pad", "hook", "crash"]},
            {"name": "outro", "bars": 2, "energy": 0.7, "parts": ["drums", "bass", "pad", "fill"]},
        ],
    }
    seconds = 8 * g.beats_per_bar * 60 / brief["bpm"] + 2
    mix, _, _ = build(brief, [], seconds, verbose=False)
    return mix


def demo_cues(brief: dict) -> list[dict]:
    """A plausible cue list on the brief's own form: interface events that follow the picture (some
    off the beat), cuts marked, one hero hit, an airy end card and the logo. Structural cuts (the act
    changes, the reveal, the end card) sit on downbeats; ordinary cuts fall where the action is, as
    in professional films, whose cuts are barely more aligned with musical hits than chance."""
    bar = FPS * 60 / brief["bpm"] * brief.get("beats_per_bar", 4)
    beat = bar / brief.get("beats_per_bar", 4)
    start, t = {}, 0.0
    for s in brief["form"]:
        start[s["name"]] = t
        t += s["bars"] * bar
    names = list(start)
    hero = max(brief["form"][1:], key=lambda s: s.get("energy", 0))["name"]
    c = []

    def add(frame, sound, **kw):
        c.append({"frame": int(round(frame)), "sound": sound, **kw})

    s1, s2 = start[names[1]], start[names[2]]
    add(s1, "swish", seconds=0.14, cut=True)
    for i, w in enumerate((0, 1.0, 1.5, 2.5)):  # words arrive with the read, not the grid
        add(s1 + w * beat + 3 * i, "text", index=i)
    for i in range(4):  # a cursor tapping through a list
        add(s1 + bar + i * beat * 0.5 + (0, 4, 2, 7)[i], "tap", index=i)
    add(s1 + 2 * bar + 1.5 * beat + 5, "card", size=0.5, cut=True)
    add(s1 + 2 * bar + beat * 1.5, "chip", index=2)
    add(s1 + 2 * bar + beat * 3, "error")
    add(s2 - 0.5 * beat, "toggle", on=True, cut=True)
    for i in range(12):  # a counter running in 16ths
        add(s2 + bar + i * beat / 4, "tick", index=i)
    add(s2 + bar * 1.5, "panel_open", seconds=0.3)
    add(start[hero], "riser", seconds=bar / FPS)
    add(start[hero], "impact", weight="hero", cut=True)
    add(start[hero] + bar, "success")
    add(start[hero] + 2 * bar + 0.75 * beat, "whoosh", seconds=0.42, cut=True)
    for i in range(3):
        add(start[hero] + 2.5 * bar + i * beat, "tier", index=i)
    add(start[hero] + 3 * bar, "pop", index=1)
    end = start[names[-1]]
    add(end, "whoosh", seconds=0.9, air=True, cut=True)
    add(end + beat * 2, "logo", weight="hero")
    add(end + bar, "texture", seconds=bar / FPS)
    return sorted(c, key=lambda x: x["frame"])


def film(genre=None, key=None, mode=None, bpm=None, seed=None, beat=True, out=Path("out"), instruments=None):
    """The kit's example brief (src/music.json), optionally re-cut, with demo_cues, into out/demo-film."""
    brief = json.loads((KIT / "src" / "music.json").read_text())
    if genre:
        g = GENRES[genre]
        brief.update(genre=genre, bpm=bpm or g.tempos[0], mode=mode or g.modes[0], palette={}, drums={})
    brief.update({k: v for k, v in dict(key=key, mode=mode, bpm=bpm, seed=seed).items() if v is not None})
    brief["beat"] = beat
    if instruments:
        brief["instruments"] = instruments
    tag = "-synth" if brief.get("instruments") == "synth" else "-samples"
    root = out / f"demo-film-{brief['genre']}{'' if beat else '-beatless'}{tag}"
    (root / "src").mkdir(parents=True, exist_ok=True)
    cues = demo_cues(brief)
    (root / "src" / "music.json").write_text(json.dumps(brief, indent=1))
    (root / "src" / "cues.json").write_text(json.dumps(cues, indent=1))
    mix, grid, dips = build(brief, cues, brief.get("length", 30.0), root)
    (root / "public").mkdir(exist_ok=True)
    soundfile.write(root / "public" / "film.wav", mix.T.astype(np.float32), dsp.SR, subtype="PCM_24")
    print(f"wrote {root / 'public' / 'film.wav'} ({len(cues)} cues)")
    report(mix, grid, dips, brief)
    return root


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("genre")
    ap.add_argument("--key", default=None)
    ap.add_argument("--mode")
    ap.add_argument("--bpm", type=float)
    ap.add_argument("--seed", type=int)
    ap.add_argument("--beatless", action="store_true", help="the same form with no drums, rubato")
    ap.add_argument("--film", action="store_true", help="render a whole film with sample cues into out/demo-film-<genre>/")
    ap.add_argument("--samples", action="store_true", help="sampled instruments (the default when the library exists)")
    ap.add_argument("--synth", action="store_true", help="the synth instead of sampled instruments")
    ap.add_argument("--out", default="out")
    a = ap.parse_args()
    Path(a.out).mkdir(exist_ok=True)
    if a.film:
        film(None if a.genre == "example" else a.genre, a.key, a.mode, a.bpm, a.seed, not a.beatless, Path(a.out),
             "synth" if a.synth else "samples" if a.samples else None)
        sys.exit(0)
    for name in (GENRES if a.genre == "all" else [a.genre]):
        x = sketch(name, a.key or "A", a.mode, a.bpm, a.seed or 1, not a.beatless, "synth" if a.synth else "samples")
        assert np.isfinite(x).all(), name
        tag = f"demo-{name}{'-beatless' if a.beatless else ''}{'-synth' if a.synth else ''}.wav"
        soundfile.write(Path(a.out) / tag, x.T.astype(np.float32), dsp.SR, subtype="PCM_24")
        print(f"{name:18s} {GENRES[name].tempos[0] if not a.bpm else a.bpm:7.2f} BPM  {dsp.rms_db(x):6.1f} dB RMS  peak {dsp.true_peak(x):5.2f} dBTP")
