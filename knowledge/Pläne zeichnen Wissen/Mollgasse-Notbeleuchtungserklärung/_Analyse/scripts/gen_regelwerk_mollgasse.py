# -*- coding: utf-8 -*-
"""gen_regelwerk_mollgasse.py — REGELWERK_Mollgasse.{json,md} aus dem
konsolidierten Gesamt-Regelwerk (nur Mollgasse-belegte Basis-Regeln) +
Häufigkeits-Zählung (PDF-Seiten + DXF-Belege, nur Mollgasse-Quellen).

Quelle: …/_Analyse_Regelwerk/REGELWERK_Notbeleuchtung.json (Gate-geprüft).
Aufruf: python gen_regelwerk_mollgasse.py
"""
from __future__ import annotations

import json
from pathlib import Path

HIER = Path(__file__).resolve()
ANALYSE = HIER.parents[1]
WISSEN = HIER.parents[3]
QUELLE = WISSEN / "_Analyse_Regelwerk" / "REGELWERK_Notbeleuchtung.json"


def main() -> int:
    alle = json.loads(QUELLE.read_text(encoding="utf-8"))
    regeln = []
    for r in alle:
        if r.get("prioritaet") != "basis":
            continue
        moll_seiten = sorted({q["seite"] for q in r.get("quelle_pdf", [])
                              if q["projekt"] == "Mollgasse"})
        moll_belege = [b for b in r.get("belege_dxf", [])
                       if "WHA_MOL" in b.get("datei", "")]
        regeln.append({
            "id": r["id"],
            "nb_ref": r.get("nb_ref"),
            "thema": r.get("thema", ""),
            "regel": r.get("regel", ""),
            "geometrische_bedingung": r.get("geometrische_bedingung", {}),
            "leuchtentyp": r.get("leuchtentyp", "-"),
            "belege": {
                "pdf_seiten": moll_seiten,
                "dxf_handles": [{"datei": Path(b["datei"]).name,
                                 "handle": b.get("handle"),
                                 "rotation": b.get("rotation"),
                                 "x": b.get("x"), "y": b.get("y")}
                                for b in moll_belege],
            },
            "haeufigkeit": {"pdf_seiten": len(moll_seiten),
                            "dxf_belege": len(moll_belege)},
            "grenzfaelle": (r.get("geometrische_bedingung") or {}).get("parameter")
            or (r.get("geometrische_bedingung") or {}).get("hinweis") or "—",
            "begruendung": r.get("begruendung", ""),
            "beleg_alternativ": r.get("beleg_alternativ"),
        })
    (ANALYSE / "REGELWERK_Mollgasse.json").write_text(
        json.dumps(regeln, ensure_ascii=False, indent=1), encoding="utf-8")

    z = [
        "# REGELWERK Mollgasse — Basis-Zeichenregeln (aus PDF 95 S. + 8 Erklär-DXFs)",
        "",
        f"Generiert aus dem Gate-geprüften Gesamt-Regelwerk ({QUELLE.name}) — "
        "nur Mollgasse-belegte BASIS-Regeln; Häufigkeit = Mollgasse-PDF-Seiten "
        "+ vermessene DXF-Belege. Nicht von Hand editieren.",
        "",
        f"**{len(regeln)} Basis-Regeln.**",
        "",
    ]
    for r in regeln:
        z.append(f"### {r['id']}" + (f" ({r['nb_ref']})" if r["nb_ref"] else "")
                 + f" — {r['thema']}")
        z.append(r["regel"])
        gb = r["geometrische_bedingung"] or {}
        if gb.get("rotation"):
            z.append(f"- **Geometrie/Rotation:** {gb['rotation']}")
        if gb.get("position"):
            z.append(f"- **Position:** {gb['position']}")
        z.append(f"- **Leuchtentyp:** {r['leuchtentyp']}")
        s = r["belege"]["pdf_seiten"]
        z.append("- **PDF:** S." + ",".join(str(x) for x in s[:14])
                 + ("…" if len(s) > 14 else "") if s else "- **PDF:** —")
        hb = r["belege"]["dxf_handles"]
        if hb:
            probe = " · ".join(f"{b['handle']} ({b['datei'].split('_Notbeleuchtung')[0]}"
                               + (f", rot {b['rotation']}" if b.get("rotation") is not None else "")
                               + ")" for b in hb[:4])
            z.append(f"- **DXF-Belege ({len(hb)}):** {probe}"
                     + (f" … +{len(hb)-4}" if len(hb) > 4 else ""))
        elif r.get("beleg_alternativ"):
            z.append(f"- **Beleg (alternativ):** {r['beleg_alternativ']}")
        z.append(f"- **Häufigkeit:** {r['haeufigkeit']['pdf_seiten']} PDF-Seiten, "
                 f"{r['haeufigkeit']['dxf_belege']} DXF-Belege")
        if r["grenzfaelle"] != "—":
            z.append(f"- **Grenzfälle/Parameter:** `{json.dumps(r['grenzfaelle'], ensure_ascii=False)[:180]}`")
        if r["begruendung"]:
            z.append(f"- **Begründung/Quelle:** {r['begruendung']}")
        z.append("")
    (ANALYSE / "REGELWERK_Mollgasse.md").write_text("\n".join(z), encoding="utf-8")
    print(f"{len(regeln)} Basis-Regeln -> REGELWERK_Mollgasse.json + .md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
