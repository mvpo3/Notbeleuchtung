"""aussen_strategy — Sicherheitsleuchte AUSSERHALB jedes Schlussausgangs.

EN 1838 §4.1.2 b): „in der Nähe [ANMERKUNG: ≤ 2 m] außerhalb jedes
Schlussausgangs" ist eine hervorzuhebende Stelle — der Flüchtende muss auch
DRAUSSEN vor der Tür noch sehen, wohin er tritt. Gap-Audit H-Gebäude
(2026-09-05): die Engine platzierte ausschließlich in Räumen, der Außenraum
existierte nicht.

Umsetzung: je `Ausgang` vom Typ `final_exit` eine SL 1 m VOR der Tür — Richtung
= Auswärts-Normale der WANDKANTE am Ausgang (nächste Raum-Polygonkante; der
Auswärts-Sinn kommt vom Gebäude-Bounds-Zentrum). Ohne Polygonkante in Türnähe
fällt die Richtung auf den Zentrums-Strahl zurück — der drückte bei
außermittigen Türen die Leuchte seitlich neben die Türachse (Elektroplan DE:
+830 mm, Owner-Korrektur Runde 1). Norm-Parameter kommen wie bei den
Sonderstellen aus der Referenz-Anforderung des Regelwerks (kein Wert wird hier
erfunden); fehlt sie, wird übersprungen. `stair_exit` löst nichts aus
(Stiegenhaus ist innen, §4.1.2 a deckt es).
"""
from __future__ import annotations

from notbeleuchtung.hauptengine.contracts import NormProvider, Platzierung, RaumModell

from .bausteine import AGV_SV_F as _AGV_SV_F
from .bausteine import building_assigner as _building_assigner
from .bausteine import referenz_anforderung as _referenz

_ABSTAND_AUSSEN_MM = 1000.0   # „nahe" (≤ 2 m); 1 m vor der Tür = Praxis-Mitte
#: Ausgänge liegen AUF der Wand — eine Kante weiter weg gehört nicht zur Tür.
_MAX_WANDKANTEN_ABSTAND_MM = 1000.0


def _wand_normale(raum: RaumModell, xy: tuple[float, float],
                  auswaerts: tuple[float, float]) -> tuple[float, float] | None:
    """Einheits-Normale der nächsten Raum-Polygonkante am Punkt, auswärts orientiert.

    `auswaerts` (Strahl von der Gebäudemitte) entscheidet nur den VORZEICHEN-Sinn
    der Normale — die Achse selbst kommt aus der Wandkante. None, wenn keine
    Kante näher als `_MAX_WANDKANTEN_ABSTAND_MM` liegt (dann Fallback beim Aufrufer).
    """
    px, py = xy
    beste: tuple[float, tuple[float, float]] | None = None
    for r in raum.raeume:
        poly = r.polygon_mm
        for i in range(len(poly)):
            (ax, ay), (bx, by) = poly[i], poly[(i + 1) % len(poly)]
            ex, ey = bx - ax, by - ay
            l2 = ex * ex + ey * ey
            if l2 == 0.0:
                continue
            t = max(0.0, min(1.0, ((px - ax) * ex + (py - ay) * ey) / l2))
            qx, qy = ax + t * ex, ay + t * ey
            d = ((px - qx) ** 2 + (py - qy) ** 2) ** 0.5
            if d <= _MAX_WANDKANTEN_ABSTAND_MM and (beste is None or d < beste[0]):
                beste = (d, (ex, ey))
    if beste is None:
        return None
    ex, ey = beste[1]
    laenge = (ex * ex + ey * ey) ** 0.5
    nx, ny = -ey / laenge, ex / laenge
    if nx * auswaerts[0] + ny * auswaerts[1] < 0.0:
        nx, ny = -nx, -ny
    return (nx, ny)


def plan_aussenleuchten(raum: RaumModell, norm: NormProvider) -> list[Platzierung]:
    """Je final_exit eine SL 1 m außerhalb, auf der Türachse (Wandkanten-Normale)."""
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
        richtung = _wand_normale(raum, a.xy_mm, (dx, dy)) or (dx / n, dy / n)
        xy = (a.xy_mm[0] + richtung[0] * _ABSTAND_AUSSEN_MM,
              a.xy_mm[1] + richtung[1] * _ABSTAND_AUSSEN_MM)
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
