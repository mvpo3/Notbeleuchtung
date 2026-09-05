"""abstand_nachpass — finaler Entzerrungs-Pass gegen Symbol-Kollisionen an der Naht.

Der Platzierer verkettet mehrere render-freie Strategien (Anker/Segment/Gang für RZ,
`flaechen_strategy` für SL+Antipanik, `deckung` für die Korridor-Verdichtung). Jede
dedupliziert **nur intern** — die Anker-Strategie mergt nahe RZ über
`anker_strategy._MIN_RZ_MERGE_MM`, aber nur RZ↔RZ innerhalb ihres Pfads. Symbole aus
*verschiedenen* Strategien (ein Anker-RZ neben einer Flächen-SL; zwei SL aus
`flaechen_strategy` und `deckung`) prüft niemand gegeneinander — die Naht *kann* Symbol-
Paare unter dem Mindestabstand erzeugen, die `validierung` Regel 7 als Kollision meldet
(historisch beobachtet Mollgasse EG 2026-08-31, `docs/DOD_SICHTPRUEFUNG.md` Befund #5).

**Ehrlich:** auf dem aktuellen Stand reproduziert Befund #5 nicht mehr (zwischenzeitliche
Platzier-Arbeit hat ihn aufgelöst) — dieser Nachpass ist deshalb **kein Bugfix für einen
lebenden Defekt, sondern eine strukturelle Garantie** (Defense-in-depth): er macht die
Kollisionsfreiheit an der Strategie-Naht *invariant* statt zufällig. Auf Mollgasse EG
läuft er aktuell als No-op (nichts zu mergen/entzerren); der Mechanismus ist gegen
synthetische Koinzidenzen unit-getestet, das reale Ergebnis durch eine E2E-Schranke
festgehalten.

Er läuft in `place` nach `lb_override` (das selbst SL hinzufügt/entfernt) und **vor**
`deckungs_zuordnung` (damit die Deckung die finalen Positionen sieht):

* **Gleiche `kind` + Kollision** → **Merge** (das spätere Duplikat verwerfen). Zwei RZ am
  selben Punkt (Anker+Gang) oder zwei SL aus zwei Flächen-Pässen sind echte Dubletten.
* **Verschiedene `kind` + Kollision** → **Nudge** das niederrangige Symbol weg vom
  Nachbarn, bis der Mindestabstand erreicht ist, und halte es im Raumpolygon. Ein RZ und
  eine SL an derselben Stelle sind **beide** normrelevant — es wird nie eine benötigte
  Leuchte gelöscht.

Prioritäts-Rang: ``rz`` > ``sicherheitsleuchte`` > ``antipanik`` (das höherrangige bleibt
stehen). Deterministisch (stabile Rang-Sortierung), idempotent (ein zweiter Lauf ändert
nichts), Ausgabe in Original-Reihenfolge (NODEID-/Render-Zählung bleibt stabil).

Render-frei, importiert nur `hauptengine.contracts` + das eigene `geometry` (Owner-Grenze:
`platzierung` importiert kein Fremd-Package, insb. **nicht** `validierung`).
"""
from __future__ import annotations

import math

from notbeleuchtung.hauptengine.contracts import Platzierung, RaumModell

from .geometry import Point, Polygon, point_in_polygon

# Mindestabstand zwischen zwei Symbolen. BEWUSST wertgleich zu `validierung._KOLLISION_MM`
# und `anker_strategy._MIN_RZ_MERGE_MM` (= 250 mm), aber lokal gehalten — ein Import von
# `validierung` verletzte die Owner-Grenze (platzierung importiert nur `contracts`).
_MIN_ABSTAND_MM = 250.0

# Owner-Korrektur (H-Gebäude-DXF, „falsch"-Marker 2026-09-05): zwei GLEICHARTIGE
# Sicherheitsleuchten in nächster Distanz (real 1,1–1,3 m: Sonderstellen-Pflicht-SL
# neben Verdichtungs-SL) sind eine zu viel — unter 2 m deckt EINE Leuchte beide
# Zwecke (Sonderstellen-„nahe" = ≤ 2 m). Bewusst NUR gleichartig und NUR SL:
# die 3,7-m-Nachbarschaften (Stiegenhaus-SL ↔ Gang-SL) hat der Owner stehen lassen.
_DUBLETTEN_ABSTAND_MM = {"sicherheitsleuchte": 2000.0}

# Prioritäts-Rang je Leuchten-Art: kleiner = wichtiger, bleibt bei Konflikt stehen.
_RANG = {"rz": 0, "sicherheitsleuchte": 1, "antipanik": 2}

