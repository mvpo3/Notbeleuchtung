"""OibRl2Provider — OIB-RL 2, Punkt 5.4 + Tabelle 6.

Schwerpunkt: Grenzwerte direkt UNTER / AUF / ÜBER jeder Schwelle, die Review-
Pfade (fehlender Fakt, kein Umkehrschluss, blockierende Unsicherheit) und die
Vollständigkeit des Audit-Trails.

Fachliche Grundlage: docs/OIB_RL2_TABELLE6.md. Kein Wert steht in diesem Test,
der nicht auch in data/oib_rl2_tabelle6.yaml belegt ist.
"""
import json
from pathlib import Path

import jsonschema
import pytest

from notbeleuchtung.hauptengine.contracts import (
    Gebaeudeteil,
    OibProvider,
    ProjektKontext,
    RaumReferenz,
)
from notbeleuchtung.hauptengine.contracts.projekt_kontext import Nutzungsart
from notbeleuchtung.normwissen import OibRl2Provider

SCHEMA = Path("src/notbeleuchtung/hauptengine/contracts/schema/oib_ergebnis.schema.json")

PROV = OibRl2Provider()


def _stufe(**felder) -> str:
    """Ein Gebäudeteil bewerten → Stufe (jurisdiction bewusst gesetzt)."""
    return _erg(**felder).stufe


def _erg(**felder):
    teil = Gebaeudeteil(id="gt", **felder)
    projekt = ProjektKontext(jurisdiction="AT", gebaeudeteile=[teil])
    return PROV.bewerte_oib(projekt).ergebnisse[0]


# ── Protocol + Grundverhalten ───────────────────────────────────────────────
def test_provider_erfuellt_oib_protocol():
    assert isinstance(PROV, OibProvider)


def test_leerer_projektkontext_liefert_leeren_befund():
    befund = PROV.bewerte_oib(ProjektKontext(jurisdiction="AT"))
    assert befund.ergebnisse == []
    jsonschema.validate(
        instance=befund.model_dump(mode="json"),
        schema=json.loads(SCHEMA.read_text(encoding="utf-8")),
    )


def test_befund_ist_schema_valide():
    befund = PROV.bewerte_oib(
        ProjektKontext(
            jurisdiction="AT",
            gebaeudeteile=[
                Gebaeudeteil(id="a", nutzungsart="KRANKENHAUS"),
                Gebaeudeteil(id="b", nutzungsart="PFLEGEHEIM", betten_anzahl=17),
            ],
        )
    )
    jsonschema.validate(
        instance=befund.model_dump(mode="json"),
        schema=json.loads(SCHEMA.read_text(encoding="utf-8")),
    )


def test_deterministisch():
    teil = Gebaeudeteil(id="gt", nutzungsart="PFLEGEHEIM", betten_anzahl=17)
    projekt = ProjektKontext(jurisdiction="AT", gebaeudeteile=[teil])
    assert PROV.bewerte_oib(projekt) == PROV.bewerte_oib(projekt)


def test_gemischte_nutzung_ein_ergebnis_je_gebaeudeteil():
    # Punkt 5.4: "Bei Gebäuden bzw. Bauwerken mit jeweils gemischter Nutzung
    # gelten die für die jeweilige Nutzung anzuwendenden Anforderungen."
    befund = PROV.bewerte_oib(
        ProjektKontext(
            jurisdiction="AT",
            gebaeudeteile=[
                Gebaeudeteil(
                    id="wohnen",
                    nutzungsart="WOHNGEBAEUDE",
                    gebaeudeklasse="GK5",
                    fluchtniveau_m=18.0,
                    lage_zur_wohnung="AUSSERHALB_WOHNUNG",
                ),
                Gebaeudeteil(
                    id="garage", nutzungsart="GARAGE", nutzflaeche_garage_m2=980.0
                ),
            ],
        )
    )
    assert [e.gebaeudeteil_id for e in befund.ergebnisse] == ["wohnen", "garage"]
    assert [e.stufe for e in befund.ergebnisse] == ["eingeschraenkt", "eingeschraenkt"]
    assert [e.zeile for e in befund.ergebnisse] == ["1.1", "11.1"]


