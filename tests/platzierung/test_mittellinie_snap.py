"""mittellinie_snap — R1 (Owner-Korrektur 2026-09-11): Gang-Notleuchten liegen auf der
Linie der BESTANDS-Allgemeinbeleuchtung („immer in einer Linie mit der Beleuchtung");
ohne Bestand auf der Bbox-Kurzachsen-Mitte (Regel A, 2026-09-10)."""
import pytest

from notbeleuchtung.hauptengine.contracts import BBox, Platzierung, Raum, RaumModell
from notbeleuchtung.platzierung.mittellinie_snap import snappe_auf_mittellinie

_GANG = [(0.0, 0.0), (20000.0, 0.0), (20000.0, 1500.0), (0.0, 1500.0)]


def _raum() -> RaumModell:
    return RaumModell(
        floor="T", bounds_mm=BBox(min_xy=(0.0, 0.0), max_xy=(20000.0, 1500.0)),
        raeume=[Raum(id="g", raum_typ="GANG", polygon_mm=_GANG, ist_fluchtweg=True)],
    )


def _sl(xy):
    return Platzierung(
        xy_mm=xy, catalog_key="sicherheitsleuchte_aufheller", rotation_deg=0.0,
        height_mm=2400.0, kind="sicherheitsleuchte", richtung="gerade",
        circuit_hint="AGV-A-F13", covers_segment=[], norm_quelle="EN 1838",
    )


def test_ohne_bestand_snappt_auf_bbox_mitte():
    out = snappe_auf_mittellinie([_sl((10000.0, 400.0))], _raum())
    assert out[0].xy_mm == pytest.approx((10000.0, 750.0))


def test_bestand_linie_schlaegt_bbox_mitte():
    """Beleg Elektroplan DE: Spot-Reihe y=1000, Bbox-Mitte 750 → Symbol auf 1000."""
    bestand = ((3000.0, 1000.0), (9000.0, 1000.0), (15000.0, 1000.0))
    out = snappe_auf_mittellinie([_sl((10000.0, 400.0))], _raum(), bestand_leuchten_mm=bestand)
    assert out[0].xy_mm == pytest.approx((10000.0, 1000.0))


def test_gestreuter_bestand_ist_keine_linie():
    """Querstreuung > 600 mm (versetzte Leuchten) → keine Reihe → Bbox-Mitte bleibt."""
    bestand = ((3000.0, 200.0), (9000.0, 1300.0))
    out = snappe_auf_mittellinie([_sl((10000.0, 400.0))], _raum(), bestand_leuchten_mm=bestand)
    assert out[0].xy_mm == pytest.approx((10000.0, 750.0))


def test_einzelner_bestand_punkt_reicht_nicht():
    bestand = ((3000.0, 1000.0),)
    out = snappe_auf_mittellinie([_sl((10000.0, 400.0))], _raum(), bestand_leuchten_mm=bestand)
    assert out[0].xy_mm == pytest.approx((10000.0, 750.0))


def test_bestand_ausserhalb_des_gangs_zaehlt_nicht():
    bestand = ((3000.0, 5000.0), (9000.0, 5000.0))   # nicht im Gang-Polygon
    out = snappe_auf_mittellinie([_sl((10000.0, 400.0))], _raum(), bestand_leuchten_mm=bestand)
    assert out[0].xy_mm == pytest.approx((10000.0, 750.0))
