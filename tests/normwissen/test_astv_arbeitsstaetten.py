"""AStV § 9 / OVE-Fachinformation E08 — Arbeitsstätten-Pfad (Enis, 2026-09-08).

Was hier geprüft wird, in vier Gruppen:

1. **Ebenen bleiben getrennt** — Rechtsquelle (A), Norm (C), Fachinformation (D).
2. **Die Tatbestände bleiben getrennt** — Z 1, Z 2, Z 3 und das Wahlrecht nach
   Abs. 4 dürfen nicht ineinander übergehen; Z 2 gilt nur für Fluchtwege.
3. **Nichts wird still entschieden** — kein Punkt ist „erfüllt", keiner „nicht
   erforderlich"; `False` erzeugt keinen Freibrief.
4. **Nichts wird aktiviert** — kein Contract-Wert, kein Protocol-Mitglied, keine
   Platzierung; die Wirkung endet bei Hinweisen.
"""
from __future__ import annotations

import inspect
from pathlib import Path

import pytest

from notbeleuchtung.hauptengine.contracts import Gebaeudeteil, ProjektKontext
from notbeleuchtung.hauptengine.contracts.ports import NormProvider
from notbeleuchtung.normwissen import En1838NormProvider, OibRl2Provider
from notbeleuchtung.normwissen.astv import (
    UNGEPRUEFT,
    ArbeitsstaettenWissen,
)

W = ArbeitsstaettenWissen()
SRC = Path(__file__).parents[2] / "src" / "notbeleuchtung"

#: Wörter, die eine Entwarnung transportieren würden. Kein Hinweis dieses Moduls
#: darf sie führen — die Punkte sind offen, nicht erledigt.
ENTWARNUNG = (
    "nicht erforderlich",
    "keine Sicherheitsbeleuchtung erforderlich",
    "entfällt",
    "erfüllt",
)


# ── 1. Ebenen ────────────────────────────────────────────────────────────────
def test_tatbestaende_sind_rechtsquelle_ebene_a() -> None:
    """§ 9 ist Verordnungsrecht — jeder Tatbestand trägt Ebene A und § 9 als Fundstelle."""
    punkte = W.pruefpunkte(True)
    assert [p.kennung for p in punkte] == [
        "z1_nicht_natuerlich_belichtet",
        "z2_belichtung_reicht_nicht_aus",
        "z3_besondere_gefahr",
    ]
    for p in punkte:
        assert p.ebene == "A", p.kennung
        assert p.fundstelle.startswith("AStV § 9 Abs. 1 Z "), p.fundstelle


def test_e08_ist_niemals_rechtspflicht() -> None:
    """Fachinformation = Auslegungshilfe (Ebene D). Sie ersetzt keine Norm."""
    angaben = W.ausfuehrung_e08()
    assert angaben, "E08-Block fehlt"
    for a in angaben:
        assert a.ist_rechtspflicht is False, a.kennung
        assert "E08:2021-04-01" in a.fundstelle, a.fundstelle
    doc_ebene = W._doc["quellen"]["e08"]
    assert doc_ebene["ebene"] == "D"
    assert "ERSETZT KEINE NORM" in doc_ebene["hinweis"].upper()


def test_quellen_tragen_ihren_ausgabestand() -> None:
    """Ohne Ausgabestand ist eine Fundstelle nicht nachprüfbar."""
    q = W._doc["quellen"]
    assert "BGBl. II Nr. 368/1998" in q["astv"]["ausgabe"]
    assert "06.09.2026" in q["astv"]["ausgabe"]      # Fassung des RIS-Ausdrucks
    assert q["astv"]["ebene"] == "A"
    assert "2021-04-01" in q["e08"]["ausgabe"]
    assert "EN 1838" in q["en1838"]["ausgabe"] and q["en1838"]["ebene"] == "C"


