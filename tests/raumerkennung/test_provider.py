"""S6 — provider: parse() liefert ein valides RaumModell (Naht zum Contract)."""
from __future__ import annotations

from pathlib import Path

import pytest

from notbeleuchtung.hauptengine.contracts import RaumModell
from notbeleuchtung.raumerkennung import ArchitekturRaumProvider


def test_synth_parse_vollstaendig(synth_dxf):
    rm = ArchitekturRaumProvider().parse(str(synth_dxf), "EG")
    assert isinstance(rm, RaumModell)
    assert rm.floor == "EG"
    assert rm.coordinate_system == "mm"
    assert len(rm.raeume) == 2
    assert any(r.raum_typ == "STIEGENHAUS" for r in rm.raeume)
    assert len(rm.tueren) == 1
    assert len(rm.zirkulation.segmente) == 1
    # Contract-Roundtrip (Schema-Konformität)
    RaumModell.model_validate(rm.model_dump(by_alias=True))


def test_mollgasse_parse_valid(mollgasse_eg):
    rm = ArchitekturRaumProvider().parse(str(mollgasse_eg), "EG")
    assert isinstance(rm, RaumModell)
    assert len(rm.tueren) >= 10
    assert len(rm.zirkulation.segmente) > 0
    RaumModell.model_validate(rm.model_dump(by_alias=True))


def test_mollgasse_leer_parse_ausgaenge(mollgasse_blank_eg):
    # Echter Input (Meter) → kalibriert; Ausgänge aus Außentüren, nicht Weg-Enden.
    rm = ArchitekturRaumProvider().parse(str(mollgasse_blank_eg), "EG")
    assert isinstance(rm, RaumModell)
    assert len(rm.ausgaenge) >= 1
    # Seit Fachteil 1 (tuer_typisierung/ausgaenge) liefert das EG zusätzlich
    # stair_exits (Stiegenhaustüren) — der Pin »alle final_exit« galt nur,
    # solange stair_exit keinen Producer hatte (GT-MOLL-EG-05).
    final = [a for a in rm.ausgaenge if a.typ == "final_exit"]
    assert len(final) >= 1
    # Obergrenze gegen Müll-Heuristiken (alt: 11 Weg-Endpunkte als Ausgänge).
    # Seit den zusätzlichen Türquellen (Außen-Analyse: Hof-/Gartentüren
    # Cluster A+B, Außenwand-Öffnungen der Durchfahrten) liegt das Ist bei 13
    # begründeten final_exits (jede Tür trägt `quelle`) — Deckel mitgezogen.
    assert len(final) <= 16
    RaumModell.model_validate(rm.model_dump(by_alias=True))


def test_doppelfluegel_verschmilzt_aussentor_tueren():
    """Spec 3d: Reihenfolge — Verschmelzen läuft NACH ``aussentor_tueren``,
    darum werden auch zwei benachbarte 'arc_aussen'-Türbögen zu EINER Tür."""
    from shapely.geometry import box

    from notbeleuchtung.raumerkennung.tueren import (
        TuerOeffnung,
        aussentor_tueren,
        verschmelze_doppelfluegel,
    )

    kontur = box(0.0, 0.0, 5000.0, 5000.0)          # Drehpunkte auf der Außenkante
    oeffnungen = [TuerOeffnung(xy_mm=xy, breite_mm=800.0, winkel_grad=0.0,
                               quelle="arc")
                  for xy in ((1000.0, 0.0), (2600.0, 0.0))]
    aussen = aussentor_tueren(oeffnungen, [], kontur)
    assert [t.quelle for t in aussen] == ["arc_aussen", "arc_aussen"]

    wand_segs = [((0.0, 0.0), (5000.0, 0.0))]       # gemeinsame Wand
    verschmolzen = verschmelze_doppelfluegel(aussen, wand_segs)
    assert len(verschmolzen) == 1
    assert verschmolzen[0].quelle == "doppelfluegel"
    assert verschmolzen[0].breite_mm == 1600.0
    assert verschmolzen[0].xy_mm == (1800.0, 0.0)


