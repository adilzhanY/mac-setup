"""
No event plays the same way twice. A real sound designer reaches for one of 3 to 6 takes, and the
take is never exactly the same; the first AI films fired one identical waveform per event, and
across films the same transients (torq and Sendoku shared 42 percent of them).

    v = Vary(film_seed)
    s = v.play("tap", lambda seed: sfx.tap("wood", seed=seed), kind="noisy")

Per film and deterministic (the same seed renders the same film):

  pool       each effect name gets `pool` takes (each a different synthesis seed, so different
             noise, partial phases and layer choices). Takes come from a shuffled bag, and a take
             never plays twice in a row.
  pitch      a jitter in cents per kind of sound: tonal sounds stay in key (plus or minus 12 cents),
             noisy ones move further (120), impacts and whooshes in between. Applied like a sampler
             (dsp.repitch), so a lower take is also a little longer.
  level      plus or minus 1.5 dB.
  offset     a small start offset, only for sounds that do not carry a picture sync point (texture,
             ambient cues). Picture synced hits stay frame exact.
  film seed  the takes are built from the film's seed, so two films never share a transient.

Music onsets are humanised in score.py (grooves.hits) with a 10 to 15 ms spread and velocity
variation; Vary is for effects and samples.
"""

from __future__ import annotations

import zlib
from itertools import pairwise

import numpy as np

import dsp

# Pitch jitter (plus or minus, in cents) per kind. Tonal UI sounds go audibly out of key past about
# 25 to 50 cents; noise tolerates 100 to 200 (ai_patterns_and_humanization.md, section 2).
CENTS = {"tonal": 12, "noisy": 120, "impact": 60, "whoosh": 150, "bell": 6, "sample": 100}
LEVEL_DB = 1.5


class Vary:
    def __init__(self, seed: int, pool: int = 4):
        self.seed = int(seed)
        self.pool = pool
        self.rng = np.random.default_rng(self.seed + 7919)
        self.bags: dict[str, list[int]] = {}
        self.last: dict[str, int] = {}
        self.cache: dict[tuple, np.ndarray] = {}

    def take(self, name: str, pool: int | None = None) -> int:
        """The next take of an effect: from a shuffled bag, never the take that just played."""
        k = pool or self.pool
        bag = self.bags.get(name) or []
        if not bag:
            bag = list(self.rng.permutation(k))
            if len(bag) > 1 and bag[-1] == self.last.get(name):
                bag[0], bag[-1] = bag[-1], bag[0]
        t = int(bag.pop())
        self.bags[name] = bag
        self.last[name] = t
        return t

    def take_seed(self, name: str, take: int) -> int:
        """A synthesis seed for a take, built from the film seed and the effect's name."""
        return (zlib.crc32(f"{self.seed}:{name}:{take}".encode()) & 0x7FFFFFFF) or 1

    def cents(self, kind: str) -> float:
        c = CENTS.get(kind, 40)
        return float(self.rng.uniform(-c, c))

    def gain(self) -> float:
        return float(10 ** (self.rng.uniform(-LEVEL_DB, LEVEL_DB) / 20))

    def offset(self, loose: bool, ms: float = 8.0) -> float:
        """Seconds to move a sound's start: 0 for picture synced hits, late leaning for loose ones
        (early deviations read worse than late ones)."""
        return float(self.rng.uniform(-0.25, 1.0) * ms / 1000) if loose else 0.0

    def play(self, name: str, make, kind: str = "noisy", key=None, pool: int | None = None) -> np.ndarray:
        """One event of an effect: a take from the pool (synthesised once per take and cached), then
        pitch and level jitter. make(seed) builds a take. key separates variants with different
        arguments (a note index, a length)."""
        t = self.take(f"{name}:{key}", pool)
        ck = (name, key, t)
        if ck not in self.cache:
            self.cache[ck] = np.asarray(make(self.take_seed(f"{name}:{key}", t)), float)
        x = dsp.repitch(self.cache[ck], self.cents(kind))
        return x * self.gain()


def _selftest():
    v = Vary(5, pool=4)
    seq = [v.take("tap") for _ in range(40)]
    assert all(a != b for a, b in pairwise(seq)), "a take repeated"
    assert set(seq) == {0, 1, 2, 3}
    a = v.play("x", lambda s: np.random.default_rng(s).standard_normal(480), "noisy")
    b = v.play("x", lambda s: np.random.default_rng(s).standard_normal(480), "noisy")
    assert not (len(a) == len(b) and np.allclose(a, b)), "two events identical"
    assert Vary(5).take_seed("tap", 0) != Vary(6).take_seed("tap", 0), "two films share a take"
    print("vary self test passed")


if __name__ == "__main__":
    _selftest()
