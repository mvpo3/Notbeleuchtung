"""tuer_zuordnung — Türen an Räume anschließen (füllt ``Tuer.von_raum/nach_raum``).

Je Tür wird beidseits der Türsehne in Stufen (100/200/300/500 mm) senkrecht
geprobt, welcher Raum den Probepunkt deckt: die erste getroffene FREMDE
Raumfläche je Seite zählt. Übersprungen werden Stufen im Wandkörper und Stufen
im „eigenen" Raum — dem Raum, der den Türpunkt selbst deckt, weil gestempelte
Raumpolygone durch die Türöffnung ragen. Findet eine Seite keinen fremden Raum,
fällt sie auf den eigenen zurück (höchstens eine Seite, sonst stünde beidseits
derselbe Raum). Die Sehne kommt aus dem ``winkel_grad`` der nächsten Türöffnung
(INSERT-Rotation bzw. ARC-Startwinkel), sonst aus der nächsten Raumkante.
Seiten ohne Raum: ``AUSSEN`` (außerhalb der Gebäude-Außenkontur) oder
``KEIN_RAUM`` — letzteres wird als ``seite_fehlt`` gemeldet statt still
hingenommen.

Zusätzlich: Wandöffnungen > 800 mm zwischen zwei Räumen ohne Bogen/Block
(``durchgaenge_ohne_tuerblatt``) werden als ``Tuer(ohne_tuerblatt=True)``
ergänzt — die Kontaktzone zweier Raumpolygone minus Wandflächen ist die
Öffnung. Ein Streifen, der die Sehne einer Block-Tür desselben Raumpaars
überlappt, ist die Öffnung DIESER Tür und entfällt (Dublette).
"""
from __future__ import annotations

import math
from itertools import pairwise

from shapely.geometry import LineString, Point, Polygon
from shapely.prepared import prep

from notbeleuchtung.hauptengine.contracts.raum_modell import Raum, Tuer

from .tueren import TuerOeffnung

XY = tuple[float, float]

AUSSEN = "AUSSEN"
KEIN_RAUM = "KEIN_RAUM"

# Probeabstände senkrecht zur Türsehne. Eine feste Probe traf bei Sehnen auf
# der Wandflanke (ArchiCAD) je nach Wanddicke die Wand statt des Nachbarraums;
# die Stufen laufen von der Flanke bis hinter eine 500-mm-Wand.
_PROBE_STUFEN_MM = (100.0, 200.0, 300.0, 500.0)
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


def _naechste_oeffnung(tuer: Tuer, oeffnungen: list[TuerOeffnung]):
    """Nächste Türöffnung MIT Sehnenwinkel, höchstens ``_OEFFNUNG_SUCH_MM`` weit."""
    best, best_d = None, _OEFFNUNG_SUCH_MM
    for o in oeffnungen:
        if o.winkel_grad is None:
            continue
        d = math.dist(o.xy_mm, tuer.xy_mm)
        if d < best_d:
            best, best_d = o, d
    return best


def _sehnen_richtung(tuer: Tuer, oeffnungen: list[TuerOeffnung], polys) -> float:
    best = _naechste_oeffnung(tuer, oeffnungen)
    if best is not None:
        return math.radians(best.winkel_grad)
    return _kanten_richtung(tuer.xy_mm, polys)


def _raum_an(xy: XY, polys) -> Raum | None:
    for r, _p, pp in polys:
        if pp.covers(Point(xy)):
            return r
    return None


