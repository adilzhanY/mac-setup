"""
Signal building blocks shared by every score: time, filters, oscillators, envelopes, buses,
effects and the master. Nothing here has a style; style lives in instruments.py (timbre),
grooves.py (rhythm) and the film's own music.json (the choices).
"""

from __future__ import annotations

import numpy as np
from pedalboard import Chorus, Compressor, Delay, Distortion, HighpassFilter, HighShelfFilter, LowShelfFilter, Pedalboard, Reverb
from scipy import ndimage, signal

SR = 48_000
rng = np.random.default_rng(1)


def seed(n: int) -> None:
    """Every film seeds its own randomness, so two films never share humanising or noise.
    Reseeds in place, so modules that imported rng see the new stream."""
    rng.bit_generator.state = np.random.default_rng(n).bit_generator.state


def hz(m: float) -> float:
    return 440.0 * 2 ** ((m - 69) / 12)


def times(seconds: float) -> np.ndarray:
    return np.arange(int(SR * seconds)) / SR


def noise(n: int) -> np.ndarray:
    return rng.standard_normal(n)


# --- Filters -----------------------------------------------------------------------------------


def _filt(x, kind, cut, order=2):
    nyq = SR / 2
    if kind == "bandpass":
        w = [max(cut[0], 10) / nyq, min(cut[1], SR * 0.45) / nyq]
    else:
        w = min(max(cut, 10), SR * 0.45) / nyq
    return signal.sosfilt(signal.butter(order, w, kind, output="sos"), x, axis=-1)


def lp(x, cut, order=2):
    return _filt(x, "lowpass", cut, order)


def hp(x, cut, order=2):
    return _filt(x, "highpass", cut, order)


def bp(x, lo, hi, order=2):
    return _filt(x, "bandpass", (lo, hi), order)


def peak(x, f, q, gain_db):
    """A resonant peak (formants, body resonances)."""
    b, a = signal.iirpeak(min(f, SR * 0.45) / (SR / 2), q)
    return x + (10 ** (gain_db / 20) - 1) * signal.lfilter(b, a, x)


def sweep_lp(x, cutoff, q=0.9, block=32):
    """A low pass whose cutoff moves per sample (filter envelopes, acid lines, wobbles).
    Biquads per block of 32 samples with the state carried across, so it sweeps without clicks."""
    cutoff = np.broadcast_to(np.asarray(cutoff, float), x.shape)
    y = np.empty_like(x)
    zi = np.zeros(2)
    for i in range(0, len(x), block):
        f = float(np.clip(cutoff[i], 20, SR * 0.45))
        w = 2 * np.pi * f / SR
        alpha = np.sin(w) / (2 * q)
        c = np.cos(w)
        b = np.array([(1 - c) / 2, 1 - c, (1 - c) / 2])
        a = np.array([1 + alpha, -2 * c, 1 - alpha])
        y[i : i + block], zi = signal.lfilter(b / a[0], a / a[0], x[i : i + block], zi=zi)
    return y


# --- Oscillators -------------------------------------------------------------------------------


def phase_of(freq, n):
    """Running phase in cycles for a constant or per-sample frequency (glides, vibrato)."""
    f = np.broadcast_to(np.asarray(freq, float), (n,))
    return np.cumsum(f) / SR


def sine(freq, n, ph=0.0):
    return np.sin(2 * np.pi * (phase_of(freq, n) + ph))


def tri(freq, n, ph=0.0):
    return signal.sawtooth(2 * np.pi * (phase_of(freq, n) + ph), 0.5)


def _bandlimited(fn, freq, n, ph):
    """Draw at four times the rate and bring it down, so bright waves do not alias."""
    f4 = np.repeat(np.broadcast_to(np.asarray(freq, float), (n,)), 4) if np.ndim(freq) else freq
    p = np.cumsum(np.broadcast_to(np.asarray(f4, float), (n * 4,))) / (SR * 4) + ph
    return signal.resample_poly(fn(2 * np.pi * p), 1, 4)[:n]


