"""
Sound effects for picture events, tuned to the film. Every tonal effect takes notes from the
film's own scale (pass the Key), and a CHARACTER says what the interface is made of:

    glass    bright inharmonic partials that ring 30 to 70 ms, airy tops    (precise, premium)
    wood     knocks: low partials damped in 10 to 20 ms, falling clicks     (calm, crafted)
    metal    many inharmonic partials with beating, rings 60 to 150 ms     (hard, physical)
    plastic  short mid knocks with a click on top                           (consumer, toys)
    paper    noise, crackle and flutter, almost no pitch                    (editorial, notes)
    digital  square pings, bit crushed, zappy pitch drops                   (games, dev tools)
    soft     felt: slower attacks, low passed, sine tones                   (wellbeing, kids)

The characters differ in envelope, noise share, pitch movement and width, not only in frequency
(sfx/ANALYSIS.md section 5, point 8). Every effect was tuned against the CC0 library's measured
ranges (sfx/ANALYSIS.md section 4); `sfx_catalog.py --synth-only --check` prints them side by side.

One effect per job, so a card landing never sounds like a tap:

    tap, click, tick, blip (select), pop, text, toggle      small interface events
    card, chip, land(size), impact, boom                    things landing, light to heavy
    swish, whoosh(seconds, air), transition, panel          movement and transitions
    success (chime), error, tier, logo                      meaning
    riser, reverse_swell, sub_drop, stutter, tape_stop, texture

Every function takes seed: the same seed gives the same sound, so vary.py can keep a pool of
variants per effect. Most take size (0 light to 1 heavy): bigger is lower, longer and wider.
Risers, reverse swells and panel(open=True) END on their frame; whooshes, swishes and transitions
PEAK on their frame (score.py aligns peak_index); everything else starts on it.
"""

from __future__ import annotations

import numpy as np

from dsp import (
    SR,
    bp,
    crush,
    dec,
    fade,
    fm,
    glide,
    hp,
    hz,
    lp,
    modal,
    pan2,
    pink,
    rng,
    sat,
    sine,
    spread,
    square,
    stereo,
    sweep_lp,
)

CHARACTERS = ("glass", "wood", "metal", "plastic", "paper", "digital", "soft")

# What each material does. band: the click noise; d20: how fast a click dies (ms); ping: the
# tonal top of a tap (Hz) and how far it falls (semitones); partials: ratio, d20 scale, level of a
# struck tone; ring: the d20 of a tonal blip (ms); noise: the transient on tonal sounds; fall: a
# blip's pitch drop (st); width: stereo spread of noisy layers; attack in ms. decay scales how long
# hits and swishes ring (wood and plastic are damped, metal and glass ring), drop is how far a hit
# falls in pitch (digital zaps, wood knocks, metal barely moves), hw is the width of hits.
MAT = {
    "glass": dict(decay=1.25, drop=5, hw=0.3, band=(2600, 7500), d20=5, ping=(4200, 6), partials=((1, 1.0, 1.0), (2.32, 0.6, 0.45), (4.25, 0.4, 0.25), (6.63, 0.3, 0.12)),
                  ring=28, noise=0.22, fall=1.5, width=0.25, attack=0.3, tick=(5000, 11000), whistle=True, air=0.95),
    "wood": dict(decay=0.7, drop=12, hw=0.08, band=(1500, 4500), d20=6, ping=(2100, 10), partials=((1, 1.0, 1.0), (2.76, 0.45, 0.4), (5.4, 0.25, 0.15)),
                 ring=20, noise=0.35, fall=2.0, width=0.1, attack=0.5, tick=(2600, 7000), whistle=False, air=0.6),
    "metal": dict(decay=1.55, drop=3, hw=0.4, band=(2000, 7000), d20=7, ping=(3300, 2), partials=((1, 1.0, 1.0), (2.76, 0.8, 0.6), (5.4, 0.6, 0.4), (8.93, 0.45, 0.25)),
                  ring=34, noise=0.18, fall=0.6, width=0.3, attack=0.2, tick=(4200, 11000), whistle=True, air=0.85, detune=7),
    "plastic": dict(decay=0.6, drop=14, hw=0.04, band=(1800, 5500), d20=4, ping=(2600, 12), partials=((1, 1.0, 1.0), (1.59, 0.5, 0.35), (2.92, 0.3, 0.2)),
                    ring=18, noise=0.4, fall=3.0, width=0.05, attack=0.3, tick=(3400, 9000), whistle=False, air=0.7),
    "paper": dict(decay=1.0, drop=7, hw=0.35, band=(1700, 6000), d20=10, ping=None, partials=((1, 1.0, 0.7), (2.1, 0.5, 0.3)),
                  ring=20, noise=0.55, fall=4.0, width=0.25, attack=1.0, tick=(4000, 12000), whistle=False, air=0.9, crackle=True),
    "digital": dict(decay=0.8, drop=24, hw=0.0, band=(2000, 6500), d20=3, ping=(2000, 14), partials=((1, 1.0, 1.0),),
                    ring=20, noise=0.15, fall=0.0, width=0.0, attack=0.1, tick=(3000, 8000), whistle=False, air=0.72, square=True, crush=True),
    "soft": dict(decay=1.3, drop=2, hw=0.25, band=(1000, 3200), d20=8, ping=None, partials=((1, 1.0, 1.0), (2.0, 0.5, 0.18)),
                 ring=26, noise=0.3, fall=1.5, width=0.2, attack=2.5, tick=(3200, 7000), whistle=False, air=0.62, low=3200),
}


