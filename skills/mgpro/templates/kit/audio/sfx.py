"""
Sound effects for picture events, tuned to the film. Every tonal effect takes notes from the
film's own scale (pass the Key), and a CHARACTER decides what the interface is made of:

    glass    bright sine and FM tings, airy whooshes       (precise, premium, light brands)
    wood     mallet and marimba knocks, dry whooshes       (calm, crafted, puzzle and reading apps)
    metal    clangs, bells, ringing partials               (hard, physical, fitness and hardware)
    digital  square blips, bit crushed clicks, zaps        (games, developer tools, retro)
    soft     felt, breath, low passed everything           (wellbeing, sleep, kids)

Effects are placed by score.py from cues.json. Risers and reverse swells END on their frame;
whooshes PEAK on their frame; everything else starts on it.
"""

from __future__ import annotations

import numpy as np

from dsp import SR, bp, crush, fade, fm, hp, lp, noise, pan2, perc, rng, sat, sine, square, sweep_lp
from instruments import keys

CHARACTERS = ("glass", "wood", "metal", "digital", "soft")


def note(key, i: int, octave: int = 5) -> int:
    """The i-th note of the film's scale, counted up from the tonic in the given octave."""
    return key.degree(i, octave - 3)


def blip(key, i: int, character: str, v: float = 0.6, length: float = 0.12):
    """A tonal tap for UI events: pitched up the scale with i, so runs become phrases."""
    m = note(key, i)
    f = 440 * 2 ** ((m - 69) / 12)
    n = int(SR * (length + 0.3))
    if character == "glass":
        x = fm(f, n, ratio=3.0, index=1.5, index_decay=0.02) * perc(n, 0.001, length)
    elif character == "wood":
        x = keys("mallet", m, length, 1.0)[:n]
        x = np.pad(x, (0, max(0, n - len(x))))
    elif character == "metal":
        x = fm(f, n, ratio=3.5, index=4.0, index_decay=0.05) * perc(n, 0.001, length * 2)
    elif character == "digital":
        x = square(f, n, duty=0.25) * perc(n, 0.001, length * 0.6) * 0.5
        x = crush(x, 6, 2)
    else:
        x = lp(sine(f, n) + 0.2 * sine(2 * f, n), 2500) * perc(n, 0.006, length)
    return fade(x * v)


def tick(character: str, pitch: float = 1.0, v: float = 0.5):
    n = int(SR * 0.05)
    f = {"glass": 3200, "wood": 1400, "metal": 2600, "digital": 2000, "soft": 900}[character] * pitch
    x = sine(f, n) * perc(n, 0, 0.008) + bp(noise(n), 2000, 8000) * perc(n, 0, 0.002) * (0.2 if character == "soft" else 0.5)
    return fade(x * v)


def click(character: str, v: float = 0.7):
    """A press and a release 75 ms later."""
    n = int(SR * 0.12)
    press = bp(noise(n), 1500, 7000) * perc(n, 0, 0.0012) + sine(3100 if character != "soft" else 1200, n) * perc(n, 0, 0.006) * 0.4
    press += sine(380, n) * perc(n, 0, 0.012) * 0.5
    rel = np.zeros(n)
    k = int(0.075 * SR)
    rel[k:] = press[: n - k] * 0.35
    return fade((press + rel) * v)


def whoosh(seconds: float = 0.5, character: str = "glass", v: float = 0.6, rise: bool = False):
    """Band passed noise whose centre sweeps up then down; pan crosses the field. Place it with
    its peak (55 percent in) on the frame."""
    n = int(SR * seconds)
    t = np.linspace(0, 1, n)
    lo, hi = {"glass": (500, 4200), "wood": (250, 1800), "metal": (400, 3500), "digital": (300, 5000), "soft": (200, 1200)}[character]
    centre = lo + (hi - lo) * (np.sin(np.pi * t) if not rise else t**2)
    x = sweep_lp(hp(noise(n), lo * 0.6), centre * 1.8, 1.4)
    env = np.sin(np.pi * np.clip(t * 1.1, 0, 1)) ** 2
    pan = np.linspace(-0.7, 0.7, n)
    out = np.stack([x * env * np.cos((pan + 1) * np.pi / 4), x * env * np.sin((pan + 1) * np.pi / 4)])
    if character == "digital":
        out = np.stack([crush(c, 8, 3) for c in out])
    return out * v


