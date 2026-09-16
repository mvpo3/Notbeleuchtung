"""tuer_zuordnung — Türen an Räume anschließen (füllt ``Tuer.von_raum/nach_raum``).

Je Tür wird 300 mm senkrecht zur Türsehne beidseits getestet, welcher Raum
den Probepunkt deckt. Die Sehne kommt aus dem ``winkel_grad`` der nächsten
Türöffnung (INSERT-Rotation bzw. ARC-Startwinkel), sonst aus der nächsten
Raumkante. Seiten ohne Raum: ``AUSSEN`` (außerhalb der Gebäude-Außenkontur)
oder ``KEIN_RAUM``.

Zusätzlich: Wandöffnungen > 800 mm zwischen zwei Räumen ohne Bogen/Block
(``durchgaenge_ohne_tuerblatt``) werden als ``Tuer(ohne_tuerblatt=True)``
ergänzt — die Kontaktzone zweier Raumpolygone minus Wandflächen ist die
Öffnung.
"""
from __future__ import annotations

import math
from itertools import pairwise

from shapely.geometry import Point, Polygon
from shapely.prepared import prep

from notbeleuchtung.hauptengine.contracts.raum_modell import Raum, Tuer

from .tueren import TuerOeffnung

XY = tuple[float, float]

AUSSEN = "AUSSEN"
KEIN_RAUM = "KEIN_RAUM"

_PROBE_MM = 300.0          # Abstand des Probepunkts senkrecht zur Türsehne
_OEFFNUNG_SUCH_MM = 1500.0  # Türöffnung muss so nah an der Tür liegen
_DURCHGANG_MIN_MM = 800.0
_KONTAKT_MM = 250.0        # halbe Wanddicke für die Kontaktzone zweier Räume
_TUER_NAH_MM = 600.0       # bestehende Tür „deckt" eine Öffnung in diesem Radius


def _raum_polys(raeume: list[Raum]) -> list[tuple[Raum, Polygon, object]]:
    out = []
    for r in raeume:
        if len(r.polygon_mm) >= 3:
            p = Polygon(r.polygon_mm).buffer(0)
            if not p.is_empty:
                out.append((r, p, prep(p)))
    return out


def _kanten_richtung(xy: XY, polys) -> float:
    """Richtung (rad) der nächsten Raumkante — Sehnen-Fallback ohne Öffnung."""
    best_d, best_w = math.inf, 0.0
    pt = Point(xy)
    for _, p, _pp in polys:
        ring = list(p.exterior.coords)
        for a, b in pairwise(ring):
            seg_len = math.dist(a, b)
            if seg_len < 1.0:
                continue
            # Punkt-Segment-Abstand
            t = max(0.0, min(1.0, ((xy[0] - a[0]) * (b[0] - a[0])
                                   + (xy[1] - a[1]) * (b[1] - a[1])) / seg_len**2))
            proj = (a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1]))
            d = pt.distance(Point(proj))
            if d < best_d:
                best_d = d
                best_w = math.atan2(b[1] - a[1], b[0] - a[0])
    return best_w


def _sehnen_richtung(tuer: Tuer, oeffnungen: list[TuerOeffnung], polys) -> float:
    best, best_d = None, _OEFFNUNG_SUCH_MM
    for o in oeffnungen:
        if o.winkel_grad is None:
            continue
        d = math.dist(o.xy_mm, tuer.xy_mm)
        if d < best_d:
            best, best_d = o, d
    if best is not None:
        return math.radians(best.winkel_grad)
    return _kanten_richtung(tuer.xy_mm, polys)


def _raum_an(xy: XY, polys) -> Raum | None:
    for r, _p, pp in polys:
        if pp.covers(Point(xy)):
            return r
    return None


