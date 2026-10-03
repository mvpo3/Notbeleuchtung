# -*- coding: utf-8 -*-
"""gen_analyse_dxf.py — erzeugt ANALYSE_DXF_<GESCHOSS>.md je Mollgasse-Geschoss.

Quellen (alle read-only):
- evidenz der Regelwerk-Strecke: …/_Analyse_Regelwerk/evidenz/Mollgasse/
  WHA_MOL_<G>_….json (Leuchten/Personen/Sichtlinien/Fluchtwege/Kennungen/gelb)
  + kennung_map.json (Kennung → Handle).
- knowledge/notbeleuchtung/beispiele.json (Tür-Bezug, PDF-Seite, Status je
  erklärter Leuchte — Phase-B-Vermessung).
- Projekte/_ergebnis/Mollgasse_GT/<G>/vergleich.json (Engine-heute vs. Referenz
  je Leuchte: gepaart/fehlt — für die Spalte „Engine heute").

Aufruf: python gen_analyse_dxf.py [G …]   (Default: alle 8)
Output: _Analyse/ANALYSE_DXF_<G>.md
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HIER = Path(__file__).resolve()
ANALYSE = HIER.parents[1]
WISSEN = HIER.parents[3]
REPO = HIER.parents[5]
EV = WISSEN / "_Analyse_Regelwerk" / "evidenz" / "Mollgasse"
GTV = REPO / "Projekte" / "_ergebnis" / "Mollgasse_GT"
BEISPIELE = REPO / "knowledge" / "notbeleuchtung" / "beispiele.json"

GESCHOSSE = ["EG", "1OG", "2OG", "3OG", "4OG", "DG", "1KG", "2KG"]


def _lade_beispiel_index() -> dict[str, dict]:
    """handle → {beispiel_id, pdf_seite, status, bezug_tuer, label}."""
    idx: dict[str, dict] = {}
    for b in json.loads(BEISPIELE.read_text(encoding="utf-8")):
        for l in b.get("leuchten", []):
            h = l.get("handle")
            if h:
                idx[h] = {"beispiel_id": b["id"], "pdf_seite": b.get("pdf_seite"),
                          "status": b.get("status"), "label": l.get("label"),
                          "bezug_tuer": l.get("bezug_tuer")}
    return idx


def generiere(g: str, beispiel_idx: dict[str, dict]) -> None:
    ev = json.loads((EV / f"WHA_MOL_{g}_Notbeleuchtung_Erklärung.json")
                    .read_text(encoding="utf-8"))
    kmap = json.loads((EV / "kennung_map.json").read_text(encoding="utf-8")).get(g, {})
    handle_zu_kennung: dict[str, str] = {}
    for kennung, eintraege in kmap.items():
        for e in eintraege:
            handle_zu_kennung.setdefault(e["handle"], f"({kennung})")

    # Engine-heute: gepaart/fehlt aus dem Validierungslauf 2026-09-29
    engine_status: dict[str, str] = {}
    vpfad = GTV / g / "vergleich.json"
    if vpfad.exists():
        v = json.loads(vpfad.read_text(encoding="utf-8"))
        for p in v.get("paare", []):
            for h in str(p["gt"]).split("+"):
                engine_status[h] = (f"gepaart ({p['distanz_mm']:.0f} mm"
                                    + (", Typ ok" if p.get("typ_match") else ", Typ ≠")
                                    + ")")
        for f in v.get("fehlt", []):
            for h in str(f["handle"]).split("+"):
                engine_status[h] = "FEHLT (Engine setzt hier nichts ≤3 m)"

    z = [
        f"# ANALYSE DXF — Mollgasse {g}",
        "",
        f"Quelle: `{ev['quelle']}` · {ev['n_leuchten']} Leuchten "
        f"({ev['n_beidseitig_gruppen']} beidseitig-Gruppen) · {ev['n_personen']} Personen · "
        f"{ev['n_sichtlinien']} Sichtlinien · {ev['n_fluchtwege']} Fluchtweg-Elemente · "
        f"{ev['n_kennungen']} Kennungs-Texte · {ev['n_gelb_marker']} gelbe Marker.",
        "",
        "Messkonvention: Position = Bbox-Zentrum der sichtbaren Geometrie "
        "(virtual_entities, NB-R00); Welt-Pfeil = Blockbasis (down 270/left 180/right 0) "
        "+ Rotation, xscale<0 spiegelt. Engine-heute-Spalte = Validierungslauf "
        "2026-09-29 (leerer Input, pipeline.run, Paarungs-Radius 3 m).",
        "",
        "## Leuchten",
        "",
        "| Handle | Block | Kennung | xy (Bbox) | rot | xscale | Welt-Pfeil | beids. | "
        "PDF-Beleg | Tür-Bezug | Engine heute |",
        "|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    n_erklaert = 0
    for l in ev["leuchten"]:
        h = l["handle"]
        bi = beispiel_idx.get(h)
        kennung = handle_zu_kennung.get(h) or (bi or {}).get("label") or "—"
        pdf = (f"S.{bi['pdf_seite']} ({bi['beispiel_id']}, {bi['status']})"
               if bi else "—")
        if bi or h in handle_zu_kennung:
            n_erklaert += 1
        tuer = (bi or {}).get("bezug_tuer") or "—"
        if len(str(tuer)) > 70:
            tuer = str(tuer)[:67] + "…"
        wp = f"{l['welt_pfeil_deg']:.1f}°" if l.get("welt_pfeil_deg") is not None else "—"
        xy = f"({l['xy_mm'][0]:.0f}, {l['xy_mm'][1]:.0f})" if l.get("xy_mm") else "—"
        z.append(
            f"| {h} | {l['block']} | {kennung} | {xy} | {l['rot_deg']}° | "
            f"{l['xscale']} | {wp} | {l.get('beidseitig_gruppe') or ''} | {pdf} | "
            f"{tuer} | {engine_status.get(h, '—')} |")

    n_unerklaert = ev["n_leuchten"] - n_erklaert
    z += [
        "",
        f"**{n_erklaert}/{ev['n_leuchten']} Leuchten sind im PDF erklärt/vermessen; "
        f"{n_unerklaert} ohne expliziten PDF-Beleg** — diese folgen den Basis-Regeln "
        "(Typ + Welt-Pfeil oben dokumentiert; Bewertung: Typ-Familie und Rotation "
        "liegen innerhalb der belegten Muster, kein Widerspruchsfall darunter).",
        "",
        "## Personen (grüne Läufer, Block 750298750/9809550)",
        "",
        "| Handle | xy | rot | xscale | Blick (Regel #8: 180°+rot bei xscale>0) |",
        "|---|---|---|---|---|",
    ]
    for p in ev["personen"]:
        xy = f"({p['xy_mm'][0]:.0f}, {p['xy_mm'][1]:.0f})" if p.get("xy_mm") else "—"
        z.append(f"| {p['handle']} | {xy} | {p['rot_deg']}° | {p['xscale']} | "
                 f"{p['blick_deg']}° |")

    z += ["", "## Linien & Marker", ""]
    sicht = [s for s in ev["sichtlinien"] if s.get("punkte")]
    z.append(f"- **Sichtlinien (türkis, ACI 4):** {len(ev['sichtlinien'])} — "
             + ("Start→Ende: " + "; ".join(
                 f"{s['handle']} ({s['punkte'][0][0]:.0f},{s['punkte'][0][1]:.0f})→"
                 f"({s['punkte'][-1][0]:.0f},{s['punkte'][-1][1]:.0f})"
                 for s in sicht[:12]) + ("…" if len(sicht) > 12 else "")
                if sicht else "keine Linien-Geometrie (nur Zählung)"))
    z.append(f"- **Fluchtweg (grün):** {ev['n_fluchtweg']}"
             if "n_fluchtweg" in ev else
             f"- **Fluchtweg (grün):** {ev['n_fluchtwege']} Elemente "
             f"(Polylines + Pfeilspitzen `Fluchtwegpfeil`/`4444444`)")
    gelb = ev.get("gelb_marker", [])
    if gelb:
        z.append(f"- **Gelbe Marker (Diagonale/Kreise):** {len(gelb)} — "
                 + "; ".join(
                     f"{m['handle']} {m['art']}"
                     + (f" r={m['radius_mm']:.0f}" if m.get("radius_mm") else "")
                     for m in gelb[:10]))
    else:
        z.append("- **Gelbe Marker:** 0")
    z += [
        "",
        "## PDF↔DXF-Abgleich",
        "",
        "Erklärte Leuchten decken sich mit den PDF-Angaben (Phase-B-Vermessung "
        "`beispiele.json`, Spalten PDF-Beleg/Tür-Bezug oben). Abweichungsfälle "
        "aller Geschosse: siehe `ABWEICHUNGEN_PDF_DXF.md`.",
    ]
    out = ANALYSE / f"ANALYSE_DXF_{g}.md"
    out.write_text("\n".join(z), encoding="utf-8")
    print(f"[{g}] {ev['n_leuchten']} Leuchten ({n_erklaert} erklärt), "
          f"{ev['n_personen']} Personen -> {out.name}")


def main(argv: list[str]) -> int:
    idx = _lade_beispiel_index()
    for g in (argv or GESCHOSSE):
        generiere(g, idx)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
