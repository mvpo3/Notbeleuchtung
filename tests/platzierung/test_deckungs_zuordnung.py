"""deckungs_zuordnung — geometrische Fluchtweg-Deckung (füllt covers_segment)."""
from fakes import FakeNormProvider
from notbeleuchtung.hauptengine.contracts import (
    BBox,
    FluchtwegSegment,
    Platzierung,
    RaumModell,
    ZirkulationsGraph,
)
from notbeleuchtung.platzierung import deckungs_zuordnung


def _rz(x: float, y: float) -> Platzierung:
    return Platzierung(xy_mm=(x, y), catalog_key="notlicht_ks_stiege_unten", kind="rz",
                       richtung="unten", norm_quelle="q")


def _raum(*segmente: FluchtwegSegment) -> RaumModell:
    return RaumModell(
        floor="T", bounds_mm=BBox(min_xy=(0.0, 0.0), max_xy=(100000.0, 100000.0)),
        zirkulation=ZirkulationsGraph(segmente=list(segmente)),
    )


def test_segment_in_reichweite_wird_dem_naechsten_rz_zugeordnet():
    nah = FluchtwegSegment(segment_id="seg_nah", polyline_mm=[(1000.0, 0.0), (3000.0, 0.0)], reason="corner")
    fern = FluchtwegSegment(segment_id="seg_fern", polyline_mm=[(90000.0, 0.0), (92000.0, 0.0)], reason="corner")
    raum = _raum(nah, fern)
    # RZ bei (2000,0): ~1..2 m zum nahen Segment (< 30 m Radius), ~88 m zum fernen.
    out = deckungs_zuordnung.zuordnen([_rz(2000.0, 0.0)], raum, FakeNormProvider())
    assert out[0].covers_segment == ["seg_nah"]   # fern bleibt ungedeckt (> Erkennungsweite)


def test_nicht_rz_bleibt_unberuehrt_und_ohne_segmente_noop():
    sl = Platzierung(xy_mm=(2000.0, 0.0), catalog_key="sicherheitsleuchte_aufheller",
                     kind="sicherheitsleuchte", norm_quelle="q")
    raum = _raum(FluchtwegSegment(segment_id="s1", polyline_mm=[(2000.0, 0.0)], reason="corner"))
    # SL wird nie als Deckung gewertet.
    assert deckungs_zuordnung.zuordnen([sl], raum, FakeNormProvider())[0].covers_segment == []
    # Ohne Segmente: unveränderte Liste zurück.
    leer = _raum()
    rz = _rz(0.0, 0.0)
    assert deckungs_zuordnung.zuordnen([rz], leer, FakeNormProvider())[0] is rz


def test_z_fallunterscheidung_hinterleuchtet_doppelter_radius():
    # EN 1838 l=z·h: z=200 hinterleuchtet vs z=100 beleuchtet → doppelte Erkennungsweite.
    norm = FakeNormProvider()
    r_hinter = deckungs_zuordnung._radius_mm(norm, True)
    r_bel = deckungs_zuordnung._radius_mm(norm, False)
    assert r_hinter == 2 * r_bel                     # 30 m vs 15 m
    assert deckungs_zuordnung.HINTERLEUCHTET_DEFAULT is True


def test_mehrere_segmente_ein_rz_deckt_alle_in_reichweite():
    segs = [FluchtwegSegment(segment_id=f"s{i}", polyline_mm=[(i * 1000.0, 0.0)], reason="corner") for i in range(5)]
    out = deckungs_zuordnung.zuordnen([_rz(2000.0, 0.0)], _raum(*segs), FakeNormProvider())
    assert set(out[0].covers_segment) == {"s0", "s1", "s2", "s3", "s4"}
