"""Track-B-Norm-Werte (Contract v1.1.0) — die Fachaussagen, festgenagelt.

PR #72 hat `NormRegelwerk` um vier abfragbare Felder erweitert; PR #80 konsumiert
sie bereits. Diese Tests halten fest, **welche** Werte belegt sind, welche
bewusst leer bleiben und warum — geprüft am Volltext der im Repo liegenden
Ausgabe (`knowledge/_extracted_text/normen/EN 1838 - Notbeleuchtung 2019.txt`).

Der scharfe Fall ist die Gleichmäßigkeit: die in PR #72, `platzierung/lux.py` und
im COORDINATION-Log kursierende Angabe „40 Rettungsweg / 10 Antipanik" ist
falsch. §4.3.2 gibt für Antipanik dieselben 1:40 wie §4.2.2 für den Rettungsweg;
die „10" stammt aus §4.4.2 und ist ein anderes Maß (Uo statt Ud).
"""
from notbeleuchtung.normwissen import En1838NormProvider

P = En1838NormProvider()
SNAP = P.regelwerk_snapshot()


# ── Gleichmäßigkeit Ud (§4.2.2 / §4.3.2) ────────────────────────────────────
def test_antipanik_ud_ist_40_nicht_10():
    """§4.3.2: „Die Ungleichmäßigkeit Ud … darf 1 : 40 nicht unterschreiten."

    Wortgleich mit §4.2.2 für den Rettungsweg. Antipanik ist NICHT 1:10 — das
    ist der Regressionstest gegen die kursierende Fehlangabe.
    """
    assert P.fuer_raum("GANG", True).gleichmaessigkeit_max == 40.0
    assert P.fuer_raum("SAAL", False).gleichmaessigkeit_max == 40.0
    assert P.fuer_raum("AUFENTHALTSRAUM", False).gleichmaessigkeit_max == 40.0


def test_uo_aus_4_4_2_landet_nicht_in_gleichmaessigkeit_max():
    """§4.4.2 fordert Uo ≥ 0,1 für Arbeitsplätze mit besonderer Gefährdung.

    Uo (kleinste : mittlere) ist nicht Ud (kleinste : größte) — der Wert darf
    weder als 10 noch als 0,1 in dieses Feld rutschen.
    """
    werte = {r.anforderung.gleichmaessigkeit_max for r in SNAP.regeln}
    assert 10.0 not in werte
    assert 0.1 not in werte


def test_aufheller_ohne_ud_beleg_bleibt_none():
    """Für Aufheller/Betonungsleuchten (§4.1) nennt EN 1838 keine eigene
    Ud-Anforderung → kein Wert, kein stiller Norm-Default."""
    assert P.fuer_raum("STIEGENHAUS", True).gleichmaessigkeit_max is None


def test_fluchtweg_abschnitt_traegt_die_rettungsweg_ud():
    """Jeder Fluchtweg-Abschnitt ist ein Rettungsweg (§4.2) → 1:40."""
    assert P.fuer_fluchtweg_abschnitt(None).gleichmaessigkeit_max == 40.0


# ── Umschaltzeit (§4.2.6 / §4.3.6 / §5.4.6) ─────────────────────────────────
def test_umschaltzeit_ist_der_vollwert_zeitpunkt():
    """Die Norm ist zweistufig — 50 % in 5 s, 100 % in 60 s. Das Contract-Feld
    ist ein Skalar und trägt deshalb den 60-s-Vollwert; ein 5er dort hieße
    „volle Beleuchtungsstärke in 5 s" und wäre strenger als die Norm."""
    for raum_typ, fluchtweg in (("GANG", True), ("SAAL", False), ("STIEGENHAUS", True)):
        assert P.fuer_raum(raum_typ, fluchtweg).umschaltzeit_max_s == 60.0


