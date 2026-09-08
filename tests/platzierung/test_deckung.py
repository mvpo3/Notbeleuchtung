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


class _MfNormProvider(FakeNormProvider):
    """Enis-Double, dessen NormAnforderung zusätzlich einen Wartungsfaktor trägt.

    Modelliert die künftige Norm-Naht (`NormAnforderung.wartungsfaktor`, Enis/3-Owner)
    per Duck-Typing — die reale NormAnforderung kennt das Feld heute noch nicht, der
    Konsum in `deckung` liest es defensiv via getattr.
    """

    def __init__(self, wartungsfaktor: float) -> None:
        super().__init__()
        self._wf = wartungsfaktor

    def fuer_raum(self, raum_typ: str, ist_fluchtweg: bool):
        return _mit_wf(super().fuer_raum(raum_typ, ist_fluchtweg), self._wf)


class _AnfMitWf:
    """Leichter Proxy: reicht alle Attribute an die echte Anforderung durch, plus wf."""

    def __init__(self, anf, wf: float) -> None:
        self._anf = anf
        self.wartungsfaktor = wf

    def __getattr__(self, name):
        return getattr(self._anf, name)


def _mit_wf(anf, wf: float):
    return _AnfMitWf(anf, wf)


def test_wartungsfaktor_verdichtet_staerker():
    # Aktivierter MF (< 1) senkt die nutzbare Beleuchtungsstärke → dichtere Platzierung.
    ohne_mf = verdichte_fluchtweg(_gang_raum(), FakeNormProvider(), i_cd=300.0)
    mit_mf = verdichte_fluchtweg(_gang_raum(), _MfNormProvider(0.5), i_cd=300.0)
    assert len(mit_mf) >= len(ohne_mf)


def test_wartungsfaktor_getattr_default_inert():
    # Ohne wartungsfaktor-Feld (heutige NormAnforderung) bleibt die Platzierung
    # unverändert gegenüber explizit 1,0 — der defensive getattr-Pfad ist ein No-op.
    basis = verdichte_fluchtweg(_gang_raum(), FakeNormProvider(), i_cd=300.0)
    eins = verdichte_fluchtweg(_gang_raum(), _MfNormProvider(1.0), i_cd=300.0)
    assert len(basis) == len(eins)
