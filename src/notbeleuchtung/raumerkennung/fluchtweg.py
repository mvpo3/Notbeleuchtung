"""fluchtweg — Fluchtweg-Segmente aus drei Quellen vereinigen.

(a) **LINIE** — explizite Fluchtweg-Linien: die 09-WEG-Segmente aus
    ``zirkulation_aus_dxf`` plus generisch erkannte Linien
    (``explizite_linien``): Layer-Muster FLW/FLUCHTWEG (Aliasnamen der
    ``materialien.yaml``-Semantik FLUCHTWEG), Farbe 96 NUR wenn der Layer
    nicht nach Kataster/Grenze/Vermessung klingt (Barawitzka-Befund,
    docs/OFFENE_FRAGEN.md).
(b) **GRAPH** — Raumgraph (Knoten Räume, Kanten Türen): von jeder
    wohnungseingang-Tür (KORRIGIERTE Rolle, ``wohnungsklasse.korrigierte_rollen``
    — Einbahn E7: das Modell trägt die rohen Rollen, die korrigierten liest
    nur der Fluchtweg) und jedem ALLGEMEIN-Raum der kürzeste Weg über
    ALLGEMEIN_ERSCHLIESSUNG-Räume zu einem stair_exit/final_exit; Polyline
    Tür-zu-Tür entlang des Raum-Skeletts (eigenes skimage-Skelett auf
    50-mm-Raster — NICHT ``platzierung/mittellinie`` importieren:
    Owner-Grenze).
(c) **FALLBACK** — Mittelachse jedes COMMUNALEN GANG/STIEGENHAUS ohne Weg
    (``richtung_unbekannt=True``; R4 aus docs/GATE_TUERSTAPEL.md § 6f).

**Durchleitung** (§ 6g, Owner-Entscheid 2026-09-20): privat heißt keine
Notbeleuchtung und keine eigene Zirkulation — aber kein Loch im Graph. Ein
privat gewordener Erschließungsraum (``wohnungsklasse.durchleitung_raeume``)
bleibt Knoten für Wege zwischen zwei communalen Räumen; er bekommt aber weder
Segment-Stützpunkte (die Teilstrecke durch ihn ist die Direktlinie Tür→Tür,
kein Skelettpfad) noch Anker noch Leuchten, und er ist nie Start- oder
Zielraum eines Segments. Ein UNBESTIMMTER Raum (§ 6g Schritt 3) wird
konservativ wie ein communaler behandelt: voller Knoten mit Stützpunkten.
"""
from __future__ import annotations

import math
import re
from collections import deque
from itertools import pairwise

import networkx as nx
import numpy as np
from shapely.geometry import LineString, Point, Polygon
from skimage.draw import polygon as _rasterpoly
from skimage.morphology import skeletonize

from notbeleuchtung.hauptengine.contracts.raum_modell import (
    Ausgang,
    FluchtwegSegment,
    Raum,
    Tuer,
)

from .dxf_load import DxfPlan
from .geschoss import (
    GESCHOSS_UNBEKANNT_WARNUNG,
    geschoss_bekannt,
    ist_obergeschoss,
)
from .tuer_zuordnung import AUSSEN, KEIN_RAUM
from .wohnungsklasse import (
    bestaetigt_privat,
    durchleitung_raeume,
    korrigierte_rollen,
    volle_knoten,
)
from .zirkulation import WEG_PREFIX, _laenge, _reason

XY = tuple[float, float]

# Layer, die explizite Fluchtweg-Linien tragen (materialien.yaml semantik
# FLUCHTWEG: Aliasnamen FLUCHTWEG* / FLW*).
_FLW_LAYER = re.compile(r"FLUCHTWEG|FLW", re.IGNORECASE)
# Farbe 96 ist auf Barawitzka KATASTER — nur werten, wenn der Layer neutral ist.
_KEIN_FLW_LAYER = re.compile(r"KATASTER|GRENZ|VERM", re.IGNORECASE)
_FLW_FARBE = 96

_RASTER_MM = 50.0
_MAX_RASTER_PX = 4_000_000  # ponytail: ab hier Raster vergröbern statt OOM
_START_GEDECKT_MM = 2000.0  # LINIE-Segment so nah → Start schon explizit geplant
_TUER_AN_RAUM_MM = 600.0


