"""Sonderstellen-Anforderungen — richtige Fundstelle je Typ, Achsen getrennt.

Befund an PR #95: die Platzierung einer Pflicht-Leuchte übernahm die `quelle` der
erstbesten Raumregel derselben Leuchtenart — eine Feuerlöscher-Leuchte trug damit
`§4.1` (STIEGENHAUS), ein Niveauänderungs-RZ `§4.2.1` (GANG). Der Audit-Trail
benannte einen Normsatz, der die Platzierung nicht begründet.

Diese Tests nageln fest, dass der Provider je Auslöser die **eigene** Fundstelle
liefert, dass die Naht-Invariante trägt und dass der vertikale 5-lx-Wert nirgends
als horizontaler Bodenwert auftaucht.

Fundstellen am Original geprüft (`knowledge/EN 1838 - Notbeleuchtung 2019 (1).pdf`,
Kopf „EN 1838:2013 (D)"): §4.1.2 c) Norm-S.8 · h)/i) Norm-S.9 · §4.3.8 Norm-S.11 ·
§4.4.1 Norm-S.12.
"""
import pytest

from notbeleuchtung.normwissen import En1838NormProvider

PROV = En1838NormProvider()
SNAP = PROV.regelwerk_snapshot()

# Auslöser -> erwartete Fundstelle. h) ist die Erste-Hilfe-Stelle, i) sind die
# Brandbekämpfungs- UND Meldeeinrichtungen (Feuerlöscher, Wandhydrant, Melder).
ERWARTET = {
    "feuerloescher": "ÖNORM EN 1838:2013 §4.1.2 i)",
    "hydrant": "ÖNORM EN 1838:2013 §4.1.2 i)",
    "brandmelder": "ÖNORM EN 1838:2013 §4.1.2 i)",
    "erste_hilfe": "ÖNORM EN 1838:2013 §4.1.2 h)",
    "niveauaenderung": "ÖNORM EN 1838:2013 §4.1.2 c)",
}


@pytest.mark.parametrize("typ,quelle", sorted(ERWARTET.items()))
def test_jede_sonderstelle_traegt_ihre_eigene_fundstelle(typ, quelle):
    for anf in PROV.fuer_sonderstelle(typ):
        assert anf.quelle == quelle
        # Genau das war der Fehler: die geliehene Raumregel-Quelle.
        assert anf.quelle not in (
            "ÖNORM EN 1838:2013 §4.1",
            "ÖNORM EN 1838:2013 §4.2.1",
            "ÖNORM EN 1838:2013 §4.3.1",
        )


def test_erste_hilfe_ist_h_und_feuerloescher_ist_i():
    """h) und i) sind zwei verschiedene Buchstaben — am Original geprüft.

    h) „nahe jeder Erste-Hilfe-Stelle … am Erste-Hilfe-Kasten";
    i) „nahe jeder Brandbekämpfungs- und Meldeeinrichtung …".
    """
    assert PROV.fuer_sonderstelle("erste_hilfe")[0].quelle.endswith("§4.1.2 h)")
    for typ in ("feuerloescher", "hydrant", "brandmelder"):
        assert PROV.fuer_sonderstelle(typ)[0].quelle.endswith("§4.1.2 i)")


@pytest.mark.parametrize("attribut,quelle", [
    ("ist_barrierefrei", "ÖNORM EN 1838:2013 §4.3.8"),
    ("besondere_gefaehrdung", "ÖNORM EN 1838:2013 §4.4.1"),
])
def test_raum_attribute_tragen_ihre_eigene_fundstelle(attribut, quelle):
    (anf,) = PROV.fuer_raum_attribut(attribut)
    assert anf.quelle == quelle


def test_niveauaenderung_loest_zwei_leuchten_aus():
    """§4.1.2 c) führt die Niveauänderung als eigenen Punkt neben b) Treppen;
    die Matrix hängt daran SL-04 und RZ-06 — beide mit derselben Fundstelle."""
    anfs = PROV.fuer_sonderstelle("niveauaenderung")
    assert [a.klassifikation for a in anfs] == ["sicherheitsleuchte", "rz"]
    assert {a.quelle for a in anfs} == {"ÖNORM EN 1838:2013 §4.1.2 c)"}


# ── Achsen-Trennung ─────────────────────────────────────────────────────────
@pytest.mark.parametrize("typ", ["feuerloescher", "hydrant", "erste_hilfe", "brandmelder"])
def test_fuenf_lux_bleiben_vertikal_und_werden_nie_horizontal(typ):
    """Der Wert aus §4.1.2 h/i gilt AM GERÄT. `lux_raster` rechnet horizontal am
    Boden — ein Durchreichen wäre derselbe Kategorienfehler wie Ud gegen Uo."""
    (anf,) = PROV.fuer_sonderstelle(typ)
    assert anf.lux_vertikal == 5.0
    assert anf.lux_horizontal is None
    assert anf.lux_vertikal_quelle is not None


