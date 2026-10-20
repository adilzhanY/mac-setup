"""
The film's score, built from its own sonic brief (src/music.json) and cue list (src/cues.json).
Writes public/film.wav at 48 kHz, 24 bit, -14 LUFS, true peak under -1 dBTP, exactly the film.

    .venv/bin/python audio/score.py

This file is the starting point for EVERY film, never an earlier film's synth. What makes the
film's music its own lives in music.json (genre, tempo, key, mode, palette, patterns, hook, form)
and in the per film hooks at the bottom of this file (SFX map, special moments). Change them; do
not paste in another film's score.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

import dsp  # noqa: E402
import instruments as ins  # noqa: E402
import sfx  # noqa: E402
from dsp import SR, Bus  # noqa: E402
from grooves import GENRES, hits, roll  # noqa: E402
from theory import Key, answer, motif, voice_lead  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
FPS = 60


class Grid:
    """Tempo, meter and the form's section starts, in seconds and frames."""

    def __init__(self, brief: dict):
        g = GENRES[brief["genre"]]
        self.genre = g
        self.bpm = brief["bpm"]
        self.spb = brief.get("steps_per_beat", g.steps_per_beat)
        self.bpb = brief.get("beats_per_bar", g.beats_per_bar)
        self.beat = 60 / self.bpm
        self.step = self.beat / self.spb
        self.bar = self.beat * self.bpb
        self.sections = []
        t = 0.0
        for s in brief["form"]:
            self.sections.append({**s, "start": t, "end": t + s["bars"] * self.bar})
            t += s["bars"] * self.bar

    def frame(self, seconds: float) -> int:
        return int(round(seconds * FPS))


def drum_kind(role: str, palette: dict) -> tuple[str, str]:
    """(function, kind) for a drum role such as kick, snare, hat_open, conga."""
    kind = palette.get(role, role)
    if role.startswith("kick"):
        return "kick", kind
    if role in ("snare", "clap", "rim", "ghost", "snap"):
        return "snare", {"ghost": palette.get("snare", "tight")}.get(role, kind)
    if role.startswith("hat") or role in ("shaker", "tamb", "open", "ride"):
        return "hat", kind if kind in ("closed", "open", "ride", "shaker", "tamb", "909", "trap") else "closed"
    return "perc", kind


def play_drum(fn: str, kind: str, v: float):
    if fn == "kick":
        return ins.kick(kind, v)
    if fn == "snare":
        return ins.snare(kind, v)
    if fn == "hat":
        return ins.hat(kind, v)
    if kind in ("taiko",):
        return ins.kick("taiko", v)
    if kind == "log":
        return None  # the log drum is a pitched bass part, played by the bass line
    return ins.perc_hit(kind, v)


