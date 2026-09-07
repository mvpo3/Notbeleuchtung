"""wohnungen — Zusammenhang über zimmertuer-Kanten + Gang-Verfeinerung."""
from __future__ import annotations

from notbeleuchtung.hauptengine.contracts.raum_modell import Raum, Tuer
from notbeleuchtung.raumerkennung.wohnungen import bilde_wohnungen


def _tuer(tid, von, nach, detail=None):
    return Tuer(id=tid, xy_mm=(0.0, 0.0), von_raum=von, nach_raum=nach,
                tuer_detail=detail)


def test_zwei_wohnungen_getrennt():
    raeume = [Raum(id=r, raum_typ="ZIMMER") for r in ("a1", "a2", "b1")]
    raeume.append(Raum(id="gang", raum_typ="GANG"))
    raeume.append(Raum(id="stgh", raum_typ="STIEGENHAUS"))
    tueren = [
        _tuer("t1", "a1", "a2", "zimmertuer"),
        _tuer("t2", "gang", "a1", "wohnungseingang"),
        _tuer("t3", "gang", "b1", "wohnungseingang"),
        _tuer("t4", "gang", "stgh", "stiegenhaustuer"),
    ]
    wohnungen = bilde_wohnungen(raeume, tueren)
    assert [w.id for w in wohnungen] == ["top_1", "top_2"]
    by_id = {r.id: r for r in raeume}
    assert by_id["a1"].wohnung_id == by_id["a2"].wohnung_id
    assert by_id["b1"].wohnung_id != by_id["a1"].wohnung_id
    assert by_id["gang"].wohnung_id is None
    top1 = next(w for w in wohnungen if "a1" in w.raum_ids)
    assert top1.eingangs_tuer_ids == ["t2"]


def test_wohnungs_flur_wird_privat():
    """VORRAUM nur an Zimmer/Bad, keine Tür in STIEGENHAUS/AUSSEN → privat."""
    raeume = [
        Raum(id="vor", raum_typ="VORRAUM"),
        Raum(id="zi", raum_typ="ZIMMER"),
        Raum(id="bad", raum_typ="BAD"),
    ]
    tueren = [_tuer("t1", "vor", "zi", "wohnungseingang"),
              _tuer("t2", "vor", "bad", "wohnungseingang")]
    wohnungen = bilde_wohnungen(raeume, tueren)
    assert raeume[0].nutzungsklasse == "WOHNUNG_PRIVAT"
    assert len(wohnungen) == 1
    assert set(wohnungen[0].raum_ids) == {"vor", "zi", "bad"}
    # Türen des privaten Flurs sind zu zimmertueren korrigiert worden.
    assert all(t.tuer_detail == "zimmertuer" for t in tueren)


def test_flur_mit_stiegenhaustuer_bleibt_erschliessung():
    raeume = [Raum(id="vor", raum_typ="VORRAUM"),
              Raum(id="zi", raum_typ="ZIMMER"),
              Raum(id="stgh", raum_typ="STIEGENHAUS")]
    tueren = [_tuer("t1", "vor", "zi", "wohnungseingang"),
              _tuer("t2", "vor", "stgh", "stiegenhaustuer")]
    bilde_wohnungen(raeume, tueren)
    assert raeume[0].nutzungsklasse == "ALLGEMEIN_ERSCHLIESSUNG"
