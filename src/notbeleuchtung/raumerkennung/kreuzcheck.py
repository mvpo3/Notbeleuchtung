"""kreuzcheck — explizite Fluchtweglinien gegen die final_exit-Menge prüfen.

Beide Richtungen:

1. Jede explizite Fluchtweglinie (quelle LINIE), deren Endpunkt AN der
   Außenkante liegt (≤ 1.5 m zur Kante der gedeckten Kontur — Außenweg-Kanten
   weit weg vom Gebäude zählen NICHT), braucht einen final_exit in 1.5 m.
   Fehlt er → Warnung + nächste Öffnung in der Außenwand als
   ``notausgang_kandidat`` (eigene Liste — Prüfstrecken-Output, KEIN Ausgang
   im Contract; Darstellung gestrichelt rot in 05_fluchtweg.png).
2. Jeder final_exit ohne endende Linie/GRAPH-Weg in 1.5 m → ``unbenutzt``
   (Berichts-Feld — der Ausgang existiert, aber kein Weg führt hin).
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

from shapely.geometry import Point

from notbeleuchtung.hauptengine.contracts.raum_modell import RaumModell

from .tuer_zuordnung import AUSSEN

XY = tuple[float, float]

_KANTE_NAH_MM = 1500.0     # Linien-Endpunkt „an der Außenkante"
_SNAP_MM = 100.0           # Netz-Snapping für die Grad-1-Endpunktbestimmung
_EXIT_NAH_MM = 1500.0      # final_exit „deckt" einen Endpunkt
_KANDIDAT_SUCH_MM = 3000.0  # Suchradius für die nächste Öffnung in der Außenwand
_KONTUR_INNEN_TOL_MM = 1.0  # bis hierhin gilt ein Punkt noch als AUF der Kontur-Grenze


@dataclass
class NotausgangKandidat:
    """Kandidat für einen fehlenden Endausgang — Prüf-Output, kein Ausgang."""

    xy_mm: XY
    typ: str = "notausgang_kandidat"
    tuer_id: str | None = None      # nächste Öffnung, falls gefunden
    grund: str = ""


@dataclass
class KreuzcheckErgebnis:
    endpunkte_aussenkante: list[XY] = field(default_factory=list)
    gedeckte_endpunkte: list[XY] = field(default_factory=list)
    warnungen: list[str] = field(default_factory=list)
    kandidaten: list[NotausgangKandidat] = field(default_factory=list)
    unbenutzte_exits: list[str] = field(default_factory=list)


def _snap(p: XY) -> tuple[int, int]:
    return (round(p[0] / _SNAP_MM), round(p[1] / _SNAP_MM))


def kreuzcheck(modell: RaumModell, kontur, kante=None) -> KreuzcheckErgebnis:
    """Fluchtweglinien ↔ final_exit-Kreuzprüfung (s. Modul-Docstring).

    ``kante`` = GEBÄUDE-Außenkante (Linien-Geometrie). Ohne sie fällt die
    Prüfung auf ``kontur.boundary`` zurück — die enthält aber auch die
    Ränder der ausgeschnittenen AUSSEN-Flächen (Hof-Wege!), wodurch
    Außenweg-Endpunkte mitten im Gelände fälschlich zählen würden.
    """
    erg = KreuzcheckErgebnis()
    if kontur is None or kontur.is_empty:
        return erg
    if kante is None:
        kante = kontur.boundary
    finals = [a for a in modell.ausgaenge if a.typ == "final_exit"]

    # ── 1. Linien-Endpunkte an der Außenkante brauchen einen final_exit ──
    # Nur ECHTE Weg-Enden (Grad 1 im gesnappten Linien-Netz): wo Segmente
    # aneinanderstoßen oder eine Linie weiterläuft, endet kein Fluchtweg.
    grad: dict[XY, int] = {}
    linien = [s for s in modell.zirkulation.segmente
              if s.quelle == "LINIE" and len(s.polyline_mm) >= 2]
    for s in linien:
        for p in s.polyline_mm:
            grad[_snap(p)] = grad.get(_snap(p), 0) + 1
    for s in linien:
        for p in (s.polyline_mm[0], s.polyline_mm[-1]):
            if grad.get(_snap(p), 0) != 1:
                continue
            # „an/außerhalb der Außenkante": der Endpunkt liegt im AUSSEN-
            # Bereich (nicht gedeckt) UND ≤ 1.5 m an der Gebäudekante —
            # Gang-Enden im Gebäudeinneren nahe der Fassade zählen nicht.
            # covers() schließt Randpunkte EIN — ein Endpunkt exakt AUF der
            # Außenkante würde damit verworfen, obwohl die Spec ihn zählt
            # („endet AN oder AUSSERHALB der Außenkante"). Deshalb nur ECHT
            # innenliegende Punkte verwerfen (> Toleranz von der Grenze weg).
            punkt = Point(p)
            innen = (kontur.covers(punkt)
                     and kontur.boundary.distance(punkt) > _KONTUR_INNEN_TOL_MM)
            if innen or kante.distance(punkt) > _KANTE_NAH_MM:
                continue
            erg.endpunkte_aussenkante.append(p)
            if any(math.dist(p, a.xy_mm) <= _EXIT_NAH_MM for a in finals):
                erg.gedeckte_endpunkte.append(p)
                continue
            erg.warnungen.append(
                f"Fluchtweglinie {s.segment_id} endet ohne Endausgang bei "
                f"({p[0]:.0f}, {p[1]:.0f})")
            erg.kandidaten.append(_kandidat(p, modell))

    # ── 2. final_exit ohne endende Linie/GRAPH-Weg → unbenutzt ──
    weg_enden = [pl[-1] for s in modell.zirkulation.segmente
                 if s.quelle in ("LINIE", "GRAPH") and (pl := s.polyline_mm)]
    weg_enden += [pl[0] for s in modell.zirkulation.segmente
                  if s.quelle == "LINIE" and (pl := s.polyline_mm)]
    for a in finals:
        if not any(math.dist(a.xy_mm, p) <= _EXIT_NAH_MM for p in weg_enden):
            erg.unbenutzte_exits.append(a.id)
    return erg


def _kandidat(p: XY, modell: RaumModell) -> NotausgangKandidat:
    """Nächste Öffnung in der Außenwand (Tür mit AUSSEN-Seite) ≤ 3 m."""
    aussen_tueren = [t for t in modell.tueren
                    if AUSSEN in (t.von_raum, t.nach_raum)]
    best = min(aussen_tueren, key=lambda t: math.dist(t.xy_mm, p), default=None)
    if best is not None and math.dist(best.xy_mm, p) <= _KANDIDAT_SUCH_MM:
        return NotausgangKandidat(
            xy_mm=best.xy_mm, tuer_id=best.id,
            grund=f"nächste Öffnung in der Außenwand ({best.quelle or '?'})")
    return NotausgangKandidat(
        xy_mm=p, grund="keine Öffnung in der Außenwand ≤ 3 m gefunden")
