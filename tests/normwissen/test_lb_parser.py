"""LbTextProvider — Leistungsbeschreibung (2. Input) → LBVorgabe.

Schwerpunkt: **fail closed**. Der Parser muss lieber sichtbar Review verlangen,
als eine erkannte projektspezifische Anforderung still zu verlieren.

Alle Fixtures unter `lb_fixtures/` sind **synthetisch** — Struktur, Zeilenumbrüche,
Dezimalkomma und Formulierungsformen sind realen LBs nachgebildet, aber kein
Kundendokument ist übernommen. Die echten PDFs bleiben lokal/gitignored und
dienen nur der manuellen Gegenprüfung.

Die Trennung, die dieser Test festhält:
* **Bereichs-LB** (Fischa-Muster) → Exklusion/Inklusion, Systemtyp, Überwachung,
  Prüfung, Normbezug — und **keine** Skalare.
* **Skalar-LB** (mo-Elektro-Muster) → 8 Std → 480 min, < 0,5 s, 1 lx, 5 lx
  Feuerlöscher, RZ-Stellen, EN ISO 7010.
"""
import json
from pathlib import Path

import jsonschema
import pytest
import yaml

from notbeleuchtung.hauptengine.contracts import LBProvider, LBVorgabe
from notbeleuchtung.normwissen import LbTextProvider
from notbeleuchtung.normwissen.lb import LbNichtLesbar, LbReviewRequired
from notbeleuchtung.normwissen.lb.parser import DATA_DIR, DATEI

FIXTURES = Path(__file__).parent / "lb_fixtures"
SCHEMA = Path("src/notbeleuchtung/hauptengine/contracts/schema/lb_vorgabe.schema.json")

PARSER = LbTextProvider()


def _pfad(name: str) -> str:
    return str(FIXTURES / name)


def _bericht(name: str):
    return PARSER.parse_bericht(_pfad(name))


def _kandidat(bericht, feld: str) -> str | None:
    treffer = [b for b in bericht.fuer_feld(feld) if b.kandidat]
    return treffer[0].kandidat if treffer else None


def _provider_ohne_typ(tmp_path, typ: str) -> LbTextProvider:
    """Provider, dessen Stützliste `typ` NICHT kennt.

    So bleibt die Fail-Closed-Mechanik prüfbar, ohne einen Raumtyp zu erfinden, den
    es nicht gibt: seit PR #49/#57 vergibt `raumerkennung/raumtyp.py` alle Typen, die
    das LB-Vokabular kennt — der blockierende Zweig wäre sonst unerreichbar.
    """
    daten = tmp_path / "data"
    daten.mkdir()
    cfg = yaml.safe_load((DATA_DIR / DATEI).read_text(encoding="utf-8"))
    cfg["unterstuetzte_raum_typen"] = [t for t in cfg["unterstuetzte_raum_typen"] if t != typ]
    (daten / DATEI).write_text(yaml.safe_dump(cfg, allow_unicode=True), encoding="utf-8")
    return LbTextProvider(data_dir=daten)


# ── Protocol + Grundverhalten ───────────────────────────────────────────────
def test_parser_erfuellt_lb_protocol():
    assert isinstance(PARSER, LBProvider)


def test_erfolgreicher_parse_ist_schema_valide():
    lb = PARSER.parse_lb(_pfad("skalar_lb.txt"))
    jsonschema.validate(
        instance=lb.model_dump(mode="json"),
        schema=json.loads(SCHEMA.read_text(encoding="utf-8")),
    )
    assert isinstance(lb, LBVorgabe)


def test_deterministisch():
    assert PARSER.parse_lb(_pfad("skalar_lb.txt")) == PARSER.parse_lb(_pfad("skalar_lb.txt"))


# ── Skalare: nur wo sie wirklich stehen ─────────────────────────────────────
def test_acht_stunden_werden_zu_480_minuten():
    assert PARSER.parse_lb(_pfad("skalar_lb.txt")).betriebsdauer_min == 480