def saw(freq, n, ph=0.0):
    return _bandlimited(signal.sawtooth, freq, n, ph)


def square(freq, n, ph=0.0, duty=0.5):
    return _bandlimited(lambda p: signal.square(p, duty), freq, n, ph)


def supersaw(freq, n, voices=7, detune_cents=22, spread=0.9):
    """Detuned saws, returned as stereo."""
    out = np.zeros((2, n))
    for k in range(voices):
        d = (k - (voices - 1) / 2) / max(1, (voices - 1) / 2)
        f = np.asarray(freq, float) * 2 ** (d * detune_cents / 1200)
        out += pan2(saw(f, n, rng.uniform(0, 1)), d * spread)
    return out / np.sqrt(voices)


def karplus(freq, seconds, decay=0.996, bright=0.5):
    """Karplus Strong plucked string: a noise burst one period long, averaged round a loop.
    bright 0 is a soft thumb, 1 a pick."""
    n = int(SR * seconds)
    p = max(2, int(round(SR / freq)))
    buf = lp(noise(p), 1500 + 9000 * bright)
    out = np.empty(n)
    for i in range(n):
        j = i % p
        out[i] = buf[j]
        buf[j] = decay * (buf[j] * (0.5 + 0.25 * bright) + buf[(j + 1) % p] * (0.5 - 0.25 * bright))
    return out / (np.abs(out).max() + 1e-9)


def fm(freq, n, ratio=2.0, index=3.0, index_decay=0.08, fb=0.0):
    """Two operator FM; the modulation index decays so the attack is bright and the tail pure."""
    t = np.arange(n) / SR
    idx = index * np.exp(-t / max(index_decay, 1e-4))
    mod = np.sin(2 * np.pi * phase_of(np.asarray(freq, float) * ratio, n))
    if fb:
        mod = np.sin(2 * np.pi * phase_of(np.asarray(freq, float) * ratio, n) + fb * mod)
    return np.sin(2 * np.pi * phase_of(freq, n) + idx * mod)


# --- Envelopes and shapes ----------------------------------------------------------------------


def adsr(n, a=0.005, d=0.1, s=0.7, r=0.1, hold=None):
    """Attack, decay, sustain until hold seconds, then release. Lengths in seconds."""
    t = np.arange(n) / SR
    hold = n / SR - r if hold is None else hold
    env = np.where(t < a, t / max(a, 1e-5), s + (1 - s) * np.exp(-(t - a) / max(d, 1e-5)))
    rel = np.clip(1 - (t - hold) / max(r, 1e-5), 0, 1)
    return env * np.where(t > hold, rel, 1)


def perc(n, a=0.001, length=0.2):
    t = np.arange(n) / SR
    return np.clip(t / max(a, 1e-5), 0, 1) * np.exp(-np.maximum(t - a, 0) / length)


