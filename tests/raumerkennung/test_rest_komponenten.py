"""Tests rest_komponenten — synthetische Wandkörper, keine DXF-Datei nötig.

Die Typ-Marker (Treppen-Insert, Schacht-Text, STO-Kästchen) kommen aus einem
In-Memory-``DxfPlan`` (factor 1.0 → Plan-Koordinaten sind mm).
"""
from __future__ import annotations

import ezdxf
from shapely.geometry import Point, Polygon

from notbeleuchtung.raumerkennung.dxf_load import XY, DxfPlan
from notbeleuchtung.raumerkennung.rest_komponenten import komponenten_ohne_stempel
from notbeleuchtung.raumerkennung.tueren import TuerOeffnung
from notbeleuchtung.raumerkennung.wandkoerper import Wandkoerper


def _wk(x0: float, y0: float, x1: float, y1: float) -> Wandkoerper:
    return Wandkoerper(polygon_mm=[(x0, y0), (x1, y0), (x1, y1), (x0, y1)],
                       material="STAHLBETON", layer="wand", quelle="msp",
                       breite_mm=min(x1 - x0, y1 - y0))


# 8×4-m-Box, Trennwand bei x≈4 m mit 0.9-m-Türöffnung, kleine türlose
# Schacht-Box im rechten Raum. Linker Raum ist „belegt".
_WAENDE = [
    _wk(0, 0, 8000, 200), _wk(0, 3800, 8000, 4000),
    _wk(0, 0, 200, 4000), _wk(7800, 0, 8000, 4000),
    _wk(3900, 200, 4100, 1500), _wk(3900, 2400, 4100, 3800),
    _wk(5500, 1500, 7100, 1600), _wk(5500, 2900, 7100, 3000),
    _wk(5500, 1500, 5600, 3000), _wk(7000, 1500, 7100, 3000),
]
_TUER = TuerOeffnung(xy_mm=(4000.0, 1950.0), breite_mm=900.0,
                     winkel_grad=None, quelle="block")
_LINKS = [(200.0, 200.0), (3900.0, 200.0), (3900.0, 3800.0), (200.0, 3800.0)]

# S3a-Layout: wie oben, aber die Schacht-Box misst innen 1.4 × 0.9 m (≈1.2 m²,
# Muster Rennweg DG2 `rest_2` mit 1,16 m²).
_WAENDE_S3A = _WAENDE[:6] + [
    _wk(5500, 1500, 7100, 1600), _wk(5500, 2500, 7100, 2600),
    _wk(5500, 1500, 5600, 2600), _wk(7000, 1500, 7100, 2600),
]
_SCHACHT_MITTE: XY = (6300.0, 2050.0)      # Mitte der Schacht-Box
_IM_GROSSEN_REST: XY = (4500.0, 3000.0)    # im rechten Raum, außerhalb der Box


def _plan(texte: list[tuple[str, XY]] | None = None,
          stiegen: list[XY] | None = None, sto: list[XY] | None = None) -> DxfPlan:
    """In-Memory-Plan mit den Typ-Markern (Wände kommen als ``Wandkoerper``)."""
    doc = ezdxf.new(setup=True)
    msp = doc.modelspace()
    for txt, xy in texte or []:
        msp.add_text(txt, dxfattribs={"insert": xy})
    if stiegen:
        doc.blocks.new("STIEGE_1")
        for xy in stiegen:
            msp.add_blockref("STIEGE_1", xy)
    if sto:
        doc.layers.add("04-STO")
        for x, y in sto:
            msp.add_lwpolyline([(x - 100, y - 100), (x + 100, y - 100),
                                (x + 100, y + 100), (x - 100, y + 100)],
                               close=True, dxfattribs={"layer": "04-STO"})
    return DxfPlan(doc=doc, space=msp, factor=1.0)


def _klein(raeume):
    return min(raeume, key=lambda r: r.flaeche_m2)


def test_rest_findet_rechten_raum_und_nische():
    raeume = komponenten_ohne_stempel(None, _WAENDE, [_TUER], [_LINKS])
    typen = sorted(r.raum_typ for r in raeume)
    # Slice K2 (Owner-Regel a): ohne Plan kein Schacht-Beleg — die türlose
    # Kleinfläche ist NISCHE, nicht mehr SCHACHT.
    assert "NISCHE" in typen and "SCHACHT" not in typen
    gross = max(raeume, key=lambda r: r.flaeche_m2)
    assert gross.raum_typ == ""                    # untypisiert, kein "UNBEKANNT"
    assert 8.0 <= gross.flaeche_m2 <= 14.0         # rechter Raum minus Schacht-Box
    # Belegter linker Raum liefert KEINE Rest-Komponente.
    links = Polygon(_LINKS)
    assert not any(links.covers(Point(*r.polygon_mm[0])) and links.covers(
        Polygon(r.polygon_mm).centroid) for r in raeume)
    assert all(r.id.startswith("rest_") for r in raeume)


