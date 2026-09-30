"""tueren — Türen aus dem Plan → ``Tuer``-Contract-Objekte (F2→F1-Naht).

F1 (`richtung_durch_tuer`) konsumiert `RaumModell.tueren` an den ECHTEN Öffnungen
— darum müssen hier alle Familien echte Türen liefern. Drei Darstellungen:

1. **Benannte Tür-Blöcke** (Mollgasse ``TÜR-80…`` / Fischamender ``…_Zimmertür``,
   Baufeld ``Öffnung_N``): Position = INSERT-Punkt, Breite ggf. aus Blockname.
2. **Schwenkbögen** (ArchiCAD: Barawitzka/Herrenholz — Türen ohne Block, nur ARC):
   je Türblatt-ARC (r≈600–1300 mm) eine Tür am Drehpunkt. Fallback, wenn (1) leer.

**Außentüren** (``WET_AUSSEN``/``SCHIEBETÜR``/…) tragen ``ist_notausgang=True``.

**Kein Maß wird erfunden:** Beschriftungs-Fahnen (Blockname „Beschriftung", z.B.
Muthgasse ``HNP_Beschriftung Türen … Durchgangslichte…``) heißen nach Türen,
sind aber keine — ``_DOOR_EXCLUDE`` verwirft sie, statt sie mit ``breite_mm=None``
als Tür zu führen. Verworfene Kandidaten stehen in ``_verworfene_bloecke``.
"""
from __future__ import annotations

import logging
import math
import re
from dataclasses import dataclass

from notbeleuchtung.hauptengine.contracts.raum_modell import BBox, Tuer

from .dxf_load import XY, DxfPlan

log = logging.getLogger(__name__)

#: Blockname → Anzahl verworfener Tür-Kandidaten (Marker/Beschläge/Fahnen).
#: Prozessweiter Zähler, damit der Ausschluss nachvollziehbar bleibt.
_verworfene_bloecke: dict[str, int] = {}

# Kandidat: Blockname nennt eine Tür/Öffnung …
_DOOR_HINT = re.compile(r"T(?:Ü|UE)R|ÖFFNUNG|OEFFNUNG|\bBST\b|F\+H", re.IGNORECASE)
# … aber diese sind Marker/Beschläge/Beschriftungs-Fahnen, keine Tür-Blätter.
# BESCHRIFT: Muthgasse trägt 83 INSERTs "HNP_Beschriftung Türen - AF 50 -
# Durchgangslichte…" — Blockdef = 1× LINE (Führungslinie), keine Türgeometrie.
# Gemessen (alle fünf Prüfpläne): fängt 83/83 Fahnen, 0 echte Türen.
_DOOR_EXCLUDE = re.compile(r"ACHSE|ÖFFNER|OEFFNER|QUALIT|BESCHRIFT", re.IGNORECASE)
# Außen-/Eingangstür-Blöcke → Ausgang. WET = Wohnungseingangstür.
_AUSSENTUER = re.compile(r"AUSSEN|EINGANG|\bWET\b|WET_|SCHIEBET|FENSTERT", re.IGNORECASE)
_OEFFNUNG = re.compile(r"ÖFFNUNG|OEFFNUNG", re.IGNORECASE)
_INT = re.compile(r"\d+")

_ARC_MIN_MM, _ARC_MAX_MM = 600.0, 1300.0  # Türblatt-Schwenkbogen-Radius


def _ist_tuer_block(name: str) -> bool:
    if _DOOR_EXCLUDE.search(name):
        # Nicht stillschweigend verwerfen: verworfene Kandidaten je Blockname
        # zählbar (``_verworfene_bloecke``) + im Log nachvollziehbar.
        if _DOOR_HINT.search(name) or _AUSSENTUER.search(name):
            _verworfene_bloecke[name] = _verworfene_bloecke.get(name, 0) + 1
            log.debug("Tuer-Kandidat verworfen (Marker/Beschriftung): %s", name)
        return False
    return bool(_DOOR_HINT.search(name) or _AUSSENTUER.search(name))


