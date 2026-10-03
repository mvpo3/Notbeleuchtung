"""schacht_abgleich — Schachtlagen über die Geschosse eines Projekts abgleichen.

Owner-Regel b, Slice K2 (2026-09-29), wörtlich: „Schächte laufen senkrecht
durchs Gebäude. Nach der Erkennung je Geschoss die Schachtpositionen über alle
Geschosse desselben Projekts abgleichen (gleiche Lage in CAD-mm, Toleranz
300 mm). Ein Schacht, der in mindestens zwei Nachbargeschossen belegt ist, wird
im dazwischenliegenden Geschoss an derselben Stelle gesucht; fehlt er, als
Warnung ‚Schacht erwartet, nicht gefunden' mit Position melden, nicht erfinden."

Planer-Lesart „dazwischenliegend": ist eine Lage in Geschoss i und j (i < j)
belegt, wird jedes Geschoss strikt dazwischen gesucht. Reine Funktion über die
Räume mehrerer Geschosse — sie erzeugt und ändert keinen Raum.

Lage = Schwerpunkt des SCHACHT-Polygons; die erste Fundstelle (von unten) ist
der Anker der Lage. NISCHE und LIFT zählen nicht.
"""
from __future__ import annotations

import re
from collections.abc import Sequence
from dataclasses import dataclass, field

from shapely.geometry import Point, Polygon

from notbeleuchtung.hauptengine.contracts.raum_modell import Raum

XY = tuple[float, float]

TOLERANZ_MM = 300.0
WARNUNG = "Schacht erwartet, nicht gefunden"

_GESCHOSS_RX = re.compile(r"^(\d*)(EG|OG|UG|KG|DG)$")
_DG_NUMMER_RX = re.compile(r"(?<![A-Z0-9])DG\s?(\d)")


def geschoss_rang(geschoss: str, name: str = "") -> int | None:
    """Höhenrang eines kanonischen Geschosses (``geschoss.py``), unten → oben.

    ``2KG`` < ``1KG``/``UG`` < ``EG`` < ``1OG`` … < ``DG``. Mehrere
    Dachgeschosse liefert ``geschoss_befund`` alle als ``DG`` (das Kürzel-Muster
    fasst ``DG1``/``DG2`` ohne Ziffer); ihre Reihenfolge trägt nur der
    Dateiname, deshalb ``name``: ``DG<n>`` → Rang 100 + n, sonst 101.
    ``None`` = Geschoss unbekannt (nimmt am Abgleich nicht teil).
    """
    m = _GESCHOSS_RX.match((geschoss or "").strip().upper())
    if not m:
        return None
    n, art = int(m.group(1) or 1), m.group(2)
    if art == "EG":
        return 0
    if art in ("UG", "KG"):
        return -n
    if art == "OG":
        return n
    d = _DG_NUMMER_RX.search(name.upper())
    return 100 + (int(d.group(1)) if d else 1)


@dataclass
class Schachtlage:
    """Eine senkrechte Schachtlage: Anker, belegte Geschosse, Lücken-Warnungen."""

    xy: XY
    belegt: dict[str, str] = field(default_factory=dict)     # Geschoss → Raum-ID
    warnungen: list[str] = field(default_factory=list)


def gleiche_schaechte_ab(geschosse: Sequence[tuple[str, Sequence[Raum]]],
                         toleranz_mm: float = TOLERANZ_MM) -> list[Schachtlage]:
    """SCHACHT-Lagen über ``geschosse`` = ``(Name, Räume)`` von unten nach oben.

    Je Lage die belegten Geschosse; fehlt der Schacht in einem Geschoss
    zwischen zwei belegten, eine Warnung mit Position und dem Raum, der dort
    liegt. Es entsteht kein Raum, kein Typ ändert sich.
    """
    # ponytail: gieriger Anker (erste Fundstelle); Cluster-Mittel erst, wenn
    # eine Lage über mehr als die Toleranz wandert.
    anker: list[tuple[Point, dict[int, str]]] = []
    for i, (_name, raeume) in enumerate(geschosse):
        for r in raeume:
            if r.raum_typ != "SCHACHT" or len(r.polygon_mm) < 3:
                continue
            c = Polygon(r.polygon_mm).centroid
            lage = next((a for a in anker if a[0].distance(c) <= toleranz_mm), None)
            if lage is None:
                anker.append((c, {i: r.id}))
            else:
                lage[1].setdefault(i, r.id)
    out: list[Schachtlage] = []
    for c, belegt in anker:
        namen = [geschosse[i][0] for i in sorted(belegt)]
        lage = Schachtlage(xy=(round(c.x), round(c.y)),
                           belegt={geschosse[i][0]: belegt[i] for i in sorted(belegt)})
        for k in range(min(belegt) + 1, max(belegt)):
            if k in belegt:
                continue
            name, raeume = geschosse[k]
            dort = next((f"{r.raum_typ or 'untypisiert'} {r.id}" for r in raeume
                         if len(r.polygon_mm) >= 3
                         and Polygon(r.polygon_mm).buffer(0).covers(c)), "kein Raum")
            lage.warnungen.append(
                f"{WARNUNG}: {name} bei ({c.x:.0f}, {c.y:.0f}) — belegt in "
                f"{', '.join(namen)}; an der Stelle: {dort}")
        out.append(lage)
    return out
