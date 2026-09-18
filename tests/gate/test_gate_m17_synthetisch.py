"""Guard für die Gate-Messfunktion — synthetische Geometrie, ohne DXF und Referenz.

Die echte Messung läuft gegen den Rennweg-Plan und das Übergabepaket (beides
außerhalb dieser Tests). Hier steht nur die SEMANTIK auf dem Prüfstand: je
Prüfart mindestens ein BESTANDEN- und ein NICHT_BESTANDEN-Pfad, die
Mehrdeutigkeits-Fälle (Sonde in zwei Räumen, Durchgang ohne Türblatt) und der
feste Nenner. Alle Koordinaten sind frei erfunden: zwei Rechteckräume mit einer
100 mm starken Wand dazwischen, die am T-Knoten aus zwei Körpern besteht.
"""
from __future__ import annotations

from types import SimpleNamespace

import pytest
from gate_m17 import messe
from gate_og1 import kennzahlen

from notbeleuchtung.hauptengine.contracts import RaumModell
from notbeleuchtung.hauptengine.contracts.raum_modell import BBox, Raum, Tuer


def _rect(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]


RAUM_L = _rect(0, 0, 2000, 3000)
RAUM_R = _rect(2100, 0, 4100, 3000)
RAUM_X = _rect(400, 900, 600, 1100)        # überlappt A -> mehrdeutige Zuordnung
WAND_U = _rect(2000, 0, 2100, 1500)
CLIP_T = _rect(1500, 1200, 2600, 1800)     # markiertes Stück am T-Knoten
CLIP_W = _rect(1900, 1200, 2200, 1800)     # markiertes Wandstück

SONDEN = {"W": [2050, 700], "C": [1000, 1500], "A": [500, 1000], "B": [3000, 1000],
          "B_links": [1500, 2000], "I": [3000, 1500], "X_aussen": [1000, 1500],
          "X_innen": [3500, 1500], "J": [2050, 1500]}


def _raeume(mit_ueberlappung: bool = False) -> list[Raum]:
    r = [Raum(id="raum_links", raum_typ="ZIMMER", polygon_mm=RAUM_L, flaeche_m2=6.0),
         Raum(id="raum_rechts", raum_typ="ZIMMER", polygon_mm=RAUM_R, flaeche_m2=6.0)]
    if mit_ueberlappung:
        r.append(Raum(id="raum_extra", raum_typ="ABSTELLRAUM", polygon_mm=RAUM_X,
                      flaeche_m2=0.04))
    return r


def _koerper(spalt_mm: float = 0.5) -> list[SimpleNamespace]:
    oben = _rect(2000, 1500 + spalt_mm, 2100, 3000)
    return [SimpleNamespace(polygon_mm=WAND_U), SimpleNamespace(polygon_mm=oben)]


def _tuer(ohne_tuerblatt: bool = False, *, id="tuer_1", xy_mm=(2050, 1500),
          breite_mm=900.0, von_raum="raum_links", nach_raum="raum_rechts") -> Tuer:
    return Tuer(id=id, xy_mm=xy_mm, breite_mm=breite_mm,
                von_raum=von_raum, nach_raum=nach_raum,
                ohne_tuerblatt=ohne_tuerblatt, quelle="block")


def _ref(kind: str, expected, objects, *, clip=CLIP_W, route=None, spalt_mm=0.5):
    fall = {"id": "S-01", "probes_wcs_source_units": SONDEN,
            "clip_polygon_wcs_source_units": clip, "wall": ["H1", "H2"],
            "checks": [{"id": "S-01-a", "kind": kind, "expected": expected,
                        "objects": objects}]}
    if route is not None:
        fall["route_wcs_source_units"] = route
    oben = _rect(2000, 1500 + spalt_mm, 2100, 3000)
    return {"source_entities": {"H1": {"points_wcs_source_units": WAND_U},
                                "H2": {"points_wcs_source_units": oben}},
            "cases": [fall]}


