"""validierung — Prüfbericht gegen EN-1838-Hard-Stops."""
from fakes import build_fake_bundle
from notbeleuchtung.hauptengine.contracts import (
    BBox,
    FluchtwegSegment,
    Platzierung,
    PlatzierungsErgebnis,
    RaumModell,
    ZirkulationsGraph,
)
from notbeleuchtung.hauptengine.pipeline import run
from notbeleuchtung.hauptengine.validierung import gesamtstatus, pruefe


def _raum(*segment_ids: str) -> RaumModell:
    return RaumModell(
        floor="EG",
        bounds_mm=BBox(min_xy=(0.0, 0.0), max_xy=(1000.0, 1000.0)),
        zirkulation=ZirkulationsGraph(segmente=[
            FluchtwegSegment(segment_id=s, polyline_mm=[(0.0, 0.0), (100.0, 0.0)], reason="exit")
            for s in segment_ids
        ]),
    )


def _rz(height=2400.0, circuit="AGV-A-F13", covers=("s1",)) -> Platzierung:
    return Platzierung(xy_mm=(0.0, 0.0), catalog_key="k", kind="rz",
                       height_mm=height, circuit_hint=circuit, covers_segment=list(covers))


def _erg(*p: Platzierung) -> PlatzierungsErgebnis:
    return PlatzierungsErgebnis(floor="EG", platzierungen=list(p))


def test_konformer_plan_ist_ok():
    befunde = pruefe(_raum("s1"), _erg(_rz()))
    assert gesamtstatus(befunde) == "ok"
    assert all(b.status == "ok" for b in befunde)


def test_zu_niedrige_montagehoehe_ist_fehler():
    befunde = pruefe(_raum("s1"), _erg(_rz(height=1800.0)))
    hoehe = next(b for b in befunde if "Montagehöhe" in b.regel)
    assert hoehe.status == "fehler"
    assert gesamtstatus(befunde) == "fehler"


def test_fehlender_sicherheitskreis_ist_warnung():
    befunde = pruefe(_raum("s1"), _erg(_rz(circuit="AGV-A-F5")))
    kreis = next(b for b in befunde if "Sicherheitskreis" in b.regel)
    assert kreis.status == "warnung"


def test_ungedecktes_segment_ist_warnung():
    befunde = pruefe(_raum("s1", "s2"), _erg(_rz(covers=("s1",))))  # s2 ungedeckt
    deckung = next(b for b in befunde if "Deckung" in b.regel)
    assert deckung.status == "warnung"
    assert "1/2" in deckung.detail


def test_fluchtweg_ohne_rz_ist_fehler():
    # Segmente da, aber nur eine SL (kein RZ) → Pflicht-RZ fehlt.
    sl = Platzierung(xy_mm=(0.0, 0.0), catalog_key="k", kind="sicherheitsleuchte",
                     height_mm=2400.0, circuit_hint="AGV-A-F13")
    befunde = pruefe(_raum("s1"), _erg(sl))
    assert gesamtstatus(befunde) == "fehler"
    assert any("Rettungszeichen vorhanden" in b.regel for b in befunde)


def test_run_haengt_pruefung_an(tmp_path):
    out = run(build_fake_bundle(), dxf_path="<fake>", floor="4OG",
              out_path=tmp_path / "x.dxf")
    p = out.render_summary["pruefung"]
    assert p["status"] in ("ok", "warnung", "fehler")
    assert isinstance(p["befunde"], list) and p["befunde"]
