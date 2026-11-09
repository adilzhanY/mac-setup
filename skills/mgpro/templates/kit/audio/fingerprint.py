"""
How alike are two soundtracks, and does a new one sit where professional films sit?

Similarity against the registry (what a listener hears as "the same song again"):

  groove     where the hits fall in the bar: onset strength per 16th, in three bands
  tempo      beats per minute
  harmony    the average pitch class profile (key and chord colour)
  timbre     the average energy in 40 mel bands (which registers the palette fills)
  shape      the loudness contour over the film (where the drops, gaps and stops sit)

Cross film checks (from 129 measured professional films, filmstats.py and pro_stats.json):

  profile distance   the 10 trait profile (tempo, density, percussive share, low end, LRA, peak
                     position, grid offset, width, dips, density variation), standardized; must be at
                     least the professional 10th percentile from EVERY registry film
  shared transients  share of strong onsets that are the same sound as in a registry film (max 10 %)
  centroid, rolloff  brightness against the professional range (the AI films were too bright)
  LRA                loudness range in LU
  opening            the first second against the integrated loudness (pros open quieter)
  cut rise           (with --cues or --video) onset strength at the cuts over the baseline

    python audio/fingerprint.py public/film.wav --bpm 104 --name sendoku
    python audio/fingerprint.py public/film.wav --bpm 104 --against ~/.claude/skills/mgpro/music/registry.json \
        --cues src/cues.json --music src/music.json
    python audio/fingerprint.py public/film.wav --checks            # the pro range checks alone, no registry
    python audio/fingerprint.py --build-stats ~/dev/mgpro-research/films   # rebuild pro_stats.json

Exits 1 when the score is too close to an earlier film or fails a check. Needs librosa.
"""

import argparse
import hashlib
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import filmstats  # noqa: E402

# A new score must stay under these against every earlier film (cosine similarity, 0 to 1).
LIMITS = {"groove": 0.85, "harmony": 0.97, "timbre": 0.70, "shape": 0.70}
# And differ in tempo by at least this many BPM, unless the groove is clearly different.
MIN_BPM_GAP = 6
MAX_SHARED = 0.10  # rule 2 of real_films_measured.md: professional median 5 %, torq and Sendoku 42 %
CACHE = Path.home() / ".cache" / "mgpro" / "filmstats"


def features(path, bpm, sr=22050):
    import librosa

    y, sr = librosa.load(path, sr=sr, mono=True)
    if bpm is None:
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        bpm = float(np.atleast_1d(tempo)[0])
    hop = 256
    S = np.abs(librosa.stft(y, n_fft=2048, hop_length=hop))
    freqs = librosa.fft_frequencies(sr=sr, n_fft=2048)

    def band_flux(lo, hi):
        b = S[(freqs >= lo) & (freqs < hi)]
        flux = np.maximum(0, np.diff(np.log1p(b), axis=1)).sum(0)
        return np.concatenate([[0], flux])

    t = np.arange(S.shape[1]) * hop / sr
    sixteenth = 60 / bpm / 4
    pos = np.floor(t / sixteenth + 0.5).astype(int) % 16
    groove = []
    for lo, hi in [(20, 150), (150, 4000), (6000, 11000)]:
        flux = band_flux(lo, hi)
        prof = np.array([flux[pos == k].mean() if np.any(pos == k) else 0 for k in range(16)])
        prof = prof - prof.mean()
        groove.append(prof / (np.linalg.norm(prof) + 1e-9))
    chroma = librosa.feature.chroma_stft(S=S**2, sr=sr).mean(1)
    # Timbre as the average log energy in 40 mel bands, centred: which registers the palette fills.
    mel = np.log(librosa.feature.melspectrogram(S=S**2, sr=sr, n_mels=40).mean(1) + 1e-9)
    # Every mastered mix tilts down to the treble; remove the tilt so the shape of the palette shows.
    k = np.arange(len(mel))
    mel = mel - np.polyval(np.polyfit(k, mel, 2), k)
    rms = librosa.feature.rms(S=S)[0]
    shape = np.interp(np.linspace(0, len(rms) - 1, 120), np.arange(len(rms)), rms)
    return {
        "bpm": round(bpm, 2),
        "groove": np.concatenate(groove).round(4).tolist(),
        "harmony": (chroma / chroma.sum()).round(4).tolist(),
        "timbre": mel.round(3).tolist(),
        "shape": (shape / (shape.max() + 1e-9)).round(4).tolist(),
        "centroid": float(np.mean(librosa.feature.spectral_centroid(S=S, sr=sr))),
    }


