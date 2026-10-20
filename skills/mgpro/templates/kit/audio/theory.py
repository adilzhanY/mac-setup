"""
Keys, modes, chords, progressions and motifs. Everything is MIDI note numbers.

    key = Key("F#", "dorian")
    key.chord("i", 7)            -> [54, 57, 61, 64]   the tonic seventh, root in octave 3
    key.progression("hopeful")   -> a list of roman numerals
    key.scale_notes(60, 84)      -> every scale note between C4 and C6
    motif(key, seed=3)           -> a hook: [(step in 16ths, length in 16ths, MIDI note), ...]
"""

from __future__ import annotations

import numpy as np

NAMES = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
         "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}

MODES = {  # semitones above the tonic, and the colour each one gives
    "ionian": [0, 2, 4, 5, 7, 9, 11],       # major: bright, plain, confident
    "lydian": [0, 2, 4, 6, 7, 9, 11],       # raised 4th: wonder, floating, futuristic optimism
    "mixolydian": [0, 2, 4, 5, 7, 9, 10],   # flat 7th: swagger, sunny groove, rock and funk
    "dorian": [0, 2, 3, 5, 7, 9, 10],       # minor with a raised 6th: cool, hopeful minor, jazzy
    "aeolian": [0, 2, 3, 5, 7, 8, 10],      # natural minor: serious, emotional, dark pop
    "phrygian": [0, 1, 3, 5, 7, 8, 10],     # flat 2nd: tense, exotic, aggressive (phonk, drill)
    "harmonic": [0, 2, 3, 5, 7, 8, 11],     # harmonic minor: dramatic, cinematic, a pull home
    "major_penta": [0, 2, 4, 7, 9],
    "minor_penta": [0, 3, 5, 7, 10],
    "blues": [0, 3, 5, 6, 7, 10],
    "hirajoshi": [0, 2, 3, 7, 8],           # Japanese pentatonic: sparse, precise, calm
    "whole": [0, 2, 4, 6, 8, 10],           # dreamlike, unresolved (use for a moment, not a score)
}

ROMAN = {"i": 0, "ii": 1, "iii": 2, "iv": 3, "v": 4, "vi": 5, "vii": 6}

# Progressions by what the film should feel like. Roman numerals are degrees of the film's own
# mode; case only labels the usual quality in that mode, the chord is built from the scale.
PROGRESSIONS = {
    "confident": [["I", "V", "vi", "IV"], ["I", "IV", "vi", "V"], ["I", "iii", "IV", "V"]],
    "hopeful": [["vi", "IV", "I", "V"], ["IV", "I", "V", "vi"], ["i", "VII", "IV", "i"]],
    "nostalgic": [["I", "vi", "IV", "V"], ["I", "iii", "vi", "IV"], ["IV", "iii", "ii", "I"]],
    "wonder": [["I", "II", "vii", "I"], ["I", "II", "V", "I"], ["IV", "V", "iii", "vi"]],
    "cool": [["i", "iv", "VII", "III"], ["i", "IV", "i", "IV"], ["ii", "V", "i", "i"]],
    "tense": [["i", "VI", "i", "VII"], ["i", "ii", "i", "ii"], ["i", "iv", "v", "i"]],
    "epic": [["i", "VI", "III", "VII"], ["vi", "IV", "I", "V"], ["i", "VII", "VI", "V"]],
    "playful": [["I", "IV", "I", "V"], ["I", "VII", "IV", "I"], ["ii", "V", "I", "vi"]],
    "dreamy": [["I", "iii", "IV", "iv"], ["IV", "I", "IV", "I"], ["I", "II", "IV", "I"]],
    "driving": [["i", "i", "VI", "VII"], ["i", "VII", "VI", "VII"], ["I", "V", "IV", "IV"]],
}


