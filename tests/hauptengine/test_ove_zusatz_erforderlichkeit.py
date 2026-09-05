"""Regel 14 — belegte Erforderlichkeit nach OVE E 8101 718.560.9.001.AT Punkt 1.

Geprüfte Quellenkette (nur diese eine Nutzung): OVE E 8101:2019-01-01
718.560.9.001.AT → OVE-Richtlinie R 12-2/AC:2019-07-01 Tabelle 5.1 Zeile 4
(Spalte „Erhöhte Anforderungen") → OIB-RL 2 Ausgabe Mai 2023 Tabelle 6 Zeile 4
(Spalte „uneingeschränkt"). Details: `docs/NORMQUELLEN_AT.md` Abschnitt 2d.

Der Befund sagt **erforderlich**, nicht **erfüllt**: Beleuchtungsart und
lichttechnischer Nachweis nennt die Klausel nicht. Es wird nichts platziert und
keine Schwelle aktiviert.
"""
from __future__ import annotations

import pytest

from notbeleuchtung.hauptengine.contracts import (
    BBox,
    Gebaeudeteil,
    ProjektKontext,
    Raum,
    RaumModell,
    RaumReferenz,
)
from notbeleuchtung.hauptengine.validierung import pruefe
from notbeleuchtung.normwissen import En1838NormProvider, OibRl2Provider
from notbeleuchtung.platzierung import NotlichtPlatzierer

POLY = [(0.0, 0.0), (3000.0, 0.0), (3000.0, 3000.0), (0.0, 3000.0)]
REGEL_14 = "Sicherheitsbeleuchtung erforderlich (OVE E 8101"
REGEL_13 = "Geltungsbereich ungeklärt"


def _raum(*raeume: Raum) -> RaumModell:
    return RaumModell(
        floor="EG", bounds_mm=BBox(min_xy=(0.0, 0.0), max_xy=(9000.0, 3000.0)),
        raeume=list(raeume),
    )


def _wc(rid: str = "wc_1", flaeche: float = 9.0, typ: str = "WC") -> Raum:
    return Raum(id=rid, raum_typ=typ, polygon_mm=POLY, flaeche_m2=flaeche)


def _verkauf(flaeche: float = 4000.0, refs=("wc_1",), tid: str = "gt_verkauf") -> Gebaeudeteil:
    return Gebaeudeteil(
        id=tid, nutzungsart="VERKAUFSSTAETTE_AUSSTELLUNGSSTAETTE",
        gebaeudeklasse="GK4", verkaufsflaeche_m2=flaeche,
        raum_referenzen=[RaumReferenz(floor="EG", raum_id=r) for r in refs],
    )


def _befunde(raum: RaumModell, *teile: Gebaeudeteil):
    pk = ProjektKontext(jurisdiction="AT", gebaeudeteile=list(teile))
    oib = OibRl2Provider().bewerte_oib(pk)
    erg = NotlichtPlatzierer().place(raum, En1838NormProvider(), oib=oib)
    return pruefe(raum, erg, norm=En1838NormProvider(), oib=oib, projekt_kontext=pk), erg


def _regel(befunde, marker):
    return [b for b in befunde if marker in b.regel]


# ── Der belegte Fall ────────────────────────────────────────────────────────
def test_verkaufsstaette_4000_mit_zugeordnetem_wc_9m2():
    befunde, erg = _befunde(_raum(_wc()), _verkauf())
    (treffer,) = _regel(befunde, REGEL_14)
    assert treffer.status == "warnung"
    assert "wc_1" in treffer.detail
    # Erforderlichkeit belegt, Ausführung offen — beides im Text.
    assert "Beleuchtungsart und lichttechnischer Nachweis noch offen" in treffer.regel
    # Die Art ist nicht festgelegt — und daraus folgt keine automatische Antipanik.
    assert "legt die Beleuchtungsart" in treffer.detail
    assert "automatische Zuordnung zu Antipanik ist damit nicht belegt" in treffer.detail
    # Keine Fussnoten-Begruendung im Befundtext — die sachliche Aussage genuegt.
    assert "Fussnote a" not in treffer.detail
    # Quellenkette mit Ausgabestand, alle drei Glieder.
    for quelle in ("OVE E 8101:2019-01-01", "R 12-2/AC:2019-07-01", "Ausgabe Mai 2023"):
        assert quelle in treffer.detail
    # Keine Platzierung aus diesem Befund.
    assert erg.platzierungen == []


