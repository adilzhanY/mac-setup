"""
How alike are two soundtracks? Measures what a listener hears as "the same song again":

  groove     where the hits fall in the bar: onset strength per 16th, in three bands
             (kick under 150 Hz, snare and body 150 Hz to 4 kHz, hats above 6 kHz)
  tempo      beats per minute
  harmony    the average pitch class profile (key and chord colour)
  timbre     the average energy in 40 mel bands (which registers the palette fills)
  shape      the loudness contour over the film (where the drops, gaps and stops sit)

    python audio/fingerprint.py public/film.wav --bpm 104 --name sendoku
    python audio/fingerprint.py public/film.wav --bpm 104 --against ~/.claude/skills/mgpro/music/registry.json

With --against it prints a similarity row per earlier film and exits 1 when the new score is
too close to one of them (see LIMITS). Needs librosa in the venv: pip install librosa.
"""

import argparse
import json
import sys
from pathlib import Path

import numpy as np

# A new score must stay under these against every earlier film (cosine similarity, 0 to 1).
LIMITS = {"groove": 0.85, "harmony": 0.97, "timbre": 0.70, "shape": 0.70}
# And differ in tempo by at least this many BPM, unless the groove is clearly different.
MIN_BPM_GAP = 6


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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("wav")
    ap.add_argument("--bpm", type=float, help="the score's tempo; detected when left out")
    ap.add_argument("--name", help="print this film's fingerprint as a registry entry")
    ap.add_argument("--against", help="registry.json of earlier films")
    a = ap.parse_args()
    fp = features(a.wav, a.bpm)
    if a.name:
        print(json.dumps({"film": a.name, "wav": str(Path(a.wav).resolve()), **fp}))
    if not a.against:
        return
    reg = json.loads(Path(a.against).expanduser().read_text())
    worst = []
    print(f"{'film':14} {'groove':>7} {'harmony':>8} {'timbre':>7} {'shape':>6} {'bpm gap':>8}")
    for e in reg["films"]:
        if "groove" not in e or Path(e.get("wav", "")).resolve() == Path(a.wav).resolve():
            continue
        c = compare(fp, e)
        flags = [k for k, lim in LIMITS.items() if c[k] > lim]
        if c["bpm_gap"] < MIN_BPM_GAP and c["groove"] > 0.6:
            flags.append("tempo")
        print(f"{e['film']:14} {c['groove']:7.2f} {c['harmony']:8.2f} {c['timbre']:7.2f} {c['shape']:6.2f} {c['bpm_gap']:8.1f}  {' '.join('TOO CLOSE: ' + f for f in flags)}")
        worst += flags
    if worst:
        print("\nThe new score repeats an earlier film. Change the groove, tempo, palette or form (see references/music.md).")
        sys.exit(1)
    print("\nDistinct from every earlier film.")


if __name__ == "__main__":
    main()
