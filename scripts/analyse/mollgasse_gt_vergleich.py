"""mollgasse_gt_vergleich.py — Engine-Output ↔ Experten-Ground-Truth je Geschoss.

Der wichtigste Real-Test des Ground-Truth-Harness (Owner-Auftrag 2026-09-20):

1. LEERER Architektur-DXF (`Projekte_Leere Architektpläne (Input)/Mollgasse/`)
   → echte Provider (`registry.build_default_bundle`) → `pipeline.run`
   → PlatzierungsErgebnis (Engine-Frame, mm).
2. Ground-Truth (`tests/fixtures/mollgasse_gt/<G>.json`, Erklärungs-Frame)
   wird über eine GEMESSENE Translation in den Engine-Frame geholt:
   die leeren Pläne sind in Metern gezeichnet (INSUNITS behauptet mm),
   Selmans Erkennung skaliert ×1000; die Translation kommt aus dem Matching
   gleichnamiger Architektur-INSERTs beider Dateien (Median-Differenz je
   Blockname mit identischer Instanzzahl, Median über die Namen — exakt für
   identische Multisets, robust gegen Einzelausreißer).
3. Paarung GT-Leuchte ↔ Engine-Platzierung je Symbolklasse (rz /
   sicherheitsleuchte / antipanik) via Nearest-Neighbor. `_PAIR_RADIUS_MM`
   ist ein reiner PAARUNGS-Radius (dokumentiert), KEINE Pass-Toleranz —
   alle Distanzen werden metrisch berichtet (Repo-Konvention: keine
   erfundenen Toleranzen).
4. Klassifikation nach den Owner-Kategorien: position_abweichung (gepaart,
   mit Distanz/Rotations-Delta), fehlt (GT ohne Engine-Partner),
   ueberfluessig (Engine ohne GT-Partner), beidseitig_abweichung.
5. Zusätzlich (G3): Lux-Nachweis auf dem EXPERTEN-Placement — GT →
   PlatzierungsErgebnis (eval-only!) → `lux_nachweis_bericht.schreibe_bericht`
   mit echter Photometrie (`bundle.platzierer._i_cd_fn`).

Ausgabe: `Projekte/_ergebnis/Mollgasse_GT/<G>/vergleich.json` + `bericht.md`
+ `gt_lux_nachweis.png`. Aufruf je Geschoss (Batches ≤ 10 min!):

    python scripts/analyse/mollgasse_gt_vergleich.py EG
    python scripts/analyse/mollgasse_gt_vergleich.py 1KG 2KG
"""
from __future__ import annotations

import json
import math
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "src"))

LEER_DIR = REPO / "Projekte_Leere Architektpläne (Input)" / "Mollgasse"
GT_DIR = REPO / "tests" / "fixtures" / "mollgasse_gt"
ERKL_DIR = REPO / "knowledge" / "Pläne zeichnen Wissen" / "Mollgasse-Notbeleuchtungserklärung"
OUT_DIR = REPO / "Projekte" / "_ergebnis" / "Mollgasse_GT"

LEER_DATEI = {
    "EG": "Erdgeschoß.dxf", "1OG": "1.Obergeschoß.dxf", "2OG": "2.Obergeschoß.dxf",
    "3OG": "3.Obergeschoß.dxf", "4OG": "4.Obergeschoß.dxf", "DG": "Dachgeschoß.dxf",
    "1KG": "1.Kellergeschoß.dxf", "2KG": "2.Kellergeschoß.dxf",
}

# Die leeren Pläne sind in METERN gezeichnet (Befund 2026-09-20; INSUNITS=4
# behauptet mm) — Selmans Erkennung skaliert auf mm, wir spiegeln das hier.
_LEER_SKALA = 1000.0
# Reiner Paarungs-Radius fürs Nearest-Neighbor-Matching (keine Pass-Toleranz).
_PAIR_RADIUS_MM = 3000.0

# GT-typ → Vergleichsklasse (Engine-`kind`).
_TYP_KLASSE = {"rz": "rz", "aufheller": "sicherheitsleuchte",
               "spot": "sicherheitsleuchte", "antipanik": "antipanik"}


