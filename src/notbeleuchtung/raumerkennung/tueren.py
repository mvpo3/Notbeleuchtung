"""tueren — Tür-Blöcke (INSERT) → Tuer + Ausgang-Contract-Objekte.

Türen liegen als direkte INSERTs im Modelspace; der Blockname trägt die
Nennbreite in cm (Fachkonvention ``TÜR-80`` = 800 mm). Position = Insert-Punkt
in mm.

**Ausgänge = Außen-/Eingangstüren** (Blocknamen ``WET_AUSSEN``, ``WET``,
``SCHIEBETÜR``, ``Fenstertür`` …): das sind die Gebäude-Egress-Punkte, an denen
im fertigen Plan die Rettungszeichen sitzen. Reine Innentüren (``TÜR-80_*er-WAND``)
sind KEINE Ausgänge. (Die alte Heuristik „Fluchtweg-Endknoten nahe Bounding-Box"
war falsch — die 09-WEG-Annotation endet am Planrahmen, nicht am Ausgang.)
"""
from __future__ import annotations

import re

from notbeleuchtung.hauptengine.contracts.raum_modell import Ausgang, Tuer

from .dxf_load import DxfPlan

# Kandidat: Blockname nennt eine Tür …
_DOOR_HINT = re.compile(r"T(?:Ü|UE)R", re.IGNORECASE)
# … aber diese sind Marker/Beschläge, keine Tür-Blätter:
_DOOR_EXCLUDE = re.compile(r"ACHSE|ÖFFNER|OEFFNER|QUALIT", re.IGNORECASE)
# Außen-/Eingangstür-Blöcke → Ausgang. WET = Wohnungseingangstür.
_AUSSENTUER = re.compile(r"AUSSEN|EINGANG|\bWET\b|WET_|SCHIEBET|FENSTERT", re.IGNORECASE)
_INT = re.compile(r"\d+")


def _ist_tuer_block(name: str) -> bool:
    if _DOOR_EXCLUDE.search(name):
        return False
    return bool(_DOOR_HINT.search(name) or _AUSSENTUER.search(name))


def _ist_aussentuer(name: str) -> bool:
    return bool(_AUSSENTUER.search(name)) and not _DOOR_EXCLUDE.search(name)


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
    """Alle Tür-INSERTs → ``Tuer`` (id, xy_mm, breite_mm). Außentüren tragen
    ``ist_notausgang=True``. von/nach offen."""
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
        out.append(Tuer(id=f"tuer_{n}", xy_mm=xy, breite_mm=_breite_mm(name),
                        ist_notausgang=_ist_aussentuer(name)))
    return out


def ausgaenge_aus_dxf(plan: DxfPlan) -> list[Ausgang]:
    """Ausgänge = Außen-/Eingangstüren (``final_exit``)."""
    out: list[Ausgang] = []
    for e in plan.entities():
        if e.dxftype() != "INSERT" or not _ist_aussentuer(e.dxf.name):
            continue
        (xy,) = plan.entity_points(e) or [(0.0, 0.0)]
        out.append(Ausgang(id=f"exit_{len(out) + 1}", xy_mm=xy, typ="final_exit"))
    return out