def cos(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-9))


def centred_cos(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    return cos(a - a.mean(), b - b.mean())


def compare(x, y):
    return {
        "groove": cos(x["groove"], y["groove"]),
        "harmony": cos(x["harmony"], y["harmony"]),
        "timbre": cos(x["timbre"], y["timbre"]),
        "shape": centred_cos(x["shape"], y["shape"]),
        "bpm_gap": abs(x["bpm"] - y["bpm"]),
    }


# --- Cross film measurements -------------------------------------------------------------------


def measured(wav) -> dict:
    """filmstats.analyze for a wav, cached by path, size and time so registry films are measured once."""
    p = Path(wav).expanduser().resolve()
    st = p.stat()
    h = hashlib.sha1(f"{p}:{st.st_size}:{st.st_mtime_ns}".encode()).hexdigest()[:16]
    j, n = CACHE / f"{h}.json", CACHE / f"{h}.npz"
    if j.exists() and n.exists():
        r = json.loads(j.read_text())
        z = np.load(n)
        r["_patches"], r["_oenv"] = z["patches"], z["oenv"]
        return r
    r = filmstats.analyze(str(p))
    CACHE.mkdir(parents=True, exist_ok=True)
    np.savez(n, patches=r["_patches"], oenv=r["_oenv"])
    j.write_text(json.dumps({k: v for k, v in r.items() if not k.startswith("_")}))
    return r


def cut_times(a, music_len=None) -> tuple[list[float], str]:
    """Cut times in seconds: from a rendered video, or from cues.json (cues marked "cut": true, else the
    hero cues, else the starts of the form's sections when music.json is given)."""
    if a.video:
        return filmstats.video_cuts(a.video), f"scene cuts in {Path(a.video).name}"
    if not a.cues:
        return [], ""
    cues = json.loads(Path(a.cues).read_text())
    cut = [c["frame"] / 60 for c in cues if c.get("cut")]
    if cut:
        return cut, "cues marked cut"
    if a.music:
        brief = json.loads(Path(a.music).read_text())
        spb = 60 / brief["bpm"] * brief.get("beats_per_bar", 4)
        starts, t = [], 0.0
        for s in brief["form"]:
            starts.append(t)
            t += s["bars"] * spb
        return starts[1:], "section starts in music.json"
    hero = [c["frame"] / 60 for c in cues if c.get("weight") == "hero"]
    return (hero, "hero cues") if hero else ([c["frame"] / 60 for c in cues], "every cue")


def row(name, value, fmt, rng, ok):
    print(f"  {name:28s} {fmt.format(value) if value is not None else 'n/a':>12s}   {rng:44s} {'pass' if ok else 'FAIL'}")
    return ok


def checks(a, r, pro, reg_films) -> bool:
    """Print pass or fail per check with the professional range next to it. True when all pass."""
    ok = True
    q = pro["metrics"]
    print("\nCross film checks (value, then the professional range it is held to)")
    print(f"  {'check':28s} {'value':>12s}   {'professional range':44s} result")
    if reg_films:
        v = filmstats.profile_vector(r, pro)
        lim = pro["crossfilm"]["distance_p10"]
        for e, er in reg_films:
            d = float(np.linalg.norm(v - filmstats.profile_vector(er, pro)))
            ok &= row(f"profile distance to {e['film'][:9]}", d, "{:.2f}", f">= {lim:.2f} (pro p10; median {pro['crossfilm']['distance_median']:.2f})", d >= lim)
        for e, er in reg_films:
            s = filmstats.shared_transients(r["_patches"], er["_patches"])
            ok &= row(f"shared transients {e['film'][:10]}", 100 * s, "{:.1f} %", f"<= {100 * MAX_SHARED:.0f} % (pro median {100 * pro['crossfilm']['shared_median']:.1f} %)", s <= MAX_SHARED)
    c, ro, lra = r["centroid_median_hz"], r["rolloff_median_hz"], r["loudness_range_lu"]
    ok &= row("spectral centroid", c, "{:.0f} Hz", f"{q['centroid_median_hz']['p10']:.0f} to {q['centroid_median_hz']['p90']:.0f} Hz (median {q['centroid_median_hz']['median']:.0f})",
              q["centroid_median_hz"]["p10"] <= c <= q["centroid_median_hz"]["p90"])
    ok &= row("85 % rolloff", ro, "{:.0f} Hz", f"{q['rolloff_median_hz']['p10']:.0f} to {q['rolloff_median_hz']['p90']:.0f} Hz (median {q['rolloff_median_hz']['median']:.0f})",
              q["rolloff_median_hz"]["p10"] <= ro <= q["rolloff_median_hz"]["p90"])
    ok &= row("loudness range (LRA)", lra, "{:.1f} LU", f"5 to {q['loudness_range_lu']['p90']:.1f} LU (median {q['loudness_range_lu']['median']:.1f})",
              5.0 <= lra <= q["loudness_range_lu"]["p90"])
    op = r["opening_lu"]
    ok &= row("opening second vs whole", op, "{:+.1f} LU", ("cold open allowed" if a.cold_open else f"<= -1.0 LU (median {q['opening_lu']['median']:+.1f}, p10 {q['opening_lu']['p10']:+.1f})"),
              a.cold_open or op <= -1.0)
    cuts, how = cut_times(a)
    if cuts:
        cr = filmstats.cut_rise(r["_oenv"], cuts)
        if cr:
            cp = pro["cutsync"]
            ok &= row(f"rise at {cr['cuts']} cuts", cr["rise"], "{:.2f} x", f"<= {cp['p90']:.2f} x (median {cp['median']:.2f}, AI films 18.6)", cr["rise"] <= cp["p90"])
            print(f"  {'':28s} cuts from {how}; peak {cr['lag_ms']:+.0f} ms after the cut")
            if a.cues:  # hero cuts may slam; the ordinary ones are what the professional median is about
                cues = json.loads(Path(a.cues).read_text())
                hero = [c["frame"] / 60 for c in cues if c.get("weight") == "hero"]
                ordinary = [t for t in cuts if all(abs(t - h) > 0.05 for h in hero)]
                for label, ts in (("hero", [t for t in cuts if t not in ordinary]), ("ordinary", ordinary)):
                    x = filmstats.cut_rise(r["_oenv"], ts) if ts else None
                    if x:
                        print(f"  {'':28s} {label} cuts: {x['cuts']}, rise {x['rise']:.2f} x")
            bars = filmstats.cut_rise(r["_oenv"], list(np.arange(2.0, r["duration_s"] - 1, 60 / (a.bpm or r["tempo_bpm"]) * 4)))
            if bars:
                print(f"  {'':28s} for scale: every bar downbeat of this music measures {bars['rise']:.2f} x with no cut at all")
    print("  informational:")
    for k, label, fmt in (("grid_offset_norm", "grid offset (share of a 16th)", "{:.3f}"), ("onsets_on_grid_share", "onsets within 25 ms of grid", "{:.2f}"),
                          ("dips_per_10s", "dips per 10 s", "{:.2f}"), ("pulse_strength", "pulse strength", "{:.2f}"),
                          ("onset_density_per_s", "onsets per second", "{:.2f}"), ("percussive_share", "percussive share", "{:.2f}"),
                          ("stereo_side_share", "stereo side share", "{:.3f}"), ("tempo_bpm", "tempo (tracked)", "{:.1f}")):
        p = q.get(k)
        rng = f"{p['p10']:.3g} / {p['median']:.3g} / {p['p90']:.3g} (pro p10 / median / p90)" if p else ""
        print(f"  {label:28s} {fmt.format(r[k]) if r.get(k) is not None else 'n/a':>12s}   {rng}")
    dips = [f"{d['pos_pct']:.0f}% {d['len_s']:.2f}s {d['rise_db'] if d['rise_db'] is not None else 0:+.0f}dB {d['next_onset_delay_ms']}ms" for d in r["dips"]]
    print(f"  dips (position, length, rise after, first onset after): {', '.join(dips) or 'none'}")
    print(f"  2 s density: {' '.join(f'{v:g}' for v in r['onset_density_2s'])}")
    return ok


def build_stats(films: Path) -> None:
    """Write pro_stats.json from the research folder (summary.csv, distributions.json, json/*, crossfilm.json, cutsync.json)."""
    import csv

    rows = list(csv.DictReader((films / "summary.csv").open()))
    X = np.array([[float(r[k]) if r[k] not in ("", "None") else np.nan for k in filmstats.PROFILE] for r in rows])
    dist = json.loads((films / "distributions.json").read_text())
    metrics = {k: {q: v[q] for q in ("p10", "median", "p90")} for k, v in dist.items()}
    metrics["pulse_strength"] = metrics["tempo_confidence"]
    op = []
    for p in (films / "json").glob("*.json"):
        j = json.loads(p.read_text())
        if j.get("label") == "pro" and j.get("loudness_curve_1s"):
            op.append(j["loudness_curve_1s"][0] - j["lufs_integrated"])
    metrics["opening_lu"] = {q: float(np.percentile(op, n)) for q, n in (("p10", 10), ("median", 50), ("p90", 90))}
    cf = json.loads((films / "crossfilm.json").read_text())["pro, different makers"]
    cs = json.loads((films / "cutsync.json").read_text())["summary"]["pro"]["film_peak_over_base"]
    out = {"source": str(films), "n_pro": sum(r["label"] == "pro" for r in rows),
           "profile": {"keys": filmstats.PROFILE, "mean": np.nanmean(X, 0).tolist(), "std": (np.nanstd(X, 0) + 1e-9).tolist()},
           "crossfilm": {"distance_p10": cf["profile_distance"]["p10"], "distance_median": cf["profile_distance"]["median"],
                         "shared_median": cf["shared_sounds"]["median"], "shared_p90": cf["shared_sounds"]["p90"]},
           "cutsync": cs, "metrics": metrics}
    filmstats.PRO.write_text(json.dumps(out, indent=1))
    print(f"wrote {filmstats.PRO} from {len(rows)} films")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("wav", nargs="?")
    ap.add_argument("--bpm", type=float, help="the score's tempo; detected when left out")
    ap.add_argument("--name", help="print this film's fingerprint as a registry entry")
    ap.add_argument("--against", help="registry.json of earlier films")
    ap.add_argument("--checks", action="store_true", help="run the professional range checks (implied by --against)")
    ap.add_argument("--cues", help="cues.json, for the rise at cuts")
    ap.add_argument("--music", help="music.json, cuts fall back to its section starts")
    ap.add_argument("--video", help="a rendered film: its scene cuts are the cuts")
    ap.add_argument("--cold-open", action="store_true", help="the brief asks for a cold open: skip the opening check")
    ap.add_argument("--build-stats", type=Path, help="rebuild pro_stats.json from the research films folder")
    a = ap.parse_args()
    if a.build_stats:
        build_stats(a.build_stats.expanduser())
        return
    fp = features(a.wav, a.bpm)
    if a.name:
        print(json.dumps({"film": a.name, "wav": str(Path(a.wav).resolve()), **fp}))
    if not a.against and not a.checks:
        return
    worst = []
    reg_films = []
    if a.against:
        reg = json.loads(Path(a.against).expanduser().read_text())
        print(f"{'film':16} {'groove':>7} {'harmony':>8} {'timbre':>7} {'shape':>6} {'bpm gap':>8}")
        for e in reg["films"]:
            if "groove" not in e or Path(e.get("wav", "")).resolve() == Path(a.wav).resolve():
                continue
            c = compare(fp, e)
            flags = [k for k, lim in LIMITS.items() if c[k] > lim]
            if c["bpm_gap"] < MIN_BPM_GAP and c["groove"] > 0.6:
                flags.append("tempo")
            print(f"{e['film']:16} {c['groove']:7.2f} {c['harmony']:8.2f} {c['timbre']:7.2f} {c['shape']:6.2f} {c['bpm_gap']:8.1f}  {' '.join('TOO CLOSE: ' + f for f in flags)}")
            worst += flags
            if Path(e.get("wav", "")).exists():
                reg_films.append((e, measured(e["wav"])))
            else:
                print(f"  {e['film']}: {e.get('wav')} is missing, so it is left out of the cross film checks")
    r = filmstats.analyze(a.wav)
    passed = checks(a, r, filmstats.pro_stats(), reg_films)
    if worst:
        print("\nThe new score repeats an earlier film. Change the groove, tempo, palette or form (see references/music.md).")
    if not passed:
        print("\nA cross film check failed: see the rows marked FAIL and the professional range beside them.")
    if worst or not passed:
        sys.exit(1)
    print("\nDistinct from every earlier film, and inside the professional ranges.")


if __name__ == "__main__":
    main()
