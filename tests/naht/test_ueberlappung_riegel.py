"""Riegel: Überlappende Raumpolygone dürfen nicht mehr werden (Owner-Auftrag).

Friert den in ``docs/ENIS_UEBERGABE_0908.md`` § 14.2 gemessenen Ist-Stand als
**Obergrenze** ein — je Plan und in Summe. Der Test schlägt fehl, sobald eine
Zahl **steigt**. Sinkt eine Zahl, wird das Band im selben Commit nachgezogen
(Owner-Regel: der Riegel hält den Fortschritt fest, er bremst ihn nicht).

Datenquelle sind die **eingecheckten** Laufergebnisse
``Projekte/_ergebnis/<Plan>/raeume.json`` und nicht ein frischer Provider-Parse.
Begründung: (a) die DXF-Eingangspläne sind per ``.gitignore`` nicht getrackt, ein
Parse-Test wäre in CI immer geskippt; (b) ein Parse der Muthgasse dauert ~800 s
und würde die Suite sprengen — dieser Test läuft in Bruchteilen einer Sekunde.
Der Preis: der Riegel greift erst, wenn die Ergebnisse neu erzeugt und
eingecheckt sind. Das ist derselbe Vertrag wie bei ``Projekte/_ergebnis/VERLAUF.md``.

Definitionen wörtlich aus § 14.1:
- Polygon = ``polygon_mm`` als ``shapely.Polygon``, ungültige Ringe über
  ``buffer(0)``; Einträge mit <3 Punkten sind Stempel ohne Polygon und zählen
  nicht als Raum.
- Überlappung = paarweise ``A.intersection(B).area``, Rauschschwelle 1 mm².
- Verhältnis **je Seite getrennt**: ``inter / eigene Fläche``.
- „Überlapper >5 %" = Raum-**Index** in einer Menge, also keine Doppelzählung;
  beide Seiten eines Paares können zählen, wenn beide die 5 % reißen.
- Doppelbelegte Fläche = Summe der Einzelflächen minus ``unary_union``-Fläche.
"""
import json
from pathlib import Path

import pytest
from shapely.geometry import Polygon
from shapely.ops import unary_union
from shapely.strtree import STRtree

BASIS = Path("Projekte/_ergebnis")
SCHWELLE = 0.05
RAUSCHEN_MM2 = 1.0

# Ist-Stand 2026-09-10 (Lauf 47df2d9), § 14.2. Obergrenzen — nur nach unten
# nachziehen, niemals anheben.
#
# NACHGEZOGEN 2026-09-12 (Lauf `6ebf676`, Bereinigung nach § 14.6/§ 14.6.1).
# Vorher standen hier 9/42,3 · 16/45,8 · 37/174,2 · 0 · 0, Summe 62/262,3.
# Gemessene Ausgabe dieses Laufs (Prüfstrecke, je Plan vorher → nachher):
#   Barawitzka_EG   9 → 0 Überlapper ·  42,253 m² → 0,05 mm²
#   Mollgasse_EG   16 → 0 Überlapper ·  45,845 m² → 0,14 mm²
#   Muthgasse_E2   37 → 0 Überlapper · 174,245 m² → 0,20 mm²
#   Rennweg_EG      0 → 0 Überlapper ·   0,000 m² → 0,00 mm²
#   Rennweg_OG3     0 → 0 Überlapper ·   0,000 m² → 0,00 mm²
# Die Restflächen (max. 0,20 mm²) liegen unter der Rauschschwelle von 1 mm² und
# damit unter dem Band 0.0 + TOLERANZ_M2.
BAND: dict[str, tuple[int, float]] = {
    # Plan: (Überlapper >5 %, doppelbelegte Fläche in m²)
    "Barawitzka_EG": (0, 0.0),
    "Mollgasse_EG": (0, 0.0),
    "Muthgasse_E2": (0, 0.0),
    "Rennweg_EG": (0, 0.0),
    "Rennweg_OG3": (0, 0.0),
}
BAND_SUMME = (0, 0.0)
TOLERANZ_M2 = 0.05  # Rundung der Bänder auf 0,1 m²

# Löschungsfeste UNTERGRENZE — die Gegenprobe zum Band oben. „0 Überlapper" ist
# zum Teil durch ENTFALL erkauft (5 Räume, Restkörper < 1 m², § 14.6.1), und
# Räume aus `raeume` zu entfernen senkt die Überlappungszahl IMMER. Gezählt
# werden deshalb die Einträge mit ≥ 3 Punkten in `raeume` PLUS die Liste
# `entfallen` (dort steht das Roh-Polygon in `polygon_roh`). Sinkt die Summe,
# ist ein weiterer Raum verschwunden — das ist eine Owner-Entscheidung und kein
# Nachziehen. Ist 2026-09-12 (Lauf `6ebf676`): 46+1 · 62+0 · 97+4 · 21+0 · 14+0.
BAND_RAEUME: dict[str, int] = {
    "Barawitzka_EG": 47,
    "Mollgasse_EG": 62,
    "Muthgasse_E2": 101,
    "Rennweg_EG": 21,
    "Rennweg_OG3": 14,
}