def note(key, i: int, octave: int = 5) -> int:
    """The i-th note of the film's scale, counted up from the tonic in the given octave."""
    return key.degree(i, octave - 3)


def near(key, i: int, lo: float, hi: float) -> float:
    """The scale note of degree i moved by octaves into lo to hi Hz (or as close as it gets)."""
    m = note(key, i, 5)
    while hz(m) < lo:
        m += 12
    while hz(m) > hi and hz(m - 12) >= lo * 0.94:
        m -= 12
    return hz(m)


def _r(seed):
    return np.random.default_rng(seed) if seed is not None else rng


def _mat(character):
    return MAT.get(character, MAT["glass"])


def _done(x, v, ms=0.5):
    """Peak normalise to v and fade both ends (a waveform that starts off zero is a click)."""
    x = np.asarray(x, float)
    x = x / (np.abs(x).max() + 1e-12) * v
    return fade(x, ms)


def _soft(x, m, cap=None):
    """Soft low passes everything; cap lifts the cut for sounds that must stay bright to work."""
    return lp(x, max(m["low"], cap or 0)) if "low" in m else x


def _crush(x, m, bits=7, keep=2):
    if not m.get("crush"):
        return x
    return np.stack([crush(c, bits, keep) for c in x]) if x.ndim == 2 else crush(x, bits, keep)


def _tone(ftrack, n, m, ring, r):
    """A struck tone in the material: partials on a frequency track, each with its own decay."""
    if m.get("square"):
        return lp(square(ftrack, n, duty=0.25), 7000) * dec(n, ring, 0.1)
    out = np.zeros(n)
    for ratio, dscale, amp in m["partials"]:
        ph = r.uniform(0, 1)
        out += amp * sine(ftrack * ratio, n, ph) * dec(n, ring * dscale, m["attack"] * 0.4)
        if m.get("detune"):
            out += 0.45 * amp * sine(ftrack * ratio * 2 ** (m["detune"] / 1200), n, ph + 0.3) * dec(n, ring * dscale, 0.2)
    return out


def _noise2(r, n, fn, width):
    """The same noisy layer twice, decorrelated, for width."""
    return spread(fn(r.standard_normal(n)), fn(r.standard_normal(n)), width)


def peak_index(x) -> int:
    """Where a sound is loudest (5 ms smoothed), so a whoosh's peak can sit on its frame."""
    e = np.abs(x if x.ndim == 1 else x.mean(0))
    k = int(SR * 0.005)
    return int(np.argmax(np.convolve(e, np.ones(k) / k, mode="same")))


# --- Small interface events --------------------------------------------------------------------


def tap(character: str = "glass", v: float = 0.7, size: float = 0.3, seed=None):
    """A press: a 4 to 15 ms noise burst, mostly 2 to 6 kHz, often with a ping falling 5 to 15 st."""
    m, r = _mat(character), _r(seed)
    n = int(SR * 0.08)
    s = 2 ** (-0.8 * size)
    lo, hi = m["band"]
    d = m["d20"] * (0.8 + 0.8 * size) * r.uniform(0.85, 1.15)
    fall = glide(1.0, 2 ** (-m["drop"] * 0.5 / 12), n, 30)  # the press falls like the material does
    out = _noise2(r, n, lambda w: sweep_lp(bp(w, lo * s, hi * s), hi * s * 1.3 * fall, 0.8) * dec(n, d, m["attack"]), m["width"])
    if m["ping"] and r.random() < 0.8:  # layer swap: one variant in five has no ping
        f0 = m["ping"][0] * s * r.uniform(0.92, 1.08)
        f = glide(f0, f0 * 2 ** (-m["ping"][1] * r.uniform(0.8, 1.2) / 12), n, 35)
        p = (lp(square(f, n), 7000) if m.get("square") else sine(f, n)) * dec(n, d * 1.2 + 3, 0.2)
        out = out + 0.22 * p
    if size > 0.5:  # a bigger button has a little body, kept under 15 percent below 500 Hz
        out = out + 0.12 * bp(r.standard_normal(n), 350, 900) * dec(n, 6, 0.3)
    if m.get("crackle"):
        out = out * (1 + 0.6 * np.sign(r.standard_normal(n)) * (r.random(n) < 0.08))
    return _done(hp(_crush(_soft(out, m), m), 400), v)


