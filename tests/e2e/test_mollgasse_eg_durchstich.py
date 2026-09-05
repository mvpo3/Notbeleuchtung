"""E2E-Regressionsschranke auf ECHTEN Daten — Mollgasse EG.

Der Durchstich `pipeline.run` auf `Projekte/Mollgasse/Erdgeschoß.dxf` ist die einzige
Stelle, an der die Platzierung auf realer Geometrie läuft. Die Unit-Fixtures (dünnes
4OG-Fake, 5 Symbole) haben in der Vergangenheit mehrere Real-Plan-Bugs verdeckt
(covers_segment leer, C2-Doppelpfeil, Belegungs-Overflow) — sie waren grün, weil das
Fake die betroffenen Pfade nicht ausübt. Dieser Test schließt die Lücke: er hält das
reale Ergebnis als Regressionsschranke fest.

Kern-Zusicherung: die Platzierung ist auf Mollgasse EG kollisionsfrei — `validierung`-
Regel „Keine Symbol-Kollision" ist **ok** und kein Symbol-Paar liegt unter 250 mm. Das
war 2026-08-31 noch nicht so (Befund #5: 1 Paar < 250 mm, `docs/DOD_SICHTPRUEFUNG.md`);
inzwischen aufgelöst, und der Abstands-Nachpass (`abstand_nachpass`) hält es strukturell
invariant. Dieser Test ist das Regressionsnetz gegen eine Wiederkehr.

Die Symbolzahlen sind als **Toleranz-Bänder** formuliert (kein starres Golden): verbessert
sich die Raumerkennung, dürfen sie wandern; ein Einbruch auf quasi-leer bricht den Test.

Skip, wenn das CAD-Asset fehlt (CI ohne Projekte/) — wie `test_ground_truth_mollgasse`.
"""
from pathlib import Path

import pytest

from notbeleuchtung.hauptengine.registry import build_default_bundle
from notbeleuchtung.hauptengine.validierung import pruefe

PLAN = Path("Projekte/Mollgasse/Erdgeschoß.dxf")


@pytest.fixture(scope="module")
def durchstich():
    if not PLAN.exists():                          # pragma: no cover — CAD-Asset fehlt
        pytest.skip(f"Architekturplan nicht vorhanden: {PLAN}")
    from notbeleuchtung.hauptengine.pipeline import run

    return run(build_default_bundle(), str(PLAN), "EG")


def _befund(befunde, teil: str):
    treffer = [b for b in befunde if teil in b.regel]
    assert treffer, f"kein Befund mit »{teil}« — vorhanden: {[b.regel for b in befunde]}"
    return treffer[0]


def test_keine_symbol_kollision_nach_entzerrung(durchstich):
    """Der eigentliche Beweis: der Abstands-Nachpass räumt die Naht-Kollision weg."""
    befunde = pruefe(durchstich.raum, durchstich.platzierung)
    kollision = _befund(befunde, "Kollision")
    assert kollision.status == "ok", kollision.detail


def test_symbolzahl_in_erwarteter_groessenordnung(durchstich):
    """Toleranz-Band statt starrem Golden (Referenz DOD: ~15 RZ + ~21 SL).

    ⚠️ **Band-Obergrenze für SL am 05.09.2026 von 28 auf 40 angehoben** (Enis,
    Änderung in @mvpo3s Lane — bitte mit reviewen). Ursache ist kein Regress,
    sondern eine Korrektur: der Lux-Nachweis rechnete jede Leuchte in ihrer
    **C0-Ebene**, weil `photometrie_i_cd_fn` den C-Parameter auf 0 ließ. Für die
    Fluchtweg-Default-Leuchte (Corridor-Optik) ist C0 die stärkste Richtung
    (γ=60°: 149,93 cd gegen 19,53 cd in C90) — die Deckung war dadurch zu
    optimistisch. Ohne zugesicherte Optik-Ausrichtung wird jetzt konservativ mit
    der kleinsten Lichtstärke über alle C-Ebenen gerechnet; Mollgasse EG braucht
    damit **36 statt 28 SL**. Kommt die Ausrichtung als zugesicherte Eingabe,
    ist die Zahl neu zu bewerten.
    """
    plzg = durchstich.platzierung.platzierungen
    rz = sum(1 for p in plzg if p.kind == "rz")
    sl = sum(1 for p in plzg if p.kind == "sicherheitsleuchte")
    assert 10 <= rz <= 22, f"RZ={rz} außerhalb des erwarteten Bandes"
    assert 15 <= sl <= 40, f"SL={sl} außerhalb des erwarteten Bandes"
    assert len(plzg) >= 30, f"nur {len(plzg)} Symbole — quasi-leer, Real-Plan-Regress"


def test_alle_symbolabstaende_mindestens_250mm(durchstich):
    """Direkter geometrischer Nachweis, unabhängig von der Validierungs-Formulierung."""
    import math
    plzg = durchstich.platzierung.platzierungen
    zu_nah = [
        (plzg[i].kind, plzg[j].kind)
        for i in range(len(plzg))
        for j in range(i + 1, len(plzg))
        if math.hypot(plzg[i].xy_mm[0] - plzg[j].xy_mm[0],
                      plzg[i].xy_mm[1] - plzg[j].xy_mm[1]) < 250.0
    ]
    assert not zu_nah, f"{len(zu_nah)} Paar(e) < 250 mm: {zu_nah[:5]}"
