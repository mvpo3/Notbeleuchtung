"""wandkoerper — Wand-/Bauteilkörper nach ERSCHEINUNGSBILD, layerunabhängig.

Quellen: alle HATCHes aus Modelspace + Blockdefinitionen (virtual_entities-Walk,
Tiefe ≤3 — die Rennweg-Wall-Blöcke liegen in Weltkoordinaten, base_point ==
Insert-Punkt, d.h. der Walk liefert bereits korrekte Koordinaten ohne doppelten
Offset). Ein Hatch zählt als Wandkörper, wenn sein Material bauteilartig ist
(Wörterbuch-Match), sein Polygon wandtypisch schmal ist (50–600 mm bei ≥0.05 m²)
oder sein Layer ein Wand-Hinweis ist. Möbel/Plangrafik und duplizierte
Planvarianten (Barawitzka Icon_1/Icon_3) werden ausgeschlossen.

Fallback: parallele Doppellinien auf Wand-Layern → Rechteck-Körper (leere
Architektur-Inputs ohne Hatches).

Grenze: liefert 2D-Körper in mm; keine Öffnungs-/Türlogik (das macht tueren.py).
"""
from __future__ import annotations

import math
import os
import re
from dataclasses import dataclass
from itertools import pairwise

from shapely.geometry import MultiPolygon, Polygon
from shapely.ops import unary_union

from notbeleuchtung.hauptengine.contracts.raum_modell import BBox

from .dxf_load import WALL_PATTERN, DxfPlan
from .material_matching import _LAYER_HINWEISE, bestimme_material, signatur_aus_hatch
from .stempel_anker import finde_stempel

XY = tuple[float, float]

# Bauteilartige Wörterbuch-Materialien (Wand/Schacht/Dämmung-Familie).
_BAUTEIL_MATERIAL = re.compile(
    r"STAHLBETON|ZIEGEL|GIPSKARTON|YTONG|SCHACHT|WAERMEDAEMM|D[ÄA]MM|ALU_GLAS")
# Wand-Layer-Hinweis (tolerant gegen cp-dekodierte Umlaute: 'Innenw?nde').
_WAND_LAYER = re.compile(
    r"\bwand\b|w.nde|schacht|\bSTB\b|(?<![A-Z0-9])GK\b", re.IGNORECASE)
# Möbel/Einrichtung/Plangrafik/Bodenbeläge sind nie Wände (Rennweg New_060/
# New_255; Mollgasse LEG-LILA/LEG-GRÜN = Belagsflächen, Rigol = Kiesrinne).
_NEGATIV_LAYER = re.compile(
    r"New_060|New_255|M(?:Ö|OE|.)BEL|EINRICHT|MOBILIAR|PLANGRAFIK"
    r"|LEG-LILA|LEG-GR.N|RIGOL|BELAG", re.IGNORECASE)

_BREITE_MIN_MM, _BREITE_MAX_MM = 50.0, 600.0
_MIN_FLAECHE_MM2 = 5e4  # 0.05 m²

# Varianten-Erkennung (Muster wie scripts/plan_pruefen.py — Barawitzka trägt
# dieselbe Etage mehrfach; nur die Variante mit den Raumstempeln zählt).
_VARIANTE_RX = re.compile(r"^(.*_)\d+ ")


@dataclass
class Wandkoerper:
    """Ein Wand-/Bauteilpolygon in mm."""

    polygon_mm: list[XY]
    material: str            # Wörterbuch-Material oder 'UNBEKANNT'
    layer: str
    quelle: str              # 'msp' | 'block:<name>'
    breite_mm: float         # Kurzseite des minimal rotierten Rechtecks


def _varianten_prefix(plan: DxfPlan) -> str | None:
    """Layer-Prefix der Stempel-Variante (z.B. '0._EG PP_2_'), sonst None."""
    layers = [s.layer for s in finde_stempel(plan) if s.layer]
    if not layers:
        return None
    m = _VARIANTE_RX.match(os.path.commonprefix(layers))
    return m.group(1) if m and len(m.group(1)) >= 4 else None


def _ist_duplikat_variante(layer: str, prefix: str | None) -> bool:
    if not prefix or layer.startswith(prefix):
        return False
    m = _VARIANTE_RX.match(layer)
    return bool(m and len(m.group(1)) >= 4)


def _shoelace(pts: list[XY]) -> float:
    return 0.5 * abs(sum(x1 * y2 - x2 * y1
                         for (x1, y1), (x2, y2) in zip(pts, pts[1:] + pts[:1])))


