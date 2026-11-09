"""
Measure a whole soundtrack the way 129 professional motion graphics films were measured
(mgpro-research/films/analyze.py and cutsync.py, ported here so the kit stands alone). The numbers
are comparable with the professional distribution in pro_stats.json.

    from filmstats import analyze, cut_rise, tone
    r = analyze("public/film.wav")          # loudness, LRA, opening, centroid, rolloff, onsets,
                                             # tempo, grid offset, dips, density, transient patches
    cut_rise("public/film.wav", [2.0, 6.5])  # onset strength at the cuts over the baseline

Every figure is measured, not heard.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

SR = 44100
SR_A = 22050
HOP = 256  # onset and beat hop at 22050 Hz, 11.6 ms
CLUSTER_T = 0.3
PROFILE = ["tempo_bpm", "onset_density_per_s", "percussive_share", "low_share_below_120hz", "loudness_range_lu",
           "peak_3s_pos_pct", "grid_offset_norm", "stereo_side_share", "dips_per_10s", "density2s_cv"]
PRO = Path(__file__).resolve().parent / "pro_stats.json"


def pro_stats() -> dict:
    return json.loads(PRO.read_text())


def _kweight(x, meter):
    y = x.copy()
    for f in meter._filters.values():
        y = f.apply_filter(y)
    return y


def _window_loudness(ms, sr, win_s, hop_s):
    """ms: summed per channel K weighted power per sample. Returns LUFS per window."""
    c = np.concatenate([[0], np.cumsum(ms)])
    w, h = int(win_s * sr), int(hop_s * sr)
    starts = np.arange(0, max(1, len(ms) - w + 1), h)
    p = (c[np.minimum(starts + w, len(ms))] - c[starts]) / w
    return -0.691 + 10 * np.log10(np.maximum(p, 1e-12)), starts / sr


def _lra(st):
    st = st[st > -70]
    if st.size < 2:
        return 0.0
    rel = -0.691 + 10 * np.log10(np.mean(10 ** ((st + 0.691) / 10))) - 20
    st = st[st > rel]
    return float(np.percentile(st, 95) - np.percentile(st, 10)) if st.size > 1 else 0.0


def _load(wav_or_array, sr_in=None):
    import soundfile as sf
    from scipy.signal import resample_poly

    if isinstance(wav_or_array, (str, Path)):
        x, sr = sf.read(str(wav_or_array), always_2d=True)
    else:
        x = np.asarray(wav_or_array, float)
        x = x.T if x.ndim == 2 and x.shape[0] <= 2 else x.reshape(-1, 1)
        sr = sr_in
    if sr != SR:
        x = resample_poly(x, SR, sr, axis=0)
    return x[:, :2] if x.shape[1] >= 2 else np.repeat(x, 2, axis=1)


def loudness(x) -> dict:
    """Integrated loudness, LRA, the 1 s curve and the opening second against the whole (LU)."""
    import pyloudnorm as pyln

    meter = pyln.Meter(SR)
    integ = float(meter.integrated_loudness(x))
    ms = (_kweight(x, meter) ** 2).sum(axis=1)
    st, _ = _window_loudness(ms, SR, 3.0, 0.1)
    l1, _ = _window_loudness(ms, SR, 1.0, 1.0)
    dur = len(x) / SR
    return {"lufs_integrated": integ, "loudness_range_lu": _lra(st), "loudness_curve_1s": [round(float(v), 1) for v in l1],
            "opening_lu": float(l1[0] - integ) if len(l1) else 0.0,
            "peak_3s_pos_pct": float(100 * (np.argmax(st) * 0.1 + 1.5) / dur), "_st": st}


def tone(mono_22k) -> dict:
    """Median spectral centroid and 85 percent rolloff over the frames within 40 dB of the loud
    level, as analyze.py measures them (librosa, magnitude weighted)."""
    import librosa

    S = np.abs(librosa.stft(mono_22k, n_fft=2048, hop_length=512))
    P = S**2
    frame_db = 10 * np.log10(P.sum(axis=0) + 1e-12)
    active = frame_db > np.percentile(frame_db, 95) - 40
    cen = librosa.feature.spectral_centroid(S=S, sr=SR_A)[0]
    rol = librosa.feature.spectral_rolloff(S=S, sr=SR_A, roll_percent=0.85)[0]
    freqs = librosa.fft_frequencies(sr=SR_A, n_fft=2048)
    tot = P.sum() + 1e-12
    return {"centroid_median_hz": float(np.median(cen[active])), "rolloff_median_hz": float(np.median(rol[active])),
            "low_share_below_120hz": float(P[freqs < 120].sum() / tot), "high_share_above_6khz": float(P[freqs > 6000].sum() / tot),
            "_S": S}


def analyze(wav, sr=None, patches=True) -> dict:
    """Every metric of the professional study that a score can be checked against. wav is a path or
    a (channels x samples) array with its sample rate."""
    import librosa
    from scipy.cluster.hierarchy import fcluster, linkage

    x = _load(wav, sr)
    dur = len(x) / SR
    mono = x.mean(axis=1)
    r = {"duration_s": round(dur, 2)}
    lo = loudness(x)
    lo.pop("_st")
    r.update(lo)
    y = librosa.resample(mono, orig_sr=SR, target_sr=SR_A)
    tn = tone(y)
    S = tn.pop("_S")
    r.update(tn)

    L, R = x[:, 0], x[:, 1]
    mid, side = (L + R) / 2, (L - R) / 2
    em, es = np.sum(mid**2), np.sum(side**2)
    r["stereo_side_share"] = float(es / (em + es + 1e-12))

    H, Pp = librosa.decompose.hpss(S)
    r["percussive_share"] = float((Pp**2).sum() / ((Pp**2).sum() + (H**2).sum() + 1e-12))

    oenv = librosa.onset.onset_strength(y=y, sr=SR_A, hop_length=HOP)
    on_f = librosa.onset.onset_detect(onset_envelope=oenv, sr=SR_A, hop_length=HOP)
    on_t = librosa.frames_to_time(on_f, sr=SR_A, hop_length=HOP)
    r["onset_density_per_s"] = float(len(on_t) / dur)
    cnt, _ = np.histogram(on_t, bins=np.arange(0, dur + 2, 2.0))
    dens = cnt / 2.0
    r["onset_density_2s"] = [float(v) for v in dens]
    r["density2s_cv"] = float(np.std(dens) / (np.mean(dens) + 1e-9))
    med = np.median(dens) if dens.size else 0
    # Density late in the film against the film's median: pros stay busy to about 85 percent.
    r["density_at_80pct"] = float(np.sum((on_t > 0.75 * dur) & (on_t < 0.85 * dur)) / (0.1 * dur))
    r["density_median"] = float(med)
    strengths = oenv[on_f] if len(on_f) else np.array([])
    r["onset_strength_cv"] = float(np.std(strengths) / (np.mean(strengths) + 1e-9)) if strengths.size else 0.0

    tempo, beats = librosa.beat.beat_track(onset_envelope=oenv, sr=SR_A, hop_length=HOP)
    tempo = float(np.atleast_1d(tempo)[0])
    bt = librosa.frames_to_time(beats, sr=SR_A, hop_length=HOP)
    r["tempo_bpm"] = tempo
    ac = librosa.autocorrelate(oenv - oenv.mean(), max_size=int(4 * SR_A / HOP))
    ac = ac / (ac[0] + 1e-12)
    li = int(round(60.0 / tempo * SR_A / HOP)) if tempo > 0 else 0
    r["pulse_strength"] = float(ac[max(1, li - 2) : li + 3].max()) if 2 < li < len(ac) - 3 else 0.0
    ibi = np.diff(bt)
    r["grid_offset_norm"] = None
    if len(bt) > 3 and len(on_t):
        grid = np.concatenate([np.linspace(bt[i], bt[i + 1], 5)[:-1] for i in range(len(bt) - 1)] + [[bt[-1]]])
        inside = on_t[(on_t >= bt[0]) & (on_t <= bt[-1])]
        if inside.size:
            idx = np.clip(np.searchsorted(grid, inside), 1, len(grid) - 1)
            off = np.minimum(np.abs(inside - grid[idx - 1]), np.abs(grid[idx] - inside))
            r["grid_offset_ms_median"] = float(np.median(off) * 1000)
            r["grid_offset_norm"] = float(np.median(off) / (np.median(ibi) / 4))
            r["onsets_on_grid_share"] = float(np.mean(off < 0.025))

    # Near silence (40 dB under the loud level, 100 ms+) and dips (20 dB under, 150 ms+), 50 ms frames.
    fr = int(0.05 * SR)
    nfr = len(mono) // fr
    rms_db = 20 * np.log10(np.sqrt(np.mean(mono[: nfr * fr].reshape(nfr, fr) ** 2, axis=1)) + 1e-9)
    ref = np.percentile(rms_db, 95)

    def runs(mask, min_len):
        out, i = [], 0
        while i < len(mask):
            if mask[i]:
                j = i
                while j < len(mask) and mask[j]:
                    j += 1
                if (j - i) * 0.05 >= min_len:
                    out.append((i * 0.05, (j - i) * 0.05))
                i = j
            else:
                i += 1
        return out

    def describe(rs):
        res = []
        for s, ln in [(s, ln) for s, ln in rs if s > 0.2 and s + ln < dur - 0.2]:
            before = rms_db[max(0, int((s - 1) / 0.05)) : int(s / 0.05)]
            after = rms_db[int((s + ln) / 0.05) : int((s + ln + 1) / 0.05)]
            nxt = on_t[on_t >= s + ln - 0.03]
            res.append({"start_s": round(s, 2), "len_s": round(ln, 2), "pos_pct": round(100 * s / dur, 1),
                        "rise_db": round(float(np.mean(after) - np.mean(before)), 1) if before.size and after.size else None,
                        "next_onset_delay_ms": round(float((nxt[0] - s - ln) * 1000)) if nxt.size else None})
        return res

    r["silences"] = describe(runs(rms_db < ref - 40, 0.1))
    r["dips"] = describe(runs(rms_db < ref - 20, 0.15))
    r["dips_per_10s"] = 10 * len(r["dips"]) / dur
    r["head_silence_s"] = float(np.argmax(rms_db > ref - 40) * 0.05)

    if patches:  # the 93 ms log mel shape after every strong onset (percussive part): "the same sound"
        yp = librosa.istft(Pp * np.exp(1j * np.angle(librosa.stft(y, n_fft=2048, hop_length=512))), hop_length=512, length=len(y))
        M = librosa.power_to_db(librosa.feature.melspectrogram(y=yp, sr=SR_A, n_fft=1024, hop_length=HOP, n_mels=48), ref=1.0)
        strong = on_f[strengths >= np.median(strengths)] if len(on_f) else on_f
        feats = []
        for f0 in strong[:600]:
            patch = M[:, f0 : f0 + 8]
            if patch.shape[1] < 8 or patch.max() < -60:
                continue
            v = patch.flatten() - patch.mean()
            feats.append(v / (np.linalg.norm(v) + 1e-9))
        r["_patches"] = np.array(feats, np.float32)
        if len(feats) >= 3:
            lab = fcluster(linkage(np.array(feats), "average", metric="correlation"), CLUSTER_T, "distance")
            _, c = np.unique(lab, return_counts=True)
            r["sound_types"] = int(np.sum(c >= max(2, 0.02 * len(feats))))
    r["_oenv"] = oenv
    return r


def shared_transients(pa, pb) -> float:
    """Share of strong onsets in A whose best match in B correlates above 0.9, averaged both ways."""
    if len(pa) == 0 or len(pb) == 0:
        return 0.0
    return float((np.mean((pa @ pb.T).max(axis=1) > 0.9) + np.mean((pb @ pa.T).max(axis=1) > 0.9)) / 2)


def profile_vector(r: dict, stats: dict) -> np.ndarray:
    """The 10 trait profile, standardized with the study's means and spreads (crossfilm.py)."""
    x = np.array([np.nan if r.get(k) is None else r[k] for k in PROFILE], float)
    mu, sd = np.array(stats["profile"]["mean"]), np.array(stats["profile"]["std"])
    return np.nan_to_num((x - mu) / sd)