def _seite(xy: XY, normale: XY, sgn: float, polys, kontur, wand,
           eigen: Raum | None) -> tuple[str, bool]:
    """Eine Seite der Tür proben → (Ergebnis, „eigener Raum berührt").

    Je Stufe: liegt der Punkt in einem Wandkörper, zählt er nicht (die Wand ist
    weder Raum noch Freiland). Ebenso wenig zählt ``eigen`` — der Raum, der den
    TÜRPUNKT deckt: gestempelte Raumpolygone ragen durch die Türöffnung, und
    gemessen an Barawitzka/Mollgasse/Muthgasse traf die 100/200-mm-Stufe dann
    beidseits denselben Raum. Erst ein FREMDER Raum entscheidet die Seite.

    Liegt der Punkt außerhalb der gedeckten Kontur, wird AUSSEN gemerkt — aber
    NICHT sofort entschieden: gemessen am Rennweg OG1 liegt der 100-mm-Punkt
    einer Zimmertür 20 mm außerhalb der Kontur und 20 mm neben dem Raum, der
    ihn bei 200 mm deckt. Ein Raum schlägt AUSSEN also über alle Stufen; AUSSEN
    bleibt, wenn keine Stufe einen fremden Raum findet.
    """
    draussen = eigen_beruehrt = False
    for stufe in _PROBE_STUFEN_MM:
        p = Point(xy[0] + sgn * stufe * normale[0], xy[1] + sgn * stufe * normale[1])
        if wand is not None and wand.covers(p):
            continue
        r = _raum_an((p.x, p.y), polys)
        if r is not None and r is eigen:
            eigen_beruehrt = True
            continue
        if r is not None:
            return r.id, eigen_beruehrt
        if kontur is not None and not kontur.covers(p):
            draussen = True
    return (AUSSEN if draussen else KEIN_RAUM), eigen_beruehrt


def ordne_tueren(tueren: list[Tuer], oeffnungen: list[TuerOeffnung],
                 raeume: list[Raum], aussenkontur, wand_union_geom=None,
                 fehlende_seiten: list | None = None) -> list[Tuer]:
    """Füllt ``von_raum``/``nach_raum`` jeder Tür in-place (Rückgabe = Eingabe).

    ``aussenkontur`` = „gedeckte" Fläche (Polygon/MultiPolygon): was sie NICHT
    deckt, ist AUSSEN — seit der Außen-Analyse auch offene Höfe zwischen den
    Gebäude-Komponenten. ``wand_union_geom`` (optional) lässt Probepunkte IM
    Wandkörper überspringen; ohne sie gelten dieselben Stufen ohne Übersprung.
    Bereits gesetzte Zuordnungen bleiben unverändert.

    ``fehlende_seiten`` sammelt (Tür, „+"/„-", letzte Stufe) für jede Seite, die
    bis zur letzten Stufe weder Raum noch AUSSEN fand — der Aufrufer macht
    daraus seinen Klartext (der Contract ``Tuer`` führt kein ``seite_fehlt``).
    """
    polys = _raum_polys(raeume)
    kontur = (prep(aussenkontur)
              if aussenkontur is not None and not aussenkontur.is_empty else None)
    wand = (prep(wand_union_geom)
            if wand_union_geom is not None and not wand_union_geom.is_empty else None)
    for t in tueren:
        if t.von_raum is not None and t.nach_raum is not None:
            continue
        w = _sehnen_richtung(t, oeffnungen, polys)
        normale = (-math.sin(w), math.cos(w))   # Normale zur Sehne
        eigen = _raum_an(t.xy_mm, polys)
        proben = [_seite(t.xy_mm, normale, sgn, polys, kontur, wand, eigen)
                  for sgn in (1.0, -1.0)]
        seiten = [p[0] for p in proben]
        # Rückfall auf den eigenen Raum: eine Seite, die bis zur letzten Stufe
        # keinen fremden Raum findet, gehört dem Raum, der den Türpunkt deckt.
        # HÖCHSTENS eine Seite — sonst stünde beidseits derselbe Raum. Vorrang
        # hat die Seite, deren Probe den eigenen Raum wirklich berührt hat;
        # AUSSEN ist ein Befund und fällt nicht zurück.
        if eigen is not None:
            for i in ((0, 1) if proben[0][1] else (1, 0)):
                if seiten[i] == KEIN_RAUM and seiten[1 - i] != eigen.id:
                    seiten[i] = eigen.id
        if fehlende_seiten is not None:
            fehlende_seiten += [
                (t, zeichen, _PROBE_STUFEN_MM[-1])
                for zeichen, seite in zip(("+", "-"), seiten, strict=True)
                if seite == KEIN_RAUM]
        t.von_raum, t.nach_raum = seiten[0], seiten[1]
    return tueren


