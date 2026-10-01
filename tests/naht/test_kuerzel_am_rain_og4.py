"""Abschnitt 1 an Am Rain OG4 — „STGH" ohne Flächenzeile in ``rest_2`` ist Stiegenhaus.

LUECKEN.md § 20.4 (R-09/F-07): der Kern mit Text „STGH" (Layer ``Raum-Beschriftung``,
12 320 / 12 909 mm) ist ein R-Stufen-Raum ohne Typ, 40,17 m², 10 Türen; das Geschoss
hatte 0 Ausgänge, 0 Stiegenhäuser, 13 Leuchten, davon 0 im Kern. Owner-Entscheid 1
(2026-10-01): das Kürzel im Polygon ist Beleg. Abnahme = Werte der Speicher-Gegenprobe
§ 20.4: 1 Stiegenhaus, 2 ``stair_exit``, 20 Leuchten.

Am Rain liegt nur als getracktes Zip vor (byteidentisch zur Prüfstrecken-Kopie).
"""
from __future__ import annotations

import zipfile
from pathlib import Path

import pytest
from shapely.geometry import Point, Polygon

AM_RAIN_ZIP = Path(__file__).resolve().parents[2] / "Projekte" / "Am Rain.zip"
AM_RAIN_OG4 = "Am Rain/ARAI5_FE_XEL_ZZ_MOP_OG4_0015_V_01.dxf"
STGH_TEXT = (12320.0, 12909.0)      # Einfügepunkt „STGH" (mm), § 20.4


@pytest.fixture(scope="module")
def og4(tmp_path_factory):
    if not AM_RAIN_ZIP.is_file():
        pytest.fail(f"Versioniertes Zip fehlt: {AM_RAIN_ZIP}")
    dxf = zipfile.ZipFile(AM_RAIN_ZIP).extract(AM_RAIN_OG4, tmp_path_factory.mktemp("amrain"))
    from notbeleuchtung.raumerkennung import ArchitekturRaumProvider

    prov = ArchitekturRaumProvider()
    return prov, prov.parse(dxf, "")


def test_stgh_kern_ist_stiegenhaus(og4):
    _, m = og4
    kern = [r for r in m.raeume if len(r.polygon_mm) >= 3
            and Polygon(r.polygon_mm).buffer(0).covers(Point(STGH_TEXT))]
    assert len(kern) == 1, [r.id for r in kern]
    r = kern[0]
    assert r.id.startswith("rest_"), r.id
    assert (r.raum_typ, r.ist_fluchtweg, r.ist_communal) == ("STIEGENHAUS", True, True)
    assert len(m.stiegenhaeuser) == 1
    assert sorted(a.typ for a in m.ausgaenge) == ["stair_exit", "stair_exit"]
    assert not [w for w in getattr(og4[0], "ausgangs_warnungen", [])
                if "kein Geschossausgang" in str(getattr(w, "grund", w))]


def test_og4_leuchten_gegenprobe(og4):
    from notbeleuchtung.hauptengine.registry import build_default_bundle

    _, m = og4
    b = build_default_bundle()
    platz = b.platzierer.place(m, b.norm, None)
    kern = next(r for r in m.raeume if len(r.polygon_mm) >= 3
                and Polygon(r.polygon_mm).buffer(0).covers(Point(STGH_TEXT)))
    poly = Polygon(kern.polygon_mm).buffer(0)
    im_kern = [p for p in platz.platzierungen if poly.covers(Point(p.xy_mm))]
    assert len(platz.platzierungen) == 20
    assert len(im_kern) >= 1, "der Stiegenhauskern bekommt Notlicht"
