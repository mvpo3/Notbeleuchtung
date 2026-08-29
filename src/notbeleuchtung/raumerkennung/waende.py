"""waende — Wand-Entities → Wand-Segmente → Raum-Polygone.

Sammelt LINE/LWPOLYLINE der Wand-Layer als Segmente (in mm) und übergibt sie
dem Port-Helfer ``extract_room_faces`` (planare Arrangement-Polygonisierung).
Jede geschlossene Fläche wird ein ``Raum``.

Grenze: naive Polygonisierung ohne Gap-Healing an Türöffnungen — leckt an
undoored Durchgängen. Robuste virtuelle Wände (Port `_build_virtual_walls_*`)
sind ein späterer Slice. Deterministisch nur auf sauber geschlossenen Wänden.
"""
from __future__ import annotations

from notbeleuchtung.hauptengine.contracts.raum_modell import Raum

from ._port.parsers.room_faces import Seg, extract_room_faces
from .dxf_load import WALL_PREFIXES, DxfPlan

XY = tuple[float, float]


def wand_segmente(plan: DxfPlan) -> list[Seg]:
    """Alle Wand-Layer-Entities als Liste von (p0, p1)-Segmenten in mm."""
    segs: list[Seg] = []
    for e in plan.entities(WALL_PREFIXES):
        t = e.dxftype()
        if t == "LINE":
            pts = plan.entity_points(e)
            if len(pts) == 2:
                segs.append((pts[0], pts[1]))
        elif t in ("LWPOLYLINE", "POLYLINE"):
            pts = plan.entity_points(e)
            for i in range(len(pts) - 1):
                segs.append((pts[i], pts[i + 1]))
            if getattr(e, "closed", False) and len(pts) >= 3:
                segs.append((pts[-1], pts[0]))
    return segs


def _flaeche_m2(poly: list[XY]) -> float:
    s = 0.0
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        s += x1 * y2 - x2 * y1
    return abs(s) / 2.0 / 1_000_000.0  # mm² → m²


def raeume_aus_waenden(plan: DxfPlan) -> list[Raum]:
    """Raum-Polygone aus den Wänden. IDs ``raum_1…``; Typ/Flags folgen in S3."""
    faces = extract_room_faces(wand_segmente(plan))
    raeume: list[Raum] = []
    for i, poly in enumerate(faces, start=1):
        raeume.append(
            Raum(
                id=f"raum_{i}",
                raum_typ="",
                polygon_mm=[(float(x), float(y)) for x, y in poly],
                flaeche_m2=_flaeche_m2(poly),
            )
        )
    return raeume
