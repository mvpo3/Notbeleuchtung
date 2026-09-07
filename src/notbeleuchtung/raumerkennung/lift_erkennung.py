"""lift_erkennung — Liftschächte layerunabhängig am Erscheinungsbild erkennen.

Ein Lift ist im Architekturplan ein geschlossenes Rechteck mit 1.0–2.8 m
Seitenlänge, belegt durch mindestens EINE dieser Evidenzen:

- **X-Diagonalen** im Rechteck (klassisches Schacht-Symbol),
- **Achsenkreuz** (Mittellinien — Mollgasse-Befund: LIFT-Block 1.65×1.90 m
  trägt ein Achsenkreuz statt X),
- **Lift-Text** im Umkreis (AUFZUG, LIFT, Fahrkabine, „Pers.", „kg", 110/140 —
  Rennweg-Befund: NUR ein MTEXT „AUFZUG 8 PERS. …", kein Symbol; der
  textbasierte Pfad muss das umgebende Rechteck finden),
- **Blockname** lift/aufzug/elevator (INSERT-Bounding-Box als Rechteck).

Ergebnis: ``Raum``-Objekte mit ``raum_typ='LIFT'`` und
``nutzungsklasse='KEIN_RAUM'``. Liegt der Lift in einem bestehenden
STIEGENHAUS-Polygon, wird er dort AUSGESTANZT (der Schacht ist keine
begehbare Stiegenhausfläche). Ein AUFZUGSVORPLATZ wird nur typisiert, wenn
ein eigener Raum vor der Lifttür existiert — automatisch ist das heute nicht
erkennbar (docs/OFFENE_FRAGEN.md), sonst bleibt die Fläche Stiegenhaus.
"""
from __future__ import annotations

import math
import re

from ezdxf import bbox
from shapely.geometry import LineString, Point, Polygon

from notbeleuchtung.hauptengine.contracts.raum_modell import Raum

from .dxf_load import DxfPlan

XY = tuple[float, float]

_LIFT_BLOCK = re.compile(r"lift|aufzug|elevator", re.IGNORECASE)
_LIFT_TEXT = re.compile(
    r"AUFZUG|LIFT|FAHRKABINE|\d+\s*PERS|\d+\s*KG|110\s*/\s*140", re.IGNORECASE)
_SEITE_MIN, _SEITE_MAX = 1000.0, 2800.0
_TEXT_UMKREIS_MM = 1500.0       # Text „im Umkreis 1 m" — plus Rechteck-Halbdiagonale
_MARKER_TOL_MM = 350.0          # Endpunkt-Toleranz für X-/Achsenkreuz-Erkennung


def _rechteck(pts: list[XY]) -> tuple[list[XY], XY, float, float] | None:
    """(rect_polygon, center, w, h) wenn die Punktliste ein Lift-großes,
    rechteck-artiges Polygon beschreibt, sonst None.

    Über das MINIMALE umschreibende Rechteck (nicht die Achsen-BBox): der
    Rennweg-Kabinenumriss ist ~23° rotiert. Konvexe Hülle statt Ringfläche:
    Kabinen-Umrisse sind oft dünne Doppellinien-/selbstschneidende Konturen —
    entscheidend ist, dass die Kontur das Rechteck AUFSPANNT (keine L-Form).
    """
    if len(pts) < 4:
        return None
    hull = Polygon(pts).convex_hull
    if hull.is_empty or hull.geom_type != "Polygon":
        return None
    mrr = hull.minimum_rotated_rectangle
    if mrr.geom_type != "Polygon":
        return None
    ecken = list(mrr.exterior.coords)[:4]
    w, h = math.dist(ecken[0], ecken[1]), math.dist(ecken[1], ecken[2])
    if not (_SEITE_MIN <= w <= _SEITE_MAX and _SEITE_MIN <= h <= _SEITE_MAX):
        return None
    if hull.area < 0.7 * mrr.area:
        return None
    c = mrr.centroid
    rect = [(float(x), float(y)) for x, y in ecken]
    return rect, (float(c.x), float(c.y)), w, h


def _segmente_mm(plan: DxfPlan) -> list[tuple[XY, XY]]:
    out: list[tuple[XY, XY]] = []
    for e in plan.entities():
        if e.dxftype() == "LINE":
            pts = plan.entity_points(e)
            out.append((pts[0], pts[1]))
        elif e.dxftype() == "LWPOLYLINE":
            pts = plan.entity_points(e)
            if len(pts) == 2:
                out.append((pts[0], pts[1]))
    return out


def _hat_marker(rect: list[XY], center: XY, w: float, h: float,
                segmente: list[tuple[XY, XY]]) -> bool:
    """X-Diagonalen ODER Achsenkreuz im Rechteck?"""
    ecken = rect
    mitten = [((ecken[i][0] + ecken[(i + 1) % 4][0]) / 2,
               (ecken[i][1] + ecken[(i + 1) % 4][1]) / 2) for i in range(4)]
    diag = [(ecken[0], ecken[2]), (ecken[1], ecken[3])]
    achse = [(mitten[0], mitten[2]), (mitten[1], mitten[3])]
    for a, b in segmente:
        if math.dist(((a[0] + b[0]) / 2, (a[1] + b[1]) / 2), center) > (w + h):
            continue
        for p, q in diag + achse:
            if ((math.dist(a, p) < _MARKER_TOL_MM and math.dist(b, q) < _MARKER_TOL_MM)
                    or (math.dist(a, q) < _MARKER_TOL_MM
                        and math.dist(b, p) < _MARKER_TOL_MM)):
                return True
    return False


