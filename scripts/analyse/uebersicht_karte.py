"""uebersicht_karte — eine Übersichtskarte je Grundriss: was die Raumerkennung erkennt.

Aufruf:
    python scripts/analyse/uebersicht_karte.py [<dxf>] [--floor X] [--out <verzeichnis>]

Ohne <dxf>: alle DXF aus Projekte/_eingang/. Ausgabe je Plan nach
Projekte/_uebersicht/<planname>/ (uebersicht.png, uebersicht.json, uebersicht.md).

Die Karte zeigt AUSSCHLIESSLICH, was ``ArchitekturRaumProvider.parse`` liefert.
Kein Norm-Urteil: Ausgänge werden nach ``Ausgang.typ`` (final_exit/stair_exit)
markiert, nicht nach fachlicher Einschätzung. Was nicht erkannt wurde, steht als
"nicht erkannt" in Karte und Bericht — nichts wird ergänzt oder geraten.

Laden/Rotation/Maßstab/Varianten-Zoom kommen 1:1 aus scripts/plan_pruefen.py
(``_figur``, ``_rotation``, ``_varianten_bounds``, ``_ztop``) — eine
Quelle der Wahrheit. Der Modelspace wird pro Plan GENAU EINMAL gerendert.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import traceback
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO / "scripts"))
sys.stdout.reconfigure(encoding="utf-8")

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import Collection
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.text import Text
from shapely.geometry import Polygon

import plan_pruefen as pp  # Wiederverwendung der Prüfstrecken-Helfer

EINGANG = REPO / "Projekte" / "_eingang"
AUSGABE = REPO / "Projekte" / "_uebersicht"

# ---------------------------------------------------------------- Kategorien

#: raum_typ → Kategorie. Alles Typisierte, was hier nicht steht, ist "nebenraum".
_GRUPPE: dict[str, str] = {
    "ZIMMER": "wohnen", "KÜCHE": "wohnen", "WOHNKÜCHE": "wohnen",
    "WOHNZIMMER": "wohnen", "SCHLAFZIMMER": "wohnen", "ESSZIMMER": "wohnen",
    "BAD": "sanitaer", "WC": "sanitaer", "DUSCHE": "sanitaer",
    "BALKON": "aussen", "TERRASSE": "aussen", "LOGGIA": "aussen",
    "GARTEN": "aussen", "GARTENFLÄCHE": "aussen",
    "GANG": "gang", "VORRAUM": "gang", "AUFZUGSVORPLATZ": "gang",
    "STIEGENHAUS": "stiege",
    "SCHACHT": "schacht", "LIFT": "schacht",
}

#: Kategorie → (Legendentext, Füllfarbe, Konturfarbe). Reihenfolge = Legende.
_KAT: dict[str, tuple[str, str, str]] = {
    "wohnen":      ("Wohnräume (ZIMMER/KÜCHE/…)", "#6fa8dc", "#2b5f96"),
    "sanitaer":    ("Sanitär (BAD/WC)", "#7fd4c1", "#2c8c78"),
    "nebenraum":   ("sonstige typisierte Räume", "#c9b6e4", "#6c4f9c"),
    "aussen":      ("Außenflächen (BALKON/TERRASSE)", "#a9dfbf", "#2e7d4f"),
    "gang":        ("Gänge (GANG/VORRAUM/AUFZUGSVORPLATZ)", "#f6c445", "#9a7400"),
    "stiege":      ("Stiegenhäuser", "#e8743b", "#8c3a10"),
    "schacht":     ("Schächte/Lifte", "#a3785a", "#5a3a22"),
    "untypisiert": ("untypisierte Räume (nicht erkannt)", "#ff2ec4", "#8b0060"),
}

_HOF_FC, _HOF_EC = "#4fa3d1", "#1d5c85"
# tab10 + Dark2 = 18 klar unterscheidbare Farben; tab20 wäre paarweise
# zu ähnlich (top_3/top_4 nicht trennbar — Sichtbefund Barawitzka).
# Rot (tab10[3]) fliegt raus: kollidiert optisch mit Fluchtweg + Überlappung.
_WOHNUNG_FARBEN = ([c for i, c in enumerate(plt.cm.tab10.colors) if i != 3]
                   + list(plt.cm.Dark2.colors))  # type: ignore[attr-defined]
_EXIT_FARBE = {"final_exit": "#00a000", "stair_exit": "#ff8c00", "door": "#777777"}
_FLW_FARBE = "#d21f3c"
_UEBER_FARBE = "#ff0000"
_UEBERLAPPUNG_SCHWELLE = 0.90
_GRAU = "#b4b4b4"


def _kategorie(raum) -> str:
    if not raum.raum_typ:
        return "untypisiert"
    return _GRUPPE.get(raum.raum_typ.upper(), "nebenraum")


def _verschluckt(raeume) -> list[dict]:
    """Räume, die zu > 90 % der eigenen Fläche in einem anderen Raum liegen."""
    geo = [(r, Polygon(r.polygon_mm).buffer(0)) for r in raeume
           if len(r.polygon_mm) >= 3]
    geo = [(r, g) for r, g in geo if g.area > 0]
    out = []
    for r, g in geo:
        for r2, g2 in geo:
            if r2.id == r.id or not g.intersects(g2):
                continue
            anteil = g.intersection(g2).area / g.area
            if anteil > _UEBERLAPPUNG_SCHWELLE:
                out.append({"raum_id": r.id, "raum_typ": r.raum_typ or None,
                            "in_raum_id": r2.id, "in_raum_typ": r2.raum_typ or None,
                            "anteil_prozent": round(anteil * 100, 1)})
    return out


# ---------------------------------------------------------------- Bild

def _hintergrund_ausgrauen(ax) -> None:
    """Den fertigen ezdxf-Render auf Hellgrau ziehen — der Plan ist Kulisse."""
    for a in ax.get_children():
        if isinstance(a, Line2D):
            a.set_color(_GRAU)
        elif isinstance(a, Collection):
            a.set_color(_GRAU)
            a.set_alpha(0.55)
        elif isinstance(a, Patch):
            a.set_facecolor("none")
            a.set_edgecolor(_GRAU)
        elif isinstance(a, Text):
            a.set_color("#9a9a9a")


def _dpi_fuer(plan, ax) -> int:
    """Mehr Pixel für große Pläne: 150 dpi (1800 px) bis 200 dpi (2400 px)."""
    x0, x1 = ax.get_xlim()
    span_m = abs(x1 - x0) * plan.factor / 1000.0
    return 150 if span_m < 60 else 200


def _schriftgroesse(ax, plan) -> float:
    x0, x1 = ax.get_xlim()
    span_m = abs(x1 - x0) * plan.factor / 1000.0
    return max(5.5, min(11.0, 340.0 / max(span_m, 1.0)))


def _text(ax, cx, cy, label: str, fs: float, z: float, labels_xy: list, achse,
          farbe: str = "black", fc: str | tuple = "white", fett: bool = False) -> bool:
    """Label MITTIG IM Polygon (representative_point), Kollisionen werden
    übersprungen statt verschoben — lieber kein Label als ein falsch sitzendes."""
    x0, x1 = achse.get_xlim()
    d2 = (0.022 * (x1 - x0)) ** 2
    if any((cx - lx) ** 2 + (cy - ly) ** 2 < d2 for lx, ly in labels_xy):
        return False
    labels_xy.append((cx, cy))
    ax.text(cx, cy, label, ha="center", va="center", fontsize=fs, color=farbe,
            fontweight="bold" if fett else "normal", zorder=z,
            bbox={"fc": fc, "alpha": 0.75, "ec": "none", "pad": 1.5})
    return True


def _pfeil(ax, xy, grad, farbe, z, laenge) -> None:
    import math
    dx = math.cos(math.radians(grad)) * laenge
    dy = math.sin(math.radians(grad)) * laenge
    ax.annotate("", xy=(xy[0] + dx, xy[1] + dy), xytext=xy, zorder=z,
                arrowprops={"arrowstyle": "-|>", "color": farbe, "lw": 2.0})


def _legende(fig, ax, zaehl: dict, n_wohnungen: int) -> None:
    h = [Patch(fc=fc, ec=ec, alpha=0.55, label=f"{txt} — {zaehl.get(k, 0)}")
         for k, (txt, fc, ec) in _KAT.items()]
    h.append(Patch(fc=_HOF_FC, ec=_HOF_EC, alpha=0.55, hatch="//",
                   label=f"Innenhöfe (geschlossene Außenflächen) — {zaehl.get('hof', 0)}"))
    h.append(Line2D([], [], color="#7b68ee", lw=2.5,
                    label=f"Wohnungen (Umriss, je Wohnung eigene Farbe) — {n_wohnungen}"))
    h.append(Line2D([], [], color=_EXIT_FARBE["final_exit"], marker="*", ls="none",
                    ms=16, mec="black",
                    label=f"Ausgang final_exit (ins Freie) — {zaehl.get('final_exit', 0)}"))
    h.append(Line2D([], [], color=_EXIT_FARBE["stair_exit"], marker="s", ls="none",
                    ms=11, mec="black",
                    label=f"Ausgang stair_exit (ins Stiegenhaus) — {zaehl.get('stair_exit', 0)}"))
    h.append(Line2D([], [], color=_EXIT_FARBE["door"], marker="o", ls="none",
                    ms=9, mec="black",
                    label=f"Ausgang door — {zaehl.get('door', 0)}"))
    h.append(Line2D([], [], color=_FLW_FARBE, lw=1.8,
                    label=f"Fluchtweg-Zirkulation (Segmente) — {zaehl.get('segmente', 0)}"))
    h.append(Line2D([], [], color=_UEBER_FARBE, lw=2.2, ls=(0, (4, 2)),
                    label=f"verschluckt (> 90 % in anderem Raum) — {zaehl.get('ueberlappung', 0)}"))
    ax.legend(handles=h, loc="upper left", fontsize=9, framealpha=0.92,
              facecolor="white", edgecolor="#444444", borderpad=0.8,
              labelspacing=0.55, title="Erkannte Kategorien",
              title_fontproperties={"weight": "bold", "size": 10})


def _inhalts_bounds(plan, modell, hoefe, rand=0.06):
    """Bounds (Plan-Koordinaten) dessen, was die Karte ZEIGT: Raumpolygone,
    Ausgänge, Fluchtweg, Höfe.

    Die Variantenbounds aus ``plan_pruefen`` spannen den ganzen Layer-Satz auf.
    Trägt eine Zeichnung zusätzliche Plankoepfe oder einen Lageplan (Muthgasse),
    schrumpft der Grundriss darin auf einen Fleck. Hier zaehlt nur, was auch
    beschriftet wird.

    ``None``, wenn nichts erkannt wurde — dann bleibt es beim alten Zoom, damit
    ein leeres Ergebnis nicht in einen leeren Ausschnitt hineinzoomt.
    """
    f = plan.factor
    xs: list[float] = []
    ys: list[float] = []

    def _nimm(koordinaten):
        for x, y in koordinaten:
            xs.append(x / f)
            ys.append(y / f)

    for r in modell.raeume:
        if r.polygon_mm and len(r.polygon_mm) >= 3:
            _nimm(r.polygon_mm)
    for a in modell.ausgaenge:
        _nimm([a.xy_mm])
    for seg in modell.zirkulation.segmente:
        _nimm(getattr(seg, "polyline_mm", None) or [])
    for h in hoefe:
        _nimm(h.exterior.coords)

    if not xs:
        return None
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    dx, dy = max(x1 - x0, 1.0), max(y1 - y0, 1.0)
    m = rand * max(dx, dy)
    return x0 - m, x1 + m, y0 - m, y1 + m


def _haupt_cluster(modell, plan, abstand_mm=5000.0):
    """Bounds des flaechengroessten zusammenhaengenden Raum-Clusters.

    Manche Zeichnungen tragen mehrere Planvarianten oder Detailauszuege auf
    EINEM Blatt (Muthgasse). Die Erkennung findet dann in jeder davon Raeume,
    und ein Ausschnitt ueber alle Raeume zeigt nur noch Briefmarken. Hier
    gewinnt der Cluster mit der groessten Raumflaeche — das ist der Grundriss,
    die anderen sind Beiwerk.

    Rueckgabe: (bounds, raeume_ausserhalb) oder (None, 0), wenn es nur einen
    Cluster gibt bzw. nichts erkannt wurde.
    """
    from shapely.geometry import Polygon
    from shapely.ops import unary_union

    polys = []
    for r in modell.raeume:
        if r.polygon_mm and len(r.polygon_mm) >= 3:
            g = Polygon(r.polygon_mm)
            if not g.is_valid:
                g = g.buffer(0)
            if not g.is_empty and g.area > 0:
                polys.append(g)
    if len(polys) < 2:
        return None, 0

    huellen = unary_union([g.buffer(abstand_mm) for g in polys])
    teile = list(getattr(huellen, "geoms", [huellen]))
    if len(teile) < 2:
        return None, 0

    bestes, beste_flaeche = None, -1.0
    for t in teile:
        fl = sum(g.area for g in polys if t.contains(g.representative_point()))
        if fl > beste_flaeche:
            bestes, beste_flaeche = t, fl
    draussen = sum(1 for g in polys
                   if not bestes.contains(g.representative_point()))

    f = plan.factor
    x0, y0, x1, y1 = bestes.bounds
    return (x0 / f, x1 / f, y0 / f, y1 / f), draussen


def _karte(plan, zoom, rot, modell, hoefe, wpolys, ueber, ziel: Path,
           titel: str) -> tuple[int, int]:
    """Ein Render des Modelspace, Overlays drauf, danach Rotation + Legende.

    Rückgabe: (Breite, Höhe) in Pixeln.
    """
    f = plan.factor
    fig, ax = pp._figur(plan, zoom)
    fig.set_dpi(_dpi_fuer(plan, ax))
    _hintergrund_ausgrauen(ax)
    ax.autoscale(False)
    ztop = pp._ztop(ax)
    labels_xy: list = []

    verschluckte = {u["raum_id"] for u in ueber}
    zaehl: Counter[str] = Counter()
    fs = _schriftgroesse(ax, plan)

    # Wohnungs-Beschriftung zuerst: sie belegt ihren Platz, Raum-Labels weichen aus.
    for i, (wid, geom) in enumerate(sorted(wpolys.items())):
        farbe = _WOHNUNG_FARBEN[i % len(_WOHNUNG_FARBEN)]
        rp = geom.representative_point()
        _text(ax, rp.x / f, rp.y / f, wid, fs + 1, ztop + 6, labels_xy, ax,
              fc=farbe, fett=True)

    # Räume — große zuerst, kleine liegen oben drauf.
    for r in sorted(modell.raeume, key=lambda r: -r.flaeche_m2):
        if len(r.polygon_mm) < 3:
            continue
        k = _kategorie(r)
        zaehl[k] += 1
        _txt, fc, ec = _KAT[k]
        xs0 = [p[0] / f for p in r.polygon_mm]
        ys0 = [p[1] / f for p in r.polygon_mm]
        ax.fill(xs0, ys0, color=fc, alpha=0.45, ec=ec, lw=1.5, zorder=ztop)
        if r.flaeche_m2 >= 2.0:
            lbl = r.raum_typ or f"nicht erkannt\n{r.id}"
            g = Polygon(r.polygon_mm).buffer(0)
            if not g.is_empty:
                rp = g.representative_point()
                _text(ax, rp.x / f, rp.y / f, lbl, fs, ztop + 3, labels_xy, ax,
                      farbe=ec if k == "untypisiert" else "black",
                      fett=k == "untypisiert")
        if k == "untypisiert":  # auffällige Signatur: nichts erkannt
            xs = [p[0] / f for p in r.polygon_mm]
            ys = [p[1] / f for p in r.polygon_mm]
            ax.fill(xs, ys, facecolor="none", ec=_KAT[k][2], lw=2.0,
                    hatch="xx", zorder=ztop + 2)
        if r.id in verschluckte:
            xs = [p[0] / f for p in r.polygon_mm]
            ys = [p[1] / f for p in r.polygon_mm]
            ax.plot(xs + xs[:1], ys + ys[:1], color=_UEBER_FARBE, lw=2.2,
                    ls=(0, (4, 2)), zorder=ztop + 4)

    # Innenhöfe (nur über provider.letzte_aussenbereiche greifbar).
    for g in hoefe:
        zaehl["hof"] += 1
        for gg in getattr(g, "geoms", [g]):
            xs, ys = zip(*[(x / f, y / f) for x, y in gg.exterior.coords])
            ax.fill(xs, ys, facecolor=_HOF_FC, alpha=0.4, ec=_HOF_EC, lw=2.0,
                    hatch="//", zorder=ztop + 1)

    # Wohnungen: Umriss je Wohnung in eigener Farbe (Label steht schon oben).
    for i, (wid, geom) in enumerate(sorted(wpolys.items())):
        farbe = _WOHNUNG_FARBEN[i % len(_WOHNUNG_FARBEN)]
        for g in getattr(geom, "geoms", [geom]):
            xs, ys = zip(*[(x / f, y / f) for x, y in g.exterior.coords])
            ax.plot(xs, ys, color=farbe, lw=3.0, zorder=ztop + 5)

    # Fluchtweg-Zirkulation.
    for s in modell.zirkulation.segmente:
        if len(s.polyline_mm) < 2:
            continue
        zaehl["segmente"] += 1
        ax.plot([x / f for x, _ in s.polyline_mm], [y / f for _, y in s.polyline_mm],
                color=_FLW_FARBE, lw=1.8, alpha=0.9,
                ls="--" if s.richtung_unbekannt else "-", zorder=ztop + 7)

    # Ausgänge. Richtungssinn nur, wenn das Modell ihn führt (Anker.fluchtrichtung_grad).
    anker = [a for a in modell.anker if a.fluchtrichtung_grad is not None]
    pfeil_len = 0.02 * abs(ax.get_xlim()[1] - ax.get_xlim()[0])
    for a in modell.ausgaenge:
        zaehl[a.typ] += 1
        x, y = a.xy_mm[0] / f, a.xy_mm[1] / f
        stil = {"final_exit": ("*", 26), "stair_exit": ("s", 15),
                "door": ("o", 12)}.get(a.typ, ("o", 12))
        ax.plot(x, y, marker=stil[0], ms=stil[1], mfc=_EXIT_FARBE.get(a.typ, "#777"),
                mec="black", mew=1.6, ls="none", zorder=ztop + 8)
        ax.text(x, y, "  " + a.typ, ha="left", va="center", fontsize=8,
                color="black", zorder=ztop + 9,
                bbox={"fc": "white", "alpha": 0.75, "ec": "none", "pad": 1})
        nah = [k for k in anker
               if abs(k.xy_mm[0] - a.xy_mm[0]) + abs(k.xy_mm[1] - a.xy_mm[1]) < 1500.0]
        if nah:
            _pfeil(ax, (x, y), nah[0].fluchtrichtung_grad, _FLW_FARBE,
                   ztop + 9, pfeil_len)

    zaehl["ueberlappung"] = len(ueber)

    # EIN Render: Bild rendern, rotieren, dann Legende + Titel obendrauf.
    tmp = ziel / "_uebersicht_raw.png"
    fig.savefig(str(tmp), facecolor="white", dpi=fig.dpi)
    plt.close(fig)
    img = plt.imread(str(tmp))
    if rot:
        img = np.rot90(img, rot)
    tmp.unlink()

    dpi = 100
    fig2 = plt.figure(figsize=(img.shape[1] / dpi, img.shape[0] / dpi), dpi=dpi)
    ax2 = fig2.add_axes([0, 0, 1, 1])
    ax2.set_axis_off()
    ax2.imshow(img, interpolation="none")
    _legende(fig2, ax2, zaehl, len(wpolys))
    # Titel unten mittig — oben links sitzt die Legende (Kollision Barawitzka).
    ax2.text(0.5, 0.006, titel, transform=ax2.transAxes, ha="center", va="bottom",
             fontsize=13, fontweight="bold",
             bbox={"fc": "white", "alpha": 0.9, "ec": "#444444", "pad": 4})
    fig2.savefig(str(ziel / "uebersicht.png"), facecolor="white")
    plt.close(fig2)
    return img.shape[1], img.shape[0]


# ---------------------------------------------------------------- Bericht

def _md(name: str, daten: dict) -> str:
    z = daten["kategorien"]
    zeilen = [f"# Übersicht — {name}", "",
              (f"DXF: `{daten['dxf']}` · Geschoss: `{daten['floor']}` · "
               f"Bild: {daten['bild_px'][0]}×{daten['bild_px'][1]} px · "
               f"Laufzeit {daten['laufzeit_s']:.1f} s"), "",
              "## Erkannte Kategorien", "",
              "| Kategorie | Anzahl |", "|---|---:|"]
    for k, (txt, _fc, _ec) in _KAT.items():
        zeilen.append(f"| {txt} | {z.get(k, 0)} |")
    zeilen += [
        f"| Innenhöfe (geschlossene Außenflächen) | {z.get('hof', 0)} |",
        f"| Wohnungen | {daten['wohnungen']['anzahl']} |",
        f"| Ausgänge final_exit | {z.get('final_exit', 0)} |",
        f"| Ausgänge stair_exit | {z.get('stair_exit', 0)} |",
        f"| Ausgänge door | {z.get('door', 0)} |",
        f"| Fluchtweg-Segmente | {z.get('segmente', 0)} |",
        f"| Räume > 90 % in anderem Raum | {z.get('ueberlappung', 0)} |",
        "", (f"Räume gesamt: **{daten['raeume_gesamt']}**, davon typisiert "
             f"{daten['raeume_typisiert']}."), ""]

    if daten["raum_typen"]:
        zeilen += ["## raum_typ im Detail", "", "| raum_typ | Anzahl |", "|---|---:|"]
        for t, n in sorted(daten["raum_typen"].items(), key=lambda kv: (-kv[1], kv[0])):
            zeilen.append(f"| {t} | {n} |")
        zeilen.append("")

    w = daten["wohnungen"]
    if w["anzahl"]:
        zeilen += ["## Wohnungen", "", "| Wohnung | Räume |", "|---|---:|"]
        for wid, n in sorted(w["raeume_je_wohnung"].items()):
            hinweis = "  ⚠ nur 1 Raum — Zusammenhang unsicher" if n == 1 else ""
            zeilen.append(f"| {wid} | {n}{hinweis} |")
        zeilen += ["", f"Räume ohne `wohnung_id`: {w['ohne_wohnung']}", ""]

    if daten["ueberlappungen"]:
        zeilen += ["## Überlappungen (> 90 % der eigenen Fläche)", "",
                   "| Raum | Typ | liegt in | Typ | Anteil |", "|---|---|---|---|---:|"]
        for u in daten["ueberlappungen"]:
            zeilen.append(f"| {u['raum_id']} | {u['raum_typ'] or '—'} | "
                          f"{u['in_raum_id']} | {u['in_raum_typ'] or '—'} | "
                          f"{u['anteil_prozent']:.1f} % |")
        zeilen.append("")

    zeilen += ["## NICHT erkannt", ""]
    for t in daten["nicht_erkannt"]:
        zeilen.append(f"- {t}")
    zeilen.append("")
    return "\n".join(zeilen)


def _nicht_erkannt(daten: dict, modell, hoefe) -> list[str]:
    z = daten["kategorien"]
    out = []
    n_untyp = z.get("untypisiert", 0)
    out.append(f"**untypisierte Räume: {n_untyp}** — `raum_typ` leer, "
               f"`nutzungsklasse` unbestimmt. In der Karte magenta schraffiert."
               if n_untyp else "untypisierte Räume: 0 — jeder Raum trägt einen `raum_typ`.")
    for k in ("gang", "stiege", "schacht", "aussen"):
        if not z.get(k):
            out.append(f"{_KAT[k][0]}: **0** — nicht erkannt (kein Raum mit "
                       f"passendem `raum_typ`).")
    if not hoefe:
        out.append("Innenhöfe: **0** — `provider.letzte_aussenbereiche.geschlossen` "
                   "ist leer (oder es gab keine Wandkörper-Analyse).")
    if not z.get("final_exit"):
        out.append("`final_exit`: **0** — kein Ausgang ins Freie erkannt "
                   "(in Obergeschossen erwartungsgemäß, s. provider.py).")
    if not z.get("stair_exit"):
        out.append("`stair_exit`: **0** — kein Stiegenhaus-Ausgang erkannt.")
    if not z.get("door"):
        out.append("`Ausgang.typ == \"door\"`: **0** — wird von "
                   "`leite_ausgaenge` grundsätzlich nicht erzeugt.")
    if not daten["wohnungen"]["anzahl"]:
        out.append("Wohnungen: **0** — keine `wohnung_id` vergeben.")
    n_nodes = len(modell.zirkulation.nodes)
    out.append(f"Zirkulationsgraph: {n_nodes} Knoten / "
               f"{len(modell.zirkulation.edges)} Kanten"
               + (" — leer; die Segmente stammen aus dem Fluchtweg-Nachlauf, "
                  "nicht aus Plan-Layern `09-WEG*`." if n_nodes == 0 else "."))
    if not modell.sonderstellen:
        out.append("Sonderstellen (Feuerlöscher/Hydrant/Erste Hilfe): **0** — "
                   "dafür existiert kein automatischer Erzeuger.")
    out.append("„Ausgang führt auf die Straße\": wird NICHT geführt — das Modell "
               "kennt nur `final_exit`/`stair_exit`, keine Straßenzuordnung.")
    return out


# ---------------------------------------------------------------- Lauf

def karte_bauen(dxf: Path, floor: str | None, out: Path,
                name: str | None = None) -> dict:
    from notbeleuchtung.raumerkennung import ArchitekturRaumProvider

    t0 = time.time()
    name = name or dxf.stem
    ziel = out / name
    ziel.mkdir(parents=True, exist_ok=True)

    geschoss = floor or pp.geschoss_aus(None, str(dxf)) or "EG"
    provider = ArchitekturRaumProvider()
    modell = provider.parse(str(dxf), geschoss)
    ab = getattr(provider, "letzte_aussenbereiche", None)
    hoefe = list(ab.geschlossen) if ab is not None and ab.geschlossen else []

    plan = pp.lade_dxf(dxf)
    stempel = pp.finde_stempel(plan)
    prefix = pp._varianten_prefix(stempel)
    zoom = pp._varianten_bounds(plan, prefix, stempel)
    rot, rot_vermerk = pp._rotation(plan)

    # Auf das zoomen, was die Karte zeigt — siehe _inhalts_bounds.
    inhalt = _inhalts_bounds(plan, modell, hoefe)
    if inhalt is not None:
        zoom = inhalt
    # Mehrere Planvarianten auf einem Blatt: auf den groessten Cluster zoomen.
    haupt, ausserhalb = _haupt_cluster(modell, plan)
    if haupt is not None:
        zoom = haupt

    wpolys = pp._wohnungs_umrisse(modell)
    ueber = _verschluckt(modell.raeume)

    px = _karte(plan, zoom, rot, modell, hoefe, wpolys, ueber, ziel,
                f"{name} — Übersicht Raumerkennung (Geschoss {geschoss})")

    kat = Counter(_kategorie(r) for r in modell.raeume)
    kat.update({"hof": len(hoefe), "ueberlappung": len(ueber),
                "segmente": len(modell.zirkulation.segmente)})
    kat.update(Counter(a.typ for a in modell.ausgaenge))
    je_wohnung = Counter(r.wohnung_id for r in modell.raeume if r.wohnung_id)

    daten = {
        "plan": name,
        "dxf": str(dxf),
        "floor": geschoss,
        "contract_version": modell.contract_version,
        "bild_px": list(px),
        "rotation": rot_vermerk,
        "kategorien": dict(kat),
        "raeume_gesamt": len(modell.raeume),
        "raeume_typisiert": sum(1 for r in modell.raeume if r.raum_typ),
        "raum_typen": dict(Counter(r.raum_typ for r in modell.raeume if r.raum_typ)),
        "wohnungen": {"anzahl": len(wpolys),
                      "raeume_je_wohnung": dict(je_wohnung),
                      "ohne_wohnung": sum(1 for r in modell.raeume if not r.wohnung_id)},
        "innenhoefe_m2": [round(g.area / 1e6, 1) for g in hoefe],
        "ausgaenge": [{"id": a.id, "typ": a.typ, "xy_mm": list(a.xy_mm)}
                      for a in modell.ausgaenge],
        "stiegenhaeuser": [s.raum_id for s in modell.stiegenhaeuser],
        "ueberlappungen": ueber,
        "tueren_gesamt": len(modell.tueren),
        "laufzeit_s": round(time.time() - t0, 1),
        "raeume_ausserhalb_ausschnitt": ausserhalb,
    }
    daten["nicht_erkannt"] = _nicht_erkannt(daten, modell, hoefe)
    (ziel / "uebersicht.json").write_text(
        json.dumps(daten, ensure_ascii=False, indent=2), encoding="utf-8")
    (ziel / "uebersicht.md").write_text(_md(name, daten), encoding="utf-8")
    return daten


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("dxf", nargs="?", help="einzelne DXF; ohne = alle aus _eingang")
    ap.add_argument("--floor", default=None)
    ap.add_argument("--out", default=str(AUSGABE))
    ap.add_argument("--name", default=None,
                    help="Ausgabename statt DXF-Dateiname (nur mit <dxf>)")
    a = ap.parse_args()
    out = Path(a.out)
    plaene = [Path(a.dxf)] if a.dxf else sorted(EINGANG.glob("*.dxf"))
    if not plaene:
        print("keine DXF gefunden", file=sys.stderr)
        return 1
    fehler = 0
    for p in plaene:
        print(f"→ {p.stem} …", flush=True)
        try:
            d = karte_bauen(p, a.floor, out, a.name if a.dxf else None)
            print(f"   ok — {d['raeume_gesamt']} Räume, "
                  f"{d['bild_px'][0]}×{d['bild_px'][1]} px, {d['laufzeit_s']} s")
        except Exception as e:  # noqa: BLE001 — ein Plan darf den Sweep nicht kippen
            fehler += 1
            ziel = out / ((a.name if a.dxf else None) or p.stem)
            ziel.mkdir(parents=True, exist_ok=True)
            (ziel / "uebersicht.md").write_text(
                f"# Übersicht — {p.stem}\n\n**nicht auswertbar**\n\n"
                f"DXF: `{p}`\n\n```\n{traceback.format_exc()}\n```\n",
                encoding="utf-8")
            (ziel / "uebersicht.json").write_text(
                json.dumps({"plan": p.stem, "dxf": str(p), "fehler": repr(e)},
                           ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"   FEHLER: {e!r} — weiter", file=sys.stderr)
            plt.close("all")
    return 1 if fehler == len(plaene) else 0


if __name__ == "__main__":
    raise SystemExit(main())