def click(character: str = "glass", v: float = 0.7, seed=None):
    """A press and a quieter, higher release 45 to 80 ms later."""
    r = _r(seed)
    press = tap(character, 1.0, 0.25, int(r.integers(1 << 30)))
    rel = tap(character, 0.32, 0.0, int(r.integers(1 << 30)))
    k = int(SR * r.uniform(0.045, 0.08))
    out = np.zeros((2, k + rel.shape[1]))
    out[:, : press.shape[1]] += press
    out[:, k:] += rel
    return _done(out, v)


def tick(character: str = "glass", pitch: float = 1.0, v: float = 0.5, seed=None):
    """A data tick: under 1 ms on, 4 to 9 ms to -20 dB, centred 3 to 10 kHz. pitch rises a run."""
    m, r = _mat(character), _r(seed)
    n = int(SR * 0.03)
    lo, hi = m["tick"]
    x = bp(r.standard_normal(n), lo * pitch, min(hi * pitch, 20000)) * dec(n, r.uniform(4, 6), 0.15)
    f = (lo + hi) / 2 * pitch * r.uniform(0.95, 1.05)
    ping = (lp(square(f / 2, n, duty=0.5), 9000) if m.get("square") else sine(f * 0.7, n)) * dec(n, 6, 0.1)
    x = x + (0.15 if character in ("paper", "wood") else 0.45) * ping
    x = x + 0.9 * bp(r.standard_normal(n), 700, 1900) * dec(n, 4, 0.15)  # a little body under the top
    return _done(_crush(_soft(x, m) if character == "soft" else x, m), v)


def blip(key, i: int, character: str = "glass", v: float = 0.6, seed=None, octave: int = 5, ring=None):
    """A select: a tone on the i-th scale note with a noise transient, falling 1 to 2 st, 13 to 35 ms
    to -20 dB. Runs up the scale become phrases."""
    m, r = _mat(character), _r(seed)
    ring = ring or m["ring"] * r.uniform(0.85, 1.2)
    f = hz(note(key, i, octave))
    n = int(SR * (ring * 2.4 / 1000 + 0.03))
    ftrack = glide(f * 2 ** (m["fall"] / 12), f, n, 40)
    x = _tone(ftrack, n, m, ring, r)
    x = x + m["noise"] * bp(r.standard_normal(n), 2000, 7000) * dec(n, 2.5, 0.1) * 3
    if character == "digital":  # a two step arcade drop instead of a glide
        half = n // 3
        x[half:] = lp(square(np.full(n - half, f * 2 ** (-5 / 12)), n - half, duty=0.25), 7000) * dec(n - half, ring * 0.8, 0.1) * 0.7
    return _done(_crush(_soft(x, m), m), v)


def pop(key, i: int = 0, character: str = "glass", v: float = 0.6, seed=None):
    """A soft pop: a tone at 740 to 990 Hz rising 3 to 7 st in 25 ms, nothing in 2 to 6 kHz."""
    r = _r(seed)
    f = near(key, i, 740, 990)
    d = {"wood": 35, "plastic": 34, "metal": 38, "glass": 37}.get(character, 36) * r.uniform(0.95, 1.05)
    n = int(SR * 0.12)
    up = r.uniform(3, 7)
    ftrack = glide(f * 2 ** (-up / 12), f, n, 25)
    x = sine(ftrack, n) * dec(n, d, 2.0)
    if character in ("glass", "metal"):
        x = x + 0.12 * sine(ftrack * 2, n) * dec(n, d * 0.5, 1.0)
    x = lp(x, 1800, 4)
    if character == "digital":
        x = crush(x, 8, 2)
    return _done(x, v)


def text(key, i: int = 0, character: str = "glass", v: float = 0.5, seed=None):
    """Text appearing, per word or line: soft and short, a tone falling about an octave plus a
    little breath, centred 0.9 to 2 kHz."""
    m, r = _mat(character), _r(seed)
    f = hz(note(key, i, 4))
    n = int(SR * 0.1)
    fall = r.uniform(14, 22)
    ftrack = glide(f * 2 ** (fall / 12), f, n, 100)
    env = dec(n, r.uniform(12, 15), 1.0) + 0.1 * dec(n, 70, 1.0)  # a quick drop, then a short tail
    x = (lp(square(ftrack, n), 4000) if m.get("square") else sine(ftrack, n) + 0.2 * sine(2 * ftrack, n)) * env
    br = sweep_lp(hp(r.standard_normal(n), 700), glide(3800, 1400, n, 50), 0.9) * dec(n, 10, 1.0)
    x = x + (0.9 if m.get("crackle") else 0.35) * br / (np.abs(br).max() + 1e-9)
    return _done(lp(x, 4500), v)


