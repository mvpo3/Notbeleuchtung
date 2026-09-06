"""Raum-Kaskade L→H→F→R — eine Quelle der Wahrheit für Skript und Provider.

Gehoben aus ``scripts/plan_pruefen._raum_kaskade``; die Prüfstrecke und
``provider.ArchitekturRaumProvider.parse`` nutzen dieselbe Orchestrierung, damit
die Engine-Pipeline (Leonis) exakt die Räume der Prüfstrecke bekommt.

L: ``raeume_aus_layer`` · H: ``raeume_aus_hatch`` additiv (IoU-Dedup gegen L)
· F: ``flute_stempel`` für Stempel ohne brauchbares Polygon · R:
``komponenten_ohne_stempel`` für den stempellosen Rest.
"""
from __future__ import annotations

import math
from collections import Counter
from dataclasses import dataclass, field

from shapely.geometry import Point, Polygon

from notbeleuchtung.hauptengine.contracts.raum_modell import Raum

from .dxf_load import DxfPlan
from .raumlayer import raeume_aus_hatch, raeume_aus_layer
from .raumtyp import raumtyp_flags
from .rest_komponenten import komponenten_ohne_stempel
from .stempel_anker import Stempel, Zuordnung, finde_stempel, ordne_zu
from .stempel_flutung import flute_stempel
from .tueren import TuerOeffnung, tuer_oeffnungen
from .wandkoerper import Wandkoerper, finde_wandkoerper


def iou(poly_a: list, poly_b: list) -> float:
    """Intersection over Union zweier Punktlisten-Polygone (mm)."""
    a, b = Polygon(poly_a).buffer(0), Polygon(poly_b).buffer(0)
    if a.is_empty or b.is_empty:
        return 0.0
    u = a.union(b).area
    return a.intersection(b).area / u if u > 0 else 0.0


@dataclass
class KaskadeErgebnis:
    """Räume der Kaskade plus die Nebenprodukte, die Aufrufer weiterverwenden."""

    zuordnungen: list[Zuordnung] = field(default_factory=list)
    raeume: list[Raum] = field(default_factory=list)
    rest_raeume: list[Raum] = field(default_factory=list)
    quelle: dict[str, str] = field(default_factory=dict)   # raum.id -> L/H/F/R
    kette: str = ""
    wandkoerper: list[Wandkoerper] = field(default_factory=list)
    tueroeffnungen: list[TuerOeffnung] = field(default_factory=list)

    @property
    def alle_raeume(self) -> list[Raum]:
        return self.raeume + self.rest_raeume


def _ein_polygon_ein_stempel(zuord: list[Zuordnung]) -> None:
    """Ein Polygon gehört genau EINEM Stempel — in-place.

    ``ordne_zu`` heftet bei Plänen ohne Raum-Layer (Mollgasse: H-Polygone aus
    Hatches) bis zu 11 Stempel ans selbe Polygon; die berechneten Flächen sind
    dann für alle bis auf einen falsch. Es bleibt der beste Flächen-Match, die
    übrigen gehen als ``kein_polygon`` zurück in die Flutung.
    """
    je_polygon: dict[int, list[int]] = {}
    for k, z in enumerate(zuord):
        if z.polygon_index is not None:
            je_polygon.setdefault(z.polygon_index, []).append(k)
    for kandidaten in je_polygon.values():
        if len(kandidaten) < 2:
            continue
        best = min(kandidaten, key=lambda k: abs(zuord[k].abweichung_prozent)
                   if zuord[k].abweichung_prozent is not None else math.inf)
        for k in kandidaten:
            if k != best:
                zuord[k] = Zuordnung(zuord[k].stempel, None, None, None, "kein_polygon")


def raeume_aus_kaskade(plan: DxfPlan,
                       stempel: list[Stempel] | None = None) -> KaskadeErgebnis:
    """Raum-Kaskade L→H→F→R über einen geladenen Plan.

    ``stempel``: bereits gefundene Raumstempel; ``None`` → ``finde_stempel``.
    """
    if stempel is None:
        stempel = finde_stempel(plan)
    raeume = raeume_aus_layer(plan)
    quelle: dict[str, str] = {r.id: "L" for r in raeume}
    for r in raeume_aus_hatch(plan, stempel):
        if any(iou(r.polygon_mm, v.polygon_mm) > 0.5 for v in raeume):
            continue
        r.id = f"raum_{len(raeume) + 1}"
        raeume.append(r)
        quelle[r.id] = "H"
    wk = finde_wandkoerper(plan)
    oeff = tuer_oeffnungen(plan)
    zuord = ordne_zu(stempel, raeume)
    _ein_polygon_ein_stempel(zuord)
    flut_i = [
        k for k, z in enumerate(zuord)
        if z.flag == "kein_polygon"
        or (z.flag != "ok" and z.raum is not None
            and not Polygon(z.raum.polygon_mm).buffer(0).covers(
                Point(z.stempel.position_mm)))
    ]
    if flut_i and wk:
        fluts = flute_stempel(plan, [zuord[k].stempel for k in flut_i], wk, oeff)
        for k, fr in zip(flut_i, fluts):
            # Degenerierte Flutungen (<1 m², z.B. Stempel in Wandtasche) blocken
            # sonst die Rest-Stufe — dort typt sie der STIEGE-/LIFT-Marker besser.
            if len(fr.polygon_mm) < 3 or Polygon(fr.polygon_mm).area < 1e6:
                zuord[k] = Zuordnung(fr.stempel, None, None, None, "kein_polygon")
                continue
            st = fr.stempel
            tf = raumtyp_flags(st.name or "")
            typ, flucht, communal = tf if tf else (st.typ or "", False, False)
            r = Raum(id=f"raum_{len(raeume) + 1}", raum_typ=typ,
                     polygon_mm=[(float(x), float(y)) for x, y in fr.polygon_mm],
                     flaeche_m2=Polygon(fr.polygon_mm).area / 1e6,
                     ist_fluchtweg=flucht, ist_communal=communal)
            raeume.append(r)
            quelle[r.id] = "F"
            zuord[k] = Zuordnung(st, len(raeume) - 1, r, fr.abweichung_prozent, fr.flag)
    belegte = [r.polygon_mm for r in raeume if len(r.polygon_mm) >= 3]
    try:
        rest_r = komponenten_ohne_stempel(plan, wk, oeff, belegte)
    except Exception as exc:  # noqa: BLE001 — Rest-Stufe darf den Lauf nie killen
        print(f"   rest_komponenten fehlgeschlagen: {exc}")
        rest_r = []
    for r in rest_r:
        quelle[r.id] = "R"
    n = Counter(quelle.values())
    kette = (f"kaskade L:{n.get('L', 0)} H:{n.get('H', 0)} "
             f"F:{n.get('F', 0)} R:{n.get('R', 0)}")
    return KaskadeErgebnis(zuordnungen=zuord, raeume=raeume, rest_raeume=rest_r,
                           quelle=quelle, kette=kette, wandkoerper=wk,
                           tueroeffnungen=oeff)
