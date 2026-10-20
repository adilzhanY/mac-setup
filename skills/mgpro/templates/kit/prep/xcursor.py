"""
Extract the user's real mouse cursors (an Xcursor theme) as PNGs plus their hotspots, so a video
uses the exact pointer the person sees every day.

    python3 xcursor.py [theme_dir] [out_dir]

theme_dir defaults to the theme in $XCURSOR_THEME, searched in ~/.local/share/icons, ~/.icons and
/usr/share/icons. Writes <shape>.png at the largest size in the file (96 px for most themes) and
cursors.json with {shape: {w, h, x, y}} where x, y is the hotspot in image pixels.
Needs numpy and ImageMagick (`magick`).
"""

import json
import os
import struct
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

SHAPES = ["left_ptr", "hand2", "xterm", "grabbing", "grab", "watch", "crosshair", "fleur"]


def find_theme() -> Path:
    name = os.environ.get("XCURSOR_THEME", "default")
    for root in (Path.home() / ".local/share/icons", Path.home() / ".icons", Path("/usr/share/icons")):
        if (root / name / "cursors").is_dir():
            return root / name
    sys.exit(f"cursor theme {name!r} not found")


def main() -> None:
    theme = Path(sys.argv[1]) if len(sys.argv) > 1 else find_theme()
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("public/cursor")
    out.mkdir(parents=True, exist_ok=True)
    meta = {}
    for name in SHAPES:
        path = theme / "cursors" / name
        if not path.exists():
            continue
        b = path.read_bytes()
        _, _, _, ntoc = struct.unpack("<4sIII", b[:16])
        images = []
        for i in range(ntoc):
            typ, _, pos = struct.unpack("<III", b[16 + 12 * i : 28 + 12 * i])
            if typ != 0xFFFD0002:  # image chunk
                continue
            _, _, _, _, w, h, xh, yh, _ = struct.unpack("<IIIIIIIII", b[pos : pos + 36])
            images.append((w, h, xh, yh, pos + 36))
        w, h, xh, yh, p = max(images, key=lambda im: im[0])
        # Pixels are premultiplied BGRA; PNG wants straight RGBA.
        px = np.frombuffer(b[p : p + w * h * 4], dtype=np.uint8).reshape(h, w, 4).astype(np.float64)
        a = px[..., 3:4] / 255.0
        rgb = np.where(a > 0, px[..., :3] / np.maximum(a, 1e-6), 0)
        rgba = np.concatenate([rgb[..., 2:3], rgb[..., 1:2], rgb[..., 0:1], px[..., 3:4]], axis=2).clip(0, 255).astype(np.uint8)
        with tempfile.NamedTemporaryFile(suffix=".rgba") as tmp:
            tmp.write(rgba.tobytes())
            tmp.flush()
            subprocess.run(["magick", "-size", f"{w}x{h}", "-depth", "8", f"rgba:{tmp.name}", str(out / f"{name}.png")], check=True)
        meta[name] = {"w": w, "h": h, "x": xh, "y": yh}
        print(f"{name}: {w}x{h}, hotspot {xh},{yh}")
    (out / "cursors.json").write_text(json.dumps(meta, indent=1))


if __name__ == "__main__":
    main()
