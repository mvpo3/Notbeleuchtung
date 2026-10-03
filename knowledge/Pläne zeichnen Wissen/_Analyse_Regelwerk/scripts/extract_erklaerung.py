"""extract_erklaerung.py — DXF-Evidenz-Extraktor für alle 5 Referenzprojekte.

Generalisierung von `scripts/analyse/mollgasse_gt_extract.py` (Messkonventionen
NB-R00 bleiben identisch):
- Position = Bbox-Zentrum der SICHTBAREN Geometrie (ezdxf.bbox über den
  aufgelösten INSERT) — Einfügepunkte tragen Basispunkt-Offsets.
- Welt-Pfeil = Blockbasis (down 270 / left 180 / right 0) + INSERT-Rotation;
  xscale < 0 spiegelt (links ↔ rechts).
- Personen: Blick = 180° + rot bei xscale > 0, sonst rot (Regel #8).
- Beidseitig: ko-lokalisierte Einzel-RZ-Paare (< 700 mm) ODER echter
  bothsided-Block.

Projekt-spezifisch (aus `inventur_dxf.py`, s. SYMBOLE_UND_LAYER.md):
Lehrlayer/Blöcke für Personen, Sichtlinien (türkis), Fluchtweg (grün),
Kennungen, gelbe Marker (Kreise/Diagonalen = Antipanik-Mitte/Alternativen).

Output: evidenz/<Projekt>/<datei_stem>.json — Schema kompatibel zum
REGELWERK-Beleg (datei/handle/block/rotation/x/y/layer/...).

Aufruf:
    python extract_erklaerung.py               # alle Projekte
    python extract_erklaerung.py Mollgasse E2  # Auswahl
"""
from __future__ import annotations

import json
import math
import re
import sys
import time
from pathlib import Path

import ezdxf
import ezdxf.bbox as ezbbox

HIER = Path(__file__).resolve()
WISSEN = HIER.parents[2]          # knowledge/Pläne zeichnen Wissen
OUT = HIER.parents[1] / "evidenz"

# Kanonische Leuchten-Typen: Blockname (lowercase) → (typ, richtung, basis_deg)
BLOCK_ALIAS: dict[str, tuple[str, str | None, float | None]] = {
    # Mollgasse (Alt-Namen)
    "rivo-sibel-arr-down": ("rz", "down", 270.0),
    "rivo-sibel-arr-left": ("rz", "left", 180.0),
    "rivo-rz-arr_right": ("rz", "right", 0.0),
    "antipanikleuchte-rivo": ("antipanik", None, None),
    "gruppenbatterie-verteiler": ("anlage", None, None),
    # RIVO_ARR-Welt (Tomaschek/AmRain/Hausfeld/E2) inkl. Tomaschek-`*0`-Duplikate
    "rivo_arr_down": ("rz", "down", 270.0),
    "rivo_arr_down0": ("rz", "down", 270.0),
    "rivo_arr_left": ("rz", "left", 180.0),
    "rivo_arr_left0": ("rz", "left", 180.0),
    "rivo_arr_right": ("rz", "right", 0.0),
    "rivo_arr_right0": ("rz", "right", 0.0),
    "rivo_arr_bothsided": ("rz", "bothsided", None),
    "rivo_arr_bothsided0": ("rz", "bothsided", None),
    "rivo_antipanik": ("antipanik", None, None),
    "rivo_antipanik0": ("antipanik", None, None),
    "rivo_aufheller": ("aufheller", None, None),
    "rivo_aufheller0": ("aufheller", None, None),
    "rivo_aufheller_variante": ("aufheller", None, None),
    "rivo_aufheller_variante0": ("aufheller", None, None),
    "rivo_gruppenbatterie_verteiler": ("anlage", None, None),
    "rivo_gruppenbatterie_verteiler0": ("anlage", None, None),
    # RIVO_NL-Zwischenstand (falls vorhanden)
    "rivo_nl_arr_down": ("rz", "down", 270.0),
    "rivo_nl_arr_left": ("rz", "left", 180.0),
    "rivo_nl_arr_right": ("rz", "right", 0.0),
    "rivo_nl_arr_bothsided": ("rz", "bothsided", None),
}

