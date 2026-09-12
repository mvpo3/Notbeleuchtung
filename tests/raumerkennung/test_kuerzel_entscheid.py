"""kuerzel_entscheid — mehrdeutiges Kürzel typisiert NUR mit Beleg UND Entscheidung.

Synthetische Mini-DXF (mm, ezdxf) statt echter Pläne: die drei Bedingungen
(Kürzel / Zusatzbeleg / Owner-Entscheidung je Stempelnummer) sind so einzeln
schaltbar. Die Zahlen der echten Fundstelle stehen in
`docs/OFFENE_FRAGEN.md` — hier wird die REGEL geprüft, nicht der Plan.
"""
from __future__ import annotations

import ezdxf

from notbeleuchtung.hauptengine.contracts.raum_modell import Raum
from notbeleuchtung.raumerkennung.dxf_load import lade_dxf
from notbeleuchtung.raumerkennung.kuerzel_entscheid import (
    kandidat_kuerzel,
    loese_kuerzel,
)
from notbeleuchtung.raumerkennung.nutzungsklasse import nutzungsklasse_fuer
from notbeleuchtung.raumerkennung.raumtyp import raumtyp_flags
from notbeleuchtung.raumerkennung.stempel_anker import Stempel

_WAND = "02-TWA-G00-LEG-M0"
# Kandidaten-Raum: 4×4 m, Stempel in der Mitte.
_RAUM_POLY = [(2000.0, 2000.0), (6000.0, 2000.0), (6000.0, 6000.0), (2000.0, 6000.0)]
_STEMPEL_XY = (4000.0, 4000.0)
# Treppen-Block-Extents 6000…7500 mm → 0 mm Kontakt an der Raumkante x=6000.
_STIEGE_XY = (6000.0, 2000.0)


def _plan(tmp_path, name: str, texte=(), stiege_bei=None):
    """Mini-DXF in mm: Wandrechteck (≥15 m → Faktor 1.0), Texte, optional Treppe."""
    doc = ezdxf.new(setup=True)
    doc.header["$INSUNITS"] = 4                      # mm
    msp = doc.modelspace()
    if _WAND not in doc.layers:
        doc.layers.add(_WAND)
    ecken = [(0, 0), (20000, 0), (20000, 12000), (0, 12000)]
    for i in range(4):
        msp.add_line(ecken[i], ecken[(i + 1) % 4], dxfattribs={"layer": _WAND})
    for txt, xy in texte:
        msp.add_mtext(txt, dxfattribs={"layer": "A-AREA-IDEN"}).set_location(xy)
    if stiege_bei is not None:
        if "Stiege_Lauf" not in doc.blocks:
            blk = doc.blocks.new("Stiege_Lauf")
            blk.add_lwpolyline([(0, 0), (1500, 0), (1500, 3000), (0, 3000)], close=True)
        msp.add_blockref("Stiege_Lauf", stiege_bei)
    pfad = tmp_path / f"{name}.dxf"
    doc.saveas(str(pfad))
    return lade_dxf(pfad)


def _raum() -> Raum:
    return Raum(id="raum_65", raum_typ="", polygon_mm=_RAUM_POLY, flaeche_m2=13.04)


def _stempel() -> Stempel:
    # typ=None wie im echten Plan: stempel_anker erfindet für Kürzel keinen Typ.
    return Stempel(name="Schl.", typ=None, flaeche_m2=13.04, belag="Ker.Bel.",
                   position_mm=_STEMPEL_XY, quelle="MTEXT", layer="A-AREA-IDEN")


def test_kandidat_kuerzel_token_exakt():
    assert kandidat_kuerzel("Schl.") == "schl"
    # kein Substring-Bleed: die echten Plan-Treffer von „schl" als Substring
    # (Anschluß, Lüftungsschlitz, TÜRSCHLIESSER) dürfen NICHT greifen.
    for fremd in ("Anschluß", "Lüftungsschlitz", "TÜRSCHLIESSER", "Zimmer"):
        assert kandidat_kuerzel(fremd) is None


def test_kuerzel_allein_bleibt_untypisiert(tmp_path):
    """Nummer im Register, aber KEIN Zusatzbeleg → kein Typ."""
    plan = _plan(tmp_path, "nur_kuerzel", texte=[("E2-VF-11a", (4300.0, 4000.0))])
    raum, stempel = _raum(), _stempel()
    hinweise = loese_kuerzel(plan, [(raum, stempel)], [raum])
    assert raum.raum_typ == ""
    assert len(hinweise) == 1
    assert "kein Zusatzbeleg" in hinweise[0]
    assert "raum_65" in hinweise[0] and "schl" in hinweise[0]


