"""OG3-Kennzahlen des Türstapel-Gates — die Zahlen hinter Bedingung (6).

``segmente_graph`` und ``anker_in_wohnung_privat`` sind wörtlich die beiden
Aussagen aus ``tests/naht/test_soll_rennweg.py``
(``test_soll_segmente_aus_graph``: mindestens ein Segment mit quelle ``GRAPH``;
``test_keine_anker_in_wohnung_privat``: kein Anker in einem Raum der
nutzungsklasse ``WOHNUNG_PRIVAT``). Die übrigen Zahlen stehen nur daneben,
damit ein Rückschritt sofort zu sehen ist — ein Urteil fällt hier nicht, das
macht ``gate_regel``.

``anker_in_wohnung_privat`` zählt mit ``Polygon.contains`` (Punkt echt innen)
und nur über Polygone mit ≥ 3 Stützpunkten — exakt wie der Test. Ein Anker
genau auf der Raumkante zählt damit NICHT mit.
"""
from __future__ import annotations

from collections import Counter

from shapely.geometry import Point, Polygon


def kennzahlen_og3(modell) -> dict:
    """Die neun OG3-Zahlen (Rennweg OG3) für Gate-Bedingung (6)."""
    privat = [Polygon(r.polygon_mm) for r in modell.raeume
              if r.nutzungsklasse == "WOHNUNG_PRIVAT" and len(r.polygon_mm) >= 3]
    je_wohnung = Counter(r.wohnung_id for r in modell.raeume if r.wohnung_id)
    segmente = modell.zirkulation.segmente
    return {
        "segmente_graph": sum(1 for s in segmente if s.quelle == "GRAPH"),
        "segmente_gesamt": len(segmente),
        "anker_gesamt": len(modell.anker),
        "anker_in_wohnung_privat": sum(
            1 for a in modell.anker
            if any(p.contains(Point(a.xy_mm)) for p in privat)),
        "wohnungen": len(je_wohnung),
        "einraum_wohnungen": sum(1 for n in je_wohnung.values() if n == 1),
        "tueren_gesamt": len(modell.tueren),
        "durchgaenge_ohne_tuerblatt": sum(1 for t in modell.tueren if t.ohne_tuerblatt),
        "raeume_wohnung_privat_gang": sum(
            1 for r in modell.raeume
            if r.raum_typ == "GANG" and r.nutzungsklasse == "WOHNUNG_PRIVAT"),
    }
