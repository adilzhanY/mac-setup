"""
The groove library: genres as data. Each genre gives tempos that sit on whole frames at 60 fps,
a swing amount, drum patterns per part, how the bass and the chords move, a default palette and
the brands it fits. A score picks ONE genre per film (or two for a beat switch) and then makes it
its own: its own tempo from the list, its own key and mode, its own hook, at least one part
rewritten (a different kick pattern, an extra percussion line, a different bass rhythm).

Pattern strings, one character per step (16ths in 4/4, 8ths in 12/8):
    X accent   x hit   g ghost (quiet)   . rest
A pattern of 32 characters spans two bars. Patterns are starting points, not the answer: edit
them per film (move a kick, add a ghost note, take the hats out of one bar).
"""

from __future__ import annotations

from dataclasses import dataclass, field

VEL = {"X": 1.0, "x": 0.78, "g": 0.38, ".": 0.0}


def beat_frames(bpm: float, fps: int = 60) -> float:
    return fps * 60 / bpm


# Tempos whose beat is a whole number of frames at 60 fps (frames per beat in brackets). A 16th is
# then a quarter of that; 24, 28, 32, 36, 40 and 48 also give whole frame 16ths.
FRAME_TEMPOS = {
    150.0: 24, 144.0: 25, 138.46: 26, 133.33: 27, 128.57: 28, 124.14: 29, 120.0: 30, 116.13: 31, 112.5: 32,
    109.09: 33, 105.88: 34, 102.86: 35, 100.0: 36, 97.3: 37, 94.74: 38, 92.31: 39, 90.0: 40, 85.71: 42,
    81.82: 44, 80.0: 45, 75.0: 48, 72.0: 50, 171.43: 21, 163.64: 22, 156.52: 23,
}


@dataclass
class Genre:
    name: str
    tempos: list[float]          # pick one; all are in FRAME_TEMPOS
    swing: float                 # 0.5 straight, 0.58 light, 0.62 to 0.67 heavy
    drums: dict[str, str]        # part -> pattern; part names map to palette roles below
    bass: dict                   # kind, rhythm pattern, motion
    chords: dict                 # style and rhythm
    palette: dict[str, str]      # role -> instruments.py kind
    modes: list[str]             # modes that suit it
    moods: list[str]             # theory.PROGRESSIONS keys that suit it
    fit: str                     # brands and moments it fits
    signature: str               # the one thing that makes this genre recognisable
    steps_per_beat: int = 4
    beats_per_bar: int = 4
    extra: dict = field(default_factory=dict)


GENRES: dict[str, Genre] = {}


def genre(**kw):
    g = Genre(**kw)
    GENRES[g.name] = g
    return g


genre(
    name="deep_house", tempos=[124.14, 120.0, 116.13], swing=0.56,
    drums={"kick": "x...x...x...x...", "clap": "....x.......x...", "hat_open": "..x...x...x...x.", "shaker": "gxgxgxgxgxgxgxgx"},
    bass={"kind": "fm", "rhythm": "..x...x...x..x.x", "motion": "root and fifth on the offbeats"},
    chords={"style": "stabs", "rhythm": "...x..x....x..x.", "kind": "organ"},
    palette={"kick": "house", "clap": "clap", "hat_open": "open", "shaker": "shaker", "keys": "organ", "pad": "warm", "lead": "vowel"},
    modes=["dorian", "aeolian"], moods=["cool", "hopeful"],
    fit="lifestyle, fashion, music and social apps, anything warm and late night",
    signature="minor 9th organ stabs on the offbeat and a sung vowel lead",
)

genre(
    name="uk_garage", tempos=[133.33, 128.57], swing=0.64,
    drums={"kick": "x.........x.....x.......x.x.....", "snare": "....x.......x...", "hat": "gxgxgxgXgxgxgxgX", "shaker": "..x...x...x...x."},
    bass={"kind": "sub", "rhythm": "x.....x...x...x.", "motion": "warbling sub with octave slides"},
    chords={"style": "stabs", "rhythm": "...x.....x.x....", "kind": "epiano"},
    palette={"kick": "punch", "snare": "crack", "hat": "closed", "shaker": "shaker", "keys": "epiano", "pad": "glass", "lead": "vowel"},
    modes=["aeolian", "dorian"], moods=["cool", "nostalgic"],
    fit="youthful consumer apps, music, nightlife, a London feel",
    signature="the skipping 2-step kick that avoids beat 3, heavy swing on the hats",
)

