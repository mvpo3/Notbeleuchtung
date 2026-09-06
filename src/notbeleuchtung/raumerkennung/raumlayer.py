"""raumlayer — Räume direkt aus dedizierten Raum-Layern lesen.

Drei der vier Input-Familien liefern **fertige Raum-Polygone** auf eigenen Layern
— deterministisch und auditierbar, ohne Wand-Polygonisierung/Clustering:

    Barawitzka    `_815 Raumbegrenzung`  (geschl. LWPOLYLINE) + `_810 Raum` (MTEXT)
    Herrenholz/   `810 Raum` / `811 Raum 2`  (geschl. LWPOLYLINE + INSERT ROOM_NAME)
    Baufeld E2
    Fischamender  `A_Raeume_`  (geschl. LWPOLYLINE) + `A_Raeume_Beschriftung_` (MTEXT)

Raumname kommt aus dem `ROOM_NAME`-ATTRIB (Herrenholz/Baufeld) oder aus einem
MTEXT-Stempel im Polygon (Barawitzka/Fischamender) → ``classify_room``. Fehlt ein
Raum-Layer (Mollgasse), liefert der Reader ``[]`` und der Provider fällt auf die
Wand-Polygonisierung zurück.
"""
from __future__ import annotations

import re
from collections import Counter
from collections.abc import Sequence

import numpy as np
from scipy.spatial import cKDTree
from shapely.geometry import Point, Polygon

from notbeleuchtung.hauptengine.contracts.raum_modell import Raum

from .dxf_load import DxfPlan
from .raumtyp import raumtyp_flags

# Layer mit Raum-Polygonen (Icon-Duplikate + reine Text-Layer werden ignoriert).
# `8\d{1,2}` deckt „810/811 Raum" (Barawitzka/Herrenholz) UND „080 Raumdefinitionen"
# (Rennweg/ArchiCAD — Match startet bei der 8) ab.
_ROOM_LAYER = re.compile(r"8\d{1,2}\s*Raum|Raumbegrenzung|A_Raeume", re.IGNORECASE)
_ROOM_LAYER_EXCLUDE = re.compile(r"Icon", re.IGNORECASE)

# HATCH-Variante: breiter (Raum deckt Raumbegrenzung/Raumdefinition/„810 Raum" ab),
# KEIN Icon-Exclude — Icon-Varianten werden über den Varianten-Versatz auf die
# Stempel-Variante geschoben und Duplikate dedupliziert (Barawitzka Icon_1/Icon_3).
_HATCH_ROOM_LAYER = re.compile(r"Raum|Raeume|Zone|Space", re.IGNORECASE)

_MIN_FLAECHE_M2 = 1.0
_HATCH_MAX_M2 = 200.0          # Kriterium (b): plausible Raumgröße für Layer-lose Hatches
XY = tuple[float, float]


def _ist_raum_layer(name: str) -> bool:
    return bool(_ROOM_LAYER.search(name)) and not _ROOM_LAYER_EXCLUDE.search(name)


def hat_raum_layer(plan: DxfPlan) -> bool:
    """True, wenn der Plan geschlossene Raum-Polygone auf einem Raum-Layer trägt."""
    return any(True for _ in _raum_polygone(plan))


def _flaeche_m2(poly: list[XY]) -> float:
    s = 0.0
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        s += x1 * y2 - x2 * y1
    return abs(s) / 2.0 / 1_000_000.0


def _raum_polygone(plan: DxfPlan):
    """Geschlossene LW/POLYLINE auf Raum-Layern → Polygon (mm), Fläche ≥ Minimum."""
    for e in plan.entities():
        if not _ist_raum_layer(e.dxf.layer):
            continue
        if e.dxftype() not in ("LWPOLYLINE", "POLYLINE"):
            continue
        if not getattr(e, "closed", False):
            continue
        poly = plan.entity_points(e)
        if len(poly) >= 3 and _flaeche_m2(poly) >= _MIN_FLAECHE_M2:
            yield poly


def _raum_stempel(plan: DxfPlan) -> list[tuple[str, XY]]:
    """(Name, xy_mm): ROOM_NAME-ATTRIBs + MTEXT/TEXT auf Raum-Layern."""
    out: list[tuple[str, XY]] = []
    for e in plan.entities():
        t = e.dxftype()
        if t == "INSERT" and e.attribs:
            for a in e.attribs:
                if "ROOM_NAME" in a.dxf.tag.upper() and a.dxf.text.strip():
                    out.append((a.dxf.text.strip(), plan._scale(e.dxf.insert)))
                    break
        elif t in ("MTEXT", "TEXT") and _ist_raum_layer(e.dxf.layer):
            txt = e.plain_text() if t == "MTEXT" else e.dxf.text
            if txt and txt.strip():
                out.append((txt.strip(), plan._scale(e.dxf.insert)))
    return out


