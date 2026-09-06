"""plan_pruefen — Prüfstrecke: DXF → Render + Raum-/Rest-Bilder + JSON + Bericht.

Aufruf: python scripts/plan_pruefen.py [einzelne.dxf]
Ohne Argument: alle DXF in Projekte/_eingang/. Ausgabe je Plan nach
Projekte/_ergebnis/<planname>/ (01_render.png, 02_raeume.png, 03_rest.png,
raeume.json, bericht.md). Jeder Lauf wird an Projekte/_ergebnis/VERLAUF.md
angehängt. Liegt <planname>.referenz.json neben der DXF, wird IoU je Raum
berechnet.

Grenze: Rotation nur bei klar dominanter 90°-Kantenrichtung (Bild-rot90);
schräg dominante Richtungen bleiben bei 0° und werden im Bericht vermerkt.
"""
from __future__ import annotations

import itertools
import json
import math
import os.path
import re
import subprocess
import sys
import time
from collections import Counter
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))
sys.stdout.reconfigure(encoding="utf-8")

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from ezdxf.addons.drawing import Frontend, RenderContext
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
from ezdxf.addons.drawing.properties import LayoutProperties

from notbeleuchtung.raumerkennung.dxf_load import WALL_PATTERN, DxfPlan, lade_dxf
from notbeleuchtung.raumerkennung.kaskade import iou, raeume_aus_kaskade
from notbeleuchtung.raumerkennung.material_matching import (
    _LAYER_HINWEISE,
    bestimme_material,
    signatur_aus_hatch,
    signatur_zu_dict,
)
from notbeleuchtung.raumerkennung.stempel_anker import (
    Zuordnung,
    finde_stempel,
    restflaechen,
    zentrum,
)

EINGANG = REPO / "Projekte" / "_eingang"
ERGEBNIS = REPO / "Projekte" / "_ergebnis"

_FARBEN = plt.cm.tab20.colors  # type: ignore[attr-defined]


def _git_hash() -> str:
    try:
        r = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=REPO,
                           capture_output=True, text=True, timeout=10, check=False)
        return r.stdout.strip() or "n/a"
    except Exception:  # noqa: BLE001 — kein git = kein Hash, Lauf geht weiter
        return "n/a"


# ---------------------------------------------------------------- Rendern

def _dominanter_winkel(plan: DxfPlan) -> tuple[float, float]:
    """(Winkel° in [0,180), Gewichtsanteil) der längen-gewichteten Kantenrichtung."""
    bins: Counter[int] = Counter()
    total = 0.0
    for e in plan.wall_entities():
        pts = plan.entity_points(e)
        for (x1, y1), (x2, y2) in itertools.pairwise(pts):
            l = math.hypot(x2 - x1, y2 - y1)
            if l < 1.0:
                continue
            a = math.degrees(math.atan2(y2 - y1, x2 - x1)) % 180.0
            bins[round(a)] += int(l)
            total += l
    if not bins or total <= 0:
        return 0.0, 0.0
    winkel, gewicht = bins.most_common(1)[0]
    return float(winkel % 180), gewicht / total


def _texte_horizontal(plan: DxfPlan) -> bool:
    """True, wenn die Plan-Texte mehrheitlich horizontal stehen (Plan schon
    richtig orientiert — Beschriftung schlägt Wand-Richtung)."""
    h = v = 0
    for e in plan.space:
        if e.dxftype() in ("TEXT", "MTEXT"):
            r = float(getattr(e.dxf, "rotation", 0.0) or 0.0) % 180.0
            if min(r, 180.0 - r) <= 10.0:
                h += 1
            elif abs(r - 90.0) <= 10.0:
                v += 1
    return h >= v


def _rotation(plan: DxfPlan) -> tuple[int, str]:
    """(Bild-Rotation in 90°-Schritten, Vermerk). Nur klare Fälle rotieren."""
    winkel, anteil = _dominanter_winkel(plan)
    if anteil < 0.15:
        return 0, "Rotation: keine dominante Kantenrichtung — 0° belassen."
    if min(winkel, 180 - winkel) <= 3:
        return 0, "Rotation: dominante Richtung bereits horizontal (0°)."
    if abs(winkel - 90) <= 3:
        if _texte_horizontal(plan):
            return 0, ("Rotation: Wände vertikal-dominant, Beschriftung aber "
                       "horizontal — Plan gilt als richtig orientiert, 0° belassen.")
        return 1, "Rotation: dominante Richtung vertikal → um 90° gedreht."
    return 0, (f"Rotation: dominante Richtung {winkel:.0f}° (schräg) — "
               "unsicher, 0° belassen.")


