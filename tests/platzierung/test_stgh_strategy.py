"""stgh_strategy — Punkt 4: din-2-RZ-Modul aus den Treppenlauf-Contract-Feldern
(Am-Rain-Referenz §3.2; Owner-Fachdoku R-G/R-H)."""
import math

from fakes import FakeNormProvider
from notbeleuchtung.hauptengine.contracts import (
    Ausgang,
    BBox,
    Podest,
    Raum,
    RaumModell,
    StiegenhausModell,
    Treppenlauf,
)
from notbeleuchtung.platzierung.stgh_strategy import fluchtvektor, plan_stiegenhaus_rz


def _rect(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def _modell(laeufe, podeste=(), ausgaenge=(), stgh_poly=None) -> RaumModell:
    return RaumModell(
        floor="1OG", bounds_mm=BBox(min_xy=(0.0, 0.0), max_xy=(10000.0, 10000.0)),
        raeume=[Raum(id="stgh", raum_typ="STIEGENHAUS", ist_communal=True,
                     polygon_mm=stgh_poly or _rect(0.0, 0.0, 4000.0, 6000.0))],
        tueren=[], ausgaenge=list(ausgaenge),
        zirkulation={"nodes": [], "edges": [], "segmente": []},
        stiegenhaeuser=[StiegenhausModell(raum_id="stgh", laeufe=list(laeufe),
                                          podeste=list(podeste))],
    )


def test_ab_lauf_setzt_richtungs_rz_am_hauptpodest():
    # Abwärtslauf Antritt (1000,5000) → Austritt (1000,1000): Flucht = −y.
    lauf = Treppenlauf(antritt_mm=(1000.0, 5000.0), austritt_mm=(1000.0, 1000.0),
                       richtung="ab")
    podest = Podest(polygon_mm=_rect(500.0, 500.0, 3500.0, 1500.0), ist_hauptpodest=True)
    out = plan_stiegenhaus_rz(_modell([lauf], [podest]), FakeNormProvider())
    assert len(out) == 1
    p = out[0]
    assert p.kind == "rz" and p.richtung == "unten"       # Flucht −y = „unten"
    assert p.xy_mm == (2000.0, 1000.0)                    # Hauptpodest-Zentrum


def test_auf_lauf_flucht_ist_gegenrichtung():
    lauf = Treppenlauf(antritt_mm=(1000.0, 1000.0), austritt_mm=(3000.0, 1000.0),
                       richtung="auf")                     # Gehen +x = aufwärts
    assert fluchtvektor(StiegenhausModell(raum_id="s", laeufe=[lauf])) == (-1.0, 0.0)
    out = plan_stiegenhaus_rz(_modell([lauf]), FakeNormProvider())
    assert len(out) == 1 and out[0].richtung == "links"    # Flucht −x


def test_ohne_laeufe_oder_unbekannt_no_op():
    assert plan_stiegenhaus_rz(_modell([]), FakeNormProvider()) == []
    lauf = Treppenlauf(antritt_mm=(0.0, 0.0), austritt_mm=(1.0, 0.0), richtung="unbekannt")
    assert plan_stiegenhaus_rz(_modell([lauf]), FakeNormProvider()) == []


def test_eg_mit_final_exit_im_stgh_no_op():
    lauf = Treppenlauf(antritt_mm=(1000.0, 5000.0), austritt_mm=(1000.0, 1000.0),
                       richtung="ab")
    ausg = Ausgang(id="E", xy_mm=(2000.0, 3000.0), typ="final_exit")
    assert plan_stiegenhaus_rz(_modell([lauf], ausgaenge=[ausg]), FakeNormProvider()) == []


def test_r8_nutzt_echte_laufrichtung():
    # R8-Nachpass: mit Läufen folgt die Rotation dem Fluchtvektor, nicht dem Zentrum.
    from notbeleuchtung.hauptengine.contracts import Platzierung
    from notbeleuchtung.platzierung.fachpraxis import stiegenhaus_rz_nachpass

    rm = _modell([Treppenlauf(antritt_mm=(3800.0, 5000.0), austritt_mm=(3800.0, 1000.0),
                              richtung="ab")],
                 ausgaenge=[Ausgang(id="X", xy_mm=(200.0, 3000.0), typ="stair_exit")])
    rz = Platzierung(xy_mm=(300.0, 3000.0), catalog_key="notlicht_ks_stiege",
                     rotation_deg=90.0, mirror_x=False, height_mm=2400.0, kind="rz",
                     richtung="unten", circuit_hint="AGV-A-F13", covers_segment=[],
                     norm_quelle="ÖNORM EN 1838:2013")
    out = stiegenhaus_rz_nachpass([rz], rm)
    # Flucht −y → Piktogramm-Achse folgt dem Fluchtvektor (rotation_zur_tuer(0,−1)=0).
    assert out[0].rotation_deg == 0.0
    d = math.hypot(out[0].xy_mm[0] - 300.0, out[0].xy_mm[1] - 3000.0)
    assert d > 0.0                                        # ins STGH gerückt