def raeume_aus_layer(plan: DxfPlan) -> list[Raum]:
    """Räume aus den Raum-Layern; ``[]`` wenn keine Raum-Polygone vorhanden."""
    polygone = list(_raum_polygone(plan))
    if not polygone:
        return []
    stempel = _raum_stempel(plan)
    raeume: list[Raum] = []
    for i, poly in enumerate(polygone, start=1):
        shp = Polygon(poly)
        raum_typ, flucht, communal = "", False, False
        for txt, xy in stempel:
            if shp.covers(Point(xy)):
                tf = raumtyp_flags(txt)
                if tf is not None:
                    raum_typ, flucht, communal = tf
                    break
        raeume.append(
            Raum(
                id=f"raum_{i}",
                raum_typ=raum_typ,
                polygon_mm=[(float(x), float(y)) for x, y in poly],
                flaeche_m2=_flaeche_m2(poly),
                ist_fluchtweg=flucht,
                ist_communal=communal,
            )
        )
    return raeume


# ------------------------------------------------------- HATCH-Raumpolygone

def _hatch_pfad_mm(plan: DxfPlan, hatch) -> list[XY]:
    """Größter Boundary-Pfad des HATCH, geflattet (mm) — Löcher/Inseln zählen nicht."""
    import ezdxf.path
    best: list[XY] = []
    best_a = 0.0
    for p in ezdxf.path.from_hatch(hatch):
        pts = [plan._scale((v.x, v.y)) for v in p.flattening(10.0 / plan.factor)]
        a = _flaeche_m2(pts) if len(pts) >= 3 else 0.0
        if a > best_a:
            best, best_a = pts, a
    return best


def _prefixe_aus_layern(quell_layer: str, ziel_layer: str) -> tuple[str, str] | None:
    """Varianten-Prefixe über das längste gemeinsame Layer-Suffix.

    '…PP Icon_1_810 Raum' vs. '…PP_2_810 Raum' → ('…PP Icon_1', '…PP_2').
    """
    n = 0
    while (n < min(len(quell_layer), len(ziel_layer))
           and quell_layer[-1 - n] == ziel_layer[-1 - n]):
        n += 1
    if n == 0 or n >= len(quell_layer) or n >= len(ziel_layer):
        return None
    return quell_layer[:-n], ziel_layer[:-n]


def varianten_versatz(plan: DxfPlan, quell_prefix: str, ziel_prefix: str) -> XY | None:
    """Translation (mm) von Variante ``quell_prefix`` nach ``ziel_prefix``.

    Über gemeinsame Layer-Suffixe wird die LINE-reichste Layer-Familie gewählt
    (z.B. '170 Schachtwände'); der Versatz ist der Median der Endpunkt-Differenzen
    nach Grob-Ausrichtung (bbox-Minimum). Validierung: ≥80 % der Quell-Endpunkte
    matchen nach dem Shift <1 mm — sonst ``None``.

    Grenze: reine Translation (keine Rotation/Skalierung) — Planvarianten im
    selben Blatt sind verschobene Kopien.
    """
    von_layer: dict[str, list[XY]] = {}
    for e in plan.space:
        if e.dxftype() == "LINE":
            von_layer.setdefault(e.dxf.layer, []).extend(
                (plan._scale(e.dxf.start), plan._scale(e.dxf.end)))
    beste: tuple[list[XY], list[XY]] | None = None
    for layer, pts in von_layer.items():
        if not layer.startswith(quell_prefix):
            continue
        ziel = von_layer.get(ziel_prefix + layer[len(quell_prefix):])
        if ziel and len(pts) >= 8 and (beste is None or len(pts) > len(beste[0])):
            beste = (pts, ziel)
    if beste is None:
        return None
    q = np.asarray(beste[0])
    z = np.asarray(beste[1])
    grob = z.min(axis=0) - q.min(axis=0)
    baum = cKDTree(z)
    d, idx = baum.query(q + grob, distance_upper_bound=500.0)
    ok = np.isfinite(d)
    if int(ok.sum()) < 4:
        return None
    fein = grob + np.median(z[idx[ok]] - (q[ok] + grob), axis=0)
    d2, _ = baum.query(q + fein)
    if float((d2 < 1.0).mean()) < 0.8:
        return None
    return (float(fein[0]), float(fein[1]))


def _geheilt(pts: list[XY]) -> Polygon | None:
    """buffer(0)-Heilung; bei Multi-Ergebnis das größte Teilpolygon."""
    shp = Polygon(pts).buffer(0)
    if shp.is_empty:
        return None
    if shp.geom_type != "Polygon":
        shp = max(shp.geoms, key=lambda g: g.area)
    return shp


