"""auto_marker — synthetische Raumerkennungs-Segmente aus dem Original-Plan.

Setzt die vom Zeichner gelernte Marker-Methodik (docs/MARKER_METHODIK_KG.md,
R1–R4) programmatisch um, damit künftige Projekte OHNE manuelle Blöcke
auskommen:

  R1  Nachziehen statt erfinden — Quelle sind die vorhandenen Wand-Layer
      (TWA/TWE/…). Verdeckte Kanten (``02-HID``) werden erfasst aber NICHT
      eingemischt: gemessen zersplittern sie die Faces (KG1 21→18 high,
      Median 0.99→0.87) — der Zeichner nutzt sie nur punktuell (7–18
      Segmente), der Layer als Ganzes ist kein Raum-Grenzsignal.
  R2  Topologie reparieren — NUR Brücken-Segmente über Lücken kollinearer
      Fragmente werden erzeugt; die Original-Geometrie wird nie dupliziert
      oder begradigt (begradigte Runs erzeugen Parallel-Sliver → Regression,
      gemessen KG1 21→18 high).
  R3  Türen überzeichnen — türgroße Lücken (≤ ``MAX_DOOR_GAP_MM``) werden
      gebrückt, wenn Tür-Evidenz nahe der Lückenmitte liegt; kleine
      Zeichen-Lücken (≤ ``SMALL_GAP_MM``) brauchen keine Evidenz. Evidenz
      (Slice N2) = TÜR-INSERT ODER geometrisch erkannter Türbogen
      (``parsers.door_arcs``: Bogen + Türblatt, namens-unabhängig).
      Zusätzlich brückt die Bogen-Sehne hinge→band_end nicht-kollineare
      Tür-Öffnungen direkt (``door_chord_bridges``).
  R4  Einzellinien-Wände bleiben unverändert (der 40mm-Offset in
      ``reconstruct_rooms`` macht die Lichtfläche).

Konsum-Pfad identisch zu den User-Markern (Slice F/I): die Segmente werden
additiv in ``reconstruct_rooms`` gemischt → direkt gegen die handmarkierten
Referenz-DXFs (KG1/KG2) validierbar.
"""
from __future__ import annotations

import math
from pathlib import Path

import ezdxf

from parsers.door_arcs import DoorArc, detect_door_arcs
from parsers.keller_geometry import (
    DEFAULT_VOCAB,
    KellerVocab,
    _polyline_segments,
)

# Verdeckte Kanten (02-HID) zählen als Grenz-Kandidat (R1) — der Zeichner
# zieht sie als Raumgrenze durch (KG1: 7, KG2: 18 Marker-Segmente). Das
# HID-Layer-Matching lebt seit N3 im KellerVocab (Profil-Sektion ``keller:``).

# Kollinear-Bins wie die Wall-Run-Fusion: 2°-Winkel, 80mm-Offset.
ANGLE_BIN_DEG = 2.0
OFFSET_BIN_MM = 80.0
# Brücken-Regeln (R2/R3): Zeichen-Lücken bis SMALL_GAP_MM immer schließen;
# darüber bis MAX_DOOR_GAP_MM nur mit TÜR-INSERT in DOOR_EVIDENCE_MM.
SMALL_GAP_MM = 400.0
MAX_DOOR_GAP_MM = 1200.0
DOOR_EVIDENCE_MM = 900.0
# Chord-Brücken (N2): Sehne nur emittieren wenn die Öffnung wirklich offen
# ist (Sehnen-MITTE ≥ EXIST-Toleranz von jeder Wand entfernt) UND beide
# Sehnen-Enden ans Wand-Netz anbinden (fail-safe gegen frei schwebende
# False-Positive-Bögen — Polygonize ignoriert Dangling, aber wir emittieren
# gar nicht erst).
CHORD_EXIST_TOL_MM = 100.0
CHORD_ATTACH_TOL_MM = 200.0

Seg = tuple[tuple[float, float], tuple[float, float]]


