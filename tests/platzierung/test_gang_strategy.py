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


def _welt_pfeil_az(rotation_deg: float) -> float:
    # Welt-Azimut des down-Blocks (Basis 270°) bei gegebener INSERT-Rotation.
    return (270.0 + rotation_deg) % 360.0


def test_gerader_gang_down_typ_entgegen_flucht():
    # NB-R06: im GERADEN Gang sind die Zwischen-RZ down-Typ „geradeaus" und so
    # gedreht, dass der Welt-Pfeil ENTGEGEN der Fluchtrichtung zeigt (Front schaut
    # die ankommende Person an) — NICHT mehr ein Richtungspfeil zum Ausgang.
    # Ausgang rechts (Ost) → Flucht Ost → Welt-Pfeil West (~180°).
    rechts = plan_rettungszeichen_gang(_gang_ohne_fluchtweglayer(30000.0), FakeNormProvider())
    assert rechts and all(p.richtung == "unten" for p in rechts)
    # Zwischenpunkte (nicht das Ziel-Ende) zeigen den Welt-Pfeil nach West.
    innere = rechts[:-1] if len(rechts) > 1 else rechts
    assert all(abs(_welt_pfeil_az(p.rotation_deg) - 180.0) < 5.0 for p in innere)
    # Ausgang links (West) → Flucht West → Welt-Pfeil Ost (~0°).
    links = plan_rettungszeichen_gang(_gang_ohne_fluchtweglayer(0.0), FakeNormProvider())
    assert links and all(p.richtung == "unten" for p in links)
    innere_l = links[:-1] if len(links) > 1 else links
    assert all(_welt_pfeil_az(p.rotation_deg) < 5.0 or _welt_pfeil_az(p.rotation_deg) > 355.0
               for p in innere_l)


def test_ist_abzweig_trennt_gerade_von_ecke():
    # NB-R07-Kern: 90°-Knick = Abzweig, kollineare Fortsetzung = geradeaus.
    from notbeleuchtung.platzierung.gang_strategy import _ist_abzweig
    assert _ist_abzweig(1000.0, 0.0, 0.0, 1000.0)          # Ost → Nord = Ecke
    assert _ist_abzweig(0.0, 1000.0, 1000.0, 0.0)          # Nord → Ost = Ecke
    assert not _ist_abzweig(1000.0, 0.0, 1000.0, 0.0)      # Ost → Ost = geradeaus
    assert not _ist_abzweig(1000.0, 0.0, 900.0, 100.0)     # leichte Schwenkung < 45°
    assert not _ist_abzweig(0.0, 0.0, 1000.0, 0.0)         # kein Einlauf → geradeaus


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
