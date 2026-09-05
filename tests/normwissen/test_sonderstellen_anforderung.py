"""Sonderstellen-Anforderungen — eigene Fundstelle, eigener Geltungsbereich, eigene Bezugsfläche.

Befund an PR #95: die Platzierung einer Pflicht-Leuchte übernahm die `quelle` der
erstbesten Raumregel derselben Leuchtenart — eine Feuerlöscher-Leuchte trug damit
`§4.1` (STIEGENHAUS), ein Niveauänderungs-RZ `§4.2.1` (GANG).

Korrektur-Slice 05.09.2026 zusätzlich:
* §4.3.8 gilt für **Toiletten** für Menschen mit Behinderung — nicht für jeden
  Raum mit `ist_barrierefrei`.
* §4.4.1 bezieht sich auf die **Arbeitsfläche**, nicht auf den Boden.
* §4.1.2 c) belegt die **Sicherheitsleuchte**; ein zusätzliches Rettungszeichen
  ist kein Norm-Default.

Fundstellen am Original geprüft (`knowledge/EN 1838 - Notbeleuchtung 2019 (1).pdf`,
Kopf „EN 1838:2013 (D)"): §4.1.2 c) Norm-S.8 · h)/i) Norm-S.9 · §4.3.1 + §4.3.8
Norm-S.11 · §4.4.1 Norm-S.12.
"""
import pytest

from notbeleuchtung.normwissen import En1838NormProvider

PROV = En1838NormProvider()
SNAP = PROV.regelwerk_snapshot()

RAUMREGEL_QUELLEN = {
    "ÖNORM EN 1838:2013 §4.1",
    "ÖNORM EN 1838:2013 §4.2.1",
    "ÖNORM EN 1838:2013 §4.3.1",
}

# h) ist die Erste-Hilfe-Stelle, i) sind Brandbekämpfungs- UND Meldeeinrichtungen.
ERWARTET = {
    "feuerloescher": "ÖNORM EN 1838:2013 §4.1.2 i)",
    "hydrant": "ÖNORM EN 1838:2013 §4.1.2 i)",
    "brandmelder": "ÖNORM EN 1838:2013 §4.1.2 i)",
    "erste_hilfe": "ÖNORM EN 1838:2013 §4.1.2 h)",
    "niveauaenderung": "ÖNORM EN 1838:2013 §4.1.2 c)",
}
GERAETE = ["feuerloescher", "hydrant", "erste_hilfe", "brandmelder"]


# ── 1. Fundstelle je Auslöser ───────────────────────────────────────────────
@pytest.mark.parametrize("typ,quelle", sorted(ERWARTET.items()))
def test_jede_sonderstelle_traegt_ihre_eigene_fundstelle(typ, quelle):
    for anf in PROV.fuer_sonderstelle(typ):
        assert anf.quelle == quelle
        assert anf.quelle not in RAUMREGEL_QUELLEN   # genau der alte Fehler


def test_erste_hilfe_ist_h_und_brandschutz_ist_i():
    assert PROV.fuer_sonderstelle("erste_hilfe")[0].quelle.endswith("§4.1.2 h)")
    for typ in ("feuerloescher", "hydrant", "brandmelder"):
        assert PROV.fuer_sonderstelle(typ)[0].quelle.endswith("§4.1.2 i)")


# ── 2. §4.3.8 — Toiletten, nicht „barrierefrei" allgemein ───────────────────
def test_barrierefreies_wc_loest_4_3_8_aus():
    (anf,) = PROV.fuer_raum_attribut("ist_barrierefrei", "WC")
    assert anf.quelle == "ÖNORM EN 1838:2013 §4.3.8"
    assert anf.klassifikation == "antipanik"


def test_gewoehnliches_wc_loest_ohne_flag_nichts_aus():
    """Das Attribut wird nur gefragt, wenn der Raum es trägt — die Norm knüpft an
    „für Menschen mit Behinderung" an, nicht an „WC". Der Katalog liefert die
    Anforderung des ATTRIBUTS; ein WC ohne Flag fragt sie gar nicht ab. Der Test
    hält fest, dass die Raumtyp-Bindung nicht umgekehrt wirkt: WC allein ist
    kein Auslöser, sondern nur die notwendige Bedingung neben dem Flag."""
    regel = PROV.fuer_raum("WC", False)
    assert regel.quelle in RAUMREGEL_QUELLEN
    assert regel.quelle != "ÖNORM EN 1838:2013 §4.3.8"


