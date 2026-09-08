"""Layout-Vorlage (Slice 3.4) — Plan im Layout1-Viewport, exakt 1:50.

Hermetisch gegen die ECHTE Repo-Vorlage `Vorlagen-Legende/Notbeleuchtungspläne-
Vorlage.dxf` (Owner-Asset, versioniert). Befund aus dem Inventar: der Vorlagen-
Plankopf besteht aus reinen TEXT-Entities — es existieren KEINE ATTRIB-Tags,
also wird nichts befüllt und `plankopf_tags` ist leer (der Prompt-Test
„MASSSTAB-Attribut enthält 1:50" ist an dieser Vorlage nicht erfüllbar;
dokumentierte Abweichung, kein stiller Skip).
"""
import json
from pathlib import Path

import ezdxf
import pytest

from notbeleuchtung.hauptengine.contracts import (
    PlatzierungsErgebnis,
    RaumModell,
)
from notbeleuchtung.hauptengine.render.dxf_renderer import (
    MassstabPasstNichtFehler,
    render_dxf,
)
from notbeleuchtung.symbols import load_symbol_mapping

FIXTURES = Path(__file__).parents[1] / "fixtures"
VORLAGE = Path(__file__).parents[2] / "Vorlagen-Legende" / "Notbeleuchtungspläne-Vorlage.dxf"


def _lade_4og():
    raum = RaumModell.model_validate(
        json.loads((FIXTURES / "raum_modell_4og.json").read_text(encoding="utf-8")))
    plzg = PlatzierungsErgebnis.model_validate(
        json.loads((FIXTURES / "platzierung_4og.json").read_text(encoding="utf-8")))
    return raum, plzg


def _render(tmp_path, raum=None, plzg=None):
    if raum is None:
        raum, plzg = _lade_4og()
    out = tmp_path / "layout.dxf"
    summary = render_dxf(plzg, raum, out, template_path=VORLAGE)
    return out, summary


def test_viewport_exakt_1_zu_50(tmp_path):
    out, summary = _render(tmp_path)
    assert summary["layout"] == "Layout1"
    assert summary["viewport_scale"] == "1:50"
    assert summary["fit"] is True
    doc = ezdxf.readfile(out)
    layout = doc.layouts.get("Layout1")
    vps = sorted(layout.query("VIEWPORT"),
                 key=lambda v: float(v.dxf.width) * float(v.dxf.height), reverse=True)
    vp = vps[0]
    assert float(vp.dxf.height) / float(vp.dxf.view_height) == pytest.approx(1 / 50, abs=1e-6)
    # Viewport zeigt aufs Modell-Zentrum.
    import ezdxf.bbox as ezbbox
    ext = ezbbox.extents(doc.modelspace(), fast=True)
    assert vp.dxf.view_center_point.x == pytest.approx((ext.extmin.x + ext.extmax.x) / 2, abs=1.0)


def test_nb_inserts_nur_im_modelspace(tmp_path):
    out, _ = _render(tmp_path)
    doc = ezdxf.readfile(out)
    nb_bloecke = {e["block_name"].strip().lower() for e in load_symbol_mapping().values()}
    msp_nb = [e for e in doc.modelspace().query("INSERT")
              if e.dxf.name.strip().lower() in nb_bloecke]
    assert msp_nb, "Platzierungs-INSERTs fehlen im Modelspace"
    # Layout1 behält exakt die 9 Owner-INSERTs der Vorlagen-Legende — der Render
    # fügt dem Paperspace KEINE Symbole hinzu.
    layout_inserts = list(doc.layouts.get("Layout1").query("INSERT"))
    assert len(layout_inserts) == 9


def test_vorlage_hat_keine_attribs_tags_leer(tmp_path):
    _, summary = _render(tmp_path)
    assert summary["plankopf_tags"] == []


def test_uebergrosses_modell_wechselt_nicht_still_den_massstab(tmp_path):
    raum, plzg = _lade_4og()
    gross = raum.model_copy(deep=True)
    # Raum künstlich auf 200 m aufblasen → passt in 1:50 in kein Planfenster.
    riesig = [(0.0, 0.0), (200000.0, 0.0), (200000.0, 200000.0), (0.0, 200000.0)]
    gross.raeume[0].polygon_mm = riesig
    with pytest.raises(MassstabPasstNichtFehler):
        render_dxf(plzg, gross, tmp_path / "zu_gross.dxf", template_path=VORLAGE)


def test_ohne_template_path_unveraendert(tmp_path):
    """Regression: Default-Pfad (Blatt-Modus #115) bleibt bit-kompatibel im Summary."""
    raum, plzg = _lade_4og()
    summary = render_dxf(plzg, raum, tmp_path / "default.dxf")
    assert "viewport_scale" not in summary
    assert summary["rendered"] is True
