"""Tests rest_komponenten — synthetische Wandkörper, keine DXF nötig."""
from __future__ import annotations

from shapely.geometry import Point, Polygon

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


def test_rest_findet_rechten_raum_und_schacht():
    raeume = komponenten_ohne_stempel(None, _WAENDE, [_TUER], [_LINKS])
    typen = sorted(r.raum_typ for r in raeume)
    assert "SCHACHT" in typen                      # türlose Kleinfläche
    gross = max(raeume, key=lambda r: r.flaeche_m2)
    assert gross.raum_typ == "UNBEKANNT"
    assert 8.0 <= gross.flaeche_m2 <= 14.0         # rechter Raum minus Schacht-Box
    # Belegter linker Raum liefert KEINE Rest-Komponente.
    links = Polygon(_LINKS)
    assert not any(links.covers(Point(*r.polygon_mm[0])) and links.covers(
        Polygon(r.polygon_mm).centroid) for r in raeume)
    assert all(r.id.startswith("rest_") for r in raeume)


def test_ohne_waende_leer():
    assert komponenten_ohne_stempel(None, [], [], []) == []
