"""bereinigung — überlappende Raumpolygone nicht destruktiv entzerren.

Reine Geometrie über ``Raum``-Objekten: kein DXF, kein ezdxf, kein Dateizugriff.
Grundlage ist ``docs/ENIS_UEBERGABE_0908.md`` § 14.6/§ 14.6.1 mit den fünf
Owner-Regeln (Reihenfolge = Vorrang):

1. LIFT/SCHACHT wird IMMER aus jedem umgebenden Raum ausgestanzt.
2. Enthaltensein: liegt ein Raum vollständig in einem anderen, bleiben beide —
   der äußere bekommt ein Loch.
3. Vorrang nach Quelle: Stempel-Polygon > Layer/HATCH ohne Stempel > Flutung >
   Restfläche (3a). Bei gleicher Quelle gewinnt das Polygon, dessen Fläche näher
   am Stempelwert liegt (3b).
4. Teilüberlappung: die gemeinsame Fläche geht an den näheren Schwerpunkt.
5. Restflächen (R) sind nachrangig und ragen nie über ein anderes Polygon.

Regel 1 steht VOR Regel 5: ein R-Raum, der selbst LIFT/SCHACHT ist, ist nie
Regel-5-Verlierer (``rest_komponenten`` typisiert kleine Komponenten als
SCHACHT — ohne die Ausnahme stanzte Regel 5 genau die Räume wieder aus, die
Regel 1 schützt).

ABWEICHUNG VON § 14.6.1, ausdrücklich deklariert: die dortige „angewandte
Kaskade" (§ 14.6.1, Z. 1975-1984) ordnet **(d) Restfläche weicht an Position 2**
— hier steht sie zuletzt (Regel 5). Grund ist dieselbe Kollision wie oben: an
Position 2 unterläuft (d) das „LIFT und SCHACHT werden IMMER ausgestanzt", weil
4 der 5 LIFT/SCHACHT-Räume im Bestand aus dem R-Zweig kommen. Gemessener
Wirkungsunterschied (nur konstruiert, im Bestand greift Regel 5 in 0 Fällen):
liegt ein R-Raum VOLLSTÄNDIG in einem Nicht-R-Raum, bleibt er hier erhalten und
der äußere bekommt ein Loch (Regel 2), während (d) an Position 2 den R-Raum
verlieren und damit entfallen ließe. Bei Teilüberlappung ist das Ergebnis
gleich, weil Rang 4 ohnehin verliert. Die Owner-Entscheidung dazu steht aus.

Nicht destruktiv: ``Raum.polygon_roh`` behält den Ring vor der Bereinigung,
``Raum.bereinigung[]`` bucht jeden Abzug mit Regel und Gegenspieler. Prüfbare
Invariante (``test_bereinigung.py::test_flaechenbuchhaltung_geht_auf``):
Fläche(polygon_roh) − Fläche(polygon_mm) == Σ ``bereinigung[].flaeche_m2``,
Entfall und Schlitzverlust eingeschlossen.

Löcher kann der Contract-Ring (eine Punktliste) nicht abbilden — sie werden am
Ende als 1-mm-Schlitz zur Außenkontur kodiert. GRENZE, gemessen: Fläche,
``point_in_polygon``, shapely ``covers`` und ``grid_points`` sehen das Loch
korrekt als außen; Konsumenten der Bbox-Mitte (``platzierung/geometry.py``
``find_center_diagonal``, und ``find_center_visual`` oberhalb Fläche/bbox ≥ 0,9)
NICHT. Dasselbe gilt für den bestehenden 50-mm-Schlitz der ``lift_erkennung``.

Robustheit: keine Ausnahme verlässt dieses Modul freiwillig. Schlägt die
Schlitz-Kodierung fehl, bleibt der betroffene Raum beim Roh-Ring (kein Eintrag,
Warnzeile) — ein GEOS-Fehler auf den 400-738-Punkt-Rasterpolygonen darf keinen
Plan-Lauf und keinen Provider-Parse abbrechen.
"""
from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass

import shapely
from shapely.geometry import Point, Polygon
from shapely.ops import unary_union
from shapely.strtree import STRtree

from notbeleuchtung.hauptengine.contracts.raum_modell import Bereinigung, Raum

from .stempel_anker import Stempel, Zuordnung

XY = tuple[float, float]

