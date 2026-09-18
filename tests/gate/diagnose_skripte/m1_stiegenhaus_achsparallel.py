# ruff: noqa
# Wortgetreu aus docs/DIAGNOSE_RENNWEG_RAUMERKENNUNG.md (Commit 34b5dd0), Anhang A.1 —
# programmatisch aus dem Codeblock extrahiert, nicht abgetippt.
# Abweichungen gegenueber der Diagnose (sonst Byte fuer Byte gleich):
#   1. diese Kopfzeilen (# ruff: noqa + Herkunftsvermerk).
#   2. REPO = Path(os.environ["NOTBEL_REPO"]) statt des hart verdrahteten Benutzerpfads;
#      Pflicht, kein Default (der Docstring nennt den alten Default noch).
#   3. Cache-Wurzel ERGEBNIS aus NOTBEL_GATE_CACHES, sonst wie bisher
#      REPO / "Projekte" / "_ergebnis_raumerkennung".
"""M1-stiegenhaus-achsparallel — achsparallele STIEGENHAUS-Polygone in gedrehten Plaenen.

Nur lesen. Grundmenge: alle _cache.pkl unter Projekte/_ergebnis_raumerkennung (rglob).
Aufruf:  PY _messen.py [out.json]      (Default: ergebnis.json neben diesem Skript)
Repo:    Umgebungsvariable NOTBEL_REPO, sonst D:/KI Projekt/Notbeleuchtung

Definitionen (unveraendert fuer Vorher/Nachher):
  Kantenwinkel     a = atan2(dy, dx) in Grad mod 90; Kanten < 1 mm ignoriert; Gewicht = Laenge.
  Rotation         Bin = round(a*2)/2 mod 90 (0,5-Grad-Bins); dominanter Bin = argmax Gewicht.
                   Abstand = min(w, 90-w); "gedreht" <=> Abstand > 3 Grad.
    - plan:        ueber alle Raumpolygon-Kanten des Plans (Vorgabe).
    - cluster:     Raumpolygone je Zusammenhangskomponente von union(buffer 1000 mm) —
                   trennt mehrere Grundrisse in einem Modelspace. Kantensumme < 20 m -> Plan-Wert.
                   MASSGEBLICH fuer "im gedrehten Plan".
    - wand_dxf:    Gegenprobe: Kanten der Wand-Layer-Entities (lade_dxf.wall_entities), INSERTs
                   eine Ebene aufgeloest (LINE/LWPOLYLINE/POLYLINE), verschachtelte INSERTs nicht.
  achsparallel     (Vorgabe) Anteil der Kantenlaenge mit min(a, 90-a) <= 1 Grad; achsparallel <=> >= 0,90.
  achsparallel_huelle  dieselbe Regel auf der konvexen Huelle (robust gegen gedreht ausgestanzte
                   Lifte/Schaechte in einem achsparallelen Rechteck).
  planparallel     Anteil der Kantenlaenge innerhalb +-1 Grad der massgeblichen Rotation (mod 90) — Info.
  Praefix          re.match(r"^([A-Za-z]+)_", id) -> Gruppe 1, sonst "(ohne)".
  Treppen-BBox     geometrie_typ.stiege_rechtecke(plan). treppen_rand_anteil = max ueber Rechtecke von
                   Laenge(Rand(Polygon) geschnitten mit Rand(Rechteck).buffer(10 mm)) / Laenge(Rand(Polygon));
                   "aus_treppen_bbox" <=> treppen_rand_anteil >= 0,5. treppen_bbox_iou = IoU(envelope, Rechteck) nur Info.
  Zusatz klein     STIEGENHAUS, flaeche_m2 < 2,0 und kein Cache-Stempel mit raum_id == id.
                   beruehrt_lift <=> shapely-Abstand zu irgendeinem LIFT-Polygon <= 300 mm.
                   schacht_text  <=> Text (TEXT/MTEXT/ATTRIB, rekursiv in INSERTs bis Tiefe 6,
                   Einfuegepunkt) mit Abstand zum Polygon <= 500 mm und Treffer SCHACHT_TEXT.
"""
from __future__ import annotations

import json
import math
import os
import pickle
import re
import sys
import time
from collections import Counter
from pathlib import Path

from shapely.geometry import Point, Polygon, box
from shapely.ops import unary_union

REPO = Path(os.environ["NOTBEL_REPO"])
ERGEBNIS = Path(os.environ.get("NOTBEL_GATE_CACHES",
                               REPO / "Projekte" / "_ergebnis_raumerkennung"))

