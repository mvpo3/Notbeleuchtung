# ruff: noqa
# Wortgetreu aus docs/DIAGNOSE_RENNWEG_RAUMERKENNUNG.md (Commit 34b5dd0), Anhang A.3 —
# programmatisch aus dem Codeblock extrahiert, nicht abgetippt.
# Abweichungen gegenueber der Diagnose (sonst Byte fuer Byte gleich):
#   1. diese Kopfzeilen (# ruff: noqa + Herkunftsvermerk).
#   2. REPO = Path(os.environ["NOTBEL_REPO"]) statt des hart verdrahteten Benutzerpfads;
#      Pflicht, kein Default (der Docstring nennt den alten Default noch).
#   3. Cache-Wurzel ERG aus NOTBEL_GATE_CACHES, sonst wie bisher
#      REPO / "Projekte" / "_ergebnis_raumerkennung".
#   4. "import os" ergaenzt — Anhang A.3 importiert os nicht.
"""M3-schacht-ohne-stanzung — Schacht-Marker (Text) in Raeumen ohne ausgestanzten SCHACHT/LIFT.

Aufruf (Repo-venv, nur lesen):
  PY _messen.py [--out <datei.json>]      Default: messung.json neben dem Skript

Grundmenge: jede Projekte/_ergebnis_raumerkennung/**/_cache.pkl (rglob, nichts hart verdrahtet).
DXF: kennzahlen.json "dxf" (relativ zum Repo), sonst Projekte/<relativer Ergebnisordner>.dxf;
     sha256 gegen kennzahlen.json geprueft (dxf_sha_ok).
Kein Pipeline-Re-Run. In-memory nur dxf_load.lade_dxf (Architektur-Space + mm-Faktor).

Walk: alle Entities von plan.space, rekursiv ueber INSERT.virtual_entities() bis Verschachtelung
MAX_TIEFE (Top-Level = 0). Koordinaten WCS (TEXT/ATTRIB: get_placement -> OCS->WCS; MTEXT: insert)
* plan.factor. Layer "0" im Block erbt den Layer des INSERTs; Farbe: true_color > ACI;
ACI 0 (BYBLOCK) erbt die effektive INSERT-Farbe; ACI 256 (BYLAYER) = Layer-true_color bzw. |Layer-ACI|
des effektiven Layers. ATTDEF zaehlt nicht (ezdxf ueberspringt es), unsichtbare ATTRIBs zaehlen nicht.
DIMENSION wird nicht betreten (Masstexte bleiben draussen).

Schritt 1 Inventar: TEXT/MTEXT/ATTRIB (MTEXT plain_text, Zeilen mit " | " verbunden) gegen TOKENS
  (breit, je Token gezaehlt + Beispiele) + haeufigste normalisierte Texte (Ziffern -> #).
Schritt 2 rote Konturen: LWPOLYLINE/2D-POLYLINE, geschlossen (Flag oder Endpunkte <= SCHLUSS_TOL_MM),
  Pfad geglaettet (ezdxf.path, FLATTEN_MM), Polygon.buffer(0), 0 < Flaeche < ROT_MAX_M2, effektive
  Farbe ROT (ACI 1 oder RGB mit R >= ROT_R_MIN und G, B <= ROT_GB_MAX).
Schritt 3 Metrik: Marker = sichtbarer Text, der MARKER matcht und nicht AUSSCHLUSS.
  Raumpolygon = Polygon(polygon_mm).buffer(0) (wie raumerkennung_darstellung._polygon).
  STANZ = Raeume mit typ in STANZ_TYPEN (SCHACHT, LIFT).
  Kategorie je Marker-Punkt P (exklusiv, in dieser Reihenfolge):
    schacht_nah          min. Abstand P -> STANZ-Polygon <= NAH_MM (0 = enthalten)
    raum_ohne_stanzung   sonst: ein Nicht-STANZ-Raumpolygon covers(P)
    ausserhalb           sonst
  wert je Plan = Anzahl DISTINKTER Raeume mit >= 1 Marker der Kategorie raum_ohne_stanzung.
  Zusatz: schacht_nah_und_raum_deckt = schacht_nah UND ein Nicht-STANZ-Raum covers(P)
          (Schacht-Polygon liegt daneben, Raum wurde am Marker nicht ausgestanzt).
  Rote Konturen: gleiche Kategorien ueber representative_point().
  FP-Kandidaten: SCHACHT-Polygone (typ in FP_TYPEN) ohne Marker-Punkt in <= NAH_MM
    (fp_ohne_text) bzw. zusaetzlich ohne rote Kontur in <= NAH_MM (fp_ohne_text_und_rot).
  Duplikate: gleicher Text <= DEDUP_MM neben gleichem Text zaehlt einmal; AUSSCHLUSS-Treffer zaehlen nicht.
  Sensitivitaet: dieselbe Kategorisierung mit NAH_MM_ALT statt NAH_MM (sensitiv_nah_1000mm).
  Flaechensignal (textunabhaengig): U = Union der roten Konturen; je Nicht-STANZ-Raum Flaeche(Raum ∩ U)
    >= ROT_FLAECHE_MIN_M2 -> rot_flaeche_in_raeumen; wert_bestaetigt_rot = Anzahl wert-Raeume, die auch
    rote Flaeche enthalten; betroffen_ohne_rot_in_raum = wert-Raeume ohne rote Flaeche (Text evtl. im Nachbarraum).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import math
import pickle
import re
import subprocess
import time
from collections import Counter, defaultdict
from pathlib import Path

from ezdxf import colors as ezcolors
from ezdxf import path as ezpath
from shapely.geometry import Point, Polygon
from shapely.ops import unary_union

REPO = Path(os.environ["NOTBEL_REPO"])
ERG = Path(os.environ.get("NOTBEL_GATE_CACHES",
                          REPO / "Projekte" / "_ergebnis_raumerkennung"))

MAX_TIEFE = 4
NAH_MM = 500.0
ROT_MAX_M2 = 3.0
ROT_R_MIN = 200
ROT_GB_MAX = 60
SCHLUSS_TOL_MM = 5.0
FLATTEN_MM = 5.0
STANZ_TYPEN = frozenset({"SCHACHT", "LIFT"})
FP_TYPEN = frozenset({"SCHACHT"})
BSP_MAX = 6
TOP_TEXTE = 60

# Schritt 1 — breites Inventar (bewusst uebervollstaendig, case-insensitive).
TOKENS = {
    "DDB": r"DDB", "BDB": r"(?<!F)BDB", "FBDB": r"FBDB", "WDB": r"WDB", "FDB": r"FDB", "DBA": r"DBA",
    "DB_wort": r"(?<![A-Z0-9])DB(?![A-Z])",
    "SCHACHT": r"SCHACHT", "SCH_wort": r"(?<![A-Z])SCH(?![A-Z])",
    "INSTALL": r"INSTALL", "STEIG": r"STEIG", "KAMIN": r"KAMIN",
    "LUEFTUNG": r"L\S{0,2}FTUNG", "AB_ZU_FORTLUFT": r"ABLUFT|ZULUFT|FORTLUFT",
    "HKLS": r"HKLS", "STRANG": r"STRANG", "FALLROHR": r"FALLROHR", "DURCHBRUCH": r"DURCHBRUCH",
    "SCHLITZ": r"SCHLITZ", "REVISION": r"REVISION", "VORWAND": r"VORWAND", "ROHR": r"ROHR",
}
TOKEN_RX = {k: re.compile(v, re.IGNORECASE) for k, v in TOKENS.items()}

# Schritt 3 — Marker (abgeleitet aus dem Inventar):
#  Durchbruch-Kuerzel als eigenes Wort (Ziffern direkt dahinter erlaubt: "DDB43/90") oder SCHACHT als
#  eigenes Wort. Komposita ("Schachtverzug ...", Hinweistext) fallen raus.
#  AUSSCHLUSS: Texte mit dem Wort RAUM benennen einen Raum ("DBA Raum", ArchiCAD-Zonenstempel), keinen Schacht.
MARKER = re.compile(r"(?<![A-Z])(?:F?BDB|DDB|WDB|FDB|DBA)(?![A-Z])|(?<![A-ZÄÖÜ])SCHACHT(?![A-ZÄÖÜ])", re.IGNORECASE)
AUSSCHLUSS = re.compile(r"(?<![A-ZÄÖÜ])RAUM(?![A-ZÄÖÜ])", re.IGNORECASE)
DEDUP_MM = 10.0            # gleicher Text <= 10 mm neben gleichem Text = Doppelexport, zaehlt einmal
NAH_MM_ALT = 1000.0        # Sensitivitaet: Textpunkte liegen gemessen meist 0,25-1 m neben der roten Kontur
ROT_FLAECHE_MIN_M2 = 0.02  # Rand-Splitter ignorieren; kleinster Durchbruch im Inventar 20/20 cm = 0,04 m2


def _polygon(pts):
    if len(pts) < 3:
        return None
    g = Polygon(pts).buffer(0)
    return None if g.is_empty else g


def _dxf(ordner: Path, kz: dict) -> Path | None:
    kand = [REPO / kz["dxf"]] if kz.get("dxf") else []
    kand.append(ERG.parent / ordner.relative_to(ERG).parent / f"{ordner.name}.dxf")
    return next((p for p in kand if p.exists()), None)


def _ist_rot(farbe) -> bool:
    k, v = farbe
    if k == "aci":
        return v == 1
    r, g, b = v
    return r >= ROT_R_MIN and g <= ROT_GB_MAX and b <= ROT_GB_MAX


def _farb_key(farbe) -> str:
    k, v = farbe
    return f"aci:{v}" if k == "aci" else "rgb:#{:02X}{:02X}{:02X}".format(*v)


class _Walker:
    def __init__(self, plan):
        self.plan = plan
        self.doc = plan.doc
        self.f = plan.factor
        self._lay: dict[str, tuple] = {}
        self.texte: list[dict] = []
        self.konturen: list[dict] = []
        self.typen: Counter = Counter()
        self.fehler = 0

    def layer_props(self, name: str):
        if name not in self._lay:
            lay = self.doc.layers.get(name)
            if lay is None:
                self._lay[name] = (("aci", 7), True)
            else:
                tc = lay.dxf.get("true_color", None)
                farbe = ("rgb", tuple(ezcolors.int2rgb(tc))) if tc is not None else ("aci", abs(lay.dxf.color))
                self._lay[name] = (farbe, lay.is_on() and not lay.is_frozen())
        return self._lay[name]

    def farbe(self, e, layer: str, erbe):
        tc = e.dxf.get("true_color", None)
        if tc is not None:
            return ("rgb", tuple(ezcolors.int2rgb(tc)))
        aci = e.dxf.get("color", 256)
        if aci == 0:
            return erbe or ("aci", 7)
        if aci == 256:
            return self.layer_props(layer)[0]
        return ("aci", aci)

    def _text(self, e, layer, farbe, pfad, tiefe):
        t = e.dxftype()
        try:
            if t == "MTEXT":
                txt = " | ".join(s.strip() for s in e.plain_text().splitlines() if s.strip())
                p = e.dxf.insert
            else:
                if t == "ATTRIB" and e.is_invisible:
                    return
                txt = str(e.dxf.text or "").strip()
                try:
                    _, p = e.get_placement()
                except Exception:  # noqa: BLE001
                    p = e.dxf.insert
                p = e.ocs().to_wcs(p)
        except Exception:  # noqa: BLE001
            self.fehler += 1
            return
        if not txt:
            return
        self.texte.append({"text": txt, "typ": t, "layer": layer, "farbe": _farb_key(farbe),
                           "sichtbar": self.layer_props(layer)[1], "pfad": "/".join(pfad), "tiefe": tiefe,
                           "xy": (float(p[0]) * self.f, float(p[1]) * self.f)})

    def _kontur(self, e, layer, farbe, pfad):
        t = e.dxftype()
        if t == "POLYLINE" and not e.is_2d_polyline:
            return
        try:
            pts = [(v.x * self.f, v.y * self.f) for v in ezpath.make_path(e).flattening(FLATTEN_MM / self.f)]
        except Exception:  # noqa: BLE001
            self.fehler += 1
            return
        if len(pts) < 3:
            return
        flag = e.closed if t == "LWPOLYLINE" else e.is_closed
        if not (flag or math.dist(pts[0], pts[-1]) <= SCHLUSS_TOL_MM):
            return
        g = _polygon(pts)
        if g is None or not (0 < g.area < ROT_MAX_M2 * 1e6):
            return
        self.konturen.append({"geo": g, "layer": layer, "farbe": farbe, "pfad": "/".join(pfad),
                              "sichtbar": self.layer_props(layer)[1]})

    def run(self):
        def walk(ents, tiefe, pfad, erbe_layer, erbe_farbe):
            for e in ents:
                t = e.dxftype()
                self.typen[t] += 1
                layer = e.dxf.get("layer", "0")
                if layer == "0" and erbe_layer:
                    layer = erbe_layer
                farbe = self.farbe(e, layer, erbe_farbe)
                if t == "INSERT":
                    for a in e.attribs:
                        al = a.dxf.get("layer", "0")
                        al = layer if al == "0" else al
                        self._text(a, al, self.farbe(a, al, farbe), pfad + (str(e.dxf.name),), tiefe + 1)
                    if tiefe < MAX_TIEFE:
                        try:
                            sub = list(e.virtual_entities())
                        except Exception:  # noqa: BLE001
                            self.fehler += 1
                            continue
                        walk(sub, tiefe + 1, pfad + (str(e.dxf.name),), layer, farbe)
                elif t in ("TEXT", "MTEXT", "ATTRIB"):
                    self._text(e, layer, farbe, pfad, tiefe)
                elif t in ("LWPOLYLINE", "POLYLINE"):
                    self._kontur(e, layer, farbe, pfad)

        walk(list(self.plan.space), 0, (), None, None)
        return self


def _bucket(d: float) -> str:
    if d == math.inf:
        return "keine"
    for grenze in (0, 250, 500, 1000, 2000):
        if d <= grenze:
            return f"<={grenze}"
    return ">2000"


def _norm(txt: str) -> str:
    return re.sub(r"\d+", "#", txt)[:50]


def messe_plan(cpath: Path, inv: dict) -> dict:
    from notbeleuchtung.raumerkennung.dxf_load import lade_dxf

    ordner = cpath.parent
    cache = pickle.loads(cpath.read_bytes())
    kzp = ordner / "kennzahlen.json"
    kz = json.loads(kzp.read_text(encoding="utf-8")) if kzp.exists() else {}
    dxf = _dxf(ordner, kz)
    key = f"{ordner.relative_to(ERG).parent.as_posix()}/{ordner.name.split(' - ')[0]}"
    out = {"ordner": str(ordner.relative_to(ERG)), "output_commit": kz.get("commit"),
           "dxf": str(dxf.relative_to(REPO)) if dxf else None}
    if dxf is None:
        out["fehler"] = "DXF nicht gefunden"
        return out
    out["dxf_sha_ok"] = (hashlib.sha256(dxf.read_bytes()).hexdigest() == kz.get("sha256")
                         if kz.get("sha256") else None)
    t0 = time.time()
    plan = lade_dxf(dxf)
    w = _Walker(plan).run()
    out["walk"] = {"s": round(time.time() - t0, 1), "factor": plan.factor, "fehler": w.fehler,
                   "texte_n": len(w.texte), "texte_unsichtbar_n": sum(1 for t in w.texte if not t["sichtbar"]),
                   "geschlossene_konturen_unter_max_n": len(w.konturen)}
    inv["typen"].update(w.typen)

    # ── Schritt 1: Inventar ───────────────────────────────────────────────
    for t in w.texte:
        treffer = [k for k, rx in TOKEN_RX.items() if rx.search(t["text"])]
        for k in treffer:
            z = inv["tokens"][k]
            z["n"] += 1
            z["je_plan"][key] += 1
            z["layer"][t["layer"]] += 1
            z["tiefe"][t["tiefe"]] += 1
            z["texte"][t["text"]] += 1
            if len(z["beispiele"]) < BSP_MAX:
                z["beispiele"].append({"plan": key, "text": t["text"], "layer": t["layer"], "pfad": t["pfad"],
                                       "xy": [round(v) for v in t["xy"]], "sichtbar": t["sichtbar"]})
        inv["normtexte"][_norm(t["text"])] += 1
    for k in w.konturen:
        inv["kontur_farben"][_farb_key(k["farbe"])] += 1
        if _ist_rot(k["farbe"]):
            inv["rot_layer"][k["layer"]] += 1
            inv["rot_pfad_top"][k["pfad"].split("/")[0].rstrip("0123456789") if k["pfad"] else "<space>"] += 1

    # ── Raeume ────────────────────────────────────────────────────────────
    raeume = [(r, g) for r in cache["raeume"] if (g := _polygon(r["polygon_mm"])) is not None]
    stanz = [(r, g) for r, g in raeume if (r.get("typ") or "") in STANZ_TYPEN]
    andere = [(r, g) for r, g in raeume if (r.get("typ") or "") not in STANZ_TYPEN]

    def einordnen(p: Point):
        d, sid = math.inf, None
        for r, g in stanz:
            dd = g.distance(p)
            if dd < d:
                d, sid = dd, r["id"]
        cov = [r for r, g in andere if g.covers(p)]
        kat = "schacht_nah" if d <= NAH_MM else ("raum_ohne_stanzung" if cov else "ausserhalb")
        return kat, cov, d, sid

    rot = [k for k in w.konturen if k["sichtbar"] and _ist_rot(k["farbe"])]

    def naechste_rote(p: Point):
        best_d, best_k = math.inf, None
        for k in rot:
            dd = k["geo"].distance(p)
            if dd < best_d:
                best_d, best_k = dd, k
        return best_d, best_k

    # ── Schritt 3: Marker ─────────────────────────────────────────────────
    kand = [t for t in w.texte if MARKER.search(t["text"])]
    out["marker_kandidaten_roh"] = len(kand)
    out["marker_unsichtbar_ausgeschlossen"] = sum(1 for t in kand if not t["sichtbar"])
    out["marker_ausschluss_regex"] = [t["text"] for t in kand if t["sichtbar"] and AUSSCHLUSS.search(t["text"])]
    marker: list[dict] = []
    dubl = 0
    for t in kand:
        if not t["sichtbar"] or AUSSCHLUSS.search(t["text"]):
            continue
        if any(m["text"] == t["text"] and math.dist(m["xy"], t["xy"]) <= DEDUP_MM for m in marker):
            dubl += 1
            continue
        marker.append(t)
    out["marker_duplikate_entfernt"] = dubl

    kat_n, rot_abst = Counter(), Counter()
    betroffen: dict[str, dict] = {}
    betroffen_alt: dict[str, dict] = {}
    marker_rows = []
    nah_und_deckt = 0
    n_alt = 0
    ausserhalb_abst: list[int] = []
    alle_raeume = unary_union([g for _, g in raeume]) if raeume else None

    def buche(ziel, cov, text):
        for r in cov:
            b = ziel.setdefault(r["id"], {"id": r["id"], "typ": r.get("typ") or "",
                                          "m2": round(r["flaeche_m2"], 2), "texte": []})
            b["texte"].append(text)

    for t in marker:
        p = Point(t["xy"])
        kat, cov, d, sid = einordnen(p)
        kat_n[kat] += 1
        if kat == "schacht_nah" and cov:
            nah_und_deckt += 1
        d_rot, k_rot = naechste_rote(p)
        rot_abst[_bucket(d_rot)] += 1
        abst_raeume = None
        if kat == "ausserhalb" and alle_raeume is not None:
            abst_raeume = round(alle_raeume.distance(p))
            ausserhalb_abst.append(abst_raeume)
        marker_rows.append({"text": t["text"], "xy": [round(v) for v in t["xy"]], "layer": t["layer"],
                            "pfad": t["pfad"], "kat": kat, "in_raeume": [r["id"] for r in cov],
                            "naechster_stanz": sid, "abstand_stanz_mm": None if sid is None else round(d),
                            "abstand_rot_mm": None if k_rot is None else round(d_rot),
                            "rot_layer": None if k_rot is None else k_rot["layer"],
                            "abstand_zu_raeumen_mm": abst_raeume})
        if kat == "raum_ohne_stanzung":
            buche(betroffen, cov, t["text"])
        if cov and d > NAH_MM_ALT:
            n_alt += 1
            buche(betroffen_alt, cov, t["text"])
    out["marker"] = {"gesamt": len(marker), "raum_ohne_stanzung": kat_n["raum_ohne_stanzung"],
                     "schacht_nah": kat_n["schacht_nah"], "schacht_nah_und_raum_deckt": nah_und_deckt,
                     "ausserhalb": kat_n["ausserhalb"], "abstand_text_zu_roter_kontur": dict(rot_abst),
                     "ausserhalb_max_abstand_zu_raeumen_mm": max(ausserhalb_abst, default=None),
                     "liste": marker_rows}
    out["betroffene_raeume"] = sorted(betroffen.values(), key=lambda b: b["id"])
    out["wert"] = len(betroffen)
    out["sensitiv_nah_1000mm"] = {"marker_raum_ohne_stanzung": n_alt, "wert": len(betroffen_alt),
                                  "raeume": sorted(betroffen_alt)}

    # ── Schritt 2: rote Konturen ─────────────────────────────────────────
    rk = Counter()
    rot_raeume = Counter()
    for k in rot:
        kat, cov, _d, _s = einordnen(k["geo"].representative_point())
        k["kat"] = kat
        rk[kat] += 1
        if kat == "raum_ohne_stanzung":
            for r in cov:
                rot_raeume[r["id"]] += 1
    out["rote_konturen"] = {"gesamt": len(rot), "m2_summe": round(sum(k["geo"].area for k in rot) / 1e6, 3),
                            "raum_ohne_stanzung": rk["raum_ohne_stanzung"], "schacht_nah": rk["schacht_nah"],
                            "ausserhalb": rk["ausserhalb"], "je_layer": dict(Counter(k["layer"] for k in rot)),
                            "raeume_ohne_stanzung": dict(rot_raeume)}
    rot_u = unary_union([k["geo"] for k in rot]) if rot else None
    flaeche = []
    rot_in_raeumen = 0.0
    if rot_u is not None and andere:
        for r, g in andere:
            a = g.intersection(rot_u).area / 1e6
            if a >= ROT_FLAECHE_MIN_M2:
                flaeche.append({"id": r["id"], "typ": r.get("typ") or "", "m2": round(r["flaeche_m2"], 2),
                                "rot_m2": round(a, 3)})
        rot_in_raeumen = unary_union([g for _, g in andere]).intersection(rot_u).area / 1e6
    out["rot_flaeche_in_raeumen"] = {"union_rot_m2": round(rot_u.area / 1e6, 3) if rot_u is not None else 0.0,
                                     "in_raeumen_m2": round(rot_in_raeumen, 3), "raeume_n": len(flaeche),
                                     "raeume": flaeche}
    ids_rot = {x["id"] for x in flaeche}
    out["wert_bestaetigt_rot"] = len(ids_rot & set(betroffen))
    out["betroffen_ohne_rot_in_raum"] = sorted(set(betroffen) - ids_rot)

    # ── FP-Kandidaten ─────────────────────────────────────────────────────
    fp = []
    for r, g in raeume:
        if (r.get("typ") or "") not in FP_TYPEN:
            continue
        txt_nah = [{"text": t["text"], "abstand_mm": round(g.distance(Point(t["xy"])))}
                   for t in marker if g.distance(Point(t["xy"])) <= NAH_MM]
        rot_nah = [{"layer": k["layer"], "m2": round(k["geo"].area / 1e6, 3), "abstand_mm": round(g.distance(k["geo"]))}
                   for k in rot if g.distance(k["geo"]) <= NAH_MM]
        d_txt = min((g.distance(Point(t["xy"])) for t in marker), default=math.inf)
        fp.append({"id": r["id"], "typ": r["typ"], "m2": round(r["flaeche_m2"], 2), "n_ecken": len(r["polygon_mm"]),
                   "naechster_marker_mm": None if d_txt == math.inf else round(d_txt),
                   "marker_text_nah": txt_nah, "rote_kontur_nah": rot_nah,
                   "fp_ohne_text": not txt_nah, "fp_ohne_text_und_rot": not txt_nah and not rot_nah})
    out["schacht_polygone"] = fp
    out["fp_ohne_text_n"] = sum(1 for x in fp if x["fp_ohne_text"])
    out["fp_ohne_text_und_rot_n"] = sum(1 for x in fp if x["fp_ohne_text_und_rot"])
    out["raeume_n"] = len(raeume)
    out["stanz_polygone_n"] = len(stanz)
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
    inv = {"tokens": defaultdict(lambda: {"n": 0, "je_plan": Counter(), "layer": Counter(), "tiefe": Counter(),
                                          "texte": Counter(), "beispiele": []}),
           "normtexte": Counter(), "typen": Counter(), "kontur_farben": Counter(), "rot_layer": Counter(),
           "rot_pfad_top": Counter()}
    for k in TOKENS:            # Null-Treffer sichtbar machen
        inv["tokens"][k]
    plaene = {}
    for cpath in sorted(ERG.rglob("_cache.pkl")):
        rel = cpath.parent.relative_to(ERG)
        key = f"{rel.parent.as_posix()}/{cpath.parent.name.split(' - ')[0]}"
        p = plaene[key] = messe_plan(cpath, inv)
        print(key, "wert", p.get("wert"), "alt1000", p.get("sensitiv_nah_1000mm"),
              "bestaetigt_rot", p.get("wert_bestaetigt_rot"), "dubl", p.get("marker_duplikate_entfernt"),
              "ausschl", p.get("marker_ausschluss_regex"),
              "marker", {k: v for k, v in p.get("marker", {}).items() if k != "liste"},
              "rot", p.get("rote_konturen", {}).get("gesamt"), "fp", p.get("fp_ohne_text_n"),
              p.get("fp_ohne_text_und_rot_n"), "walk", p.get("walk"), flush=True)

    tokens = {k: {"n": z["n"], "je_plan": dict(z["je_plan"]), "layer": dict(z["layer"].most_common(8)),
                  "tiefe": dict(z["tiefe"]), "texte_top": dict(z["texte"].most_common(15)),
                  "beispiele": z["beispiele"]}
              for k, z in sorted(inv["tokens"].items(), key=lambda kv: -kv[1]["n"])}
    res = {
        "metrik": "M3-schacht-ohne-stanzung", "repo_head": head,
        "konstanten": {"MAX_TIEFE": MAX_TIEFE, "NAH_MM": NAH_MM, "ROT_MAX_M2": ROT_MAX_M2, "ROT_R_MIN": ROT_R_MIN,
                       "ROT_GB_MAX": ROT_GB_MAX, "SCHLUSS_TOL_MM": SCHLUSS_TOL_MM, "FLATTEN_MM": FLATTEN_MM,
                       "STANZ_TYPEN": sorted(STANZ_TYPEN), "FP_TYPEN": sorted(FP_TYPEN),
                       "MARKER": MARKER.pattern, "AUSSCHLUSS": AUSSCHLUSS.pattern, "DEDUP_MM": DEDUP_MM,
                       "NAH_MM_ALT": NAH_MM_ALT, "ROT_FLAECHE_MIN_M2": ROT_FLAECHE_MIN_M2, "TOKENS": TOKENS},
        "inventar": {"tokens": tokens, "texte_normalisiert_top": dict(inv["normtexte"].most_common(TOP_TEXTE)),
                     "entity_typen": dict(inv["typen"].most_common()),
                     "farben_geschlossene_konturen_unter_max": dict(inv["kontur_farben"].most_common(25)),
                     "rot_layer": dict(inv["rot_layer"].most_common()),
                     "rot_pfad_top": dict(inv["rot_pfad_top"].most_common())},
        "summe": {"plaene": len(plaene),
                  "wert_raeume_ohne_stanzung": sum(p.get("wert", 0) for p in plaene.values()),
                  "wert_sensitiv_nah_1000mm": sum(p.get("sensitiv_nah_1000mm", {}).get("wert", 0)
                                                  for p in plaene.values()),
                  "marker_raum_ohne_stanzung_sensitiv_1000mm": sum(
                      p.get("sensitiv_nah_1000mm", {}).get("marker_raum_ohne_stanzung", 0) for p in plaene.values()),
                  "wert_bestaetigt_rot": sum(p.get("wert_bestaetigt_rot", 0) for p in plaene.values()),
                  "rot_flaeche_raeume_n": sum(p.get("rot_flaeche_in_raeumen", {}).get("raeume_n", 0)
                                              for p in plaene.values()),
                  "rot_in_raeumen_m2": round(sum(p.get("rot_flaeche_in_raeumen", {}).get("in_raeumen_m2", 0)
                                                 for p in plaene.values()), 3),
                  "marker_duplikate_entfernt": sum(p.get("marker_duplikate_entfernt", 0) for p in plaene.values()),
                  "marker_ausschluss_regex": sum(len(p.get("marker_ausschluss_regex", [])) for p in plaene.values()),
                  "marker_abstand_text_zu_roter_kontur": dict(sum(
                      (Counter(p.get("marker", {}).get("abstand_text_zu_roter_kontur", {})) for p in plaene.values()),
                      Counter())),
                  "marker_ausserhalb_max_abstand_zu_raeumen_mm": max(
                      (p.get("marker", {}).get("ausserhalb_max_abstand_zu_raeumen_mm") or 0 for p in plaene.values()),
                      default=0),
                  **{f"marker_{k}": sum(p.get("marker", {}).get(k, 0) for p in plaene.values())
                     for k in ("gesamt", "raum_ohne_stanzung", "schacht_nah", "schacht_nah_und_raum_deckt",
                               "ausserhalb")},
                  **{f"rot_{k}": sum(p.get("rote_konturen", {}).get(k, 0) for p in plaene.values())
                     for k in ("gesamt", "raum_ohne_stanzung", "schacht_nah", "ausserhalb")},
                  "schacht_polygone": sum(len(p.get("schacht_polygone", [])) for p in plaene.values()),
                  "fp_ohne_text": sum(p.get("fp_ohne_text_n", 0) for p in plaene.values()),
                  "fp_ohne_text_und_rot": sum(p.get("fp_ohne_text_und_rot_n", 0) for p in plaene.values())},
        "plaene": plaene,
    }
    Path(a.out).write_text(json.dumps(res, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    print("->", a.out)


if __name__ == "__main__":
    main()
