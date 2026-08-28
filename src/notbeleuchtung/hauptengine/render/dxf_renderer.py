"""dxf_renderer — PlatzierungsErgebnis + RaumModell → Notbeleuchtungs-DXF.

Generative Adaption von elektro-planer backend/engine/dxf_writer.py (siehe
docs/PORT_LOG.md): konsumiert Contract-Objekte statt Placement-/Architektur-
JSON. Gezeichnet werden Raum-Konturen + raum_typ-Labels, Fluchtweg-Segmente,
die Schrack-Symbole (via symbols/inserter) und Stromkreis-Labels mit
Anti-Kollision. Wände/Pass-Through-Architektur, Höhenkoten und das
Paperspace-Layout-Template folgen in späteren Slices.

Layer-Entscheid (statt Port der elektro-planer layer_convention): die Symbole
liegen auf dem Library-Layer `E_Sicherheitsbeleuchtung` (DoD + Block-Geometrie
nutzen ihn); dazu zwei eigene Layer für Labels und Architektur-Kontur.
"""
from __future__ import annotations

import math
from pathlib import Path

import ezdxf
from ezdxf.enums import MTextEntityAlignment

from notbeleuchtung.hauptengine.contracts import PlatzierungsErgebnis, RaumModell
from notbeleuchtung.symbols import inserter, library

LAYER_NOTBELEUCHTUNG = library.SAFETY_LAYER
LAYER_STROMKREIS = "E_Stromkreis_Label"
LAYER_ARCH_RAUM = "ARCH_Raum"
LAYER_FLUCHTWEG = "ARCH_Fluchtweg"

ROOM_LABEL_HEIGHT_MM = 120.0

# Stromkreis-Label — Konstanten verbatim aus elektro-planer dxf_writer.py:
# Offset folgt der Symbol-Normale (freie Raumseite), Text bleibt horizontal;
# Anti-Kollision: x-Band + Mindest-Vertikalabstand, bei Kollision weiter
# entlang der Normale hinausschieben (Korrektur-DXF TOP 24: median 235 mm).
CIRCUIT_LABEL_HEIGHT_MM = 90.0
CIRCUIT_LABEL_OFFSET_NORMAL_MM = 240.0
CIRCUIT_LABEL_BAND_X_MM = 300.0
CIRCUIT_LABEL_MIN_GAP_MM = 150.0
CIRCUIT_LABEL_MAX_NUDGE = 8


def _add_own_layers(doc) -> None:
    doc.layers.add(LAYER_STROMKREIS, color=4)   # cyan
    doc.layers.add(LAYER_ARCH_RAUM, color=8)    # dunkelgrau
    doc.layers.add(LAYER_FLUCHTWEG, color=9)    # hellgrau


def _draw_raeume(msp, raum: RaumModell) -> int:
    """Raum-Polygone als geschlossene LWPOLYLINE + raum_typ-Label am Zentroid."""
    drawn = 0
    for r in raum.raeume:
        if len(r.polygon_mm) < 3:
            continue
        msp.add_lwpolyline(
            list(r.polygon_mm),
            close=True,
            dxfattribs={"layer": LAYER_ARCH_RAUM},
        )
        cx = sum(p[0] for p in r.polygon_mm) / len(r.polygon_mm)
        cy = sum(p[1] for p in r.polygon_mm) / len(r.polygon_mm)
        mt = msp.add_mtext(
            f"{r.raum_typ} ({r.id})",
            dxfattribs={"layer": LAYER_ARCH_RAUM, "char_height": ROOM_LABEL_HEIGHT_MM},
        )
        mt.set_location((cx, cy), attachment_point=MTextEntityAlignment.MIDDLE_CENTER)
        drawn += 1
    return drawn


def _draw_segmente(msp, raum: RaumModell) -> int:
    """Fluchtweg-Segmente als dünne Polylines (Review gegen die GU-PDF)."""
    drawn = 0
    for seg in raum.zirkulation.segmente:
        if len(seg.polyline_mm) < 2:
            continue
        msp.add_lwpolyline(
            list(seg.polyline_mm),
            dxfattribs={"layer": LAYER_FLUCHTWEG},
        )
        drawn += 1
    return drawn


