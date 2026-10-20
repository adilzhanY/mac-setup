"""
Reference only: this film's music is taken (see music/registry.json). Read it for mixing ideas;
never start a new score from it. New films start from templates/kit/audio/score.py.

The torq film's soundtrack: a 120 BPM score in A minor (dark, hard, premium gym energy), and one
synthesized sound for every cue of src/cues.json, placed on the cue's frame (60 fps).
Writes public/torq.wav: 30.0 s, 48 kHz, stereo, 24 bit, about -14 LUFS, true peak below -1 dBTP.

    .venv/bin/python audio/synth.py
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






def marimba(m: int, v: float = 1.0) -> np.ndarray:
    t = times(0.6)
    f = hz(m)
    bar = np.sin(2 * np.pi * f * t) * np.exp(-t / 0.22) + 0.35 * np.sin(2 * np.pi * 4 * f * t) * np.exp(-t / 0.04)
    mallet = bp(noise(len(t)), 1500, 4000) * np.exp(-t / 0.002) * 0.15
    return tail_fade((bar + mallet) * v)


def kick(v: float = 1.0) -> np.ndarray:
    """Heavier and tighter than a pop kick: lower body, a harder click, more drive."""
    t = times(0.5)
    f = 44 + 150 * np.exp(-t / 0.024) + 60 * np.exp(-t / 0.003)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.22)
    click = bp(noise(len(t)), 2000, 9000) * np.exp(-t / 0.0018) * 0.45
    return tail_fade(np.tanh(2.4 * (body + click)) * 0.9 * v)


def bass_note(m: int, dur: float, v: float = 1.0, bright: float = 1.0) -> np.ndarray:
    """A sub sine plus a saw an octave up, filter closing fast, driven hard for grit."""
    t = times(dur + 0.05)
    g = gate(t, dur, 0.035) * np.clip(t / 0.003, 0, 1)
    sub = np.sin(2 * np.pi * hz(m) * t) * g
    raw = saw(hz(m + 12), len(t)) + 0.4 * saw(hz(m + 12) * 1.006, len(t))
    fe = np.exp(-t / 0.08) * bright
    mid = (lp(raw, 320) * (1 - fe) + lp(raw, 2600) * fe) * decay(t, 0.003, 0.35) * g
    grit = np.tanh(3.0 * (0.8 * sub + 0.6 * mid))
    return tail_fade((0.55 * grit + 0.45 * np.tanh(1.2 * sub)) * v)


def dark_pluck(m: int, dur: float, v: float = 1.0, cut: float = 2400) -> np.ndarray:
    t = times(dur + 0.35)
    raw = saw(hz(m), len(t)) * 0.7 + saw(hz(m) * 0.997, len(t)) * 0.3
    fe = np.exp(-t / 0.045)
    x = lp(raw, cut * 0.3) * (1 - fe) + lp(raw, cut) * fe
    return tail_fade(x * decay(t, 0.002, 0.28) * gate(t, dur, 0.12) * v)


def pluck_chord(notes, dur, v, cut) -> np.ndarray:
    n = int(SR * (dur + 0.4))
    out = np.zeros(n)
    for k, m in enumerate(notes):
        s = dark_pluck(m, dur, v * (0.85 + 0.15 * rng.random()), cut)
        i = int(SR * 0.005 * k)
        out[i : i + len(s)] += s[: n - i]
    return out / len(notes) * 1.7


def pluck(m: int, dur: float, v: float = 1.0) -> np.ndarray:
    """The hook: two detuned saws through a fast filter, a sine sparkle an octave up."""
    t = times(dur + 0.4)
    raw = saw(hz(m), len(t)) * 0.7 + saw(hz(m) * 1.004, len(t)) * 0.3
    fe = np.exp(-t / 0.05)
    x = lp(raw, 1300) * (1 - fe) + lp(raw, 7000) * fe
    sparkle = np.sin(2 * np.pi * hz(m + 12) * t) * np.exp(-t / 0.1) * 0.25
    return tail_fade((x + sparkle) * decay(t, 0.002, 0.3) * gate(t, dur, 0.12) * v)


# --- The score ----------------------------------------------------------------------------------

CHORD = {
    "Am(add9)": ([45, 52, 57, 60, 64, 71], 33),
    "Am": ([57, 60, 64, 69], 33),
    "F": ([53, 57, 60, 65], 29),
    "Fmaj7": ([53, 57, 60, 64], 29),
    "C": ([48, 55, 60, 64], 36),
    "G": ([55, 59, 62, 67], 31),
    "Am9": ([57, 60, 64, 67, 71], 33),
    "Dm": ([50, 57, 62, 65], 38),
    "E": ([52, 56, 59, 64], 40),
}
TIMELINE = [
    (0, 240, "Am(add9)"),
    (240, 300, "Am"), (300, 360, "F"), (360, 390, "C"), (390, 420, "G"),
    (420, 510, "Am9"), (510, 600, "Fmaj7"),
    (600, 660, "Dm"), (660, 720, "F"), (720, 780, "G"), (780, 825, "E"),
    (840, 960, "Am"), (960, 1080, "F"), (1080, 1200, "C"), (1200, 1290, "G"),
    (1320, 1380, "Am"), (1380, 1440, "F"), (1440, 1500, "C"), (1500, 1530, "G"),
    (1560, 1800, "Am(add9)"),
]
SECTIONS = (
    ("intro", 0, 240), ("lift", 240, 420), ("engine", 420, 600), ("build", 600, 825), ("gap", 825, 840),
    ("drop", 840, 1290), ("stop", 1290, 1320), ("groove", 1320, 1530), ("swell", 1530, 1560), ("end", 1560, 1800),
)


def section(frame: float) -> str:
    return next(name for name, a, b in SECTIONS if a <= frame < b)


BOUNCY = [(0, 0, 2), (3, 12, 1), (6, 0, 1), (8, 0, 2), (10, 12, 1), (11, 7, 1), (14, 12, 1)]


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
        eighths = int(round(length / (BEAT / 2)))

        # Plucked chords: comping in the grooves, a slow arpeggio in the engine, stabs in the build.
        if part in ("lift", "drop", "groove"):
            cut = {"lift": 2200, "drop": 3800, "groove": 3200}[part]
            for pos, v, dur in ((0, 0.9, 0.5), (3, 0.6, 0.3), (6, 0.7, 0.4)):
                if pos < eighths:
                    keys.add(pluck_chord(notes, dur, v, cut), t0 + pos * BEAT / 2)
        elif part == "engine":
            arp = notes + [notes[1] + 12]
            for pos in range(eighths):
                k = (a - 420 + pos * 15) / 180
                keys.add(dark_pluck(arp[pos % len(arp)] + 12, 0.2, 0.55, 1200 + 2400 * k), t0 + pos * BEAT / 2, 0.75,
                         pan=-0.35 if pos % 2 else 0.35)
        elif part == "build":
            for pos in range(1, eighths, 2):
                k = (a - 600 + pos * 15) / 225
                keys.add(pluck_chord(notes, 0.15, 0.5 + 0.4 * k, 1600 + 3600 * k), t0 + pos * BEAT / 2, 0.85)
        elif part == "end":
            keys.add(pluck_chord(notes, 3.2, 1.0, 3000), t0, 1.1)

        # Pads.
        if part == "intro":
            pad.add(pad_chord(notes, length + 0.3, 900, attack=2.5), t0, 0.8)
        elif part == "engine":
            pad.add(pad_chord([m + 12 for m in notes], length + 0.5, 4200, attack=0.6), t0, 0.7)
        elif part == "end":
            pad.add(pad_chord(notes, 4.0, 2000, attack=0.05), t0, 1.1)
        elif part in ("lift", "build", "drop", "groove"):
            g = {"lift": 0.5, "build": 0.5, "drop": 0.55, "groove": 0.5}[part]
            pad.add(pad_chord(notes, length + 0.25, 2200), t0, g)

        # Supersaw stabs on the off 8ths in the drop, softer in the groove.
        if part in ("drop", "groove"):
            stab = supersaw([m + 12 for m in notes], 0.2, 4500)
            for pos in range(1, eighths, 2):
                stabs.add(stab, t0 + pos * BEAT / 2, 0.8 if part == "drop" else 0.5)
        if part == "end":
            stabs.add(supersaw([m + 12 for m in notes], 1.0, 4500), t0, 0.9)

        # Bass.
        if part in ("lift", "drop", "groove"):
            for step, interval, steps in BOUNCY:
                f = a + step * 7.5
                if f < b:
                    bass.add(bass_note(root + interval, steps * S16 * 0.9, 0.9), sec(f))
        elif part == "engine":
            for pos in range(eighths):
                k = (a - 420 + pos * 15) / 180
                bass.add(bass_note(root, BEAT / 2 * 0.7, 0.75, bright=0.1 + 0.7 * k), t0 + pos * BEAT / 2)
        elif part == "build":
            step = 15 if a < 720 else 7.5
            f = a
            while f < b:
                bass.add(bass_note(root, sec(step) * 0.7, 0.8, bright=0.5 + 0.5 * (f - 600) / 225), sec(f))
                f += step
        elif part == "end":
            bass.add(bass_note(root, 3.2, 1.0, bright=0.6), t0)

    # The intro sub swell: an A under everything, rising into the lift.
    t = times(sec(240))
    swell = np.sin(2 * np.pi * hz(33) * t) * (t / t[-1]) ** 1.6 * 0.5
    bass.add(swell, 0.0)

    # Kicks.
    for f in range(240, 420, 30):
        kick_at(f)
    for bar in (420, 540):
        kick_at(bar)
        if bar + 75 < 600:
            kick_at(bar + 75, 0.8)
        perc.add(snap(0.9), sec(bar + 60))  # the rim on 3 in half time
    for f in range(600, 825, 30):
        kick_at(f, 0.85 + 0.15 * (f - 600) / 225)
    for f in range(840, 1290, 30):
        kick_at(f, 1.05)
    for f in range(1320, 1530, 30):
        kick_at(f)
    kick_at(1560, 1.15)

    # Snaps on 2 and 4 in the intro and lift, claps from the lift on.
    for f in range(90, 420, 60):
        perc.add(snap(0.85), sec(f), pan=0.15)
    claps = list(range(270, 420, 60)) + list(range(630, 825, 60)) + list(range(870, 1290, 60)) + list(range(1350, 1530, 60))
    for f in claps:
        perc.add(clap(0.95 if f >= 840 else 0.75), sec(f))
        if f >= 840:
            perc.add(snap(0.55), sec(f) + 0.004, pan=-0.2)

    # Hats: filtered 16ths in the intro, offbeats in the lift, quiet 8ths in the engine,
    # building 16ths in the build, open offbeats plus 16ths in the drop and groove.
    f = 0.0
    while f < 240:
        perc.add(lp(hat(0.02, 0.5 + 0.3 * (int(f / 7.5) % 2 == 0)), 6000 + 4000 * f / 240), sec(f), 0.6, pan=0.25)
        f += 7.5
    for f in range(255, 420, 30):
        perc.add(hat(0.035, 0.85), sec(f), pan=-0.25)
    for f in range(420, 600, 15):
        perc.add(hat(0.02, 0.35), sec(f), pan=0.3)
    f = 600.0
    while f < 825:
        k = (f - 600) / 225
        perc.add(hat(0.025, 0.35 + 0.55 * k * (1.0 if int(f / 7.5) % 2 == 0 else 0.6)), sec(f), pan=-0.25)
        f += 7.5
    for a, b in ((840, 1290), (1320, 1530)):
        for f in range(a + 15, b, 30):
            perc.add(hat(0.16, 0.75), sec(f), pan=-0.3)
        g = float(a)
        while g < b:
            perc.add(hat(0.02, 0.32 + 0.1 * rng.random()), sec(g), pan=0.3)
            g += 7.5

    # The snare roll into the drop: 8ths, 16ths, 32nds, 64ths, louder and brighter.
    for start, end, step in ((600, 690, 15), (690, 750, 7.5), (750, 795, 3.75), (795, 825, 1.875)):
        f = float(start)
        while f < end:
            k = (f - 600) / 225
            drums.add(snare(0.18 + 0.82 * k**1.5, 200 + 1800 * k), sec(f))
            f += step

    for f, v in ((840, 1.0), (1320, 0.9), (1560, 1.0)):
        perc.add(crash(2.6, v), sec(f))

    # The hook in A minor pentatonic: call and response over the four drop bars.
    call = [(0, 76, 2), (2, 74, 1), (3, 72, 2), (6, 69, 2), (8, 72, 1), (10, 74, 2), (12, 76, 1), (14, 79, 2)]
    answer = [(0, 81, 3), (3, 79, 2), (6, 76, 2), (8, 74, 2), (10, 72, 2), (12, 69, 4)]
    call2 = [(0, 76, 2), (2, 74, 1), (3, 72, 2), (6, 69, 2), (8, 72, 1), (10, 74, 2), (12, 79, 1), (14, 81, 2)]
    answer2 = [(0, 84, 3), (3, 81, 2), (6, 79, 2), (8, 76, 3)]
    for bar, phrase in ((840, call), (960, answer), (1080, call2), (1200, answer2)):
        for step, m, steps in phrase:
            hook.add(pluck(m, steps * S16 * 0.85, 0.8), sec(bar + step * 7.5), pan=-0.1)
            hook.add(pluck(m + 12, steps * S16 * 0.6, 0.2), sec(bar + step * 7.5) + 0.003, pan=0.25)

    # Effects per bus.
    perc.x = room(perc.x, 0.22, 0.2, 0.6)
    keys.x = fx(keys.x, Chorus(rate_hz=0.6, depth=0.2, centre_delay_ms=7.0, feedback=0.0, mix=0.35),
                Reverb(room_size=0.55, damping=0.5, wet_level=0.22, dry_level=1.0, width=1.0))
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
        duck[i:j] = np.minimum(duck[i:j], 1 - 0.5 * np.clip(seg / 0.003, 0, 1) * np.exp(-seg / 0.11))
    for b_ in (keys, pad, stabs, hook):
        b_.x *= duck
    bass.x *= np.clip(1 - (1 - duck) * 1.3, 0, 1)

    # The build thins the synths towards the drop, as if a high pass were opening.
    synth = keys.x * 0.85 + pad.x * 0.8 + stabs.x * 0.75 + hook.x * 0.85
    ramp = np.clip((t - 10.0) / 3.75, 0, 1) * (t < 13.75)
    synth = synth * (1 - ramp * 0.7) + hp(synth, 900) * ramp * 0.7
    music = synth + bass.x * 0.85 + drums.x * 0.9 + perc.x * 0.8

    # Mix automation: quiet start, lift at 4 s, lower in the engine, a build, the drop biggest.
    level = np.interp(
        t,
        [0, 3.95, 4.0, 6.95, 7.0, 9.95, 10.0, 13.75, 14.0, 21.5, 22.0, 25.5, 26.0, 30.0],
        [0.6, 0.6, 0.7, 0.7, 0.55, 0.55, 0.36, 0.55, 1.0, 1.0, 0.9, 0.9, 0.95, 0.95],
    )
    music = music * level

    # Dead stops: before the drop, the beat before the payoff, and the drums out before the end.
    k = int(0.004 * SR)
    for a, b in ((825, 840), (1290, 1320)):
        i, j = int(sec(a) * SR), int(sec(b) * SR)
        music[:, i - k : i] *= np.linspace(1, 0, k)
        music[:, i:j] = 0
        music[:, j : j + k] *= np.linspace(0, 1, k)
    i, j = int(sec(1530) * SR), int(sec(1560) * SR)
    music[:, i - k : i] *= np.linspace(1, 0, k)
    music[:, i:j] = 0
    music[:, j : j + k] *= np.linspace(0, 1, k)
    return music


# --- Sound effects ------------------------------------------------------------------------------

# A minor pentatonic, upwards from A3.
PENTA = [m for m in range(57, 110) if m % 12 in (9, 0, 2, 4, 7)]


def zip_up(seconds: float) -> np.ndarray:
    t = times(seconds)
    n = len(t)
    nz = noise(n)
    out = np.zeros(n)
    for i in range(0, n, 512):
        c = 500 * (7000 / 500) ** (i / n)
        out[i : i + 512] = bp(nz[max(0, i - 2048) : i + 512], c / 1.3, c * 1.3)[-min(512, n - i) :]
    tone = np.sin(2 * np.pi * np.cumsum(np.interp(t, [0, seconds], [220, 880])) / SR) * 0.25
    e = np.clip(t / 0.03, 0, 1) * np.clip((seconds - t) / 0.12, 0, 1)
    return np.stack([out * 0.4 + tone, np.roll(out, 200) * 0.4 + tone]) * e * 0.6


def slam(index: int) -> np.ndarray:
    """An iron plate hitting a loaded bar: a low thump plus inharmonic clang that rings briefly."""
    t = times(1.0)
    p = 1 + 0.07 * index + rng.uniform(-0.015, 0.015)
    f = 46 + 80 * np.exp(-t / 0.05)
    thump = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.25)
    base = 310 * p
    clang = sum(g * np.sin(2 * np.pi * base * r * t + rng.random() * 6.3) * np.exp(-t / dl)
                for r, g, dl in ((1.0, 0.5, 0.28), (2.76, 0.4, 0.2), (4.1, 0.25, 0.14), (5.4, 0.3, 0.11), (7.9, 0.18, 0.07)))
    crack = bp(noise(len(t)), 800, 6000) * np.exp(-t / 0.012) * 0.8
    mono = np.tanh(1.8 * (thump * 1.1 + crack)) + clang * 0.55
    return tail_fade(np.stack([mono, np.roll(mono, 90) * 0.96]) * 0.8, 30)


def collar() -> np.ndarray:
    t = times(0.15)
    click = hp(noise(len(t)), 4000) * np.exp(-t / 0.0015)
    ring = sum(np.sin(2 * np.pi * f * t) for f in (3400, 5100, 6900)) / 3 * np.exp(-t / 0.02)
    return tail_fade((click * 0.7 + ring * 0.5) * 0.7)


def blip(m: float, length: float = 0.12, v: float = 0.5) -> np.ndarray:
    t = times(length + 0.05)
    x = np.sin(2 * np.pi * hz(m) * t + 0.6 * np.exp(-t / 0.02) * np.sin(4 * np.pi * hz(m) * t))
    return tail_fade(x * decay(t, 0.001, length * 0.5) * v)


def run(ms, gap: float, length: float, v: float = 0.5) -> np.ndarray:
    out = np.zeros(int(SR * (gap * len(ms) + length + 0.1)))
    for k, m in enumerate(ms):
        s = blip(m, length, v)
        i = int(SR * gap * k)
        out[i : i + len(s)] += s
    return out


def set_done(index: int) -> np.ndarray:
    i0 = PENTA.index(76)
    return run([PENTA[i0 + index], PENTA[i0 + index + 2]], 0.03, 0.14, 0.42)


def pr_run() -> np.ndarray:
    out = run([76, 79, 84, 88], 0.05, 0.3, 0.42)
    n = len(out)
    return out + np.concatenate([np.zeros(int(SR * 0.15)), fm_bell(hz(88), 0.8, ratio=2, index=2, length=0.35) * 0.3])[:n]


def grain() -> np.ndarray:
    t = times(0.03)
    return tail_fade(np.sin(2 * np.pi * rng.uniform(2200, 5200) * t) * np.exp(-t / 0.004) * rng.uniform(0.15, 0.3))


def tier(index: int) -> np.ndarray:
    """A metal being forged one grade up: a struck clang plus an FM bell, brighter each time."""
    t = times(1.2)
    p = 2 ** (index * 2 / 12)
    clang = sum(np.sin(2 * np.pi * 420 * p * r * t + rng.random() * 6.3) * np.exp(-t / dl)
                for r, dl in ((1.0, 0.18), (2.32, 0.12), (3.87, 0.08), (5.9, 0.05))) / 4
    crack = hp(noise(len(t)), 2500 + 600 * index) * np.exp(-t / 0.006) * (0.4 + 0.08 * index)
    thump = np.sin(2 * np.pi * 70 * t) * np.exp(-t / 0.06) * 0.6
    m = PENTA[8 + index]
    ring = np.concatenate([fm_bell(hz(m), 1.0, ratio=3.5, index=2 + 0.4 * index, length=0.3 + 0.03 * index), np.zeros(int(SR * 0.2))])
    mono = clang * 0.6 + crack + thump + ring[: len(t)] * 0.5
    return tail_fade(np.stack([mono, np.roll(mono, 120)]) * 0.75, 30)


def swap() -> np.ndarray:
    w = whoosh(0.25) * 0.6
    p = pop(True, 1.25)
    i = int(SR * 0.12)
    out = np.zeros((2, max(w.shape[1], i + len(p))))
    out[:, : w.shape[1]] += w
    out[:, i : i + len(p)] += pan2(p, 0.0)
    return out


def chime() -> np.ndarray:
    out = np.zeros(int(SR * 1.8))
    for k, m in enumerate((76, 81, 84)):
        b = fm_bell(hz(m), 1.6, ratio=2, index=2, length=0.7) * (0.5 if k < 2 else 0.35)
        i = int(SR * 0.08 * k)
        out[i : i + len(b)] += b[: len(out) - i]
    return out


def block(index: int) -> np.ndarray:
    m = PENTA[5 + index]
    return marimba(m, 0.55) + fm_bell(hz(m + 12), 0.6, ratio=2, index=1, length=0.2) * 0.15


def bell(index: int) -> np.ndarray:
    if index < 8:
        return fm_bell(hz(PENTA[10 + index]), 0.6, ratio=2, index=2.2, length=0.2) * 0.5
    out = np.zeros(int(SR * 3.2))
    for k, (m, g) in enumerate(((81, 0.5), (88, 0.35), (93, 0.25))):
        b = fm_bell(hz(m), 3.0, ratio=2, index=1.8, length=1.2) * g
        i = int(SR * 0.012 * k)
        out[i : i + len(b)] += b[: len(out) - i]
    return out


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


def pop(up: bool = True, pitch: float = 1.0) -> np.ndarray:
    t = times(0.16)
    f = np.interp(t, [0, 0.04], [380 * pitch, 820 * pitch] if up else [700 * pitch, 330 * pitch])
    v = np.sin(2 * np.pi * np.cumsum(f) / SR) * decay(t, 0.002, 0.05)
    return tail_fade(v * 0.65)


def glass(index: int) -> np.ndarray:
    m = int(rng.choice(PENTA[20:27]))
    t = times(0.12)
    return tail_fade(np.sin(2 * np.pi * hz(m) * t) * decay(t, 0.0008, 0.035) * 0.25)


def message() -> np.ndarray:
    t = times(0.14)
    sweep = bp(noise(len(t)), 1200, 6000) * np.sin(np.pi * t / 0.14) ** 2 * 0.25
    s = np.zeros(int(SR * 0.3))
    s[: len(sweep)] += sweep
    p = pop(True, 1.15)
    i = int(SR * 0.1)
    s[i : i + len(p)] += p[: len(s) - i]
    return s


def hit() -> np.ndarray:
    b = boom(1.0, 0.75)
    burst = hp(noise(len(b)), 3000) * np.exp(-np.arange(len(b)) / SR / 0.05) * 0.25
    return b + burst


def count(index: int) -> np.ndarray:
    t = times(0.05)
    f = 900 * 2 ** (index / 28)
    return tail_fade((np.sin(2 * np.pi * f * t) * np.exp(-t / 0.008) + bp(noise(len(t)), 1500, 4000) * np.exp(-t / 0.001) * 0.3) * 0.3)


def reverse_swell(seconds: float) -> np.ndarray:
    c = crash(1.2, 1.0)[:, ::-1]
    return c * np.linspace(0.2, 1, c.shape[1]) * 0.9


def final() -> np.ndarray:
    b = boom(1.8, 1.0)
    t = np.arange(len(b)) / SR
    air = hp(noise(len(b)), 6000) * np.exp(-t / 0.4) * 0.12
    return b + air


# Gains per sound: the interface reads clearly over the music, the textures sit under it.
SFX = {
    "zip": (lambda c: zip_up(c["seconds"]), 0.6),
    "slam": (lambda c: slam(c["index"]), 0.75),
    "collar": (lambda c: collar(), 0.8),
    "whoosh": (lambda c: whoosh(c.get("seconds", 0.45)), 0.75),
    "boom": (lambda c: boom(), 0.8),
    "tick": (lambda c: tick(1.0 + 0.06 * c.get("index", 0)), 0.6),
    "set": (lambda c: set_done(c["index"]), 0.85),
    "pr": (lambda c: pr_run(), 0.8),
    "rest": (lambda c: blip(69, 0.08, 0.35), 0.7),
    "go": (lambda c: run([81, 88], 0.0, 0.25, 0.4), 0.85),
    "shimmer": (lambda c: shimmer(c["seconds"]), 0.45),
    "grain": (lambda c: grain(), 0.5),
    "pin": (lambda c: pin(), 0.9),
    "bell": (lambda c: bell(c["index"]), 0.55),
    "pop": (lambda c: pop(), 0.8),
    "crash": (lambda c: crash(2.4, 1.0), 0.55),
    "tier": (lambda c: tier(c["index"]), 0.55),
    "riser": (lambda c: riser(c["seconds"]), 0.5),
    "impact": (lambda c: boom(1.8, 1.0), 0.9),
    "glass": (lambda c: glass(c["index"]), 0.4),
    "count": (lambda c: count(c["index"]), 0.6),
    "swap": (lambda c: swap(), 0.8),
    "message": (lambda c: message(), 0.85),
    "blip": (lambda c: blip(PENTA[10 + c["index"]], 0.12, 0.45), 0.8),
    "chime": (lambda c: chime(), 0.3),
    "hit": (lambda c: hit(), 0.9),
    "reverse": (lambda c: reverse_swell(c["seconds"]), 0.6),
    "final": (lambda c: final(), 0.85),
    "block": (lambda c: block(c["index"]), 0.8),
}
HEAVY = ("boom", "impact", "hit", "final", "slam")


def effects(cues: list[dict]) -> np.ndarray:
    bus = Bus()
    for c in cues:
        make, gain = SFX[c["sound"]]
        s = make(c)
        t = sec(c["frame"])
        length = s.shape[-1] / SR
        if c["sound"] == "whoosh":
            t -= c.get("seconds", 0.45) * 0.55  # the peak lands on the frame
        elif c["sound"] in ("riser", "reverse"):
            t -= length  # both end on their frame
        pan = {"glass": rng.uniform(-0.8, 0.8), "grain": rng.uniform(-0.7, 0.7),
               "blip": -0.3 + 0.1 * c.get("index", 0), "bell": -0.35 + 0.1 * c.get("index", 0) if c.get("index", 0) < 8 else 0.0}.get(c["sound"], 0.0)
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
    cues = json.loads((ROOT / "src" / "cues.json").read_text())
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
    # The gap before the drop is dead silence for the effects too (the riser ends on its first frame).
    i, j, k = int(sec(825) * SR), int(sec(840) * SR), int(0.004 * SR)
    sfx[:, i - k : i] *= np.linspace(1, 0, k)
    sfx[:, i:j] = 0
    mix = music * duck + sfx * 0.5

    mix = fx(mix, HighpassFilter(28), Compressor(threshold_db=-16, ratio=1.8, attack_ms=25, release_ms=160))
    mix *= (t >= 28.3) * np.clip((29.8 - t) / 1.5, 0, 1) ** 2 + (t < 28.3)

    meter = pyloudnorm.Meter(SR)
    for _ in range(8):
        mix *= 10 ** ((-14 - meter.integrated_loudness(mix.T)) / 20)
        if true_peak(mix) <= -1.05:
            break
        mix = limit(mix, -1.4)
    if true_peak(mix) > -1.0:
        mix *= 10 ** ((-1.05 - true_peak(mix)) / 20)
    print(f"loudness {meter.integrated_loudness(mix.T):.2f} LUFS, true peak {true_peak(mix):.2f} dBTP, length {mix.shape[1] / SR:.3f} s")
    for name, a, b in SECTIONS:
        seg = mix[:, int(sec(a) * SR) : int(sec(b) * SR)]
        print(f"  {name:7s} {a:5d} to {b:5d}: {20 * np.log10(np.sqrt((seg**2).mean()) + 1e-9):6.1f} dB RMS")
    soundfile.write(ROOT / "public" / "torq.wav", mix.T.astype(np.float32), SR, subtype="PCM_24")


if __name__ == "__main__":
    main()
