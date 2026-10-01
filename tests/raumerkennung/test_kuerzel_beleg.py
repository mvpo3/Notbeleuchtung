"""Abschnitt 1 (Owner 2026-10-01, Entscheid 1): ein Raumkürzel im Raumpolygon ist
Typbeleg — auch ohne Flächenzeile. Ausschluss: Text außerhalb jedes Polygons,
Legenden-/Plankopf-Layer, Achs-/Schnittmarken (Einzelbuchstaben/Zahlen),
Stufen-Beschriftung („17 STG 17/29"). Mehrdeutige Kürzel (SR, TR, KA) bleiben
untypisiert mit Grund; ≥ 2 Sanitärobjekte schlagen AR/ZIMMER."""
from __future__ import annotations

import pytest

from notbeleuchtung.hauptengine.contracts.raum_modell import Raum
from notbeleuchtung.raumerkennung.kuerzel_beleg import kuerzel_typ, typisiere_kuerzel

RAUM = [(0.0, 0.0), (4000.0, 0.0), (4000.0, 3000.0), (0.0, 3000.0)]
RAUM2 = [(5000.0, 0.0), (9000.0, 0.0), (9000.0, 3000.0), (5000.0, 3000.0)]


def _raum(rid: str, poly=RAUM, typ: str = "") -> Raum:
    return Raum(id=rid, raum_typ=typ, polygon_mm=list(poly), flaeche_m2=12.0)


# ── Kürzeltabelle: Varianten ────────────────────────────────────────────────
@pytest.mark.parametrize(
    "text, erwartet",
    [
        ("STGH", "STIEGENHAUS"), ("STGH.", "STIEGENHAUS"), ("stgh", "STIEGENHAUS"),
        ("Stgh.", "STIEGENHAUS"),
        ("VR", "VORRAUM"), ("Vr.", "VORRAUM"), ("Vorr.", "VORRAUM"),
        ("AR", "ABSTELLRAUM"), ("ar", "ABSTELLRAUM"),
        ("BAD", "BAD"), ("Bad", "BAD"), ("BAD/WC", "BAD"), ("BAD-WC", "BAD"),
        ("WC", "WC"),
        ("LOGGIA", "BALKON"), ("WOHNRAUM", "WOHNZIMMER"), ("GANG", "GANG"),
        ("TREPPENHAUS 1", "STIEGENHAUS"), ("KIWA", "KINDERWAGENRAUM"),
    ],
)
def test_kuerzel_varianten(text, erwartet):
    tf = kuerzel_typ(text)
    assert isinstance(tf, tuple), f"{text!r} → {tf!r}"
    assert tf[0] == erwartet


# ── Ausschluss: Form (Achsmarken, Stufen, Fließtext, Höhenkoten) ───────────
@pytest.mark.parametrize(
    "text",
    [
        "A", "B", "1", "12", "A-A", "B–B",                      # Achs-/Schnittmarken
        "17 STG 17/29", "20 STG 19/29", "1 Stg 20/24", "15 STG",  # Stufen-Beschriftung
        "STUK = 225 Ü. FOK STGH = -0.70",                       # Höhenkote mit „STGH"
        "WOHNFLÄCHE (INKL.LOGGIA)", "TERRASSE/BALKON/GARTEN",   # Top-Summenblock
        "RDUK BALKON = +1.58 FDUK = RDUK", "LUFTRAUM GARAGE",
        "GULLY MÜLL", "T KIWA", "KA STG1 (+1)", "LÜFTUNG SCHLEUSE",
        "12.78 m²", "Parkett", "GANG KA", "2_02_BÜRO", "KA 101", "WC/DU", "Zul.KA", "Zul.KA 1",
    ],
)
def test_kein_kuerzel_text(text):
    assert kuerzel_typ(text) is None, text


# ── Mehrdeutig / Kandidat ───────────────────────────────────────────────────
@pytest.mark.parametrize("text", ["SR", "TR", "KA", "KA 10", "Schl.", "sr"])
def test_mehrdeutige_kuerzel_bleiben_offen(text):
    assert kuerzel_typ(text) == "mehrdeutig"


def test_mehrdeutig_bleibt_untypisiert_mit_grund():
    r = _raum("rest_1")
    warn: list[str] = []
    typisiere_kuerzel([("SR", (2000.0, 1500.0), "Raum")], [r], list,
                      hinweise=[], warnungen=warn)
    assert r.raum_typ == ""
    assert warn and "rest_1" in warn[0] and "mehrdeutig" in warn[0] and "SR" in warn[0]


# ── Polygon-Bedingung, Legende, Eindeutigkeit ───────────────────────────────
def test_kuerzel_im_polygon_typisiert_rest_raum():
    r = _raum("rest_2")
    hinw: list[str] = []
    typisiere_kuerzel([("STGH", (2000.0, 1500.0), "Raum-Beschriftung")], [r], list,
                      hinweise=hinw, warnungen=[])
    assert (r.raum_typ, r.ist_fluchtweg, r.ist_communal) == ("STIEGENHAUS", True, True)
    assert hinw and "rest_2" in hinw[0] and "STGH" in hinw[0]


def test_text_ausserhalb_jedes_polygons_zaehlt_nicht():
    r = _raum("rest_1")
    typisiere_kuerzel([("STGH", (4500.0, 1500.0), "Raum")], [r], list,
                      hinweise=[], warnungen=[])
    assert r.raum_typ == ""


def test_legenden_layer_zaehlt_nicht():
    r = _raum("rest_1")
    typisiere_kuerzel([("STGH", (2000.0, 1500.0), "A-LEGENDE")], [r], list,
                      hinweise=[], warnungen=[])
    assert r.raum_typ == ""


