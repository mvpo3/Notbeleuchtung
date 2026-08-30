"""Photometrie-Verdrahtung (F2→F1): i_cd_fn fließt in die Lux-Deckung.

Der Platzierer nimmt ein Lichtstärke-Callable (aus F2s Hersteller-Photometrie) und
reicht es an die Deckungs-Schicht. Weniger Licht → mehr Leuchten nötig.
"""
from pathlib import Path

from fakes import FakeNormProvider
from notbeleuchtung.hauptengine.contracts import BBox, Raum, RaumModell
from notbeleuchtung.platzierung.platzierer import NotlichtPlatzierer


def _gang_raum() -> RaumModell:
    poly = [(0.0, 0.0), (30000.0, 0.0), (30000.0, 3000.0), (0.0, 3000.0)]
    return RaumModell(
        floor="EG",
        bounds_mm=BBox(min_xy=(0.0, 0.0), max_xy=(30000.0, 3000.0)),
        raeume=[Raum(id="g", raum_typ="GANG", polygon_mm=poly, ist_fluchtweg=True)],
    )


def _sl(ergebnis):
    return [p for p in ergebnis.platzierungen if p.kind == "sicherheitsleuchte"]


def test_i_cd_fn_beeinflusst_deckungsdichte():
    norm = FakeNormProvider()
    hoch = NotlichtPlatzierer(i_cd_fn=lambda _g: 500.0).place(_gang_raum(), norm)
    niedrig = NotlichtPlatzierer(i_cd_fn=lambda _g: 5.0).place(_gang_raum(), norm)
    # Geringere Lichtstärke → die Deckung verdichtet stärker → mindestens so viele SL.
    assert len(_sl(niedrig)) >= len(_sl(hoch)) >= 1


def test_ohne_i_cd_fn_laeuft_konstant():
    # Default (kein Callable) = konstant-isotrop, kein Fehler.
    erg = NotlichtPlatzierer().place(_gang_raum(), FakeNormProvider())
    assert _sl(erg)  # Deckung liefert Sicherheitsleuchten


def test_registry_baut_i_cd_fn_aus_ldt():
    from notbeleuchtung.hauptengine.registry import photometrie_i_cd_fn
    ldt = Path("tests/fixtures/photometrie/mini.ldt")
    fn = photometrie_i_cd_fn(ldt)
    wert = fn(0.0)   # Lichtstärke bei γ = 0°
    assert isinstance(wert, float) and wert >= 0.0
