"""Photometrie-Katalog — Naht-Invarianten + Parse-Garantie der Schrack-LDTs.

Skip-if-Asset (wie die Real-Plan-E2E): läuft nur, wenn CAD_Symbole/photometrie/
im Baum liegt. Ohne Katalog muss die Registry still auf isotrop zurückfallen.
"""
import pytest

from notbeleuchtung.symbols import catalog_keys
from notbeleuchtung.symbols.photometrie_katalog import (
    _katalog_dir,
    _mapping,
    fluchtweg_default_ldt,
    ldt_pfad_fuer,
)

_KATALOG_DA = _katalog_dir() is not None
braucht_katalog = pytest.mark.skipif(not _KATALOG_DA, reason="CAD_Symbole/photometrie fehlt")


def test_mapping_keys_sind_symbol_keys():
    # Naht-Invariante: das Photometrie-Mapping erfindet keine Katalog-Keys.
    keys = set(catalog_keys())
    fremd = set(_mapping().get("keys", {})) - keys
    assert not fremd, f"Photometrie-Mapping mit unbekannten catalog_keys: {sorted(fremd)}"


@braucht_katalog
def test_alle_katalog_ldts_parsen_und_liefern_licht():
    from notbeleuchtung.normwissen.photometrie import lade_ldt

    for key in _mapping().get("keys", {}):
        pfad = ldt_pfad_fuer(key)
        assert pfad is not None, f"LDT für {key} fehlt im Katalog"
        p = lade_ldt(pfad)
        assert p.lampen_lumen > 0
        # Irgendwo im Halbraum muss real Licht ankommen (kein Platzhalter-Download).
        assert max(p.intensitaet(g) for g in range(0, 91, 5)) > 1.0, key


@braucht_katalog
def test_fluchtweg_default_ist_corridor_optik():
    pfad = fluchtweg_default_ldt()
    assert pfad is not None and pfad.is_file()
    assert "corridor" in pfad.name


def test_registry_faellt_ohne_katalog_auf_isotrop_zurueck(monkeypatch):
    # Deployment ohne CAD_Symbole: kein Crash, i_cd_fn bleibt None (isotrop).
    import notbeleuchtung.symbols.photometrie_katalog as pk

    monkeypatch.setattr(pk, "_katalog_dir", lambda: None)
    assert pk.fluchtweg_default_ldt() is None
    assert pk.ldt_pfad_fuer("sicherheitsleuchte_aufheller") is None
