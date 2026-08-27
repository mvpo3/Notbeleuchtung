"""keller_geometry.py — mm-genaue Raum-Polygon-Rekonstruktion für Kellergeschosse.

Der bestehende Architektur-Parser liefert für ~60 % der KG-Räume nur einen
Anker-Punkt (``polygon_source == "anchor_only"``), keine Geometrie. Dieses
Modul rekonstruiert die Raum-Umringe **direkt aus den Wandlinien** der DXF:

  1. Wand-Segmente NUR aus den Struktur-Wand-Layern ziehen (02-TWA/TWE/…),
     Bemaßung/HVAC/Hatch/Achsen ignorieren; in mm skalieren
     (``factor_to_mm`` aus dem Parser-Scale).
  2. shapely ``polygonize`` bildet aus den genodeten Segmenten die Faces
     (geschlossene Wand-Umringe = Raum-Kandidaten).
  3. Jeder Raum-Anker wird der kleinsten ihn enthaltenden Face zugeordnet =
     rekonstruiertes Raum-Polygon. Fläche gegen den Plan-Stempel validiert.

Bewusst NUR lesend gegenüber ``architecture_dxf`` (Scale + Anker werden
importiert, nicht verändert). Neue Geometrie-Logik lebt komplett hier.

Bekannte Grenzen (Folge-Slices): Türöffnungen schließen die kleinen Abteile
nicht immer → Gap-Bridging; Wand-MITTE-Umring ist um ~½ Wandstärke größer als
die Lichtfläche (Ratio ~1.05–1.10) → Innen-Offset; 2.KG (Garage) nodet noch
unzureichend.

**User-Marker (Slice F, 2026-07-26):** Wenn die DXF drei Zeichner-Blöcke auf
Layer ``0`` trägt, werden sie ADDITIV in die Wand-Menge gemischt und pro Raum
mit-reportet:
  - ``Raumerkennung``               — nachgezogene Wand-Achsen (Union in Segmente)
  - ``Durchbrüche und Schächte``    — Wanddurchbrüche (kleine geschlossene Polys)
  - ``Deckendurchbrüche und Schächte`` — Deckenschächte

Fehlt ein Block, greift lautlos der alte Pfad.

**Slice I (2026-07-27):** Kombi-Block ``Wand und Deckendurchbrüche`` wird
unterstützt; Schacht-Polys werden per FARBE geroutet (blau=5 → Wand,
grün=3 → Decke, sonst Block-Default). Farbe gewinnt über den Block-Namen.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import math

import ezdxf
from shapely.geometry import LineString, Point, Polygon
from shapely.ops import polygonize, unary_union

from parsers.architecture_dxf import parse_architecture

# Struktur-Wand-Layer nach ADR-0011-Namensschema: 2. Layer-Feld (nach "02-").
WALL_LAYER_FIELDS = frozenset(
    {"TWA", "TWE", "TWB", "ZWA", "ZWE", "AWA", "AWB", "BWA", "WDA", "MWA"}
)

# Zeichner-Blöcke (Layer 0), die manuelle Marker tragen können.
MARKER_BLOCK_WALLS = "Raumerkennung"
MARKER_BLOCK_WALL_SHAFTS = "Durchbrüche und Schächte"
MARKER_BLOCK_CEILING_SHAFTS = "Deckendurchbrüche und Schächte"
MARKER_BLOCK_COMBINED_SHAFTS = "Wand und Deckendurchbrüche"
# Farb-Konvention des Zeichners (Slice I): Blau = Wand-, Grün = Decken-
# Durchbruch. Farbe gewinnt über den Block-Namen; andere Farben fallen auf
# den Block-Default zurück (alte Drei-Block-DXFs bleiben kompatibel).
_COLOR_WALL_SHAFT = 5     # blau
_COLOR_CEILING_SHAFT = 3  # grün
_ARC_CHORD_DEG = 5.0  # ARC → Sehnen-Polylinie, ~5° pro Segment (glatt genug).

# Fidelity-Schwellen für die Flächen-Validierung (Polygon vs. Stempel).
_RATIO_HIGH = (0.85, 1.25)

# Zonen-Stempel (Slice K/L): Labels OHNE eigene Wände auf KG-Ebene
# (Methodik R7). Können nie über Faces matchen → fidelity="zone", aus der
# high/coarse/unmatched-Wertung ausgenommen. DOPPELPARKER deckt auch
# GRUBE/LUFTRAUM-Varianten, GARAGE auch GARAGENRAMPE. INNENHOF = Hof-Stempel
# ÜBER dem Keller (Slice L: war 2× pro KG der "rote X"-Unmatched-Fall —
# identische Label-Flächen in KG1+KG2, Umgebung ohne Wand-Geometrie).
# GULLY = Entwässerungs-Bereichsstempel (Bodenfläche mit Gefälle, keine
# Wände). ER-GESAMT = Summen-Stempel über alle Einlagerungsräume eines
# Traktes (parse_er_numbers liefert dafür schon []) — Aggregat, kein Raum.
_ZONE_TOKENS = ("GARAGE", "DOPPELPARKER", "INNENHOF", "GULLY", "ER-GESAMT")


def _zone_match(name: str, tokens: tuple[str, ...]) -> bool:
    """Zone-Token-Match: Substring; ``=``-Präfix = exakter Name (Slice R1 —
    ``=L`` für Barawitzka-Luftraum-Stempel; Substring "L" träfe alles)."""
    up = (name or "").strip().upper()
    for tok in tokens:
        if tok.startswith("="):
            if up == tok[1:]:
                return True
        elif tok in up:
            return True
    return False


def is_zone(name: str) -> bool:
    return _zone_match(name, _ZONE_TOKENS)


@dataclass
class RoomGeometry:
    name: str
    er_numbers: list[int]
    anchor_xy: tuple[float, float]
    label_area_m2: float
    polygon_mm: list[tuple[float, float]] | None
    polygon_area_m2: float | None
    area_ratio: float | None
    fidelity: str            # high | coarse | unmatched | zone
    wall_shafts_mm: list[list[tuple[float, float]]] | None = None
    ceiling_shafts_mm: list[list[tuple[float, float]]] | None = None
    refined: bool = False    # True = Polygon aus Stempel-Suche (Slice N1)


def is_wall_layer(layer: str) -> bool:
    parts = str(layer or "").split("-")
    return len(parts) > 1 and parts[1].upper() in WALL_LAYER_FIELDS


def _is_hid_layer_default(layer: str) -> bool:
    parts = str(layer or "").split("-")
    return len(parts) > 1 and parts[1].upper() == "HID"


@dataclass(frozen=True)
class KellerVocab:
    """KG-Rekonstruktions-Vokabular eines Projekts (Slice N3).

    Kommt aus der optionalen ``keller:``-Sektion des Layer-Profils
    (``wall_layer_patterns``/``hid_layer_patterns`` = Regex-Listen,
    ``zone_tokens`` = Stempel-Substrings). Ohne Sektion greift der
    Mollgasse-Default: Feld-basiertes ``is_wall_layer`` (2. Layer-Feld in
    ``WALL_LAYER_FIELDS``), ``02-HID``-Feld, ``_ZONE_TOKENS`` — exakt die
    Vor-N3-Semantik, kein Regex-Drift.
    """
    wall_patterns: tuple[re.Pattern, ...] = ()
    hid_patterns: tuple[re.Pattern, ...] = ()
    zone_tokens: tuple[str, ...] = _ZONE_TOKENS

    def is_wall(self, layer: str) -> bool:
        lay = str(layer or "")
        if not self.wall_patterns:
            return is_wall_layer(lay)
        return any(p.search(lay) for p in self.wall_patterns)

    def is_hid(self, layer: str) -> bool:
        lay = str(layer or "")
        if not self.hid_patterns:
            return _is_hid_layer_default(lay)
        return any(p.search(lay) for p in self.hid_patterns)

    def is_zone(self, name: str) -> bool:
        return _zone_match(name, self.zone_tokens)


DEFAULT_VOCAB = KellerVocab()


def keller_vocab_for(profile_id: str) -> KellerVocab:
    """Vocab aus dem Layer-Profil; ohne ``keller:``-Sektion → Default."""
    from parsers.layer_profiles import load_profile
    section = load_profile(profile_id).keller
    if not section:
        return DEFAULT_VOCAB
    return KellerVocab(
        wall_patterns=tuple(
            re.compile(p) for p in section.get("wall_layer_patterns") or []),
        hid_patterns=tuple(
            re.compile(p) for p in section.get("hid_layer_patterns") or []),
        zone_tokens=tuple(
            str(t).upper() for t in section.get("zone_tokens") or _ZONE_TOKENS),
    )


def _er_numbers(name: str) -> list[int]:
    up = (name or "").strip().upper()
    if not up.startswith("ER") or "GESAMT" in up:
        return []
    # Fischamender-Konvention "ER <BT>.<NN>" (z.B. "ER 1.05"): Abteil-Nummer
    # ist der NN-Teil; der BT-Präfix bleibt im Label (ein DXF = ein Bauteil).
    dot = re.match(r"^ER[\s\-]*(\d+)\.(\d+)$", up)
    if dot:
        return [int(dot.group(2))]
    m = re.match(r"^ER[\s\-]*([0-9+\s]+)", up)
    return [int(n) for n in re.findall(r"\d+", m.group(1))] if m else []


def extract_wall_segments(
    dxf_path: str | Path, factor_to_mm: float, include_markers: bool = True,
    vocab: KellerVocab | None = None,
) -> list[tuple[tuple[float, float], tuple[float, float]]]:
    """LINE + explodierte (LW)POLYLINE der Wand-Layer, skaliert nach mm.

    ``include_markers=True`` mischt zusätzlich die User-Wandmarker aus dem
    ``Raumerkennung``-Block ein (falls vorhanden) — jede Zeichner-Polylinie
    wird zu Segmenten zerlegt, ARCs als Sehnen-Polys approximiert.
    ``vocab`` (Slice N3) = projekt-spezifisches Wand-Layer-Vokabular;
    ``None`` = Mollgasse-Default.
    """
    voc = vocab or DEFAULT_VOCAB
    doc = ezdxf.readfile(str(dxf_path))
    msp = doc.modelspace()
    f = float(factor_to_mm)
    segs: list[tuple[tuple[float, float], tuple[float, float]]] = []
    for e in msp:
        if not voc.is_wall(e.dxf.layer):
            continue
        t = e.dxftype()
        if t == "LINE":
            a = (e.dxf.start.x * f, e.dxf.start.y * f)
            b = (e.dxf.end.x * f, e.dxf.end.y * f)
            if a != b:
                segs.append((a, b))
        elif t == "LWPOLYLINE":
            pts = [(p[0] * f, p[1] * f) for p in e.get_points()]
            segs.extend(_polyline_segments(pts, bool(e.closed)))
        elif t == "POLYLINE":
            try:
                pts = [(v.dxf.location.x * f, v.dxf.location.y * f) for v in e.vertices]
            except Exception:
                continue
            segs.extend(_polyline_segments(pts, bool(getattr(e, "is_closed", False))))

    if include_markers:
        markers = extract_marker_geometry(dxf_path, f, _doc=doc)
        segs.extend(markers["wall_segments"])
        segs.extend(close_marker_gaps(markers["wall_segments"]))
    return segs


def _arc_to_segments(cx: float, cy: float, r: float, start_deg: float,
                     end_deg: float, factor: float
                     ) -> list[tuple[tuple[float, float], tuple[float, float]]]:
    """ARC → gerade Sehnen-Polylinie in mm (Schritt ~_ARC_CHORD_DEG)."""
    if r <= 0:
        return []
    sweep = (end_deg - start_deg) % 360.0
    if sweep == 0:
        sweep = 360.0
    n = max(2, int(math.ceil(sweep / _ARC_CHORD_DEG)))
    pts = []
    for i in range(n + 1):
        a = math.radians(start_deg + sweep * i / n)
        pts.append(((cx + r * math.cos(a)) * factor,
                    (cy + r * math.sin(a)) * factor))
    return _polyline_segments(pts, closed=False)


def extract_marker_geometry(
    dxf_path: str | Path, factor_to_mm: float, _doc=None
) -> dict:
    """Lese die drei User-Marker-Blöcke (falls vorhanden).

    Rückgabe: ``{wall_segments, wall_shafts, ceiling_shafts, present}``.
    ``wall_segments`` = Segmentliste analog ``extract_wall_segments``;
    ``wall_shafts``/``ceiling_shafts`` = Liste von Punktlisten (mm, geschlossene
    Polygone). ``present`` = welche Blöcke tatsächlich existieren.
    """
    doc = _doc if _doc is not None else ezdxf.readfile(str(dxf_path))
    f = float(factor_to_mm)
    wall_segs: list[tuple[tuple[float, float], tuple[float, float]]] = []
    wall_shafts: list[list[tuple[float, float]]] = []
    ceiling_shafts: list[list[tuple[float, float]]] = []
    present: list[str] = []

    def _drain_segments(block, sink_segs):
        for e in block:
            t = e.dxftype()
            if t == "LWPOLYLINE":
                pts = [(p[0] * f, p[1] * f) for p in e.get_points()]
                sink_segs.extend(_polyline_segments(pts, bool(e.closed)))
            elif t == "LINE":
                a = (e.dxf.start.x * f, e.dxf.start.y * f)
                b = (e.dxf.end.x * f, e.dxf.end.y * f)
                if a != b:
                    sink_segs.append((a, b))
            elif t == "ARC":
                sink_segs.extend(_arc_to_segments(
                    e.dxf.center.x, e.dxf.center.y, e.dxf.radius,
                    float(e.dxf.start_angle), float(e.dxf.end_angle), f))

    def _drain_polygons(block, default_sink):
        # Auch OFFENE Polylines akzeptieren (Zeichner lässt U-Formen an der
        # Wand offen) — ≥3 Punkte werden implizit geschlossen (Slice I).
        for e in block:
            if e.dxftype() == "LWPOLYLINE":
                pts = [(p[0] * f, p[1] * f) for p in e.get_points()]
                if len(pts) < 3:
                    continue
                color = int(getattr(e.dxf, "color", 256) or 256)
                if color == _COLOR_WALL_SHAFT:
                    wall_shafts.append(pts)
                elif color == _COLOR_CEILING_SHAFT:
                    ceiling_shafts.append(pts)
                else:
                    default_sink.append(pts)

    if MARKER_BLOCK_WALLS in doc.blocks:
        present.append(MARKER_BLOCK_WALLS)
        _drain_segments(doc.blocks[MARKER_BLOCK_WALLS], wall_segs)
    if MARKER_BLOCK_WALL_SHAFTS in doc.blocks:
        present.append(MARKER_BLOCK_WALL_SHAFTS)
        _drain_polygons(doc.blocks[MARKER_BLOCK_WALL_SHAFTS], wall_shafts)
    if MARKER_BLOCK_CEILING_SHAFTS in doc.blocks:
        present.append(MARKER_BLOCK_CEILING_SHAFTS)
        _drain_polygons(doc.blocks[MARKER_BLOCK_CEILING_SHAFTS], ceiling_shafts)
    if MARKER_BLOCK_COMBINED_SHAFTS in doc.blocks:
        present.append(MARKER_BLOCK_COMBINED_SHAFTS)
        _drain_polygons(doc.blocks[MARKER_BLOCK_COMBINED_SHAFTS], wall_shafts)

    return {
        "wall_segments": wall_segs,
        "wall_shafts": wall_shafts,
        "ceiling_shafts": ceiling_shafts,
        "present": present,
    }


def _polyline_segments(pts, closed):
    out = []
    for i in range(len(pts) - 1):
        if pts[i] != pts[i + 1]:
            out.append((pts[i], pts[i + 1]))
    if closed and len(pts) > 2 and pts[0] != pts[-1]:
        out.append((pts[-1], pts[0]))
    return out


# Endpunkt-Snapping schließt Zeichen-Ungenauigkeits-Lücken (Wand-Enden, die sich
# knapp verfehlen), damit die kleinen Abteil-Umringe polygonize-fähig werden.
# 50 mm = Messungs-Sweet-Spot (KG1: 12 → 19 ER high-fidelity).
DEFAULT_SNAP_GRID_MM = 50.0


def snap_segments(segments, grid_mm: float):
    """Runde Segment-Endpunkte auf ein Gitter → nahe Enden fallen zusammen."""
    if grid_mm <= 0:
        return list(segments)
    def r(v):
        return round(v / grid_mm) * grid_mm
    out = []
    for a, b in segments:
        A = (r(a[0]), r(a[1]))
        B = (r(b[0]), r(b[1]))
        if A != B:
            out.append((A, B))
    return out


# Loop-Closure für Marker (Slice H): User-Polylines schließen teils >50 mm
# neben dem Nachbar-Ende → 50er-Snap greift nicht. Statt globales Grid hoch:
# offene Marker-Enden gezielt brücken. 200 mm deckt die KG1-Gaps ab.
DEFAULT_MARKER_GAP_TOL_MM = 200.0


def close_marker_gaps(
    segments,
    tol_mm: float = DEFAULT_MARKER_GAP_TOL_MM,
    node_grid_mm: float = DEFAULT_SNAP_GRID_MM,
) -> list[tuple[tuple[float, float], tuple[float, float]]]:
    """Brücke offene Marker-Enden, die sich knapp verfehlen (Slice H).

    Ein Endpunkt gilt als offen (dangling), wenn sein Node im
    ``node_grid_mm``-Raster von genau einem Segment berührt wird. Gebrückt
    wird NUR ein Paar, das sich gegenseitig als nächstes offenes Ende hat
    und ≤ ``tol_mm`` auseinanderliegt — verhindert False-Bridges quer durch
    Türöffnungen. Rückgabe: neue Bridge-Segmente (Original-Koordinaten).
    """
    if tol_mm <= 0 or not segments:
        return []
    grid = node_grid_mm if node_grid_mm > 0 else 1.0

    def key(p):
        return (round(p[0] / grid) * grid, round(p[1] / grid) * grid)

    degree: dict[tuple[float, float], int] = {}
    for a, b in segments:
        for p in (a, b):
            degree[key(p)] = degree.get(key(p), 0) + 1

    dangling: list[tuple[float, float]] = []
    seen: set[tuple[float, float]] = set()
    for a, b in segments:
        for p in (a, b):
            k = key(p)
            if degree[k] == 1 and k not in seen:
                seen.add(k)
                dangling.append(p)

    def nearest(i: int, used: set[int]) -> tuple[int | None, float | None]:
        best_j, best_d = None, None
        px, py = dangling[i]
        for j, (qx, qy) in enumerate(dangling):
            if j == i or j in used:
                continue
            d = math.hypot(px - qx, py - qy)
            if best_d is None or d < best_d:
                best_j, best_d = j, d
        return best_j, best_d

    bridges = []
    used: set[int] = set()
    for i in range(len(dangling)):
        if i in used:
            continue
        j, d = nearest(i, used)
        if j is None or d is None or d > tol_mm or d <= 0:
            continue
        j_back, _ = nearest(j, used)
        if j_back == i:                      # mutual-nearest → sichere Brücke
            bridges.append((dangling[i], dangling[j]))
            used.add(i)
            used.add(j)
    return bridges


def build_faces(segments, snap_grid_mm: float = 0.0) -> list[Polygon]:
    """Genode die Wand-Segmente und bilde die Polygon-Faces (Raum-Kandidaten).

    ``snap_grid_mm`` schließt vorab kleine Endpunkt-Lücken (0 = aus).
    Default ist AUS: der Engine-Parse-Pfad (``unit_faces``, seit 1.16.0)
    ruft ohne Argument und erwartet rohes ``polygonize(unary_union)`` —
    der KG-Pfad (``reconstruct_rooms``) übergibt sein Snap-Grid explizit
    (Merge-Abstimmung Fenster 1↔2, 31.07.2026).
    """
    if not segments:
        return []
    snapped = snap_segments(segments, snap_grid_mm)
    # Slice R5.b: exakte Duplikate raus, BEVOR unary_union rechnet —
    # Layer-Spiegel (Barawitzka "Icon_1_"/"Icon_3_" duplizieren jede Wand
    # ×3) machten polygonize auf Regelgeschossen unrechenbar (>9 min).
    # Kanonische Richtung (kleinerer Punkt zuerst) fängt auch gespiegelte
    # Doppel. Ergebnis-identisch: union hätte sie ohnehin verschmolzen.
    seen: set[tuple] = set()
    unique = []
    for a, b in snapped:
        key = (a, b) if a <= b else (b, a)
        if key in seen:
            continue
        seen.add(key)
        unique.append((a, b))
    lines = [LineString([a, b]) for a, b in unique]
    return list(polygonize(unary_union(lines)))


# Innen-Offset: die Faces liegen auf der WAND-MITTE, die Lichtfläche ist um
# ~½ Wandstärke kleiner. 40 mm (= ~80 mm Trennwand, BAB Metall-Systemtrennwände)
# bringt den Median-Ratio der Abteile von ~1.08 auf ~1.00 (kalibriert Slice C).
DEFAULT_INNER_OFFSET_MM = 40.0


def inner_offset(polygon: Polygon, offset_mm: float) -> Polygon | None:
    """Schrumpfe ein Face um ``offset_mm`` nach innen → Wand-Innen-Umring.

    Gibt None zurück, wenn der Raum dabei degeneriert (leer); bei Zerfall in
    mehrere Teile wird das größte Teil-Polygon behalten.
    """
    if offset_mm <= 0:
        return polygon
    shrunk = polygon.buffer(-offset_mm, join_style=2)
    if shrunk.is_empty:
        return None
    if shrunk.geom_type == "MultiPolygon":
        shrunk = max(shrunk.geoms, key=lambda g: g.area)
    return shrunk


def _classify(ratio: float | None, matched: bool) -> str:
    if not matched:
        return "unmatched"
    if ratio is not None and _RATIO_HIGH[0] <= ratio <= _RATIO_HIGH[1]:
        return "high"
    return "coarse"


def _assign_shafts(anchor: Point, room_poly: Polygon | None,
                   shafts_poly: list[Polygon]) -> list[list[tuple[float, float]]]:
    """Ordne Schacht-Polygone dem Raum zu (intersect mit Raum-Umring bzw. Anker-Nähe)."""
    if not shafts_poly:
        return []
    picked: list[list[tuple[float, float]]] = []
    for sp in shafts_poly:
        hit = False
        if room_poly is not None and not room_poly.is_empty:
            hit = room_poly.intersects(sp) or room_poly.buffer(200).contains(sp.centroid)
        else:
            hit = anchor.distance(sp.centroid) < 5000.0
        if hit:
            picked.append([(x, y) for x, y in sp.exterior.coords])
    return picked


def resolve_profile_id(
    dxf_path: str | Path,
    profile_id: str | None,
    allow_generic: bool = False,
) -> str:
    """``profile_id=None`` → Auto-Detection über die N6-Fingerprints.

    Explizite IDs laufen unverändert durch (Default-Verhalten byte-identisch).
    Uneindeutige Detection → ``allow_generic=True`` fällt auf das
    Fallback-Profil ``generic_kg`` zurück (Slice N12, generalisierte
    Muster der gelernten Projekte); sonst ``ValueError`` (kein Raten)."""
    if profile_id is not None:
        return profile_id
    from parsers.layer_profiles import detect_profile_for_dxf
    detected = detect_profile_for_dxf(Path(dxf_path))
    if detected is None:
        if allow_generic:
            return "generic_kg"
        raise ValueError(
            f"Layer-Profil für {Path(dxf_path).name!r} nicht eindeutig "
            "erkennbar — profile_id explizit angeben")
    return detected


def reconstruct_rooms(
    dxf_path: str | Path,
    snap_grid_mm: float = DEFAULT_SNAP_GRID_MM,
    inner_offset_mm: float = DEFAULT_INNER_OFFSET_MM,
    include_markers: bool = True,
    marker_gap_tol_mm: float = DEFAULT_MARKER_GAP_TOL_MM,
    auto_markers: bool = True,
    stamp_refine: bool = True,
    profile_id: str | None = "mollgasse",
) -> tuple[list[RoomGeometry], dict[str, Any]]:
    """Rekonstruiere mm-Raum-Polygone für alle Räume einer KG-DXF.

    ``snap_grid_mm`` = Gap-Bridging-Toleranz (Slice B). ``inner_offset_mm`` =
    Wand-Innen-Offset (Slice C, ½ Wandstärke) → Face-Umring wird zur Lichtfläche.
    ``include_markers`` (Slice F) mischt User-Wandmarker + Schacht-Blöcke ein.
    ``marker_gap_tol_mm`` (Slice H) brückt offene Marker-Enden (0 = aus).
    ``auto_markers`` (Slice J, default AN) mischt SYNTHETISCHE Brücken aus
    dem Original-Plan ein (``parsers.auto_marker``, Methodik R1–R4).
    Additiv zu User-Markern; gemessen verbessert es alle Konfigurationen
    (KG1 21→22, KG2 14→20, mit User-Markern KG1 23→24 / KG2 24→31 high).
    ``stamp_refine`` (Slice N1, default AN) sucht für coarse-Räume per
    Stempel-Fläche nach der korrekten Zerteilung/Vereinigung ihres Faces
    (``parsers.stamp_refine`` — die Zeichner-Methodik als Ziel).
    ``profile_id`` (Slice N3) wählt Layer-Profil + KG-Vokabular
    (``keller:``-Sektion; ohne Sektion Mollgasse-Default). ``None`` →
    Auto-Detection über die N6-Fingerprints; unbekanntes Schema fällt in
    der Pipeline auf ``generic_kg`` zurück (Slice N12).
    Returns (rooms, summary) mit matched/high/coarse/unmatched + Median-Ratio.
    """
    profile_id = resolve_profile_id(dxf_path, profile_id, allow_generic=True)
    vocab = keller_vocab_for(profile_id)
    model = parse_architecture(dxf_path, profile_id=profile_id)
    factor = model.scale.factor_to_mm
    doc = ezdxf.readfile(str(dxf_path))
    base_segments = extract_wall_segments(
        dxf_path, factor, include_markers=False, vocab=vocab)
    markers = extract_marker_geometry(dxf_path, factor, _doc=doc) if include_markers \
        else {"wall_segments": [], "wall_shafts": [], "ceiling_shafts": [], "present": []}
    auto = {"wall_segments": [], "hid_segments": 0, "bridges": 0}
    if auto_markers:
        from parsers.auto_marker import generate_marker_segments
        auto = generate_marker_segments(dxf_path, factor, _doc=doc, vocab=vocab)
    marker_segs = markers["wall_segments"] + auto["wall_segments"]
    bridges = close_marker_gaps(marker_segs, tol_mm=marker_gap_tol_mm)
    segments = base_segments + marker_segs + bridges
    faces = build_faces(segments, snap_grid_mm=snap_grid_mm)

    wall_shafts_poly = [Polygon(p) for p in markers["wall_shafts"] if len(p) >= 3]
    ceil_shafts_poly = [Polygon(p) for p in markers["ceiling_shafts"] if len(p) >= 3]

    rooms: list[RoomGeometry] = []
    room_faces: list[Polygon | None] = []   # Roh-Face pro Raum (für Slice N1)
    profile_polygons = 0
    for r in model.rooms:
        ax, ay = r.anchor.anchor_x_mm, r.anchor.anchor_y_mm
        lab = float(r.anchor.area_m2 or 0.0)
        point = Point(ax, ay)
        # Profil-Polygon-Fast-Path (Slice N4): liefert der Projekt-Parser
        # den Raum-Umring schon explizit (z.B. Barawitzka 815 Raumbegrenzung,
        # polygon_source == closed_polygon_profile), gilt plan-explizite
        # Geometrie vor Rekonstruktion — kein Face-Matching, kein Refine.
        prof_poly = getattr(r, "polygon_mm", None)
        if (getattr(r, "polygon_source", "") == "closed_polygon_profile"
                and prof_poly and len(prof_poly) >= 3):
            poly = Polygon(prof_poly)
            if poly.is_valid and not poly.is_empty:
                profile_polygons += 1
                parea = poly.area / 1e6
                ratio = (parea / lab) if lab > 0 else None
                fid = _classify(ratio, True)
                # Slice R2: Zone-Downgrade im Fast-Path — passt das
                # Plan-Polygon NICHT zum Stempel-Soll UND der Name ist
                # Zone-Token (Fischamender AUFZUG hat ein A_Raeume-
                # Kästchen), ist es Schacht/Aggregat, kein Raum. Ein
                # BALKON mit stimmigem Polygon bleibt dagegen high.
                if fid != "high" and vocab.is_zone(r.anchor.name):
                    room_faces.append(None)
                    rooms.append(RoomGeometry(
                        name=r.anchor.name.strip(), er_numbers=[],
                        anchor_xy=(ax, ay), label_area_m2=lab,
                        polygon_mm=None, polygon_area_m2=None,
                        area_ratio=None, fidelity="zone",
                        wall_shafts_mm=_assign_shafts(
                            point, None, wall_shafts_poly),
                        ceiling_shafts_mm=_assign_shafts(
                            point, None, ceil_shafts_poly)))
                    continue
                room_faces.append(None)
                rooms.append(RoomGeometry(
                    name=r.anchor.name.strip(),
                    er_numbers=_er_numbers(r.anchor.name),
                    anchor_xy=(ax, ay), label_area_m2=lab,
                    polygon_mm=[(x, y) for x, y in poly.exterior.coords],
                    polygon_area_m2=parea, area_ratio=ratio,
                    fidelity=fid,
                    wall_shafts_mm=_assign_shafts(point, poly, wall_shafts_poly),
                    ceiling_shafts_mm=_assign_shafts(point, poly, ceil_shafts_poly)))
                continue
        # Zone-Stempel ohne (passendes) Plan-Polygon: Garage, Outdoor,
        # Summen-Stempel — kein Wand-Einschluss zu erwarten.
        if vocab.is_zone(r.anchor.name):
            room_faces.append(None)
            rooms.append(RoomGeometry(
                name=r.anchor.name.strip(), er_numbers=[],
                anchor_xy=(ax, ay), label_area_m2=lab, polygon_mm=None,
                polygon_area_m2=None, area_ratio=None, fidelity="zone",
                wall_shafts_mm=_assign_shafts(point, None, wall_shafts_poly),
                ceiling_shafts_mm=_assign_shafts(point, None, ceil_shafts_poly)))
            continue
        containing = [fc for fc in faces if fc.contains(point)]
        room_poly: Polygon | None = None
        if containing:
            face = min(containing, key=lambda fc: fc.area)
            room_faces.append(face)
            clear = inner_offset(face, inner_offset_mm) if inner_offset_mm > 0 else face
            if clear is None or clear.is_empty:
                clear = face  # degeneriert → Wandmitte behalten
            poly = [(x, y) for x, y in clear.exterior.coords]
            parea = clear.area / 1e6
            ratio = (parea / lab) if lab > 0 else None
            room_poly = clear
            rooms.append(RoomGeometry(
                name=r.anchor.name.strip(), er_numbers=_er_numbers(r.anchor.name),
                anchor_xy=(ax, ay), label_area_m2=lab, polygon_mm=poly,
                polygon_area_m2=parea, area_ratio=ratio,
                fidelity=_classify(ratio, True),
                wall_shafts_mm=_assign_shafts(point, room_poly, wall_shafts_poly),
                ceiling_shafts_mm=_assign_shafts(point, room_poly, ceil_shafts_poly)))
        else:
            room_faces.append(None)
            rooms.append(RoomGeometry(
                name=r.anchor.name.strip(), er_numbers=_er_numbers(r.anchor.name),
                anchor_xy=(ax, ay), label_area_m2=lab, polygon_mm=None,
                polygon_area_m2=None, area_ratio=None, fidelity="unmatched",
                wall_shafts_mm=_assign_shafts(point, None, wall_shafts_poly),
                ceiling_shafts_mm=_assign_shafts(point, None, ceil_shafts_poly)))

    refine_stats = {"attempted": 0, "refined": 0, "split": 0, "merged": 0}
    if stamp_refine:
        from parsers.stamp_refine import refine_rooms
        refine_stats = refine_rooms(rooms, room_faces, faces, doc, factor,
                                    inner_offset_mm, vocab=vocab)

    ratios = sorted(x.area_ratio for x in rooms if x.area_ratio is not None)
    median = ratios[len(ratios) // 2] if ratios else None
    summary = {
        "rooms": len(rooms),
        "wall_segments": len(segments),
        "wall_segments_marker": len(markers["wall_segments"]),
        "faces": len(faces),
        "matched": sum(1 for x in rooms if x.fidelity not in ("unmatched", "zone")),
        "high": sum(1 for x in rooms if x.fidelity == "high"),
        "coarse": sum(1 for x in rooms if x.fidelity == "coarse"),
        "unmatched": sum(1 for x in rooms if x.fidelity == "unmatched"),
        "zones": sum(1 for x in rooms if x.fidelity == "zone"),
        "median_area_ratio": round(median, 3) if median else None,
        "profile_id": profile_id,
        "factor_to_mm": factor,
        "snap_grid_mm": snap_grid_mm,
        "inner_offset_mm": inner_offset_mm,
        "marker_blocks_present": markers["present"],
        "marker_bridges": len(bridges),
        "marker_gap_tol_mm": marker_gap_tol_mm,
        "auto_marker_segments": len(auto["wall_segments"]),
        "auto_marker_hid": auto["hid_segments"],
        "auto_marker_bridges": auto["bridges"],
        "wall_shafts_total": len(wall_shafts_poly),
        "ceiling_shafts_total": len(ceil_shafts_poly),
        "profile_polygons": profile_polygons,
        "stamp_refine": refine_stats,
    }
    return rooms, summary
