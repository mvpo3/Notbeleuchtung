"""aussenbereich — Komponenten-Konturen, offene und geschlossene Außenflächen."""
from __future__ import annotations

import ezdxf
from shapely.geometry import Point, Polygon
from shapely.ops import unary_union

from notbeleuchtung.hauptengine.contracts.raum_modell import Raum
from notbeleuchtung.raumerkennung import aussenbereich
from notbeleuchtung.raumerkennung.aussenbereich import (
    _SCHLIESS_MM,
    _wand_geschlossen,
    aussen_indizien,
    aussenkontur_komponenten,
    erkenne_aussenbereiche,
    grundstuecksgrenze,
    ueberdachungen,
)
from notbeleuchtung.raumerkennung.dxf_load import DxfPlan
from notbeleuchtung.raumerkennung.stempel_anker import Stempel, Zuordnung
from notbeleuchtung.raumerkennung.wandkoerper import Wandkoerper


def _wk(x0, y0, x1, y1) -> Wandkoerper:
    return Wandkoerper(
        polygon_mm=[(x0, y0), (x1, y0), (x1, y1), (x0, y1)],
        material="STAHLBETON", layer="wand", quelle="msp", breite_mm=300.0)


def _ring(x0, y0, x1, y1, d=1500.0) -> list[Wandkoerper]:
    """Geschlossener Wand-Ring (4 Platten der Dicke d) um das Rechteck."""
    return [
        _wk(x0, y0, x1, y0 + d), _wk(x0, y1 - d, x1, y1),
        _wk(x0, y0, x0 + d, y1), _wk(x1 - d, y0, x1, y1),
    ]


def _wand_zu(koerper):
    return _wand_geschlossen(koerper, _SCHLIESS_MM)


def _leerer_plan(baum_xy=None, gruen_linie=None) -> DxfPlan:
    doc = ezdxf.new()
    doc.header["$INSUNITS"] = 4
    msp = doc.modelspace()
    if baum_xy is not None:
        doc.blocks.new("BAUM_LAUB")
        doc.layers.add("20-AUS")
        msp.add_blockref("BAUM_LAUB", baum_xy, dxfattribs={"layer": "20-AUS"})
    if gruen_linie is not None:
        doc.layers.add("02-FIL-G00-LEG-GRÜN")
        msp.add_line(*gruen_linie, dxfattribs={"layer": "02-FIL-G00-LEG-GRÜN"})
    return DxfPlan(doc=doc, space=msp, factor=1.0)


def test_zwei_trakte_geben_zwei_komponenten_und_offenen_zwischenraum():
    koerper = _ring(0, 0, 20000, 20000) + _ring(30000, 0, 50000, 20000)
    komponenten = aussenkontur_komponenten(koerper)
    assert len(komponenten) == 2, "je Trakt eine Außenkontur (Barawitzka-Muster)"
    ab = erkenne_aussenbereiche(_leerer_plan(), koerper)
    zwischen = Point(25000, 10000)   # Fläche zwischen den Trakten, offen n. Rand
    assert any(p.covers(zwischen) for p in ab.offen), "Zwischenraum nicht AUSSEN"
    assert not ab.gedeckt().covers(zwischen)
    # Rauminneres bleibt gedeckt (kein AUSSEN):
    assert ab.gedeckt().covers(Point(10000, 10000))


def test_eingeschlossener_hof_mit_baum_ist_aussen_geschlossen():
    koerper = _ring(0, 0, 30000, 30000, d=5000.0)   # Hof 20×20 m, versiegelt
    hof = Point(15000, 15000)
    ab = erkenne_aussenbereiche(_leerer_plan(baum_xy=(15000, 15000)), koerper)
    assert any(p.covers(hof) for p in ab.geschlossen), "Hof nicht als geschlossen erkannt"
    assert not any(p.covers(hof) for p in ab.offen)
    # Geschlossener Hof zählt als gedeckt → Türen dorthin werden NICHT AUSSEN
    # (kein final_exit; offene Frage an Enis).
    assert ab.gedeckt().covers(hof)


def test_hof_ohne_indiz_bleibt_unklassifiziert():
    koerper = _ring(0, 0, 30000, 30000, d=5000.0)
    ab = erkenne_aussenbereiche(_leerer_plan(), koerper)
    assert not ab.geschlossen and not ab.offen or all(
        not p.covers(Point(15000, 15000)) for p in ab.geschlossen + ab.offen)


