"""
Sampled instruments for the score: a small SFZ player in numpy, so the engine's patterns and
harmony are performed by recorded instruments instead of oscillators.

    sampler.py --list                     every mapped kind and whether its samples are installed
    sampler.py --demo piano [--out x.wav]  a short phrase on one kind, for a quick check
    sampler.py --test                     self test on a generated SFZ (no library needed)

The library lives outside the skill (fetch_instruments.sh, default /games/mgpro/instruments, or
$MGPRO_INSTRUMENTS). sampler_map.json maps the engine's instrument kinds (keys:piano, kick:punch,
pad:strings ...) to instruments made of one or more SFZ layers. score.py uses it when music.json
says "instruments": "samples" and falls back to the synth for any kind the map does not cover or
when the library is missing.

What the player does:
  SFZ        #include, #define, <control> default_path and set_ccN, <global>/<master>/<group>/
             <region> inheritance, key and velocity ranges, note names, pitch_keycenter, tune,
             transpose, pitch_keytrack, volume, amplitude, pan, offset, end, amp_veltrack and
             amp_velcurve_N, ampeg attack/hold/decay/sustain/release, loop_mode one_shot,
             trigger=release with rt_decay, group/off_by/off_mode (choke), seq_length/position
             and lorand/hirand (round robins), locc/hicc against the set_cc defaults, sw_last
             against sw_default. Paths are matched without case, a missing .wav is read as .flac.
  folders    load_folder(): file names carrying a note (C4, F#3, A#-1), a layer (v2, vl3, pp..fff,
             soft/med/loud) and a round robin (rr2) become regions, split halfway between notes.
  playing    the region nearest the note is repitched (polyphase resampling, file rate to 48 kHz
             in the same pass); a round robin bag per key and layer never repeats a take twice in
             a row; release samples play at note off; a sustain pedal holds note offs; choke
             groups cut ringing voices (an open hat by the closed hat); notes longer than their
             sample loop its tail with a crossfade; notes outside the range move by octaves.
  space      convolution with a recorded room (Voxengo IRs when installed) or a generated one.
"""

from __future__ import annotations

import json
import math
import os
import re
import sys
from collections import OrderedDict
from fractions import Fraction
from functools import lru_cache
from pathlib import Path

import numpy as np
import soundfile as sf
from scipy import signal

SR = 48_000
HERE = Path(__file__).resolve().parent
LIBRARY = Path(os.environ.get("MGPRO_INSTRUMENTS", "/games/mgpro/instruments"))
MAP = HERE / "sampler_map.json"
READ_SECONDS = 14.0  # longest stretch of one sample ever read; longer notes loop the tail
NOTES = {"c": 0, "d": 2, "e": 4, "f": 5, "g": 7, "a": 9, "b": 11}


def note_number(v) -> int:
    """60, "60", "c4", "F#3", "bb2", "A#-1" -> MIDI note (c4 = 60)."""
    s = str(v).strip().lower()
    if re.fullmatch(r"-?\d+", s):
        return int(s)
    m = re.fullmatch(r"([a-g])([#b]?)(-?\d+)", s)
    if not m:
        raise ValueError(f"not a note: {v}")
    return 12 * (int(m[3]) + 1) + NOTES[m[1]] + {"#": 1, "b": -1, "": 0}[m[2]]


# --- Paths -------------------------------------------------------------------------------------


@lru_cache(maxsize=4096)
def _listing(d: str) -> dict:
    try:
        return {p.lower(): p for p in os.listdir(d)}
    except OSError:
        return {}


def resolve(base: Path, rel: str) -> Path | None:
    """A sample path from an SFZ: backslashes, any case, .wav stored as .flac."""
    cur = base
    parts = [p for p in rel.replace("\\", "/").split("/") if p not in ("", ".")]
    for i, part in enumerate(parts):
        if part == "..":
            cur = cur.parent
            continue
        names = _listing(str(cur))
        hit = names.get(part.lower())
        if hit is None and i == len(parts) - 1 and part.lower().endswith(".wav"):
            hit = names.get(part.lower()[:-4] + ".flac")
        if hit is None:
            return None
        cur = cur / hit
    return cur


# --- SFZ parsing -------------------------------------------------------------------------------


def _expand(path: Path, root: Path, defines: dict, depth=0, pinned=frozenset()) -> list[str]:
    """Lines of an SFZ with comments removed, #include inlined and $defines substituted (a pinned
    define, given by the map, wins over the file's own)."""
    if depth > 12:
        raise RuntimeError(f"#include too deep at {path}")
    txt = re.sub(r"/\*.*?\*/", " ", path.read_text(errors="replace"), flags=re.S)
    out = []
    for line in txt.splitlines():
        line = re.sub(r"(^|\s)//.*", "", line)
        s = line.strip()
        if not s:
            continue
        if s.startswith("#define"):
            parts = s.split(None, 2)
            if len(parts) == 3 and parts[1] not in pinned:
                defines[parts[1]] = parts[2].strip()
            continue
        m = re.match(r'#include\s+"(.+?)"', s)
        if m:
            inc = resolve(root, m[1])
            if inc is None:
                raise FileNotFoundError(f"{path}: #include {m[1]}")
            out += _expand(inc, root, defines, depth + 1, pinned)
            continue
        for k in sorted(defines, key=len, reverse=True):
            line = line.replace(k, defines[k])
        out.append(line)
    return out


TOKEN = re.compile(r"<(\w+)>|([A-Za-z0-9_]+)=")


