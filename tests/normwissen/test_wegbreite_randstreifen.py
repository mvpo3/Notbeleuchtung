"""§4.2.1 Wegbreite/Mittelbereich und §4.3.1 Randstreifen — Geltungsbereiche.

Am Original geprüft: `knowledge/EN 1838 - Notbeleuchtung 2019 (1).pdf`, Kopfzeile
„EN 1838:2013 (D)". §4.2.1 Norm-S.9, §4.3.1 Norm-S.11, Anhang B Norm-S.16–17.

Die drei Größen werden bewusst getrennt gehalten:

* **Mittellinie** (§4.2.1 Satz 1) — 1 lx, gebunden an eine Breite **bis zu 2 m**.
* **Mittelbereich** (§4.2.1 Satz 2) — mindestens die halbe Wegbreite, mindestens
  50 % des Wertes.
* **Randstreifen** (§4.3.1) — 0,5 m, gehört zur **Antipanik**beleuchtung und hat
  mit dem Rettungsweg-Nachweis nichts zu tun.
"""
import pytest

from notbeleuchtung.normwissen import En1838NormProvider

PROV = En1838NormProvider()


# ── §4.2.1: Geltungsbereich der Mittellinien-Regel ──────────────────────────
@pytest.mark.parametrize("breite", [500.0, 1200.0, 2000.0])
def test_bis_zwei_meter_gilt_der_mittellinien_nachweis(breite):
    w = PROV.weg_nachweis(breite)
    assert w.regime == "mittellinie"
    assert w.mittellinie_lux == 1.0            # Wert kommt aus lux.rettungsweg
    assert w.review_erforderlich is False


@pytest.mark.parametrize("breite", [2000.1, 3000.0, 6000.0])
def test_ueber_zwei_meter_ist_planer_entscheidung(breite):
    """Satz 3 ist eine KANN-Aussage mit zwei Wegen — die Engine wählt keinen."""
    w = PROV.weg_nachweis(breite)
    assert w.regime == "breiter_weg"
    assert set(w.optionen) == {"streifen_2m", "antipanik"}
    assert w.review_erforderlich is True
    assert w.mittellinie_lux is None           # für diese Breite gibt §4.2.1 nichts her


def test_ohne_breite_kein_default():
    """Fail closed: eine geratene Wegbreite wäre ein erfundener Geltungsbereich."""
    w = PROV.weg_nachweis(None)
    assert w.regime == "unbestimmbar"
    assert w.review_erforderlich is True
    assert w.mittellinie_lux is None and w.mittelbereich_breite_mm is None
    assert "Breite" in w.grund


def test_grenze_ist_die_norm_grenze_nicht_geraten():
    assert PROV.weg_nachweis(1000.0).max_breite_mm == 2000


# ── §4.2.1 Satz 2: Mittelbereich ────────────────────────────────────────────
@pytest.mark.parametrize("breite,band_mm", [(2000.0, 1000.0), (1200.0, 600.0)])
def test_mittelbereich_ist_die_halbe_wegbreite(breite, band_mm):
    w = PROV.weg_nachweis(breite)
    assert w.mittelbereich_breite_mm == band_mm


def test_mittelbereich_lux_sind_fuenfzig_prozent_des_mittellinienwerts():
    w = PROV.weg_nachweis(2000.0)
    assert w.mittelbereich_lux == w.mittellinie_lux * 0.5 == 0.5


def test_keine_doppelte_zahlenpflege():
    """Der Mittelbereich rechnet auf `lux.rettungsweg` — er führt keinen zweiten
    Absolutwert. Ändert sich der Grundwert, wandert der Bandwert mit."""
    from notbeleuchtung.normwissen.provider import En1838NormProvider as P

    prov = P()
    grund = prov.regelwerk_snapshot().regeln
    rettungsweg_lux = {r.anforderung.min_lux for r in grund if r.raum_typ == "GANG"}
    assert prov.weg_nachweis(2000.0).mittellinie_lux in rettungsweg_lux


# ── §4.3.1: Randstreifen gehört zur Antipanik ───────────────────────────────
def test_randstreifen_ist_antipanik_nicht_rettungsweg():
    assert PROV.antipanik_randstreifen_mm() == 500.0
    assert PROV.antipanik_randstreifen_quelle().endswith("§4.3.1")


def test_rettungsweg_nachweis_kennt_keinen_randstreifen():
    """§4.2.1 nennt Mittellinie und Mittelbereich — keinen Randstreifen. Die
    Verwechslung stand als Docstring in `platzierung/lux.py::lux_raster`."""
    w = PROV.weg_nachweis(2000.0)
    assert not hasattr(w, "randstreifen_mm")
    assert w.quelle.endswith("§4.2.1")


# ── Anhang B ────────────────────────────────────────────────────────────────
def test_keine_oesterreichische_a_abweichung():
    """Anhang B führt FR, IT, DE, NL — für Österreich gibt es keine Abweichung;
    die deutschen 15 s (§4.2.6/§4.3.6) gelten hier ausdrücklich nicht."""
    assert PROV.hat_at_abweichung() is False
