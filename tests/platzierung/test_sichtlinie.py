"""plan_rettungszeichen_sichtlinie — Sichtlinien-Regel: RZ an Ausgängen (Basissymbol
'Pfeil nach unten' rotiert zur Tür) + beidseitig an der Wasserscheide, ohne Überproduktion."""
from fakes import FakeNormProvider
from notbeleuchtung.hauptengine.contracts import (
    Ausgang,
    BBox,
    Edge,
    Node,
    RaumModell,
    ZirkulationsGraph,
)
from notbeleuchtung.platzierung.anker_strategy import (
    plan_rettungszeichen_sichtlinie,
    richtung_durch_tuer,
)
from notbeleuchtung.symbols import catalog_keys


def _og() -> RaumModell:
    # Gerader Gang, 2 Stiegenhäuser als Ausgänge (stair_exit) an den Enden.
    return RaumModell(
        floor="1OG", bounds_mm=BBox(min_xy=(0, 3000), max_xy=(20000, 11000)),
        ausgaenge=[Ausgang(id="A", xy_mm=(2000, 6000), typ="stair_exit"),
                   Ausgang(id="B", xy_mm=(18000, 6000), typ="stair_exit")],
        zirkulation=ZirkulationsGraph(
            nodes=[Node(id="A", typ="stair", xy_mm=(2000, 6000)), Node(id="B", typ="stair", xy_mm=(18000, 6000))],
            edges=[Edge(**{"from": "A", "to": "B", "len_mm": 16000})]),
    )


def _eg() -> RaumModell:
    # Zentraler Hauptausgang (final_exit) + 2 Stiegenhäuser als Transit (kein Ausgang).
    return RaumModell(
        floor="EG", bounds_mm=BBox(min_xy=(0, 3000), max_xy=(20000, 11000)),
        ausgaenge=[Ausgang(id="M", xy_mm=(10000, 6000), typ="final_exit")],
        zirkulation=ZirkulationsGraph(
            nodes=[Node(id="A", typ="stair", xy_mm=(2000, 6000)),
                   Node(id="M", typ="exit", xy_mm=(10000, 6000)),
                   Node(id="B", typ="stair", xy_mm=(18000, 6000))],
            edges=[Edge(**{"from": "A", "to": "M", "len_mm": 8000}), Edge(**{"from": "M", "to": "B", "len_mm": 8000})]),
    )


def test_og_stiegenhaus_rotiert_plus_mitte_beidseitig():
    rz = plan_rettungszeichen_sichtlinie(_og(), FakeNormProvider(), max_abstand_mm=12000.0)
    assert len(rz) == 3                                   # 2 Stiegenhaus + 1 Mitte, keine Überproduktion
    assert all(p.kind == "rz" for p in rz)
    by = {p.richtung: p for p in rz}
    assert by["links"].rotation_deg == 270.0             # STGH A: Pfeil-nach-unten zur linken Tür
    assert by["rechts"].rotation_deg == 90.0             # STGH B: zur rechten Tür
    assert "gerade" in by                                # Wasserscheide → beidseitig
    assert by["gerade"].xy_mm[0] == 10000.0              # genau mittig


def test_eg_zentraler_ausgang_konvergent():
    rz = plan_rettungszeichen_sichtlinie(_eg(), FakeNormProvider(), max_abstand_mm=12000.0)
    assert len(rz) == 3
    by = {p.richtung: p for p in rz}
    assert by["unten"].xy_mm[0] == 10000.0 and by["unten"].rotation_deg == 0.0   # zentraler Ausgang ↓ ins Freie
    assert by["rechts"].xy_mm[0] == 2000.0               # STGH A zeigt zur Mitte (rechts)
    assert by["links"].xy_mm[0] == 18000.0              # STGH B zeigt zur Mitte (links)


def test_naht_catalog_keys_gueltig():
    keys = catalog_keys()
    for raum in (_og(), _eg()):
        for p in plan_rettungszeichen_sichtlinie(raum, FakeNormProvider()):
            assert p.catalog_key in keys


def test_ohne_ausgang_leer():
    leer = RaumModell(floor="X", bounds_mm=BBox(min_xy=(0, 0), max_xy=(1, 1)))
    assert plan_rettungszeichen_sichtlinie(leer, FakeNormProvider()) == []


def test_rz_dichte_folgt_erkennungsweite_l_gleich_z_mal_h():
    # Default (kein max_abstand): l = z·h. Hinterleuchtet, h=0.15 → l=30 m > 16-m-Gang
    # → KEINE Sichtlinien-Füllung, nur die 2 Stiegenhaus-RZ (norm-korrekt, keine Überprod.).
    rz = plan_rettungszeichen_sichtlinie(_og(), FakeNormProvider())
    assert len(rz) == 2
    assert "gerade" not in {p.richtung for p in rz}
    # Kleineres, nur beleuchtetes Pikto → l = 100·0.10 = 10 m < 16 m → Füllung an der
    # Wasserscheide (beidseitig). Weniger Sichtweite → mehr RZ, direkt aus der Norm.
    eng = plan_rettungszeichen_sichtlinie(
        _og(), FakeNormProvider(), piktogramm_hoehe_m=0.10, hinterleuchtet=False
    )
    assert len(eng) == 3
    assert "gerade" in {p.richtung for p in eng}


def test_richtung_durch_tuer_zeigt_durch_die_oeffnung():
    # Übergang vertikaler Arm → Gang: Öffnung oben, Ziel (Gang) darunter → Pfeil ↓.
    assert richtung_durch_tuer((20000.0, 7000.0), (20000.0, 6000.0)) == "unten"
    # Stiegenhaus-Tür rechts vom Stiegenhaus: Ziel (Stiegenhaus) links → Pfeil ←.
    assert richtung_durch_tuer((3000.0, 6000.0), (2000.0, 6000.0)) == "links"
