"""mittellinie — mediale Achse (skeletonize) + Leuchten-Sampling entlang der Linie."""
from itertools import pairwise

from notbeleuchtung.platzierung.mittellinie import leuchten_auf_linie, mittellinie

# Breiter Gang 10 m × 2 m.
GANG = [(0.0, 0.0), (10000.0, 0.0), (10000.0, 2000.0), (0.0, 2000.0)]


def test_mittellinie_rechteck_liegt_mittig():
    pts = mittellinie(GANG, raster_mm=200.0)
    assert len(pts) > 10
    ys = sorted(p[1] for p in pts)
    median_y = ys[len(ys) // 2]
    assert 800.0 <= median_y <= 1200.0            # ~Mitte (y≈1000)
    xspan = max(p[0] for p in pts) - min(p[0] for p in pts)
    assert xspan > 5000.0                          # Achse läuft längs durch


def test_leuchten_auf_linie_abstand():
    leuchten = leuchten_auf_linie(GANG, abstand_mm=2500.0, raster_mm=200.0)
    assert len(leuchten) >= 3
    # aufeinanderfolgende Kandidaten haben ~>= geforderten Abstand
    for (x0, y0), (x1, y1) in pairwise(leuchten):
        assert ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5 >= 2000.0


def test_leeres_polygon():
    assert mittellinie([(0.0, 0.0), (1.0, 1.0)]) == []
