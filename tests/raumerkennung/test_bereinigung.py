"""Raumbereinigung — die fünf Owner-Regeln, Loch-Kodierung, Buchhaltung.

Rein synthetisch (mm-Rechtecke), kein DXF, kein Netz, keine Fixtures. Die
Konstellationen sind so gebaut, dass jeweils GENAU eine Regel greift — sonst
prüft der Test die Reihenfolge statt der Regel.
"""
from __future__ import annotations

import pytest
from pydantic import ValidationError
from shapely.geometry import Point, Polygon

from notbeleuchtung.hauptengine.contracts.raum_modell import Bereinigung, Raum
from notbeleuchtung.raumerkennung import bereinigung as bm
from notbeleuchtung.raumerkennung.bereinigung import (
    RAUSCH_MM2,
    bereinige,
    bereinige_kaskade,
    ueberlappung,
)
from notbeleuchtung.raumerkennung.stempel_anker import Stempel, Zuordnung


def _rect(x0: float, y0: float, x1: float, y1: float) -> list[tuple[float, float]]:
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def _raum(rid: str, ring: list, typ: str = "") -> Raum:
    return Raum(id=rid, raum_typ=typ, polygon_mm=ring,
                flaeche_m2=Polygon(ring).area / 1e6)


def _stempel(flaeche: float | None) -> Stempel:
    return Stempel(name="Raum", typ=None, flaeche_m2=flaeche, belag=None,
                   position_mm=(0.0, 0.0), quelle="MTEXT", layer="L")


def _regeln(b) -> list[str]:
    return [e.regel for e in b.eintraege]


def _buchhaltung_haelt(raeume: list[Raum], erg: dict) -> None:
    """Invariante § 3.5.5: roh − bereinigt == Σ gebuchte Flächen (± 1 mm²)."""
    for r in raeume:
        b = erg.get(r.id)
        if b is None:
            continue
        roh = Polygon(r.polygon_mm).area / 1e6
        gebucht = sum(e.flaeche_m2 for e in b.eintraege)
        assert abs((roh - b.flaeche_m2) - gebucht) <= 1e-6, (
            f"{r.id}: roh {roh:.6f} − bereinigt {b.flaeche_m2:.6f} "
            f"!= gebucht {gebucht:.6f}")


# --------------------------------------------------------------- ohne Regel

def test_ohne_ueberlappung_bleibt_unveraendert():
    a = _raum("a", _rect(0, 0, 4000, 4000))
    b = _raum("b", _rect(5000, 0, 9000, 4000))
    erg = bereinige([a, b], {"a": "L", "b": "L"}, {})
    assert erg["a"].eintraege == [] and erg["b"].eintraege == []
    assert not erg["a"].entfallen and not erg["b"].entfallen
    assert Polygon(erg["a"].polygon_mm).area == pytest.approx(16e6)


# ----------------------------------------------------------------- Regel 1

def test_regel1_lift_wird_ausgestanzt():
    # Lift ragt über den Rand → kein Enthaltensein, Regel 1 entscheidet allein.
    raum = _raum("raum_1", _rect(0, 0, 10000, 10000), "ZIMMER")
    lift = _raum("lift_1", _rect(9000, 4000, 11000, 6000), "LIFT")
    erg = bereinige([raum, lift], {"raum_1": "L", "lift_1": "R"}, {})
    assert erg["lift_1"].eintraege == []          # Gewinner bekommt keinen Eintrag
    assert _regeln(erg["raum_1"]) == ["LIFT_SCHACHT"]
    assert erg["raum_1"].eintraege[0].gegenspieler == "lift_1"
    assert erg["raum_1"].eintraege[0].flaeche_m2 == pytest.approx(2.0)
    _buchhaltung_haelt([raum, lift], erg)


