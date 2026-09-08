"""Pfeilrichtung — Geometrie-Tests des EINEN Rotationsrahmens (Slice 3.1).

Prüft Winkel/Spiegel-Algebra gegen die GEMESSENEN Block-Basisorientierungen
(Inventar D, 2026-09-07: unten=270°, links=180°, rechts=0° — der rechts-Block
ist ein echter X-Spiegel, PORT_LOG stimmt), nicht Strings. Regression für
Befund 3: „oben" im Fallback rendete als „rechts" (Achsen-Frame 90° statt
unten-Basis-Frame 180°).
"""
import json
import math
from pathlib import Path

import ezdxf
import pytest

from fakes import FakeNormProvider
from notbeleuchtung.hauptengine.contracts import Ausgang, BBox, Raum, RaumModell
from notbeleuchtung.platzierung.bausteine import key_und_rotation
from notbeleuchtung.platzierung.gang_strategy import plan_rettungszeichen_gang
from notbeleuchtung.platzierung.platzierer import NotlichtPlatzierer
from notbeleuchtung.symbols import library, load_symbol_mapping
from notbeleuchtung.symbols.orientation import ZIEL_DEG, basis_deg

FIXTURES = Path(__file__).parents[1] / "fixtures"

ALLE_RICHTUNGS_KEYS = [
    "notlicht_ks_stiege",
    "notlicht_ks_stiege_unten",
    "notlicht_ks_stiege_links",
    "notlicht_ks_stiege_rechts",
]
NUR_FALLBACK = ["notlicht_ks_stiege"]


def _effektive_richtung_deg(catalog_key: str, rotation: float, mirror_x: bool) -> float:
    """Weltwinkel, in den der Pfeil des INSERTs zeigt (Basis → Spiegel → Rotation)."""
    block = load_symbol_mapping()[catalog_key]["block_name"]
    basis = basis_deg(block)
    assert basis is not None, f"{catalog_key}: kein Richtungs-Block"
    eff = (180.0 - basis) % 360.0 if mirror_x else basis
    return (eff + rotation) % 360.0


def _winkel_diff(a: float, b: float) -> float:
    return abs((a - b + 180.0) % 360.0 - 180.0)


@pytest.mark.parametrize("richtung", ["rechts", "oben", "links", "unten"])
@pytest.mark.parametrize("keys", [ALLE_RICHTUNGS_KEYS, NUR_FALLBACK],
                         ids=["direktional", "fallback"])
def test_effektive_richtung_trifft_ziel(richtung, keys):
    key, rotation, mirror_x = key_und_rotation(keys, richtung)
    eff = _effektive_richtung_deg(key, rotation, mirror_x)
    assert _winkel_diff(eff, ZIEL_DEG[richtung]) <= 5.0, (
        f"{richtung}: {key} rot={rotation} mirror={mirror_x} -> {eff}°"
    )


def test_fallback_oben_ist_180_nicht_90():
    """Befund-3-Regression: unten-Basis-Block braucht 180°, der alte Achsen-Frame gab 90°."""
    key, rotation, mirror_x = key_und_rotation(NUR_FALLBACK, "oben")
    assert (key, rotation, mirror_x) == ("notlicht_ks_stiege", 180.0, False)


def test_fallback_spiegelt_nie():
    """Der alte rechts-mirror-Hack (links-Basis-Ära) ist raus — alle Basen sind Blöcke."""
    for richtung in ("rechts", "oben", "links", "unten"):
        _, _, mirror_x = key_und_rotation(NUR_FALLBACK, richtung)
        assert mirror_x is False


def _block_punkte(doc, name: str) -> list[tuple[float, float]]:
    pts: list[tuple[float, float]] = []
    for e in doc.blocks[name]:
        if e.dxftype() == "LWPOLYLINE":
            pts += [(p[0], p[1]) for p in e.get_points("xy")]
        elif e.dxftype() == "LINE":
            pts += [(e.dxf.start.x, e.dxf.start.y), (e.dxf.end.x, e.dxf.end.y)]
    return pts


