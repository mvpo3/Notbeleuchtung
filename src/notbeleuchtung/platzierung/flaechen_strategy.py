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
from .geometry import _bbox, find_center_visual, grid_points
from .lux import lux_raster, ud_min_aus_norm

# Sicherung gegen Überproduktion, falls der Lux-Nachweis nie hält (defekte Geometrie).
_ANTIPANIK_MAX_LEUCHTEN = 25
_ANTIPANIK_MAX_RUNDEN = 6

# WC/Sanitär-Raumtypen für den flächenbasierten Antipanik-Trigger (EN 1838 §4.3).
_WC_TYPEN = {"WC", "SANITAER", "SANITÄR", "BAD", "DUSCHE", "NASSRAUM"}


def _antipanik_referenz(norm: NormProvider):
    """Repräsentative Antipanik-Anforderung aus dem Norm-Regelwerk (0,5 lx, Symbol, Quelle).

    Wird gebraucht, wenn ein Raum NICHT über seinen Typ, sondern über die Fläche
    antipanik-pflichtig wird: die Antipanik-Parameter kommen dann aus Enis' eigener
    Antipanik-Regel (Leonis fabriziert keine Norm-Werte). `None`, falls das Regelwerk
    keine Antipanik-Regel kennt → dann wird nicht flächen-getriggert.
    """
    for regel in norm.regelwerk_snapshot().regeln:
        if regel.anforderung.klassifikation == "antipanik" and regel.anforderung.symbol_katalog_keys:
            return regel.anforderung
    return None


def _ist_flaechen_antipanik(raum_typ: str, flaeche_m2: float, schwellen) -> bool:
    """Löst die Fläche eine Antipanik-Pflicht aus? Beide Schwellen `None` → nie (inert)."""
    ap = schwellen.antipanik_min_m2
    wc = schwellen.wc_sanitaer_min_m2
    if ap is not None and flaeche_m2 >= ap:
        return True
    return wc is not None and raum_typ.upper() in _WC_TYPEN and flaeche_m2 >= wc


def _antipanik_punkte(polygon: list, anf) -> list:
    """Antipanik-Raster, verdichtet bis der EN-1838-Nachweis (`anf.min_lux`, i.d.R.
    0,5 lx / Ud≥1:40) erfüllt ist — nicht nur `mindest_anzahl` blind gesetzt.

    Startet beim Norm-Raster (`mindest_anzahl`) und erhöht die Punktzahl, solange der
    Nachweis fehlt. Ist die Fläche kleiner als das EN-Nachweisfenster (Randstreifen),
    gibt es kein Raster → dann bleibt es beim Norm-Raster (nicht beweisbar, nicht raten).
    """
    n = max(1, anf.mindest_anzahl)
    bounds = _bbox(polygon)
    h_m = anf.montagehoehe_mm / 1000.0
    ud_min = ud_min_aus_norm(anf.gleichmaessigkeit_max)
    pts = grid_points(polygon, n)
    for _ in range(_ANTIPANIK_MAX_RUNDEN):
        res = lux_raster(pts, bounds, montagehoehe_m=h_m, ziel_lux=anf.min_lux, ud_min=ud_min)
        if res.max_lux == 0.0:                       # kein Nachweisfenster (Fläche < Rand)
            return grid_points(polygon, max(1, anf.mindest_anzahl))
        if res.erfuellt_min and res.erfuellt_ud:
            break
        if len(pts) >= _ANTIPANIK_MAX_LEUCHTEN:
            break
        n = max(n + 1, int(n * 1.6))
        pts = grid_points(polygon, n)
    return pts


def _plan_raumleuchten(
    raum: RaumModell, norm: NormProvider, klassifikation: str
) -> list[Platzierung]:
    """Je Raum mit passender Norm-Klassifikation Leuchten, geometrisch über die Fläche
    verteilt (`grid_points`): Sicherheitsleuchte → `mindest_anzahl` (Aufheller-Betonung);
    Antipanik → verdichtet bis zum EN-1838-Lux-Nachweis (`_antipanik_punkte`, §4.3).
    `kind` == `klassifikation` (Literale deckungsgleich: rz/sicherheitsleuchte/antipanik).
    Alle Leuchten eines Raums teilen dessen Stromkreis-Bauteil (A|B aus Zentroid-x)."""
    centroids = {
        r.id: find_center_visual(r.polygon_mm) for r in raum.raeume if r.polygon_mm
    }
    assign_building = _building_assigner([cx for cx, _ in centroids.values()])

    # Flächen-Trigger (EN 1838 §4.3) nur im Antipanik-Durchlauf: große offene Flächen /
    # WC über der Norm-Schwelle werden antipanik-pflichtig, auch ohne Typ-Klassifikation.
    schwellen = norm.regelwerk_snapshot().flaechen_schwellen
    ap_referenz = _antipanik_referenz(norm) if klassifikation == "antipanik" else None

    out: list[Platzierung] = []
    for r in raum.raeume:
        if r.id not in centroids:
            continue
        anf = norm.fuer_raum(r.raum_typ, r.ist_fluchtweg)
        eff = anf
        if anf.klassifikation != klassifikation:
            # Zusatz-Trigger: darf nur ADDIEREN (Antipanik über Fläche), nie überschreiben.
            if (
                ap_referenz is not None
                and _ist_flaechen_antipanik(r.raum_typ, r.flaeche_m2, schwellen)
            ):
                eff = ap_referenz
            else:
                continue
        building = assign_building(centroids[r.id][0])
        punkte = (
            _antipanik_punkte(r.polygon_mm, eff)
            if klassifikation == "antipanik"
            else grid_points(r.polygon_mm, max(1, eff.mindest_anzahl))
        )
        for px, py in punkte:
            out.append(
                Platzierung(
                    xy_mm=(px, py),
                    catalog_key=eff.symbol_katalog_keys[0],
                    rotation_deg=0.0,
                    height_mm=float(eff.montagehoehe_mm),
                    kind=klassifikation,
                    richtung="gerade",
                    circuit_hint=f"AGV-{building}-F{_AGV_SV_F}",
                    covers_segment=[],
                    norm_quelle=eff.quelle,
                )
            )
    return out


def plan_sicherheitsleuchten(raum: RaumModell, norm: NormProvider) -> list[Platzierung]:
    """Aufheller-Sicherheitsleuchten je Raum mit Norm-Klassifikation 'sicherheitsleuchte'."""
    return _plan_raumleuchten(raum, norm, "sicherheitsleuchte")


def plan_antipanik(raum: RaumModell, norm: NormProvider) -> list[Platzierung]:
    """Antipanik-Leuchten je Raum mit Norm-Klassifikation 'antipanik' (offene Fläche)."""
    return _plan_raumleuchten(raum, norm, "antipanik")