def toggle(key, on: bool = True, character: str = "glass", v: float = 0.6, seed=None):
    """A switch: a click, then two tones a fourth apart, rising for on and falling for off."""
    m, r = _mat(character), _r(seed)
    a, b = hz(note(key, 0, 6)), hz(note(key, 3, 6))
    if not on:
        a, b = b, a
    gap = int(SR * r.uniform(0.03, 0.04))
    n = int(SR * 0.16)
    out = np.zeros(n)
    for k, f in ((0, a), (gap, b)):
        tn = _tone(np.full(n - k, f), n - k, m, 34 * (1.35 if character == "metal" else 1) * r.uniform(0.9, 1.1), r)
        out[k:] += tn * (0.62 if k else 0.8)
    out = out + 0.35 * bp(r.standard_normal(n), *m["band"]) * dec(n, 3, 0.1)
    return _done(_crush(_soft(out, m), m), v)


# --- Things landing ----------------------------------------------------------------------------


def card(character: str = "glass", v: float = 0.8, size: float = 0.5, seed=None):
    """A card lands: an 80 to 180 ms thud, nearly all of it under 500 Hz and most of that in 120 to
    500 Hz (so it survives a phone speaker), a short pitch drop, the material on top, quietly."""
    m, r = _mat(character), _r(seed)
    n = int(SR * 0.2)
    f = r.uniform(150, 200) * 2 ** (-0.7 * size)
    k = m["decay"]
    body = sine(glide(f * 2 ** (min(m["drop"], 8) / 12), f, n, 22), n) * dec(n, r.uniform(17, 21) * k**0.6 * (1 + 0.3 * size), 0.6)
    thump = bp(r.standard_normal(n), 120, 480, 4) * dec(n, (14 + 8 * size) * k, 0.3) * 1.3
    x = body + 0.7 * thump / (np.abs(thump).max() + 1e-9)
    x = x + 0.2 * bp(r.standard_normal(n), 120, 450, 4) * dec(n, 120, 2)  # the floor answering, 20 dB down
    if character in ("wood", "plastic"):
        x = x + (0.22 if character == "wood" else 0.15) * modal(n, [f * 2.3, f * 3.9], [10, 6], [1.0, 0.5], r)
    elif character in ("glass", "metal"):
        x = x + 0.035 * modal(n, [f * 9.1, f * 14.3], [40, 25], [1.0, 0.6], r, detune=m.get("detune", 0))
    elif character == "paper":
        x = x + 0.08 * bp(r.standard_normal(n), 1500, 6000) * dec(n, 15, 2)
    elif character == "digital":
        x = crush(x, 8, 3)
    if character == "soft":
        x = lp(x, 450) * np.clip(np.arange(n) / (SR * 0.0015), 0, 1)
    return _done(x, v)


def chip(key, i: int = 0, character: str = "glass", v: float = 0.7, seed=None):
    """A light object lands (a glass card, a chip, a token): a struck tone near C6 ringing 45 to 90
    ms to -20 dB, with a click and a small low knock under it."""
    m, r = _mat(character), _r(seed)
    if character == "paper":
        return card("paper", v, 0.1, seed)
    f = near(key, i, 950, 1250)
    ring = {"glass": 66, "metal": 74, "wood": 56, "plastic": 58, "digital": 58, "soft": 60}.get(character, 60) * r.uniform(0.92, 1.08)
    n = int(SR * (ring * 2.3 / 1000 + 0.04))
    x = _tone(np.full(n, f), n, m, ring, r)
    x = x + 0.5 * bp(r.standard_normal(n), 2000, 7500) * dec(n, 2.5, 0.1)
    x = x + 0.3 * sine(glide(330, 210, n, 15), n) * dec(n, 8, 0.3)
    return _done(_crush(_soft(x, m), m), v)