def _ist_aussentuer(name: str) -> bool:
    return bool(_AUSSENTUER.search(name)) and not _DOOR_EXCLUDE.search(name)


#: Grund für ``breite_quelle="UNBEKANNT"``, wenn der Blockname kein Maß trägt.
_GRUND_BLOCKNAME = "Blockname traegt kein Breitenmass (Oeffnungs-Marker oder kein cm/mm-Token)"


def _breite_mm(name: str) -> float | None:
    """Nennbreite in mm: erste Zahl im cm-Türbereich (60–130) × 10.

    Öffnungs-Marker (``Öffnung_81``) tragen eine ID, keine Breite → ``None``
    (v1.4.0: keine Messung ist None, nicht 0.0).
    """
    if _OEFFNUNG.search(name):
        return None
    for tok in _INT.findall(name):
        n = int(tok)
        if 60 <= n <= 130:        # cm-Konvention (TÜR-80)
            return float(n) * 10.0
        if 600 <= n <= 1300:      # mm direkt (…_0800x2000)
            return float(n)
    return None


def _block_tueren(plan: DxfPlan) -> list[Tuer]:
    out: list[Tuer] = []
    for e in plan.entities():
        if e.dxftype() != "INSERT" or not _ist_tuer_block(e.dxf.name):
            continue
        (xy,) = plan.entity_points(e) or [(0.0, 0.0)]
        b = _breite_mm(e.dxf.name)
        out.append(Tuer(id=f"tuer_{len(out) + 1}", xy_mm=xy,
                        breite_mm=b,
                        breite_quelle="BLOCKNAME" if b is not None else "UNBEKANNT",
                        breite_grund=None if b is not None else _GRUND_BLOCKNAME,
                        ist_notausgang=_ist_aussentuer(e.dxf.name),
                        quelle="block"))
    return out


def _arc_tueren(plan: DxfPlan) -> list[Tuer]:
    """Fallback (ArchiCAD): Tür-Schwenkbögen → Tür am Drehpunkt, Breite = Radius."""
    out: list[Tuer] = []
    for e in plan.entities():
        if e.dxftype() != "ARC":
            continue
        r = float(e.dxf.radius) * plan.factor
        if _ARC_MIN_MM < r < _ARC_MAX_MM:
            out.append(Tuer(id=f"tuer_{len(out) + 1}",
                            xy_mm=plan._scale(e.dxf.center), breite_mm=round(r),
                            breite_quelle="GEOMETRIE_SCHWENKRADIUS",
                            quelle="arc"))
    return out


def tueren_aus_dxf(plan: DxfPlan) -> list[Tuer]:
    """Türen aller Familien → ``Tuer``. Benannte Blöcke zuerst; sonst Schwenkbögen."""
    out = _block_tueren(plan)
    if not out:
        out = _arc_tueren(plan)
    return out


# ── Türöffnungen (auch IN Blockdefinitionen) ─────────────────────────────────
_SWEEP_MIN, _SWEEP_MAX = 60.0, 120.0  # Türblatt schwenkt ~90°


@dataclass
class TuerOeffnung:
    """Eine Türöffnung — Position + Nennbreite, quelle 'block' oder 'arc'."""

    xy_mm: XY
    breite_mm: float | None
    winkel_grad: float | None
    quelle: str
    #: Herkunft von ``breite_mm`` (Contract-Vokabular ``BreiteQuelle``, v1.4.0).
    breite_quelle: str = "UNBEKANNT"
    #: Warum keine Breite gemessen werden konnte (nur bei ``UNBEKANNT``).
    breite_grund: str | None = None
    #: Name des umgebenden Wand-Blocks — nur bei Weltkoordinaten-Blöcken
    #: gesetzt, deren Lage aus der Blockgeometrie stammt (s. ``_blockgeometrie``).
    wand_block: str | None = None


