"""Punkt 2d — freie Fläche im Wohnungsumriss (Owner 2026-09-30), synthetisch.

„Innerhalb eines Wohnungsumrisses gibt es keine freie Fläche ohne Raum":
Öffnung ohne Türblatt → die Fläche geht in den Nachbarraum (die breiteste
entscheidet, nicht eindeutig → eigener Raum); Tür mit Blatt → eigener Raum
UNBEKANNT ohne Wohnung. Außerhalb eines Wohnungsumrisses bleibt alles frei.
Echter Plan: ``tests/naht/test_freiflaeche_wohnung.py`` (Rennweg DG1).
"""
from __future__ import annotations

import pytest
from shapely.geometry import box

from notbeleuchtung.hauptengine.contracts.raum_modell import Raum, Tuer
from notbeleuchtung.raumerkennung.freiflaeche import fuelle_freie_flaechen


def _raum(rid, geom, typ="ZIMMER", wid="top_1", klasse="WOHNUNG_PRIVAT"):
    return Raum(id=rid, raum_typ=typ, polygon_mm=list(geom.exterior.coords)[:-1],
                flaeche_m2=geom.area / 1e6, nutzungsklasse=klasse, wohnung_id=wid)


def test_oeffnung_ohne_tuerblatt_geht_in_den_raum():
    a = _raum("a", box(0, 0, 8000, 3000), "WOHNZIMMER")
    raeume = [a]
    befund = fuelle_freie_flaechen(raeume, [], box(0, 0, 8000, 6000), None)
    assert [r.id for r in raeume] == ["a"]
    assert a.flaeche_m2 == pytest.approx(48.0, abs=0.01)
    assert (a.raum_typ, a.wohnung_id, a.nutzungsklasse) == ("WOHNZIMMER", "top_1", "WOHNUNG_PRIVAT")
    assert len(befund) == 1 and "→ a WOHNZIMMER 24.00 → 48.00 m²" in befund[0], befund


def test_tuer_mit_blatt_trennt_eigener_raum_ohne_wohnung():
    a = _raum("a", box(0, 0, 8000, 3000))
    wand = box(0, 3000, 3000, 3200).union(box(3900, 3000, 8000, 3200))
    tuer = Tuer(id="tuer_1", xy_mm=(3450.0, 3100.0), von_raum="a", nach_raum="KEIN_RAUM")
    raeume = [a]
    befund = fuelle_freie_flaechen(raeume, [tuer], box(0, 0, 8000, 6000), wand)
    assert a.flaeche_m2 == pytest.approx(24.0)
    neu = [r for r in raeume if r.id != "a"]
    assert len(neu) == 1, befund
    r = neu[0]
    assert (r.id, r.raum_typ, r.wohnung_id, r.nutzungsklasse) == ("frei_1", "", None, None)
    assert (r.ist_fluchtweg, r.ist_communal) == (False, False)
    assert r.flaeche_m2 == pytest.approx(8.0 * 2.8 + 0.9 * 0.2, abs=0.01)
    assert "neuer Raum frei_1 UNBEKANNT" in befund[0] and "tuer_1 a|KEIN_RAUM" in befund[0], befund


def test_zwei_gleich_breite_oeffnungen_nicht_eindeutig():
    raeume = [_raum("a", box(0, 0, 4000, 3000)), _raum("b", box(4000, 0, 8000, 3000))]
    befund = fuelle_freie_flaechen(raeume, [], box(0, 0, 8000, 6000), None)
    assert [r.flaeche_m2 for r in raeume[:2]] == [pytest.approx(12.0), pytest.approx(12.0)]
    assert [r.id for r in raeume[2:]] == ["frei_1"]
    assert "nicht eindeutig" in befund[0], befund


def test_ausserhalb_des_wohnungsumrisses_bleibt_frei():
    """Nachbar Erschließung (ohne Wohnung) → nicht im Umriss einer Wohnung."""
    raeume = [_raum("a", box(0, 0, 8000, 3000)),
              _raum("g", box(0, 6000, 8000, 9000), "GANG", None, "ALLGEMEIN_ERSCHLIESSUNG")]
    befund = fuelle_freie_flaechen(raeume, [], box(0, 0, 8000, 9000), None)
    assert befund == []
    assert [(r.id, r.flaeche_m2) for r in raeume] == [("a", 24.0), ("g", 24.0)]
