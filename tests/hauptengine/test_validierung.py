"""validierung — Prüfbericht gegen EN-1838-Hard-Stops."""
from fakes import build_fake_bundle
from notbeleuchtung.hauptengine.contracts import (
    Ausgang,
    BBox,
    FluchtwegSegment,
    Platzierung,
    PlatzierungsErgebnis,
    Raum,
    RaumModell,
    ZirkulationsGraph,
)
from notbeleuchtung.hauptengine.pipeline import run
from notbeleuchtung.hauptengine.validierung import gesamtstatus, pruefe


def _raum(*segment_ids: str, ausgaenge=()) -> RaumModell:
    return RaumModell(
        floor="EG",
        bounds_mm=BBox(min_xy=(0.0, 0.0), max_xy=(1000.0, 1000.0)),
        ausgaenge=list(ausgaenge),
        zirkulation=ZirkulationsGraph(segmente=[
            FluchtwegSegment(segment_id=s, polyline_mm=[(0.0, 0.0), (100.0, 0.0)], reason="exit")
            for s in segment_ids
        ]),
    )


def _rz(height=2400.0, circuit="AGV-A-F13", covers=("s1",), xy=(0.0, 0.0), richtung="unten") -> Platzierung:
    return Platzierung(xy_mm=xy, catalog_key="k", kind="rz", richtung=richtung,
                       height_mm=height, circuit_hint=circuit, covers_segment=list(covers))


def _erg(*p: Platzierung) -> PlatzierungsErgebnis:
    return PlatzierungsErgebnis(floor="EG", platzierungen=list(p))


def _raum_mit_raeumen(n: int) -> RaumModell:
    """Grundriss mit n Räumen, aber ohne Fluchtweg-Segmente (Raumerkennung unvollständig)."""
    poly = [(0.0, 0.0), (100.0, 0.0), (100.0, 100.0), (0.0, 100.0)]
    return RaumModell(
        floor="OG", bounds_mm=BBox(min_xy=(0.0, 0.0), max_xy=(1000.0, 1000.0)),
        raeume=[Raum(id=f"r{i}", raum_typ="UNKNOWN", polygon_mm=poly) for i in range(n)],
    )


def test_leerer_plan_bei_vielen_raeumen_ist_fehler():
    # 20 Räume, 0 Symbole, keine Segmente → Fluchtweg-Regeln schweigen, Plausibilität greift.
    befunde = pruefe(_raum_mit_raeumen(20), _erg())
    plaus = next(b for b in befunde if "Plausibilität" in b.regel)
    assert plaus.status == "fehler"
    assert gesamtstatus(befunde) == "fehler"


def test_viele_raeume_ohne_rz_ist_warnung():
    # 20 Räume, nur SL (kein RZ), keine Segmente → warnung statt falschem "ok".
    sl = Platzierung(xy_mm=(0.0, 0.0), catalog_key="k", kind="sicherheitsleuchte",
                     height_mm=2400.0, circuit_hint="AGV-A-F13")
    befunde = pruefe(_raum_mit_raeumen(20), _erg(sl))
    plaus = next(b for b in befunde if "Plausibilität" in b.regel)
    assert plaus.status == "warnung"


def test_wenige_raeume_ohne_symbole_kein_plausibilitaets_fehler():
    # Unter der Schwelle (kleine Technik-Etage): Regel greift nicht.
    befunde = pruefe(_raum_mit_raeumen(3), _erg())
    assert not any("Plausibilität" in b.regel for b in befunde)


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


def test_notausgang_ohne_rz_ist_warnung():
    # Notausgang weit weg vom einzigen RZ (bei 0,0) → keine RZ in Reichweite.
    raum = _raum("s1", ausgaenge=[Ausgang(id="E", xy_mm=(50000.0, 0.0), typ="final_exit")])
    befunde = pruefe(raum, _erg(_rz()))
    b = next(b for b in befunde if "Notausgäng" in b.regel)
    assert b.status == "warnung"


def test_notausgang_mit_nahem_rz_ist_ok():
    raum = _raum("s1", ausgaenge=[Ausgang(id="E", xy_mm=(1000.0, 0.0), typ="final_exit")])
    befunde = pruefe(raum, _erg(_rz(xy=(0.0, 0.0))))  # RZ 1 m entfernt → in Reichweite
    b = next(b for b in befunde if "Notausgäng" in b.regel)
    assert b.status == "ok"


def test_rz_ohne_richtung_ist_warnung():
    befunde = pruefe(_raum("s1"), _erg(_rz(richtung=None)))
    b = next(b for b in befunde if "Richtung" in b.regel)
    assert b.status == "warnung"


def test_kollision_ist_warnung():
    befunde = pruefe(_raum("s1"), _erg(_rz(xy=(0.0, 0.0)), _rz(xy=(100.0, 0.0))))  # 100 mm < 250
    b = next(b for b in befunde if "Kollision" in b.regel)
    assert b.status == "warnung"
    assert "1 Symbol-Paar" in b.detail


def test_run_haengt_pruefung_an(tmp_path):
    out = run(build_fake_bundle(), dxf_path="<fake>", floor="4OG",
              out_path=tmp_path / "x.dxf")
    p = out.render_summary["pruefung"]
    assert p["status"] in ("ok", "warnung", "fehler")
    assert isinstance(p["befunde"], list) and p["befunde"]
