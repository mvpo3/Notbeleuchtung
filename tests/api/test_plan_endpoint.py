"""api POST /plan — Nordstern-Naht: DXF hoch → Notbeleuchtungs-DXF zurück (Slice 5).

Fährt die Engine über HTTP gegen die Fake-Provider (wie der E2E-Durchstich), damit die
Auslieferungs-Schicht grün ist, bevor die echten Provider (Selman #13/Enis #6) gemergt
sind. Tausch echt↔Fake läuft über `create_app(bundle_factory=…)`.
"""
import json

from fastapi.testclient import TestClient

from fakes import build_fake_bundle
from notbeleuchtung.api.main import create_app


def _client() -> TestClient:
    return TestClient(create_app(bundle_factory=build_fake_bundle))


def test_health():
    assert _client().get("/health").json() == {"status": "ok"}


def test_plan_liefert_dxf_zurueck():
    r = _client().post(
        "/plan",
        files={"datei": ("leer.dxf", b"<architekturplan>", "image/vnd.dxf")},
        data={"floor": "4OG"},
    )
    assert r.status_code == 200
    # DXF-Bytes kommen zurück (FakeRaumProvider ignoriert den Upload → 4OG-Fixture).
    assert len(r.content) > 0
    assert r.headers["content-disposition"].endswith('filename="4OG_notbeleuchtung.dxf"')
    # Summary im Header: 7 Symbole (5 RZ + 2 SL), gerendert.
    summary = json.loads(r.headers["X-Notbeleuchtung"])
    assert summary["floor"] == "4OG"
    assert summary["n_symbols"] == 7
    assert summary["by_kind"] == {"rz": 5, "sicherheitsleuchte": 2}
    assert summary["rendered"] is True


def test_plan_ohne_datei_ist_422():
    # Pflicht-Upload fehlt → FastAPI-Validierung.
    assert _client().post("/plan", data={"floor": "4OG"}).status_code == 422


def test_default_app_ohne_provider_ist_503():
    # Default-App nutzt build_default_bundle → NotImplementedError → 503 (noch nicht verdrahtet).
    r = TestClient(create_app()).post(
        "/plan", files={"datei": ("leer.dxf", b"x", "image/vnd.dxf")}, data={"floor": "EG"}
    )
    assert r.status_code == 503
