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


def _stiege_anker(plan: DxfPlan) -> list[tuple[XY, Polygon | None]]:
    """Je Treppen-Blockreferenz: Bbox-Mitte (mm) und konvexe Hülle ihrer Linien.

    Die Hülle hält die Drehung fest, die `stiege_rechtecke` in der Achs-Bbox
    verliert (Diagnose Rennweg U1). ``None`` = Block ohne Liniengeometrie, also
    ein Zonenstempel (`Stiegenhaus__16`) und keine Treppe.
    """
    out: list[tuple[XY, Polygon | None]] = []
    f = plan.factor
    for e in plan.space:
        if e.dxftype() != "INSERT" or not _STAIR_BLOCK.search(e.dxf.name or ""):
            continue
        b = bbox.extents([e])          # leere/fehlende Geometrie → has_data == False
        if not b.has_data or b.extmax[0] <= b.extmin[0] or b.extmax[1] <= b.extmin[1]:
            continue                   # Index bleibt deckungsgleich mit `stiege_rechtecke`
        try:
            pts = [p for v in e.virtual_entities() for p in _wcs_pts(v, f)]
        except Exception as exc:  # noqa: BLE001 — kaputter Block darf nicht killen
            print(f"   virtual_entities({e.dxf.name}) fehlgeschlagen: {exc}")
            pts = []
        huelle = MultiPoint(pts).convex_hull if len(pts) >= 3 else None
        mitte = ((b.extmin[0] + b.extmax[0]) / 2 * f, (b.extmin[1] + b.extmax[1]) / 2 * f)
        out.append((mitte, huelle if huelle is not None and huelle.area > 0 else None))
    return out


def typisiere_stiegenhaus(raeume: list[Raum],
                          stiegen: Sequence[tuple[XY, Polygon | None]]) -> list[Raum]:
    """STIEGENHAUS setzen: echten Raum um den Treppen-Anker typisieren, sonst Raum anlegen.

    Ein Treppen-Anker (Bbox-Mitte) in einem echten (≥2 m²) noch untypisierten Raum
    färbt diesen. Deckt kein solcher Raum den Anker — Fragmente/label-los, oder die
    Bbox-Mitte einer gedrehten Treppe liegt in einer Wand (Diagnose Rennweg U1,
    DG2 `Stair_2`) —, entscheidet die gedrehte Hülle des Blocks: ohne Hülle ist er
    ein Zonenstempel und keine Treppe; ist die Hülle schon zu ``_ANTEIL_NEU`` von
    Räumen gedeckt, bleibt es bei den vorhandenen Räumen; sonst wird ihr ungedeckter
    Teil ein eigener STIEGENHAUS-Raum. Typisierte Räume bleiben unangetastet.
    """
    polys = [(r, Polygon(r.polygon_mm)) for r in raeume if len(r.polygon_mm) >= 3]
    raum_union = unary_union([p.buffer(0) for _r, p in polys])
    for i, (center, huelle) in enumerate(stiegen, start=1):
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
            continue
        if huelle is None:
            continue                                   # Zonenstempel, keine Treppe
        rest = huelle.difference(raum_union)           # ungedeckter Teil der gedrehten Hülle
        if 1.0 - rest.area / huelle.area >= _ANTEIL_NEU:
            continue                                   # Räume decken die Treppe schon
        teil = max(rest.geoms, key=lambda g: g.area) if hasattr(rest, "geoms") else rest
        # größte Komponente, Außenkontur: `Raum.polygon_mm` trägt genau einen Ring.
        polygon = [(float(x), float(y)) for x, y in teil.exterior.coords[:-1]]
        raeume.append(
            Raum(
                id=f"stiegenhaus_{i}",
                raum_typ="STIEGENHAUS",
                polygon_mm=polygon,
                flaeche_m2=_flaeche_m2(polygon),
                ist_fluchtweg=True,
                ist_communal=True,
            )
        )
        raum_union = unary_union([raum_union, teil])    # deckt die nächste Treppe mit
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
    raeume = typisiere_stiegenhaus(raeume, _stiege_anker(plan))
    return typisiere_gang(raeume, gang_polygone(plan))
