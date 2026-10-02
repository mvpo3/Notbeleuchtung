"""Abschnitt 2 an Am Rain — Stempel vor UNBEKANNT in den ``frei_*``-Räumen aus 2d.

LUECKEN.md § 22: von den 12 neuen UNBEKANNT-Räumen (alle Am Rain) tragen 6 einen
Raumstempel im Polygon (VR 12,78 · AR 3,37 · BALKON 3,88 · LOGGIA 7,67 · BAD 5,35 +
GANG 7,68 · VR 5,13), zwei weitere das Kürzel „VR" ohne Flächenzeile. Owner-Entscheid 2
(2026-10-01): Stempel werden gelesen, bevor ein Raum UNBEKANNT wird — Typ nach
Abschnitt 1 (``kuerzel_beleg``), Klasse statisch nach Typ, ``wohnung_id`` weiter nur
aus rohen Türen (bleibt leer). Doppelstempel ohne dominanten Stempel (OG1 ``frei_5``:
drei Räume in einem Polygon) → bleibt UNBESTIMMT mit Grund, Notlicht bleibt.

Hier OG3 (ein Raum, VR 5,13) und OG1 (fünf Räume, alle Fälle); EG (VR 12,78, AR
3,37, 313 s Parse) wird über den Blast-Runner geprüft (LUECKEN.md § 24).
Am Rain liegt nur als getracktes Zip vor (byteidentisch zur Prüfstrecken-Kopie).
"""
from __future__ import annotations

import zipfile
from pathlib import Path

import pytest

AM_RAIN_ZIP = Path(__file__).resolve().parents[2] / "Projekte" / "Am Rain.zip"
PLAENE = {"OG1": "Am Rain/ARAI5_FE_XEL_ZZ_MOP_OG1_0012_V_01.dxf",
          "OG3": "Am Rain/ARAI5_FE_XEL_ZZ_MOP_OG3_0014_V_01.dxf"}


def _parse(geschoss: str, tmp_path_factory):
    if not AM_RAIN_ZIP.is_file():
        pytest.fail(f"Versioniertes Zip fehlt: {AM_RAIN_ZIP}")
    dxf = zipfile.ZipFile(AM_RAIN_ZIP).extract(PLAENE[geschoss],
                                               tmp_path_factory.mktemp("amrain"))
    from notbeleuchtung.raumerkennung import ArchitekturRaumProvider

    prov = ArchitekturRaumProvider()
    return prov, prov.parse(dxf, "")


@pytest.fixture(scope="module")
def og3(tmp_path_factory):
    return _parse("OG3", tmp_path_factory)


@pytest.fixture(scope="module")
def og1(tmp_path_factory):
    return _parse("OG1", tmp_path_factory)


def _frei(m) -> dict[float, object]:
    """``frei_*`` nach Fläche (0,1 m²) — IDs hängen an der Reihenfolge der Flächen."""
    return {round(r.flaeche_m2, 1): r for r in m.raeume if r.id.startswith("frei_")}


def test_og3_vr_5_13_wird_vorraum(og3):
    prov, m = og3
    frei = _frei(m)
    assert list(frei) == [2.7], sorted(frei)
    r = frei[2.7]
    assert (r.raum_typ, r.nutzungsklasse, r.wohnung_id) == ("VORRAUM", "WOHNUNG_PRIVAT", None)
    assert [b for b in prov.freiflaeche_befund if f"neuer Raum {r.id} VORRAUM" in b], \
        prov.freiflaeche_befund


def test_og1_stempel_vor_unbekannt(og1):
    prov, m = og1
    frei = _frei(m)
    assert sorted(frei) == [2.4, 4.0, 6.7, 11.2, 18.2], sorted(frei)
    # BALKON 3,88 (Polygon nimmt die Nachbar-Loggien mit) und LOGGIA 7,67 → BALKON (AUSSEN).
    assert (frei[11.2].raum_typ, frei[11.2].nutzungsklasse) == ("BALKON", "AUSSEN")
    assert (frei[2.4].raum_typ, frei[2.4].nutzungsklasse) == ("BALKON", "AUSSEN")
    # „VR" ohne Flächenzeile im Polygon (Flächenzeile liegt im Schacht) → Kürzel ist Beleg.
    assert (frei[4.0].raum_typ, frei[4.0].nutzungsklasse) == ("VORRAUM", "WOHNUNG_PRIVAT")
    # Doppelstempel BAD 5,35 + GANG 7,68 (+ KOCHNISCHE 5,34) in 18,19 m²: kein Stempel
    # deckt die Hälfte → nicht eindeutig, bleibt UNBESTIMMT mit Grund (Notlicht bleibt).
    drei = frei[18.2]
    assert (drei.raum_typ, drei.nutzungsklasse) == ("", None)
    assert [w for w in prov.freiflaeche_befund
            if w.startswith(f"kuerzel: {drei.id} bleibt UNBESTIMMT") and "nicht eindeutig" in w], \
        prov.freiflaeche_befund
    # Wohnungsinterne Stiege ohne Text bleibt UNBEKANNT.
    assert (frei[6.7].raum_typ, frei[6.7].nutzungsklasse) == ("", None)
    # Grundsatz (b): kein neuer Raum bekommt eine Wohnung.
    assert all(r.wohnung_id is None for r in frei.values())