def fade(x, ms=4):
    """Raised fades at both ends: a waveform that starts at a non zero value is a click."""
    k = min(x.shape[-1] // 2, int(SR * ms / 1000))
    if k > 0:
        ramp = 0.5 - 0.5 * np.cos(np.linspace(0, np.pi, k))
        x[..., :k] *= ramp
        x[..., -k:] *= ramp[::-1]
    return x


def sat(x, drive=1.5):
    return np.tanh(drive * x) / np.tanh(drive)


def fold(x, amount=1.5):
    """Wave folding: a harder, buzzier grit than tanh."""
    return np.sin(np.pi / 2 * amount * x)


def crush(x, bits=8, keep=4):
    """Bit and sample rate reduction (lo fi, phonk, glitch)."""
    y = np.round(x * 2 ** (bits - 1)) / 2 ** (bits - 1)
    return np.repeat(y[::keep], keep)[: len(x)]


def pan2(s, p=0.0):
    a = (np.clip(p, -1, 1) + 1) * np.pi / 4
    return np.stack([s * np.cos(a), s * np.sin(a)])


def stereo(s):
    return s if s.ndim == 2 else pan2(s, 0.0)


def widen(x, ms=11):
    """Haas widening of a mono or stereo part (pads, chords); keep bass and kick out of it."""
    x = stereo(x).copy()
    k = int(SR * ms / 1000)
    x[1] = np.concatenate([np.zeros(k), x[1][:-k]])
    return x


# --- Effects (pedalboard) ----------------------------------------------------------------------


def fx(x, *plugins):
    y = Pedalboard(list(plugins))(stereo(x).astype(np.float32), SR)
    return y.astype(np.float64)


def room(x, size=0.4, wet=0.15, damping=0.5, width=1.0):
    return fx(x, Reverb(room_size=size, damping=damping, wet_level=wet, dry_level=1.0, width=width))


def hall(x, wet=0.3):
    return fx(x, Reverb(room_size=0.9, damping=0.35, wet_level=wet, dry_level=1.0, width=1.0))


def delay(x, seconds, feedback=0.35, mix=0.25):
    return fx(x, Delay(delay_seconds=seconds, feedback=feedback, mix=mix))


def pingpong(x, seconds, feedback=0.4, mix=0.3):
    """Delay bouncing left and right: echoes on alternate sides."""
    x = stereo(x)
    out = x.copy()
    k = int(seconds * SR)
    g = mix
    for i in range(1, 6):
        side = i % 2
        shifted = np.zeros_like(x[0])
        if k * i < x.shape[1]:
            shifted[k * i :] = (x[0] + x[1])[: -k * i] * 0.5
        out[side] += lp(shifted, 6000 - 700 * i) * g
        g *= feedback
    return out


def wow(x, depth_ms=2.2, rate=0.55):
    """Tape wow: a slowly wandering pitch (lofi, nostalgia)."""
    x = stereo(x)
    n = x.shape[1]
    t = np.arange(n) / SR
    d = (depth_ms / 1000) * (0.6 + 0.4 * np.sin(2 * np.pi * rate * t) + 0.15 * np.sin(2 * np.pi * 0.13 * t)) * SR
    idx = np.clip(np.arange(n) - d, 0, n - 1)
    return np.stack([np.interp(idx, np.arange(n), c) for c in x])


def chorus(x, rate=0.6, depth=0.25, mix=0.4):
    return fx(x, Chorus(rate_hz=rate, depth=depth, mix=mix))


def drive(x, db=12):
    return fx(x, Distortion(drive_db=db))


def comp(x, threshold=-18, ratio=3, attack=5, release=120):
    return fx(x, Compressor(threshold_db=threshold, ratio=ratio, attack_ms=attack, release_ms=release))


def gated(x, seconds=0.28):
    """Gated reverb (the eighties snare): a big room cut short."""
    wet = fx(x, Reverb(room_size=0.95, damping=0.2, wet_level=1.0, dry_level=0.0, width=1.0))
    n = min(wet.shape[1], int(seconds * SR))
    wet[:, n:] = 0
    wet[:, :n] *= np.linspace(1, 0.6, n)
    return stereo(x) + wet * 0.8


# --- Buses and mixing --------------------------------------------------------------------------


class Bus:
    """A stereo track. add() places a sound at a time in seconds."""

    def __init__(self, seconds: float):
        self.n = int(round(seconds * SR))
        self.x = np.zeros((2, self.n))

    def add(self, s, t, gain=1.0, pan=0.0):
        s = pan2(s, pan) if s.ndim == 1 else s
        i = int(round(t * SR))
        lo, hi = max(i, 0), min(self.n, i + s.shape[1])
        if hi > lo:
            self.x[:, lo:hi] += s[:, lo - i : hi - i] * gain


def duck_curve(n, hits, depth=0.45, attack=0.003, release=0.11):
    """A sidechain gain curve: dips under every hit time (seconds), the pump of dance music."""
    g = np.ones(n)
    for t in hits:
        i = int(t * SR)
        if i >= n or i < 0:
            continue
        k = np.arange(int(SR * (attack + release * 5)))
        env = np.where(k < attack * SR, k / (attack * SR), np.exp(-(k - attack * SR) / (release * SR)))
        seg = slice(i, min(n, i + len(k)))
        g[seg] = np.minimum(g[seg], 1 - depth * env[: seg.stop - seg.start])
    return g


def rms_db(x):
    return 20 * np.log10(np.sqrt(np.mean(x**2)) + 1e-12)


def band_share(x, lo, hi):
    """Share of the energy between lo and hi Hz (0 to 1)."""
    m = stereo(x).mean(0)
    S = np.abs(np.fft.rfft(m)) ** 2
    f = np.fft.rfftfreq(len(m), 1 / SR)
    return float(S[(f >= lo) & (f < hi)].sum() / (S.sum() + 1e-12))


def balance(x, top=(0.03, 0.10), low=(0.15, 0.55), verbose=True):
    """Keeps the tonal balance in the range finished ads sit in: 3 to 10 percent of the energy above
    8 kHz (more is hiss and fatigue) and 15 to 55 percent under 150 Hz (less sounds thin on a phone
    and small on a TV). Corrects with gentle shelves and says what it did. A genre that wants to
    sit outside (lofi is darker) can pass its own ranges."""
    for _ in range(6):
        hi, lo_ = band_share(x, 8000, SR / 2), band_share(x, 20, 150)
        moves = []
        if hi > top[1]:
            moves.append(HighShelfFilter(cutoff_frequency_hz=7000, gain_db=-2.0))
        elif hi < top[0]:
            moves.append(HighShelfFilter(cutoff_frequency_hz=7000, gain_db=1.5))
        if lo_ < low[0]:
            moves.append(LowShelfFilter(cutoff_frequency_hz=140, gain_db=2.0))
        elif lo_ > low[1]:
            moves.append(LowShelfFilter(cutoff_frequency_hz=140, gain_db=-1.5))
        if not moves:
            break
        x = fx(x, *moves)
    if verbose:
        print(f"  balance: {100 * band_share(x, 8000, SR / 2):.1f}% above 8 kHz, {100 * band_share(x, 20, 150):.1f}% under 150 Hz")
    return x


# --- Master ------------------------------------------------------------------------------------


def true_peak(x):
    return 20 * np.log10(np.abs(signal.resample_poly(x, 4, 1, axis=1)).max() + 1e-12)


def limit(x, ceiling_db):
    """A look ahead limiter whose gain follows the 4x oversampled peak, so true peaks stay down."""
    ceiling = 10 ** (ceiling_db / 20)
    over = np.abs(signal.resample_poly(x, 4, 1, axis=1)).max(axis=0)
    pk = over[: 4 * x.shape[1]].reshape(-1, 4).max(axis=1)
    need = np.minimum(1.0, ceiling / np.maximum(pk, 1e-9))
    look = int(0.004 * SR)
    held = ndimage.minimum_filter1d(np.pad(need, (look, look), constant_values=1), size=2 * look + 1)[look:-look]
    # One pole release, vectorised by running it in the log domain on a decimated curve.
    g = ndimage.minimum_filter1d(held, size=int(0.06 * SR))
    g = ndimage.uniform_filter1d(g, look)
    return x * np.minimum(g, held)


def master(mix, lufs=-14.0, tp=-1.0):
    """High pass, glue, loudness to target, true peak under the ceiling. Returns the master."""
    import pyloudnorm

    mix = fx(mix, HighpassFilter(28), Compressor(threshold_db=-16, ratio=1.8, attack_ms=25, release_ms=160))
    meter = pyloudnorm.Meter(SR)
    for _ in range(8):
        mix *= 10 ** ((lufs - meter.integrated_loudness(mix.T)) / 20)
        if true_peak(mix) <= tp - 0.05:
            break
        mix = limit(mix, tp - 0.4)
    if true_peak(mix) > tp:
        mix *= 10 ** ((tp - 0.05 - true_peak(mix)) / 20)
    return mix
