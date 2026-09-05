"""dxf_renderer — PlatzierungsErgebnis + RaumModell → Notbeleuchtungs-DXF.

Generative Adaption von elektro-planer backend/engine/dxf_writer.py (siehe
docs/PORT_LOG.md): konsumiert Contract-Objekte statt Placement-/Architektur-
JSON. Gezeichnet werden Raum-Konturen + raum_typ-Labels, Fluchtweg-Segmente,
die Schrack-Symbole (via symbols/inserter), Stromkreis-Labels mit
Anti-Kollision und Montagehöhen-Koten (h=2,40 je Symbol). Wände/Pass-Through-
Architektur und das Paperspace-Layout-Template folgen in späteren Slices.

Layer-Schema folgt der DIN_SIBEL-Profi-Konvention (siehe knowledge/extracted/
PROFI_DIN_PLAN_UND_VORSCHRIFTEN.md §1.3): die Symbole liegen auf
`din_SIBEL_10_emergency_lighting` (aus dem Library-Layer umbenannt); dazu je ein
DIN_SIBEL-Layer für Beschriftung/Info/Legende/Plankopf und die Architektur-Kontur.
"""
from __future__ import annotations

import math
import re
from pathlib import Path

import ezdxf
from ezdxf.enums import MTextEntityAlignment

from notbeleuchtung.hauptengine.contracts import LBVorgabe, PlatzierungsErgebnis, RaumModell
from notbeleuchtung.symbols import inserter, library

# DIN_SIBEL-Layer-Schema (Profi-Konvention, siehe knowledge/extracted/
# PROFI_DIN_PLAN_UND_VORSCHRIFTEN.md §1.3). Lean-Rename: 1 Layer je Plan-Element,
# semantische DIN_SIBEL-Namen statt Ad-hoc-`E_*`. Architektur-Hintergrund (`ARCH_*`)
# bleibt — das ist kein SIBEL-Element.
LAYER_NOTBELEUCHTUNG = library.SAFETY_LAYER  # din_SIBEL_10_emergency_lighting
LAYER_ARCH_RAUM = "ARCH_Raum"
LAYER_ARCH_TUER = "ARCH_Tuer"
LAYER_FLUCHTWEG = "ARCH_Fluchtweg"
LAYER_LEGENDE = "din_SIBEL_70_legend_white"
LAYER_STUECKLISTE = "din_SIBEL_70_legend_green"
LAYER_PLANKOPF = "din_SIBEL_99_titleblock"
LAYER_PRUEFBERICHT = "din_SIBEL_99_inspection"
LAYER_NODEID = "din_SIBEL_63_luminaire_ID"
LAYER_BELEGUNG = "din_SIBEL_11_system"

_PRUEF_STATUS_LABEL = {"ok": "OK", "warnung": "WARNUNG", "fehler": "FEHLER"}

ROOM_LABEL_HEIGHT_MM = 120.0
LEGENDE_HEIGHT_MM = 200.0
LEGENDE_OFFSET_MM = 1000.0   # Abstand über der Grundriss-Oberkante

# Schriftfeld-Leiste (rechts neben dem Grundriss): ALLE Info-Blöcke in EINER Spalte
# gerahmter Boxen mit festen Höhen (deterministisch, kein fragiles Text-Messen), von
# unten nach oben gestapelt — Plankopf unten (Konvention), darüber Prüfbericht,
# Stückliste, Legende. Ersetzt die früher frei um den Grundriss verstreuten Blöcke.
_PANEL_ABSTAND_MM = 2000.0   # Grundriss → Spalte
_PANEL_B_MM = 16000.0        # Spaltenbreite
_PANEL_PAD_MM = 400.0
_PANEL_GAP_MM = 600.0        # Lücke zwischen Boxen
_BOX_H_PLANKOPF_MM = 5600.0
_BOX_H_PRUEF_MM = 8200.0
_BOX_H_STUECK_MM = 3400.0
_BOX_H_LEGENDE_MM = 4400.0
_BOX_H_BELEGUNG_MM = 5000.0
# y-Unterkanten relativ zu min_y (bottom-up):
_BOX_Y_PLANKOPF = 0.0
_BOX_Y_PRUEF = _BOX_H_PLANKOPF_MM + _PANEL_GAP_MM
_BOX_Y_STUECK = _BOX_Y_PRUEF + _BOX_H_PRUEF_MM + _PANEL_GAP_MM
_BOX_Y_LEGENDE = _BOX_Y_STUECK + _BOX_H_STUECK_MM + _PANEL_GAP_MM
_BOX_Y_BELEGUNG = _BOX_Y_LEGENDE + _BOX_H_LEGENDE_MM + _PANEL_GAP_MM


