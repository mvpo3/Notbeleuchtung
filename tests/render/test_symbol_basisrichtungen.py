"""Guard: _BLOCK_BASE_DEG gegen die ECHTE Block-Geometrie, nicht gegen sich selbst.

Die Basistabelle (symbols/orientation.py) ist eine gemessene Konstante — ein
Tippfehler dort dreht jeden Pfeil im Plan, ohne dass ein Test bricht (alle
Pfeilrichtungs-Tests rechnen mit derselben Tabelle). Dieser Test misst die
Pfeilrichtung neu aus der importierten Library-Geometrie:

  Pfeil-Polygon (7-Eck der HATCH) → Vektor vom BBox-Zentrum zum FLÄCHEN-
  Schwerpunkt. Der Schwerpunkt liegt kopflastig, der Vektor zeigt also in die
  Pfeilrichtung (Betrag ~0.086 Library-Units, Winkelabweichung gemessen ≤2°).

OCS-Falle (bewusst über ezdxf.path.from_hatch gelöst): der Block
'RIVO-RZ-ARR_right' (wie sein historischer Vorgänger) kann eine HATCH mit extrusion=(0,0,-1) tragen. Wer die
Stützpunkte roh liest, misst den Pfeil spiegelverkehrt (Azimut 178° statt 358°)
und „belegt" damit einen Fehler, den es nicht gibt.

NICHT geprüft (bewusst): dass die Pfeilspitze der geometrisch weiteste Punkt
ist (der Schaft-Fuß ist minimal weiter weg), die Piktogramm-Bestandteile
(Männchen/Tür) und die Richtungen der richtungslosen Blöcke. Fehlt die Library
oder ändert sich der Pfeil-Aufbau so, dass kein 7-Eck mehr findbar ist, prüft
`test_basistabelle_invarianten` weiter die Struktur (90°-Raster,
links/rechts-Spiegelsymmetrie, Zentrierung) — dann aber ohne Geometriebezug.
"""
import math

import ezdxf
import ezdxf.bbox
import pytest
from ezdxf import path as ezpath
from shapely.geometry import Polygon

from notbeleuchtung.symbols import library, load_symbol_mapping
from notbeleuchtung.symbols.orientation import _BLOCK_BASE_DEG

TOL_GRAD = 10.0


def _pfeil_polygon(doc, block_name: str) -> list[tuple[float, float]] | None:
    """Das Pfeil-7-Eck der Block-HATCH in WCS (from_hatch löst die OCS auf).

    Die RIVO-Blöcke der Owner-Bibliothek führen das Pfeil-7-Eck teils DOPPELT
    (Umriss-HATCH + Füll-HATCH, gemessen ±0°-identisch) — mehrere Funde sind
    ok, solange alle dieselbe Richtung messen (±5°); sonst uneindeutig → None."""
    gefunden = []
    for e in doc.blocks[block_name]:
        if e.dxftype() != "HATCH":
            continue
        for p in ezpath.from_hatch(e):
            vs: list[tuple[float, float]] = []
            for v in p.flattening(0.02):
                if not vs or math.dist((v.x, v.y), vs[-1]) > 1e-9:
                    vs.append((v.x, v.y))
            if len(vs) > 1 and math.dist(vs[0], vs[-1]) < 1e-9:
                vs.pop()
            if len(vs) == 7:
                gefunden.append(vs)
    if not gefunden:
        return None
    az0 = _gemessener_azimut(gefunden[0])
    if all(_winkel_diff(_gemessener_azimut(g), az0) <= 5.0 for g in gefunden[1:]):
        return gefunden[0]
    return None


def _gemessener_azimut(poly: list[tuple[float, float]]) -> float:
    xs = [x for x, _ in poly]
    ys = [y for _, y in poly]
    c = Polygon(poly).centroid
    dx = c.x - (min(xs) + max(xs)) / 2.0
    dy = c.y - (min(ys) + max(ys)) / 2.0
    return math.degrees(math.atan2(dy, dx)) % 360.0


def _winkel_diff(a: float, b: float) -> float:
    return abs((a - b + 180.0) % 360.0 - 180.0)


@pytest.fixture(scope="module")
def doc_mit_bloecken():
    doc = ezdxf.new("R2018")
    for block in _BLOCK_BASE_DEG:
        try:
            library.import_block(doc, block)
        except (OSError, KeyError, ValueError) as exc:   # pragma: no cover — Library fehlt
            pytest.skip(f"Library-Block {block!r} nicht importierbar: {exc}")
    return doc


@pytest.mark.parametrize("block,basis", sorted(_BLOCK_BASE_DEG.items()))
def test_basis_stimmt_mit_block_geometrie(doc_mit_bloecken, block, basis):
    """Gemessene Pfeilrichtung == hinterlegte Basis (±10°)."""
    poly = _pfeil_polygon(doc_mit_bloecken, block)
    if poly is None:                             # pragma: no cover — Pfeil-Aufbau geändert
        pytest.skip(f"kein eindeutiges Pfeil-7-Eck in {block!r}")
    az = _gemessener_azimut(poly)
    assert _winkel_diff(az, basis) <= TOL_GRAD, (
        f"{block}: Tabelle sagt {basis}°, Geometrie misst {az:.1f}°"
    )


def test_block_ist_auf_extents_zentrum_normalisiert(doc_mit_bloecken):
    """Basispunkt-Konvention: nach import_block liegt das Extents-Zentrum bei (0,0).

    Sonst zeigt der Pfeil zwar richtig, sitzt aber neben dem INSERT-Punkt."""
    for block in _BLOCK_BASE_DEG:
        ext = ezdxf.bbox.extents(doc_mit_bloecken.blocks[block], fast=False)
        assert ext.has_data, block
        assert abs(ext.center.x) < 1e-3 and abs(ext.center.y) < 1e-3, (
            f"{block}: Extents-Zentrum {ext.center} statt (0,0)"
        )


def test_basistabelle_invarianten():
    """Struktur-Invarianten, unabhängig von der Library-Geometrie."""
    assert all(v % 90.0 == 0.0 for v in _BLOCK_BASE_DEG.values()), _BLOCK_BASE_DEG
    assert all(k == k.strip().lower() for k in _BLOCK_BASE_DEG), "Keys nicht normalisiert"

    def _suffix(k: str) -> str:
        # RIVO-Namensschema: ...-down / ...-left / ..._right (Binde-/Unterstrich).
        return k.replace("_", "-").rsplit("-", 1)[-1]

    basen = {_suffix(k): v for k, v in _BLOCK_BASE_DEG.items()}
    assert set(basen) == {"down", "left", "right"}
    assert basen["down"] == 270.0
    # links/rechts sind Gegenrichtungen auf der X-Achse: 180° - Basis.
    assert basen["left"] == (180.0 - basen["right"]) % 360.0
    # Die Registry-Blöcke müssen (lowercase-normalisiert) dieselben Namen tragen
    # wie die Tabelle, sonst greift basis_deg() nie (stiller Rückfall auf rot 0).
    bloecke = {e["block_name"].strip().lower() for e in load_symbol_mapping().values()}
    assert set(_BLOCK_BASE_DEG) <= bloecke, set(_BLOCK_BASE_DEG) - bloecke
