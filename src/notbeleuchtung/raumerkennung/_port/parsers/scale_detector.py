"""scale_detector.py — empirical coordinate-scale detection.

Multi-signal detector that measures a single factor F mapping
input-DXF geometry values to mm-world. The pipeline is interested
exclusively in `factor_to_mm`; everything else is diagnostic.

Implements Slice 9.3.0 / ADR 0006.
"""
from __future__ import annotations

import math
import statistics
from dataclasses import dataclass
from typing import Any

from ezdxf.document import Drawing

# Single-source-of-truth: door identification patterns live in
# parsers.door_patterns (a leaf module) so this detector and
# parsers.architecture_dxf can both import them without forming a
# circular import. The architecture parser's _door_geometry() bakes a
# scale factor into its returned world-mm coordinates and is therefore
# unsuitable for raw input-scale measurement — we re-implement raw
# arc-radius extraction here on top of the same patterns.
from parsers.door_patterns import (
    DOOR_LABEL_PATTERNS,
    DOOR_NAME_PATTERNS,
    SLIDING_DOOR_PATTERNS,
)

EXPECTED_DOOR_WIDTH_MM = 800.0

# Power-of-10 factors that real architectural CAD files use in practice.
# After empirical aggregation we snap onto these to keep the pipeline's
# absolute mm-world stable across runs (small door-width variance must
# not drift the factor away from its "obvious" decade).
DECADES: tuple[float, ...] = (0.1, 1.0, 10.0, 100.0, 1_000.0, 10_000.0)

# AutoCAD INSUNITS code → factor-to-mm. Only the codes we care about.
_INSUNITS_TO_MM_FACTOR: dict[int, float] = {
    1: 25.4,    # inches
    2: 304.8,   # feet
    4: 1.0,     # mm
    5: 10.0,    # cm
    6: 1000.0,  # m
}


@dataclass(frozen=True)
class ScaleInfo:
    factor_to_mm: float       # Multiplikator: Geometrie-Wert × F = mm-Welt
    confidence: float          # 0.0 - 1.0
    signals: dict[str, dict]   # Per-signal evidence (audit trail)
    source_unit: str | None    # Optional, diagnostic only ("mm"/"cm"/"m"/None)

# Faktor-zentrisch: Pipeline interessiert NUR factor_to_mm.
# source_unit ist diagnostisch (für Logs), keine Logik hängt davon ab.
# source_pattern entfernt — Pattern-Taxonomie war Plan-Erfindung,
# tatsächlich gibt es einen kontinuierlichen Faktor-Raum.


class AmbiguousScaleError(ValueError):
    """Raised when no factor_to_mm can be derived with sufficient
    confidence, or when top-2 signal votes diverge by > 20 %."""


# ── Helpers ──────────────────────────────────────────────────
def _name_match(name: str, patterns: tuple[str, ...]) -> bool:
    upper = name.upper()
    return any(p.upper() in upper for p in patterns)


def _find_wrapper_insert(msp) -> Any | None:
    """Return the single Pattern-C-style wrapper INSERT in modelspace,
    or None. Heuristic: exactly one INSERT with xscale != 1.0.

    Light-weight on purpose — load_architecture's full wall-count check
    is not duplicated here, since this signal only feeds detect_scale.
    """
    candidates = []
    for e in msp:
        if e.dxftype() != "INSERT":
            continue
        if abs(float(e.dxf.xscale) - 1.0) < 1e-9:
            continue
        candidates.append(e)
    return candidates[0] if len(candidates) == 1 else None


def _door_block_inserts(layout) -> list[Any]:
    """Swing-door INSERTs in a layout, with sliding-door + label filters."""
    out: list[Any] = []
    for e in layout:
        if e.dxftype() != "INSERT":
            continue
        name = str(e.dxf.name)
        if not _name_match(name, DOOR_NAME_PATTERNS):
            continue
        # Filter Türlisten-Stempel — they share the TÜR prefix but have
        # no ARC and no wall geometry, only an ATTDEF.
        if _name_match(name, DOOR_LABEL_PATTERNS):
            continue
        # Sliding doors have variable widths 800-1200 mm and would
        # poison the median. Only swing doors as scale source.
        if _name_match(name, SLIDING_DOOR_PATTERNS):
            continue
        out.append(e)
    return out


def _arc_radius_in_block(doc: Drawing, block_name: str) -> float | None:
    """Radius of the first ARC inside a block, or None if absent."""
    try:
        blk = doc.blocks[block_name]
    except KeyError:
        return None
    for e in blk:
        if e.dxftype() == "ARC":
            return float(e.dxf.radius)
    return None