def _miss(ref, *, raeume=None, tueren=(), spalt_mm=0.5):
    """Ein Fall, ein check — das eine Ergebnis zurück."""
    return messe(ref, raeume if raeume is not None else _raeume(), list(tueren),
                 _koerper(spalt_mm))[0]


# ------------------------------------------------- physical_wall_covers_probe

@pytest.mark.parametrize(("sonde", "expected", "status"), [
    ("W", True, "BESTANDEN"),          # W liegt im Wandkörper, in keinem Raum
    ("C", True, "NICHT_BESTANDEN"),    # C liegt im Raum, nicht in der Wand
    ("C", False, "BESTANDEN"),
    ("W", False, "NICHT_BESTANDEN"),
])
def test_wand_deckt_sonde(sonde, expected, status):
    e = _miss(_ref("physical_wall_covers_probe", expected, [sonde]))
    assert e["status"] == status, e["grund"]


# ---------------------------------------------------------------- same_room

def test_same_room_gleicher_raum_ohne_wand_auf_der_route():
    e = _miss(_ref("same_room", True, ["A", "B_links"],
                   route=[[500, 1000], [1500, 2000]]))
    assert e["status"] == "BESTANDEN", e["grund"]


def test_same_room_verschiedene_raeume():
    e = _miss(_ref("same_room", True, ["A", "B"]))
    assert e["status"] == "NICHT_BESTANDEN"


def test_same_room_route_durch_die_wand_faellt_durch():
    e = _miss(_ref("same_room", True, ["A", "B"], route=[[1000, 800], [3000, 800]]))
    assert e["status"] == "NICHT_BESTANDEN"
    assert e["messwerte"]["route_schnitt"], "Schnittlängen gehören in die Messwerte"


def test_sonde_in_zwei_raeumen_ist_nicht_messbar():
    e = _miss(_ref("same_room", True, ["A", "B_links"]),
              raeume=_raeume(mit_ueberlappung=True))
    assert e["status"] == "NICHT_MESSBAR"
    assert "mehrdeutig" in e["grund"]


# --------------------------------------------------------- room_covers_probe

@pytest.mark.parametrize(("sonde", "expected", "status"), [
    ("I", True, "BESTANDEN"),
    ("W", True, "NICHT_BESTANDEN"),     # W liegt in keinem Raumpolygon
])
def test_raum_deckt_sonde_positiv(sonde, expected, status):
    e = _miss(_ref("room_covers_probe", expected, [sonde]))
    assert e["status"] == status, e["grund"]


def test_raum_deckt_sonde_positiv_mehrdeutig_ist_nicht_messbar():
    """Sonde in zwei Raumpolygonen ist keine Messung — gleiche Lesart wie same_room."""
    e = _miss(_ref("room_covers_probe", True, ["A"]), raeume=_raeume(mit_ueberlappung=True))
    assert e["status"] == "NICHT_MESSBAR", e["grund"]
    assert "mehrdeutig" in e["grund"]


@pytest.mark.parametrize(("sonde", "status"), [
    ("X_aussen", "BESTANDEN"),          # links -> nicht im Zielraum rechts
    ("X_innen", "NICHT_BESTANDEN"),     # rechts -> doch im Zielraum
])
def test_raum_deckt_sonde_negativ(sonde, status):
    ref = _ref("room_covers_probe", True, ["I"])
    ref["cases"][0]["checks"].append(
        {"id": "S-01-b", "kind": "room_covers_probe", "expected": False, "objects": [sonde]})
    e = messe(ref, _raeume(), [], _koerper())[1]
    assert e["status"] == status, e["grund"]
    assert e["messwerte"]["zielraum"] == "raum_rechts"


# ------------------------------------------ direct_portal_in_probe_segment

def test_kein_direktes_portal_im_markierten_stueck():
    e = _miss(_ref("direct_portal_in_probe_segment", False, ["A", "B"]))
    assert e["status"] == "BESTANDEN", e["grund"]


