"""stiegenhaus — Innenleben eines STIEGENHAUS-Raums: Läufe, Podeste, Anker.

Treppenläufe = Gruppen aus ≥3 parallelen Stufenlinien mit 150–350 mm
Senkrecht-Abstand (Rennweg real 186–227 mm, Mollgasse exakt 280 mm).
Laufrichtung aus Laufnummern-Texten 1..n (Rennweg „1"…„20") oder aus der
Gehlinie (Mollgasse: 43°-Diagonale) — sonst ``unbekannt``. Podeste =
Raumfläche minus Läufe minus Lift; Hauptpodest = Komponente mit den
Geschosstüren. Verbotszonen = Laufpolygone + Lift-/Schachtpolygone.

Anker (Platzierungs-Punkte, KEINE Platzierung — die bleibt Leonis):
PODEST/ANTRITT/AUSTRITT/TUER/RICHTUNGSWECHSEL mit ``winkel_grad``
(Podest-Längsachse bzw. Türwandwinkel) und ``fluchtrichtung_grad``
(abwärts Richtung Ausgang, aus der Laufrichtung).

ADR-0006 (bindend, zitiert): „Für Fluchtweg-Sicherheitsleuchten leitet der
Verdichter den Korridor-Achsen-Azimut ab, rechnet die C-Ebene RELATIV dazu
und schreibt DENSELBEN Azimut als rotation_deg — der Plan selbst ist die
Montage-/Ausrichtungs-Zusicherung." Diese Anker liefern nur die Azimute
(``winkel_grad``/``fluchtrichtung_grad``); ob/was rotiert platziert wird,
entscheidet die Platzierung (Leonis).
"""
from __future__ import annotations

import math
import re
from itertools import pairwise

from ezdxf.math import OCS
from shapely.geometry import LineString, MultiPoint, Point, Polygon

from notbeleuchtung.hauptengine.contracts.raum_modell import (
    Anker,
    Podest,
    Raum,
    StiegenhausModell,
    Treppenlauf,
    Tuer,
)

from .dxf_load import DxfPlan

XY = tuple[float, float]

_STAIR_BLOCK = re.compile(r"stiege|stieg|trepp|stair", re.IGNORECASE)
_STUFE_MIN_MM, _STUFE_MAX_MM = 200.0, 4000.0     # plausible Stufenlinien-Länge
_ABSTAND_MIN_MM, _ABSTAND_MAX_MM = 150.0, 350.0  # Senkrecht-Abstand der Stufen
_WINKEL_TOL_GRAD = 5.0
_MIN_STUFEN = 3
_PODEST_MIN_M2 = 1.0
_LAUF_MAX_M2 = 60.0      # größer = degenerierter Keil, kein Treppenlauf
_TUER_AN_RAUM_MM = 600.0
_KNICK_GRAD = 30.0


def _wcs_pts(v, f: float) -> list[XY]:
    """Stützpunkte einer virtuellen Block-Entity in WCS-mm (OCS-fest —
    gespiegelte Inserts tragen extrusion (0,0,-1), Mollgasse-Befund)."""
    t = v.dxftype()
    if t == "LINE":
        return [(v.dxf.start[0] * f, v.dxf.start[1] * f),
                (v.dxf.end[0] * f, v.dxf.end[1] * f)]
    if t == "LWPOLYLINE":
        ocs = OCS(v.dxf.extrusion)
        elev = float(v.dxf.elevation or 0.0)
        out = []
        for x, y, *_ in v.get_points():
            w = ocs.to_wcs((x, y, elev))
            out.append((float(w[0]) * f, float(w[1]) * f))
        return out
    return []