def test_beleg_ohne_entscheidung_bleibt_untypisiert(tmp_path):
    """Zusatzbeleg da, Stempelnummer NICHT im Register (E2-VF-11b) → kein Typ."""
    plan = _plan(tmp_path, "beleg_ohne_ent",
                 texte=[("E2-VF-11b", (4300.0, 4000.0)), ("DBA", (5400.0, 4000.0))])
    raum, stempel = _raum(), _stempel()
    hinweise = loese_kuerzel(plan, [(raum, stempel)], [raum])
    assert raum.raum_typ == ""
    assert len(hinweise) == 1
    assert "Entscheidung ausstehend" in hinweise[0]
    assert "E2-VF-11b" in hinweise[0] and "DBA" in hinweise[0]


def test_beleg_und_entscheidung_typisiert_schleuse(tmp_path):
    """Text-Beleg + eingetragene Stempelnummer → SCHLEUSE mit Flags."""
    plan = _plan(tmp_path, "beleg_und_ent",
                 texte=[("E2-VF-11a", (4300.0, 4000.0)), ("DBA", (5400.0, 4000.0))])
    raum, stempel = _raum(), _stempel()
    hinweise = loese_kuerzel(plan, [(raum, stempel)], [raum])
    assert raum.raum_typ == "SCHLEUSE"
    assert raum.ist_fluchtweg is True
    assert raum.ist_communal is True
    assert nutzungsklasse_fuer(raum.raum_typ) == "ALLGEMEIN_ERSCHLIESSUNG"
    assert len(hinweise) == 1
    assert "SCHLEUSE" in hinweise[0] and "Enis" in hinweise[0]


def test_stiegenkern_lage_als_beleg_typisiert(tmp_path):
    """Zweiter Belegweg: 0-mm-Kontakt zum Treppen-Block-Extent statt Text-Beleg."""
    plan = _plan(tmp_path, "stiegenkern", texte=[("E2-VF-11a", (4300.0, 4000.0))],
                 stiege_bei=_STIEGE_XY)
    raum, stempel = _raum(), _stempel()
    hinweise = loese_kuerzel(plan, [(raum, stempel)], [raum])
    assert raum.raum_typ == "SCHLEUSE"
    assert "Stiegenkern-Lage" in hinweise[0]


def test_stiegenhaus_polygon_als_beleg_typisiert(tmp_path):
    """Dritter Belegweg: 0-mm-Kontakt zu einem STIEGENHAUS-typisierten Raum."""
    plan = _plan(tmp_path, "stgh_polygon", texte=[("E2-VF-11a", (4300.0, 4000.0))])
    raum, stempel = _raum(), _stempel()
    stgh = Raum(id="raum_88", raum_typ="STIEGENHAUS", flaeche_m2=20.67,
                polygon_mm=[(6000.0, 2000.0), (9000.0, 2000.0),
                            (9000.0, 6000.0), (6000.0, 6000.0)])
    hinweise = loese_kuerzel(plan, [(raum, stempel)], [raum, stgh])
    assert raum.raum_typ == "SCHLEUSE"
    assert "Stiegenkern-Lage" in hinweise[0]


def test_ohne_nummer_bleibt_untypisiert(tmp_path):
    """Beleg da, aber kein Nummerntext im Stempelumkreis → Entscheidung greift nicht."""
    plan = _plan(tmp_path, "ohne_nummer", texte=[("DBA", (5400.0, 4000.0))])
    raum, stempel = _raum(), _stempel()
    hinweise = loese_kuerzel(plan, [(raum, stempel)], [raum])
    assert raum.raum_typ == ""
    assert "keine Nummer gefunden" in hinweise[0]
    assert "Entscheidung ausstehend" in hinweise[0]


def test_ausgeschriebene_schleuse_typt_direkt():
    """Das ausgeschriebene Wort ist eindeutig → regulärer Kanon-Weg, ohne Register."""
    assert raumtyp_flags("Schleuse") == ("SCHLEUSE", True, True)
    assert raumtyp_flags("DBA-Abstr. Schleuse") == ("SCHLEUSE", True, True)
    assert nutzungsklasse_fuer("SCHLEUSE") == "ALLGEMEIN_ERSCHLIESSUNG"
    # Das KÜRZEL bleibt im Wörterbuch bewusst unbelegt.
    assert raumtyp_flags("Schl.") is None


def test_keine_kandidaten_kein_aufwand(tmp_path):
    plan = _plan(tmp_path, "leer")
    assert loese_kuerzel(plan, [], []) == []