def render(brief: dict, cues: list[dict], seconds: float) -> tuple[np.ndarray, Grid]:
    dsp.seed(brief.get("seed", 1))
    rng = np.random.default_rng(brief.get("seed", 1))
    grid = Grid(brief)
    g = grid.genre
    key = Key(brief["key"], brief["mode"])
    palette = {**g.palette, **brief.get("palette", {})}
    patterns = {**g.drums, **brief.get("drums", {})}
    swing = brief.get("swing", g.swing)
    prog = brief.get("progression") or key.progression(brief.get("mood", g.moods[0]), brief.get("progression_variant", 0))
    chords = voice_lead([key.chord(r, 4 if brief.get("sevenths", True) else 3) for r in prog], centre=brief.get("chord_centre", 62))
    harm_bars = brief.get("bars_per_chord", 1)
    hook_cfg = brief.get("hook", {})
    hook = motif(key, hook_cfg.get("seed", 3), hook_cfg.get("contour", "arch"), hook_cfg.get("notes", 6),
                 low=hook_cfg.get("low", 67), bar_steps=grid.spb * grid.bpb, rhythm=hook_cfg.get("rhythm"))
    reply = answer(hook, key)

    buses = {k: Bus(seconds) for k in ("kick", "drums", "bass", "chords", "pad", "hook", "fx")}
    kick_times = []

    for sec in grid.sections:
        parts = set(sec.get("parts", []))
        energy = sec.get("energy", 0.7)
        for b in range(int(np.ceil(sec["bars"]))):
            t0 = sec["start"] + b * grid.bar
            inside = lambda hs: [(t, v) for t, v in hs if t < sec["end"] - 0.01]  # noqa: E731
            bar_index = int(round(t0 / grid.bar))
            chord = chords[(bar_index // harm_bars) % len(chords)]
            root = min(chord) - 12
            while root > 45:
                root -= 12
            last_bar = b == int(np.ceil(sec["bars"])) - 1

            # Drums: every part named in the section plays its pattern ("drums" plays them all).
            for role, pat in patterns.items():
                if role not in parts and "drums" not in parts:
                    continue
                if f"-{role}" in parts:
                    continue
                spb = len(pat) // max(1, len(pat) // (grid.spb * grid.bpb))
                bar_pat = pat[(b % max(1, len(pat) // spb)) * spb :][:spb]
                fn, kind = drum_kind(role, palette)
                for t, v in inside(hits(bar_pat, t0, grid.step, swing, grid.spb, 0.004, rng)):
                    s = play_drum(fn, kind, v * (0.6 + 0.4 * energy))
                    if s is None:
                        continue
                    bus = buses["kick"] if fn == "kick" else buses["drums"]
                    pan = {"hat": 0.25, "perc": rng.uniform(-0.5, 0.5)}.get(fn, 0.0)
                    bus.add(s, t, {"kick": 1.0, "hat": 0.4}.get(fn, 0.55), pan)
                    if fn == "kick":
                        kick_times.append(t)
            if "fill" in parts and last_bar:
                for t, v in roll(t0 + grid.beat * (grid.bpb - 1), grid.beat, grid.step / 2):
                    buses["drums"].add(ins.snare(palette.get("snare", "tight"), v * 0.6), t, 0.5)
            if g.extra.get("hat_rolls") and "drums" in parts and b % 2 == 1:
                for t, v in roll(t0 + grid.beat * (grid.bpb - 1) + grid.step * 2, grid.step * 2, grid.step / 3, 0.3, 0.6):
                    buses["drums"].add(ins.hat("trap", v), t, 0.4, 0.25)

            # Bass: the genre's rhythm on the chord root; octave kinds jump on accented steps.
            if "bass" in parts:
                bpat = brief.get("bass_rhythm", g.bass["rhythm"])
                kind = palette.get("bass", g.bass["kind"])
                prev = None
                for i, (t, v) in enumerate(inside(hits(bpat[: grid.spb * grid.bpb], t0, grid.step, swing, grid.spb))):
                    m = root + (12 if kind == "octave" and i % 2 else 0)
                    if kind == "log" and i % 3 == 2:
                        m = root + 7
                    dur = grid.step * (2 if kind not in ("808", "reese") else 6)
                    s = ins.bass(kind, m, dur, v, glide_from=prev if kind in ("808", "acid", "log") and prev != m else None,
                                 cut=0.6 + 0.6 * energy, accent=v > 0.9)
                    buses["bass"].add(s, t, 1.0)
                    prev = m

            # Chords in the genre's style.
            if "chords" in parts:
                style = brief.get("chord_style", g.chords["style"])
                kind = palette.get("keys", g.chords["kind"])
                cpat = brief.get("chord_rhythm", g.chords["rhythm"])[: grid.spb * grid.bpb]
                if style in ("stabs", "comp"):
                    for t, v in inside(hits(cpat, t0, grid.step, swing, grid.spb)):
                        d = grid.step * (1.5 if style == "stabs" else 3)
                        if kind in ins.KEY_KINDS:
                            s = ins.strum(kind, chord, d, v * 0.8, cut=0.4 + 0.6 * energy)
                        else:  # a pad sound played short: string or saw stabs
                            s = ins.pad(kind, chord, d, cut=1500 + 3000 * energy, attack=0.004, v=v * 1.4)
                        buses["chords"].add(s, t, 0.5)
                elif style == "ostinato":
                    tones = chord + [chord[0] + 12]
                    for i, (t, v) in enumerate(inside(hits(cpat, t0, grid.step, swing, grid.spb))):
                        s = ins.lead("pluck", tones[i % len(tones)], grid.step * 0.9, v * 0.6, cut=0.5 + 0.5 * energy)
                        buses["chords"].add(s, t, 0.4, (i % 2) * 0.6 - 0.3)
            if "pad" in parts and b % harm_bars == 0:
                kind = palette.get("pad", "warm")
                s = ins.pad(kind, chord, min(grid.bar * harm_bars, sec["end"] - t0), cut=900 + 3000 * energy, attack=min(0.6, grid.beat))
                buses["pad"].add(s, t0, 0.35)

            # The hook: call on even bars, answer on odd bars.
            if "hook" in parts or "hook_sparse" in parts:
                if "hook_sparse" in parts and b % 2 == 1:
                    continue
                phrase = hook if b % 2 == 0 else reply
                kind = palette.get("lead", "pluck")
                for st, ln, m in phrase:
                    t = t0 + st * grid.step + ((2 * swing - 1) * grid.step if st % 2 and grid.spb % 2 == 0 else 0)
                    if t >= sec["end"] - 0.01:
                        continue
                    d = ln * grid.step
                    if kind == "fold":
                        s = ins.fold_lead(m, d, 0.7)
                    elif kind in ("mallet", "marimba", "kalimba", "vibes", "steel", "bell", "celesta", "nylon", "harp", "piano", "epiano"):
                        s = ins.keys(kind, m, d, 0.8)
                    else:
                        s = ins.lead(kind, m, d, 0.7, vowel="aeiou"[st % 5])
                    buses["hook"].add(s, t, 0.5, 0.0)

        if "crash" in parts:
            buses["fx"].add(ins.crash(0.7), sec["start"], 0.35)

    # Mix: each bus its treatment, the musical buses pumping under the kick.
    n = buses["kick"].n
    duck = dsp.duck_curve(n, kick_times, depth=brief.get("pump", 0.4))
    drums = dsp.lp(dsp.room(buses["drums"].x, 0.25, 0.08), 13000)
    bass = dsp.comp(buses["bass"].x, -20, 3, 4, 90) * duck ** 1.3
    chords_x = dsp.chorus(dsp.room(buses["chords"].x, 0.5, 0.18), 0.5, 0.2, 0.3) * duck
    pad_x = dsp.hall(buses["pad"].x, 0.3) * duck
    hook_x = dsp.pingpong(buses["hook"].x, grid.beat * 0.75, 0.35, 0.25)
    hook_x = dsp.room(hook_x, 0.45, 0.15) * duck ** 0.5
    music = buses["kick"].x + drums + bass + chords_x + pad_x + hook_x + buses["fx"].x
    if g.extra.get("vinyl"):
        music += dsp.stereo(ins.vinyl(seconds, 0.4))[:, :n]
    if g.extra.get("wow") or brief.get("wow"):
        music = dsp.wow(music)
    music = dsp.balance(music, **brief.get("balance", {}))

    # Section levels follow the form's energy, ramped over 20 ms so nothing clicks.
    level = np.ones(n)
    for sec in grid.sections:
        a, b = int(sec["start"] * SR), min(n, int(sec["end"] * SR))
        level[a:b] = 0.35 + 0.65 * sec.get("energy", 0.7) if "silence" not in sec.get("parts", []) else 0.0
    k = int(0.02 * SR)
    level = np.convolve(level, np.ones(k) / k, mode="same")
    return music * level, grid


# --- Per film: effects -------------------------------------------------------------------------
# Map every cue name in cues.json to a sound. Pick the film's CHARACTER (sfx.CHARACTERS) once.


def effects(cues: list[dict], seconds: float, key: Key, character: str) -> np.ndarray:
    bus = Bus(seconds)
    for c in cues:
        name, i, t = c["sound"], c.get("index", 0), c["frame"] / FPS
        if name in ("whoosh", "swish"):
            s = sfx.whoosh(c.get("seconds", 0.5), character)
            t -= c.get("seconds", 0.5) * 0.55
        elif name == "riser":
            s = sfx.riser(key, c.get("seconds", 1.5), character)
            t -= c.get("seconds", 1.5)
        elif name == "reverse":
            s = sfx.reverse_swell(c.get("seconds", 1.0))
            t -= c.get("seconds", 1.0)
        elif name in ("impact", "boom", "hit", "final"):
            s = sfx.impact(character, 1.0 if name != "boom" else 0.7)
        elif name in ("tap", "place", "blip", "land", "block", "card", "tier"):
            s = sfx.blip(key, i, character)
        elif name in ("tick", "count"):
            s = sfx.tick(character, 1 + i / 40)
        elif name == "click":
            s = sfx.click(character)
        elif name in ("chime", "bell", "success"):
            s = sfx.chime(key, character)
        elif name in ("gap", "stop", "sub"):
            continue  # handled by the form (silence) or the score
        else:
            print(f"  no sound designed for cue '{name}': add it to effects()")
            continue
        bus.add(s, t, 0.8 * 10 ** (dsp.rng.uniform(-1, 1) / 20), dsp.rng.uniform(-0.2, 0.2) if s.ndim == 1 else 0.0)
    return dsp.room(bus.x, 0.3, 0.1)


def main() -> None:
    brief = json.loads((ROOT / "src" / "music.json").read_text())
    cues = json.loads((ROOT / "src" / "cues.json").read_text())
    seconds = brief.get("length", 30.0)
    music, grid = render(brief, cues, seconds)
    key = Key(brief["key"], brief["mode"])
    fxs = effects(cues, seconds, key, brief.get("character", "glass"))
    mix = music + fxs * brief.get("fx_level", 0.5)
    for sec in grid.sections:  # a silent section is silent for the effects too
        if "silence" in sec.get("parts", []):
            a, b = int(sec["start"] * SR), int(sec["end"] * SR)
            mix[:, a:b] = 0
    t = np.arange(mix.shape[1]) / SR
    f0, f1 = brief.get("fade", [seconds - 1.7, seconds - 0.2])
    mix *= np.where(t < f0, 1, np.clip((f1 - t) / (f1 - f0), 0, 1) ** 2)
    # Loudness for the destination (references/destinations.md): -14 LUFS for web, social and stores,
    # -23 LUFS for European TV (EBU R128), -24 for US TV (ATSC A/85).
    loud = brief.get("loudness", {})
    mix = dsp.master(mix, loud.get("lufs", -14.0), loud.get("tp", -1.0))
    import pyloudnorm
    import soundfile

    print(f"{brief['genre']} {grid.bpm} BPM, {brief['key']} {brief['mode']}: "
          f"{pyloudnorm.Meter(SR).integrated_loudness(mix.T):.2f} LUFS, true peak {dsp.true_peak(mix):.2f} dBTP")
    for sec in grid.sections:
        a, b = int(sec["start"] * SR), min(mix.shape[1], int(sec["end"] * SR))
        if b > a:
            print(f"  {sec['name']:10s} frames {grid.frame(sec['start']):5d} to {grid.frame(sec['end']):5d}: {dsp.rms_db(mix[:, a:b]):6.1f} dB RMS")
    (ROOT / "public").mkdir(exist_ok=True)
    soundfile.write(ROOT / "public" / "film.wav", mix.T.astype(np.float32), SR, subtype="PCM_24")


if __name__ == "__main__":
    main()