def _blattbreite_aus_block(insert, factor: float, tiefe: int = 0) -> float | None:
    """Türblatt-Breite = Radius des Schwenkbogen-ARC in der Blockdefinition
    (Rennweg-Zargentüren tragen keine Breite im Namen). Spiegelung (xscale=-1)
    ist egal — der Radius ist skaleninvariant bei |scale|=1."""
    try:
        for v in insert.virtual_entities():
            if v.dxftype() == "ARC":
                r = float(v.dxf.radius) * factor
                if _ARC_MIN_MM < r < _ARC_MAX_MM:
                    return float(round(r))
            elif v.dxftype() == "INSERT" and tiefe < 2:
                r = _blattbreite_aus_block(v, factor, tiefe + 1)
                if r:
                    return r
    except Exception:  # noqa: BLE001, S110 — kaputter Block liefert eben keine Breite
        pass
    return None


#: Grund für ``breite_quelle="UNBEKANNT"`` bei einem Türblock ohne Schwenkbogen.
_GRUND_OHNE_BOGEN = ("Tuerblock ohne Schwenkbogen (Schiebetuer): keine messbare "
                     "Blattbreite")
_SCHARNIER_TOL_MM = 150.0   # Blatt-/Öffnungslinie beginnt am Drehpunkt
_BLATT_MIN, _BLATT_MAX = 0.75, 1.25   # Länge einer blattlangen Linie / Radius
_SPITZE_TOL = 0.35          # Abstand zum ARC-Endpunkt / Radius


def _skaliere(p, factor: float) -> XY:
    return (float(p[0]) * factor, float(p[1]) * factor)


