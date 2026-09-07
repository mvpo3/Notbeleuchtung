"""Tests nutzungsklasse — Mapping deckt den ganzen Kanon, nicht mehr."""
from notbeleuchtung.raumerkennung import raumtyp
from notbeleuchtung.raumerkennung.nutzungsklasse import (
    _MAP,
    nutzungsklasse_fuer,
    regeltyp_fuer,
)


def _kanon() -> set[str]:
    return (
        {v[0] for v in raumtyp._TYP_MAP.values()}
        | {v[0] for v in raumtyp._EXTRA_DIRECT.values()}
        | {v[0] for v in raumtyp._EXTRA_OVERRIDE.values()}
    )


def test_mapping_deckt_kanon_vollstaendig():
    assert set(_MAP) == _kanon()


def test_beispiele():
    assert nutzungsklasse_fuer("SCHLAFZIMMER") == "WOHNUNG_PRIVAT"
    assert nutzungsklasse_fuer("STIEGENHAUS") == "ALLGEMEIN_ERSCHLIESSUNG"
    assert nutzungsklasse_fuer("AUFZUGSVORPLATZ") == "ALLGEMEIN_ERSCHLIESSUNG"
    assert nutzungsklasse_fuer("WASCHKÜCHE") == "ALLGEMEIN_NEBENRAUM"
    assert nutzungsklasse_fuer("BALKON") == "AUSSEN"
    assert nutzungsklasse_fuer("SCHACHT") == "KEIN_RAUM"
    assert nutzungsklasse_fuer("") is None          # untypisiert
    assert nutzungsklasse_fuer("UNBEKANNT") is None


def test_regeltyp():
    assert regeltyp_fuer("GANG") == "GANG"
    assert regeltyp_fuer("STIEGENHAUS") == "STIEGENHAUS"
    # Quelle fehlt, Enis — heute kein eigener Regel-Schlüssel:
    for t in ("KELLER", "TECHNIK", "GARAGE", "LAGER", "AUFZUGSVORPLATZ"):
        assert regeltyp_fuer(t) is None
