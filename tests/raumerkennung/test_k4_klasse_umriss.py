"""K4 — Nutzungsklasse für UNBESTIMMTE GANG/VORRAUM aus dem Wohnungsumriss (Owner 2026-09-30).

Regel (Owner): „liegt ein GANG oder VORRAUM vollständig innerhalb eines
Wohnungsumrisses (top_n), ist er WOHNUNG_PRIVAT. Liegt er außerhalb jedes
Umrisses und ist vom Stiegenhaus ohne Wohnungseingang erreichbar, ist er
ALLGEMEIN_ERSCHLIESSUNG. Alles andere bleibt UNBESTIMMT mit Grund, Notlicht
bleibt."

Planer-Präzisierung: „vollständig innerhalb" = ≥ 98 % der Raumfläche im Umriss
(Außenkontur ohne Löcher von ``unary_union(Räume gleicher wohnung_id)
.buffer(+250).buffer(−250)``, Definition aus dem K1-Auftrag); ein Mitglied von
top_n liegt in top_n. Erreichbarkeit = Ankerregel auf ROHEN Türrollen, keine
Klasse. Die Regel setzt nur die Klasse; ``wohnung_id`` bleibt (Grundsatz (b)),
Notlicht entzieht weiter nur ``bestaetigt_privat``.
"""
from __future__ import annotations

import pytest

from notbeleuchtung.hauptengine.contracts.raum_modell import Raum, Tuer
from notbeleuchtung.raumerkennung.wohnungen import bilde_wohnungen
from notbeleuchtung.raumerkennung.wohnungsklasse import klasse_aus_umriss
from notbeleuchtung.raumerkennung.wohnungsumriss import anteile_im_umriss, wohnungsumrisse