genre(
    name="trap", tempos=[144.0, 138.46, 150.0], swing=0.5,
    drums={"kick": "x......x..x.....x.x.......x..x..", "snare": "........X.......", "hat": "xxxxxxxxxxxxxxxx", "open": "..............x."},
    bass={"kind": "808", "rhythm": "x......x..x.....", "motion": "808 follows the kick and glides between roots"},
    chords={"style": "pad", "rhythm": "x...............", "kind": "bell"},
    palette={"kick": "808", "snare": "trap", "hat": "trap", "open": "open", "keys": "bell", "pad": "choir", "lead": "fold"},
    modes=["phrygian", "harmonic", "aeolian"], moods=["tense", "epic"],
    fit="bold, competitive, gaming, sports, finance with attitude",
    signature="half time snare on beat 3, rolling hats with triplet rolls, a gliding 808",
    extra={"hat_rolls": True},
)

genre(
    name="boom_bap", tempos=[90.0, 92.31, 94.74], swing=0.6,
    drums={"kick": "x......x..x.....x.x.......x.....", "snare": "....x.......x..g", "hat": "x.x.x.x.x.x.x.x."},
    bass={"kind": "upright", "rhythm": "x......x..x...x.", "motion": "plucked roots that walk to the next chord"},
    chords={"style": "comp", "rhythm": "x.......x..x....", "kind": "piano"},
    palette={"kick": "acoustic", "snare": "crack", "hat": "closed", "keys": "piano", "pad": "strings", "lead": "flute"},
    modes=["dorian", "aeolian"], moods=["cool", "nostalgic"],
    fit="creators, writing and productivity tools, education, anything with a human, crafted feel",
    signature="lazy swung hats, chopped piano and an upright bass",
)

genre(
    name="lofi", tempos=[75.0, 80.0, 81.82], swing=0.63,
    drums={"kick": "x.......x.x.....", "snare": "....x.......x...", "hat": "x.gx.gx.x.gx.gx."},
    bass={"kind": "sub", "rhythm": "x.......x.x.....", "motion": "soft roots"},
    chords={"style": "comp", "rhythm": "x.....x.........", "kind": "epiano"},
    palette={"kick": "soft", "snare": "rim", "hat": "closed", "keys": "epiano", "pad": "warm", "lead": "vibes"},
    modes=["dorian", "ionian"], moods=["nostalgic", "dreamy"],
    fit="focus, study, journaling, wellbeing, calm puzzle and reading apps",
    signature="tape warble, vinyl crackle, a detuned electric piano with maj7 and min9 chords",
    extra={"vinyl": True, "wow": True},
)

genre(
    name="liquid_dnb", tempos=[171.43, 163.64], swing=0.5,
    drums={"kick": "x.........x.....", "snare": "....X.......X...", "ghost": ".......g.g....g.", "hat": "x.x.x.x.x.x.x.x.", "shaker": "gxgxgxgxgxgxgxgx"},
    bass={"kind": "reese", "rhythm": "x.........x.....", "motion": "long rolling reese notes, one per half bar"},
    chords={"style": "pad", "rhythm": "x...............", "kind": "epiano"},
    palette={"kick": "punch", "snare": "tight", "ghost": "tight", "hat": "ride", "shaker": "shaker", "keys": "epiano", "pad": "strings", "lead": "sine"},
    modes=["aeolian", "dorian"], moods=["hopeful", "epic"],
    fit="speed, travel, health and fitness, anything about momentum",
    signature="fast two-step breaks over slow, warm chords and a rolling reese",
)

genre(
    name="amapiano", tempos=[112.5, 109.09], swing=0.58,
    drums={"kick": "x...x...x...x...", "log": "x.....x...x..x..x.......x.x..x..", "shaker": "gxgXgxgxgxgXgxgx", "rim": "...x.....x..x...", "clap": "............x..."},
    bass={"kind": "log", "rhythm": "x.....x...x..x..", "motion": "log drum riffs with slides, fifths and octaves"},
    chords={"style": "pad", "rhythm": "x.......x.......", "kind": "piano"},
    palette={"kick": "soft", "log": "log", "shaker": "shaker", "rim": "rim", "clap": "clap", "keys": "piano", "pad": "warm", "lead": "whistle"},
    modes=["dorian", "aeolian", "ionian"], moods=["cool", "hopeful"],
    fit="social, payments, food and delivery, entertainment, warm and modern",
    signature="the log drum: a pitched, gliding thump in call and response with the kick",
)

