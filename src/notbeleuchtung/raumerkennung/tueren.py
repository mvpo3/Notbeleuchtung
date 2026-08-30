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

from notbeleuchtung.hauptengine.contracts.raum_modell import Tuer

from .dxf_load import DxfPlan

# Kandidat: Blockname nennt eine Tür/Öffnung …
_DOOR_HINT = re.compile(r"T(?:Ü|UE)R|ÖFFNUNG|OEFFNUNG", re.IGNORECASE)
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


