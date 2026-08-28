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