ALLE_REGELN: frozenset[int] = frozenset({1, 2, 3, 4, 5})
RAUSCH_MM2 = 1.0        # Rauschschwelle § 14.1
ENTFALL_MM2 = 1e6       # 1 m², dasselbe Kriterium wie kaskade.py:115
SCHLITZ_MM = 1.0        # Schlitzbreite (0,5 mm Puffer je Seite, square caps)
#: Regel 1 greift nur für diese Kanon-Typen. NICHT AUFZUGSVORPLATZ (das ist die
#: Erschließungsfläche VOR dem Lift, kein Schacht). § 14.6.1 (c) nennt zusätzlich
#: „AUFZUG" — für dieses Wort gibt es im Kanon kein Label (`raumtyp.py` vergibt
#: nur LIFT, SCHACHT, AUFZUGSVORPLATZ), die Auslassung ist also kein Versehen.
LIFT_SCHACHT = frozenset({"LIFT", "SCHACHT"})
_ENTHALTEN = 0.99       # „vollständig in" — Anteil der eigenen Fläche


@dataclass(frozen=True)
class Bereinigt:
    """Ergebnis je Raum. ``eintraege`` leer = unverändert."""

    polygon_mm: list[XY]            # bereinigter Ring; [] bei Entfall
    flaeche_m2: float               # Fläche von polygon_mm (0.0 bei Entfall)
    eintraege: list[Bereinigung]
    entfallen: bool


def _groesste(geom) -> Polygon | None:
    """Größte Polygon-Komponente; Gleichstand nach ``bounds`` (deterministisch)."""
    if geom is None or geom.is_empty:
        return None
    if geom.geom_type == "Polygon":
        return geom
    teile = [g for g in getattr(geom, "geoms", [])
             if g.geom_type == "Polygon" and not g.is_empty and g.area > 0]
    if not teile:
        return None
    return min(teile, key=lambda g: (-g.area, g.bounds))


def _startpolygon(ring: Sequence[XY]) -> Polygon | None:
    """Ring → gültiges Polygon (``buffer(0)``-Reparatur); None = nimmt nicht teil."""
    if ring is None or len(ring) < 3:
        return None
    p = Polygon(ring)
    if not p.is_valid:
        p = _groesste(p.buffer(0))
    if p is None or p.is_empty or p.area <= 0:
        return None
    return p


def _ring(p: Polygon) -> list[XY]:
    return [(float(x), float(y)) for x, y in p.exterior.coords[:-1]]


def _rang(raum_id: str, quelle: Mapping[str, str],
          stempel_m2: Mapping[str, float | None]) -> int:
    """Quellen-Rang für Regel 3a: kleiner gewinnt."""
    q = (quelle.get(raum_id) or "").strip().upper()
    if q in ("L", "H"):
        return 1 if stempel_m2.get(raum_id) is not None else 2
    if q == "F":
        return 3
    return 4                      # R und unbekannte Quelle


def _stempel_abweichung(flaeche_mm2: float, stempel_m2: float) -> float:
    """Relative Abweichung |A − S| / S für Regel 3b. S == 0 und A > 0 → unendlich."""
    a = flaeche_mm2 / 1e6
    if stempel_m2 == 0:
        return math.inf if a > 0 else 0.0
    return abs(a - stempel_m2) / stempel_m2


def _entscheid(a: str, b: str, roh: Mapping[str, Polygon], inter,
               typ: Mapping[str, str], quelle: Mapping[str, str],
               stempel_m2: Mapping[str, float | None],
               regeln: frozenset[int]) -> tuple[int, str, str, str] | None:
    """(Regelnummer, Regel-Label, Gewinner-id, Verlierer-id) oder None (Paar offen).

    Entscheidet AUSSCHLIESSLICH auf Roh-Attributen — dadurch ist das Ergebnis
    unabhängig von der Abarbeitungsreihenfolge der Paare.
    """
    if 1 in regeln:
        a_ls, b_ls = typ[a] in LIFT_SCHACHT, typ[b] in LIFT_SCHACHT
        if a_ls != b_ls:
            return (1, "LIFT_SCHACHT", a, b) if a_ls else (1, "LIFT_SCHACHT", b, a)
    if 2 in regeln:
        klein, gross = sorted((a, b), key=lambda i: (roh[i].area, i))
        if (inter.area / roh[klein].area >= _ENTHALTEN
                and inter.area / roh[gross].area < _ENTHALTEN):
            return (2, "ENTHALTENSEIN", klein, gross)
    if 3 in regeln:
        ra, rb = (_rang(a, quelle, stempel_m2), _rang(b, quelle, stempel_m2))
        if ra != rb:
            return (3, "QUELLE_RANG", a, b) if ra < rb else (3, "QUELLE_RANG", b, a)
        sa, sb = stempel_m2.get(a), stempel_m2.get(b)
        if sa is not None and sb is not None:
            da = _stempel_abweichung(roh[a].area, sa)
            db = _stempel_abweichung(roh[b].area, sb)
            if da != db:
                return (3, "STEMPEL_NAEHE", a, b) if da < db else (3, "STEMPEL_NAEHE", b, a)
    if 4 in regeln:
        za = roh[a].centroid.distance(inter.centroid)
        zb = roh[b].centroid.distance(inter.centroid)
        if za != zb:
            return (4, "SCHWERPUNKT", a, b) if za < zb else (4, "SCHWERPUNKT", b, a)
        return (4, "SCHWERPUNKT", a, b) if a < b else (4, "SCHWERPUNKT", b, a)
    return None


