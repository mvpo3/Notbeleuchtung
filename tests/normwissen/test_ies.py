"""ies — IESNA-LM-63-Import: Achsen/Lumen, Interpolation, absolute Fotometrie, Symmetrie."""
from pathlib import Path

import numpy as np
import pytest

from notbeleuchtung.normwissen.photometrie import Photometrie, lade_ies

MINI = Path(__file__).parent.parent / "fixtures" / "photometrie" / "mini.ies"


def _p() -> Photometrie:
    return lade_ies(MINI)


def test_parst_achsen_und_lumen():
    p = _p()
    assert isinstance(p, Photometrie)
    assert p.name == "MINI Rettungszeichenleuchte IES"
    assert p.lampen_lumen == 1000.0
    assert list(p.gamma_grad) == [0, 15, 30, 45, 60, 75, 90]     # vertikale Winkel = γ
    assert p.cd_pro_klm.shape[1] == 7


def test_intensitaet_stuetzstellen_und_interpolation():
    p = _p()
    assert p.intensitaet(0.0) == 200.0        # candela_multiplier=1, 1000 lm → cd == roh
    assert p.intensitaet(45.0) == 120.0
    assert p.intensitaet(90.0) == 0.0
    # γ=37.5 mittig zwischen 30° (160) und 45° (120) → 140.
    assert p.intensitaet(37.5) == 140.0


def test_rotationssym_unabhaengig_von_c():
    p = _p()
    assert p.intensitaet(30.0, c_grad=0.0) == p.intensitaet(30.0, c_grad=180.0)
    assert p.intensitaet(60.0, c_grad=90.0) == p.intensitaet(60.0, c_grad=270.0)


def test_absolute_fotometrie_lumens_minus1(tmp_path):
    # lumens_per_lamp == -1 → Bezugsstrom 1000 lm; candela_multiplier skaliert absolute cd.
    ies = tmp_path / "abs.ies"
    ies.write_text(
        "IESNA:LM-63-2002\n[LUMINAIRE] ABS\nTILT=NONE\n"
        "1 -1 2.0 3 1 1 2 0 0 0\n1 1 5\n"
        "0 45 90\n0\n"
        "150 100 0\n"
    )
    p = lade_ies(ies)
    assert p.lampen_lumen == 1000.0
    assert p.intensitaet(0.0) == 300.0        # 150 roh · candela_multiplier 2.0
    assert p.intensitaet(45.0) == 200.0


def test_horizontale_symmetrie_bilateral(tmp_path):
    # 0–180° bilateral → volle C-Runde; C=270 spiegelt auf C=90.
    ies = tmp_path / "bilat.ies"
    ies.write_text(
        "IESNA:LM-63-2002\n[LUMINAIRE] BILAT\nTILT=NONE\n"
        "1 1000 1.0 3 3 1 2 0 0 0\n1 1 5\n"
        "0 45 90\n"          # γ
        "0 90 180\n"         # C-Ebenen (bilateral)
        "10 11 12\n"         # C0
        "20 21 22\n"         # C90
        "30 31 32\n"         # C180
    )
    p = lade_ies(ies)
    assert list(p.c_grad) == [0.0, 90.0, 180.0, 270.0]    # auf volle Runde expandiert
    assert p.intensitaet(0.0, c_grad=270.0) == p.intensitaet(0.0, c_grad=90.0)  # 270→90
    assert p.intensitaet(0.0, c_grad=90.0) == 20.0


def test_kaputte_datei_valueerror(tmp_path):
    bad = tmp_path / "kaputt.ies"
    bad.write_text("das ist keine IES-Datei\nnur text\n")
    with pytest.raises(ValueError):
        lade_ies(bad)


def test_output_typ_identisch_zu_ldt():
    # F1-Naht hängt am gemeinsamen Typ + Callable-Signatur.
    p = _p()
    assert callable(p.intensitaet)
    assert isinstance(p.cd_pro_klm, np.ndarray)
