"""Guard — Rotations-Konvention des unten-Pfeilblocks (Rotationsfix 2026-09-07).

Block-Konvention (selbst verifiziert, docs/REFERENZ_PLATZIERUNG.md §4): der
kanonische Pfeilblock „nach unten" zeigt bei rotation=0 nach −Y (Azimut 270°).
Soll der Pfeil in Azimut A zeigen, gilt rotation = (A + 90) % 360 — dieselbe
Formel wie die Tür-Regel (atan2 + 90°) und die `_ROT`-Tabelle in
`plan_rettungszeichen_sichtlinie`. `richtung_und_rotation` lieferte vorher den
Azimut PUR → jeder is_directional=False-Pfad zeigte 90° falsch (A−90).

ADR-0006 bleibt unberührt: SL-`rotation_deg` ist Optik-Azimut, kein Pfeil.
"""
from notbeleuchtung.platzierung.bausteine import richtung_und_rotation

#: Pfeilrichtung (Azimut °) des unten-Blocks bei rotation=0.
BLOCK_NULL_AZIMUT = 270.0


def _pfeil_azimut(rotation_deg: float) -> float:
    """Finale Welt-Pfeilrichtung des unten-Blocks nach Rotation (DXF-CCW)."""
    return (BLOCK_NULL_AZIMUT + rotation_deg) % 360.0


def test_jede_richtung_zeigt_den_pfeil_in_die_laufrichtung():
    faelle = {
        (1.0, 0.0): ("rechts", 0.0),
        (-1.0, 0.0): ("links", 180.0),
        (0.0, 1.0): ("oben", 90.0),
        (0.0, -1.0): ("unten", 270.0),
    }
    for (dx, dy), (erwartete_richtung, azimut) in faelle.items():
        richtung, rotation = richtung_und_rotation(dx, dy)
        assert richtung == erwartete_richtung
        assert _pfeil_azimut(rotation) == azimut, (
            f"{richtung}: rotation {rotation}° dreht den unten-Block auf "
            f"{_pfeil_azimut(rotation)}° statt {azimut}°"
        )


def test_unten_block_bleibt_unrotiert_am_ausgang():
    # „Ausgang erreicht" = Pfeil raus (−Y) = unten-Block PUR, rotation 0.
    assert richtung_und_rotation(0.0, -1.0) == ("unten", 0.0)


def test_rotationstabelle_explizit():
    # oben→180, rechts→90, links→270, unten→0 (rotation = (Azimut+90) % 360).
    assert richtung_und_rotation(0.0, 1.0)[1] == 180.0
    assert richtung_und_rotation(1.0, 0.0)[1] == 90.0
    assert richtung_und_rotation(-1.0, 0.0)[1] == 270.0
    assert richtung_und_rotation(0.0, -1.0)[1] == 0.0