# ── Signals ──────────────────────────────────────────────────
def _signal_door_geometry(doc: Drawing) -> dict | None:
    """Empirical scale from swing-door ARC radii.

    Iterates over door INSERTs in modelspace (Direct-Mode) or the
    Pattern-C wrapper-block when present, measures ARC radius × xscale
    × wrapper_xscale → effective modelspace width per door, takes the
    median, and returns `factor_to_mm = 800 / median`.

    Confidence: 0.7 with 1 door, 0.85 with 2, 0.95 with ≥3.
    Returns None if no usable swing doors found.
    """
    msp = doc.modelspace()
    wrapper = _find_wrapper_insert(msp)
    if wrapper is not None:
        wrapper_xscale = float(wrapper.dxf.xscale)
        try:
            layout = doc.blocks[wrapper.dxf.name]
        except KeyError:
            return None
    else:
        wrapper_xscale = 1.0
        layout = msp

    door_inserts = _door_block_inserts(layout)
    if not door_inserts:
        return None

    measured: list[float] = []
    for ins in door_inserts:
        radius = _arc_radius_in_block(doc, str(ins.dxf.name))
        if radius is None or radius <= 0:
            continue
        ix = abs(float(ins.dxf.xscale))
        if ix <= 0:
            continue
        w_msp = radius * ix * wrapper_xscale
        if w_msp > 0:
            measured.append(w_msp)

    if not measured:
        return None

    med = statistics.median(measured)
    if med <= 0:
        return None
    factor = EXPECTED_DOOR_WIDTH_MM / med

    n = len(measured)
    confidence = 0.95 if n >= 3 else (0.85 if n == 2 else 0.7)

    return {
        "factor_to_mm": factor,
        "confidence": confidence,
        "evidence": {
            "n_doors": n,
            "widths_modelspace": [round(w, 6) for w in measured],
            "median_width": round(med, 6),
            "wrapper_xscale": wrapper_xscale,
        },
    }


def _signal_block_insert_scale(doc: Drawing) -> dict | None:
    """Wrapper-INSERT xscale as a validation hint.

    Pattern C makes the wrapper.xscale an explicit scale declaration,
    but it cannot vote for a factor on its own — the block contents'
    native unit is unknown without door-geometry. We report the wrapper
    xscale as evidence so the audit trail is complete and door-geometry
    can be cross-checked at the call site.
    """
    msp = doc.modelspace()
    wrapper = _find_wrapper_insert(msp)
    if wrapper is None:
        return None
    return {
        "factor_to_mm": None,  # Validation hint, no standalone vote.
        "confidence": 0.0,
        "evidence": {
            "wrapper_block_name": str(wrapper.dxf.name),
            "wrapper_xscale": float(wrapper.dxf.xscale),
            "wrapper_yscale": float(wrapper.dxf.yscale),
            "role": "validation_hint_only",
        },
    }


def _signal_bbox_span(doc: Drawing) -> dict | None:
    """Modelspace bbox plausibility check.

    A residential apartment is typically 5-30 m wide; we widen to
    [5 000 ; 50 000] mm to cover small studios up to large family flats.
    Multiplying the raw modelspace span by candidate factors
    {0.1, 1, 10, 100, 1000, 10000} and keeping those that land in the
    plausible mm range gives a coarse vote. If exactly one candidate
    lands in range we vote for it with low confidence; otherwise we
    abstain.
    """
    msp = doc.modelspace()
    xs: list[float] = []
    ys: list[float] = []
    for e in msp:
        t = e.dxftype()
        if t == "LINE":
            xs += [float(e.dxf.start.x), float(e.dxf.end.x)]
            ys += [float(e.dxf.start.y), float(e.dxf.end.y)]
        elif t == "LWPOLYLINE":
            try:
                for p in e.get_points("xy"):
                    xs.append(float(p[0]))
                    ys.append(float(p[1]))
            except Exception:
                pass
        elif t == "INSERT":
            xs.append(float(e.dxf.insert.x))
            ys.append(float(e.dxf.insert.y))
    if not xs or not ys:
        return None
    span = max(max(xs) - min(xs), max(ys) - min(ys))
    if span <= 0:
        return None

    plausible = []
    for f in (0.1, 1.0, 10.0, 100.0, 1000.0, 10_000.0):
        if 5_000.0 <= span * f <= 50_000.0:
            plausible.append(f)

    if len(plausible) == 1:
        return {
            "factor_to_mm": plausible[0],
            "confidence": 0.5,
            "evidence": {
                "span_native": round(span, 3),
                "plausible_factors": plausible,
            },
        }
    return {
        "factor_to_mm": None,
        "confidence": 0.0,
        "evidence": {
            "span_native": round(span, 3),
            "plausible_factors": plausible,
        },
    }


def _signal_insunits_header(doc: Drawing) -> dict | None:
    """`$INSUNITS` header tiebreaker.

    Pattern B (`Architektplanblank.dxf`) proves the header lies often,
    so it is never primary — only a low-confidence tiebreaker.
    """
    code = int(doc.header.get("$INSUNITS", 0) or 0)
    if code == 0:
        return None
    f = _INSUNITS_TO_MM_FACTOR.get(code)
    if f is None:
        return None
    return {
        "factor_to_mm": f,
        "confidence": 0.3,
        "evidence": {"insunits_code": code},
    }