def test_regel1_nur_exakt_lift_und_schacht():
    # AUFZUGSVORPLATZ löst Regel 1 NICHT aus: der Rang entscheidet, also
    # verliert der Vorplatz (F, Rang 3) gegen den L-Raum mit Stempel (Rang 1).
    raum = _raum("a", _rect(0, 0, 10000, 10000), "ZIMMER")
    vor = _raum("b", _rect(9000, 4000, 11000, 6000), "AUFZUGSVORPLATZ")
    erg = bereinige([raum, vor], {"a": "L", "b": "F"}, {"a": 100.0})
    assert _regeln(erg["a"]) == [] and _regeln(erg["b"]) == ["QUELLE_RANG"]
    # SCHACHT an derselben Stelle gewinnt dagegen trotz schlechterer Quelle.
    schacht = _raum("b", _rect(9000, 4000, 11000, 6000), "SCHACHT")
    erg = bereinige([raum, schacht], {"a": "L", "b": "F"}, {"a": 100.0})
    assert _regeln(erg["a"]) == ["LIFT_SCHACHT"] and _regeln(erg["b"]) == []


def test_regel1_beide_lift_schacht_geht_zu_regel2():
    gross = _raum("a", _rect(0, 0, 4000, 4000), "SCHACHT")
    klein = _raum("b", _rect(1000, 1000, 3000, 3000), "LIFT")
    erg = bereinige([gross, klein], {"a": "L", "b": "R"}, {})
    assert _regeln(erg["b"]) == []
    assert "ENTHALTENSEIN" in _regeln(erg["a"])    # Regel 2, nicht Regel 1


# ----------------------------------------------------------------- Regel 2

def test_regel2_enthaltensein_beide_bleiben():
    gross = _raum("a", _rect(0, 0, 20000, 20000), "ZIMMER")
    klein = _raum("b", _rect(8000, 8000, 12000, 12000), "WC")
    erg = bereinige([gross, klein], {"a": "L", "b": "F"}, {})
    assert _regeln(erg["b"]) == [] and not erg["b"].entfallen
    assert _regeln(erg["a"])[0] == "ENTHALTENSEIN"
    assert not erg["a"].entfallen                  # der äußere bleibt auch
    ring = Polygon(erg["a"].polygon_mm)
    assert ring.is_valid and len(ring.interiors) == 0
    assert not ring.covers(Point(10000, 10000))    # Loch liegt außen
    _buchhaltung_haelt([gross, klein], erg)


def test_regel2_duplikat_faellt_auf_regel3():
    # Deckungsgleiche Polygone: beide Verhältnisse 1,0 → Regel 2 greift NICHT.
    ring = _rect(0, 0, 4000, 4000)
    a, b = _raum("a", ring), _raum("b", list(ring))
    erg = bereinige([a, b], {"a": "L", "b": "F"}, {"a": 16.0})
    assert "ENTHALTENSEIN" not in _regeln(erg["a"]) + _regeln(erg["b"])
    assert _regeln(erg["a"]) == []
    assert _regeln(erg["b"]) == ["QUELLE_RANG", "ENTFALL"]
    assert erg["b"].entfallen
    _buchhaltung_haelt([a, b], erg)


# ----------------------------------------------------------------- Regel 3

def test_regel3a_quellen_rang():
    a = _raum("a", _rect(0, 0, 6000, 4000))
    b = _raum("b", _rect(5000, 0, 11000, 4000))
    erg = bereinige([a, b], {"a": "L", "b": "F"}, {"a": 24.0})
    assert _regeln(erg["a"]) == [] and _regeln(erg["b"]) == ["QUELLE_RANG"]
    assert erg["b"].eintraege[0].flaeche_m2 == pytest.approx(4.0)
    # H ohne Stempel (Rang 2) verliert gegen L mit Stempel (Rang 1).
    erg = bereinige([a, b], {"a": "L", "b": "H"}, {"a": 24.0})
    assert _regeln(erg["b"]) == ["QUELLE_RANG"]


def test_regel3b_naeher_am_stempelwert():
    a = _raum("a", _rect(0, 0, 5000, 4000))        # 20 m², Stempel 20 → Abw 0
    b = _raum("b", _rect(4000, 0, 9000, 4000))     # 20 m², Stempel 10 → Abw 1,0
    erg = bereinige([a, b], {"a": "L", "b": "L"}, {"a": 20.0, "b": 10.0})
    assert _regeln(erg["a"]) == [] and _regeln(erg["b"]) == ["STEMPEL_NAEHE"]
    # flaeche_stempel == 0.0 zählt als VORHANDEN → Regel 3b greift, nicht Regel 4.
    erg = bereinige([a, b], {"a": "L", "b": "L"}, {"a": 20.0, "b": 0.0})
    assert _regeln(erg["b"]) == ["STEMPEL_NAEHE"]