def _transform(geschoss: str) -> tuple[float, float, dict]:
    """Translation Erklärungs-Frame → Engine-Frame (leer × 1000), gemessen."""
    import ezdxf

    erkl = ezdxf.readfile(str(ERKL_DIR / f"WHA_MOL_{geschoss}_Notbeleuchtung_Erklärung.dxf"))
    leer = ezdxf.readfile(str(LEER_DIR / LEER_DATEI[geschoss]))

    def punkte(doc, skala):
        pts: dict[str, list[tuple[float, float]]] = defaultdict(list)
        for e in doc.modelspace().query("INSERT"):
            p = e.dxf.insert
            pts[e.dxf.name.strip().lower()].append((p.x * skala, p.y * skala))
        return pts

    pe, pl = punkte(erkl, 1.0), punkte(leer, _LEER_SKALA)
    dx_kand, dy_kand, namen = [], [], []
    for name, le in pl.items():
        ee = pe.get(name)
        if not ee or len(ee) != len(le) or len(le) > 60:
            continue
        dx = statistics.median(p[0] for p in ee) - statistics.median(p[0] for p in le)
        dy = statistics.median(p[1] for p in ee) - statistics.median(p[1] for p in le)
        dx_kand.append(dx)
        dy_kand.append(dy)
        namen.append(name)
    if not dx_kand:
        raise RuntimeError(f"{geschoss}: keine gemeinsamen Architektur-INSERTs — Frame nicht auflösbar")
    tx, ty = statistics.median(dx_kand), statistics.median(dy_kand)
    inlier = [n for n, dx, dy in zip(namen, dx_kand, dy_kand)
              if abs(dx - tx) < 500 and abs(dy - ty) < 500]
    return tx, ty, {"n_namen": len(namen), "n_inlier": len(inlier),
                    "tx_mm": round(tx, 1), "ty_mm": round(ty, 1)}


def _gt_einheiten(gt: dict, tx: float, ty: float) -> list[dict]:
    """GT-Leuchten in Engine-Frame; beidseitig-Paare zu EINER Einheit kollabiert."""
    einheiten, gruppen = [], {}
    for l in gt["leuchten"]:
        if l["typ"] == "anlage" or not l["xy_mm"]:
            continue
        x, y = l["xy_mm"][0] - tx, l["xy_mm"][1] - ty
        g = l.get("beidseitig_gruppe")
        eintrag = {"handle": l["handle"], "typ": l["typ"], "klasse": _TYP_KLASSE[l["typ"]],
                   "richtung_block": l.get("richtung_block"),
                   "welt_pfeil_deg": l.get("welt_pfeil_deg"),
                   "rot_deg": l.get("rot_deg"), "x": x, "y": y,
                   "beidseitig": bool(g)}
        if g:
            gruppen.setdefault(g, []).append(eintrag)
        else:
            einheiten.append(eintrag)
    for g, paar in gruppen.items():
        einheiten.append({
            "handle": "+".join(p["handle"] for p in paar), "typ": "rz",
            "klasse": "rz", "richtung_block": "beidseitig",
            "welt_pfeil_deg": None, "rot_deg": paar[0]["rot_deg"],
            "x": sum(p["x"] for p in paar) / len(paar),
            "y": sum(p["y"] for p in paar) / len(paar), "beidseitig": True,
        })
    return einheiten


