"""lux_nachweis — EN-1838-Fluchtweg-Nachweis als Bericht (wie Profi-DIALux/Relux).

Drei geprüfte Profi-Berechnungen (Aichholzgasse/Schrack · Barawitzka/din · Linke
Wienzeile/din — siehe `knowledge/extracted/LICHTBERECHNUNG_REFERENZ.md`) weisen je
Rettungsweg **zwei** Werte aus:

- **Mittellinie** ≥ 1,00 lx (horizontale Mindest-Beleuchtungsstärke auf der Achse)
- **Mittelfläche** (halbes Band ± Breite/4) ≥ 0,50 lx

plus **Ud = Emin/Emax ≥ 1:40** (0,025) — gerechnet mit **Wartungsfaktor 0,80** und
**ohne Reflexion**. Die Engine platziert bereits danach (`deckung.verdichte_fluchtweg`),
lieferte den Nachweis aber nie als auditierbaren Bericht.

Dieses Modul erzeugt ihn **render-frei aus dem fertigen `PlatzierungsErgebnis`** —
reine Konsumption, es ändert KEINE Platzierung. Damit liegt es sauber in der
Leonis-/Platzierungs-Lane und schneidet sich nicht mit paralleler Pipeline-/Render-
Arbeit; die Hauptengine hängt es später additiv in `render_summary` ein (Naht).
"""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from notbeleuchtung.hauptengine.contracts import (
    NormProvider,
    PlatzierungsErgebnis,
    RaumModell,
)

from .bausteine import KORRIDOR_TYPEN as _KORRIDOR_TYPEN
from .geometry import _bbox, point_in_polygon
from .lux import lux_punkte, ud_min_aus_norm, wartungsfaktor_aus_norm
from .mittellinie import mittellinie

_NACHWEIS_RASTER_MM = 250.0
Point = tuple[float, float]


@dataclass
class FluchtwegNachweis:
    """EN-1838-§4.2.1-Nachweis eines Fluchtweg-Raums (ein Rettungsweg im Bericht)."""

    bereich_id: str
    leuchten: int
    emin_mittellinie: float          # lx, Soll ≥ soll_mittellinie
    emin_mittelflaeche: float        # lx, Soll ≥ soll_mittelflaeche
    emax: float                      # lx, größter Nachweispunkt
    ud: float                        # Emin/Emax über die Mittelfläche (0..1)
    soll_mittellinie: float          # 1,0 lx (Fluchtweg)
    soll_mittelflaeche: float        # 0,5 lx (halbes Mittenband)
    soll_ud: float                   # 0,025 (= Emax:Emin ≤ 40)
    wartungsfaktor: float            # angewandter MF (1,0 = keiner)
    erfuellt: bool
    norm_quelle: str


def _band_punkte(linie: list[Point], breite_mm: float) -> list[Point]:
    """Mittenband-Punkte ± Breite/4 entlang der lokalen Tangente (wie deckung)."""
    if len(linie) < 2:
        return []
    off = breite_mm / 4.0
    band: list[Point] = []
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
    return band


def nachweis_fluchtweg(
    raum: RaumModell,
    norm: NormProvider,
    ergebnis: PlatzierungsErgebnis,
    *,
    i_cd: float = 200.0,
    i_cd_fn: Callable[..., float] | None = None,
) -> list[FluchtwegNachweis]:
    """Je Korridor-Raum ein `FluchtwegNachweis` aus den platzierten Sicherheitsleuchten.

    Rechnet die Beleuchtungsstärke der IM Raum liegenden `sicherheitsleuchte`-
    Platzierungen (mit deren Optik-Azimut = `rotation_deg`) auf Mittellinie und
    Mittenband — physikidentisch zu `deckung`/`lux`, inkl. Wartungsfaktor aus der
    Norm (`anf.wartungsfaktor`, defensiv; 1,0 solange die Norm ihn nicht liefert).
    Audit/Reporting — verändert nichts.
    """
    sl = [
        (p.xy_mm[0], p.xy_mm[1], p.rotation_deg)
        for p in ergebnis.platzierungen
        if p.kind == "sicherheitsleuchte"
    ]
    berichte: list[FluchtwegNachweis] = []
    for r in raum.raeume:
        if r.raum_typ.upper() not in _KORRIDOR_TYPEN or len(r.polygon_mm) < 3:
            continue
        anf = norm.fuer_raum(r.raum_typ, r.ist_fluchtweg)
        h_m = anf.montagehoehe_mm / 1000.0
        ud_min = ud_min_aus_norm(anf.gleichmaessigkeit_max)
        ziel = anf.min_lux or 1.0
        wf = wartungsfaktor_aus_norm(anf)

        drin = [(x, y, az) for (x, y, az) in sl if point_in_polygon((x, y), r.polygon_mm)]
        bounds = _bbox(r.polygon_mm)
        breite = min(bounds[2] - bounds[0], bounds[3] - bounds[1])
        linie = mittellinie(r.polygon_mm, raster_mm=_NACHWEIS_RASTER_MM)
        band = _band_punkte(linie, breite)

        mitte = lux_punkte(
            drin, linie, montagehoehe_m=h_m, i_cd=i_cd, i_cd_fn=i_cd_fn,
            ziel_lux=ziel, ud_min=ud_min, wartungsfaktor=wf,
        )
        flaeche = lux_punkte(
            drin, linie + band, montagehoehe_m=h_m, i_cd=i_cd, i_cd_fn=i_cd_fn,
            ziel_lux=ziel / 2.0, ud_min=ud_min, wartungsfaktor=wf,
        ) if band else mitte

        erfuellt = (
            bool(drin)
            and mitte.erfuellt_min                 # Mittellinie ≥ 1 lx
            and flaeche.erfuellt_min               # Mittelfläche ≥ 0,5 lx
            and flaeche.ud >= ud_min               # Emax:Emin ≤ 40
        )
        berichte.append(
            FluchtwegNachweis(
                bereich_id=r.id,
                leuchten=len(drin),
                emin_mittellinie=round(mitte.min_lux, 2),
                emin_mittelflaeche=round(flaeche.min_lux, 2),
                emax=round(flaeche.max_lux, 2),
                ud=round(flaeche.ud, 3),
                soll_mittellinie=ziel,
                soll_mittelflaeche=ziel / 2.0,
                soll_ud=round(ud_min, 3),
                wartungsfaktor=wf,
                erfuellt=erfuellt,
                norm_quelle=anf.quelle,
            )
        )
    return berichte


def nachweis_summary(berichte: list[FluchtwegNachweis]) -> dict:
    """Kompakte, JSON-fähige Zusammenfassung für `render_summary["lux_nachweis"]`."""
    return {
        "bereiche": len(berichte),
        "erfuellt": sum(1 for b in berichte if b.erfuellt),
        "alle_erfuellt": all(b.erfuellt for b in berichte) if berichte else True,
        "wartungsfaktor": (berichte[0].wartungsfaktor if berichte else 1.0),
        "rettungswege": [
            {
                "bereich": b.bereich_id,
                "leuchten": b.leuchten,
                "emin_mittellinie": b.emin_mittellinie,
                "emin_mittelflaeche": b.emin_mittelflaeche,
                "ud": b.ud,
                "soll": {
                    "mittellinie": b.soll_mittellinie,
                    "mittelflaeche": b.soll_mittelflaeche,
                    "ud": b.soll_ud,
                },
                "erfuellt": b.erfuellt,
                "norm_quelle": b.norm_quelle,
            }
            for b in berichte
        ],
    }
