"""
The instrument library. Every function returns one hit or one note as a numpy array (mono, or
stereo when the sound is wide by nature), at dsp.SR. A palette is a choice of KIND per role:
two films with different palettes should not share a kick, a bass or a lead.

    kick(kind)    house, punch, soft, boom, 808, dist, acoustic, taiko
    snare(kind)   tight, gated, brush, trap, rim, clap, snap, crack
    hat(kind)     closed, open, ride, shaker, tamb, 909, trap
    perc(kind)    conga, bongo, woodblock, cowbell, clave, tom, cabasa, triangle, agogo
    bass(kind)    sub, 808, reese, acid, pluck, fm, octave, upright, log, wobble
    keys(kind)    epiano, piano, organ, mallet, marimba, kalimba, vibes, steel, clav, nylon, harp, bell, celesta
    pad(kind)     saw, strings, choir, glass, warm, air
    lead(kind)    supersaw, square, sine, vowel, whistle, pluck, brass, flute, sync

Use the arguments (cut, bright, drive, decay) to tune a sound to the film rather than adding a
new instrument for each one. Add a new kind when a genre needs a sound none of these makes.
"""

from __future__ import annotations

import numpy as np

from dsp import (SR, adsr, bp, fade, fm, fold, hp, hz, karplus, lp, noise, pan2, peak, perc, rng, sat, saw, sine,
                 square, supersaw, sweep_lp, tri, widen)

VOWELS = {  # formant centres and widths (Hz): a, e, i, o, u
    "a": [(800, 80), (1150, 90), (2900, 120)],
    "e": [(400, 70), (1700, 80), (2600, 100)],
    "i": [(300, 50), (2200, 100), (3000, 120)],
    "o": [(450, 70), (800, 80), (2830, 100)],
    "u": [(325, 50), (700, 60), (2530, 100)],
}

# --- Drums -------------------------------------------------------------------------------------


def kick(kind="punch", v=1.0, tune=0.0):
    """tune in semitones moves the body pitch, so the kick can sit on the song's root."""
    k = 2 ** (tune / 12)
    spec = {  # (body Hz, sweep Hz, sweep time, length, click, drive)
        "house": (50, 110, 0.035, 0.32, 0.6, 1.6),
        "punch": (55, 140, 0.025, 0.2, 0.9, 1.8),
        "soft": (52, 70, 0.04, 0.24, 0.15, 1.1),
        "boom": (48, 120, 0.05, 0.42, 0.5, 2.2),
        "808": (44, 90, 0.06, 1.1, 0.25, 1.3),
        "dist": (50, 160, 0.03, 0.36, 1.0, 4.5),
        "acoustic": (64, 90, 0.02, 0.16, 1.2, 1.4),
        "taiko": (70, 50, 0.09, 0.9, 0.3, 1.2),
    }[kind]
    body, sweep, st, length, click, dr = spec
    n = int(SR * (length + 0.05))
    t = np.arange(n) / SR
    f = (body + sweep * np.exp(-t / st)) * k
    x = sine(f, n) * perc(n, 0.001, length / 2.2)
    x += click * hp(noise(n), 2500) * perc(n, 0.0003, 0.003) * 0.5
    if kind == "taiko":
        x += lp(noise(n), 400) * perc(n, 0.002, 0.18) * 0.6
    if kind == "acoustic":
        x += bp(noise(n), 1500, 5000) * perc(n, 0.0005, 0.012) * 0.4
    return fade(sat(x, dr) * v, 2)


