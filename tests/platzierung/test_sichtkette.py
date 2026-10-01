"""sichtkette — R-F: Gang-RZ auf die lückenlose Sichtkette ausdünnen (Fachdoku v2 S.7–9).

Ground truth Elektroplan DE EG: 4 Gang-RZ → 1. Sichtbarkeit ersetzt Zeichen;
an L-Knicken reißt die Kette und die RZ bleiben.
"""
import math

from fakes import FakeNormProvider
from notbeleuchtung.hauptengine.contracts import (
    Ausgang,
    BBox,
    Platzierung,
    Raum,
    RaumModell,
    Tuer,
)
from notbeleuchtung.platzierung.sichtkette import kette_ausduennen


def _rz(xy, quelle="ÖNORM EN 1838:2013") -> Platzierung:
    return Platzierung(
        xy_mm=xy, catalog_key="notlicht_ks_stiege", rotation_deg=0.0, mirror_x=False,
        height_mm=2400.0, kind="rz", richtung="unten", circuit_hint="AGV-A-F13",
        covers_segment=[], norm_quelle=quelle,
    )


def _rect(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def _gerader_gang() -> RaumModell:
    # 24-m-Gang, Ausgang am Ost-Ende; Wohnungstüren am West- und Mittelteil.
    return RaumModell(
        floor="EG", bounds_mm=BBox(min_xy=(0.0, 0.0), max_xy=(24000.0, 3000.0)),
        raeume=[Raum(id="gang", raum_typ="GANG", polygon_mm=_rect(0.0, 0.0, 24000.0, 3000.0),
                     ist_fluchtweg=True, ist_communal=True)],
        tueren=[Tuer(id="t1", xy_mm=(1000.0, 0.0), von_raum="w1", nach_raum="gang"),
                Tuer(id="t2", xy_mm=(12000.0, 0.0), von_raum="w2", nach_raum="gang")],
        ausgaenge=[Ausgang(id="E", xy_mm=(23800.0, 1500.0), typ="final_exit")],
        zirkulation={"nodes": [], "edges": [], "segmente": []},
    )


def test_redundante_gang_rz_werden_ausgeduennt():
    # 3 Gang-RZ auf 24 m + Exit-RZ: hinterleuchtet l=30 m → JEDER Punkt sieht das
    # Exit-RZ, die Kette hält ohne die Zwischen-RZ (R-F: „kein weiteres gesetzt").
    raum = _gerader_gang()
    rz = [_rz((6000.0, 1500.0)), _rz((12000.0, 1500.0)), _rz((18000.0, 1500.0)),
          _rz((23500.0, 1500.0))]                       # letzter = Exit-RZ (geschützt)
    out = kette_ausduennen(rz, raum, FakeNormProvider())
    uebrig = [p for p in out if p.kind == "rz"]
    assert len(uebrig) < 4
    # Exit-RZ bleibt immer (EN 1838 §4.1.2 g):
    assert any(math.hypot(p.xy_mm[0] - 23500.0, p.xy_mm[1] - 1500.0) < 1.0 for p in uebrig)


def test_l_knick_haelt_seine_rz():
    # L-Gang: Sicht bricht an der Ecke — das RZ im Nord-Arm darf NICHT fallen.
    raum = RaumModell(
        floor="EG", bounds_mm=BBox(min_xy=(0.0, 0.0), max_xy=(20000.0, 20000.0)),
        raeume=[Raum(id="ost", raum_typ="GANG", polygon_mm=_rect(0.0, 0.0, 20000.0, 3000.0),
                     ist_fluchtweg=True, ist_communal=True),
                Raum(id="nord", raum_typ="GANG", polygon_mm=_rect(0.0, 3000.0, 3000.0, 20000.0),
                     ist_fluchtweg=True, ist_communal=True)],
        tueren=[Tuer(id="t1", xy_mm=(1500.0, 19000.0), von_raum="w1", nach_raum="nord")],
        ausgaenge=[Ausgang(id="E", xy_mm=(19500.0, 1500.0), typ="final_exit")],
        zirkulation={"nodes": [], "edges": [], "segmente": []},
    )
    rz = [_rz((1500.0, 12000.0)), _rz((19000.0, 1500.0))]
    out = kette_ausduennen(rz, raum, FakeNormProvider())
    uebrig = [p for p in out if p.kind == "rz"]
    # Tür t1 im Nord-Arm sieht das Exit-RZ nicht (Ecke) → Nord-RZ bleibt.
    assert any(p.xy_mm == (1500.0, 12000.0) for p in uebrig)


def test_tuer_rz_und_nicht_gang_rz_bleiben_unberuehrt():
    raum = _gerader_gang()
    tuer_rz = _rz((1000.0, 200.0), quelle="Referenz-Praxis: Technik-/Nebenraum-SL an der Tür")
    stgh_rz = _rz((30000.0, 9000.0))                     # außerhalb der Korridore
    out = kette_ausduennen([tuer_rz, stgh_rz, _rz((23500.0, 1500.0))],
                           raum, FakeNormProvider())
    assert tuer_rz in out and stgh_rz in out


def test_kellergang_tuerbarrieren_verdichten_die_kette():
    """Punkt 2 (Owner 2026-09-12, Kellerabteil-Gang): Türaufschläge sind
    Sichtbarrieren → im türreichen Abteilgang bleiben MEHR Verlaufs-RZ in
    Gangmitte als im türfreien Gang gleicher Länge (kein fester Takt — die
    Dichte kommt aus der Sicht-Logik)."""
    from notbeleuchtung.platzierung.platzierer import NotlichtPlatzierer

    def _gang(mit_tueren: bool) -> RaumModell:
        tueren, abteile = [], []
        if mit_tueren:
            # 8 Abteiltüren beidseitig versetzt, 800er Blätter, alle 2,4 m —
            # Abteile ALS Räume modelliert (KELLERABTEIL, klein): nur so zählen
            # die Türen als Aufschlag-Barrieren (Wohnungstüren täten es nicht).
            for i in range(8):
                x = 2000.0 + i * 2400.0
                y = 0.0 if i % 2 == 0 else 2400.0
                tueren.append(Tuer(id=f"ka{i}", xy_mm=(x, y), breite_mm=800.0,
                                   von_raum=f"abteil{i}", nach_raum="gang"))
                ay = (-2000.0, 0.0) if i % 2 == 0 else (2400.0, 4400.0)
                abteile.append(Raum(id=f"abteil{i}", raum_typ="KELLERABTEIL",
                                    flaeche_m2=3.0,
                                    polygon_mm=_rect(x - 1000.0, ay[0], x + 1000.0, ay[1])))
        return RaumModell(
            floor="UG", bounds_mm=BBox(min_xy=(0.0, -2000.0), max_xy=(22000.0, 4400.0)),
            raeume=[Raum(id="gang", raum_typ="GANG", ist_fluchtweg=True, ist_communal=True,
                         polygon_mm=_rect(0.0, 0.0, 22000.0, 2400.0)), *abteile],
            tueren=tueren,
            ausgaenge=[Ausgang(id="E", xy_mm=(21800.0, 1200.0), typ="final_exit")],
            zirkulation={"nodes": [], "edges": [], "segmente": [
                {"segment_id": "s1", "reason": "exit", "ziel_ausgang": "E",
                 "polyline_mm": [(500.0, 1200.0), (21800.0, 1200.0)]}]},
        )

    norm = FakeNormProvider()
    mit = [p for p in NotlichtPlatzierer().place(_gang(True), norm).platzierungen
           if p.kind == "rz"]
    ohne = [p for p in NotlichtPlatzierer().place(_gang(False), norm).platzierungen
            if p.kind == "rz"]
    assert len(mit) > len(ohne), (len(mit), len(ohne))
    # Verlaufs-RZ liegen in Gangmitte (quer zentriert):
    verlauf = [p for p in mit if 2000.0 < p.xy_mm[0] < 20000.0]
    assert verlauf and all(abs(p.xy_mm[1] - 1200.0) < 600.0 for p in verlauf)


def test_zacken_gang_rz_knapp_ausserhalb_wird_ausgeduennt():
    """D6 (Fischamend/S3-Befund raum_13): ein FLUCHTWEG-RZ, das wegen eines
    Zacken-Polygons knapp AUSSERHALB der Gang-Kontur liegt (Kerbe, 200 mm),
    zaehlt jetzt zum Gang und faellt, wenn die Sichtkette ohne es haelt.
    Ein Nicht-Fluchtweg-RZ an derselben Stelle bleibt fremde Lane."""
    kerbe = [(0.0, 0.0), (24000.0, 0.0), (24000.0, 3000.0), (12200.0, 3000.0),
             (12200.0, 2000.0), (11800.0, 2000.0), (11800.0, 3000.0), (0.0, 3000.0)]
    raum = RaumModell(
        floor="EG", bounds_mm=BBox(min_xy=(0.0, 0.0), max_xy=(24000.0, 3000.0)),
        raeume=[Raum(id="gang", raum_typ="GANG", polygon_mm=kerbe,
                     ist_fluchtweg=True, ist_communal=True)],
        tueren=[Tuer(id="t1", xy_mm=(1000.0, 0.0), von_raum="w1", nach_raum="gang"),
                Tuer(id="t2", xy_mm=(12000.0, 0.0), von_raum="w2", nach_raum="gang")],
        ausgaenge=[Ausgang(id="E", xy_mm=(23800.0, 1500.0), typ="final_exit")],
        zirkulation={"nodes": [], "edges": [], "segmente": []},
    )
    exit_rz = _rz((23500.0, 1500.0), quelle="ÖNORM EN 1838:2013 §4.2.1")
    kerben_rz = _rz((12000.0, 2500.0), quelle="ÖNORM EN 1838:2013 §4.2.1")
    out = kette_ausduennen([kerben_rz, exit_rz], raum, FakeNormProvider())
    assert exit_rz in out
    assert kerben_rz not in out
    # Gegenprobe: gleiche Stelle, aber KEINE Fluchtweg-Quelle -> bleibt.
    fremd_rz = _rz((12000.0, 2500.0), quelle="ÖNORM EN 1838:2013 §4.1.2 h")
    out2 = kette_ausduennen([fremd_rz, exit_rz], raum, FakeNormProvider())
    assert fremd_rz in out2
