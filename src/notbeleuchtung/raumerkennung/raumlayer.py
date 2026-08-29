"""raumlayer — Räume direkt aus dedizierten Raum-Layern lesen.

Drei der vier Input-Familien liefern **fertige Raum-Polygone** auf eigenen Layern
— deterministisch und auditierbar, ohne Wand-Polygonisierung/Clustering:

    Barawitzka    `_815 Raumbegrenzung`  (geschl. LWPOLYLINE) + `_810 Raum` (MTEXT)
    Herrenholz/   `810 Raum` / `811 Raum 2`  (geschl. LWPOLYLINE + INSERT ROOM_NAME)
    Baufeld E2
    Fischamender  `A_Raeume_`  (geschl. LWPOLYLINE) + `A_Raeume_Beschriftung_` (MTEXT)

Raumname kommt aus dem `ROOM_NAME`-ATTRIB (Herrenholz/Baufeld) oder aus einem
MTEXT-Stempel im Polygon (Barawitzka/Fischamender) → ``classify_room``. Fehlt ein
Raum-Layer (Mollgasse), liefert der Reader ``[]`` und der Provider fällt auf die
Wand-Polygonisierung zurück.
"""
from __future__ import annotations

import re

from shapely.geometry import Point, Polygon

from notbeleuchtung.hauptengine.contracts.raum_modell import Raum

from .dxf_load import DxfPlan
from .raumtyp import raumtyp_flags

# Layer mit Raum-Polygonen (Icon-Duplikate + reine Text-Layer werden ignoriert).
_ROOM_LAYER = re.compile(r"81\d\s*Raum|Raumbegrenzung|A_Raeume", re.IGNORECASE)
_ROOM_LAYER_EXCLUDE = re.compile(r"Icon", re.IGNORECASE)

_MIN_FLAECHE_M2 = 1.0
XY = tuple[float, float]


def _ist_raum_layer(name: str) -> bool:
    return bool(_ROOM_LAYER.search(name)) and not _ROOM_LAYER_EXCLUDE.search(name)


def hat_raum_layer(plan: DxfPlan) -> bool:
    """True, wenn der Plan geschlossene Raum-Polygone auf einem Raum-Layer trägt."""
    return any(True for _ in _raum_polygone(plan))


def _flaeche_m2(poly: list[XY]) -> float:
    s = 0.0
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        s += x1 * y2 - x2 * y1
    return abs(s) / 2.0 / 1_000_000.0


def _raum_polygone(plan: DxfPlan):
    """Geschlossene LW/POLYLINE auf Raum-Layern → Polygon (mm), Fläche ≥ Minimum."""
    for e in plan.entities():
        if not _ist_raum_layer(e.dxf.layer):
            continue
        if e.dxftype() not in ("LWPOLYLINE", "POLYLINE"):
            continue
        if not getattr(e, "closed", False):
            continue
        poly = plan.entity_points(e)
        if len(poly) >= 3 and _flaeche_m2(poly) >= _MIN_FLAECHE_M2:
            yield poly


def _raum_stempel(plan: DxfPlan) -> list[tuple[str, XY]]:
    """(Name, xy_mm): ROOM_NAME-ATTRIBs + MTEXT/TEXT auf Raum-Layern."""
    out: list[tuple[str, XY]] = []
    for e in plan.entities():
        t = e.dxftype()
        if t == "INSERT" and e.attribs:
            for a in e.attribs:
                if "ROOM_NAME" in a.dxf.tag.upper() and a.dxf.text.strip():
                    out.append((a.dxf.text.strip(), plan._scale(e.dxf.insert)))
                    break
        elif t in ("MTEXT", "TEXT") and _ist_raum_layer(e.dxf.layer):
            txt = e.plain_text() if t == "MTEXT" else e.dxf.text
            if txt and txt.strip():
                out.append((txt.strip(), plan._scale(e.dxf.insert)))
    return out


def raeume_aus_layer(plan: DxfPlan) -> list[Raum]:
    """Räume aus den Raum-Layern; ``[]`` wenn keine Raum-Polygone vorhanden."""
    polygone = list(_raum_polygone(plan))
    if not polygone:
        return []
    stempel = _raum_stempel(plan)
    raeume: list[Raum] = []
    for i, poly in enumerate(polygone, start=1):
        shp = Polygon(poly)
        raum_typ, flucht, communal = "", False, False
        for txt, xy in stempel:
            if shp.covers(Point(xy)):
                tf = raumtyp_flags(txt)
                if tf is not None:
                    raum_typ, flucht, communal = tf
                    break
        raeume.append(
            Raum(
                id=f"raum_{i}",
                raum_typ=raum_typ,
                polygon_mm=[(float(x), float(y)) for x, y in poly],
                flaeche_m2=_flaeche_m2(poly),
                ist_fluchtweg=flucht,
                ist_communal=communal,
            )
        )
    return raeume
