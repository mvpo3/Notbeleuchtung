"""bereinigung — überlappende Raumpolygone nicht destruktiv entzerren.

Reine Geometrie über ``Raum``-Objekten: kein DXF, kein ezdxf, kein Dateizugriff.
Grundlage ist ``docs/ENIS_UEBERGABE_0908.md`` § 14.6/§ 14.6.1. Die Reihenfolge
ist genau die „angewandte Kaskade" aus § 14.6.1 (Owner-Entscheid, Reihenfolge =
Vorrang):

1. LIFT/SCHACHT wird IMMER aus jedem umgebenden Raum ausgestanzt (§ 14.6.1 (c)):
   genau EINE Seite ist exakt LIFT oder SCHACHT → sie gewinnt. Beide Seiten →
   weiter zur nächsten Regel.
2. RESTFLÄCHE (§ 14.6.1 (d)): hat genau EINE Seite quelle „R", VERLIERT diese
   Seite — AUSSER ihr ``raum_typ`` ist LIFT oder SCHACHT, dann verliert sie NIE
   (s. unten). Beide R → weiter zur nächsten Regel.
3. Enthaltensein (§ 14.6.1 (b)): Schnitt/kleinere Fläche >= 0,99 und kein
   Duplikat → die kleinere gewinnt, die größere bekommt das Loch. MIT
   Stempelschutz, siehe unten.
4. Vorrang nach Quelle (§ 14.6.1 (a)): Stempel-Polygon > Layer/HATCH ohne
   Stempel > Flutung > Restfläche (``QUELLE_RANG``). Bei gleichem Rang gewinnt
   das Polygon, dessen Fläche näher am Stempelwert liegt (``STEMPEL_NAEHE``).
5. Teilüberlappung: die gemeinsame Fläche geht an den näheren Schwerpunkt
   (``SCHWERPUNKT``).

Die Buchungsnamen des Contract-Literals ``BereinigungsRegel`` sind UNVERÄNDERT;
verschoben haben sich nur die Regel-NUMMERN: ``RESTFLAECHE`` 5 → 2,
``ENTHALTENSEIN`` 2 → 3, ``QUELLE_RANG``/``STEMPEL_NAEHE`` 3 → 4,
``SCHWERPUNKT`` 4 → 5. ``ALLE_REGELN`` bleibt die Menge 1-5.

Owner-Begründung für Regel 2 an Position 2 (wörtlich): „sonst kann eine
Restfläche in Regel 4 über Schwerpunktnähe Fläche gewinnen, obwohl sie
nachrangig ist." Damit ist der frühere Regel-5-SCHLUSSPASS (R minus Vereinigung
aller Nicht-R nach den Paaren) ÜBERFLÜSSIG und entfernt — Regel 2 zieht den
Schnitt für jedes gemischte Paar schon als Paar-Regel ab.

Regel 1 steht VOR Regel 2, und das ist nicht verhandelbar: 4 der 5
LIFT/SCHACHT-Räume im Bestand haben quelle R (Barawitzka ``rest_1`` 2,304 m²
und ``rest_3`` 2,534 m², Rennweg_OG3 ``rest_1`` 1,157 m² und ``rest_2``
1,152 m² — die beiden letzten nur 0,15 m² über der Entfall-Schwelle). Stünde
Regel 2 vorn, stanzte die Restflächen-Regel genau die Räume aus, die Regel 1
schützt (``rest_komponenten`` typisiert kleine Komponenten als SCHACHT).
Festgehalten in ``test_regel1_vor_regel2_schacht_gewinnt``.

Dieselbe Reihenfolge hatte eine LÜCKE, jetzt geschlossen: sind BEIDE Seiten
LIFT/SCHACHT und nur eine davon quelle R, greift Regel 1 per XOR nicht und
Regel 2 löschte die R-Seite — also genau den Raum, den Regel 1 schützt. Darum
ist ein Raum mit ``raum_typ`` LIFT oder SCHACHT NIE Verlierer der Regel 2; das
Paar fällt dann auf Regel 3/4/5 (``test_regel1_beide_lift_schacht_dann_regel2``,
der vorher die Lücke festschrieb). Reine Vorsorge: im Bestand kommt das Paar
nicht vor (0 RESTFLAECHE-Buchungen über alle fünf Pläne) — bei Rennweg_OG3 lägen
``rest_1`` 1,157 m² und ``rest_2`` 1,152 m² aber nur 0,15 m² über der
Entfall-Schwelle.

STEMPELSCHUTZ bei Regel 3 (Owner-Entscheid, ``STEMPEL_SCHUTZ`` = 10 %): „Regel 2
bleibt vor Regel 3 (Geometrie vor Herkunft), aber mit Schutz." Geprüft wird der
VERLIERER der Enthaltensein-Regel — der äußere, größere Raum, der das Loch
bekäme. Er wird nur dann NICHT gestanzt, wenn BEIDE Bedingungen gelten:

1. ``_rang(Verlierer) < _rang(Gewinner)`` — der äußere Raum hat den BESSEREN
   Quellen-Rang (1 = L/H mit Stempel, 2 = L/H ohne, 3 = F, 4 = R/unbekannt).
   Bei GLEICHEM Rang greift der Schutz NICHT.
2. Er hat eine Stempelfläche S und wiche seine Fläche NACH dem Abzug um mehr
   als 10 % von S ab (``|(A_nach − S) / S| > 0,10``).

Bedingung 1 ist der Owner-NACHENTSCHEID; der erste Entscheid hatte nur
Bedingung 2 und war damit zu breit. Begründung des Owners: geschützt werden soll
ein gezeichneter, gestempelter Raum, der durch das Ausstanzen von seinem
Stempelwert wegwandert — nicht eine Flutung, die ihren Stempelwert ohnehin nur
durch Übergriff erreicht.

GEMESSEN mit ``scripts/analyse/ueberlappung_regeln.py`` über die eingecheckten
Roh-Ringe der fünf Pläne (Messskript-Zahlen, kein Planlauf). Nur mit
Bedingung 2 schützte die Regel SECHS Paare, es blieben 11 Überlapper /
58,260 m² doppelt belegt. MIT Bedingung 1 bleibt genau EIN Paar geschützt —
Muthgasse ``raum_29`` (quelle L mit Stempel, Rang 1) enthält ``raum_91``
(quelle F, Rang 3) zu 99,97 %, Stempel 16,52 m², roh 16,52 → 13,97 m² =
−15,4 % — und es bleiben 2 Überlapper / 2,552 m². Die anderen fünf Paare werden
wieder gestanzt: dort ist der äußere Raum eine Flutung (F) gegen einen
L/H-Gewinner oder F gegen F. Mitbewegt gegenüber dem breiten Schutz:
ENTHALTENSEIN 1 → 6 Buchungen (7 Paare erkannt, 6 gestanzt, 1 geschützt),
ENTFALL 4 → 5 (``raum_86`` entfällt wieder), ZERFALL 9,300 → 14,799 m²,
SCHLITZ 0 → 1.

Das geschützte Paar bleibt ungelöst und wird ausdrücklich NICHT an Regel 4/5
weitergegeben; stattdessen entsteht eine Zeile in ``warnungen`` mit Raum-ids,
Stempelwert, Fläche vorher, Fläche nachher und Abweichung in Prozent. Folge,
bewusst in Kauf genommen: das Paar bleibt überlappend, die Überlapper-Kennzahl
steigt (ohne Schutz 0, mit Schutz 2).

VIER GRENZEN des Schutzes, alle gemessen:
(a) Geprüft wird die ROH-Differenz ``Fläche(roh) − Schnitt``, NICHT die
    Endfläche nach Zerfall und Schlitz-Kodierung — bewusst, weil die Endfläche
    reihenfolgeabhängig wäre und der Entscheid deterministisch bleiben muss.
    Gemessener Grenzfall (Konstruktion: 100,000 m² außen, 10,000 m² mittiges
    Loch, Stempel 100,00 m²): geprüft −10,0000 % — nicht > 10 %, also
    gestanzt; die Endfläche liegt bei rund −10,003 % (Schlitzverlust
    ≈ 3000 mm²). Ohne die Konstruktion ist die zweite Dezimale nicht
    reproduzierbar, sie hängt allein an der Schlitzlänge.
(b) Der Rand bei genau 10 % entscheidet sich am Gleitkomma-Rauschen
    (0,10000000000000003 schützt, 0,099999999999999936 nicht) — nicht garantiert.
(c) Stempelwert 0,00 m² gilt als „Stempel vorhanden" und ergibt unendliche
    Abweichung (``_stempel_abweichung``), erfüllt die 10-%-Bedingung also
    IMMER — schützt aber nur zusammen mit Bedingung 1: bei besserem Rang
    des Verlierers stets, bei gleichem oder schlechterem Rang gar nicht.
    Gegenfall gemessen: S=0,00 und beide Seiten F → kein Schutz, Buchungen
    ENTHALTENSEIN + SCHLITZ, keine Warnung. Im Bestand 0 Fälle.
(d) Der Schutz gilt ausdrücklich NUR für Regel 3. Ein gestempelter R-Raum
    verliert über Regel 2 ohne Schutz und ohne Warnung; im Bestand 0 Fälle.

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

#: Alle Regeln. Die MENGE bleibt 1-5, die BEDEUTUNG der Nummern folgt der
#: angewandten Kaskade aus § 14.6.1 (Modul-Docstring): 1 LIFT_SCHACHT,
#: 2 RESTFLAECHE, 3 ENTHALTENSEIN, 4 QUELLE_RANG/STEMPEL_NAEHE, 5 SCHWERPUNKT.
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
#: Stempelschutz bei Regel 3 (Owner-Entscheid): weicht der Verlierer NACH dem
#: Abzug um mehr als das vom Stempelwert ab UND hat er den besseren
#: Quellen-Rang als der Gewinner (Owner-Nachentscheid), wird NICHT ausgestanzt,
#: sondern gewarnt — das Paar bleibt ungelöst (keine Weitergabe an Regel 4/5).
STEMPEL_SCHUTZ = 0.10


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
    """Quellen-Rang für Regel 4 (``QUELLE_RANG``): kleiner gewinnt."""
    q = (quelle.get(raum_id) or "").strip().upper()
    if q in ("L", "H"):
        return 1 if stempel_m2.get(raum_id) is not None else 2
    if q == "F":
        return 3
    return 4                      # R und unbekannte Quelle


def _stempel_abweichung(flaeche_mm2: float, stempel_m2: float) -> float:
    """Relative Abweichung |A − S| / S. S == 0 und A > 0 → unendlich.

    Zwei Verwender: Regel 4 (``STEMPEL_NAEHE``, kleinere Abweichung gewinnt) und
    der Stempelschutz in Regel 3 (Abweichung NACH dem Abzug gegen
    ``STEMPEL_SCHUTZ``).
    """
    a = flaeche_mm2 / 1e6
    if stempel_m2 == 0:
        return math.inf if a > 0 else 0.0
    return abs(a - stempel_m2) / stempel_m2


def _ist_rest(raum_id: str, quelle: Mapping[str, str]) -> bool:
    """Regel 2: quelle „R" = Restfläche aus ``rest_komponenten``."""
    return (quelle.get(raum_id) or "").strip().upper() == "R"