def parse_sfz(path: Path, defines: dict | None = None) -> tuple[list[dict], dict]:
    """(regions as flat opcode dicts with '_path' resolved, control opcodes). defines pins $names."""
    path = Path(path)
    root = path.parent
    control: dict = {}
    levels = {"global": {}, "master": {}, "group": {}}
    region = None
    level = "global"
    regions = []

    def flush():
        if region is not None:
            regions.append({**levels["global"], **levels["master"], **levels["group"], **region})

    for line in _expand(path, root, dict(defines or {}), 0, frozenset(defines or ())):
        toks = list(TOKEN.finditer(line))
        for i, m in enumerate(toks):
            if m[1]:
                head = m[1].lower()
                if head == "region":
                    flush()
                    region, level = {"_dp": control.get("default_path", "")}, "region"
                    continue
                flush()
                region = None
                if head == "global":
                    levels.update(global_={}, master={}, group={})
                    levels["global"] = {}
                elif head == "master":
                    levels["master"], levels["group"] = {}, {}
                elif head == "group":
                    levels["group"] = {}
                level = head if head in ("control", "global", "master", "group") else "ignore"
                continue
            end = toks[i + 1].start() if i + 1 < len(toks) else len(line)
            key, val = m[2].lower(), line[m.end() : end].strip()
            if level == "control":
                control[key] = val
            elif level == "region":
                region[key] = val
            elif level in levels:
                levels[level][key] = val
    flush()
    levels.pop("global_", None)
    for r in regions:
        rel = r.get("sample")
        r["_path"] = resolve(root, r["_dp"].replace("\\", "/") + rel) if rel else None
    return regions, control


class Region:
    __slots__ = ("path", "lokey", "hikey", "center", "lovel", "hivel", "trigger", "alt", "tune", "keytrack", "gain",
                 "pan", "offset", "end", "one_shot", "attack", "hold", "decay", "sustain", "release", "veltrack",
                 "velcurve", "group", "off_by", "off_fast", "rt_decay", "xf")

    def __init__(self, op: dict, note_shift: int = 0, cc: dict | None = None):
        op = _cc_resolve(op, cc or {})
        f = lambda k, d: float(op.get(k, d))  # noqa: E731
        if "key" in op:
            k = note_number(op["key"])
            self.lokey = self.hikey = self.center = k
        else:
            self.lokey, self.hikey = note_number(op.get("lokey", 0)), note_number(op.get("hikey", 127))
            self.center = note_number(op.get("pitch_keycenter", 60)) if op.get("pitch_keycenter", "").lower() != "sample" else 60
        if "pitch_keycenter" in op and op["pitch_keycenter"].lower() != "sample":
            self.center = note_number(op["pitch_keycenter"])
        self.lokey -= note_shift
        self.hikey -= note_shift
        self.center -= note_shift
        self.path = op["_path"]
        self.lovel, self.hivel = int(f("lovel", 0)), int(f("hivel", 127))
        trig = op.get("trigger", "attack").lower()
        self.trigger = "release" if trig.startswith("release") else "attack"
        seq = int(f("seq_length", 1))
        self.alt = (int(f("seq_position", 1)) if seq > 1 else 0, round(f("lorand", 0) * 1000))
        self.tune = f("tune", 0) / 100 + f("transpose", 0)
        self.keytrack = f("pitch_keytrack", 100) / 100
        vol = f("volume", 0) + f("group_volume", 0) + f("master_volume", 0) + f("global_volume", 0)
        self.gain = 10 ** (vol / 20) * f("amplitude", 100) / 100
        self.pan = f("pan", 0) / 100
        self.offset, self.end = int(f("offset", 0)), int(f("end", 0))
        self.one_shot = op.get("loop_mode", "").lower() == "one_shot"
        self.attack, self.hold, self.decay = f("ampeg_attack", 0.0), f("ampeg_hold", 0.0), f("ampeg_decay", 0.0)
        self.sustain = f("ampeg_sustain", 100) / 100
        self.release = f("ampeg_release", 0.08)
        self.veltrack = f("amp_veltrack", 100) / 100
        pts = sorted((int(k[13:]), float(v)) for k, v in op.items() if re.fullmatch(r"amp_velcurve_\d+", k))
        self.velcurve = pts or None
        self.group = int(f("group", 0))
        self.off_by = int(op["off_by"]) if "off_by" in op else None
        self.off_fast = op.get("off_mode", "fast").lower() == "fast"
        self.rt_decay = f("rt_decay", 0)
        self.xf = tuple(f(k, d) for k, d in (("xfin_lovel", 0), ("xfin_hivel", 0), ("xfout_lovel", 127), ("xfout_hivel", 127)))

    def vel_gain(self, vel: int) -> float:
        if self.velcurve:
            xs, ys = zip(*([(0, 0.0)] + self.velcurve + ([(127, 1.0)] if self.velcurve[-1][0] < 127 else [])))
            g = float(np.interp(vel, xs, ys))
        else:
            g = (max(vel, 1) / 127) ** (2 * self.veltrack)
        a, b, c, d = self.xf  # velocity crossfades, power curve
        if b > a:
            g *= math.sqrt(min(max((vel - a) / (b - a), 0.0), 1.0))
        if d > c:
            g *= math.sqrt(1 - min(max((vel - c) / (d - c), 0.0), 1.0))
        return g


# Opcodes a controller moves linearly (value + depth * cc / 127). Tuning and filters are left out:
# kits centre their tune controllers with bipolar curves this player does not model.
CC_MOVES = {"pan", "volume", "ampeg_attack", "ampeg_hold", "ampeg_decay", "ampeg_sustain", "ampeg_release", "offset"}
CC_DEFAULT = {"ampeg_sustain": 100}


