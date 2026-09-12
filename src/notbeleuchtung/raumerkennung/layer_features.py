"""layer_features — Merkmalsvektor je Layer: deterministisch, OHNE Layernamen.

Hintergrund (Slice 3b, Leonis Schritte 1/3/4 — Quelle ``docs/COORDINATION.md``
Log-Eintrag 2026-09-10 auf ``origin/leonis/demo-l-gebaeude``): heute vergibt die
Erkennung JEDE Layer-Rolle namensbasiert — über die Wand-, Raum-, Tür- und
Treppen-Namensmuster in ``dxf_load``, ``raumlayer``, ``tueren`` und
``geometrie_typ``.
Ein fremder Dialekt mit anderen Namen fällt damit still aus. Dieses Modul leitet
die Rolle aus der GEOMETRIE ab — das ist der ganze Grund für sein Dasein.

Zweistufig gegen Zirkularität (Leonis Einwand a): Runde 1 nutzt ausschließlich
Self-Features (Nr. 1–30). Aus Runde 1 wird die Wand-Menge gebildet
(``rolle == "wand"`` und ``confidence >= 0.60``); Runde 2 (Nr. 31–37) rechnet
Nachbarschaft NUR gegen diese Menge und ändert Nr. 1–30 nicht. Es gibt bewusst
keine dritte Runde — der Vektor bleibt deterministisch.

**Kein Selbstbezug in Runde 2** (lf-2): die Referenzmenge eines Layers ``L`` ist
die Wand-Menge OHNE ``L``. Vorher waren die Wandlayer selbst in ihrer eigenen
Referenz — gemessen maßen Linien-Wandlayer ``wand_naehe_quote`` =
``wand_parallel_quote`` = ``wand_endpunkt_quote`` = 1,000 und
``wand_abstand_p50_rel`` = 0,0000 gegen sich selbst, und bei den Gewichten 0,25
+ 0,20 des ``oeffnung``-Scores waren das +0,45 geschenkt. Wird die Referenz durch
den Ausschluss leer (``L`` ist der EINZIGE Wandlayer), sind Nr. 31–37
**unbelegt**: ``runde2_belegt`` bleibt ``False`` und alle sieben Felder tragen
den neutralen Wert **0.0** — weder Bonus noch Malus. Ein 0.0 in Nr. 31–37 ist
deshalb nur zusammen mit ``runde2_belegt`` lesbar: gemessene Null oder
gar nicht gemessen.

Harte Auflagen, die dieses Modul einhält:

- **Kein Feature liest einen Namen.** Kein Layername, kein Blockname, kein
  Namensmuster — auch nicht indirekt. ``layer_name`` ist ausschließlich
  Metadatum und Label-Schlüssel. Deshalb wird aus ``material_matching`` nur
  ``signatur_aus_hatch`` + ``struktur_klasse`` benutzt (reine
  Musterlinien-Geometrie) und NICHT ``bestimme_material``: dessen Score mischt
  Aliasnamen (15 %) und Layer-Hinweise (10 %) mit
  (``material_matching.py:282-284``).
- **Der mm-Faktor wird NIE neu abgeleitet.** ``plan.factor`` kommt wie geliefert
  aus ``dxf_load._calibrate_factor`` (leitet ihn geometrisch aus der Wandspanne
  bzw. dem Tür-ARC-Tiebreak ab; der Header-Einheitencode ist dort nur letzter
  Fallback). Der Header-Einheitencode wird in diesem Modul nirgends gelesen.
- **Block-Abstieg ist Pflicht** (Tiefe ≤3): ``plan.wall_layers`` sieht nur den
  gewählten Raum, block-interne Layer fehlen dort komplett (gemessen Rennweg_EG:
  27 Modelspace-Layer / 1073 Entities → 61 / 10728 mit Abstieg).

Layout (Teil von ``FEATURE_LAYOUT_VERSION`` — jede Änderung verschiebt lautlos
jeden Vektor und muss die Version hochziehen):

- Punkte je Entity: LINE/LW/POLYLINE → Segment-Endpunkte (Innenknoten doppelt),
  INSERT/TEXT/MTEXT/POINT → Einfügepunkt, HATCH → Randpunkte des größten
  Boundary-Pfads (``wandkoerper._hatch_punkte``), sonst keine. DIMENSION trägt
  damit 0 Punkte (gemessen: Muthgasse ``A-ANNO-DIMS`` 1871 Entities, 0 Punkte)
  → jedes Verhältnis braucht einen Nenner-Guard.
- Segmente: nur LINE/LW/POLYLINE, Länge > 1 mm; eine geschlossene Polylinie
  schließt das letzte Segment.
- Quantile: ``dxf_load._perzentil`` (``sorted``, Index ``round(q*(len-1))``).
- Absolutmaße über das 2-/98-%-Fenster (``dxf_load._SPAN_PERZENTIL``), nicht
  min/max: sonst liefern Block-Inhalte weit neben dem Grundriss Diagonalen um
  5,4 Mio. mm (gemessen an vier Mollgasse-Layern).
- Entropien: Farbe/Linientyp normiert über die BEOBACHTETEN Kategorien
  (1 Kategorie ⇒ 0.0), Winkel über die feste Bin-Zahl ``log2(12)``.
- ``parallel_quote``-Nenner sind ALLE Segmente des Layers (nicht nur die
  ≥200 mm langen) — so sind die Werte gegen die Messläufe vergleichbar.

Was ``confidence`` NICHT ist: keine Wahrscheinlichkeit. Der Wert ist die
gewichtete Erfüllung handgesetzter geometrischer Prädikate, von einer Person an
sechs Plänen kalibriert (der Fischamend-Elektroplan kam erst danach dazu und
ist NICHT mitkalibriert). ``0.85`` heißt nicht „15 % Fehlerrate" und nicht „85 %
der Fälle richtig" — es ist eine Bedienschwelle, keine Kalibrierung. Der Wert
sagt nichts über Fehlerrate, Verwechslungsrichtung oder Übertragbarkeit auf
einen siebten Dialekt. Eine kalibrierte Wahrscheinlichkeit gibt es erst mit
Korpus + trainiertem Modell und leave-one-plan-out-Auswertung (Leonis Schritt 5,
hier NICHT gebaut).

Grenze: die API liefert ``rolle`` + ``confidence`` + ``modus``, verdrahtet aber
nichts. Kein Aufrufer in ``provider``/``kaskade``/``bereinigung``, kein
Contract-Feld (``raum_modell.CONTRACT_VERSION`` bleibt 1.5.0) — Leonis
``rolle+confidence``-Forderung ist Vorschlag 1.6.0 und schließt hier nur an.

Bewusst genutzte private Importe (gleiche Semantik wie die Aufrufer im Paket):
``dxf_load._perzentil``/``_SPAN_PERZENTIL``/``_SPAN_MIN_MM``/``_SPAN_MAX_MM``,
``stiegenhaus._wcs_pts``, ``wandkoerper._heile``/``_hatch_punkte``/
``_kurzseite``/``_BREITE_MIN_MM``/``_BREITE_MAX_MM``/``_MIN_FLAECHE_MM2``/
``_PARALLEL_TOL_RAD``/``_MIN_UEBERLAPPUNG_MM``,
``raumlayer._MIN_FLAECHE_M2``/``_HATCH_MAX_M2`` (nur die beiden Flächenzahlen,
kein Layer-Muster).
"""
from __future__ import annotations

import json
import math
import os
import re
import tempfile
from collections import Counter
from dataclasses import dataclass, field, replace
from datetime import UTC, datetime
from itertools import pairwise
from pathlib import Path
from typing import Literal

import numpy as np
from shapely.geometry import LineString, Point
from shapely.ops import unary_union
from shapely.strtree import STRtree