# ── (a) explizite Linien ─────────────────────────────────────────────────────
def _effektive_farbe(e, plan: DxfPlan) -> int:
    farbe = int(e.dxf.get("color", 256) or 256)
    if 0 < farbe < 256:
        return farbe
    # `layers.get` wirft bei einem Layer ohne Tabelleneintrag (Minimal-DXF,
    # 2a) — der None-Zweig war dafür gedacht.
    layers = plan.doc.layers
    layer = layers.get(e.dxf.layer) if layers.has_entry(e.dxf.layer) else None
    return int(layer.color) if layer is not None else 0


def explizite_linien(plan: DxfPlan) -> list[list[XY]]:
    """Explizite Fluchtweg-Polylinien JENSEITS der 09-WEG-Layer (die liefert
    schon ``zirkulation_aus_dxf``): FLW-Layer-Muster oder Farbe 96 auf
    neutralem Layer."""
    out: list[list[XY]] = []
    for e in plan.entities():
        if e.dxftype() not in ("LINE", "LWPOLYLINE", "POLYLINE"):
            continue
        layer = e.dxf.layer
        if layer.startswith(WEG_PREFIX):
            continue
        if _KEIN_FLW_LAYER.search(layer):
            continue
        if not (_FLW_LAYER.search(layer)
                or _effektive_farbe(e, plan) == _FLW_FARBE):
            continue
        pts = plan.entity_points(e)
        if len(pts) >= 2:
            out.append(pts)
    return out


def linien_segmente(polylinien: list[list[XY]],
                    start_index: int) -> list[FluchtwegSegment]:
    return [
        FluchtwegSegment(
            segment_id=f"seg_{start_index + i}",
            polyline_mm=[(float(x), float(y)) for x, y in pts],
            laenge_mm=_laenge(pts), reason=_reason(pts), quelle="LINIE")
        for i, pts in enumerate(polylinien, start=1)
    ]


# ── Skelett-Pfad in einem Raumpolygon ────────────────────────────────────────
def _skelett_pfad(poly: Polygon, a: XY, b: XY) -> list[XY]:
    """Pfad a→b entlang des skimage-Skeletts der Raumfläche (50-mm-Raster);
    Fallback = Direktlinie, wenn das Skelett nichts hergibt."""
    minx, miny, maxx, maxy = poly.bounds
    res = _RASTER_MM
    w, h = int((maxx - minx) / res) + 3, int((maxy - miny) / res) + 3
    if w * h > _MAX_RASTER_PX:
        res *= math.ceil(math.sqrt(w * h / _MAX_RASTER_PX))
        w, h = int((maxx - minx) / res) + 3, int((maxy - miny) / res) + 3
    mask = np.zeros((h, w), dtype=bool)
    xs = [(x - minx) / res + 1 for x, _ in poly.exterior.coords]
    ys = [(y - miny) / res + 1 for _, y in poly.exterior.coords]
    rr, cc = _rasterpoly(np.array(ys), np.array(xs), shape=mask.shape)
    mask[rr, cc] = True
    skel = skeletonize(mask)
    if not skel.any():
        return [a, b]

    def _px(p: XY) -> tuple[int, int]:
        return (int((p[1] - miny) / res) + 1, int((p[0] - minx) / res) + 1)

    def _naechster_skelett_px(p: XY) -> tuple[int, int]:
        r0, c0 = _px(p)
        rs, cs = np.nonzero(skel)
        k = int(np.argmin((rs - r0) ** 2 + (cs - c0) ** 2))
        return int(rs[k]), int(cs[k])

    start, ziel = _naechster_skelett_px(a), _naechster_skelett_px(b)
    # BFS auf dem Skelett (8er-Nachbarschaft).
    vor: dict[tuple[int, int], tuple[int, int] | None] = {start: None}
    q = deque([start])
    while q:
        cur = q.popleft()
        if cur == ziel:
            break
        r, c = cur
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                n = (r + dr, c + dc)
                if (n not in vor and 0 <= n[0] < h and 0 <= n[1] < w
                        and skel[n]):
                    vor[n] = cur
                    q.append(n)
    if ziel not in vor:
        return [a, b]
    px_pfad = []
    p: tuple[int, int] | None = ziel
    while p is not None:
        px_pfad.append(p)
        p = vor[p]
    px_pfad.reverse()
    mm = [(minx + (c - 1) * res, miny + (r - 1) * res) for r, c in px_pfad]
    linie = LineString([a, *mm, b]).simplify(2 * _RASTER_MM)
    return [(float(x), float(y)) for x, y in linie.coords]