# ── Feste Zeilen ────────────────────────────────────────────────────────────
def test_zeile_8_krankenhaus_immer_uneingeschraenkt():
    erg = _erg(nutzungsart="KRANKENHAUS")
    assert (erg.stufe, erg.zeile) == ("uneingeschraenkt", "8")


def test_zeile_12_2_sonstiges_gebaeude_ueber_22m():
    erg = _erg(nutzungsart="SONSTIGES_GEBAEUDE", fluchtniveau_m=40.0)
    assert (erg.stufe, erg.zeile) == ("uneingeschraenkt", "12.2")


@pytest.mark.parametrize("gk", ["GK4", "GK5"])
def test_zeile_1_2_sonstige_gebaeude_gk4_gk5(gk):
    erg = _erg(nutzungsart="SONSTIGES_GEBAEUDE", fluchtniveau_m=10.0, gebaeudeklasse=gk)
    assert (erg.stufe, erg.zeile) == ("eingeschraenkt", "1.2")


@pytest.mark.parametrize("gk", ["GK1", "GK2", "GK3"])
def test_zeile_1_2_gk1_bis_gk3_ist_review_kein_umkehrschluss(gk):
    erg = _erg(nutzungsart="SONSTIGES_GEBAEUDE", fluchtniveau_m=10.0, gebaeudeklasse=gk)
    assert erg.stufe == "review_required"
    assert any("kein Umkehrschluss" in h for h in erg.hinweise)


def test_zeile_1_1_wohngebaeude_gk4_ist_review():
    # Zeile 1.1 nennt nur die GK 5; Zeile 1.2 gilt nur für "sonstige Gebäude".
    erg = _erg(
        nutzungsart="WOHNGEBAEUDE",
        fluchtniveau_m=10.0,
        gebaeudeklasse="GK4",
        lage_zur_wohnung="AUSSERHALB_WOHNUNG",
    )
    assert erg.stufe == "review_required"


# ── Bänder: direkt unter / auf / über der Schwelle ──────────────────────────
@pytest.mark.parametrize(
    "betten,erwartet",
    [(9, "review_required"), (10, "review_required"), (11, "eingeschraenkt"),
     (99, "eingeschraenkt"), (100, "eingeschraenkt"), (101, "uneingeschraenkt")],
)
def test_zeile_3_beherbergung_betten(betten, erwartet):
    assert _stufe(nutzungsart="BEHERBERGUNG_STUDENTENHEIM", betten_anzahl=betten) == erwartet


@pytest.mark.parametrize(
    "betten,erwartet",
    [(10, "review_required"), (11, "eingeschraenkt"),
     (100, "eingeschraenkt"), (101, "uneingeschraenkt")],
)
def test_zeile_6_seniorenheim_betten(betten, erwartet):
    assert _stufe(nutzungsart="ALTEN_SENIORENHEIM", betten_anzahl=betten) == erwartet


@pytest.mark.parametrize(
    "betten,erwartet",
    [(0, "eingeschraenkt"), (15, "eingeschraenkt"), (16, "eingeschraenkt"),
     (17, "uneingeschraenkt")],
)
def test_zeile_7_pflegeheim_betten_keine_luecke_nach_unten(betten, erwartet):
    assert _stufe(nutzungsart="PFLEGEHEIM", betten_anzahl=betten) == erwartet


@pytest.mark.parametrize(
    "flaeche,erwartet",
    [(199.0, "review_required"), (200.0, "review_required"), (200.1, "eingeschraenkt"),
     (3000.0, "eingeschraenkt"), (3000.1, "uneingeschraenkt")],
)
def test_zeile_4_verkaufsflaeche(flaeche, erwartet):
    assert _stufe(
        nutzungsart="VERKAUFSSTAETTE_AUSSTELLUNGSSTAETTE", verkaufsflaeche_m2=flaeche
    ) == erwartet


@pytest.mark.parametrize(
    "plaetze,erwartet",
    [(60, "review_required"), (61, "eingeschraenkt"),
     (240, "eingeschraenkt"), (241, "uneingeschraenkt")],
)
def test_zeile_5_1_verabreichungsplaetze(plaetze, erwartet):
    assert _stufe(
        nutzungsart="SCHANK_SPEISEWIRTSCHAFT", verabreichungsplaetze_anzahl=plaetze
    ) == erwartet