def test_direktes_portal_im_markierten_stueck_faellt_durch():
    e = _miss(_ref("direct_portal_in_probe_segment", False, ["A", "B"]), tueren=[_tuer()])
    assert e["status"] == "NICHT_BESTANDEN"
    assert [p["id"] for p in e["messwerte"]["portale"]] == ["tuer_1"]


def test_portal_zaehlt_auch_ohne_zweite_raumseite():
    """Verliert eine Tür durch einen Slice die Gegenseite, bleibt die Öffnung."""
    e = _miss(_ref("direct_portal_in_probe_segment", False, ["A", "B"]),
              tueren=[_tuer(nach_raum=None)])
    assert e["status"] == "NICHT_BESTANDEN", e["grund"]
    portal = e["messwerte"]["portale"][0]
    assert portal["id"] == "tuer_1" and portal["nach_raum"] is None
    assert portal["abstand_wand_mm"] == 0.0
    assert e["messwerte"]["direkte_tueren_gesamt"] == 0


def test_tuer_weit_weg_von_der_wand_ist_kein_portal():
    """500 mm von der markierten Wand entfernt (Grenze 250 mm), fremde Räume."""
    e = _miss(_ref("direct_portal_in_probe_segment", False, ["A", "B"], clip=CLIP_T),
              tueren=[_tuer(id="tuer_fern", xy_mm=(1500, 1500),
                            von_raum="raum_x", nach_raum="raum_y")])
    assert e["status"] == "BESTANDEN", e["grund"]
    assert e["messwerte"]["portale"] == []


# ------------------------------------- distinct_rooms_connected_by_door

def test_genau_eine_tuerverbindung():
    e = _miss(_ref("distinct_rooms_connected_by_door", True, ["A", "B", "J"]),
              tueren=[_tuer()])
    assert e["status"] == "BESTANDEN", e["grund"]


def test_keine_tuerverbindung_faellt_durch():
    e = _miss(_ref("distinct_rooms_connected_by_door", True, ["A", "B", "J"]))
    assert e["status"] == "NICHT_BESTANDEN"


def test_verbindung_ausserhalb_der_halben_breite_von_o_zaehlt_nicht():
    """Die Sonde O markiert die Öffnung: 500 mm entfernt bei 900 mm Breite ist sie es nicht."""
    e = _miss(_ref("distinct_rooms_connected_by_door", True, ["A", "B", "J"], clip=CLIP_T),
              tueren=[_tuer(id="tuer_fern", xy_mm=(2550, 1500))])
    assert e["status"] == "NICHT_BESTANDEN", e["grund"]
    assert e["messwerte"]["verbindungen"] == []


def test_verbindung_ohne_tuerblatt_ist_nicht_messbar():
    e = _miss(_ref("distinct_rooms_connected_by_door", True, ["A", "B", "J"]),
              tueren=[_tuer(ohne_tuerblatt=True)])
    assert e["status"] == "NICHT_MESSBAR"
    assert "Türblatt" in e["grund"]
    # Der Grund muss die gemessenen Fakten tragen, nicht nur die Frage.
    for teil in ("tuer_1", "900.0 mm", "0 mm von J", "docs/OFFENE_FRAGEN.md"):
        assert teil in e["grund"], e["grund"]
    assert e["messwerte"]["verbindungen"][0]["abstand_zu_O_mm"] == 0


# ------------------------------------- physical_wall_intersects_route

@pytest.mark.parametrize(("route", "status"), [
    ([[500, 800], [1500, 800]], "BESTANDEN"),        # bleibt im linken Raum
    ([[1000, 800], [3000, 800]], "NICHT_BESTANDEN"),  # quert die Wand
])
def test_route_schneidet_wand(route, status):
    e = _miss(_ref("physical_wall_intersects_route", False, ["A", "B"], route=route))
    assert e["status"] == status, e["grund"]


# ------------------------------------------------- wall_contact_preserved

