"""api.main — FastAPI `POST /plan`: leerer Architekturplan (DXF) → Notbeleuchtungsplan.

Die dünne Hülle über `hauptengine.pipeline.run()` (CLAUDE.md-Nordstern: Chat lädt Plan
hoch → bekommt den fertigen Notbeleuchtungsplan zurück). Sie enthält **kein** Fach-
Wissen — sie nimmt den Upload entgegen, ruft die Pipeline und gibt das gerenderte DXF
zurück. Die konkreten Provider (Selman/Enis/Leonis) kommen aus
`registry.build_default_bundle`; über `create_app(bundle_factory=…)` lässt sich das für
Tests gegen die Fakes austauschen (Dependency-Inversion wie im Rest der Engine).

Der 2. Input (Leistungsbeschreibung/LB) ist optional: liegt eine LB bei UND ist ein
LB-Provider verdrahtet (`ProviderBundle.lb`, Enis), parst die Pipeline sie in eine
`LBVorgabe`, die die norm-getriebene Platzierung übersteuert. Ohne LB (oder ohne
LB-Provider) läuft die Engine rein norm-getrieben.

Bricht der LB-Parser fail closed ab (`LbReviewRequired`/`LbNichtLesbar`), liefert die
Pipeline weiterhin einen Plan — aber einen rein norm-getriebenen. Das trägt der
`X-Notbeleuchtung`-Header als `lb_review` nach außen; ohne dieses Feld wäre der Fall
von einem regulären Plan nicht unterscheidbar.
"""
from __future__ import annotations

import json
import shutil
import tempfile
from collections.abc import Callable
from pathlib import Path

from fastapi import Depends, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from pydantic import ValidationError
from starlette.background import BackgroundTask

from notbeleuchtung.hauptengine.contracts import ProjektKontext, ProviderBundle
from notbeleuchtung.hauptengine.dwg_input import OdaKonverterFehlt, stelle_dxf_bereit
from notbeleuchtung.hauptengine.pipeline import run
from notbeleuchtung.hauptengine.projekt import ProjektPlan, run_projekt
from notbeleuchtung.hauptengine.registry import build_default_bundle
from notbeleuchtung.hauptengine.render import dxf_zu_pdf

BundleFactory = Callable[[], ProviderBundle]

# Nur maschinen-lesbare, ASCII-sichere Felder in den Response-Header (kein temp-Pfad).
#
# `lb_review` MUSS dabei sein: die Pipeline setzt es, wenn Enis' LB-Parser fail closed
# abbricht (`LbFehler`). Der Plan wird dann zwar geliefert, aber rein norm-getrieben —
# die expliziten LB-Vorgaben sind NICHT angewendet. Fällt das Feld hier aus der Antwort,
# bekommt der Client (und damit das Chat-Interface) einen normal aussehenden Plan und
# erfährt nichts davon; das Fail-Closed endet dann an der API-Grenze.
#
# `oib` gehört aus demselben Grund dazu: trägt der Request einen ProjektKontext, sagt
# nur dieser Block, ob das Flächen-Trigger-Gate offen/zu war (fail-closed ist sonst
# von „kein OIB-Pfad" nicht unterscheidbar).
_SUMMARY_HEADER_KEYS = ("floor", "n_symbols", "by_kind", "n_raeume", "rendered", "lb_review", "oib")

# HTTP-Header sind längenbegrenzt (uvicorn: ~8 KB je Zeile) und `ensure_ascii` bläht
# Umlaute auf 6 Zeichen. Die Review-Meldung trägt alle blockierenden Befunde und kann
# darum beliebig lang werden — im Header wird sie gekappt, der volle Befund bleibt über
# `LbTextProvider.parse_bericht()` erreichbar.
_LB_REVIEW_MELDUNG_MAX = 600


def _header_summary(render_summary: dict) -> dict:
    """Die Header-tauglichen Felder aus dem Pipeline-Summary — `lb_review` gekürzt."""
    summary = {k: render_summary[k] for k in _SUMMARY_HEADER_KEYS if k in render_summary}
    review = summary.get("lb_review")
    if isinstance(review, dict):
        meldung = str(review.get("meldung", ""))
        summary["lb_review"] = dict(review)
        if len(meldung) > _LB_REVIEW_MELDUNG_MAX:
            summary["lb_review"]["meldung"] = meldung[:_LB_REVIEW_MELDUNG_MAX] + "…"
            summary["lb_review"]["gekuerzt"] = True
    return summary