def test_dezimalkomma_umschaltzeit():
    assert PARSER.parse_lb(_pfad("skalar_lb.txt")).umschaltzeit_max_s == 0.5


def test_mindest_lux_fluchtweg():
    assert PARSER.parse_lb(_pfad("skalar_lb.txt")).mindest_lux_fluchtweg == 1.0


def test_sonder_lux_feuerloescher():
    lux = PARSER.parse_lb(_pfad("skalar_lb.txt")).sonder_lux
    assert len(lux) == 1
    assert lux[0].ort == "feuerloescher_wandhydrant"
    assert lux[0].min_lux == 5.0


def test_piktogramm_norm():
    assert "7010" in PARSER.parse_lb(_pfad("skalar_lb.txt")).piktogramm_norm


def test_rz_stellen_aus_prosa_und_bullets():
    stellen = set(PARSER.parse_lb(_pfad("skalar_lb.txt")).rz_stellen)
    assert {"fluchttuer", "kreuzung", "richtungsaenderung", "niveauaenderung",
            "notausgang_aussen"} <= stellen


def test_bereichs_lb_erzeugt_NIEMALS_die_skalarwerte():
    """Der Kernfehler, den es zu verhindern gilt: Skalare aus einem anderen
    Dokument in eine LBVorgabe schreiben, die eine Bereichs-LB als Quelle nennt."""
    bericht = _bericht("bereichs_lb.txt")
    for feld in ("betriebsdauer_min", "umschaltzeit_max_s", "mindest_lux_fluchtweg"):
        befunde = bericht.fuer_feld(feld)
        assert befunde, f"{feld} muss im Bericht auftauchen"
        assert all(b.status == "nicht_spezifiziert" for b in befunde)
        assert all(b.kandidat is None for b in befunde)
    assert not [b for b in bericht.fuer_feld("sonder_lux") if b.status == "wert"]
    assert not [b for b in bericht.fuer_feld("piktogramm_norm") if b.status == "wert"]


def test_normverweis_allein_erzeugt_keinen_wert():
    """Die LB nennt EN 1838 — daraus darf weder 1,0 lx noch 60 min entstehen."""
    bericht = _bericht("bereichs_lb.txt")
    normen = [b.kandidat for b in bericht.fuer_feld("norm_bezug")]
    assert "EN 1838" in normen
    assert _kandidat(bericht, "mindest_lux_fluchtweg") is None
    assert _kandidat(bericht, "betriebsdauer_min") is None


# ── Bereiche ────────────────────────────────────────────────────────────────
def test_negation_ueber_zeilenumbruch_erzeugt_exklusion():
    """Im Original steht „ist KEINE\\nLED- Sicherheitsbeleuchtung herzustellen"."""
    bericht = _bericht("bereichs_lb.txt")
    exkl = [b for b in bericht.fuer_feld("bereiche")
            if b.kandidat and b.kandidat.startswith("exklusion")]
    typen = {b.kandidat.split(": ")[1] for b in exkl}
    assert typen == {"STIEGENHAUS", "GANG"}
    assert all(b.status == "wert" for b in exkl)
    assert any("GK4" in (b.begruendung or "") for b in exkl)


def test_exklusion_landet_als_bereichsregel_mit_begruendung():
    lb = PARSER.parse_lb(_pfad("skalar_lb.txt"))
    assert lb.bereiche_exklusion == []          # diese LB schliesst nichts aus
    typen = {r.raum_typ for r in lb.bereiche_inklusion}
    assert {"STIEGENHAUS", "GANG"} <= typen


