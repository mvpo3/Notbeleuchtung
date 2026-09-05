"""validierung — Prüfbericht gegen EN-1838-Hard-Stops."""
from fakes import build_fake_bundle
from notbeleuchtung.hauptengine.contracts import (
    Ausgang,
    BBox,
    BereichsRegel,
    FluchtwegSegment,
    LBVorgabe,
    Platzierung,
    PlatzierungsErgebnis,
    Raum,
    RaumModell,
    Sonderstelle,
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


def test_quasi_leerer_plan_bei_vielen_raeumen_ist_fehler():
    # DoD Mollgasse 1OG: 254 Räume, 2 isolierte SL, 0 RZ → FEHLER (nicht nur warnung).
    sl = [Platzierung(xy_mm=(float(i), 0.0), catalog_key="k", kind="sicherheitsleuchte",
                      height_mm=2400.0, circuit_hint="AGV-A-F13") for i in range(2)]
    befunde = pruefe(_raum_mit_raeumen(254), _erg(*sl))
    plaus = next(b for b in befunde if "Plausibilität" in b.regel)
    assert plaus.status == "fehler"
    assert gesamtstatus(befunde) == "fehler"


def test_wenige_raeume_ohne_symbole_kein_plausibilitaets_fehler():
    # Unter der Schwelle (kleine Technik-Etage): Regel greift nicht.
    befunde = pruefe(_raum_mit_raeumen(3), _erg())
    assert not any("Plausibilität" in b.regel for b in befunde)


# ---- Regel 8b: Prüfbasis (0 Ausgänge / 0 Segmente erkannt = ungeprüft ≠ ok) ----

def test_symbole_ohne_ausgaenge_und_segmente_ist_pruefbasis_warnung():
    # Realer Fischamender-Fall: viele Räume, Symbole platziert, aber die Erkennung
    # liefert 0 Ausgänge + 0 Segmente → Regel 3/4/4b/5 liefen NIE. Der Bericht darf
    # nicht „ok" sagen — zwei Prüfbasis-Warnungen.
    sl = Platzierung(xy_mm=(0.0, 0.0), catalog_key="k", kind="rz", richtung="unten",
                     height_mm=2400.0, circuit_hint="AGV-A-F13")
    befunde = pruefe(_raum_mit_raeumen(20), _erg(sl))
    basis = [b for b in befunde if "Prüfbasis" in b.regel]
    assert {b.regel for b in basis} == {
        "Prüfbasis Notausgänge (Erkennung)", "Prüfbasis Fluchtwege (Erkennung)"}
    assert all(b.status == "warnung" for b in basis)
    assert gesamtstatus(befunde) != "ok"


def test_pruefbasis_schweigt_ohne_symbole():
    # 0 Symbole → Regel 8 erzählt die Geschichte (fehler); 8b wäre Doppelrauschen.
    befunde = pruefe(_raum_mit_raeumen(20), _erg())
    assert not any("Prüfbasis" in b.regel for b in befunde)


def test_pruefbasis_schweigt_mit_erkannten_ausgaengen_und_segmenten():
    raum = _raum("s1", ausgaenge=[Ausgang(id="E", xy_mm=(0.0, 0.0), typ="final_exit")])
    raum = raum.model_copy(update={"raeume": _raum_mit_raeumen(20).raeume})
    befunde = pruefe(raum, _erg(_rz()))
    assert not any("Prüfbasis" in b.regel for b in befunde)


def test_pruefbasis_schweigt_bei_wenigen_raeumen():
    # Synthetische Mini-Modelle (Unit-Fixtures) sollen keine Warnung kassieren.
    befunde = pruefe(_raum_mit_raeumen(3), _erg(_rz()))
    assert not any("Prüfbasis" in b.regel for b in befunde)


# ---- Regel 8c: widersprüchliche Erkennungsbasis (Türen ≫ Räume) ----

def _raum_mit_tueren(n_tueren: int, n_raeume: int) -> RaumModell:
    from notbeleuchtung.hauptengine.contracts import Tuer
    basis = _raum_mit_raeumen(n_raeume)
    return basis.model_copy(update={"tueren": [
        Tuer(id=f"t{i}", xy_mm=(float(i), 0.0)) for i in range(n_tueren)
    ]})


def test_viele_tueren_fast_keine_raeume_ist_warnung():
    # Realer Barawitzka-Fall: 116 Türen beweisen ein Gebäude, aber nur 2 Räume
    # erschlossen + 0 Symbole → bisher rutschte das als „ok" durch (Regel 8/8b
    # gaten auf n_raeume >= 15).
    befunde = pruefe(_raum_mit_tueren(116, 2), _erg())
    b = next(b for b in befunde if "Räume (Erkennung widersprüchlich)" in b.regel)
    assert b.status == "warnung"
    assert gesamtstatus(befunde) != "ok"


def test_tueren_raeume_konsistent_schweigt():
    # Genug Räume erschlossen → kein Widerspruch, Regel 8c schweigt.
    befunde = pruefe(_raum_mit_tueren(116, 20), _erg(_rz()))
    assert not any("widersprüchlich" in b.regel for b in befunde)


def test_wenige_tueren_wenige_raeume_schweigt():
    # Kleines Fragment/Mini-Fixture (wenige Türen) → kein Gebäude-Beweis, kein Alarm.
    befunde = pruefe(_raum_mit_tueren(5, 2), _erg())
    assert not any("widersprüchlich" in b.regel for b in befunde)


def _raum_raeume_und_segmente(n: int, *segment_ids: str) -> RaumModell:
    """Viele Räume UND erkannte Fluchtweg-Segmente (Regel 3/4 greifen)."""
    poly = [(0.0, 0.0), (100.0, 0.0), (100.0, 100.0), (0.0, 100.0)]
    return RaumModell(
        floor="OG", bounds_mm=BBox(min_xy=(0.0, 0.0), max_xy=(1000.0, 1000.0)),
        raeume=[Raum(id=f"r{i}", raum_typ="UNKNOWN", polygon_mm=poly) for i in range(n)],
        zirkulation=ZirkulationsGraph(segmente=[
            FluchtwegSegment(segment_id=s, polyline_mm=[(0.0, 0.0), (100.0, 0.0)], reason="exit")
            for s in segment_ids
        ]),
    )


def test_plausibilitaet_schweigt_wenn_segmente_erkannt():
    # 20 Räume + Segment + 0 Symbole: Regel 4 (Pflicht-RZ) feuert fehler; Regel 8 darf
    # NICHT zusätzlich feuern (sonst redundante Doppelmeldung).
    befunde = pruefe(_raum_raeume_und_segmente(20, "s1"), _erg())
    assert gesamtstatus(befunde) == "fehler"
    assert any("Rettungszeichen vorhanden" in b.regel for b in befunde)
    assert not any("Plausibilität" in b.regel for b in befunde)


def test_konformer_plan_ist_ok():
    # Zwei RZ am Abschnitt → gedeckt UND redundant (EN 50172) → alles ok.
    befunde = pruefe(_raum("s1"), _erg(_rz(xy=(0.0, 0.0)), _rz(xy=(5000.0, 0.0))))
    assert gesamtstatus(befunde) == "ok"
    assert all(b.status == "ok" for b in befunde)


def test_redundanz_einzelne_leuchte_ist_warnung():
    # Nur 1 Leuchte am Abschnitt → kein Ausfallschutz (EN 50172) → Warnung, kein Fehler.
    befunde = pruefe(_raum("s1"), _erg(_rz(xy=(0.0, 0.0))))
    b = next(b for b in befunde if "Redundanz" in b.regel)
    assert b.status == "warnung"
    assert "1/1" in b.detail
    assert gesamtstatus(befunde) != "fehler"


def test_redundanz_zwei_leuchten_ist_ok():
    # RZ + SL beide in Reichweite des Abschnitts → redundant.
    befunde = pruefe(_raum("s1"), _erg(_rz(xy=(0.0, 0.0)), _sl((5000.0, 0.0))))
    b = next(b for b in befunde if "Redundanz" in b.regel)
    assert b.status == "ok"


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


_POLY = [(0.0, 0.0), (100.0, 0.0), (100.0, 100.0), (0.0, 100.0)]


def _raum_typ(raum_typ: str) -> RaumModell:
    return RaumModell(
        floor="EG", bounds_mm=BBox(min_xy=(0.0, 0.0), max_xy=(1000.0, 1000.0)),
        raeume=[Raum(id="r1", raum_typ=raum_typ, polygon_mm=_POLY)],
    )


def _sl(xy=(50.0, 50.0)) -> Platzierung:
    return Platzierung(xy_mm=xy, catalog_key="k", kind="sicherheitsleuchte",
                       height_mm=2400.0, circuit_hint="AGV-A-F13")


def test_lb_exklusion_verletzt_ist_fehler():
    # LB schließt STIEGENHAUS aus, es liegt aber eine SL im Stiegenhaus → Hard-Override verletzt.
    lb = LBVorgabe(bereiche_exklusion=[BereichsRegel(raum_typ="STIEGENHAUS", sicherheitsbeleuchtung=False)])
    befunde = pruefe(_raum_typ("STIEGENHAUS"), _erg(_sl((50.0, 50.0))), lb)
    b = next(b for b in befunde if "LB-Exklusion" in b.regel)
    assert b.status == "fehler"
    assert gesamtstatus(befunde) == "fehler"


def test_lb_exklusion_respektiert_ist_ok():
    # SL liegt AUSSERHALB des ausgeschlossenen Raums → Exklusion eingehalten.
    lb = LBVorgabe(bereiche_exklusion=[BereichsRegel(raum_typ="STIEGENHAUS", sicherheitsbeleuchtung=False)])
    befunde = pruefe(_raum_typ("STIEGENHAUS"), _erg(_sl((5000.0, 5000.0))), lb)
    b = next(b for b in befunde if "LB-Exklusion" in b.regel)
    assert b.status == "ok"


def test_lb_inklusion_fehlt_ist_fehler():
    # LB verlangt SL in der GARAGE (kanonischer Fall), keine platziert → Fehler.
    lb = LBVorgabe(bereiche_inklusion=[BereichsRegel(raum_typ="GARAGE", sicherheitsbeleuchtung=True)])
    befunde = pruefe(_raum_typ("GARAGE"), _erg(), lb)
    b = next(b for b in befunde if "LB-Inklusion" in b.regel)
    assert b.status == "fehler"
    assert gesamtstatus(befunde) == "fehler"


def test_lb_inklusion_erfuellt_ist_ok():
    lb = LBVorgabe(bereiche_inklusion=[BereichsRegel(raum_typ="GARAGE", sicherheitsbeleuchtung=True)])
    befunde = pruefe(_raum_typ("GARAGE"), _erg(_sl((50.0, 50.0))), lb)
    b = next(b for b in befunde if "LB-Inklusion" in b.regel)
    assert b.status == "ok"


# ---- Regel 10b: tote LB-Bereichsregeln (Vokabular-Naht LB ↔ RaumModell) ----

def _bereichs_befund(befunde):
    return [b for b in befunde if "Bereichsregeln wirksam" in b.regel]


def test_lb_exklusion_ohne_matchenden_raum_ist_warnung():
    # LB schließt KELLER aus, der Plan kennt nur STIEGENHAUS → Regel ist ein
    # stiller No-op (Regel 9 schweigt) und muss als Warnung sichtbar werden.
    lb = LBVorgabe(bereiche_exklusion=[BereichsRegel(raum_typ="KELLER", sicherheitsbeleuchtung=False)])
    befunde = pruefe(_raum_typ("STIEGENHAUS"), _erg(_sl((50.0, 50.0))), lb)
    assert not any("LB-Exklusion" in b.regel for b in befunde)  # Regel 9 schweigt …
    b = _bereichs_befund(befunde)
    assert len(b) == 1 and b[0].status == "warnung"             # … 10b meldet es.
    assert "KELLER" in b[0].detail


def test_lb_inklusion_ohne_matchenden_raum_ist_warnung():
    lb = LBVorgabe(bereiche_inklusion=[BereichsRegel(raum_typ="GARAGE", sicherheitsbeleuchtung=True)])
    befunde = pruefe(_raum_typ("WOHNUNG"), _erg(), lb)
    b = _bereichs_befund(befunde)
    assert len(b) == 1 and b[0].status == "warnung"
    assert "GARAGE" in b[0].detail


def test_lb_bereichsregeln_alle_wirksam_ist_ok():
    lb = LBVorgabe(bereiche_exklusion=[BereichsRegel(raum_typ="STIEGENHAUS", sicherheitsbeleuchtung=False)])
    befunde = pruefe(_raum_typ("STIEGENHAUS"), _erg(), lb)
    b = _bereichs_befund(befunde)
    assert len(b) == 1 and b[0].status == "ok"


def test_lb_bereichsregel_matcht_nur_polygonlose_raeume():
    # Raumtyp existiert, aber kein Raum trägt ein gültiges Polygon → Regel kann
    # geometrisch nicht wirken; das Detail nennt die Ursache.
    raum = RaumModell(
        floor="EG", bounds_mm=BBox(min_xy=(0.0, 0.0), max_xy=(1000.0, 1000.0)),
        raeume=[Raum(id="r1", raum_typ="GARAGE", polygon_mm=[])],
    )
    lb = LBVorgabe(bereiche_inklusion=[BereichsRegel(raum_typ="GARAGE", sicherheitsbeleuchtung=True)])
    befunde = pruefe(raum, _erg(), lb)
    b = _bereichs_befund(befunde)
    assert len(b) == 1 and b[0].status == "warnung"
    assert "ohne gültiges Polygon" in b[0].detail


def test_lb_ohne_bereichsregeln_kein_bereichs_befund():
    # Keine Bereichsregeln in der LB → Regel 10b schweigt (kein Rausch-Befund).
    befunde = pruefe(_raum_typ("STIEGENHAUS"), _erg(), LBVorgabe())
    assert _bereichs_befund(befunde) == []


def test_ohne_lb_keine_lb_befunde():
    befunde = pruefe(_raum("s1"), _erg(_rz()))
    assert not any(b.regel.startswith("LB-") for b in befunde)


def test_run_haengt_pruefung_an(tmp_path):
    out = run(build_fake_bundle(), dxf_path="<fake>", floor="4OG",
              out_path=tmp_path / "x.dxf")
    p = out.render_summary["pruefung"]
    assert p["status"] in ("ok", "warnung", "fehler")
    assert isinstance(p["befunde"], list) and p["befunde"]


# ── Track B: Umschaltzeit-Befund (Norm-Höchstwert vs. LB-Systemvorgabe) ──────────
def _norm_mit_umschaltzeit(sekunden: float):
    from fakes import FakeNormProvider
    fake = FakeNormProvider()
    fake._snapshot.regeln[0].anforderung.umschaltzeit_max_s = sekunden
    return fake


def _umschalt_befund(befunde):
    return [b for b in befunde if "Umschaltzeit" in b.regel]


def test_umschaltzeit_lb_ueber_norm_ist_warnung():
    lb = LBVorgabe(umschaltzeit_max_s=15.0)
    befunde = pruefe(_raum("s1"), _erg(_rz()), lb, norm=_norm_mit_umschaltzeit(5.0))
    b = _umschalt_befund(befunde)
    assert len(b) == 1 and b[0].status == "warnung"


def test_umschaltzeit_lb_unter_norm_ist_ok():
    lb = LBVorgabe(umschaltzeit_max_s=1.0)
    befunde = pruefe(_raum("s1"), _erg(_rz()), lb, norm=_norm_mit_umschaltzeit(5.0))
    b = _umschalt_befund(befunde)
    assert len(b) == 1 and b[0].status == "ok"


def test_umschaltzeit_ohne_norm_wert_uebersprungen():
    from fakes import FakeNormProvider
    lb = LBVorgabe(umschaltzeit_max_s=15.0)
    # Norm ohne umschaltzeit_max_s (Enis-Werte noch offen) → Regel schweigt (kein Fehlalarm).
    befunde = pruefe(_raum("s1"), _erg(_rz()), lb, norm=FakeNormProvider())
    assert _umschalt_befund(befunde) == []


def test_umschaltzeit_ohne_norm_arg_uebersprungen():
    # Bestehende Aufrufer ohne norm-Argument bleiben unberührt (keine Umschaltzeit-Regel).
    lb = LBVorgabe(umschaltzeit_max_s=15.0)
    befunde = pruefe(_raum("s1"), _erg(_rz()), lb)
    assert _umschalt_befund(befunde) == []


def test_regel11_sonderstelle_mit_lux_anforderung_warnt():
    # §4.1.2 h/i (5 lx VERTIKAL): Leuchte gesetzt ≠ Nachweis geführt — der Bericht
    # muss "manuell prüfen" sagen (Enis-Review #95, Befund 2).
    raum = _raum("s1")
    raum.sonderstellen.append(Sonderstelle(
        id="f1", typ="feuerloescher", xy_mm=(10.0, 10.0), quelle="Test"))
    befunde = pruefe(raum, _erg(_rz()))
    treffer = [b for b in befunde if "5-lx-vertikal" in b.regel]
    assert len(treffer) == 1 and treffer[0].status == "warnung"
    assert "feuerloescher" in treffer[0].detail


def test_regel11_niveauaenderung_loest_keine_lux_warnung_aus():
    # §4.1.2 c) nennt KEIN Beleuchtungsniveau → kein vertikaler Nachweis geschuldet.
    raum = _raum("s1")
    raum.sonderstellen.append(Sonderstelle(
        id="n1", typ="niveauaenderung", xy_mm=(10.0, 10.0), quelle="Test"))
    befunde = pruefe(raum, _erg(_rz()))
    assert not [b for b in befunde if "5-lx-vertikal" in b.regel]


def test_regel11b_besondere_gefaehrdung_warnt():
    raum = _raum("s1")
    raum.raeume.append(Raum(
        id="r_gef", raum_typ="WERKSTATT", besondere_gefaehrdung=True,
        polygon_mm=[(0.0, 0.0), (100.0, 0.0), (100.0, 100.0), (0.0, 100.0)],
    ))
    befunde = pruefe(raum, _erg(_rz()))
    treffer = [b for b in befunde if "besonderer Gefährdung" in b.regel]
    assert len(treffer) == 1 and treffer[0].status == "warnung"
    assert "arbeitsplatz_lux" in treffer[0].detail


def test_regel12b_nennt_die_arbeitsflaeche_als_bezugsflaeche():
    """§4.4.1 (Norm-S.12) fordert den Wert AUF DER ARBEITSFLÄCHE — weder der
    Bodenwert aus `lux_raster` noch der vertikale Wert aus §4.1.2 h/i. Die drei
    Bezugsflächen sind nicht ineinander umrechenbar; der Bericht muss sagen,
    welche gemeint ist (Enis-Nachzug 05.09.)."""
    raum = _raum("s1")
    raum.raeume.append(Raum(
        id="r_gef2", raum_typ="WERKSTATT", besondere_gefaehrdung=True,
        polygon_mm=[(0.0, 0.0), (100.0, 0.0), (100.0, 100.0), (0.0, 100.0)],
    ))
    treffer = [
        b for b in pruefe(raum, _erg(_rz())) if "besonderer Gefährdung" in b.regel
    ]
    assert len(treffer) == 1
    befund = treffer[0]
    assert "ARBEITSFLÄCHE" in befund.regel.upper() or "ARBEITSFLÄCHE" in befund.detail.upper()
    assert "15 lx" in befund.detail and "10 %" in befund.detail
    # Der Bodenwert darf nicht als Ersatz durchgehen.
    assert "lux_raster" in befund.detail
