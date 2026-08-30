"""lb.parser — Leistungsbeschreibung → LBVorgabe (Fischa GK4: SL-Exklusion)."""
from pathlib import Path

from notbeleuchtung.hauptengine.contracts.lb_vorgabe import LBVorgabe
from notbeleuchtung.normwissen.lb import LbTextProvider, parse_lb

FISCHA = Path(__file__).parent.parent / "fixtures" / "lb" / "fischa_lb.txt"


def _fischa() -> LBVorgabe:
    return parse_lb(str(FISCHA))


def test_provider_erfuellt_protocol():
    lb = LbTextProvider().parse_lb(str(FISCHA))
    assert isinstance(lb, LBVorgabe)
    assert lb.lb_quelle == "fischa_lb.txt"


def test_fischa_gk4_exklusion_stiegenhaus_und_gang():
    lb = _fischa()
    exkl = {b.raum_typ: b for b in lb.bereiche_exklusion}
    assert "STIEGENHAUS" in exkl and "GANG" in exkl
    assert exkl["STIEGENHAUS"].sicherheitsbeleuchtung is False
    assert exkl["GANG"].sicherheitsbeleuchtung is False
    assert exkl["STIEGENHAUS"].begruendung == "GK4"


def test_fischa_inklusion_garage():
    lb = _fischa()
    inkl = {b.raum_typ: b for b in lb.bereiche_inklusion}
    assert "GARAGE" in inkl and inkl["GARAGE"].sicherheitsbeleuchtung is True
    # kein Widerspruch inkl/exkl (Contract-Validator würde sonst werfen)
    assert not ({b.raum_typ for b in lb.bereiche_inklusion}
                & {b.raum_typ for b in lb.bereiche_exklusion})


def test_fischa_skalare_felder():
    lb = _fischa()
    assert lb.betriebsdauer_min == 480          # „8 Std" → 480
    assert lb.umschaltzeit_max_s == 0.5         # „< 0,5 s"
    assert lb.mindest_lux_fluchtweg == 1.0      # „1 lx"
    assert lb.system_typ == "gruppenbatterie"
    assert lb.ueberwachung == "einzelleuchte"
    assert lb.pruefung == "web"
    assert lb.piktogramm_norm == "EN ISO 7010"


def test_fischa_sonderlux_und_normbezug():
    lb = _fischa()
    orte = {s.ort: s.min_lux for s in lb.sonder_lux}
    assert orte.get("feuerloescher") == 5.0
    assert "EN 1838" in lb.norm_bezug and "OVE E 8101" in lb.norm_bezug


def test_leere_lb_bleibt_norm_default(tmp_path):
    # Ohne explizite Vorgaben → alles None/leer → Norm greift.
    p = tmp_path / "leer.txt"
    p.write_text("Allgemeine Baubeschreibung ohne Notbeleuchtungs-Angaben.\n")
    lb = parse_lb(str(p))
    assert lb.betriebsdauer_min is None
    assert lb.bereiche_exklusion == [] and lb.bereiche_inklusion == []


def test_registry_bundle_hat_lb_provider():
    from notbeleuchtung.hauptengine.registry import build_default_bundle

    bundle = build_default_bundle()
    assert bundle.lb is not None
    assert hasattr(bundle.lb, "parse_lb")