def riser(key, seconds: float = 1.5, character: str = "glass", v: float = 0.6):
    """Noise opening upward plus three chirps climbing an octave to the tonic. ENDS on its frame."""
    n = int(SR * seconds)
    t = np.linspace(0, 1, n)
    x = sweep_lp(hp(noise(n), 300), 400 + 9000 * t**2, 1.2) * 0.6
    top = 440 * 2 ** ((note(key, 7, 5) - 69) / 12)
    for k in range(3):
        f = top / 2 * 2 ** t * (1 + 0.004 * k)
        x += (sine(f, n) if character != "digital" else square(f, n) * 0.5) * 0.12
    return fade(x * t**2.2 * v, 3)


def reverse_swell(seconds: float = 1.0, v: float = 0.6):
    """A crash played backwards: ENDS on its frame."""
    n = int(SR * seconds)
    x = hp(noise(n), 3500) * perc(n, 0.002, seconds / 3)
    return fade(x[::-1] * v, 2)


def impact(character: str = "glass", v: float = 1.0, length: float = 1.2):
    """The big hit for a drop or a reveal: sub body, a noise burst, and a character layer."""
    n = int(SR * length)
    t = np.arange(n) / SR
    x = sine(38 + 55 * np.exp(-t / 0.09), n) * perc(n, 0.001, 0.35)
    x += lp(noise(n), 900) * perc(n, 0.001, 0.08) * 0.6
    if character == "metal":
        for f in (310, 547, 893, 1420):
            x += sine(f, n) * perc(n, 0, 0.25) * 0.08
    elif character == "glass":
        x += hp(noise(n), 5000) * perc(n, 0, 0.4) * 0.15
    elif character == "wood":
        x += sine(180, n) * perc(n, 0, 0.12) * 0.4
    elif character == "digital":
        x = crush(x, 7, 2)
    return fade(sat(x, 1.6) * v)


def sub_drop(seconds: float = 1.2, v: float = 0.8):
    """A falling sub: the floor drops away (a transition into a lower, darker section)."""
    n = int(SR * seconds)
    t = np.arange(n) / SR
    return fade(sine(90 * np.exp(-t / 0.4) + 28, n) * perc(n, 0.005, seconds / 2.5) * v)


def chime(key, character: str = "glass", v: float = 0.5, degrees=(0, 2, 4)):
    """A success: chord tones 80 ms apart."""
    parts = [blip(key, d + 7, character, v, 0.4) for d in degrees]
    n = max(len(p) for p in parts) + int(SR * 0.08 * len(parts))
    out = np.zeros(n)
    for i, p in enumerate(parts):
        k = int(SR * 0.08 * i)
        out[k : k + len(p)] += p
    return out


def stutter(source, slices: int = 6, slice_s: float = 0.045):
    """A glitch: the first slice of a sound repeated, getting shorter (hyperpop, digital)."""
    out = []
    for i in range(slices):
        k = int(SR * slice_s * (1 - i / (slices + 2)))
        out.append(fade(source[..., :k].copy(), 1))
    return np.concatenate(out, axis=-1)


def tape_stop(x, seconds: float = 0.6):
    """Slow a sound to a stop (the beat dying before a gap)."""
    n = x.shape[-1]
    speed = np.linspace(1, 0.02, int(SR * seconds))
    pos = np.cumsum(speed)
    pos = pos[pos < n - 1]
    return np.interp(pos, np.arange(n), x if x.ndim == 1 else x.mean(0))


def texture(seconds: float, character: str, key, v: float = 0.3):
    """A bed of tiny tonal grains (counting, scanning, data arriving), notes from the scale."""
    n = int(SR * seconds)
    out = np.zeros((2, n))
    for _ in range(int(seconds * 24)):
        i = int(rng.integers(0, n - int(SR * 0.3)))
        g = blip(key, int(rng.integers(5, 14)), character, rng.uniform(0.15, 0.5), 0.06)
        out[:, i : i + len(g)] += pan2(g, rng.uniform(-0.8, 0.8))[:, : n - i]
    return out * v
