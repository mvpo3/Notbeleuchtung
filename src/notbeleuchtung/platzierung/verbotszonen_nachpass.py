"""verbotszonen_nachpass — Platzierungen aus Stiegenhaus-Verbotszonen holen.

Selman liefert je Stiegenhaus `verbotszonen_mm` (Laufflächen, Öffnungen — Flächen,
auf denen laut RaumModell v1.2.0 nichts montiert werden darf). Die Platzier-Strategien
kennen diese Flächen nicht und können ein Symbol auf einen Treppenlauf setzen
(Selman-BEFUND Fachteil 3: Barawitzka 4 / Mollgasse 7 Leuchten auf Verbotszonen,
`docs/OFFENE_FRAGEN.md`). Dieser Post-Pass verschiebt eine betroffene Platzierung mit
`geometry._relocate_outside_exclusions` an den nächsten montierbaren Punkt **desselben**
Stiegenhaus-Raums.

Defensiv (Selman meldet im Mollgasse-Südost übergroße Zonen-Hüllen): findet sich kein
gültiger Punkt — etwa weil eine fehlerhafte Hülle den ganzen Raum überdeckt —, bleibt die
Platzierung unverändert. Nie löschen: eine gebrauchte Leuchte verschwindet nicht still,
der Befund bleibt für die Prüfung (validierung) sichtbar. Ohne `stiegenhaeuser` bzw.
`verbotszonen_mm` ist der Pass ein No-op → bestehende Pläne bit-identisch.

Läuft in `place` nach `lb_override` und **vor** `abstand_nachpass.entzerre`, damit dieser
Kollisionen entzerrt, die eine Verschiebung erzeugt haben könnte.

Render-frei, importiert nur `hauptengine.contracts` + das eigene `geometry` (Owner-Grenze).
"""
from __future__ import annotations

from notbeleuchtung.hauptengine.contracts import Platzierung, RaumModell

from .geometry import (
    Polygon,
    _inside_any_exclusion,
    _normalise_exclusions,
    _relocate_outside_exclusions,
    point_in_polygon,
)


def _raum_polygon(raum_id: str, raum: RaumModell) -> Polygon | None:
    """Polygon des Stiegenhaus-Raums (per id); None, wenn unbekannt/degeneriert."""
    for r in raum.raeume:
        if r.id == raum_id and len(r.polygon_mm) >= 3:
            return r.polygon_mm
    return None


def entferne_aus_verbotszonen(
    placements: list[Platzierung], raum: RaumModell
) -> list[Platzierung]:
    """Verschiebt Platzierungen aus Stiegenhaus-Verbotszonen an den nächsten
    montierbaren Punkt desselben Raums.

    Gibt eine neue Liste in Original-Reihenfolge zurück (verschobene tragen neues
    ``xy_mm``); mutiert die Eingabe nicht. No-op ohne Verbotszonen."""
    # Je Stiegenhaus-Raum: (Raumpolygon, normalisierte Verbots-Polygone). `_normalise_
    # exclusions` wirft degenerierte/nicht-überlappende Hüllen raus.
    zonen: dict[str, tuple[Polygon, list[Polygon]]] = {}
    for sh in raum.stiegenhaeuser:
        if not sh.verbotszonen_mm:
            continue
        poly = _raum_polygon(sh.raum_id, raum)
        if poly is None:
            continue
        excl = _normalise_exclusions(poly, [list(z) for z in sh.verbotszonen_mm])
        if excl:
            zonen[sh.raum_id] = (poly, excl)
    if not zonen:
        return list(placements)

    ergebnis: list[Platzierung] = []
    for p in placements:
        neu_p = p
        for poly, excl in zonen.values():
            if point_in_polygon(p.xy_mm, poly) and _inside_any_exclusion(p.xy_mm, excl):
                andere = [q.xy_mm for q in placements if q is not p]
                neu_xy = _relocate_outside_exclusions(p.xy_mm, poly, excl, existing=andere)
                if neu_xy != p.xy_mm:
                    neu_p = p.model_copy(update={"xy_mm": neu_xy})
                break  # eine Platzierung liegt in höchstens einem Stiegenhaus-Raum
        ergebnis.append(neu_p)
    return ergebnis
