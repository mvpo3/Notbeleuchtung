"""run_projekt_neu — Hauptengine auf dem realen Elektroplan (EG+1OG_Elektroplan_DE_NEU.dxf).

Primärweg = Selmans Raumerkennung (`pipeline._parse_raum`): sie typt 16/12 Räume korrekt
(WOHNZIMMER/KÜCHE/BAD/GANG …). ABER: die einzigen Türen „zu AUSSEN" sind Wohnungs-
Balkone/Fenster, kein Gebäude-Ausgang → 0 Fluchtweg-Ausgänge → ohne Ziel bleibt der Plan
dünn (1 RZ/1 SL).

**ANREICHERUNG (GROSS gekennzeichnet, NICHT rein aus Erkennung):** an die beiden Enden des
erkannten GANG-Korridors je einen `final_exit` setzen (Gebäude-Fluchtrichtungen) + ein
Fluchtweg-Segment entlang des Gangs. Damit hat die Platzierung ein Ziel — Pfeilumkehr,
Zwischen-RZ, Deckung greifen. Räume/Typen/Türen bleiben unverändert aus der Erkennung.
"""
from __future__ import annotations

import tempfile
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

from notbeleuchtung.hauptengine import pipeline
from notbeleuchtung.hauptengine.contracts import Ausgang, FluchtwegSegment
from notbeleuchtung.hauptengine.registry import build_default_bundle
from notbeleuchtung.hauptengine.render.lux_nachweis_bericht import schreibe_bericht
from notbeleuchtung.hauptengine.render.pdf_export import dxf_zu_pdf

P4 = Path(r"C:\Users\mvpst\Documents\KI-Projekt\Notbeleuchtung\Projektbeispiele-demo-Platzierungslogik")
OUT = P4 / "elektroplan_out"


def _bbox(poly):
    xs = [p[0] for p in poly]
    ys = [p[1] for p in poly]
    return min(xs), min(ys), max(xs), max(ys)


def _anreichern(raum):
    """Ausgänge an die GANG-Enden + Fluchtweg-Segment ergänzen (Gebäude-Flucht)."""
    gaenge = [r for r in raum.raeume if (r.raum_typ or "").upper() == "GANG"
              and len(r.polygon_mm) >= 3]
    if not gaenge:
        return raum
    g = max(gaenge, key=lambda r: r.flaeche_m2)
    x0, y0, x1, y1 = _bbox(g.polygon_mm)
    laengs = 0 if (x1 - x0) >= (y1 - y0) else 1
    quer = (y0 + y1) / 2.0 if laengs == 0 else (x0 + x1) / 2.0
    lo, hi = (x0, x1) if laengs == 0 else (y0, y1)
    inset = 800.0
    p_lo = (lo + inset, quer) if laengs == 0 else (quer, lo + inset)
    p_hi = (hi - inset, quer) if laengs == 0 else (quer, hi - inset)
    ausgaenge = [
        *raum.ausgaenge,
        Ausgang(id="EXIT-A", xy_mm=p_lo, typ="final_exit"),
        Ausgang(id="EXIT-B", xy_mm=p_hi, typ="final_exit"),
    ]
    seg = FluchtwegSegment(
        segment_id="gang-flucht", polyline_mm=[list(p_lo), list(p_hi)],
        laenge_mm=abs(hi - lo), reason="long_run", quelle="FALLBACK", ziel_ausgang="EXIT-A")
    zirk = raum.zirkulation.model_copy(update={"segmente": [*raum.zirkulation.segmente, seg]})
    return raum.model_copy(update={"ausgaenge": ausgaenge, "zirkulation": zirk})


def _merge(seiten, ziel):
    from pypdf import PdfReader, PdfWriter
    w = PdfWriter()
    for s in seiten:
        for pg in PdfReader(str(s)).pages:
            w.add_page(pg)
    with open(ziel, "wb") as fh:
        w.write(fh)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    bundle = build_default_bundle()
    i_cd_fn = getattr(bundle.platzierer, "_i_cd_fn", None)
    for floor in ("EG", "1OG"):
        dxf_in = P4 / f"{floor}_Elektroplan_DE_NEU.dxf"
        with tempfile.TemporaryDirectory(prefix="elektroplan_") as tmp:
            raum, quelle_dxf = pipeline._parse_raum(bundle, str(dxf_in), floor, tmp)
            raum = _anreichern(raum)
            out_dxf = OUT / f"{floor}_notbeleuchtung.dxf"
            res = pipeline._run_mit_quelle(
                bundle, raum, quelle_dxf, out_path=str(out_dxf), lb_path=None,
                plankopf={"projekt": f"Elektroplan DE · {floor}"},
                projekt_kontext=None, photometrie=None)
            plan_pdf = OUT / f"{floor}_plan.pdf"
            dxf_zu_pdf(str(out_dxf), str(plan_pdf))
            lb_pdf = OUT / f"{floor}_lichtberechnung.pdf"
            bericht = schreibe_bericht(res.raum, res.platzierung, bundle.norm, str(lb_pdf),
                                       i_cd_fn=i_cd_fn, projekt=f"Elektroplan DE · {floor}")
            _merge([plan_pdf, lb_pdf] if bericht else [plan_pdf], OUT / f"{floor}.pdf")
        bk: dict = {}
        for p in res.platzierung.platzierungen:
            bk[p.kind] = bk.get(p.kind, 0) + 1
        pr = res.render_summary.get("pruefung", {})
        print(f"{floor}: raeume={len(res.raum.raeume)} ausg={len(res.raum.ausgaenge)} "
              f"| platzierungen={bk} status={pr.get('status')}")


if __name__ == "__main__":
    main()