def test_niveauaenderung_erfindet_keinen_lux_wert():
    """c) nennt — anders als h)/i) — kein Beleuchtungsniveau."""
    for anf in PROV.fuer_sonderstelle("niveauaenderung"):
        assert anf.lux_vertikal is None
        assert anf.lux_horizontal is None


def test_barrierefrei_leiht_den_horizontalen_wert_von_4_3_1():
    """§4.3.8 fordert Antipanikbeleuchtung ohne eigenen Zahlenwert; das Niveau
    ist das der Antipanikbeleuchtung (§4.3.1: 0,5 lx horizontal). Geliehen,
    nicht erfunden — und ausdrücklich horizontal."""
    (anf,) = PROV.fuer_raum_attribut("ist_barrierefrei")
    assert anf.lux_horizontal == 0.5
    assert anf.lux_horizontal_quelle == "ÖNORM EN 1838:2013 §4.3.1"
    assert anf.lux_vertikal is None


# ── Nachweis: Quelle ersetzt keinen Nachweis ────────────────────────────────
@pytest.mark.parametrize("typ", ["feuerloescher", "hydrant", "erste_hilfe", "brandmelder"])
def test_offener_vertikalnachweis_ist_markiert(typ):
    """Die Leuchte ist Pflicht, der vertikale Nachweis wird heute nicht erbracht.
    Das muss am Ergebnis erkennbar bleiben (Prüfbericht), sonst sieht ein
    unvollständiger Plan „ok" aus."""
    (anf,) = PROV.fuer_sonderstelle(typ)
    assert anf.nachweis_offen is True
    assert "vertikal" in anf.nachweis_offen_grund.lower()


def test_besondere_gefaehrdung_nennt_den_grund_der_offenen_lage():
    """§4.4.1 fordert 10 % der Nennbeleuchtungsstärke, mind. 15 lx — die
    Bezugsgröße existiert im RaumModell nicht, deshalb kein Wert, aber ein
    ausgewiesener offener Nachweis (Contract-Feld `arbeitsplatz_lux` bleibt leer)."""
    (anf,) = PROV.fuer_raum_attribut("besondere_gefaehrdung")
    assert anf.nachweis_offen is True
    assert "15 lx" in anf.nachweis_offen_grund


def test_barrierefrei_hat_keinen_offenen_nachweis():
    """Hier ist der Wert bestimmbar (0,5 lx horizontal) — der Nachweis ist Sache
    des Konsumenten, nicht eine Lücke im Normwissen."""
    (anf,) = PROV.fuer_raum_attribut("ist_barrierefrei")
    assert anf.nachweis_offen is False


# ── Naht + Mechanik ─────────────────────────────────────────────────────────
def test_jede_ausgegebene_quelle_liegt_in_regelwerk_quellen():
    """Naht-Invariante: was der Provider vergibt, muss er auch im Snapshot führen —
    sonst bricht `Platzierung.norm_quelle ∈ NormRegelwerk.quellen`."""
    alle = [a for t in ERWARTET for a in PROV.fuer_sonderstelle(t)]
    alle += [a for at in ("ist_barrierefrei", "besondere_gefaehrdung")
             for a in PROV.fuer_raum_attribut(at)]
    for anf in alle:
        assert anf.quelle in SNAP.quellen


def test_symbol_und_hoehe_werden_geliehen_nicht_erfunden():
    """EN 1838 schreibt für eine hervorzuhebende Stelle kein eigenes Symbol und
    keine eigene Höhe vor — beides kommt aus einer bestehenden Raumregel, die
    Höhe nie unter dem Norm-Floor §4.1.1 (2000 mm)."""
    (anf,) = PROV.fuer_sonderstelle("feuerloescher")
    assert anf.symbol_katalog_keys == PROV.fuer_raum("STIEGENHAUS", True).symbol_katalog_keys
    assert anf.montagehoehe_mm >= 2000
    (rz,) = [a for a in PROV.fuer_sonderstelle("niveauaenderung") if a.klassifikation == "rz"]
    assert rz.symbol_katalog_keys == PROV.fuer_raum("GANG", True).symbol_katalog_keys


def test_zwei_meter_regel_nur_fuer_punkte():
    """§4.1.2 ANMERKUNG 1: „nicht mehr als 2 m in der Horizontalen". Ein
    Raum-Attribut hat keinen Bezugspunkt → kein Abstand."""
    assert PROV.fuer_sonderstelle("feuerloescher")[0].max_abstand_mm == 2000
    assert PROV.fuer_raum_attribut("ist_barrierefrei")[0].max_abstand_mm is None


def test_falscher_einstieg_wird_abgewiesen():
    """Fail closed: kein stiller Default für einen unbekannten oder
    verwechselten Auslöser."""
    with pytest.raises(KeyError):
        PROV.fuer_sonderstelle("ist_barrierefrei")
    with pytest.raises(KeyError):
        PROV.fuer_raum_attribut("feuerloescher")
    with pytest.raises(KeyError):
        PROV.fuer_sonderstelle("gibt_es_nicht")