def _draw_circuit_label(
    msp,
    x: float,
    y: float,
    circuit_hint: str,
    rotation_deg: float,
    placed: list[tuple[float, float]],
) -> bool:
    """Stromkreis-Label als MTEXT entlang der Symbol-Normale, anti-kollidierend."""
    text = (circuit_hint or "").strip()
    if not text:
        return False
    angle = math.radians(rotation_deg or 0.0)
    nx = -math.sin(angle)
    ny = math.cos(angle)
    tx = x + nx * CIRCUIT_LABEL_OFFSET_NORMAL_MM
    ty = y + ny * CIRCUIT_LABEL_OFFSET_NORMAL_MM
    guard = 0
    while guard < CIRCUIT_LABEL_MAX_NUDGE and any(
        abs(tx - px) < CIRCUIT_LABEL_BAND_X_MM
        and abs(ty - py) < CIRCUIT_LABEL_MIN_GAP_MM
        for (px, py) in placed
    ):
        tx += nx * CIRCUIT_LABEL_MIN_GAP_MM
        ty += ny * CIRCUIT_LABEL_MIN_GAP_MM
        guard += 1
    placed.append((tx, ty))
    # Attachment so, dass der Text vom Symbol WEG wächst.
    if abs(nx) >= abs(ny):
        attach = (MTextEntityAlignment.MIDDLE_LEFT if nx > 0
                  else MTextEntityAlignment.MIDDLE_RIGHT)
    else:
        attach = (MTextEntityAlignment.BOTTOM_CENTER if ny > 0
                  else MTextEntityAlignment.TOP_CENTER)
    mt = msp.add_mtext(text, dxfattribs={
        "layer": LAYER_STROMKREIS,
        "char_height": CIRCUIT_LABEL_HEIGHT_MM,
    })
    mt.set_location((tx, ty), attachment_point=attach)
    return True


def _set_vport(doc, raum: RaumModell, platzierung: PlatzierungsErgebnis) -> None:
    """Initial-Ansicht = Grundriss: Modelspace-VPORT auf Bounds ∪ Symbolpunkte,
    sonst öffnet AutoCAD bei (0,0) und der Plan muss per Zoom-Extents gesucht
    werden. Höhe mit Rand, Breite über konservatives Seitenverhältnis (1.5)."""
    xs = [p.xy_mm[0] for p in platzierung.platzierungen]
    ys = [p.xy_mm[1] for p in platzierung.platzierungen]
    xs += [raum.bounds_mm.min_xy[0], raum.bounds_mm.max_xy[0]]
    ys += [raum.bounds_mm.min_xy[1], raum.bounds_mm.max_xy[1]]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    height = max(y1 - y0, (x1 - x0) / 1.5, 1000.0) * 1.1
    doc.set_modelspace_vport(height, center=((x0 + x1) / 2.0, (y0 + y1) / 2.0))


def render_dxf(
    platzierung: PlatzierungsErgebnis,
    raum: RaumModell,
    out_path: Path | str,
) -> dict:
    """Notbeleuchtungs-DXF schreiben; Summary-Superset des Pipeline-Stubs."""
    out_path = Path(out_path)
    doc = ezdxf.new("R2018", units=4)  # 4 = mm
    library.sync_layers(doc)
    _add_own_layers(doc)
    msp = doc.modelspace()

    n_raeume_drawn = _draw_raeume(msp, raum)
    n_segmente = _draw_segmente(msp, raum)

    by_kind: dict[str, int] = {}
    placed_labels: list[tuple[float, float]] = []
    circuit_labels = 0
    for p in platzierung.platzierungen:
        inserter.insert_platzierung(doc, p)
        by_kind[p.kind] = by_kind.get(p.kind, 0) + 1
        if _draw_circuit_label(
            msp, p.xy_mm[0], p.xy_mm[1], p.circuit_hint, p.rotation_deg, placed_labels
        ):
            circuit_labels += 1

    _set_vport(doc, raum, platzierung)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    doc.saveas(str(out_path))

    return {
        "floor": platzierung.floor,
        "n_symbols": len(platzierung.platzierungen),
        "by_kind": by_kind,
        "n_raeume": len(raum.raeume),
        "rendered": True,
        "output_path": str(out_path),
        "schrack_inserted": len(platzierung.platzierungen),
        "circuit_labels_drawn": circuit_labels,
        "raum_konturen_drawn": n_raeume_drawn,
        "fluchtweg_segmente_drawn": n_segmente,
        "layer": LAYER_NOTBELEUCHTUNG,
    }