def _abziehen(aktuell: dict[str, Polygon | None], eintraege: dict[str, list[Bereinigung]],
              verlierer: str, gewinner_geom, label: str, gegenspieler: str) -> None:
    """``verlierer -= gewinner``; Eintrag nur bei Flächenverlust > Rauschschwelle."""
    vorher = aktuell[verlierer]
    if vorher is None or vorher.is_empty:
        return
    nachher = vorher.difference(gewinner_geom)
    verlust = vorher.area - nachher.area
    if verlust <= RAUSCH_MM2:
        return
    aktuell[verlierer] = nachher
    eintraege[verlierer].append(Bereinigung(
        regel=label, gegenspieler=gegenspieler, flaeche_m2=verlust / 1e6))


def _schlitz(p: Polygon) -> tuple[Polygon, float, bool]:
    """Löcher als 1-mm-Schlitz zur Außenkontur → (ein Ring, Verlust mm², ok).

    ``ok=False`` heißt: der Aufrufer verwirft die Bereinigung dieses Raums und
    bleibt beim Roh-Ring. Kein ``assert`` — der würde unter ``python -O``
    verschwinden und im Produktionspfad den Lauf abreißen.

    „Nächstes Loch zuerst" schließt das Kreuzen offener Löcher aus: kreuzte die
    kürzeste Verbindung von Loch H ein noch offenes H2, wäre dessen Abstand zur
    Außenkontur kleiner — Widerspruch zur Minimalität.
    """
    verlust = 0.0
    try:
        for _ in range(len(p.interiors) + 5):
            if not p.interiors:
                return p, verlust, True
            aussen = p.exterior
            loch = min(p.interiors, key=lambda r: (aussen.distance(r), r.bounds))
            linie = shapely.shortest_line(loch, aussen)
            if linie is None or linie.is_empty:
                return p, verlust, False
            if linie.length < 1e-6:
                schlitz = Point(linie.coords[0]).buffer(SCHLITZ_MM / 2, cap_style="square")
            else:
                schlitz = linie.buffer(SCHLITZ_MM / 2, cap_style="square")
            vorher = p.area
            gross = _groesste(p.difference(schlitz))
            if gross is None:
                return p, verlust, False
            verlust += vorher - gross.area
            p = gross
    except Exception as exc:  # noqa: BLE001 — Schlitz-Kodierung darf den Lauf nie killen
        print(f"   bereinigung: Schlitz-Kodierung fehlgeschlagen: {exc}")
        return p, verlust, False
    return p, verlust, not p.interiors