def _block_geometrie_teile(insert, factor: float, tiefe: int = 0):
    """(Segmente in mm, Türblatt-ARCs) der Blockgeometrie, rekursiv bis Tiefe 2."""
    segs: list[tuple[XY, XY]] = []
    arcs: list = []
    try:
        for v in insert.virtual_entities():
            t = v.dxftype()
            if t == "LINE":
                segs.append((_skaliere(v.dxf.start, factor),
                             _skaliere(v.dxf.end, factor)))
            elif t == "LWPOLYLINE":
                pts = [_skaliere(p, factor) for p in v.get_points("xy")]
                segs += [(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
            elif t == "ARC":
                r = float(v.dxf.radius) * factor
                sweep = (float(v.dxf.end_angle) - float(v.dxf.start_angle)) % 360.0
                if _ARC_MIN_MM < r < _ARC_MAX_MM and _SWEEP_MIN <= sweep <= _SWEEP_MAX:
                    arcs.append(v)
            elif t == "INSERT" and tiefe < 2:
                s2, a2 = _block_geometrie_teile(v, factor, tiefe + 1)
                segs += s2
                arcs += a2
    except Exception:  # noqa: BLE001, S110 — kaputter Block liefert eben keine Geometrie
        pass
    return segs, arcs


def _blockgeometrie(insert, factor: float) -> TuerOeffnung | None:
    """Lage/Sehne/Breite eines Türblocks aus seiner GEOMETRIE (nicht dem INSERT).

    ArchiCAD-Exporte (Rennweg) zeichnen Blockinhalte in Weltkoordinaten und
    setzen ``base_point`` ≈ INSERT-Punkt; der INSERT-Punkt ist dann ein
    gemeinsamer Anker weit außerhalb des Plans, die echte Türlage steckt nur
    in der Geometrie.

    Mit Schwenkbogen: Scharnier = ARC-Zentrum, Sehne = Scharnier → Wandseite,
    ``xy`` = Sehnenmitte, Breite = Radius. Die Wandseite ist der ARC-Endpunkt
    mit den MEISTEN blattlangen Linien am Scharnier: ArchiCAD zeichnet die
    Öffnung als geschlossenes Blatt-Rechteck LÄNGS der Wand (≥ 2 Linien) und
    die offene Blattstellung mit EINER Linie quer dazu (gemessen an allen 7
    Zargentüren auf Rennweg OG1 — der Wand-Endpunkt liegt dort 28 mm, der
    Blatt-Endpunkt 341–860 mm vom nächsten Wandkörper entfernt, und die Sehne
    zeigt in die Längsrichtung des umgebenden ``Wall_*``-Blocks). Gleichstand
    → start_angle-Endpunkt (Konvention des Ports).

    Ohne Schwenkbogen (Schiebetür): ``xy`` = Mitte der Geometrie-Bbox, Winkel =
    Richtung der längsten Kante, Breite None mit Grund — kein Standardwert.
    """
    segs, arcs = _block_geometrie_teile(insert, factor)
    if arcs:
        a = arcs[0]
        c = _skaliere(a.dxf.center, factor)
        r = float(a.dxf.radius) * factor
        enden = [(c[0] + r * math.cos(math.radians(w)),
                  c[1] + r * math.sin(math.radians(w)))
                 for w in (float(a.dxf.start_angle), float(a.dxf.end_angle))]
        treffer = [0, 0]
        for s0, s1 in segs:
            if not (_BLATT_MIN * r <= math.dist(s0, s1) <= _BLATT_MAX * r):
                continue
            for nah, fern in ((s0, s1), (s1, s0)):
                if math.dist(nah, c) > _SCHARNIER_TOL_MM:
                    continue
                for i, ende in enumerate(enden):
                    if math.dist(fern, ende) <= _SPITZE_TOL * r:
                        treffer[i] += 1
                        break
        wand = enden[0] if treffer[0] >= treffer[1] else enden[1]
        return TuerOeffnung(
            xy_mm=((c[0] + wand[0]) / 2.0, (c[1] + wand[1]) / 2.0),
            breite_mm=float(round(r)),
            winkel_grad=math.degrees(math.atan2(wand[1] - c[1], wand[0] - c[0])) % 180.0,
            quelle="block", breite_quelle="GEOMETRIE_SCHWENKRADIUS")
    if not segs:
        return None
    xs = [p[0] for s in segs for p in s]
    ys = [p[1] for s in segs for p in s]
    a, b = max(segs, key=lambda s: math.dist(*s))
    return TuerOeffnung(
        xy_mm=((min(xs) + max(xs)) / 2.0, (min(ys) + max(ys)) / 2.0),
        breite_mm=None,
        winkel_grad=math.degrees(math.atan2(b[1] - a[1], b[0] - a[0])) % 180.0,
        quelle="block", breite_quelle="UNBEKANNT", breite_grund=_GRUND_OHNE_BOGEN)


def tuer_oeffnungen(plan: DxfPlan,
                    planbereich: BBox | None = None) -> list[TuerOeffnung]:
    """Alle Türöffnungen — Tür-Blöcke UND Schwenkbogen-ARCs, auch INNERHALB von
    Blockdefinitionen (virtual_entities-Walk, Tiefe ≤3). In Tür-Blöcke wird
    nicht hinein-rekursiert (deren ARC ist das Türblatt, keine zweite Tür).

    ``planbereich`` (Bounding-Box der Wandkörper): Liegt der INSERT-Punkt eines
    Türblocks außerhalb, aber seine GEOMETRIE innerhalb, wird die Öffnung aus
    der Geometrie gebaut (Weltkoordinaten-Blöcke, s. ``_blockgeometrie``) und
    trägt den Namen des umgebenden Blocks als ``wand_block``. Ohne
    ``planbereich`` — und für jeden Block, dessen INSERT-Punkt an der Tür sitzt
    — bleibt alles wie bisher.
    """
    out: list[TuerOeffnung] = []

    def _walk(entities, tiefe: int = 0, eltern: str | None = None) -> None:
        for e in entities:
            t = e.dxftype()
            if t == "INSERT":
                name = str(e.dxf.name)
                if _ist_tuer_block(name):
                    xy = plan._scale(e.dxf.insert)
                    geo = None
                    if planbereich is not None and not _im_bereich(xy, planbereich):
                        geo = _blockgeometrie(e, plan.factor)
                        if geo is not None and not _im_bereich(geo.xy_mm, planbereich):
                            geo = None
                    breite = _breite_mm(name)
                    if geo is not None:
                        if breite is not None:      # Blockname schlägt Geometrie
                            geo.breite_mm, geo.breite_quelle = breite, "BLOCKNAME"
                            geo.breite_grund = None
                        geo.wand_block = eltern
                        out.append(geo)
                    else:
                        b_quelle = "BLOCKNAME"
                        if breite is None:
                            breite = _blattbreite_aus_block(e, plan.factor)
                            b_quelle = ("GEOMETRIE_SCHWENKRADIUS" if breite is not None
                                        else "UNBEKANNT")
                        out.append(TuerOeffnung(
                            xy_mm=xy, breite_mm=breite,
                            winkel_grad=float(e.dxf.get("rotation", 0.0)),
                            quelle="block", breite_quelle=b_quelle))
                elif tiefe < 3:
                    try:
                        _walk(e.virtual_entities(), tiefe + 1, name)
                    except Exception:  # noqa: BLE001, S110 — kaputter Block killt den Walk nicht
                        pass
            elif t == "ARC":
                r = float(e.dxf.radius) * plan.factor
                sweep = (float(e.dxf.end_angle) - float(e.dxf.start_angle)) % 360.0
                if _ARC_MIN_MM < r < _ARC_MAX_MM and _SWEEP_MIN <= sweep <= _SWEEP_MAX:
                    out.append(TuerOeffnung(
                        xy_mm=plan._scale(e.dxf.center), breite_mm=float(round(r)),
                        winkel_grad=float(e.dxf.start_angle), quelle="arc",
                        breite_quelle="GEOMETRIE_SCHWENKRADIUS"))

    _walk(plan.space)
    return out


# ── Zusätzliche Türquellen (Fachteil „Türquellen", additiv) ──────────────────
_TUER_NAH_MM = 600.0        # bestehende Tür „deckt" eine Öffnung in dem Radius
_AUSSEN_PROBE_MM = 500.0    # Probekreis um den Öffnungs-Drehpunkt
_DOPPEL_TOL_MM = 300.0      # |Zentrenabstand − (b1+b2)| einer Doppelflügel-Tür
_WAND_NAH_MM = 250.0        # Drehpunkt liegt an einer Wand
_PARALLEL_TOL_GRAD = 15.0
_TEXT_TUER_NAH_MM = 1500.0


def aussentor_tueren(oeffnungen: list[TuerOeffnung], tueren: list[Tuer],
                     kontur) -> list[Tuer]:
    """Tür-Schwenkbögen an der AUSSEN-Grenze, die kein Tür-Block deckt.

    Auf Block-Familien (Mollgasse) liefert ``tueren_aus_dxf`` nur die
    benannten Blöcke — Hof-/Gartentüren sind dort aber reine ARCs. Eine
    Öffnung zählt, wenn ein Probepunkt (Kreis r=500 mm um den Drehpunkt)
    außerhalb der gedeckten Fläche liegt (= AUSSEN, s. aussenbereich).
    """
    if kontur is None or kontur.is_empty:
        return []
    from shapely.geometry import Point
    from shapely.prepared import prep
    deck = prep(kontur)
    grenze = kontur.boundary
    punkte = [t.xy_mm for t in tueren]
    out: list[Tuer] = []
    for o in oeffnungen:
        if o.quelle != "arc" or not o.breite_mm:
            continue
        if any(math.dist(o.xy_mm, p) < _TUER_NAH_MM for p in punkte):
            continue
        proben = [(o.xy_mm[0] + _AUSSEN_PROBE_MM * math.cos(w),
                   o.xy_mm[1] + _AUSSEN_PROBE_MM * math.sin(w))
                  for w in (k * math.pi / 4 for k in range(8))]
        # AUSSEN-grenznah: ein Probepunkt liegt draußen ODER der Drehpunkt
        # sitzt direkt an der AUSSEN-Grenze (Türblatt schlägt nach innen auf,
        # der Bogen bleibt dann komplett im gedeckten Bereich).
        if (not any(not deck.covers(Point(p)) for p in proben)
                and grenze.distance(Point(o.xy_mm)) > _AUSSEN_PROBE_MM):
            continue
        out.append(Tuer(id=f"aussentor_{len(out) + 1}", xy_mm=o.xy_mm,
                        breite_mm=o.breite_mm, breite_quelle=o.breite_quelle,
                        quelle="arc_aussen"))
        punkte.append(o.xy_mm)
    return out


def _wandwinkel_bei(segs, xy: XY, max_mm: float = _WAND_NAH_MM) -> float | None:
    """Winkel (Grad, mod 180) des nächsten Wandsegments ≤ max_mm, sonst None."""
    best_d, best_w = max_mm, None
    for a, b in segs:
        seg_len = math.dist(a, b)
        if seg_len < 1.0:
            continue
        t = max(0.0, min(1.0, ((xy[0] - a[0]) * (b[0] - a[0])
                               + (xy[1] - a[1]) * (b[1] - a[1])) / seg_len**2))
        proj = (a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1]))
        d = math.dist(xy, proj)
        if d < best_d:
            best_d = d
            best_w = math.degrees(math.atan2(b[1] - a[1], b[0] - a[0])) % 180.0
    return best_w