from .dxf_load import _SPAN_MAX_MM, _SPAN_MIN_MM, _SPAN_PERZENTIL, DxfPlan, _perzentil
from .material_matching import signatur_aus_hatch, struktur_klasse
from .raumlayer import _HATCH_MAX_M2, _MIN_FLAECHE_M2
from .stiegenhaus import _wcs_pts
from .wandkoerper import (
    _BREITE_MAX_MM,
    _BREITE_MIN_MM,
    _MIN_FLAECHE_MM2,
    _MIN_UEBERLAPPUNG_MM,
    _PARALLEL_TOL_RAD,
    _hatch_punkte,
    _heile,
    _kurzseite,
)

XY = tuple[float, float]

#: Bei JEDER Feld-/Formel-/Toleranz-Änderung hochziehen (steht in jeder Korpuszeile).
#: ``lf-2``: Runde-2-Referenz ohne den eigenen Layer (vorher Selbstbezug) und
#: reihenfolgefreie ``_stichprobe``. Beides verschiebt Vektoren — lf-1-Zeilen
#: sind mit lf-2-Zeilen NICHT vergleichbar und dürfen nicht gemischt werden.
FEATURE_LAYOUT_VERSION = "lf-2"
#: 30 Runde 1 + 7 Runde 2.
VECTOR_LEN = 37

Rolle = Literal["wand", "oeffnung", "raumkontur", "rest"]
Modus = Literal["UEBERNEHMEN", "BESTAETIGEN", "HARD_STOP"]

#: Reihenfolge ist Teil des Layouts (Tie-Break des argmax).
_KLASSEN: tuple[Rolle, ...] = ("wand", "oeffnung", "raumkontur", "rest")

# ── Layout-Konstanten (R7: Toleranzen SIND Layout) ───────────────────────────
_MIN_SEG_MM = 1.0               # kürzere „Segmente" sind Zeichenrauschen
_ORTHO_TOL_GRAD = 2.0
_WINKEL_BIN_GRAD = 15.0
_WINKEL_BINS = 12
_SPREIZUNG_MAX = 99.0
_MAX_SEGMENTE = 1500            # Deckel je Layer (s. _parallel_quote)
_MAX_WAND_SEGMENTE = 20_000     # Deckel der Runde-2-Referenz
_MAX_KONTUREN = 50
_KONTUR_SCHRITT_MM = 250.0
_KONTUR_PROBEN_MAX = 400
_NAEHE_MM = 300.0               # Runde 2: „klebt an der Wand"
_WAND_WINKEL_TOL_GRAD = 5.0
_ENDPUNKT_MM = 150.0
_ABSCHLUSS_MM = 600.0           # wie wandkoerper.aussenkontur(d_mm=600)
#: GESETZT, NICHT GEMESSEN: ab 10 % der Plandiagonale gilt ein Layer als
#: wandfern. Diese Rampe ist von Hand gewählt — es gibt keine Messung, die
#: 10 % gegen 5 % oder 20 % belegt, und sie ist an keinem Plan kalibriert.
_WAND_FERN_REL = 0.10
_TUERBLATT_MIN_MM, _TUERBLATT_MAX_MM = 600.0, 1300.0

# ── Betriebsschwellen (Leonis, wörtlich) ─────────────────────────────────────
_UEBERNEHMEN_AB = 0.85
_BESTAETIGEN_AB = 0.60
_WAND_MIN_CONF = 0.60           # Aufnahmeschwelle in die Runde-2-Wandmenge
_DECKEL_KEIN_BELEG = 0.59       # → HARD_STOP
_DECKEL_UNSICHER = 0.84         # → nie automatisch übernehmen
#: ``rest`` ist eine RESTKLASSE: ihr Score ist ``1 - max(andere)``, entsteht also
#: aus der ABWESENHEIT von Belegen und nicht aus einem Beleg — ein geometrieloser
#: Layer wird damit maximal sicher. Gemessen (lf-1, sechs Pläne): 70 ×
#: UEBERNEHMEN, davon 57 mit ``rolle == "rest"``, davon 8 im Widerspruch zum
#: heutigen Namens-Label (über alle 70 UEBERNEHMEN sind es 16 Widersprüche);
#: drei mit ``n_punkte == 0`` erreichten confidence 1,000
#: (Muthgasse ``A-ANNO-DIMS`` 1871 Entities/0 Punkte, Rennweg_EG ``New_110
#: Bemassungen`` 190/0, Rennweg_OG3 ``New_GRUNDSTÜCKSGRENZE`` 103/0). Eine
#: Restklasse darf deshalb NIE automatisch übernommen werden → höchstens
#: BESTAETIGEN.
_DECKEL_RESTKLASSE = _DECKEL_UNSICHER
#: Ohne Geometrie (kein Punkt bzw. robuste Diagonale 0) gibt es überhaupt keine
#: Entscheidungsgrundlage — auch nicht für ``rest`` → HARD_STOP.
_DECKEL_OHNE_GEOMETRIE = _DECKEL_KEIN_BELEG
_MIN_ENTITIES = 5
_VARIANTE_DEZIMALEN = 4

#: Reihenfolge == Feldreihenfolge == to_vector(); NIE ändern ohne Versions-Bump.
FEATURE_NAMES: tuple[str, ...] = (
    # Runde 1 — Self-Features (Nr. 1–30)
    "anteil_line",
    "anteil_polyline",
    "anteil_hatch",
    "anteil_insert",
    "anteil_text",
    "anteil_bogen",
    "anteil_dimension",
    "anteil_geschlossen",
    "laenge_p10_rel",
    "laenge_p50_rel",
    "laenge_p90_rel",
    "laenge_spreizung",
    "ortho_quote",
    "winkel_entropie",
    "parallel_quote",
    "hatch_flaechen_anteil",
    "hatch_schmal_quote",
    "hatch_solid_quote",
    "hatch_einfach_quote",
    "hatch_kreuz_quote",
    "hatch_paar_sd_quote",
    "hatch_welle_quote",
    "hatch_bg_quote",
    "farb_entropie",
    "ltype_entropie",
    "punktdichte_pro_m2",
    "layer_diag_rel",
    "bbox_aspekt",
    "laenge_p50_mm",
    "layer_diag_mm",
    # Runde 2 — Nachbarschaft relativ zu den Runde-1-Wänden (Nr. 31–37)
    "runde2",
    "wand_naehe_quote",
    "wand_parallel_quote",
    "wand_endpunkt_quote",
    "wand_umschlossen_quote",
    "wand_kontur_deckung",
    "wand_abstand_p50_rel",
)

#: Features, die am mm-Faktor hängen (Schwellen in mm bzw. Absolutmaße).
#: ``wand_abstand_p50_rel`` steht bewusst NICHT hier: es ist auf die
#: Plandiagonale normiert, also faktor-invariant.
_FAKTOR_FEATURES: tuple[str, ...] = (
    "parallel_quote", "hatch_schmal_quote", "punktdichte_pro_m2",
    "laenge_p50_mm", "layer_diag_mm", "wand_naehe_quote",
    "wand_parallel_quote", "wand_endpunkt_quote", "wand_umschlossen_quote",
)


