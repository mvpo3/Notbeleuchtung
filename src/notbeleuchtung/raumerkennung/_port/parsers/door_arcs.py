"""door_arcs — geometrischer Tür-Detektor: Bogen + Türblatt statt Blockname.

Slice N2. Die bisherige Tür-Erkennung (``auto_marker.door_positions``) hängt
am Blocknamen ``*TÜR*`` — das generalisiert nicht: In den Mollgasse-KGs sind
nur 3/11 Türen benannte INSERTs, die Mehrheit ist als roher ARC direkt auf
dem Wand-Layer gezeichnet (KG1: 192, KG2: 227 ARCs auf 02-TWA). Fremdprojekte
(Barawitzka-KG) haben ÜBERHAUPT keine tür-benannten Blöcke — nur rohe
90°-ARCs auf Wand-Layern.

Erkennungs-Pattern (wie ein Zeichner eine Schwenktür zeichnet):
  - Türbogen: ARC mit türplausiblem Radius + Schwenk-Winkel
  - Türblatt: Linien-Segment ~Radius-Länge, das am Bogen-Zentrum (Band)
    ansetzt — trennt Türbögen von Wand-Fillets und Möbel-Radien

Quellen: (a) rohe ARCs im Modelspace, (b) ARCs in INSERT-Blöcken
(world-transformiert, Muster wie ``architecture_dxf._door_geometry``).
Annotations-Layer (Bemaßung/Beschriftung/…) sind ausgeschlossen.

Pro Tür liefert der Detektor ``hinge`` (Band-Drehpunkt = ARC-Zentrum) und
``band_end`` (ARC-Endpunkt auf der Wand) — die Sehne hinge→band_end ist die
Tür-Öffnung in der Wand und dient ``auto_marker`` als Brücken-Segment.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

from parsers.stamp_refine import _is_annotation_layer

# Schwellen aus dem KG1/KG2-Radius-Histogramm (Pre-Read N2, factor 1000):
# Türbögen liegen bei 550–1400 mm; darunter Wand-Fillets (200–500 mm),
# darüber Rampen-/Fassaden-Radien (1600+ mm). Schwenk-Winkel einer Tür
# ~90°, mit Zeichen-Toleranz 45–135° (Halbkreise = Symbole, keine Türen).
DOOR_RADIUS_MM = (550.0, 1400.0)
DOOR_SPAN_DEG = (45.0, 135.0)
# Türblatt: Länge ≈ Radius (±25 %), ein Ende ≤150 mm am Bogen-Zentrum.
LEAF_RATIO = (0.75, 1.25)
LEAF_HINGE_TOL_MM = 150.0
# Blattspitze ≈ ARC-Endpunkt → identifiziert die Wand-Seite des Bogens.
LEAF_TIP_TOL_RATIO = 0.35

Seg = tuple[tuple[float, float], tuple[float, float]]


@dataclass
class DoorArc:
    hinge: tuple[float, float]      # Band-Drehpunkt (ARC-Zentrum), mm
    band_end: tuple[float, float]   # ARC-Endpunkt auf der Wand, mm
    radius_mm: float
    span_deg: float
    source: str                     # "raw_arc" | "block"

    @property
    def opening_mid(self) -> tuple[float, float]:
        """Mitte der Tür-Öffnung (Sehne hinge→band_end)."""
        return ((self.hinge[0] + self.band_end[0]) / 2.0,
                (self.hinge[1] + self.band_end[1]) / 2.0)


def _arc_endpoints_mm(cx, cy, r, start_deg, end_deg):
    a0 = math.radians(start_deg)
    a1 = math.radians(end_deg)
    return ((cx + r * math.cos(a0), cy + r * math.sin(a0)),
            (cx + r * math.cos(a1), cy + r * math.sin(a1)))


def _insert_transform(ins):
    """Block→World-Affine eines INSERT (scale → rotate → translate)."""
    sx = float(ins.dxf.xscale or 1.0)
    sy = float(ins.dxf.yscale or 1.0)
    rot = math.radians(float(ins.dxf.rotation or 0.0))
    ix = float(ins.dxf.insert.x)
    iy = float(ins.dxf.insert.y)
    c, s = math.cos(rot), math.sin(rot)

    def tf(bx: float, by: float) -> tuple[float, float]:
        x, y = bx * sx, by * sy
        return (c * x - s * y + ix, s * x + c * y + iy)

    scale = (abs(sx) + abs(sy)) / 2.0
    return tf, scale


def _match_leaf(hinge, r, e0, e1, segs: list[Seg]):
    """Türblatt-Suche: Segment ~r lang, ein Ende am hinge.

    Rückgabe: ``band_end`` (der ARC-Endpunkt auf der WAND — der jeweils
    andere als die Blattspitze) oder ``None`` wenn kein Blatt gefunden.
    """
    lo, hi = LEAF_RATIO
    tip_tol = LEAF_TIP_TOL_RATIO * r
    fallback = None
    for a, b in segs:
        length = math.hypot(b[0] - a[0], b[1] - a[1])
        if not (lo <= length / r <= hi):
            continue
        for near, far in ((a, b), (b, a)):
            if math.hypot(near[0] - hinge[0], near[1] - hinge[1]) \
                    > LEAF_HINGE_TOL_MM:
                continue
            # Blattspitze nahe einem ARC-Ende → das ANDERE Ende ist die Wand.
            if math.hypot(far[0] - e1[0], far[1] - e1[1]) <= tip_tol:
                return e0
            if math.hypot(far[0] - e0[0], far[1] - e0[1]) <= tip_tol:
                return e1
            # Blatt am Band, Spitze woanders (z.B. leicht offen gezeichnet):
            # Blatt-Evidenz zählt, Wand-Seite unbestimmt → start_angle-Ende
            # (Konvention wie architecture_dxf._door_geometry).
            fallback = e0
    return fallback


def _collect_msp_segments(msp, factor: float) -> list[Seg]:
    """LINE + LWPOLYLINE-Kanten aller Nicht-Annotations-Layer, mm."""
    segs: list[Seg] = []
    for e in msp:
        if _is_annotation_layer(str(e.dxf.layer or "")):
            continue
        t = e.dxftype()
        if t == "LINE":
            a = (e.dxf.start.x * factor, e.dxf.start.y * factor)
            b = (e.dxf.end.x * factor, e.dxf.end.y * factor)
            if a != b:
                segs.append((a, b))
        elif t == "LWPOLYLINE":
            pts = [(p[0] * factor, p[1] * factor) for p in e.get_points()]
            for i in range(len(pts) - 1):
                if pts[i] != pts[i + 1]:
                    segs.append((pts[i], pts[i + 1]))
            if bool(e.closed) and len(pts) > 2 and pts[0] != pts[-1]:
                segs.append((pts[-1], pts[0]))
    return segs


def detect_door_arcs(doc, factor_to_mm: float) -> list[DoorArc]:
    """Alle Tür-Bögen des Modelspace, namens-unabhängig erkannt."""
    f = float(factor_to_mm)
    msp = doc.modelspace()
    out: list[DoorArc] = []

    # (a) Rohe ARCs — Blatt-Kandidaten sind alle Modelspace-Segmente.
    msp_segs: list[Seg] | None = None
    for e in msp:
        if e.dxftype() != "ARC":
            continue
        if _is_annotation_layer(str(e.dxf.layer or "")):
            continue
        r = float(e.dxf.radius) * f
        span = (float(e.dxf.end_angle) - float(e.dxf.start_angle)) % 360.0
        if not (DOOR_RADIUS_MM[0] <= r <= DOOR_RADIUS_MM[1]
                and DOOR_SPAN_DEG[0] <= span <= DOOR_SPAN_DEG[1]):
            continue
        if msp_segs is None:
            msp_segs = _collect_msp_segments(msp, f)
        hinge = (e.dxf.center.x * f, e.dxf.center.y * f)
        e0, e1 = _arc_endpoints_mm(
            hinge[0], hinge[1], r,
            float(e.dxf.start_angle), float(e.dxf.end_angle))
        band = _match_leaf(hinge, r, e0, e1, msp_segs)
        if band is not None:
            out.append(DoorArc(hinge, band, r, span, "raw_arc"))

    # (b) ARCs in INSERT-Blöcken — Blatt-Kandidaten aus demselben Block.
    for ins in msp:
        if ins.dxftype() != "INSERT":
            continue
        try:
            blk = doc.blocks[ins.dxf.name]
        except Exception:
            continue
        tf, scale = _insert_transform(ins)

        blk_segs: list[Seg] | None = None
        for be in blk:
            if be.dxftype() != "ARC":
                continue
            r = float(be.dxf.radius) * scale * f
            span = (float(be.dxf.end_angle)
                    - float(be.dxf.start_angle)) % 360.0
            if not (DOOR_RADIUS_MM[0] <= r <= DOOR_RADIUS_MM[1]
                    and DOOR_SPAN_DEG[0] <= span <= DOOR_SPAN_DEG[1]):
                continue
            if blk_segs is None:
                blk_segs = []
                for le in blk:
                    t = le.dxftype()
                    if t == "LINE":
                        a = tf(le.dxf.start.x, le.dxf.start.y)
                        b = tf(le.dxf.end.x, le.dxf.end.y)
                        blk_segs.append(((a[0] * f, a[1] * f),
                                         (b[0] * f, b[1] * f)))
                    elif t == "LWPOLYLINE":
                        pts = [tf(p[0], p[1]) for p in le.get_points()]
                        for i in range(len(pts) - 1):
                            blk_segs.append(
                                ((pts[i][0] * f, pts[i][1] * f),
                                 (pts[i + 1][0] * f, pts[i + 1][1] * f)))
            cx_b = float(be.dxf.center.x)
            cy_b = float(be.dxf.center.y)
            r_b = float(be.dxf.radius)
            e0_b, e1_b = _arc_endpoints_mm(
                cx_b, cy_b, r_b,
                float(be.dxf.start_angle), float(be.dxf.end_angle))
            hinge_w = tf(cx_b, cy_b)
            hinge = (hinge_w[0] * f, hinge_w[1] * f)
            e0_w = tf(*e0_b)
            e1_w = tf(*e1_b)
            e0 = (e0_w[0] * f, e0_w[1] * f)
            e1 = (e1_w[0] * f, e1_w[1] * f)
            band = _match_leaf(hinge, r, e0, e1, blk_segs)
            if band is not None:
                out.append(DoorArc(hinge, band, r, span, "block"))
    return out
