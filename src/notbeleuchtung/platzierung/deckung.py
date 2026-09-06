"""deckung — Lux-getriebene Verdichtung der Fluchtweg-Beleuchtung (Schicht „Deckung").

Schließt den Fahrplan Anker → Linie → Fläche → **Deckung**: Fluchtweg-SL entlang der
Mittelachse (`mittellinie.leuchten_auf_linie`), Abstand **photometrisch hergeleitet**
(`lux.max_leuchtenabstand_mm` aus der Hersteller-LDT) und gegen den **norm-korrekten
Nachweis** verifiziert: EN 1838 §4.2.1 fordert ≥ 1 lx auf der MITTELLINIE des
Rettungswegs + ≥ 0,5 lx im halben Mittenband (± Breite/4) + Ud ≥ 1:40 — NICHT
flächig bis in jede Raum-Ecke. Der frühere bbox-Raster-Nachweis war strenger als
die Norm und erzwang ~5-m-Abstände (Faktor 2–3 Überproduktion gegenüber
Herstellerangaben: Schrack IL-Flur > 24 m, din SL5 ~16–21 m — siehe
knowledge/extracted/PRODUKTE_SCHRACK_DIN.md). Erfüllt der photometrische
Start-Abstand den Nachweis nicht, wird verdichtet (÷1.3) bis er hält oder der
Mindestabstand erreicht ist.

Norm-getrieben: OB ein Raum Fluchtweg-Beleuchtung braucht + Montagehöhe/Katalog-Key
kommen aus `norm.fuer_raum`. Feuert nur auf Korridor-Räumen (GANG/FLUR/KORRIDOR) mit
Polygon — Stiegenhäuser/Wohnräume bleiben unberührt. Render-frei, kein Contract berührt.
"""
from __future__ import annotations

from collections.abc import Callable

from notbeleuchtung.hauptengine.contracts import NormProvider, Platzierung, RaumModell

from .communal_stgh_strategy import _AGV_SV_F, _building_assigner
from .geometry import _bbox
from .lux import (
    LuxErgebnis,
    lux_punkte,
    lux_raster,
    max_leuchtenabstand_mm,
    ud_min_aus_norm,
)
from .mittellinie import leuchten_auf_linie_mit_richtung, mittellinie

_KORRIDOR_TYPEN = {"GANG", "FLUR", "KORRIDOR"}
_SL_KEY = "sicherheitsleuchte_aufheller"   # bis die Norm einen Fluchtweg-SL-Key liefert
_MAX_VERDICHTUNGEN = 6
_VERDICHTUNGS_FAKTOR = 1.3
_MIN_ABSTAND_MM = 4000.0   # Fluchtweg-SL realistisch ≥ 4 m Abstand (nicht 1,5 m)
_MAX_ABSTAND_MM = 30000.0  # Sanity-Cap (Hersteller-Maximum Hochdecken-Optik ~35 m)
_NACHWEIS_RASTER_MM = 250.0


def _nachweis_punkte(linie: list, breite_mm: float) -> tuple[list, list]:
    """(Mittellinien-Punkte, Mittenband-Punkte ± Breite/4) für den §4.2.1-Nachweis.

    Band-Offsets folgen der lokalen Tangente (Nachbarpunkte) — deckt auch L-förmige
    Korridore. §4.2.1: Mittellinie ≥ 1 lx, halbes Mittenband ≥ 0,5 lx.
    """
    if len(linie) < 2:
        return linie, []
    off = breite_mm / 4.0
    band = []
    for i, (x, y) in enumerate(linie):
        x2, y2 = linie[min(i + 1, len(linie) - 1)]
        x1, y1 = linie[max(i - 1, 0)]
        tx, ty = x2 - x1, y2 - y1
        n = (tx * tx + ty * ty) ** 0.5
        if n < 1e-9:
            continue
        nx, ny = -ty / n, tx / n
        band.append((x + nx * off, y + ny * off))
        band.append((x - nx * off, y - ny * off))
    return linie, band


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
        ud_min = ud_min_aus_norm(anf.gleichmaessigkeit_max)
        ziel = anf.min_lux or 1.0
        breite = min(bounds[2] - bounds[0], bounds[3] - bounds[1])
        linie, band = _nachweis_punkte(
            mittellinie(r.polygon_mm, raster_mm=_NACHWEIS_RASTER_MM), breite
        )
        # Start-Abstand photometrisch aus der Leuchte selbst (aufweiten UND verdichten
        # möglich — der alte Fix-Start bei 8 m konnte nur verdichten). Die Optik wird
        # längs der Korridor-Achse montiert (Azimut je Kandidat, s.u.) — der Reihen-
        # Startwert darf deshalb die C0-Keule ansetzen.
        abstand = max_leuchtenabstand_mm(
            montagehoehe_m=h_m, i_cd=i_cd, i_cd_fn=i_cd_fn, ziel_lux=ziel,
            min_mm=_MIN_ABSTAND_MM, max_mm=_MAX_ABSTAND_MM, optik_entlang_reihe=True,
        )
        kandidaten = leuchten_auf_linie_mit_richtung(r.polygon_mm, abstand)
        for _ in range(_MAX_VERDICHTUNGEN):
            if not linie:   # degeneriertes Polygon → alter Flächen-Nachweis als Fallback
                res = lux_raster(
                    kandidaten, bounds, montagehoehe_m=h_m, i_cd=i_cd, i_cd_fn=i_cd_fn,
                    ziel_lux=ziel, ud_min=ud_min,
                )
                erfuellt = res.erfuellt_min and res.erfuellt_ud
            else:
                mitte = lux_punkte(
                    kandidaten, linie, montagehoehe_m=h_m, i_cd=i_cd, i_cd_fn=i_cd_fn,
                    ziel_lux=ziel, ud_min=ud_min,
                )
                halbband = lux_punkte(
                    kandidaten, band, montagehoehe_m=h_m, i_cd=i_cd, i_cd_fn=i_cd_fn,
                    ziel_lux=ziel / 2.0, ud_min=0.0,
                ) if band else None
                erfuellt = (
                    mitte.erfuellt_min and mitte.erfuellt_ud
                    and (halbband is None or halbband.erfuellt_min)
                )
            if erfuellt or abstand <= _MIN_ABSTAND_MM:
                break
            abstand = max(_MIN_ABSTAND_MM, abstand / _VERDICHTUNGS_FAKTOR)
            kandidaten = leuchten_auf_linie_mit_richtung(r.polygon_mm, abstand)
        cx = (bounds[0] + bounds[2]) / 2
        building = assign_building(cx)
        for px, py, az in kandidaten:
            out.append(
                Platzierung(
                    xy_mm=(px, py),
                    catalog_key=_SL_KEY,
                    # Montage-Rotation = Korridor-Achse: die Optik-C0 zeigt längs
                    # des Gangs — exakt der Azimut, mit dem der Lux-Nachweis oben
                    # gerechnet hat (Azimut-Tripel). Symbol dreht mit.
                    rotation_deg=az,
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
