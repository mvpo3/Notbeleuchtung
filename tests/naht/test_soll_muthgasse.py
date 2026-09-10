"""Soll-Tests Muthgasse 109B E2 — 4. erschlossene CAD-Familie (AIA-Layer, ODA-DWG).

Erschlossen 2026-09-07: WALL_PATTERN um ``(?<![A-Z])[AI]-WALL`` erweitert,
Faktor-Kalibrierung über Tür-ARCs aus A-DOOR-Blöcken (virtual_entities — die
Modelspace-ARCs sind Kurvenwände, ×10-Falle), A-AREA-BNDY als Raum-Layer,
'Ker.Bel.' im Belag-Vokabular, A-FLOR/A-CLNG/Q-SPCQ in der Wandkörper-
Negativliste.

Ist-Stand (selbst gemessen, Provider-Parse E2): factor 10.0 · 4 Wand-Layer ·
98/98 Stempel mit Fläche+Typ (85 mit Belag) · 737 Wandkörper · 114 Räume
(seit der Typ-Rückschreibung in der Kaskade ≥ 90 typisiert, vorher 34) ·
291 Türen · 5 stair_exit / 5 final_exit (vor dem Fahnen-Ausschluss 12 / 0)
· 143 Segmente (139 LINIE) · 9 Stiegenhäuser. Bänder knapp unter Ist —
dürfen nur wachsen.

Türzahl-Korrektur 2026-09-10: 308 → **291** Türen. Die 83 Beschriftungs-Fahnen
(``HNP_Beschriftung Türen … Durchgangslichte…``, keine Türgeometrie) fallen aus
``_DOOR_EXCLUDE``; an ihren Stellen entstehen 66 echte ``durchgang``/``text:``-
Türen neu, weil deren Sperrwirkung wegfällt. Gemessen, nicht abgeleitet
(Provider-Parse E2, 825,6 s): 291 Türen, 113 Räume, 205 typisiert = 70,5 %.
Nebenwirkung, gemessen und NICHT geglättet: stair_exit fällt von 12 auf 5 —
5 der 12 stammten aus Fahnen, 3 echte Türen verlieren ihre Typisierung
(``test_soll_stair_exits`` als strict-xfail-Zielbild).
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
    assert len(rm.tueren) >= 280, f"nur {len(rm.tueren)} Türen (Ist 291)"
    assert len(rm.zirkulation.segmente) >= 100, (
        f"nur {len(rm.zirkulation.segmente)} Segmente (Ist 143)"
    )
    assert len(rm.stiegenhaeuser) >= 5, (
        f"nur {len(rm.stiegenhaeuser)} Stiegenhäuser (Ist 9)"
    )


# ── Zielbilder ──────────────────────────────────────────────────────────────

@pytest.mark.xfail(
    strict=True,
    reason="Soll ≥ 9 stair_exit — Ist Muthgasse E2 2026-09-10: 5 (vorher 12). "
    "Gemessen nach dem Fahnen-Ausschluss: 7 Türen tragen stiegenhaustuer/"
    "brandschutztuer (alle 7 mit Stiegenhaus-Seite), 2 davon werden final_exit. "
    "Vorher waren es 15 Kandidaten — 5 davon waren Beschriftungs-Fahnen "
    "(gemessen im Vorher-Dump: 5× tuer_detail='stiegenhaustuer'), also frei "
    "erfundene Ausgänge. Die restlichen 3 verlorenen Kandidaten sind echte "
    "Türen, die ihre Typisierung eingebüßt haben — offener Befund der "
    "Tür-Typisierung, NICHT durch Absenken des Bandes zu heilen.",
)
def test_soll_stair_exits(rm):
    assert sum(1 for a in rm.ausgaenge if a.typ == "stair_exit") >= 9, (
        "stair_exit-Erkennung eingebrochen (Ist 5, vor dem Fahnen-Ausschluss 12)"
    )


def test_soll_raeume_flaechendeckend_typisiert(rm):
    """Erreicht 2026-09-08: die Kaskade schreibt den Stempel-Typ auf L-/H-Räume
    zurück (``kaskade.raeume_aus_kaskade``) — vorher blieb der Typ im Stempel
    stecken und nur 34 der Räume waren typisiert (xfail-Zielbild)."""
    typisiert = sum(1 for r in rm.raeume if r.raum_typ)
    assert typisiert >= 90, f"nur {typisiert} Räume typisiert"


@pytest.mark.xfail(
    strict=True,
    reason="Soll ≥ 90 % typisierte Türen je Familie — Ist Muthgasse E2 "
    "2026-09-10: 70,5 % (205/291; vor dem Fahnen-Ausschluss 218/308 = 70,8 %, "
    "vor der Typ-Rückschreibung 8 %). Rest sind "
    "Türen ohne typisierte Gegenseite; Gründe-Tabelle in bericht.md",
)
def test_soll_90_prozent_tueren_typisiert(rm):
    typ = sum(1 for t in rm.tueren if t.tuer_detail)
    assert rm.tueren and typ / len(rm.tueren) >= 0.9, (
        f"nur {typ}/{len(rm.tueren)} Türen typisiert")


def test_soll_keine_beschriftungsfahnen_als_tueren(plan, rm):
    """Muthgasse trägt 83 INSERTs ``HNP_Beschriftung Türen … Durchgangslichte…``
    (Blockdef = 1× LINE, keine Türgeometrie). Sie standen bis 2026-09-10 als
    Türen im Modell — ``_DOOR_EXCLUDE`` verwirft sie jetzt. Klammer: keine Tür
    sitzt mehr auf einem Fahnen-INSERT-Punkt."""
    fahnen = [plan._scale(e.dxf.insert) for e in plan.entities()
              if e.dxftype() == "INSERT" and "beschrift" in str(e.dxf.name).lower()]
    assert len(fahnen) >= 83, f"nur {len(fahnen)} Fahnen-INSERTs im Plan"
    treffer = [(t.id, t.xy_mm) for t in rm.tueren
               if any(abs(t.xy_mm[0] - f[0]) < 1.0 and abs(t.xy_mm[1] - f[1]) < 1.0
                      for f in fahnen)]
    assert not treffer, f"Beschriftungs-Fahnen wieder als Türen: {treffer}"
