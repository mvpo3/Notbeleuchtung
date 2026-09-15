"""geometrie_typ — STIEGENHAUS aus Treppen-Blöcken (Typisierung ohne Text-Label)."""
import ezdxf
from shapely.affinity import rotate, translate
from shapely.geometry import Polygon, box
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


# Diagnose Rennweg U1, Slice S9: gedrehte Treppe (Muster DG2 `Stair_2`), deren
# Achs-Bbox-Mitte in einer Wand liegt.
_WAND = "02-TWA-G00-LEG-M0"
_TREPPE_XY, _TREPPE_GRAD = (8000.0, 3000.0), 30.0


def _gedrehte_treppe(tmp_path):
    """Mini-DXF (mm): Wandrechteck, Treppen-Block 3,0 × 1,2 m (Umriss + Stufen), 30° gedreht."""
    doc = ezdxf.new(setup=True)
    doc.header["$INSUNITS"] = 4                      # mm
    doc.layers.add(_WAND)
    msp = doc.modelspace()
    ecken = [(0, 0), (20000, 0), (20000, 12000), (0, 12000)]
    for i in range(4):
        msp.add_line(ecken[i], ecken[(i + 1) % 4], dxfattribs={"layer": _WAND})
    blk = doc.blocks.new("Stair_2")
    blk.add_lwpolyline([(0, 0), (3000, 0), (3000, 1200), (0, 1200)], close=True)
    for x in range(250, 3000, 250):
        blk.add_line((x, 0), (x, 1200))
    msp.add_blockref("Stair_2", _TREPPE_XY, dxfattribs={"rotation": _TREPPE_GRAD})
    pfad = tmp_path / "treppe_gedreht.dxf"
    doc.saveas(str(pfad))
    return lade_dxf(pfad)


def test_gedrehte_treppe_huelle_gedeckt_haengt_nicht_an(tmp_path):
    """Bbox-Mitte in einer 250-mm-Wand, Hülle zu ~90 % von Räumen gedeckt → kein Anhang."""
    plan = _gedrehte_treppe(tmp_path)
    ((_rect, (cx, cy), _area),) = stiege_rechtecke(plan)
    links = _raum("links", [(cx - 4000, cy - 3000), (cx - 125, cy - 3000),
                            (cx - 125, cy + 3000), (cx - 4000, cy + 3000)])
    rechts = _raum("rechts", [(cx + 125, cy - 3000), (cx + 4000, cy - 3000),
                              (cx + 4000, cy + 3000), (cx + 125, cy + 3000)])
    huelle = translate(rotate(box(0, 0, 3000, 1200), _TREPPE_GRAD, origin=(0, 0)), *_TREPPE_XY)
    gedeckt = huelle.intersection(
        unary_union([Polygon(links.polygon_mm), Polygon(rechts.polygon_mm)])).area / huelle.area
    assert 0.89 < gedeckt < 0.91                     # Vorbedingung: Hülle zu ~90 % gedeckt
    out = typisiere_geometrisch(plan, [links, rechts])
    assert [r.id for r in out] == ["links", "rechts"]   # kein achsparalleles stiegenhaus_1


def test_freistehende_gedrehte_treppe_haengt_an(tmp_path):
    """Gegenprobe: dieselbe Treppe, kein Raum deckt die Hülle → STIEGENHAUS wird angehängt."""
    out = typisiere_geometrisch(_gedrehte_treppe(tmp_path), [_raum("fern", _QUAD)])
    assert [(r.id, r.raum_typ) for r in out] == [("fern", ""), ("stiegenhaus_1", "STIEGENHAUS")]


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
