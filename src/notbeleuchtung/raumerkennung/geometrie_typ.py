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
from collections.abc import Sequence

from ezdxf import bbox
from shapely.geometry import LineString, MultiPoint, Point, Polygon
from shapely.ops import unary_union

from notbeleuchtung.hauptengine.contracts.raum_modell import Raum

from .dxf_load import DxfPlan
from .stiegenhaus import _wcs_pts

XY = tuple[float, float]

_STAIR_BLOCK = re.compile(r"stiege|stieg|trepp|stair", re.IGNORECASE)
# Fluchtweg-Layer je CAD-Familie (Mollgasse 09-WEG, Fischamender A_Fluchtweg).
_FLUCHTWEG_LAYER = re.compile(r"09-WEG|A_Fluchtweg|Fluchtweg", re.IGNORECASE)
_GANG_PUFFER_MM = 750.0         # Halbbreite → ~1.5 m Korridor um die Fluchtweg-Achse
_MIN_REALRAUM_M2 = 2.0          # kleiner = Fragment, kein „echter" Raum zum Typisieren
# Diagnose Rennweg U1, Slice S9: Anteil der gedrehten Treppen-Hülle, den vorhandene
# Räume decken müssen, damit kein eigener STIEGENHAUS-Raum angehängt wird.
# ponytail: fester Knopf; Rennweg-Hüllen beim Aufruf 0,846-0,988 gedeckt (DG2 `Stair_2` 0,846).
# Vor Merge auf Muthgasse/Mollgasse/Barawitzka nachmessen (F19), sonst bei neuer Familie.
_ANTEIL_NEU = 0.8


def _flaeche_m2(poly: list[XY]) -> float:
    s = 0.0
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        s += x1 * y2 - x2 * y1
    return abs(s) / 2.0 / 1_000_000.0


def stiege_rechtecke(plan: DxfPlan) -> list[tuple[list[XY], XY, float]]:
    """Bounding-Rechtecke (mm) der Treppen-Blockreferenzen: (polygon, center, area_m2)."""
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
        rect = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
        out.append((rect, ((x0 + x1) / 2, (y0 + y1) / 2), _flaeche_m2(rect)))
    return out


def stiege_huellen(plan: DxfPlan) -> list[Polygon]:
    """Konvexe Hüllen (mm) der Linien in Treppen-Blockreferenzen — Drehung bleibt erhalten."""
    out: list[Polygon] = []
    f = plan.factor
    for e in plan.space:
        if e.dxftype() != "INSERT" or not _STAIR_BLOCK.search(e.dxf.name or ""):
            continue
        try:
            pts = [p for v in e.virtual_entities() for p in _wcs_pts(v, f)]
        except Exception as exc:  # noqa: BLE001 — kaputter Block darf nicht killen
            print(f"   virtual_entities({e.dxf.name}) fehlgeschlagen: {exc}")
            continue
        huelle = MultiPoint(pts).convex_hull if len(pts) >= 3 else None
        if huelle is not None and huelle.area > 0:
            out.append(huelle)
    return out


def typisiere_stiegenhaus(raeume: list[Raum], stiegen: list[tuple[list[XY], XY, float]],
                          huellen: Sequence[Polygon] = ()) -> list[Raum]:
    """STIEGENHAUS setzen: echten Raum um den Treppen-Anker typisieren, sonst Raum anlegen.

    Ein Treppen-Anker in einem echten (≥2 m²) noch untypisierten Raum färbt diesen;
    fehlt ein solcher Raum (Fragmente/label-los), wird das Treppen-Rechteck selbst
    ein STIEGENHAUS-Raum — außer die gedrehte Treppen-Hülle (``huellen``) ist schon
    zu ``_ANTEIL_NEU`` von Räumen gedeckt. Bereits typisierte Räume bleiben unangetastet.
    """
    polys = [(r, Polygon(r.polygon_mm)) for r in raeume if len(r.polygon_mm) >= 3]
    raum_union = None
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
            # Diagnose Rennweg U1, Slice S9: Die Bbox-Mitte einer gedrehten Treppe kann
            # in einer Wand liegen (DG2 `Stair_2`), obwohl Räume die Treppe schon
            # decken. Deckung darum an der eigenen Hülle messen (größte Hülle im Rechteck).
            fp = max((h for h in huellen if Polygon(rect).buffer(1.0).covers(h)),
                     key=lambda h: h.area, default=None)
            if fp is not None:
                if raum_union is None:
                    raum_union = unary_union([p.buffer(0) for _r, p in polys])
                if fp.intersection(raum_union).area / fp.area >= _ANTEIL_NEU:
                    continue
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
    for e in plan.space:
        if not _FLUCHTWEG_LAYER.search(e.dxf.layer):
            continue
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
    raeume = typisiere_stiegenhaus(raeume, stiege_rechtecke(plan), stiege_huellen(plan))
    return typisiere_gang(raeume, gang_polygone(plan))