def impact(character: str = "glass", v: float = 1.0, size: float = 1.0, seed=None, tail: float = 0.0):
    """A hit for a reveal or a drop: a sub body that drops in pitch and dies in 50 to 70 ms, a 120 to
    500 Hz knock carrying 20 to 35 percent of the energy (a phone hears this part), a crack, the
    material, and a low tail. tail above 0 keeps a longer cinematic sub (a boom under a drop)."""
    m, r = _mat(character), _r(seed)
    n = int(SR * (0.75 + 0.5 * tail))
    s = 2 ** (-0.5 * size)
    fs = r.uniform(48, 56) * (0.9 + 0.2 * s)
    k = m["decay"]
    sub = sine(glide(fs * 2 ** ((10 + 0.25 * m["drop"]) / 12), fs, n, 38), n) * dec(n, (40 + 22 * size) * k**0.4 * (1 + 3 * tail), 0.8)
    sub = sat(sub + 0.07 * sine(fs, n) * dec(n, 520 + 400 * tail, 20, 30), 1.8)
    kf = r.uniform(165, 205) * (1.3 - 0.3 * size)
    kk = k**0.5
    knock = modal(n, [kf, kf * 1.52, kf * 2.31], [36 * kk, 26 * kk, 17 * kk], [0.6, 0.35, 0.2], r)
    knock = knock + (0.7 if character == "paper" else 0.5) * bp(r.standard_normal(n), 120, 520) * dec(n, 30 * kk, 0.5)
    crack = hp(r.standard_normal(n), 2500) * dec(n, 3, 0.1)
    room = bp(r.standard_normal(n), 150, 600, 4) * dec(n, 260, 5, 20)
    x = sub + 1.15 * (0.6 + 0.5 * size) * knock + 0.08 * crack + 0.035 * room
    if character == "metal":
        x = x + 0.22 * modal(n, [310 * s, 547 * s, 893 * s, 1420 * s, 2210 * s], [160, 130, 100, 80, 60], [1, 0.8, 0.6, 0.45, 0.3], r, detune=7)
    elif character == "glass":
        x = x + 0.08 * modal(n, [2350, 3900, 6100], [140, 100, 70], [1, 0.7, 0.4], r) + 0.06 * hp(r.standard_normal(n), 5000) * dec(n, 60, 1)
    elif character in ("wood", "plastic"):
        x = x + 0.35 * modal(n, [kf * 2.2, kf * 3.6], [16, 9], [1, 0.5], r)
    elif character == "paper":
        x = x + 0.08 * bp(r.standard_normal(n), 1200, 6000) * dec(n, 40, 2) * (1 + (r.random(n) < 0.05))
    elif character == "digital":
        x = crush(x, 7, 2)
    if character == "soft":
        x = lp(x, 1600)
    side = bp(r.standard_normal(n), 200, 2000) * dec(n, 40 * k, 1) + 0.3 * modal(n, [kf * 1.1, kf * 1.9], [30 * k, 20 * k], [1, 0.6], r)
    x = x if size < 0.6 or not m["hw"] else spread(x, side * np.abs(x).max() * 0.4, m["hw"] * size)
    return _done(x, v, 0.3)


def boom(character: str = "glass", v: float = 1.0, seed=None):
    """The cinematic version: the same hit with a longer sub tail, for the one drop or reveal."""
    return impact(character, v, 1.0, seed, tail=1.0)


def land(character: str = "glass", size: float = 0.5, key=None, i: int = 0, v: float = 0.8, seed=None):
    """Something lands; the sound follows its size: a chip, a card, or a hit."""
    if size < 0.3 and key is not None:
        return chip(key, i, character, v, seed)
    if size < 0.75:
        return card(character, v, size, seed)
    return impact(character, v, size, seed)


# --- Movement ----------------------------------------------------------------------------------


def swish(seconds: float = 0.12, character: str = "glass", v: float = 0.6, seed=None, direction: int = 1, whistle=None):
    """A fast swish: 60 to 160 ms, peak in the first third, a low 200 to 700 Hz band of air with an
    optional whistle bending through a doppler. Place its peak (peak_index) on the frame."""
    m, r = _mat(character), _r(seed)
    n = int(SR * seconds)
    t = np.linspace(0, 1, n)
    p = r.uniform(0.25, 0.38)
    d20 = min(0.18 * seconds * 1000 * m["decay"] ** 0.7, 0.6 * seconds * 1000)
    env = np.where(t < p, (t / p) ** 2, np.exp(-(t - p) * seconds * 1000 * np.log(10) / d20))
    centre = 200 + 330 * np.exp(-((t - p) / 0.25) ** 2) * (0.75 if character in ("wood", "soft") else 1.0)
    centre = centre * glide(2 ** (m["drop"] * 0.15 / 12), 2 ** (-m["drop"] * 0.15 / 12), n, seconds * 1000)  # doppler, deeper for hard materials

    def air(w):
        return sweep_lp(hp(w, 130, 4), centre * 1.2, 1.1)

    out = spread(air(pink(n, r)), air(pink(n, r)), 0.45 * m["hw"]) * env
    if whistle if whistle is not None else (m["whistle"] and r.random() < 0.7):
        f = r.uniform(620, 1050)
        bend = glide(f * 2 ** (1.5 / 12), f * 2 ** (-1.5 / 12), n, seconds * 1000, "lin")
        out = out + 0.22 * np.abs(out).max() * sine(bend, n) * env
    out = out * np.array([[1 - 0.25 * direction], [1 + 0.25 * direction]])
    return _done(_crush(out, m), v, 1)


