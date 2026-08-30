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
"""
from __future__ import annotations

import json
import shutil
import tempfile
from collections.abc import Callable
from pathlib import Path

from fastapi import Depends, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from starlette.background import BackgroundTask

from notbeleuchtung.hauptengine.contracts import ProviderBundle
from notbeleuchtung.hauptengine.pipeline import run
from notbeleuchtung.hauptengine.registry import build_default_bundle
from notbeleuchtung.hauptengine.render import dxf_zu_pdf

BundleFactory = Callable[[], ProviderBundle]

# Nur maschinen-lesbare, ASCII-sichere Felder in den Response-Header (kein temp-Pfad).
_SUMMARY_HEADER_KEYS = ("floor", "n_symbols", "by_kind", "n_raeume", "rendered")


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
        datei: UploadFile = File(..., description="Leerer Architekturplan (DXF)"),
        floor: str = Form("EG", description="Geschoss-Kennung, z.B. '4OG'"),
        lb_datei: UploadFile | None = File(None, description="Leistungsbeschreibung (2. Input, optional)"),
        format: str = Form("dxf", description="Ausgabeformat: 'dxf' (CAD) oder 'pdf' (Dokument)"),
        bundle: ProviderBundle = Depends(get_bundle),
    ) -> FileResponse:
        """DXF (+ optional LB) hoch → Notbeleuchtungsplan zurück (DXF oder PDF). Summary
        im `X-Notbeleuchtung`-Header."""
        if format not in ("dxf", "pdf"):
            raise HTTPException(status_code=422, detail="format muss 'dxf' oder 'pdf' sein")
        workdir = Path(tempfile.mkdtemp(prefix="notbel_"))
        cleanup = BackgroundTask(shutil.rmtree, workdir, ignore_errors=True)
        try:
            dxf_in = workdir / (Path(datei.filename or "plan.dxf").name)
            dxf_in.write_bytes(datei.file.read())
            lb_path: str | None = None
            if lb_datei is not None:
                lb_in = workdir / (Path(lb_datei.filename or "lb").name)
                lb_in.write_bytes(lb_datei.file.read())
                lb_path = str(lb_in)
            out_path = workdir / f"{floor}_notbeleuchtung.dxf"
            try:
                ergebnis = run(bundle, dxf_path=str(dxf_in), floor=floor, out_path=out_path, lb_path=lb_path)
            except Exception as exc:  # Provider-/Render-Fehler → 422, Ursache mitgeben.
                raise HTTPException(status_code=422, detail=f"Plan-Erzeugung fehlgeschlagen: {exc}") from exc
            summary = {k: ergebnis.render_summary[k] for k in _SUMMARY_HEADER_KEYS if k in ergebnis.render_summary}
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

    return app


# Default-App für `uvicorn notbeleuchtung.api.main:app` (echte Provider via Registry).
app = create_app()
