"""pdf_export — gerendertes DXF → PDF-Liefer-Dokument."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from notbeleuchtung.hauptengine.contracts import PlatzierungsErgebnis, RaumModell
from notbeleuchtung.hauptengine.render import dxf_zu_pdf, render_dxf

pytest.importorskip("matplotlib")

FIXTURES = Path(__file__).parent.parent / "fixtures"


def _dxf(tmp_path: Path) -> Path:
    platzierung = PlatzierungsErgebnis.model_validate(
        json.loads((FIXTURES / "platzierung_4og.json").read_text(encoding="utf-8"))
    )
    raum = RaumModell.model_validate(
        json.loads((FIXTURES / "raum_modell_4og.json").read_text(encoding="utf-8"))
    )
    out = tmp_path / "plan.dxf"
    render_dxf(platzierung, raum, out)
    return out


def test_dxf_zu_pdf_erzeugt_pdf(tmp_path):
    pdf = dxf_zu_pdf(_dxf(tmp_path), tmp_path / "plan.pdf", dpi=100)
    assert pdf.is_file()
    assert pdf.read_bytes()[:5] == b"%PDF-"   # gültiger PDF-Header
    assert pdf.stat().st_size > 1000


def test_liefer_pdf_ist_1zu50_vektorblatt(tmp_path):
    """Owner 2026-09-09: das Liefer-PDF ist ein echtes 1:50-Vektor-Blatt — Seite =
    Ausschnitt/50 (mm), nicht tight-gecropt — damit man wie in einem CAD-Plan zoomen
    kann. Fest verankert (Referenz MOL_GR-…_1-50, Seite 900×1800 mm)."""
    from pypdf import PdfReader
    pdf = dxf_zu_pdf(_dxf(tmp_path), tmp_path / "blatt.pdf",
                     ausschnitt=(0.0, 0.0, 50000.0, 40000.0), dpi=80)
    mb = PdfReader(str(pdf)).pages[0].mediabox
    w_mm, h_mm = float(mb.width) * 25.4 / 72, float(mb.height) * 25.4 / 72
    # 50000/50=1000, 40000/50=800 mm (+1 % Rand je Seite → ~1020×816)
    assert 1000.0 < w_mm < 1045.0, w_mm
    assert 800.0 < h_mm < 835.0, h_mm

    # massstab=None → altes A3-tight-Verhalten (viel kleiner, NICHT ausschnitt/50)
    klein = dxf_zu_pdf(_dxf(tmp_path), tmp_path / "a3.pdf",
                       ausschnitt=(0.0, 0.0, 50000.0, 40000.0), massstab=None, dpi=80)
    mb2 = PdfReader(str(klein)).pages[0].mediabox
    assert float(mb2.width) * 25.4 / 72 < 600.0


def test_dxf_zu_pdf_hell_und_dunkel(tmp_path):
    dxf = _dxf(tmp_path)
    hell = dxf_zu_pdf(dxf, tmp_path / "hell.pdf", dunkel=False, dpi=100)
    dunkel = dxf_zu_pdf(dxf, tmp_path / "dunkel.pdf", dunkel=True, dpi=100)
    assert hell.is_file() and dunkel.is_file()


def test_hell_export_invertiert_layerfarbe7(tmp_path):
    """Farbe-7-Text (Legende/Plankopf) muss auf weißem Grund schwarz gerendert werden.

    Regression: ohne Farb-Inversion wäre er weiß-auf-weiß = unsichtbar (Legende/
    Stückliste/Plankopf/Prüfbericht fehlten im Liefer-PDF)."""
    import ezdxf
    import matplotlib.image as mpimg

    doc = ezdxf.new("R2018", units=4)
    doc.layers.add("TXT7", color=7)  # weiß/schwarz — muss auf hell invertieren
    doc.modelspace().add_mtext(
        "LEGENDE", dxfattribs={"layer": "TXT7", "char_height": 100.0}
    ).set_location((0.0, 0.0))
    dxf = tmp_path / "farbe7.dxf"
    doc.saveas(str(dxf))
    png = dxf_zu_pdf(dxf, tmp_path / "farbe7.png", dunkel=False, dpi=80)
    arr = mpimg.imread(str(png))[..., :3]
    # Nur Text auf weißem Grund: bei korrekter Inversion existieren dunkle Text-Pixel.
    assert float(arr.min()) < 0.3
