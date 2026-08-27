"""sliding_door_loader.py — Loader für Schiebetüren-Aussparungs-
Polygone aus ``architecture_parsed.json`` (Slice 11.3.2).

Schließt M2-Phase-3 ab: die 10 Sliding-Türen, die in
``door_opening_loader`` mit ``REASON_SLIDING_UNSUPPORTED`` skipped
wurden, werden hier zu DoorOpenings mit ``source_kind="door_sliding"``.

Anchor-Strategie ist Pre-Read-validiert (10/10 ≤ 50 mm Wand-Distanz):
``anchor = position_mm + width/2 · (cos α, sin α)``. Position ist
Block-Origin (NICHT Wand-Mittelpunkt wie bei Windows) — gleiches
Pattern wie Drehflügel, nur die Wand-Richtung wird aus
``rotation_deg`` rekonstruiert statt aus ``wall_unit_xy`` (das ist
[0, 0] für Sliding).

``swing_polygon_mm`` (im JSON ein 4-Eck Schiebebereich, ~209 × 1800 mm)
wird durchgereicht für 11.7.0 Schwung-Avoidance — als Wand-Aussparung
ist es unbrauchbar (zu groß).
"""
from __future__ import annotations

import json
import math
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

from engine.walls.door_opening import (
    DEFAULT_WALL_THICKNESS_MM,
    DoorOpening,
    build_door_polygon,
)
from engine.walls.door_opening_index import DoorOpeningIndex

# Default Sliding-Tür-Breite. Aktuelles Asset: alle 10 Sliding sind
# SCHIEBETÜR-80 → 800 mm. Defensive Default für Edge-Cases.
DEFAULT_SLIDING_DOOR_WIDTH_MM: float = 800.0

# Skip-Reasons mit SLIDING-Prefix — vermeidet Re-Export-Kollision mit
# door_opening_loader und window_opening_loader.
REASON_SLIDING_DEGENERATE_WIDTH = "sliding_degenerate_width"
REASON_SLIDING_MISSING_ROTATION = "sliding_missing_rotation"
REASON_MALFORMED_SLIDING = "malformed_sliding"


@dataclass(frozen=True)
class SlidingDoorLoadStats:
    """Statistik-Snapshot eines Sliding-Loader-Runs."""

    total_input: int
    total_loaded: int
    skipped_count: int
    skipped_reasons: dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "total_input": self.total_input,
            "total_loaded": self.total_loaded,
            "skipped_count": self.skipped_count,
            "skipped_reasons": dict(self.skipped_reasons),
        }


def load_sliding_door_openings_from_arch(
    arch_path: Path | str,
    *,
    wall_thickness_mm: float = DEFAULT_WALL_THICKNESS_MM,
    log_skipped: bool = True,
) -> tuple[DoorOpeningIndex, SlidingDoorLoadStats]:
    """Load Sliding-Tür-Aussparungs-Polygone aus
    ``architecture_parsed.json``. Filter ``is_sliding == True``."""
    p = Path(arch_path)
    if not p.exists():
        raise FileNotFoundError(f"architecture_parsed.json not found at {p}")

    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"corrupt JSON at {p}: {exc}") from exc

    rooms = data.get("rooms")
    if rooms is None or not isinstance(rooms, list):
        raise ValueError(
            f"no valid 'rooms' list in {p} (top-level keys: {list(data.keys())})"
        )

    openings: list[DoorOpening] = []
    skipped_reasons: Counter = Counter()
    total_input = 0
    global_idx = 0

    for ri, room in enumerate(rooms):
        room_id = f"r_{ri:04d}"
        for di, door in enumerate(room.get("doors") or []):
            if door.get("is_sliding") is not True:
                continue
            total_input += 1
            res = _sliding_to_opening(
                door=door,
                door_idx=di,
                room_id=room_id,
                global_idx=global_idx,
                wall_thickness_mm=wall_thickness_mm,
            )
            if isinstance(res, DoorOpening):
                openings.append(res)
                global_idx += 1
            else:
                reason, detail = res
                skipped_reasons[reason] += 1
                if log_skipped:
                    _log_skip(room_id, di, door, reason, detail)

    index = DoorOpeningIndex.from_openings(openings)
    stats = SlidingDoorLoadStats(
        total_input=total_input,
        total_loaded=len(openings),
        skipped_count=sum(skipped_reasons.values()),
        skipped_reasons=dict(skipped_reasons),
    )
    return index, stats