def test_kontakt_bei_halbem_millimeter_spalt_bleibt_erhalten():
    e = _miss(_ref("wall_contact_preserved", True, ["H1", "H2", "J"], clip=CLIP_T),
              spalt_mm=0.5)
    assert e["status"] == "BESTANDEN", e["grund"]
    assert e["messwerte"]["abstand_mm"] == pytest.approx(0.5, abs=1e-3)
    assert e["messwerte"]["leck"] is False
    assert e["messwerte"]["intersects"] is False
    assert e["messwerte"]["touches"] is False


def test_beruehrende_koerper_melden_touches_und_signifikante_null():
    """Spalt 0: die Körper berühren sich — intersects/touches stehen in den Messwerten."""
    e = _miss(_ref("wall_contact_preserved", True, ["H1", "H2", "J"], clip=CLIP_T,
                   spalt_mm=0.0), spalt_mm=0.0)
    assert e["status"] == "BESTANDEN", e["grund"]
    assert e["messwerte"]["intersects"] is True
    assert e["messwerte"]["touches"] is True
    assert e["messwerte"]["abstand_mm"] == 0.0
    assert "Quellpräzision im Speicher" in e["grund"]


def test_fuenf_millimeter_spalt_bricht_kontakt_und_leckt():
    e = _miss(_ref("wall_contact_preserved", True, ["H1", "H2", "J"], clip=CLIP_T,
                   spalt_mm=5.0), spalt_mm=5.0)
    assert e["status"] == "NICHT_BESTANDEN"
    assert e["messwerte"]["leck"] is True


def test_quellwand_ohne_wandkoerper_faellt_durch():
    ref = _ref("wall_contact_preserved", True, ["H1", "H2", "J"], clip=CLIP_T)
    ref["source_entities"]["H2"]["points_wcs_source_units"] = _rect(9000, 9000, 9100, 9500)
    e = _miss(ref)
    assert e["status"] == "NICHT_BESTANDEN"
    assert "nicht als Wandkörper erkannt" in e["grund"]


# ------------------------------------------------------------------ Nenner

def test_nenner_bleibt_die_anzahl_der_checks_auch_bei_unbekannter_pruefart():
    ref = _ref("physical_wall_covers_probe", True, ["W"])
    ref["cases"][0]["checks"].append(
        {"id": "S-01-b", "kind": "quantenmechanik", "expected": True, "objects": ["W"]})
    ergebnisse = messe(ref, _raeume(), [], _koerper())
    assert [e["id"] for e in ergebnisse] == ["S-01-a", "S-01-b"]
    assert ergebnisse[1]["status"] == "NICHT_MESSBAR"
    assert all(e["status"] in ("BESTANDEN", "NICHT_BESTANDEN", "NICHT_MESSBAR")
               for e in ergebnisse)


# ------------------------------------------------------------ OG1-Kennzahlen

def test_og1_kennzahlen():
    modell = RaumModell(
        floor="OG1", bounds_mm=BBox(min_xy=(0, 0), max_xy=(4100, 3000)),
        raeume=[Raum(id="r1", raum_typ="ZIMMER", wohnung_id="w1"),
                Raum(id="r2", raum_typ="", wohnung_id="w1"),
                Raum(id="r3", raum_typ="UNBEKANNT", wohnung_id="w2"),
                Raum(id="r4", raum_typ="GANG")],
        tueren=[Tuer(id="t1", xy_mm=(0, 0), von_raum="r1", nach_raum="r1"),
                Tuer(id="t2", xy_mm=(1, 1), von_raum="r1", nach_raum="r2",
                     ohne_tuerblatt=True),
                Tuer(id="t3", xy_mm=(2, 2), von_raum="r3", nach_raum=None)])
    k = kennzahlen(modell)
    assert k["raeume_gesamt"] == 4
    assert k["unbekannt"] == 2
    assert k["tueren_gesamt"] == 3
    assert k["tueren_raum_a_gleich_b"] == 1
    assert k["tueren_raum_a_gleich_b_liste"] == [{"id": "t1", "raum": "r1"}]
    assert k["durchgaenge_ohne_tuerblatt"] == 1
    assert k["wohnungen"] == 2
    assert k["einraum_wohnungen"] == 1
    assert k["einraum_wohnungen_liste"] == ["w2"]