genre(
    name="afrobeats", tempos=[105.88, 102.86, 100.0], swing=0.55,
    drums={"kick": "x.....x.....x...", "rim": "..x..x....x..x..", "clap": "....x.......x...", "shaker": "xgxgxgxgxgxgxgxg", "conga": "...x.x.....x.x.x"},
    bass={"kind": "pluck", "rhythm": "x..x..x...x.x...", "motion": "syncopated roots, a step above on the last 8th"},
    chords={"style": "comp", "rhythm": "..x...x...x...x.", "kind": "harp"},
    palette={"kick": "soft", "rim": "rim", "clap": "clap", "shaker": "shaker", "conga": "conga", "keys": "nylon", "pad": "warm", "lead": "steel"},
    modes=["ionian", "mixolydian"], moods=["confident", "playful"],
    fit="joyful consumer apps, food, travel, music, community, payments",
    signature="tresillo kick (3+3+2), interlocking rims and congas, clean plucked guitar lines",
)

genre(
    name="dembow", tempos=[94.74, 97.3, 92.31], swing=0.5,
    drums={"kick": "x...x...x...x...", "snare": "...x..x....x..x.", "hat": "x.x.x.x.x.x.x.x."},
    bass={"kind": "sub", "rhythm": "x...x...x...x...", "motion": "sub on every kick"},
    chords={"style": "stabs", "rhythm": "x..x..x...x..x..", "kind": "marimba"},
    palette={"kick": "boom", "snare": "rim", "hat": "closed", "keys": "marimba", "pad": "saw", "lead": "pluck"},
    modes=["aeolian", "harmonic"], moods=["driving", "tense"],
    fit="energetic consumer, dating, nightlife, sports, Latin markets",
    signature="the dembow: kick on every beat, snare on the and of 1 and on 3 (3+3+2 feel)",
)

genre(
    name="synthwave", tempos=[105.88, 100.0, 109.09], swing=0.5,
    drums={"kick": "x.......x.......", "snare": "....X.......X...", "hat": "x.x.x.x.x.x.x.x."},
    bass={"kind": "octave", "rhythm": "xxxxxxxxxxxxxxxx", "motion": "16th note octave arpeggio on the root"},
    chords={"style": "pad", "rhythm": "x...............", "kind": "saw"},
    palette={"kick": "punch", "snare": "gated", "hat": "closed", "keys": "bell", "pad": "saw", "lead": "square"},
    modes=["aeolian", "dorian"], moods=["nostalgic", "epic"],
    fit="retro, gaming, developer tools, cars, night drives, neon brands",
    signature="gated reverb snare, 16th octave bass, wide detuned saw pads",
)

genre(
    name="nu_disco", tempos=[116.13, 120.0, 112.5], swing=0.52,
    drums={"kick": "x...x...x...x...", "clap": "....x.......x...", "hat_open": "..x...x...x...x.", "tamb": "gxgxgxgxgxgxgxgx"},
    bass={"kind": "octave", "rhythm": "x.x.x.x.x.x.x.x.", "motion": "octave jumps on 8ths"},
    chords={"style": "stabs", "rhythm": "..x.....x.x.....", "kind": "strings"},
    palette={"kick": "house", "clap": "clap", "hat_open": "open", "tamb": "tamb", "keys": "clav", "pad": "strings", "lead": "brass"},
    modes=["ionian", "mixolydian", "dorian"], moods=["confident", "playful"],
    fit="fashion, beauty, shopping, celebration, upbeat social",
    signature="octave bass, string stabs, clavinet and handclaps",
)

genre(
    name="breakbeat", tempos=[128.57, 133.33, 124.14], swing=0.52,
    drums={"kick": "x.........x.....x.x.......x.....", "snare": "....x..g.g..x..g", "hat": "x.x.x.x.x.x.x.x."},
    bass={"kind": "acid", "rhythm": "xx.xx.x.xx.x.xx.", "motion": "a squelching 303 line with slides and accents"},
    chords={"style": "none", "rhythm": "................", "kind": "organ"},
    palette={"kick": "punch", "snare": "crack", "hat": "closed", "keys": "organ", "pad": "air", "lead": "sync"},
    modes=["phrygian", "aeolian", "blues"], moods=["driving", "tense"],
    fit="developer tools, security, hardware, edgy launches",
    signature="a broken beat with ghost snares under a resonant acid line",
)