def _q(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def _r(rid, typ, poly, wohnung=None, klasse=None):
    return Raum(id=rid, raum_typ=typ, polygon_mm=poly, wohnung_id=wohnung,
                nutzungsklasse=klasse, ist_fluchtweg=typ in ("GANG", "VORRAUM"),
                ist_communal=typ in ("GANG", "VORRAUM"))


def _t(tid, von, nach, detail=None):
    return Tuer(id=tid, xy_mm=(0.0, 0.0), von_raum=von, nach_raum=nach, tuer_detail=detail)


def _ring():
    """top_1 als Ring aus vier Zimmern um ein Feld 3 × 3 m (0..3000), Wände
    200 mm; das Feld selbst gehört keiner Wohnung."""
    return [_r("n", "ZIMMER", _q(-3200, 3200, 6200, 6200), "top_1", "WOHNUNG_PRIVAT"),
            _r("s", "ZIMMER", _q(-3200, -3200, 6200, -200), "top_1", "WOHNUNG_PRIVAT"),
            _r("w", "ZIMMER", _q(-3200, 0, -200, 3000), "top_1", "WOHNUNG_PRIVAT"),
            _r("o", "KÜCHE", _q(3200, 0, 6200, 3000), "top_1", "WOHNUNG_PRIVAT")]


# ── Umriss (gemeinsame Hilfsfunktion) ───────────────────────────────────────
def test_umriss_schliesst_waende_und_fuellt_loecher():
    u = wohnungsumrisse(_ring())["top_1"]
    assert u.geom_type == "Polygon"
    assert not u.interiors                          # ohne Löcher
    assert u.area == pytest.approx(9400 * 9400, rel=1e-3)


def test_mitglied_liegt_ganz_in_seiner_wohnung():
    ring = _ring()
    fern = _r("v", "VORRAUM", _q(50000, 0, 52000, 2000), "top_1")
    assert anteile_im_umriss(fern, wohnungsumrisse(ring)) == {"top_1": 1.0}


@pytest.mark.parametrize(("poly", "anteil"), [
    (_q(0, 0, 3000, 3000), 1.0),                    # das Feld im Ring
    (_q(1500, 0, 4500, 3000), 1.0),                 # reicht in die Küche: noch im Umriss
    (_q(4700, 0, 7700, 3000), 0.5),                 # halb über die Außenkante hinaus
    (_q(20000, 0, 23000, 3000), 0.0)])
def test_anteil_der_raumflaeche_im_umriss(poly, anteil):
    g = _r("g", "GANG", poly)
    assert anteile_im_umriss(g, wohnungsumrisse(_ring()))["top_1"] == pytest.approx(
        anteil, abs=1e-6)


# ── Regel ───────────────────────────────────────────────────────────────────
def test_unbestimmtes_mitglied_wird_privat():
    raeume = _ring() + [_r("v", "VORRAUM", _q(0, 0, 3000, 3000), "top_1")]
    k, grund = klasse_aus_umriss(raeume, [])["v"]
    assert k == "WOHNUNG_PRIVAT"
    assert "top_1" in grund and "Mitglied" in grund


def test_unbestimmt_ohne_wohnung_voll_im_umriss_wird_privat():
    raeume = _ring() + [_r("g", "GANG", _q(0, 0, 3000, 3000))]
    k, grund = klasse_aus_umriss(raeume, [])["g"]
    assert k == "WOHNUNG_PRIVAT"
    assert "top_1" in grund and "100 %" in grund


def _aussen(detail):
    """GANG g weit weg vom Ring, Tür zum Stiegenhaus mit roher Rolle ``detail``."""
    return (_ring() + [_r("g", "GANG", _q(20000, 0, 23000, 3000)),
                       _r("stgh", "STIEGENHAUS", _q(23200, 0, 26000, 3000), None,
                          "ALLGEMEIN_ERSCHLIESSUNG")],
            [_t("ts", "g", "stgh", detail)])


def test_ausserhalb_und_ohne_wohnungseingang_erreichbar_wird_allgemein():
    raeume, tueren = _aussen("stiegenhaustuer")
    k, grund = klasse_aus_umriss(raeume, tueren)["g"]
    assert k == "ALLGEMEIN_ERSCHLIESSUNG"
    assert "außerhalb jedes Wohnungsumrisses" in grund and "ts" in grund


@pytest.mark.parametrize("detail", ["wohnungseingang", None])
def test_ausserhalb_nur_ueber_wohnungseingang_oder_ohne_tuer_bleibt(detail):
    raeume, tueren = _aussen(detail)
    if detail is None:
        tueren = []                                 # vom Stiegenhaus gar nicht erreichbar
    k, grund = klasse_aus_umriss(raeume, tueren)["g"]
    assert k is None
    assert "Notlicht bleibt" in grund


def test_teilweise_im_umriss_bleibt_unbestimmt():
    """Weder vollständig innen (≥ 98 %) noch außerhalb: bleibt, mit Anteil."""
    raeume = _ring() + [_r("g", "GANG", _q(4700, 0, 7700, 3000)),
                        _r("stgh", "STIEGENHAUS", _q(7900, 0, 9000, 3000), None,
                           "ALLGEMEIN_ERSCHLIESSUNG")]
    k, grund = klasse_aus_umriss(raeume, [_t("ts", "g", "stgh", "stiegenhaustuer")])["g"]
    assert k is None
    assert "50 %" in grund and "top_1" in grund


def test_riegel_g3_geht_vor():
    """G3 (Owner 2026-09-22): „in keinem Schritt PRIVAT" — auch nicht in K4.
    Ein Mitglied mit Tür ins Freie bleibt unbestimmt, Notlicht bleibt
    (gefunden von ``test_k4_zufallssuche``, Topologie 136; auf den 23
    Prüfgeschossen 4 Räume, z. B. Mollgasse 4.OG ``raum_10``)."""
    raeume = _ring() + [_r("v", "VORRAUM", _q(0, 0, 3000, 3000), "top_1")]
    k, grund = klasse_aus_umriss(raeume, [_t("ta", "v", "AUSSEN")])["v"]
    assert k is None
    assert "Riegel (G3)" in grund and "Notlicht bleibt" in grund


def test_liest_keine_klasse_der_nachbarn():
    """Erreichbarkeit über rohe Rollen (Ankerregel), keine Klasse: andere
    Nachbarklassen ändern das Urteil nicht."""
    raeume, tueren = _aussen("stiegenhaustuer")
    vorher = klasse_aus_umriss(raeume, tueren)
    for r in raeume:
        if r.id != "g":
            r.nutzungsklasse = None
    assert klasse_aus_umriss(raeume, tueren) == vorher


def test_nur_unbestimmte_gang_und_vorraum():
    raeume = _ring() + [_r("g", "GANG", _q(0, 0, 3000, 3000), None, "ALLGEMEIN_ERSCHLIESSUNG"),
                        _r("x", "", _q(0, 0, 1000, 1000))]
    assert klasse_aus_umriss(raeume, []) == {}


def test_setzt_nichts():
    raeume = _ring() + [_r("v", "VORRAUM", _q(0, 0, 3000, 3000), "top_1")]
    klasse_aus_umriss(raeume, [])
    assert raeume[-1].nutzungsklasse is None and raeume[-1].wohnung_id == "top_1"


# ── im Durchlauf: bilde_wohnungen ───────────────────────────────────────────
def _loch_vorraum():
    """VORRAUM v hinter einer rohen Zimmertür an Zimmer z und Bad b, vom
    Stiegenhaus über KEINE Tür erreichbar (Loch, Messfall S4c/S3b); Wohnung
    {b, v, z} aus rohen Türen, bisher Klasse offen."""
    raeume = [_r("v", "VORRAUM", _q(0, 0, 2000, 3000)),
              _r("z", "ZIMMER", _q(2200, 0, 6000, 3000)),
              _r("b", "BAD", _q(0, 3200, 2000, 5000)),
              _r("stgh", "STIEGENHAUS", _q(-3000, 0, -200, 3000))]
    tueren = [_t("tz", "v", "z", "zimmertuer"), _t("tb", "v", "b", "zimmertuer")]
    return raeume, tueren


def test_loch_vorraum_in_seiner_wohnung_wird_privat_und_behaelt_notlicht():
    raeume, tueren = _loch_vorraum()
    warnungen: list[str] = []
    bilde_wohnungen(raeume, tueren, warnungen)
    v = raeume[0]
    assert v.nutzungsklasse == "WOHNUNG_PRIVAT"
    assert v.wohnung_id == raeume[1].wohnung_id == raeume[2].wohnung_id is not None
    # Ankerregel „über keine Tür erreichbar" bestätigt nicht → kein Entzug.
    assert (v.ist_fluchtweg, v.ist_communal) == (True, True)
    k4 = [w for w in warnungen if w.startswith("k4: v — privat")]
    assert len(k4) == 1, warnungen
    assert "vorher unbestimmt" in k4[0]
    assert not [w for w in warnungen if w.startswith("unbestimmt: v — ")], warnungen


def test_wohnung_bleibt_wie_ohne_k4():
    """Grundsatz (b): K4 setzt nur die Klasse — Wohnungen und ihre Eingänge
    sind dieselben wie aus rohen Türen."""
    raeume, tueren = _loch_vorraum()
    wohnungen = bilde_wohnungen(raeume, tueren)
    assert [(w.raum_ids, w.eingangs_tuer_ids) for w in wohnungen] == [(["b", "v", "z"], [])]
