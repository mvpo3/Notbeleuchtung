"""lb.parser — Leistungsbeschreibung → LBVorgabe (Fischa GK4: SL-Exklusion)."""
from pathlib import Path

from notbeleuchtung.hauptengine.contracts.lb_vorgabe import LBVorgabe
from notbeleuchtung.normwissen.lb import LbTextProvider, parse_lb

_FIX = Path(__file__).parent.parent / "fixtures" / "lb"
FISCHA = _FIX / "fischa_lb.txt"
MO_ELEKTRO = _FIX / "mo_elektro_ausschnitt.txt"
BETRIEBSDAUER_DISTRAKTOREN = _FIX / "betriebsdauer_distraktoren.txt"


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


def test_mo_elektro_lux_kontext_und_betriebsdauer():
    # Härtung gegen reale Fehlparses (mo-Elektro): Fluchtweg-Lux als „1 Lux" (Wort),
    # nicht der 200-lx-Aufzugsvorplatz; Feuerlöscher/Hydrant „5 Lux" über Umbruch;
    # Betriebsdauer aus „8 Std."/„Nennbetriebsdauer … 8 Stunden".
    lb = parse_lb(str(MO_ELEKTRO))
    assert lb.mindest_lux_fluchtweg == 1.0       # NICHT 200.0 (Aufzugsvorplatz)
    assert lb.betriebsdauer_min == 480
    orte = {s.ort: s.min_lux for s in lb.sonder_lux}
    assert orte.get("feuerloescher") == 5.0 and orte.get("hydrant") == 5.0


def test_betriebsdauer_distraktoren_keine_fehltreffer():
    # Stunden-/„h"-Angaben ohne Notlicht-Kontext (Gewährleistung, Position „123 H",
    # Austrocknung, Notrufsystem-Batterie) dürfen NICHT als Betriebsdauer gelten.
    lb = parse_lb(str(BETRIEBSDAUER_DISTRAKTOREN))
    assert lb.betriebsdauer_min is None


def test_betriebsdauer_dezimal(tmp_path):
    p = tmp_path / "dez.txt"
    p.write_text("Die Akkus sind auf 8,5 Std auszulegen.\n", encoding="utf-8")
    assert parse_lb(str(p)).betriebsdauer_min == 510


def test_lux_wortform_und_plausibilitaetscap(tmp_path):
    # „Lux" (Wort) wird erkannt; ein unplausibler Fluchtweg-Wert (> Cap) verworfen.
    p = tmp_path / "lux.txt"
    p.write_text("Im Fluchtweg ist mindestens 1 Lux sicherzustellen. "
                 "Arbeitsplatzbeleuchtung 500 lx im Fluchtwegbereich.\n", encoding="utf-8")
    assert parse_lb(str(p)).mindest_lux_fluchtweg == 1.0


def test_fluchtweg_lux_nicht_von_antipanik_unterboten(tmp_path):
    # Fluchtweg-Mittellinie 1 lx und Antipanik 0,5 lx im selben Satz: der Fluchtweg-
    # Wert (1.0) gilt, NICHT der kleinere Antipanik-Wert (0.5).
    p = tmp_path / "ap.txt"
    p.write_text("Auf dem Fluchtweg 1 lx, in der Antipanikflaeche 0,5 lx.\n",
                 encoding="utf-8")
    assert parse_lb(str(p)).mindest_lux_fluchtweg == 1.0


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