def snare(kind="tight", v=1.0):
    n = int(SR * 0.6)
    t = np.arange(n) / SR
    if kind in ("clap",):
        x = np.zeros(n)
        for d in (0.0, 0.009, 0.019, 0.028):
            i = int(d * SR)
            x[i:] += bp(noise(n - i), 900, 2400) * perc(n - i, 0.0005, 0.004)
        x += bp(noise(n), 1000, 3000) * perc(n, 0.0, 0.11) * 0.5
        return fade(x * v * 0.9)
    if kind == "snap":
        x = bp(noise(n), 1700, 6000) * perc(n, 0.0003, 0.003) + sine(2150, n) * perc(n, 0.0, 0.011) * 0.4
        return fade(x * v)
    if kind == "rim":
        x = sine(1650, n) * perc(n, 0.0, 0.012) * 0.6 + sine(520, n) * perc(n, 0, 0.02) * 0.5
        x += bp(noise(n), 2000, 7000) * perc(n, 0, 0.004) * 0.6
        return fade(x * v)
    if kind == "brush":
        x = bp(noise(n), 2500, 9000) * adsr(n, 0.012, 0.09, 0.0, 0.05)
        return fade(x * v * 0.7)
    body, tone_len, noise_len, bright = {
        "tight": (190, 0.04, 0.09, 0.8),
        "gated": (170, 0.07, 0.22, 0.6),
        "trap": (210, 0.05, 0.13, 1.0),
        "crack": (240, 0.03, 0.06, 1.2),
    }[kind]
    f = body * (1 + 0.4 * np.exp(-t / 0.01))
    x = sine(f, n) * perc(n, 0.0005, tone_len) * 0.8
    x += bp(noise(n), 1800, 5000 + 4000 * bright) * perc(n, 0.0005, noise_len)
    if kind == "trap":
        x += hp(noise(n), 6000) * perc(n, 0, 0.03) * 0.4
    return fade(sat(x, 1.4) * v)


HAT_F = np.array([205.3, 304.4, 369.6, 522.7, 540.0, 800.0]) * 1.6


def hat(kind="closed", v=1.0):
    length = {"closed": 0.03, "open": 0.22, "ride": 0.9, "shaker": 0.06, "tamb": 0.14, "909": 0.05, "trap": 0.02}[kind]
    n = int(SR * (length * 2 + 0.02))
    if kind == "shaker":
        x = hp(noise(n), 5500, 4) * adsr(n, 0.012, 0.025, 0.0, 0.02)
        return fade(x * v * 0.8)
    if kind == "tamb":
        jingles = sum(sine(f, n) for f in rng.uniform(5000, 9000, 8)) / 8
        x = (hp(noise(n), 7000) * 0.7 + jingles * 0.4) * perc(n, 0.001, length / 2)
        return fade(x * v)
    metal = sum(np.sign(sine(f, n)) for f in HAT_F) / 6
    if kind == "ride":  # mostly ringing tone with a short tick; a noisy ride turns into a wall of hiss
        bell = sum(sine(f, n) * a for f, a in ((3150, 0.5), (4870, 0.35), (6420, 0.25), (8030, 0.15)))
        x = bell * perc(n, 0.001, 0.35) * 0.35 + bp(noise(n), 6000, 11000) * perc(n, 0, 0.012) * 0.3
        return fade(lp(x, 11000) * v * 0.7)
    x = bp(metal * 0.6 + noise(n) * 0.35, 7000, 13000) * perc(n, 0.0005, length)
    if kind == "909":
        x = hp(noise(n), 8000, 4) * perc(n, 0.0003, length) * 0.8
    if kind == "open":
        x *= 0.7
    return fade(x * v)


def crash(v=1.0, seconds=2.4):
    n = int(SR * seconds)
    x = hp(noise(n), 4000) * 0.6
    for f in rng.uniform(3200, 9500, 18):
        x += np.sign(sine(f, n)) * 0.05
    # The tail must reach silence inside the buffer, or the crash is cut off while still audible.
    t = np.arange(n) / SR
    env = perc(n, 0.002, seconds / 3.2) * np.clip((seconds - t) / (seconds * 0.45), 0, 1) ** 2
    return np.stack([bp(x, 3000, 15000) * env, bp(np.roll(x, 97), 3000, 15000) * env]) * v