def test_regel4_schwerpunkt():
    # Beide H ohne Stempel → gleicher Rang, kein Stempelwert: nur Regel 4 bleibt.
    a = _raum("a", _rect(0, 0, 4000, 4000))        # Schwerpunkt 1500 mm entfernt
    b = _raum("b", _rect(3000, 0, 13000, 4000))    # Schwerpunkt 4500 mm entfernt
    erg = bereinige([a, b], {"a": "H", "b": "H"}, {})
    assert _regeln(erg["a"]) == [] and _regeln(erg["b"]) == ["SCHWERPUNKT"]
    assert erg["b"].eintraege[0].flaeche_m2 == pytest.approx(4.0)


# ----------------------------------------------------------------- Regel 5

def test_regel5_restflaeche_ragt_nie_ueber():
    l_ring = _rect(0, 0, 10000, 10000)
    li = _raum("l", l_ring)
    re = _raum("rest_1", _rect(9000, 0, 12000, 3000))
    erg = bereinige([li, re], {"l": "L", "rest_1": "R"}, {}, regeln=frozenset({5}))
    assert _regeln(erg["l"]) == []
    assert _regeln(erg["rest_1"]) == ["RESTFLAECHE"]
    assert erg["rest_1"].eintraege[0].gegenspieler == "l"
    rest = Polygon(erg["rest_1"].polygon_mm)
    assert rest.intersection(Polygon(l_ring)).area <= RAUSCH_MM2
    _buchhaltung_haelt([li, re], erg)


def test_regel5_stanzt_keinen_schacht_aus():
    """Owner-Reihenfolge: Regel 1 vor Regel 5 — SCHACHT bleibt SCHACHT.

    Ohne die Ausnahme stanzte Regel 5 die SCHACHT-Räume aus dem R-Zweig
    (``rest_komponenten.py:98-100``) wieder aus; zwei Rennweg-Schächte liegen
    nur 0,15 m² über der Entfall-Schwelle.
    """
    l_ring = _rect(0, 0, 10000, 10000)
    li = _raum("l", l_ring, "STIEGENHAUS")
    schacht = _raum("rest_1", _rect(9000, 4000, 12000, 7000), "SCHACHT")
    erg = bereinige([li, schacht], {"l": "L", "rest_1": "R"}, {"l": 100.0})
    assert _regeln(erg["rest_1"]) == []            # kein RESTFLAECHE-Abzug
    assert not erg["rest_1"].entfallen
    assert Polygon(erg["rest_1"].polygon_mm).area == pytest.approx(9e6)
    assert _regeln(erg["l"]) == ["LIFT_SCHACHT"]


# --------------------------------------------------- Loch-/Schlitz-Kodierung

def test_schlitz_mehrere_loecher_gueltig():
    gross = _raum("a", _rect(0, 0, 20000, 20000))
    loecher = [_raum("b", _rect(2000, 2000, 4000, 4000)),
               _raum("c", _rect(8000, 8000, 10000, 10000)),
               _raum("d", _rect(15000, 15000, 17000, 17000))]
    erg = bereinige([gross, *loecher], {"a": "L", "b": "F", "c": "F", "d": "F"}, {})
    ring = Polygon(erg["a"].polygon_mm)
    assert ring.is_valid and len(ring.interiors) == 0
    for mitte in ((3000, 3000), (9000, 9000), (16000, 16000)):
        assert not ring.covers(Point(mitte)), f"{mitte} müsste im Loch liegen"
    assert _regeln(erg["a"]).count("ENTHALTENSEIN") == 3
    assert "SCHLITZ" in _regeln(erg["a"])
    _buchhaltung_haelt([gross, *loecher], erg)


