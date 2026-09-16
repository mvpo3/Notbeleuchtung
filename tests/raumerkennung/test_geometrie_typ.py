"""geometrie_typ — STIEGENHAUS aus Treppen-Blöcken (Typisierung ohne Text-Label)."""
import ezdxf
import pytest
from shapely.affinity import rotate, translate
from shapely.geometry import Point, Polygon, box
from shapely.ops import unary_union

from notbeleuchtung.hauptengine.contracts.raum_modell import Raum
from notbeleuchtung.raumerkennung.dxf_load import lade_dxf
from notbeleuchtung.raumerkennung.geometrie_typ import (
    gang_polygone,
    stiege_rechtecke,
    typisiere_gang,
    typisiere_geometrisch,
    typisiere_stiegenhaus,
)


def _raum(rid: str, poly: list[tuple[float, float]], typ: str = "") -> Raum:
    return Raum(id=rid, raum_typ=typ, polygon_mm=poly, flaeche_m2=0.0)


_QUAD = [(0.0, 0.0), (5000.0, 0.0), (5000.0, 5000.0), (0.0, 5000.0)]      # 25 m²
_STAIR = ((2000.0, 2000.0), box(1000.0, 1000.0, 3000.0, 3000.0))          # Anker + Hülle 4 m²


def test_stiege_in_echtem_raum_typisiert_diesen():
    r = _raum("a", _QUAD)
    out = typisiere_stiegenhaus([r], [_STAIR])
    assert len(out) == 1                      # kein zusätzlicher Raum
    assert out[0].raum_typ == "STIEGENHAUS"
    assert out[0].ist_fluchtweg and out[0].ist_communal


def test_stiege_ohne_raum_legt_stiegenhaus_an():
    out = typisiere_stiegenhaus([], [((2400.0, 600.0), box(0.0, 0.0, 4800.0, 1200.0))])
    assert len(out) == 1
    assert out[0].raum_typ == "STIEGENHAUS"
    assert out[0].flaeche_m2 == pytest.approx(5.76)    # Fläche der Hülle selbst


def test_bereits_typisierter_raum_bleibt_unangetastet():
    r = _raum("a", _QUAD, typ="WOHNZIMMER")
    out = typisiere_stiegenhaus([r], [_STAIR])
    assert len(out) == 1                      # Anker in bestehendem Raum → kein Dup
    assert out[0].raum_typ == "WOHNZIMMER"


def test_fragment_wird_nicht_typisiert_sondern_raum_angelegt():
    # 0.25 m² Fragment deckt den Anker, ist aber zu klein für „echten" Raum.
    frag = _raum("f", [(0.0, 0.0), (500.0, 0.0), (500.0, 500.0), (0.0, 500.0)])
    stair = ((250.0, 250.0), box(0.0, 0.0, 1000.0, 1000.0))
    out = typisiere_stiegenhaus([frag], [stair])
    assert frag.raum_typ == ""               # Fragment bleibt untypisiert
    assert len(out) == 2 and any(r.raum_typ == "STIEGENHAUS" for r in out)
    assert out[-1].flaeche_m2 == pytest.approx(0.75)   # Hülle ohne das gedeckte Fragment


# Diagnose Rennweg U1, Slice S9: gedrehte Treppe (Muster DG2 `Stair_2`), deren
# Achs-Bbox-Mitte in einer Wand liegt.
_WAND = "02-TWA-G00-LEG-M0"
_TREPPE_XY, _TREPPE_GRAD = (8000.0, 3000.0), 30.0
_TREPPE_L, _TREPPE_B = 3000.0, 1200.0            # Lauflänge × Laufbreite (mm), 3,6 m²


def _im_treppenraster(x0, y0, x1, y1):
    """Rechteck im Koordinatensystem des Treppen-Blocks → Weltlage (30° gedreht, mm)."""
    return translate(rotate(box(x0, y0, x1, y1), _TREPPE_GRAD, origin=(0, 0)), *_TREPPE_XY)


def _raum_aus(rid: str, poly: Polygon) -> Raum:
    return _raum(rid, [(x, y) for x, y in poly.exterior.coords[:-1]])


def _doc_mit_wand():
    """Mini-DXF-Dokument (mm) mit Außenwand-Rechteck 20 × 12 m."""
    doc = ezdxf.new(setup=True)
    doc.header["$INSUNITS"] = 4                      # mm
    doc.layers.add(_WAND)
    ecken = [(0, 0), (20000, 0), (20000, 12000), (0, 12000)]
    for i in range(4):
        doc.modelspace().add_line(ecken[i], ecken[(i + 1) % 4], dxfattribs={"layer": _WAND})
    return doc


def _stair_block(doc, name: str = "Stair_2") -> str:
    """Treppen-Blockdefinition 3,0 × 1,2 m: Umriss + Stufenlinien."""
    blk = doc.blocks.new(name)
    blk.add_lwpolyline([(0, 0), (_TREPPE_L, 0), (_TREPPE_L, _TREPPE_B), (0, _TREPPE_B)], close=True)
    for x in range(250, int(_TREPPE_L), 250):
        blk.add_line((x, 0), (x, _TREPPE_B))
    return name


def _geladen(doc, tmp_path, name: str):
    pfad = tmp_path / f"{name}.dxf"
    doc.saveas(str(pfad))
    return lade_dxf(pfad)


def _gedrehte_treppe(tmp_path):
    """Mini-DXF (mm): Wandrechteck, Treppen-Block 3,0 × 1,2 m (Umriss + Stufen), 30° gedreht."""
    doc = _doc_mit_wand()
    doc.modelspace().add_blockref(_stair_block(doc), _TREPPE_XY,
                                  dxfattribs={"rotation": _TREPPE_GRAD})
    return _geladen(doc, tmp_path, "treppe_gedreht")