def perc_hit(kind="conga", v=1.0, tune=0.0):
    k = 2 ** (tune / 12)
    n = int(SR * 0.5)
    t = np.arange(n) / SR
    if kind in ("conga", "bongo", "tom"):
        f0 = {"conga": 230, "bongo": 380, "tom": 120}[kind] * k
        x = sine(f0 * (1 + 0.15 * np.exp(-t / 0.01)), n) * perc(n, 0.001, {"conga": 0.12, "bongo": 0.07, "tom": 0.25}[kind])
        x += bp(noise(n), 1000, 4000) * perc(n, 0, 0.006) * 0.4
    elif kind == "woodblock":
        x = (sine(1100 * k, n) + 0.5 * sine(2700 * k, n)) * perc(n, 0, 0.025)
    elif kind == "cowbell":
        x = bp(square(540 * k, n) + square(800 * k, n), 500, 3000) * perc(n, 0.0005, 0.09)
    elif kind == "agogo":
        x = (sine(880 * k, n) + 0.4 * sine(2310 * k, n)) * perc(n, 0, 0.12)
    elif kind == "clave":
        x = sine(2500 * k, n) * perc(n, 0, 0.02)
    elif kind == "cabasa":
        x = hp(noise(n), 6000) * adsr(n, 0.005, 0.05, 0, 0.02)
    elif kind == "triangle":
        x = (sine(4200 * k, n) + 0.5 * sine(6100 * k, n)) * perc(n, 0, 0.35) * 0.5
    else:
        raise ValueError(kind)
    return fade(x * v)


def vinyl(seconds, v=0.05):
    """Crackle and hiss for lo fi beds."""
    n = int(SR * seconds)
    x = lp(noise(n), 5000) * 0.05
    pops = rng.random(n) < 18 / SR
    x[pops] += rng.uniform(-1, 1, pops.sum())
    return hp(x, 300) * v


# --- Basses ------------------------------------------------------------------------------------


def bass(kind="sub", m=36, dur=0.25, v=1.0, glide_from=None, cut=1.0, accent=False):
    """One bass note. dur in seconds. glide_from (a MIDI note) slides into the note (808, acid).
    cut scales brightness; accent opens the filter and adds drive (acid)."""
    tail = {"808": 0.5, "log": 0.25, "pluck": 0.3, "upright": 0.4}.get(kind, 0.06)
    n = int(SR * (dur + tail))
    t = np.arange(n) / SR
    f = np.full(n, hz(m))
    if glide_from is not None:
        g = np.exp(-t / 0.045)
        f = hz(m) * 2 ** ((glide_from - m) * g / 12)
    if kind == "sub":
        x = sine(f, n) * adsr(n, 0.004, 0.2, 0.85, 0.05, dur)
    elif kind == "808":
        x = sat(sine(f, n) * perc(n, 0.002, dur * 0.7 + 0.25), 1.6)
        x += hp(noise(n), 3000) * perc(n, 0, 0.003) * 0.3
    elif kind == "reese":
        x = sum(saw(f * 2 ** (d / 1200), n, rng.uniform()) for d in (-14, -5, 6, 15)) / 4
        x = sweep_lp(x, 420 * cut + 250 * np.sin(2 * np.pi * 0.6 * t) ** 2, 0.8) + sine(f, n) * 0.6
        x *= adsr(n, 0.01, 0.2, 0.9, 0.06, dur)
    elif kind == "acid":
        env = np.exp(-t / (0.09 if not accent else 0.16))
        x = saw(f, n)
        x = sweep_lp(x, (250 + 2400 * env * (1.6 if accent else 1.0)) * cut, 4.5 if accent else 3.0)
        x = sat(x * (1.8 if accent else 1.2), 1.5) * adsr(n, 0.002, 0.1, 0.8, 0.02, dur)
    elif kind == "pluck":
        x = sweep_lp(saw(f, n) * 0.7 + square(f, n) * 0.3, (180 + 2400 * np.exp(-t / 0.07)) * cut, 1.0)
        x = (x + sine(f, n) * 0.7) * perc(n, 0.002, max(0.12, dur * 0.8))
    elif kind == "fm":
        x = fm(f, n, ratio=1.0, index=2.5 * cut, index_decay=0.12) * adsr(n, 0.003, 0.15, 0.7, 0.04, dur)
        x += sine(f, n) * 0.5 * adsr(n, 0.003, 0.15, 0.7, 0.04, dur)
    elif kind == "octave":
        x = sweep_lp(saw(f, n), 900 * cut, 1.2) * adsr(n, 0.002, 0.08, 0.6, 0.03, dur) + sine(f, n) * 0.5 * adsr(n, 0.002, 0.1, 0.8, 0.03, dur)
    elif kind == "upright":
        x = lp(karplus(float(f[0]), n / SR, 0.993, 0.15)[:n], 1200 * cut)
        x = np.pad(x, (0, n - len(x))) + sine(f, n) * perc(n, 0.006, 0.35) * 0.5
    elif kind == "log":
        # The amapiano log drum: a pitched, gliding, slightly hollow FM thump between a kick and a bass.
        fl = f * (1 + 0.25 * np.exp(-t / 0.02))
        x = fm(fl, n, ratio=1.5, index=1.6, index_decay=0.05) * perc(n, 0.002, 0.16 + dur * 0.4)
        x = sat(x + sine(fl, n) * 0.6 * perc(n, 0.002, 0.25), 1.8)
    elif kind == "wobble":
        lfo = 0.5 + 0.5 * np.sin(2 * np.pi * (1 / max(dur, 0.1)) * 2 * t - np.pi / 2)
        x = sweep_lp(saw(f, n) + square(f * 0.5, n) * 0.6, 150 + 2200 * lfo * cut, 2.0) * adsr(n, 0.005, 0.1, 0.9, 0.04, dur)
    else:
        raise ValueError(kind)
    return fade(x * v)


