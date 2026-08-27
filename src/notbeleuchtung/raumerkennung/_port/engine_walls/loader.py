"""loader.py — Wand-Loader für architecture_parsed.json (Slice 11.2.0).

Liest die `walls`-Liste aus `architecture_parsed.json` ein und konstruiert
`list[Wall]` via `Wall.from_arch_dict()`. Degenerate Walls (length_mm
unter Wall-Validation-Schwelle) werden gefangen und im LoadStats-Report
mit `review_reason="degenerate_zero_length"` aufgeführt.

Walls behalten ihren ursprünglichen Listen-Index als id-Padding
(`f"w_{idx:04d}"`), damit `walls_idx`-Lookups aus dem
`check_architecture`-Schema konsistent bleiben.

Loader ist Modul-Funktion (state-less). Pattern analog zu
`parsers/scale_detector.detect_scale()`.
"""
from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

from engine.walls.wall import Wall

# Skip-Reasons als Konstanten — andere Konsumenten können sie referenzieren.
REASON_DEGENERATE_ZERO_LENGTH = "degenerate_zero_length"
REASON_MALFORMED = "malformed_arch_dict"


@dataclass(frozen=True)
class LoadStats:
    """Statistik-Snapshot eines Loader-Runs."""
    total_input: int
    valid_walls: int
    skipped_walls: int
    skipped_reasons: dict[str, int] = field(default_factory=dict)
    wall_type_distribution: dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "total_input": self.total_input,
            "valid_walls": self.valid_walls,
            "skipped_walls": self.skipped_walls,
            "skipped_reasons": dict(self.skipped_reasons),
            "wall_type_distribution": dict(self.wall_type_distribution),
        }


def load_walls_from_arch(
    arch_path: Path | str,
    *,
    log_skipped: bool = True,
) -> tuple[list[Wall], LoadStats]:
    """Load `Wall`-Instanzen aus `architecture_parsed.json`.

    Parameters
    ----------
    arch_path
        Pfad zu `architecture_parsed.json` (oder kompatiblem File mit
        `walls: list[{start_mm, end_mm, wall_type, ...}]`).
    log_skipped
        Wenn True (Default), wird pro übersprungener Wand eine
        einzeilige Diagnose-Zeile auf stdout ausgegeben. Tests/CI
        können `log_skipped=False` setzen für leise Ausführung.

    Returns
    -------
    walls : list[Wall]
        Alle erfolgreich konstruierten Walls. IDs `f"w_{idx:04d}"`
        encodiert den Original-Listen-Index aus dem File (Skipped
        belegen Indizes, sind aber nicht in der Liste).
    stats : LoadStats
        total_input, valid_walls, skipped_walls + aggregierte Counts
        nach skip-reason und wall_type.

    Raises
    ------
    FileNotFoundError
        Wenn `arch_path` nicht existiert.
    ValueError
        Wenn das File kein gültiges JSON ist oder kein top-level
        `walls`-Key enthält.
    """
    p = Path(arch_path)
    if not p.exists():
        raise FileNotFoundError(f"architecture_parsed.json not found at {p}")

    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"corrupt JSON at {p}: {exc}") from exc

    walls_raw = data.get("walls")
    if walls_raw is None:
        raise ValueError(f"no 'walls' key in {p} (top-level keys: {list(data.keys())})")
    if not isinstance(walls_raw, list):
        raise ValueError(f"'walls' is not a list in {p} (got {type(walls_raw).__name__})")

    walls: list[Wall] = []
    skipped_reasons: Counter = Counter()

    for idx, d in enumerate(walls_raw):
        try:
            w = Wall.from_arch_dict(d, idx=idx)
        except ValueError as exc:
            # length_mm < threshold → degenerate
            reason = REASON_DEGENERATE_ZERO_LENGTH
            skipped_reasons[reason] += 1
            if log_skipped:
                _log_skip(idx, d, reason, str(exc))
            continue
        except (KeyError, TypeError) as exc:
            # Schema-Verstoß — fehlende start_mm/end_mm/wall_type oder Typ-Fehler
            reason = REASON_MALFORMED
            skipped_reasons[reason] += 1
            if log_skipped:
                _log_skip(idx, d, reason, str(exc))
            continue
        walls.append(w)

    wall_type_distribution: Counter = Counter(w.wall_type for w in walls)

    stats = LoadStats(
        total_input=len(walls_raw),
        valid_walls=len(walls),
        skipped_walls=sum(skipped_reasons.values()),
        skipped_reasons=dict(skipped_reasons),
        wall_type_distribution=dict(wall_type_distribution),
    )
    return walls, stats


def _log_skip(idx: int, d: dict, reason: str, detail: str) -> None:
    """One-line skip-message for CLI visibility."""
    start = d.get("start_mm", "?")
    end = d.get("end_mm", "?")
    print(
        f"[wall_loader] skip w_{idx:04d} (reason={reason}): "
        f"start={start} end={end} | {detail}"
    )
