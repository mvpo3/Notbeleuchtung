"""run_mollgasse — Hauptengine roh auf den LEEREN Mollgasse-Architekturplänen.

Rivoplan-Endstrecke des Ground-Truth-Auftrags (2026-09-20): leerer
Architektur-DXF → Selman-Erkennung unangereichert → `pipeline.run` mit
`pdf_quelle=True` (A0-Blatt aus der Rivoplan-Mastervorlage; ezdxf rastert
Paperspace nicht → PDF aus dem Modelspace-Sibling), danach Lux-Nachweis-Seite
+ Merge je Geschoss. Symbole = ausschließlich Rivoplan_Notbeleuchtungs_
Symbole.dxf, Blatt = Rivoplan_Notbeleuchtungs_Vorlage.dxf (Migration M1–M3).

Aufruf:  python scripts/demo/run_mollgasse.py [EG 1KG ...]
Ohne Argumente laufen alle 8 Geschosse; für Vordergrund-Batches ≤10 min
Geschosse gruppenweise übergeben (Background-Prozesse werden in der
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

REPO = Path(__file__).resolve().parents[2]
LEER = REPO / "Projekte_Leere Architektpläne (Input)" / "Mollgasse"
OUT = REPO / "Projekte" / "_ergebnis" / "Mollgasse_GT" / "rivoplan_out"

GESCHOSSE: dict[str, Path] = {
    "EG": LEER / "Erdgeschoß.dxf",
    "1OG": LEER / "1.Obergeschoß.dxf",
    "2OG": LEER / "2.Obergeschoß.dxf",
    "3OG": LEER / "3.Obergeschoß.dxf",
    "4OG": LEER / "4.Obergeschoß.dxf",
    "DG": LEER / "Dachgeschoß.dxf",
    "1KG": LEER / "1.Kellergeschoß.dxf",
    "2KG": LEER / "2.Kellergeschoß.dxf",
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
            plankopf={"projekt": f"WHA Mollgasse · {key}"},
            pdf_quelle=True,
        )
        quelle = out_dxf.with_name(out_dxf.stem + ".modelspace.dxf")
        plan_pdf = OUT / f"{key}_plan.pdf"
        dxf_zu_pdf(str(quelle if quelle.exists() else out_dxf), str(plan_pdf))
        lux_pdf = OUT / f"{key}_lux.pdf"
        bericht = schreibe_bericht(
            res.raum, res.platzierung, bundle.norm, str(lux_pdf),
            i_cd_fn=i_cd_fn, projekt=f"WHA Mollgasse · {key}")
        _merge([plan_pdf, lux_pdf] if bericht else [plan_pdf], OUT / f"{key}.pdf")
        eof_ok = (OUT / f"{key}.pdf").read_bytes().rstrip().endswith(b"%%EOF")
        arten: dict[str, int] = {}
        for p in res.platzierung.platzierungen:
            arten[p.kind] = arten.get(p.kind, 0) + 1
        pr = res.render_summary.get("pruefung", {})
        print(f"{key}: raeume={len(res.raum.raeume)} n={len(res.platzierung.platzierungen)} "
              f"arten={arten} status={pr.get('status')} layout={res.render_summary.get('layout')} "
              f"eof_ok={eof_ok}", flush=True)


if __name__ == "__main__":
    main(sys.argv[1:])