def _draw_info_box(msp, raum: RaumModell, y_unten_rel: float, hoehe: float,
                   layer: str, text: str, *, char_h: float = LEGENDE_HEIGHT_MM) -> None:
    """Gerahmte Info-Box in der rechten Schriftfeld-Leiste (feste Größe, Text wrappt)."""
    (_min_x, min_y), (max_x, _max_y) = raum.bounds_mm.min_xy, raum.bounds_mm.max_xy
    x0 = max_x + _PANEL_ABSTAND_MM
    y0 = min_y + y_unten_rel
    x1, y1 = x0 + _PANEL_B_MM, y0 + hoehe
    msp.add_lwpolyline([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], close=True,
                       dxfattribs={"layer": layer})
    mt = msp.add_mtext(text, dxfattribs={"layer": layer, "char_height": char_h})
    mt.dxf.width = _PANEL_B_MM - 2 * _PANEL_PAD_MM   # Referenzbreite → Zeilenumbruch
    mt.set_location((x0 + _PANEL_PAD_MM, y1 - _PANEL_PAD_MM),
                    attachment_point=MTextEntityAlignment.TOP_LEFT)

# Menschenlesbare Symbol-Arten für die Stückliste.
_KIND_LABEL = {
    "rz": "Rettungszeichen",
    "sicherheitsleuchte": "Sicherheitsleuchte (Aufheller)",
    "antipanik": "Antipanik-Leuchte",
}



# NODEID-Annotation (fortlaufende Leuchten-ID je Symbol, Wartung/Adressierung, Profi-
# Plan din_SIBEL_63_luminaire_ID). Sitzt tangential (entlang der Symbol-Achse), damit
# sie weder mit dem Stromkreis-Label (+Normale) noch der Höhenkote (−Normale) kollidiert.
NODEID_HEIGHT_MM = 90.0
# Offset je Art = Symbol-Halbbreite (gemessen: RZ-Block 580×290, kleiner SL-Aufheller
# 342×342 = 1.85 units × 185, Antipanik 1043×294) + Clearance für die halbe Textbreite
# → Label sitzt knapp NEBEN dem Symbol, nicht drin und nicht abgesetzt.
_NODEID_HALBBREITE_MM = {"rz": 290.0, "sicherheitsleuchte": 171.0, "antipanik": 522.0}
NODEID_CLEARANCE_MM = 280.0
_KIND_CODE = {"rz": "RZ", "sicherheitsleuchte": "SL", "antipanik": "AP"}

# Schaltungsart je Leuchtenart (Profi-Belegungsplan 1.xlsx §3b): Rettungszeichen =
# Dauerlicht (DL, maintained, muss immer leuchten), Sicherheits-/Antipanik-Leuchten =
# Bereitschaftslicht (BL, non-maintained, nur im Notfall). Speist die Stromkreis-
# Belegungsliste; im Symbol-Datenmodell (Contract-Empf. #6) später ein echtes Feld.
_SCHALTUNGSART = {"rz": "DL", "sicherheitsleuchte": "BL", "antipanik": "BL"}


def _add_own_layers(doc) -> None:
    doc.layers.add(LAYER_ARCH_RAUM, color=8)    # dunkelgrau
    doc.layers.add(LAYER_ARCH_TUER, color=8)    # dunkelgrau (Architektur-Bestand)
    fw = doc.layers.add(LAYER_FLUCHTWEG)        # Fluchtweg in Notbeleuchtungs-Grün
    fw.dxf.true_color = (30 << 16) | (180 << 8) | 80
    doc.layers.add(LAYER_LEGENDE, color=7)      # weiß/schwarz
    doc.layers.add(LAYER_STUECKLISTE, color=7)  # weiß/schwarz
    doc.layers.add(LAYER_PLANKOPF, color=7)     # weiß/schwarz
    doc.layers.add(LAYER_PRUEFBERICHT, color=7)  # weiß/schwarz
    doc.layers.add(LAYER_NODEID, color=6)        # magenta
    doc.layers.add(LAYER_BELEGUNG, color=7)      # weiß/schwarz


def _lb_legende_text(lb: LBVorgabe | None) -> str | None:
    """SV-Anlagen-Kennzeichnung aus den gesetzten LB-Vorgaben (None = nichts zu zeigen)."""
    if lb is None:
        return None
    zeilen = ["SICHERHEITSBELEUCHTUNG (Leistungsbeschreibung)"]
    _SYS = {"einzelbatterie": "Einzelbatterie", "gruppenbatterie": "Gruppenbatterie",
            "zentralbatterie": "Zentralbatterie"}
    if lb.system_typ:
        zeilen.append(f"System: {_SYS.get(lb.system_typ, lb.system_typ)}")
    if lb.betriebsdauer_min is not None:
        zeilen.append(f"Betriebsdauer: {lb.betriebsdauer_min / 60:g} h")
    if lb.umschaltzeit_max_s is not None:
        zeilen.append(f"Umschaltzeit: < {lb.umschaltzeit_max_s:g} s")
    if lb.mindest_lux_fluchtweg is not None:
        zeilen.append(f"Fluchtweg: min. {lb.mindest_lux_fluchtweg:g} lx")
    if lb.piktogramm_norm:
        zeilen.append(f"Piktogramme: {lb.piktogramm_norm}")
    if lb.norm_bezug:
        zeilen.append("Normbezug: " + ", ".join(lb.norm_bezug))
    if lb.lb_quelle:
        zeilen.append(f"Quelle: {lb.lb_quelle}")
    # Nur zeichnen, wenn über den Titel hinaus etwas Konkretes drinsteht.
    return "\\P".join(zeilen) if len(zeilen) > 1 else None