_GELB_ACIS = {2, 40, 50}           # gelbe Marker (Diagonale/Kreise)
_SICHT_ACI = 4                     # türkis/cyan
_GRUEN_ACIS = {3, 100, 102}
_GRUEN_TCS = {0x21DF37, 0x21DE37, 0x1EB350}


def _lay_re(pattern: str):
    return re.compile(pattern, re.IGNORECASE)


# Projekt-Konfiguration (aus Inventur — NICHT geraten)
PROJEKTE: dict[str, dict] = {
    "Mollgasse": {
        "ordner": "Mollgasse-Notbeleuchtungserklärung",
        "muster": r"^WHA_MOL_(?P<g>.+)_Notbeleuchtung_Erklärung\.dxf$",
        "person_bloecke": {"750298750", "9809550"},
        # 4444444 = grüne Fluchtweg-Pfeilspitze (Crop-verifiziert 2026-09-29),
        # KEIN Blickwinkel-Keil; Sichtlinien Mollgasse = ACI-4-Linien (Fallback).
        "fluchtweg_bloecke": {"fluchtwegpfeil", "4444444"},
    },
    "Tomaschek": {
        "ordner": "Tomaschek-Schule -Notbeleuchtungserklärung",
        "muster": r"^(?P<g>.+)_RIVO_Erklaerung\.dxf$",
        "sicht_layer": _lay_re(r"^RIVO_ERK_SICHTLINIE$"),
        "weg_layer": _lay_re(r"^RIVO_ERK_FLUCHTWEG$"),
        "kennung_layer": _lay_re(r"^RIVO_ERK_"),
    },
    "AmRain": {
        "ordner": "Am Rain Notbeleuchtungserklärung",
        "muster": r"^ARAI5_FE_XEL_ZZ_MOP_(?P<g>[A-Z0-9]+)_.+_TEILSTAND_v2\.dxf$",
        # EG doppelt: nur die Erklär-Fassung für EG, RIVO_Symbole für den Rest
        "datei_filter": lambda name: ("EG_Erklaerung" in name) or ("EG_0011" not in name),
        "ignore_layer": _lay_re(r"^SIMA_ET_"),  # SIMA-Zweitwelt (Owner: ignorieren)
    },
    "Hausfeld": {
        "ordner": "Hausfeldstraße Notbeleuchtung zeichnen",
        "muster": r"^Hausfeldstraße_(?P<g>.+)_Notbeleuchtung_RIVO\.dxf$",
        "szene_layer": _lay_re(
            r"^HF_LEHR_HF-(?P<g>[A-Z0-9]+)-S(?P<s>\d+)_(?P<kat>WEGE|SICHT|MENSCHEN|KENNUNGEN|HINWEISE)$"
        ),
    },
    "BaufeldE2": {
        "ordner": "Baufeld E2 Notbeleuchtung zeichnen",
        "muster": r"^Notbeleuchtungspläne_(?P<g>UG)_RIVO_mit_Lehrlayern\.dxf$",
        "person_bloecke": {"E2_MOL_LEHRPERSON_ZENTRIERT".lower()},
        "sicht_layer": _lay_re(r"^E2_LEHR_WEG_B_INTERPRETATION$"),
        "weg_layer": _lay_re(r"^681 Fluchtlinien"),
        "kennung_layer": _lay_re(r"^E2_LEHR_KENNUNG$"),
    },
}


