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


def test_ausgangs_rz_pfeil_zeigt_zur_tuer():
    # Owner-Korrektur (H-Gebäude-DXF 2026-09-05): am Ausgang hängt IMMER das
    # Pfeil-unten-Zeichen, rotiert, sodass der Pfeil ZUR TÜR zeigt. Referenzfall:
    # Stiegenhaus-Tür OBERHALB des Gangs → Block um 180° gedreht (Pfeil nach oben).
    from notbeleuchtung.hauptengine.contracts import Edge, Node, Tuer, ZirkulationsGraph
    from notbeleuchtung.platzierung.anker_strategy import plan_rettungszeichen_anker

    raum = _raum([{"id": "ex1", "xy_mm": [1000.0, 5000.0], "typ": "stair_exit"}])
    raum.tueren.append(Tuer(id="t1", xy_mm=(1000.0, 5000.0), breite_mm=1000,
                            ist_notausgang=True))
    raum.zirkulation = ZirkulationsGraph(
        nodes=[Node(id="ex1", typ="exit", xy_mm=(1000.0, 5000.0)),
               Node(id="g1", typ="junction", xy_mm=(1000.0, 1000.0)),
               Node(id="g0", typ="junction", xy_mm=(4000.0, 1000.0)),
               Node(id="g2", typ="junction", xy_mm=(1000.0, -3000.0))],
        edges=[Edge(**{"from": "g1", "to": "ex1", "len_mm": 4000}),
               Edge(**{"from": "g0", "to": "g1", "len_mm": 3000}),
               Edge(**{"from": "g2", "to": "g1", "len_mm": 4000})],
    )
    rz = [p for p in plan_rettungszeichen_anker(raum, FakeNormProvider())
          if p.xy_mm == (1000.0, 5000.0)]
    assert len(rz) == 1
    # Tür liegt OBERHALB (Anlauf von unten) → unten-Block um 180° = Pfeil nach oben.
    assert rz[0].richtung == "unten"
    assert abs(rz[0].rotation_deg - 180.0) < 1.0