def test_ohne_waende_leer():
    assert komponenten_ohne_stempel(None, [], [], []) == []


# --- S3a: Schacht-Evidenz vor der Treppenmarker-Regel (Diagnose Rennweg U2) ---

def test_schacht_text_schlaegt_treppenmarker():
    """DG2 `rest_2`: „DBA SCHACHT" im Polygon, Treppenmarker 700 mm daneben."""
    plan = _plan(texte=[("DBA SCHACHT", _SCHACHT_MITTE)], stiegen=[(7700.0, 2050.0)])
    klein = _klein(komponenten_ohne_stempel(plan, _WAENDE_S3A, [_TUER], [_LINKS]))
    assert klein.flaeche_m2 < 3.0
    assert klein.raum_typ == "SCHACHT"
    # SCHACHT ist KEIN_RAUM (nutzungsklasse.py) — Fluchtweg-Flag wäre falsch.
    assert not klein.ist_fluchtweg
    assert not klein.ist_communal


def test_bdb_text_ist_evidenz():
    """Zweiter Wortzweig `F?BDB|DDB`: „SCHACHTTYP" scheitert an der Wortgrenze,
    „DDB" trägt die Evidenz allein (gemessener Mollgasse-Text)."""
    plan = _plan(texte=[("S1.2 SCHACHTTYP A DDB 79.5/38", _SCHACHT_MITTE)],
                 stiegen=[_SCHACHT_MITTE])
    klein = _klein(komponenten_ohne_stempel(plan, _WAENDE_S3A, [_TUER], [_LINKS]))
    assert klein.raum_typ == "SCHACHT"


def test_sto_kaestchen_schlaegt_treppenmarker():
    """Zweiter Evidenz-Zweig: STO-Kästchen im Polygon, Marker mitten drin."""
    plan = _plan(stiegen=[_SCHACHT_MITTE], sto=[_SCHACHT_MITTE])
    klein = _klein(komponenten_ohne_stempel(plan, _WAENDE_S3A, [_TUER], [_LINKS]))
    assert klein.raum_typ == "SCHACHT"
    assert not klein.ist_fluchtweg
    assert not klein.ist_communal


def test_tuerlose_kleinflaeche_am_marker_bleibt_stiegenhaus():
    """Ohne Planzeichen bleibt die Markerregel vorn (Liftringe; S3b/F4 offen)."""
    plan = _plan(stiegen=[_SCHACHT_MITTE])
    klein = _klein(komponenten_ohne_stempel(plan, _WAENDE_S3A, [_TUER], [_LINKS]))
    assert klein.flaeche_m2 < 3.0
    assert klein.raum_typ == "STIEGENHAUS"


def test_grosse_flaeche_mit_text_und_marker_bleibt_stiegenhaus():
    """Deckelung < 3 m²: der Treppenlauf bleibt STIEGENHAUS trotz Schacht-Text."""
    plan = _plan(texte=[("DBA SCHACHT", _IM_GROSSEN_REST)], stiegen=[_IM_GROSSEN_REST])
    raeume = komponenten_ohne_stempel(plan, _WAENDE_S3A, [_TUER], [_LINKS])
    gross = max(raeume, key=lambda r: r.flaeche_m2)
    assert gross.flaeche_m2 >= 3.0
    assert gross.raum_typ == "STIEGENHAUS"


def test_ausschlussliste_stoppt_raum_treppen_lifttexte():
    """Ausschlussliste RAUM/TREPP/STIEG/AUFZUG/LIFT: beide Texte treffen den
    Wortschatz („SCHACHT" bzw. „DDB") und werden erst hier gestoppt.

    Kein gemessener Plan löst den Ausschluss heute aus (Rennweg UG..DG2,
    Barawitzka/Mollgasse/Muthgasse EG: 0 Treffer) — er ist der Guard gegen
    Treppen-/Lifttexte aus U2 (Z.478), nicht der heutige Normalfall.
    """
    plan = _plan(texte=[("Schacht Treppenlauf", _SCHACHT_MITTE),
                        ("Liftschacht DDB 79/38", _SCHACHT_MITTE)],
                 stiegen=[_SCHACHT_MITTE])
    klein = _klein(komponenten_ohne_stempel(plan, _WAENDE_S3A, [_TUER], [_LINKS]))
    assert klein.raum_typ == "STIEGENHAUS"


