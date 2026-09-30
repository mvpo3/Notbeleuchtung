"""sanitaer — Slice K3 (Enis Referenz 07): Bad und WC aus Sanitärbeleg.

Owner-Regel (2026-09-30): ein Raum ohne Stempel innerhalb einer Wohnung mit
mindestens zwei Sanitärobjekten (WC, Waschbecken, Dusche, Badewanne, Bidet)
wird BAD; mit genau WC oder WC plus Waschbecken wird WC. Sanitärobjekte aus
Blocknamen und Einbaulayer. Fliesenbelag allein reicht nicht. Der Raum muss
innerhalb eines Wohnungsumrisses liegen, sonst bleibt UNBEKANNT.

Planer-Präzisierung: Objekte als Multimenge — genau {WC} oder genau
{WC, Waschbecken} (je eines) → WC, sonst ≥ 2 Objekte → BAD, sonst unverändert;
nur Räume mit ``raum_typ == ""`` und ohne zugeordneten Stempel.
"""
from __future__ import annotations

from collections import Counter

import pytest

from notbeleuchtung.hauptengine.contracts.raum_modell import Raum, Tuer
from notbeleuchtung.raumerkennung import sanitaer as s


# ── Multimenge → Typ ────────────────────────────────────────────────────────
@pytest.mark.parametrize(("objekte", "typ"), [
    ({s.WC: 1}, "WC"),
    ({s.WC: 1, s.WASCHBECKEN: 1}, "WC"),
    # Rennweg OG3 „UNBEKANNT 6,6 m²": WC, Dusche, zwei Waschbecken
    ({s.WC: 1, s.WASCHBECKEN: 2, s.DUSCHE: 1}, "BAD"),
    # Mollgasse 2.OG: Waschtisch + Badewanne
    ({s.WASCHBECKEN: 1, s.BADEWANNE: 1}, "BAD"),
    ({s.WC: 1, s.WASCHBECKEN: 2}, "BAD"),     # nicht „genau" WC + Waschbecken
    ({s.WC: 2}, "BAD"),
    ({s.WC: 1, s.BIDET: 1}, "BAD"),
    ({s.DUSCHE: 1}, None),
    ({s.WASCHBECKEN: 1}, None),
    ({}, None),
])
def test_multimenge(objekte, typ):
    assert s.sanitaer_typ(Counter(objekte)) == typ


# ── Objekt aus Blockname UND Einbaulayer (gemessene Namen der drei Familien) ─
@pytest.mark.parametrize(("name", "layer", "klasse"), [
    # Rennweg (ArchiCAD „New_0xx")
    ("WC_1_Symbol 10[35]", "New_060 Möbel Einbau", s.WC),
    ("Waschbecken_3 10[56]", "New_065 Möbel Einrichtung", s.WASCHBECKEN),
    ("Shower Kit 27[38]", "New_060 Möbel Einbau", s.DUSCHE),
    ("Badewanne_freistehend[16]", "New_065 Möbel Einrichtung_Pen_No__31", s.BADEWANNE),
    # Mollgasse („07-SAN")
    ("07-WC", "07-SAN-G00-L02-M0", s.WC),
    ("07-WT-WC", "07-SAN-G00-L02-M0", s.WASCHBECKEN),    # Handwaschbecken im WC
    ("07-WT60", "07-SAN-G00-L02-M0", s.WASCHBECKEN),
    ("07-Badewanne", "07-SAN-G00-L02-M0", s.BADEWANNE),
    ("07-Dusche_2", "07-SAN-G00-L01-M0", s.DUSCHE),
    # Muthgasse (Revit „P-SANR-FIXT")
    ("WC UP-Spülkasten Betätigung vorne - 36 x 49cm-4213-E 5 - FOK AF 300",
     "P-SANR-FIXT", s.WC),
    ("Dusche bodeneben - Ablaufrinne - 1000x1300x90-77-E 5 - FOK AF 300",
     "P-SANR-FIXT", s.DUSCHE),
    ("Waschtisch - 45 x 35cm-12-E 5 - FOK AF 300", "P-SANR-FIXT", s.WASCHBECKEN),
    # kein Sanitärobjekt
    ("HNP_Extern_Duschset - HNP_Extern_Duschset-15208554-E 6 - FOK AF 300",
     "P-SANR-FIXT", None),                              # Armatur, gehört zur Dusche
    ("2D_barrierefrei_WC 130x190 - r75-5023949-E 5 - FOK AF 300",
     "A-GENM", None),                                   # Bewegungsfläche, kein Einbaulayer
    ("HNP_T_UZ_1-DF - HNP_T12_UZ-S_H_E0_1DF_80x200-WT-14495060-E 4 - FOK AF 300",
     "A-DOOR", None),                                   # Tür
    ("Spüle", "07-SAN-G00-L01-Küche", None),            # Küche, nicht in der Owner-Liste
    ("07-WM", "07-SAN-G00-L01-M0", None),               # Waschmaschine
    ("Urinal", "New_065 Möbel Einrichtung", None),      # nicht in der Owner-Liste
    ("Chair 02", "New_065 Möbel Einrichtung", None),
    ("Bad__6", "New_080 Raumdefinitionen", None),       # Zonenstempel, kein Objekt
])
def test_objektklasse_aus_blockname_und_einbaulayer(name, layer, klasse):
    assert s.objektklasse(name, layer) == klasse


