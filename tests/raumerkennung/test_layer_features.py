"""layer_features — Golden-Vektoren auf SYNTHETISCHEN DXF + Namens-Blindheit.

Warum synthetisch: ein Golden muss deterministisch und klein sein. Die echten
Prüfpläne sind zwar versioniert (`tests/plaene.py`), ihre Zahlen gehören aber in
`scripts/analyse/layer_merkmale.py` und in den Bericht, nicht in einen CI-Test.

Die Werte unten sind gepinnte Referenz: jede Toleranz-/Formeländerung verschiebt
sie lautlos, deshalb sind sie exakt und `FEATURE_LAYOUT_VERSION` steht mit drin.
"""
from __future__ import annotations

import math
import random
from pathlib import Path

import ezdxf
import pytest

from notbeleuchtung.raumerkennung import layer_features as lf
from notbeleuchtung.raumerkennung.dxf_load import lade_dxf
from notbeleuchtung.raumerkennung.layer_features import (
    FEATURE_LAYOUT_VERSION,
    FEATURE_NAMES,
    VECTOR_LEN,
    klassifiziere_plan,
    merkmale_aus_plan,
)

W = "02-TWA-G00-LEG-M0"


def _merkmale(pfad: Path, plan_id: str = "synth"):
    plan = lade_dxf(pfad)
    return plan, {m.layer_name: m for m in merkmale_aus_plan(plan, plan_id)}


def _merkmale_nach_runde2(pfad: Path, plan_id: str = "d2"):
    """Befunde nach Runde 1 + Runde 2, je Layername (für die lf-2-Tests)."""
    plan = lade_dxf(pfad)
    return plan, {b.layer_name: b for b in klassifiziere_plan(plan, plan_id)}


def _wandrechteck(doc) -> None:
    """20 m × 12 m Wandrechteck — genug Ausdehnung für die Faktor-Kalibrierung."""
    doc.layers.add(W)
    msp = doc.modelspace()
    c = [(0, 0), (20000, 0), (20000, 12000), (0, 12000)]
    for i in range(4):
        msp.add_line(c[i], c[(i + 1) % 4], dxfattribs={"layer": W})


def _neu(insunits: int = 4):
    doc = ezdxf.new(setup=True)
    doc.header["$INSUNITS"] = insunits
    return doc


# ── 1. Gepinnte Vektoren auf build_synth_dxf ─────────────────────────────────
def test_synth_vektoren_gepinnt(synth_dxf):
    plan, m = _merkmale(synth_dxf)
    assert plan.factor == 1.0
    assert plan.wall_layers == frozenset({W})

    wand = m[W]
    assert (wand.n_entities, wand.n_punkte, wand.quelle) == (5, 10, "msp")
    assert wand.anteil_line == 1.0
    assert (wand.anteil_polyline, wand.anteil_hatch, wand.anteil_insert,
            wand.anteil_text, wand.anteil_geschlossen) == (0.0, 0.0, 0.0, 0.0, 0.0)
    assert wand.layer_diag_mm == pytest.approx(23323.807579381202, rel=1e-9)
    assert wand.laenge_p50_mm == 12000.0
    assert wand.laenge_p50_rel == pytest.approx(0.5144957554275265, rel=1e-9)
    assert wand.laenge_p90_rel == pytest.approx(0.8574929257125442, rel=1e-9)
    assert wand.laenge_spreizung == pytest.approx(5 / 3, rel=1e-9)
    assert wand.ortho_quote == 1.0
    assert wand.parallel_quote == 0.0          # 12 000/8 000 mm liegen über 600 mm
    assert wand.farb_entropie == 0.0
    assert wand.ltype_entropie == 0.0
    assert wand.punktdichte_pro_m2 == pytest.approx(10 / 240, rel=1e-9)
    assert wand.layer_diag_rel == 1.0
    assert wand.bbox_aspekt == pytest.approx(0.6, rel=1e-9)

    weg = m["09-WEG-G00-LEG-M0"]
    assert weg.anteil_polyline == 1.0
    assert weg.anteil_geschlossen == 0.0
    assert weg.n_punkte == 4
    assert weg.layer_diag_mm == pytest.approx(11180.339887498949, rel=1e-9)
    assert weg.laenge_p50_mm == 5000.0
    assert weg.laenge_p50_rel == pytest.approx(0.4472135954999579, rel=1e-9)
    assert weg.laenge_p90_rel == pytest.approx(0.8944271909999159, rel=1e-9)
    assert weg.ortho_quote == 1.0
    assert weg.punktdichte_pro_m2 == pytest.approx(0.08, rel=1e-9)

    # Null-Guard-Fälle: ein Einfügepunkt spannt keine Fläche auf.
    txt = m["01-TXT-G00-LEG-M0"]
    assert txt.anteil_text == 1.0
    assert txt.layer_diag_mm == 0.0
    assert txt.punktdichte_pro_m2 == 0.0
    assert txt.laenge_p50_rel == 0.0
    sym = m["05-SYM-G00-LEG-M0"]
    assert sym.anteil_insert == 1.0
    assert sym.layer_diag_mm == 0.0


