"""S3 — raumtyp: Stempel → raum_typ + Flags (Point-in-Polygon)."""
from __future__ import annotations

import pytest

from notbeleuchtung.raumerkennung.dxf_load import lade_dxf
from notbeleuchtung.raumerkennung.raumtyp import beschrifte_raeume, raumtyp_flags
from notbeleuchtung.raumerkennung.waende import raeume_aus_waenden


def test_synth_stiegenhaus_zugeordnet(synth_dxf):
    plan = lade_dxf(synth_dxf)
    raeume = beschrifte_raeume(plan, raeume_aus_waenden(plan))
    stgh = [r for r in raeume if r.raum_typ == "STIEGENHAUS"]
    assert len(stgh) == 1                    # Stempel im linken Raum
    assert stgh[0].ist_fluchtweg is True
    assert stgh[0].ist_communal is True
    # rechter Raum hat keinen Stempel → leer
    assert any(r.raum_typ == "" for r in raeume)


@pytest.mark.parametrize(
    "label, erwartet, flucht",
    [
        ("VR", "VORRAUM", True),            # Vorraum-Abkürzung (Fischamender)
        ("AR", "ABSTELLRAUM", False),       # Abstellraum-Abkürzung
        ("TRH BT1 EG", "STIEGENHAUS", True),  # Treppenhaus — sicherheitskritisch
        ("Loggia", "BALKON", False),
    ],
)
def test_oesterr_abkuerzungen_token_exakt(label, erwartet, flucht):
    tf = raumtyp_flags(label)
    assert tf is not None, f"{label!r} sollte typisieren"
    assert tf[0] == erwartet
    assert tf[1] is flucht


@pytest.mark.parametrize("label", ["Garten", "Rasen", "Parkett", "Fahrräder", "Rampe"])
def test_abkuerzung_kein_substring_bleed(label):
    # „ar"/„vr" dürfen NICHT als Substring in Fremdwörtern (Garten, Fahrräder) greifen.
    assert raumtyp_flags(label) is None


@pytest.mark.parametrize(
    "label, erwartet, flucht, communal",
    [
        ("Fahrradraum", "ABSTELLRAUM", False, False),      # Fahrrad-/Kinderwagenraum
        ("FAHRRADRAUM", "ABSTELLRAUM", False, False),
        ("Fahrrad", "ABSTELLRAUM", False, False),
        ("Kinderwagenraum", "ABSTELLRAUM", False, False),
        ("Kinderwagen", "ABSTELLRAUM", False, False),
        ("Keller", "KELLER", False, True),
        ("Kellerabteil", "KELLER", False, True),
        ("KELLERABTEIL BT1", "KELLER", False, True),
    ],
)
def test_nebenraeume_vokabular(label, erwartet, flucht, communal):
    # Nebenraum-Vokabular: Fahrrad/Kinderwagen → ABSTELLRAUM, Keller(abteil) → KELLER.
    tf = raumtyp_flags(label)
    assert tf is not None, f"{label!r} sollte typisieren"
    assert tf[0] == erwartet
    assert tf[1] is flucht
    assert tf[2] is communal


@pytest.mark.parametrize("label", ["Luftraum", "Kellerdecke", "Fahrräder"])
def test_nebenraeume_kein_bleed(label):
    # Token-exakt: „fahrräder"≠„fahrrad", „kellerdecke"≠„keller", „luftraum" ist kein
    # Keller — dürfen NICHT fälschlich typisieren.
    assert raumtyp_flags(label) is None


@pytest.mark.parametrize(
    "label",
    ["Zugang", "Ausgang", "Übergang", "Eingangstür", "Wohnungseingangstür",
     "Hauseingang", "Zugang Müll", "Terrassentür", "Terrassentrennwand"],
)
def test_classify_room_kein_gang_bleed(label):
    # „gang" in Ein/Zu/Aus-gang und „terrasse" in Terrassentür dürfen NICHT als
    # CORRIDOR/TERRACE fehltypisieren (CORRIDOR=Fluchtweg → sonst falsches Notlicht).
    tf = raumtyp_flags(label)
    assert tf is None or tf[0] not in ("GANG", "TERRASSE")


@pytest.mark.parametrize(
    "label, erwartet, communal",
    [
        ("GARAGE BT1", "GARAGE", True),
        ("Tiefgarage", "GARAGE", True),
        ("Haustechnik", "TECHNIK", True),
        ("E-Technik-", "TECHNIK", True),
        ("MÜLLRAUM", "MUELLRAUM", True),
        ("Zugang Müllraum", "MUELLRAUM", True),   # Bleed-Fix + Vokabular zusammen
        ("Lager", "LAGER", True),
    ],
)
def test_lb_vokabular_typen(label, erwartet, communal):
    # LB-Vokabular-Typen (GARAGE/TECHNIK/LAGER/MUELLRAUM) müssen typen, damit die
    # lb_override-Inklusion/Exklusion sie trifft (sonst tote Regel).
    tf = raumtyp_flags(label)
    assert tf is not None and tf[0] == erwartet and tf[2] is communal


@pytest.mark.parametrize(
    "label, erwartet",
    [("Wohnküche", "KÜCHE"), ("Gästezimmer", "ZIMMER"), ("Abstellkammer", "ABSTELLRAUM"),
     ("Gang", "GANG"), ("Wohnzimmer 01", "WOHNZIMMER")],
)
def test_komposita_erhalten(label, erwartet):
    # Komposita-Köpfe (…küche/…zimmer) + Abstell-Prefix + exaktes Token bleiben erhalten.
    tf = raumtyp_flags(label)
    assert tf is not None and tf[0] == erwartet
