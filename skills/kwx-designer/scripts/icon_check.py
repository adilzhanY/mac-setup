#!/usr/bin/env python3
"""icon_check.py: lint, rasterise and preview hand drawn SVG icons.

An agent cannot look at an icon, so this script looks for it. For every SVG it
checks the root element against the house spec, renders the icon at 16, 20, 24
and 48 px, measures the ink, prints an ASCII picture at the canvas size, and at
the end writes one contact sheet PNG of the whole family that the agent can open
with its image reader.

Usage:
    icon_check.py ICON.svg [ICON.svg ...] [options]
    icon_check.py --selftest

Options:
    --canvas N      viewBox size of the master (default 24)
    --padding N     empty pixels between ink and canvas edge (default 2).
                    Round shapes may overshoot by 1px (warning, not error).
                    Use --padding 1 to check against Lucide's own minimum.
    --stroke N      required root stroke-width (default 2)
    --sheet PATH    where to write the contact sheet (default: a temp file)
    --no-ascii      skip the ASCII preview
    --blur-limit P  warn when more than P percent of inked pixels at canvas
                    size are partly covered (default 70, Lucide's 95th
                    percentile measured on 250 icons)

What it reports, per icon:
    lint            root attributes, allowed elements, child attributes,
                    number precision, coordinates off the pixel grid
    ink box         first and last inked pixel column and row at each size
    partial         share of inked pixels that are anti-aliased (blur measure;
                    lower is crisper; only the canvas size can be crisp).
                    Straight-edged icons land near 15%, curvy ones 40 to 70%.
    soft            straight edges (4+ pixels long) drawn at half opacity, the
                    signature of a line or rect edge sitting between pixels.
                    On grid icons score 0 (247 of 250 Lucide icons do).
    coverage        ink area as a share of the canvas (optical weight; compare
                    it across the family and with a reference circle/square)
    parts           connected ink shapes; fewer parts at 16 px than at 48 px
                    means a gap closed up at small size
    holes           enclosed empty counters (inside a ring, a knock-out in a
                    filled shape); fewer at 16 px means a counter filled up

Exit status: 0 when no icon has an error, 1 otherwise, 2 when a tool is missing.

Needs: resvg (preferred) or rsvg-convert, and ImageMagick 7 (`magick`).
Python 3 standard library only.
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

SVG_NS = "http://www.w3.org/2000/svg"
ALLOWED = {"path", "line", "polyline", "polygon", "circle", "ellipse", "rect"}
BANNED_CHILD_ATTRS = {
    "stroke", "stroke-width", "stroke-linecap", "stroke-linejoin", "transform",
    "filter", "style", "class", "id", "opacity", "mask", "clip-path",
}
GRID_ATTRS = {"x", "y", "width", "height", "x1", "y1", "x2", "y2", "cx", "cy"}
SIZES = (16, 20, 24, 48)
NUM = re.compile(r"-?\d*\.?\d+(?:e-?\d+)?", re.I)


class ToolMissing(Exception):
    pass


def find_tools():
    if not shutil.which("magick"):
        raise ToolMissing(
            "ImageMagick 7 (`magick`) is not installed. Install it "
            "(Arch: pacman -S imagemagick, Debian: apt install imagemagick, "
            "macOS: brew install imagemagick) and run again.")
    if shutil.which("resvg"):
        return "resvg"
    if shutil.which("rsvg-convert"):
        return "rsvg-convert"
    raise ToolMissing(
        "No SVG renderer found. Install resvg (preferred, Arch: pacman -S resvg, "
        "cargo install resvg) or rsvg-convert (Arch: pacman -S librsvg, "
        "Debian: apt install librsvg2-bin, macOS: brew install librsvg).")


def run(cmd):
    p = subprocess.run(cmd, capture_output=True)
    if p.returncode != 0:
        raise RuntimeError(f"{cmd[0]} failed: {p.stderr.decode(errors='replace').strip()}")
    return p.stdout


def render(renderer, svg, png, size):
    if renderer == "resvg":
        run(["resvg", "-w", str(size), "-h", str(size), svg, png])
    else:
        run(["rsvg-convert", "-w", str(size), "-h", str(size), svg, "-o", png])


def read_alpha(png, size):
    raw = run(["magick", png, "-alpha", "extract", "-depth", "8", "gray:-"])
    if len(raw) != size * size:
        raise RuntimeError(f"{png}: expected {size * size} alpha bytes, got {len(raw)}")
    return [list(raw[r * size:(r + 1) * size]) for r in range(size)]


# ---------------------------------------------------------------- lint

def lint(path, canvas, stroke):
    errors, warns = [], []
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as e:
        return [f"not valid XML: {e}"], []
    if root.tag != f"{{{SVG_NS}}}svg":
        return [f'root is <{root.tag}>, expected <svg xmlns="{SVG_NS}">'], []

    def num(v):
        try:
            return float(v)
        except (TypeError, ValueError):
            return None

    want = {
        "width": str(canvas), "height": str(canvas),
        "viewBox": f"0 0 {canvas} {canvas}", "fill": "none",
        "stroke": "currentColor", "stroke-width": None,
        "stroke-linecap": "round", "stroke-linejoin": "round",
    }
    for key, val in want.items():
        got = root.get(key)
        if key == "stroke-width":
            if num(got) != float(stroke):
                errors.append(f'root stroke-width="{got}", spec says {stroke:g}')
        elif key == "viewBox":
            if got is None or [num(t) for t in got.replace(",", " ").split()] != [0, 0, canvas, canvas]:
                errors.append(f'root viewBox="{got}", spec says "{val}"')
        elif key in ("width", "height"):
            if num(got) != float(canvas):
                errors.append(f'root {key}="{got}", spec says {val}')
        elif got != val:
            errors.append(f'root {key}="{got}", spec says "{val}"')
    for key in root.attrib:
        if key in ("transform", "style"):
            errors.append(f"root has {key}, remove it")
        elif key == "class":
            warns.append("root has class: a build artifact, keep source masters clean")

    count = 0
    for el in root.iter():
        if el is root:
            continue
        tag = el.tag.split("}")[-1]
        if tag not in ALLOWED:
            errors.append(f"<{tag}> not allowed (use path, line, polyline, polygon, circle, ellipse, rect)")
            continue
        count += 1
        for key, val in el.attrib.items():
            if key in BANNED_CHILD_ATTRS:
                errors.append(f"<{tag}> has {key}: geometry only on children, style lives on the root")
            if key == "fill" and val not in ("none", "currentColor"):
                errors.append(f'<{tag}> fill="{val}": only "currentColor" (solid part) or "none"')
            for n in NUM.findall(val):
                if "." in n and len(n.split(".")[1].rstrip("0")) > 3:
                    warns.append(f"<{tag}> {key} has {n}: keep at most 3 decimals")
                    break
            if key in GRID_ATTRS or key == "points":
                for n in NUM.findall(val):
                    v = float(n)
                    if (v * 2) != int(v * 2):
                        warns.append(f"<{tag}> {key}={n} is off the pixel grid (not a whole or half unit)")
                    elif v != int(v) and stroke % 2 == 0:
                        warns.append(f"<{tag}> {key}={n} is a half unit: an even stroke on it blurs, use whole units")
        if tag == "rect" and el.get("rx") is None:
            warns.append("<rect> without rx: the spec rounds corners (rx 2, or 1 on shapes under 8)")
    # shortcut: path coordinates are only checked for precision, not grid; the raster blur measure catches off grid paths.
    if count == 0:
        errors.append("no drawable elements")
    if count > 12:
        warns.append(f"{count} elements: dense for a UI icon, check it at 16 px")
    return errors, warns


# ---------------------------------------------------------------- raster

def measure(alpha):
    n = len(alpha)
    ink = [(x, y) for y in range(n) for x in range(n) if alpha[y][x] > 0]
    if not ink:
        return None
    xs = [p[0] for p in ink]
    ys = [p[1] for p in ink]
    partial = sum(1 for x, y in ink if alpha[y][x] < 255)
    total = sum(sum(r) for r in alpha) / 255
    return {
        "box": (min(xs), max(xs), min(ys), max(ys)),
        "partial": 100 * partial / len(ink),
        "coverage": 100 * total / (n * n),
        "parts": parts(alpha),
        "holes": holes(alpha),
        "soft": soft_edges(alpha),
    }


def soft_edges(alpha, lo=64, hi=191, minrun=4):
    """Count straight runs of half covered pixels along rows and columns."""
    runs = 0
    for lines in (alpha, [list(c) for c in zip(*alpha)]):
        for row in lines:
            k = 0
            for i, a in enumerate(row + [0]):
                if lo <= a <= hi and (k == 0 or abs(a - row[i - 1]) <= 40):
                    k += 1
                else:
                    if k >= minrun:
                        runs += 1
                    k = 1 if lo <= a <= hi else 0
    return runs


def regions(alpha, inked, threshold=128):
    """Connected regions (4-neighbour) of ink, or of empty space when inked is False.
    Returns (count, count of regions that touch the canvas border)."""
    n = len(alpha)
    seen = [[False] * n for _ in range(n)]
    count = border = 0
    for y in range(n):
        for x in range(n):
            if (alpha[y][x] >= threshold) == inked and not seen[y][x]:
                count += 1
                edge = False
                stack = [(x, y)]
                seen[y][x] = True
                while stack:
                    cx, cy = stack.pop()
                    edge = edge or cx in (0, n - 1) or cy in (0, n - 1)
                    for nx, ny in ((cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)):
                        if 0 <= nx < n and 0 <= ny < n and not seen[ny][nx] and (alpha[ny][nx] >= threshold) == inked:
                            seen[ny][nx] = True
                            stack.append((nx, ny))
                border += edge
    return count, border


def parts(alpha):
    return regions(alpha, True)[0]


def holes(alpha):
    count, border = regions(alpha, False)
    return count - border


def ascii_art(alpha):
    n = len(alpha)
    out = ["    " + "".join(f"{x % 10} " for x in range(n))]
    for y, row in enumerate(alpha):
        line = ""
        for a in row:
            line += "##" if a == 255 else "**" if a >= 170 else "++" if a >= 85 else "--" if a > 0 else ". "
        out.append(f"{y:3d} {line}")
    out.append("    legend: ## solid, ** 67-99%, ++ 33-66%, -- under 33%, . empty")
    return "\n".join(out)


# ---------------------------------------------------------------- per icon

def check_icon(path, renderer, work, args):
    rep = {"path": path, "name": os.path.splitext(os.path.basename(path))[0], "pngs": {}}
    errors, warns = lint(path, args.canvas, args.stroke)
    rep["errors"], rep["warns"], rep["metrics"] = errors, warns, {}
    sizes = sorted(set(SIZES) | {args.canvas})
    for s in sizes:
        png = os.path.join(work, f"{rep['name']}-{len(os.listdir(work))}-{s}.png")
        try:
            render(renderer, path, png, s)
            alpha = read_alpha(png, s)
        except RuntimeError as e:
            errors.append(f"render at {s}px failed: {e}")
            return rep
        rep["pngs"][s] = png
        m = measure(alpha)
        if m is None:
            errors.append(f"nothing rendered at {s}px (empty or invisible icon)")
            return rep
        rep["metrics"][s] = m
        if s == args.canvas:
            rep["alpha"] = alpha

    c, p = args.canvas, args.padding
    x0, x1, y0, y1 = rep["metrics"][c]["box"]
    lo, hi = min(x0, y0), max(x1, y1)
    if lo < p - 1 or hi > c - p:
        errors.append(f"ink reaches pixel {lo}..{hi} at {c}px, padding {p} allows {p}..{c - p - 1}")
    elif lo < p or hi > c - p - 1:
        warns.append(f"ink reaches pixel {lo}..{hi} at {c}px: 1px overshoot, fine only for round shapes")
    part = rep["metrics"][c]["partial"]
    if part > args.blur_limit:
        warns.append(f"{part:.0f}% of inked pixels are partial at {c}px (limit {args.blur_limit:g}%): "
                     "look for coordinates off the grid or diagonals that are not 45 degrees")
    soft = rep["metrics"][c]["soft"]
    if soft:
        warns.append(f"{soft} straight edge(s) sit between pixels at {c}px: move that line or rect "
                     "edge to whole units (half units for odd strokes)")
    big, small = rep["metrics"][48]["parts"], rep["metrics"][16]["parts"]
    if small < big:
        warns.append(f"{big} separate shapes at 48px but {small} at 16px: a gap closes at small size")
    big, small = rep["metrics"][48]["holes"], rep["metrics"][16]["holes"]
    if small < big:
        warns.append(f"{big} enclosed counters at 48px but {small} at 16px: an inner space fills up at small size")
    return rep


def print_report(rep, args):
    print(f"\n== {rep['path']}")
    for e in rep["errors"]:
        print(f"  ERROR {e}")
    for w in rep["warns"]:
        print(f"  warn  {w}")
    if not rep["errors"] and not rep["warns"]:
        print("  lint and checks: ok")
    if rep["metrics"]:
        print("  size  ink x      ink y      partial  coverage  parts  holes  soft")
        for s, m in sorted(rep["metrics"].items()):
            x0, x1, y0, y1 = m["box"]
            print(f"  {s:>4}  {x0:>2}..{x1:<5}  {y0:>2}..{y1:<5}  {m['partial']:>6.1f}%  {m['coverage']:>7.1f}%  {m['parts']:>5}  {m['holes']:>5}  {m['soft']:>4}")
    if "alpha" in rep and not args.no_ascii:
        print(f"  ASCII at {args.canvas}px (column and row numbers are pixel indices):")
        print(ascii_art(rep["alpha"]))


# ---------------------------------------------------------------- contact sheet

def contact_sheet(reports, work, out):
    tiles = []
    for i, rep in enumerate(reports):
        if 48 not in rep["pngs"] or 24 not in rep["pngs"]:
            continue
        p48, p24 = rep["pngs"][48], rep["pngs"][24]
        tile = os.path.join(work, f"tile-{i}.png")
        light = ["-background", "white", "-flatten", "-gravity", "center", "-extent", "64x64"]
        dark = ["-channel", "RGB", "-negate", "+channel", "-background", "#1c1c1e", "-flatten",
                "-gravity", "center", "-extent", "64x64"]
        run(["magick",
             "(", p48, *light, ")", "(", p24, *light, ")",
             "(", p48, *dark, ")", "(", p24, *dark, ")", "+append", tile])
        tiles.append((rep["name"], tile))
    if not tiles:
        return None
    cmd = ["magick", "montage", "-pointsize", "12", "-background", "white"]
    for name, tile in tiles:
        cmd += ["-label", name, tile]
    cmd += ["-tile", f"{min(4, len(tiles))}x", "-geometry", "+10+10", out]
    run(cmd)
    return out


# ---------------------------------------------------------------- main

def main(argv=None):
    ap = argparse.ArgumentParser(description="Lint, rasterise and preview SVG icons.",
                                 formatter_class=argparse.RawDescriptionHelpFormatter,
                                 epilog=__doc__.split("Options:")[1].split("Needs:")[0])
    ap.add_argument("svgs", nargs="*")
    ap.add_argument("--canvas", type=int, default=24)
    ap.add_argument("--padding", type=int, default=2)
    ap.add_argument("--stroke", type=float, default=2)
    ap.add_argument("--sheet")
    ap.add_argument("--no-ascii", action="store_true")
    ap.add_argument("--blur-limit", type=float, default=70)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)

    try:
        renderer = find_tools()
    except ToolMissing as e:
        print(f"icon_check: {e}", file=sys.stderr)
        return 2
    if args.selftest:
        return selftest(renderer)
    if not args.svgs:
        ap.error("give at least one SVG file, or --selftest")
    missing = [s for s in args.svgs if not os.path.isfile(s)]
    if missing:
        ap.error("no such file: " + ", ".join(missing))

    work = tempfile.mkdtemp(prefix="icon_check-")
    print(f"icon_check: renderer {renderer}, spec canvas {args.canvas}, padding {args.padding}, stroke {args.stroke:g}")
    reports = [check_icon(s, renderer, work, args) for s in args.svgs]
    for rep in reports:
        print_report(rep, args)
    sheet = contact_sheet(reports, work, args.sheet or os.path.join(work, "contact-sheet.png"))
    bad = sum(1 for r in reports if r["errors"])
    nwarn = sum(len(r["warns"]) for r in reports)
    print(f"\n{len(reports)} icon(s), {bad} with errors, {nwarn} warning(s)")
    if sheet:
        print(f"contact sheet (per icon: 48 and 24 px on light, then on dark): {sheet}")
    return 1 if bad else 0


ROOT = ('<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" '
        'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">')


def selftest(renderer):
    work = tempfile.mkdtemp(prefix="icon_check-selftest-")
    on = os.path.join(work, "on-grid.svg")
    off = os.path.join(work, "off-grid.svg")
    with open(on, "w") as f:
        f.write(ROOT + '<rect x="4" y="4" width="16" height="16" rx="2"/><line x1="12" y1="8" x2="12" y2="16"/></svg>\n')
    with open(off, "w") as f:
        f.write(ROOT + '<rect x="4.5" y="4.5" width="15" height="15" rx="2"/><line x1="11.5" y1="8" x2="11.5" y2="16"/></svg>\n')
    args = argparse.Namespace(canvas=24, padding=2, stroke=2, no_ascii=False, blur_limit=70)
    a, b = (check_icon(p, renderer, work, args) for p in (on, off))
    pa, pb = a["metrics"][24]["partial"], b["metrics"][24]["partial"]
    checks = [
        ("on grid icon has no lint errors", not a["errors"]),
        ("on grid ink box is pixels 3..20", a["metrics"][24]["box"] == (3, 20, 3, 20)),
        ("off grid icon gets off grid warnings", any("half unit" in w for w in b["warns"])),
        ("off grid has soft straight edges, on grid has none",
         b["metrics"][24]["soft"] > 0 and a["metrics"][24]["soft"] == 0),
        (f"off grid is blurrier ({pb:.1f}% partial vs {pa:.1f}%)", pb > pa),
        ("ASCII preview has 24 pixel rows", len(ascii_art(a["alpha"]).splitlines()) == 26),
        ("contact sheet written", bool(contact_sheet([a, b], work, os.path.join(work, "sheet.png")))),
    ]
    for label, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'}  {label}")
    print(f"selftest files in {work}")
    return 0 if all(ok for _, ok in checks) else 1


if __name__ == "__main__":
    sys.exit(main())