def collect_boundary_segments(dxf_path: str | Path, factor_to_mm: float,
                              _doc=None, vocab: KellerVocab | None = None,
                              ) -> tuple[list[Seg], list[Seg]]:
    """(Wand-Layer-Segmente, HID-Segmente) des Modelspace in mm (R1).

    ``vocab`` (Slice N3) = projekt-spezifisches Layer-Vokabular;
    ``None`` = Mollgasse-Default.
    """
    voc = vocab or DEFAULT_VOCAB
    doc = _doc if _doc is not None else ezdxf.readfile(str(dxf_path))
    f = float(factor_to_mm)
    wall_segs: list[Seg] = []
    hid_segs: list[Seg] = []
    for e in doc.modelspace():
        lay = str(e.dxf.layer or "")
        is_hid = voc.is_hid(lay)
        if not (voc.is_wall(lay) or is_hid):
            continue
        sink = hid_segs if is_hid else wall_segs
        t = e.dxftype()
        if t == "LINE":
            a = (e.dxf.start.x * f, e.dxf.start.y * f)
            b = (e.dxf.end.x * f, e.dxf.end.y * f)
            if a != b:
                sink.append((a, b))
        elif t == "LWPOLYLINE":
            pts = [(p[0] * f, p[1] * f) for p in e.get_points()]
            sink.extend(_polyline_segments(pts, bool(e.closed)))
    return wall_segs, hid_segs


def door_positions(dxf_path: str | Path, factor_to_mm: float,
                   _doc=None,
                   door_arcs: list[DoorArc] | None = None,
                   ) -> list[tuple[float, float]]:
    """Tür-Evidenz-Positionen in mm: benannte INSERTs ∪ Bogen-Öffnungsmitten.

    ``door_arcs`` kann vorberechnet übergeben werden (ein Detektor-Lauf pro
    DXF); sonst wird ``detect_door_arcs`` selbst aufgerufen (Slice N2).
    """
    doc = _doc if _doc is not None else ezdxf.readfile(str(dxf_path))
    f = float(factor_to_mm)
    out = []
    for e in doc.modelspace():
        if e.dxftype() == "INSERT" and "TÜR" in str(e.dxf.name).upper():
            out.append((e.dxf.insert.x * f, e.dxf.insert.y * f))
    if door_arcs is None:
        door_arcs = detect_door_arcs(doc, f)
    out.extend(d.opening_mid for d in door_arcs)
    return out


def _pt_seg_dist(p: tuple[float, float], a: tuple[float, float],
                 b: tuple[float, float]) -> float:
    vx, vy = b[0] - a[0], b[1] - a[1]
    L2 = vx * vx + vy * vy
    if L2 <= 1e-12:
        return math.hypot(p[0] - a[0], p[1] - a[1])
    t = max(0.0, min(1.0, ((p[0] - a[0]) * vx + (p[1] - a[1]) * vy) / L2))
    return math.hypot(p[0] - (a[0] + t * vx), p[1] - (a[1] + t * vy))


def door_chord_bridges(door_arcs: list[DoorArc], wall_segs: list[Seg],
                       exist_tol_mm: float = CHORD_EXIST_TOL_MM,
                       attach_tol_mm: float = CHORD_ATTACH_TOL_MM,
                       ) -> list[Seg]:
    """Sehnen-Brücken hinge→band_end für offene Tür-Öffnungen (N2).

    Anders als ``collinear_gap_bridges`` unabhängig von Kollinear-Bins —
    schließt auch Öffnungen mit versetzten/nicht-kollinearen Wand-Enden.
    Fail-safe: nur wenn die Sehnen-Mitte frei ist (keine Wand quert die
    Öffnung schon) und beide Enden ans Wand-Netz anbinden.
    """
    bridges: list[Seg] = []
    for d in door_arcs:
        mid = d.opening_mid
        mid_free = all(_pt_seg_dist(mid, a, b) > exist_tol_mm
                       for a, b in wall_segs)
        if not mid_free:
            continue
        attached = all(
            any(_pt_seg_dist(pt, a, b) <= attach_tol_mm
                for a, b in wall_segs)
            for pt in (d.hinge, d.band_end))
        if attached:
            bridges.append((d.hinge, d.band_end))
    return bridges


