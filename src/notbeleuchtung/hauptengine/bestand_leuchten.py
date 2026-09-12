"""bestand_leuchten — Allgemeinbeleuchtung aus der Architektur-Unterlage extrahieren.

Punkt 3 der Owner-Reihe (2026-09-12): die R1-Lichtlinien-Regel („Notleuchten immer
in einer Linie mit der Beleuchtung", 3× Owner-korrigiert) und R6 (Spot-Lückenmitte)
brauchen die Positionen der BESTANDS-Leuchten. Bisher lieferte die nur der
Elektroplan-Runner von Hand — dieses Modul macht sie zum Pipeline-Standard:
`pipeline._run_mit_quelle` extrahiert automatisch aus dem Quell-DXF und reicht
`bestand_leuchten_mm` an `place()` durch. Referenz-Beleg Am Rain OG1: Bestands-
raster 2,5 m, din-Notleuchten 22 mm neben der Reihe (AM_RAIN-Digest §3).

Fail-open: kein bekanntes Leuchten-Vokabular im Plan / keine plausible Skala →
leeres Tuple, `mittellinie_snap` fällt auf die Bbox-Gangmitte zurück (heutiges
Verhalten). Reine Positionsverfeinerung — Symbolzahlen ändern sich nicht.

Skala: statt einer eigenen Einheiten-Heuristik wird der mm-Faktor GEGEN das
RaumModell kalibriert (bounds sind die Wahrheit der Erkennung): gewählt wird der
Kandidat, der die meisten Roh-Punkte in die Geschoss-Bounds legt — das filtert
zugleich Phantom-Koordinaten (Extents-Ausreißer-Klasse, 34-km-Inseln).
"""
from __future__ import annotations

from pathlib import Path

import ezdxf

from notbeleuchtung.hauptengine.contracts import RaumModell

#: Blocknamen-Vokabular der Allgemeinbeleuchtung (lowercase, exakt) — wächst wie
#: das Tür-Vokabular je CAD-Dialekt. Elektroplan-DE-Dialekt: spots/deckenauslass/
#: wandlichtauslass. BEWUSST eng (fail-open schlägt fail-wrong).
BESTAND_BLOCKNAMEN = {
    "spots", "spot", "deckenauslass", "wandlichtauslass", "deckenleuchte",
    "downlight", "langfeldleuchte", "anbauleuchte",
}

#: Skala-Kandidaten Quell-Einheit → mm (wie der Unterlage-Importer #126).
_FAKTOREN = (1.0, 10.0, 25.4, 1000.0)
#: Toleranzrand um die Geschoss-Bounds (Leuchten am Blattrand).
_RAND_MM = 2000.0
#: Mindestanteil der Roh-Punkte, den der Sieger-Faktor in die Bounds legen muss —
#: darunter ist die Kalibrierung Zufall und die Extraktion bleibt leer (fail-open).
_MIN_TREFFERQUOTE = 0.5


def _roh_punkte(dxf_pfad: str | Path) -> list[tuple[float, float]]:
    doc = ezdxf.readfile(str(dxf_pfad))
    return [
        (float(e.dxf.insert.x), float(e.dxf.insert.y))
        for e in doc.modelspace().query("INSERT")
        if e.dxf.name.lower().strip() in BESTAND_BLOCKNAMEN
    ]


def extrahiere_fuer(raum: RaumModell, dxf_pfad: str | Path) -> tuple[tuple[float, float], ...]:
    """Bestands-Leuchten in mm im RaumModell-Rahmen — oder () (fail-open)."""
    try:
        roh = _roh_punkte(dxf_pfad)
    except (OSError, ezdxf.DXFError):
        return ()
    if not roh:
        return ()
    (min_x, min_y), (max_x, max_y) = raum.bounds_mm.min_xy, raum.bounds_mm.max_xy
    lo_x, lo_y = min_x - _RAND_MM, min_y - _RAND_MM
    hi_x, hi_y = max_x + _RAND_MM, max_y + _RAND_MM

    def _drin(f: float) -> list[tuple[float, float]]:
        return [(x * f, y * f) for x, y in roh
                if lo_x <= x * f <= hi_x and lo_y <= y * f <= hi_y]

    def _spannweite(pts) -> float:
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        return (max(xs) - min(xs)) + (max(ys) - min(ys)) if pts else 0.0

    # Sieger = meiste Punkte in den Bounds; bei Gleichstand die größte Spannweite —
    # Leuchten verteilen sich über das Geschoss, eine Meter-Quelle passt sonst auch
    # „als mm" in die Bounds (8-mm-Häufchen in der Ecke).
    beste: list[tuple[float, float]] = []
    for f in _FAKTOREN:
        drin = _drin(f)
        if (len(drin), _spannweite(drin)) > (len(beste), _spannweite(beste)):
            beste = drin
    if len(beste) < max(2, int(len(roh) * _MIN_TREFFERQUOTE)):
        return ()                    # keine plausible Skala/alles Ausreißer
    return tuple(beste)