@dataclass(frozen=True, slots=True)
class LayerMerkmale:
    """Merkmale EINES Layers. Nur die Felder in ``FEATURE_NAMES`` sind Vektor."""

    # ── Metadaten: NICHT Teil von to_vector() ────────────────────────────────
    plan_id: str
    layer_name: str            #: NUR Metadatum/Label-Schlüssel, nie Feature
    quelle: str                #: "msp" | "block" | "gemischt"
    n_entities: int
    n_punkte: int
    plan_factor: float         #: aus plan.factor, unverändert übernommen
    faktor_abhaengig: bool     #: mind. ein mm-Feature ist belegt
    #: Plan-weit: mind. EIN Layer hat im kalibrierten mm-Maß eine robuste
    #: Diagonale im Geschoss-Fenster (15–500 m), der Faktor ist also
    #: geometrisch bestätigt. Basis war vorher der PUNKTREICHSTE Layer — das ist
    #: nicht der größte: auf EG_Grundriss_DE_NEU gewann damit ein 6,9-m-Füllayer
    #: (02-FIL-G00-L04-LILA, 2488 Punkte) gegen den 21,9-m-Grundriss, und alle
    #: 51 Layer standen fälschlich auf False.
    faktor_plausibel: bool
    massstab_verdacht: bool    #: Layer nur im Modelspace eines Wrapper-Plans
    variante_verdacht: bool    #: gleicher Vektor wie ein anderer Layer des Plans
    runde2_belegt: bool
    flaeche_median_m2: float   #: Median der geschlossenen Polygone/Hatches
    # ── Vektor, FESTE Reihenfolge = FEATURE_NAMES ────────────────────────────
    anteil_line: float = 0.0
    anteil_polyline: float = 0.0
    anteil_hatch: float = 0.0
    anteil_insert: float = 0.0
    anteil_text: float = 0.0
    anteil_bogen: float = 0.0
    anteil_dimension: float = 0.0
    anteil_geschlossen: float = 0.0
    laenge_p10_rel: float = 0.0
    laenge_p50_rel: float = 0.0
    laenge_p90_rel: float = 0.0
    laenge_spreizung: float = 0.0
    ortho_quote: float = 0.0
    winkel_entropie: float = 0.0
    parallel_quote: float = 0.0
    hatch_flaechen_anteil: float = 0.0
    hatch_schmal_quote: float = 0.0
    hatch_solid_quote: float = 0.0
    hatch_einfach_quote: float = 0.0
    hatch_kreuz_quote: float = 0.0
    hatch_paar_sd_quote: float = 0.0
    hatch_welle_quote: float = 0.0
    hatch_bg_quote: float = 0.0
    farb_entropie: float = 0.0
    ltype_entropie: float = 0.0
    punktdichte_pro_m2: float = 0.0
    layer_diag_rel: float = 0.0
    bbox_aspekt: float = 0.0
    laenge_p50_mm: float = 0.0
    layer_diag_mm: float = 0.0
    runde2: float = 0.0
    wand_naehe_quote: float = 0.0
    wand_parallel_quote: float = 0.0
    wand_endpunkt_quote: float = 0.0
    wand_umschlossen_quote: float = 0.0
    wand_kontur_deckung: float = 0.0
    wand_abstand_p50_rel: float = 0.0

    def to_vector(self) -> tuple[float, ...]:
        """Reihenfolge = ``FEATURE_NAMES``, Länge == ``VECTOR_LEN``.

        Layout-Version ``FEATURE_LAYOUT_VERSION``. Reihenfolge NIE ändern ohne
        Versions-Bump — sonst verschiebt sich jede Korpuszeile lautlos.
        """
        return tuple(float(getattr(self, n)) for n in FEATURE_NAMES)


@dataclass(frozen=True, slots=True)
class RollenBefund:
    """Regel-Entscheid für einen Layer (Leonis Schritt 3, regelbasiert)."""

    plan_id: str
    layer_name: str
    rolle: Rolle
    confidence: float           #: 0.0–1.0, KEINE Wahrscheinlichkeit (Modul-Docstring)
    modus: Modus
    scores: dict[str, float]    #: alle vier Klassen-Scores, Audit-Trail
    begruendung: str            #: erfüllte Prädikate im Klartext
    merkmale: LayerMerkmale


# ── Roh-Sammlung ─────────────────────────────────────────────────────────────
@dataclass
class _Roh:
    """Rohdaten eines Layers (mm), aus Raum UND Blöcken zusammengetragen."""

    typen: Counter = field(default_factory=Counter)
    farben: Counter = field(default_factory=Counter)
    ltypes: Counter = field(default_factory=Counter)
    pts: list[XY] = field(default_factory=list)
    segs: list[tuple[XY, XY]] = field(default_factory=list)
    konturen: list[list[XY]] = field(default_factory=list)
    flaechen_m2: list[float] = field(default_factory=list)
    #: (struktur_klasse, area_mm2, kurzseite_mm, hat_bgcolor)
    hatches: list[tuple[str, float, float, bool]] = field(default_factory=list)
    n_poly: int = 0
    n_geschlossen: int = 0
    n_msp: int = 0          # Entities auf oberster Ebene
    n_block: int = 0        # Entities aus aufgelösten INSERTs
    n_raum: int = 0         # aus plan.space
    n_msp_extra: int = 0    # nur aus dem Modelspace eines Wrapper-Plans
    #: Ziffern-TEXTE (Treppen-Laufnummern) für objekt_stiege — Textinhalt einer
    #: Entity, kein Layer-/Blockname; geht in KEIN Feature des Vektors ein.
    texte: list[tuple[int, XY]] = field(default_factory=list)


#: Laufnummern-Muster wie stiegenhaus._nimm_text.
_ZIFFER = re.compile(r"\d{1,2}")


def _ist_geschlossen(e) -> bool:
    """LWPOLYLINE trägt ``closed``, POLYLINE ``is_closed``."""
    return bool(getattr(e, "closed", False) or getattr(e, "is_closed", False))


def _geometrie(e, f: float, virtuell: bool) -> tuple[list[XY], list[tuple[XY, XY]]]:
    """(Punkte, Segmente) einer Entity in mm — Punkt-/Segmentdefinition s. Modul.

    Virtuelle Block-Entities laufen über ``stiegenhaus._wcs_pts`` (OCS-fest:
    gespiegelte Inserts tragen ``extrusion (0,0,-1)``, Mollgasse-Befund).
    """
    t = e.dxftype()
    if t in ("INSERT", "TEXT", "MTEXT", "POINT"):
        try:
            p = e.dxf.insert
        except Exception:  # noqa: BLE001 — POINT trägt location, kein insert
            return [], []
        return [(float(p[0]) * f, float(p[1]) * f)], []
    if t == "HATCH":
        try:
            return [(x * f, y * f) for x, y in _hatch_punkte(e)], []
        except Exception:  # noqa: BLE001 — kaputter Boundary-Pfad darf nicht killen
            return [], []
    if t not in ("LINE", "LWPOLYLINE", "POLYLINE"):
        return [], []
    if virtuell and t in ("LINE", "LWPOLYLINE"):
        pts = _wcs_pts(e, f)
    elif t == "LINE":
        pts = [(float(e.dxf.start[0]) * f, float(e.dxf.start[1]) * f),
               (float(e.dxf.end[0]) * f, float(e.dxf.end[1]) * f)]
    elif t == "LWPOLYLINE":
        pts = [(float(q[0]) * f, float(q[1]) * f) for q in e.get_points("xy")]
    else:
        pts = [(float(v.dxf.location[0]) * f, float(v.dxf.location[1]) * f)
               for v in e.vertices]
    segs = list(pairwise(pts))
    if len(pts) > 2 and _ist_geschlossen(e):
        segs.append((pts[-1], pts[0]))
    segs = [s for s in segs if math.dist(*s) > _MIN_SEG_MM]
    return [q for s in segs for q in s], segs


