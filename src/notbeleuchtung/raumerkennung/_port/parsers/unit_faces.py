"""unit_faces — mm-genaue Raum-Polygone aus Wandlinien, für ALLE Geschosse.

Generalisierung von ``keller_geometry`` (KG-spezifisch) auf Wohngeschosse,
gelernt aus dem User-Ground-Truth-Markup (Test/4.Obergeschoß.dxf, Block
"Raumerkennung eine Wohnung plus Terasse": Wand-Trace = wahre Raum-Umringe;
Block "Schächte und Hohlbereiche": anker-lose Klein-Faces = Schächte/
Hohlbereiche, KEINE Räume).

Kern: shapely-polygonize über die Struktur-Wand-Layer → Faces; jeder
Raum-Anker bekommt die kleinste ihn enthaltende Face (flächen-validiert
gegen den Architekten-Stempel). Kleine Faces ohne Anker = Schacht/Hohlraum.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from shapely.geometry import Point, Polygon

from parsers.keller_geometry import build_faces

# Face-Zuordnung: Polygon/Stempel-Ratio-Fenster (Wand-Mitte-Umring ist um
# ~½ Wandstärke größer als die Lichtfläche → bis 1.6 tolerieren).
FACE_RATIO_RANGE = (0.5, 1.6)
# Anker-lose Faces bis zu dieser Fläche gelten als Schacht/Hohlbereich.
VOID_MAX_M2 = 3.0
VOID_MIN_M2 = 0.02

# Slice R3.3 — Policy (User-Entscheid 13.08.): Stiegenhaus/Gang bilden offene
# Zirkulations-Komplexe — R3.2 bewies, dass für sie KEINE Trennkanten
# gezeichnet sind (Split unmöglich). Bleibt so ein Raum nach allen
# Reparatur-Stufen coarse, wird er als eigene Klasse "complex" geführt:
# ehrlich getrennt von coarse, Elektro-Bedarf bleibt adressierbar.
# Token-EXAKTER Namens-Match (EINGANG/DURCHGANG dürfen nicht matchen).
_COMPLEX_NAME_TOKENS = {"STGH", "STIEGENHAUS", "TREPPENHAUS", "GANG"}


def _is_complex_name(name: str | None) -> bool:
    tokens = re.split(r"[^A-ZÄÖÜ]+", (name or "").upper())
    return any(t in _COMPLEX_NAME_TOKENS for t in tokens)


@dataclass
class FloorFaces:
    """Rekonstruierte Geometrie eines Geschosses."""
    room_polygons: dict[tuple[float, float], list[tuple[float, float]]]
    room_fidelity: dict[tuple[float, float], str]  # high|coarse|none|zone|complex
    voids: list[list[tuple[float, float]]] = field(default_factory=list)
    stats: dict[str, Any] = field(default_factory=dict)


def _anchor_key(x: float, y: float) -> tuple[float, float]:
    return (round(x, 1), round(y, 1))


def _opening_closures(openings: list, default_width: float = 1000.0):
    """Schließ-Segmente über Tür-/Fenster-Öffnungen.

    Kern-Lektion aus dem User-Markup: der Hand-Trace schließt jede Öffnung
    entlang der Wand — ohne diese Brücken zerfallen die Raum-Umringe beim
    polygonize in Wand-Slivers. Segment = Öffnungs-Achse (Position ± ½ Breite
    in Block-Rotation), plus Quersegment als Fallback für gedrehte Blöcke.
    """
    import math as _m
    segs = []
    for o in openings:
        x, y = o.position_mm[:2]
        w = (getattr(o, "width_mm", None) or default_width) * 1.25
        rad = _m.radians(getattr(o, "rotation_deg", 0.0) or 0.0)
        for ang in (rad, rad + _m.pi / 2.0):
            dx, dy = _m.cos(ang) * w / 2.0, _m.sin(ang) * w / 2.0
            segs.append(((x - dx, y - dy), (x + dx, y + dy)))
    return segs


# Slice 1.29.0: 25→40 — Verschluss-Enden der Regelgeschoss-ASR/VR-Türen
# liegen 30–37.5 mm neben der Wandlinie (Messung 1.OG); 40 hebt 7 Räume
# coarse→high (Flip-Audit: 0 down), 50 bringt nichts mehr (Plateau).
_TOUCH_MM = 40.0        # Endpunkt gilt als angebunden, wenn ≤ so nah an Fremdsegment
_BRIDGE_MAX_MM = 2200.0  # freies Wand-Ende → nächste Gegenwand (Tür-/Laibungsbreite)
_CAP_MAX_MM = 450.0      # Kavitäten-Kappe: Endpunkt → nächste PARALLELE Wandlinie
_CAP_ANG_TOL_DEG = 15.0
_JAMB_PERP_MAX_MM = 350.0   # Laibungs-Suchband quer zur Öffnung (Wanddicken-Skala)
_JAMB_ANG_TOL_DEG = 10.0
_JAMB_END_TOL_MM = 150.0    # Wand-Ende gilt als Laibung, wenn im Band-Fenster


def _jamb_closures(openings: list, wall_segments: list):
    """Schließt pro Öffnung die Lücken ALLER parallelen Wandlinien im Band.

    Doppellinien-Leak (Pre-Read 1.20.0): der Achsen-Verschluss aus
    ``_opening_closures`` liegt kollinear zu EINER der beiden Wandlinien —
    die Partnerlinie behält eine türbreite Lücke, deren Stummel-Enden durch
    FIL-Kappen als „touched" gelten und nie eine Brücke bekommen. Der Raum
    fließt um das offene Laibungsende (VR+WC+BAD = eine Face).

    Hier: Öffnungs-Band [t0,t1] aus ``hinge_world_mm``/``band_end_world_mm``
    entlang ``wall_unit_xy``; jede annähernd parallele Wandlinie mit
    Endpunkten im Band-Fenster liefert Laibungs-Punkte. Lane-Key kommt aus
    der TRÄGERLINIE des Segments (Winkel + Normal-Offset) — der Tür-Vektor
    ist um Grad-Bruchteile verdreht, Endpunkt-Perp-Quantisierung driftet
    über die Bandlänge und reißt kollineare Enden auseinander. Punktpaar,
    das die Öffnung ÜBERSPANNT → Schließ-Segment exakt auf der Linie."""
    import math as _m

    ang_tol = _m.radians(_JAMB_ANG_TOL_DEG)
    segs = []
    for o in openings:
        h = getattr(o, "hinge_world_mm", None)
        be = getattr(o, "band_end_world_mm", None)
        u = getattr(o, "wall_unit_xy", None)
        if not (h and be and u):
            continue
        ux, uy = u
        norm = _m.hypot(ux, uy)
        if norm < 1e-9:
            continue
        ux, uy = ux / norm, uy / norm
        px, py = -uy, ux
        ox, oy = o.position_mm[:2]
        th = (h[0] - ox) * ux + (h[1] - oy) * uy
        tb = (be[0] - ox) * ux + (be[1] - oy) * uy
        t0, t1 = min(th, tb), max(th, tb)
        if t1 - t0 < 100.0:
            continue
        ang_open = _m.atan2(uy, ux) % _m.pi

        lanes: dict[tuple[int, int],
                    list[tuple[float, tuple[float, float]]]] = {}
        for a, b in wall_segments:
            sdx, sdy = b[0] - a[0], b[1] - a[1]
            slen = _m.hypot(sdx, sdy)
            if slen < 1e-9:
                continue
            ang = _m.atan2(sdy, sdx) % _m.pi
            da = abs(ang - ang_open)
            da = min(da, _m.pi - da)
            if da > ang_tol:
                continue
            snx, sny = -sdy / slen, sdx / slen
            c = ((a[0] + b[0]) / 2.0) * snx + ((a[1] + b[1]) / 2.0) * sny
            key = (round(_m.degrees(ang) / 5.0), round(c / 40.0))
            for pt in (a, b):
                d_perp = (pt[0] - ox) * px + (pt[1] - oy) * py
                if abs(d_perp) > _JAMB_PERP_MAX_MM:
                    continue
                t = (pt[0] - ox) * ux + (pt[1] - oy) * uy
                if t0 - _JAMB_END_TOL_MM <= t <= t1 + _JAMB_END_TOL_MM:
                    lanes.setdefault(key, []).append((t, pt))

        mid = (t0 + t1) / 2.0
        max_len = (t1 - t0) + 2.0 * _JAMB_END_TOL_MM
        for pts in lanes.values():
            if len(pts) < 2:
                continue
            pts.sort(key=lambda x: x[0])
            lo, hi = pts[0], pts[-1]
            # Schließer muss die Öffnung überspannen (Laibung beidseits),
            # sonst zerschneidet er den Raum statt die Lücke zu schließen.
            if lo[0] < mid < hi[0] and 100.0 < hi[0] - lo[0] <= max_len:
                segs.append((lo[1], hi[1]))
    return segs


def _micro_snaps(closure_segs: list, all_segs: list):
    """Nur-Micro-Anbindung (0.01 < d ≤ _TOUCH_MM) für Verschluss-Endpunkte.

    Verschluss-Achsen enden Millimeter NEBEN der parallelen Wandlinie →
    polygonize sieht eine Dangle-Kante und verwirft den ganzen Verschluss.
    Weit-Brücken (``_free_endpoint_bridges``) sind hier tabu: Öffnungs-
    Achsen ragen in den Raum und würden quer durch Räume brücken
    (DG-Regress im Prototyp-Lauf)."""
    from shapely.geometry import LineString, Point as _P
    from shapely.strtree import STRtree

    lines = [LineString([a, b]) for a, b in all_segs]
    tree = STRtree(lines)
    snaps = []
    for a, b in closure_segs:
        for pt in (a, b):
            p = _P(pt)
            best = None
            for li in tree.query(p.buffer(_TOUCH_MM)):
                # eigene Linie überspringen — der Endpunkt liegt immer
                # exakt auf ihr und würde jeden Snap unterdrücken.
                if all_segs[li] in ((a, b), (b, a)):
                    continue
                d = lines[li].distance(p)
                if d <= 0.01:
                    best = "exact"
                    break
                if d <= _TOUCH_MM and (
                        best is None or (best != "exact" and d < best[0])):
                    best = (d, li)
            if isinstance(best, tuple):
                np_ = lines[best[1]].interpolate(lines[best[1]].project(p))
                snaps.append((pt, (np_.x, np_.y)))
    return snaps


def _cavity_caps(segments):
    """Doppellinien-Hohlräume an Wandenden verschließen (Leak-Befund 26.07.).

    Wände sind im Plan Doppellinien; an Tür-Laibungen verläuft der
    Öffnungs-Schließer kollinear mit EINER der beiden Linien — der Endpunkt
    gilt dann als „touched" (d=0) und bekommt nie eine Brücke. Die parallele
    Partnerlinie bleibt offen und der Raum leckt durch den Wand-Hohlraum in
    den Nachbarraum. Kappe: jedes Segment-Ende wird quer zur nächsten
    annähernd PARALLELEN Fremdlinie (≤ _CAP_MAX_MM = Wanddicken-Skala)
    verbunden. Kappen liegen innerhalb der Wanddicke — Raum-Interiors
    können sie nicht zerschneiden."""
    import math as _m

    from shapely.geometry import LineString, Point as _P
    from shapely.strtree import STRtree

    lines = [LineString([a, b]) for a, b in segments]
    angs = [_m.atan2(b[1] - a[1], b[0] - a[0]) % _m.pi for a, b in segments]
    tree = STRtree(lines)
    tol = _m.radians(_CAP_ANG_TOL_DEG)
    caps = []
    for si, (a, b) in enumerate(segments):
        for pt in (a, b):
            p = _P(pt)
            best = None
            for li in tree.query(p.buffer(_CAP_MAX_MM)):
                if li == si:
                    continue
                da = abs(angs[li] - angs[si])
                da = min(da, _m.pi - da)
                if da > tol:
                    continue
                d = lines[li].distance(p)
                if 0.01 < d <= _CAP_MAX_MM and (best is None or d < best[0]):
                    best = (d, li)
            if best is None:
                continue
            np_ = lines[best[1]].interpolate(lines[best[1]].project(p))
            caps.append((pt, (np_.x, np_.y)))
    return caps


def _free_endpoint_bridges(segments):
    """Freie Wand-Enden auf die nächste Gegenwand brücken.

    User-Markup-Lektion: der Hand-Trace schließt jede Öffnung in der
    Wandflucht. Geometrisch: Wand-Endpunkte, die kein anderes Segment
    berühren (Tür-Laibungen), werden mit dem nächstliegenden Punkt eines
    fremden Segments verbunden (≤ 1.4 m = Tür-/Fensteröffnung).

    Micro-Bridge (26.07.): Endpunkte mit 0 < d ≤ _TOUCH_MM galten als
    „angebunden", aber polygonize nodet nur echte Schnitte — der 25-mm-Spalt
    blieb offen und der Raum leckte in die Nachbar-Face. Solche Fast-Berührer
    bekommen jetzt ebenfalls ein Schließ-Segment zum Fußpunkt."""
    from shapely.geometry import LineString, Point as _P
    from shapely.strtree import STRtree

    lines = [LineString([a, b]) for a, b in segments]
    tree = STRtree(lines)
    bridges = []
    for si, (a, b) in enumerate(segments):
        for pt in (a, b):
            p = _P(pt)
            best = None
            micro = None
            for li in tree.query(p.buffer(_BRIDGE_MAX_MM)):
                if li == si:
                    continue
                d = lines[li].distance(p)
                if d <= _TOUCH_MM:
                    if d <= 0.01:  # exakt genodet — nichts zu schließen
                        micro = "exact"
                        break
                    if not isinstance(micro, tuple) or d < micro[0]:
                        micro = (d, li)
                elif d <= _BRIDGE_MAX_MM and (best is None or d < best[0]):
                    best = (d, li)
            if micro == "exact":
                continue
            target = micro if isinstance(micro, tuple) else best
            if target is None:
                continue
            np_ = lines[target[1]].interpolate(lines[target[1]].project(p))
            bridges.append((pt, (np_.x, np_.y)))
    return bridges


def extract_closure_layer_segments(dxf_path: str | Path, profile_id: str,
                                   factor_to_mm: float,
                                   layer_tokens: tuple[str, ...] = ("-ANS-",),
                                   block=None) -> list[tuple]:
    """Zusatz-Segmente von Schließ-Layern (Default: 02-ANS Anschläge).

    Bodentiefe Fensterbänder haben KEINE Wand-Linie — die Fassade existiert
    dort nur als Anschlag-Geometrie. Ohne diese Segmente bleiben alle
    Fassaden-Räume nach außen offen (Debug-Befund 25.07.). Wrapper-aware
    über den Profil-Loader. ``block``: bereits geladener Entity-Container —
    spart den zweiten DXF-Read, wenn der Aufrufer (parse_architecture)
    das Dokument schon offen hat."""
    if block is None:
        from parsers.architecture_dxf import load_architecture_for_profile
        from parsers.layer_profiles import load_profile

        profile = load_profile(profile_id)
        _doc, block = load_architecture_for_profile(Path(dxf_path), profile)
    f = float(factor_to_mm)
    segs: list[tuple] = []
    for e in block:
        layer = str(e.dxf.layer)
        if not any(tok in layer for tok in layer_tokens):
            continue
        t = e.dxftype()
        if t == "LINE":
            a = (e.dxf.start.x * f, e.dxf.start.y * f)
            b = (e.dxf.end.x * f, e.dxf.end.y * f)
            if a != b:
                segs.append((a, b))
        elif t == "LWPOLYLINE":
            pts = [(p[0] * f, p[1] * f) for p in e.get_points("xy")]
            for i in range(len(pts) - 1):
                if pts[i] != pts[i + 1]:
                    segs.append((pts[i], pts[i + 1]))
            if e.closed and len(pts) > 2:
                segs.append((pts[-1], pts[0]))
    return segs


# Slice 1.31.0 — 02-HID-Leichtbauwände: Trennwände (z.B. ASR-Partition
# 1.–3.OG) liegen teils NUR auf 02-HID ("hidden"), nicht auf den Wand-
# Layern → Räume verschmelzen (Verschmelzungs-Trios 2./3.OG). 02-HID trägt
# aber auch Nicht-Wand-Kanten (Dachkanten, Schacht-Marker). Filter:
# Wand-Querschnitt-Signatur = Doppellinien-PAAR (parallel, Abstand im
# Wanddicken-Band, axialer Overlap). Einzelkanten fallen raus. DG ist
# ausgeschlossen (Dachschrägen-Scharen = parallele Paare → zerschneiden
# Räume, Pre-Read-Befund 05.08.).
_HID_LAYER_TOKEN = "02-HID"
_HID_PAIR_ANG_TOL_DEG = 5.0
_HID_PAIR_GAP_MM = (50.0, 500.0)
_HID_PAIR_MIN_OVERLAP_MM = 300.0


def _hid_pair_segments(segs: list[tuple]) -> list[tuple]:
    """Nur 02-HID-Segmente mit parallelem Partner im Wanddicken-Band
    (Abstand 50–500 mm, axialer Overlap ≥300 mm) behalten — die
    Doppellinien-Signatur eines Wand-Querschnitts."""
    import math as _m

    geo = []
    for (x1, y1), (x2, y2) in segs:
        dx, dy = x2 - x1, y2 - y1
        length = _m.hypot(dx, dy)
        geo.append(None if length < 1e-6
                   else ((x1, y1), (dx / length, dy / length), length))
    cos_tol = _m.cos(_m.radians(_HID_PAIR_ANG_TOL_DEG))
    lo_gap, hi_gap = _HID_PAIR_GAP_MM
    keep = []
    for i, gi in enumerate(geo):
        if gi is None:
            continue
        (ox, oy), (ux, uy), li = gi
        for j, gj in enumerate(geo):
            if j == i or gj is None:
                continue
            (px, py), (vx, vy), lj = gj
            if abs(ux * vx + uy * vy) < cos_tol:
                continue
            wx, wy = px - ox, py - oy
            perp = abs(wx * -uy + wy * ux)
            if not (lo_gap <= perp <= hi_gap):
                continue
            t1 = wx * ux + wy * uy
            qx, qy = px + vx * lj - ox, py + vy * lj - oy
            t2 = qx * ux + qy * uy
            overlap = min(max(t1, t2), li) - max(min(t1, t2), 0.0)
            if overlap >= _HID_PAIR_MIN_OVERLAP_MM:
                keep.append(segs[i])
                break
    return keep


def _fidelity_buckets(rooms: list, room_fidelity: dict) -> tuple[
        dict[str, int], dict[str, int], dict[str, int]]:
    """Fidelity-Zählung gesamt + Indoor/Outdoor getrennt.

    Außenflächen (Balkon/Loggia/Terrasse/…) haben keine Wandlinien und
    können prinzipiell keine Face bekommen — sie in der Indoor-Quote
    mitzuzählen verfälscht die Messung nach unten."""
    fidelity_counts: dict[str, int] = {}
    for v in room_fidelity.values():
        fidelity_counts[v] = fidelity_counts.get(v, 0) + 1

    from parsers.architecture_dxf import SPECIAL_SURFACE_ROOM_PATTERNS
    indoor_counts: dict[str, int] = {}
    outdoor_counts: dict[str, int] = {}
    for r in rooms:
        key = _anchor_key(r.anchor.anchor_x_mm, r.anchor.anchor_y_mm)
        fid = room_fidelity.get(key)
        if fid is None:
            continue
        up = (r.anchor.name or "").upper()
        bucket = (outdoor_counts
                  if any(p in up for p in SPECIAL_SURFACE_ROOM_PATTERNS)
                  else indoor_counts)
        bucket[fid] = bucket.get(fid, 0) + 1
    return fidelity_counts, indoor_counts, outdoor_counts


# Slice R3.1 — Subzellen-Vereinigung (Übertragung von stamp_refines
# N1-„Ketten-Vereinigung anker-loser Nachbarn" auf den unit_faces-Pfad):
# Möblierungs-/Einbau-Linien zerteilen manche Räume in Subzellen — der
# Anker sitzt dann in einem Face « Stempel (EG MÜLL 0.32, 1.OG BAD 0.45,
# 4.OG ASR 0.09, DG WC 0.12 …). Anker-lose kanten-adjazente Nachbar-Faces
# werden akkumuliert, bis das Ratio-Band erreicht ist; kein Band-Treffer
# → bleibt coarse (fail-safe, N1-Doktrin).
_SUBCELL_MIN_SHARED_MM = 200.0
_SUBCELL_MAX_STEPS = 6
# Akzeptanz = STRENGES N1-Band (nicht FACE_RATIO_RANGE 0.5–1.6): bis 1.6
# aufzufüllen schluckt fremde Subzellen, deren eigener Anker in einer
# anderen Zelle sitzt (Befund: 3.OG VR fraß +15,75 m² → building_units-
# Gate ROT). 0.85–1.25 = stamp_refine-Konvention.
_SUBCELL_BAND = (0.85, 1.25)


def _merge_underfilled_subcells(faces, underfilled, face_anchor_total,
                                used_faces, room_polygons, room_fidelity):
    from shapely.ops import unary_union as _uu

    lo, hi = _SUBCELL_BAND
    for key, (fi0, stamp) in underfilled.items():
        merged = {fi0}
        area = faces[fi0].area
        for _ in range(_SUBCELL_MAX_STEPS):
            ratio = area / 1e6 / stamp
            if lo <= ratio <= hi:
                break
            # Kandidaten: anker-lose, unbenutzte Faces mit gemeinsamer
            # Kante (>=200 mm) zu irgendeinem Merge-Mitglied.
            best = None
            for fj, face in enumerate(faces):
                if fj in merged or fj in used_faces:
                    continue
                if face_anchor_total.get(fj, 0) > 0:
                    continue
                if area + face.area > hi * stamp * 1e6:
                    continue          # würde übers Band schießen
                shared = 0.0
                for fm in merged:
                    inter = faces[fm].exterior.intersection(face.exterior)
                    shared = max(shared, getattr(inter, "length", 0.0))
                if shared < _SUBCELL_MIN_SHARED_MM:
                    continue
                if best is None or shared > best[0]:
                    best = (shared, fj)
            if best is None:
                break
            merged.add(best[1])
            area += faces[best[1]].area
        ratio = area / 1e6 / stamp
        if not (lo <= ratio <= hi) or len(merged) == 1:
            continue                  # fail-safe: bleibt coarse
        union = _uu([faces[fm] for fm in merged])
        if union.geom_type != "Polygon" or union.is_empty:
            continue
        room_polygons[key] = list(union.exterior.coords)
        room_fidelity[key] = "high"
        used_faces.update(merged)


# Slice R3.2 — Σ-Evidenz-Split: trägt EIN Face mehrere Anker und passt die
# STEMPEL-SUMME zum Face (0.85–1.25), fehlen genau die inneren Trennwände
# (bewiesen 1.OG: Face 10,2 m² = ASR 1,73 + VR 3,41 + BAD 4,72). Dann wird
# NUR in diesem Face mit Kandidaten-Segmenten (Nicht-Annotations-Layer)
# re-polygonisiert; akzeptiert wird ausschließlich, wenn JEDER Anker ein
# EIGENES Subface im strengen Band bekommt (fail-safe, N1-Doktrin).
_SPLIT_MIN_SEG_MM = 300.0
_SPLIT_MIN_SUBFACE_M2 = 0.3


def _split_multianchor_faces(faces, face_best, room_fidelity,
                             room_polygons, used_faces, candidates):
    from shapely import STRtree
    from shapely.geometry import LineString
    from shapely.ops import polygonize as _pz, unary_union as _uu

    lo, hi = _SUBCELL_BAND
    cand_lines = [LineString([a, b]) for a, b in candidates if a != b]
    if not cand_lines:
        return
    tree = STRtree(cand_lines)
    for fi, anchors in face_best.items():
        if any(room_fidelity.get(k) != "coarse" for k, _, _ in anchors):
            continue
        face = faces[fi]
        stamp_sum = sum(s for _, s, _ in anchors)
        if stamp_sum <= 0.3:
            continue
        # Multi-Anker: Σ-Stempel muss zum Face passen (starke Evidenz).
        # Einzel-Anker: Face zu groß ist bereits belegt (ratio > 1.6);
        # die Wand-Sehnen-Disziplin + Band-Akzeptanz sichern den Split
        # (ASR-Fall: fehlende Leichtbauwand existiert als Sehnen-Linie).
        if (len(anchors) >= 2
                and not (lo <= face.area / 1e6 / stamp_sum <= hi)):
            continue          # Σ-Evidenz fehlt → Finger weg
        inner = []
        boundary = face.exterior
        for k in tree.query(face):
            seg = cand_lines[k].intersection(face)
            for g in getattr(seg, "geoms", [seg]):
                if (g.geom_type != "LineString"
                        or g.length < _SPLIT_MIN_SEG_MM):
                    continue
                # Nur WANDARTIGE Sehnen: beide Enden an der Face-Grenze
                # (Trennwand spannt Wand-zu-Wand) — Möbel-/Einbau-Linien
                # enden frei im Raum und würden das Face zu Konfetti
                # zerlegen (kleinstes enthaltendes Subface → Band-Fail).
                c0, c1 = g.coords[0], g.coords[-1]
                from shapely.geometry import Point as _Pt
                if (boundary.distance(_Pt(c0)) > 60.0
                        or boundary.distance(_Pt(c1)) > 60.0):
                    continue
                inner.append(g)
        if not inner:
            continue
        subfaces = [f for f in _pz(_uu([face.exterior] + inner))
                    if f.area > _SPLIT_MIN_SUBFACE_M2 * 1e6]
        if len(subfaces) < len(anchors):
            continue
        assigned: dict = {}
        used_sub: set[int] = set()
        for key, stamp, pt in anchors:
            best = None
            for si, sf in enumerate(subfaces):
                if sf.contains(pt) and (best is None or sf.area < best[0]):
                    best = (sf.area, si, sf)
            if best is None or stamp <= 0.3:
                assigned = {}
                break
            ratio = best[0] / 1e6 / stamp
            if not (lo <= ratio <= hi) or best[1] in used_sub:
                assigned = {}
                break
            used_sub.add(best[1])
            assigned[key] = best[2]
        if not assigned:
            continue          # fail-safe: Face bleibt unangetastet
        for key, sf in assigned.items():
            room_polygons[key] = list(sf.exterior.coords)
            room_fidelity[key] = "high"
        used_faces.add(fi)


def reconstruct_floor_faces(walls: list, rooms: list,
                            doors: list = (), windows: list = (),
                            extra_segments: list = (),
                            split_candidates: list = ()) -> FloorFaces:
    """Faces bauen + Raum-Ankern zuordnen; Rest-Klein-Faces = Schächte.

    ``walls``: geparste WallSegments (start_mm/end_mm — der Parser hat
    Wrapper-Block + Skalierung bereits aufgelöst; keller_geometrys eigener
    DXF-Read sieht Wrapper-Geschosse nicht).
    ``rooms``: geparste Room-Objekte (anchor.anchor_x_mm/…_y_mm, area_m2).
    ``doors``/``windows``: Öffnungen — werden als Schließ-Segmente überbrückt.
    """
    wall_tuples = [(tuple(w.start_mm), tuple(w.end_mm)) for w in walls
                   if tuple(w.start_mm) != tuple(w.end_mm)]
    segments = list(wall_tuples)
    segments += list(extra_segments)
    segments += _cavity_caps(segments)
    segments += _free_endpoint_bridges(segments)
    # Slice 1.20.0: Öffnungs-Verschlüsse + Laibungs-Schließer beider
    # Wandlinien, Enden per Micro-Snap angebunden (sonst Dangle → verworfen).
    openings = list(doors) + list(windows)
    closures = _opening_closures(openings) + _jamb_closures(
        openings, wall_tuples)
    segments += closures
    segments += _micro_snaps(closures, segments)
    faces = [f for f in build_faces(segments) if f.area > VOID_MIN_M2 * 1e6]

    room_polygons: dict[tuple[float, float], list[tuple[float, float]]] = {}
    room_fidelity: dict[tuple[float, float], str] = {}
    used_faces: set[int] = set()
    anchors_per_face: dict[int, int] = {}
    unstamped_keys: dict[tuple[float, float], int] = {}
    # R3.1: Anker-Zählung über ALLE enthaltenden Faces (nicht nur best) —
    # ein Merge-Kandidat darf keinerlei fremden Anker tragen.
    face_anchor_total: dict[int, int] = {}
    underfilled: dict[tuple[float, float], tuple[int, float]] = {}
    # R3.2: pro Face die zugeordneten (zu großen) Anker fürs Σ-Splitting.
    face_best: dict[int, list] = {}

    for r in rooms:
        key = _anchor_key(r.anchor.anchor_x_mm, r.anchor.anchor_y_mm)
        pt = Point(r.anchor.anchor_x_mm, r.anchor.anchor_y_mm)
        stamp = r.anchor.area_m2 or 0.0
        best: tuple[float, int, Polygon] | None = None
        for fi, face in enumerate(faces):
            if not face.contains(pt):
                continue
            face_anchor_total[fi] = face_anchor_total.get(fi, 0) + 1
            if best is None or face.area < best[0]:
                best = (face.area, fi, face)
        if best is None:
            room_fidelity[key] = "none"
            continue
        anchors_per_face[best[1]] = anchors_per_face.get(best[1], 0) + 1
        area_m2 = best[0] / 1e6
        ratio = (area_m2 / stamp) if stamp > 0.3 else None
        if ratio is not None and not (
                FACE_RATIO_RANGE[0] <= ratio <= FACE_RATIO_RANGE[1]):
            # Face viel zu groß (offene Wand → Nachbar-Leak): als coarse
            # markieren, Polygon NICHT übernehmen.
            room_fidelity[key] = "coarse"
            if ratio < FACE_RATIO_RANGE[0]:
                # Face zu KLEIN (Anker in Subzelle) → Merge-Kandidat (R3.1)
                underfilled[key] = (best[1], stamp)
            else:
                # Face zu GROSS → Σ-Split-Kandidat (R3.2)
                face_best.setdefault(best[1], []).append((key, stamp, pt))
            continue
        used_faces.add(best[1])
        room_polygons[key] = list(best[2].exterior.coords)
        if ratio is not None:
            room_fidelity[key] = "high"
        else:
            room_fidelity[key] = "coarse"
            unstamped_keys[key] = best[1]

    # Slice 1.30.0: Stempel-lose Räume (AUFZUG, EG-WC — ratio nicht prüfbar)
    # sind vertrauenswürdig, wenn ihr Face EXKLUSIV ist (kein fremder Anker
    # im selben Face). Geteiltes Face = Leak-Verdacht → bleibt coarse
    # (Messung 03.08.: 16 exklusiv / 4 geteilt, geteilt sind echte Leaks).
    for key, fi in unstamped_keys.items():
        if anchors_per_face.get(fi, 0) == 1:
            room_fidelity[key] = "high"

    # Slice R3.1 — Unterdeckungs-Räume mit anker-losen Nachbar-Subzellen
    # zum Stempel-Band auffüllen (fail-safe: kein Band-Treffer → coarse).
    if underfilled:
        _merge_underfilled_subcells(faces, underfilled, face_anchor_total,
                                    used_faces, room_polygons,
                                    room_fidelity)

    # Slice R3.2 — Multi-Anker-Faces mit Σ-Stempel-Evidenz splitten.
    if face_best and split_candidates:
        _split_multianchor_faces(faces, face_best, room_fidelity,
                                 room_polygons, used_faces,
                                 split_candidates)

    # Slice R3.3 — verbliebene coarse STGH/GANG-Räume = legitime offene
    # Komplexe (Policy statt unmöglicher Geometrie-Split); Reparatur
    # (R3.1/R3.2) hat Vorrang — high bleibt high.
    for r in rooms:
        key = _anchor_key(r.anchor.anchor_x_mm, r.anchor.anchor_y_mm)
        if (room_fidelity.get(key) == "coarse"
                and _is_complex_name(r.anchor.name)):
            room_fidelity[key] = "complex"

    # Alle anker-losen Klein-Faces bleiben Voids — der GT-Block heißt
    # „Schächte und HOHLBEREICHE", Wand-Hohlräume sind legitime Targets.
    # Display-Filterung (Kavitäten-Noise) ist Sache des Renderers.
    voids = []
    for fi, face in enumerate(faces):
        if fi in used_faces:
            continue
        a = face.area / 1e6
        if VOID_MIN_M2 <= a <= VOID_MAX_M2:
            voids.append(list(face.exterior.coords))

    fidelity_counts, indoor_counts, outdoor_counts = _fidelity_buckets(
        rooms, room_fidelity)

    return FloorFaces(
        room_polygons=room_polygons,
        room_fidelity=room_fidelity,
        voids=voids,
        stats={
            "faces_total": len(faces),
            "rooms": len(rooms),
            "fidelity": fidelity_counts,
            "fidelity_indoor": indoor_counts,
            "fidelity_outdoor": outdoor_counts,
            "voids": len(voids),
        },
    )


def room_face_polygon(floor_faces: FloorFaces, room):
    """Rekonstruiertes Polygon für ein Room-Objekt (oder None)."""
    key = _anchor_key(room.anchor.anchor_x_mm, room.anchor.anchor_y_mm)
    return floor_faces.room_polygons.get(key)


# --- KG-Delegation (Slice 1.23.0) ------------------------------------------
# KG-Geschosse haben kaum durchgehende Wand-Traces (fragmentierte Kellerwände,
# Zonen wie GARAGE/INNENHOF) — der generische Pfad schafft dort nur 15 high.
# ``keller_geometry.reconstruct_rooms`` (Marker + auto_marker + stamp_refine)
# schafft auf denselben Floors 27–39 high → KG-Floors delegieren.

_KG_NAME_TOKEN = "kellergescho"
_DG_NAME_TOKEN = "dachgescho"

# keller_geometry-Fidelity → unit_faces-Vokabular. "zone" bleibt eigener
# Bucket (Bereichsstempel ohne Wände: GARAGE, GULLY, ER-GESAMT, …) — auf
# none zu mappen würde sie fälschlich als Rekonstruktions-Lücke zählen.
_KG_FIDELITY_MAP = {"high": "high", "coarse": "coarse",
                    "unmatched": "none", "zone": "zone"}

# Re-Entry-Guard: reconstruct_rooms parst die DXF selbst nochmal
# (parse_architecture → apply_face_polygons → build_floor_faces) — der
# innere Aufruf darf nicht erneut delegieren.
_KG_DELEGATION_ACTIVE = False


def _is_kg_floor(source_path) -> bool:
    return _KG_NAME_TOKEN in Path(str(source_path or "")).name.lower()


def _kg_floor_faces(model) -> FloorFaces:
    """FloorFaces eines KG-Geschosses via ``keller_geometry.reconstruct_rooms``."""
    global _KG_DELEGATION_ACTIVE
    from parsers.keller_geometry import reconstruct_rooms

    _KG_DELEGATION_ACTIVE = True
    try:
        kg_rooms, summary = reconstruct_rooms(model.source_path)
    finally:
        _KG_DELEGATION_ACTIVE = False

    room_polygons: dict[tuple[float, float], list[tuple[float, float]]] = {}
    room_fidelity: dict[tuple[float, float], str] = {}
    voids: list[list[tuple[float, float]]] = []
    seen_shafts: set[tuple] = set()
    for kr in kg_rooms:
        key = _anchor_key(*kr.anchor_xy)
        fid = _KG_FIDELITY_MAP.get(kr.fidelity, "none")
        room_fidelity[key] = fid
        if fid == "high" and kr.polygon_mm:
            room_polygons[key] = [(float(x), float(y))
                                  for x, y in kr.polygon_mm]
        # Schächte sind pro Raum zugeordnet — derselbe Schacht kann in
        # mehreren Räumen auftauchen, daher Koordinaten-Signatur-Dedupe.
        for shaft in ((kr.wall_shafts_mm or [])
                      + (kr.ceiling_shafts_mm or [])):
            sig = tuple(sorted((round(x, 1), round(y, 1)) for x, y in shaft))
            if sig in seen_shafts:
                continue
            seen_shafts.add(sig)
            voids.append([(float(x), float(y)) for x, y in shaft])

    fidelity_counts, indoor_counts, outdoor_counts = _fidelity_buckets(
        model.rooms, room_fidelity)

    return FloorFaces(
        room_polygons=room_polygons,
        room_fidelity=room_fidelity,
        voids=voids,
        stats={
            "faces_total": summary.get("faces"),
            "rooms": len(kg_rooms),
            "fidelity": fidelity_counts,
            "fidelity_indoor": indoor_counts,
            "fidelity_outdoor": outdoor_counts,
            "voids": len(voids),
            "kg_delegation": True,
            "kg_summary": {k: summary.get(k) for k in (
                "high", "coarse", "unmatched", "zones",
                "median_area_ratio", "marker_bridges",
                "auto_marker_segments", "stamp_refine")},
        },
    )


def _split_candidate_segments(dxf_path, profile_id: str,
                              factor_to_mm: float, block=None) -> list:
    """R3.2-Kandidaten: LINE/LWPOLYLINE aller NICHT-Annotations-Layer
    (N1-Konvention „Innen-Kanten beliebiger Nicht-Annotations-Layer")."""
    from parsers.stamp_refine import _is_annotation_layer

    if block is None:
        from parsers.architecture_dxf import load_architecture_for_profile
        from parsers.layer_profiles import load_profile

        profile = load_profile(profile_id)
        _doc, block = load_architecture_for_profile(Path(dxf_path), profile)
    f = float(factor_to_mm)
    segs: list = []
    for e in block:
        if _is_annotation_layer(str(e.dxf.layer or "")):
            continue
        t = e.dxftype()
        if t == "LINE":
            a = (e.dxf.start.x * f, e.dxf.start.y * f)
            b = (e.dxf.end.x * f, e.dxf.end.y * f)
            if a != b:
                segs.append((a, b))
        elif t == "LWPOLYLINE":
            pts = [(p[0] * f, p[1] * f) for p in e.get_points("xy")]
            for i in range(len(pts) - 1):
                if pts[i] != pts[i + 1]:
                    segs.append((pts[i], pts[i + 1]))
    return segs


def build_floor_faces(model, profile_id: str = "mollgasse",
                      block=None) -> FloorFaces:
    """Wandbasierte Face-Rekonstruktion eines Geschosses (Slice 1.12–1.16).

    Einmal pro Geschoss rechnen — ANS-Anschläge schließen Fensterband-
    Fassaden, anker-lose Klein-Faces = Schächte. ``block``: bereits
    geladener Entity-Container (spart DXF-Re-Read im Parse-Pfad).
    KG-Geschosse (Slice 1.23.0) delegieren an ``keller_geometry``."""
    if _KG_DELEGATION_ACTIVE:
        # Innerer parse_architecture aus reconstruct_rooms — Faces dort
        # ungenutzt, leeres Ergebnis statt Rekursion/Doppelarbeit.
        return FloorFaces(room_polygons={}, room_fidelity={},
                          stats={"kg_delegation_inner": True})
    if _is_kg_floor(getattr(model, "source_path", "")):
        return _kg_floor_faces(model)
    extra = []
    src = getattr(model, "source_path", "")
    if src or block is not None:
        try:
            extra = extract_closure_layer_segments(
                src, profile_id, model.scale.factor_to_mm or 1.0,
                block=block)
        except Exception:
            extra = []
        # Slice 1.31.0: 02-HID-Leichtbauwände (Doppellinien-Paare) — nicht
        # im DG (Dachschrägen-Kanten liegen dort ebenfalls auf 02-HID).
        if _DG_NAME_TOKEN not in Path(str(src or "")).name.lower():
            try:
                hid = extract_closure_layer_segments(
                    src, profile_id, model.scale.factor_to_mm or 1.0,
                    layer_tokens=(_HID_LAYER_TOKEN,), block=block)
                extra = list(extra) + _hid_pair_segments(hid)
            except Exception:
                pass
    # Slice R3.2 — Split-Kandidaten (Nicht-Annotations-Segmente): wirken
    # NUR innerhalb akzeptierter Σ-Evidenz-Splits, nie global (der globale
    # Include ist als Sliver-Quelle falsifiziert, docs/SLICE_R3_PREREAD.md).
    split_candidates = []
    if src or block is not None:
        try:
            split_candidates = _split_candidate_segments(
                src, profile_id, model.scale.factor_to_mm or 1.0,
                block=block)
        except Exception:
            split_candidates = []
    return reconstruct_floor_faces(
        model.walls, model.rooms,
        doors=model.all_doors, windows=model.all_windows,
        extra_segments=extra, split_candidates=split_candidates)


# polygon_source-Wert für Räume, deren Polygon durch eine Face ersetzt wurde.
FACE_POLYGON_SOURCE = "unit_face"


def apply_face_polygons(model, profile_id: str = "mollgasse",
                        block=None) -> FloorFaces:
    """``room.polygon_mm`` ← Face-Polygon, wo fidelity=high (Slice 1.16.0).

    high = Anker in kleinster enthaltender Face UND Fläche im Stempel-
    Ratio-Fenster — nur dort ist die Face nachweislich wandgenau. coarse/
    none behalten ihr Raycast-Polygon (wall_bbox/walls_flood/anchor_only).
    Provenance über ``polygon_source`` — Konsumenten unverändert."""
    ff = build_floor_faces(model, profile_id, block=block)
    replaced = 0
    for r in model.rooms:
        # Slice N7: plan-explizite Profil-Polygone (closed_polygon_profile,
        # z.B. Fischamender A_Raeume_ / Barawitzka 815 Raumbegrenzung) NIE
        # durch rekonstruierte Faces ersetzen — N4-Doktrin: plan-explizit >
        # Rekonstruktion. Die Ersetzung galt Raycast-Polygonen (1.16.0).
        if str(getattr(r, "polygon_source", "")).startswith(
                "closed_polygon_profile"):
            continue
        key = _anchor_key(r.anchor.anchor_x_mm, r.anchor.anchor_y_mm)
        if ff.room_fidelity.get(key) != "high":
            continue
        poly = ff.room_polygons.get(key)
        if not poly:
            continue
        r.polygon_mm = [(float(x), float(y)) for x, y in poly]
        r.polygon_source = FACE_POLYGON_SOURCE
        replaced += 1
    ff.stats["polygon_override"] = replaced
    return ff
