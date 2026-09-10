"""fenster_signatur — Fensteröffnung nach ERSCHEINUNGSBILD, ohne Fensterobjekt.

Für die Barawitzka-Familie (ArchiCAD, reine Linien/Hatches): 0 Fenster-Layer,
0 Fenster-Blöcke, 0 INSERTs im Modelspace (``docs/ENIS_UEBERGABE_0908.md``
§ 4.2). Ein Fenster ist dort nur als Zeichnung vorhanden — Wandschraffur
unterbrochen, in der Lücke ein Rahmenpaar mit Scheibenlinien dazwischen.

Die Signatur (gemessene Werte, § 4.5):

1. zwei parallele Segmente auf einem Wand-Layer, Normalabstand 80–100 mm
   (Rahmentiefe, gemessen durchweg 90 mm), Längsüberlappung ≥ 300 mm,
2. dazwischen ≥ 2 weitere parallele Segmente (Scheiben, gemessen 20 mm
   Abstand) mit Längsüberlappung ≥ 60 % der Rahmenlänge,
3. Mittelpunkt NICHT in der Wandfläche, also in der Wandunterbrechung.

Punkt 2 allein trägt nicht (Wandaufbau-Schichtlinien erzeugen denselben
Doppelstrich), Punkt 1+2 ohne Punkt 3 ebenfalls nicht — beide Zwischenstufen
sind auf den Vergleichsplänen als überwiegend falsch gemessen (§ 4.5).

Was dieses Modul NICHT tut: es setzt kein Maß und keinen Normwert ein. Wo
nichts gefunden wird, kommt eine leere Liste — und die heißt nur dann „keine
Fenster", wenn ``wandsegmente(plan)`` überhaupt etwas zu prüfen hatte. Auf
Plänen mit Wänden in Blockdefinitionen (Rennweg) ist sie leer, das Ergebnis
heißt dort „nicht gesucht", nicht „nicht vorhanden".

Kein Contract-Touch: ``Fensteroeffnung`` ist der Rückgabetyp dieses Moduls.
Die Belichtungsfelder an ``Raum`` bleiben VORSCHLAG (§ 4.4).
"""
from __future__ import annotations

import math
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, replace
from itertools import pairwise

from shapely.geometry import Point, Polygon
from shapely.geometry.base import BaseGeometry
from shapely.ops import unary_union

from .dxf_load import WALL_PATTERN, DxfPlan
from .wandkoerper import _varianten_prefix, finde_wandkoerper

XY = tuple[float, float]
Segment = tuple[XY, XY, str]  # start, ende, layer (alles mm)

RAHMEN_MM = (80.0, 100.0)      # Normalabstand des Rahmenpaars
MIN_LAENGE_MM = 300.0          # Längsüberlappung des Rahmenpaars
WINKEL_TOLERANZ_GRAD = 1.0     # „parallel"
SCHEIBEN_MIN = 2               # Innenlinien zwischen den Rahmenkanten
SCHEIBEN_BAND = (0.15, 0.85)   # Lage der Innenlinien, Anteil der Rahmentiefe
SCHEIBEN_UEBERLAPPUNG = 0.6    # Anteil der Rahmenlänge
CLUSTER_MM = 200.0             # näher = dasselbe Element
MIN_SEGMENT_MM = 100.0         # kürzer = Stützpunktrauschen
BOGEN_RADIUS_MM = (500.0, 1500.0)  # Türbogen einer Fenster-/Balkontür
BOGEN_ZUSCHLAG_MM = 400.0


@dataclass(frozen=True)
class Fensteroeffnung:
    """Ein Fensterkandidat in mm. ``hat_tuerbogen=None`` = nicht ausgewertet."""

    mitte_mm: XY
    breite_mm: float
    rahmentiefe_mm: float
    scheibenlinien: int
    layer: str
    hat_tuerbogen: bool | None = None


def wandsegmente(plan: DxfPlan) -> list[Segment]:
    """Gerade Segmente auf Wand-Layern des Plan-Raums, in mm.

    Leer heißt „hier ist nichts zu prüfen" (Wände stecken in Blöcken), nicht
    „keine Wände".
    """
    prefix = _varianten_prefix(plan)
    f = plan.factor
    out: list[Segment] = []
    for e in plan.space:
        layer = str(e.dxf.layer)
        if not WALL_PATTERN.search(layer):
            continue
        if prefix and not layer.startswith(prefix):
            continue  # doppelt gezeichnete Planvariante
        typ = e.dxftype()
        if typ == "LINE":
            pts = [(e.dxf.start.x * f, e.dxf.start.y * f),
                   (e.dxf.end.x * f, e.dxf.end.y * f)]
        elif typ == "LWPOLYLINE":
            pts = [(p[0] * f, p[1] * f) for p in e.get_points()]
        else:
            continue
        out += [(a, b, layer) for a, b in pairwise(pts)
                if math.dist(a, b) >= MIN_SEGMENT_MM]
    return out


def _achsen(segmente: Iterable[Segment]):
    """(start, ende, ux, uy, laenge, winkel_mod_pi, layer) je Segment."""
    for a, b, layer in segmente:
        laenge = math.dist(a, b)
        if laenge < MIN_SEGMENT_MM:
            continue
        ux, uy = (b[0] - a[0]) / laenge, (b[1] - a[1]) / laenge
        yield a, b, ux, uy, laenge, math.atan2(uy, ux) % math.pi, layer