def verschmelze_doppelfluegel(tueren: list[Tuer], wand_segs) -> list[Tuer]:
    """Doppelflügel-Türen: zwei Schwenkbögen an der GEMEINSAMEN Wand, deren
    Drehpunkt-Abstand ≈ Summe der Blattbreiten ist → EINE Tür mit Gesamtbreite.

    Die Wand-Kollinearität (Verbindungslinie ∥ Wand an beiden Drehpunkten)
    schließt gegenüberliegende Gangtüren aus (deren Verbindung steht senkrecht
    auf den Wänden). Nur ARC-Quellen — Block-Türen tragen ihre Breite selbst.
    """
    arcs = [t for t in tueren if t.quelle in ("arc", "arc_aussen")
            and t.breite_mm is not None
            and _ARC_MIN_MM < t.breite_mm < _ARC_MAX_MM]
    verbraucht: set[str] = set()
    neu: list[Tuer] = []
    for i, t1 in enumerate(arcs):
        if t1.id in verbraucht:
            continue
        for t2 in arcs[i + 1:]:
            if t2.id in verbraucht:
                continue
            d = math.dist(t1.xy_mm, t2.xy_mm)
            if abs(d - (t1.breite_mm + t2.breite_mm)) > _DOPPEL_TOL_MM:
                continue
            w_verb = math.degrees(math.atan2(
                t2.xy_mm[1] - t1.xy_mm[1], t2.xy_mm[0] - t1.xy_mm[0])) % 180.0
            w1 = _wandwinkel_bei(wand_segs, t1.xy_mm)
            w2 = _wandwinkel_bei(wand_segs, t2.xy_mm)
            if w1 is None or w2 is None:
                continue
            if any(min(abs(w_verb - w), 180.0 - abs(w_verb - w))
                   > _PARALLEL_TOL_GRAD for w in (w1, w2)):
                continue
            mitte = ((t1.xy_mm[0] + t2.xy_mm[0]) / 2,
                     (t1.xy_mm[1] + t2.xy_mm[1]) / 2)
            neu.append(Tuer(id=f"doppel_{len(neu) + 1}", xy_mm=mitte,
                            breite_mm=t1.breite_mm + t2.breite_mm,
                            breite_quelle="GEOMETRIE_SUMME",
                            quelle="doppelfluegel"))
            verbraucht |= {t1.id, t2.id}
            break
    if not neu:
        return tueren
    return [t for t in tueren if t.id not in verbraucht] + neu