def _stufen_und_texte(plan: DxfPlan, poly: Polygon
                      ) -> tuple[list[tuple[XY, XY]], list[tuple[int, XY]],
                                 list[tuple[XY, XY]]]:
    """(Stufenlinien-Kandidaten, Laufnummern, sonstige Segmente) im Raum.

    Quellen: Entities direkt im Layout PLUS die aufgelösten Treppen-Blöcke
    (Rennweg: Stufen + Nummern leben IN den Stair-Blockdefinitionen).
    """
    hull = poly.buffer(500.0)
    f = plan.factor
    segs: list[tuple[XY, XY]] = []
    nums: list[tuple[int, XY]] = []

    def _nimm_segment(pts: list[XY]) -> None:
        for a, b in pairwise(pts):
            m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
            if hull.covers(Point(m)):
                segs.append((a, b))

    def _nimm_text(txt: str, xy: XY) -> None:
        t = (txt or "").strip()
        if re.fullmatch(r"\d{1,2}", t) and hull.covers(Point(xy)):
            nums.append((int(t), xy))

    for e in plan.entities():
        t = e.dxftype()
        if t in ("LINE", "LWPOLYLINE", "POLYLINE"):
            _nimm_segment(plan.entity_points(e))
        elif t in ("TEXT", "MTEXT"):
            txt = e.plain_text() if t == "MTEXT" else e.dxf.text
            p = e.dxf.insert
            _nimm_text(txt, (float(p[0]) * f, float(p[1]) * f))
        elif t == "INSERT" and _STAIR_BLOCK.search(e.dxf.name or ""):
            try:
                virtuelle = list(e.virtual_entities())
            except Exception as exc:  # noqa: BLE001 — kaputter Block darf nicht killen
                print(f"   virtual_entities({e.dxf.name}) fehlgeschlagen: {exc}")
                continue
            for v in virtuelle:
                vt = v.dxftype()
                if vt in ("LINE", "LWPOLYLINE"):
                    _nimm_segment(_wcs_pts(v, f))
                elif vt in ("TEXT", "MTEXT"):
                    txt = v.plain_text() if vt == "MTEXT" else v.dxf.text
                    p = v.dxf.insert
                    _nimm_text(txt, (float(p[0]) * f, float(p[1]) * f))
    stufen = [(a, b) for a, b in segs
              if _STUFE_MIN_MM <= math.dist(a, b) <= _STUFE_MAX_MM]
    return stufen, nums, segs


def _gruppiere_laeufe(stufen: list[tuple[XY, XY]]
                      ) -> list[list[tuple[XY, XY]]]:
    """≥3 parallele Linien mit 150–350 mm Senkrecht-Abstand → ein Lauf."""
    reste = list(stufen)
    laeufe: list[list[tuple[XY, XY]]] = []
    while reste:
        a0, b0 = reste[0]
        ang0 = math.atan2(b0[1] - a0[1], b0[0] - a0[0]) % math.pi
        gleich = []
        for s in reste:
            a, b = s
            ang = math.atan2(b[1] - a[1], b[0] - a[0]) % math.pi
            d = abs(ang - ang0)
            if min(d, math.pi - d) <= math.radians(_WINKEL_TOL_GRAD):
                gleich.append(s)
        # Projektion der Mittelpunkte auf die Normale → Ketten mit 150-350 mm.
        nx, ny = -math.sin(ang0), math.cos(ang0)
        gleich.sort(key=lambda s: ((s[0][0] + s[1][0]) / 2 * nx
                                   + (s[0][1] + s[1][1]) / 2 * ny))
        kette: list[tuple[XY, XY]] = []
        ketten: list[list[tuple[XY, XY]]] = []
        letzter = None
        for s in gleich:
            off = ((s[0][0] + s[1][0]) / 2 * nx + (s[0][1] + s[1][1]) / 2 * ny)
            if letzter is None or off - letzter <= _ABSTAND_MAX_MM:
                if (letzter is not None
                        and off - letzter < _ABSTAND_MIN_MM * 0.3):
                    letzter = off      # Duplikat-Linie (Doppelstrich) schlucken
                    kette.append(s)
                    continue
                kette.append(s)
            else:
                ketten.append(kette)
                kette = [s]
            letzter = off
        ketten.append(kette)
        for k in ketten:
            if len(k) >= _MIN_STUFEN:
                laeufe.append(k)
        # Alle parallelen Segmente sind einer Kette zugeteilt → abräumen
        # (Ketten <3 Linien sind keine Treppe und entfallen).
        weg = {id(s) for s in gleich}
        reste = [s for s in reste if id(s) not in weg]
    return laeufe


