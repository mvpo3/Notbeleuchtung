"""OIB-Stufe im gezeichneten Prüfvermerk (Ausgabelücken-Befund 2026-09-07).

Testet bis zur TATSÄCHLICH GELIEFERTEN Ausgabe: die Pipeline läuft mit
OIB-Pfad und out_path, danach wird die geschriebene DXF gelesen und der
Vermerk-Text geprüft — nicht nur ein Summary-Flag.

Auslieferung 2026-09-09: das gelieferte DXF ist das Layout-Blatt (Vorlage in
Layout1, Viewport 1:50). Der dynamische Prüfvermerk (Enis Regel 13) wird auf dem
Modelspace-Blatt der PDF-Quelle (`<name>.modelspace.dxf`, `pdf_quelle=True`)
gezeichnet — die statische Layout-Vorlage trägt ihn nicht. Das `pruefung`-Dict
(inkl. `oib_stufen`) bleibt unverändert im Summary/API.
"""
import json

import ezdxf

from fakes import build_fake_bundle_mit_oib
from notbeleuchtung.hauptengine.contracts import Gebaeudeteil, ProjektKontext
from notbeleuchtung.hauptengine.pipeline import run

_KONTEXT = ProjektKontext(
    jurisdiction="AT",
    gebaeudeteile=[Gebaeudeteil(id="teil_1", nutzungsart="SONSTIGES_GEBAEUDE")],
)


def _texte(dxf_pfad) -> list[str]:
    doc = ezdxf.readfile(dxf_pfad)
    return [e.dxf.text for e in doc.modelspace().query("TEXT")]


def test_oib_stufe_steht_im_gezeichneten_vermerk(tmp_path):
    out = run(
        build_fake_bundle_mit_oib(), "<fake>", "4OG",
        out_path=tmp_path / "plan.dxf", projekt_kontext=_KONTEXT, pdf_quelle=True,
    )
    # Prüfvermerk lebt auf dem Modelspace-Blatt der PDF-Quelle (Modus 1).
    stufen_zeilen = [t for t in _texte(tmp_path / "plan.modelspace.dxf")
                     if t.startswith("OIB-RL2-Stufe:")]
    assert stufen_zeilen == ["OIB-RL2-Stufe: teil_1: eingeschraenkt"]
    # Und der Bericht selbst trägt den Block (Quelle der Vermerk-Zeile) — im Summary.
    assert out.render_summary["pruefung"]["oib_stufen"] == {"teil_1": "eingeschraenkt"}


def test_ohne_oib_pfad_keine_stufen_zeile(tmp_path):
    out = run(build_fake_bundle_mit_oib(), "<fake>", "4OG", out_path=tmp_path / "plan.dxf")
    assert not any(t.startswith("OIB-RL2-Stufe:") for t in _texte(tmp_path / "plan.dxf"))
    assert "oib_stufen" not in out.render_summary["pruefung"]


def test_pruefung_dict_ist_json_serialisierbar(tmp_path):
    """API-Naht: der erweiterte Bericht muss weiter durch json.dumps gehen."""
    out = run(
        build_fake_bundle_mit_oib(), "<fake>", "4OG",
        out_path=tmp_path / "plan.dxf", projekt_kontext=_KONTEXT,
    )
    json.dumps(out.render_summary["pruefung"])


def test_stufen_zeile_liegt_zwischen_kopf_und_details(tmp_path):
    """Layout-Invariante der Bande: PRÜFVERMERK-Kopf oben, Stufen-Zeile darunter,
    Details-Verweis zuunterst — die neue Zeile schiebt nichts aus der Bande,
    sondern reiht sich in die bestehende y-Ordnung ein."""
    run(
        build_fake_bundle_mit_oib(), "<fake>", "4OG",
        out_path=tmp_path / "plan.dxf", projekt_kontext=_KONTEXT, pdf_quelle=True,
    )
    doc = ezdxf.readfile(tmp_path / "plan.modelspace.dxf")
    y = {}
    for e in doc.modelspace().query("TEXT"):
        for key, praefix in (("kopf", "PRÜFVERMERK"), ("stufe", "OIB-RL2-Stufe:"),
                             ("details", "Details:")):
            if e.dxf.text.startswith(praefix):
                y[key] = e.get_placement()[1].y
    assert set(y) == {"kopf", "stufe", "details"}
    assert y["kopf"] > y["stufe"] > y["details"]