def test_schlitz_loch_beruehrt_aussenkontur():
    # (1) Loch 0,3 mm vom Rand; (2) Loch, das die durch Loch (1) entstandene
    # Einbuchtung in einem Punkt berührt → Kodierung muss beides tragen.
    gross = _raum("a", _rect(0, 0, 10000, 10000))
    nah = _raum("b", _rect(300, 3000, 2300, 5000))
    ecke = _raum("c", _rect(2300, 5000, 4300, 7000))
    erg = bereinige([gross, nah, ecke], {"a": "L", "b": "F", "c": "F"}, {})
    ring = Polygon(erg["a"].polygon_mm)
    assert ring.is_valid and len(ring.interiors) == 0
    assert not ring.covers(Point(1300, 4000))
    assert not ring.covers(Point(3300, 6000))
    _buchhaltung_haelt([gross, nah, ecke], erg)


# ------------------------------------------------------- Zerfall und Entfall

def test_zerfall_groesste_komponente():
    # Balken (L mit Stempel) schneidet den F-Raum in 12 m² und 20 m².
    f = _raum("a", _rect(0, 0, 10000, 4000))
    balken = _raum("b", _rect(3000, -1000, 5000, 5000))
    erg = bereinige([f, balken], {"a": "F", "b": "L"}, {"b": 12.0})
    assert _regeln(erg["a"]) == ["QUELLE_RANG", "ZERFALL"]
    assert erg["a"].eintraege[1].flaeche_m2 == pytest.approx(12.0)
    assert erg["a"].eintraege[1].gegenspieler is None
    assert erg["a"].flaeche_m2 == pytest.approx(20.0)
    _buchhaltung_haelt([f, balken], erg)


def test_entfall_unter_einem_quadratmeter():
    a = _raum("a", _rect(0, 0, 4000, 4000))              # 16 m²
    b = _raum("b", _rect(0, 0, 4000, 3800))              # 15,2 m² Gewinner
    erg = bereinige([a, b], {"a": "F", "b": "L"}, {"b": 15.2})
    assert erg["a"].entfallen
    assert erg["a"].polygon_mm == [] and erg["a"].flaeche_m2 == 0.0
    assert _regeln(erg["a"])[-1] == "ENTFALL"
    assert erg["a"].eintraege[-1].flaeche_m2 == pytest.approx(0.8)
    assert erg["a"].eintraege[-1].gegenspieler is None
    assert not erg["b"].entfallen
    _buchhaltung_haelt([a, b], erg)


# ------------------------------------------------------------------ Adapter

def _kaskade_fall() -> tuple[list[Raum], list[Raum], list[Zuordnung], dict]:
    """Gewinner, Verlierer (entfällt) und ein unbeteiligter Raum mit Zuordnungen."""
    gewinner = _raum("raum_1", _rect(0, 0, 4000, 3800))
    verlierer = _raum("raum_2", _rect(0, 0, 4000, 4000))
    frei = _raum("raum_3", _rect(20000, 0, 24000, 4000))
    raeume = [gewinner, verlierer, frei]
    zuord = [Zuordnung(_stempel(15.2), 0, gewinner, 0.0, "ok"),
             Zuordnung(_stempel(16.0), 1, verlierer, 0.0, "ok"),
             Zuordnung(_stempel(16.0), 2, frei, 0.0, "ok")]
    quelle = {"raum_1": "L", "raum_2": "F", "raum_3": "L"}
    return raeume, [], zuord, quelle


def test_kaskade_adapter_entfall():
    raeume, rest, zuord, quelle = _kaskade_fall()
    verlierer = raeume[1]
    entfallen = bereinige_kaskade(raeume, rest, zuord, quelle)

    assert [r.id for r in raeume] == ["raum_1", "raum_3"]
    assert len(entfallen) == 1
    raum, stempel = entfallen[0]
    assert raum is verlierer and stempel is not None
    assert stempel.flaeche_m2 == pytest.approx(16.0)
    # Zuordnung des entfallenen Raums ist kein_polygon, Objekt behält die Belege.
    assert zuord[1].raum is None and zuord[1].flag == "kein_polygon"
    assert zuord[1].polygon_index is None
    assert raum.polygon_mm == [] and raum.polygon_roh
    assert [e.regel for e in raum.bereinigung][-1] == "ENTFALL"
    # polygon_index NEU vergeben — restflaechen() filtert über diese Positionen.
    for z in zuord:
        if z.raum is not None:
            assert raeume[z.polygon_index] is z.raum
    assert zuord[0].polygon_index == 0 and zuord[2].polygon_index == 1


