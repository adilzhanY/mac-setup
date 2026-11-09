#!/usr/bin/env bash
# Fetch the sample instruments for sampler.py into one folder (default /games/mgpro/instruments).
#
#   audio/fetch_instruments.sh [DEST]
#
# Every source is CC0 1.0 except the Voxengo impulse responses (free for any purpose, commercial
# included, not to be resold). Each source is pinned to a commit or a dated archive, and only the
# instruments listed below are taken (about 3 GB of WAV, stored as FLAC, about 2 GB on disk).
# Licence evidence is copied next to each source and summed up in DEST/SOURCES.txt.
#
# The disk is checked before every source: the script stops if / has under 3 GB free or the
# destination disk under 8 GB. Files already present are skipped, so it can be run again.
# WAV files are converted to FLAC (24 bit) after download; sampler.py finds a .flac when an SFZ
# names a .wav.
set -euo pipefail

DEST=${1:-/games/mgpro/instruments}
PY=${PY:-python3}
mkdir -p "$DEST"

check_disk() {
  local root dest
  root=$(df --output=avail -B1G / | tail -1 | tr -d ' ')
  dest=$(df --output=avail -B1G "$DEST" | tail -1 | tr -d ' ')
  echo "  free: / ${root} GB, $(df --output=target "$DEST" | tail -1) ${dest} GB"
  if [ "$root" -lt 3 ] || [ "$dest" -lt 8 ]; then
    echo "stopping: / must keep 3 GB and the destination 8 GB free" >&2
    exit 1
  fi
}

# fetch_github NAME OWNER/REPO COMMIT PREFIX...
# Lists the repo tree at the pinned commit and downloads every file whose path starts with one
# of the prefixes, from https://raw.githubusercontent.com/OWNER/REPO/COMMIT/<path>.
fetch_github() {
  local name=$1 repo=$2 sha=$3
  shift 3
  echo "== $name ($repo @ ${sha:0:7})"
  check_disk
  local tree
  # gh (when logged in) avoids the API's 60 requests per hour limit for anonymous calls
  if command -v gh > /dev/null && gh auth status > /dev/null 2>&1; then
    tree=$(gh api "repos/$repo/git/trees/$sha?recursive=1")
  else
    tree=$(curl -sfL --retry 3 "https://api.github.com/repos/$repo/git/trees/$sha?recursive=1")
  fi
  printf '%s' "$tree" | "$PY" -I -c '
import json, sys, urllib.parse
repo, sha, prefixes = sys.argv[1], sys.argv[2], sys.argv[3:]
for x in json.load(sys.stdin)["tree"]:
    p = x["path"]
    if x["type"] == "blob" and any(p == q or p.startswith(q) for q in prefixes):
        print(f"https://raw.githubusercontent.com/{repo}/{sha}/{urllib.parse.quote(p)}\t{p}")
' "$repo" "$sha" "$@" | while IFS=$'\t' read -r url path; do
    out="$DEST/$name/$path"
    [ -s "$out" ] || [ -s "${out%.wav}.flac" ] && continue
    printf '%s\t%s\n' "$url" "$out"
  done | "$PY" -I -c '
import concurrent.futures, os, subprocess, sys
jobs = [l.rstrip("\n").split("\t") for l in sys.stdin if l.strip()]
def get(job):
    url, out = job
    os.makedirs(os.path.dirname(out), exist_ok=True)
    subprocess.run(["curl", "-sfL", "--retry", "4", "-o", out + ".part", url], check=True)
    os.replace(out + ".part", out)
with concurrent.futures.ThreadPoolExecutor(8) as ex:
    list(ex.map(get, jobs))
print(f"  {len(jobs)} files downloaded")
'
  check_disk
}

# fetch_archive NAME URL  (a 7z or zip, unpacked into DEST/NAME)
fetch_archive() {
  local name=$1 url=$2 file
  echo "== $name ($url)"
  check_disk
  [ -d "$DEST/$name" ] && [ -n "$(ls -A "$DEST/$name")" ] && { echo "  present"; return; }
  mkdir -p "$DEST/$name"
  file="$DEST/$name/$(basename "$url")"
  curl -sfL --retry 3 -o "$file" "$url"
  case "$file" in
    *.7z) 7z x -y -o"$DEST/$name" "$file" > /dev/null ;;
    *.zip) unzip -q -o "$file" -d "$DEST/$name" ;;
  esac
  rm -f "$file"
  check_disk
}

