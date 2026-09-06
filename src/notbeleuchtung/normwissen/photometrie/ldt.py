"""ldt — EULUMDAT/LDT-Photometrie-Import (Hersteller-Lichtstärkeverteilung).

Liest eine EULUMDAT-Datei (`.ldt`, Herstellerformat für Leuchten) und liefert die
richtungsabhängige Lichtstärke `I(γ, C)` in **cd**. γ = Ausstrahlungswinkel gegen die
Lot-Achse (0° = senkrecht nach unten), C = azimutale C-Ebene (0..360°).

Zweck (Naht F2→F1, siehe `docs/COORDINATION.md`): der Lux-Nachweis in
`platzierung/lux.py` rechnet bisher mit einer konstanten, isotropen Lichtstärke
(`i_cd`). `Photometrie.intensitaet(γ, C)` ersetzt diese Konstante durch die echte
Verteilung der eingesetzten Leuchte → normkonform beweisbarer EN-1838-Nachweis.

EULUMDAT-Aufbau (zeilenbasiert, 1-indexiert): 26 Kopfzeilen, dann je Lampensatz
6 Zeilen, dann 10 Direktwirkungs-Werte (DR), dann `Mc` C-Winkel, `Ng` γ-Winkel und
schließlich die Intensitäten (cd/1000 lm). Die Anzahl gespeicherter Intensitäten
hängt an der Symmetrie `Isym` — die volle C-Matrix wird per Spiegelung rekonstruiert.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np


@dataclass
class Photometrie:
    """Lichtstärkeverteilung einer Leuchte, aus EULUMDAT rekonstruiert.

    `cd_pro_klm` ist die volle C×γ-Matrix in cd/1000 lm (Form `[len(c_grad), len(gamma_grad)]`).
    Absolute cd = Wert · `lampen_lumen` / 1000.
    """

    c_grad: np.ndarray          # C-Ebenen-Winkel 0..<360 (aufsteigend), Länge Mc
    gamma_grad: np.ndarray      # γ-Winkel 0..≤180 (aufsteigend), Länge Ng
    cd_pro_klm: np.ndarray      # [len(c_grad), len(gamma_grad)] in cd/1000 lm
    lampen_lumen: float         # Gesamt-Lichtstrom der Lampen (lm)
    name: str = ""

    def ist_rotationssymmetrisch(self, toleranz_cd: float = 1e-9) -> bool:
        """Streuen die C-Ebenen? **An den Daten geprüft**, nicht am Produktnamen.

        „Rundoptik" im Namen belegt keine Rotationssymmetrie — und der
        EULUMDAT-Header hilft auch nicht zuverlässig: die Schrack-Rundlinsen
        tragen `Isym = 4` (Quadrant), sind nach der Symmetrie-Expansion aber
        tatsächlich rotationssymmetrisch. Deshalb wird die expandierte Matrix
        geprüft.
        """
        streuung = float(np.max(np.ptp(self.cd_pro_klm, axis=0)))
        return streuung * self.lampen_lumen / 1000.0 < toleranz_cd

    def min_intensitaet(self, gamma_grad: float) -> float:
        """Kleinste Lichtstärke über **alle** C-Ebenen bei diesem γ, in cd.

        Der belastbare Wert, wenn die physische Ausrichtung der Optik im Plan
        nicht zugesichert ist: er unterschätzt nie. Bewusst **kein** Mittelwert
        und **kein** fester C-Winkel — beides könnte einen Nachweis fälschlich
        bestehen lassen.
        """
        g = float(np.clip(gamma_grad, self.gamma_grad[0], self.gamma_grad[-1]))
        werte = [np.interp(g, self.gamma_grad, zeile) for zeile in self.cd_pro_klm]
        return float(min(werte)) * self.lampen_lumen / 1000.0

    def intensitaet(self, gamma_grad: float, c_grad: float = 0.0) -> float:
        """Lichtstärke in **cd** für Ausstrahlwinkel γ und C-Ebene C (bilinear).

        γ wird auf den erfassten Bereich geklemmt, C periodisch (mod 360°) behandelt.
        """
        g = float(np.clip(gamma_grad, self.gamma_grad[0], self.gamma_grad[-1]))
        c = float(c_grad) % 360.0
        # C periodisch schließen: Ebene bei 360° = Ebene bei 0°.
        c_ext = np.append(self.c_grad, self.c_grad[0] + 360.0)
        mat_ext = np.vstack([self.cd_pro_klm, self.cd_pro_klm[0:1]])
        i = int(np.searchsorted(c_ext, c, side="right") - 1)
        i = max(0, min(i, len(c_ext) - 2))
        c0, c1 = c_ext[i], c_ext[i + 1]
        t = 0.0 if c1 == c0 else (c - c0) / (c1 - c0)
        row = mat_ext[i] * (1.0 - t) + mat_ext[i + 1] * t   # γ-Profil der interpol. C-Ebene
        val_klm = float(np.interp(g, self.gamma_grad, row))
        return val_klm * self.lampen_lumen / 1000.0


def _f(s: str) -> float:
    """EULUMDAT-Zahl → float (Komma- oder Punkt-Dezimal)."""
    return float(s.strip().replace(",", "."))


def lade_ldt(pfad: str | Path) -> Photometrie:
    """EULUMDAT-Datei (`.ldt`) einlesen → `Photometrie`."""
    lines = [ln.strip() for ln in Path(pfad).read_text(encoding="latin-1").splitlines()]

    isym = int(lines[2])
    mc = int(lines[3])                     # Anzahl C-Ebenen
    ng = int(lines[5])                     # Anzahl γ-Werte je C-Ebene
    name = lines[8]
    conversion = _f(lines[23]) or 1.0      # Umrechnungsfaktor Lichtstärken
    n_sets = abs(int(lines[25]))           # Anzahl Lampensätze (neg = absolute Fotometrie)

    # Lampensätze: je 6 Zeilen (Anzahl / Typ / Lichtstrom / Farbe / Ra / Watt).
    lamp0 = 26
    lampen_lumen = _f(lines[lamp0 + 2]) if n_sets else 1000.0

    # Nach den Lampensätzen: 10 DR-Werte, dann Mc C-Winkel, Ng γ-Winkel, dann Intensitäten.
    p = lamp0 + 6 * n_sets + 10
    c_angles = np.array([_f(lines[p + k]) for k in range(mc)])
    p += mc
    gamma = np.array([_f(lines[p + k]) for k in range(ng)])
    p += ng

    n_stored = _stored_planes(isym, mc)
    vals = np.array([_f(lines[p + k]) for k in range(n_stored * ng)]) * conversion
    stored = vals.reshape(n_stored, ng)                 # [gespeicherte C-Ebenen, γ]

    matrix = _expand_symmetry(stored, isym, mc, c_angles, gamma)
    return Photometrie(
        c_grad=c_angles, gamma_grad=gamma, cd_pro_klm=matrix,
        lampen_lumen=lampen_lumen, name=name,
    )


def _stored_planes(isym: int, mc: int) -> int:
    """Anzahl tatsächlich gespeicherter C-Ebenen je Symmetrie-Typ."""
    if isym == 0:
        return mc
    if isym == 1:
        return 1
    if isym in (2, 3):
        return mc // 2 + 1
    if isym == 4:
        return mc // 4 + 1
    raise ValueError(f"unbekannte EULUMDAT-Symmetrie Isym={isym}")


def _expand_symmetry(
    stored: np.ndarray, isym: int, mc: int, c_angles: np.ndarray, gamma: np.ndarray,
) -> np.ndarray:
    """Gespeicherte C-Ebenen per Spiegelung auf die volle Mc×Ng-Matrix bringen."""
    ng = len(gamma)
    if isym == 0:
        return stored
    if isym == 1:
        return np.repeat(stored, mc, axis=0)            # rotationssymmetrisch

    # Isym 2/3/4: gespeicherte Ebenen liegen bei bekannten C-Winkeln; jede volle
    # Ebene über ihren (ggf. gespiegelten) Winkel auf eine gespeicherte Zeile abbilden.
    n_stored = stored.shape[0]
    span = 90.0 if isym == 4 else 180.0
    base = 90.0 if isym == 3 else 0.0       # Isym=3 speichert C90..C270
    stored_angles = base + (np.arange(n_stored) * (span / (n_stored - 1)) if n_stored > 1
                            else np.array([0.0]))

    full = np.zeros((mc, ng))
    for idx, a in enumerate(c_angles):
        af = _fold_angle(a, isym)
        j = int(np.argmin(np.abs(stored_angles - af)))
        full[idx] = stored[j]
    return full


def _fold_angle(a: float, isym: int) -> float:
    """C-Winkel in den gespeicherten Bereich falten (Symmetrie-Ebenen)."""
    a = a % 360.0
    if isym == 2:                       # Symmetrie an C0-C180 → I(a)=I(360-a)
        return 360.0 - a if a > 180.0 else a
    if isym == 3:                       # Symmetrie an C90-C270 → I(a)=I(180-a)
        return (180.0 - a) % 360.0 if not (90.0 <= a <= 270.0) else a
    if isym == 4:                       # beide → in ersten Quadranten
        if a > 180.0:
            a = 360.0 - a
        if a > 90.0:
            a = 180.0 - a
        return a
    return a
