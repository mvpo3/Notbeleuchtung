"""dwg_input — DWG-Pläne via ODA File Converter (Discovery + Konvertierung + Nähte).

Unit-Tests laufen überall (Discovery gegen gefakte Verzeichnisbäume, Fehlerpfad
gemonkeypatcht). Die Integrations-Tests brauchen den echten ODA File Converter —
erstes **skip-if-Tool**-Pattern im Repo (analog zum skip-if-Asset der E2E-Netze):
ohne installierten Konverter werden sie übersprungen, nie rot.
"""
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from fakes import build_fake_bundle
from notbeleuchtung.api.main import create_app
from notbeleuchtung.hauptengine import dwg_input
from notbeleuchtung.hauptengine.dwg_input import (
    OdaKonverterFehlt,
    finde_oda_exe,
    oda_verfuegbar,
    stelle_dxf_bereit,
)

# Getracktes DWG-Asset im Repo (Wissens-Gap aus PROFI_DIN_PLAN_UND_VORSCHRIFTEN.md).
STROMKREIS_DWG = Path("knowledge/sonstiges Wissen Notbeleuchtung/din Planungsunterstützung_Stromkreisnummer.dwg")


def _skip_ohne_oda() -> None:
    if not oda_verfuegbar():  # pragma: no cover — Umgebung ohne ODA-Konverter
        pytest.skip("ODA File Converter nicht installiert")


# ---- Unit: Passthrough + Fehlerpfad ----

def test_dxf_geht_unveraendert_durch(tmp_path):
    """DXF-Input berührt den Konverter nie — bit-identisches Verhalten zum Bestand."""
    dxf = tmp_path / "plan.DXF"
    dxf.write_bytes(b"egal")
    assert stelle_dxf_bereit(dxf, tmp_path / "work") == dxf


def test_dwg_ohne_konverter_klarer_fehler(tmp_path, monkeypatch):
    monkeypatch.setattr(dwg_input, "oda_verfuegbar", lambda: False)
    dwg = tmp_path / "plan.dwg"
    dwg.write_bytes(b"egal")
    with pytest.raises(OdaKonverterFehlt, match="ODA File Converter"):
        stelle_dxf_bereit(dwg, tmp_path)


# ---- Unit: Discovery der versionierten Installations-Ordner ----

def _fake_installation(wurzel: Path, ordner: str) -> Path:
    exe = wurzel / ordner / "ODAFileConverter.exe"
    exe.parent.mkdir(parents=True)
    exe.write_bytes(b"")
    return exe


def test_discovery_waehlt_neueste_version(tmp_path):
    oda = tmp_path / "ODA"
    _fake_installation(oda, "ODAFileConverter 25.4.0")
    neueste = _fake_installation(oda, "ODAFileConverter 27.1.0")
    assert finde_oda_exe(such_wurzeln=[oda]) == neueste


def test_discovery_ohne_installation_ist_none(tmp_path):
    assert finde_oda_exe(such_wurzeln=[tmp_path / "gibts_nicht"]) is None


# ---- Naht API: DWG-Upload ohne Konverter = Deployment-Lücke → 503 ----

def test_api_dwg_ohne_konverter_503(monkeypatch):
    monkeypatch.setattr(dwg_input, "oda_verfuegbar", lambda: False)
    client = TestClient(create_app(bundle_factory=build_fake_bundle))
    r = client.post("/plan", files={"datei": ("plan.dwg", b"<dwg>", "application/octet-stream")})
    assert r.status_code == 503
    assert "ODA File Converter" in r.json()["detail"]


# ---- Integration (skip-if-Tool): echte Konvertierung ----

def test_konvertiert_repo_dwg_und_ezdxf_liest(tmp_path):
    """Das getrackte Stromkreisnummer-DWG wird konvertiert und ist ezdxf-lesbar."""
    _skip_ohne_oda()
    if not STROMKREIS_DWG.exists():  # pragma: no cover — Asset fehlt (Sparse-Checkout)
        pytest.skip(f"DWG-Asset nicht vorhanden: {STROMKREIS_DWG}")
    import ezdxf

    dxf = stelle_dxf_bereit(STROMKREIS_DWG, tmp_path)
    assert dxf.suffix == ".dxf" and dxf.parent == tmp_path
    doc = ezdxf.readfile(dxf)
    assert len(doc.modelspace()) > 0


def test_pipeline_nimmt_dwg_wie_dxf(tmp_path):
    """`run()` mit .dwg liefert dasselbe Ergebnis wie mit .dxf (Fake ignoriert den
    Inhalt — geprüft wird die Konvertier-Naht + das Aufräumen des Konvertats)."""
    _skip_ohne_oda()
    import ezdxf
    from ezdxf.addons import odafc

    from notbeleuchtung.hauptengine.pipeline import run

    doc = ezdxf.new("R2018")
    doc.modelspace().add_line((0, 0), (1000, 0))
    dwg = tmp_path / "mini.dwg"
    odafc.export_dwg(doc, dwg)

    ergebnis = run(build_fake_bundle(), str(dwg), "4OG")
    assert ergebnis.render_summary["n_symbols"] == 7  # 4OG-Golden: 5 RZ + 2 SL
    # Konvertat lag im TemporaryDirectory der Pipeline — nichts bleibt zurück.
    assert list(tmp_path.glob("*.dxf")) == []