def _cc_resolve(op: dict, cc: dict) -> dict:
    out = dict(op)
    for k, v in op.items():
        m = re.fullmatch(r"(\w+?)_oncc(\d+)", k) or re.fullmatch(r"(ampeg_[a-z]+)cc(\d+)", k)
        if m and m[1] in CC_MOVES:
            try:
                base = float(out.get(m[1], CC_DEFAULT.get(m[1], 0)))
                out[m[1]] = str(base + float(v) * cc.get(int(m[2]), 0) / 127)
            except ValueError:
                continue
    return out


def _cc_ok(op: dict, cc: dict) -> bool:
    for k, v in op.items():
        m = re.fullmatch(r"(lo|hi)cc(\d+)", k)
        if m:
            val = cc.get(int(m[2]), 0)
            if (m[1] == "lo" and val < float(v)) or (m[1] == "hi" and val > float(v)):
                return False
    return True


def regions_from_sfz(path: Path, switch=None, cc: dict | None = None, defines: dict | None = None,
                     chokes: set | None = None) -> list[Region]:
    """Playable regions with controllers at their set_cc defaults (or cc overrides, {"4": 127}).
    chokes, when given, collects every (off_by, group) pair, also of regions the controllers
    leave out, so choke chains through them still hold."""
    ops, control = parse_sfz(path, defines)
    if chokes is not None:
        chokes.update((int(o["off_by"]), int(o.get("group", 0))) for o in ops if "off_by" in o)
    cc = {**{int(k[6:]): float(v) for k, v in control.items() if re.fullmatch(r"set_cc\d+", k)},
          **{int(k): float(v) for k, v in (cc or {}).items()}}
    shift = -int(control.get("note_offset", 0)) - 12 * int(control.get("octave_offset", 0))
    sw = [o for o in ops if "sw_last" in o]
    if sw:
        if switch is None:
            d = next((o["sw_default"] for o in ops if "sw_default" in o), None)
            switch = note_number(d) if d is not None else min(note_number(o["sw_last"]) for o in sw)
        ops = [o for o in ops if "sw_last" not in o or note_number(o["sw_last"]) == switch]
    out = []
    for o in ops:
        if o["_path"] is None or not _cc_ok(o, cc):
            continue
        try:
            out.append(Region(o, shift, cc))
        except ValueError:
            continue
    return out


# --- Folder instruments ------------------------------------------------------------------------

DYN = {"ppp": 1, "pp": 2, "p": 3, "mp": 4, "mf": 5, "f": 6, "ff": 7, "fff": 8, "soft": 2, "med": 5, "medium": 5, "loud": 7}


