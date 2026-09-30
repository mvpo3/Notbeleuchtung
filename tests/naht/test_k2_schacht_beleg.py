"""Slice K2 auf Rennweg (docs/SLICES_K1_K4.md, K2): Schächte nur mit Beleg,
konsistent über die Geschosse.

Owner-Befund 2026-09-29: DG2 „Schacht 1,4" oben links ist die Fensternische
mit rotem Keil (Falschtreffer); OG2 hat 0 Schächte, obwohl Nachbargeschosse
dieselben Schächte tragen. Räume werden über ihre Lage gefunden, nicht über
die ID (Rest-IDs verschieben sich mit jeder Kaskaden-Änderung).
"""
from __future__ import annotations

import pytest
from shapely.geometry import Point, Polygon

from notbeleuchtung.raumerkennung.provider import ArchitekturRaumProvider
from notbeleuchtung.raumerkennung.schacht_abgleich import WARNUNG, gleiche_schaechte_ab
from plaene import (
    RENNWEG_DG1,
    RENNWEG_DG2,
    RENNWEG_EG,
    RENNWEG_OG1,
    RENNWEG_OG2,
    RENNWEG_OG3,
    RENNWEG_UG,
    plan,
)

# Geschosse von unten nach oben (Rang: geschoss_rang, DG1/DG2 über den Dateinamen).
GESCHOSSE = [("UG", RENNWEG_UG), ("EG", RENNWEG_EG), ("OG1", RENNWEG_OG1),
             ("OG2", RENNWEG_OG2), ("OG3", RENNWEG_OG3), ("DG1", RENNWEG_DG1),
             ("DG2", RENNWEG_DG2)]
NISCHE_DG2 = (12545233.0, 356225851.0)        # Basis de31621: `rest_5` SCHACHT 1,43 m²
LIFTSCHACHT_REST = (12549150.0, 356219200.0)  # S5c/F1: Kabine > 50 % → SCHACHT
DBA_SCHACHT = (12552000.0, 356216450.0)       # „DBA SCHACHT" + Keil im Kasten


@pytest.fixture(scope="module")
def modelle():
    return {name: ArchitekturRaumProvider().parse(str(plan(pfad)), name)
            for name, pfad in GESCHOSSE}


def _raum_an(modell, xy, typ=None):
    """Nächster Raum (≤ 300 mm) an ``xy``, optional nur vom Typ ``typ``."""
    pt = Point(xy)
    nah = [(Polygon(r.polygon_mm).buffer(0).distance(pt), r) for r in modell.raeume
           if len(r.polygon_mm) >= 3 and (typ is None or r.raum_typ == typ)]
    nah = [(d, r) for d, r in nah if d <= 300]
    return min(nah, key=lambda x: x[0])[1] if nah else None


def test_dg2_fensternische_ist_nische(modelle):
    r = _raum_an(modelle["DG2"], NISCHE_DG2)
    assert r is not None and 1.2 <= r.flaeche_m2 <= 1.6
    assert r.raum_typ == "NISCHE"
    assert r.nutzungsklasse is None          # fail-safe: nicht KEIN_RAUM


@pytest.mark.parametrize("geschoss", ["UG", "EG", "OG1", "DG1", "DG2"])
def test_liftschacht_reste_bleiben_schacht(modelle, geschoss):
    assert _raum_an(modelle[geschoss], LIFTSCHACHT_REST, "SCHACHT") is not None


@pytest.mark.parametrize("geschoss", ["OG3", "DG1", "DG2"])
def test_dba_schacht_bleibt_schacht(modelle, geschoss):
    assert _raum_an(modelle[geschoss], DBA_SCHACHT, "SCHACHT") is not None


def test_abgleich_meldet_luecken_und_erfindet_nichts(modelle):
    vorher = {g: [(r.id, r.raum_typ) for r in m.raeume] for g, m in modelle.items()}
    lagen = gleiche_schaechte_ab([(g, modelle[g].raeume) for g, _ in GESCHOSSE])
    assert {g: [(r.id, r.raum_typ) for r in m.raeume] for g, m in modelle.items()} == vorher

    lift = next(lg for lg in lagen
                if Point(lg.xy).distance(Point(LIFTSCHACHT_REST)) <= 300)
    assert list(lift.belegt) == ["UG", "EG", "OG1", "DG1", "DG2"]
    assert [w.split(" bei ")[0] for w in lift.warnungen] == [
        f"{WARNUNG}: OG2", f"{WARNUNG}: OG3"]
    dba = next(lg for lg in lagen if Point(lg.xy).distance(Point(DBA_SCHACHT)) <= 300)
    assert list(dba.belegt) == ["OG3", "DG1", "DG2"] and dba.warnungen == []
    # Die Fensternische nimmt am Abgleich nicht teil.
    assert not any(Point(lg.xy).distance(Point(NISCHE_DG2)) <= 300 for lg in lagen)
