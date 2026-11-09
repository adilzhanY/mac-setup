"""
Real sounds from the CC0 library (~/.local/share/mgpro/sfx, 1126 files, measured in
sfx/catalog.json), mixed with the synthesis when a film allows samples. Off by default; a film
turns it on in music.json:

    "samples": {"enabled": true, "jobs": ["card", "logo"], "layer": ["impact"]}

jobs     effect jobs played from a sample instead of the synth ("all" for every job with a family)
layer    jobs where a sample sits under the synth (at -6 dB) instead of replacing it

    s = Samples(film_seed, film_root, vary)
    x = s.play("card")                 # a take from the job's family, varied like any effect
    s.write_assets()                   # public/sfx/ASSETS.txt: file, pack, source page, CC0

Every file used is copied into the film (public/sfx/) and read from there, so the film builds on
another machine. Each job has a family of 2 to 5 files (the picks of sfx/ANALYSIS.md section 3);
takes rotate with no immediate repeat and get the same pitch (plus or minus 100 cents), level and
lead trim variation as synthesized effects. A job with no named family falls back to the 3
library sounds nearest to its feature target in its category.
"""

from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

import numpy as np

from dsp import SR, fade
from vary import Vary

LIB = Path.home() / ".local/share/mgpro/sfx"
# The kit is copied into each film, so look beside this file first, then at the installed skill.
SKILL = next((p for p in (Path(__file__).resolve().parents[3], Path.home() / ".claude/skills/mgpro") if (p / "sfx" / "catalog.json").exists()),
             Path.home() / ".claude/skills/mgpro")
CATALOG = SKILL / "sfx" / "catalog.json"

# job: (path pattern of the named family, category, feature target for the fallback)
JOBS = {
    "tap": (r"kenney-ui-audio/Audio/click[45]\.|kenney-interface-sounds/Audio/click_00[23]\.", "click/tap", {"decay20_ms": 10, "centroid_hz": 3000}),
    "click": (r"kenney-ui-audio/Audio/click[45]\.|kenney-interface-sounds/Audio/click_00[23]\.", "click/tap", {"decay20_ms": 10, "centroid_hz": 3000}),
    "blip": (r"kenney-interface-sounds/Audio/select_00[1-3]\.", "click/tap", {"decay20_ms": 20, "centroid_hz": 2000}),
    "toggle": (r"kenney-interface-sounds/Audio/toggle_00[1-4]\.|kenney-ui-audio/Audio/switch2\.", "click/tap", {"decay20_ms": 60, "centroid_hz": 2000}),
    "text": (r"kenney-ui-audio/Audio/rollover[25]\.|kenney-interface-sounds/Audio/select_002\.|kenney-interface-sounds/Audio/glass_00[26]\.", "click/tap", {"decay20_ms": 17, "centroid_hz": 1400}),
    "tick": (r"kenney-interface-sounds/Audio/tick_00[12]\.|kenney-interface-sounds/Audio/scroll_00[45]\.", "click/tap", {"decay20_ms": 6, "centroid_hz": 6000}),
    "pop": (r"kenney-interface-sounds/Audio/drop_00[234]\.|oga-pop-effects/.*p_1\.", "pop", {"decay20_ms": 25, "centroid_hz": 850}),
    "card": (r"kenney-impact-sounds/Audio/impactWood_light_00[0-2]\.|kenney-impact-sounds/Audio/impactSoft_medium_00[0-4]\.", "impact/thud", {"decay20_ms": 20, "centroid_hz": 300}),
    "chip": (r"kenney-impact-sounds/Audio/impactGlass_light_00[0-2]\.|kenney-impact-sounds/Audio/impactMetal_light_00[0-2]\.", "impact/thud", {"decay20_ms": 60, "centroid_hz": 1500}),
    "impact": (r"kenney-impact-sounds/Audio/impactPunch_heavy_00[0-4]\.|kenney-impact-sounds/Audio/impactPlate_heavy_00[0-4]\.", "impact/thud", {"decay20_ms": 45, "centroid_hz": 250}),
    "swish": (r"oga-swishes/swishes/swish-1[0-3]\.|remotion-cc0/whip\.|remotion-cc0/whoosh\.", "whoosh/swish", {"decay20_ms": 20, "centroid_hz": 400}),
    "whoosh": (r"oga-time-hit-wind/qubodup-megaswosh[12]\.", "whoosh/swish", {"decay20_ms": 40, "centroid_hz": 430}),
    "airy": (r"oga-scifi-50/misc_(09|10|11)\.", "whoosh/swish", {"decay20_ms": 350, "centroid_hz": 6500}),
    "panel_open": (r"kenney-interface-sounds/Audio/open_00[2-4]\.", "riser", {"decay20_ms": 2, "centroid_hz": 9000}),
    "panel_close": (r"kenney-interface-sounds/Audio/close_00[2-4]\.", "whoosh/swish", {"decay20_ms": 250, "centroid_hz": 9000}),
    "success": (r"kenney-interface-sounds/Audio/confirmation_00[1-4]\.", "tonal/bell", {"decay20_ms": 240, "centroid_hz": 1800}),
    "error": (r"kenney-interface-sounds/Audio/error_00[367]\.", "glitch/digital", {"decay20_ms": 60, "centroid_hz": 600}),
    "logo": (r"oga-metal-dings/ding\.[23]\.|oga-bell-dings/bell_ding3\.", "tonal/bell", {"decay20_ms": 250, "centroid_hz": 1500}),
    "tier": (r"kenney-impact-sounds/Audio/impactBell_heavy_00[0-4]\.", "impact/thud", {"decay20_ms": 150, "centroid_hz": 1200}),
}


