"""sichtkette — Gang-RZ auf die lückenlose SICHTKETTE ausdünnen (R-F).

Owner-Fachdoku „Notbeleuchtung zeichnen lernen" v2 (S.7–9), AUTORITATIV:
Rettungszeichen werden nicht nach festem Abstand gesetzt, sondern so, dass eine
lückenlose Sichtkette entsteht — von jedem Punkt des Fluchtwegs ist ≥1 RZ
sichtbar, von jedem RZ das nächste. **Ist das nächste Zeichen bereits sichtbar,
wird kein weiteres gesetzt** (Sichtbarkeit ersetzt Zeichen; Ground truth
Elektroplan DE EG: Gang-RZ 4 → 1). [AT-verbindlich: ÖNORM EN 1838 §4.1.1]

Dieses Modul ENTFERNT nur (Nachpass über die fertige RZ-Liste) — es erfindet
keine Positionen. Geschützt (nie entfernt):
* Exit-RZ (≤ `_SCHUTZ_RADIUS_MM` an einem Ausgang, EN 1838 §4.1.2 g),
* Kreuzungs-RZ (≤ `_SCHUTZ_RADIUS_MM` an einem Graph-Knoten mit degree ≥ 3,
  §4.1.2 f),
* Tür-RZ (Praxis-Quellen `Referenz-Praxis:`/`fachpraxis:` — R-B/R-C-Leuchten),
* RZ außerhalb der Korridor-Polygone (Sonderstellen, Stiegenhaus-Nachpass).

Sichtbarkeit = Luftlinie ≤ Erkennungsweite (l = z·h aus `NormProvider`, kein
eigener Wert) UND der Sichtstrahl bleibt in der Korridor-Fläche (Sampling gegen
die GANG-Polygone — an konkaven Ecken/L-Gängen verlässt der Strahl die Fläche,
die Kette „reißt", das RZ bleibt). Glastüren/Trennelemente stehen nicht im
RaumModell — sobald die Erkennung sie liefert, gehören sie hier als
Sichtbarriere dazu (R-F, Owner: „JA sie zählt").
"""
from __future__ import annotations

import math

from notbeleuchtung.hauptengine.contracts import NormProvider, Platzierung, RaumModell

from .bausteine import KORRIDOR_TYPEN as _KORRIDOR_TYPEN
from .geometry import point_in_polygon
from .graph import build_circulation_graph

#: RZ näher als das an einem Ausgang/Kreuzungs-Knoten = Pflicht-RZ, geschützt.
_SCHUTZ_RADIUS_MM = 2000.0
#: Piktogramm-Default (0,15 m, hinterleuchtet) — gleiche Annahme wie die übrigen
#: l=z·h-Konsumenten (gang_strategy._abstand_mm, platzierer._arm_gap_mm).
_PIKTO_HOEHE_M = 0.15
#: Sichtstrahl-Sampling: Prüfpunkte je Strahl; Ränder ausgespart (Tür-XY liegt AUF
#: der Wand — der Startpunkt selbst darf knapp außerhalb des Polygons liegen).
_SAMPLES = 12
_RAND_ANTEIL = 0.08


