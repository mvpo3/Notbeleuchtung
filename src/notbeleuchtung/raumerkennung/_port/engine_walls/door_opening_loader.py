"""door_opening_loader.py — Loader für Tür-Aussparungs-Polygone aus
``architecture_parsed.json`` (Slice 11.3.0-redo).

Iteriert über alle Türen (geschachtelt in ``rooms[].doors``), filtert
Drehflügeltüren (mit gesetztem ``hinge_world_mm`` und ``wall_unit_xy``),
parst die Tür-Breite aus dem Block-Namen und konstruiert pro Tür ein
``DoorOpening``-Polygon. Schiebetüren werden mit
``REASON_SLIDING_UNSUPPORTED`` skipped — eigener Slice 11.3.2.
"""
from __future__ import annotations

import json
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

# Default Tür-Breite wenn weder im JSON noch im Block-Namen parsbar.
# 80 cm ist die ÖNORM-Standard-Innentür.
DEFAULT_DOOR_WIDTH_MM: float = 800.0

# Skip-Reasons (Konstanten — Konsumenten dürfen referenzieren).
REASON_SLIDING_UNSUPPORTED = "sliding_unsupported"
REASON_MISSING_HINGE = "missing_hinge"
REASON_DEGENERATE_WIDTH = "degenerate_width"
REASON_MALFORMED = "malformed_door"


@dataclass(frozen=True)
class DoorLoadStats:
    """Statistik-Snapshot eines Loader-Runs."""

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


def load_door_openings_from_arch(
    arch_path: Path | str,
    *,
    wall_thickness_mm: float = DEFAULT_WALL_THICKNESS_MM,
    log_skipped: bool = True,
) -> tuple[DoorOpeningIndex, DoorLoadStats]:
    """Load Drehflügeltür-Aussparungs-Polygone aus
    ``architecture_parsed.json``.

    Parameters
    ----------
    arch_path
        Pfad zu ``architecture_parsed.json``.
    wall_thickness_mm
        Wand-Stärke für die Polygon-Tiefe. Default 200 mm.
    log_skipped
        Wenn True (Default), eine Diagnose-Zeile pro Skip auf stdout.
    """
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
            total_input += 1
            res = _door_to_opening(
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
    stats = DoorLoadStats(
        total_input=total_input,
        total_loaded=len(openings),
        skipped_count=sum(skipped_reasons.values()),
        skipped_reasons=dict(skipped_reasons),
    )
    return index, stats


def _door_to_opening(
    *,
    door: dict,
    door_idx: int,
    room_id: str,
    global_idx: int,
    wall_thickness_mm: float,
) -> DoorOpening | tuple[str, str]:
    """Konstruiert eine ``DoorOpening`` aus einem Door-JSON-Dict.
    Returnt ``(reason, detail)`` wenn geskipt."""
    block_name = door.get("block_name", "?")
    if door.get("is_sliding") is True:
        return (REASON_SLIDING_UNSUPPORTED, f"is_sliding=True for {block_name}")

    hinge = door.get("hinge_world_mm")
    wall_unit = door.get("wall_unit_xy")
    if (
        hinge is None
        or wall_unit is None
        or len(hinge) != 2
        or len(wall_unit) != 2
        or (hinge[0] == 0.0 and hinge[1] == 0.0)
        or (wall_unit[0] == 0.0 and wall_unit[1] == 0.0)
    ):
        return (
            REASON_MISSING_HINGE,
            f"hinge or wall_unit unset/zero for {block_name}",
        )

    width_mm = _parse_door_width(door)
    if width_mm <= 0.0:
        return (REASON_DEGENERATE_WIDTH, f"width_mm={width_mm} for {block_name}")

    try:
        hx, hy = float(hinge[0]), float(hinge[1])
        ux, uy = float(wall_unit[0]), float(wall_unit[1])
        polygon = build_door_polygon(
            (hx, hy), (ux, uy), width_mm, wall_thickness_mm
        )
    except (ValueError, TypeError) as exc:
        return (REASON_MALFORMED, f"polygon construction failed: {exc}")

    swing_raw = door.get("swing_polygon_mm") or []
    try:
        swing = tuple(
            (float(p[0]), float(p[1])) for p in swing_raw if len(p) >= 2
        )
    except (TypeError, ValueError, IndexError):
        swing = ()

    # Slice 11.5.1: Anker-Felder durchreichen fuer near_door-Strategy.
    # hinge / wall_unit sind hier garantiert valide (oben bereits geprueft);
    # handle_side_pos_mm wird vom Parser parallel gesetzt - defensive Pruefung.
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

    door_id = f"d_{global_idx:04d}"
    source_ref = f"{room_id}#{block_name}#{door_idx}"
    return DoorOpening(
        door_id=door_id,
        polygon_mm=polygon,
        source_ref=source_ref,
        swing_polygon_mm=swing,
        hinge_xy=(hx, hy),
        handle_side_xy=handle_xy,
        wall_unit_xy=(ux, uy),
    )


def _parse_door_width(door: dict) -> float:
    """Extrahiert die Tür-Breite. Reihenfolge:
    1. JSON-Feld ``width_mm`` wenn finite und > 0 (im aktuellen Export
       *nicht* gesetzt, defensive trotzdem).
    2. Aus ``block_name`` parsen (z.B. ``TÜR-80_10er-WAND`` → 80 cm = 800 mm).
    3. ``DEFAULT_DOOR_WIDTH_MM`` (800 mm).
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

    return DEFAULT_DOOR_WIDTH_MM


# Encoding-tolerant: 'TÜR-', 'TUER-', 'T�R-' (cp1252-mojibake aus DXF).
_WIDTH_FROM_NAME_RE = re.compile(r"(?:T(?:Ü|UE|�)R)-(\d+)", re.IGNORECASE)


def _parse_width_from_block_name(name: str) -> float | None:
    """Tür-Block-Namen der Form ``TÜR-80_10er-WAND`` codieren 80 cm.
    Plausibilitäts-Range 40–200 cm; sonst None."""
    if not name:
        return None
    m = _WIDTH_FROM_NAME_RE.search(name)
    if not m:
        return None
    try:
        cm = int(m.group(1))
    except ValueError:
        return None
    if 40 <= cm <= 200:
        return float(cm) * 10.0
    return None


def _log_skip(
    room_id: str, door_idx: int, door: dict, reason: str, detail: str
) -> None:
    block = door.get("block_name", "?")
    print(
        f"[door_opening_loader] skip {room_id}#{block}#{door_idx} "
        f"(reason={reason}): {detail}"
    )
