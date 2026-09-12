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
