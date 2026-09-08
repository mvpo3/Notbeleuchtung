"""Mollgasse-UG: unabhängige NB-Referenz aus den GU-Elektro-Plänen (Slice 4.1).

Liest die GU-Grundriss-PDFs (extern, read-only), findet die Notbeleuchtungs-
Symbole als Vektor-Cluster und schreibt eine Referenz-Fixture je Geschoss
(`tests/fixtures/mollgasse_ug_referenz.json`-Familie) + Crops zur Sichtprüfung
(`reports/mollgasse_ug/<floor>/`, gitignored).

Methode (dokumentiert in docs/analyse/mollgasse_ug_notbeleuchtung.md):
- NB-Symbole = Vektor-Primitive in RGB (0, 0.722, 0) im Planfeld (x < 4300 pt).
  Die Legende (x > 4300) nutzt andere Grüntöne; Fluchtweg-Strichlinien ebenfalls.
- Cluster = Union-Find über bbox-Nähe (Gap 6 pt ≈ 106 mm Modell).
- Typ + Pfeilrichtung + Montage: SICHT-Klassifikation der Crops (2026-09-07,
  Claude-Session unter Owner Leonis) — als Tabelle unten versioniert, damit der
  Lauf reproduzierbar bleibt. Unklassifizierte Cluster → konfidenz "niedrig".
- Kalibrierung: Blatt-CropBox 4904.28 x 2105.16 pt x 25.4/72 = 1730.1 x 742.7 mm
  = Plankopf-Rahmenangabe "1730 x 743" (Abweichung < 0.1 %) → 1 pt Papier =
  25.4/72 mm; Maßstab 1:50 aus Plankopf → 1 pt = 17.6389 mm Modell.
- Koordinaten der Fixture: mm Modell, Ursprung = linke UNTERE Ecke der
  MediaBox-Seite (y nach oben; pdfplumber-`top` wird gespiegelt).

Aufruf:  python scripts/analyse/mollgasse_ug_nb.py [1KG] [2KG]
Braucht: pip install -e ".[analyse]"  (pdfplumber, pypdfium2 — KEINE Runtime-Deps).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pdfplumber
import pypdfium2 as pdfium

BASIS = Path(
    r"C:\Users\mvpst\Documents\KI-Projekt\elektro-planer"
    r"\S-24-2103-GU, 1180 Wien Mollgasse 15\Elektro"
)
DATEIEN = {
    "1KG": "MOL_GR-1KG_01-1-50_Index_4.pdf",
    "2KG": "MOL_GR-2KG_00-1-50_Index_5.pdf",
}
MASSSTAB = 50
ERFASST = "2026-09-07"  # Datum der Sicht-Klassifikation (SICHT-Tabelle unten)
PT_ZU_MM_MODELL = 25.4 / 72 * MASSSTAB  # 17.6389 mm Modell je pt
PLANFELD_MAX_X_PT = 4300.0              # rechts davon: Legende + Plankopf
CLUSTER_GAP_PT = 6.0
SEITE_H_PT = 2551.0

# Sicht-Klassifikation der Crops (reports/mollgasse_ug/<floor>/<id>.png).
# kind: rz | sl · richtung: Pfeilrichtung IM PLAN (rechts/links/oben/unten)
# montage: horizontal | vertikal (Symbol-Längsachse im Plan)
# n: Leuchten im Cluster (Doppel-RZ Rücken an Rücken = 2)
SICHT = {
    "1kg_c00": ("rz", "rechts", "horizontal", 1, "hoch"),
    "1kg_c01": ("rz", "unten", "vertikal", 1, "hoch"),
    "1kg_c02": ("rz", "unten", "horizontal", 1, "hoch"),
    "1kg_c03": ("rz", "unten", "horizontal", 1, "hoch"),
    "1kg_c04": ("rz", "oben", "vertikal", 1, "hoch"),
    "1kg_c05": ("rz", "unten", "horizontal", 1, "hoch"),
    "1kg_c06": ("rz", "rechts", "horizontal", 2, "hoch"),
    "1kg_c07": ("rz", "oben", "vertikal", 2, "hoch"),
    "1kg_c08": ("rz", "oben", "vertikal", 1, "hoch"),
    "2kg_c00": ("rz", "oben", "vertikal", 1, "hoch"),
    "2kg_c01": ("rz", "rechts", "horizontal", 1, "hoch"),
    "2kg_c02": ("rz", "unten", "horizontal", 1, "hoch"),
    "2kg_c03": ("rz", "rechts", "horizontal", 1, "hoch"),
    "2kg_c04": ("rz", "unten", "vertikal", 1, "hoch"),
    "2kg_c05": ("rz", "unten", "horizontal", 2, "hoch"),
    "2kg_c06": ("rz", "oben", "horizontal", 1, "hoch"),
    "2kg_c07": ("rz", "rechts", "horizontal", 2, "hoch"),
    "2kg_c08": ("rz", "links", "vertikal", 1, "hoch"),
    "2kg_c09": ("rz", "links", "vertikal", 2, "hoch"),
    "2kg_c10": ("rz", "rechts", "vertikal", 1, "mittel"),   # abgewinkelter Pfeil
    "2kg_c11": ("rz", "oben", "horizontal", 1, "hoch"),
    "2kg_c12": ("rz", "oben", "horizontal", 1, "hoch"),
    "2kg_c13": ("rz", "unten", "horizontal", 1, "hoch"),
    "2kg_c14": ("sl", None, "horizontal", 1, "hoch"),       # X-Rechteck
    "2kg_c15": ("rz", "rechts", "vertikal", 1, "mittel"),   # abgewinkelter Pfeil
    "2kg_c16": ("rz", "oben", "horizontal", 1, "hoch"),
    "2kg_c17": ("rz", "unten", "horizontal", 2, "hoch"),
    "2kg_c18": ("rz", "links", "vertikal", 2, "hoch"),
    "2kg_c19": ("rz", "oben", "vertikal", 2, "hoch"),
    "2kg_c20": ("rz", "oben", "vertikal", 1, "mittel"),     # abgewinkelter Pfeil
    "2kg_c21": ("rz", "oben", "horizontal", 1, "hoch"),
    "2kg_c22": ("rz", "oben", "vertikal", 1, "hoch"),
    "2kg_c23": ("rz", "rechts", "horizontal", 1, "hoch"),
    "2kg_c24": ("sl", None, "horizontal", 1, "hoch"),       # X-Rechteck
    "2kg_c25": ("rz", "rechts", "vertikal", 1, "mittel"),   # wie c15 (Symmetrie-Zwilling)
}

# Türmaß-Texte, deren Nähe als „an Tür" zählt (GU-Plan schreibt Breite/Höhe ans Blatt).
_TUERMASSE = {"80", "90", "100", "200"}


def _ist_nb_gruen(c) -> bool:
    for key in ("stroking_color", "non_stroking_color"):
        v = c.get(key)
        if v and not isinstance(v, (int, float)):
            try:
                r, g, b = float(v[0]), float(v[1]), float(v[2])
            except (TypeError, ValueError, IndexError):
                continue
            if abs(r) < 0.05 and abs(g - 0.722) < 0.05 and abs(b) < 0.05:
                return True
    return False


def _cluster(boxes: list[tuple], gap: float) -> dict[int, list[tuple]]:
    parent = list(range(len(boxes)))

    def find(i: int) -> int:
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            a, b = boxes[i], boxes[j]
            if not (a[2] + gap < b[0] or b[2] + gap < a[0]
                    or a[3] + gap < b[1] or b[3] + gap < a[1]):
                parent[find(i)] = find(j)
    out: dict[int, list[tuple]] = {}
    for i, b in enumerate(boxes):
        out.setdefault(find(i), []).append(b)
    return out


def analysiere(floor: str) -> dict:
    pfad = BASIS / DATEIEN[floor]
    with pdfplumber.open(pfad) as pdf:
        page = pdf.pages[0]
        prims = [c for c in page.curves + page.lines + page.rects
                 if c["x1"] < PLANFELD_MAX_X_PT and _ist_nb_gruen(c)]
        boxes = [(c["x0"], c["top"], c["x1"], c["bottom"]) for c in prims]
        cluster = _cluster(boxes, CLUSTER_GAP_PT)
        worte = page.extract_words()

    eintraege = []
    for members in cluster.values():
        x0 = min(m[0] for m in members); y0 = min(m[1] for m in members)
        x1 = max(m[2] for m in members); y1 = max(m[3] for m in members)
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        nah = sorted(
            (w for w in worte
             if abs((w["x0"] + w["x1"]) / 2 - cx) < 60
             and abs((w["top"] + w["bottom"]) / 2 - cy) < 40),
            key=lambda w: ((w["x0"] + w["x1"]) / 2 - cx) ** 2
            + ((w["top"] + w["bottom"]) / 2 - cy) ** 2,
        )
        tuermass = next((w for w in nah if w["text"] in _TUERMASSE), None)
        raum = next((w["text"] for w in nah
                     if any(ch.isalpha() for ch in w["text"]) and len(w["text"]) >= 3), None)
        eintraege.append({
            "zentrum_pt": (cx, cy),
            "bbox_pt": (x0, y0, x1, y1),  # intern für crops(), NICHT in die Fixture
            "xy_mm": [round(cx * PT_ZU_MM_MODELL, 1),
                      round((SEITE_H_PT - cy) * PT_ZU_MM_MODELL, 1)],
            "naechste_tuer_mm": (
                round((((tuermass["x0"] + tuermass["x1"]) / 2 - cx) ** 2
                       + ((tuermass["top"] + tuermass["bottom"]) / 2 - cy) ** 2) ** 0.5
                      * PT_ZU_MM_MODELL)
                if tuermass else None),
            "raum_text": raum,
        })
    eintraege.sort(key=lambda e: (e["zentrum_pt"][1], e["zentrum_pt"][0]))

    symbole = []
    crop_boxes: list[tuple[str, tuple]] = []
    unklassifiziert = 0
    for i, e in enumerate(eintraege):
        cid = f"{floor.lower()}_c{i:02d}"
        crop_boxes.append((cid, e["bbox_pt"]))
        kind, richtung, montage, n, konf = SICHT.get(
            cid, ("unbekannt", None, None, 1, "niedrig"))
        if cid not in SICHT:
            unklassifiziert += 1
        for k in range(n):
            symbole.append({
                "id": f"{cid}" + (f"_{k}" if n > 1 else ""),
                "kind": kind,
                "xy_mm": e["xy_mm"],
                "richtung": richtung,
                "montage": montage,
                "naechste_tuer_mm": e["naechste_tuer_mm"],
                "raum_text": e["raum_text"],
                "konfidenz": konf,
                "crop": f"reports/mollgasse_ug/{floor}/{cid}.png",
            })
    ref = {
        "_source": (
            f"GU-Plan {DATEIEN[floor]}, Seite 1, Maßstab 1:{MASSSTAB}, "
            f"kalibriert {PT_ZU_MM_MODELL:.4f} mm/pt "
            f"(CropBox-Gegenprobe 1730x743-Rahmen < 0.1 %), erfasst {ERFASST}"
        ),
        "_koordinaten": "mm Modell, Ursprung = linke untere MediaBox-Ecke, y nach oben",
        "floor": floor,
        "symbole": symbole,
        "_unklassifiziert": unklassifiziert,
    }
    return ref, crop_boxes


def crops(floor: str, eintraege_pt: list[tuple], out: Path) -> None:
    pfad = BASIS / DATEIEN[floor]
    doc = pdfium.PdfDocument(str(pfad))
    fp = doc[0]
    fp.set_cropbox(0, 0, SEITE_H_PT, 5102)  # MediaBox unrotiert (Hochformat)
    s = 4.0
    bild = fp.render(scale=s).to_pil()
    out.mkdir(parents=True, exist_ok=True)
    for cid, (x0, y0, x1, y1) in eintraege_pt:
        pad = 30
        box = (max(0, int((x0 - pad) * s)), max(0, int((y0 - pad) * s)),
               min(bild.width, int((x1 + pad) * s)), min(bild.height, int((y1 + pad) * s)))
        bild.crop(box).save(out / f"{cid}.png")


def main() -> None:
    floors = sys.argv[1:] or list(DATEIEN)
    for floor in floors:
        ref, crop_boxes = analysiere(floor)
        ziel = Path(f"tests/fixtures/mollgasse_ug_referenz_{floor.lower()}.json")
        ziel.write_text(json.dumps(ref, indent=1, ensure_ascii=False), encoding="utf-8")
        # Sicht-Crops regenerieren (reports/ gitignored) — macht die
        # Sicht-Klassifikation reproduzierbar (Review-Befund 2026-09-07: crops()
        # war vorher unaufgerufen). Nach dem Fixture-Write, damit ein Crop-Fehler
        # die Fixture nicht verliert.
        crops(floor, crop_boxes, Path(f"reports/mollgasse_ug/{floor}"))
        arten: dict[str, int] = {}
        for s in ref["symbole"]:
            arten[s["kind"]] = arten.get(s["kind"], 0) + 1
        print(f"{floor}: {len(ref['symbole'])} Leuchten {arten} "
              f"(unklassifiziert: {ref['_unklassifiziert']}) -> {ziel} "
              f"(+{len(crop_boxes)} Crops)")


if __name__ == "__main__":
    main()
