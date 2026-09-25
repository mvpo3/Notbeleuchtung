"""Befund B5: § 6g verlangt den unbestimmten Raum magenta — in ALLEN drei
Darstellungen, nicht nur in ``raumerkennung_darstellung``.

Umgesetzt war es dort; ``gesamtdarstellung`` zeichnete ihn als ``gang_allg``
bzw. ``stiege`` und ``plan_pruefen`` fiel in den neutralen else-Zweig (weiß).
Beide Bilder behaupteten damit eine Entscheidung, die keine Regel getroffen
hat. ``raumerkennung_darstellung`` prüft
``test_raumerkennung_darstellung.py::test_kategorie_unbestimmter_gang_ist_magenta``.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib
from shapely.geometry import box

matplotlib.use("Agg")

from notbeleuchtung.hauptengine.contracts.raum_modell import Raum

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts" / "analyse"))
sys.path.insert(0, str(REPO / "scripts"))
import gesamtdarstellung as gd  # noqa: I001
import plan_pruefen as pp

MAGENTA = "#ff00ff"


def _raum(rid, typ, klasse):
    return Raum(id=rid, raum_typ=typ, nutzungsklasse=klasse,
                polygon_mm=list(box(0, 0, 4000, 3000).exterior.coords)[:-1])


def test_gesamtdarstellung_faerbt_den_unbestimmten_raum_eigen():
    assert gd._kategorie(_raum("g", "GANG", None)) == "unbestimmt"
    assert gd._kategorie(_raum("v", "VORRAUM", None)) == "unbestimmt"
    assert gd._KAT["unbestimmt"][1] == MAGENTA
    # Gegenprobe: die entschiedenen Klassen bleiben, wo sie waren.
    assert gd._kategorie(_raum("g", "GANG", "ALLGEMEIN_ERSCHLIESSUNG")) == "gang_allg"
    assert gd._kategorie(_raum("g", "GANG", "WOHNUNG_PRIVAT")) == "gang_priv"
    assert gd._kategorie(_raum("v", "VORRAUM", "ALLGEMEIN_ERSCHLIESSUNG")) == "stiege"
    # Ein Raum ohne raum_typ bleibt „unbekannt" — das ist etwas anderes.
    assert gd._kategorie(_raum("x", "", None)) == "unbekannt"


def test_plan_pruefen_zeichnet_den_unbestimmten_raum_magenta():
    stil = {k: pp._raumflaeche_stil(_raum("g", "GANG", k))
            for k in (None, "ALLGEMEIN_ERSCHLIESSUNG", "WOHNUNG_PRIVAT",
                      "KEIN_RAUM")}
    assert stil[None]["fc"] == MAGENTA
    assert stil[None] != stil["ALLGEMEIN_ERSCHLIESSUNG"]
    assert stil[None] != stil["WOHNUNG_PRIVAT"]
    # Ein untypisierter Raum ohne Klasse bleibt neutral — unbestimmt meint
    # ausdrücklich nur GANG/VORRAUM.
    assert pp._raumflaeche_stil(_raum("x", "ZIMMER", None)) == \
        stil["ALLGEMEIN_ERSCHLIESSUNG"]


def test_plan_pruefen_bericht_nennt_die_unbestimmten_raeume_mit_grund():
    """Reviewer-Befund Runde 4 (Linse Naht): § 6g Punkt 3 verlangt den
    unbestimmten Raum „mit Grund, im Bericht aufgelistet". Der Grund stand nur
    im Provider-Attribut ``wohnungsklasse_warnungen``; das Bild zeigte
    magenta, aber kein Ausgabeprodukt sagte warum. Jetzt schreibt
    ``plan_pruefen`` einen eigenen Block in bericht.md — die Durchleitungen
    (dieselbe Liste) daneben."""
    import inspect
    from types import SimpleNamespace

    zeilen = pp._kreuzcheck_md(
        SimpleNamespace(tueren=[]), None, [], None,
        [("unbestimmt: raum_9 — Ankerregel nicht auswertbar: vom Stiegenhaus "
          "über keine Tür erreichbar"),
         "durchleitung: seg_graph_tuer_1 führt durch den privaten Raum raum_2"])
    assert "### Unbestimmte Räume (§ 6g)" in zeilen
    block = zeilen[zeilen.index("### Unbestimmte Räume (§ 6g)"):]
    assert any("raum_9" in z and "Ankerregel nicht auswertbar" in z for z in block)
    assert any("durchleitung: seg_graph_tuer_1" in z for z in zeilen)
    # … und der Aufrufer reicht die Provider-Liste wirklich durch.
    assert "wohnungsklasse_warnungen" in inspect.getsource(pp._fachteil3)


def test_plan_pruefen_bericht_nennt_den_messfall_loch():
    """Runde 8 (E5 Satz 2): ein vom Stiegenhaus über keine Tür erreichbarer
    Raum kann jetzt ALLGEMEIN sein statt unbestimmt — der Messfall S4c/S3b
    darf damit nicht aus dem Bericht verschwinden."""
    from types import SimpleNamespace

    zeilen = pp._kreuzcheck_md(
        SimpleNamespace(tueren=[]), None, [], None,
        [("loch: raum_10 — vom Stiegenhaus über keine Tür erreichbar — Tür- oder "
          "Raumerkennungsloch (Messfall S4c/S3b); Klasse allgemein")])
    kopf = next(z for z in zeilen if z.startswith("### ") and "S4c/S3b" in z)
    block = zeilen[zeilen.index(kopf):]
    assert any("raum_10" in z and "über keine Tür" in z for z in block)


def test_plan_pruefen_bericht_nennt_den_tiebreak():
    """Owner-Grundsatz 2026-09-22 (G2): wo der Fixpunkt-Tiebreak entschieden
    hat (ankerprivater Raum bleibt allgemein), steht eine Zeile mit Grund im
    Bericht."""
    from types import SimpleNamespace

    zeilen = pp._kreuzcheck_md(
        SimpleNamespace(tueren=[]), None, [], None,
        [("tiebreak: raum_57 — Ankerregel privat (…), Klasse allgemein: kein voll "
          "ankerbestätigter Fixpunkt (…) — bei mehreren Fixpunkten gilt der "
          "allgemeine (Board 4), Notlicht bleibt")])
    kopf = next(z for z in zeilen if z.startswith("### ") and "Tiebreak" in z)
    assert any("raum_57" in z for z in zeilen[zeilen.index(kopf):])
