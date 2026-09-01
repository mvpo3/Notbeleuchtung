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
LAYER_STROMKREIS = "din_SIBEL_61_labeling"
LAYER_ARCH_RAUM = "ARCH_Raum"
LAYER_FLUCHTWEG = "ARCH_Fluchtweg"
LAYER_LEGENDE = "din_SIBEL_70_legend_white"
LAYER_STUECKLISTE = "din_SIBEL_70_legend_green"
LAYER_PLANKOPF = "din_SIBEL_99_titleblock"
LAYER_PRUEFBERICHT = "din_SIBEL_99_inspection"
LAYER_HOEHENKOTE = "din_SIBEL_52_info"

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
# y-Unterkanten relativ zu min_y (bottom-up):
_BOX_Y_PLANKOPF = 0.0
_BOX_Y_PRUEF = _BOX_H_PLANKOPF_MM + _PANEL_GAP_MM
_BOX_Y_STUECK = _BOX_Y_PRUEF + _BOX_H_PRUEF_MM + _PANEL_GAP_MM
_BOX_Y_LEGENDE = _BOX_Y_STUECK + _BOX_H_STUECK_MM + _PANEL_GAP_MM


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

# Stromkreis-Label — Konstanten verbatim aus elektro-planer dxf_writer.py:
# Offset folgt der Symbol-Normale (freie Raumseite), Text bleibt horizontal;
# Anti-Kollision: x-Band + Mindest-Vertikalabstand, bei Kollision weiter
# entlang der Normale hinausschieben (Korrektur-DXF TOP 24: median 235 mm).
CIRCUIT_LABEL_HEIGHT_MM = 90.0
CIRCUIT_LABEL_OFFSET_NORMAL_MM = 240.0
CIRCUIT_LABEL_BAND_X_MM = 300.0
CIRCUIT_LABEL_MIN_GAP_MM = 150.0
CIRCUIT_LABEL_MAX_NUDGE = 8

# Montagehöhen-Kote — sitzt entgegen der Stromkreis-Label-Seite (−Normale),
# damit Kote und Kreis-Label nicht überlappen. 150 mm (≈1,5 mm auf 1:100) statt 80 mm
# (0,8 mm — am Plan-Maßstab unleserlich), auf Höhe der Stromkreis-Label-Skala.
HOEHENKOTE_HEIGHT_MM = 150.0
HOEHENKOTE_OFFSET_NORMAL_MM = 240.0


def _add_own_layers(doc) -> None:
    doc.layers.add(LAYER_STROMKREIS, color=4)   # cyan
    doc.layers.add(LAYER_ARCH_RAUM, color=8)    # dunkelgrau
    doc.layers.add(LAYER_FLUCHTWEG, color=9)    # hellgrau
    doc.layers.add(LAYER_LEGENDE, color=7)      # weiß/schwarz
    doc.layers.add(LAYER_STUECKLISTE, color=7)  # weiß/schwarz
    doc.layers.add(LAYER_PLANKOPF, color=7)     # weiß/schwarz
    doc.layers.add(LAYER_PRUEFBERICHT, color=7)  # weiß/schwarz
    doc.layers.add(LAYER_HOEHENKOTE, color=3)    # grün


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
    """Stückliste der platzierten Symbol-Arten (Art + Anzahl). None wenn leer."""
    counts: dict[str, int] = {}
    for p in platzierung.platzierungen:
        counts[p.kind] = counts.get(p.kind, 0) + 1
    if not counts:
        return None
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


def _draw_stueckliste(msp, raum: RaumModell, platzierung: PlatzierungsErgebnis) -> bool:
    """Stückliste-Box in der rechten Schriftfeld-Leiste (über dem Prüfbericht)."""
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


