"""Punkt 2d an Rennweg DG1 — das Sofa-Feld gehört zum Wohnzimmer (Owner 2026-09-30).

K1-Diagnose (``LUECKEN.md`` § 6.5): links neben Bad 8,6 / WC 1,7 liegt ein
stempelloses Feld von 16,90 m² (Sofas, TV, Layer ``New_065 Möbel
Einrichtung``), in keinem Raum. Die Grenze zum Wohnzimmer (5,79 m) ist zu 3 %
wandbelegt, eine Tür gibt es dort nicht — eine Öffnung ohne Türblatt, also kein
Trenner: das Feld geht ins Wohnzimmer, 73,95 + 16,90 = 90,85 m². Wohnung,
Klasse und Flags des Wohnzimmers bleiben (Grundsatz (b)).
"""
import pytest
from shapely.geometry import Point, Polygon

from plaene import RENNWEG_DG1, plan

SOFA_TV = (12540958.0, 356217077.0)      # Insert „Flat Panel TV 27" im Feld
WOHNZIMMER = (12550500.0, 356211755.0)   # im Wohnzimmer vor 2d (representative_point)


def _raum_an(m, xy):
    treffer = [r for r in m.raeume if len(r.polygon_mm) >= 3
               and Polygon(r.polygon_mm).buffer(0).contains(Point(xy))]
    assert len(treffer) == 1, [r.id for r in treffer]
    return treffer[0]


def test_dg1_sofa_feld_geht_ins_wohnzimmer():
    from notbeleuchtung.raumerkennung import ArchitekturRaumProvider

    prov = ArchitekturRaumProvider()
    m = prov.parse(str(plan(RENNWEG_DG1)), "")
    wz = _raum_an(m, WOHNZIMMER)
    assert wz.raum_typ == "WOHNZIMMER"
    assert _raum_an(m, SOFA_TV).id == wz.id
    # 90,85 = 73,95 + 16,90 (K1, Deckenplatte − Wandkörper − Räume). Toleranz
    # 0,25 m² = 14 mm Randversatz auf dem ganzen Feldumfang (18,1 m); gemessen
    # 90,89 (gedeckte Kontur statt Deckenplatte, symmetrische Differenz 0,05).
    assert wz.flaeche_m2 == pytest.approx(90.85, abs=0.25)
    assert (wz.wohnung_id, wz.nutzungsklasse) == ("top_1", "WOHNUNG_PRIVAT")
    assert (wz.ist_fluchtweg, wz.ist_communal) == (False, False)
    assert not [r for r in m.raeume if r.id.startswith("frei_")]
    assert [b for b in getattr(prov, "freiflaeche_befund", [])
            if f"→ {wz.id} WOHNZIMMER" in b], getattr(prov, "freiflaeche_befund", None)
