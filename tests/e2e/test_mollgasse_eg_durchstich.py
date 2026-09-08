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
    der kleinsten Lichtstärke über alle C-Ebenen gerechnet.

    Das Verfahren ermittelt unter diesen konservativen Annahmen **36 SL** (vorher
    28). Eine minimale Leuchtenzahl oder eine optimierte Anordnung ist damit
    **nicht** nachgewiesen — und das erweiterte Anzahl-Band ist für sich genommen
    **kein Beleg für ausreichende Beleuchtung**: es prüft eine Größenordnung, nicht
    die Norm-Erfüllung. Der lichttechnische Nachweis bleibt offen, solange die
    physische Optik-Ausrichtung kein zugesicherter Input ist (Regel „Lichttechnischer
    Nachweis: Photometrie-Grundlage" im Prüfbericht).

    **Nachtrag 06.09.2026 (optik_aus_achse, Leonis):** die Ausrichtung IST jetzt
    Input — der Verdichter leitet je Fluchtweg-SL den Korridor-Achsen-Azimut ab,
    rechnet die C-Ebene relativ dazu und vermerkt den Azimut als Montage-Rotation
    am Symbol. Ergebnis richtungsRICHTIG statt Minimum: **32 SL**, Prüfstatus
    wieder `ok` (Regel 15 vollständig). Das Band 15..40 deckt alle drei Stände
    (28 C0-optimistisch · 32 richtungsrichtig · 36 konservativ).
    """
    plzg = durchstich.platzierung.platzierungen
    rz = sum(1 for p in plzg if p.kind == "rz")
    sl = sum(1 for p in plzg if p.kind == "sicherheitsleuchte")
    # Zwei additive Ursachen, beide Seiten des Merges 2026-09-08:
    # (1) Selman, Außen-Analyse/Türquellen: das EG hat begründete final_exits
    #     (Hof-/Gartentüren, Durchfahrten — jede Tür trägt `quelle`) statt 5
    #     → mehr Ausgangs- und Richtungs-RZ.
    # (2) Owner-Korrektur der Türleuchten-Regel: TECHNIK/MUELLRAUM/KINDERWAGENRAUM
    #     tragen an der Tür ein RETTUNGSZEICHEN (Pfeil zur Tür) statt einer
    #     Sicherheitsleuchte — Mollgasse EG hat 6 solche Räume; die B1-Regel
    #     (#135, `aufheller_je_rz`) setzt hinter JEDES RZ einen Aufheller, also
    #     wächst SL mit.
    # Am gemergten Stand nachgemessen (2026-09-08): RZ 26, SL 34 — die beiden
    # Ursachen addieren sich NICHT, weil (2) auf Mollgasse noch nicht greift:
    # `KINDERWAGENRAUM` fällt in `raumerkennung/raumtyp.py` auf `ABSTELLRAUM`
    # zusammen (Board-Befund Leonis → Selman, offen). Bänder bleiben deshalb die
    # weiteren der beiden Seiten; greift die Türleuchten-Regel später wirklich,
    # wandert RZ nach oben und SL mit (`aufheller_je_rz`).
    assert 10 <= rz <= 30, f"RZ={rz} außerhalb des erwarteten Bandes"
    assert 15 <= sl <= 44, f"SL={sl} außerhalb des erwarteten Bandes"
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
