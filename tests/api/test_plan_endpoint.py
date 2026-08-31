"""api POST /plan — Nordstern-Naht: DXF hoch → Notbeleuchtungs-DXF zurück (Slice 5).

Fährt die Engine über HTTP gegen die Fake-Provider (wie der E2E-Durchstich), damit die
Auslieferungs-Schicht grün ist, bevor die echten Provider (Selman #13/Enis #6) gemergt
sind. Tausch echt↔Fake läuft über `create_app(bundle_factory=…)`.
"""
import json

from fastapi.testclient import TestClient

from fakes import (
    build_fake_bundle,
    build_fake_bundle_mit_lb,
    build_fake_bundle_mit_lb_review,
)
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


def test_plan_mit_lb_uebersteuert_norm():
    # 2. Input: LB schließt Sicherheitsbeleuchtung im STIEGENHAUS aus (Fischa GK4).
    # → die 2 Aufheller-SL fallen weg, nur die 5 RZ bleiben.
    client = TestClient(create_app(bundle_factory=build_fake_bundle_mit_lb))
    r = client.post(
        "/plan",
        files={
            "datei": ("leer.dxf", b"<architekturplan>", "image/vnd.dxf"),
            "lb_datei": ("lb.txt", b"GK4 keine SL im Stiegenhaus", "text/plain"),
        },
        data={"floor": "4OG"},
    )
    assert r.status_code == 200
    summary = json.loads(r.headers["X-Notbeleuchtung"])
    assert summary["by_kind"] == {"rz": 5}          # SL durch LB-Exklusion entfernt
    assert summary["n_symbols"] == 5


def test_plan_ohne_lb_provider_ignoriert_lb_upload():
    # Ohne verdrahteten LB-Provider bleibt eine mitgeschickte LB folgenlos (reine Norm).
    r = _client().post(
        "/plan",
        files={
            "datei": ("leer.dxf", b"x", "image/vnd.dxf"),
            "lb_datei": ("lb.txt", b"egal", "text/plain"),
        },
        data={"floor": "4OG"},
    )
    assert r.status_code == 200
    assert json.loads(r.headers["X-Notbeleuchtung"])["n_symbols"] == 7


def test_plan_format_pdf_liefert_pdf():
    r = _client().post(
        "/plan",
        files={"datei": ("leer.dxf", b"<architekturplan>", "image/vnd.dxf")},
        data={"floor": "4OG", "format": "pdf"},
    )
    assert r.status_code == 200
    assert r.headers["content-type"] == "application/pdf"
    assert r.content[:5] == b"%PDF-"
    assert r.headers["content-disposition"].endswith('filename="4OG_notbeleuchtung.pdf"')


def test_plan_unbekanntes_format_ist_422():
    r = _client().post(
        "/plan",
        files={"datei": ("leer.dxf", b"x", "image/vnd.dxf")},
        data={"floor": "4OG", "format": "svg"},
    )
    assert r.status_code == 422


def test_plan_pdf_mit_plankopf_metadaten():
    # Plankopf-Metadaten (projekt/datum/ersteller) fließen bis in den gerenderten Plan.
    r = _client().post(
        "/plan",
        files={"datei": ("leer.dxf", b"x", "image/vnd.dxf")},
        data={"floor": "4OG", "format": "pdf", "projekt": "Wohnbau X",
              "datum": "2026-08-30", "ersteller": "Leonis"},
    )
    assert r.status_code == 200
    assert r.content[:5] == b"%PDF-"


def test_projekt_mehrere_geschosse_sammel_pdf():
    r = _client().post(
        "/projekt",
        files=[
            ("dateien", ("eg.dxf", b"<eg>", "image/vnd.dxf")),
            ("dateien", ("og.dxf", b"<og>", "image/vnd.dxf")),
        ],
        data={"floors": "EG, 1OG", "projekt_name": "Wohnbau X"},
    )
    assert r.status_code == 200
    assert r.headers["content-type"] == "application/pdf"
    assert r.content[:5] == b"%PDF-"
    summary = json.loads(r.headers["X-Notbeleuchtung"])
    assert summary["n_geschosse"] == 2


def test_projekt_floors_mismatch_ist_422():
    r = _client().post(
        "/projekt",
        files=[("dateien", ("eg.dxf", b"x", "image/vnd.dxf"))],
        data={"floors": "EG, 1OG"},   # 1 Datei, 2 floors
    )
    assert r.status_code == 422


def test_plan_ohne_datei_ist_422():
    # Pflicht-Upload fehlt → FastAPI-Validierung.
    assert _client().post("/plan", data={"floor": "4OG"}).status_code == 422