# ── 2. Tatbestände getrennt ──────────────────────────────────────────────────
def test_z2_gilt_nur_fuer_fluchtwege() -> None:
    """⚠️ Der Wortlaut nennt in Z 2 ausschließlich Fluchtwege.

    Z 1 erfasst „Arbeitsräume und Fluchtwege", Z 2 nur „Fluchtwege". Die
    Ausdehnung von Z 2 auf Arbeitsräume wäre unbelegte Auslegung — dieser Test
    nagelt die Unterscheidung fest.
    """
    z1, z2, _ = W.pruefpunkte(True)
    assert z1.gilt_fuer == ["arbeitsraum", "fluchtweg"]
    assert z2.gilt_fuer == ["fluchtweg"]
    assert "arbeitsraum" not in z2.gilt_fuer
    assert "nur FLUCHTWEGE" in z2.abgrenzung or "ausschliesslich fuer FLUCHTWEGE" in z2.abgrenzung


def test_z2_ist_nicht_aus_z1_ableitbar() -> None:
    """Z 1 fragt OB belichtet, Z 2 ob die Belichtung im Ausfallfall genügt."""
    _, z2, _ = W.pruefpunkte(True)
    assert "NICHT aus Z 1 ableitbar" in z2.abgrenzung
    assert any("Beurteilung" in a for a in z2.benoetigte_angabe)


def test_z3_wird_nicht_mit_dem_contract_feld_gleichgesetzt() -> None:
    """AStV Z 3 (Erforderlichkeit für Bereiche) ≠ EN 1838 § 4.4 (Lux am Arbeitsplatz)."""
    _, _, z3 = W.pruefpunkte(True)
    assert "besondere_gefaehrdung" in z3.abgrenzung
    assert "EN 1838" in z3.abgrenzung
    assert "NICHT gleichzusetzen" in z3.abgrenzung


def test_wahlrecht_bleibt_beim_planer_und_deckt_nur_z1_und_z2() -> None:
    """§ 9 Abs. 4 ist ein Wahlrecht — die Engine übt es nicht aus."""
    w = W.wahlrecht()
    assert w.fundstelle == "AStV § 9 Abs. 4"
    assert "NICHT die Engine" in w.entscheider
    assert w.status == UNGEPRUEFT
    # Die drei Grenzen der Ausnahme, jede einzeln nachgewiesen.
    assert any("Z 3" in b for b in w.bedingungen)
    assert "Abs. 1 Z 1 und 2" in w.reichweite
    for fremd in ("E 8101", "R 12-2", "OIB-RL 2"):
        assert fremd in w.reichweite, fremd


# ── 3. Bekannte, unbekannte und widersprüchliche Eingaben ────────────────────
@pytest.mark.parametrize("angabe", [True, None])
def test_offene_punkte_bei_arbeitsstaette_und_bei_unbekannt(angabe: bool | None) -> None:
    """Ob Arbeitsstätte oder unbekannt — ungeprüft sind dieselben drei Tatbestände."""
    punkte = W.pruefpunkte(angabe)
    assert len(punkte) == 3
    assert {p.status for p in punkte} == {UNGEPRUEFT}
    assert all(p.benoetigte_angabe for p in punkte)


def test_false_erzeugt_keinen_freibrief() -> None:
    """„keine Arbeitsstätte" ist keine Aussage über § 1 Abs. 2.

    Die Prüfpunkte entfallen — der Reichweiten-Vorbehalt wird dafür LÄNGER,
    nicht kürzer: außerhalb der Arbeitsstätte gelegene, von Arbeitnehmer/innen
    benutzte Gebäudeteile bleiben erfasst.
    """
    assert W.pruefpunkte(False) == []
    vorbehalt = W.reichweite_vorbehalt(False)
    assert len(vorbehalt) > len(W.reichweite_vorbehalt(True))
    assert any("§ 1 Abs. 2" in v for v in vorbehalt)
    assert any("vier kumulativen Bedingungen" in v for v in vorbehalt)