def _draw_circuit_label(
    msp,
    x: float,
    y: float,
    circuit_hint: str,
    rotation_deg: float,
    placed: list[tuple[float, float]],
) -> bool:
    """Stromkreis-Label als MTEXT entlang der Symbol-Normale, anti-kollidierend."""
    text = (circuit_hint or "").strip()
    if not text:
        return False
    angle = math.radians(rotation_deg or 0.0)
    nx = -math.sin(angle)
    ny = math.cos(angle)
    tx = x + nx * CIRCUIT_LABEL_OFFSET_NORMAL_MM
    ty = y + ny * CIRCUIT_LABEL_OFFSET_NORMAL_MM
    guard = 0
    while guard < CIRCUIT_LABEL_MAX_NUDGE and any(
        abs(tx - px) < CIRCUIT_LABEL_BAND_X_MM
        and abs(ty - py) < CIRCUIT_LABEL_MIN_GAP_MM
        for (px, py) in placed
    ):
        tx += nx * CIRCUIT_LABEL_MIN_GAP_MM
        ty += ny * CIRCUIT_LABEL_MIN_GAP_MM
        guard += 1
    placed.append((tx, ty))
    # Attachment so, dass der Text vom Symbol WEG wächst.
    if abs(nx) >= abs(ny):
        attach = (MTextEntityAlignment.MIDDLE_LEFT if nx > 0
                  else MTextEntityAlignment.MIDDLE_RIGHT)
    else:
        attach = (MTextEntityAlignment.BOTTOM_CENTER if ny > 0
                  else MTextEntityAlignment.TOP_CENTER)
    mt = msp.add_mtext(text, dxfattribs={
        "layer": LAYER_STROMKREIS,
        "char_height": CIRCUIT_LABEL_HEIGHT_MM,
    })
    mt.set_location((tx, ty), attachment_point=attach)
    return True


def _hoehenkote_text(height_mm: float) -> str:
    """Montagehöhe als Kote in Metern, österreichische Komma-Notation (h=2,40)."""
    return f"h={height_mm / 1000.0:.2f}".replace(".", ",")


def _draw_hoehenkoten(msp, platzierung: PlatzierungsErgebnis) -> int:
    """Montagehöhen-Kote (h=2,40) je Symbol. Sitzt entgegen der Stromkreis-Label-
    Seite (−Normale), damit Kote und Kreis-Label nicht überlappen. EN 1838 §4.1:
    height_mm liegt im Contract, war bisher nur unsichtbar."""
    drawn = 0
    for p in platzierung.platzierungen:
        angle = math.radians(p.rotation_deg or 0.0)
        nx = -math.sin(angle)
        ny = math.cos(angle)
        tx = p.xy_mm[0] - nx * HOEHENKOTE_OFFSET_NORMAL_MM
        ty = p.xy_mm[1] - ny * HOEHENKOTE_OFFSET_NORMAL_MM
        mt = msp.add_mtext(_hoehenkote_text(p.height_mm), dxfattribs={
            "layer": LAYER_HOEHENKOTE,
            "char_height": HOEHENKOTE_HEIGHT_MM,
        })
        mt.set_location((tx, ty), attachment_point=MTextEntityAlignment.MIDDLE_CENTER)
        drawn += 1
    return drawn


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
    n_segmente = _draw_segmente(msp, raum)
    lb_legende_drawn = _draw_lb_legende(msp, raum, lb)
    stueckliste_drawn = _draw_stueckliste(msp, raum, platzierung)
    plankopf_drawn = _draw_plankopf(msp, raum, platzierung, lb, plankopf)
    pruefbericht_drawn = _draw_pruefbericht(msp, raum, pruefung)

    by_kind: dict[str, int] = {}
    placed_labels: list[tuple[float, float]] = []
    circuit_labels = 0
    for p in platzierung.platzierungen:
        inserter.insert_platzierung(doc, p)
        by_kind[p.kind] = by_kind.get(p.kind, 0) + 1
        if _draw_circuit_label(
            msp, p.xy_mm[0], p.xy_mm[1], p.circuit_hint, p.rotation_deg, placed_labels
        ):
            circuit_labels += 1

    hoehenkoten_drawn = _draw_hoehenkoten(msp, platzierung)

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
        "circuit_labels_drawn": circuit_labels,
        "hoehenkoten_drawn": hoehenkoten_drawn,
        "raum_konturen_drawn": n_raeume_drawn,
        "fluchtweg_segmente_drawn": n_segmente,
        "lb_legende_drawn": lb_legende_drawn,
        "stueckliste_drawn": stueckliste_drawn,
        "plankopf_drawn": plankopf_drawn,
        "pruefbericht_drawn": pruefbericht_drawn,
        "layer": LAYER_NOTBELEUCHTUNG,
    }