def test_nicht_verdrahteter_provider_ist_503():
    # Fehlt ein Provider-Package (ImportError aus build_default_bundle), übersetzt die
    # API das in 503. Merge-stabil über eine injizierte Factory getestet — nicht über
    # den aktuellen Scaffold-Zustand der Default-App.
    def broken_factory():
        raise ImportError("normwissen ist noch Scaffold (Enis #6 nicht gemergt)")

    r = TestClient(create_app(bundle_factory=broken_factory)).post(
        "/plan", files={"datei": ("leer.dxf", b"x", "image/vnd.dxf")}, data={"floor": "EG"}
    )
    assert r.status_code == 503


# ── Fail-Closed bis an die API-Grenze ───────────────────────────────────────
#
# Bricht Enis' LB-Parser mit `LbFehler` ab, liefert die Pipeline weiterhin einen Plan
# — aber einen rein NORM-getriebenen: die expliziten LB-Vorgaben sind nicht angewendet.
# Diese Information muss beim Client ankommen. Ohne sie sieht ein Review-Fall exakt aus
# wie ein regulärer Plan, und das Fail-Closed endet an der Auslieferungs-Schicht.
def test_plan_lb_review_kommt_im_header_an():
    client = TestClient(create_app(bundle_factory=build_fake_bundle_mit_lb_review))
    r = client.post(
        "/plan",
        files={
            "datei": ("leer.dxf", b"<architekturplan>", "image/vnd.dxf"),
            "lb_datei": ("lb.pdf", b"%PDF-1.4 unlesbar", "application/pdf"),
        },
        data={"floor": "4OG"},
    )
    # Plan wird geliefert (aktuelle Architekturentscheidung: Norm-Default statt Abbruch) …
    assert r.status_code == 200
    assert len(r.content) > 0
    summary = json.loads(r.headers["X-Notbeleuchtung"])
    assert summary["n_symbols"] == 7          # 5 RZ + 2 SL = reine Norm, keine LB-Exklusion
    # … und der Review-Bedarf ist in der Antwort sichtbar.
    review = summary["lb_review"]
    assert review["status"] == "review_erforderlich"
    assert "manuelle Prüfung" in review["meldung"]
    assert "gekuerzt" not in review           # kurze Meldung → ungekürzt


def test_plan_ohne_review_hat_kein_lb_review_feld():
    """Gegenprobe: die erfolgreiche LB darf das Flag nicht setzen."""
    client = TestClient(create_app(bundle_factory=build_fake_bundle_mit_lb))
    r = client.post(
        "/plan",
        files={
            "datei": ("leer.dxf", b"<architekturplan>", "image/vnd.dxf"),
            "lb_datei": ("lb.txt", b"GK4 keine SL im Stiegenhaus", "text/plain"),
        },
        data={"floor": "4OG"},
    )
    assert "lb_review" not in json.loads(r.headers["X-Notbeleuchtung"])


def test_plan_lange_review_meldung_wird_fuer_den_header_gekuerzt():
    """Die Meldung trägt alle blockierenden Befunde und kann den Header sprengen
    (uvicorn kappt bei ~8 KB, `ensure_ascii` bläht Umlaute auf 6 Zeichen)."""
    lang = "LB erfordert manuelle Prüfung (test.pdf) — " + "bereiche: GARAGE nicht abbildbar; " * 80
    client = TestClient(create_app(
        bundle_factory=lambda: build_fake_bundle_mit_lb_review(lang)))
    r = client.post(
        "/plan",
        files={
            "datei": ("leer.dxf", b"<architekturplan>", "image/vnd.dxf"),
            "lb_datei": ("lb.pdf", b"x", "application/pdf"),
        },
        data={"floor": "4OG"},
    )
    assert r.status_code == 200
    roh = r.headers["X-Notbeleuchtung"]
    assert len(roh.encode("ascii")) < 4096, "Header muss transportierbar bleiben"
    review = json.loads(roh)["lb_review"]
    assert review["gekuerzt"] is True
    assert review["meldung"].startswith("LB erfordert manuelle Prüfung")
    assert review["meldung"].endswith("…")


def test_projekt_lb_review_kommt_im_summary_an():
    """Dieselbe Lücke am Mehr-Geschoss-Endpunkt: eine LB gilt fürs ganze Projekt,
    der Review-Bedarf gehört deshalb auf die oberste Summary-Ebene."""
    client = TestClient(create_app(bundle_factory=build_fake_bundle_mit_lb_review))
    r = client.post(
        "/projekt",
        files=[
            ("dateien", ("eg.dxf", b"<eg>", "image/vnd.dxf")),
            ("dateien", ("og.dxf", b"<og>", "image/vnd.dxf")),
            ("lb_datei", ("lb.pdf", b"x", "application/pdf")),
        ],
        data={"floors": "EG, 1OG"},
    )
    assert r.status_code == 200
    summary = json.loads(r.headers["X-Notbeleuchtung"])
    assert summary["n_geschosse"] == 2
    assert summary["lb_review"]["status"] == "review_erforderlich"