GEDREHT_GRAD = 3.0
ACHS_TOL_GRAD = 1.0
ACHS_ANTEIL = 0.90
CLUSTER_PUFFER_MM = 1000.0
CLUSTER_MIN_KANTEN_MM = 20_000.0
TREPPEN_RAND_MM = 10.0
TREPPEN_RAND_ANTEIL = 0.5
KLEIN_M2 = 2.0
LIFT_ABSTAND_MM = 300.0
ZAEHL = ("achsparallel", "achsparallel_im_gedrehten", "achsparallel_huelle",
         "achsparallel_huelle_im_gedrehten", "aus_treppen_bbox")
TEXT_ABSTAND_MM = 500.0
TEXT_TIEFE = 6
# Schacht-Kuerzel nach der Service-Marker-Liste im Port
# (_port/parsers/architecture_dxf.py _SERVICE_MARKER_KIND_ALIASES, Z. 2667-2671).
SCHACHT_TEXT = re.compile(
    r"SCHACHT|INSTALLATION|(?<![A-Z])(?:DDB|BDB|FBDB|WDB|FDB|DBA|HKLS)(?![A-Z])"
    r"|\b(?:DD|BD|FBD|WDD|WODD)\s*(?:[-/]\s*)?(?:HT|ET)?\s*\d",
    re.IGNORECASE)


def kanten(pts, geschlossen=True):
    n = len(pts)
    for i in range(n if geschlossen else n - 1):
        (x1, y1), (x2, y2) = pts[i], pts[(i + 1) % n]
        l = math.hypot(x2 - x1, y2 - y1)
        if l >= 1.0:
            yield math.degrees(math.atan2(y2 - y1, x2 - x1)) % 90.0, l


def rotation(kantenlisten) -> dict:
    bins: Counter = Counter()
    tot = 0.0
    for ks in kantenlisten:
        for a, l in ks:
            bins[(round(a * 2) / 2) % 90.0] += l
            tot += l
    if tot <= 0:
        return {"winkel_mod90": None, "anteil": 0.0, "abstand_0_90": None, "gedreht": None,
                "kanten_m": 0.0}
    w, g = bins.most_common(1)[0]
    ab = min(w, 90.0 - w)
    return {"winkel_mod90": w, "anteil": round(g / tot, 3), "abstand_0_90": ab,
            "gedreht": ab > GEDREHT_GRAD, "kanten_m": round(tot / 1000, 1)}


def diff90(a, b):
    d = abs(a - b) % 90.0
    return min(d, 90.0 - d)


def poly(pts):
    if len(pts) < 3:
        return None
    p = Polygon(pts)
    return p if p.is_valid else p.buffer(0)


def wand_rotation(plan) -> dict:
    def ks():
        for e in plan.wall_entities():
            ents = [e]
            if e.dxftype() == "INSERT":
                try:
                    ents = [v for v in e.virtual_entities()
                            if v.dxftype() in ("LINE", "LWPOLYLINE", "POLYLINE")]
                except Exception:  # noqa: BLE001
                    continue
            for v in ents:
                pts = plan.entity_points(v)
                if len(pts) >= 2:
                    yield list(kanten(pts, geschlossen=False))
    return rotation(ks())


def schacht_texte(plan) -> list[dict]:
    f = plan.factor
    out: list[dict] = []

    def add(txt, ins, layer, pfad):
        if txt and SCHACHT_TEXT.search(txt):
            out.append({"text": txt.strip()[:80], "xy_mm": [round(ins[0] * f), round(ins[1] * f)],
                        "layer": layer, "pfad": pfad})

    def walk(ents, pfad, tiefe):
        for e in ents:
            t = e.dxftype()
            try:
                if t == "INSERT":
                    for at in e.attribs:
                        add(at.dxf.text, at.dxf.insert, at.dxf.layer, pfad + [e.dxf.name])
                    if tiefe < TEXT_TIEFE:
                        walk(list(e.virtual_entities()), pfad + [e.dxf.name], tiefe + 1)
                elif t in ("TEXT", "ATTRIB"):
                    add(e.dxf.text, e.dxf.insert, e.dxf.layer, pfad)
                elif t == "MTEXT":
                    add(e.plain_text(), e.dxf.insert, e.dxf.layer, pfad)
            except Exception:  # noqa: BLE001
                continue
    walk(list(plan.space), [], 0)
    return out


def dxf_pfad(ordner: Path, kz: dict) -> Path | None:
    kand = [REPO / "Projekte" / ordner.parent.name / f"{ordner.name}.dxf"]
    if kz.get("dxf"):
        kand.append(REPO / kz["dxf"])
    return next((p for p in kand if p.exists()), None)