def _sehnen_zonen(tueren: list[Tuer], oeffnungen: list[TuerOeffnung]):
    """(gepufferte Sehne, Raumpaar) je Block-Tür mit Breite — Dubletten-Probe.

    Die Sehne ist ``xy_mm`` ± halbe Breite entlang ``winkel_grad`` der nächsten
    Öffnung, gepuffert um die halbe Wanddicke (``_KONTAKT_MM``), weil die Sehne
    auf einer Wandflanke liegen kann. Der Puffer ist FLACH (``cap_style="flat"``,
    nur quer zur Sehne): rund verlängert er die Zone um 250 mm über jedes
    Sehnenende hinaus und verschluckt eine echte Öffnung neben der Tür, sobald
    der Pfeiler dazwischen dünner als 250 mm ist (synthetisch belegt, 180 mm).

    Ohne gemessenen Sehnenwinkel gibt es KEINE Zone — der Kanten-Fallback von
    ``_sehnen_richtung`` wäre hier geraten, und eine geratene Sehne darf keinen
    Durchgang löschen. Türen ohne messbare Breite (Schiebetür) bleiben
    ebenfalls draußen: für sie gilt weiter allein die 600-mm-Regel.
    """
    zonen = []
    for t in tueren:
        if t.quelle != "block" or not t.breite_mm:
            continue
        o = _naechste_oeffnung(t, oeffnungen)
        if o is None:
            continue
        w = math.radians(o.winkel_grad)
        halb = t.breite_mm / 2.0
        sehne = LineString([
            (t.xy_mm[0] - halb * math.cos(w), t.xy_mm[1] - halb * math.sin(w)),
            (t.xy_mm[0] + halb * math.cos(w), t.xy_mm[1] + halb * math.sin(w))])
        zonen.append((sehne.buffer(_KONTAKT_MM, cap_style="flat"),
                      {t.von_raum, t.nach_raum}))
    return zonen


def durchgaenge_ohne_tuerblatt(
        raeume: list[Raum], tueren: list[Tuer], wand_union_geom,
        oeffnungen: list[TuerOeffnung] | None = None) -> list[Tuer]:
    """Öffnungen > 800 mm zwischen zwei Räumen ohne Bogen/Block.

    Kontaktzone = Schnitt der um die halbe Wanddicke gepufferten Raumpolygone;
    was davon NICHT von Wandkörpern gedeckt ist, ist eine Öffnung. Liegt dort
    keine bekannte Tür, entsteht eine ``Tuer`` mit ``ohne_tuerblatt=True``.

    Zwei Regeln halten bekannte Türen frei. (a) Die alte: eine Tür < 600 mm vom
    Streifen-Schwerpunkt. (b) Die Dublette: überlappt der Streifen die Sehne
    einer Block-Tür, die DASSELBE Raumpaar verbindet, ist er deren eigene
    Öffnung. Gemessen am Rennweg OG1: der Streifen läuft die ganze dünne Wand
    entlang (5711 mm), sein Schwerpunkt liegt 1766 mm von der Tür — (a) greift
    dort nicht, (b) schon (Überlappung 70,7 % der Sehnenzone). Das Raumpaar
    gehört zur Bedingung: ein Streifen eines ANDEREN Paares streift dieselbe
    Sehnenzone am Rennweg OG1 zu 1,3 % und ist keine Dublette, sondern ein
    eigener Durchgang (dort der Gang) — ob DER bleiben darf, entscheidet S5b.
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
    zonen = _sehnen_zonen(tueren, oeffnungen or [])
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
                if any(paar == {ra.id, rb.id} and g.intersects(sehnen_zone)
                       for sehnen_zone, paar in zonen):
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