def test_barrierefreies_zimmer_loest_4_3_8_nicht_aus():
    """§4.3.8 nennt Toiletten. Ein barrierefreies Zimmer fällt nicht darunter."""
    assert PROV.fuer_raum_attribut("ist_barrierefrei", "ZIMMER") == []


def test_leere_liste_heisst_nicht_kein_licht():
    """Andere Anforderungen bleiben unabhängig: der Raum bekommt weiterhin, was
    seine Raumtyp-Regel bzw. der Fluchtweg-Pfad vorsieht."""
    assert PROV.fuer_raum_attribut("ist_barrierefrei", "ZIMMER") == []
    assert PROV.fuer_raum("ZIMMER", False).min_lux > 0


def test_ohne_raumtyp_keine_entscheidung():
    """Fail closed: §4.3.8 ist ohne Raumtyp nicht entscheidbar — kein Default."""
    with pytest.raises(ValueError, match="raumtyp-gebunden"):
        PROV.fuer_raum_attribut("ist_barrierefrei")


def test_barrierefrei_leiht_den_horizontalen_wert_von_4_3_1():
    """§4.3.8 nennt keinen Zahlenwert; es gilt das Antipanik-Niveau (§4.3.1:
    0,5 lx horizontal auf der freien Bodenfläche). Geliehen, nicht erfunden."""
    (anf,) = PROV.fuer_raum_attribut("ist_barrierefrei", "WC")
    assert anf.lux.bezugsflaeche == "horizontal_boden"
    assert anf.lux_horizontal_boden == 0.5
    assert anf.lux.quelle == "ÖNORM EN 1838:2013 §4.3.1"
    assert anf.lux_vertikal_am_geraet is None
    assert anf.nachweis_offen is False      # Wert ist bestimmbar


# ── 3. §4.4.1 — Bezugsfläche ist die Arbeitsfläche ──────────────────────────
def test_besondere_gefaehrdung_bezieht_sich_auf_die_arbeitsflaeche():
    (anf,) = PROV.fuer_raum_attribut("besondere_gefaehrdung")
    assert anf.lux.bezugsflaeche == "arbeitsflaeche"
    # Weder Boden noch vertikal am Gerät — beides wäre unterstellt.
    assert anf.lux_horizontal_boden is None
    assert anf.lux_vertikal_am_geraet is None


def test_besondere_gefaehrdung_dokumentiert_15_lx_und_10_prozent():
    (anf,) = PROV.fuer_raum_attribut("besondere_gefaehrdung")
    assert anf.lux.mindestwert == 15.0
    assert anf.lux.anteil_nennbeleuchtung == 0.10
    assert anf.quelle == "ÖNORM EN 1838:2013 §4.4.1"


def test_besondere_gefaehrdung_bleibt_ohne_aufgabenbeleuchtung_offen():
    """Der 10-%-Anteil braucht den Wartungswert der Aufgabenbeleuchtung, die
    Arbeitsfläche ist im RaumModell nicht beschrieben → kein berechneter Wert,
    Nachweis offen."""
    (anf,) = PROV.fuer_raum_attribut("besondere_gefaehrdung")
    assert anf.lux.wert is None
    assert anf.lux.vollstaendig_bestimmbar is False
    assert anf.nachweis_offen is True
    assert "Arbeitsfläche" in anf.nachweis_offen_grund
    assert "15 lx" in anf.nachweis_offen_grund


# ── 4. Niveauänderung — c) belegt die Leuchte, nicht das Zeichen ────────────
def test_niveauaenderung_liefert_als_norm_default_nur_die_sicherheitsleuchte():
    anfs = PROV.fuer_sonderstelle("niveauaenderung")
    assert [a.klassifikation for a in anfs] == ["sicherheitsleuchte"]
    assert anfs[0].ist_norm_default is True


def test_rettungszeichen_an_niveauaenderung_ist_kein_norm_default():
    """§4.1.2 c) fordert kein Zeichen; d) verlangt nur, dass VORHANDENE
    Sicherheitszeichen beleuchtet sind. Ohne eigene Entscheidungs-Quelle (LB)
    entsteht keine RZ-Pflicht — und keine erfundene Norm-Quelle."""
    (rz,) = PROV.zur_pruefung("niveauaenderung")
    assert rz.klassifikation == "rz"
    assert rz.ist_norm_default is False
    assert rz.quelle is None                      # keine Norm-Fundstelle
    assert rz.decision_source == "lb_explizit"
    assert "LB" in rz.begruendung or "Auftraggeber" in rz.begruendung
    assert rz.nachweis_offen is True


