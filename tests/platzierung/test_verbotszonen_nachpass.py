"""verbotszonen_nachpass — Platzierungen aus Stiegenhaus-Verbotszonen holen (S1)."""
from notbeleuchtung.hauptengine.contracts import (
    BBox,
    Platzierung,
    Raum,
    RaumModell,
    StiegenhausModell,
)
from notbeleuchtung.platzierung.geometry import point_in_polygon
from notbeleuchtung.platzierung.verbotszonen_nachpass import entferne_aus_verbotszonen

RAUM_POLY = [(0.0, 0.0), (10000.0, 0.0), (10000.0, 10000.0), (0.0, 10000.0)]  # 10×10 m
ZONE = [(4000.0, 0.0), (6000.0, 0.0), (6000.0, 10000.0), (4000.0, 10000.0)]   # Treppenlauf-Streifen


def _raum(stiegenhaeuser=()):
    return RaumModell(
        floor="EG",
        bounds_mm=BBox(min_xy=(0.0, 0.0), max_xy=(10000.0, 10000.0)),
        raeume=[Raum(id="SH1", raum_typ="STIEGENHAUS", polygon_mm=RAUM_POLY)],
        stiegenhaeuser=list(stiegenhaeuser),
    )


def _pl(xy):
    return Platzierung(xy_mm=xy, catalog_key="rettungszeichen", kind="rz")


def test_platzierung_in_verbotszone_wird_verschoben():
    raum = _raum([StiegenhausModell(raum_id="SH1", verbotszonen_mm=[ZONE])])
    out = entferne_aus_verbotszonen([_pl((5000.0, 5000.0))], raum)
    assert len(out) == 1
    assert not point_in_polygon(out[0].xy_mm, ZONE)        # raus aus dem Treppenlauf
    assert point_in_polygon(out[0].xy_mm, RAUM_POLY)       # aber weiter im Stiegenhaus


def test_platzierung_ausserhalb_zone_unveraendert():
    raum = _raum([StiegenhausModell(raum_id="SH1", verbotszonen_mm=[ZONE])])
    out = entferne_aus_verbotszonen([_pl((1000.0, 1000.0))], raum)
    assert out[0].xy_mm == (1000.0, 1000.0)


def test_ohne_verbotszonen_noop():
    p = _pl((5000.0, 5000.0))
    out = entferne_aus_verbotszonen([p], _raum())          # keine stiegenhaeuser
    assert out[0] is p                                     # identisch → echter No-op


def test_uebergrosse_zone_behaelt_punkt():
    # Fehlerhafte/übergroße Hülle deckt den ganzen Raum (Selman-Warnung Mollgasse-SO)
    # → kein montierbarer Punkt → Platzierung bleibt (defensiv, nie löschen).
    ganz = [(-1000.0, -1000.0), (11000.0, -1000.0), (11000.0, 11000.0), (-1000.0, 11000.0)]
    raum = _raum([StiegenhausModell(raum_id="SH1", verbotszonen_mm=[ganz])])
    out = entferne_aus_verbotszonen([_pl((5000.0, 5000.0))], raum)
    assert out[0].xy_mm == (5000.0, 5000.0)


def test_unbekannter_raum_id_noop():
    # Stiegenhaus verweist auf einen Raum, den es nicht gibt → kein Polygon → No-op.
    raum = _raum([StiegenhausModell(raum_id="FEHLT", verbotszonen_mm=[ZONE])])
    p = _pl((5000.0, 5000.0))
    out = entferne_aus_verbotszonen([p], raum)
    assert out[0] is p
