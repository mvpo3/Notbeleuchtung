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
from shapely.geometry import Polygon

from notbeleuchtung.raumerkennung.dxf_load import DxfPlan, lade_dxf
from notbeleuchtung.raumerkennung.raumlayer import raeume_aus_layer
from notbeleuchtung.raumerkennung.stempel_anker import (
    Zuordnung,
    finde_stempel,
    ordne_zu,
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


def _varianten_bounds(plan: DxfPlan, stempel) -> tuple[float, float, float, float] | None:
    """Bounds (Plan-Koordinaten) der Entities auf den Stempel-Layern.

    Barawitzka trägt drei Planvarianten nebeneinander im Modelspace; nur die
    Variante mit den Stempeln ('0._EG PP_2_*') soll gerendert werden."""
    layers = [s.layer for s in stempel if s.layer]
    if not layers:
        return None
    # Basis: die Stempel-Positionen selbst (TEXT/MTEXT liefern keine entity_points).
    xs = [s.position_mm[0] / plan.factor for s in stempel]
    ys = [s.position_mm[1] / plan.factor for s in stempel]
    # Varianten-Prefix: Stempel-Layer '0._EG PP_2_810 Raum' → '0._EG PP_2_'
    # (alle Layer der Variante teilen den Prefix vor der Layer-Nummer).
    m = re.match(r"(.*_)\d+ ", os.path.commonprefix(layers))
    if m and len(m.group(1)) >= 4:
        for e in plan.space:
            if e.dxf.layer.startswith(m.group(1)):
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
                   ztop: float, labels_xy: list) -> None:
    """Halbtransparente Füllung + optionales Label am Zentroid — über dem Render."""
    xs = [p[0] / plan.factor for p in punkte_mm]
    ys = [p[1] / plan.factor for p in punkte_mm]
    ax.fill(xs, ys, color=farbe, alpha=0.4, ec=farbe, lw=1.5, zorder=ztop)
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

def iou(poly_a: list, poly_b: list) -> float:
    """Intersection over Union zweier Punktlisten-Polygone (mm)."""
    a, b = Polygon(poly_a).buffer(0), Polygon(poly_b).buffer(0)
    if a.is_empty or b.is_empty:
        return 0.0
    u = a.union(b).area
    return a.intersection(b).area / u if u > 0 else 0.0


def referenz_vergleich(referenz: list[dict], raeume) -> list[tuple[str, float]]:
    """Je Referenz-Raum die beste IoU gegen die erkannten Polygone."""
    out = []
    for ref in referenz:
        best = max((iou(ref["polygon_mm"], r.polygon_mm) for r in raeume
                    if len(r.polygon_mm) >= 3), default=0.0)
        out.append((ref.get("name") or ref.get("id", "?"), best))
    return out


# ---------------------------------------------------------------- Hauptlauf

def _raeume(plan: DxfPlan) -> tuple[list, str]:
    raeume = raeume_aus_layer(plan)
    if raeume:
        return raeume, "raumlayer"
    try:
        from notbeleuchtung.raumerkennung.waende import raeume_aus_waenden
        return raeume_aus_waenden(plan), "waende"
    except Exception as exc:  # noqa: BLE001 — Fallback darf den Lauf nie killen
        return [], f"waende-fallback fehlgeschlagen: {exc}"


def _json_eintraege(zuordnungen: list[Zuordnung], rest) -> list[dict]:
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
            "quelle": st.quelle,
        })
    for r in rest:
        out.append({
            "id": r.id, "typ": r.raum_typ or None, "name": None,
            "polygon_mm": [list(p) for p in r.polygon_mm],
            "flaeche_stempel": None, "flaeche_berechnet": r.flaeche_m2,
            "abweichung_prozent": None, "flag": "kein_stempel",
            "quelle": "restflaeche",
        })
    return out


def plan_pruefen(dxf: Path) -> dict:
    t0 = time.time()
    name = dxf.stem
    ziel = ERGEBNIS / name
    ziel.mkdir(parents=True, exist_ok=True)

    plan = lade_dxf(dxf)
    stempel = finde_stempel(plan)
    raeume, raum_quelle = _raeume(plan)
    zuordnungen = ordne_zu(stempel, raeume)
    rest = restflaechen(raeume, zuordnungen)
    rot, rot_vermerk = _rotation(plan)

    zoom = _varianten_bounds(plan, stempel)

    # 01: Plan wie geplottet + Meterraster.
    fig, ax = _figur(plan, zoom)
    _meterraster(ax, plan)
    _speichern(fig, ziel / "01_render.png", rot)

    # 02: erkannte Räume eingefärbt (Label nur ab 4 m², sonst Clutter).
    fig, ax = _figur(plan, zoom)
    _meterraster(ax, plan)
    ztop, labels_xy = _ztop(ax), []
    for n, z in enumerate(zuordnungen):
        if z.raum is None or len(z.raum.polygon_mm) < 3:
            continue
        st = z.stempel
        if z.raum.flaeche_m2 >= 4.0:
            lbl = (f"{st.name}\nStempel: {st.flaeche_m2:.1f} m²" if st.flaeche_m2
                   else st.name)
            lbl += f" / berechnet: {z.raum.flaeche_m2:.1f} m²"
        else:
            lbl = ""
        _poly_zeichnen(ax, z.raum.polygon_mm, _FARBEN[n % len(_FARBEN)], lbl, plan,
                       ztop, labels_xy)
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

    eintraege = _json_eintraege(zuordnungen, rest)
    (ziel / "raeume.json").write_text(
        json.dumps(eintraege, ensure_ascii=False, indent=2), encoding="utf-8")

    # Referenz-IoU (optional).
    iou_zeilen, iou_mittel = [], None
    ref_datei = dxf.with_name(f"{name}.referenz.json")
    if ref_datei.exists():
        ref = json.loads(ref_datei.read_text(encoding="utf-8"))
        iou_zeilen = referenz_vergleich(ref, raeume)
        if iou_zeilen:
            iou_mittel = sum(v for _, v in iou_zeilen) / len(iou_zeilen)

    laufzeit = time.time() - t0
    _bericht(ziel / "bericht.md", name, zuordnungen, rest, raum_quelle,
             rot_vermerk, iou_zeilen, iou_mittel, laufzeit, len(raeume))
    flags = sum(1 for z in zuordnungen if z.flag != "ok")
    # Zählung aus derselben Quelle wie raeume.json: Stempel-Einträge + Rest-Einträge.
    rest_n = sum(1 for e in eintraege if e["quelle"] == "restflaeche")
    return {"plan": name, "stempel": len(stempel),
            "raeume": len(eintraege) - rest_n,
            "rest": rest_n, "flags": flags, "iou_mittel": iou_mittel,
            "laufzeit": laufzeit}


