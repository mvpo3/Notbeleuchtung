"""run_fischamend — Hauptengine roh auf BVH Fischamenderstraße (BT1+BT2, 9 Geschosse).

Runner-Muster der v2-Runde (Handoff 2026-09-18), jetzt versioniert: Selmans
Erkennung unangereichert, `pipeline.run` mit `pdf_quelle=True` (A0-Blatt-Weg:
ezdxf rastert Paperspace nicht → PDF aus dem Modelspace-Sibling), danach
Lux-Nachweis-Seite + Merge je Geschoss.

Aufruf:  python scripts/demo/run_fischamend.py [BT1_EG BT2_DG ...]
Ohne Argumente laufen alle 9 Geschosse; für Vordergrund-Batches ≤10 min
Geschosse einzeln/gruppenweise übergeben (Background-Prozesse werden in der
Claude-Umgebung gekillt).
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

from notbeleuchtung.hauptengine import pipeline
from notbeleuchtung.hauptengine.registry import build_default_bundle
from notbeleuchtung.hauptengine.render.lux_nachweis_bericht import schreibe_bericht
from notbeleuchtung.hauptengine.render.pdf_export import dxf_zu_pdf

PROJEKT = Path(__file__).resolve().parents[2] / "Projekte" / "BVH Fischamenderstraße"
OUT = PROJEKT / "notbeleuchtung_out" / "v3"

GESCHOSSE: dict[str, Path] = {
    "BT1_EG": PROJEKT / "BT1" / "260320_938-AR-PP-11000-A_ERDGESCHOSS BT1.dxf",
    "BT1_1OG": PROJEKT / "BT1" / "260320_938-AR-PP-11010-A_1.OBERGESCHOSS BT1.dxf",
    "BT1_2OG": PROJEKT / "BT1" / "260320_938-AR-PP-11020-A_2.OBERGESCHOSS BT1.dxf",
    "BT1_DG": PROJEKT / "BT1" / "260320_938-AR-PP-11030-A_DACHGESCHOSS BT1.dxf",
    "BT1_UG": PROJEKT / "BT1" / "260320_938-AR-PP-11990-A_UNTERGESCHOSS BT1.dxf",
    "BT2_EG": PROJEKT / "BT2" / "260320_938-AR-PP-21000-A_ERDGESCHOSS BT2.dxf",
    "BT2_1OG": PROJEKT / "BT2" / "260320_938-AR-PP-21010-A_1.OBERGESCHOSS BT2.dxf",
    "BT2_2OG": PROJEKT / "BT2" / "260320_938-AR-PP-21020-A_2.OBERGESCHOSS BT2.dxf",
    "BT2_DG": PROJEKT / "BT2" / "260320_938-AR-PP-21030-A_DACHGESCHOSS BT2.dxf",
}


def _merge(seiten: list[Path], ziel: Path) -> None:
    from pypdf import PdfReader, PdfWriter

    w = PdfWriter()
    for s in seiten:
        for pg in PdfReader(str(s)).pages:
            w.add_page(pg)
    with open(ziel, "wb") as fh:
        w.write(fh)


def main(keys: list[str]) -> None:
    unbekannt = [k for k in keys if k not in GESCHOSSE]
    if unbekannt:
        raise SystemExit(f"unbekannte Geschosse: {unbekannt} — erlaubt: {list(GESCHOSSE)}")
    OUT.mkdir(parents=True, exist_ok=True)
    bundle = build_default_bundle()
    i_cd_fn = getattr(bundle.platzierer, "_i_cd_fn", None)
    for key in keys or list(GESCHOSSE):
        dxf_in = GESCHOSSE[key]
        out_dxf = OUT / f"{key}_notbeleuchtung.dxf"
        res = pipeline.run(
            bundle, str(dxf_in), key, out_path=str(out_dxf),
            plankopf={"projekt": f"BVH Fischamenderstraße · {key}"},
            pdf_quelle=True,
        )
        quelle = out_dxf.with_name(out_dxf.stem + ".modelspace.dxf")
        plan_pdf = OUT / f"{key}_plan.pdf"
        dxf_zu_pdf(str(quelle if quelle.exists() else out_dxf), str(plan_pdf))
        lux_pdf = OUT / f"{key}_lux.pdf"
        bericht = schreibe_bericht(
            res.raum, res.platzierung, bundle.norm, str(lux_pdf),
            i_cd_fn=i_cd_fn, projekt=f"BVH Fischamenderstraße · {key}")
        _merge([plan_pdf, lux_pdf] if bericht else [plan_pdf], OUT / f"{key}.pdf")
        arten: dict[str, int] = {}
        for p in res.platzierung.platzierungen:
            arten[p.kind] = arten.get(p.kind, 0) + 1
        pr = res.render_summary.get("pruefung", {})
        print(f"{key}: raeume={len(res.raum.raeume)} n={len(res.platzierung.platzierungen)} "
              f"arten={arten} status={pr.get('status')}", flush=True)


if __name__ == "__main__":
    main(sys.argv[1:])
