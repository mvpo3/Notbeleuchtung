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


def test_dxf_zu_pdf_hell_und_dunkel(tmp_path):
    dxf = _dxf(tmp_path)
    hell = dxf_zu_pdf(dxf, tmp_path / "hell.pdf", dunkel=False, dpi=100)
    dunkel = dxf_zu_pdf(dxf, tmp_path / "dunkel.pdf", dunkel=True, dpi=100)
    assert hell.is_file() and dunkel.is_file()
