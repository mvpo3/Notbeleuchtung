"""build_l_gebaeude — Generator des synthetischen L-Demo-Gebäudes (Owner-Spec 2026-09-10).

Zwei Inputs für die Engine werden hier NICHT von Hand gezeichnet, sondern parametrisch
gebaut: aus der Quell-DXF `Four-story-Apartment.dxf` (P4) werden zwei reale Bausteine
extrahiert — `WHG_MUSTER` (Wohnungs-Footprint ohne Stiege) und `STIEGE_MUSTER` (die
zweiläufig-gewendelte Stiege, Auftritt 0,30 m / Laufbreite 1,00 m). Daraus entsteht ein
L-förmiges Gebäude (EG + 1OG) in DER Layer-Konvention, die Selmans Raumerkennung erwartet
(`02-TWA` Wand · `810 Raum` Raumpolygon+Stempel · `TÜR-<b>` Türblock · `09-WEG` Zirkulation).

Zusätzlich wird je Geschoss das GROUND-TRUTH-RaumModell (JSON, Contract-serialisierbar)
geschrieben — Fallback, falls die Erkennung die synthetische DXF nicht verarbeitet.

Deterministisch: keine Zeitstempel, kein Zufall; zweifacher Lauf = bitgleiche Ausgabe.

Ausgabe (nur nach P4, nichts ins Repo unter Projekte/):
  P4/demo/DEMO_EG.dxf · DEMO_1OG.dxf · DEMO_SPEC.md · LAYER_MAPPING.md
  P4/demo/DEMO_EG.raummodell.json · DEMO_1OG.raummodell.json
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

# Determinismus: gleiche dict/set-Ordnung je Lauf (sonst tauscht ezdxf OBJECTS-Reihenfolge).
if os.environ.get("PYTHONHASHSEED") != "0":
    os.environ["PYTHONHASHSEED"] = "0"
    os.execv(sys.executable, [sys.executable, *sys.argv])

import ezdxf

# ── Pfade (P4) ──────────────────────────────────────────────────────────────
P4 = Path(r"C:\Users\mvpst\Documents\KI-Projekt\Notbeleuchtung\Projektbeispiele-demo-Platzierungslogik")
Q = P4 / "Four-story-Apartment.dxf"
DEMO = P4 / "demo"
OUT = DEMO / "out"

# ── Geometrie-Konstanten (mm; Demo wird in mm geschrieben, $INSUNITS=4) ──────
GANG = 1500.0            # lichte Gangbreite
DEPTH = 15500.0         # Wohnungstiefe (aus Q-Footprint)
FRONT = 7600.0          # Wohnungsfront (aus Q-Footprint)
POCKET = 3000.0         # quadratischer Stiegen-Pocket am L-Knick (hält 2800×2000-Stiege)
W_AUSSEN = 250.0        # Außenwand Stahlbeton
W_INNEN = 200.0         # Trennwand Stahlbeton
N_A, N_B = 3, 2         # Wohnungen Schenkel A (Süd) / B (West)

# Gang-L (Achsen): horizontaler Arm nach +X, vertikaler Arm nach +Y, Pocket am Ursprung.
HX0, HX1 = POCKET, POCKET + N_A * FRONT            # 3000 .. 25800
VY0, VY1 = POCKET, POCKET + N_B * FRONT            # 3000 .. 18200

# ── Layer-Konvention (Ziel = Selman-Raumerkennung) ──────────────────────────
L_WALL = "02-TWA-G00-LEG-M0"       # WALL_PATTERN (Mollgasse-Dialekt)
L_ROOM = "810 Raum"                # _ROOM_LAYER (closed LWPOLYLINE + Stempel)
L_TXT = "01-TXT-G00-LEG-M0"
L_WEG = "09-WEG-G00-LEG-M0"        # Zirkulation
L_SYM = "05-SYM-G00-LEG-M0"        # Türblöcke
L_WHG = "90-DEMO-WHG"              # eingebettete Q-Wohnungsgeometrie (Fidelity)
L_STIEGE = "90-DEMO-STIEGE"        # eingebettete Q-Stiegengeometrie (Auftritt/Laufbreite)

# Spanisch → Ziel (für LAYER_MAPPING.md); Zählungen kommen aus der Extraktion.
DIALEKT = [
    ("MURO", L_WALL, "Wandlinienwerk (Haupt-Wand) → Wand-Layer der Erkennung"),
    ("MUROS", L_SYM, "trägt die Tür-INSERTs A$C27562579 → als benannte TÜR-Blöcke neu"),
    ("VENTANA", L_WHG, "Fenster → in WHG_MUSTER als Fidelity-Geometrie"),
    ("quicios", L_WHG, "Türlaibung Wohnungseingang → WHG_MUSTER"),
    ("SOLAR", L_STIEGE, "VERDREHTE SEMANTIK: trägt die Stiegen-Setzstufen (nicht ESCALERA!)"),
    ("ESCALERA", "—", "Fremd-/Grundstücksgeometrie (y 123–128 m), NICHT importiert"),
    ("A-MOBILIARIO/Muebles/0", "—", "Möbel/Ansichten weit außerhalb, weggeclippt"),
]

# ── Extraktion der Bausteine aus Q ──────────────────────────────────────────
FP = (-18.78, -11.18, 128.74, 144.24)   # Whg-Footprint (m)
ST = (-18.58, -15.78, 128.93, 130.93)   # Stiege (m)
WHITELIST = {"MURO", "MUROS", "VENTANA", "quicios"}
M = 1000.0                               # m → mm


def _inbox(p, b):
    x0, x1, y0, y1 = b
    return x0 - 0.01 <= p[0] <= x1 + 0.01 and y0 - 0.01 <= p[1] <= y1 + 0.01


def extract_bausteine():
    """WHG_MUSTER + STIEGE_MUSTER als normalisierte mm-Liniensegmente aus Q.

    Rückgabe: (whg_lines, stiege_lines) — je Liste [(x0,y0,x1,y1)] auf (0,0) normalisiert
    (Footprint-Ursprung bzw. Stiegen-Ursprung), Stiege AUS der Wohnung ausgeschnitten.
    """
    doc = ezdxf.readfile(str(Q))
    msp = doc.modelspace()
    fx0, fy0 = FP[0], FP[2]
    sx0, sy0 = ST[0], ST[2]
    whg, stiege = [], []
    for e in sorted(msp.query("LINE"), key=lambda e: (round(e.dxf.start.x, 3), round(e.dxf.start.y, 3))):
        s, en = e.dxf.start, e.dxf.end
        lyr = e.dxf.layer
        mid = ((s.x + en.x) / 2, (s.y + en.y) / 2)
        if lyr in WHITELIST and _inbox(s, FP) and _inbox(en, FP) and not _inbox(mid, ST):
            whg.append(((s.x - fx0) * M, (s.y - fy0) * M, (en.x - fx0) * M, (en.y - fy0) * M))
        if lyr == "SOLAR" and _inbox(s, ST) and _inbox(en, ST):
            stiege.append(((s.x - sx0) * M, (s.y - sy0) * M, (en.x - sx0) * M, (en.y - sy0) * M))
    return whg, stiege


# ── DXF-Bausteine ───────────────────────────────────────────────────────────
def _determinismus(doc):
    """Zeitstempel + GUIDs auf feste Werte — sonst ist die DXF pro Lauf verschieden."""
    for k in ("$TDCREATE", "$TDUCREATE", "$TDUPDATE", "$TDUUPDATE", "$TDINDWG"):
        if k in doc.header:
            doc.header[k] = 2451545.0        # J2000, fest
    doc.header["$FINGERPRINTGUID"] = "{00000000-0000-0000-0000-000000000000}"
    doc.header["$VERSIONGUID"] = "{00000000-0000-0000-0000-000000000001}"


_TD_VARS = {"$TDCREATE", "$TDUCREATE", "$TDUPDATE", "$TDUUPDATE", "$TDINDWG"}
_GUID_VARS = {"$VERSIONGUID": "{00000000-0000-0000-0000-000000000001}",
              "$FINGERPRINTGUID": "{00000000-0000-0000-0000-000000000000}"}


def _normalize_dxf(path):
    """Post-Save: ezdxf schreibt beim Save Zeitstempel/GUID/Versions-Stempel NEU (nur
    Metadaten, keine Geometrie). Die auf feste Werte setzen → byte-deterministische DXF."""
    lines = Path(path).read_text(encoding="utf-8").splitlines(keepends=True)
    out = []
    i = 0
    while i < len(lines):
        name = lines[i].strip()
        if name in _TD_VARS and i + 2 < len(lines):
            out.append(lines[i]); out.append(lines[i + 1]); out.append("2451545.0\n")
            i += 3; continue
        if name in _GUID_VARS and i + 2 < len(lines):
            out.append(lines[i]); out.append(lines[i + 1]); out.append(_GUID_VARS[name] + "\n")
            i += 3; continue
        # ezdxf-Metadaten-Stempel „<version> @ <ISO-Zeit>" → Zeit fixieren.
        out.append(re.sub(r"@ \d{4}-\d{2}-\d{2}T[0-9:.+\-]+", "@ 2000-01-01T00:00:00+00:00", lines[i]))
        i += 1
    Path(path).write_text("".join(out), encoding="utf-8")


def _ensure_layers(doc):
    for name in (L_WALL, L_ROOM, L_TXT, L_WEG, L_SYM, L_WHG, L_STIEGE):
        if name not in doc.layers:
            doc.layers.add(name)


def _tuer_block(doc, breite_mm):
    """Benannter Türblock `TÜR-<cm>` (Selman liest die Breite aus dem Namen: cm×10)."""
    cm = round(breite_mm / 10.0)
    name = f"TÜR-{cm}"
    if name in doc.blocks:
        return name
    blk = doc.blocks.new(name=name)
    b = breite_mm
    blk.add_line((0, 0), (b, 0))          # Schwelle
    blk.add_line((0, 0), (0, b))          # Türblatt
    blk.add_arc((0, 0), b, 0, 90)         # Schwenkbogen (Radius = Breite → Selman-ARC-Fallback)
    return name


def rect_walls(msp, x0, y0, x1, y1):
    for a, b in (((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)),
                 ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0))):
        msp.add_line(a, b, dxfattribs={"layer": L_WALL})


def room(msp, poly, stempel):
    msp.add_lwpolyline([(x, y) for x, y in poly], close=True, dxfattribs={"layer": L_ROOM})
    cx = sum(p[0] for p in poly) / len(poly)
    cy = sum(p[1] for p in poly) / len(poly)
    msp.add_text(stempel, dxfattribs={"layer": L_ROOM, "height": 300.0,
                                      "insert": (cx, cy)})


def tuer(msp, doc, xy, breite, name_hint=""):
    blk = _tuer_block(doc, breite)
    label = name_hint or blk
    msp.add_blockref(blk, xy, dxfattribs={"layer": L_SYM})
    msp.add_text(label, dxfattribs={"layer": L_TXT, "height": 200.0, "insert": (xy[0], xy[1] + 250)})


def embed(msp, lines, dx, dy, layer, rot=0):
    """Rohe Liniensegmente (mm, auf 0 normalisiert) an (dx,dy) einsetzen, opt. 90°-Rotation."""
    import math
    ca, sa = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    for x0, y0, x1, y1 in lines:
        p0 = (dx + x0 * ca - y0 * sa, dy + x0 * sa + y0 * ca)
        p1 = (dx + x1 * ca - y1 * sa, dy + x1 * sa + y1 * ca)
        msp.add_line(p0, p1, dxfattribs={"layer": layer})


# ── Raumgeometrie (Ground Truth, mm) ────────────────────────────────────────
def _rect(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def gang_poly():
    """L-Gang als drei Rechtecke (Pocket + H-Arm + V-Arm) — für Erkennung EIN GANG-Polygon
    je Arm + Pocket; hier als Liste (mehrere GANG-Räume zulässig, Erkennung mergt über Typ)."""
    pocket = _rect(0, 0, POCKET, POCKET)
    harm = _rect(HX0, 0, HX1, GANG)
    varm = _rect(0, VY0, GANG, VY1)
    return {"POCKET": pocket, "H": harm, "V": varm}


def stiege_slot():
    # Stiege 2800×2000 im Pocket, unten-links.
    return _rect(0, 0, 2800, 2000)


def whg_slots_A():
    return [(_rect(HX0 + i * FRONT, -DEPTH, HX0 + (i + 1) * FRONT, 0), (HX0 + (i + 0.5) * FRONT, 0))
            for i in range(N_A)]


def whg_slots_B():
    return [(_rect(-DEPTH, VY0 + j * FRONT, 0, VY0 + (j + 1) * FRONT), (0, VY0 + (j + 0.5) * FRONT))
            for j in range(N_B)]


def exits():
    # Schenkel A: Ostende; Schenkel B: Nordende. Je final_exit + 1,20-m-Tür.
    return {
        "EXIT-A": {"xy": (HX1, GANG / 2), "tuer": (HX1, GANG / 2)},
        "EXIT-B": {"xy": (GANG / 2, VY1), "tuer": (GANG / 2, VY1)},
    }


# ── RaumModell (Ground Truth) ───────────────────────────────────────────────
def _flaeche(poly):
    s = sum(poly[i][0] * poly[(i + 1) % len(poly)][1] - poly[(i + 1) % len(poly)][0] * poly[i][1]
            for i in range(len(poly)))
    return round(abs(s) / 2.0 / 1e6, 2)


def _raum(rid, typ, poly, **kw):
    d = {"id": rid, "raum_typ": typ, "polygon_mm": [[float(x), float(y)] for x, y in poly],
         "flaeche_m2": _flaeche(poly), "ist_fluchtweg": kw.get("fluchtweg", False),
         "ist_communal": kw.get("communal", False)}
    if kw.get("nutzung"):
        d["nutzungsklasse"] = kw["nutzung"]
    return d


def _tuer(tid, xy, von, nach, breite=1000.0, notausgang=False, detail=None):
    d = {"id": tid, "xy_mm": [float(xy[0]), float(xy[1])], "breite_mm": float(breite),
         "von_raum": von, "nach_raum": nach, "ist_notausgang": notausgang,
         "schwenk_richtung": "unbekannt"}
    if detail:
        d["tuer_detail"] = detail
    return d


def _seg(sid, pts, reason, ziel=None):
    laenge = sum(((pts[i + 1][0] - pts[i][0]) ** 2 + (pts[i + 1][1] - pts[i][1]) ** 2) ** 0.5
                 for i in range(len(pts) - 1))
    d = {"segment_id": sid, "polyline_mm": [[float(x), float(y)] for x, y in pts],
         "laenge_mm": laenge, "reason": reason, "quelle": "FALLBACK"}
    if ziel:
        d["ziel_ausgang"] = ziel
    return d


def _modell(floor, raeume, tueren, ausgaenge, segmente, stgh):
    xs = [p[0] for r in raeume for p in r["polygon_mm"]]
    ys = [p[1] for r in raeume for p in r["polygon_mm"]]
    return {"contract": "RaumModell", "contract_version": "1.4.0", "floor": floor,
            "coordinate_system": "mm",
            "bounds_mm": {"min_xy": [min(xs), min(ys)], "max_xy": [max(xs), max(ys)]},
            "raeume": raeume, "tueren": tueren, "ausgaenge": ausgaenge,
            "zirkulation": {"nodes": [], "edges": [], "segmente": segmente},
            "sonderstellen": [], "stiegenhaeuser": [stgh] if stgh else [], "anker": []}


def _gang_raeume(p):
    g = gang_poly()
    return [_raum(f"{p}-GANG-P", "GANG", g["POCKET"], fluchtweg=True, communal=True),
            _raum(f"{p}-GANG-H", "GANG", g["H"], fluchtweg=True, communal=True),
            _raum(f"{p}-GANG-V", "GANG", g["V"], fluchtweg=True, communal=True)]


def _stiege_raum(p):
    r = _raum(f"{p}-STGH", "STIEGENHAUS", stiege_slot(), communal=True)
    stgh = {"raum_id": f"{p}-STGH", "verbotszonen_mm": []}
    return r, stgh


def _segmente(p, mit_exits):
    # L-Zirkulation: V-Arm (Nordexit) → Knick → H-Arm (Ostexit).
    segs = [_seg(f"{p}-segV", [(GANG / 2, VY1), (GANG / 2, GANG / 2)],
                 "exit" if mit_exits else "long_run", ziel=f"{p}-EXIT-B" if mit_exits else None),
            _seg(f"{p}-segH", [(GANG / 2, GANG / 2), (HX1, GANG / 2)],
                 "exit" if mit_exits else "long_run", ziel=f"{p}-EXIT-A" if mit_exits else None)]
    return segs


def modell_eg():
    p = "EG"
    r = _gang_raeume(p)
    sr, stgh = _stiege_raum(p)
    r.append(sr)
    # Technik 15 m² (3×5) + Müll 18 m² (3,6×5) auf der Wohnungsseite des H-Gangs (Süd).
    tech = _rect(HX0, -5000, HX0 + 3000, 0)
    muell = _rect(HX0 + 3600, -5000, HX0 + 7200, 0)
    r.append(_raum(f"{p}-TECHNIK", "TECHNIK", tech, communal=True))
    r.append(_raum(f"{p}-MUELL", "MUELLRAUM", muell, communal=True))
    t = [_tuer(f"{p}-TECH-T", (HX0 + 1500, 0), f"{p}-TECHNIK", f"{p}-GANG-H", 900),
         _tuer(f"{p}-MUELL-T", (HX0 + 5400, 0), f"{p}-MUELL", f"{p}-GANG-H", 900)]
    ex = exits()
    a = [{"id": f"{p}-EXIT-A", "xy_mm": [float(ex['EXIT-A']['xy'][0]), float(ex['EXIT-A']['xy'][1])],
          "typ": "final_exit"},
         {"id": f"{p}-EXIT-B", "xy_mm": [float(ex['EXIT-B']['xy'][0]), float(ex['EXIT-B']['xy'][1])],
          "typ": "final_exit"}]
    t.append(_tuer(f"{p}-HE-A", ex["EXIT-A"]["tuer"], f"{p}-GANG-H", f"{p}-EXIT-A", 1200,
                   notausgang=True, detail="hauseingang"))
    t.append(_tuer(f"{p}-HE-B", ex["EXIT-B"]["tuer"], f"{p}-GANG-V", f"{p}-EXIT-B", 1200,
                   notausgang=True, detail="hauseingang"))
    return _modell(p, r, t, a, _segmente(p, True), stgh)


def modell_1og():
    p = "1OG"
    r = _gang_raeume(p)
    sr, stgh = _stiege_raum(p)
    r.append(sr)
    t = []
    for i, (poly, door) in enumerate(whg_slots_A(), 1):
        rid = f"{p}-WHG-A{i}"
        r.append(_raum(rid, "WOHNUNG", poly, nutzung="WOHNUNG_PRIVAT"))
        t.append(_tuer(f"{rid}-T", door, rid, f"{p}-GANG-H", 1000, detail="wohnungseingang"))
    for j, (poly, door) in enumerate(whg_slots_B(), 1):
        rid = f"{p}-WHG-B{j}"
        r.append(_raum(rid, "WOHNUNG", poly, nutzung="WOHNUNG_PRIVAT"))
        t.append(_tuer(f"{rid}-T", door, rid, f"{p}-GANG-V", 1000, detail="wohnungseingang"))
    # kein zweiter Ausgang; Flucht über die Stiege → Segmente ohne exit-Ziel.
    return _modell(p, r, t, [], _segmente(p, False), stgh)


# ── DXF-Schreiben ───────────────────────────────────────────────────────────
def _draw_floor(modell, whg_lines, stiege_lines, is_eg):
    doc = ezdxf.new(setup=True)
    doc.header["$INSUNITS"] = 4    # mm
    _determinismus(doc)
    _ensure_layers(doc)
    msp = doc.modelspace()
    modell["floor"]

    # Außen-Kontur der L (Wand) + Gang/Raum-Polygone.
    for r in modell["raeume"]:
        poly = [(x, y) for x, y in [tuple(pt) for pt in r["polygon_mm"]]]
        xs = [q[0] for q in poly]; ys = [q[1] for q in poly]
        rect_walls(msp, min(xs), min(ys), max(xs), max(ys))
        room(msp, poly, r["raum_typ"])

    # Türen (benannte Blöcke + Beschriftung).
    for t in modell["tueren"]:
        breite = t["breite_mm"]
        hint = "EINGANG" if t.get("ist_notausgang") else ""
        tuer(msp, doc, (t["xy_mm"][0], t["xy_mm"][1]), breite, name_hint=hint)

    # Zirkulation (09-WEG) als L-Polylinie durch die Gang-Mittelachse.
    weg = [(GANG / 2, VY1), (GANG / 2, GANG / 2), (HX1, GANG / 2)]
    msp.add_lwpolyline(weg, dxfattribs={"layer": L_WEG})

    # Stiege real (Auftritt 0,30 / Laufbreite 1,00 messbar erhalten) im Pocket.
    embed(msp, stiege_lines, 0.0, 0.0, L_STIEGE)

    # 1OG: reale Wohnungsgeometrie je Slot als Fidelity (Wing A orig, Wing B 90° gedreht).
    if not is_eg:
        for i, (poly, _door) in enumerate(whg_slots_A()):
            x0 = min(q[0] for q in poly); y0 = min(q[1] for q in poly)
            embed(msp, whg_lines, x0, y0, L_WHG)
        for j, (poly, _door) in enumerate(whg_slots_B()):
            x0 = min(q[0] for q in poly); y0 = min(q[1] for q in poly)
            embed(msp, whg_lines, x0 + DEPTH, y0, L_WHG, rot=90)
    return doc


def main():
    DEMO.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    whg_lines, stiege_lines = extract_bausteine()

    floors = {"EG": (modell_eg(), True), "1OG": (modell_1og(), False)}
    for label, (m, is_eg) in floors.items():
        doc = _draw_floor(m, whg_lines, stiege_lines, is_eg)
        doc.saveas(str(DEMO / f"DEMO_{label}.dxf"))
        _normalize_dxf(DEMO / f"DEMO_{label}.dxf")
        (DEMO / f"DEMO_{label}.raummodell.json").write_text(
            json.dumps(m, ensure_ascii=False, indent=1, sort_keys=False), encoding="utf-8")

    _write_layer_mapping(whg_lines, stiege_lines)
    _write_spec(floors, whg_lines, stiege_lines)
    print(f"WHG_MUSTER-Linien={len(whg_lines)} STIEGE_MUSTER-Linien={len(stiege_lines)}")
    for label, (m, _) in floors.items():
        print(f"{label}: raeume={len(m['raeume'])} tueren={len(m['tueren'])} "
              f"ausg={len(m['ausgaenge'])} seg={len(m['zirkulation']['segmente'])}")


def _write_layer_mapping(whg, stiege):
    rows = "\n".join(f"| `{sp}` | `{zi}` | {note} |" for sp, zi, note in DIALEKT)
    txt = f"""# LAYER_MAPPING — Quell-Dialekt (spanisch) → Demo-Konvention (Selman-Erkennung)