@pytest.mark.parametrize(
    "personen,erwartet",
    [(0, "eingeschraenkt"), (120, "eingeschraenkt"), (121, "uneingeschraenkt")],
)
def test_zeile_5_2_diskothek_personen(personen, erwartet):
    assert _stufe(
        nutzungsart="DISKOTHEK_TANZCAFE", personen_anzahl_bestimmt=personen
    ) == erwartet


@pytest.mark.parametrize(
    "personen,erwartet",
    [(120, "review_required"), (121, "eingeschraenkt"),
     (5000, "eingeschraenkt"), (5001, "uneingeschraenkt")],
)
def test_zeile_9_2_versammlung_ausserhalb(personen, erwartet):
    assert _stufe(
        nutzungsart="VERSAMMLUNG_AUSSERHALB_GEBAEUDE", personen_anzahl_bestimmt=personen
    ) == erwartet


@pytest.mark.parametrize(
    "flaeche,erwartet",
    [(250.0, "review_required"), (250.1, "eingeschraenkt"),
     (1600.0, "eingeschraenkt"), (1600.1, "uneingeschraenkt")],
)
def test_zeile_11_1_garage_nutzflaeche(flaeche, erwartet):
    assert _stufe(nutzungsart="GARAGE", nutzflaeche_garage_m2=flaeche) == erwartet


def test_zeile_11_1_gilt_auch_fuer_parkdeck():
    erg = _erg(nutzungsart="PARKDECK", nutzflaeche_garage_m2=2000.0)
    assert (erg.stufe, erg.zeile) == ("uneingeschraenkt", "11.1")


@pytest.mark.parametrize(
    "fluchtniveau,erwartet",
    [(22.1, "eingeschraenkt"), (32.0, "eingeschraenkt"), (32.1, "uneingeschraenkt")],
)
def test_zeile_12_1_wohngebaeude_ueber_22m(fluchtniveau, erwartet):
    assert _stufe(
        nutzungsart="WOHNGEBAEUDE",
        fluchtniveau_m=fluchtniveau,
        lage_zur_wohnung="AUSSERHALB_WOHNUNG",
    ) == erwartet


def test_fluchtniveau_grenze_22_trennt_zeile_1_1_von_12_1():
    auf_grenze = _erg(
        nutzungsart="WOHNGEBAEUDE",
        fluchtniveau_m=22.0,
        gebaeudeklasse="GK5",
        lage_zur_wohnung="AUSSERHALB_WOHNUNG",
    )
    darueber = _erg(
        nutzungsart="WOHNGEBAEUDE",
        fluchtniveau_m=22.1,
        lage_zur_wohnung="AUSSERHALB_WOHNUNG",
    )
    assert auf_grenze.zeile == "1.1"
    assert darueber.zeile == "12.1"


# ── Blockierende Unsicherheiten: rechnen ja, entscheiden nein ───────────────
@pytest.mark.parametrize("flaeche", [3200.0, 3200.1])
def test_zeile_2_netto_grundflaeche_immer_review(flaeche):
    # Die Definition der Netto-Grundfläche ist nicht abgesichert (MANUELL PRÜFEN).
    erg = _erg(nutzungsart="SCHULE_KINDERGARTEN", netto_grundflaeche_m2=flaeche)
    assert erg.stufe == "review_required"
    assert any("Netto-Grundfläche" in h for h in erg.hinweise)
    assert any("Kandidatenstufe" in h for h in erg.hinweise)
    assert erg.angewandter_schwellenwert is not None


def test_zeile_10_betriebsbau_astv_bleibt_review():
    erg = _erg(nutzungsart="BETRIEBSBAU", netto_grundflaeche_m2=5000.0)
    assert erg.stufe == "review_required"
    assert any("AStV" in h for h in erg.hinweise)
    assert any("MINDESTENS die eingeschränkte" in h for h in erg.hinweise)
    assert any("Kandidatenstufe (NICHT verbindlich" in h for h in erg.hinweise)


