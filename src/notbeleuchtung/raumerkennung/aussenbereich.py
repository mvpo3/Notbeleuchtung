"""aussenbereich — AUSSEN-Flächen erkennen (Hof, Garten, Wege ins Freie).

AUSSEN = freie Fläche innerhalb der konvexen Hülle des Gebäudes, die
(a) Außenanlagen enthält (GRÜN-/Platten-/Kies-Schraffuren, Baum-Blöcke,
    Grundstücksgrenze-Layer — Layer-Hinweise, keine Normwerte) ODER
(b) über eine Lücke in der Außenkante mit dem freien Außenraum verbunden ist.

Ein Hof OHNE Weg ins Freie ist ``AUSSEN_GESCHLOSSEN``: dort entsteht kein
final_exit (offene Frage an Enis, docs/OFFENE_FRAGEN.md) — seine Fläche zählt
für die Türzuordnung weiter als "gedeckt" (Türen dorthin werden nicht AUSSEN).

Die Außenkontur wird JE GEBÄUDE-KOMPONENTE gerechnet (Barawitzka = 2 Trakte
mit offenem Hof dazwischen — eine einzige Kontur verschluckt den Südtrakt).

Decken-Heuristik (Slab-Polygone) ist hier bewusst KEIN Ausschluss: auf Rennweg
EG enthält die Slab-Union den Türschließer-Eingang (Beleg docs/OFFENE_FRAGEN.md)
— Slabs taugen nur als Positiv-Hinweis, wo sie verlässlich sind.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from shapely.geometry import MultiPolygon, Point, Polygon
from shapely.ops import unary_union

from .dxf_load import DxfPlan
from .wandkoerper import Wandkoerper

XY = tuple[float, float]

# Layer-Hinweise auf Außenanlagen (tolerant gegen cp-dekodierte Umlaute:
# 'GRÜN' → 'GR.N'). BELAG bewusst NICHT: Belagsflächen gibt es auch innen.
_AUSSEN_LAYER = re.compile(
    r"GR.N|KIES|GARTEN|RASEN|PLATTE|BAUM|B.UME|GRUNDST|GRENZE", re.IGNORECASE)
# Baum-/Bepflanzungs-Blöcke.
_BAUM_BLOCK = re.compile(r"BAUM|TREE|STRAUCH", re.IGNORECASE)

# Morphologisches Schließen der Wand-Union. BEWUSST größer als aussenkontur
# (600): auch Doppelflügel-Hauseingänge (~1.9 m) müssen versiegelt werden,
# sonst „leckt" der Erschließungsgang durch die Eingangsöffnung in den
# Außenraum und würde als AUSSEN klassifiziert. Tore > 2.4 m (Garagen-/
# Hof-Durchfahrten) bleiben offen — gewollt: dort ist ein Weg ins Freie.
_SCHLIESS_MM = 1200.0
_MIN_HOF_M2 = 5.0        # kleinere freie Flächen sind Nischen, keine Höfe
_RAND_EPS_MM = 250.0     # "berührt die konvexe Hülle" -Toleranz


@dataclass
class AussenBereiche:
    """Ergebnis der Außen-Analyse (Vektor-Geometrie in mm)."""

    komponenten: list[Polygon] = field(default_factory=list)   # Kontur je Trakt
    offen: list[Polygon] = field(default_factory=list)         # AUSSEN
    geschlossen: list[Polygon] = field(default_factory=list)   # AUSSEN_GESCHLOSSEN

    def gedeckt(self):
        """Fläche, die für die Türzuordnung als „nicht AUSSEN" gilt:
        alle Komponenten-Konturen minus der offenen Außenflächen, plus
        geschlossene Höfe (dort kein final_exit)."""
        u = unary_union([*self.komponenten, *self.geschlossen])
        if self.offen:
            u = u.difference(unary_union(self.offen))
        return u


def aussen_indizien(plan: DxfPlan) -> list[XY]:
    """Punkte mit Außenanlagen-Indiz: Schwerpunkte von Hatches/Linien auf
    Außen-Layern + Baum-Block-Positionen (mm)."""
    out: list[XY] = []
    for e in plan.entities():
        t = e.dxftype()
        layer = str(e.dxf.layer)
        if t == "INSERT" and _BAUM_BLOCK.search(str(e.dxf.name)):
            out.append(plan._scale(e.dxf.insert))
        elif _AUSSEN_LAYER.search(layer):
            if t == "HATCH":
                try:
                    seeds = list(e.seeds) or None
                except Exception:  # noqa: BLE001 — kaputter Hatch liefert keinen Seed
                    seeds = None
                if seeds:
                    out.append(plan._scale(seeds[0]))
                else:
                    pts = plan.entity_points(e)
                    if pts:
                        out.append(pts[0])
            else:
                pts = plan.entity_points(e)
                if pts:
                    out.extend(pts[:2])
    return out


def aussenkontur_komponenten(koerper: list[Wandkoerper],
                             d_mm: float = _SCHLIESS_MM) -> list[Polygon]:
    """Außenkontur JE zusammenhängender Gebäude-Komponente (Löcher gefüllt).

    Union der Wandkörper, morphologisch geschlossen (überbrückt Tür-/Fenster-
    öffnungen ≤ 2·d) — jede verbleibende Komponente ist ein Trakt.
    """
    if not koerper:
        return []
    u = unary_union([Polygon(k.polygon_mm).buffer(0) for k in koerper])
    u = u.buffer(d_mm).buffer(-d_mm)
    geoms = list(u.geoms) if isinstance(u, MultiPolygon) else [u]
    return [Polygon(g.exterior) for g in geoms
            if g.geom_type == "Polygon" and g.area >= 1e6]  # ≥1 m²


def erkenne_aussenbereiche(plan: DxfPlan,
                           koerper: list[Wandkoerper]) -> AussenBereiche:
    """Außen-Analyse: Komponenten-Konturen + offene/geschlossene Außenflächen."""
    komponenten = aussenkontur_komponenten(koerper)
    if not komponenten:
        return AussenBereiche()
    # Geschlossene Wand-Union MIT Löchern — Höfe/Innenräume bleiben Löcher.
    wand_zu = unary_union(
        [Polygon(k.polygon_mm).buffer(0) for k in koerper]
    ).buffer(_SCHLIESS_MM).buffer(-_SCHLIESS_MM)
    huelle = unary_union(komponenten).convex_hull
    # Freie Fläche = Hülle minus Wand-Geometrie (MIT Löchern): enthält den
    # Raum zwischen den Trakten, Höfe (Löcher) UND Innenräume — letztere
    # filtert die Indiz-/Rand-Pflicht unten heraus.
    frei = huelle.difference(wand_zu)
    teile = (list(frei.geoms) if hasattr(frei, "geoms")
             else ([frei] if not frei.is_empty else []))

    indizien = aussen_indizien(plan)
    rand = huelle.exterior
    offen: list[Polygon] = []
    geschlossen: list[Polygon] = []
    for t in teile:
        if t.area < _MIN_HOF_M2 * 1e6:
            continue
        hat_indiz = any(t.covers(Point(p)) for p in indizien)
        beruehrt_rand = t.distance(rand) < _RAND_EPS_MM
        if not (hat_indiz or beruehrt_rand):
            continue                      # Innenraum-Loch ohne Außen-Indiz
        # Weg ins Freie ⇔ die Fläche reicht bis an die konvexe Hülle; ein
        # eingeschlossenes Loch (nur ≤2.4-m-Lücken, vom Schließen versiegelt)
        # hat keinen Weg ins Freie → AUSSEN_GESCHLOSSEN.
        (offen if beruehrt_rand else geschlossen).append(t)
    return AussenBereiche(komponenten=komponenten, offen=offen,
                          geschlossen=geschlossen)
