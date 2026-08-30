"""lb_override — LBVorgabe (2. Input) übersteuert die norm-getriebene Platzierung.

CLAUDE.md-Hierarchie: `LB-explizit → Referenz-Praxis → EN-1838/ÖNorm → OVE-Verbote`.
Die Platzierungs-Strategien sind rein norm-getrieben; diese Schicht wendet danach die
expliziten LB-Vorgaben an:

* **Exklusion** (`bereiche_exklusion`) — entfernt Sicherheits-/Antipanik-Leuchten in
  ausgeschlossenen Raumtypen. Kanonischer Fischa-GK4-Fall: „KEINE Sicherheitsbeleuchtung
  in Stiegenhaus/Gängen" kippt den Norm-Default `STIEGENHAUS → sicherheitsleuchte`.
  Rettungszeichen (Fluchtwegkennzeichnung) bleiben bewusst — sie sind nicht
  „Sicherheitsbeleuchtung" i.e.S.
* **Inklusion** (`bereiche_inklusion`) — ERZWINGT eine Sicherheitsleuchte in Raumtypen,
  die die LB verlangt, in denen die Norm aber keine vorsieht (z.B. Lager-/Technikräume
  laut LB). Je qualifiziertem Raum ohne bestehende Aufheller-Leuchte 1 SL am visuellen
  Zentrum. Solche Platzierungen tragen **`lb_quelle`** (keine Norm begründet sie) —
  deshalb bleibt `norm_quelle` leer.

Render-frei. `lb=None` → unveränderte Rückgabe (reines Norm-Verhalten).
"""
from __future__ import annotations

from notbeleuchtung.hauptengine.contracts import (
    LBVorgabe,
    Platzierung,
    RaumModell,
)

from .geometry import find_center_visual, point_in_polygon

_AUFHELLER_ARTEN = {"sicherheitsleuchte", "antipanik"}
# Erzwungene LB-SL: Aufheller-Block, Standard-Montagehöhe, getrennter Sicherheitskreis.
_SL_KEY = "sicherheitsleuchte_aufheller"
_SL_HOEHE_MM = 2400.0
_SV_CIRCUIT = "AGV-A-F13"


def anwenden(
    platzierungen: list[Platzierung], raum: RaumModell, lb: LBVorgabe | None
) -> list[Platzierung]:
    """Wendet die LB-Vorgaben (Exklusion + Inklusion) auf die Platzierungen an."""
    if lb is None:
        return platzierungen
    ergebnis = _exklusion(platzierungen, raum, lb)
    ergebnis = _inklusion(ergebnis, raum, lb)
    return ergebnis


def _exklusion(
    platzierungen: list[Platzierung], raum: RaumModell, lb: LBVorgabe
) -> list[Platzierung]:
    """Entfernt Aufheller-Leuchten in explizit ausgeschlossenen Raumtypen."""
    excl_typen = {
        b.raum_typ.upper() for b in lb.bereiche_exklusion if not b.sicherheitsbeleuchtung
    }
    if not excl_typen:
        return platzierungen
    excl_polys = [
        r.polygon_mm
        for r in raum.raeume
        if r.raum_typ.upper() in excl_typen and len(r.polygon_mm) >= 3
    ]
    if not excl_polys:
        return platzierungen

    def in_ausgeschlossenem_raum(xy: tuple[float, float]) -> bool:
        return any(point_in_polygon(xy, poly) for poly in excl_polys)

    return [
        p
        for p in platzierungen
        if not (p.kind in _AUFHELLER_ARTEN and in_ausgeschlossenem_raum(p.xy_mm))
    ]


def _inklusion(
    platzierungen: list[Platzierung], raum: RaumModell, lb: LBVorgabe
) -> list[Platzierung]:
    """Erzwingt eine SL je LB-eingeschlossenem Raum ohne bestehende Aufheller-Leuchte."""
    incl_typen = {
        b.raum_typ.upper() for b in lb.bereiche_inklusion if b.sicherheitsbeleuchtung
    }
    if not incl_typen:
        return platzierungen
    aufheller = [p for p in platzierungen if p.kind in _AUFHELLER_ARTEN]

    def hat_schon_leuchte(poly: list[tuple[float, float]]) -> bool:
        return any(point_in_polygon(p.xy_mm, poly) for p in aufheller)

    quelle = lb.lb_quelle or "LB bereiche_inklusion"
    zusatz: list[Platzierung] = []
    for r in raum.raeume:
        if r.raum_typ.upper() not in incl_typen or len(r.polygon_mm) < 3:
            continue
        if hat_schon_leuchte(r.polygon_mm):
            continue
        cx, cy = find_center_visual(r.polygon_mm)
        zusatz.append(
            Platzierung(
                xy_mm=(cx, cy),
                catalog_key=_SL_KEY,
                height_mm=_SL_HOEHE_MM,
                kind="sicherheitsleuchte",
                richtung="gerade",
                circuit_hint=_SV_CIRCUIT,
                covers_segment=[],
                norm_quelle="",          # keine Norm begründet sie …
                lb_quelle=quelle,        # … die LB tut es (Provenienz).
            )
        )
    return platzierungen + zusatz