# ── 2. Der harte Nachweis: kein Feature sieht den Layernamen ─────────────────
def test_namen_blind(synth_dxf, tmp_path):
    """Dieselbe Geometrie mit ZZZ_*-Layernamen muss identische Vektoren geben."""
    _, original = _merkmale(synth_dxf)
    doc = ezdxf.readfile(str(synth_dxf))
    abbildung = {a: f"ZZZ_{i + 1}"
                 for i, a in enumerate(sorted({str(e.dxf.layer)
                                               for e in doc.modelspace()}))}
    for neu in abbildung.values():
        if neu not in doc.layers:
            doc.layers.add(neu)
    for e in doc.modelspace():
        e.dxf.layer = abbildung[str(e.dxf.layer)]
    ziel = tmp_path / "umbenannt.dxf"
    doc.saveas(str(ziel))

    _, umbenannt = _merkmale(ziel)
    assert set(umbenannt) == set(abbildung.values())
    for alt, m in original.items():
        assert m.to_vector() == umbenannt[abbildung[alt]].to_vector(), alt


# ── 3. Der mm-Faktor, nicht $INSUNITS ────────────────────────────────────────
def _rechteck(pfad: Path, einheit: float) -> Path:
    """Dasselbe Rechteck in mm bzw. in Metern — $INSUNITS behauptet beide Male mm."""
    doc = _neu(4)
    doc.layers.add(W)
    msp = doc.modelspace()
    c = [(0, 0), (20000 * einheit, 0), (20000 * einheit, 12000 * einheit),
         (0, 12000 * einheit)]
    for i in range(4):
        msp.add_line(c[i], c[(i + 1) % 4], dxfattribs={"layer": W})
    msp.add_line((12000 * einheit, 0), (12000 * einheit, 12000 * einheit),
                 dxfattribs={"layer": W})
    doc.saveas(str(pfad))
    return pfad


def test_faktor_statt_insunits(tmp_path):
    """Owner-Fall: $INSUNITS=4 (mm), gezeichnet in Metern → Faktor 1000.

    Der Vektor muss danach identisch zur mm-Variante sein — inklusive der
    absoluten mm-Features. Genau das ist „setzt zwingend auf dem kalibrierten
    mm-Faktor auf".
    """
    plan_mm, m_mm = _merkmale(_rechteck(tmp_path / "mm.dxf", 1.0), "mm")
    plan_m, m_m = _merkmale(_rechteck(tmp_path / "meter.dxf", 0.001), "meter")
    assert plan_mm.factor == 1.0
    assert plan_m.factor == 1000.0
    assert m_m[W].laenge_p50_mm == m_mm[W].laenge_p50_mm == 12000.0
    assert m_m[W].layer_diag_mm == pytest.approx(m_mm[W].layer_diag_mm, rel=1e-9)
    assert m_m[W].to_vector() == m_mm[W].to_vector()