Der Demo-Plan wird NICHT im spanischen Quell-Dialekt geschrieben, sondern in der
Layer-Konvention, die `raumerkennung` erwartet. Fremddialekt-Erkennung ist ein eigener
Slice — dieser Test prüft **Platzierung + Lichtberechnung**, nicht Dialekterkennung.

| Quell-Layer (spanisch) | Ziel-Layer (Demo) | Anmerkung |
|---|---|---|
{rows}

**Verdrehte Semantik (Dialekt-Befund):** Im Quellplan liegen die Stiegen-Setzstufen auf
Layer `SOLAR` (nicht `ESCALERA`); `ESCALERA` trägt Grundstücks-/Fremdgeometrie (y 123–128 m).
Extrahiert: WHG_MUSTER = {len(whg)} Linien (MURO/VENTANA/quicios, Stiege ausgeschnitten),
STIEGE_MUSTER = {len(stiege)} SOLAR-Linien.
"""
    (DEMO / "LAYER_MAPPING.md").write_text(txt, encoding="utf-8")


def _write_spec(floors, whg, stiege):
    def area(poly):
        return _flaeche([tuple(p) for p in poly])
    lines = ["# DEMO_SPEC — L-Demo-Gebäude (generiert, mm)", "",
             "Quelle Bausteine: `Four-story-Apartment.dxf` (P4). Einheit Demo = mm ($INSUNITS=4).", "",
             "## Maße (Soll → Ist)",
             "- Gangbreite lichte: 1500 mm (Soll 1,50 m) ✓",
             f"- Wohnungsfront: {FRONT:.0f} mm · Tiefe: {DEPTH:.0f} mm (aus Q-Footprint 7,60×15,50 m)",
             f"- Schenkel A: {N_A} Whg (Front {N_A*FRONT:.0f} mm) · Schenkel B: {N_B} Whg (Front {N_B*FRONT:.0f} mm)",
             f"- Stiegen-Pocket am L-Knick: {POCKET:.0f}×{POCKET:.0f} mm (hält Stiege 2800×2000)",
             "", "## Stiegen-Kennwerte (aus Q, messbar erhalten)",
             f"- STIEGE_MUSTER-Linien: {len(stiege)} · Auftritt 0,30 m · Laufbreite 1,00 m · 2 Wendestufen 45°",
             "", "## Räume je Geschoss (Ist)"]
    for label, (m, _) in floors.items():
        lines.append(f"### {label}")
        for r in m["raeume"]:
            lines.append(f"- {r['id']} · {r['raum_typ']} · {r['flaeche_m2']} m²")
        lines.append(f"- Türen: {len(m['tueren'])} · Ausgänge: {len(m['ausgaenge'])} "
                     f"· Segmente: {len(m['zirkulation']['segmente'])}")
        lines.append("")
    lines += ["## Bewusste Abweichungen (begründet)",
              "- Stiege sitzt in einem 3,0×3,0-m-Pocket am L-Knick (Gang ist nur 1,5 m breit; eine",
              "  2,8×2,0-m-Stiege passt nicht in einen 1,5-m-Gang → lokaler Podest-/Pocket-Knoten).",
              "- Wohnungen auf der Außenseite (konvexe Seite) beider Schenkel — Süd (A) / West (B).",
              "- EG-Restfläche unprogrammiert (nur Technik+Müll+2 Ausgänge, wie spezifiziert)."]
    (DEMO / "DEMO_SPEC.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