def _draw_lb_legende(msp, raum: RaumModell, lb: LBVorgabe | None) -> bool:
    """Legenden-Box (SV-System-Spec) oben in der rechten Schriftfeld-Leiste."""
    text = _lb_legende_text(lb)
    if text is None:
        return False
    _draw_info_box(msp, raum, _BOX_Y_LEGENDE, _BOX_H_LEGENDE_MM, LAYER_LEGENDE, text)
    return True


def _stueckliste_text(platzierung: PlatzierungsErgebnis) -> str | None:
    """Stückliste. None wenn leer.

    Tragen ALLE Platzierungen einen `typ_letter` (Symbol-Datenmodell v1.2.0), wird
    die Profi-Form gerendert: **Typ-Letter-Legende** (Digest #7, Gruppierung nach
    Legenden-Letter wie in der Barawitzkagasse-Stückliste), Produkt = `typ_name`
    oder ersatzweise der `catalog_key`. Sonst — Fremd-Platzierer, alte Fixtures —
    das bisherige Art+Anzahl-Format (Fallback, keine Golden-Änderung).
    """
    if not platzierung.platzierungen:
        return None
    if all(p.typ_letter for p in platzierung.platzierungen):
        gruppen: dict[str, dict] = {}
        for p in platzierung.platzierungen:
            g = gruppen.setdefault(
                p.typ_letter,
                {"kind": p.kind, "produkt": p.typ_name or p.catalog_key, "n": 0},
            )
            g["n"] += 1
        zeilen = ["STÜCKLISTE"]
        for letter in sorted(gruppen):
            g = gruppen[letter]
            label = _KIND_LABEL.get(g["kind"], g["kind"])
            zeilen.append(f"Typ {letter}: {g['n']}× {label} — {g['produkt']}")
        zeilen.append(f"Summe: {len(platzierung.platzierungen)}")
        return "\\P".join(zeilen)

    counts: dict[str, int] = {}
    for p in platzierung.platzierungen:
        counts[p.kind] = counts.get(p.kind, 0) + 1
    zeilen = ["STÜCKLISTE"]
    for kind in ("rz", "sicherheitsleuchte", "antipanik"):
        if counts.get(kind):
            zeilen.append(f"{_KIND_LABEL[kind]}: {counts[kind]}")
    # Etwaige unbekannte Arten defensiv anhängen.
    for kind, n in counts.items():
        if kind not in _KIND_LABEL:
            zeilen.append(f"{kind}: {n}")
    zeilen.append(f"Summe: {len(platzierung.platzierungen)}")
    return "\\P".join(zeilen)


_LEGENDE_SYMBOL_H_MM = 300.0     # Ziel-Höhe des Mini-Symbols in der Stücklisten-Zeile
_LEGENDE_ZEILE_MM = 420.0        # Zeilenabstand der Symbol-Stückliste