def _classify_unit(factor: float) -> str | None:
    for unit, ref in (("mm", 1.0), ("cm", 10.0), ("m", 1000.0)):
        if abs(factor - ref) / ref < 0.05:
            return unit
    return None


def _snap_to_decade(raw_factor: float,
                     signals: dict[str, dict]) -> tuple[float, float]:
    """Snap an empirically-aggregated factor to the nearest power-of-10
    decade with a three-zone confidence policy.

      - within  ±0.05 dec → snap, confidence multiplier 1.0
      - within ±0.15 dec → snap, confidence multiplier 0.85
      - otherwise        → keep raw, multiplier 1.0

    Distance is measured in log10 space (orders of magnitude from the
    nearest decade), consistent with the log10-proximity used to *pick*
    the nearest decade. A multiplicative metric is the correct one for a
    scale factor: it is symmetric across decades, so doors that read wide
    (BLOCKZARGE → raw ≈ 830) snap to 1000 just like doors that read narrow
    (TÜR-80 → raw ≈ 966), instead of the wide side falling outside a
    linear window. Records the decision under signals["snap"].

    Returns (snapped_or_raw_factor, confidence_multiplier).
    """
    if raw_factor <= 0:
        return raw_factor, 1.0

    log_raw = math.log10(raw_factor)
    nearest = min(DECADES, key=lambda d: abs(math.log10(d) - log_raw))
    snap_distance_pct = abs(log_raw - math.log10(nearest))

    if snap_distance_pct <= 0.05:
        snapped, mult = nearest, 1.0
    elif snap_distance_pct <= 0.15:
        snapped, mult = nearest, 0.85
    else:
        snapped, mult = raw_factor, 1.0

    signals["snap"] = {
        "raw_factor": raw_factor,
        "snapped_to": snapped,
        "snap_distance_pct": snap_distance_pct,
        "confidence_multiplier": mult,
    }
    return snapped, mult


# ── Aggregation ──────────────────────────────────────────────
def detect_scale(doc: Drawing) -> ScaleInfo:
    """Multi-signal scale detection.

    Returns a ScaleInfo with `factor_to_mm` derived primarily from
    swing-door ARC radii (target 800 mm), with bbox-span and
    `$INSUNITS` as fallback / tiebreaker, and wrapper-INSERT-xscale
    as audit evidence.

    Raises AmbiguousScaleError if no signal can vote, or if the top-2
    voting signals diverge by more than 20 % AND both have confidence
    > 0.5.
    """
    signals: dict[str, dict] = {}
    for name, fn in (
        ("door_geometry", _signal_door_geometry),
        ("block_insert_scale", _signal_block_insert_scale),
        ("bbox_span", _signal_bbox_span),
        ("insunits_header", _signal_insunits_header),
    ):
        sig = fn(doc)
        if sig is not None:
            signals[name] = sig

    voting: list[tuple[str, float, float]] = [
        (n, sig["factor_to_mm"], sig["confidence"])
        for n, sig in signals.items()
        if sig.get("factor_to_mm") is not None and sig.get("confidence", 0.0) > 0
    ]

    if not voting:
        raise AmbiguousScaleError(
            "Konnte Skala nicht erkennen. Keine Signal-Quelle hat einen "
            "Faktor geliefert. Mögliche Gründe: keine Türen im Plan, "
            "Bbox in unplausibler Range, INSUNITS=0/unset.\n"
            f"Signale: {signals}"
        )

    voting.sort(key=lambda v: -v[2])

    if len(voting) >= 2:
        f1, c1 = voting[0][1], voting[0][2]
        f2, c2 = voting[1][1], voting[1][2]
        rel_diff = abs(f1 - f2) / max(f1, f2)
        if rel_diff > 0.20 and c1 > 0.5 and c2 > 0.5:
            raise AmbiguousScaleError(
                "Skala-Signale widersprechen sich.\n"
                f"  Top-1: {voting[0][0]} → factor={f1:.3f}, conf={c1:.2f}\n"
                f"  Top-2: {voting[1][0]} → factor={f2:.3f}, conf={c2:.2f}\n"
                f"  Relative Abweichung: {rel_diff*100:.1f}% (Schwelle: 20%)\n"
                f"Signale: {signals}"
            )

    factor = voting[0][1]
    confidence = voting[0][2]
    if len(voting) >= 2:
        f2, c2 = voting[1][1], voting[1][2]
        rel = abs(factor - f2) / max(factor, f2)
        if rel < 0.05 and c2 > 0.3:
            confidence = min(0.99, confidence + 0.05)

    # Snap empirical factor to nearest decade (handles real-world door
    # width variance: 828 mm doors → raw F ≈ 965, should report F=1000).
    factor, conf_mult = _snap_to_decade(factor, signals)
    confidence = min(0.99, confidence * conf_mult)

    return ScaleInfo(
        factor_to_mm=factor,
        confidence=confidence,
        signals=signals,
        source_unit=_classify_unit(factor),
    )
