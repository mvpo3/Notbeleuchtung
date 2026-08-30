"""ies — IESNA LM-63 Photometrie-Import (zweites Hersteller-Format neben EULUMDAT).

Viele Hersteller liefern `.ies` (IESNA LM-63) statt `.ldt`. `lade_ies` erzeugt
denselben `Photometrie`-Typ wie `lade_ldt` — die öffentliche API (`intensitaet`,
Felder `c_grad/gamma_grad/cd_pro_klm/lampen_lumen/name`) bleibt identisch, damit die
F1-Naht (`platzierung/lux.py` via `i_cd_fn`) unverändert läuft.

LM-63-Aufbau: Keyword-/Kommentarzeilen, dann `TILT=…`, dann ein reiner Zahlenstrom
(zeilenübergreifend, tokenweise): Lampen-/Geometrie-Kopf, Vorschalt-Zeile, die
vertikalen Winkel (= γ), die horizontalen Winkel (= C-Ebenen) und schließlich die
Candela-Werte je horizontalem Winkel (Reihenfolge `candela[h][v]`).

Einheiten: `intensitaet` rechnet `cd = cd_pro_klm · lampen_lumen/1000`. IES liefert
absolute cd (`roh · candela_multiplier`), darum
`cd_pro_klm[h][v] = roh · candela_multiplier · 1000 / lampen_lumen` — so kommen
hinten wieder korrekte absolute cd heraus.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np

from .ldt import Photometrie


class _Tokens:
    """Whitespace-Token-Strom mit Positionszeiger — LM-63-Zahlen brechen über Zeilen um."""

    def __init__(self, text: str) -> None:
        self._t = text.split()
        self._i = 0

    def _next(self) -> str:
        if self._i >= len(self._t):
            raise ValueError("IES: Zahlenstrom endet vorzeitig (Datei unvollständig).")
        v = self._t[self._i]
        self._i += 1
        return v

    def i(self) -> int:
        try:
            return int(float(self._next()))
        except ValueError as e:
            raise ValueError(f"IES: erwartete Ganzzahl, las '{self._t[self._i - 1]}'.") from e

    def f(self) -> float:
        try:
            return float(self._next())
        except ValueError as e:
            raise ValueError(f"IES: erwartete Zahl, las '{self._t[self._i - 1]}'.") from e

    def floats(self, n: int) -> np.ndarray:
        return np.array([self.f() for _ in range(n)])


def lade_ies(pfad: str | Path) -> Photometrie:
    """IESNA-LM-63-Datei (`.ies`) einlesen → `Photometrie` (gleicher Typ wie `lade_ldt`)."""
    raw = Path(pfad).read_text(encoding="latin-1")
    lines = raw.splitlines()

    # Kopf (Keywords/Kommentare) bis zur TILT-Zeile überspringen.
    tilt_idx = next((k for k, ln in enumerate(lines) if ln.strip().upper().startswith("TILT=")), -1)
    if tilt_idx < 0:
        raise ValueError("IES: keine 'TILT='-Zeile gefunden — kein gültiges LM-63.")
    name = _luminaire_name(lines[:tilt_idx])
    tilt_val = lines[tilt_idx].split("=", 1)[1].strip().upper()

    tok = _Tokens("\n".join(lines[tilt_idx + 1:]))

    if tilt_val == "INCLUDE":                    # eingebettete Tilt-Daten überspringen
        tok.f()                                  # lamp-to-luminaire geometry
        n_tilt = tok.i()
        tok.floats(2 * n_tilt)                   # Winkel + Multiplikatoren

    n_lamps = tok.i()
    lumens_per_lamp = tok.f()
    candela_multiplier = tok.f()
    n_vert = tok.i()
    n_horiz = tok.i()
    tok.i()                                      # photometric_type (nicht benötigt)
    tok.i()                                      # units_type
    tok.floats(3)                                # width / length / height
    tok.floats(3)                                # ballast_factor / future / input_watts

    if n_vert < 1 or n_horiz < 1:
        raise ValueError(f"IES: ungültige Winkelzahl n_vert={n_vert} n_horiz={n_horiz}.")

    gamma = tok.floats(n_vert)                   # vertikale Winkel = γ
    c_angles = tok.floats(n_horiz)               # horizontale Winkel = C-Ebenen
    cd_raw = tok.floats(n_horiz * n_vert).reshape(n_horiz, n_vert)   # candela[h][v]

    # absolute Fotometrie: lumens_per_lamp == -1 → Bezugsstrom 1000 lm.
    lampen_lumen = 1000.0 if lumens_per_lamp == -1 else n_lamps * lumens_per_lamp
    if lampen_lumen <= 0:
        raise ValueError(f"IES: Lampen-Lichtstrom nicht positiv ({lampen_lumen}).")
    cd_pro_klm = cd_raw * candela_multiplier * 1000.0 / lampen_lumen

    c_grad, matrix = _expand_horizontal(c_angles, cd_pro_klm)
    return Photometrie(
        c_grad=c_grad, gamma_grad=gamma, cd_pro_klm=matrix,
        lampen_lumen=lampen_lumen, name=name,
    )


def _luminaire_name(pre: list[str]) -> str:
    """Leuchtenname aus Keyword ([LUMINAIRE]/[MANUFAC]) vor TILT, sonst erste Zeile."""
    def kw(key: str) -> str | None:
        tag = f"[{key}]"
        for ln in pre:
            s = ln.strip()
            if s.upper().startswith(tag):
                return s[len(tag):].strip()
        return None

    return kw("LUMINAIRE") or kw("MANUFAC") or next((ln.strip() for ln in pre if ln.strip()), "")


def _expand_horizontal(c_angles: np.ndarray, matrix: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """LM-63-Horizontalsymmetrie → volle C-Runde (monoton 0..<360)."""
    nv = matrix.shape[1]
    last = float(c_angles[-1])

    if len(c_angles) == 1 or last <= 1e-6:       # nur 0° → rotationssymmetrisch
        return np.array([0.0, 90.0, 180.0, 270.0]), np.repeat(matrix[0:1], 4, axis=0)

    step = float(c_angles[1] - c_angles[0])
    if abs(last - 90.0) < 1.0:
        span = 90.0                              # 0–90° → Quadranten-Symmetrie
    elif abs(last - 180.0) < 1.0:
        span = 180.0                             # 0–180° → bilateral
    else:                                        # 0–360° (oder frei) → wie geliefert
        c = np.asarray(c_angles, float)
        if abs(c[-1] - 360.0) < 1e-6:            # doppelte 360°-Ebene fällt weg (== 0°)
            return c[:-1], matrix[:-1]
        return c, matrix

    n_full = round(360.0 / step)
    full_c = np.arange(n_full) * step
    given = np.asarray(c_angles, float)
    full = np.zeros((n_full, nv))
    for k, a in enumerate(full_c):
        af = _fold_h(a, span)
        full[k] = matrix[int(np.argmin(np.abs(given - af)))]
    return full_c, full


def _fold_h(a: float, span: float) -> float:
    """Horizontalwinkel in den gespeicherten Bereich falten."""
    a = a % 360.0
    if span == 180.0:                            # Symmetrie an C0-C180
        return 360.0 - a if a > 180.0 else a
    if a > 180.0:                                # Quadrant: an C0-C180 …
        a = 360.0 - a
    if a > 90.0:                                 # … und an C90-C270
        a = 180.0 - a
    return a