def _draw_stueckliste(msp, raum: RaumModell, platzierung: PlatzierungsErgebnis) -> bool:
    """Stückliste-Box in der rechten Schriftfeld-Leiste (über dem Prüfbericht).

    Mit Typ-Lettern (Symbol-Datenmodell v1.2.0) in der Profi-Form der din-Legende
    (ACAD_TABLE „Legende Not-/Sicherheitsbeleuchtung": Stk. | SYMBOL | Typ |
    Beschreibung): je Typ-Zeile das echte Katalog-Symbol klein vorangestellt."""
    if platzierung.platzierungen and all(p.typ_letter for p in platzierung.platzierungen):
        from ezdxf import bbox as _ezbbox

        gruppen: dict[str, dict] = {}
        for p in platzierung.platzierungen:
            g = gruppen.setdefault(
                p.typ_letter,
                {"kind": p.kind, "produkt": p.typ_name or p.catalog_key,
                 "key": p.catalog_key, "n": 0},
            )
            g["n"] += 1
        (_min_x, min_y), (max_x, _max_y) = raum.bounds_mm.min_xy, raum.bounds_mm.max_xy
        x0 = max_x + _PANEL_ABSTAND_MM
        y0 = min_y + _BOX_Y_STUECK
        x1, y1 = x0 + _PANEL_B_MM, y0 + _BOX_H_STUECK_MM
        msp.add_lwpolyline([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], close=True,
                           dxfattribs={"layer": LAYER_STUECKLISTE})
        kopf = msp.add_mtext("STÜCKLISTE / LEGENDE", dxfattribs={
            "layer": LAYER_STUECKLISTE, "char_height": LEGENDE_HEIGHT_MM})
        kopf.set_location((x0 + _PANEL_PAD_MM, y1 - _PANEL_PAD_MM),
                          attachment_point=MTextEntityAlignment.TOP_LEFT)
        mapping = library.load_mapping()
        y = y1 - _PANEL_PAD_MM - _LEGENDE_ZEILE_MM * 1.2
        for letter in sorted(gruppen):
            g = gruppen[letter]
            eintrag = mapping.get(g["key"])
            sym_x = x0 + _PANEL_PAD_MM + 500.0
            if eintrag is not None:
                block_name = eintrag["block_name"]
                library.import_block(msp.doc, block_name)
                bb = _ezbbox.extents(msp.doc.blocks[block_name], fast=True)
                h_units = max(bb.size.y, 1e-6)
                s = _LEGENDE_SYMBOL_H_MM / h_units
                msp.add_blockref(block_name, (sym_x, y - _LEGENDE_ZEILE_MM / 2 + 60.0),
                                 dxfattribs={"xscale": s, "yscale": s,
                                             "layer": LAYER_NOTBELEUCHTUNG})
            zeile = msp.add_mtext(
                f"{g['n']}x | Typ {letter} | {_KIND_LABEL.get(g['kind'], g['kind'])} | {g['produkt']}",
                dxfattribs={"layer": LAYER_STUECKLISTE,
                            "char_height": LEGENDE_HEIGHT_MM * 0.8})
            zeile.set_location((sym_x + 800.0, y - _LEGENDE_ZEILE_MM / 2 + 60.0),
                               attachment_point=MTextEntityAlignment.MIDDLE_LEFT)
            y -= _LEGENDE_ZEILE_MM
        summe = msp.add_mtext(f"Summe: {len(platzierung.platzierungen)}", dxfattribs={
            "layer": LAYER_STUECKLISTE, "char_height": LEGENDE_HEIGHT_MM * 0.8})
        summe.set_location((x0 + _PANEL_PAD_MM, y - 60.0),
                           attachment_point=MTextEntityAlignment.TOP_LEFT)
        return True

    text = _stueckliste_text(platzierung)
    if text is None:
        return False
    _draw_info_box(msp, raum, _BOX_Y_STUECK, _BOX_H_STUECK_MM, LAYER_STUECKLISTE, text)
    return True


# Schriftfeld-Geometrie (mm): Plankopf = unterste Box der Schriftfeld-Leiste, an deren
# Spaltenbreite/Abstand ausgerichtet.
_PLANKOPF_B_MM = _PANEL_B_MM
_PLANKOPF_H_MM = _BOX_H_PLANKOPF_MM
_PLANKOPF_ABSTAND_MM = _PANEL_ABSTAND_MM
_PLANKOPF_PAD_MM = _PANEL_PAD_MM


def _draw_plankopf(msp, raum: RaumModell, platzierung: PlatzierungsErgebnis,
                   lb: LBVorgabe | None, meta: dict | None = None) -> bool:
    """Gerahmtes Schriftfeld (Plankopf) rechts unten neben dem Grundriss.

    Projekt/Geschoss/Norm/Anlage aus RaumModell + LB; `meta` (projekt/datum/ersteller/
    massstab) überschreibt/füllt die Kopf-Felder (z.B. aus API-Formularfeldern). Fehlt
    ein Wert, bleibt ein Leerfeld „__________" zum Ausfüllen (kein nichtdeterministisches
    Datum im Render).
    """
    meta = meta or {}
    (_min_x, min_y), (max_x, _max_y) = raum.bounds_mm.min_xy, raum.bounds_mm.max_xy
    x0 = max_x + _PLANKOPF_ABSTAND_MM
    y0 = min_y
    x1, y1 = x0 + _PLANKOPF_B_MM, y0 + _PLANKOPF_H_MM
    # Rahmen.
    msp.add_lwpolyline(
        [(x0, y0), (x1, y0), (x1, y1), (x0, y1)],
        close=True, dxfattribs={"layer": LAYER_PLANKOPF},
    )
    projekt = meta.get("projekt") or (lb.projekt if lb and lb.projekt else "—")
    norm = ", ".join(lb.norm_bezug) if (lb and lb.norm_bezug) else "EN 1838 / ÖVE E 8101"
    system = lb.system_typ if (lb and lb.system_typ) else "—"
    massstab = meta.get("massstab") or "1:100"
    datum = meta.get("datum") or "__________"
    ersteller = meta.get("ersteller") or "Engine (automatisch)"
    zeilen = [
        "NOTBELEUCHTUNGSPLAN",
        f"Projekt: {projekt}",
        f"Geschoss: {raum.floor}",
        f"Norm: {norm}",
        f"Anlage: {system}    Symbole: {len(platzierung.platzierungen)}",
        f"Maßstab: {massstab}    Datum: {datum}",
        f"Erstellt: {ersteller}    Geprüft: __________",
    ]
    mt = msp.add_mtext("\\P".join(zeilen), dxfattribs={
        "layer": LAYER_PLANKOPF,
        "char_height": LEGENDE_HEIGHT_MM * 0.85,
    })
    mt.set_location((x0 + _PLANKOPF_PAD_MM, y1 - _PLANKOPF_PAD_MM),
                    attachment_point=MTextEntityAlignment.TOP_LEFT)
    return True


