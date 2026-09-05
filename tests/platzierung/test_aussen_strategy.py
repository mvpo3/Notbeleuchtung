"""aussen_strategy — SL außerhalb jedes Schlussausgangs (EN 1838 §4.1.2 b)."""
import json
from pathlib import Path

from fakes import FakeNormProvider
from notbeleuchtung.hauptengine.contracts import RaumModell
from notbeleuchtung.platzierung.aussen_strategy import plan_aussenleuchten

FIXTURES = Path(__file__).parents[1] / "fixtures"


def _raum(ausgaenge) -> RaumModell:
    data = json.loads((FIXTURES / "raum_modell_4og.json").read_text(encoding="utf-8"))
    data["ausgaenge"] = ausgaenge
    return RaumModell.model_validate(data)


def _bounds(raum):
    return raum.bounds_mm.min_xy, raum.bounds_mm.max_xy


def test_final_exit_bekommt_aussenleuchte():
    basis = _raum([])
    (min_x, min_y), (_max_x, max_y) = _bounds(basis)
    ex = (min_x, (min_y + max_y) / 2.0)   # Schlussausgang am linken Gebäuderand
    raum = _raum([{"id": "ex1", "xy_mm": list(ex), "typ": "final_exit"}])
    out = plan_aussenleuchten(raum, FakeNormProvider())
    assert len(out) == 1
    p = out[0]
    assert p.kind == "sicherheitsleuchte"
    # Auswärts: Leuchte sitzt links AUSSERHALB der Gebäude-Bounds …
    assert p.xy_mm[0] < min_x
    # … und „nahe" (≤ 2 m, ANMERKUNG 1).
    d = ((p.xy_mm[0] - ex[0]) ** 2 + (p.xy_mm[1] - ex[1]) ** 2) ** 0.5
    assert d <= 2000.0


def test_stair_exit_loest_nichts_aus():
    raum = _raum([{"id": "s1", "xy_mm": [0.0, 500.0], "typ": "stair_exit"}])
    assert plan_aussenleuchten(raum, FakeNormProvider()) == []


def test_place_integriert_aussenleuchte():
    from notbeleuchtung.platzierung import NotlichtPlatzierer

    mit = _raum([{"id": "ex1", "xy_mm": [0.0, 500.0], "typ": "final_exit"}])
    ohne = _raum([{"id": "s1", "xy_mm": [0.0, 500.0], "typ": "stair_exit"}])
    n_mit = len(NotlichtPlatzierer().place(mit, FakeNormProvider()).platzierungen)
    n_ohne = len(NotlichtPlatzierer().place(ohne, FakeNormProvider()).platzierungen)
    assert n_mit == n_ohne + 1