def test_text_ohne_schacht_wortgrenze_ist_keine_evidenz():
    """Negativ: „DBA" allein, „DBA Raum" und „Schachtverzug" sind kein Planzeichen."""
    plan = _plan(texte=[("DBA", _SCHACHT_MITTE), ("DBA Raum", _SCHACHT_MITTE),
                        ("Schachtverzug im Zimmer", _SCHACHT_MITTE)],
                 stiegen=[_SCHACHT_MITTE])
    klein = _klein(komponenten_ohne_stempel(plan, _WAENDE_S3A, [_TUER], [_LINKS]))
    assert klein.raum_typ == "STIEGENHAUS"


# --- K2: Schacht nur mit Beleg (Owner-Regel a, 2026-09-29) -------------------
#
# „Rote Kontur allein ist kein Beleg. SCHACHT braucht mindestens eines: Text
# DDB/BDB/DBA/Schacht/Durchbruch in 500 mm, U-förmige Schachtmauer,
# FEUERFESTER_STEIN-Keil, Schacht-Zone oder -Layer. Sonst NISCHE."
# Schacht-Box innen x 5600..7000, y 1600..2500 (1,26 m², türlos).

_BOX_INNEN = [(5600.0, 1600.0), (7000.0, 1600.0), (7000.0, 2500.0), (5600.0, 2500.0)]


def _plan_k2(texte=(), kaesten=(), keile=(), layer_linien=()) -> DxfPlan:
    """Plan ohne Treppenmarker; Kästen als geschlossene rote LWPOLYLINE,
    Keile als HATCH FEUERFESTER_STEIN, Schacht-Layer als LINE."""
    doc = ezdxf.new(setup=True)
    msp = doc.modelspace()
    for txt, xy in texte:
        msp.add_text(txt, dxfattribs={"insert": xy})
    for pts in kaesten:
        msp.add_lwpolyline(pts, close=True, dxfattribs={"color": 1})
    for pts in keile:
        h = msp.add_hatch(color=1)
        h.set_pattern_fill("ANSI31", scale=10)
        h.dxf.pattern_name = "FEUERFESTER_STEIN"
        h.paths.add_polyline_path(pts, is_closed=True)
    for layer, a, b in layer_linien:
        msp.add_line(a, b, dxfattribs={"layer": layer})
    return DxfPlan(doc=doc, space=msp, factor=1.0)


def _box_typ(plan) -> str:
    klein = _klein(komponenten_ohne_stempel(plan, _WAENDE_S3A, [_TUER], [_LINKS]))
    assert klein.flaeche_m2 < 3.0
    return klein.raum_typ


def test_k2_tuerlose_kleinflaeche_ohne_beleg_ist_nische():
    """Rennweg DG2 `rest_5`-Muster: klein, türlos, kein Planzeichen → NISCHE,
    ohne Fluchtweg-/communal-Flag und ohne Nutzungsklasse (fail-safe)."""
    from notbeleuchtung.raumerkennung.nutzungsklasse import nutzungsklasse_fuer

    klein = _klein(komponenten_ohne_stempel(_plan_k2(), _WAENDE_S3A, [_TUER], [_LINKS]))
    assert klein.raum_typ == "NISCHE"
    assert not klein.ist_fluchtweg and not klein.ist_communal
    assert nutzungsklasse_fuer("NISCHE") is None


def test_k2_text_im_umkreis_500_ist_beleg():
    """Text außerhalb der Fläche, 400 mm unter der Box: Beleg (DBA zählt, Owner)."""
    assert _box_typ(_plan_k2(texte=[("DBA 40/70", (6300.0, 1200.0))])) == "SCHACHT"
    assert _box_typ(_plan_k2(texte=[("Deckendurchbruch", (6300.0, 1200.0))])) == "SCHACHT"


def test_k2_text_weiter_als_500_ist_kein_beleg():
    assert _box_typ(_plan_k2(texte=[("DDB 40/70", (6300.0, 900.0))])) == "NISCHE"


def test_k2_keil_im_kasten_der_flaeche_ist_beleg():
    """Keil (FEUERFESTER_STEIN) in einem Kasten, der die Fläche deckt → SCHACHT."""
    plan = _plan_k2(kaesten=[_BOX_INNEN],
                    keile=[[(6700.0, 1600.0), (7000.0, 1600.0), (7000.0, 1900.0)]])
    assert _box_typ(plan) == "SCHACHT"