def _draw_pruefbericht(msp, raum: RaumModell, pruefung: dict | None) -> bool:
    """Norm-Prüfbericht (Gesamtstatus + Befunde) rechts unten unter dem Plankopf."""
    if not pruefung:
        return False
    status = _PRUEF_STATUS_LABEL.get(pruefung.get("status", ""), "—")
    zeilen = [f"PRÜFBERICHT (EN 1838): {status}"]
    for b in pruefung.get("befunde", []):
        marke = _PRUEF_STATUS_LABEL.get(b.get("status", ""), "?")
        zeilen.append(f"[{marke}] {b.get('regel', '')} — {b.get('detail', '')}")
    _draw_info_box(msp, raum, _BOX_Y_PRUEF, _BOX_H_PRUEF_MM, LAYER_PRUEFBERICHT,
                   "\\P".join(zeilen), char_h=LEGENDE_HEIGHT_MM * 0.85)
    return True


def _draw_raeume(msp, raum: RaumModell) -> int:
    """Raum-Polygone als geschlossene LWPOLYLINE + raum_typ-Label am Zentroid."""
    drawn = 0
    for r in raum.raeume:
        if len(r.polygon_mm) < 3:
            continue
        msp.add_lwpolyline(
            list(r.polygon_mm),
            close=True,
            dxfattribs={"layer": LAYER_ARCH_RAUM},
        )
        cx = sum(p[0] for p in r.polygon_mm) / len(r.polygon_mm)
        cy = sum(p[1] for p in r.polygon_mm) / len(r.polygon_mm)
        mt = msp.add_mtext(
            f"{r.raum_typ} ({r.id})",
            dxfattribs={"layer": LAYER_ARCH_RAUM, "char_height": ROOM_LABEL_HEIGHT_MM},
        )
        mt.set_location((cx, cy), attachment_point=MTextEntityAlignment.MIDDLE_CENTER)
        drawn += 1
    return drawn


def _wand_richtung(raum: RaumModell, tuer) -> tuple[float, float]:
    """Einheits-Richtung der Wand, in der die Tür sitzt: nächstliegende Polygon-Kante
    des Anschluss-Raums (von_raum/nach_raum) durch den Türpunkt. Fallback horizontal."""
    tx, ty = tuer.xy_mm
    best, best_d = (1.0, 0.0), float("inf")
    kandidaten = [r for r in raum.raeume if r.id in (tuer.von_raum, tuer.nach_raum)]
    for r in kandidaten or raum.raeume:
        poly = r.polygon_mm
        for i in range(len(poly)):
            (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % len(poly)]
            ex, ey = x2 - x1, y2 - y1
            ln = (ex * ex + ey * ey) ** 0.5
            if ln < 1e-9:
                continue
            # Abstand Türpunkt → Kante (Projektion, geklemmt)
            t = max(0.0, min(1.0, ((tx - x1) * ex + (ty - y1) * ey) / (ln * ln)))
            px, py = x1 + t * ex, y1 + t * ey
            d = ((tx - px) ** 2 + (ty - py) ** 2) ** 0.5
            if d < best_d:
                best_d, best = d, (ex / ln, ey / ln)
    return best


def _draw_tueren(msp, raum: RaumModell) -> int:
    """Türen aus dem Contract zeichnen (Gap-Audit H-Gebäude: `raum.tueren` wurde vom
    Render ignoriert — der Plan wirkte türlos). Darstellung wie im Architektur-Bestand:
    Öffnungs-Schwelle in der Wand + Türblatt + Schwenk-Viertelbogen (`schwenk_richtung`).
    Notausgangs-Türen zusätzlich mit Doppel-Schwelle markiert."""
    import math as _math

    drawn = 0
    for t in raum.tueren:
        breite = t.breite_mm or 900.0
        wx, wy = _wand_richtung(raum, t)
        nx, ny = -wy, wx                       # Wand-Normale (Aufschlagseite)
        if t.schwenk_richtung == "links":
            nx, ny = -nx, -ny
        x0, y0 = t.xy_mm[0] - wx * breite / 2, t.xy_mm[1] - wy * breite / 2
        x1, y1 = t.xy_mm[0] + wx * breite / 2, t.xy_mm[1] + wy * breite / 2
        # Schwelle (Öffnung in der Wand)
        msp.add_line((x0, y0), (x1, y1), dxfattribs={"layer": LAYER_ARCH_TUER})
        if t.ist_notausgang:                   # Doppel-Schwelle = Notausgang
            off = 120.0
            msp.add_line((x0 + nx * off, y0 + ny * off), (x1 + nx * off, y1 + ny * off),
                         dxfattribs={"layer": LAYER_ARCH_TUER})
        # Türblatt (senkrecht zur Wand am Angelpunkt) + Schwenkbogen
        msp.add_line((x0, y0), (x0 + nx * breite, y0 + ny * breite),
                     dxfattribs={"layer": LAYER_ARCH_TUER})
        start = _math.degrees(_math.atan2(wy, wx))
        ende = _math.degrees(_math.atan2(ny, nx))
        msp.add_arc(center=(x0, y0), radius=breite, start_angle=min(start, ende),
                    end_angle=max(start, ende), dxfattribs={"layer": LAYER_ARCH_TUER})
        drawn += 1
    return drawn


