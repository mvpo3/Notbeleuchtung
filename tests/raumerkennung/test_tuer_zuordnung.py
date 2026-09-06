"""tuer_zuordnung — von_raum/nach_raum aus Probepunkten beidseits der Sehne."""
from __future__ import annotations

from shapely.geometry import Polygon, box

from notbeleuchtung.hauptengine.contracts.raum_modell import Raum, Tuer
from notbeleuchtung.raumerkennung.tuer_zuordnung import (
    AUSSEN,
    KEIN_RAUM,
    durchgaenge_ohne_tuerblatt,
    ordne_tueren,
)
from notbeleuchtung.raumerkennung.tueren import TuerOeffnung


def _raum(rid, x0, y0, x1, y1, typ="ZIMMER"):
    return Raum(id=rid, raum_typ=typ,
                polygon_mm=[(x0, y0), (x1, y0), (x1, y1), (x0, y1)],
                flaeche_m2=(x1 - x0) * (y1 - y0) / 1e6)


def test_tuer_zwischen_zwei_raeumen():
    # Zwei Räume, Trennwand bei x=5000, Tür in der Wand (Sehne läuft in y).
    raeume = [_raum("a", 0, 0, 4900, 4000), _raum("b", 5100, 0, 10000, 4000)]
    t = Tuer(id="t1", xy_mm=(5000.0, 2000.0), breite_mm=800)
    o = TuerOeffnung(xy_mm=(5000.0, 2000.0), breite_mm=800, winkel_grad=90.0,
                     quelle="block")
    ordne_tueren([t], [o], raeume, box(0, 0, 10000, 4000))
    assert {t.von_raum, t.nach_raum} == {"a", "b"}


def test_aussentuer_und_kein_raum():
    raeume = [_raum("a", 0, 0, 4900, 4000)]
    kontur = Polygon([(0, 0), (5000, 0), (5000, 4000), (0, 4000)])
    t = Tuer(id="t1", xy_mm=(5000.0, 2000.0), breite_mm=900)
    o = TuerOeffnung(xy_mm=(5000.0, 2000.0), breite_mm=900, winkel_grad=90.0,
                     quelle="arc")
    ordne_tueren([t], [o], raeume, kontur)
    assert {t.von_raum, t.nach_raum} == {"a", AUSSEN}
    # Ohne Kontur wird die freie Seite KEIN_RAUM.
    t2 = Tuer(id="t2", xy_mm=(5000.0, 2000.0), breite_mm=900)
    ordne_tueren([t2], [o], raeume, None)
    assert KEIN_RAUM in (t2.von_raum, t2.nach_raum)


def test_durchgang_ohne_tuerblatt():
    # Zwei Räume, Wand bei x=5000..5200 mit 1.2-m-Lücke (y 1400..2600) und
    # KEINER bekannten Tür → Durchgang > 800 mm mit ohne_tuerblatt=True.
    raeume = [_raum("a", 0, 0, 5000, 4000), _raum("b", 5200, 0, 10000, 4000)]
    wand = box(5000, 0, 5200, 1400).union(box(5000, 2600, 5200, 4000))
    (d,) = durchgaenge_ohne_tuerblatt(raeume, [], wand)
    assert d.ohne_tuerblatt and d.breite_mm > 800
    assert {d.von_raum, d.nach_raum} == {"a", "b"}


def test_durchgang_nicht_wo_tuer_ist():
    raeume = [_raum("a", 0, 0, 5000, 4000), _raum("b", 5200, 0, 10000, 4000)]
    wand = box(5000, 0, 5200, 1400).union(box(5000, 2600, 5200, 4000))
    tuer = Tuer(id="t1", xy_mm=(5100.0, 2000.0), breite_mm=1200)
    assert durchgaenge_ohne_tuerblatt(raeume, [tuer], wand) == []
