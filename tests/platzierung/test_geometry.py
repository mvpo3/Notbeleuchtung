"""Unit-Tests für die portierten Geometrie-Primitive (platzierung/geometry.py)."""
from notbeleuchtung.platzierung import geometry as geo

# Einheits-Quadrat 0..10.
SQUARE = [(0.0, 0.0), (10.0, 0.0), (10.0, 10.0), (0.0, 10.0)]


def test_point_in_polygon_innen_aussen_rand():
    assert geo.point_in_polygon((5.0, 5.0), SQUARE) is True
    assert geo.point_in_polygon((20.0, 5.0), SQUARE) is False
    assert geo.point_in_polygon((0.0, 5.0), SQUARE) is True   # Rand zählt als innen


def test_point_in_polygon_doppelter_schluss_vertex():
    """Null-Kante (doppelter Vertex) darf point_in_polygon nicht auf konstant
    True kippen (Regression aus dem Port-Kommentar)."""
    poly = SQUARE + [(0.0, 0.0)]           # Schluss-Vertex doppelt
    assert geo.point_in_polygon((5.0, 5.0), poly) is True
    assert geo.point_in_polygon((50.0, 50.0), poly) is False


def test_find_center_rechteck():
    assert geo.find_center_diagonal(SQUARE) == (5.0, 5.0)
    # Nahezu rechteckig → find_center_visual fällt auf die Bbox-Mitte zurück.
    assert geo.find_center_visual(SQUARE) == (5.0, 5.0)


def test_room_main_axis():
    breit = [(0.0, 0.0), (10.0, 0.0), (10.0, 2.0), (0.0, 2.0)]
    hoch = [(0.0, 0.0), (2.0, 0.0), (2.0, 10.0), (0.0, 10.0)]
    assert geo.room_main_axis(breit) == "horizontal"
    assert geo.room_main_axis(hoch) == "vertical"


def test_offset_point():
    assert geo.offset_point((0.0, 0.0), "horizontal", 5.0) == (5.0, 0.0)
    assert geo.offset_point((0.0, 0.0), "vertical", 5.0, positive=False) == (0.0, -5.0)


def test_grid_points_n1_ist_zentrum():
    assert geo.grid_points(SQUARE, 1) == [(5.0, 5.0)]
    assert geo.grid_points(SQUARE, 0) == [(5.0, 5.0)]


def test_grid_points_raster_liegt_innen_und_verteilt():
    pts = geo.grid_points(SQUARE, 4)
    assert len(pts) == 4
    assert len(set(pts)) == 4                              # verschiedene Positionen
    assert all(geo.point_in_polygon(p, SQUARE) for p in pts)  # alle im Raum
    # 2×2 im Einheits-Quadrat 0..10 → Viertelpunkte
    assert set(pts) == {(2.5, 2.5), (7.5, 2.5), (2.5, 7.5), (7.5, 7.5)}


def test_grid_points_l_form_wirft_aussenpunkte_raus():
    # L-Form: rechteck-Raster würde Punkte in die fehlende Ecke legen → müssen raus.
    l_shape = [(0.0, 0.0), (10.0, 0.0), (10.0, 4.0), (4.0, 4.0), (4.0, 10.0), (0.0, 10.0)]
    pts = geo.grid_points(l_shape, 4)
    assert all(geo.point_in_polygon(p, l_shape) for p in pts)