def raeume_aus_hatch(plan: DxfPlan, stempel: Sequence | None = None) -> list[Raum]:
    """Räume aus HATCH-Grenzpfaden (Barawitzka: 41 Raum-HATCHes, PolylinePaths).

    Ein HATCH wird Raumpolygon, wenn (a) sein Layer nach Raum aussieht (Raum/
    Raumbegrenzung/Raumdefinition/Zone/Space/A_Raeume/8xx — ohne Icon-Exclude)
    ODER (b) seine Fläche 1–200 m² beträgt UND ein Stempel darin liegt.
    (b) greift nur als Fallback ohne (a)-Treffer — sonst duplizieren Belags-/
    Bodenaufbau-Hatches die Raum-Layer-Polygone (Barawitzka: 41, nicht 49).
    ``stempel``: ``stempel_anker.Stempel``-Objekte (``position_mm``/``name``/``layer``).

    Liegen die Raum-HATCHes in einer anderen Planvariante als die Stempel
    (bbox-disjunkt), wird der ``varianten_versatz`` zur Stempel-Variante bestimmt
    und angewendet; Varianten ohne bestimmbaren Versatz entfallen. Exakte
    Duplikate (Icon_1/Icon_3 nach Shift deckungsgleich) werden dedupliziert.

    Kaskade (Doku): langfristig dockt das zwischen ``raeume_aus_layer`` und der
    Wand-Polygonisierung an — provider.py Z.40-42 bzw. plan_pruefen._raeume
    stellen in einem separaten Schritt um.
    """
    gruppen: dict[str, list[tuple[list[XY], bool]]] = {}
    for e in plan.entities():
        if e.dxftype() != "HATCH":
            continue
        layer = str(e.dxf.layer)
        pts = _hatch_pfad_mm(plan, e)
        if len(pts) < 3:
            continue
        f = _flaeche_m2(pts)
        per_layer = bool(_HATCH_ROOM_LAYER.search(layer))
        if per_layer:
            if f < _MIN_FLAECHE_M2:
                continue
        elif not (stempel and _MIN_FLAECHE_M2 <= f <= _HATCH_MAX_M2):
            continue
        gruppen.setdefault(layer, []).append((pts, per_layer))

    # (b) nur als Fallback: gibt es (a)-Treffer, fallen die Layer-losen weg.
    if any(pl for kandidaten in gruppen.values() for _pts, pl in kandidaten):
        gruppen = {
            layer: kandidaten for layer, kandidaten in gruppen.items()
            if any(pl for _pts, pl in kandidaten)
        }

    st_liste = list(stempel or [])
    st_bbox = None
    ziel_layer = ""
    if st_liste:
        xs = [s.position_mm[0] for s in st_liste]
        ys = [s.position_mm[1] for s in st_liste]
        st_bbox = (min(xs), min(ys), max(xs), max(ys))
        ziel_layer = Counter(s.layer for s in st_liste).most_common(1)[0][0]

    raeume: list[Raum] = []
    gesehen: set[tuple] = set()
    for layer, kandidaten in sorted(gruppen.items()):
        dx = dy = 0.0
        if st_bbox is not None:
            xs = [x for pts, _ in kandidaten for x, _y in pts]
            ys = [y for pts, _ in kandidaten for _x, y in pts]
            disjunkt = (max(xs) < st_bbox[0] or min(xs) > st_bbox[2]
                        or max(ys) < st_bbox[1] or min(ys) > st_bbox[3])
            if disjunkt:
                prefixe = _prefixe_aus_layern(layer, ziel_layer)
                versatz = (varianten_versatz(plan, *prefixe) if prefixe else None)
                if versatz is None:
                    continue        # Variante ohne Anker zur Stempel-Variante
                dx, dy = versatz
        for pts, per_layer in kandidaten:
            shp = _geheilt([(x + dx, y + dy) for x, y in pts])
            if shp is None:
                continue
            if not per_layer and not any(
                    shp.covers(Point(s.position_mm)) for s in st_liste):
                continue
            poly = [(float(x), float(y)) for x, y in shp.exterior.coords[:-1]]
            key = tuple((round(x, 1), round(y, 1)) for x, y in poly)
            if key in gesehen:
                continue
            gesehen.add(key)
            raum_typ, flucht, communal = "", False, False
            for s in st_liste:
                if shp.covers(Point(s.position_mm)):
                    tf = raumtyp_flags(getattr(s, "name", "") or "")
                    if tf is not None:
                        raum_typ, flucht, communal = tf
                        break
            raeume.append(
                Raum(
                    id=f"raum_{len(raeume) + 1}",
                    raum_typ=raum_typ,
                    polygon_mm=poly,
                    flaeche_m2=shp.area / 1e6,
                    ist_fluchtweg=flucht,
                    ist_communal=communal,
                )
            )
    return raeume