class Key:
    def __init__(self, tonic: str, mode: str = "aeolian", octave: int = 3):
        self.tonic = tonic
        self.mode = mode
        self.root = 12 * (octave + 1) + NAMES[tonic]
        self.steps = MODES[mode]

    def degree(self, d: int, octave_shift: int = 0) -> int:
        """The d-th scale degree (0 based, may run past the octave or below zero)."""
        k = len(self.steps)
        return self.root + 12 * (d // k + octave_shift) + self.steps[d % k]

    def scale_notes(self, lo: int, hi: int) -> list[int]:
        pcs = {(self.root + s) % 12 for s in self.steps}
        return [m for m in range(lo, hi + 1) if m % 12 in pcs]

    def chord(self, roman: str, size: int = 3, inversion: int = 0, octave_shift: int = 0, add: tuple = ()) -> list[int]:
        """Stacked thirds from the scale: size 3 a triad, 4 a seventh, 5 a ninth. add=(9,) adds a ninth,
        add=("sus2",) or ("sus4",) replaces the third. Degrees outside a 7 note mode fall back to ionian."""
        steps = self.steps if len(self.steps) == 7 else MODES["ionian"]
        base = roman.strip("°+").lower()
        acc = 0
        if base.startswith("b"):
            acc, base = -1, base[1:]
        d = ROMAN[base]
        notes = []
        for k in range(size):
            idx = d + 2 * k
            notes.append(self.root + 12 * (idx // 7 + octave_shift) + steps[idx % 7] + acc)
        if "sus2" in add:
            notes[1] = notes[0] + (steps[(d + 1) % 7] - steps[d % 7]) % 12
        if "sus4" in add:
            notes[1] = notes[0] + (steps[(d + 3) % 7] - steps[d % 7]) % 12
        if 9 in add and size < 5:
            notes.append(notes[0] + 12 + (steps[(d + 1) % 7] - steps[d % 7]) % 12)
        for _ in range(inversion):
            notes = notes[1:] + [notes[0] + 12]
        return notes

    def progression(self, mood: str, variant: int = 0) -> list[str]:
        return PROGRESSIONS[mood][variant % len(PROGRESSIONS[mood])]


def voice_lead(chords: list[list[int]], centre: int = 62) -> list[list[int]]:
    """Moves each chord to the inversion and octave nearest the previous one, so pads glide."""
    out = []
    prev = None
    for ch in chords:
        best, cost = None, 1e9
        for inv in range(len(ch)):
            v = ch[inv:] + [m + 12 for m in ch[:inv]]
            for o in (-24, -12, 0, 12):
                cand = [m + o for m in v]
                ref = prev if prev else [centre] * len(cand)
                c = sum(abs(a - b) for a, b in zip(sorted(cand), sorted(ref)))
                c += abs(np.mean(cand) - centre) * 0.5
                if c < cost:
                    best, cost = cand, c
        out.append(sorted(best))
        prev = best
    return out


def euclid(k: int, n: int, rotate: int = 0) -> list[int]:
    """Toussaint's Euclidean rhythm: k onsets spread as evenly as possible over n steps.
    E(3,8) is the tresillo, E(5,8) the cinquillo, E(5,16) a bossa feel, E(7,16) a samba bell."""
    pat = [1 if (i * k) % n < k else 0 for i in range(n)]
    return pat[-rotate % n :] + pat[: -rotate % n] if rotate else pat


CONTOURS = {  # the shape of a phrase over its notes, from 0 (low) to 1 (high)
    "arch": [0.2, 0.5, 0.8, 1.0, 0.7, 0.4],   # rise then fall: the commonest catchy shape
    "rise": [0.0, 0.25, 0.4, 0.6, 0.8, 1.0],  # ascending: lift, hope, a question
    "fall": [1.0, 0.8, 0.6, 0.45, 0.25, 0.1],  # descending: settling, an answer
    "valley": [0.8, 0.4, 0.1, 0.3, 0.6, 0.9],
    "wave": [0.3, 0.7, 0.4, 0.9, 0.5, 0.2],
    "pedal": [0.5, 0.5, 0.8, 0.5, 0.5, 0.9],   # repeated note with escapes: hypnotic, minimal
}


def motif(key: Key, seed: int, contour: str = "arch", notes: int = 6, span: int = 7, low: int = 64,
          rhythm: list[int] | None = None, leap: bool = True, bar_steps: int = 16) -> list[tuple[int, int, int]]:
    """Writes a hook: (step, length, MIDI note) inside one bar of 16ths.

    What makes a hook stick (Jakubowski et al. 2016): a common overall contour plus one unusual
    interval (a leap) or more repeated notes than usual. So: follow a contour mostly by step,
    then break it once with a leap of a 4th to a 6th, and end on a stable chord tone."""
    rng = np.random.default_rng(seed)
    scale = key.scale_notes(low, low + 24)
    if rhythm is None:
        rhythm = sorted(rng.choice(np.arange(bar_steps), size=notes, replace=False).tolist())
        rhythm[0] = rng.choice([0, 0, 2, 3])
        rhythm = sorted(set(rhythm))
    shape = np.interp(np.linspace(0, 1, len(rhythm)), np.linspace(0, 1, len(CONTOURS[contour])), CONTOURS[contour])
    idx = [int(round(s * span)) for s in shape]
    if leap and len(idx) > 3:
        j = int(rng.integers(1, len(idx) - 1))
        idx[j] = min(len(scale) - 1, idx[j - 1] + int(rng.choice([3, 4, 5])))
    stable = {(key.root + s) % 12 for s in (0, key.steps[min(2, len(key.steps) - 1)], 7)}
    out = []
    for i, (st, d) in enumerate(zip(rhythm, idx)):
        m = scale[min(max(d, 0), len(scale) - 1)]
        if i == len(rhythm) - 1:  # land on a chord tone
            while m % 12 not in stable:
                m -= 1
        nxt = rhythm[i + 1] if i + 1 < len(rhythm) else bar_steps
        out.append((st, max(1, min(4, nxt - st)), m))
    return out


def answer(call: list[tuple[int, int, int]], key: Key, shift: int = -2) -> list[tuple[int, int, int]]:
    """Call and response: the answer keeps the call's rhythm and opening, moves the end down
    the scale and resolves to the tonic, so the pair sounds like question and reply."""
    scale = key.scale_notes(min(m for *_, m in call) - 12, max(m for *_, m in call) + 12)
    out = []
    for i, (st, ln, m) in enumerate(call):
        if i >= len(call) // 2:
            j = scale.index(m) if m in scale else 0
            m = scale[max(0, j + shift)]
        out.append((st, ln, m))
    tonic = [m for m in scale if m % 12 == key.root % 12]
    last = out[-1]
    out[-1] = (last[0], last[1], min(tonic, key=lambda t: abs(t - last[2])))
    return out
