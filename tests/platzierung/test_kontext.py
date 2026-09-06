"""PlatzierungsKontext — ein Objekt statt Parameter-Fädelei (Architektur-Slice).

Hot-Spot-Befund 2026-09-06: platzierer.py war das meistgeänderte Modul, weil
jede neue Naht Parameter durch mehrere Signatur-Ebenen fädelte. Der Kontext
bündelt die querschneidenden Eingaben; explizite Einzel-kwargs der Strategie-
Einstiege gewinnen weiterhin (Test-Komfort, keine Doppel-Wahrheit).
"""
from __future__ import annotations

from fakes import FakeNormProvider
from notbeleuchtung.hauptengine.contracts import BBox, Raum, RaumModell
from notbeleuchtung.platzierung.deckung import verdichte_fluchtweg
from notbeleuchtung.platzierung.flaechen_strategy import plan_antipanik
from notbeleuchtung.platzierung.kontext import LEER, PlatzierungsKontext

GANG = [(0.0, 0.0), (20000.0, 0.0), (20000.0, 2000.0), (0.0, 2000.0)]
SAAL = [(0.0, 0.0), (12000.0, 0.0), (12000.0, 9000.0), (0.0, 9000.0)]


def _raum(poly, typ, flaeche):
    return RaumModell(
        floor="EG", bounds_mm=BBox(min_xy=(0.0, 0.0), max_xy=(20000.0, 9000.0)),
        raeume=[Raum(id="r1", raum_typ=typ, polygon_mm=poly, flaeche_m2=flaeche,
                     ist_fluchtweg=(typ == "GANG"))],
    )


def test_kontext_traegt_i_cd_fn_in_die_verdichtung():
    """kontext.i_cd_fn wirkt wie das explizite kwarg (schwache Leuchte → mehr SL)."""
    schwach = PlatzierungsKontext(i_cd_fn=lambda g, c=None: 5.0)
    via_kontext = verdichte_fluchtweg(_raum(GANG, "GANG", 40.0), FakeNormProvider(),
                                      kontext=schwach)
    via_kwarg = verdichte_fluchtweg(_raum(GANG, "GANG", 40.0), FakeNormProvider(),
                                    i_cd_fn=lambda g, c=None: 5.0)
    assert [p.xy_mm for p in via_kontext] == [p.xy_mm for p in via_kwarg]
    assert len(via_kontext) > len(
        verdichte_fluchtweg(_raum(GANG, "GANG", 40.0), FakeNormProvider())
    )


def test_explizites_kwarg_gewinnt_gegen_kontext():
    kontext = PlatzierungsKontext(i_cd_fn=lambda g, c=None: 5.0)
    explizit = verdichte_fluchtweg(_raum(GANG, "GANG", 40.0), FakeNormProvider(),
                                   i_cd_fn=lambda g, c=None: 2000.0, kontext=kontext)
    nur_kontext = verdichte_fluchtweg(_raum(GANG, "GANG", 40.0), FakeNormProvider(),
                                      kontext=kontext)
    assert len(explizit) < len(nur_kontext)


def test_kontext_traegt_familien_callables_zur_antipanik():
    aufrufe = []

    def spion(gamma, c=None):
        aufrufe.append(gamma)
        return 200.0

    kontext = PlatzierungsKontext(i_cd_fn_je_key={"antipanik_leuchte": spion})
    out = plan_antipanik(_raum(SAAL, "SAAL", 108.0), FakeNormProvider(), kontext=kontext)
    assert any(p.kind == "antipanik" for p in out)
    assert aufrufe, "Familien-Callable kam nicht durch den Kontext an"


def test_leerer_kontext_ist_neutral():
    mit = plan_antipanik(_raum(SAAL, "SAAL", 108.0), FakeNormProvider(), kontext=LEER)
    ohne = plan_antipanik(_raum(SAAL, "SAAL", 108.0), FakeNormProvider())
    assert [p.xy_mm for p in mit] == [p.xy_mm for p in ohne]