def _vergleiche(geschoss: str, output, gt_einheiten: list[dict]) -> dict:
    engine = [{"i": i, "klasse": p.kind, "x": p.xy_mm[0], "y": p.xy_mm[1],
               "rot": p.rotation_deg, "richtung": p.richtung,
               "beidseitig": (p.richtung == "gerade" and p.kind == "rz"),
               "key": p.catalog_key}
              for i, p in enumerate(output.platzierung.platzierungen)]
    frei = {e["i"] for e in engine}
    paare, fehlt = [], []
    for g in gt_einheiten:
        kand = [e for e in engine if e["i"] in frei and e["klasse"] == g["klasse"]]
        if not kand:
            fehlt.append(g)
            continue
        best = min(kand, key=lambda e: math.dist((e["x"], e["y"]), (g["x"], g["y"])))
        d = math.dist((best["x"], best["y"]), (g["x"], g["y"]))
        if d > _PAIR_RADIUS_MM:
            fehlt.append(g)
            continue
        frei.discard(best["i"])
        rot_delta = None
        if g.get("welt_pfeil_deg") is not None and best["klasse"] == "rz":
            # Engine-Welt-Pfeil aus richtung (Ziel-Richtung) approximieren wir
            # NICHT — wir vergleichen die INSERT-Rotationen direkt nur, wenn
            # beide down-Basis tragen; sonst nur Distanz (metrisch ehrlich).
            rot_delta = round(abs(((best["rot"] - g["rot_deg"]) + 180) % 360 - 180), 1)
        paare.append({
            "gt": g["handle"], "gt_typ": g["typ"], "gt_richtung": g["richtung_block"],
            "engine_key": best["key"], "engine_richtung": best["richtung"],
            "distanz_mm": round(d, 1), "rot_delta_deg": rot_delta,
            "beidseitig_gt": g["beidseitig"], "beidseitig_engine": best["beidseitig"],
        })
    ueberfluessig = [e for e in engine if e["i"] in frei]
    dists = [p["distanz_mm"] for p in paare]
    return {
        "geschoss": geschoss,
        "engine_n": len(engine),
        "engine_by_kind": dict(Counter(e["klasse"] for e in engine)),
        "gt_n": len(gt_einheiten),
        "gt_by_klasse": dict(Counter(g["klasse"] for g in gt_einheiten)),
        "gepaart": len(paare),
        "fehlt_n": len(fehlt),
        "ueberfluessig_n": len(ueberfluessig),
        "distanz_median_mm": round(statistics.median(dists), 1) if dists else None,
        "distanz_max_mm": round(max(dists), 1) if dists else None,
        "beidseitig_treffer": sum(1 for p in paare if p["beidseitig_gt"] and p["beidseitig_engine"]),
        "beidseitig_gt_gesamt": sum(1 for g in gt_einheiten if g["beidseitig"]),
        "paare": paare,
        "fehlt": [{"handle": g["handle"], "typ": g["typ"],
                   "richtung": g["richtung_block"],
                   "xy": [round(g["x"], 1), round(g["y"], 1)]} for g in fehlt],
        "ueberfluessig": [{"key": e["key"], "klasse": e["klasse"],
                           "xy": [round(e["x"], 1), round(e["y"], 1)]}
                          for e in ueberfluessig],
        "pair_radius_mm": _PAIR_RADIUS_MM,
    }


def _gt_platzierungsergebnis(geschoss: str, gt_einheiten: list[dict]):
    """GT → PlatzierungsErgebnis (EVAL-ONLY: Koordinaten sind Testdaten)."""
    from notbeleuchtung.hauptengine.contracts import Platzierung, PlatzierungsErgebnis

    key_map = {"down": "notlicht_ks_stiege_unten", "left": "notlicht_ks_stiege_links",
               "right": "notlicht_ks_stiege_rechts", "beidseitig": "notlicht_ks_stiege"}
    plz = []
    for g in gt_einheiten:
        if g["typ"] == "rz":
            key = key_map.get(g["richtung_block"] or "down", "notlicht_ks_stiege_unten")
            richtung = "gerade" if g["beidseitig"] else None
        elif g["typ"] == "antipanik":
            key, richtung = "antipanik_leuchte", "gerade"
        elif g["typ"] == "spot":
            key, richtung = "sicherheitsleuchte_spot", "gerade"
        else:
            key, richtung = "sicherheitsleuchte_aufheller", "gerade"
        kwargs = {"xy_mm": (g["x"], g["y"]), "catalog_key": key,
                  "kind": g["klasse"], "rotation_deg": g.get("rot_deg") or 0.0}
        if richtung:
            kwargs["richtung"] = richtung
        plz.append(Platzierung(**kwargs))
    return PlatzierungsErgebnis(floor=geschoss, platzierungen=plz)


