"""Abschnitt 5 (Owner-Entscheid 6, 2026-10-01): Ausgang = Übergang ins Freie, mit
oder ohne Tür; Innenhof = Loch in der äußeren Gebäudekontur, kein Ausgang und
kein Fluchtziel (``docs/AUFTRAG_2026-10-01.md`` § 5, ``LUECKEN.md`` § 27).

Synthetischer Plan „Loch in der Kontur" — die Figur von Mollgasse EG ``exit_1``:
Gebäude 30 × 20 m (500-mm-HATCH-Wände mit Linien), an der Ostseite ein Hof 9,5 × 10 m
zwischen zwei Flügeln, nach Osten nur durch einen 200-mm-Streifen OHNE Linien
geschlossen (Wandkörper, aber keine Wand-Linie — wie ``01-ANS`` in Mollgasse).
Die Außen-Analyse (Wandkörper) sieht darum ein Loch der Außenkontur, der
Raster-Umriss von ``footprint`` (Wand-Linien) eine offene Bucht: ein
Doppeltür-Bogenpaar in der Hofwand liegt an seinem Rand und wurde vor
Abschnitt 5 ``final_exit``. Dazu eine echte Doppeltür in der Südfassade (ins
Freie), eine Straßentür und eine Hoftür (je Einzeltür) aus dem Gang. Wie Loch 0
in Mollgasse trägt der Hof kein Außen-Indiz: die Geometrie entscheidet.
"""
from __future__ import annotations

import math

import ezdxf
import pytest
from shapely.geometry import Point, box

from notbeleuchtung.hauptengine.contracts.raum_modell import Ausgang
from notbeleuchtung.raumerkennung import ArchitekturRaumProvider
from notbeleuchtung.raumerkennung.tuer_zuordnung import AUSSEN

# Wanddicke 500 mm: die Außen-Analyse schließt die Wand-Union mit 8-Eck-Puffern
# (quad_segs 2) — eine 1,5-m-Doppeltür in einer 300-mm-Wand bleibt dort ein
# Schlitz, und das Loch wäre keines (gemessen: Brücke 0 mm; 500 mm: 61 mm).
_W = 500.0
FASSADE_DOPPELTUER = (5000.0, 0.0)      # Mitte der Doppeltür in der Südfassade
HOF_DOPPELTUER = (20000.0, 12600.0)     # Mitte der Doppeltür Gang → Hof
STRASSENTUER = (14500.0, _W)            # Angel der Einzeltür Gang → Straße
HOFTUER = (20000.0, 9000.0)             # Angel der Einzeltür Gang → Hof
HOF_MITTE = (25000.0, 10000.0)


def _wand(msp, x0, y0, x1, y1, linien=True, layer="A-WALL"):
    h = msp.add_hatch(color=7, dxfattribs={"layer": layer})
    pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    h.paths.add_polyline_path(pts, is_closed=True)
    if linien:
        for a, b in zip(pts, pts[1:] + pts[:1], strict=True):
            msp.add_line(a, b, dxfattribs={"layer": layer})


def loch_in_kontur_dxf(pfad) -> str:
    doc = ezdxf.new()
    doc.header["$INSUNITS"] = 4
    for layer in ("A-WALL", "A-DOOR", "A-TEXT", "01-ANS-G00-LEG-M0"):
        doc.layers.add(layer)
    msp = doc.modelspace()
    # Außenwände; Südfassade mit Doppeltür (x 4 250 … 5 750) und Straßentür
    # (x 14 500 … 15 600), Ostfassade nur an den Flügelköpfen
    _wand(msp, 0, 0, 4250, _W)
    _wand(msp, 5750, 0, 14500, _W)
    _wand(msp, 15600, 0, 30000, _W)
    _wand(msp, 0, 20000 - _W, 30000, 20000)
    _wand(msp, 0, _W, _W, 20000 - _W)
    _wand(msp, 30000 - _W, _W, 30000, 5000)
    _wand(msp, 30000 - _W, 15000, 30000, 20000 - _W)
    # Hof x 20 000 … 29 500, y 5 000 … 15 000; Westwand mit Hoftür
    # (y 9 000 … 10 100) und Doppeltür (y 11 850 … 13 350)
    _wand(msp, 20000, 5000 - _W, 30000 - _W, 5000)
    _wand(msp, 20000, 15000, 30000 - _W, 15000 + _W)
    _wand(msp, 20000 - _W, 5000 - _W, 20000, 9000)
    _wand(msp, 20000 - _W, 10100, 20000, 11850)
    _wand(msp, 20000 - _W, 13350, 20000, 15000 + _W)
    # Ostseite des Hofs: 200-mm-Ziegelstreifen ohne Linien (Wandkörper, keine
    # Wand-Linie) — schließt die Außenkontur, nicht den Raster-Umriss
    _wand(msp, 29800, 5000, 30000, 15000, linien=False, layer="01-ANS-G00-LEG-M0")
    # Türbögen. Doppeltüren: zwei Blätter r 750, Drehpunkte 1 500 mm auseinander;
    # Einzeltüren r 1 100 (paaren sich mit keinem Bogen)
    msp.add_arc((4250, 0), 750, 270, 360, dxfattribs={"layer": "A-DOOR"})
    msp.add_arc((5750, 0), 750, 180, 270, dxfattribs={"layer": "A-DOOR"})
    msp.add_arc((20000, 11850), 750, 0, 90, dxfattribs={"layer": "A-DOOR"})
    msp.add_arc((20000, 13350), 750, 270, 360, dxfattribs={"layer": "A-DOOR"})
    msp.add_arc(STRASSENTUER, 1100, 0, 90, dxfattribs={"layer": "A-DOOR"})
    msp.add_arc(HOFTUER, 1100, 0, 90, dxfattribs={"layer": "A-DOOR"})
    for text, xy in (("GANG", (10000, 10000)), ("441,00 m²", (10000, 9500))):
        msp.add_text(text, dxfattribs={"insert": xy, "height": 250, "layer": "A-TEXT"})
    doc.saveas(str(pfad))
    return str(pfad)


