# ruff: noqa
# Wortgetreu aus docs/DIAGNOSE_RENNWEG_RAUMERKENNUNG.md (Commit 34b5dd0), Anhang A.2 —
# programmatisch aus dem Codeblock extrahiert, nicht abgetippt.
# Abweichungen gegenueber der Diagnose (sonst Byte fuer Byte gleich):
#   1. diese Kopfzeilen (# ruff: noqa + Herkunftsvermerk).
#   2. REPO = Path(os.environ["NOTBEL_REPO"]) statt des hart verdrahteten Benutzerpfads;
#      Pflicht, kein Default (der Docstring nennt den alten Default noch).
#   3. Cache-Wurzel ERG aus NOTBEL_GATE_CACHES, sonst wie bisher
#      REPO / "Projekte" / "_ergebnis_raumerkennung".
#   4. "import os" ergaenzt — Anhang A.2 importiert os nicht.
"""M2-aussen-auf-innenraum — Innenraeume (Fachregel S-C) mit Schnitt zum OFFENEN Aussenbereich.

Aufruf (Repo-venv, nur lesen):
  PY _messen.py [--out <datei.json>]      Default: messung.json neben dem Skript

Grundmenge: jede Projekte/_ergebnis_raumerkennung/**/_cache.pkl (rglob, nichts hart verdrahtet).
DXF: kennzahlen.json "dxf" (relativ zum Repo), sonst Projekte/<relativer Ergebnisordner>.dxf;
     sha256 wird gegen kennzahlen.json geprueft (dxf_sha_ok).
Kein Pipeline-Re-Run. In-memory nur: dxf_load.lade_dxf (Space + Faktor, fuer Bloecke),
wandkoerper.finde_wandkoerper (nur Huelle H2).

Definition:
  Raumpolygon     = Polygon(polygon_mm).buffer(0) wie raumerkennung_darstellung._polygon (leer -> ignoriert)
  AUSSEN          = unary_union(cache["aussen_offen"])   (aussen_geschlossen zaehlt NICHT)
  schnitt_m2      = Flaeche(Raum ∩ AUSSEN) / 1e6
  beruehrt        = schnitt_m2 > SCHNITT_MIN_M2 (0.05); gross = schnitt_m2 > SCHNITT_GROSS_M2 (1.0)
  innen, wenn mind. ein Grund:
    typ      raum_typ in INNEN_TYPEN oder FREI_TYPEN
    stempel  mind. ein cache["stempel"] mit raum_id == Raum-id
    sanitaer/moebel  Einfuegepunkt (WCS, OCS->WCS, * factor) eines INSERTs, rekursiv ueber
             virtual_entities bis Verschachtelungstiefe MAX_TIEFE, liegt im Raumpolygon (covers);
             Blockname passt SANITAER bzw. MOEBEL (Sanitaer hat Vorrang), Namen mit STEMPELBLOCK
             (ArchiCAD-Zonenstempel "Bad__4") sind ausgeschlossen.
  Freiflaeche     = raum_typ in FREI_TYPEN -> getrennt ausgewiesen, zaehlt nicht in "wert".
  wert je Plan    = Anzahl innen-Raeume ohne Freiflaechen mit schnitt_m2 > 0.05.
  Huelle H1       = Union aller Raumpolygone, closing H1_CLOSE_MM (buffer +r/-r, quad_segs 2), Loecher gefuellt.
  Huelle H2       = Union finde_wandkoerper (buffer(0), simplify 20), closing H2_CLOSE_MM, Loecher gefuellt,
                    Teile >= 1 m2.  anteil = Flaeche(AUSSEN ∩ H) / Flaeche(AUSSEN).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import pickle
import re
import subprocess
from collections import Counter
from pathlib import Path

from shapely import wkb
from shapely.geometry import MultiPolygon, Point, Polygon
from shapely.ops import unary_union

REPO = Path(os.environ["NOTBEL_REPO"])
ERG = Path(os.environ.get("NOTBEL_GATE_CACHES",
                          REPO / "Projekte" / "_ergebnis_raumerkennung"))

INNEN_TYPEN = frozenset({"WOHNZIMMER", "ZIMMER", "SCHLAFZIMMER", "KINDERZIMMER", "BAD", "WC",
                         "ABSTELLRAUM", "VORRAUM", "STIEGENHAUS"})
FREI_TYPEN = frozenset({"TERRASSE", "BALKON", "LOGGIA"})
SCHNITT_MIN_M2 = 0.05
SCHNITT_GROSS_M2 = 1.0
MAX_TIEFE = 4
H1_CLOSE_MM = 400.0
H2_CLOSE_MM = 3000.0
WEIT_MM = 2000.0          # Einfuegepunkt weiter als das vom Block-bbox-Mittelpunkt -> Plausibilitaetswarnung

STEMPELBLOCK = re.compile(r"__\d+$")
SANITAER = re.compile(
    r"(?<![a-z])WC(?![a-z])|WASCH(BECKEN|TISCH)|DUSCH|SHOWER|WANNE|BATHTUB|URINAL|SP(Ü|UE)LE"
    r"|(?<![a-z])SINK(?![a-z])|BIDET|TOILET", re.IGNORECASE)
MOEBEL = re.compile(
    r"CHAIR|ST(U|Ü|UE)HL|TISCH|TABLE|SOFA|COUCH|BETT|(?<![a-z])BED(?![a-z])|SCHRANK|WARDROBE"
    r"|REGAL|K(Ü|UE)CHE|KITCHEN|KOCHFELD|PANEL TV|HOME-TRAINER|HANTELBANK|LAUFBAND|R(Ü|UE)CKENTRAINER",
    re.IGNORECASE)
AUSSEN_STEMPEL = re.compile(r"HOF|ZUGANG|EINFAHRT|M(Ü|UE)LLPLATZ|GARTEN|VORPLATZ", re.IGNORECASE)


def _polygon(pts):
    if len(pts) < 3:
        return None
    g = Polygon(pts).buffer(0)
    return None if g.is_empty else g


def _fuellen(g, min_m2: float = 0.0):
    gs = list(g.geoms) if isinstance(g, MultiPolygon) else [g]
    return unary_union([Polygon(p.exterior) for p in gs
                        if p.geom_type == "Polygon" and not p.is_empty and p.area >= min_m2 * 1e6])


def _closing(g, r):
    return g.buffer(r, quad_segs=2).buffer(-r, quad_segs=2)


def _norm(name: str) -> str:
    return re.sub(r"\d+", "#", name)


def _dxf(ordner: Path, kz: dict) -> Path | None:
    kand = [REPO / kz["dxf"]] if kz.get("dxf") else []
    kand.append(ERG.parent / ordner.relative_to(ERG).parent / f"{ordner.name}.dxf")
    return next((p for p in kand if p.exists()), None)


def _inserts(plan):
    """(name, xy_mm, entity) aller INSERTs, rekursiv ueber virtual_entities bis MAX_TIEFE."""
    f = plan.factor

    def walk(ents, tiefe):
        for e in ents:
            if e.dxftype() != "INSERT":
                continue
            try:
                p = e.ocs().to_wcs(e.dxf.insert)
            except Exception:  # noqa: BLE001
                p = e.dxf.insert
            yield str(e.dxf.name), (float(p[0]) * f, float(p[1]) * f), e
            if tiefe < MAX_TIEFE:
                try:
                    sub = list(e.virtual_entities())
                except Exception:  # noqa: BLE001
                    continue
                yield from walk(sub, tiefe + 1)

    yield from walk(list(plan.space), 0)


def messe_plan(cpath: Path, glob_treffer: dict, glob_rest: Counter) -> dict:
    from ezdxf import bbox

    from notbeleuchtung.raumerkennung.dxf_load import lade_dxf
    from notbeleuchtung.raumerkennung.wandkoerper import finde_wandkoerper

    ordner = cpath.parent
    cache = pickle.loads(cpath.read_bytes())
    kzp = ordner / "kennzahlen.json"
    kz = json.loads(kzp.read_text(encoding="utf-8")) if kzp.exists() else {}
    dxf = _dxf(ordner, kz)
    out = {"ordner": str(ordner.relative_to(ERG)), "output_commit": kz.get("commit"),
           "dxf": str(dxf.relative_to(REPO)) if dxf else None}
    if dxf is None:
        out["fehler"] = "DXF nicht gefunden"
        return out
    out["dxf_sha_ok"] = (hashlib.sha256(dxf.read_bytes()).hexdigest() == kz.get("sha256")
                         if kz.get("sha256") else None)

    aussen = [wkb.loads(g) for g in cache.get("aussen_offen", [])]
    au = unary_union(aussen) if aussen else None
    au_m2 = au.area / 1e6 if au is not None else 0.0
    out["aussen_offen_n"] = len(aussen)
    out["aussen_offen_m2"] = round(au_m2, 2)

    # ── Bloecke ────────────────────────────────────────────────────────────
    plan = lade_dxf(dxf)
    out["factor_cache_plan"] = [cache.get("factor"), plan.factor]
    treffer = []                    # (kat, name, xy)
    n_ins = n_stempelblock = n_weit = 0
    weit_bsp = []
    bb = bbox.Cache()
    for name, xy, e in _inserts(plan):
        n_ins += 1
        if STEMPELBLOCK.search(name):
            n_stempelblock += 1
            continue
        kat = "sanitaer" if SANITAER.search(name) else ("moebel" if MOEBEL.search(name) else None)
        if kat is None:
            glob_rest[_norm(name)] += 1
            continue
        treffer.append((kat, name, xy))
        glob_treffer[kat][_norm(name)] += 1
        try:
            ext = bbox.extents([e], cache=bb)
            if ext.has_data:
                c = ext.center
                d = Point(c.x * plan.factor, c.y * plan.factor).distance(Point(xy))
                if d > WEIT_MM:
                    n_weit += 1
                    if len(weit_bsp) < 5:
                        weit_bsp.append({"block": name, "abstand_mm": round(d)})
        except Exception:  # noqa: BLE001
            pass
    out["bloecke"] = {"inserts": n_ins, "zonenstempel_ausgeschlossen": n_stempelblock,
                      "sanitaer": sum(1 for t in treffer if t[0] == "sanitaer"),
                      "moebel": sum(1 for t in treffer if t[0] == "moebel"),
                      "einfuegepunkt_weit_von_bbox": n_weit, "weit_beispiele": weit_bsp}

    # ── Raeume ─────────────────────────────────────────────────────────────
    st_je: dict[str, list[str]] = {}
    for s in cache.get("stempel", []):
        if s.get("raum_id"):
            st_je.setdefault(s["raum_id"], []).append(s.get("name") or "")
    polys = {}
    innen_n = frei_n = 0
    innen_hit, frei_hit, sonst_hit = [], [], []
    for r in cache["raeume"]:
        g = _polygon(r["polygon_mm"])
        if g is None:
            continue
        polys[r["id"]] = g
        typ = r.get("typ") or ""
        gruende = []
        if typ in INNEN_TYPEN or typ in FREI_TYPEN:
            gruende.append("typ")
        st = st_je.get(r["id"], [])
        if st:
            gruende.append("stempel")
        san = sorted({n for k, n, xy in treffer if k == "sanitaer" and g.covers(Point(xy))})
        moe = sorted({n for k, n, xy in treffer if k == "moebel" and g.covers(Point(xy))})
        if san:
            gruende.append("sanitaer")
        if moe:
            gruende.append("moebel")
        innen = bool(gruende)
        frei = typ in FREI_TYPEN
        if innen and not frei:
            innen_n += 1
        if frei:
            frei_n += 1
        schnitt = g.intersection(au).area / 1e6 if au is not None else 0.0
        if schnitt <= SCHNITT_MIN_M2:
            continue
        row = {"id": r["id"], "typ": typ, "stempel": st, "m2": round(r["flaeche_m2"], 2),
               "schnitt_m2": round(schnitt, 2), "schnitt_anteil": round(schnitt / max(g.area / 1e6, 1e-9), 3),
               "gruende": gruende, "sanitaer": san, "moebel": moe}
        if st and any(AUSSEN_STEMPEL.search(n) for n in st):
            row["stempel_aussen_verdacht"] = True
        (frei_hit if frei else innen_hit if innen else sonst_hit).append(row)

    def _flaechen(rows):
        if not rows or au is None:
            return 0.0, 0.0
        summe = sum(x["schnitt_m2"] for x in rows)
        union = unary_union([polys[x["id"]] for x in rows]).intersection(au).area / 1e6
        return round(summe, 2), round(union, 2)

    for key, rows in (("innen", innen_hit), ("frei", frei_hit), ("nicht_innen", sonst_hit)):
        s, u = _flaechen(rows)
        rows.sort(key=lambda x: -x["schnitt_m2"])
        out[key] = {"beruehrt_n": len(rows),
                    "gross_n": sum(1 for x in rows if x["schnitt_m2"] > SCHNITT_GROSS_M2),
                    "schnitt_m2_summe": s, "schnitt_m2_union": u, "raeume": rows}
    out["raeume_n"] = len(polys)
    out["innen_raeume_n_ohne_frei"] = innen_n
    out["frei_raeume_n"] = frei_n
    out["wert"] = len(innen_hit)

    # ── Huellen ────────────────────────────────────────────────────────────
    def _anteil(h):
        a = au.intersection(h).area / 1e6 if au is not None and not h.is_empty else 0.0
        return {"huelle_m2": round(h.area / 1e6, 1), "aussen_in_huelle_m2": round(a, 2),
                "anteil": round(a / au_m2, 3) if au_m2 > 0 else None}

    h1 = _fuellen(_closing(unary_union(list(polys.values())), H1_CLOSE_MM)) if polys else Polygon()
    out["huelle_H1_raeume"] = _anteil(h1)
    wk = finde_wandkoerper(plan)
    if wk:
        wu = unary_union([Polygon(k.polygon_mm).buffer(0) for k in wk]).simplify(20.0)
        h2 = _fuellen(_closing(wu, H2_CLOSE_MM), min_m2=1.0)
        out["huelle_H2_wand"] = {**_anteil(h2), "wandkoerper_n": len(wk),
                                 "wandkoerper_union_m2": round(wu.area / 1e6, 1)}
    else:
        out["huelle_H2_wand"] = {"wandkoerper_n": 0}
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(Path(__file__).with_name("messung.json")))
    a = ap.parse_args()
    try:
        head = subprocess.run(["git", "-C", str(REPO), "rev-parse", "--short", "HEAD"],
                              capture_output=True, text=True, check=False).stdout.strip()
    except OSError:
        head = None
    glob_treffer = {"sanitaer": Counter(), "moebel": Counter()}
    glob_rest: Counter = Counter()
    plaene = {}
    for cpath in sorted(ERG.rglob("_cache.pkl")):
        rel = cpath.parent.relative_to(ERG)
        key = f"{rel.parent.as_posix()}/{cpath.parent.name.split(' - ')[0]}"
        plaene[key] = messe_plan(cpath, glob_treffer, glob_rest)
        p = plaene[key]
        print(key, "wert", p.get("wert"), "innen_schnitt_union", p.get("innen", {}).get("schnitt_m2_union"),
              "frei", p.get("frei", {}).get("beruehrt_n"), flush=True)

    def sm(k1, k2):
        return round(sum(p.get(k1, {}).get(k2, 0) for p in plaene.values()), 2)

    res = {
        "metrik": "M2-aussen-auf-innenraum", "repo_head": head,
        "konstanten": {"INNEN_TYPEN": sorted(INNEN_TYPEN), "FREI_TYPEN": sorted(FREI_TYPEN),
                       "SCHNITT_MIN_M2": SCHNITT_MIN_M2, "SCHNITT_GROSS_M2": SCHNITT_GROSS_M2,
                       "MAX_TIEFE": MAX_TIEFE, "H1_CLOSE_MM": H1_CLOSE_MM, "H2_CLOSE_MM": H2_CLOSE_MM,
                       "WEIT_MM": WEIT_MM, "STEMPELBLOCK": STEMPELBLOCK.pattern,
                       "SANITAER": SANITAER.pattern, "MOEBEL": MOEBEL.pattern,
                       "AUSSEN_STEMPEL": AUSSEN_STEMPEL.pattern},
        "block_treffer_gesamt": {k: dict(v.most_common()) for k, v in glob_treffer.items()},
        "block_unklassifiziert_top40": dict(glob_rest.most_common(40)),
        "summe": {"plaene": len(plaene),
                  "wert_innen_beruehrt": sum(p.get("wert", 0) for p in plaene.values()),
                  "innen_gross_n": sum(p.get("innen", {}).get("gross_n", 0) for p in plaene.values()),
                  "innen_schnitt_m2_union": sm("innen", "schnitt_m2_union"),
                  "frei_beruehrt_n": sum(p.get("frei", {}).get("beruehrt_n", 0) for p in plaene.values()),
                  "frei_schnitt_m2_union": sm("frei", "schnitt_m2_union"),
                  "nicht_innen_beruehrt_n": sum(p.get("nicht_innen", {}).get("beruehrt_n", 0)
                                                for p in plaene.values()),
                  "aussen_offen_m2": round(sum(p.get("aussen_offen_m2", 0) for p in plaene.values()), 2),
                  "aussen_in_H1_m2": sm("huelle_H1_raeume", "aussen_in_huelle_m2"),
                  "aussen_in_H2_m2": sm("huelle_H2_wand", "aussen_in_huelle_m2")},
        "plaene": plaene,
    }
    Path(a.out).write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print("->", a.out)


if __name__ == "__main__":
    main()