def test_nicht_destruktiv():
    raeume, rest, zuord, quelle = _kaskade_fall()
    gewinner, verlierer = raeume[0], raeume[1]
    roh_gewinner = list(gewinner.polygon_mm)
    roh_verlierer = list(verlierer.polygon_mm)
    # bereinige() selbst mutiert nichts.
    bereinige(raeume, quelle, {"raum_1": 15.2})
    assert gewinner.polygon_mm == roh_gewinner and gewinner.polygon_roh == []
    assert verlierer.polygon_mm == roh_verlierer and verlierer.bereinigung == []
    # Der Adapter schreibt den Roh-Ring fort, statt ihn zu überschreiben.
    bereinige_kaskade(raeume, rest, zuord, quelle)
    assert verlierer.polygon_roh == roh_verlierer
    assert gewinner.polygon_roh == []              # Gewinner unverändert
    assert gewinner.polygon_mm == roh_gewinner


# -------------------------------------------------- Determinismus/Parameter

def test_determinismus():
    raeume = [_raum("a", _rect(0, 0, 6000, 6000)),
              _raum("b", _rect(4000, 0, 10000, 6000)),
              _raum("c", _rect(2000, 2000, 8000, 8000))]
    quelle = {"a": "F", "b": "H", "c": "L"}
    stempel = {"c": 36.0}
    vor = bereinige(raeume, quelle, stempel)
    rueck = bereinige(list(reversed(raeume)), quelle, stempel)
    assert {k: v.polygon_mm for k, v in vor.items()} == \
           {k: v.polygon_mm for k, v in rueck.items()}
    assert {k: _regeln(v) for k, v in vor.items()} == \
           {k: _regeln(v) for k, v in rueck.items()}


def test_regeln_parameter_schaltet_regeln_ab():
    raeume = [_raum("a", _rect(0, 0, 10000, 10000), "ZIMMER"),
              _raum("b", _rect(9000, 4000, 11000, 6000), "LIFT"),
              _raum("c", _rect(2000, 2000, 4000, 4000), "WC")]
    quelle = {"a": "L", "b": "R", "c": "F"}
    leer = bereinige(raeume, quelle, {}, regeln=frozenset())
    assert all(v.eintraege == [] for v in leer.values())
    nur1 = bereinige(raeume, quelle, {}, regeln=frozenset({1}))
    assert _regeln(nur1["a"]) == ["LIFT_SCHACHT"]      # Regel 2 (c) bleibt offen
    bis2 = bereinige(raeume, quelle, {}, regeln=frozenset({1, 2}))
    assert set(_regeln(bis2["a"])) >= {"LIFT_SCHACHT", "ENTHALTENSEIN"}


# ---------------------------------------------------------- Contract/Invarianten

def test_contract_rundreise():
    raum = _raum("a", _rect(0, 0, 4000, 4000))
    raum.polygon_roh = list(raum.polygon_mm)
    raum.bereinigung = [Bereinigung(regel="ZERFALL", gegenspieler=None, flaeche_m2=1.5),
                        Bereinigung(regel="QUELLE_RANG", gegenspieler="b", flaeche_m2=2.0)]
    rund = Raum.model_validate(raum.model_dump())
    assert rund.polygon_roh == raum.polygon_roh
    assert [e.regel for e in rund.bereinigung] == ["ZERFALL", "QUELLE_RANG"]
    assert rund.bereinigung[1].gegenspieler == "b"
    # Default: leer = unverändert.
    assert Raum(id="x", raum_typ="").polygon_roh == []
    assert Raum(id="x", raum_typ="").bereinigung == []
    with pytest.raises(ValidationError):
        Bereinigung(regel="ERFUNDEN", gegenspieler=None, flaeche_m2=1.0)


