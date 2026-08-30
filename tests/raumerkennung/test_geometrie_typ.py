"""geometrie_typ — STIEGENHAUS aus Treppen-Blöcken (Typisierung ohne Text-Label)."""
from notbeleuchtung.hauptengine.contracts.raum_modell import Raum
from notbeleuchtung.raumerkennung.dxf_load import lade_dxf
from notbeleuchtung.raumerkennung.geometrie_typ import (
    stiege_rechtecke,
    typisiere_geometrisch,
    typisiere_stiegenhaus,
)


def _raum(rid: str, poly: list[tuple[float, float]], typ: str = "") -> Raum:
    return Raum(id=rid, raum_typ=typ, polygon_mm=poly, flaeche_m2=0.0)


_QUAD = [(0.0, 0.0), (5000.0, 0.0), (5000.0, 5000.0), (0.0, 5000.0)]      # 25 m²
_STAIR = ([(1000.0, 1000.0), (3000.0, 1000.0), (3000.0, 3000.0), (1000.0, 3000.0)],
          (2000.0, 2000.0), 4.0)


def test_stiege_in_echtem_raum_typisiert_diesen():
    r = _raum("a", _QUAD)
    out = typisiere_stiegenhaus([r], [_STAIR])
    assert len(out) == 1                      # kein zusätzlicher Raum
    assert out[0].raum_typ == "STIEGENHAUS"
    assert out[0].ist_fluchtweg and out[0].ist_communal


def test_stiege_ohne_raum_legt_stiegenhaus_an():
    rect = [(0.0, 0.0), (4800.0, 0.0), (4800.0, 1200.0), (0.0, 1200.0)]
    out = typisiere_stiegenhaus([], [(rect, (2400.0, 600.0), 5.8)])
    assert len(out) == 1
    assert out[0].raum_typ == "STIEGENHAUS"
    assert out[0].flaeche_m2 == 5.8


def test_bereits_typisierter_raum_bleibt_unangetastet():
    r = _raum("a", _QUAD, typ="WOHNZIMMER")
    out = typisiere_stiegenhaus([r], [_STAIR])
    assert len(out) == 1                      # Anker in bestehendem Raum → kein Dup
    assert out[0].raum_typ == "WOHNZIMMER"


def test_fragment_wird_nicht_typisiert_sondern_raum_angelegt():
    # 0.25 m² Fragment deckt den Anker, ist aber zu klein für „echten" Raum.
    frag = _raum("f", [(0.0, 0.0), (500.0, 0.0), (500.0, 500.0), (0.0, 500.0)])
    stair = ([(0.0, 0.0), (1000.0, 0.0), (1000.0, 1000.0), (0.0, 1000.0)], (250.0, 250.0), 1.0)
    out = typisiere_stiegenhaus([frag], [stair])
    assert frag.raum_typ == ""               # Fragment bleibt untypisiert
    assert len(out) == 2 and any(r.raum_typ == "STIEGENHAUS" for r in out)


def test_stiege_rechtecke_mollgasse_echt(mollgasse_blank_eg):
    plan = lade_dxf(str(mollgasse_blank_eg))
    rects = stiege_rechtecke(plan)
    assert len(rects) >= 1                    # Mollgasse-EG hat STIEGE-Blöcke
    for _poly, _center, area in rects:
        assert 1.0 <= area <= 30.0            # plausible Treppen-Grundfläche


def test_typisiere_geometrisch_liefert_stiegenhaus_auf_mollgasse(mollgasse_blank_eg):
    # DoD ①: label-loser Plan → trotzdem ≥1 typisierter STIEGENHAUS.
    plan = lade_dxf(str(mollgasse_blank_eg))
    out = typisiere_geometrisch(plan, [])
    assert any(r.raum_typ == "STIEGENHAUS" for r in out)


def test_provider_parse_mollgasse_hat_typisierte_raeume(mollgasse_blank_eg):
    # DoD ① end-to-end: ArchitekturRaumProvider.parse liefert gefüllte raum_typ,
    # obwohl der Plan keine Raum-Text-Labels trägt.
    from notbeleuchtung.raumerkennung.provider import ArchitekturRaumProvider

    raum = ArchitekturRaumProvider().parse(str(mollgasse_blank_eg), "EG")
    typisiert = [r for r in raum.raeume if (r.raum_typ or "").strip()]
    assert typisiert, "Mollgasse-parse muss ≥1 typisierten Raum liefern"
    assert any(r.raum_typ == "STIEGENHAUS" for r in typisiert)
