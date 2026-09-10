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
BAND: dict[str, tuple[int, float]] = {
    # Plan: (Überlapper >5 %, doppelbelegte Fläche in m²)
    "Barawitzka_EG": (9, 42.3),
    "Mollgasse_EG": (16, 45.8),
    "Muthgasse_E2": (37, 174.2),
    "Rennweg_EG": (0, 0.0),
    "Rennweg_OG3": (0, 0.0),
}
BAND_SUMME = (62, 262.3)
TOLERANZ_M2 = 0.05  # Rundung der Bänder auf 0,1 m²


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
