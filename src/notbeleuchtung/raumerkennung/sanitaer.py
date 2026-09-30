"""sanitaer — Bad und WC aus Sanitärbeleg (Slice K3, Enis Referenz 07).

Owner-Regel (2026-09-30, wörtlich): „ein Raum ohne Stempel innerhalb einer
Wohnung mit mindestens zwei Sanitärobjekten (WC, Waschbecken, Dusche,
Badewanne, Bidet) wird BAD; mit genau WC oder WC plus Waschbecken wird WC.
Sanitärobjekte aus Blocknamen und Einbaulayer, wie bei der Fenstererkennung
nach Erscheinungsbild. Fliesenbelag allein reicht nicht, wie Enis schreibt. Der
Top-Stempel ist Kontrolle: der Raum muss innerhalb eines Wohnungsumrisses
liegen, sonst bleibt UNBEKANNT."

Planer-Präzisierung: Objekte als Multimenge — genau {WC} oder genau
{WC, Waschbecken} (je eines) → WC, sonst ≥ 2 Objekte → BAD, sonst unverändert;
nur Räume mit ``raum_typ == ""`` und ohne zugeordneten Stempel.

**Objekt** = ein INSERT im Architektur-Raum, dessen Blockname die Art nennt UND
der auf einem Möbel-/Einbau-/Sanitär-Layer liegt (gemessen: Rennweg ``New_060
Möbel Einbau``/``New_065 Möbel Einrichtung``, Mollgasse ``07-SAN-…``, Muthgasse
``P-SANR-FIXT``). Der Layer hält Bewegungsflächen (Muthgasse ``A-GENM``
„2D_barrierefrei_WC") und Türen („…-WT-…" auf ``A-DOOR``) draußen. Fliesen sind
kein Objekt und werden nie gelesen. Lage = Mitte der Block-Bbox (der
Einfügepunkt liegt bis 836 mm neben der Mitte, ``aussenbereich._beleg_punkte``).
Nicht gebaut: Sanitärobjekte als zerlegte Linien OHNE Block (Barawitzka
``540 Sanitäreinrichtung``, Erkennung nach Erscheinungsbild wie
``fenster_signatur``) — gemessen 0 Kandidaten mit solcher Geometrie auf den 23
Prüfgeschossen und im Gate-Plan Barawitzka EG.

**Reihenfolge (Einbahn, Owner Board 7):** der Wohnungsumriss steht erst nach
``bilde_wohnungen`` fest, die Türrollen brauchen den Typ vorher. Darum ein
Vorlauf ohne Rückkopplung (``provider``): Türen und Wohnungen einmal als Probe
auf Kopien, ``typisiere_sanitaer`` prüft darin den Umriss und setzt am echten
Raum nur Typ und Flags — wie ein Stempel „Bad"/„WC". Danach läuft EIN
regulärer Durchlauf; Klasse und Wohnung entstehen dort wie für jeden
gestempelten Raum aus rohen Türen (Grundsatz (b) 2026-09-22). Keine Iteration.
"""
from __future__ import annotations

import re
from collections import Counter

from ezdxf import bbox
from shapely.geometry import Point, Polygon

from notbeleuchtung.hauptengine.contracts.raum_modell import Raum, Tuer

from .dxf_load import DxfPlan
from .raumtyp import raumtyp_flags
from .wohnungsumriss import umschliessende_wohnung

XY = tuple[float, float]

WC, WASCHBECKEN, DUSCHE, BADEWANNE, BIDET = (
    "WC", "WASCHBECKEN", "DUSCHE", "BADEWANNE", "BIDET")