# VS Chamber Orchestra 2 Community Edition, SFZ branch. CC0 1.0 (LICENSE in the repo).
fetch_github vsco sgossner/VSCO-2-CE 6dd651d55dde97fd4028699be9d4481f26917891 \
  LICENSE README.md \
  ViolinEnsSusVib.sfz ViolinEnsSpic.sfz ViolinEnsPizz.sfz \
  ViolaEnsSusVib.sfz ViolaEnsSpic.sfz ViolaEnsPizz.sfz \
  CelloEnsSusVib.sfz CelloEnsSpic.sfz CelloEnsPizz.sfz \
  ContrabassSusVB.sfz ContrabassPizz.sfz Harp.sfz UprightPiano.sfz Glockenspiel.sfz \
  Timpani.sfz FluteSusVib.sfz FHornSus.sfz \
  "Strings/Violin Section/susVib/" "Strings/Violin Section/Spic/" "Strings/Violin Section/Pizz/" \
  "Strings/Viola Section/susvib/" "Strings/Viola Section/spic/" "Strings/Viola Section/pizz/" \
  "Strings/Cello Section/susvib/" "Strings/Cello Section/spic/" "Strings/Cello Section/pizzT/" \
  "Strings/Solo Contrabass/SusVib/" "Strings/Solo Contrabass/Pizz/" "Strings/Harp/" \
  "Keys/Upright Piano/" "Percussion/Glock/" "Percussion/Timpani/" "Percussion/BDrumNewhit" \
  "Woodwinds/Flute/susvib/" "Brass/F Horn/sus/"

# Versilian Community Sample Library v1.2.2-RC (SFZ release tag). CC0 1.0.
fetch_github vcsl sgossner/VCSL b6e6ac82d22248edee98a0bde185eb9ef6d439ad \
  LICENSE README.md \
  "Chordophones/Zithers/Grand Piano, Kawai.sfz" "Chordophones/Zithers/Grand Piano, Kawai/" \
  "Idiophones/Struck Idiophones/Marimba" \
  "Idiophones/Struck Idiophones/Vibraphone - Soft Mallets.sfz" "Idiophones/Struck Idiophones/Vibraphone/Soft Mallets/" \
  "Idiophones/Struck Idiophones/Glockenspiel" \
  "Idiophones/Struck Idiophones/Claps" "Idiophones/Struck Idiophones/Shaker, Small" \
  "Idiophones/Struck Idiophones/Tambourine 1" "Idiophones/Struck Idiophones/Woodblock" \
  "Idiophones/Struck Idiophones/Cabasa" "Idiophones/Struck Idiophones/Claves" \
  "Idiophones/Struck Idiophones/Cajon" "Idiophones/Plucked Idiophones/Kalimba, Kenya"

# Virtuosity Drums (Versilian Studios and Karoryfer Samples), mid mic program only. CC0 1.0.
fetch_github virtuosity sfzinstruments/virtuosity_drums 9f04cf9a734527edfbb0a4eee1f674e45bbf71bc \
  LICENSE README.md Programs/ Samples/mid/ Samples/perc/mid/

# Osiris Piano (Versilian Studios and Karoryfer Samples), una corda: the soft piano. CC0 1.0.
fetch_github osiris sfzinstruments/Osiris_Piano 18c6afccb60cff458edbf7c394571783e074e1e9 \
  LICENSE beta_notes.txt Programs/ UC/ UC-Sus/

# Karoryfer x bigcat cello (solo cello: sustain, staccato, pizzicato). CC0 1.0.
fetch_github cello sfzinstruments/karoryfer-bigcat.cello 6fd75fbfc1dbb3109bf26220ba1adea46188a18b \
  LICENSE readme.txt Programs/ Samples/sus/ Samples/staccato/ Samples/pizzcato/

# Karoryfer Shinyguitar, the miked archtop (acoustic) half. CC0 1.0.
fetch_github shinyguitar sfzinstruments/karoryfer.shinyguitar 57243cca85277dbcc120ce17c6178032f93c80f3 \
  LICENSE readme.txt Programs/ Samples/acoustic/

# Karoryfer Sneakybass, pizzicato double bass (pluck articulation). CC0 1.0.
fetch_github sneakybass sfzinstruments/karoryfer.sneakybass cc1a67e5c913678b85eaad1a3b5cb180d3be3e2d \
  LICENSE readme.txt Programs/ Samples/pluck/

