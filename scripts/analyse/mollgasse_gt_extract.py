"""mollgasse_gt_extract.py — Ground-Truth-Extraktor für die Mollgasse-Erklärungs-DXFs.

Liest die Owner-Erklärungs-DXFs (`knowledge/Pläne zeichnen Wissen/
Mollgasse-Notbeleuchtungserklärung/WHA_MOL_<G>_Notbeleuchtung_Erklärung.dxf`)
und schreibt je Geschoss eine strukturierte Ground-Truth-JSON nach
`tests/fixtures/mollgasse_gt/<G>.json` — die Eval-Basis für den
Engine↔Experten-Vergleich (Koordinaten sind hier als TEST-/EVAL-DATEN erlaubt,
nie als Production-Logik).

Messkonventionen (NB-R00, kalibriert Phase B 2026-09-18):
- Position = Bbox-Zentrum der SICHTBAREN Geometrie (`ezdxf.bbox` über den
  aufgelösten INSERT) — die Einfügepunkte tragen Basispunkt-Offsets > 1 km.
- „Pfeil nach unten/links/rechts" bezeichnet den Block-TYP; Welt-Pfeil =
  Blockbasis (down 270° / left 180° / right 0°, an den Erklärungs-Blöcken
  gemessen) + INSERT-Rotation; xscale < 0 spiegelt die Basis an der Y-Achse
  des Block-Rahmens (links ↔ rechts).
- Personen-Läufer (Block 750298750 bzw. nested 9809550): Blick = 180° + rot
  bei xscale > 0, sonst rot (Regel #8 — NIE die rohe rot lesen).
- Beidseitige Rettungszeichen zeichnet der Owner als ZWEI ko-lokalisierte
  Einzel-Blöcke — Paare mit Bbox-Zentren < _BEIDSEITIG_RADIUS_MM gelten als
  EIN beidseitiges Zeichen (`beidseitig_gruppe`).

Aufruf:
    python scripts/analyse/mollgasse_gt_extract.py            # alle 8 Geschosse
    python scripts/analyse/mollgasse_gt_extract.py EG 1KG     # Auswahl
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import ezdxf
import ezdxf.bbox as ezbbox

REPO = Path(__file__).resolve().parents[2]
QUELL_DIR = REPO / "knowledge" / "Pläne zeichnen Wissen" / "Mollgasse-Notbeleuchtungserklärung"
OUT_DIR = REPO / "tests" / "fixtures" / "mollgasse_gt"

GESCHOSSE = ["EG", "1OG", "2OG", "3OG", "4OG", "DG", "1KG", "2KG"]

# Blockname (lowercase) → (typ, richtung_block, basis_deg). Die Erklärungs-DXFs
# tragen die VOR-Rivoplan-Blocknamen — das ist Ground-Truth-Bestand, kein
# Production-Pfad (die Engine rendert seit 2026-09-20 RIVO_NL_ARR_*).
NB_BLOCKS: dict[str, tuple[str, str | None, float | None]] = {
    "rivo-sibel-arr-down": ("rz", "down", 270.0),
    "rivo-sibel-arr-left": ("rz", "left", 180.0),
    "rivo-rz-arr_right": ("rz", "right", 0.0),
    "rivo_nl_arr_down": ("rz", "down", 270.0),
    "rivo_nl_arr_left": ("rz", "left", 180.0),
    "rivo_nl_arr_right": ("rz", "right", 0.0),
    "rivo_nl_arr_bothsided": ("rz", "bothsided", None),
    "antipanikleuchte-rivo": ("antipanik", None, None),
    "aufheller notbeleuchtung": ("aufheller", None, None),
    "sicherheitsleuchte aufheller": ("aufheller", None, None),
    "spot notbeleuchtung": ("spot", None, None),
    "gruppenbatterie-verteiler": ("anlage", None, None),
}

_PERSON_BLOCKS = {"750298750", "9809550"}
_FLUCHTWEG_TRUE_COLOR = 0x21DF37
# Fluchtweg-Grün variiert je Erklärungs-DXF: EG true_color 0x21DF37 / ACI 102,
# 1KG ACI 100 (Abgleich-Befund 2026-09-20).
_FLUCHTWEG_ACIS = {100, 102}
# HINWEIS: n_sichtlinien ist eine ROH-Zählung aller ACI-4-Linien — Architektur-
# Cyan (Schnittmarken etc.) zählt mit; die kuratierte Zählung steht im
# jeweiligen abgleich/<G>/abgleich_<G>.md.
_SICHTLINIE_ACI = 4          # cyan/türkis = Blickwinkel/Sichtverbindung
_LABEL_ACIS = {3, 100, 102}  # grüne (M)TEXT-Labels (A), (B), …
# Zwei ~636-mm-Schilder Rücken an Rücken: Bbox-Zentren liegen bis ~650 mm
# auseinander; echte Nachbar-RZ im Gang stehen > 2 m (SL<2m-Merge-Regel).
_BEIDSEITIG_RADIUS_MM = 700.0


def _welt_pfeil(basis: float | None, rot: float, xscale: float) -> float | None:
    if basis is None:
        return None
    if xscale < 0:
        basis = (180.0 - basis) % 360.0
    return (basis + rot) % 360.0


def _bbox_zentrum(entity) -> tuple[float, float] | None:
    ext = ezbbox.extents([entity], fast=False)
    if not ext.has_data:
        return None
    return (round(ext.center.x, 1), round(ext.center.y, 1))


def _farbe(e) -> int | None:
    return getattr(e.dxf, "color", None)


def _ist_fluchtweg(e) -> bool:
    tc = getattr(e.dxf, "true_color", None)
    return tc == _FLUCHTWEG_TRUE_COLOR or _farbe(e) in _FLUCHTWEG_ACIS


def extrahiere(geschoss: str) -> dict:
    pfad = QUELL_DIR / f"WHA_MOL_{geschoss}_Notbeleuchtung_Erklärung.dxf"
    doc = ezdxf.readfile(str(pfad))
    ms = doc.modelspace()

    leuchten: list[dict] = []
    personen: list[dict] = []
    labels: list[dict] = []
    fluchtweg_pl = 0
    sichtlinien = 0

    for e in ms:
        typ = e.dxftype()
        if typ == "INSERT":
            name = e.dxf.name.strip().lower()
            if name in NB_BLOCKS:
                kind, richtung, basis = NB_BLOCKS[name]
                xy = _bbox_zentrum(e)
                rot = float(e.dxf.rotation) % 360.0
                xs = float(e.dxf.xscale)
                leuchten.append({
                    "handle": e.dxf.handle,
                    "block": e.dxf.name,
                    "typ": kind,
                    "richtung_block": richtung,
                    "xy_mm": xy,
                    "insert_xy_mm": (round(e.dxf.insert.x, 1), round(e.dxf.insert.y, 1)),
                    "rot_deg": round(rot, 2),
                    "xscale": round(xs, 4),
                    "welt_pfeil_deg": (round(w, 2) if (w := _welt_pfeil(basis, rot, xs)) is not None else None),
                    "layer": e.dxf.layer,
                })
            elif e.dxf.name in _PERSON_BLOCKS:
                xy = _bbox_zentrum(e)
                rot = float(e.dxf.rotation) % 360.0
                xs = float(e.dxf.xscale)
                blick = (180.0 + rot) % 360.0 if xs > 0 else rot % 360.0
                personen.append({
                    "handle": e.dxf.handle,
                    "xy_mm": xy,
                    "rot_deg": round(rot, 2),
                    "xscale": round(xs, 4),
                    "blick_deg": round(blick, 2),
                })
        elif typ in ("MTEXT", "TEXT"):
            text = (e.text if typ == "MTEXT" else e.dxf.text).strip()
            if not text or len(text) > 40:
                continue
            if _farbe(e) in _LABEL_ACIS or _ist_fluchtweg(e):
                p = e.dxf.insert
                labels.append({
                    "text": text,
                    "xy_mm": (round(p.x, 1), round(p.y, 1)),
                    "handle": e.dxf.handle,
                })
        elif typ == "LWPOLYLINE" and _ist_fluchtweg(e):
            fluchtweg_pl += 1
        elif typ in ("LINE", "LWPOLYLINE") and _farbe(e) == _SICHTLINIE_ACI:
            sichtlinien += 1

    # Beidseitig-Gruppen: ko-lokalisierte RZ-Paare (< _BEIDSEITIG_RADIUS_MM).
    rz = [l for l in leuchten if l["typ"] == "rz" and l["xy_mm"]]
    gruppe = 0
    for i, a in enumerate(rz):
        if "beidseitig_gruppe" in a:
            continue
        for b in rz[i + 1:]:
            if "beidseitig_gruppe" in b or b["xy_mm"] is None:
                continue
            if math.dist(a["xy_mm"], b["xy_mm"]) < _BEIDSEITIG_RADIUS_MM:
                gruppe += 1
                a["beidseitig_gruppe"] = b["beidseitig_gruppe"] = gruppe

    return {
        "geschoss": geschoss,
        "quelle": str(pfad.relative_to(REPO)),
        "n_leuchten": len(leuchten),
        "n_beidseitig_gruppen": gruppe,
        "leuchten": leuchten,
        "personen": personen,
        "labels": labels,
        "n_fluchtweg_polylines": fluchtweg_pl,
        "n_sichtlinien": sichtlinien,
    }


def main(argv: list[str]) -> int:
    geschosse = argv or GESCHOSSE
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for g in geschosse:
        daten = extrahiere(g)
        out = OUT_DIR / f"{g}.json"
        out.write_text(json.dumps(daten, ensure_ascii=False, indent=1), encoding="utf-8")
        bs = daten["n_beidseitig_gruppen"]
        print(f"{g}: {daten['n_leuchten']} Leuchten ({bs} beidseitig-Paare), "
              f"{len(daten['personen'])} Personen, {len(daten['labels'])} Labels, "
              f"{daten['n_fluchtweg_polylines']} Fluchtweg-PL -> {out.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
