"""anker_strategy — graph-basierte RZ-Platzierung an Entscheidungspunkten.

Die generative Segment-Strategie (`communal_stgh_strategy`) setzt 1 RZ je
Fluchtweg-Segment — gut für dünne Fixtures, aber sie **überproduziert auf realen
Wegenetzen** (Mollgasse: 77 RZ aus 77 WEG-Segmenten). Diese Strategie setzt RZ
stattdessen an den **Ankern des Zirkulationsgraphen**:

* **Kreuzungen** — Knoten mit `degree >= 3` (EN 1838 §4.1.2 f, Pflicht-Betonungspunkt)
* **Ausgänge** — `raum.ausgaenge` (EN 1838 §4.1.2 g)

Die Fluchtrichtung je Anker zeigt **zum nächsten Ausgang** (Gefälle der Dijkstra-
Distanz, `graph.distanz_zu_ausgang`). Nutzt `platzierung/graph.py` (networkx) + die
Richtungs-Blockwahl aus `communal_stgh_strategy`. Render-frei, kein Contract berührt.

Voraussetzung: ein Zirkulationsgraph mit Knoten/Kanten (Selmans echter Graph, Slice 4).
Auf dem dünnen 4OG-Fixture (2 Kanten, keine Kreuzung) liefert sie nur die Ausgänge —
darum bleibt `plan_rettungszeichen` (Segment-basiert) die Default-Strategie, bis der
echte Graph da ist.
"""
from __future__ import annotations

import math

from notbeleuchtung.hauptengine.contracts import (
    FluchtwegSegment,
    NormProvider,
    Platzierung,
    RaumModell,
)

from .communal_stgh_strategy import (
    _AGV_SV_F,
    _building_assigner,
    _richtung_und_rotation,
    _select_key,
)
from .deckungs_zuordnung import HINTERLEUCHTET_DEFAULT
from .graph import build_circulation_graph, distanz_zu_ausgang, kreuzungs_anker


def _node_positions(raum: RaumModell) -> dict[str, tuple[float, float]]:
    pos = {n.id: (n.xy_mm[0], n.xy_mm[1]) for n in raum.zirkulation.nodes}
    pos.update({a.id: (a.xy_mm[0], a.xy_mm[1]) for a in raum.ausgaenge})
    return pos


# Anker näher als das = eine Position (nahe-koinzidente Graph-Knoten sonst → zwei RZ
# unter dem Kollisions-Mindestabstand, echte Doppelplatzierung).
_MIN_RZ_MERGE_MM = 250.0


def _dedupe_anker(anker, pos, exits, G):
    """Near-coincident Anker verschmelzen: Ausgang gewinnt, sonst höherer Graph-Grad."""
    def prio(nid):
        return (0 if nid in exits else 1, -(G.degree(nid) if nid in G else 0), str(nid))
    behalten: list = []
    for nid in sorted(anker, key=prio):
        if nid not in pos:
            continue
        if any(math.hypot(pos[nid][0] - pos[k][0], pos[nid][1] - pos[k][1]) < _MIN_RZ_MERGE_MM
               for k in behalten):
            continue
        behalten.append(nid)
    return behalten


