"""deckung — Lux-getriebene Gang-Verdichtung (Linie + Deckung)."""
import json
from pathlib import Path

from fakes import FakeNormProvider
from notbeleuchtung.hauptengine.contracts import BBox, Raum, RaumModell
from notbeleuchtung.platzierung.deckung import verdichte_fluchtweg

FIXTURES = Path(__file__).parents[1] / "fixtures"
GANG_POLY = [(0.0, 0.0), (15000.0, 0.0), (15000.0, 2400.0), (0.0, 2400.0)]


def _gang_raum() -> RaumModell:
    return RaumModell(
        floor="X",
        bounds_mm=BBox(min_xy=(0.0, 0.0), max_xy=(15000.0, 2400.0)),
        raeume=[Raum(id="gang1", raum_typ="GANG", polygon_mm=GANG_POLY, ist_fluchtweg=True)],
    )


def test_verdichtet_gang_mit_sicherheitsleuchten():
    out = verdichte_fluchtweg(_gang_raum(), FakeNormProvider())
    assert len(out) >= 2
    assert all(p.kind == "sicherheitsleuchte" for p in out)
    assert all(p.catalog_key == "sicherheitsleuchte_aufheller" for p in out)
    # alle innerhalb des Gangs
    for p in out:
        assert 0.0 <= p.xy_mm[0] <= 15000.0 and 0.0 <= p.xy_mm[1] <= 2400.0


def test_niedrige_lichtstaerke_verdichtet_staerker():
    wenig_licht = verdichte_fluchtweg(_gang_raum(), FakeNormProvider(), i_cd=3.0)
    viel_licht = verdichte_fluchtweg(_gang_raum(), FakeNormProvider(), i_cd=2000.0)
    assert len(wenig_licht) >= len(viel_licht)  # schwächere Leuchte → engerer Abstand


def test_keine_korridore_keine_verdichtung():
    # 4OG-Fixture: nur STIEGENHAUS, kein GANG/FLUR → nichts hinzufügen.
    data = json.loads((FIXTURES / "raum_modell_4og.json").read_text(encoding="utf-8"))
    assert verdichte_fluchtweg(RaumModell.model_validate(data), FakeNormProvider()) == []
