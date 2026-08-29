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

from dataclasses import dataclass
from pathlib import Path

import ezdxf

from notbeleuchtung.hauptengine.contracts.raum_modell import BBox

# Wand-Layer-Prefixe (floor-agnostisch: Suffix -LEG-/-L04-/… wird ignoriert).
WALL_PREFIXES: tuple[str, ...] = ("02-TWA", "02-ZWA", "02-WDA")

# $INSUNITS-Code → Faktor auf mm. 4=mm, 5=cm, 6=m; Rest → 1.0 (mm-Annahme).
_INSUNITS_TO_MM: dict[int, float] = {4: 1.0, 5: 10.0, 6: 1000.0}

XY = tuple[float, float]


# Plausible Ausdehnung eines Geschosses in mm (ein paar Meter … ~500 m).
_SPAN_MIN_MM = 8_000.0
_SPAN_MAX_MM = 500_000.0


def _raw_wall_span(space) -> float:
    """Größte Wand-Ausdehnung (dx/dy) in Quell-Einheiten (ohne Skalierung)."""
    xs: list[float] = []
    ys: list[float] = []
    for e in space:
        if not e.dxf.layer.startswith(WALL_PREFIXES):
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


def _calibrate_factor(raw_span: float, doc: ezdxf.document.Drawing) -> float:
    """mm-Faktor aus der Geometrie ableiten (Dekaden-Snap), NICHT aus $INSUNITS.

    $INSUNITS ist in der Praxis unzuverlässig (leere Pläne stehen in Metern,
    fertige in mm — beide deklarieren oft denselben Code). Wir wählen die
    Zehnerpotenz, die die Geschoss-Ausdehnung in den plausiblen mm-Bereich legt.
    """
    if raw_span > 0:
        for factor in (1.0, 10.0, 100.0, 1000.0, 10000.0):
            if _SPAN_MIN_MM <= raw_span * factor <= _SPAN_MAX_MM:
                return factor
    # Fallback: $INSUNITS-Code.
    code = int(doc.header.get("$INSUNITS", 0) or 0)
    return _INSUNITS_TO_MM.get(code, 1.0)


def _has_walls(space, min_count: int = 10) -> bool:
    n = 0
    for e in space:
        if e.dxf.layer.startswith(WALL_PREFIXES):
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

    def entities(self, prefixes: tuple[str, ...] | None = None):
        """Alle Entities des Architektur-Raums, optional nach Layer-Prefix gefiltert."""
        for e in self.space:
            if prefixes is None or e.dxf.layer.startswith(prefixes):
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
    factor = _calibrate_factor(_raw_wall_span(space), doc)
    return DxfPlan(doc=doc, space=space, factor=factor)


def bounds_mm(plan: DxfPlan) -> BBox:
    """Bounding-Box (mm) über alle Wand-Entities."""
    xs: list[float] = []
    ys: list[float] = []
    for e in plan.entities(WALL_PREFIXES):
        for x, y in plan.entity_points(e):
            xs.append(x)
            ys.append(y)
    if not xs:
        raise ValueError("Keine Wand-Entities gefunden — Layer-Prefixe prüfen.")
    return BBox(min_xy=(min(xs), min(ys)), max_xy=(max(xs), max(ys)))