# ── 4. Doppellinien-Wand ohne Namen ──────────────────────────────────────────
@pytest.mark.parametrize(("abstand", "quote"), [(150.0, 1.0), (900.0, 0.0)])
def test_doppellinie_parallel_quote(tmp_path, abstand, quote):
    """50–600 mm Senkrechtabstand ist Wand, 900 mm ist keine (wandkoerper-Fenster)."""
    doc = _neu()
    _wandrechteck(doc)
    doc.layers.add("DW")
    msp = doc.modelspace()
    msp.add_line((2000, 3000), (10000, 3000), dxfattribs={"layer": "DW"})
    msp.add_line((2000, 3000 + abstand), (10000, 3000 + abstand),
                 dxfattribs={"layer": "DW"})
    pfad = tmp_path / f"dw{int(abstand)}.dxf"
    doc.saveas(str(pfad))
    _, m = _merkmale(pfad, "dw")
    assert m["DW"].parallel_quote == quote


# ── 5. Geschlossene Raumkontur ───────────────────────────────────────────────
def test_raumkontur_geschlossen(tmp_path):
    doc = _neu()
    _wandrechteck(doc)
    doc.layers.add("RK")
    doc.modelspace().add_lwpolyline(
        [(1000, 1000), (13000, 1000), (13000, 9000), (1000, 9000)],
        close=True, dxfattribs={"layer": "RK"})
    pfad = tmp_path / "rk.dxf"
    doc.saveas(str(pfad))
    _, m = _merkmale(pfad, "rk")
    rk = m["RK"]
    assert rk.anteil_geschlossen == 1.0
    assert rk.flaeche_median_m2 == pytest.approx(96.0, rel=1e-9)
    assert 1.0 <= rk.flaeche_median_m2 <= 200.0      # Raumgrößen-Fenster
    assert rk.laenge_p50_mm == 12000.0               # geschlossenes letztes Segment


# ── 6. Block-Abstieg ist Pflicht ─────────────────────────────────────────────
def test_block_quelle(tmp_path):
    """Ohne Abstieg in INSERTs wäre dieser Layer unsichtbar (Falle 3)."""
    doc = _neu()
    _wandrechteck(doc)
    doc.layers.add("SYM")
    doc.layers.add("INNEN-GEOM")
    blk = doc.blocks.new("INNEN")
    for i in range(6):
        blk.add_line((3000, 2000 + i * 400), (9000, 2000 + i * 400),
                     dxfattribs={"layer": "INNEN-GEOM"})
    doc.modelspace().add_blockref("INNEN", (0, 0), dxfattribs={"layer": "SYM"})
    pfad = tmp_path / "blk.dxf"
    doc.saveas(str(pfad))
    _, m = _merkmale(pfad, "blk")
    innen = m["INNEN-GEOM"]
    assert innen.quelle == "block"
    assert innen.n_entities == 6
    assert innen.n_punkte == 12
    assert innen.anteil_line == 1.0
    assert innen.parallel_quote == 1.0        # 400 mm Abstand → Doppellinien-Beleg
    assert m["SYM"].quelle == "msp"           # der INSERT selbst


