"""apartment_clusters — Wohnungs-Clustering für Fremdprojekte (Slice R6).

Mollgasse hat `building_units` (TOP-Stempel-Konvention, Fenster-1-Track) —
Fremdprojekte brauchen ein Äquivalent. Zwei Bausteine (Spec:
docs/SLICE_R6_PREREAD.md):

1. **Wohnungs-Stempel** (Fischamender): ``Top <BT>.<NN>``-Kombi-Stempel
   tragen Wohnungs-ID + Gesamtfläche + Position (sitzen in einem Raum der
   Wohnung). Seit R2 werden sie als Raum-Label gedroppt
   (``_TOP_AGGREGATE_RE``) — hier werden sie EXTRAHIERT.
2. **Tür-Graph-Komponenten**: Raum-Adjazenz über Türen (N2-ARC-Türen +
   N15-Block-Türen) — Kante, wenn eine Tür-Öffnung an ZWEI Raum-Polygonen
   liegt. Gemeinschaftsräume (Treppenhaus, Schleuse, Müllraum, …) werden
   vor der Komponenten-Bildung entfernt; jede Restkomponente = eine
   Wohnung. Validierung: Σ Raumflächen im Band 0.85–1.25 der
   Stempel-Fläche (stamp_refine-Konvention).

Rennweg (keine Wohnungs-Stempel) bekommt synthetische IDs ``W<n>`` —
Validierung dort nur strukturell. Read-only-Diagnose; kein Engine-Konsum
in diesem Slice.
"""
from __future__ import annotations

import math
import re
from dataclasses import dataclass, field

from shapely.geometry import Point, Polygon

# Wohnungs-Stempel-Muster (R2: architecture_dxf._TOP_AGGREGATE_RE ist der
# Drop-Filter; hier das Extraktions-Gegenstück mit ID-Capture).
_TOP_ID_RE = re.compile(r"^\s*(Top\s*[\d.]+)\s*$", re.IGNORECASE)
_AREA_RE = re.compile(r"^\s*(\d{1,4}[.,]\d{1,2})\s*(?:m\s*2|m²|m\^2)?\s*$",
                      re.IGNORECASE)

# Flächen-Band wie stamp_refine (N1): Σ Raumflächen vs. Stempel-Soll.
AREA_BAND = (0.85, 1.25)

# Gemeinschafts-/Nicht-Wohnungs-Räume: vor der Komponenten-Bildung
# entfernen (Substring-Tokens, Taxonomie R4). Track-A-Struktur —
# fachliche Erweiterung via handoff(B) H-18.
COMMON_ROOM_TOKENS: tuple[str, ...] = (
    "TREPPENHAUS", "TRH", "STGH", "SCHLEUSE", "MÜLLRAUM", "MUELLRAUM",
    "WASCHKÜCHE", "WASCHKUECHE", "TECHNIKRAUM", "TECHNIK", "KIWA",
    "FAHRRAD", "FAHRRÄDER", "AUFZUG", "TROCKENRAUM", "NIEDERSP",
    "MEDIENR", "WASSERZ", "HAUSTECHNIK",
)

# Tür-Öffnung ↔ Raum-Polygon: maximale Distanz (Öffnungs-Sehne liegt in
# der Wandmitte, Raum-Polygone sind um inner_offset (~40 mm) geschrumpft;
# 600 mm deckt dicke Außen-/Wohnungstrennwände).
DOOR_ROOM_TOL_MM = 600.0


@dataclass(frozen=True)
class ApartmentStamp:
    apartment_id: str            # "Top 2.06"
    area_m2: float               # Wohnungs-Gesamtfläche laut Stempel
    anchor_xy: tuple[float, float]


@dataclass
class ApartmentCluster:
    apartment_id: str | None     # Stempel-ID oder synthetisch "W<n>"
    room_indices: list[int]      # Indizes in der übergebenen Raum-Liste
    sum_area_m2: float
    stamp: ApartmentStamp | None = None
    band_ok: bool | None = None  # None = kein Stempel (strukturell)
    extra_stamps: list[ApartmentStamp] = field(default_factory=list)


def is_common_room(name: str) -> bool:
    up = (name or "").strip().upper()
    return any(tok in up for tok in COMMON_ROOM_TOKENS)


