"""api.main — FastAPI `POST /plan`: leerer Architekturplan (DXF) → Notbeleuchtungsplan.

Die dünne Hülle über `hauptengine.pipeline.run()` (CLAUDE.md-Nordstern: Chat lädt Plan
hoch → bekommt den fertigen Notbeleuchtungsplan zurück). Sie enthält **kein** Fach-
Wissen — sie nimmt den Upload entgegen, ruft die Pipeline und gibt das gerenderte DXF
zurück. Die konkreten Provider (Selman/Enis/Leonis) kommen aus
`registry.build_default_bundle`; über `create_app(bundle_factory=…)` lässt sich das für
Tests gegen die Fakes austauschen (Dependency-Inversion wie im Rest der Engine).

Der 2. Input (Leistungsbeschreibung/LB) ist noch nicht in `pipeline.run()` verdrahtet
(Enis' `LBVorgabe`) — das Feld wird bewusst noch nicht angeboten, bis die Pipeline es
konsumiert.
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
        except NotImplementedError as exc:
            # Registry noch nicht verdrahtet (echte Provider Slice 1/4 offen).
            raise HTTPException(status_code=503, detail=f"Engine noch nicht verdrahtet: {exc}") from exc

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/plan")
    def plan(
        datei: UploadFile = File(..., description="Leerer Architekturplan (DXF)"),
        floor: str = Form("EG", description="Geschoss-Kennung, z.B. '4OG'"),
        bundle: ProviderBundle = Depends(get_bundle),
    ) -> FileResponse:
        """DXF hoch → Notbeleuchtungsplan (DXF) zurück. Summary im `X-Notbeleuchtung`-Header."""
        workdir = Path(tempfile.mkdtemp(prefix="notbel_"))
        cleanup = BackgroundTask(shutil.rmtree, workdir, ignore_errors=True)
        try:
            dxf_in = workdir / (Path(datei.filename or "plan.dxf").name)
            dxf_in.write_bytes(datei.file.read())
            out_path = workdir / f"{floor}_notbeleuchtung.dxf"
            try:
                ergebnis = run(bundle, dxf_path=str(dxf_in), floor=floor, out_path=out_path)
            except Exception as exc:  # Provider-/Render-Fehler → 422, Ursache mitgeben.
                raise HTTPException(status_code=422, detail=f"Plan-Erzeugung fehlgeschlagen: {exc}") from exc
            summary = {k: ergebnis.render_summary[k] for k in _SUMMARY_HEADER_KEYS if k in ergebnis.render_summary}
            return FileResponse(
                out_path,
                media_type="image/vnd.dxf",
                filename=out_path.name,
                headers={"X-Notbeleuchtung": json.dumps(summary, ensure_ascii=True)},
                background=cleanup,
            )
        except HTTPException:
            cleanup()  # Fehlerpfad räumt sofort auf (FileResponse übernimmt das sonst).
            raise

    return app


# Default-App für `uvicorn notbeleuchtung.api.main:app` (echte Provider via Registry).
app = create_app()
