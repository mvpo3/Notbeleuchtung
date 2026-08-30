"""projekt — Mehr-Geschoss-Orchestrierung + Sammel-PDF."""
import pytest

from fakes import build_fake_bundle
from notbeleuchtung.hauptengine.projekt import ProjektPlan, run_projekt


def _plaene():
    # FakeRaumProvider ignoriert den Pfad → beide „Geschosse" rendern die 4OG-Fixture.
    return [ProjektPlan(dxf_path="<fake>", floor="EG"),
            ProjektPlan(dxf_path="<fake>", floor="1OG")]


def test_run_projekt_pro_geschoss(tmp_path):
    erg = run_projekt(build_fake_bundle(), _plaene(), out_dir=tmp_path)
    assert erg.summary["n_geschosse"] == 2
    assert len(erg.outputs) == 2
    # Je Geschoss ein DXF + eine Prüfung.
    assert (tmp_path / "EG_notbeleuchtung.dxf").is_file()
    assert (tmp_path / "1OG_notbeleuchtung.dxf").is_file()
    assert all(g["n_symbols"] == 7 for g in erg.summary["geschosse"])
    assert all(g["pruefung"] in ("ok", "warnung", "fehler") for g in erg.summary["geschosse"])
    assert erg.combined_pdf is None   # ohne pdf=True kein Sammel-PDF


def test_run_projekt_sammel_pdf(tmp_path):
    pytest.importorskip("matplotlib")
    pytest.importorskip("pypdf")
    erg = run_projekt(build_fake_bundle(), _plaene(), out_dir=tmp_path, pdf=True)
    assert erg.combined_pdf is not None
    from pathlib import Path
    pdf = Path(erg.combined_pdf)
    assert pdf.is_file()
    assert pdf.read_bytes()[:5] == b"%PDF-"
    # Ein Blatt je Geschoss.
    from pypdf import PdfReader
    assert len(PdfReader(str(pdf)).pages) == 2