def _parallel(w1: float, w2: float, toleranz: float) -> bool:
    d = abs(w1 - w2)
    return min(d, math.pi - d) <= toleranz


def finde_rahmenfenster(
    segmente: Sequence[Segment],
    wandflaeche: BaseGeometry | None = None,
) -> list[Fensteroeffnung]:
    """Rahmen+Scheiben-Signatur über Wandsegmente (mm), rein geometrisch.

    ``wandflaeche``: Union der Wandkörper. Kandidaten, deren Mittelpunkt darin
    liegt, sind geschlossene Wand und fallen raus. ``None`` = Öffnungs-
    bedingung nicht geprüft (dann ist das Ergebnis ein Rohbefund).
    """
    # ponytail: O(n²) über die langen Wandsegmente (Barawitzka ~2k → 2 s).
    # Erst bei größeren Plänen lohnt ein Gitter/STRtree über die Achsen.
    toleranz = math.radians(WINKEL_TOLERANZ_GRAD)
    alle = list(_achsen(segmente))
    lang = [s for s in alle if s[4] >= MIN_LAENGE_MM]
    roh: list[Fensteroeffnung] = []
    for i, (a, _b, ux, uy, laenge, winkel, layer) in enumerate(lang):
        for a2, b2, _, _, _, winkel2, _ in lang[i + 1:]:
            if not _parallel(winkel, winkel2, toleranz):
                continue
            quer = -uy * (a2[0] - a[0]) + ux * (a2[1] - a[1])
            tiefe = abs(quer)
            if not RAHMEN_MM[0] <= tiefe <= RAHMEN_MM[1]:
                continue
            laengs = sorted(ux * (p[0] - a[0]) + uy * (p[1] - a[1])
                            for p in (a2, b2))
            s0, s1 = max(0.0, laengs[0]), min(laenge, laengs[1])
            if s1 - s0 < MIN_LAENGE_MM:
                continue
            vz = 1.0 if quer > 0 else -1.0
            n = _scheiben(alle, a, ux, uy, tiefe, vz, s0, s1, toleranz)
            if n < SCHEIBEN_MIN:
                continue
            mitte = ((s0 + s1) / 2, tiefe / 2 * vz)
            roh.append(Fensteroeffnung(
                mitte_mm=(a[0] + mitte[0] * ux - mitte[1] * uy,
                          a[1] + mitte[0] * uy + mitte[1] * ux),
                breite_mm=s1 - s0, rahmentiefe_mm=tiefe,
                scheibenlinien=n, layer=layer))

    treffer: list[Fensteroeffnung] = []
    for k in sorted(roh, key=lambda x: -x.breite_mm):
        if any(math.dist(k.mitte_mm, t.mitte_mm) < CLUSTER_MM for t in treffer):
            continue
        if wandflaeche is not None and wandflaeche.contains(Point(k.mitte_mm)):
            continue  # geschlossene Wand, keine Öffnung
        treffer.append(k)
    return treffer


def _scheiben(alle, a, ux, uy, tiefe, vz, s0, s1, toleranz) -> int:
    """Parallele Innenlinien zwischen den Rahmenkanten, längs überlappend."""
    winkel_rahmen = math.atan2(uy, ux) % math.pi
    n = 0
    for a3, b3, _, _, _, winkel3, _ in alle:
        if not _parallel(winkel_rahmen, winkel3, toleranz):
            continue
        d = (-uy * (a3[0] - a[0]) + ux * (a3[1] - a[1])) * vz
        if not SCHEIBEN_BAND[0] * tiefe < d < SCHEIBEN_BAND[1] * tiefe:
            continue
        c0, c1 = sorted(ux * (p[0] - a[0]) + uy * (p[1] - a[1]) for p in (a3, b3))
        if min(s1, c1) - max(s0, c0) >= SCHEIBEN_UEBERLAPPUNG * (s1 - s0):
            n += 1
    return n


def finde_fensteroeffnungen(plan: DxfPlan) -> list[Fensteroeffnung]:
    """Fensterkandidaten eines Plans (mm), inkl. Öffnungs- und Bogenprüfung."""
    segmente = wandsegmente(plan)
    polygone = [p for p in (Polygon(k.polygon_mm).buffer(0)
                            for k in finde_wandkoerper(plan))
                if not p.is_empty and p.is_valid]
    flaeche = unary_union(polygone) if polygone else None
    treffer = finde_rahmenfenster(segmente, flaeche)
    boegen = _tuerboegen(plan)
    return [replace(k, hat_tuerbogen=any(
        math.dist(k.mitte_mm, z) <= k.breite_mm / 2 + BOGEN_ZUSCHLAG_MM
        for z in boegen)) for k in treffer]


def _tuerboegen(plan: DxfPlan) -> list[XY]:
    """Zentren der ARCs mit Türblatt-Radius (mm)."""
    prefix = _varianten_prefix(plan)
    f = plan.factor
    return [(e.dxf.center.x * f, e.dxf.center.y * f) for e in plan.space
            if e.dxftype() == "ARC"
            and not (prefix and not str(e.dxf.layer).startswith(prefix))
            and BOGEN_RADIUS_MM[0] <= e.dxf.radius * f <= BOGEN_RADIUS_MM[1]]