def messe_plan(cache_pfad: Path) -> dict:
    t0 = time.time()
    ordner = cache_pfad.parent
    kzp = ordner / "kennzahlen.json"
    kz = json.loads(kzp.read_text(encoding="utf-8-sig")) if kzp.exists() else {}
    c = pickle.loads(cache_pfad.read_bytes())
    raeume = c["raeume"]
    geo = {r["id"]: g for r in raeume if (g := poly(r["polygon_mm"])) is not None and not g.is_empty}
    stempel_je = Counter(s["raum_id"] for s in c["stempel"] if s.get("raum_id"))

    rot_plan = rotation(list(kanten(r["polygon_mm"])) for r in raeume)

    # Cluster (mehrere Grundrisse je Modelspace)
    u = unary_union([g.buffer(CLUSTER_PUFFER_MM) for g in geo.values()])
    komps = list(getattr(u, "geoms", [u]))
    cluster_von = {rid: next((i for i, k in enumerate(komps) if k.covers(g.representative_point())), -1)
                   for rid, g in geo.items()}
    cluster_rot = {}
    for i in range(len(komps)):
        ids = [r for r in raeume if cluster_von.get(r["id"]) == i]
        cr = rotation(list(kanten(r["polygon_mm"])) for r in ids)
        cr["n_raeume"] = len(ids)
        cr["fallback_plan"] = cr["kanten_m"] * 1000 < CLUSTER_MIN_KANTEN_MM
        cluster_rot[i] = cr

    dxf = dxf_pfad(ordner, kz)
    plan = None
    fehler = []
    if dxf is not None:
        from notbeleuchtung.raumerkennung.dxf_load import lade_dxf
        plan = lade_dxf(dxf)
    else:
        fehler.append("DXF nicht gefunden")
    rot_wand = wand_rotation(plan) if plan is not None else None
    treppen = []
    if plan is not None:
        try:
            from notbeleuchtung.raumerkennung.geometrie_typ import stiege_rechtecke
            treppen = [Polygon(rect) for rect, _c, _a in stiege_rechtecke(plan)]
        except Exception as e:  # noqa: BLE001
            fehler.append(f"stiege_rechtecke: {e!r}")

    lifte = [geo[r["id"]] for r in raeume if r["typ"] == "LIFT" and r["id"] in geo]
    stg = [r for r in raeume if r["typ"] == "STIEGENHAUS"]
    klein_kand = [r for r in stg if r["flaeche_m2"] < KLEIN_M2 and not stempel_je.get(r["id"])]
    texte = schacht_texte(plan) if (plan is not None and klein_kand) else []

    zeilen = []
    for r in stg:
        g = geo.get(r["id"])
        ks = list(kanten(r["polygon_mm"]))
        tot = sum(l for _a, l in ks) or 1.0
        achs = sum(l for a, l in ks if min(a, 90.0 - a) <= ACHS_TOL_GRAD) / tot
        ci = cluster_von.get(r["id"], -1)
        cr = cluster_rot.get(ci)
        mass = rot_plan if (cr is None or cr["fallback_plan"]) else cr
        plan_par = (sum(l for a, l in ks if diff90(a, mass["winkel_mod90"]) <= ACHS_TOL_GRAD) / tot
                    if mass["winkel_mod90"] is not None else None)
        m = re.match(r"^([A-Za-z]+)_", r["id"])
        z = {"id": r["id"], "praefix": m.group(1) if m else "(ohne)",
             "flaeche_m2": round(r["flaeche_m2"], 2), "n_ecken": len(r["polygon_mm"]),
             "bbox_mm": [round(v) for v in g.bounds] if g is not None else None,
             "achsparallel_anteil": round(achs, 3), "achsparallel": achs >= ACHS_ANTEIL,
             "planparallel_anteil": round(plan_par, 3) if plan_par is not None else None,
             "cluster": ci, "rotation_massgeblich": mass["winkel_mod90"],
             "im_gedrehten_plan": bool(mass["gedreht"]),
             "stempel_n": stempel_je.get(r["id"], 0), "wohnung_id": r.get("wohnung_id")}
        z["achsparallel_im_gedrehten"] = z["achsparallel"] and z["im_gedrehten_plan"]
        hks = list(kanten(list(g.convex_hull.exterior.coords)[:-1])) if g is not None else []
        htot = sum(l for _a, l in hks) or 1.0
        hachs = sum(l for a, l in hks if min(a, 90.0 - a) <= ACHS_TOL_GRAD) / htot
        z["achsparallel_huelle_anteil"] = round(hachs, 3)
        z["achsparallel_huelle"] = hachs >= ACHS_ANTEIL
        z["achsparallel_huelle_im_gedrehten"] = z["achsparallel_huelle"] and z["im_gedrehten_plan"]
        if g is not None and treppen:
            env, rand = g.envelope, g.boundary
            ious = [env.intersection(t).area / env.union(t).area for t in treppen]
            rant = [rand.intersection(t.exterior.buffer(TREPPEN_RAND_MM)).length / rand.length
                    for t in treppen]
            z["treppen_bbox_iou"] = round(max(ious), 3)
            z["treppen_rand_anteil"] = round(max(rant), 3)
            z["aus_treppen_bbox"] = max(rant) >= TREPPEN_RAND_ANTEIL
        else:
            z["treppen_bbox_iou"], z["treppen_rand_anteil"], z["aus_treppen_bbox"] = None, None, False
        if r in klein_kand and g is not None:
            dl = min((g.distance(lg) for lg in lifte), default=None)
            nah = [dict(t, abstand_mm=round(g.distance(Point(t["xy_mm"]))))
                   for t in texte if g.distance(Point(t["xy_mm"])) <= TEXT_ABSTAND_MM]
            z["klein_ohne_stempel"] = {
                "lift_abstand_mm": round(dl) if dl is not None else None,
                "beruehrt_lift": dl is not None and dl <= LIFT_ABSTAND_MM,
                "schacht_text": bool(nah), "schacht_texte": nah}
        zeilen.append(z)

    def summe(rows):
        return {"n": len(rows), "m2": round(sum(x["flaeche_m2"] for x in rows), 2)}

    je_praefix = {}
    for p in sorted({z["praefix"] for z in zeilen}):
        rows = [z for z in zeilen if z["praefix"] == p]
        je_praefix[p] = {"gesamt": summe(rows)} | {k: summe([z for z in rows if z[k]]) for k in ZAEHL}
    klein = [z for z in zeilen if "klein_ohne_stempel" in z]
    return {
        "plan": ordner.name, "projekt": ordner.parent.name, "commit_output": kz.get("commit"),
        "dxf": str(dxf) if dxf else None, "fehler": fehler,
        "rotation_plan_raumkanten": rot_plan, "rotation_wand_dxf": rot_wand,
        "cluster": {str(i): cr for i, cr in cluster_rot.items()},
        "treppen_rechtecke_n": len(treppen),
        "treppen_rechtecke_bbox_mm": [[round(v) for v in t.bounds] for t in treppen],
        "stiegenhaus": {"gesamt": summe(zeilen)}
                       | {k: summe([z for z in zeilen if z[k]]) for k in ZAEHL}
                       | {"je_praefix": je_praefix},
        "klein_ohne_stempel": {
            "n": len(klein),
            "beruehrt_lift": sum(z["klein_ohne_stempel"]["beruehrt_lift"] for z in klein),
            "schacht_text": sum(z["klein_ohne_stempel"]["schacht_text"] for z in klein)},
        "schacht_texte_im_plan_n": len(texte) if klein_kand else None,
        "polygone": zeilen, "dauer_s": round(time.time() - t0, 1),
    }