def test_loch_hinter_duenner_fassade_ohne_indiz_ist_nie_aussen():
    """Owner-Entscheid F7 (2026-09-15): Ein Loch der Komponenten ohne Außen-
    Indiz ist nie AUSSEN, auch < 250 mm vor dem Hüllrand (Rennweg DG1:
    Wohnzimmer-Loch 193 mm vor der Hülle wurde offen, Diagnose U7)."""
    koerper = _ring(0, 0, 20000, 20000, d=150.0)   # 150-mm-Restbarriere zur Hülle
    innen = Point(10000, 10000)
    ab = erkenne_aussenbereiche(_leerer_plan(), koerper)
    assert not any(p.covers(innen) for p in ab.offen), "Innenraum-Loch als AUSSEN offen"
    assert not any(p.covers(innen) for p in ab.geschlossen)
    assert ab.gedeckt().covers(innen)
    # Gegenprobe: gleiches Loch mit Baum-Block bleibt AUSSEN.
    ab_baum = erkenne_aussenbereiche(_leerer_plan(baum_xy=(10000, 10000)), koerper)
    assert any(p.covers(innen) for p in ab_baum.offen + ab_baum.geschlossen), \
        "Loch mit Außen-Indiz nicht AUSSEN"


def test_aussen_indizien_baum_und_gruenlayer():
    plan = _leerer_plan(baum_xy=(1000, 2000),
                        gruen_linie=((0, 0), (5000, 0)))
    pts = aussen_indizien(plan)
    assert (1000.0, 2000.0) in pts
    assert (0.0, 0.0) in pts


def _grenz_plan(typ: str, gehsteig=None) -> DxfPlan:
    """Plan mit KATASTER-Layer: als geschlossene Polylinie oder nur als DIMENSION.

    Der DIMENSION-Fall bildet Rennweg_OG3 nach (Layer 'New_GRUNDSTÜCKSGRENZE'
    mit 103 DIMENSION und NULL Liniengeometrie) — dort darf kein Ring entstehen.
    """
    doc = ezdxf.new()
    doc.header["$INSUNITS"] = 4
    msp = doc.modelspace()
    doc.layers.add("KATASTER-GRENZE")
    ecken = [(-5000, -5000), (35000, -5000), (35000, 35000), (-5000, 35000)]
    if typ == "polyline":
        msp.add_lwpolyline(ecken, close=True, dxfattribs={"layer": "KATASTER-GRENZE"})
    else:
        msp.add_aligned_dim(p1=ecken[0], p2=ecken[1], distance=1000,
                            dxfattribs={"layer": "KATASTER-GRENZE"})
    if gehsteig is not None:
        doc.layers.add("09-SYM-GEHSTEIG")
        msp.add_line(*gehsteig, dxfattribs={"layer": "09-SYM-GEHSTEIG"})
    return DxfPlan(doc=doc, space=msp, factor=1.0)


def test_grundstuecksgrenze_nur_mit_liniengeometrie():
    koerper = _ring(0, 0, 30000, 30000, d=5000.0)
    ring = grundstuecksgrenze(_grenz_plan("polyline"), _wand_zu(koerper))
    assert ring is not None and abs(ring.area - 40000 * 40000) < 1.0
    # Gleicher Layer, aber nur DIMENSION → Typ-Filter greift, kein Falschpositiv.
    assert grundstuecksgrenze(_grenz_plan("dimension"), _wand_zu(koerper)) is None


def test_hof_ohne_strassenkante_bleibt_geschlossen():
    """Hof am Grundstücksrand: erst die Straßenkante macht ihn zum Weg ins Freie.

    Barawitzka-Muster: nach Süden offener Hof, Grundstück reicht dort weiter;
    im Norden liegt die Straße, aber davor steht das Gebäude.
    """
    koerper = [_wk(0, 25000, 30000, 30000),          # Nordtrakt
               _wk(0, 0, 5000, 30000), _wk(25000, 0, 30000, 30000)]
    hof = Point(15000, 12000)

    def _plan(gehsteig_y=None) -> DxfPlan:
        doc = ezdxf.new()
        doc.header["$INSUNITS"] = 4
        msp = doc.modelspace()
        doc.layers.add("KATASTER-GRENZE")
        # Grundstück: im Norden bündig mit dem Gebäude, nach Süden 10 m Hof.
        msp.add_lwpolyline([(0, -10000), (30000, -10000), (30000, 30000),
                            (0, 30000)], close=True,
                           dxfattribs={"layer": "KATASTER-GRENZE"})
        if gehsteig_y is not None:
            doc.layers.add("09-SYM-GEHSTEIG")
            msp.add_line((0, gehsteig_y), (30000, gehsteig_y),
                         dxfattribs={"layer": "09-SYM-GEHSTEIG"})
        return DxfPlan(doc=doc, space=msp, factor=1.0)

    ab = erkenne_aussenbereiche(_plan(gehsteig_y=32000), koerper)
    assert any(p.covers(hof) for p in ab.geschlossen), "Straße im Norden verbaut"
    assert not any(p.covers(hof) for p in ab.offen)

    ab2 = erkenne_aussenbereiche(_plan(gehsteig_y=-12000), koerper)
    assert any(p.covers(hof) for p in ab2.offen), "Straßenkante im Süden nicht erkannt"