def plan_rettungszeichen_anker(raum: RaumModell, norm: NormProvider) -> list[Platzierung]:
    """RZ an Kreuzungs-Ankern (degree>=3) + Ausgängen, Richtung zum nächsten Ausgang."""
    G = build_circulation_graph(raum)
    if G.number_of_nodes() == 0:
        return []
    pos = _node_positions(raum)
    dist = distanz_zu_ausgang(raum, G)
    # Jeder Ausgang bekommt ein RZ (EN 1838 §4.1.2 g) — auch wenn er KEIN Knoten des
    # Zirkulationsgraphs ist (reale Pläne: Ausgänge liegen oft neben, nicht auf dem
    # Wegenetz). Position kommt aus `pos` (enthält alle ausgaenge), Richtung fällt für
    # graphlose Ausgänge auf „unten" (raus) zurück. Nahe-koinzidente Anker werden vorher
    # verschmolzen (sonst zwei RZ unter Mindestabstand).
    exits = {a.id for a in raum.ausgaenge}
    anker = _dedupe_anker(set(kreuzungs_anker(G)) | exits, pos, exits, G)
    assign_building = _building_assigner([pos[n][0] for n in anker if n in pos])
    exit_pos = [pos[e] for e in exits if e in pos]

    out: list[Platzierung] = []
    for nid in anker:
        if nid not in pos:
            continue
        nx_, ny = pos[nid]
        # Am Ausgang: Pfeil „unten" (Ausgang erreicht). An Kreuzungen: Richtung zum
        # nächsten Ausgang = Nachbar mit kleinster Dijkstra-Distanz (Gefälle-Richtung).
        nbrs = [m for m in G.neighbors(nid) if m in pos and m in dist] if nid in G else []
        if nid not in exits and nbrs and nid in dist:
            tgt = min(nbrs, key=lambda m: dist[m])
            richtung, fallback_rot = _richtung_und_rotation(pos[tgt][0] - nx_, pos[tgt][1] - ny)
        elif nid not in exits and exit_pos:
            # Kreuzung in einer Graph-Komponente OHNE erreichbaren Ausgang (Provider-
            # Lücke, disconnected graph): das Dijkstra-Gefälle existiert nicht. Statt
            # „unten" zu fabrizieren (= Pfeil behauptet „Ausgang erreicht"), zeigt der
            # Pfeil per Luftlinie zum geometrisch nächsten Ausgang — die beste
            # verfügbare Richtungs-Information.
            ex_x, ex_y = min(exit_pos, key=lambda p: math.hypot(p[0] - nx_, p[1] - ny))
            richtung, fallback_rot = _richtung_und_rotation(ex_x - nx_, ex_y - ny)
        else:
            richtung, fallback_rot = "unten", 270.0
        seg = FluchtwegSegment(segment_id=f"anker_{nid}", polyline_mm=[(nx_, ny)], reason="corner")
        anf = norm.fuer_fluchtweg_abschnitt(seg)
        catalog_key, is_directional = _select_key(anf.symbol_katalog_keys, richtung)
        rotation = 0.0 if is_directional else fallback_rot
        mirror_x = False if is_directional else (richtung == "rechts")
        out.append(
            Platzierung(
                xy_mm=(nx_, ny),
                catalog_key=catalog_key,
                rotation_deg=rotation,
                mirror_x=mirror_x,
                height_mm=float(anf.montagehoehe_mm),
                kind="rz",
                richtung=richtung,
                circuit_hint=f"AGV-{assign_building(nx_)}-F{_AGV_SV_F}",
                covers_segment=[],
                norm_quelle=anf.quelle,
            )
        )
    return out


# Sichtlinien-Grenze: max. Abstand zwischen zwei RZ entlang des Gangs. Ist ein
# Gang-Stück länger, muss ein RZ dazwischen (EN 1838 §4.1.1: von jedem Punkt des
# Fluchtwegs ist ein RZ sichtbar). Konservativer Default; exakt = Erkennungsweite l=z·h.
_MAX_RZ_ABSTAND_MM = 12000.0


def richtung_durch_tuer(
    tuer_xy: tuple[float, float], ziel_xy: tuple[float, float]
) -> str:
    """RZ an einer **Tür/Öffnung**: Pfeil zeigt **DURCH die Tür** in Reiserichtung.

    Regel (Owner-Korrektur, PLATZIERUNGS_KONZEPTE Schicht-1-Anker): ein RZ, das an
    einer Tür/Öffnung sitzt, wird **entlang der Schwelle** platziert und der Pfeil
    zeigt **senkrecht durch die Öffnung** — von der Tür zum `ziel_xy` (die nächste Zone
    Richtung Ausgang). Das **überschreibt** das reine Distanz-Gefälle: der Flüchtende
    soll erst die Öffnung durchqueren, dann leitet das nächste RZ weiter. (Beispiel:
    Übergang vertikaler Arm→Gang = Pfeil ↓ durch die Öffnung, nicht ← am Knick vorbei;
    Stiegenhaus-Tür = Pfeil ← durch die Tür ins Stiegenhaus.)
    """
    richtung, _ = _richtung_und_rotation(ziel_xy[0] - tuer_xy[0], ziel_xy[1] - tuer_xy[1])
    return richtung