def bereinige(raeume: Sequence[Raum],
              quelle: Mapping[str, str],                 # raum.id -> "L"|"H"|"F"|"R"
              stempel_m2: Mapping[str, float | None],    # raum.id -> Stempelfläche (m²)
              regeln: frozenset[int] = ALLE_REGELN) -> dict[str, Bereinigt]:
    """Raumbereinigung nach den Owner-Regeln 1-5. Mutiert NICHTS.

    ``regeln`` schaltet einzelne Regeln ab (kumulative Messung in
    ``scripts/analyse/ueberlappung_regeln.py``). Räume mit < 3 Punkten oder
    Fläche 0 nehmen nicht teil und fehlen im Ergebnis-Dict.

    Räume ohne Abzug kommen mit ``eintraege == []`` zurück, ihr ``polygon_mm``
    ist dann der ``buffer(0)``-REPARIERTE Ring, nicht zwingend der Eingabering.
    Produktiv folgenlos (``bereinige_kaskade`` schreibt nur Räume MIT Einträgen
    zurück), für Messskripte aber relevant: der Überlappungs-Riegel misst die
    Originale aus ``raeume.json``.
    """
    roh: dict[str, Polygon] = {}
    typ: dict[str, str] = {}
    for r in raeume:
        p = _startpolygon(r.polygon_mm)
        if p is None:
            continue
        roh[r.id] = p
        typ[r.id] = (r.raum_typ or "").strip().upper()
    ids = sorted(roh)
    aktuell: dict[str, Polygon | None] = dict(roh)
    eintraege: dict[str, list[Bereinigung]] = {i: [] for i in ids}

    # Paare über den Roh-Polygonen; ein Paar zählt erst über der Rauschschwelle.
    reihe = [roh[i] for i in ids]
    baum = STRtree(reihe)
    paare: list[tuple[str, str, object]] = []
    for k, i in enumerate(ids):
        for m in baum.query(reihe[k]):
            m = int(m)
            if m <= k:
                continue
            inter = roh[i].intersection(roh[ids[m]])
            if inter.is_empty or inter.area <= RAUSCH_MM2:
                continue
            paare.append((i, ids[m], inter))

    entschieden = []
    regel1_paare: set[tuple[str, str]] = set()
    for i, j, inter in paare:
        e = _entscheid(i, j, roh, inter, typ, quelle, stempel_m2, regeln)
        if e is None:
            continue                      # Paar bleibt offen (nur für die Messung)
        nummer, label, gewinner, verlierer = e
        if nummer == 1:
            regel1_paare.add((i, j))
        entschieden.append((nummer, -inter.area, (i, j), label, gewinner, verlierer))
    entschieden.sort(key=lambda t: t[:3])

    for _, _, _, label, gewinner, verlierer in entschieden:
        _abziehen(aktuell, eintraege, verlierer, aktuell[gewinner], label, gewinner)

    # Regel 5 zum Schluss: R weicht jedem Nicht-R-Polygon. Ausnahme (Owner-
    # Reihenfolge 1 vor 5): ein R-Raum, der selbst LIFT/SCHACHT ist, ist nie
    # Verlierer, und ein von Regel 1 entschiedenes Paar wird nicht erneut angefasst.
    if 5 in regeln:
        nicht_r = [i for i in ids if (quelle.get(i) or "").strip().upper() != "R"]
        for i in [i for i in ids if (quelle.get(i) or "").strip().upper() == "R"]:
            if typ[i] in LIFT_SCHACHT:
                continue
            gegner = []
            for j in nicht_r:
                if tuple(sorted((i, j))) in regel1_paare:
                    continue
                if aktuell[i] is None or aktuell[j] is None:
                    continue
                s = aktuell[i].intersection(aktuell[j])
                if s.is_empty or s.area <= RAUSCH_MM2:
                    continue
                gegner.append((-s.area, j))
            for _, j in sorted(gegner):
                _abziehen(aktuell, eintraege, i, aktuell[j], "RESTFLAECHE", j)

    ergebnis: dict[str, Bereinigt] = {}
    for i in ids:
        eintr = list(eintraege[i])
        unveraendert = Bereinigt(_ring(roh[i]), roh[i].area / 1e6, [], False)
        if not eintr:
            ergebnis[i] = unveraendert
            continue
        gross = _groesste(aktuell[i])
        p = None
        if gross is not None:
            verworfen = aktuell[i].area - gross.area
            # Ohne Schwelle: die Invariante ist als „==" dokumentiert, also darf
            # auch ein Bruchteil eines mm² nicht unbelegt verschwinden (gemessen
            # auf Mollgasse: 3 Räume mit je ~0,17 mm² Nebenkomponente).
            if verworfen > 0:
                eintr.append(Bereinigung(regel="ZERFALL", gegenspieler=None,
                                         flaeche_m2=verworfen / 1e6))
            p, schlitzverlust, ok = _schlitz(gross)
            if not ok:
                print(f"   bereinigung: {i} bleibt beim Roh-Ring "
                      f"(Loch-Kodierung nicht möglich)")
                ergebnis[i] = unveraendert
                continue
            if schlitzverlust > 0:      # s. ZERFALL: keine Schwelle, sonst leckt die Bilanz
                eintr.append(Bereinigung(regel="SCHLITZ", gegenspieler=None,
                                         flaeche_m2=schlitzverlust / 1e6))
        rest_mm2 = 0.0 if p is None else p.area
        if rest_mm2 < ENTFALL_MM2:
            eintr.append(Bereinigung(regel="ENTFALL", gegenspieler=None,
                                     flaeche_m2=rest_mm2 / 1e6))
            ergebnis[i] = Bereinigt([], 0.0, eintr, True)
            continue
        ring = _ring(p)
        ergebnis[i] = Bereinigt(ring, Polygon(ring).area / 1e6, eintr, False)
    return ergebnis