def whoosh(seconds: float = 0.4, character: str = "glass", v: float = 0.6, seed=None, weight: float = 0.6,
           air: bool = False, whistle=None, direction: int = 1, rise: bool = False):
    """Movement whose length follows the motion. Up to 0.18 s it is a swish. Otherwise a swing: a
    low "whum" (most energy in 120 to 500 Hz, centroid near 400 Hz) falling about 2 st, wide, peak
    35 to 45 percent in, with an optional whistle; heavier weight is lower and slower. air=True is
    the designed airy sweep instead: bright noise (5 to 8 kHz), slow attack, long and wide, for light
    sweeps and reveals. Place the peak (peak_index) on the frame."""
    if seconds <= 0.18 and not air:
        return swish(seconds, character, v, seed, direction, whistle)
    m, r = _mat(character), _r(seed)
    n = int(SR * seconds)
    t = np.linspace(0, 1, n)
    if air:
        p = r.uniform(0.18, 0.3) if not rise else 0.92
        env = np.where(t < p, np.sin(np.pi / 2 * t / p) ** 2, np.exp(-(t - p) * seconds * np.log(10) / (0.5 * seconds)))
        c = 3800 + 5200 * m["air"] * np.exp(-((t - p) / 0.4) ** 2) + (2500 * t if rise else 0)

        def layer(w):
            return sweep_lp(hp(w, 2500), np.minimum(c * 1.4, 19000), 0.8)

        out = spread(layer(r.standard_normal(n)), layer(r.standard_normal(n)), 0.55 + 0.3 * m["width"]) * env
        shine = sine(np.minimum(c * 0.9, 16000), n) * env * 0.12 * np.abs(out).max()  # a faint designed tone in the air
        out = out + np.stack([shine, shine])
        pan = np.linspace(-0.6, 0.6, n) * direction
        out = out * np.stack([1 - 0.4 * pan, 1 + 0.4 * pan])
        return _done(_crush(_soft(out, m, 9000), m), v, 3)
    p = r.uniform(0.26, 0.34)
    w = np.clip(weight, 0, 1)
    d20 = (0.12 + 0.08 * w) * seconds * 1000 * m["decay"] ** 0.5
    env = np.where(t < p, np.sin(np.pi / 2 * t / p) ** 2, np.exp(-(t - p) * seconds * 1000 * np.log(10) / d20))
    env = env + np.where(t < p, 0, 0.09 * np.exp(-(t - p) * seconds * 1000 * np.log(10) / (4 * d20)))  # the air settling
    centre = (220 - 60 * w) + (360 - 110 * w) * np.exp(-((t - p) / 0.3) ** 2)
    centre = centre * glide(1.0, 2 ** (-2 / 12), n, seconds * 1000)

    def whum(x):
        return sweep_lp(hp(x, 135, 4), centre * 1.25, 1.3)

    out = spread(whum(pink(n, r)), whum(pink(n, r)), 0.55 + 1.2 * m["hw"])
    body = sine(glide(215 - 40 * w, (215 - 40 * w) * 2 ** (-2 / 12), n, seconds * 1000), n)
    out = (out + 0.25 * body * np.abs(out).max()) * env
    if whistle if whistle is not None else (m["whistle"] and r.random() < 0.5):
        f = r.uniform(520, 900)
        out = out + 0.07 * np.abs(out).max() * sine(glide(f * 2 ** (2 / 12), f * 2 ** (-2 / 12), n, seconds * 1000, "lin"), n) * env
    pan = np.linspace(-0.5, 0.5, n) * direction
    out = out * np.stack([1 - 0.35 * pan, 1 + 0.35 * pan])
    if character == "paper":  # paper moving is flutter, not wind
        out = out * (1 + 0.5 * np.sin(2 * np.pi * 38 * t * seconds))
    return _done(_crush(out, m), v, 2)


def transition(seconds: float = 0.35, character: str = "glass", v: float = 0.8, seed=None, weight: float = 0.5):
    """A whoosh into a small landing: the whoosh peaks on the frame, a light knock lands right after
    it. For a structural cut; ordinary cuts should get the music, or a swish at most."""
    r = _r(seed)
    w = whoosh(seconds, character, 1.0, int(r.integers(1 << 30)), weight)
    k = peak_index(w)
    hit = stereo(impact(character, 0.55, 0.35, int(r.integers(1 << 30))))
    out = np.zeros((2, max(w.shape[1], k + hit.shape[1])))
    out[:, : w.shape[1]] += w
    out[:, k : k + hit.shape[1]] += hit
    return _done(out, v)


