"""K4 an echten Plänen — Nutzungsklasse für UNBESTIMMTE Gänge und Vorräume.

Owner-Befund (2026-09-30): Rennweg DG1 Gang 12,2, DG2 Vorraum 10,8 (Stempel
Garderobe), OG3 Gang 9,4 sind magenta schraffiert, Klasse offen. Alle drei
liegen nach rohen Türen in ``top_1``: DG1/DG2 nur durch eine blattlose Öffnung
vom Stiegenhaus getrennt (Ankerregel nicht auswertbar), OG3 der R1-Wohnungsflur
hinter der Stiegenhaustür. Nach K4 haben DG1/DG2 eine Klasse; Wohnung und
Notlicht (Flags 11 — die Ankerregel bestätigt keinen von ihnen) bleiben.

Owner 2026-09-30 (K4-Nachzug), R1-Aussetzung: für den nach R1 (Fassung A+C)
gebundenen Wohnungsflur setzt K4 keine Klasse — OG3 Gang 9,4 bleibt offen mit
Grund „R1-Flur, Owner 2026-09-30", Notlicht bleibt, Gate (6) bleibt grün.
"""
import pytest
from shapely.geometry import Point, Polygon

from plaene import RENNWEG_DG1, RENNWEG_DG2, RENNWEG_OG3, plan

# Ein Punkt je Raum (representative_point der Basis-Polygone auf f682c77).
FAELLE = [
    pytest.param(RENNWEG_DG1, (12546168.0, 356220346.0), "GANG", 12.19, id="DG1-gang-12,2"),
    pytest.param(RENNWEG_DG2, (12543649.0, 356220029.0), "VORRAUM", 10.84,
                 id="DG2-vorraum-10,8"),
]
OG3_GANG = (12553336.0, 356215229.0)


def _parse(pfad):
    from notbeleuchtung.raumerkennung import ArchitekturRaumProvider

    p = ArchitekturRaumProvider()
    return p, p.parse(str(plan(pfad)), "")


def _raum_an(m, xy):
    treffer = [r for r in m.raeume if len(r.polygon_mm) >= 3
               and Polygon(r.polygon_mm).buffer(0).contains(Point(xy))]
    assert len(treffer) == 1, [r.id for r in treffer]
    return treffer[0]


@pytest.mark.parametrize(("pfad", "xy", "typ", "m2"), FAELLE)
def test_owner_raum_bekommt_eine_klasse(pfad, xy, typ, m2):
    prov, m = _parse(pfad)
    r = _raum_an(m, xy)
    assert r.raum_typ == typ
    assert r.flaeche_m2 == pytest.approx(m2, abs=0.05)
    assert r.nutzungsklasse is not None, [w for w in prov.wohnungsklasse_warnungen
                                          if r.id in w]
    assert r.nutzungsklasse == "WOHNUNG_PRIVAT"
    # Grundsatz (b): die Wohnung kommt aus rohen Türen, K4 ändert sie nicht.
    assert r.wohnung_id == "top_1"
    # Notlicht bleibt: die Ankerregel bestätigt keinen der drei privat.
    assert (r.ist_fluchtweg, r.ist_communal) == (True, True)
    assert [w for w in prov.wohnungsklasse_warnungen
            if w.startswith(f"k4: {r.id} — privat")], prov.wohnungsklasse_warnungen


def test_og3_r1_flur_bleibt_offen():
    """R1-Aussetzung (Owner 2026-09-30): OG3 Gang 9,38 m² (``raum_10``, R1-Flur
    hinter ``tuer_5``) bekommt von K4 keine Klasse, Wohnung ``top_1`` und
    Flags 11 bleiben; der Grund steht in der ``k4:``-Zeile, der R1-Grund der
    Iteration in der ``unbestimmt:``-Zeile."""
    prov, m = _parse(RENNWEG_OG3)
    r = _raum_an(m, OG3_GANG)
    assert (r.raum_typ, r.flaeche_m2) == ("GANG", pytest.approx(9.38, abs=0.05))
    assert r.nutzungsklasse is None, r.nutzungsklasse
    assert r.wohnung_id == "top_1"
    assert (r.ist_fluchtweg, r.ist_communal) == (True, True)
    warn = prov.wohnungsklasse_warnungen
    assert [w for w in warn
            if w.startswith(f"k4: {r.id} — offen: R1-Flur, Owner 2026-09-30")], warn
    assert [w for w in warn if w.startswith(f"unbestimmt: {r.id} — R1: Wohnungsflur")], warn