# ── 7. Layout-Pin ────────────────────────────────────────────────────────────
def test_layout_pin(synth_dxf):
    """Jede Umsortierung/Umbenennung eines Features muss hier rot werden."""
    assert FEATURE_LAYOUT_VERSION == "lf-2"
    assert len(FEATURE_NAMES) == VECTOR_LEN == 37
    assert FEATURE_NAMES == (
        "anteil_line", "anteil_polyline", "anteil_hatch", "anteil_insert",
        "anteil_text", "anteil_bogen", "anteil_dimension", "anteil_geschlossen",
        "laenge_p10_rel", "laenge_p50_rel", "laenge_p90_rel", "laenge_spreizung",
        "ortho_quote", "winkel_entropie", "parallel_quote", "hatch_flaechen_anteil",
        "hatch_schmal_quote", "hatch_solid_quote", "hatch_einfach_quote",
        "hatch_kreuz_quote", "hatch_paar_sd_quote", "hatch_welle_quote",
        "hatch_bg_quote", "farb_entropie", "ltype_entropie", "punktdichte_pro_m2",
        "layer_diag_rel", "bbox_aspekt", "laenge_p50_mm", "layer_diag_mm",
        "runde2", "wand_naehe_quote", "wand_parallel_quote", "wand_endpunkt_quote",
        "wand_umschlossen_quote", "wand_kontur_deckung", "wand_abstand_p50_rel")
    _, m = _merkmale(synth_dxf)
    for merkmale in m.values():
        assert len(merkmale.to_vector()) == VECTOR_LEN


# ── 8. Hatch-Struktur ohne Materialnamen ─────────────────────────────────────
def test_hatch_struktur_quoten(tmp_path):
    """struktur_klasse ist reine Musterliniengeometrie — kein Alias, kein Layer."""
    doc = _neu()
    _wandrechteck(doc)
    doc.layers.add("HX")
    msp = doc.modelspace()
    solid = msp.add_hatch(color=7, dxfattribs={"layer": "HX"})
    solid.paths.add_polyline_path(
        [(1000, 1000), (2000, 1000), (2000, 2000), (1000, 2000)], is_closed=True)
    kreuz = msp.add_hatch(color=7, dxfattribs={"layer": "HX"})
    kreuz.paths.add_polyline_path(
        [(3000, 1000), (4000, 1000), (4000, 2000), (3000, 2000)], is_closed=True)
    kreuz.set_pattern_fill("KREUZ", definition=[[45.0, (0, 0), (0, 100.0), []],
                                                [135.0, (0, 0), (0, 100.0), []]])
    pfad = tmp_path / "hx.dxf"
    doc.saveas(str(pfad))
    _, m = _merkmale(pfad, "hx")
    hx = m["HX"]
    assert hx.anteil_hatch == 1.0
    assert hx.hatch_solid_quote == 0.5
    assert hx.hatch_kreuz_quote == 0.5
    assert hx.hatch_einfach_quote == 0.0
    assert hx.layer_diag_mm > 0.0        # Hatch-Ränder spannen die Extents auf


# ── 9. Runde 2 ohne Selbstbezug (lf-2) ──────────────────────────────────────
def _doppellinien_plan(pfad: Path, *, zwei: bool) -> Path:
    """Wandrechteck + 1 bzw. 2 Doppellinien-Layer (6 Linien im 400-mm-Raster).

    Die Doppellinien-Layer sind die EINZIGEN, die Runde 1 mit
    `confidence >= 0.60` als `wand` erkennt — nur so entsteht überhaupt eine
    Runde-2-Referenz (das Wandrechteck allein kommt auf 0,25).
    """
    doc = _neu()
    _wandrechteck(doc)
    msp = doc.modelspace()
    msp.add_line((12000, 0), (12000, 12000), dxfattribs={"layer": W})
    for name, y0 in [("DW1", 2000), *([("DW2", 9000)] if zwei else [])]:
        doc.layers.add(name)
        for i in range(6):
            msp.add_line((3000, y0 + i * 400), (9000, y0 + i * 400),
                         dxfattribs={"layer": name})
    doc.saveas(str(pfad))
    return pfad


def _r2(m) -> tuple[float, ...]:
    return tuple(getattr(m, n) for n in FEATURE_NAMES[30:])