def _lift_texte(plan: DxfPlan) -> list[XY]:
    out: list[XY] = []
    for e in plan.entities():
        t = e.dxftype()
        if t not in ("TEXT", "MTEXT"):
            continue
        txt = e.plain_text() if t == "MTEXT" else e.dxf.text
        if txt and _LIFT_TEXT.search(txt):
            p = e.dxf.insert
            out.append((float(p[0]) * plan.factor, float(p[1]) * plan.factor))
    return out


def finde_lifte(plan: DxfPlan, raeume: list[Raum]) -> list[Raum]:
    """Lifte erkennen, als LIFT/KEIN_RAUM-Räume anhängen, aus STIEGENHAUS ausstanzen.

    Gibt die NEU erzeugten Lift-Räume zurück (sie sind bereits an ``raeume``
    angehängt; überdeckte STIEGENHAUS-Polygone sind in-place ausgestanzt).
    """
    f = plan.factor
    kandidaten: list[tuple[list[XY], XY, float, float, bool]] = []  # + belegt-Flag
    for e in plan.entities():
        if e.dxftype() == "INSERT" and _LIFT_BLOCK.search(e.dxf.name or ""):
            b = bbox.extents([e])
            if not b.has_data:
                continue
            r = _rechteck([(b.extmin[0] * f, b.extmin[1] * f),
                           (b.extmax[0] * f, b.extmin[1] * f),
                           (b.extmax[0] * f, b.extmax[1] * f),
                           (b.extmin[0] * f, b.extmax[1] * f)])
            if r:
                kandidaten.append((*r, True))          # Blockname = Evidenz
        elif e.dxftype() in ("LWPOLYLINE", "POLYLINE"):
            pts = plan.entity_points(e)
            r = _rechteck(pts)
            if r:
                kandidaten.append((*r, False))
    if not kandidaten:
        return []
    segmente = _segmente_mm(plan)
    texte = _lift_texte(plan)
    # Marker-Evidenz (X/Achsenkreuz) ist NUR in der Erschließung eindeutig:
    # Betten/Möbel/Waschmaschinen tragen dieselben Diagonalen (Barawitzka-
    # Befund: 9 Fehltreffer in Küche/Bad/Waschküche/Terrasse). Text und
    # Blockname sind starke Evidenz und gelten überall.
    erschliessung = [Polygon(r.polygon_mm).buffer(0) for r in raeume
                     if r.raum_typ in ("STIEGENHAUS", "GANG")
                     and len(r.polygon_mm) >= 3]
    belegte: list[tuple[list[XY], XY]] = []
    for rect, center, w, h, belegt in kandidaten:
        radius = _TEXT_UMKREIS_MM + math.hypot(w, h) / 2
        if not belegt:
            belegt = any(math.dist(t, center) < radius for t in texte) or (
                any(p.covers(Point(center)) for p in erschliessung)
                and _hat_marker(rect, center, w, h, segmente))
        if belegt:
            belegte.append((rect, center))
    # Dedup: überlappende Kandidaten (z.B. Block + gezeichnetes Rechteck).
    lifte: list[tuple[list[XY], XY]] = []
    for rect, center in belegte:
        if any(Polygon(rect).intersection(Polygon(r2)).area
               > 0.5 * Polygon(rect).area for r2, _ in lifte):
            continue
        lifte.append((rect, center))

    neu: list[Raum] = []
    for i, (rect, center) in enumerate(lifte, start=1):
        # Schon ein LIFT-Raum an der Stelle? Dann nichts erfinden.
        if any(r.raum_typ == "LIFT" and len(r.polygon_mm) >= 3
               and Polygon(r.polygon_mm).covers(Point(center)) for r in raeume):
            continue
        lift_poly = Polygon(rect)
        raum = Raum(id=f"lift_{i}", raum_typ="LIFT", polygon_mm=rect,
                    flaeche_m2=lift_poly.area / 1e6, nutzungsklasse="KEIN_RAUM")
        # Ausstanzen aus überdeckenden STIEGENHAUS-Polygonen.
        for r in raeume:
            if r.raum_typ != "STIEGENHAUS" or len(r.polygon_mm) < 3:
                continue
            poly = Polygon(r.polygon_mm).buffer(0)
            if not poly.covers(Point(center)):
                continue
            stanze = lift_poly
            rest = poly.difference(stanze)
            if getattr(rest, "interiors", None) and list(rest.interiors):
                # Lift liegt komplett IM Raum → Loch, das der Contract-Ring
                # nicht abbilden kann: Stanze per schmalem Schlitz mit der
                # nächsten Außenkante verbinden (minimaler Flächenverlust).
                naechster = poly.exterior.interpolate(
                    poly.exterior.project(lift_poly.centroid))
                schlitz = LineString(
                    [lift_poly.centroid, naechster]).buffer(25.0)
                stanze = lift_poly.union(schlitz)
                rest = poly.difference(stanze)
            teile = list(rest.geoms) if hasattr(rest, "geoms") else [rest]
            groesster = max((t for t in teile if not t.is_empty),
                            key=lambda t: t.area, default=None)
            if groesster is not None and groesster.exterior is not None:
                r.polygon_mm = [(float(x), float(y))
                                for x, y in groesster.exterior.coords[:-1]]
                r.flaeche_m2 = groesster.area / 1e6
        neu.append(raum)
    raeume.extend(neu)
    return neu
