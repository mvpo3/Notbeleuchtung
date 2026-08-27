"""window_opening_index.py — Avoidance-Lookup für Fenster-Aussparungen
(Slice 11.3.1).

Re-uses ``point_in_polygon`` aus ``door_opening_index`` (single source
of truth — wenn Slice 11.3.2 oder Folgendes auch testet, wird der
Helper später in ``engine/walls/_geometry.py`` extrahiert).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Optional

from engine.walls.door_opening_index import point_in_polygon
from engine.walls.window_opening import WindowOpening


@dataclass(frozen=True)
class WindowOpeningIndex:
    """Read-only Index über WindowOpenings für Avoidance-Lookups."""

    _openings: tuple[WindowOpening, ...]

    @classmethod
    def from_openings(
        cls, openings: Iterable[WindowOpening]
    ) -> "WindowOpeningIndex":
        return cls(_openings=tuple(openings))

    def is_blocked(self, point_xy: tuple[float, float]) -> bool:
        """True wenn der Punkt in einem der Fenster-Polygone liegt."""
        for o in self._openings:
            if point_in_polygon(point_xy, o.polygon_mm):
                return True
        return False

    def blocking_window(
        self, point_xy: tuple[float, float]
    ) -> Optional[WindowOpening]:
        """Die erste WindowOpening die den Punkt enthält, sonst None."""
        for o in self._openings:
            if point_in_polygon(point_xy, o.polygon_mm):
                return o
        return None

    @property
    def total_openings(self) -> int:
        return len(self._openings)

    def to_dict(self) -> dict:
        return {"openings": [o.to_dict() for o in self._openings]}
