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

from plaene import MOLLGASSE_3OG, MOLLGASSE_DG, RENNWEG_DG1, RENNWEG_DG2, RENNWEG_OG3, plan

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


# ── Punkt 2c (LUECKEN.md § 14): korrigierte Rollen am K4-privaten Loch-Raum ──
#: Belegte Fälle aus der Aufschlüsselung der 270 gekippten Rollen (Tür-Lage und
#: ein Punkt im Loch-Raum, Stand 2016268): Innentür des Loch-Raums zu einem Zimmer
#: derselben Wohnung (rohe Türen), vor K4 korrigiert ``zimmertuer``, nach K4
#: ``wohnungseingang`` (Option W zählte den unbestätigt privaten Loch-Raum als
#: Erschließung).
LOCH_INNENTUEREN = [
    pytest.param(MOLLGASSE_DG, (2925051.1, 1670875.8), (2923849.0, 1668943.0), "VORRAUM",
                 "zimmertuer", id="moll-dg-tuer_12-vorraum-zimmer"),
    pytest.param(MOLLGASSE_DG, (2924781.1, 1685260.8), (2923392.0, 1684999.0), "GANG",
                 "wohnungseingang", id="moll-dg-tuer_6-r1-gang-zimmer"),
    pytest.param(MOLLGASSE_3OG, (2460319.2, 1406104.0), (2458480.0, 1406311.0), "GANG",
                 "wohnungseingang", id="moll-3og-tuer_43-r1-gang-zimmer"),
]


@pytest.mark.parametrize(("pfad", "tuer_xy", "loch_xy", "loch_typ", "roh"), LOCH_INNENTUEREN)
def test_k4_loch_raum_innentuer_bleibt_zimmertuer(pfad, tuer_xy, loch_xy, loch_typ, roh):
    """S7c: Zimmertür innerhalb einer Wohnung. Der Loch-Raum ist K4-privat und
    unbestätigt (Notlicht bleibt, Flags 11), gehört aber nach rohen Türen zur
    Wohnung des Zimmers — seine Innentür bleibt korrigiert ``zimmertuer``, wie
    vor K4. Die rohe Rolle bleibt unverändert."""
    import math

    from notbeleuchtung.raumerkennung import wohnungsklasse as wk

    _, m = _parse(pfad)
    loch = _raum_an(m, loch_xy)
    assert loch.raum_typ == loch_typ
    assert loch.id in wk.loch_raeume(m.raeume, m.tueren), "Vorbedingung: Loch-Raum"
    assert loch.nutzungsklasse == "WOHNUNG_PRIVAT", "Vorbedingung: K4 privat"
    assert loch.id not in wk.bestaetigt_privat(m.raeume, m.tueren)
    assert (loch.ist_fluchtweg, loch.ist_communal) == (True, True)
    t = min(m.tueren, key=lambda t: math.dist(t.xy_mm, tuer_xy))
    assert math.dist(t.xy_mm, tuer_xy) < 50, (t.id, t.xy_mm)
    assert loch.id in (t.von_raum, t.nach_raum), (t.id, t.von_raum, t.nach_raum)
    zimmer = next(r for r in m.raeume
                  if r.id in (t.von_raum, t.nach_raum) and r.id != loch.id)
    assert zimmer.raum_typ == "ZIMMER"
    assert zimmer.wohnung_id == loch.wohnung_id is not None
    assert t.tuer_detail == roh
    assert wk.korrigierte_rollen(m.raeume, m.tueren)[t.id] == "zimmertuer", t.id