# ── Ohne Wand-Layer: Warnung und Weiterlauf statt ValueError (P0 Am Rain) ──
# Owner-Regel 2026-09-30: greift kein Wand-Layer-Muster, bricht parse NICHT
# mit „Keine Wand-Entities gefunden" ab. Es warnt (`wand_warnungen`, wie
# `tuer_warnungen` kein Contract-Feld) und läuft über die Erscheinungsbild-
# Pfade weiter: HATCH beliebiger Layer, schmale Polygone, Doppellinien.
def _hatch_waende_dxf(path):
    import ezdxf

    doc = ezdxf.new()
    doc.header["$INSUNITS"] = 4
    msp = doc.modelspace()

    def wand(x0, y0, x1, y1, layer="Wand Beton tragend"):
        h = msp.add_hatch(color=7, dxfattribs={"layer": layer})
        h.paths.add_polyline_path([(x0, y0), (x1, y0), (x1, y1), (x0, y1)],
                                  is_closed=True)

    wand(0, 0, 20000, 200)
    wand(0, 11800, 20000, 12000)
    wand(0, 200, 200, 11800)
    wand(19800, 200, 20000, 11800)
    wand(12000, 200, 12200, 11800, layer="Fuellung 3")   # beliebiger Layer, schmal
    # Weltkoordinaten-Block-Kopie wie Am Rain OG4 *U25 (~34,6 km daneben).
    wand(34_637_525, 1_186_661, 34_640_525, 1_186_861, layer="0")
    doc.saveas(str(path))
    return path


def test_ohne_wandlayer_hatch_waende_raeume_statt_valueerror(tmp_path):
    p = ArchitekturRaumProvider()
    rm = p.parse(str(_hatch_waende_dxf(tmp_path / "hatch_waende.dxf")), "EG")
    assert len(rm.raeume) >= 1
    assert any("keine_wand_entities" in w for w in p.wand_warnungen), p.wand_warnungen
    # Bounds aus den Wandkörpern, ohne den Fern-Körper.
    assert rm.bounds_mm.min_xy[0] >= 0.0 and rm.bounds_mm.max_xy[0] <= 20000.0
    assert rm.bounds_mm.max_xy[1] <= 12000.0
    RaumModell.model_validate(rm.model_dump(by_alias=True))


# Am Rain liegt nur als getracktes Zip vor (`Projekte/Am Rain.zip`, 6 DXF,
# ARAI5-Dialekt); `tests/plaene.py` führt nur getrackte DXF — darum hier.
AM_RAIN_ZIP = Path(__file__).resolve().parents[2] / "Projekte" / "Am Rain.zip"
AM_RAIN_OG4 = "Am Rain/ARAI5_FE_XEL_ZZ_MOP_OG4_0015_V_01.dxf"


def test_naht_am_rain_og4_parse_ohne_abbruch(tmp_path):
    """Leonis' Befund: „Keine Wand-Entities gefunden" auf Am Rain. Naht:
    OG4 liefert Räume und keine Exception."""
    import zipfile

    if not AM_RAIN_ZIP.is_file():
        pytest.fail(f"Versioniertes Zip fehlt: {AM_RAIN_ZIP}")
    dxf = zipfile.ZipFile(AM_RAIN_ZIP).extract(AM_RAIN_OG4, tmp_path)
    p = ArchitekturRaumProvider()
    rm = p.parse(dxf, "OG4")
    assert len(rm.raeume) >= 1
    assert p.wand_warnungen
    RaumModell.model_validate(rm.model_dump(by_alias=True))


# ── 2a: leerer oder defekter Plan → Warnung und RaumModell, kein Abbruch ──
# Owner-Auftrag 2026-09-30 (LUECKEN.md X-02): keine Geometrie, nur Text, nur
# Wände ohne geschlossenen Raum, Minimal-DXF ohne Tabellen (Entities auf
# Layern, die keine Layer-Tabelle kennt) liefern ein RaumModell (hier ohne
# Räume) und eine Warnung in `wand_warnungen`. Einzige Ausnahme: eine Datei,
# die ezdxf nicht als DXF lesen kann → `DxfNichtLesbar` mit Pfad in der Meldung.
def _leer_dxf(path):
    import ezdxf

    ezdxf.new().saveas(str(path))
    return path