def _bbox_zentrum(entity) -> tuple[float, float] | None:
    try:
        ext = ezbbox.extents([entity], fast=False)
    except Exception:  # noqa: BLE001 — Analyse-Robustheit
        # korrupte Sub-Entities (z.B. Extrusion 0,0,0) → fast-Modus, dann Insert
        try:
            ext = ezbbox.extents([entity], fast=True)
        except Exception:  # noqa: BLE001 — Analyse-Robustheit
            ins = getattr(entity.dxf, "insert", None)
            return (round(ins.x, 1), round(ins.y, 1)) if ins is not None else None
    if not ext.has_data:
        return None
    return (round(ext.center.x, 1), round(ext.center.y, 1))


def _welt_pfeil(basis: float | None, rot: float, xscale: float) -> float | None:
    if basis is None:
        return None
    if xscale < 0:
        basis = (180.0 - basis) % 360.0
    return (basis + rot) % 360.0


def _farbe(e) -> int | None:
    return getattr(e.dxf, "color", None)


def _true_color(e) -> int | None:
    return e.dxf.true_color if e.dxf.hasattr("true_color") else None


def _ist_gruen(e) -> bool:
    return _true_color(e) in _GRUEN_TCS or _farbe(e) in _GRUEN_ACIS


def _punkte(e) -> list[tuple[float, float]]:
    """Start/Ende (LINE) bzw. Stützpunkte (LWPOLYLINE), gerundet."""
    if e.dxftype() == "LINE":
        return [(round(e.dxf.start.x, 1), round(e.dxf.start.y, 1)),
                (round(e.dxf.end.x, 1), round(e.dxf.end.y, 1))]
    if e.dxftype() == "LWPOLYLINE":
        return [(round(x, 1), round(y, 1)) for x, y, *_ in e.get_points()]
    if e.dxftype() == "SOLID":
        pts = []
        for attr in ("vtx0", "vtx1", "vtx2", "vtx3"):
            v = getattr(e.dxf, attr, None)
            if v is not None:
                pts.append((round(v.x, 1), round(v.y, 1)))
        return pts
    return []