#: Blockname → Objektart, erste passende gewinnt: „07-WT-WC" ist der
#: Handwaschbecken-Block im WC (Mollgasse), also Waschbecken vor WC. Gemessene
#: Namen der drei Familien stehen in tests/raumerkennung/test_sanitaer.py.
_ART = tuple((art, re.compile(muster, re.IGNORECASE)) for art, muster in (
    (WASCHBECKEN, r"WASCHBECKEN|WASCHTISCH|(?<![A-Z])WT(?![A-Z])"),
    (WC, r"(?<![A-Z])WC(?![A-Z])"),
    (DUSCHE, r"DUSCH|SHOWER"),
    (BADEWANNE, r"WANNE"),
    (BIDET, r"BIDET"),
))
#: Zubehör mit Objektnamen: „HNP_Extern_Duschset" ist die Armatur der Dusche,
#: die als „Dusche bodeneben" schon zählt (Muthgasse 119 : 118).
_ZUBEHOER = re.compile(r"DUSCHSET", re.IGNORECASE)
#: Möbel-/Einbau-/Sanitär-Layer der Familien (``M.{1,2}BEL``: Umlaut ggf.
#: cp-dekodiert).
_EINBAU_LAYER = re.compile(r"M.{1,2}BEL|EINBAU|SAN", re.IGNORECASE)


def objektklasse(blockname: str, layer: str) -> str | None:
    """Objektart eines Blocks, None wenn kein Sanitärobjekt der Owner-Liste."""
    if not _EINBAU_LAYER.search(layer) or _ZUBEHOER.search(blockname):
        return None
    return next((art for art, rx in _ART if rx.search(blockname)), None)


def sanitaerobjekte(plan: DxfPlan) -> list[tuple[str, XY]]:
    """(Art, Bbox-Mitte in mm) aller Sanitärobjekte im Architektur-Raum."""
    out: list[tuple[str, XY]] = []
    for e in plan.space:
        if e.dxftype() != "INSERT":
            continue
        art = objektklasse(str(e.dxf.name), str(e.dxf.layer))
        if art is None:
            continue
        try:
            box = bbox.extents([e], fast=True)
        except Exception:  # noqa: BLE001, S112 — kaputte Block-Referenz überspringen
            continue
        if box.has_data:
            out.append((art, plan._scale(box.center)))
    return out


def sanitaer_typ(objekte: Counter) -> str | None:
    """Multimenge der Objektarten → ``"WC"``, ``"BAD"`` oder None."""
    if objekte in (Counter({WC: 1}), Counter({WC: 1, WASCHBECKEN: 1})):
        return "WC"
    return "BAD" if sum(objekte.values()) >= 2 else None


def kandidaten(raeume: list[Raum], objekte: list[tuple[str, XY]],
               gestempelt: set[str]) -> dict[str, tuple[str, Counter]]:
    """``{raum_id: (typ, objekte)}`` der stempellosen Räume ohne Typ, deren
    Sanitärobjekte einen Typ ergeben — noch ohne Umriss-Kontrolle."""
    out: dict[str, tuple[str, Counter]] = {}
    for r in raeume:
        if r.raum_typ or r.id in gestempelt or len(r.polygon_mm) < 3:
            continue
        g = Polygon(r.polygon_mm).buffer(0)
        drin = Counter(art for art, xy in objekte if g.contains(Point(xy)))
        typ = sanitaer_typ(drin)
        if typ is not None:
            out[r.id] = (typ, drin)
    return out


def typisiere_sanitaer(raeume: list[Raum], kand: dict[str, tuple[str, Counter]],
                       probe_raeume: list[Raum], probe_tueren: list[Tuer]) -> list[str]:
    """Setzt an ``raeume`` Typ und Flags der Kandidaten, die in der Probe im
    Umriss einer Wohnung liegen; liefert je Kandidat eine Befundzeile.
    ``wohnung_id`` und ``nutzungsklasse`` bleiben unberührt (regulärer Lauf)."""
    probe = {r.id: r for r in probe_raeume}
    echt = {r.id: r for r in raeume}
    befund: list[str] = []
    for rid, (typ, drin) in kand.items():
        beleg = ", ".join(f"{art} {n}" for art, n in sorted(drin.items()))
        wid, grund = umschliessende_wohnung(probe[rid], probe_raeume, probe_tueren)
        if wid is None:
            befund.append(f"{rid}: bleibt UNBEKANNT — Sanitärbeleg {typ} ({beleg}), "
                          f"aber nicht im Umriss einer Wohnung: {grund}")
            continue
        r = echt[rid]
        r.raum_typ, r.ist_fluchtweg, r.ist_communal = raumtyp_flags(typ)
        befund.append(f"{rid}: {typ} aus Sanitärbeleg ({beleg}) im Umriss {wid} "
                      f"(Probe) — {grund}")
    return befund
