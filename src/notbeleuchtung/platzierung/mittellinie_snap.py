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
"""
from __future__ import annotations

from notbeleuchtung.hauptengine.contracts import Platzierung, RaumModell

from .bausteine import KORRIDOR_TYPEN as _KORRIDOR_TYPEN
from .fachpraxis import QUELLE_TUERLEUCHTE
from .geometry import _bbox, point_in_polygon

_KINDS = ("rz", "sicherheitsleuchte", "antipanik")
_LAENGS_FAKTOR = 2.0   # Arm gilt erst als „gerader Korridor", wenn lang >= 2× kurz
_MIN_SNAP_MM = 20.0    # kleinere Verschiebung = schon zentriert, unverändert lassen


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


def snappe_auf_mittellinie(platzierungen: list[Platzierung], raum: RaumModell) -> list[Platzierung]:
    korridore = [
        r for r in raum.raeume
        if (r.raum_typ or "").upper() in _KORRIDOR_TYPEN and len(r.polygon_mm) >= 3
    ]
    achsen = {r.id: _korridor_achse(r.polygon_mm) for r in korridore}
    if not any(a for a, _ in achsen.values()):
        return platzierungen
    out: list[Platzierung] = []
    for p in platzierungen:
        if p.kind not in _KINDS or p.norm_quelle == QUELLE_TUERLEUCHTE:
            out.append(p)
            continue
        korr = next((r for r in korridore if point_in_polygon(p.xy_mm, r.polygon_mm)), None)
        achse, mitte = achsen[korr.id] if korr else (None, 0.0)
        if achse is None:
            out.append(p)
            continue
        x, y = p.xy_mm
        neu = (x, mitte) if achse == "y" else (mitte, y)
        if (neu[0] - x) ** 2 + (neu[1] - y) ** 2 <= _MIN_SNAP_MM ** 2:
            out.append(p)
        else:
            out.append(p.model_copy(update={"xy_mm": neu}))
    return out
