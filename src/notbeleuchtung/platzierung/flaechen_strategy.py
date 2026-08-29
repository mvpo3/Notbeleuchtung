"""flaechen_strategy — raum-bezogene Notbeleuchtung: Sicherheitsleuchten + Antipanik.

Ergänzt die RZ-Strategie (`communal_stgh_strategy`, Fluchtweg-Segmente) um die
flächigen Leuchten-Arten: Sicherheitsleuchten (Aufheller an Betonungspunkten,
EN 1838 §4.1) und Antipanik-Beleuchtung (offene Flächen, EN 1838 §4.3). Render-frei
— produziert ausschließlich Contract-B `Platzierung`.

Norm-getrieben (CLAUDE.md-Regel): OB ein Raum eine Leuchten-Art braucht, entscheidet
die Norm über `norm.fuer_raum(raum_typ, ist_fluchtweg)` (Fläche/Schwelle liegt in
Enis' Norm-Daten, nicht hier hartcodiert). Leonis entscheidet nur die GEOMETRIE:
1 Leuchte je qualifiziertem Raum am visuellen Zentrum (`find_center_visual` — bleibt
bei L-förmigen Räumen innen). Stromkreis A|B via derselben x-Cluster-Regel wie die RZ.
"""
from __future__ import annotations

from notbeleuchtung.hauptengine.contracts import (
    NormProvider,
    Platzierung,
    RaumModell,
)

from .communal_stgh_strategy import _AGV_SV_F, _building_assigner
from .geometry import find_center_visual


def _plan_raumleuchten(
    raum: RaumModell, norm: NormProvider, klassifikation: str
) -> list[Platzierung]:
    """Je Raum, dessen Norm-Klassifikation `klassifikation` ist, 1 Leuchte am
    visuellen Zentrum. `kind` == `klassifikation` (Kind- und Klassifikation-Literale
    sind deckungsgleich: rz/sicherheitsleuchte/antipanik)."""
    centroids = {
        r.id: find_center_visual(r.polygon_mm) for r in raum.raeume if r.polygon_mm
    }
    assign_building = _building_assigner([cx for cx, _ in centroids.values()])

    out: list[Platzierung] = []
    for r in raum.raeume:
        if r.id not in centroids:
            continue
        anf = norm.fuer_raum(r.raum_typ, r.ist_fluchtweg)
        if anf.klassifikation != klassifikation:
            continue
        cx, cy = centroids[r.id]
        out.append(
            Platzierung(
                xy_mm=(cx, cy),
                catalog_key=anf.symbol_katalog_keys[0],
                rotation_deg=0.0,
                height_mm=float(anf.montagehoehe_mm),
                kind=klassifikation,
                richtung="gerade",
                circuit_hint=f"AGV-{assign_building(cx)}-F{_AGV_SV_F}",
                covers_segment=[],
                norm_quelle=anf.quelle,
            )
        )
    return out


def plan_sicherheitsleuchten(raum: RaumModell, norm: NormProvider) -> list[Platzierung]:
    """Aufheller-Sicherheitsleuchten je Raum mit Norm-Klassifikation 'sicherheitsleuchte'."""
    return _plan_raumleuchten(raum, norm, "sicherheitsleuchte")


def plan_antipanik(raum: RaumModell, norm: NormProvider) -> list[Platzierung]:
    """Antipanik-Leuchten je Raum mit Norm-Klassifikation 'antipanik' (offene Fläche)."""
    return _plan_raumleuchten(raum, norm, "antipanik")
