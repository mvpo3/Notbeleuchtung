"""geometrie_typ — Raumtyp aus Geometrie/Semantik-Layern statt Text-Stempel.

Viele echte Pläne (z.B. Mollgasse) tragen **keine** Raum-Typ-Labels als Text — die
Stempel existieren schlicht nicht (verifiziert: Mollgasse-EG = 566 Texte, 0 Raum-
Namen). `raumtyp.beschrifte_raeume` (Text) läuft dort ins Leere. Dieser Reader leitet
die sicherheitskritischen Typen **deterministisch aus Geometrie** ab:

    STIEGENHAUS ← STIEGE/Treppen-Blockreferenzen (INSERT)
    GANG        ← 09-WEG-Fluchtweg-Geometrie

Rein additiv, kein Norm-Urteil. Greift für jeden Raum-Pfad (Raum-Layer wie Wand-
Polygonisierung): deckt ein echter Raum den Anker, wird sein leerer `raum_typ`
gesetzt; deckt keiner (fragmentierte/label-lose Pläne), entsteht ein eigener Raum
aus der Anker-Geometrie.
"""
from __future__ import annotations

import re

from ezdxf import bbox
from shapely.geometry import LineString, Point, Polygon
from shapely.ops import unary_union

from notbeleuchtung.hauptengine.contracts.raum_modell import Raum

from .dxf_load import FLUCHTWEG_PATTERN, STIEGE_PATTERN, DxfPlan

XY = tuple[float, float]

_STAIR_BLOCK = re.compile(r"stiege|stieg|trepp|stair", re.IGNORECASE)
# Beschriftungs-/Bemaßungs-Layer der Treppe tragen keine Treppen-Geometrie.
_STIEGE_LAYER_EXCLUDE = re.compile(r"ANNO|IDEN|MBND|Beschriftung|Text", re.IGNORECASE)
_STIEGE_CLUSTER_MM = 4000.0     # Stufen-Linien dichter als das sind dieselbe Treppe
_STIEGE_MIN_M2, _STIEGE_MAX_M2 = 3.0, 80.0   # plausible Treppenlauf-Grundfläche
_GANG_PUFFER_MM = 750.0         # Halbbreite → ~1.5 m Korridor um die Fluchtweg-Achse
_MIN_REALRAUM_M2 = 2.0          # kleiner = Fragment, kein „echter" Raum zum Typisieren


def _flaeche_m2(poly: list[XY]) -> float:
    s = 0.0
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        s += x1 * y2 - x2 * y1
    return abs(s) / 2.0 / 1_000_000.0


def _block_stiegen(plan: DxfPlan) -> list[tuple[list[XY], XY, float]]:
    """Treppen als benannte Blockreferenz (Mollgasse ``STIEGE``)."""
    out: list[tuple[list[XY], XY, float]] = []
    f = plan.factor
    for e in plan.space:
        if e.dxftype() != "INSERT" or not _STAIR_BLOCK.search(e.dxf.name or ""):
            continue
        b = bbox.extents([e])          # leere/fehlende Geometrie → has_data == False
        if not b.has_data:
            continue
        x0, y0 = b.extmin[0] * f, b.extmin[1] * f
        x1, y1 = b.extmax[0] * f, b.extmax[1] * f
        if x1 <= x0 or y1 <= y0:
            continue
        out.append(_als_rechteck(x0, y0, x1, y1))
    return out


def _als_rechteck(x0: float, y0: float, x1: float, y1: float) -> tuple[list[XY], XY, float]:
    rect = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    return rect, ((x0 + x1) / 2, (y0 + y1) / 2), _flaeche_m2(rect)


def _layer_stiegen(plan: DxfPlan) -> list[tuple[list[XY], XY, float]]:
    """Treppen aus dedizierten Treppen-Layern (Fischamender ``S-STRS``, ArchiCAD
    ``410 Treppe``) — dort gibt es keinen Blocknamen-Hinweis, nur Layer-Geometrie.

    Die Layer tragen die einzelnen Stufen-Linien, nicht eine Treppe als Ganzes.
    Deshalb werden die Stützpunkte greedy zu Clustern zusammengezogen (Treppen
    liegen räumlich weit auseinander) und jedes Cluster zum Rechteck geschlossen.
    """
    boxen: list[list[float]] = []       # [x0, y0, x1, y1] je Cluster
    for e in plan.entities_matching(STIEGE_PATTERN):
        if _STIEGE_LAYER_EXCLUDE.search(e.dxf.layer):
            continue
        for x, y in plan.entity_points(e):
            passend = next(
                (b for b in boxen
                 if b[0] - _STIEGE_CLUSTER_MM <= x <= b[2] + _STIEGE_CLUSTER_MM
                 and b[1] - _STIEGE_CLUSTER_MM <= y <= b[3] + _STIEGE_CLUSTER_MM),
                None,
            )
            if passend is None:
                boxen.append([x, y, x, y])
            else:
                passend[0] = min(passend[0], x)
                passend[1] = min(passend[1], y)
                passend[2] = max(passend[2], x)
                passend[3] = max(passend[3], y)

    out: list[tuple[list[XY], XY, float]] = []
    for x0, y0, x1, y1 in boxen:
        if x1 <= x0 or y1 <= y0:
            continue
        eintrag = _als_rechteck(x0, y0, x1, y1)
        if _STIEGE_MIN_M2 <= eintrag[2] <= _STIEGE_MAX_M2:
            out.append(eintrag)
    return out