def load_folder(d) -> list[Region]:
    """Regions from file names: a note (C4, F#3), a layer (v2, vl3, pp..fff, soft, loud), a round
    robin (rr2). Keys split halfway between sampled notes; layers split the velocity range evenly.
    A folder with no notes in its names is one unpitched drum: every file sits on key 60, one shot.
    d is a folder or a list of files."""
    found = []
    for p in sorted(Path(d).rglob("*")) if isinstance(d, (str, Path)) else sorted(map(Path, d)):
        if p.suffix.lower() not in (".wav", ".flac", ".ogg"):
            continue
        toks = re.split(r"[_\s\-.]+(?=[A-Za-z])|[_\s.]+", p.stem)
        note = next((note_number(t) for t in toks if re.fullmatch(r"[A-Ga-g][#b]?-?\d", t)), None)
        layer = next((int(m[1]) for t in toks if (m := re.fullmatch(r"(?:v|vl|dyn)(\d+)", t, re.I))), None)
        if layer is None:
            layer = next((DYN[t.lower()] for t in toks if t.lower() in DYN), 1)
        rr = next((int(m[1]) for t in toks if (m := re.fullmatch(r"rr(\d+)", t, re.I))), 1)
        found.append((note, layer, rr, p))
    shot = all(n is None for n, *_ in found)
    found = [(60 if shot else n, ly, rr, p) for n, ly, rr, p in found if shot or n is not None]
    notes = sorted({n for n, *_ in found})
    out = []
    for n, layer, rr, p in found:
        i = notes.index(n)
        lo = 0 if i == 0 else (notes[i - 1] + n) // 2 + 1
        hi = 127 if i == len(notes) - 1 else (n + notes[i + 1]) // 2
        layers = sorted({ly for nn, ly, *_ in found if nn == n})
        j = layers.index(layer)
        op = {"_path": p, "lokey": lo, "hikey": hi, "pitch_keycenter": n, "seq_length": 9, "seq_position": rr,
              "lovel": 1 + 127 * j // len(layers), "hivel": 127 * (j + 1) // len(layers), "amp_veltrack": 40}
        if shot:
            op["loop_mode"] = "one_shot"
        out.append(Region({k: str(v) if k != "_path" else v for k, v in op.items()}))
    return out


# --- Audio helpers -----------------------------------------------------------------------------


class _LRU(OrderedDict):
    def __init__(self, max_bytes):
        super().__init__()
        self.max_bytes, self.bytes = max_bytes, 0

    def put(self, k, v):
        if k in self:
            self.bytes -= self.pop(k)[0].nbytes
        self[k] = v
        self.bytes += v[0].nbytes
        while self.bytes > self.max_bytes and len(self) > 1:
            self.bytes -= self.popitem(last=False)[1][0].nbytes

    def get_(self, k):
        if k in self:
            self.move_to_end(k)
            return self[k]
        return None


_RAW = _LRU(1_500_000_000)
_PITCHED = _LRU(1_000_000_000)


def load(path: Path, frames: int) -> tuple[np.ndarray, int, bool]:
    """(stereo float32 (2, n), file rate, whole file read)."""
    hit = _RAW.get_(path)
    if hit is not None and (hit[2] or hit[0].shape[1] >= frames):
        return hit
    info = sf.info(str(path))
    x, sr = sf.read(str(path), frames=min(frames, info.frames), dtype="float32", always_2d=True)
    x = np.ascontiguousarray((x if x.shape[1] > 1 else np.repeat(x, 2, 1))[:, :2].T)
    # Some spaced pair recordings are close to polarity inverted between channels (VCSL marimba
    # B4: correlation -0.7) and vanish on a phone speaker; such a file plays its louder channel.
    e = np.einsum("ij,ij->i", x, x)
    if float(x[0] @ x[1]) < -0.3 * math.sqrt(e[0] * e[1] + 1e-20):
        x = np.repeat(x[[int(np.argmax(e))]], 2, 0)
    v = (x, sr, frames >= info.frames)
    _RAW.put(path, v)
    return v


@lru_cache(maxsize=64)
def _fir(up: int, down: int) -> np.ndarray:
    half = 10 * max(up, down)
    return signal.firwin(2 * half + 1, 1.0 / max(up, down), window=("kaiser", 5.0))


def repitch(x: np.ndarray, ratio: float) -> np.ndarray:
    """Resample by ratio input samples per output sample (pitch up when > 1), polyphase."""
    if abs(ratio - 1) < 1e-7:
        return x
    fr = Fraction(1 / ratio).limit_denominator(400)
    return signal.resample_poly(x, fr.numerator, fr.denominator, axis=-1, window=_fir(fr.numerator, fr.denominator)).astype(np.float32)


def loop_tail(y: np.ndarray, n: int, xfade: int = int(0.12 * SR)) -> np.ndarray:
    """Lengthen a sustained note to n samples by crossfade looping its middle to late part."""
    if y.shape[1] >= n or y.shape[1] < 4 * xfade:
        return y
    a, b = int(y.shape[1] * 0.45), y.shape[1] - xfade
    seg = y[:, a:b]
    out = [y[:, :b]]
    length = b
    ramp = np.sin(np.linspace(0, np.pi / 2, xfade)) ** 2
    tail = y[:, b:]
    while length < n:
        head = seg[:, :xfade] * ramp + tail[:, :xfade] * ramp[::-1]
        out += [head, seg[:, xfade:]]
        length += seg.shape[1]
        tail = y[:, b:]
    return np.concatenate(out, axis=1)[:, :n]


def pan2(y: np.ndarray, pan: float) -> np.ndarray:
    """Balance a stereo pair: pan -1 (left) to 1 (right), centre untouched."""
    if not pan:
        return y
    return y * np.array([[min(1.0, 1 - pan)], [min(1.0, 1 + pan)]], dtype=np.float32)


# --- The instrument ----------------------------------------------------------------------------


class Voice:
    __slots__ = ("start", "y", "group", "off_by", "fade", "cut")

    def __init__(self, start, y, group, off_by, fade):
        self.start, self.y, self.group, self.off_by, self.fade, self.cut = start, y, group, off_by, fade, None


class Instrument:
    """One sampled instrument: regions from one or more SFZ files or folders."""

    def __init__(self, regions: list[Region], name="instrument", seed=1, releases=True, edges=None):
        if not regions:
            raise ValueError(f"{name}: no playable regions")
        self.name, self.regions, self.releases = name, regions, releases
        att = [r for r in regions if r.trigger == "attack"]
        self.lo, self.hi = min(r.lokey for r in att), max(r.hikey for r in att)
        self.rng = np.random.default_rng(seed)
        self._bags: dict = {}
        # Chokes follow off_by chains: a closed hat cuts the half open hat, which cuts the 3/4,
        # which cuts the open one, so closing the hat silences any more open state.
        cut_by: dict = {}
        for a, b in set(edges or ()) | {(r.off_by, r.group) for r in regions if r.off_by is not None}:
            cut_by.setdefault(a, set()).add(b)
        self.chokes = {}
        for g in {r.group for r in regions}:
            seen, todo = set(), [g]
            while todo:
                for h in cut_by.get(todo.pop(), ()):
                    if h not in seen:
                        seen.add(h)
                        todo.append(h)
            self.chokes[g] = seen

    @classmethod
    def from_path(cls, p: Path, name=None, seed=1, switch=None, releases=True, cc=None, defines=None):
        p = Path(p)
        edges: set = set()
        regions = regions_from_sfz(p, switch, cc, defines, edges) if p.suffix.lower() == ".sfz" else load_folder(p)
        return cls(regions, name or p.stem, seed, releases, edges)

    def pick(self, m: int, vel: int, trigger="attack") -> list[Region]:
        """The regions that sound for this note: every match, one round robin take, never the same
        take twice in a row on one key and layer."""
        c = [r for r in self.regions if r.trigger == trigger and r.lokey <= m <= r.hikey and r.lovel <= vel <= r.hivel]
        if not c:  # a velocity outside every layer takes the nearest layer
            c = [r for r in self.regions if r.trigger == trigger and r.lokey <= m <= r.hikey]
            if not c:
                return []
            near = min(c, key=lambda r: min(abs(vel - r.lovel), abs(vel - r.hivel)))
            c = [r for r in c if (r.lovel, r.hivel) == (near.lovel, near.hivel)]
        alts = sorted({r.alt for r in c})
        if len(alts) > 1:
            slot = (trigger, m, tuple(sorted({(r.lovel, r.hivel) for r in c})))
            st = self._bags.setdefault(slot, {"bag": [], "last": None})
            if not st["bag"]:
                bag = [alts[i] for i in self.rng.permutation(len(alts))]
                if bag[0] == st["last"]:
                    bag.append(bag.pop(0))
                st["bag"] = bag
            st["last"] = st["bag"].pop(0)
            c = [r for r in c if r.alt == st["last"]]
        return c

    def play(self, r: Region, m: float, vel: int, dur: float, one_shot=None, attack=None, release=None) -> np.ndarray:
        """One region sounding: repitched to m, enveloped, its own gain and pan applied."""
        shot = r.one_shot if one_shot is None else one_shot
        rel = r.release if release is None else release
        semis = (m - r.center) * r.keytrack + r.tune
        probe = sf.info(str(r.path)).samplerate if _RAW.get_(r.path) is None else _RAW.get_(r.path)[1]
        ratio = 2 ** (semis / 12) * probe / SR
        want_out = int(READ_SECONDS * SR) if shot else int((dur + rel * 1.2 + 0.05) * SR)
        want_in = min(int(READ_SECONDS * probe), int(want_out * ratio) + 4096) + r.offset
        x, fsr, whole = load(r.path, want_in)
        x = x[:, r.offset : (r.end + 1 if r.end else None)]
        key = (r.path, r.offset, r.end, round(ratio, 9))
        hit = _PITCHED.get_(key)
        if hit is not None and (hit[1] or hit[0].shape[1] >= min(want_out, int(x.shape[1] / ratio) - 8)):
            y = hit[0]
        else:
            y = repitch(x, ratio)
            _PITCHED.put(key, (y, whole))
        if not shot:
            y = loop_tail(y, want_out)[:, :want_out]
        n = y.shape[1]
        t = np.arange(n, dtype=np.float32) / SR
        a = max(r.attack, attack or 0.0, 0.0008)
        env = np.minimum(1.0, t / a)
        if r.decay > 0 and r.sustain < 1:
            k = np.clip((t - a - r.hold) / r.decay, 0, 1)
            env *= 1 - (1 - r.sustain) * k
        if not shot:
            off = dur
            env *= np.where(t < off, 1.0, np.exp(-6.9 * np.maximum(t - off, 0) / max(rel, 0.01)))
        y = y * env.astype(np.float32)
        return pan2(y * (r.gain * r.vel_gain(vel)), r.pan)

    def render(self, events: list[dict], seconds: float | None = None, pedal=(), vel=(1, 127), gamma=1.0,
               releases=None) -> np.ndarray:
        """Events {"t": s, "m": midi, "v": 0..1, "d": s, "pan", "gain", "attack", "release"} to a
        stereo buffer at 48 kHz. vel maps v to a MIDI velocity range (gamma shapes it); pedal is a
        list of (down, up) seconds: note offs inside one wait for its release."""
        releases = self.releases if releases is None else releases
        voices: list[Voice] = []
        for e in sorted(events, key=lambda e: e["t"]):
            t = float(e["t"])
            m = float(e.get("m", 60))
            mi = int(round(m))
            while mi < self.lo:
                mi, m = mi + 12, m + 12
            while mi > self.hi:
                mi, m = mi - 12, m - 12
            v = min(max(float(e.get("v", 0.8)), 0.0), 1.0)
            velocity = int(round(vel[0] + (vel[1] - vel[0]) * v**gamma))
            t_off = t + float(e.get("d", 0.0))
            for a, b in pedal:
                if a <= t_off < b:
                    t_off = b
            i0 = int(round(t * SR))
            g = float(e.get("gain", 1.0))
            for r in self.pick(mi, velocity):
                cuts = self.chokes.get(r.group, ())
                for vo in voices:  # choke: this region's group silences voices that are off_by it
                    if vo.group in cuts and vo.off_by is not None and vo.start < i0 < vo.start + vo.y.shape[1]:
                        vo.cut = i0 if vo.cut is None else min(vo.cut, i0)
                y = self.play(r, m + (mi - round(m)), velocity, t_off - t, None, e.get("attack"), e.get("release"))
                y = pan2(y * g, float(e.get("pan", 0.0)))
                voices.append(Voice(i0, y, r.group, r.off_by, 0.006 if r.off_fast else r.release))
            if releases:
                for r in self.pick(mi, velocity, "release"):
                    y = self.play(r, m, velocity, 0.0, one_shot=True) * g * 10 ** (-r.rt_decay * (t_off - t) / 20)
                    voices.append(Voice(int(round(t_off * SR)), pan2(y, float(e.get("pan", 0.0))), r.group, None, 0.0))
        n = int(round(seconds * SR)) if seconds else max((v.start + v.y.shape[1] for v in voices), default=0)
        out = np.zeros((2, n), np.float32)
        for vo in voices:
            y = vo.y
            if vo.cut is not None:
                k = vo.cut - vo.start
                f = max(1, int(vo.fade * SR))
                y = y[:, : k + f].copy()
                y[:, k:] *= np.exp(-6.9 * np.arange(y.shape[1] - k) / f)
            lo, hi = max(vo.start, 0), min(n, vo.start + y.shape[1])
            if hi > lo:
                out[:, lo:hi] += y[:, lo - vo.start : hi - vo.start]
        return out


class Layered:
    """Several instruments as one, split by key (cello low, violas middle, violins high)."""

    def __init__(self, parts: list[tuple[Instrument, int, int]]):
        self.parts = parts
        self.lo = min(p[1] for p in parts)
        self.hi = max(p[2] for p in parts)

    def render(self, events, seconds=None, **kw):
        out = None
        for inst, lo, hi in self.parts:
            mine = [e for e in events if lo <= round(e.get("m", 60)) <= hi]
            if not mine:
                continue
            y = inst.render(mine, seconds, **kw)
            if out is None:
                out = y
            else:
                L = max(out.shape[1], y.shape[1])
                out = np.pad(out, ((0, 0), (0, L - out.shape[1]))) + np.pad(y, ((0, 0), (0, L - y.shape[1])))
        return out if out is not None else np.zeros((2, int(round((seconds or 0) * SR))), np.float32)


# --- Space -------------------------------------------------------------------------------------


def room_ir(rt60=1.2, predelay=0.012, size=0.6, seed=7, bright=0.5) -> np.ndarray:
    """A generated stereo room: sparse early reflections, then decorrelated noise whose highs die
    faster than its lows (three bands with their own decay), faded in so it has no hard edge."""
    rng = np.random.default_rng(seed)
    n = int((rt60 * 1.3 + predelay) * SR)
    t = np.arange(n) / SR
    ir = np.zeros((2, n))
    p0 = int(predelay * SR)
    for c in range(2):
        for _ in range(int(14 + 20 * size)):
            k = p0 + int(rng.uniform(0.002, 0.03 + 0.06 * size) * SR)
            ir[c, k] += rng.choice([-1, 1]) * rng.uniform(0.2, 0.7) * np.exp(-k / SR / (rt60 / 6.9))
        noise = rng.standard_normal(n)
        late = np.zeros(n)
        for lo, hi, mult in ((20, 500, 1.15), (500, 3000, 1.0), (3000, 16000, 0.45 + 0.4 * bright)):
            band = signal.sosfilt(signal.butter(2, [lo, hi], "bandpass", fs=SR, output="sos"), noise)
            late += band * np.exp(-6.9 * t / (rt60 * mult))
        onset = np.clip((t - predelay) / (0.02 + 0.05 * size), 0, 1) ** 2
        ir[c] += late * onset * 0.5
    return ir / np.sqrt((ir**2).sum(axis=1, keepdims=True))


@lru_cache(maxsize=8)
def load_ir(path: str) -> np.ndarray:
    x, sr = sf.read(path, dtype="float64", always_2d=True)
    x = x.T if x.shape[1] > 1 else np.repeat(x.T, 2, 0)
    x = x[:2]
    if sr != SR:
        fr = Fraction(SR, sr)
        x = signal.resample_poly(x, fr.numerator, fr.denominator, axis=-1)
    x = x[:, np.argmax(np.abs(x).max(0) > 1e-4 * np.abs(x).max()) :]  # no dead lead
    return x / np.sqrt((x**2).sum(axis=1, keepdims=True))


def convolve(x: np.ndarray, ir: np.ndarray, wet=0.2, lo=180.0, hi=9000.0, width=0.6) -> np.ndarray:
    """x plus wet times its convolution with ir; the wet signal band limited so it never muds the
    low end or adds fizz, and its side narrowed (width) so stereo samples plus a wide room stay
    inside the professional side share (p90 0.24)."""
    if wet <= 0 or not np.any(x):
        return x
    w = np.stack([signal.oaconvolve(x[c], ir[c % ir.shape[0]])[: x.shape[1]] for c in range(2)])
    w = signal.sosfilt(signal.butter(2, [lo, hi], "bandpass", fs=SR, output="sos"), w, axis=-1)
    mid, side = (w[0] + w[1]) / 2, (w[0] - w[1]) / 2 * width
    return x + wet * np.stack([mid + side, mid - side])


# --- The map and the performer used by score.py ------------------------------------------------


def load_map(path: Path = MAP, overrides: dict | None = None) -> dict:
    m = json.loads(Path(path).read_text())
    m["kinds"] = {**m["kinds"], **(overrides or {})}
    return m


class Performer:
    """Collects note events per sampled instrument during one score render and renders each
    instrument's events in one pass at the end (round robins and chokes need the whole part).
    score.py asks note() or chord(); False means "no sample for this kind, use the synth"."""

    def __init__(self, seed=1, overrides=None, library: Path | None = None, map_path: Path = MAP, verbose=True):
        self.map = load_map(map_path, overrides)
        self.lib = Path(library or os.environ.get("MGPRO_INSTRUMENTS") or self.map.get("library") or LIBRARY)
        self.seed = seed
        self.rng = np.random.default_rng(seed + 77)
        self.events: dict = {}
        self.cache: dict = {}
        self.missing: set = set()
        self.used: set = set()
        self.say = print if verbose else (lambda *a, **k: None)

    @property
    def available(self) -> bool:
        return self.lib.is_dir() and any(self.lib.iterdir())

    def entry(self, family: str, kind: str) -> dict | None:
        e = self.map["kinds"].get(f"{family}:{kind}")
        if e is None:
            return None
        e = {"instrument": e} if isinstance(e, str) else dict(e)
        spec = self.map["instruments"][e["instrument"]]
        return {**spec, **e}

    def instrument(self, name: str):
        if name in self.cache:
            return self.cache[name]
        spec = self.map["instruments"][name]
        parts = []
        try:
            for i, layer in enumerate(spec["layers"]):
                p = self.lib / layer["path"]
                if "*" in layer["path"]:  # a glob of one shot files: a folder instrument
                    files = sorted(self.lib.glob(layer["path"]))
                    if not files:
                        raise FileNotFoundError(p)
                    inst = Instrument(load_folder(files), name, self.seed + 31 * i)
                elif not p.exists():
                    raise FileNotFoundError(p)
                else:
                    inst = Instrument.from_path(p, name, self.seed + 31 * i, layer.get("switch"), spec.get("releases", True),
                                                layer.get("cc"), layer.get("defines"))
                parts.append((inst, layer.get("lokey", 0), layer.get("hikey", 127)))
        except (FileNotFoundError, ValueError) as err:
            if name not in self.missing:
                self.say(f"  sampler: {name} not available ({err}); the synth plays it")
            self.missing.add(name)
            self.cache[name] = None
            return None
        inst = parts[0][0] if len(parts) == 1 and parts[0][1:] == (0, 127) else Layered(parts)
        self.cache[name] = inst
        return inst

    def has(self, family: str, kind: str) -> bool:
        e = self.entry(family, kind)
        return e is not None and self.instrument(e["instrument"]) is not None

    def note(self, bus: str, family: str, kind: str, t: float, m, v: float, d: float, gain=1.0, pan=0.0, **kw) -> bool:
        if not self.has(family, kind):
            return False
        e = self.entry(family, kind)
        m = e["key"] if "key" in e else m
        m = (m if m is not None else 60) + 12 * e.get("octave", 0)
        ev = {"t": t, "m": m, "v": v, "d": max(d, e.get("min_d", 0.0)), "gain": gain, "pan": pan, **kw}
        self.events.setdefault((e["instrument"], f"{family}:{kind}", bus), []).append(ev)
        self.used.add(e["instrument"])
        return True

    def chord(self, bus, family, kind, t, notes, v, d, gain=1.0, spread=0.012, width=0.5, **kw) -> bool:
        """A chord with its notes spread a few ms and across the field, as a hand plays it."""
        if not self.has(family, kind):
            return False
        n = len(notes)
        for i, m in enumerate(sorted(notes)):
            pos = (i / max(1, n - 1) - 0.5) * 2 * width
            vv = v * (0.9 + 0.2 * self.rng.random())
            self.note(bus, family, kind, t + spread * i * self.rng.uniform(0.6, 1.2), m, vv, d, gain / math.sqrt(n), pos, **kw)
        return True

    def norm(self, name: str, e: dict) -> float:
        """Gain so a note at full velocity peaks near 1, like the synth's instruments."""
        key = ("norm", name, e.get("key"))
        if key not in self.cache:
            inst = self.cache[name]
            m = e["key"] if "key" in e else (inst.lo + inst.hi) // 2
            vel = tuple(self.map["instruments"][name].get("vel", (1, 127)))  # the instrument's own range, so a softer kind stays softer
            y = inst.render([{"t": 0, "m": m, "v": 1.0, "d": 0.6}], None, vel=vel)
            self.cache[key] = 1.0 / max(float(np.abs(y).max()), 1e-4)
        return self.cache[key]

    def render(self, buses: dict, seconds: float, pedal_by_bus: dict | None = None) -> None:
        """Every collected part into its bus (dsp.Bus objects with .x)."""
        for (name, fk, bus), evs in self.events.items():
            e = self.entry(*fk.split(":", 1))
            inst = self.cache[name]
            kw = {"vel": tuple(e.get("vel", (1, 127))), "gamma": e.get("gamma", 1.0), "pedal": (pedal_by_bus or {}).get(bus, ())}
            y = inst.render(evs, seconds, **kw) * (self.norm(name, e) * 10 ** (e.get("db", 0) / 20))
            # spaced pair recordings are wider than the synth; width (default 0.75) narrows the side
            mid, side = (y[0] + y[1]) / 2, (y[0] - y[1]) / 2 * e.get("width", 0.75)
            y = np.stack([mid + side, mid - side])
            n = min(buses[bus].x.shape[1], y.shape[1])
            buses[bus].x[:, :n] += y[:, :n]
        self.events.clear()

    def space(self, x: np.ndarray, room: str, wet: float) -> np.ndarray:
        """Convolve with the map's IR for this room (drums, room, hall), else a generated one."""
        spec = self.map.get("spaces", {}).get(room, {})
        ir = None
        p = self.lib / spec["ir"] if "ir" in spec else None
        if p is not None and p.exists():
            ir = load_ir(str(p))
        else:
            ir = _gen_ir(spec.get("rt60", 1.0), spec.get("size", 0.5))
        return convolve(x, ir, wet * spec.get("wet", 1.0), spec.get("lo", 180.0), spec.get("hi", 9000.0))


@lru_cache(maxsize=8)
def _gen_ir(rt60, size):
    return room_ir(rt60, 0.01 + 0.02 * size, size)


# --- CLI ---------------------------------------------------------------------------------------


def _self_test() -> None:
    import tempfile

    d = Path(tempfile.mkdtemp(prefix="sampler-test-"))
    (d / "s").mkdir()
    names = {60: "C4", 72: "C5"}
    for key, f0 in ((60, 261.6256), (72, 523.2511)):
        for layer in (1, 2):
            for rr in (1, 2, 3):
                t = np.arange(int(1.0 * 44100)) / 44100
                x = np.sin(2 * np.pi * f0 * t) * np.exp(-t / 0.6) * (0.4 * layer) * (1 + 0.01 * rr)
                sf.write(d / "s" / f"tone_{names[key]}_v{layer}_rr{rr}.wav", np.stack([x, x], 1), 44100)
    sf.write(d / "s" / "rel.wav", np.stack([np.ones(441) * 0.3] * 2, 1), 44100)
    sf.write(d / "s" / "hat.wav", np.stack([np.ones(44100) * 0.2] * 2, 1), 44100)
    regions = ["<control>\ndefault_path=s\\\n#define $HATKEY 90\n<global> ampeg_release=0.1\n"]
    for key in (60, 72):
        for layer, (lo, hi) in ((1, (0, 63)), (2, (64, 127))):
            regions.append("<group> seq_length=3 lovel=%d hivel=%d\n" % (lo, hi))
            for rr in (1, 2, 3):
                regions.append(f"<region> sample=TONE_{names[key]}_v{layer}_rr{rr}.wav lokey={key - 6} hikey={key + 5} "
                               f"pitch_keycenter={key} seq_position={rr} // comment\n")
    regions.append("<group> trigger=release rt_decay=3\n<region> sample=rel.wav lokey=0 hikey=89\n")
    regions.append("<group> loop_mode=one_shot group=1 off_by=2\n<region> sample=hat.wav key=$HATKEY\n")
    regions.append("<group> loop_mode=one_shot group=2\n<region> sample=hat.wav key=91 locc5=10\n<region> sample=hat.wav key=91\n")
    (d / "t.sfz").write_text("".join(regions))
    inst = Instrument.from_path(d / "t.sfz", seed=3)
    assert len(inst.regions) == 12 + 1 + 1 + 1, len(inst.regions)  # locc5=10 region dropped (cc5 = 0)
    # Nearest sample and repitch: E4 (64) comes from the C4 sample, two thirds up, at 329.6 Hz.
    r = inst.pick(64, 100)
    assert len(r) == 1 and r[0].center == 60
    y = inst.render([{"t": 0, "m": 64, "v": 1.0, "d": 0.5}], 0.6, releases=False)
    spec = np.abs(np.fft.rfft(y[0, : SR // 2] * np.hanning(SR // 2)))
    f = np.argmax(spec) * SR / (SR // 2)
    assert abs(f - 329.63) < 3, f
    # Round robins: no take twice in a row over many notes.
    seq = [inst.pick(60, 100)[0].alt for _ in range(30)]
    assert all(a != b for a, b in zip(seq, seq[1:])), seq
    assert len(set(seq)) == 3
    # Velocity layers: soft notes come from layer 1.
    assert "v1" in inst.pick(60, 20)[0].path.name and "v2" in inst.pick(60, 120)[0].path.name
    # Release sample at note off, attenuated by rt_decay.
    y = inst.render([{"t": 0, "m": 60, "v": 0.5, "d": 0.3}], 0.5)
    assert np.abs(y[:, int(0.301 * SR) : int(0.309 * SR)]).max() > 0.05
    # Choke: the hat (group 1, off_by 2) stops when key 91 (group 2) plays.
    y = inst.render([{"t": 0.0, "m": 90, "v": 1.0}, {"t": 0.5, "m": 91, "v": 1.0}], 1.0)
    one = inst.render([{"t": 0.0, "m": 90, "v": 1.0}], 1.0)
    assert np.abs(y[0, int(0.7 * SR)]) < np.abs(one[0, int(0.7 * SR)]) + 0.2 and np.abs(one[0, int(0.7 * SR)]) > 0.15
    # Sustain pedal holds the note off; long notes loop instead of stopping.
    held = inst.render([{"t": 0, "m": 60, "v": 1.0, "d": 0.1}], 1.0, pedal=[(0.0, 0.8)], releases=False)
    free = inst.render([{"t": 0, "m": 60, "v": 1.0, "d": 0.1}], 1.0, releases=False)
    assert np.abs(held[:, int(0.5 * SR) :]).max() > 5 * np.abs(free[:, int(0.5 * SR) :]).max()
    long = inst.render([{"t": 0, "m": 60, "v": 1.0, "d": 2.5}], 3.0, releases=False)
    assert np.abs(long[:, int(2.0 * SR) : int(2.4 * SR)]).max() > 0.01
    # Out of range notes move by octaves; folder loading reads names.
    assert inst.render([{"t": 0, "m": 30, "v": 1.0, "d": 0.2}], 0.3).any()
    fold = Instrument(load_folder(d / "s"))
    assert len(fold.regions) == 12
    assert fold.pick(66, 100)[0].center in (60, 72) and note_number("A#-1") == 10 and note_number("c4") == 60
    (d / "drum").mkdir()
    for v in (1, 2):
        for rr in (1, 2):
            sf.write(d / "drum" / f"BDrum_v{v}_rr{rr}_Sum.wav", np.stack([np.ones(4410) * 0.2 * v] * 2, 1), 44100)
    drum = Instrument(load_folder(d / "drum"))
    assert len(drum.regions) == 4 and all(r.one_shot and r.center == 60 for r in drum.regions)
    # Space: an IR adds a tail.
    ir = room_ir(0.8)
    x = np.zeros((2, SR))
    x[:, 100] = 1
    assert np.abs(convolve(x, ir, 0.5)[:, SR // 4 :]).max() > 1e-4
    print("sampler self test: ok")


def main() -> None:
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--test", action="store_true")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--demo", help="a kind from sampler_map.json, such as keys:piano or kick:punch")
    ap.add_argument("--out", default="sampler-demo.wav")
    a = ap.parse_args()
    if a.test:
        _self_test()
        return
    perf = Performer()
    if a.list:
        print(f"library: {perf.lib} ({'present' if perf.available else 'MISSING, run fetch_instruments.sh'})")
        for k, v in perf.map["kinds"].items():
            e = perf.entry(*k.split(":", 1))
            ok = perf.instrument(e["instrument"]) is not None
            print(f"  {k:22s} {e['instrument']:14s} {'ok' if ok else 'missing'}")
        return
    if a.demo:
        fam, kind = a.demo.split(":", 1)
        from dsp import Bus

        bus = {"x": Bus(4.0)}
        e = perf.entry(fam, kind)
        notes = [None] * 8 if "key" in e else [60, 62, 64, 67, 69, 67, 64, 72]
        for i, m in enumerate(notes):
            perf.note("x", fam, kind, 0.1 + i * 0.45, m, 0.45 + 0.07 * i, 0.4)
        perf.render(bus, 4.0)
        sf.write(a.out, bus["x"].x.T, SR, subtype="PCM_24")
        print(f"wrote {a.out}")


if __name__ == "__main__":
    sys.exit(main())
