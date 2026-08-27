"""wall.py — Wand-Datenmodell (Slice 11.1.0, Track 11.x.x M2 Phase 1).

Wrapper-Dataclass um die Wand-Dicts aus architecture_parsed.json
({start_mm, end_mm, wall_type, layer}). Reine Geometrie + Helper —
kein Konsumenten-Touch in dieser Slice. Resolver `wall_ref → Wall`
folgt in Slice 11.4.0.

Konventionen:
- Koordinaten in mm-Welt als tuple[float, float] (konsistent zu
  PlacementDecision.position).
- IDs deterministisch aus Walls-Listen-Index: f"w_{idx:04d}". Stabil
  zwischen Pipeline-Runs solange parse_architecture deterministisch ist.
- @dataclass(frozen=True) mit __post_init__-Validation: length_mm > 0.
- wall_type bleibt ein offener String — Vocabulary in Slice 11.2.0
  potenziell erweitert. is_outer als computed property (wall_type ==
  "aussen").
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Optional

# Float-Toleranz für length-Validation (1 micron in mm-Welt).
_MIN_LENGTH_MM = 1e-3


@dataclass(frozen=True)
class OpeningSpan:
    """Forbidden opening interval measured along a logical wall."""

    start_mm: float
    end_mm: float
    opening_id: str
    kind: str
    clearance_mm: float = 0.0

    def normalized(self) -> "OpeningSpan":
        if self.start_mm <= self.end_mm:
            return self
        return OpeningSpan(
            start_mm=self.end_mm,
            end_mm=self.start_mm,
            opening_id=self.opening_id,
            kind=self.kind,
            clearance_mm=self.clearance_mm,
        )

    def to_dict(self) -> dict:
        span = self.normalized()
        return {
            "start_mm": span.start_mm,
            "end_mm": span.end_mm,
            "opening_id": span.opening_id,
            "kind": span.kind,
            "clearance_mm": span.clearance_mm,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "OpeningSpan":
        return cls(
            start_mm=float(d["start_mm"]),
            end_mm=float(d["end_mm"]),
            opening_id=str(d.get("opening_id", "")),
            kind=str(d.get("kind", "opening")),
            clearance_mm=float(d.get("clearance_mm", 0.0)),
        ).normalized()


@dataclass(frozen=True)
class Wall:
    """One wall segment in mm-world coordinates."""

    id: str
    start_xy: tuple[float, float]
    end_xy: tuple[float, float]
    wall_type: str
    room_id: Optional[str] = None
    opening_spans: tuple[OpeningSpan, ...] = field(default_factory=tuple)
    source_wall_ids: tuple[str, ...] = field(default_factory=tuple)
    source_midpoints: tuple[tuple[float, float], ...] = field(default_factory=tuple)
    is_logical_bridge: bool = False
    no_mount: bool = False
    no_mount_source: str = ""

    def __post_init__(self) -> None:
        # Validation: degenerate Wände blockieren — meist Mess-Artefakt
        # aus dem DXF-Parser. Slice 11.2.0 muss solche Fälle dort fangen.
        if self.length_mm < _MIN_LENGTH_MM:
            raise ValueError(
                f"Wall {self.id!r} has zero/near-zero length: "
                f"start={self.start_xy} end={self.end_xy} "
                f"length_mm={self.length_mm}"
            )

    # ── Geometrie als computed properties ─────────────────────────────

    @property
    def length_mm(self) -> float:
        """Euklidische Länge der Wand in mm."""
        dx = self.end_xy[0] - self.start_xy[0]
        dy = self.end_xy[1] - self.start_xy[1]
        return math.sqrt(dx * dx + dy * dy)

    @property
    def direction_vector(self) -> tuple[float, float]:
        """Roher Richtungsvektor (dx, dy) — nicht normalisiert."""
        return (
            self.end_xy[0] - self.start_xy[0],
            self.end_xy[1] - self.start_xy[1],
        )

    @property
    def unit_vector(self) -> tuple[float, float]:
        """Einheitsvektor in Wand-Richtung. Norm == 1.0 ± Float-Toleranz."""
        L = self.length_mm
        dx, dy = self.direction_vector
        return (dx / L, dy / L)

    @property
    def angle_deg(self) -> float:
        """Wand-Winkel via atan2(dy, dx) in Grad. Range (-180, 180]."""
        dx, dy = self.direction_vector
        return math.degrees(math.atan2(dy, dx))

    @property
    def is_outer(self) -> bool:
        """True wenn Außenwand. Mapping: wall_type == 'aussen'."""
        return self.wall_type == "aussen"

    # ── Geometrie-Methoden ────────────────────────────────────────────

    def point_at_distance(self, d_mm: float) -> tuple[float, float]:
        """Punkt auf der Wand bei Distanz d_mm vom start_xy entlang der
        Wand-Richtung. d_mm = 0 → start_xy; d_mm = length_mm → end_xy.
        """
        ux, uy = self.unit_vector
        return (self.start_xy[0] + d_mm * ux, self.start_xy[1] + d_mm * uy)

    def is_axis_aligned(self, tol_deg: float = 1.0) -> bool:
        """True wenn der Wand-Winkel innerhalb tol_deg von einer der
        Achsen-Richtungen liegt (-180 / -90 / 0 / 90 / 180).

        Default-Toleranz 1° fängt Float-Drift in nominell achs-parallelen
        DXF-Wänden (typische Drift ~0.5° bei 12 m Wand).
        """
        a = self.angle_deg
        return min(abs(a - axis) for axis in (-180.0, -90.0, 0.0, 90.0, 180.0)) <= tol_deg

    # ── Serialization ─────────────────────────────────────────────────

    def to_dict(self) -> dict:
        """JSON-tauglicher Dict-Snapshot. Round-Trip via from_dict()."""
        return {
            "id": self.id,
            "start_xy": list(self.start_xy),
            "end_xy": list(self.end_xy),
            "wall_type": self.wall_type,
            "room_id": self.room_id,
            "opening_spans": [s.to_dict() for s in self.opening_spans],
            "source_wall_ids": list(self.source_wall_ids),
            "source_midpoints": [list(p) for p in self.source_midpoints],
            "is_logical_bridge": self.is_logical_bridge,
            "no_mount": self.no_mount,
            "no_mount_source": self.no_mount_source,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Wall":
        """Inverse zu to_dict(). Akzeptiert Listen oder Tuples für Koordinaten."""
        return cls(
            id=d["id"],
            start_xy=tuple(d["start_xy"]),
            end_xy=tuple(d["end_xy"]),
            wall_type=d["wall_type"],
            room_id=d.get("room_id"),
            opening_spans=tuple(
                OpeningSpan.from_dict(s) for s in d.get("opening_spans", ())
            ),
            source_wall_ids=tuple(d.get("source_wall_ids", ())),
            source_midpoints=tuple(tuple(p) for p in d.get("source_midpoints", ())),
            is_logical_bridge=bool(d.get("is_logical_bridge", False)),
            no_mount=bool(d.get("no_mount", False)),
            no_mount_source=str(d.get("no_mount_source", "")),
        )

    @classmethod
    def from_arch_dict(
        cls,
        d: dict,
        *,
        idx: int,
        room_id: Optional[str] = None,
    ) -> "Wall":
        """Constructor aus dem architecture_parsed.json-Schema.

        Erwartet d = {"start_mm": [x, y], "end_mm": [x, y], "wall_type": str, ...}.
        Das `layer`-Feld aus arch_parsed wird aktuell nicht übernommen —
        es ist Diagnose-Info, nicht domain-relevant.
        """
        return cls(
            id=f"w_{idx:04d}",
            start_xy=tuple(d["start_mm"]),
            end_xy=tuple(d["end_mm"]),
            wall_type=d["wall_type"],
            room_id=room_id,
            no_mount=bool(d.get("no_mount", False)),
            no_mount_source=str(d.get("no_mount_source", "")),
        )