def test_runde2_ohne_selbstbezug(tmp_path):
    """Der einzige Wandlayer misst NICHT gegen sich selbst, sondern ist unbelegt.

    Mit Selbstbezug (lf-1) stand DW1 auf naehe = parallel = endpunkt = 1,000 bei
    `wand_abstand_p50_rel` 0,0000 — bei den Gewichten 0,25 + 0,20 des
    `oeffnung`-Scores waren das +0,45 geschenkt. Jetzt ist die Referenz
    `wand ohne DW1`, also leer: `runde2_belegt` False und alle sieben Felder auf
    dem neutralen 0.0. Werte aus dem Lauf gepinnt.
    """
    _, m = _merkmale_nach_runde2(_doppellinien_plan(tmp_path / "ein.dxf", zwei=False))
    dw1 = m["DW1"]
    assert (dw1.rolle, dw1.modus) == ("wand", "BESTAETIGEN")
    assert dw1.confidence == 0.84            # Deckel „Runde 2 unbelegt"
    assert dw1.merkmale.runde2_belegt is False
    assert _r2(dw1.merkmale) == (0.0,) * 7

    # Die übrigen Layer messen gegen DW1 — die sind belegt.
    wand = m[W]
    assert wand.merkmale.runde2_belegt is True
    assert wand.merkmale.runde2 == 1.0
    assert wand.merkmale.wand_abstand_p50_rel == pytest.approx(
        0.3663211384435633, rel=1e-9)


def test_runde2_referenz_ist_wand_ohne_sich_selbst(tmp_path):
    """Zwei Wandlayer: jeder misst gegen den ANDEREN, keiner gegen sich.

    DW1 und DW2 liegen 5 m auseinander (> `_NAEHE_MM`), deshalb ist
    `wand_naehe_quote` 0,0 statt der 1,0 aus dem Selbstbezug. Beide sind
    symmetrisch, also identisch bewertet.
    """
    _, m = _merkmale_nach_runde2(_doppellinien_plan(tmp_path / "zwei.dxf", zwei=True))
    dw1, dw2 = m["DW1"].merkmale, m["DW2"].merkmale
    for d in (dw1, dw2):
        assert d.runde2_belegt is True
        assert (d.wand_naehe_quote, d.wand_parallel_quote,
                d.wand_endpunkt_quote) == (0.0, 0.0, 0.0)
        assert d.wand_abstand_p50_rel == pytest.approx(0.26582280697088867,
                                                       rel=1e-9)
    assert _r2(dw1) == _r2(dw2)
    # wandfern (> _WAND_FERN_REL) dämpft den Wand-Score auf 0,8 — kein Bonus.
    assert m["DW1"].confidence == m["DW2"].confidence == 0.8


# ── 10. Stichprobe: Reihenfolge der Eingabe darf nichts verschieben ──────────
def test_stichprobe_reihenfolgefrei():
    """Über dem Deckel `_MAX_SEGMENTE` muss getauschte Reihenfolge identisch sein.

    Greift bewusst auf die Modul-Internas zu: 1800 Segmente als DXF zu schreiben
    macht den Test nur langsam. Mit `random.Random(0).sample` wichen hier 8 von
    37 Features ab (laenge_spreizung, parallel_quote, laenge_p50_mm,
    laenge_p10/p50/p90_rel, ortho_quote, winkel_entropie).
    """
    rnd = random.Random(42)
    segs = []
    for _ in range(1800):
        x, y = rnd.uniform(0, 40000), rnd.uniform(0, 25000)
        laenge, w = rnd.uniform(50, 4000), rnd.uniform(0, math.pi)
        segs.append(((x, y), (x + laenge * math.cos(w), y + laenge * math.sin(w))))
    assert len(segs) > lf._MAX_SEGMENTE

    def vektor(reihenfolge):
        d = lf._Roh()
        d.segs = list(reihenfolge)
        d.pts = [p for s in d.segs for p in s]
        d.typen["LINE"] = len(d.segs)
        return lf._merkmale_runde1("p", "L", d, plan_factor=1.0,
                                   plan_diag=50000.0,
                                   massstab_verdacht=False).to_vector()

    vorwaerts, rueckwaerts = vektor(segs), vektor(list(reversed(segs)))
    abweichend = [n for n, a, b in zip(FEATURE_NAMES, vorwaerts, rueckwaerts,
                                       strict=True) if a != b]
    assert abweichend == []