def _draw_segmente(msp, raum: RaumModell) -> int:
    """Fluchtweg-Segmente als dünne Polylines (Review gegen die GU-PDF)."""
    drawn = 0
    for seg in raum.zirkulation.segmente:
        if len(seg.polyline_mm) < 2:
            continue
        msp.add_lwpolyline(
            list(seg.polyline_mm),
            dxfattribs={"layer": LAYER_FLUCHTWEG},
        )
        drawn += 1
    return drawn



def _nodeids(platzierung: PlatzierungsErgebnis) -> list[str]:
    """NODEID je Platzierung in Reihenfolge — bevorzugt das Contract-Feld
    `luminaire_id` (Symbol-Datenmodell v1.2.0, vom Platzierer vergeben); fehlt es,
    wird wie bisher synthetisiert (RZ-001/SL-002/AP-003, je Art gezählt).

    Quelle der Leuchten-IDs für die Symbol-Annotation (`_draw_nodeid_labels`).
    """
    counters: dict[str, int] = {}
    ids: list[str] = []
    for p in platzierung.platzierungen:
        code = _KIND_CODE.get(p.kind, "XX")
        counters[code] = counters.get(code, 0) + 1
        ids.append(p.luminaire_id or f"{code}-{counters[code]:03d}")
    return ids


_ANLAGE_RE = re.compile(r"AGV-([A-Z])-")


def _stromkreisnummern(platzierung: PlatzierungsErgebnis) -> list[str]:
    """Stromkreisnummer je Platzierung im Profi-Format Anlage/Kreis/Adresse
    (LABELING1 im din-DWG, STROMKREISNUMMER_DWG.md Empfehlung #1).

    Deterministisch aus `circuit_hint` abgeleitet, kein Contract-Feld:
    Anlage = Gebäude-Letter des Hints (A=1, B=2, …; ohne Match 1), Kreis =
    distinct Hints je Anlage in Erst-Auftretens-Reihenfolge (deckt alte
    `AGV-A-F13`- und neue `AGV-A-F13-DL-1`-Hints ohne Suffix-Parsing ab),
    Adresse = fortlaufend im Hint. Ohne Hint → "" (kein Label).
    """
    kreis_je_anlage: dict[int, dict[str, int]] = {}
    adresse: dict[str, int] = {}
    nummern: list[str] = []
    for p in platzierung.platzierungen:
        hint = (p.circuit_hint or "").strip()
        if not hint:
            nummern.append("")
            continue
        m = _ANLAGE_RE.match(hint)
        anlage = (ord(m.group(1)) - ord("A") + 1) if m else 1
        kreise = kreis_je_anlage.setdefault(anlage, {})
        if hint not in kreise:
            kreise[hint] = len(kreise) + 1
        adresse[hint] = adresse.get(hint, 0) + 1
        nummern.append(f"{anlage}/{kreise[hint]}/{adresse[hint]}")
    return nummern


def _draw_nodeid_labels(msp, platzierung: PlatzierungsErgebnis) -> tuple[int, int]:
    """Leuchten-ID (NODEID) als kleiner Text neben das Symbol — Wartung/Adressierung
    (Profi-Plan din_SIBEL_63_luminaire_ID). ID aus `_nodeids` (Contract-Feld
    `luminaire_id` v1.2.0 mit Render-Synthese als Fallback). Zweite Zeile =
    Stromkreisnummer Anlage/Kreis/Adresse (Profi-Plan LABELING1), sofern ein Kreis
    zugeordnet ist. Liefert (Labels gesamt, davon mit Stromkreisnummern-Zeile)."""
    drawn = 0
    mit_kreis = 0
    sknrn = _stromkreisnummern(platzierung)
    alle_xy = [q.xy_mm for q in platzierung.platzierungen]

    def _frei(x: float, y: float, selbst) -> bool:
        # Label darf in KEIN anderes Symbol ragen (Owner-Feedback: Beschriftung war
        # teils von Nachbar-Symbolen verdeckt). Sperrzone = Symbol-Halbbreite + halbe
        # Textbreite.
        for q, qxy in zip(platzierung.platzierungen, alle_xy):
            if q is selbst:
                continue
            sperr = _NODEID_HALBBREITE_MM.get(q.kind, 435.0) + 380.0
            if math.hypot(qxy[0] - x, qxy[1] - y) < sperr:
                return False
        return True

    for p, nodeid, sknr in zip(platzierung.platzierungen, _nodeids(platzierung), sknrn):
        angle = math.radians(p.rotation_deg or 0.0)
        offset = _NODEID_HALBBREITE_MM.get(p.kind, 435.0) + NODEID_CLEARANCE_MM
        # Seiten-/Distanz-Ausweich: +Tangente → −Tangente → +Normale → weiter raus.
        kandidaten = [
            (math.cos(angle) * offset, math.sin(angle) * offset),
            (-math.cos(angle) * offset, -math.sin(angle) * offset),
            (-math.sin(angle) * offset, math.cos(angle) * offset),
            (math.cos(angle) * offset * 2.2, math.sin(angle) * offset * 2.2),
        ]
        tx, ty = p.xy_mm[0] + kandidaten[0][0], p.xy_mm[1] + kandidaten[0][1]
        for dx, dy in kandidaten:
            kx, ky = p.xy_mm[0] + dx, p.xy_mm[1] + dy
            if _frei(kx, ky, p):
                tx, ty = kx, ky
                break
        text = f"{nodeid}\\P{sknr}" if sknr else nodeid
        if sknr:
            mit_kreis += 1
        mt = msp.add_mtext(text, dxfattribs={
            "layer": LAYER_NODEID,
            "char_height": NODEID_HEIGHT_MM,
        })
        mt.set_location((tx, ty), attachment_point=MTextEntityAlignment.MIDDLE_CENTER)
        drawn += 1
    return drawn, mit_kreis