def test_unbekannt_sagt_dass_der_status_selbst_offen_ist() -> None:
    """`None` = nicht erhoben — das muss im Vorbehalt stehen, nicht geraten werden."""
    vorbehalt = W.reichweite_vorbehalt(None)
    assert any("nicht erhoben" in v for v in vorbehalt)
    assert any("arbeitsstaette_nach_aschg" in v for v in vorbehalt)


def test_abs3_ist_keine_wohnbau_bereichsausnahme() -> None:
    """Korrektur K2 des Quellenaudits, hier festgenagelt."""
    klar = " ".join(W.reichweite_vorbehalt(True))
    assert "kein pauschaler Ausschluss der AStV fuer Wohngebaeude" in klar
    assert "§ 94 ASchG" in klar
    bedingungen = W._doc["reichweite"]["bedingungen_abs3_kumulativ"]
    assert len(bedingungen) == 4


def test_kein_hinweis_traegt_eine_entwarnung() -> None:
    """Kein Satz dieses Moduls darf als „nichts zu tun" lesbar sein."""
    saetze = [
        *W.hinweise_fuer_ausgabe(None),
        *W.hinweise_fuer_ausgabe(True),
        *W.reichweite_vorbehalt(False),
    ]
    assert saetze
    for s in saetze:
        for wort in ENTWARNUNG:
            assert wort not in s.lower(), (wort, s)


def test_hinweise_nennen_ihre_fundstelle() -> None:
    """Jeder ausgegebene Satz bleibt rückverfolgbar."""
    for s in W.hinweise_fuer_ausgabe(True):
        assert "AStV § 9" in s, s


# ── 4. E08 — Auslegung, sauber abgegrenzt ────────────────────────────────────
def test_e08_tabelle1_bleibt_inaktiv_und_ihr_schweigen_bleibt_schweigen() -> None:
    """Die Raumgrößen-Tabelle ist eine Empfehlung — und ihre Leerstelle kein Nein."""
    t1 = next(a for a in W.ausfuehrung_e08() if a.kennung == "e08_tabelle1_arbeitsraeume")
    assert t1.status == "nicht_aktiv"
    assert "Schweigen, kein" in t1.grenze
    zeilen = W._doc["ausfuehrung_e08"][0]["tabelle"]
    assert [z["flaeche_m2"] for z in zeilen] == ["< 30", "30 bis 100", "> 100 bis 1600", "> 1600"]
    assert zeilen[0]["mit_natuerlichem_licht"] == "keine Angabe"


def test_e08_15_lx_ist_belegt_aber_nicht_aktivierbar() -> None:
    """Der Wert fehlt nicht — die Bezugsfläche fehlt.

    EN 1838 § 4.4.1 misst auf der ARBEITSFLÄCHE und bezieht die 10 % auf den
    Wartungswert der AUFGABENbeleuchtung; E08 § 5.3 bezieht sie auf die
    ALLGEMEINbeleuchtung. Gleich ist nur die absolute Untergrenze 15 lx.
    """
    e = next(a for a in W.ausfuehrung_e08() if a.kennung == "e08_besondere_gefaehrdung_lux")
    assert e.status == "belegt_aber_nicht_aktivierbar"
    roh = W._doc["ausfuehrung_e08"][3]
    assert "mindestens 15 lx" in " ".join(e.angaben)
    assert "NICHT dieselbe" in roh["verhaeltnis_zu_en1838"]
    assert "ARBEITSFLAECHE" in roh["warum_kein_contract_wert"]


def test_e08_fluchtwegstellen_bestaetigen_en1838_ohne_neue_grundlage() -> None:
    """E08 Abschnitt 4 deckt sich mit EN 1838 § 4.1.2 — Bestätigung, kein Ersatz."""
    e = next(a for a in W.ausfuehrung_e08()
             if a.kennung == "e08_fluchtweg_zu_beleuchtende_stellen")
    assert e.status == "bestaetigend"
    roh = W._doc["ausfuehrung_e08"][1]
    assert "KEINE zusaetzliche Rechtsgrundlage" in roh["verhaeltnis_zu_en1838"]
    assert len(roh["stellen"]) == 5


