"""Rekonstruiert das Wohnbau-RaumModell aus den gerenderten v8-DXFs.

Der Generator (spec_builder_v8.py, Session-Scratchpad) ist verloren; die
Owner-abgenommenen Outputs output/wohnbau_v8_*.dxf tragen aber alles:
Raum-Polygone+Labels (ARCH_Raum), Türen als Schwelle/Blatt/Bogen (ARCH_Tuer,
Doppel-Schwelle=Notausgang), Fluchtweg-Segmente (ARCH_Fluchtweg).
"""
import json
import math
import re
import sys
from pathlib import Path

import ezdxf

FLOORS = {"EG": "wohnbau_v8_eg.dxf", "1OG": "wohnbau_v8_og1.dxf", "DG": "wohnbau_v8_dg.dxf"}
FLUCHTWEG_TYPEN = {"GANG", "STIEGENHAUS", "FLUR", "KORRIDOR"}


def _dist_point_seg(p, a, b):
    ax, ay = a
    bx, by = b
    px, py = p
    dx, dy = bx - ax, by - ay
    ll = dx * dx + dy * dy
    t = 0.0 if ll == 0 else max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / ll))
    cx, cy = ax + t * dx, ay + t * dy
    return math.hypot(px - cx, py - cy)


def _dist_poly(p, poly):
    return min(_dist_point_seg(p, poly[i], poly[(i + 1) % len(poly)]) for i in range(len(poly)))


def _centroid(poly):
    return (sum(p[0] for p in poly) / len(poly), sum(p[1] for p in poly) / len(poly))


def _area_m2(poly):
    s = 0.0
    for i in range(len(poly)):
        x0, y0 = poly[i]
        x1, y1 = poly[(i + 1) % len(poly)]
        s += x0 * y1 - x1 * y0
    return abs(s) / 2.0 / 1e6