KEY_KINDS = {"epiano", "piano", "organ", "mallet", "marimba", "kalimba", "vibes", "steel", "clav", "nylon", "harp", "bell", "celesta"}

# --- Keys and mallets --------------------------------------------------------------------------


def keys(kind="epiano", m=60, dur=0.5, v=1.0, cut=1.0):
    """One note. Most kinds ring past dur; organ and clav stop with it."""
    ring = {"piano": 2.2, "epiano": 1.4, "mallet": 0.5, "marimba": 0.6, "kalimba": 1.0, "vibes": 2.0, "steel": 1.0,
            "bell": 2.4, "celesta": 1.4, "nylon": 1.6, "harp": 2.4, "organ": 0.08, "clav": 0.08}[kind]
    n = int(SR * (dur + ring))
    t = np.arange(n) / SR
    f = hz(m)
    if kind == "epiano":
        idx = 0.25 + 1.5 * v * np.exp(-t / 0.35)
        x = np.sin(2 * np.pi * f * t + idx * np.sin(2 * np.pi * f * t))
        x += 0.25 * np.sin(2 * np.pi * f * 14 * t) * np.exp(-t / 0.045)
        x *= perc(n, 0.002, 0.9) * np.clip((dur + 0.25 - t) / 0.25, 0.25, 1)
    elif kind == "piano":
        x = np.zeros(n)
        for k in range(1, 9):
            fk = f * k * np.sqrt(1 + 0.0004 * k * k)  # string stiffness stretches the partials
            x += np.sin(2 * np.pi * fk * t) * np.exp(-t * (0.9 + 0.7 * k)) / k**1.1
        x += bp(noise(n), 1500, 6000) * perc(n, 0, 0.005) * 0.2
        x *= perc(n, 0.001, 1.6) * np.clip((dur + 0.4 - t) / 0.4, 0.15, 1)
    elif kind == "organ":
        x = sum(a * sine(f * h, n) for h, a in ((0.5, 0.5), (1, 1), (2, 0.6), (3, 0.35), (4, 0.25), (6, 0.12)))
        x *= adsr(n, 0.008, 0.05, 0.95, 0.06, dur) * 0.5
        x += sine(f * 3, n) * perc(n, 0.001, 0.03) * 0.3  # key click
    elif kind == "mallet":  # the soft wooden mallet: sine, two quiet harmonics, raised cosine attack
        x = sine(f, n) + 0.18 * sine(f * 2, n) + 0.06 * sine(f * 3, n)
        att = np.clip(t / 0.004, 0, 1)
        x *= (0.5 - 0.5 * np.cos(np.pi * att)) * np.exp(-t / 0.22)
    elif kind == "marimba":
        x = sine(f, n) * np.exp(-t / 0.25) + 0.35 * sine(f * 4, n) * np.exp(-t / 0.04)
        x += bp(noise(n), 1500, 4000) * perc(n, 0, 0.003) * 0.15
    elif kind == "kalimba":
        x = fm(f, n, ratio=3.0, index=1.2, index_decay=0.02) * perc(n, 0.001, 0.45) + 0.2 * sine(f * 5.4, n) * perc(n, 0, 0.05)
    elif kind == "vibes":
        trem = 1 + 0.3 * np.sin(2 * np.pi * 5.5 * t)
        x = (sine(f, n) + 0.3 * sine(f * 4, n) * np.exp(-t / 0.2)) * perc(n, 0.002, 1.4) * trem
    elif kind == "steel":
        x = fm(f, n, ratio=2.0, index=1.0, index_decay=0.25) * perc(n, 0.002, 0.5) + 0.3 * sine(f * 2.98, n) * perc(n, 0, 0.3)
    elif kind == "bell":
        x = fm(f, n, ratio=3.5, index=3.5, index_decay=0.3) * perc(n, 0.001, 1.0)
    elif kind == "celesta":
        x = (sine(f * 2, n) + 0.4 * sine(f * 4, n) * np.exp(-t / 0.3)) * perc(n, 0.001, 0.7)
    elif kind == "clav":
        x = sweep_lp(square(f, n, duty=0.18), 400 + 5000 * np.exp(-t / 0.05), 1.4) * adsr(n, 0.001, 0.08, 0.5, 0.03, dur)
    elif kind in ("nylon", "harp"):
        x = karplus(f, (dur + ring), 0.997 if kind == "harp" else 0.995, 0.2 if kind == "nylon" else 0.45)[:n]
        x = lp(x, 3500 if kind == "nylon" else 7000)
    else:
        raise ValueError(kind)
    x = lp(x, 400 + 9000 * cut) if cut < 1 else x
    return fade(x * v)