def extrahiere_datei(projekt: str, cfg: dict, pfad: Path, geschoss: str) -> dict:
    t0 = time.time()
    doc = ezdxf.readfile(str(pfad))
    ms = doc.modelspace()

    person_bloecke = {b.lower() for b in cfg.get("person_bloecke", set())}
    blick_bloecke = {b.lower() for b in cfg.get("blick_bloecke", set())}
    weg_bloecke = {b.lower() for b in cfg.get("fluchtweg_bloecke", set())}
    sicht_layer = cfg.get("sicht_layer")
    weg_layer = cfg.get("weg_layer")
    kennung_layer = cfg.get("kennung_layer")
    szene_layer = cfg.get("szene_layer")
    ignore_layer = cfg.get("ignore_layer")

    leuchten: list[dict] = []
    personen: list[dict] = []
    sichtlinien: list[dict] = []
    fluchtwege: list[dict] = []
    kennungen: list[dict] = []
    gelb_marker: list[dict] = []
    hinweise: list[dict] = []

    def _szene(layer: str) -> dict:
        """Hausfeld-Szenen-Tag aus dem Layernamen (S##)."""
        if szene_layer is None:
            return {}
        m = szene_layer.match(layer)
        if not m:
            return {}
        return {"szene": int(m.group("s")), "kategorie": m.group("kat")}

    for e in ms:
        lay = e.dxf.layer
        if ignore_layer is not None and ignore_layer.match(lay):
            continue
        typ = e.dxftype()
        sz = _szene(lay)

        if typ == "INSERT":
            name = e.dxf.name.strip().lower()
            if name in BLOCK_ALIAS:
                kind, richtung, basis = BLOCK_ALIAS[name]
                rot = float(e.dxf.rotation) % 360.0
                xs = float(e.dxf.xscale)
                leuchten.append({
                    "datei": pfad.name,
                    "handle": e.dxf.handle,
                    "block": e.dxf.name,
                    "typ": kind,
                    "richtung_block": richtung,
                    "xy_mm": _bbox_zentrum(e),
                    "insert_xy_mm": (round(e.dxf.insert.x, 1), round(e.dxf.insert.y, 1)),
                    "rot_deg": round(rot, 2),
                    "xscale": round(xs, 4),
                    "welt_pfeil_deg": (round(w, 2) if (w := _welt_pfeil(basis, rot, xs)) is not None else None),
                    "layer": lay,
                    **sz,
                })
            elif name in person_bloecke:
                rot = float(e.dxf.rotation) % 360.0
                xs = float(e.dxf.xscale)
                blick = (180.0 + rot) % 360.0 if xs > 0 else rot % 360.0
                personen.append({
                    "datei": pfad.name, "handle": e.dxf.handle, "block": e.dxf.name,
                    "xy_mm": _bbox_zentrum(e), "rot_deg": round(rot, 2),
                    "xscale": round(xs, 4), "blick_deg": round(blick, 2),
                    "layer": lay, **sz,
                })
            elif name in blick_bloecke:
                rot = float(e.dxf.rotation) % 360.0
                sichtlinien.append({
                    "datei": pfad.name, "handle": e.dxf.handle, "block": e.dxf.name,
                    "art": "keil", "xy_mm": _bbox_zentrum(e),
                    "rot_deg": round(rot, 2), "layer": lay, **sz,
                })
            elif name in weg_bloecke:
                rot = float(e.dxf.rotation) % 360.0
                fluchtwege.append({
                    "datei": pfad.name, "handle": e.dxf.handle, "block": e.dxf.name,
                    "art": "pfeil", "xy_mm": _bbox_zentrum(e),
                    "rot_deg": round(rot, 2), "layer": lay, **sz,
                })
            elif szene_layer is not None and sz:
                # Hausfeld: unbekannte Blöcke auf Lehr-Layern mitnehmen
                eintrag = {
                    "datei": pfad.name, "handle": e.dxf.handle, "block": e.dxf.name,
                    "xy_mm": _bbox_zentrum(e),
                    "rot_deg": round(float(e.dxf.rotation) % 360.0, 2),
                    "xscale": round(float(e.dxf.xscale), 4), "layer": lay, **sz,
                }
                if sz.get("kategorie") == "MENSCHEN":
                    xs = eintrag["xscale"]
                    rot = eintrag["rot_deg"]
                    eintrag["blick_deg"] = round((180.0 + rot) % 360.0 if xs > 0 else rot, 2)
                    personen.append(eintrag)
                else:
                    hinweise.append(eintrag)

        elif typ in ("LINE", "LWPOLYLINE", "SPLINE", "ARC", "CIRCLE", "SOLID"):
            ist_sicht_lay = sicht_layer is not None and sicht_layer.match(lay)
            ist_weg_lay = weg_layer is not None and weg_layer.match(lay)
            ist_sz_sicht = sz.get("kategorie") == "SICHT"
            ist_sz_weg = sz.get("kategorie") == "WEGE"
            if ist_sicht_lay or ist_sz_sicht or (
                sicht_layer is None and szene_layer is None
                and _farbe(e) == _SICHT_ACI and typ in ("LINE", "LWPOLYLINE")
            ):
                sichtlinien.append({
                    "datei": pfad.name, "handle": e.dxf.handle, "art": typ.lower(),
                    "punkte": _punkte(e), "layer": lay, **sz,
                })
            elif ist_weg_lay or ist_sz_weg or (
                weg_layer is None and szene_layer is None
                and typ == "LWPOLYLINE" and _ist_gruen(e)
            ):
                fluchtwege.append({
                    "datei": pfad.name, "handle": e.dxf.handle, "art": typ.lower(),
                    "punkte": _punkte(e), "layer": lay, **sz,
                })
            elif _farbe(e) in _GELB_ACIS:
                d = {
                    "datei": pfad.name, "handle": e.dxf.handle, "art": typ.lower(),
                    "layer": lay, **sz,
                }
                if typ == "CIRCLE":
                    c = e.dxf.center
                    d["xy_mm"] = (round(c.x, 1), round(c.y, 1))
                    d["radius_mm"] = round(e.dxf.radius, 1)
                else:
                    d["punkte"] = _punkte(e)
                gelb_marker.append(d)

        elif typ in ("MTEXT", "TEXT"):
            text = (e.text if typ == "MTEXT" else e.dxf.text).strip()
            if not text or len(text) > 60:
                continue
            ist_kennung_lay = kennung_layer is not None and kennung_layer.match(lay)
            ist_sz = bool(sz)
            if ist_kennung_lay or ist_sz or _ist_gruen(e) or _farbe(e) == _SICHT_ACI:
                p = e.dxf.insert
                kennungen.append({
                    "datei": pfad.name, "handle": e.dxf.handle, "text": text,
                    "xy_mm": (round(p.x, 1), round(p.y, 1)), "layer": lay, **sz,
                })

    # Beidseitig-Gruppen: echter bothsided-Block ODER ko-lokalisierte Paare
    rz = [l for l in leuchten if l["typ"] == "rz" and l["xy_mm"]]
    gruppe = 0
    for l in rz:
        if l["richtung_block"] == "bothsided":
            gruppe += 1
            l["beidseitig_gruppe"] = gruppe
    for i, a in enumerate(rz):
        if "beidseitig_gruppe" in a:
            continue
        for b in rz[i + 1:]:
            if "beidseitig_gruppe" in b or b["xy_mm"] is None:
                continue
            if math.dist(a["xy_mm"], b["xy_mm"]) < 700.0:
                gruppe += 1
                a["beidseitig_gruppe"] = b["beidseitig_gruppe"] = gruppe

    return {
        "projekt": projekt,
        "geschoss": geschoss,
        "datei": pfad.name,
        "quelle": str(pfad.relative_to(WISSEN)),
        "n_leuchten": len(leuchten),
        "n_beidseitig_gruppen": gruppe,
        "n_personen": len(personen),
        "n_sichtlinien": len(sichtlinien),
        "n_fluchtwege": len(fluchtwege),
        "n_kennungen": len(kennungen),
        "n_gelb_marker": len(gelb_marker),
        "leuchten": leuchten,
        "personen": personen,
        "sichtlinien": sichtlinien,
        "fluchtwege": fluchtwege,
        "kennungen": kennungen,
        "gelb_marker": gelb_marker,
        "hinweise": hinweise,
        "dauer_s": round(time.time() - t0, 1),
    }


