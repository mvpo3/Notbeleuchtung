"""communal_stgh_strategy — Rettungszeichen entlang der Fluchtweg-Segmente.

Render-freie Adaption der generativen STGH-Logik aus elektro-planer
`backend/diagnostics/inject_communal_stgh.py` (siehe docs/PORT_LOG.md). Die
Original-Version ZEICHNET (ezdxf/insert_symbol/render_layout_pdf); diese Strategy
produziert ausschließlich Contract-B `Platzierung`-Objekte — die Hauptengine
rendert später. Import-Grenze (CLAUDE.md, hart): nur `hauptengine.contracts` +
`platzierung.geometry` + `notbeleuchtung.symbols`, KEIN Render.

Kern-Regel (generativ, KEINE Ground-Truth-Koordinaten):
  1 Rettungszeichen je Fluchtweg-Segment, gesetzt am **Ausgangs-Endpunkt** des
  Segments (`polyline_mm[-1]`). Der RaumModell-Fixture setzt diese Endpunkte an
  die realen RZ-Stellen → Positionen matchen, ohne dass hier etwas hardcodet wird.

Orientierung (`richtung`/`rotation_deg`) folgt der Segment-Laufrichtung
(`polyline_mm[-2] → [-1]`) auf die dominante Achse gerundet (Kardinal 0/90/180/270).
Die exakten Sub-Grad-Rotationen der Referenz (180.1°, 359.7° …) sind
DXF-Extraktions-Artefakte und werden bewusst NICHT reproduziert (Owner-Entscheid:
generativ statt faithful).

Bauteil-/Stromkreis-Zuordnung (AGV-<A|B>-F13) übernimmt die Cluster-Regel des
Originals: liegen die RZ über >20 m gespreizt, teilt die x-Mitte in Bauteil A
(westlich) / B (östlich); F13 = getrennter Sicherheitskreis (EN 1838).
"""
from __future__ import annotations

from notbeleuchtung.hauptengine.contracts import (
    NormProvider,
    Platzierung,
    RaumModell,
)

# Slice 2.46.3 (elektro-planer): Communal-STGH hängt am Allgemeinverteiler (AGV,
# getrennt vom Wohnungszähler). SV = Sicherheitsbeleuchtung, dauergeschaltet → F13.
_AGV_SV_F = 13
# Zwei Bauteile annehmen, wenn die RZ-x-Spanne diese Lücke überschreitet.
_BUILDING_SPREAD_MM = 20000.0


def _richtung_und_rotation(dx: float, dy: float) -> tuple[str, float]:
    """Segment-Laufrichtung → (richtung, rotation_deg), auf die dominante Achse
    gerundet. Pfeil zeigt Richtung Ausgang (= Segment-Endpunkt)."""
    if abs(dx) >= abs(dy):
        return ("rechts", 0.0) if dx >= 0 else ("links", 180.0)
    return ("oben", 90.0) if dy >= 0 else ("unten", 270.0)


def _catalog_key(symbol_katalog_keys: list[str], richtung: str) -> str:
    """Ersten Norm-Katalog-Key wählen; bei richtung 'unten' die _unten-Variante,
    falls die Norm sie anbietet (Down-Pfeil = Ausgang erreicht)."""
    keys = symbol_katalog_keys or ["notlicht_ks_stiege"]
    if richtung == "unten":
        for k in keys:
            if k.endswith("_unten"):
                return k
    return keys[0]


def _building_assigner(x_coords: list[float]):
    """Cluster-Regel A|B aus der x-Verteilung der RZ (Original 2.46.3).
    A = westlich (kleineres x), B = östlich. Ein Cluster → alles A."""
    if x_coords and (max(x_coords) - min(x_coords) > _BUILDING_SPREAD_MM):
        mid = (max(x_coords) + min(x_coords)) / 2.0
        return lambda x: "A" if x < mid else "B"
    return lambda _x: "A"


def plan_rettungszeichen(raum: RaumModell, norm: NormProvider) -> list[Platzierung]:
    """Ein RZ je Fluchtweg-Segment → Contract-B `Platzierung`-Liste (render-frei).

    Leonis fragt die Norm über `fuer_fluchtweg_abschnitt` (parst nie YAML). Position
    = Segment-Ausgangs-Endpunkt; Orientierung/Bauteil generativ (s. Modul-Docstring).
    """
    segmente = raum.zirkulation.segmente
    endpoints: list[tuple[float, float]] = [
        (seg.polyline_mm[-1] if seg.polyline_mm else (0.0, 0.0)) for seg in segmente
    ]
    assign_building = _building_assigner([x for x, _ in endpoints])

    out: list[Platzierung] = []
    for seg, (ex, ey) in zip(segmente, endpoints):
        if not seg.polyline_mm:
            continue
        anf = norm.fuer_fluchtweg_abschnitt(seg)
        # Laufrichtung aus dem letzten Polyline-Schenkel (Vorgänger → Endpunkt).
        px, py = seg.polyline_mm[-2] if len(seg.polyline_mm) >= 2 else (ex, ey)
        richtung, rotation = _richtung_und_rotation(ex - px, ey - py)
        building = assign_building(ex)
        out.append(
            Platzierung(
                xy_mm=(ex, ey),
                catalog_key=_catalog_key(anf.symbol_katalog_keys, richtung),
                rotation_deg=rotation,
                mirror_x=(richtung == "rechts"),
                height_mm=float(anf.montagehoehe_mm),
                kind=anf.klassifikation,
                richtung=richtung,
                circuit_hint=f"AGV-{building}-F{_AGV_SV_F}",
                covers_segment=[seg.segment_id],
                norm_quelle=anf.quelle,
            )
        )
    return out
