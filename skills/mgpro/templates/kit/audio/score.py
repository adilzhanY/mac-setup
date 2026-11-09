"""
The film's score, built from its own sonic brief (src/music.json) and cue list (src/cues.json).
Writes public/film.wav at 48 kHz, 24 bit, the brief's loudness, true peak under -1 dBTP, exactly
the film.

    .venv/bin/python audio/score.py                 # this film (the folder above audio/)
    .venv/bin/python audio/score.py --root ../other  # another film folder

This file is the starting point for EVERY film, never an earlier film's synth. What makes the
film's music its own lives in music.json (genre, tempo, key, mode, palette, patterns, hook, form)
and in the per film hooks below (the JOBS map, special moments). Change them; do not paste in
another film's score.

What it does beyond playing the brief, from 129 measured professional films
(mgpro-research, real_films_measured.md):

  cue weight   hero cues get the full sound, support cues a small one, ambient cues a quiet one or
               nothing; only hero moments jump at the cut (pro films rise 1.2 to 1.7 times at a cut,
               the first AI films 18.6)
  variation    every effect event is a different take with pitch, level and layer variation (vary.py)
  feel         systematic microtiming: one timing and accent template per part that repeats every
               bar (hats and backbeat laid back, kick and every bar downbeat exact), a velocity
               contour over each phrase, and pushes of 5 to 15 ms only on phrase peaks and cadences
               (Feel); no independent random jitter per note
  breaths      a form section with "parts": ["dip"] is arranged, not a gain hole: drums, bass, hook
               and rhythmic parts stop, the chord and pad keep ringing with their reverb, and the
               level moves less than about 3 dB. Gain dips ("dips": "auto" or a list) are opt in
               only; the user heard the automatic -24 dB dips as the audio breaking
  opening      the first second about 2 LU under the whole (unless "opening": "cold")
  keep alive   the film stays busy until about 85 percent of its length
  beatless     "beat": false plays the form without drums, rubato
  samples      recorded instruments by default ("instruments": "samples", sampler.py,
               sampler_map.json, fetch_instruments.sh) for every part the map covers, in a convolved
               room, with a lighter pump; anything not covered, or no library, stays synth;
               "instruments": "synth" forces the synth
  master       darker (centroid near 1.8 kHz, rolloff near 4 kHz), low end carried by harmonics for
               small speakers, loudness range about 6 LU
"""

from __future__ import annotations

import argparse
import os
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

import dsp  # noqa: E402
import filmstats  # noqa: E402
import instruments as ins  # noqa: E402
import sampler  # noqa: E402
import sfx  # noqa: E402
from dsp import SR, Bus  # noqa: E402
from grooves import GENRES, VEL, hits, roll  # noqa: E402
from theory import Key, answer, motif, voice_lead  # noqa: E402
from vary import Vary  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
FPS = 60
# Where all three first AI films put their one gap (frame 825 of 1800): never again by habit.
AVOID = (0.458,)
# Share of the film's humanize spread each part gets: the kick stays tight, hats and comping loose.
HUMANIZE = {"kick": 0.3, "snare": 0.55, "hat": 1.0, "perc": 1.0, "bass": 0.45, "chords": 0.8, "hook": 0.7}


class Grid:
    """Tempo, meter and the form's section starts, in seconds and frames."""

    def __init__(self, brief: dict):
        g = GENRES[brief["genre"]]
        self.genre = g
        self.bpm = brief["bpm"]
        self.spb = brief.get("steps_per_beat", g.steps_per_beat)
        self.bpb = brief.get("beats_per_bar", g.beats_per_bar)
        self.beat = 60 / self.bpm
        self.step = self.beat / self.spb
        self.bar = self.beat * self.bpb
        self.sections = []
        t = 0.0
        prev = []
        for s in brief["form"]:
            parts = list(s.get("parts", []))
            if parts == ["dip"]:  # a dip section keeps the music going underneath, 20 dB down
                parts = prev + ["dip"]
            self.sections.append({**s, "parts": parts, "start": t, "end": t + s["bars"] * self.bar})
            prev = [p for p in parts if p not in ("crash", "fill", "dip", "silence")]
            t += s["bars"] * self.bar

    def frame(self, seconds: float) -> int:
        return int(round(seconds * FPS))


def drum_kind(role: str, palette: dict) -> tuple[str, str]:
    """(function, kind) for a drum role such as kick, snare, hat_open, conga."""
    kind = palette.get(role, role)
    if role.startswith("kick"):
        return "kick", kind
    if role in ("snare", "clap", "rim", "ghost", "snap"):
        return "snare", {"ghost": palette.get("snare", "tight")}.get(role, kind)
    if role.startswith("hat") or role in ("shaker", "tamb", "open", "ride"):
        return "hat", kind if kind in ("closed", "open", "ride", "shaker", "tamb", "909", "trap") else "closed"
    return "perc", kind


def play_drum(fn: str, kind: str, v: float):
    if fn == "kick":
        return ins.kick(kind, v)
    if fn == "snare":
        return ins.snare(kind, v)
    if fn == "hat":
        return ins.hat(kind, v)
    if kind in ("taiko",):
        return ins.kick("taiko", v)
    if kind == "log":
        return None  # the log drum is a pitched bass part, played by the bass line
    return ins.perc_hit(kind, v)


LIGHT_ROLES = ("shaker", "hat", "rim", "tamb", "hat_open", "conga", "perc", "bell")
# Kinds that exist only as samples (sampler_map.json) and what the synth plays in their place.
SYNTH_ALIAS = {"felt": "piano", "grand": "piano", "upright_piano": "piano", "cello": "sine", "violin": "sine", "pizz": "upright"}


def syn(kind: str) -> str:
    return SYNTH_ALIAS.get(kind, kind)


def performer(brief: dict):
    """The sampler for this brief, or None (synth). Samples are the default when the library is
    installed; "instruments": "synth" forces the synth; "samples_map" overrides kinds, such as
    {"keys:piano": "felt"}."""
    if brief.get("instruments", "samples") != "samples":
        return None
    perf = sampler.Performer(brief.get("seed", 1), brief.get("samples_map"))
    if not perf.available:
        print(f"  sampler: no instruments in {perf.lib} (run audio/fetch_instruments.sh); the synth plays everything")
        return None
    return perf