def test_anlagenanforderungen_trennen_gedeckt_von_offen() -> None:
    """Umschaltzeit/Dauer/1 lx sind gedeckt; Prüfeinrichtung und Stromkreise nicht."""
    e = next(a for a in W.ausfuehrung_e08() if a.kennung == "e08_anlagenanforderungen")
    assert "deckungsgleich" in e.deckung_mit_engine["umschaltzeit"]
    assert e.deckung_mit_engine["pruefeinrichtung_ab_20_leuchten"].startswith("NICHT abgebildet")
    assert e.deckung_mit_engine["stromkreis_aufteilung"].startswith("NICHT abgebildet")


def test_betriebspflichten_liegen_ausserhalb_der_plangenerierung() -> None:
    """AStV § 13 und E08 Abschnitt 6 sind Betrieb, nicht Planung."""
    pflichten = W.betriebspflichten()
    assert len(pflichten) == 3
    assert {p.funktionsbereich for p in pflichten} == {
        "Betrieb/Instandhaltung — ausserhalb der Plangenerierung"
    }
    assert any(p.fundstelle == "AStV § 13" and p.ebene == "A" for p in pflichten)
    assert any(p.ebene == "D" for p in pflichten)


# ── 5. Wirkung und Grenzen der Wirkung ───────────────────────────────────────
def test_pruefpunkte_erreichen_den_oib_befund() -> None:
    """Messbare Wirkung: `bewerte_oib` trägt die § 9-Prüfpunkte je Gebäudeteil."""
    resolver = OibRl2Provider()
    for angabe in (True, None):
        befund = resolver.bewerte_oib(ProjektKontext(
            jurisdiction="AT",
            gebaeudeteile=[Gebaeudeteil(
                id="t1", nutzungsart="SONSTIGES_GEBAEUDE",
                arbeitsstaette_nach_aschg=angabe,
            )],
        ))
        text = " ".join(befund.ergebnisse[0].hinweise)
        assert "AStV § 9 Abs. 1 kennt DREI getrennte, hier NICHT ausgewertete Tatbestaende" in text
        for marke in ("Z 1", "Z 2", "Z 3", "Abs. 4", "E08:2021-04-01"):
            assert marke in text, (angabe, marke)


def test_keine_astv_hinweise_wenn_ausdruecklich_keine_arbeitsstaette() -> None:
    """`False` = ausdrückliche Angabe → kein AStV-Hinweis im OIB-Befund.

    ⚠️ Das ist eine Aussage über die AUSGABE, nicht über die Rechtslage; der
    Vorbehalt aus § 1 Abs. 2/3 lebt in `reichweite_vorbehalt(False)` weiter.
    """
    befund = OibRl2Provider().bewerte_oib(ProjektKontext(
        jurisdiction="AT",
        gebaeudeteile=[Gebaeudeteil(id="t1", nutzungsart="SONSTIGES_GEBAEUDE",
                                    arbeitsstaette_nach_aschg=False)],
    ))
    assert not any("AStV" in h for h in befund.ergebnisse[0].hinweise)


def test_oib_stufen_bleiben_unveraendert() -> None:
    """Der neue Hinweis ergänzt — er ändert keine Einstufung."""
    resolver = OibRl2Provider()
    stufen = {}
    for angabe in (True, False, None):
        befund = resolver.bewerte_oib(ProjektKontext(
            jurisdiction="AT",
            gebaeudeteile=[Gebaeudeteil(id="t1", nutzungsart="GARAGE",
                                        nutzflaeche_garage_m2=500.0,
                                        arbeitsstaette_nach_aschg=angabe)],
        ))
        stufen[angabe] = befund.ergebnisse[0].stufe
    assert set(stufen.values()) == {"eingeschraenkt"}


