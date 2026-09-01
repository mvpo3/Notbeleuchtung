"""deckung — Lux-getriebene Verdichtung der Fluchtweg-Beleuchtung (Schicht „Deckung").

Schließt den Fahrplan Anker → Linie → Fläche → **Deckung**: statt Leuchten zu raten,
verdichtet diese Schicht die Fluchtweg-Sicherheitsleuchten entlang der Mittelachse
(`mittellinie.leuchten_auf_linie`), bis der EN-1838-Lux-Nachweis (`lux.lux_raster`)
erfüllt ist (≥ 1 lx, Ud ≥ 1:40). Der Abstand wird halbiert, bis das Kriterium hält
oder der Mindestabstand erreicht ist.

Norm-getrieben: OB ein Raum Fluchtweg-Beleuchtung braucht + Montagehöhe/Katalog-Key
kommen aus `norm.fuer_raum`. Feuert nur auf Korridor-Räumen (GANG/FLUR/KORRIDOR) mit
Polygon — Stiegenhäuser/Wohnräume bleiben unberührt. Render-frei, kein Contract berührt.
"""
from __future__ import annotations

from collections.abc import Callable

from notbeleuchtung.hauptengine.contracts import NormProvider, Platzierung, RaumModell

from .communal_stgh_strategy import _AGV_SV_F, _building_assigner
from .geometry import _bbox
from .lux import LuxErgebnis, lux_raster
from .mittellinie import leuchten_auf_linie

_KORRIDOR_TYPEN = {"GANG", "FLUR", "KORRIDOR"}
_SL_KEY = "sicherheitsleuchte_aufheller"   # bis die Norm einen Fluchtweg-SL-Key liefert
_MAX_HALBIERUNGEN = 3
_START_ABSTAND_MM = 8000.0
_MIN_ABSTAND_MM = 4000.0   # Fluchtweg-SL realistisch ≥ 4 m Abstand (nicht 1,5 m)


def verdichte_fluchtweg(
    raum: RaumModell, norm: NormProvider, *,
    i_cd: float = 200.0,
    i_cd_fn: Callable[[float], float] | None = None,
) -> list[Platzierung]:
    """Sicherheitsleuchten entlang jeder Korridor-Mittellinie, verdichtet bis 1 lx / Ud≥1:40.

    `i_cd` = konstante Lichtstärke-Annahme; `i_cd_fn(γ)` = richtungsabhängige Hersteller-
    Photometrie (EULUMDAT/LDT, überschreibt `i_cd`), von der Hauptengine injiziert.
    """
    korridore = [
        r for r in raum.raeume if r.raum_typ.upper() in _KORRIDOR_TYPEN and len(r.polygon_mm) >= 3
    ]
    if not korridore:
        return []
    assign_building = _building_assigner(
        [(_bbox(r.polygon_mm)[0] + _bbox(r.polygon_mm)[2]) / 2 for r in korridore]
    )

    out: list[Platzierung] = []
    for r in korridore:
        anf = norm.fuer_raum(r.raum_typ, r.ist_fluchtweg)
        bounds = _bbox(r.polygon_mm)
        h_m = anf.montagehoehe_mm / 1000.0
        abstand = _START_ABSTAND_MM
        kandidaten = leuchten_auf_linie(r.polygon_mm, abstand)
        for _ in range(_MAX_HALBIERUNGEN):
            res = lux_raster(
                kandidaten, bounds, montagehoehe_m=h_m, i_cd=i_cd, i_cd_fn=i_cd_fn,
                ziel_lux=anf.min_lux,
            )
            if res.erfuellt_min and res.erfuellt_ud:
                break
            abstand = max(_MIN_ABSTAND_MM, abstand / 1.5)
            kandidaten = leuchten_auf_linie(r.polygon_mm, abstand)
        cx = (bounds[0] + bounds[2]) / 2
        building = assign_building(cx)
        for px, py in kandidaten:
            out.append(
                Platzierung(
                    xy_mm=(px, py),
                    catalog_key=_SL_KEY,
                    rotation_deg=0.0,
                    height_mm=float(anf.montagehoehe_mm),
                    kind="sicherheitsleuchte",
                    richtung="gerade",
                    circuit_hint=f"AGV-{building}-F{_AGV_SV_F}",
                    covers_segment=[],
                    norm_quelle=anf.quelle,
                )
            )
    return out


def lux_bericht(
    raum: RaumModell, ergebnis, *,
    i_cd: float = 200.0,
    i_cd_fn: Callable[[float], float] | None = None,
) -> dict[str, LuxErgebnis]:
    """Je Korridor-Raum: Lux-Bewertung der darin liegenden Sicherheitsleuchten.

    Reporting/Audit — verändert nichts. Schlüssel = Raum-ID. `i_cd_fn` wie in
    `verdichte_fluchtweg` (Hersteller-Photometrie statt konstant `i_cd`).
    """
    from .geometry import point_in_polygon

    bericht: dict[str, LuxErgebnis] = {}
    sl = [p for p in ergebnis.platzierungen if p.kind == "sicherheitsleuchte"]
    for r in raum.raeume:
        if r.raum_typ.upper() not in _KORRIDOR_TYPEN or len(r.polygon_mm) < 3:
            continue
        drin = [p.xy_mm for p in sl if point_in_polygon(p.xy_mm, r.polygon_mm)]
        bericht[r.id] = lux_raster(
            drin, _bbox(r.polygon_mm), i_cd=i_cd, i_cd_fn=i_cd_fn, ziel_lux=1.0
        )
    return bericht