def catalog() -> list[dict]:
    return json.loads(CATALOG.read_text())["sounds"]


def sources() -> dict[str, str]:
    """Pack folder to its source page, from the licence table in sfx/README.md."""
    out = {}
    for line in (SKILL / "sfx" / "README.md").read_text().splitlines():
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) == 5 and cells[3].startswith("http"):
            out[cells[0]] = cells[3]
    return out


def family(job: str, rows: list[dict] | None = None, k: int = 3) -> list[dict]:
    """The files a job draws from: its named family, else the k nearest by features in its category.
    Files with clipped samples, more than 150 ms of lead silence or no measured length are skipped."""
    rows = rows if rows is not None else catalog()
    pat, cat, target = JOBS[job]
    usable = [r for r in rows if "length_ms" in r and not r.get("clipped") and r.get("lead_ms", 0) <= 150]
    named = [r for r in usable if re.search(pat, r["path"])]
    if named:
        return sorted(named, key=lambda r: r["path"])
    pool = [r for r in usable if r.get("category") == cat]
    dist = [sum(abs(np.log((r[f] + 1) / (v + 1))) for f, v in target.items()) for r in pool]
    return [pool[i] for i in np.argsort(dist)[:k]]


class Samples:
    def __init__(self, seed: int, film_root: Path, vary: Vary | None = None, jobs="all", layer=()):
        self.root = Path(film_root)
        self.dir = self.root / "public" / "sfx"
        self.vary = vary or Vary(seed)
        self.jobs = set(JOBS) if jobs == "all" else set(jobs)
        self.layer = set(layer)
        self.rows = catalog()
        self.used: dict[str, dict] = {}
        self.audio: dict[str, np.ndarray] = {}

    def wants(self, job: str) -> bool:
        return job in JOBS and (job in self.jobs or job in self.layer)

    def local(self, row: dict) -> Path:
        """Copy a library file into the film once and return the film's copy."""
        name = row["path"].replace("/", "__").replace(" ", "_")
        dst = self.dir / name
        if not dst.exists():
            src = LIB / row["path"]
            if not src.exists():
                raise FileNotFoundError(f"{src} is missing: run templates/kit/audio/fetch_sfx.sh")
            self.dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
        self.used[name] = row
        return dst

    def load(self, row: dict) -> np.ndarray:
        """A file as 48 kHz stereo, its lead silence trimmed so it lands on its frame."""
        import soundfile as sf
        from scipy.signal import resample_poly

        p = self.local(row)
        if str(p) not in self.audio:
            x, sr = sf.read(str(p), always_2d=True)
            x = x[int(row.get("lead_ms", 0) * sr / 1000) :].T
            if sr != SR:
                x = resample_poly(x, SR, sr, axis=1)
            x = x[:2] if x.shape[0] >= 2 else np.repeat(x, 2, axis=0)
            x = x * (10 ** (-1.5 / 20) if row.get("clipped") else 1.0)
            self.audio[str(p)] = fade(x / (np.abs(x).max() + 1e-12), 1)
        return self.audio[str(p)]

    def play(self, job: str) -> np.ndarray:
        """One event of a job from its family, varied: the take rotates with no immediate repeat,
        then pitch, level and a 0 to 4 ms trim into the attack."""
        fam = family(job, self.rows)
        x = self.load(fam[self.vary.take(f"sample:{job}", len(fam))])
        trim = int(SR * self.vary.rng.uniform(0, 0.004))
        from dsp import repitch

        return repitch(x[:, trim:], self.vary.cents("sample")) * self.vary.gain()

    def write_assets(self) -> Path | None:
        """The film's asset list for every sample used (no on screen credit is required for CC0)."""
        if not self.used:
            return None
        src = sources()
        lines = ["file | pack | source page | licence"]
        for name, row in sorted(self.used.items()):
            lines.append(f"public/sfx/{name} | {row['pack']} | {src.get(row['pack'], 'see sfx/README.md')} | CC0 1.0")
        out = self.dir / "ASSETS.txt"
        out.write_text("\n".join(lines) + "\n")
        return out


if __name__ == "__main__":
    rows = catalog()
    for job in JOBS:
        fam = family(job, rows)
        print(f"{job:12s} {len(fam)} files: " + ", ".join(Path(r['path']).name for r in fam))
