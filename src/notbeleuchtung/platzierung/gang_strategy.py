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

from .bausteine import (
    AGV_SV_F as _AGV_SV_F,
)
from .bausteine import KORRIDOR_TYPEN as _KORRIDOR_TYPEN
from .bausteine import (
    building_assigner as _building_assigner,
)
from .bausteine import (
    richtung_und_rotation as _richtung_und_rotation,
)
from .bausteine import (
    select_key as _select_key,
)
from .geometry import _bbox
from .mittellinie import leuchten_auf_linie

# RZ-Abstand, wenn die Norm keine Erkennungsweite liefert (defensiver Default).
_DEFAULT_RZ_ABSTAND_MM = 15000.0


def _abstand_mm(erkennungsweite_m: float | None) -> float:
    """RZ-Abstand aus der Norm-Erkennungsweite (l = z·h) in mm; sonst Default."""
    if erkennungsweite_m and erkennungsweite_m > 0:
        return erkennungsweite_m * 1000.0
    return _DEFAULT_RZ_ABSTAND_MM


def _ziel_tuer(r, raum: RaumModell):
    """Flucht-Ziel-Tür des Gangs: Notausgang > Tür zum STIEGENHAUS > sonst None.

    Owner-Regel #111 verallgemeinert auf den Fallback: auch ohne erkannte
    Ausgänge/Segmente hat ein Gang meist eine Tür, „durch die man flieht" —
    sie gibt die Pfeilrichtung vor (Baufeld 5OG: alle RZ standen stur auf 0°,
    weil die Regel nur im Anker-Pfad lebte).
    """
    typen = {x.id: (x.raum_typ or "").upper() for x in raum.raeume}
    kandidaten = [
        t for t in raum.tueren if r.id in (t.von_raum, t.nach_raum)
    ]
    if not kandidaten:
        return None
    for t in kandidaten:
        if t.ist_notausgang:
            return t
    for t in kandidaten:
        anderer = t.nach_raum if t.von_raum == r.id else t.von_raum
        if typen.get(anderer or "") == "STIEGENHAUS":
            return t
    return None


def _order_zum_ziel(pts: list[tuple[float, float]], raum: RaumModell, ziel_xy):
    """Achsenpunkte so ordnen, dass das letzte Element am Flucht-Ziel liegt
    (Ausgang oder Ziel-Tür). Ohne Ziel: unverändert (deterministisch)."""
    ziele = [a.xy_mm for a in raum.ausgaenge]
    if ziel_xy is not None:
        ziele.append(ziel_xy)
    if len(pts) < 2 or not ziele:
        return pts

    def d(a, b):
        return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5

    d_erst = min(d(pts[0], z) for z in ziele)
    d_letzt = min(d(pts[-1], z) for z in ziele)
    # Näher am Ziel = Ziel-Ende → soll pts[-1] sein.
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
        ziel = _ziel_tuer(r, raum)
        ziel_xy = ziel.xy_mm if ziel is not None else None
        pts = _order_zum_ziel(
            leuchten_auf_linie(r.polygon_mm, _abstand_mm(anf.erkennungsweite_m)),
            raum, ziel_xy,
        )
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
            # Owner-Regel #111 (Pfeil-zur-Tür), Fallback-Ausprägung: das RZ am
            # Ziel-Ende zeigt mit dem UNTEN-Block physisch ZUR Ziel-Tür —
            # unrotiert weist der Block auf −y → rotation = Winkel(RZ→Tür)+90°,
            # auf 90° gerastert (wie im Anker-Pfad).
            if ziel_xy is not None and i == len(pts) - 1:
                import math as _math
                dx, dy = ziel_xy[0] - px, ziel_xy[1] - py
                if _math.hypot(dx, dy) > 50.0:
                    unten_key, _ = _select_key(anf.symbol_katalog_keys, "unten")
                    catalog_key = unten_key
                    rotation = (round((_math.degrees(_math.atan2(dy, dx)) + 90.0) / 90.0) * 90.0) % 360.0
                    mirror_x = False
                    richtung = "unten"
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
