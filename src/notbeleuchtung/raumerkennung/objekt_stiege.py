"""objekt_stiege — Treppenläufe als Objekt-Matcher auf Entity-Gruppen, raumlos.

Owner-Vorgabe d / Leonis Einwand b: ``stiege`` gehört NICHT in den
Layer-Klassifikator (~1 Beispiel je Plan → leave-one-plan-out-Recall wäre
Rauschen), sondern ist ein Objekt-Matcher auf Entity-Gruppen — parallele
Stufenlinien, Teilung 0,25–0,35 m, Laufrichtung.

Aufsetzend auf der VORHANDENEN Treppenerkennung (``stiegenhaus.py`` bleibt
unverändert, wird nur importiert): ``_gruppiere_laeufe`` (≥3 parallele Linien,
Winkel-Toleranz 5°, Normalenprojektion, Doppelstrich-Schluckung),
``_lauf_aus_gruppe`` (Lauf-Polygon, Laufachse, Antritt/Austritt, Laufrichtung
aus Laufnummern oder Gehlinie — prüft selbst KEIN Raumpolygon),
``_STUFE_MIN_MM``/``_STUFE_MAX_MM`` (200–4000 mm), ``_LAUF_MAX_M2`` (60 m²).

NICHT wiederverwendet: ``stiegenhaus._stufen_und_texte``. Es braucht ein
Raumpolygon (``hull = poly.buffer(500)``, ``stiegenhaus.py:81``) und steigt nur
in INSERTs mit treppenartigem Blocknamen ab — also namensbasiert. Ersatz: Sammler
``layer_features._sammle`` (Modelspace + alle INSERTs, Tiefe ≤3, OCS-fest) und
statt des Raumpolygons die robusten Layer-Extents mit demselben 500-mm-Puffer.
Kein Blockname, kein Layername im Entscheid — der Layername ist nur Metadatum.

Die Owner-Teilung 250–350 mm ist eine eigene Konstante gegen die 150–350 mm in
``stiegenhaus`` (die dort unberührt bleiben), kein neuer Algorithmus.

Ketten-Nachbearbeitung, gemessen zwingend: ``_gruppiere_laeufe`` kettet alles
mit Abstand ≤350 mm in EINE Kette. Ungefiltert liefert das Unsinn (Barawitzka:
78 Layer mit „Läufen"; Muthgasse ``A-FLOR`` allein 102 Gruppen) und lässt die
echte Treppe durchfallen (Barawitzka ``0._EG PP_2_410 Treppe``: eine Gruppe mit
38 „Stufen", Gaps [140, 163, 147, 270, 270, …], Konsistenz 0,622, Fläche
103,2 m² → verworfen, obwohl die echte Teilung 270 mm ist). Deshalb nach
``_gruppiere_laeufe``: Doppelstrich-Kollaps → Kette bei jedem Gap außerhalb des
Teilungsfensters aufschneiden → Teilketten einzeln prüfen.

Grenze (gemessen, kein Vorsichtsritual): ein Fahrradständer ist von einem
Treppenlauf geometrisch nicht unterscheidbar — Mollgasse_EG
``07-MOB-G00-LEG-FAHRRAD`` liefert DREI Kandidaten mit 6/16/18 „Stufen", alle
mit Teilung 350,0 mm und Konsistenz 1,0 (Flächen 1,92/6,00/24,74 m²), alle mit
confidence 0,84. Solange kein Diskriminator existiert, ist die Confidence bei
0,84 gedeckelt: JEDER Kandidat geht zur menschlichen Bestätigung, keiner wird
automatisch übernommen.

Die Stufenzahlen hängen an der Stichprobe: ``layer_features._stichprobe`` zieht
seit ``lf-2`` reihenfolgefrei (kanonisch sortiert + gestridet) statt zufällig,
deshalb schneidet ``_gruppiere_laeufe`` hier anders — vorher waren es vier
Kandidaten mit 6/16/13/5 Stufen. Der Deckel ändert sich dadurch nicht.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from itertools import pairwise
from typing import Literal

from shapely.geometry import MultiPoint, Point, box

from .dxf_load import _SPAN_PERZENTIL, DxfPlan, _perzentil
from .layer_features import _Roh, _sammle, _stichprobe
from .stiegenhaus import (
    _LAUF_MAX_M2,
    _STUFE_MAX_MM,
    _STUFE_MIN_MM,
    _gruppiere_laeufe,
    _lauf_aus_gruppe,
)

XY = tuple[float, float]

# ── Eigene Konstanten; die von stiegenhaus bleiben unberührt ─────────────────
TEILUNG_MIN_MM, TEILUNG_MAX_MM = 250.0, 350.0   # Owner: 0,25–0,35 m
TEILUNG_STREUUNG = 0.20                 # Konsistenz-Fenster um den Median-Gap
TEILUNG_KONSISTENZ_MIN = 0.80
MIN_STUFEN = 5
STUFE_LAENGE_MIN_MM = 700.0             # Laufbreite; darunter ist es kein Lauf
STUFE_LAENGE_TOL = 0.25                 # ±25 % um die Median-Stufenlänge
STUFE_LAENGE_ANTEIL_MIN = 0.60          # Wangen/Podestkanten dürfen abweichen
DOPPELSTRICH_MM = TEILUNG_MIN_MM * 0.5  # 125 mm = dieselbe Stufe

_MAX_STUFEN = 1500          # ponytail: _gruppiere_laeufe ist O(n²) je Layer
_HULL_PUFFER_MM = 500.0     # wie stiegenhaus._stufen_und_texte
_NUM_PUFFER_MM = 400.0      # wie stiegenhaus._lauf_aus_gruppe
_CONF_BASIS = 0.60
_CONF_DECKEL = 0.84
_LAUFBREITE_TYPISCH = (900.0, 2000.0)


@dataclass(frozen=True, slots=True)
class StiegenKandidat:
    """Ein Treppenlauf-Kandidat (mm). ``layer_name`` ist NUR Metadatum."""

    polygon_mm: list[XY]
    antritt_mm: XY
    austritt_mm: XY
    laufrichtung: Literal["auf", "ab", "unbekannt"]
    teilung_mm: float           #: Median-Gap der Stufen
    n_stufen: int
    winkel_grad: float          #: Stufenrichtung mod 180
    flaeche_m2: float
    konsistenz: float           #: Anteil Gaps im Teilungsfenster
    layer_name: str
    quelle: str                 #: "msp" | "block" | "gemischt"
    confidence: float


def _median(werte: list[float]) -> float:
    """Unteres Mittel (``s[len//2]``) — dieselbe Definition wie die Messläufe."""
    s = sorted(werte)
    return s[len(s) // 2] if s else 0.0


def _robuste_box(pts: list[XY]):
    """Layer-Extents im 2-/98-%-Fenster — Ersatz für das Raumpolygon."""
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    lo, hi = _SPAN_PERZENTIL, 1.0 - _SPAN_PERZENTIL
    return box(_perzentil(xs, lo), _perzentil(ys, lo),
               _perzentil(xs, hi), _perzentil(ys, hi))


def _teilketten(gruppe: list[tuple[XY, XY]]
                ) -> tuple[float, list[list[tuple[float, list[tuple[XY, XY]]]]]]:
    """Gruppe → (Stufenwinkel, Teilketten) auf den Normalen-Offsets.

    1. Doppelstrich-Kollaps: Offsets < ``DOPPELSTRICH_MM`` sind dieselbe Stufe.
    2. Kette bei jedem Gap außerhalb ``[TEILUNG_MIN_MM, TEILUNG_MAX_MM]`` trennen.
    """
    a0, b0 = gruppe[0]
    ang = math.atan2(b0[1] - a0[1], b0[0] - a0[0]) % math.pi
    nx, ny = -math.sin(ang), math.cos(ang)
    mit_off = sorted(((s[0][0] + s[1][0]) / 2 * nx + (s[0][1] + s[1][1]) / 2 * ny, s)
                     for s in gruppe)
    stufen: list[tuple[float, list[tuple[XY, XY]]]] = []
    for off, s in mit_off:
        if stufen and off - stufen[-1][0] < DOPPELSTRICH_MM:
            stufen[-1][1].append(s)
        else:
            stufen.append((off, [s]))
    ketten: list[list[tuple[float, list[tuple[XY, XY]]]]] = (
        [[stufen[0]]] if stufen else [])
    for vorher, jetzt in pairwise(stufen):
        if TEILUNG_MIN_MM <= jetzt[0] - vorher[0] <= TEILUNG_MAX_MM:
            ketten[-1].append(jetzt)
        else:
            ketten.append([jetzt])
    return ang, ketten


def _pruefe_kette(kette: list[tuple[float, list[tuple[XY, XY]]]]
                  ) -> tuple[bool, dict, list[tuple[XY, XY]]]:
    """(bestanden, Diagnose, Kernstufen) einer Teilkette."""
    offs = [o for o, _ in kette]
    gaps = [b - a for a, b in pairwise(offs)]
    segs = [s for _, ss in kette for s in ss]
    laengen = [math.dist(*s) for s in segs]
    ml = _median(laengen)
    anteil = ((sum(1 for x in laengen if abs(x - ml) <= STUFE_LAENGE_TOL * ml)
               / len(laengen)) if laengen and ml > 0 else 0.0)
    kern = [s for s in segs if abs(math.dist(*s) - ml) <= STUFE_LAENGE_TOL * ml]
    xs = [q[0] for s in kern for q in s]
    ys = [q[1] for s in kern for q in s]
    flaeche = ((max(xs) - min(xs)) * (max(ys) - min(ys)) / 1e6) if xs else 0.0
    t = _median(gaps)
    konsist = ((sum(1 for g in gaps if abs(g - t) <= TEILUNG_STREUUNG * t) / len(gaps))
               if gaps and t > 0 else 0.0)
    diag = {"n_stufen": len(kette), "teilung_mm": round(t, 1),
            "konsistenz": round(konsist, 3), "laenge_med_mm": round(ml, 1),
            "laenge_anteil": round(anteil, 3), "flaeche_m2": round(flaeche, 2)}
    ok = (len(kette) >= MIN_STUFEN
          and TEILUNG_MIN_MM <= t <= TEILUNG_MAX_MM
          and konsist >= TEILUNG_KONSISTENZ_MIN
          and anteil >= STUFE_LAENGE_ANTEIL_MIN
          and ml >= STUFE_LAENGE_MIN_MM
          and 0 < flaeche <= _LAUF_MAX_M2)
    return ok, diag, kern


def _confidence(diag: dict, *, aus_nummern: bool, massstab_verdacht: bool) -> float:
    """Regelbasiert und gedeckelt — s. Modul-Docstring (Fahrradständer-Befund)."""
    c = _CONF_BASIS
    if diag["n_stufen"] >= 7:
        c += 0.15
    if diag["konsistenz"] == 1.0:
        c += 0.10
    if aus_nummern:
        c += 0.10
    if _LAUFBREITE_TYPISCH[0] <= diag["laenge_med_mm"] <= _LAUFBREITE_TYPISCH[1]:
        c += 0.05
    c = min(c, _CONF_DECKEL)
    if massstab_verdacht:
        c -= 0.20
    return round(max(0.0, c), 6)


def _quelle(d: _Roh) -> str:
    return "gemischt" if d.n_msp and d.n_block else "block" if d.n_block else "msp"


def finde_stiegen(plan: DxfPlan) -> list[StiegenKandidat]:
    """Treppenlauf-Kandidaten des Plans — layerweise, ohne Raum und ohne Namen.

    Laufnummern werden über ALLE Layer gesammelt (sie liegen oft auf Textlayern)
    und gegen die robusten Extents des jeweiligen Geometrie-Layers gefiltert.
    """
    roh, wrapper = _sammle(plan)
    nums = [(n, p) for d in roh.values() for n, p in d.texte]
    out: list[StiegenKandidat] = []
    for lay, d in sorted(roh.items()):
        stufen = [s for s in d.segs
                  if _STUFE_MIN_MM <= math.dist(*s) <= _STUFE_MAX_MM]
        if len(stufen) < MIN_STUFEN:
            continue
        hull = _robuste_box(d.pts).buffer(_HULL_PUFFER_MM)
        lay_nums = [(n, p) for n, p in nums if hull.covers(Point(p))]
        verdacht = bool(wrapper is not None and d.n_raum == 0)
        for gruppe in _gruppiere_laeufe(_stichprobe(stufen, _MAX_STUFEN)):
            ang, ketten = _teilketten(gruppe)
            for kette in ketten:
                ok, diag, kern = _pruefe_kette(kette)
                if not ok:
                    continue
                lauf = _lauf_aus_gruppe(kern, lay_nums, d.segs)
                kh = MultiPoint([p for s in kern for p in s]).convex_hull
                if kh.geom_type != "Polygon":
                    kh = kh.buffer(50.0)
                # Gleiches Prädikat wie _lauf_aus_gruppe: ab 2 Nummern im Lauf
                # kommt die Richtung aus den Laufnummern, nicht aus der Gehlinie.
                aus_nummern = sum(
                    1 for _, p in lay_nums
                    if kh.buffer(_NUM_PUFFER_MM).covers(Point(p))) >= 2
                out.append(StiegenKandidat(
                    polygon_mm=[(float(x), float(y)) for x, y in lauf.polygon_mm],
                    antritt_mm=lauf.antritt_mm, austritt_mm=lauf.austritt_mm,
                    laufrichtung=lauf.richtung,
                    teilung_mm=diag["teilung_mm"], n_stufen=diag["n_stufen"],
                    winkel_grad=round(math.degrees(ang) % 180.0, 1),
                    flaeche_m2=diag["flaeche_m2"], konsistenz=diag["konsistenz"],
                    layer_name=lay, quelle=_quelle(d),
                    confidence=_confidence(diag, aus_nummern=aus_nummern,
                                           massstab_verdacht=verdacht)))
    return out