def _hatch_punkte(hatch) -> list[XY]:
    """Größter Boundary-Pfad des HATCH, flach (Quell-Einheiten)."""
    import ezdxf.path
    best: list[XY] = []
    best_a = -1.0
    for p in ezdxf.path.from_hatch(hatch):
        pts = [(float(v.x), float(v.y)) for v in p.flattening(10)]
        a = _shoelace(pts) if len(pts) >= 3 else 0.0
        if a > best_a:
            best, best_a = pts, a
    return best


def _kurzseite(poly: Polygon) -> float:
    """Kurzseite des minimal rotierten Rechtecks (= Wandbreite bei Wandkörpern)."""
    r = poly.minimum_rotated_rectangle
    if r.geom_type != "Polygon":
        return 0.0
    c = list(r.exterior.coords)
    return min(math.dist(c[0], c[1]), math.dist(c[1], c[2]))


def _heile(pts_mm: list[XY]) -> Polygon | None:
    """Punkte → Polygon, buffer(0)-Heilung; None wenn degeneriert."""
    if len(pts_mm) < 3:
        return None
    poly = Polygon(pts_mm).buffer(0)
    if poly.is_empty:
        return None
    if poly.geom_type != "Polygon":
        poly = max(poly.geoms, key=lambda g: g.area)
    return poly if poly.area > 0 else None


def _ist_wandlayer(plan: DxfPlan, layer: str) -> bool:
    return (layer in plan.wall_layers or bool(WALL_PATTERN.search(layer))
            or bool(_WAND_LAYER.search(layer)))


def finde_wandkoerper(plan: DxfPlan) -> list[Wandkoerper]:
    """Alle Wandkörper des Plans (Erscheinungsbild-basiert, layerunabhängig)."""
    prefix = _varianten_prefix(plan)
    out: list[Wandkoerper] = []
    seen: set[tuple[float, float, float]] = set()

    def _hatch_pruefen(h, quelle: str) -> None:
        layer = str(h.dxf.layer)
        if _NEGATIV_LAYER.search(layer) or _ist_duplikat_variante(layer, prefix):
            return
        pts = _hatch_punkte(h)
        poly = _heile([(x * plan.factor, y * plan.factor) for x, y in pts])
        if poly is None:
            return
        sig = signatur_aus_hatch(h)
        material = bestimme_material(sig, layer=layer).material
        if material == "UNBEKANNT" and not sig.linien:
            # SOLID ohne Muster: Material steckt ggf. im Layer-Namen (Barawitzka).
            for rx, ziel in _LAYER_HINWEISE:
                if rx.search(layer):
                    material = ziel
                    break
        breite = _kurzseite(poly)
        schmal = (_BREITE_MIN_MM <= breite <= _BREITE_MAX_MM
                  and poly.area >= _MIN_FLAECHE_MM2)
        if not (_BAUTEIL_MATERIAL.search(material) or schmal
                or _ist_wandlayer(plan, layer)):
            return
        key = (round(poly.area, 1), round(poly.centroid.x, 1), round(poly.centroid.y, 1))
        if key in seen:  # identische Polygone (Kopien/Doppel-Hatches) dedupen
            return
        seen.add(key)
        out.append(Wandkoerper(polygon_mm=list(poly.exterior.coords),
                               material=material, layer=layer, quelle=quelle,
                               breite_mm=round(breite, 1)))

    def _walk(entities, quelle: str, tiefe: int = 0) -> None:
        for e in entities:
            t = e.dxftype()
            if t == "HATCH":
                _hatch_pruefen(e, quelle)
            elif t == "INSERT" and tiefe < 3:
                try:
                    _walk(e.virtual_entities(), f"block:{e.dxf.name}", tiefe + 1)
                except Exception:  # noqa: BLE001, S110 — kaputter Block killt den Scan nicht
                    pass

    _walk(plan.space, "msp")
    if len(out) < 5:
        out.extend(_doppellinien(plan))
    return out


# ── Fallback: Doppellinien-Wände ─────────────────────────────────────────────
_PARALLEL_TOL_RAD = math.radians(2.0)
_MIN_UEBERLAPPUNG_MM = 200.0


def _segmente(plan: DxfPlan) -> list[tuple[XY, XY]]:
    segs: list[tuple[XY, XY]] = []
    for e in plan.wall_entities():
        if e.dxftype() not in ("LINE", "LWPOLYLINE", "POLYLINE"):
            continue
        pts = plan.entity_points(e)
        segs.extend(pairwise(pts))
    return segs