genre(
    name="jersey_club", tempos=[138.46, 144.0], swing=0.5,
    drums={"kick": "x...x...x..x..x.", "clap": "....x.......x...", "hat": "..x...x...x...x."},
    bass={"kind": "808", "rhythm": "x.......x.......", "motion": "long 808 roots"},
    chords={"style": "stabs", "rhythm": "x.....x.....x...", "kind": "bell"},
    palette={"kick": "punch", "clap": "clap", "hat": "909", "keys": "bell", "pad": "glass", "lead": "vowel"},
    modes=["aeolian", "dorian"], moods=["driving", "playful"],
    fit="youth, social, short video, dance, playful energy",
    signature="the bouncing five kick bar (quarter, quarter, dotted 8th, dotted 8th, 8th) and chopped vowels",
)

genre(
    name="minimal_techno", tempos=[128.57, 124.14], swing=0.54,
    drums={"kick": "x...x...x...x...", "rim": "..x..x....x..x..", "hat_open": "..x...x...x...x.", "clap": "............x...", "perc": "...x......x....x"},
    bass={"kind": "sub", "rhythm": "...x...x...x...x", "motion": "one note, offbeat, filter moving"},
    chords={"style": "stabs", "rhythm": "......x.......x.", "kind": "bell"},
    palette={"kick": "punch", "rim": "rim", "hat_open": "909", "clap": "clap", "perc": "woodblock", "keys": "bell", "pad": "air", "lead": "pluck"},
    modes=["phrygian", "aeolian"], moods=["tense", "cool"],
    fit="infrastructure, AI and data, precision tools, anything systematic and hypnotic",
    signature="a repeating one bar loop that changes by filter and one percussion line at a time",
)

genre(
    name="cinematic_pulse", tempos=[100.0, 90.0, 105.88], swing=0.5,
    drums={"taiko": "x.....x.x.......", "tom": "..........x...x.", "hat": "................"},
    bass={"kind": "sub", "rhythm": "x.......x.......", "motion": "long roots under the strings"},
    chords={"style": "ostinato", "rhythm": "xxxxxxxxxxxxxxxx", "kind": "strings"},
    palette={"taiko": "taiko", "tom": "tom", "hat": "closed", "keys": "piano", "pad": "strings", "lead": "brass"},
    modes=["harmonic", "aeolian", "lydian"], moods=["epic", "wonder"],
    fit="launches, hardware reveals, space, science, enterprise keynotes",
    signature="string ostinato in 16ths, taiko hits, a brass swell on the reveal",
)

genre(
    name="bossa_electronica", tempos=[112.5, 120.0], swing=0.55,
    drums={"kick": "x..x....x..x....", "rim": "x..x..x...x..x..", "shaker": "xgxgxgxgxgxgxgxg"},
    bass={"kind": "upright", "rhythm": "x..x....x..x....", "motion": "root and fifth on the bossa bass rhythm"},
    chords={"style": "comp", "rhythm": "x..x..x...x..x..", "kind": "nylon"},
    palette={"kick": "soft", "rim": "rim", "shaker": "shaker", "keys": "nylon", "pad": "warm", "lead": "flute"},
    modes=["ionian", "lydian", "dorian"], moods=["dreamy", "nostalgic"],
    fit="travel, hospitality, food, design tools, calm premium brands",
    signature="the 3-2 bossa clave on a rim, nylon guitar comping with maj7 and 9th chords",
)

genre(
    name="phonk", tempos=[138.46, 144.0, 133.33], swing=0.5,
    drums={"kick": "x.....x...x.....", "snare": "....x.......x...", "hat": "xxxxxxxxxxxxxxxx", "cowbell": "x.xx.x.xx.x.x.x."},
    bass={"kind": "808", "rhythm": "x.....x...x.....", "motion": "distorted 808 on the kick"},
    chords={"style": "none", "rhythm": "................", "kind": "bell"},
    palette={"kick": "dist", "snare": "clap", "hat": "trap", "cowbell": "cowbell", "keys": "bell", "pad": "choir", "lead": "fold"},
    modes=["phrygian", "harmonic"], moods=["tense", "driving"],
    fit="cars, sports, gaming, edits, anything aggressive and young",
    signature="a melodic cowbell riff in phrygian over a blown out 808",
)

