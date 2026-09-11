"""mittellinie_snap — Owner-Korrektur 2026-09-10 (AutoCAD-Diff L-Demo): Rettungszeichen
und Aufheller im Gang liegen auf der **Korridor-Mittelachse**, nicht off-center.

Post-Pass: snappt jedes RZ/SL/Antipanik-Symbol in einem geraden GANG-Arm auf die
geometrische **Kurzachsen-Mitte** des Arms (z.B. 1,5-m-Gang → Symbol auf 0,75 m). Die
Querachse wird zentriert, die Längsachse bleibt (Abstände erhalten, keine Kollisionen).

Bewusst NICHT die skelettierte `mittellinie`: deren Raster-Skelett zappelt (±200 mm) und
träfe die saubere Mitte nicht. Ein gerader Korridor-Arm ist ein Rechteck-Streifen — seine
Mitte ist exakt die Bbox-Mitte der kurzen Achse.

Ausgenommen: Tür-RZ (`QUELLE_TUERLEUCHTE`, gehört an die Tür) und quadratische Räume
(Pocket/Knoten ohne klare Längsachse). Render-frei, kein Contract berührt.

R1 (Owner-Korrektur 2026-09-11, AutoCAD-Diff Elektroplan DE, 3× notiert „immer in einer
Linie mit der Beleuchtung"): liegen BESTANDS-Leuchten der Allgemeinbeleuchtung im Gang
(z.B. die Spot-Reihe der Architektur-Unterlage), ist DEREN Linie die Montagelinie — die
Notleuchten sitzen in einer Reihe mit dem Bestand, nicht auf der geometrischen Bbox-Mitte
(Beleg: Spot-Reihe y=1735,829, Owner-Symbole exakt darauf; Bbox-Mitte lag 300 mm daneben).
Ohne Bestands-Punkte: bisheriges Verhalten (Bbox-Mitte).
"""
from __future__ import annotations

import statistics

from notbeleuchtung.hauptengine.contracts import Platzierung, RaumModell

from .bausteine import KORRIDOR_TYPEN as _KORRIDOR_TYPEN
from .fachpraxis import QUELLE_TUERLEUCHTE
from .geometry import _bbox, point_in_polygon

_KINDS = ("rz", "sicherheitsleuchte", "antipanik")
_LAENGS_FAKTOR = 2.0   # Arm gilt erst als „gerader Korridor", wenn lang >= 2× kurz
_MIN_SNAP_MM = 20.0    # kleinere Verschiebung = schon zentriert, unverändert lassen
#: R1: Bestands-Leuchten gelten nur als „Reihe", wenn ihre Querstreuung im Arm klein ist —
#: sonst ist es keine Linie (z.B. versetzte Wandleuchten) und die Bbox-Mitte bleibt.
_BESTAND_QUER_SPREAD_MM = 600.0
_BESTAND_MIN_PUNKTE = 2
#: R6 (Owner-Korrektur 2026-09-11, 2ד So nicht mitten in der Lampe"): eine Notleuchte
#: auf der Bestandslinie darf nicht AUF einer Bestands-Leuchte sitzen — unter diesem
#: Längsabstand weicht sie in die Mitte der Spot-Lücke aus, in der sie steht.
_BESTAND_MIN_LAENGS_MM = 800.0


def _korridor_achse(polygon):
    """(achse, mitte) für einen geraden Gang-Arm: 'x' bzw. 'y' = die zu zentrierende
    Querachse, mitte = deren Bbox-Mitte. None, wenn der Raum zu quadratisch ist."""
    x0, y0, x1, y1 = _bbox(polygon)
    w, h = x1 - x0, y1 - y0
    if w >= _LAENGS_FAKTOR * h:          # horizontaler Arm → y zentrieren
        return "y", (y0 + y1) / 2.0
    if h >= _LAENGS_FAKTOR * w:          # vertikaler Arm → x zentrieren
        return "x", (x0 + x1) / 2.0
    return None, 0.0


def _bestand_mitte(achse, polygon, bestand_leuchten_mm):
    """R1: (quer_median, laengs_sortiert) der Bestands-Leuchten IM Korridor — oder
    (None, ()) wenn keine belastbare Reihe da ist (zu wenige Punkte / zu breit gestreut)."""
    drin = [p for p in bestand_leuchten_mm if point_in_polygon((p[0], p[1]), polygon)]
    quer = [p[1] if achse == "y" else p[0] for p in drin]
    if len(quer) < _BESTAND_MIN_PUNKTE or max(quer) - min(quer) > _BESTAND_QUER_SPREAD_MM:
        return None, ()
    laengs = tuple(sorted(p[0] if achse == "y" else p[1] for p in drin))
    return statistics.median(quer), laengs


def _laengs_ausweichen(laengs: float, spots: tuple[float, ...]) -> float:
    """R6: sitzt die Leuchte längs näher als `_BESTAND_MIN_LAENGS_MM` an einem
    Bestands-Spot, weicht sie in die Mitte der Lücke aus, in der sie steht
    (vor/nach der Reihe: auf Mindestabstand vom Randspot)."""
    if not spots:
        return laengs
    naechster = min(spots, key=lambda s: abs(s - laengs))
    if abs(naechster - laengs) >= _BESTAND_MIN_LAENGS_MM:
        return laengs
    i = spots.index(naechster)
    if laengs <= spots[0]:
        return spots[0] - _BESTAND_MIN_LAENGS_MM
    if laengs >= spots[-1]:
        return spots[-1] + _BESTAND_MIN_LAENGS_MM
    lo, hi = (spots[i - 1], naechster) if laengs < naechster else (naechster, spots[i + 1])
    return (lo + hi) / 2.0


def snappe_auf_mittellinie(
    platzierungen: list[Platzierung],
    raum: RaumModell,
    bestand_leuchten_mm: tuple[tuple[float, float], ...] = (),
) -> list[Platzierung]:
    korridore = [
        r for r in raum.raeume
        if (r.raum_typ or "").upper() in _KORRIDOR_TYPEN and len(r.polygon_mm) >= 3
    ]
    achsen = {r.id: (*_korridor_achse(r.polygon_mm), ()) for r in korridore}
    if bestand_leuchten_mm:
        for r in korridore:
            achse, mitte, _ = achsen[r.id]
            if achse is None:
                continue
            bm, laengs = _bestand_mitte(achse, r.polygon_mm, bestand_leuchten_mm)
            if bm is not None:
                achsen[r.id] = (achse, bm, laengs)   # R1: Bestandslinie schlägt Bbox-Mitte
    if not any(a for a, _, _ in achsen.values()):
        return platzierungen
    out: list[Platzierung] = []
    for p in platzierungen:
        if p.kind not in _KINDS or p.norm_quelle == QUELLE_TUERLEUCHTE:
            out.append(p)
            continue
        korr = next((r for r in korridore if point_in_polygon(p.xy_mm, r.polygon_mm)), None)
        achse, mitte, laengs_spots = achsen[korr.id] if korr else (None, 0.0, ())
        if achse is None:
            out.append(p)
            continue
        x, y = p.xy_mm
        if achse == "y":
            neu = (_laengs_ausweichen(x, laengs_spots), mitte)   # R6 längs · R1 quer
        else:
            neu = (mitte, _laengs_ausweichen(y, laengs_spots))
        if (neu[0] - x) ** 2 + (neu[1] - y) ** 2 <= _MIN_SNAP_MM ** 2:
            out.append(p)
        else:
            out.append(p.model_copy(update={"xy_mm": neu}))
    return out