def test_belegter_raum_erscheint_nicht_mehr_als_ungeklaert():
    """Für diesen Raum ist der Geltungsbereich geklärt — Regel 13 darf dort nicht
    weiter „R 12-2 fehlt" melden."""
    befunde, _ = _befunde(_raum(_wc()), _verkauf())
    assert _regel(befunde, REGEL_14)
    assert not _regel(befunde, REGEL_13)


def test_andere_ungeklaerte_raeume_bleiben_sichtbar():
    """Ein zweiter, nicht zugeordneter Raum bleibt ungeklärt — die Ausnahme gilt
    nur dem belegten Fall."""
    befunde, _ = _befunde(_raum(_wc(), _wc("wc_2")), _verkauf(refs=("wc_1",)))
    assert _regel(befunde, REGEL_14)
    (unklar,) = _regel(befunde, REGEL_13)
    assert "wc_2" in unklar.detail and "wc_1" not in unklar.detail


# ── Grenzen ─────────────────────────────────────────────────────────────────
@pytest.mark.parametrize("verkaufsflaeche,belegt", [(3000.1, True), (3000.0, False), (2999.0, False)])
def test_grenze_3000_m2_verkaufsflaeche(verkaufsflaeche, belegt):
    """Tabelle 6/5.1 Zeile 4: erhöhte Anforderungen erst **über** 3.000 m²."""
    befunde, _ = _befunde(_raum(_wc()), _verkauf(flaeche=verkaufsflaeche))
    assert bool(_regel(befunde, REGEL_14)) is belegt


@pytest.mark.parametrize("flaeche,belegt", [(8.0, True), (8.1, True), (7.9, False)])
def test_grenze_8_m2_sanitaerflaeche(flaeche, belegt):
    """718.560.9.001.AT Punkt 1: „in Sanitärbereichen **ab** 8 m² Größe"."""
    befunde, _ = _befunde(_raum(_wc(flaeche=flaeche)), _verkauf())
    assert bool(_regel(befunde, REGEL_14)) is belegt


def test_kein_sanitaerraum_kein_befund():
    befunde, _ = _befunde(_raum(_wc(typ="ZIMMER")), _verkauf())
    assert not _regel(befunde, REGEL_14)


def test_fehlende_verkaufsflaeche_ist_kein_beleg():
    """Ohne Zahl kein Beleg — und die OIB-Auswertung liefert dann ohnehin
    review_required."""
    teil = Gebaeudeteil(
        id="gt_ohne", nutzungsart="VERKAUFSSTAETTE_AUSSTELLUNGSSTAETTE",
        raum_referenzen=[RaumReferenz(floor="EG", raum_id="wc_1")],
    )
    befunde, _ = _befunde(_raum(_wc()), teil)
    assert not _regel(befunde, REGEL_14)
    assert _regel(befunde, REGEL_13)


# ── Zuordnung ───────────────────────────────────────────────────────────────
def test_ohne_raumzuordnung_kein_befund():
    befunde, _ = _befunde(_raum(_wc()), _verkauf(refs=()))
    assert not _regel(befunde, REGEL_14)
    assert _regel(befunde, REGEL_13)


def test_widerspruechliche_zuordnung_kein_befund():
    """Derselbe Raum hängt zusätzlich an einem Teil mit review_required →
    die Zuordnung ist nicht eindeutig, also kein belegter Fall."""
    unklar = Gebaeudeteil(
        id="gt_unklar", nutzungsart="VERKEHRSEINRICHTUNG",
        raum_referenzen=[RaumReferenz(floor="EG", raum_id="wc_1")],
    )
    befunde, _ = _befunde(_raum(_wc()), _verkauf(), unklar)
    assert not _regel(befunde, REGEL_14)
    assert _regel(befunde, REGEL_13)


def test_gemischte_nutzung_trifft_nur_den_eigenen_raum():
    """R 12-2 Fußnote c / OIB 5.4: je Nutzung. Der Wohnteil-Raum bleibt außen vor."""
    wohnen = Gebaeudeteil(
        id="gt_wohnen", nutzungsart="WOHNGEBAEUDE", gebaeudeklasse="GK5",
        lage_zur_wohnung="AUSSERHALB_WOHNUNG",
        raum_referenzen=[RaumReferenz(floor="EG", raum_id="wc_2")],
    )
    befunde, _ = _befunde(_raum(_wc(), _wc("wc_2")), _verkauf(), wohnen)
    (treffer,) = _regel(befunde, REGEL_14)
    assert "wc_1" in treffer.detail and "wc_2" not in treffer.detail


