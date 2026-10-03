"""gen_analyse_md.py — generiert ANALYSE_<Projekt>.md aus dem Seitenprotokoll.

Input:  evidenz/<Projekt>/seitenprotokoll.jsonl  (1 Record je PDF-Seite)
Output: ANALYSE_<Projekt>.md  (Bild-für-Bild-Protokoll, Auftrags-Deliverable 3)

Record-Schema (geschrieben von den Analyse-Batches):
{
  "seite": 12,
  "geschoss": "EG",                  # oder null
  "ueberschrift": "…",               # Überschrift/Thema der Seite
  "bereich": "Stiegenhaus Top 1",    # dargestellter Bereich (Raumnamen)
  "bildinhalt": "…",                 # was das BILD zeigt (2-4 Sätze)
  "regeln_zitate": ["…"],           # wörtliche Regel-Aussagen des Texts
  "elemente": {"leuchten": [{"kennung": "(A)", "typ": "down", …}],
                "personen": […], "linien": "…"},
  "dxf_abgleich": {"datei": "…", "handles": ["…"], "befund": "stimmt|abweichung: …"},
  "bewertung": "bestaetigt:NB-R06" | "neu" | "widerspruch" | "kein_regelgehalt",
  "regel_kandidat": "…"              # falls neu/widerspruch
}

Aufruf: python gen_analyse_md.py [Projekt …]
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HIER = Path(__file__).resolve()
BASIS = HIER.parents[1]

PROJEKT_TITEL = {
    "Mollgasse": "Projekt 1 — Mollgasse (BASIS)",
    "Tomaschek": "Projekt 2 — Tomaschek-Schule",
    "AmRain": "Projekt 3 — Am Rain (TEILSTAND)",
    "Hausfeld": "Projekt 4 — Hausfeldstraße",
    "BaufeldE2": "Projekt 5 — Baufeld E2 (nur DXF)",
}


def generiere(projekt: str) -> None:
    jl = BASIS / "evidenz" / projekt / "seitenprotokoll.jsonl"
    if not jl.exists():
        print(f"[{projekt}] kein seitenprotokoll.jsonl — übersprungen")
        return
    records = [json.loads(z) for z in jl.read_text(encoding="utf-8").splitlines() if z.strip()]
    records.sort(key=lambda r: r.get("seite", 0))

    zeilen = [
        f"# ANALYSE — {PROJEKT_TITEL.get(projekt, projekt)}",
        "",
        (f"Generiert aus `evidenz/{projekt}/seitenprotokoll.jsonl` "
         f"({len(records)} Seiten-Records) — nicht von Hand editieren."),
        "",
    ]
    n_best, n_neu, n_wid, n_ohne = 0, 0, 0, 0
    for r in records:
        bew = r.get("bewertung", "")
        if bew.startswith("bestaetigt"):
            n_best += 1
        elif bew == "neu":
            n_neu += 1
        elif bew == "widerspruch":
            n_wid += 1
        else:
            n_ohne += 1
        kopf = f"## S.{r['seite']:>3}"
        if r.get("geschoss"):
            kopf += f" · {r['geschoss']}"
        if r.get("ueberschrift"):
            kopf += f" — {r['ueberschrift']}"
        zeilen.append(kopf)
        if r.get("bereich"):
            zeilen.append(f"**Bereich:** {r['bereich']}")
        if r.get("bildinhalt"):
            zeilen.append(f"**Bild:** {r['bildinhalt']}")
        for z in r.get("regeln_zitate", []) or []:
            zeilen.append(f"> „{z}“")
        el = r.get("elemente") or {}
        if el.get("leuchten"):
            le = ", ".join(
                f"{x.get('kennung','?')} {x.get('typ','?')}" for x in el["leuchten"]
            )
            zeilen.append(f"**Leuchten im Bild:** {le}")
        if el.get("personen"):
            pe = ", ".join(
                f"{x.get('herkunft','?')}" for x in el["personen"]
            )
            zeilen.append(f"**Personen:** {pe}")
        if el.get("linien"):
            zeilen.append(f"**Linien:** {el['linien']}")
        ab = r.get("dxf_abgleich") or {}
        if ab:
            zeilen.append(
                f"**DXF-Abgleich:** {ab.get('datei','—')} · "
                f"Handles {', '.join(ab.get('handles', []) or ['—'])} · "
                f"{ab.get('befund','—')}"
            )
        if bew:
            zeilen.append(f"**Bewertung:** {bew}"
                          + (f" → {r['regel_kandidat']}" if r.get("regel_kandidat") else ""))
        zeilen.append("")

    zeilen.insert(4, (
        f"**Bilanz:** {n_best} bestätigt · {n_neu} neu · {n_wid} Widerspruch · "
        f"{n_ohne} ohne Regelgehalt (Deckblatt/Legende/…)\n"
    ))
    out = BASIS / f"ANALYSE_{projekt}.md"
    out.write_text("\n".join(zeilen), encoding="utf-8")
    print(f"[{projekt}] {len(records)} Records -> {out.name} "
          f"({n_best} best./{n_neu} neu/{n_wid} wid.)")


def main(argv: list[str]) -> int:
    for projekt in (argv or PROJEKT_TITEL):
        generiere(projekt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