def ordne_tueren(tueren: list[Tuer], oeffnungen: list[TuerOeffnung],
                 raeume: list[Raum], aussenkontur) -> list[Tuer]:
    """Füllt ``von_raum``/``nach_raum`` jeder Tür in-place (Rückgabe = Eingabe).

    ``aussenkontur`` = „gedeckte" Fläche (Polygon/MultiPolygon): was sie NICHT
    deckt, ist AUSSEN — seit der Außen-Analyse auch offene Höfe zwischen den
    Gebäude-Komponenten. Bereits gesetzte Zuordnungen bleiben unverändert.
    """
    polys = _raum_polys(raeume)
    kontur = (prep(aussenkontur)
              if aussenkontur is not None and not aussenkontur.is_empty else None)
    for t in tueren:
        if t.von_raum is not None and t.nach_raum is not None:
            continue
        w = _sehnen_richtung(t, oeffnungen, polys)
        nx_, ny = -math.sin(w), math.cos(w)   # Normale zur Sehne
        seiten: list[str] = []
        for sgn in (1.0, -1.0):
            p = (t.xy_mm[0] + sgn * _PROBE_MM * nx_,
                 t.xy_mm[1] + sgn * _PROBE_MM * ny)
            r = _raum_an(p, polys)
            if r is not None:
                seiten.append(r.id)
            elif kontur is not None and not kontur.covers(Point(p)):
                seiten.append(AUSSEN)
            else:
                seiten.append(KEIN_RAUM)
        t.von_raum, t.nach_raum = seiten[0], seiten[1]
    return tueren


def durchgaenge_ohne_tuerblatt(raeume: list[Raum], tueren: list[Tuer],
                               wand_union_geom) -> list[Tuer]:
    """Öffnungen > 800 mm zwischen zwei Räumen ohne Bogen/Block.

    Kontaktzone = Schnitt der um die halbe Wanddicke gepufferten Raumpolygone;
    was davon NICHT von Wandkörpern gedeckt ist, ist eine Öffnung. Liegt dort
    keine bekannte Tür, entsteht eine ``Tuer`` mit ``ohne_tuerblatt=True``.
    """
    if wand_union_geom is None or wand_union_geom.is_empty:
        return []
    from .nutzungsklasse import nutzungsklasse_fuer
    # Diagnose Rennweg U13, Slice S5a: SCHACHT/LIFT (KEIN_RAUM) sind nicht
    # begehbar — Paare mit so einer Seite geben keinen Durchgang. Statische Map,
    # weil Raum.nutzungsklasse hier noch None ist (lift_* entstehen erst später).
    polys = [x for x in _raum_polys(raeume)
             if nutzungsklasse_fuer(x[0].raum_typ) != KEIN_RAUM]
    tuer_punkte = [t.xy_mm for t in tueren]
    out: list[Tuer] = []
    for i, (ra, pa, _) in enumerate(polys):
        for rb, pb, _ in polys[i + 1:]:
            if pa.distance(pb) > 2 * _KONTAKT_MM:
                continue
            zone = pa.buffer(_KONTAKT_MM).intersection(pb.buffer(_KONTAKT_MM))
            frei = zone.difference(wand_union_geom)
            if frei.is_empty:
                continue
            teile = list(frei.geoms) if hasattr(frei, "geoms") else [frei]
            for g in teile:
                mrr = g.minimum_rotated_rectangle
                coords = list(getattr(mrr, "exterior", g).coords)[:4]
                if len(coords) < 3:
                    continue
                breite = max(math.dist(coords[0], coords[1]),
                             math.dist(coords[1], coords[2]))
                if breite < _DURCHGANG_MIN_MM:
                    continue
                c = g.centroid
                xy = (float(c.x), float(c.y))
                if any(math.dist(xy, p) < _TUER_NAH_MM for p in tuer_punkte):
                    continue
                out.append(Tuer(
                    id=f"durchgang_{len(out) + 1}", xy_mm=xy,
                    breite_mm=float(round(breite)),
                    breite_quelle="GEOMETRIE_OEFFNUNG", von_raum=ra.id,
                    nach_raum=rb.id, ohne_tuerblatt=True, quelle="durchgang"))
                tuer_punkte.append(xy)
    return out


# ── Öffnungen in der AUSSENWAND (ohne Türblatt) ──────────────────────────────
_AUSSEN_KONTAKT_MM = 400.0   # Außenwände sind dicker als Innenwände (≤ 800)
_AUSSEN_DURCHGANG_MAX_MM = 2600.0  # breiter = Fassaden-Artefakt, keine Tür