# Texte, die eine Tür/einen Eingang implizieren — stark genug, um OHNE
# gezeichnetes Türblatt eine Tür anzulegen (Rennweg EG: 'TÜRSCHLIESSER'
# an einer 1340-mm-Wandlücke, kein Schwenkbogen, kein Block).
_TEXT_TUER = re.compile(
    r"T(?:Ü|UE|.)RSCHLIE|AUTOMATIKT|SCHIEBET(?:Ü|UE|.)R|EINGANG"
    r"|WINDFANG|NOTAUSGANG|FLUCHTT(?:Ü|UE|.)R|PANIKBESCHLAG"
    # Ausgangs-Kennungen/Anlagen-Kürzel nur als eigenständiges Token
    # (sonst matcht E1 in "BE12", BST in "ABSTAND").
    r"|\bE[12]\b|\bBST\b|\bRWA\b",
    re.IGNORECASE)


def tuer_texte(plan: DxfPlan) -> list[tuple[str, XY]]:
    """(Text, Position mm) aller türimplizierenden Texte im Plan."""
    out: list[tuple[str, XY]] = []
    for e in plan.entities():
        t = e.dxftype()
        if t == "MTEXT":
            text, ins = e.plain_text(), e.dxf.insert
        elif t == "TEXT":
            text, ins = e.dxf.text, e.dxf.insert
        else:
            continue
        if _TEXT_TUER.search(text or ""):
            out.append((text.strip(), plan._scale(ins)))
    return out


