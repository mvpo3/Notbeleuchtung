"""door_opening.py — Tür-Aussparungs-Polygone (Slice 11.3.0-redo).

Modelliert die Wand-Aussparung einer Drehflügeltür als 2D-Polygon im
Welt-mm-Koordinatensystem. Quelle ist die im Parser bereits berechnete
Geometrie pro Tür: ``hinge_world_mm`` (Drehpunkt = Wand-Anker),
``wall_unit_xy`` (normalisierte Wand-Richtung an der Tür) und die
aus dem Block-Namen geparste ``width_mm``.

Slice 11.3.0-redo nutzt direkt die Door-Daten ohne Wall-Mapping —
Avoidance-Tests in 11.7.0 erfolgen per Point-in-Polygon (siehe
``door_opening_index.py``). Hintergrund: das parametrische Wall-Gap-
Modell aus dem WIP-Branch ``leonis/slice-11-3-0-WIP-architecture-finding``
hat sich an der Wand-Topologie gestoßen (siehe
``docs/SLICE_11_3_0_STATE.md`` + ``docs/SLICE_11_2_5_PRE_READ.md``).

Slice 11.3.1 erweitert das Modell um Window-Polygone, Slice 11.3.2 um
Schiebetüren — beide sind in 11.3.0-redo bewusst nicht enthalten.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Literal, Optional

# Default Wand-Stärke. Mittelwert aus österreichischen Innenwänden
# (10/12.5/20er). Wand-Typ-spezifische Werte erst wenn nötig.
DEFAULT_WALL_THICKNESS_MM: float = 200.0


@dataclass(frozen=True)
class DoorOpening:
    """Eine Tür-Aussparung als 4-Punkt-Rechteck-Polygon in mm-Welt.

    ``polygon_mm`` ist die Wand-Aussparung (Korridor durch die Wand:
    Tür-Breite × Wand-Stärke). ``swing_polygon_mm`` ist der Schwung-
    Bereich, getrennt geführt — wird in 11.7.0 für Möbel-/Symbol-
    Schwung-Avoidance benutzt.

    Slice 11.5.1: optionale Anker-Felder ``hinge_xy``,
    ``handle_side_xy`` und ``wall_unit_xy`` ermöglichen
    ``_position_near_door`` im Position-Resolver, ohne Schema-
    Migration. Alle drei Felder default ``None`` für Backward-Compat
    mit 11.3.x-Tests, die ``DoorOpening`` ohne Anker konstruieren.
    """

    door_id: str
    polygon_mm: tuple[tuple[float, float], ...]
    source_ref: str
    source_kind: Literal["door", "door_sliding"] = "door"
    swing_polygon_mm: tuple[tuple[float, float], ...] = field(default_factory=tuple)
    # Slice 11.5.1: Anker-Felder fuer near_door-Position
    hinge_xy: Optional[tuple[float, float]] = None
    handle_side_xy: Optional[tuple[float, float]] = None
    wall_unit_xy: Optional[tuple[float, float]] = None

    def __post_init__(self) -> None:
        if len(self.polygon_mm) < 3:
            raise ValueError(
                f"DoorOpening {self.door_id!r}: polygon_mm needs >=3 vertices, "
                f"got {len(self.polygon_mm)}"
            )
        for i, (x, y) in enumerate(self.polygon_mm):
            if not (math.isfinite(x) and math.isfinite(y)):
                raise ValueError(
                    f"DoorOpening {self.door_id!r}: polygon vertex {i} not finite: ({x}, {y})"
                )
        for name, anchor in (
            ("hinge_xy", self.hinge_xy),
            ("handle_side_xy", self.handle_side_xy),
            ("wall_unit_xy", self.wall_unit_xy),
        ):
            if anchor is None:
                continue
            if len(anchor) != 2 or not all(math.isfinite(v) for v in anchor):
                raise ValueError(
                    f"DoorOpening {self.door_id!r}: {name}={anchor!r} "
                    f"must be a 2-tuple of finite floats or None"
                )

    def to_dict(self) -> dict:
        return {
            "door_id": self.door_id,
            "polygon_mm": [list(p) for p in self.polygon_mm],
            "source_kind": self.source_kind,
            "source_ref": self.source_ref,
            "swing_polygon_mm": [list(p) for p in self.swing_polygon_mm],
            "hinge_xy": list(self.hinge_xy) if self.hinge_xy else None,
            "handle_side_xy": (
                list(self.handle_side_xy) if self.handle_side_xy else None
            ),
            "wall_unit_xy": (
                list(self.wall_unit_xy) if self.wall_unit_xy else None
            ),
        }

    @classmethod
    def from_dict(cls, d: dict) -> "DoorOpening":
        def _opt_xy(v) -> Optional[tuple[float, float]]:
            return tuple(v) if v is not None else None

        return cls(
            door_id=d["door_id"],
            polygon_mm=tuple(tuple(p) for p in d["polygon_mm"]),
            source_kind=d.get("source_kind", "door"),
            source_ref=d.get("source_ref", ""),
            swing_polygon_mm=tuple(tuple(p) for p in d.get("swing_polygon_mm", ())),
            hinge_xy=_opt_xy(d.get("hinge_xy")),
            handle_side_xy=_opt_xy(d.get("handle_side_xy")),
            wall_unit_xy=_opt_xy(d.get("wall_unit_xy")),
        )


def build_door_polygon(
    hinge_xy: tuple[float, float],
    wall_unit: tuple[float, float],
    width_mm: float,
    wall_thickness_mm: float = DEFAULT_WALL_THICKNESS_MM,
) -> tuple[tuple[float, float], tuple[float, float], tuple[float, float], tuple[float, float]]:
    """Konstruiert das Aussparungs-Rechteck am Drehpunkt-Anker.

    Geometrie: hinge ist Ecke 0; das Rechteck spannt sich entlang
    ``wall_unit`` über ``width_mm`` und perpendicular über
    ``wall_thickness_mm`` (zentriert um die Wand-Achse).

    Reihenfolge der Eckpunkte (counter-clockwise wenn wall_unit
    nach +X zeigt): hinge−normal/2, opposite−normal/2,
    opposite+normal/2, hinge+normal/2.

    Validation:
    - ``width_mm > 0``
    - ``wall_thickness_mm > 0``
    - ``|wall_unit| ≈ 1`` (Toleranz 1 %)
    """
    if width_mm <= 0.0 or not math.isfinite(width_mm):
        raise ValueError(f"width_mm must be positive and finite, got {width_mm}")
    if wall_thickness_mm <= 0.0 or not math.isfinite(wall_thickness_mm):
        raise ValueError(
            f"wall_thickness_mm must be positive and finite, got {wall_thickness_mm}"
        )
    ux, uy = wall_unit
    norm = math.hypot(ux, uy)
    if not (0.99 <= norm <= 1.01):
        raise ValueError(
            f"wall_unit must have norm ~1.0, got {norm:.4f} from ({ux}, {uy})"
        )
    hx, hy = hinge_xy
    if not (math.isfinite(hx) and math.isfinite(hy)):
        raise ValueError(f"hinge_xy must be finite, got ({hx}, {hy})")

    # Perpendicular unit vector: 90° counter-clockwise rotation.
    nx, ny = -uy, ux
    half_t = 0.5 * wall_thickness_mm

    # End point of the door span along wall_unit.
    ex = hx + width_mm * ux
    ey = hy + width_mm * uy

    return (
        (hx - half_t * nx, hy - half_t * ny),
        (ex - half_t * nx, ey - half_t * ny),
        (ex + half_t * nx, ey + half_t * ny),
        (hx + half_t * nx, hy + half_t * ny),
    )