def _stromkreis_belegung_text(platzierung: PlatzierungsErgebnis) -> str | None:
    """Stromkreis-Belegungsübersicht (Profi-Vorlage 1.xlsx §3b): je Endstromkreis die
    Anzahl je Leuchtenart mit Schaltungsart (DL/BL) und Gesamtzahl. Kompakt — die genaue
    ID↔Kreis-Zuordnung trägt der Plan selbst (NODEID-Annotation + Kreis-Label je Symbol),
    darum hier eine Zeile je Kreis statt einer Voll-ID-Liste (die auf realen Plänen mit
    Dutzenden Leuchten die Info-Box sprengt). Gruppiert nach `circuit_hint`; Platzierungen
    ohne Kreis unter „(ohne Kreis)". None wenn leer.
    """
    if not platzierung.platzierungen:
        return None
    # circuit_hint → geordnete {(Art-Code, DL/BL): Anzahl}. Schaltungsart bevorzugt aus
    # dem Contract-Feld (v1.2.0); fehlt es, greift die bisherige kind-Heuristik.
    kreise: dict[str, dict[tuple[str, str], int]] = {}
    reihenfolge: list[str] = []
    for p in platzierung.platzierungen:
        kreis = (p.circuit_hint or "").strip() or "(ohne Kreis)"
        if kreis not in kreise:
            kreise[kreis] = {}
            reihenfolge.append(kreis)
        eintrag = (_KIND_CODE.get(p.kind, "XX"), p.schaltungsart or _SCHALTUNGSART.get(p.kind, "—"))
        kreise[kreis][eintrag] = kreise[kreis].get(eintrag, 0) + 1
    zeilen = ["STROMKREIS-BELEGUNG"]
    for kreis in reihenfolge:
        arten = kreise[kreis]
        teile = [f"{n}× {code} ({art})" for (code, art), n in arten.items()]
        zeilen.append(f"{kreis}: {' · '.join(teile)} — Σ{sum(arten.values())}")
    return "\\P".join(zeilen)


_ANLAGEN_RAUM_TYPEN = {"TECHNIK", "TECHNIKRAUM", "HAUSTECHNIK", "ELEKTRO", "BATTERIERAUM"}


def _draw_anlage(msp, raum: RaumModell, lb: LBVorgabe | None) -> bool:
    """SV-Anlagen-Symbol (Gruppenbatterie, din STANDARD_SYSTEM-Pendant).

    LB-explizit (CLAUDE.md-Hierarchie): gezeichnet NUR, wenn die LB einen
    `system_typ` deklariert (z.B. mo-Elektro-LB §2.3 „Gruppenbatterie").
    Standort: Zentrum des Technik-/Batterieraums, falls die Raumerkennung einen
    liefert; sonst kein Symbol (kein geratener Standort). Kein Contract — die
    Anlage ist keine Leuchten-Platzierung, sie wird render-seitig gesetzt."""
    if lb is None or not lb.system_typ:
        return False
    kandidaten = [
        r for r in raum.raeume
        if r.raum_typ.upper() in _ANLAGEN_RAUM_TYPEN and len(r.polygon_mm) >= 3
    ]
    if not kandidaten:
        return False
    r = kandidaten[0]
    cx = sum(p[0] for p in r.polygon_mm) / len(r.polygon_mm)
    cy = sum(p[1] for p in r.polygon_mm) / len(r.polygon_mm)
    eintrag = library.load_mapping().get("gruppenbatterie_anlage")
    if eintrag is None:
        return False
    library.import_block(msp.doc, eintrag["block_name"])
    msp.add_blockref(eintrag["block_name"], (cx, cy), dxfattribs={
        "xscale": inserter.DE_GLOBAL_SCALE, "yscale": inserter.DE_GLOBAL_SCALE,
        "layer": LAYER_BELEGUNG,
    })
    _SYS = {"einzelbatterie": "Einzelbatterie", "gruppenbatterie": "Gruppenbatterie",
            "zentralbatterie": "Zentralbatterie"}
    text = f"SV-Anlage 1 — {_SYS.get(lb.system_typ, lb.system_typ)}"
    if lb.batterie_standort:
        text += f"\\P{lb.batterie_standort}"
    mt = msp.add_mtext(text, dxfattribs={"layer": LAYER_BELEGUNG,
                                         "char_height": ROOM_LABEL_HEIGHT_MM})
    mt.set_location((cx, cy - 700.0), attachment_point=MTextEntityAlignment.TOP_CENTER)
    return True


