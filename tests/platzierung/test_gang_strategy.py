"""gang_strategy — RZ-Fallback entlang GANG-Mittellinie ohne Fluchtweg-Layer (B2)."""
import json
from pathlib import Path

from fakes import FakeNormProvider
from notbeleuchtung.hauptengine.contracts import (
    Ausgang,
    BBox,
    Raum,
    RaumModell,
)
from notbeleuchtung.platzierung.gang_strategy import plan_rettungszeichen_gang
from notbeleuchtung.platzierung.platzierer import NotlichtPlatzierer

FIXTURES = Path(__file__).parents[1] / "fixtures"


def _gang_ohne_fluchtweglayer(ausgang_x: float = 30000.0) -> RaumModell:
    """30 m langer GANG (Rechteck), 1 Ausgang, KEINE Segmente, KEINE Kreuzung.

    Spiegelt die fischamender-Lage: der Fluchtweg-Layer wurde nicht erkannt →
    zirkulation leer, aber der GANG-Raum ist typisiert + als Fluchtweg markiert.
    """
    poly = [(0.0, 0.0), (30000.0, 0.0), (30000.0, 2000.0), (0.0, 2000.0)]
    return RaumModell(
        floor="FISCH",
        bounds_mm=BBox(min_xy=(0.0, 0.0), max_xy=(30000.0, 2000.0)),
        raeume=[Raum(id="gang1", raum_typ="GANG", polygon_mm=poly, ist_fluchtweg=True)],
        ausgaenge=[Ausgang(id="EXIT", xy_mm=(ausgang_x, 1000.0), typ="final_exit")],
    )


def test_fallback_setzt_rz_entlang_gang():
    out = plan_rettungszeichen_gang(_gang_ohne_fluchtweglayer(), FakeNormProvider())
    assert out, "GANG-Fallback muss RZ liefern, wenn ein Fluchtweg-GANG existiert"
    assert all(p.kind == "rz" for p in out)
    # Alle RZ liegen im GANG-Polygon-Streifen (0..30000 x, ~1000 y = Mittelachse).
    assert all(0.0 <= p.xy_mm[0] <= 30000.0 for p in out)
    # Naht: kein Segment gedeckt (es gibt keine), Norm-Quelle gesetzt.
    assert all(p.covers_segment == [] for p in out)
    assert all(p.norm_quelle for p in out)


def test_pfeil_zeigt_zum_ausgang():
    # Ausgang rechts (x=30000) → Pfeile nach rechts.
    rechts = plan_rettungszeichen_gang(_gang_ohne_fluchtweglayer(30000.0), FakeNormProvider())
    assert rechts and all(p.richtung == "rechts" for p in rechts)
    # Ausgang links (x=0) → Pfeile nach links.
    links = plan_rettungszeichen_gang(_gang_ohne_fluchtweglayer(0.0), FakeNormProvider())
    assert links and all(p.richtung == "links" for p in links)


def test_kein_gang_kein_rz():
    raum = RaumModell(
        floor="X", bounds_mm=BBox(min_xy=(0.0, 0.0), max_xy=(1000.0, 1000.0)),
        raeume=[Raum(id="wc", raum_typ="WC", polygon_mm=[(0.0, 0.0), (1000.0, 0.0), (1000.0, 1000.0)])],
    )
    assert plan_rettungszeichen_gang(raum, FakeNormProvider()) == []


def test_dispatcher_nutzt_fallback_ohne_segment_und_kreuzung():
    # place() muss über den Fallback RZ setzen, wenn Segment- + Anker-Strategie leer sind.
    erg = NotlichtPlatzierer().place(_gang_ohne_fluchtweglayer(), FakeNormProvider())
    assert any(p.kind == "rz" for p in erg.platzierungen)


def test_dispatcher_bevorzugt_segmente_wenn_vorhanden():
    # 4OG-Fixture hat Segmente → Segment-Strategie (5 RZ), NICHT der GANG-Fallback.
    data = json.loads((FIXTURES / "raum_modell_4og.json").read_text(encoding="utf-8"))
    erg = NotlichtPlatzierer().place(RaumModell.model_validate(data), FakeNormProvider())
    rz = [p for p in erg.platzierungen if p.kind == "rz"]
    assert len(rz) == 5
    assert all(p.covers_segment for p in rz)  # Segment-RZ decken je 1 Segment
