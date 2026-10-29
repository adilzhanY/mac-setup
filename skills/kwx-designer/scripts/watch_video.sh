#!/usr/bin/env bash
# watch_video.sh: turn a design video into things an agent can read.
#
#   watch_video.sh <youtube-url> <out-dir> [interval-seconds]
#
# Produces in <out-dir>:
#   transcript.txt   timestamped, deduplicated lines ([mm:ss] text)
#   f/NNNN.jpg       scene-change frames plus one every <interval> s (default 8)
#   frames.tsv       frame file and its timestamp in seconds
#   sheets/NN.jpg    3x3 contact sheets, each tile labelled with its time
# Read the sheets in order next to transcript.txt, then Read single frames at
# full size wherever the screen shows real UI.
#
# The video is streamed, never saved. Audio for the whisper fallback is a temp
# WAV that is deleted afterwards.
set -euo pipefail

url=${1:?usage: watch_video.sh <url> <out-dir> [interval]}
out=${2:?usage: watch_video.sh <url> <out-dir> [interval]}
interval=${3:-8}
whisper=${WHISPER_CLI:-$HOME/dev/OpenHyprWhisper/vendor/whisper.cpp/build/bin/whisper-cli}
model=${WHISPER_MODEL:-$HOME/.local/share/openhyprwhisper/models/ggml-large-v3-turbo-q5_0.bin}

for t in yt-dlp ffmpeg montage python3; do
    command -v "$t" >/dev/null || { echo "missing tool: $t" >&2; exit 1; }
done
mkdir -p "$out/f" "$out/sheets"

# 1. Transcript: YouTube subs first; they often fail with HTTP 429, so fall back to whisper.cpp.
if yt-dlp -q --skip-download --write-auto-subs --write-subs --sub-langs "en.*" \
        --sub-format vtt -o "$out/sub" "$url" 2>/dev/null && ls "$out"/sub*.vtt >/dev/null 2>&1; then
    python3 -I - "$(ls "$out"/sub*.vtt | head -1)" > "$out/transcript.txt" <<'PY'
import re, sys
seen, cur = set(), None
for line in open(sys.argv[1], encoding="utf-8"):
    m = re.match(r"(\d+):(\d+):(\d+)\.\d+ -->", line)
    if m:
        h, mi, s = map(int, m.groups()); cur = f"[{h*60+mi:02d}:{s:02d}]"; continue
    text = re.sub(r"<[^>]+>", "", line).strip()
    if cur and text and text not in seen and not text.startswith(("WEBVTT", "Kind:", "Language:")):
        seen.add(text); print(cur, text)
PY
elif [ -x "$whisper" ] && [ -f "$model" ]; then
    echo "subtitles unavailable, transcribing with whisper.cpp" >&2
    wav=$(mktemp --suffix=.wav)
    trap 'rm -f "$wav"' EXIT
    ffmpeg -loglevel error -y -i "$(yt-dlp -g -f ba "$url")" -ac 1 -ar 16000 "$wav"
    "$whisper" -m "$model" -f "$wav" 2>/dev/null | sed -nE 's/^\[([0-9:.]+) --> [^]]*\] */[\1] /p' > "$out/transcript.txt"
else
    echo "no subtitles and no whisper.cpp at $whisper; continuing with frames only" >&2
fi

# 2. Frames straight from the stream: scene changes OR every <interval> seconds.
# shortcut: the interval assumes 30 fps, so a 60 fps video samples twice as often; fine for reading.
stream=$(yt-dlp -g -f "bv[height<=720]/b[height<=720]" "$url" | head -1)
ffmpeg -loglevel info -y -i "$stream" \
    -vf "select='gt(scene,0.25)+not(mod(n,round(${interval}*30)))',showinfo,scale=1280:-1" \
    -fps_mode vfr -q:v 3 "$out/f/%04d.jpg" 2> "$out/showinfo.log"
grep -oE 'pts_time:[0-9.]+' "$out/showinfo.log" | cut -d: -f2 \
    | paste <(ls "$out/f" | sort) - > "$out/frames.tsv"

# 3. Contact sheets, 9 frames each, labelled mm:ss.
python3 -I - "$out" <<'PY'
import subprocess, sys
out = sys.argv[1]
rows = [l.split("\t") for l in open(f"{out}/frames.tsv").read().splitlines() if "\t" in l]
for i in range(0, len(rows), 9):
    args = []
    for name, t in rows[i:i + 9]:
        s = int(float(t)); args += ["-label", f"{s // 60:02d}:{s % 60:02d}  {name}", f"{out}/f/{name}"]
    subprocess.run(["montage", *args, "-tile", "3x3", "-geometry", "640x360+4+4",
                    "-pointsize", "22", f"{out}/sheets/{i // 9 + 1:02d}.jpg"], check=True)
print(f"{len(rows)} frames, {(len(rows) + 8) // 9} sheets in {out}/sheets")
PY