def _figur(plan: DxfPlan, zoom=None) -> tuple[plt.Figure, plt.Axes]:
    """Weißer Grund, Plan via drawing-Addon, längste Seite ≈ 1200 px.

    ``zoom``: optionale (x0, x1, y0, y1)-Bounds in Plan-Koordinaten — für
    Modelspaces mit mehreren Planvarianten nebeneinander (Barawitzka)."""
    doc = plan.doc
    if "Standard" in doc.styles:  # SHX-'txt' hat Glyph-Lücken im mpl-Backend
        doc.styles.get("Standard").dxf.font = "DejaVuSans.ttf"
    fig = plt.figure(figsize=(12, 12), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_axis_off()
    lp = LayoutProperties.from_layout(doc.modelspace())
    lp.set_colors("#FFFFFF")
    Frontend(RenderContext(doc), MatplotlibBackend(ax)).draw_layout(
        plan.space, finalize=True, layout_properties=lp)
    ax.set_aspect("equal")
    x0, x1 = ax.get_xlim()
    y0, y1 = ax.get_ylim()
    if zoom is not None:
        zx0, zx1, zy0, zy1 = zoom
        # Nur zoomen, wenn die Variante deutlich kleiner als der Gesamt-Render ist.
        if (zx1 - zx0) < 0.7 * (x1 - x0) or (zy1 - zy0) < 0.7 * (y1 - y0):
            rand = 2000.0 / plan.factor  # 2 m Rand
            ax.set_xlim(zx0 - rand, zx1 + rand)
            ax.set_ylim(zy0 - rand, zy1 + rand)
            x0, x1 = ax.get_xlim()
            y0, y1 = ax.get_ylim()
    w, h = max(x1 - x0, 1e-9), max(y1 - y0, 1e-9)
    lang = 12.0
    fig.set_size_inches(lang if w >= h else lang * w / h,
                        lang if h > w else lang * h / w)
    return fig, ax


#: Layer-Schema einer Planvariante: '<Prefix>_<Nummer> <Bezeichnung>'.
_VARIANTE_RX = re.compile(r"^(.*_)\d+ ")


def _varianten_prefix(stempel) -> str | None:
    """Layer-Prefix der Variante mit den Stempeln, z.B. '0._EG PP_2_'.

    Barawitzka trägt dieselbe Etage dreimal im Modelspace ('0._EG PP_2_*' =
    echter Plan, '0._Erdgeschoß PP Icon_1_*'/'Icon_3_*' = Kopien daneben).
    Stempel-Layer '0._EG PP_2_810 Raum' → Prefix vor der Layer-Nummer."""
    layers = [s.layer for s in stempel if s.layer]
    if not layers:
        return None
    m = _VARIANTE_RX.match(os.path.commonprefix(layers))
    return m.group(1) if m and len(m.group(1)) >= 4 else None


def _ist_duplikat_variante(layer: str, prefix: str | None) -> bool:
    """True für Layer einer duplizierten Planvariante: gleiches Layer-Schema,
    aber anderer Varianten-Prefix als die Stempel-Variante."""
    if not prefix or layer.startswith(prefix):
        return False
    m = _VARIANTE_RX.match(layer)
    return bool(m and len(m.group(1)) >= 4)


def _varianten_bounds(plan: DxfPlan, prefix: str | None,
                      stempel) -> tuple[float, float, float, float] | None:
    """Bounds (Plan-Koordinaten) der Entities auf den Layern der Stempel-Variante."""
    if not stempel:
        return None
    # Basis: die Stempel-Positionen selbst (TEXT/MTEXT liefern keine entity_points).
    xs = [s.position_mm[0] / plan.factor for s in stempel]
    ys = [s.position_mm[1] / plan.factor for s in stempel]
    if prefix:
        for e in plan.space:
            if e.dxf.layer.startswith(prefix):
                for x, y in plan.entity_points(e):
                    xs.append(x / plan.factor)
                    ys.append(y / plan.factor)
    if not xs:
        return None
    return min(xs), max(xs), min(ys), max(ys)


def _ztop(ax: plt.Axes) -> float:
    """zorder ÜBER dem ezdxf-Render — das Backend vergibt zorder bis ~30000,
    Overlays mit kleinem zorder verschwinden unter weißen Füllflächen."""
    return max((c.get_zorder() for c in ax.get_children()), default=0.0) + 1.0


def _meterraster(ax: plt.Axes, plan: DxfPlan) -> None:
    """Dezente Gitterlinien alle 1 m (Plan-Koordinaten = Quell-Einheiten)."""
    schritt = 1000.0 / plan.factor
    x0, x1 = ax.get_xlim()
    y0, y1 = ax.get_ylim()
    while (x1 - x0) / schritt > 400:  # ponytail: bei Riesenplänen 10-m-Raster
        schritt *= 10
    for x in np.arange(math.floor(x0 / schritt) * schritt, x1, schritt):
        ax.axvline(x, color="#4488cc", alpha=0.18, lw=0.5, zorder=0)
    for y in np.arange(math.floor(y0 / schritt) * schritt, y1, schritt):
        ax.axhline(y, color="#4488cc", alpha=0.18, lw=0.5, zorder=0)


def _speichern(fig: plt.Figure, pfad: Path, rot90: int) -> None:
    fig.savefig(str(pfad), facecolor="white")
    plt.close(fig)
    if rot90:
        img = plt.imread(str(pfad))
        plt.imsave(str(pfad), np.rot90(img, rot90))


def _poly_zeichnen(ax: plt.Axes, punkte_mm, farbe, label: str, plan: DxfPlan,
                   ztop: float, labels_xy: list, ec=None) -> None:
    """Halbtransparente Füllung + optionales Label am Zentroid — über dem Render."""
    xs = [p[0] / plan.factor for p in punkte_mm]
    ys = [p[1] / plan.factor for p in punkte_mm]
    ax.fill(xs, ys, color=farbe, alpha=0.4, ec=ec or farbe, lw=1.5, zorder=ztop)
    if not label:
        return
    cx, cy = zentrum(list(punkte_mm))
    cx, cy = cx / plan.factor, cy / plan.factor
    x0, x1 = ax.get_xlim()
    y0, y1 = ax.get_ylim()
    span = max(x1 - x0, 1e-9)
    hoehe = max(y1 - y0, 1e-9)
    # Mindestabstand zwischen Labels (2.5 % der Bildbreite) gegen Überlappung.
    d2 = (0.025 * span) ** 2
    if any((cx - lx) ** 2 + (cy - ly) ** 2 < d2 for lx, ly in labels_xy):
        return
    labels_xy.append((cx, cy))
    span_m = span * plan.factor / 1000.0
    fs = max(5.0, min(9.0, 700.0 / max(span_m, 1.0)))  # dynamisch: große Pläne → klein
    # Label ÜBER die Polygon-Oberkante (sonst deckt die Textbox kleine Polygone
    # komplett zu) und in den Bildausschnitt geklemmt (sonst schneiden Labels
    # am Rand ab). Textmaß grob aus Zeichenzahl × Schriftgröße geschätzt.
    zeilen = label.splitlines() or [""]
    px_x = max(ax.figure.get_size_inches()[0] * ax.figure.dpi, 1.0)
    px_y = max(ax.figure.get_size_inches()[1] * ax.figure.dpi, 1.0)
    halb = min((0.5 * max(len(z) for z in zeilen) * fs * 0.72 + 4) / px_x * span,
               0.5 * span)
    hoch = (len(zeilen) * fs * 1.5 + 4) / px_y * hoehe
    tx = min(max(cx, x0 + halb), x1 - halb)
    ty = min(max(max(ys) + 0.01 * hoehe, y0), y1 - hoch)
    ax.text(tx, ty, label, ha="center", va="bottom",
            fontsize=fs, color="black", zorder=ztop + 1,
            bbox={"fc": "white", "alpha": 0.6, "ec": "none", "pad": 1})


# ---------------------------------------------------------------- Referenz/IoU

def referenz_vergleich(referenz: list[dict], raeume) -> list[tuple[str, float]]:
    """Je Referenz-Raum die beste IoU gegen die erkannten Polygone."""
    out = []
    for ref in referenz:
        best = max((iou(ref["polygon_mm"], r.polygon_mm) for r in raeume
                    if len(r.polygon_mm) >= 3), default=0.0)
        out.append((ref.get("name") or ref.get("id", "?"), best))
    return out


# ---------------------------------------------------------------- Material

#: Legendenfarben (RGB 0–255) fürs 04-Bild — 1:1 aus der Baulegende.
_MAT_FARBEN: dict[str, tuple[int, int, int]] = {
    "STAHLBETON": (134, 206, 152),
    "ZIEGELMAUERWERK": (255, 83, 83),
    "GIPSKARTON_EI0": (255, 213, 170),
    "GIPSKARTON": (255, 213, 170),      # Layer-Hinweis ohne EI-Klasse
    "GIPSKARTON_EI30": (255, 170, 240),
    "GIPSKARTON_EI90": (226, 199, 199),
    "YTONG": (255, 128, 128),
    "WAERMEDAEMMUNG": (255, 170, 205),
    "ALU_GLAS": (0, 232, 232),
}


def _shoelace(pts: list[tuple[float, float]]) -> float:
    return 0.5 * abs(sum(x1 * y2 - x2 * y1
                         for (x1, y1), (x2, y2) in zip(pts, pts[1:] + pts[:1])))


def _hatch_punkte(hatch) -> list[tuple[float, float]]:
    """Größter Boundary-Pfad des HATCH, flach (Quell-Einheiten).

    ponytail: nur der größte Pfad — Löcher/Inseln zählen bei Wandkörpern nicht.
    """
    import ezdxf.path
    best: list[tuple[float, float]] = []
    best_a = -1.0
    for p in ezdxf.path.from_hatch(hatch):
        pts = [(float(v.x), float(v.y)) for v in p.flattening(10)]
        a = _shoelace(pts) if len(pts) >= 3 else 0.0
        if a > best_a:
            best, best_a = pts, a
    return best


def _material_scan(plan: DxfPlan,
                   prefix: str | None = None) -> tuple[list[dict], list[list], list[list]]:
    """Alle HATCHes (MSP + Blockdefinitionen via INSERT-Transformation) matchen.

    ``prefix``: Varianten-Prefix der echten Plan-Variante; HATCHes auf den Layern
    duplizierter Varianten werden als 'Duplikat-Variante' nicht bewertet.

    Rückgabe: (wandkoerper-Dicts, Brandabschnitt-Linien, Fluchtweg-Linien) —
    Linienpunkte in Quell-Einheiten. '_pts' im Dict ist nur fürs Rendern.
    """
    koerper: list[dict] = []
    brand: list[list] = []
    flucht: list[list] = []

    def _linie_pruefen(e, quelle: str) -> None:
        if e.dxftype() not in ("LINE", "LWPOLYLINE", "POLYLINE"):
            return
        farbe = int(e.dxf.get("color", 256))
        ltyp = str(e.dxf.get("linetype", ""))
        pts = plan.entity_points(e)  # mm — für die Berichtsliste
        raw = [(x / plan.factor, y / plan.factor) for x, y in pts]
        if len(raw) < 2:
            return
        if farbe == 30 or ltyp.lower().startswith("brandabschnitt"):
            brand.append(raw)
        elif farbe == 96:
            flucht.append(raw)

    def _hatch_pruefen(h, quelle: str) -> None:
        sig = signatur_aus_hatch(h)
        layer = str(h.dxf.layer)
        pts = _hatch_punkte(h)
        if len(pts) < 3:
            return
        t = bestimme_material(sig, layer=layer)
        material, via_layer = t.material, False
        if material == "UNBEKANNT" and not sig.linien:
            # SOLID ohne Muster: Material steckt ggf. im Layer-Namen (Barawitzka).
            for rx, ziel in _LAYER_HINWEISE:
                if rx.search(layer):
                    material, via_layer = ziel, True
                    break
        # Bauteil-Abgrenzung: Muster-Hatches immer; SOLIDs nur mit Material-,
        # Layer-Hinweis- oder Wand-Layer-Beleg. Rest = Möbel/Plangrafik.
        bauteil = (bool(sig.linien) or material != "UNBEKANNT"
                   or layer in plan.wall_layers or bool(WALL_PATTERN.search(layer)))
        duplikat = _ist_duplikat_variante(layer, prefix)
        if duplikat:
            bauteil = False
        cx = sum(p[0] for p in pts) / len(pts)
        cy = sum(p[1] for p in pts) / len(pts)
        koerper.append({
            "material": material,
            "score": t.score if not via_layer else None,
            "via_layer": via_layer,
            "layer": layer,
            "pattern": sig.pattern_name,
            "flaeche_mm2": round(_shoelace(pts) * plan.factor ** 2, 1),
            "zentrum": [round(cx * plan.factor, 1), round(cy * plan.factor, 1)],
            "bauteil": bauteil,
            "duplikat_variante": duplikat,
            "quelle": quelle,
            "begruendung": t.begruendung,
            "_pts": pts,
            "_sig": sig,
        })

    def _walk(entities, quelle: str, tiefe: int = 0) -> None:
        for e in entities:
            t = e.dxftype()
            if t == "HATCH":
                _hatch_pruefen(e, quelle)
            elif t == "INSERT" and tiefe < 3:
                try:
                    _walk(e.virtual_entities(), f"block:{e.dxf.name}", tiefe + 1)
                except Exception:  # noqa: BLE001, S110 — kaputter Block killt den Scan nicht
                    pass
            else:
                _linie_pruefen(e, quelle)

    _walk(plan.space, "msp")
    return koerper, brand, flucht


def _bild_material(plan: DxfPlan, zoom, koerper: list[dict],
                   brand: list[list], flucht: list[list],
                   pfad: Path, rot: int) -> None:
    """04_material.png: Bauteil-Hatches in Legendenfarben + Markierungslinien."""
    fig, ax = _figur(plan, zoom)
    _meterraster(ax, plan)
    ztop = _ztop(ax)
    labels_xy: list = []
    x0, x1 = ax.get_xlim()
    d2 = (0.02 * max(x1 - x0, 1e-9)) ** 2
    for k in koerper:
        if not k["bauteil"]:
            continue
        xs = [p[0] for p in k["_pts"]]
        ys = [p[1] for p in k["_pts"]]
        mat = k["material"]
        if mat == "SCHACHT":
            ax.fill(xs, ys, fc="none", ec=(1.0, 0.0, 0.0), lw=1.5, zorder=ztop)
        elif mat == "UNBEKANNT":
            ax.fill(xs, ys, color="#999999", alpha=0.55, ec="#777777",
                    lw=0.5, zorder=ztop)
            cx, cy = (k["zentrum"][0] / plan.factor, k["zentrum"][1] / plan.factor)
            if not any((cx - lx) ** 2 + (cy - ly) ** 2 < d2 for lx, ly in labels_xy):
                labels_xy.append((cx, cy))
                ax.text(cx, cy, "?", ha="center", va="center", fontsize=8,
                        color="black", zorder=ztop + 2)
        else:
            rgb = _MAT_FARBEN.get(mat, (150, 150, 150))
            f = tuple(c / 255.0 for c in rgb)
            ax.fill(xs, ys, color=f, alpha=0.55, ec=f, lw=0.5, zorder=ztop)
    for pts in brand:
        ax.plot([p[0] for p in pts], [p[1] for p in pts],
                color=(1.0, 0.5, 0.0), lw=3.0, zorder=ztop + 1)
    for pts in flucht:
        ax.plot([p[0] for p in pts], [p[1] for p in pts],
                color=(0.0, 0.5, 0.0), lw=2.0, zorder=ztop + 1)
    _speichern(fig, pfad, rot)


def _kachel_fenster(k: dict, plan: DxfPlan) -> tuple[float, float, float]:
    """(cx, cy, Seitenlänge) des Weltausschnitts in Quell-Einheiten: 2 m um das
    Hatch-Zentrum, bei größeren Hatches die Hatch-BBox + 20 %."""
    xs = [p[0] for p in k["_pts"]]
    ys = [p[1] for p in k["_pts"]]
    seite = max(2000.0 / plan.factor,
                1.2 * max(max(xs) - min(xs), max(ys) - min(ys)))
    return k["zentrum"][0] / plan.factor, k["zentrum"][1] / plan.factor, seite


def _ueberlappt(a: tuple[float, float, float], b: tuple[float, float, float]) -> bool:
    """Überschneiden sich zwei quadratische Ausschnitte (cx, cy, Seite)?"""
    return (abs(a[0] - b[0]) < 0.5 * (a[2] + b[2])
            and abs(a[1] - b[1]) < 0.5 * (a[2] + b[2]))


def _unbekannt_kacheln(plan: DxfPlan, koerper: list[dict], ziel: Path) -> int:
    """Je unbekannter Signatur-Variante eine 200x200-px-Kachel + JSON.

    Dedupliziert nach Signatur (ohne Skala); Kachel = eigener Render des
    Weltausschnitts um das Hatch (2 m bzw. Hatch-BBox + 20 %), nicht ein
    200-px-Crop aus dem Voll-Render.
    """
    unbekannt = [k for k in koerper if k["bauteil"] and k["material"] == "UNBEKANNT"]
    gruppen: dict[str, list[dict]] = {}
    for k in unbekannt:
        key = json.dumps(signatur_zu_dict(k["_sig"]), sort_keys=True)
        gruppen.setdefault(key, []).append(k)
    ordner = ziel / "unbekannte_muster"
    if ordner.exists():
        for f in ordner.iterdir():
            f.unlink()
    if not gruppen:
        return 0
    ordner.mkdir(parents=True, exist_ok=True)
    # Einmal zeichnen, dann je Kachel nur Ausschnitt setzen und speichern —
    # das Aufbauen der Artists (ezdxf-Frontend) ist der teure Teil.
    fig, ax = _figur(plan, None)
    fig.set_size_inches(2, 2)
    belegt: list[tuple[float, float, float]] = []
    for n, (key, ks) in enumerate(sorted(gruppen.items()), start=1):
        kandidaten = sorted(ks, key=lambda k: -k["flaeche_mm2"])[:50]
        fenster = [_kachel_fenster(k, plan) for k in kandidaten]
        # Repräsentant, dessen Ausschnitt keinen schon vergebenen überlappt —
        # sonst wären zwei Kacheln bildgleich (gleiche Stelle, andere Signatur).
        i = next((j for j, f in enumerate(fenster)
                  if not any(_ueberlappt(f, b) for b in belegt)), 0)
        rep, (cx, cy, seite) = kandidaten[i], fenster[i]
        belegt.append(fenster[i])
        ax.set_xlim(cx - seite / 2, cx + seite / 2)
        ax.set_ylim(cy - seite / 2, cy + seite / 2)
        fig.savefig(str(ordner / f"muster_{n:02d}.png"), dpi=100, facecolor="white")
        (ordner / f"muster_{n:02d}.json").write_text(json.dumps({
            "signatur": signatur_zu_dict(rep["_sig"]),
            "layer": sorted({k["layer"] for k in ks}),
            "anzahl_hatches": len(ks),
            "flaeche_mm2_summe": round(sum(k["flaeche_mm2"] for k in ks), 1),
            "beispiel_zentrum_mm": rep["zentrum"],
            "ausschnitt_m": round(seite * plan.factor / 1000.0, 2),
            "bester_kandidat": rep["begruendung"],
        }, ensure_ascii=False, indent=2), encoding="utf-8")
    plt.close(fig)
    return len(gruppen)


def _material_md(koerper: list[dict], brand: list[list], flucht: list[list],
                 abdeckung: float | None, plan: DxfPlan) -> list[str]:
    """Markdown-Block: Materialtabelle + Markierungen + Legendenabdeckung."""
    bauteile = [k for k in koerper if k["bauteil"]]
    dupl = [k for k in koerper if k.get("duplikat_variante")]
    rest = [k for k in koerper if not k["bauteil"] and not k.get("duplikat_variante")]
    agg: dict[str, list[dict]] = {}
    for k in bauteile:
        agg.setdefault(k["material"], []).append(k)
    l = ["", "## Material (Bauteil-Hatches)", "",
         "| Material | Anzahl | Fläche m² | mittl. Score |", "|---|--:|--:|--:|"]
    for mat, ks in sorted(agg.items(), key=lambda x: -sum(k["flaeche_mm2"] for k in x[1])):
        scores = [k["score"] for k in ks if k["score"] is not None]
        s = f"{sum(scores) / len(scores):.2f}" if scores else "via Layer"
        l.append(f"| {mat} | {len(ks)} | "
                 f"{sum(k['flaeche_mm2'] for k in ks) / 1e6:.1f} | {s} |")
    if rest:
        l.append(f"| _nicht bewertet (Möbel/Plangrafik-SOLIDs)_ | {len(rest)} | "
                 f"{sum(k['flaeche_mm2'] for k in rest) / 1e6:.1f} | — |")
    if dupl:
        l.append(f"| _Duplikat-Variante, nicht bewertet_ | {len(dupl)} | "
                 f"{sum(k['flaeche_mm2'] for k in dupl) / 1e6:.1f} | — |")
    l += ["",
          ("Abgrenzung: Muster-Hatches zählen immer als Bauteil; SOLIDs nur mit "
           "Material-Treffer, Layer-Hinweis oder Wand-Layer — übrige SOLIDs "
           "(Möbel/Treppen/Plangrafik) sind „nicht bewertet“ und gehen NICHT in "
           "die Legendenabdeckung ein."), ""]
    if dupl:
        layer_pre = sorted({_VARIANTE_RX.match(k["layer"]).group(1) for k in dupl
                            if _VARIANTE_RX.match(k["layer"])})
        l += [("Duplikat-Varianten: Der Modelspace trägt dieselbe Etage mehrfach; "
               "nur die Variante mit den Raumstempeln wird bewertet und gerendert. "
               f"Hatches auf den Kopie-Layern ({', '.join(p + '*' for p in layer_pre)}) sind "
               "„Duplikat-Variante, nicht bewertet“ und gehen NICHT in "
               "Legendenabdeckung oder UNBEKANNT-Zahl ein."), ""]
    if abdeckung is not None:
        l.append(f"**Legendenabdeckung: {abdeckung * 100:.1f} %** "
                 "(bekannte Materialfläche / Bauteil-Schraffurfläche)")
    else:
        l.append("**Legendenabdeckung: — (keine Bauteil-Hatches)**")
    l += ["", "## Markierungen", "",
          f"- Brandabschnittslinien: {len(brand)}",
          f"- Fluchtweglinien: {len(flucht)}"]
    for titel, linien in (("Brandabschnitt", brand), ("Fluchtweg", flucht)):
        if linien:
            l += ["", f"### {titel}-Linien", ""]
            for pts in linien:
                (ax_, ay_), (bx_, by_) = pts[0], pts[-1]
                l.append(f"- ({ax_ * plan.factor / 1000:.2f}, {ay_ * plan.factor / 1000:.2f}) m "
                         f"→ ({bx_ * plan.factor / 1000:.2f}, {by_ * plan.factor / 1000:.2f}) m")
    return l


# ---------------------------------------------------------------- Hauptlauf

def _raum_kaskade(plan: DxfPlan, stempel) -> tuple[list[Zuordnung], list, list, dict, str]:
    """Raum-Kaskade L→H→F→R — Orchestrierung liegt in ``raumerkennung.kaskade``.

    Eine Quelle der Wahrheit: Prüfstrecke und ``ArchitekturRaumProvider.parse``
    rufen dieselbe ``raeume_aus_kaskade``.
    """
    e = raeume_aus_kaskade(plan, stempel)
    return e.zuordnungen, e.raeume, e.rest_raeume, e.quelle, e.kette


#: Raumtyp → (Füllfarbe, Konturfarbe) fürs 02-Bild.
def _typ_stil(typ: str | None, name: str | None = None) -> tuple[str, str]:
    # Namens-Fallback vor dem Typ-Mapping: 'Wohnküche' typt zu KÜCHE, 'Hobbyraum'
    # zu ZIMMER — beides grün; der Stempelname ist hier die feinere Quelle.
    n = (name or "").lower()
    if "wohn" in n or "hobby" in n:
        return "#7b68ee", "#7b68ee"                      # blau/lila
    t = (typ or "").upper()
    if "SCHACHT" in t:
        return "#ffffff", "#dd0000"                      # weiß, rote Kontur
    if "STIEG" in t or "TREPP" in t or "LIFT" in t:
        return "#ff9500", "#ff9500"                      # orange
    if "GANG" in t or "FLUR" in t or "VORRAUM" in t:
        return "#ffd400", "#c8a800"                      # gelb
    if t in ("BAD", "WC") or "NASS" in t or "WASCH" in t:
        return "#e04040", "#e04040"                      # rot
    if "HOBBY" in t or "WOHN" in t:
        return "#7b68ee", "#7b68ee"                      # blau/lila
    if t in ("ABSTELLRAUM", "LAGER", "KELLER", "TECHNIK", "MUELLRAUM", "GARAGE"):
        return "#909090", "#707070"                      # grau (AR & Co.)
    if t and t != "UNBEKANNT":
        return "#3cb043", "#3cb043"                      # Zimmer-Familie grün
    return "#d3d3d3", "#b0b0b0"                          # UNBEKANNT hellgrau


def _json_eintraege(zuordnungen: list[Zuordnung], rest, quelle: dict) -> list[dict]:
    out = []
    for n, z in enumerate(zuordnungen, start=1):
        st = z.stempel
        out.append({
            "id": z.raum.id if z.raum else f"stempel_{n}",
            "typ": st.typ,
            "name": st.name,
            "polygon_mm": [list(p) for p in (z.raum.polygon_mm if z.raum else [])],
            "flaeche_stempel": st.flaeche_m2,
            "flaeche_berechnet": z.raum.flaeche_m2 if z.raum else None,
            "abweichung_prozent": (round(z.abweichung_prozent, 2)
                                   if z.abweichung_prozent is not None else None),
            "flag": z.flag,
            "quelle": quelle.get(z.raum.id) if z.raum else None,
            "stempel_quelle": st.quelle,
        })
    for r in rest:
        out.append({
            "id": r.id, "typ": r.raum_typ or None, "name": None,
            "polygon_mm": [list(p) for p in r.polygon_mm],
            "flaeche_stempel": None, "flaeche_berechnet": r.flaeche_m2,
            "abweichung_prozent": None, "flag": "kein_stempel",
            "quelle": quelle.get(r.id),
            "stempel_quelle": None,
        })
    return out


def plan_pruefen(dxf: Path) -> dict:
    t0 = time.time()
    name = dxf.stem
    ziel = ERGEBNIS / name
    ziel.mkdir(parents=True, exist_ok=True)

    plan = lade_dxf(dxf)
    stempel = finde_stempel(plan)
    zuordnungen, raeume, rest_r, quelle, raum_quelle = _raum_kaskade(plan, stempel)
    rest = restflaechen(raeume, zuordnungen) + rest_r
    rot, rot_vermerk = _rotation(plan)

    prefix = _varianten_prefix(stempel)
    zoom = _varianten_bounds(plan, prefix, stempel)

    # 01: Plan wie geplottet + Meterraster.
    fig, ax = _figur(plan, zoom)
    _meterraster(ax, plan)
    _speichern(fig, ziel / "01_render.png", rot)

    # 02: ALLE Räume, Farbe nach TYP, Quelle-Kürzel (L/H/F/R) im Label.
    stempel_je_raum = {}
    for z in zuordnungen:
        if z.raum is not None and z.raum.id not in stempel_je_raum:
            stempel_je_raum[z.raum.id] = z
    fig, ax = _figur(plan, zoom)
    _meterraster(ax, plan)
    ztop, labels_xy = _ztop(ax), []
    for r in raeume + rest_r:
        if len(r.polygon_mm) < 3:
            continue
        q = quelle.get(r.id, "?")
        z = stempel_je_raum.get(r.id)
        fc, ec = _typ_stil(r.raum_typ, z.stempel.name if z else None)
        if r.flaeche_m2 < 4.0:
            lbl = ""
        elif z is not None:
            st = z.stempel
            lbl = f"[{q}] " + " ".join(st.name.splitlines())
            if st.flaeche_m2:
                lbl += f"\n{st.flaeche_m2:.1f} / {r.flaeche_m2:.1f} m²"
            else:
                lbl += f"\n{r.flaeche_m2:.1f} m²"
        else:
            lbl = f"[{q}] {r.raum_typ or '?'}\n{r.flaeche_m2:.1f} m²"
        _poly_zeichnen(ax, r.polygon_mm, fc, lbl, plan, ztop, labels_xy, ec=ec)
    _speichern(fig, ziel / "02_raeume.png", rot)

    # 03: Restflächen ohne Stempel.
    fig, ax = _figur(plan, zoom)
    _meterraster(ax, plan)
    ztop, labels_xy = _ztop(ax), []
    for n, r in enumerate(rest):
        if len(r.polygon_mm) < 3:
            continue
        _poly_zeichnen(ax, r.polygon_mm, _FARBEN[n % len(_FARBEN)],
                       f"{r.flaeche_m2:.1f} m²" if r.flaeche_m2 >= 4.0 else "", plan,
                       ztop, labels_xy)
    _speichern(fig, ziel / "03_rest.png", rot)

    # 04: Material-Analyse (MSP + Blockdefinitionen) + Markierungslinien.
    koerper, brand, flucht = _material_scan(plan, prefix)
    _bild_material(plan, zoom, koerper, brand, flucht, ziel / "04_material.png", rot)
    n_muster = _unbekannt_kacheln(plan, koerper, ziel)
    bauteile = [k for k in koerper if k["bauteil"]]
    flaeche_bauteil = sum(k["flaeche_mm2"] for k in bauteile)
    flaeche_bekannt = sum(k["flaeche_mm2"] for k in bauteile
                          if k["material"] != "UNBEKANNT")
    abdeckung = flaeche_bekannt / flaeche_bauteil if flaeche_bauteil > 0 else None

    eintraege = _json_eintraege(zuordnungen, rest, quelle)
    ids = [e["id"] for e in eintraege]
    doppelt = [i for i, n in Counter(ids).items() if n > 1]
    assert not doppelt, f"{name}: Mehrfach-Zuordnung auf {doppelt}"
    daten = {"raeume": eintraege,
             "wandkoerper": [{k: v for k, v in w.items() if not k.startswith("_")}
                             for w in koerper]}
    (ziel / "raeume.json").write_text(
        json.dumps(daten, ensure_ascii=False, indent=2), encoding="utf-8")

    # Referenz-IoU (optional).
    iou_zeilen, iou_mittel = [], None
    ref_datei = dxf.with_name(f"{name}.referenz.json")
    if ref_datei.exists():
        ref = json.loads(ref_datei.read_text(encoding="utf-8"))
        iou_zeilen = referenz_vergleich(ref, raeume)
        if iou_zeilen:
            iou_mittel = sum(v for _, v in iou_zeilen) / len(iou_zeilen)

    laufzeit = time.time() - t0
    material_block = _material_md(koerper, brand, flucht, abdeckung, plan)
    # Kennzahlen der Kaskade.
    gesamt = len(raeume) + len(rest_r)
    mit_stempel = len({z.raum.id for z in zuordnungen if z.raum is not None})
    flag_ok = sum(1 for z in zuordnungen if z.flag == "ok")
    rest_typ = sum(1 for r in rest_r if r.raum_typ != "UNBEKANNT")
    rest_untyp = len(rest_r) - rest_typ
    _bericht(ziel / "bericht.md", name, zuordnungen, rest, raum_quelle,
             rot_vermerk, iou_zeilen, iou_mittel, laufzeit, len(raeume),
             material_block, quelle)
    flags = sum(1 for z in zuordnungen if z.flag != "ok")
    # Zählung aus derselben Quelle wie raeume.json: Stempel-Einträge + Rest-Einträge.
    rest_n = sum(1 for e in eintraege if e["flag"] == "kein_stempel")
    return {"plan": name, "stempel": len(stempel),
            "raeume": len(eintraege) - rest_n,
            "rest": rest_n, "flags": flags, "iou_mittel": iou_mittel,
            "laufzeit": laufzeit,
            "abdeckung": abdeckung, "unbekannte_muster": n_muster,
            "brand_linien": len(brand), "flucht_linien": len(flucht),
            "material_md": material_block,
            "raeume_gesamt": gesamt, "mit_stempel": mit_stempel,
            "flag_ok": flag_ok, "rest_typisiert": rest_typ,
            "rest_untypisiert": rest_untyp,
            "quellen_mix": raum_quelle}


def _bericht(pfad: Path, name: str, zuordnungen: list[Zuordnung], rest,
             raum_quelle: str, rot_vermerk: str,
             iou_zeilen, iou_mittel, laufzeit: float, n_raeume: int = 0,
             material_block: list[str] | None = None,
             quelle: dict | None = None) -> None:
    quelle = quelle or {}
    l = [f"# Prüfbericht {name}", "",
         f"Raum-Polygon-Quelle: `{raum_quelle}` — {rot_vermerk}", ""]
    l += [
         "## Räume", "",
         "| Quelle | Name | Typ | m² Stempel | m² berechnet | Abw. % | Flag |",
         "|---|---|---|--:|--:|--:|---|"]
    for z in zuordnungen:
        st = z.stempel
        l.append("| {} | {} | {} | {} | {} | {} | {} |".format(
            quelle.get(z.raum.id, "—") if z.raum else "—",
            " / ".join(st.name.replace("|", "/").splitlines()), st.typ or "—",
            f"{st.flaeche_m2:.2f}" if st.flaeche_m2 is not None else "—",
            f"{z.raum.flaeche_m2:.2f}" if z.raum else "—",
            f"{z.abweichung_prozent:+.1f}" if z.abweichung_prozent is not None else "—",
            z.flag))
    for r in rest:
        l.append("| {} | {} | {} | — | {:.2f} | — | kein_stempel |".format(
            quelle.get(r.id, "—"), r.id, r.raum_typ or "—", r.flaeche_m2))
    l += ["", f"## Restflächen ohne Stempel ({len(rest)})", ""]
    for r in rest:
        cx, cy = zentrum(r)
        l.append(f"- {r.id} [{quelle.get(r.id, '?')}] {r.raum_typ or '—'}: "
                 f"{r.flaeche_m2:.2f} m², Zentrum ({cx / 1000:.2f}, {cy / 1000:.2f}) m")
    warn = [f"Stempel ohne Polygon: „{z.stempel.name}“"
            for z in zuordnungen if z.polygon_index is None]
    warn += [f"Polygon ohne Stempel: {r.id} ({r.flaeche_m2:.2f} m²)" for r in rest]
    warn += [f"Abweichung > 10 %: „{z.stempel.name}“ ({z.abweichung_prozent:+.1f} %)"
             for z in zuordnungen
             if z.abweichung_prozent is not None and abs(z.abweichung_prozent) > 10]
    l += ["", f"## Warnungen ({len(warn)})", ""]
    l += [f"- {w}" for w in warn] or ["- keine"]
    ausbruch = [z for z in zuordnungen
                if z.flag == "flutung_unsicher" and z.raum is not None
                and z.abweichung_prozent is not None and z.abweichung_prozent > 200]
    if ausbruch:
        l += ["", "## Bekannte Grenze: ausgebrochene Flutungen", "",
              ("Bei diesen Stempeln läuft die Flutung über eine offene Tür in "
              "Vorplatz/Korridor. Zwei Gegenversuche brachten keine Verbesserung "
              "ohne Regression und sind daher NICHT eingebaut: eine zusätzliche "
              "niedrigere Start-Versiegelungsstufe (300 bzw. 400 mm) senkte "
              "plan-weit die „ok“-Flutungen von 41 auf 38; eine Deckelung der "
              "Flutfläche auf 3× Stempelfläche trifft zwar genau diese Fälle, "
              "verletzt aber die Modul-Invariante „NIE verwerfen“ "
              "(`test_stempel_flutung.py::test_riesenbereich_unsicher`). Die "
               "Fälle bleiben darum als `flutung_unsicher` ehrlich geflaggt."), ""]
        l += [f"- „{' / '.join(z.stempel.name.splitlines())}“: "
              f"{z.stempel.flaeche_m2:.2f} m² Stempel → {z.raum.flaeche_m2:.2f} m² "
              f"geflutet ({z.abweichung_prozent:+.0f} %)" for z in ausbruch]
    if iou_zeilen:
        l += ["", "## Referenz-Vergleich (IoU)", "", "| Raum | IoU |", "|---|--:|"]
        l += [f"| {n} | {v:.3f} |" for n, v in iou_zeilen]
        l += ["", f"**Mittelwert: {iou_mittel:.3f}**"]
    l += material_block or []
    l += ["", f"Laufzeit: {laufzeit:.1f} s", ""]
    pfad.write_text("\n".join(l), encoding="utf-8")


def _verlauf_schreiben(ergebnisse: list[dict], commit: str) -> None:
    """Ein Block je Aufruf, idempotent: alte Zeilen mit gleichem (Commit, Plan)
    werden ersetzt statt dupliziert; leergeräumte Blöcke fallen weg."""
    verlauf = ERGEBNIS / "VERLAUF.md"
    alt = (verlauf.read_text(encoding="utf-8").splitlines()
           if verlauf.exists() else [])
    marker = {f"· {commit} · {r['plan']}:" for r in ergebnisse}
    zeilen = [z for z in alt
              if z.startswith("## Lauf")
              or (z.startswith("- ") and not any(m in z for m in marker))]
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")  # noqa: DTZ005 — lokale Log-Zeit reicht
    zeilen.append(f"## Lauf {stamp} · {commit}")
    for r in ergebnisse:
        iou_txt = f"{r['iou_mittel']:.3f}" if r["iou_mittel"] is not None else "—"
        abd = r.get("abdeckung")
        abd_txt = f", Legendenabdeckung {abd * 100:.1f} %" if abd is not None else ""
        zeilen.append(
            f"- {stamp[:10]} · {commit} · {r['plan']}: {r['stempel']} Stempel, "
            f"{r['raeume']} Räume, {r['rest']} Restflächen, IoU-Mittel {iou_txt}"
            f"{abd_txt} · Räume gesamt {r.get('raeume_gesamt', 0)}, "
            f"mit Stempel {r.get('mit_stempel', 0)}, Flag ok {r.get('flag_ok', 0)}, "
            f"Rest typisiert {r.get('rest_typisiert', 0)} / "
            f"untypisiert {r.get('rest_untypisiert', 0)} "
            f"({r.get('quellen_mix', '')})")
    out = ["# Verlauf plan_pruefen"]
    for i, z in enumerate(zeilen):
        if z.startswith("## Lauf") and (i + 1 >= len(zeilen)
                                        or zeilen[i + 1].startswith("## Lauf")):
            continue  # Block ohne verbliebene Zeilen
        if z.startswith("## Lauf"):
            out.append("")
        out.append(z)
    verlauf.write_text("\n".join(out) + "\n", encoding="utf-8")


def _material_report(ergebnisse: list[dict]) -> None:
    """docs/MATERIAL_REPORT.md — je Plan eine Sektion, idempotent ersetzt."""
    pfad = REPO / "docs" / "MATERIAL_REPORT.md"
    alt = pfad.read_text(encoding="utf-8") if pfad.exists() else ""
    sektionen: dict[str, str] = {}
    for block in re.split(r"^(?=# Plan )", alt, flags=re.MULTILINE):
        m = re.match(r"# Plan (\S+)", block)
        if m:
            sektionen[m.group(1)] = block.rstrip()
    for r in ergebnisse:
        abd = r.get("abdeckung")
        kopf = [f"# Plan {r['plan']}", "",
                "Legendenabdeckung: "
                + (f"{abd * 100:.1f} %" if abd is not None else "—")
                + f" · unbekannte Muster: {r.get('unbekannte_muster', 0)}"]
        sektionen[r["plan"]] = "\n".join(kopf + r.get("material_md", []))
    out = ["<!-- generiert von scripts/plan_pruefen.py — nicht von Hand pflegen -->",
           "", *(sektionen[k] + "\n" for k in sorted(sektionen))]
    pfad.write_text("\n".join(out), encoding="utf-8")


def main() -> int:
    dateien = ([Path(sys.argv[1])] if len(sys.argv) > 1
               else sorted(EINGANG.glob("*.dxf")))
    ERGEBNIS.mkdir(parents=True, exist_ok=True)
    commit = _git_hash()
    ergebnisse = []
    for dxf in dateien:
        print(f"== {dxf.name} ==")
        r = plan_pruefen(dxf)
        abd = r.get("abdeckung")
        print(f"   {r['stempel']} Stempel, {r['raeume']} Räume, {r['rest']} Rest, "
              f"{r['flags']} Flags, Abdeckung "
              + (f"{abd * 100:.1f} %" if abd is not None else "—")
              + f", {r['unbekannte_muster']} unbek. Muster, {r['laufzeit']:.1f} s")
        print(f"   Kaskade: gesamt {r['raeume_gesamt']}, mit Stempel "
              f"{r['mit_stempel']}, Flag ok {r['flag_ok']}, Rest typisiert "
              f"{r['rest_typisiert']} / untypisiert {r['rest_untypisiert']} "
              f"({r['quellen_mix']})")
        ergebnisse.append(r)
    if ergebnisse:
        _verlauf_schreiben(ergebnisse, commit)
        _material_report(ergebnisse)
    return 0


if __name__ == "__main__":
    sys.exit(main())