def _sicht_frei(
    a: tuple[float, float], b: tuple[float, float],
    polys: list[list[tuple[float, float]]], weite_mm: float,
) -> bool:
    if math.hypot(b[0] - a[0], b[1] - a[1]) > weite_mm:
        return False
    for i in range(_SAMPLES):
        t = _RAND_ANTEIL + (1.0 - 2.0 * _RAND_ANTEIL) * i / (_SAMPLES - 1)
        p = (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
        if not any(point_in_polygon(p, poly) for poly in polys):
            return False
    return True


def kette_ausduennen(
    platzierungen: list[Platzierung], raum: RaumModell, norm: NormProvider
) -> list[Platzierung]:
    """Redundante Gang-RZ entfernen, solange die Sichtkette geschlossen bleibt.

    Invariante nach jedem Entfernen: (1) jeder Einzugspunkt (Tür in einen
    Korridor, Ausgang) sieht ≥1 verbleibendes RZ; (2) jedes verbleibende
    Korridor-RZ sieht ≥1 weiteres RZ oder einen Ausgang (Kette führt weiter).
    Kann eine Entfernung die Invariante nicht halten, bleibt das RZ — fail-safe
    Richtung „mehr Zeichen"."""
    korridore = [
        r for r in raum.raeume
        if (r.raum_typ or "").upper() in _KORRIDOR_TYPEN and len(r.polygon_mm) >= 3
    ]
    if not korridore:
        return platzierungen
    polys = [r.polygon_mm for r in korridore]
    korridor_ids = {r.id for r in korridore}
    try:
        weite_mm = float(norm.erkennungsweite_m(_PIKTO_HOEHE_M, True)) * 1000.0
    except (AttributeError, TypeError, ValueError):
        return platzierungen                     # ohne Norm-Weite keine Ausdünnung
    if weite_mm <= 0.0:
        return platzierungen

    rz = [p for p in platzierungen if p.kind == "rz"]
    rest = [p for p in platzierungen if p.kind != "rz"]

    G = build_circulation_graph(raum)
    knoten_pos = {n.id: n.xy_mm for n in raum.zirkulation.nodes}
    kreuzungen = [knoten_pos[n] for n in G.nodes if n in knoten_pos and G.degree(n) >= 3]
    ausgaenge = [a.xy_mm for a in raum.ausgaenge]

    def _nah(xy, punkte) -> bool:
        return any(math.hypot(xy[0] - p[0], xy[1] - p[1]) <= _SCHUTZ_RADIUS_MM for p in punkte)

    def _geschuetzt(p: Platzierung) -> bool:
        if p.norm_quelle.startswith(("Referenz-Praxis:", "fachpraxis:")):
            return True                                    # Tür-RZ (R-B/R-C)
        if not any(point_in_polygon(p.xy_mm, poly) for poly in polys):
            return True                                    # kein Gang-RZ → nicht unsere Lane
        return _nah(p.xy_mm, ausgaenge) or _nah(p.xy_mm, kreuzungen)

    fest = [p for p in rz if _geschuetzt(p)]
    kandidaten = [p for p in rz if not _geschuetzt(p)]
    if not kandidaten:
        return platzierungen

    # Einzugspunkte = „jeder Punkt des Fluchtwegs" (§4.1.1): Türen in Korridore,
    # Ausgänge UND ein Sampling entlang der Fluchtweg-Segmente — sonst gälte ein
    # Gang-Arm ohne modellierte Türen fälschlich als gedeckt.
    einzug = [t.xy_mm for t in raum.tueren
              if t.von_raum in korridor_ids or t.nach_raum in korridor_ids]
    einzug += ausgaenge
    schritt = max(weite_mm / 5.0, 1000.0)
    for seg in raum.zirkulation.segmente:
        pts = seg.polyline_mm
        for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
            laenge = math.hypot(x2 - x1, y2 - y1)
            n = max(int(laenge / schritt), 1)
            # nur Punkte IN der Korridor-Fläche — ein Segment-Stück außerhalb
            # (Tür-Durchtritt, fremder Raum) kann nie ein RZ „sehen" und würde
            # die Ausdünnung sonst komplett blockieren.
            einzug += [
                p for i in range(n + 1)
                for p in [(x1 + (x2 - x1) * i / n, y1 + (y2 - y1) * i / n)]
                if any(point_in_polygon(p, poly) for poly in polys)
            ]

    def _kette_haelt(bleibend: list[Platzierung]) -> bool:
        punkte = [p.xy_mm for p in fest + bleibend]
        if einzug and not all(
            any(_sicht_frei(e, q, polys, weite_mm) for q in punkte) for e in einzug
        ):
            return False
        # Jedes Korridor-RZ führt weiter: sieht ein anderes RZ oder einen Ausgang.
        for q in punkte:
            weiter = [w for w in punkte if w != q] + ausgaenge
            if not any(_sicht_frei(q, w, polys, weite_mm) for w in weiter):
                return False
        return True

    # Redundanteste zuerst probieren (meiste Sicht-Nachbarn).
    def _redundanz(p: Platzierung) -> int:
        andere = [q.xy_mm for q in fest + kandidaten if q is not p]
        return sum(_sicht_frei(p.xy_mm, q, polys, weite_mm) for q in andere)

    bleibend = list(kandidaten)
    for p in sorted(kandidaten, key=_redundanz, reverse=True):
        probe = [q for q in bleibend if q is not p]
        if _kette_haelt(probe):
            bleibend = probe
    return rest + fest + bleibend
