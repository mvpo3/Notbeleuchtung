"""window_opening_loader.py — Loader für Fenster-Aussparungs-Polygone
aus ``architecture_parsed.json`` (Slice 11.3.1).

Iteriert über alle Fenster (geschachtelt in ``rooms[].windows`` —
seit Slice 11.3.1 Step 0 im JSON exportiert), parst die Fenster-Breite
aus ``width_mm`` (im aktuellen Datensatz für 76/76 gesetzt) mit
defensiven Fallbacks, und konstruiert pro Fenster ein ``WindowOpening``-
Polygon.
"""
from __future__ import annotations

import json
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

from engine.walls.door_opening import DEFAULT_WALL_THICKNESS_MM
from engine.walls.window_opening import WindowOpening, build_window_polygon
from engine.walls.window_opening_index import WindowOpeningIndex

# Default Fenster-Breite wenn weder im JSON noch im Block-Namen parsbar.
# 1 m ist ein realistischer Mittelwert über typische Wohnungsfenster.
DEFAULT_WINDOW_WIDTH_MM: float = 1000.0

# Skip-Reasons (Konstanten — Konsumenten dürfen referenzieren).
REASON_DEGENERATE_WIDTH = "degenerate_width"
REASON_MISSING_ROTATION = "missing_rotation"
REASON_MALFORMED = "malformed_window"


@dataclass(frozen=True)
class WindowLoadStats:
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


def load_window_openings_from_arch(
    arch_path: Path | str,
    *,
    wall_thickness_mm: float = DEFAULT_WALL_THICKNESS_MM,
    log_skipped: bool = True,
) -> tuple[WindowOpeningIndex, WindowLoadStats]:
    """Load Fenster-Aussparungs-Polygone aus ``architecture_parsed.json``."""
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

    openings: list[WindowOpening] = []
    skipped_reasons: Counter = Counter()
    total_input = 0
    global_idx = 0

    for ri, room in enumerate(rooms):
        room_id = f"r_{ri:04d}"
        for wi, window in enumerate(room.get("windows") or []):
            total_input += 1
            res = _window_to_opening(
                window=window,
                window_idx=wi,
                room_id=room_id,
                global_idx=global_idx,
                wall_thickness_mm=wall_thickness_mm,
            )
            if isinstance(res, WindowOpening):
                openings.append(res)
                global_idx += 1
            else:
                reason, detail = res
                skipped_reasons[reason] += 1
                if log_skipped:
                    _log_skip(room_id, wi, window, reason, detail)

    index = WindowOpeningIndex.from_openings(openings)
    stats = WindowLoadStats(
        total_input=total_input,
        total_loaded=len(openings),
        skipped_count=sum(skipped_reasons.values()),
        skipped_reasons=dict(skipped_reasons),
    )
    return index, stats


def _window_to_opening(
    *,
    window: dict,
    window_idx: int,
    room_id: str,
    global_idx: int,
    wall_thickness_mm: float,
) -> WindowOpening | tuple[str, str]:
    """Konstruiert eine ``WindowOpening`` aus einem Window-JSON-Dict."""
    block_name = window.get("block_name", "?")

    rotation = window.get("rotation_deg")
    if rotation is None:
        return (
            REASON_MISSING_ROTATION,
            f"rotation_deg is None for {block_name}",
        )
    try:
        rotation = float(rotation)
    except (TypeError, ValueError):
        return (
            REASON_MISSING_ROTATION,
            f"rotation_deg not parseable as float for {block_name}",
        )

    width_mm = _parse_window_width(window)
    if width_mm <= 0.0:
        return (REASON_DEGENERATE_WIDTH, f"width_mm={width_mm} for {block_name}")

    try:
        pos = window["position_mm"]
        px, py = float(pos[0]), float(pos[1])
        polygon = build_window_polygon(
            (px, py), rotation, width_mm, wall_thickness_mm
        )
    except (KeyError, TypeError, ValueError, IndexError) as exc:
        return (REASON_MALFORMED, f"polygon construction failed: {exc}")

    height_raw = window.get("height_mm")
    height_mm: float | None
    try:
        height_mm = float(height_raw) if height_raw is not None else None
    except (TypeError, ValueError):
        height_mm = None

    window_id = f"wo_{global_idx:04d}"
    source_ref = f"{room_id}#{block_name}#{window_idx}"
    return WindowOpening(
        window_id=window_id,
        polygon_mm=polygon,
        source_ref=source_ref,
        height_mm=height_mm,
    )


def _parse_window_width(window: dict) -> float:
    """Extrahiert die Fenster-Breite. Reihenfolge:
    1. JSON-Feld ``width_mm`` wenn finite und > 0 (im aktuellen Export
       für 76/76 Windows gesetzt).
    2. Aus ``block_name`` parsen (z.B. ``FENSTER_140`` → 1400 mm,
       ``Fenster Doppelt 196`` → 1960 mm).
    3. ``DEFAULT_WINDOW_WIDTH_MM`` (1000 mm).
    """
    raw = window.get("width_mm")
    if raw is not None:
        try:
            v = float(raw)
            if v > 0.0:
                return v
        except (TypeError, ValueError):
            pass

    parsed = _parse_width_from_block_name(window.get("block_name", "") or "")
    if parsed is not None:
        return parsed

    return DEFAULT_WINDOW_WIDTH_MM


# Pattern matcht 'FENSTER_140', 'Fenster Doppelt 196', 'FENSTER 120',
# 'Fenster_214' usw. — case-insensitive, optional 'Doppelt'.
_WIDTH_FROM_NAME_RE = re.compile(
    r"FENSTER[_ ](?:Doppelt[_ ])?(\d+)", re.IGNORECASE
)


def _parse_width_from_block_name(name: str) -> float | None:
    """``FENSTER_140`` → 1400 mm. Plausibilitäts-Range: 30–500 cm
    (kleinste WC-Fenster bis größte Schaufenster)."""
    if not name:
        return None
    m = _WIDTH_FROM_NAME_RE.search(name)
    if not m:
        return None
    try:
        cm = int(m.group(1))
    except ValueError:
        return None
    if 30 <= cm <= 500:
        return float(cm) * 10.0
    return None


def _log_skip(
    room_id: str, window_idx: int, window: dict, reason: str, detail: str
) -> None:
    block = window.get("block_name", "?")
    print(
        f"[window_opening_loader] skip {room_id}#{block}#{window_idx} "
        f"(reason={reason}): {detail}"
    )
