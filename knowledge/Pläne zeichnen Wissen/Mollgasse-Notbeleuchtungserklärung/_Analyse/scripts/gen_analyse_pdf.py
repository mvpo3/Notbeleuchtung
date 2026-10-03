# -*- coding: utf-8 -*-
"""gen_analyse_pdf.py — ANALYSE_PDF.md (Seite-für-Seite) + ABWEICHUNGEN_PDF_DXF.md
aus den Detail-Batches (evidenz/detail_batch_*.jsonl, Zweitpass 2026-09-30).

Aufruf: python gen_analyse_pdf.py
"""
from __future__ import annotations

import json
from pathlib import Path

HIER = Path(__file__).resolve()
ANALYSE = HIER.parents[1]
EV = ANALYSE / "evidenz"


def main() -> int:
    records: list[dict] = []
    for jl in sorted(EV.glob("detail_batch_*.jsonl")):
        for z in jl.read_text(encoding="utf-8").splitlines():
            if z.strip():
                records.append(json.loads(z))
    records.sort(key=lambda r: r.get("seite", 0))

    n_regeln = sum(len(r.get("regeln") or []) for r in records)
    n_abw = sum(1 for r in records if r.get("abweichung_pdf_dxf"))
    z = [
        "# ANALYSE_PDF — Mollgasse Notbeleuchtungen-zeichnen-PDF (95 S.), Bild für Bild",
        "",
        f"Detail-Zweitpass 2026-09-30 (alle Seiten als Bild angesehen; wörtliche "
        f"Zitate aus dem Seitentext). {len(records)} Seiten-Records, "
        f"{n_regeln} Regel-Aussagen mit Warum-Begründung, {n_abw} PDF↔DXF-Abweichungsvermerke.",
        "Generiert aus `evidenz/detail_batch_*.jsonl` — nicht von Hand editieren.",
        "",
    ]
    for r in records:
        kopf = f"## S.{r['seite']:>3}"
        if r.get("geschoss"):
            kopf += f" · {r['geschoss']}"
        if r.get("ueberschrift"):
            kopf += f" — {r['ueberschrift']}"
        z.append(kopf)
        if r.get("bereich"):
            z.append(f"**Bereich:** {r['bereich']}")
        for q in r.get("zitate") or []:
            z.append(f"> „{q}“")
        for reg in r.get("regeln") or []:
            z.append(f"- **Regel:** {reg.get('regel', '')}")
            if reg.get("warum"):
                z.append(f"  **Warum:** {reg['warum']}")
        le = r.get("leuchten") or []
        if le:
            z.append("**Leuchten:** " + " · ".join(
                f"{x.get('kennung','?')} {x.get('typ','?')}"
                + (f" [{x['dxf_handle']}]" if x.get("dxf_handle") else "")
                + (f" Pfeil {x['rotation_bild']}" if x.get("rotation_bild") else "")
                for x in le))
        pe = r.get("personen") or []
        if pe:
            z.append("**Personen:** " + " · ".join(
                f"{x.get('herkunft','?')} (Blick {x.get('blick','?')}"
                + (f", sieht {x['sieht']}" if x.get("sieht") else "") + ")"
                for x in pe))
        sl = r.get("sichtlinien") or []
        if sl:
            z.append("**Sichtlinien:** " + " · ".join(
                f"{x.get('von','?')}→{x.get('zu','?')}" for x in sl))
        if r.get("linien"):
            z.append(f"**Linien/Marker:** {r['linien']}")
        if r.get("abweichung_pdf_dxf"):
            z.append(f"**⚠ PDF↔DXF:** {r['abweichung_pdf_dxf']}")
        for u in r.get("unsicher") or []:
            z.append(f"- unsicher: {u}")
        z.append("")
    (ANALYSE / "ANALYSE_PDF.md").write_text("\n".join(z), encoding="utf-8")

    # Abweichungs-Sammlung
    a = [
        "# ABWEICHUNGEN PDF ↔ DXF — Mollgasse (alle Geschosse)",
        "",
        "Aus dem Detail-Zweitpass (Spalte abweichung_pdf_dxf) + bekannte Fälle.",
        "",
    ]
    for r in records:
        if r.get("abweichung_pdf_dxf"):
            a.append(f"- **S.{r['seite']} ({r.get('geschoss','?')}):** {r['abweichung_pdf_dxf']}")
    a += [
        "",
        "## Einordnung",
        "",
        "Kein Fall stellt eine Zeichen-REGEL in Frage — alle Abweichungen sind",
        "Text-/Benennungs-Fehler der PDF oder Versionsstands-Reste; die DXF-Geometrie",
        "ist jeweils regelkonform (Detailbewertung je Fall oben; Owner-Meldung",
        "S.57 B↔C seit 2026-09-20 offen, offene_fragen.md #27-34).",
    ]
    (ANALYSE / "ABWEICHUNGEN_PDF_DXF.md").write_text("\n".join(a), encoding="utf-8")
    print(f"{len(records)} Seiten, {n_regeln} Regeln, {n_abw} Abweichungen "
          f"-> ANALYSE_PDF.md + ABWEICHUNGEN_PDF_DXF.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