def _zaehle_raeume(plan: str) -> tuple[int, int]:
    """(Räume mit Polygon in ``raeume``, entfallene Räume mit Roh-Polygon)."""
    daten = json.loads((BASIS / plan / "raeume.json").read_text(encoding="utf-8"))
    lebend = sum(1 for e in daten["raeume"] if len(e.get("polygon_mm") or []) >= 3)
    weg = sum(1 for e in daten.get("entfallen", [])
              if len(e.get("polygon_roh") or []) >= 3)
    return lebend, weg


@pytest.mark.parametrize("plan", sorted(BAND_RAEUME))
def test_raeume_verschwinden_nicht(plan):
    """Gegenprobe zum Überlappungsband: die Raumzahl darf nicht sinken.

    Ohne diesen Test wäre der Riegel blind gegen den einfachsten Weg zu
    „0 Überlapper": Räume löschen. Er liest dieselbe Datei, aber die Anzahl.
    """
    if not BASIS.exists():  # pragma: no cover — Laufergebnisse fehlen
        pytest.skip(f"Laufergebnisse nicht vorhanden: {BASIS}")
    lebend, weg = _zaehle_raeume(plan)
    band = BAND_RAEUME[plan]
    assert lebend + weg >= band, (
        f"{plan}: {lebend} Räume + {weg} entfallen = {lebend + weg} gegen "
        f"Untergrenze {band}. Sinkt = Räume sind verschwunden (Entfall oder "
        "verlorene Erkennung) — Owner-Entscheidung, kein Nachziehen."
    )


def _messe(plan: str) -> tuple[int, float]:
    """(Anzahl Überlapper >5 %, doppelbelegte Fläche in m²) für einen Plan."""
    daten = json.loads((BASIS / plan / "raeume.json").read_text(encoding="utf-8"))
    geo = []
    for raum in daten["raeume"]:
        punkte = raum.get("polygon_mm") or []
        if len(punkte) < 3:
            continue
        poly = Polygon(punkte)
        if not poly.is_valid:
            poly = poly.buffer(0)
        if poly.is_empty or poly.area <= 0:
            continue
        geo.append(poly)

    baum = STRtree(geo)
    ueberlapper: set[int] = set()
    for i, a in enumerate(geo):
        for j in baum.query(a):
            j = int(j)
            if j <= i:
                continue
            inter = a.intersection(geo[j]).area
            if inter <= RAUSCHEN_MM2:
                continue
            if inter / a.area > SCHWELLE:
                ueberlapper.add(i)
            if inter / geo[j].area > SCHWELLE:
                ueberlapper.add(j)

    doppelt = (sum(g.area for g in geo) - unary_union(geo).area) / 1e6
    return len(ueberlapper), doppelt


@pytest.fixture(scope="module")
def messung() -> dict[str, tuple[int, float]]:
    if not BASIS.exists():  # pragma: no cover — Laufergebnisse fehlen
        pytest.skip(f"Laufergebnisse nicht vorhanden: {BASIS}")
    return {plan: _messe(plan) for plan in BAND}


@pytest.mark.parametrize("plan", sorted(BAND))
def test_ueberlapper_je_plan_steigt_nicht(plan, messung):
    ist, _ = messung[plan]
    band = BAND[plan][0]
    assert ist <= band, (
        f"{plan}: {ist} Überlapper >5 % gegen Band {band}. "
        "Steigt = Regression. Sinkt = Band im selben Commit nachziehen."
    )


@pytest.mark.parametrize("plan", sorted(BAND))
def test_doppelbelegte_flaeche_je_plan_steigt_nicht(plan, messung):
    _, ist = messung[plan]
    band = BAND[plan][1]
    assert ist <= band + TOLERANZ_M2, (
        f"{plan}: {ist:.1f} m² doppelbelegt gegen Band {band} m². "
        "Steigt = Regression. Sinkt = Band im selben Commit nachziehen."
    )


def test_summe_steigt_nicht(messung):
    anzahl = sum(a for a, _ in messung.values())
    flaeche = sum(f for _, f in messung.values())
    assert anzahl <= BAND_SUMME[0], f"{anzahl} Überlapper gesamt gegen Band {BAND_SUMME[0]}"
    assert flaeche <= BAND_SUMME[1] + TOLERANZ_M2, (
        f"{flaeche:.1f} m² doppelbelegt gesamt gegen Band {BAND_SUMME[1]} m²"
    )