def collinear_gap_bridges(segments: list[Seg],
                          doors: list[tuple[float, float]],
                          small_gap_mm: float = SMALL_GAP_MM,
                          max_door_gap_mm: float = MAX_DOOR_GAP_MM,
                          door_evidence_mm: float = DOOR_EVIDENCE_MM,
                          ) -> list[Seg]:
    """Brücken über Lücken zwischen kollinearen Fragmenten (R2/R3).

    Fragmente werden in (2°-Winkel, 80mm-Offset)-Bins gruppiert und entlang
    ihrer Achse als Intervalle gemergt. Eine Lücke zwischen zwei Intervallen
    wird gebrückt (Original-Endpunkte, keine Projektion), wenn sie klein ist
    ODER ein Tür-INSERT sie erklärt. Es wird NUR die Brücke emittiert.
    """
    groups: dict[tuple[int, int], list[tuple[float, float, tuple, tuple]]] = {}
    for a, b in segments:
        dx, dy = b[0] - a[0], b[1] - a[1]
        if abs(dx) < 1e-9 and abs(dy) < 1e-9:
            continue
        ang = math.degrees(math.atan2(dy, dx)) % 180.0
        bin_ang = int(round(ang / ANGLE_BIN_DEG)) % int(180 / ANGLE_BIN_DEG)
        rad = math.radians(bin_ang * ANGLE_BIN_DEG)
        u = (math.cos(rad), math.sin(rad))
        t_a = a[0] * u[0] + a[1] * u[1]
        t_b = b[0] * u[0] + b[1] * u[1]
        mid = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        off = -mid[0] * u[1] + mid[1] * u[0]
        key = (bin_ang, int(round(off / OFFSET_BIN_MM)))
        lo, hi = (t_a, t_b) if t_a <= t_b else (t_b, t_a)
        lo_pt, hi_pt = (a, b) if t_a <= t_b else (b, a)
        groups.setdefault(key, []).append((lo, hi, lo_pt, hi_pt))

    bridges: list[Seg] = []
    for ivs in groups.values():
        if len(ivs) < 2:
            continue
        ivs.sort(key=lambda x: x[0])
        cur_hi, cur_hi_pt = ivs[0][1], ivs[0][3]
        for lo, hi, lo_pt, hi_pt in ivs[1:]:
            gap = lo - cur_hi
            if gap > 0:
                mid = ((cur_hi_pt[0] + lo_pt[0]) / 2,
                       (cur_hi_pt[1] + lo_pt[1]) / 2)
                has_door = any(
                    math.hypot(mid[0] - dx, mid[1] - dy) <= door_evidence_mm
                    for dx, dy in doors)
                if gap <= small_gap_mm or (gap <= max_door_gap_mm and has_door):
                    bridges.append((cur_hi_pt, lo_pt))
            if hi > cur_hi:
                cur_hi, cur_hi_pt = hi, hi_pt
    return bridges


def generate_marker_segments(
    dxf_path: str | Path, factor_to_mm: float, _doc=None,
    vocab: KellerVocab | None = None,
) -> dict:
    """Synthetische Marker-Segmente analog ``extract_marker_geometry``.

    Rückgabe: ``{wall_segments, hid_segments, bridges, door_arcs,
    chord_bridges}`` — ``wall_segments`` = NUR die Lücken-Brücken
    (kollineare + Tür-Sehnen; Bindegewebe — die Wand-Layer-Segmente selbst
    liefert der Basis-Pfad bereits, HID bleibt draußen — siehe R1).
    """
    doc = _doc if _doc is not None else ezdxf.readfile(str(dxf_path))
    wall_segs, hid_segs = collect_boundary_segments(
        dxf_path, factor_to_mm, _doc=doc, vocab=vocab)
    arcs = detect_door_arcs(doc, float(factor_to_mm))
    doors = door_positions(dxf_path, factor_to_mm, _doc=doc, door_arcs=arcs)
    bridges = collinear_gap_bridges(wall_segs, doors)
    chords = door_chord_bridges(arcs, wall_segs)
    return {
        "wall_segments": list(bridges) + list(chords),
        "hid_segments": len(hid_segs),
        "bridges": len(bridges),
        "door_arcs": len(arcs),
        "chord_bridges": len(chords),
    }
