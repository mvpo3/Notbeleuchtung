"""deckungs_zuordnung — geometrische Fluchtweg-Deckung: welches RZ deckt welches Segment.

Die modernen RZ-Strategien (Anker/Gang/Sichtlinie) setzen absichtlich **nicht** 1 RZ je
Fluchtweg-Segment (das überproduziert auf realen Wegenetzen), tragen darum kein
`covers_segment` ein — auf echten Plänen blieb das Feld leer und die Deckungs-Prüfung
(`validierung` Regel 3) meldete alle Segmente als ungedeckt, obwohl RZ auf den Gängen
liegen.

Diese Schicht ordnet **nachträglich** zu: ein Fluchtweg-Segment gilt als gedeckt, wenn
ein Rettungszeichen innerhalb der Norm-Erkennungsweite (l = z·h) an seiner Polylinie
liegt (EN 1838 §4.1.1). Jedes Segment wird dem **nächstliegenden** RZ in Reichweite
zugeordnet; Segmente ohne RZ in Reichweite bleiben ungedeckt (echte Norm-Lücke, die die
Prüfung zurecht meldet).

**Grenze (bewusst konservativ, kein Freibrief):** gemessen wird der **euklidische**
Abstand (Luftlinie) RZ→Segment, **ohne** Sichtlinien-/Wand-Prüfung — ein RZ kann so ein
Segment „decken", das in Reichweite, aber hinter einer Wand/um eine Ecke liegt (real
nicht sichtbar). Eine echte Line-of-Sight-Prüfung braucht Wandgeometrie bzw. Kopplung an
die Weglänge im Zirkulationsgraph (Follow-up, siehe docs/DOD_SICHTPRUEFUNG.md). Die
Erkennungsweite ist außerdem von der Beleuchtungsart abhängig (`hinterleuchtet`:
z=200 → 30 m; beleuchtet: z=100 → 15 m); Default `hinterleuchtet=True`, weil die
gesetzten RZ hinterleuchtete Rettungszeichenleuchten (`notlicht_ks…`) sind.

Render-frei, kein Contract berührt: füllt nur das schon vorhandene Feld `covers_segment`
und erfüllt damit die Naht-Invariante `covers_segment ⊆ RaumModell.segmente`.
"""
from __future__ import annotations

import math
from itertools import pairwise

from notbeleuchtung.hauptengine.contracts import NormProvider, Platzierung, RaumModell

# Deckungs-Radius, wenn die Norm keine Erkennungsweite liefert (defensiver Default,
# entspricht dem RZ-Abstands-Default der Gang-Strategie).
_DEFAULT_RADIUS_MM = 15000.0
# Piktogramm-Annahme für die Erkennungsweite l = z·h (hinterleuchtet, 0,15 m Pikto).
_PIKTO_HOEHE_M = 0.15


def _dist_punkt_strecke(px: float, py: float, ax: float, ay: float, bx: float, by: float) -> float:
    """Abstand Punkt (px,py) zur Strecke A(ax,ay)–B(bx,by)."""
    dx, dy = bx - ax, by - ay
    laenge_q = dx * dx + dy * dy
    if laenge_q == 0.0:
        return math.hypot(px - ax, py - ay)
    t = ((px - ax) * dx + (py - ay) * dy) / laenge_q
    t = max(0.0, min(1.0, t))
    return math.hypot(px - (ax + t * dx), py - (ay + t * dy))


def _dist_punkt_polyline(p: tuple[float, float], poly: list) -> float:
    """Minimaler Abstand von Punkt p zur Polylinie (Punkt-Sonderfall: Punktabstand)."""
    if not poly:
        return math.inf
    if len(poly) == 1:
        return math.hypot(p[0] - poly[0][0], p[1] - poly[0][1])
    return min(
        _dist_punkt_strecke(p[0], p[1], a[0], a[1], b[0], b[1])
        for a, b in pairwise(poly)
    )


def _radius_mm(norm: NormProvider, hinterleuchtet: bool) -> float:
    """Deckungs-Radius = Norm-Erkennungsweite (l = z·h) in mm; sonst Default."""
    weite_m = norm.erkennungsweite_m(_PIKTO_HOEHE_M, hinterleuchtet)
    return weite_m * 1000.0 if weite_m and weite_m > 0 else _DEFAULT_RADIUS_MM


def zuordnen(
    placements: list[Platzierung], raum: RaumModell, norm: NormProvider,
    *, hinterleuchtet: bool = True,
) -> list[Platzierung]:
    """Füllt `covers_segment` der RZ geometrisch: jedes Segment → nächstes RZ in Reichweite.

    `hinterleuchtet` wählt die Erkennungsweite (True=z·h mit z=200 → 30 m für
    hinterleuchtete RZ-Leuchten; False=z=100 → 15 m). Gibt eine neue Liste zurück (RZ mit
    gesetztem `covers_segment`, Rest unverändert); mutiert die Eingabe nicht."""
    segmente = raum.zirkulation.segmente
    rz_idx = [i for i, p in enumerate(placements) if p.kind == "rz"]
    if not segmente or not rz_idx:
        return placements

    radius = _radius_mm(norm, hinterleuchtet)
    deckung: dict[int, list[str]] = {i: [] for i in rz_idx}
    for seg in segmente:
        beste_i, bester_d = None, radius
        for i in rz_idx:
            d = _dist_punkt_polyline(placements[i].xy_mm, seg.polyline_mm)
            if d <= bester_d:
                beste_i, bester_d = i, d
        if beste_i is not None:
            deckung[beste_i].append(seg.segment_id)

    out = list(placements)
    for i, seg_ids in deckung.items():
        if seg_ids:
            out[i] = placements[i].model_copy(update={"covers_segment": seg_ids})
    return out
