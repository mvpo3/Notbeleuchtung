"""lux — Punktmethode-Beleuchtungsstärke + EN-1838-Bewertung (Mindest-Lux, Ud)."""
from notbeleuchtung.platzierung.lux import lux_raster

BOUNDS = (0.0, 0.0, 10000.0, 10000.0)  # 10 × 10 m Raum


def test_einzelleuchte_ungleichmaessig():
    r = lux_raster([(5000.0, 5000.0)], BOUNDS, montagehoehe_m=2.5, i_cd=2000.0, raster_mm=500.0)
    assert r.max_lux > r.min_lux > 0.0
    assert r.ud < 0.5                         # eine Leuchte → schlechte Gleichmäßigkeit


def test_raster_besser_als_einzeln():
    grid = [(x, y) for x in (2500.0, 5000.0, 7500.0) for y in (2500.0, 5000.0, 7500.0)]
    r = lux_raster(grid, BOUNDS, montagehoehe_m=2.5, i_cd=2000.0, raster_mm=500.0)
    einzeln = lux_raster([(5000.0, 5000.0)], BOUNDS, montagehoehe_m=2.5, i_cd=2000.0, raster_mm=500.0)
    assert r.min_lux > einzeln.min_lux        # 3×3-Raster hebt das Minimum
    assert r.ud > einzeln.ud                  # und die Gleichmäßigkeit


def test_antipanik_kriterium_05lx():
    grid = [(x, y) for x in (2500.0, 5000.0, 7500.0) for y in (2500.0, 5000.0, 7500.0)]
    r = lux_raster(grid, BOUNDS, i_cd=2000.0, ziel_lux=0.5, raster_mm=500.0)
    assert r.erfuellt_min is (r.min_lux >= 0.5)
    assert r.erfuellt_ud is (r.ud >= 1.0 / 40.0)


def test_ohne_leuchten_null():
    r = lux_raster([], BOUNDS)
    assert r.min_lux == 0.0 and r.erfuellt_min is False


def test_i_cd_fn_konstant_gleich_i_cd():
    # Ein Callable, das immer denselben Wert liefert, muss identisch zur i_cd-Konstante sein.
    grid = [(5000.0, 5000.0)]
    konst = lux_raster(grid, BOUNDS, i_cd=1500.0, raster_mm=500.0)
    per_fn = lux_raster(grid, BOUNDS, i_cd_fn=lambda _g: 1500.0, raster_mm=500.0)
    assert per_fn.max_lux == konst.max_lux
    assert per_fn.min_lux == konst.min_lux


def test_i_cd_fn_ueberschreibt_i_cd():
    # Bei gesetztem i_cd_fn wird i_cd ignoriert.
    grid = [(5000.0, 5000.0)]
    r = lux_raster(grid, BOUNDS, i_cd=9999.0, i_cd_fn=lambda _g: 1500.0, raster_mm=500.0)
    ref = lux_raster(grid, BOUNDS, i_cd=1500.0, raster_mm=500.0)
    assert r.max_lux == ref.max_lux


def test_naht_echte_ldt_photometrie():
    # End-to-End F2→F1: Hersteller-Photometrie als i_cd_fn injiziert (γ in Grad).
    from pathlib import Path

    from notbeleuchtung.normwissen.photometrie import lade_ldt

    photo = lade_ldt(Path(__file__).parent.parent / "fixtures" / "photometrie" / "mini.ldt")
    grid = [(5000.0, 5000.0)]
    r = lux_raster(grid, BOUNDS, montagehoehe_m=2.5, i_cd_fn=photo.intensitaet, raster_mm=500.0)
    # mini.ldt strahlt zur Seite schwächer (I fällt 200→0 cd) → Randminimum sinkt unter
    # den isotropen Fall mit demselben Nadir-Wert (200 cd).
    iso = lux_raster(grid, BOUNDS, montagehoehe_m=2.5, i_cd=200.0, raster_mm=500.0)
    assert r.max_lux > 0.0
    assert r.min_lux < iso.min_lux
