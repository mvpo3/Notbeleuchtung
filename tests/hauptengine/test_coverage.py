"""pipeline._coverage — Planungs-Audit macht stummes RZ-only-Ergebnis laut.

Regressions-Netz für den B3-Fund (Slice-5-Integration): untypisierte Räume →
Norm-Default rz → Plan kommt RZ-only heraus. Die Coverage-Warnungen surfacen das.
"""
from fakes import build_fake_bundle
from notbeleuchtung.hauptengine.contracts import (
    BBox,
    BereichsRegel,
    LBVorgabe,
    Platzierung,
    PlatzierungsErgebnis,
    Raum,
    RaumModell,
)
from notbeleuchtung.hauptengine.pipeline import _coverage, run


def _raum(*typen: str) -> RaumModell:
    return RaumModell(
        floor="EG",
        bounds_mm=BBox(min_xy=(0.0, 0.0), max_xy=(1000.0, 1000.0)),
        raeume=[Raum(id=f"r{i}", raum_typ=t) for i, t in enumerate(typen)],
    )


def _erg(*kinds: str) -> PlatzierungsErgebnis:
    return PlatzierungsErgebnis(
        floor="EG",
        platzierungen=[Platzierung(xy_mm=(0.0, 0.0), catalog_key="k", kind=k) for k in kinds],
    )


def test_alle_untypisiert_warnt():
    cov = _coverage(_raum("", "", ""), _erg("rz", "rz"))
    assert cov["n_raeume_untypisiert"] == 3
    assert any("Kein Raum typisiert" in w for w in cov["warnungen"])
    # RZ-only-Warnung zusätzlich (nur rz platziert).
    assert any("Nur Rettungszeichen" in w for w in cov["warnungen"])


def test_teilweise_untypisiert_warnt_weicher():
    cov = _coverage(_raum("STIEGENHAUS", ""), _erg("rz", "sicherheitsleuchte"))
    assert cov["n_raeume_untypisiert"] == 1
    assert any("1/2 Räume ohne Raumtyp" in w for w in cov["warnungen"])
    # SL vorhanden → keine RZ-only-Warnung.
    assert not any("Nur Rettungszeichen" in w for w in cov["warnungen"])


def test_ueber_20_leuchten_hinweis_auto_pruefeinrichtung():
    # OVE E 8101 560.9.001.AT: > 20 Leuchten → EN-62034-Prüfeinrichtung Pflicht (Hinweis).
    cov = _coverage(_raum("GANG"), _erg(*(["sicherheitsleuchte"] * 21)))
    assert any("Prüfeinrichtung" in h and "EN 62034" in h for h in cov["hinweise"])
    # Nicht-blockierend: keine Warnung, gesamtstatus unberührt.
    cov20 = _coverage(_raum("GANG"), _erg(*(["sicherheitsleuchte"] * 20)))
    assert not any("Prüfeinrichtung" in h for h in cov20["hinweise"])   # genau 20 = noch nicht


def test_voll_typisiert_mit_arten_keine_warnung():
    cov = _coverage(_raum("STIEGENHAUS", "SAAL"), _erg("rz", "sicherheitsleuchte", "antipanik"))
    assert cov["n_raeume_untypisiert"] == 0
    assert cov["warnungen"] == []
    assert cov["arten_platziert"] == ["antipanik", "rz", "sicherheitsleuchte"]


def test_run_haengt_coverage_an(tmp_path):
    # 4OG-Fake ist typisiert (STIEGENHAUS) + hat SL → coverage da, keine Warnung.
    out = run(build_fake_bundle(), dxf_path="<fake>", floor="4OG",
              out_path=tmp_path / "x.dxf")
    assert "coverage" in out.render_summary
    assert out.render_summary["coverage"]["warnungen"] == []
    assert out.render_summary["coverage"]["lb_angewendet"] is False


def test_lb_ausschluss_unterdrueckt_rz_only_warnung():
    # LB schließt SL aus → RZ-only ist gewollt: keine „Nur Rettungszeichen"-Warnung,
    # stattdessen ein neutraler Hinweis.
    lb = LBVorgabe(bereiche_exklusion=[
        BereichsRegel(raum_typ="STIEGENHAUS", sicherheitsbeleuchtung=False, begruendung="GK4"),
    ])
    cov = _coverage(_raum("STIEGENHAUS"), _erg("rz"), lb)
    assert not any("Nur Rettungszeichen" in w for w in cov["warnungen"])
    assert any("per LB ausgeschlossen" in h for h in cov["hinweise"])
    assert cov["lb_angewendet"] is True


def test_ohne_lb_rz_only_bleibt_warnung():
    # Ohne LB-Ausschluss bleibt RZ-only eine Warnung (Regressionsschutz).
    cov = _coverage(_raum("STIEGENHAUS"), _erg("rz"))
    assert any("Nur Rettungszeichen" in w for w in cov["warnungen"])
    assert cov["hinweise"] == []
