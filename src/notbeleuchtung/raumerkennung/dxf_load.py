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


def _factor_to_mm(doc: ezdxf.document.Drawing) -> float:
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
    """Öffne die DXF, wähle den Architektur-Raum, bestimme den mm-Faktor."""
    doc = ezdxf.readfile(str(pfad))
    msp = doc.modelspace()
    factor = _factor_to_mm(doc)
    space = msp
    if not _has_walls(msp):
        # Wrapper-Mode: ersten INSERT suchen, dessen Block Wände trägt.
        for ins in (e for e in msp if e.dxftype() == "INSERT"):
            blk = doc.blocks.get(ins.dxf.name)
            if blk is not None and _has_walls(blk):
                space = blk
                break
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