def strum(kind, notes, dur, v=1.0, spread=0.012, cut=1.0, width=0.5):
    """A chord, its notes spread over a few milliseconds and across the stereo field."""
    parts = [keys(kind, m, dur, v * (0.9 + 0.2 * rng.random()), cut) for m in notes]
    n = max(len(p) for p in parts) + int(SR * spread * len(notes))
    out = np.zeros((2, n))
    for i, p in enumerate(parts):
        k = int(SR * spread * i)
        pos = (i / max(1, len(notes) - 1) - 0.5) * 2 * width
        out[:, k : k + len(p)] += pan2(p, pos)
    return out / np.sqrt(len(notes))


# --- Pads --------------------------------------------------------------------------------------


def pad(kind="saw", notes=(57, 60, 64), seconds=2.0, cut=2400, attack=0.4, v=1.0):
    n = int(SR * (seconds + 0.6))
    out = np.zeros((2, n))
    for i, m in enumerate(notes):
        f = hz(m)
        pos = (i / max(1, len(notes) - 1) - 0.5) * 1.4
        if kind in ("saw", "strings"):
            det = (-9, 0, 8) if kind == "saw" else (-12, -4, 5, 13)
            x = sum(saw(f * 2 ** (d / 1200), n, rng.uniform()) for d in det) / len(det)
            if kind == "strings":
                vib = 1 + 0.004 * np.sin(2 * np.pi * 5.2 * np.arange(n) / SR + rng.uniform(0, 6))
                x = sum(saw(f * vib * 2 ** (d / 1200), n, rng.uniform()) for d in det) / len(det)
                x = peak(x, 900, 2, 4)
            x = lp(x, cut, 2)
        elif kind == "choir":
            src = saw(f, n) * 0.6 + saw(f * 1.004, n) * 0.4
            vowel = VOWELS["a" if i % 2 == 0 else "o"]
            x = sum(bp(src, c - w, c + w) * (1 / (j + 1)) for j, (c, w) in enumerate(vowel)) * 3
        elif kind == "glass":
            x = fm(f, n, ratio=2.0, index=0.8, index_decay=10.0) * 0.6 + sine(f * 2, n) * 0.2
        elif kind == "warm":
            x = sum(tri(f * 2 ** (d / 1200), n, rng.uniform()) for d in (-7, 0, 7)) / 3
        elif kind == "air":
            x = bp(noise(n), f * 4, f * 4.6) * 6 + sine(f, n) * 0.15
        else:
            raise ValueError(kind)
        x *= adsr(n, attack, 0.5, 0.85, 0.6, seconds)
        out += pan2(x, pos)
    return widen(out * v / np.sqrt(len(notes)), 9)