def test_links_block_ist_x_spiegel_des_rechts_blocks():
    """Library-Zusicherung (PORT_LOG): 'nach rechts' = echter X-Spiegel von 'nach links'."""
    doc = ezdxf.new("R2018")
    links = load_symbol_mapping()["notlicht_ks_stiege_links"]["block_name"]
    rechts = load_symbol_mapping()["notlicht_ks_stiege_rechts"]["block_name"]
    library.import_block(doc, links)
    library.import_block(doc, rechts)
    p_links = _block_punkte(doc, links)
    p_rechts = [(-x, y) for x, y in _block_punkte(doc, rechts)]
    assert p_links and p_rechts
    # Symmetrischer Nächster-Punkt-Abstand (Blöcke sind origin-zentriert normalisiert).
    def max_min_abstand(a, b):
        return max(min(math.hypot(ax - bx, ay - by) for bx, by in b) for ax, ay in a)
    tol = 0.05  # Library-units (Blockgröße 3.13)
    assert max_min_abstand(p_links, p_rechts) < tol
    assert max_min_abstand(p_rechts, p_links) < tol


def test_mapping_nutzt_nur_eine_unten_schreibweise():
    """Duplikat-Guard (Befund 2, historisch): eine kanonische 'nach unten'-Schreibweise."""
    unten_bloecke = {
        e["block_name"] for e in load_symbol_mapping().values()
        if "nach unten" in e["block_name"]
    }
    assert unten_bloecke == {"notbeleuchtung- richtungspfeil nach unten"}
    lib_namen = [n for n in library.load_library().blocks.block_names()
                 if n.strip().lower().endswith("richtungspfeil nach unten")]
    assert len(lib_namen) == 1, f"Duplikat-Blöcke in der Library: {lib_namen}"


def _vertikaler_gang(ausgang_y: float) -> RaumModell:
    poly = [(0.0, 0.0), (2000.0, 0.0), (2000.0, 30000.0), (0.0, 30000.0)]
    return RaumModell(
        floor="V",
        bounds_mm=BBox(min_xy=(0.0, 0.0), max_xy=(2000.0, 30000.0)),
        raeume=[Raum(id="gang1", raum_typ="GANG", polygon_mm=poly, ist_fluchtweg=True)],
        ausgaenge=[Ausgang(id="EXIT", xy_mm=(1000.0, ausgang_y), typ="final_exit")],
    )


def test_gang_fallback_vertikal_zeigt_effektiv_zum_ausgang():
    """End-to-End durch die Strategie: vertikaler Gang, nur Fallback-Key im Fake —
    JEDES RZ zeigt effektiv (Basis+Rotation) in seine deklarierte Richtung."""
    for ausgang_y in (30000.0, 0.0):
        out = plan_rettungszeichen_gang(_vertikaler_gang(ausgang_y), FakeNormProvider())
        assert out
        for p in out:
            if p.richtung not in ZIEL_DEG:
                continue
            eff = _effektive_richtung_deg(p.catalog_key, p.rotation_deg, p.mirror_x)
            assert _winkel_diff(eff, ZIEL_DEG[p.richtung]) <= 5.0, (
                f"ausgang_y={ausgang_y}: {p.richtung} -> {eff}°"
            )


def test_4og_rz_geometrisch_konsistent():
    """DoD am 4OG-Golden: 3 direktionale rechts-RZ (rot 0) + 2 Tür-RZ (#111:
    unten-Block, zur Tür rotiert). Für die direktionalen gilt Basis+Rotation=Ziel;
    die Tür-RZ tragen absichtlich rotation≠0 bei richtung='unten' (Pfeil DURCH die
    Tür — ihre Rotation kommt aus dem Tür-Winkel, nicht aus dem Richtungs-Frame)."""
    data = json.loads((FIXTURES / "raum_modell_4og.json").read_text(encoding="utf-8"))
    erg = NotlichtPlatzierer().place(RaumModell.model_validate(data), FakeNormProvider())
    rz = [p for p in erg.platzierungen if p.kind == "rz"]
    assert len(rz) == 5
    direktional = [p for p in rz if p.catalog_key == "notlicht_ks_stiege_rechts"]
    tuer = [p for p in rz if p.catalog_key == "notlicht_ks_stiege_unten"]
    assert len(direktional) == 3 and len(tuer) == 2
    for p in direktional:
        eff = _effektive_richtung_deg(p.catalog_key, p.rotation_deg, p.mirror_x)
        assert _winkel_diff(eff, ZIEL_DEG[p.richtung]) <= 5.0
    for p in tuer:
        assert p.rotation_deg % 90.0 == 0.0  # 90°-Raster der Tür-Regel
