"""lux — photometrischer Nachweis der Notbeleuchtung (numpy Punktmethode).

Rechnet die horizontale Beleuchtungsstärke am Boden aus Leuchten-Positionen und
prüft die EN-1838-Kriterien: Mindest-Lux (1 lx Fluchtweg / 0,5 lx Antipanik) +
Gleichmäßigkeit Ud = min:max ≥ 1:40. Damit wird die geometrische Platzierung
**normkonform beweisbar** (die Lücke aus der Mollgasse-Analyse).

Modell = Punktlicht-Näherung: E = I · cos³θ / h²  (θ = Winkel Lot→Punkt, h = Montage-
höhe). `I` (cd) ist entweder konstant-isotrop (`i_cd`) oder — realistisch — richtungs-
abhängig aus der Hersteller-Photometrie (EULUMDAT/LDT): dann wird `i_cd_fn(γ)` mit dem
Ausstrahlwinkel γ [Grad] je Rasterpunkt aufgerufen. `i_cd_fn` ist bewusst ein
**Callable** (Dependency-Injection), damit `platzierung` das `normwissen`-Photometrie-
Modul NICHT importiert — die Import-Grenze zwischen den Owner-Packages bleibt gewahrt;
die Hauptengine baut das Callable aus `normwissen.photometrie.Photometrie.intensitaet`.
"""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

import numpy as np

Point = tuple[float, float]

_UD_DEFAULT = 1.0 / 40.0   # EN-1838-Default (Fluchtweg), falls die Norm keinen Wert liefert


def ud_min_aus_norm(gleichmaessigkeit_max: float | None) -> float:
    """Ud-Grenze (min:max) aus der Norm-Gleichmäßigkeit (max:min).

    Die Norm gibt die Gleichmäßigkeit als Verhältnis max:min an — EN 1838 §4.2.2
    (Rettungsweg) und §4.3.2 (Antipanik) fordern wortgleich je 40 (Ud 1:40). Die
    früher hier behauptete „10 Antipanik" war Uo >= 0,1 aus §4.4.2 (Arbeitsplätze) —
    Uo (kleinste:mittlere, EN 12665) ist ein anderes Maß als Ud (kleinste:größte),
    Enis' Quellen-Korrektur (COORDINATION 2026-09-01). Der Lux-Nachweis rechnet Ud
    als min:max → Kehrwert. `None` (Norm liefert (noch) keinen Wert) fällt auf den
    Default 1:40 zurück, damit sich ohne Enis-Daten nichts am Plan ändert.
    """
    return 1.0 / gleichmaessigkeit_max if gleichmaessigkeit_max else _UD_DEFAULT


@dataclass
class LuxErgebnis:
    min_lux: float
    max_lux: float
    mittel_lux: float
    ud: float                    # min:max (0..1); EN 1838 verlangt >= 1/40
    erfuellt_min: bool
    erfuellt_ud: bool


def lux_raster(
    leuchten: list[Point],
    bounds_mm: tuple[float, float, float, float],
    *,
    montagehoehe_m: float = 2.0,   # EN-1838-§4.1-Mindesthöhe als Fallback; produktive
    #                                Aufrufer übergeben die echte Norm-Höhe (anf.montagehoehe_mm)
    i_cd: float = 200.0,
    i_cd_fn: Callable[[float], float] | None = None,
    ziel_lux: float = 1.0,
    ud_min: float = _UD_DEFAULT,
    rand_mm: float = 500.0,
    raster_mm: float = 250.0,
) -> LuxErgebnis:
    """Beleuchtungsstärke-Raster über `bounds_mm` und EN-1838-Bewertung.

    `rand_mm` = umlaufender Randstreifen, der laut EN 1838 §4.2.1 vom Nachweis
    ausgenommen ist. `ziel_lux` = 1.0 Fluchtweg / 0.5 Antipanik. `ud_min` = geforderte
    Gleichmäßigkeit (min:max), Default 1:40; produktive Aufrufer leiten sie über
    `ud_min_aus_norm(anf.gleichmaessigkeit_max)` aus der Norm ab.

    Ist `i_cd_fn` gesetzt, überschreibt es `i_cd`: die Lichtstärke wird je Rasterpunkt
    aus dem Ausstrahlwinkel γ [Grad] = atan(horizontale Distanz / h) bestimmt
    (Hersteller-Photometrie). Sonst wird konstant `i_cd` (isotrop) gerechnet.
    """
    minx, miny, maxx, maxy = bounds_mm
    xs = np.arange(minx + rand_mm, maxx - rand_mm + 1e-6, raster_mm)
    ys = np.arange(miny + rand_mm, maxy - rand_mm + 1e-6, raster_mm)
    if len(xs) == 0 or len(ys) == 0 or not leuchten:
        return LuxErgebnis(0.0, 0.0, 0.0, 0.0, False, False)
    gx, gy = np.meshgrid(xs, ys)
    h_mm = montagehoehe_m * 1000.0
    i_fn_v = np.vectorize(i_cd_fn) if i_cd_fn is not None else None
    e = np.zeros_like(gx, dtype=float)
    for lx, ly in leuchten:
        dx = gx - lx
        dy = gy - ly
        d_h = np.sqrt(dx * dx + dy * dy)          # horizontale Distanz (mm)
        d = np.sqrt(d_h * d_h + h_mm * h_mm)       # Schrägdistanz zur Leuchte
        cos_theta = h_mm / d                       # cos zwischen Lot und Strahl
        # I je Punkt: richtungsabhängig aus Photometrie (γ) oder konstant isotrop.
        i = i_fn_v(np.degrees(np.arctan2(d_h, h_mm))) if i_fn_v is not None else i_cd
        # E = I * cos^3(theta) / h^2 ; h in Metern (I in cd, Ergebnis in lx)
        e += i * cos_theta**3 / (montagehoehe_m**2)
    mn, mx, mean = float(e.min()), float(e.max()), float(e.mean())
    ud = (mn / mx) if mx > 0 else 0.0
    return LuxErgebnis(
        min_lux=mn, max_lux=mx, mittel_lux=mean, ud=ud,
        erfuellt_min=mn >= ziel_lux,
        erfuellt_ud=ud >= ud_min,
    )