def test_k2_keil_kasten_streift_die_flaeche_nur_ist_nische():
    """Rennweg DG2 `rest_5`: der Kasten „Schachtverzug über Dach" deckt nur 18 %
    der Nische. Hier deckt er 0,12 von 1,26 m² → kein Beleg → NISCHE."""
    ecke = [(5600.0, 1600.0), (6000.0, 1600.0), (6000.0, 1900.0), (5600.0, 1900.0)]
    plan = _plan_k2(kaesten=[ecke],
                    keile=[[(5600.0, 1600.0), (5800.0, 1600.0), (5600.0, 1800.0)]])
    assert _box_typ(plan) == "NISCHE"


def test_k2_rote_kontur_allein_ist_kein_beleg():
    assert _box_typ(_plan_k2(kaesten=[_BOX_INNEN])) == "NISCHE"


def test_k2_schacht_layer_ist_beleg():
    plan = _plan_k2(layer_linien=[("HKLS Schacht", (6000.0, 2000.0), (6600.0, 2000.0))])
    assert _box_typ(plan) == "SCHACHT"


# --- S3b: Rückdehnung der Türscheiben (docs/GATE_TUERSTAPEL.md § 7) ---------
#
# Die Türscheibe (r = max(600, Breite) mm) trennt die Restflächen an der
# Öffnung; ohne Rückdehnung enden die Konturen r mm vor der Tür (Rennweg OG3:
# 810–968 mm, 7 Blocktüren `seite_fehlt`). Zurückgedehnt wird wie in
# ``stempel_flutung``: nur die versiegelten Zellen, geodätisch, mit allen
# Restflächen als konkurrierenden Markern — nie in Wand, Freiland oder belegte
# Räume.

_ZELLE_MM = 50.0                       # Rasterweite der Rest-Stufe
_TUERPUNKT = Point(_TUER.xy_mm)        # (4000, 1950), Trennwand x 3900..4100
_WAENDE_S3B = _WAENDE[:6]              # zwei leere Räume, eine 0.9-m-Öffnung


def _links_rechts(raeume):
    links = [Polygon(r.polygon_mm) for r in raeume
             if Polygon(r.polygon_mm).centroid.x < _TUERPUNKT.x]
    rechts = [Polygon(r.polygon_mm) for r in raeume
              if Polygon(r.polygon_mm).centroid.x > _TUERPUNKT.x]
    return links, rechts


def test_s3b_kontur_erreicht_die_tuerlinie():
    """Beide Restflächen reichen bis auf eine Rasterzelle an den Türpunkt."""
    links, rechts = _links_rechts(
        komponenten_ohne_stempel(None, _WAENDE_S3B, [_TUER], []))
    assert len(links) == 1 and len(rechts) == 1
    abstand = [round(p.distance(_TUERPUNKT), 1) for p in (links[0], rechts[0])]
    assert max(abstand) <= _ZELLE_MM, abstand


def test_s3b_zwei_restflaechen_trennen_sich_an_der_tuerlinie():
    """Zwei Restflächen an derselben Tür treffen sich an der Türlinie: keine
    läuft über die andere, beide bleiben eigene Räume."""
    links, rechts = _links_rechts(
        komponenten_ohne_stempel(None, _WAENDE_S3B, [_TUER], []))
    assert len(links) == 1 and len(rechts) == 1
    li, re_ = links[0], rechts[0]
    assert li.intersection(re_).area < 1e4          # < 0,01 m²
    assert li.bounds[2] <= _TUERPUNKT.x + _ZELLE_MM, li.bounds
    assert re_.bounds[0] >= _TUERPUNKT.x - _ZELLE_MM, re_.bounds
    assert li.distance(re_) <= 2 * _ZELLE_MM


def test_s3b_kein_wachsen_in_belegte_raeume():
    """Die Rückdehnung endet am (gepufferten) belegten Raum — die Restfläche
    reicht bis an die Tür, aber nicht in den gestempelten Raum hinein."""
    raeume = komponenten_ohne_stempel(None, _WAENDE_S3B, [_TUER], [_LINKS])
    assert len(raeume) == 1
    rest = Polygon(raeume[0].polygon_mm)
    assert rest.intersection(Polygon(_LINKS)).area < 1e4
    assert rest.distance(_TUERPUNKT) <= 2 * _ZELLE_MM


