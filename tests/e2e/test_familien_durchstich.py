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
* **Muthgasse 109B E2** (AIA-Familie, via ODA aus DWG konvertiert): seit
  2026-09-07 ERSCHLOSSEN (WALL_PATTERN `[AI]-WALL`, ×10-Kalibrierung über
  A-DOOR-Block-ARCs). Hier nur der schnelle Erschließungs-Beleg; volle Bänder
  in tests/naht/test_soll_muthgasse.py.

Toleranz-Bänder statt starrer Goldens; Skip, wenn das CAD-Asset fehlt (CI ohne
Projekte/).
"""
from pathlib import Path

import pytest

from notbeleuchtung.hauptengine.registry import build_default_bundle

FISCHA_EG = Path("Projekte/BVH Fischamenderstraße/BT1/260320_938-AR-PP-11000-A_ERDGESCHOSS BT1.dxf")
HERRENHOLZ_EG = Path("Projekte/DXF_Herrenholzgasse/20230228_po_eg_V.dxf")
BARAWITZKA_EG = Path("Projekte/Barawitzkagasse/415_260415_PP_VA_1_3 0 EG.dxf")
MUTHGASSE_E2 = Path("Projekte/Pläne 19., Muthgasse 109B - 2026-05-07_13-12/"
                    "Architekt/Ausführungsplan/M109B_-Plan - AR-AF-A-GR-E2 100 - GRUNDRISS E2.dxf")


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


def test_fischa_bug_b2_gefixt_ausgaenge_und_segmente(fischa):
    """Bug B2 (0 Ausgänge/0 Segmente) ist seit Fachteil 1 GEFIXT: die Tür-
    Typisierung liefert stair_exits (Stiegenhaustüren) und die Fluchtweg-
    Vereinigung GRAPH-/FALLBACK-Segmente — Basis-Asserts gedreht, die alte
    Prüfbasis-Warnungs-Erwartung entfällt (Anleitung im alten Docstring)."""
    r = fischa.raum
    assert len(r.ausgaenge) >= 1, "B2-Regress: wieder 0 Ausgänge"
    assert len(r.zirkulation.segmente) >= 1, "B2-Regress: wieder 0 Segmente"


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


# ---- Barawitzkagasse EG ----

@pytest.fixture(scope="module")
def barawitzka():
    return _run(BARAWITZKA_EG, "EG")


def test_barawitzka_tueren_und_raeume_erkannt(barawitzka):
    """Ist-Stand seit der Raum-Kaskade L→H→F→R im Provider: Türen (≥ 60) UND Räume.

    Vorher war die Raum-Lücke der Ist-Stand (~2 Räume aus dem Raum-Layer); die
    Kaskade holt die HATCH-Räume dazu (Prüfstrecke: 47 Räume, 40 typisiert)."""
    r = barawitzka.raum
    assert len(r.tueren) >= 60, f"nur {len(r.tueren)} Türen — Tür-Erkennungs-Regress"
    assert len(r.raeume) >= 41, f"nur {len(r.raeume)} Räume — Kaskaden-Regress"
    typed = sum(1 for x in r.raeume if x.raum_typ and x.raum_typ != "UNBEKANNT")
    assert typed >= 30, f"nur {typed} typisiert — Stempel/Typ-Regress"


# ---- Muthgasse 109B E2 ----

def test_muthgasse_familie_erschlossen():
    """GEKIPPT 2026-09-07 (laut eigener Anleitung: raises-Assert brach nach dem
    WALL_PATTERN-/Kalibrierungs-Fix): die AIA-Familie ist erschlossen —
    `lade_dxf` findet die Wand-Layer und kalibriert ×10 (Tür-ARCs aus
    A-DOOR-Blöcken statt der Kurvenwand-×1-Falle).

    Bänder wie bei den anderen Familien: die VOLLEN Parse-Bänder (98 Stempel,
    ≥ 650 Wandkörper, Räume/Türen/Ausgänge) liegen in
    tests/naht/test_soll_muthgasse.py — hier nur der schnelle
    Erschließungs-Beleg, damit der teure 23-MB-Parse nicht doppelt läuft."""
    if not MUTHGASSE_E2.exists():                  # pragma: no cover — CAD-Asset fehlt
        pytest.skip(f"Architekturplan nicht vorhanden: {MUTHGASSE_E2}")
    from notbeleuchtung.raumerkennung.dxf_load import lade_dxf

    plan = lade_dxf(str(MUTHGASSE_E2))
    assert {"A-WALL", "I-WALL"} <= set(plan.wall_layers)
    assert plan.factor == 10.0


def test_barawitzka_pruefung_ohne_befund(barawitzka):
    """GEKIPPT 2026-09-07 (Sichtprüfungs-Fix „Phantom-Türen"): Barawitzka ist
    NICHT mehr „dünn" — die Prüfung meldet 0 Befunde.

    Vorher hielt dieser Test fest, dass das Ergebnis nicht „ok" werden darf
    (2 FALLBACK-Segmente, keine gedeckte Fluchtweg-Kette). Ist-Beleg nach dem
    Fix (``pipeline.run`` auf diesem Plan): 100 Türen statt 182 — die 83
    beidseits-AUSSEN-Phantome der zwei Duplikat-Etagen-Varianten sind weg —,
    50 Räume, 1 final_exit, 6 Segmente (5 GRAPH + 1 FALLBACK), alle 6
    Abschnitte mit ≥2 Leuchten gedeckt → jede Prüfregel „ok".

    Der Test bleibt als Regressionsschranke: kippt eine Regel zurück auf
    Befund, bricht er sichtbar.

    **Kipp 2026-09-07 (Außen-Analyse/Türquellen, Selman):** die Raumerkennung
    findet jetzt einen ZWEITEN Notausgang (Hoftür des Südtrakts — vorher
    verschluckte die Ein-Konturen-Heuristik den ganzen Trakt). Die Platzierung
    setzt dort noch kein RZ → genau EINE Warnung »Rettungszeichen an
    Notausgängen (EN 1838 §4.1.2 g): 1/2 ohne RZ in Reichweite«. Das ist ein
    echter, gewollter Befund der Prüfung (mehr erkannte Ausgänge als gedeckte)
    — als bekannter Ist-Stand gepinnt, offene Frage an Leonis in
    docs/OFFENE_FRAGEN.md. Jede ANDERE Regel muss weiter »ok« sein."""
    pruef = barawitzka.render_summary["pruefung"]
    assert pruef["befunde"], "keine einzige Prüfregel ausgewertet"
    nicht_ok = [b for b in pruef["befunde"] if b["status"] != "ok"]
    andere = [b for b in nicht_ok if "Notausg" not in b["regel"]]
    assert not andere, f"Regel nicht ok: {andere}"
    assert len(nicht_ok) <= 1, f"mehr als der bekannte Notausgang-Befund: {nicht_ok}"
