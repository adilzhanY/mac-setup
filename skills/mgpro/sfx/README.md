# Sound effect library (CC0)

A real, legally clean library of 1126 sound effects from 30 packs, every one CC0 (public domain dedication: no attribution, commercial use allowed, no share alike, no non commercial clause). It exists so the skill can study what designed sounds look like in numbers and, when a film allows samples, use one.

Measured, not heard: everything in `CATALOG.md`, `ANALYSIS.md` and the sheets comes from analysis code. Listen before trusting a pick.

## Where things live

| What | Where |
|---|---|
| The audio files (58 MB, not in the skill repo because of size) | `~/.local/share/mgpro/sfx/<pack>/` |
| Python with the analysis packages | `~/.local/share/mgpro/.venv/bin/python` (numpy, scipy, librosa, soundfile, pyloudnorm, matplotlib, pedalboard) |
| Download script with the exact URLs | `templates/kit/audio/fetch_sfx.sh` |
| Analysis script | `templates/kit/audio/sfx_catalog.py` |
| Every sound with its numbers | `sfx/catalog.json` (also per category summaries) |
| Readable tables, one per category | `sfx/CATALOG.md` |
| Contact sheets: waveform plus mel spectrogram per sound | `sfx/sheets/<category>-<page>.png` |
| What the library teaches, best picks per job, synth targets | `sfx/ANALYSIS.md` |
| The same numbers for every effect `sfx.py` synthesizes | `sfx/synth.json` |

Paths in `catalog.json` and `CATALOG.md` are relative to the library root `~/.local/share/mgpro/sfx/`.

## Rebuild

```bash
~/.claude/skills/mgpro/templates/kit/audio/fetch_sfx.sh            # downloads missing packs only
python3 -m venv ~/.local/share/mgpro/.venv                          # once
~/.local/share/mgpro/.venv/bin/pip install numpy scipy librosa soundfile pyloudnorm matplotlib pedalboard
~/.local/share/mgpro/.venv/bin/python ~/.claude/skills/mgpro/templates/kit/audio/sfx_catalog.py --synth
~/.local/share/mgpro/.venv/bin/python ~/.claude/skills/mgpro/templates/kit/audio/sfx_catalog.py --file some.wav   # one file
```

A full run takes about 90 seconds. To add a pack: add one line to `PACKS` in `fetch_sfx.sh` (only after checking its licence, see below), run it, run the catalogue.

## Seeing a sound without ears

1. Find candidates in `CATALOG.md` (the character column is plain words: length, onset, brightness, tone or noise, note, pitch movement, number of hits, width).
2. Open its contact sheet. Top strip: waveform normalised to its own peak, showing the sounding part plus 30 ms. Bottom strip: mel spectrogram, 0 to -80 dB of the file's own peak, low frequencies at the bottom, up to 16 kHz. A vertical bar is a transient, a horizontal line is a tone, a haze is noise, a diagonal is a pitch sweep.
3. Read its full row in `catalog.json`: `attack_ms`, `decay20_ms` (peak to -20 dB, the part you hear), `decay_ms` (peak to -40 dB, the tail), `centroid_hz` (power weighted), `bands` (share of energy under 120 Hz, 120 to 500, 500 to 2 k, 2 to 6 k, above 6 k), `noisiness` (0 pure tone, 1 pure noise), `note`, `movement`, `width`, `transients`, `lead_ms` (silence before the sound), `floor_db`, `clipped`.

## Licences, per pack