def _walk(entities, f: float, acc: dict[str, _Roh], *, raum: bool,
          tiefe: int = 0, ohne_block: str | None = None) -> None:
    """Entities je Layer einsammeln, Tiefe ≤3 in INSERTs absteigen.

    Abstieg wie ``wandkoerper._walk`` mit ``try/except`` je Block. ``ohne_block``
    hält den Wrapper-Block draußen, dessen Inhalt schon über ``plan.space`` kam.
    """
    for e in entities:
        try:
            lay = str(e.dxf.layer)
        except Exception:  # noqa: BLE001, S112 — Entity ohne Layer-Attribut
            continue
        d = acc.setdefault(lay, _Roh())
        t = e.dxftype()
        d.typen[t] += 1
        d.farben[int(getattr(e.dxf, "color", 256) or 256)] += 1
        d.ltypes[str(getattr(e.dxf, "linetype", "BYLAYER") or "BYLAYER")] += 1
        if tiefe == 0:
            d.n_msp += 1
        else:
            d.n_block += 1
        if raum:
            d.n_raum += 1
        else:
            d.n_msp_extra += 1
        pts, segs = _geometrie(e, f, tiefe > 0)
        d.pts += pts
        d.segs += segs
        if t in ("TEXT", "MTEXT") and pts:
            try:
                txt = (e.plain_text() if t == "MTEXT" else str(e.dxf.text)).strip()
            except Exception:  # noqa: BLE001 — kaputter Text darf nicht killen
                txt = ""
            if _ZIFFER.fullmatch(txt):
                d.texte.append((int(txt), pts[0]))
        if t in ("LWPOLYLINE", "POLYLINE"):
            d.n_poly += 1
            if _ist_geschlossen(e):
                d.n_geschlossen += 1
                poly = _heile(pts)
                if poly is not None:
                    d.flaechen_m2.append(poly.area / 1e6)
                    if len(d.konturen) < _MAX_KONTUREN:
                        d.konturen.append(
                            [(float(x), float(y)) for x, y in poly.exterior.coords])
        elif t == "HATCH":
            try:
                poly = _heile(pts)
                if poly is not None:
                    d.hatches.append((struktur_klasse(signatur_aus_hatch(e)),
                                      poly.area, _kurzseite(poly),
                                      e.bgcolor is not None))
                    d.flaechen_m2.append(poly.area / 1e6)
            except Exception:  # noqa: BLE001, S110 — kaputtes Muster killt den Scan nicht
                pass
        if t == "INSERT" and tiefe < 3 and str(e.dxf.name or "") != ohne_block:
            try:
                _walk(e.virtual_entities(), f, acc, raum=raum,
                      tiefe=tiefe + 1, ohne_block=ohne_block)
            except Exception:  # noqa: BLE001, S112 — kaputte Block-Referenz überspringen
                continue


def _sammle(plan: DxfPlan) -> tuple[dict[str, _Roh], str | None]:
    """Layer-Rohdaten aus ``plan.space`` UND — bei Wrapper-Plänen — dem Modelspace.

    Falle 2, gemessen am Fischamend-Elektroplan (``fertige
    Elektromontagepläne/BT1/…_ERDGESCHOSS BT1.dxf``): ``lade_dxf`` wählt dort
    den Blockraum (Wrapper-Block ``65465465``, INSERT xscale 1000). Beide
    Reichweiten stehen absichtlich hier, weil 55 gegen 64 sonst wie ein
    Widerspruch aussieht: über ``plan.space`` mit Block-Abstieg sind **55**
    Layer erreichbar, **9** weitere existieren NUR im Modelspace → **64**
    insgesamt. Die 9 stehen in einem ANDEREN Maßstab und tragen deshalb
    ``massstab_verdacht`` (gemessene Roh-Spanne: Blockinhalt 51,0 Einheiten
    gegen Modelspace 34.480,0 — Verhältnis 676).
    Der Wrapper-INSERT wird beim Modelspace-Lauf nicht aufgelöst, sonst zählt
    der Blockinhalt doppelt. Der Insert-Offset bleibt wie in ``dxf_load``
    unbeachtet (dort Docstring: „best-effort, ohne Transform").
    """
    msp = plan.doc.modelspace()
    acc: dict[str, _Roh] = {}
    wrapper = None
    if plan.space is not msp:
        wrapper = str(getattr(plan.space, "name", "") or "") or None
    _walk(plan.space, plan.factor, acc, raum=True)
    if wrapper is not None:
        _walk(msp, plan.factor, acc, raum=False, ohne_block=wrapper)
    return acc, wrapper


# ── Hilfsrechnungen ──────────────────────────────────────────────────────────
def _quantil(werte: list[float], q: float) -> float:
    return _perzentil(werte, q) if werte else 0.0


def _robuste_extents(pts: list[XY]) -> tuple[float, float]:
    """(dx, dy) im 2-/98-%-Fenster — min/max nimmt Phantom-Geometrie mit."""
    if not pts:
        return 0.0, 0.0
    lo, hi = _SPAN_PERZENTIL, 1.0 - _SPAN_PERZENTIL
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    return (_perzentil(xs, hi) - _perzentil(xs, lo),
            _perzentil(ys, hi) - _perzentil(ys, lo))


def _entropie(c: Counter) -> float:
    """Normierte Shannon-Entropie über die beobachteten Kategorien (1 ⇒ 0.0)."""
    n = sum(c.values())
    if n <= 0 or len(c) <= 1:
        return 0.0
    return -sum((v / n) * math.log2(v / n) for v in c.values()) / math.log2(len(c))


def _kanonisch(w):
    """Sortierschlüssel aus gerundeten Koordinaten — trägt keine Eingabereihenfolge."""
    return (tuple(_kanonisch(x) for x in w) if isinstance(w, tuple)
            else round(float(w), 3))


def _stichprobe(werte: list, k: int) -> list:
    """Reihenfolgefreier Deckel: kanonisch sortieren, dann gleichmäßig striden.

    ``random.Random(0).sample`` war NICHT reihenfolgefrei — der Seed macht nur
    die INDEX-Auswahl reproduzierbar, und die Indizes zeigen bei umsortierter
    Eingabe auf andere Segmente. Gemessen an 1800 unregelmäßigen Segmenten in
    getauschter Reihenfolge wichen 8 von 37 Features ab (laenge_spreizung
    7,5991 → 7,9954 · parallel_quote 0,6040 → 0,6013 · laenge_p50_mm
    2067,76 → 2079,77 · laenge_p10/p50/p90_rel · ortho_quote ·
    winkel_entropie). Sortieren + Striden hängt nur an den Koordinaten und hält
    die Stichprobe über den Wertebereich gestreut.
    """
    s = sorted(werte, key=_kanonisch)
    if len(s) <= k:
        return s
    schritt = len(s) / k
    return [s[int(i * schritt)] for i in range(k)]


def _parallel_quote(segs: list[tuple[XY, XY]]) -> float:
    """Anteil Segmente mit parallelem Partner in 50–600 mm Senkrechtabstand.

    Muster und Toleranzen 1:1 aus ``wandkoerper._doppellinien``
    (``_PARALLEL_TOL_RAD`` 2°, ``_MIN_UEBERLAPPUNG_MM`` 200 mm, Breite
    ``_BREITE_MIN_MM``–``_BREITE_MAX_MM``) — der namensfreie Doppellinien-Beleg
    einer Wand. Nenner sind ALLE Segmente des Layers.

    ponytail: O(n²)-Paarvergleich, gedeckelt auf 1500 Segmente je Layer;
    shapely.STRtree erst, wenn Pläne >5k Segmente je Layer tragen.
    """
    if not segs:
        return 0.0
    treffer = 0
    for a1, a2 in segs:
        ux, uy = a2[0] - a1[0], a2[1] - a1[1]
        la = math.hypot(ux, uy)
        if la < _MIN_UEBERLAPPUNG_MM:
            continue
        ux, uy = ux / la, uy / la
        wa = math.atan2(uy, ux) % math.pi
        for b1, b2 in segs:
            if (b1, b2) == (a1, a2) or math.dist(b1, b2) < _MIN_UEBERLAPPUNG_MM:
                continue
            wb = math.atan2(b2[1] - b1[1], b2[0] - b1[0]) % math.pi
            dw = abs(wa - wb)
            if min(dw, math.pi - dw) > _PARALLEL_TOL_RAD:
                continue
            dx, dy = b1[0] - a1[0], b1[1] - a1[1]
            if _BREITE_MIN_MM <= abs(-uy * dx + ux * dy) <= _BREITE_MAX_MM:
                treffer += 1
                break
    return treffer / len(segs)