def text_tueren(plan: DxfPlan, tueren: list[Tuer]) -> list[Tuer]:
    """Türen aus türimplizierenden Texten OHNE gezeichnete Tür ≤ 1.5 m.

    Position = Textposition (die Öffnung liegt daneben — gut genug für
    Zuordnung + Ausgangs-Ableitung); Breite unbekannt (None, nichts erfinden);
    ``quelle`` trägt den Text als Begründung.
    """
    punkte = [t.xy_mm for t in tueren]
    out: list[Tuer] = []
    for text, xy in tuer_texte(plan):
        if any(math.dist(xy, p) < _TEXT_TUER_NAH_MM for p in punkte):
            continue
        out.append(Tuer(id=f"texttuer_{len(out) + 1}", xy_mm=xy,
                        breite_mm=None, breite_quelle="UNBEKANNT",
                        breite_grund="nur Text-Beleg, keine Geometrie",
                        quelle=f"text:{text[:40]}"))
        punkte.append(xy)
    return out


# ── Plan-Bereich: Phantom-Türen anderer Plan-Cluster verwerfen ───────────────
_RAND_MM = 2000.0


def _im_bereich(xy: XY, bounds: BBox, rand_mm: float = _RAND_MM) -> bool:
    (x0, y0), (x1, y1) = bounds.min_xy, bounds.max_xy
    return (x0 - rand_mm <= xy[0] <= x1 + rand_mm
            and y0 - rand_mm <= xy[1] <= y1 + rand_mm)


def im_planbereich(elemente: list, bounds: BBox, rand_mm: float = _RAND_MM) -> list:
    """Nur Elemente mit ``xy_mm`` innerhalb ``bounds`` + Rand.

    ``bounds`` = Bounding-Box der Wandkörper (die filtern Duplikat-Etagen-
    Varianten schon über ``wandkoerper._varianten_prefix``). Damit fallen die
    Phantom-Türen weg, die sonst beidseits AUSSEN landen: Barawitzka trägt
    dieselbe Etage 3× nebeneinander (Icon-Varianten, +32 m / +61 m versetzt).

    Rennwegs Zargen-INSERTs sind KEIN zweiter Plan-Cluster (so stand es hier
    bis S4a): es sind Weltkoordinaten-Blöcke, die sich alle denselben
    INSERT-Punkt weit außerhalb des Grundrisses teilen, während ihre Geometrie
    mitten im Plan liegt. Ihre Öffnungen kommen seit S4a mit der Geometrie-Lage
    aus ``tuer_oeffnungen`` und werden hier deshalb nicht mehr verworfen.
    """
    return [e for e in elemente if _im_bereich(e.xy_mm, bounds, rand_mm)]