def test_zeile_10_unter_200_ist_review_ohne_kandidatenstufe():
    erg = _erg(nutzungsart="BETRIEBSBAU", netto_grundflaeche_m2=200.0)
    assert erg.stufe == "review_required"
    assert not any("Kandidatenstufe" in h for h in erg.hinweise)


@pytest.mark.parametrize("personen", [61, 240, 241])
def test_zeile_9_1_zwei_personenzahlen_blockieren(personen):
    erg = _erg(
        nutzungsart="VERSAMMLUNG_INNERHALB_GEBAEUDE", personen_anzahl_bestimmt=personen
    )
    assert erg.stufe == "review_required"
    assert any("zwei Personenzahlen" in h for h in erg.hinweise)
    assert any("Kandidatenstufe" in h for h in erg.hinweise)


def test_zeile_9_1_unter_60_personen_ist_review_ohne_kandidat():
    erg = _erg(nutzungsart="VERSAMMLUNG_INNERHALB_GEBAEUDE", personen_anzahl_bestimmt=60)
    assert erg.stufe == "review_required"
    assert not any("Kandidatenstufe" in h for h in erg.hinweise)


@pytest.mark.parametrize("flaeche", [1600.0, 1600.1])
def test_zeile_11_2_fussnoten_unklarheit_blockiert(flaeche):
    erg = _erg(nutzungsart="UEBERDACHTER_STELLPLATZ", nutzflaeche_garage_m2=flaeche)
    assert erg.stufe == "review_required"
    assert any("Fußnoten-Marker" in h for h in erg.hinweise)


# ── Schutzhütte (Punkt 7.9.12) ──────────────────────────────────────────────
def test_schutzhuette_unter_30_schlafplaetzen_review_kein_negativschluss():
    erg = _erg(nutzungsart="SCHUTZHUETTE_EXTREMLAGE", schlafplaetze_anzahl=29)
    assert erg.stufe == "review_required"
    assert any("Negativschluss" in h for h in erg.hinweise)
    assert not any("Kandidatenstufe" in h for h in erg.hinweise)


def test_schutzhuette_ab_30_schlafplaetzen_bleibt_review_auslegung():
    erg = _erg(
        nutzungsart="SCHUTZHUETTE_EXTREMLAGE", schlafplaetze_anzahl=30, betten_anzahl=40
    )
    assert erg.stufe == "review_required"
    assert erg.zeile == "3 (i.V.m. 7.9.12)"
    assert any("nennt aber keine Stufe" in h for h in erg.hinweise)
    assert any("Kandidatenstufe (NICHT verbindlich" in h for h in erg.hinweise)


def test_schutzhuette_fundstelle_zeigt_auf_punkt_7_9_12():
    erg = _erg(nutzungsart="SCHUTZHUETTE_EXTREMLAGE", schlafplaetze_anzahl=50)
    assert "7.9.12" in erg.fundstelle_seite


# ── Fehlende Fakten werden nie geraten ──────────────────────────────────────
@pytest.mark.parametrize(
    "nutzungsart,fakt",
    [
        ("BEHERBERGUNG_STUDENTENHEIM", "betten_anzahl"),
        ("PFLEGEHEIM", "betten_anzahl"),
        ("VERKAUFSSTAETTE_AUSSTELLUNGSSTAETTE", "verkaufsflaeche_m2"),
        ("SCHANK_SPEISEWIRTSCHAFT", "verabreichungsplaetze_anzahl"),
        ("DISKOTHEK_TANZCAFE", "personen_anzahl_bestimmt"),
        ("GARAGE", "nutzflaeche_garage_m2"),
    ],
)
def test_fehlender_kriteriumsfakt_ist_review(nutzungsart, fakt):
    erg = _erg(nutzungsart=nutzungsart)
    assert erg.stufe == "review_required"
    assert erg.fehlende_fakten == [fakt]
    assert erg.eingangswerte[fakt] == "nicht erhoben"


