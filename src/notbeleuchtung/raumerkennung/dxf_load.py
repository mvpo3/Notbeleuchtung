"""dxf_load — DXF öffnen, Einheiten normalisieren, Layer/Geometrie-Zugriff.

Kapselt ezdxf: liefert einen ``DxfPlan`` (Dokument + der Layout-Raum, der die
Architektur trägt + Skalierungsfaktor auf mm). Der Rest des Packages arbeitet
nur mit mm — die Faktor-Multiplikation passiert genau hier.

Zwei Layouts (auto-erkannt):
- **Direct-Mode**: Wände liegen direkt im Modelspace (Mollgasse).
- **Wrapper-Mode**: Modelspace enthält einen INSERT, dessen Block die Wände
  trägt — dann wird der Block-Raum genommen (best-effort, ohne Transform).
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import ezdxf

from notbeleuchtung.hauptengine.contracts.raum_modell import BBox

# Wand-Layer über Projekt-Familien erkennen (Muster statt fixem Prefix):
#   Mollgasse:    02-TWA/02-ZWA/02-WDA-… (floor-agnostisch)
#   Fischamender: A_Waende / A_Wand…
#   ArchiCAD-num: „110/120/130 Wand …" (auch mit Präfix ``PP_2_110 Wand``,
#                 Suffix ``_Stift_Nr__N``)
WALL_PATTERN = re.compile(r"02-(?:TWA|ZWA|WDA)|A_Wa?ende|A_Wand|(?<!\d)1[123]0 Wand",
                          re.IGNORECASE)

# Rückwärts-kompatibel (Mollgasse-Tests/Direktnutzung).
WALL_PREFIXES: tuple[str, ...] = ("02-TWA", "02-ZWA", "02-WDA")

# $INSUNITS-Code → Faktor auf mm. 4=mm, 5=cm, 6=m; Rest → 1.0 (mm-Annahme).
_INSUNITS_TO_MM: dict[int, float] = {4: 1.0, 5: 10.0, 6: 1000.0}

XY = tuple[float, float]


# Plausible Ausdehnung eines Geschosses in mm (~15 m … ~500 m). Die 15-m-Untergrenze
# schließt die falsche Klein-Dekade aus (z.B. 8 m statt 80 m bei Meter-Plänen).
_SPAN_MIN_MM = 15_000.0
_SPAN_MAX_MM = 500_000.0


def _wall_layers(space) -> frozenset[str]:
    """Wand-Layer-Namen im Raum, per WALL_PATTERN erkannt (projekt-familien-agnostisch)."""
    return frozenset(
        e.dxf.layer for e in space if WALL_PATTERN.search(e.dxf.layer)
    )


def _raw_wall_span(space, wall_layers: frozenset[str]) -> float:
    """Größte Wand-Ausdehnung (dx/dy) in Quell-Einheiten (ohne Skalierung)."""
    xs: list[float] = []
    ys: list[float] = []
    for e in space:
        if e.dxf.layer not in wall_layers:
            continue
        t = e.dxftype()
        if t == "LINE":
            xs += [e.dxf.start[0], e.dxf.end[0]]
            ys += [e.dxf.start[1], e.dxf.end[1]]
        elif t == "LWPOLYLINE":
            for p in e.get_points("xy"):
                xs.append(p[0]); ys.append(p[1])
    if not xs:
        return 0.0
    return max(max(xs) - min(xs), max(ys) - min(ys))


_DOOR_MM = 900.0         # Tür-Blattbreite ≈ Schwenkbogen-Radius (Kalibrier-Anker)
_DOOR_MIN_MM, _DOOR_MAX_MM = 600.0, 1300.0


def _door_arc_factor(space) -> float | None:
    """mm-Faktor aus Tür-Schwenkbögen: wähle die Zehnerpotenz, die die MEISTEN
    ARC-Radien in den Tür-Blattbreiten-Bereich (600–1300 mm) legt.

    Robuster als die Geschoss-Ausdehnung (die ist zwischen 8 m und 80 m
    mehrdeutig); eine Tür ist immer ~0.9 m breit.
    """
    radii = [e.dxf.radius for e in space if e.dxftype() == "ARC" and e.dxf.radius > 0]
    if not radii:
        return None
    best, best_count = None, 0
    for factor in (1.0, 10.0, 100.0, 1000.0):
        count = sum(1 for r in radii if _DOOR_MIN_MM <= r * factor <= _DOOR_MAX_MM)
        if count > best_count:
            best, best_count = factor, count
    return best if best_count >= 3 else None


def _calibrate_factor(raw_span: float, space, doc: ezdxf.document.Drawing) -> float:
    """mm-Faktor aus der Geometrie ableiten, NICHT aus $INSUNITS (das lügt oft:
    leere Pläne in Metern, fertige in mm — beide mit gleichem Code).

    Die Geschoss-Ausdehnung (15–500 m) gibt die Kandidaten-Dekaden vor. Bleibt
    genau eine → nimm sie. Bleiben mehrere → Tür-Schwenkbogen-Radius (~0.9 m)
    als Tiebreak, sonst die kleinste (konservativ).
    """
    candidates = [
        f for f in (1.0, 10.0, 100.0, 1000.0, 10000.0)
        if raw_span > 0 and _SPAN_MIN_MM <= raw_span * f <= _SPAN_MAX_MM
    ]
    if len(candidates) == 1:
        return candidates[0]
    if candidates:
        by_door = _door_arc_factor(space)
        return by_door if by_door in candidates else candidates[0]
    code = int(doc.header.get("$INSUNITS", 0) or 0)
    return _INSUNITS_TO_MM.get(code, 1.0)


def _has_walls(space, min_count: int = 10) -> bool:
    n = 0
    for e in space:
        if WALL_PATTERN.search(e.dxf.layer):
            n += 1
            if n >= min_count:
                return True
    return False


@dataclass
class DxfPlan:
    """Geöffneter Plan — Zugriff auf Entities in mm."""

    doc: ezdxf.document.Drawing
    space: object          # Modelspace oder Block-Layout, das die Architektur trägt
    factor: float          # Multiplikator Quell-Einheit → mm
    wall_layers: frozenset[str] = frozenset()  # erkannte Wand-Layer

    def entities(self, prefixes: tuple[str, ...] | None = None):
        """Alle Entities des Architektur-Raums, optional nach Layer-Prefix gefiltert."""
        for e in self.space:
            if prefixes is None or e.dxf.layer.startswith(prefixes):
                yield e

    def wall_entities(self):
        """Entities auf den erkannten Wand-Layern (familien-agnostisch)."""
        for e in self.space:
            if e.dxf.layer in self.wall_layers:
                yield e

    def _scale(self, p) -> XY:
        return (float(p[0]) * self.factor, float(p[1]) * self.factor)

    def entity_points(self, e) -> list[XY]:
        """Stützpunkte einer Entity in mm (LINE→2, LW/POLYLINE→n, INSERT→Position)."""
        t = e.dxftype()
        if t == "LINE":
            return [self._scale(e.dxf.start), self._scale(e.dxf.end)]
        if t == "LWPOLYLINE":
            return [self._scale(p) for p in e.get_points("xy")]
        if t == "POLYLINE":
            return [self._scale(v.dxf.location) for v in e.vertices]
        if t == "INSERT":
            return [self._scale(e.dxf.insert)]
        return []


def lade_dxf(pfad: str | Path) -> DxfPlan:
    """Öffne die DXF, wähle den Architektur-Raum, kalibriere den mm-Faktor."""
    doc = ezdxf.readfile(str(pfad))
    msp = doc.modelspace()
    space = msp
    if not _has_walls(msp):
        # Wrapper-Mode: ersten INSERT suchen, dessen Block Wände trägt.
        for ins in (e for e in msp if e.dxftype() == "INSERT"):
            blk = doc.blocks.get(ins.dxf.name)
            if blk is not None and _has_walls(blk):
                space = blk
                break
    wall_layers = _wall_layers(space)
    factor = _calibrate_factor(_raw_wall_span(space, wall_layers), space, doc)
    return DxfPlan(doc=doc, space=space, factor=factor, wall_layers=wall_layers)


def bounds_mm(plan: DxfPlan) -> BBox:
    """Bounding-Box (mm) über alle Wand-Entities."""
    xs: list[float] = []
    ys: list[float] = []
    for e in plan.wall_entities():
        for x, y in plan.entity_points(e):
            xs.append(x)
            ys.append(y)
    if not xs:
        raise ValueError("Keine Wand-Entities gefunden — Layer-Muster prüfen.")
    return BBox(min_xy=(min(xs), min(ys)), max_xy=(max(xs), max(ys)))