def _nur_text_dxf(path):
    import ezdxf

    doc = ezdxf.new()
    msp = doc.modelspace()
    msp.add_text("Wohnzimmer", dxfattribs={"insert": (1000, 1000), "height": 250})
    msp.add_text("Bad 4,50 m²", dxfattribs={"insert": (6000, 1000), "height": 250})
    doc.saveas(str(path))
    return path


_OFFENE_WAENDE = (((0, 0), (10000, 0)), ((0, 200), (10000, 200)),
                  ((0, 0), (0, 8000)), ((200, 200), (200, 8000)))


def _offene_waende_dxf(path):
    import ezdxf

    doc = ezdxf.new()
    doc.header["$INSUNITS"] = 4
    doc.layers.add("A-WALL")
    msp = doc.modelspace()
    for a, b in _OFFENE_WAENDE:          # zwei Wandschenkel, kein Raum zu
        msp.add_line(a, b, dxfattribs={"layer": "A-WALL"})
    doc.saveas(str(path))
    return path


def _ohne_tabellen_dxf(path):
    """Minimal-DXF nur mit ENTITIES-Sektion: keine Layer-Tabelle, kein
    Block-Record für den Modelspace — LINEs auf nirgends definiertem Layer."""
    zeilen = ["0", "SECTION", "2", "ENTITIES"]
    for (x0, y0), (x1, y1) in _OFFENE_WAENDE:
        zeilen += ["0", "LINE", "8", "A-WALL", "10", str(x0), "20", str(y0),
                   "11", str(x1), "21", str(y1)]
    zeilen += ["0", "ENDSEC", "0", "EOF"]
    path.write_text("\n".join(zeilen) + "\n", encoding="ascii")
    return path


@pytest.mark.parametrize(("bau", "warnungen"), [
    (_leer_dxf, ("keine_geometrie", "keine_raeume")),
    (_nur_text_dxf, ("keine_geometrie", "keine_raeume")),
    (_offene_waende_dxf, ("keine_raeume",)),
    (_ohne_tabellen_dxf, ("keine_raeume",)),
], ids=["ohne_geometrie", "nur_text", "waende_ohne_raum", "ohne_tabellen"])
def test_leerer_oder_defekter_plan_warnt_statt_abbruch(tmp_path, bau, warnungen):
    p = ArchitekturRaumProvider()
    rm = p.parse(str(bau(tmp_path / "plan.dxf")), "EG")
    assert rm.raeume == []
    for w in warnungen:
        assert any(x.startswith(f"{w}:") for x in p.wand_warnungen), p.wand_warnungen
    RaumModell.model_validate(rm.model_dump(by_alias=True))


def test_nicht_lesbare_datei_definierter_fehler(tmp_path):
    from notbeleuchtung.raumerkennung.dxf_load import DxfNichtLesbar

    kein_dxf = tmp_path / "kein.dxf"
    kein_dxf.write_text("kein DXF\n", encoding="utf-8")
    for pfad in (kein_dxf, tmp_path / "fehlt.dxf"):
        with pytest.raises(DxfNichtLesbar, match=r"DXF nicht lesbar: .*\.dxf"):
            ArchitekturRaumProvider().parse(str(pfad), "EG")


def test_plan_pruefen_schreibt_wand_warnung_in_bericht(tmp_path, monkeypatch):
    """O-04 (Teil): `wand_warnungen` stehen im bericht.md-Abschnitt
    „Warnungen" — Prüfstrecke end-to-end auf einem Plan ohne Wand-Layer."""
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
    import plan_pruefen as pp

    monkeypatch.setattr(pp, "ERGEBNIS", tmp_path / "ergebnis")
    dxf = _hatch_waende_dxf(tmp_path / "hatch_waende.dxf")
    pp.plan_pruefen(dxf)
    bericht = (tmp_path / "ergebnis" / "hatch_waende" / "bericht.md").read_text(
        encoding="utf-8")
    abschnitt = bericht.split("## Warnungen", 1)[1].split("\n## ", 1)[0]
    assert "- keine_wand_entities: " in abschnitt, abschnitt
