"""Soll-Tests Muthgasse 109B E2 — 4. erschlossene CAD-Familie (AIA-Layer, ODA-DWG).

Erschlossen 2026-09-07: WALL_PATTERN um ``(?<![A-Z])[AI]-WALL`` erweitert,
Faktor-Kalibrierung über Tür-ARCs aus A-DOOR-Blöcken (virtual_entities — die
Modelspace-ARCs sind Kurvenwände, ×10-Falle), A-AREA-BNDY als Raum-Layer,
'Ker.Bel.' im Belag-Vokabular, A-FLOR/A-CLNG/Q-SPCQ in der Wandkörper-
Negativliste.

Ist-Stand (selbst gemessen, Provider-Parse E2): factor 10.0 · 4 Wand-Layer ·
98/98 Stempel mit Fläche+Typ (85 mit Belag) · 737 Wandkörper · 114 Räume
(davon nur 34 typisiert — Stempel↔Raum-Zuordnung ist die offene Lücke) ·
272 Türen · 12 stair_exit / 0 final_exit (E2 = unterstes Geschoss im Ordner)
· 143 Segmente (139 LINIE) · 9 Stiegenhäuser. Bänder knapp unter Ist —
dürfen nur wachsen.
"""
from pathlib import Path

import pytest

PLAN = Path("Projekte/_eingang/Muthgasse_E2.dxf")


def _skip_ohne_plan():
    if not PLAN.exists():                        # pragma: no cover — CAD-Asset fehlt
        pytest.skip(f"Architekturplan nicht vorhanden: {PLAN}")


@pytest.fixture(scope="module")
def plan():
    _skip_ohne_plan()
    from notbeleuchtung.raumerkennung.dxf_load import lade_dxf

    return lade_dxf(str(PLAN))


@pytest.fixture(scope="module")
def rm(plan):
    from notbeleuchtung.raumerkennung import ArchitekturRaumProvider

    return ArchitekturRaumProvider().parse(str(PLAN), "E2")


# ── scharf: Erschließung der Familie ────────────────────────────────────────

def test_soll_faktor_kalibrierung_x10(plan):
    """Kalibrierungs-Falle: Kurvenwand-ARCs (600–1300 Quell-Einheiten) dürfen den
    Faktor nicht auf ×1 ziehen — Tür-Bögen aus A-DOOR-Blöcken entscheiden."""
    assert plan.factor == 10.0, f"Faktor {plan.factor} statt 10.0 (×10-Falle)"


def test_soll_wand_layer_erkannt(plan):
    assert {"A-WALL", "I-WALL"} <= set(plan.wall_layers), (
        f"AIA-Wand-Layer fehlen: {sorted(plan.wall_layers)}"
    )


def test_soll_98_stempel_mit_flaeche_und_typ(plan):
    from notbeleuchtung.raumerkennung.stempel_anker import finde_stempel

    st = finde_stempel(plan)
    assert len(st) >= 98, f"nur {len(st)} Stempel (Ist 98)"
    assert sum(1 for s in st if s.flaeche_m2) >= 98, "Stempel ohne Fläche"
    assert sum(1 for s in st if s.typ) >= 98, "Stempel ohne Typ"
    assert sum(1 for s in st if s.belag) >= 80, "Belag-Spur ('Ker.Bel.') eingebrochen"


def test_soll_wandkoerper_band(plan):
    from notbeleuchtung.raumerkennung.wandkoerper import finde_wandkoerper

    wk = finde_wandkoerper(plan)
    assert len(wk) >= 650, f"nur {len(wk)} Wandkörper (Ist 737)"


def test_soll_raeume_tueren_ausgaenge(rm):
    assert len(rm.raeume) >= 98, f"nur {len(rm.raeume)} Räume (Ist 114)"
    assert len(rm.tueren) >= 250, f"nur {len(rm.tueren)} Türen (Ist 272)"
    assert sum(1 for a in rm.ausgaenge if a.typ == "stair_exit") >= 9, (
        "stair_exit-Erkennung eingebrochen (Ist 12)"
    )
    assert len(rm.zirkulation.segmente) >= 100, (
        f"nur {len(rm.zirkulation.segmente)} Segmente (Ist 143)"
    )
    assert len(rm.stiegenhaeuser) >= 5, (
        f"nur {len(rm.stiegenhaeuser)} Stiegenhäuser (Ist 9)"
    )


# ── Zielbild (xfail strict) ─────────────────────────────────────────────────

@pytest.mark.xfail(
    strict=True,
    reason="Stempel↔Raum-Zuordnung: 98 Stempel tragen Typ, aber nur 34 der 114 "
    "Räume sind typisiert — die A-AREA-BNDY-Polygone matchen die Stempel noch "
    "nicht flächendeckend (Soll: ≥ 90 typisierte Räume)",
)
def test_soll_raeume_flaechendeckend_typisiert(rm):
    typisiert = sum(1 for r in rm.raeume if r.raum_typ)
    assert typisiert >= 90, f"nur {typisiert} Räume typisiert"