def _draw_stromkreis_belegung(msp, raum: RaumModell, platzierung: PlatzierungsErgebnis) -> bool:
    """Stromkreis-Belegungs-Box oben in der rechten Schriftfeld-Leiste."""
    text = _stromkreis_belegung_text(platzierung)
    if text is None:
        return False
    _draw_info_box(msp, raum, _BOX_Y_BELEGUNG, _BOX_H_BELEGUNG_MM, LAYER_BELEGUNG,
                   text, char_h=LEGENDE_HEIGHT_MM * 0.85)
    return True


def _set_vport(doc, raum: RaumModell, platzierung: PlatzierungsErgebnis) -> None:
    """Initial-Ansicht = Grundriss: Modelspace-VPORT auf Bounds ∪ Symbolpunkte,
    sonst öffnet AutoCAD bei (0,0) und der Plan muss per Zoom-Extents gesucht
    werden. Höhe mit Rand, Breite über konservatives Seitenverhältnis (1.5)."""
    xs = [p.xy_mm[0] for p in platzierung.platzierungen]
    ys = [p.xy_mm[1] for p in platzierung.platzierungen]
    xs += [raum.bounds_mm.min_xy[0], raum.bounds_mm.max_xy[0]]
    ys += [raum.bounds_mm.min_xy[1], raum.bounds_mm.max_xy[1]]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    height = max(y1 - y0, (x1 - x0) / 1.5, 1000.0) * 1.1
    doc.set_modelspace_vport(height, center=((x0 + x1) / 2.0, (y0 + y1) / 2.0))


def render_dxf(
    platzierung: PlatzierungsErgebnis,
    raum: RaumModell,
    out_path: Path | str,
    lb: LBVorgabe | None = None,
    pruefung: dict | None = None,
    plankopf: dict | None = None,
) -> dict:
    """Notbeleuchtungs-DXF schreiben; Summary-Superset des Pipeline-Stubs.

    `lb` (2. Input) → SV-Anlagen-Legende. `pruefung` (Prüfbericht-Dict aus
    validierung.pruefbericht) → Prüfbericht-Legende. `plankopf` (dict: projekt/datum/
    ersteller/massstab) → füllt die Schriftfeld-Kopf-Felder.
    """
    out_path = Path(out_path)
    doc = ezdxf.new("R2018", units=4)  # 4 = mm
    library.sync_layers(doc)
    _add_own_layers(doc)
    msp = doc.modelspace()

    n_raeume_drawn = _draw_raeume(msp, raum)
    n_tueren_drawn = _draw_tueren(msp, raum)
    n_segmente = _draw_segmente(msp, raum)
    lb_legende_drawn = _draw_lb_legende(msp, raum, lb)
    stueckliste_drawn = _draw_stueckliste(msp, raum, platzierung)
    plankopf_drawn = _draw_plankopf(msp, raum, platzierung, lb, plankopf)
    pruefbericht_drawn = _draw_pruefbericht(msp, raum, pruefung)
    belegung_drawn = _draw_stromkreis_belegung(msp, raum, platzierung)
    anlage_drawn = _draw_anlage(msp, raum, lb)

    by_kind: dict[str, int] = {}
    for p in platzierung.platzierungen:
        inserter.insert_platzierung(doc, p)
        by_kind[p.kind] = by_kind.get(p.kind, 0) + 1

    nodeids_drawn, stromkreisnummern_drawn = _draw_nodeid_labels(msp, platzierung)

    _set_vport(doc, raum, platzierung)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    doc.saveas(str(out_path))

    return {
        "floor": platzierung.floor,
        "n_symbols": len(platzierung.platzierungen),
        "by_kind": by_kind,
        "n_raeume": len(raum.raeume),
        "rendered": True,
        "output_path": str(out_path),
        "schrack_inserted": len(platzierung.platzierungen),
        "nodeids_drawn": nodeids_drawn,
        "stromkreisnummern_drawn": stromkreisnummern_drawn,
        "raum_konturen_drawn": n_raeume_drawn,
        "tueren_drawn": n_tueren_drawn,
        "fluchtweg_segmente_drawn": n_segmente,
        "lb_legende_drawn": lb_legende_drawn,
        "stueckliste_drawn": stueckliste_drawn,
        "plankopf_drawn": plankopf_drawn,
        "pruefbericht_drawn": pruefbericht_drawn,
        "stromkreis_belegung_drawn": belegung_drawn,
        "anlage_drawn": anlage_drawn,
        "layer": LAYER_NOTBELEUCHTUNG,
    }