def cut_rise(oenv, cuts, w=0.4):
    """How hard the sound hits at picture cuts: the onset envelope (divided by its median) averaged
    over a window around every cut; the peak within 70 ms over the baseline beyond 250 ms (cutsync.py)."""
    o = oenv / (np.median(oenv[oenv > 0]) + 1e-9) if (oenv > 0).any() else oenv
    fr = SR_A / HOP
    lags = np.arange(-int(w * fr), int(w * fr) + 1) / fr * 1000
    ws = []
    for c in cuts:
        i = int(round(c * fr))
        a, b = i - int(w * fr), i + int(w * fr) + 1
        if c > 0.5 and a >= 0 and b <= len(o):
            ws.append(o[a:b])
    if not ws:
        return None
    m = np.mean(ws, axis=0)
    pk = int(np.argmax(np.where(np.abs(lags) <= 70, m, -np.inf)))
    base = np.median(m[np.abs(lags) >= 250])
    return {"cuts": len(ws), "rise": float(m[pk] / (base + 1e-9)), "lag_ms": float(lags[pk])}


def video_cuts(path) -> list[float]:
    """Hard cuts in a rendered video (ffmpeg scene score above 0.3), as analyze.py found them."""
    import re
    import subprocess

    out = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(path), "-an", "-vf", "select='gt(scene,0.3)',showinfo",
                          "-f", "null", "-"], capture_output=True, text=True).stderr
    return [float(m) for m in re.findall(r"pts_time:([0-9.]+)", out)]
