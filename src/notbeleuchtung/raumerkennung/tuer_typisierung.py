"""tuer_typisierung — Tür-Rollen (``Tuer.tuer_detail``) aus den Raum-Seiten.

Regelkette (die ERSTE greifende Regel setzt das Detail):

1. AUSSEN × ALLGEMEIN_ERSCHLIESSUNG → ``hauseingang`` (nur EG); Notausgang-
   Zusatz (``ist_notausgang=True``), wenn eine Fluchtweglinie dort endet ODER
   Doppelflügel (> 1.4 m).
2. AUSSEN × WOHNUNG_PRIVAT → ``balkontuer`` (nie Ausgang).
3. STIEGENHAUS × WOHNUNG_PRIVAT → ``wohnungseingang`` · STIEGENHAUS ×
   ALLGEMEIN_ERSCHLIESSUNG → ``stiegenhaustuer``. (Der Contract hat EIN
   ``tuer_detail``: die Wohnungseingangs-Rolle gewinnt gegen die Stiegenhaus-
   Rolle, weil sie die Fluchtweg-STARTseite bestimmt; die Stiegenhaus-Seite
   rekonstruiert ``ausgaenge.leite_ausgaenge`` aus den Raum-Seiten.)
4. WOHNUNG_PRIVAT × WOHNUNG_PRIVAT → ``zimmertuer``.
5. ALLGEMEIN_ERSCHLIESSUNG (GANG/VORRAUM) × WOHNUNG_PRIVAT → ``wohnungseingang``.
6. GARAGE beidseits + Breite > 2.2 m → ``garagentor``.
7. BST/T30/T90/EI30/EI90-Text in 500 mm → ``brandschutztuer`` NUR wenn kein
   spezifischeres Detail greift (sonst bleibt das spezifischere Detail —
   Brandschutz-Priorität dokumentiert im Modul-Docstring; ein eigenes
   Zusatzfeld gibt der Contract nicht her).

Geschoss: ``geschoss_aus(floor, dxf_pfad)`` — floor-Parameter zuerst, sonst
EG/OG\\d/UG/KG/DG aus dem Dateinamen. Im OG entstehen keine hauseingang-
Endausgänge.
"""
from __future__ import annotations

import math
import re
from pathlib import Path

from notbeleuchtung.hauptengine.contracts.raum_modell import Raum, Tuer

from .nutzungsklasse import nutzungsklasse_fuer
from .tuer_zuordnung import AUSSEN

XY = tuple[float, float]

_GESCHOSS_RE = re.compile(r"(?<![A-Z0-9])(EG|UG\d*|KG\d*|DG|OG\s?\d+|\d+\.?\s?OG)",
                          re.IGNORECASE)
_BRANDSCHUTZ_RE = re.compile(r"\bBST\b|T\s?30|T\s?90|EI\s?30|EI\s?90", re.IGNORECASE)
_BST_NAH_MM = 500.0
_FLW_ENDE_NAH_MM = 1000.0
_DOPPELFLUEGEL_MM = 1400.0
_GARAGENTOR_MM = 2200.0


def geschoss_aus(floor: str | None, dxf_pfad: str | None = None) -> str:
    """Geschoss-Kürzel: floor-Parameter zuerst, sonst aus dem Dateinamen."""
    for quelle in (floor, Path(dxf_pfad).stem if dxf_pfad else None):
        if not quelle:
            continue
        m = _GESCHOSS_RE.search(quelle)
        if m:
            return m.group(1).upper().replace(" ", "").replace(".", "")
    return ""


def ist_erdgeschoss(geschoss: str) -> bool:
    return geschoss.upper().startswith("EG")


def ist_obergeschoss(geschoss: str) -> bool:
    g = geschoss.upper()
    return "OG" in g and not g.startswith("EG") or g == "DG"


def brandschutz_hinweise_aus_dxf(plan) -> list[XY]:
    """Positionen von BST/T30/T90/EI30/EI90-Texten im Plan (mm)."""
    out: list[XY] = []
    for e in plan.entities():
        t = e.dxftype()
        if t == "MTEXT":
            text, ins = e.text, e.dxf.insert
        elif t == "TEXT":
            text, ins = e.dxf.text, e.dxf.insert
        else:
            continue
        if _BRANDSCHUTZ_RE.search(text or ""):
            out.append(plan._scale(ins))
    return out


def _klasse(seite: str | None, raum_by_id: dict[str, Raum]) -> str | None:
    if seite in (AUSSEN, "KEIN_RAUM"):
        return seite
    r = raum_by_id.get(seite or "")
    if r is None:
        return None
    return r.nutzungsklasse or nutzungsklasse_fuer(r.raum_typ)


def _typ(seite: str | None, raum_by_id: dict[str, Raum]) -> str:
    r = raum_by_id.get(seite or "")
    return r.raum_typ if r is not None else ""


def typisiere_tueren(tueren: list[Tuer], raeume: list[Raum], geschoss: str,
                     brandschutz_hinweise: list[XY] = (),
                     fluchtweg_enden: list[XY] = ()) -> list[Tuer]:
    """Setzt ``tuer_detail``/``ist_notausgang`` in-place (Rückgabe = Eingabe)."""
    by_id = {r.id: r for r in raeume}
    eg = ist_erdgeschoss(geschoss)
    for t in tueren:
        ka, kb = _klasse(t.von_raum, by_id), _klasse(t.nach_raum, by_id)
        ta, tb = _typ(t.von_raum, by_id), _typ(t.nach_raum, by_id)
        klassen, typen = {ka, kb}, {ta, tb}
        detail = None
        if AUSSEN in klassen and "ALLGEMEIN_ERSCHLIESSUNG" in klassen:
            if eg:
                detail = "hauseingang"
            endet_flw = any(math.dist(t.xy_mm, p) < _FLW_ENDE_NAH_MM
                            for p in fluchtweg_enden)
            if endet_flw or t.breite_mm > _DOPPELFLUEGEL_MM:
                t.ist_notausgang = True
        elif AUSSEN in klassen and "WOHNUNG_PRIVAT" in klassen:
            detail = "balkontuer"
            t.ist_notausgang = False
        elif "STIEGENHAUS" in typen and "WOHNUNG_PRIVAT" in klassen:
            detail = "wohnungseingang"
        elif "STIEGENHAUS" in typen and "ALLGEMEIN_ERSCHLIESSUNG" == (
                kb if ta == "STIEGENHAUS" else ka):
            detail = "stiegenhaustuer"
        elif ka == kb == "WOHNUNG_PRIVAT":
            detail = "zimmertuer"
        elif "WOHNUNG_PRIVAT" in klassen and "ALLGEMEIN_ERSCHLIESSUNG" in klassen:
            detail = "wohnungseingang"
        elif ta == tb == "GARAGE" and t.breite_mm > _GARAGENTOR_MM:
            detail = "garagentor"
        if detail is None and any(math.dist(t.xy_mm, p) < _BST_NAH_MM
                                  for p in brandschutz_hinweise):
            detail = "brandschutztuer"
        if t.tuer_detail is None:
            t.tuer_detail = detail
    return tueren