def _winkel_grad(a: XY, b: XY) -> float:
    return math.degrees(math.atan2(b[1] - a[1], b[0] - a[0])) % 180.0


# ── Runde 1 ──────────────────────────────────────────────────────────────────
def _merkmale_runde1(plan_id: str, layer: str, d: _Roh, *, plan_factor: float,
                     plan_diag: float, massstab_verdacht: bool) -> LayerMerkmale:
    n = sum(d.typen.values())
    bw, bh = _robuste_extents(d.pts)
    diag = math.hypot(bw, bh)
    bbox_mm2 = bw * bh
    segs = _stichprobe(d.segs, _MAX_SEGMENTE)
    laengen = [math.dist(*s) for s in segs]
    p10, p50, p90 = (_quantil(laengen, q) for q in (0.10, 0.50, 0.90))
    winkel = [_winkel_grad(a, b) for a, b in segs]
    ortho = (sum(1 for w in winkel
                 if min(w % 90.0, 90.0 - w % 90.0) <= _ORTHO_TOL_GRAD) / len(winkel)
             ) if winkel else 0.0
    bins = Counter(min(_WINKEL_BINS - 1, int(w // _WINKEL_BIN_GRAD)) for w in winkel)
    w_ent = 0.0
    if len(bins) > 1:
        tot = sum(bins.values())
        w_ent = -sum((v / tot) * math.log2(v / tot)
                     for v in bins.values()) / math.log2(_WINKEL_BINS)
    nh = len(d.hatches)
    kl = Counter(k for k, *_ in d.hatches)
    flaechen = sorted(d.flaechen_m2)
    werte = {
        "anteil_line": d.typen["LINE"] / n if n else 0.0,
        "anteil_polyline": d.n_poly / n if n else 0.0,
        "anteil_hatch": d.typen["HATCH"] / n if n else 0.0,
        "anteil_insert": d.typen["INSERT"] / n if n else 0.0,
        "anteil_text": (d.typen["TEXT"] + d.typen["MTEXT"]) / n if n else 0.0,
        "anteil_bogen": ((d.typen["ARC"] + d.typen["CIRCLE"] + d.typen["ELLIPSE"]) / n
                         if n else 0.0),
        "anteil_dimension": d.typen["DIMENSION"] / n if n else 0.0,
        "anteil_geschlossen": d.n_geschlossen / d.n_poly if d.n_poly else 0.0,
        "laenge_p10_rel": p10 / diag if diag else 0.0,
        "laenge_p50_rel": p50 / diag if diag else 0.0,
        "laenge_p90_rel": p90 / diag if diag else 0.0,
        "laenge_spreizung": min(p90 / p10, _SPREIZUNG_MAX) if p10 else 0.0,
        "ortho_quote": ortho,
        "winkel_entropie": w_ent,
        "parallel_quote": _parallel_quote(segs),
        "hatch_flaechen_anteil": (sum(a for _, a, _, _ in d.hatches) / bbox_mm2
                                  if bbox_mm2 > 0 else 0.0),
        "hatch_schmal_quote": (sum(1 for _, a, ks, _ in d.hatches
                                   if _BREITE_MIN_MM <= ks <= _BREITE_MAX_MM
                                   and a >= _MIN_FLAECHE_MM2) / nh) if nh else 0.0,
        "hatch_solid_quote": kl["solid"] / nh if nh else 0.0,
        "hatch_einfach_quote": kl["einfach"] / nh if nh else 0.0,
        "hatch_kreuz_quote": kl["kreuz"] / nh if nh else 0.0,
        "hatch_paar_sd_quote": kl["paar_sd"] / nh if nh else 0.0,
        "hatch_welle_quote": kl["welle"] / nh if nh else 0.0,
        "hatch_bg_quote": (sum(1 for *_, bg in d.hatches if bg) / nh) if nh else 0.0,
        "farb_entropie": _entropie(d.farben),
        "ltype_entropie": _entropie(d.ltypes),
        "punktdichte_pro_m2": (len(d.pts) / (bbox_mm2 / 1e6)) if bbox_mm2 > 0 else 0.0,
        "layer_diag_rel": diag / plan_diag if plan_diag else 0.0,
        "bbox_aspekt": (min(bw, bh) / max(bw, bh)) if max(bw, bh) > 0 else 0.0,
        "laenge_p50_mm": p50,
        "layer_diag_mm": diag,
    }
    quelle = ("gemischt" if d.n_msp and d.n_block
              else "block" if d.n_block else "msp")
    return LayerMerkmale(
        plan_id=plan_id, layer_name=layer, quelle=quelle, n_entities=n,
        n_punkte=len(d.pts), plan_factor=plan_factor,
        faktor_abhaengig=any(werte.get(k, 0.0) > 0 for k in _FAKTOR_FEATURES),
        faktor_plausibel=False,   # plan-weit, s. _merkmale_liste
        massstab_verdacht=massstab_verdacht,
        variante_verdacht=False, runde2_belegt=False,
        flaeche_median_m2=_quantil(flaechen, 0.5), **werte)


def _variante_markieren(merkmale: list[LayerMerkmale]) -> list[LayerMerkmale]:
    """R4: trägt ein anderer Layer desselben Plans denselben Vektor (4 Dezimalen),
    ist es eine Planvariante (Barawitzka ``Icon_1``/``Icon_3`` tragen dieselbe
    Etage doppelt) — drei fast identische Zeilen je echtem Layer machen jede
    LOPO-Auswertung optimistisch."""
    zaehler = Counter(tuple(round(v, _VARIANTE_DEZIMALEN) for v in m.to_vector())
                      for m in merkmale)
    return [replace(m, variante_verdacht=zaehler[
        tuple(round(v, _VARIANTE_DEZIMALEN) for v in m.to_vector())] > 1)
        for m in merkmale]


def _plan_diagonale(roh: dict[str, _Roh]) -> float:
    alle = [p for d in roh.values() for p in d.pts]
    bw, bh = _robuste_extents(alle)
    return math.hypot(bw, bh)


def _merkmale_liste(plan: DxfPlan, plan_id: str, roh: dict[str, _Roh],
                    wrapper: str | None) -> tuple[list[LayerMerkmale], float]:
    plan_diag = _plan_diagonale(roh)
    merkmale = [
        _merkmale_runde1(
            plan_id, lay, d, plan_factor=plan.factor, plan_diag=plan_diag,
            massstab_verdacht=bool(wrapper is not None and d.n_raum == 0))
        for lay, d in sorted(roh.items())
    ]
    # faktor_plausibel: liegt IRGENDEIN Layer im Geschoss-Fenster, ist der
    # kalibrierte mm-Faktor geometrisch bestätigt. ``layer_diag_mm`` ist genau
    # diese robuste Diagonale — nichts wird doppelt gerechnet. Weder die
    # Plan-Diagonale noch die größte Layer-Diagonale taugen als Basis: beide
    # tragen Phantom-Geometrie mit (gemessen Rennweg_EG 1.214.571 mm bzw.
    # 1.409.156 mm gegen einen 33-m-Grundriss).
    plausibel = any(_SPAN_MIN_MM <= m.layer_diag_mm <= _SPAN_MAX_MM
                    for m in merkmale)
    return _variante_markieren(
        [replace(m, faktor_plausibel=plausibel) for m in merkmale]), plan_diag


def merkmale_aus_plan(plan: DxfPlan, plan_id: str) -> list[LayerMerkmale]:
    """Runde 1: Self-Features je Layer, ohne jede Nachbarschaft und ohne Namen."""
    roh, wrapper = _sammle(plan)
    return _merkmale_liste(plan, plan_id, roh, wrapper)[0]


# ── Runde 2 ──────────────────────────────────────────────────────────────────
@dataclass
class _WandRef:
    """Referenzgeometrie der in Runde 1 vorhergesagten Wände."""

    segs: list[tuple[XY, XY]]
    tree: STRtree
    enden: STRtree
    abschluss: object


def _naechste(tree: STRtree, geoms: list) -> tuple[list[int], list[float]]:
    """Je Geometrie (Index des nächsten Baum-Elements, Abstand) — vektorisiert.

    ``STRtree.query_nearest`` liefert bei Array-Eingabe ein 2D-Paar-Array
    ``(Eingabe-Index, Baum-Index)``; Einträge ohne Treffer fehlen darin. Die
    Rückgabe ist deshalb auf Eingabelänge aufgefüllt (``inf`` = kein Nachbar),
    damit der Aufrufer strikt gegen seine Segmentliste zippen kann.
    """
    if not geoms:
        return [], []
    rohidx, rohdist = tree.query_nearest(np.asarray(geoms, dtype=object),
                                         return_distance=True, all_matches=False)
    a = np.asarray(rohidx)
    eingang, baum = (a[0], a[1]) if a.ndim == 2 else (np.arange(len(geoms)), a)
    treffer = [0] * len(geoms)
    abstand = [math.inf] * len(geoms)
    for e, b, dd in zip(eingang, baum, np.asarray(rohdist).ravel(), strict=True):
        treffer[int(e)] = int(b)
        abstand[int(e)] = float(dd)
    return treffer, abstand


def _dilatiere(roh: dict[str, _Roh], wand_layer: set[str]) -> dict[str, object]:
    """``buffer(+_ABSCHLUSS_MM)`` je Wandlayer — EINMAL je Plan, dann gecacht.

    Die Dilatation verteilt sich über die Vereinigung
    (``union(A∪B).buffer(d) == union(A.buffer(d), B.buffer(d))``), die Erosion
    nicht. Deshalb wird hier je Layer dilatiert und in ``_wand_referenz`` nur
    noch aus Polygonen zusammengesetzt und einmal erodiert. Ohne diesen Cache
    kostet die Leave-one-out-Referenz (Nr. 31–37 ohne Selbstbezug) das
    Dilatieren einmal je Wandlayer — gemessen an Barawitzka_EG: 2047
    Wandsegmente, 53,0 s je Dilatation, 23 Wandlayer, also 24 × 53 s gegen
    1 × 53 s.

    ponytail: die 53 s stecken in ``shapely.buffer`` selbst; ein kleineres
    ``quad_segs`` wäre schneller, verschiebt aber jeden Vektor — erst mit dem
    nächsten Layout-Bump.
    """
    return {lay: unary_union(
        [LineString(s) for s in _stichprobe(roh[lay].segs, _MAX_WAND_SEGMENTE)]
    ).buffer(_ABSCHLUSS_MM) for lay in sorted(wand_layer)}


def _wand_referenz(roh: dict[str, _Roh], wand_layer: set[str],
                   dilatiert: dict[str, object]) -> _WandRef | None:
    segs = [s for lay in sorted(wand_layer) for s in roh[lay].segs]
    segs = _stichprobe(segs, _MAX_WAND_SEGMENTE)
    if not segs:
        return None
    lines = [LineString(s) for s in segs]
    # Morphologischer Abschluss wie wandkoerper.aussenkontur(d_mm=600) —
    # überbrückt Tür-/Fensteröffnungen, ohne wand_union nachzubauen. Dilatiert
    # ist je Layer vorberechnet (s. _dilatiere), erodiert wird hier einmal je
    # Referenzmenge.
    abschluss = unary_union([dilatiert[lay] for lay in sorted(wand_layer)]
                            ).buffer(-_ABSCHLUSS_MM)
    return _WandRef(segs=segs, tree=STRtree(lines),
                    enden=STRtree([Point(p) for s in segs for p in s]),
                    abschluss=abschluss)


def _kontur_deckung(konturen: list[list[XY]], tree: STRtree) -> float:
    """Anteil Randlänge geschlossener eigener Polygone mit ≤300 mm Wandabstand.

    ponytail: Rand im 250-mm-Raster abgetastet (max. 400 Punkte je Kontur) statt
    exaktem Verschnitt mit der gepufferten Wand-Union — exakt erst, wenn die
    Quote eine Entscheidung kippt.
    """
    werte: list[float] = []
    for k in konturen:
        if len(k) < 3:
            continue
        ring = LineString(k)
        if ring.length <= 0:
            continue
        n = min(_KONTUR_PROBEN_MAX, max(4, int(ring.length / _KONTUR_SCHRITT_MM)))
        proben = [ring.interpolate(i / (n - 1), normalized=True) for i in range(n)]
        _, dist = _naechste(tree, proben)
        if dist:
            werte.append(sum(1 for x in dist if x <= _NAEHE_MM) / len(dist))
    return sum(werte) / len(werte) if werte else 0.0


def _runde2(m: LayerMerkmale, d: _Roh, ref: _WandRef,
            plan_diag: float) -> LayerMerkmale:
    """Nachbarschaft gegen die Runde-1-Wände OHNE den eigenen Layer.

    Der Ausschluss steckt in ``ref`` (s. ``klassifiziere_plan``): mit Selbstbezug
    maßen Linien-Wandlayer 1,000/1,000/1,000 bei Abstand 0,0000 gegen sich
    selbst. Features 1–30 bleiben unberührt. Ist die Referenz leer, wird diese
    Funktion NICHT gerufen — dann bleiben die sieben Felder auf dem neutralen
    0.0 und ``runde2_belegt`` auf ``False``.
    """
    segs = _stichprobe(d.segs, _MAX_SEGMENTE)
    pts = _stichprobe(d.pts, _MAX_SEGMENTE)
    mitten = [Point((a[0] + b[0]) / 2, (a[1] + b[1]) / 2) for a, b in segs]
    idx, d_mitte = _naechste(ref.tree, mitten)
    naehe = (sum(1 for x in d_mitte if x <= _NAEHE_MM) / len(d_mitte)) if d_mitte else 0.0
    par = 0
    for (a, b), i, dist in zip(segs, idx, d_mitte, strict=True):
        if dist > _BREITE_MAX_MM:
            continue
        c, e = ref.segs[i]
        diff = abs(_winkel_grad(a, b) - _winkel_grad(c, e))
        if min(diff, 180.0 - diff) <= _WAND_WINKEL_TOL_GRAD:
            par += 1
    _, d_ende = _naechste(ref.enden, [Point(p) for s in segs for p in s])
    _, d_pts = _naechste(ref.tree, [Point(p) for p in pts])
    return replace(
        m, runde2_belegt=True, runde2=1.0,
        wand_naehe_quote=naehe,
        wand_parallel_quote=par / len(segs) if segs else 0.0,
        wand_endpunkt_quote=((sum(1 for x in d_ende if x <= _ENDPUNKT_MM) / len(d_ende))
                             if d_ende else 0.0),
        wand_umschlossen_quote=((sum(1 for p in pts if ref.abschluss.covers(Point(p)))
                                 / len(pts)) if pts else 0.0),
        wand_kontur_deckung=_kontur_deckung(d.konturen, ref.tree),
        wand_abstand_p50_rel=(_quantil([x for x in d_pts if math.isfinite(x)], 0.5)
                              / plan_diag if plan_diag and d_pts else 0.0))


# ── Regel-Entscheidung (Leonis Schritt 3) ────────────────────────────────────
def _rampe(x: float, lo: float, hi: float) -> float:
    """0 unter ``lo``, 1 über ``hi``, linear dazwischen — keine Kanten."""
    if hi <= lo:
        return 1.0 if x >= hi else 0.0
    return min(1.0, max(0.0, (x - lo) / (hi - lo)))


def _fenster(x: float, lo: float, hi: float) -> float:
    """1 im Intervall, linear auf 0 bei ±50 %."""
    if lo <= x <= hi:
        return 1.0
    if x < lo:
        return max(0.0, (x - lo * 0.5) / (lo * 0.5)) if lo > 0 else 0.0
    return max(0.0, (hi * 1.5 - x) / (hi * 0.5)) if hi > 0 else 0.0


def entscheide_rolle(m: LayerMerkmale) -> RollenBefund:
    """Regelbasierter Entscheid auf DENSELBEN Features (Leonis Schritt 3).

    Pro Klasse 3–5 weiche Prädikate mit Gewichtssumme 1. ``confidence`` ist
    KEINE Wahrscheinlichkeit (s. Modul-Docstring) — nur eine Bedienschwelle.

    Deckel (jeder senkt nur, keiner hebt): ``massstab_verdacht`` und zu wenige
    Entities → ``_DECKEL_KEIN_BELEG`` · keine Geometrie →
    ``_DECKEL_OHNE_GEOMETRIE`` · ``rolle == "rest"`` → ``_DECKEL_RESTKLASSE`` ·
    Runde 2 unbelegt und ``variante_verdacht`` → ``_DECKEL_UNSICHER``.
    """
    linien_beleg = (0.5 * _rampe(m.parallel_quote, 0.15, 0.60)
                    + 0.3 * _rampe(m.ortho_quote, 0.60, 0.95)
                    + 0.2 * _rampe(m.laenge_p90_rel, 0.05, 0.30))
    hatch_beleg = (0.6 * _rampe(m.hatch_schmal_quote, 0.20, 0.70)
                   + 0.4 * _rampe(m.anteil_hatch, 0.10, 0.50))
    daempfung = ((1 - 0.5 * _rampe(m.anteil_text, 0.10, 0.50))
                 * (1 - 0.5 * _rampe(m.anteil_dimension, 0.05, 0.30)))
    s_wand = max(linien_beleg, hatch_beleg) * daempfung
    if m.runde2_belegt:
        s_wand *= 0.8 + 0.2 * (1 - _rampe(m.wand_abstand_p50_rel, 0.0, _WAND_FERN_REL))
    s_oeffnung = (0.45 * _rampe(m.anteil_bogen, 0.05, 0.40)
                  + 0.25 * _rampe(m.wand_parallel_quote, 0.20, 0.70)
                  + 0.20 * _rampe(m.wand_endpunkt_quote, 0.10, 0.50)
                  + 0.10 * _fenster(m.laenge_p50_mm, _TUERBLATT_MIN_MM,
                                    _TUERBLATT_MAX_MM))
    s_raum = (0.45 * _rampe(m.anteil_geschlossen, 0.30, 0.90)
              + 0.20 * _rampe(m.wand_umschlossen_quote, 0.40, 0.90)
              + 0.20 * _rampe(m.wand_kontur_deckung, 0.30, 0.80)
              + 0.15 * _fenster(m.flaeche_median_m2, _MIN_FLAECHE_M2, _HATCH_MAX_M2))
    scores: dict[str, float] = {
        "wand": round(s_wand, 6), "oeffnung": round(s_oeffnung, 6),
        "raumkontur": round(s_raum, 6),
        # rest ist der Rest — damit ist argmax total und es gibt immer eine Klasse.
        "rest": round(1.0 - max(s_wand, s_oeffnung, s_raum), 6),
    }
    geordnet = sorted(scores.items(), key=lambda kv: (-kv[1], _KLASSEN.index(kv[0])))
    (rolle, best), (_, second) = geordnet[0], geordnet[1]
    conf = best * min(1.0, max(0.0, 0.5 + (best - second)))
    gruende = [f"{rolle}-Score {best:.3f} (2. {second:.3f})"]
    if m.massstab_verdacht:
        conf = min(conf, _DECKEL_KEIN_BELEG)
        gruende.append("massstab_verdacht: Layer nur im Modelspace eines "
                       "Wrapper-Plans → HARD STOP statt falscher Maßstab")
    if m.n_entities < _MIN_ENTITIES:
        conf = min(conf, _DECKEL_KEIN_BELEG)
        gruende.append(f"nur {m.n_entities} Entities → zu wenig Beleg")
    if m.n_punkte == 0 or m.layer_diag_mm == 0.0:
        conf = min(conf, _DECKEL_OHNE_GEOMETRIE)
        gruende.append("keine Geometrie (0 Punkte bzw. Diagonale 0) → ohne "
                       "Geometrie gibt es keine Grundlage, auch nicht für rest")
    if rolle == "rest":
        conf = min(conf, _DECKEL_RESTKLASSE)
        gruende.append("rest ist Restklasse (Sicherheit aus der Abwesenheit von "
                       "Belegen) → nie automatisch übernehmen")
    if not m.runde2_belegt:
        conf = min(conf, _DECKEL_UNSICHER)
        gruende.append("Runde 2 leer (keine Wand aus Runde 1) → nie automatisch")
    if m.variante_verdacht:
        conf = min(conf, _DECKEL_UNSICHER)
        gruende.append("variante_verdacht: gleicher Vektor wie ein anderer Layer")
    modus: Modus = ("UEBERNEHMEN" if conf >= _UEBERNEHMEN_AB
                    else "BESTAETIGEN" if conf >= _BESTAETIGEN_AB else "HARD_STOP")
    return RollenBefund(plan_id=m.plan_id, layer_name=m.layer_name,
                        rolle=rolle, confidence=round(conf, 6), modus=modus,
                        scores=scores, begruendung=" · ".join(gruende), merkmale=m)


def klassifiziere_plan(plan: DxfPlan, plan_id: str) -> list[RollenBefund]:
    """Runde 1 → Wände raten → Runde 2 → Regel. Ohne Wand bleibt Runde 2 leer.

    Die Referenzmenge eines Layers ist die Wandmenge OHNE ihn selbst. Gebaut
    wird deshalb eine Referenz je Wandlayer plus eine für alle übrigen. Die
    Wandmenge aus Runde 1 ist NICHT klein — gemessen Barawitzka_EG 23 von 129
    Layern, also 24 Referenzen —, deshalb ist das teure Dilatieren in
    ``_dilatiere`` je Layer gecacht und nur die Erosion läuft je Referenz.
    """
    roh, wrapper = _sammle(plan)
    merkmale, plan_diag = _merkmale_liste(plan, plan_id, roh, wrapper)
    befunde = [entscheide_rolle(m) for m in merkmale]
    wand = {b.layer_name for b in befunde
            if b.rolle == "wand" and b.confidence >= _WAND_MIN_CONF}
    if not wand:
        return befunde
    dilatiert = _dilatiere(roh, wand)
    refs: dict[str | None, _WandRef | None] = {}
    ergebnis: list[RollenBefund] = []
    for m in merkmale:
        eigen = m.layer_name if m.layer_name in wand else None
        if eigen not in refs:
            refs[eigen] = _wand_referenz(
                roh, wand - {eigen} if eigen else wand, dilatiert)
        ref = refs[eigen]
        ergebnis.append(entscheide_rolle(
            m if ref is None else _runde2(m, roh[m.layer_name], ref, plan_diag)))
    return ergebnis


# ── Korpus-Writer (Leonis Schritt 4, ab Tag 1) ───────────────────────────────
try:  # pragma: no cover — Umgebungsfrage, kein Zweig der Logik
    import pyarrow  # noqa: F401
    _HAT_PYARROW = True
except ImportError:
    _HAT_PYARROW = False

#: Label-Quellen: nur bestätigte Profile sind Trainingswahrheit.
LABEL_BESTAETIGT = "dialekt_profil_bestaetigt"
LABEL_NAMENSREGEL = "namensregel_heute"


#: Ein Basisname, zwei Suffixe — gelesen werden immer BEIDE (s. schreibe_korpus).
_KORPUS_BASIS = "layer_labels"
#: Übernommene Datei wird umbenannt, nicht gelöscht.
_ABGELEGT = ".abgelegt"


def _korpus_zeile(b: RollenBefund, label_quelle: str) -> dict:
    """Kanonische Zeile: Skalare + Vektor als Objekt ``features``.

    Parquet wird erst beim Schreiben spaltig (``_spaltig``), damit Lesen und
    Dedupe für beide Suffixe DASSELBE Schema sehen.
    """
    m = b.merkmale
    return {
        "plan_id": m.plan_id,
        "layer_name": m.layer_name,          # Metadatum, nie Feature
        "quelle": m.quelle,
        "layout_version": FEATURE_LAYOUT_VERSION,
        "vektor_laenge": VECTOR_LEN,
        "zeitstempel": datetime.now(UTC).isoformat(timespec="seconds"),
        "rolle": b.rolle,
        "confidence": b.confidence,
        "modus": b.modus,
        "label_quelle": label_quelle,
        "plan_factor": m.plan_factor,        # R1: macht einen Faktorwechsel erkennbar
        "n_entities": m.n_entities,
        "massstab_verdacht": m.massstab_verdacht,
        "variante_verdacht": m.variante_verdacht,
        "runde2_belegt": m.runde2_belegt,
        # Ohne bestätigten Faktor ist die Zeile später invalidierbar (Falle 1).
        "faktor_plausibel": m.faktor_plausibel,
        "features": dict(zip(FEATURE_NAMES, m.to_vector(), strict=True)),
    }


def _spaltig(r: dict) -> dict:
    """Kanonische Zeile → Parquet-Schema (``f_<name>``-Spalten, sklearn-fähig)."""
    return {**{k: v for k, v in r.items() if k != "features"},
            **{f"f_{k}": v for k, v in r["features"].items()}}


def _kanonische_zeile(r: dict) -> dict:
    """Parquet-Zeile → kanonische Form; eine JSONL-Zeile ist es schon."""
    if "features" in r:
        return r
    return {**{k: v for k, v in r.items() if not k.startswith("f_")},
            "features": {k[2:]: v for k, v in r.items() if k.startswith("f_")}}


def _lies_datei(p: Path) -> list[dict]:
    """Zeilen EINER Korpusdatei, Suffix-abhängig, immer kanonisch."""
    if not p.exists():
        return []
    if p.suffix == ".parquet":
        import pyarrow.parquet as pq
        return [_kanonische_zeile(r) for r in pq.read_table(p).to_pylist()]
    return [_kanonische_zeile(json.loads(z))
            for z in p.read_text(encoding="utf-8").splitlines() if z]


def _version_rang(v: object) -> int:
    """``"lf-2"`` → 2. Unbekanntes Format ist die niedrigste Version."""
    t = re.search(r"(\d+)$", str(v or ""))
    return int(t.group(1)) if t else -1


def _vereinige(*quellen: list[dict]) -> dict[tuple, dict]:
    """Zeilen mehrerer Quellen auf ``(plan_id, layer_name)`` dedupliziert.

    Gewinner ist die HÖHERE ``layout_version``; bei gleicher Version die spätere
    Quelle (Argumentreihenfolge = aufsteigende Priorität). Ein älteres Layout
    darf ein neueres nie überschreiben — lf-1- und lf-2-Vektoren sind nicht
    vergleichbar.
    """
    out: dict[tuple, dict] = {}
    for quelle in quellen:
        for r in quelle:
            k = (r.get("plan_id"), r.get("layer_name"))
            alt = out.get(k)
            if alt is None or (_version_rang(r.get("layout_version"))
                               >= _version_rang(alt.get("layout_version"))):
                out[k] = r
    return out


def _lege_ab(p: Path) -> Path:
    """Datei umbenennen statt löschen (``…jsonl.abgelegt``, bei Kollision ``…2``)."""
    ziel = p.with_suffix(p.suffix + _ABGELEGT)
    i = 2
    while ziel.exists():
        ziel = p.with_suffix(f"{p.suffix}{_ABGELEGT}{i}")
        i += 1
    os.replace(p, ziel)
    return ziel


def _schreibe_atomar(ziel: Path, zeilen: list[dict]) -> None:
    fd, tmp = tempfile.mkstemp(dir=str(ziel.parent), suffix=ziel.suffix)
    os.close(fd)
    p = Path(tmp)
    if ziel.suffix == ".parquet":
        import pyarrow as pa
        import pyarrow.parquet as pq
        pq.write_table(pa.Table.from_pylist([_spaltig(z) for z in zeilen]), p)
    else:
        p.write_text("".join(json.dumps(z, ensure_ascii=False) + "\n"
                             for z in zeilen), encoding="utf-8")
    os.replace(p, ziel)


def schreibe_korpus(befunde: list[RollenBefund], label_quelle: str,
                    ordner: Path = Path("corpus")) -> Path:
    """Korpuszeilen ``(plan_id, layer_name, feature_vektor, rolle)`` fortschreiben.

    Ziel ist ``corpus/layer_labels.parquet``, wenn ``pyarrow`` importierbar ist,
    sonst ``corpus/layer_labels.jsonl`` — gleicher Basisname, gleiches Schema,
    gleiche Feldnamen (JSONL trägt den Vektor als Objekt ``features``, Parquet
    spaltig als ``f_<name>``, damit es direkt sklearn-fähig bleibt).

    **Ein Korpus-Ziel, auch über den Suffix-Wechsel hinweg:** gelesen werden
    IMMER beide Suffixe und über ``(plan_id, layer_name)`` dedupliziert (höhere
    ``layout_version`` gewinnt). Wird Parquet geschrieben, während eine JSONL
    liegt, werden deren Zeilen übernommen und die JSONL nach
    ``layer_labels.jsonl.abgelegt`` UMBENANNT — nicht gelöscht. Ohne das
    verwaisen die JSONL-Zeilen beim ersten ``pip install -e .[layerml]`` still.
    Eine Parquet-Datei ohne installiertes ``pyarrow`` bleibt unangetastet
    liegen (nicht lesbar ⇒ nicht übernehmbar ⇒ auch nicht weggeräumt).

    ``label_quelle`` ist Pflicht (``LABEL_BESTAETIGT`` wenn ein Mensch ein
    Dialekt-Profil bestätigt hat, ``LABEL_NAMENSREGEL`` wenn eine Regex geraten
    hat): später wird trainiert, was bestätigt ist — nicht, was geraten wurde.

    ponytail: Datei wird komplett neu geschrieben (gemessen 501 Zeilen über
    sieben Pläne); ein Append-Pfad ist erst ab ~50k Zeilen nötig.
    """
    ordner = Path(ordner)
    ordner.mkdir(parents=True, exist_ok=True)
    parquet = ordner / f"{_KORPUS_BASIS}.parquet"
    jsonl = ordner / f"{_KORPUS_BASIS}.jsonl"
    ziel, andere = (parquet, jsonl) if _HAT_PYARROW else (jsonl, parquet)
    lesbar = _HAT_PYARROW or andere.suffix != ".parquet"
    fremd = _lies_datei(andere) if lesbar else []
    zeilen = _vereinige(fremd, _lies_datei(ziel),
                        [_korpus_zeile(b, label_quelle) for b in befunde])
    _schreibe_atomar(ziel, [zeilen[k] for k in
                            sorted(zeilen, key=lambda k: (str(k[0]), str(k[1])))])
    if fremd and andere.exists():
        _lege_ab(andere)
    return ziel
