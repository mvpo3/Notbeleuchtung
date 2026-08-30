"""gang_strategy — RZ-Fallback entlang GANG-Mittellinien ohne Fluchtweg-Layer.

Liefert Selman/F2 **keine** Fluchtweg-Segmente UND hat der Zirkulationsgraph **keine**
Kreuzung (fremde CAD-Familie: der `A_Fluchtweg`-/`09-WEG`-Layer wurde nicht erkannt,
fischamender-Bug B2), dann produzieren weder `anker_strategy` noch
`communal_stgh_strategy` ein Rettungszeichen — die Engine setzt gar kein RZ.

Diese Fallback-Schicht routet Rettungszeichen entlang der **Mittelachse** jedes
GANG-/Flur-/Korridor-Raums (`mittellinie.leuchten_auf_linie`), damit die Engine auch
auf ungesehenen Plänen RZ setzt. Der Abstand ist norm-getrieben (RZ-Erkennungsweite
l = z·h — keine Überproduktion); die Pfeilrichtung zeigt zum nächsten Ausgang, sonst
entlang der dominanten Korridor-Achse. Render-frei, kein Contract berührt.

Nur Fallback: die Segment-/Anker-Strategien bleiben Default, wo ein echter
Fluchtweg-Layer vorliegt (siehe `platzierer._plan_rettungszeichen`).
"""
from __future__ import annotations

from notbeleuchtung.hauptengine.contracts import NormProvider, Platzierung, RaumModell

from .communal_stgh_strategy import (
    _AGV_SV_F,
    _building_assigner,
    _richtung_und_rotation,
    _select_key,
)
from .deckung import _KORRIDOR_TYPEN
from .geometry import _bbox
from .mittellinie import leuchten_auf_linie

# RZ-Abstand, wenn die Norm keine Erkennungsweite liefert (defensiver Default).
_DEFAULT_RZ_ABSTAND_MM = 15000.0


def _abstand_mm(erkennungsweite_m: float | None) -> float:
    """RZ-Abstand aus der Norm-Erkennungsweite (l = z·h) in mm; sonst Default."""
    if erkennungsweite_m and erkennungsweite_m > 0:
        return erkennungsweite_m * 1000.0
    return _DEFAULT_RZ_ABSTAND_MM


def _order_zum_ausgang(pts: list[tuple[float, float]], raum: RaumModell):
    """Achsenpunkte so ordnen, dass das letzte Element am Ausgang-Ende liegt.

    Ohne Ausgang: unverändert (deterministisch, dominante x-Achse)."""
    if len(pts) < 2 or not raum.ausgaenge:
        return pts

    def d(a, b):
        return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5

    d_erst = min(d(pts[0], a.xy_mm) for a in raum.ausgaenge)
    d_letzt = min(d(pts[-1], a.xy_mm) for a in raum.ausgaenge)
    # Näher am Ausgang = Ziel-Ende → soll pts[-1] sein.
    return list(reversed(pts)) if d_erst < d_letzt else pts


def plan_rettungszeichen_gang(raum: RaumModell, norm: NormProvider) -> list[Platzierung]:
    """RZ entlang der Mittelachse jedes GANG-Raums, Pfeil zum Ausgang-Ende."""
    korridore = [
        r for r in raum.raeume
        if r.raum_typ.upper() in _KORRIDOR_TYPEN and len(r.polygon_mm) >= 3
    ]
    if not korridore:
        return []
    assign_building = _building_assigner(
        [(_bbox(r.polygon_mm)[0] + _bbox(r.polygon_mm)[2]) / 2 for r in korridore]
    )

    out: list[Platzierung] = []
    for r in korridore:
        anf = norm.fuer_raum(r.raum_typ, r.ist_fluchtweg)
        pts = _order_zum_ausgang(leuchten_auf_linie(r.polygon_mm, _abstand_mm(anf.erkennungsweite_m)), raum)
        if not pts:
            continue
        cx = (_bbox(r.polygon_mm)[0] + _bbox(r.polygon_mm)[2]) / 2
        building = assign_building(cx)
        for i, (px, py) in enumerate(pts):
            # Pfeil zeigt zum nächsten Achsenpunkt Richtung Ausgang-Ende (pts[-1]);
            # am Ausgang-Ende selbst die Richtung des letzten Schenkels beibehalten.
            if len(pts) == 1:
                # Einzel-RZ: zum nächsten Ausgang, sonst „unten" (Ausgang erreicht).
                naechster = min(raum.ausgaenge, key=lambda a: (a.xy_mm[0] - px) ** 2 + (a.xy_mm[1] - py) ** 2,
                                default=None) if raum.ausgaenge else None
                if naechster is not None:
                    richtung, fallback_rot = _richtung_und_rotation(naechster.xy_mm[0] - px, naechster.xy_mm[1] - py)
                else:
                    richtung, fallback_rot = "unten", 270.0
            elif i + 1 < len(pts):
                richtung, fallback_rot = _richtung_und_rotation(pts[i + 1][0] - px, pts[i + 1][1] - py)
            else:
                richtung, fallback_rot = _richtung_und_rotation(px - pts[i - 1][0], py - pts[i - 1][1])
            catalog_key, is_directional = _select_key(anf.symbol_katalog_keys, richtung)
            rotation = 0.0 if is_directional else fallback_rot
            mirror_x = False if is_directional else (richtung == "rechts")
            out.append(
                Platzierung(
                    xy_mm=(px, py),
                    catalog_key=catalog_key,
                    rotation_deg=rotation,
                    mirror_x=mirror_x,
                    height_mm=float(anf.montagehoehe_mm),
                    kind="rz",
                    richtung=richtung,
                    circuit_hint=f"AGV-{building}-F{_AGV_SV_F}",
                    covers_segment=[],
                    norm_quelle=anf.quelle,
                )
            )
    return out