def ueberlappung(polygone: Sequence[Sequence[XY]],
                 schwelle: float = 0.05) -> tuple[set[int], float]:
    """(Indizes der Überlapper > ``schwelle`` der EIGENEN Fläche, doppelt belegte mm²).

    Definitionen wörtlich aus § 14.1: Rauschschwelle 1 mm², ``buffer(0)``-Reparatur,
    Einträge mit < 3 Punkten zählen nicht als Raum, Verhältnis je Seite getrennt,
    doppelt belegt = Σ Einzelflächen − ``unary_union``. Rückgabe in mm², damit
    „fast null" nicht als „0,000 m²" gelesen wird. Die Indizes beziehen sich auf
    die EINGABE-Sequenz (übersprungene Einträge kommen nie in die Menge).
    """
    geo: dict[int, Polygon] = {}
    for k, ring in enumerate(polygone):
        p = _startpolygon(ring)
        if p is not None:
            geo[k] = p
    idx = sorted(geo)
    reihe = [geo[k] for k in idx]
    if not reihe:
        return set(), 0.0
    baum = STRtree(reihe)
    ueberlapper: set[int] = set()
    for a_pos, a in enumerate(reihe):
        for b_pos in baum.query(a):
            b_pos = int(b_pos)
            if b_pos <= a_pos:
                continue
            inter = a.intersection(reihe[b_pos]).area
            if inter <= RAUSCH_MM2:
                continue
            if inter / a.area > schwelle:
                ueberlapper.add(idx[a_pos])
            if inter / reihe[b_pos].area > schwelle:
                ueberlapper.add(idx[b_pos])
    doppelt = sum(g.area for g in reihe) - unary_union(reihe).area
    return ueberlapper, doppelt


def bereinige_kaskade(raeume: list[Raum], rest_raeume: list[Raum],
                      zuordnungen: list[Zuordnung],
                      quelle: dict[str, str]) -> list[tuple[Raum, Stempel | None]]:
    """Kern auf ein Kaskaden-Ergebnis anwenden (IN PLACE) → entfallene Räume.

    Nicht destruktiv am Objekt: ``polygon_roh`` bekommt den Ring vor der
    Bereinigung, ``bereinigung`` die Buchungen. Entfallene Räume verlassen
    ``raeume``/``rest_raeume``, ihre Zuordnung wird ``kein_polygon`` (Muster
    ``kaskade.py:116``) — die Objekte selbst behalten Roh-Ring und Buchungen für
    Bericht und ``raeume.json``.

    ``polygon_index`` MUSS danach neu vergeben werden: ``restflaechen``
    (``stempel_anker.py:309-312``) filtert über die Positionen in ``raeume``.
    """
    alle = list(raeume) + list(rest_raeume)
    stempel_m2: dict[str, float | None] = {}
    stempel_je_raum: dict[str, Stempel] = {}
    for z in zuordnungen:
        if z.raum is None:
            continue
        stempel_m2.setdefault(z.raum.id, z.stempel.flaeche_m2)
        stempel_je_raum.setdefault(z.raum.id, z.stempel)

    erg = bereinige(alle, quelle, stempel_m2)
    entfallen: list[tuple[Raum, Stempel | None]] = []
    for r in alle:
        b = erg.get(r.id)
        if b is None or not b.eintraege:
            continue
        if not r.polygon_roh:
            r.polygon_roh = list(r.polygon_mm)
        r.polygon_mm = list(b.polygon_mm)
        r.flaeche_m2 = b.flaeche_m2
        r.bereinigung.extend(b.eintraege)
        if b.entfallen:
            entfallen.append((r, stempel_je_raum.get(r.id)))

    if entfallen:
        weg = {id(r) for r, _ in entfallen}
        raeume[:] = [r for r in raeume if id(r) not in weg]
        rest_raeume[:] = [r for r in rest_raeume if id(r) not in weg]
        for k, z in enumerate(zuordnungen):
            if z.raum is not None and id(z.raum) in weg:
                zuordnungen[k] = Zuordnung(z.stempel, None, None, None, "kein_polygon")
    # Nur `raeume`: Zuordnungen zeigen ausschliesslich dorthin, weil `ordne_zu`
    # vor der R-Stufe laeuft (`kaskade.py`) — ein `rest_raeume`-Objekt hat nie
    # eine Zuordnung. `restflaechen` (stempel_anker) filtert ueber genau diese
    # Positionen, deshalb muss die Neuvergabe nach dem Entfernen passieren.
    pos = {id(r): i for i, r in enumerate(raeume)}
    for z in zuordnungen:
        if z.raum is not None and id(z.raum) in pos:
            z.polygon_index = pos[id(z.raum)]
    return entfallen