def wall_segments_from_block_inserts(doc, factor_to_mm: float,
                                     insert_layer_patterns: tuple[str, ...],
                                     ) -> list[tuple[tuple[float, float],
                                                     tuple[float, float]]]:
    """Wand-Segmente aus BLOCK-Inhalten (Slice R6.a — Rennweg-Konvention:
    alle Wand-LINEs stecken in ``Wall_N``-INSERTs auf den Wand-Layern,
    der Modelspace selbst ist leer). base_point-korrekt transformiert
    (Wiederverwendung der N15-Transform-Helfer)."""
    from parsers.door_blocks import _block_base_point, _compose

    pats = tuple(re.compile(p) for p in insert_layer_patterns)
    f = float(factor_to_mm)
    segs: list[tuple[tuple[float, float], tuple[float, float]]] = []
    for ins in doc.modelspace():
        if ins.dxftype() != "INSERT":
            continue
        if not any(p.search(str(ins.dxf.layer)) for p in pats):
            continue
        name = str(ins.dxf.name or "")
        try:
            blk = doc.blocks[name]
        except Exception:
            continue
        tf, _scale = _compose(None, 1.0, ins, _block_base_point(doc, name))
        for e in blk:
            t = e.dxftype()
            if t == "LINE":
                a = tf(e.dxf.start.x, e.dxf.start.y)
                b = tf(e.dxf.end.x, e.dxf.end.y)
                segs.append(((a[0] * f, a[1] * f), (b[0] * f, b[1] * f)))
            elif t == "LWPOLYLINE":
                pts = [tf(p[0], p[1]) for p in e.get_points()]
                for i in range(len(pts) - 1):
                    segs.append(((pts[i][0] * f, pts[i][1] * f),
                                 (pts[i + 1][0] * f, pts[i + 1][1] * f)))
    return segs


# Outdoor-Anhänge (gehören zur Wohnung, verbinden sich aber untereinander
# über Trennbleche, die NICHT im Wand-Layer liegen — Loggia-Ketten würden
# sonst alle Wohnungen eines Riegels verschmelzen).
_OUTDOOR_TOKENS: tuple[str, ...] = ("BALKON", "LOGGIA", "TERRASSE",
                                    "GARTEN", "DACHGARTEN")


def _is_outdoor(name: str) -> bool:
    up = (name or "").strip().upper()
    return any(tok in up for tok in _OUTDOOR_TOKENS)


def extract_apartment_stamps(msp, factor_to_mm: float,
                             label_layer_patterns: tuple[str, ...],
                             ) -> list[ApartmentStamp]:
    """Top-Stempel eines Modelspace: ID-Zeile + m²-Zeile direkt darunter.

    Layout (R2-Befund): "Top 2.09" und die Gesamt-m²-Zeile stehen
    gestapelt (<900 mm), die m²-Zeile UNTER der ID-Zeile.
    """
    import ezdxf  # noqa: F401  (Typ-Kontext; msp kommt von ezdxf)

    pats = tuple(re.compile(p, re.IGNORECASE) for p in label_layer_patterns)
    f = float(factor_to_mm)
    ids: list[tuple[str, float, float]] = []
    areas: list[tuple[float, float, float]] = []
    for e in msp:
        if e.dxftype() not in {"MTEXT", "TEXT"}:
            continue
        layer = str(e.dxf.layer)
        if pats and not any(p.search(layer) for p in pats):
            continue
        raw = e.plain_text() if hasattr(e, "plain_text") else str(
            getattr(e.dxf, "text", ""))
        text = re.sub(r"\s+", " ", str(raw)).strip()
        x = float(e.dxf.insert.x) * f
        y = float(e.dxf.insert.y) * f
        m_id = _TOP_ID_RE.match(text)
        if m_id:
            ids.append((re.sub(r"\s+", " ", m_id.group(1)), x, y))
            continue
        m_area = _AREA_RE.match(text)
        if m_area:
            areas.append((float(m_area.group(1).replace(",", ".")), x, y))

    out: list[ApartmentStamp] = []
    seen: set[str] = set()
    for apt_id, ix, iy in ids:
        best = None
        for a, ax, ay in areas:
            dy = iy - ay          # m²-Zeile UNTER der ID-Zeile → dy > 0
            if abs(ax - ix) <= 700.0 and 0.0 < dy <= 900.0:
                d = math.hypot(ax - ix, ay - iy)
                if best is None or d < best[1]:
                    best = ((a, ax, ay), d)
        if best is None:
            continue
        key = apt_id.upper()
        if key in seen:           # Overlay-Doppel (R1-Muster)
            continue
        seen.add(key)
        (a, ax, ay), _ = best
        out.append(ApartmentStamp(apt_id, a, (ax, ay)))
    return out


