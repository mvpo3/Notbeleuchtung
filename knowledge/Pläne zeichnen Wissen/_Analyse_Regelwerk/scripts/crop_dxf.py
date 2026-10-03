"""crop_dxf.py — schneller DXF-Ausschnitts-Renderer für die Bild↔DXF-Verifikation.

Standalone-Adaption des fastcad-Rezepts (Baufeld E2 `_RIVO_Ausgabe/scripts/
fastcad.py`): Geschoss EINMAL zu farbigen Liniensegmenten + Textlabels
explodieren und cachen, pro Ausschnitt via LineCollection zeichnen (<1 s).
Hier OHNE Symbol-Stempel — die RIVO-Blöcke sollen als Liniengeometrie sichtbar
sein (wir prüfen ja gerade ihre Rotation/Position). Weißer Grund (Abgleich mit
PDF-Seiten).

Aufruf:
    python crop_dxf.py <dxf> --xy <cx> <cy> --hw 8000 [--out out.png]
    python crop_dxf.py <dxf> --handle 2A3F [--hw 6000] [--out out.png]
"""
from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

import ezdxf
import ezdxf.bbox as ezbbox
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from ezdxf import colors as ezcolors
from matplotlib.collections import LineCollection

_CACHE: dict[str, tuple] = {}


def _rgb(e, layer_rgb):
    try:
        tc = e.dxf.true_color if e.dxf.hasattr("true_color") else None
        if tc:
            return ((tc >> 16) & 255) / 255, ((tc >> 8) & 255) / 255, (tc & 255) / 255
        aci = int(getattr(e.dxf, "color", 256) or 256)
        if aci in (256, 0):
            return layer_rgb
        if aci == 7:               # weiß/schwarz-Flip: auf weißem Grund schwarz
            return (0.0, 0.0, 0.0)
        r, g, b = ezcolors.aci2rgb(aci)
        return r / 255, g / 255, b / 255
    except Exception:  # noqa: BLE001 — Analyse-Robustheit
        return layer_rgb


def _layer_rgb(doc, name):
    try:
        lay = doc.layers.get(name)
        tc = lay.dxf.true_color if lay.dxf.hasattr("true_color") else None
        if tc:
            return ((tc >> 16) & 255) / 255, ((tc >> 8) & 255) / 255, (tc & 255) / 255
        aci = int(lay.color)
        if abs(aci) == 7 or aci == 0:
            return (0.0, 0.0, 0.0)
        r, g, b = ezcolors.aci2rgb(abs(aci))
        return r / 255, g / 255, b / 255
    except Exception:  # noqa: BLE001 — Analyse-Robustheit
        return (0.35, 0.35, 0.35)