# Karoryfer Black And Blue Basses, the Dark Black electric bass (fingered plucks). CC0 1.0.
fetch_github bluebass sfzinstruments/karoryfer.black-and-blue-basses 6e7d674cdb41be7a54dbccb15472401ad01099b9 \
  LICENSE changelog.txt Programs/ Samples/darkblack/reg/ Samples/darkblack/rel/

# Body percussion (claps, snaps, stomps). CC0 1.0.
fetch_github body sfzinstruments/body_percussion 4ac9d8966679c648b62fa10a188179e186b97f24 \
  LICENSE readme.txt Programs/ Samples/

# FreePats Upright Piano KW 2022-02-21, a small dry upright. CC0 1.0.
fetch_archive uprightkw https://freepats.zenvoid.org/Piano/UprightPianoKW/UprightPianoKW-SFZ+FLAC-20220221.7z

# Voxengo free reverb impulse responses: royalty free for any purpose including commercial use,
# not to be sold or redistributed for profit. Used only to convolve, never shipped as files.
fetch_archive voxengo https://www.voxengo.com/files/impulses/IMreverbs.zip

cat > "$DEST/SOURCES.txt" <<'EOF'
Sample instruments for mgpro's sampler.py, fetched by fetch_instruments.sh.
Licence checked 2026-10-29 from each source's LICENSE file or official page.

folder       source                                                         licence
vsco         github.com/sgossner/VSCO-2-CE @6dd651d (SFZ branch)            CC0 1.0 (LICENSE: "CC0 1.0 Universal")
vcsl         github.com/sgossner/VCSL @b6e6ac8 (v1.2.2-RC)                   CC0 1.0 (README: "you can do whatever you want with these sounds (even make commercial software), no royalties, no credit, no special terms")
virtuosity   github.com/sfzinstruments/virtuosity_drums @9f04cf9             CC0 1.0 (LICENSE)
osiris       github.com/sfzinstruments/Osiris_Piano @18c6afc                 CC0 1.0 (LICENSE; beta_notes.txt: "CC0 license added")
cello        github.com/sfzinstruments/karoryfer-bigcat.cello @6fd75fb       CC0 1.0 (LICENSE; readme: "royalty-free for all commercial and non-commercial use")
shinyguitar  github.com/sfzinstruments/karoryfer.shinyguitar @57243cc        CC0 1.0 (LICENSE)
sneakybass   github.com/sfzinstruments/karoryfer.sneakybass @cc1a67e         CC0 1.0 (readme: "Royalty-free for all commercial and non-commercial use. CC-0 license.")
bluebass     github.com/sfzinstruments/karoryfer.black-and-blue-basses @6e7d674   CC0 1.0 (LICENSE)
body         github.com/sfzinstruments/body_percussion @4ac9d89              CC0 1.0 (readme: "CC 0 license.")
uprightkw    freepats.zenvoid.org/Piano/acoustic-grand-piano.html, 2022-02-21  CC0 1.0 ("Published under the terms of the Creative Commons CC0 1.0 public domain dedication.")
voxengo      voxengo.com/impulses (IMreverbs.zip)                           Voxengo terms: "Permission is granted to anyone to use these impulse files royalty-free for any purpose, including commercial usage." "You may not sell these impulse files or earn any direct or indirect profit from their distribution."

Not used: Salamander Grand Piano (CC BY 3.0, needs a credit an ad cannot carry), Sonatina Symphonic
Orchestra and Virtual Playing Orchestra (CC Sampling Plus 1.0 excludes advertising), Spitfire LABS.
CC0 needs no credit. Never redistribute the Voxengo files; a rendered film is fine.
EOF

echo "== converting WAV to FLAC"
check_disk
find "$DEST" -name '*.wav' -print0 | "$PY" -I -c '
import concurrent.futures, os, sys
import soundfile as sf
paths = [p for p in sys.stdin.read().split("\0") if p and "/voxengo/" not in p]
def conv(p):
    x, sr = sf.read(p, always_2d=True)
    sf.write(p[:-4] + ".flac", x, sr, subtype="PCM_24" if sf.info(p).subtype not in ("PCM_16", "PCM_S8", "PCM_U8") else "PCM_16")
    os.remove(p)
with concurrent.futures.ThreadPoolExecutor(os.cpu_count()) as ex:
    list(ex.map(conv, paths))
print(f"  {len(paths)} files converted")
'
check_disk
du -sh "$DEST"
echo "done: see $DEST/SOURCES.txt"