def test_garage_ist_eine_echte_bereichsregel():
    """Seit PR #49 vergibt `raumerkennung/raumtyp.py` das Label GARAGE — die Regel ist
    im Platzierer kein stiller No-op mehr. Also wird sie zum Wert, nicht zum Review.
    Vorher blockierte genau dieser Fall, und das war damals richtig."""
    lb = PARSER.parse_lb(_pfad("bereichs_lb.txt"))
    garage = [b for b in lb.bereiche_inklusion if b.raum_typ == "GARAGE"]
    assert garage and garage[0].sicherheitsbeleuchtung is True


def test_unbekannter_raumtyp_bleibt_blockierender_review(tmp_path):
    """Die Fail-Closed-Mechanik selbst: kennt die Raumerkennung einen Typ nicht, wäre
    die Regel im Platzierer wirkungslos — sie darf weder still verschwinden noch still
    'angewendet' werden."""
    parser = _provider_ohne_typ(tmp_path, "GARAGE")
    with pytest.raises(LbReviewRequired) as exc:
        parser.parse_lb(_pfad("bereichs_lb.txt"))

    garage = [b for b in exc.value.bericht.blockierende if b.kandidat and "GARAGE" in b.kandidat]
    assert garage, "GARAGE-Anforderung muss als blockierender Befund erhalten bleiben"
    assert "inklusion" in garage[0].kandidat
    assert "raum_typ nicht" in garage[0].begruendung or "No-op" in garage[0].begruendung
    assert garage[0].abschnitt and garage[0].seite


def test_nebenraum_typen_aus_bullet_listen_werden_regeln():
    """Garage/Technik/Lager/Müllraum in einer Aufzählungsliste — seit PR #49/#57 alles
    Typen, die die Raumerkennung vergibt. „Lager- und Müllräumen" muss BEIDE erzeugen."""
    lb = PARSER.parse_lb(_pfad("skalar_lb_mit_garage.txt"))
    typen = {b.raum_typ for b in lb.bereiche_inklusion}
    assert {"GARAGE", "TECHNIK", "LAGER", "MUELLRAUM"} <= typen


def test_kandidatenwerte_bleiben_trotz_blockade_im_bericht(tmp_path):
    """parse_bericht() liefert den vollen Befund — auch für blockierte Dateien."""
    bericht = _provider_ohne_typ(tmp_path, "GARAGE").parse_bericht(
        _pfad("skalar_lb_mit_garage.txt"))
    assert _kandidat(bericht, "betriebsdauer_min") == "480"
    assert bericht.blockierende


# ── Systemtyp: Widerspruch wird nicht geraten ───────────────────────────────
def test_systemtyp_konflikt_ergibt_keinen_wert():
    """Technikteil sagt Gruppenbatterie, die Fabrikatsliste Zentralbatterie."""
    bericht = _bericht("bereichs_lb.txt")
    befunde = bericht.fuer_feld("system_typ")
    assert befunde and befunde[0].status == "review_informativ"
    assert "gruppenbatterie" in befunde[0].kandidat
    assert "zentralbatterie" in befunde[0].kandidat
    assert "geraten" in befunde[0].begruendung


def test_eindeutiger_systemtyp_wird_gesetzt():
    assert PARSER.parse_lb(_pfad("skalar_lb.txt")).system_typ == "gruppenbatterie"


def test_ueberwachung_und_pruefung():
    lb = PARSER.parse_lb(_pfad("skalar_lb.txt"))
    assert lb.ueberwachung == "einzelleuchte"
    assert lb.pruefung == "automatisch"


def test_web_pruefung_schlaegt_automatisch_kein_konflikt():
    """Reale LBs nennen beides nebeneinander — das ist keine Widersprüchlichkeit."""
    bericht = _bericht("bereichs_lb.txt")
    befunde = [b for b in bericht.fuer_feld("pruefung") if b.status == "wert"]
    assert befunde and befunde[0].kandidat == "web"


# ── Homonym-Abwehr ──────────────────────────────────────────────────────────
def test_sanitaerbatterien_erzeugen_keinen_systemtyp():
    """„Brausebatterie", „Thermostatbatterie", „Rauchwarnmelder mit Batterie"."""
    bericht = _bericht("ausstattung_ohne_notlicht.txt")
    assert not [b for b in bericht.fuer_feld("system_typ") if b.status == "wert"]