def _rect(x0, y0, x1, y1) -> list:
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def _raum(rid: str, typ: str, poly: list) -> Raum:
    return Raum(id=rid, raum_typ=typ, polygon_mm=poly,
                flaeche_m2=Polygon(poly).area / 1e6)


def _zuordnung(raum: Raum, name: str) -> Zuordnung:
    """Stempel-Zuordnung der Kaskade — nur Name und Raum zählen für S2."""
    s = Stempel(name=name, typ=None, flaeche_m2=None, belag=None,
                position_mm=(0.0, 0.0), quelle="MTEXT", layer="text")
    return Zuordnung(stempel=s, polygon_index=None, raum=raum,
                     abweichung_prozent=None, flag="ok")


def _ring_mit_luecke(x0, y0, x1, y1, d=500.0, luecke=(8500.0, 11500.0)) -> list[Wandkoerper]:
    """Wand-Ring mit 3-m-Fensterlücke in der Südwand: die 1200-mm-Versiegelung
    (`_SCHLIESS_MM`) überbrückt sie nicht — die Außenfläche fließt ins Haus.

    500-mm-Fassade, weil erst ab dieser Dicke die 5-m-Gebäudemaske den Ring
    über der Lücke schließt (gemessen: bei 300 mm bleibt sie offen, die Maske
    ist dann nur das Wandband selbst)."""
    a, b = luecke
    return [
        _wk(x0, y0, a, y0 + d), _wk(b, y0, x1, y0 + d), _wk(x0, y1 - d, x1, y1),
        _wk(x0, y0, x0 + d, y1), _wk(x1 - d, y0, x1, y1),
    ]


def _setze_block(plan: DxfPlan, name: str, xy, wrapper: str | None = None) -> None:
    """INSERT `name` an xy (mm) — direkt oder über einen Wrapper-Block
    (Einfügepunkt-Rekursion über `virtual_entities`)."""
    if name not in plan.doc.blocks:
        plan.doc.blocks.new(name)
    if wrapper is None:
        plan.space.add_blockref(name, xy)
        return
    blk = plan.doc.blocks.new(wrapper)
    blk.add_blockref(name, (xy[0] - 1000.0, xy[1]))
    plan.space.add_blockref(wrapper, (1000.0, 0.0))


def test_gestempelte_innenzone_hinter_fensterluecke_ist_nicht_aussen():
    """Diagnose Rennweg U8, Slice S2: ein gestempeltes ZIMMER hinter einer
    3-m-Fensterlücke ist nie AUSSEN und zählt als gedeckt; die TERRASSE vor der
    Fassade bleibt offen (Freifläche, F6)."""
    koerper = _ring_mit_luecke(0, 0, 20000, 20000)
    zimmer = _raum("raum_1", "ZIMMER", _rect(500, 500, 19500, 19500))
    terrasse = _raum("raum_2", "TERRASSE", _rect(2000, -4000, 8000, -300))
    plan = _grenz_plan("polyline")
    zonen = aussenbereich.waehle_innen_zonen(
        plan, [zimmer, terrasse], [_zuordnung(zimmer, "Zimmer 18,20 m2")])
    ab = erkenne_aussenbereiche(plan, koerper, zonen)
    drinnen, davor = Point(10000, 10000), Point(5000, -2000)
    assert not any(p.covers(drinnen) for p in ab.offen), "Innenzone weiter AUSSEN"
    assert ab.gedeckt().covers(drinnen), "Innenzone nicht gedeckt"
    assert any(p.covers(davor) for p in ab.offen), "TERRASSE vor der Fassade nicht offen"
    assert not ab.gedeckt().covers(davor)