genre(
    name="hyperpop", tempos=[150.0, 156.52], swing=0.5,
    drums={"kick": "x...x...x...x...", "snare": "....x.......x...", "hat": "xxxxxxxxxxxxxxxx"},
    bass={"kind": "808", "rhythm": "x...x...x...x...", "motion": "bright distorted roots"},
    chords={"style": "stabs", "rhythm": "x.x...x.x...x...", "kind": "bell"},
    palette={"kick": "dist", "snare": "crack", "hat": "909", "keys": "celesta", "pad": "saw", "lead": "supersaw"},
    modes=["ionian", "lydian"], moods=["playful", "wonder"],
    fit="Gen Z products, AI toys, creative tools, maximal and loud brands",
    signature="sugary supersaws, pitched up vowels, glitch stutters, everything bright",
)

genre(
    name="funk", tempos=[105.88, 102.86, 109.09], swing=0.56,
    drums={"kick": "x.....x...x.x...", "snare": "....x..g.g..x..g", "hat": "xgxgxgxgxgxgxgxg"},
    bass={"kind": "pluck", "rhythm": "x..x..x.x.x..x.x", "motion": "slap style 16ths with octave pops"},
    chords={"style": "comp", "rhythm": "..x..x.x..x..x.x", "kind": "clav"},
    palette={"kick": "acoustic", "snare": "tight", "hat": "closed", "keys": "clav", "pad": "strings", "lead": "brass"},
    modes=["mixolydian", "dorian"], moods=["playful", "confident"],
    fit="food, fitness classes, social, anything with swagger and humour",
    signature="ghost note snares, 16th clav comping, a brass hook",
)

genre(
    name="ambient_pulse", tempos=[75.0, 72.0, 80.0], swing=0.6,
    drums={"kick": "x.........x.....", "rim": "....x.......x.g.", "hat": "..g...g...g...g."},
    bass={"kind": "sub", "rhythm": "x...............", "motion": "one long note per bar"},
    chords={"style": "pad", "rhythm": "x...............", "kind": "glass"},
    palette={"kick": "soft", "rim": "rim", "hat": "shaker", "keys": "celesta", "pad": "glass", "lead": "vowel"},
    modes=["lydian", "ionian", "dorian"], moods=["dreamy", "wonder"],
    fit="meditation, health, privacy, premium minimal brands, slow reveals",
    signature="slow glassy pads, a sparse half time pulse, one sung vowel motif",
)

genre(
    name="afro_68", tempos=[120.0, 112.5, 105.88], swing=0.5, steps_per_beat=3, beats_per_bar=4,
    drums={"bell": "x.x.xx.x.x.x", "kick": "x.....x.....", "shaker": "xgxxgxxgxxgx", "conga": "..x..x..xx.x"},
    bass={"kind": "pluck", "rhythm": "x..x..x..x..", "motion": "dotted quarter roots"},
    chords={"style": "comp", "rhythm": "x..x..x..x..", "kind": "marimba"},
    palette={"bell": "agogo", "kick": "soft", "shaker": "shaker", "conga": "conga", "keys": "marimba", "pad": "warm", "lead": "flute"},
    modes=["mixolydian", "ionian"], moods=["playful", "confident"],
    fit="community, education, travel, anything warm with a rolling triple feel",
    signature="12/8 with the West African standard bell pattern: a rolling triple feel nothing else has",
    extra={"meter": "12/8"},
)


def hits(pattern: str, start: float, step: float, swing: float = 0.5, steps_per_beat: int = 4, humanize: float = 0.0, rng=None):
    """(time in seconds, velocity) for every hit in a pattern starting at start. step is one
    step's length in seconds. Swing delays the second step of each pair (16ths in 4/4)."""
    out = []
    for i, ch in enumerate(pattern):
        v = VEL.get(ch, 0.0)
        if v <= 0:
            continue
        t = start + i * step
        if steps_per_beat % 2 == 0 and i % 2 == 1:
            t += (2 * swing - 1) * step
        if humanize and rng is not None:
            t += rng.normal(0, humanize)
            v *= 1 + rng.normal(0, 0.06)
        out.append((t, max(0.05, v)))
    return out


def roll(start: float, length: float, rate: float, v0=0.5, v1=1.0):
    """A hat or snare roll: hits every rate seconds over length, velocity ramping."""
    n = max(1, int(length / rate))
    return [(start + i * rate, v0 + (v1 - v0) * i / n) for i in range(n)]
