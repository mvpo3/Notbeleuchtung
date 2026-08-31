"""Naht-Test Geometrie ↔ LB-Vokabular.

Die Geometrie-Typisierung (`raumtyp_flags`, aus DXF-Stempeln) und das LB-Bereichs-
Vokabular (`_BEREICH_VOCAB`, aus dem LB-Text) müssen für denselben deutschen Stempel
DASSELBE `raum_typ`-Label erzeugen — sonst joint `lb_override` (r.raum_typ.upper() ==
b.raum_typ.upper()) nie und die LB-Inklusion/Exklusion ist für den Typ eine tote Regel
(Review-Befund zu #50/#51). Dieser Test friert die Übereinstimmung ein und bricht bei
künftiger Vokabular-Drift.
"""
from __future__ import annotations

import pytest

from notbeleuchtung.normwissen.lb.parser import _BEREICH_VOCAB
from notbeleuchtung.raumerkennung.raumtyp import raumtyp_flags

# Repräsentative reale Stempel → kanonisches Label. BEIDE Seiten müssen es liefern.
NAHT = [
    ("Garage", "GARAGE"), ("Tiefgarage", "GARAGE"),
    ("Technikraum", "TECHNIK"), ("Haustechnik", "TECHNIK"),
    ("Lager", "LAGER"), ("Lagerraum", "LAGER"),
    ("Abstellraum", "ABSTELLRAUM"), ("Einlagerungsraum", "ABSTELLRAUM"),
    ("Müllraum", "MUELLRAUM"), ("Restmüll", "MUELLRAUM"),
    ("Stiegenhaus", "STIEGENHAUS"),
]


def _lb_labels(stamp: str) -> set[str]:
    return {label for pat, label in _BEREICH_VOCAB if pat.search(stamp)}


@pytest.mark.parametrize("stamp, label", NAHT)
def test_geometrie_und_lb_vokabular_stimmen_ueberein(stamp, label):
    geom = raumtyp_flags(stamp)
    assert geom is not None and geom[0] == label, f"Geometrie {stamp!r} → {geom}"
    assert label in _lb_labels(stamp), f"LB {stamp!r} → {_lb_labels(stamp)}"


def test_einlagerung_nicht_als_lager_fehlgejoint():
    # „Einlagerungsraum" ist ABSTELLRAUM (beide Seiten), NICHT LAGER — \\blager greift
    # mid-word nicht, einlager gewinnt.
    assert _lb_labels("Einlagerungsraum") == {"ABSTELLRAUM"}
    assert raumtyp_flags("Einlagerungsraum")[0] == "ABSTELLRAUM"