# Drei Räume in einer Reihe, zwei Öffnungen: Reihenfolge-Invarianz.
_WAENDE_REIHE = [
    _wk(0, 0, 11000, 200), _wk(0, 3800, 11000, 4000),
    _wk(0, 0, 200, 4000), _wk(10800, 0, 11000, 4000),
    _wk(3900, 200, 4100, 1500), _wk(3900, 2400, 4100, 3800),
    _wk(7400, 200, 7600, 1500), _wk(7400, 2400, 7600, 3800),
]
_TUER_2 = TuerOeffnung(xy_mm=(7500.0, 1950.0), breite_mm=900.0,
                       winkel_grad=None, quelle="block")
_RECHTS_REIHE = [(7600.0, 200.0), (10800.0, 200.0), (10800.0, 3800.0),
                 (7600.0, 3800.0)]


def _abdruck(raeume):
    return [(r.id, r.raum_typ, round(r.flaeche_m2, 6),
             [(round(x, 3), round(y, 3)) for x, y in r.polygon_mm])
            for r in raeume]


def test_s3b_reihenfolge_invariant():
    """Türen, Wandkörper und belegte Polygone in anderer Reihenfolge →
    dieselben Räume (IDs, Typen, Polygone)."""
    for belegt in ([], [_LINKS, _RECHTS_REIHE]):
        a = komponenten_ohne_stempel(None, _WAENDE_REIHE, [_TUER, _TUER_2], belegt)
        b = komponenten_ohne_stempel(None, list(reversed(_WAENDE_REIHE)),
                                     [_TUER_2, _TUER], list(reversed(belegt)))
        assert a
        assert _abdruck(a) == _abdruck(b)


def test_s3b_mittlerer_raum_erreicht_beide_tueren():
    """Der Mittelraum reicht an beide Türlinien, auch wenn beide Nachbarn
    belegt sind (Muster Rennweg OG3 `rest_4`: Stiegenhaus zwischen Wohnungen)."""
    raeume = komponenten_ohne_stempel(None, _WAENDE_REIHE, [_TUER, _TUER_2],
                                      [_LINKS, _RECHTS_REIHE])
    assert len(raeume) == 1
    mitte = Polygon(raeume[0].polygon_mm)
    assert mitte.distance(_TUERPUNKT) <= 2 * _ZELLE_MM
    assert mitte.distance(Point(_TUER_2.xy_mm)) <= 2 * _ZELLE_MM


# Kleinraum hinter einer 600-mm-Tür: erodiert < 1 m², zurückgedehnt ≥ 1 m².
# Gang unten (y 200..1200), Kleinraum oben rechts (x 3800..4800, y 1400..2700,
# 1,30 m²), Tür in der Zwischenwand bei (4300, 1300).
_WAENDE_KLEIN = [
    _wk(0, 0, 5000, 200), _wk(0, 2700, 5000, 2900),
    _wk(0, 0, 200, 2900), _wk(4800, 0, 5000, 2900),
    _wk(200, 1200, 4000, 1400), _wk(4600, 1200, 4800, 1400),
    _wk(3600, 1400, 3800, 2700),
]
_TUER_KLEIN = TuerOeffnung(xy_mm=(4300.0, 1300.0), breite_mm=600.0,
                           winkel_grad=None, quelle="block")
_KLEINRAUM = Polygon([(3800, 1400), (4800, 1400), (4800, 2700), (3800, 2700)])


def test_s3b_mindestflaeche_gilt_nach_der_rueckdehnung():
    """``_MIN_M2`` wird NACH der Rückdehnung geprüft: der Kleinraum ist
    erodiert kleiner als 1 m² (die Türscheibe frisst 0,6 m tief hinein),
    zurückgedehnt 1,3 m² — er ist ein Raum und endet an der Türlinie."""
    raeume = komponenten_ohne_stempel(None, _WAENDE_KLEIN, [_TUER_KLEIN], [])
    klein = [r for r in raeume
             if _KLEINRAUM.contains(Polygon(r.polygon_mm).representative_point())]
    assert len(klein) == 1, [(r.id, r.flaeche_m2) for r in raeume]
    assert 1.0 <= klein[0].flaeche_m2 <= 1.4
    assert Polygon(klein[0].polygon_mm).distance(Point(_TUER_KLEIN.xy_mm)) <= _ZELLE_MM
    # Der Gang wächst bis an die Tür, aber nicht in den Kleinraum.
    gang = [Polygon(r.polygon_mm) for r in raeume if r is not klein[0]
            and Polygon(r.polygon_mm).distance(Point(_TUER_KLEIN.xy_mm)) <= _ZELLE_MM]
    assert len(gang) == 1
    assert gang[0].intersection(_KLEINRAUM).area < 1e4
