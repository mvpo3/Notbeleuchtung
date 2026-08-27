"""window_opening.py — Fenster-Aussparungs-Polygone (Slice 11.3.1).

Modelliert die Wand-Aussparung eines Fensters als 2D-Polygon im
Welt-mm-Koordinatensystem. Anders als bei Türen ist das Polygon
**zentriert um `position_mm`**, weil der Parser `position_mm` direkt
auf der Wand-Achse setzt (Pre-Read 76/76 Windows ≤ 50 mm Wand-Distanz).

Wand-Richtung wird aus ``rotation_deg`` über ``(cos, sin)``
rekonstruiert — der Window-Dataclass im Parser hat kein
``wall_unit_xy``-Feld wie der Door-Dataclass.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Literal, Optional

from engine.walls.door_opening import DEFAULT_WALL_THICKNESS_MM


@dataclass(frozen=True)
class WindowOpening:
    """Eine Fenster-Aussparung als 4-Punkt-Rechteck-Polygon.

    Polygon ist zentriert um den Wand-Mittelpunkt der Aussparung
    (Pre-Read-validierte Anchor-Strategie). ``height_mm`` wird für
    künftige 3D-Höhen-Constraints durchgereicht — beeinflusst die
    2D-Avoidance nicht.
    """

    window_id: str
    polygon_mm: tuple[tuple[float, float], ...]
    source_ref: str
    source_kind: Literal["window"] = "window"
    height_mm: Optional[float] = None

    def __post_init__(self) -> None:
        if len(self.polygon_mm) < 3:
            raise ValueError(
                f"WindowOpening {self.window_id!r}: polygon_mm needs >=3 vertices, "
                f"got {len(self.polygon_mm)}"
            )
        for i, (x, y) in enumerate(self.polygon_mm):
            if not (math.isfinite(x) and math.isfinite(y)):
                raise ValueError(
                    f"WindowOpening {self.window_id!r}: polygon vertex {i} "
                    f"not finite: ({x}, {y})"
                )

    def to_dict(self) -> dict:
        return {
            "window_id": self.window_id,
            "polygon_mm": [list(p) for p in self.polygon_mm],
            "source_kind": self.source_kind,
            "source_ref": self.source_ref,
            "height_mm": self.height_mm,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "WindowOpening":
        return cls(
            window_id=d["window_id"],
            polygon_mm=tuple(tuple(p) for p in d["polygon_mm"]),
            source_kind=d.get("source_kind", "window"),
            source_ref=d.get("source_ref", ""),
            height_mm=d.get("height_mm"),
        )


def build_window_polygon(
    position_xy: tuple[float, float],
    rotation_deg: float,
    width_mm: float,
    wall_thickness_mm: float = DEFAULT_WALL_THICKNESS_MM,
) -> tuple[tuple[float, float], tuple[float, float], tuple[float, float], tuple[float, float]]:
    """Konstruiert das Aussparungs-Rechteck zentriert um position_xy.

    Wand-Richtungs-Vektor aus ``rotation_deg``:
    ``(ux, uy) = (cos(rad), sin(rad))``. Perpendicular: ``(-uy, ux)``.

    Polygon-Eckpunkte (counter-clockwise wenn ux nach +X zeigt):
    ``position ± half_width·(ux,uy) ± half_thickness·(nx,ny)``.

    Validation:
    - ``width_mm > 0``
    - ``wall_thickness_mm > 0``
    - ``rotation_deg`` und ``position_xy`` finite
    """
    if width_mm <= 0.0 or not math.isfinite(width_mm):
        raise ValueError(f"width_mm must be positive and finite, got {width_mm}")
    if wall_thickness_mm <= 0.0 or not math.isfinite(wall_thickness_mm):
        raise ValueError(
            f"wall_thickness_mm must be positive and finite, got {wall_thickness_mm}"
        )
    if not math.isfinite(rotation_deg):
        raise ValueError(f"rotation_deg must be finite, got {rotation_deg}")
    px, py = position_xy
    if not (math.isfinite(px) and math.isfinite(py)):
        raise ValueError(f"position_xy must be finite, got ({px}, {py})")

    rad = math.radians(rotation_deg)
    ux, uy = math.cos(rad), math.sin(rad)
    nx, ny = -uy, ux
    half_w = 0.5 * width_mm
    half_t = 0.5 * wall_thickness_mm

    return (
        (px - half_w * ux - half_t * nx, py - half_w * uy - half_t * ny),
        (px + half_w * ux - half_t * nx, py + half_w * uy - half_t * ny),
        (px + half_w * ux + half_t * nx, py + half_w * uy + half_t * ny),
        (px - half_w * ux + half_t * nx, py - half_w * uy + half_t * ny),
    )