def test_kabinennotbeleuchtung_erzeugt_keine_gebaeude_vorgabe():
    bericht = _bericht("ausstattung_ohne_notlicht.txt")
    assert bericht.dokument_art != "elektro_lb"
    assert not [b for b in bericht.befunde if b.status == "wert"]


def test_dokument_ohne_notbeleuchtungsabschnitt_ist_fail_closed():
    with pytest.raises(LbReviewRequired) as exc:
        PARSER.parse_lb(_pfad("ausstattung_ohne_notlicht.txt"))
    gruende = [b.feld for b in exc.value.bericht.blockierende]
    assert "notbeleuchtungs_abschnitt" in gruende


# ── Verweise: nicht jeder Querverweis ist eine Lücke ────────────────────────
def test_ausgelagerte_vorgaben_ohne_eigene_angaben_blockieren():
    """GU-Rahmen verweist auf die separate Elektro-LB und trägt selbst nichts."""
    with pytest.raises(LbReviewRequired) as exc:
        PARSER.parse_lb(_pfad("rahmen_verweis.txt"))
    verweise = [b for b in exc.value.bericht.blockierende if b.feld == "verweis"]
    assert verweise and verweise[0].kandidat == "ausgelagert"
    assert "Leistungsbeschreibung Gewerk Elektrotechnik" in verweise[0].anker


def test_allgemeiner_verweis_blockiert_nicht():
    """Brandschutzkonzept/Behörde/Norm sind Koordination, keine fehlende Vorgabe."""
    bericht = _bericht("bereichs_lb.txt")
    verweise = bericht.fuer_feld("verweis")
    assert verweise, "der Verweis muss im Audit sichtbar bleiben"
    assert all(v.status == "review_informativ" for v in verweise)
    assert all(v.kandidat == "allgemein" for v in verweise)
    # ... und er darf nicht der Grund für das Fail-Closed sein:
    assert "verweis" not in {b.feld for b in bericht.blockierende}


def test_bereichs_lb_parst_ohne_blockierenden_befund():
    """Der GU-Bereichsfall geht mit dem erweiterten Vokabular durch: Exklusion
    Stiegenhaus+Gang (GK4), Inklusion Garage — und weiterhin keine Skalare."""
    assert _bericht("bereichs_lb.txt").blockierende == []
    lb = PARSER.parse_lb(_pfad("bereichs_lb.txt"))
    assert {b.raum_typ for b in lb.bereiche_exklusion} == {"STIEGENHAUS", "GANG"}
    assert {b.raum_typ for b in lb.bereiche_inklusion} == {"GARAGE"}


# ── Nicht lesbar ────────────────────────────────────────────────────────────
def test_fehlende_datei():
    with pytest.raises(LbNichtLesbar):
        PARSER.parse_lb(str(FIXTURES / "gibtsnicht.txt"))


def test_nicht_unterstuetztes_format(tmp_path):
    p = tmp_path / "lb.docx"
    p.write_bytes(b"PK\x03\x04irgendwas")
    with pytest.raises(LbNichtLesbar, match="Format nicht unterstützt"):
        PARSER.parse_lb(str(p))


def test_leere_datei_ist_fail_closed(tmp_path):
    p = tmp_path / "leer.txt"
    p.write_text("   \n\n", encoding="utf-8")
    with pytest.raises(LbNichtLesbar, match="Kein extrahierbarer Text"):
        PARSER.parse_lb(str(p))


