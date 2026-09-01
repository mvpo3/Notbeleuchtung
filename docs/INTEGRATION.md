# Hauptengine in eine eigene App integrieren

Für Host-/Demo-Apps, die die Notbeleuchtungs-Engine aufrufen wollen (Raumerkennung +
Platzierung + Norm-/LB-Wissen). Die Engine ist ein **installierbares Python-Paket** —
sie ist komplett auf `main`, nichts muss separat übergeben werden: **`git pull`** genügt.

## 1. Installieren

Im Klon des Repos (die Host-App nimmt das Paket als Dependency oder editable-Install):

```
python -m venv .venv
.venv/Scripts/python -m pip install -e ".[render]"    # +render = PDF-Export (matplotlib)
```

Das Norm-/LB-Wissen ist Teil des Pakets und wird automatisch geladen:
- `src/notbeleuchtung/normwissen/data/*.yaml` — EN 1838 / ÖNorm-Grundwerte, Raumtyp-Regeln,
  Platzierungs-Regelmatrix, OIB, LB-Extraktion, Sonderstellen.
- `knowledge/extracted/` — Digests & extrahierte Vorschriften (Referenz, nicht Laufzeit).

## 2. Der eine Einstiegspunkt

```python
from notbeleuchtung.hauptengine.pipeline import run
from notbeleuchtung.hauptengine.registry import build_default_bundle

bundle = build_default_bundle()          # Raumerkennung (Selman) + Platzierung (Leonis) + Norm + LB (Enis)
out = run(
    bundle,
    dxf_path="Projekte/Mollgasse/Erdgeschoß.dxf",
    floor="EG",
    out_path="output/plan.dxf",          # schreibt das Notbeleuchtungs-DXF; None → nur Summary
    lb_path=None,                        # optional: Leistungsbeschreibung (PDF/TXT), übersteuert Norm
)
```

`build_default_bundle()` verdrahtet das echte Owner-Trio (Dependency-Inversion). Für Tests
gegen Fakes: `create_app(bundle_factory=…)` bzw. eigenes `ProviderBundle`.

## 3. Was zurückkommt — `Output`

```python
out.raum          # RaumModell           → Räume, Türen, Ausgänge, Zirkulation (Raumerkennung)
out.platzierung   # PlatzierungsErgebnis → jede Leuchte: xy_mm, kind (rz/sicherheitsleuchte/antipanik),
                  #                        richtung, height_mm, circuit_hint, covers_segment, norm_quelle
out.render_summary
#   {"floor", "n_symbols", "by_kind": {"rz": …, "sicherheitsleuchte": …},
#    "n_raeume", "rendered",
#    "coverage": {"warnungen": [...], "hinweise": [...]},   # Audit (z.B. untypisierte Räume)
#    "pruefung": {"status": "ok|warnung|fehler", "befunde": [...]}}   # EN-1838-Prüfbericht
```

## 4. PDF statt DXF

`run(out_path=...)` schreibt DXF. PDF ist ein separater Renderer:

```python
from notbeleuchtung.hauptengine.render import dxf_zu_pdf
dxf_zu_pdf("output/plan.dxf", "output/plan.pdf")   # braucht das 'render'-Extra
```

## 5. Sofort ausprobieren

Lauffähiges Beispiel liegt bei: [`examples/demo_run.py`](../examples/demo_run.py).

```
python examples/demo_run.py                                   # Mollgasse EG → DXF
python examples/demo_run.py <plan.dxf> <FLOOR> out.pdf        # eigener Plan → PDF
python examples/demo_run.py <plan.dxf> EG out.dxf <lb.pdf>    # + 2. Input (LB)
```

Referenz-Durchstich (Mollgasse EG): **192 Räume, 15 RZ + 21 SL, Prüfstatus ok**. Der
Coverage-Audit meldet dort ehrlich „185/192 Räume ohne Raumtyp" — die Raumerkennung typt
auf diesem Plan dünn (bekannter Blocker), die Engine platziert entsprechend RZ-getrieben.

## Alternative: als HTTP-Dienst

Ist die Host-App nicht Python, statt In-Process-Import die FastAPI als Backend nutzen:

```
.venv/Scripts/uvicorn notbeleuchtung.api.main:app --port 8000    # pip install -e ".[api,render]"
```

`POST /plan` (DXF-Upload + optional LB → DXF/PDF, Statistik im Header `X-Notbeleuchtung`),
`POST /projekt` (mehrere Geschosse → Sammel-PDF), `GET /health`. Für ein Browser-Frontend
muss noch CORS aktiviert werden (aktuell nicht gesetzt).