def test_astv_wissen_ist_kein_protocol_mitglied() -> None:
    """Normwissen-eigene Auskunft — kein Contract, kein Protocol, kein Schema."""
    protocol_namen = {n for n in dir(NormProvider) if not n.startswith("_")}
    assert "pruefpunkte" not in protocol_namen
    assert "ausfuehrung_e08" not in protocol_namen
    assert not hasattr(En1838NormProvider, "pruefpunkte")


def test_konsument_ruft_die_auskunft_auf() -> None:
    """Seit dem AStV-Integrationsschritt (2026-09-09, Enis-Paket v2) hat die Auskunft
    einen echten Konsumenten: `hauptengine/validierung.py` speist die § 9-Prüfpunkte
    je Gebäudeteil in den Prüfbericht.

    Vorher hielt dieser Test den Zustand „kein Konsument" fest (Wissen auf Vorrat);
    mit Enis abgestimmt umgestellt (MANIFEST v2: „auf den neuen Konsumenten umstellen").
    """
    treffer = [
        p.relative_to(SRC).as_posix()
        for p in SRC.rglob("*.py")
        if p.name != "astv.py" and "ArbeitsstaettenWissen" in p.read_text(encoding="utf-8")
    ]
    assert "hauptengine/validierung.py" in treffer, treffer


def test_lazy_load_kein_dateizugriff_beim_aufbau(tmp_path: Path) -> None:
    """Konstruktor ohne Datei darf nicht scheitern — erst die Abfrage liest."""
    leer = ArbeitsstaettenWissen(data_dir=tmp_path)
    with pytest.raises(FileNotFoundError):
        leer.pruefpunkte(True)


def test_kein_contract_wert_wird_aktiviert() -> None:
    """Weder `arbeitsplatz_lux` noch `flaechen_schwellen` werden hier gefüllt."""
    snap = En1838NormProvider().regelwerk_snapshot()
    assert snap.arbeitsplatz_lux.min_lux is None
    assert snap.arbeitsplatz_lux.min_lux_absolut is None
    assert snap.flaechen_schwellen.antipanik_min_m2 is None
    assert snap.flaechen_schwellen.wc_sanitaer_min_m2 is None
    quelle = inspect.getsource(ArbeitsstaettenWissen)
    assert "NormAnforderung" not in quelle and "min_lux" not in quelle


def test_hinweis_bleibt_im_header_budget() -> None:
    """Der AStV-Hinweisblock wiederholt sich JE Gebäudeteil — er muss klein bleiben.

    `api/main.py` legt `render_summary["oib"]` als JSON in den
    `X-Notbeleuchtung`-Header; uvicorn begrenzt eine Header-Zeile auf ~8 KB, und
    `ensure_ascii=True` bläht jeden Umlaut auf sechs Zeichen. `gate_summary`
    stellt jedem Provider-Hinweis `[gebaeudeteil]` voran und dedupliziert deshalb
    NICHT über Gebäudeteile hinweg. Gemessen (Mollgasse KG, echte Pipeline, alle
    Gebäudeteile als Arbeitsstätte): mit einem 1 262-Byte-Block sprengten bereits
    **vier** Gebäudeteile den Header (12 981 B). Der Langtext gehört deshalb in
    `astv_arbeitsstaetten.yaml` bzw. `ArbeitsstaettenWissen`, nicht in den Hinweis.
    """
    import json

    import yaml

    from notbeleuchtung.normwissen.oib.provider import DATA_DIR

    with open(DATA_DIR / "oib_rl2_tabelle6.yaml", encoding="utf-8") as fh:
        astv = yaml.safe_load(fh)["astv_parallelpfad"]
    block = astv["wenn_arbeitsstaette"] + astv["pruefpunkte_kurz"]
    # ensure_ascii wie in api/main.py — nur so ist die Zahl vergleichbar.
    groesse = len(json.dumps(block, ensure_ascii=True).encode())
    assert groesse < 2500, groesse
    assert len(json.dumps(astv["pruefpunkte_kurz"], ensure_ascii=True).encode()) < 1000
