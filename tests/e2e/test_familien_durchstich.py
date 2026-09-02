"""E2E-Regressionsnetz auf ECHTEN Daten — zweite/dritte CAD-Familie.

Erweitert das Muster von `test_mollgasse_eg_durchstich.py` auf die Familien, die
NICHT Mollgasse-nah sind. Zweck ist NICHT „der Plan ist gut" — er ist es dort noch
nicht — sondern das ehrliche Festhalten des Ist-Stands als Regressionsschranke:

* **Fischamender BT1 EG** (`A_*`-Konvention): Räume + Türen werden voll erkannt,
  aber **0 Ausgänge / 0 Fluchtweg-Segmente** (Provider-Bug B2, docs/COORDINATION.md).
  Die Engine platziert trotzdem Symbole; der Prüfbericht muss das seit Regel 8b als
  „Prüfbasis fehlt"-Warnung ausweisen — NICHT als „ok". Fixt Selman B2, kippen die
  Basis-Asserts hier sichtbar → dann Bänder anheben und Warnung-Erwartung drehen.
* **Herrenholz EG** (ArchiCAD-Konvention, 473 typisierte Räume): die Engine läuft
  durch, platziert aber 0 Symbole → die Plausibilitäts-Regel MUSS „fehler" sagen
  (fail-closed). Verstummt sie je, bricht dieser Test.

Toleranz-Bänder statt starrer Goldens; Skip, wenn das CAD-Asset fehlt (CI ohne
Projekte/).
"""
from pathlib import Path

import pytest

from notbeleuchtung.hauptengine.registry import build_default_bundle

FISCHA_EG = Path("Projekte/BVH Fischamenderstraße/BT1/260320_938-AR-PP-11000-A_ERDGESCHOSS BT1.dxf")
HERRENHOLZ_EG = Path("Projekte/DXF_Herrenholzgasse/20230228_po_eg_V.dxf")


def _run(plan: Path, floor: str):
    if not plan.exists():                          # pragma: no cover — CAD-Asset fehlt
        pytest.skip(f"Architekturplan nicht vorhanden: {plan}")
    from notbeleuchtung.hauptengine.pipeline import run

    return run(build_default_bundle(), str(plan), floor)


@pytest.fixture(scope="module")
def fischa():
    return _run(FISCHA_EG, "EG")


@pytest.fixture(scope="module")
def herrenholz():
    return _run(HERRENHOLZ_EG, "EG")


# ---- Fischamender BT1 EG ----

def test_fischa_raeume_und_tueren_erkannt(fischa):
    """Was heute FUNKTIONIERT, bleibt: Räume voll typisiert + Türen erkannt."""
    r = fischa.raum
    typed = sum(1 for x in r.raeume if x.raum_typ != "UNKNOWN")
    assert len(r.raeume) >= 50, f"nur {len(r.raeume)} Räume — Raum-Layer-Regress"
    assert typed >= 50, f"nur {typed} typisiert — Stempel/Typ-Regress"
    assert len(r.tueren) >= 60, f"nur {len(r.tueren)} Türen — Tür-Erkennungs-Regress"


def test_fischa_platzierung_nicht_leer(fischa):
    """Die Engine liefert auf der A_*-Familie ein nicht-leeres Ergebnis."""
    plzg = fischa.platzierung.platzierungen
    assert len(plzg) >= 10, f"nur {len(plzg)} Symbole — Fischamender-Regress"
    assert any(p.kind == "rz" for p in plzg)


def test_fischa_bug_b2_als_pruefbasis_warnung_ausgewiesen(fischa):
    """Bug B2 (0 Ausgänge/0 Segmente) darf NICHT als „ok" durchgehen (Regel 8b).

    Wenn dieser Test bricht, weil Ausgänge/Segmente erkannt werden: B2 ist gefixt —
    Basis-Asserts drehen, Bänder anheben, Warnung-Erwartung entfernen."""
    r = fischa.raum
    assert len(r.ausgaenge) == 0, "B2 gefixt? → Test-Erwartungen aktualisieren"
    assert len(r.zirkulation.segmente) == 0, "B2 gefixt? → Test-Erwartungen aktualisieren"
    pruef = fischa.render_summary["pruefung"]
    basis = [b for b in pruef["befunde"] if "Prüfbasis" in b["regel"]]
    assert len(basis) == 2, f"Prüfbasis-Warnungen fehlen: {[b['regel'] for b in pruef['befunde']]}"
    assert pruef["status"] != "ok", "0 Ausgänge/0 Segmente darf nicht als ok gelten"


# ---- Herrenholz EG ----

def test_herrenholz_engine_laeuft_durch(herrenholz):
    """Kein Crash auf der ArchiCAD-Familie; Raum-Erkennung liefert massiv Räume."""
    r = herrenholz.raum
    assert len(r.raeume) >= 300, f"nur {len(r.raeume)} Räume — Raum-Layer-Regress"


def test_herrenholz_leeres_ergebnis_ist_fehler(herrenholz):
    """0 Symbole auf 473 Räumen → Plausibilitäts-Regel MUSS fail-closed melden."""
    pruef = herrenholz.render_summary["pruefung"]
    if herrenholz.platzierung.platzierungen:
        pytest.skip("Herrenholz platziert inzwischen Symbole — Erwartung aktualisieren")
    assert pruef["status"] == "fehler", "leerer Plan bestand die Prüfung als nicht-fehler"
    assert any("Plausibilität" in b["regel"] for b in pruef["befunde"])
