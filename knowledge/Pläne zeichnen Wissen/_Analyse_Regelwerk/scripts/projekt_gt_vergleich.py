# -*- coding: utf-8 -*-
"""projekt_gt_vergleich.py — Engine vs. Referenz-Evidenz für Projekte 2–5.

Analog `scripts/analyse/mollgasse_gt_vergleich.py`, aber generisch:
GT = evidenz/<Projekt>/<Datei>.json (extract_erklaerung.py), Input = leerer
Architekturplan aus `Projekte_Leere Architektpläne (Input)/<Ordner>/`.
Frame-Transform über gleichnamige Architektur-INSERTs (Median-Differenz).
Kennzahlen: gepaart/fehlt/überflüssig + Typ-Match + ERREICHBAR-Modus
(GT in erkannten Raum-/Zirkulations-Geometrien). KONFLIKTE-rückführbare
Abweichungen zählen nicht als Fehler (Auftrag Schritt 5.4).

Aufruf:  python projekt_gt_vergleich.py Tomaschek [SG EG OG] …
Output:  _Analyse_Regelwerk/validierung/<Projekt>/<G>/vergleich.json + bericht.md
"""
from __future__ import annotations

import json
import math
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

HIER = Path(__file__).resolve()
BASIS = HIER.parents[1]
WISSEN = HIER.parents[2]
REPO = HIER.parents[4]
sys.path.insert(0, str(REPO / "src"))

LEER_BASIS = REPO / "Projekte_Leere Architektpläne (Input)"
OUT = BASIS / "validierung"

_PAIR_RADIUS_MM = 3000.0
_TYP_KLASSE = {"rz": "rz", "aufheller": "sicherheitsleuchte",
               "spot": "sicherheitsleuchte", "antipanik": "antipanik"}
_RICHTUNG_MAP = {"down": "unten", "left": "links", "right": "rechts"}

PROJEKTE: dict[str, dict] = {
    "Tomaschek": {
        "leer_dir": "Tomaschek-Schule",
        "leer": {"EG": "SH21-TOM44-AR0-AP-EG-01-1 Erdgeschoss.dxf",
                 "OG": "SH21-TOM44-AR0-AP-OG-1 1. Obergeschoss.dxf",
                 "SG": "SH21-TOM44-AR0-AP-SG-01-1 Sockelgeschoss.dxf"},
        "gt": {"EG": "EG_RIVO_Erklaerung.json", "OG": "OG_RIVO_Erklaerung.json",
               "SG": "SG_RIVO_Erklaerung.json"},
        "gt_dxf_dir": "Tomaschek-Schule -Notbeleuchtungserklärung",
    },
    "AmRain": {
        "leer_dir": "Am Rain",
        "leer": {"UG": "ARAI5_FE_XEL_ZZ_MOP_UG_0010_V_02.dxf",
                 "EG": "ARAI5_FE_XEL_ZZ_MOP_EG_0011_V_02.dxf",
                 "OG1": "ARAI5_FE_XEL_ZZ_MOP_OG1_0012_V_01.dxf",
                 "OG2": "ARAI5_FE_XEL_ZZ_MOP_OG2_0013_V_01.dxf",
                 "OG3": "ARAI5_FE_XEL_ZZ_MOP_OG3_0014_V_01.dxf",
                 "OG4": "ARAI5_FE_XEL_ZZ_MOP_OG4_0015_V_01.dxf"},
        "gt": {"UG": "ARAI5_FE_XEL_ZZ_MOP_UG_0010_V_02_RIVO_Symbole_TEILSTAND_v2.json",
               "EG": "ARAI5_FE_XEL_ZZ_MOP_EG_0011_V_02_EG_Erklaerung_TEILSTAND_v2.json",
               "OG1": "ARAI5_FE_XEL_ZZ_MOP_OG1_0012_V_01_RIVO_Symbole_TEILSTAND_v2.json",
               "OG2": "ARAI5_FE_XEL_ZZ_MOP_OG2_0013_V_01_RIVO_Symbole_TEILSTAND_v2.json",
               "OG3": "ARAI5_FE_XEL_ZZ_MOP_OG3_0014_V_01_RIVO_Symbole_TEILSTAND_v2.json",
               "OG4": "ARAI5_FE_XEL_ZZ_MOP_OG4_0015_V_01_RIVO_Symbole_TEILSTAND_v2.json"},
        "gt_dxf_dir": "Am Rain Notbeleuchtungserklärung",
    },
    "Hausfeld": {
        "leer_dir": "Hausfeldstraße",
        "leer": {"UG": "1.Elektromontageplan UG_Index A.dxf",
                 "EG": "2.Elektromontageplan EG_Index A.dxf",
                 "1OG": "3.Elektromontageplan 1OG_Index A.dxf",
                 "1DG": "4.Elektromontageplan 1DG_Index A.dxf",
                 "2DG": "5.Elektromontageplan 2DG_Index A.dxf"},
        "gt": {g: f"Hausfeldstraße_{g}_Notbeleuchtung_RIVO.json"
               for g in ("UG", "EG", "1OG", "1DG", "2DG")},
        "gt_dxf_dir": "Hausfeldstraße Notbeleuchtung zeichnen",
    },
    "BaufeldE2": {
        "leer_dir": "Baufeld E2",
        "leer": {"UG": "Elektromontageplan_UG.dxf"},
        "gt": {"UG": "Notbeleuchtungspläne_UG_RIVO_mit_Lehrlayern.json"},
        "gt_dxf_dir": "Baufeld E2 Notbeleuchtung zeichnen",
    },
}