def _doppellinien(plan: DxfPlan) -> list[Wandkoerper]:
    """Parallele Linien-Paare (Abstand 50–600 mm) auf Wand-Layern → Rechtecke.

    ponytail: O(n²)-Paarvergleich — Spatial-Index erst, wenn Pläne >5k Segmente haben.
    """
    segs = _segmente(plan)
    out: list[Wandkoerper] = []
    for i, (a1, a2) in enumerate(segs):
        ux, uy = a2[0] - a1[0], a2[1] - a1[1]
        la = math.hypot(ux, uy)
        if la < _MIN_UEBERLAPPUNG_MM:
            continue
        ux, uy = ux / la, uy / la
        wa = math.atan2(uy, ux) % math.pi
        for b1, b2 in segs[i + 1:]:
            lb = math.dist(b1, b2)
            if lb < _MIN_UEBERLAPPUNG_MM:
                continue
            wb = math.atan2(b2[1] - b1[1], b2[0] - b1[0]) % math.pi
            dw = abs(wa - wb)
            if min(dw, math.pi - dw) > _PARALLEL_TOL_RAD:
                continue
            # Senkrechter Abstand + Überlappung entlang der a-Richtung.
            dx, dy = b1[0] - a1[0], b1[1] - a1[1]
            gap = abs(-uy * dx + ux * dy)
            if not (_BREITE_MIN_MM <= gap <= _BREITE_MAX_MM):
                continue
            sb = sorted(ux * (p[0] - a1[0]) + uy * (p[1] - a1[1]) for p in (b1, b2))
            s0, s1 = max(0.0, sb[0]), min(la, sb[1])
            if s1 - s0 < _MIN_UEBERLAPPUNG_MM:
                continue
            off = (dx - (ux * dx + uy * dy) * ux, dy - (ux * dx + uy * dy) * uy)
            pa0 = (a1[0] + s0 * ux, a1[1] + s0 * uy)
            pa1 = (a1[0] + s1 * ux, a1[1] + s1 * uy)
            rect = [pa0, pa1, (pa1[0] + off[0], pa1[1] + off[1]),
                    (pa0[0] + off[0], pa0[1] + off[1])]
            out.append(Wandkoerper(polygon_mm=rect, material="UNBEKANNT",
                                   layer="", quelle="msp", breite_mm=round(gap, 1)))
    return out


# ── Hilfsfunktionen ──────────────────────────────────────────────────────────
def wand_union(koerper: list[Wandkoerper], puffer_mm: float = 25.0) -> MultiPolygon:
    """Verschmolzene Wandflächen: buffer(+p)-union-buffer(-p) schließt Fugen ≤2p."""
    if not koerper:
        return MultiPolygon()
    u = unary_union([Polygon(k.polygon_mm).buffer(puffer_mm) for k in koerper])
    u = u.buffer(-puffer_mm)
    if u.geom_type == "Polygon":
        return MultiPolygon([u])
    if u.geom_type == "MultiPolygon":
        return u
    return MultiPolygon()


def aussenkontur(koerper: list[Wandkoerper], d_mm: float = 600.0) -> Polygon:
    """Außenkontur des größten zusammenhängenden Bauteils: Union morphologisch
    geschlossen (buffer(+d).buffer(-d)) — überbrückt Tür-/Fensteröffnungen."""
    if not koerper:
        return Polygon()
    u = unary_union([Polygon(k.polygon_mm) for k in koerper])
    u = u.buffer(d_mm).buffer(-d_mm)
    if u.geom_type == "MultiPolygon":
        u = max(u.geoms, key=lambda g: g.area)
    if u.geom_type != "Polygon":
        return Polygon()
    return Polygon(u.exterior)


def bounds_aus_wandkoerpern(koerper: list[Wandkoerper]) -> BBox:
    """Bounding-Box (mm) über alle Wandkörper — Fallback, wenn ``bounds_mm``
    keine Wand-Linien findet (Hatch-only-Pläne wie Rennweg)."""
    if not koerper:
        raise ValueError("Keine Wandkörper — Plan ohne erkennbare Wände.")
    xs = [x for k in koerper for x, _ in k.polygon_mm]
    ys = [y for k in koerper for _, y in k.polygon_mm]
    return BBox(min_xy=(min(xs), min(ys)), max_xy=(max(xs), max(ys)))