def panel(opening: bool = True, character: str = "glass", v: float = 0.6, seconds: float = 0.3, seed=None):
    """A panel or sheet opening or closing: a noise sweep rising 6 to 17 st that ENDS on its frame
    with a hard stop (opening), or falling from its frame (closing)."""
    m, r = _mat(character), _r(seed)
    n = int(SR * seconds)
    t = np.linspace(0, 1, n)
    st = r.uniform(16, 22)
    base = 1600 + 1900 * m["air"]
    track = base * 2 ** ((t if opening else 1 - t) ** 1.8 * st / 12)  # the climb speeds up, like a swipe

    def layer(w):  # a band whose both edges move, so the centre really climbs
        y = sweep_lp(w, np.minimum(track * 1.25, 20000), 1.4)
        return y - sweep_lp(y, track * 0.6, 0.7)

    out = spread(layer(r.standard_normal(n)), layer(r.standard_normal(n)), m["width"])
    env = t**2.2 if opening else np.exp(-t * seconds * 1000 * np.log(10) / (0.8 * seconds * 1000))
    out = out * env
    if opening:
        out[:, -int(SR * 0.0015) :] *= np.linspace(1, 0, int(SR * 0.0015))
    return _done(_crush(_soft(out, m, 9000), m), v, 0.5)


# --- Meaning -----------------------------------------------------------------------------------


def success(key, character: str = "glass", v: float = 0.5, seed=None, degrees=(0, 2, 4, 7)):
    """A success: 4 to 6 notes 60 to 80 ms apart, rising, the last one ringing (190 to 290 ms to
    -20 dB over the whole), notes alternating a little left and right."""
    m, r = _mat(character), _r(seed)
    gap = r.uniform(0.062, 0.078)
    n = int(SR * (gap * len(degrees) + 0.5))
    out = np.zeros((2, n))
    for j, d in enumerate(degrees):
        last = j == len(degrees) - 1
        f = hz(note(key, d, 5 if character != "digital" else 6))
        ring = (70 if last else 90) * (1.15 if character in ("metal", "glass") else 0.9 if character == "wood" else 1.0)
        k = int(SR * gap * j)
        nn = n - k
        x = _tone(np.full(nn, f), nn, m, ring, r) * (1.0 - 0.06 * j)
        x = x + 0.25 * m["noise"] * bp(r.standard_normal(nn), 2500, 7000) * dec(nn, 2, 0.1)
        out[:, k:] += pan2(_soft(x, m), (0.25 if j % 2 else -0.25) * (1 if m["width"] else 0))
    return _done(_crush(out, m), v)


def chime(key, character: str = "glass", v: float = 0.5, degrees=(0, 2, 4), seed=None):
    """A short success on chosen degrees (kept for older cue maps)."""
    return success(key, character, v, seed, degrees)


def error(key, character: str = "glass", v: float = 0.5, seed=None, hits: int = 2):
    """An error: low (180 to 1000 Hz centroid), a little buzz, each hit with its semitone neighbour
    (the clash is the message) and falling, 40 to 75 ms to -20 dB."""
    m, r = _mat(character), _r(seed)
    f = hz(note(key, 0, 4))
    gap = r.uniform(0.07, 0.09)
    n = int(SR * (gap * hits + 0.12))
    out = np.zeros(n)
    for j in range(hits):
        k = int(SR * gap * j)
        nn = n - k
        tr = glide(f, f * 2 ** (-1 / 12), nn, 60) * (2 ** (-2 / 12) if j else 1)
        wav = square(tr, nn, duty=0.4) if m.get("square") else sine(tr, nn) + 0.5 * sine(2 * tr, nn) + 0.3 * sine(3 * tr, nn)
        wav = wav + 0.4 * (sine(tr * 2 ** (1 / 12), nn) if not m.get("square") else square(tr * 2 ** (1 / 12), nn, duty=0.4))
        buzz = bp(r.standard_normal(nn), 150, 1300) * 1.2
        out[k:] += lp(wav + buzz, 1600) * dec(nn, r.uniform(44, 56), 1.0) * (0.8 if j else 1.0)
    return _done(_crush(_soft(out, m), m), v)


def tier(key, i: int = 0, character: str = "metal", v: float = 0.7, seed=None):
    """A tier or level change: a struck hit plus a bell a scale step higher per tier, brighter as it
    climbs (a material being upgraded)."""
    m, r = _mat(character), _r(seed)
    f = hz(note(key, 7 + 2 * i, 4))
    n = int(SR * 0.7)
    bell = fm(f, n, ratio=3.5, index=1.5 + 0.6 * i, index_decay=0.05) * dec(n, 150 + 15 * i, 1.0)
    hit = chip(key, 2 * i, character, 1.0, int(r.integers(1 << 30)))
    out = 0.6 * bell
    out[: len(hit)] += hit
    out = out + 0.4 * sine(glide(260, 190, n, 20), n) * dec(n, 18, 0.3)
    return _done(pan2(_soft(out, m), 0) if m["width"] == 0 else spread(out, np.roll(out, int(SR * 0.0007)), 0.3), v)


