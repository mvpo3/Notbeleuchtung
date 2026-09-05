"""aussen_strategy — Sicherheitsleuchte AUSSERHALB jedes Schlussausgangs.

EN 1838 §4.1.2 b): „in der Nähe [ANMERKUNG: ≤ 2 m] außerhalb jedes
Schlussausgangs" ist eine hervorzuhebende Stelle — der Flüchtende muss auch
DRAUSSEN vor der Tür noch sehen, wohin er tritt. Gap-Audit H-Gebäude
(2026-09-05): die Engine platzierte ausschließlich in Räumen, der Außenraum
existierte nicht.

Umsetzung: je `Ausgang` vom Typ `final_exit` eine SL 1 m VOR der Tür — Richtung
= Auswärts-Normale (vom Gebäude-Bounds-Zentrum weg, Ausgänge liegen am Rand).
Norm-Parameter kommen wie bei den Sonderstellen aus der Referenz-Anforderung
des Regelwerks (kein Wert wird hier erfunden); fehlt sie, wird übersprungen.
`stair_exit` löst nichts aus (Stiegenhaus ist innen, §4.1.2 a deckt es).
"""
from __future__ import annotations

from notbeleuchtung.hauptengine.contracts import NormProvider, Platzierung, RaumModell

from .communal_stgh_strategy import _AGV_SV_F, _building_assigner
from .sonderstellen_strategy import _referenz

_ABSTAND_AUSSEN_MM = 1000.0   # „nahe" (≤ 2 m); 1 m vor der Tür = Praxis-Mitte


def plan_aussenleuchten(raum: RaumModell, norm: NormProvider) -> list[Platzierung]:
    """Je final_exit eine SL 1 m außerhalb (Auswärts-Normale von der Gebäudemitte)."""
    exits = [a for a in raum.ausgaenge if a.typ == "final_exit"]
    if not exits:
        return []
    anf = _referenz(norm, "sicherheitsleuchte")
    if anf is None:
        return []
    (min_x, min_y), (max_x, max_y) = raum.bounds_mm.min_xy, raum.bounds_mm.max_xy
    cx, cy = (min_x + max_x) / 2.0, (min_y + max_y) / 2.0
    assign_building = _building_assigner([a.xy_mm[0] for a in exits])

    out: list[Platzierung] = []
    for a in exits:
        dx, dy = a.xy_mm[0] - cx, a.xy_mm[1] - cy
        n = (dx * dx + dy * dy) ** 0.5 or 1.0
        xy = (a.xy_mm[0] + dx / n * _ABSTAND_AUSSEN_MM,
              a.xy_mm[1] + dy / n * _ABSTAND_AUSSEN_MM)
        out.append(Platzierung(
            xy_mm=xy,
            catalog_key=anf.symbol_katalog_keys[0],
            rotation_deg=0.0,
            height_mm=float(anf.montagehoehe_mm),
            kind="sicherheitsleuchte",
            richtung="gerade",
            circuit_hint=f"AGV-{assign_building(a.xy_mm[0])}-F{_AGV_SV_F}",
            covers_segment=[],
            norm_quelle=anf.quelle,
        ))
    return out
