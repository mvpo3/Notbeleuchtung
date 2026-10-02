"""Abschnitt 6 (Entscheid 7, D-04) — Maßstab über die Tür an den vier Plänen mit
widersprechender Türprobe.

LUECKEN.md § 20.3: Rennweg EG und Am Rain OG4/OG3/EG fallen mangels Wand-Spanne auf
``$INSUNITS=4`` (Faktor 1) zurück, die alte Türprobe sagte „10 — widerspricht". Seit
Entscheid 7 kalibriert der Rückfall über die Türschwenkbögen mit Tür-Beleg (Tür-Layer
oder Tür-Block, Schwenk 60–120°): der Faktor legt ihren Median in die Regelbreite
(900 mm, Band 600–1300 mm). Abnahme: die vier Pläne laufen kalibriert durch, die
Türbreiten danach (``tuer_oeffnungen`` in mm) liegen im Median im Band (§ 28).

Rennweg EG ist der getrackte Gate-Plan; Am Rain liegt als getracktes Zip vor
(byteidentisch zur Prüfstrecken-Kopie). Nur ``lade_dxf`` + Türöffnungen, kein Parse.
"""
from __future__ import annotations

import statistics
import zipfile
from pathlib import Path

import pytest

from plaene import RENNWEG_EG, plan

AM_RAIN_ZIP = Path(__file__).resolve().parents[2] / "Projekte" / "Am Rain.zip"
AM_RAIN = {
    "AmRain_OG4": "Am Rain/ARAI5_FE_XEL_ZZ_MOP_OG4_0015_V_01.dxf",
    "AmRain_OG3": "Am Rain/ARAI5_FE_XEL_ZZ_MOP_OG3_0014_V_01.dxf",
    "AmRain_EG": "Am Rain/ARAI5_FE_XEL_ZZ_MOP_EG_0011_V_02.dxf",
}
BAND_MM = (600.0, 1300.0)          # Regelbreite 900 mm ± Nennmaß-Türbereich


def _dxf(name: str, tmp_path_factory) -> Path:
    if name == "Rennweg_EG":
        return plan(RENNWEG_EG)
    if not AM_RAIN_ZIP.is_file():
        pytest.fail(f"Versioniertes Zip fehlt: {AM_RAIN_ZIP}")
    return Path(zipfile.ZipFile(AM_RAIN_ZIP).extract(AM_RAIN[name],
                                                    tmp_path_factory.mktemp(name)))


@pytest.mark.parametrize("name", ["Rennweg_EG", "AmRain_OG4", "AmRain_OG3", "AmRain_EG"])
def test_widersprechende_tuerprobe_kalibriert_ueber_tueren(name, tmp_path_factory):
    from notbeleuchtung.raumerkennung.dxf_load import lade_dxf
    from notbeleuchtung.raumerkennung.tueren import tuer_oeffnungen

    p = lade_dxf(_dxf(name, tmp_path_factory))
    assert p.factor == 1.0, (p.factor, p.faktor_quelle)
    assert not p.massstab_unsicher, p.faktor_quelle
    assert p.faktor_quelle.startswith("Türkalibrierung ("), p.faktor_quelle
    assert p.faktor_quelle.endswith("$INSUNITS=4 (keine Wand-Spanne 15–500 m messbar) "
                                    "bestätigt"), p.faktor_quelle
    # Türbreiten danach: die vermessenen Türblätter (Schwenkradius/Blockname) in mm.
    breiten = [o.breite_mm for o in tuer_oeffnungen(p) if o.breite_mm]
    assert len(breiten) >= 3, breiten
    assert BAND_MM[0] <= statistics.median(breiten) <= BAND_MM[1], sorted(breiten)
