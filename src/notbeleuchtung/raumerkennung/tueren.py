"""tueren — Türen aus dem Plan → ``Tuer``-Contract-Objekte (F2→F1-Naht).

F1 (`richtung_durch_tuer`) konsumiert `RaumModell.tueren` an den ECHTEN Öffnungen
— darum müssen hier alle Familien echte Türen liefern. Drei Darstellungen:

1. **Benannte Tür-Blöcke** (Mollgasse ``TÜR-80…`` / Fischamender ``…_Zimmertür``,
   Baufeld ``Öffnung_N``): Position = INSERT-Punkt, Breite ggf. aus Blockname.
2. **Schwenkbögen** (ArchiCAD: Barawitzka/Herrenholz — Türen ohne Block, nur ARC):
   je Türblatt-ARC (r≈600–1300 mm) eine Tür am Drehpunkt. Fallback, wenn (1) leer.

**Außentüren** (``WET_AUSSEN``/``SCHIEBETÜR``/…) tragen ``ist_notausgang=True``.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

from notbeleuchtung.hauptengine.contracts.raum_modell import Tuer

from .dxf_load import XY, DxfPlan

# Kandidat: Blockname nennt eine Tür/Öffnung …
_DOOR_HINT = re.compile(r"T(?:Ü|UE)R|ÖFFNUNG|OEFFNUNG|\bBST\b|F\+H", re.IGNORECASE)
# … aber diese sind Marker/Beschläge, keine Tür-Blätter:
_DOOR_EXCLUDE = re.compile(r"ACHSE|ÖFFNER|OEFFNER|QUALIT", re.IGNORECASE)
# Außen-/Eingangstür-Blöcke → Ausgang. WET = Wohnungseingangstür.
_AUSSENTUER = re.compile(r"AUSSEN|EINGANG|\bWET\b|WET_|SCHIEBET|FENSTERT", re.IGNORECASE)
_OEFFNUNG = re.compile(r"ÖFFNUNG|OEFFNUNG", re.IGNORECASE)
_INT = re.compile(r"\d+")

_ARC_MIN_MM, _ARC_MAX_MM = 600.0, 1300.0  # Türblatt-Schwenkbogen-Radius


def _ist_tuer_block(name: str) -> bool:
    if _DOOR_EXCLUDE.search(name):
        return False
    return bool(_DOOR_HINT.search(name) or _AUSSENTUER.search(name))


def _ist_aussentuer(name: str) -> bool:
    return bool(_AUSSENTUER.search(name)) and not _DOOR_EXCLUDE.search(name)


def _breite_mm(name: str) -> float:
    """Nennbreite in mm: erste Zahl im cm-Türbereich (60–130) × 10.

    Öffnungs-Marker (``Öffnung_81``) tragen eine ID, keine Breite → 0.
    """
    if _OEFFNUNG.search(name):
        return 0.0
    for tok in _INT.findall(name):
        n = int(tok)
        if 60 <= n <= 130:        # cm-Konvention (TÜR-80)
            return float(n) * 10.0
        if 600 <= n <= 1300:      # mm direkt (…_0800x2000)
            return float(n)
    return 0.0


def _block_tueren(plan: DxfPlan) -> list[Tuer]:
    out: list[Tuer] = []
    for e in plan.entities():
        if e.dxftype() != "INSERT" or not _ist_tuer_block(e.dxf.name):
            continue
        (xy,) = plan.entity_points(e) or [(0.0, 0.0)]
        out.append(Tuer(id=f"tuer_{len(out) + 1}", xy_mm=xy,
                        breite_mm=_breite_mm(e.dxf.name),
                        ist_notausgang=_ist_aussentuer(e.dxf.name)))
    return out


def _arc_tueren(plan: DxfPlan) -> list[Tuer]:
    """Fallback (ArchiCAD): Tür-Schwenkbögen → Tür am Drehpunkt, Breite = Radius."""
    out: list[Tuer] = []
    for e in plan.entities():
        if e.dxftype() != "ARC":
            continue
        r = float(e.dxf.radius) * plan.factor
        if _ARC_MIN_MM < r < _ARC_MAX_MM:
            out.append(Tuer(id=f"tuer_{len(out) + 1}",
                            xy_mm=plan._scale(e.dxf.center), breite_mm=round(r)))
    return out


def tueren_aus_dxf(plan: DxfPlan) -> list[Tuer]:
    """Türen aller Familien → ``Tuer``. Benannte Blöcke zuerst; sonst Schwenkbögen."""
    out = _block_tueren(plan)
    if not out:
        out = _arc_tueren(plan)
    return out


# ── Türöffnungen (auch IN Blockdefinitionen) ─────────────────────────────────
_SWEEP_MIN, _SWEEP_MAX = 60.0, 120.0  # Türblatt schwenkt ~90°


@dataclass
class TuerOeffnung:
    """Eine Türöffnung — Position + Nennbreite, quelle 'block' oder 'arc'."""

    xy_mm: XY
    breite_mm: float
    winkel_grad: float | None
    quelle: str


def _blattbreite_aus_block(insert, factor: float, tiefe: int = 0) -> float:
    """Türblatt-Breite = Radius des Schwenkbogen-ARC in der Blockdefinition
    (Rennweg-Zargentüren tragen keine Breite im Namen). Spiegelung (xscale=-1)
    ist egal — der Radius ist skaleninvariant bei |scale|=1."""
    try:
        for v in insert.virtual_entities():
            if v.dxftype() == "ARC":
                r = float(v.dxf.radius) * factor
                if _ARC_MIN_MM < r < _ARC_MAX_MM:
                    return float(round(r))
            elif v.dxftype() == "INSERT" and tiefe < 2:
                r = _blattbreite_aus_block(v, factor, tiefe + 1)
                if r:
                    return r
    except Exception:  # noqa: BLE001, S110 — kaputter Block liefert eben keine Breite
        pass
    return 0.0


def tuer_oeffnungen(plan: DxfPlan) -> list[TuerOeffnung]:
    """Alle Türöffnungen — Tür-Blöcke UND Schwenkbogen-ARCs, auch INNERHALB von
    Blockdefinitionen (virtual_entities-Walk, Tiefe ≤3). In Tür-Blöcke wird
    nicht hinein-rekursiert (deren ARC ist das Türblatt, keine zweite Tür)."""
    out: list[TuerOeffnung] = []

    def _walk(entities, tiefe: int = 0) -> None:
        for e in entities:
            t = e.dxftype()
            if t == "INSERT":
                name = str(e.dxf.name)
                if _ist_tuer_block(name):
                    breite = _breite_mm(name) or _blattbreite_aus_block(e, plan.factor)
                    out.append(TuerOeffnung(
                        xy_mm=plan._scale(e.dxf.insert), breite_mm=breite,
                        winkel_grad=float(e.dxf.get("rotation", 0.0)),
                        quelle="block"))
                elif tiefe < 3:
                    try:
                        _walk(e.virtual_entities(), tiefe + 1)
                    except Exception:  # noqa: BLE001, S110 — kaputter Block killt den Walk nicht
                        pass
            elif t == "ARC":
                r = float(e.dxf.radius) * plan.factor
                sweep = (float(e.dxf.end_angle) - float(e.dxf.start_angle)) % 360.0
                if _ARC_MIN_MM < r < _ARC_MAX_MM and _SWEEP_MIN <= sweep <= _SWEEP_MAX:
                    out.append(TuerOeffnung(
                        xy_mm=plan._scale(e.dxf.center), breite_mm=float(round(r)),
                        winkel_grad=float(e.dxf.start_angle), quelle="arc"))

    _walk(plan.space)
    return out


