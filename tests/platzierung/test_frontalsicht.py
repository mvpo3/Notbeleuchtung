"""frontalsicht_block (M3/RW-007) — Pfeiltyp nach Ankunfts-Frontalsicht.

Gerade Fortsetzung (Ankunft ≤45° zur Achse) → down-Typ, Pfeil ENTGEGEN der Flucht
(Front schaut die ankommende Person an). Echter Abzweig (>45°) → gerichteter
links/rechts-Block, der den Weg zeigt. Ohne Ankunftsvektor (|in|<1) → down-Fallback.
Belegt Mollgasse-GT (Podest-RZ überwiegend „unten"); EINE Quelle für gang/stgh.
"""
from notbeleuchtung.platzierung.bausteine import (
    frontalsicht_block,
    ist_abzweig,
    rotation_piktogramm_in_raum,
)

# Dedizierte Richtungs-Blöcke wie sie der NormProvider liefert (mit _suffix).
_KEYS = ["notlicht_ks_stiege_unten", "notlicht_ks_stiege_links",
         "notlicht_ks_stiege_rechts"]


def test_ohne_anlauf_ist_down_frontal():
    # Kein Ankunftsvektor (in=0) → down-Fallback, Pfeil entgegen Flucht.
    key, rot, mirror, richtung = frontalsicht_block((0.0, 0.0), (1000.0, 0.0), _KEYS)
    assert richtung == "unten"
    assert key.endswith("_unten")
    assert mirror is False
    assert rot == rotation_piktogramm_in_raum(1000.0, 0.0)   # entgegen der Flucht


def test_gerade_fortsetzung_ist_down():
    # Anlauf kollinear zur Flucht (≤45°) → geradeaus → down-Typ.
    key, _, _, richtung = frontalsicht_block((1000.0, 0.0), (1000.0, 0.0), _KEYS)
    assert richtung == "unten" and key.endswith("_unten")


def test_leichte_schwenkung_bleibt_down():
    # < 45° Schwenkung ist keine Ecke → weiterhin down-Frontal.
    _, _, _, richtung = frontalsicht_block((1000.0, 0.0), (900.0, 100.0), _KEYS)
    assert richtung == "unten"


def test_abzweig_nach_links():
    # Ankunft Nord, Weiterweg West (90°-Ecke) → Richtungspfeil links.
    key, rot, mirror, richtung = frontalsicht_block((0.0, 1000.0), (-1000.0, 0.0), _KEYS)
    assert richtung == "links" and key.endswith("_links")
    assert rot == 0.0 and mirror is False          # gerichteter Block, keine Rotation


def test_abzweig_nach_rechts():
    key, _, _, richtung = frontalsicht_block((0.0, 1000.0), (1000.0, 0.0), _KEYS)
    assert richtung == "rechts" and key.endswith("_rechts")


def test_ist_abzweig_schwelle_45_grad():
    assert ist_abzweig(1000.0, 0.0, 0.0, 1000.0)       # 90° = Ecke
    assert not ist_abzweig(1000.0, 0.0, 1000.0, 0.0)   # kollinear = geradeaus
    assert not ist_abzweig(0.0, 0.0, 1000.0, 0.0)      # kein Einlauf → geradeaus
