"""Soll-Tests Barawitzka EG — final_exit + brandschutztuer seit Fachteil 1
SCHARF; Rest Zielbild (xfail strict).

WICHTIGER PLAN-BEFUND (Analyse 2026-09, s. docs/OFFENE_FRAGEN.md): die 16
Farbe-96-Linien sind KATASTERGRENZEN (Layer »Kataster Grenzen«), KEINE
Fluchtweg-Linien; Farbe 30 = Wand-/Bau-Layer. Explizite FLW-Linien existieren
in diesem Plan NICHT — die Erwartung »≥16 Segmente quelle LINIE« ist mit
diesem Plan nicht erfüllbar. Der Test bleibt trotzdem als xfail stehen: die
Quelle »explizite Fluchtweg-Linie« wird generisch gebaut (Layer-Muster
FLW/09-WEG + materialien.yaml-Semantik FLUCHTWEG; Farbe 96 nur, wenn der
Layer nicht Kataster/Grenze/verm enthält) und greift auf anderen Plänen.
Brandschutz real: Layer »0._EG PP_2_970 Brandschutz« + 6 Texte
»Glaswand EI30 + A2« → Kandidaten für brandschutztuer.
"""
from pathlib import Path

import pytest

PLAN = Path("Projekte/_eingang/Barawitzka_EG.dxf")


@pytest.fixture(scope="module")
def provider():
    if not PLAN.exists():                        # pragma: no cover — CAD-Asset fehlt
        pytest.skip(f"Architekturplan nicht vorhanden: {PLAN}")
    from notbeleuchtung.raumerkennung import ArchitekturRaumProvider

    return ArchitekturRaumProvider()


@pytest.fixture(scope="module")
def rm(provider):
    return provider.parse(str(PLAN), "EG")


def test_soll_final_exit(rm):
    """Scharf seit Fachteil 1: hauseingang-Typisierung → final_exit im EG."""
    assert any(a.typ == "final_exit" for a in rm.ausgaenge), "kein final_exit"


def test_soll_zwei_final_exit(rm):
    """Scharf seit der Außen-Analyse je Gebäude-Komponente (2 Trakte + Hof):
    Hof-/Gartentüren des Südtrakts werden AUSSEN-seitig erkannt → ≥ 2
    Endausgänge (Ist 2026-09-07: 2)."""
    final = [a for a in rm.ausgaenge if a.typ == "final_exit"]
    assert len(final) >= 2, f"nur {len(final)} final_exit"


@pytest.mark.xfail(
    strict=True,
    reason="Plan hat KEINE expliziten Fluchtweg-Linien: die 16 Farbe-96-Linien "
    "sind KATASTERGRENZEN (Layer »Kataster Grenzen«, Analyse 2026-09, "
    "docs/OFFENE_FRAGEN.md) — die alte »≥16 Segmente LINIE«-Erwartung ist "
    "damit widerlegt und auf »explizite Linien vorhanden« umformuliert. Der "
    "xfail bleibt als Zielbild für einen Plan-Nachtrag des Fachplaners stehen; "
    "die LINIE-Quelle selbst ist generisch gebaut und greift auf anderen "
    "Plänen (Mollgasse 103, Muthgasse 139).",
)
def test_soll_explizite_linien_vorhanden(rm):
    linie = [s for s in rm.zirkulation.segmente if s.quelle == "LINIE"]
    assert linie, "keine Segmente mit quelle LINIE (explizite Fluchtweg-Linien)"


@pytest.mark.xfail(
    strict=True,
    reason="Soll ≥ 90 % typisierte Türen je Familie — Ist Barawitzka 2026-09-07: "
    "53 % (Haupt-Lücke: unbekannte_kombination/kein_nachbarraum, s. "
    "untypisiert_grund-Tabelle in bericht.md)",
)
def test_soll_90_prozent_tueren_typisiert(rm):
    typ = sum(1 for t in rm.tueren if t.tuer_detail)
    assert rm.tueren and typ / len(rm.tueren) >= 0.9, (
        f"nur {typ}/{len(rm.tueren)} Türen typisiert")


def test_soll_brandschutztuer(rm):
    """Scharf seit Fachteil 1: EI30-Texte in 500 mm → brandschutztuer."""
    bst = [t for t in rm.tueren if t.tuer_detail == "brandschutztuer"]
    assert len(bst) >= 1, "keine Brandschutztür erkannt"


def test_soll_41_raeume_mit_stempel(rm):
    """Scharf seit Fachteil 2: LIFT-Erkennung + Gang-/Geometrie-Typisierung
    heben die typisierten Räume über die Soll-Schwelle 41 (XPASS-Kipp)."""
    typisiert = [r for r in rm.raeume if r.raum_typ]
    assert len(typisiert) >= 41, f"nur {len(typisiert)} Räume mit Stempel typisiert"


@pytest.mark.xfail(
    strict=True,
    reason="Soll (Spec 6): alle 16 FLW-Endpunkte an der Außenkante sind mit "
    "final_exit gedeckt — Ist 2026-09-07 (selbst gemessen): 0 Segmente quelle "
    "LINIE, damit 0 Endpunkte an der Außenkante und 0 gedeckte (2 final_exit "
    "existieren, decken aber keinen Linien-Endpunkt). Ursache: die 16 "
    "Farbe-96-Linien sind Katastergrenzen, echte FLW-Linien fehlen im Plan "
    "(s. test_soll_explizite_linien_vorhanden).",
)
def test_soll_16_endpunkte_an_der_aussenkante_gedeckt(provider, rm):
    kc = provider.letzter_kreuzcheck
    assert len(kc.endpunkte_aussenkante) == 16, (
        f"{len(kc.endpunkte_aussenkante)} statt 16 FLW-Endpunkte an der "
        "Außenkante")
    assert len(kc.gedeckte_endpunkte) == len(kc.endpunkte_aussenkante), (
        f"nur {len(kc.gedeckte_endpunkte)}/{len(kc.endpunkte_aussenkante)} "
        "Endpunkte mit final_exit gedeckt")
