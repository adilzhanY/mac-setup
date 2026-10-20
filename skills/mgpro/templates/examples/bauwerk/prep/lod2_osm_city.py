"""
The city of the commercial: the real LoD2 buildings around Methfesselstraße 8 (from the live
Bauwerk API) and the streets and parks around them (OpenStreetMap), as flat triangle buffers
the film loads straight into three.js. Frame: x east, y up, z south, metres from the BOo origin.

    .venv/bin/python prep/city.py <neighbours.json> <boo-detail.json> <osm.json>
"""

import json
import math
import sys
from pathlib import Path

import mapbox_earcut as earcut
import numpy as np
from pyproj import Transformer

RADIUS = 680.0
nb_path, boo_path, osm_path = sys.argv[1:4]
out = Path(__file__).resolve().parent.parent / "public" / "ad"
boo = json.load(open(boo_path))["parts"][0]["mesh"]
ox, oy = boo["origin"][0], boo["origin"][1]


def ring_points(flat):
    p = np.asarray(flat, dtype=np.float64).reshape(-1, 3)
    if len(p) > 1 and np.allclose(p[0], p[-1]):
        p = p[:-1]
    return p


def triangulate(rings):
    """Triangles of one planar polygon with holes, in 3D."""
    outer = rings[0]
    # Newell normal, to drop the axis the polygon is flattest along.
    n = np.zeros(3)
    for i in range(len(outer)):
        a, b = outer[i], outer[(i + 1) % len(outer)]
        n += [(a[1] - b[1]) * (a[2] + b[2]), (a[2] - b[2]) * (a[0] + b[0]), (a[0] - b[0]) * (a[1] + b[1])]
    axis = int(np.argmax(np.abs(n)))
    keep = [i for i in range(3) if i != axis]
    pts = np.concatenate(rings)
    ends = np.cumsum([len(r) for r in rings]).astype(np.uint32)
    try:
        idx = earcut.triangulate_float64(pts[:, keep], ends)
    except Exception:
        return np.zeros((0, 3))
    return pts[idx]


def surfaces(mesh):
    for s in mesh["surfaces"]:
        if s["kind"] not in ("wall", "roof"):
            continue
        rings = [ring_points(r) for r in s["rings"]]
        rings = [r for r in rings if len(r) >= 3]
        if rings:
            yield s["kind"], rings


# --- Buildings ------------------------------------------------------------------------------------
verts = []
count = 0
for b in json.load(open(nb_path)):
    m = b["mesh"]
    bx, by, bz = m["origin"]
    tris = []
    for kind, rings in surfaces(m):
        t = triangulate(rings)
        if len(t):
            tris.append((kind, t))
    if not tris:
        continue
    zmin = min(t[:, 2].min() for _, t in tris)
    allp = np.concatenate([t for _, t in tris])
    cx, cy = allp[:, 0].mean() + bx - ox, allp[:, 1].mean() + by - oy
    dist = math.hypot(cx, cy)
    if dist > RADIUS:
        continue
    count += 1
    for kind, t in tris:
        x = t[:, 0] + bx - ox
        y = t[:, 1] + by - oy
        z = t[:, 2] - zmin
        k = 1.0 if kind == "roof" else 0.0
        verts.append(np.stack([x, z, -y, np.full(len(t), dist), np.full(len(t), k)], axis=1))
city = np.concatenate(verts).astype(np.float32)
city.tofile(out / "city.bin")

# BOo's own LoD2 ground ring, to place the hero model.
ground = [ring_points(s["rings"][0]) for s in boo["surfaces"] if s["kind"] == "ground"][0]
groundRing = [[float(p[0]), float(p[1])] for p in ground]

# --- Streets and parks ------------------------------------------------------------------------------
to_utm = Transformer.from_crs("EPSG:4326", "EPSG:25833", always_xy=True)
WIDTH = {"motorway": 16, "trunk": 16, "primary": 16, "secondary": 13, "tertiary": 11, "residential": 8.5,
         "unclassified": 8.5, "living_street": 7, "pedestrian": 6, "service": 4.5}
PATH = {"footway", "path", "cycleway", "steps", "track", "bridleway"}
flat = []


def local(geom):
    lon = [g["lon"] for g in geom]
    lat = [g["lat"] for g in geom]
    x, y = to_utm.transform(lon, lat)
    return np.stack([np.asarray(x) - ox, np.asarray(y) - oy], axis=1)


def ribbon(p, w, kind):
    h = w / 2
    for a, b in zip(p[:-1], p[1:]):
        d = b - a
        L = np.hypot(*d)
        if L < 1e-6:
            continue
        n = np.array([-d[1], d[0]]) / L * h
        quad = [a + n, b + n, b - n, a + n, b - n, a - n]
        flat.extend([q[0], -q[1], kind] for q in quad)
    for c in p:  # round joins
        for i in range(10):
            a0, a1 = 2 * math.pi * i / 10, 2 * math.pi * (i + 1) / 10
            for q in (c, c + h * np.array([math.cos(a0), math.sin(a0)]), c + h * np.array([math.cos(a1), math.sin(a1)])):
                flat.append([q[0], -q[1], kind])


def area(p, kind):
    if len(p) > 1 and np.allclose(p[0], p[-1]):
        p = p[:-1]
    if len(p) < 3:
        return
    idx = earcut.triangulate_float64(p, np.array([len(p)], dtype=np.uint32))
    flat.extend([p[i][0], -p[i][1], kind] for i in idx)


osm = json.load(open(osm_path))["elements"]
# Areas first, so roads draw over them (same height, drawn in order).
for e in osm:
    t = e.get("tags", {})
    if e["type"] == "way" and "geometry" in e and (t.get("leisure") == "park" or t.get("landuse") in ("grass", "cemetery", "forest")):
        area(local(e["geometry"]), 2.0)
for e in osm:
    t = e.get("tags", {})
    if e["type"] != "way" or "geometry" not in e:
        continue
    hw = t.get("highway")
    if hw in WIDTH:
        ribbon(local(e["geometry"]), WIDTH[hw], 0.0)
    elif hw in PATH:
        ribbon(local(e["geometry"]), 1.8, 1.0)
    elif t.get("railway") == "rail":
        ribbon(local(e["geometry"]), 3.0, 3.0)
streets = np.asarray(flat, dtype=np.float32)
streets.tofile(out / "streets.bin")

(out / "city.json").write_text(json.dumps({
    "buildings": count, "cityVertices": len(city), "streetVertices": len(streets),
    "radius": RADIUS, "booGround": groundRing,
}))
print(count, "buildings,", len(city) // 3, "triangles,", len(streets) // 3, "street triangles")
