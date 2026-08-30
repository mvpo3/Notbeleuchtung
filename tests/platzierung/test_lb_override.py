"""lb_override — LBVorgabe (2. Input) übersteuert die norm-getriebene Platzierung.

Kanonischer Fall: LB schließt Sicherheitsbeleuchtung im Stiegenhaus aus (Fischa GK4).
"""
from fakes import FakeNormProvider
from notbeleuchtung.hauptengine.contracts import (
    BBox,
    BereichsRegel,
    LBVorgabe,
    Platzierung,
    Raum,
    RaumModell,
)
from notbeleuchtung.platzierung import lb_override
from notbeleuchtung.platzierung.platzierer import NotlichtPlatzierer

_STGH_POLY = [(0.0, 0.0), (1000.0, 0.0), (1000.0, 1000.0), (0.0, 1000.0)]


def _raum_mit_stiegenhaus() -> RaumModell:
    return RaumModell(
        floor="EG",
        bounds_mm=BBox(min_xy=(0.0, 0.0), max_xy=(1000.0, 1000.0)),
        raeume=[Raum(id="s1", raum_typ="STIEGENHAUS", polygon_mm=_STGH_POLY, ist_fluchtweg=True)],
    )


def _lb_exkl_stiegenhaus() -> LBVorgabe:
    return LBVorgabe(
        bereiche_exklusion=[
            BereichsRegel(raum_typ="STIEGENHAUS", sicherheitsbeleuchtung=False, begruendung="GK4"),
        ]
    )


def _p(kind: str, xy=(500.0, 500.0)) -> Platzierung:
    return Platzierung(xy_mm=xy, catalog_key="k", kind=kind)


def test_none_lb_unveraendert():
    plzg = [_p("sicherheitsleuchte"), _p("rz")]
    assert lb_override.anwenden(plzg, _raum_mit_stiegenhaus(), None) == plzg


def test_exklusion_entfernt_sl_im_stiegenhaus_rz_bleibt():
    plzg = [_p("sicherheitsleuchte"), _p("antipanik"), _p("rz")]
    out = lb_override.anwenden(plzg, _raum_mit_stiegenhaus(), _lb_exkl_stiegenhaus())
    arten = [p.kind for p in out]
    assert "sicherheitsleuchte" not in arten
    assert "antipanik" not in arten
    assert "rz" in arten            # Rettungszeichen bleiben (Fluchtwegkennzeichnung)


def test_exklusion_laesst_leuchten_ausserhalb_unberuehrt():
    # SL außerhalb des Stiegenhaus-Polygons → bleibt.
    plzg = [_p("sicherheitsleuchte", xy=(5000.0, 5000.0))]
    out = lb_override.anwenden(plzg, _raum_mit_stiegenhaus(), _lb_exkl_stiegenhaus())
    assert len(out) == 1


def test_place_respektiert_lb_exklusion():
    # Voller Platzierer: mit LB-Exklusion darf keine Sicherheits-/Antipanik-Leuchte
    # im Stiegenhaus liegen; ohne LB ist das Ergebnis mindestens so groß.
    raum = _raum_mit_stiegenhaus()
    norm = FakeNormProvider()
    ohne = NotlichtPlatzierer().place(raum, norm)
    mit = NotlichtPlatzierer().place(raum, norm, _lb_exkl_stiegenhaus())
    sl_mit = [p for p in mit.platzierungen if p.kind in ("sicherheitsleuchte", "antipanik")]
    assert sl_mit == []
    assert len(mit.platzierungen) <= len(ohne.platzierungen)


# --- Inklusion: SL erzwingen, wo die LB fordert aber die Norm keine vorsieht --------

_LAGER_POLY = [(0.0, 0.0), (2000.0, 0.0), (2000.0, 2000.0), (0.0, 2000.0)]


def _raum_mit_lager() -> RaumModell:
    return RaumModell(
        floor="EG",
        bounds_mm=BBox(min_xy=(0.0, 0.0), max_xy=(2000.0, 2000.0)),
        raeume=[Raum(id="l1", raum_typ="LAGER", polygon_mm=_LAGER_POLY)],
    )


def _lb_inkl_lager() -> LBVorgabe:
    return LBVorgabe(
        bereiche_inklusion=[BereichsRegel(raum_typ="LAGER", sicherheitsbeleuchtung=True)],
        lb_quelle="LB mo-Elektro §5.1.23",
    )


def test_inklusion_erzwingt_sl_mit_lb_quelle():
    # Norm sieht für LAGER keine SL vor (keine Platzierung) → LB erzwingt eine.
    out = lb_override.anwenden([], _raum_mit_lager(), _lb_inkl_lager())
    sl = [p for p in out if p.kind == "sicherheitsleuchte"]
    assert len(sl) == 1
    assert sl[0].norm_quelle == ""                       # keine Norm begründet sie
    assert sl[0].lb_quelle == "LB mo-Elektro §5.1.23"    # LB-Provenienz gesetzt
    # Leuchte liegt im Lager-Polygon.
    from notbeleuchtung.platzierung.geometry import point_in_polygon
    assert point_in_polygon(sl[0].xy_mm, _LAGER_POLY)


def test_inklusion_dupliziert_nicht_wenn_schon_leuchte_da():
    # Ist im Lager bereits eine Aufheller-Leuchte, wird keine zweite erzwungen.
    vorhanden = [Platzierung(xy_mm=(1000.0, 1000.0), catalog_key="k", kind="sicherheitsleuchte")]
    out = lb_override.anwenden(vorhanden, _raum_mit_lager(), _lb_inkl_lager())
    assert len([p for p in out if p.kind == "sicherheitsleuchte"]) == 1


def test_leere_lb_bereiche_unveraendert():
    # LBVorgabe ohne Inklusion/Exklusion lässt die Platzierung unangetastet.
    plzg = [_p("rz")]
    assert lb_override.anwenden(plzg, _raum_mit_lager(), LBVorgabe()) == plzg