def _schutz_warnung(gross: str, klein: str, stempel_m2: float,
                    vorher_mm2: float, nachher_mm2: float) -> str:
    """Eine Zeile je geschütztem Paar — DATEN, kein Druck (der WARNPFAD druckt
    nicht; die zwei Fehlermeldungen zu Schlitz-Kodierung und Roh-Ring-Rückfall
    drucken weiter).

    Enthält alles, was der Bericht braucht: beide Raum-ids, Stempelwert, Fläche
    vorher, Fläche nachher, Abweichung in Prozent.
    """
    nach = nachher_mm2 / 1e6
    abw = ("unendlich (Stempel 0,00 m2)" if stempel_m2 == 0
           else f"{(nach - stempel_m2) / stempel_m2 * 100:+.1f} %")
    return (f"{gross} nicht ausgestanzt (enthaelt {klein}): Stempel "
            f"{stempel_m2:.2f} m2, Flaeche {vorher_mm2 / 1e6:.2f} m2 -> "
            f"{nach:.2f} m2 = {abw} Abweichung, ueber Stempelschutz "
            f"{STEMPEL_SCHUTZ * 100:.0f} % -> Paar bleibt ueberlappend")


def _entscheid(a: str, b: str, roh: Mapping[str, Polygon], inter,
               typ: Mapping[str, str], quelle: Mapping[str, str],
               stempel_m2: Mapping[str, float | None],
               regeln: frozenset[int],
               warnungen: list[str]) -> tuple[int, str, str, str] | None:
    """(Regelnummer, Regel-Label, Gewinner-id, Verlierer-id) oder None (Paar offen).

    Entscheidet AUSSCHLIESSLICH auf Roh-Attributen — dadurch ist das Ergebnis
    unabhängig von der Abarbeitungsreihenfolge der Paare.

    ``None`` heißt „das Paar bleibt überlappend". Zwei Wege dorthin: keine Regel
    greift, ODER der Stempelschutz bricht Regel 3 ab — dann hängt diese Funktion
    eine Zeile an ``warnungen`` und gibt das Paar ausdrücklich NICHT an Regel 4/5
    weiter (Owner-Entscheid). Der Schutz greift nur, wenn der Verlierer den
    besseren Quellen-Rang hat als der Gewinner (Owner-Nachentscheid, s.
    Modul-Docstring).
    """
    if 1 in regeln:
        a_ls, b_ls = typ[a] in LIFT_SCHACHT, typ[b] in LIFT_SCHACHT
        if a_ls != b_ls:
            return (1, "LIFT_SCHACHT", a, b) if a_ls else (1, "LIFT_SCHACHT", b, a)
    if 2 in regeln:
        a_r, b_r = _ist_rest(a, quelle), _ist_rest(b, quelle)
        if a_r != b_r:
            gewinner, verlierer = (b, a) if a_r else (a, b)
            # LIFT/SCHACHT ist NIE Regel-2-Verlierer: § 14.6.1 (c) („IMMER
            # ausgestanzt") steht über (d). Greifbar wird das nur, wenn BEIDE
            # Seiten LIFT/SCHACHT sind — dann greift Regel 1 per XOR nicht und
            # Regel 2 löschte die R-Seite. Das Paar fällt dann auf Regel 3/4/5.
            if typ[verlierer] not in LIFT_SCHACHT:
                return (2, "RESTFLAECHE", gewinner, verlierer)
    if 3 in regeln:
        klein, gross = sorted((a, b), key=lambda i: (roh[i].area, i))
        if (inter.area / roh[klein].area >= _ENTHALTEN
                and inter.area / roh[gross].area < _ENTHALTEN):
            # Stempelschutz: der äußere Raum bekäme das Loch. Er wird nur dann
            # NICHT gestanzt, wenn er den besseren Quellen-Rang hat als der
            # innere UND danach um > STEMPEL_SCHUTZ von seinem Stempelwert
            # abwiche (Owner-Nachentscheid, s. Modul-Docstring).
            s = stempel_m2.get(gross)
            nach = roh[gross].area - inter.area
            if (s is not None
                    and _rang(gross, quelle, stempel_m2)
                    < _rang(klein, quelle, stempel_m2)
                    and _stempel_abweichung(nach, s) > STEMPEL_SCHUTZ):
                warnungen.append(
                    _schutz_warnung(gross, klein, s, roh[gross].area, nach))
                return None
            return (3, "ENTHALTENSEIN", klein, gross)
    if 4 in regeln:
        ra, rb = (_rang(a, quelle, stempel_m2), _rang(b, quelle, stempel_m2))
        if ra != rb:
            return (4, "QUELLE_RANG", a, b) if ra < rb else (4, "QUELLE_RANG", b, a)
        sa, sb = stempel_m2.get(a), stempel_m2.get(b)
        if sa is not None and sb is not None:
            da = _stempel_abweichung(roh[a].area, sa)
            db = _stempel_abweichung(roh[b].area, sb)
            if da != db:
                return (4, "STEMPEL_NAEHE", a, b) if da < db else (4, "STEMPEL_NAEHE", b, a)
    if 5 in regeln:
        za = roh[a].centroid.distance(inter.centroid)
        zb = roh[b].centroid.distance(inter.centroid)
        if za != zb:
            return (5, "SCHWERPUNKT", a, b) if za < zb else (5, "SCHWERPUNKT", b, a)
        return (5, "SCHWERPUNKT", a, b) if a < b else (5, "SCHWERPUNKT", b, a)
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
              regeln: frozenset[int] = ALLE_REGELN,
              warnungen: list[str] | None = None) -> dict[str, Bereinigt]:
    """Raumbereinigung nach den Owner-Regeln 1-5. Mutiert NICHTS.

    ``regeln`` schaltet einzelne Regeln ab (kumulative Messung in
    ``scripts/analyse/ueberlappung_regeln.py``). Räume mit < 3 Punkten oder
    Fläche 0 nehmen nicht teil und fehlen im Ergebnis-Dict.

    ``warnungen``: wer die Stempelschutz-Meldungen (Regel 3) braucht, gibt eine
    Liste herein — sie wird ANGEHÄNGT. Der WARNPFAD druckt nichts, die
    Warnungen sind Daten; die zwei bestehenden Fehlermeldungen
    (Schlitz-Kodierung, Roh-Ring-Rückfall) bleiben und drucken weiter.
    ``bereinige_kaskade`` reicht die Liste durch.

    Räume ohne Abzug kommen mit ``eintraege == []`` zurück, ihr ``polygon_mm``
    ist dann der ``buffer(0)``-REPARIERTE Ring, nicht zwingend der Eingabering.
    Produktiv folgenlos (``bereinige_kaskade`` schreibt nur Räume MIT Einträgen
    zurück), für Messskripte aber relevant: der Überlappungs-Riegel misst die
    Originale aus ``raeume.json``.
    """
    warn = warnungen if warnungen is not None else []
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
    for i, j, inter in paare:
        e = _entscheid(i, j, roh, inter, typ, quelle, stempel_m2, regeln, warn)
        if e is None:
            continue        # keine Regel greift ODER Stempelschutz → Paar offen
        nummer, label, gewinner, verlierer = e
        entschieden.append((nummer, -inter.area, (i, j), label, gewinner, verlierer))
    entschieden.sort(key=lambda t: t[:3])

    for _, _, _, label, gewinner, verlierer in entschieden:
        _abziehen(aktuell, eintraege, verlierer, aktuell[gewinner], label, gewinner)

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
                      quelle: dict[str, str],
                      warnungen: list[str] | None = None,
                      ) -> list[tuple[Raum, Stempel | None]]:
    """Kern auf ein Kaskaden-Ergebnis anwenden (IN PLACE) → entfallene Räume.

    ``warnungen`` wird — falls übergeben — mit den Stempelschutz-Meldungen der
    Regel 3 gefüllt (durchgereicht an ``bereinige``). Kein Contract-Feld: die
    Zeilen gehen über ``KaskadeErgebnis.bereinigung_warnungen`` an den Bericht.

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

    erg = bereinige(alle, quelle, stempel_m2, warnungen=warnungen)
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