def test_andere_nutzung_erzeugt_keinen_befund():
    """Nur Zeile 4 ist geprüft — für andere Nutzungen wird nichts behauptet."""
    schule = Gebaeudeteil(
        id="gt_schule", nutzungsart="SCHULE_KINDERGARTEN",
        netto_grundflaeche_m2=9000.0,
        raum_referenzen=[RaumReferenz(floor="EG", raum_id="wc_1")],
    )
    befunde, _ = _befunde(_raum(_wc()), schule)
    assert not _regel(befunde, REGEL_14)


# ── Unabhängigkeit ──────────────────────────────────────────────────────────
def test_platzierungen_bleiben_unveraendert():
    """Der Befund platziert nichts und unterdrückt nichts: ein SAAL bekommt seine
    typ-begründete Antipanik wie ohne ProjektKontext."""
    saal = Raum(id="saal", raum_typ="SAAL", polygon_mm=POLY, flaeche_m2=80.0)
    raum = _raum(_wc(), saal)
    ohne = NotlichtPlatzierer().place(raum, En1838NormProvider())
    _, mit = _befunde(raum, _verkauf())
    assert [(p.kind, p.xy_mm) for p in mit.platzierungen] == \
           [(p.kind, p.xy_mm) for p in ohne.platzierungen]
    assert any(p.kind == "antipanik" for p in ohne.platzierungen)


def test_schwellen_bleiben_leer():
    s = En1838NormProvider().regelwerk_snapshot().flaechen_schwellen
    assert s.antipanik_min_m2 is None and s.wc_sanitaer_min_m2 is None


def test_ohne_projekt_kontext_kein_befund():
    raum = _raum(_wc())
    erg = NotlichtPlatzierer().place(raum, En1838NormProvider())
    befunde = pruefe(raum, erg, norm=En1838NormProvider())
    assert not _regel(befunde, REGEL_14) and not _regel(befunde, REGEL_13)


# ── Bis zur tatsächlichen Ausgabe ───────────────────────────────────────────
def test_befund_erreicht_den_gezeichneten_pruefbericht(tmp_path):
    """Sichtbarkeit bis zum Plan: der Befund steht im gezeichneten Prüfbericht
    des DXF und nimmt den Gesamtstatus mit."""
    ezdxf = pytest.importorskip("ezdxf")
    from notbeleuchtung.hauptengine.pipeline import run
    from notbeleuchtung.hauptengine.render import render_dxf
    from notbeleuchtung.hauptengine.validierung import pruefbericht

    raum = _raum(_wc())
    pk = ProjektKontext(jurisdiction="AT", gebaeudeteile=[_verkauf()])
    oib = OibRl2Provider().bewerte_oib(pk)
    erg = NotlichtPlatzierer().place(raum, En1838NormProvider(), oib=oib)
    bericht = pruefbericht(
        raum, erg, norm=En1838NormProvider(), oib=oib, projekt_kontext=pk
    )
    assert bericht["status"] == "warnung"

    out = tmp_path / "plan.dxf"
    render_dxf(erg, raum, str(out), None, pruefung=bericht)
    doc = ezdxf.readfile(str(out))
    bloecke = [
        e.text for e in doc.modelspace()
        if e.dxftype() == "MTEXT" and "PRÜFBERICHT" in e.text
    ]
    assert len(bloecke) == 1
    assert "Sicherheitsbeleuchtung erforderlich" in bloecke[0]
    assert bloecke[0].startswith("PRÜFBERICHT (EN 1838): WARNUNG")
    assert run  # Pipeline reicht projekt_kontext durch (test_pipeline_oib deckt das)


# ── Ausgabestand ────────────────────────────────────────────────────────────
def test_befund_steht_unter_ausgewiesenem_vorbehalt():
    """Für die OVE-Ausgaben gibt es im Projekt keine Auswahl — der Befund ist
    eine Vorprüfung und sagt das auch."""
    befunde, _ = _befunde(_raum(_wc()), _verkauf())
    (treffer,) = _regel(befunde, REGEL_14)
    assert "Vorprüfung" in treffer.regel
    assert (
        "Unter der geprueften Quellenkombination ist Sicherheitsbeleuchtung "
        "erforderlich; die Anwendbarkeit dieser Ausgaben auf das Projekt ist noch "
        "zu bestaetigen."
    ) in treffer.detail
    # Kein Ausschluss der Ausgabe 2025 behauptet.
    assert "weder behauptet noch ausgeschlossen" in treffer.detail
    assert "2025" not in treffer.detail