# ── Kandidaten: nur Typ leer, ohne zugeordneten Stempel ──────────────────────
def _q(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def _raum(rid, typ="", poly=None, wohnung=None, klasse=None):
    return Raum(id=rid, raum_typ=typ, polygon_mm=poly or _q(0, 0, 2000, 2000),
                wohnung_id=wohnung, nutzungsklasse=klasse)


_BAD_OBJEKTE = [(s.WC, (500.0, 500.0)), (s.WASCHBECKEN, (1500.0, 500.0)),
                (s.WASCHBECKEN, (1500.0, 1500.0)), (s.DUSCHE, (500.0, 1500.0))]


def test_kandidat_bad_und_wc():
    raeume = [_raum("x"), _raum("y", poly=_q(3000, 0, 5000, 2000))]
    objekte = _BAD_OBJEKTE + [(s.WC, (3500.0, 500.0)), (s.WASCHBECKEN, (4500.0, 500.0))]
    kand = s.kandidaten(raeume, objekte, gestempelt=set())
    assert {rid: typ for rid, (typ, _) in kand.items()} == {"x": "BAD", "y": "WC"}
    assert kand["x"][1] == Counter({s.WASCHBECKEN: 2, s.WC: 1, s.DUSCHE: 1})


def test_kandidat_nicht_mit_stempel_nicht_mit_typ_nicht_mit_einem_objekt():
    raeume = [_raum("gestempelt"), _raum("typisiert", typ="ABSTELLRAUM"),
              _raum("dusche", poly=_q(3000, 0, 5000, 2000))]
    objekte = _BAD_OBJEKTE + [(s.DUSCHE, (3500.0, 500.0))]
    assert s.kandidaten(raeume, objekte, gestempelt={"gestempelt"}) == {}


def test_objekte_ausserhalb_zaehlen_nicht():
    """Fliesenbelag ist kein Objekt; ein Objekt zählt nur mit seiner Mitte im Raum."""
    raeume = [_raum("x")]
    objekte = [(s.WC, (500.0, 500.0)), (s.WASCHBECKEN, (2500.0, 500.0))]
    assert s.kandidaten(raeume, objekte, gestempelt=set()) == {
        "x": ("WC", Counter({s.WC: 1}))}


# ── Typisierung: Kontrolle über den Wohnungsumriss (Probe) ───────────────────
def _probe(nachbar_wohnung="top_1", nachbar_klasse="WOHNUNG_PRIVAT", nachbar_typ="ZIMMER"):
    """x (2 × 2 m, links Fassade) zwischen zwei Räumen; Tür x↔vr."""
    raeume = [_raum("x"),
              _raum("zi", "ZIMMER", _q(2100, 0, 6000, 4000), "top_1", "WOHNUNG_PRIVAT"),
              _raum("vr", nachbar_typ, _q(0, 2100, 2000, 4000), nachbar_wohnung,
                    nachbar_klasse)]
    tueren = [Tuer(id="t1", xy_mm=(1000.0, 2050.0), von_raum="x", nach_raum="vr")]
    return raeume, tueren


def test_bad_im_umriss_wird_bad_wohnung_bleibt_offen():
    """Der Vorlauf setzt Typ und Flags wie ein Stempel „Bad" — Klasse und
    Wohnung vergibt danach der reguläre Lauf aus rohen Türen (Grundsatz (b))."""
    raeume, tueren = _probe()
    echt = [r.model_copy(deep=True) for r in raeume]
    kand = s.kandidaten(raeume, _BAD_OBJEKTE, gestempelt=set())
    befund = s.typisiere_sanitaer(echt, kand, raeume, tueren)
    x = echt[0]
    assert (x.raum_typ, x.ist_fluchtweg, x.ist_communal) == ("BAD", False, False)
    assert x.wohnung_id is None and x.nutzungsklasse is None
    assert len(befund) == 1 and befund[0].startswith("x: BAD") and "top_1" in befund[0]
    assert raeume[0].raum_typ == ""                 # die Probe bleibt unberührt


@pytest.mark.parametrize(("wohnung", "klasse", "typ"), [
    (None, "ALLGEMEIN_ERSCHLIESSUNG", "GANG"),     # Erschließung (Mollgasse 3.OG)
    ("top_2", "WOHNUNG_PRIVAT", "VORRAUM"),        # zweite Wohnung
    (None, None, ""),                              # unbekannter Nachbar
])
def test_nicht_im_umriss_bleibt_unbekannt(wohnung, klasse, typ):
    raeume, tueren = _probe(wohnung, klasse, typ)
    echt = [r.model_copy(deep=True) for r in raeume]
    kand = s.kandidaten(raeume, _BAD_OBJEKTE, gestempelt=set())
    befund = s.typisiere_sanitaer(echt, kand, raeume, tueren)
    assert echt[0].raum_typ == ""
    assert len(befund) == 1 and "bleibt UNBEKANNT" in befund[0]
