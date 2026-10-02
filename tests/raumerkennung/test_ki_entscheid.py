"""KI-Zweitmeinung Teil B (Abschnitt 3, Entscheid 3) — Anfrage, Entscheidungsregeln, Herkunft, Verdrahtung.

Alles mit synthetischen oder gespeicherten Antworten (``tests/fixtures/ki/``); kein Test ruft
die KI live auf. „Erscheinungsbild ist Wahrheit, KI ist zweite Meinung" (Auftrag § 3).
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import ezdxf
import pytest
from shapely.geometry import Polygon

from notbeleuchtung.hauptengine.contracts.raum_modell import Raum
from notbeleuchtung.raumerkennung import ArchitekturRaumProvider
from notbeleuchtung.raumerkennung.ki_anfrage import (
    QUADRANT_AB_MM,
    baue_anfragen,
    belege_je_raum,
    quadranten,
    rendere_bilder,
)
from notbeleuchtung.raumerkennung.ki_backends import CodexAboBackend
from notbeleuchtung.raumerkennung.ki_zweitmeinung import (
    FREIGABE,
    SICHERHEIT_MIN,
    UNBESTIMMT,
    Antwort,
    GeschossAnfrage,
    Herkunft,
    KiFehler,
    KiKonfig,
    RaumAnfrage,
    RaumAntwort,
    parse_antwort,
    verliert_notlicht,
    zweitmeinung_anwenden,
)
from notbeleuchtung.raumerkennung.sanitaer import moebelklasse

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "ki"
SECHS = json.loads((FIXTURES / "amrain_6_ohne_stempel.json").read_text(encoding="utf-8"))
LIMIT_JSONL = (FIXTURES / "codex_limit.jsonl").read_text(encoding="utf-8")
ANTWORT_JSONL = (FIXTURES / "codex_antwort_synth.jsonl").read_text(encoding="utf-8")


# --- Hilfen -------------------------------------------------------------------------------

def _quadrat(flaeche_m2: float, x0: float = 0.0, y0: float = 0.0) -> list[tuple[float, float]]:
    s = (flaeche_m2 * 1e6) ** 0.5
    return [(x0, y0), (x0 + s, y0), (x0 + s, y0 + s), (x0, y0 + s)]


def _raum(rid: str, typ: str = "", m2: float = 10.0, **felder) -> Raum:
    r = Raum(id=rid, raum_typ=typ, polygon_mm=_quadrat(m2), flaeche_m2=m2, **felder)
    if typ:
        from notbeleuchtung.raumerkennung.nutzungsklasse import nutzungsklasse_fuer
        from notbeleuchtung.raumerkennung.raumtyp import raumtyp_flags
        tf = raumtyp_flags(typ)
        if tf:
            r.ist_fluchtweg, r.ist_communal = tf[1], tf[2]
        r.nutzungsklasse = nutzungsklasse_fuer(typ)
    return r


def _anfrage(tmp_path: Path, raeume: list[Raum], belege: dict[str, str] | None = None,
             geschoss: str = "EG") -> GeschossAnfrage:
    dxf = tmp_path / "plan.dxf"
    if not dxf.exists():
        dxf.write_bytes(b"0\nSECTION\n0\nEOF\n")
    belege = belege or {}
    return GeschossAnfrage(plan_datei=dxf, geschoss=geschoss, raeume=tuple(
        RaumAnfrage(r.id, r.raum_typ, belege.get(r.id, "stempel" if r.raum_typ else ""),
                    {"flaeche_m2": r.flaeche_m2}) for r in raeume))


def _antwort(*raeume: tuple) -> Antwort:
    return Antwort(raeume=[RaumAntwort(*r) for r in raeume], quelle="backend", modell="mock")


def _zustand(r: Raum) -> tuple:
    return (r.raum_typ, r.ist_fluchtweg, r.ist_communal, r.nutzungsklasse, r.wohnung_id)


# --- (ii) Kürzel vs. KI: Kürzel bleibt, strittig -----------------------------------------

def test_kuerzel_bleibt_bei_widerspruch_raum_ist_strittig(tmp_path):
    ar = _raum("rest_3", "ABSTELLRAUM", 3.4)
    vorher = _zustand(ar)
    anfrage = _anfrage(tmp_path, [ar], {"rest_3": "kuerzel"})
    herkunft = zweitmeinung_anwenden(
        [ar], anfrage, _antwort(("rest_3", "WC", 0.95, False, "WC und Waschbecken gezeichnet")),
        freigabe=frozenset({"WC"}))
    assert _zustand(ar) == vorher, "Engine-Typ mit Kürzel-Beleg bleibt"
    (h,) = herkunft
    assert h.herkunft == "strittig" and h.engine_typ == "ABSTELLRAUM" and h.ki_typ == "WC"
    assert h.beleg == "kuerzel" and "Kürzel" in h.grund or "kuerzel" in h.grund
    assert "WC und Waschbecken" in h.grund, "beide Begründungen im Bericht"


def test_stempel_und_erscheinungsbild_bleiben_ebenfalls(tmp_path):
    st = _raum("raum_1", "STIEGENHAUS", 30.0)
    bad = _raum("rest_9", "BAD", 5.0)
    anfrage = _anfrage(tmp_path, [st, bad], {"raum_1": "stempel", "rest_9": "erscheinungsbild"})
    herkunft = zweitmeinung_anwenden(
        [st, bad], anfrage,
        _antwort(("raum_1", "GANG", 0.99, False, "sieht aus wie Gang"),
                 ("rest_9", "ABSTELLRAUM", 0.99, False, "kein Sanitär zu sehen")),
        freigabe=frozenset({"GANG", "ABSTELLRAUM"}))
    assert st.raum_typ == "STIEGENHAUS" and bad.raum_typ == "BAD"
    assert [h.herkunft for h in herkunft] == ["strittig", "strittig"]


def test_uebereinstimmung_ist_bestaetigt_enthaltung_ist_engine(tmp_path):
    st = _raum("raum_1", "STIEGENHAUS", 30.0)
    gang = _raum("raum_2", "GANG", 12.0)
    anfrage = _anfrage(tmp_path, [st, gang])
    herkunft = zweitmeinung_anwenden(
        [st, gang], anfrage,
        _antwort(("raum_1", "STIEGENHAUS", 0.9, True, "Treppenlauf"),
                 ("raum_2", UNBESTIMMT, 0.3, False, "nicht erkennbar")))
    assert [(h.herkunft, h.raum_id) for h in herkunft] == [("bestätigt", "raum_1"),
                                                            ("Engine", "raum_2")]
    assert "enthält sich" in herkunft[1].grund or "UNBESTIMMT" in herkunft[1].grund


# --- (iii) Notlicht-Verlust nur mit bestätigender Regel -----------------------------------

def test_notlicht_verlust_typen_sind_privat_mit_flags_00():
    assert verliert_notlicht("SCHLAFZIMMER") and verliert_notlicht("BAD") and verliert_notlicht("WC")
    assert verliert_notlicht("ABSTELLRAUM") and verliert_notlicht("KÜCHE")
    assert not verliert_notlicht("VORRAUM"), "PRIVAT, aber Flags 11 — kein Verlust"
    assert not verliert_notlicht("GANG") and not verliert_notlicht("STIEGENHAUS")
    assert not verliert_notlicht("BALKON") and not verliert_notlicht("SCHACHT")


def test_unbestimmt_bleibt_mit_notlicht_ohne_bestaetigende_regel(tmp_path):
    r = _raum("frei_2", "", 14.0)
    anfrage = _anfrage(tmp_path, [r])
    herkunft = zweitmeinung_anwenden(
        [r], anfrage, _antwort(("frei_2", "SCHLAFZIMMER", 0.95, False, "Doppelbett, Schrank")),
        freigabe=frozenset({"SCHLAFZIMMER"}))
    assert r.raum_typ == "" and r.nutzungsklasse is None, "UNBESTIMMT mit Notlicht"
    (h,) = herkunft
    assert h.herkunft == "Engine" and h.ki_typ == "SCHLAFZIMMER"
    assert "Notlicht" in h.grund and "Regel" in h.grund


def test_bestaetigende_regel_erlaubt_uebernahme_mit_notlicht_verlust(tmp_path):
    r = _raum("frei_2", "", 5.0)
    anfrage = _anfrage(tmp_path, [r])
    herkunft = zweitmeinung_anwenden(
        [r], anfrage, _antwort(("frei_2", "BAD", 0.9, False, "Wanne und Waschbecken")),
        freigabe=frozenset({"BAD"}),
        regel_bestaetigt=lambda raum, typ: typ == "BAD")   # z. B. K3-Sanitärbeleg
    assert r.raum_typ == "BAD" and r.nutzungsklasse == "WOHNUNG_PRIVAT"
    assert (r.ist_fluchtweg, r.ist_communal) == (False, False) and r.wohnung_id is None
    assert herkunft[0].herkunft == "KI" and "Regel" in herkunft[0].grund


# --- unbelegt → KI-Typ ab 0,8, Freigabeliste, Geometrie ----------------------------------

def test_freigabeliste_heute_leer_ki_uebernimmt_nichts(tmp_path):
    assert FREIGABE == frozenset() and SICHERHEIT_MIN == 0.8
    r = _raum("frei_1", "", 4.0)
    anfrage = _anfrage(tmp_path, [r])
    herkunft = zweitmeinung_anwenden(
        [r], anfrage, _antwort(("frei_1", "VORRAUM", 0.95, False, "Garderobe, Wohnungstür")))
    assert r.raum_typ == ""
    (h,) = herkunft
    assert h.herkunft == "Engine" and h.ki_typ == "VORRAUM" and h.sicherheit == 0.95
    assert "nicht freigegeben" in h.grund


def test_freigegebener_typ_ohne_notlicht_verlust_wird_uebernommen(tmp_path):
    r = _raum("frei_1", "", 4.0)
    anfrage = _anfrage(tmp_path, [r])
    herkunft = zweitmeinung_anwenden(
        [r], anfrage, _antwort(("frei_1", "VORRAUM", 0.95, False, "Garderobe, Wohnungstür")),
        freigabe=frozenset({"VORRAUM"}))
    assert _zustand(r) == ("VORRAUM", True, True, "WOHNUNG_PRIVAT", None)
    assert herkunft[0].herkunft == "KI"


def test_sicherheit_unter_schwelle_und_geometrie_widerspruch(tmp_path):
    klein, gross = _raum("a", "", 4.0), _raum("b", "", 60.0)
    anfrage = _anfrage(tmp_path, [klein, gross])
    herkunft = zweitmeinung_anwenden(
        [klein, gross], anfrage,
        _antwort(("a", "VORRAUM", 0.79, False, "vielleicht"),
                 ("b", "WC", 0.99, False, "WC-Symbol")),       # 60 m² WC ist nicht plausibel
        freigabe=frozenset({"VORRAUM", "WC"}))
    assert klein.raum_typ == "" and gross.raum_typ == ""
    assert "0,79" in herkunft[0].grund or "0.79" in herkunft[0].grund
    assert "Geometrie" in herkunft[1].grund or "Fläche" in herkunft[1].grund


def test_kein_raum_typen_nur_mit_lift_oder_schacht_evidenz(tmp_path):
    r = _raum("rest_4", "", 1.2)
    anfrage = _anfrage(tmp_path, [r])
    ant = _antwort(("rest_4", "SCHACHT", 0.95, False, "schwarz gefüllt"))
    zweitmeinung_anwenden([r], anfrage, ant, freigabe=frozenset({"SCHACHT"}))
    assert r.raum_typ == "", "ohne Evidenz kein KEIN_RAUM"
    herkunft = zweitmeinung_anwenden([r], anfrage, ant, freigabe=frozenset({"SCHACHT"}),
                                     evidenz=lambda raum, typ: "")
    assert r.raum_typ == "SCHACHT" and r.nutzungsklasse == "KEIN_RAUM"
    assert herkunft[0].herkunft == "KI"


def test_stempel_ohne_kanon_typ_wird_nie_umtypisiert(tmp_path):
    r = _raum("raum_7", "", 40.0)                    # Stempel „GESCHÄFTSLOKAL" (Vokabular, Enis)
    anfrage = _anfrage(tmp_path, [r], {"raum_7": "stempel"})
    herkunft = zweitmeinung_anwenden(
        [r], anfrage, _antwort(("raum_7", "LAGER", 0.95, False, "Regale")),
        freigabe=frozenset({"LAGER"}))
    assert r.raum_typ == "" and herkunft[0].herkunft == "Engine" and "Stempel" in herkunft[0].grund


def test_eichung_belege_bleiben_fuer_herkunft_und_stempelschutz(tmp_path):
    """Review 2: in der Eichung (``stempel_abdecken``) trägt die Anfrage keinen Beleg — die
    echten Belege kommen über ``belege`` mit: Herkunft zeigt sie, der Stempel-Schutz greift,
    der Vergleich läuft gegen den echten Engine-Typ (Rückfall ``raum.raum_typ``)."""
    vok = _raum("raum_7", "", 40.0)                 # Stempel „GESCHÄFTSLOKAL" (Vokabular)
    st = _raum("raum_1", "STIEGENHAUS", 30.0)
    anfrage = GeschossAnfrage(plan_datei=tmp_path / "p.dxf", geschoss="EG", raeume=(
        RaumAnfrage("raum_7", "", "", {}), RaumAnfrage("raum_1", "", "", {})))   # wie Eichung
    herkunft = zweitmeinung_anwenden(
        [vok, st], anfrage,
        _antwort(("raum_7", "LAGER", 0.95, False, "Regale"), ("raum_1", "GANG", 0.9, False, "lang")),
        freigabe=frozenset({"LAGER", "GANG"}), belege={"raum_7": "stempel", "raum_1": "stempel"})
    assert vok.raum_typ == "" and st.raum_typ == "STIEGENHAUS"
    assert [(h.herkunft, h.beleg, h.engine_typ) for h in herkunft] == [
        ("Engine", "stempel", ""), ("strittig", "stempel", "STIEGENHAUS")]
    assert "Stempel" in herkunft[0].grund


def test_fehler_oder_verworfen_laesst_alles_unveraendert(tmp_path):
    a, b = _raum("a", "GANG", 12.0), _raum("b", "", 5.0)
    anfrage = _anfrage(tmp_path, [a, b])
    vorher = [_zustand(a), _zustand(b)]
    herkunft = zweitmeinung_anwenden([a, b], anfrage, Antwort(
        fehler=KiFehler("limit", "You've hit your usage limit"), quelle="backend"))
    assert [_zustand(a), _zustand(b)] == vorher
    assert [h.herkunft for h in herkunft] == ["Engine", "Engine"]
    assert all("limit" in h.grund for h in herkunft)
    ant = Antwort(raeume=[], verworfen=["b: raum_typ 'BÜRO' außerhalb Kanon"], quelle="backend")
    herkunft = zweitmeinung_anwenden([a, b], anfrage, ant)
    assert "verworfen" in herkunft[1].grund and "BÜRO" in herkunft[1].grund


# --- (i) die 6 Räume ohne Stempel (Am Rain, § 22) mit gespeicherter Antwort --------------

def _faelle(tmp_path: Path):
    for fall in SECHS["faelle"]:
        raeume = [_raum(r["raum_id"], r["engine_typ"], r["flaeche_m2"]) for r in fall["raeume"]]
        anfrage = GeschossAnfrage(
            plan_datei=tmp_path / f"{fall['plan']}.dxf", geschoss=fall["geschoss"], raeume=tuple(
                RaumAnfrage(r["raum_id"], r["engine_typ"], r["beleg"],
                            {"flaeche_m2": r["flaeche_m2"], **r["merkmale"]})
                for r in fall["raeume"]))
        roh = json.dumps(fall["antwort"], ensure_ascii=False)
        geparst, verworfen, fehler = parse_antwort(roh, anfrage.raum_ids)
        assert fehler is None and not verworfen, (fall["plan"], verworfen)
        yield fall["plan"], raeume, anfrage, Antwort(raeume=geparst, roh=roh, quelle="cache")


def test_sechs_raeume_ohne_stempel_heute_nichts_uebernommen(tmp_path):
    ergebnis: dict[tuple[str, str], Herkunft] = {}
    for plan, raeume, anfrage, antwort in _faelle(tmp_path):
        vorher = {r.id: _zustand(r) for r in raeume}
        for h in zweitmeinung_anwenden(raeume, anfrage, antwort):   # FREIGABE leer
            ergebnis[(plan, h.raum_id)] = h
        assert {r.id: _zustand(r) for r in raeume} == vorher, plan
    assert len(ergebnis) == 6
    h = ergebnis[("AmRain_EG", "frei_3")]
    assert h.herkunft == "Engine" and h.ki_typ == "VORRAUM" and "nicht freigegeben" in h.grund
    h = ergebnis[("AmRain_EG", "frei_4")]
    assert h.herkunft == "Engine" and h.ki_typ == "ZIMMER" and "nicht freigegeben" in h.grund
    h = ergebnis[("AmRain_OG1", "frei_2")]
    assert h.herkunft == "Engine" and h.ki_typ == "STIEGENHAUS" and h.sicherheit == 0.7
    assert ergebnis[("AmRain_OG1", "frei_3")].herkunft == "bestätigt"
    assert ergebnis[("AmRain_OG2", "frei_1")].herkunft == "bestätigt"
    h = ergebnis[("AmRain_OG4", "frei_1")]
    assert h.herkunft == "Engine" and h.ki_typ == UNBESTIMMT and "Dachausstieg" in h.grund


def test_sechs_raeume_mit_freigabe_vorraum_ja_zimmer_nur_mit_regel(tmp_path):
    frei = frozenset({"VORRAUM", "ZIMMER", "STIEGENHAUS"})
    typen: dict[tuple[str, str], tuple] = {}
    gruende: dict[tuple[str, str], Herkunft] = {}
    for plan, raeume, anfrage, antwort in _faelle(tmp_path):
        for h in zweitmeinung_anwenden(raeume, anfrage, antwort, freigabe=frei):
            gruende[(plan, h.raum_id)] = h
        typen.update({(plan, r.id): _zustand(r) for r in raeume})
    # Vorraum-Stich: unbelegt, 0,85 ≥ 0,8, VORRAUM behält Notlicht (Flags 11) → übernommen
    assert typen[("AmRain_EG", "frei_3")] == ("VORRAUM", True, True, "WOHNUNG_PRIVAT", None)
    assert gruende[("AmRain_EG", "frei_3")].herkunft == "KI"
    # ZI 2: ZIMMER verliert Notlicht, keine bestehende Regel bestätigt → UNBESTIMMT mit Notlicht
    assert typen[("AmRain_EG", "frei_4")][0] == "" and typen[("AmRain_EG", "frei_4")][3] is None
    assert "Notlicht" in gruende[("AmRain_EG", "frei_4")].grund
    # wohnungsinterne Stiege: Sicherheit 0,7 < 0,8 → bleibt UNBEKANNT, Grund nennt die Schwelle
    assert typen[("AmRain_OG1", "frei_2")][0] == ""
    assert "0,8" in gruende[("AmRain_OG1", "frei_2")].grund
    # Dachausstieg: KI enthält sich → bleibt
    assert typen[("AmRain_OG4", "frei_1")][0] == ""


# --- Anfrage-Aufbau: Belege, Merkmale, Quadranten, Bild ------------------------------------

def test_belege_aus_zuordnung_hinweisen_und_befunden():
    from notbeleuchtung.raumerkennung.stempel_anker import Stempel, Zuordnung

    st = _raum("raum_1", "STIEGENHAUS"); ku = _raum("rest_2", "STIEGENHAUS")
    sa = _raum("rest_9", "BAD"); ge = _raum("rest_5", "SCHACHT"); fr = _raum("frei_1", "VORRAUM")
    un = _raum("frei_2", ""); vo = _raum("raum_7", "")
    stempel = Stempel("STGH 32.44 m²", "STIEGENHAUS", 32.44, None, (0, 0), "TEXT", "L")
    vokab = Stempel("GESCHÄFTSLOKAL 40 m²", None, 40.0, None, (0, 0), "TEXT", "L")
    zuord = [Zuordnung(stempel, 0, st, 1.0, "ok"), Zuordnung(vokab, 1, vo, 0.0, "ok")]
    hinweise = ["rest_2: Kürzel »STGH« im Polygon (Layer X) -> STIEGENHAUS (Entscheid 1, Owner 2026-10-01)"]
    sanitaer = ["rest_9: BAD aus Sanitärbeleg (WASCHBECKEN 1, WC 1) im Umriss top_1 (Probe) — …"]
    frei = [("freiflaeche: 3.92 m² bei (33.4, 19.9) m → neuer Raum frei_1 VORRAUM, im Umriss top_3; "
             "frei_1: Kürzel »VR« im Polygon -> VORRAUM (Entscheid 2: Stempel vor UNBEKANNT)"),
            "freiflaeche: 2.36 m² bei (23.4, 13.1) m → neuer Raum frei_2 UNBEKANNT, Tür mit Blatt trennt"]
    b = belege_je_raum([st, ku, sa, ge, fr, un, vo], zuord, hinweise, sanitaer, frei)
    assert b == {"raum_1": "stempel", "rest_2": "kuerzel", "rest_9": "erscheinungsbild",
                 "rest_5": "geometrie", "frei_1": "kuerzel", "frei_2": "", "raum_7": "stempel"}


def test_moebelklasse_blocknamen_der_pruefplaene():
    # Mollgasse 07_MOB / 07-SAN, Muthgasse I-FURN / A-GENM / P-SANR-FIXT, Rennweg New_06x Möbel
    assert moebelklasse("BETT_90", "07_MOB-G00-LEG-M0") == "BETT"
    assert moebelklasse("Doppelbett - Doppelbett 180x200-17321697-E 2", "I-FURN") == "BETT"
    assert moebelklasse("kochfeld", "07-SAN-G00-Leg-Küche") == "HERD"
    assert moebelklasse("Küche-Zeile klein_GSP 45_4 Kochfelder", "I-FURN") == "HERD"
    assert moebelklasse("Spüle", "07-SAN-G00-Leg-Küche") == "SPUELE"
    assert moebelklasse("ECKSOFA_240", "07_MOB-G00-LEG-M0") == "SOFA"
    assert moebelklasse("2D_sofa_38585[47]", "New_065 Möbel Einrichtung_Pen_No__31") == "SOFA"
    assert moebelklasse("Dining Table 01 27[55]", "New_065 Möbel Einrichtung") == "ESSTISCH"
    assert moebelklasse("tisch-4sessel_eng - tisch-4sessel_eng-V49-E 2", "I-FURN") == "ESSTISCH"
    assert moebelklasse("möbel_schreibtisch", "07_MOB-G00-LEG-M0") is None, "Schreibtisch ≠ Esstisch"
    assert moebelklasse("07-WM", "07-SAN-G00-LEG-M0") == "WASCHMASCHINE"
    assert moebelklasse("Waschmaschine - Waschmaschine-6522932-E 2", "A-GENM") == "WASCHMASCHINE"
    assert moebelklasse("07_Doppelparker_2_250x520", "02-PKW-G00-LKG-M0") == "AUTO"
    # Sanitär wie bisher (K3-Liste), Bewegungsflächen und Raumstempel-Blöcke nicht
    assert moebelklasse("07-WC", "07-SAN-G00-LEG-M0") == "WC"
    assert moebelklasse("07-Badewanne", "07-SAN-G00-LEG-M0") == "BADEWANNE"
    assert moebelklasse("2D_barrierefrei_WC 130x190 - r75", "A-GENM") is None
    assert moebelklasse("Bad_WC__3", "New_080 Raumdefinitionen") is None
    assert moebelklasse("Schrank variabel 25[43]", "New_065 Möbel Einrichtung") is None


def _drei_raeume_dxf(path: Path, *, sanitaer_in_mitte: bool = False) -> Path:
    """30 × 6 m, zwei Trennwände: links (60 m²) Stempel STIEGENHAUS, Mitte (18 m²) ohne
    Text, rechts (102 m²) Kürzel »AR« ohne Flächenzeile. Türen als Blöcke, kein 09-WEG."""
    doc = ezdxf.new(setup=True)
    doc.header["$INSUNITS"] = 4
    msp = doc.modelspace()
    for lyr in ("02-TWA-G00-LEG-M0", "05-SYM-G00-LEG-M0", "01-TXT-G00-LEG-M0", "07-SAN-G00-LEG-M0"):
        doc.layers.add(lyr)
    w = "02-TWA-G00-LEG-M0"
    ecken = [(0, 0), (30000, 0), (30000, 6000), (0, 6000)]
    for i in range(4):
        msp.add_line(ecken[i], ecken[(i + 1) % 4], dxfattribs={"layer": w})
    msp.add_line((10000, 0), (10000, 6000), dxfattribs={"layer": w})
    msp.add_line((13000, 0), (13000, 6000), dxfattribs={"layer": w})
    msp.add_mtext("STIEGENHAUS", dxfattribs={"layer": "01-TXT-G00-LEG-M0"}).set_location((5000, 3000))
    msp.add_text("AR", dxfattribs={"layer": "01-TXT-G00-LEG-M0", "height": 250}).set_placement((22000, 3000))
    doc.blocks.new("TÜR-80_10er-WAND")
    msp.add_blockref("TÜR-80_10er-WAND", (10000, 3000), dxfattribs={"layer": "05-SYM-G00-LEG-M0"})
    msp.add_blockref("TÜR-80_10er-WAND", (13000, 3000), dxfattribs={"layer": "05-SYM-G00-LEG-M0"})
    if sanitaer_in_mitte:
        for name, xy in (("07-WC", (10500, 1500)), ("07-WT", (11500, 1500)), ("07-Dusche_2", (12000, 4000))):
            blk = doc.blocks.new(name)
            blk.add_lwpolyline([(0, 0), (400, 0), (400, 600), (0, 600)], close=True)
            msp.add_blockref(name, xy, dxfattribs={"layer": "07-SAN-G00-LEG-M0"})
    doc.saveas(str(path))
    return path


class _Mock:
    name = "mock"

    def __init__(self, antwort: Antwort):
        self.antwort, self.anfragen = antwort, []

    def frage(self, anfrage, modell=None):
        self.anfragen.append(anfrage)
        return self.antwort


def _raeume_aus_plan(plan):
    """Wie `provider.parse`: Kaskade, sonst Wandzyklen + Stempel (Linien-DXF ohne Wandkörper)."""
    from notbeleuchtung.raumerkennung.kaskade import raeume_aus_kaskade
    from notbeleuchtung.raumerkennung.raumtyp import beschrifte_raeume
    from notbeleuchtung.raumerkennung.waende import raeume_aus_waenden

    return raeume_aus_kaskade(plan).alle_raeume or beschrifte_raeume(plan, raeume_aus_waenden(plan))


def test_anfrage_traegt_merkmale_je_raum_und_quadranten(tmp_path):
    from notbeleuchtung.raumerkennung.dxf_load import lade_dxf

    dxf = _drei_raeume_dxf(tmp_path / "drei.dxf", sanitaer_in_mitte=True)
    plan = lade_dxf(dxf)
    raeume = _raeume_aus_plan(plan)
    belege = {r.id: ("stempel" if r.raum_typ == "STIEGENHAUS" else "") for r in raeume}
    anfragen = baue_anfragen(plan, dxf, "EG", raeume, [], belege, bilder={"": tmp_path / "x.png"})
    assert len(anfragen) == 1 and anfragen[0].quadrant == "" and anfragen[0].bilder == (tmp_path / "x.png",)
    je = {r.raum_id: r for r in anfragen[0].raeume}
    assert set(je) == {r.id for r in raeume if len(r.polygon_mm) >= 3}
    st = next(r for r in je.values() if r.engine_typ == "STIEGENHAUS")
    assert st.beleg == "stempel" and "STIEGENHAUS" in st.merkmale["texte"]
    assert st.merkmale["flaeche_m2"] == pytest.approx(60.0, abs=1.0)
    mitte = next(r for r in je.values() if r.merkmale["objekte"])
    assert mitte.merkmale["objekte"] == {"DUSCHE": 1, "WASCHBECKEN": 1, "WC": 1}
    assert {"flaeche_m2", "texte", "objekte", "fenster", "stiegen", "lift", "tueren", "wohnung",
            "wohnungseingang_am_raum", "klasse", "nachbarn"} <= set(st.merkmale)
    assert any(n.startswith(mitte.raum_id) for n in st.merkmale["nachbarn"])
    # Eichung: Stempel abdecken → keine Texte in den Textdaten; Review 2: auch kein aus dem
    # Stempel abgeleiteter Engine-Typ/Beleg, keine Nachbar-Typen, keine Klasse — sonst misst
    # die Eichung nur, ob die KI abschreiben kann
    ohne = baue_anfragen(plan, dxf, "EG", raeume, [], belege, stempel_abdecken=True)
    assert all("texte" not in r.merkmale and "klasse" not in r.merkmale for r in ohne[0].raeume)
    assert all(r.engine_typ == "" and r.beleg == "" for r in ohne[0].raeume)
    assert all(" " not in n for r in ohne[0].raeume for n in r.merkmale["nachbarn"]), "nur IDs"
    assert {r.raum_id for r in ohne[0].raeume} == set(je)
    # Quadranten wie beim Vision-Audit: ab QUADRANT_AB_MM längster Seite, 1 m Überlappung
    polys = [Polygon(r.polygon_mm) for r in raeume if len(r.polygon_mm) >= 3]
    assert [q for q, _ in quadranten(polys)] == [""]
    gross = [Polygon([(0, 0), (QUADRANT_AB_MM + 1, 0), (QUADRANT_AB_MM + 1, 20000), (0, 20000)])]
    q = dict(quadranten(gross))
    assert set(q) == {"NW", "NO", "SW", "SO"}
    assert q["NW"][2] - q["NO"][0] == pytest.approx(1000.0) and q["SW"][3] - q["NW"][1] == pytest.approx(1000.0)


def test_bild_zeigt_raum_ids_und_stempel_abdecken_versteckt_texte(tmp_path):
    import numpy as np
    from matplotlib.image import imread

    from notbeleuchtung.raumerkennung.dxf_load import lade_dxf

    dxf = _drei_raeume_dxf(tmp_path / "drei.dxf")
    plan = lade_dxf(dxf)
    raeume = _raeume_aus_plan(plan)
    polys = [Polygon(r.polygon_mm) for r in raeume if len(r.polygon_mm) >= 3]
    q = quadranten(polys)
    mit = rendere_bilder(plan, raeume, tmp_path / "mit", q)
    ohne = rendere_bilder(plan, raeume, tmp_path / "ohne", q, stempel_abdecken=True)
    assert set(mit) == {""} and mit[""].suffix == ".png" and mit[""].is_file()
    a, b = imread(str(mit[""])), imread(str(ohne[""]))
    assert a.shape == b.shape and max(a.shape[:2]) >= 1200
    # ohne Stempeltexte ist weniger Tinte im Bild (die Raum-ID-Labels stehen in beiden)
    tinte = lambda img: int(np.sum(img[..., :3].min(axis=2) < 0.5))
    assert tinte(b) < tinte(a)
    # dasselbe Bild ohne Räume verrät, dass die Raum-Labels gezeichnet wurden
    leer = rendere_bilder(plan, [], tmp_path / "leer", q, stempel_abdecken=True)
    assert tinte(imread(str(leer[""]))) < tinte(b)


# --- Verdrahtung im Provider ---------------------------------------------------------------

def _parse(dxf: Path, konfig: KiKonfig | None = None, backend=None):
    prov = ArchitekturRaumProvider(ki_konfig=konfig, ki_backend=backend)
    return prov, prov.parse(str(dxf), "EG")


def test_provider_ohne_ki_laeuft_wie_bisher_und_weist_herkunft_aus(tmp_path):
    dxf = _drei_raeume_dxf(tmp_path / "drei.dxf")
    prov, modell = _parse(dxf, KiKonfig(an=False, cache_pfad=tmp_path / "c"))
    typen = {r.raum_typ for r in modell.raeume}
    assert typen == {"STIEGENHAUS", "", "ABSTELLRAUM"}, typen
    ki = prov.ki_ergebnis
    assert ki.an is False and ki.anfragen == 0 and ki.treffer == 0 and ki.warnungen == []
    assert {h.raum_id for h in ki.herkunft} == {r.id for r in modell.raeume}
    assert all(h.herkunft == "Engine" for h in ki.herkunft)
    belege = {h.engine_typ: h.beleg for h in ki.herkunft}
    # Linien-DXF ohne Wandkörper: Räume aus Wandzyklen, Typen von `beschrifte_raeume`
    # (jeder Wörterbuch-Text im Polygon zählt dort als Stempel, auch »AR«)
    assert belege == {"STIEGENHAUS": "stempel", "": "", "ABSTELLRAUM": "stempel"}
    assert not (tmp_path / "c").exists()


def test_provider_mit_ki_mock_bild_merkmale_herkunft_und_null_aenderung(tmp_path):
    dxf = _drei_raeume_dxf(tmp_path / "drei.dxf")
    _, ohne = _parse(dxf, KiKonfig(an=False, cache_pfad=tmp_path / "c0"))
    ids = {r.raum_typ: r.id for r in ohne.raeume}
    antwort = Antwort(raeume=[
        RaumAntwort(ids["STIEGENHAUS"], "STIEGENHAUS", 0.95, True, "Treppe und Stempel"),
        RaumAntwort(ids[""], "GANG", 0.9, False, "lang und schmal, zwei Türen"),
        RaumAntwort(ids["ABSTELLRAUM"], "WC", 0.9, False, "WC-Symbol"),
    ], roh=json.dumps({"raeume": []}))
    mock = _Mock(antwort)
    prov, mit = _parse(dxf, KiKonfig(an=True, cache_pfad=tmp_path / "c1"), mock)
    # Freigabeliste leer → das Modell ist mit und ohne KI identisch (0 Änderungen)
    assert mit.model_dump(by_alias=True) == ohne.model_dump(by_alias=True)
    assert len(mock.anfragen) == 1
    a = mock.anfragen[0]
    assert a.geschoss == "EG" and a.plan_datei == dxf and len(a.bilder) == 1
    assert a.bilder[0].suffix == ".png"
    assert {r.raum_id for r in a.raeume} == set(ids.values())
    ki = prov.ki_ergebnis
    assert ki.an and ki.anfragen == 1 and ki.treffer == 0 and ki.warnungen == []
    je = {h.raum_id: h for h in ki.herkunft}
    assert je[ids["STIEGENHAUS"]].herkunft == "bestätigt"
    assert je[ids[""]].herkunft == "Engine" and "nicht freigegeben" in je[ids[""]].grund
    assert je[ids["ABSTELLRAUM"]].herkunft == "strittig" and je[ids["ABSTELLRAUM"]].beleg == "stempel"
    # zweiter Lauf: Cache-Treffer, kein Aufruf, kein Bild nötig
    prov2, _ = _parse(dxf, KiKonfig(an=True, cache_pfad=tmp_path / "c1"), mock)
    assert len(mock.anfragen) == 1 and prov2.ki_ergebnis.treffer == 1 and prov2.ki_ergebnis.anfragen == 0


def test_provider_freigabe_bad_sanitaerregel_nur_im_wohnungsumriss(tmp_path):
    """Review 2: die bestätigende Regel ist K3 VOLLSTÄNDIG — Sanitärobjekte UND Umriss einer
    Wohnung (Owner-Regel sanitaer.py: „der Raum muss innerhalb eines Wohnungsumrisses liegen,
    sonst bleibt UNBEKANNT"). Die 3-Raum-DXF hat keine Wohnung → KI-BAD mit 3 Sanitärblöcken
    bleibt UNBESTIMMT mit Notlicht (Grundsatz (a))."""
    dxf = _drei_raeume_dxf(tmp_path / "drei.dxf", sanitaer_in_mitte=True)
    _, ohne = _parse(dxf, KiKonfig(an=False, cache_pfad=tmp_path / "c0"))
    mitte = next(r for r in ohne.raeume if r.raum_typ == "")   # K3 greift nicht: kein Wohnungsumriss
    mock = _Mock(Antwort(raeume=[RaumAntwort(mitte.id, "BAD", 0.9, False, "WC und Waschbecken")],
                         roh="{}"))
    prov, mit = _parse(dxf, KiKonfig(an=True, cache_pfad=tmp_path / "c1",
                                     freigabe=frozenset({"BAD"})), mock)
    neu = next(r for r in mit.raeume if r.id == mitte.id)
    assert neu.raum_typ == "" and neu.nutzungsklasse is None, "ohne Wohnungsumriss kein BAD"
    assert mit.model_dump(by_alias=True) == ohne.model_dump(by_alias=True)
    h = next(h for h in prov.ki_ergebnis.herkunft if h.raum_id == mitte.id)
    assert h.herkunft == "Engine" and h.ki_typ == "BAD" and "Notlicht" in h.grund
    # dieselbe Antwort ohne Sanitärobjekte: ebenso UNBESTIMMT mit Notlicht
    dxf2 = _drei_raeume_dxf(tmp_path / "drei2.dxf")
    mock2 = _Mock(Antwort(raeume=[RaumAntwort(mitte.id, "BAD", 0.9, False, "sieht nach Bad aus")],
                          roh="{}"))
    prov2, mit2 = _parse(dxf2, KiKonfig(an=True, cache_pfad=tmp_path / "c2",
                                        freigabe=frozenset({"BAD"})), mock2)
    assert next(r for r in mit2.raeume if r.id == mitte.id).raum_typ == ""
    h2 = next(h for h in prov2.ki_ergebnis.herkunft if h.raum_id == mitte.id)
    assert h2.herkunft == "Engine" and "Notlicht" in h2.grund


def test_sanitaerregel_bestaetigt_nur_objekte_und_wohnungsumriss(tmp_path):
    """Die Regel selbst: Objekte im Polygon ergeben den Typ UND der Raum liegt im Umriss einer
    Wohnung (Nachbarn bis 500 mm alle in einer Wohnung, keine Tür hinaus) → bestätigt; ohne
    Wohnung oder mit anderem Typ → nicht."""
    from notbeleuchtung.raumerkennung.dxf_load import lade_dxf
    from notbeleuchtung.raumerkennung.ki_anfrage import _sanitaer_regel

    plan = lade_dxf(_drei_raeume_dxf(tmp_path / "drei.dxf", sanitaer_in_mitte=True))
    raeume = _raeume_aus_plan(plan)
    mitte = next(r for r in raeume if r.raum_typ == "")
    regel = _sanitaer_regel(plan, raeume, [])
    assert not regel(mitte, "BAD"), "Nachbarn ohne Wohnung → K3-Kontrolle verneint"
    for r in raeume:
        if r.id != mitte.id:
            r.wohnung_id, r.nutzungsklasse = "top_1", "WOHNUNG_PRIVAT"
    assert regel(mitte, "BAD")
    assert not regel(mitte, "WC"), "3 Objekte sind BAD, nicht WC"
    herkunft = zweitmeinung_anwenden(
        raeume, _anfrage(tmp_path, [mitte]),
        _antwort((mitte.id, "BAD", 0.9, False, "Wanne, WC, Waschbecken")),
        freigabe=frozenset({"BAD"}), regel_bestaetigt=regel)
    assert mitte.raum_typ == "BAD" and herkunft[0].herkunft == "KI"


# --- (iv) Backend codex_abo mit gespeicherten Antworten -----------------------------------

class _Lauf:
    """``aufrufe`` = nur ``codex exec``; ``codex login status`` (Abo-Regel) → ``status``."""

    def __init__(self, stdout: str, returncode: int = 0):
        self.stdout, self.returncode, self.aufrufe, self.status = stdout, returncode, [], []

    def __call__(self, args, **kw):
        if list(args[1:3]) == ["login", "status"]:
            self.status.append((list(args), kw))
            return subprocess.CompletedProcess(args, 0, "", "Logged in using ChatGPT\n")
        self.aufrufe.append((list(args), kw))
        return subprocess.CompletedProcess(args, self.returncode, self.stdout, "")


def _codex(tmp_path: Path, lauf: _Lauf, **konfig) -> tuple[KiKonfig, CodexAboBackend]:
    exe = tmp_path / "bin" / "codex.exe"
    exe.parent.mkdir(exist_ok=True)
    exe.write_bytes(b"MZ")
    k = KiKonfig(an=True, codex_binary=str(exe), cache_pfad=tmp_path / "cache", **konfig)
    return k, CodexAboBackend(k, run=lauf)


def test_codex_antwort_fixture_wird_zugeordnet(tmp_path):
    dxf = _drei_raeume_dxf(tmp_path / "drei.dxf")
    lauf = _Lauf(ANTWORT_JSONL)
    konfig, backend = _codex(tmp_path, lauf)
    prov, modell = _parse(dxf, konfig, backend)
    assert len(lauf.aufrufe) == 1
    args, kw = lauf.aufrufe[0]
    assert args[1] == "exec" and args[-1] == "-" and any(a.startswith("--image=") for a in args)
    assert "OPENAI_API_KEY" not in kw["env"]
    ki = prov.ki_ergebnis
    assert ki.anfragen == 1 and ki.warnungen == []
    je = {h.engine_typ: h for h in ki.herkunft}
    assert je["STIEGENHAUS"].herkunft == "bestätigt"
    assert je["ABSTELLRAUM"].herkunft == "strittig" and je["ABSTELLRAUM"].ki_typ == "WC"
    assert je[""].herkunft == "Engine" and je[""].ki_typ == "GANG" and "nicht freigegeben" in je[""].grund
    assert {r.raum_typ for r in modell.raeume} == {"STIEGENHAUS", "", "ABSTELLRAUM"}
    assert list((tmp_path / "cache").rglob("*.json")), "gültige Antwort wird gecacht"


def test_codex_limit_fixture_warnung_kein_abbruch_raeume_unveraendert(tmp_path):
    dxf = _drei_raeume_dxf(tmp_path / "drei.dxf")
    _, ohne = _parse(dxf, KiKonfig(an=False, cache_pfad=tmp_path / "c0"))
    lauf = _Lauf(LIMIT_JSONL, returncode=1)
    konfig, backend = _codex(tmp_path, lauf)
    prov, mit = _parse(dxf, konfig, backend)
    assert mit.model_dump(by_alias=True) == ohne.model_dump(by_alias=True)
    ki = prov.ki_ergebnis
    assert len(ki.warnungen) == 1
    assert ki.warnungen[0].startswith("ki: Abo-Kontingent erschöpft — warten (Owner-Regel nur Abo)")
    assert "Engine-Ergebnis bleibt unverändert" in ki.warnungen[0]
    assert len(lauf.aufrufe) == 1, "Limit gilt kontoweit: kein Fallback-Aufruf"
    assert len(lauf.status) == 1, "Login-Status einmal vor dem ersten exec"
    assert all(h.herkunft == "Engine" and "limit" in h.grund for h in ki.herkunft)
    assert not list((tmp_path / "cache").rglob("*.json")), "Fehler werden nie gecacht"


def test_plan_pruefen_schreibt_raumtyp_herkunft_in_bericht(tmp_path, monkeypatch):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
    import plan_pruefen as pp

    monkeypatch.setattr(pp, "ERGEBNIS", tmp_path / "ergebnis")
    monkeypatch.delenv("NOTBEL_KI", raising=False)
    dxf = _drei_raeume_dxf(tmp_path / "drei.dxf")
    pp.plan_pruefen(dxf)
    bericht = (tmp_path / "ergebnis" / "drei" / "bericht.md").read_text(encoding="utf-8")
    assert "## Raumtyp-Herkunft" in bericht
    abschnitt = bericht.split("## Raumtyp-Herkunft", 1)[1].split("\n## ", 1)[0]
    assert "KI aus" in abschnitt and "Anfragen 0" in abschnitt and "Cache-Treffer 0" in abschnitt
    assert "| STIEGENHAUS | Engine | stempel |" in abschnitt
    assert "| ABSTELLRAUM | Engine | stempel |" in abschnitt


def test_ki_md_fuehrt_raeume_nach_der_zweiten_meinung_mit(tmp_path):
    """Review 2: Räume, die erst nach der zweiten Meinung entstehen (LIFT aus `finde_lifte`,
    Rennweg OG3 `lift_1`), bekommen eine Herkunftszeile „Engine" — Herkunft je Raum heißt
    jeder Raum des Modells."""
    from notbeleuchtung.raumerkennung.ki_anfrage import KiErgebnis

    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
    import plan_pruefen as pp

    ki = KiErgebnis(herkunft=[Herkunft("raum_1", "Engine", "STIEGENHAUS", "stempel", grund="KI aus")])
    lift = _raum("lift_1", "LIFT", 3.0)
    md = "\n".join(pp._ki_md(ki, [_raum("raum_1", "STIEGENHAUS", 30.0), lift]))
    assert "| raum_1 | STIEGENHAUS | Engine | stempel |" in md
    assert "| lift_1 | LIFT | Engine | geometrie |" in md and "nach der zweiten Meinung" in md
    assert "Engine 2" in md