def _segs(e):
    t = e.dxftype()
    try:
        if t == "LINE":
            s, en = e.dxf.start, e.dxf.end
            return [((s[0], s[1]), (en[0], en[1]))]
        if t == "LWPOLYLINE":
            pts = [(p[0], p[1]) for p in e.get_points()]
            segs = [(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
            if e.closed and len(pts) > 2:
                segs.append((pts[-1], pts[0]))
            return segs
        if t == "POLYLINE":
            pts = [(v.dxf.location[0], v.dxf.location[1]) for v in e.vertices]
            return [(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
        if t == "ARC":
            c = e.dxf.center
            r = e.dxf.radius
            a0 = math.radians(e.dxf.start_angle)
            a1 = math.radians(e.dxf.end_angle)
            if a1 <= a0:
                a1 += 2 * math.pi
            n = max(3, int((a1 - a0) / 0.25))
            p = [(c[0] + r * math.cos(a0 + (a1 - a0) * k / n),
                  c[1] + r * math.sin(a0 + (a1 - a0) * k / n)) for k in range(n + 1)]
            return [(p[i], p[i + 1]) for i in range(len(p) - 1)]
        if t == "CIRCLE":
            c = e.dxf.center
            r = e.dxf.radius
            p = [(c[0] + r * math.cos(2 * math.pi * k / 40),
                  c[1] + r * math.sin(2 * math.pi * k / 40)) for k in range(41)]
            return [(p[i], p[i + 1]) for i in range(len(p) - 1)]
        if t == "ELLIPSE":
            pts = list(e.flattening(0.2))
            return [((pts[i][0], pts[i][1]), (pts[i + 1][0], pts[i + 1][1]))
                    for i in range(len(pts) - 1)]
        if t == "SOLID":
            pts = []
            for a in ("vtx0", "vtx1", "vtx3", "vtx2"):  # DXF-SOLID-Reihenfolge!
                v = getattr(e.dxf, a, None)
                if v is not None:
                    pts.append((v[0], v[1]))
            return [(pts[i], pts[(i + 1) % len(pts)]) for i in range(len(pts))] if len(pts) >= 3 else []
        if t == "HATCH":
            segs = []
            for path in e.paths:
                verts = getattr(path, "vertices", None)
                if verts:
                    pts = [(v[0], v[1]) for v in verts]
                    segs += [(pts[i], pts[(i + 1) % len(pts)]) for i in range(len(pts))]
            return segs
    except Exception:  # noqa: BLE001 — Analyse-Robustheit
        return []
    return []


def flatten(path: str):
    if path in _CACHE:
        return _CACHE[path]
    doc = ezdxf.readfile(path)
    msp = doc.modelspace()
    lrgb: dict[str, tuple] = {}
    segs = []
    labels = []
    for e in msp:
        t = e.dxftype()
        lay = str(e.dxf.layer)
        if lay not in lrgb:
            lrgb[lay] = _layer_rgb(doc, lay)
        if t in ("TEXT", "MTEXT"):
            try:
                s = e.plain_text() if t == "MTEXT" else e.dxf.text
                s = str(s).strip()
                if not s:
                    continue
                pos = e.dxf.insert
                h = float(getattr(e.dxf, "char_height", 0) or getattr(e.dxf, "height", 0) or 200)
                labels.append((pos[0], pos[1], s, _rgb(e, lrgb[lay]), h))
            except Exception:  # noqa: BLE001, S110 — Analyse-Robustheit
                pass
            continue
        if t == "INSERT":
            try:
                subs = list(e.virtual_entities())
            except Exception:  # noqa: BLE001 — Analyse-Robustheit
                subs = []
            for se in subs:
                st = se.dxftype()
                if st in ("TEXT", "MTEXT", "ATTRIB"):
                    continue
                slay = str(se.dxf.layer)
                if slay not in lrgb:
                    lrgb[slay] = _layer_rgb(doc, slay)
                rgb = _rgb(se, lrgb.get(slay, (0.35, 0.35, 0.35)))
                for (p0, p1) in _segs(se):
                    segs.append((p0[0], p0[1], p1[0], p1[1], rgb))
            continue
        rgb = _rgb(e, lrgb[lay])
        for (p0, p1) in _segs(e):
            segs.append((p0[0], p0[1], p1[0], p1[1], rgb))
    arr = (np.array([[s[0], s[1], s[2], s[3]] for s in segs], dtype=float)
           if segs else np.zeros((0, 4)))
    cols = [s[4] for s in segs]
    _CACHE[path] = (arr, cols, labels)
    return _CACHE[path]


def draw(ax, path: str, cx: float, cy: float, hw: float, hh: float | None = None,
         lw: float = 0.7, texte: bool = True):
    hh = hh or hw
    arr, cols, labels = flatten(path)
    x0, y0, x1, y1 = cx - hw, cy - hh, cx + hw, cy + hh
    ax.set_facecolor("white")
    if len(arr):
        m = hw * 0.15
        sx0 = np.minimum(arr[:, 0], arr[:, 2])
        sx1 = np.maximum(arr[:, 0], arr[:, 2])
        sy0 = np.minimum(arr[:, 1], arr[:, 3])
        sy1 = np.maximum(arr[:, 1], arr[:, 3])
        vis = ~((sx1 < x0 - m) | (sx0 > x1 + m) | (sy1 < y0 - m) | (sy0 > y1 + m))
        idx = np.nonzero(vis)[0]
        if len(idx):
            lc = LineCollection([[(a, b), (c, d)] for a, b, c, d in arr[idx]],
                                colors=[cols[i] for i in idx], linewidths=lw)
            ax.add_collection(lc)
    if texte:
        for (lx, ly, s, rgb, h) in labels:
            if x0 <= lx <= x1 and y0 <= ly <= y1 and len(s) < 40:
                ax.text(lx, ly, s, color=rgb, fontsize=5.5, ha="left",
                        va="bottom", zorder=20, clip_on=True)
    ax.set_xlim(x0, x1)
    ax.set_ylim(y0, y1)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xticks([])
    ax.set_yticks([])
    return (x0, y0, x1, y1)


def crop_png(path: str, cx: float, cy: float, hw: float, out: str,
             hh: float | None = None, dpi: int = 160) -> str:
    fig, ax = plt.subplots(figsize=(10, 10 * ((hh or hw) / hw)))
    draw(ax, path, cx, cy, hw, hh)
    fig.savefig(out, dpi=dpi, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return out


def handle_zentrum(path: str, handle: str) -> tuple[float, float]:
    doc = ezdxf.readfile(path)
    e = doc.entitydb.get(handle)
    if e is None:
        raise SystemExit(f"Handle {handle} nicht gefunden in {path}")
    ext = ezbbox.extents([e], fast=False)
    if not ext.has_data:
        raise SystemExit(f"Handle {handle}: keine Geometrie")
    return (ext.center.x, ext.center.y)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("dxf")
    ap.add_argument("--xy", nargs=2, type=float, default=None)
    ap.add_argument("--handle", default=None)
    ap.add_argument("--hw", type=float, default=8000.0)
    ap.add_argument("--out", default=None)
    a = ap.parse_args(argv)
    if a.handle:
        cx, cy = handle_zentrum(a.dxf, a.handle)
    elif a.xy:
        cx, cy = a.xy
    else:
        ap.error("--xy oder --handle angeben")
    out = a.out or str(Path(a.dxf).with_suffix("")) + f"_crop_{int(cx)}_{int(cy)}.png"
    crop_png(a.dxf, cx, cy, a.hw, out)
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
