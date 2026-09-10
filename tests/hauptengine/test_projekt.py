"""projekt — Mehr-Geschoss-Orchestrierung + Sammel-PDF."""
from pathlib import Path

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
    assert all(g["n_symbols"] == 11 for g in erg.summary["geschosse"])  # inkl. fachpraxis-Aufheller
    assert all(g["pruefung"] in ("ok", "warnung", "fehler") for g in erg.summary["geschosse"])
    assert erg.combined_pdf is None   # ohne pdf=True kein Sammel-PDF


def test_run_projekt_sammel_pdf(tmp_path):
    pytest.importorskip("matplotlib")
    pytest.importorskip("pypdf")
    erg = run_projekt(build_fake_bundle(), _plaene(), out_dir=tmp_path, pdf=True)
    assert erg.combined_pdf is not None
    pdf = Path(erg.combined_pdf)
    assert pdf.is_file()
    assert pdf.read_bytes()[:5] == b"%PDF-"
    # Ein Blatt je Geschoss.
    from pypdf import PdfReader
    assert len(PdfReader(str(pdf)).pages) == 2
    # Das interne Modelspace-Blatt (PDF-Quelle) wird nach dem Merge entfernt.
    assert not (Path(erg.combined_pdf).parent / "EG_notbeleuchtung.modelspace.dxf").exists()


def test_geliefertes_dxf_ist_layout_blatt(tmp_path):
    """Auslieferung (Owner 2026-09-09): das gelieferte Geschoss-DXF ist das Layout-Blatt
    — Vorlage in Layout1, Viewport exakt 1:50 (in AutoCAD plot-fertig), kein Blatt-Rahmen
    im Modelspace. Die Pipeline setzt den Template-Modus als Standard-Weg."""
    ezdxf = pytest.importorskip("ezdxf")
    erg = run_projekt(build_fake_bundle(), _plaene(), out_dir=tmp_path)
    assert all(o.render_summary.get("viewport_scale") == "1:50" for o in erg.outputs)
    doc = ezdxf.readfile(str(tmp_path / "EG_notbeleuchtung.dxf"))
    layout = doc.layouts.get("Layout1")
    vps = sorted(layout.query("VIEWPORT"),
                 key=lambda v: float(v.dxf.width) * float(v.dxf.height), reverse=True)
    assert float(vps[0].dxf.height) / float(vps[0].dxf.view_height) == pytest.approx(1 / 50, abs=1e-6)
    assert not [e for e in doc.modelspace() if e.dxf.layer == "din_SIBEL_99_titleblock"]


def test_layout_fallback_bei_uebergrossem_plan(tmp_path, monkeypatch):
    """Liefer-Policy: passt der Plan in 1:50 nicht in den Vorlagen-Viewport (G6), bricht
    der Lauf NICHT ab — er fällt auf das Modelspace-Blatt (#115) zurück und macht den
    Maßstab-Verlust im Summary sichtbar (`layout_fallback`)."""
    from notbeleuchtung.hauptengine import pipeline
    from notbeleuchtung.hauptengine.render.dxf_renderer import MassstabPasstNichtFehler

    echt = pipeline.render_dxf

    def falle(*args, template_path=None, **kw):
        if template_path is not None:            # Template-Weg „passt nicht"
            raise MassstabPasstNichtFehler("Modell zu groß für 1:50 (Test)")
        return echt(*args, template_path=None, **kw)

    monkeypatch.setattr(pipeline, "render_dxf", falle)
    erg = run_projekt(build_fake_bundle(), _plaene()[:1], out_dir=tmp_path)
    s = erg.outputs[0].render_summary
    assert "layout_fallback" in s
    assert s["blatt_layout_drawn"] is True       # Modelspace-Blatt statt Layout
    assert "viewport_scale" not in s
    assert (tmp_path / "EG_notbeleuchtung.dxf").is_file()
