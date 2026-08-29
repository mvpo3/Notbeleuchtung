"""tueren — Tür-Blöcke (INSERT) → Tuer-Contract-Objekte.

Türen liegen als direkte INSERTs im Modelspace; der Blockname trägt die
Nennbreite in cm (Fachkonvention ``TÜR-80`` = 800 mm). Position = Insert-Punkt
in mm. Norm-Urteile (Notausgang, Schwenkrichtung) bleiben offen — reine
Geometrie/Topologie.
"""
from __future__ import annotations

import re

from notbeleuchtung.hauptengine.contracts.raum_modell import Tuer

from .dxf_load import DxfPlan

# Kandidat: Blockname nennt eine Tür …
_DOOR_HINT = re.compile(r"T(?:Ü|UE)R", re.IGNORECASE)
# … aber diese sind Marker/Beschläge, keine Tür-Blätter:
_DOOR_EXCLUDE = re.compile(r"ACHSE|ÖFFNER|OEFFNER|QUALIT", re.IGNORECASE)
_INT = re.compile(r"\d+")


def _ist_tuer_block(name: str) -> bool:
    return bool(_DOOR_HINT.search(name)) and not _DOOR_EXCLUDE.search(name)


def _breite_mm(name: str) -> float:
    """Nennbreite in mm: erste Zahl im cm-Türbereich (60–130) × 10.

    So werden Wandstärke-Tokens (``10er``/``20er``/``12-5er``) übersprungen und
    Zargen-Varianten (``BLOCKZARGE-SCHACHT_125``) korrekt getroffen.
    """
    for tok in _INT.findall(name):
        cm = int(tok)
        if 60 <= cm <= 130:
            return float(cm) * 10.0
    return 0.0


def tueren_aus_dxf(plan: DxfPlan) -> list[Tuer]:
    """Alle Tür-INSERTs → ``Tuer`` (id, xy_mm, breite_mm). von/nach offen."""
    out: list[Tuer] = []
    n = 0
    for e in plan.entities():
        if e.dxftype() != "INSERT":
            continue
        name = e.dxf.name
        if not _ist_tuer_block(name):
            continue
        (xy,) = plan.entity_points(e) or [(0.0, 0.0)]
        n += 1
        out.append(Tuer(id=f"tuer_{n}", xy_mm=xy, breite_mm=_breite_mm(name)))
    return out