def _transform(leer_pfad: Path, gt_dxf_pfad: Path, leer_skala: float) -> tuple[float, float, dict]:
    import ezdxf

    def punkte(doc, skala):
        pts: dict[str, list[tuple[float, float]]] = defaultdict(list)
        for e in doc.modelspace().query("INSERT"):
            p = e.dxf.insert
            pts[e.dxf.name.strip().lower()].append((p.x * skala, p.y * skala))
        return pts

    pe = punkte(ezdxf.readfile(str(gt_dxf_pfad)), 1.0)
    pl = punkte(ezdxf.readfile(str(leer_pfad)), leer_skala)
    dx_kand, dy_kand, namen = [], [], []
    for name, le in pl.items():
        ee = pe.get(name)
        if not ee or len(ee) != len(le) or len(le) > 80:
            continue
        dx_kand.append(statistics.median(p[0] for p in ee) - statistics.median(p[0] for p in le))
        dy_kand.append(statistics.median(p[1] for p in ee) - statistics.median(p[1] for p in le))
        namen.append(name)
    if not dx_kand:
        raise RuntimeError("keine gemeinsamen Architektur-INSERTs — Frame nicht auflösbar")
    tx, ty = statistics.median(dx_kand), statistics.median(dy_kand)
    inlier = sum(1 for dx, dy in zip(dx_kand, dy_kand)
                 if abs(dx - tx) < 500 and abs(dy - ty) < 500)
    return tx, ty, {"n_namen": len(namen), "n_inlier": inlier,
                    "tx_mm": round(tx, 1), "ty_mm": round(ty, 1)}


def _punkt_in_polygon(x: float, y: float, poly: list) -> bool:
    innen = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i][0], poly[i][1]
        x2, y2 = poly[(i + 1) % n][0], poly[(i + 1) % n][1]
        if (y1 > y) != (y2 > y) and x < x1 + (y - y1) / (y2 - y1) * (x2 - x1):
            innen = not innen
    return innen


def _ist_erreichbar(x: float, y: float, raum_modell) -> bool:
    for r in raum_modell.raeume:
        if r.polygon_mm and _punkt_in_polygon(x, y, r.polygon_mm):
            return True
    nah = 1500.0
    for s in raum_modell.zirkulation.segmente:
        pts = s.polyline_mm
        for i in range(len(pts) - 1):
            (x1, y1), (x2, y2) = pts[i], pts[i + 1]
            dx, dy = x2 - x1, y2 - y1
            l2 = dx * dx + dy * dy
            t = 0.0 if l2 == 0 else max(0.0, min(1.0, ((x - x1) * dx + (y - y1) * dy) / l2))
            if math.dist((x, y), (x1 + t * dx, y1 + t * dy)) <= nah:
                return True
    return False


def _gt_einheiten(gt: dict, tx: float, ty: float) -> list[dict]:
    einheiten, gruppen = [], {}
    for l in gt["leuchten"]:
        if l["typ"] == "anlage" or not l.get("xy_mm"):
            continue
        eintrag = {"handle": l["handle"], "typ": l["typ"],
                   "klasse": _TYP_KLASSE.get(l["typ"], "sicherheitsleuchte"),
                   "richtung_block": l.get("richtung_block"),
                   "rot_deg": l.get("rot_deg"),
                   "x": l["xy_mm"][0] - tx, "y": l["xy_mm"][1] - ty,
                   "beidseitig": bool(l.get("beidseitig_gruppe"))
                   or l.get("richtung_block") == "bothsided"}
        g = l.get("beidseitig_gruppe")
        if g and l.get("richtung_block") != "bothsided":
            gruppen.setdefault(g, []).append(eintrag)
        else:
            einheiten.append(eintrag)
    for paar in gruppen.values():
        einheiten.append({"handle": "+".join(p["handle"] for p in paar), "typ": "rz",
                          "klasse": "rz", "richtung_block": "beidseitig",
                          "rot_deg": paar[0]["rot_deg"],
                          "x": sum(p["x"] for p in paar) / len(paar),
                          "y": sum(p["y"] for p in paar) / len(paar),
                          "beidseitig": True})
    return einheiten