# Kleiner Puffer über den Mindestabstand, damit float-Rundung die (< 250)-Prüfung nicht
# wieder triggert.
_NUDGE_EPS_MM = 1.0


def _dist(a: Point, b: Point) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


def _rang(p: Platzierung) -> int:
    return _RANG.get(p.kind, 99)


def _polygon_of(xy: Point, raum: RaumModell) -> Polygon | None:
    """Das Raumpolygon, in dem ``xy`` liegt (Nudge-Clamp); None, wenn keins passt."""
    for r in raum.raeume:
        if len(r.polygon_mm) >= 3 and point_in_polygon(xy, r.polygon_mm):
            return r.polygon_mm
    return None


def _erster_konflikt(p: Platzierung, akzeptiert: list[Platzierung]) -> Platzierung | None:
    """Erstes schon akzeptiertes Symbol im Konfliktabstand (oder None).

    Gleichartige Symbole nutzen ggf. eine größere Dubletten-Schwelle
    (`_DUBLETTEN_ABSTAND_MM`), verschieden-artige den 250-mm-Mindestabstand."""
    for q in akzeptiert:
        d = _dist(p.xy_mm, q.xy_mm)
        schwelle = (
            _DUBLETTEN_ABSTAND_MM.get(p.kind, _MIN_ABSTAND_MM)
            if p.kind == q.kind else _MIN_ABSTAND_MM
        )
        if d < schwelle:
            return q
    return None


def _freie_position(xy: Point, akzeptiert: list[Platzierung], poly: Polygon | None) -> Point:
    """Nächste freie Position für ``xy``: ≥ Mindestabstand zu allen akzeptierten Symbolen
    und (falls ``poly`` gegeben) im Raumpolygon.

    Deterministische, gedeckelte Suche: weg vom Schwerpunkt der kollidierenden Nachbarn,
    in wachsenden Radien und einem festen Winkelkranz. Findet sich kein gültiger Punkt,
    bleibt ``xy`` unverändert (nie löschen — der echte Konflikt bleibt für die Prüfung
    sichtbar)."""

    def frei(k: Point) -> bool:
        if poly is not None and not point_in_polygon(k, poly):
            return False
        return all(_dist(k, q.xy_mm) >= _MIN_ABSTAND_MM for q in akzeptiert)

    if frei(xy):
        return xy

    nah = [q.xy_mm for q in akzeptiert if _dist(xy, q.xy_mm) < _MIN_ABSTAND_MM]
    cx = sum(a[0] for a in nah) / len(nah)
    cy = sum(a[1] for a in nah) / len(nah)
    dx, dy = xy[0] - cx, xy[1] - cy
    d = math.hypot(dx, dy)
    if d < 1e-9:                       # exakt koinzident → deterministische Default-Richtung
        dx, dy = 1.0, 0.0
    basis = math.atan2(dy, dx)
    schritt = _MIN_ABSTAND_MM + _NUDGE_EPS_MM
    for r_faktor in range(1, 9):       # bis 8× Mindestabstand
        radius = schritt * r_faktor
        for k in range(16):            # 16 Winkel, primär die Weg-Richtung (k=0)
            for s in (1, -1):
                a = basis + s * (math.pi / 8) * k
                kand = (cx + math.cos(a) * radius, cy + math.sin(a) * radius)
                if frei(kand):
                    return kand
    return xy


def entzerre(placements: list[Platzierung], raum: RaumModell) -> list[Platzierung]:
    """Löst Symbol-Kollisionen (< Mindestabstand) über alle Leuchten-Arten auf.

    Gibt eine neue Liste in **Original-Reihenfolge** zurück (verworfene Dubletten fehlen,
    verschobene tragen neues ``xy_mm``); mutiert die Eingabe nicht."""
    n = len(placements)
    if n < 2:
        return list(placements)

    order = sorted(range(n), key=lambda i: (_rang(placements[i]), i))
    akzeptiert: list[Platzierung] = []
    gehalten: dict[int, Platzierung] = {}
    for i in order:
        p = placements[i]
        konflikt = _erster_konflikt(p, akzeptiert)
        if konflikt is None:
            akzeptiert.append(p)
            gehalten[i] = p
        elif p.kind == konflikt.kind:
            continue                    # echte Dublette → verwerfen
        else:
            neu_xy = _freie_position(p.xy_mm, akzeptiert, _polygon_of(p.xy_mm, raum))
            p2 = p if neu_xy == p.xy_mm else p.model_copy(update={"xy_mm": neu_xy})
            akzeptiert.append(p2)
            gehalten[i] = p2

    return [gehalten[i] for i in range(n) if i in gehalten]