class Feel:
    """How the players lean, decided once per film and kept: a timing template per part that
    repeats every bar (systematic microtiming, as real players have: hats and the backbeat a few
    ms behind, the kick and every bar downbeat on the grid), an accent template per part, a
    velocity contour that rises and falls over each phrase, and small pushes (5 to 15 ms early)
    only where a phrase peaks or cadences. humanize_ms sets the size; HUMANIZE the share per part."""

    LEAN = {"kick": 0.1, "snare": 0.7, "hat": 0.6, "perc": 0.5, "bass": 0.25, "chords": 0.45, "hook": 0.35}

    def __init__(self, brief: dict, grid: Grid):
        rng = np.random.default_rng(brief.get("seed", 1) + 303)
        self.grid, self.steps = grid, grid.spb * grid.bpb
        self.phrase = brief.get("phrase_bars", 4)
        ms = brief.get("humanize_ms", 12) / 1000
        k = np.arange(self.steps)
        pos = k % grid.spb
        self.tpl, self.acc = {}, {}
        for part, share in HUMANIZE.items():
            off = (self.LEAN[part] + rng.normal(0, 0.45, self.steps)) * share * ms * np.where(pos == 0, 0.5, 1.0)
            off = np.clip(off, -0.5 * share * ms, 2 * share * ms)  # lean late; early reads worse
            off[0] = 0.0  # the bar downbeat stays exact
            self.tpl[part] = off
            acc = np.where(k == 0, 1.06, np.where(pos == 0, 1.0, np.where(pos == grid.spb // 2, 0.93, 0.87)))
            self.acc[part] = acc * (1 + rng.normal(0, 0.03, self.steps))  # each part's own hand, fixed
        self.rng = np.random.default_rng(brief.get("seed", 1) + 304)

    def contour(self, bar: int, step: int, depth=0.12) -> float:
        x = ((bar % self.phrase) + step / self.steps) / self.phrase
        return 1 - depth / 2 + depth * float(np.sin(np.pi * x))

    def push(self) -> float:
        return -float(self.rng.uniform(0.005, 0.015))

    def cadence(self, bar: int) -> bool:
        return bar % self.phrase == self.phrase - 1

    def hits(self, pattern: str, t0: float, part: str, bar: int, swing: float, depth=0.08):
        """grooves.hits on the grid, then this part's template and the phrase contour."""
        idx = [i for i, ch in enumerate(pattern) if VEL.get(ch, 0.0) > 0]
        out = []
        for i, (t, v) in zip(idx, hits(pattern, t0, self.grid.step, swing, self.grid.spb)):
            s = i % self.steps
            v *= self.acc[part][s] * self.contour(bar, s, depth) * (1 + self.rng.normal(0, 0.02))
            out.append((t + self.tpl[part][s], max(0.05, v)))
        return out


def render(brief: dict, cues: list[dict], seconds: float) -> tuple[np.ndarray, Grid]:
    """The music, unlevelled: every section at full level. levels() gives the form's level curve."""
    dsp.seed(brief.get("seed", 1))
    rng = np.random.default_rng(brief.get("seed", 1))
    grid = Grid(brief)
    g = grid.genre
    key = Key(brief["key"], brief["mode"])
    beat = brief.get("beat", True)
    palette = {**g.palette, **brief.get("palette", {})}
    patterns = {**g.drums, **brief.get("drums", {})} if beat else {}
    swing = brief.get("swing", g.swing)
    feel = Feel(brief, grid)
    prog = brief.get("progression") or key.progression(brief.get("mood", g.moods[0]), brief.get("progression_variant", 0))
    chords = voice_lead([key.chord(r, 4 if brief.get("sevenths", True) else 3) for r in prog], centre=brief.get("chord_centre", 62))
    harm_bars = brief.get("bars_per_chord", 1)
    hook_cfg = brief.get("hook", {})
    hook = motif(key, hook_cfg.get("seed", 3), hook_cfg.get("contour", "arch"), hook_cfg.get("notes", 6),
                 low=hook_cfg.get("low", 67), bar_steps=grid.spb * grid.bpb, rhythm=hook_cfg.get("rhythm"))
    reply = answer(hook, key)
    keep_alive = brief.get("keep_alive", True)
    light = next((r for r in LIGHT_ROLES if r in patterns), None)

    buses = {k: Bus(seconds) for k in ("kick", "drums", "bass", "chords", "pad", "hook", "fx", "bed")}
    perf = performer(brief)
    pedal = []  # sustain pedal for sampled keys: down on each chord, up just before the next
    hero_sec = max(grid.sections, key=lambda s: s.get("energy", 0))
    kick_times = []

    for sec in grid.sections:
        parts = set(sec.get("parts", []))
        energy = sec.get("energy", 0.7)
        if "silence" in parts:
            continue
        breath = "dip" in parts
        if breath:  # an arranged breath: the rhythm stops, the harmony keeps ringing
            energy = max(energy, 0.4)
            parts = {"pad"} | ({"chords"} if "chords" in parts else set())
        for b in range(int(np.ceil(sec["bars"]))):
            t0 = sec["start"] + b * grid.bar
            inside = lambda hs: [(t, v) for t, v in hs if t < sec["end"] - 0.01]  # noqa: E731
            bar_index = int(round(t0 / grid.bar))
            chord = chords[(bar_index // harm_bars) % len(chords)]
            root = min(chord) - 12
            while root > 45:
                root -= 12
            last_bar = b == int(np.ceil(sec["bars"])) - 1
            drums_here = "drums" in parts or any(r in parts for r in patterns)
            # Keep the film busy until about 85 percent: a drumless bar there gets the lightest part.
            alive = keep_alive and not drums_here and not breath and 0.55 * seconds <= t0 < 0.85 * seconds

            # Drums: every part named in the section plays its pattern ("drums" plays them all).
            for role, pat in patterns.items():
                if alive and role == light:
                    pass
                elif (role not in parts and "drums" not in parts) or f"-{role}" in parts:
                    continue
                spb = len(pat) // max(1, len(pat) // (grid.spb * grid.bpb))
                bar_pat = pat[(b % max(1, len(pat) // spb)) * spb :][:spb]
                fn, kind = drum_kind(role, palette)
                for t, v in inside(feel.hits(bar_pat, t0, fn, bar_index, swing, 0.06)):
                    vv = v * (0.6 + 0.4 * energy) * (0.55 if alive else 1.0)
                    name = "kick" if fn == "kick" else "drums"
                    gain = {"kick": 1.0, "hat": 0.4}.get(fn, 0.55)
                    sampled = perf is not None and perf.has(fn, kind)
                    s = None if sampled else play_drum(fn, kind, vv)
                    if s is None and not sampled:
                        continue
                    pan = {"hat": 0.25, "perc": rng.uniform(-0.5, 0.5)}.get(fn, 0.0)
                    if sampled:
                        perf.note(name, fn, kind, t, None, vv, 0.0, gain, pan)
                    else:
                        buses[name].add(s, t, gain, pan)
                    if fn == "kick":
                        kick_times.append(t)
            if alive and not beat:  # a beatless film stays alive with a few grains instead
                buses["fx"].add(sfx.texture(grid.bar, brief.get("character", "glass"), key, 0.35, int(rng.integers(1 << 30)), 6), t0, 0.5)
            if beat and "fill" in parts and last_bar:
                for t, v in roll(t0 + grid.beat * (grid.bpb - 1), grid.beat, grid.step / 2):
                    if not (perf and perf.note("drums", "snare", palette.get("snare", "tight"), t, None, v * 0.6, 0.0, 0.5)):
                        buses["drums"].add(ins.snare(palette.get("snare", "tight"), v * 0.6), t, 0.5)
            if beat and g.extra.get("hat_rolls") and "drums" in parts and b % 2 == 1:
                for t, v in roll(t0 + grid.beat * (grid.bpb - 1) + grid.step * 2, grid.step * 2, grid.step / 3, 0.3, 0.6):
                    if not (perf and perf.note("drums", "hat", "trap", t, None, v, 0.0, 0.4, 0.25)):
                        buses["drums"].add(ins.hat("trap", v), t, 0.4, 0.25)

            # Bass: the genre's rhythm on the chord root; octave kinds jump on accented steps. A
            # beatless film holds one long note per chord.
            if "bass" in parts:
                kind = palette.get("bass", g.bass["kind"])
                if not beat:
                    if b % harm_bars == 0:
                        d = min(grid.bar * harm_bars, sec["end"] - t0)
                        tb = t0 + rng.uniform(0, 0.04)
                        if not (perf and perf.note("bass", "bass", "sub", tb, root, 0.8, d)):
                            buses["bass"].add(ins.bass("sub", root, d, 0.8, cut=0.6 + 0.4 * energy), tb, 1.0)
                else:
                    bpat = brief.get("bass_rhythm", g.bass["rhythm"])
                    prev = None
                    for i, (t, v) in enumerate(inside(feel.hits(bpat[: grid.spb * grid.bpb], t0, "bass", bar_index, swing))):
                        m = root + (12 if kind == "octave" and i % 2 else 0)
                        if kind == "log" and i % 3 == 2:
                            m = root + 7
                        dur = grid.step * (2 if kind not in ("808", "reese") else 6)
                        prev, last = m, prev
                        if perf and perf.note("bass", "bass", kind, t, m, v, dur):
                            continue
                        s = ins.bass(syn(kind), m, dur, v, glide_from=last if kind in ("808", "acid", "log") and last != m else None,
                                     cut=0.6 + 0.6 * energy, accent=v > 0.9)
                        buses["bass"].add(s, t, 1.0)

            # Chords in the genre's style (beatless: one rubato strum per chord).
            if "chords" in parts:
                style = brief.get("chord_style", g.chords["style"]) if beat and not breath else "rubato"
                kind = palette.get("keys", g.chords["kind"])
                cpat = brief.get("chord_rhythm", g.chords["rhythm"])[: grid.spb * grid.bpb]
                keyed = syn(kind) in ins.KEY_KINDS
                if style == "rubato":
                    if b % harm_bars == 0 and keyed:
                        d, spread, tc = grid.bar * harm_bars * 0.9, rng.uniform(0.02, 0.06), t0 + rng.uniform(0.01, 0.09)
                        if perf and perf.chord("chords", "keys", kind, tc, chord, 0.6, d, 0.5, spread):
                            pedal.append((tc + 0.05, tc + grid.bar * harm_bars - 0.03))
                        else:
                            buses["chords"].add(ins.strum(syn(kind), chord, d, 0.6, spread=spread, cut=0.4 + 0.5 * energy), tc, 0.5)
                elif style in ("stabs", "comp"):
                    hs = inside(feel.hits(cpat, t0, "chords", bar_index, swing, 0.12))
                    if hs and feel.cadence(bar_index):  # the cadence chord leans ahead
                        hs[-1] = (hs[-1][0] + feel.push(), hs[-1][1])
                    for t, v in hs:
                        d = grid.step * (1.5 if style == "stabs" else 3)
                        if perf and perf.chord("chords", "keys" if keyed else "stab", kind, t, chord, v * 0.8, d, 0.5):
                            continue
                        if keyed:
                            s = ins.strum(syn(kind), chord, d, v * 0.8, cut=0.4 + 0.6 * energy)
                        else:  # a pad sound played short: string or saw stabs
                            s = ins.pad(kind, chord, d, cut=1500 + 3000 * energy, attack=0.004, v=v * 1.4)
                        buses["chords"].add(s, t, 0.5)
                elif style == "ostinato":
                    tones = chord + [chord[0] + 12]
                    for i, (t, v) in enumerate(inside(feel.hits(cpat, t0, "chords", bar_index, swing, 0.12))):
                        m, pan = tones[i % len(tones)], (i % 2) * 0.6 - 0.3
                        if perf and perf.note("chords", "ostinato", kind, t, m, v * 0.6, grid.step * 0.9, 0.4, pan):
                            continue
                        s = ins.lead("pluck", m, grid.step * 0.9, v * 0.6, cut=0.5 + 0.5 * energy)
                        buses["chords"].add(s, t, 0.4, pan)
            if "pad" in parts and b % harm_bars == 0:
                kind = palette.get("pad", "warm")
                d = min(grid.bar * harm_bars, sec["end"] - t0)
                att = 0.08 if breath else min(0.6, grid.beat)  # a breath's chord must sound at once
                if not (perf and perf.chord("pad", "pad", kind, t0, chord, 0.35 + 0.5 * energy, d, 0.35, 0.03, 0.7, attack=att)):
                    s = ins.pad(kind, chord, d, cut=900 + 3000 * energy, attack=att)
                    buses["pad"].add(s, t0, 0.35)

            # The hook: call on even bars, answer on odd bars; loose in time, never machine exact.
            if "hook" in parts or "hook_sparse" in parts:
                if "hook_sparse" in parts and b % 2 == 1:
                    continue
                phrase = hook if b % 2 == 0 else reply
                kind = palette.get("lead", "pluck")
                peak = max(m for _, _, m in phrase)
                for j, (st, ln, m) in enumerate(phrase):
                    t = t0 + st * grid.step + ((2 * swing - 1) * grid.step if st % 2 and grid.spb % 2 == 0 else 0)
                    if beat:  # the template, plus a push on the phrase's peak note and on its cadence
                        t += feel.tpl["hook"][st % feel.steps]
                        if m == peak or (j == len(phrase) - 1 and b % 2 == 1):
                            t += feel.push()
                    else:  # beatless: rubato, the phrase breathes freely
                        t += rng.uniform(0.0, 0.035)
                    if t >= sec["end"] - 0.01:
                        continue
                    d = ln * grid.step * (1.0 if beat else 1.6)
                    vv = 0.7 * feel.contour(bar_index, st % feel.steps, 0.16) * (1 + feel.rng.normal(0, 0.03))
                    keyed = syn(kind) in ins.KEY_KINDS and kind not in ("organ", "clav")
                    if perf and perf.note("hook", "keys" if keyed else "lead", kind, t, m, min(1.0, vv + (0.1 if keyed else 0)), d):
                        continue
                    if kind == "fold":
                        s = ins.fold_lead(m, d, vv)
                    elif keyed:
                        s = ins.keys(syn(kind), m, d, vv + 0.1)
                    else:
                        s = ins.lead(syn(kind), m, d, vv, vowel="aeiou"[st % 5])
                    buses["hook"].add(s, t, 0.5, 0.0)

        if "crash" in parts and (sec.get("hero") or sec is hero_sec):  # one crash for the big moment, not every section
            if beat and not (perf and perf.note("fx", "crash", "crash", sec["start"], None, 0.7, 0.0, 0.25)):
                buses["fx"].add(ins.crash(0.7), sec["start"], 0.25)
            else:  # beatless: a swell into the section instead of a hit on it
                buses["fx"].add(sfx.reverse_swell(min(2.0, grid.bar), 0.5, int(rng.integers(1 << 30))), sec["start"] - min(2.0, grid.bar), 0.4)

    # The bed: quiet percussive grains off the grid between the hits (rule 12 of the film study: pro
    # films carry 0.2 to 0.5 of their energy in transients, spread evenly; a synth groove alone is
    # spiky, 0.1, so every downbeat towers over the gaps and every cut on one reads as a slam).
    bed = brief.get("bed", 0.5 if beat else 1.5)  # a beatless film's cuts are carried by its texture
    if bed:
        ch = brief.get("character", "glass")
        grains = [sfx.tap(ch, 1, 0.0, 900 + k) for k in range(6)] + [sfx.tick(ch, 0.8 + 0.1 * k, 1, 950 + k) for k in range(4)]
        for sec in grid.sections:
            if "silence" in sec.get("parts", []) or sec.get("energy", 0.7) < 0.25:
                continue
            rate = brief.get("bed_rate", 7 if beat else 10) * (0.5 + sec.get("energy", 0.7))
            for t in np.sort(rng.uniform(sec["start"], sec["end"], int(rate * (sec["end"] - sec["start"])))):
                k, lvl, pan = int(rng.integers(len(grains))), rng.uniform(0.15, 0.6), rng.uniform(-0.7, 0.7)
                # sampled: the grains are real hand percussion played very softly
                if not (perf and perf.note("bed", "bed", "grain", t, None, lvl, 0.0, 1.0, pan)):
                    buses["bed"].add(grains[k], t, lvl, pan)

    # Mix: each bus its treatment, the musical buses pumping under the kick. Sampled parts sit in
    # a convolved room instead of the synthetic reverbs and chorus, and pump far less (players do
    # not duck under the kick).
    n = buses["kick"].n
    if perf:
        # Musical cues: real notes on a sampled instrument at a picture frame (a sonic logo, rooms
        # filling as notes of the chord). {"sound": "notes", "family": "keys", "kind": "marimba",
        # "notes": [65, 69, 72], "spread": 0.09, "v": 0.7, "d": 0.8, "bus": "hook", "accent": [..]};
        # spread is the time between notes in seconds (0 plays a chord).
        for c in cues:
            if c.get("sound") != "notes":
                continue
            t0 = c["frame"] / FPS
            fam, kind = c.get("family", "keys"), c.get("kind", "marimba")
            acc = c.get("accent", [1.0])
            for j, m in enumerate(c["notes"]):
                perf.note(c.get("bus", "hook"), fam, kind, t0 + c.get("spread", 0.0) * j, m, c.get("v", 0.7) * acc[j % len(acc)], c.get("d", 0.6), c.get("gain", 1.0), c.get("pan", 0.0))
        perf.render(buses, seconds, {"chords": pedal, "hook": []})
    duck = dsp.duck_curve(n, kick_times, depth=brief.get("pump", 0.12 if perf else 0.4)) if kick_times else np.ones(n)
    if perf:
        buses["kick"].x = perf.space(buses["kick"].x, "drums", 0.12)
        drums = dsp.lp(perf.space(buses["drums"].x, "drums", 0.3), 12000)
        chords_x = perf.space(buses["chords"].x, "room", 0.3) * duck
        pad_x = perf.space(buses["pad"].x, "hall", 0.45) * duck
        hook_x = perf.space(dsp.pingpong(buses["hook"].x, grid.beat * 0.75, 0.25, 0.15), "hall", 0.35) * duck**0.5
        bed_x = perf.space(buses["bed"].x, "room", 0.3) * bed * 0.25
    else:
        drums = dsp.lp(dsp.room(buses["drums"].x, 0.25, 0.08), 11000)
        chords_x = dsp.chorus(dsp.room(buses["chords"].x, 0.5, 0.18), 0.5, 0.2, 0.3) * duck
        pad_x = dsp.hall(buses["pad"].x, 0.3) * duck
        hook_x = dsp.pingpong(buses["hook"].x, grid.beat * 0.75, 0.35, 0.25)
        hook_x = dsp.room(hook_x, 0.45, 0.15) * duck**0.5
        bed_x = dsp.room(dsp.lp(buses["bed"].x, 7000), 0.35, 0.2) * bed * 0.25
    bass = dsp.comp(buses["bass"].x, -20, 3, 4, 90) * duck**1.3
    music = buses["kick"].x + drums + bass + chords_x + pad_x + hook_x + buses["fx"].x + bed_x
    if g.extra.get("vinyl"):
        music += dsp.stereo(ins.vinyl(seconds, 0.4))[:, :n]
    if g.extra.get("wow") or brief.get("wow"):
        music = dsp.wow(music)
    music = dsp.balance(music, **brief.get("balance", {}))
    return music, grid


def energy_curve(grid: Grid, n: int) -> tuple[np.ndarray, np.ndarray]:
    """(energy 0 to 1 per sample, silence mask), ramped over 20 ms so nothing clicks. A breath
    ("dip") keeps the level of the section before it: it is thinner, not quieter."""
    e = np.zeros(n)
    silent = np.zeros(n, bool)
    prev = 0.7
    for sec in grid.sections:
        a, b = int(sec["start"] * SR), min(n, int(sec["end"] * SR))
        breath = "dip" in sec.get("parts", [])
        e[a:b] = prev if breath else sec.get("energy", 0.7)
        prev = e[a] if b > a else prev
        silent[a:b] = "silence" in sec.get("parts", [])
    k = int(0.02 * SR)
    return np.convolve(e, np.ones(k) / k, mode="same"), silent


def breath_guard(mix: np.ndarray, grid: Grid, most_db: float = 3.0) -> np.ndarray:
    """Keep every breath within most_db of the bar before it: when the ringing chord and tails
    measure quieter than that, the breath is lifted (40 ms ramps), so it never reads as a hole."""
    n = mix.shape[1]
    g = np.ones(n)
    for i, sec in enumerate(grid.sections):
        if i == 0 or "dip" not in sec.get("parts", []):
            continue
        a, b = int(sec["start"] * SR), min(n, int(sec["end"] * SR))
        r = max(0, a - int(grid.bar * SR))
        if b - a < int(0.05 * SR) or a - r < int(0.05 * SR):
            continue
        lift = (dsp.rms_db(mix[:, r:a]) - (most_db - 0.5)) - dsp.rms_db(mix[:, a:b])
        if lift > 0:
            g[a:b] = 10 ** (min(lift, 12.0) / 20)
    k = int(0.04 * SR)
    g = np.convolve(g, np.ones(k) / k, mode="same")
    return mix * g


def plan_dips(brief: dict, grid: Grid, seconds: float, cuts=()) -> list[dict]:
    """Gain dips, opt in only ("dips": "auto" or a list; the default 0 plans none, because the user
    heard -24 dB dips as the audio breaking). Form sections with "parts": ["dip"] are arranged
    breaths instead (render, breath_guard). "auto": about 20 dB down for about 0.3 s, a breath in the opening, one before the end card, one before
    the loudest section (the re-entry, with a quieter bar before it so the return is about 9 dB
    up), and more at bar lines, about one per 7 s in all. Each dip ends a seeded 20 to 70 ms before
    its bar line, so the first hit comes that much after the dip. Only the main dip may end on a cut:
    a dip before every cut is the pre-hit duck that made the first AI films slam their cuts. Section
    starts count as cuts too. Positions follow the form and the seed, so two films do not dip in the
    same places."""
    rng = np.random.default_rng(brief.get("seed", 1) + 101)
    spec = brief.get("dips", 0)
    if not spec:
        return []
    bar = grid.bar
    dips = []

    starts = [s["start"] for s in grid.sections[1:] if "silence" not in s.get("parts", [])]
    busy = list(cuts) + starts

    def add(end, length, main=False):
        if end - length < 0.2 or end > seconds - 0.3:
            return
        if not main and any(abs(end - c) < 0.6 * grid.beat for c in busy):
            return
        if any(abs(end - d["end"]) < 1.5 * bar for d in dips):
            return
        if any(abs((end - length) / seconds - a) < 0.02 for a in AVOID):
            return
        dips.append({"end": end, "length": length, "main": main, "reentry": float(rng.uniform(0.02, 0.07)), "pre_db": float(rng.uniform(5, 8))})

    # "dip" sections are arranged breaths (render, breath_guard), never gain dips.
    if isinstance(spec, list):
        for d in spec:
            end = grid.sections[[s["name"] for s in grid.sections].index(d["at"])]["start"] if "at" in d else d["bar"] * bar
            add(end, d.get("len", 0.3), d.get("main", False))
        return sorted(dips, key=lambda d: d["end"])
    lines = list(np.arange(bar, seconds - 0.5, bar)) + list(np.arange(bar / 2, seconds - 0.5, bar))
    hero = max(grid.sections[1:], key=lambda s: s.get("energy", 0), default=None)
    if hero and not any(d["main"] for d in dips):
        add(hero["start"], float(rng.uniform(0.22, 0.45)), True)
    early = [t for t in lines if 0.05 * seconds <= t <= 0.16 * seconds]
    for t in rng.permutation(early):
        if len(dips) < (2 if any(d["main"] for d in dips) else 1):
            add(float(t), float(rng.uniform(0.18, 0.4)))
    for t in sorted([t for t in lines if 0.84 * seconds <= t <= 0.96 * seconds], key=lambda t: abs(t - 0.9 * seconds)):
        n0 = len(dips)
        add(float(t), float(rng.uniform(0.2, 0.45)))
        if len(dips) > n0:
            break
    want = max(2, int(round(seconds / 10 * rng.uniform(1.1, 1.7))))
    middle = [t for t in lines if 0.16 * seconds < t < 0.86 * seconds]
    rng.shuffle(middle)
    for t in middle:
        if len(dips) >= want:
            break
        add(float(t), float(np.clip(rng.lognormal(np.log(0.28), 0.35), 0.16, min(0.6, 0.45 * bar))))
    return sorted(dips, key=lambda d: d["end"])


def dip_curve(dips: list[dict], n: int, depth_db: float = -24.0) -> np.ndarray:
    """Gain per sample: each dip depth_db down with 15 ms ramps; before a main dip a bar long slide
    down by its pre_db, so the music comes back about 9 dB louder than it left."""
    g = np.zeros(n)  # in dB
    for d in dips:
        a, b = int((d["end"] - d["reentry"] - d["length"]) * SR), int((d["end"] - d["reentry"]) * SR)
        g[max(0, a) : min(n, b)] = depth_db
        if d["main"]:
            k = int(min(2.0, d.get("bar", 1.6)) * SR)
            lo = max(0, a - k)
            g[lo:a] = np.minimum(g[lo:a], -d["pre_db"] * np.linspace(0, 1, a - lo) ** 1.5)
    k = int(0.015 * SR)
    g = np.convolve(g, np.ones(k) / k, mode="same")
    return 10 ** (g / 20)


# --- Per film: effects -------------------------------------------------------------------------
# Every cue name maps to a job; every job is its own designed sound (sfx.py), never one sound for
# many events. (job, default level, kind of variation, where the sound sits on its frame).
JOBS = {
    "tap": (0.5, "noisy", "start"), "click": (0.5, "noisy", "start"), "tick": (0.3, "noisy", "start"),
    "blip": (0.45, "tonal", "start"), "pop": (0.45, "tonal", "start"), "text": (0.35, "tonal", "start"),
    "toggle": (0.45, "tonal", "start"), "card": (0.7, "impact", "start"), "chip": (0.55, "tonal", "start"),
    "land": (0.7, "impact", "start"), "impact": (0.9, "impact", "start"), "boom": (1.0, "impact", "start"),
    "swish": (0.45, "whoosh", "peak"), "whoosh": (0.55, "whoosh", "peak"), "airy": (0.4, "whoosh", "peak"),
    "transition": (0.7, "whoosh", "peak"), "panel_open": (0.4, "noisy", "end"), "panel_close": (0.4, "noisy", "start"),
    "success": (0.5, "bell", "start"), "error": (0.5, "tonal", "start"), "tier": (0.6, "bell", "start"),
    "logo": (0.75, "bell", "start"), "riser": (0.5, "noisy", "end"), "reverse": (0.5, "noisy", "end"),
    "sub_drop": (0.7, "impact", "start"), "texture": (0.3, "noisy", "loose"),
}
# Cue names used by earlier films and their job.
ALIASES = {"place": "chip", "block": "chip", "word": "text", "type": "text", "switch": "toggle", "open": "panel_open",
           "close": "panel_close", "panel": "panel_open", "chime": "success", "done": "success", "bell": "logo",
           "hit": "impact", "final": "impact", "sub": "sub_drop", "count": "tick", "grain": "tick", "key": "tap"}
WEIGHT_GAIN = {"hero": 1.0, "support": 0.4, "ambient": 0.16}
# Sounds with a hard attack. On an ordinary cut (marked "cut" but not hero) they drop to ambient:
# the music carries ordinary cuts, only structural ones get a hit (real_films_measured.md rule 13).
TRANSIENT = {"tap", "click", "card", "chip", "land", "impact", "boom", "toggle", "pop", "transition", "tier", "error"}
DEFAULT_WEIGHT = {"logo": "hero", "boom": "hero", "texture": "ambient", "tick": "ambient"}


def make(job: str, c: dict, key: Key, ch: str, weight: str):
    """A function seed -> sound for one cue. Support impacts are smaller and lose the long sub."""
    i, sec = c.get("index", 0), c.get("seconds")
    size = c.get("size", 0.3 if job == "tap" else 0.5)
    size = {"light": 0.2, "heavy": 0.9}.get(size, 0.5) if isinstance(size, str) else float(size)
    if job in ("impact", "boom") and weight != "hero":
        size = min(size, 0.55)
    return {
        "tap": lambda s: sfx.tap(ch, 1, size, s),
        "click": lambda s: sfx.click(ch, 1, s),
        "tick": lambda s: sfx.tick(ch, 1 + i / 40, 1, s),
        "blip": lambda s: sfx.blip(key, i, ch, 1, s),
        "pop": lambda s: sfx.pop(key, i, ch, 1, s),
        "text": lambda s: sfx.text(key, i, ch, 1, s),
        "toggle": lambda s: sfx.toggle(key, c.get("on", True), ch, 1, s),
        "card": lambda s: sfx.card(ch, 1, size, s),
        "chip": lambda s: sfx.chip(key, i, ch, 1, s),
        "land": lambda s: sfx.land(ch, size, key, i, 1, s),
        "impact": lambda s: sfx.impact(ch, 1, max(size, 0.8) if weight == "hero" else size, s),
        "boom": lambda s: sfx.boom(ch, 1, s) if weight == "hero" else sfx.impact(ch, 1, size, s),
        "swish": lambda s: sfx.swish(sec or 0.12, ch, 1, s, c.get("direction", 1)),
        "whoosh": lambda s: sfx.whoosh(sec or 0.4, ch, 1, s, size, c.get("air", False), None, c.get("direction", 1)),
        "airy": lambda s: sfx.whoosh(sec or 0.8, ch, 1, s, air=True, direction=c.get("direction", 1)),
        "transition": lambda s: sfx.transition(sec or 0.35, ch, 1, s, size),
        "panel_open": lambda s: sfx.panel(True, ch, 1, sec or 0.3, s),
        "panel_close": lambda s: sfx.panel(False, ch, 1, sec or 0.3, s),
        "success": lambda s: sfx.success(key, ch, 1, s),
        "error": lambda s: sfx.error(key, ch, 1, s),
        "tier": lambda s: sfx.tier(key, i, ch, 1, s),
        "logo": lambda s: sfx.logo(key, ch, 1, s, c.get("notes")),
        "riser": lambda s: sfx.riser(key, sec or 1.5, ch, 1, s),
        "reverse": lambda s: sfx.reverse_swell(sec or 1.0, 1, s),
        "sub_drop": lambda s: sfx.sub_drop(sec or 1.2, 1),
        "texture": lambda s: sfx.texture(sec or 1.0, ch, key, 1, s),
    }[job]


SFX_LIB = Path(os.environ.get("MGPRO_SFX", Path.home() / ".local/share/mgpro/sfx"))
USED_FILES: set[str] = set()


def copy_found(root: Path) -> int:
    """Every found recording a cue played ("file"), copied into the film's public/sfx with a
    licence line in public/sfx/ASSETS.txt (references/rights.md). Files already in public/ stay."""
    import shutil

    d = root / "public" / "sfx"
    d.mkdir(parents=True, exist_ok=True)
    out = d / "ASSETS.txt"
    lines = out.read_text().splitlines() if out.exists() else ["file | pack | source page | licence"]
    n = 0
    for f in sorted(USED_FILES):
        if (root / "public" / f).exists():
            continue
        src = SFX_LIB / f
        name = f.replace("/", "__")
        shutil.copy2(src, d / name)
        pack = f.split("/")[0]
        lic = "CC0 1.0" if pack.startswith(("kenney", "oga", "remotion")) else "see the pack's licence file"
        line = f"public/sfx/{name} | {pack} | see sfx/README.md | {lic}"
        if line not in lines:
            lines.append(line)
            n += 1
    out.write_text("\n".join(lines) + "\n")
    return n


def recording(path: str) -> np.ndarray:
    """A downloaded recording for a cue's "file": looked up in the film's public/ folder, then in the
    CC0 library. The silence before its first transient is cut (a click file with 120 ms of lead
    lands 7 frames late otherwise), the peak is normalised, the tail gets a 5 ms fade."""
    import soundfile as sf
    for base in (ROOT / "public", SFX_LIB, Path("/")):
        p = base / path
        if p.exists():
            break
    else:
        raise FileNotFoundError(path)
    x, sr = sf.read(str(p), always_2d=True)
    x = x.T.astype(np.float64)
    if sr != SR:
        from scipy.signal import resample_poly
        x = resample_poly(x, SR, sr, axis=1)
    a = np.abs(x).max(axis=0)
    start = max(0, int(np.argmax(a > a.max() * 0.08)) - int(0.002 * SR))
    x = x[:, start:]
    x /= max(np.abs(x).max(), 1e-6)
    fade = min(x.shape[1], int(0.005 * SR))
    x[:, -fade:] *= np.linspace(1, 0, fade)
    return x if x.shape[0] == 2 else np.vstack([x[0], x[0]])


def effects(cues: list[dict], seconds: float, key: Key, character: str, vary: Vary, samples=None) -> np.ndarray:
    """Every cue placed on its frame through the weight hierarchy, each event a different take."""
    bus = Bus(seconds)
    heroes = 0
    for c in cues:
        name = c["sound"]
        if name in ("gap", "stop", "notes"):
            continue  # handled by the form, or played by the sampler with the music
        job = ALIASES.get(name, name)
        if job not in JOBS:
            print(f"  no sound designed for cue '{name}': add it to JOBS and make() in score.py")
            continue
        level, kind, anchor = JOBS[job]
        weight = c.get("weight", DEFAULT_WEIGHT.get(job, "support"))
        story = bool(c.get("story"))
        if c.get("cut") and weight == "support" and job in TRANSIENT and not story:
            weight = "ambient"
        if story and weight == "ambient":
            weight = "support"  # an action the story turns on (a click that opens the next scene) is never background
        heroes += weight == "hero"
        if weight == "ambient" and vary.rng.random() < 0.35:
            continue  # ambient events may get nothing: background motion does not need a sound each
        ch = c.get("material", character)
        argkey = (job, ch, c.get("index", 0), c.get("seconds"), c.get("size"), c.get("on"), weight, c.get("file"))
        if c.get("file"):
            files = c["file"] if isinstance(c["file"], list) else [c["file"]]
            pick = files[vary.take(f"file:{job}:{'|'.join(files)}", len(files))] if len(files) > 1 else files[0]
            USED_FILES.add(pick)
            s = vary.play(job, lambda seed, f=pick: recording(f), "sample", key=(*argkey[:-1], pick))
        else:
            s = vary.play(job, make(job, c, key, ch, weight), kind, key=argkey)
        sjob = job if job != "whoosh" else "airy" if c.get("air") else "swish" if (c.get("seconds") or 0.4) <= 0.18 else "whoosh"
        if samples is not None and samples.wants(sjob) and not c.get("file"):
            smp = samples.play(sjob)
            if sjob in samples.layer:
                s = dsp.stereo(s)
                L = max(s.shape[1], smp.shape[1])
                s = np.pad(s, ((0, 0), (0, L - s.shape[1]))) + 0.5 * np.pad(smp, ((0, 0), (0, L - smp.shape[1])))
            else:
                s = smp
        if story:
            s = dsp.hp(s, c.get("hp", 170))  # a story sound must read on a phone: no energy it cannot play
        t = c["frame"] / FPS
        if anchor == "peak":
            t -= sfx.peak_index(s) / SR
        elif anchor == "end":
            t -= s.shape[-1] / SR
        t += vary.offset(weight == "ambient" or anchor == "loose" or c.get("loose", False))
        pan = c.get("pan", float(vary.rng.uniform(-0.25, 0.25))) if s.ndim == 1 else 0.0
        bus.add(s, t, level * WEIGHT_GAIN[weight] * c.get("gain", 1.0), pan)
    if heroes > max(2, seconds / 8):
        print(f"  {heroes} hero cues in {seconds:.0f} s: keep full hits for the title, the reveal and the end card")
    return dsp.room(bus.x, 0.3, 0.1)


def loudness(x) -> dict:
    return filmstats.loudness(filmstats._load(x, SR))


def build(brief: dict, cues: list[dict], seconds: float, root: Path | None = None, verbose: bool = True):
    """Music, effects, form levels, dips, opening and master. Returns (master, grid, dips)."""
    say = print if verbose else (lambda *a, **k: None)
    seed = brief.get("seed", 1)
    music, grid = render(brief, cues, seconds)
    key = Key(brief["key"], brief["mode"])
    vary = Vary(seed, brief.get("pool", 4))
    smp = None
    scfg = brief.get("samples", {})
    if scfg.get("enabled") and root is not None:
        from samples import Samples

        smp = Samples(seed, root, vary, scfg.get("jobs", "all"), scfg.get("layer", []))
    fxs = effects(cues, seconds, key, brief.get("character", "glass"), vary, smp)
    if smp is not None and smp.write_assets():
        say(f"  samples: {len(smp.used)} files copied to public/sfx, listed in public/sfx/ASSETS.txt")
    n = music.shape[1]
    # Story sounds cut through by the music stepping aside, as an editor ducks it: about 3 dB from
    # 20 ms before the sound, back over about 150 ms ("story_duck_db", 0 turns it off).
    sd = brief.get("story_duck_db", 3.0)
    story_duck = dsp.duck_curve(n, [c["frame"] / FPS - 0.02 for c in cues if c.get("story")], depth=1 - 10 ** (-sd / 20), attack=0.015, release=0.05) if sd else np.ones(n)
    if root is not None and USED_FILES:
        say(f"  found recordings: {copy_found(Path(root))} new licence lines in public/sfx/ASSETS.txt")
    energy, silent = energy_curve(grid, n)
    dips = plan_dips(brief, grid, seconds, [c["frame"] / FPS for c in cues if c.get("cut")])
    for d in dips:
        d["bar"] = grid.bar
    dipg = dip_curve(dips, n, brief.get("dip_db", -24.0))
    t = np.arange(n) / SR
    f0, f1 = brief.get("fade", [seconds - 1.7, seconds - 0.2])
    tail = np.where(t < f0, 1, np.clip((f1 - t) / (f1 - f0), 0, 1) ** 2)
    rng = np.random.default_rng(seed + 202)
    cold = brief.get("opening", "soft") == "cold"
    head = 0.0 if cold else brief.get("head", float(rng.uniform(0.0, 0.12)))
    want_open = brief.get("opening_lu", float(rng.uniform(-3.5, -1.6)))
    want_lra = brief.get("lra", 6.0)
    span, depth = 9.0, 6.0  # dB between energy 0 and 1; dB the opening starts under the body
    for _ in range(5):  # find the level span and opening depth that land LRA and the opening
        level = 10 ** (-span * (1 - energy) / 20) * ~silent
        opening = np.ones(n) if cold else np.where(t < head, 0, 10 ** (-depth * np.clip(1 - (t - head) / 1.6, 0, 1) ** 1.5 / 20))
        mix = breath_guard(music * level, grid) * story_duck + fxs * brief.get("fx_level", 0.5)
        mix = mix * dipg * opening * tail
        mix[:, silent] = 0
        lo = loudness(mix)
        say(f"  level pass: span {span:.1f} dB, opening depth {depth:.1f} dB -> LRA {lo['loudness_range_lu']:.1f} LU, opening {lo['opening_lu']:+.1f} LU")
        ok_lra = abs(lo["loudness_range_lu"] - want_lra) < 0.6
        ok_open = cold or abs(lo["opening_lu"] - want_open) < 0.5
        if ok_lra and ok_open:
            break
        span = float(np.clip(span * want_lra / max(lo["loudness_range_lu"], 0.5), 1.5, 26))
        if not cold:
            depth = float(np.clip(depth + lo["opening_lu"] - want_open, 0, 24))
    # Loudness for the destination (references/destinations.md): -14 LUFS for web, social and stores,
    # -23 LUFS for European TV (EBU R128), -24 for US TV (ATSC A/85).
    loud = brief.get("loudness", {})
    tone = brief.get("tone", {})
    out = dsp.master(mix, loud.get("lufs", -14.0), loud.get("tp", -1.0),
                     tone=None if tone is False else (tone.get("centroid", 1800.0), tone.get("rolloff", 4000.0)),
                     bass_harmonics=brief.get("bass_harmonics", 0.3))
    return out, grid, dips


def report(mix: np.ndarray, grid: Grid, dips: list[dict], brief: dict) -> None:
    import pyloudnorm

    r = filmstats.analyze(mix, SR, patches=False)
    print(f"{brief['genre']}{'' if brief.get('beat', True) else ' (beatless)'} {grid.bpm} BPM, {brief['key']} {brief['mode']}: "
          f"{pyloudnorm.Meter(SR).integrated_loudness(mix.T):.2f} LUFS, true peak {dsp.true_peak(mix):.2f} dBTP")
    print(f"  LRA {r['loudness_range_lu']:.1f} LU (pro 5 to 11), opening {r['opening_lu']:+.1f} LU (pro median -1.9), "
          f"centroid {r['centroid_median_hz']:.0f} Hz (pro median 1834), rolloff {r['rolloff_median_hz']:.0f} Hz (pro median 3973)")
    print(f"  grid offset {r['grid_offset_norm'] or 0:.3f} of a 16th (pro median 0.105), pulse {r['pulse_strength']:.2f}, "
          f"density at 75 to 85 percent {r['density_at_80pct']:.1f}/s against a median {r['density_median']:.1f}/s")
    print("  dips planned: " + ", ".join(f"{100 * (d['end'] - d['length']) / (mix.shape[1] / SR):.0f}% {d['length']:.2f}s{' main' if d['main'] else ''}" for d in dips))
    print("  dips measured: " + (", ".join(f"{d['pos_pct']:.0f}% {d['len_s']:.2f}s {d['rise_db'] or 0:+.0f}dB {d['next_onset_delay_ms']}ms" for d in r["dips"]) or "none"))
    for sec in grid.sections:
        a, b = int(sec["start"] * SR), min(mix.shape[1], int(sec["end"] * SR))
        if b > a:
            print(f"  {sec['name']:10s} frames {grid.frame(sec['start']):5d} to {grid.frame(sec['end']):5d}: {dsp.rms_db(mix[:, a:b]):6.1f} dB RMS")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=ROOT, help="the film folder (src/music.json, src/cues.json, public/)")
    a = ap.parse_args()
    root = a.root.resolve()
    brief = json.loads((root / "src" / "music.json").read_text())
    cues = json.loads((root / "src" / "cues.json").read_text())
    seconds = brief.get("length", 30.0)
    mix, grid, dips = build(brief, cues, seconds, root)
    import soundfile

    (root / "public").mkdir(exist_ok=True)
    soundfile.write(root / "public" / "film.wav", mix.T.astype(np.float32), SR, subtype="PCM_24")
    report(mix, grid, dips, brief)


if __name__ == "__main__":
    main()