def main(argv: list[str]) -> int:
    auswahl = set(argv) or set(PROJEKTE)
    for projekt, cfg in PROJEKTE.items():
        if projekt not in auswahl:
            continue
        ordner = WISSEN / cfg["ordner"]
        out_dir = OUT / projekt
        out_dir.mkdir(parents=True, exist_ok=True)
        muster = re.compile(cfg["muster"])
        dateien = sorted(p for p in ordner.iterdir() if p.is_file() and muster.match(p.name))
        if flt := cfg.get("datei_filter"):
            dateien = [p for p in dateien if flt(p.name)]
        for p in dateien:
            g = muster.match(p.name).group("g")
            daten = extrahiere_datei(projekt, cfg, p, g)
            out = out_dir / f"{p.stem}.json"
            out.write_text(json.dumps(daten, ensure_ascii=False, indent=1), encoding="utf-8")
            print(f"[{projekt}/{g}] {daten['n_leuchten']} Leuchten "
                  f"({daten['n_beidseitig_gruppen']} beids.), {daten['n_personen']} Pers., "
                  f"{daten['n_sichtlinien']} Sicht, {daten['n_fluchtwege']} Weg, "
                  f"{daten['n_kennungen']} Kennungen, {daten['n_gelb_marker']} gelb "
                  f"[{daten['dauer_s']}s]", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