# --- Leads -------------------------------------------------------------------------------------


def lead(kind="pluck", m=72, dur=0.25, v=1.0, cut=1.0, glide_from=None, vowel="a"):
    tail = {"pluck": 0.25, "sine": 0.15, "whistle": 0.1, "vowel": 0.1, "flute": 0.12}.get(kind, 0.08)
    n = int(SR * (dur + tail))
    t = np.arange(n) / SR
    f = np.full(n, hz(m))
    if glide_from is not None:
        f = hz(m) * 2 ** ((glide_from - m) * np.exp(-t / 0.05) / 12)
    vib = 1 + 0.006 * np.sin(2 * np.pi * 5.5 * t) * np.clip((t - 0.15) / 0.2, 0, 1)
    if kind == "supersaw":
        x = supersaw(f, n) * adsr(n, 0.004, 0.15, 0.7, 0.08, dur)
        return fade(np.stack([lp(c, 7000 * cut) for c in x]) * v)
    if kind == "square":
        x = square(f * vib, n, duty=0.5) * 0.6 + square(f * vib * 1.003, n, duty=0.3) * 0.4
        x = lp(x, 3500 * cut) * adsr(n, 0.004, 0.1, 0.75, 0.05, dur)
    elif kind == "sine":
        x = (sine(f * vib, n) + 0.12 * sine(f * vib * 2, n)) * adsr(n, 0.01, 0.2, 0.8, 0.1, dur)
    elif kind == "whistle":
        x = sine(f * vib, n) + bp(noise(n), hz(m) * 0.9, hz(m) * 1.15) * 0.25
        x *= adsr(n, 0.03, 0.1, 0.85, 0.08, dur)
    elif kind == "vowel":  # a sung, formant shaped note: vocal chop territory without a voice sample
        src = saw(f * vib, n)
        x = sum(bp(src, c - w, c + w) / (j + 1) for j, (c, w) in enumerate(VOWELS[vowel])) * 4
        x *= adsr(n, 0.01, 0.1, 0.8, 0.06, dur)
    elif kind == "pluck":
        x = sweep_lp(saw(f, n) + saw(f * 1.006, n), (900 + 7000 * np.exp(-t / 0.05)) * cut, 1.0) * 0.5
        x += sine(f * 2, n) * perc(n, 0.001, 0.08) * 0.2
        x *= perc(n, 0.001, max(0.15, dur))
    elif kind == "brass":
        env = adsr(n, 0.03, 0.2, 0.8, 0.08, dur)
        x = sweep_lp(saw(f * vib, n), (600 + 3000 * env) * cut, 1.1) * env
    elif kind == "flute":
        x = (sine(f * vib, n) + 0.1 * sine(f * vib * 2, n) + bp(noise(n), hz(m), hz(m) * 3) * 0.08)
        x *= adsr(n, 0.05, 0.1, 0.9, 0.1, dur)
    elif kind == "sync":  # hard sync: a slave saw restarted by the master, swept down for an aggressive edge
        ratio = 1.5 + 1.5 * np.exp(-t / 0.15)
        master_phase = np.cumsum(f) / SR
        x = 2 * ((master_phase % 1) * ratio % 1) - 1
        x = lp(x, 6000 * cut) * adsr(n, 0.003, 0.1, 0.7, 0.05, dur)
    else:
        raise ValueError(kind)
    return fade(x * v)


def fold_lead(m, dur, v=1.0, amount=2.2):
    """A wave folded sine: glassy and buzzy at once (hyperpop, phonk melodies)."""
    n = int(SR * (dur + 0.08))
    x = fold(sine(hz(m), n), amount) * adsr(n, 0.003, 0.12, 0.7, 0.05, dur)
    return fade(x * v)
