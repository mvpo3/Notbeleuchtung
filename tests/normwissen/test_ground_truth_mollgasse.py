"""Ground Truth — greifen die Matrix-Regeln an einem ECHTEN Grundriss?

Prüft `ground_truth/mollgasse_eg.yaml` gegen den realen Plan
`Projekte/Mollgasse/Erdgeschoß.dxf`. Die Fälle beschreiben die **Auslöser-Lage**
des Gebäudes (wie viele Ausgänge, Kreuzungen, Richtungswechsel es gibt), nicht ein
Soll-Ergebnis: einen professionell gezeichneten Mollgasse-Notbeleuchtungsplan gibt
es im Repo nicht (siehe Kopf der YAML).

Die Assertions sind **Untergrenzen**. Verbessert Selman die Raumerkennung, dürfen
die Zahlen steigen, ohne diesen Test zu brechen — fällt sie zurück, bricht er.
Genau die Fälle, die heute NICHT greifen (`status: input_fehlt_*`), sind als
solche festgehalten: sie sind der Arbeitsvorrat, kein Fehler dieser Matrix.

Der Test importiert `raumerkennung`, weil Ground Truth nur an echter Geometrie
existiert. Er liegt in `tests/`, nicht im `normwissen`-Package — die Owner-Grenze
zwischen den Packages bleibt unberührt.
"""
from pathlib import Path

import pytest
import yaml

from notbeleuchtung.normwissen import PlatzierungsRegelwerk

PLAN = Path("Projekte/Mollgasse/Erdgeschoß.dxf")
GT = Path(__file__).parent / "ground_truth" / "mollgasse_eg.yaml"


@pytest.fixture(scope="module")
def gt() -> dict:
    return yaml.safe_load(GT.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def raum():
    if not PLAN.exists():                      # pragma: no cover — CAD-Asset fehlt
        pytest.skip(f"Architekturplan nicht vorhanden: {PLAN}")
    from notbeleuchtung.raumerkennung import ArchitekturRaumProvider

    return ArchitekturRaumProvider().parse(str(PLAN), "EG")


def _grade(raum) -> dict[str, int]:
    grade: dict[str, int] = {}
    for e in raum.zirkulation.edges:
        grade[e.from_] = grade.get(e.from_, 0) + 1
        grade[e.to] = grade.get(e.to, 0) + 1
    return grade


# ── Auslöser, die auf dem echten Plan wirklich vorkommen ────────────────────
def test_gt01_ausgaenge_ins_freie_loesen_rettungszeichen_aus(raum, gt):
    fall = _fall(gt, "GT-MOLL-EG-01")
    final_exits = [a for a in raum.ausgaenge if a.typ == "final_exit"]
    assert len(final_exits) >= fall["mindestens"]


def test_gt02_notausgangstueren_loesen_rettungszeichen_aus(raum, gt):
    fall = _fall(gt, "GT-MOLL-EG-02")
    assert sum(1 for t in raum.tueren if t.ist_notausgang) >= fall["mindestens"]


def test_gt03_kreuzungen_loesen_rettungszeichen_aus(raum, gt):
    fall = _fall(gt, "GT-MOLL-EG-03")
    kreuzungen = sum(1 for g in _grade(raum).values() if g >= 3)
    assert kreuzungen >= fall["mindestens"]


def test_gt04_richtungswechsel_sind_kandidaten_kein_stueckzahlziel(raum, gt):
    """81 Knickpunkte heißen nicht 81 Leuchten — RZ-09 und die Ausgangs-Priorität
    dünnen aus. Der Test hält nur fest, dass der Kandidatenvorrat existiert."""
    fall = _fall(gt, "GT-MOLL-EG-04")
    wechsel = sum(1 for s in raum.zirkulation.segmente
                  if s.reason in ("direction_change", "corner"))
    assert wechsel >= fall["mindestens"]
    assert "kein Stückzahl-Ziel" in fall["erwartung"]


# ── Die dokumentierten Lücken — als Lücke festgehalten, nicht als Erfolg ────
def test_gt05_stiegenhaus_ausgaenge_fehlen_auf_dem_echten_plan(raum, gt):
    """Zwei STIEGENHAUS-Räume, aber kein einziger `stair_exit`. Deshalb stehen
    RZ-05 und RZ-07 in der Matrix auf `teilweise` statt `unterstuetzt`."""
    fall = _fall(gt, "GT-MOLL-EG-05")
    assert fall["status"] == "input_fehlt_auf_echtem_plan"
    stiegenhaeuser = [r for r in raum.raeume if r.raum_typ == "STIEGENHAUS"]
    assert stiegenhaeuser, "das EG hat Stiegenhäuser"
    # Kein Assert auf 0: verbessert sich F2, ist das ein Fortschritt, kein Bruch.
    if not [a for a in raum.ausgaenge if a.typ == "stair_exit"]:
        w = PlatzierungsRegelwerk()
        assert w.regel("RZ-05-TREPPE").engine_status == "teilweise"
        assert w.regel("RZ-07-AUSGANG-STIEGENHAUS").engine_status == "teilweise"


def test_gt06_brandschutz_und_erste_hilfe_stellen_sind_contract_luecke(raum, gt):
    """EN 1838 §4.1.2 fordert die Betonung von Feuerlöschern, Wandhydranten,
    Erste-Hilfe-Stellen und Meldeeinrichtungen. Das `RaumModell` führt keines
    dieser Merkmale — vier belegte Pflichtstellen sind heute nicht planbar."""
    fall = _fall(gt, "GT-MOLL-EG-06")
    assert fall["status"] == "input_fehlt_im_contract"
    felder = set(type(raum).model_fields)
    assert not (felder & {"feuerloescher", "hydranten", "erste_hilfe", "melder"})
    blockiert = {r.id for r in PlatzierungsRegelwerk().blockiert_durch_contract()}
    assert set(fall["regel"]) <= blockiert


def test_gt07_leeres_geschoss_ist_ein_review_fall(gt):
    """1OG/1KG typisieren fast nichts und liefern 0 Fluchtweg-Segmente. Ein Plan
    daraus wäre geraten — RZ-11 macht daraus einen Review statt einer Platzierung."""
    fall = _fall(gt, "GT-MOLL-EG-07")
    assert fall["status"] == "review_fall"
    regel = PlatzierungsRegelwerk().regel("RZ-11-FLUCHTWEG-UNKLAR")
    assert regel.review_erforderlich and regel.leuchtenart == "keine"


# ── Die Fixture beschreibt, was sie ist ─────────────────────────────────────
def test_ground_truth_beansprucht_keine_normwirkung(gt):
    """Ground Truth ist Referenz, kein Normersatz (CLAUDE.md). Die Datei muss das
    selbst sagen — sonst wird sie irgendwann als Quelle zitiert."""
    assert "übersteuert keine Norm" in GT.read_text(encoding="utf-8")
    assert gt["meta"]["gemessen_mit"].endswith("ArchitekturRaumProvider")


def test_jeder_fall_nennt_eine_matrix_regel(gt):
    w = PlatzierungsRegelwerk()
    for fall in gt["faelle"]:
        regeln = fall["regel"] if isinstance(fall["regel"], list) else [fall["regel"]]
        for rid in regeln:
            w.regel(rid)      # wirft KeyError, wenn die ID nicht existiert


def _fall(gt: dict, fall_id: str) -> dict:
    for f in gt["faelle"]:
        if f["id"] == fall_id:
            return f
    raise AssertionError(f"Ground-Truth-Fall fehlt: {fall_id}")
