"""ldt — EULUMDAT-Import: Achsen/Lumen, γ-Interpolation, cd-Skalierung, Isym-Symmetrie."""
from pathlib import Path

from notbeleuchtung.normwissen.photometrie import Photometrie, lade_ldt

MINI = Path(__file__).parent.parent / "fixtures" / "photometrie" / "mini.ldt"


def _p() -> Photometrie:
    return lade_ldt(MINI)


def test_parst_achsen_und_lumen():
    p = _p()
    assert p.name == "MINI Rettungszeichenleuchte"
    assert p.lampen_lumen == 1000.0
    assert list(p.gamma_grad) == [0, 15, 30, 45, 60, 75, 90]
    assert len(p.c_grad) == 24                    # Mc C-Ebenen, auch bei Isym=1
    assert p.cd_pro_klm.shape == (24, 7)          # volle Matrix nach Expansion


def test_intensitaet_stuetzstellen():
    p = _p()
    assert p.intensitaet(0.0) == 200.0            # γ=0 exakte Stützstelle, 1000 lm → cd = klm-Wert
    assert p.intensitaet(45.0) == 120.0
    assert p.intensitaet(90.0) == 0.0


def test_intensitaet_interpoliert_linear():
    p = _p()
    # γ=37.5 liegt mittig zwischen 30° (160) und 45° (120) → 140.
    assert p.intensitaet(37.5) == 140.0


def test_cd_skaliert_mit_lumen():
    p = _p()
    p.lampen_lumen = 2000.0                        # doppelter Lichtstrom → doppelte cd
    assert p.intensitaet(0.0) == 400.0


def test_isym1_unabhaengig_von_c():
    p = _p()
    # Rotationssymmetrisch: gleiche Lichtstärke in jeder C-Ebene.
    assert p.intensitaet(30.0, c_grad=0.0) == p.intensitaet(30.0, c_grad=180.0)
    assert p.intensitaet(60.0, c_grad=90.0) == p.intensitaet(60.0, c_grad=270.0)


def test_gamma_ausserhalb_geklemmt():
    p = _p()
    assert p.intensitaet(120.0) == p.intensitaet(90.0)   # über Messbereich → geklemmt