def test_fehlendes_fluchtniveau_blockiert_die_zeilenauswahl():
    erg = _erg(nutzungsart="WOHNGEBAEUDE", gebaeudeklasse="GK5")
    assert erg.stufe == "review_required"
    assert erg.fehlende_fakten == ["fluchtniveau_m"]
    assert erg.zeile is None


def test_fehlende_gebaeudeklasse_ist_review():
    erg = _erg(
        nutzungsart="WOHNGEBAEUDE",
        fluchtniveau_m=15.0,
        lage_zur_wohnung="AUSSERHALB_WOHNUNG",
    )
    assert erg.stufe == "review_required"
    assert erg.fehlende_fakten == ["gebaeudeklasse"]


def test_fehlende_lage_zur_wohnung_ist_review():
    erg = _erg(nutzungsart="WOHNGEBAEUDE", fluchtniveau_m=15.0, gebaeudeklasse="GK5")
    assert erg.stufe == "review_required"
    assert "lage_zur_wohnung" in erg.fehlende_fakten


def test_innerhalb_wohnung_ist_nicht_abgedeckt():
    erg = _erg(
        nutzungsart="WOHNGEBAEUDE",
        fluchtniveau_m=15.0,
        gebaeudeklasse="GK5",
        lage_zur_wohnung="INNERHALB_WOHNUNG",
    )
    assert erg.stufe == "review_required"
    assert any("außerhalb von Wohnungen" in h for h in erg.hinweise)


# ── Jurisdiktion ────────────────────────────────────────────────────────────
def test_ohne_jurisdiction_keine_verbindliche_stufe():
    projekt = ProjektKontext(gebaeudeteile=[Gebaeudeteil(id="gt", nutzungsart="KRANKENHAUS")])
    erg = PROV.bewerte_oib(projekt).ergebnisse[0]
    assert erg.stufe == "review_required"
    assert "jurisdiction" in erg.fehlende_fakten
    assert any("Kandidatenstufe (NICHT verbindlich" in h for h in erg.hinweise)
    # Die Tabellenzeile bleibt im Audit sichtbar.
    assert erg.zeile == "8"


# ── Nutzungsarten ohne auswertbare Zeile ────────────────────────────────────
def test_verkehrseinrichtung_ist_kann_aussage_also_review():
    erg = _erg(nutzungsart="VERKEHRSEINRICHTUNG")
    assert erg.stufe == "review_required"
    assert erg.zeile is None
    assert any("KÖNNEN" in h for h in erg.hinweise)


def test_nicht_in_tabelle_6_ist_review():
    erg = _erg(nutzungsart="NICHT_IN_TABELLE_6")
    assert erg.stufe == "review_required"
    assert erg.zeile is None


def test_jede_nutzungsart_ist_abgedeckt():
    """Kein Literal des Contracts darf durch das Raster fallen."""
    alle = set(Nutzungsart.__args__)
    assert alle - (PROV.abgedeckte_nutzungsarten | PROV.review_nutzungsarten) == set()


# ── Audit-Trail ─────────────────────────────────────────────────────────────
def test_audit_trail_vollstaendig_bei_definitiver_stufe():
    erg = _erg(nutzungsart="PFLEGEHEIM", betten_anzahl=17)
    assert erg.stufe == "uneingeschraenkt"
    assert erg.zeile == "7"
    assert erg.quelle == "OIB-Richtlinie 2, Punkt 5.4 + Tabelle 6"
    assert erg.norm_ausgabe.startswith("Ausgabe Mai 2023")
    assert erg.fundstelle_seite == "Norm-S. 32 / PDF-S. 34"
    assert erg.angewandter_schwellenwert == "> 16 Betten"
    assert erg.eingangswerte["betten_anzahl"] == "17"
    assert erg.eingangswerte["nutzungsart"] == "PFLEGEHEIM"
    assert erg.fehlende_fakten == []