# ── (b) Raumgraph + (c) Fallback ─────────────────────────────────────────────
def _klasse(r: Raum) -> str | None:
    # KEIN Rückfall auf `nutzungsklasse_fuer(raum_typ)`: § 6g nennt diese Zeile
    # wörtlich als Stelle des Slices — der Default machte aus einem
    # unbestimmten VORRAUM still WOHNUNG_PRIVAT, also genau die willkürliche
    # Festlegung, die § 6g ausschließt. `bilde_wohnungen` setzt die statischen
    # Defaults vorher; `None` heißt hier ausschließlich „unbestimmt".
    return r.nutzungsklasse


def _final_exit_fehlt_grund(tueren: list[Tuer]) -> str:
    """Warum gibt es keinen final_exit? (Berichts-Text, beste Heuristik)."""
    mit_aussen = [t for t in tueren if AUSSEN in (t.von_raum, t.nach_raum)]
    if mit_aussen:
        return ("Tür(en) nach außen ohne Ausgangs-Rolle "
                f"(z.B. {mit_aussen[0].id}) — Typisierung prüfen")
    # Einseitig ohne Nachbarraum (Raum auf der einen, nichts auf der anderen
    # Seite) = Spec-Grund „Tür ohne Nachbarraum". Beidseits ohne Raum heißt
    # dagegen, dass gar kein Außenbereich erkannt wurde. Gleiche Unterscheidung
    # wie `_untypisiert_grund` (kein_nachbarraum vs. tuer_ins_nichts).
    def _ohne_raum(seite: str | None) -> bool:
        return seite is None or seite == KEIN_RAUM

    if any(_ohne_raum(t.von_raum) != _ohne_raum(t.nach_raum) for t in tueren):
        return "Tür ohne Nachbarraum (eine Türseite keinem Raum zugeordnet)"
    if any(_ohne_raum(t.von_raum) for t in tueren):
        return "Außenbereich nicht erkannt (Türseiten KEIN_RAUM statt AUSSEN)"
    return "keine Tür nach außen erkannt"


def _raum_der_tuer(t: Tuer, erschliessung: dict[str, Raum]) -> Raum | None:
    for s in (t.von_raum, t.nach_raum):
        if s in erschliessung:
            return erschliessung[s]
    return None


