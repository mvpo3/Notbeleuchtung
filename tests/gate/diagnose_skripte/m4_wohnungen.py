# ruff: noqa
# Wortgetreu aus docs/DIAGNOSE_RENNWEG_RAUMERKENNUNG.md (Commit 34b5dd0), Anhang A.4 —
# programmatisch aus dem Codeblock extrahiert, nicht abgetippt.
# Abweichungen gegenueber der Diagnose (sonst Byte fuer Byte gleich):
#   1. diese Kopfzeilen (# ruff: noqa + Herkunftsvermerk).
#   2. REPO = Path(os.environ["NOTBEL_REPO"]) statt des hart verdrahteten Benutzerpfads;
#      Pflicht, kein Default (der Docstring nennt den alten Default noch).
#   3. Cache-Wurzel AUSGABE aus NOTBEL_GATE_CACHES, sonst wie bisher
#      REPO / "Projekte" / "_ergebnis_raumerkennung".
#   4. "import os" ergaenzt — Anhang A.4 importiert os nicht.
"""M4-wohnungen — Vorher/Nachher-Messung der Wohnungsbildung (S-H4).

Liest NUR die Output-Caches (_cache.pkl) unter Projekte/_ergebnis_raumerkennung,
keine Pipeline, kein DXF. Aufruf:
    python _messen.py [ausgabe.json]      (Default: ergebnis.json neben dem Skript)

Definitionen (fix, fuer Vorher und Nachher identisch):
  Wohnung          = jede verschiedene, nicht-leere raeume[].wohnung_id eines Plans.
  Einraum-Wohnung  = Wohnung mit genau 1 Raum in den Daten.
  Datenbefund      = Wohnung enthaelt einen Raum mit typ in ERSCHL_TYPEN oder
                     nutzungsklasse beginnend mit "ALLGEMEIN_".
  Darstellungsbefund = Nachbau von scripts/analyse/raumerkennung_darstellung.py
                     _zeichne_ausschnitt Z.709-731 (Umriss) + _polygon Z.218-222:
                     u = unary_union(Raumpolygone der Wohnung).buffer(200).buffer(-200)
                     (leer -> unary_union ohne Puffer); gezeichnet werden NUR die
                     Aussenringe -> "gezeichnete Flaeche" = Union der Polygon(exterior).
                     Befund, wenn ein Raum mit typ in ERSCHL_TYPEN davon > MIN_M2 m2
                     ueberdeckt wird (unabhaengig davon, ob er in den Daten dazugehoert).
  Privatraum ohne Wohnung = wohnung_id leer UND (typ.upper() in PRIVAT_TYPEN ODER
                     (typ leer = UNBEKANNT UND ein zugeordneter Stempel (stempel.raum_id)
                     matcht WOHN_STEMPEL_RX)).
"""
import json
import os
import pickle
import re
import sys
from pathlib import Path

from shapely.geometry import Polygon
from shapely.ops import unary_union

REPO = Path(os.environ["NOTBEL_REPO"])
AUSGABE = Path(os.environ.get("NOTBEL_GATE_CACHES",
                              REPO / "Projekte" / "_ergebnis_raumerkennung"))
MIN_M2 = 0.5
PUFFER_MM = 200.0                      # = raumerkennung_darstellung.py Z.715
ERSCHL_TYPEN = {"STIEGENHAUS", "TREPPENHAUS", "LIFT", "AUFZUG"}
PRIVAT_TYPEN = {"ZIMMER", "WOHNZIMMER", "BAD", "WC", "KUECHE", "KÜCHE", "ABSTELLRAUM", "VORRAUM"}
WOHN_STEMPEL_RX = re.compile(r"wohn|tv[\s._-]*raum|k(?:ü|ue)?che", re.IGNORECASE)


def _polygon(pts):                     # = raumerkennung_darstellung._polygon Z.218-222
    if len(pts) < 3:
        return None
    g = Polygon(pts).buffer(0)
    return None if g.is_empty else g


def _umriss(ps):                       # = _zeichne_ausschnitt Z.715-722
    u = unary_union(ps).buffer(PUFFER_MM).buffer(-PUFFER_MM)
    if u.is_empty:
        u = unary_union(ps)
    teile = list(getattr(u, "geoms", [u]))
    gezeichnet = unary_union([Polygon(g.exterior) for g in teile])
    return u, gezeichnet, teile


def _r(r):
    return {"id": r["id"], "typ": r["typ"] or "UNBEKANNT", "m2": round(r["flaeche_m2"], 2),
            "nutzungsklasse": r["nutzungsklasse"], "wohnung_id": r["wohnung_id"]}