def test_kandidaten_stehen_nicht_in_den_norm_quellen():
    """Was keine Norm-Quelle hat, darf auch keine in `quellen` bekommen."""
    for anf in PROV.zur_pruefung("niveauaenderung"):
        assert anf.quelle is None
    assert not any("rz_stellen" in q for q in SNAP.quellen)


def test_matrix_fuehrt_rz_06_nicht_mehr_als_norm_default():
    from notbeleuchtung.normwissen import PlatzierungsRegelwerk
    w = PlatzierungsRegelwerk()
    rz06 = w.regel("RZ-06-NIVEAUAENDERUNG")
    assert rz06.decision_source == "lb_explizit"
    assert rz06.review_erforderlich is True
    # Die Sicherheitsleuchte an derselben Stelle bleibt Norm-Default.
    assert w.regel("SL-04-NIVEAUAENDERUNG").decision_source == "norm_default"


# ── 5. Achsen-Trennung ──────────────────────────────────────────────────────
@pytest.mark.parametrize("typ", GERAETE)
def test_fuenf_lux_bleiben_vertikal_am_geraet(typ):
    """Der Wert aus §4.1.2 h/i gilt AM GERÄT. `lux_raster` rechnet horizontal am
    Boden — ein Durchreichen wäre derselbe Kategorienfehler wie Ud gegen Uo."""
    (anf,) = PROV.fuer_sonderstelle(typ)
    assert anf.lux.bezugsflaeche == "vertikal_am_geraet"
    assert anf.lux_vertikal_am_geraet == 5.0
    assert anf.lux_horizontal_boden is None
    assert anf.lux_arbeitsflaeche is None


def test_niveauaenderung_erfindet_keinen_lux_wert():
    """c) nennt — anders als h)/i) — kein Beleuchtungsniveau."""
    for anf in PROV.fuer_sonderstelle("niveauaenderung"):
        assert anf.lux is None
        assert anf.lux_horizontal_boden is None


# ── 6. Nachweis: Quelle ersetzt keinen Nachweis ─────────────────────────────
@pytest.mark.parametrize("typ", GERAETE)
def test_offener_vertikalnachweis_ist_markiert(typ):
    (anf,) = PROV.fuer_sonderstelle(typ)
    assert anf.nachweis_offen is True
    assert "vertikal" in anf.nachweis_offen_grund.lower()


# ── 7. Naht + Mechanik ──────────────────────────────────────────────────────
def test_jede_ausgegebene_norm_quelle_liegt_in_regelwerk_quellen():
    alle = [a for t in ERWARTET for a in PROV.fuer_sonderstelle(t)]
    alle += PROV.fuer_raum_attribut("ist_barrierefrei", "WC")
    alle += PROV.fuer_raum_attribut("besondere_gefaehrdung")
    for anf in alle:
        assert anf.quelle in SNAP.quellen


def test_bisherige_quellen_bleiben_erhalten():
    for alt in RAUMREGEL_QUELLEN:
        assert alt in SNAP.quellen


def test_symbol_und_hoehe_werden_geliehen_nicht_erfunden():
    """EN 1838 schreibt für eine hervorzuhebende Stelle kein eigenes Symbol und
    keine eigene Höhe vor — beides kommt aus einer bestehenden Raumregel, die
    Höhe nie unter dem Norm-Floor §4.1.1 (2000 mm)."""
    (anf,) = PROV.fuer_sonderstelle("feuerloescher")
    assert anf.symbol_katalog_keys == PROV.fuer_raum("STIEGENHAUS", True).symbol_katalog_keys
    assert anf.montagehoehe_mm >= 2000


def test_zwei_meter_regel_nur_fuer_punkte():
    """§4.1.2 ANMERKUNG 1: „nicht mehr als 2 m in der Horizontalen"."""
    assert PROV.fuer_sonderstelle("feuerloescher")[0].max_abstand_mm == 2000
    assert PROV.fuer_raum_attribut("ist_barrierefrei", "WC")[0].max_abstand_mm is None


def test_falscher_einstieg_wird_abgewiesen():
    with pytest.raises(KeyError):
        PROV.fuer_sonderstelle("ist_barrierefrei")
    with pytest.raises(KeyError):
        PROV.fuer_raum_attribut("feuerloescher")
    with pytest.raises(KeyError):
        PROV.fuer_sonderstelle("gibt_es_nicht")