@pytest.fixture(scope="module")
def lauf(tmp_path_factory):
    prov = ArchitekturRaumProvider()
    dxf = loch_in_kontur_dxf(tmp_path_factory.mktemp("innenhof") / "loch_in_kontur.dxf")
    return prov, prov.parse(dxf, "EG")


def _final_nah(modell, xy, d=1500.0):
    return [a.id for a in modell.ausgaenge
            if a.typ == "final_exit" and math.dist(a.xy_mm, xy) < d]


def test_doppeltuer_in_den_innenhof_ist_kein_ausgang(lauf):
    """Owner-Entscheid 6: die Doppeltür aus dem Gang in den Hof (Loch der
    Außenkontur) ist kein Ausgang und kein Fluchtziel — auch wenn der
    Raster-Umriss sie an den Gebäuderand legt. Der Befund steht in den
    Ausgangs-Warnungen (bericht.md)."""
    prov, m = lauf
    assert _final_nah(m, HOF_DOPPELTUER) == []
    ziele = {s.ziel_ausgang for s in m.zirkulation.segmente if s.ziel_ausgang}
    aus = {a.id: a.xy_mm for a in m.ausgaenge}
    assert not [z for z in ziele if z in aus and math.dist(aus[z], HOF_DOPPELTUER) < 1500.0]
    assert any("mündet nicht ins Freie" in w.grund for w in prov.ausgangs_warnungen), [
        w.grund for w in prov.ausgangs_warnungen]


def test_doppeltuer_ins_freie_bleibt_final_exit(lauf):
    """Owner-Entscheid 6: die Doppeltür in der Südfassade mündet ins Freie
    (außerhalb der Außenkontur) und bleibt ``final_exit``."""
    _, m = lauf
    assert _final_nah(m, FASSADE_DOPPELTUER), [(a.id, a.typ, a.xy_mm) for a in m.ausgaenge]


def test_strassentuer_ist_final_exit_hoftuer_nicht(lauf):
    """Die Einzeltür auf die Straße (Gegenseite AUSSEN) ist ``final_exit``; die
    Einzeltür in den Hof bekommt keine AUSSEN-Seite, ist kein Ausgang und kein
    Fluchtziel. Der Hof ist ein Loch der Außenkontur: von der Komponente
    gedeckt, weder ``offen`` noch Fläche außerhalb der Kontur."""
    prov, m = lauf
    strasse = min(m.tueren, key=lambda t: math.dist(t.xy_mm, STRASSENTUER))
    hof = min(m.tueren, key=lambda t: math.dist(t.xy_mm, HOFTUER))
    assert math.dist(strasse.xy_mm, STRASSENTUER) < 1.0
    assert math.dist(hof.xy_mm, HOFTUER) < 1.0
    typ = {a.id: a.typ for a in m.ausgaenge}
    assert typ.get(f"exit_{strasse.id}") == "final_exit"
    assert AUSSEN in (strasse.von_raum, strasse.nach_raum)
    assert f"exit_{hof.id}" not in typ
    assert AUSSEN not in (hof.von_raum, hof.nach_raum)
    assert f"exit_{hof.id}" not in {s.ziel_ausgang for s in m.zirkulation.segmente}
    au = prov.letzte_aussenbereiche
    assert any(k.covers(Point(HOF_MITTE)) for k in au.komponenten)
    assert not any(p.covers(Point(HOF_MITTE)) for p in au.offen), [
        round(p.area / 1e6, 1) for p in au.offen]


def test_nur_ins_freie_regel():
    """Die Regel ohne Plan: Freie = außerhalb der Komponenten-Kontur (Löcher
    gefüllt) und außerhalb geschlossener Höfe, Reichweite 500 mm (letzte
    Probestufe der Türseite)."""
    from notbeleuchtung.raumerkennung.ausgaenge import nur_ins_freie
    from notbeleuchtung.raumerkennung.aussenbereich import AussenBereiche

    au = AussenBereiche(komponenten=[box(0, 0, 10000, 10000)],
                        geschlossen=[box(12000, 0, 16000, 10000)])
    ausgaenge = [Ausgang(id=i, xy_mm=xy, typ="final_exit") for i, xy in (
        ("rand", (5000.0, 9900.0)),      # Öffnung in der Fassade: 100 mm zur Freie
        ("innen", (5000.0, 5000.0)),     # Loch/Gebäude: 5 m zur Freie
        ("frei", (11000.0, 5000.0)),     # zwischen Kontur und geschlossenem Hof
        ("hof", (14000.0, 5000.0)),      # im geschlossenen Hof
    )]
    bleiben, warnungen = nur_ins_freie(ausgaenge, au, "EG")
    assert [a.id for a in bleiben] == ["rand", "frei"]
    assert [w.grund.split()[0] for w in warnungen] == ["innen", "hof"]
    assert all(w.geschoss == "EG" for w in warnungen)
    assert nur_ins_freie(ausgaenge, None, "EG") == (ausgaenge, [])
    assert nur_ins_freie(ausgaenge, AussenBereiche(), "EG") == (ausgaenge, [])