def aussen_durchgaenge(raeume: list[Raum], tueren: list[Tuer],
                       wand_union_geom, kontur) -> list[Tuer]:
    """Öffnungen > 800 mm in der Außenwand eines ALLGEMEIN-Raums ohne
    Bogen/Block → ``Tuer(ohne_tuerblatt=True, nach_raum=AUSSEN)``.

    Analog zu ``durchgaenge_ohne_tuerblatt``, aber gegen die AUSSEN-Fläche:
    Kontaktzone = Raum-Puffer ∩ Außenring (2 m um die gedeckte Kontur),
    minus Wandkörper. Nur ALLGEMEIN-Räume (Rennweg-EG-Muster: Rampenkorridor
    mit 1340-mm-Lücke) — Wohnungs-Fensteröffnungen bleiben draußen.

    OFFEN (Diagnose U8, Slice S5c Z.1271-1274, Frage F8 Z.1406): Sobald S2 die
    Innen-Zonen deckt, liest diese Funktion am Rennweg OG3 eine 1547-mm-Lücke
    in der Stiegenhausfassade als Weg ins Freie (gemessene Folge: Notlicht in
    einer Privatwohnung). Ob eine Fassadenlücke im Obergeschoss ein Fenster
    oder ein Durchgang ist, entscheidet F8; das Querungskriterium dafür gehört
    zu S5c. S2 nimmt weder das eine noch das andere vorweg.
    """
    if (wand_union_geom is None or wand_union_geom.is_empty
            or kontur is None or kontur.is_empty):
        return []
    from .nutzungsklasse import nutzungsklasse_fuer
    # Ring + Kontakt-Puffer EINMAL rechnen (die Kontur ist auf großen Plänen
    # komplex — je Raum gepuffert war das der Zeitfresser auf Muthgasse).
    aussen_ring = (kontur.buffer(2000.0).difference(kontur)
                   .buffer(_AUSSEN_KONTAKT_MM))
    tuer_punkte = [t.xy_mm for t in tueren]
    out: list[Tuer] = []
    for r in raeume:
        klasse = r.nutzungsklasse or nutzungsklasse_fuer(r.raum_typ)
        if not (klasse or "").startswith("ALLGEMEIN") or len(r.polygon_mm) < 3:
            continue
        poly = Polygon(r.polygon_mm).buffer(0)
        if poly.is_empty:
            continue
        zone = poly.buffer(_AUSSEN_KONTAKT_MM).intersection(aussen_ring)
        frei = zone.difference(wand_union_geom)
        teile = list(frei.geoms) if hasattr(frei, "geoms") else [frei]
        for g in teile:
            if g.is_empty:
                continue
            mrr = g.minimum_rotated_rectangle
            coords = list(getattr(mrr, "exterior", g).coords)[:4]
            if len(coords) < 3:
                continue
            # Langseite ≈ Öffnungsbreite (die Wand klippt die Zone seitlich).
            # Der Deckel filtert Fassaden-Artefakte (fehlende Wandkörper an
            # einer ganzen Raumkante ergäben raumlange Pseudo-Öffnungen).
            breite = max(math.dist(coords[0], coords[1]),
                         math.dist(coords[1], coords[2]))
            if not (_DURCHGANG_MIN_MM < breite <= _AUSSEN_DURCHGANG_MAX_MM):
                continue
            c = g.centroid
            xy = (float(c.x), float(c.y))
            if any(math.dist(xy, p) < 2 * _TUER_NAH_MM for p in tuer_punkte):
                continue
            out.append(Tuer(
                id=f"aussenoeffnung_{len(out) + 1}", xy_mm=xy,
                breite_mm=float(round(breite)),
                breite_quelle="GEOMETRIE_OEFFNUNG", von_raum=r.id,
                nach_raum=AUSSEN, ohne_tuerblatt=True,
                quelle="oeffnung_aussenwand"))
            tuer_punkte.append(xy)
    return out