def logo(key, character: str = "glass", v: float = 0.7, seed=None, notes=None, gap: float = 0.12):
    """The sonic logo: optional hook notes, then a bell on the last one: inharmonic partials ringing
    110 to 380 ms to -20 dB and 1.2 to 2.4 s in all, a strike on top, partials spread a little."""
    m, r = _mat(character), _r(seed)
    notes = list(notes or [])
    f = hz(notes[-1]) if notes else hz(note(key, 7, 4))
    n = int(SR * 2.4)
    ratios = {"metal": (0.5, 1, 1.19, 1.5, 2, 2.5, 2.67, 3.01, 4.17), "glass": (1, 2.32, 4.25, 6.63), "wood": (1, 3.93, 9.2)}.get(
        character, (0.5, 1, 1.2, 2, 2.76, 4.1))
    d20s = [(900 if q < 1 else 360 / q**0.6) * (0.5 if character in ("wood", "plastic") else 1) for q in ratios]
    amps = [(0.35 if q < 1 else 1 / q**0.7) for q in ratios]
    left = modal(n, [f * q for q in ratios[::2]], d20s[::2], amps[::2], r, detune=4)
    right = modal(n, [f * q for q in ratios[1::2]], d20s[1::2], amps[1::2], r, detune=4)
    strike = bp(r.standard_normal(n), 1500, 7000) * dec(n, 4, 0.5) * 0.4
    bell = spread(left + 0.6 * right + strike, right + 0.6 * left + strike, 0.35)
    bell = bell + 0.25 * sine(f / 4, n) * dec(n, 320, 3)
    hum = (0.25 if character in ("wood", "plastic") else 0.4) * sine(f * (0.5 if character != "glass" else 1.0), n) * dec(n, 1150, 8)  # the long tail every bell has
    bell = bell + np.stack([hum, hum])
    k = int(SR * gap * max(0, len(notes) - 1))
    out = np.zeros((2, k + n))
    for j, mm in enumerate(notes[:-1]):
        nb = int(SR * 0.2)
        b = _tone(np.full(nb, hz(mm)), nb, m, 60, r)
        out[:, int(SR * gap * j) : int(SR * gap * j) + len(b)] += pan2(b, 0) * 0.5
    out[:, k:] += bell
    return _done(_crush(_soft(out, m), m), v, 1)


# --- Builds, drops and textures ----------------------------------------------------------------


def riser(key, seconds: float = 1.5, character: str = "glass", v: float = 0.6, seed=None):
    """Noise opening upward (high passed, so it leaves the kick alone) plus three chirps climbing an
    octave to the tonic, widening as it rises. ENDS on its frame."""
    m, r = _mat(character), _r(seed)
    n = int(SR * seconds)
    t = np.linspace(0, 1, n)

    def layer(w):
        return sweep_lp(hp(w, 300), 400 + 8000 * m["air"] * t**2, 1.2) * 0.6

    x = spread(layer(r.standard_normal(n)), layer(r.standard_normal(n)), t) * (0.4 + 0.6 * t)  # widens as it rises
    top = hz(note(key, 7, 5))
    tone = np.zeros(n)
    for k in range(3):
        f = top / 2 * 2**t * (1 + 0.004 * k)
        tone += (sine(f, n) if not m.get("square") else square(f, n) * 0.5) * 0.12
    x = x + pan2(tone, 0)
    return _done(_crush(x * t**2.2, m), v, 3)


def reverse_swell(seconds: float = 1.0, v: float = 0.6, seed=None):
    """A crash played backwards: ENDS on its frame."""
    r = _r(seed)
    n = int(SR * seconds)
    x = spread(hp(r.standard_normal(n), 3500), hp(r.standard_normal(n), 3500), 0.8) * dec(n, seconds * 700, 2)
    return _done(lp(x[:, ::-1], 9000), v, 2)


def sub_drop(seconds: float = 1.2, v: float = 0.8):
    """A falling sub: the floor drops away (a transition into a lower, darker section)."""
    n = int(SR * seconds)
    t = np.arange(n) / SR
    x = sine(90 * np.exp(-t / 0.4) + 28, n) * dec(n, seconds * 400, 5)
    return _done(sat(x, 2.0), v, 5)


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


def texture(seconds: float, character: str, key, v: float = 0.3, seed=None, rate: float = 24):
    """A bed of tiny tonal grains (counting, scanning, data arriving), notes from the scale, at
    random times, pans and levels: off the grid on purpose."""
    r = _r(seed)
    n = int(SR * seconds)
    out = np.zeros((2, n))
    for _ in range(int(seconds * rate)):
        i = int(r.integers(0, max(1, n - int(SR * 0.2))))
        g = blip(key, int(r.integers(0, 9)), character, r.uniform(0.15, 0.5), int(r.integers(1 << 30)), octave=6, ring=12)
        out[:, i : i + len(g)] += pan2(g, r.uniform(-0.8, 0.8))[:, : n - i]
    return out * v
