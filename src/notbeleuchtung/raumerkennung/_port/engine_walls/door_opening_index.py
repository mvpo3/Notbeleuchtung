"""door_opening_index.py — Avoidance-Lookup für Tür-Aussparungen
(Slice 11.3.0-redo).

Nimmt eine Sequenz ``DoorOpening`` und stellt schnellen
Point-in-Polygon-Test bereit. Wird in Slice 11.7.0 vom
Position-Resolver konsumiert: jede Symbol-Kandidaten-Position wird
gegen ``is_blocked()`` geprüft, falls True → Position verwerfen.

Algorithmus: Ray-Casting (even-odd-rule), self-implementiert. Keine
Shapely-Dependency — der Index hält wenige hundert Polygone à 4 Punkte,
``is_blocked`` ist O(n_openings) mit einer trivialen 4-Edge-Schleife
pro Polygon. Reicht weit.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Optional

from engine.walls.door_opening import DoorOpening


@dataclass(frozen=True)
class DoorOpeningIndex:
    """Read-only Index über DoorOpenings für Avoidance-Lookups."""

    _openings: tuple[DoorOpening, ...]

    @classmethod
    def from_openings(cls, openings: Iterable[DoorOpening]) -> "DoorOpeningIndex":
        return cls(_openings=tuple(openings))

    def is_blocked(self, point_xy: tuple[float, float]) -> bool:
        """True wenn der Punkt in einem der Aussparungs-Polygone liegt."""
        for o in self._openings:
            if point_in_polygon(point_xy, o.polygon_mm):
                return True
        return False

    def blocking_door(
        self, point_xy: tuple[float, float]
    ) -> Optional[DoorOpening]:
        """Die erste DoorOpening die den Punkt enthält, sonst None.
        Reihenfolge ist die Insertion-Order beim Index-Bau."""
        for o in self._openings:
            if point_in_polygon(point_xy, o.polygon_mm):
                return o
        return None

    @property
    def total_openings(self) -> int:
        return len(self._openings)

    def __iter__(self):
        """Slice 16.1.2: iterate openings (e.g. for per-room filtering)."""
        return iter(self._openings)

    def to_dict(self) -> dict:
        return {"openings": [o.to_dict() for o in self._openings]}


def point_in_polygon(
    point: tuple[float, float],
    polygon: tuple[tuple[float, float], ...],
) -> bool:
    """Even-odd-rule Ray-Casting. Edge-Cases (Punkt exakt auf einer
    Kante) werden pessimistisch behandelt — Ergebnis nicht garantiert
    True/False. Für Avoidance unkritisch (Symbole landen nie exakt
    auf Polygon-Kanten in mm-Welt).
    """
    n = len(polygon)
    if n < 3:
        return False
    x, y = point
    inside = False
    j = n - 1
    for i in range(n):
        xi, yi = polygon[i]
        xj, yj = polygon[j]
        if ((yi > y) != (yj > y)) and (
            x < (xj - xi) * (y - yi) / ((yj - yi) or 1e-12) + xi
        ):
            inside = not inside
        j = i
    return inside
