"""Wohnbau-Durchstich — der Owner-abgenommene Blatt-Ausgabeweg als Regressionsnetz.

Die Fixtures `raum_modell_wohnbau_{eg,1og,dg}.json` sind aus den Owner-
abgenommenen Outputs `output/wohnbau_v8_*.dxf` rekonstruiert (Nacht-Session
2026-09-05, Blatt-Modus-Fixierung #115; der Generator spec_builder_v8.py lag im
Session-Scratchpad und ist verloren — die gezeichneten Räume/Türen/Segmente
tragen aber das volle RaumModell). Verifiziert: die Reproduktion trifft die
v8-RZ-Muster exakt (EG 3×unten+1×links · OG/DG je 2+2); SL-Zahlen weichen
gewollt ab (Engine-Evolution #117 C-Ebene + #119 optik_aus_achse).

Damit bricht ab jetzt CI — nicht erst der Owner in AutoCAD — wenn jemand den
Blatt-Modus oder die Platzierung an diesem Gebäude kippt.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from notbeleuchtung.hauptengine.contracts import RaumModell
from notbeleuchtung.hauptengine.registry import default_photometrie
from notbeleuchtung.hauptengine.render import render_dxf
from notbeleuchtung.hauptengine.validierung import pruefbericht
from notbeleuchtung.normwissen import En1838NormProvider
from notbeleuchtung.platzierung import NotlichtPlatzierer
from notbeleuchtung.symbols import library

FIXTURES = Path(__file__).parent.parent / "fixtures"
FLOORS = ("eg", "1og", "dg")

#: Ist-Stand-Bänder (heutige Werte: EG 4 RZ + 4 SL · 1OG/DG je 4 RZ + 7 SL).
#: Kippt ein Band → Platzierungs-Verhalten am Owner-Gebäude hat sich geändert:
#: bewusst? Dann Band + Begründung hier nachziehen (wie Mollgasse-E2E).
RZ_BAND = (3, 6)
SL_BAND = {"eg": (3, 8), "1og": (5, 10), "dg": (5, 10)}


@pytest.fixture(autouse=True)
def _fresh_cache():
    library.reset_cache()
    yield
    library.reset_cache()


def _lauf(floor: str, tmp_path: Path):
    raum = RaumModell.model_validate(json.loads(
        (FIXTURES / f"raum_modell_wohnbau_{floor}.json").read_text(encoding="utf-8")
    ))
    i_cd_fn, befund = default_photometrie(optik_aus_achse=True)
    norm = En1838NormProvider()
    erg = NotlichtPlatzierer(i_cd_fn=i_cd_fn).place(raum, norm)
    pruef = pruefbericht(raum, erg, norm=norm, photometrie=befund)
    out = tmp_path / f"wohnbau_{floor}.dxf"
    summary = render_dxf(erg, raum, out, pruefung=pruef, photometrie=befund)
    return raum, erg, pruef, summary, out


@pytest.mark.parametrize("floor", FLOORS)
def test_symbolzahlen_im_band(floor, tmp_path):
    _raum, erg, _pruef, _summary, _out = _lauf(floor, tmp_path)
    rz = sum(1 for p in erg.platzierungen if p.kind == "rz")
    sl = sum(1 for p in erg.platzierungen if p.kind == "sicherheitsleuchte")
    lo, hi = SL_BAND[floor]
    assert RZ_BAND[0] <= rz <= RZ_BAND[1], f"{floor}: RZ={rz} außerhalb {RZ_BAND}"
    assert lo <= sl <= hi, f"{floor}: SL={sl} außerhalb ({lo},{hi})"


@pytest.mark.parametrize("floor", FLOORS)
def test_blatt_modus_und_owner_fixierung(floor, tmp_path):
    """#115: das Blatt trägt alles — keine Zusatz-Boxen; #118: Prüfvermerk-Feld."""
    raum, _erg, _pruef, summary, out = _lauf(floor, tmp_path)
    ezdxf = pytest.importorskip("ezdxf")
    assert summary["blatt_layout_drawn"] is True
    assert summary["pruefbericht_drawn"] is False
    assert summary["stueckliste_drawn"] is False
    assert summary["stromkreis_belegung_drawn"] is False
    assert summary["pruefvermerk_am_blatt"] is True
    assert summary["tueren_drawn"] == len(raum.tueren)
    assert summary["fluchtweg_segmente_drawn"] == len(raum.zirkulation.segmente)
    msp = ezdxf.readfile(str(out)).modelspace()
    texte = [e.dxf.text for e in msp.query("TEXT")]
    assert any("PRÜFVERMERK" in t for t in texte)
    # Owner-Fixierung: PROJEKT-Platzhaltertext bleibt leer.
    assert not any("MVP-Projekt" in t for t in texte)
    blatt_syms = [e for e in msp.query("INSERT") if not e.has_xdata("NOTBELEUCHTUNG")]
    assert len(blatt_syms) >= 5, "Blatt-Legende nicht bestückt"


def test_eg_rz_muster_und_aussenleuchte(tmp_path):
    """Die abgenommenen EG-Eigenschaften: RZ-Richtungsmuster (3×unten + 1×links,
    exakt wie v8) + Außenleuchte §4.1.2 b vor dem final_exit."""
    raum, erg, _pruef, _summary, _out = _lauf("eg", tmp_path)
    rz_keys = sorted(p.catalog_key for p in erg.platzierungen if p.kind == "rz")
    assert rz_keys.count("notlicht_ks_stiege_unten") == 3
    assert rz_keys.count("notlicht_ks_stiege_links") == 1
    (exit_,) = [a for a in raum.ausgaenge if a.typ == "final_exit"]
    sl = [p for p in erg.platzierungen if p.kind == "sicherheitsleuchte"]
    naechste = min(
        ((p.xy_mm[0] - exit_.xy_mm[0]) ** 2 + (p.xy_mm[1] - exit_.xy_mm[1]) ** 2) ** 0.5
        for p in sl
    )
    assert naechste < 2000.0, "keine SL nahe dem final_exit (Außenleuchte §4.1.2 b)"


@pytest.mark.parametrize("floor", FLOORS)
def test_pruefstatus_nicht_fehler(floor, tmp_path):
    """Regressionsnetz, kein Norm-Golden: `fehler` am Owner-Gebäude wäre ein
    Engine-Regress. (Regel 15 ist mit optik_aus_achse `ok`, #119.)"""
    _raum, _erg, pruef, _summary, _out = _lauf(floor, tmp_path)
    assert pruef["status"] in ("ok", "warnung"), pruef["status"]
    regel15 = [b for b in pruef["befunde"] if "Photometrie-Grundlage" in b["regel"]]
    assert regel15 and regel15[0]["status"] == "ok"


def test_pdf_export_smoke(tmp_path):
    """#115-PDF-Fallen (Logo-Flip, extent-Crash, Ausschnitt) bleiben tot."""
    pytest.importorskip("matplotlib")
    from notbeleuchtung.hauptengine.render.pdf_export import dxf_zu_pdf

    _raum, _erg, _pruef, _summary, out = _lauf("eg", tmp_path)
    pdf = out.with_suffix(".pdf")
    dxf_zu_pdf(str(out), str(pdf))
    assert pdf.is_file() and pdf.stat().st_size > 10_000