def _als_dxf(plan_pfad: Path, workdir: Path) -> Path:
    """DWG-Upload direkt im Workdir konvertieren (der räumt sich per BackgroundTask
    auf). Ohne installierten ODA-Konverter ist das eine Deployment-Lücke, kein
    Client-Fehler → 503 statt 422."""
    try:
        return stelle_dxf_bereit(plan_pfad, workdir)
    except OdaKonverterFehlt as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


def _parse_projekt_kontext(raw: str | None) -> ProjektKontext | None:
    """Optionales Form-Feld (JSON) → ProjektKontext; ungültig = 422 mit Ursache.

    Der 3. Input (gebäudeweite Projektfakten für den OIB-Pfad) kommt als JSON-String,
    weil er — anders als Plan/LB — keine Datei ist, sondern strukturierte Angaben des
    Auftraggebers (Nutzungsart, Gebäudeklasse, Fluchtniveau …).
    """
    if raw is None or not raw.strip():
        return None
    try:
        return ProjektKontext.model_validate_json(raw)
    except ValidationError as exc:
        raise HTTPException(
            status_code=422, detail=f"projekt_kontext ungültig: {exc}"
        ) from exc


def create_app(bundle_factory: BundleFactory = build_default_bundle) -> FastAPI:
    """Baut die App. `bundle_factory` bindet die Provider (echt via Registry oder Fake)."""
    app = FastAPI(
        title="Notbeleuchtung",
        version="0.1.0",
        summary="Leerer Architekturplan (DXF) → ÖNorm-Notbeleuchtungsplan (EN 1838).",
    )

    def get_bundle() -> ProviderBundle:
        try:
            return bundle_factory()
        except (NotImplementedError, ImportError) as exc:
            # Ein Provider-Package ist noch Scaffold (Enis' Norm #6 / Selman's Raum #13
            # noch nicht gemergt) → build_default_bundle importiert nicht.
            raise HTTPException(status_code=503, detail=f"Engine noch nicht verdrahtet: {exc}") from exc

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/plan")
    def plan(
        datei: UploadFile = File(..., description="Leerer Architekturplan (DXF oder DWG)"),
        floor: str = Form("EG", description="Geschoss-Kennung, z.B. '4OG'"),
        lb_datei: UploadFile | None = File(None, description="Leistungsbeschreibung (2. Input, optional)"),
        format: str = Form("dxf", description="Ausgabeformat: 'dxf' (CAD) oder 'pdf' (Dokument)"),
        projekt: str | None = Form(None, description="Plankopf: Projektbezeichnung"),
        datum: str | None = Form(None, description="Plankopf: Datum"),
        ersteller: str | None = Form(None, description="Plankopf: Ersteller"),
        projekt_kontext: str | None = Form(
            None, description="ProjektKontext als JSON (3. Input, optional): "
                              "gebäudeweite Fakten für den OIB-Pfad (OIB-RL 2 Tabelle 6)"),
        bundle: ProviderBundle = Depends(get_bundle),
    ) -> FileResponse:
        """DXF (+ optional LB) hoch → Notbeleuchtungsplan zurück (DXF oder PDF). Summary
        im `X-Notbeleuchtung`-Header."""
        if format not in ("dxf", "pdf"):
            raise HTTPException(status_code=422, detail="format muss 'dxf' oder 'pdf' sein")
        kontext = _parse_projekt_kontext(projekt_kontext)
        workdir = Path(tempfile.mkdtemp(prefix="notbel_"))
        cleanup = BackgroundTask(shutil.rmtree, workdir, ignore_errors=True)
        try:
            dxf_in = workdir / (Path(datei.filename or "plan.dxf").name)
            dxf_in.write_bytes(datei.file.read())
            dxf_in = _als_dxf(dxf_in, workdir)
            lb_path: str | None = None
            if lb_datei is not None:
                lb_in = workdir / (Path(lb_datei.filename or "lb").name)
                lb_in.write_bytes(lb_datei.file.read())
                lb_path = str(lb_in)
            out_path = workdir / f"{floor}_notbeleuchtung.dxf"
            plankopf = {k: v for k, v in
                        {"projekt": projekt, "datum": datum, "ersteller": ersteller}.items()
                        if v}
            try:
                ergebnis = run(bundle, dxf_path=str(dxf_in), floor=floor, out_path=out_path,
                               lb_path=lb_path, plankopf=plankopf or None,
                               projekt_kontext=kontext)
            except Exception as exc:  # Provider-/Render-Fehler → 422, Ursache mitgeben.
                raise HTTPException(status_code=422, detail=f"Plan-Erzeugung fehlgeschlagen: {exc}") from exc
            summary = _header_summary(ergebnis.render_summary)
            if format == "pdf":
                try:
                    resp_path = dxf_zu_pdf(out_path, workdir / f"{floor}_notbeleuchtung.pdf")
                except Exception as exc:  # matplotlib fehlt (Extra `render`) o.ä.
                    raise HTTPException(status_code=422, detail=f"PDF-Export fehlgeschlagen: {exc}") from exc
                media = "application/pdf"
            else:
                resp_path = out_path
                media = "image/vnd.dxf"
            return FileResponse(
                resp_path,
                media_type=media,
                filename=resp_path.name,
                headers={"X-Notbeleuchtung": json.dumps(summary, ensure_ascii=True)},
                background=cleanup,
            )
        except HTTPException:
            cleanup()  # Fehlerpfad räumt sofort auf (FileResponse übernimmt das sonst).
            raise

    @app.post("/projekt")
    def projekt(
        dateien: list[UploadFile] = File(..., description="Architekturpläne (DXF), ein Blatt je Geschoss"),
        floors: str = Form(..., description="Geschoss-Kennungen, komma-getrennt in Datei-Reihenfolge"),
        lb_datei: UploadFile | None = File(None, description="Leistungsbeschreibung (2. Input, optional)"),
        projekt_name: str | None = Form(None, description="Plankopf: Projektbezeichnung"),
        projekt_kontext: str | None = Form(
            None, description="ProjektKontext als JSON (3. Input, optional): "
                              "gebäudeweite Fakten für den OIB-Pfad (OIB-RL 2 Tabelle 6)"),
        bundle: ProviderBundle = Depends(get_bundle),
    ) -> FileResponse:
        """Mehrere Geschoss-DXF (+ optional LB) → ein Sammel-PDF (ein Blatt je Geschoss)."""
        kontext = _parse_projekt_kontext(projekt_kontext)
        floor_list = [f.strip() for f in floors.split(",") if f.strip()]
        if len(floor_list) != len(dateien):
            raise HTTPException(status_code=422,
                                detail=f"{len(dateien)} Dateien, aber {len(floor_list)} floors")
        workdir = Path(tempfile.mkdtemp(prefix="notbel_proj_"))
        cleanup = BackgroundTask(shutil.rmtree, workdir, ignore_errors=True)
        try:
            plaene = []
            for datei, floor in zip(dateien, floor_list):
                dxf_in = workdir / f"{floor}_{Path(datei.filename or 'plan.dxf').name}"
                dxf_in.write_bytes(datei.file.read())
                dxf_in = _als_dxf(dxf_in, workdir)
                plaene.append(ProjektPlan(dxf_path=str(dxf_in), floor=floor))
            lb_path = None
            if lb_datei is not None:
                lb_in = workdir / (Path(lb_datei.filename or "lb").name)
                lb_in.write_bytes(lb_datei.file.read())
                lb_path = str(lb_in)
            plankopf = {"projekt": projekt_name} if projekt_name else None
            try:
                erg = run_projekt(bundle, plaene, out_dir=workdir, lb_path=lb_path,
                                  plankopf=plankopf, pdf=True, projekt_kontext=kontext)
            except Exception as exc:
                raise HTTPException(status_code=422, detail=f"Projekt-Erzeugung fehlgeschlagen: {exc}") from exc
            return FileResponse(
                erg.combined_pdf,
                media_type="application/pdf",
                filename="projekt_notbeleuchtung.pdf",
                headers={"X-Notbeleuchtung": json.dumps(erg.summary, ensure_ascii=True)},
                background=cleanup,
            )
        except HTTPException:
            cleanup()
            raise

    return app


# Default-App für `uvicorn notbeleuchtung.api.main:app` (echte Provider via Registry).
app = create_app()