def messe_plan(cache_pfad: Path) -> dict:
    c = pickle.loads(cache_pfad.read_bytes())
    kz_pfad = cache_pfad.parent / "kennzahlen.json"
    kz = json.loads(kz_pfad.read_text(encoding="utf-8")) if kz_pfad.exists() else {}
    raeume = c["raeume"]
    polys = {r["id"]: g for r in raeume if (g := _polygon(r["polygon_mm"])) is not None}
    stempel_je_raum = {}
    for s in c["stempel"]:
        if s.get("raum_id"):
            stempel_je_raum.setdefault(s["raum_id"], []).append(s["name"])

    # Einheitscheck: Polygonflaeche (mm2/1e6) gegen flaeche_m2
    abw = [abs(polys[r["id"]].area / 1e6 - r["flaeche_m2"]) / r["flaeche_m2"]
           for r in raeume if r["id"] in polys and r["flaeche_m2"] > 0]

    whg = {}
    for r in raeume:
        if r["wohnung_id"]:
            whg.setdefault(r["wohnung_id"], []).append(r)

    einraum = [{"wohnung": w, **_r(rs[0])} for w, rs in sorted(whg.items()) if len(rs) == 1]

    daten = []
    for w, rs in sorted(whg.items()):
        treffer = [_r(r) for r in rs
                   if (r["typ"] or "").upper() in ERSCHL_TYPEN
                   or (r["nutzungsklasse"] or "").startswith("ALLGEMEIN_")]
        if treffer:
            daten.append({"wohnung": w, "raeume": treffer})

    darstellung, fremde, umrisse = [], [], []
    for w, rs in sorted(whg.items()):
        ps = [polys[r["id"]] for r in rs if r["id"] in polys]
        if not ps:
            continue
        ids = {r["id"] for r in rs}
        u, gez, teile = _umriss(ps)
        umrisse.append({"wohnung": w, "raeume_daten": len(rs),
                        "raeume_m2_daten": round(sum(r["flaeche_m2"] for r in rs), 2),
                        "umriss_teile": len(teile),
                        "loecher_nicht_gezeichnet": sum(len(t.interiors) for t in teile),
                        "gezeichnete_flaeche_m2": round(gez.area / 1e6, 2)})
        for r in raeume:
            p = polys.get(r["id"])
            if p is None:
                continue
            a = gez.intersection(p).area / 1e6
            if a <= MIN_M2:
                continue
            eintrag = {"wohnung": w, **_r(r), "ueberdeckt_m2": round(a, 2),
                       "ueberdeckt_m2_mit_loechern": round(u.intersection(p).area / 1e6, 2),
                       "in_daten": r["id"] in ids}
            if (r["typ"] or "").upper() in ERSCHL_TYPEN:
                darstellung.append(eintrag)
            if r["id"] not in ids:
                fremde.append(eintrag)

    privat, unbek_kontext = [], []
    for r in raeume:
        if r["wohnung_id"]:
            continue
        typ = (r["typ"] or "").upper()
        namen = stempel_je_raum.get(r["id"], [])
        if typ in PRIVAT_TYPEN:
            privat.append({**_r(r), "grund": "typ", "stempel": namen})
        elif not typ:
            wohn = [n for n in namen if WOHN_STEMPEL_RX.search(n)]
            e = {**_r(r), "stempel": namen, "stempel_ascii": [ascii(n) for n in namen]}
            if wohn:
                privat.append({**e, "grund": "UNBEKANNT+Wohn-Stempel"})
            else:
                unbek_kontext.append(e)

    return {
        "projekt": cache_pfad.parent.parent.name,
        "plan_ordner": cache_pfad.parent.name,
        "plan": cache_pfad.parent.name.split(" - ")[0],
        "commit_output": kz.get("commit"),
        "kennzahlen_wohnungen": kz.get("wohnungen"),
        "raeume_gesamt": len(raeume),
        "einheit_max_rel_abw_polygon_vs_m2": round(max(abw), 4) if abw else None,
        "wohnungen": len(whg),
        "raeume_je_wohnung": {w: len(rs) for w, rs in sorted(whg.items())},
        "einraum_wohnungen": einraum,
        "daten_erschliessung_in_wohnung": daten,
        "darstellung_erschliessung_im_umriss": darstellung,
        "kontext_fremde_raeume_im_umriss": fremde,
        "kontext_umrisse": umrisse,
        "privat_ohne_wohnung": privat,
        "kontext_unbekannt_ohne_wohnung_ohne_wohnstempel": unbek_kontext,
        "zahlen": {
            "wohnungen": len(whg),
            "einraum": len(einraum),
            "wohnungen_daten_erschliessung": len(daten),
            "wohnungen_darstellung_erschliessung": len({d["wohnung"] for d in darstellung}),
            "wohnungen_auffaellig": len({e["wohnung"] for e in einraum + daten + darstellung}),
            "privat_ohne_wohnung": len(privat),
            "privat_ohne_wohnung_nicht_allgemein": sum(
                1 for p in privat if not (p["nutzungsklasse"] or "").startswith("ALLGEMEIN_")),
        },
    }


def main() -> int:
    ziel = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("ergebnis.json")
    plaene = [messe_plan(p) for p in sorted(AUSGABE.rglob("_cache.pkl"))]
    summe = {k: sum(p["zahlen"][k] for p in plaene) for k in plaene[0]["zahlen"]} if plaene else {}
    summe["plaene"] = len(plaene)
    summe["plaene_mit_befund"] = sum(
        1 for p in plaene if p["zahlen"]["einraum"] or p["zahlen"]["wohnungen_daten_erschliessung"]
        or p["zahlen"]["wohnungen_darstellung_erschliessung"])
    ergebnis = {"metrik": "M4-wohnungen", "min_m2": MIN_M2, "puffer_mm": PUFFER_MM,
                "erschl_typen": sorted(ERSCHL_TYPEN), "privat_typen": sorted(PRIVAT_TYPEN),
                "wohn_stempel_rx": WOHN_STEMPEL_RX.pattern, "summe": summe, "plaene": plaene}
    ziel.write_text(json.dumps(ergebnis, ensure_ascii=False, indent=1), encoding="utf-8")
    for p in plaene:
        print(p["plan"], p["commit_output"], json.dumps(p["zahlen"]))
    print("SUMME", json.dumps(summe))
    return 0


if __name__ == "__main__":
    sys.exit(main())
