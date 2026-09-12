"""run_demo — Engine-Lauf des L-Demo-Gebäudes je Geschoss (roher Hauptengine-Output).

RaumModell-Weg:
  PRIMÄR  = Selmans Raumerkennung (`ArchitekturRaumProvider.parse` auf DEMO_*.dxf).
  FALLBACK= Ground-Truth-RaumModell aus dem Generator (DEMO_*.raummodell.json).
Der Primärweg wird versucht + protokolliert; erkennt er die Kern-Merkmale NICHT
(Ausgänge/Typen), wird der Fallback benutzt und im Output GROSS als
„RaumModell aus Generator, NICHT aus Erkennung" markiert. Platzierungen kommen in
JEDEM Fall aus der Engine — nichts von Hand.

Ausgabe nach P4/demo/out/:
  DEMO_{EG,1OG}_notbeleuchtung.dxf · DEMO_{EG,1OG}.platzierung.json · DEMO_{EG,1OG}.pruefung.json
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

from notbeleuchtung.hauptengine.contracts import RaumModell
from notbeleuchtung.hauptengine.registry import default_photometrie
from notbeleuchtung.hauptengine.render.dxf_renderer import render_dxf
from notbeleuchtung.hauptengine.render.lux_nachweis_bericht import schreibe_bericht
from notbeleuchtung.hauptengine.render.pdf_export import dxf_zu_pdf
from notbeleuchtung.hauptengine.validierung import pruefbericht
from notbeleuchtung.normwissen.provider import En1838NormProvider
from notbeleuchtung.platzierung.platzierer import NotlichtPlatzierer

P4 = Path(r"C:\Users\mvpst\Documents\KI-Projekt\Notbeleuchtung\Projektbeispiele-demo-Platzierungslogik")
DEMO = P4 / "demo"
OUT = DEMO / "out"


def _primary_probe(floor):
    """Selmans Erkennung diagnostisch versuchen (nicht benutzt — nur belegt, was sie liefert).

    Befund am Demo (2026-09-10): der Primärweg parst die synthetische DXF zwar, liefert
    aber KEINE Ausgänge (Pfeilumkehr = Kern-Test) und typt Wohnungen/Müll/Stiege nicht →
    für den Platzierungs-/Licht-Test untauglich. Deshalb Fallback für BEIDE Geschosse."""
    try:
        from notbeleuchtung.raumerkennung.provider import ArchitekturRaumProvider
        r = ArchitekturRaumProvider().parse(str(DEMO / f"DEMO_{floor}.dxf"), floor)
        untyp = sum(1 for x in r.raeume if not (x.raum_typ or "").strip())
        return (f"raeume={len(r.raeume)} tueren={len(r.tueren)} ausgaenge={len(r.ausgaenge)} "
                f"segmente={len(r.zirkulation.segmente)} untypisiert={untyp}")
    except Exception as e:  # noqa: BLE001 — Diagnose in den Report
        return f"PARSE-FEHLER: {type(e).__name__}: {e}"


def run_floor(floor):
    OUT.mkdir(parents=True, exist_ok=True)
    info = _primary_probe(floor)
    # FALLBACK für beide Geschosse (Primärweg untauglich, s. _primary_probe):
    raum = RaumModell.model_validate(
        json.loads((DEMO / f"DEMO_{floor}.raummodell.json").read_text(encoding="utf-8")))
    quelle = "GENERATOR-GROUND-TRUTH (NICHT aus Erkennung)"

    norm = En1838NormProvider()
    i_cd_fn, befund = default_photometrie(optik_aus_achse=True)
    erg = NotlichtPlatzierer(i_cd_fn=i_cd_fn).place(raum, norm)
    pruef = pruefbericht(raum, erg, norm=norm, photometrie=befund)

    dxf = OUT / f"DEMO_{floor}_notbeleuchtung.dxf"
    # Owner-Ausgabeweg (#115): MODELSPACE-Blatt-Modus (versionierte Rivoplan-Vorlage) +
    # reiche DEMO-Architektur als Unterlage (unterlage_dxf). Der Blatt-Modus skaliert die
    # Vorlage MIT dem Plan (S = max(plan_w/fenster_w, plan_h/fenster_h)) → bei größerem
    # Grundriss wächst das Blatt, der Plan bleibt IM Planfenster. dxf_zu_pdf nimmt den
    # Blatt-Rahmen als 1:50-Liefer-Ausschnitt → A0. (KEIN template_path: der Layout1-
    # Viewport-Modus deaktiviert genau diesen Modelspace-Blatt-Modus → dann A3-Fallback.)
    render_dxf(erg, raum, str(dxf), pruefung=pruef, photometrie=befund,
               plankopf={"projekt": f"L-Demo · {floor}"},
               unterlage_dxf=str(DEMO / f"DEMO_{floor}.dxf"))
    (OUT / f"DEMO_{floor}.platzierung.json").write_text(
        erg.model_dump_json(indent=1), encoding="utf-8")
    (OUT / f"DEMO_{floor}.pruefung.json").write_text(
        json.dumps(pruef, ensure_ascii=False, indent=1), encoding="utf-8")

    # A0-PDF (1:50): dxf_zu_pdf nimmt automatisch den Blatt-Rahmen als Liefer-Ausschnitt.
    plan_pdf = OUT / f"DEMO_{floor}_plan.pdf"
    dxf_zu_pdf(str(dxf), str(plan_pdf))               # papierformat A0, massstab 1:50 (Default)
    # Lichtberechnungs-Seite (DIALux-artiger Nachweis) als eigenes PDF.
    lb_pdf = OUT / f"DEMO_{floor}_lichtberechnung.pdf"
    bericht = schreibe_bericht(raum, erg, norm, str(lb_pdf), i_cd_fn=i_cd_fn,
                               projekt=f"L-Demo · {floor}")
    # Zu EINEM A0-PDF zusammenführen (Plan-Seite + Nachweis-Seite).
    _merge_pdf([plan_pdf, lb_pdf] if bericht else [plan_pdf],
               OUT / f"DEMO_{floor}.pdf")

    bk = {}
    for p in erg.platzierungen:
        bk[p.kind] = bk.get(p.kind, 0) + 1
    print(f"{floor}: quelle={quelle} | primär-probe: {info}")
    print(f"     platzierungen={bk} status={pruef.get('status')} | PDF+DXF (1:50) geschrieben")
    return {"floor": floor, "quelle": quelle, "primaer_probe": info,
            "platzierungen": bk, "status": pruef.get("status")}


def _merge_pdf(seiten, ziel):
    from pypdf import PdfReader, PdfWriter
    w = PdfWriter()
    for src in seiten:
        for pg in PdfReader(str(src)).pages:
            w.add_page(pg)
    with open(ziel, "wb") as fh:
        w.write(fh)


def main():
    zus = [run_floor("EG"), run_floor("1OG")]
    (OUT / "run_summary.json").write_text(json.dumps(zus, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