def test_innen_zonen_option_4_stempel_moebel_und_aussen_vokabular():
    """Owner-Entscheid F6 Option 4 (2026-09-15): Grund = Innen-Typ ODER
    zugeordneter Stempel ODER Sanitär-/Möbel-Beleg; der Ausschluss (Freifläche,
    Außen-Vokabular im Stempel) hat Vorrang. ArchiCAD-Zonenstempel-Blöcke
    (»Dusche__4«) sind Beschriftung, kein Beleg."""
    koerper = _ring_mit_luecke(0, 0, 20000, 20000)
    tv = _raum("raum_1", "", _rect(500, 500, 4000, 19500))         # Stempel »TV Raum«
    hof = _raum("raum_2", "", _rect(4000, 500, 8000, 19500))       # Stempel »Hof«
    schlaf = _raum("raum_3", "", _rect(8000, 500, 12000, 19500))   # Möbel-Beleg
    bad = _raum("raum_4", "", _rect(12000, 500, 16000, 19500))     # Sanitär-Beleg (im Block)
    rest = _raum("raum_5", "", _rect(16000, 500, 19500, 19500))    # nur Zonenstempel-Block
    terrasse = _raum("raum_6", "TERRASSE", _rect(2000, -4000, 8000, -300))
    plan = _grenz_plan("polyline")
    _setze_block(plan, "Doppelbett 01", (10000, 10000))
    _setze_block(plan, "Waschbecken 01", (14000, 10000), wrapper="Bad Gruppe")
    _setze_block(plan, "Dusche__4", (18000, 10000))
    _setze_block(plan, "Chair 02", (5000, -2000))      # Möbel auf der Freifläche
    zonen = aussenbereich.waehle_innen_zonen(
        plan, [tv, hof, schlaf, bad, rest, terrasse],
        [_zuordnung(tv, "TV Raum"), _zuordnung(hof, "Hof 23,50 m2")])
    ab = erkenne_aussenbereiche(plan, koerper, zonen)

    def _offen(xy) -> bool:
        return any(p.covers(Point(xy)) for p in ab.offen)

    assert not _offen((2000, 10000)), "untypisierter Raum mit Stempel blieb AUSSEN"
    assert _offen((6000, 10000)), "Stempel »Hof« bekam ein Innen-Veto"
    assert not _offen((10000, 10000)), "Möbel-Beleg ohne Wirkung"
    assert not _offen((14000, 10000)), "Sanitär-Beleg ohne Wirkung"
    assert _offen((18000, 10000)), "Zonenstempel-Block als Sanitär-Beleg gewertet"
    assert _offen((5000, -2000)), "TERRASSE mit Möbeln wurde Innen-Zone"


def test_freiflaeche_mit_moebeln_innerhalb_der_maske_bleibt_aussen():
    """F6 (Owner 2026-09-15): Möbel machen eine Freifläche nie innen — auch eine
    zurückspringende Loggia/Terrasse INNERHALB des Wandrings (Rennweg OG2
    raum_13/raum_14, DG2 raum_3) bleibt AUSSEN.

    Kontrollierter Vergleich: dieselbe Geometrie mit demselben Möbel-Block,
    einmal als ZIMMER, einmal als LOGGIA. Der ZIMMER-Lauf belegt, dass die
    Gebäudemaske diese Fläche deckt — die Loggia bleibt also wegen der
    Freiflächen-Regel offen, nicht wegen des Maskenzuschnitts.
    """
    koerper = _ring_mit_luecke(0, 0, 20000, 20000)
    plan = _grenz_plan("polyline")
    _setze_block(plan, "Chair 02", (10000, 10000))     # Möbel-Beleg im Polygon
    poly = _rect(500, 500, 19500, 19500)
    drinnen = Point(10000, 10000)

    def _ab(typ):
        raum = _raum("raum_1", typ, poly)
        zonen = aussenbereich.waehle_innen_zonen(plan, [raum], [])
        return erkenne_aussenbereiche(plan, koerper, zonen)

    assert _ab("ZIMMER").gedeckt().covers(drinnen), "Maske deckt die Fläche nicht"
    ab = _ab("LOGGIA")
    assert any(p.covers(drinnen) for p in ab.offen), "Loggia mit Möbeln wurde Innen-Zone"
    assert not ab.gedeckt().covers(drinnen)


