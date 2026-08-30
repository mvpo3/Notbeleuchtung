"""lb_override — LBVorgabe (2. Input) übersteuert die norm-getriebene Platzierung.

CLAUDE.md-Hierarchie: `LB-explizit → Referenz-Praxis → EN-1838/ÖNorm → OVE-Verbote`.
Die Platzierungs-Strategien sind rein norm-getrieben; diese Schicht wendet danach die
expliziten LB-Vorgaben an — allen voran `bereiche_exklusion` (der kanonische Fischa-
GK4-Fall: „KEINE Sicherheitsbeleuchtung in Stiegenhaus/Gängen" kippt den Norm-Default
`STIEGENHAUS → sicherheitsleuchte`).

Render-frei, kein Contract berührt. `lb=None` → unveränderte Rückgabe (reines Norm-
Verhalten).

**Umfang v1 (Exklusion):** entfernt Sicherheits-/Antipanik-Leuchten in explizit
ausgeschlossenen Raumtypen. Rettungszeichen (Fluchtwegkennzeichnung) bleiben bewusst
erhalten — sie sind nicht „Sicherheitsbeleuchtung" i.e.S. `bereiche_inklusion`
(SL erzwingen, wo die Norm keine fordert) folgt in einem eigenen Slice.
"""
from __future__ import annotations

from notbeleuchtung.hauptengine.contracts import (
    LBVorgabe,
    Platzierung,
    RaumModell,
)

from .geometry import point_in_polygon

_AUFHELLER_ARTEN = {"sicherheitsleuchte", "antipanik"}


def anwenden(
    platzierungen: list[Platzierung], raum: RaumModell, lb: LBVorgabe | None
) -> list[Platzierung]:
    """Wendet die LB-Exklusionen auf die norm-getriebenen Platzierungen an."""
    if lb is None:
        return platzierungen
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
