"""
Reference only: this film's music is taken (see music/registry.json). Read it for mixing ideas;
never start a new score from it. New films start from templates/kit/audio/score.py.

The commercial's soundtrack: a 120 BPM score in G major in the spirit of an Apple ad, and one
synthesized sound for every cue of src/ad/cues.json, placed on the cue's frame (60 fps).
Writes public/ad.wav: 30.0 s, 48 kHz, stereo, 24 bit, about -14 LUFS, true peak below -1 dBTP.

    .venv/bin/python audio/ad.py
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pyloudnorm
import soundfile
from pedalboard import Chorus, Compressor, HighpassFilter, LowpassFilter, Pedalboard, Reverb
from scipy import ndimage, signal

SR = 48_000
FPS = 60
N = SR * 30
BEAT = 0.5
S16 = BEAT / 4
ROOT = Path(__file__).resolve().parent.parent
rng = np.random.default_rng(20)


def sec(frame: float) -> float:
    return frame / FPS


def hz(m: float) -> float:
    return 440.0 * 2 ** ((m - 69) / 12)


# G major pentatonic, upwards from G3.
PENTA = [m for m in range(55, 110) if m % 12 in (7, 9, 11, 2, 4)]


# --- Building blocks --------------------------------------------------------------------------


def times(seconds: float) -> np.ndarray:
    return np.arange(int(SR * seconds)) / SR


def filt(x: np.ndarray, kind: str, cut, order: int = 2) -> np.ndarray:
    nyq = SR / 2
    w = [cut[0] / nyq, min(cut[1], SR * 0.45) / nyq] if kind == "bandpass" else min(cut, SR * 0.45) / nyq
    return signal.sosfilt(signal.butter(order, w, kind, output="sos"), x, axis=-1)


def lp(x, cut, order=2):
    return filt(x, "lowpass", cut, order)


def hp(x, cut, order=2):
    return filt(x, "highpass", cut, order)


def bp(x, lo, hi, order=2):
    return filt(x, "bandpass", (lo, hi), order)


def noise(n: int) -> np.ndarray:
    return rng.standard_normal(n)


def decay(t: np.ndarray, attack: float, length: float) -> np.ndarray:
    return np.clip(t / max(attack, 1e-4), 0, 1) * np.exp(-np.maximum(t - attack, 0) / length)


def gate(t: np.ndarray, dur: float, release: float) -> np.ndarray:
    return np.clip((dur + release - t) / release, 0, 1)


def tail_fade(x: np.ndarray, ms: float = 4) -> np.ndarray:
    k = min(x.shape[-1] // 2, int(SR * ms / 1000))
    x[..., -k:] *= np.linspace(1, 0, k)
    return x


def saw(f: float, n: int, phase: float = 0.0) -> np.ndarray:
    """A saw drawn at four times the rate and brought down, so the high notes do not alias."""
    t = np.arange(n * 4) / (SR * 4)
    return signal.resample_poly(signal.sawtooth(2 * np.pi * (f * t + phase)), 1, 4)[:n]


def pan2(s: np.ndarray, p: float) -> np.ndarray:
    a = (p + 1) * np.pi / 4
    return np.stack([s * np.cos(a), s * np.sin(a)])


class Bus:
    def __init__(self) -> None:
        self.x = np.zeros((2, N))

    def add(self, s: np.ndarray, t: float, gain: float = 1.0, pan: float = 0.0) -> None:
        s = pan2(s, pan) if s.ndim == 1 else s
        i = int(round(t * SR))
        lo, hi = max(i, 0), min(N, i + s.shape[1])
        if hi > lo:
            self.x[:, lo:hi] += s[:, lo - i : hi - i] * gain


def fx(x: np.ndarray, *plugins) -> np.ndarray:
    return Pedalboard(list(plugins))(x.astype(np.float32), SR).astype(np.float64)


def room(x: np.ndarray, size: float, wet: float, damping: float = 0.5) -> np.ndarray:
    return fx(x, Reverb(room_size=size, damping=damping, wet_level=wet, dry_level=1.0, width=1.0))


def fm_bell(f: float, seconds: float, ratio: float = 2.0, index: float = 3.0, length: float = 0.4) -> np.ndarray:
    t = times(seconds)
    idx = 0.4 + index * np.exp(-t / 0.05)
    v = np.sin(2 * np.pi * f * t + idx * np.sin(2 * np.pi * f * ratio * t))
    return tail_fade(v * decay(t, 0.001, length))


# --- Drums --------------------------------------------------------------------------------------


def kick(v: float = 1.0) -> np.ndarray:
    t = times(0.45)
    f = 47 + 125 * np.exp(-t / 0.028) + 30 * np.exp(-t / 0.004)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.19)
    click = bp(noise(len(t)), 2500, 8000) * np.exp(-t / 0.002) * 0.3
    return tail_fade(np.tanh(1.7 * (body + click)) * 0.95 * v)


def clap(v: float = 1.0) -> np.ndarray:
    t = times(0.4)
    e = np.zeros(len(t))
    for off in (0.0, 0.0085, 0.018, 0.027):
        e += (t >= off) * np.exp(-np.maximum(t - off, 0) / 0.004)
    tail = (t >= 0.027) * np.exp(-np.maximum(t - 0.027, 0) / 0.1) * 0.4
    a = bp(noise(len(t)), 900, 2300) * (e + tail)
    b = bp(noise(len(t)), 1500, 6000) * (e * 0.6 + tail * 0.5)
    return tail_fade(np.stack([a + 0.6 * b, 0.9 * a + 0.75 * b]) * v)


def snap(v: float = 1.0) -> np.ndarray:
    t = times(0.12)
    crack = bp(noise(len(t)), 1700, 6000) * np.exp(-t / 0.003)
    ring = np.sin(2 * np.pi * 2150 * t) * np.exp(-t / 0.011) * 0.3
    return tail_fade((crack + ring) * 1.2 * v)


def shaker(v: float = 1.0) -> np.ndarray:
    t = times(0.09)
    return tail_fade(hp(noise(len(t)), 5500, 4) * decay(t, 0.012, 0.025) * 0.4 * v)


HAT_F = np.array([205.3, 304.4, 369.6, 522.7, 540.0, 800.0]) * 1.6


def hat(length: float = 0.035, v: float = 1.0) -> np.ndarray:
    t = times(length * 6 + 0.01)
    metal = sum(signal.square(2 * np.pi * f * t) for f in HAT_F) / 6
    x = bp(metal + 0.6 * noise(len(t)), 7000, 15000, 4) * np.exp(-t / length)
    return tail_fade(x * 0.55 * v)


def snare(v: float = 1.0, cut: float = 200) -> np.ndarray:
    t = times(0.22)
    f = 180 + 60 * np.exp(-t / 0.008)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.05)
    rattle = bp(noise(len(t)), 1800, 9000) * np.exp(-t / 0.08)
    return tail_fade(hp(0.55 * body + rattle, cut) * 0.7 * v)


def crash(seconds: float = 2.4, v: float = 1.0) -> np.ndarray:
    t = times(seconds)
    out = []
    for _ in range(2):
        metal = sum(np.sin(2 * np.pi * f * t + rng.random() * 6.3) for f in rng.uniform(3200, 9500, 18)) / 18
        x = hp(noise(len(t)), 4500, 2) * 0.8 + metal * 0.35
        out.append(x * decay(t, 0.002, 0.75))
    return tail_fade(np.stack(out) * 0.45 * v, 40)


# --- Tonal instruments --------------------------------------------------------------------------


def ep_note(m: int, dur: float, v: float = 1.0, ring: float = 1.1) -> np.ndarray:
    """A DX7 style electric piano: a soft FM body and a short metallic tine at 14:1."""
    t = times(dur + 0.35)
    f = hz(m)
    idx = 0.25 + 1.5 * v * np.exp(-t / 0.35)
    body = np.sin(2 * np.pi * f * t + idx * np.sin(2 * np.pi * f * t))
    tine = np.sin(2 * np.pi * f * t + 2.2 * np.exp(-t / 0.012) * np.sin(2 * np.pi * 14 * f * t)) * np.exp(-t / 0.045)
    amp = decay(t, 0.003, ring) * gate(t, dur, 0.3)
    return tail_fade((body * amp + 0.3 * tine * gate(t, dur, 0.3)) * v)


def ep_chord(notes, dur, v, cut) -> np.ndarray:
    n = int(SR * (dur + 0.4))
    out = np.zeros(n)
    for k, m in enumerate(notes):
        s = ep_note(m, dur, v * (0.85 + 0.15 * rng.random()))
        i = int(SR * 0.004 * k)  # a light strum
        out[i : i + len(s)] += s[: n - i]
    return lp(out, cut) / len(notes) * 1.6


def pad_chord(notes, seconds: float, cut: float, voices: int = 3, attack: float = 0.5) -> np.ndarray:
    n = int(SR * seconds)
    out = np.zeros((2, n))
    detune = [0, -7, 7, -13, 13][:voices]
    for m in notes:
        for k, cents in enumerate(detune):
            v = saw(hz(m) * 2 ** (cents / 1200), n, rng.random())
            out += pan2(v, 0 if k == 0 else (0.6 if k % 2 else -0.6))
    out = lp(out, cut)
    t = np.arange(n) / SR
    e = np.clip(t / attack, 0, 1) * np.clip((seconds - t) / 0.4, 0, 1)
    return out * e / (len(notes) * voices)


def supersaw(notes, seconds: float, cut: float = 6000) -> np.ndarray:
    n = int(SR * seconds)
    out = np.zeros((2, n))
    for m in notes:
        for k, cents in enumerate((0, -11, 11, -21, 21, -31, 31)):
            v = saw(hz(m) * 2 ** (cents / 1200), n, rng.random())
            out += pan2(v, 0 if k == 0 else (0.85 if k % 2 else -0.85) * (k / 6))
    t = np.arange(n) / SR
    out = lp(out, cut) * decay(t, 0.003, seconds * 0.45)
    return tail_fade(out / (len(notes) * 4.5), 10)


def bass_note(m: int, dur: float, v: float = 1.0, bright: float = 1.0) -> np.ndarray:
    """Sub sine on the root, plus a plucky saw an octave above whose filter closes fast."""
    t = times(dur + 0.05)
    g = gate(t, dur, 0.04) * np.clip(t / 0.004, 0, 1)
    sub = np.sin(2 * np.pi * hz(m) * t) * g
    raw = saw(hz(m + 12), len(t))
    fe = np.exp(-t / 0.07) * bright
    mid = (lp(raw, 260) * (1 - fe) + lp(raw, 2200) * fe) * decay(t, 0.003, 0.3) * g
    return tail_fade(np.tanh(1.3 * (0.85 * sub + 0.55 * mid)) * v)


def pluck(m: int, dur: float, v: float = 1.0) -> np.ndarray:
    t = times(dur + 0.4)
    raw = saw(hz(m), len(t)) * 0.7 + saw(hz(m) * 1.004, len(t)) * 0.3
    fe = np.exp(-t / 0.05)
    x = lp(raw, 1100) * (1 - fe) + lp(raw, 8000) * fe
    amp = decay(t, 0.002, 0.3) * gate(t, dur, 0.12)
    sparkle = np.sin(2 * np.pi * hz(m + 12) * t) * np.exp(-t / 0.12) * 0.3
    return tail_fade((x + sparkle) * amp * v)


def marimba(m: int, v: float = 1.0) -> np.ndarray:
    t = times(0.6)
    f = hz(m)
    bar = np.sin(2 * np.pi * f * t) * np.exp(-t / 0.22) + 0.35 * np.sin(2 * np.pi * 4 * f * t) * np.exp(-t / 0.04)
    mallet = bp(noise(len(t)), 1500, 4000) * np.exp(-t / 0.002) * 0.15
    return tail_fade((bar + mallet) * v)


# --- The score ----------------------------------------------------------------------------------

CHORD = {
    "Cmaj9": ([48, 55, 59, 62, 64], 36),
    "Em7": ([52, 55, 59, 62], 40),
    "Em9": ([52, 59, 62, 66, 67], 40),
    "Dadd9": ([50, 57, 62, 64, 66], 38),
    "Gadd9": ([55, 59, 62, 69], 31),
    "G": ([55, 59, 62, 67], 31),
    "Am9": ([57, 60, 64, 67, 71], 33),
    "Cmaj7": ([48, 55, 59, 64], 36),
    "D/F#": ([54, 57, 62, 66], 30),
}
TIMELINE = [
    (0, 120, "Cmaj9"), (120, 180, "Em7"), (180, 240, "Dadd9"),
    (240, 360, "Gadd9"), (360, 480, "Am9"), (480, 600, "Em9"),
    (600, 720, "Cmaj7"), (720, 840, "Dadd9"),
    (840, 960, "G"), (960, 1080, "D/F#"), (1080, 1200, "Em7"), (1200, 1320, "Cmaj9"),
    (1320, 1440, "G"), (1440, 1500, "Cmaj9"), (1500, 1560, "Dadd9"),
    (1560, 1800, "Gadd9"),
]


def section(frame: float) -> str:
    for name, a, b in (
        ("intro", 0, 240), ("lift", 240, 360), ("ai", 360, 600), ("facade", 600, 825),
        ("drop", 840, 1290), ("groove", 1320, 1530), ("end", 1560, 1800),
    ):
        if a <= frame < b:
            return name
    return "stop"


def score():
    drums, perc, keys, pad, stabs, bass, hook = (Bus() for _ in range(7))
    kicks: list[float] = []

    def kick_at(frame, v=1.0):
        kicks.append(sec(frame))
        drums.add(kick(v), sec(frame))

    for a, b, name in TIMELINE:
        notes, root = CHORD[name]
        part = section(a)
        t0, length = sec(a), sec(b - a)
        eighths = int(length / (BEAT / 2))

        # Electric piano comping.
        if part in ("intro", "lift", "drop", "groove"):
            cut = {"intro": 1600, "lift": 2600, "drop": 4500, "groove": 4000}[part]
            hits = [(0, 0.9, 0.7), (3, 0.55, 0.6), (6, 0.65, 0.5)] if eighths == 8 else [(0, 0.85, 0.7), (3, 0.55, 0.3)]
            for pos, v, dur in hits:
                keys.add(ep_chord(notes, dur, v, cut), t0 + pos * BEAT / 2, 0.9 if part != "intro" else 1.0)
        elif part == "ai":
            k = (a - 360) / 240
            for pos, v in ((0, 0.7), (4, 0.45)):
                keys.add(ep_chord(notes, 0.9, v, 1300 + 1300 * k + 650 * pos / 4), t0 + pos * BEAT / 2, 0.85)
        elif part == "facade":
            for pos in (1, 3, 5, 7):
                k = (a - 600 + pos * 15) / 225
                keys.add(ep_chord(notes, 0.18, 0.45 + 0.35 * k, 1800 + 2600 * k), t0 + pos * BEAT / 2, 0.8)
        elif part == "end":
            keys.add(ep_chord(notes, 3.4, 0.95, 3400), t0, 1.1)

        # Pads: warm under everything, an octave up and wide while the AI reads.
        if part == "ai":
            pad.add(pad_chord([m + 12 for m in notes], length + 0.5, 4200, attack=0.8), t0, 0.75)
        elif part == "end":
            pad.add(pad_chord(notes, 4.0, 2200, attack=0.05), t0, 1.1)
        elif part != "stop":
            g = {"intro": 0.55, "lift": 0.55, "facade": 0.5, "drop": 0.55, "groove": 0.5}[part]
            seg = min(length, sec(825 - a)) if part == "facade" and b > 825 else length
            pad.add(pad_chord(notes, seg + 0.3, 1800 if part == "intro" else 2600), t0, g)

        # Supersaw stabs on the off 8ths, only in the drop (softer when the groove comes back).
        if part in ("drop", "groove"):
            stab = supersaw([m + 12 for m in notes], 0.2)
            for pos in range(1, eighths, 2):
                if a + pos * 15 < (1290 if part == "drop" else 1530):
                    stabs.add(stab, t0 + pos * BEAT / 2, 0.75 if part == "drop" else 0.5)
        if part == "end":
            stabs.add(supersaw([m + 12 for m in notes], 0.9), t0, 0.9)

        # Bass.
        bouncy = [(0, 0, 2), (3, 12, 1), (6, 0, 1), (8, 0, 2), (10, 12, 1), (11, 7, 1), (14, 12, 1)]
        if part in ("lift", "drop", "groove"):
            for step, interval, steps in bouncy:
                f = a + step * 7.5
                if f < b and f < {"lift": 360, "drop": 1290, "groove": 1530}[part]:
                    bass.add(bass_note(root + interval, steps * S16 * 0.9, 0.9), sec(f))
        elif part == "ai":
            for pos in range(eighths):
                k = (a - 360 + pos * 15) / 240
                bass.add(bass_note(root, BEAT / 2 * 0.7, 0.75, bright=0.15 + 0.6 * k), t0 + pos * BEAT / 2)
        elif part == "facade":
            step = 15 if a < 720 else 7.5
            f = a
            while f < min(b, 825):
                bass.add(bass_note(root, sec(step) * 0.7, 0.8, bright=0.5 + 0.5 * (f - 600) / 225), sec(f))
                f += step
        elif part == "end":
            bass.add(bass_note(root, 3.0, 1.0, bright=0.6), t0)

    # Drums, section by section.
    for f in range(240, 360, 30):
        kick_at(f)
    for bar in (360, 480):
        kick_at(bar)
        kick_at(bar + 75, 0.8)
        perc.add(snap(0.9), sec(bar + 60))  # the rim on 3 in half time
    for f in range(600, 825, 30):
        kick_at(f, 0.85 + 0.15 * (f - 600) / 225)
    for f in range(840, 1290, 30):
        kick_at(f)
    for f in range(1320, 1530, 30):
        kick_at(f)
    kick_at(1560, 1.1)

    for f in range(90, 360, 60):  # snaps on 2 and 4
        perc.add(snap(0.85), sec(f), pan=0.15)
    claps = [330] + list(range(870, 1290, 60)) + list(range(1350, 1530, 60))
    for f in claps:
        perc.add(clap(0.9), sec(f))
        if f >= 840:
            perc.add(snap(0.5), sec(f) + 0.004, pan=-0.2)

    def shake(a, b, g):
        f = a
        while f < b:
            perc.add(shaker(0.75 + 0.15 * rng.random()), sec(f), g, pan=0.35)
            perc.add(shaker(1.0 + 0.1 * rng.random()), sec(f) + 0.55 * BEAT / 2, g, pan=0.35)
            f += 15

    shake(120, 360, 0.5)
    shake(360, 600, 0.45)
    shake(600, 825, 0.65)
    shake(840, 1290, 0.85)
    shake(1320, 1530, 0.75)

    for f in range(255, 360, 30):
        perc.add(hat(0.03, 0.8), sec(f), pan=-0.25)
    f = 600.0
    while f < 825:
        k = (f - 600) / 225
        perc.add(hat(0.025, 0.35 + 0.55 * k * (1.0 if int(f / 7.5) % 2 == 0 else 0.6)), sec(f), pan=-0.25)
        f += 7.5
    for a, b in ((840, 1290), (1320, 1530)):
        for f in range(a + 15, b, 30):
            perc.add(hat(0.16, 0.7), sec(f), pan=-0.3)
        g = a
        while g < b:
            perc.add(hat(0.02, 0.3), sec(g), pan=0.3)
            g += 7.5

    # The snare roll into the drop: 8ths, 16ths, 32nds, 64ths, louder and brighter.
    roll, t = [], 12.0
    for start, step in ((12.0, 0.25), (12.5, 0.125), (13.0, 0.0625), (13.5, 0.03125)):
        t = start
        while t < start + 0.5 - 1e-9 and t < 13.75:
            roll.append(t)
            t += step
    for t in roll:
        k = (t - 12.0) / 1.75
        drums.add(snare(0.2 + 0.8 * k**1.5, 200 + 1600 * k), t)

    for f, v in ((840, 1.0), (1320, 0.9), (1560, 1.0)):
        perc.add(crash(2.6, v), sec(f))

    # The hook: two bar call and response, twice, in the drop.
    call = [(0, 71, 2), (2, 74, 1), (3, 76, 3), (6, 74, 2), (8, 71, 2), (10, 67, 1), (11, 69, 2), (14, 71, 2)]
    answer = [(0, 69, 3), (3, 71, 2), (6, 69, 2), (8, 67, 2), (10, 64, 2), (12, 62, 4)]
    call2 = [(0, 71, 2), (2, 74, 1), (3, 76, 3), (6, 74, 2), (8, 79, 2), (10, 76, 1), (11, 74, 2), (14, 71, 2)]
    answer2 = [(0, 76, 3), (3, 74, 2), (6, 71, 2), (8, 69, 4)]
    for bar, phrase in ((840, call), (960, answer), (1080, call2), (1200, answer2)):
        for step, m, steps in phrase:
            hook.add(pluck(m, steps * S16 * 0.85, 0.8), sec(bar + step * 7.5), pan=-0.1)
            hook.add(pluck(m + 12, steps * S16 * 0.6, 0.22), sec(bar + step * 7.5) + 0.003, pan=0.25)

    # Effects per bus.
    perc.x = room(perc.x, 0.22, 0.22, 0.6)
    keys.x = fx(keys.x, Chorus(rate_hz=0.7, depth=0.18, centre_delay_ms=7.0, feedback=0.0, mix=0.35),
                Reverb(room_size=0.5, damping=0.5, wet_level=0.2, dry_level=1.0, width=1.0))
    pad.x = fx(pad.x, Chorus(rate_hz=0.3, depth=0.3, centre_delay_ms=9.0, feedback=0.0, mix=0.5),
               Reverb(room_size=0.85, damping=0.4, wet_level=0.35, dry_level=0.9, width=1.0))
    stabs.x = fx(stabs.x, HighpassFilter(280), Reverb(room_size=0.55, damping=0.5, wet_level=0.22, dry_level=1.0, width=1.0))
    d = int(0.375 * SR)  # dotted 8th ping pong on the hook
    echo = np.zeros_like(hook.x)
    echo[0, d:] += hook.x[1, :-d] * 0.32
    echo[1, 2 * d :] += hook.x[0, : -2 * d] * 0.2
    hook.x = fx(hook.x + lp(echo, 5000), Reverb(room_size=0.5, damping=0.5, wet_level=0.2, dry_level=1.0, width=1.0))
    bass.x = fx(bass.x, Compressor(threshold_db=-12, ratio=3, attack_ms=5, release_ms=90))
    drums.x = fx(drums.x, Compressor(threshold_db=-10, ratio=2.5, attack_ms=8, release_ms=80))

    # Sidechain: the tonal parts duck under every kick and swell back.
    t = np.arange(N) / SR
    duck = np.ones(N)
    for k in kicks:
        i, j = int(k * SR), min(N, int((k + 0.5) * SR))
        seg = t[i:j] - k
        duck[i:j] = np.minimum(duck[i:j], 1 - 0.45 * np.clip(seg / 0.003, 0, 1) * np.exp(-seg / 0.11))
    for b_ in (keys, pad, stabs, hook):
        b_.x *= duck
    bass.x *= 1 - (1 - duck) * 1.3

    # The build: the tonal parts thin out towards the drop, as if a high pass were opening.
    synth = keys.x * 0.85 + pad.x * 0.8 + stabs.x * 0.7 + hook.x * 0.85
    ramp = np.clip((t - 12.0) / 1.75, 0, 1) * (t < 13.75)
    synth = synth * (1 - ramp * 0.75) + hp(synth, 900) * ramp * 0.75
    music = synth + bass.x * 0.8 + drums.x * 0.9 + perc.x * 0.8

    # Mix automation: each part sits at its own level, so the film has a shape (quiet start,
    # lift at 4 s, darker and lower while the AI reads, a build, the drop biggest).
    level = np.interp(
        t,
        [0, 3.9, 4.0, 5.9, 6.0, 9.9, 10.0, 13.75, 14.0, 21.5, 22.0, 25.5, 26.0, 30.0],
        [0.42, 0.42, 0.68, 0.68, 0.5, 0.5, 0.45, 0.8, 1.0, 1.0, 0.92, 0.92, 0.95, 0.95],
    )
    music = music * level

    # Dead stops: before the drop, and one beat before the payoff hit.
    for a, b in ((13.75, 14.0), (sec(1290), sec(1320))):
        k = int(0.004 * SR)
        i, j = int(a * SR), int(b * SR)
        music[:, i - k : i] *= np.linspace(1, 0, k)
        music[:, i:j] = 0
        music[:, j : j + k] *= np.linspace(0, 1, k)
    return music


# --- Sound effects ------------------------------------------------------------------------------


def click() -> np.ndarray:
    t = times(0.12)
    press = bp(noise(len(t)), 2000, 6000) * np.exp(-t / 0.0012) + np.sin(2 * np.pi * 3100 * t) * np.exp(-t / 0.003) * 0.4
    release = np.roll(bp(noise(len(t)), 2600, 7000) * np.exp(-t / 0.001) * 0.45, int(0.075 * SR))
    body = np.sin(2 * np.pi * 380 * t) * np.exp(-t / 0.006) * 0.3
    return tail_fade((press + release + body) * 0.7)


def key(space: bool) -> np.ndarray:
    t = times(0.09)
    c = rng.uniform(2800, 4600)
    top = bp(noise(len(t)), c * 0.7, c * 1.3) * np.exp(-t / rng.uniform(0.0025, 0.0045))
    f = rng.uniform(170, 240) * (0.65 if space else 1.0)
    thock = np.sin(2 * np.pi * f * t) * np.exp(-t / (0.02 if space else 0.012)) * 0.6
    clack = bp(noise(len(t)), 500, 1600) * np.exp(-t / 0.006) * (0.5 if space else 0.25)
    rattle = np.roll(bp(noise(len(t)), 2000, 5000) * np.exp(-t / 0.003) * 0.2, int(0.03 * SR)) if space else 0
    return tail_fade((top + thock + clack + rattle) * rng.uniform(0.75, 1.0) * 0.6)


def tick(pitch: float = 1.0) -> np.ndarray:
    t = times(0.08)
    return tail_fade((np.sin(2 * np.pi * 1800 * pitch * t) * np.exp(-t / 0.012) + bp(noise(len(t)), 3000, 7000) * np.exp(-t / 0.001) * 0.3) * 0.4)


def whoosh(seconds: float) -> np.ndarray:
    t = times(seconds)
    n = len(t)
    pink = np.cumsum(noise(n)) * 0.03
    pink = hp(pink - pink.mean(), 120)
    centre = np.interp(t, [0, seconds * 0.55, seconds], [350, 2600, 600])
    out = np.zeros((2, n))
    step = 512
    for i in range(0, n, step):
        c = centre[i]
        seg = bp(pink[max(0, i - 2048) : i + step], c / 1.7, c * 1.7)[-min(step, n - i) :]
        out[:, i : i + len(seg)] += pan2(seg, -0.6 + 1.2 * i / n)
    out *= np.sin(np.pi * np.clip(t / seconds, 0, 1)) ** 2
    return out / (np.abs(out).max() + 1e-9) * 0.5


def pin() -> np.ndarray:
    t = times(0.3)
    f = np.interp(t, [0, 0.05], [1100, 520])
    tock = np.sin(2 * np.pi * np.cumsum(f) / SR) * decay(t, 0.001, 0.05)
    thump = np.sin(2 * np.pi * 110 * t) * np.exp(-t / 0.06) * 0.6
    return tail_fade((tock * 0.6 + thump) * 0.7)


def riser(seconds: float) -> np.ndarray:
    t = times(seconds)
    k = t / seconds
    n = len(t)
    nz = noise(n)
    out = np.zeros(n)
    step = 1024
    for i in range(0, n, step):
        c = 400 * (9000 / 400) ** (i / n)
        out[i : i + step] = hp(nz[max(0, i - 4096) : i + step], c)[-min(step, n - i) :]
    tone = sum(lp(signal.chirp(t, hz(m), seconds, hz(m + 12), method="logarithmic"), 3000) for m in (50, 57, 62)) / 3
    return np.stack([out * 0.45 + tone * 0.3, np.roll(out, 400) * 0.45 + tone * 0.3]) * k**2.2


def boom(length: float = 1.4, v: float = 1.0) -> np.ndarray:
    t = times(length)
    f = 38 + 55 * np.exp(-t / 0.09)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.35)
    burst = lp(noise(len(t)), 2500) * np.exp(-t / 0.025) * 0.35
    return tail_fade(np.tanh(1.4 * (body + burst)) * 0.9 * v, 30)


def rumble(seconds: float) -> np.ndarray:
    t = times(seconds)
    x = lp(np.cumsum(noise(len(t))) * 0.02, 180)
    x = hp(x - x.mean(), 30)
    x /= np.abs(x).max() + 1e-9
    return x * np.sin(np.pi * np.clip(t / seconds, 0, 1)) ** 1.5 * 0.6


def shimmer(seconds: float) -> np.ndarray:
    n = int(SR * seconds)
    out = np.zeros((2, n))
    for _ in range(int(seconds * 28)):
        m = int(rng.choice(PENTA[12:22]))
        g = fm_bell(hz(m), 0.12, ratio=3, index=0.6, length=0.05) * np.hanning(int(SR * 0.12)) * 10 ** (rng.uniform(-20, -8) / 20)
        i = int(rng.integers(0, max(1, n - len(g))))
        out[:, i : i + len(g)] += pan2(g, rng.uniform(-0.85, 0.85))
    t = np.arange(n) / SR
    air = bp(noise(n), 6500, 11000) * 0.05 * (0.6 + 0.4 * np.sin(2 * np.pi * 0.7 * t))
    out += np.stack([air, np.roll(air, 300)])
    return out * (np.clip(t / 0.4, 0, 1) * np.clip((seconds - t) / 0.6, 0, 1))


def trace_note(index: int) -> np.ndarray:
    m = PENTA[min(index + 1, len(PENTA) - 1)]
    t = times(0.35)
    v = np.sin(2 * np.pi * hz(m) * t + 1.2 * np.exp(-t / 0.03) * np.sin(2 * np.pi * 2 * hz(m) * t))
    return tail_fade((v * decay(t, 0.001, 0.12) + bp(noise(len(t)), 4000, 9000) * np.exp(-t / 0.001) * 0.2) * 0.55)


def swish() -> np.ndarray:
    return whoosh(0.35) * 0.5


def pop(up: bool = True, pitch: float = 1.0) -> np.ndarray:
    t = times(0.16)
    f = np.interp(t, [0, 0.04], [380 * pitch, 820 * pitch] if up else [700 * pitch, 330 * pitch])
    v = np.sin(2 * np.pi * np.cumsum(f) / SR) * decay(t, 0.002, 0.05)
    return tail_fade(v * 0.65)


def build(seconds: float) -> np.ndarray:
    t = times(seconds)
    f = np.interp(t, [0, seconds], [70, 190])
    tone = lp(np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.25 * signal.sawtooth(2 * np.pi * np.cumsum(f) / SR), 600)
    e = np.clip(t / 0.08, 0, 1) * np.clip((seconds - t) / 0.08, 0, 1)
    return (tone * 0.45 + rumble(seconds) * 0.6) * e


def thud() -> np.ndarray:
    t = times(0.25)
    paper = bp(noise(len(t)), 150, 1200) * np.exp(-t / 0.03) * 0.6
    body = np.sin(2 * np.pi * 90 * t) * np.exp(-t / 0.05) * 0.7
    return tail_fade((paper + body) * 0.8)


def scan(seconds: float) -> np.ndarray:
    t = times(seconds)
    n = len(t)
    nz = noise(n)
    out = np.zeros(n)
    step = 1024
    for i in range(0, n, step):
        c = 6500 * (900 / 6500) ** (i / n)
        out[i : i + step] = bp(nz[max(0, i - 4096) : i + step], c / 1.25, c * 1.25)[-min(step, n - i) :]
    e = np.clip(t / 0.15, 0, 1) * np.clip((seconds - t) / 0.2, 0, 1)
    return np.stack([out, np.roll(out, 240)]) * e * 0.25


def detect(row: int, col: int) -> np.ndarray:
    m = PENTA[5 + 2 * row + col]
    return fm_bell(hz(m), 0.5, ratio=2, index=2.5, length=0.18) * 0.45


def glass(index: int) -> np.ndarray:
    m = int(rng.choice(PENTA[20:27]))
    t = times(0.12)
    return tail_fade(np.sin(2 * np.pi * hz(m) * t) * decay(t, 0.0008, 0.035) * 0.25)


def dots() -> np.ndarray:
    out = np.zeros(int(SR * 0.45))
    for k in range(3):
        s = tick(1.15 + 0.05 * k) * 0.45
        i = int(SR * 0.13 * k)
        out[i : i + len(s)] += s
    return out


def message() -> np.ndarray:
    t = times(0.14)
    sweep = bp(noise(len(t)), 1200, 6000) * np.sin(np.pi * t / 0.14) ** 2 * 0.25
    s = np.zeros(int(SR * 0.3))
    s[: len(sweep)] += sweep
    p = pop(True, 1.15)
    i = int(SR * 0.1)
    s[i : i + len(p)] += p[: len(s) - i]
    return s


def grab() -> np.ndarray:
    t = times(0.06)
    return tail_fade((lp(noise(len(t)), 1800) * np.exp(-t / 0.004) * 0.6 + np.sin(2 * np.pi * 300 * t) * np.exp(-t / 0.01) * 0.5) * 0.6)


def slider(value: int) -> np.ndarray:
    t = times(0.05)
    f = 1300 * 2 ** ((value - 1) / 16)
    return tail_fade((np.sin(2 * np.pi * f * t) * np.exp(-t / 0.006) + bp(noise(len(t)), 3000, 8000) * np.exp(-t / 0.0008) * 0.4) * 0.35)


def roll(to: str) -> np.ndarray:
    p = {"F": 1.0, "E": 1.06, "D": 1.12, "C": 1.19, "B": 1.26}.get(to, 1.0)
    out = np.zeros(int(SR * 0.18))
    for k in range(4):
        s = tick(p * (0.9 + 0.08 * k)) * (0.6 if k < 3 else 0.9)
        i = int(SR * 0.024 * k)
        out[i : i + len(s)] += s
    return out


def toggle() -> np.ndarray:
    out = np.zeros(int(SR * 0.25))
    for k, s in enumerate((click() * 0.5, pop(True, 1.3) * 0.5)):
        i = int(SR * 0.05 * k)
        out[i : i + len(s)] += s[: len(out) - i]
    return out


def sweep() -> np.ndarray:
    seconds = 0.7
    t = times(seconds)
    n = len(t)
    nz = noise(n)
    out = np.zeros(n)
    for i in range(0, n, 1024):
        c = 3000 * (11000 / 3000) ** (i / n)
        out[i : i + 1024] = bp(nz[max(0, i - 4096) : i + 1024], c / 1.3, min(c * 1.3, 20000))[-min(1024, n - i) :]
    e = np.sin(np.pi * t / seconds) ** 2
    st = np.stack([out * e * np.linspace(1, 0.2, n), out * e * np.linspace(0.2, 1, n)]) * 0.3
    for k, m in enumerate(PENTA[14:19]):
        b = fm_bell(hz(m), 0.4, ratio=3, index=1, length=0.12) * 0.12
        i = int(SR * 0.1 * k)
        st[:, i : i + len(b)] += pan2(b, -0.6 + 0.3 * k)[:, : n - i]
    return st


def chime() -> np.ndarray:
    out = np.zeros(int(SR * 1.8))
    for k, m in enumerate((74, 79, 83)):
        b = fm_bell(hz(m), 1.6, ratio=2, index=2, length=0.7) * (0.5 if k < 2 else 0.35)
        i = int(SR * 0.08 * k)
        out[i : i + len(b)] += b[: len(out) - i]
    return out


def hit() -> np.ndarray:
    b = boom(1.0, 0.75)
    burst = hp(noise(len(b)), 3000) * np.exp(-np.arange(len(b)) / SR / 0.05) * 0.25
    return b + burst


def count(index: int) -> np.ndarray:
    t = times(0.05)
    f = 900 * 2 ** (index / 28)
    return tail_fade((np.sin(2 * np.pi * f * t) * np.exp(-t / 0.008) + bp(noise(len(t)), 1500, 4000) * np.exp(-t / 0.001) * 0.3) * 0.3)


def paper() -> np.ndarray:
    seconds = 0.45
    t = times(seconds)
    grain = np.abs(noise(len(t))) ** 3
    crinkle = bp(noise(len(t)), 1200, 6000) * lp(grain, 60) * 3
    e = np.sin(np.pi * t / seconds) ** 2
    return np.stack([crinkle * e * np.linspace(0.4, 1, len(t)), crinkle * e * np.linspace(1, 0.4, len(t))]) * 0.4


def success() -> np.ndarray:
    out = np.zeros(int(SR * 0.6))
    for k, m in enumerate((74, 79)):
        b = fm_bell(hz(m), 0.5, ratio=2, index=1.2, length=0.15) * 0.35
        i = int(SR * 0.07 * k)
        out[i : i + len(b)] += b[: len(out) - i]
    return out


def reverse_swell(seconds: float) -> np.ndarray:
    c = crash(1.2, 1.0)[:, ::-1]
    return c * np.linspace(0.2, 1, c.shape[1]) * 0.9


def final() -> np.ndarray:
    b = boom(1.8, 1.0)
    t = np.arange(len(b)) / SR
    air = hp(noise(len(b)), 6000) * np.exp(-t / 0.4) * 0.12
    return b + air


def block(index: int) -> np.ndarray:
    return marimba((79, 83, 86)[index], 0.55) + fm_bell(hz((79, 83, 86)[index] + 12), 0.6, ratio=2, index=1, length=0.2)[: int(SR * 0.6)] * 0.15


def bell() -> np.ndarray:
    out = np.zeros(int(SR * 3.2))
    for k, (m, g) in enumerate(((79, 0.5), (86, 0.35), (91, 0.25))):
        b = fm_bell(hz(m), 3.0, ratio=2, index=1.8, length=1.2) * g
        i = int(SR * 0.012 * k)
        out[i : i + len(b)] += b[: len(out) - i]
    return out


def bloom() -> np.ndarray:
    seconds = 1.3
    t = times(seconds)
    tone = sum(np.sin(2 * np.pi * hz(m) * t) for m in (67, 74, 79)) / 3
    air = bp(noise(len(t)), 800, 5000)
    sw = np.interp(t, [0, seconds], [0.2, 1.0])
    x = lp(tone * 0.7 + air * 0.25 * sw, 2500)
    e = np.clip(t / 0.45, 0, 1) ** 2 * np.clip((seconds - t) / 0.85, 0, 1)
    return np.stack([x, np.roll(x, 200)]) * e * 0.45


# Gains per sound: the interface reads clearly over the music, the textures sit under it.
SFX = {
    "bloom": (lambda c: bloom(), 0.8),
    "click": (lambda c: click(), 0.9),
    "key": (lambda c: key(c.get("space", False)), 0.75),
    "tick": (lambda c: tick(c.get("pitch", 1.0)), 0.7),
    "whoosh": (lambda c: whoosh(c.get("seconds", 0.45)), 0.75),
    "pin": (lambda c: pin(), 0.9),
    "riser": (lambda c: riser(c["seconds"]), 0.55),
    "boom": (lambda c: boom(), 0.75),
    "rumble": (lambda c: rumble(c["seconds"]), 0.7),
    "shimmer": (lambda c: shimmer(c["seconds"]), 0.4),
    "trace": (lambda c: trace_note(c["index"]), 0.32),
    "swish": (lambda c: swish(), 0.6),
    "room": (lambda c: marimba((64, 67, 71, 74, 78, 79, 83, 86)[c["index"]], 0.6), 0.5),
    "pop": (lambda c: pop(), 0.8),
    "build": (lambda c: build(c["seconds"]), 0.8),
    "thud": (lambda c: thud(), 0.9),
    "scan": (lambda c: scan(c["seconds"]), 0.6),
    "detect": (lambda c: detect(c["row"], c["col"]), 0.28),
    "glass": (lambda c: glass(c["index"]), 0.45),
    "impact": (lambda c: boom(1.6, 1.0), 0.8),
    "join": (lambda c: pop(True, c.get("pitch", 1.0)), 0.8),
    "dots": (lambda c: dots(), 0.7),
    "message": (lambda c: message(), 0.85),
    "grab": (lambda c: grab(), 0.8),
    "slider": (lambda c: slider(c["value"]), 0.8),
    "roll": (lambda c: roll(c.get("to", "F")), 0.8),
    "toggle": (lambda c: toggle(), 0.9),
    "sweep": (lambda c: sweep(), 0.8),
    "chime": (lambda c: chime(), 0.5),
    "hit": (lambda c: hit(), 0.9),
    "count": (lambda c: count(c["index"]), 0.6),
    "paper": (lambda c: paper(), 0.35),
    "success": (lambda c: success(), 0.8),
    "reverse": (lambda c: reverse_swell(c["seconds"]), 0.6),
    "final": (lambda c: final(), 0.8),
    "block": (lambda c: block(c["index"]), 0.8),
    "bell": (lambda c: bell(), 0.6),
}
HEAVY = ("boom", "impact", "hit", "final")


def effects(cues: list[dict]) -> np.ndarray:
    bus = Bus()
    for c in cues:
        make, gain = SFX[c["sound"]]
        s = make(c)
        t = sec(c["frame"])
        length = s.shape[-1] / SR
        if c["sound"] == "whoosh":
            t -= c.get("seconds", 0.45) * 0.55  # the peak lands on the frame
        elif c["sound"] == "riser":
            t -= length  # it ends on the frame
        elif c["sound"] == "reverse":
            t += c["seconds"] - length  # it ends at frame plus seconds
        pan = {"key": rng.uniform(-0.15, 0.15), "trace": 0.25 if c.get("index", 0) % 2 else -0.25,
               "detect": -0.4 + 0.2 * c.get("col", 0), "glass": rng.uniform(-0.8, 0.8)}.get(c["sound"], 0.0)
        bus.add(s, t, gain * 10 ** (rng.uniform(-1.0, 1.0) / 20), pan)
    return room(bus.x, 0.3, 0.1)


# --- Master -------------------------------------------------------------------------------------


def limit(x: np.ndarray, ceiling_db: float) -> np.ndarray:
    """A look ahead limiter whose gain follows the 4x oversampled peak, so true peaks stay down."""
    ceiling = 10 ** (ceiling_db / 20)
    over = np.abs(signal.resample_poly(x, 4, 1, axis=1)).max(axis=0)
    peak = over[: 4 * x.shape[1]].reshape(-1, 4).max(axis=1)
    need = np.minimum(1.0, ceiling / np.maximum(peak, 1e-9))
    look = int(0.004 * SR)
    held = ndimage.minimum_filter1d(np.pad(need, (look, look), constant_values=1), size=2 * look + 1)[look:-look]
    rel = np.exp(-1 / (0.06 * SR))
    g = np.empty_like(held)
    cur = 1.0
    for i, h in enumerate(held):
        cur = h if h < cur else cur * rel + h * (1 - rel)
        g[i] = cur
    g = ndimage.uniform_filter1d(g, look)  # soften the attack edge without letting peaks through
    return x * np.minimum(g, held)


def true_peak(x: np.ndarray) -> float:
    return 20 * np.log10(np.abs(signal.resample_poly(x, 4, 1, axis=1)).max())


def main() -> None:
    cues = json.loads((ROOT / "src" / "ad" / "cues.json").read_text())
    music = score()
    sfx = effects(cues)

    # The music gives way a little under the big hits.
    t = np.arange(N) / SR
    duck = np.ones(N)
    for c in cues:
        if c["sound"] in HEAVY:
            k = sec(c["frame"])
            m = (t >= k) & (t < k + 0.6)
            duck[m] = np.minimum(duck[m], 1 - 0.3 * np.exp(-(t[m] - k) / 0.25))
    mix = music * duck + sfx * 1.0

    mix = fx(mix, HighpassFilter(28), Compressor(threshold_db=-16, ratio=1.8, attack_ms=25, release_ms=160))
    end = (t >= 28.3) * np.clip((29.8 - t) / 1.5, 0, 1) ** 2 + (t < 28.3)
    mix *= end

    meter = pyloudnorm.Meter(SR)
    for _ in range(8):
        mix *= 10 ** ((-14 - meter.integrated_loudness(mix.T)) / 20)
        tp = true_peak(mix)
        if tp <= -1.05:
            break
        mix = limit(mix, -1.4)
    if true_peak(mix) > -1.0:
        mix *= 10 ** ((-1.05 - true_peak(mix)) / 20)
    loud = meter.integrated_loudness(mix.T)
    print(f"loudness {loud:.2f} LUFS, true peak {true_peak(mix):.2f} dBTP, length {mix.shape[1] / SR:.3f} s")
    # The energy over time, every half second, short term loudness (3 s window is too long here).
    w = SR // 2
    rms = [20 * np.log10(np.sqrt((mix[:, i : i + w] ** 2).mean()) + 1e-9) for i in range(0, N, w)]
    print("rms per 0.5 s:", " ".join(f"{r:.0f}" for r in rms))
    soundfile.write(ROOT / "public" / "ad.wav", mix.T.astype(np.float32), SR, subtype="PCM_24")


if __name__ == "__main__":
    main()
