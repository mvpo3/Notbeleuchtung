"""demo_run — die Hauptengine in einer eigenen App aufrufen (Raumerkennung + Platzierung).

Das ist der EINE Einstiegspunkt, den eine Demo-/Host-App braucht: sie baut das echte
Owner-Trio (`build_default_bundle`) und ruft `pipeline.run(...)`. Darin steckt der ganze
Durchstich —

    DXF  --parse-->  RaumModell            (Selman: Raumerkennung)
                     PlatzierungsErgebnis  (Leonis: Notbeleuchtungs-Platzierung, norm-getrieben)
         --render->  Notbeleuchtungs-DXF/PDF (Hauptengine)

Kein HTTP nötig, wenn die Host-App Python ist: einfach importieren. Das Norm-/LB-Wissen
(EN 1838 / ÖNorm, `normwissen/data/*.yaml`, `knowledge/`) ist Teil des Pakets und wird
von `build_default_bundle()` automatisch geladen.

Aufruf:
    python examples/demo_run.py                        # Default: Mollgasse EG → DXF
    python examples/demo_run.py <plan.dxf> <FLOOR>     # eigener Plan/Geschoss
    python examples/demo_run.py <plan.dxf> EG out.pdf  # PDF statt DXF (Endung .pdf)
    python examples/demo_run.py <plan.dxf> EG out.dxf <leistungsbeschreibung.pdf>  # + 2. Input (LB)
"""
from __future__ import annotations

import contextlib
import sys
from pathlib import Path

from notbeleuchtung.hauptengine.pipeline import run
from notbeleuchtung.hauptengine.registry import build_default_bundle
from notbeleuchtung.hauptengine.render import dxf_zu_pdf

# Default-Plan: der leere Mollgasse-EG-Architekturplan aus dem Repo (Referenz-Durchstich).
_DEFAULT_DXF = "Projekte/Mollgasse/Erdgeschoß.dxf"
_DEFAULT_FLOOR = "EG"


def erzeuge_plan(
    dxf_path: str, floor: str, out_path: str | None = None, lb_path: str | None = None
):
    """Ein Aufruf = fertiger Notbeleuchtungsplan. Gibt das `Output` der Pipeline zurück.

    `out_path` mit Endung `.pdf` rendert erst DXF, dann PDF; `.dxf` (oder None) bleibt DXF.
    `lb_path` (optional) ist der 2. Input (Leistungsbeschreibung) — übersteuert Norm-Defaults.
    """
    bundle = build_default_bundle()               # Raumerkennung + Platzierung + Norm + LB
    will_pdf = bool(out_path) and out_path.lower().endswith(".pdf")
    dxf_out = out_path if (out_path and not will_pdf) else (
        str(Path(out_path).with_suffix(".dxf")) if out_path else None
    )
    out = run(bundle, dxf_path=dxf_path, floor=floor, out_path=dxf_out, lb_path=lb_path)
    if will_pdf and dxf_out:
        dxf_zu_pdf(dxf_out, out_path)              # 'render'-Extra nötig (matplotlib)
    return out


def main(argv: list[str]) -> int:
    # Umlaute/Pfeile in Norm-Meldungen sicher ausgeben (Windows-Konsole = cp1252).
    with contextlib.suppress(AttributeError, ValueError):
        sys.stdout.reconfigure(encoding="utf-8")
    dxf_path = argv[1] if len(argv) > 1 else _DEFAULT_DXF
    floor = argv[2] if len(argv) > 2 else _DEFAULT_FLOOR
    out_path = argv[3] if len(argv) > 3 else "output/demo_plan.dxf"
    lb_path = argv[4] if len(argv) > 4 else None

    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    out = erzeuge_plan(dxf_path, floor, out_path, lb_path)

    s = out.render_summary
    print(f"Plan: {dxf_path} ({floor})")
    print(f"  Räume erkannt : {s.get('n_raeume')}")
    print(f"  Symbole       : {s.get('n_symbols')}  {s.get('by_kind')}")
    print(f"  Prüfstatus    : {s.get('pruefung', {}).get('status')}")
    print(f"  Ausgabe       : {out_path}")
    for w in s.get("coverage", {}).get("warnungen", []):
        print(f"  [!] {w}")
    # Die Contract-Objekte selbst (für tiefere Integration in die Host-App):
    #   out.raum        → RaumModell (Räume/Türen/Ausgänge/Zirkulation)
    #   out.platzierung → PlatzierungsErgebnis (jede Leuchte mit xy, kind, richtung, norm_quelle)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