def extract(floor, path):
    doc = ezdxf.readfile(path)
    msp = doc.modelspace()

    polys, labels = [], []
    for e in msp:
        if e.dxf.layer == "ARCH_Raum":
            if e.dxftype() == "LWPOLYLINE":
                polys.append([(p[0], p[1]) for p in e.get_points()])
            elif e.dxftype() == "MTEXT":
                m = re.match(r"(.+?) \((.+?)\)$", e.plain_text().strip())
                if m:
                    labels.append((m.group(1), m.group(2), (e.dxf.insert.x, e.dxf.insert.y)))

    raeume = []
    for typ, rid, (lx, ly) in labels:
        poly = min(polys, key=lambda pl: math.hypot(_centroid(pl)[0] - lx, _centroid(pl)[1] - ly))
        raeume.append({
            "id": rid, "raum_typ": typ, "polygon_mm": [list(p) for p in poly],
            "flaeche_m2": round(_area_m2(poly), 2),
            "ist_fluchtweg": typ.upper() in FLUCHTWEG_TYPEN,
            "ist_communal": typ.upper() == "STIEGENHAUS",
        })

    arcs, lines = [], []
    for e in msp:
        if e.dxf.layer != "ARCH_Tuer":
            continue
        if e.dxftype() == "ARC":
            arcs.append(((e.dxf.center.x, e.dxf.center.y), e.dxf.radius))
        elif e.dxftype() == "LINE":
            lines.append(((e.dxf.start.x, e.dxf.start.y), (e.dxf.end.x, e.dxf.end.y)))

    def _near(a, b, tol=1.0):
        return math.hypot(a[0] - b[0], a[1] - b[1]) < tol

    used = set()
    tueren = []
    for di, (center, radius) in enumerate(arcs):
        cands = [i for i, (s, e) in enumerate(lines)
                 if i not in used and (_near(s, center) or _near(e, center))
                 and abs(math.hypot(e[0] - s[0], e[1] - s[1]) - radius) < 2.0]
        if len(cands) < 2:
            print(f"  ⚠ Tür {di}: nur {len(cands)} Linien am Angel", file=sys.stderr)
            continue
        # Schwelle = Linie, deren Mitte an einer Raum-Kante liegt; Blatt ragt hinein.
        def mid(i):
            s, e = lines[i]
            return ((s[0] + e[0]) / 2, (s[1] + e[1]) / 2)
        cands.sort(key=lambda i: min(_dist_poly(mid(i), r["polygon_mm"]) for r in raeume))
        schwelle, blatt = cands[0], cands[1]
        used.update({schwelle, blatt})
        s, e = lines[schwelle]
        xy = mid(schwelle)
        wx, wy = (e[0] - s[0]) / radius, (e[1] - s[1]) / radius
        # Doppel-Schwelle (Offset 120) = Notausgang; als verbraucht markieren.
        notausgang = False
        for i, (ls, le) in enumerate(lines):
            if i in used:
                continue
            if abs(math.hypot(le[0] - ls[0], le[1] - ls[1]) - radius) < 2.0 and \
               110 < _dist_point_seg(((ls[0] + le[0]) / 2, (ls[1] + le[1]) / 2), s, e) < 130:
                notausgang = True
                used.add(i)
                break
        # Schwenkrichtung aus Blatt-Endpunkt vs. Wand-Normale (rechts = +Normale).
        bs, be = lines[blatt]
        tip = be if _near(bs, center) else bs
        nx, ny = -wy, wx
        rechts = (tip[0] - center[0]) * nx + (tip[1] - center[1]) * ny > 0
        anlieger = sorted(
            (r["id"] for r in raeume if _dist_poly(xy, r["polygon_mm"]) < 150.0),
            key=lambda rid: _dist_poly(xy, next(r["polygon_mm"] for r in raeume if r["id"] == rid)),
        )
        tueren.append({
            "id": f"tuer_{floor.lower()}_{len(tueren)+1}", "xy_mm": list(xy),
            "breite_mm": round(radius, 1),
            "von_raum": anlieger[0] if anlieger else None,
            "nach_raum": anlieger[1] if len(anlieger) > 1 else None,
            "ist_notausgang": notausgang,
            "schwenk_richtung": "rechts" if rechts else "links",
        })
    rest = [i for i in range(len(lines)) if i not in used]
    if rest:
        print(f"  ⚠ {len(rest)} Tür-Linien unzugeordnet", file=sys.stderr)

    segmente = []
    for e in msp:
        if e.dxf.layer == "ARCH_Fluchtweg" and e.dxftype() == "LWPOLYLINE":
            pts = [(p[0], p[1]) for p in e.get_points()]
            laenge = sum(math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1])
                         for i in range(len(pts) - 1))
            segmente.append({
                "segment_id": f"seg_{floor.lower()}_{len(segmente)+1}",
                "polyline_mm": [list(p) for p in pts],
                "laenge_mm": round(laenge, 1),
                "reason": "long_run",
            })

    ausgaenge = [
        {"id": f"exit_{floor.lower()}_{i+1}", "xy_mm": t["xy_mm"], "typ": "final_exit"}
        for i, t in enumerate(tueren) if t["ist_notausgang"]
    ]
    if not ausgaenge:  # Obergeschosse: Stiegenhaus ist der Ausgang
        ausgaenge = [
            {"id": f"stair_{floor.lower()}_{i+1}", "xy_mm": list(_centroid(r["polygon_mm"])),
             "typ": "stair_exit"}
            for i, r in enumerate(raeume) if r["raum_typ"].upper() == "STIEGENHAUS"
        ]

    xs = [p[0] for r in raeume for p in r["polygon_mm"]]
    ys = [p[1] for r in raeume for p in r["polygon_mm"]]
    return {
        "contract": "RaumModell",
        "contract_version": "1.1.0",
        "floor": floor,
        "coordinate_system": "mm",
        "_source": "rekonstruiert aus output/wohnbau_v8_*.dxf (Owner-abgenommen 2026-09-05)",
        "bounds_mm": {"min_xy": [min(xs), min(ys)], "max_xy": [max(xs), max(ys)]},
        "raeume": raeume,
        "tueren": tueren,
        "ausgaenge": ausgaenge,
        "zirkulation": {"nodes": [], "edges": [], "segmente": segmente},
    }


for floor, name in FLOORS.items():
    m = extract(floor, f"output/{name}")
    out = Path("tests/fixtures") / f"raum_modell_wohnbau_{floor.lower()}.json"
    out.write_text(json.dumps(m, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"{floor}: {len(m['raeume'])} Räume, {len(m['tueren'])} Türen "
          f"({sum(t['ist_notausgang'] for t in m['tueren'])} Notausgang), "
          f"{len(m['ausgaenge'])} Ausgänge ({m['ausgaenge'][0]['typ'] if m['ausgaenge'] else '-'}), "
          f"{len(m['zirkulation']['segmente'])} Segmente -> {out.name}")