def _lauf_aus_gruppe(gruppe: list[tuple[XY, XY]],
                     nums: list[tuple[int, XY]],
                     gehlinien: list[tuple[XY, XY]]) -> Treppenlauf:
    pts = [p for s in gruppe for p in s]
    hull = MultiPoint(pts).convex_hull
    if hull.geom_type != "Polygon":
        hull = hull.buffer(50.0)
    polygon = [(float(x), float(y)) for x, y in hull.exterior.coords[:-1]]
    # Laufachse = Senkrechte auf die Stufen; Enden = extreme Stufen-Mittelpunkte.
    a0, b0 = gruppe[0]
    ang = math.atan2(b0[1] - a0[1], b0[0] - a0[0]) % math.pi
    nx, ny = -math.sin(ang), math.cos(ang)
    mids = sorted((((s[0][0] + s[1][0]) / 2, (s[0][1] + s[1][1]) / 2)
                   for s in gruppe), key=lambda m: m[0] * nx + m[1] * ny)
    ende_a, ende_b = mids[0], mids[-1]
    richtung = "unbekannt"
    antritt, austritt = ende_a, ende_b
    hp = hull.buffer(400.0)
    drin = [(n, p) for n, p in nums if hp.covers(Point(p))]
    if len(drin) >= 2:
        # Nummern zählen aufwärts: Antritt = Ende bei der kleinsten Nummer.
        lo = min(drin)[1]
        if math.dist(ende_a, lo) > math.dist(ende_b, lo):
            ende_a, ende_b = ende_b, ende_a
        antritt, austritt = ende_a, ende_b
        richtung = "auf"
    else:
        # Gehlinie: quer zur Stufenrichtung (>30°) MITTEN durch den Lauf —
        # das erodierte Hull schließt die flankierenden Wand-/Wangenlinien aus.
        kern = hull.buffer(-min(200.0, math.dist(ende_a, ende_b) / 10 + 1.0))
        for a, b in gehlinien:
            ga = math.atan2(b[1] - a[1], b[0] - a[0]) % math.pi
            d = abs(ga - ang)
            if min(d, math.pi - d) < math.radians(30.0):
                continue
            if not kern.is_empty and LineString([a, b]).intersects(kern):
                # Gehlinien-Start markiert konventionell den Antritt,
                # gezeichnet wird sie in Gehrichtung aufwärts.
                if math.dist(ende_a, a) > math.dist(ende_b, a):
                    ende_a, ende_b = ende_b, ende_a
                antritt, austritt = ende_a, ende_b
                richtung = "auf"
                break
    return Treppenlauf(polygon_mm=polygon, antritt_mm=antritt,
                       austritt_mm=austritt, richtung=richtung)


def _clip_lauf(lauf: Treppenlauf, raum: Polygon) -> Treppenlauf | None:
    """Lauf-Polygon auf das Stiegenhaus-Polygon clippen; None, wenn nichts
    übrig bleibt oder die Fläche kein Treppenlauf mehr sein kann.

    Die Lauf-Polygone sind konvexe Hüllen über Stufenlinien-Gruppen. Streuen
    die Linien (ausgebrochene Flutungs-Polygone, Barawitzka/Mollgasse), wird
    die Hülle zum Riesen-Keil weit über den Raum hinaus — als Verbotszone
    unbrauchbar. Clip + Flächendeckel machen daraus wieder eine Raumfläche.
    """
    p = Polygon(lauf.polygon_mm).buffer(0).intersection(raum)
    if p.is_empty:
        return None
    if p.geom_type != "Polygon":
        p = max(p.geoms, key=lambda g: g.area)
    if p.geom_type != "Polygon" or p.area <= 0 or p.area / 1e6 > _LAUF_MAX_M2:
        return None
    lauf.polygon_mm = [(float(x), float(y)) for x, y in p.exterior.coords[:-1]]
    return lauf


def _wandwinkel(poly: Polygon, xy: XY) -> float:
    """Winkel (Grad, mod 180) der Raumpolygon-Kante, die dem Punkt am nächsten
    liegt — der Türwandwinkel für TUER-Anker (Rotationsquelle nach ADR-0006:
    geliefert wird der Azimut, die Rotations-Entscheidung bleibt Leonis)."""
    pt = Point(xy)
    coords = list(poly.exterior.coords)
    best, best_d = 0.0, math.inf
    for a, b in pairwise(coords):
        d = LineString([a, b]).distance(pt)
        if d < best_d:
            best_d = d
            best = math.degrees(math.atan2(b[1] - a[1], b[0] - a[0])) % 180.0
    return best