def test_ausfuehrungs_verweise_je_stufe():
    eingeschraenkt = _erg(nutzungsart="PFLEGEHEIM", betten_anzahl=16)
    uneingeschraenkt = _erg(nutzungsart="PFLEGEHEIM", betten_anzahl=17)
    review = _erg(nutzungsart="PFLEGEHEIM")

    assert len(eingeschraenkt.ausfuehrungs_verweise) == 3
    assert any("Abweichung möglich" in v for v in eingeschraenkt.ausfuehrungs_verweise)
    assert any("NICHT auf Fluchtwege" in v for v in uneingeschraenkt.ausfuehrungs_verweise)
    assert any("OHNE die" in v for v in uneingeschraenkt.ausfuehrungs_verweise)
    # Ohne Entscheidung keine Ausführungsanforderung.
    assert review.ausfuehrungs_verweise == []


def test_globale_hinweise_haengen_an_jedem_ergebnis():
    erg = _erg(nutzungsart="KRANKENHAUS")
    assert any("Verbindlichkeit" in h for h in erg.hinweise)
    assert any("Rettungsweg" in h and "Fluchtweg" in h for h in erg.hinweise)
    assert any("Raumzuordnung NICHT geprüft" in h for h in erg.hinweise)


def test_astv_hinweis_je_nach_arbeitsstaette():
    ja = _erg(nutzungsart="KRANKENHAUS", arbeitsstaette_nach_aschg=True)
    nein = _erg(nutzungsart="KRANKENHAUS", arbeitsstaette_nach_aschg=False)
    unbekannt = _erg(nutzungsart="KRANKENHAUS")

    assert any("AStV-Parallelpfad" in h for h in ja.hinweise)
    assert any("nicht erhoben" in h for h in unbekannt.hinweise)
    assert not any("AStV" in h for h in nein.hinweise)
    # Der AStV-Pfad kann nur ergänzen — er senkt die Stufe nie.
    assert ja.stufe == nein.stufe == "uneingeschraenkt"


def test_raumreferenzen_werden_nicht_stillschweigend_als_geprueft_ausgegeben():
    befund = PROV.bewerte_oib(
        ProjektKontext(
            jurisdiction="AT",
            gebaeudeteile=[
                Gebaeudeteil(
                    id="gt",
                    nutzungsart="KRANKENHAUS",
                    raum_referenzen=[RaumReferenz(floor="EG", raum_id="r1")],
                )
            ],
        )
    )
    assert befund.nicht_zugeordnete_raum_referenzen == []
    assert any(
        "nicht auswertbar" in h for h in befund.ergebnisse[0].hinweise
    )


# ── Kein Umkehrschluss, global ──────────────────────────────────────────────
@pytest.mark.parametrize(
    "felder",
    [
        {"nutzungsart": "BEHERBERGUNG_STUDENTENHEIM", "betten_anzahl": 5},
        {"nutzungsart": "ALTEN_SENIORENHEIM", "betten_anzahl": 0},
        {"nutzungsart": "VERKAUFSSTAETTE_AUSSTELLUNGSSTAETTE", "verkaufsflaeche_m2": 50.0},
        {"nutzungsart": "SCHANK_SPEISEWIRTSCHAFT", "verabreichungsplaetze_anzahl": 20},
        {"nutzungsart": "VERSAMMLUNG_AUSSERHALB_GEBAEUDE", "personen_anzahl_bestimmt": 10},
        {"nutzungsart": "GARAGE", "nutzflaeche_garage_m2": 100.0},
        {"nutzungsart": "UEBERDACHTER_STELLPLATZ", "nutzflaeche_garage_m2": 100.0},
        {"nutzungsart": "BETRIEBSBAU", "netto_grundflaeche_m2": 10.0},
    ],
)
def test_unter_der_schwelle_niemals_nicht_erforderlich(felder):
    erg = _erg(**felder)
    assert erg.stufe == "review_required"
    assert any("kein Umkehrschluss" in h for h in erg.hinweise)


def test_nicht_erforderlich_wird_nie_zurueckgegeben():
    """Mit den heute im Repo liegenden Quellen gibt es keinen belegten Fall."""
    teile = [
        Gebaeudeteil(id=f"gt{i}", nutzungsart=art)
        for i, art in enumerate(Nutzungsart.__args__)
    ]
    befund = PROV.bewerte_oib(ProjektKontext(jurisdiction="AT", gebaeudeteile=teile))
    assert all(e.stufe != "nicht_erforderlich" for e in befund.ergebnisse)