def test_typisierter_raum_bleibt():
    r = _raum("raum_1", typ="KÜCHE")
    typisiere_kuerzel([("STGH", (2000.0, 1500.0), "Raum")], [r], list,
                      hinweise=[], warnungen=[])
    assert r.raum_typ == "KÜCHE"


def test_zwei_typen_im_polygon_nicht_eindeutig():
    r = _raum("rest_1")
    warn: list[str] = []
    typisiere_kuerzel([("BAD", (1000.0, 1500.0), "Raum"), ("GANG", (3000.0, 1500.0), "Raum")],
                      [r], list, hinweise=[], warnungen=warn)
    assert r.raum_typ == ""
    assert warn and "nicht eindeutig" in warn[0] and "BAD" in warn[0] and "GANG" in warn[0]


def test_gleicher_typ_zweimal_ist_eindeutig():
    r = _raum("rest_1")
    typisiere_kuerzel([("VR", (1000.0, 1500.0), "Raum"), ("Vorr.", (3000.0, 1500.0), "Raum")],
                      [r], list, hinweise=[], warnungen=[])
    assert r.raum_typ == "VORRAUM"


def test_jeder_raum_eigenes_kuerzel():
    a, b = _raum("rest_1"), _raum("rest_2", RAUM2)
    typisiere_kuerzel([("VR", (2000.0, 1500.0), "Raum"), ("AR", (7000.0, 1500.0), "Raum")],
                      [a, b], list, hinweise=[], warnungen=[])
    assert (a.raum_typ, b.raum_typ) == ("VORRAUM", "ABSTELLRAUM")


# ── Erscheinungsbild schlägt Kürzel (≥ 2 Sanitärobjekte) ────────────────────
def test_sanitaer_schlaegt_ar():
    r = _raum("rest_1")
    warn: list[str] = []
    san = [("WC", (1000.0, 1000.0)), ("WASCHBECKEN", (1500.0, 1000.0))]
    typisiere_kuerzel([("AR", (2000.0, 1500.0), "Raum")], [r], lambda: san,
                      hinweise=[], warnungen=warn)
    assert r.raum_typ == ""
    assert warn and "AR" in warn[0] and "Sanit" in warn[0] and "rest_1" in warn[0]


def test_ein_sanitaerobjekt_schlaegt_nicht():
    r = _raum("rest_1")
    typisiere_kuerzel([("AR", (2000.0, 1500.0), "Raum")], [r], lambda: [("WC", (1000.0, 1000.0))],
                      hinweise=[], warnungen=[])
    assert r.raum_typ == "ABSTELLRAUM"


def test_sanitaer_stoert_bad_nicht():
    r = _raum("rest_1")
    san = [("WC", (1000.0, 1000.0)), ("WASCHBECKEN", (1500.0, 1000.0))]
    typisiere_kuerzel([("BAD", (2000.0, 1500.0), "Raum")], [r], lambda: san,
                      hinweise=[], warnungen=[])
    assert r.raum_typ == "BAD"


# ── Dominanter Stempel bei widersprechenden Kürzeln (Am Rain OG4 rest_2) ─────
def _stempel(name, typ, m2, xy):
    from notbeleuchtung.raumerkennung.stempel_anker import Stempel

    return Stempel(name=name, typ=typ, flaeche_m2=m2, belag=None, position_mm=xy,
                   quelle="TEXT", layer="Raum-Beschriftung")


def test_dominanter_stempel_entscheidet():
    r = _raum("rest_2")                          # 12 m²
    hinw: list[str] = []
    st = [_stempel("STGH", "STIEGENHAUS", 9.0, (2000.0, 1000.0)),
          _stempel("VR", "VORRAUM", 2.5, (3500.0, 2500.0))]
    typisiere_kuerzel([("STGH", (2000.0, 1500.0), "Raum"), ("VR", (3500.0, 2800.0), "Raum"),
                       ("Schacht-", (500.0, 500.0), "Beschriften")],
                      [r], list, hinweise=hinw, warnungen=[], stempel=st)
    assert r.raum_typ == "STIEGENHAUS"
    assert hinw and "dominante Stempel" in hinw[0] and "75 %" in hinw[0]


def test_kein_dominanter_stempel_nicht_eindeutig():
    r = _raum("rest_2")                          # 12 m², zwei Stempel je 4 m² (33 %)
    warn: list[str] = []
    st = [_stempel("STGH", "STIEGENHAUS", 4.0, (2000.0, 1000.0)),
          _stempel("VR", "VORRAUM", 4.0, (3500.0, 2500.0))]
    typisiere_kuerzel([("STGH", (2000.0, 1500.0), "Raum"), ("VR", (3500.0, 2800.0), "Raum")],
                      [r], list, hinweise=[], warnungen=warn, stempel=st)
    assert r.raum_typ == ""
    assert warn and "nicht eindeutig" in warn[0] and "kein dominanter Stempel" in warn[0]


def test_trennstrich_fragment_ist_kein_kuerzel():
    assert kuerzel_typ("Schacht-") is None
    assert kuerzel_typ("SCHACHT") is not None


def test_raum_mit_stempel_ohne_typ_bleibt():
    # Rennweg EG raum_12 „GESCHÄFTLOKAL" (Stempel ohne Kanon-Typ, Enis) trägt die
    # Möbelbeschriftung „Garderobe" — kein Gegenbeleg, der Raum bleibt wie er ist.
    r = _raum("raum_12")
    hinw: list[str] = []
    typisiere_kuerzel([("Garderobe", (2000.0, 1500.0), "Beschriftung")], [r], list,
                      hinweise=hinw, warnungen=[], gestempelt={"raum_12"})
    assert r.raum_typ == "" and not hinw