def test_halbwertstufe_bleibt_in_der_yaml_sichtbar():
    """Die 5-s-Stufe hat kein Contract-Feld — sie darf trotzdem nicht aus der
    Wissensbasis verschwinden, sonst geht die Norm-Aussage still verloren."""
    import yaml

    from notbeleuchtung.normwissen.provider import DATA_DIR

    with open(DATA_DIR / "en1838_grundwerte.yaml", encoding="utf-8") as fh:
        grund = yaml.safe_load(fh)
    assert grund["umschaltzeit"]["halbwert_s"] == 5.0
    assert grund["umschaltzeit"]["vollwert_s"] == 60.0


# ── Bewusst NICHT gefüllt ───────────────────────────────────────────────────
def test_flaechen_schwellen_bleiben_ohne_en_1838_beleg_leer():
    """60 m² / 8 m² stehen NICHT in EN 1838.

    Belegt sind sie in OVE E 8101:2019 718.560.9.001.AT und ÖVE/ÖNORM E 8002-1
    — dort aber scope-gebunden (erhöhte Anforderungen nach der Art der Nutzung
    bzw. nur Flughäfen/Bahnhöfe). Das Contract-Feld wirkt global. Bis zur
    3-Owner-Entscheidung über ein Scope-Gate bleibt es leer, statt die Schwelle
    auf jedes Gebäude anzuwenden.
    """
    assert SNAP.flaechen_schwellen.antipanik_min_m2 is None
    assert SNAP.flaechen_schwellen.wc_sanitaer_min_m2 is None


def test_arbeitsplatz_lux_bleibt_leer_solange_der_raumtyp_fehlt():
    """§4.4.1 (10 % / mind. 15 lx) ist belegt, aber das RaumModell kennt keinen
    „Arbeitsplatz mit besonderer Gefährdung" → der Wert hätte keinen Auslöser
    und wäre toter Code (Track C, @polatselman)."""
    assert SNAP.arbeitsplatz_lux.min_lux is None
    assert SNAP.arbeitsplatz_lux.min_lux_absolut is None


# ── Naht ────────────────────────────────────────────────────────────────────
def test_track_b_werte_stehen_nicht_in_den_quellen():
    """Die Track-B-Fundstellen (§4.2.2/§4.3.2/§4.2.6) stehen bewusst NICHT in
    `quellen`: sie begründen keine eigene Platzierung, sondern präzisieren Werte
    bestehender Anforderungen. `quellen` führt nur Strings, die als
    `Platzierung.norm_quelle` auftreten können."""
    for nicht_drin in ("§4.2.2", "§4.3.2", "§4.2.6"):
        assert not any(nicht_drin in q for q in SNAP.quellen)


def test_quellen_sind_die_drei_raumregeln_plus_die_sonderstellen():
    """`quellen` ist rein additiv gewachsen: die drei Raumregel-Fundstellen sind
    unverändert da, dazu kommen die Auslöser der Sonderstellen (§4.1.2 c/h/i) und
    der beiden Raum-Attribute (§4.3.8, §4.4.1).

    Erst dadurch kann eine Sonderstellen-Platzierung ihre ECHTE Fundstelle
    tragen, ohne die Naht-Invariante `norm_quelle ∈ quellen` zu verletzen. Die
    Menge wird nur größer — bestehende Platzierungen bleiben gültig.

    `tests/fixtures/norm_regelwerk_snapshot.json` (3-Owner-Lane) bleibt bei den
    drei alten Strings und wird hier bewusst NICHT nachgezogen; siehe
    docs/SPEC_SONDERSTELLEN_CONTRACT.md §7.
    """
    assert SNAP.quellen == [
        "ÖNORM EN 1838:2013 §4.1",
        "ÖNORM EN 1838:2013 §4.1.2 c)",
        "ÖNORM EN 1838:2013 §4.1.2 h)",
        "ÖNORM EN 1838:2013 §4.1.2 i)",
        "ÖNORM EN 1838:2013 §4.2.1",
        "ÖNORM EN 1838:2013 §4.3.1",
        "ÖNORM EN 1838:2013 §4.3.8",
        "ÖNORM EN 1838:2013 §4.4.1",
    ]
    for alt in ("§4.1", "§4.2.1", "§4.3.1"):
        assert f"ÖNORM EN 1838:2013 {alt}" in SNAP.quellen