def main() -> None:
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("ergebnis.json")
    plaene = [messe_plan(p) for p in sorted(ERGEBNIS.rglob("_cache.pkl"))]
    tot = {k: {"n": sum(p["stiegenhaus"][k]["n"] for p in plaene),
               "m2": round(sum(p["stiegenhaus"][k]["m2"] for p in plaene), 2)}
           for k in ("gesamt", *ZAEHL)}
    tot["plaene"] = len(plaene)
    tot["plaene_gedreht"] = sum(bool(p["rotation_plan_raumkanten"]["gedreht"]) for p in plaene)
    tot["klein_ohne_stempel"] = {k: sum(p["klein_ohne_stempel"][k] for p in plaene)
                                 for k in ("n", "beruehrt_lift", "schacht_text")}
    res = {"metrik": "M1-stiegenhaus-achsparallel", "definition": __doc__, "summe": tot,
           "plaene": plaene}
    out.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({"summe": tot, "je_plan": [
        {"plan": p["plan"][:4], "rot_raum": p["rotation_plan_raumkanten"], "rot_wand": p["rotation_wand_dxf"],
         "cluster": {i: (c["winkel_mod90"], c["n_raeume"], c["fallback_plan"]) for i, c in p["cluster"].items()},
         "treppen": p["treppen_rechtecke_n"], "stg": p["stiegenhaus"], "klein": p["klein_ohne_stempel"],
         "texte": p["schacht_texte_im_plan_n"], "fehler": p["fehler"], "s": p["dauer_s"]}
        for p in plaene]}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