def _room_polygons(rooms) -> list[Polygon | None]:
    polys: list[Polygon | None] = []
    for r in rooms:
        if r.polygon_mm and len(r.polygon_mm) >= 3:
            p = Polygon(r.polygon_mm)
            polys.append(p if p.is_valid and not p.is_empty else None)
        else:
            polys.append(None)
    return polys


# Öffnungs-Kante: gemeinsamer Polygon-Kanten-Abschnitt ≥ OPENING_MIN ohne
# Wand-Segment-Deckung. A_Raeume-Polygone sind ACHSmaß (teilen Kanten auch
# durch Wände) — die Unterscheidung Wand vs. Durchgang/Tür liefert erst
# die Wand-Layer-Evidenz: Öffnung = Lücke im Wand-Satz.
ADJ_GAP_MM = 25.0
OPENING_MIN_MM = 600.0        # ≥ Türbreite; filtert Ecken-Kontakte
WALL_COVER_TOL_MM = 100.0     # Sample gilt als wand-gedeckt bei ≤100 mm
_SAMPLE_STEP_MM = 100.0


def _has_open_passage(shared, wall_tree, wall_lines) -> bool:
    """Längster wand-freier Abschnitt der gemeinsamen Kante ≥ OPENING_MIN?

    ``shared`` = Schnitt der gepufferten Boundaries (Polygon-Geometrie);
    gesampelt entlang der Bounding-Diagonale wäre falsch — wir samplen
    die Boundary-Abschnitte selbst.
    """
    geoms = getattr(shared, "geoms", [shared])
    for g in geoms:
        boundary = getattr(g, "exterior", g)
        length = boundary.length
        if length < OPENING_MIN_MM:
            continue
        run = 0.0
        best = 0.0
        d = 0.0
        while d <= length:
            pt = boundary.interpolate(d)
            idxs = wall_tree.query(pt.buffer(WALL_COVER_TOL_MM))
            covered = any(
                wall_lines[k].distance(pt) <= WALL_COVER_TOL_MM
                for k in idxs
            )
            if covered:
                run = 0.0
            else:
                run += _SAMPLE_STEP_MM
                best = max(best, run)
            d += _SAMPLE_STEP_MM
        # Buffer-Schnitt umrundet den Berühr-Streifen → Kantenlänge ≈
        # halbe Umfangslänge; der wandfreie Run entlang einer Seite
        # entspricht der Öffnungsbreite.
        if best >= OPENING_MIN_MM:
            return True
    return False


