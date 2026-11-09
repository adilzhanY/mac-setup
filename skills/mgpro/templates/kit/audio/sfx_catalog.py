"""
Analyse the sound effect library so an agent can "see" every sound without ears.

    python sfx_catalog.py                 # analyse ~/.local/share/mgpro/sfx, write catalog + sheets
    python sfx_catalog.py --synth         # also render sfx.py's effects and analyse them the same way
    python sfx_catalog.py --synth-only --check   # only the effects, each against the library targets
    python sfx_catalog.py --file a.wav    # print the analysis of one file (check a new effect)

Run it with the library venv: ~/.local/share/mgpro/.venv/bin/python (numpy, scipy, librosa,
soundfile, pyloudnorm, matplotlib; pedalboard too for --synth).

Writes, next to the skill (../../../sfx/ from this file):
    catalog.json     every sound with its numbers, plus per category summaries
    CATALOG.md       one table per category, readable
    sheets/*.png     contact sheets: waveform plus mel spectrogram per sound, one set per category
    synth.json       (--synth) the same numbers for every effect sfx.py makes
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from multiprocessing import Pool
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
SKILL = HERE.parents[2]
LIB = Path.home() / ".local/share/mgpro/sfx"
OUT = SKILL / "sfx"
EXTS = {".wav", ".ogg", ".flac", ".mp3"}

CATEGORIES = ["click/tap", "pop", "whoosh/swish", "impact/thud", "riser", "tonal/bell", "glitch/digital", "texture/noise", "foley"]

# Filename words that name the category outright. Checked in this order, first match wins.
NAME_RULES = [
    ("tonal/bell", r"jingle"),  # Kenney "jingles_HIT00" are musical stings, not hits
    ("riser", r"rise|riser|charge|power_?up|level_?up|teleport|morph|slomo"),
    ("whoosh/swish", r"whoosh|swish|swosh|megaswosh|whip|swoosh|woosh|swing|swipe|wind|air_|air$"),
    ("pop", r"pop|bubble|blop|plop|drop|droplet|bloop"),
    ("click/tap", r"click|clic|tap|tick|button|switch|toggle|select|key|press|menu_?move|scroll|cursor|rollover|shutter"),
    ("impact/thud", r"impact|hit|punch|thud|slam|explosion|explode|crash|knock|bang|boom|heavy|thump|kick|collide|land"),
    ("tonal/bell", r"bell|ding|chime|confirm|jingle|success|complete|glass_\d|maximize|minimize|notif|positive|negative|bong|level|coin|pickup|win|ability|question|pluck"),
    ("texture/noise", r"engine|ambien|loop|noise|forcefield|force_field|static|hum|rumble|thruster"),
    ("glitch/digital", r"glitch|laser|zap|phaser|phase|beep|retro|synth|digital|error|computer|bleep|blip|two_?tone|three_?tone|pep|low_?down|high_?up|space|tone"),
    ("foley", r"footstep|door|cloth|book|chop|handle|drawer|creak|card|chip|dice|toilet|paper|zip|leather|belt|knife|metal_?pot|latch|pot|wood|water|spring|chair|rock|break|fall|glass|shatter|squeak|gong|scratch|machine|tool|splash|dish"),
]
"""Each word must start a token of the snake cased file name (impactWood_heavy -> impact_wood_heavy)."""


def load(path):
    """(channels x samples float32, sample rate). Uses soundfile, falls back to librosa for odd mp3s."""
    import soundfile as sf
    try:
        x, sr = sf.read(str(path), always_2d=True, dtype="float32")
        x = x.T
    except Exception:
        import librosa
        x, sr = librosa.load(str(path), sr=None, mono=False)
        x = np.atleast_2d(x)
    return x[:2], sr


def envelope(mono, sr, ms=1.0):
    """RMS envelope, one value per ms (2 ms window)."""
    hop = max(1, int(sr * ms / 1000))
    win = hop * 2
    padded = np.pad(mono, (0, win))
    frames = np.lib.stride_tricks.sliding_window_view(padded ** 2, win)[::hop]
    return np.sqrt(frames.mean(1) + 1e-20)


def db(v):
    return float(20 * np.log10(max(float(v), 1e-10)))


def k_weighted_ms(x, sr):
    """Mean square of the K-weighted signal per channel (the loudness filter of BS.1770)."""
    import pyloudnorm as pyln
    meter = pyln.Meter(sr)
    y = x.T.astype(np.float64)
    for f in meter._filters.values():
        y = f.apply_filter(y)
    return (y ** 2).mean(0), meter


def note_name(hz):
    import librosa
    return librosa.hz_to_note(hz, unicode=False)


def analyse(path, rel=None):
    import librosa
    x, sr = load(path)
    n = x.shape[1]
    mono = x.mean(0)
    peak = float(np.abs(x).max()) if n else 0.0
    out = {"path": rel or str(path), "sr": sr, "channels": x.shape[0], "file_ms": round(1000 * n / sr, 1)}
    if peak < 1e-5 or n < sr * 0.003:
        out.update(silent=True)
        return out

    env = envelope(mono, sr)
    ep = env.max()
    ipk = int(env.argmax())
    above40 = np.nonzero(env >= ep * 10 ** (-40 / 20))[0]
    start, end = int(above40[0]), int(above40[-1])
    pre = env[: ipk + 1]
    t10 = int(np.nonzero(pre >= 0.1 * ep)[0][0])
    t90 = int(np.nonzero(pre >= 0.9 * ep)[0][0])
    seg = x[:, int(start * sr / 1000): int((end + 1) * sr / 1000) + 1]

    # Loudness: integrated (gated) when long enough, otherwise K-weighted RMS over the sounding part.
    ms, meter = k_weighted_ms(seg if seg.shape[1] > 64 else x, sr)
    lufs_est = -0.691 + 10 * np.log10(ms.sum() + 1e-20)
    lufs, method = lufs_est, "rms"
    if n >= 0.45 * sr:
        try:
            v = meter.integrated_loudness(x.T.astype(np.float64))
            if np.isfinite(v):
                lufs, method = v, "integrated"
        except ValueError:
            pass

    # Spectral shape, weighted by frame energy over the sounding part.
    mono_seg = seg.mean(0)
    nfft = 1024 if sr <= 48000 else 2048
    y = np.pad(mono_seg, (0, max(0, nfft - len(mono_seg))))
    S = np.abs(librosa.stft(y, n_fft=nfft, hop_length=256)) + 1e-12
    w = (S ** 2).sum(0)
    w = w / w.sum()
    # Centroid, bandwidth and rolloff weighted by POWER (librosa weights by magnitude, which lets a
    # quiet broadband floor drag the centroid of a low "whum" up to 1.5 kHz).
    freqs = librosa.fft_frequencies(sr=sr, n_fft=nfft)[:, None]
    P = S ** 2
    cent = (freqs * P).sum(0) / P.sum(0)
    band = np.sqrt((((freqs - cent) ** 2) * P).sum(0) / P.sum(0))
    roll = freqs[np.argmax(np.cumsum(P, 0) >= 0.85 * P.sum(0), 0), 0]
    centroid = float((cent * w).sum())
    flat = librosa.feature.spectral_flatness(S=S)[0]
    flatness = float((flat * w).sum())
    # Noisiness: share of energy NOT in narrow peaks standing 10 dB over the local median spectrum.
    # Unlike flatness it ignores spectral tilt, so a band passed whoosh reads as noise (above 0.7)
    # and a ring or bell as tone (under 0.3).
    from scipy.ndimage import median_filter
    Pn = P[int(30 * nfft / sr) + 1:]  # drop DC and sub rumble, which some files carry
    peaks = Pn > 10 * median_filter(Pn, size=(31, 1), mode="reflect")
    noisiness = float(((1 - (Pn * peaks).sum(0) / Pn.sum(0)) * w).sum())
    f1 = freqs[:, 0]
    bands = {name: round(float(P[(f1 >= lo) & (f1 < hi)].sum() / P.sum()), 3)
             for name, lo, hi in (("sub", 0, 120), ("low", 120, 500), ("mid", 500, 2000), ("presence", 2000, 6000), ("air", 6000, sr))}

    # Pitch: pYIN on the sounding part, at most 3 s of it.
    f0, vflag, vprob = librosa.pyin(mono_seg[: 3 * sr] if len(mono_seg) > 2048 else np.pad(mono_seg, (0, 2048)),
                                     fmin=55, fmax=min(4200, sr / 4), sr=sr, frame_length=2048, hop_length=256)
    voiced = f0[vflag & np.isfinite(f0)] if f0 is not None else np.array([])
    voiced_share = float(np.mean(vflag)) if len(vflag) else 0.0
    tonal = len(voiced) >= 3 and voiced_share >= 0.35 and noisiness < 0.5
    pitch_hz = float(np.median(voiced)) if tonal else None

    # Movement: f0 when tonal, otherwise the centroid; first third against last third, in semitones.
    def move(track):
        track = np.asarray(track, float)
        track = track[np.isfinite(track) & (track > 0)]
        if len(track) < 4:
            return 0.0
        k = max(1, len(track) // 3)
        return float(12 * np.log2(np.median(track[-k:]) / np.median(track[:k])))
    semis = move(voiced) if tonal else move(cent[w > 0.2 / len(w)])
    movement = "rising" if semis > 1.5 else "falling" if semis < -1.5 else "flat"

    # Stereo width: side RMS over mid RMS (0 is mono, 1 is very wide).
    width = 0.0
    if x.shape[0] == 2:
        mid, side = (x[0] + x[1]) / 2, (x[0] - x[1]) / 2
        width = float(np.sqrt((side ** 2).mean()) / (np.sqrt((mid ** 2).mean()) + 1e-12))

    onset_env = librosa.onset.onset_strength(y=np.pad(mono, (0, 2048)), sr=sr, hop_length=128)
    onsets = librosa.onset.onset_detect(onset_envelope=onset_env, sr=sr, hop_length=128, delta=0.25, wait=8, units="time")

    out.update(
        length_ms=end - start + 1,
        lead_ms=start,
        peak_db=round(db(peak), 1),
        rms_db=round(db(np.sqrt((seg ** 2).mean())), 1),
        lufs=round(float(lufs), 1),
        lufs_method=method,
        attack_ms=max(0, t90 - t10),
        peak_at_ms=ipk - start,
        decay_ms=end - ipk,
        decay20_ms=int(np.argmax(env[ipk:] < ep * 0.1)) if (env[ipk:] < ep * 0.1).any() else end - ipk,
        centroid_hz=round(centroid),
        rolloff_hz=round(float((roll * w).sum())),
        bandwidth_hz=round(float((band * w).sum())),
        flatness=round(flatness, 4),
        noisiness=round(noisiness, 2),
        tonal=bool(tonal),
        pitch_hz=round(pitch_hz, 1) if pitch_hz else None,
        note=note_name(pitch_hz) if pitch_hz else None,
        movement=movement,
        movement_semitones=round(semis, 1),
        movement_basis="pitch" if tonal else "centroid",
        width=round(width, 2),
        bands=bands,
        floor_db=round(db(np.percentile(env, 10) / ep), 1),
        clipped=int((np.abs(x) >= 0.999).sum()),
        transients=max(1, len(onsets)),
    )
    return out


def categorise(s, name):
    stem = re.sub(r"([a-z])([A-Z0-9])", r"\1_\2", Path(name).stem)  # the file name only: folder names (krank "spring", "winter") would mislead
    stem = re.sub(r"[^a-z0-9]+", "_", stem.lower())
    for cat, rx in NAME_RULES:
        if re.search(rf"(?:^|_)(?:{rx})", stem):
            return cat, "name"
    L, a, c, nz = s["length_ms"], s["attack_ms"], s["centroid_hz"], s["noisiness"]
    if s["movement"] == "rising" and s["peak_at_ms"] > 0.5 * L and L > 300:
        return "riser", "features"
    if nz > 0.7 and a > 40 and L > 200:
        return ("texture/noise" if L > 1500 else "whoosh/swish"), "features"
    if c < 900 and a < 15:
        return "impact/thud", "features"
    if L < 120 and not s["tonal"]:
        return "click/tap", "features"
    if s["tonal"] and L < 250:
        return "pop", "features"
    if s["tonal"]:
        return "tonal/bell", "features"
    if s["transients"] > 3:
        return "glitch/digital", "features"
    return "foley", "features"


def describe(s):
    L, a, c, nz = s["length_ms"], s["attack_ms"], s["centroid_hz"], s["noisiness"]
    words = ["tiny" if L < 60 else "short" if L < 150 else "medium" if L < 450 else "long" if L < 1500 else "very long"]
    words.append("sharp" if a < 3 else "quick" if a < 15 else "soft onset" if a < 80 else "slow swell")
    words.append("dark" if c < 500 else "warm" if c < 1500 else "present" if c < 3000 else "bright" if c < 6000 else "airy")
    words.append("pure tone" if s["tonal"] and nz < 0.1 else "tonal" if s["tonal"] else "noisy" if nz > 0.7 else "part tone, part noise")
    if s["tonal"]:
        words.append(f"at {s['note']}")
    if s["movement"] != "flat":
        words.append(f"{s['movement']} {abs(s['movement_semitones']):.0f} st")
    if s["transients"] > 1:
        words.append(f"{s['transients']} hits")
    if s["width"] > 0.25:
        words.append("wide")
    return ", ".join(words)


def _job(args):
    path, rel = args
    try:
        return analyse(path, rel)
    except Exception as e:  # one broken file must not stop the catalogue
        return {"path": rel, "error": repr(e)}


def scan(root):
    files = sorted(p for p in root.rglob("*") if p.suffix.lower() in EXTS)
    with Pool() as pool:
        rows = pool.map(_job, [(p, str(p.relative_to(root))) for p in files], chunksize=4)
    for r in rows:
        r["pack"] = r["path"].split("/")[0]
        r["name"] = Path(r["path"]).stem
        if "length_ms" in r:
            inner = "/".join(r["path"].split("/")[1:])
            r["category"], r["category_basis"] = categorise(r, inner)
            r["character"] = describe(r)
    return rows


def summarise(rows):
    keys = ["length_ms", "attack_ms", "decay20_ms", "decay_ms", "centroid_hz", "rolloff_hz", "flatness", "noisiness", "lufs"]
    out = {}
    for cat in CATEGORIES:
        rs = [r for r in rows if r.get("category") == cat]
        if not rs:
            continue
        d = {"count": len(rs), "tonal_share": round(np.mean([r["tonal"] for r in rs]), 2)}
        for k in keys:
            v = np.array([r[k] for r in rs], float)
            d[k] = {"p25": round(float(np.percentile(v, 25)), 4), "median": round(float(np.median(v)), 4), "p75": round(float(np.percentile(v, 75)), 4)}
        d["movement"] = {m: sum(r["movement"] == m for r in rs) for m in ("rising", "falling", "flat")}
        out[cat] = d
    return out


def slug(cat):
    return cat.replace("/", "-")


def write_md(rows, summary, path):
    lines = ["# Sound effect catalogue", "",
             f"{len(rows)} sounds from {len({r['pack'] for r in rows})} packs, all CC0. Library root: `~/.local/share/mgpro/sfx/`. "
             "Generated by `templates/kit/audio/sfx_catalog.py`; do not edit by hand. Numbers are measured, not heard. "
             "Length is the sounding part (first to last point within 40 dB of the peak); attack is 10 to 90 percent of the peak; decay20 is peak to -20 dB (the part you hear), decay to -40 dB is the tail; "
             "centroid is power weighted (energy over the sounding part); pitch is pYIN on tonal sounds only. Contact sheets per category are in `sheets/`.", ""]
    for cat in CATEGORIES:
        rs = sorted((r for r in rows if r.get("category") == cat), key=lambda r: (r["pack"], r["name"]))
        if not rs:
            continue
        s = summary[cat]
        lines += [f"## {cat} ({len(rs)})", "",
                  f"Median length {s['length_ms']['median']:.0f} ms, attack {s['attack_ms']['median']:.0f} ms, "
                  f"centroid {s['centroid_hz']['median']:.0f} Hz, tonal {s['tonal_share']*100:.0f} percent. "
                  f"Sheets: `sheets/{slug(cat)}-*.png`.", "",
                  "| name | pack | length ms | attack ms | centroid Hz | pitch | character | path |", "|---|---|---|---|---|---|---|---|"]
        for r in rs:
            pitch = f"{r['note']} ({r['pitch_hz']:.0f} Hz)" if r["tonal"] else "none"
            lines.append(f"| {r['name']} | {r['pack']} | {r['length_ms']} | {r['attack_ms']} | {r['centroid_hz']} | {pitch} | {r['character']} | `{r['path']}` |")
        lines.append("")
    path.write_text("\n".join(lines))


def sheets(rows, root, outdir, per_page=48, cols=6):
    """Per category, pages of tiles: waveform (top) and mel spectrogram (bottom, 0 to -80 dB of the
    file's own peak, mel axis to 16 kHz), title = name, length and centroid."""
    import librosa
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from PIL import Image

    outdir.mkdir(parents=True, exist_ok=True)
    for old in outdir.glob("*.png"):
        old.unlink()
    for cat in CATEGORIES:
        rs = sorted((r for r in rows if r.get("category") == cat), key=lambda r: (r["pack"], r["name"]))
        for page in range(0, len(rs), per_page):
            chunk = rs[page: page + per_page]
            nrows = (len(chunk) + cols - 1) // cols
            fig = plt.figure(figsize=(cols * 2.5, nrows * 2.05), dpi=80)
            fig.patch.set_facecolor("white")
            gs = fig.add_gridspec(nrows * 2, cols, height_ratios=[1, 2.2] * nrows, hspace=0.55, wspace=0.12,
                                  left=0.01, right=0.99, top=1 - 0.25 / nrows, bottom=0.01)
            for i, r in enumerate(chunk):
                x, sr = load(root / r["path"])
                mono = x.mean(0)
                a = int(r["lead_ms"] * sr / 1000)
                b = min(len(mono), a + int((r["length_ms"] + 30) * sr / 1000))
                seg = mono[a:b]
                row, col = divmod(i, cols)
                ax = fig.add_subplot(gs[2 * row, col])
                ax.plot(np.arange(len(seg)) / sr * 1000, seg / (np.abs(seg).max() + 1e-9), color="#222", lw=0.4)
                ax.set_xlim(0, max(1, len(seg) / sr * 1000))
                ax.set_ylim(-1.05, 1.05)
                ax.axis("off")
                pitch = r["note"] if r["tonal"] else "no pitch"
                ax.set_title(f"{r['name'][:24]}\n{r['length_ms']} ms  {r['centroid_hz']} Hz  {pitch}", fontsize=7, pad=2)
                ax2 = fig.add_subplot(gs[2 * row + 1, col])
                y = np.pad(seg, (0, max(0, 2048 - len(seg))))
                M = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=1024, hop_length=max(64, len(y) // 160), n_mels=64, fmax=min(16000, sr / 2))
                ax2.imshow(librosa.power_to_db(M, ref=np.max, top_db=80), origin="lower", aspect="auto", cmap="magma", vmin=-80, vmax=0)
                ax2.set_xticks([])
                ax2.set_yticks([])
            name = outdir / f"{slug(cat)}-{page // per_page + 1}.png"
            fig.savefig(name)
            plt.close(fig)
            Image.open(name).convert("RGB").quantize(colors=64).save(name, optimize=True)


# Ranges a synthesized effect should land in (sfx/ANALYSIS.md section 4), as (low, high) per measure.
# below500 is the share of energy under 500 Hz, above2k over 2 kHz, below2k under 2 kHz.
TARGETS = {
    "tap": dict(attack_ms=(0, 3), decay20_ms=(4, 15), length_ms=(10, 80), centroid_hz=(1500, 4500), below500=(0, 0.15), noisiness=(0.6, 1.0), width=(0, 0.4)),
    "click": dict(attack_ms=(0, 3), decay20_ms=(4, 15), length_ms=(10, 140), centroid_hz=(1500, 4500), below500=(0, 0.15), noisiness=(0.55, 1.0), width=(0, 0.4)),
    "tick": dict(attack_ms=(0, 1), decay20_ms=(4, 9), length_ms=(9, 25), centroid_hz=(3000, 10000), above2k=(0.5, 0.95), width=(0, 0.05)),
    "blip": dict(attack_ms=(0, 2), decay20_ms=(13, 35), length_ms=(35, 180), centroid_hz=(1200, 3500), noisiness=(0.05, 0.3), width=(0, 0.3)),
    "pop": dict(attack_ms=(1, 5), decay20_ms=(10, 40), length_ms=(70, 110), centroid_hz=(650, 1000), presence=(0, 0.03), noisiness=(0, 0.2), movement_semitones=(3, 7)),
    "text": dict(decay20_ms=(13, 21), length_ms=(43, 96), centroid_hz=(900, 2000), movement_semitones=(-28, -5)),
    "toggle": dict(attack_ms=(0, 3), decay20_ms=(40, 80), centroid_hz=(1000, 3500)),
    "card": dict(attack_ms=(0, 5), decay20_ms=(12, 30), length_ms=(80, 180), centroid_hz=(70, 450), below500=(0.85, 1.0), low=(0.45, 1.0), width=(0, 0.05)),
    "chip": dict(attack_ms=(0, 5), decay20_ms=(45, 87), length_ms=(105, 185)),
    "impact": dict(attack_ms=(0, 12), decay20_ms=(30, 70), length_ms=(400, 1000), centroid_hz=(70, 420), sub=(0.55, 0.8), low=(0.2, 0.35), width=(0, 0.5)),
    "swish": dict(attack_ms=(10, 30), decay20_ms=(8, 28), length_ms=(60, 160), centroid_hz=(200, 600), below2k=(0.9, 1.0), width=(0, 0.3)),
    "whoosh": dict(attack_ms=(30, 100), decay20_ms=(30, 90), length_ms=(300, 500), centroid_hz=(300, 550), low=(0.6, 1.0), width=(0.4, 1.2)),
    "airy": dict(attack_ms=(70, 170), decay20_ms=(250, 440), length_ms=(500, 1100), centroid_hz=(5000, 8500), air=(0.3, 0.9), noisiness=(0.8, 0.98), width=(0.4, 0.9)),
    "panel_open": dict(attack_ms=(150, 280), length_ms=(220, 330), centroid_hz=(6000, 13000), movement_semitones=(6, 17)),
    "panel_close": dict(attack_ms=(0, 15), length_ms=(200, 330), movement_semitones=(-17, -5)),
    "success": dict(decay20_ms=(190, 290), length_ms=(280, 520), centroid_hz=(1200, 2600), width=(0, 0.6)),
    "error": dict(attack_ms=(0, 15), decay20_ms=(40, 75), length_ms=(100, 220), centroid_hz=(180, 1000), noisiness=(0.15, 0.45), width=(0, 0.05)),
    "logo": dict(attack_ms=(0, 50), decay20_ms=(110, 380), length_ms=(1200, 2400), centroid_hz=(700, 3000), width=(0, 0.5)),
}


def measure(r, k):
    b = r["bands"]
    return {"below500": b["sub"] + b["low"], "above2k": b["presence"] + b["air"], "below2k": b["sub"] + b["low"] + b["mid"],
            "sub": b["sub"], "low": b["low"], "presence": b["presence"], "air": b["air"]}.get(k, r.get(k))


def check(srows):
    """Print each synthesized effect against its target ranges: measured value, and a star when outside."""
    hit = tot = 0
    for name in TARGETS:
        rows = [r for r in srows if r["name"].rsplit("_", 1)[0] == name or r["name"] == name]
        if not rows:
            continue
        keys = list(TARGETS[name])
        print(f"\n{name}: " + ", ".join(f"{k} {lo:g} to {hi:g}" for k, (lo, hi) in TARGETS[name].items()))
        for r in rows:
            cells = []
            for k in keys:
                v = measure(r, k)
                lo, hi = TARGETS[name][k]
                ok = v is not None and lo <= v <= hi
                hit, tot = hit + ok, tot + 1
                cells.append(f"{k[:9]} {v:.3g}{'' if ok else '*'}")
            print(f"  {r['name']:22s} " + "  ".join(cells))
    print(f"\n{hit} of {tot} measures inside the library ranges (* marks the rest)")


def render_synth(tmp):
    """Render each effect sfx.py makes (every character) to wav files in tmp."""
    import soundfile as sf
    sys.path.insert(0, str(HERE))
    import dsp
    import sfx
    from theory import Key
    dsp.seed(7)
    key = Key("G", "ionian")
    made = {}
    for ch in sfx.CHARACTERS:
        made[f"tap_{ch}"] = sfx.tap(ch, seed=1)
        made[f"click_{ch}"] = sfx.click(ch, seed=1)
        made[f"tick_{ch}"] = sfx.tick(ch, seed=1)
        made[f"blip_{ch}"] = sfx.blip(key, 4, ch, seed=1)
        made[f"pop_{ch}"] = sfx.pop(key, 2, ch, seed=1)
        made[f"text_{ch}"] = sfx.text(key, 2, ch, seed=1)
        made[f"toggle_{ch}"] = sfx.toggle(key, True, ch, seed=1)
        made[f"card_{ch}"] = sfx.card(ch, seed=1)
        made[f"chip_{ch}"] = sfx.chip(key, 0, ch, seed=1)
        made[f"impact_{ch}"] = sfx.impact(ch, seed=1)
        made[f"swish_{ch}"] = sfx.swish(0.12, ch, seed=1)
        made[f"whoosh_{ch}"] = sfx.whoosh(0.45, ch, seed=1)
        made[f"airy_{ch}"] = sfx.whoosh(0.8, ch, seed=1, air=True)
        made[f"panel_open_{ch}"] = sfx.panel(True, ch, seed=1)
        made[f"panel_close_{ch}"] = sfx.panel(False, ch, seed=1)
        made[f"success_{ch}"] = sfx.success(key, ch, seed=1)
        made[f"error_{ch}"] = sfx.error(key, ch, seed=1)
        made[f"tier_{ch}"] = sfx.tier(key, 1, ch, seed=1)
        made[f"logo_{ch}"] = sfx.logo(key, ch, seed=1)
        made[f"riser_{ch}"] = sfx.riser(key, 1.5, ch, seed=1)
        made[f"texture_{ch}"] = sfx.texture(2.0, ch, key, seed=1)
    made["boom"] = sfx.boom("glass", seed=1)
    made["transition"] = sfx.transition(0.35, "glass", seed=1)
    made["reverse_swell"] = sfx.reverse_swell(seed=1)
    made["sub_drop"] = sfx.sub_drop()
    made["stutter"] = sfx.stutter(sfx.blip(key, 4, "digital", seed=1))
    tmp.mkdir(parents=True, exist_ok=True)
    for k, v in made.items():
        v = np.asarray(v, float)
        v = v * min(1.0, 0.89 / np.abs(v).max())  # keep the synth's own level, only pull overs down to -1 dBFS
        sf.write(tmp / f"{k}.wav", v.T if v.ndim == 2 else v, dsp.SR, subtype="PCM_24")
    return tmp


def synth_rows():
    import shutil
    import tempfile
    tmp = render_synth(Path(tempfile.mkdtemp(prefix="mgpro-synth-")))
    srows = []
    for p in sorted(tmp.glob("*.wav")):
        r = analyse(p, p.name)
        r["name"] = p.stem
        r["character"] = describe(r)
        srows.append(r)
    shutil.rmtree(tmp)
    return srows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=LIB)
    ap.add_argument("--out", type=Path, default=OUT)
    ap.add_argument("--synth", action="store_true", help="also analyse sfx.py's effects into synth.json")
    ap.add_argument("--synth-only", action="store_true", help="only analyse sfx.py's effects (no library scan)")
    ap.add_argument("--check", action="store_true", help="with --synth or --synth-only: print every effect against the targets")
    ap.add_argument("--no-sheets", action="store_true")
    ap.add_argument("--file", type=Path, help="analyse one file and print it")
    a = ap.parse_args()

    if a.file:
        r = analyse(a.file)
        r["category"], r["category_basis"] = categorise(r, a.file.name)
        r["character"] = describe(r)
        print(json.dumps(r, indent=1))
        return

    a.out.mkdir(parents=True, exist_ok=True)
    if a.synth_only:
        srows = synth_rows()
        (a.out / "synth.json").write_text(json.dumps(srows, indent=1))
        print(f"{len(srows)} synth effects analysed into {a.out / 'synth.json'}")
        if a.check:
            check(srows)
        return
    rows = scan(a.root)
    bad = [r for r in rows if "length_ms" not in r]
    rows = [r for r in rows if "length_ms" in r]
    summary = summarise(rows)
    (a.out / "catalog.json").write_text(json.dumps({"root": "~/.local/share/mgpro/sfx", "count": len(rows),
                                                    "skipped": bad, "summary": summary, "sounds": rows}, indent=1))
    write_md(rows, summary, a.out / "CATALOG.md")
    print(f"{len(rows)} sounds, {len(bad)} skipped; " + ", ".join(f"{c} {summary[c]['count']}" for c in summary))
    if not a.no_sheets:
        sheets(rows, a.root, a.out / "sheets")

    if a.synth:
        srows = synth_rows()
        (a.out / "synth.json").write_text(json.dumps(srows, indent=1))
        print(f"{len(srows)} synth effects analysed")
        if a.check:
            check(srows)


if __name__ == "__main__":
    main()
