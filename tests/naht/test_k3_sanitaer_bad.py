"""K3 an echten Plänen — Bad und WC aus Sanitärbeleg (Enis Referenz 07).

Owner-Befund: Rennweg OG3 „UNBEKANNT 6,6 m²" links hat zwei Waschbecken und
WC-Symbole (dazu eine Dusche), liegt im Umriss von top_2, kein Stempel — er
wird BAD. Mollgasse 2.OG und 3.OG tragen dieselbe Nasszelle (Waschtisch +
Badewanne) in einem stempellosen Rest-Raum: im 2.OG liegt sie im Umriss von
``top_13`` (BAD), im 3.OG grenzt sie an einen Gang ohne Wohnung und bleibt
UNBEKANNT (Kontrolle greift).

Die Typisierung ist ein Vorlauf ohne Rückkopplung: der Wohnungsumriss kommt
aus einer Probe, danach läuft EIN regulärer Durchlauf mit dem neuen Typ — die
Wohnung des Bades folgt dort rohen Türen (Grundsatz (b), 2026-09-22).
"""
import pytest
from shapely.geometry import Point, Polygon

from plaene import MOLLGASSE_2OG, MOLLGASSE_3OG, RENNWEG_OG3, plan

# Ein Punkt je Raum (representative_point der Basis-Polygone auf de31621).
OG3_REST_6 = (12543873.0, 356220728.0)
MOLL_2OG_REST_4 = (2757780.0, 1535433.0)
MOLL_3OG_REST_2 = (2481312.0, 1385961.0)


def _parse(pfad):
    from notbeleuchtung.raumerkennung import ArchitekturRaumProvider

    p = ArchitekturRaumProvider()
    return p, p.parse(str(plan(pfad)), "")


def _raum_an(m, xy):
    treffer = [r for r in m.raeume if len(r.polygon_mm) >= 3
               and Polygon(r.polygon_mm).buffer(0).contains(Point(xy))]
    assert len(treffer) == 1, [r.id for r in treffer]
    return treffer[0]


@pytest.fixture(scope="module")
def og3():
    return _parse(RENNWEG_OG3)


@pytest.fixture(scope="module")
def moll_2og():
    return _parse(MOLLGASSE_2OG)


@pytest.fixture(scope="module")
def moll_3og():
    return _parse(MOLLGASSE_3OG)


def test_og3_raum_6_6_wird_bad(og3):
    prov, m = og3
    r = _raum_an(m, OG3_REST_6)
    assert r.raum_typ == "BAD"
    assert 6.3 <= r.flaeche_m2 <= 6.9
    assert r.nutzungsklasse == "WOHNUNG_PRIVAT"
    assert (r.ist_fluchtweg, r.ist_communal) == (False, False)
    # Die Wohnung kommt aus rohen Türen im regulären Lauf, nicht aus dem Umriss.
    assert r.wohnung_id == "top_2"
    assert any(z.startswith(f"{r.id}: BAD") and "top_2" in z for z in prov.sanitaer_befund)


def test_og3_tueren_des_bades_haben_eine_rolle(og3):
    """Ein regulärer Durchlauf mit dem neuen Typ: die rohen Türrollen sehen
    das Bad wie ein gestempeltes (vorher beide Rolle None)."""
    _, m = og3
    r = _raum_an(m, OG3_REST_6)
    rollen = [t.tuer_detail for t in m.tueren if r.id in (t.von_raum, t.nach_raum)]
    assert len(rollen) == 2
    assert None not in rollen


def test_mollgasse_2og_nasszelle_wird_bad(moll_2og):
    _, m = moll_2og
    r = _raum_an(m, MOLL_2OG_REST_4)
    assert (r.raum_typ, r.nutzungsklasse, r.wohnung_id) == ("BAD", "WOHNUNG_PRIVAT", "top_13")


def test_mollgasse_3og_nasszelle_ausserhalb_bleibt_unbekannt(moll_3og):
    prov, m = moll_3og
    r = _raum_an(m, MOLL_3OG_REST_2)
    assert r.raum_typ == ""
    assert r.nutzungsklasse is None and r.wohnung_id is None
    assert any(z.startswith(f"{r.id}: bleibt UNBEKANNT") for z in prov.sanitaer_befund)


@pytest.mark.parametrize("fixture", ["og3", "moll_2og", "moll_3og"])
def test_kein_sanitaer_raum_ausserhalb_einer_wohnung(fixture, request):
    """Jeder aus Sanitärbeleg typisierte Raum liegt nachher in einer Wohnung —
    derselben, deren Umriss ihn in der Probe umschloss."""
    prov, m = request.getfixturevalue(fixture)
    wohnung = {r.id: r.wohnung_id for r in m.raeume}
    for zeile in prov.sanitaer_befund:
        rid, rest = zeile.split(": ", 1)
        if "bleibt UNBEKANNT" in rest:
            continue
        umriss = rest.split("im Umriss ", 1)[1].split()[0]
        assert wohnung[rid] == umriss, zeile