def plan_rettungszeichen_sichtlinie(
    raum: RaumModell,
    norm: NormProvider,
    *,
    max_abstand_mm: float | None = None,
    piktogramm_hoehe_m: float = 0.15,
    hinterleuchtet: bool = HINTERLEUCHTET_DEFAULT,
) -> list[Platzierung]:
    """RZ nach der Sichtlinien-Regel — **so wenige wie nötig, so sichtbar wie möglich**.

    RZ entstehen an drei Sorten von Punkten, Richtung immer **zum nächsten Ausgang**:

    1. **Ausgänge** — `stair_exit` → Pfeil zur Stiegenhaus-Tür (nach außen: links am
       linken Ende, rechts am rechten); `final_exit` → **raus** (Pfeil unten, ins Freie).
    2. **Stiegenhaus-Transit** — Stiegenhaus-Knoten, die auf dieser Etage KEIN Ausgang
       sind (z.B. EG bei zentralem Hauptausgang): RZ Richtung nächster Ausgang.
    3. **Sichtlinien-Füllung** — ist ein Gang-Stück zwischen zwei RZ länger als
       `max_abstand_mm`, ein RZ dazwischen; genau mittig zwischen zwei gleich weiten
       Ausgängen = Wasserscheide → `richtung='gerade'` (beidseitig).

    **RZ-Dichte = Erkennungsweite `l = z·h`** (EN 1838 §4.1): `max_abstand_mm` wird,
    wenn nicht explizit gesetzt, aus der Norm gezogen — `norm.erkennungsweite_m` mit
    `z` = 200 (hinterleuchtet) / 100 (beleuchtet) und `h` = Piktogramm-Höhe. So folgt
    die Anzahl der RZ dem Sichtbarkeits-Wissen statt einem geratenen Konstanten-Wert:
    ein hinterleuchtetes 0,15-m-Pikto (l=30 m) deckt einen 16-m-Gang ohne Füllung, ein
    kleineres beleuchtetes Pikto braucht Zwischen-RZ.

    So sieht man von jeder Wohnungstür sofort eine Notleuchte, ohne Überproduktion.
    Achse = x (Gang-Hauptrichtung).
    """
    pos = _node_positions(raum)
    # Jeder Ausgang zählt, auch graphlos (§4.1.2 g) — Symmetrie zu plan_rettungszeichen_anker.
    ex = [(a.id, a.typ, pos[a.id]) for a in raum.ausgaenge if a.id in pos]
    if not ex:
        return []
    if max_abstand_mm is None:
        max_abstand_mm = norm.erkennungsweite_m(piktogramm_hoehe_m, hinterleuchtet) * 1000.0
    exit_xs = [p[0] for _, _, p in ex]
    all_xs = [pos[n][0] for n in pos]
    bcx = (min(all_xs) + max(all_xs)) / 2.0          # Gebäude-/Gang-Mitte
    ymid = ex[0][2][1]
    assign = _building_assigner(exit_xs)
    anf = norm.fuer_fluchtweg_abschnitt(
        FluchtwegSegment(segment_id="rz", polyline_mm=[ex[0][2]], reason="exit")
    )
    # Ein Basissymbol „Pfeil nach unten" (Rettungszeichenleuchte), per Rotation
    # ausgerichtet — reale Konvention (eine Leuchte, gedreht) statt separater
    # Links/Rechts-Blöcke. Rotation (DXF, CCW): 0=unten, 90=rechts, 270=links.
    _unten = next(
        (k for k in anf.symbol_katalog_keys if k.endswith("_unten")),
        (anf.symbol_katalog_keys or ["notlicht_ks_stiege_unten"])[0],
    )
    _ROT = {"unten": 0.0, "rechts": 90.0, "links": 270.0, "gerade": 0.0}

    def mk(x: float, y: float, richtung: str) -> Platzierung:
        return Platzierung(
            xy_mm=(x, y), catalog_key=_unten, rotation_deg=_ROT[richtung], mirror_x=False,
            height_mm=float(anf.montagehoehe_mm), kind="rz", richtung=richtung,
            circuit_hint=f"AGV-{assign(x)}-F{_AGV_SV_F}", covers_segment=[], norm_quelle=anf.quelle,
        )

    def richtung_zum_ausgang(x: float) -> str:
        d = sorted((abs(x - ex_x), ex_x) for ex_x in exit_xs)
        if len(d) >= 2 and abs(d[0][0] - d[1][0]) < 0.15 * max_abstand_mm and d[0][0] > 1.0:
            return "gerade"                            # Wasserscheide → beidseitig
        return "rechts" if d[0][1] > x else "links"

    out: list[Platzierung] = []
    placed: list[float] = []
    # 1. Ausgänge
    for _aid, typ, (x, y) in ex:
        richtung = ("links" if x < bcx else "rechts") if typ == "stair_exit" else "unten"
        out.append(mk(x, y, richtung)); placed.append(x)
    # 2. Stiegenhaus-Transit (kein Ausgang auf dieser Etage → zeigt zum Ausgang)
    for n in raum.zirkulation.nodes:
        if n.typ == "stair" and n.id not in {e[0] for e in ex}:
            x = pos[n.id][0]
            out.append(mk(x, pos[n.id][1], richtung_zum_ausgang(x))); placed.append(x)
    # 3. Sichtlinien-Füllung: Lücken zwischen aufeinanderfolgenden RZ > max_abstand
    for a, b in zip(sorted(placed), sorted(placed)[1:]):
        gap = b - a
        for k in range(1, max(0, math.ceil(gap / max_abstand_mm) - 1) + 1):
            fx = a + gap * k / (math.ceil(gap / max_abstand_mm))
            out.append(mk(fx, ymid, richtung_zum_ausgang(fx)))
    return out