def _sliding_to_opening(
    *,
    door: dict,
    door_idx: int,
    room_id: str,
    global_idx: int,
    wall_thickness_mm: float,
) -> DoorOpening | tuple[str, str]:
    """Konstruiert eine Sliding-DoorOpening.

    Reuse von ``build_door_polygon``: das Polygon spannt vom übergebenen
    ``hinge``-Punkt entlang ``wall_unit`` über ``width`` auf. Bei Sliding
    übergeben wir ``hinge=position`` (Block-Origin) und
    ``wall_unit=(cos α, sin α)`` aus ``rotation_deg``.
    """
    block_name = door.get("block_name", "?")

    rotation = door.get("rotation_deg")
    if rotation is None:
        return (
            REASON_SLIDING_MISSING_ROTATION,
            f"rotation_deg is None for {block_name}",
        )
    try:
        rotation = float(rotation)
    except (TypeError, ValueError):
        return (
            REASON_SLIDING_MISSING_ROTATION,
            f"rotation_deg not parseable for {block_name}",
        )
    if not math.isfinite(rotation):
        return (
            REASON_SLIDING_MISSING_ROTATION,
            f"rotation_deg not finite for {block_name}",
        )

    width_mm = _parse_sliding_door_width(door)
    if width_mm <= 0.0:
        return (
            REASON_SLIDING_DEGENERATE_WIDTH,
            f"width_mm={width_mm} for {block_name}",
        )

    try:
        pos = door["position_mm"]
        px, py = float(pos[0]), float(pos[1])
        rad = math.radians(rotation)
        ux, uy = math.cos(rad), math.sin(rad)
        polygon = build_door_polygon(
            (px, py), (ux, uy), width_mm, wall_thickness_mm
        )
    except (KeyError, TypeError, ValueError, IndexError) as exc:
        return (
            REASON_MALFORMED_SLIDING,
            f"polygon construction failed: {exc}",
        )

    swing_raw = door.get("swing_polygon_mm") or []
    try:
        swing = tuple(
            (float(p[0]), float(p[1])) for p in swing_raw if len(p) >= 2
        )
    except (TypeError, ValueError, IndexError):
        swing = ()

    # Slice 11.5.1: Anker-Felder schema-konsistent durchreichen.
    # Sliding-Tueren haben typisch ``handle_side_pos_mm`` und
    # ``wall_unit_xy`` unset im Parser - durchgereicht als ``None``.
    handle_raw = door.get("handle_side_pos_mm")
    if (
        handle_raw is not None
        and len(handle_raw) == 2
        and not (handle_raw[0] == 0.0 and handle_raw[1] == 0.0)
    ):
        handle_xy: tuple[float, float] | None = (
            float(handle_raw[0]), float(handle_raw[1])
        )
    else:
        handle_xy = None

    wall_unit_raw = door.get("wall_unit_xy")
    if (
        wall_unit_raw is not None
        and len(wall_unit_raw) == 2
        and not (wall_unit_raw[0] == 0.0 and wall_unit_raw[1] == 0.0)
    ):
        wall_unit_field: tuple[float, float] | None = (
            float(wall_unit_raw[0]), float(wall_unit_raw[1])
        )
    else:
        # Fallback: aus rotation_deg rekonstruiert (immer verfuegbar).
        wall_unit_field = (ux, uy)

    door_id = f"sd_{global_idx:04d}"
    source_ref = f"{room_id}#{block_name}#{door_idx}"
    return DoorOpening(
        door_id=door_id,
        polygon_mm=polygon,
        source_ref=source_ref,
        source_kind="door_sliding",
        swing_polygon_mm=swing,
        hinge_xy=(px, py),
        handle_side_xy=handle_xy,
        wall_unit_xy=wall_unit_field,
    )


# Encoding-tolerant: 'SCHIEBETÜR', 'SCHIEBETUER', 'SCHIEBET�R' (cp1252-mojibake).
# Optional Hyphen/Whitespace zwischen 'SCHIEBE' und 'TÜR'.
_SLIDING_WIDTH_RE = re.compile(
    r"SCHIEBE[\W_]*T(?:Ü|UE|�)R[\W_]*(\d+)", re.IGNORECASE
)


def _parse_sliding_door_width(door: dict) -> float:
    """Extrahiert Sliding-Tür-Breite. Reihenfolge:
    1. JSON-Feld ``width_mm`` wenn finite und > 0
    2. block_name regex (``SCHIEBETÜR-80`` → 800 mm)
    3. ``DEFAULT_SLIDING_DOOR_WIDTH_MM`` (800 mm)
    """
    raw = door.get("width_mm")
    if raw is not None:
        try:
            v = float(raw)
            if v > 0.0:
                return v
        except (TypeError, ValueError):
            pass

    parsed = _parse_width_from_block_name(door.get("block_name", "") or "")
    if parsed is not None:
        return parsed

    return DEFAULT_SLIDING_DOOR_WIDTH_MM


def _parse_width_from_block_name(name: str) -> float | None:
    """``SCHIEBETÜR-80`` → 800 mm. Plausibilitäts-Range 60–250 cm."""
    if not name:
        return None
    m = _SLIDING_WIDTH_RE.search(name)
    if not m:
        return None
    try:
        cm = int(m.group(1))
    except ValueError:
        return None
    if 60 <= cm <= 250:
        return float(cm) * 10.0
    return None


def _log_skip(
    room_id: str, door_idx: int, door: dict, reason: str, detail: str
) -> None:
    block = door.get("block_name", "?")
    print(
        f"[sliding_door_loader] skip {room_id}#{block}#{door_idx} "
        f"(reason={reason}): {detail}"
    )