def test_gedrehte_treppe_huelle_gedeckt_haengt_nicht_an(tmp_path):
    """Räume längs der gedrehten Treppe, 150-mm-Wand durch die Bbox-Mitte.

    Trennt Hülle von Achs-Bbox (Reviewbefund S9): die Räume decken die gedrehte
    Hülle zu 0,875 (über der Schwelle → kein Anhang), die Achs-Bbox aber nur zu
    ~0,54 — wer im else-Zweig das Achsrechteck statt der Hülle misst, hängt hier an.
    """
    plan = _gedrehte_treppe(tmp_path)
    ((rect, (cx, cy), _area),) = stiege_rechtecke(plan)
    links = _raum_aus("links", _im_treppenraster(0, -200, _TREPPE_L, 525))
    rechts = _raum_aus("rechts", _im_treppenraster(0, 675, _TREPPE_L, 1400))
    union = unary_union([Polygon(links.polygon_mm), Polygon(rechts.polygon_mm)])
    huelle = _im_treppenraster(0, 0, _TREPPE_L, _TREPPE_B)
    assert not union.covers(Point(cx, cy))           # Bbox-Mitte liegt in der Wand
    assert huelle.intersection(union).area / huelle.area == pytest.approx(0.875, abs=0.01)
    assert Polygon(rect).intersection(union).area / Polygon(rect).area < 0.6   # Bbox weit darunter
    out = typisiere_geometrisch(plan, [links, rechts])
    assert [r.id for r in out] == ["links", "rechts"]   # kein achsparalleles stiegenhaus_1


def test_freistehende_gedrehte_treppe_haengt_gedrehte_huelle_an(tmp_path):
    """Gegenprobe: kein Raum deckt die Hülle → STIEGENHAUS aus der Hülle, nicht aus der Bbox."""
    out = typisiere_geometrisch(_gedrehte_treppe(tmp_path), [_raum("fern", _QUAD)])
    assert [(r.id, r.raum_typ) for r in out] == [("fern", ""), ("stiegenhaus_1", "STIEGENHAUS")]
    neu, huelle = Polygon(out[-1].polygon_mm), _im_treppenraster(0, 0, _TREPPE_L, _TREPPE_B)
    assert neu.symmetric_difference(huelle).area < 1000.0          # mm² — die gedrehte Hülle
    assert out[-1].flaeche_m2 == pytest.approx(3.6, abs=0.05)      # 3,6 m² statt 8,12 m² Achs-Bbox


def test_zonenstempel_ohne_linien_haengt_nicht_an(tmp_path):
    """U1 Z. 416: Treppen-Block ohne Liniengeometrie (Rennweg UG `Stiegenhaus__16`,
    0,63 m²) ist ein Zonenstempel, keine Treppe — trotz Bbox kein eigener Raum."""
    doc = _doc_mit_wand()
    doc.blocks.new("Stiegenhaus__16").add_circle((0, 0), 300)    # Kreis, keine Linien → keine Hülle
    doc.modelspace().add_blockref("Stiegenhaus__16", (2000.0, 9000.0))
    plan = _geladen(doc, tmp_path, "zonenstempel")
    assert len(stiege_rechtecke(plan)) == 1          # Bbox vorhanden: der alte Pfad hängte an
    assert typisiere_geometrisch(plan, []) == []


def test_zweite_treppe_auf_dem_ersten_anhang_haengt_nicht_an(tmp_path):
    """Im selben Lauf angehängte STIEGENHAUS-Räume decken die nächste Treppe mit."""
    doc = _doc_mit_wand()
    name = _stair_block(doc)
    for dx in (0.0, 150.0):                          # zweite Treppe 150 mm versetzt → Hülle 0,9 gedeckt
        doc.modelspace().add_blockref(name, (_TREPPE_XY[0] + dx, _TREPPE_XY[1]),
                                      dxfattribs={"rotation": _TREPPE_GRAD})
    out = typisiere_geometrisch(_geladen(doc, tmp_path, "zwei_treppen"), [])
    assert [r.id for r in out] == ["stiegenhaus_1"]


_KORRIDOR = [(0.0, 0.0), (10000.0, 0.0), (10000.0, 5000.0), (0.0, 5000.0)]   # deckt (2500,2500)


def test_gang_fluchtweg_durch_echten_raum_typisiert():
    r = _raum("a", _QUAD)                      # Zentrum (2500,2500) liegt im Korridor
    out = typisiere_gang([r], [_KORRIDOR])
    assert len(out) == 1
    assert out[0].raum_typ == "GANG" and out[0].ist_fluchtweg


def test_gang_ohne_raum_legt_gang_an():
    out = typisiere_gang([], [_KORRIDOR])
    assert len(out) == 1 and out[0].raum_typ == "GANG"


def test_gang_ruehrt_typisierten_raum_nicht_an():
    r = _raum("a", _QUAD, typ="STIEGENHAUS")
    out = typisiere_gang([r], [_KORRIDOR])
    assert r.raum_typ == "STIEGENHAUS"        # bestehender Typ unangetastet
    # kein echter Raum getroffen → Korridor wird separater GANG-Raum
    assert any(x.raum_typ == "GANG" for x in out)


def test_gang_polygone_mollgasse_echt(mollgasse_blank_eg):
    plan = lade_dxf(str(mollgasse_blank_eg))
    assert len(gang_polygone(plan)) >= 1       # 09-WEG-Fluchtweg → Korridor-Polygone


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
    typen = {r.raum_typ for r in raum.raeume if (r.raum_typ or "").strip()}
    assert "STIEGENHAUS" in typen              # aus STIEGE-Blöcken
    assert "GANG" in typen                     # aus 09-WEG-Fluchtweg