def stiege_rechtecke(plan: DxfPlan) -> list[tuple[list[XY], XY, float]]:
    """Bounding-Rechtecke (mm) der Treppen: (polygon, center, area_m2).

    Benannte Blöcke zuerst (präzise), sonst die Treppen-Layer der übrigen
    CAD-Familien.
    """
    return _block_stiegen(plan) or _layer_stiegen(plan)


def typisiere_stiegenhaus(raeume: list[Raum], stiegen: list[tuple[list[XY], XY, float]]) -> list[Raum]:
    """STIEGENHAUS setzen: echten Raum um den Treppen-Anker typisieren, sonst Raum anlegen.

    Ein Treppen-Anker in einem echten (≥2 m²) noch untypisierten Raum färbt diesen;
    fehlt ein solcher Raum (Fragmente/label-los), wird das Treppen-Rechteck selbst
    ein STIEGENHAUS-Raum. Bereits typisierte Räume bleiben unangetastet.
    """
    polys = [(r, Polygon(r.polygon_mm)) for r in raeume if len(r.polygon_mm) >= 3]
    for i, (rect, center, area) in enumerate(stiegen, start=1):
        pt = Point(center)
        cover = next(
            (r for r, poly in polys
             if poly.area / 1_000_000.0 >= _MIN_REALRAUM_M2 and poly.covers(pt)),
            None,
        )
        if cover is not None:
            if not (cover.raum_typ or "").strip():
                cover.raum_typ = "STIEGENHAUS"
                cover.ist_fluchtweg = True
                cover.ist_communal = True
        else:
            raeume.append(
                Raum(
                    id=f"stiegenhaus_{i}",
                    raum_typ="STIEGENHAUS",
                    polygon_mm=rect,
                    flaeche_m2=area,
                    ist_fluchtweg=True,
                    ist_communal=True,
                )
            )
    return raeume


def gang_polygone(plan: DxfPlan, puffer_mm: float = _GANG_PUFFER_MM) -> list[list[XY]]:
    """Korridor-Polygone (mm) aus der Fluchtweg-Achse (09-WEG / A_Fluchtweg) gepuffert."""
    linien: list[LineString] = []
    for e in plan.entities_matching(FLUCHTWEG_PATTERN):
        if e.dxftype() in ("LINE", "LWPOLYLINE", "POLYLINE"):
            pts = plan.entity_points(e)
            if len(pts) >= 2:
                linien.append(LineString(pts))
    if not linien:
        return []
    korridor = unary_union([ln.buffer(puffer_mm) for ln in linien])
    teile = list(korridor.geoms) if hasattr(korridor, "geoms") else [korridor]
    return [
        [(float(x), float(y)) for x, y in p.exterior.coords[:-1]]
        for p in teile
        if p.area / 1_000_000.0 >= 1.0
    ]


def typisiere_gang(raeume: list[Raum], gang_polys: list[list[XY]]) -> list[Raum]:
    """GANG setzen: echte Räume, deren Zentrum im Fluchtweg-Korridor liegt, sonst Korridor-Raum.

    Läuft der Fluchtweg durch einen echten (≥2 m²) untypisierten Raum, wird dieser GANG;
    trifft der Korridor keinen echten Raum (Fragmente/label-los), wird der Korridor selbst
    ein GANG-Raum. Bereits typisierte Räume bleiben unangetastet.
    """
    if not gang_polys:
        return raeume
    korridore = [Polygon(p) for p in gang_polys]
    getroffen = False
    for r in raeume:
        if (r.raum_typ or "").strip() or len(r.polygon_mm) < 3:
            continue
        poly = Polygon(r.polygon_mm)
        if poly.area / 1_000_000.0 < _MIN_REALRAUM_M2:
            continue
        if any(k.covers(poly.centroid) for k in korridore):
            r.raum_typ = "GANG"
            r.ist_fluchtweg = True
            r.ist_communal = True
            getroffen = True
    if not getroffen:
        for i, p in enumerate(gang_polys, start=1):
            raeume.append(
                Raum(
                    id=f"gang_{i}",
                    raum_typ="GANG",
                    polygon_mm=p,
                    flaeche_m2=_flaeche_m2(p),
                    ist_fluchtweg=True,
                    ist_communal=True,
                )
            )
    return raeume


def typisiere_geometrisch(plan: DxfPlan, raeume: list[Raum]) -> list[Raum]:
    """Alle geometrischen Typ-Ableitungen: STIEGENHAUS (Treppen-Blöcke) + GANG (Fluchtweg)."""
    raeume = typisiere_stiegenhaus(raeume, stiege_rechtecke(plan))
    return typisiere_gang(raeume, gang_polygone(plan))