def test_pdf_ohne_text_ist_fail_closed(tmp_path):
    """Scan ohne Text-Layer: eine leere LBVorgabe wäre hier gefährlich."""
    pypdf = pytest.importorskip("pypdf")
    p = tmp_path / "scan.pdf"
    writer = pypdf.PdfWriter()
    writer.add_blank_page(width=595, height=842)
    with open(p, "wb") as fh:
        writer.write(fh)
    with pytest.raises(LbNichtLesbar, match="Kein extrahierbarer Text"):
        PARSER.parse_lb(str(p))


def test_defektes_pdf_ist_fail_closed(tmp_path):
    p = tmp_path / "kaputt.pdf"
    p.write_bytes(b"%PDF-1.4\nkein gueltiger Inhalt")
    with pytest.raises(LbNichtLesbar):
        PARSER.parse_lb(str(p))


# ── Audit-Trail ─────────────────────────────────────────────────────────────
def test_lb_quelle_nennt_datei_abschnitt_und_seite():
    lb = PARSER.parse_lb(_pfad("skalar_lb.txt"))
    assert "skalar_lb.txt" in lb.lb_quelle
    assert "§5.1.23" in lb.lb_quelle
    assert "S. 37" in lb.lb_quelle


def test_treffer_traegt_die_seite_des_treffers_nicht_des_abschnittsbeginns():
    """Ein Abschnitt kann über Seiten laufen. Die Überschrift steht auf S. 20,
    die Werte auf S. 21 — ein Befund muss S. 21 melden, sonst ist die
    Fundstelle wissentlich falsch."""
    bericht = _bericht("langer_abschnitt.txt")
    dauer = [b for b in bericht.fuer_feld("betriebsdauer_min") if b.status == "wert"]
    umschalt = [b for b in bericht.fuer_feld("umschaltzeit_max_s") if b.status == "wert"]
    assert dauer and dauer[0].seite == 21
    assert umschalt and umschalt[0].seite == 21
    # Abschnittsnummer und -titel bleiben die der Überschrift.
    assert dauer[0].abschnitt == "5.1.23 Fluchtwegorientierungsbeleuchtung"


def test_bereichstreffer_traegt_die_seite_seiner_aussage():
    bericht = _bericht("langer_abschnitt.txt")
    bereiche = [b for b in bericht.fuer_feld("bereiche") if b.status == "wert"]
    assert bereiche
    assert all(b.seite == 21 for b in bereiche)
    assert all(b.abschnitt == "5.1.23 Fluchtwegorientierungsbeleuchtung" for b in bereiche)


def test_einseitige_abschnitte_regressieren_nicht():
    """Wo Überschrift und Treffer auf derselben Seite liegen, bleibt alles gleich."""
    bericht = _bericht("skalar_lb.txt")
    assert all(b.seite == 37 for b in bericht.befunde if b.status == "wert")


def test_jeder_befund_traegt_provenienz():
    bericht = _bericht("skalar_lb.txt")
    for b in (x for x in bericht.befunde if x.status == "wert"):
        assert b.datei and b.abschnitt and b.anker
        assert b.seite == 37
        assert b.begruendung


def test_funktionserhalt_nur_informativ():
    """E30 ist extrahierbar, hat aber kein Contract-Feld — kein erfundenes Feld."""
    bericht = _bericht("skalar_lb.txt")
    befunde = bericht.fuer_feld("funktionserhalt")
    assert befunde and befunde[0].status == "review_informativ"
    assert "E30" in befunde[0].kandidat.replace(" ", "")
    assert not befunde[0].blockierend


def test_bericht_als_text_ist_lesbar():
    text = _bericht("bereichs_lb.txt").als_text()
    assert "LB-Bericht" in text
    assert "GARAGE" in text
    # Ein blockierender Fall muss als solcher lesbar sein.
    assert "BLOCKIEREND" in _bericht("rahmen_verweis.txt").als_text()


def test_dokument_art_erkannt():
    assert _bericht("skalar_lb.txt").dokument_art == "elektro_lb"
    assert _bericht("rahmen_verweis.txt").dokument_art in {"gu_rahmen", "unbekannt"}