All 30 packs are CC0 1.0 (https://creativecommons.org/publicdomain/zero/1.0/). Every pack folder holds its licence file next to the audio: Kenney's own `License.txt`, or a `LICENSE.txt` written by `fetch_sfx.sh` that records the source page, author and licence.

Kenney packs ship a `License.txt` that says, verbatim: "License (Creative Commons Zero, CC0) http://creativecommons.org/publicdomain/zero/1.0/ You may use these assets in personal and commercial projects. Credit (Kenney or www.kenney.nl) would be nice but is not mandatory." Each Kenney asset page also says "Creative Commons CC0". OpenGameArt pages state the licence in a "License(s)" field; for every OGA pack below that field lists CC0 and nothing else (packs that listed several licences were left out). The Remotion files are the CC0 originals from Freesound that Remotion mirrors; each attribution line on remotion.dev reads "License: Creative Commons 0".

| Pack folder | Sounds | Author | Source page | Licence |
|---|---|---|---|---|
| kenney-ui-audio | 51 | Kenney | https://kenney.nl/assets/ui-audio | CC0 (License.txt) |
| kenney-interface-sounds | 100 | Kenney | https://kenney.nl/assets/interface-sounds | CC0 (License.txt) |
| kenney-impact-sounds | 130 | Kenney | https://kenney.nl/assets/impact-sounds | CC0 (License.txt) |
| kenney-digital-audio | 62 | Kenney | https://kenney.nl/assets/digital-audio | CC0 (License.txt) |
| kenney-casino-audio | 54 | Kenney | https://kenney.nl/assets/casino-audio | CC0 (License.txt) |
| kenney-rpg-audio | 51 | Kenney | https://kenney.nl/assets/rpg-audio | CC0 (License.txt) |
| kenney-sci-fi-sounds | 73 | Kenney | https://kenney.nl/assets/sci-fi-sounds | CC0 (License.txt) |
| kenney-music-jingles | 85 | Kenney | https://kenney.nl/assets/music-jingles | CC0 (License.txt) |
| remotion-cc0 | 5 | 1bob, JW_Audio, Pixeliota, ristooooo1, hmilleo (via Freesound) | https://www.remotion.dev/docs/sfx | CC0 per file (see LICENSE.txt) |
| oga-swishes | 13 | artisticdude | https://opengameart.org/content/swishes-sound-pack | CC0 |
| oga-air-whoosh | 1 | pyranostudios | https://opengameart.org/content/air-whoosh | CC0 |
| oga-click-clips | 87 | owlishmedia | https://opengameart.org/content/87-clickety-clips | CC0 |
| oga-3-pops | 3 | wubitog | https://opengameart.org/content/3-pop-sounds | CC0 |
| oga-pop-effects | 5 | trezegames | https://opengameart.org/content/pop-effect-sounds | CC0 |
| oga-slide-pop | 1 | ezduzziteh | https://opengameart.org/content/a-slide-pop-sound | CC0 |
| oga-clicks-switches | 11 | starninjas | https://opengameart.org/content/10-clicks-and-switches | CC0 |
| oga-button-clicks | 16 | qubodup | https://opengameart.org/content/16-button-clicks | CC0 |
| oga-ui-feedback | 12 | robin-lamb | https://opengameart.org/content/ui-sound-effects-button-clicks-user-feedback-notifications | CC0 |
| oga-ui-sounds | 5 | stumpystrust | https://opengameart.org/content/ui-sounds | CC0 |
| oga-ui-assorted | 7 | joth | https://opengameart.org/content/7-assorted-sound-effects-menu-level-up | CC0 |
| oga-ui-haeldb | 11 | haeldb | https://opengameart.org/content/ui-sounds-0 | CC0 |
| oga-gui-lokif | 13 | lokif | https://opengameart.org/content/gui-sound-effects | CC0 |
| oga-interaction | 43 | qubodup | https://opengameart.org/content/atmospheric-interaction-sound-pack | CC0 |
| oga-time-hit-wind | 4 | qubodup | https://opengameart.org/content/wind-hit-time-morph | CC0 |
| oga-bell-dings | 4 | pwl | https://opengameart.org/content/bell-dingschimes | CC0 |
| oga-metal-dings | 4 | starninjas | https://opengameart.org/content/4-metal-dingsrings | CC0 |
| oga-scifi-50 | 50 | rubberduck | https://opengameart.org/content/50-cc0-sci-fi-sfx | CC0 |
| oga-retro-synth-50 | 50 | rubberduck | https://opengameart.org/content/50-cc0-retro-synth-sfx | CC0 |
| oga-breaking-75 | 75 | rubberduck | https://opengameart.org/content/75-cc0-breaking-falling-hit-sfx | CC0 |
| oga-100-sfx | 100 | rubberduck | https://opengameart.org/content/100-cc0-sfx | CC0 |

Left out on purpose: OGA "Wierd Whooshes" and "Completion sound" (several licences listed, CC-BY among them), OGA "UI Sound Effects Library" (CC-BY 3.0), OGA "51 UI sound effects" (the same files as kenney-ui-audio), the Remotion meme sounds and `ding.wav` (no free licence), any Freesound page that needs an account, and itch.io packs (download needs a browser). Preview montages inside packs (`Preview.ogg`, `3pops.ogg`, `MenuSFXPreview.mp3`) are deleted by the fetch script.

## Using a sample in a film

`references/rights.md` makes synthesis the default. A sample from this library goes in only when the film allows samples, and then:

1. **Copy it into the film**, never read it from `~/.local/share` at render time: `cp ~/.local/share/mgpro/sfx/<path> <film>/public/sfx/`. The film must build on another machine.
2. **Record it** in the film's asset list: file, pack, source page, "CC0". No credit is required, so no credit line goes on screen.
3. **Never play the same file twice the same way.** Per use, vary pitch (plus or minus 1 to 2 semitones), level (plus or minus 1.5 dB) and start (plus or minus 4 ms), and pick between 2 or 3 files of a family (Kenney ships most sounds in numbered sets of 3 to 5) so a run of taps never machine guns.
4. **Mix it on the effects bus in `score.py`**, next to the synthesized effects, so the master and loudness pass treat it like everything else:

```python
from pathlib import Path
import soundfile as sf
from scipy.signal import resample
from dsp import SR, rng, fade

SFX = ROOT / "public" / "sfx"

def sample(name, semis=0.0, db=0.0):
    """A sample from the film's public/sfx, resampled to 48 kHz and shifted in pitch (and length)."""
    x, sr = sf.read(str(SFX / name), always_2d=True)
    n = int(round(x.shape[0] * SR / sr / 2 ** (semis / 12)))
    y = resample(x, n, axis=0).T * 10 ** (db / 20)
    return fade(y if y.shape[0] == 2 else y[0], 1)

# in effects(): a card landing, one of three files, varied every time
s = sample(f"impactWood_light_00{rng.integers(0, 3)}.ogg", rng.uniform(-1, 1), rng.uniform(-1.5, 1.5))
bus.add(s, t + rng.uniform(-0.004, 0.004), 0.8, 0.0)
```

Trim `lead_ms` (silence before the sound, in `catalog.json`) from the cue time, or the sound lands late: some files start 50 to 140 ms in. Check `clipped` too; a file with clipped samples needs 1 to 2 dB of headroom and a listen.