def test_fremde_oib_ausgabe_erzeugt_keinen_befund():
    """Ausführbare Absicherung: kommt der Befund aus einer anderen OIB-Ausgabe als
    der geprüften, gilt die Kette nicht — der Fall bleibt ungeklärt."""
    from notbeleuchtung.hauptengine.contracts import OibBefund, OibErgebnis
    from notbeleuchtung.hauptengine.validierung import pruefe as _pruefe

    raum = _raum(_wc())
    teil = _verkauf()
    pk = ProjektKontext(jurisdiction="AT", gebaeudeteile=[teil])
    fremd = OibBefund(ergebnisse=[OibErgebnis(
        gebaeudeteil_id=teil.id, stufe="uneingeschraenkt",
        quelle="OIB-Richtlinie 2, Punkt 5.4 + Tabelle 6",
        norm_ausgabe="Ausgabe April 2019",          # NICHT die geprüfte Ausgabe
        raum_referenzen=list(teil.raum_referenzen),
    )])
    erg = NotlichtPlatzierer().place(raum, En1838NormProvider(), oib=fremd)
    befunde = _pruefe(raum, erg, norm=En1838NormProvider(), oib=fremd, projekt_kontext=pk)
    assert not _regel(befunde, REGEL_14)
    assert _regel(befunde, REGEL_13)


def test_akzeptierter_stand_stimmt_heute_mit_dem_provider_ueberein():
    """Heute passen Pin und Provider zusammen — deshalb entsteht der Befund."""
    from notbeleuchtung.normwissen import OveZusatzKatalog

    katalog = OveZusatzKatalog()
    pk = ProjektKontext(jurisdiction="AT", gebaeudeteile=[_verkauf()])
    ergebnis = OibRl2Provider().bewerte_oib(pk).ergebnisse[0]
    assert katalog.passt_zur_geprueften_oib_ausgabe(ergebnis.norm_ausgabe)
    assert katalog.ausgaben_pruefstatus() == {
        "oib_rl2": "ausfuehrbar_geprueft",
        "ove_e8101": "nicht_pruefbar",
        "r12_2": "nicht_pruefbar",
    }


def test_akzeptierter_stand_haengt_am_quellenbeleg_nicht_an_den_provider_metadaten(tmp_path):
    """Der entscheidende Regressionsfall: die **Provider-Metadaten** wandern auf
    eine neue OIB-Ausgabe — Metadaten und `OibErgebnis.norm_ausgabe` wechseln
    also gemeinsam —, während der **Quellenbeleg der Zusatzregel** unverändert
    Mai 2023 nennt.

    Erwartung: **keine** positive OVE-Vorprüfung. Die Spalten-Entsprechung ist nur
    gegen Mai 2023 geprüft; ein Ausgabenwechsel der allgemeinen Auswertung darf
    den akzeptierten Stand nicht stillschweigend erweitern. Der offene Prüfbedarf
    bleibt sichtbar (Regel 13).
    """
    import shutil

    from notbeleuchtung.normwissen import OveZusatzKatalog
    from notbeleuchtung.normwissen.oib import OibRl2Provider as Provider
    from notbeleuchtung.normwissen.provider import DATA_DIR

    # Provider-Datenstand kopieren und auf eine ANDERE Ausgabe heben.
    for name in ("oib_rl2_tabelle6.yaml", "ove_e8101_zusatz.yaml"):
        shutil.copy(DATA_DIR / name, tmp_path / name)
    oib_yaml = tmp_path / "oib_rl2_tabelle6.yaml"
    alt_stand = "Ausgabe Mai 2023 (OIB-330.2-029/23)"
    neuer_stand = "Ausgabe Maerz 2027 (OIB-330.2-999/27)"
    oib_yaml.write_text(
        oib_yaml.read_text(encoding="utf-8").replace(alt_stand, neuer_stand),
        encoding="utf-8",
    )

    raum = _raum(_wc())
    teil = _verkauf()
    pk = ProjektKontext(jurisdiction="AT", gebaeudeteile=[teil])
    befund = Provider(tmp_path).bewerte_oib(pk)

    # Metadaten UND Ergebnis tragen jetzt die neue Ausgabe …
    assert befund.ergebnisse[0].norm_ausgabe == neuer_stand
    assert befund.ergebnisse[0].stufe == "uneingeschraenkt"
    # … der Quellenbeleg der Zusatzregel dagegen unverändert Mai 2023.
    assert OveZusatzKatalog(tmp_path).oib_ausgabe() == alt_stand

    erg = NotlichtPlatzierer().place(raum, En1838NormProvider(), oib=befund)
    befunde = pruefe(raum, erg, norm=En1838NormProvider(), oib=befund, projekt_kontext=pk)
    assert not _regel(befunde, REGEL_14)          # keine positive Vorprüfung
    assert _regel(befunde, REGEL_13)              # Prüfbedarf bleibt sichtbar
