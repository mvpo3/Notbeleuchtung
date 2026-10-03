"""pdf_seiten.py — rendert alle Seiten der 4 Erklär-PDFs als PNG (Analyse-Cache).

pypdfium2, ~150 dpi (scale 2.1) → seiten/<Projekt>/S###.png + text/<Projekt>.jsonl
(extrahierter Seitentext für den Protokoll-Abgleich). Quell-PDFs nur lesend.

Aufruf:
    python pdf_seiten.py                # alle
    python pdf_seiten.py Mollgasse      # Auswahl
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import pypdfium2 as pdfium

HIER = Path(__file__).resolve()
WISSEN = HIER.parents[2]
SEITEN = HIER.parents[1] / "seiten"

PDFS = {
    "Mollgasse": WISSEN / "Mollgasse-Notbeleuchtungserklärung" / "Notbeleuchtungen zeichnen.pdf",
    "Hausfeld": WISSEN / "Hausfeldstraße Notbeleuchtung zeichnen" / "Hausfeldstraße Notbeleuchtung zeichnen_aktualisiert.pdf",
    "AmRain": WISSEN / "Am Rain Notbeleuchtungserklärung" / "Am_Rain_Notbeleuchtungen_zeichnen_RIVO_TEILSTAND_v1.pdf",
    "Tomaschek": WISSEN / "Tomaschek-Schule -Notbeleuchtungserklärung" / "Tomaschek_Schule_Notbeleuchtungen_zeichnen_RIVO_Formkorrektur.pdf",
}


def rendere(projekt: str, pfad: Path, scale: float = 2.1) -> None:
    out_dir = SEITEN / projekt
    out_dir.mkdir(parents=True, exist_ok=True)
    doc = pdfium.PdfDocument(str(pfad))
    texte = []
    t0 = time.time()
    for i in range(len(doc)):
        seite = i + 1
        png = out_dir / f"S{seite:03d}.png"
        if not png.exists():
            page = doc[i]
            bmp = page.render(scale=scale)
            bmp.to_pil().save(str(png))
        try:
            tp = doc[i].get_textpage()
            texte.append({"seite": seite, "text": tp.get_text_bounded()})
        except Exception as exc:  # noqa: BLE001
            texte.append({"seite": seite, "text": "", "fehler": str(exc)})
    (out_dir / "text.jsonl").write_text(
        "\n".join(json.dumps(t, ensure_ascii=False) for t in texte),
        encoding="utf-8",
    )
    doc.close()
    print(f"[{projekt}] {seite} Seiten -> {out_dir} [{time.time()-t0:.0f}s]", flush=True)


def main(argv: list[str]) -> int:
    auswahl = set(argv) or set(PDFS)
    for projekt, pfad in PDFS.items():
        if projekt in auswahl:
            rendere(projekt, pfad)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