def fluchtwege(raeume: list[Raum], tueren: list[Tuer], ausgaenge: list[Ausgang],
               segmente_bisher: list[FluchtwegSegment], geschoss: str = "",
               warnungen: list[str] | None = None,
               durchleitung: list[str] | None = None) -> list[FluchtwegSegment]:
    """GRAPH- und FALLBACK-Segmente ERGÄNZEND zu den bestehenden Segmenten.

    Zielwahl nach Geschoss: **EG/UG** → jeder Weg endet an einem
    ``final_exit`` (stair_exit sind nur Zwischenknoten; je Stiegenhaustür
    entsteht zusätzlich das Segment Stiegenhaustür→nächster final_exit);
    **OG** → Ziel ist der ``stair_exit``. Bei UNBEKANNTem ``geschoss`` wird
    GAR KEIN Ziel gewählt, sondern gewarnt: fail closed hat der Plan dann
    keinen ``final_exit`` (``ausgaenge.ohne_unzulaessige_final_exits``), und
    der Ersatzgriff auf „irgendeinen Ausgang" hätte den Weg an einem
    ``stair_exit`` enden lassen — gezählt als erfüllter Fluchtweg, obwohl
    niemand weiß, ob er ins Freie führt. Das ist das Gegenteil von
    konservativ.

    Startpunkte, in deren Nähe schon eine explizite LINIE verläuft, werden
    übersprungen — der Plan hat dort selbst geplant. ``warnungen`` (optional,
    in-place): Starts im EG/UG ohne erreichbaren final_exit mit Endraum+Grund.
    ``durchleitung`` (optional, in-place): je Segment, das durch einen privaten
    Raum geleitet wurde, eine Berichtszeile (Board-Antrag statt Contract-Feld).

    **Vorbedingung:** ``bilde_wohnungen`` muss vorher gelaufen sein. Seit der
    Rückfall von ``_klasse`` auf ``nutzungsklasse_fuer(raum_typ)`` entfallen
    ist, hat ein Raum ohne gesetzte ``nutzungsklasse`` keine Klasse — dann
    fehlen STIEGENHAUS und die übrigen Erschließungstypen im Türgraph (nur
    GANG/VORRAUM sind über ``volle_knoten`` auch ohne Klasse Knoten), und die
    Wege brechen vor dem Stiegenhaus ab.
    """
    og = ist_obergeschoss(geschoss)
    bekannt = geschoss_bekannt(geschoss)
    durch = durchleitung_raeume(raeume, tueren)
    # Fail-Safe (Owner 2026-09-21): jeder Kandidat, dem die Ankerregel nichts
    # nimmt, bleibt VOLLER Knoten mit eigenen Stützpunkten — unbestimmt wie
    # „privat erst laut Schritt 2". Wer Notlicht behält, behält auch seine
    # Zirkulation.
    weich = volle_knoten(raeume, tueren)
    erschliessung = {r.id: r for r in raeume
                     if (_klasse(r) == "ALLGEMEIN_ERSCHLIESSUNG"
                         or r.id in weich)
                     and len(r.polygon_mm) >= 3}
    # Knoten = eigene Erschließung PLUS die durchgeleiteten privaten Räume.
    knoten = dict(erschliessung)
    knoten.update({r.id: r for r in raeume
                   if r.id in durch and len(r.polygon_mm) >= 3})
    polys = {rid: Polygon(r.polygon_mm).buffer(0)
             for rid, r in knoten.items()}
    linie_punkte = [p for s in segmente_bisher if s.quelle == "LINIE"
                    for p in s.polyline_mm]

    def _gedeckt(xy: XY) -> bool:
        return any(math.dist(xy, p) < _START_GEDECKT_MM for p in linie_punkte)

    # Zieltüren = Türen, auf die ein Ausgang zeigt (exit_<tuer_id>).
    # Geschoss-Regel: OG → stair_exit; EG/UG → final_exit (stair_exit ist
    # dort nur Zwischenknoten). Fallback auf alle, wenn der Zieltyp fehlt
    # (lieber ein Weg zum falschen Ausgangstyp als gar keiner — die Lücke
    # meldet `warnungen`).
    ziel_typ = "stair_exit" if og else "final_exit"
    ziel_ausgaenge = [a for a in ausgaenge if a.typ == ziel_typ]
    if not bekannt:
        # Kein Ziel erfinden: ohne belegtes Geschoss gibt es keinen final_exit,
        # und der Fallback auf `ausgaenge` würde den Weg am stair_exit enden
        # lassen und ihn als erfüllt zählen.
        ziel_ausgaenge = []
        if warnungen is not None:
            warnungen.append(
                f"{GESCHOSS_UNBEKANNT_WARNUNG} — kein Fluchtweg-Ziel "
                "bestimmbar, keine GRAPH-Wege erzeugt")
    elif not ziel_ausgaenge:
        ziel_ausgaenge = ausgaenge
    tuer_by_id = {t.id: t for t in tueren}
    ziele: dict[str, Ausgang] = {}
    for a in ziel_ausgaenge:
        tid = a.id.removeprefix("exit_")
        if tid in tuer_by_id:
            ziele[tid] = a
        else:  # footprint-Ausgang ohne Tür-Referenz → nächste Tür suchen
            nah = min(tueren, key=lambda t: math.dist(t.xy_mm, a.xy_mm),
                      default=None)
            if nah is not None and math.dist(nah.xy_mm, a.xy_mm) < 1500.0:
                ziele.setdefault(nah.id, a)

    # Türgraph: Kante zwischen zwei Türen desselben Knoten-Raums.
    an_raum: dict[str, list[Tuer]] = {rid: [] for rid in knoten}
    for t in tueren:
        for s in (t.von_raum, t.nach_raum):
            if s in an_raum:
                an_raum[s].append(t)
    # Ausgangs-Türen ohne Raum-Zuordnung (Zargen an der Raumkante) trotzdem
    # dem nächstliegenden Erschließungsraum zuschlagen.
    for tid in ziele:
        t = tuer_by_id[tid]
        if any(t in ts for ts in an_raum.values()):
            continue
        nah = min(erschliessung, default=None,
                  key=lambda rid: polys[rid].distance(Point(t.xy_mm)))
        if nah is not None and polys[nah].distance(Point(t.xy_mm)) < _TUER_AN_RAUM_MM:
            an_raum[nah].append(t)

    g = nx.Graph()
    for rid, ts in an_raum.items():
        for i, t1 in enumerate(ts):
            for t2 in ts[i + 1:]:
                d = math.dist(t1.xy_mm, t2.xy_mm)
                if not g.has_edge(t1.id, t2.id) or g[t1.id][t2.id]["w"] > d:
                    g.add_edge(t1.id, t2.id, w=d, raum=rid)

    # Starts: wohnungseingang-Türen + Türen von ALLGEMEIN-Räumen in die
    # Erschließung; im EG/UG zusätzlich jede Stiegenhaustür (Segment
    # Stiegenhaustür → nächster final_exit, der Geschoss-Restweg).
    starts: list[Tuer] = []
    by_id = {r.id: r for r in raeume}
    rollen = korrigierte_rollen(raeume, tueren)
    for t in tueren:
        if rollen[t.id] == "wohnungseingang" or (
                not og and rollen[t.id] == "stiegenhaustuer"):
            starts.append(t)
            continue
        seiten_klassen = {(_klasse(by_id[s]) if s in by_id else None)
                          for s in (t.von_raum, t.nach_raum)}
        # `knoten`, nicht `erschliessung`: ein ALLGEMEIN_NEBENRAUM, dessen Tür
        # DIREKT in einen durchgeleiteten privaten Raum führt, bekäme sonst
        # keine Starttür und damit keinen Weg — genau das Loch, das die
        # Durchleitung verhindern soll (§ 6g: Rennweg UG KINDERWAGENRAUM).
        if "ALLGEMEIN_NEBENRAUM" in seiten_klassen and (
                t.von_raum in knoten or t.nach_raum in knoten):
            starts.append(t)

    out: list[FluchtwegSegment] = []
    kein_finales_ziel = (not og and bekannt
                         and not any(a.typ == "final_exit" for a in ausgaenge))
    if warnungen is not None and kein_finales_ziel and starts:
        warnungen.append(
            "EG/UG ohne final_exit: Wege enden ersatzweise am stair_exit — "
            + _final_exit_fehlt_grund(tueren))
    for start in starts:
        if start.id in ziele or _gedeckt(start.xy_mm):
            continue
        if start.id not in g:
            continue
        erreichbare = [z for z in ziele if z in g and z != start.id]
        best: list[str] | None = None
        best_len = math.inf
        for z in erreichbare:
            try:
                laenge, pfad = nx.single_source_dijkstra(g, start.id, z,
                                                         weight="w")
            except nx.NetworkXNoPath:
                continue
            if laenge < best_len:
                best, best_len = pfad, laenge
        if best is None or len(best) < 2:
            if warnungen is not None and not og and bekannt:
                endraum = next((s for s in (start.von_raum, start.nach_raum)
                                if s not in knoten), start.von_raum)
                grund = (_final_exit_fehlt_grund(tueren) if kein_finales_ziel
                         else "Türgraph endet vor dem Ausgang")
                warnungen.append(
                    f"EG/UG: kein final_exit erreichbar von Tür {start.id} "
                    f"(Endraum {endraum}) — {grund}")
            continue
        punkte: list[XY] = [tuer_by_id[best[0]].xy_mm]
        for a_id, b_id in pairwise(best):
            rid = g[a_id][b_id]["raum"]
            a_xy, b_xy = tuer_by_id[a_id].xy_mm, tuer_by_id[b_id].xy_mm
            # Durchleitung: im privaten Raum KEINE Stützpunkte — Direktlinie
            # Tür zu Tür statt Skelettpfad. ABER nur, wenn das Raumpolygon die
            # Strecke DECKT: bei einem nicht-konvexen Raum (L-Form) verlässt
            # die Direktlinie das Polygon, und das GRAPH-Segment liefe durch
            # eine Wand. Dann bleibt es beim Skelettpfad — lieber Stützpunkte
            # in einem privaten Raum als ein Fluchtweg durch Mauerwerk.
            if rid in durch and polys[rid].covers(LineString([a_xy, b_xy])):
                teil = [a_xy, b_xy]
                if durchleitung is not None:
                    durchleitung.append(
                        f"durchleitung: seg_graph_{start.id} führt durch den "
                        f"privaten Raum {rid} (keine eigene Zirkulation, keine "
                        "Anker, keine Leuchten)")
            else:
                if rid in durch and durchleitung is not None:
                    durchleitung.append(
                        f"durchleitung: seg_graph_{start.id} NICHT direkt durch "
                        f"{rid} geleitet — die Direktlinie verlässt das "
                        "Raumpolygon (nicht konvex); Skelettpfad statt Wand")
                teil = _skelett_pfad(polys[rid], a_xy, b_xy)
            punkte.extend(teil[1:])
        ziel_tuer = best[-1]
        ausgang = ziele[ziel_tuer]
        zt = tuer_by_id[ziel_tuer]
        start_raum = next((s for s in (start.von_raum, start.nach_raum)
                           if s not in knoten), start.von_raum)
        ziel_raum = next((s for s in (zt.von_raum, zt.nach_raum)
                          if s not in knoten), zt.nach_raum)
        out.append(FluchtwegSegment(
            segment_id=f"seg_graph_{start.id}",
            polyline_mm=[(float(x), float(y)) for x, y in punkte],
            laenge_mm=_laenge(punkte), reason="exit", quelle="GRAPH",
            start_raum=start_raum, ziel_raum=ziel_raum,
            ziel_ausgang=ausgang.id))

    # (c) Fallback: COMMUNALER GANG/STIEGENHAUS ohne jedes Segment →
    # Mittelachse. R4 (§ 6f) unter dem Fail-Safe-Riegel: nur auf einem
    # ANKERBESTÄTIGT privaten Gang entsteht kein Fluchtweg-Segment mehr — er
    # trägt nach R3 `ist_communal = False`.
    bestaetigt = bestaetigt_privat(raeume, tueren)
    alle = segmente_bisher + out
    for r in raeume:
        if (r.raum_typ not in ("GANG", "STIEGENHAUS") or r.id in bestaetigt
                or len(r.polygon_mm) < 3):
            continue
        poly = Polygon(r.polygon_mm).buffer(0)
        if poly.is_empty:
            continue
        if any(poly.distance(Point(p)) < 1.0
               for s in alle for p in s.polyline_mm):
            continue
        mrr = poly.minimum_rotated_rectangle
        ecken = list(mrr.exterior.coords)[:4]
        s01, s12 = math.dist(ecken[0], ecken[1]), math.dist(ecken[1], ecken[2])
        if s01 >= s12:  # Mittelachse längs der langen Seite
            a = ((ecken[0][0] + ecken[3][0]) / 2, (ecken[0][1] + ecken[3][1]) / 2)
            b = ((ecken[1][0] + ecken[2][0]) / 2, (ecken[1][1] + ecken[2][1]) / 2)
        else:
            a = ((ecken[0][0] + ecken[1][0]) / 2, (ecken[0][1] + ecken[1][1]) / 2)
            b = ((ecken[2][0] + ecken[3][0]) / 2, (ecken[2][1] + ecken[3][1]) / 2)
        achse = LineString([a, b]).intersection(poly)
        if achse.is_empty or achse.geom_type != "LineString":
            achse = LineString([a, b])
        pts = [(float(x), float(y)) for x, y in achse.coords]
        seg = FluchtwegSegment(
            segment_id=f"seg_fallback_{r.id}", polyline_mm=pts,
            laenge_mm=_laenge(pts), reason=_reason(pts), quelle="FALLBACK",
            start_raum=r.id, richtung_unbekannt=True)
        out.append(seg)
        alle.append(seg)
    return out