def test_zone_ausserhalb_der_gebaeudemaske_bleibt_aussen():
    """Rennweg DG2 (U9/F5): die ArchiCAD-Zone ragt 1,5 m über die Fassade —
    der Zuschnitt auf die Gebäudemaske lässt den Dachstreifen offen."""
    koerper = _ring_mit_luecke(0, 0, 20000, 20000)
    zimmer = _raum("raum_1", "ZIMMER", _rect(500, -1500, 19500, 19500))
    plan = _grenz_plan("polyline")
    zonen = aussenbereich.waehle_innen_zonen(plan, [zimmer], [])
    ab = erkenne_aussenbereiche(plan, koerper, zonen)
    streifen = Point(5000, -800)
    assert any(p.covers(streifen) for p in ab.offen), "Dachstreifen nicht mehr AUSSEN"
    assert not ab.gedeckt().covers(streifen), "Zone außerhalb der Maske gedeckt"
    assert ab.gedeckt().covers(Point(10000, 10000)), "Zone in der Maske nicht gedeckt"


def test_maske_ueberbrueckt_den_abstand_zwischen_zwei_trakten_nicht():
    """Gegenprobe NACH OBEN zum Maskenknopf (`_MASKE_MM`, heute 5000 mm).

    Die Tests halten die Maske bisher nur nach unten fest (zu klein → Innen-Zone
    bleibt offen). Das dokumentierte Risiko der anderen Richtung ist „Maske zu
    groß → ein Hof/Vorplatz wird gedeckt" (Diagnose Z.1230). Hier im
    Barawitzka-Muster: zwei Trakte mit 12 m Abstand, eine ZIMMER-Zone ragt 6 m
    in den Zwischenraum. Mit 5000 mm bleiben es zwei Maskenkomponenten, der
    Zwischenraum bleibt AUSSEN; ein deutlich größerer Knopf verbindet die
    Trakte und deckt ihn mit (gemessen: bei `_MASKE_MM` = 60000 fällt genau
    dieser Test, die vier übrigen S2-Tests bleiben grün).
    """
    koerper = _ring(0, 0, 20000, 20000) + _ring(32000, 0, 52000, 20000)
    zimmer = _raum("raum_1", "ZIMMER", _rect(1500, 1500, 26000, 18500))
    plan = _leerer_plan()
    zonen = aussenbereich.waehle_innen_zonen(plan, [zimmer], [])
    ab = erkenne_aussenbereiche(plan, koerper, zonen)
    zwischen = Point(24000, 10000)      # im Zwischenraum, aber INNERHALB der Zone
    assert any(p.covers(zwischen) for p in ab.offen), "Zwischenraum nicht mehr AUSSEN"
    assert not ab.gedeckt().covers(zwischen), "Maske deckt den Trakt-Abstand mit"
    assert ab.gedeckt().covers(Point(10000, 10000)), "Zone im Trakt nicht gedeckt"


def _decke_plan(rechteck) -> DxfPlan:
    """Plan mit EINER geschlossenen Deckenfläche auf einem Decken-Layer."""
    doc = ezdxf.new()
    doc.header["$INSUNITS"] = 4
    msp = doc.modelspace()
    doc.layers.add("0._EG PP_2_210 Decke")
    (x0, y0), (x1, y1) = rechteck
    msp.add_lwpolyline([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], close=True,
                       dxfattribs={"layer": "0._EG PP_2_210 Decke"})
    return DxfPlan(doc=doc, space=msp, factor=1.0)


def test_ueberdachung_nur_bei_nicht_flaechendeckendem_deckenlayer():
    """Flächendeckende Decke (Rennweg-Muster) → nichts; ein Deckenstück über
    der offenen Außenfläche zwischen zwei Trakten → eine Überdachung."""
    koerper = _ring(0, 0, 20000, 20000) + _ring(30000, 0, 50000, 20000)
    ab = erkenne_aussenbereiche(_leerer_plan(), koerper)
    gebaeude = unary_union(ab.komponenten)

    voll = _decke_plan(((0, 0), (50000, 20000)))     # deckt 100 % des Gebäudes
    assert ueberdachungen(voll, gebaeude, ab.offen) == []

    vordach = _decke_plan(((22000, 5000), (28000, 15000)))   # 6 × 10 m im Hof
    treffer = ueberdachungen(vordach, gebaeude, ab.offen)
    assert len(treffer) == 1
    assert abs(treffer[0].area / 1e6 - 60.0) < 0.1