def test_flaechenbuchhaltung_geht_auf():
    """Jeder Raum: roh − bereinigt == Σ Buchungen, Entfall eingeschlossen."""
    # Drei räumlich getrennte Konstellationen, damit je Raum genau der gewollte
    # Posten entsteht (Zerfall / Entfall / Schlitz).
    raeume = [
        _raum("a", _rect(0, 0, 10000, 4000)),                  # verliert + zerfällt
        _raum("b", _rect(3000, -1000, 5000, 5000)),            # Gewinner (Balken)
        _raum("c", _rect(0, 20000, 4000, 24000)),              # entfällt
        _raum("d", _rect(0, 20000, 4000, 23800)),              # Gewinner über c
        _raum("e", _rect(20000, 0, 30000, 10000)),             # bekommt ein Loch
        _raum("f", _rect(24000, 4000, 26000, 6000)),           # Loch in e
    ]
    quelle = {"a": "F", "b": "L", "c": "F", "d": "L", "e": "L", "f": "F"}
    stempel = {"b": 12.0, "d": 15.2, "e": 100.0}
    erg = bereinige(raeume, quelle, stempel)
    _buchhaltung_haelt(raeume, erg)
    assert erg["c"].entfallen and "ENTFALL" in _regeln(erg["c"])
    assert "ZERFALL" in _regeln(erg["a"])
    assert "SCHLITZ" in _regeln(erg["e"])
    # Entfall bucht den Restkörper — sonst fällt die Fläche aus der Bilanz.
    assert sum(e.flaeche_m2 for e in erg["c"].eintraege) == pytest.approx(16.0)


def test_kein_restpaar_ueber_rauschschwelle():
    """Dreieckskonstellation: A verliert an C, B gegen A — danach kein Paar > 1 mm²."""
    raeume = [_raum("a", _rect(0, 0, 6000, 6000)),
              _raum("b", _rect(4000, 0, 10000, 6000)),
              _raum("c", _rect(2000, 2000, 8000, 8000))]
    quelle = {"a": "F", "b": "H", "c": "L"}
    erg = bereinige(raeume, quelle, {"c": 36.0})
    ringe = [erg[r.id].polygon_mm for r in raeume]
    ueber, doppelt = ueberlappung(ringe)
    assert ueber == set(), f"verbleibende Überlapper: {ueber}"
    assert doppelt <= RAUSCH_MM2, f"{doppelt:.4f} mm² doppelt belegt"
    _buchhaltung_haelt(raeume, erg)


def test_abbruch_killt_den_lauf_nicht(monkeypatch):
    """Schlägt die Loch-Kodierung fehl, bleibt der Raum beim Roh-Ring — kein Wurf."""
    def boom(*args, **kwargs):
        raise RuntimeError("GEOS-TopologyException (simuliert)")

    monkeypatch.setattr(bm.shapely, "shortest_line", boom)
    gross = _raum("raum_1", _rect(0, 0, 20000, 20000))
    klein = _raum("raum_2", _rect(8000, 8000, 12000, 12000))
    roh = list(gross.polygon_mm)

    erg = bereinige([gross, klein], {"raum_1": "L", "raum_2": "F"}, {})
    assert erg["raum_1"].eintraege == []           # Bereinigung verworfen
    assert Polygon(erg["raum_1"].polygon_mm).area == pytest.approx(400e6)

    zuord = [Zuordnung(_stempel(400.0), 0, gross, 0.0, "ok"),
             Zuordnung(_stempel(16.0), 1, klein, 0.0, "ok")]
    raeume = [gross, klein]
    entfallen = bereinige_kaskade(raeume, [], zuord,
                                  {"raum_1": "L", "raum_2": "F"})
    assert entfallen == []
    assert gross.polygon_mm == roh and gross.polygon_roh == []
    assert gross.bereinigung == []


def test_ueberlappung_misst_wie_der_riegel():
    """§ 14.1-Definitionen: Verhältnis je Seite, Rauschschwelle, < 3 Punkte zählen nicht."""
    ringe = [_rect(0, 0, 10000, 10000),      # 0: beide Seiten reißen 5 %
             _rect(9000, 0, 19000, 10000),   # 1: Überlappung 10 m² = 10 %
             _rect(50000, 0, 51000, 100),    # 2: allein
             [(0.0, 0.0), (1.0, 1.0)]]       # 3: < 3 Punkte = kein Raum
    ueber, doppelt = ueberlappung(ringe)
    assert ueber == {0, 1}
    assert doppelt == pytest.approx(10e6)
    # Unter der Schwelle zählt kein Index, die Fläche aber weiter.
    ueber, doppelt = ueberlappung(ringe, schwelle=0.5)
    assert ueber == set() and doppelt == pytest.approx(10e6)
