"""lux_nachweis — EN-1838-Fluchtweg-Nachweis aus dem fertigen PlatzierungsErgebnis."""
from fakes import FakeNormProvider
from notbeleuchtung.hauptengine.contracts import (
    BBox,
    Platzierung,
    PlatzierungsErgebnis,
    Raum,
    RaumModell,
)
from notbeleuchtung.platzierung.deckung import verdichte_fluchtweg
from notbeleuchtung.platzierung.lux_nachweis import (
    nachweis_fluchtweg,
    nachweis_summary,
)

GANG_POLY = [(0.0, 0.0), (15000.0, 0.0), (15000.0, 2400.0), (0.0, 2400.0)]


def _gang_raum() -> RaumModell:
    return RaumModell(
        floor="X",
        bounds_mm=BBox(min_xy=(0.0, 0.0), max_xy=(15000.0, 2400.0)),
        raeume=[Raum(id="gang1", raum_typ="GANG", polygon_mm=GANG_POLY, ist_fluchtweg=True)],
    )


def _ergebnis(platzierungen: list[Platzierung]) -> PlatzierungsErgebnis:
    return PlatzierungsErgebnis(floor="X", platzierungen=platzierungen)


def _platziert(raum: RaumModell, **kw) -> PlatzierungsErgebnis:
    """Reale Platzierung erzeugen und als Ergebnis verpacken (End-to-End-Naht)."""
    return _ergebnis(verdichte_fluchtweg(raum, FakeNormProvider(), **kw))


def test_nachweis_je_korridor_mit_starkem_licht_erfuellt():
    raum = _gang_raum()
    erg = _platziert(raum, i_cd=2000.0)
    berichte = nachweis_fluchtweg(raum, FakeNormProvider(), erg, i_cd=2000.0)
    assert len(berichte) == 1
    b = berichte[0]
    assert b.bereich_id == "gang1"
    assert b.leuchten >= 2
    assert b.emin_mittellinie >= b.soll_mittellinie      # ≥ 1 lx
    assert b.emin_mittelflaeche >= b.soll_mittelflaeche   # ≥ 0,5 lx
    assert b.erfuellt is True
    assert b.soll_ud == 0.025                              # EN 1838 1:40


def test_ohne_leuchten_nicht_erfuellt():
    # Korridor ohne platzierte Sicherheitsleuchte → Nachweis kann nicht bestehen.
    raum = _gang_raum()
    berichte = nachweis_fluchtweg(raum, FakeNormProvider(), _ergebnis([]), i_cd=2000.0)
    assert len(berichte) == 1
    assert berichte[0].leuchten == 0
    assert berichte[0].erfuellt is False


def test_nur_sicherheitsleuchten_zaehlen():
    # Rettungszeichen (kind=rettungszeichen) im Gang darf den Fluchtweg-Nachweis NICHT tragen.
    raum = _gang_raum()
    rz = Platzierung(xy_mm=(7500.0, 1200.0), catalog_key="rettungszeichen", kind="rz")
    berichte = nachweis_fluchtweg(raum, FakeNormProvider(), _ergebnis([rz]), i_cd=2000.0)
    assert berichte[0].leuchten == 0
    assert berichte[0].erfuellt is False


def test_wartungsfaktor_wird_ausgewiesen_und_gerechnet():
    # Ohne Norm-Feld ist der MF 1,0 (defensiver getattr-Default) und wird ausgewiesen.
    raum = _gang_raum()
    erg = _platziert(raum, i_cd=2000.0)
    b = nachweis_fluchtweg(raum, FakeNormProvider(), erg, i_cd=2000.0)[0]
    assert b.wartungsfaktor == 1.0


def test_summary_shape_json_faehig():
    raum = _gang_raum()
    erg = _platziert(raum, i_cd=2000.0)
    berichte = nachweis_fluchtweg(raum, FakeNormProvider(), erg, i_cd=2000.0)
    s = nachweis_summary(berichte)
    assert s["bereiche"] == 1
    assert s["alle_erfuellt"] is True
    assert s["rettungswege"][0]["soll"]["mittellinie"] == 1.0
    assert set(s["rettungswege"][0]) >= {"bereich", "emin_mittellinie", "ud", "erfuellt"}


def test_keine_korridore_leerer_bericht():
    # RaumModell ohne GANG/FLUR/KORRIDOR → kein Nachweis-Eintrag.
    raum = RaumModell(
        floor="X",
        bounds_mm=BBox(min_xy=(0.0, 0.0), max_xy=(5000.0, 5000.0)),
        raeume=[Raum(id="wc", raum_typ="WC", polygon_mm=GANG_POLY, ist_fluchtweg=False)],
    )
    assert nachweis_fluchtweg(raum, FakeNormProvider(), _ergebnis([])) == []
    assert nachweis_summary([])["alle_erfuellt"] is True
