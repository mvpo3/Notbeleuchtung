"""tuer_typisierung — Tür-Rollen (``Tuer.tuer_detail``) aus den Raum-Seiten.

Regelkette (die ERSTE greifende Regel setzt das Detail):

1. AUSSEN × ALLGEMEIN_ERSCHLIESSUNG → ``hauseingang`` (nur EG, und nicht in
   eine Fläche ohne Weg ins Freie — Argument ``kein_weg_ins_freie``);
   Notausgang-Zusatz (``ist_notausgang=True``), wenn eine Fluchtweglinie dort
   endet ODER Doppelflügel (> 1.4 m).
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

from shapely.geometry import Point
from shapely.geometry.base import BaseGeometry

from notbeleuchtung.hauptengine.contracts.raum_modell import Raum, Tuer

from .nutzungsklasse import nutzungsklasse_fuer
from .tuer_zuordnung import AUSSEN

XY = tuple[float, float]

_GESCHOSS_RE = re.compile(r"(?<![A-Z0-9])(EG|UG\d*|KG\d*|DG|OG\s?\d+|\d+\.?\s?OG)",
                          re.IGNORECASE)
_BRANDSCHUTZ_RE = re.compile(r"\bBST\b|T\s?30|T\s?90|EI\s?30|EI\s?90", re.IGNORECASE)
_BST_NAH_MM = 500.0
# Fluchtweg-Ende „an der Tür": 2 m — die 09-WEG-Annotation endet oft kurz vor
# der Türsehne (Mollgasse Südgarten: Endpunkt 1.9 m vor dem Türbogen).
_FLW_ENDE_NAH_MM = 2000.0
_DOPPELFLUEGEL_MM = 1400.0
_GARAGENTOR_MM = 2200.0
_TEXT_NAH_MM = 1500.0
_WINDFANG_M2 = 8.0
# Tür „liegt an" der Fläche ohne Weg ins Freie (Türsehne vs. Hofrand).
_KEIN_WEG_NAH_MM = 600.0

# Text → Tür-Rolle (Fachteil „Türquellen" (b)): Eingangs-Wörter machen im EG
# einen hauseingang, Notausgangs-Wörter einen Notausgang.
_EINGANG_TEXT = re.compile(
    r"T(?:Ü|UE|.)RSCHLIE|AUTOMATIKT|SCHIEBET|EINGANG|WINDFANG", re.IGNORECASE)
_NOTAUSGANG_TEXT = re.compile(
    r"NOTAUSGANG|FLUCHTT|PANIK|\bE[12]\b", re.IGNORECASE)


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
                     fluchtweg_enden: list[XY] = (),
                     tuer_texte: list[tuple[str, XY]] = (),
                     kein_weg_ins_freie: BaseGeometry | None = None) -> list[Tuer]:
    """Setzt ``tuer_detail``/``ist_notausgang``/``untypisiert_grund`` in-place
    (Rückgabe = Eingabe). ``tuer_texte`` = türimplizierende Texte (b).

    ``kein_weg_ins_freie`` = Fläche ohne Weg ins Freie (geschlossene Höfe aus
    ``aussenbereich``). Türen dorthin werden KEIN ``hauseingang``: die AUSSEN-
    Klasse kommt bei Regel 1 auch aus ``nutzungsklasse`` (``TERRASSE`` →
    ``AUSSEN``) und würde sonst am Hof-Fix vorbei einen Endausgang erzeugen
    (Barawitzka EG: STIEGENHAUS raum_37 ↔ TERRASSE raum_43 im ummauerten Hof).
    ``None`` = Bestandsverhalten."""
    by_id = {r.id: r for r in raeume}
    eg = ist_erdgeschoss(geschoss)
    for t in tueren:
        ka, kb = _klasse(t.von_raum, by_id), _klasse(t.nach_raum, by_id)
        ta, tb = _typ(t.von_raum, by_id), _typ(t.nach_raum, by_id)
        klassen, typen = {ka, kb}, {ta, tb}
        detail = None
        # Notausgang-Zusatz: Tür ins Freie, an der eine Fluchtweglinie endet
        # oder die Doppelflügel-Breite hat — unabhängig davon, ob der
        # Innenraum schon typisiert ist (Mollgasse-Hoftüren: Raum untypisiert).
        if AUSSEN in klassen:
            endet_flw = any(math.dist(t.xy_mm, p) < _FLW_ENDE_NAH_MM
                            for p in fluchtweg_enden)
            if endet_flw or t.breite_mm > _DOPPELFLUEGEL_MM:
                t.ist_notausgang = True
        if AUSSEN in klassen and "ALLGEMEIN_ERSCHLIESSUNG" in klassen:
            if eg and not (kein_weg_ins_freie is not None
                           and kein_weg_ins_freie.distance(Point(t.xy_mm))
                           < _KEIN_WEG_NAH_MM):
                detail = "hauseingang"
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
        elif "GARAGE" in typen and t.breite_mm > _GARAGENTOR_MM:
            # Garagentor/Rolltor > 2.2 m — auch Tor GARAGE↔AUSSEN (Durchfahrt).
            # Endausgang wird es NUR, wenn ein Fluchtweg dort endet (Regel (e),
            # entscheidet leite_ausgaenge) — der Breiten-Notausgang gilt nicht.
            detail = "garagentor"
            t.ist_notausgang = False
        # (b) Türtext ≤ 1.5 m: Eingangs-Wort → hauseingang (EG), Notausgangs-
        # Wort → ist_notausgang; der Text wandert als Begründung in `quelle`.
        if detail is None or t.quelle and t.quelle.startswith("text:"):
            text = _naechster_text(t.xy_mm, tuer_texte)
            if text is not None:
                if _EINGANG_TEXT.search(text) and eg and detail is None:
                    detail = "hauseingang"
                # Balkontür/Garagentor haben ihr `ist_notausgang=False` aus einer
                # fachlichen Regel (Owner-Entscheidung, docs/OFFENE_FRAGEN.md) —
                # ein Türtext darf das nicht zurückdrehen (Muthgasse: das
                # Geschosskürzel „E2" im Türtext machte Balkontüren zu Ausgängen).
                if _NOTAUSGANG_TEXT.search(text) and detail not in (
                        "balkontuer", "garagentor"):
                    t.ist_notausgang = True
                if not (t.quelle or "").startswith("text:"):
                    t.quelle = f"{t.quelle or 'unbekannt'}+text:{text[:40]}"
        if detail is None and any(math.dist(t.xy_mm, p) < _BST_NAH_MM
                                  for p in brandschutz_hinweise):
            detail = "brandschutztuer"
        if t.tuer_detail is None:
            t.tuer_detail = detail
    markiere_windfang(tueren, raeume, geschoss)
    for t in tueren:
        if t.tuer_detail is None:
            t.untypisiert_grund = _untypisiert_grund(t, by_id)
    return tueren


def _naechster_text(xy: XY, texte: list[tuple[str, XY]]) -> str | None:
    best, best_d = None, _TEXT_NAH_MM
    for text, p in texte:
        d = math.dist(xy, p)
        if d < best_d:
            best, best_d = text, d
    return best


def markiere_windfang(tueren: list[Tuer], raeume: list[Raum],
                      geschoss: str) -> None:
    """(c) Windfang: ALLGEMEIN-Raum < 8 m² mit mind. 2 Türen, genau eine nach
    AUSSEN → die äußere Tür ist der Endausgang (hauseingang im EG)."""
    eg = ist_erdgeschoss(geschoss)
    by_id = {r.id: r for r in raeume}
    an_raum: dict[str, list[Tuer]] = {}
    for t in tueren:
        for s in (t.von_raum, t.nach_raum):
            if s and s not in (AUSSEN, "KEIN_RAUM"):
                an_raum.setdefault(s, []).append(t)
    for rid, ts in an_raum.items():
        r = by_id.get(rid)
        # mind. 2 Türen (durchgaenge_ohne_tuerblatt/aussen_durchgaenge hängen
        # zusätzliche Tür-Objekte an denselben Raum) — genau eine davon nach AUSSEN.
        if r is None or len(ts) < 2:
            continue
        klasse = r.nutzungsklasse or nutzungsklasse_fuer(r.raum_typ)
        flaeche = r.flaeche_m2 or _flaeche_m2(r)
        if not (klasse or "").startswith("ALLGEMEIN") or flaeche >= _WINDFANG_M2:
            continue
        aussen_t = [t for t in ts if AUSSEN in (t.von_raum, t.nach_raum)]
        if len(aussen_t) != 1:
            continue
        t = aussen_t[0]
        t.ist_notausgang = True
        if eg and t.tuer_detail in (None, "hauseingang"):
            t.tuer_detail = "hauseingang"
        t.quelle = f"{t.quelle or 'unbekannt'}+windfang"


def _flaeche_m2(r: Raum) -> float:
    if len(r.polygon_mm) < 3:
        return 0.0
    pts = r.polygon_mm
    a = 0.5 * abs(sum(x1 * y2 - x2 * y1
                      for (x1, y1), (x2, y2) in zip(pts, pts[1:] + pts[:1])))
    return a / 1e6


def _untypisiert_grund(t: Tuer, by_id: dict[str, Raum]) -> str:
    """Grund, warum keine Tür-Rolle bestimmt werden konnte (Berichts-Tabelle)."""
    seiten = (t.von_raum, t.nach_raum)
    typen = [_typ(s, by_id) for s in seiten]
    if any(ty in ("SCHACHT", "LIFT") for ty in typen):
        return "tuer_in_schacht"
    ohne_raum = [s in (None, "KEIN_RAUM") for s in seiten]
    if all(ohne_raum):
        return "tuer_ins_nichts"
    if any(ohne_raum):
        return "kein_nachbarraum"
    raeume_da = [by_id.get(s or "") for s in seiten if s != AUSSEN]
    if raeume_da and all(r is not None and not r.raum_typ for r in raeume_da):
        return "beide_seiten_untypisiert"
    return "unbekannte_kombination"