def cluster_rooms(rooms, door_points: list[tuple[float, float]],
                  wall_segments: list[tuple[tuple[float, float],
                                            tuple[float, float]]],
                  tol_mm: float = DOOR_ROOM_TOL_MM,
                  adj_gap_mm: float = ADJ_GAP_MM,
                  ) -> list[list[int]]:
    """Zusammenhangskomponenten der Wohnungs-Räume.

    Kanten: (a) gemeinsame Polygon-Kante MIT Wand-Lücke ≥ Türbreite
    (deckt Türen UND offene Durchgänge), (b) Tür-Punkte als Zusatz-Kante,
    aber NUR wenn die zwei nächsten Räume ÜBERHAUPT (inkl. Gemeinschafts-
    räume gerechnet) beide eligible sind — sonst verbindet eine
    Wohnungstür (wahrer Partner: das ausgeschlossene Treppenhaus)
    fälschlich zwei fremde Wohnungen. Zonen, Gemeinschaftsräume und
    polygon-lose Räume bleiben außen vor.
    """
    from shapely import STRtree
    from shapely.geometry import LineString

    polys = _room_polygons(rooms)
    with_poly = [i for i in range(len(rooms)) if polys[i] is not None
                 and rooms[i].fidelity != "zone"]
    eligible = [i for i in with_poly if not is_common_room(rooms[i].name)]
    eligible_set = set(eligible)
    parent = {i: i for i in eligible}

    def find(i: int) -> int:
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    def union(a: int, b: int) -> None:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    wall_lines = [LineString([a, b]) for a, b in wall_segments if a != b]
    wall_tree = STRtree(wall_lines) if wall_lines else None

    edges: set[tuple[int, int]] = set()

    # (a) Öffnungs-Kanten — O(n²) mit Bbox-Prefilter (n ≈ 60/Geschoss).
    half = adj_gap_mm / 2.0
    bufs = {i: polys[i].exterior.buffer(half) for i in eligible}
    bounds = {i: bufs[i].bounds for i in eligible}
    if wall_tree is not None:
        for ai in range(len(eligible)):
            i = eligible[ai]
            ix0, iy0, ix1, iy1 = bounds[i]
            for bi in range(ai + 1, len(eligible)):
                j = eligible[bi]
                if _is_outdoor(rooms[i].name) and _is_outdoor(rooms[j].name):
                    continue          # Loggia-Ketten-Sperre
                jx0, jy0, jx1, jy1 = bounds[j]
                if jx0 > ix1 or ix0 > jx1 or jy0 > iy1 or iy0 > jy1:
                    continue
                shared = bufs[i].intersection(bufs[j])
                if shared.is_empty or shared.area < adj_gap_mm * OPENING_MIN_MM / 2:
                    continue
                if _has_open_passage(shared, wall_tree, wall_lines):
                    edges.add((min(i, j), max(i, j)))

    # (b) Tür-Punkte (Zusatz — rekonstruierte Polygonsätze, Barawitzka).
    for dx, dy in door_points:
        pt = Point(dx, dy)
        near = sorted(
            ((polys[i].distance(pt), i) for i in with_poly),
            key=lambda t: t[0],
        )[:2]
        if (len(near) == 2 and near[0][0] <= tol_mm
                and near[1][0] <= tol_mm
                and near[0][1] in eligible_set
                and near[1][1] in eligible_set):
            edges.add((min(near[0][1], near[1][1]),
                       max(near[0][1], near[1][1])))

    # Verteiler-Erkennung: der ÖFFENTLICHE Flur heißt oft auch nur "Gang"
    # (Fischamender) — Namens-Filter greift nicht. Struktur-Signal: ein
    # Raum mit Kanten zu ≥3 VERSCHIEDENEN Vorräumen (VR = Wohnungs-
    # Eingangsraum) ist der Erschließungs-Flur → wie Gemeinschaftsraum
    # behandeln (Raum + seine Kanten raus).
    vr_partners: dict[int, set[int]] = {}
    for i, j in edges:
        for a, b in ((i, j), (j, i)):
            nb = (rooms[b].name or "").strip().upper()
            if nb in {"VR", "VORRAUM"}:
                vr_partners.setdefault(a, set()).add(b)
    public = {i for i, vrs in vr_partners.items()
              if len(vrs) >= 3
              and (rooms[i].name or "").strip().upper() not in {"VR",
                                                                "VORRAUM"}}
    for i, j in edges:
        if i in public or j in public:
            continue
        union(i, j)

    comps: dict[int, list[int]] = {}
    for i in eligible:
        if i in public:
            continue
        comps.setdefault(find(i), []).append(i)
    return sorted(comps.values(), key=lambda c: -len(c))


def assign_apartments(rooms, clusters: list[list[int]],
                      stamps: list[ApartmentStamp],
                      ) -> list[ApartmentCluster]:
    """Cluster ↔ Stempel: Komponente, die den Stempel-Anker enthält
    (bzw. ihm am nächsten liegt), bekommt die Wohnungs-ID; Validierung
    über das Flächen-Band. Ohne Stempel → synthetische ID ``W<n>``."""
    polys = _room_polygons(rooms)

    def cluster_dist(cluster: list[int], pt: Point) -> float:
        return min(polys[i].distance(pt) for i in cluster)

    result = [
        ApartmentCluster(
            apartment_id=None,
            room_indices=list(c),
            # Wohnflächen-Summe = INDOOR only — der Top-Stempel-Soll ist
            # Wohnfläche; Balkon/Loggia/Terrasse/Garten zählen nicht mit.
            sum_area_m2=sum(
                (rooms[i].polygon_area_m2 or 0.0) for i in c
                if not _is_outdoor(rooms[i].name)),
        )
        for c in clusters
    ]
    for stamp in stamps:
        pt = Point(stamp.anchor_xy)
        if not result:
            break
        best = min(result, key=lambda ac: cluster_dist(ac.room_indices, pt))
        if cluster_dist(best.room_indices, pt) > DOOR_ROOM_TOL_MM * 2:
            continue
        if best.stamp is None:
            best.apartment_id = stamp.apartment_id
            best.stamp = stamp
            ratio = (best.sum_area_m2 / stamp.area_m2
                     if stamp.area_m2 > 0 else 0.0)
            best.band_ok = AREA_BAND[0] <= ratio <= AREA_BAND[1]
        else:
            # Zwei Stempel in einer Komponente = Cluster-Verschmelzung
            # (fehlende Tür-Trennung) — ehrlich flaggen, nicht raten.
            best.extra_stamps.append(stamp)
            best.band_ok = False
    n = 0
    for ac in result:
        if ac.apartment_id is None:
            n += 1
            ac.apartment_id = f"W{n}"
    return result