def lauf(geschoss: str) -> None:
    from notbeleuchtung.hauptengine import pipeline, registry

    out_dir = OUT_DIR / geschoss
    out_dir.mkdir(parents=True, exist_ok=True)
    bundle = registry.build_default_bundle()
    leer = LEER_DIR / LEER_DATEI[geschoss]
    print(f"[{geschoss}] Engine-Lauf auf leerem Input: {leer.name}")
    output = pipeline.run(bundle, str(leer), geschoss)

    tx, ty, tinfo = _transform(geschoss)
    print(f"[{geschoss}] Frame-Transform: T=({tinfo['tx_mm']}, {tinfo['ty_mm']}) "
          f"aus {tinfo['n_inlier']}/{tinfo['n_namen']} Namen")

    gt = json.loads((GT_DIR / f"{geschoss}.json").read_text(encoding="utf-8"))
    einheiten = _gt_einheiten(gt, tx, ty)
    ergebnis = _vergleiche(geschoss, output, einheiten)
    ergebnis["transform"] = tinfo
    ergebnis["engine_summary"] = {k: output.render_summary.get(k)
                                  for k in ("n_symbols", "by_kind", "n_raeume")}

    # G3: Lux auf dem Experten-Placement (echte Photometrie, nichts erfinden).
    try:
        from notbeleuchtung.hauptengine.render.lux_nachweis_bericht import schreibe_bericht
        gt_plz = _gt_platzierungsergebnis(geschoss, einheiten)
        bericht = schreibe_bericht(
            output.raum, gt_plz, bundle.norm, out_dir / "gt_lux_nachweis.png",
            i_cd_fn=getattr(bundle.platzierer, "_i_cd_fn", None),
            projekt=f"Mollgasse {geschoss} — Experten-Ground-Truth",
        )
        ergebnis["gt_lux_nachweis"] = str(bericht) if bericht else None
    except Exception as e:  # noqa: BLE001 — Lux additiv, Vergleich bleibt gültig
        ergebnis["gt_lux_fehler"] = str(e)

    (out_dir / "vergleich.json").write_text(
        json.dumps(ergebnis, ensure_ascii=False, indent=1), encoding="utf-8")
    zeilen = [
        f"# Mollgasse {geschoss} — Engine vs. Experten-Ground-Truth",
        "",
        f"- Engine: {ergebnis['engine_n']} Platzierungen {ergebnis['engine_by_kind']}",
        f"- Ground Truth: {ergebnis['gt_n']} Einheiten {ergebnis['gt_by_klasse']}"
        f" (beidseitig: {ergebnis['beidseitig_gt_gesamt']})",
        f"- gepaart: {ergebnis['gepaart']} (Median {ergebnis['distanz_median_mm']} mm,"
        f" Max {ergebnis['distanz_max_mm']} mm; Paarungs-Radius {int(_PAIR_RADIUS_MM)} mm)",
        f"- fehlt (GT ohne Engine): {ergebnis['fehlt_n']}",
        f"- ueberfluessig (Engine ohne GT): {ergebnis['ueberfluessig_n']}",
        f"- beidseitig getroffen: {ergebnis['beidseitig_treffer']}/{ergebnis['beidseitig_gt_gesamt']}",
        f"- Lux auf GT: {ergebnis.get('gt_lux_nachweis') or ergebnis.get('gt_lux_fehler', '-')}",
        "",
        "Details: vergleich.json",
    ]
    (out_dir / "bericht.md").write_text("\n".join(zeilen), encoding="utf-8")
    print(f"[{geschoss}] gepaart {ergebnis['gepaart']}/{ergebnis['gt_n']}, "
          f"fehlt {ergebnis['fehlt_n']}, ueberfluessig {ergebnis['ueberfluessig_n']}, "
          f"Median {ergebnis['distanz_median_mm']} mm -> {out_dir.relative_to(REPO)}")


def main(argv: list[str]) -> int:
    for g in argv or list(LEER_DATEI):
        lauf(g)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