def lauf(projekt: str, geschoss: str) -> dict | None:
    from notbeleuchtung.hauptengine import pipeline, registry

    cfg = PROJEKTE[projekt]
    leer = LEER_BASIS / cfg["leer_dir"] / cfg["leer"][geschoss]
    gt_json = BASIS / "evidenz" / projekt / cfg["gt"][geschoss]
    gt_dxf = WISSEN / cfg["gt_dxf_dir"] / cfg["gt"][geschoss].replace(".json", ".dxf")
    out_dir = OUT / projekt / geschoss
    out_dir.mkdir(parents=True, exist_ok=True)
    ergebnis: dict = {"projekt": projekt, "geschoss": geschoss, "input": leer.name}
    try:
        bundle = registry.build_default_bundle()
        print(f"[{projekt}/{geschoss}] Engine-Lauf: {leer.name}", flush=True)
        output = pipeline.run(bundle, str(leer), geschoss)
        # Skala: Heuristik wie Healthcheck — falls Extents < 1000 → Meter-Plan
        import ezdxf.bbox as ezbbox  # noqa: F401 (Skala kommt aus Selman-Erkennung)
        tx, ty, tinfo = _transform(leer, gt_dxf, 1.0)
        gt = json.loads(gt_json.read_text(encoding="utf-8"))
        einheiten = _gt_einheiten(gt, tx, ty)
        engine = [{"i": i, "klasse": p.kind, "x": p.xy_mm[0], "y": p.xy_mm[1],
                   "richtung": p.richtung,
                   "beidseitig": (p.richtung == "gerade" and p.kind == "rz")}
                  for i, p in enumerate(output.platzierung.platzierungen)]
        frei = {e["i"] for e in engine}
        paare, fehlt = [], []
        for g in einheiten:
            kand = [e for e in engine if e["i"] in frei and e["klasse"] == g["klasse"]]
            best = min(kand, key=lambda e: math.dist((e["x"], e["y"]), (g["x"], g["y"])),
                       default=None)
            if best is None or math.dist((best["x"], best["y"]), (g["x"], g["y"])) > _PAIR_RADIUS_MM:
                fehlt.append(g)
                continue
            frei.discard(best["i"])
            if g["beidseitig"] or best["beidseitig"]:
                typ_match = g["beidseitig"] and best["beidseitig"]
            elif g["klasse"] != "rz":
                typ_match = True
            else:
                typ_match = _RICHTUNG_MAP.get(g["richtung_block"] or "") == best["richtung"]
            paare.append({"gt": g["handle"],
                          "distanz_mm": round(math.dist((best["x"], best["y"]), (g["x"], g["y"])), 1),
                          "typ_match": typ_match})
        erreichbar = [g for g in einheiten if _ist_erreichbar(g["x"], g["y"], output.raum)]
        err_h = {g["handle"] for g in erreichbar}
        ergebnis.update({
            "engine_n": len(engine), "gt_n": len(einheiten),
            "gt_by_klasse": dict(Counter(g["klasse"] for g in einheiten)),
            "gepaart": len(paare),
            "typ_match_n": sum(1 for p in paare if p["typ_match"]),
            "fehlt_n": len(fehlt), "ueberfluessig_n": len(frei),
            "erreichbar_n": len(erreichbar),
            "erreichbar_gepaart": sum(1 for p in paare if p["gt"] in err_h),
            "distanz_median_mm": (round(statistics.median([p["distanz_mm"] for p in paare]), 1)
                                  if paare else None),
            "transform": tinfo, "paare": paare,
            "engine_status": output.render_summary.get("status"),
        })
    except Exception as exc:  # noqa: BLE001 — Crash-Klassen protokollieren, nicht abbrechen
        ergebnis["fehler"] = f"{type(exc).__name__}: {exc}"
        print(f"[{projekt}/{geschoss}] FEHLER: {ergebnis['fehler']}", flush=True)
    (out_dir / "vergleich.json").write_text(
        json.dumps(ergebnis, ensure_ascii=False, indent=1), encoding="utf-8")
    if "fehler" not in ergebnis:
        print(f"[{projekt}/{geschoss}] gepaart {ergebnis['gepaart']}/{ergebnis['gt_n']} "
              f"(erreichbar {ergebnis['erreichbar_gepaart']}/{ergebnis['erreichbar_n']}, "
              f"typ {ergebnis['typ_match_n']}), ueberfluessig {ergebnis['ueberfluessig_n']}",
              flush=True)
    return ergebnis


def main(argv: list[str]) -> int:
    projekt = argv[0] if argv else "Tomaschek"
    geschosse = argv[1:] or list(PROJEKTE[projekt]["leer"])
    for g in geschosse:
        lauf(projekt, g)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
