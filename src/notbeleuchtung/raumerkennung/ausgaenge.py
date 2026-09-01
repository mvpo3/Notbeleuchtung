"""ausgaenge — Ausgänge über alle CAD-Familien (Kaskade statt Ein-Muster).

Bisher kam die Ausgangs-Erkennung ausschließlich aus einem einzigen Muster:
Doppeltür als zwei Schwenkbögen an der Gebäude-Außenkante (``footprint``). Das
ist Mollgasse-Kalibrierung — Fischamender/Barawitzka/Herrenholz lieferten damit
**0 Ausgänge**, womit F1 keine Rettungszeichen routen kann (Board-Ticket B2).

Darum eine **Kaskade**: die erste Stufe, die etwas findet, gewinnt. Jede Stufe
ist ein eigenständiges Zeichen-Muster einer CAD-Familie, von „am spezifischsten"
nach „am robustesten":

1. **Doppeltür am Gebäude-Rand** → ``final_exit`` (Mollgasse-Fachmuster).
2. **Außentür-Block am Gebäude-Rand** → ``final_exit`` (``WET_AUSSEN``/
   ``EINGANG``/``SCHIEBETÜR``… — ``tueren`` markiert die bereits).
3. **Stiegenhaus-Anker** → ``stair_exit`` (ArchiCAD/Fischamender ohne
   Eingangs-Sonderzeichnung; das Stiegenhaus IST der Fluchtweg-Endpunkt).
4. **Fallback: jede Tür am Gebäude-Rand** → ``door``, damit F1 nie mit einer
   leeren Liste dasteht.

Reine Geometrie/Topologie — kein Norm-Urteil (das bleibt Enis/Leonis).
"""
from __future__ import annotations

import math

from notbeleuchtung.hauptengine.contracts.raum_modell import Ausgang, BBox, Tuer

from .dxf_load import DxfPlan
from .footprint import Umriss, gebaeude_umriss, hauptausgaenge
from .geometrie_typ import stiege_rechtecke

XY = tuple[float, float]

_MERGE_MM = 1000.0        # Ausgänge näher als das sind dieselbe Öffnung
_TUER_AM_ANKER_MM = 6000.0  # Tür in dieser Nähe repräsentiert das Stiegenhaus


def _dedup(kandidaten: list[XY]) -> list[XY]:
    """Positionen zusammenfassen, die dieselbe Öffnung meinen (< ``_MERGE_MM``)."""
    out: list[XY] = []
    for xy in kandidaten:
        if not any(math.dist(xy, vorhanden) < _MERGE_MM for vorhanden in out):
            out.append(xy)
    return out


def _als_ausgaenge(punkte: list[XY], typ: str) -> list[Ausgang]:
    return [
        Ausgang(id=f"exit_{i}", xy_mm=(float(x), float(y)), typ=typ)
        for i, (x, y) in enumerate(_dedup(punkte), start=1)
    ]


def _aussentueren_am_rand(tueren: list[Tuer], umriss: Umriss) -> list[XY]:
    """Stufe 2: als Außen-/Eingangstür markierte Türen an der Gebäude-Außenkante."""
    return [t.xy_mm for t in tueren if t.ist_notausgang and umriss.ist_am_rand(t.xy_mm)]


def _stiegenhaus_anker(plan: DxfPlan, tueren: list[Tuer]) -> list[XY]:
    """Stufe 3: je Treppen-Anker die nächstgelegene Tür, sonst das Anker-Zentrum.

    Die Tür ist die bessere Position (dort hängt das Rettungszeichen), das
    Zentrum nur der Notnagel für Pläne ohne erkannte Türen am Stiegenhaus.
    """
    out: list[XY] = []
    for _rect, center, _area in stiege_rechtecke(plan):
        naechste = min(
            (t for t in tueren if math.dist(t.xy_mm, center) <= _TUER_AM_ANKER_MM),
            key=lambda t: math.dist(t.xy_mm, center),
            default=None,
        )
        out.append(naechste.xy_mm if naechste is not None else center)
    return out


def ausgaenge_ermitteln(
    plan: DxfPlan, tueren: list[Tuer], bounds: BBox
) -> list[Ausgang]:
    """Ausgänge über die Familien-Kaskade (siehe Modul-Docstring)."""
    umriss = gebaeude_umriss(plan, bounds)

    doppeltueren = hauptausgaenge(plan, bounds, umriss=umriss)
    if doppeltueren:
        return doppeltueren

    if umriss is not None:
        aussen = _aussentueren_am_rand(tueren, umriss)
        if aussen:
            return _als_ausgaenge(aussen, "final_exit")

    stiegen = _stiegenhaus_anker(plan, tueren)
    if stiegen:
        return _als_ausgaenge(stiegen, "stair_exit")

    if umriss is not None:
        am_rand = [t.xy_mm for t in tueren if umriss.ist_am_rand(t.xy_mm)]
        if am_rand:
            return _als_ausgaenge(am_rand, "door")

    return []