def _laengsachse_grad(poly) -> float:
    mrr = poly.minimum_rotated_rectangle
    if mrr.geom_type != "Polygon":
        return 0.0
    e = list(mrr.exterior.coords)
    return math.degrees(
        math.atan2(*((e[1][1] - e[0][1], e[1][0] - e[0][0])
                     if math.dist(e[0], e[1]) >= math.dist(e[1], e[2])
                     else (e[2][1] - e[1][1], e[2][0] - e[1][0])))) % 180.0


def baue_stiegenhaus_modell(plan: DxfPlan, raum: Raum, lifte: list[Raum],
                            tueren: list[Tuer]
                            ) -> tuple[StiegenhausModell, list[Anker]]:
    """Stiegenhaus-Innenleben + Anker eines STIEGENHAUS-Raums ableiten.

    Anker tragen ``winkel_grad`` (Podest-Längsachse bzw. Türwandwinkel) und
    ``fluchtrichtung_grad`` (abwärts zum Ausgang) — Azimut-Lieferung im Sinne
    von ADR-0006 (s. Modul-Docstring), keine Platzierungs-Entscheidung.
    """
    poly = Polygon(raum.polygon_mm).buffer(0)
    stufen, nums, alle_segs = _stufen_und_texte(plan, poly)
    gruppen = _gruppiere_laeufe(stufen)
    # Nur Läufe IM Stiegenhaus: Treppen-Blöcke ragen über Nachbarräume
    # (Rennweg: Stufenlinien der Stair-Blöcke in Wohnungs-Polygonen).
    gruppen = [g for g in gruppen if poly.covers(
        MultiPoint([p for s in g for p in s]).convex_hull.centroid)]
    laeufe = [_lauf_aus_gruppe(g, nums, alle_segs) for g in gruppen]
    # Lauf-/Verbotszonen-Polygone bleiben im Raum (s. _clip_lauf).
    laeufe = [lf for lf in (_clip_lauf(x, poly) for x in laeufe) if lf is not None]

    lift_polys = [Polygon(lf.polygon_mm).buffer(0) for lf in lifte
                  if len(lf.polygon_mm) >= 3
                  and Polygon(lf.polygon_mm).buffer(0).intersects(poly)]
    lauf_polys = [Polygon(lf.polygon_mm).buffer(0) for lf in laeufe]

    # Geschosstüren dieses Stiegenhauses.
    stgh_tueren = [t for t in tueren
                   if raum.id in (t.von_raum, t.nach_raum)
                   or poly.exterior.distance(Point(t.xy_mm)) < _TUER_AN_RAUM_MM]

    # Podeste = Raum minus Läufe minus Lifte.
    frei = poly
    for p in lauf_polys + lift_polys:
        frei = frei.difference(p.buffer(50.0))
    teile = list(frei.geoms) if hasattr(frei, "geoms") else [frei]
    podeste: list[Podest] = []
    for t in teile:
        if t.is_empty or t.area / 1e6 < _PODEST_MIN_M2:
            continue
        ist_haupt = any(t.buffer(_TUER_AN_RAUM_MM).covers(Point(tr.xy_mm))
                        for tr in stgh_tueren)
        podeste.append(Podest(
            polygon_mm=[(float(x), float(y)) for x, y in t.exterior.coords[:-1]],
            ist_hauptpodest=ist_haupt))
    if podeste and not any(p.ist_hauptpodest for p in podeste):
        podeste[0].ist_hauptpodest = True

    verbotszonen = [lf.polygon_mm for lf in laeufe] + [
        [(float(x), float(y)) for x, y in p.exterior.coords[:-1]]
        for p in lift_polys]

    modell = StiegenhausModell(
        raum_id=raum.id, laeufe=laeufe, podeste=podeste,
        tuer_ids=[t.id for t in stgh_tueren], verbotszonen_mm=verbotszonen)

    # ── Anker ────────────────────────────────────────────────────────────────
    anker: list[Anker] = []

    def _ab_richtung(nahe: XY) -> float | None:
        """Fluchtrichtung = abwärts des nächsten Laufes mit bekannter Richtung."""
        best = None
        best_d = math.inf
        for lf in laeufe:
            if lf.richtung == "unbekannt":
                continue
            d = math.dist(nahe, lf.antritt_mm)
            if d < best_d:
                best_d = d
                a, b = ((lf.austritt_mm, lf.antritt_mm) if lf.richtung == "auf"
                        else (lf.antritt_mm, lf.austritt_mm))
                best = math.degrees(math.atan2(b[1] - a[1], b[0] - a[0])) % 360.0
        return best

    n = 0
    for p in podeste:
        n += 1
        pp = Polygon(p.polygon_mm)
        c = pp.representative_point()
        anker.append(Anker(
            id=f"{raum.id}_podest_{n}", typ="PODEST",
            xy_mm=(float(c.x), float(c.y)),
            winkel_grad=_laengsachse_grad(pp),
            fluchtrichtung_grad=_ab_richtung((float(c.x), float(c.y))),
            raum_id=raum.id))
    for i, lf in enumerate(laeufe, start=1):
        anker.append(Anker(id=f"{raum.id}_antritt_{i}", typ="ANTRITT",
                           xy_mm=lf.antritt_mm,
                           fluchtrichtung_grad=_ab_richtung(lf.antritt_mm),
                           raum_id=raum.id))
        anker.append(Anker(id=f"{raum.id}_austritt_{i}", typ="AUSTRITT",
                           xy_mm=lf.austritt_mm,
                           fluchtrichtung_grad=_ab_richtung(lf.austritt_mm),
                           raum_id=raum.id))
    for t in stgh_tueren:
        anker.append(Anker(id=f"{raum.id}_tuer_{t.id}", typ="TUER",
                           xy_mm=t.xy_mm,
                           winkel_grad=_wandwinkel(poly, t.xy_mm),
                           fluchtrichtung_grad=_ab_richtung(t.xy_mm),
                           raum_id=raum.id))
    # RICHTUNGSWECHSEL: Knick im Laufgraphen — zwei nahe Läufe, >30° Versatz.
    for i, l1 in enumerate(laeufe):
        for l2 in laeufe[i + 1:]:
            w1 = math.degrees(math.atan2(
                l1.austritt_mm[1] - l1.antritt_mm[1],
                l1.austritt_mm[0] - l1.antritt_mm[0])) % 180.0
            w2 = math.degrees(math.atan2(
                l2.austritt_mm[1] - l2.antritt_mm[1],
                l2.austritt_mm[0] - l2.antritt_mm[0])) % 180.0
            diff = abs(w1 - w2)
            diff = min(diff, 180.0 - diff)
            if diff <= _KNICK_GRAD:
                continue
            enden1 = (l1.antritt_mm, l1.austritt_mm)
            enden2 = (l2.antritt_mm, l2.austritt_mm)
            e1, e2 = min(((a, b) for a in enden1 for b in enden2),
                         key=lambda ab: math.dist(*ab))
            if math.dist(e1, e2) > 3000.0:
                continue
            xy = ((e1[0] + e2[0]) / 2, (e1[1] + e2[1]) / 2)
            n += 1
            anker.append(Anker(id=f"{raum.id}_knick_{n}",
                               typ="RICHTUNGSWECHSEL", xy_mm=xy,
                               fluchtrichtung_grad=_ab_richtung(xy),
                               raum_id=raum.id))
    # Keine Anker in Verbotszonen (Lauf-/Liftflächen sind nicht montierbar).
    sperren = [Polygon(v).buffer(0) for v in verbotszonen if len(v) >= 3]
    innen = poly.buffer(200.0)
    anker = [a for a in anker
             if innen.covers(Point(a.xy_mm))       # kein Anker außerhalb des Raums
             and (a.typ in ("ANTRITT", "AUSTRITT")  # Lauf-Enden liegen am Rand
                  or not any(s.contains(Point(a.xy_mm)) for s in sperren))]
    return modell, _entklumpe(anker)


_ANKER_MIN_ABSTAND_MM = 1000.0


def _entklumpe(anker: list[Anker]) -> list[Anker]:
    """Mindestabstand 1 m je Ankertyp — näher beieinander sind es Dubletten
    desselben Montagepunkts (Mollgasse: RICHTUNGSWECHSEL-Klumpen aus jedem
    Laufpaar am selben Knick). Der erste Anker gewinnt."""
    out: list[Anker] = []
    for a in anker:
        if any(b.typ == a.typ
               and math.dist(a.xy_mm, b.xy_mm) < _ANKER_MIN_ABSTAND_MM
               for b in out):
            continue
        out.append(a)
    return out