def _bericht(pfad: Path, name: str, zuordnungen: list[Zuordnung], rest,
             raum_quelle: str, rot_vermerk: str,
             iou_zeilen, iou_mittel, laufzeit: float, n_raeume: int = 0) -> None:
    l = [f"# Prüfbericht {name}", "",
         f"Raum-Polygon-Quelle: `{raum_quelle}` — {rot_vermerk}", ""]
    if zuordnungen and n_raeume * 5 < len(zuordnungen):
        l += [("**Bekannte Lücke:** Raumerkennung deckt den Plan nicht ab "
               f"(nur {n_raeume} Polygone bei {len(zuordnungen)} Stempeln) — "
               "HATCH-basierte Räume werden noch nicht erkannt."), ""]
    l += [
         "## Stempel", "",
         "| Name | Typ | m² Stempel | m² Polygon | Abw. % | Flag |",
         "|---|---|--:|--:|--:|---|"]
    for z in zuordnungen:
        st = z.stempel
        l.append("| {} | {} | {} | {} | {} | {} |".format(
            " / ".join(st.name.replace("|", "/").splitlines()), st.typ or "—",
            f"{st.flaeche_m2:.2f}" if st.flaeche_m2 is not None else "—",
            f"{z.raum.flaeche_m2:.2f}" if z.raum else "—",
            f"{z.abweichung_prozent:+.1f}" if z.abweichung_prozent is not None else "—",
            z.flag))
    l += ["", f"## Restflächen ohne Stempel ({len(rest)})", ""]
    for r in rest:
        cx, cy = zentrum(r)
        l.append(f"- {r.id}: {r.flaeche_m2:.2f} m², Zentrum ({cx / 1000:.2f}, {cy / 1000:.2f}) m")
    warn = [f"Stempel ohne Polygon: „{z.stempel.name}“"
            for z in zuordnungen if z.polygon_index is None]
    warn += [f"Polygon ohne Stempel: {r.id} ({r.flaeche_m2:.2f} m²)" for r in rest]
    warn += [f"Abweichung > 10 %: „{z.stempel.name}“ ({z.abweichung_prozent:+.1f} %)"
             for z in zuordnungen
             if z.abweichung_prozent is not None and abs(z.abweichung_prozent) > 10]
    l += ["", f"## Warnungen ({len(warn)})", ""]
    l += [f"- {w}" for w in warn] or ["- keine"]
    if iou_zeilen:
        l += ["", "## Referenz-Vergleich (IoU)", "", "| Raum | IoU |", "|---|--:|"]
        l += [f"| {n} | {v:.3f} |" for n, v in iou_zeilen]
        l += ["", f"**Mittelwert: {iou_mittel:.3f}**"]
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
        zeilen.append(f"- {stamp[:10]} · {commit} · {r['plan']}: {r['stempel']} Stempel, "
                      f"{r['raeume']} Räume, {r['rest']} Restflächen, IoU-Mittel {iou_txt}")
    out = ["# Verlauf plan_pruefen"]
    for i, z in enumerate(zeilen):
        if z.startswith("## Lauf") and (i + 1 >= len(zeilen)
                                        or zeilen[i + 1].startswith("## Lauf")):
            continue  # Block ohne verbliebene Zeilen
        if z.startswith("## Lauf"):
            out.append("")
        out.append(z)
    verlauf.write_text("\n".join(out) + "\n", encoding="utf-8")


def main() -> int:
    dateien = ([Path(sys.argv[1])] if len(sys.argv) > 1
               else sorted(EINGANG.glob("*.dxf")))
    ERGEBNIS.mkdir(parents=True, exist_ok=True)
    commit = _git_hash()
    ergebnisse = []
    for dxf in dateien:
        print(f"== {dxf.name} ==")
        r = plan_pruefen(dxf)
        print(f"   {r['stempel']} Stempel, {r['raeume']} Räume, {r['rest']} Rest, "
              f"{r['flags']} Flags, {r['laufzeit']:.1f} s")
        ergebnisse.append(r)
    if ergebnisse:
        _verlauf_schreiben(ergebnisse, commit)
    return 0


if __name__ == "__main__":
    sys.exit(main())
