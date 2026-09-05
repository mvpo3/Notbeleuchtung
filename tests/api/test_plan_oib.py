"""api POST /plan + /projekt — 3. Input `projekt_kontext` (JSON) → OIB-Pfad.

Der ProjektKontext kommt als Form-Feld (JSON-String), weil er keine Datei ist,
sondern strukturierte Auftraggeber-Fakten. Gültig → Pipeline fährt den OIB-Pfad
und der `oib`-Block (Stufen + Gate) landet im X-Notbeleuchtung-Header; ungültig →
422 mit Ursache; fehlend → kein `oib`-Block (bisheriges Verhalten).
"""
import json

from fastapi.testclient import TestClient

from fakes import build_fake_bundle, build_fake_bundle_mit_oib
from notbeleuchtung.api.main import create_app

_KONTEXT_JSON = json.dumps({
    "jurisdiction": "AT",
    "gebaeudeteile": [{"id": "teil_1", "nutzungsart": "SONSTIGES_GEBAEUDE"}],
})


def _post_plan(client: TestClient, **extra_data) -> object:
    return client.post(
        "/plan",
        files={"datei": ("leer.dxf", b"<architekturplan>", "image/vnd.dxf")},
        data={"floor": "4OG", **extra_data},
    )


def test_plan_mit_projekt_kontext_traegt_oib_block():
    client = TestClient(create_app(bundle_factory=build_fake_bundle_mit_oib))
    r = _post_plan(client, projekt_kontext=_KONTEXT_JSON)
    assert r.status_code == 200
    summary = json.loads(r.headers["X-Notbeleuchtung"])
    assert summary["oib"]["stufen"] == {"teil_1": "eingeschraenkt"}
    # Scope je Raum statt Gate-Flag (Enis 05.09.): ohne raum_referenzen ungeklärt.
    assert summary["oib"]["sanitaer_scope"]["anwendbar"] == 0
    # Der Plan selbst ist unverändert (4OG-Fixture hat keine Flächen-Schwellen).
    assert summary["by_kind"] == {"rz": 5, "sicherheitsleuchte": 2}


def test_plan_ohne_kontext_kein_oib_block():
    client = TestClient(create_app(bundle_factory=build_fake_bundle_mit_oib))
    r = _post_plan(client)
    assert r.status_code == 200
    assert "oib" not in json.loads(r.headers["X-Notbeleuchtung"])


def test_plan_kontext_ohne_oib_provider_laeuft_wie_bisher():
    client = TestClient(create_app(bundle_factory=build_fake_bundle))
    r = _post_plan(client, projekt_kontext=_KONTEXT_JSON)
    assert r.status_code == 200
    assert "oib" not in json.loads(r.headers["X-Notbeleuchtung"])


def test_plan_ungueltiger_kontext_ist_422_mit_ursache():
    client = TestClient(create_app(bundle_factory=build_fake_bundle_mit_oib))
    r = _post_plan(client, projekt_kontext='{"gebaeudeteile": [{"id": ""}]}')
    assert r.status_code == 422
    assert "projekt_kontext ungültig" in r.json()["detail"]


def test_projekt_mit_kontext_traegt_oib_block_topleve():
    client = TestClient(create_app(bundle_factory=build_fake_bundle_mit_oib))
    r = client.post(
        "/projekt",
        files=[("dateien", ("eg.dxf", b"<plan>", "image/vnd.dxf"))],
        data={"floors": "4OG", "projekt_kontext": _KONTEXT_JSON},
    )
    # PDF-Export braucht das Render-Extra; ohne matplotlib wäre es 422 — dann
    # überspringen statt falsch-rot (gleiches Muster wie Render-Skips).
    if r.status_code == 422 and "PDF" in r.json().get("detail", ""):
        import pytest
        pytest.skip("Render-Extra (matplotlib/pypdf) nicht installiert")
    assert r.status_code == 200
    summary = json.loads(r.headers["X-Notbeleuchtung"])
    assert summary["oib"]["stufen"] == {"teil_1": "eingeschraenkt"}
